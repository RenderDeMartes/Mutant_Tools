/**
 * Mirroring of surface points across a symmetry plane, snapped back onto the
 * surface (closest point), for left/right landmark pairs.
 */

import { TriangleBVH, makeHit } from '../spatial/bvh';
import { icpAlign } from '../alignment/rigid';
import { mat4Identity, symEig3, transformPositions } from '../core/mat3';
import { computeBBox } from '../core/mesh';
import { evalSurfacePoint, SurfacePoint } from './landmarks';

export interface Plane {
  point: [number, number, number];
  /** unit normal */
  normal: [number, number, number];
}

export function reflect(p: ArrayLike<number>, plane: Plane): [number, number, number] {
  const [nx, ny, nz] = plane.normal;
  const d = (p[0] - plane.point[0]) * nx + (p[1] - plane.point[1]) * ny + (p[2] - plane.point[2]) * nz;
  return [p[0] - 2 * d * nx, p[1] - 2 * d * ny, p[2] - 2 * d * nz];
}

/**
 * Default symmetry plane of a modelled character: x = centre of the bounding
 * box in the mesh's own coordinates (characters are modelled facing ±Z with
 * left/right along X).
 */
export function defaultSymmetryPlane(positions: ArrayLike<number>): Plane {
  const b = computeBBox(positions);
  return { point: [b.center[0], b.center[1], b.center[2]], normal: [1, 0, 0] };
}

/**
 * Fit the symmetry plane of a near-symmetric mesh: reflect sampled vertices
 * across the initial plane, rigidly register the reflected copy onto the
 * surface (ICP), and read the plane from the resulting mirror pairs —
 * normal = principal direction of the pair differences, point = mean
 * midpoint. Works when the initial plane is within ~30° of the true one.
 */
export function fitSymmetryPlane(positions: Float64Array, bvh: TriangleBVH, initial: Plane, rounds = 5): Plane {
  let plane = initial;
  for (let r = 0; r < rounds; r++) {
    const next = fitSymmetryPlaneOnce(positions, bvh, plane, 60);
    const change = 1 - Math.abs(next.normal[0] * plane.normal[0] + next.normal[1] * plane.normal[1] + next.normal[2] * plane.normal[2]);
    plane = next;
    if (change < 1e-8) break;
  }
  return plane;
}

function fitSymmetryPlaneOnce(positions: Float64Array, bvh: TriangleBVH, initial: Plane, iterations: number): Plane {
  const n = positions.length / 3;
  const step = Math.max(1, Math.floor(n / 4000));
  const src: number[] = [];
  const refl: number[] = [];
  for (let i = 0; i < n; i += step) {
    const p = [positions[i * 3], positions[i * 3 + 1], positions[i * 3 + 2]];
    src.push(p[0], p[1], p[2]);
    refl.push(...reflect(p, initial));
  }
  const reflected = Float64Array.from(refl);
  let T: Float64Array;
  try {
    T = icpAlign(reflected, mat4Identity(), bvh, { maxIterations: iterations, trimFraction: 0.85, sampleCount: reflected.length / 3 }).transform;
  } catch {
    return initial;
  }
  const mirrored = transformPositions(reflected, T); // ≈ true mirror image of each source point
  const C = new Float64Array(9);
  let mx = 0, my = 0, mz = 0;
  const m = src.length / 3;
  for (let k = 0; k < m; k++) {
    const ex = src[k * 3] - mirrored[k * 3], ey = src[k * 3 + 1] - mirrored[k * 3 + 1], ez = src[k * 3 + 2] - mirrored[k * 3 + 2];
    C[0] += ex * ex; C[1] += ex * ey; C[2] += ex * ez;
    C[4] += ey * ey; C[5] += ey * ez; C[8] += ez * ez;
    mx += (src[k * 3] + mirrored[k * 3]) / 2;
    my += (src[k * 3 + 1] + mirrored[k * 3 + 1]) / 2;
    mz += (src[k * 3 + 2] + mirrored[k * 3 + 2]) / 2;
  }
  C[3] = C[1]; C[6] = C[2]; C[7] = C[5];
  const w = new Float64Array(3), V = new Float64Array(9);
  symEig3(C, w, V);
  const k = w[0] >= w[1] && w[0] >= w[2] ? 0 : w[1] >= w[2] ? 1 : 2;
  let normal: [number, number, number] = [V[k], V[3 + k], V[6 + k]];
  if (normal[0] * initial.normal[0] + normal[1] * initial.normal[1] + normal[2] * initial.normal[2] < 0) normal = [-normal[0], -normal[1], -normal[2]];
  return { point: [mx / m, my / m, mz / m], normal };
}

/** Mirror a surface point across `plane` and snap it to the closest point of the surface. */
export function mirrorSurfacePoint(positions: Float64Array, triangles: Uint32Array, bvh: TriangleBVH, sp: SurfacePoint, plane: Plane): SurfacePoint {
  const p = evalSurfacePoint(positions, triangles, sp);
  const r = reflect(p, plane);
  const hit = makeHit();
  if (!bvh.closestPoint(r[0], r[1], r[2], Infinity, hit)) throw new Error('Mirror failed: mesh has no faces.');
  return { tri: hit.tri, bary: [hit.u, hit.v, hit.w] };
}
