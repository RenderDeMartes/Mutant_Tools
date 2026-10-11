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
