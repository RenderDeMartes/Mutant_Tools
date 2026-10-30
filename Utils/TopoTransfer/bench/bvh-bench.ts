/** Closest-point query throughput on near-surface points (as during wrapping). npx tsx bench/bvh-bench.ts */
import { triangulate } from '../src/engine/core/mesh';
import { applyField, HEAD_FIELD, icosphere } from '../src/engine/synthetic/shapes';
import { TriangleBVH, makeHit } from '../src/engine/spatial/bvh';
const ref = applyField(icosphere(7), HEAD_FIELD);
let t = performance.now();
const bvh = TriangleBVH.build(ref.positions, triangulate(ref).triangles);
console.log(`build ${(performance.now() - t).toFixed(0)} ms, ${bvh.nodeCount} nodes`);
// near-surface queries: reference vertices pushed off the surface by up to ±1% of size
let s = 7;
const rnd = () => ((s = (Math.imul(s, 1664525) + 1013904223) >>> 0) / 4294967296 - 0.5) * 0.04;
const n = 100000;
const q = new Float64Array(n * 3);
for (let i = 0; i < n; i++) for (let k = 0; k < 3; k++) q[i * 3 + k] = ref.positions[(i * 1.6 | 0) * 3 + k] + rnd();
const hit = makeHit();
for (let rep = 0; rep < 3; rep++) {
  t = performance.now();
  let acc = 0;
  for (let i = 0; i < n; i++) { bvh.closestPoint(q[i * 3], q[i * 3 + 1], q[i * 3 + 2], 0.35 * 0.35, hit); acc += hit.distSq; }
  console.log(`${n} queries ${(performance.now() - t).toFixed(0)} ms (checksum ${acc.toFixed(6)})`);
}
