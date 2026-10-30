/**
 * Small dense 3x3 / 4x4 helpers. Matrices are row-major `Float64Array(9)` for
 * 3x3; 4x4 transforms are column-major `Float64Array(16)` to match common
 * graphics conventions (and three.js `Matrix4.elements`).
 */

export type Mat3 = Float64Array;
export type Mat4 = Float64Array;

export function mat3Identity(out: Mat3 = new Float64Array(9)): Mat3 {
  out.fill(0);
  out[0] = 1;
  out[4] = 1;
  out[8] = 1;
  return out;
}

export function det3(m: ArrayLike<number>): number {
  return (
    m[0] * (m[4] * m[8] - m[5] * m[7]) -
    m[1] * (m[3] * m[8] - m[5] * m[6]) +
    m[2] * (m[3] * m[7] - m[4] * m[6])
  );
}

/**
 * Eigen-decomposition of a symmetric 3x3 matrix with cyclic Jacobi rotations.
 * `w` receives eigenvalues, `V` the eigenvectors as columns (row-major storage,
 * `V[r*3+c]` is component r of eigenvector c). Not sorted.
 */
const _m = new Float64Array(9);

export function symEig3(a: ArrayLike<number>, w: Float64Array, V: Float64Array): void {
  const m = _m;
  for (let i = 0; i < 9; i++) m[i] = a[i];
  mat3Identity(V);
  const scale = Math.abs(m[0]) + Math.abs(m[4]) + Math.abs(m[8]) + Math.abs(m[1]) + Math.abs(m[2]) + Math.abs(m[5]);
  if (scale === 0) {
    w[0] = w[1] = w[2] = 0;
    return;
  }
  for (let sweep = 0; sweep < 50; sweep++) {
    const off = m[1] * m[1] + m[2] * m[2] + m[5] * m[5];
    if (off <= 1e-30 * scale * scale) break;
    for (let pq = 0; pq < 3; pq++) {
      const p = pq === 2 ? 1 : 0;
      const q = pq === 0 ? 1 : 2;
      const apq = m[p * 3 + q];
      if (Math.abs(apq) <= 1e-300) continue;
      const app = m[p * 3 + p];
      const aqq = m[q * 3 + q];
      const theta = (aqq - app) / (2 * apq);
      const t = (theta >= 0 ? 1 : -1) / (Math.abs(theta) + Math.sqrt(theta * theta + 1));
      const c = 1 / Math.sqrt(t * t + 1);
      const s = t * c;
      m[p * 3 + p] = app - t * apq;
      m[q * 3 + q] = aqq + t * apq;
      m[p * 3 + q] = m[q * 3 + p] = 0;
      for (let r = 0; r < 3; r++) {
        if (r !== p && r !== q) {
          const arp = m[r * 3 + p];
          const arq = m[r * 3 + q];
          const nrp = c * arp - s * arq;
          const nrq = s * arp + c * arq;
          m[r * 3 + p] = m[p * 3 + r] = nrp;
          m[r * 3 + q] = m[q * 3 + r] = nrq;
        }
        const vrp = V[r * 3 + p];
        const vrq = V[r * 3 + q];
        V[r * 3 + p] = c * vrp - s * vrq;
        V[r * 3 + q] = s * vrp + c * vrq;
      }
    }
  }
  w[0] = m[0];
  w[1] = m[4];
  w[2] = m[8];
}

const _mtm = new Float64Array(9);
const _w = new Float64Array(3);
const _V = new Float64Array(9);

/**
 * Singular value decomposition M = U diag(s) V^T of a general 3x3 matrix.
 * Singular values are sorted descending; U and V are proper orthonormal bases
 * (U may be a reflection only when M itself has negative determinant).
 */
export function svd3(M: ArrayLike<number>, U: Float64Array, s: Float64Array, V: Float64Array): void {
  // M^T M
  for (let i = 0; i < 3; i++) {
    for (let j = 0; j < 3; j++) {
      _mtm[i * 3 + j] = M[i] * M[j] + M[3 + i] * M[3 + j] + M[6 + i] * M[6 + j];
    }
  }
  symEig3(_mtm, _w, _V);
  // sort descending (3-element network, no allocation)
  let o0 = 0, o1 = 1, o2 = 2, tmp: number;
  if (_w[o0] < _w[o1]) { tmp = o0; o0 = o1; o1 = tmp; }
  if (_w[o1] < _w[o2]) { tmp = o1; o1 = o2; o2 = tmp; }
  if (_w[o0] < _w[o1]) { tmp = o0; o0 = o1; o1 = tmp; }
  for (let c = 0; c < 3; c++) {
    const src = c === 0 ? o0 : c === 1 ? o1 : o2;
    s[c] = Math.sqrt(Math.max(0, _w[src]));
    V[c] = _V[src];
    V[3 + c] = _V[3 + src];
    V[6 + c] = _V[6 + src];
  }
  // make V a proper rotation basis (det +1) for stable completion
  if (det3(V) < 0) {
    V[2] = -V[2];
    V[5] = -V[5];
    V[8] = -V[8];
  }
  const tol = Math.max(s[0], 1e-300) * 1e-10;
  let good = 0;
  for (let c = 0; c < 3; c++) {
    if (s[c] > tol) {
      const ux = M[0] * V[c] + M[1] * V[3 + c] + M[2] * V[6 + c];
      const uy = M[3] * V[c] + M[4] * V[3 + c] + M[5] * V[6 + c];
      const uz = M[6] * V[c] + M[7] * V[3 + c] + M[8] * V[6 + c];
      const inv = 1 / s[c];
      U[c] = ux * inv;
      U[3 + c] = uy * inv;
      U[6 + c] = uz * inv;
      good++;
    } else {
      s[c] = 0;
    }
  }
  if (good === 0) {
    mat3Identity(U);
    return;
  }
  if (good === 1) {
    // any unit vector orthogonal to U0
    const x = U[0], y = U[3], z = U[6];
    let ox: number, oy: number, oz: number;
    if (Math.abs(x) < 0.9) {
      // cross with e_x
      ox = 0; oy = z; oz = -y;
    } else {
      // cross with e_y
      ox = -z; oy = 0; oz = x;
    }
    const l = Math.hypot(ox, oy, oz);
    U[1] = ox / l; U[4] = oy / l; U[7] = oz / l;
    good = 2;
  }
  if (good === 2) {
    // U2 = U0 x U1
    U[2] = U[3] * U[7] - U[6] * U[4];
    U[5] = U[6] * U[1] - U[0] * U[7];
    U[8] = U[0] * U[4] - U[3] * U[1];
  }
}

const _U = new Float64Array(9);
const _S = new Float64Array(3);
const _V2 = new Float64Array(9);

/**
 * Closest proper rotation to M (polar decomposition with reflection fix):
 * argmax_R tr(R^T M), det R = +1. Writes row-major R. Returns sum of the
 * singular values with the sign correction applied (used by Umeyama scale).
 */
export function closestRotation(M: ArrayLike<number>, R: Float64Array): number {
  svd3(M, _U, _S, _V2);
  let d = det3(_U) * det3(_V2) < 0 ? -1 : 1;
  // R = U diag(1,1,d) V^T
  for (let i = 0; i < 3; i++) {
    for (let j = 0; j < 3; j++) {
      R[i * 3 + j] =
        _U[i * 3] * _V2[j * 3] + _U[i * 3 + 1] * _V2[j * 3 + 1] + d * _U[i * 3 + 2] * _V2[j * 3 + 2];
    }
  }
  return _S[0] + _S[1] + d * _S[2];
}

/** 4x4 column-major identity. */
export function mat4Identity(out: Mat4 = new Float64Array(16)): Mat4 {
  out.fill(0);
  out[0] = out[5] = out[10] = out[15] = 1;
  return out;
}

/** out = a * b (column-major 4x4). */
export function mat4Multiply(a: ArrayLike<number>, b: ArrayLike<number>, out: Mat4 = new Float64Array(16)): Mat4 {
  const r = new Float64Array(16);
  for (let c = 0; c < 4; c++) {
    for (let rr = 0; rr < 4; rr++) {
      r[c * 4 + rr] =
        a[rr] * b[c * 4] + a[4 + rr] * b[c * 4 + 1] + a[8 + rr] * b[c * 4 + 2] + a[12 + rr] * b[c * 4 + 3];
    }
  }
  out.set(r);
  return out;
}

/** Build a similarity transform (column-major) from row-major rotation, uniform scale and translation. */
export function mat4FromSimilarity(R: ArrayLike<number>, scale: number, t: ArrayLike<number>): Mat4 {
  const m = mat4Identity();
  for (let i = 0; i < 3; i++) {
    for (let j = 0; j < 3; j++) {
      m[j * 4 + i] = R[i * 3 + j] * scale;
    }
  }
  m[12] = t[0];
  m[13] = t[1];
  m[14] = t[2];
  return m;
}

/** General 4x4 inverse (column-major). Throws if singular. */
export function mat4Invert(m: ArrayLike<number>): Mat4 {
  const inv = new Float64Array(16);
  inv[0] = m[5] * m[10] * m[15] - m[5] * m[11] * m[14] - m[9] * m[6] * m[15] + m[9] * m[7] * m[14] + m[13] * m[6] * m[11] - m[13] * m[7] * m[10];
  inv[4] = -m[4] * m[10] * m[15] + m[4] * m[11] * m[14] + m[8] * m[6] * m[15] - m[8] * m[7] * m[14] - m[12] * m[6] * m[11] + m[12] * m[7] * m[10];
  inv[8] = m[4] * m[9] * m[15] - m[4] * m[11] * m[13] - m[8] * m[5] * m[15] + m[8] * m[7] * m[13] + m[12] * m[5] * m[11] - m[12] * m[7] * m[9];
  inv[12] = -m[4] * m[9] * m[14] + m[4] * m[10] * m[13] + m[8] * m[5] * m[14] - m[8] * m[6] * m[13] - m[12] * m[5] * m[10] + m[12] * m[6] * m[9];
  inv[1] = -m[1] * m[10] * m[15] + m[1] * m[11] * m[14] + m[9] * m[2] * m[15] - m[9] * m[3] * m[14] - m[13] * m[2] * m[11] + m[13] * m[3] * m[10];
  inv[5] = m[0] * m[10] * m[15] - m[0] * m[11] * m[14] - m[8] * m[2] * m[15] + m[8] * m[3] * m[14] + m[12] * m[2] * m[11] - m[12] * m[3] * m[10];
  inv[9] = -m[0] * m[9] * m[15] + m[0] * m[11] * m[13] + m[8] * m[1] * m[15] - m[8] * m[3] * m[13] - m[12] * m[1] * m[11] + m[12] * m[3] * m[9];
  inv[13] = m[0] * m[9] * m[14] - m[0] * m[10] * m[13] - m[8] * m[1] * m[14] + m[8] * m[2] * m[13] + m[12] * m[1] * m[10] - m[12] * m[2] * m[9];
  inv[2] = m[1] * m[6] * m[15] - m[1] * m[7] * m[14] - m[5] * m[2] * m[15] + m[5] * m[3] * m[14] + m[13] * m[2] * m[7] - m[13] * m[3] * m[6];
  inv[6] = -m[0] * m[6] * m[15] + m[0] * m[7] * m[14] + m[4] * m[2] * m[15] - m[4] * m[3] * m[14] - m[12] * m[2] * m[7] + m[12] * m[3] * m[6];
  inv[10] = m[0] * m[5] * m[15] - m[0] * m[7] * m[13] - m[4] * m[1] * m[15] + m[4] * m[3] * m[13] + m[12] * m[1] * m[7] - m[12] * m[3] * m[5];
  inv[14] = -m[0] * m[5] * m[14] + m[0] * m[6] * m[13] + m[4] * m[1] * m[14] - m[4] * m[2] * m[13] - m[12] * m[1] * m[6] + m[12] * m[2] * m[5];
  inv[3] = -m[1] * m[6] * m[11] + m[1] * m[7] * m[10] + m[5] * m[2] * m[11] - m[5] * m[3] * m[10] - m[9] * m[2] * m[7] + m[9] * m[3] * m[6];
  inv[7] = m[0] * m[6] * m[11] - m[0] * m[7] * m[10] - m[4] * m[2] * m[11] + m[4] * m[3] * m[10] + m[8] * m[2] * m[7] - m[8] * m[3] * m[6];
  inv[11] = -m[0] * m[5] * m[11] + m[0] * m[7] * m[9] + m[4] * m[1] * m[11] - m[4] * m[3] * m[9] - m[8] * m[1] * m[7] + m[8] * m[3] * m[5];
  inv[15] = m[0] * m[5] * m[10] - m[0] * m[6] * m[9] - m[4] * m[1] * m[10] + m[4] * m[2] * m[9] + m[8] * m[1] * m[6] - m[8] * m[2] * m[5];
  const det = m[0] * inv[0] + m[1] * inv[4] + m[2] * inv[8] + m[3] * inv[12];
  if (!Number.isFinite(det) || Math.abs(det) < 1e-300) throw new Error('Transform is singular and cannot be inverted.');
  const id = 1 / det;
  for (let i = 0; i < 16; i++) inv[i] *= id;
  return inv;
}

/** Apply a column-major 4x4 transform to interleaved xyz positions. */
export function transformPositions(positions: Float64Array, m: ArrayLike<number>, out?: Float64Array): Float64Array {
  const res = out ?? new Float64Array(positions.length);
  for (let i = 0; i < positions.length; i += 3) {
    const x = positions[i], y = positions[i + 1], z = positions[i + 2];
    res[i] = m[0] * x + m[4] * y + m[8] * z + m[12];
    res[i + 1] = m[1] * x + m[5] * y + m[9] * z + m[13];
    res[i + 2] = m[2] * x + m[6] * y + m[10] * z + m[14];
  }
  return res;
}

export function transformPoint(p: ArrayLike<number>, m: ArrayLike<number>): [number, number, number] {
  const x = p[0], y = p[1], z = p[2];
  return [
    m[0] * x + m[4] * y + m[8] * z + m[12],
    m[1] * x + m[5] * y + m[9] * z + m[13],
    m[2] * x + m[6] * y + m[10] * z + m[14],
  ];
}

/** True if the 4x4 transform's linear part is a uniform scale times a proper rotation (within tolerance). */
export function isSimilarity(m: ArrayLike<number>, tol = 1e-6): boolean {
  const cols = [0, 4, 8].map((o) => [m[o], m[o + 1], m[o + 2]]);
  const lens = cols.map((c) => Math.hypot(c[0], c[1], c[2]));
  const s = lens[0];
  if (s <= 0) return false;
  for (const l of lens) if (Math.abs(l - s) > tol * s) return false;
  for (let a = 0; a < 3; a++) {
    for (let b = a + 1; b < 3; b++) {
      const d = cols[a][0] * cols[b][0] + cols[a][1] * cols[b][1] + cols[a][2] * cols[b][2];
      if (Math.abs(d) > tol * s * s) return false;
    }
  }
  return true;
}
