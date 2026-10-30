# Human bodies and faces

Human bodies and faces are TopoTransfer's primary target. This page covers the bundled CC0 human
test data, measured results, and what to do (and what is still missing) for production characters
such as custom MetaHumans.

## Test data (CC0)

All human example meshes come from Blender Studio's **Human Base Meshes** bundle v1.4.1, released
under **CC0 1.0** (public domain) — https://www.blender.org/download/demo/ . They ship with the app
in `public/examples/human/` and are available from **Examples ▸ Human body / Human head**.

| File | Role | Contents |
| --- | --- | --- |
| `body_male_base.obj` | Base | Realistic male body cage, 10,582 vertices, quads + UVs, plus two eyes as separate parts (Follow) |
| `body_female_sculpt_ref.ply` | Reference | Realistic female body sculpt (Multires level 2), 169,362 vertices, float32 |
| `body_female_cage_groundtruth.obj` | Evaluation | Female body cage with **the same vertex order as the male cage** — a ground-truth correspondence |
| `head_anim_base.obj` | Base | Animation-topology realistic head (3,242 v) + sclera and iris parts (Follow) |
| `head_sculpt_ref.ply` | Reference | Sculpting-topology realistic head (different topology), Multires level 1, 13,212 vertices |

### Regenerating them

The source is a `.blend`. The export is reproducible with Blender 4.2 LTS (portable zip is fine):

```bash
blender -b human_base_meshes_bundle.blend --python tools/blender_export_meshes.py -- third_party/human-obj
```

```bash
blender -b human_base_meshes_bundle.blend --python tools/blender_export_meshes.py -- third_party/human-obj "body_(male|female)_realistic$|head_(sculpting|animation)_realistic$" 2
```

```bash
npx tsx scripts/prepare-human-examples.ts
```

(the second command evaluates Multires at level 2 for the high-resolution references; the export
script writes vertices in original order, without triangulating, converting Z-up to Y-up.)
`third_party/` is git-ignored.

## Measured results

`npx tsx bench/human.ts` (Node 24, defaults unless stated; rigid pre-alignment = Auto bounds without
scale, then ICP; same as the app workflow):

| Case | Surface distance after (mean / p95 / max) | Ground-truth correspondence error (mean / p95) | Flipped | Time |
| --- | --- | --- | ---: | ---: |
| Male body cage → female sculpt (169k) | 1.3 / 4.0 / 14.1 mm | 6.9 / 20.9 mm (from 42.0 mean) | 0 | 3.9 s |
| same, smoothness 0.15 | 1.0 / 3.3 / 11.4 mm | 7.0 / 21.1 mm | 0 | 3.7 s |
| same + 24 sparse landmarks | 1.1 / 3.0 / 13.3 mm | **4.2 / 14.8 mm** | 0 | 3.4 s |
| Animation head (+eyes Follow) → sculpt head | 0.19 / 0.69 / 1.79 mm | — (different topology) | 0 | 1.1 s |

How to read this:

* **Surface distance** says the result lies on the reference. It is already at the millimetre level.
  The remaining maxima on the body are on the face, fingers and chest, where the 10k-vertex body
  cage simply has too few vertices to represent the sculpt's detail.
* **Correspondence error** says whether each vertex landed on the *semantically right* spot (a nose
  vertex on the nose, a knuckle vertex on the knuckle). Surface fitting alone lets vertices slide
  along the surface; landmarks reduce sliding by ~40% here. For rigged / animation topology this is
  the number that matters most.
* Inner parts (eyes, sclera, iris) default to **Follow** and keep their exact shape.

## Recommended workflow for bodies and heads

1. Base = your production topology (OBJ/PLY, any vertex count up to ~100k), with eyes/teeth/tongue
   as separate parts. Check **Base parts**: the skin should be *Fit*, inner parts *Follow*.
2. Reference = scan / sculpt / other character, in the same units. Clean scans first (remove
   floaters, fill large holes or leave them open — open boundaries are rejected automatically).
3. Align: **Auto (bounds)** with *Allow uniform scale* **off** when both are real-world scale, then
   **ICP refine**. If the poses or proportions differ a lot, place ≥ 3 landmarks and use
   **From landmarks** instead.
4. Landmarks: **Landmarks ▸ Preset ▸ Face** (32 named points: brow, nasion, nose tip/alae, eye
   corners and lids, mouth corners and lips, chin, jaw angles, cheekbones, ears) or **Body** (40
   points: head, neck, shoulders, nipples, navel, joints, fingertips, hips, knees, ankles, heels,
   toes). Guided placement prompts each point with an anatomical hint — click it on the Base, then on
   the Reference; **Skip** points that are not visible. Place one side of each L/R pair and press
   **Mirror L↔R**: the counterparts are mirrored across each mesh's symmetry plane, which is fitted
   automatically (reflect + rigid ICP + PCA of mirror pairs) so it also works on scans that are not
   axis-aligned.
5. Wrap with defaults; lower **Smoothness** (0.1–0.2) for more surface detail; check the distance
   colours and the flip/stretch counters; commit; export OBJ in *Original base space* if the result
   must stay in the base's coordinate system.

## Custom MetaHumans

The full pipeline — export the MetaHuman meshes from a DNA, wrap them to a custom head here,
calibrate the DNA (neutral meshes + facial joints) with Epic's DNACalib, and transfer the rig onto
the custom mesh in Maya — is **Meta Mutant**, documented in
[Utils/MetaMutant/README.md](../../MetaMutant/README.md).

### Parameter sweep (sliding vs. solver effort)

`npx tsx bench/human.ts sweep`, body case, ground-truth correspondence error (mean):

| Variant | GT error | Time |
| --- | ---: | ---: |
| defaults (4 levels × 6) | 6.9 mm | 4.0 s |
| point-to-plane 0.6 | 6.0 mm | 4.4 s |
| 6 levels × 10 | **5.2 mm** | 7.5 s |
| 6 levels × 20 | 6.4 mm | 13.3 s |
| no local scaling | 10.0 mm | 3.8 s |
| 24 landmarks (defaults) | **4.2 mm** | 3.4 s |

More stiff-level iterations help up to a point; beyond that, extra fine-level iterations let
vertices slide further. Landmarks remain the most effective lever, hence the presets and mirroring.

### Still missing for production-grade human fitting (planned work)

* **Symmetry**: optional left/right symmetric deformation for symmetric bases.
* **Correspondence quality**: reduce sliding without landmarks (e.g. feature-aware weighting near
  high curvature, or a semantic pre-registration pass); measured against the ground-truth pair
  above.
* **Thin parts** (fingers, lips, eyelids): sheet-aware correspondence rejection beyond the normal
  threshold.
* **Multi-component references** (scans with separate eyes or clothing pieces).
