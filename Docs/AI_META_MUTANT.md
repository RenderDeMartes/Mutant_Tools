# Meta Mutant: guide for an AI assistant

You are helping an artist on a computer where Mutant Tools is installed as a Maya tool. There may be no
repository, no project open in your editor, and no system Python. Find what you need as below. Do not assume
paths, ports or mesh names: they differ on every computer.

Meta Mutant moves Epic's MetaHuman face rig onto a custom head in Maya 2026. Artist's tutorial:
<https://mutanttools.com/meta-mutant/>

## 1. Find the install

The folder is `Mutant_Tools`, inside Maya's scripts folder. A computer can hold old copies for other Maya
versions, without Meta Mutant. Take the first one that has both marker files, newest Maya first:

```python
import glob, os
home = os.path.expanduser('~')
roots = [os.environ.get('MAYA_APP_DIR', ''), os.path.join(home, 'Documents', 'maya'),
         os.path.join(home, 'OneDrive', 'Documents', 'maya'), os.path.join(home, 'maya'),
         os.path.join(home, 'Library', 'Preferences', 'Autodesk', 'maya')]
found = [p for r in roots if r for p in sorted(glob.glob(os.path.join(r, '*', 'scripts', 'Mutant_Tools')), reverse=True)
         if os.path.isfile(os.path.join(p, 'Utils', 'MetaMutant', 'mm_controller.py'))
         and os.path.isfile(os.path.join(p, 'Dev', 'MayaMCP', 'bridge_transport.py'))]
print(found)
```

Below, `<MT>` is that folder. Found nothing? Ask the artist to run this in Maya's Script Editor (Python tab) and
send you the result:

```python
import Mutant_Tools; print(Mutant_Tools.__file__)
```

If that fails too, Mutant Tools is not installed, or is too old to have Meta Mutant: send the artist to
<https://mutanttools.com/free-maya-rigging-tools/#install>.

**Python:** use `python` if it exists. If not, use Maya's own, which is enough for everything here:
`C:/Program Files/Autodesk/Maya2026/bin/mayapy.exe`. Meta Mutant's DNA module ships for Windows only.

## 2. Connect to the open Maya

Ask the artist to open Maya 2026 with their scene, then start the bridge. Either the **MCP** menu in the Mutant
Tools window, **Start Bridge**, or in the Script Editor:

```python
from Mutant_Tools.Dev.MayaMCP import maya_listener; maya_listener.start_bridge()
```

It only listens on this computer. It runs any code you send it inside the artist's session, so check the scene before
changing anything. To find its port (several Mayas: ask which one, the scene name is listed):

```
python -c "import sys; sys.path.insert(0, r'<MT>/Dev/MayaMCP'); import bridge_transport as b; print(b.list_sessions())"
```

Run code in Maya with a file, or `-c` for one line. Files avoid quoting trouble:

```
python "<MT>/Dev/MayaMCP/run_in_maya.py" your_script.py --port <port> --timeout 600
python "<MT>/Dev/MayaMCP/run_in_maya.py" -c "import maya.cmds as c; print(c.file(q=True, sn=True))" --port <port>
```

- `print` what you need to see: stdout and tracebacks come back. Each call is its own run, with its own variables.
  Functions in a script cannot see that script's top-level names.
- Selection-changed events and `evalDeferred` only fire between calls, not during one.
- First check: `cmds.about(version=True)` must be 2026. Meta Mutant needs Maya 2026.
- Optional, typed tools instead of scripts: `pip install "mcp>=2.0,<3"`, then
  `claude mcp add mutant-maya -- python "<MT>/Dev/MayaMCP/mcp_server.py"`. See `<MT>/Dev/MayaMCP/README.md`.

## 3. What to read

| For | Read |
|---|---|
| The whole workflow, every setting, limits | `<MT>/Utils/MetaMutant/README.md` |
| The steps as an artist sees them | `<MT>/Utils/MetaMutant/tutorial/TUTORIAL.md` |
| The window | `<MT>/UI/MetaMutant/load_meta_mutant.py`, `load_point_picker.py` |
| Steps and their order, no UI | `<MT>/Utils/MetaMutant/mm_controller.py` |
| Calibration, joints moved, pivots, teeth arches | `mm_core.py`, `mm_dna.py` |
| Rig and face board built in Maya | `mm_rig.py`, `mm_faceboard.py`, `mm_face.py` |
| Skin, blendshapes, materials on your head | `mm_maya.py` |
| Lip and eyelid pairing | `mm_points.py`, `mm_zones.py`, `mm_picker.py` |
| Corrections after Apply: lids, teeth | `mm_fixes.py` |
| Fitting tool in the browser | `<MT>/Utils/TopoTransfer/README.md`, `maya/tt_claude.py` |

The `mm_*` files are in `<MT>/Utils/MetaMutant`. Tests are in its `tests` folder, and need no Maya:
`python -m unittest discover -s tests`, run from `Utils/MetaMutant`.

## 4. Where the data is

The work folder of a head holds all its files. Ask Maya for it:

```python
import maya.cmds as cmds
print(cmds.optionVar(q='metaMutant_workDir') if cmds.optionVar(exists='metaMutant_workDir') else 'never opened here')
```

A new head defaults to `<Maya project>/data/MetaMutant/<head>`.

| File | Holds |
|---|---|
| `meta_mutant.json` | Settings: DNA path, head mesh, eye and teeth meshes |
| `points.json` | The picks: 30 points and 6 lines, as vertex ids |
| `guides.json` | The picks as TopoTransfer loads them |
| `mh_head_lod0.obj`, `custom_head.obj` | What goes to TopoTransfer: MetaHuman, your head |
| `mh_head_lod0_wrapped.obj` | The fit from TopoTransfer |
| `head_custom.dna` | The calibrated rig data |

Epic's download, when the artist used it, is in `<Maya user folder>/MetaMutant/epic`.

In the scene: `<head>_MH`, `<part>_MH` (rigged copies), `metaMutant_rig`, `metaMutant_faceBoard`, controls `CTRL_*`,
joints `FACIAL_*`, cameras `metaMutant_faceCam` and `metaMutant_boardCam`. `head_lod0_mesh` is the hidden MetaHuman that
drives the rig: compare against it.

## 5. Drive it

```python
from Mutant_Tools.UI.MetaMutant import load_meta_mutant as mm
win = mm.open_window()            # the last work folder. open_window('Head') starts that head's folder in the project
win.use_work_dir(r'<folder>')     # or go to the folder of section 4
win.workflow.status()             # which steps are done
win.workflow.prepare()            # export, then open TopoTransfer in their browser
win.workflow.apply_all()          # calibrate, build rig, transfer, board, corrections
```

Picking points is built for the artist's clicks in the window. Placing guides from the page: the page must be open with
**Claude** on in its Guides step, then `tt_claude.py state`, `capture`, `set_guides`, as described at the top of that file.
Your head mesh must stand up, face forward (+Z), with its mouth closed.

## 6. Ask the artist first

- **Saving or overwriting a scene, ever.** Work on the open scene, leave saving to them.
- **Apply again.** It rebuilds the rig and board: animation keyed on the board is lost and the face camera resets.
- **Freezing a mesh's scale.**
- **Editing the tool.** It is their installed copy: say which file and why, keep a backup, and warn that the next Mutant
  Tools update replaces it. Suggest reporting the fix to the Mutant Tools team.
- **Publishing pictures or the rig.** Check that the head's author and Epic's license allow it.

After editing an `mm_*` file, reload in this order, or restart Maya:
`mm_core, mm_dna, mm_rig, mm_regions, mm_points, mm_face, mm_epic, mm_faceboard, mm_zones, mm_maya, mm_fixes, mm_picker, mm_workflow, mm_controller`.

## 7. Checks that catch real problems

The artist judges by eye and has the last word: numbers looked fine on problems they caught. Render close-ups from more
than one angle, and once with nothing isolated, in the view they actually use.

| Look at | How | Expect |
|---|---|---|
| Eye turns about its center | Rigid fit of `<eye>_MH` between rest and control at ±1, applied to `FACIAL_*_Eye` | Does not move. A sphere fit per pose reads falsely: the iris dent turns with the eye |
| Pivots | Compare the MetaHuman DNA and `head_custom.dna` with `mm_core.skeleton_from_reader`, `joint_world` | Joints at one point on the MetaHuman stay at one point: eye and lid pivots, `FACIAL_C_Jaw` with `FACIAL_C_LowerLipRotation` |
| Teeth | Weights per connected piece of `<teeth>_MH` | Each tooth and gum follows one jaw only. Upper teeth stay still when the jaw opens |
| Teeth through skin | Skin seen from the front, per pose: see `mm_fixes.in_front_of_skin` | Nothing in front of the skin. Closest-point checks miss thin lips |
| Lips with the jaw open | Upper minus lower lip height at the same X, inner 70% of the line | Above 0: lips do not cross |
| Lids at full blink | Same measure on the lid lines | About 0 or slightly below: no eye shows, and no lump past the lower lid |
| Original meshes | Visibility of your head, eyes and teeth | Hidden after Apply. Left showing, they stand still inside the moving rig |

A fix can break its neighbour: moving the lid pivots changed how far the lids travel. Re-measure what is nearby. Compare
with the same measure as before, not a new one.

## 8. Sharing the rig

The result is vanilla Maya 2026: joints, skinCluster, blendShape and math nodes. Animators need no custom nodes, plugin or
Mutant Tools. Older Mayas cannot load its `multDL` nodes. To check a scene: list node types by plugin, look for unknown
nodes, then open it in a clean `mayapy` and move the controls.
