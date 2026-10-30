/**
 * Rigid / similarity alignment. All functions return a column-major 4x4
 * transform that maps base-mesh coordinates into reference space; nothing here
 * changes mesh data.
 */

import { closestRotation, mat4FromSimilarity, mat4Identity, mat4Multiply, Mat4, transformPositions } from '../core/mat3';
import { computeBBox } from '../core/mesh';
import { TriangleBVH, makeHit } from '../spatial/bvh';

export interface SimilarityFit {
  transform: Mat4;
  scale: number;
  /** weighted RMS of residuals after fitting */
  rms: number;
}

/**
 * Weighted least-squares similarity (Umeyama 1991) mapping `src` onto `dst`.
 * `allowScale = false` gives a rigid transform.
 */
export function umeyama(src: ArrayLike<number>, dst: ArrayLike<number>, weights: ArrayLike<number> | null, allowScale: boolean): SimilarityFit {
  const m = src.length / 3;
  if (m < 3) throw new Error('At least 3 point pairs are required for alignment.');
  let W = 0;
  const ms = [0, 0, 0], md = [0, 0, 0];
  for (let i = 0; i < m; i++) {
    const w = weights ? weights[i] : 1;
    W += w;
    for (let k = 0; k < 3; k++) {
      ms[k] += w * src[i * 3 + k];
      md[k] += w * dst[i * 3 + k];
    }
  }
  if (!(W > 0)) throw new Error('Alignment weights sum to zero.');
  for (let k = 0; k < 3; k++) {
    ms[k] /= W;
    md[k] /= W;
  }
  const C = new Float64Array(9);
  let varS = 0;
  for (let i = 0; i < m; i++) {
    const w = (weights ? weights[i] : 1) / W;
    const sx = src[i * 3] - ms[0], sy = src[i * 3 + 1] - ms[1], sz = src[i * 3 + 2] - ms[2];
    const dx = dst[i * 3] - md[0], dy = dst[i * 3 + 1] - md[1], dz = dst[i * 3 + 2] - md[2];
    varS += w * (sx * sx + sy * sy + sz * sz);
    // C = Σ w d s^T
    C[0] += w * dx * sx; C[1] += w * dx * sy; C[2] += w * dx * sz;
    C[3] += w * dy * sx; C[4] += w * dy * sy; C[5] += w * dy * sz;
    C[6] += w * dz * sx; C[7] += w * dz * sy; C[8] += w * dz * sz;
  }
  if (!(varS > 0)) throw new Error('Alignment points are all coincident.');
  // rank check: points must not be collinear
  const cov = new Float64Array(9);
  for (let i = 0; i < m; i++) {
    const sx = src[i * 3] - ms[0], sy = src[i * 3 + 1] - ms[1], sz = src[i * 3 + 2] - ms[2];
    cov[0] += sx * sx; cov[1] += sx * sy; cov[2] += sx * sz;
    cov[4] += sy * sy; cov[5] += sy * sz; cov[8] += sz * sz;
  }
  cov[3] = cov[1]; cov[6] = cov[2]; cov[7] = cov[5];
  {
    // second singular value relative to the first
    const tr = cov[0] + cov[4] + cov[8];
    const minor = cov[0] * cov[4] - cov[1] * cov[3] + cov[0] * cov[8] - cov[2] * cov[6] + cov[4] * cov[8] - cov[5] * cov[7];
    if (minor <= 1e-12 * tr * tr) throw new Error('Alignment points are collinear; add points that span a plane.');
  }
  const R = new Float64Array(9);
  const traceDS = closestRotation(C, R);
  const scale = allowScale ? traceDS / varS : 1;
  const t = [0, 0, 0];
  for (let k = 0; k < 3; k++) {
    t[k] = md[k] - scale * (R[k * 3] * ms[0] + R[k * 3 + 1] * ms[1] + R[k * 3 + 2] * ms[2]);
  }
  const transform = mat4FromSimilarity(R, scale, t);
  // residual
  const moved = transformPositions(Float64Array.from(src), transform);
  let e = 0;
  for (let i = 0; i < m; i++) {
    const w = (weights ? weights[i] : 1) / W;
    const dx = moved[i * 3] - dst[i * 3], dy = moved[i * 3 + 1] - dst[i * 3 + 1], dz = moved[i * 3 + 2] - dst[i * 3 + 2];
    e += w * (dx * dx + dy * dy + dz * dz);
  }
  return { transform, scale, rms: Math.sqrt(e) };
}

/**
 * Initial alignment from bounding boxes: match centres and (optionally) scale
 * uniformly so the bounding-box diagonals agree. No rotation is guessed.
 */
export function boundingBoxAlignment(basePositions: Float64Array, refPositions: Float64Array, allowScale: boolean): Mat4 {
  const a = computeBBox(basePositions);
  const b = computeBBox(refPositions);
  const s = allowScale && a.diagonal > 0 ? b.diagonal / a.diagonal : 1;
  const m = mat4Identity();
  m[0] = m[5] = m[10] = s;
  m[12] = b.center[0] - s * a.center[0];
  m[13] = b.center[1] - s * a.center[1];
  m[14] = b.center[2] - s * a.center[2];
  return m;
}

export interface ICPOptions {
  maxIterations?: number;
  allowScale?: boolean;
  /** maximum number of base vertices sampled per iteration */
  sampleCount?: number;
  /** keep this fraction of the closest pairs each iteration (trimmed ICP) */
  trimFraction?: number;
  /** stop when the transform update moves points less than this fraction of the bbox diagonal */
  tolerance?: number;
}

export interface ICPResult {
  /** total transform: input transform composed with the ICP update */
  transform: Mat4;
  iterations: number;
  rmsBefore: number;
  rmsAfter: number;
  converged: boolean;
}

/**
 * Trimmed point-to-surface ICP: base vertices (already placed by
 * `initial`) are matched to closest points on the reference surface. The first
 * two updates are closed-form point-to-point (Umeyama, robust from far away);
 * later updates are linearised point-to-plane Gauss–Newton steps with a small
 * point-to-point term, which converge much faster once the shapes overlap.
 */
export function icpAlign(
  basePositions: Float64Array,
  initial: ArrayLike<number>,
  refBVH: TriangleBVH,
  opts: ICPOptions = {},
): ICPResult {
  const maxIt = opts.maxIterations ?? 50;
  const trim = opts.trimFraction ?? 0.8;
  const n = basePositions.length / 3;
  const sampleCount = Math.min(n, opts.sampleCount ?? 4000);
  const stride = n / sampleCount;
  const idx = new Uint32Array(sampleCount);
  for (let k = 0; k < sampleCount; k++) idx[k] = Math.min(n - 1, Math.floor(k * stride));
  const src = new Float64Array(sampleCount * 3);
  for (let k = 0; k < sampleCount; k++) {
    src[k * 3] = basePositions[idx[k] * 3];
    src[k * 3 + 1] = basePositions[idx[k] * 3 + 1];
    src[k * 3 + 2] = basePositions[idx[k] * 3 + 2];
  }
  let T: Mat4 = Float64Array.from(initial);
  const diag = computeBBox(refBVH.positions).diagonal || 1;
  const tol = (opts.tolerance ?? 1e-6) * diag;
  const hit = makeHit();
  const moved = new Float64Array(src.length);
  const dst = new Float64Array(src.length);
  const nrm = new Float64Array(src.length);
  const dist = new Float64Array(sampleCount);
  const order = new Uint32Array(sampleCount);
  const rmsOf = (): number => {
    transformPositions(src, T, moved);
    let s = 0;
    for (let k = 0; k < sampleCount; k++) {
      refBVH.closestPoint(moved[k * 3], moved[k * 3 + 1], moved[k * 3 + 2], Infinity, hit);
      s += hit.distSq;
    }
    return Math.sqrt(s / sampleCount);
  };
  const rmsBefore = rmsOf();
  let converged = false;
  let it = 0;
  // ICP is not guaranteed to decrease the untrimmed RMS (trimming, differing shapes); keep the best transform seen
  let best: { T: Mat4; rms: number } = { T: Float64Array.from(T), rms: rmsBefore };
  for (; it < maxIt; it++) {
    transformPositions(src, T, moved);
    let sumSq = 0;
    for (let k = 0; k < sampleCount; k++) {
      refBVH.closestPoint(moved[k * 3], moved[k * 3 + 1], moved[k * 3 + 2], Infinity, hit);
      dst[k * 3] = hit.x;
      dst[k * 3 + 1] = hit.y;
      dst[k * 3 + 2] = hit.z;
      dist[k] = hit.distSq;
      sumSq += hit.distSq;
      order[k] = k;
      faceNormal(refBVH, hit.tri, nrm, k * 3);
    }
    const rmsNow = Math.sqrt(sumSq / sampleCount);
    if (rmsNow < best.rms) best = { T: Float64Array.from(T), rms: rmsNow };
    // trimmed: keep the closest `trim` fraction
    const sorted = Array.from(order).sort((a, b) => dist[a] - dist[b]);
    const keep = Math.max(3, Math.floor(sampleCount * trim));
    const s2 = new Float64Array(keep * 3), d2 = new Float64Array(keep * 3), n2 = new Float64Array(keep * 3);
    for (let j = 0; j < keep; j++) {
      const k = sorted[j];
      s2.set(moved.subarray(k * 3, k * 3 + 3), j * 3);
      d2.set(dst.subarray(k * 3, k * 3 + 3), j * 3);
      n2.set(nrm.subarray(k * 3, k * 3 + 3), j * 3);
    }
    let fit: { transform: Mat4 };
    try {
      fit = it < 2 ? umeyama(s2, d2, null, !!opts.allowScale) : { transform: pointToPlaneStep(s2, d2, n2, !!opts.allowScale) };
    } catch {
      break;
    }
    T = mat4Multiply(fit.transform, T);
    // measure update size on the kept points
    const upd = transformPositions(s2, fit.transform);
    let maxMove = 0;
    for (let j = 0; j < keep; j++) {
      const dx = upd[j * 3] - s2[j * 3], dy = upd[j * 3 + 1] - s2[j * 3 + 1], dz = upd[j * 3 + 2] - s2[j * 3 + 2];
      maxMove = Math.max(maxMove, Math.hypot(dx, dy, dz));
    }
    if (maxMove < tol) {
      converged = true;
      it++;
      break;
    }
  }
  const rmsFinal = rmsOf();
  if (rmsFinal > best.rms) return { transform: best.T, iterations: it, rmsBefore, rmsAfter: best.rms, converged };
  return { transform: T, iterations: it, rmsBefore, rmsAfter: rmsFinal, converged };
}

function faceNormal(bvh: TriangleBVH, tri: number, out: Float64Array, o: number) {
  const P = bvh.positions, T = bvh.triangles;
  const a = T[tri * 3] * 3, b = T[tri * 3 + 1] * 3, c = T[tri * 3 + 2] * 3;
  const ux = P[b] - P[a], uy = P[b + 1] - P[a + 1], uz = P[b + 2] - P[a + 2];
  const vx = P[c] - P[a], vy = P[c + 1] - P[a + 1], vz = P[c + 2] - P[a + 2];
  const nx = uy * vz - uz * vy, ny = uz * vx - ux * vz, nz = ux * vy - uy * vx;
  const l = Math.hypot(nx, ny, nz) || 1;
  out[o] = nx / l;
  out[o + 1] = ny / l;
  out[o + 2] = nz / l;
}

/**
 * One Gauss–Newton step for x' = c + (1+s) R (x - c) + t with R ≈ I + [ω]×,
 * minimising Σ (n·(x'-q))² + β Σ |x'-q|². Returns the (re-orthonormalised)
 * update transform. Scale is fixed at 1 unless `allowScale`.
 */
function pointToPlaneStep(src: Float64Array, dst: Float64Array, nrm: Float64Array, allowScale: boolean): Mat4 {
  const m = src.length / 3;
  const c = [0, 0, 0];
  for (let i = 0; i < m; i++) for (let k = 0; k < 3; k++) c[k] += src[i * 3 + k] / m;
  let ext = 0;
  for (let i = 0; i < m; i++) ext = Math.max(ext, Math.hypot(src[i * 3] - c[0], src[i * 3 + 1] - c[1], src[i * 3 + 2] - c[2]));
  const L = ext || 1; // normalise rotation/scale columns for conditioning
  const P = allowScale ? 7 : 6;
  const H = new Float64Array(P * P);
  const g = new Float64Array(P);
  const J = new Float64Array(P);
  const beta = 0.05;
  const add = (w: number, r: number) => {
    for (let a = 0; a < P; a++) {
      g[a] += w * J[a] * r;
      for (let b = 0; b < P; b++) H[a * P + b] += w * J[a] * J[b];
    }
  };
  for (let i = 0; i < m; i++) {
    const ax = (src[i * 3] - c[0]) / L, ay = (src[i * 3 + 1] - c[1]) / L, az = (src[i * 3 + 2] - c[2]) / L;
    const rx = src[i * 3] - dst[i * 3], ry = src[i * 3 + 1] - dst[i * 3 + 1], rz = src[i * 3 + 2] - dst[i * 3 + 2];
    const nx = nrm[i * 3], ny = nrm[i * 3 + 1], nz = nrm[i * 3 + 2];
    // point-to-plane row: d/dω = L (a × n), d/dt = n, d/ds = L (n·a)
    J[0] = L * (ay * nz - az * ny); J[1] = L * (az * nx - ax * nz); J[2] = L * (ax * ny - ay * nx);
    J[3] = nx; J[4] = ny; J[5] = nz;
    if (allowScale) J[6] = L * (nx * ax + ny * ay + nz * az);
    add(1, nx * rx + ny * ry + nz * rz);
    // point-to-point rows (ω × a = -[a]× ω)
    J[0] = 0; J[1] = L * az; J[2] = -L * ay; J[3] = 1; J[4] = 0; J[5] = 0; if (allowScale) J[6] = L * ax;
    add(beta, rx);
    J[0] = -L * az; J[1] = 0; J[2] = L * ax; J[3] = 0; J[4] = 1; J[5] = 0; if (allowScale) J[6] = L * ay;
    add(beta, ry);
    J[0] = L * ay; J[1] = -L * ax; J[2] = 0; J[3] = 0; J[4] = 0; J[5] = 1; if (allowScale) J[6] = L * az;
    add(beta, rz);
  }
  let tr = 0;
  for (let a = 0; a < P; a++) tr += H[a * P + a];
  for (let a = 0; a < P; a++) H[a * P + a] += 1e-9 * tr + 1e-300;
  // solve H d = -g (Cholesky)
  const Lm = H.slice();
  for (let j = 0; j < P; j++) {
    let d = Lm[j * P + j];
    for (let k = 0; k < j; k++) d -= Lm[j * P + k] ** 2;
    if (!(d > 0)) throw new Error('ICP step is singular');
    const ljj = Math.sqrt(d);
    Lm[j * P + j] = ljj;
    for (let i = j + 1; i < P; i++) {
      let s = Lm[i * P + j];
      for (let k = 0; k < j; k++) s -= Lm[i * P + k] * Lm[j * P + k];
      Lm[i * P + j] = s / ljj;
    }
  }
  const d = Array.from(g, (v) => -v);
  for (let i = 0; i < P; i++) {
    for (let k = 0; k < i; k++) d[i] -= Lm[i * P + k] * d[k];
    d[i] /= Lm[i * P + i];
  }
  for (let i = P - 1; i >= 0; i--) {
    for (let k = i + 1; k < P; k++) d[i] -= Lm[k * P + i] * d[k];
    d[i] /= Lm[i * P + i];
  }
  const w = [d[0], d[1], d[2]];
  const angle = Math.hypot(w[0], w[1], w[2]);
  const R = new Float64Array([1, 0, 0, 0, 1, 0, 0, 0, 1]);
  if (angle > 0) {
    const [x, y, z] = w.map((v) => v / angle);
    const co = Math.cos(angle), si = Math.sin(angle), t = 1 - co;
    R.set([t * x * x + co, t * x * y - si * z, t * x * z + si * y, t * x * y + si * z, t * y * y + co, t * y * z - si * x, t * x * z - si * y, t * y * z + si * x, t * z * z + co]);
  }
  const sc = allowScale ? Math.max(0.5, Math.min(2, 1 + d[6])) : 1;
  // x' = sc R (x - c) + c + t
  const tvec = [0, 1, 2].map((k) => c[k] + d[3 + k] - sc * (R[k * 3] * c[0] + R[k * 3 + 1] * c[1] + R[k * 3 + 2] * c[2]));
  return mat4FromSimilarity(R, sc, tvec);
}
