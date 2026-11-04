"""
Meta Mutant, the custom MetaHuman head workflow, without any UI: the steps,
their order and the link to the TopoTransfer app. The Meta Mutant window
(Mutant_Tools/UI/MetaMutant/load_meta_mutant.py) drives it; anything else can too:

    import mm_controller
    w = mm_controller.Workflow(settings, log=print)
                    # 1: optional, the Pick Points window saves points.json (load_point_picker)
    w.prepare()     # 2: export Base + Reference, open TopoTransfer with both loaded (and the points)
                    # 3: wrap in the browser; Export sends the OBJ back (on_change fires)
    w.apply_all()   # 4: fit eyes / teeth, calibrate the DNA, build the rig, transfer to <head>_MH

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
        """Which of the steps are done (from the files on disk)."""
        st = wf.status(self.s)
        return {"points": st["points"], "prepare": st["export"], "wrap": st["wrapped"], "apply": self.applied}

    # ------------------------------------------------------------------ the steps

    def prepare(self):
        """2: export Base + Reference OBJs and the picked points, then open TopoTransfer with them loaded."""
        self.export()
        self.open_app()

    def apply_all(self):
        """4: find the export, calibrate, build the rig, transfer. Stops at the first failure."""
        self.import_wrapped()
        self.calibrate()
        self.remove_result()
        self.build_rig()
        self.transfer()
        if self.s.face_board:
            self.build_face_board()
            self.apply_fixes()
        self.log("done: your head is rigged with the calibrated MetaHuman rig")

    # ------------------------------------------------------------------ scale of your meshes

    def picked_meshes(self) -> List[str]:
        """Your head, and the eye and teeth meshes picked: what must not carry a scale."""
        meshes = [self.s.custom_mesh] if self.s.custom_mesh else []
        for item in list(self.s.eyes) + list(self.s.teeth):
            mesh = item.split(".")[0]
            if mesh not in meshes:
                meshes.append(mesh)
        return meshes

    def scale_problems(self):
        _, mm_maya = self.modules()
        return mm_maya.scale_problems(self.picked_meshes())

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

    def teeth_arches(self, positions_of=None) -> Dict[str, tuple]:
        """mesh -> (upper, lower, tongue) vertex ids of the teeth picked, each tooth or gum whole on one arch.
        `positions_of(mesh)`: where to read the meshes from (default: where they are named in the settings)."""
        import mm_core as core

        _, mm_maya = self.modules()
        parts = mm_maya.spec_vertices(self.s.teeth) if self.s.teeth else {}
        read = positions_of or mm_maya.mesh_points
        points: List[tuple] = []
        shells: List[List[int]] = []
        owners = []  # (first id of a mesh in `points`, mesh)
        for mesh, ids in parts.items():
            owners.append((len(points), mesh))
            at = len(points)
            whole = read(mesh)
            own = {v: at + row for row, v in enumerate(ids)}
            points += [tuple(whole[v]) for v in ids]
            shells += [[own[v] for v in shell] for shell in mm_maya.mesh_shells(mesh, ids)]
        out = {mesh: ([], [], []) for mesh in parts}
        back = [(row + first, mesh, v) for first, mesh in owners for row, v in enumerate(parts[mesh])]
        where = {at: (mesh, v) for at, mesh, v in back}
        for slot, ids in enumerate(core.teeth_parts(points, shells)):
            for at in ids:
                mesh, v = where[at]
                out[mesh][slot].append(v)
        return out

    def teeth_arches_dna(self):
        """(upper, lower) points of the teeth picked, in DNA space; None without teeth."""
        import mm_core as core

        _, mm_maya = self.modules()
        split = self.teeth_arches()
        if not split:
            return None
        inv = core.mat4_inverse(core.read_obj_positions(self.s.wrapped_obj).alignment)
        upper: List[tuple] = []
        lower: List[tuple] = []
        for mesh, (up, low, _) in split.items():
            whole = mm_maya.mesh_points(mesh)
            upper += [core.mat4_apply(inv, whole[v]) for v in up]
            lower += [core.mat4_apply(inv, whole[v]) for v in low]
        return upper, lower

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
        remap = mm_maya.export_head_without(self.s.custom_mesh, left_out, p.reference_obj)
        self.log(f"Reference: {p.reference_obj} ({self.s.custom_mesh}, world space"
                 + (f", without the {len(left_out)} eye / teeth vertices" if left_out else "") + ")")
        self.write_guides(remap)

    def write_guides(self, remap=None):
        """The points picked in Maya, as TopoTransfer loads them. Without any, no file: it guesses on its own."""
        import mm_core as core
        import mm_points as mp
        import mm_regions

        mm_dna, mm_maya = self.modules()
        import mm_rig

        p = self.paths()
        if os.path.isfile(p.guides):
            os.remove(p.guides)
        picked = {k: v for k, v in (self.s.regions or {}).items() if v and k in mm_regions.MATCHED}
        points = mp.load(p.points)
        if not (points["guides"] or points["lines"] or picked):
            return
        head = mm_maya.mesh_points(self.s.custom_mesh)
        problem = mp.stale(points, self.s.custom_mesh, len(head))
        if problem:
            raise RuntimeError(f"{problem}: pick the points again (step 1)")
        points = mp.refreshed(points, head)  # your head may have moved since they were picked
        base = core.read_obj_positions(p.base_obj).positions
        regions = {k: mm_maya.spec_vertices(v).get(self.s.custom_mesh, []) for k, v in picked.items()}
        base_regions = self.metahuman_regions() if regions else {}
        if points["lines"]:  # the lines say which lip is which; a region picked by hand wins
            import mm_zones

            reader = mm_dna.load_dna(self.s.dna_path)
            head_index = mm_dna.mesh_indices_for_lod(reader, 0, ("head",))[0]
            data = mm_rig.mesh_data(reader, head_index)
            line_base, line_head = mm_zones.lock_regions(points, head, mm_maya.mesh_edges(self.s.custom_mesh), data["positions"],
                                                         mm_zones.polygon_edges(data["counts"], data["connects"]))
            for k, ids in line_head.items():
                if k not in regions:
                    regions[k] = ids
                    base_regions[k] = line_base.get(k, [])
        xs = [q[0] for q in head]
        guides = mp.launch_guides(points, base, base_regions, mp.reference_regions(regions, remap), (min(xs) + max(xs)) / 2)
        mp.write_guides(p.guides, guides)
        self.log(f"Guides: {len(guides['landmarks'])} pairs, regions locked in TopoTransfer: {', '.join(guides['regions']) or 'none'}")

    def picked_points(self) -> Optional[dict]:
        """The points of this work folder when they were picked on this head, else None."""
        import mm_points as mp

        _, mm_maya = self.modules()
        points = mp.load(self.paths().points)
        if not points.get("lines") and not points.get("guides"):
            return None
        return None if mp.stale(points, self.s.custom_mesh, len(mm_maya.mesh_points(self.s.custom_mesh))) else points

    def metahuman_regions(self) -> Dict[str, List[int]]:
        """Lips, eyelids and mouth bag of the MetaHuman head, from the skin weights in the DNA."""
        mm_dna, _ = self.modules()
        import mm_picker

        reader = mm_dna.load_dna(self.s.dna_path)
        return mm_picker.dna_regions(reader, mm_dna.mesh_indices_for_lod(reader, 0, ("head",))[0])

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
        files = {"base": p.base_obj, "reference": p.reference_obj}
        if os.path.isfile(p.guides):
            files["guides"] = p.guides
        self.bridge = tt_bridge.Bridge(
            self.s.work_dir, self.s.topotransfer_url, files,
            result_path=p.wrapped_obj, on_result=self._result_arrived,
            validate=lambda tmp: wf.wrapped_obj_problem(tmp, expected),
            app_dir=app_dir, static_dirs=static,
        ).start()
        webbrowser.open(self.bridge.app_launch_url())
        self.log("opened TopoTransfer with Base + Reference loaded - fit there; Export sends the OBJ back here")

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
            raise RuntimeError(f"{self.s.wrapped_obj} has {n} vertices, the exported Base has {want}: export the fit from TopoTransfer with mh_head_lod0.obj as Base")
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
        self.need(self.s.wrapped_obj, "fitted OBJ")
        # all picked eye points together: split into two eyes by position (one mesh may hold both eyes,
        # and eye + cornea meshes may be picked together)
        eyes = [[q for group in self.part_points_dna(self.s.eyes) for q in group]] if self.s.eyes else []
        teeth = [q for group in self.part_points_dna(self.s.teeth) for q in group] if self.s.teeth else []
        report = mm_dna.calibrate(self.s.dna_path, p.manifest, self.s.wrapped_obj, p.custom_dna,
                                  joint_filter=wf.joint_filter(self.s.joints), update_lower_lods=self.s.lower_lods,
                                  backend=self.s.backend, eyes=eyes, teeth=teeth, arches=self.teeth_arches_dna())
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
        import mm_core as core
        import mm_faceboard

        import maya.cmds as cmds  # type: ignore
        import mm_epic

        # Epic's own MetaHuman board when it came with the Epic download (Epic Files menu), else Meta Mutant's
        epic = mm_epic.found(mm_epic.default_dir(cmds.internalVar(userAppDir=True)))
        board = epic.face_board if epic and epic.face_board else ""
        mm_dna, _ = self.modules()
        travel = core.lid_travel(core.eye_radius(mm_dna.load_dna(self.s.dna_path)), core.eye_radius(mm_dna.load_dna(self.paths().custom_dna)))
        self.log(f"lids turn {travel:.2f} of the MetaHuman's angle, so they travel as far on your eyes")
        mm_faceboard.build(self.paths().custom_dna, head=self.s.custom_mesh + RESULT_SUFFIX, log=self.log, epic_board=board, lid_travel=travel)

    def apply_fixes(self):
        """What the proportions of your head still ask for once the rig moves: lids that meet, teeth inside the skin."""
        import mm_core as core
        import mm_fixes
        import mm_rig

        _, mm_maya = self.modules()
        points = self.picked_points()
        if not points or not points.get("lines"):
            return
        head = self.s.custom_mesh + RESULT_SUFFIX
        source = wf.head_mesh_name(self.paths().manifest)
        if self.s.close_eyelids:
            parts = mm_maya.spec_vertices(self.s.eyes) if self.s.eyes else {}
            meshes = [mesh + RESULT_SUFFIX for mesh in parts if mesh != self.s.custom_mesh]
            eyes = []
            if self.s.custom_mesh in parts:  # eyes on the head's own mesh: their spheres
                every = mm_maya.mesh_points(self.s.custom_mesh)
                a, b = core.split_two([every[i] for i in parts[self.s.custom_mesh]])
                eyes = [core.sphere_fit(g) for g in (a, b) if len(g) >= 4]
            mm_fixes.close_eyelids(head, source, points, mm_rig.ROOT, eyes, meshes, log=self.log)
        if self.s.fit_teeth and self.s.teeth:
            arches = {mesh + RESULT_SUFFIX: (up, low) for mesh, (up, low, _) in self.teeth_arches().items() if mesh != self.s.custom_mesh}
            mm_fixes.place_teeth(head, arches, points, mm_rig.ROOT, log=self.log)
            mm_fixes.fit_teeth(head, list(arches), points, log=self.log)

    def transfer(self):
        import maya.cmds as cmds  # type: ignore

        _, mm_maya = self.modules()
        p = self.paths()
        self.need(self.s.wrapped_obj, "fitted OBJ")
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
            cmds.setAttr(copies[mesh] + ".visibility", True)  # your mesh may be hidden; its rigged copy must show
            mm_maya.align_custom_mesh(copies[mesh], self.s.wrapped_obj)
            self.log(f"{copies[mesh]}: moved into DNA space")
        target = copies[self.s.custom_mesh]
        if cmds.objExists(PREVIEW_NAME):
            cmds.hide(PREVIEW_NAME)
        # lips / eyelids / mouth bag / eye sockets picked on your head: region-to-region transfer
        regions = {k: mm_maya.spec_vertices(spec).get(self.s.custom_mesh, []) for k, spec in (self.s.regions or {}).items() if spec}
        corr = mm_maya.region_correspondence(source, target, regions, log=self.log) if any(regions.values()) else None
        points = self.picked_points()
        lines_picked = bool(points and points.get("lines"))
        if lines_picked:  # lips and lids pair by where they sit against the lines, whatever the regions say
            corr = mm_maya.line_correspondence(source, target, points, corr, log=self.log)
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
            # the MetaHuman's gums and teeth lie across yours: closest point would split your teeth between the jaws
            import mm_core as core

            for mesh, (upper, lower, tongue) in self.teeth_arches(lambda m: mm_maya.mesh_points(copies[m])).items():
                mm_maya.set_rigid(copies[mesh], {core.TEETH_UPPER_JOINT: upper, core.TEETH_LOWER_JOINT: lower})
                self.log(f"{copies[mesh]}: upper teeth {len(upper)}, lower teeth {len(lower)} vertices follow their jaw whole"
                         + (f", tongue {len(tongue)} as the MetaHuman's" if tongue else ""))
        if self.s.blendshapes:
            # with lines, the sockets follow the MetaHuman's insides like the rest, so no lid tears away from them
            still = sorted(set(eye_parts.get(self.s.custom_mesh, []) + teeth_parts.get(self.s.custom_mesh, [])
                               + ([] if lines_picked else regions.get("eye_socket", []))))
            out["blendShape"] = mm_maya.transfer_blendshapes(source, target, keep_still=still, log=self.log, corr=corr)
            for mesh in teeth_parts:  # separate teeth / tongue meshes: the tongue shapes too
                if mesh != self.s.custom_mesh and teeth_source:
                    mm_maya.transfer_blendshapes(teeth_source, copies[mesh], log=self.log)
        # everything was built and transferred in DNA space: back onto your head, where it was
        mm_maya.place_in_scene(self.s.wrapped_obj, list(copies.values()))
        # the MetaHuman's own meshes only drive the rig now: hidden, your copies show
        cmds.hide([m for m in cmds.listRelatives("metaMutant_geometry", children=True, type="transform") or []
                   if m.endswith("_lod0_mesh")])
        mm_maya.plain_material_where_missing([copy for mesh, copy in copies.items() if mesh != self.s.custom_mesh], log=self.log)
        # your meshes stay as they were, only hidden: left showing they would stand still inside the moving copies
        cmds.hide(list(copies))
        self.log(f"rig placed on your head (its original position); your {', '.join(copies)} hidden, not changed")
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
