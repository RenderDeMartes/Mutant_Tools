"""mm_zones: pairing vertices by where they sit against the lip and eyelid lines. No Maya."""

import os
import sys
import unittest

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import mm_points as mp  # noqa: E402
import mm_zones as mz  # noqa: E402


def grid(nx, ny, sx=1.0, sy=1.0):
    """A flat sheet of quads in XY, centred on the origin. Returns points, counts, connects."""
    pts = [[(i - nx / 2) * sx, (j - ny / 2) * sy, 0.0] for j in range(ny + 1) for i in range(nx + 1)]
    counts, connects = [], []
    for j in range(ny):
        for i in range(nx):
            a = j * (nx + 1) + i
            counts.append(4)
            connects += [a, a + 1, a + nx + 2, a + nx + 1]
    return np.array(pts), counts, connects


def sheet_ring(nx, ny, half_w, half_h):
    """A closed line on the sheet: a box around the centre; corners at the far left and right on its middle row."""
    cx, cy = nx // 2, ny // 2
    at = lambda i, j: j * (nx + 1) + i  # noqa: E731
    top = [at(cx - half_w, cy)] + [at(i, cy + half_h) for i in range(cx - half_w, cx + half_w + 1)] + [at(cx + half_w, cy)]
    bottom = [at(cx - half_w, cy)] + [at(i, cy - half_h) for i in range(cx - half_w, cx + half_w + 1)] + [at(cx + half_w, cy)]
    # the columns between the corner and the rows, so the loop is really closed along edges
    left = [at(cx - half_w, j) for j in range(cy, cy + half_h + 1)]
    right = [at(cx + half_w, j) for j in range(cy, cy + half_h + 1)]
    left_low = [at(cx - half_w, j) for j in range(cy, cy - half_h - 1, -1)]
    right_low = [at(cx + half_w, j) for j in range(cy, cy - half_h - 1, -1)]
    upper = left + [at(i, cy + half_h) for i in range(cx - half_w + 1, cx + half_w)] + right[::-1]
    lower = left_low + [at(i, cy - half_h) for i in range(cx - half_w + 1, cx + half_w)] + right_low[::-1]
    return upper, lower


class Edges(unittest.TestCase):
    def test_unique_polygon_edges(self):
        _, counts, connects = grid(2, 1)
        self.assertEqual(len(mz.polygon_edges(counts, connects)), 7)


class Inside(unittest.TestCase):
    def setUp(self):
        self.p, counts, connects = grid(12, 12)
        self.e = mz.polygon_edges(counts, connects)
        self.upper, self.lower = sheet_ring(12, 12, 3, 2)

    def test_a_closed_line_cuts_the_mesh_in_two(self):
        z = mz.zones(self.p, self.e, mz.Ring("mouth", self.upper, self.lower, None), outside_seed=0)
        # inside the box: 5 by 3 vertices
        self.assertEqual(int(z.inside.sum()), 15)
        self.assertFalse(z.inside[0])

    def test_an_open_line_cuts_nothing(self):
        z = mz.zones(self.p, self.e, mz.Ring("mouth", self.upper[:4], self.lower[:4], None), outside_seed=0)
        self.assertEqual(int(z.inside.sum()), 0)

    def test_upper_and_lower_by_the_nearer_line_on_both_sides(self):
        z = mz.zones(self.p, self.e, mz.Ring("mouth", self.upper, self.lower, None), outside_seed=0)
        above_inside = int(np.flatnonzero((np.abs(self.p[:, 0]) < 0.1) & (self.p[:, 1] == 1))[0])
        below_inside = int(np.flatnonzero((np.abs(self.p[:, 0]) < 0.1) & (self.p[:, 1] == -1))[0])
        above_outside = int(np.flatnonzero((np.abs(self.p[:, 0]) < 0.1) & (self.p[:, 1] == 4))[0])
        below_outside = int(np.flatnonzero((np.abs(self.p[:, 0]) < 0.1) & (self.p[:, 1] == -4))[0])
        self.assertTrue(z.inside[above_inside] and z.inside[below_inside])
        self.assertFalse(z.inside[above_outside] or z.inside[below_outside])
        self.assertEqual(z.part[above_inside], mz.UPPER)
        self.assertEqual(z.part[below_inside], mz.LOWER)
        self.assertEqual(z.part[above_outside], mz.UPPER)
        self.assertEqual(z.part[below_outside], mz.LOWER)
        self.assertEqual(z.depth[above_outside], 2.0)
        self.assertEqual(z.depth[above_inside], 1.0)

    def test_the_line_itself_has_no_depth_and_runs_along(self):
        z = mz.zones(self.p, self.e, mz.Ring("mouth", self.upper, self.lower, None), outside_seed=0)
        self.assertTrue(all(z.depth[v] == 0 for v in self.upper + self.lower))
        self.assertEqual(z.along[self.upper[0]], 0.0)
        self.assertEqual(z.along[self.upper[-1]], 1.0)


class Pairing(unittest.TestCase):
    def setUp(self):
        self.p, counts, connects = grid(12, 12)
        self.e = mz.polygon_edges(counts, connects)
        self.upper, self.lower = sheet_ring(12, 12, 3, 2)
        self.ring = mz.Ring("mouth", self.upper, self.lower, None)

    def test_same_mesh_pairs_each_vertex_with_itself(self):
        z = mz.zones(self.p, self.e, self.ring, outside_seed=0)
        paired = mz.pair(z, z, reach=3.0)
        for v in self.upper + self.lower:
            ids, weights, mix = paired[v]
            self.assertEqual(ids[int(np.argmax(weights))], v)
            self.assertEqual(mix, 0.0)

    def test_inside_never_pairs_with_outside_nor_upper_with_lower(self):
        z = mz.zones(self.p, self.e, self.ring, outside_seed=0)
        for t, (ids, weights, _) in mz.pair(z, z, reach=3.0).items():
            for v, w in zip(ids, weights):
                if w > 0.01 and z.depth[v] > 0 and z.depth[t] > 0:
                    self.assertEqual(bool(z.inside[v]), bool(z.inside[t]))
                    self.assertEqual(z.part[v], z.part[t])

    def test_a_mouth_of_another_depth_meets_at_the_bottom(self):
        # the other mesh is the same topology with its inside pushed twice as far along the surface
        z = mz.zones(self.p, self.e, self.ring, outside_seed=0)
        deep = mz.Zones(z.inside, z.part, z.along, np.where(z.inside, z.depth * 2, z.depth), z.length)
        t = int(np.flatnonzero(z.inside & (z.depth == z.depth[z.inside].max()))[0])
        ids, weights, _ = mz.pair(deep, z, reach=3.0)[t]
        self.assertEqual(z.depth[ids[int(np.argmax(weights))]], z.depth[z.inside].max())

    def test_the_outside_blends_back_into_closest_point_within_its_reach(self):
        self.assertEqual(float(mz.blend(np.array([0.0]), 4.0)[0]), 0.0)
        self.assertEqual(float(mz.blend(np.array([2.0]), 4.0)[0]), 0.0)
        self.assertEqual(float(mz.blend(np.array([4.0]), 4.0)[0]), 1.0)
        self.assertTrue(0 < float(mz.blend(np.array([3.0]), 4.0)[0]) < 1)
        z = mz.zones(self.p, self.e, self.ring, outside_seed=0)
        far = np.flatnonzero(~z.inside & (z.depth >= 3.0))
        paired = mz.pair(z, z, reach=3.0)
        self.assertTrue(all(int(v) not in paired for v in far))


class Along(unittest.TestCase):
    def test_a_line_of_few_vertices_leaves_no_steps_along_it(self):
        # a line with two vertices; points above it must not all take the parameter of one end
        line = np.array([[0.0, 0, 0], [10.0, 0, 0]])
        params = np.array([0.0, 1.0])
        query = np.array([[2.0, 3, 0], [7.0, 3, 0]])
        out = mz._along_segments(query, line, params, np.array([0.0, 1.0]))
        np.testing.assert_allclose(out, [0.2, 0.7])

    def test_beyond_its_ends_the_parameter_stops(self):
        line = np.array([[0.0, 0, 0], [10.0, 0, 0]])
        out = mz._along_segments(np.array([[-5.0, 1, 0]]), line, np.array([0.0, 1.0]), np.array([0.0]))
        self.assertEqual(float(out[0]), 0.0)


class Smooth(unittest.TestCase):
    def test_neighbours_share_sources_and_stay_normalised(self):
        around = [[1], [0, 2], [1]]
        out = mz.smooth_pairs({0: {10: 1.0}, 1: {11: 1.0}, 2: {12: 1.0}}, around, np.zeros(3, bool), rounds=1, amount=0.5)
        self.assertAlmostEqual(sum(out[1].values()), 1.0)
        self.assertAlmostEqual(out[1][11], 0.5)
        self.assertAlmostEqual(out[1][10], 0.25)
        self.assertAlmostEqual(out[0][11], 0.5)

    def test_the_lines_themselves_do_not_move(self):
        around = [[1], [0]]
        out = mz.smooth_pairs({0: {10: 1.0}, 1: {11: 1.0}}, around, np.array([True, False]), rounds=2, amount=0.5)
        self.assertEqual(out[0], {10: 1.0})
        self.assertGreater(out[1][10], 0.0)

    def test_it_keeps_only_the_strongest_sources(self):
        around = [[1, 2, 3], [0], [0], [0]]
        pairs = {0: {i: 0.25 for i in range(4)}, 1: {i + 10: 0.25 for i in range(4)}, 2: {i + 20: 0.25 for i in range(4)}, 3: {i + 30: 0.25 for i in range(4)}}
        out = mz.smooth_pairs(pairs, around, np.zeros(4, bool), rounds=1, keep=5)
        self.assertEqual(len(out[0]), 5)
        self.assertAlmostEqual(sum(out[0].values()), 1.0)


class Correspondence(unittest.TestCase):
    def test_lines_override_the_base_near_them_and_leave_the_rest(self):
        import mm_points

        p, counts, connects = grid(12, 12)
        e = mz.polygon_edges(counts, connects)
        upper, lower = sheet_ring(12, 12, 3, 2)
        ring = mz.Ring("mouth", upper, lower, None)
        base = [((1, 2, 3), (0.5, 0.25, 0.25)) for _ in range(len(p))]
        orig = mz.rings_of
        mz.rings_of = lambda *_: [(ring, ring)]
        try:
            out = mz.correspondence({}, p, e, p, e, base, log=lambda t: None)
        finally:
            mz.rings_of = orig
        self.assertEqual(out[0], base[0])  # the far corner of the sheet
        ids, weights = out[upper[3]]
        self.assertEqual(ids[int(np.argmax(weights))], upper[3])
        self.assertAlmostEqual(sum(weights), 1.0)
        for ids, weights in out:
            self.assertAlmostEqual(sum(weights), 1.0)
        self.assertEqual(len(mm_points.LINE_PAIRS), 3)

    def test_no_lines_picked_is_the_base_as_it_is(self):
        p = np.zeros((40000, 3))
        base = [((0, 1, 2), (1.0, 0.0, 0.0))] * 5
        self.assertEqual(mz.correspondence({"lines": {}}, p[:5], np.zeros((0, 2), int), p, np.zeros((0, 2), int), base), base)


if __name__ == "__main__":
    unittest.main()
