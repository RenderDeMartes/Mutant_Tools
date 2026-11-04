/**
 * Guides prepared in Maya (Meta Mutant's Pick Points window, `?guides=<url>`): named points and dense
 * lip / eyelid line points, each a MetaHuman vertex paired with a position on your head, plus the
 * face regions that keep the wrap from crossing (see constraints/regionLock.ts).
 *
 * The Reference side comes as positions, not vertex ids, so it stays right when eyes and teeth
 * were cut out of the exported Reference.
 */

import { makeHit, TriangleBVH } from '../spatial/bvh';
import type { Landmark, LandmarkGroup, SurfacePoint } from './landmarks';
import { LANDMARK_GROUPS } from './landmarks';

export interface MayaGuidePoint {
  label: string;
  group: LandmarkGroup;
  weight: number;
  base_vertex: number;
  ref: [number, number, number];
}

export interface MayaGuides {
  version: number;
  landmarks: MayaGuidePoint[];
  /** region name -> MetaHuman vertices and Reference vertices (OBJ order) */
  regions: Record<string, { base: number[]; ref: number[] }>;
}

export function parseMayaGuides(json: unknown): MayaGuides {
  const d = json as Partial<MayaGuides> | null;
  if (!d || typeof d !== 'object' || !Array.isArray(d.landmarks)) throw new Error('not a guides file from Meta Mutant');
  const landmarks = d.landmarks.map((p, i) => {
    const ok = p && typeof p.label === 'string' && Number.isInteger(p.base_vertex) && p.base_vertex >= 0 && Array.isArray(p.ref) && p.ref.length === 3 && p.ref.every(Number.isFinite);
    if (!ok) throw new Error(`guide ${i} is not valid`);
    const group: LandmarkGroup = (LANDMARK_GROUPS as readonly string[]).includes(p.group) ? p.group : 'other';
    return { label: p.label, group, weight: Number.isFinite(p.weight) && p.weight > 0 ? p.weight : 1, base_vertex: p.base_vertex, ref: p.ref };
  });
  return { version: d.version ?? 1, landmarks, regions: d.regions && typeof d.regions === 'object' ? d.regions : {} };
}

/** A vertex as a surface point: one triangle using it, with all the weight on that corner. */
export function vertexSurfacePoints(triangles: Uint32Array, vertexCount: number): (v: number) => SurfacePoint | null {
  const corner = new Int32Array(vertexCount).fill(-1);
  for (let c = 0; c < triangles.length; c++) if (corner[triangles[c]] < 0) corner[triangles[c]] = c;
  return (v) => {
    if (v < 0 || v >= vertexCount || corner[v] < 0) return null;
    const bary: [number, number, number] = [0, 0, 0];
    bary[corner[v] % 3] = 1;
    return { tri: Math.floor(corner[v] / 3), bary };
  };
}

export interface BuiltGuides {
  landmarks: Landmark[];
  skipped: string[];
}

/** The guides as complete landmarks; a point whose MetaHuman vertex is not on the Base is skipped and reported. */
export function buildMayaLandmarks(guides: MayaGuides, firstId: number, baseTriangles: Uint32Array, baseVertices: number, refBvh: TriangleBVH): BuiltGuides {
  const atVertex = vertexSurfacePoints(baseTriangles, baseVertices);
  const hit = makeHit();
  const landmarks: Landmark[] = [];
  const skipped: string[] = [];
  let id = firstId;
  for (const p of guides.landmarks) {
    const base = atVertex(p.base_vertex);
    hit.distSq = Infinity;
    if (!base || !refBvh.closestPoint(p.ref[0], p.ref[1], p.ref[2], Infinity, hit)) {
      skipped.push(p.label);
      continue;
    }
    landmarks.push({ id: id++, label: p.label, group: p.group, weight: p.weight, base, ref: { tri: hit.tri, bary: [hit.u, hit.v, hit.w] } });
  }
  return { landmarks, skipped };
}
