/** Compressed sparse row matrices and the few operations the solver needs. */

export interface CSRMatrix {
  rows: number;
  cols: number;
  rowPtr: Int32Array;
  colIdx: Int32Array;
  values: Float64Array;
}

/**
 * Square symmetric pattern containing the diagonal plus (i,j) and (j,i) for
 * every pair. Duplicate pairs are merged. Values start at zero.
 */
export function symmetricPattern(n: number, pairs: Uint32Array): CSRMatrix {
  const m = pairs.length / 2;
  const deg = new Int32Array(n);
  for (let i = 0; i < n; i++) deg[i] = 1;
  for (let e = 0; e < m; e++) {
    const a = pairs[e * 2], b = pairs[e * 2 + 1];
    if (a === b) continue;
    deg[a]++;
    deg[b]++;
  }
  const start = new Int32Array(n + 1);
  for (let i = 0; i < n; i++) start[i + 1] = start[i] + deg[i];
  const raw = new Int32Array(start[n]);
  const fill = start.slice(0, n);
  for (let i = 0; i < n; i++) raw[fill[i]++] = i;
  for (let e = 0; e < m; e++) {
    const a = pairs[e * 2], b = pairs[e * 2 + 1];
    if (a === b) continue;
    raw[fill[a]++] = b;
    raw[fill[b]++] = a;
  }
  const rowPtr = new Int32Array(n + 1);
  const cols: number[] = [];
  for (let i = 0; i < n; i++) {
    const seg = Array.from(raw.subarray(start[i], start[i + 1])).sort((x, y) => x - y);
    let last = -1;
    for (const c of seg) {
      if (c !== last) cols.push(c);
      last = c;
    }
    rowPtr[i + 1] = cols.length;
  }
  return { rows: n, cols: n, rowPtr, colIdx: Int32Array.from(cols), values: new Float64Array(cols.length) };
}

/** Index of entry (i, j) in values/colIdx, or -1 if not in the pattern. */
export function findEntry(A: CSRMatrix, i: number, j: number): number {
  let lo = A.rowPtr[i], hi = A.rowPtr[i + 1] - 1;
  const c = A.colIdx;
  while (lo <= hi) {
    const mid = (lo + hi) >> 1;
    const v = c[mid];
    if (v === j) return mid;
    if (v < j) lo = mid + 1;
    else hi = mid - 1;
  }
  return -1;
}

export function diagonalIndices(A: CSRMatrix): Int32Array {
  const d = new Int32Array(A.rows);
  for (let i = 0; i < A.rows; i++) {
    d[i] = findEntry(A, i, i);
  }
  return d;
}

/** y = A x */
export function spmv(A: CSRMatrix, x: Float64Array, y: Float64Array): void {
  const { rowPtr, colIdx, values } = A;
  for (let i = 0; i < A.rows; i++) {
    let s = 0;
    for (let k = rowPtr[i]; k < rowPtr[i + 1]; k++) s += values[k] * x[colIdx[k]];
    y[i] = s;
  }
}

export function transpose(A: CSRMatrix): CSRMatrix {
  const count = new Int32Array(A.cols + 1);
  for (let k = 0; k < A.colIdx.length; k++) count[A.colIdx[k] + 1]++;
  for (let j = 0; j < A.cols; j++) count[j + 1] += count[j];
  const rowPtr = count.slice();
  const fill = count.slice(0, A.cols);
  const colIdx = new Int32Array(A.colIdx.length);
  const values = new Float64Array(A.colIdx.length);
  for (let i = 0; i < A.rows; i++) {
    for (let k = A.rowPtr[i]; k < A.rowPtr[i + 1]; k++) {
      const j = A.colIdx[k];
      const p = fill[j]++;
      colIdx[p] = i;
      values[p] = A.values[k];
    }
  }
  return { rows: A.cols, cols: A.rows, rowPtr, colIdx, values };
}

/** Sparse matrix product C = A B (columns sorted per row). */
export function spgemm(A: CSRMatrix, B: CSRMatrix): CSRMatrix {
  if (A.cols !== B.rows) throw new Error('spgemm: dimension mismatch');
  const marker = new Int32Array(B.cols).fill(-1);
  const acc = new Float64Array(B.cols);
  const rowPtr = new Int32Array(A.rows + 1);
  let cap = Math.max(16, A.colIdx.length + B.colIdx.length);
  let colIdx = new Int32Array(cap);
  let values = new Float64Array(cap);
  let nnz = 0;
  const rowCols: number[] = [];
  for (let i = 0; i < A.rows; i++) {
    rowCols.length = 0;
    for (let ka = A.rowPtr[i]; ka < A.rowPtr[i + 1]; ka++) {
      const k = A.colIdx[ka];
      const av = A.values[ka];
      for (let kb = B.rowPtr[k]; kb < B.rowPtr[k + 1]; kb++) {
        const j = B.colIdx[kb];
        if (marker[j] !== i) {
          marker[j] = i;
          acc[j] = av * B.values[kb];
          rowCols.push(j);
        } else {
          acc[j] += av * B.values[kb];
        }
      }
    }
    rowCols.sort((x, y) => x - y);
    if (nnz + rowCols.length > cap) {
      cap = Math.max(cap * 2, nnz + rowCols.length);
      const c2 = new Int32Array(cap); c2.set(colIdx); colIdx = c2;
      const v2 = new Float64Array(cap); v2.set(values); values = v2;
    }
    for (const j of rowCols) {
      colIdx[nnz] = j;
      values[nnz] = acc[j];
      nnz++;
    }
    rowPtr[i + 1] = nnz;
  }
  return { rows: A.rows, cols: B.cols, rowPtr, colIdx: colIdx.slice(0, nnz), values: values.slice(0, nnz) };
}

/**
 * Numeric-only product: recompute C.values = (A B) where C already holds the
 * sparsity pattern of A B (from an earlier `spgemm` with the same patterns).
 * `acc` must have length >= B.cols.
 */
export function spgemmNumeric(A: CSRMatrix, B: CSRMatrix, C: CSRMatrix, acc: Float64Array): void {
  for (let i = 0; i < A.rows; i++) {
    const cs = C.rowPtr[i], ce = C.rowPtr[i + 1];
    for (let k = cs; k < ce; k++) acc[C.colIdx[k]] = 0;
    for (let ka = A.rowPtr[i]; ka < A.rowPtr[i + 1]; ka++) {
      const k = A.colIdx[ka];
      const av = A.values[ka];
      for (let kb = B.rowPtr[k]; kb < B.rowPtr[k + 1]; kb++) acc[B.colIdx[kb]] += av * B.values[kb];
    }
    for (let k = cs; k < ce; k++) C.values[k] = acc[C.colIdx[k]];
  }
}

/** In-place dense Cholesky (lower, row-major n x n). Returns false if not positive definite. */
export function denseCholesky(M: Float64Array, n: number): boolean {
  for (let j = 0; j < n; j++) {
    let d = M[j * n + j];
    for (let k = 0; k < j; k++) d -= M[j * n + k] * M[j * n + k];
    if (!(d > 0)) return false;
    const ljj = Math.sqrt(d);
    M[j * n + j] = ljj;
    const inv = 1 / ljj;
    for (let i = j + 1; i < n; i++) {
      let s = M[i * n + j];
      for (let k = 0; k < j; k++) s -= M[i * n + k] * M[j * n + k];
      M[i * n + j] = s * inv;
    }
  }
  return true;
}

/** Solve L L^T x = b in place (x holds b on entry). */
export function denseCholeskySolve(L: Float64Array, n: number, x: Float64Array): void {
  for (let i = 0; i < n; i++) {
    let s = x[i];
    for (let k = 0; k < i; k++) s -= L[i * n + k] * x[k];
    x[i] = s / L[i * n + i];
  }
  for (let i = n - 1; i >= 0; i--) {
    let s = x[i];
    for (let k = i + 1; k < n; k++) s -= L[k * n + i] * x[k];
    x[i] = s / L[i * n + i];
  }
}
