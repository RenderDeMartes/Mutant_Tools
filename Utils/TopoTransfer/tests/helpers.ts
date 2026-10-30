import { PolyMesh, triangulate } from '../src/engine/core/mesh';
import { mat4FromSimilarity, transformPositions } from '../src/engine/core/mat3';
import { TriangleBVH } from '../src/engine/spatial/bvh';
import { pointToSurfaceDistances } from '../src/engine/validation/metrics';

/** Rotation matrix (row-major) about a unit axis. */
export function axisAngle(axis: [number, number, number], angle: number): Float64Array {
  const [x, y, z] = axis.map((v) => v / Math.hypot(...axis));
  const c = Math.cos(angle), s = Math.sin(angle), t = 1 - c;
  return Float64Array.from([
    t * x * x + c, t * x * y - s * z, t * x * z + s * y,
    t * x * y + s * z, t * y * y + c, t * y * z - s * x,
    t * x * z - s * y, t * y * z + s * x, t * z * z + c,
  ]);
}

export function similarity(axis: [number, number, number], angle: number, scale: number, t: [number, number, number]) {
  return mat4FromSimilarity(axisAngle(axis, angle), scale, t);
}

export function transformed(mesh: PolyMesh, m: ArrayLike<number>): PolyMesh {
  return { ...mesh, positions: transformPositions(mesh.positions, m) };
}

/** Mean distance from points to a mesh surface. */
export function meanDistance(points: Float64Array, target: PolyMesh): number {
  const bvh = TriangleBVH.build(target.positions, triangulate(target).triangles);
  return pointToSurfaceDistances(points, bvh).mean;
}

/** Deterministic pseudo-random generator. */
export function rng(seed = 1) {
  let s = seed >>> 0;
  return () => {
    s = (Math.imul(s, 1664525) + 1013904223) >>> 0;
    return s / 4294967296;
  };
}

export function dist(p: ArrayLike<number>, i: number, q: ArrayLike<number>): number {
  return Math.hypot(p[i * 3] - q[0], p[i * 3 + 1] - q[1], p[i * 3 + 2] - q[2]);
}
