import { describe, expect, it } from 'vitest';
import { closestRotation, det3, svd3 } from '../src/engine/core/mat3';
import { triangulate } from '../src/engine/core/mesh';
import { TriangleBVH, makeHit, closestOnTriangle } from '../src/engine/spatial/bvh';
import { AMG } from '../src/engine/linalg/amg';
import { pcg } from '../src/engine/linalg/pcg';
import { spmv, symmetricPattern, findEntry, denseCholesky, denseCholeskySolve } from '../src/engine/linalg/csr';
import { buildAdjacency, uniqueEdges } from '../src/engine/geometry/topology';
import { cubeSphere, icosphere } from '../src/engine/synthetic/shapes';
import { axisAngle, rng } from './helpers';

describe('3x3 decompositions', () => {
  it('svd3 reconstructs random matrices and closestRotation returns proper rotations', () => {
    const r = rng(11);
    const U = new Float64Array(9), S = new Float64Array(3), V = new Float64Array(9), R = new Float64Array(9);
    for (let t = 0; t < 200; t++) {
      const M = Float64Array.from({ length: 9 }, () => r() * 2 - 1);
      svd3(M, U, S, V);
      for (let i = 0; i < 3; i++) {
        for (let j = 0; j < 3; j++) {
          let v = 0;
          for (let k = 0; k < 3; k++) v += U[i * 3 + k] * S[k] * V[j * 3 + k];
          expect(v).toBeCloseTo(M[i * 3 + j], 8);
        }
      }
      expect(S[0]).toBeGreaterThanOrEqual(S[1]);
      expect(S[1]).toBeGreaterThanOrEqual(S[2]);
      closestRotation(M, R);
      expect(det3(R)).toBeCloseTo(1, 9);
    }
    // exact rotation (also a scaled one) is recovered
    const Q = axisAngle([1, -2, 0.5], 2.1);
    closestRotation(Q.map((v) => v * 3), R);
    for (let i = 0; i < 9; i++) expect(R[i]).toBeCloseTo(Q[i], 9);
    // rank-deficient input still gives a rotation
    closestRotation(Float64Array.from([1, 0, 0, 0, 0, 0, 0, 0, 0]), R);
    expect(det3(R)).toBeCloseTo(1, 9);
  });
});

describe('BVH', () => {
  it('closest point matches brute force on random queries', () => {
    const m = icosphere(3);
    const tris = triangulate(m).triangles;
    const bvh = TriangleBVH.build(m.positions, tris);
    const r = rng(5);
    const hit = makeHit(), brute = makeHit();
    for (let q = 0; q < 300; q++) {
      const x = r() * 3 - 1.5, y = r() * 3 - 1.5, z = r() * 3 - 1.5;
      bvh.closestPoint(x, y, z, Infinity, hit);
      brute.distSq = Infinity;
      for (let t = 0; t < tris.length / 3; t++) closestOnTriangle(m.positions, tris, t, x, y, z, brute);
      expect(hit.distSq).toBeCloseTo(brute.distSq, 12);
      expect(Math.abs(hit.u + hit.v + hit.w - 1)).toBeLessThan(1e-12);
    }
    // radius limit
    expect(bvh.closestPoint(5, 0, 0, 1, hit)).toBe(false);
  });

  it('raycast hits the expected surface and refit tracks moved vertices', () => {
    const m = icosphere(3);
    const tris = triangulate(m).triangles;
    const bvh = TriangleBVH.build(m.positions.slice(), tris);
    const hit = { tri: -1, t: 0, u: 0, v: 0, w: 0 };
    expect(bvh.raycast(0, 0, 5, 0, 0, -1, hit)).toBe(true);
    expect(5 - hit.t).toBeCloseTo(1, 1); // icosphere radius 1 (faceted)
    const scaled = m.positions.map((v) => v * 2);
    bvh.refit(scaled);
    expect(bvh.raycast(0, 0, 5, 0, 0, -1, hit)).toBe(true);
    expect(5 - hit.t).toBeCloseTo(2, 1);
  });
});

describe('sparse solver', () => {
  it('AMG-preconditioned CG solves a mesh Laplacian system to tolerance in few iterations', () => {
    const m = cubeSphere(30); // ~5.4k vertices
    const n = m.positions.length / 3;
    const adj = buildAdjacency(triangulate(m).triangles, n);
    const A = symmetricPattern(n, uniqueEdges(adj));
    for (let i = 0; i < n; i++) {
      for (let k = adj.offsets[i]; k < adj.offsets[i + 1]; k++) {
        const j = adj.neighbors[k];
        A.values[findEntry(A, i, j)] -= 50;
        A.values[findEntry(A, i, i)] += 50;
      }
      A.values[findEntry(A, i, i)] += 1e-3; // weakly anchored: very ill-conditioned
    }
    const amg = AMG.build(A);
    expect(amg.levelCount).toBeGreaterThan(1);
    const r = rng(2);
    const xTrue = Float64Array.from({ length: n }, () => r());
    const b = new Float64Array(n);
    spmv(A, xTrue, b);
    const x = new Float64Array(n);
    const res = pcg((v, o) => spmv(A, v, o), (rr, z) => amg.apply(rr, z), b, x, 1e-10, 200);
    expect(res.converged).toBe(true);
    expect(res.iterations).toBeLessThan(40);
    // Jacobi-PCG on the same system needs far more iterations
    const diag = Float64Array.from({ length: n }, (_, i) => A.values[findEntry(A, i, i)]);
    const x2 = new Float64Array(n);
    const res2 = pcg((v, o) => spmv(A, v, o), (rr, z) => { for (let i = 0; i < n; i++) z[i] = rr[i] / diag[i]; }, b, x2, 1e-10, 2000);
    expect(res2.iterations).toBeGreaterThan(res.iterations * 3);
  });

  it('dense Cholesky solves SPD systems and rejects indefinite ones', () => {
    const M = Float64Array.from([4, 1, 0, 1, 3, 1, 0, 1, 2]);
    const L = M.slice();
    expect(denseCholesky(L, 3)).toBe(true);
    const x = Float64Array.from([1, 2, 3]);
    denseCholeskySolve(L, 3, x);
    const y = [0, 1, 2].map((i) => M[i * 3] * x[0] + M[i * 3 + 1] * x[1] + M[i * 3 + 2] * x[2]);
    expect(y[0]).toBeCloseTo(1, 12);
    expect(y[1]).toBeCloseTo(2, 12);
    expect(y[2]).toBeCloseTo(3, 12);
    expect(denseCholesky(Float64Array.from([1, 2, 2, 1]), 2)).toBe(false);
  });
});
