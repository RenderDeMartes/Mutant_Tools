/**
 * File-format interop between Meta Mutant (Utils/MetaMutant, Python) and the TopoTransfer
 * engine: Python exports a MetaHuman-style OBJ + manifest from a fake DNA,
 * TopoTransfer loads it as Base and exports a moved result with its alignment
 * header, Python calibrates and the recorded DNACalib commands are checked.
 * Skipped when no Python 3 interpreter is available.
 */
import { spawnSync } from 'node:child_process';
import { mkdtempSync, readFileSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join, resolve } from 'node:path';
import { describe, expect, it } from 'vitest';
import { loadMeshFile } from '../src/engine/io/load';
import { exportMesh } from '../src/engine/export/exporter';
import { transformPositions } from '../src/engine/core/mat3';
import { similarity } from './helpers';

const py = ['python', 'python3'].find((c) => spawnSync(c, ['--version']).status === 0);
const root = resolve(__dirname, '..');

function runPy(code: string) {
  const r = spawnSync(py!, ['-c', code], { cwd: root, encoding: 'utf8' });
  if (r.status !== 0) throw new Error(r.stderr);
  return r.stdout;
}

describe.skipIf(!py)('MetaHuman tools interop', () => {
  it('python export -> TopoTransfer -> python calibrate keeps vertex mapping and DNA space', () => {
    const dir = mkdtempSync(join(tmpdir(), 'tt-mh-'));
    const obj = join(dir, 'mh.obj').replace(/\\/g, '/');
    const prelude = `import sys; sys.path[:0]=['../MetaMutant','../MetaMutant/tests']\nimport mm_dna, mm_core, json\nfrom test_meta_mutant import FakeReader, FakeDnac\n`;
    runPy(prelude + `print(mm_dna.export_obj('fake.dna', r'${obj}', reader=FakeReader()))`);
    const buf = readFileSync(obj);
    const base = loadMeshFile('mh.obj', buf.buffer.slice(buf.byteOffset, buf.byteOffset + buf.byteLength) as ArrayBuffer, 'base');
    expect(base.mesh.positions.length / 3).toBe(7);
    // "wrap": move every vertex +0.5 z in base (DNA) space, then place in reference space with a similarity
    const T = similarity([0, 1, 0], 0.4, 1.3, [5, 1, -2]);
    const moved = base.mesh.positions.map((v, i) => (i % 3 === 2 ? v + 0.5 : v));
    for (const space of ['reference', 'original'] as const) {
      const out = exportMesh({ base, positions: transformPositions(moved, T), transform: T, format: 'obj', space });
      const wrapped = join(dir, `wrapped_${space}.obj`).replace(/\\/g, '/');
      writeFileSync(wrapped, Buffer.from(out.data));
      const res = runPy(
        prelude +
          `FakeDnac.log=[]\nmm_dna.calibrate('fake.dna', r'${obj.replace('.obj', '.manifest.json')}', r'${wrapped}', '', reader=FakeReader(), dnac_module=FakeDnac)\n` +
          `print(json.dumps([c[2] for c in FakeDnac.log if c[0]=='positions']))`,
      );
      const meshes: number[][][] = JSON.parse(res.trim().split('\n').pop()!);
      expect(meshes).toHaveLength(2);
      for (const m of meshes) for (const d of m) {
        expect(d[0]).toBeCloseTo(0, 4);
        expect(d[1]).toBeCloseTo(0, 4);
        expect(d[2]).toBeCloseTo(0.5, 4);
      }
    }
  });
});
