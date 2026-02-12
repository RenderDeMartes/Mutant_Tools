# Mutant Tools AI Command Rules — Human Tutorial (With Many Examples)

This tutorial explains the rules in `AI_MT_COMMAND_RULES.md` in practical terms for artists, technical artists, and developers.

It focuses on **real block script workflows** in `Blocks/**/exec_*.py` and includes many **copy/paste examples** you can adapt.

---

## 0) Core Pattern (Memorize This)

Every Mutant block script should follow this rhythm:

1. Import Mutant API.
2. In `create_*`, load module JSON, ask/check name, call `mt.create_block`.
3. In `build_*`, import configs and validate base.
4. Guard every scene operation (`objExists`, `attributeQuery`).
5. Keep constraints deterministic if rebuilding.
6. Print concise success and warn on recoverable issues.

---

## 1) Boilerplate You Can Reuse

### Example 1 — Minimal imports and Mutant instance

```python
from maya import cmds

from Mutant_Tools.Utils.Rigging import main_mutant
mt = main_mutant.Mutant()
```

### Example 2 — Standard `create` + `build` function names

```python
def create_arm_fk_block():
    pass


def build_arm_fk_block():
    pass
```

### Example 3 — Build bootstrap (required)

```python
def build_arm_fk_block():
    nc, curve_data, setup = mt.import_configs()
    mt.check_is_there_is_base()
```

---

## 2) Create Block Examples

### Example 4 — Load module JSON from current folder

```python
import os
import json


def _load_block_definition(json_file):
    folder = os.path.dirname(__file__)
    path = os.path.join(folder, json_file)
    with open(path, 'r') as handle:
        return json.load(handle)
```

### Example 5 — Ask user for name and stop on cancel

```python
def _ask_block_name(default_name='L_Arm'):
    name = mt.ask_name(default_name)
    if not name:
        cmds.warning('Block creation cancelled: no name provided.')
        return None
    return name
```

### Example 6 — Validate unique block transform name

```python
def _block_node_name(name, nc):
    return '{}{}{}'.format(name, nc['module'], nc['group'])


def _ensure_unique_name(name, nc):
    candidate = _block_node_name(name, nc)
    if cmds.objExists(candidate):
        cmds.warning('Block already exists: {}'.format(candidate))
        return False
    return True
```

### Example 7 — Basic block create call

```python
def create_arm_fk_block():
    nc, curve_data, setup = mt.import_configs()
    module = _load_block_definition('07_ArmFk.json')

    name = _ask_block_name(module.get('Name', 'L_Arm'))
    if not name:
        return

    if not _ensure_unique_name(name, nc):
        return

    block = mt.create_block(
        name=name,
        icon=module.get('Icon', 'Arm'),
        attrs=module.get('Attrs', {}),
        build_command=module.get('BuildCommand', 'build_arm_fk_block'),
        import_command=module.get('ImportCommand', 'create_arm_fk_block')
    )

    if block and cmds.objExists(block):
        cmds.select(block)
        print('Created block: {}'.format(block))
```

### Example 8 — Create guide joint after block creation

```python
def create_leg_fk_block():
    nc, curve_data, setup = mt.import_configs()
    module = _load_block_definition('08_LegFk.json')
    name = _ask_block_name(module.get('Name', 'L_Leg'))
    if not name or not _ensure_unique_name(name, nc):
        return

    block = mt.create_block(
        name=name,
        icon=module.get('Icon', 'Leg'),
        attrs=module.get('Attrs', {}),
        build_command='build_leg_fk_block',
        import_command='create_leg_fk_block'
    )

    guide = mt.create_joint_guide(name='{}{}_Jnt'.format(name, nc['joint']))
    if guide and cmds.objExists(guide):
        mt.match(guide, block, r=True, t=True)

    cmds.select(block)
```

### Example 9 — Guard selection assumptions in create

```python
def create_from_selected_prefix_block():
    nc, curve_data, setup = mt.import_configs()
    selection = cmds.ls(sl=True) or []
    if not selection:
        cmds.warning('Select one object to infer the block name.')
        return

    base_name = selection[0].split('|')[-1]
    name = _ask_block_name(base_name)
    if not name:
        return

    mt.create_block(
        name=name,
        icon='Generic',
        attrs={},
        build_command='build_from_selected_prefix_block',
        import_command='create_from_selected_prefix_block'
    )
```

### Example 10 — Use warnings for recoverable issues

```python
def create_spine_block():
    nc, curve_data, setup = mt.import_configs()
    name = _ask_block_name('Spine')
    if not name:
        cmds.warning('Spine block was not created.')
        return
    mt.create_block(name=name, icon='Spine', attrs={}, build_command='build_spine_block', import_command='create_spine_block')
    print('Spine block ready.')
```

---

## 3) Build Block Examples (Safe and Deterministic)

### Example 11 — Minimal safe build

```python
def build_arm_fk_block():
    nc, curve_data, setup = mt.import_configs()
    mt.check_is_there_is_base()

    selected_blocks = cmds.ls(sl=True) or []
    if not selected_blocks:
        cmds.warning('Select a block to build.')
        return

    block = selected_blocks[0]
    if not cmds.objExists(block):
        cmds.warning('Selected block does not exist: {}'.format(block))
        return

    print('Building block: {}'.format(block))
```

### Example 12 — Validate custom attributes before reading

```python
def _get_bool_attr(node, attr_name, default=False):
    if not cmds.objExists(node):
        return default
    if not cmds.attributeQuery(attr_name, node=node, exists=True):
        return default
    return bool(cmds.getAttr('{}.{}'.format(node, attr_name)))
```

### Example 13 — Validate enum/string attrs safely

```python
def _get_str_attr(node, attr_name, default=''):
    if not cmds.objExists(node):
        return default
    if not cmds.attributeQuery(attr_name, node=node, exists=True):
        return default
    value = cmds.getAttr('{}.{}'.format(node, attr_name))
    return value if value is not None else default
```

### Example 14 — Skip invalid joints during build

```python
def _filter_existing(nodes):
    return [node for node in nodes if cmds.objExists(node)]
```

### Example 15 — Create control and offset group safely

```python
def _create_fk_ctrl(joint, ctrl_name):
    if not cmds.objExists(joint):
        cmds.warning('Joint missing: {}'.format(joint))
        return None

    ctrl = cmds.circle(name=ctrl_name, normal=(1, 0, 0), ch=False)[0]
    mt.match(ctrl, joint, r=True, t=True)

    offset = mt.root_grp(input=ctrl, custom=True, custom_name='FkOffset')[0]
    return ctrl, offset
```

### Example 16 — Avoid helper-group naming collisions

```python
def _make_twist_offset(ctrl, index):
    suffix = 'TwistOffset_{:02d}'.format(index)
    return mt.root_grp(input=ctrl, custom=True, custom_name=suffix)[0]
```

### Example 17 — Parent with guards

```python
def _safe_parent(child, parent):
    if not cmds.objExists(child):
        cmds.warning('Cannot parent missing child: {}'.format(child))
        return False
    if not cmds.objExists(parent):
        cmds.warning('Cannot parent to missing parent: {}'.format(parent))
        return False
    cmds.parent(child, parent)
    return True
```

### Example 18 — Match transforms with guards

```python
def _safe_match(target, source):
    if not cmds.objExists(target) or not cmds.objExists(source):
        cmds.warning('Match failed. Missing target or source.')
        return False
    mt.match(target, source, r=True, t=True)
    return True
```

### Example 19 — Build only if guides are present

```python
def build_spine_block():
    nc, curve_data, setup = mt.import_configs()
    mt.check_is_there_is_base()

    guides = _filter_existing(cmds.ls('*Spine*Guide*', type='transform') or [])
    if not guides:
        cmds.warning('No spine guides found.')
        return

    print('Found {} spine guides.'.format(len(guides)))
```

### Example 20 — Mirror helper when requested

```python
def _mirror_if_needed(node, enabled):
    if not enabled:
        return None
    if not cmds.objExists(node):
        cmds.warning('Cannot mirror missing node: {}'.format(node))
        return None
    return mt.mirror_group(node, world=True)
```

---

## 4) Constraint Rebuild Patterns (Deterministic)

### Example 21 — Cache supported constraints

```python
def _get_constraint_type(node):
    if cmds.nodeType(node) == 'parentConstraint':
        return 'parent'
    if cmds.nodeType(node) == 'orientConstraint':
        return 'orient'
    if cmds.nodeType(node) == 'pointConstraint':
        return 'point'
    if cmds.nodeType(node) == 'scaleConstraint':
        return 'scale'
    return None


def _cache_constraints(target):
    cached = []
    if not cmds.objExists(target):
        return cached

    history = cmds.listHistory(target) or []
    for node in history:
        ctype = _get_constraint_type(node)
        if not ctype:
            continue

        drivers = cmds.listConnections('{}.target'.format(node), source=True, destination=False) or []
        drivers = list(dict.fromkeys([d for d in drivers if cmds.objExists(d)]))
        if not drivers:
            continue

        cached.append({
            'constraint': node,
            'type': ctype,
            'drivers': drivers,
            'target': target
        })
    return cached
```

### Example 22 — Delete cached constraints safely

```python
def _delete_cached_constraints(cached):
    for item in cached:
        node = item.get('constraint')
        if node and cmds.objExists(node):
            cmds.delete(node)
```

### Example 23 — Restore only supported types with `mo=True`

```python
def _restore_constraints(cached):
    for item in cached:
        target = item.get('target')
        drivers = item.get('drivers', [])
        ctype = item.get('type')

        if not cmds.objExists(target):
            continue
        valid_drivers = [d for d in drivers if cmds.objExists(d)]
        if not valid_drivers:
            continue

        if ctype == 'orient':
            cmds.orientConstraint(valid_drivers, target, mo=True)
        elif ctype == 'parent':
            cmds.parentConstraint(valid_drivers, target, mo=True)
        elif ctype == 'point':
            cmds.pointConstraint(valid_drivers, target, mo=True)
        elif ctype == 'scale':
            cmds.scaleConstraint(valid_drivers, target, mo=True)
```

### Example 24 — Full temporary-unconstrain workflow

```python
def _rebuild_with_constraint_preservation(target, builder_callable):
    cached = _cache_constraints(target)
    _delete_cached_constraints(cached)
    builder_callable()
    _restore_constraints(cached)
```

### Example 25 — Rebuild only orient + parent constraints

```python
def _restore_rotation_position_constraints(cached):
    for item in cached:
        target = item.get('target')
        drivers = [d for d in item.get('drivers', []) if cmds.objExists(d)]
        ctype = item.get('type')
        if not cmds.objExists(target) or not drivers:
            continue

        if ctype == 'orient':
            cmds.orientConstraint(drivers, target, mo=True)
        elif ctype == 'parent':
            cmds.parentConstraint(drivers, target, mo=True)
```

---

## 5) Config-Driven Naming (No Hardcoded Pipeline Values)

### Example 26 — Build names with `nc`

```python
def _ctrl_name(side, region, part, nc):
    return '{}_{}_{}{}'.format(side, region, part, nc['ctrl'])
```

### Example 27 — Build joint names with `nc`

```python
def _joint_name(side, region, part, nc):
    return '{}_{}_{}{}'.format(side, region, part, nc['joint'])
```

### Example 28 — Resolve group names from setup dictionary

```python
def _base_rig_groups(setup):
    return {
        'geo': setup.get('geometry_group', 'Geometry'),
        'rig': setup.get('rig_group', 'Rig'),
        'ctrls': setup.get('controls_group', 'Controls')
    }
```

### Example 29 — Read module attr defaults with fallback

```python
def _module_attr(module_data, key, fallback=None):
    attrs = module_data.get('Attrs', {})
    return attrs.get(key, fallback)
```

### Example 30 — Use config for left/right tokens

```python
def _is_left_name(name, nc):
    left = nc.get('left', 'L')
    return name.startswith(left + '_')
```

---

## 6) Selection + Scene Validation Patterns

### Example 31 — Require exact selection count

```python
def _require_selection_count(count):
    selection = cmds.ls(sl=True) or []
    if len(selection) != count:
        cmds.warning('Expected {} selected object(s), got {}.'.format(count, len(selection)))
        return None
    return selection
```

### Example 32 — Require selected node has attr

```python
def _selected_node_with_attr(attr_name):
    selection = cmds.ls(sl=True) or []
    if not selection:
        cmds.warning('Select a node first.')
        return None

    node = selection[0]
    if not cmds.attributeQuery(attr_name, node=node, exists=True):
        cmds.warning('Node {} has no attribute {}.'.format(node, attr_name))
        return None

    return node
```

### Example 33 — Validate transform type

```python
def _is_transform(node):
    return cmds.objExists(node) and cmds.nodeType(node) == 'transform'
```

### Example 34 — Validate joint chain order safely

```python
def _valid_joint_chain(joints):
    if len(joints) < 2:
        return False
    for joint in joints:
        if not cmds.objExists(joint) or cmds.nodeType(joint) != 'joint':
            return False
    return True
```

### Example 35 — Gather descendants safely

```python
def _list_descendants(node, node_type='transform'):
    if not cmds.objExists(node):
        return []
    return cmds.listRelatives(node, ad=True, type=node_type, f=False) or []
```

---

## 7) Helper Group Strategies (No Name Clash)

### Example 36 — Unique helper per control purpose

```python
def _make_helper_group(ctrl, purpose):
    suffix = '{}Helper'.format(purpose)
    return mt.root_grp(input=ctrl, custom=True, custom_name=suffix)[0]
```

### Example 37 — Helper with side + section suffix

```python
def _make_section_helper(ctrl, side, section):
    suffix = '{}_{}_Offset'.format(side, section)
    return mt.root_grp(input=ctrl, custom=True, custom_name=suffix)[0]
```

### Example 38 — Multiple helper groups on same control

```python
def _stack_helpers(ctrl):
    first = mt.root_grp(input=ctrl, custom=True, custom_name='SpaceSwap')[0]
    second = mt.root_grp(input=ctrl, custom=True, custom_name='SdkBuffer')[0]
    third = mt.root_grp(input=ctrl, custom=True, custom_name='NoScale')[0]
    return [first, second, third]
```

---

## 8) Practical Mini Build Recipes

### Example 39 — Build FK chain controls

```python
def _build_fk_chain(joints, nc):
    ctrls = []
    for joint in joints:
        if not cmds.objExists(joint):
            continue

        ctrl = cmds.circle(name=joint.replace(nc['joint'], nc['ctrl']), normal=(1, 0, 0), ch=False)[0]
        mt.match(ctrl, joint, r=True, t=True)
        mt.root_grp(input=ctrl, custom=True, custom_name='FkOffset')
        cmds.parentConstraint(ctrl, joint, mo=True)
        ctrls.append(ctrl)

    for idx in range(1, len(ctrls)):
        cmds.parent(ctrls[idx], ctrls[idx - 1])

    return ctrls
```

### Example 40 — Build aim setup with guards

```python
def _safe_aim(source, target, up_obj):
    for node in [source, target, up_obj]:
        if not cmds.objExists(node):
            cmds.warning('Aim setup failed. Missing: {}'.format(node))
            return None

    return cmds.aimConstraint(
        target,
        source,
        aimVector=(1, 0, 0),
        upVector=(0, 1, 0),
        worldUpType='object',
        worldUpObject=up_obj,
        mo=True
    )
```

### Example 41 — Add optional visibility attr if missing

```python
def _ensure_visibility_attr(node, attr_name='secondaryVis'):
    if not cmds.objExists(node):
        return False
    if not cmds.attributeQuery(attr_name, node=node, exists=True):
        cmds.addAttr(node, ln=attr_name, at='bool', k=True, dv=1)
    return True
```

### Example 42 — Connect attr only if both sides exist

```python
def _safe_connect(src_node, src_attr, dst_node, dst_attr):
    if not cmds.objExists(src_node) or not cmds.objExists(dst_node):
        return False

    if not cmds.attributeQuery(src_attr, node=src_node, exists=True):
        return False
    if not cmds.attributeQuery(dst_attr, node=dst_node, exists=True):
        return False

    src = '{}.{}'.format(src_node, src_attr)
    dst = '{}.{}'.format(dst_node, dst_attr)
    if not cmds.isConnected(src, dst):
        cmds.connectAttr(src, dst, force=True)
    return True
```

### Example 43 — Build with optional mirroring toggle attr

```python
def build_hand_block():
    nc, curve_data, setup = mt.import_configs()
    mt.check_is_there_is_base()

    selection = cmds.ls(sl=True) or []
    if not selection:
        cmds.warning('Select hand block first.')
        return

    block = selection[0]
    should_mirror = _get_bool_attr(block, 'Mirror', default=False)

    ctrl = cmds.circle(name='Hand_Main{}'.format(nc['ctrl']), ch=False)[0]
    mt.root_grp(input=ctrl, custom=True, custom_name='HandOffset')

    if should_mirror:
        mt.mirror_group(ctrl, world=True)

    print('Built hand block: {}'.format(block))
```

### Example 44 — Build module and parent to rig group from setup

```python
def _parent_to_rig_group(node, setup):
    rig_group = setup.get('rig_group', 'Rig')
    if not cmds.objExists(node):
        return False
    if not cmds.objExists(rig_group):
        cmds.warning('Rig group not found: {}'.format(rig_group))
        return False
    cmds.parent(node, rig_group)
    return True
```

### Example 45 — Build from selected blocks loop

```python
def build_selected_blocks():
    nc, curve_data, setup = mt.import_configs()
    mt.check_is_there_is_base()

    blocks = cmds.ls(sl=True, type='transform') or []
    if not blocks:
        cmds.warning('Select one or more blocks.')
        return

    for block in blocks:
        if not cmds.objExists(block):
            continue
        print('Building {}'.format(block))
```

---

## 9) Good vs Bad Patterns

### Example 46 — Bad: hardcoded suffixes

```python
ctrl = '{}_CTRL'.format(name)
joint = '{}_JNT'.format(name)
```

### Example 47 — Good: config suffixes

```python
ctrl = '{}{}'.format(name, nc['ctrl'])
joint = '{}{}'.format(name, nc['joint'])
```

### Example 48 — Bad: no node check

```python
cmds.parentConstraint('Driver_CTRL', 'Target_JNT', mo=True)
```

### Example 49 — Good: guarded constraint

```python
if cmds.objExists('Driver_CTRL') and cmds.objExists('Target_JNT'):
    cmds.parentConstraint('Driver_CTRL', 'Target_JNT', mo=True)
else:
    cmds.warning('Driver or target missing.')
```

### Example 50 — Bad: implicit selection dependency

```python
node = cmds.ls(sl=True)[0]
```

### Example 51 — Good: explicit selection validation

```python
selection = cmds.ls(sl=True) or []
if not selection:
    cmds.warning('Select one node.')
    return
node = selection[0]
```

### Example 52 — Bad: repeated default root groups

```python
mt.root_grp(input=ctrl)
mt.root_grp(input=ctrl)
```

### Example 53 — Good: custom root group names

```python
mt.root_grp(input=ctrl, custom=True, custom_name='SdkBuffer')
mt.root_grp(input=ctrl, custom=True, custom_name='NoScale')
```

---

## 10) Complete Block Skeleton (Reference)

### Example 54 — Full create/build skeleton

```python
from maya import cmds
import os
import json

from Mutant_Tools.Utils.Rigging import main_mutant
mt = main_mutant.Mutant()


def _load_module_data(file_name):
    file_path = os.path.join(os.path.dirname(__file__), file_name)
    with open(file_path, 'r') as handle:
        return json.load(handle)


def create_example_block():
    nc, curve_data, setup = mt.import_configs()
    module = _load_module_data('99_Example.json')

    name = mt.ask_name(module.get('Name', 'Example'))
    if not name:
        cmds.warning('Cancelled create_example_block.')
        return

    block_name = '{}{}{}'.format(name, nc['module'], nc['group'])
    if cmds.objExists(block_name):
        cmds.warning('Block exists: {}'.format(block_name))
        return

    block = mt.create_block(
        name=name,
        icon=module.get('Icon', 'Generic'),
        attrs=module.get('Attrs', {}),
        build_command='build_example_block',
        import_command='create_example_block'
    )

    if block and cmds.objExists(block):
        cmds.select(block)
        print('Created {}'.format(block))


def build_example_block():
    nc, curve_data, setup = mt.import_configs()
    mt.check_is_there_is_base()

    selection = cmds.ls(sl=True) or []
    if not selection:
        cmds.warning('Select the example block to build.')
        return

    block = selection[0]
    if not cmds.objExists(block):
        cmds.warning('Block missing: {}'.format(block))
        return

    ctrl = cmds.circle(name='Example_Main{}'.format(nc['ctrl']), ch=False)[0]
    mt.match(ctrl, block, r=True, t=True)
    mt.root_grp(input=ctrl, custom=True, custom_name='ExampleOffset')

    if cmds.attributeQuery('Mirror', node=block, exists=True):
        if cmds.getAttr('{}.Mirror'.format(block)):
            mt.mirror_group(ctrl, world=True)

    print('Built {}'.format(block))
```

---

## 11) “Copy/Paste Task Prompts” for AI (Human-Friendly)

### Example 55 — Prompt for safe feature update

```text
Modify only build_arm_fk_block in this file.
Keep create_arm_fk_block unchanged.

Requirements:
- Use nc, curve_data, setup = mt.import_configs()
- Call mt.check_is_there_is_base() at build start
- Guard all Maya node operations with objExists/attributeQuery
- If adding helper groups, use mt.root_grp(..., custom=True, custom_name='...')
- Keep constraints deterministic and restore orient/parent/point/scale only
- Minimal edit, no refactor outside this function
```

### Example 56 — Prompt for adding one attr safely

```text
In build_spine_block, add a boolean attr 'SecondaryCtrls' on the block if missing.
Then use it to drive visibility of all controls named *SpineSecondary*.

Rules:
- No hardcoded naming suffixes if nc/setup alternatives exist
- Guard all missing node/attr cases
- Use cmds.warning for recoverable issues
- Keep code style consistent with file
```

### Example 57 — Prompt for scoped change only

```text
Implement the requested change only for FK arms.
Do not add leg/finger/spine logic.

Keep create/build architecture unchanged and make minimal targeted edits.
```

---

## 12) Quick Checklist Before You Merge

- `create_*` and `build_*` both still exist.
- Build starts with config import + base validation.
- No risky scene calls without existence checks.
- Helper groups use custom names when repeated.
- Constraint rebuild is deterministic and supported types only.
- User feedback uses concise `cmds.warning` / `print`.
- Scope stayed focused (no unrelated refactors).

---

## 13) Fast Troubleshooting Examples

### Example 58 — “My build does nothing”

```python
selection = cmds.ls(sl=True) or []
print('DEBUG selected:', selection)
if not selection:
    cmds.warning('Select block first.')
    return
```

### Example 59 — “Attr read fails”

```python
if not cmds.attributeQuery('Mirror', node=block, exists=True):
    cmds.warning('Mirror attr missing on {}'.format(block))
    return
mirror = cmds.getAttr('{}.Mirror'.format(block))
```

### Example 60 — “Constraint came back wrong”

```python
cached = _cache_constraints(target)
print('DEBUG cached constraints:', cached)
_delete_cached_constraints(cached)
_restore_constraints(cached)
```

---

## 14) Final Notes

If requirements are ambiguous, prefer the **simplest implementation that matches existing block patterns**.

When in doubt, prioritize:

1. Safety (`objExists`, `attributeQuery`)
2. Determinism (explicit constraint restore)
3. Consistency (existing naming/style)
4. Minimal edits (only what was requested)
