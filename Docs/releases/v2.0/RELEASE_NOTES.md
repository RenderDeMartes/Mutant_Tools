# Mutant Tools 2.0

Mutant Tools 2.0 rebuilds the core biped and animal blocks on matrix nodes, adds a local face
rig that matches the game mouth, and makes builds easier to read when something goes wrong.
Rigs from 1.6 keep building as they did: every block keeps its old versions, and you choose
when to move each one to the new version.

**By the numbers** (measured in development on each block alone; how much faster a full rig
plays back depends on the character):

| Block | Change |
|---|---|
| Spine v002 | about 2x faster evaluation |
| Limb v002 | about 2x faster playback |
| Head v003 | about 1.6x faster neck (8 joints, parallel) |
| Hand v002 | 324 → 385 fps in the same scene |
| MouthGames v003 | same fps as v002 with about 3.7x the lip joints |
| Rebuild | about 3x faster skin load with the fast skin pack |

## Highlights

- **Faster blocks.** Spine, Limb, Head, Hand, Foot, QuadLimb and QuadSpine use matrix nodes
  instead of constraints, and uvPins instead of follicles, so playback runs in parallel with no
  evaluation cycles.
- **More controls for animators.** Spine tweakers and squash & stretch, bendy limbs that curve
  into a true arc, controller scale that only scales its own joints, a neck you can curve from
  the top, and IK fingers that don't flip.
- **Wings v002.** Add or remove feathers live from the builder, set joints per feather, curve
  the feathers, and spread or fold whole wings with two controls.
- **A local face that matches the game mouth.** Lips v003, Jaw v002 and StickyLips v002 bring the
  MouthGames features (even lip joints, soft tweaks, roll, rotating mid controls, zip) to the
  layered face, and the controller names match so animation moves between the two.
- **Builds you can read.** The new Build Log shows every block with its build time and opens the
  block that failed, with a likely cause. Rebuilds keep your skins even when joints are missing.
- **A new AutoRigger panel.** Block settings now show as cards with toggles, sliders and pickers.
  An eye button shows what changes between versions before you update.
- **Help on every button.** Hover any button for a tooltip, or right click it and pick
  **Learn more** for steps and examples.

---

## Biped blocks

### Spine v002

- **JointCount** 3 / 5 / 7 / 9 / 11 (default 5). With 5 joints the names match v001.
- **Tweakers**: one control per joint that moves, turns and scales only its own bind joint.
- **SSMultiplier**: one attribute for squash & stretch. 0 keeps length and volume (the joints slide
  along the curve), 1 is normal, higher values push the volume change further.
- **Twist past 180°** from the Bottom / Belly / Top IK controls, and **PivotSlide** on the
  Bottom / Top IK to move the pivot toward the belly.
- **BellyFollow** and **BellyFollowChest** set how much the belly IK follows the root and chest.
- **DefaultCtrls** (Both / IK / FK) sets which controls are visible after the build.
- The chest no longer flips 180° when the end IK moves past it, and translating the IK controls
  no longer adds twist.
- FK / IK controller scale reaches the joints, uniform or non uniform, without the children
  inheriting it.

### Limb v002

- **About 2x faster playback.** Follicles were swapped for uvPins (they forced the serial
  evaluator), and the IK/FK switch attributes moved to a data node with proxies, which removed an
  evaluation cycle.
- **Bendy path.** The tweakers ride an exact path through the start, mid bendy control and end,
  without wobble. **BendyCurve** goes from straight to a perfect arc, **AutoCurve** curves the limb
  as it bends, and **Upper/LowerCurve** plus start/end ease shape each half.
- **Bendys: SN** builds a 5-control bendy setup on the same bind joints, so skins carry over.
- **Controller scale.** FK, IK, Sub IK, bendy and tweak controls scale the bind joints without the
  children inheriting it. FK scale follows the hierarchy, so scaling the shoulder makes the arm
  longer.
- **GlobalScale control** per arm and leg scales the whole limb from its start.
- **ArmsSoftIk** (optional) adds soft IK to arms, using the same maths as the leg soft IK block.
- **Orients: SN** applies the studio orients directly in the block.
- Fixed: the IK no longer jumps to the origin after a rebuild when controls are renamed.

### Head v003

- **Matrix neck**: no constraints, follicles, NURBS or skinClusters. About 1.6x faster with 8 neck
  joints in parallel, with no evaluation cycles.
- Neck joints are spread evenly from the Neck guide, and head twist spreads up the neck.
- **Neck_End_Ctrl** sets where the neck enters the head. Rotating it curves the neck (a Bezier end
  tangent, multiplied by **CurveAmount**) and twists the top. Turn it on with **NeckEndVis**.
- **Stretch** (0 keeps the neck length) and **Volume** sit on every neck control.
- Bind joints keep values on translate, rotate and scale, ready for game export.
- **Orients: SN** aligns the neck controls to the world like the spine.
- The default Head block now builds v003. v001 and v002 stay available.

### Hand v002 and SmartHand v002

- **IK fingers** stay in place when the hand moves. Each IK control has **Twist**, **Stretch** and
  **Volume**.
- **No-flip pole vectors**: the finger pole vector follows the hand instead of the IK control.
- **FingerScale**: *Phalanx* (a control scales its own joint) or *Finger* (the scale goes down the
  rest of the finger). Scaling the IK control squashes the last phalanx, for example a fingertip
  pressing on something.
- The hand follows a non uniform scale on its parent.
- Curls, cups, poses and IK/FK switches are on every hand control. **CupCtrls** hides the cup
  controls by default.
- Toggling fingers in the AutoRigger creates or deletes their guides right away.
- Faster evaluation (324 → 385 fps in our test scene). SmartHand v002 uses 1 or 2 groups per
  finger control instead of 6.

### Foot v002 and LegSoftIK v003

- Built for Limb v002 legs: the foot roll and reverse foot drive the v002 leg.
- Ankle IK / Sub IK / FK scale scales the whole foot around the ankle. The toes control scales
  the toes.
- The foot scales with the leg's GlobalScale control.
- **Orients: SN** option, faster matrix connections, and a fix for the right side picking the
  wrong joints.
- **RollBall** now lifts the heel with positive values, like the other rolls.
- **LegSoftIK v003** adds soft IK to Limb v002 legs and works with the foot roll.

---

## Animal blocks

### Wings v002

- **Live feather guides.** Change the Scapular, Secondary or Primary feather count and the guides
  update in the builder right away. The first and last feathers stay in place and the ones in
  between are interpolated.
- **Joints per feather** for each part, plus optional bend guides so feathers can curve.
- **Elbow and wrist spread controls** drive both feather groups where they meet. **AutoClose**
  keeps the groups from opening a gap when the wing bends.
- **SpreadMode: Roll** (default) turns each feather to follow the next one, so overlapping
  feathers don't clip. **SheetFollow** blends it.
- **PivotX/Y/Z** on every feather control, **SpreadMin** to reach the far feather, and a
  **Feather Pivots** tool in Helpers ▸ Animals.
- With default settings Wings v002 builds exactly like v001.

### QuadLimb v002 and QuadSpine v002

Same guides, joints, controls and bind names as v001, so existing quadrupeds can move up.

- **QuadLimb v002**: matrix build with no evaluation cycles. The pole vector stays on the leg
  plane, which fixes legs far from Z 0 popping sideways at rest. Stretch and soft IK run from hip
  to ankle. Adds a leg GlobalScale control, controller scale, Foot v002 support, and an optional
  BendyCurve.
- **QuadSpine v002**: the hip and chest controls fully drive the end joints, and **HipBend** /
  **ChestBend** bend the spine into them. Joints ride the curve by arc length: Stretch 0 keeps the
  length and Squash keeps the volume. Adds Tweakers, DefaultCtrls, JointCount, and a bind chain
  ready for game export.

---

## Face blocks

- **Lips v003**: a fully local lip rig. Moving or scaling the parent never moves the lip joints,
  only the lip controls (we measured 0.00000 units of leak, down from up to 10). It brings the
  MouthGames lips over: roll, soft tweaks, weighted scale, rotating mid controls that follow and
  aim at the corners, BindJoints and the buccal flap. Corner mode works like v001 again: **BSP** keeps the
  main control free for blendshapes and **RIG** drives the lips. **GameMode** builds world-space
  bind joints that match MouthGames v003. **LegacyBindNames** keeps the v002 joint names so
  existing skins still load.
- **Jaw v002**: a dynamic jaw pivot (JawPivot guide and Pivot control), a Follow null for lips,
  teeth and tongue, and **GameNames** so the jaw uses the same names as the game rigs and
  animation transfers.
- **StickyLips v002**: zip for the local Lips v003 + Jaw v002 face. Each lip point slides to the
  middle of both lips from the corners in (Zip 0-3 at the corners, 7-10 in the middle). It reads
  the jaw skin live, so it works with any skin weights and any build order. If something is set
  up wrong, the error message says what to fix.
- **MouthGames v003**: lip joints spaced evenly by curve length (**BindJoints**: per vertex or
  21/15/11/9/7/5), soft tweaks with a cosine falloff, per-axis scale, Roll and Zip, a dynamic jaw
  pivot, rotating mid controls, corner follow and aim, and an optional buccal flap. It runs at the
  same fps as v002 with about 3.7x the joints.
- **FaceAutomations** (new): cheek follow, cheekbone follow, cheek push and nostril follow, with
  toggles. It replaces the CheekAutomations / CheekPushZ / Nostril code blocks with the same
  result and clean right-side channels.
- **Commissures v002** is off while the corner control is in RIG mode, so the mouth corner no
  longer moves twice.

---

## Props and studio blocks

### Squash v002

- Squash_Ctrl translate drives the v001 bend and squash deformers, with every v001 setting.
- Rotate and scale drive a **lattice** made of FK rows from the base, so rotations add up into an
  extra curve. **RotationAmount** sets how strong it is, and scale fades out toward the base.
- Row, edge and corner controls move their part of the lattice. They are hidden by default.
- The default Squash block now builds v002.

### Studio

- **SN_Renamer** (new): renames controls to the show convention and tags them so Load Ctrls still
  finds them. It runs in the new **RunBeforeLoadCtrls** build phase.
- **Orients: SN** is now an option on Limb, Head and Foot.
- **Load Ctrls** has an SN controller data preset.
- All **19 preset templates** use the latest block versions.

---

## Building and rebuilding

### AutoRigger card view

- Block settings are grouped into collapsible cards with toggle chips, segmented choices, sliders,
  a filter box, readable labels and help tooltips. Changed values are marked, and right click
  resets one to its default or restores a backup. The classic view is still one click away.
- The control type and color fields are pickers with previews, and any curve or color in the repo
  can be picked.
- **Values survive version changes.** Settings carry over by name and convert between types.
  Values that don't fit the new version are kept in a backup and come back if you switch back.
  Renamed attributes carry over too.
- Blocks can show settings that update live: Hand finger toggles and Wings feather counts change
  the guides right away.

### Version diff and update to latest

The eye button next to the Version dropdown compares two versions of a block: new, removed and
changed attributes, default changes, and what happens to your values. Right click ▸ Update now
picks the latest version by default.

### Build Log

The AutoRigger logs the whole build. **Build Log** (also under View Log in the Mutant-Tools menu) shows one row per
block or builder step with its time. Green means built and grey means not built. The failed block
opens in red with a likely cause matched from common errors. **Raw Log** still shows the full
text.

### IO report and safer rebuilds

- **Skins survive missing joints.** If a joint no longer exists, its weights move to the remaining
  influences instead of the mesh being skipped.
- **Fast skin pack**: rebuilds load skins about 3x faster when pymel is installed, using the new
  *Rebuild With Fast Skin Pack (pymel)* option.
- At the end of a rebuild, the IO report lists the skins and controllers that need a look. Click a
  line to select the node.
- Controllers are found by their MutantController tag, not just the `_Ctrl` suffix, so renamed
  controls keep their shapes through rebuilds.
- Rebuilds skip the skin save and load when the scene has no skinClusters.

---

## Help and UI

- **Button help on every tool.** Hover for a tooltip, or right click ▸ **Learn more** for what the
  button does, steps, examples and how it works. The Code tab shows the handler, with **Open in VS
  Code** at that line. 408 of 428 buttons are covered.
- **New line icon set** across the tool UIs.

- **Helpers ▸ Geo Update** tab: Copy Skin to Other Geo, plus Save / Select Skin Joints, which can
  recreate missing joints at their saved position in another scene.
- **Maya 2024 compatibility.** Rigs built in Maya 2026 open in 2024: blocks no longer create the
  2026-only `multDL` / `addDL` node types. PySide2 fallbacks were added where they were missing.

---

## Early previews

These are new and still early. Try them and send us feedback.

- **WebToRig (beta)**: place joints on your character at
  [mutanttools.com/web-to-rig](https://mutanttools.com/web-to-rig/), download, and drag the file
  into Maya. A guided window imports the character, places the template and builds the rig, then
  lets you try built-in animations.
- **TopoTransfer** and **Meta Mutant** (Mutant-Tools ▸ Misc): fit a base mesh onto a scan or
  sculpt while keeping its topology, and put the MetaHuman face rig on your own head (Maya 2026).

---

## Upgrading from 1.6

1. Install 2.0 as usual (drag `easy_install.py` into the viewport). The in-Maya updater will also
   offer it.
2. **Existing rigs build the same as before.** Blocks in your scenes stay on their current version
   until you change them.
3. To move a block up, open the AutoRigger, click the eye next to **Version** to see what changes,
   then switch the version (or right click ▸ Update). Values carry over, and anything that doesn't
   fit goes to a backup.
4. New blocks and the preset templates start on the latest versions.

**Changes that can affect existing setups when you update a block:**

| Block | Change |
|---|---|
| Head | The default block is now v003. The *Bend* attribute is gone. |
| Squash | The default block is now v002. |
| Spine v002 | JointCount defaults to 5. |
| Limb v002 | The *AutoBend* attributes are replaced by BendyCurve / AutoCurve / Upper/LowerCurve. |
| Foot v002 | *RollBall* is flipped: positive values lift the heel. |
| Lips v003 | Zip moved to StickyLips v002. *SetJaw* is gone: Lips and Jaw are separate systems that build in any order. Use *LegacyBindNames* to keep v002 joint names. |
| MouthGames | v004 was folded into v003. Templates that pointed at v004 now use v003. |
| Face templates | Human_Face_Template and ToonFaceTemplate use Jaw v002, Lips v003 and Commissures v002. The blocks are renamed Mouth_Jaw / Mouth. |

---

## Fixes

- Rebuilds no longer stop when loading skins back on meshes skinned by an FBX import (their
  skinning method came in as -1, which Maya refuses to set).
- Creating a Spine block no longer fails looking for its JSON.
- Skirt v001: Delete and Rebuild no longer fails on a duplicated master control.
- Squash v001: the bend and squash pivots stay on the bottom of the geo, and UseCustomPivots only
  moves the control.
- Loading controllers reconnects visibility to every curve shape, not the first shape found.
- BaseA: the Mover Gimbal visibility attribute is no longer keyable.
- AutoRigger: guides inside blocks show in the outliner again (new Help menu buttons: Black Box
  off, Refresh Blocks in Outliner).

---

<details>
<summary><b>For TDs and block authors</b></summary>

- **Block hooks**: a block module can define `on_attr_changed` to react when its settings change
  in the AutoRigger, and list `DYNAMIC_ATTRS` to show them in a Dynamic section.
- **BlockBuildError** (`Utils/Rigging/block_errors.py`): raise it from a block to show your own
  message in the Build Log instead of a guessed cause.
- **New build phase**: `RunBeforeLoadCtrls` runs after skins load and before controllers load.
- **MutantController tag**: `mt.curve` and `mt.controller` tag every controller they create.
  Save, load and mirror use the tag.
- **MayaMCP** (`Dev/MayaMCP`): a live bridge into Maya for scripted and AI-assisted work, with
  helpers for fitting guides to a model, skinning shell by shell with ngSkinTools, and retargeting
  FBX skeleton animation onto rig controls.
- **ChainSkin** (`Utils/IO/ChainSkin.py`): skins meshes to joint chains matched from the top view
  (feathers, hair cards).

</details>

## Credits

- Built by Blue Tape Rigging Studios, with MouthGames v003 and FaceAutomations work by
  [ElSebasCisneros](https://github.com/ElSebasCisneros).

**Full changelog**: https://github.com/RenderDeMartes/Mutant_Tools/compare/v1.6...v2.0
