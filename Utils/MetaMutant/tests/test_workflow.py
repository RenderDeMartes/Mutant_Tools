"""
Tests for mm_workflow.py (the Maya-independent part of the Meta Mutant window).

    python -m unittest discover -s tests -v
"""

import os
import sys
import tempfile
import time
import unittest
from unittest import mock

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
sys.path.insert(0, HERE)

import mm_core as core  # noqa: E402
import mm_dna  # noqa: E402
import mm_workflow as wf  # noqa: E402
from test_meta_mutant import FakeReader, write_wrapped  # noqa: E402


def write_obj(path, n, header=("Exported by TopoTransfer", "space: reference coordinates"), mtime=None):
    with open(path, "w") as f:
        for h in header:
            f.write(f"# {h}\n")
        for i in range(n):
            f.write(f"v {i} 0 0\n")
    if mtime is not None:
        os.utime(path, (mtime, mtime))


class TestWorkflow(unittest.TestCase):
    def test_settings_roundtrip_ignores_unknown_keys(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = wf.paths(tmp).settings
            s = wf.Settings(dna_path="a.dna", work_dir=tmp, joints="", lower_lods=False)
            wf.save_settings(s, p)
            self.assertEqual(wf.load_settings(p), s)
            with open(p, "w") as f:
                f.write('{"dna_path": "b.dna", "from_the_future": 1}')
            self.assertEqual(wf.load_settings(p).dna_path, "b.dna")
            self.assertEqual(wf.load_settings(os.path.join(tmp, "missing.json")), wf.Settings())

    def test_paths_match_pipeline_names(self):
        p = wf.paths("w")
        self.assertEqual(os.path.basename(p.base_obj), "mh_head_lod0.obj")
        # mm_dna.export_obj writes the manifest next to the OBJ with this name
        self.assertEqual(p.manifest, os.path.splitext(p.base_obj)[0] + ".manifest.json")
        # TopoTransfer's exporter downloads `<base stem>_wrapped.obj`
        self.assertEqual(os.path.basename(p.wrapped_obj), "mh_head_lod0_wrapped.obj")

    def test_joint_filter(self):
        self.assertTrue(wf.joint_filter("")("spine_01"))
        f = wf.joint_filter("FACIAL_, head")
        self.assertTrue(f("FACIAL_C_Jaw"))
        self.assertTrue(f("head"))
        self.assertFalse(f("neck_01"))

    def test_manifest_helpers(self):
        with tempfile.TemporaryDirectory() as tmp:
            manifest = mm_dna.export_obj("fake.dna", os.path.join(tmp, "mh_head_lod0.obj"), reader=FakeReader())
            self.assertEqual(wf.manifest_vertex_count(manifest), 7)
            self.assertEqual(wf.head_mesh_name(manifest), "head_lod0_mesh")

    def test_find_wrapped_obj(self):
        with tempfile.TemporaryDirectory() as work, tempfile.TemporaryDirectory() as downloads:
            now = time.time()
            write_obj(os.path.join(work, "mh_head_lod0_wrapped.obj"), 7, mtime=now - 100)
            write_obj(os.path.join(downloads, "mh_head_lod0_wrapped (1).obj"), 7, mtime=now - 10)
            write_obj(os.path.join(downloads, "mh_head_lod0_wrapped (2).obj"), 5, mtime=now)  # wrong count
            write_obj(os.path.join(downloads, "mh_head_lod0_wrapped (3).obj"), 7, header=("other tool",), mtime=now)
            write_obj(os.path.join(downloads, "other_wrapped.obj"), 7, mtime=now)
            dirs = [work, downloads]
            self.assertEqual(wf.find_wrapped_obj(dirs, 7), os.path.join(downloads, "mh_head_lod0_wrapped (1).obj"))
            self.assertEqual(wf.find_wrapped_obj(dirs, 5), os.path.join(downloads, "mh_head_lod0_wrapped (2).obj"))
            self.assertIsNone(wf.find_wrapped_obj(dirs, 7, newer_than=now - 5))
            self.assertIsNone(wf.find_wrapped_obj([os.path.join(work, "missing")], 7))

    def test_preview_matrix(self):
        r = FakeReader()
        with tempfile.TemporaryDirectory() as tmp:
            _, wrapped = write_wrapped(tmp, r)  # reference space
            self.assertEqual(wf.preview_matrix(wrapped), core.IDENTITY4)
            with open(wrapped) as f:
                text = f.read().replace("space: reference coordinates", "space: original base coordinates")
            with open(wrapped, "w") as f:
                f.write(text)
            self.assertEqual(wf.preview_matrix(wrapped), [2, 0, 0, 0, 0, 2, 0, 0, 0, 0, 2, 0, 10, 0, 0, 1])

    def test_status_and_warnings(self):
        with tempfile.TemporaryDirectory() as tmp:
            s = wf.Settings(work_dir=tmp, dna_path=os.path.join(tmp, "head.dna"))
            self.assertEqual(wf.status(s), {"setup": False, "export": False, "wrapped": False, "calibrated": False})
            p = wf.paths(tmp)
            for f in (s.dna_path, p.base_obj, p.manifest, p.reference_obj, p.wrapped_obj, p.custom_dna):
                open(f, "w").close()
            s.wrapped_obj = p.wrapped_obj
            self.assertTrue(all(wf.status(s).values()))
        self.assertEqual(wf.scene_warnings("cm", "y"), [])
        self.assertEqual(len(wf.scene_warnings("m", "z")), 2)


class TestBundledDnaModule(unittest.TestCase):
    def test_maya_2026_comes_with_its_dna_module(self):
        if not sys.platform.startswith("win"):
            self.skipTest("the bundled build is Windows only")
        folder = wf.bundled_dna_module("2026")
        self.assertTrue(os.path.isfile(os.path.join(folder, "dna.py")))
        self.assertTrue(any(f.endswith(".pyd") for f in os.listdir(folder)))
        self.assertTrue(os.path.isfile(os.path.join(folder, "LICENSE_OpenRigLogic.txt")))
        self.assertEqual(wf.bundled_dna_module("2023"), "")
        self.assertEqual(wf.bundled_dna_module(""), "")


class TestWrappedObjProblem(unittest.TestCase):
    WRAPPED = "# Exported by TopoTransfer\n# space: reference coordinates\nv 0 0 1\nv 1 0 1\nv 0 1 1\nf 1 2 3\n"
    BASE = "# MetaHuman LOD0\nv 0 0 0\nv 1 0 0\nv 0 1 0\nf 1 2 3\n"

    def test_checks_header_and_vertex_count(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = os.path.join(tmp, "w.obj")
            with open(p, "w", newline="") as f:
                f.write(self.WRAPPED)
            self.assertIsNone(wf.wrapped_obj_problem(p, 3))
            self.assertIsNone(wf.wrapped_obj_problem(p))
            self.assertIn("3 vertices, the exported Base has 4", wf.wrapped_obj_problem(p, 4))
            with open(p, "w", newline="") as f:
                f.write(self.BASE)
            self.assertIn("not an OBJ exported by TopoTransfer", wf.wrapped_obj_problem(p, 3))



if __name__ == "__main__":
    unittest.main()
