# Copilot Instructions for Mutant_Tools

## Big picture architecture
- This is a Maya rigging toolkit centered on a single API object: `mt = main_mutant.Mutant()` (`Utils/Rigging/main_mutant.py`).
- `Mutant` aggregates rigging/tool/module behaviors via inheritance (`modules.Modules_class`) and scene helpers used across the codebase.
- Feature implementation is block-based: each rig feature lives in `Blocks/<tab>/exec_*.py` plus a paired JSON definition in the same folder.
- UI loaders in `UI/**/load_*.py` are mostly launchers; heavy rig logic usually lives in `Blocks/**` and `Utils/**`.
- Menu/bootstrap lives in `Utils/mt_menu.py`; install/drop entrypoint is `easy_install.py` (`onMayaDroppedPythonFile`).

## Core block pattern (must follow)
- Keep paired functions: `create_<name>_block()` and `build_<name>_block()` (see `Blocks/002_Biped/exec_spine.py`, `exec_limb.py`).
- In build functions, start with:
  - `nc, curve_data, setup = mt.import_configs()`
  - `mt.check_is_there_is_base()`
- Creation flow is config-driven: load block JSON, ask/check name, call `mt.create_block(...)`, create guides, then select block.
- Build flow assumes selected block/config connections; avoid changing this UX unless requested.

## Naming and config conventions
- Do not hardcode suffixes/prefixes already defined in `Config/name_conventions.json` (e.g., `nc['joint']`, `nc['ctrl']`, `nc['module']`).
- Use colors/shapes/settings from `Config/rig_setup.json` where available (left/right/main colors, ctrl defaults).
- Block attributes are declared in JSON (`Blocks/**/<block>.json`) using typed keys like `_string`, `_enum`, `_bool`, `_float`.

## Code style and compatibility constraints
- Preserve existing compatibility style: frequent `try: importlib.reload ... except: imp.reload ...` and `from __future__` imports.
- This repo uses Maya `cmds`-first patterns; keep operations defensive (`cmds.objExists`, `cmds.attributeQuery`) before acting.
- Prefer small localized edits over refactors; many scripts are production legacy and depend on current naming/selection behavior.

## Developer workflows
- Typical install for artists: copy `Mutant_Tools` into Maya scripts directory or drag-drop `easy_install.py`.
- Typical bootstrap in Maya Python tab:
  - import/reload `Mutant_Tools.Utils.mt_menu`
  - call `mt_menu.create_mutant_menu()`
- Documentation build is Sphinx-based under `Docs/` (`make.bat html` on Windows, `make html` where `make` exists).
- No obvious unit-test harness is present at repo root; validate changes by running targeted block/UI flows in Maya.

## Integration boundaries
- `Utils/Unreal/MetaHuman/dna_calibration/**` contains external/vendor-style code and READMEs; avoid broad style rewrites there unless task-specific.
- External runtime dependencies are Maya Python APIs (`maya.cmds`, `maya.mel`, `maya.OpenMaya`) and occasional PyMEL-like tooling.

## Practical edit rules for agents
- If modifying a block, update both JSON-driven assumptions and Python code paths together.
- Keep scene side effects deterministic: avoid renaming core nodes/groups unless required by the task.
- Maintain concise artist-facing feedback (`cmds.warning` for recoverable issues, `print` for milestones).
- When uncertain, mirror nearby block implementations in the same tab folder instead of inventing new patterns.
