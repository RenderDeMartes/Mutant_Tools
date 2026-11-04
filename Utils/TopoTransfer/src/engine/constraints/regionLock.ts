/**
 * Keeps touching surfaces apart during the wrap. With the mouth closed, a MetaHuman upper lip vertex
 * can be closest to your lower lip; once it lands there the upper lip opens with the jaw. A region
 * lock forbids exactly that: a Base vertex of one region may land on its own region or on skin that
 * belongs to no region, never on another region.
 *
 * Not "only its own region": a region's Base side comes from skin weights and reaches past the
 * lips, so restricting it would pull the philtrum down onto a tight lip selection.
 */

export interface RegionLock {
  /** Base vertex -> region (0 = none) */
  baseVertex: Uint8Array;
  /** Reference triangle -> region (0 = none): a triangle belongs when all its corners are in the region */
  refTriangle: Uint8Array;
  /** Reference vertex -> region (0 = none) */
  refVertex: Uint8Array;
  /** names, index 0 = region 1 */
  names: string[];
}

export interface RegionLockInput {
  name: string;
  base: number[];
  ref: number[];
}

/** Regions with vertices on both sides become a lock; the rest are reported in `skipped`. */
export function buildRegionLock(regions: RegionLockInput[], baseVertices: number, refVertices: number, refTriangles: Uint32Array): { lock: RegionLock | null; skipped: string[] } {
  const baseVertex = new Uint8Array(baseVertices);
  const refVertex = new Uint8Array(refVertices);
  const refTriangle = new Uint8Array(refTriangles.length / 3);
  const names: string[] = [];
  const skipped: string[] = [];
  for (const r of regions) {
    const member = new Uint8Array(refVertices);
    for (const v of r.ref) if (v >= 0 && v < refVertices) member[v] = 1;
    const picked: number[] = [];
    for (let t = 0; t < refTriangle.length; t++) {
      if (!refTriangle[t] && member[refTriangles[t * 3]] && member[refTriangles[t * 3 + 1]] && member[refTriangles[t * 3 + 2]]) picked.push(t);
    }
    const baseValid = r.base.filter((v) => v >= 0 && v < baseVertices);
    if (!picked.length || !baseValid.length) {
      skipped.push(r.name);
      continue;
    }
    const k = names.length + 1;
    for (const t of picked) refTriangle[t] = k;
    for (const v of baseValid) if (!baseVertex[v]) baseVertex[v] = k;
    for (const v of r.ref) if (v >= 0 && v < refVertices && !refVertex[v]) refVertex[v] = k;
    names.push(r.name);
  }
  return { lock: names.length ? { baseVertex, refTriangle, refVertex, names } : null, skipped };
}

/** The Reference triangles a Base vertex of region `k` may land on: everything but the other regions. */
export function allowedTriangles(lock: RegionLock, k: number, refTriangles: Uint32Array): { triangles: Uint32Array; ids: Uint32Array } {
  const ids: number[] = [];
  for (let t = 0; t < lock.refTriangle.length; t++) if (!lock.refTriangle[t] || lock.refTriangle[t] === k) ids.push(t);
  const triangles = new Uint32Array(ids.length * 3);
  ids.forEach((t, i) => {
    triangles[i * 3] = refTriangles[t * 3];
    triangles[i * 3 + 1] = refTriangles[t * 3 + 1];
    triangles[i * 3 + 2] = refTriangles[t * 3 + 2];
  });
  return { triangles, ids: Uint32Array.from(ids) };
}

/** A Reference point of region `refRegion` may not pull a Base triangle that only belongs to other regions. */
export function reverseAllowed(lock: RegionLock, refRegion: number, a: number, b: number, c: number): boolean {
  if (!refRegion) return true;
  const ra = lock.baseVertex[a], rb = lock.baseVertex[b], rc = lock.baseVertex[c];
  if (ra === refRegion || rb === refRegion || rc === refRegion) return true;
  return !ra && !rb && !rc;
}
