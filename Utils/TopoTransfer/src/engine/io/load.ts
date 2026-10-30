import type { PolyMesh } from '../core/mesh';
import { MeshParseError, ObjSource, parseOBJ } from './obj';
import { parsePLY, PlySource } from './ply';
import { parseSTL, StlSource } from './stl';

export type MeshRole = 'base' | 'reference';
export type MeshFormat = 'obj' | 'ply' | 'stl';
export type MeshSource = ObjSource | PlySource | StlSource;

export interface LoadedMesh {
  name: string;
  format: MeshFormat;
  mesh: PolyMesh;
  source: MeshSource;
  attributes: string[];
  warnings: string[];
  fileSize: number;
}

export function detectFormat(name: string, buffer: ArrayBuffer): MeshFormat {
  const ext = name.toLowerCase().split('.').pop() ?? '';
  if (ext === 'obj' || ext === 'ply' || ext === 'stl') return ext;
  const head = new TextDecoder('ascii').decode(new Uint8Array(buffer, 0, Math.min(256, buffer.byteLength)));
  if (head.startsWith('ply')) return 'ply';
  if (/^\s*solid/.test(head)) return 'stl';
  if (/^\s*(v|#|o|g|mtllib)\s/m.test(head)) return 'obj';
  throw new MeshParseError(`Unsupported file type "${ext || name}". Use OBJ, PLY or STL.`);
}

/** Parse a mesh file. STL is rejected for the base role because it has no stored connectivity. */
export function loadMeshFile(name: string, buffer: ArrayBuffer, role: MeshRole): LoadedMesh {
  const format = detectFormat(name, buffer);
  if (format === 'stl' && role === 'base') {
    throw new MeshParseError(
      'STL files store an unconnected triangle soup, so their topology cannot be preserved. Load STL as the Reference mesh, and use OBJ or PLY for the Base mesh.',
    );
  }
  let res;
  if (format === 'obj') res = parseOBJ(new TextDecoder().decode(buffer));
  else if (format === 'ply') res = parsePLY(buffer);
  else res = parseSTL(buffer);
  if (res.mesh.faceOffsets.length < 2) {
    throw new MeshParseError(`${name} has no polygons. Point clouds are not supported; mesh the data first.`);
  }
  return { name, format, mesh: res.mesh, source: res.source, attributes: res.attributes, warnings: res.warnings, fileSize: buffer.byteLength };
}

/** True when the file starts with the header written by Meta Mutant (MetaHuman meshes exported from a DNA). */
export function isMetaHumanExport(buffer: ArrayBuffer): boolean {
  const head = new TextDecoder().decode(new Uint8Array(buffer, 0, Math.min(400, buffer.byteLength)));
  return /^#.*MetaHuman LOD\d/m.test(head);
}
