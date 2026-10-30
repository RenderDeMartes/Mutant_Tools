# Meta Mutant: the MetaHuman rig on your own head

You have a **custom head** (scan, sculpt, another character) and a **MetaHuman DNA**. Meta Mutant
reshapes the MetaHuman head to your head while keeping its topology, writes a new DNA with the
updated neutral meshes and facial joints, builds the rig in Maya and transfers it (skin weights +
blendshapes) onto a copy of your head. Your eyes and teeth (with the tongue) can come along too.

```
 Maya ── 1 Prepare ──► mh_head_lod0.obj + custom_head.obj
                                │
 Browser ── 2 Wrap (TopoTransfer) ──► mh_head_lod0_wrapped.obj
                                │
 Maya ── 3 Apply ──► head_custom.dna ► rig ► <your head>_MH rigged
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
3. **Eyes** (optional): select your two eyeballs — the eye meshes, eye + cornea meshes, or the
   faces of each eye on your head mesh — then **Use selected**.
4. **Teeth** (optional): select your teeth, gums and tongue — meshes or faces — **Use selected**.
5. **Face regions** (optional, for cleaner lips and eyelids): open **▸ Face regions** and, for each of
   upper lip, lower lip, upper eyelids, lower eyelids, mouth bag and eye sockets, select its faces on
   your head and **Use selected**. See [Face regions](#face-regions).

Then the three steps, top to bottom (the next one is lit):

1. **Prepare** — **Export and open TopoTransfer**: writes the MetaHuman meshes from the DNA and your
   head (without the picked eyes / teeth) into the work folder, and opens TopoTransfer in the
   browser with both loaded.
2. **Wrap (browser)** — the MetaHuman head is the Base, your head the Reference; the eyes, teeth
   and lashes are set to Follow on their own.
   * **Align** → **Auto align** (uniform scale is on, so heads of any size match).
   * **Guides** (MetaHuman mode, Mirror on) → **Place guides**: the MetaHuman points are placed for
     you and a first guess of each is put on your head (both shown side by side, one colour per
     pair). Fix the wrong ones: click a dot on your head, then its right spot — on the character's
     left side (right of the screen), as with Mutant Tools guides; the other side follows. **Ctrl+Z**
     undoes. **Done**. Or turn **Claude** on and let Claude Code place them (see below).
   * **Fit** → check the result (0 flips) → **Keep result**.
   * **Brush** (optional): Move, Sculpt (Ctrl: in), Smooth and Relax (both stick back onto your
     head), Mirror for both sides; one undo per stroke.
   * **Export** → **Send to Maya**: the OBJ comes back on its own and step 2 turns green. Greyed
     out ("not listening") when the page was not opened from Maya; **Download** saves the file.
3. **Apply** — **Apply to my head**: fits the MetaHuman eyes and teeth onto yours, calibrates the
   DNA (`head_custom.dna`), builds the rig from it and rigs a copy of your head, `<your head>_MH`
   (and `<part>_MH` for eye / teeth meshes), right where your head is. Your meshes are not touched. **Apply again** replaces
   the earlier result.

**Check** on the face board beside your head: drag `CTRL_C_jaw` down (the jaw opens, lower teeth and
tongue follow), `CTRL_L_eye` / `CTRL_R_eye` (the eyes turn), the brow and mouth controls (your head
follows, eyes and teeth stay put).

Menus: **File** (open / change the work folder; by default `<project>/data/MetaMutant/<head>`),
**Epic Files** (the sample DNA: download, update, delete, open its folder) and **Help**.

## Eyes and teeth

| You pick | Meta Mutant |
| --- | --- |
| **Eyes**: eye meshes, eye + cornea, or faces of the head | every picked vertex is split into two eyes by position; each MetaHuman eyeball is moved and scaled onto the nearer one (least-squares sphere fit), the eye shell and eye edge follow; the eye joints move with them (skin-weighted calibration); your eye vertices are weighted like the MetaHuman eyeball, so they turn with `FACIAL_L/R_Eye` |
| **Teeth**: teeth, gums, tongue — meshes or faces | the MetaHuman teeth (with the tongue) and saliva are moved and scaled onto their box; the teeth joints follow; your teeth are weighted like the MetaHuman teeth (jaw, teeth, tongue joints) and, as their own meshes, get the teeth's tongue blendshapes |
| faces of the head mesh | left out of the TopoTransfer Reference (the wrap fits the skin, not the eyeballs) and kept still by the head's blendshapes |

## Face regions

Closest-point transfer bleeds where two surfaces touch: with the mouth closed, a point of your upper
lip can be closer to the MetaHuman's lower lip and then opens with the jaw; eyelids can stick the same
way. With regions picked (`mm_regions.py`):

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
| Calibrate DNA | writes `head_custom.dna`: new LOD0 neutral meshes; each `FACIAL_*` joint moves by the skin-weighted displacement of the vertices it drives (rotations kept, neck/body joints untouched); skin weights, blendshapes and behaviour copied |
| Build rig | `mm_rig.build`: joints (translate / jointOrient), LOD0 meshes with UVs, skinClusters and blendShapes from `head_custom.dna`; then the built joints are checked against the DNA math |
| Face board | the controls and their node network, beside your head (see below) |
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
w.prepare()        # then wrap in the browser (or: npx tsx scripts/wrap-cli.ts in Utils/TopoTransfer)
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
* Closest-point skin and blendshape transfer can bleed between lips or eyelids: pick the [face regions](#face-regions), or check and paint those areas.
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

Step 1 starts a small HTTP server inside Maya (`Utils/TopoTransfer/maya/tt_bridge.py`, standard
library only) that serves the bundled app and the two exported OBJs, and opens
`http://127.0.0.1:<port>/<token>/app/?base=…&reference=…&return=…`. Export POSTs the result back.
The Claude link uses `GET /<token>/claude/next` (long poll) and `POST /<token>/claude/reply`;
Claude Code sends commands with `POST /<token>/claude/call` (never from a browser page), finding the
open bridge through a file per bridge in `%TEMP%/topotransfer_claude` (removed when it stops). It listens on 127.0.0.1 only, behind a random per-open token; only the app's own origin is
accepted; the result must carry TopoTransfer's export header and the Base vertex count. The server
stops when the window closes or Maya quits.
