"""Static configuration and data for ArkKit.

Constants, UI groupings/colors, and the data loaded from the JSON files in
./data (the 52 ARKit blendshape names and the rig control list).
"""

import json
import os


# -------- PATHS --------
# All asset paths are resolved relative to this package folder, so the whole
# tool is portable: drop the package anywhere on Maya's script path and its
# data files travel with it.
_HERE = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(_HERE, "data")

# Default folder for Export / Import of per-character ArkKit datasets. Kept
# separate from data/ (the tool's static config) so exports never mingle with
# controls.json / blendshapes.json.
EXPORTS_DIR = os.path.join(_HERE, "exports")


def _pkg_path(*parts):
    """Build an absolute path inside the package, with forward slashes.

    Maya's file commands prefer forward slashes on Windows, so we normalize
    here rather than handing Maya the OS-native backslashes from os.path.join.
    """
    return os.path.join(_HERE, *parts).replace(os.sep, "/")


# -------- VERSION --------
# Bumped on every change to the tool. Shown in the UI so a reload can be
# verified as having picked up the latest code.
VERSION = "1.4.0"


# -------- CONSTANTS --------
# The single scene node that stores all authored ArkKit data. Created the
# first time "Set Defaults" runs so the work survives a Maya restart.
DATA_NODE = "ArkKit_Data"

# String-attribute names on DATA_NODE.
DEFAULTS_ATTR = "akDefaults"      # JSON {"ctrl.attr": value}
CONTROLS_ATTR = "akControls"      # JSON ["ctrlA", "ctrlB", ...]
GEOS_ATTR = "akGeos"              # JSON ["geoA", "geoB", ...] (remembered targets)
EXPR_ATTR_PREFIX = "akExpr_"      # one attr per expression: akExpr_<name>

# Blendshape node created per geo when baking (e.g. "head_geo_ArkKit_BS").
BLENDSHAPE_SUFFIX = "_ArkKit_BS"

# Numeric attribute types we treat as capturable channels.
NUMERIC_ATTR_TYPES = ("double", "float", "doubleLinear", "doubleAngle", "long", "short")

# Deltas smaller than this are treated as "no change" and not stored.
DELTA_EPSILON = 1e-6

# -------- MIRRORING --------
# String attr on DATA_NODE holding the learned per-channel signs:
#   {control: {channel: +1/-1}, "__meta__": {"axis": "x"}}
MIRROR_ATTR = "akMirror"

# World axis of the character's left/right mirror plane NORMAL. A character
# facing +Z or -Z (the Maya default) mirrors across the YZ plane, so this is
# "x". If mirrored signs come out wrong, change this and re-run Snapshot Mirror.
MIRROR_AXIS = "x"

# Sign used for channels the snapshot cannot geometrically probe (custom / non-
# transform attrs): the opposite control gets the SAME value.
MIRROR_DEFAULT_SIGN = 1.0

# The transform channels the snapshot probes by nudging + comparing world motion.
MIRROR_TRANSFORM_CHANNELS = [
    "translateX", "translateY", "translateZ",
    "rotateX", "rotateY", "rotateZ",
]

# Left/right token pairs for finding a CONTROL NODE's mirror counterpart by name.
# Checked in order; the first token found in the name is swapped. Tune to match
# your rig. More specific (underscore-delimited) pairs first.
MIRROR_PAIRS = [
    ("_L_", "_R_"),
    ("_lf_", "_rt_"),
    ("L_", "R_"),
    ("lf_", "rt_"),
    ("_L", "_R"),
    ("_lf", "_rt"),
    (":L", ":R"),
    ("Left", "Right"),
    ("left", "right"),
]

# Slider integer range (maps the 0..1 blend weight to integer slider steps).
# Kept modest so a full drag emits hundreds — not thousands — of updates.
SLIDER_RESOLUTION = 1000


# -------- DATA LOADING --------
def _load_json(filename):
    """Loads a JSON file from the local data/ directory."""
    path = os.path.join(DATA_DIR, filename)
    with open(path, "r") as f:
        return json.load(f)


# {group_name: [blendshape_name, ...]} — drives the collapsible UI sections and
# the master expression list.
BLENDSHAPE_GROUPS = _load_json("blendshapes.json")

# Flat, ordered list of all 52 ARKit expression names.
EXPRESSIONS = [name for names in BLENDSHAPE_GROUPS.values() for name in names]


def load_controls():
    """Read the control list from data/controls.json.

    Read fresh (not cached) so hand-edits to the file are picked up on the next
    UI refresh without reloading the package.
    """
    data = _load_json("controls.json")
    return list(data.get("controls", []))


# -------- COLORS --------
# Region -> accent color for the expression rows' "set" indicator strip.
GROUP_COLORS = {
    "Eyes": "#6FB7FF",
    "Brows": "#C792EA",
    "Nose": "#FF9AA2",
    "Cheeks": "#58C79D",
    "Jaw": "#FFBE78",
    "Mouth": "#DED52A",
    "Tongue": "#E34676",
    "default": "#B0BEC5",
}


def group_for_expression(name):
    """Return the group name a given expression belongs to (or 'default')."""
    for group, names in BLENDSHAPE_GROUPS.items():
        if name in names:
            return group
    return "default"


def color_for_expression(name):
    """Return the accent hex color for an expression's group."""
    return GROUP_COLORS.get(group_for_expression(name), GROUP_COLORS["default"])


def mirror_expression_name(name):
    """Return the opposite-side ARKit expression name, or None if it's a center
    shape.

    ARKit uses a trailing ``Left`` / ``Right`` on paired shapes (eyeBlinkLeft,
    mouthSmileRight, and also mouthLeft/mouthRight, jawLeft/jawRight). Center
    shapes (jawOpen, cheekPuff, mouthClose, browInnerUp, …) have no opposite.
    """
    if "Left" in name:
        return name.replace("Left", "Right")
    if "Right" in name:
        return name.replace("Right", "Left")
    return None
