"""mm_fixes: the math of the lid and teeth corrections. No Maya."""

import os
import sys
import unittest

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import mm_fixes as mf  # noqa: E402
import mm_zones as mz  # noqa: E402


class Lids(unittest.TestCase):
    def setUp(self):
        # two parallel lines 1 apart in Y, the "lids" at full blink when they should meet
        self.pose = np.array([[x, 1.0, 0.0] for x in range(5)] + [[x, 0.0, 0.0] for x in range(5)], float)
        self.up, self.low = list(range(5)), list(range(5, 10))

    def test_the_gap_points_from_upper_to_where_it_should_be(self):
        t_up, gap_up, t_low, gap_low = mf.lid_gaps(self.pose, self.up, self.low, lambda t: np.zeros((len(t), 3)))
        np.testing.assert_allclose(gap_up, [[0, -1, 0]] * 5)
        np.testing.assert_allclose(gap_low, [[0, -1, 0]] * 5)
        self.assertEqual(float(t_up[0]), 0.0)
        self.assertEqual(float(t_low[-1]), 1.0)

    def test_lids_that_should_keep_apart_keep_apart(self):
        _, gap_up, _, _ = mf.lid_gaps(self.pose, self.up, self.low, lambda t: np.tile([0, 1.0, 0], (len(t), 1)))
        np.testing.assert_allclose(gap_up, np.zeros((5, 3)), atol=1e-12)

    def test_upper_comes_down_and_lower_comes_up_by_their_shares(self):
        z = mz.Zones(np.zeros(10, bool), np.array([mz.UPPER] * 5 + [mz.LOWER] * 5), np.r_[np.linspace(0, 1, 5), np.linspace(0, 1, 5)], np.zeros(10), 4.0)
        t_up, gap_up, t_low, gap_low = mf.lid_gaps(self.pose, self.up, self.low, lambda t: np.zeros((len(t), 3)))
        move = mf.delta_along_lines(z, np.arange(10), 1.0, t_up, gap_up, t_low, gap_low, upper_share=0.8)
        np.testing.assert_allclose(move[:5], [[0, -0.8, 0]] * 5)
        np.testing.assert_allclose(move[5:], [[0, 0.2, 0]] * 5)
        closed = self.pose + move
        np.testing.assert_allclose(closed[:5, 1], closed[5:, 1])

    def test_the_correction_fades_with_distance_from_the_line(self):
        fade = mf.falloff(np.array([0.0, 0.5, 1.0, 2.0]), 1.0)
        np.testing.assert_allclose(fade, [1.0, 0.5, 0.0, 0.0])


class Overlap(unittest.TestCase):
    def test_full_in_the_middle_nothing_at_the_corners(self):
        out = mf.overlap_along(np.array([0.0, 0.5, 1.0]), 0.2, [0, -1, 0])
        np.testing.assert_allclose(out, [[0, 0, 0], [0, -0.2, 0], [0, 0, 0]], atol=1e-6)


class Eye(unittest.TestCase):
    def test_a_point_inside_the_eye_comes_out_to_its_surface(self):
        move = mf.out_of_sphere(np.array([[0.5, 0, 0], [3.0, 0, 0]]), [0, 0, 0], 1.0)
        np.testing.assert_allclose(move, [[0.5, 0, 0], [0, 0, 0]])


class Teeth(unittest.TestCase):
    def test_the_back_stays_and_the_front_comes_in(self):
        p = np.array([[-2.0, 5.0, 0.0], [2.0, 5.0, 0.0], [0.0, 7.0, 10.0]])
        q = mf.narrowed(p, 0.5)
        np.testing.assert_allclose(q, [[-1.0, 5.0, 0.0], [1.0, 5.0, 0.0], [0.0, 7.0, 5.0]])


if __name__ == "__main__":
    unittest.main()
