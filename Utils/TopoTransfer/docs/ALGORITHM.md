# TopoTransfer — Wrapping Algorithm

This document describes the non-rigid fitting method used by TopoTransfer, why it
was chosen, and where it is known to fail. It was written before the solver was
implemented and updated with measured behaviour afterwards.

## 1. Problem statement

Given

* a **Base mesh** with rest positions `X̄ ∈ R^{n×3}` (after rigid alignment) and
  fixed polygon connectivity, and
* a **Reference mesh** (any topology, any vertex count — never modified),

find new base positions `X` such that the base surface lies on the reference
surface where they overlap, while the base keeps a clean, undistorted surface.
Only `X` changes. Vertex count, vertex order, face indices and polygon
connectivity are never touched; this is enforced structurally (the solver never
receives or returns connectivity) and verified by tests.

## 2. Methods considered

| Method | Pros | Cons |
| --- | --- | --- |
| Nearest-vertex / closest-point snapping | trivial | no regularisation: folds, collapses, noise. Explicitly ruled out. |
| Laplacian (displacement) smoothing + closest point | linear, fast | not rotation invariant: bending a region distorts its detail. |
| Optimal-step NICP (per-vertex affine, Amberg 2007) | proven on faces, stiffness annealing | 12 unknowns/vertex (4× larger system), affine allows shear. |
| Embedded deformation graph (Sumner 2007) | small unknown count, good for large motions | nonlinear Gauss–Newton, needs a second stage to fit fine detail. |
| **ARAP-regularised non-rigid ICP (chosen)** | rotation invariant, preserves base detail, 3 unknowns/vertex, each step is a sparse SPD linear solve | resists local scale change (mitigated by similarity pre-alignment and annealing), alternating optimisation is a local method |

## 3. Chosen method: ARAP-regularised non-rigid ICP with stiffness annealing

### 3.1 Energy

For fixed correspondences the solver minimises

```
E(X, R) =  Σ_i  ŵ_i · c_i · [ (1-μ)‖x_i − p_i‖² + μ (n_i·(x_i − p_i))² ]          (fit, point-to-point / point-to-plane)
         + Σ_k  ŵ_k^rev · ‖Σ_j β_kj x_j − q_k‖²                                     (reverse fit: reference → base)
         + λ·n · Σ_i Σ_{j∈N(i)} w_ij ‖(x_i − x_j) − R_i (x̄_i − x̄_j)‖²             (ARAP stiffness)
         + Σ_l  ω_l · ‖Σ_j b_lj x_j − ℓ_l‖²                                        (landmarks)
         + Σ_i  π_i · ‖x_i − x_i⁰‖²                                                  (protected regions)
         + Σ_(i,j)∈seams  σ · ‖x_i − x_j‖²                                          (coincident-vertex seam lock)
         + ε Σ_i ‖x_i − x_i^prev‖²                                                  (Tikhonov, keeps system SPD)
```

* `p_i`, `n_i`: closest point on the reference surface to base vertex `i` and the
  interpolated reference normal there (BVH query, point-on-triangle, not
  nearest vertex).
* `ŵ_i = n·a_i/A · fitStrength`: per-vertex area weight (mean 1) so the result
  does not depend on mesh resolution.
* `c_i ∈ [0,1]`: robust correspondence weight (Tukey biweight of distance,
  times normal agreement). Correspondences are **rejected** (`c_i = 0`) when the
  distance exceeds *Maximum Correspondence Distance*, when normals disagree by
  more than the normal threshold, or when the closest point lies on a reference
  boundary (holes / open scan edges).
* Reverse terms: for (sub-sampled) reference vertices, the closest point on the
  current base surface, expressed with barycentric weights `β` on a base
  triangle. This pulls the base into regions no base vertex is closest to
  (protrusions, concavities) and is what prevents "partial coverage".
* `w_ij`: clamped cotangent weights computed on the rest shape.
* `R_i`: per-vertex best-fit rotation (local step), via 3×3 SVD. With *Allow local scaling*
  (default) `R_i` is a rotation times a uniform scale `s_i ∈ [1/s_max, s_max]` (bounded
  as-similar-as-possible), so regions can grow or shrink — proportions differ between scans — without
  fighting the stiffness, while shear and anisotropic stretch are still penalised.
* `λ`: stiffness. With the normalisation above, `λ ≈ fraction of surface area`
  over which a deformation feature is resisted — `λ=1` is near rigid,
  `λ=1e-3` allows features covering ~0.1% of the area.
* Landmarks: base side is a surface point (triangle + barycentrics) so landmarks
  need not sit on vertices.

### 3.2 Optimisation

Alternating (local/global) minimisation inside a non-rigid ICP loop:

```
for level in coarse → fine:               λ goes geometrically from λ_start to λ_end
    repeat `iterations` times (or until max |Δx| < tol):
        1. correspondences  (BVH closest point, filters, robust weights)
        2. local step       R_i = polar( Σ_j w_ij (x_i − x_j)(x̄_i − x̄_j)ᵀ )
        3. global step      solve  (S ⊗ I₃ + blockdiag(B_i)) x = b       (sparse SPD)
        4. diagnostics      NaN/Inf, solver residual, energy, displacement
```

The global step is a sparse symmetric positive-definite system with 3×3 blocks
(the point-to-plane term couples x/y/z per vertex). It is solved matrix-free with
**preconditioned conjugate gradients**, warm-started from the previous iterate.
The preconditioner is a **smoothed-aggregation algebraic multigrid V-cycle**
built on the scalar part of the operator. Without it, the stiff early levels
(`λ·n` large) would need thousands of CG iterations on 100k-vertex meshes because
Jacobi-type preconditioners cannot remove low-frequency error. Aggregates and
prolongators are built once per run from the mesh graph; Galerkin coarse
operators are rebuilt each iteration (values change), and the coarsest level is
solved with dense Cholesky.

### 3.3 Coarse-to-fine

"Coarse-to-fine levels" is **stiffness annealing** (λ from 0.1 down to `λ_end`) (as in optimal-step NICP):
early levels use high stiffness so only global, low-frequency shape changes are
possible (proportions, large-scale bending); later levels lower the stiffness so
progressively finer features are fitted. The multigrid hierarchy provides the
coarse *numerical* resolution. There is no separate decimated-mesh stage.

### 3.4 Multi-part meshes

Connected components of the Base get a mode. **Fit** components take part in the energy above.
**Follow** components (default for parts smaller than 25% of the largest) get no fit terms; after
the solve each is moved by the weighted least-squares similarity transform (Umeyama) that maps the
nearest fitted vertices from rest to result, so the part keeps its exact shape and its placement
relative to the surrounding surface. **Fixed** components keep their aligned rest positions.

## 4. Artist controls → parameters

| Control | Parameter |
| --- | --- |
| Fitting Strength | scales `ŵ` (fit vs. stiffness/landmarks/protection) |
| Deformation Smoothness | `λ_end = 10^(−4 + 3·s)`, `s ∈ [0,1]` |
| Coarse-to-Fine Levels | number of annealing levels |
| Iterations | max ICP iterations per level |
| Maximum Correspondence Distance | rejection radius, % of reference bounding-box diagonal |
| Normal Alignment | `μ` (point-to-plane share) and normal rejection angle |
| Landmark Influence | global multiplier on `ω` (per-landmark weights also apply) |
| Protected Regions / Region Influence | painted mask → `π_i` anchors to the start-of-wrap position and removes fit weight |

## 5. Failure detection

The solver does not claim to prevent every failure. It detects and reports:

* non-finite values (aborts, nothing is committed),
* linear solver not converging (warning with residual),
* energy increase across an iteration beyond tolerance (warning),
* too few accepted correspondences (alignment or max-distance problem),
* displacement larger than the reference size (aborts),
* after the fit: flipped faces (normal reversed relative to the locally rotated
  rest normal), collapsed triangles (area < 5% of rest), and over-stretched edges
  (length ratio outside [1/3, 3]).

## 6. Measured behaviour

* On the synthetic head benchmark the mean Base→Reference distance drops by ~99.8% at 5k–100k
  vertices with no flipped or collapsed triangles (docs/PERFORMANCE.md).
* Ablations on the example scene: disabling reverse correspondences increases the residual ~3×,
  disabling local scaling ~6× (pure ARAP cannot change proportions cheaply).
* An initial schedule starting at λ = 1 spent half the iterations making almost no progress
  (near-rigid), so the schedule starts at λ = 0.1.
* The multigrid-preconditioned CG needs ~5–6 iterations per solve at every tested size.
* `tests/wrap.test.ts` checks these properties numerically on every run.

## 7. Known limitations

* **Local method.** Needs a reasonable rigid alignment first; correspondences are
  closest points, so features that are far apart (e.g. a nose 3 cm lower) need
  landmarks.
* **ARAP resists local scale changes.** Large local volume changes are fitted by
  bending/stretching against the stiffness; lower the smoothness or add
  landmarks. Global scale is handled by the similarity alignment stage.
* **Thin parts / close sheets** (lips, eyelids, fingers): closest-point
  correspondences can jump to the wrong sheet. Normal rejection reduces this;
  landmarks and protected regions are the artist-level fix.
* **Inconsistent reference normals** (some scans) defeat normal rejection; turn
  on "two-sided normals" in that case.
* Self-intersections of the result are not detected.
* Polygons with more than four sides are fan-triangulated internally for
  closest-point queries and stiffness; the exported polygons are unchanged.
