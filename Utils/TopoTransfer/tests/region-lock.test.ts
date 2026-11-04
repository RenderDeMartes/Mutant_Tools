import { describe, expect, it } from 'vitest';
import { allowedTriangles, buildRegionLock, reverseAllowed } from '../src/engine/constraints/regionLock';
import { buildMayaLandmarks, parseMayaGuides, vertexSurfacePoints } from '../src/engine/landmarks/mayaGuides';
import { TriangleBVH } from '../src/engine/spatial/bvh';
import { wrapMesh } from '../src/engine/wrapping/nricp';

/** A flat square at height `y`, `k` quads a side, appended to the arrays. */
function plate(pos: number[], tris: number[], y: number, k: number) {
  const first = pos.length / 3;
  for (let j = 0; j <= k; j++) for (let i = 0; i <= k; i++) pos.push(i / k - 0.5, y, j / k - 0.5);
  for (let j = 0; j < k; j++) {
    for (let i = 0; i < k; i++) {
      const a = first + j * (k + 1) + i, b = a + 1, c = a + k + 1, d = c + 1;
      tris.push(a, c, b, b, c, d);
    }
  }
  return { first, count: (k + 1) * (k + 1) };
}

/** Two lips: on the Reference the lower lip is what the Base's upper lip is closest to. */
function lips() {
  const k = 8;
  const bp: number[] = [], bt: number[] = [];
  const bUp = plate(bp, bt, 0.05, k);
  const bLo = plate(bp, bt, -0.05, k);
  const rp: number[] = [], rt: number[] = [];
  const rUp = plate(rp, rt, 0.3, k);
  const rLo = plate(rp, rt, 0, k);
  const ids = (p: { first: number; count: number }) => Array.from({ length: p.count }, (_, i) => p.first + i);
  return {
    base: Float64Array.from(bp), baseTris: Uint32Array.from(bt),
    ref: Float64Array.from(rp), refTris: Uint32Array.from(rt),
    regions: [
      { name: 'upper_lip', base: ids(bUp), ref: ids(rUp) },
      { name: 'lower_lip', base: ids(bLo), ref: ids(rLo) },
    ],
    upper: bUp,
  };
}

const meanY = (p: Float64Array, first: number, count: number) => {
  let s = 0;
  for (let i = 0; i < count; i++) s += p[(first + i) * 3 + 1];
  return s / count;
};

describe('region lock', () => {
  it('a triangle belongs to a region only with all its corners in it', () => {
    const tris = Uint32Array.from([0, 1, 2, 1, 2, 3]);
    const { lock } = buildRegionLock([{ name: 'a', base: [0], ref: [0, 1, 2] }], 4, 4, tris);
    expect(Array.from(lock!.refTriangle)).toEqual([1, 0]);
  });

  it('skips a region with nothing on one side', () => {
    const tris = Uint32Array.from([0, 1, 2]);
    const { lock, skipped } = buildRegionLock([{ name: 'a', base: [], ref: [0, 1, 2] }, { name: 'b', base: [0], ref: [0] }], 3, 3, tris);
    expect(lock).toBeNull();
    expect(skipped).toEqual(['a', 'b']);
  });

  it('region vertices search their own region and free skin, not other regions', () => {
    const tris = Uint32Array.from([0, 1, 2, 3, 4, 5, 6, 7, 8]);
    const { lock } = buildRegionLock([{ name: 'a', base: [0], ref: [0, 1, 2] }, { name: 'b', base: [1], ref: [3, 4, 5] }], 3, 9, tris);
    expect(Array.from(allowedTriangles(lock!, 1, tris).ids)).toEqual([0, 2]);
    expect(Array.from(allowedTriangles(lock!, 2, tris).ids)).toEqual([1, 2]);
  });

  it('reverse pull: not onto a triangle that only belongs to another region', () => {
    const tris = Uint32Array.from([0, 1, 2]);
    const { lock } = buildRegionLock([{ name: 'a', base: [0], ref: [0, 1, 2] }], 4, 3, tris);
    expect(reverseAllowed(lock!, 0, 1, 2, 3)).toBe(true);
    expect(reverseAllowed(lock!, 1, 0, 1, 2)).toBe(true);
    expect(reverseAllowed(lock!, 1, 1, 2, 3)).toBe(true); // free skin
    expect(reverseAllowed({ ...lock!, baseVertex: Uint8Array.from([2, 2, 2, 0]) }, 1, 0, 1, 2)).toBe(false); // only another region
  });

  it('without a lock the upper lip lands on the lower lip; with it, on the upper lip', async () => {
    const m = lips();
    const params = { maxCorrespondenceDistance: 0.5 } as never;
    const run = (regionLock: never | null) =>
      wrapMesh({ baseRest: m.base, baseStart: m.base, baseTriangles: m.baseTris, refPositions: m.ref, refTriangles: m.refTris, regionLock, params }, {});
    const free = await run(null);
    expect(free.status).toBe('completed');
    expect(meanY(free.positions!, m.upper.first, m.upper.count)).toBeLessThan(0.15);
    const { lock } = buildRegionLock(m.regions, m.base.length / 3, m.ref.length / 3, m.refTris);
    const locked = await run(lock as never);
    expect(locked.status).toBe('completed');
    expect(meanY(locked.positions!, m.upper.first, m.upper.count)).toBeGreaterThan(0.2);
  });
});

describe('guides from Maya', () => {
  it('rejects anything else', () => {
    expect(() => parseMayaGuides({})).toThrow();
    expect(() => parseMayaGuides({ landmarks: [{ label: 'x', base_vertex: -1, ref: [0, 0, 0] }] })).toThrow();
    expect(() => parseMayaGuides({ landmarks: [{ label: 'x', base_vertex: 0, ref: [0, 0] }] })).toThrow();
  });

  it('a vertex becomes a surface point exactly on it', () => {
    const at = vertexSurfacePoints(Uint32Array.from([0, 1, 2, 2, 1, 3]), 5);
    expect(at(3)).toEqual({ tri: 1, bary: [0, 0, 1] });
    expect(at(4)).toBeNull(); // on no face
    expect(at(9)).toBeNull();
  });

  it('pairs each MetaHuman vertex with the closest point of the Reference, and reports the rest', () => {
    const baseTris = Uint32Array.from([0, 1, 2]);
    const refPos = Float64Array.from([0, 0, 0, 1, 0, 0, 0, 1, 0]);
    const refTris = Uint32Array.from([0, 1, 2]);
    const guides = parseMayaGuides({
      landmarks: [
        { label: 'Nose tip', group: 'nose', weight: 1, base_vertex: 1, ref: [1, 0, 0] },
        { label: 'Line 1', group: 'lines', weight: 0.2, base_vertex: 2, ref: [0.25, 0.25, 0] },
        { label: 'Gone', group: 'nope', weight: 1, base_vertex: 99, ref: [0, 0, 0] },
      ],
    });
    const { landmarks, skipped } = buildMayaLandmarks(guides, 5, baseTris, 3, TriangleBVH.build(refPos, refTris));
    expect(landmarks.map((l) => l.id)).toEqual([5, 6]);
    expect(landmarks[0].ref!.bary[1]).toBeCloseTo(1);
    expect(landmarks[1].weight).toBe(0.2);
    expect(skipped).toEqual(['Gone']);
  });
});
