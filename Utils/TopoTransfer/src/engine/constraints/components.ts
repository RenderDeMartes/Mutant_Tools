/**
 * Per-component handling for multi-part base meshes (eyeballs, teeth, tongue,
 * eyelashes...). Such parts are not on the outer surface the reference
 * describes, so fitting them to closest points would pull them onto the skin.
 *
 * Modes:
 *  - 'fit'    : fitted to the reference like the main surface.
 *  - 'follow' : not fitted; after wrapping, the component is moved by the
 *               best-fit similarity transform (rotation + uniform scale +
 *               translation) of the fitted surface around it, so it keeps its
 *               own shape (an eyeball stays a sphere) and stays in place
 *               relative to the surrounding skin.
 *  - 'fixed'  : not fitted and not moved (keeps the aligned rest position).
 */

import { umeyama } from '../alignment/rigid';
import { transformPositions } from '../core/mat3';
import type { Adjacency } from '../geometry/topology';
import { connectedComponents } from '../geometry/topology';

export type ComponentMode = 'fit' | 'follow' | 'fixed';

export interface ComponentInfo {
  /** component label per vertex */
  labels: Int32Array;
  /** vertex count per component */
  sizes: number[];
}

export function labelComponents(adj: Adjacency): ComponentInfo {
  return connectedComponents(adj);
}

/**
 * Default modes: every component with at least 25% of the largest
 * component's vertex count is fitted, smaller ones follow, and single
 * unreferenced vertices are fixed.
 */
export function defaultComponentModes(sizes: number[]): ComponentMode[] {
  const largest = Math.max(0, ...sizes);
  return sizes.map((s) => (s <= 1 ? 'fixed' : s >= 0.25 * largest ? 'fit' : 'follow'));
}

/** Per-vertex flag: 1 when the vertex belongs to a fitted component. */
export function fitVertexMask(info: ComponentInfo, modes: ComponentMode[] | null | undefined): Uint8Array {
  const n = info.labels.length;
  const out = new Uint8Array(n);
  for (let i = 0; i < n; i++) out[i] = !modes || modes[info.labels[i]] === 'fit' ? 1 : 0;
  return out;
}

export interface FollowReport {
  component: number;
  mode: ComponentMode;
  drivers: number;
  scale: number;
  /** RMS residual of the similarity fit on the driver vertices (measured) */
  rms: number;
}

/**
 * Move 'follow' components with the fitted surface and reset 'fixed' ones to
 * rest. `result` is modified in place. Driver vertices are the fitted
 * vertices nearest to each component (by rest position), weighted by
 * proximity.
 */
export function applyComponentModes(
  rest: Float64Array,
  result: Float64Array,
  info: ComponentInfo,
  modes: ComponentMode[],
): FollowReport[] {
  const n = rest.length / 3;
  const fitIdx: number[] = [];
  for (let i = 0; i < n; i++) if (modes[info.labels[i]] === 'fit') fitIdx.push(i);
  const members: number[][] = info.sizes.map(() => []);
  for (let i = 0; i < n; i++) members[info.labels[i]].push(i);
  const reports: FollowReport[] = [];
  for (let c = 0; c < info.sizes.length; c++) {
    const mode = modes[c];
    if (mode === 'fit') continue;
    const verts = members[c];
    if (mode === 'fixed' || fitIdx.length < 3) {
      for (const v of verts) for (let k = 0; k < 3; k++) result[v * 3 + k] = rest[v * 3 + k];
      reports.push({ component: c, mode: mode === 'fixed' ? 'fixed' : 'follow', drivers: 0, scale: 1, rms: 0 });
      continue;
    }
    // component centre and radius (rest)
    const ctr = [0, 0, 0];
    for (const v of verts) for (let k = 0; k < 3; k++) ctr[k] += rest[v * 3 + k] / verts.length;
    let radius = 0;
    for (const v of verts) radius = Math.max(radius, Math.hypot(rest[v * 3] - ctr[0], rest[v * 3 + 1] - ctr[1], rest[v * 3 + 2] - ctr[2]));
    radius = Math.max(radius, 1e-12);
    // nearest fitted vertices to the component (distance to the closest component vertex, approximated by centre distance - radius)
    const K = Math.min(fitIdx.length, Math.max(48, Math.min(400, verts.length * 4)));
    const d2 = new Float64Array(fitIdx.length);
    for (let j = 0; j < fitIdx.length; j++) {
      const v = fitIdx[j];
      d2[j] = (rest[v * 3] - ctr[0]) ** 2 + (rest[v * 3 + 1] - ctr[1]) ** 2 + (rest[v * 3 + 2] - ctr[2]) ** 2;
    }
    const order = Array.from(fitIdx.keys()).sort((a, b) => d2[a] - d2[b]).slice(0, K);
    const src = new Float64Array(order.length * 3);
    const dst = new Float64Array(order.length * 3);
    const w = new Float64Array(order.length);
    const dK = Math.sqrt(d2[order[order.length - 1]]);
    order.forEach((j, k) => {
      const v = fitIdx[j];
      for (let a = 0; a < 3; a++) {
        src[k * 3 + a] = rest[v * 3 + a];
        dst[k * 3 + a] = result[v * 3 + a];
      }
      const t = Math.sqrt(d2[j]) / (dK || 1);
      w[k] = (1 - t * t) * (1 - t * t) + 1e-3; // smooth falloff, nearer drivers count more
    });
    let fit;
    try {
      fit = umeyama(src, dst, w, true);
    } catch {
      // degenerate driver set (e.g. collinear): translate by the mean driver displacement
      const t = [0, 0, 0];
      let W = 0;
      for (let k = 0; k < order.length; k++) {
        W += w[k];
        for (let a = 0; a < 3; a++) t[a] += w[k] * (dst[k * 3 + a] - src[k * 3 + a]);
      }
      for (const v of verts) for (let a = 0; a < 3; a++) result[v * 3 + a] = rest[v * 3 + a] + t[a] / W;
      reports.push({ component: c, mode, drivers: order.length, scale: 1, rms: NaN });
      continue;
    }
    const compRest = new Float64Array(verts.length * 3);
    verts.forEach((v, k) => compRest.set(rest.subarray(v * 3, v * 3 + 3), k * 3));
    const moved = transformPositions(compRest, fit.transform);
    verts.forEach((v, k) => result.set(moved.subarray(k * 3, k * 3 + 3), v * 3));
    reports.push({ component: c, mode, drivers: order.length, scale: fit.scale, rms: fit.rms });
  }
  return reports;
}
