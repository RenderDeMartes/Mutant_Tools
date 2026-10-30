/**
 * Performance benchmark for the wrapping engine.
 *
 *   npm run bench                 # 5k, 25k, 50k, 100k base vertices
 *   npm run bench -- 5000 25000   # custom sizes
 *
 * Base: quad cube-sphere. Reference: differently tessellated icosphere with the
 * stylised head shape applied. Reports wall time per stage, heap/array-buffer
 * memory, fitting error before/after and a topology check. Runs in Node (V8),
 * the same JavaScript engine as Chrome/Edge; browser timings are similar but
 * not identical.
 */

import { writeFileSync, mkdirSync } from 'node:fs';
import { triangulate, topologyHash, hashArrays } from '../src/engine/core/mesh';
import { applyField, cubeSphere, HEAD_FIELD, icosphere, segmentsForVertexCount } from '../src/engine/synthetic/shapes';
import { prepareBase, prepareReference } from '../src/engine/wrapping/prepare';
import { wrapMesh } from '../src/engine/wrapping/nricp';
import { DEFAULT_WRAP_PARAMS } from '../src/engine/wrapping/params';

const sizes = process.argv.slice(2).map(Number).filter((n) => n > 0);
const targets = sizes.length ? sizes : [5000, 25000, 50000, 100000];

function mem() {
  const m = process.memoryUsage();
  return (m.heapUsed + m.arrayBuffers) / 1048576;
}

function refSubdivFor(n: number): number {
  // pick the icosphere level whose vertex count is closest to n
  let best = 3, bd = Infinity;
  for (let k = 3; k <= 8; k++) {
    const v = 10 * 4 ** k + 2;
    const d = Math.abs(Math.log(v / n));
    if (d < bd) { bd = d; best = k; }
  }
  return best;
}

interface Row {
  target: number;
  vertices: number;
  faces: number;
  refVertices: number;
  prepBaseMs: number;
  prepRefMs: number;
  fitMs: number;
  totalMs: number;
  iterations: number;
  meanIterMs: number;
  meanCg: number;
  peakMemMB: number;
  meanBefore: number;
  meanAfter: number;
  maxAfter: number;
  coverageAfter: number;
  flipped: number;
  topologyPreserved: boolean;
  referenceUnchanged: boolean;
}

async function run(target: number): Promise<Row> {
  (globalThis as { gc?: () => void }).gc?.();
  const m0 = mem();
  const base = cubeSphere(segmentsForVertexCount(target));
  const ref = applyField(icosphere(refSubdivFor(target)), HEAD_FIELD);
  const bt = triangulate(base).triangles;
  const rt = triangulate(ref).triangles;
  const topoBefore = topologyHash(base);
  const refHash = hashArrays(ref.positions, ref.faceIndices, ref.faceOffsets);
  let peak = mem() - m0;
  const sample = setInterval(() => (peak = Math.max(peak, mem() - m0)), 20);

  let t = performance.now();
  const basePrep = prepareBase(base.positions, bt, true);
  const prepBaseMs = performance.now() - t;
  t = performance.now();
  const refPrep = prepareReference(ref.positions, rt);
  const prepRefMs = performance.now() - t;
  peak = Math.max(peak, mem() - m0);

  const res = await wrapMesh(
    { baseRest: base.positions, baseStart: base.positions, baseTriangles: bt, refPositions: ref.positions, refTriangles: rt, params: DEFAULT_WRAP_PARAMS },
    { basePrep, refPrep, yieldControl: async () => { peak = Math.max(peak, mem() - m0); } },
  );
  clearInterval(sample);
  peak = Math.max(peak, mem() - m0);
  if (res.status !== 'completed' || !res.diagnostics) throw new Error(res.message);
  const d = res.diagnostics;
  const its = d.iterations;
  return {
    target,
    vertices: base.positions.length / 3,
    faces: base.faceOffsets.length - 1,
    refVertices: ref.positions.length / 3,
    prepBaseMs,
    prepRefMs,
    fitMs: d.timings.fitMs,
    totalMs: prepBaseMs + prepRefMs + d.timings.totalMs,
    iterations: its.length,
    meanIterMs: its.reduce((a, b) => a + b.ms, 0) / its.length,
    meanCg: its.reduce((a, b) => a + b.cgIterations, 0) / its.length,
    peakMemMB: peak,
    meanBefore: d.distanceBefore.mean,
    meanAfter: d.distanceAfter.mean,
    maxAfter: d.distanceAfter.max,
    coverageAfter: d.coverageAfter.mean,
    flipped: d.quality.flippedTriangles,
    topologyPreserved: topologyHash(base) === topoBefore && res.positions.length === base.positions.length,
    referenceUnchanged: hashArrays(ref.positions, ref.faceIndices, ref.faceOffsets) === refHash,
  };
}

const rows: Row[] = [];
for (const n of targets) {
  process.stdout.write(`Running ${n} vertices... `);
  const r = await run(n);
  rows.push(r);
  console.log(`${(r.totalMs / 1000).toFixed(1)} s`);
}

const f = (v: number, d = 1) => v.toFixed(d);
const lines = [
  '| Base verts | Ref verts | Prep base | Prep ref | Fit | Total | Iter (mean) | CG its (mean) | Peak mem | Mean dist before → after | Max after | Coverage after | Flipped | Topology | Ref unchanged |',
  '|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---:|---:|---:|:-:|:-:|',
  ...rows.map(
    (r) =>
      `| ${r.vertices} | ${r.refVertices} | ${f(r.prepBaseMs / 1000, 2)} s | ${f(r.prepRefMs / 1000, 2)} s | ${f(r.fitMs / 1000, 1)} s | ${f(r.totalMs / 1000, 1)} s | ${f(r.meanIterMs, 0)} ms | ${f(r.meanCg, 1)} | ${f(r.peakMemMB, 0)} MB | ${r.meanBefore.toExponential(2)} → ${r.meanAfter.toExponential(2)} | ${r.maxAfter.toExponential(2)} | ${r.coverageAfter.toExponential(2)} | ${r.flipped} | ${r.topologyPreserved ? 'yes' : 'NO'} | ${r.referenceUnchanged ? 'yes' : 'NO'} |`,
  ),
];
console.log('\n' + lines.join('\n'));
console.log(`\nNode ${process.version}, ${process.platform} ${process.arch}. Reference bounding-box diagonal ≈ 3.5 units. Iterations: ${DEFAULT_WRAP_PARAMS.levels} levels × ≤ ${DEFAULT_WRAP_PARAMS.iterationsPerLevel}.`);
mkdirSync('bench/results', { recursive: true });
writeFileSync('bench/results/latest.json', JSON.stringify({ node: process.version, date: new Date().toISOString(), rows }, null, 2));
