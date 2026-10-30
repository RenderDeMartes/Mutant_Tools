/**
 * Topology-preserving export with a mandatory validation step: the exported
 * bytes are parsed again and compared against the original connectivity
 * before anything is handed to the user.
 */

import { mat4Invert, transformPositions } from '../core/mat3';
import { PolyMesh, sameTopology } from '../core/mesh';
import type { LoadedMesh } from '../io/load';
import { parseOBJ, writeOBJ, writeOBJRoundTrip } from '../io/obj';
import { parsePLY, writePLY, writePLYRoundTrip } from '../io/ply';

export type ExportFormat = 'obj' | 'ply';
export type ExportSpace = 'reference' | 'original';

export interface ExportRequest {
  base: LoadedMesh;
  /** deformed positions in reference (world) space */
  positions: Float64Array;
  /** base placement transform (original -> reference space), column-major */
  transform: ArrayLike<number>;
  format: ExportFormat;
  space: ExportSpace;
}

export interface TopologyCheck {
  ok: boolean;
  vertexCount: [number, number];
  faceCount: [number, number];
  cornerCount: [number, number];
  /** max |exported - intended| coordinate difference after re-import */
  maxPositionError: number;
  messages: string[];
}

export interface ExportResult {
  fileName: string;
  mime: string;
  data: ArrayBuffer;
  check: TopologyCheck;
  notes: string[];
}

export function verifyTopology(original: PolyMesh, exported: PolyMesh, intended: Float64Array): TopologyCheck {
  const messages: string[] = [];
  const vc: [number, number] = [original.positions.length / 3, exported.positions.length / 3];
  const fc: [number, number] = [original.faceOffsets.length - 1, exported.faceOffsets.length - 1];
  const cc: [number, number] = [original.faceIndices.length, exported.faceIndices.length];
  if (vc[0] !== vc[1]) messages.push(`Vertex count changed: ${vc[0]} → ${vc[1]}`);
  if (fc[0] !== fc[1]) messages.push(`Face count changed: ${fc[0]} → ${fc[1]}`);
  const topoOK = sameTopology({ ...original, positions: exported.positions }, exported) && vc[0] === vc[1];
  if (!topoOK && messages.length === 0) messages.push('Face indices or polygon connectivity differ from the original.');
  let maxErr = 0;
  if (vc[0] === vc[1]) {
    for (let i = 0; i < intended.length; i++) maxErr = Math.max(maxErr, Math.abs(intended[i] - exported.positions[i]));
  }
  return { ok: topoOK && messages.length === 0, vertexCount: vc, faceCount: fc, cornerCount: cc, maxPositionError: maxErr, messages };
}

export function exportMesh(req: ExportRequest): ExportResult {
  const { base, format, space } = req;
  const original = base.mesh;
  if (req.positions.length !== original.positions.length) {
    throw new Error('Deformed positions do not match the base vertex count; export refused.');
  }
  const positions = space === 'original' ? transformPositions(req.positions, mat4Invert(req.transform)) : req.positions.slice();
  const out: PolyMesh = { positions, faceOffsets: original.faceOffsets, faceIndices: original.faceIndices };
  const header = [
    'Exported by TopoTransfer',
    `space: ${space === 'original' ? 'original base coordinates' : 'reference coordinates'}`,
    `vertices: ${positions.length / 3}, faces: ${original.faceOffsets.length - 1}`,
    // machine-readable placement, used by Meta Mutant (Utils/MetaMutant) to bring the reference into base space
    `topotransfer-alignment base_to_reference column_major ${Array.from(req.transform, (v) => +v.toPrecision(12)).join(' ')}`,
  ];
  const notes: string[] = [];
  let data: ArrayBuffer;
  let reparsed: PolyMesh;
  if (format === 'obj') {
    let text: string;
    if (base.source.kind === 'obj') {
      text = writeOBJRoundTrip(out, base.source, { header });
      if (base.source.normalCount) notes.push('Normals (vn) were recomputed from the deformed surface; normal indexing kept.');
      if (base.source.materials) notes.push('Material assignments kept; the .mtl file itself is not exported.');
    } else {
      text = writeOBJ(out, { header });
      if (base.source.kind === 'ply') notes.push('Source was PLY: only positions and polygons are written to OBJ. Export as PLY to keep all PLY properties.');
    }
    data = new TextEncoder().encode(text).buffer as ArrayBuffer;
    reparsed = parseOBJ(text).mesh;
  } else {
    if (base.source.kind === 'ply') {
      data = writePLYRoundTrip(out, base.source, { header });
      if (base.source.elements[base.source.vertexElement].properties.some((p) => p.name === 'nx')) notes.push('Vertex normals were recomputed.');
      const xType = base.source.elements[base.source.vertexElement].properties.find((p) => p.name === 'x')?.type;
      if (xType === 'float') notes.push('Positions are stored as 32-bit floats, as in the source file.');
    } else {
      data = writePLY(out, { header });
      if (base.source.kind === 'obj' && (base.source.uvCount || base.source.normalCount)) {
        notes.push('Source was OBJ: UVs, normals, groups and materials are not representable in this PLY export and were not written. Export as OBJ to keep them.');
      }
    }
    reparsed = parsePLY(data).mesh;
  }
  const check = verifyTopology(original, reparsed, positions);
  let scale = 1e-12;
  for (let i = 0; i < positions.length; i++) scale = Math.max(scale, Math.abs(positions[i]));
  // float32 storage allows ~1e-7 relative error; text OBJ is written with ≥ 4 decimals relative to the largest coordinate
  if (check.maxPositionError > scale * 1e-4) {
    check.ok = false;
    check.messages.push(`Exported positions differ from the result by up to ${check.maxPositionError.toPrecision(3)}.`);
  }
  if (!check.ok) throw new Error(`Export validation failed: ${check.messages.join('; ')}`);
  const stem = base.name.replace(/\.[^.]+$/, '');
  return {
    fileName: `${stem}_wrapped.${format}`,
    mime: format === 'obj' ? 'text/plain' : 'application/octet-stream',
    data,
    check,
    notes,
  };
}
