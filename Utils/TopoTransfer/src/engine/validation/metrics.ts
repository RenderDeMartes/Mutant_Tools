/**
 * Measured fitting and mesh-quality metrics. Every number here is computed
 * from the actual geometry (no estimates); distances are sampled at vertices.
 */

import { closestRotation } from '../core/mat3';
import { TriangleBVH, makeHit } from '../spatial/bvh';
import { triangleNormalsAreas, Adjacency, uniqueEdges } from '../geometry/topology';

export interface DistanceStats {
  /** number of sample points measured */
  count: number;
  mean: number;
  rms: number;
  max: number;
  p95: number;
}

export function emptyStats(): DistanceStats {
  return { count: 0, mean: 0, rms: 0, max: 0, p95: 0 };
}

export function statsFromDistances(d: Float64Array, count = d.length): DistanceStats {
  if (count === 0) return emptyStats();
  let s = 0, s2 = 0, mx = 0;
  for (let i = 0; i < count; i++) {
    s += d[i];
    s2 += d[i] * d[i];
    if (d[i] > mx) mx = d[i];
  }
  const sorted = d.slice(0, count).sort();
  const p95 = sorted[Math.min(count - 1, Math.floor(0.95 * (count - 1)))];
  return { count, mean: s / count, rms: Math.sqrt(s2 / count), max: mx, p95 };
}

/**
 * Distance from each (selected) point to the surface in `bvh`.
 * `select` optionally restricts which points are measured; `perPoint` receives
 * individual distances (NaN for skipped points) when provided.
 */
export function pointToSurfaceDistances(
  positions: Float64Array,
  bvh: TriangleBVH,
  select?: (i: number) => boolean,
  perPoint?: Float64Array,
  stride = 1,
): DistanceStats {
  const n = positions.length / 3;
  const d = new Float64Array(Math.ceil(n / stride));
  let c = 0;
  const hit = makeHit();
  if (perPoint) perPoint.fill(NaN);
  for (let i = 0; i < n; i += stride) {
    if (select && !select(i)) continue;
    bvh.closestPoint(positions[i * 3], positions[i * 3 + 1], positions[i * 3 + 2], Infinity, hit);
    const v = Math.sqrt(hit.distSq);
    d[c++] = v;
    if (perPoint) perPoint[i] = v;
  }
  return statsFromDistances(d, c);
}

export interface QualityReport {
  triangles: number;
  /** triangles whose normal reversed relative to the (locally rotated) rest normal */
  flippedTriangles: number;
  /** triangles whose area fell below 5% of rest area */
  collapsedTriangles: number;
  /** edges whose length ratio is outside [1/3, 3] */
  stretchedEdges: number;
  edges: number;
  minEdgeRatio: number;
  maxEdgeRatio: number;
  minAreaRatio: number;
  maxAreaRatio: number;
}

/**
 * Compare deformed positions against rest positions. If per-vertex rotations
 * are supplied (row-major 3x3 per vertex) they are used to rotate the rest
 * normal before the flip test, so large but valid bends are not flagged.
 */
export function qualityReport(
  rest: Float64Array,
  deformed: Float64Array,
  triangles: Uint32Array,
  adj: Adjacency,
  rotations?: Float64Array,
): QualityReport {
  const r = triangleNormalsAreas(rest, triangles);
  const d = triangleNormalsAreas(deformed, triangles);
  const T = triangles.length / 3;
  let flipped = 0, collapsed = 0;
  let minA = Infinity, maxA = 0;
  for (let t = 0; t < T; t++) {
    const ar = r.areas[t];
    if (!(ar > 0)) continue;
    const ratio = d.areas[t] / ar;
    if (ratio < minA) minA = ratio;
    if (ratio > maxA) maxA = ratio;
    if (ratio < 0.05) collapsed++;
    let nx = r.normals[t * 3], ny = r.normals[t * 3 + 1], nz = r.normals[t * 3 + 2];
    if (rotations) {
      const o = triangles[t * 3] * 9;
      const rx = rotations[o] * nx + rotations[o + 1] * ny + rotations[o + 2] * nz;
      const ry = rotations[o + 3] * nx + rotations[o + 4] * ny + rotations[o + 5] * nz;
      const rz = rotations[o + 6] * nx + rotations[o + 7] * ny + rotations[o + 8] * nz;
      nx = rx; ny = ry; nz = rz;
    }
    const dot = nx * d.normals[t * 3] + ny * d.normals[t * 3 + 1] + nz * d.normals[t * 3 + 2];
    if (d.areas[t] > 0 && dot < 0) flipped++;
  }
  const edges = uniqueEdges(adj);
  let stretched = 0, minE = Infinity, maxE = 0, counted = 0;
  for (let e = 0; e < edges.length; e += 2) {
    const i = edges[e] * 3, j = edges[e + 1] * 3;
    const lr = Math.hypot(rest[i] - rest[j], rest[i + 1] - rest[j + 1], rest[i + 2] - rest[j + 2]);
    if (!(lr > 0)) continue;
    const ld = Math.hypot(deformed[i] - deformed[j], deformed[i + 1] - deformed[j + 1], deformed[i + 2] - deformed[j + 2]);
    const ratio = ld / lr;
    counted++;
    if (ratio < minE) minE = ratio;
    if (ratio > maxE) maxE = ratio;
    if (ratio > 3 || ratio < 1 / 3) stretched++;
  }
  return {
    triangles: T,
    flippedTriangles: flipped,
    collapsedTriangles: collapsed,
    stretchedEdges: stretched,
    edges: counted,
    minEdgeRatio: counted ? minE : 1,
    maxEdgeRatio: counted ? maxE : 1,
    minAreaRatio: Number.isFinite(minA) ? minA : 1,
    maxAreaRatio: maxA || 1,
  };
}

/** Per-vertex best-fit rotations between rest and deformed one-rings (used for flip tests outside the solver). */
export function fitRotations(rest: Float64Array, deformed: Float64Array, adj: Adjacency, weights?: Float64Array): Float64Array {
  const n = adj.n;
  const R = new Float64Array(n * 9);
  const M = new Float64Array(9);
  const Ri = new Float64Array(9);
  for (let i = 0; i < n; i++) {
    M.fill(0);
    for (let k = adj.offsets[i]; k < adj.offsets[i + 1]; k++) {
      const j = adj.neighbors[k];
      const w = weights ? weights[k] : 1;
      const ex = deformed[i * 3] - deformed[j * 3], ey = deformed[i * 3 + 1] - deformed[j * 3 + 1], ez = deformed[i * 3 + 2] - deformed[j * 3 + 2];
      const fx = rest[i * 3] - rest[j * 3], fy = rest[i * 3 + 1] - rest[j * 3 + 1], fz = rest[i * 3 + 2] - rest[j * 3 + 2];
      M[0] += w * ex * fx; M[1] += w * ex * fy; M[2] += w * ex * fz;
      M[3] += w * ey * fx; M[4] += w * ey * fy; M[5] += w * ey * fz;
      M[6] += w * ez * fx; M[7] += w * ez * fy; M[8] += w * ez * fz;
    }
    if (adj.offsets[i + 1] === adj.offsets[i]) {
      Ri.fill(0); Ri[0] = Ri[4] = Ri[8] = 1;
    } else {
      closestRotation(M, Ri);
    }
    R.set(Ri, i * 9);
  }
  return R;
}
