"""Standalone helper functions for ArkKit.

Scene / attribute helpers with no UI state; the UI and persistence modules
import them.
"""

from maya import cmds
import maya.OpenMayaUI as omui
import maya.api.OpenMaya as om
import shiboken6
from PySide6 import QtWidgets

from . import config


def get_maya_main_window():
    """Return Maya's main window as a QWidget so dialogs parent correctly."""
    ptr = omui.MQtUtil.mainWindow()
    return shiboken6.wrapInstance(int(ptr), QtWidgets.QWidget)


# -------- ATTRIBUTE DISCOVERY --------

def capturable_plugs(control):
    """Return the capturable "control.attr" plugs for a single control node.

    A capturable attribute is keyable, settable, unlocked and numeric — i.e.
    exactly the animatable channels an artist edits in the channel box.
    Returns an empty list if the node does not exist.
    """
    if not cmds.objExists(control):
        return []

    plugs = []
    attrs = cmds.listAttr(control, keyable=True, unlocked=True) or []

    for attr in attrs:
        full = "{}.{}".format(control, attr)

        # Skip compound parents (e.g. "translate") — we only want leaf channels
        # like translateX. Compounds report no scalar type.
        if not cmds.objExists(full):
            continue

        try:
            attr_type = cmds.getAttr(full, type=True)
        except Exception:
            continue

        if attr_type not in config.NUMERIC_ATTR_TYPES:
            continue

        # Must be settable (not driven/connected/locked).
        try:
            if not cmds.getAttr(full, settable=True):
                continue
        except Exception:
            continue

        plugs.append(full)

    return plugs


def capturable_plugs_for_controls(controls):
    """Flatten capturable_plugs() across an ordered list of control nodes.

    Returns (plugs, missing) where `plugs` is the ordered, de-duplicated list
    of "control.attr" strings and `missing` lists any control nodes that were
    not found in the scene.
    """
    plugs = []
    seen = set()
    missing = []

    for control in controls:
        if not cmds.objExists(control):
            missing.append(control)
            continue
        for plug in capturable_plugs(control):
            if plug not in seen:
                seen.add(plug)
                plugs.append(plug)

    return plugs, missing


def get_plug_value(plug):
    """Safely read a plug value, returning None on failure."""
    try:
        return float(cmds.getAttr(plug))
    except Exception:
        return None


def set_plug_value(plug, value):
    """Safely set a plug value; returns True on success.

    Silently skips plugs that no longer exist or are not settable so a single
    stale control does not abort a whole blend/apply pass.
    """
    if not cmds.objExists(plug):
        return False
    try:
        if not cmds.getAttr(plug, settable=True):
            return False
        cmds.setAttr(plug, value)
        return True
    except Exception:
        return False


# -------- MESH SELECTION --------

def filter_meshes(selection_list):
    """Return only the transforms in `selection_list` that have a mesh shape."""
    filtered = []
    for obj in selection_list or []:
        shapes = cmds.listRelatives(obj, shapes=True, fullPath=True) or []
        for shape in shapes:
            if cmds.objectType(shape) == "mesh" and obj not in filtered:
                filtered.append(obj)
    return filtered


def selected_meshes():
    """Return the currently selected mesh transforms (short names), or []."""
    selection = cmds.ls(selection=True, long=False) or []
    return filter_meshes(selection)


def selected_transforms():
    """Return the currently selected transform nodes (short names), or []."""
    return cmds.ls(selection=True, transforms=True, long=False) or []


# -------- MIRROR: NAMES --------

def split_plug(plug):
    """Split a "node.attr" plug into (node, attr). Attrs are leaf channels, so
    the first '.' separates them (node names may contain ':' but not '.')."""
    node, _, attr = plug.partition(".")
    return node, attr


def mirror_counterpart(node):
    """Return the opposite-side control name for ``node`` via config.MIRROR_PAIRS,
    or None if the name carries no side token (a center control)."""
    for left, right in config.MIRROR_PAIRS:
        if left in node:
            return node.replace(left, right)
        if right in node:
            return node.replace(right, left)
    return None


def control_side(node):
    """Return 'L', 'R' or None (center) for ``node`` per config.MIRROR_PAIRS."""
    for left, right in config.MIRROR_PAIRS:
        if left in node:
            return "L"
        if right in node:
            return "R"
    return None


# -------- MIRROR: WORLD-SPACE PROBE MATH (ported from AnimTools) --------

def plane_normal(axis):
    """Return the mirror plane's world-space unit normal as an MVector."""
    idx = {"x": 0, "y": 1, "z": 2}.get(axis, 0)
    return om.MVector(*[(1, 0, 0), (0, 1, 0), (0, 0, 1)][idx])


def reflection_from_normal(normal):
    """4x4 reflection MMatrix (rotation only) across the plane with this normal."""
    nx, ny, nz = normal.x, normal.y, normal.z
    return om.MMatrix([
        1 - 2 * nx * nx, -2 * nx * ny, -2 * nx * nz, 0.0,
        -2 * ny * nx, 1 - 2 * ny * ny, -2 * ny * nz, 0.0,
        -2 * nz * nx, -2 * nz * ny, 1 - 2 * nz * nz, 0.0,
        0.0, 0.0, 0.0, 1.0,
    ])


def world_position(node):
    return om.MVector(*cmds.xform(node, query=True, worldSpace=True, translation=True))


def world_rotation(node):
    """World matrix of ``node`` with translation stripped (isolates rotation)."""
    m = list(cmds.xform(node, query=True, worldSpace=True, matrix=True))
    m[12] = m[13] = m[14] = 0.0
    return om.MMatrix(m)


def matrix_distance(a, b):
    return sum((a[i] - b[i]) ** 2 for i in range(16))


def probe_channel_sign(source, target, channel, normal, reflect):
    """Return +1.0/-1.0 for how ``channel`` inverts from ``source`` to ``target``.

    Nudges the channel on both controls, compares how ``source`` moves in world
    to the mirror of that motion, and picks the sign of ``target``'s response
    that matches. Returns None if the channel isn't probeable on both. Values
    are restored, so the scene pose is left untouched.
    """
    src_plug = "{}.{}".format(source, channel)
    tgt_plug = "{}.{}".format(target, channel)
    if not (cmds.objExists(src_plug) and cmds.objExists(tgt_plug)):
        return None
    try:
        if not (cmds.getAttr(src_plug, settable=True) and cmds.getAttr(tgt_plug, settable=True)):
            return None
    except Exception:
        return None

    is_translate = channel.startswith("translate")
    delta = 1.0 if is_translate else 15.0

    if is_translate:
        base = cmds.getAttr(src_plug)
        p0 = world_position(source)
        cmds.setAttr(src_plug, base + delta)
        d_source = world_position(source) - p0
        cmds.setAttr(src_plug, base)

        base = cmds.getAttr(tgt_plug)
        q0 = world_position(target)
        cmds.setAttr(tgt_plug, base + delta)
        d_target = world_position(target) - q0
        cmds.setAttr(tgt_plug, base)

        if d_source.length() < 1e-6 or d_target.length() < 1e-6:
            return None
        expected = d_source - 2.0 * (d_source * normal) * normal  # reflect vector
        return 1.0 if (expected * d_target) >= 0.0 else -1.0

    # rotation: compare world rotation deltas as matrices
    base = cmds.getAttr(src_plug)
    r0 = world_rotation(source)
    cmds.setAttr(src_plug, base + delta)
    dr_source = r0.inverse() * world_rotation(source)
    cmds.setAttr(src_plug, base)

    base = cmds.getAttr(tgt_plug)
    r0t = world_rotation(target)
    cmds.setAttr(tgt_plug, base + delta)
    dr_target = r0t.inverse() * world_rotation(target)
    cmds.setAttr(tgt_plug, base)

    mirrored = reflect * dr_source * reflect
    d_pos = matrix_distance(list(mirrored), list(dr_target))
    d_neg = matrix_distance(list(mirrored), list(dr_target.inverse()))
    return 1.0 if d_pos <= d_neg else -1.0
