# Skeleton retarget (FBX animation -> Mutant rig controls)

Bakes skeleton animation (Unreal exports, Mixamo, ...) onto a Mutant rig's
controls, IK arms and legs included, so it can be edited on the rig and
exported back from the rig's export skeleton. First used on Coins100's
MegaMuffin (12 game animations from UE 5.8).

Files:
- `skeleton_retarget.py` — runs **inside Maya** (live bridge or mayapy).
- `../run_in_maya.py` — send a script to the live bridge.

## Requirements

- The rig has an **export skeleton** (e.g. `|root`) constrained to the bind
  joints, with the **same joint names** as the source. Names that differ go
  in `rename` (rig name -> source name). Unreal renames a bone whose name
  clashes with a mesh node regardless of case, e.g. `head` -> `head1`.
- Bone lengths match. Rest pose can differ (A-pose rig vs T-pose source):
  offsets are measured on the rig's default pose, not the source bind pose.
- Controls are at their default values in the base scene.

## Use

```python
from Mutant_Tools.Dev.MayaMCP.retarget import skeleton_retarget as sr

# 1. Is it the same skeleton? Import the source bind pose and compare.
sr.import_fbx(r'.../SK_Character_BindPose.fbx', 'BIND')
print(sr.compare_skeletons('|root', 'BIND', rename={'head': 'head1'}))
sr.remove_namespace('BIND')

# 2. Retarget one clip, or a whole folder, to .ma files.
mapping = lambda: sr.mutant_biped_map(cape=7) + [('Belly_Ctrl', 'Belly', 'parent')]
print(sr.retarget_fbx(base_rig_ma, r'.../A_Run.fbx', r'.../Run.ma',
                      mapping_fn=mapping, switches=sr.MUTANT_BIPED_SWITCHES,
                      rename={'head': 'head1'}))
print(sr.retarget_folder(base_rig_ma, fbx_dir, out_dir, mapping_fn=mapping,
                         switches=sr.MUTANT_BIPED_SWITCHES, rename={'head': 'head1'}))
```

`retarget_fbx` opens the base rig, sets the switches (IK = 0 on Mutant limb
switches), measures, imports the FBX into `SRC:` (scene fps follows the FBX),
keys every mapped control each frame, euler-filters, prints a report, deletes
the source and saves the `.ma`. About 1 s per 3 frames on a full biped.

## Mapping rows

`(control, export joint, mode)`, solved in order (parents first):
- `parent` — world translate + rotate.
- `orient` — rotate only; translate stays at default (FK, fingers, toes).
- `pole` — translate only; the joint is the limb's **middle** joint. The pole
  sits on the source limb's plane at the rig's default pole distance.

`mutant_biped_map()` covers Mover, COG, hips, FK spine, neck, head,
clavicles, FK + IK arms/legs with poles, toes and fingers, mapped to Unreal
mannequin bone names. Missing controls are skipped. Extra rig-specific rows
(cape, belly, ...) are appended by the caller.

## Why not constraints / HIK

- Mutant's right-side controls are mirrored with negative scale; a
  `parentConstraint` to a target with a negative-scale offset flips them.
  Solving with `xform(ws=True, m=...)` per frame does not.
- Control spaces follow other controls through constraints, not the DAG, so
  rows are solved twice per frame (`passes=2`) to settle.

## Reading the report

`pos` (cm) and `boneDir` (deg) should be small; that means the export
skeleton lands on the source. `rot` includes twist about the bone. On Mutant
limbs the export upper arm/thigh follow the ribbon start (no-roll), so source
twist there shows up as `rot` error with a small `boneDir`: expected, the
twist goes to the twist joints instead.

The IK hinge cannot bend backwards: where the source hyperextends an elbow or
knee, the pole stays on the natural side (no 180 flip) and that joint is off
by a few cm. The FK controls are keyed too, so switching that limb to FK
gives the exact pose.

# Polish: cartoon, feet, hands, FK arms (`anim_polish.py`)

After retargeting, `polish_clip()` on the open clip does, in order:

1. **Arms to FK** — the retarget keys FK too; the shoulder switches are keyed
   to FK so arms are edited with FK arcs.
2. **`cartoon_filter`** — Cartoon Animation Filter (Wang et al. 2006):
   `x' = x + k * (x - blur_sigma(x))`, after a light pre-blur so mocap jitter
   is not amplified. Adds anticipation/overshoot/follow-through; slow, large
   motion (root travel, flips) is untouched. `cyclic=True` wraps loops.
   Mover and fingers are not filtered.
3. **`exaggerate`** (loops) — rotations scaled about their average.
4. **`plant_feet`** — sole geometry from `foot_setup(mesh)`: vertices of the
   lower boot, behind the ball in ankle-control space, in front of it in
   ball-joint space (they bend with the toes). Contact = near the ground and
   slow. Contact runs go onto the ground, flat (and toes straight) when heel
   and ball are both down, pinned when the run barely travels. Every frame is
   pushed out of the ground.
5. **`relax_fingers`** — curl cascade on -rz (index least, pinky most) plus a
   bit of the mocap motion around its average.

```python
from Mutant_Tools.Dev.MayaMCP.retarget import anim_polish as ap
ap.polish_clip(k=1.2, sigma=3.0, cyclic=True, exaggeration=1.25)   # a loop
ap.polish_clip(k=0.8, sigma=2.5)                                   # a one-shot (flip, roll)
ap.side_playblast(out_dir, 'Run', 0, 58)                           # side view tracking COG
```

`polish_clip` modifies the clip in place: run it once per clip (keep the
retargeted file to start over).

Settings used on Coins100's MegaMuffin:

| Clip | k | sigma | cyclic | exaggeration |
|---|---|---|---|---|
| Idle | 1.4 | 4 | yes | 1.5 |
| Walk_Fwd | 1.2 | 3 | yes | 1.25 |
| Run_Fwd | 1.0 | 2.5 | yes | 1.2 |
| Fall_Loop | 1.2 | 3 | yes | 1.3 |
| Hanging_Idle (no planting) | 1.2 | 3 | yes | 1.4 |
| Jump / Land | 1.2 / 1.3 | 2.5 | no | - |
| Dash | 1.0 | 2.5 | no | - |
| BackFlip / Roll | 0.8 | 2.5 | no | - |

# Limb stability (no flipping arms or legs)

`polish_clip` also runs these (or call `fix_limbs()` on any clip):

- **`untwist_elbows`** — the FK elbow becomes a hinge: its twist about the
  forearm (swing-twist decomposition) is removed and handed to the wrist,
  which keeps the hand's world orientation. The forearm twist joints spread
  it instead of the elbow wringing.
- **`clamp_leg_reach`** — wherever a leg would straighten past 97% of its
  length, the COG is lowered (smoothed) so the IK knee never snaps straight.
- **`knee_poles`** — rebuilds knee poles pointing between the pelvis' front
  and the foot's, perpendicular to the hip-ankle line, continuous frame to
  frame. Good for locomotion; for flips, rolls and tucks keep the retargeted
  poles instead (`rebuild_poles=False`). Poles are never cartoon-filtered:
  amplifying them is what flipped knees.
- `plant_feet` only flattens a foot that is right way up, and `flat=0`
  disables flattening (Walk_Fwd: flattening at heel strike snapped the knee).

Checking: compare each limb joint's local rotation with the rig's rest pose
per frame; a twist change above ~15 deg/frame about the bone axis, or any
local rotation change above ~30 deg/frame outside genuinely fast moves, is a
flip. On MegaMuffin all clips pass except Run and Roll, which stay at their
mocap's own speed (fast pumps and a tumble).

# Back to Unreal

Bake the export skeleton (`|root`), delete its constraints, rename joints
whose Unreal names differ (`head` -> `head1`), export the skeleton only
(FBX 2020, Y up, cm, baked animation) and reimport over the existing
AnimSequence assets (`AssetImportTask` with `replace_existing`, skeleton
set, animation only), restoring `enable_root_motion` and friends after the
import. Montages, blend spaces and AnimBPs keep pointing at the same assets.
