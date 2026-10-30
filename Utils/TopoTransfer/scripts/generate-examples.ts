/**
 * Writes reproducible example / test geometry to ./examples.
 *   npm run examples
 */
import { mkdirSync, writeFileSync } from 'node:fs';
import { writeOBJ } from '../src/engine/io/obj';
import { writePLY } from '../src/engine/io/ply';
import { mat4Identity, transformPositions } from '../src/engine/core/mat3';
import { triangulate, PolyMesh } from '../src/engine/core/mesh';
import { applyField, cropFaces, cubeSphere, HEAD_FIELD, icosphere } from '../src/engine/synthetic/shapes';

mkdirSync('examples', { recursive: true });
const write = (name: string, data: string | ArrayBuffer) => {
  writeFileSync(`examples/${name}`, typeof data === 'string' ? data : Buffer.from(data));
  console.log(`examples/${name}`);
};

// 1. quad base with UVs (spherical projection) so attribute preservation can be checked
const base = cubeSphere(40);
{
  const n = base.positions.length / 3;
  const lines = ['# TopoTransfer example base: quad sphere (9,602 vertices), with UVs', 'o base_head'];
  for (let i = 0; i < n; i++) lines.push(`v ${base.positions[i * 3].toFixed(6)} ${base.positions[i * 3 + 1].toFixed(6)} ${base.positions[i * 3 + 2].toFixed(6)}`);
  for (let i = 0; i < n; i++) {
    const x = base.positions[i * 3], y = base.positions[i * 3 + 1], z = base.positions[i * 3 + 2];
    lines.push(`vt ${(0.5 + Math.atan2(x, z) / (2 * Math.PI)).toFixed(6)} ${(0.5 + Math.asin(Math.max(-1, Math.min(1, y))) / Math.PI).toFixed(6)}`);
  }
  lines.push('g head', 's 1');
  for (let f = 0; f + 1 < base.faceOffsets.length; f++) {
    const c: string[] = [];
    for (let k = base.faceOffsets[f]; k < base.faceOffsets[f + 1]; k++) c.push(`${base.faceIndices[k] + 1}/${base.faceIndices[k] + 1}`);
    lines.push(`f ${c.join(' ')}`);
  }
  write('base_quadsphere.obj', lines.join('\n') + '\n');
}

// 2. stylised head reference in centimetres, rotated and offset (needs alignment)
const head = applyField(icosphere(6), HEAD_FIELD);
const m = mat4Identity();
const a = 0.18;
m[0] = 12 * Math.cos(a); m[2] = -12 * Math.sin(a); m[5] = 12; m[8] = 12 * Math.sin(a); m[10] = 12 * Math.cos(a);
m[12] = 4; m[13] = 160;
const headCm: PolyMesh = { ...head, positions: transformPositions(head.positions, m) };
write('reference_head_cm.obj', writeOBJ(headCm, { header: ['TopoTransfer example reference: stylised head, cm, rotated 10.3 deg about Y, offset (4, 160, 0)'] }));

// 3. partial "scan": same head with the back of the skull missing (open boundary), binary PLY
const partial = cropFaces(head, (_x, _y, z) => z > -0.45);
write('reference_head_partial_scan.ply', writePLY(partial, { header: ['TopoTransfer example: partial scan with open boundary'] }));

// 4. binary STL of the head (reference-only format)
{
  const tris = triangulate(head).triangles;
  const T = tris.length / 3;
  const buf = Buffer.alloc(84 + T * 50);
  buf.write('TopoTransfer example STL', 0);
  buf.writeUInt32LE(T, 80);
  for (let t = 0; t < T; t++) {
    const o = 84 + t * 50;
    for (let c = 0; c < 3; c++) for (let k = 0; k < 3; k++) buf.writeFloatLE(head.positions[tris[t * 3 + c] * 3 + k], o + 12 + c * 12 + k * 4);
  }
  write('reference_head.stl', buf.buffer.slice(buf.byteOffset, buf.byteOffset + buf.byteLength) as ArrayBuffer);
}

// 5. low-poly base for quick experiments
write('base_quadsphere_lowpoly.obj', writeOBJ(cubeSphere(12), { header: ['TopoTransfer example base: quad sphere, 866 vertices'] }));
