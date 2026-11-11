"""
Tests for Dev/MayaMCP/fit_math.py (pure math, runs outside Maya).

Run from the Mutant_Tools root:
    python -m pytest Tests/test_maya_mcp_fit_math.py -v
    python Tests/test_maya_mcp_fit_math.py
"""
import importlib.util
import math
import unittest
from pathlib import Path

_PATH = Path(__file__).resolve().parents[1] / 'Dev' / 'MayaMCP' / 'fit_math.py'
_spec = importlib.util.spec_from_file_location('fit_math', _PATH)
fm = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(fm)

# Cross-section profiles measured on a creature foot (dist from the nail, mean
# radius), walked tip -> root. The creases and the base were checked by eye on
# the mesh: each toe has two creases, then merges into the foot pad.
TOES = {
    'Inner': [(0.5, 1.03), (1.0, 1.22), (1.5, 1.3), (2.0, 1.61), (2.5, 1.76), (3.0, 1.87), (3.5, 1.89), (4.0, 1.88), (4.5, 1.8), (5.0, 1.6), (5.5, 1.62), (6.0, 1.7), (6.5, 1.78), (7.0, 1.8), (7.5, 1.76), (8.0, 1.66), (8.5, 1.58), (9.0, 1.78), (9.5, 1.89), (10.0, 1.94), (10.5, 1.94), (11.0, 2.0), (11.5, 1.98), (12.0, 2.12), (12.5, None), (13.0, 4.03), (13.5, 4.59)],
    'InMid': [(0.5, 1.03), (1.0, 1.24), (1.5, 1.43), (2.0, 1.52), (2.5, 1.77), (3.0, 1.97), (3.5, 2.05), (4.0, 2.08), (4.5, 2.12), (5.0, 2.01), (5.5, 1.82), (6.0, 1.74), (6.5, 1.81), (7.0, 1.95), (7.5, 2.01), (8.0, 2.0), (8.5, 1.93), (9.0, 1.82), (9.5, 1.78), (10.0, 1.96), (10.5, 2.05), (11.0, 2.11), (11.5, 2.2), (12.0, 2.26), (12.5, 2.27), (13.0, 3.06), (13.5, 4.44)],
    'Mid': [(0.5, 0.79), (1.0, 1.18), (1.5, 1.4), (2.0, 1.52), (2.5, 1.62), (3.0, 1.86), (3.5, 2.13), (4.0, 2.29), (4.5, 2.32), (5.0, 2.27), (5.5, 2.28), (6.0, 2.16), (6.5, 2.07), (7.0, 1.99), (7.5, 2.03), (8.0, 2.18), (8.5, 2.26), (9.0, 2.24), (9.5, 2.2), (10.0, 2.14), (10.5, 2.01), (11.0, 2.07), (11.5, 2.2), (12.0, 2.32), (12.5, 2.37), (13.0, 2.48), (13.5, 2.54), (14.0, 2.57), (14.5, 2.63), (15.0, 2.64), (15.5, 4.04), (16.0, 4.62)],
    'OutMid': [(0.5, 0.94), (1.0, 1.21), (1.5, 1.41), (2.0, 1.49), (2.5, 1.71), (3.0, 1.96), (3.5, 2.08), (4.0, 2.1), (4.5, 2.09), (5.0, 2.01), (5.5, 1.88), (6.0, 1.77), (6.5, 1.81), (7.0, 1.96), (7.5, 2.05), (8.0, 2.0), (8.5, 1.95), (9.0, 1.88), (9.5, 1.8), (10.0, 1.92), (10.5, 2.04), (11.0, 2.11), (11.5, 2.2), (12.0, 2.22), (12.5, 2.3), (13.0, 3.09), (13.5, 4.56)],
    'Outer': [(0.5, 1.08), (1.0, 1.25), (1.5, 1.28), (2.0, 1.63), (2.5, 1.78), (3.0, 1.87), (3.5, 1.88), (4.0, 1.87), (4.5, 1.77), (5.0, 1.56), (5.5, 1.69), (6.0, 1.75), (6.5, 1.77), (7.0, 1.78), (7.5, 1.72), (8.0, 1.62), (8.5, 1.67), (9.0, 1.79), (9.5, 1.91), (10.0, 1.93), (10.5, 1.98), (11.0, 1.99), (11.5, 2.07), (12.0, 3.72), (12.5, 4.4)],
}
# expected (base, creases root -> tip) in distance from the nail
EXPECTED = {
    'Inner': (12.0, [8.5, 5.0]),
    'InMid': (12.5, [9.5, 6.0]),
    'Mid': (15.0, [10.5, 7.0]),
    'OutMid': (12.5, [9.5, 6.0]),
    'Outer': (11.5, [8.0, 5.0]),
}
# the back toe is a spur: it widens steadily and has no crease
BACK = [(0.5, 0.86), (1.0, 1.2), (1.5, 1.36), (2.0, 1.8), (2.5, 1.96), (3.0, 2.03), (3.5, 2.04), (4.0, 2.04), (4.5, 2.24), (5.0, 2.41), (5.5, 2.49), (6.0, 2.6), (6.5, 2.91), (7.0, 3.1), (7.5, 4.36)]


def _dists(profile, indices):
    clean = fm._clean(profile)
    return [clean[i][0] for i in indices]


class TestTubeProfiles(unittest.TestCase):

    def test_toe_joints_match_the_mesh(self):
        for name, profile in TOES.items():
            base, creases = EXPECTED[name]
            got = _dists(profile, fm.tube_joint_indices(profile))
            self.assertEqual(len(got), 3, name)
            for want, have in zip([base] + creases, got):
                self.assertAlmostEqual(have, want, delta=0.5, msg='{}: {}'.format(name, got))

    def test_count_keeps_the_creases_nearest_the_base(self):
        got = _dists(TOES['Mid'], fm.tube_joint_indices(TOES['Mid'], count=2))
        self.assertEqual(got, [15.0, 10.5])

    def test_spur_without_creases_gives_only_the_base(self):
        idx = fm.tube_joint_indices(BACK)
        self.assertEqual(_dists(BACK, idx), [7.0])

    def test_merge_ignores_missing_samples(self):
        # Inner has a slice without a loop right before the foot pad
        self.assertEqual(_dists(TOES['Inner'], [fm.find_merge(TOES['Inner'])]), [12.0])

    def test_shallow_wobble_is_not_a_crease(self):
        flat = [(i * 0.5, 2.0 + (0.01 if i % 2 else 0.0)) for i in range(30)]
        self.assertEqual(fm.find_creases(flat), [])

    def test_empty_profile_raises(self):
        with self.assertRaises(ValueError):
            fm.find_merge([(0.5, None)])


class TestLinesAndPlanes(unittest.TestCase):

    def test_fit_line_direction_and_order(self):
        pts = [[1 + 0.01 * ((i * 7) % 3 - 1), 10 - i, 2 * i] for i in range(10)]
        c, d = fm.fit_line(pts)
        want = fm._unit([0, -1, 2])
        self.assertGreater(fm._dot(d, want), 0.999)
        c2, d2 = fm.fit_line(pts[::-1])
        self.assertLess(fm._dot(d2, want), -0.999)

    def test_closest_points_of_crossing_lines(self):
        mid, gap = fm.closest_points([0, 0, 0], [1, 0, 0], [5, -3, 0], [0, 1, 0])
        self.assertAlmostEqual(gap, 0.0, places=6)
        for a, b in zip(mid, [5, 0, 0]):
            self.assertAlmostEqual(a, b, places=6)

    def test_closest_points_of_skew_lines(self):
        mid, gap = fm.closest_points([0, 0, 0], [1, 0, 0], [0, 0, 2], [0, 1, 0])
        self.assertAlmostEqual(gap, 2.0, places=6)
        self.assertAlmostEqual(mid[2], 1.0, places=6)

    def test_parallel_lines_raise(self):
        with self.assertRaises(ValueError):
            fm.closest_points([0, 0, 0], [1, 0, 0], [0, 1, 0], [2, 0, 0])

    def test_fit_plane_any_orientation(self):
        n = fm._unit([0.3, -0.2, 0.93])
        a = fm._unit([n[1], -n[0], 0])
        b = [n[1] * a[2] - n[2] * a[1], n[2] * a[0] - n[0] * a[2], n[0] * a[1] - n[1] * a[0]]
        pts = [fm._add([4, 5, 6], fm._add(fm._mul(a, math.cos(t) * 10), fm._mul(b, math.sin(t) * 3)))
               for t in [i * 0.7 for i in range(9)]]
        c, normal = fm.fit_plane(pts)
        self.assertGreater(abs(fm._dot(normal, n)), 0.9999)
        off = fm._add(pts[0], fm._mul(n, 2.5))
        p = fm.project_to_plane(off, c, normal)
        self.assertAlmostEqual(fm._dot(fm._sub(p, c), normal), 0.0, places=6)

    def test_collinear_plane_raises(self):
        with self.assertRaises(ValueError):
            fm.fit_plane([[0, 0, 0], [1, 1, 1], [2, 2, 2]])

    def test_plane_axes_longest_first(self):
        pts = [[math.cos(t) * 9, 0, math.sin(t) * 2] for t in [i * 0.5 for i in range(13)]]
        c, e1, e2, n = fm.plane_axes(pts)
        self.assertGreater(abs(e1[0]), 0.99)
        self.assertGreater(abs(e2[2]), 0.99)
        self.assertGreater(abs(n[1]), 0.99)


if __name__ == '__main__':
    unittest.main()
