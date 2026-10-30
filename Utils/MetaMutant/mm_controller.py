"""
Meta Mutant, the custom MetaHuman head workflow, without any UI: the steps,
their order and the link to the TopoTransfer app. The Meta Mutant window
(Mutant_Tools/UI/MetaMutant/load_meta_mutant.py) drives it; anything else can too:

    import mm_controller
    w = mm_controller.Workflow(settings, log=print)
    w.prepare()     # 1: export Base + Reference, open TopoTransfer with both loaded
                    # 2: wrap in the browser; Export sends the OBJ back (on_change fires)
    w.apply_all()   # 3: fit eyes / teeth, calibrate the DNA, build the rig, transfer to <head>_MH

Maya 2026 only: Epic's `dna` module comes with Meta Mutant (dna_module/Maya2026, built from
OpenRigLogic) and the rig is built by mm_rig. Steps raise on failure with a message meant for
the artist; the UI shows it.
"""

from __future__ import annotations

import os
import shutil
import sys
import webbrowser
from typing import Callable, Dict, List, Optional

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mm_workflow as wf  # noqa: E402
import tt_app  # noqa: E402
import tt_bridge  # noqa: E402

PREVIEW_NAME = "tt_wrapped_preview"
MAYA_VERSION = "2026"
RESULT_SUFFIX = "_MH"


def _main_thread(fn, *args):
    """Run `fn` on Maya's main thread (bridge callbacks arrive on a server thread)."""
    try:
        import maya.utils  # type: ignore

        maya.utils.executeDeferred(fn, *args)
    except ImportError:  # outside Maya
        fn(*args)


def maya_version() -> str:
    try:
        import maya.cmds as cmds  # type: ignore

        return cmds.about(version=True).split()[0]
    except ImportError:
        return ""


class Workflow:
    """Settings + steps. `log(text)` reports progress; `on_change()` fires when state changed outside a step (result received)."""

    def __init__(self, settings: Optional[wf.Settings] = None, log: Callable[[str], None] = print,
                 on_change: Optional[Callable[[], None]] = None, call_on_main: Callable = _main_thread):
        self.s = settings or wf.Settings()
        self.log = log
        self.on_change = on_change
        self.call_on_main = call_on_main
        self.bridge: Optional[tt_bridge.Bridge] = None
        self.applied = False

    # ------------------------------------------------------------------ helpers

    def work(self) -> str:
        if not self.s.work_dir:
            raise RuntimeError("set a Work folder first")
        os.makedirs(self.s.work_dir, exist_ok=True)
        return self.s.work_dir

    def paths(self) -> wf.Paths:
        return wf.paths(self.work())

    @staticmethod
    def need(path, what):
        if not path or not os.path.isfile(path):
            raise RuntimeError(f"{what} not found: {path or '(not set)'}")

    def save(self):
        if self.s.work_dir:
            wf.save_settings(self.s, wf.paths(self.s.work_dir).settings)

    def dna_module_dir(self) -> str:
        """The configured dna module folder, else the one Meta Mutant ships for this Maya."""
        return self.s.dna_module_dir or wf.bundled_dna_module(maya_version())

    def modules(self):
        """Put Epic's dna module on sys.path and import the pipeline modules."""
        dna_dir = self.dna_module_dir()
        if not dna_dir:
            raise RuntimeError(f"Meta Mutant needs Maya {MAYA_VERSION} (this is Maya {maya_version() or '?'})")
        for d in wf.extend_sys_path([dna_dir]):
            self.log(f"added to sys.path: {d}")
        import mm_dna
        import mm_maya

        return mm_dna, mm_maya

    def status(self) -> dict:
        """Which of the three steps are done (from the files on disk)."""
        st = wf.status(self.s)
        return {"prepare": st["export"], "wrap": st["wrapped"], "apply": self.applied}

    # ------------------------------------------------------------------ the three steps

    def prepare(self):
        """1: export Base + Reference OBJs, then open TopoTransfer with both loaded."""
        self.export()
        self.open_app()

    def apply_all(self):
        """3: find the export, calibrate, build the rig, transfer. Stops at the first failure."""
        self.import_wrapped()
        self.calibrate()
        self.remove_result()
        self.build_rig()
        self.transfer()
        if self.s.face_board:
            self.build_face_board()
        self.log("done: your head is rigged with the calibrated MetaHuman rig")

    # ------------------------------------------------------------------ eyes and teeth

    def parts_on_head(self) -> List[int]:
        """Vertex ids of the head mesh picked as eyes or teeth (faces of the head itself)."""
        _, mm_maya = self.modules()
        ids: List[int] = []
        for spec in (self.s.eyes, self.s.teeth):
            if spec:
                ids += mm_maya.spec_vertices(spec).get(self.s.custom_mesh, [])
        return sorted(set(ids))

    def part_points_dna(self, spec: List[str]) -> List[List[tuple]]:
        """The picked points in DNA space (through the alignment TopoTransfer exported), one list per mesh."""
        import mm_core as core

        _, mm_maya = self.modules()
        inv = core.mat4_inverse(core.read_obj_positions(self.s.wrapped_obj).alignment)
        return [[core.mat4_apply(inv, p) for p in group] for group in mm_maya.spec_points(spec)]

    # ------------------------------------------------------------------ sub-steps

    def export(self):
        mm_dna, mm_maya = self.modules()
        self.need(self.s.dna_path, "Head DNA")
        if not self.s.custom_mesh:
            raise RuntimeError("set your head mesh (select it, then Use selected)")
        for w in wf.scene_warnings(*mm_maya.scene_space()):
            self.log("warning: " + w)
        p = self.paths()
        manifest = mm_dna.export_obj(self.s.dna_path, p.base_obj)
        self.log(f"Base: {p.base_obj} ({wf.manifest_vertex_count(manifest)} vertices)")
        left_out = self.parts_on_head()
        mm_maya.export_head_without(self.s.custom_mesh, left_out, p.reference_obj)
        self.log(f"Reference: {p.reference_obj} ({self.s.custom_mesh}, world space"
                 + (f", without the {len(left_out)} eye / teeth vertices" if left_out else "") + ")")

    def open_app(self):
        """Open TopoTransfer with the exported files loaded; its Export comes back here."""
        self.stop_link()
        bundled = tt_app.bundled_app(tt_app.ROOT)
        if not bundled:  # development checkout without app/: needs the dev server
            ok, message = tt_app.ensure_app_running(self.s.topotransfer_url, tt_app.ROOT)
            self.log(message)
            if not ok:
                raise RuntimeError(message)
        p = self.paths()
        for path in (p.base_obj, p.manifest, p.reference_obj):
            self.need(path, "Base / Reference export (run step 1)")
        expected = wf.manifest_vertex_count(p.manifest)
        app_dir, static = bundled if bundled else (None, ())
        self.bridge = tt_bridge.Bridge(
            self.s.work_dir, self.s.topotransfer_url, {"base": p.base_obj, "reference": p.reference_obj},
            result_path=p.wrapped_obj, on_result=self._result_arrived,
            validate=lambda tmp: wf.wrapped_obj_problem(tmp, expected),
            app_dir=app_dir, static_dirs=static,
        ).start()
        webbrowser.open(self.bridge.app_launch_url())
        self.log("opened TopoTransfer with Base + Reference loaded - wrap there; Export sends the OBJ back here")

    def stop_link(self):
        if self.bridge:
            self.bridge.stop()
            self.bridge = None

    def _result_arrived(self, path):
        self.call_on_main(self._take_result, path)

    def _take_result(self, path):
        self.s.wrapped_obj = path
        self.save()
        self.log(f"received {os.path.basename(path)} from TopoTransfer - next: Apply to my head")
        if self.on_change:
            self.on_change()

    def find_wrapped(self):
        p = self.paths()
        self.need(p.manifest, "manifest (run step 1)")
        self.need(p.base_obj, "Base OBJ (run step 1)")
        found = wf.find_wrapped_obj(wf.default_search_dirs(self.s.work_dir), wf.manifest_vertex_count(p.manifest), os.path.getmtime(p.base_obj))
        if not found:
            raise RuntimeError("no TopoTransfer export yet (mh_head_lod0_wrapped*.obj, newer than step 1, matching vertex count) "
                               "in the work folder or Downloads: finish step 2, or pick the file")
        self.s.wrapped_obj = found
        self.log(f"found {found}")

    def import_wrapped(self):
        _, mm_maya = self.modules()
        p = self.paths()
        if not self.s.wrapped_obj or not os.path.isfile(self.s.wrapped_obj):
            self.find_wrapped()
        self.need(p.manifest, "manifest (run step 1)")
        n, want = wf.obj_vertex_count(self.s.wrapped_obj), wf.manifest_vertex_count(p.manifest)
        if n != want:
            raise RuntimeError(f"{self.s.wrapped_obj} has {n} vertices, the exported Base has {want}: export the result of the wrap with mh_head_lod0.obj as Base")
        if not wf.is_topotransfer_obj(self.s.wrapped_obj):
            self.log("warning: no TopoTransfer header in this OBJ; DNA space cannot be recovered without its alignment line")
        if os.path.normcase(os.path.abspath(self.s.wrapped_obj)) != os.path.normcase(os.path.abspath(p.wrapped_obj)):
            shutil.copy2(self.s.wrapped_obj, p.wrapped_obj)
            self.log(f"copied to {p.wrapped_obj}")
            self.s.wrapped_obj = p.wrapped_obj
        node = mm_maya.import_obj(self.s.wrapped_obj, PREVIEW_NAME, wf.preview_matrix(self.s.wrapped_obj))
        self.log(f"imported {node} ({n} vertices) on top of your head")

    def calibrate(self):
        mm_dna, _ = self.modules()
        p = self.paths()
        self.need(self.s.dna_path, "Head DNA")
        self.need(p.manifest, "manifest (run step 1)")
        self.need(self.s.wrapped_obj, "wrapped OBJ")
        # all picked eye points together: split into two eyes by position (one mesh may hold both eyes,
        # and eye + cornea meshes may be picked together)
        eyes = [[q for group in self.part_points_dna(self.s.eyes) for q in group]] if self.s.eyes else []
        teeth = [q for group in self.part_points_dna(self.s.teeth) for q in group] if self.s.teeth else []
        report = mm_dna.calibrate(self.s.dna_path, p.manifest, self.s.wrapped_obj, p.custom_dna,
                                  joint_filter=wf.joint_filter(self.s.joints), update_lower_lods=self.s.lower_lods,
                                  backend=self.s.backend, eyes=eyes, teeth=teeth)
        for line in report:
            self.log(line)

    def result_names(self) -> List[str]:
        """The copies Apply makes: <head>_MH, and <part>_MH for eyes / teeth picked as separate meshes."""
        import maya.cmds as cmds  # type: ignore

        names = [self.s.custom_mesh + RESULT_SUFFIX]
        _, mm_maya = self.modules()
        for spec in (self.s.eyes, self.s.teeth):
            for mesh in (mm_maya.spec_vertices(spec) if spec else {}):
                if mesh != self.s.custom_mesh:
                    names.append(mesh + RESULT_SUFFIX)
        return [n for n in names if cmds.objExists(n)]

    def remove_result(self):
        """Apply again replaces the earlier result (its joints are rebuilt)."""
        import maya.cmds as cmds  # type: ignore

        old = self.result_names()
        if old:
            cmds.delete(old)
            self.log(f"removed the earlier result: {', '.join(old)}")

    def build_rig(self):
        _, mm_maya = self.modules()
        p = self.paths()
        self.need(p.custom_dna, "head_custom.dna (calibrate first)")
        mm_maya.build_rig(p.custom_dna, blendshapes=self.s.blendshapes)
        err = mm_maya.check_joint_convention(p.custom_dna)
        self.log(f"rig built from {os.path.basename(p.custom_dna)} (joints match the DNA, max error {err:.6f})")

    def build_face_board(self):
        """The face board beside your head: its controls move the joints and blendshapes as RigLogic would."""
        import mm_faceboard

        import maya.cmds as cmds  # type: ignore
        import mm_epic

        # Epic's own MetaHuman board when it came with the Epic download (Epic Files menu), else Meta Mutant's
        epic = mm_epic.found(mm_epic.default_dir(cmds.internalVar(userAppDir=True)))
        board = epic.face_board if epic and epic.face_board else ""
        mm_faceboard.build(self.paths().custom_dna, head=self.s.custom_mesh + RESULT_SUFFIX, log=self.log, epic_board=board)

    def transfer(self):
        import maya.cmds as cmds  # type: ignore

        _, mm_maya = self.modules()
        p = self.paths()
        self.need(self.s.wrapped_obj, "wrapped OBJ")
        source = wf.head_mesh_name(p.manifest)
        if not cmds.objExists(source):
            raise RuntimeError(f"{source} is not in the scene: build the rig first")
        if not cmds.objExists(self.s.custom_mesh):
            raise RuntimeError(f"your head mesh {self.s.custom_mesh!r} is not in the scene")
        mh = {key: [m for m in cmds.ls("*_lod0_mesh", type="transform") if key in m] for key in ("eyeLeft", "eyeRight", "teeth")}
        eye_sources = mh["eyeLeft"] + mh["eyeRight"]
        teeth_source = mh["teeth"][0] if mh["teeth"] else ""
        eye_parts = mm_maya.spec_vertices(self.s.eyes) if self.s.eyes else {}
        teeth_parts = mm_maya.spec_vertices(self.s.teeth) if self.s.teeth else {}

        # copies in DNA space: <head>_MH, and <part>_MH for eyes / teeth that are meshes of their own
        copies: Dict[str, str] = {}
        for mesh in [self.s.custom_mesh] + [m for m in list(eye_parts) + list(teeth_parts) if m != self.s.custom_mesh]:
            if mesh in copies:
                continue
            copies[mesh] = cmds.duplicate(mesh, name=mesh + RESULT_SUFFIX)[0]
            mm_maya.align_custom_mesh(copies[mesh], self.s.wrapped_obj)
            self.log(f"{copies[mesh]}: moved into DNA space")
        target = copies[self.s.custom_mesh]
        if cmds.objExists(PREVIEW_NAME):
            cmds.hide(PREVIEW_NAME)
        # lips / eyelids / mouth bag / eye sockets picked on your head: region-to-region transfer
        regions = {k: mm_maya.spec_vertices(spec).get(self.s.custom_mesh, []) for k, spec in (self.s.regions or {}).items() if spec}
        corr = mm_maya.region_correspondence(source, target, regions, log=self.log) if any(regions.values()) else None
        out = {"skinCluster": mm_maya.transfer_skin(source, target, corr=corr)}
        for mesh, copy in copies.items():  # part meshes: bound to the same joints first
            if mesh != self.s.custom_mesh:
                mm_maya.transfer_skin(teeth_source if mesh in teeth_parts and teeth_source else
                                      (eye_sources[0] if eye_sources else source), copy)
        # eyes: every picked eye vertex, split into two eyes by position, weighted like the nearer MetaHuman eye
        if eye_parts and eye_sources:
            entries = [(mesh, i, p) for mesh, ids in eye_parts.items()
                       for pts in [mm_maya.mesh_points(copies[mesh])] for i, p in ((i, pts[i]) for i in ids)]
            for group in self._split_eyes(entries):
                src = mm_maya.nearest_mesh([p for _, _, p in group], eye_sources)
                for mesh in {m for m, _, _ in group}:
                    ids = [i for m, i, _ in group if m == mesh]
                    mm_maya.copy_part_skin(src, copies[mesh], ids)
                    self.log(f"{copies[mesh]}: {len(ids)} eye vertices weighted like {src}")
        # teeth and tongue: weighted like the MetaHuman teeth
        if teeth_parts and teeth_source:
            for mesh, ids in teeth_parts.items():
                mm_maya.copy_part_skin(teeth_source, copies[mesh], ids)
                self.log(f"{copies[mesh]}: {len(ids)} teeth vertices weighted like {teeth_source}")
        if self.s.blendshapes:
            still = sorted(set(eye_parts.get(self.s.custom_mesh, []) + teeth_parts.get(self.s.custom_mesh, [])
                               + regions.get("eye_socket", [])))
            out["blendShape"] = mm_maya.transfer_blendshapes(source, target, keep_still=still, log=self.log, corr=corr)
            for mesh in teeth_parts:  # separate teeth / tongue meshes: the tongue shapes too
                if mesh != self.s.custom_mesh and teeth_source:
                    mm_maya.transfer_blendshapes(teeth_source, copies[mesh], log=self.log)
        # everything was built and transferred in DNA space: back onto your head, where it was
        mm_maya.place_in_scene(self.s.wrapped_obj, list(copies.values()))
        # the MetaHuman's own meshes only drive the rig now: hidden, your copies show
        cmds.hide([m for m in cmds.listRelatives("metaMutant_geometry", children=True, type="transform") or []
                   if m.endswith("_lod0_mesh")])
        self.log("rig placed on your head (its original position)")
        self.applied = True
        self.log(f"rig transferred from {source} to {', '.join(copies.values())}")

    @staticmethod
    def _split_eyes(entries):
        """(mesh, vertex id, point) of every picked eye vertex, split into the two eyes by position."""
        import mm_core as core

        a, b = core.split_two([p for _, _, p in entries])
        ca, cb = core.centroid(a), core.centroid(b)
        near_a = [e for e in entries if core._dist(e[2], ca) <= core._dist(e[2], cb)]
        near_b = [e for e in entries if core._dist(e[2], ca) > core._dist(e[2], cb)]
        return [g for g in (near_a, near_b) if g]


# ----------------------------------------------------------------------------- Maya helpers


def selected_meshes():
    """Selected transforms with a mesh shape (a face selection counts as its object)."""
    import maya.cmds as cmds  # type: ignore

    out = []
    for n in cmds.ls(selection=True, objectsOnly=True, long=False) or []:
        node = n
        if cmds.nodeType(n) == "mesh":
            node = (cmds.listRelatives(n, parent=True) or [n])[0]
        if cmds.listRelatives(node, shapes=True, type="mesh") and node not in out:
            out.append(node)
    return out
