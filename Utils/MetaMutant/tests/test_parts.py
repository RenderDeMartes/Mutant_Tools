"""
Tests for fitting the MetaHuman eyes and teeth onto the artist's (mm_core.fit_parts). Pure Python.

    python -m unittest discover -s tests -v
"""

import math
import os
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))

import mm_core as core  # noqa: E402


def sphere(c, r, n=12, cap=1.0):
    """Points on a sphere; cap < 1 keeps only the front part (a picked set of faces)."""
    pts = []
    for i in range(1, n):
        th = math.pi * i / n
        if math.cos(th) < 1 - 2 * cap:
            continue
        for k in range(n):
            ph = 2 * math.pi * k / n
            pts.append((c[0] + r * math.sin(th) * math.cos(ph), c[1] + r * math.sin(th) * math.sin(ph), c[2] + r * math.cos(th)))
    return pts


def close(a, b, tol=1e-6):
    return all(abs(x - y) <= tol for x, y in zip(a, b))


class TestFitParts(unittest.TestCase):
    def test_sphere_fit_on_a_whole_and_a_partial_sphere(self):
        for cap in (1.0, 0.4):
            c, r = core.sphere_fit(sphere((3, -2, 7), 1.5, cap=cap))
            self.assertTrue(close(c, (3, -2, 7), 1e-6), (cap, c))
            self.assertAlmostEqual(r, 1.5, places=6)

    def test_split_two_eyes_picked_together(self):
        a, b = core.split_two(sphere((-3, 0, 0), 1) + sphere((3, 0, 0), 1))
        centres = sorted([core.centroid(a), core.centroid(b)])
        self.assertTrue(close(centres[0], (-3, 0, 0), 1e-6))
        self.assertTrue(close(centres[1], (3, 0, 0), 1e-6))

    def blocks(self):
        meshes = {
            "head_lod0_mesh": [(0, 0, 0), (1, 1, 1), (2, 0, 1), (0, 2, 0)],
            "eyeLeft_lod0_mesh": sphere((3, 160, 8), 1.2),
            "eyeRight_lod0_mesh": sphere((-3, 160, 8), 1.2),
            "eyeshell_lod0_mesh": [(3, 160, 9.3), (-3, 160, 9.3)],
            "teeth_lod0_mesh": [(-2, 150, 6), (2, 150, 6), (0, 148, 2), (0, 152, 7)],
            "saliva_lod0_mesh": [(0, 150, 5)],
        }
        blocks, positions, offset = [], {}, 0
        for i, (name, pts) in enumerate(meshes.items()):
            blocks.append(core.MeshBlock(name, i, len(pts), offset))
            positions[i] = list(pts)
            offset += len(pts)
        return blocks, positions

    def test_eyes_go_onto_the_nearer_picked_eye_and_the_shell_follows(self):
        blocks, pos = self.blocks()
        # one selection with both eyes, a little wider apart and bigger than the MetaHuman's
        report = core.fit_parts(pos, blocks, eyes=[sphere((-3.5, 161, 8.5), 1.4) + sphere((3.5, 161, 8.5), 1.4)])
        left, right = core.sphere_fit(pos[1]), core.sphere_fit(pos[2])
        self.assertTrue(close(left[0], (3.5, 161, 8.5), 1e-6), left)
        self.assertTrue(close(right[0], (-3.5, 161, 8.5), 1e-6), right)
        self.assertAlmostEqual(left[1], 1.4, places=6)
        self.assertGreater(pos[3][0][0], 3.0)  # the shell vertex near the left eye moved with it
        self.assertEqual(pos[0], self.blocks()[1][0])  # the head is not touched
        self.assertTrue(any("eyeshell" in line for line in report))

    def test_teeth_and_saliva_go_onto_the_picked_teeth_box(self):
        blocks, pos = self.blocks()
        picked = [(-2.5, 149, 6.5), (2.5, 149, 6.5), (0, 147, 2.5), (0, 151, 7.5)]
        core.fit_parts(pos, blocks, teeth=picked)
        self.assertTrue(close(core.bounds(pos[4])[0], core.bounds(picked)[0]))
        self.assertTrue(close(core.bounds(pos[4])[1], core.bounds(picked)[1]))
        self.assertTrue(close(pos[5][0], (0.0, 149.0, 5.5 + 0.0)), pos[5])

    def test_nothing_picked_nothing_changes(self):
        blocks, pos = self.blocks()
        before = {k: list(v) for k, v in pos.items()}
        self.assertEqual(core.fit_parts(pos, blocks), [])
        self.assertEqual(pos, before)


class TestComponentIds(unittest.TestCase):
    def test_blendshape_component_lists(self):
        import mm_maya

        self.assertEqual(mm_maya._component_ids(["vtx[3]", "vtx[5:8]", "vtx[0]"]), [3, 5, 6, 7, 8, 0])
        self.assertEqual(mm_maya._component_ids([]), [])


if __name__ == "__main__":
    unittest.main()
