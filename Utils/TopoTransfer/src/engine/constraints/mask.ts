/**
 * Per-vertex region masks (values in [0, 1]) used for protected regions and
 * partial fitting. Masks never change topology; they only scale solver terms.
 */

import type { Adjacency } from '../geometry/topology';

export type MaskMode = 'protect' | 'fitOnly';

export function createMask(n: number): Float32Array {
  return new Float32Array(n);
}

/**
 * Paint a sphere of `radius` around `center`, blending towards `value` with a
 * smooth falloff (`hardness` 1 = hard edge, 0 = fully smooth).
 */
export function paintSphere(
  mask: Float32Array,
  positions: ArrayLike<number>,
  center: ArrayLike<number>,
  radius: number,
  value: number,
  hardness = 0.5,
): number {
  let touched = 0;
  const r2 = radius * radius;
  const inner = Math.max(0, Math.min(1, hardness));
  for (let i = 0; i < mask.length; i++) {
    const dx = positions[i * 3] - center[0], dy = positions[i * 3 + 1] - center[1], dz = positions[i * 3 + 2] - center[2];
    const d2 = dx * dx + dy * dy + dz * dz;
    if (d2 > r2) continue;
    const d = Math.sqrt(d2) / radius;
    let f = 1;
    if (d > inner) {
      const t = (d - inner) / Math.max(1e-9, 1 - inner);
      f = 1 - t * t * (3 - 2 * t);
    }
    const old = mask[i];
    const nv = old + (value - old) * f;
    mask[i] = value > old ? Math.max(old, nv) : Math.min(old, nv);
    touched++;
  }
  return touched;
}

export function invertMask(mask: Float32Array): void {
  for (let i = 0; i < mask.length; i++) mask[i] = 1 - mask[i];
}

/** Laplacian smoothing of mask values over the mesh graph. */
export function smoothMask(mask: Float32Array, adj: Adjacency, iterations = 1): void {
  const tmp = new Float32Array(mask.length);
  for (let it = 0; it < iterations; it++) {
    for (let i = 0; i < mask.length; i++) {
      const s = adj.offsets[i], e = adj.offsets[i + 1];
      if (e === s) {
        tmp[i] = mask[i];
        continue;
      }
      let acc = 0;
      for (let k = s; k < e; k++) acc += mask[adj.neighbors[k]];
      tmp[i] = 0.5 * mask[i] + 0.5 * (acc / (e - s));
    }
    mask.set(tmp);
  }
}

/** Morphological dilation (grow = true) or erosion over one ring of neighbours. */
export function growMask(mask: Float32Array, adj: Adjacency, grow: boolean): void {
  const tmp = mask.slice();
  for (let i = 0; i < mask.length; i++) {
    let v = mask[i];
    for (let k = adj.offsets[i]; k < adj.offsets[i + 1]; k++) {
      const u = mask[adj.neighbors[k]];
      v = grow ? Math.max(v, u) : Math.min(v, u);
    }
    tmp[i] = v;
  }
  mask.set(tmp);
}

/**
 * Effective protection per vertex: in 'protect' mode the painted value; in
 * 'fitOnly' mode its complement (unpainted vertices are protected).
 */
export function protectionWeights(mask: Float32Array | null, mode: MaskMode, n: number): Float32Array {
  const out = new Float32Array(n);
  if (!mask) {
    if (mode === 'fitOnly') out.fill(1);
    return out;
  }
  for (let i = 0; i < n; i++) {
    const m = Math.max(0, Math.min(1, mask[i]));
    out[i] = mode === 'protect' ? m : 1 - m;
  }
  return out;
}

export function maskCoverage(mask: Float32Array): number {
  let s = 0;
  for (let i = 0; i < mask.length; i++) s += mask[i];
  return mask.length ? s / mask.length : 0;
}
