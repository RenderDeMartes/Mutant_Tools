"""
Maya meshes to TopoTransfer and back, for any Mutant tool (the TopoTransfer window, Skeletor,
Zombinator...):

    import tt_maya
    link = tt_maya.send("baseMesh", "referenceMesh", on_result=print)   # exports, opens the app
    ...                                                                    # wrap, then Export there
    # on_result(new_mesh): a copy of the base with the wrapped shape, same topology and UVs
    link.stop()

Both meshes go out as OBJ in world space, so the export comes back in world space too (in
the Base's or the Reference's coordinates, both Maya world) and lands on a duplicate of the
base by vertex index: TopoTransfer never reorders vertices.
"""

from __future__ import annotations

import os
import re
import sys
import tempfile
import time
from typing import Callable, List, Optional, Tuple

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tt_app  # noqa: E402
import tt_bridge  # noqa: E402

Vec3 = Tuple[float, float, float]
HEADER = "Exported by TopoTransfer"


# ----------------------------------------------------------------------------- files (no Maya)


def work_dir() -> str:
    """A fresh folder per send, under the temp folder."""
    path = os.path.join(tempfile.gettempdir(), "MutantTopoTransfer", time.strftime("%Y%m%d_%H%M%S"))
    os.makedirs(path, exist_ok=True)
    return path


def safe_name(node: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]+", "_", node.split("|")[-1].split(":")[-1]) or "mesh"


def obj_vertices(path: str) -> List[Vec3]:
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        return [tuple(float(x) for x in line.split()[1:4]) for line in f if line.startswith("v ")]


def is_topotransfer_obj(path: str) -> bool:
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        for line in f:
            if not line.startswith("#"):
                return False
            if HEADER in line:
                return True
    return False


def result_problem(path: str, expected_vertices: int) -> Optional[str]:
    """Why the uploaded file cannot go back onto the base, or None."""
    if not is_topotransfer_obj(path):
        return "not an OBJ exported by TopoTransfer (export OBJ, not PLY)"
    n = len(obj_vertices(path))
    if n != expected_vertices:
        return f"{n} vertices, the base has {expected_vertices}: export the wrapped Base"
    return None


# ----------------------------------------------------------------------------- Maya


def _cmds():
    import maya.cmds as cmds  # type: ignore

    return cmds


def selected_meshes() -> List[str]:
    """Selected transforms with a mesh shape, in selection order (a face selection counts as its object)."""
    cmds = _cmds()
    out: List[str] = []
    for n in cmds.ls(selection=True, objectsOnly=True, long=False) or []:
        node = n
        if cmds.nodeType(n) == "mesh":
            node = (cmds.listRelatives(n, parent=True) or [n])[0]
        if cmds.listRelatives(node, shapes=True, type="mesh", noIntermediate=True) and node not in out:
            out.append(node)
    return out


def vertex_count(mesh: str) -> int:
    return _cmds().polyEvaluate(mesh, vertex=True)


def export_mesh_obj(mesh: str, path: str) -> str:
    """One mesh as OBJ in world space (Maya's objExport), vertices in Maya's order."""
    cmds = _cmds()
    if not cmds.objExists(mesh):
        raise RuntimeError(f"{mesh} does not exist")
    cmds.loadPlugin("objExport", quiet=True)
    sel = cmds.ls(selection=True)
    try:
        cmds.select(mesh, replace=True)
        cmds.file(path, force=True, options="groups=0;ptgroups=0;materials=0;smoothing=0;normals=0",
                  type="OBJexport", exportSelected=True, preserveReferences=False)
    finally:
        cmds.select(sel, replace=True) if sel else cmds.select(clear=True)
    return path


def apply_result(base: str, obj_path: str, name: str = "") -> str:
    """A duplicate of `base` (`<base>_topoTransfer`) with the wrapped shape from `obj_path`, in world space."""
    import maya.api.OpenMaya as om  # type: ignore

    cmds = _cmds()
    points = obj_vertices(obj_path)
    if len(points) != vertex_count(base):
        raise RuntimeError(f"the result has {len(points)} vertices, {base} has {vertex_count(base)}")
    target = cmds.duplicate(base, name=name or safe_name(base) + "_topoTransfer")[0]
    shape = cmds.listRelatives(target, shapes=True, type="mesh", noIntermediate=True, fullPath=True)[0]
    sel = om.MSelectionList()
    sel.add(shape)
    mesh = om.MFnMesh(sel.getDagPath(0))
    mesh.setPoints(om.MPointArray([om.MPoint(*p) for p in points]), om.MSpace.kWorld)
    return target


class Link:
    """One send: the exported files, the bridge serving them, and the way back."""

    def __init__(self, base: str, reference: str, bridge: tt_bridge.Bridge, folder: str):
        self.base, self.reference, self.bridge, self.folder = base, reference, bridge, folder

    @property
    def url(self) -> str:
        return self.bridge.app_launch_url()

    def stop(self) -> None:
        self.bridge.stop()


def _main_thread(fn, *args):
    try:
        import maya.utils  # type: ignore

        maya.utils.executeDeferred(fn, *args)
    except ImportError:
        fn(*args)


def send(base: str, reference: str = "", on_result: Optional[Callable[[str], None]] = None,
         on_error: Optional[Callable[[str], None]] = None, open_browser: bool = True) -> Link:
    """
    Export `base` (and `reference`, optional: without it, pick the Reference in the browser), open
    TopoTransfer with them loaded, and when its Export comes back, put the shape on a copy of the base
    and call on_result(copy) on Maya's main thread.
    """
    import webbrowser

    folder = work_dir()
    files = {"base": export_mesh_obj(base, os.path.join(folder, safe_name(base) + ".obj"))}
    if reference:
        files["reference"] = export_mesh_obj(reference, os.path.join(folder, safe_name(reference) + ".obj"))
    expected = vertex_count(base)
    bundled = tt_app.bundled_app(tt_app.ROOT)
    if not bundled:
        ok, message = tt_app.ensure_app_running(tt_app.DEFAULT_URL, tt_app.ROOT)
        if not ok:
            raise RuntimeError(message)
    app_dir, static = bundled if bundled else (None, ())

    def arrived(path):
        def take():
            try:
                copy = apply_result(base, path)
            except Exception as error:  # report, never leave a half-applied state silently
                if on_error:
                    on_error(str(error))
                return
            if on_result:
                on_result(copy)

        _main_thread(take)

    bridge = tt_bridge.Bridge(
        folder, tt_app.DEFAULT_URL, files, result_path=os.path.join(folder, safe_name(base) + "_wrapped.obj"),
        on_result=arrived, validate=lambda tmp: result_problem(tmp, expected), app_dir=app_dir, static_dirs=static,
    ).start()
    link = Link(base, reference, bridge, folder)
    if open_browser:
        webbrowser.open(link.url)
    return link
