/**
 * Bounding volume hierarchy over triangles for exact closest-point-on-surface
 * queries and ray casting. Positions may be updated in place followed by
 * `refit()` (topology stays fixed), which is how the deforming base mesh is
 * queried during reverse correspondences.
 */

/** Region of the triangle the closest point lies in. */
export enum TriRegion {
  Face = 0,
  EdgeAB = 1,
  EdgeBC = 2,
  EdgeCA = 3,
  VertA = 4,
  VertB = 5,
  VertC = 6,
}

export interface ClosestHit {
  tri: number;
  distSq: number;
  x: number;
  y: number;
  z: number;
  /** barycentric weights for triangle corners a, b, c */
  u: number;
  v: number;
  w: number;
  region: TriRegion;
}

export interface RayHit {
  tri: number;
  t: number;
  u: number;
  v: number;
  w: number;
}

export function makeHit(): ClosestHit {
  return { tri: -1, distSq: Infinity, x: 0, y: 0, z: 0, u: 0, v: 0, w: 0, region: TriRegion.Face };
}

const LEAF_SIZE = 4;

export class TriangleBVH {
  positions: Float64Array;
  readonly triangles: Uint32Array;
  /** bounds per node: minx miny minz maxx maxy maxz */
  readonly bounds: Float64Array;
  /** per node: [firstChild or -1, start, count] */
  readonly nodes: Int32Array;
  readonly order: Uint32Array;
  readonly nodeCount: number;
  private stack = new Int32Array(256);
  private stackD = new Float64Array(256);

  private constructor(positions: Float64Array, triangles: Uint32Array, bounds: Float64Array, nodes: Int32Array, order: Uint32Array, nodeCount: number) {
    this.positions = positions;
    this.triangles = triangles;
    this.bounds = bounds;
    this.nodes = nodes;
    this.order = order;
    this.nodeCount = nodeCount;
  }

  static build(positions: Float64Array, triangles: Uint32Array): TriangleBVH {
    const T = triangles.length / 3;
    const cent = new Float64Array(T * 3);
    for (let t = 0; t < T; t++) {
      const a = triangles[t * 3] * 3, b = triangles[t * 3 + 1] * 3, c = triangles[t * 3 + 2] * 3;
      cent[t * 3] = (positions[a] + positions[b] + positions[c]) / 3;
      cent[t * 3 + 1] = (positions[a + 1] + positions[b + 1] + positions[c + 1]) / 3;
      cent[t * 3 + 2] = (positions[a + 2] + positions[b + 2] + positions[c + 2]) / 3;
    }
    const order = new Uint32Array(T);
    for (let t = 0; t < T; t++) order[t] = t;
    const maxNodes = Math.max(1, 2 * Math.ceil(T / LEAF_SIZE) * 2);
    let nodes = new Int32Array(maxNodes * 3);
    let nodeCount = 1;
    nodes[0] = -1;
    nodes[1] = 0;
    nodes[2] = T;
    const work: number[] = [0];
    while (work.length) {
      const node = work.pop()!;
      const start = nodes[node * 3 + 1];
      const count = nodes[node * 3 + 2];
      if (count <= LEAF_SIZE) continue;
      // centroid bounds
      let mnx = Infinity, mny = Infinity, mnz = Infinity, mxx = -Infinity, mxy = -Infinity, mxz = -Infinity;
      for (let k = start; k < start + count; k++) {
        const t = order[k] * 3;
        const x = cent[t], y = cent[t + 1], z = cent[t + 2];
        if (x < mnx) mnx = x; if (x > mxx) mxx = x;
        if (y < mny) mny = y; if (y > mxy) mxy = y;
        if (z < mnz) mnz = z; if (z > mxz) mxz = z;
      }
      const ex = mxx - mnx, ey = mxy - mny, ez = mxz - mnz;
      const axis = ex >= ey && ex >= ez ? 0 : ey >= ez ? 1 : 2;
      const extent = axis === 0 ? ex : axis === 1 ? ey : ez;
      if (extent <= 0) continue; // all centroids identical -> leaf
      const split = (axis === 0 ? mnx : axis === 1 ? mny : mnz) + extent / 2;
      // partition
      let i = start, j = start + count - 1;
      while (i <= j) {
        if (cent[order[i] * 3 + axis] < split) i++;
        else {
          const tmp = order[i];
          order[i] = order[j];
          order[j] = tmp;
          j--;
        }
      }
      let mid = i;
      if (mid === start || mid === start + count) mid = start + (count >> 1);
      if (nodeCount + 2 > nodes.length / 3) {
        const grown = new Int32Array(nodes.length * 2);
        grown.set(nodes);
        nodes = grown;
      }
      const left = nodeCount;
      nodeCount += 2;
      nodes[node * 3] = left;
      nodes[left * 3] = -1;
      nodes[left * 3 + 1] = start;
      nodes[left * 3 + 2] = mid - start;
      nodes[(left + 1) * 3] = -1;
      nodes[(left + 1) * 3 + 1] = mid;
      nodes[(left + 1) * 3 + 2] = start + count - mid;
      work.push(left, left + 1);
    }
    const bvh = new TriangleBVH(positions, triangles, new Float64Array(nodeCount * 6), nodes.slice(0, nodeCount * 3), order, nodeCount);
    bvh.refit(positions);
    return bvh;
  }

  /** Recompute node bounds for (possibly new) vertex positions with the same topology. */
  refit(positions: Float64Array = this.positions): void {
    this.positions = positions;
    const { nodes, bounds, order, triangles } = this;
    for (let node = this.nodeCount - 1; node >= 0; node--) {
      const child = nodes[node * 3];
      const o = node * 6;
      if (child < 0) {
        let mnx = Infinity, mny = Infinity, mnz = Infinity, mxx = -Infinity, mxy = -Infinity, mxz = -Infinity;
        const start = nodes[node * 3 + 1], end = start + nodes[node * 3 + 2];
        for (let k = start; k < end; k++) {
          const t = order[k] * 3;
          for (let c = 0; c < 3; c++) {
            const p = triangles[t + c] * 3;
            const x = positions[p], y = positions[p + 1], z = positions[p + 2];
            if (x < mnx) mnx = x; if (x > mxx) mxx = x;
            if (y < mny) mny = y; if (y > mxy) mxy = y;
            if (z < mnz) mnz = z; if (z > mxz) mxz = z;
          }
        }
        bounds[o] = mnx; bounds[o + 1] = mny; bounds[o + 2] = mnz;
        bounds[o + 3] = mxx; bounds[o + 4] = mxy; bounds[o + 5] = mxz;
      } else {
        const a = child * 6, b = (child + 1) * 6;
        for (let k = 0; k < 3; k++) {
          bounds[o + k] = Math.min(bounds[a + k], bounds[b + k]);
          bounds[o + 3 + k] = Math.max(bounds[a + 3 + k], bounds[b + 3 + k]);
        }
      }
    }
  }

  private boxDistSq(node: number, x: number, y: number, z: number): number {
    const o = node * 6, b = this.bounds;
    let d = 0, v: number;
    v = b[o] - x; if (v > 0) d += v * v; else { v = x - b[o + 3]; if (v > 0) d += v * v; }
    v = b[o + 1] - y; if (v > 0) d += v * v; else { v = y - b[o + 4]; if (v > 0) d += v * v; }
    v = b[o + 2] - z; if (v > 0) d += v * v; else { v = z - b[o + 5]; if (v > 0) d += v * v; }
    return d;
  }

  /**
   * Closest point on the surface to (x,y,z) within sqrt(maxDistSq).
   * Returns false (hit untouched except distSq) when nothing is in range.
   * `hintTri` (e.g. last iteration's answer) is tested first to tighten the
   * search bound; the result is still the exact closest point.
   */
  closestPoint(x: number, y: number, z: number, maxDistSq: number, hit: ClosestHit, hintTri = -1): boolean {
    hit.tri = -1;
    hit.distSq = maxDistSq;
    if (this.triangles.length === 0) return false;
    if (hintTri >= 0) closestOnTriangle(this.positions, this.triangles, hintTri, x, y, z, hit);
    let stack = this.stack, stackD = this.stackD;
    let sp = 0;
    stack[sp] = 0;
    stackD[sp] = this.boxDistSq(0, x, y, z);
    sp++;
    const { nodes, order, triangles, positions } = this;
    while (sp > 0) {
      sp--;
      const node = stack[sp];
      if (stackD[sp] >= hit.distSq) continue;
      const child = nodes[node * 3];
      if (child < 0) {
        const start = nodes[node * 3 + 1], end = start + nodes[node * 3 + 2];
        for (let k = start; k < end; k++) {
          const t = order[k];
          closestOnTriangle(positions, triangles, t, x, y, z, hit);
        }
      } else {
        const dl = this.boxDistSq(child, x, y, z);
        const dr = this.boxDistSq(child + 1, x, y, z);
        if (sp + 2 >= stack.length) {
          const s2 = new Int32Array(stack.length * 2); s2.set(stack); stack = this.stack = s2;
          const d2 = new Float64Array(stackD.length * 2); d2.set(stackD); stackD = this.stackD = d2;
        }
        // push farther first so nearer is processed first
        if (dl < dr) {
          if (dr < hit.distSq) { stack[sp] = child + 1; stackD[sp] = dr; sp++; }
          if (dl < hit.distSq) { stack[sp] = child; stackD[sp] = dl; sp++; }
        } else {
          if (dl < hit.distSq) { stack[sp] = child; stackD[sp] = dl; sp++; }
          if (dr < hit.distSq) { stack[sp] = child + 1; stackD[sp] = dr; sp++; }
        }
      }
    }
    return hit.tri >= 0;
  }

  /** Nearest ray intersection (two-sided). Direction need not be normalised; t is in units of it. */
  raycast(ox: number, oy: number, oz: number, dx: number, dy: number, dz: number, hit: RayHit, tMax = Infinity): boolean {
    hit.tri = -1;
    hit.t = tMax;
    if (this.triangles.length === 0) return false;
    const idx = 1 / dx, idy = 1 / dy, idz = 1 / dz;
    const stack: number[] = [0];
    const { nodes, bounds, order, triangles, positions } = this;
    while (stack.length) {
      const node = stack.pop()!;
      const o = node * 6;
      // slab test
      let t0 = 0, t1 = hit.t;
      let ta = (bounds[o] - ox) * idx, tb = (bounds[o + 3] - ox) * idx;
      if (ta > tb) { const s = ta; ta = tb; tb = s; }
      t0 = ta > t0 ? ta : t0; t1 = tb < t1 ? tb : t1;
      ta = (bounds[o + 1] - oy) * idy; tb = (bounds[o + 4] - oy) * idy;
      if (ta > tb) { const s = ta; ta = tb; tb = s; }
      t0 = ta > t0 ? ta : t0; t1 = tb < t1 ? tb : t1;
      ta = (bounds[o + 2] - oz) * idz; tb = (bounds[o + 5] - oz) * idz;
      if (ta > tb) { const s = ta; ta = tb; tb = s; }
      t0 = ta > t0 ? ta : t0; t1 = tb < t1 ? tb : t1;
      if (!(t0 <= t1)) continue; // also rejects NaN
      const child = nodes[node * 3];
      if (child >= 0) {
        stack.push(child, child + 1);
        continue;
      }
      const start = nodes[node * 3 + 1], end = start + nodes[node * 3 + 2];
      for (let k = start; k < end; k++) {
        const t = order[k];
        const a = triangles[t * 3] * 3, b = triangles[t * 3 + 1] * 3, c = triangles[t * 3 + 2] * 3;
        const e1x = positions[b] - positions[a], e1y = positions[b + 1] - positions[a + 1], e1z = positions[b + 2] - positions[a + 2];
        const e2x = positions[c] - positions[a], e2y = positions[c + 1] - positions[a + 1], e2z = positions[c + 2] - positions[a + 2];
        const px = dy * e2z - dz * e2y, py = dz * e2x - dx * e2z, pz = dx * e2y - dy * e2x;
        const det = e1x * px + e1y * py + e1z * pz;
        if (Math.abs(det) < 1e-300) continue;
        const inv = 1 / det;
        const sx = ox - positions[a], sy = oy - positions[a + 1], sz = oz - positions[a + 2];
        const u = (sx * px + sy * py + sz * pz) * inv;
        if (u < 0 || u > 1) continue;
        const qx = sy * e1z - sz * e1y, qy = sz * e1x - sx * e1z, qz = sx * e1y - sy * e1x;
        const v = (dx * qx + dy * qy + dz * qz) * inv;
        if (v < 0 || u + v > 1) continue;
        const tt = (e2x * qx + e2y * qy + e2z * qz) * inv;
        if (tt > 0 && tt < hit.t) {
          hit.t = tt;
          hit.tri = t;
          hit.u = 1 - u - v;
          hit.v = u;
          hit.w = v;
        }
      }
    }
    return hit.tri >= 0;
  }
}

/**
 * Closest point on triangle t to p (Ericson, Real-Time Collision Detection 5.1.5).
 * Updates `hit` only if closer than hit.distSq.
 */
export function closestOnTriangle(positions: Float64Array, triangles: Uint32Array, t: number, px: number, py: number, pz: number, hit: ClosestHit): void {
  const ia = triangles[t * 3] * 3, ib = triangles[t * 3 + 1] * 3, ic = triangles[t * 3 + 2] * 3;
  const ax = positions[ia], ay = positions[ia + 1], az = positions[ia + 2];
  const bx = positions[ib], by = positions[ib + 1], bz = positions[ib + 2];
  const cx = positions[ic], cy = positions[ic + 1], cz = positions[ic + 2];
  const abx = bx - ax, aby = by - ay, abz = bz - az;
  const acx = cx - ax, acy = cy - ay, acz = cz - az;
  const apx = px - ax, apy = py - ay, apz = pz - az;
  let u: number, v: number, w: number, region: TriRegion;
  const d1 = abx * apx + aby * apy + abz * apz;
  const d2 = acx * apx + acy * apy + acz * apz;
  if (d1 <= 0 && d2 <= 0) {
    u = 1; v = 0; w = 0; region = TriRegion.VertA;
  } else {
    const bpx = px - bx, bpy = py - by, bpz = pz - bz;
    const d3 = abx * bpx + aby * bpy + abz * bpz;
    const d4 = acx * bpx + acy * bpy + acz * bpz;
    if (d3 >= 0 && d4 <= d3) {
      u = 0; v = 1; w = 0; region = TriRegion.VertB;
    } else {
      const vc = d1 * d4 - d3 * d2;
      if (vc <= 0 && d1 >= 0 && d3 <= 0) {
        const s = d1 / (d1 - d3);
        u = 1 - s; v = s; w = 0; region = TriRegion.EdgeAB;
      } else {
        const cpx = px - cx, cpy = py - cy, cpz = pz - cz;
        const d5 = abx * cpx + aby * cpy + abz * cpz;
        const d6 = acx * cpx + acy * cpy + acz * cpz;
        if (d6 >= 0 && d5 <= d6) {
          u = 0; v = 0; w = 1; region = TriRegion.VertC;
        } else {
          const vb = d5 * d2 - d1 * d6;
          if (vb <= 0 && d2 >= 0 && d6 <= 0) {
            const s = d2 / (d2 - d6);
            u = 1 - s; v = 0; w = s; region = TriRegion.EdgeCA;
          } else {
            const va = d3 * d6 - d5 * d4;
            if (va <= 0 && d4 - d3 >= 0 && d5 - d6 >= 0) {
              const s = (d4 - d3) / (d4 - d3 + (d5 - d6));
              u = 0; v = 1 - s; w = s; region = TriRegion.EdgeBC;
            } else {
              const denom = 1 / (va + vb + vc);
              if (!Number.isFinite(denom)) {
                u = 1; v = 0; w = 0; region = TriRegion.VertA;
              } else {
                v = vb * denom; w = vc * denom; u = 1 - v - w; region = TriRegion.Face;
              }
            }
          }
        }
      }
    }
  }
  const qx = u * ax + v * bx + w * cx;
  const qy = u * ay + v * by + w * cy;
  const qz = u * az + v * bz + w * cz;
  const dx = px - qx, dy = py - qy, dz = pz - qz;
  const d = dx * dx + dy * dy + dz * dz;
  if (d < hit.distSq) {
    hit.distSq = d;
    hit.tri = t;
    hit.x = qx; hit.y = qy; hit.z = qz;
    hit.u = u; hit.v = v; hit.w = w;
    hit.region = region;
  }
}
