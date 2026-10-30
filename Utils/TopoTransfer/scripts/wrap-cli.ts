/**
 * Wrap without the browser: the same engine and export as the app.
 *
 *   npx tsx scripts/wrap-cli.ts <base.obj> <reference.obj|ply|stl> <out.obj>
 *
 * Auto-aligns the Base to the Reference (bounds, then ICP with uniform scale, so heads of any size
 * work), wraps with the default component modes (largest piece Fit, the rest Follow)
 * and writes the result like the app's Export OBJ (reference coordinates, TopoTransfer header with
 * the alignment). Used to check pipelines end to end (Meta Mutant) and for batch work.
 */

import { readFileSync, writeFileSync } from 'node:fs';
import { basename } from 'node:path';
import { loadMeshFile } from '../src/engine/io/load';
import { triangulate } from '../src/engine/core/mesh';
import { wrapMesh } from '../src/engine/wrapping/nricp';
import { prepareBase, prepareReference } from '../src/engine/wrapping/prepare';
import { defaultComponentModes, labelComponents } from '../src/engine/constraints/components';
import { buildAdjacency } from '../src/engine/geometry/topology';
import { boundingBoxAlignment, icpAlign } from '../src/engine/alignment/rigid';
import { transformPositions } from '../src/engine/core/mat3';
import { TriangleBVH } from '../src/engine/spatial/bvh';
import { exportMesh } from '../src/engine/export/exporter';

const [baseFile, refFile, outFile] = process.argv.slice(2);
if (!baseFile || !refFile || !outFile) {
  console.error('usage: npx tsx scripts/wrap-cli.ts <base.obj> <reference> <out.obj>');
  process.exit(2);
}

const read = (path: string, role: 'base' | 'reference') => {
  const b = readFileSync(path);
  return loadMeshFile(basename(path), b.buffer.slice(b.byteOffset, b.byteOffset + b.byteLength) as ArrayBuffer, role);
};

const base = read(baseFile, 'base');
const ref = read(refFile, 'reference');
const refTris = triangulate(ref.mesh).triangles;
const bvh = TriangleBVH.build(ref.mesh.positions, refTris);
const init = boundingBoxAlignment(base.mesh.positions, ref.mesh.positions, true);
const icp = icpAlign(base.mesh.positions, init, bvh, { allowScale: true, maxIterations: 80 });
const start = transformPositions(base.mesh.positions, icp.transform);
const baseTris = triangulate(base.mesh).triangles;
const comps = labelComponents(buildAdjacency(baseTris, base.mesh.positions.length / 3));

const t0 = performance.now();
const res = await wrapMesh(
  {
    baseRest: start, baseStart: start, baseTriangles: baseTris, refPositions: ref.mesh.positions, refTriangles: refTris,
    componentModes: defaultComponentModes(comps.sizes), landmarks: [], params: {},
  },
  { basePrep: prepareBase(start, baseTris, true), refPrep: prepareReference(ref.mesh.positions, refTris) },
);
if (res.status !== 'completed') {
  console.error(`wrap failed: ${res.message}`);
  process.exit(1);
}
const out = exportMesh({ base, positions: res.positions, transform: icp.transform, format: 'obj', space: 'reference' });
writeFileSync(outFile, Buffer.from(out.data));
const d = res.diagnostics!;
console.log(
  `wrapped ${base.mesh.positions.length / 3} vertices onto ${basename(refFile)} in ${((performance.now() - t0) / 1000).toFixed(1)} s: ` +
    `surface distance mean ${d.distanceBefore.mean.toFixed(3)} -> ${d.distanceAfter.mean.toFixed(3)}, flips ${d.quality.flippedTriangles} -> ${outFile}`,
);
