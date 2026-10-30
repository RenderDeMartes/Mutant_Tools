/** Parameter sweep on the example scene (used to choose defaults). npx tsx bench/sweep.ts */
import { triangulate } from '../src/engine/core/mesh';
import { applyField, cubeSphere, HEAD_FIELD, icosphere } from '../src/engine/synthetic/shapes';
import { prepareBase, prepareReference } from '../src/engine/wrapping/prepare';
import { wrapMesh } from '../src/engine/wrapping/nricp';
import type { WrapParams } from '../src/engine/wrapping/params';

const base = cubeSphere(40);
const ref = applyField(icosphere(6), HEAD_FIELD);
const bt = triangulate(base).triangles;
const rt = triangulate(ref).triangles;
const basePrep = prepareBase(base.positions, bt, true);
const refPrep = prepareReference(ref.positions, rt);

const variants: Partial<WrapParams>[] = [
  {},
  { smoothness: 0.25 },
  { smoothness: 0.15 },
  { iterationsPerLevel: 10 },
  { smoothness: 0.25, iterationsPerLevel: 10 },
  { normalAlignment: 0 },
  { bidirectional: false },
  { allowLocalScaling: false },
  { levels: 5, smoothness: 0.25 },
];
for (const v of variants) {
  const t = performance.now();
  const r = await wrapMesh({ baseRest: base.positions, baseStart: base.positions, baseTriangles: bt, refPositions: ref.positions, refTriangles: rt, params: v }, { basePrep, refPrep });
  const d = r.diagnostics!;
  console.log(
    JSON.stringify(v).padEnd(48),
    `mean ${d.distanceAfter.mean.toExponential(2)} p95 ${d.distanceAfter.p95.toExponential(2)} max ${d.distanceAfter.max.toExponential(2)} cov ${d.coverageAfter.mean.toExponential(2)} covMax ${d.coverageAfter.max.toExponential(2)}`,
    `flip ${d.quality.flippedTriangles} edge ${d.quality.minEdgeRatio.toFixed(2)}-${d.quality.maxEdgeRatio.toFixed(2)} ${((performance.now() - t) / 1000).toFixed(1)}s`,
  );
}
