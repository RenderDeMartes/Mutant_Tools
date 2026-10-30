# TopoTransfer

Topology-preserving non-rigid mesh fitting for character artists and rigging TDs.
TopoTransfer deforms a **Base mesh** (your production topology) onto a **Reference
mesh** (scan, sculpt, other character) while keeping the Base's vertex count,
vertex order, face indices and polygon connectivity exactly unchanged.

It runs entirely in the browser (React + TypeScript + three.js, geometry engine in a Web Worker).
This is the web architecture from the project brief; the earlier desktop (PySide6/VTK) plan was not
built. The engine is UI-independent, so other front ends can reuse it.

It runs entirely in the browser. Meshes, landmarks and settings never leave your
machine: there is no server, account, upload or telemetry.

## In Maya (Mutant Tools)

TopoTransfer lives in Mutant Tools (`Mutant_Tools/Utils/TopoTransfer`). In Maya:
**Mutant-Tools ▸ Misc ▸ TopoTransfer** opens a small window: **Base** (the topology to keep) and
**Reference** (the shape to match, optional), each with **Use selected** (the menu fills them from
the selection), and one button, **Send to TopoTransfer**. It exports both and opens the app with
them loaded; your Export comes back onto a copy of the Base, `<base>_topoTransfer` (same vertices,
UVs and faces). The app is bundled in `app/` and served by Maya — no
Node.js needed. After changing the web app, rebuild that copy with `npm run build:maya`.

`maya/` has the Maya side any Mutant tool can use: `tt_maya.py` (`send(base, reference)`: export,
open, apply the result), `tt_app.py` (find, start, open the app) and `tt_bridge.py` (hand meshes to
the app and take its export back). **Meta Mutant**
(`Utils/MetaMutant`, **Misc ▸ Meta Mutant**) uses them to put the MetaHuman rig on your own
head.

## Quick start (development)

Requirements: [Node.js](https://nodejs.org) 20 or newer (tested with Node 24), a desktop browser with WebGL 2
(Chrome, Edge or Firefox).

```bash
npm install
```

```bash
npm run dev
```

Open http://localhost:5173 and pick an example (**Human body**, **Human head** — CC0 meshes from
Blender Studio — or a synthetic head), or drag OBJ / PLY / STL files onto the window.

**Human bodies and faces are the primary target.** See [docs/HUMANS.md](docs/HUMANS.md) for the
CC0 human test data and measured results (≈1 mm surface error on a full body in ~4 s), and
**Meta Mutant** ([its README](../MetaMutant/README.md)) for custom MetaHuman heads — three steps:
*Prepare* in Maya (**Mutant-Tools ▸ Misc ▸ Meta Mutant**), *Wrap* here, *Apply* in Maya
(calibrates the DNA with Epic's DNA library, builds the rig and transfers it onto your head).

A production build (static files you can host anywhere, or open via `npm run preview`) is created
with:

```bash
npm run build
```

Other scripts:

| Command | What it does |
| --- | --- |
| `npm test` | Automated numerical, IO and integration tests (Vitest, ~10 s) |
| `npm run test:python` | Tests for the Maya link (`maya/`) and Meta Mutant (plain Python 3, no Maya needed) |
| `npx tsx scripts/wrap-cli.ts base.obj ref.obj out.obj` | Wrap without the browser (auto align with scale, default modes, the app's OBJ export) |
| `npm run serve` | Production build served locally on port 4173 |
| `npx tsx bench/profile.ts 100000` | Per-stage timing of one wrap |
| `npx tsx bench/human.ts` | Human body / head evaluation incl. ground-truth correspondence error |
| `npm run bench` | Performance benchmark at 5k / 25k / 50k / 100k vertices (`npm run bench -- 20000` for custom sizes) |
| `npm run examples` | Regenerates the reproducible example meshes in `examples/` |
| `npm run typecheck` | TypeScript type check |

## Workflow

The interface is a single guided sidebar with six steps; only the essentials are visible, the rest
sits behind **More** disclosures. The viewport toolbar holds display, visibility and colour modes;
the status bar shows progress and the latest message, and opens the Log / Mesh checks / Solver
drawer.

1. **Meshes** — a Base (OBJ or PLY, the topology to keep) and a Reference (OBJ, PLY or STL, the
   shape to match); drop files or pick an example. Set **Units** for millimetre read-outs. Validation
   findings show as a badge (details in *Checks*). **Parts** lists separate components: inner parts
   (eyes, teeth, tongue) default to *Follow* — not fitted, moved rigidly with the surrounding skin.
2. **Align** — **Auto align** (bounding boxes, then ICP; uniform scale on by default), or **From N
   guides** once ≥ 3 pairs exist. *Manual* has numeric move/rotate/scale and a gizmo (T / R / S).
3. **Guides** (optional) — both meshes side by side, one colour per pair. **Free** (click the Base,
   then the Reference; **Face set** / **Body set** ask for named points) or **MetaHuman** (the
   MetaHuman side is pre-placed and your side guessed; click a dot, then its spot). **Mirror**: only
   the character's left side is placed, the right follows. **Claude**: Claude Code places them
   through the Maya link (below). `Ctrl+Z` undoes a point.
4. **Fit** — two controls: **Detail** (smooth ↔ detailed) and **Quality** (Fast / Balanced / High).
   Run (`Ctrl+Enter`), check the result card and distance colours, then **Keep** or **Discard**.
   *Regions* (paint to protect or fit-only) and all solver settings are under More.
5. **Brush** (optional, after a kept fit; `G`) — **Move**, **Sculpt** (Ctrl: push in), **Smooth**
   and **Relax** (both projected back onto the Reference), **Mirror** across the Base's symmetry
   plane; `[` / `]` size; one undo per stroke; works on the clicked part only.
6. **Export** — OBJ, at the Reference position or the original Base position. **Send to Maya**
   when the page was opened from Maya (otherwise greyed out: open TopoTransfer from Mutant Tools,
   which opens the link), or **Download**. The written file is re-imported and its topology
   compared with the original first.

**Claude link** — with **Claude** on (only when opened from Maya), the page answers commands
(`state`, `capture`, `set_guides`; `src/claude/link.ts`) sent by Claude Code with
`python maya/tt_claude.py …` (or the Mutant Tools MCP's `topotransfer_*` tools, or
`tt_bridge.claude_call` in Maya). No API key, no Maya MCP listener needed.

Press `?` in the app for all shortcuts.

## Controls

| Control | Meaning |
| --- | --- |
| Detail | `1 − smoothness`: how much fine Reference detail the Base follows |
| Quality | Solver effort presets (3×4, 4×6, 6×10 levels × iterations) |
| Fitting strength | Pull of the surface fit relative to stiffness, landmarks and protected regions |
| Smoothness | Final stiffness. Low fits fine detail; high keeps the Base smoother/stiffer |
| Landmark influence | Multiplier on landmark weights (0 ignores landmarks) |
| Max distance | Correspondences farther than this (fraction of Reference size) are rejected |
| Iterations / level, Coarse-to-fine levels | Stiffness annealing schedule |
| Normal alignment / Normal threshold | Point-to-plane share; rejection of correspondences with disagreeing normals |
| Region influence | Strength of protected regions |
| Advanced | Bidirectional correspondences, open-boundary rejection, two-sided normals, seam lock, local scaling, solver tolerance |

Defaults produce a useful result on typical heads/bodies without touching anything.

## How it works

The solver is an ARAP-regularised non-rigid ICP with stiffness annealing, bidirectional
closest-point-on-surface correspondences, robust rejection, landmarks as soft constraints, and a
multigrid-preconditioned sparse solver. See [docs/ALGORITHM.md](docs/ALGORITHM.md) for the energy,
reasoning and **known limitations**.

## Performance

Measured on synthetic meshes (Node 24 / V8, same engine as Chrome/Edge), default parameters.
Full table and method in [docs/PERFORMANCE.md](docs/PERFORMANCE.md).

| Base vertices | Reference vertices | Total wrap time | Mean distance before → after | Flipped triangles |
| ---: | ---: | ---: | ---: | ---: |
| 5,048 | 2,562 | 0.9 s | 7.6e-2 → 5.6e-4 | 0 |
| 25,352 | 40,962 | 4.7 s | 7.5e-2 → 2.0e-4 | 0 |
| 49,688 | 40,962 | 9.5 s | 7.5e-2 → 1.8e-4 | 0 |
| 99,848 | 163,842 | 22.3 s | 7.5e-2 → 1.6e-4 | 0 |

Time grows roughly linearly with vertex count (the multigrid keeps solver iterations constant).
Wrapping is **not** real-time; the app shows an estimate (labelled as such) before long runs.

## Architecture

```
src/
  engine/            Geometry engine — pure TypeScript, no React / three.js / DOM
    core/            mesh representation, 3x3/4x4 math (SVD, polar, transforms)
    io/              OBJ (round-trip), PLY (ascii/binary, all properties), STL (reference only)
    geometry/        adjacency, normals, cotangent weights, validation
    spatial/         triangle BVH: closest point, ray cast, refit
    linalg/          CSR matrices, smoothed-aggregation multigrid, PCG, dense Cholesky
    alignment/       Umeyama, bounding-box, trimmed ICP (point-to-plane)
    landmarks/       landmark data, surface points, landmark alignment
    constraints/     region masks (paint, grow, smooth, protect / fit-only)
    wrapping/        parameters, precomputation, non-rigid solver
    validation/      distance metrics, mesh-quality report
    export/          topology-preserving export + verification
    synthetic/       deterministic test / example geometry
    api.ts           stable GeometryEngine interface
  worker/            Web Worker host + client implementing GeometryEngine (cancellable)
  state/             application state (zustand) and user actions, undo/redo
  ui/                React panels, three.js viewport controller, shortcuts
tests/               Vitest suites (numerical, IO, alignment, wrapping, export, integration)
bench/               benchmarks (synthetic, human ground truth), profiler, parameter sweeps
maya/                Maya side: tt_app (open the app), tt_bridge (hand meshes over, take the export back)
tools/               Blender export script
examples/            reproducible example meshes (generated by scripts/generate-examples.ts)
```

The UI only talks to `GeometryEngine` (`src/engine/api.ts`). A remote/Python backend could implement
the same interface later; the measurements so far do not show a need for one (see PERFORMANCE.md).
The engine has no browser dependencies and runs unchanged in Node, so it can be wrapped by DCC
adapters (e.g. via a Node/WASM bridge) in future.

## Supported data and what is preserved

| | OBJ | PLY | STL |
| --- | --- | --- | --- |
| As Base | yes | yes | no (no stored connectivity) |
| As Reference | yes | yes | yes |
| Polygons (quads / n-gons) | kept exactly | kept exactly | — |
| Export | round-trip: every non-`v`/`vn` line byte-identical (UVs, groups, materials, smoothing groups, lines, unknown records); normals recomputed with original indexing; vertex colours kept | same header, elements, property types and format; positions replaced, `nx/ny/nz` recomputed; all other properties kept | — |

Cross-format export (OBJ → PLY or PLY → OBJ) writes positions and polygons only and lists in the log
what could not be represented. `.mtl` files are referenced but not copied.

## Testing

`npm test` runs 81 tests (plus 46 Python tests via `npm run test:python`) covering: loading two meshes; rigid alignment recovering known
transforms (Umeyama, ICP, landmarks); wrapping onto differently tessellated references with
independently measured error reduction; landmarks moving a feature where closest points fail;
unchanged connectivity and an unmodified reference (hash checks); smoothness producing measurable
differences; protected and fit-only regions; open-boundary rejection; seam lock; cancellation;
eyeball-style inner components that follow instead of being flattened; useful errors for invalid input; export → re-import topology identity; and an end-to-end run on the
shipped example files.

## Privacy

All processing happens locally (Web Worker in your browser). The app makes no network requests
other than loading its own static files. Exports are saved through your browser's normal download.

## Licences

TopoTransfer's own code is part of Mutant Tools. The web app bundles react, react-dom, scheduler,
use-sync-external-store, zustand and three.js (all MIT); every build writes their licence texts to
`THIRD_PARTY_LICENSES.txt` next to the app. The human example meshes in `public/examples/human/` are
derived from Blender Studio's "Human Base Meshes" (CC0, see the `LICENSE.txt` there); the other
examples are synthetic. No Epic / MetaHuman files are included: bring your own DNA and modules
(see [Meta Mutant](../MetaMutant/README.md)).
