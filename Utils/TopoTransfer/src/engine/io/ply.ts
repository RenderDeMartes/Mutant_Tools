/**
 * Stanford PLY import/export (ascii, binary little/big endian).
 *
 * All elements and properties are kept generically so export can write the
 * file back with the same header, element order and property types; only
 * vertex x/y/z (and nx/ny/nz, recomputed) change.
 */

import type { PolyMesh } from '../core/mesh';
import { triangulate } from '../core/mesh';
import { vertexNormals } from '../geometry/topology';
import { MeshParseError, ParseResult } from './obj';

type PlyFormat = 'ascii' | 'binary_little_endian' | 'binary_big_endian';
type ScalarType = 'char' | 'uchar' | 'short' | 'ushort' | 'int' | 'uint' | 'float' | 'double';

interface PlyProperty {
  name: string;
  type: ScalarType;
  /** list properties: count type */
  listCountType?: ScalarType;
}

interface PlyElement {
  name: string;
  count: number;
  properties: PlyProperty[];
  /** scalar property data (same order as properties; null for list props) */
  scalars: (Float64Array | null)[];
  /** list property data */
  lists: ({ offsets: Uint32Array; values: Float64Array } | null)[];
}

export interface PlySource {
  kind: 'ply';
  format: PlyFormat;
  comments: string[];
  objInfo: string[];
  elements: PlyElement[];
  vertexElement: number;
  faceElement: number;
  faceProperty: number;
}

const TYPE_ALIASES: Record<string, ScalarType> = {
  char: 'char', int8: 'char',
  uchar: 'uchar', uint8: 'uchar',
  short: 'short', int16: 'short',
  ushort: 'ushort', uint16: 'ushort',
  int: 'int', int32: 'int',
  uint: 'uint', uint32: 'uint',
  float: 'float', float32: 'float',
  double: 'double', float64: 'double',
};

const TYPE_SIZE: Record<ScalarType, number> = { char: 1, uchar: 1, short: 2, ushort: 2, int: 4, uint: 4, float: 4, double: 8 };

function readScalar(dv: DataView, off: number, t: ScalarType, le: boolean): number {
  switch (t) {
    case 'char': return dv.getInt8(off);
    case 'uchar': return dv.getUint8(off);
    case 'short': return dv.getInt16(off, le);
    case 'ushort': return dv.getUint16(off, le);
    case 'int': return dv.getInt32(off, le);
    case 'uint': return dv.getUint32(off, le);
    case 'float': return dv.getFloat32(off, le);
    case 'double': return dv.getFloat64(off, le);
  }
}

function writeScalar(dv: DataView, off: number, t: ScalarType, v: number, le: boolean): void {
  switch (t) {
    case 'char': dv.setInt8(off, v); break;
    case 'uchar': dv.setUint8(off, v); break;
    case 'short': dv.setInt16(off, v, le); break;
    case 'ushort': dv.setUint16(off, v, le); break;
    case 'int': dv.setInt32(off, v, le); break;
    case 'uint': dv.setUint32(off, v, le); break;
    case 'float': dv.setFloat32(off, v, le); break;
    case 'double': dv.setFloat64(off, v, le); break;
  }
}

export function parsePLY(buffer: ArrayBuffer): ParseResult<PlySource> {
  const bytes = new Uint8Array(buffer);
  // locate end_header
  const marker = 'end_header';
  let headerEnd = -1;
  const limit = Math.min(bytes.length, 1 << 20);
  for (let i = 0; i < limit - marker.length; i++) {
    let ok = true;
    for (let k = 0; k < marker.length; k++) if (bytes[i + k] !== marker.charCodeAt(k)) { ok = false; break; }
    if (ok) {
      let j = i + marker.length;
      if (bytes[j] === 13) j++;
      if (bytes[j] === 10) j++;
      headerEnd = j;
      break;
    }
  }
  if (headerEnd < 0) throw new MeshParseError('PLY header has no end_header line');
  const header = new TextDecoder('ascii').decode(bytes.subarray(0, headerEnd));
  const hlines = header.split(/\r?\n/).map((l) => l.trim()).filter((l) => l.length);
  if (hlines[0] !== 'ply') throw new MeshParseError('Not a PLY file (missing "ply" magic)');
  let format: PlyFormat | null = null;
  const comments: string[] = [];
  const objInfo: string[] = [];
  const elements: PlyElement[] = [];
  for (let i = 1; i < hlines.length; i++) {
    const t = hlines[i].split(/\s+/);
    if (t[0] === 'format') {
      if (t[1] !== 'ascii' && t[1] !== 'binary_little_endian' && t[1] !== 'binary_big_endian') throw new MeshParseError(`Unsupported PLY format "${t[1]}"`);
      format = t[1];
    } else if (t[0] === 'comment') comments.push(hlines[i].slice(8));
    else if (t[0] === 'obj_info') objInfo.push(hlines[i].slice(9));
    else if (t[0] === 'element') {
      const count = parseInt(t[2], 10);
      if (!(count >= 0)) throw new MeshParseError(`Invalid element count in "${hlines[i]}"`);
      elements.push({ name: t[1], count, properties: [], scalars: [], lists: [] });
    } else if (t[0] === 'property') {
      const el = elements[elements.length - 1];
      if (!el) throw new MeshParseError('PLY property declared before any element');
      if (t[1] === 'list') {
        const ct = TYPE_ALIASES[t[2]], it = TYPE_ALIASES[t[3]];
        if (!ct || !it) throw new MeshParseError(`Unknown PLY list type in "${hlines[i]}"`);
        el.properties.push({ name: t[4], type: it, listCountType: ct });
      } else {
        const ty = TYPE_ALIASES[t[1]];
        if (!ty) throw new MeshParseError(`Unknown PLY property type in "${hlines[i]}"`);
        el.properties.push({ name: t[2], type: ty });
      }
    } else if (t[0] === 'end_header') break;
  }
  if (!format) throw new MeshParseError('PLY header has no format line');

  if (format === 'ascii') {
    const body = new TextDecoder().decode(bytes.subarray(headerEnd));
    const tok = body.split(/\s+/).filter((s) => s.length);
    let p = 0;
    const next = () => {
      if (p >= tok.length) throw new MeshParseError('PLY data ended early');
      return +tok[p++];
    };
    for (const el of elements) {
      allocate(el);
      for (let r = 0; r < el.count; r++) {
        el.properties.forEach((prop, pi) => {
          if (prop.listCountType) {
            const c = next();
            const L = el.lists[pi]!;
            pushList(L, r, c, next);
          } else el.scalars[pi]![r] = next();
        });
      }
      finishLists(el);
    }
  } else {
    const le = format === 'binary_little_endian';
    const dv = new DataView(buffer);
    let off = headerEnd;
    for (const el of elements) {
      allocate(el);
      for (let r = 0; r < el.count; r++) {
        for (let pi = 0; pi < el.properties.length; pi++) {
          const prop = el.properties[pi];
          if (prop.listCountType) {
            if (off + TYPE_SIZE[prop.listCountType] > buffer.byteLength) throw new MeshParseError('PLY binary data ended early');
            const c = readScalar(dv, off, prop.listCountType, le);
            off += TYPE_SIZE[prop.listCountType];
            const sz = TYPE_SIZE[prop.type];
            if (off + c * sz > buffer.byteLength) throw new MeshParseError('PLY binary data ended early');
            const L = el.lists[pi]!;
            let k = 0;
            pushList(L, r, c, () => {
              const v = readScalar(dv, off + k * sz, prop.type, le);
              k++;
              return v;
            });
            off += c * sz;
          } else {
            if (off + TYPE_SIZE[prop.type] > buffer.byteLength) throw new MeshParseError('PLY binary data ended early');
            el.scalars[pi]![r] = readScalar(dv, off, prop.type, le);
            off += TYPE_SIZE[prop.type];
          }
        }
      }
      finishLists(el);
    }
  }

  const vertexElement = elements.findIndex((e) => e.name === 'vertex');
  if (vertexElement < 0) throw new MeshParseError('PLY file has no vertex element');
  const ve = elements[vertexElement];
  const ix = ve.properties.findIndex((p) => p.name === 'x');
  const iy = ve.properties.findIndex((p) => p.name === 'y');
  const iz = ve.properties.findIndex((p) => p.name === 'z');
  if (ix < 0 || iy < 0 || iz < 0) throw new MeshParseError('PLY vertex element lacks x/y/z');
  const n = ve.count;
  const positions = new Float64Array(n * 3);
  for (let i = 0; i < n; i++) {
    positions[i * 3] = ve.scalars[ix]![i];
    positions[i * 3 + 1] = ve.scalars[iy]![i];
    positions[i * 3 + 2] = ve.scalars[iz]![i];
  }
  const faceElement = elements.findIndex((e) => e.name === 'face');
  let faceProperty = -1;
  let faceOffsets = new Uint32Array([0]);
  let faceIndices = new Uint32Array(0);
  if (faceElement >= 0) {
    const fe = elements[faceElement];
    faceProperty = fe.properties.findIndex((p) => !!p.listCountType && (p.name === 'vertex_indices' || p.name === 'vertex_index'));
    if (faceProperty < 0) throw new MeshParseError('PLY face element has no vertex_indices list');
    const L = fe.lists[faceProperty]!;
    faceOffsets = L.offsets.slice();
    faceIndices = new Uint32Array(L.values.length);
    for (let k = 0; k < L.values.length; k++) {
      const v = L.values[k];
      if (!Number.isInteger(v) || v < 0 || v >= n) throw new MeshParseError(`PLY face references vertex ${v} (mesh has ${n} vertices)`);
      faceIndices[k] = v;
    }
  }
  const attributes: string[] = [];
  const warnings: string[] = [];
  const vprops = ve.properties.map((p) => p.name).filter((nm) => !['x', 'y', 'z'].includes(nm));
  if (vprops.some((p) => p === 'nx')) attributes.push('vertex normals (recomputed on export)');
  const other = vprops.filter((p) => !['nx', 'ny', 'nz'].includes(p));
  if (other.length) attributes.push(`vertex properties ${other.join(', ')} (preserved)`);
  if (faceElement >= 0) {
    const fp = elements[faceElement].properties.filter((_, i) => i !== faceProperty).map((p) => p.name);
    if (fp.length) attributes.push(`face properties ${fp.join(', ')} (preserved)`);
  }
  for (const el of elements) {
    if (el.name !== 'vertex' && el.name !== 'face') attributes.push(`element "${el.name}" ×${el.count} (preserved, not deformed)`);
  }
  if (faceElement < 0) warnings.push('PLY file has no faces (point cloud). It can only be used as a reference after meshing.');
  return {
    mesh: { positions, faceOffsets, faceIndices },
    source: { kind: 'ply', format, comments, objInfo, elements, vertexElement, faceElement, faceProperty },
    attributes,
    warnings,
  };
}

function allocate(el: PlyElement) {
  el.scalars = el.properties.map((p) => (p.listCountType ? null : new Float64Array(el.count)));
  el.lists = el.properties.map((p) => (p.listCountType ? { offsets: new Uint32Array(el.count + 1), values: new Float64Array(Math.max(16, el.count * 4)) } : null));
}

function pushList(L: { offsets: Uint32Array; values: Float64Array }, row: number, count: number, next: () => number) {
  if (!Number.isInteger(count) || count < 0) throw new MeshParseError(`Invalid PLY list length ${count}`);
  const start = L.offsets[row];
  if (start + count > L.values.length) {
    const grown = new Float64Array(Math.max(L.values.length * 2, start + count));
    grown.set(L.values);
    L.values = grown;
  }
  for (let k = 0; k < count; k++) L.values[start + k] = next();
  L.offsets[row + 1] = start + count;
}

function finishLists(el: PlyElement) {
  el.lists = el.lists.map((L) => (L ? { offsets: L.offsets, values: L.values.slice(0, L.offsets[el.count]) } : null));
}

/** Export: same header, elements and types; vertex positions replaced, normals recomputed if present. */
export function writePLYRoundTrip(mesh: PolyMesh, source: PlySource, opts: { header?: string[]; format?: PlyFormat } = {}): ArrayBuffer {
  const format = opts.format ?? source.format;
  const elements = source.elements.map((e) => ({ ...e, scalars: e.scalars.slice(), lists: e.lists.slice() }));
  const ve = elements[source.vertexElement];
  const n = mesh.positions.length / 3;
  if (n !== ve.count) throw new Error('Vertex count differs from the original PLY; refusing to export.');
  const setProp = (name: string, data: (i: number) => number) => {
    const pi = ve.properties.findIndex((p) => p.name === name);
    if (pi < 0) return;
    const arr = new Float64Array(n);
    for (let i = 0; i < n; i++) arr[i] = data(i);
    ve.scalars[pi] = arr;
  };
  const p = mesh.positions;
  setProp('x', (i) => p[i * 3]);
  setProp('y', (i) => p[i * 3 + 1]);
  setProp('z', (i) => p[i * 3 + 2]);
  if (ve.properties.some((q) => q.name === 'nx')) {
    const N = vertexNormals(p, triangulate(mesh).triangles);
    setProp('nx', (i) => N[i * 3]);
    setProp('ny', (i) => N[i * 3 + 1]);
    setProp('nz', (i) => N[i * 3 + 2]);
  }
  return encodePLY(format, [...source.comments, ...(opts.header ?? [])], source.objInfo, elements);
}

/** Plain PLY writer for meshes without a PLY source. */
export function writePLY(mesh: PolyMesh, opts: { header?: string[]; format?: PlyFormat } = {}): ArrayBuffer {
  const n = mesh.positions.length / 3;
  const F = mesh.faceOffsets.length - 1;
  const xs = new Float64Array(n), ys = new Float64Array(n), zs = new Float64Array(n);
  for (let i = 0; i < n; i++) {
    xs[i] = mesh.positions[i * 3];
    ys[i] = mesh.positions[i * 3 + 1];
    zs[i] = mesh.positions[i * 3 + 2];
  }
  const elements: PlyElement[] = [
    {
      name: 'vertex',
      count: n,
      properties: [{ name: 'x', type: 'double' }, { name: 'y', type: 'double' }, { name: 'z', type: 'double' }],
      scalars: [xs, ys, zs],
      lists: [null, null, null],
    },
    {
      name: 'face',
      count: F,
      properties: [{ name: 'vertex_indices', type: 'int', listCountType: 'uchar' }],
      scalars: [null],
      lists: [{ offsets: mesh.faceOffsets.slice(), values: Float64Array.from(mesh.faceIndices) }],
    },
  ];
  for (let f = 0; f < F; f++) {
    if (mesh.faceOffsets[f + 1] - mesh.faceOffsets[f] > 255) elements[1].properties[0].listCountType = 'int';
  }
  return encodePLY(opts.format ?? 'binary_little_endian', opts.header ?? [], [], elements);
}

function encodePLY(format: PlyFormat, comments: string[], objInfo: string[], elements: PlyElement[]): ArrayBuffer {
  const h: string[] = ['ply', `format ${format} 1.0`];
  for (const c of comments) h.push(`comment ${c}`);
  for (const o of objInfo) h.push(`obj_info ${o}`);
  for (const el of elements) {
    h.push(`element ${el.name} ${el.count}`);
    for (const p of el.properties) h.push(p.listCountType ? `property list ${p.listCountType} ${p.type} ${p.name}` : `property ${p.type} ${p.name}`);
  }
  h.push('end_header');
  const headerText = h.join('\n') + '\n';
  const enc = new TextEncoder();
  if (format === 'ascii') {
    const out: string[] = [headerText];
    const fmt = (v: number, t: ScalarType) => (t === 'float' || t === 'double' ? (Number.isInteger(v) ? String(v) : v.toPrecision(t === 'float' ? 9 : 17)) : String(Math.round(v)));
    for (const el of elements) {
      for (let r = 0; r < el.count; r++) {
        const parts: string[] = [];
        el.properties.forEach((p, pi) => {
          if (p.listCountType) {
            const L = el.lists[pi]!;
            const s = L.offsets[r], e = L.offsets[r + 1];
            parts.push(String(e - s));
            for (let k = s; k < e; k++) parts.push(fmt(L.values[k], p.type));
          } else parts.push(fmt(el.scalars[pi]![r], p.type));
        });
        out.push(parts.join(' ') + '\n');
      }
    }
    return enc.encode(out.join('')).buffer as ArrayBuffer;
  }
  const le = format === 'binary_little_endian';
  let size = 0;
  for (const el of elements) {
    el.properties.forEach((p, pi) => {
      if (p.listCountType) {
        const L = el.lists[pi]!;
        size += el.count * TYPE_SIZE[p.listCountType] + L.offsets[el.count] * TYPE_SIZE[p.type];
      } else size += el.count * TYPE_SIZE[p.type];
    });
  }
  const hb = enc.encode(headerText);
  const buf = new ArrayBuffer(hb.length + size);
  new Uint8Array(buf).set(hb);
  const dv = new DataView(buf);
  let off = hb.length;
  for (const el of elements) {
    for (let r = 0; r < el.count; r++) {
      for (let pi = 0; pi < el.properties.length; pi++) {
        const p = el.properties[pi];
        if (p.listCountType) {
          const L = el.lists[pi]!;
          const s = L.offsets[r], e = L.offsets[r + 1];
          writeScalar(dv, off, p.listCountType, e - s, le);
          off += TYPE_SIZE[p.listCountType];
          for (let k = s; k < e; k++) {
            writeScalar(dv, off, p.type, L.values[k], le);
            off += TYPE_SIZE[p.type];
          }
        } else {
          writeScalar(dv, off, p.type, el.scalars[pi]![r], le);
          off += TYPE_SIZE[p.type];
        }
      }
    }
  }
  return buf;
}
