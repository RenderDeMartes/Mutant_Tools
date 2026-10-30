# Performance

All numbers below are **measured** with `npm run bench` (default wrap parameters: 4 levels × ≤ 6
iterations, bidirectional correspondences on). Machine: Windows 11, Node v24.16.0 (V8, the same
JavaScript engine as Chrome and Edge). Browser timings are of the same order but are not identical,
and depend on the machine.

Test case: Base = quad cube-sphere; Reference = icosphere with a stylised head shape applied
(different tessellation and vertex count), reference bounding-box diagonal ≈ 3.5 units.
Distances are measured from every Base vertex to the Reference surface (one-sided); coverage is
measured from Reference vertices to the Base surface.

| Base verts | Ref verts | Prep base | Prep ref | Fit | Total | Time / iteration | CG iterations / solve | Peak memory* | Mean distance before → after | Max after | Coverage after | Flipped | Topology preserved | Reference unchanged |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---:|---:|---:|:-:|:-:|
| 5,048 | 2,562 | 0.08 s | 0.01 s | 0.8 s | **0.9 s** | 32 ms | 4.8 | 19 MB | 7.57e-2 → 5.55e-4 | 9.96e-3 | 9.25e-4 | 0 | yes | yes |
| 25,352 | 40,962 | 0.27 s | 0.07 s | 4.0 s | **4.7 s** | 165 ms | 5.5 | 104 MB | 7.54e-2 → 2.02e-4 | 1.06e-2 | 2.07e-4 | 0 | yes | yes |
| 49,688 | 40,962 | 0.46 s | 0.06 s | 8.3 s | **9.5 s** | 347 ms | 5.8 | 101 MB | 7.54e-2 → 1.78e-4 | 8.97e-3 | 1.69e-4 | 0 | yes | yes |
| 99,848 | 163,842 | 0.84 s | 0.24 s | 19.9 s | **22.3 s** | 827 ms | 6.1 | 154 MB | 7.54e-2 → 1.64e-4 | 8.86e-3 | 1.48e-4 | 0 | yes | yes |

\* Peak JS heap + ArrayBuffer growth during the run, sampled every 20 ms and at each iteration
(an approximation). In the browser, add the main thread's copy of both meshes, the three.js GPU
buffers and the worker's copy: plan for roughly 2–3× the figure above.

"Topology preserved" compares a hash of the Base's face offsets and indices before and after and
checks the result has the same vertex count. "Reference unchanged" compares a hash of the
Reference's positions and faces before and after.

## Observations

* **Linear scaling.** Time per iteration grows linearly with vertex count; the number of conjugate
  gradient iterations per solve stays ~5–6 from 5k to 100k vertices because of the smoothed-
  aggregation multigrid preconditioner. With a Jacobi preconditioner the same systems need many
  times more iterations (see `tests/numerics.test.ts`).
* **Where the time goes** (100k, `npx tsx bench/profile.ts 100000`, also shown in the app's
  *Solver iterations* tab):

  | Stage | Share of loop time |
  | --- | ---: |
  | Forward closest-point correspondences (100k queries / iteration) | 32% |
  | Reverse correspondences (82k queries + BVH refit) | 24% |
  | Linear solve (multigrid-preconditioned CG) | 23% |
  | Local rotation fits | 7% |
  | Assembly | 5% |
  | Energy monitoring | 4% |
  | Multigrid coarse-operator update | 3% |

  Optimisations applied after the first benchmark: numeric-only Galerkin updates that reuse the
  sparsity pattern (multigrid update 2.5 s → 0.6 s per wrap), allocation-free 3×3 SVD, and
  warm-started closest-point queries. A surface-area-heuristic BVH was tried and gave no query
  speed-up (≈1.9 µs per near-surface query either way) at 5× the build cost, so it was not kept.
* **Next optimisation candidates:** spread closest-point queries over several workers (needs
  `SharedArrayBuffer`, i.e. cross-origin-isolation headers on the hosting server), and WebAssembly
  SIMD for the query and sparse kernels.
* **Not real-time.** A full wrap of a 100k mesh takes ~22 s; the UI stays responsive because the
  solver runs in a Web Worker, reports progress per iteration and can be cancelled between
  iterations (or terminated immediately if a single solve takes too long).
* **Above 100k vertices** the app works but warns at load time; time continues to scale roughly
  linearly (expect ~1 min at 250k with default settings — an extrapolation, not a measurement).

## Is a native / Python backend needed?

Not on current evidence: the design-target range (5k–100k) completes in 1–22 s locally without
uploads. The engine is isolated behind `GeometryEngine` (`src/engine/api.ts`), so a backend can be
added later without UI changes if measurements on real production meshes show a need (e.g. much
larger scans, or batch processing). WebAssembly/SIMD for the closest-point and sparse kernels would
be the first optimisation to try before introducing infrastructure.

## Default-parameter evidence

`npx tsx bench/sweep.ts` runs a parameter sweep on the example scene (9.6k-vertex Base). Measured
results that informed the defaults (mean / max distance after, in units of a ~2-unit-tall head):

| Variant | Mean after | Max after | Flipped |
| --- | ---: | ---: | ---: |
| smoothness 0.35 | 5.9e-4 | 2.5e-2 | 0 |
| **smoothness 0.25 (default)** | **3.0e-4** | **1.4e-2** | **0** |
| smoothness 0.15 | 1.7e-4 | 8.1e-3 | 0 |
| bidirectional correspondences off | 9.7e-4 | 5.1e-2 | 0 |
| local scaling off (pure ARAP) | 2.0e-3 | 3.4e-2 | 0 |

Lower smoothness fits more detail on clean synthetic data; 0.25 was chosen as a default that keeps
more of the Base's own surface character on noisy real scans. Reverse (reference→base)
correspondences and bounded local scaling each reduce the residual by 2–6×.
