/**
 * Mesh validation. Reports problems; never modifies the mesh.
 */

import { BBox, computeBBox, PolyMesh, triangulate } from '../core/mesh';
import { buildAdjacency, coincidentPairs, connectedComponents, referencedVertices, triangleNormalsAreas } from './topology';

export type Severity = 'error' | 'warning' | 'info';

export interface ValidationIssue {
  severity: Severity;
  code: string;
  message: string;
  count?: number;
  /** a few offending element indices for inspection */
  samples?: number[];
}

export interface MeshStats {
  vertices: number;
  faces: number;
  triangles: number;
  /** polygon size histogram: { 3: n, 4: n, '5+': n } */
  polygonSizes: Record<string, number>;
  edges: number;
  boundaryEdges: number;
  components: number;
  surfaceArea: number;
  bbox: BBox;
  /** signed volume (meaningful only for closed meshes) */
  volume: number;
  closed: boolean;
}

export interface ValidationReport {
  stats: MeshStats;
  issues: ValidationIssue[];
  /** true when there are no error-severity issues */
  ok: boolean;
}

const SAMPLE = 8;

export function validateMesh(mesh: PolyMesh, role: 'base' | 'reference'): ValidationReport {
  const issues: ValidationIssue[] = [];
  const { positions, faceOffsets, faceIndices } = mesh;
  const n = positions.length / 3;
  const F = faceOffsets.length - 1;

  // --- coordinates ---
  const badCoords: number[] = [];
  for (let i = 0; i < n; i++) {
    if (!Number.isFinite(positions[i * 3]) || !Number.isFinite(positions[i * 3 + 1]) || !Number.isFinite(positions[i * 3 + 2])) badCoords.push(i);
  }
  if (badCoords.length) {
    issues.push({ severity: 'error', code: 'nan-coordinates', message: `${badCoords.length} vertices have NaN or infinite coordinates.`, count: badCoords.length, samples: badCoords.slice(0, SAMPLE) });
  }
  // --- indices / polygon sizes ---
  const sizes: Record<string, number> = {};
  const outOfRange: number[] = [];
  const tooSmall: number[] = [];
  const repeated: number[] = [];
  for (let f = 0; f < F; f++) {
    const s = faceOffsets[f], e = faceOffsets[f + 1];
    const k = e - s;
    const key = k >= 5 ? '5+' : String(k);
    sizes[key] = (sizes[key] ?? 0) + 1;
    if (k < 3) tooSmall.push(f);
    let rep = false;
    for (let a = s; a < e; a++) {
      if (faceIndices[a] >= n) outOfRange.push(f);
      for (let b = a + 1; b < e; b++) if (faceIndices[a] === faceIndices[b]) rep = true;
    }
    if (rep) repeated.push(f);
  }
  if (outOfRange.length) {
    issues.push({ severity: 'error', code: 'index-out-of-range', message: `${outOfRange.length} faces reference vertices that do not exist.`, count: outOfRange.length, samples: outOfRange.slice(0, SAMPLE) });
  }
  if (tooSmall.length) {
    issues.push({ severity: 'error', code: 'face-too-small', message: `${tooSmall.length} faces have fewer than 3 corners.`, count: tooSmall.length, samples: tooSmall.slice(0, SAMPLE) });
  }
  const bbox = computeBBox(positions);
  if (badCoords.length || outOfRange.length) {
    return { stats: emptyStats(n, F, sizes, bbox), issues, ok: false };
  }
  if (F === 0) {
    issues.push({ severity: 'error', code: 'no-faces', message: 'Mesh has no faces.' });
    return { stats: emptyStats(n, F, sizes, bbox), issues, ok: false };
  }

  const { triangles, triFace } = triangulate(mesh);
  const { areas, normals } = triangleNormalsAreas(positions, triangles);
  const diag = bbox.diagonal;
  const areaTol = Math.max(1e-30, diag * diag * 1e-12);

  // --- degenerate faces ---
  const degenerate = new Set<number>(repeated);
  const faceArea = new Float64Array(F);
  for (let t = 0; t < areas.length; t++) faceArea[triFace[t]] += areas[t];
  for (let f = 0; f < F; f++) if (faceArea[f] <= areaTol && faceOffsets[f + 1] - faceOffsets[f] >= 3) degenerate.add(f);
  if (degenerate.size) {
    const list = Array.from(degenerate);
    issues.push({
      severity: 'warning',
      code: 'degenerate-faces',
      message: `${list.length} degenerate faces (zero area or repeated vertices). They are kept, but contribute nothing to fitting.`,
      count: list.length,
      samples: list.slice(0, SAMPLE),
    });
  }

  // --- unreferenced vertices ---
  const ref = referencedVertices(triangles, n);
  const unref: number[] = [];
  for (let i = 0; i < n; i++) if (!ref[i]) unref.push(i);
  if (unref.length) {
    issues.push({
      severity: 'warning',
      code: 'unreferenced-vertices',
      message: `${unref.length} vertices are not used by any face.${role === 'base' ? ' They follow the rigid alignment only.' : ''}`,
      count: unref.length,
      samples: unref.slice(0, SAMPLE),
    });
  }

  // --- duplicate vertices ---
  const dup = coincidentPairs(positions, Math.max(diag * 1e-7, 1e-12));
  if (dup.length) {
    const cnt = dup.length / 2;
    issues.push({
      severity: role === 'base' ? 'info' : 'warning',
      code: 'duplicate-vertices',
      message:
        role === 'base'
          ? `${cnt} coincident vertex pairs (typical for UV or hard-edge splits). They are kept separate; Seam Lock keeps them together during wrapping.`
          : `${cnt} coincident vertex pairs. Their surfaces are treated as one where possible.`,
      count: cnt,
      samples: Array.from(dup.slice(0, SAMPLE)),
    });
  }

  // --- polygon edge manifoldness & orientation ---
  const edgeMap = new Map<number, number>(); // key -> packed: count * 4 + (orientation info)
  const edgeDir = new Map<number, number>(); // key -> sum of +1 (i<j) / -1 directions
  let nonManifoldEdges = 0, inconsistent = 0;
  const nmSamples: number[] = [];
  for (let f = 0; f < F; f++) {
    const s = faceOffsets[f], e = faceOffsets[f + 1];
    if (e - s < 3) continue;
    for (let k = s; k < e; k++) {
      const a = faceIndices[k], b = faceIndices[k + 1 < e ? k + 1 : s];
      if (a === b) continue;
      const lo = a < b ? a : b, hi = a < b ? b : a;
      const key = lo * n + hi;
      edgeMap.set(key, (edgeMap.get(key) ?? 0) + 1);
      edgeDir.set(key, (edgeDir.get(key) ?? 0) + (a < b ? 1 : -1));
    }
  }
  let boundaryEdges = 0;
  for (const [key, c] of edgeMap) {
    if (c === 1) boundaryEdges++;
    else if (c > 2) {
      nonManifoldEdges++;
      if (nmSamples.length < SAMPLE) nmSamples.push(Math.floor(key / n));
    } else if (c === 2 && edgeDir.get(key) !== 0) inconsistent++;
  }
  if (nonManifoldEdges) {
    issues.push({
      severity: 'warning',
      code: 'non-manifold-edges',
      message: `${nonManifoldEdges} non-manifold edges (shared by more than two faces). Fitting may pull those sheets together.`,
      count: nonManifoldEdges,
      samples: nmSamples,
    });
  }
  if (inconsistent) {
    issues.push({
      severity: 'warning',
      code: 'inconsistent-orientation',
      message: `${inconsistent} edges join faces with opposite winding (inconsistent normals). ${role === 'reference' ? 'Enable "Two-sided normals" when wrapping.' : 'Normal-based rejection will be unreliable near them.'}`,
      count: inconsistent,
    });
  }

  // --- non-manifold vertices (more than one fan of faces around a vertex) ---
  const nmv = nonManifoldVertices(mesh, n);
  if (nmv.length) {
    issues.push({ severity: 'warning', code: 'non-manifold-vertices', message: `${nmv.length} non-manifold vertices (faces meet only at a point).`, count: nmv.length, samples: nmv.slice(0, SAMPLE) });
  }

  // --- components ---
  const adj = buildAdjacency(triangles, n);
  const comps = connectedComponents(adj);
  const realComps = comps.sizes.filter((s) => s > 1).length;
  if (realComps > 1) {
    const sorted = comps.sizes.filter((s) => s > 1).sort((a, b) => b - a);
    issues.push({
      severity: 'info',
      code: 'components',
      message: `${realComps} disconnected components (largest: ${sorted.slice(0, 3).join(', ')} vertices).`,
      count: realComps,
    });
  }

  // --- area, volume ---
  let area = 0, vol = 0;
  for (let t = 0; t < areas.length; t++) {
    area += areas[t];
    const a = triangles[t * 3] * 3, b = triangles[t * 3 + 1] * 3, c = triangles[t * 3 + 2] * 3;
    vol +=
      (positions[a] * (positions[b + 1] * positions[c + 2] - positions[b + 2] * positions[c + 1]) -
        positions[a + 1] * (positions[b] * positions[c + 2] - positions[b + 2] * positions[c]) +
        positions[a + 2] * (positions[b] * positions[c + 1] - positions[b + 1] * positions[c])) /
      6;
  }
  void normals;
  const closed = boundaryEdges === 0 && nonManifoldEdges === 0;
  if (closed && inconsistent === 0 && vol < 0) {
    issues.push({ severity: 'warning', code: 'inside-out', message: 'Mesh is closed with negative volume: face winding appears inverted (normals point inward).' });
  }
  if (boundaryEdges) {
    issues.push({ severity: 'info', code: 'open-boundary', message: `Open mesh with ${boundaryEdges} boundary edges.`, count: boundaryEdges });
  }

  // --- scale sanity ---
  if (diag > 0 && (diag < 1e-3 || diag > 1e5)) {
    issues.push({ severity: 'warning', code: 'unusual-scale', message: `Bounding-box diagonal is ${diag.toPrecision(3)} units. Check the export units.` });
  }
  if (diag === 0) issues.push({ severity: 'error', code: 'zero-size', message: 'All vertices are at the same position.' });

  const stats: MeshStats = {
    vertices: n,
    faces: F,
    triangles: triangles.length / 3,
    polygonSizes: sizes,
    edges: edgeMap.size,
    boundaryEdges,
    components: comps.sizes.length,
    surfaceArea: area,
    bbox,
    volume: vol,
    closed,
  };
  return { stats, issues, ok: !issues.some((i) => i.severity === 'error') };
}

function emptyStats(n: number, F: number, sizes: Record<string, number>, bbox: BBox): MeshStats {
  return { vertices: n, faces: F, triangles: 0, polygonSizes: sizes, edges: 0, boundaryEdges: 0, components: 0, surfaceArea: 0, bbox, volume: 0, closed: false };
}

/** Vertices whose incident faces split into more than one edge-connected fan. */
function nonManifoldVertices(mesh: PolyMesh, n: number): number[] {
  const { faceOffsets, faceIndices } = mesh;
  const F = faceOffsets.length - 1;
  // vertex -> incident faces (CSR)
  const deg = new Uint32Array(n + 1);
  for (let k = 0; k < faceIndices.length; k++) deg[faceIndices[k] + 1]++;
  for (let i = 0; i < n; i++) deg[i + 1] += deg[i];
  const vf = new Uint32Array(faceIndices.length);
  const fill = deg.slice(0, n);
  for (let f = 0; f < F; f++) for (let k = faceOffsets[f]; k < faceOffsets[f + 1]; k++) vf[fill[faceIndices[k]]++] = f;
  const out: number[] = [];
  const parent: number[] = [];
  for (let v = 0; v < n; v++) {
    const s = deg[v], e = deg[v + 1];
    const m = e - s;
    if (m <= 1) continue;
    parent.length = m;
    for (let i = 0; i < m; i++) parent[i] = i;
    const find = (x: number): number => (parent[x] === x ? x : (parent[x] = find(parent[x])));
    // neighbours of v within each face; faces sharing such a neighbour share an edge at v
    const nbOwner = new Map<number, number>();
    for (let i = 0; i < m; i++) {
      const f = vf[s + i];
      const fs = faceOffsets[f], fe = faceOffsets[f + 1];
      for (let k = fs; k < fe; k++) {
        if (faceIndices[k] !== v) continue;
        const prev = faceIndices[k === fs ? fe - 1 : k - 1];
        const next = faceIndices[k + 1 < fe ? k + 1 : fs];
        for (const u of [prev, next]) {
          const o = nbOwner.get(u);
          if (o === undefined) nbOwner.set(u, i);
          else parent[find(o)] = find(i);
        }
      }
    }
    let roots = 0;
    for (let i = 0; i < m; i++) if (find(i) === i) roots++;
    if (roots > 1) out.push(v);
  }
  return out;
}
