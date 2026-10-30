/**
 * Wavefront OBJ import/export.
 *
 * Export is a *round-trip*: every original line is written back verbatim
 * except vertex positions (`v`) and, optionally, normals (`vn`), which are
 * recomputed from the deformed surface while keeping the original normal
 * indexing (so hard-edge splits survive). Face lines, UVs, groups, materials
 * and smoothing groups are copied byte-for-byte, which guarantees identical
 * vertex order, face indices and polygon connectivity.
 */

import type { PolyMesh } from '../core/mesh';

export interface ObjSource {
  kind: 'obj';
  lines: string[];
  /** line index of each `v` record */
  vertexLine: Int32Array;
  /** line index of each `vn` record */
  normalLine: Int32Array;
  /** normal index per face corner (aligned with faceIndices), -1 if none */
  cornerNormal: Int32Array;
  uvCount: number;
  normalCount: number;
  /** number of vertex records that carry extra values (e.g. vertex colours) */
  vertexExtraCount: number;
  groups: number;
  objects: number;
  materials: number;
  lineElements: number;
  pointElements: number;
  /** keyword -> count for records we pass through without interpreting */
  passthrough: Record<string, number>;
}

export interface ParseResult<S> {
  mesh: PolyMesh;
  source: S;
  /** human-readable notes about attributes found */
  attributes: string[];
  warnings: string[];
}

export class MeshParseError extends Error {
  constructor(message: string, public readonly line?: number) {
    super(line !== undefined ? `${message} (line ${line + 1})` : message);
  }
}

const KNOWN = new Set(['v', 'vt', 'vn', 'f', 'g', 'o', 's', 'usemtl', 'mtllib', 'l', 'p', 'vp']);

export function parseOBJ(text: string): ParseResult<ObjSource> {
  const lines = text.split(/\r?\n/);
  // OBJ allows '\' line continuation; join them so face records are complete
  if (text.includes('\\\n') || text.includes('\\\r\n')) {
    for (let i = 0; i < lines.length - 1; i++) {
      while (lines[i].endsWith('\\') && i + 1 < lines.length) {
        lines[i] = lines[i].slice(0, -1) + ' ' + lines[i + 1];
        lines.splice(i + 1, 1);
      }
    }
  }
  const pos: number[] = [];
  const vertexLine: number[] = [];
  const normalLine: number[] = [];
  const faceOffsets: number[] = [0];
  const faceIdx: number[] = [];
  const cornerNormal: number[] = [];
  let uvCount = 0;
  let vertexExtraCount = 0;
  let groups = 0, objects = 0, materials = 0, lineElements = 0, pointElements = 0;
  const passthrough: Record<string, number> = {};
  const warnings: string[] = [];

  for (let li = 0; li < lines.length; li++) {
    const raw = lines[li];
    let s = 0;
    while (s < raw.length && (raw.charCodeAt(s) === 32 || raw.charCodeAt(s) === 9)) s++;
    if (s >= raw.length || raw.charCodeAt(s) === 35) continue; // blank or comment
    const tokens = raw.slice(s).trim().split(/\s+/);
    const key = tokens[0];
    switch (key) {
      case 'v': {
        if (tokens.length < 4) throw new MeshParseError('Vertex record needs 3 coordinates', li);
        const x = +tokens[1], y = +tokens[2], z = +tokens[3];
        if (!Number.isFinite(x) || !Number.isFinite(y) || !Number.isFinite(z)) {
          throw new MeshParseError(`Invalid vertex coordinate "${tokens.slice(1, 4).join(' ')}"`, li);
        }
        pos.push(x, y, z);
        vertexLine.push(li);
        if (tokens.length > 4) vertexExtraCount++;
        break;
      }
      case 'vt':
        uvCount++;
        break;
      case 'vn':
        normalLine.push(li);
        break;
      case 'f': {
        if (tokens.length < 4) throw new MeshParseError('Face record needs at least 3 corners', li);
        const nv = pos.length / 3;
        for (let k = 1; k < tokens.length; k++) {
          const parts = tokens[k].split('/');
          let vi = parseInt(parts[0], 10);
          if (!Number.isFinite(vi) || vi === 0) throw new MeshParseError(`Invalid face vertex index "${tokens[k]}"`, li);
          vi = vi < 0 ? nv + vi : vi - 1;
          if (vi < 0 || vi >= nv) throw new MeshParseError(`Face references vertex ${parts[0]} which is not defined before it`, li);
          faceIdx.push(vi);
          let ni = -1;
          if (parts.length >= 3 && parts[2] !== '') {
            const raw2 = parseInt(parts[2], 10);
            if (Number.isFinite(raw2) && raw2 !== 0) ni = raw2 < 0 ? normalLine.length + raw2 : raw2 - 1;
            if (ni < 0 || ni >= normalLine.length) {
              warnings.push(`Face on line ${li + 1} references an undefined normal; normal index ignored.`);
              ni = -1;
            }
          }
          cornerNormal.push(ni);
        }
        faceOffsets.push(faceIdx.length);
        break;
      }
      case 'g': groups++; break;
      case 'o': objects++; break;
      case 'usemtl': materials++; break;
      case 'l': lineElements++; break;
      case 'p': pointElements++; break;
      default:
        if (!KNOWN.has(key)) passthrough[key] = (passthrough[key] ?? 0) + 1;
    }
  }
  if (pos.length === 0) throw new MeshParseError('OBJ file contains no vertices');
  const mesh: PolyMesh = {
    positions: Float64Array.from(pos),
    faceOffsets: Uint32Array.from(faceOffsets),
    faceIndices: Uint32Array.from(faceIdx),
  };
  const source: ObjSource = {
    kind: 'obj',
    lines,
    vertexLine: Int32Array.from(vertexLine),
    normalLine: Int32Array.from(normalLine),
    cornerNormal: Int32Array.from(cornerNormal),
    uvCount,
    normalCount: normalLine.length,
    vertexExtraCount,
    groups,
    objects,
    materials,
    lineElements,
    pointElements,
    passthrough,
  };
  const attributes: string[] = [];
  if (uvCount) attributes.push(`${uvCount} texture coordinates (preserved)`);
  if (normalLine.length) attributes.push(`${normalLine.length} normals (recomputed on export, indexing preserved)`);
  if (vertexExtraCount) attributes.push(`${vertexExtraCount} vertices with extra values, e.g. colours (preserved)`);
  if (groups || objects) attributes.push(`${groups} groups / ${objects} objects (preserved)`);
  if (materials) attributes.push(`${materials} material assignments (preserved; .mtl file is not exported)`);
  if (lineElements || pointElements) attributes.push(`${lineElements} line / ${pointElements} point elements (preserved, not deformed separately)`);
  for (const [k, c] of Object.entries(passthrough)) attributes.push(`${c} unrecognised "${k}" records (copied verbatim)`);
  return { mesh, source, attributes, warnings: Array.from(new Set(warnings)) };
}

function decimalsFor(positions: Float64Array): number {
  let m = 0;
  for (let i = 0; i < positions.length; i++) m = Math.max(m, Math.abs(positions[i]));
  if (!(m > 0)) return 6;
  return Math.min(12, Math.max(4, 8 - Math.floor(Math.log10(m))));
}

/**
 * Recompute normals for an OBJ normal table: each original `vn` index gets the
 * area-weighted average of the polygon normals of all corners that use it.
 */
export function recomputeObjNormals(mesh: PolyMesh, source: ObjSource): Float64Array {
  const out = new Float64Array(source.normalCount * 3);
  const { positions, faceOffsets, faceIndices } = mesh;
  const F = faceOffsets.length - 1;
  for (let f = 0; f < F; f++) {
    const s = faceOffsets[f], e = faceOffsets[f + 1];
    // Newell normal (area-weighted, robust for non-planar polygons)
    let nx = 0, ny = 0, nz = 0;
    for (let k = s; k < e; k++) {
      const a = faceIndices[k] * 3, b = faceIndices[k + 1 < e ? k + 1 : s] * 3;
      nx += (positions[a + 1] - positions[b + 1]) * (positions[a + 2] + positions[b + 2]);
      ny += (positions[a + 2] - positions[b + 2]) * (positions[a] + positions[b]);
      nz += (positions[a] - positions[b]) * (positions[a + 1] + positions[b + 1]);
    }
    for (let k = s; k < e; k++) {
      const ni = source.cornerNormal[k];
      if (ni < 0) continue;
      out[ni * 3] += nx;
      out[ni * 3 + 1] += ny;
      out[ni * 3 + 2] += nz;
    }
  }
  for (let i = 0; i < source.normalCount; i++) {
    const l = Math.hypot(out[i * 3], out[i * 3 + 1], out[i * 3 + 2]);
    if (l > 0) {
      out[i * 3] /= l;
      out[i * 3 + 1] /= l;
      out[i * 3 + 2] /= l;
    } else {
      out[i * 3 + 2] = 1;
    }
  }
  return out;
}

export interface ObjExportOptions {
  /** recompute vn records from the new geometry (default true) */
  recomputeNormals?: boolean;
  header?: string[];
}

/** Round-trip export using the original OBJ source. `mesh` must have the source's topology. */
export function writeOBJRoundTrip(mesh: PolyMesh, source: ObjSource, opts: ObjExportOptions = {}): string {
  const n = mesh.positions.length / 3;
  if (n !== source.vertexLine.length) throw new Error('Vertex count differs from the original OBJ; refusing to export.');
  const dec = decimalsFor(mesh.positions);
  const lines = source.lines.slice();
  const p = mesh.positions;
  for (let i = 0; i < n; i++) {
    const li = source.vertexLine[i];
    const tokens = lines[li].trim().split(/\s+/);
    const extra = tokens.length > 4 ? ' ' + tokens.slice(4).join(' ') : '';
    lines[li] = `v ${p[i * 3].toFixed(dec)} ${p[i * 3 + 1].toFixed(dec)} ${p[i * 3 + 2].toFixed(dec)}${extra}`;
  }
  if ((opts.recomputeNormals ?? true) && source.normalCount > 0) {
    const N = recomputeObjNormals(mesh, source);
    for (let i = 0; i < source.normalCount; i++) {
      lines[source.normalLine[i]] = `vn ${N[i * 3].toFixed(6)} ${N[i * 3 + 1].toFixed(6)} ${N[i * 3 + 2].toFixed(6)}`;
    }
  }
  const header = (opts.header ?? []).map((h) => `# ${h}`);
  // drop a trailing empty line from split() so we don't grow the file each round trip
  if (lines.length && lines[lines.length - 1] === '') lines.pop();
  return [...header, ...lines].join('\n') + '\n';
}

/** Plain OBJ writer (no source available, e.g. base imported from PLY). */
export function writeOBJ(mesh: PolyMesh, opts: { header?: string[] } = {}): string {
  const out: string[] = (opts.header ?? []).map((h) => `# ${h}`);
  const p = mesh.positions;
  const dec = decimalsFor(p);
  for (let i = 0; i < p.length; i += 3) out.push(`v ${p[i].toFixed(dec)} ${p[i + 1].toFixed(dec)} ${p[i + 2].toFixed(dec)}`);
  const { faceOffsets, faceIndices } = mesh;
  for (let f = 0; f + 1 < faceOffsets.length; f++) {
    let s = 'f';
    for (let k = faceOffsets[f]; k < faceOffsets[f + 1]; k++) s += ' ' + (faceIndices[k] + 1);
    out.push(s);
  }
  return out.join('\n') + '\n';
}
