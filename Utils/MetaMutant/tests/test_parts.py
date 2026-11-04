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


def box(centre, size, n=3):
    """Points of a small grid block, as a tooth or a gum."""
    return [tuple(centre[k] + size[k] * (((i, j, m)[k]) / (n - 1) - 0.5) for k in range(3))
            for i in range(n) for j in range(n) for m in range(n)]


class TestPivots(unittest.TestCase):
    def test_eyeball_fit_ignores_what_is_in_front(self):
        c, r = (3.0, 150.0, 8.0), 2.0
        points = []
        for p in sphere(c, r, n=24):
            if p[2] > c[2] + r * 0.8:  # the iris: a dent, flat
                p = (p[0], p[1], c[2] + r * 0.8)
            points.append(p)
        fitted, radius = core.eyeball_fit(points)
        self.assertTrue(close(fitted, c, 1e-3), fitted)
        self.assertAlmostEqual(radius, r, places=3)
        self.assertGreater(core._dist(core.sphere_fit(points)[0], c), 0.01)  # a fit of the whole is pulled off

    def test_hinge_moves_with_the_skin_beside_it_not_the_chin(self):
        hinge = (0.0, 145.0, 2.0)
        old, new = [], []
        for x in (-7.0, -6.0, 6.0, 7.0):
            for dy in (-0.5, 0.5):
                old.append((x, hinge[1] + dy, hinge[2]))
                new.append((x, hinge[1] + dy - 0.1, hinge[2] + 0.9))
        for x in (-1.0, 0.0, 1.0):  # the chin: far from the hinge, moved a lot
            old.append((x, 135.0, 10.0))
            new.append((x, 130.0, 10.0))
        self.assertTrue(close(core.hinge_delta(old, new, hinge), (0.0, -0.1, 0.9)))
        self.assertIsNone(core.hinge_delta(old, new, (100.0, 145.0, 2.0)))


class TestLidTravel(unittest.TestCase):
    def test_keeps_the_distance_within_its_range(self):
        self.assertAlmostEqual(core.lid_travel(1.3, 2.0), 0.65)
        self.assertEqual(core.lid_travel(1.0, 5.0), core.LID_TRAVEL_RANGE[0])
        self.assertEqual(core.lid_travel(None, 2.0), 1.0)


class TestTeethParts(unittest.TestCase):
    def pieces(self, *blocks):
        points, shells = [], []
        for block in blocks:
            shells.append(list(range(len(points), len(points) + len(block))))
            points += block
        return points, shells

    def test_every_piece_goes_whole_to_one_arch(self):
        points, shells = self.pieces(box((0, 10, 5), (14, 3, 11)), box((-5, 8.5, 12), (2, 3, 1)), box((5, 8.5, 12), (2, 3, 1)),
                                     box((0, 5, 5), (14, 3, 11)), box((-5, 7, 12), (2, 3, 1)), box((5, 7, 12), (2, 3, 1)))
        upper, lower, tongue = core.teeth_parts(points, shells)
        self.assertEqual(sorted(upper), sorted(shells[0] + shells[1] + shells[2]))
        self.assertEqual(sorted(lower), sorted(shells[3] + shells[4] + shells[5]))
        self.assertEqual(tongue, [])

    def test_the_tongue_is_left_to_itself(self):
        points, shells = self.pieces(box((0, 10, 5), (14, 3, 11)), box((0, 5, 5), (14, 3, 11)), box((0, 7, 5), (6, 2, 9)))
        upper, lower, tongue = core.teeth_parts(points, shells)
        self.assertEqual(tongue, shells[2])
        self.assertEqual(upper, shells[0])
        self.assertEqual(lower, shells[1])

    def test_arches_in_one_piece_split_by_height(self):
        points, shells = self.pieces(box((0, 10, 5), (14, 3, 11)) + box((0, 5, 5), (14, 3, 11)))
        upper, lower, _ = core.teeth_parts(points, shells)
        self.assertTrue(all(points[i][1] > 7 for i in upper) and all(points[i][1] < 7 for i in lower))
        self.assertEqual(len(upper), len(lower))

    def test_metahuman_arches_by_their_weights(self):
        names = ["FACIAL_C_TeethUpper", "FACIAL_C_TeethLower", "FACIAL_C_Tongue1"]
        skin = [[(0, 1.0)], [(0, 0.6), (1, 0.4)], [(1, 1.0)], [(2, 1.0)]]
        self.assertEqual(core.mh_teeth_arches(skin, names), ([0, 1], [2, 3], [0], [2]))


class TestFitParts(unittest.TestCase):
    def test_each_arch_goes_onto_yours(self):
        blocks = [core.MeshBlock("teeth_lod0_mesh", 0, 6, 0)]
        pos = {0: [(-1, 2, 0), (1, 4, 2), (-1, 0, 0), (1, 1, 2), (0, 3, 1), (0, 0.5, 1)]}
        upper_mine = [(-2, 12, 0), (2, 16, 2)]
        lower_mine = [(-2, 5, 0), (2, 7, 2)]
        report = core.fit_parts(pos, blocks, teeth=upper_mine + lower_mine, arches=(upper_mine, lower_mine),
                                mh_arches=lambda b: ([0, 1, 4], [2, 3, 5], [0, 1], [2, 3]))
        self.assertTrue(close(pos[0][0], (-2, 12, 0)) and close(pos[0][1], (2, 16, 2)))
        self.assertTrue(close(pos[0][2], (-2, 5, 0)) and close(pos[0][3], (2, 7, 2)))
        self.assertIn("each arch", report[0])

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
