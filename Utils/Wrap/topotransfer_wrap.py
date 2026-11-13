"""
Zombinator wrap step without Wrap 3D: TopoTransfer does the same job.

The Zombinator fits its base mesh (Utils/Wrap/BaseMesh/<base>/Alembic/Body.abc or Face.abc) onto your character
and brings it back as `transf0`, the base topology in your character's shape. The guides, the base skin and the
skin copy all read `transf0`, so they work the same whichever tool made it.

    from Mutant_Tools.Utils.Wrap import topotransfer_wrap as ttw
    ttw.wrap3d_command()                      # the Wrap 3D command if it is installed, else None
    link = ttw.wrap('MyCharacter_geo', base_mesh='WrapBaseMesh', mode='Body', on_done=print)
    # TopoTransfer opens with the base mesh and your character: place points, wrap, Export.
    # on_done('transf0') runs when the result is back in Maya. Keep `link` alive until then; link.stop() ends it.

Wrap 3D presets come with point pairs; in TopoTransfer you place the guides in its Guides step (or let it align
on its own for a human-like character).
"""

from __future__ import annotations

import glob
import os
import shutil
import sys

import maya.cmds as cmds

HERE = os.path.dirname(os.path.abspath(__file__))
MUTANT = os.path.dirname(os.path.dirname(HERE))
TT_MAYA = os.path.join(MUTANT, 'Utils', 'TopoTransfer', 'maya')
RESULT = 'transf0'
BASE_GRP = 'Zombinator_TopoTransfer_Base_Grp'


def wrap3d_command():
    """The command that starts Wrap 3D, or None when it isn't installed."""
    for name in ('r3ds_wrap', 'Wrap', 'wrap3d'):
        path = shutil.which(name)
        if path:
            return [path]
    if shutil.which('sclenv'):                       # studio Linux: Wrap 3D comes through the environment launcher
        return ['sclenv', 'r3ds_wrap']
    if sys.platform == 'darwin':
        apps = sorted(glob.glob('/Applications/Wrap*.app') + glob.glob(os.path.expanduser('~/Applications/Wrap*.app')))
        if apps:
            return ['open', '-a', apps[-1]]
    if sys.platform.startswith('win'):
        for root in (os.environ.get('ProgramFiles', r'C:\Program Files'), os.environ.get('ProgramFiles(x86)', '')):
            exes = sorted(glob.glob(os.path.join(root, 'R3DS', 'Wrap*', 'Wrap.exe'))) if root else []
            if exes:
                return [exes[-1]]
    return None


def base_alembic(base_mesh='WrapBaseMesh', mode='Body'):
    path = os.path.join(MUTANT, 'Utils', 'Wrap', 'BaseMesh', base_mesh, 'Alembic', '{}.abc'.format('Face' if mode == 'Face' else 'Body'))
    if not os.path.exists(path):
        raise RuntimeError('No base mesh for {} ({}): {}'.format(base_mesh, mode, path))
    return path


def import_base(base_mesh='WrapBaseMesh', mode='Body'):
    """Import the Zombinator base mesh into its own hidden group and return its transform."""
    if not cmds.pluginInfo('AbcImport', q=True, loaded=True):
        cmds.loadPlugin('AbcImport', quiet=True)
    before = set(cmds.ls(assemblies=True, l=True))
    cmds.AbcImport(base_alembic(base_mesh, mode), mode='import')
    new = [n for n in cmds.ls(assemblies=True, l=True) if n not in before]
    meshes = [t for t in new if cmds.listRelatives(t, ad=True, type='mesh', f=True)]
    if not meshes:
        raise RuntimeError('The base mesh Alembic has no mesh: {}'.format(base_alembic(base_mesh, mode)))
    shape = max((s for t in meshes for s in cmds.listRelatives(t, ad=True, type='mesh', f=True) if not cmds.getAttr(s + '.intermediateObject')),
                key=lambda s: cmds.polyEvaluate(s, v=True))
    base = cmds.listRelatives(shape, p=True, f=True)[0]
    if not cmds.objExists(BASE_GRP):
        cmds.group(em=True, n=BASE_GRP)
    base = cmds.parent(base, BASE_GRP)[0]
    for n in new:
        if cmds.objExists(n) and not cmds.listRelatives(n, ad=True):
            cmds.delete(n)
    base = cmds.rename(base, 'Zombinator_{}_Base'.format(mode))
    cmds.setAttr(BASE_GRP + '.visibility', 0)
    return base


def _take_result(copy):
    """The wrapped copy becomes transf0 (an older transf0 is kept, renamed)."""
    if cmds.objExists(RESULT) and cmds.ls(RESULT, l=True)[0] != cmds.ls(copy, l=True)[0]:
        cmds.rename(RESULT, RESULT + '_old#')
    if cmds.listRelatives(copy, p=True):
        copy = cmds.parent(copy, w=True)[0]
    copy = cmds.rename(copy, RESULT)
    for s in cmds.listRelatives(copy, s=True, f=True) or []:
        cmds.rename(s, RESULT + 'Shape')
    cmds.setAttr(copy + '.visibility', 1)
    return copy


def wrap(reference, base_mesh='WrapBaseMesh', mode='Body', on_done=None, on_error=None, open_browser=True):
    """Fit the Zombinator base mesh onto `reference` (your character's geo) in TopoTransfer, the way Wrap 3D would.
    Returns the TopoTransfer link; on_done('transf0') runs when the wrapped mesh is back."""
    if not reference or not cmds.objExists(reference):
        raise RuntimeError('Select your character geo first (the mesh the base mesh should wrap onto).')
    if TT_MAYA not in sys.path:
        sys.path.insert(0, TT_MAYA)
    import tt_maya
    base = import_base(base_mesh, mode)

    def arrived(copy):
        try:
            name = _take_result(copy)
        except Exception as error:
            if on_error:
                on_error(str(error))
            return
        print('Zombinator: {} is the {} base mesh wrapped onto {} (TopoTransfer).'.format(name, base_mesh, reference))
        if on_done:
            on_done(name)

    return tt_maya.send(base, reference, on_result=arrived, on_error=on_error, open_browser=open_browser)
