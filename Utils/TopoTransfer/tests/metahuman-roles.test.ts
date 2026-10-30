import { describe, expect, it } from 'vitest';
import { isMetaHumanExport } from '../src/engine/io/load';

const buf = (s: string) => new TextEncoder().encode(s).buffer as ArrayBuffer;

describe('MetaHuman export detection (drop order independent roles)', () => {
  it('recognises the header written by the Meta Mutant mm_dna.py export', () => {
    expect(isMetaHumanExport(buf('# MetaHuman LOD0 meshes exported from head.dna for TopoTransfer (DNA space, vertex order preserved)\no head_lod0_mesh\nv 0 0 0\n'))).toBe(true);
    expect(isMetaHumanExport(buf('# Exported by TopoTransfer\nv 0 0 0\n'))).toBe(false);
    expect(isMetaHumanExport(buf('v 0 0 0\n# MetaHuman-ish comment later\n'))).toBe(false);
  });
});
