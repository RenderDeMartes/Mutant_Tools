/**
 * Reusable per-mesh precomputation for the wrapping solver. Both structures
 * depend only on connectivity and on similarity-invariant geometry (cotangent
 * weights, normalised areas), so they can be cached across runs while the
 * rigid alignment changes.
 */

import { computeBBox } from '../core/mesh';
import {
  Adjacency,
  adjacencyIndex,
  buildAdjacency,
  coincidentPairs,
  cotanWeights,
  referencedVertices,
  seamAwareBoundary,
  uniqueEdges,
  vertexAreas,
  vertexNormals,
} from '../geometry/topology';
import { AMG } from '../linalg/amg';
import { ComponentInfo, labelComponents } from '../constraints/components';
import { CSRMatrix, diagonalIndices, findEntry, symmetricPattern } from '../linalg/csr';
import { TriangleBVH } from '../spatial/bvh';

export interface BasePrep {
  n: number;
  triangles: Uint32Array;
  adj: Adjacency;
  /** clamped cotangent weight per adjacency entry (0 for seam pairs) */
  weights: Float64Array;
  /** n * a_i / A (mean 1) */
  areaWeights: Float64Array;
  referenced: Uint8Array;
  /** open-boundary vertices (seams excluded) */
  boundary: Uint8Array;
  /** adjacency of the triangulation only (no seam pairs), for boundary-edge tests */
  triAdj: Adjacency;
  /** coincident-vertex pairs that are not mesh edges */
  seamPairs: Uint32Array;
  pattern: CSRMatrix;
  /** CSR entry for each adjacency entry */
  adjToCsr: Int32Array;
  diag: Int32Array;
  amg: AMG;
  bvh: TriangleBVH;
  /** connected components of the triangulation (seam pairs do not join components) */
  components: ComponentInfo;
}

export interface RefPrep {
  positions: Float64Array;
  triangles: Uint32Array;
  bvh: TriangleBVH;
  normals: Float64Array;
  adj: Adjacency;
  /** open-boundary vertices (seams excluded) */
  boundary: Uint8Array;
  areas: Float64Array;
  referenced: Uint8Array;
  diagonal: number;
}

export function prepareBase(rest: Float64Array, triangles: Uint32Array, seamLock: boolean): BasePrep {
  const n = rest.length / 3;
  const triAdj = buildAdjacency(triangles, n);
  const diag = computeBBox(rest).diagonal || 1;
  let seamPairs: Uint32Array = new Uint32Array(0);
  if (seamLock) {
    const all = coincidentPairs(rest, diag * 1e-7);
    const keep: number[] = [];
    for (let e = 0; e < all.length; e += 2) {
      if (adjacencyIndex(triAdj, all[e], all[e + 1]) < 0) keep.push(all[e], all[e + 1]);
    }
    seamPairs = Uint32Array.from(keep);
  }
  const adj = seamPairs.length ? buildAdjacency(triangles, n, seamPairs) : triAdj;
  const weights = cotanWeights(rest, triangles, adj);
  const areas = vertexAreas(rest, triangles);
  let A = 0;
  for (let i = 0; i < n; i++) A += areas[i];
  const areaWeights = new Float64Array(n);
  if (A > 0) for (let i = 0; i < n; i++) areaWeights[i] = (n * areas[i]) / A;
  const pattern = symmetricPattern(n, uniqueEdges(adj));
  const adjToCsr = new Int32Array(adj.neighbors.length);
  for (let i = 0; i < n; i++) {
    for (let k = adj.offsets[i]; k < adj.offsets[i + 1]; k++) adjToCsr[k] = findEntry(pattern, i, adj.neighbors[k]);
  }
  const diagIdx = diagonalIndices(pattern);
  // AMG hierarchy from the stiffness Laplacian (+ small shift); reused for every solve
  const setup: CSRMatrix = { ...pattern, values: new Float64Array(pattern.values.length) };
  for (let i = 0; i < n; i++) {
    for (let k = adj.offsets[i]; k < adj.offsets[i + 1]; k++) {
      const w = adj.edgeTriCount[k] > 0 ? weights[k] : 1;
      setup.values[adjToCsr[k]] -= w;
      setup.values[diagIdx[i]] += w;
    }
  }
  for (let i = 0; i < n; i++) setup.values[diagIdx[i]] += 1e-3 * Math.max(1e-6, setup.values[diagIdx[i]]) + 1e-9;
  const amg = AMG.build(setup);
  return {
    n,
    triangles,
    adj,
    weights,
    areaWeights,
    referenced: referencedVertices(triangles, n),
    boundary: seamAwareBoundary(rest, triAdj, diag * 1e-7),
    triAdj,
    seamPairs,
    pattern,
    adjToCsr,
    diag: diagIdx,
    amg,
    bvh: TriangleBVH.build(rest.slice(), triangles),
    components: labelComponents(triAdj),
  };
}

export function prepareReference(positions: Float64Array, triangles: Uint32Array): RefPrep {
  const n = positions.length / 3;
  const adj = buildAdjacency(triangles, n);
  return {
    positions,
    triangles,
    bvh: TriangleBVH.build(positions, triangles),
    normals: vertexNormals(positions, triangles),
    adj,
    boundary: seamAwareBoundary(positions, adj, (computeBBox(positions).diagonal || 1) * 1e-7),
    areas: vertexAreas(positions, triangles),
    referenced: referencedVertices(triangles, n),
    diagonal: computeBBox(positions).diagonal,
  };
}
