"""
Tests for maya/tt_maya.py without Maya: names, reading the returned OBJ, checking it fits the base.

    python -m unittest discover -s tests/python -v
"""

import os
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "maya"))

import tt_maya  # noqa: E402

RESULT = "# Exported by TopoTransfer\n# space: original base coordinates\nv 0 1 2\nv 3 4 5.5\nvt 0 0\nf 1 2 1\n"


class TestMayaLink(unittest.TestCase):
    def write(self, text):
        fd, path = tempfile.mkstemp(suffix=".obj")
        with os.fdopen(fd, "w", newline="") as f:
            f.write(text)
        self.addCleanup(os.remove, path)
        return path

    def test_safe_names_for_files_and_nodes(self):
        self.assertEqual(tt_maya.safe_name("|grp|ns:body Mesh"), "body_Mesh")
        self.assertEqual(tt_maya.safe_name(":"), "mesh")

    def test_reads_vertices_in_file_order(self):
        self.assertEqual(tt_maya.obj_vertices(self.write(RESULT)), [(0.0, 1.0, 2.0), (3.0, 4.0, 5.5)])

    def test_result_must_be_a_topotransfer_export_of_the_base(self):
        path = self.write(RESULT)
        self.assertIsNone(tt_maya.result_problem(path, 2))
        self.assertIn("2 vertices, the base has 3", tt_maya.result_problem(path, 3))
        self.assertIn("not an OBJ exported by TopoTransfer", tt_maya.result_problem(self.write("v 0 0 0\n"), 1))

    def test_each_send_gets_its_own_folder(self):
        a = tt_maya.work_dir()
        self.assertTrue(os.path.isdir(a))
        self.assertIn("MutantTopoTransfer", a)


if __name__ == "__main__":
    unittest.main()
