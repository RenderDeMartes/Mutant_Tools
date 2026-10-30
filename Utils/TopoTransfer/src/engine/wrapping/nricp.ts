/**
 * ARAP-regularised non-rigid ICP with stiffness annealing.
 * See docs/ALGORITHM.md for the energy and the reasoning behind it.
 *
 * The function only ever reads connectivity and returns a new positions array
 * of the same length; base topology and reference data are never modified.
 */

import { closestRotation } from '../core/mat3';
import { computeBBox } from '../core/mesh';
import { isBoundaryEdge, vertexNormals } from '../geometry/topology';
import { protectionWeights } from '../constraints/mask';
import { applyComponentModes, ComponentMode, fitVertexMask, FollowReport } from '../constraints/components';
import { checkSurfacePoint, evalSurfacePoint, isComplete, Landmark } from '../landmarks/landmarks';
import { pcg } from '../linalg/pcg';
import { makeHit, TriRegion } from '../spatial/bvh';
import { DistanceStats, pointToSurfaceDistances, qualityReport, QualityReport } from '../validation/metrics';
import { sanitizeParams, stiffnessSchedule, WrapParams } from './params';
import { BasePrep, prepareBase, prepareReference, RefPrep } from './prepare';

export interface WrapInput {
  /** rigidly aligned rest shape of the base (world / reference space) */
  baseRest: Float64Array;
  /** starting positions (usually equal to baseRest, or a previously committed result) */
  baseStart: Float64Array;
  baseTriangles: Uint32Array;
  refPositions: Float64Array;
  refTriangles: Uint32Array;
  landmarks?: Landmark[];
  /** painted region mask (0..1 per base vertex) */
  mask?: Float32Array | null;
  /** per connected component of the base (see BasePrep.components); null = fit everything */
  componentModes?: ComponentMode[] | null;
  params?: Partial<WrapParams>;
}

export interface WrapProgress {
  stage: 'setup' | 'fitting' | 'analysis';
  level: number;
  levels: number;
  iteration: number;
  iterationsPerLevel: number;
  /** 0..1 overall */
  fraction: number;
  message: string;
  rmsFit?: number;
}

export interface WrapHooks {
  onProgress?: (p: WrapProgress) => void;
  isCancelled?: () => boolean;
  /** awaited between iterations (lets a worker process cancel messages) */
  yieldControl?: () => Promise<void>;
  /** precomputed data reused across runs */
  basePrep?: BasePrep;
  refPrep?: RefPrep;
}

export interface IterationLog {
  level: number;
  iteration: number;
  lambda: number;
  accepted: number;
  acceptedFraction: number;
  reverseAccepted: number;
  /** RMS distance of accepted forward correspondences before the solve */
  rmsFit: number;
  cgIterations: number;
  cgResidual: number;
  maxDisplacement: number;
  energyBefore: number;
  energyAfter: number;
  ms: number;
  /** wall time per stage of this iteration (ms) */
  stages: { correspondences: number; reverse: number; rotations: number; assembly: number; multigrid: number; solve: number; energy: number };
}

export interface WrapDiagnostics {
  params: WrapParams;
  schedule: number[];
  iterations: IterationLog[];
  warnings: string[];
  seamPairs: number;
  landmarksUsed: number;
  /** how non-fitted components were placed */
  components: FollowReport[];
  amgLevels: number[];
  /** distance from base vertices to the reference surface (measured) */
  distanceBefore: DistanceStats;
  distanceAfter: DistanceStats;
  /** distance from reference vertices to the base surface (measured; coverage) */
  coverageBefore: DistanceStats;
  coverageAfter: DistanceStats;
  /** same as distanceAfter but restricted to vertices with an accepted correspondence in the last iteration */
  inlierDistanceAfter: DistanceStats;
  quality: QualityReport;
  timings: { setupMs: number; fitMs: number; analysisMs: number; totalMs: number };
  vertexCount: number;
  triangleCount: number;
}

export interface WrapResult {
  status: 'completed' | 'cancelled' | 'failed';
  message: string;
  positions: Float64Array;
  diagnostics: WrapDiagnostics | null;
}

const now = () => (typeof performance !== 'undefined' ? performance.now() : Date.now());

class WrapFailure extends Error {}

export async function wrapMesh(input: WrapInput, hooks: WrapHooks = {}): Promise<WrapResult> {
  const t0 = now();
  const params = sanitizeParams(input.params ?? {});
  const { baseRest, baseStart, baseTriangles, refPositions, refTriangles } = input;
  const n = baseRest.length / 3;
  const fail = (message: string): WrapResult => ({ status: 'failed', message, positions: baseStart.slice(), diagnostics: null });

  // ---------- input validation ----------
  if (n === 0 || baseRest.length % 3 !== 0) return fail('Base mesh has no vertices.');
  if (baseStart.length !== baseRest.length) return fail('Start and rest positions have different lengths.');
  if (baseTriangles.length === 0) return fail('Base mesh has no faces.');
  if (refTriangles.length === 0) return fail('Reference mesh has no faces.');
  for (const [name, arr] of [['base', baseStart], ['base rest', baseRest], ['reference', refPositions]] as const) {
    for (let i = 0; i < arr.length; i++) if (!Number.isFinite(arr[i])) return fail(`The ${name} positions contain NaN or infinite values.`);
  }
  for (let i = 0; i < baseTriangles.length; i++) if (baseTriangles[i] >= n) return fail('Base triangle index out of range.');
  const nRef = refPositions.length / 3;
  for (let i = 0; i < refTriangles.length; i++) if (refTriangles[i] >= nRef) return fail('Reference triangle index out of range.');
  if (input.mask && input.mask.length !== n) return fail('Region mask size does not match the base vertex count.');

  const report = (p: Omit<WrapProgress, 'levels' | 'iterationsPerLevel'>) =>
    hooks.onProgress?.({ ...p, levels: params.levels, iterationsPerLevel: params.iterationsPerLevel });
  report({ stage: 'setup', level: 0, iteration: 0, fraction: 0, message: 'Preparing meshes' });

  const base = hooks.basePrep ?? prepareBase(baseRest, baseTriangles, params.seamLock);
  const ref = hooks.refPrep ?? prepareReference(refPositions, refTriangles);
  if (base.n !== n) return fail('Cached base data does not match the base mesh.');
  const warnings: string[] = [];
  const modes = input.componentModes ?? null;
  if (modes && modes.length !== base.components.sizes.length) {
    return fail(`Component modes list has ${modes.length} entries but the base has ${base.components.sizes.length} components.`);
  }
  const fitMask = fitVertexMask(base.components, modes);
  const fitCount = fitMask.reduce((a, b) => a + b, 0);
  if (fitCount === 0) return fail('No component is set to Fit; nothing to wrap.');

  const refDiag = ref.diagonal || computeBBox(refPositions).diagonal;
  if (!(refDiag > 0)) return fail('Reference mesh has zero size.');
  const maxDist = params.maxCorrespondenceDistance * refDiag;
  const maxDistSq = maxDist * maxDist;
  const cosThr = Math.cos((params.normalThresholdDeg * Math.PI) / 180);
  const mu = params.normalAlignment;
  const schedule = stiffnessSchedule(params);
  const eps = 1e-3;

  // ---------- region weights ----------
  const hasMask = !!input.mask;
  const prot = protectionWeights(input.mask ?? null, params.maskMode, n);
  if (!hasMask && params.maskMode === 'fitOnly') {
    warnings.push('"Fit only painted region" is selected but no region is painted; the mask is ignored.');
    prot.fill(0);
  }
  const protStrength = Math.pow(10, 4 * params.regionInfluence - 2);
  const dataMul = new Float64Array(n);
  const anchor = new Float64Array(n);
  let protectedCount = 0;
  for (let i = 0; i < n; i++) {
    const p = prot[i] * (params.regionInfluence > 0 ? 1 : 0);
    dataMul[i] = fitMask[i] ? Math.max(0, 1 - p * Math.min(1, params.regionInfluence * 1.25)) : 0;
    anchor[i] = p > 0 ? p * protStrength : 0;
    if (p > 0.5) protectedCount++;
  }
  if (protectedCount === n) warnings.push('Every base vertex is protected; nothing will be fitted.');

  // ---------- landmarks ----------
  const lms = (input.landmarks ?? []).filter(isComplete);
  const refTriCount = refTriangles.length / 3;
  const baseTriCount = baseTriangles.length / 3;
  const lmTerms: { tri: number; bary: [number, number, number]; target: [number, number, number]; w: number }[] = [];
  for (const l of lms) {
    const e1 = checkSurfacePoint(l.base, baseTriCount);
    const e2 = checkSurfacePoint(l.ref, refTriCount);
    if (e1 || e2) {
      warnings.push(`Landmark "${l.label}" skipped: ${e1 ?? e2}.`);
      continue;
    }
    if (!(l.weight > 0) || params.landmarkInfluence <= 0) continue;
    const lt = l.base.tri * 3;
    if (!fitMask[baseTriangles[lt]] || !fitMask[baseTriangles[lt + 1]] || !fitMask[baseTriangles[lt + 2]]) {
      warnings.push(`Landmark "${l.label}" is on a component that is not fitted; it is ignored.`);
      continue;
    }
    lmTerms.push({
      tri: l.base.tri,
      bary: l.base.bary,
      target: evalSurfacePoint(refPositions, refTriangles, l.ref),
      w: 0.02 * n * params.landmarkInfluence * l.weight,
    });
  }

  // ---------- reverse-correspondence samples ----------
  const revIdx: number[] = [];
  if (params.bidirectional) {
    const maxRev = Math.max(20000, n);
    const stride = Math.max(1, Math.ceil(nRef / maxRev));
    for (let q = 0; q < nRef; q += stride) if (ref.referenced[q] && ref.areas[q] > 0) revIdx.push(q);
  }
  let revAreaSum = 0;
  for (const q of revIdx) revAreaSum += ref.areas[q];
  const revScale = revIdx.length && revAreaSum > 0 ? (0.5 * n) / revAreaSum : 0;

  // ---------- working state ----------
  const x = baseStart.slice();
  const xPrev = new Float64Array(3 * n);
  const R = new Float64Array(9 * n);
  for (let i = 0; i < n; i++) R[i * 9] = R[i * 9 + 4] = R[i * 9 + 8] = 1;
  const corrP = new Float64Array(3 * n);
  const corrN = new Float64Array(3 * n);
  const corrW = new Float64Array(n);
  const fwdHint = new Int32Array(n).fill(-1);
  const revTri = new Int32Array(revIdx.length);
  const revBary = new Float64Array(revIdx.length * 3);
  const revW = new Float64Array(revIdx.length);
  const revHint = new Int32Array(revIdx.length).fill(-1);
  const S = base.pattern;
  const Svals = new Float64Array(S.values.length);
  const Sbar = { ...S, values: new Float64Array(S.values.length) };
  const B = new Float64Array(6 * n); // xx xy xz yy yz zz
  const rhs = new Float64Array(3 * n);
  const sol = new Float64Array(3 * n);
  const cx = new Float64Array(n), cz = new Float64Array(n), cr = new Float64Array(n);
  const hit = makeHit();
  const Mtmp = new Float64Array(9);
  const Rtmp = new Float64Array(9);
  const iterLogs: IterationLog[] = [];
  const adj = base.adj;
  const wts = base.weights;
  let normals: Float64Array = new Float64Array(3 * n);
  const totalSteps = params.levels * params.iterationsPerLevel;
  // Σ_j w_ij |ē_ij|² per vertex (for the optimal local scale)
  const restNorm = new Float64Array(n);
  for (let i = 0; i < n; i++) {
    let s = 0;
    for (let k = adj.offsets[i]; k < adj.offsets[i + 1]; k++) {
      if (adj.edgeTriCount[k] === 0) continue;
      const j = adj.neighbors[k] * 3;
      const ex = baseRest[i * 3] - baseRest[j], ey = baseRest[i * 3 + 1] - baseRest[j + 1], ez = baseRest[i * 3 + 2] - baseRest[j + 2];
      s += wts[k] * (ex * ex + ey * ey + ez * ez);
    }
    restNorm[i] = s;
  }
  const minScale = 1 / params.maxLocalScale;
  let stepsDone = 0;
  let lambdaN = 0;
  const seamSigma = () => Math.max(100, 20 * lambdaN);

  const distanceBefore = pointToSurfaceDistances(baseStart, ref.bvh, (i) => base.referenced[i] === 1 && fitMask[i] === 1, undefined, Math.max(1, Math.floor(n / 50000)));
  base.bvh.refit(baseStart.slice());
  const coverageBefore = pointToSurfaceDistances(refPositions, base.bvh, (q) => ref.referenced[q] === 1, undefined, Math.max(1, Math.floor(nRef / 50000)));
  const setupMs = now() - t0;

  // ---------- energy (for monitoring) ----------
  const energy = (pos: Float64Array): number => {
    let E = 0;
    for (let i = 0; i < n; i++) {
      const o = i * 3;
      const dx = pos[o] - corrP[o], dy = pos[o + 1] - corrP[o + 1], dz = pos[o + 2] - corrP[o + 2];
      if (corrW[i] > 0) {
        const dn = dx * corrN[o] + dy * corrN[o + 1] + dz * corrN[o + 2];
        E += corrW[i] * ((1 - mu) * (dx * dx + dy * dy + dz * dz) + mu * dn * dn);
      }
      if (anchor[i] > 0) {
        const ax = pos[o] - baseStart[o], ay = pos[o + 1] - baseStart[o + 1], az = pos[o + 2] - baseStart[o + 2];
        E += anchor[i] * (ax * ax + ay * ay + az * az);
      }
      const px = pos[o] - xPrev[o], py = pos[o + 1] - xPrev[o + 1], pz = pos[o + 2] - xPrev[o + 2];
      E += eps * (px * px + py * py + pz * pz);
      const r = i * 9;
      for (let k = adj.offsets[i]; k < adj.offsets[i + 1]; k++) {
        const j = adj.neighbors[k];
        const q = j * 3;
        if (adj.edgeTriCount[k] === 0) {
          if (j > i) {
            const sx = pos[o] - pos[q], sy = pos[o + 1] - pos[q + 1], sz = pos[o + 2] - pos[q + 2];
            E += seamSigma() * (sx * sx + sy * sy + sz * sz);
          }
          continue;
        }
        const ex = baseRest[o] - baseRest[q], ey = baseRest[o + 1] - baseRest[q + 1], ez = baseRest[o + 2] - baseRest[q + 2];
        const rx = pos[o] - pos[q] - (R[r] * ex + R[r + 1] * ey + R[r + 2] * ez);
        const ry = pos[o + 1] - pos[q + 1] - (R[r + 3] * ex + R[r + 4] * ey + R[r + 5] * ez);
        const rz = pos[o + 2] - pos[q + 2] - (R[r + 6] * ex + R[r + 7] * ey + R[r + 8] * ez);
        E += lambdaN * wts[k] * (rx * rx + ry * ry + rz * rz);
      }
    }
    const tri = baseTriangles;
    const term = (t: number, b0: number, b1: number, b2: number, tx: number, ty: number, tz: number, w: number) => {
      const a = tri[t * 3] * 3, b = tri[t * 3 + 1] * 3, c = tri[t * 3 + 2] * 3;
      const px = b0 * pos[a] + b1 * pos[b] + b2 * pos[c] - tx;
      const py = b0 * pos[a + 1] + b1 * pos[b + 1] + b2 * pos[c + 1] - ty;
      const pz = b0 * pos[a + 2] + b1 * pos[b + 2] + b2 * pos[c + 2] - tz;
      return w * (px * px + py * py + pz * pz);
    };
    for (let s = 0; s < revIdx.length; s++) {
      if (revW[s] <= 0) continue;
      const q = revIdx[s] * 3;
      E += term(revTri[s], revBary[s * 3], revBary[s * 3 + 1], revBary[s * 3 + 2], refPositions[q], refPositions[q + 1], refPositions[q + 2], revW[s]);
    }
    for (const l of lmTerms) E += term(l.tri, l.bary[0], l.bary[1], l.bary[2], l.target[0], l.target[1], l.target[2], l.w);
    return E;
  };

  // ---------- operator ----------
  const applyA = (v: Float64Array, out: Float64Array) => {
    const { rowPtr, colIdx } = S;
    for (let i = 0; i < n; i++) {
      let sx = 0, sy = 0, sz = 0;
      for (let k = rowPtr[i]; k < rowPtr[i + 1]; k++) {
        const j = colIdx[k] * 3;
        const a = Svals[k];
        sx += a * v[j];
        sy += a * v[j + 1];
        sz += a * v[j + 2];
      }
      const o = i * 3, b = i * 6;
      const vx = v[o], vy = v[o + 1], vz = v[o + 2];
      out[o] = sx + B[b] * vx + B[b + 1] * vy + B[b + 2] * vz;
      out[o + 1] = sy + B[b + 1] * vx + B[b + 3] * vy + B[b + 4] * vz;
      out[o + 2] = sz + B[b + 2] * vx + B[b + 4] * vy + B[b + 5] * vz;
    }
  };
  const precond = (r: Float64Array, z: Float64Array) => {
    for (let i = 0; i < n; i++) cx[i] = r[i * 3];
    base.amg.apply(cx, cr);
    for (let i = 0; i < n; i++) z[i * 3] = cr[i];
    for (let i = 0; i < n; i++) cx[i] = r[i * 3 + 1];
    base.amg.apply(cx, cr);
    for (let i = 0; i < n; i++) z[i * 3 + 1] = cr[i];
    for (let i = 0; i < n; i++) cz[i] = r[i * 3 + 2];
    base.amg.apply(cz, cr);
    for (let i = 0; i < n; i++) z[i * 3 + 2] = cr[i];
  };

  const addCoupling = (t: number, b0: number, b1: number, b2: number, tx: number, ty: number, tz: number, w: number) => {
    const ids = [baseTriangles[t * 3], baseTriangles[t * 3 + 1], baseTriangles[t * 3 + 2]];
    const bs = [b0, b1, b2];
    for (let p = 0; p < 3; p++) {
      const i = ids[p];
      if (bs[p] === 0) continue;
      rhs[i * 3] += w * bs[p] * tx;
      rhs[i * 3 + 1] += w * bs[p] * ty;
      rhs[i * 3 + 2] += w * bs[p] * tz;
      for (let q = 0; q < 3; q++) {
        if (bs[q] === 0) continue;
        const j = ids[q];
        const k = i === j ? base.diag[i] : findCsr(i, j);
        if (k >= 0) Svals[k] += w * bs[p] * bs[q];
      }
    }
  };
  const findCsr = (i: number, j: number): number => {
    let lo = S.rowPtr[i], hi = S.rowPtr[i + 1] - 1;
    while (lo <= hi) {
      const mid = (lo + hi) >> 1;
      const v = S.colIdx[mid];
      if (v === j) return mid;
      if (v < j) lo = mid + 1;
      else hi = mid - 1;
    }
    return -1;
  };

  // ---------- main loop ----------
  let lastAcceptedMask: Uint8Array = new Uint8Array(n);
  const tFit = now();
  try {
    for (let level = 0; level < schedule.length; level++) {
      const lambda = schedule[level];
      lambdaN = lambda * n;
      for (let it = 0; it < params.iterationsPerLevel; it++) {
        const tIt = now();
        if (hooks.isCancelled?.()) {
          return { status: 'cancelled', message: 'Wrapping cancelled; no changes were applied.', positions: baseStart.slice(), diagnostics: null };
        }
        xPrev.set(x);
        normals = vertexNormals(x, baseTriangles, normals);

        let tS = now();
        const stages = { correspondences: 0, reverse: 0, rotations: 0, assembly: 0, multigrid: 0, solve: 0, energy: 0 };
        const lap = (k: keyof typeof stages) => {
          const t = now();
          stages[k] += t - tS;
          tS = t;
        };
        // 1. forward correspondences
        let accepted = 0, fitSq = 0, eligible = 0;
        const acceptedMask = new Uint8Array(n);
        for (let i = 0; i < n; i++) {
          corrW[i] = 0;
          if (!base.referenced[i] || dataMul[i] <= 0 || params.fitStrength <= 0) continue;
          eligible++;
          const o = i * 3;
          if (!ref.bvh.closestPoint(x[o], x[o + 1], x[o + 2], maxDistSq, hit, fwdHint[i])) continue;
          fwdHint[i] = hit.tri;
          if (params.rejectBoundary && onBoundary(hit.region, hit.tri, ref.triangles, ref.boundary, ref.adj)) continue;
          const ta = ref.triangles[hit.tri * 3] * 3, tb = ref.triangles[hit.tri * 3 + 1] * 3, tc = ref.triangles[hit.tri * 3 + 2] * 3;
          let nx = hit.u * ref.normals[ta] + hit.v * ref.normals[tb] + hit.w * ref.normals[tc];
          let ny = hit.u * ref.normals[ta + 1] + hit.v * ref.normals[tb + 1] + hit.w * ref.normals[tc + 1];
          let nz = hit.u * ref.normals[ta + 2] + hit.v * ref.normals[tb + 2] + hit.w * ref.normals[tc + 2];
          const nl = Math.hypot(nx, ny, nz);
          if (nl > 0) { nx /= nl; ny /= nl; nz /= nl; }
          let dot = nx * normals[o] + ny * normals[o + 1] + nz * normals[o + 2];
          if (params.twoSidedNormals) dot = Math.abs(dot);
          if (nl === 0) dot = 1;
          if (dot < cosThr) continue;
          const d = Math.sqrt(hit.distSq) / maxDist;
          const tukey = (1 - d * d) * (1 - d * d);
          const c = tukey * Math.max(0.05, dot);
          corrW[i] = base.areaWeights[i] * c * params.fitStrength * dataMul[i];
          if (!(corrW[i] > 0)) continue;
          corrP[o] = hit.x; corrP[o + 1] = hit.y; corrP[o + 2] = hit.z;
          corrN[o] = nx; corrN[o + 1] = ny; corrN[o + 2] = nz;
          accepted++;
          acceptedMask[i] = 1;
          fitSq += hit.distSq;
        }
        lastAcceptedMask = acceptedMask;

        lap('correspondences');
        // 2. reverse correspondences (reference -> current base surface)
        let revAccepted = 0;
        if (revIdx.length && params.fitStrength > 0) {
          base.bvh.refit(x);
          for (let s = 0; s < revIdx.length; s++) {
            revW[s] = 0;
            const q = revIdx[s] * 3;
            if (!base.bvh.closestPoint(refPositions[q], refPositions[q + 1], refPositions[q + 2], maxDistSq, hit, revHint[s])) continue;
            revHint[s] = hit.tri;
            if (onBaseBoundary(hit.region, hit.tri, baseTriangles, base)) continue;
            const ta = baseTriangles[hit.tri * 3], tb = baseTriangles[hit.tri * 3 + 1], tc = baseTriangles[hit.tri * 3 + 2];
            if (!fitMask[ta] || !fitMask[tb] || !fitMask[tc]) continue;
            let nx = hit.u * normals[ta * 3] + hit.v * normals[tb * 3] + hit.w * normals[tc * 3];
            let ny = hit.u * normals[ta * 3 + 1] + hit.v * normals[tb * 3 + 1] + hit.w * normals[tc * 3 + 1];
            let nz = hit.u * normals[ta * 3 + 2] + hit.v * normals[tb * 3 + 2] + hit.w * normals[tc * 3 + 2];
            const nl = Math.hypot(nx, ny, nz);
            if (nl > 0) { nx /= nl; ny /= nl; nz /= nl; }
            let dot = nx * ref.normals[q] + ny * ref.normals[q + 1] + nz * ref.normals[q + 2];
            if (params.twoSidedNormals) dot = Math.abs(dot);
            if (dot < cosThr) continue;
            const mul = hit.u * dataMul[ta] + hit.v * dataMul[tb] + hit.w * dataMul[tc];
            if (mul <= 0) continue;
            const d = Math.sqrt(hit.distSq) / maxDist;
            const tukey = (1 - d * d) * (1 - d * d);
            revW[s] = revScale * ref.areas[revIdx[s]] * tukey * Math.max(0.05, dot) * params.fitStrength * mul;
            revTri[s] = hit.tri;
            revBary[s * 3] = hit.u; revBary[s * 3 + 1] = hit.v; revBary[s * 3 + 2] = hit.w;
            if (revW[s] > 0) revAccepted++;
          }
        }

        if (eligible > 0 && accepted < 0.1 * eligible && lmTerms.length === 0 && level === 0 && it === 0) {
          warnings.push(
            `Only ${accepted} of ${eligible} base vertices found a reference surface within the maximum correspondence distance. ` +
              'Check the alignment or increase Maximum Correspondence Distance.',
          );
        }

        lap('reverse');
        // 3. local step: best-fit rotations
        for (let i = 0; i < n; i++) {
          const o = i * 3;
          Mtmp.fill(0);
          let any = false;
          for (let k = adj.offsets[i]; k < adj.offsets[i + 1]; k++) {
            if (adj.edgeTriCount[k] === 0) continue;
            const j = adj.neighbors[k] * 3;
            const w = wts[k];
            const ex = x[o] - x[j], ey = x[o + 1] - x[j + 1], ez = x[o + 2] - x[j + 2];
            const fx = baseRest[o] - baseRest[j], fy = baseRest[o + 1] - baseRest[j + 1], fz = baseRest[o + 2] - baseRest[j + 2];
            Mtmp[0] += w * ex * fx; Mtmp[1] += w * ex * fy; Mtmp[2] += w * ex * fz;
            Mtmp[3] += w * ey * fx; Mtmp[4] += w * ey * fy; Mtmp[5] += w * ey * fz;
            Mtmp[6] += w * ez * fx; Mtmp[7] += w * ez * fy; Mtmp[8] += w * ez * fz;
            any = true;
          }
          if (any) {
            const traceRM = closestRotation(Mtmp, Rtmp);
            if (params.allowLocalScaling && restNorm[i] > 0) {
              let sc = traceRM / restNorm[i];
              sc = sc < minScale ? minScale : sc > params.maxLocalScale ? params.maxLocalScale : sc;
              for (let k = 0; k < 9; k++) Rtmp[k] *= sc;
            }
            R.set(Rtmp, i * 9);
          }
        }

        lap('rotations');
        // 4. assemble global system
        Svals.fill(0);
        B.fill(0);
        rhs.fill(0);
        const sigma = seamSigma();
        for (let i = 0; i < n; i++) {
          const o = i * 3, r = i * 9;
          const di = base.diag[i];
          for (let k = adj.offsets[i]; k < adj.offsets[i + 1]; k++) {
            const j = adj.neighbors[k];
            if (adj.edgeTriCount[k] === 0) {
              // seam lock
              Svals[base.adjToCsr[k]] -= sigma;
              Svals[di] += sigma;
              continue;
            }
            const w = wts[k];
            const c = 2 * lambdaN * w;
            Svals[base.adjToCsr[k]] -= c;
            Svals[di] += c;
            const q = j * 3, s = j * 9;
            const ex = baseRest[o] - baseRest[q], ey = baseRest[o + 1] - baseRest[q + 1], ez = baseRest[o + 2] - baseRest[q + 2];
            const f = lambdaN * w;
            rhs[o] += f * ((R[r] + R[s]) * ex + (R[r + 1] + R[s + 1]) * ey + (R[r + 2] + R[s + 2]) * ez);
            rhs[o + 1] += f * ((R[r + 3] + R[s + 3]) * ex + (R[r + 4] + R[s + 4]) * ey + (R[r + 5] + R[s + 5]) * ez);
            rhs[o + 2] += f * ((R[r + 6] + R[s + 6]) * ex + (R[r + 7] + R[s + 7]) * ey + (R[r + 8] + R[s + 8]) * ez);
          }
          // data block
          const b = i * 6;
          const cw = corrW[i];
          if (cw > 0) {
            const nx = corrN[o], ny = corrN[o + 1], nz = corrN[o + 2];
            const iso = cw * (1 - mu), an = cw * mu;
            B[b] += iso + an * nx * nx; B[b + 1] += an * nx * ny; B[b + 2] += an * nx * nz;
            B[b + 3] += iso + an * ny * ny; B[b + 4] += an * ny * nz; B[b + 5] += iso + an * nz * nz;
            const px = corrP[o], py = corrP[o + 1], pz = corrP[o + 2];
            const pn = nx * px + ny * py + nz * pz;
            rhs[o] += iso * px + an * nx * pn;
            rhs[o + 1] += iso * py + an * ny * pn;
            rhs[o + 2] += iso * pz + an * nz * pn;
          }
          const iso2 = anchor[i] + eps;
          B[b] += iso2; B[b + 3] += iso2; B[b + 5] += iso2;
          rhs[o] += anchor[i] * baseStart[o] + eps * x[o];
          rhs[o + 1] += anchor[i] * baseStart[o + 1] + eps * x[o + 1];
          rhs[o + 2] += anchor[i] * baseStart[o + 2] + eps * x[o + 2];
        }
        for (let s = 0; s < revIdx.length; s++) {
          if (revW[s] <= 0) continue;
          const q = revIdx[s] * 3;
          addCoupling(revTri[s], revBary[s * 3], revBary[s * 3 + 1], revBary[s * 3 + 2], refPositions[q], refPositions[q + 1], refPositions[q + 2], revW[s]);
        }
        for (const l of lmTerms) addCoupling(l.tri, l.bary[0], l.bary[1], l.bary[2], l.target[0], l.target[1], l.target[2], l.w);

        // scalar approximation for the multigrid preconditioner
        Sbar.values.set(Svals);
        for (let i = 0; i < n; i++) {
          const b = i * 6;
          Sbar.values[base.diag[i]] += (B[b] + B[b + 3] + B[b + 5]) / 3;
        }
        lap('assembly');
        base.amg.update(Sbar);
        lap('multigrid');

        // 5. solve
        const eBefore = energy(x);
        lap('energy');
        sol.set(x);
        const res = pcg(applyA, precond, rhs, sol, params.solverTolerance, params.maxSolverIterations);
        for (let k = 0; k < sol.length; k++) {
          if (!Number.isFinite(sol[k])) throw new WrapFailure('The linear solver produced non-finite values (numerical instability). No changes were applied.');
        }
        lap('solve');
        const eAfter = energy(sol);
        lap('energy');
        let maxDisp = 0;
        for (let i = 0; i < n; i++) {
          const o = i * 3;
          const d = Math.hypot(sol[o] - x[o], sol[o + 1] - x[o + 1], sol[o + 2] - x[o + 2]);
          if (d > maxDisp) maxDisp = d;
        }
        if (maxDisp > 2 * refDiag) {
          throw new WrapFailure(
            `Unstable step: vertices moved ${maxDisp.toPrecision(3)} units in one iteration (reference size ${refDiag.toPrecision(3)}). No changes were applied.`,
          );
        }
        if (!res.converged && res.relativeResidual > 1e-3) {
          warnings.push(
            `Level ${level + 1}, iteration ${it + 1}: linear solver stopped at relative residual ${res.relativeResidual.toExponential(2)} after ${res.iterations} iterations.`,
          );
        }
        if (eAfter > eBefore * (1 + 1e-4) + 1e-12) {
          warnings.push(`Level ${level + 1}, iteration ${it + 1}: energy increased during the solve (${eBefore.toPrecision(4)} → ${eAfter.toPrecision(4)}).`);
        }
        x.set(sol);
        stepsDone++;
        const rmsFit = accepted ? Math.sqrt(fitSq / accepted) : 0;
        iterLogs.push({
          level,
          iteration: it,
          lambda,
          accepted,
          acceptedFraction: eligible ? accepted / eligible : 0,
          reverseAccepted: revAccepted,
          rmsFit,
          cgIterations: res.iterations,
          cgResidual: res.relativeResidual,
          maxDisplacement: maxDisp,
          energyBefore: eBefore,
          energyAfter: eAfter,
          ms: now() - tIt,
          stages,
        });
        report({
          stage: 'fitting',
          level,
          iteration: it,
          fraction: stepsDone / totalSteps,
          message: `Level ${level + 1}/${params.levels} · iteration ${it + 1}`,
          rmsFit,
        });
        if (hooks.yieldControl) await hooks.yieldControl();
        if (maxDisp < 1e-5 * refDiag) {
          stepsDone += params.iterationsPerLevel - it - 1;
          break; // converged at this stiffness
        }
      }
    }
  } catch (e) {
    if (e instanceof WrapFailure) return fail(e.message);
    throw e;
  }
  const fitMs = now() - tFit;

  // ---------- analysis ----------
  report({ stage: 'analysis', level: params.levels - 1, iteration: params.iterationsPerLevel - 1, fraction: 1, message: 'Measuring result' });
  const tA = now();
  const stride = Math.max(1, Math.floor(n / 50000));
  const componentReports = modes ? applyComponentModes(baseRest, x, base.components, modes) : [];
  const distanceAfter = pointToSurfaceDistances(x, ref.bvh, (i) => base.referenced[i] === 1 && fitMask[i] === 1, undefined, stride);
  const inlierDistanceAfter = pointToSurfaceDistances(x, ref.bvh, (i) => lastAcceptedMask[i] === 1, undefined, stride);
  base.bvh.refit(x);
  const coverageAfter = pointToSurfaceDistances(refPositions, base.bvh, (q) => ref.referenced[q] === 1, undefined, Math.max(1, Math.floor(nRef / 50000)));
  const quality = qualityReport(baseRest, x, baseTriangles, base.triAdj, R);
  if (quality.flippedTriangles > 0) {
    warnings.push(`${quality.flippedTriangles} triangle(s) flipped orientation. Increase smoothness, add landmarks or protect the affected region.`);
  }
  if (quality.collapsedTriangles > 0) warnings.push(`${quality.collapsedTriangles} triangle(s) collapsed below 5% of their original area.`);
  if (quality.stretchedEdges > 0) warnings.push(`${quality.stretchedEdges} edge(s) changed length by more than 3×.`);
  if (distanceAfter.mean > distanceBefore.mean * 1.05 && distanceBefore.mean > 1e-9 * refDiag) {
    warnings.push('Average distance to the reference increased. The meshes may be poorly aligned or the parameters too stiff/too restrictive.');
  }
  const analysisMs = now() - tA;
  // dedupe repeated warnings
  const uniq = Array.from(new Set(warnings));
  return {
    status: 'completed',
    message: uniq.length ? `Completed with ${uniq.length} warning(s).` : 'Completed.',
    positions: x,
    diagnostics: {
      params,
      schedule,
      iterations: iterLogs,
      warnings: uniq,
      seamPairs: base.seamPairs.length / 2,
      landmarksUsed: lmTerms.length,
      components: componentReports,
      amgLevels: base.amg.levelSizes,
      distanceBefore,
      distanceAfter,
      coverageBefore,
      coverageAfter,
      inlierDistanceAfter,
      quality,
      timings: { setupMs, fitMs, analysisMs, totalMs: now() - t0 },
      vertexCount: n,
      triangleCount: baseTriangles.length / 3,
    },
  };
}

function onBoundary(region: TriRegion, tri: number, triangles: Uint32Array, boundary: Uint8Array, adj: import('../geometry/topology').Adjacency): boolean {
  if (region === TriRegion.Face) return false;
  const a = triangles[tri * 3], b = triangles[tri * 3 + 1], c = triangles[tri * 3 + 2];
  switch (region) {
    case TriRegion.VertA: return boundary[a] === 1;
    case TriRegion.VertB: return boundary[b] === 1;
    case TriRegion.VertC: return boundary[c] === 1;
    case TriRegion.EdgeAB: return boundary[a] === 1 && boundary[b] === 1 && isBoundaryEdge(adj, a, b);
    case TriRegion.EdgeBC: return boundary[b] === 1 && boundary[c] === 1 && isBoundaryEdge(adj, b, c);
    case TriRegion.EdgeCA: return boundary[c] === 1 && boundary[a] === 1 && isBoundaryEdge(adj, c, a);
  }
  return false;
}

function onBaseBoundary(region: TriRegion, tri: number, triangles: Uint32Array, base: BasePrep): boolean {
  return onBoundary(region, tri, triangles, base.boundary, base.triAdj);
}
