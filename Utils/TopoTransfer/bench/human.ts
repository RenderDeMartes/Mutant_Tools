/**
 * Human-body / face evaluation on Blender Studio's CC0 Human Base Meshes.
 *
 * Uses the CC0 example files in public/examples/human (see docs/HUMANS.md).
 *   npx tsx bench/human.ts [body|head]
 *
 * Case A (body): Base = realistic male body cage (+ eyes, Follow).
 *   Reference = realistic female body sculpt at multires level 2 (~169k vertices).
 *   The female cage has the same vertex order as the male cage, so it is a
 *   ground-truth correspondence: after wrapping, male vertex i should land
 *   where female-cage vertex i is. That measures sliding, not just distance.
 * Case B (face): Base = animation-topology realistic head (+ sclera/iris, Follow).
 *   Reference = sculpting head (different topology) at multires level 1.
 */

import { readFileSync, existsSync } from 'node:fs';
import { loadMeshFile } from '../src/engine/io/load';
import { PolyMesh, triangulate, computeBBox } from '../src/engine/core/mesh';
import { wrapMesh } from '../src/engine/wrapping/nricp';
import { prepareBase, prepareReference } from '../src/engine/wrapping/prepare';
import { defaultComponentModes, labelComponents } from '../src/engine/constraints/components';
import { buildAdjacency } from '../src/engine/geometry/topology';
import type { WrapParams } from '../src/engine/wrapping/params';
import type { Landmark } from '../src/engine/landmarks/landmarks';
import { boundingBoxAlignment, icpAlign } from '../src/engine/alignment/rigid';
import { transformPositions } from '../src/engine/core/mat3';
import { TriangleBVH } from '../src/engine/spatial/bvh';

/** Same rigid pre-alignment an artist would do in the app: Auto (bounds, no scale) then rigid ICP. */
function align(base: PolyMesh, ref: PolyMesh, refTris: Uint32Array, allowScale = false): PolyMesh {
  const bvh = TriangleBVH.build(ref.positions, refTris);
  const init = boundingBoxAlignment(base.positions, ref.positions, allowScale);
  const icp = icpAlign(base.positions, init, bvh, { allowScale, maxIterations: 80 });
  return { ...base, positions: transformPositions(base.positions, icp.transform) };
}

const DIR = 'public/examples/human';
const load = (f: string): PolyMesh => {
  const p = `${DIR}/${f}`;
  if (!existsSync(p)) throw new Error(`${p} missing — run scripts/prepare-human-examples.ts (docs/HUMANS.md)`);
  const b = readFileSync(p);
  return loadMeshFile(f, b.buffer.slice(b.byteOffset, b.byteOffset + b.byteLength) as ArrayBuffer, 'base').mesh;
};

function pct(sorted: Float64Array, q: number) {
  return sorted[Math.min(sorted.length - 1, Math.floor(q * (sorted.length - 1)))];
}

/** Ground-truth vertex landmarks: each base vertex i should go to target vertex i. */
function gtLandmarks(base: PolyMesh, target: PolyMesh, vertices: number[], refTris: Uint32Array, refPos: Float64Array): Landmark[] {
  const tris = triangulate(base).triangles;
  const out: Landmark[] = [];
  // nearest reference triangle corner to the target position (exact enough for evaluation landmarks)
  for (const v of vertices) {
    let tri = -1, corner = 0;
    for (let t = 0; t < tris.length / 3 && tri < 0; t++) for (let c = 0; c < 3; c++) if (tris[t * 3 + c] === v) { tri = t; corner = c; }
    const bary: [number, number, number] = [0, 0, 0];
    bary[corner] = 1;
    let best = -1, bd = Infinity;
    const x = target.positions[v * 3], y = target.positions[v * 3 + 1], z = target.positions[v * 3 + 2];
    for (let i = 0; i < refPos.length / 3; i++) {
      const d = (refPos[i * 3] - x) ** 2 + (refPos[i * 3 + 1] - y) ** 2 + (refPos[i * 3 + 2] - z) ** 2;
      if (d < bd) { bd = d; best = i; }
    }
    let rt = -1, rc = 0;
    for (let t = 0; t < refTris.length / 3 && rt < 0; t++) for (let c = 0; c < 3; c++) if (refTris[t * 3 + c] === best) { rt = t; rc = c; }
    const rb: [number, number, number] = [0, 0, 0];
    rb[rc] = 1;
    out.push({ id: out.length + 1, label: `gt${v}`, group: 'body', weight: 1, base: { tri, bary }, ref: { tri: rt, bary: rb } });
  }
  return out;
}

/** Extreme vertices (fingertips, toes, head top, nose...) as a sparse, artist-like landmark set. */
function extremeVertices(m: PolyMesh, count: number): number[] {
  const n = m.positions.length / 3;
  const dirs: [number, number, number][] = [];
  for (let k = 0; k < count; k++) {
    const t = Math.acos(1 - (2 * (k + 0.5)) / count), p = Math.PI * (1 + Math.sqrt(5)) * k;
    dirs.push([Math.sin(t) * Math.cos(p), Math.cos(t), Math.sin(t) * Math.sin(p)]);
  }
  const c = computeBBox(m.positions).center;
  const out = new Set<number>();
  for (const d of dirs) {
    let best = 0, bv = -Infinity;
    for (let i = 0; i < n; i++) {
      const v = (m.positions[i * 3] - c[0]) * d[0] + (m.positions[i * 3 + 1] - c[1]) * d[1] + (m.positions[i * 3 + 2] - c[2]) * d[2];
      if (v > bv) { bv = v; best = i; }
    }
    out.add(best);
  }
  return [...out];
}

async function bodyCase(label: string, params: Partial<WrapParams>, landmarkCount = 0) {
  const baseFile = load('body_male_base.obj'); // body cage (10,582 v) followed by two eyes
  const femaleCage = load('body_female_cage_groundtruth.obj');
  const ref = load('body_female_sculpt_ref.ply');
  const rt = triangulate(ref).triangles;
  const base = align(baseFile, ref, rt);
  const nBody = femaleCage.positions.length / 3;
  const bt = triangulate(base).triangles;
  const maleAligned = { ...base, positions: base.positions.slice(0, nBody * 3) };
  const comps = labelComponents(buildAdjacency(bt, base.positions.length / 3));
  const modes = defaultComponentModes(comps.sizes);
  const lms = landmarkCount ? gtLandmarks(maleAligned, femaleCage, extremeVertices({ ...baseFile, positions: baseFile.positions.slice(0, nBody * 3) }, landmarkCount), rt, ref.positions) : [];
  const t0 = performance.now();
  const res = await wrapMesh(
    { baseRest: base.positions, baseStart: base.positions, baseTriangles: bt, refPositions: ref.positions, refTriangles: rt, componentModes: modes, landmarks: lms, params },
    { basePrep: prepareBase(base.positions, bt, true), refPrep: prepareReference(ref.positions, rt) },
  );
  const ms = performance.now() - t0;
  if (res.status !== 'completed') throw new Error(res.message);
  const d = res.diagnostics!;
  const err = (p: Float64Array) => {
    const e = new Float64Array(nBody);
    for (let i = 0; i < nBody; i++) e[i] = Math.hypot(p[i * 3] - femaleCage.positions[i * 3], p[i * 3 + 1] - femaleCage.positions[i * 3 + 1], p[i * 3 + 2] - femaleCage.positions[i * 3 + 2]);
    const s = e.slice().sort();
    return { mean: e.reduce((a, b) => a + b, 0) / nBody, p95: pct(s, 0.95), max: s[nBody - 1] };
  };
  const before = err(base.positions), after = err(res.positions);
  const mm = (v: number) => (v * 1000).toFixed(1);
  console.log(
    `${label.padEnd(34)} surface mean ${mm(d.distanceBefore.mean)}→${mm(d.distanceAfter.mean)} mm p95 ${mm(d.distanceAfter.p95)} max ${mm(d.distanceAfter.max)} | ` +
      `GT corr mean ${mm(before.mean)}→${mm(after.mean)} mm p95 ${mm(after.p95)} max ${mm(after.max)} | flips ${d.quality.flippedTriangles} stretch ${d.quality.stretchedEdges} | ${(ms / 1000).toFixed(1)} s`,
  );
  return { res, base };
}

async function headCase(label: string, params: Partial<WrapParams>) {
  const ref = load('head_sculpt_ref.ply');
  const rt = triangulate(ref).triangles;
  const base = align(load('head_anim_base.obj'), ref, rt);
  const bt = triangulate(base).triangles;
  const comps = labelComponents(buildAdjacency(bt, base.positions.length / 3));
  const t0 = performance.now();
  const res = await wrapMesh({ baseRest: base.positions, baseStart: base.positions, baseTriangles: bt, refPositions: ref.positions, refTriangles: rt, componentModes: defaultComponentModes(comps.sizes), params });
  const d = res.diagnostics!;
  const mm = (v: number) => (v * 1000).toFixed(2);
  console.log(
    `${label.padEnd(34)} parts ${comps.sizes.join('/')} surface mean ${mm(d.distanceBefore.mean)}→${mm(d.distanceAfter.mean)} mm p95 ${mm(d.distanceAfter.p95)} max ${mm(d.distanceAfter.max)} | coverage ${mm(d.coverageAfter.mean)} | flips ${d.quality.flippedTriangles} | ${((performance.now() - t0) / 1000).toFixed(1)} s`,
  );
}

const only = process.argv.slice(2);
if (only[0] === 'sweep') {
  const variants: [string, Partial<WrapParams>][] = [
    ['L6 it10', { levels: 6, iterationsPerLevel: 10 }],
    ['L6 it10 mu0.6', { levels: 6, iterationsPerLevel: 10, normalAlignment: 0.6 }],
    ['L8 it10 mu0.6', { levels: 8, iterationsPerLevel: 10, normalAlignment: 0.6 }],
    ['L6 it20 mu0.6', { levels: 6, iterationsPerLevel: 20, normalAlignment: 0.6 }],
    ['L6 it10 mu0.8', { levels: 6, iterationsPerLevel: 10, normalAlignment: 0.8 }],
  ];
  for (const [name, p] of variants) await bodyCase(`sweep: ${name}`, p);
  process.exit(0);
}
const want = (k: string) => !only.length || only.includes(k);
if (want('body')) {
  await bodyCase('body: defaults', {});
  await bodyCase('body: smoothness 0.15', { smoothness: 0.15 });
  await bodyCase('body: 24 sparse landmarks', {}, 24);
}
if (want('head')) {
  await headCase('head: defaults', {});
  await headCase('head: smoothness 0.15', { smoothness: 0.15 });
}
