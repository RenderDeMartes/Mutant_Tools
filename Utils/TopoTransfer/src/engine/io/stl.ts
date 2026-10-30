/**
 * STL import (binary and ascii). STL stores an unindexed triangle soup, so
 * vertices are welded by exact position. Because welding defines the
 * connectivity, STL is accepted for the Reference mesh only.
 */

import type { PolyMesh } from '../core/mesh';
import { MeshParseError, ParseResult } from './obj';

export interface StlSource {
  kind: 'stl';
  binary: boolean;
  soupVertices: number;
}

export function parseSTL(buffer: ArrayBuffer): ParseResult<StlSource> {
  const bytes = new Uint8Array(buffer);
  let tris: Float64Array;
  let binary = false;
  if (bytes.length >= 84) {
    const count = new DataView(buffer).getUint32(80, true);
    if (84 + count * 50 === bytes.length) binary = true;
  }
  if (binary) {
    const dv = new DataView(buffer);
    const count = dv.getUint32(80, true);
    tris = new Float64Array(count * 9);
    for (let t = 0; t < count; t++) {
      const o = 84 + t * 50 + 12;
      for (let k = 0; k < 9; k++) tris[t * 9 + k] = dv.getFloat32(o + k * 4, true);
    }
  } else {
    const text = new TextDecoder().decode(bytes);
    if (!/^\s*solid/.test(text)) throw new MeshParseError('Not a valid STL file');
    const vals: number[] = [];
    const re = /vertex\s+(\S+)\s+(\S+)\s+(\S+)/g;
    let m: RegExpExecArray | null;
    while ((m = re.exec(text))) vals.push(+m[1], +m[2], +m[3]);
    if (vals.length % 9 !== 0) throw new MeshParseError('ASCII STL has an incomplete facet');
    tris = Float64Array.from(vals);
  }
  for (let i = 0; i < tris.length; i++) if (!Number.isFinite(tris[i])) throw new MeshParseError('STL contains non-finite coordinates');
  const T = tris.length / 9;
  if (T === 0) throw new MeshParseError('STL file contains no triangles');
  // weld identical positions
  const map = new Map<string, number>();
  const pos: number[] = [];
  const idx = new Uint32Array(T * 3);
  for (let c = 0; c < T * 3; c++) {
    const x = tris[c * 3], y = tris[c * 3 + 1], z = tris[c * 3 + 2];
    const key = `${x},${y},${z}`;
    let id = map.get(key);
    if (id === undefined) {
      id = pos.length / 3;
      map.set(key, id);
      pos.push(x, y, z);
    }
    idx[c] = id;
  }
  const faceOffsets = new Uint32Array(T + 1);
  for (let t = 0; t <= T; t++) faceOffsets[t] = t * 3;
  const mesh: PolyMesh = { positions: Float64Array.from(pos), faceOffsets, faceIndices: idx };
  return {
    mesh,
    source: { kind: 'stl', binary, soupVertices: T * 3 },
    attributes: [`welded ${T * 3} STL corners into ${pos.length / 3} vertices`],
    warnings: [],
  };
}
