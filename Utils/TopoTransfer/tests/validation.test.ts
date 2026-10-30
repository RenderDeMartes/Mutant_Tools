import { describe, expect, it } from 'vitest';
import { validateMesh } from '../src/engine/geometry/validation';
import { polyMeshFromArrays } from '../src/engine/core/mesh';
import { cubeSphere } from '../src/engine/synthetic/shapes';

const codes = (r: ReturnType<typeof validateMesh>) => r.issues.map((i) => i.code);

describe('mesh validation', () => {
  it('a clean closed quad mesh has no warnings or errors', () => {
    const r = validateMesh(cubeSphere(8), 'base');
    expect(r.ok).toBe(true);
    expect(r.issues.filter((i) => i.severity !== 'info')).toEqual([]);
    expect(r.stats.closed).toBe(true);
    expect(r.stats.polygonSizes['4']).toBe(6 * 64);
    expect(r.stats.components).toBe(1);
    expect(r.stats.volume).toBeGreaterThan(0);
  });

  it('detects degenerate faces, duplicates, unreferenced vertices and open boundaries', () => {
    const m = polyMeshFromArrays(
      [0, 0, 0, 1, 0, 0, 0, 1, 0, 2, 0, 0, 1, 0, 0, 5, 5, 5],
      [
        [0, 1, 2],
        [0, 1, 3], // collinear -> zero area
        [0, 0, 2], // repeated vertex
        [4, 2, 3], // uses vertex 4, which duplicates vertex 1
      ],
    );
    const r = validateMesh(m, 'base');
    const c = codes(r);
    expect(c).toContain('degenerate-faces');
    expect(r.issues.find((i) => i.code === 'degenerate-faces')!.count).toBe(2);
    expect(c).toContain('duplicate-vertices');
    expect(c).toContain('unreferenced-vertices');
    expect(r.issues.find((i) => i.code === 'unreferenced-vertices')!.samples).toEqual([5]);
    expect(c).toContain('open-boundary');
  });

  it('detects non-manifold edges and vertices', () => {
    // three triangles sharing edge 0-1
    const fan = polyMeshFromArrays([0, 0, 0, 1, 0, 0, 0, 1, 0, 0, -1, 0, 0, 0, 1], [[0, 1, 2], [1, 0, 3], [0, 1, 4]]);
    expect(codes(validateMesh(fan, 'base'))).toContain('non-manifold-edges');
    // two triangles touching at a single vertex (bow-tie)
    const bow = polyMeshFromArrays([0, 0, 0, 1, 0, 0, 1, 1, 0, -1, 0, 0, -1, -1, 0], [[0, 1, 2], [0, 3, 4]]);
    const r = validateMesh(bow, 'base');
    expect(codes(r)).toContain('non-manifold-vertices');
    expect(r.issues.find((i) => i.code === 'non-manifold-vertices')!.samples).toEqual([0]);
  });

  it('detects inconsistent orientation, inside-out meshes and multiple components', () => {
    const cube = cubeSphere(2);
    const flipped = { ...cube, faceIndices: cube.faceIndices.slice() };
    // reverse the first face only -> inconsistent
    const s = flipped.faceOffsets[0], e = flipped.faceOffsets[1];
    flipped.faceIndices.subarray(s, e).reverse();
    expect(codes(validateMesh(flipped, 'reference'))).toContain('inconsistent-orientation');
    // reverse all faces -> inside out
    const inside = { ...cube, faceIndices: cube.faceIndices.slice() };
    for (let f = 0; f + 1 < inside.faceOffsets.length; f++) inside.faceIndices.subarray(inside.faceOffsets[f], inside.faceOffsets[f + 1]).reverse();
    expect(codes(validateMesh(inside, 'base'))).toContain('inside-out');
    // two separate spheres
    const a = cubeSphere(3);
    const n = a.positions.length / 3;
    const two = {
      positions: Float64Array.from([...a.positions, ...a.positions.map((v, i) => (i % 3 === 0 ? v + 5 : v))]),
      faceOffsets: Uint32Array.from([...a.faceOffsets, ...Array.from(a.faceOffsets.subarray(1)).map((o) => o + a.faceIndices.length)]),
      faceIndices: Uint32Array.from([...a.faceIndices, ...Array.from(a.faceIndices).map((i) => i + n)]),
    };
    const r = validateMesh(two, 'base');
    expect(codes(r)).toContain('components');
    expect(r.stats.components).toBe(2);
  });

  it('returns errors (not exceptions) for NaN coordinates, bad indices and zero-size meshes', () => {
    const nan = polyMeshFromArrays([0, 0, 0, NaN, 0, 0, 0, 1, 0], [[0, 1, 2]]);
    const r1 = validateMesh(nan, 'base');
    expect(r1.ok).toBe(false);
    expect(codes(r1)).toContain('nan-coordinates');
    const bad = polyMeshFromArrays([0, 0, 0, 1, 0, 0, 0, 1, 0], [[0, 1, 7]]);
    const r2 = validateMesh(bad, 'base');
    expect(r2.ok).toBe(false);
    expect(r2.issues[0].message).toMatch(/do not exist/);
    const zero = polyMeshFromArrays([1, 1, 1, 1, 1, 1, 1, 1, 1], [[0, 1, 2]]);
    expect(codes(validateMesh(zero, 'base'))).toContain('zero-size');
  });
});
