/**
 * Landmark correspondences. A landmark pairs a surface point on the base mesh
 * (triangle + barycentric weights, so it follows the deforming surface) with a
 * fixed point on the reference mesh.
 */

import { umeyama, SimilarityFit } from '../alignment/rigid';

export const LANDMARK_GROUPS = ['face', 'eyes', 'nose', 'mouth', 'ears', 'body', 'other'] as const;
export type LandmarkGroup = (typeof LANDMARK_GROUPS)[number];

export interface SurfacePoint {
  /** triangle index in the mesh's deterministic fan triangulation */
  tri: number;
  /** barycentric weights for the triangle's corners */
  bary: [number, number, number];
}

export interface Landmark {
  id: number;
  label: string;
  group: LandmarkGroup;
  weight: number;
  base: SurfacePoint | null;
  ref: SurfacePoint | null;
}

export function evalSurfacePoint(positions: ArrayLike<number>, triangles: Uint32Array, sp: SurfacePoint): [number, number, number] {
  const a = triangles[sp.tri * 3] * 3, b = triangles[sp.tri * 3 + 1] * 3, c = triangles[sp.tri * 3 + 2] * 3;
  const [u, v, w] = sp.bary;
  return [
    u * positions[a] + v * positions[b] + w * positions[c],
    u * positions[a + 1] + v * positions[b + 1] + w * positions[c + 1],
    u * positions[a + 2] + v * positions[b + 2] + w * positions[c + 2],
  ];
}

export function isComplete(l: Landmark): l is Landmark & { base: SurfacePoint; ref: SurfacePoint } {
  return l.base !== null && l.ref !== null;
}

/** Validate a surface point against a triangle count; returns an error message or null. */
export function checkSurfacePoint(sp: SurfacePoint, triangleCount: number): string | null {
  if (!Number.isInteger(sp.tri) || sp.tri < 0 || sp.tri >= triangleCount) return `triangle ${sp.tri} out of range`;
  const s = sp.bary[0] + sp.bary[1] + sp.bary[2];
  if (!sp.bary.every(Number.isFinite) || Math.abs(s - 1) > 1e-6) return 'barycentric weights must sum to 1';
  return null;
}

/**
 * Similarity (or rigid) transform that maps base landmark positions onto the
 * reference landmark positions. `basePositions` are untransformed base
 * coordinates, so the result directly replaces the base placement transform.
 */
export function alignFromLandmarks(
  landmarks: Landmark[],
  basePositions: ArrayLike<number>,
  baseTriangles: Uint32Array,
  refPositions: ArrayLike<number>,
  refTriangles: Uint32Array,
  allowScale: boolean,
): SimilarityFit {
  const pairs = landmarks.filter(isComplete);
  if (pairs.length < 3) throw new Error(`Landmark alignment needs at least 3 complete landmark pairs (have ${pairs.length}).`);
  const src = new Float64Array(pairs.length * 3);
  const dst = new Float64Array(pairs.length * 3);
  const w = new Float64Array(pairs.length);
  pairs.forEach((l, k) => {
    src.set(evalSurfacePoint(basePositions, baseTriangles, l.base), k * 3);
    dst.set(evalSurfacePoint(refPositions, refTriangles, l.ref), k * 3);
    w[k] = Math.max(1e-6, l.weight);
  });
  return umeyama(src, dst, w, allowScale);
}
