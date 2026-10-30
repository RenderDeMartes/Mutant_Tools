/**
 * Brush (after Fit): touch up the fitted Base by hand.
 *
 *   move    drag the vertices under the brush (on the view plane)
 *   sculpt  push out along the surface normal (Ctrl: push in), for detail
 *   smooth  smooth, then pull back onto the Reference (project smooth)
 *   relax   even out the edges along the surface, then pull back onto the Reference (project relax)
 *
 * A stroke works on one connected part (the one clicked) of the kept result, `committed`, and is
 * one undo step. Mirror repeats it across the Base's symmetry plane.
 */

import { computeBBox } from '../engine/core/mesh';
import { transformPoint } from '../engine/core/mat3';
import { makeHit } from '../engine/spatial/bvh';
import { baseAdjacency, bvhFor, meshComponents, symmetryPlanes } from './actions';
import { baseEntry, baseRestPositions, get, pushUndo, refEntry, set } from './store';

export type SculptMode = 'move' | 'sculpt' | 'smooth' | 'relax';
type V = [number, number, number];

interface Stroke {
  P: Float64Array;
  labels: Int32Array;
  comp: number;
  R: number;
  invert: boolean;
  plane: { p: V; n: V } | null;
  grab?: { idx: number[]; w1: number[]; w2: number[]; start: Float64Array; origin: V };
}

let stroke: Stroke | null = null;

const falloff = (d: number, R: number) => {
  const x = 1 - (d * d) / (R * R);
  return x > 0 ? x * x : 0;
};

/** The Base's symmetry plane, in world space (where the result lives). */
function worldPlane(): { p: V; n: V } | null {
  const planes = symmetryPlanes();
  if (!planes) return null;
  const T = get().transform;
  const { point, normal } = planes.base;
  const p = transformPoint(point, T);
  const q = transformPoint([point[0] + normal[0], point[1] + normal[1], point[2] + normal[2]], T);
  const l = Math.hypot(q[0] - p[0], q[1] - p[1], q[2] - p[2]) || 1;
  return { p, n: [(q[0] - p[0]) / l, (q[1] - p[1]) / l, (q[2] - p[2]) / l] };
}

function reflect(c: V, pl: { p: V; n: V }): V {
  const d = 2 * ((c[0] - pl.p[0]) * pl.n[0] + (c[1] - pl.p[1]) * pl.n[1] + (c[2] - pl.p[2]) * pl.n[2]);
  return [c[0] - d * pl.n[0], c[1] - d * pl.n[1], c[2] - d * pl.n[2]];
}

function reflectDir(v: V, n: V): V {
  const d = 2 * (v[0] * n[0] + v[1] * n[1] + v[2] * n[2]);
  return [v[0] - d * n[0], v[1] - d * n[1], v[2] - d * n[2]];
}

/** Vertices of the stroke's part within the brush around `c`, with their weights. */
function under(st: Stroke, c: V): { idx: number[]; w: number[] } {
  const idx: number[] = [], w: number[] = [];
  const P = st.P;
  for (let i = 0; i < st.labels.length; i++) {
    if (st.labels[i] !== st.comp) continue;
    const dx = P[i * 3] - c[0], dy = P[i * 3 + 1] - c[1], dz = P[i * 3 + 2] - c[2];
    const d2 = dx * dx + dy * dy + dz * dz;
    if (d2 >= st.R * st.R) continue;
    idx.push(i);
    w.push(falloff(Math.sqrt(d2), st.R));
  }
  return { idx, w };
}

/** Area-weighted normals of the given vertices (only the triangles around them are summed). */
function normalsOf(P: Float64Array, tris: Uint32Array, idx: number[]): Map<number, V> {
  const want = new Map<number, V>(idx.map((i) => [i, [0, 0, 0] as V]));
  for (let t = 0; t < tris.length; t += 3) {
    const a = tris[t], b = tris[t + 1], c = tris[t + 2];
    const na = want.get(a), nb = want.get(b), nc = want.get(c);
    if (!na && !nb && !nc) continue;
    const ux = P[b * 3] - P[a * 3], uy = P[b * 3 + 1] - P[a * 3 + 1], uz = P[b * 3 + 2] - P[a * 3 + 2];
    const vx = P[c * 3] - P[a * 3], vy = P[c * 3 + 1] - P[a * 3 + 1], vz = P[c * 3 + 2] - P[a * 3 + 2];
    const n: V = [uy * vz - uz * vy, uz * vx - ux * vz, ux * vy - uy * vx];
    for (const acc of [na, nb, nc]) if (acc) (acc[0] += n[0]), (acc[1] += n[1]), (acc[2] += n[2]);
  }
  for (const n of want.values()) {
    const l = Math.hypot(...n) || 1;
    n[0] /= l, n[1] /= l, n[2] /= l;
  }
  return want;
}

function publish(st: Stroke) {
  set({ committed: st.P, heat: null });
}

/** Start a stroke at a point of the Base surface (`tri`: the clicked triangle). */
export function sculptBegin(center: V, tri: number, invert: boolean) {
  const s = get();
  const b = baseEntry(s);
  if (!b || s.preview || s.job) return;
  const start = s.committed ?? baseRestPositions(s);
  if (!start) return;
  pushUndo('Brush');
  const labels = meshComponents(b).labels;
  const st: Stroke = {
    P: start.slice(),
    labels,
    comp: labels[b.triangles[tri * 3]],
    R: s.sculpt.radius * computeBBox(start).diagonal,
    invert,
    plane: s.sculpt.mirror ? worldPlane() : null,
  };
  stroke = st;
  if (s.sculpt.mode === 'move') {
    const a = under(st, center);
    const w2 = new Map<number, number>();
    if (st.plane) {
      const m = under(st, reflect(center, st.plane));
      m.idx.forEach((i, k) => w2.set(i, m.w[k]));
    }
    const all = [...new Set([...a.idx, ...w2.keys()])];
    const w1 = new Map(a.idx.map((i, k) => [i, a.w[k]]));
    st.grab = { idx: all, w1: all.map((i) => w1.get(i) ?? 0), w2: all.map((i) => w2.get(i) ?? 0), start: st.P.slice(), origin: center };
  } else sculptDab(center);
}

/** Move: the brush followed the mouse to `point` (on the view plane through the grab point). */
export function sculptDrag(point: V) {
  const st = stroke;
  if (!st?.grab) return;
  const g = st.grab;
  const d: V = [point[0] - g.origin[0], point[1] - g.origin[1], point[2] - g.origin[2]];
  const m = st.plane ? reflectDir(d, st.plane.n) : d;
  const P = st.P.slice();
  g.idx.forEach((i, k) => {
    for (let c = 0; c < 3; c++) P[i * 3 + c] = g.start[i * 3 + c] + g.w1[k] * d[c] + g.w2[k] * m[c];
  });
  st.P = P;
  publish(st);
}

/** Sculpt / smooth / relax: one dab of the brush at `center` (and its mirror). */
export function sculptDab(center: V) {
  const st = stroke;
  const s = get();
  const b = baseEntry(s);
  if (!st || !b || s.sculpt.mode === 'move') return;
  const mode = s.sculpt.mode;
  const k = s.sculpt.strength;
  const centers = st.plane ? [center, reflect(center, st.plane)] : [center];
  const P = st.P.slice();
  const adj = baseAdjacency(b);
  const r = refEntry(s);
  const bvh = r ? bvhFor(r) : null;
  const hit = makeHit();
  for (const c of centers) {
    const { idx, w } = under({ ...st, P }, c);
    if (!idx.length) continue;
    const normals = mode === 'smooth' ? null : normalsOf(P, b.triangles, idx);
    const out = new Float64Array(idx.length * 3);
    idx.forEach((i, j) => {
      const p: V = [P[i * 3], P[i * 3 + 1], P[i * 3 + 2]];
      const wk = w[j] * k;
      let q: V;
      if (mode === 'sculpt') {
        const n = normals!.get(i)!;
        const h = wk * st.R * 0.15 * (st.invert ? -1 : 1);
        q = [p[0] + n[0] * h, p[1] + n[1] * h, p[2] + n[2] * h];
      } else {
        const avg: V = [0, 0, 0];
        const s0 = adj.offsets[i], s1 = adj.offsets[i + 1];
        for (let e = s0; e < s1; e++) {
          const nb = adj.neighbors[e];
          avg[0] += P[nb * 3], avg[1] += P[nb * 3 + 1], avg[2] += P[nb * 3 + 2];
        }
        const cnt = Math.max(1, s1 - s0);
        const dl: V = [avg[0] / cnt - p[0], avg[1] / cnt - p[1], avg[2] / cnt - p[2]];
        if (mode === 'relax') {
          // along the surface only: the shape stays, the edges even out
          const n = normals!.get(i)!;
          const dn = dl[0] * n[0] + dl[1] * n[1] + dl[2] * n[2];
          dl[0] -= dn * n[0], dl[1] -= dn * n[1], dl[2] -= dn * n[2];
        }
        q = [p[0] + wk * dl[0], p[1] + wk * dl[1], p[2] + wk * dl[2]];
        // project: back onto the Reference, as much as the brush weight
        if (bvh && bvh.closestPoint(q[0], q[1], q[2], Infinity, hit)) {
          const f = w[j];
          q = [q[0] + f * (hit.x - q[0]), q[1] + f * (hit.y - q[1]), q[2] + f * (hit.z - q[2])];
        }
      }
      out[j * 3] = q[0], out[j * 3 + 1] = q[1], out[j * 3 + 2] = q[2];
    });
    idx.forEach((i, j) => {
      P[i * 3] = out[j * 3], P[i * 3 + 1] = out[j * 3 + 1], P[i * 3 + 2] = out[j * 3 + 2];
    });
  }
  st.P = P;
  publish(st);
}

export function sculptEnd() {
  stroke = null;
}

export function sculpting(): boolean {
  return stroke !== null;
}
