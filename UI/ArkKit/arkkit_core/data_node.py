"""Persistence layer for ArkKit.

All authored data lives on a single scene transform node (``ArkKit_Data``) as
JSON string attributes, so the work survives a Maya restart. This module is the
only place that reads/writes those attributes, and it also handles JSON
export/import so a setup can be moved to another rig with matching control
names.

On-node layout (see config.py for the exact attribute names):
    akDefaults        JSON {"ctrl.attr": value}    captured neutral pose
    akControls        JSON ["ctrlA", ...]          controls used at capture time
    akGeos            JSON ["geoA", ...]           remembered bake targets
    akExpr_<name>     JSON {"ctrl.attr": delta}    one attr per recorded expression
"""

import json

from maya import cmds

from . import config


# -------- NODE --------

def exists():
    """True if the ArkKit data node is present in the scene."""
    return cmds.objExists(config.DATA_NODE)


def get_or_create():
    """Return the ArkKit data node, creating it (a plain transform) if needed."""
    if cmds.objExists(config.DATA_NODE):
        return config.DATA_NODE

    node = cmds.createNode("transform", name=config.DATA_NODE)
    try:
        cmds.setAttr(node + ".isHistoricallyInteresting", 0)
    except Exception:
        pass

    # Keep it out of the way in the viewport but visible/selectable in the
    # outliner so the artist can find and delete it if they ever need to.
    for attr in ("tx", "ty", "tz", "rx", "ry", "rz", "sx", "sy", "sz"):
        try:
            cmds.setAttr("{}.{}".format(node, attr), lock=True, keyable=False)
        except Exception:
            pass

    return node


def delete_node():
    """Remove the ArkKit data node entirely (wipes all authored data)."""
    if cmds.objExists(config.DATA_NODE):
        cmds.delete(config.DATA_NODE)


# -------- LOW-LEVEL JSON STRING ATTRS --------

def _ensure_string_attr(node, attr):
    if not cmds.attributeQuery(attr, node=node, exists=True):
        cmds.addAttr(node, longName=attr, dataType="string")


def _write_json_attr(attr, obj):
    """Serialize `obj` to JSON and store it on `attr` of the data node."""
    node = get_or_create()
    _ensure_string_attr(node, attr)
    cmds.setAttr("{}.{}".format(node, attr), json.dumps(obj), type="string")


def _read_json_attr(attr, default):
    """Read+parse a JSON string attr, returning `default` if absent/invalid."""
    if not cmds.objExists(config.DATA_NODE):
        return default
    full = "{}.{}".format(config.DATA_NODE, attr)
    if not cmds.objExists(full):
        return default
    raw = cmds.getAttr(full)
    if not raw:
        return default
    try:
        return json.loads(raw)
    except (ValueError, TypeError):
        return default


# -------- DEFAULTS / CONTROLS / GEOS --------

def write_defaults(defaults):
    """Store the captured neutral pose {plug: value}."""
    _write_json_attr(config.DEFAULTS_ATTR, defaults)


def read_defaults():
    """Return the captured neutral pose {plug: value} (or {})."""
    return _read_json_attr(config.DEFAULTS_ATTR, {})


def has_defaults():
    return bool(read_defaults())


def write_controls(controls):
    """Store the control-node list used at capture time."""
    _write_json_attr(config.CONTROLS_ATTR, list(controls))


def read_controls():
    """Return the stored control-node list (or [])."""
    return _read_json_attr(config.CONTROLS_ATTR, [])


def write_geos(geos):
    """Store the remembered bake-target geo list."""
    _write_json_attr(config.GEOS_ATTR, list(geos))


def read_geos():
    """Return the remembered bake-target geo list (or [])."""
    return _read_json_attr(config.GEOS_ATTR, [])


# -------- MIRROR TABLE --------

def write_mirror(table):
    """Store the learned mirror sign table {control: {channel: sign}, __meta__}."""
    _write_json_attr(config.MIRROR_ATTR, table)


def read_mirror():
    """Return the learned mirror sign table (or {})."""
    return _read_json_attr(config.MIRROR_ATTR, {})


def has_mirror():
    return bool({k for k in read_mirror() if k != "__meta__"})


# -------- EXPRESSIONS --------

def _expr_attr(name):
    return config.EXPR_ATTR_PREFIX + name


def write_expression(name, delta):
    """Store one expression's delta dict {plug: delta}."""
    _write_json_attr(_expr_attr(name), delta)


def read_expression(name):
    """Return one expression's delta dict {plug: delta}, or {} if unset."""
    return _read_json_attr(_expr_attr(name), {})


def has_expression(name):
    """True if the expression has been recorded (its attr exists & non-empty)."""
    return bool(read_expression(name))


def delete_expression(name):
    """Remove one expression's stored attr, if present."""
    if not cmds.objExists(config.DATA_NODE):
        return
    full = "{}.{}".format(config.DATA_NODE, _expr_attr(name))
    if cmds.objExists(full):
        try:
            cmds.deleteAttr(full)
        except Exception:
            pass


def all_expressions():
    """Return {name: delta_dict} for every recorded expression on the node."""
    result = {}
    if not cmds.objExists(config.DATA_NODE):
        return result

    attrs = cmds.listAttr(config.DATA_NODE, userDefined=True) or []
    prefix = config.EXPR_ATTR_PREFIX
    for attr in attrs:
        if attr.startswith(prefix):
            name = attr[len(prefix):]
            result[name] = read_expression(name)
    return result


# -------- EXPORT / IMPORT --------

def export_json(path):
    """Write the full ArkKit dataset to a JSON file.

    Structure: {"defaults": {...}, "controls": [...], "geos": [...],
                "expressions": {name: {plug: delta}}}
    """
    payload = {
        "defaults": read_defaults(),
        "controls": read_controls(),
        "geos": read_geos(),
        "mirror": read_mirror(),
        "expressions": all_expressions(),
    }
    with open(path, "w") as f:
        json.dump(payload, f, indent=4)
    return payload


def import_json(path):
    """Load an ArkKit dataset from a JSON file onto the data node.

    Creates the node if needed and overwrites defaults/controls/geos and every
    expression present in the file. Returns the parsed payload.
    """
    with open(path, "r") as f:
        payload = json.load(f)

    get_or_create()

    write_defaults(payload.get("defaults", {}))
    write_controls(payload.get("controls", []))
    write_geos(payload.get("geos", []))

    mirror = payload.get("mirror")
    if mirror:
        write_mirror(mirror)

    for name, delta in (payload.get("expressions", {}) or {}).items():
        write_expression(name, delta)

    return payload
