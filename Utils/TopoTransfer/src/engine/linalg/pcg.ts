/** Preconditioned conjugate gradients for SPD operators given as callbacks. */

export interface PCGResult {
  iterations: number;
  /** ||b - A x|| / ||b|| at exit */
  relativeResidual: number;
  converged: boolean;
}

export function pcg(
  apply: (x: Float64Array, out: Float64Array) => void,
  precond: (r: Float64Array, out: Float64Array) => void,
  b: Float64Array,
  x: Float64Array,
  tol: number,
  maxIter: number,
): PCGResult {
  const n = b.length;
  const r = new Float64Array(n);
  const z = new Float64Array(n);
  const p = new Float64Array(n);
  const q = new Float64Array(n);
  let bnorm = 0;
  for (let i = 0; i < n; i++) bnorm += b[i] * b[i];
  bnorm = Math.sqrt(bnorm);
  if (bnorm === 0) {
    x.fill(0);
    return { iterations: 0, relativeResidual: 0, converged: true };
  }
  apply(x, q);
  let rnorm = 0;
  for (let i = 0; i < n; i++) {
    r[i] = b[i] - q[i];
    rnorm += r[i] * r[i];
  }
  rnorm = Math.sqrt(rnorm);
  if (rnorm / bnorm <= tol) return { iterations: 0, relativeResidual: rnorm / bnorm, converged: true };
  precond(r, z);
  p.set(z);
  let rz = 0;
  for (let i = 0; i < n; i++) rz += r[i] * z[i];
  let it = 0;
  for (; it < maxIter; it++) {
    apply(p, q);
    let pq = 0;
    for (let i = 0; i < n; i++) pq += p[i] * q[i];
    if (!(pq > 0)) break; // loss of positive definiteness or breakdown
    const alpha = rz / pq;
    rnorm = 0;
    for (let i = 0; i < n; i++) {
      x[i] += alpha * p[i];
      r[i] -= alpha * q[i];
      rnorm += r[i] * r[i];
    }
    rnorm = Math.sqrt(rnorm);
    if (rnorm / bnorm <= tol) {
      it++;
      break;
    }
    precond(r, z);
    let rzNew = 0;
    for (let i = 0; i < n; i++) rzNew += r[i] * z[i];
    const beta = rzNew / rz;
    rz = rzNew;
    for (let i = 0; i < n; i++) p[i] = z[i] + beta * p[i];
  }
  const rel = rnorm / bnorm;
  return { iterations: it, relativeResidual: rel, converged: rel <= tol };
}
