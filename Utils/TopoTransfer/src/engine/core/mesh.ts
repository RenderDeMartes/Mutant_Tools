/**
 * Core mesh representation. Polygon connectivity is stored exactly as imported
 * (faceOffsets / faceIndices) and is never modified by any engine operation;
 * only `positions` of a copy may change.
 */

export interface PolyMesh {
  /** Interleaved xyz, length 3 * vertexCount. */
  positions: Float64Array;
  /** Polygon start offsets into `faceIndices`, length faceCount + 1. */
  faceOffsets: Uint32Array;
  /** Concatenated polygon vertex indices. */
  faceIndices: Uint32Array;
}

export interface Triangulation {
  /** Triangle vertex indices, length 3 * triangleCount. */
  triangles: Uint32Array;
  /** Source polygon of each triangle. */
  triFace: Uint32Array;
}

export interface BBox {
  min: [number, number, number];
  max: [number, number, number];
  size: [number, number, number];
  center: [number, number, number];
  diagonal: number;
}

export function vertexCount(mesh: PolyMesh): number {
  return mesh.positions.length / 3;
}

export function faceCount(mesh: PolyMesh): number {
  return mesh.faceOffsets.length - 1;
}

/**
 * Fan triangulation of every polygon (polygons with < 3 corners produce no
 * triangles). Deterministic, so a (triangle, barycentric) surface point is a
 * stable reference into the base mesh.
 */
export function triangulate(mesh: PolyMesh): Triangulation {
  const { faceOffsets, faceIndices } = mesh;
  const F = faceOffsets.length - 1;
  let T = 0;
  for (let f = 0; f < F; f++) {
    const k = faceOffsets[f + 1] - faceOffsets[f];
    if (k >= 3) T += k - 2;
  }
  const triangles = new Uint32Array(T * 3);
  const triFace = new Uint32Array(T);
  let t = 0;
  for (let f = 0; f < F; f++) {
    const s = faceOffsets[f];
    const k = faceOffsets[f + 1] - s;
    for (let j = 1; j + 1 < k; j++) {
      triangles[t * 3] = faceIndices[s];
      triangles[t * 3 + 1] = faceIndices[s + j];
      triangles[t * 3 + 2] = faceIndices[s + j + 1];
      triFace[t] = f;
      t++;
    }
  }
  return { triangles, triFace };
}

export function computeBBox(positions: ArrayLike<number>): BBox {
  const min: [number, number, number] = [Infinity, Infinity, Infinity];
  const max: [number, number, number] = [-Infinity, -Infinity, -Infinity];
  for (let i = 0; i < positions.length; i += 3) {
    for (let k = 0; k < 3; k++) {
      const v = positions[i + k];
      if (v < min[k]) min[k] = v;
      if (v > max[k]) max[k] = v;
    }
  }
  if (positions.length === 0) {
    return { min: [0, 0, 0], max: [0, 0, 0], size: [0, 0, 0], center: [0, 0, 0], diagonal: 0 };
  }
  const size: [number, number, number] = [max[0] - min[0], max[1] - min[1], max[2] - min[2]];
  const center: [number, number, number] = [(min[0] + max[0]) / 2, (min[1] + max[1]) / 2, (min[2] + max[2]) / 2];
  return { min, max, size, center, diagonal: Math.hypot(size[0], size[1], size[2]) };
}

export function cloneMesh(mesh: PolyMesh): PolyMesh {
  return {
    positions: mesh.positions.slice(),
    faceOffsets: mesh.faceOffsets.slice(),
    faceIndices: mesh.faceIndices.slice(),
  };
}

/** Build a PolyMesh from simple arrays (convenience for tests / generators). */
export function polyMeshFromArrays(positions: ArrayLike<number>, faces: ArrayLike<number>[]): PolyMesh {
  const faceOffsets = new Uint32Array(faces.length + 1);
  let total = 0;
  for (let f = 0; f < faces.length; f++) {
    faceOffsets[f] = total;
    total += faces[f].length;
  }
  faceOffsets[faces.length] = total;
  const faceIndices = new Uint32Array(total);
  let o = 0;
  for (const f of faces) for (let k = 0; k < f.length; k++) faceIndices[o++] = f[k];
  return { positions: Float64Array.from(positions), faceOffsets, faceIndices };
}

/** 32-bit FNV-1a hash over the raw bytes of typed arrays (used to prove data was not modified). */
export function hashArrays(...arrays: ArrayBufferView[]): string {
  let h = 0x811c9dc5;
  for (const a of arrays) {
    const bytes = new Uint8Array(a.buffer, a.byteOffset, a.byteLength);
    for (let i = 0; i < bytes.length; i++) {
      h ^= bytes[i];
      h = Math.imul(h, 0x01000193);
    }
  }
  return (h >>> 0).toString(16).padStart(8, '0');
}

/** Hash of connectivity only (faceOffsets + faceIndices). */
export function topologyHash(mesh: PolyMesh): string {
  return hashArrays(mesh.faceOffsets, mesh.faceIndices);
}

/** Exact equality of connectivity and vertex count. */
export function sameTopology(a: PolyMesh, b: PolyMesh): boolean {
  if (a.positions.length !== b.positions.length) return false;
  if (a.faceOffsets.length !== b.faceOffsets.length) return false;
  if (a.faceIndices.length !== b.faceIndices.length) return false;
  for (let i = 0; i < a.faceOffsets.length; i++) if (a.faceOffsets[i] !== b.faceOffsets[i]) return false;
  for (let i = 0; i < a.faceIndices.length; i++) if (a.faceIndices[i] !== b.faceIndices[i]) return false;
  return true;
}
