"""
Maya-independent state of Meta Mutant, the custom MetaHuman head workflow (mm_controller.py):
file layout of the work folder, saved settings, finding the OBJ that
TopoTransfer exported (browser download) and which steps are done.

Work folder layout:

    <work>/mh_head_lod0.obj             MetaHuman LOD0 meshes from the DNA   -> TopoTransfer Base
    <work>/mh_head_lod0.manifest.json   vertex ranges of the DNA meshes
    <work>/custom_head.obj              custom head exported from Maya       -> TopoTransfer Reference
    <work>/mh_head_lod0_wrapped.obj     TopoTransfer result (saved here or left in Downloads)
    <work>/head_custom.dna              calibrated DNA
    <work>/meta_mutant.json            settings of the Meta Mutant window
"""

from __future__ import annotations

import json
import os
import sys
from dataclasses import asdict, dataclass, field, fields
from typing import Dict, Iterable, List, Optional, Sequence

HERE = os.path.dirname(os.path.abspath(__file__))
TOPOTRANSFER = os.path.join(os.path.dirname(HERE), "TopoTransfer")  # the app, and its Maya link in maya/
sys.path.insert(0, HERE)
sys.path.insert(1, os.path.join(TOPOTRANSFER, "maya"))
import mm_core as core  # noqa: E402
from tt_app import DEFAULT_URL  # noqa: E402,F401

BASE_STEM = "mh_head_lod0"
SETTINGS_FILE = "meta_mutant.json"


@dataclass
class Settings:
    dna_path: str = ""
    work_dir: str = ""
    custom_mesh: str = ""
    #: the artist's eyes and teeth (with the tongue): whole meshes and / or faces of the head mesh
    eyes: List[str] = field(default_factory=list)
    teeth: List[str] = field(default_factory=list)
    topotransfer_url: str = DEFAULT_URL
    #: open TopoTransfer with the files loaded and receive the export back (tt_bridge), no drag and drop
    direct_link: bool = True
    #: folder containing Epic's `dna` Python module; empty = the one Meta Mutant ships for Maya 2026
    dna_module_dir: str = ""
    backend: str = "auto"
    joints: str = "FACIAL_"
    lower_lods: bool = True
    blendshapes: bool = True
    face_board: bool = True  # MetaHuman-style controls driving the rig (mm_faceboard, plain Maya nodes)
    #: optional face regions on your head (mm_regions.REGIONS keys -> faces / vertices): the skin and
    #: blendshapes of each come only from the same region of the MetaHuman (no bleeding between lips)
    regions: Dict[str, List[str]] = field(default_factory=dict)
    wrapped_obj: str = ""


@dataclass
class Paths:
    base_obj: str
    manifest: str
    reference_obj: str
    wrapped_obj: str
    custom_dna: str
    settings: str


def paths(work_dir: str) -> Paths:
    j = lambda name: os.path.join(work_dir, name)  # noqa: E731
    return Paths(
        base_obj=j(BASE_STEM + ".obj"),
        manifest=j(BASE_STEM + ".manifest.json"),
        reference_obj=j("custom_head.obj"),
        wrapped_obj=j(BASE_STEM + "_wrapped.obj"),
        custom_dna=j("head_custom.dna"),
        settings=j(SETTINGS_FILE),
    )


def load_settings(path: str) -> Settings:
    """Settings from JSON; unknown keys are ignored, missing ones take defaults."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (OSError, ValueError):
        return Settings()
    known = {f.name for f in fields(Settings)}
    return Settings(**{k: v for k, v in data.items() if k in known})


def save_settings(s: Settings, path: str) -> None:
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(asdict(s), f, indent=2)


def joint_filter(prefixes: str):
    """'' = every joint, else comma-separated name prefixes (same rule as `mm_dna.py calibrate --joints`)."""
    items = [p.strip() for p in prefixes.split(",") if p.strip()]
    if not items:
        return lambda n: True
    return lambda n: any(n.startswith(p) for p in items)


def manifest_vertex_count(manifest: str) -> int:
    return sum(b.vertex_count for b in core.read_manifest(manifest))


def head_mesh_name(manifest: str) -> str:
    """Name of the DNA head mesh (the one the rig is transferred from), from the manifest."""
    blocks = core.read_manifest(manifest)
    heads = [b for b in blocks if b.name.lower().startswith("head")]
    if not heads:
        raise ValueError(f"no head mesh in {manifest}: {[b.name for b in blocks]}")
    return heads[0].name


def is_topotransfer_obj(path: str) -> bool:
    """True when the OBJ header says it was exported by TopoTransfer."""
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            for line in f:
                if not line.startswith("#"):
                    return False
                if "Exported by TopoTransfer" in line:
                    return True
    except OSError:
        return False
    return False


def obj_vertex_count(path: str) -> int:
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        return sum(1 for line in f if line.startswith("v "))


def wrapped_obj_problem(path: str, expected_vertices: Optional[int] = None) -> Optional[str]:
    """Why `path` is not a usable TopoTransfer result for the exported Base, or None when it is."""
    if not is_topotransfer_obj(path):
        return "not an OBJ exported by TopoTransfer (export OBJ, not PLY)"
    if expected_vertices is not None:
        n = obj_vertex_count(path)
        if n != expected_vertices:
            return f"{n} vertices, the exported Base has {expected_vertices}: wrap with mh_head_lod0.obj as Base"
    return None


def default_search_dirs(work_dir: str) -> List[str]:
    """Where a TopoTransfer export may land: the work folder, then the browser's Downloads folder."""
    out = [work_dir]
    downloads = os.path.join(os.path.expanduser("~"), "Downloads")
    if os.path.isdir(downloads):
        out.append(downloads)
    return out


def find_wrapped_obj(
    search_dirs: Sequence[str],
    expected_vertices: Optional[int] = None,
    newer_than: Optional[float] = None,
    stem: str = BASE_STEM,
) -> Optional[str]:
    """
    Newest `<stem>_wrapped*.obj` (browsers add ' (1)' etc. to repeated downloads) in the
    given folders that TopoTransfer exported, optionally with the expected vertex count
    and modified after `newer_than` (e.g. the time the base OBJ was exported).
    """
    candidates = []
    for d in search_dirs:
        if not d or not os.path.isdir(d):
            continue
        for name in os.listdir(d):
            low = name.lower()
            if not (low.startswith(stem.lower() + "_wrapped") and low.endswith(".obj")):
                continue
            p = os.path.join(d, name)
            mtime = os.path.getmtime(p)
            if newer_than is not None and mtime < newer_than:
                continue
            if not is_topotransfer_obj(p):
                continue
            if expected_vertices is not None and obj_vertex_count(p) != expected_vertices:
                continue
            candidates.append((mtime, p))
    return max(candidates)[1] if candidates else None


def preview_matrix(wrapped_obj: str) -> List[float]:
    """
    Matrix (column-major = Maya row-major list) that places the imported wrapped OBJ on
    the custom head in the Maya scene: identity when it was exported in reference
    coordinates, base->reference when exported in original (DNA) coordinates.
    """
    w = core.read_obj_positions(wrapped_obj)
    return list(core.IDENTITY4) if w.space != "original" else list(w.alignment)


def scene_warnings(linear_unit: str, up_axis: str) -> List[str]:
    out = []
    if linear_unit != "cm":
        out.append(f"scene unit is '{linear_unit}': MetaHuman DNAs are in centimetres, set Preferences > Settings > Linear to cm")
    if up_axis.lower() != "y":
        out.append(f"up axis is '{up_axis}': MetaHuman DNAs are Y up")
    return out


def status(s: Settings) -> Dict[str, bool]:
    """Which steps have their output on disk."""
    if not s.work_dir:
        return {"setup": False, "export": False, "wrapped": False, "calibrated": False}
    p = paths(s.work_dir)
    return {
        "setup": bool(s.dna_path) and os.path.isfile(s.dna_path),
        "export": all(os.path.isfile(f) for f in (p.base_obj, p.manifest, p.reference_obj)),
        "wrapped": bool(s.wrapped_obj) and os.path.isfile(s.wrapped_obj),
        "calibrated": os.path.isfile(p.custom_dna),
    }


def extend_sys_path(dirs: Iterable[str]) -> List[str]:
    """Append existing folders to sys.path (once). Returns the ones added."""
    added = []
    for d in dirs:
        if d and os.path.isdir(d) and d not in sys.path:
            sys.path.append(d)
            added.append(d)
    return added


def bundled_dna_module(maya_version: str) -> str:
    """The dna module that comes with Meta Mutant for this Maya (built from OpenRigLogic), or ""."""
    system = "windows" if sys.platform.startswith("win") else "linux"
    folder = os.path.join(HERE, "dna_module", f"Maya{maya_version}", system)
    return folder if maya_version and os.path.isfile(os.path.join(folder, "dna.py")) else ""
