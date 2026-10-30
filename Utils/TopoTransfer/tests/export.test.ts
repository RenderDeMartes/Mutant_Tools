import { describe, expect, it } from 'vitest';
import { exportMesh } from '../src/engine/export/exporter';
import { loadMeshFile } from '../src/engine/io/load';
import { writeOBJ } from '../src/engine/io/obj';
import { writePLY } from '../src/engine/io/ply';
import { sameTopology, triangulate } from '../src/engine/core/mesh';
import { transformPositions, mat4Identity } from '../src/engine/core/mat3';
import { applyField, cubeSphere, HEAD_FIELD, icosphere } from '../src/engine/synthetic/shapes';
import { wrapMesh } from '../src/engine/wrapping/nricp';
import { similarity } from './helpers';

const enc = (s: string) => new TextEncoder().encode(s).buffer as ArrayBuffer;

/** Base OBJ with per-vertex UVs, per-face-corner normals, groups and a material. */
function richObj(): string {
  const m = cubeSphere(10);
  const n = m.positions.length / 3;
  const lines = ['mtllib skin.mtl', 'o head'];
  for (let i = 0; i < n; i++) lines.push(`v ${m.positions[i * 3]} ${m.positions[i * 3 + 1]} ${m.positions[i * 3 + 2]}`);
  for (let i = 0; i < n; i++) lines.push(`vt ${(i % 17) / 17} ${(i % 13) / 13}`);
  const F = m.faceOffsets.length - 1;
  for (let f = 0; f < F; f++) lines.push('vn 0 0 1');
  lines.push('g skin', 'usemtl skin', 's 1');
  for (let f = 0; f < F; f++) {
    const c: string[] = [];
    for (let k = m.faceOffsets[f]; k < m.faceOffsets[f + 1]; k++) c.push(`${m.faceIndices[k] + 1}/${m.faceIndices[k] + 1}/${f + 1}`);
    lines.push('f ' + c.join(' '));
  }
  return lines.join('\n') + '\n';
}

async function wrapped(base: ReturnType<typeof loadMeshFile>, T: Float64Array) {
  const rest = transformPositions(base.mesh.positions, T);
  const ref = transformed(applyField(icosphere(4), HEAD_FIELD), T);
  const res = await wrapMesh({
    baseRest: rest,
    baseStart: rest,
    baseTriangles: triangulate(base.mesh).triangles,
    refPositions: ref,
    refTriangles: triangulate(applyField(icosphere(4), HEAD_FIELD)).triangles,
    params: { levels: 2, iterationsPerLevel: 3 },
  });
  expect(res.status).toBe('completed');
  return res.positions;
}

function transformed(m: { positions: Float64Array }, T: Float64Array) {
  return transformPositions(m.positions, T);
}

describe('topology-preserving export', () => {
  it('OBJ export of a wrapped mesh re-imports with identical topology and attributes', async () => {
    const text = richObj();
    const base = loadMeshFile('head.obj', enc(text), 'base');
    const T = mat4Identity();
    const pos = await wrapped(base, T);
    const out = exportMesh({ base, positions: pos, transform: T, format: 'obj', space: 'reference' });
    expect(out.check.ok).toBe(true);
    expect(out.fileName).toBe('head_wrapped.obj');
    const re = loadMeshFile(out.fileName, out.data, 'base');
    expect(sameTopology(re.mesh, base.mesh)).toBe(true);
    for (let i = 0; i < pos.length; i++) expect(Math.abs(re.mesh.positions[i] - pos[i])).toBeLessThan(1e-6);
    // every face line, UV line, group and material survives byte-for-byte
    const origLines = text.trim().split('\n');
    const outLines = new TextDecoder().decode(out.data).trim().split('\n').filter((l) => !l.startsWith('#'));
    expect(outLines.length).toBe(origLines.length);
    origLines.forEach((l, i) => {
      if (!l.startsWith('v ') && !l.startsWith('vn ')) expect(outLines[i]).toBe(l);
    });
    expect(out.notes.join(' ')).toMatch(/recomputed/);
  });

  it('exports in original base space by inverting the alignment transform', async () => {
    const base = loadMeshFile('b.obj', enc(writeOBJ(cubeSphere(8))), 'base');
    const T = similarity([0, 1, 0], 0.4, 2.5, [10, -3, 4]);
    const pos = await wrapped(base, T);
    const out = exportMesh({ base, positions: pos, transform: T, format: 'obj', space: 'original' });
    const re = loadMeshFile('x.obj', out.data, 'base');
    const back = transformPositions(re.mesh.positions, T);
    for (let i = 0; i < pos.length; i++) expect(Math.abs(back[i] - pos[i])).toBeLessThan(1e-4);
  });

  it('PLY round-trip keeps every element and property; OBJ→PLY reports what cannot be kept', async () => {
    const m = cubeSphere(8);
    const ply = loadMeshFile('b.ply', writePLY(m, { format: 'binary_little_endian' }), 'base');
    const pos = await wrapped(ply, mat4Identity());
    const out = exportMesh({ base: ply, positions: pos, transform: mat4Identity(), format: 'ply', space: 'reference' });
    const re = loadMeshFile('o.ply', out.data, 'base');
    expect(sameTopology(re.mesh, m)).toBe(true);
    expect(Array.from(re.mesh.positions)).toEqual(Array.from(pos)); // stored as double: exact

    const obj = loadMeshFile('h.obj', enc(richObj()), 'base');
    const out2 = exportMesh({ base: obj, positions: obj.mesh.positions, transform: mat4Identity(), format: 'ply', space: 'reference' });
    expect(out2.notes.join(' ')).toMatch(/UVs, normals, groups and materials/);
    expect(sameTopology(loadMeshFile('o.ply', out2.data, 'base').mesh, obj.mesh)).toBe(true);
  });

  it('refuses to export positions that do not match the base vertex count', () => {
    const base = loadMeshFile('b.obj', enc(writeOBJ(cubeSphere(4))), 'base');
    expect(() => exportMesh({ base, positions: new Float64Array(9), transform: mat4Identity(), format: 'obj', space: 'reference' })).toThrow(/vertex count/);
  });
});

describe('export header', () => {
  it('records the base-to-reference alignment matrix for downstream tools', () => {
    const base = loadMeshFile('b.obj', enc(writeOBJ(cubeSphere(4))), 'base');
    const T = similarity([0, 1, 0], 0.3, 1.5, [1, 2, 3]);
    const out = exportMesh({ base, positions: transformPositions(base.mesh.positions, T), transform: T, format: 'obj', space: 'original' });
    const line = new TextDecoder().decode(out.data).split('\n').find((l) => l.includes('topotransfer-alignment'))!;
    const nums = line.split(/\s+/).slice(-16).map(Number);
    nums.forEach((v, i) => expect(v).toBeCloseTo(T[i], 9));
  });
});
