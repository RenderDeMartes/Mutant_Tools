import { readFileSync } from 'node:fs';
import { describe, expect, it } from 'vitest';
import { loadMeshFile } from '../src/engine/io/load';
import { validateMesh } from '../src/engine/geometry/validation';
import { boundingBoxAlignment, icpAlign } from '../src/engine/alignment/rigid';
import { transformPositions } from '../src/engine/core/mat3';
import { triangulate, topologyHash } from '../src/engine/core/mesh';
import { TriangleBVH } from '../src/engine/spatial/bvh';
import { wrapMesh } from '../src/engine/wrapping/nricp';
import { exportMesh } from '../src/engine/export/exporter';

const file = (name: string) => {
  const b = readFileSync(`examples/${name}`);
  return b.buffer.slice(b.byteOffset, b.byteOffset + b.byteLength) as ArrayBuffer;
};

describe('shipped example files (integration)', () => {
  it('load, validate, align, wrap and export the example scene end to end', async () => {
    const base = loadMeshFile('base_quadsphere_lowpoly.obj', file('base_quadsphere_lowpoly.obj'), 'base');
    const ref = loadMeshFile('reference_head_cm.obj', file('reference_head_cm.obj'), 'reference');
    expect(validateMesh(base.mesh, 'base').ok).toBe(true);
    expect(validateMesh(ref.mesh, 'reference').ok).toBe(true);
    const refTris = triangulate(ref.mesh).triangles;
    const bvh = TriangleBVH.build(ref.mesh.positions, refTris);
    const init = boundingBoxAlignment(base.mesh.positions, ref.mesh.positions, true);
    const icp = icpAlign(base.mesh.positions, init, bvh, { allowScale: true, maxIterations: 60 });
    expect(icp.rmsAfter).toBeLessThan(icp.rmsBefore);
    const rest = transformPositions(base.mesh.positions, icp.transform);
    const topo = topologyHash(base.mesh);
    const res = await wrapMesh({ baseRest: rest, baseStart: rest, baseTriangles: triangulate(base.mesh).triangles, refPositions: ref.mesh.positions, refTriangles: refTris });
    expect(res.status).toBe('completed');
    const d = res.diagnostics!;
    expect(d.distanceAfter.mean).toBeLessThan(d.distanceBefore.mean * 0.1);
    expect(d.quality.flippedTriangles).toBe(0);
    const out = exportMesh({ base, positions: res.positions, transform: icp.transform, format: 'obj', space: 'reference' });
    expect(out.check.ok).toBe(true);
    expect(topologyHash(loadMeshFile('o.obj', out.data, 'base').mesh)).toBe(topo);
  });

  it('wraps onto a partial scan (open boundary) without dragging uncovered parts to the rim', async () => {
    const base = loadMeshFile('base_quadsphere_lowpoly.obj', file('base_quadsphere_lowpoly.obj'), 'base');
    const scan = loadMeshFile('reference_head_partial_scan.ply', file('reference_head_partial_scan.ply'), 'reference');
    const v = validateMesh(scan.mesh, 'reference');
    expect(v.issues.map((i) => i.code)).toContain('open-boundary');
    const rest = base.mesh.positions;
    const res = await wrapMesh({ baseRest: rest, baseStart: rest, baseTriangles: triangulate(base.mesh).triangles, refPositions: scan.mesh.positions, refTriangles: triangulate(scan.mesh).triangles });
    expect(res.status).toBe('completed');
    expect(res.diagnostics!.inlierDistanceAfter.mean).toBeLessThan(res.diagnostics!.distanceBefore.mean * 0.15);
    expect(res.diagnostics!.quality.flippedTriangles).toBe(0);
    expect(res.diagnostics!.quality.collapsedTriangles).toBe(0);
  });

  it('accepts the STL example as a reference only', () => {
    expect(() => loadMeshFile('reference_head.stl', file('reference_head.stl'), 'base')).toThrow(/STL/);
    const s = loadMeshFile('reference_head.stl', file('reference_head.stl'), 'reference');
    expect(s.mesh.positions.length / 3).toBe(40962); // welded back to the icosphere's vertex count
  });
});
