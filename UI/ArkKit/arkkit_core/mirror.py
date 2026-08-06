"""Mirroring logic for ArkKit — no UI state.

Adapted from the AnimTools per-channel, default-relative mirror method. Because
ArkKit stores each expression as a delta from the captured default, mirroring a
stored expression reduces to ``mirrored_delta = sign * src_delta`` on the
name-matched counterpart control — only the one-time snapshot needs the live rig.

The sign table is ``{control: {channel: +1/-1}}``; channels the probe can't
measure geometrically (custom / non-transform attrs) default to +1, i.e. the
opposite control receives the same value.
"""

from maya import cmds

from . import config
from . import utils


# -------- SNAPSHOT (needs the live rig) --------

def snapshot(controls, defaults, axis=None):
    """Learn the per-control, per-channel mirror signs by probing the live rig.

    Applies the captured defaults first so the rig is at its neutral pose (the
    probe's world-motion comparison is only valid there), probes the six
    transform channels for each control + its counterpart (both directions), and
    assigns +1 to every other capturable channel. Returns
    ``{control: {channel: sign}, "__meta__": {"axis": axis}}``.
    """
    axis = (axis or config.MIRROR_AXIS or "x").lower()
    if axis not in ("x", "y", "z"):
        axis = "x"

    normal = utils.plane_normal(axis)
    reflect = utils.reflection_from_normal(normal)

    table = {}

    auto_key = cmds.autoKeyframe(query=True, state=True)
    cmds.autoKeyframe(state=False)
    cmds.undoInfo(openChunk=True)
    try:
        # Neutral pose so the world-motion probe is meaningful.
        for plug, value in defaults.items():
            utils.set_plug_value(plug, value)

        for ctrl in controls:
            if not cmds.objExists(ctrl):
                continue

            counterpart = utils.mirror_counterpart(ctrl)
            paired = bool(counterpart and cmds.objExists(counterpart))
            directions = (((ctrl, counterpart), (counterpart, ctrl)) if paired
                          else ((ctrl, ctrl),))

            for src, tgt in directions:
                signs = {}

                # Transform channels — geometric probe.
                for ch in config.MIRROR_TRANSFORM_CHANNELS:
                    sign = utils.probe_channel_sign(src, tgt, ch, normal, reflect)
                    if sign is not None:
                        signs[ch] = sign

                # Everything else capturable on this control -> same-value (+1).
                for plug in utils.capturable_plugs(src):
                    _, attr = utils.split_plug(plug)
                    if attr not in signs:
                        signs[attr] = config.MIRROR_DEFAULT_SIGN

                if signs:
                    table[src] = signs
    finally:
        cmds.undoInfo(closeChunk=True)
        cmds.autoKeyframe(state=auto_key)

    table["__meta__"] = {"axis": axis}
    return table


# -------- MIRROR / SYMMETRIZE STORED DELTAS (no live rig needed) --------

def _sign_for(signs, node, attr):
    return signs.get(node, {}).get(attr, config.MIRROR_DEFAULT_SIGN)


def mirror_delta(delta, signs):
    """Return the opposite-side delta: for each ``node.attr -> d`` produce
    ``counterpart(node).attr -> sign * d`` (center controls map in place)."""
    result = {}
    for plug, d in delta.items():
        node, attr = utils.split_plug(plug)
        target = utils.mirror_counterpart(node) or node
        result["{}.{}".format(target, attr)] = _sign_for(signs, node, attr) * d
    return result


def symmetrize_delta(delta, signs, source_side="L"):
    """Return a bilaterally symmetric delta by copying the ``source_side`` (and
    center controls) onto the opposite side — a one-way copy, not a swap."""
    target_side = "R" if source_side == "L" else "L"

    # Keep source-side + center; drop the target side (it gets rewritten).
    result = {}
    for plug, d in delta.items():
        node, _ = utils.split_plug(plug)
        if utils.control_side(node) == target_side:
            continue
        result[plug] = d

    for plug, d in list(result.items()):
        node, attr = utils.split_plug(plug)
        side = utils.control_side(node)
        if side == source_side:
            target = utils.mirror_counterpart(node) or node
        elif side is None:
            target = node  # center: mirror in place
        else:
            continue
        result["{}.{}".format(target, attr)] = _sign_for(signs, node, attr) * d

    return result


# -------- SYMMETRIZE THE LIVE POSE (during recording) --------

def symmetrize_live(defaults, signs, source_side="L"):
    """Make the LIVE rig pose symmetric by copying the ``source_side`` (and
    center controls) onto the opposite side. Used while recording so the pose
    captured on stop is symmetric. Returns the number of channels written.
    """
    count = 0
    cmds.undoInfo(openChunk=True)
    try:
        for plug, src_def in defaults.items():
            node, attr = utils.split_plug(plug)
            side = utils.control_side(node)
            if side == source_side:
                target = utils.mirror_counterpart(node) or node
            elif side is None:
                target = node  # center: mirror in place
            else:
                continue  # target-side controls are written as counterparts

            src_val = utils.get_plug_value(plug)
            if src_val is None:
                continue

            target_plug = "{}.{}".format(target, attr)
            tgt_def = defaults.get(target_plug, src_def)
            mirrored = tgt_def + _sign_for(signs, node, attr) * (src_val - src_def)
            if utils.set_plug_value(target_plug, mirrored):
                count += 1
    finally:
        cmds.undoInfo(closeChunk=True)
    return count
