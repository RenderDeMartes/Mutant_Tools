# Guide fitting (placing block guides on a mesh)

Tools for fitting Mutant block guides (Limb + Hand) to a model, driven from
outside Maya through the bridge. Used first on the SN_Rigging
`module/arms` variants (blob, cartoon, robot, skeleton).

Files:
- `guide_fit.py` — runs **inside Maya** (live session or mayapy).
- `run_in_maya.py` — sends a script file (or `-c` code) to the live bridge
  and prints stdout/traceback. Sending a file avoids quoting problems.

```
python Dev/MayaMCP/run_in_maya.py my_fit.py --port 7501
python Dev/MayaMCP/run_in_maya.py -c "import maya.cmds as mc; print(mc.ls(sl=1))"
```

Inside a script: `import Mutant_Tools.Dev.MayaMCP.guide_fit as gf` (call
`importlib.reload(gf)` after editing the module).

## Channel rules (keep fits comparable between assets)

| Guide | Allowed |
|---|---|
| Shoulder | translate + rotate |
| Elbow | tx + one bend rotation (rz) |
| Wrist | tx only |
| Palm | translate + rotate (sits on the wrist) |
| Finger / thumb `_00` roots | translate (all axes), no rotate |
| Every other finger guide, cups | tx only |
| jointOrient | **never touched** |

The solvers enforce this; finger rotations stay at template values, so a
fanned or curled finger can't be matched exactly — the fit is the best
straight chain (thumb direction especially is template-locked).

## Workflow

1. **Open the scene** in the live Maya (check `mc.file(q=True, modified=True)`
   first so nothing unsaved is lost). Note `Mutant_Build.v` to restore it.
2. **Look**: `gf.snap(name, 'top'|'front'|'side', cx, cy, width, out_dir,
   guides=False)` writes a calibrated ortho playblast. Read it, pick pixels,
   convert with `gf.px_to_world(view, cx, cy, width, px, py)`.
   - top: screen right = +X, down = +Z. front: right = +X, down = -Y.
   - Character convention here: arm along +X, thumb toward +Z, elbow back
     is -Z, back of hand up (+Y).
3. **Get targets** (world points):
   - Hard-surface parts: `gf.mesh_shells(mesh, min_x=0.5)` lists connected
     pieces; `gf.shell_chain_joints(mesh, [seg0, [seg1a, seg1b], seg2], shells)`
     returns `[start, joint1, ..., end]` for a chain of rigid segments (exact
     joint locations for robot fingers / bones).
   - Organic parts: eyeball knuckle + tip, then
     `gf.finger_points(knuckle, tip)` (phalanx ratios .45/.30/.25) and
     recentre each with `gf.tube_center(mesh, p, axis)[0]`.
     Don't trust `tube_center` at a knuckle (it centres on the palm section)
     or at an open flare (shoulder cuffs) — keep the picked lateral/height
     there.
   - No elbow in the model (noodle/tube arms): elbow = midpoint pushed
     `-Z` by 2% of limb length (small back prebend, keeps IK pole sane).
4. **Fit**:
   ```python
   gf.fit_limb('L_Shoulder_Guide', 'L_Elbow_Guide', 'L_Wrist_Guide', S, E, W)
   res, T = gf.fit_hand_points(W, {'Index': [k, j2, j3, tip], 'Middle': ..., 'Ring': ..., 'Pinky': ...},
                               thumb=[mcp, ip, tip])
   ```
   User default: keep the limb as above (rz bend), then pass
   `up=(0, 1, 0)` to `fit_hand_points` and call `gf.roll_to_up('L_Wrist_Guide')`
   so palm, fingers and wrist have Y (green) up; thumb and cups keep the
   template. The palm only aims X with no roll (fingers inherit it; Y tilts
   only by the fingers' pitch). `fit_limb(..., up=...)` also exists (bend
   becomes ry) but the user didn't want it.
   To fix an already-placed hand without losing manual tweaks: use the
   current guide world positions as targets and run `fit_hand(..., up=...)`.
   `fit_hand_points` builds weighted targets (tips 1.5, joints 1, thumb 0.3,
   roots/cups weak), puts the palm on the wrist and optimises its rotation
   (Nelder-Mead), projecting every tx. `res` = per-guide residual distance.
   Lower-level: `gf.fit_hand(palm, targets, weights, free_t=[...])`.
5. **Check**: `gf.show_targets(T)` (locators in `fit_targets_grp`) and snap
   again with guides on. Iterate on targets, not on the solver.
6. **Save as a new version**: `gf.save_as(path_v00N, build_visible=<orig>)`
   deletes `fit_targets_grp`, restores `Mutant_Build.v`, saves .ma. It
   refuses existing files or versions the pipeline registered (`.json`):
   the user saves wip versions from their own tool too, so always list the
   folder and take the next free number.

## Gotchas
- Don't name scratch scripts `inspect.py` (shadows stdlib, mayapy crashes).
- Code exec'd through the bridge runs with separate globals/locals: helper
  functions defined in the script can't see the script's top-level names —
  pass them as default args.
- Scenes with Arnold attrs open with errors when mtoa isn't loaded; wrap
  `mc.file(o=True)` in try/except. Saving then drops `requires "mtoa"`.
- Hands with fewer fingers: extra finger guides (e.g. Pinky on a 3-finger
  hand) are parked next to the closest finger; toggle the finger off on the
  Hand block if it shouldn't exist.
