import { describe, expect, it } from 'vitest';
import { FACE_PRESET, BODY_PRESET, mirrorName } from '../src/engine/landmarks/presets';
import { defaultSymmetryPlane, fitSymmetryPlane, mirrorSurfacePoint, reflect } from '../src/engine/landmarks/mirror';
import { evalSurfacePoint } from '../src/engine/landmarks/landmarks';
import { triangulate } from '../src/engine/core/mesh';
import { applyField, cubeSphere, HEAD_FIELD } from '../src/engine/synthetic/shapes';
import { TriangleBVH } from '../src/engine/spatial/bvh';
import { transformPositions } from '../src/engine/core/mat3';
import { similarity } from './helpers';

describe('landmark presets and mirroring', () => {
  it('presets have unique names and every L/R point has its counterpart', () => {
    for (const preset of [FACE_PRESET, BODY_PRESET]) {
      const names = preset.map((p) => p.name);
      expect(new Set(names).size).toBe(names.length);
      for (const n of names) {
        const m = mirrorName(n);
        if (m) expect(names).toContain(m);
      }
    }
    expect(mirrorName('Ear top L')).toBe('Ear top R');
    expect(mirrorName('Nose tip')).toBeNull();
  });

  it('fits the symmetry plane of a rotated, offset symmetric head and mirrors points onto their twins', () => {
    const head = applyField(cubeSphere(16), HEAD_FIELD); // symmetric about x = 0
    const tris = triangulate(head).triangles;
    // move it into "scan space": rotated 20° about Y and offset — the plane is no longer x = const
    const T = similarity([0, 1, 0], 0.35, 1, [3, 1, -2]);
    const moved = transformPositions(head.positions, T);
    const bvh = TriangleBVH.build(moved, tris);
    const plane = fitSymmetryPlane(moved, bvh, defaultSymmetryPlane(moved), 12);
    // true plane normal is the rotated x axis
    const trueN = [T[0], T[1], T[2]];
    const dot = Math.abs(plane.normal[0] * trueN[0] + plane.normal[1] * trueN[1] + plane.normal[2] * trueN[2]);
    expect(dot).toBeGreaterThan(0.999);
    // mirror a point on the right ear region and compare with the exact mirror image
    const sp = { tri: 123, bary: [0.2, 0.3, 0.5] as [number, number, number] };
    const m = mirrorSurfacePoint(moved, tris, bvh, sp, plane);
    const p = evalSurfacePoint(moved, tris, sp);
    const exact = reflect(p, { point: [3, 1, -2], normal: [trueN[0], trueN[1], trueN[2]] });
    const q = evalSurfacePoint(moved, tris, m);
    expect(Math.hypot(q[0] - exact[0], q[1] - exact[1], q[2] - exact[2])).toBeLessThan(0.01);
  });
});
