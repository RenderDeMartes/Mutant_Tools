import { describe, expect, it } from 'vitest';
import { loadMeshFile } from '../src/engine/io/load';
import { parseOBJ, writeOBJ, writeOBJRoundTrip } from '../src/engine/io/obj';
import { parsePLY, writePLY, writePLYRoundTrip } from '../src/engine/io/ply';
import { parseSTL } from '../src/engine/io/stl';
import { cubeSphere, icosphere } from '../src/engine/synthetic/shapes';
import { sameTopology } from '../src/engine/core/mesh';

const enc = (s: string) => new TextEncoder().encode(s).buffer as ArrayBuffer;

const QUAD_OBJ = `# test
mtllib mat.mtl
o box
v 0 0 0
v 1 0 0
v 1 1 0
v 0 1 0 0.5 0.5 0.5
v 0 0 1
v 1 0 1
vt 0 0
vt 1 0
vt 1 1
vt 0 1
vn 0 0 -1
vn 0 0 1
g front
usemtl red
s 1
f 1/1/1 4/4/1 3/3/1 2/2/1
f -2/1/2 -1/2/2 2/3/2 1/4/2
l 1 5
`;

describe('mesh import', () => {
  it('loads a base OBJ and a reference PLY successfully', () => {
    const base = cubeSphere(6);
    const ref = icosphere(2);
    const a = loadMeshFile('base.obj', enc(writeOBJ(base)), 'base');
    const b = loadMeshFile('ref.ply', writePLY(ref), 'reference');
    expect(a.mesh.positions.length / 3).toBe(base.positions.length / 3);
    expect(sameTopology(a.mesh, base)).toBe(true);
    expect(b.mesh.positions.length / 3).toBe(ref.positions.length / 3);
    expect(sameTopology(b.mesh, ref)).toBe(true);
    for (let i = 0; i < ref.positions.length; i++) expect(b.mesh.positions[i]).toBeCloseTo(ref.positions[i], 12);
  });

  it('parses polygons, negative indices, uv/normal indices and passthrough records', () => {
    const r = parseOBJ(QUAD_OBJ);
    expect(r.mesh.positions.length).toBe(18);
    expect(Array.from(r.mesh.faceOffsets)).toEqual([0, 4, 8]);
    expect(Array.from(r.mesh.faceIndices)).toEqual([0, 3, 2, 1, 4, 5, 1, 0]);
    expect(r.source.uvCount).toBe(4);
    expect(r.source.normalCount).toBe(2);
    expect(Array.from(r.source.cornerNormal)).toEqual([0, 0, 0, 0, 1, 1, 1, 1]);
    expect(r.source.vertexExtraCount).toBe(1);
    expect(r.source.lineElements).toBe(1);
  });

  it('OBJ round-trip keeps every non-position record byte-identical', () => {
    const r = parseOBJ(QUAD_OBJ);
    const moved = { ...r.mesh, positions: r.mesh.positions.map((v) => v + 0.25) };
    const out = writeOBJRoundTrip(moved, r.source, { recomputeNormals: true });
    const inLines = QUAD_OBJ.trim().split('\n');
    const outLines = out.trim().split('\n');
    expect(outLines.length).toBe(inLines.length);
    inLines.forEach((line, i) => {
      if (line.startsWith('v ') || line.startsWith('vn ')) return;
      expect(outLines[i]).toBe(line);
    });
    // vertex colour tokens survive
    expect(outLines[6].endsWith('0.5 0.5 0.5')).toBe(true);
    const re = parseOBJ(out);
    expect(sameTopology(re.mesh, r.mesh)).toBe(true);
    for (let i = 0; i < moved.positions.length; i++) expect(re.mesh.positions[i]).toBeCloseTo(moved.positions[i], 6);
  });

  it('PLY ascii and binary (both endians) round-trip with extra properties', () => {
    const ascii = `ply
format ascii 1.0
comment hello
element vertex 4
property float x
property float y
property float z
property uchar red
property uchar green
property uchar blue
element face 2
property list uchar int vertex_indices
property uchar flags
end_header
0 0 0 255 0 0
1 0 0 0 255 0
1 1 0 0 0 255
0 1 0 9 9 9
3 0 1 2 7
3 0 2 3 8
`;
    const a = parsePLY(enc(ascii));
    expect(Array.from(a.mesh.faceIndices)).toEqual([0, 1, 2, 0, 2, 3]);
    for (const fmt of ['ascii', 'binary_little_endian', 'binary_big_endian'] as const) {
      const moved = { ...a.mesh, positions: a.mesh.positions.map((v) => v * 2) };
      const buf = writePLYRoundTrip(moved, a.source, { format: fmt });
      const b = parsePLY(buf);
      expect(b.source.format).toBe(fmt);
      expect(sameTopology(b.mesh, a.mesh)).toBe(true);
      expect(Array.from(b.mesh.positions)).toEqual(Array.from(moved.positions));
      const ve = b.source.elements[b.source.vertexElement];
      const red = ve.scalars[ve.properties.findIndex((p) => p.name === 'red')]!;
      expect(Array.from(red)).toEqual([255, 0, 0, 9]);
      const fe = b.source.elements[b.source.faceElement];
      expect(Array.from(fe.scalars[fe.properties.findIndex((p) => p.name === 'flags')]!)).toEqual([7, 8]);
      expect(b.source.comments).toContain('hello');
    }
  });

  it('STL is welded and accepted as reference but rejected as base with an explanation', () => {
    const tri = 'solid t\nfacet normal 0 0 1\nouter loop\nvertex 0 0 0\nvertex 1 0 0\nvertex 0 1 0\nendloop\nendfacet\nfacet normal 0 0 1\nouter loop\nvertex 1 0 0\nvertex 1 1 0\nvertex 0 1 0\nendloop\nendfacet\nendsolid t\n';
    const r = parseSTL(enc(tri));
    expect(r.mesh.positions.length / 3).toBe(4);
    expect(r.mesh.faceOffsets.length - 1).toBe(2);
    expect(() => loadMeshFile('scan.stl', enc(tri), 'base')).toThrow(/topology cannot be preserved/);
    expect(loadMeshFile('scan.stl', enc(tri), 'reference').mesh.positions.length).toBe(12);
    // binary STL
    const bin = new ArrayBuffer(84 + 50);
    const dv = new DataView(bin);
    dv.setUint32(80, 1, true);
    [0, 0, 1, 0, 0, 0, 2, 0, 0, 0, 2, 0].forEach((v, i) => dv.setFloat32(84 + i * 4, v, true));
    expect(parseSTL(bin).mesh.positions.length).toBe(9);
  });

  it('reports useful errors for invalid input', () => {
    expect(() => parseOBJ('v 0 0 0\nv 1 0 0\nf 1 2 3\n')).toThrow(/vertex 3 which is not defined/);
    expect(() => parseOBJ('v 0 nan 0\n')).toThrow(/Invalid vertex coordinate/);
    expect(() => parseOBJ('# nothing\n')).toThrow(/no vertices/);
    expect(() => parseOBJ('v 0 0 0\nf 1 1\n')).toThrow(/at least 3 corners/);
    expect(() => parsePLY(enc('ply\nformat ascii 1.0\nelement vertex 1\nproperty float x\n'))).toThrow(/end_header/);
    expect(() =>
      parsePLY(enc('ply\nformat ascii 1.0\nelement vertex 1\nproperty float x\nproperty float y\nproperty float z\nelement face 1\nproperty list uchar int vertex_indices\nend_header\n0 0 0\n3 0 1 2\n')),
    ).toThrow(/references vertex 1/);
    expect(() => loadMeshFile('a.fbx', enc('xyz'), 'base')).toThrow(/Unsupported file type/);
    expect(() => loadMeshFile('pts.obj', enc('v 0 0 0\nv 1 0 0\n'), 'base')).toThrow(/no polygons/);
  });
});
