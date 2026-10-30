import { describe, expect, it } from 'vitest';
import { boundingBoxAlignment, icpAlign, umeyama } from '../src/engine/alignment/rigid';
import { alignFromLandmarks, Landmark } from '../src/engine/landmarks/landmarks';
import { computeBBox, triangulate } from '../src/engine/core/mesh';
import { mat4Identity, mat4Multiply, transformPositions } from '../src/engine/core/mat3';
import { applyField, cubeSphere, HEAD_FIELD, icosphere } from '../src/engine/synthetic/shapes';
import { TriangleBVH } from '../src/engine/spatial/bvh';
import { rng, similarity, transformed } from './helpers';

function maxDiff(a: ArrayLike<number>, b: ArrayLike<number>) {
  let m = 0;
  for (let i = 0; i < a.length; i++) m = Math.max(m, Math.abs(a[i] - b[i]));
  return m;
}

describe('rigid alignment', () => {
  it('Umeyama recovers a known similarity transform exactly', () => {
    const r = rng(3);
    const src = Float64Array.from({ length: 60 }, () => r() * 2 - 1);
    const T = similarity([1, 2, 0.5], 1.1, 2.5, [3, -1, 7]);
    const dst = transformPositions(src, T);
    const fit = umeyama(src, dst, null, true);
    expect(maxDiff(fit.transform, T)).toBeLessThan(1e-9);
    expect(fit.scale).toBeCloseTo(2.5, 9);
    expect(fit.rms).toBeLessThan(1e-9);
    // rigid mode keeps scale 1
    const R = similarity([0, 1, 0], -0.7, 1, [0.1, 0.2, 0.3]);
    expect(maxDiff(umeyama(src, transformPositions(src, R), null, false).transform, R)).toBeLessThan(1e-9);
  });

  it('Umeyama rejects degenerate (collinear) input with a clear error', () => {
    const line = Float64Array.from([0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3]);
    expect(() => umeyama(line, line, null, true)).toThrow(/collinear/);
    expect(() => umeyama(line.subarray(0, 6), line.subarray(0, 6), null, true)).toThrow(/At least 3/);
  });

  it('bounding-box alignment matches centres and size', () => {
    const base = cubeSphere(6);
    const ref = transformed(icosphere(3), similarity([0, 0, 1], 0, 4, [10, 20, 30]));
    const T = boundingBoxAlignment(base.positions, ref.positions, true);
    const a = computeBBox(transformPositions(base.positions, T));
    const b = computeBBox(ref.positions);
    for (let k = 0; k < 3; k++) expect(a.center[k]).toBeCloseTo(b.center[k], 9);
    expect(a.diagonal).toBeCloseTo(b.diagonal, 9);
  });

  it('ICP recovers a known rigid transform between differently tessellated meshes', () => {
    const shape = HEAD_FIELD;
    const base = applyField(cubeSphere(20), shape);
    const ref0 = applyField(icosphere(5), shape);
    const T = similarity([0.3, 1, 0.2], 0.25, 1, [0.15, -0.1, 0.2]);
    const ref = transformed(ref0, T);
    const bvh = TriangleBVH.build(ref.positions, triangulate(ref).triangles);
    const res = icpAlign(base.positions, mat4Identity(), bvh, { maxIterations: 200, allowScale: false, trimFraction: 0.9 });
    expect(res.rmsAfter).toBeLessThan(res.rmsBefore * 0.05);
    // compare the recovered transform's effect on the base vertices to the ground truth
    const err = maxDiff(transformPositions(base.positions, res.transform), transformPositions(base.positions, T));
    // tessellations differ (facets of the icosphere lie inside the true surface), so allow 2% of the ~2.2 unit size
    expect(err).toBeLessThan(0.045);
  });

  it('ICP recovers a known rigid transform exactly when the meshes share their shape samples', () => {
    const base = applyField(cubeSphere(16), HEAD_FIELD);
    const T = similarity([0.3, 1, 0.2], 0.2, 1, [0.1, -0.1, 0.15]);
    const ref = transformed(base, T);
    const bvh = TriangleBVH.build(ref.positions, triangulate(ref).triangles);
    const res = icpAlign(base.positions, mat4Identity(), bvh, { maxIterations: 300, allowScale: false, trimFraction: 1, sampleCount: 100000, tolerance: 1e-12 });
    expect(maxDiff(transformPositions(base.positions, res.transform), ref.positions)).toBeLessThan(1e-6);
  });

  it('ICP with scale recovers a similarity transform', () => {
    const base = applyField(cubeSphere(16), HEAD_FIELD);
    const ref = transformed(applyField(icosphere(5), HEAD_FIELD), similarity([1, 0, 0], 0.1, 1.3, [1, 2, 3]));
    const bvh = TriangleBVH.build(ref.positions, triangulate(ref).triangles);
    const init = boundingBoxAlignment(base.positions, ref.positions, true);
    const res = icpAlign(base.positions, init, bvh, { maxIterations: 200, allowScale: true, trimFraction: 0.9 });
    expect(res.rmsAfter).toBeLessThan(0.01 * 1.3);
  });

  it('landmark alignment recovers the placement from >= 3 surface-point pairs', () => {
    const base = cubeSphere(8);
    const tris = triangulate(base).triangles;
    const T = similarity([1, 1, 0], 0.6, 0.5, [-2, 0, 1]);
    const ref = transformed(base, T);
    const lms: Landmark[] = [0, 37, 101, 250].map((tri, i) => ({
      id: i + 1,
      label: `L${i}`,
      group: 'face',
      weight: 1,
      base: { tri, bary: [0.2, 0.3, 0.5] },
      ref: { tri, bary: [0.2, 0.3, 0.5] },
    }));
    const fit = alignFromLandmarks(lms, base.positions, tris, ref.positions, tris, true);
    expect(maxDiff(fit.transform, T)).toBeLessThan(1e-9);
    expect(() => alignFromLandmarks(lms.slice(0, 2), base.positions, tris, ref.positions, tris, true)).toThrow(/at least 3/);
  });

  it('matrix helpers compose consistently', () => {
    const A = similarity([0, 1, 0], 0.3, 2, [1, 0, 0]);
    const B = similarity([1, 0, 0], -0.2, 0.5, [0, 3, 0]);
    const p = Float64Array.from([0.3, -0.4, 0.9]);
    const viaProduct = transformPositions(p, mat4Multiply(A, B));
    const viaSteps = transformPositions(transformPositions(p, B), A);
    expect(maxDiff(viaProduct, viaSteps)).toBeLessThan(1e-12);
  });
});

describe('ICP safety', () => {
  it('never returns a placement worse than where it started, even for different shapes', () => {
    // base and reference with different proportions: trimmed ICP can drift; the best transform must be kept
    const base = applyField(cubeSphere(16), { scale: [0.7, 1.4, 0.9], bumps: [] });
    const ref = applyField(icosphere(4), HEAD_FIELD);
    const bvh = TriangleBVH.build(ref.positions, triangulate(ref).triangles);
    for (const trimFraction of [0.5, 0.8, 1]) {
      const res = icpAlign(base.positions, mat4Identity(), bvh, { maxIterations: 40, trimFraction });
      expect(res.rmsAfter).toBeLessThanOrEqual(res.rmsBefore + 1e-12);
    }
  });
});
