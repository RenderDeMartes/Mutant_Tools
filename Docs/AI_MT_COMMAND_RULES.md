# Mutant Tools - AI Command Rules (Initial Prompt Ready)

## Purpose
This document defines **how an AI assistant should write and modify Mutant Tools code** in this workspace, especially for Maya block scripts and `mt` command usage.

Use this as:
- Team coding rules for AI-assisted changes.
- A copy/paste **initial prompt** before starting implementation.

For a human-oriented walkthrough with many practical examples, see:
- `Docs/AI_MT_COMMAND_TUTORIAL.md`

---

## 1) Workspace Context the AI Must Assume
- Project is `Mutant_Tools` for Maya.
- Main API entry point is:
  - `from Mutant_Tools.Utils.Rigging import main_mutant`
  - `mt = main_mutant.Mutant()`
- Most rig logic is implemented in `Blocks/**/exec_*.py`.
- Naming conventions and setup must come from configs, not hardcoded assumptions.

---

## 2) Mandatory `mt` Usage Rules

### 2.1 Always bootstrap with config imports
Inside block create/build functions, AI should use:
- `nc, curve_data, setup = mt.import_configs()`

### 2.2 Validate scene prerequisites before build actions
In build functions, AI should call:
- `mt.check_is_there_is_base()`

### 2.3 Respect block pattern
For block scripts, keep the existing structure:
- `create_<block>_block()`
- `build_<block>_block()`

Creation flow should follow existing pattern:
1. Load block json module file.
2. Ask/check name (`mt.ask_name`, existence check).
3. Create block via `mt.create_block(...)`.
4. Leave selection on the created block.

### 2.4 Use safe guards for Maya objects/attrs
Before operating:
- Check nodes with `cmds.objExists(...)`.
- Check attrs with `cmds.attributeQuery(..., exists=True)`.
- Avoid assuming selected order without validation.

### 2.5 Use `mt.root_grp` with custom naming when collisions are possible
If generating helper offset groups repeatedly, prefer:
- `mt.root_grp(input=node, custom=True, custom_name='SomeUniqueSuffix')`

Do not rely on default group suffixes when the operation may run multiple times on the same controls.

### 2.6 Keep constraints deterministic
When rebuilding constraints:
- Cache source ctrl, target object, and original constraint type.
- Recreate only supported types explicitly (`orient`, `parent`, `point`, `scale`).
- Use `mo=True` unless the task explicitly requires otherwise.

### 2.7 Do not hardcode pipeline-specific values when config exists
Prefer `nc` and setup dictionaries over hardcoded suffixes/names when equivalents exist.

### 2.8 Keep user-visible feedback concise
Use:
- `cmds.warning(...)` for recoverable issues.
- `print(...)` for successful milestones.

---

## 3) Editing Rules for AI in This Repo
- Make minimal, targeted edits.
- Preserve existing coding style and function names.
- Do not refactor unrelated code.
- Avoid adding new dependencies unless requested.
- Keep legacy-compatible style (this codebase mixes Python 2/3 compatibility patterns).
- Prefer local helper functions inside build functions when logic is block-specific.

---

## 4) Recommended Implementation Checklist
Before finalizing any change, AI should verify:
1. `create_` and `build_` functions still exist and are callable.
2. New code handles missing nodes safely.
3. New code does not create name clashes for helper groups.
4. Constraints are recreated after temporary deletions (if workflow requires it).
5. Only requested body parts/features are changed.

---

## 5) Quick `mt` Command Patterns (Common)
- Import configs: `nc, curve_data, setup = mt.import_configs()`
- Base validation: `mt.check_is_there_is_base()`
- Create block: `mt.create_block(name=..., icon=..., attrs=..., build_command=..., import_command=...)`
- Root/offset group:
  - Default: `mt.root_grp(input=node)[0]`
  - Safer (no clash): `mt.root_grp(input=node, custom=True, custom_name='OrientChange')[0]`
- Create guide joint: `mt.create_joint_guide(name=...)`
- Match transforms: `mt.match(target, source, r=True, t=True)`
- Mirror helper: `mt.mirror_group(node, world=True)`

---

## 6) Copy/Paste Initial Prompt for AI
Use the block below at the beginning of a new AI coding session:

```text
You are coding inside the Mutant_Tools Maya rigging workspace.

Follow these rules strictly:
1) Use Mutant API entry point:
   from Mutant_Tools.Utils.Rigging import main_mutant
   mt = main_mutant.Mutant()
2) In block functions, always import configs with:
   nc, curve_data, setup = mt.import_configs()
3) In build functions, always validate base with:
   mt.check_is_there_is_base()
4) Preserve existing block architecture and naming patterns.
5) Before Maya operations, guard with objExists/attributeQuery.
6) If creating offset/root helper groups repeatedly, use:
   mt.root_grp(input=node, custom=True, custom_name='UniqueSuffix')
   to avoid name clashes.
7) If deleting/rebuilding constraints, cache constraint type + targets and restore deterministically.
8) Make minimal, focused edits only; do not refactor unrelated code.
9) Use cmds.warning for issues and concise prints for success.
10) Keep changes compatible with the existing Mutant_Tools style.

When requirements are ambiguous, choose the simplest solution consistent with existing blocks.
```

---

## 7) Optional Session Add-on (Task Scoped)
For scoped tasks (example: only FK arms):

```text
Scope constraint: Implement only the requested body section.
Do not add legs/fingers/misc logic unless explicitly asked.
```
