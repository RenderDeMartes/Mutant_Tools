import { describe, expect, it } from 'vitest';
import { PolyMesh, triangulate } from '../src/engine/core/mesh';
import { applyField, cubeSphere, HEAD_FIELD, icosphere } from '../src/engine/synthetic/shapes';
import { wrapMesh } from '../src/engine/wrapping/nricp';
import { defaultComponentModes, ComponentMode } from '../src/engine/constraints/components';
import { meanDistance } from './helpers';

/** Head proxy plus a small inner "eyeball" sphere as a second component (like a production head). */
function headWithEye(): { mesh: PolyMesh; eye: number[] } {
  const head = cubeSphere(16);
  const eye = cubeSphere(4);
  const n = head.positions.length / 3;
  const c = [0.3, 0.1, 0.72], r = 0.15;
  const pos = Float64Array.from([...head.positions, ...Array.from(eye.positions, (v, i) => v * r + c[i % 3])]);
  const faceIndices = Uint32Array.from([...head.faceIndices, ...Array.from(eye.faceIndices, (v) => v + n)]);
  const faceOffsets = Uint32Array.from([...head.faceOffsets, ...Array.from(eye.faceOffsets.subarray(1), (o) => o + head.faceIndices.length)]);
  const eyeIdx = Array.from({ length: eye.positions.length / 3 }, (_, k) => n + k);
  return { mesh: { positions: pos, faceOffsets, faceIndices }, eye: eyeIdx };
}

function sphereStats(p: Float64Array, idx: number[]) {
  const c = [0, 0, 0];
  for (const i of idx) for (let k = 0; k < 3; k++) c[k] += p[i * 3 + k] / idx.length;
  const d = idx.map((i) => Math.hypot(p[i * 3] - c[0], p[i * 3 + 1] - c[1], p[i * 3 + 2] - c[2]));
  const mean = d.reduce((a, b) => a + b, 0) / d.length;
  const spread = Math.max(...d) / Math.min(...d);
  return { c, mean, spread };
}

const REF = applyField(icosphere(4), HEAD_FIELD);

describe('multi-component base meshes', () => {
  it('defaults: large parts fit, small parts follow, loose vertices stay fixed', () => {
    expect(defaultComponentModes([10000, 300, 9000, 1])).toEqual(['fit', 'follow', 'fit', 'fixed']);
  });

  it('a following eyeball keeps its shape and moves with the head; fitting it would flatten it onto the skin', async () => {
    const { mesh, eye } = headWithEye();
    const input = (modes: ComponentMode[] | null) => ({
      baseRest: mesh.positions,
      baseStart: mesh.positions,
      baseTriangles: triangulate(mesh).triangles,
      refPositions: REF.positions,
      refTriangles: triangulate(REF).triangles,
      componentModes: modes,
    });
    const restEye = sphereStats(mesh.positions, eye);
    const follow = await wrapMesh(input(['fit', 'follow']));
    expect(follow.status).toBe('completed');
    const fe = sphereStats(follow.positions, eye);
    // shape preserved: still a sphere (same max/min radius ratio as at rest)
    expect(fe.spread).toBeCloseTo(restEye.spread, 6);
    // moved with the surrounding surface (the head grows/shifts around the eye region)
    expect(Math.hypot(fe.c[0] - restEye.c[0], fe.c[1] - restEye.c[1], fe.c[2] - restEye.c[2])).toBeGreaterThan(0.01);
    expect(follow.diagnostics!.components).toHaveLength(1);
    expect(follow.diagnostics!.components[0].mode).toBe('follow');
    // the head itself is still fitted
    const headIdx = (i: number) => i < mesh.positions.length / 3 - eye.length;
    const headPts = follow.positions.filter((_, k) => headIdx(Math.floor(k / 3)));
    expect(meanDistance(headPts, REF)).toBeLessThan(0.01);

    // fitting everything drags eyeball vertices onto the reference skin and distorts the sphere
    const fitAll = await wrapMesh(input(null));
    const ae = sphereStats(fitAll.positions, eye);
    expect(ae.spread).toBeGreaterThan(restEye.spread * 1.05);
    const eyePts = (p: Float64Array) => Float64Array.from(eye.flatMap((i) => [p[i * 3], p[i * 3 + 1], p[i * 3 + 2]]));
    expect(meanDistance(eyePts(fitAll.positions), REF)).toBeLessThan(meanDistance(eyePts(follow.positions), REF) * 0.75);
  });

  it('fixed components keep their aligned rest position exactly; invalid mode lists are rejected', async () => {
    const { mesh, eye } = headWithEye();
    const base = {
      baseRest: mesh.positions,
      baseStart: mesh.positions,
      baseTriangles: triangulate(mesh).triangles,
      refPositions: REF.positions,
      refTriangles: triangulate(REF).triangles,
    };
    const res = await wrapMesh({ ...base, componentModes: ['fit', 'fixed'] });
    for (const i of eye) for (let k = 0; k < 3; k++) expect(res.positions[i * 3 + k]).toBe(mesh.positions[i * 3 + k]);
    expect((await wrapMesh({ ...base, componentModes: ['fit'] })).message).toMatch(/2 components/);
    expect((await wrapMesh({ ...base, componentModes: ['follow', 'follow'] })).message).toMatch(/No component is set to Fit/);
  });
});
