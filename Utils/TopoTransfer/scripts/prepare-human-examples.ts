/**
 * Builds the human example files served by the app from Blender Studio's CC0
 * Human Base Meshes (exported to third_party/human-obj, see docs/HUMAN_ASSETS.md).
 *
 *   npx tsx scripts/prepare-human-examples.ts
 *
 * Bases are OBJ (quads + UVs, eyes as separate parts, original vertex order).
 * References are binary PLY (float32) to keep the high-resolution sculpts small.
 */

import { mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { loadMeshFile } from '../src/engine/io/load';

const SRC = 'third_party/human-obj';
const OUT = 'public/examples/human';
mkdirSync(OUT, { recursive: true });

/** Concatenate OBJ files keeping UVs: v/vt indices of later files are offset. */
function concatObj(files: string[], header: string[]): string {
  const out = header.map((h) => `# ${h}`);
  let vOff = 0, tOff = 0;
  for (const f of files) {
    const text = readFileSync(`${SRC}/${f}`, 'utf8');
    let v = 0, t = 0;
    for (const line of text.split('\n')) {
      if (line.startsWith('v ')) { out.push(line); v++; }
      else if (line.startsWith('vt ')) { out.push(line); t++; }
      else if (line.startsWith('o ')) out.push(line);
      else if (line.startsWith('f ')) {
        out.push('f ' + line.slice(2).trim().split(/\s+/).map((c) => {
          const [a, b] = c.split('/');
          return b ? `${+a + vOff}/${+b + tOff}` : `${+a + vOff}`;
        }).join(' '));
      }
    }
    vOff += v;
    tOff += t;
  }
  return out.join('\n') + '\n';
}

function objToPly(file: string, header: string[]): ArrayBuffer {
  const b = readFileSync(`${SRC}/${file}`);
  const m = loadMeshFile(file, b.buffer.slice(b.byteOffset, b.byteOffset + b.byteLength) as ArrayBuffer, 'reference').mesh;
  // float32 positions keep the file small; sub-micrometre precision loss at human scale
  const n = m.positions.length / 3;
  const F = m.faceOffsets.length - 1;
  const head = `ply\nformat binary_little_endian 1.0\n${header.map((h) => `comment ${h}\n`).join('')}element vertex ${n}\nproperty float x\nproperty float y\nproperty float z\nelement face ${F}\nproperty list uchar int vertex_indices\nend_header\n`;
  const hb = new TextEncoder().encode(head);
  const buf = new ArrayBuffer(hb.length + n * 12 + m.faceIndices.length * 4 + F);
  new Uint8Array(buf).set(hb);
  const dv = new DataView(buf);
  let o = hb.length;
  for (let i = 0; i < n * 3; i++, o += 4) dv.setFloat32(o, m.positions[i], true);
  for (let f = 0; f < F; f++) {
    const s = m.faceOffsets[f], e = m.faceOffsets[f + 1];
    dv.setUint8(o++, e - s);
    for (let k = s; k < e; k++, o += 4) dv.setInt32(o, m.faceIndices[k], true);
  }
  return buf;
}

const credit = 'Source: Blender Studio "Human Base Meshes" v1.4.1, CC0 (https://www.blender.org/download/demo/)';
const files: [string, string | ArrayBuffer][] = [
  ['body_male_base.obj', concatObj(['GEO-body_male_realistic.obj', 'GEO-body_male_realistic.eye.L.obj', 'GEO-body_male_realistic.eye.R.obj'], ['TopoTransfer human example base: realistic male body cage + eyes (10,582 + 2x546 vertices), metres, Y up', credit])],
  ['body_female_sculpt_ref.ply', objToPly('GEO-body_female_realistic_mr2.obj', ['TopoTransfer human example reference: realistic female body sculpt, multires level 2', credit])],
  ['head_anim_base.obj', concatObj(['GEO-head_animation_realistic.obj', 'GEO-head_animation_realistic.sclera.L.obj', 'GEO-head_animation_realistic.sclera.R.obj', 'GEO-head_animation_realistic.iris.L.obj', 'GEO-head_animation_realistic.iris.R.obj'], ['TopoTransfer human example base: realistic animation-topology head + sclera/iris', credit])],
  ['head_sculpt_ref.ply', objToPly('GEO-head_sculpting_realistic_mr1.obj', ['TopoTransfer human example reference: realistic sculpting head (different topology), multires level 1', credit])],
  // ground truth for evaluation: female cage shares the male cage's vertex order
  ['body_female_cage_groundtruth.obj', concatObj(['GEO-body_female_realistic.obj'], ['Female body cage: same vertex order as body_male_base.obj body part (evaluation ground truth)', credit])],
];
for (const [name, data] of files) {
  writeFileSync(`${OUT}/${name}`, typeof data === 'string' ? data : Buffer.from(data));
  console.log(`${OUT}/${name}`, typeof data === 'string' ? data.length : data.byteLength, 'bytes');
}
writeFileSync(
  `${OUT}/LICENSE.txt`,
  `These meshes are derived from Blender Studio's "Human Base Meshes" asset bundle v1.4.1,\nreleased under CC0 1.0 Universal (public domain dedication).\nhttps://www.blender.org/download/demo/  —  https://creativecommons.org/publicdomain/zero/1.0/\n\nDerivation: exported with tools/blender_export_meshes.py (Blender 4.2.23 LTS) and\nscripts/prepare-human-examples.ts. Vertex order of each base part is unchanged.\n`,
);
