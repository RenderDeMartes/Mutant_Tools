import { describe, expect, it } from 'vitest';
import { hashArrays, PolyMesh, topologyHash, triangulate } from '../src/engine/core/mesh';
import { applyField, cropFaces, cubeSphere, evalField, HEAD_FIELD, icosphere, nearestVertex, ShapeField } from '../src/engine/synthetic/shapes';
import { wrapMesh, WrapInput } from '../src/engine/wrapping/nricp';
import { TriangleBVH, makeHit } from '../src/engine/spatial/bvh';
import type { Landmark } from '../src/engine/landmarks/landmarks';
import type { WrapParams } from '../src/engine/wrapping/params';
import { dist, meanDistance } from './helpers';

function setup(base: PolyMesh, ref: PolyMesh, params: Partial<WrapParams> = {}, extra: Partial<WrapInput> = {}): WrapInput {
  return {
    baseRest: base.positions,
    baseStart: base.positions,
    baseTriangles: triangulate(base).triangles,
    refPositions: ref.positions,
    refTriangles: triangulate(ref).triangles,
    params,
    ...extra,
  };
}

const BASE = cubeSphere(16); // 1,538 vertices, quads
const REF = applyField(icosphere(4), HEAD_FIELD); // 2,562 vertices, triangles

describe('non-rigid wrapping', () => {
  it('deforms the base toward a differently tessellated reference (measured independently)', async () => {
    const before = meanDistance(BASE.positions, REF);
    const res = await wrapMesh(setup(BASE, REF));
    expect(res.status).toBe('completed');
    const after = meanDistance(res.positions, REF);
    expect(after).toBeLessThan(before * 0.05);
    // the engine's own measurement agrees with the independent one
    expect(res.diagnostics!.distanceAfter.mean).toBeCloseTo(after, 9);
    // the reference is covered too (no partial fit)
    expect(res.diagnostics!.coverageAfter.mean).toBeLessThan(res.diagnostics!.coverageBefore.mean * 0.1);
    expect(res.diagnostics!.quality.flippedTriangles).toBe(0);
    expect(res.diagnostics!.quality.collapsedTriangles).toBe(0);
  });

  it('never changes base connectivity or vertex count, and never modifies the reference', async () => {
    const base = cubeSphere(12);
    const ref = applyField(icosphere(4), HEAD_FIELD);
    const input = setup(base, ref);
    const topo = topologyHash(base);
    const triHash = hashArrays(input.baseTriangles);
    const restHash = hashArrays(input.baseRest);
    const refHash = hashArrays(ref.positions, ref.faceOffsets, ref.faceIndices, input.refTriangles);
    const res = await wrapMesh(input);
    expect(res.status).toBe('completed');
    expect(res.positions.length).toBe(base.positions.length);
    expect(res.positions).not.toBe(input.baseStart);
    expect(topologyHash(base)).toBe(topo);
    expect(hashArrays(input.baseTriangles)).toBe(triHash);
    expect(hashArrays(input.baseRest)).toBe(restHash);
    expect(hashArrays(ref.positions, ref.faceOffsets, ref.faceIndices, input.refTriangles)).toBe(refHash);
  });

  it('smoothness produces measurable differences in fit and distortion', async () => {
    const flexible = await wrapMesh(setup(BASE, REF, { smoothness: 0.05 }));
    const stiff = await wrapMesh(setup(BASE, REF, { smoothness: 0.95 }));
    const ef = flexible.diagnostics!.distanceAfter.mean;
    const es = stiff.diagnostics!.distanceAfter.mean;
    expect(es).toBeGreaterThan(ef * 3);
    // stiffer result stays closer to the rigid rest shape (less edge distortion)
    const spread = (q: { minEdgeRatio: number; maxEdgeRatio: number }) => q.maxEdgeRatio / q.minEdgeRatio;
    expect(spread(stiff.diagnostics!.quality)).toBeLessThan(spread(flexible.diagnostics!.quality));
    // and the solutions really differ
    let maxDelta = 0;
    for (let i = 0; i < flexible.positions.length; i++) maxDelta = Math.max(maxDelta, Math.abs(flexible.positions[i] - stiff.positions[i]));
    expect(maxDelta).toBeGreaterThan(0.01);
  });

  it('landmarks move a feature to its intended location where closest points would not', async () => {
    // shared features pin the global orientation; only the "nose" differs in position
    const noseAt = (dir: [number, number, number]): ShapeField => ({
      scale: [1, 1, 1],
      bumps: [
        { dir, amplitude: 0.35, width: 0.25 },
        { dir: [0, 1, 0], amplitude: 0.3, width: 0.35 },
        { dir: [-0.7, -0.3, -0.7], amplitude: 0.3, width: 0.35 },
        { dir: [0.2, -1, 0.1], amplitude: 0.25, width: 0.3 },
      ],
    });
    const a = (40 * Math.PI) / 180;
    const refDir: [number, number, number] = [Math.sin(a), 0, Math.cos(a)];
    const base = applyField(cubeSphere(20), noseAt([0, 0, 1]));
    const ref = applyField(icosphere(5), noseAt(refDir));
    const baseTip = nearestVertex(base, 0, 0, 2);
    const refTip = evalField(noseAt(refDir), ...refDir);
    const baseTris = triangulate(base).triangles;
    const refTris = triangulate(ref).triangles;
    // landmark surface points: a triangle that uses the tip vertex, and the closest reference point to the true tip
    let tri = -1, corner = 0;
    for (let t = 0; t < baseTris.length / 3 && tri < 0; t++) for (let c = 0; c < 3; c++) if (baseTris[t * 3 + c] === baseTip) { tri = t; corner = c; }
    const bary: [number, number, number] = [0, 0, 0];
    bary[corner] = 1;
    const hit = makeHit();
    TriangleBVH.build(ref.positions, refTris).closestPoint(refTip[0], refTip[1], refTip[2], Infinity, hit);
    const lm: Landmark = { id: 1, label: 'nose', group: 'nose', weight: 1, base: { tri, bary }, ref: { tri: hit.tri, bary: [hit.u, hit.v, hit.w] } };

    const without = await wrapMesh(setup(base, ref));
    const withLm = await wrapMesh(setup(base, ref, {}, { landmarks: [lm] }));
    const eWithout = dist(without.positions, baseTip, refTip);
    const eWith = dist(withLm.positions, baseTip, refTip);
    expect(withLm.diagnostics!.landmarksUsed).toBe(1);
    expect(eWithout).toBeGreaterThan(0.1);
    expect(eWith).toBeLessThan(eWithout * 0.25);
    expect(eWith).toBeLessThan(0.05);
    // landmarks do not degrade the overall surface fit
    expect(withLm.diagnostics!.distanceAfter.mean).toBeLessThan(withLm.diagnostics!.distanceBefore.mean * 0.3);
  });

  it('protected regions stay in place; fit-only mode fits just the painted region', async () => {
    const n = BASE.positions.length / 3;
    const top = new Float32Array(n);
    for (let i = 0; i < n; i++) top[i] = BASE.positions[i * 3 + 1] > 0.3 ? 1 : 0;
    const moved = (res: Float64Array, sel: (i: number) => boolean) => {
      let m = 0, c = 0, s = 0;
      for (let i = 0; i < n; i++) {
        if (!sel(i)) continue;
        const d = Math.hypot(res[i * 3] - BASE.positions[i * 3], res[i * 3 + 1] - BASE.positions[i * 3 + 1], res[i * 3 + 2] - BASE.positions[i * 3 + 2]);
        m = Math.max(m, d);
        s += d;
        c++;
      }
      return { max: m, mean: s / c };
    };
    const free = await wrapMesh(setup(BASE, REF));
    const prot = await wrapMesh(setup(BASE, REF, { maskMode: 'protect', regionInfluence: 1 }, { mask: top }));
    const isTop = (i: number) => top[i] === 1;
    const freeTop = moved(free.positions, isTop);
    const protTop = moved(prot.positions, isTop);
    expect(freeTop.mean).toBeGreaterThan(0.05);
    expect(protTop.mean).toBeLessThan(freeTop.mean * 0.05);
    // unprotected part is still fitted
    const bottomFit = meanDistance(prot.positions.filter((_, k) => !isTop(Math.floor(k / 3))), REF);
    expect(bottomFit).toBeLessThan(meanDistance(BASE.positions, REF) * 0.2);

    const fitOnly = await wrapMesh(setup(BASE, REF, { maskMode: 'fitOnly', regionInfluence: 1 }, { mask: top }));
    const foTop = moved(fitOnly.positions, isTop);
    const foBottom = moved(fitOnly.positions, (i) => !isTop(i) && BASE.positions[i * 3 + 1] < 0);
    expect(foTop.mean).toBeGreaterThan(foBottom.mean * 10);
  });

  it('rejects correspondences on reference holes so the base is not dragged onto the rim', async () => {
    const base = cubeSphere(16);
    const full = applyField(icosphere(4), { scale: [1.15, 1.15, 1.15], bumps: [] });
    const holed = cropFaces(full, (_x, _y, z) => z < 0.55);
    const n = base.positions.length / 3;
    const front = (i: number) => base.positions[i * 3 + 2] > 0.85;
    const frontMove = (p: Float64Array) => {
      let s = 0, c = 0;
      for (let i = 0; i < n; i++) if (front(i)) {
        s += Math.hypot(p[i * 3] - base.positions[i * 3], p[i * 3 + 1] - base.positions[i * 3 + 1], p[i * 3 + 2] - base.positions[i * 3 + 2]);
        c++;
      }
      return s / c;
    };
    const rej = await wrapMesh(setup(base, holed, { rejectBoundary: true, maxCorrespondenceDistance: 0.5 }));
    const naive = await wrapMesh(setup(base, holed, { rejectBoundary: false, maxCorrespondenceDistance: 0.5 }));
    // with rejection the uncovered cap follows the stiffness (≈ 15% radial growth), not the rim
    expect(frontMove(rej.positions)).toBeLessThan(frontMove(naive.positions) * 0.75);
    expect(rej.diagnostics!.quality.flippedTriangles).toBe(0);
  });

  it('improves the fit for several synthetic references with known shape', async () => {
    const fields: ShapeField[] = [
      { scale: [1.3, 0.8, 1], bumps: [] },
      { scale: [1, 1, 1], bumps: [{ dir: [1, 1, 0], amplitude: 0.25, width: 0.4 }, { dir: [-1, 0, -1], amplitude: -0.2, width: 0.5 }] },
      HEAD_FIELD,
    ];
    for (const f of fields) {
      const ref = applyField(icosphere(4), f);
      const res = await wrapMesh(setup(BASE, ref));
      const d = res.diagnostics!;
      expect(d.distanceAfter.mean).toBeLessThan(d.distanceBefore.mean * 0.1);
      expect(d.distanceAfter.p95).toBeLessThan(d.distanceBefore.p95 * 0.15);
      expect(d.quality.flippedTriangles).toBe(0);
      // every solve converged
      for (const it of d.iterations) expect(it.cgResidual).toBeLessThan(1e-3);
    }
  });

  it('seam lock keeps coincident but unconnected vertices together', async () => {
    // split the sphere into two halves that share no vertices (like a UV seam)
    const src = cubeSphere(12);
    const n = src.positions.length / 3;
    const positions = Array.from(src.positions);
    const remap = new Map<number, number>();
    const faceIndices = Array.from(src.faceIndices);
    for (let f = 0; f + 1 < src.faceOffsets.length; f++) {
      let cx = 0;
      for (let k = src.faceOffsets[f]; k < src.faceOffsets[f + 1]; k++) cx += src.positions[src.faceIndices[k] * 3];
      if (cx <= 0) continue;
      for (let k = src.faceOffsets[f]; k < src.faceOffsets[f + 1]; k++) {
        const v = src.faceIndices[k];
        if (Math.abs(src.positions[v * 3]) > 1e-9) continue; // only vertices on the x = 0 seam
        if (!remap.has(v)) {
          remap.set(v, positions.length / 3);
          positions.push(src.positions[v * 3], src.positions[v * 3 + 1], src.positions[v * 3 + 2]);
        }
        faceIndices[k] = remap.get(v)!;
      }
    }
    expect(remap.size).toBeGreaterThan(10);
    const split: PolyMesh = { positions: Float64Array.from(positions), faceOffsets: src.faceOffsets, faceIndices: Uint32Array.from(faceIndices) };
    const gap = (p: Float64Array) => {
      let m = 0;
      for (const [a, b] of remap) m = Math.max(m, Math.hypot(p[a * 3] - p[b * 3], p[a * 3 + 1] - p[b * 3 + 1], p[a * 3 + 2] - p[b * 3 + 2]));
      return m;
    };
    const locked = await wrapMesh(setup(split, REF, { seamLock: true }));
    const unlocked = await wrapMesh(setup(split, REF, { seamLock: false }));
    expect(locked.diagnostics!.seamPairs).toBe(remap.size);
    expect(gap(locked.positions)).toBeLessThan(2e-3);
    expect(gap(unlocked.positions)).toBeGreaterThan(gap(locked.positions) * 3);
    expect(n).toBeLessThan(split.positions.length / 3);
  });

  it('can be cancelled and then returns the untouched start positions', async () => {
    let calls = 0;
    const input = setup(BASE, REF);
    const res = await wrapMesh(input, { onProgress: (p) => { if (p.stage === 'fitting') calls++; }, isCancelled: () => calls >= 2 });
    expect(res.status).toBe('cancelled');
    expect(Array.from(res.positions)).toEqual(Array.from(input.baseStart));
    expect(res.diagnostics).toBeNull();
  });

  it('reports invalid input and poor overlap with useful messages instead of crashing', async () => {
    const bad = applyField(icosphere(2), HEAD_FIELD);
    bad.positions[5] = NaN;
    expect((await wrapMesh(setup(BASE, bad))).message).toMatch(/reference positions contain NaN/);
    const r2 = await wrapMesh({ ...setup(BASE, REF), baseStart: BASE.positions.subarray(0, 30) });
    expect(r2.status).toBe('failed');
    expect(r2.message).toMatch(/different lengths/);
    const r3 = await wrapMesh(setup(BASE, REF, {}, { mask: new Float32Array(3) }));
    expect(r3.message).toMatch(/mask size/);
    const r4 = await wrapMesh({ ...setup(BASE, REF), refTriangles: new Uint32Array(0) });
    expect(r4.message).toMatch(/no faces/);
    // reference far away: nothing within the correspondence radius
    const far = { ...REF, positions: REF.positions.map((v, i) => (i % 3 === 0 ? v + 50 : v)) };
    const r5 = await wrapMesh(setup(BASE, far, { levels: 1, iterationsPerLevel: 2 }));
    expect(r5.status).toBe('completed');
    expect(r5.diagnostics!.warnings.join(' ')).toMatch(/Check the alignment/);
    // and the base did not move to an unreliable place
    let maxMove = 0;
    for (let i = 0; i < BASE.positions.length; i++) maxMove = Math.max(maxMove, Math.abs(r5.positions[i] - BASE.positions[i]));
    expect(maxMove).toBeLessThan(1e-6);
  });

  it('wrapping again from a committed result keeps improving or holds steady', async () => {
    const first = await wrapMesh(setup(BASE, REF, { levels: 2, iterationsPerLevel: 3 }));
    const second = await wrapMesh({ ...setup(BASE, REF, { levels: 2, iterationsPerLevel: 3 }), baseStart: first.positions });
    expect(second.diagnostics!.distanceAfter.mean).toBeLessThanOrEqual(first.diagnostics!.distanceAfter.mean * 1.05);
  });
});
