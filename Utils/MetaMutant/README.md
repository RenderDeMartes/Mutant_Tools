# Meta Mutant: the MetaHuman rig on your own head

You have a **custom head** (scan, sculpt, another character) and a **MetaHuman DNA**. Meta Mutant
reshapes the MetaHuman head to your head while keeping its topology, writes a new DNA with the
updated neutral meshes and facial joints, builds the rig in Maya and transfers it (skin weights +
blendshapes) onto a copy of your head. Your eyes and teeth (with the tongue) can come along too.

```
 Maya ── 1 Pick points ──► points.json (optional)
                                │
 Maya ── 2 Prepare ──► mh_head_lod0.obj + custom_head.obj + guides.json
                                │
 Browser ── 3 Wrap (TopoTransfer) ──► mh_head_lod0_wrapped.obj
                                │
 Maya ── 4 Apply ──► head_custom.dna ► rig ► <your head>_MH rigged
```

New here? **Help ▸ Tutorial** (`tutorial/TUTORIAL.md`) walks through it with pictures.

**Maya 2026 only.** Everything it needs comes with Mutant Tools: TopoTransfer (served by Maya,
no Node.js) and Epic's `dna` module for Maya 2026 (`dna_module/Maya2026`, built from
[OpenRigLogic](https://github.com/EpicGames/OpenRigLogic), MIT). The rig is built by Meta Mutant
itself (`mm_rig.py`). The only thing you bring is a head DNA.

## Quick start

**Mutant-Tools ▸ Misc ▸ Meta Mutant** (select your head mesh first and it is filled in).

1. **Head DNA**: your MetaHuman's `.dna`, or **Get the sample DNA from Epic...** (Ada; see
   [Getting a DNA](#getting-a-dna)).
2. **Your head**: select it, **Use selected** (centimetres, Y up, neutral expression).

Then the four steps, top to bottom (the next one is lit):

1. **Pick points** — opens two views, see [Pick Points](#pick-points). **Skip** goes straight to step 2:
   TopoTransfer then guesses the points in the browser.
2. **Prepare** — **Export and open TopoTransfer**: writes the MetaHuman meshes from the DNA, your
   head (without the picked eyes / teeth) and your points into the work folder, and opens TopoTransfer
   in the browser with them loaded.
3. **Wrap (browser)** — the MetaHuman head is the Base, your head the Reference; the eyes, teeth
   and lashes are set to Follow on their own.
   * With points from Maya the head is already aligned from them and every guide is placed: go to **Fit**.
     To change a guide, drag its dot.
   * Without them: **Align** → **Auto align** (uniform scale is on, so heads of any size match), then
     **Guides** (MetaHuman mode, Mirror on) → **Place guides**: the MetaHuman points are placed for
     you and a first guess of each is put on your head (both shown side by side, one colour per
     pair). Fix the wrong ones: click a dot on your head, then its right spot — on the character's
     left side (right of the screen), as with Mutant Tools guides; the other side follows. **Ctrl+Z**
     undoes. **Done**. Or turn **Claude** on and let Claude Code place them (see below).
   * **Fit** → check the result (0 flips) → **Keep result**.
   * **Brush** (optional): Move, Sculpt (Ctrl: in), Smooth and Relax (both stick back onto your
     head), Mirror for both sides; one undo per stroke.
   * **Export** → **Send to Maya**: the OBJ comes back on its own and step 2 turns green. Greyed
     out ("not listening") when the page was not opened from Maya; **Download** saves the file.
4. **Apply** — **Apply to my head**: fits the MetaHuman eyes and teeth onto yours, calibrates the
   DNA (`head_custom.dna`), builds the rig from it and rigs a copy of your head, `<your head>_MH`
   (and `<part>_MH` for eye / teeth meshes), right where your head is. Your meshes are not touched. They are only hidden, so they do not stand still inside the moving copies. **Apply again** replaces
   the earlier result.

**Face + board view** (on the green panel at the end) turns Maya's viewport into two panels: your face on the left, the
face board on the right, each through its own camera (`metaMutant_faceCam`, `metaMutant_boardCam`). **One view** goes back.

**Check** on the face board beside your head: drag `CTRL_C_jaw` down (the jaw opens, lower teeth and
tongue follow), `CTRL_L_eye` / `CTRL_R_eye` (the eyes turn), the brow and mouth controls (your head
follows, eyes and teeth stay put).

Steps 1 and 2 first check that your meshes have a scale of 1, their parents' scale included. If not, they
ask to freeze them (nothing moves, Ctrl+Z brings it back). A mesh with a deformer, a locked or connected
scale or from a reference cannot be frozen there: fix it first, or go on as it is.

Menus: **File** (open / change the work folder; by default `<project>/data/MetaMutant/<head>`),
**Epic Files** (the sample DNA: download, update, delete, open its folder) and **Help**.

## Pick Points

Two panels: the MetaHuman on the left, your head on the right. Both look through one camera, so tumbling
either moves both. The MetaHuman is already marked and cannot be selected; you only pick on your head, on a
copy of it (your mesh is not touched; picks are stored with its name). Everything leaves the scene when
the window closes, and each pick is saved at once, so you can stop and come back. While it is open the two
heads also show, one over the other, in your other viewports.

| Tab | You pick | What it does |
| --- | --- | --- |
| **Points** | one vertex each, asked for in order: click it and the next is asked for. **Mirror L to R** fills each right point from its left one, for symmetric heads | exact pairs for the wrap, and the alignment |
| **Lines** | the most important picks. Double click an edge of the loop where the lips meet, **Use selected**: it splits at its corners into the upper and lower line. The same for the edge of each eye opening. Or select each line alone, corner to corner | matched to the MetaHuman's same line by arc length (lips: each side of the midline on its own), giving many pairs exactly where closest-point wrapping fails. They also decide the [skin and blendshapes](#lips-and-eyes) around them |
| **Regions** | optional: faces of the lips, eyelids, mouth bag, eye sockets, to correct what the lines say | see [Face regions](#face-regions) |
| **Eyes & teeth** | your meshes (they show in this tab), or faces of the head | see [Eyes and teeth](#eyes-and-teeth) |

**Sphere size** sets the markers of the points. The two heads line up better with each point you pick.

Stored in `<work>/points.json` and the settings. Step 2 turns them into `guides.json` for TopoTransfer, reading
the positions again from your head in case it moved. Points picked on other topology are dropped.

## Lips and eyes

Closest point does not know which side of a lip a vertex is on. Inside the mouth or in a fold under the brow it jumps
between surfaces: lips stay stuck across an open mouth, lids crumple. So with lines picked, each vertex near them
gets coordinates on both heads (`mm_zones.py`): outside or inside the closed line, upper or lower, how far along it,
how far from it along the surface. A vertex of your head takes its skin weights and blendshapes from the MetaHuman points
with the same coordinates. The whole inside of the mouth and sockets goes this way; on the skin it blends back into
closest point away from the line. At the mouth, your line pairs only with the part of the MetaHuman's where its lips really
part: further out its upper and lower line are one crease of skin, and your lips would stay stuck together that far. The same zones lock the wrap's regions, so nothing else has to be picked.

Then, with the rig moving, Apply corrects what depends on your head's proportions (`mm_fixes.py`, needs the face board):

| Setting | What it does |
| --- | --- |
| `close_eyelids` | in the blink pose, measures what your lids still lack to meet as the MetaHuman's do, with the upper riding slightly over the lower and the lids kept out of your eye meshes. Stored as a blendShape target per eye (`mmFix_lidClose_L/R`) driven by the MetaHuman's `eye_blink_L/R` |
| `fit_teeth` | teeth modelled close behind the lips come through them when the lips press back. Moves the rigged copy (`<teeth>_MH`) back, both arches alike so the bite stays, as little as keeps it behind the skin seen from the front in the mouth's poses. What still comes through the cheeks when the jaw opens, it narrows. It logs by how much. Your own teeth mesh is not touched |

Both are on by default; set them in `<work>/meta_mutant.json`.

Measured on a stylised head (Ada wrapped onto it, picks made carefully, face board poses):

| | Closest point, regions picked by hand | With lines and fixes | MetaHuman |
| --- | --- | --- | --- |
| Eye centre sliding as it looks around, worst (eye radius 4) | 1.27 | 0 | |
| Upper teeth moving with the jaw | yes | 0 | |
| Lowest lip gap with the jaw open (below 0: lips cross) | -1.28 | 1.18 | 0.00 (its crease) |
| Mean lid gap at full blink (below 0: the upper lid rides over the lower) | 0.23 | -0.41 | -0.20 |
| Teeth through the skin, worst of jaw / smile | 1.42 | 0 | |
| Flipped faces in the wrap | 14 | 2 | |

## Eyes and teeth

| You pick | Meta Mutant |
| --- | --- |
| **Eyes**: eye meshes, eye + cornea, or faces of the head | every picked vertex is split into two eyes by position; each MetaHuman eyeball is moved and scaled onto the nearer one (sphere fit of the back half: the iris dent and the cornea's bulge are in front); `FACIAL_L/R_Eye` and the lid pivots move onto the centre of your eye, and the rig's small translations of the eye joint are removed, so the eye turns about its centre; the eye shell and eye edge follow; your eye vertices are weighted like the MetaHuman eyeball |
| **Teeth**: teeth, gums, tongue — meshes or faces | each connected piece goes whole to the upper or lower arch, by height (a piece as long as the arches, narrower and in the middle, is the tongue). Each MetaHuman arch is moved and scaled onto yours, the teeth joints and the tongue follow. Upper teeth follow `FACIAL_C_TeethUpper` and lower teeth `FACIAL_C_TeethLower`, whole; a tongue is weighted like the MetaHuman's. As their own meshes they get the teeth's tongue blendshapes |
| faces of the head mesh | left out of the TopoTransfer Reference (the wrap fits the skin, not the eyeballs) and kept still by the head's blendshapes |

## Face regions

Closest-point transfer bleeds where two surfaces touch: with the mouth closed, a point of your upper
lip can be closer to the MetaHuman's lower lip and then opens with the jaw; eyelids can stick the same
way. The [lines](#lips-and-eyes) solve this on their own; regions picked in [Pick Points](#pick-points) correct them, and act twice.

In the wrap (`Lock regions` in TopoTransfer's Guides; lips, eyelids and mouth bag): a MetaHuman vertex of one
region may land on its own region or on free skin, never on another region.

In the rig transfer (`mm_regions.py`):

| Region | Skin weights and blendshapes come from |
| --- | --- |
| upper lip, lower lip, upper eyelids, lower eyelids, mouth bag | the same region of the MetaHuman only |
| eye sockets | the MetaHuman's face around the eye (never its lids, lips or mouth); kept still by the blendshapes |
| the rest of your head | the MetaHuman outside the regions you picked |

The MetaHuman's regions are found on their own from its skin (`FACIAL_*_LipUpper*`,
`*_EyelidLower*`, `*_MouthInterior*`… weighing at least 0.35). Pick generously: a few faces too many
at a border do no harm. The mouth bag is matched, not frozen, so it opens with the jaw instead of
poking through the lips.

## Getting a DNA

A MetaHuman head DNA already contains the meshes of every LOD (head, teeth, eyes, lashes… with UVs),
the joints, skin weights, blendshapes and RigLogic behaviour — step 1 exports the meshes from it.

* **Your own MetaHuman**: create it in **MetaHuman Creator** (inside Unreal Engine from UE 5.6) and
  export it for Maya (the **MetaHuman for Maya** plugin on Fab) to get the head `.dna`.
* **Epic's sample (Ada)** and **Epic's face board** (`gui.ma`, used for the controls): **Get the
  sample DNA from Epic...** shows Epic's licence and downloads only after you tick **I accept**, straight from Epic's
  [MetaHuman-DNA-Calibration](https://github.com/EpicGames/MetaHuman-DNA-Calibration) into
  `<Maya user folder>/MetaMutant/epic` (outside Mutant Tools), about 70 MB. Once downloaded, an
  empty Head DNA is filled in with it whenever the window opens.

MetaHuman characters are covered by Epic's MetaHuman licence (since June 2025 also usable outside
Unreal, in other engines and creative software). Don't commit DNA files, MetaHuman meshes or
MetaHuman-DNA-Calibration to a public repository: its licence (section 1) does not allow
distributing it. OpenRigLogic (the bundled `dna` module) is MIT.

## What Apply does

| Part | What happens |
| --- | --- |
| Import preview | finds `mh_head_lod0_wrapped*.obj` newer than step 1 with the right vertex count, copies it into the work folder, imports it as `tt_wrapped_preview` on your head |
| Fit eyes and teeth | `mm_core.fit_parts`, in DNA space (through the alignment TopoTransfer exported) |
| Pivots | `mm_core.pivot_deltas`: a joint usually moves by the average of its vertices, wrong for what the face rotates about. The eye joints and lid pivots go to your eye's centre (the lids' turn is scaled by the ratio of the eye sizes, so they travel as far as designed); the jaw hinge (`FACIAL_C_Jaw`, `FACIAL_C_LowerLipRotation`) moves with the skin beside it |
| Calibrate DNA | writes `head_custom.dna`: new LOD0 neutral meshes; each `FACIAL_*` joint moves by the skin-weighted displacement of the vertices it drives (rotations kept, neck/body joints untouched); skin weights, blendshapes and behaviour copied |
| Build rig | `mm_rig.build`: joints (translate / jointOrient), LOD0 meshes with UVs, skinClusters and blendShapes from `head_custom.dna`; then the built joints are checked against the DNA math |
| Face board | the controls and their node network, beside your head (see below) |
| Lines | with lines picked, the pairs below follow them around the lips and eyes (see [Lips and eyes](#lips-and-eyes)) |
| Transfer rig | duplicates your head as `<your head>_MH` (and eye / teeth meshes as `<part>_MH`), moves the copies into DNA space, binds them to the same joints, copies skin weights (closest point; eyes and teeth from their MetaHuman meshes) and gives it every blendshape: each vertex takes the delta of the closest point on the MetaHuman mesh, written straight into a blendShape node driven by the MetaHuman weights; then the whole rig (`metaMutant_rig`) is moved back onto your head with TopoTransfer's alignment, so everything sits where your meshes are |

No RigLogic plugin (Epic ships none for Maya 2026): the **face board** (`mm_faceboard.py`, setting
`face_board`) rebuilds RigLogic's behaviour from `head_custom.dna` with Maya's own nodes, so the scene
opens in any Maya 2026. **Epic's own MetaHuman board** is used when it is in your Epic download
(`data/mh4/gui.ma`, fetched with the sample DNA by **Epic Files ▸ Download the sample DNA...**; never
shipped with Mutant Tools): Meta Mutant imports it, drops its neck setup (it needs Epic's RBF plugin,
which Maya 2026 does not have, and RigLogic) and connects its controls. Without it, Meta Mutant draws
its own board: its 161 MetaHuman-named controls (`CTRL_L_brow_down`, `CTRL_C_jaw`, …) sit
like a face (brows, eyes, nose, mouth, jaw, tongue, neck; the character's right on the left, as seen
from the front), each in a frame of its range with its name under it. Every control moves the way its
joints do: where a control's value moves the face down (jaw open, blink, brow down) or to the other
side, its frame is drawn flipped, so dragging down moves the face down; the values stay the MetaHuman
ones. The controls go
through set-driven-key curves (control ranges), clamps and multiply nodes (correctives) into the
MetaHuman blendshape weights and into a hidden curve (`metaMutant_faceDriver`): one blendShape target
per control holds its joint moves, and `curveInfo` feeds the summed points to the joints. It matches
RigLogic's math (`mm_face.py`) to 0.00001°; moving a control re-evaluates in about 30 ms. The face
joints are driven by it: animate the controls, not the joints. Not included: wrinkle maps (animated
maps).

Defaults (edit `<work folder>/meta_mutant.json` or set them on `mm_controller.Workflow`):
`joints` (`FACIAL_`), `backend` (`auto`), `lower_lods` (true), `blendshapes` (true).

## Scripting

```python
import sys; sys.path.append(r"C:/…/Mutant_Tools/Utils/MetaMutant")
import mm_controller, mm_workflow as wf
w = mm_controller.Workflow(wf.Settings(dna_path=r"C:/mh/head.dna", work_dir=r"C:/work", custom_mesh="myHead",
                                       eyes=["eyeL", "eyeR"], teeth=["teeth"]))
w.prepare()        # then wrap in the browser (or: npx tsx scripts/wrap-cli.ts base ref out [guides.json] in Utils/TopoTransfer)
w.apply_all()
```

`mm_dna.py` also runs from the command line (`export`, `calibrate`). Tests:
`python -m unittest discover -s tests` in this folder (no Maya needed).

## Limitations

* Joint placement is a geometric estimate (skin-weighted). Joints that follow bone rather than skin
  (jaw pivot) may need manual correction for heads very different from the MetaHuman.
* Blendshape deltas are kept as they are; on heads much larger or smaller than the MetaHuman they
  do not scale with the face.
* The `writer` backend (no DNACalib) leaves lower LODs in the original shape.
* Pick Points finds lines by the head looking along +Z, Y up: lines are ordered by X and split at their corners by X.
* `fit_teeth` only looks at the jaw and smile poses; another expression could still bring the teeth through.
* A head whose lip line cannot be picked as one line (no such edge loop) falls back to closest point there.
* Jaw selection is not there yet: the jaw joint is still the skin-weighted estimate.
* Teeth picked as faces of the head get the teeth's skin but not the tongue blendshapes (pick them as their own mesh for those).
* Head DNA only; neck/body joints are not moved by default.

## Claude places the guides (optional)

With **Claude** on in the Guides step, Claude Code can read and place the guides: ask it to "place
the guides in TopoTransfer". It talks to the page through TopoTransfer's own link
(`Utils/TopoTransfer/maya/tt_claude.py`: `state`, `capture` (a picture of your head from the front /
left / right, zoomed on a guide, guides drawn on it), `set_guides` (from pixels of those
pictures)); the Mutant Tools MCP has the same as `topotransfer_*` tools. Maya's MCP listener is not
needed. No API key: it is your Claude Code session.

## Local link (Maya ↔ browser)

Step 2 starts a small HTTP server inside Maya (`Utils/TopoTransfer/maya/tt_bridge.py`, standard
library only) that serves the bundled app, the two exported OBJs and the guides, and opens
`http://127.0.0.1:<port>/<token>/app/?base=…&reference=…&guides=…&return=…`. Export POSTs the result back.
The Claude link uses `GET /<token>/claude/next` (long poll) and `POST /<token>/claude/reply`;
Claude Code sends commands with `POST /<token>/claude/call` (never from a browser page), finding the
open bridge through a file per bridge in `%TEMP%/topotransfer_claude` (removed when it stops). It listens on 127.0.0.1 only, behind a random per-open token; only the app's own origin is
accepted; the result must carry TopoTransfer's export header and the Base vertex count. The server
stops when the window closes or Maya quits.
