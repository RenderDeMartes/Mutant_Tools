/**
 * Mesh-derived data used by validation and the solver: vertex adjacency,
 * normals, areas, cotangent weights, boundaries and components.
 */

/** Undirected vertex adjacency in CSR form, neighbours sorted ascending. */
export interface Adjacency {
  n: number;
  offsets: Uint32Array;
  neighbors: Uint32Array;
  /** Number of triangles using each (vertex, neighbour) edge, aligned with `neighbors`. */
  edgeTriCount: Uint32Array;
}

export function buildAdjacency(triangles: Uint32Array, n: number, extraPairs?: Uint32Array): Adjacency {
  const T = triangles.length / 3;
  const extra = extraPairs ? extraPairs.length / 2 : 0;
  const deg = new Uint32Array(n + 1);
  for (let t = 0; t < T; t++) {
    const a = triangles[t * 3], b = triangles[t * 3 + 1], c = triangles[t * 3 + 2];
    deg[a] += 2;
    deg[b] += 2;
    deg[c] += 2;
  }
  for (let e = 0; e < extra; e++) {
    deg[extraPairs![e * 2]]++;
    deg[extraPairs![e * 2 + 1]]++;
  }
  const start = new Uint32Array(n + 1);
  for (let i = 0; i < n; i++) start[i + 1] = start[i] + deg[i];
  const raw = new Uint32Array(start[n]);
  const rawTri = new Uint8Array(start[n]);
  const fill = start.slice(0, n);
  const push = (i: number, j: number, isTri: number) => {
    raw[fill[i]] = j;
    rawTri[fill[i]] = isTri;
    fill[i]++;
  };
  for (let t = 0; t < T; t++) {
    const a = triangles[t * 3], b = triangles[t * 3 + 1], c = triangles[t * 3 + 2];
    push(a, b, 1); push(b, a, 1);
    push(b, c, 1); push(c, b, 1);
    push(c, a, 1); push(a, c, 1);
  }
  for (let e = 0; e < extra; e++) {
    const a = extraPairs![e * 2], b = extraPairs![e * 2 + 1];
    push(a, b, 0);
    push(b, a, 0);
  }
  // sort + dedupe each row, counting triangle incidences
  const offsets = new Uint32Array(n + 1);
  const tmpN: number[] = [];
  const outN: number[] = [];
  const outC: number[] = [];
  for (let i = 0; i < n; i++) {
    tmpN.length = 0;
    for (let k = start[i]; k < start[i + 1]; k++) tmpN.push(raw[k] * 2 + rawTri[k]);
    tmpN.sort((x, y) => x - y);
    let last = -1;
    for (const v of tmpN) {
      const j = v >> 1;
      if (j === i) continue; // degenerate triangle with repeated index
      if (j !== last) {
        outN.push(j);
        outC.push(v & 1);
        last = j;
      } else {
        outC[outC.length - 1] += v & 1;
      }
    }
    offsets[i + 1] = outN.length;
  }
  // each triangle edge was pushed once per incident triangle per direction
  return { n, offsets, neighbors: Uint32Array.from(outN), edgeTriCount: Uint32Array.from(outC) };
}

/** Index into adjacency arrays for edge (i, j), or -1. */
export function adjacencyIndex(adj: Adjacency, i: number, j: number): number {
  let lo = adj.offsets[i];
  let hi = adj.offsets[i + 1] - 1;
  const nb = adj.neighbors;
  while (lo <= hi) {
    const mid = (lo + hi) >> 1;
    const v = nb[mid];
    if (v === j) return mid;
    if (v < j) lo = mid + 1;
    else hi = mid - 1;
  }
  return -1;
}

/** Unique undirected edges (i < j) as pairs. */
export function uniqueEdges(adj: Adjacency): Uint32Array {
  let count = 0;
  for (let i = 0; i < adj.n; i++) {
    for (let k = adj.offsets[i]; k < adj.offsets[i + 1]; k++) if (adj.neighbors[k] > i) count++;
  }
  const out = new Uint32Array(count * 2);
  let o = 0;
  for (let i = 0; i < adj.n; i++) {
    for (let k = adj.offsets[i]; k < adj.offsets[i + 1]; k++) {
      const j = adj.neighbors[k];
      if (j > i) {
        out[o++] = i;
        out[o++] = j;
      }
    }
  }
  return out;
}

/** Area-weighted vertex normals (unit length; zero vector for isolated vertices). */
export function vertexNormals(positions: Float64Array, triangles: Uint32Array, out?: Float64Array): Float64Array {
  const n = positions.length / 3;
  const N = out ?? new Float64Array(n * 3);
  N.fill(0);
  for (let t = 0; t < triangles.length; t += 3) {
    const a = triangles[t] * 3, b = triangles[t + 1] * 3, c = triangles[t + 2] * 3;
    const e1x = positions[b] - positions[a], e1y = positions[b + 1] - positions[a + 1], e1z = positions[b + 2] - positions[a + 2];
    const e2x = positions[c] - positions[a], e2y = positions[c + 1] - positions[a + 1], e2z = positions[c + 2] - positions[a + 2];
    const nx = e1y * e2z - e1z * e2y;
    const ny = e1z * e2x - e1x * e2z;
    const nz = e1x * e2y - e1y * e2x;
    N[a] += nx; N[a + 1] += ny; N[a + 2] += nz;
    N[b] += nx; N[b + 1] += ny; N[b + 2] += nz;
    N[c] += nx; N[c + 1] += ny; N[c + 2] += nz;
  }
  for (let i = 0; i < N.length; i += 3) {
    const l = Math.hypot(N[i], N[i + 1], N[i + 2]);
    if (l > 0) {
      N[i] /= l; N[i + 1] /= l; N[i + 2] /= l;
    }
  }
  return N;
}

/** Unit face normals and areas of triangles. */
export function triangleNormalsAreas(positions: Float64Array, triangles: Uint32Array): { normals: Float64Array; areas: Float64Array } {
  const T = triangles.length / 3;
  const normals = new Float64Array(T * 3);
  const areas = new Float64Array(T);
  for (let t = 0; t < T; t++) {
    const a = triangles[t * 3] * 3, b = triangles[t * 3 + 1] * 3, c = triangles[t * 3 + 2] * 3;
    const e1x = positions[b] - positions[a], e1y = positions[b + 1] - positions[a + 1], e1z = positions[b + 2] - positions[a + 2];
    const e2x = positions[c] - positions[a], e2y = positions[c + 1] - positions[a + 1], e2z = positions[c + 2] - positions[a + 2];
    const nx = e1y * e2z - e1z * e2y;
    const ny = e1z * e2x - e1x * e2z;
    const nz = e1x * e2y - e1y * e2x;
    const l = Math.hypot(nx, ny, nz);
    areas[t] = l / 2;
    if (l > 0) {
      normals[t * 3] = nx / l;
      normals[t * 3 + 1] = ny / l;
      normals[t * 3 + 2] = nz / l;
    }
  }
  return { normals, areas };
}

/** Barycentric vertex areas (one third of each incident triangle). */
export function vertexAreas(positions: Float64Array, triangles: Uint32Array): Float64Array {
  const n = positions.length / 3;
  const A = new Float64Array(n);
  const { areas } = triangleNormalsAreas(positions, triangles);
  for (let t = 0; t < areas.length; t++) {
    const a3 = areas[t] / 3;
    A[triangles[t * 3]] += a3;
    A[triangles[t * 3 + 1]] += a3;
    A[triangles[t * 3 + 2]] += a3;
  }
  return A;
}

/**
 * Clamped cotangent weights per adjacency entry (symmetric). Weights are
 * clamped to [minW, maxW] so the resulting Laplacian is an M-matrix (SPD after
 * any positive diagonal shift) even on obtuse or sliver triangles.
 */
export function cotanWeights(positions: Float64Array, triangles: Uint32Array, adj: Adjacency, minW = 0.05, maxW = 10): Float64Array {
  const w = new Float64Array(adj.neighbors.length);
  const T = triangles.length / 3;
  const add = (i: number, j: number, v: number) => {
    const k1 = adjacencyIndex(adj, i, j);
    const k2 = adjacencyIndex(adj, j, i);
    if (k1 >= 0) w[k1] += v;
    if (k2 >= 0) w[k2] += v;
  };
  for (let t = 0; t < T; t++) {
    const ids = [triangles[t * 3], triangles[t * 3 + 1], triangles[t * 3 + 2]];
    for (let c = 0; c < 3; c++) {
      const o = ids[c] * 3, i = ids[(c + 1) % 3] * 3, j = ids[(c + 2) % 3] * 3;
      const ux = positions[i] - positions[o], uy = positions[i + 1] - positions[o + 1], uz = positions[i + 2] - positions[o + 2];
      const vx = positions[j] - positions[o], vy = positions[j + 1] - positions[o + 1], vz = positions[j + 2] - positions[o + 2];
      const dot = ux * vx + uy * vy + uz * vz;
      const cx = uy * vz - uz * vy, cy = uz * vx - ux * vz, cz = ux * vy - uy * vx;
      const cr = Math.hypot(cx, cy, cz);
      const cot = cr > 1e-300 ? dot / cr : maxW;
      add(ids[(c + 1) % 3], ids[(c + 2) % 3], 0.5 * cot);
    }
  }
  for (let k = 0; k < w.length; k++) {
    if (adj.edgeTriCount[k] === 0) {
      w[k] = 0; // non-mesh pair (e.g. seam lock); weight assigned by caller
      continue;
    }
    const v = w[k];
    w[k] = v < minW ? minW : v > maxW ? maxW : v;
  }
  return w;
}

/** Flags for vertices on a boundary edge (edge used by exactly one triangle). */
export function boundaryVertices(adj: Adjacency): Uint8Array {
  const flags = new Uint8Array(adj.n);
  for (let i = 0; i < adj.n; i++) {
    for (let k = adj.offsets[i]; k < adj.offsets[i + 1]; k++) {
      if (adj.edgeTriCount[k] === 1) {
        flags[i] = 1;
        break;
      }
    }
  }
  return flags;
}

export function isBoundaryEdge(adj: Adjacency, i: number, j: number): boolean {
  const k = adjacencyIndex(adj, i, j);
  return k >= 0 && adj.edgeTriCount[k] === 1;
}

/** Connected components over the adjacency graph. Returns label per vertex and component sizes. */
export function connectedComponents(adj: Adjacency): { labels: Int32Array; sizes: number[] } {
  const labels = new Int32Array(adj.n).fill(-1);
  const sizes: number[] = [];
  const stack: number[] = [];
  for (let s = 0; s < adj.n; s++) {
    if (labels[s] >= 0) continue;
    const id = sizes.length;
    let size = 0;
    labels[s] = id;
    stack.push(s);
    while (stack.length) {
      const v = stack.pop()!;
      size++;
      for (let k = adj.offsets[v]; k < adj.offsets[v + 1]; k++) {
        const u = adj.neighbors[k];
        if (labels[u] < 0) {
          labels[u] = id;
          stack.push(u);
        }
      }
    }
    sizes.push(size);
  }
  return { labels, sizes };
}

/** Which vertices are referenced by at least one triangle. */
export function referencedVertices(triangles: Uint32Array, n: number): Uint8Array {
  const r = new Uint8Array(n);
  for (let t = 0; t < triangles.length; t++) r[triangles[t]] = 1;
  return r;
}

/**
 * Groups of coincident vertices (distance <= tol) returned as pairs (i, j)
 * chaining each group. Uses a uniform hash grid with cell size = tol.
 */
export function coincidentPairs(positions: Float64Array, tol: number): Uint32Array {
  const n = positions.length / 3;
  if (n === 0 || !(tol > 0)) return new Uint32Array(0);
  const inv = 1 / tol;
  // hashed grid; collisions only merge buckets, distances are checked exactly
  const map = new Map<number, number[]>();
  const key = (x: number, y: number, z: number) => (Math.imul(x, 73856093) ^ Math.imul(y, 19349663) ^ Math.imul(z, 83492791)) | 0;
  for (let i = 0; i < n; i++) {
    const k = key(Math.floor(positions[i * 3] * inv), Math.floor(positions[i * 3 + 1] * inv), Math.floor(positions[i * 3 + 2] * inv));
    let arr = map.get(k);
    if (!arr) map.set(k, (arr = []));
    arr.push(i);
  }
  const parent = new Int32Array(n);
  for (let i = 0; i < n; i++) parent[i] = i;
  const find = (x: number): number => {
    while (parent[x] !== x) {
      parent[x] = parent[parent[x]];
      x = parent[x];
    }
    return x;
  };
  const tol2 = tol * tol;
  const out: number[] = [];
  for (let i = 0; i < n; i++) {
    const cx = Math.floor(positions[i * 3] * inv), cy = Math.floor(positions[i * 3 + 1] * inv), cz = Math.floor(positions[i * 3 + 2] * inv);
    for (let dx = -1; dx <= 1; dx++) for (let dy = -1; dy <= 1; dy++) for (let dz = -1; dz <= 1; dz++) {
      const arr = map.get(key(cx + dx, cy + dy, cz + dz));
      if (!arr) continue;
      for (const j of arr) {
        if (j <= i) continue;
        const ddx = positions[i * 3] - positions[j * 3];
        const ddy = positions[i * 3 + 1] - positions[j * 3 + 1];
        const ddz = positions[i * 3 + 2] - positions[j * 3 + 2];
        if (ddx * ddx + ddy * ddy + ddz * ddz <= tol2) {
          const ri = find(i), rj = find(j);
          if (ri !== rj) {
            parent[rj] = ri;
            out.push(i, j);
          }
        }
      }
    }
  }
  return Uint32Array.from(out);
}

/**
 * Boundary flags that ignore "seams": boundary vertices that coincide with
 * another boundary vertex (UV / hard-edge splits) are not treated as open
 * boundary, since the surface continues across them geometrically.
 */
export function seamAwareBoundary(positions: Float64Array, adj: Adjacency, tol: number): Uint8Array {
  const flags = boundaryVertices(adj);
  const ids: number[] = [];
  for (let i = 0; i < flags.length; i++) if (flags[i]) ids.push(i);
  if (ids.length < 2) return flags;
  const sub = new Float64Array(ids.length * 3);
  ids.forEach((v, k) => sub.set(positions.subarray(v * 3, v * 3 + 3), k * 3));
  const pairs = coincidentPairs(sub, tol);
  for (let e = 0; e < pairs.length; e++) flags[ids[pairs[e]]] = 0;
  return flags;
}
