"""
Tests for mm_controller (the UI-free Meta Mutant workflow its window drives). No Maya needed.

    python -m unittest discover -s tests -v
"""

import http.server
import os
import socket
import sys
import tempfile
import threading
import types
import unittest
from unittest import mock

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))

import mm_controller as mc  # noqa: E402
import mm_workflow as wf  # noqa: E402
import tt_app  # noqa: E402


def fake_maya(cmds):
    maya = types.ModuleType("maya")
    maya.cmds = cmds
    return {"maya": maya, "maya.cmds": cmds}


class TestController(unittest.TestCase):
    def test_finds_the_topotransfer_app(self):
        self.assertTrue(os.path.isfile(os.path.join(tt_app.ROOT, "package.json")))

    def test_prepare_and_apply_run_their_steps_in_order(self):
        w = mc.Workflow(log=lambda t: None)
        calls = []
        for name in ("export", "open_app", "import_wrapped", "calibrate", "remove_result", "build_rig", "transfer", "build_face_board"):
            setattr(w, name, (lambda n: lambda: calls.append(n))(name))
        w.prepare()
        self.assertEqual(calls, ["export", "open_app"])
        calls.clear()
        w.apply_all()
        self.assertEqual(calls, ["import_wrapped", "calibrate", "remove_result", "build_rig", "transfer", "build_face_board"])
        calls.clear()

        def bad():
            raise RuntimeError("joint convention mismatch")

        w.build_rig = bad
        with self.assertRaises(RuntimeError):
            w.apply_all()
        self.assertEqual(calls, ["import_wrapped", "calibrate", "remove_result"])  # transfer never ran

    def test_needs_maya_2026(self):
        w = mc.Workflow(log=lambda t: None)
        with mock.patch.object(mc, "maya_version", return_value="2024"):
            with self.assertRaisesRegex(RuntimeError, "needs Maya 2026"):
                w.modules()

    def test_clear_errors_for_missing_inputs(self):
        w = mc.Workflow(log=lambda t: None)
        with self.assertRaisesRegex(RuntimeError, "Work folder"):
            w.paths()
        with self.assertRaisesRegex(RuntimeError, "Head DNA not found"):
            w.need("", "Head DNA")

    def test_result_from_the_app_updates_settings_and_notifies(self):
        with tempfile.TemporaryDirectory() as work:
            changed, logs = [], []
            w = mc.Workflow(wf.Settings(work_dir=work), log=logs.append, on_change=lambda: changed.append(True), call_on_main=lambda fn, *a: fn(*a))
            path = os.path.join(work, "mh_head_lod0_wrapped.obj")
            w._result_arrived(path)
            self.assertEqual(w.s.wrapped_obj, path)
            self.assertEqual(changed, [True])
            self.assertIn("received", logs[-1])
            self.assertTrue(os.path.isfile(wf.paths(work).settings))  # remembered
            self.assertTrue(w.status()["wrap"] is False)  # file itself not written in this test

    def test_open_app_serves_the_bundled_app_with_both_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo, work = os.path.join(tmp, "repo"), os.path.join(tmp, "work")
            os.makedirs(os.path.join(repo, "app"))
            os.makedirs(work)
            with open(os.path.join(repo, "app", "index.html"), "w") as f:
                f.write("<html></html>")
            p = wf.paths(work)
            for path in (p.base_obj, p.reference_obj):
                with open(path, "w") as f:
                    f.write("v 0 0 0\n")
            with open(p.manifest, "w") as f:
                f.write('{"format": "topotransfer-metahuman-manifest/1", "dna": "x", "lod": 0, "meshes": [{"name": "head", "dna_index": 0, "vertex_count": 1, "offset": 0}]}')
            w = mc.Workflow(wf.Settings(work_dir=work), log=lambda t: None)
            with mock.patch.object(mc.tt_app, "ROOT", repo), mock.patch.object(mc.webbrowser, "open") as browser, \
                    mock.patch.object(mc.tt_app, "ensure_app_running") as dev_server:
                w.open_app()
                try:
                    url = browser.call_args[0][0]
                    self.assertTrue(url.startswith(f"http://127.0.0.1:{w.bridge.port}/{w.bridge.token}/app/?base="), url)
                    self.assertIn("reference=", url)
                    self.assertIn("return=", url)
                    dev_server.assert_not_called()  # bundled app: no Node.js needed
                finally:
                    w.stop_link()
            self.assertIsNone(w.bridge)

    def test_selected_meshes_resolves_shapes_and_components(self):
        cmds = mock.MagicMock()
        cmds.ls.return_value = ["head_geoShape", "head_geo"]
        cmds.nodeType.side_effect = lambda n: "mesh" if n.endswith("Shape") else "transform"
        cmds.listRelatives.side_effect = lambda n, **k: ["head_geo"] if k.get("parent") else (["head_geoShape"] if n == "head_geo" else [])
        with mock.patch.dict(sys.modules, fake_maya(cmds)):
            self.assertEqual(mc.selected_meshes(), ["head_geo"])


if __name__ == "__main__":
    unittest.main()
