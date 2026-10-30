/**
 * Smoothed-aggregation algebraic multigrid used as a preconditioner for the
 * wrapping solver's sparse SPD systems.
 *
 * Setup (once per wrap): aggregates and smoothed prolongators P_l are built
 * from a setup matrix (the stiffness Laplacian). Each solver iteration calls
 * `update(A)` to rebuild the Galerkin coarse operators R A P for the current
 * values, then `apply` runs one symmetric V-cycle (forward Gauss–Seidel pre-
 * smoothing, backward post-smoothing, dense Cholesky on the coarsest level), so
 * the preconditioner is symmetric positive definite as PCG requires.
 */

import { CSRMatrix, denseCholesky, denseCholeskySolve, diagonalIndices, spgemm, spgemmNumeric, spmv, transpose } from './csr';

interface Level {
  A: CSRMatrix;
  P: CSRMatrix | null;
  R: CSRMatrix | null;
  diag: Int32Array;
  x: Float64Array;
  b: Float64Array;
  r: Float64Array;
}

export interface AMGOptions {
  maxCoarse?: number;
  maxLevels?: number;
  strengthTheta?: number;
}

export class AMG {
  private prolongators: CSRMatrix[] = [];
  private restrictors: CSRMatrix[] = [];
  private levels: Level[] = [];
  private coarseL: Float64Array | null = null;
  /** cached Galerkin products per level (patterns are reused when the fine pattern is unchanged) */
  private galerkin: { fineRowPtr: Int32Array; fineColIdx: Int32Array; AP: CSRMatrix; RAP: CSRMatrix }[] = [];
  private acc = new Float64Array(0);
  private coarseN = 0;

  get levelCount(): number {
    return this.prolongators.length + 1;
  }

  get levelSizes(): number[] {
    return this.levels.map((l) => l.A.rows);
  }

  static build(Asetup: CSRMatrix, opts: AMGOptions = {}): AMG {
    const maxCoarse = opts.maxCoarse ?? 300;
    const maxLevels = opts.maxLevels ?? 12;
    let theta = opts.strengthTheta ?? 0.08;
    const amg = new AMG();
    let A = Asetup;
    for (let l = 0; l < maxLevels - 1 && A.rows > maxCoarse; l++) {
      const agg = aggregate(A, theta);
      if (agg.count >= A.rows * 0.9 || agg.count < 1) break; // coarsening stalled
      const P = smoothProlongator(A, agg.labels, agg.count);
      const R = transpose(P);
      amg.prolongators.push(P);
      amg.restrictors.push(R);
      A = spgemm(R, spgemm(A, P));
      theta *= 0.5;
    }
    amg.update(Asetup);
    return amg;
  }

  /** Rebuild Galerkin coarse operators for new fine-level values (pattern may differ from setup). */
  update(A0: CSRMatrix): void {
    const prev = this.levels;
    this.levels = [];
    let A = A0;
    for (let l = 0; l <= this.prolongators.length; l++) {
      const P = l < this.prolongators.length ? this.prolongators[l] : null;
      const R = l < this.restrictors.length ? this.restrictors[l] : null;
      const old = prev[l];
      const samePattern = !!old && old.A.rowPtr === A.rowPtr && old.A.colIdx === A.colIdx;
      this.levels.push({
        A,
        P,
        R,
        diag: samePattern ? old.diag : diagonalIndices(A),
        x: samePattern ? old.x : new Float64Array(A.rows),
        b: samePattern ? old.b : new Float64Array(A.rows),
        r: samePattern ? old.r : new Float64Array(A.rows),
      });
      if (P && R) {
        const g = this.galerkin[l];
        if (g && g.fineRowPtr === A.rowPtr && g.fineColIdx === A.colIdx) {
          const need = Math.max(g.AP.cols, g.RAP.cols);
          if (this.acc.length < need) this.acc = new Float64Array(need);
          spgemmNumeric(A, P, g.AP, this.acc);
          spgemmNumeric(R, g.AP, g.RAP, this.acc);
          A = g.RAP;
        } else {
          const AP = spgemm(A, P);
          const RAP = spgemm(R, AP);
          this.galerkin[l] = { fineRowPtr: A.rowPtr, fineColIdx: A.colIdx, AP, RAP };
          A = RAP;
        }
      }
    }
    const coarse = this.levels[this.levels.length - 1].A;
    const n = coarse.rows;
    const M = new Float64Array(n * n);
    let maxDiag = 0;
    for (let i = 0; i < n; i++) {
      for (let k = coarse.rowPtr[i]; k < coarse.rowPtr[i + 1]; k++) {
        M[i * n + coarse.colIdx[k]] = coarse.values[k];
        if (coarse.colIdx[k] === i) maxDiag = Math.max(maxDiag, coarse.values[k]);
      }
    }
    let shift = 0;
    for (let attempt = 0; attempt < 8; attempt++) {
      const W = M.slice();
      if (shift > 0) for (let i = 0; i < n; i++) W[i * n + i] += shift;
      if (denseCholesky(W, n)) {
        this.coarseL = W;
        this.coarseN = n;
        return;
      }
      shift = shift === 0 ? Math.max(maxDiag, 1e-300) * 1e-12 : shift * 100;
    }
    throw new Error('AMG: coarse operator is not positive definite');
  }

  /** z ≈ A^{-1} r via one V-cycle (z is overwritten). */
  apply(r: Float64Array, z: Float64Array): void {
    const top = this.levels[0];
    top.b.set(r);
    this.vcycle(0);
    z.set(top.x);
  }

  private vcycle(l: number): void {
    const lev = this.levels[l];
    if (l === this.levels.length - 1) {
      lev.x.set(lev.b);
      denseCholeskySolve(this.coarseL!, this.coarseN, lev.x);
      return;
    }
    lev.x.fill(0);
    gaussSeidel(lev.A, lev.diag, lev.b, lev.x, true);
    spmv(lev.A, lev.x, lev.r);
    for (let i = 0; i < lev.r.length; i++) lev.r[i] = lev.b[i] - lev.r[i];
    const next = this.levels[l + 1];
    spmv(lev.R!, lev.r, next.b);
    this.vcycle(l + 1);
    // x += P xc
    const P = lev.P!;
    for (let i = 0; i < P.rows; i++) {
      let s = 0;
      for (let k = P.rowPtr[i]; k < P.rowPtr[i + 1]; k++) s += P.values[k] * next.x[P.colIdx[k]];
      lev.x[i] += s;
    }
    gaussSeidel(lev.A, lev.diag, lev.b, lev.x, false);
  }
}

function gaussSeidel(A: CSRMatrix, diag: Int32Array, b: Float64Array, x: Float64Array, forward: boolean): void {
  const { rowPtr, colIdx, values } = A;
  const n = A.rows;
  if (forward) {
    for (let i = 0; i < n; i++) {
      let s = b[i];
      for (let k = rowPtr[i]; k < rowPtr[i + 1]; k++) s -= values[k] * x[colIdx[k]];
      const d = values[diag[i]];
      x[i] += s / d;
    }
  } else {
    for (let i = n - 1; i >= 0; i--) {
      let s = b[i];
      for (let k = rowPtr[i]; k < rowPtr[i + 1]; k++) s -= values[k] * x[colIdx[k]];
      const d = values[diag[i]];
      x[i] += s / d;
    }
  }
}

/** Greedy aggregation over strong connections (standard SA passes 1–3). */
function aggregate(A: CSRMatrix, theta: number): { labels: Int32Array; count: number } {
  const n = A.rows;
  const diag = new Float64Array(n);
  for (let i = 0; i < n; i++) {
    for (let k = A.rowPtr[i]; k < A.rowPtr[i + 1]; k++) if (A.colIdx[k] === i) diag[i] = A.values[k];
  }
  const strong = (i: number, k: number) => {
    const j = A.colIdx[k];
    if (j === i) return false;
    const a = Math.abs(A.values[k]);
    return a > theta * Math.sqrt(Math.abs(diag[i] * diag[j]));
  };
  const labels = new Int32Array(n).fill(-1);
  let count = 0;
  // pass 1: roots whose strong neighbourhood is entirely free
  for (let i = 0; i < n; i++) {
    if (labels[i] >= 0) continue;
    let free = true;
    let hasStrong = false;
    for (let k = A.rowPtr[i]; k < A.rowPtr[i + 1]; k++) {
      if (!strong(i, k)) continue;
      hasStrong = true;
      if (labels[A.colIdx[k]] >= 0) {
        free = false;
        break;
      }
    }
    if (!free || !hasStrong) continue;
    labels[i] = count;
    for (let k = A.rowPtr[i]; k < A.rowPtr[i + 1]; k++) if (strong(i, k)) labels[A.colIdx[k]] = count;
    count++;
  }
  // pass 2: attach remaining nodes to the strongest neighbouring aggregate
  const pass2 = labels.slice();
  for (let i = 0; i < n; i++) {
    if (labels[i] >= 0) continue;
    let best = -1, bestV = -Infinity;
    for (let k = A.rowPtr[i]; k < A.rowPtr[i + 1]; k++) {
      const j = A.colIdx[k];
      if (j === i || labels[j] < 0) continue;
      const v = Math.abs(A.values[k]);
      if (v > bestV) {
        bestV = v;
        best = labels[j];
      }
    }
    if (best >= 0) pass2[i] = best;
  }
  // pass 3: leftovers (isolated or weakly connected) become their own aggregates
  for (let i = 0; i < n; i++) {
    if (pass2[i] < 0) pass2[i] = count++;
  }
  return { labels: pass2, count };
}

/** P = (I - ω D^{-1} A) P0 with ω = 4 / (3 ρ(D^{-1} A)). */
function smoothProlongator(A: CSRMatrix, labels: Int32Array, count: number): CSRMatrix {
  const n = A.rows;
  const invD = new Float64Array(n);
  for (let i = 0; i < n; i++) {
    for (let k = A.rowPtr[i]; k < A.rowPtr[i + 1]; k++) if (A.colIdx[k] === i) invD[i] = A.values[k] !== 0 ? 1 / A.values[k] : 0;
  }
  const rho = spectralRadiusDinvA(A, invD);
  const omega = rho > 0 ? 4 / (3 * rho) : 0;
  // P0 is 0/1 aggregation; S = I - ω D^{-1} A; P = S P0 computed row by row
  const rowPtr = new Int32Array(n + 1);
  const cols: number[] = [];
  const vals: number[] = [];
  const acc = new Map<number, number>();
  for (let i = 0; i < n; i++) {
    acc.clear();
    acc.set(labels[i], 1);
    for (let k = A.rowPtr[i]; k < A.rowPtr[i + 1]; k++) {
      const j = A.colIdx[k];
      const c = labels[j];
      acc.set(c, (acc.get(c) ?? 0) - omega * invD[i] * A.values[k]);
    }
    const keys = Array.from(acc.keys()).sort((a, b) => a - b);
    for (const c of keys) {
      const v = acc.get(c)!;
      if (v !== 0) {
        cols.push(c);
        vals.push(v);
      }
    }
    rowPtr[i + 1] = cols.length;
  }
  return { rows: n, cols: count, rowPtr, colIdx: Int32Array.from(cols), values: Float64Array.from(vals) };
}

function spectralRadiusDinvA(A: CSRMatrix, invD: Float64Array): number {
  const n = A.rows;
  let v = new Float64Array(n);
  let w = new Float64Array(n);
  // deterministic pseudo-random start
  let seed = 12345;
  for (let i = 0; i < n; i++) {
    seed = (Math.imul(seed, 1103515245) + 12345) | 0;
    v[i] = ((seed >>> 8) & 0xffff) / 65536 + 0.5;
  }
  let lambda = 0;
  for (let it = 0; it < 15; it++) {
    spmv(A, v, w);
    let norm = 0;
    for (let i = 0; i < n; i++) {
      w[i] *= invD[i];
      norm += w[i] * w[i];
    }
    norm = Math.sqrt(norm);
    if (norm === 0) return 0;
    let vn = 0;
    for (let i = 0; i < n; i++) vn += v[i] * v[i];
    lambda = norm / Math.sqrt(vn);
    for (let i = 0; i < n; i++) w[i] /= norm;
    const t = v; v = w; w = t;
  }
  // power iteration underestimates; pad slightly so ω stays safe
  return lambda * 1.05;
}
