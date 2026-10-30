/** Per-stage timing of one wrap. npx tsx bench/profile.ts [vertices] */
import { triangulate } from '../src/engine/core/mesh';
import { applyField, cubeSphere, HEAD_FIELD, icosphere, segmentsForVertexCount } from '../src/engine/synthetic/shapes';
import { prepareBase, prepareReference } from '../src/engine/wrapping/prepare';
import { wrapMesh } from '../src/engine/wrapping/nricp';

const n = Number(process.argv[2] ?? 100000);
const base = cubeSphere(segmentsForVertexCount(n));
const ref = applyField(icosphere(n > 60000 ? 7 : 6), HEAD_FIELD);
const bt = triangulate(base).triangles, rt = triangulate(ref).triangles;
let t = performance.now();
const basePrep = prepareBase(base.positions, bt, true);
console.log(`prepareBase ${(performance.now() - t).toFixed(0)} ms, AMG levels ${basePrep.amg.levelSizes.join('/')}`);
t = performance.now();
const refPrep = prepareReference(ref.positions, rt);
console.log(`prepareReference ${(performance.now() - t).toFixed(0)} ms`);
const res = await wrapMesh({ baseRest: base.positions, baseStart: base.positions, baseTriangles: bt, refPositions: ref.positions, refTriangles: rt }, { basePrep, refPrep });
const d = res.diagnostics!;
const sum: Record<string, number> = {};
for (const it of d.iterations) for (const [k, v] of Object.entries(it.stages)) sum[k] = (sum[k] ?? 0) + v;
const total = d.iterations.reduce((a, b) => a + b.ms, 0);
console.log(`${d.iterations.length} iterations, ${total.toFixed(0)} ms total in loop; analysis ${d.timings.analysisMs.toFixed(0)} ms, setup ${d.timings.setupMs.toFixed(0)} ms`);
for (const [k, v] of Object.entries(sum).sort((a, b) => b[1] - a[1])) console.log(`  ${k.padEnd(16)} ${v.toFixed(0).padStart(7)} ms  ${((100 * v) / total).toFixed(1)}%`);
console.log(`mean distance ${d.distanceBefore.mean.toExponential(2)} -> ${d.distanceAfter.mean.toExponential(2)}`);
