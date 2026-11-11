"""Mutant blocks without the UI: create, configure and build from a script.

Runs INSIDE Maya. Block create functions ask for names in a prompt dialog
(mt.ask_name), which would block a bridge call: create_block() answers those
prompts from a list instead. build_rig() runs the Auto Rigger build the same
way its Build button does, with the rebuild question answered.

    from Mutant_Tools.Dev.MayaMCP import block_build as bb
    bb.create_block('Chain', answers=['L_Toe', '3'], parent='Body', after='L_Foot_Block',
                    attrs={'SetParent': 'L_Foot_Ball_Jnt', 'Mirror': True, 'CtrlType': 'octagon'})
    bb.build_rig()              # first build, or delete and rebuild
"""
import importlib
import io
import json
import os
import re
import sys
import tempfile
import time
from pathlib import Path

import maya.cmds as mc

BLOCKS_DIR = Path(__file__).resolve().parents[2] / 'Blocks'
_VERSION = re.compile(r'_v\d+$')


# --------------------------------------------------------------------------
# Finding and creating blocks
# --------------------------------------------------------------------------
def find_block(name):
    """Launcher info of a block from any common way to name it.

    name: folder ('08_Chain'), folder without its number ('Chain'), the
    block's JSON 'Name', or the exec module ('exec_chain', 'exec_chain_v001').
    Returns {'folder', 'module', 'create', 'build', 'json'}; the module and
    commands are the ones the launcher JSON points at (its current version).
    """
    key = name.lower()
    matches = []
    for js in sorted(BLOCKS_DIR.glob('*/*/*.json')):
        if js.stem != js.parent.name:          # launcher JSON only (no _v00X copies)
            continue
        try:
            data = json.loads(js.read_text())
        except (ValueError, OSError):
            continue
        module = str(data.get('python_file', '')).replace('.py', '')
        folder = js.parent.name
        names = {folder.lower(), folder.split('_', 1)[-1].lower(), str(data.get('Name', '')).lower(),
                 module.lower(), _VERSION.sub('', module).lower()}
        if key in names:
            matches.append((folder, module, data, js))
    if not matches:
        raise ValueError('no block called {}'.format(name))
    if len(matches) > 1:
        raise ValueError('{} matches several blocks: {}'.format(
            name, ', '.join('{}/{}'.format(m[3].parent.parent.name, m[0]) for m in matches)))
    folder, module, data, js = matches[0]
    create = str(data['exec_command']).split('.', 1)[1].split('(')[0]
    build = str(data['build_command']).split('.', 1)[1].split('(')[0]
    return {'folder': str(js.parent), 'module': module, 'create': create, 'build': build, 'json': str(js)}


def _import(info):
    if info['folder'] not in sys.path:
        sys.path.insert(0, info['folder'])
    mod = importlib.import_module(info['module'])
    return importlib.reload(mod)


def _all_blocks(suffix):
    return set(mc.ls('*' + suffix))


def create_block(block, answers, parent=None, after=None, attrs=None):
    """Create a block the way its tab button does, with the prompts answered.

    answers: the replies to its name prompts, in order (Chain asks the name,
    then the joint count; most blocks only ask the name). parent: a group
    under Mutant_Build to put it in ('Body', 'Extras'...); after: an existing
    block to place it right after (build order is outliner order); attrs:
    settings for set_block_attrs(). Returns {'blocks', 'configs', 'guides'}.
    """
    info = find_block(block)
    mod = _import(info)
    mt = mod.mt
    suffix = mt.import_configs()[0]['module']
    queue = list(answers)

    def ask_name(*args, **kwargs):
        if not queue:
            raise ValueError('create_block: {} asked more questions than the {} answers given'.format(
                block, len(answers)))
        return queue.pop(0)

    before = _all_blocks(suffix)
    original = mt.ask_name
    mt.ask_name = ask_name
    try:
        getattr(mod, info['create'])()
    finally:
        mt.ask_name = original
    new = sorted(_all_blocks(suffix) - before)
    if not new:
        raise RuntimeError('{} created no block (name taken, or the prompt was refused)'.format(block))
    for b in new:
        if parent:
            if not mc.objExists(parent):
                raise ValueError('parent group {} does not exist'.format(parent))
            if (mc.listRelatives(b, p=True) or [''])[0] != parent:
                mc.parent(b, parent)
        if after:
            siblings = mc.listRelatives(mc.listRelatives(b, p=True)[0], c=True)
            if after not in siblings:
                raise ValueError('{} is not next to {} (different group)'.format(after, b))
            mc.reorder(b, r=siblings.index(after) + 1 - siblings.index(b))
        if attrs:
            set_block_attrs(b, attrs)
    return {'blocks': new, 'configs': [block_config(b) for b in new],
            'guides': [g for b in new for g in (mc.listRelatives(b, ad=True, type='transform') or [])
                       if not g.endswith('Shape')]}


def block_config(block):
    """The config (network) node of a block."""
    nets = [n for n in mc.listConnections(block) or [] if mc.nodeType(n) == 'network']
    if not nets:
        raise ValueError('{} has no config node'.format(block))
    return nets[0]


def set_block_attrs(block, attrs):
    """Set block settings by name; enums take their label ('octagon') or index.

    Returns {attr: value as stored} for what was set. Unknown attrs raise,
    so a typo never silently builds with the default.
    """
    cfg = block_config(block)
    done = {}
    for name, value in attrs.items():
        if not mc.attributeQuery(name, n=cfg, exists=True):
            raise ValueError('{} has no setting {}'.format(block, name))
        plug = '{}.{}'.format(cfg, name)
        kind = mc.getAttr(plug, type=True)
        if kind == 'enum':
            labels = mc.attributeQuery(name, n=cfg, le=True)[0].split(':')
            if isinstance(value, str) and not value.isdigit():
                if value not in labels:
                    raise ValueError('{}: {} is not one of {}'.format(name, value, labels))
                value = labels.index(value)
            mc.setAttr(plug, int(value))
            done[name] = labels[int(value)]
        elif kind == 'string':
            mc.setAttr(plug, str(value), type='string')
            done[name] = str(value)
        else:
            mc.setAttr(plug, value)
            done[name] = mc.getAttr(plug)
    return done


# --------------------------------------------------------------------------
# Building
# --------------------------------------------------------------------------
_MODES = {'first': 'First Build', 'delete': 'Delete and Rebuild', 'just': 'Just Rebuild'}


def build_rig(mode='auto', rename_skins=True, log_lines=40):
    """Build every block like the Auto Rigger's Build button, no dialogs.

    mode: 'auto' (first build, or delete and rebuild when a rig exists),
    'first', 'delete' (saves skins / controller shapes and loads them back)
    or 'just'. The build reverts itself if a block fails (Mutant's Revert on
    Fail option). rename_skins: the rebuild loads skins back as
    skinClusterNN, so give each mesh its skinCluster name back.
    Returns {'ok', 'failed', 'reverted', 'error', 'seconds', 'renamed', 'log'}.
    """
    exists = mc.objExists('Mutant_Tools_Grp')
    if mode == 'auto':
        mode = 'delete' if exists else 'first'
    if mode not in _MODES:
        raise ValueError('mode must be auto, first, delete or just')
    if mode == 'first' and exists:
        raise ValueError('a rig is already built: use delete or just')
    # A rebuild loads the Skeleton hierarchy it saved from the old rig. When the
    # old rig had no Skeleton nothing is saved and an older file (any scene) is
    # read instead -- or the build stops when there is none. Start it empty.
    if mode != 'first' and not mc.objExists('Skeleton'):
        folder = os.path.join(tempfile.gettempdir(), 'RebuildTemp')
        os.makedirs(folder, exist_ok=True)
        open(os.path.join(folder, 'skeleton_hierarchy.txt'), 'w').close()
    skins = {}
    if rename_skins:
        for sc in mc.ls(type='skinCluster'):
            for geo in mc.skinCluster(sc, q=True, g=True) or []:
                skins[geo] = sc
    failed = []
    out, buf = sys.stdout, io.StringIO()
    start = time.time()
    sys.stdout = buf   # the Auto Rigger prints its whole log (and menu code on import)
    builder = None
    try:
        from Mutant_Tools.UI.AutoRigger import load_autoRigger
        importlib.reload(load_autoRigger)
        builder = load_autoRigger.AutoRigger()
        builder.check_if_previous_build = lambda: _MODES[mode]
        builder.view_log = lambda: failed.append(True)
        builder.build_autorigger(only_progressbar=True)
    finally:
        sys.stdout = out
        if builder is not None:
            try:
                builder.close()
            except Exception:
                pass
    text = buf.getvalue()
    result = {'ok': not failed, 'failed': None, 'reverted': False, 'error': None}
    for line in text.splitlines():
        if line.startswith('[Mutant Result] '):
            try:
                data = json.loads(line[len('[Mutant Result] '):])
            except ValueError:
                continue
            result.update(ok=bool(data.get('ok')), failed=data.get('failed'),
                          reverted=bool(data.get('reverted')), error=data.get('error'))
    renamed = {}
    if rename_skins and result['ok']:
        for geo, name in skins.items():
            if not mc.objExists(geo):
                continue
            now = mc.ls(mc.listHistory(geo, pdo=True) or [], type='skinCluster')
            if now and now[0] != name and not mc.objExists(name):
                renamed[now[0]] = mc.rename(now[0], name)
    result.update(seconds=round(time.time() - start, 1), renamed=renamed,
                  log=text.splitlines()[-log_lines:] if log_lines else [])
    return result
