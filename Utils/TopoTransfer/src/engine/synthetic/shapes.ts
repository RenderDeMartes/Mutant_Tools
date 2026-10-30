/**
 * Deterministic synthetic meshes with known geometry, used for tests,
 * benchmarks and the in-app example scene.
 */

import { PolyMesh, polyMeshFromArrays } from '../core/mesh';

/**
 * Quad-dominant sphere built from a subdivided cube ("spherified cube").
 * `segments` quads per cube edge; vertex count = 6·segments² + 2.
 */
export function cubeSphere(segments: number, radius = 1): PolyMesh {
  const N = Math.max(1, Math.floor(segments));
  const keyOf = (x: number, y: number, z: number) => `${x},${y},${z}`;
  const index = new Map<string, number>();
  const pos: number[] = [];
  const faces: number[][] = [];
  const vid = (c: [number, number, number]) => {
    const k = keyOf(c[0], c[1], c[2]);
    let id = index.get(k);
    if (id === undefined) {
      id = pos.length / 3;
      index.set(k, id);
      const x = c[0] / N, y = c[1] / N, z = c[2] / N;
      // equal-area-ish cube -> sphere map
      const sx = x * Math.sqrt(1 - (y * y) / 2 - (z * z) / 2 + (y * y * z * z) / 3);
      const sy = y * Math.sqrt(1 - (z * z) / 2 - (x * x) / 2 + (z * z * x * x) / 3);
      const sz = z * Math.sqrt(1 - (x * x) / 2 - (y * y) / 2 + (x * x * y * y) / 3);
      pos.push(sx * radius, sy * radius, sz * radius);
    }
    return id;
  };
  for (let k = 0; k < 3; k++) {
    const ua = (k + 1) % 3, va = (k + 2) % 3;
    for (const s of [1, -1]) {
      for (let i = 0; i < N; i++) {
        for (let j = 0; j < N; j++) {
          const corner = (ii: number, jj: number): [number, number, number] => {
            const c: [number, number, number] = [0, 0, 0];
            c[k] = s * N;
            c[ua] = -N + 2 * ii;
            c[va] = -N + 2 * jj;
            return c;
          };
          const q = [corner(i, j), corner(i + 1, j), corner(i + 1, j + 1), corner(i, j + 1)].map(vid);
          faces.push(s > 0 ? q : [q[0], q[3], q[2], q[1]]);
        }
      }
    }
  }
  return polyMeshFromArrays(pos, faces);
}

/** Icosphere (triangles only); vertex count = 10·4^subdivisions + 2. */
export function icosphere(subdivisions: number, radius = 1): PolyMesh {
  const t = (1 + Math.sqrt(5)) / 2;
  let verts: number[][] = [
    [-1, t, 0], [1, t, 0], [-1, -t, 0], [1, -t, 0],
    [0, -1, t], [0, 1, t], [0, -1, -t], [0, 1, -t],
    [t, 0, -1], [t, 0, 1], [-t, 0, -1], [-t, 0, 1],
  ].map(normalize);
  let faces: number[][] = [
    [0, 11, 5], [0, 5, 1], [0, 1, 7], [0, 7, 10], [0, 10, 11],
    [1, 5, 9], [5, 11, 4], [11, 10, 2], [10, 7, 6], [7, 1, 8],
    [3, 9, 4], [3, 4, 2], [3, 2, 6], [3, 6, 8], [3, 8, 9],
    [4, 9, 5], [2, 4, 11], [6, 2, 10], [8, 6, 7], [9, 8, 1],
  ];
  for (let s = 0; s < subdivisions; s++) {
    const cache = new Map<string, number>();
    const mid = (a: number, b: number) => {
      const key = a < b ? `${a}_${b}` : `${b}_${a}`;
      let id = cache.get(key);
      if (id === undefined) {
        id = verts.length;
        verts.push(normalize([(verts[a][0] + verts[b][0]) / 2, (verts[a][1] + verts[b][1]) / 2, (verts[a][2] + verts[b][2]) / 2]));
        cache.set(key, id);
      }
      return id;
    };
    const next: number[][] = [];
    for (const [a, b, c] of faces) {
      const ab = mid(a, b), bc = mid(b, c), ca = mid(c, a);
      next.push([a, ab, ca], [b, bc, ab], [c, ca, bc], [ab, bc, ca]);
    }
    faces = next;
  }
  verts = verts.map((v) => v.map((x) => x * radius));
  return polyMeshFromArrays(verts.flat(), faces);
}

function normalize(v: number[]): number[] {
  const l = Math.hypot(v[0], v[1], v[2]);
  return [v[0] / l, v[1] / l, v[2] / l];
}

export interface Bump {
  dir: [number, number, number];
  amplitude: number;
  width: number;
}

export interface ShapeField {
  scale: [number, number, number];
  bumps: Bump[];
}

/** Radial shape function: point on unit sphere -> deformed surface point. */
export function evalField(field: ShapeField, x: number, y: number, z: number): [number, number, number] {
  const l = Math.hypot(x, y, z) || 1;
  const ux = x / l, uy = y / l, uz = z / l;
  let r = 1;
  for (const b of field.bumps) {
    const d = normalize(b.dir);
    const dx = ux - d[0], dy = uy - d[1], dz = uz - d[2];
    r += b.amplitude * Math.exp(-(dx * dx + dy * dy + dz * dz) / (b.width * b.width));
  }
  return [ux * r * field.scale[0], uy * r * field.scale[1], uz * r * field.scale[2]];
}

/** Apply a shape field to every vertex (vertices are projected onto the unit sphere first). */
export function applyField(mesh: PolyMesh, field: ShapeField): PolyMesh {
  const p = mesh.positions.slice();
  for (let i = 0; i < p.length; i += 3) {
    const q = evalField(field, p[i], p[i + 1], p[i + 2]);
    p[i] = q[0];
    p[i + 1] = q[1];
    p[i + 2] = q[2];
  }
  return { positions: p, faceOffsets: mesh.faceOffsets.slice(), faceIndices: mesh.faceIndices.slice() };
}

/** Stylised head proportions used for the example scene and tests. */
export const HEAD_FIELD: ShapeField = {
  scale: [0.82, 1.08, 0.95],
  bumps: [
    { dir: [0, -0.15, 1], amplitude: 0.22, width: 0.22 }, // nose
    { dir: [0, -0.75, 0.66], amplitude: 0.1, width: 0.3 }, // chin
    { dir: [0.35, 0.25, 0.9], amplitude: 0.06, width: 0.18 }, // brow R
    { dir: [-0.35, 0.25, 0.9], amplitude: 0.06, width: 0.18 }, // brow L
    { dir: [1, 0.05, 0], amplitude: 0.1, width: 0.16 }, // ear R
    { dir: [-1, 0.05, 0], amplitude: 0.1, width: 0.16 }, // ear L
    { dir: [0, 1, -0.3], amplitude: 0.08, width: 0.6 }, // cranium
  ],
};

/** Keep only faces whose centroid satisfies `keep` (creates open boundaries). */
export function cropFaces(mesh: PolyMesh, keep: (cx: number, cy: number, cz: number) => boolean): PolyMesh {
  const faces: number[][] = [];
  const { positions: p, faceOffsets, faceIndices } = mesh;
  for (let f = 0; f + 1 < faceOffsets.length; f++) {
    let cx = 0, cy = 0, cz = 0;
    const s = faceOffsets[f], e = faceOffsets[f + 1];
    for (let k = s; k < e; k++) {
      cx += p[faceIndices[k] * 3];
      cy += p[faceIndices[k] * 3 + 1];
      cz += p[faceIndices[k] * 3 + 2];
    }
    const m = e - s;
    if (keep(cx / m, cy / m, cz / m)) faces.push(Array.from(faceIndices.subarray(s, e)));
  }
  return polyMeshFromArrays(p, faces);
}

/** Nearest vertex to a point (brute force; test helper). */
export function nearestVertex(mesh: PolyMesh, x: number, y: number, z: number): number {
  let best = -1, bd = Infinity;
  const p = mesh.positions;
  for (let i = 0; i < p.length; i += 3) {
    const d = (p[i] - x) ** 2 + (p[i + 1] - y) ** 2 + (p[i + 2] - z) ** 2;
    if (d < bd) {
      bd = d;
      best = i / 3;
    }
  }
  return best;
}

/** cube-sphere segments needed for roughly `vertices` vertices */
export function segmentsForVertexCount(vertices: number): number {
  return Math.max(1, Math.round(Math.sqrt(Math.max(0, vertices - 2) / 6)));
}

/** Concatenate meshes into one multi-component mesh (vertex order = input order). */
export function mergeMeshes(parts: PolyMesh[]): PolyMesh {
  const pos: number[] = [];
  const faces: number[][] = [];
  for (const m of parts) {
    const off = pos.length / 3;
    pos.push(...m.positions);
    for (let f = 0; f + 1 < m.faceOffsets.length; f++) faces.push(Array.from(m.faceIndices.subarray(m.faceOffsets[f], m.faceOffsets[f + 1]), (v) => v + off));
  }
  return polyMeshFromArrays(pos, faces);
}

/** Small sphere component (e.g. an eyeball) at `center` with `radius`. */
export function sphereAt(center: [number, number, number], radius: number, segments = 6): PolyMesh {
  const m = cubeSphere(segments);
  return { ...m, positions: m.positions.map((v, i) => v * radius + center[i % 3]) };
}

/** Example base: head proxy with two inner eyeballs as separate components. */
export function exampleHeadBase(segments = 40): PolyMesh {
  return mergeMeshes([cubeSphere(segments), sphereAt([0.3, 0.12, 0.74], 0.15), sphereAt([-0.3, 0.12, 0.74], 0.15)]);
}
