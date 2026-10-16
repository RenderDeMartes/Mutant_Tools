# Mutant Tools 🦾

## 🚀 Overview
Mutant Tools is a **block-based modular rigging system** for Autodesk Maya, built for **speed, stability, and efficiency**. Developed by **Blue Tape Rigging Studios**, it lets riggers stack guide-driven blocks into production-ready rigs, and gives animators fast, clean controls.

Current release: **v1.6** (see [Config/version.json](Config/version.json)).

## 🎯 Features
- 🧱 **Block-based building** – stack blocks, place guides, build. Rebuild any time without losing skin, controller shapes or guide data.
- 🏎 **Fast viewport evaluation** – v002+ blocks use matrix-based builds, uvPin instead of follicles and proxy attributes, tuned for parallel evaluation.
- 🔁 **Versioned blocks** – every block keeps its old versions (`_v001`, `_v002`, …) so existing rigs keep building the same while new rigs get the upgrades.
- 🎭 **Realistic & cartoony** – stretch/squash, bendy limbs, soft IK, ribbons, sticky lips, toon eyes and more.
- 🧩 **Presets** – ready-made templates for humans, toons, game rigs, quadrupeds, birds, vehicles and props.
- 🎮 **Game-ready output** – root/convert-body blocks and Unreal game templates.
- 🤖 **Scriptable** – everything is Python, with a headless build path and an MCP bridge for AI-assisted work.

## 🧱 Blocks
Blocks live in [Blocks/](Blocks/), one folder per category:

| Category | Examples |
|---|---|
| `000_Presets` | Toon, Human Body/Face, Human Game, Unreal Game, Quad, Car, Bird, Prop templates |
| `001_Studio` | Custom orients & rotate orders, Toon Eye, Pickwalk, Vis Attrs, SN Lips, SN Renamer |
| `002_Biped` | Spine, Clavicle, Pelvis, Limb, Head, Hand, Foot, Eyes, Smart RFL, Leg Soft IK |
| `003_Facial` | Jaw, Mouth, Eyelids, Brows, Cheeks, Nose, Tongue, Teeth, Sticky Lips, Eyelashes |
| `004_Animals` | Wings, Tail, Quad Limb, Quad Spine, Snake, Ant Leg, Animal Mouth |
| `005_Clothes` | Cap, Pin, Skirt, Tie, Shirt, Cape |
| `006_Vehicles` | Wheel, Auto Wheel, Chassis, Steering Wheel, Doors, Drift, Push |
| `007_Games` | Root, Convert Body, Slide/Push Correctives |
| `008_Props` | Single FK, Rivet, Ribbonizer, Chain, Squash, Lattice, Reverse FK/Spline |
| `009_Data` | Load Skin, Load Ctrls |
| `010_Other` | BaseA, Code, Space Switches, Surface Constraint, Skin, Setter, Proxy Attr |

Each block is a JSON definition plus an `exec_*.py` build script. Blocks can run at different build phases (`RunBeforeBuild`, `RunBeforeLoadCtrls`, `RunAfterBuild`) and can define an `on_attr_changed` hook to react live to their settings (e.g. Hand finger toggles create/delete guides).

### Recent block upgrades
- **Spine v002** – no end flip, joint count, tweakers, stretch/squash multiplier, unlimited twist, pivot slide.
- **Limb v002** – parallel evaluation, bendy curve, controller scale, soft IK, SN orients.
- **Head v003** – matrix neck, joints from the Neck guide, stretch and SN orients.
- **Hand / SmartHand v002** – IK fingers with no-flip pole vectors, FingerScale, follows block parent scale.
- **Foot v002 / LegSoftIK v003** – built for Limb v002 legs, scales with the limb GlobalScale ctrl.
- **SN Renamer** – new studio block for renaming to SN conventions.

## 🛠 Tools
UI tools live in [UI/](UI/) and are reachable from the **Mutant-Tools** menu and the Bluetape Rigging shelf:
- **AutoRigger / Block Builder** – main block rigging UI.
- **Guide Placements & Presets** – place, mirror and save guides; load templates.
- **Helpers** – rigging utilities, Geo Update tab (save/select skin joints), ArkKit blendshape tool, mocap tab.
- **Face Install, Zombinator, Proxy Maker, Strict Skinning, Butcher** – facial setup, mesh/skin utilities.
- **Anim Loader, Games & Crowds, Variant Manager, Versionize** – animation, game and pipeline tools.

## 📜 Installation
Supports Maya **2022 – 2026** (PySide2 and PySide6).

**Drag & drop (recommended)**
1. Download the latest release and unzip it anywhere.
2. Drag [easy_install.py](easy_install.py) into the Maya viewport.
3. The installer copies the tools, installs the Bluetape Rigging shelf and adds the **Mutant-Tools** menu (auto-loaded on startup). The menu checks for new versions on its own.

**Manual**
1. Copy the `Mutant_Tools` folder into `maya/<version>/scripts/`.
2. Copy [shelf_Bluetape_Rigging.mel](shelf_Bluetape_Rigging.mel) into `maya/<version>/prefs/shelves/`.
3. In Maya's Script Editor (Python):
   ```python
   import Mutant_Tools.Utils.mt_menu as mt_menu
   mt_menu.create_mutant_menu()
   mt_menu.put_in_userSetup()
   ```

Full guide: [INSTALLATION_GUIDE.txt](INSTALLATION_GUIDE.txt) · [Video walkthroughs](https://mutanttools.com/installation-guide/)

## 🧪 Development
- **Tests** – static checks for every block, no Maya needed:
  ```
  python -m pytest Tests/test_blocks.py -v
  ```
- **Headless build** – [Dev/build_no_ui.py](Dev/build_no_ui.py) builds a rig without the UI.
- **Maya MCP bridge** – [Dev/MayaMCP/](Dev/MayaMCP/README.md) lets Claude Code, Claude Desktop, Codex and other MCP clients read and drive a live Maya session (start it from the **MCP** menu in the main window). Includes guide fitting helpers ([GUIDE_FITTING.md](Dev/MayaMCP/GUIDE_FITTING.md)) and FBX skeleton retargeting.
- **AI coding guide** – [Docs/AI_MT_COMMAND_RULES.md](Docs/AI_MT_COMMAND_RULES.md) and [Docs/AI_MT_COMMAND_TUTORIAL.md](Docs/AI_MT_COMMAND_TUTORIAL.md).
- **Releases** – push a `v*` tag; the [release workflow](.github/workflows/release.yml) zips the repo, creates the GitHub release and syncs it to Gumroad.

## 📫 Get in Touch
- 🌐 [Mutant Tools](https://mutanttools.com/)
- 📚 [Mutant Commands Wiki](https://mutanttools.com/docs/_build/html/index.html)
- 🧑‍💻 [Render de Martes](https://renderdemartes.com/)
- 🎬 [Blue Tape Rigging](https://bluetaperigging.com/)
- 💼 [LinkedIn](https://www.linkedin.com/in/esteban-rodriguez-488a68147/)

🚀 Elevate your rigging pipeline with **Mutant Tools** today!
