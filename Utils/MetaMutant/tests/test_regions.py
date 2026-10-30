"""mm_regions: MetaHuman regions from skin weights, region-restricted closest points (no Maya)."""

import os
import sys
import unittest

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import mm_regions as rg  # noqa: E402


class TestRegions(unittest.TestCase):
    def test_regions_from_skin_weights(self):
        joints = ["head", "FACIAL_C_LipUpper1", "FACIAL_L_12IPV_LipLower3", "FACIAL_L_EyelidUpperA2", "FACIAL_C_MouthInteriorUpper"]
        weights = [
            [(0, 1.0)],                    # skin
            [(1, 0.8), (0, 0.2)],          # upper lip
            [(2, 0.5), (1, 0.3), (0, 0.2)],  # lower lip wins
            [(3, 0.4), (0, 0.6)],          # upper eyelid (above the threshold)
            [(4, 0.2), (0, 0.8)],          # too little mouth: skin
        ]
        r = rg.metahuman_regions(joints, weights)
        self.assertEqual(r["upper_lip"], [1])
        self.assertEqual(r["lower_lip"], [2])
        self.assertEqual(r["upper_eyelid"], [3])
        self.assertEqual(r["mouth_bag"], [])

    def test_lips_touching_take_their_own_lip(self):
        # two horizontal strips (MetaHuman upper lip at y=0.01, lower lip at y=-0.01), touching
        src = np.array([[0, 0.01, 0], [1, 0.01, 0], [0, 0.01, 1], [0, -0.01, 0], [1, -0.01, 0], [0, -0.01, 1]], float)
        tris = np.array([[0, 1, 2], [3, 4, 5]])
        # your lips: the upper one sits slightly low (nearer the MetaHuman's lower lip)
        tgt = np.array([[0.2, -0.008, 0.2], [0.2, -0.012, 0.2]], float)
        plain = rg.correspondence(tgt, src, tris, rg.groups(2, {}, 6, {}))
        self.assertEqual(plain[0][0], (3, 4, 5))  # without regions: the wrong lip
        g = rg.groups(2, {"upper_lip": [0], "lower_lip": [1]}, 6, {"upper_lip": [0, 1, 2], "lower_lip": [3, 4, 5]})
        tri, w = rg.correspondence(tgt, src, tris, g)[0]
        self.assertEqual(tri, (0, 1, 2))
        self.assertAlmostEqual(sum(w), 1.0)
        self.assertEqual(rg.correspondence(tgt, src, tris, g)[1][0], (3, 4, 5))

    def test_unpicked_vertices_avoid_picked_regions(self):
        src = np.array([[0, 0, 0], [1, 0, 0], [0, 1, 0], [5, 0, 0], [6, 0, 0], [5, 1, 0]], float)
        tris = np.array([[0, 1, 2], [3, 4, 5]])
        g = rg.groups(1, {"upper_lip": []}, 6, {"upper_lip": [0, 1, 2]})
        # nothing picked on your head: everything may use everything
        self.assertEqual(rg.correspondence(np.array([[0.1, 0.1, 0]]), src, tris, g)[0][0], (0, 1, 2))
        g = rg.groups(2, {"upper_lip": [1]}, 6, {"upper_lip": [0, 1, 2]})
        # vertex 0 is not lip: it may not use the MetaHuman's lip, even if it is closer
        self.assertEqual(rg.correspondence(np.array([[0.1, 0.1, 0], [0.1, 0.1, 0]]), src, tris, g)[0][0], (3, 4, 5))

    def test_closest_point_inside_and_on_edges(self):
        a, b, c = np.array([0, 0, 0.0]), np.array([1, 0, 0.0]), np.array([0, 1, 0.0])
        d, w = rg._closest_on_triangle(np.array([0.25, 0.25, 2.0]), a, b, c)
        self.assertAlmostEqual(d, 4.0)
        np.testing.assert_allclose(w, (0.5, 0.25, 0.25))
        d, w = rg._closest_on_triangle(np.array([2.0, -1.0, 0.0]), a, b, c)
        np.testing.assert_allclose(w, (0, 1, 0))


if __name__ == "__main__":
    unittest.main()
