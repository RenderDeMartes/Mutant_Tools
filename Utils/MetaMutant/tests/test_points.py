"""mm_points: what is picked in the Pick Points window and how it reaches TopoTransfer. No Maya."""

import os
import re
import sys
import tempfile
import unittest

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import mm_points as mp  # noqa: E402

PRESETS = os.path.join(os.path.dirname(HERE), "..", "TopoTransfer", "src", "engine", "landmarks", "presets.ts")


def fake_base():
    """A MetaHuman-sized list of positions: every vertex at (id / 1000, 0, 0), its X rising with its id."""
    n = max(max(c) for c in mp.METAHUMAN_LINES.values()) + 1
    n = max(n, max(v for _, v, _ in mp.GUIDES) + 1)
    p = np.zeros((n, 3))
    p[:, 0] = np.arange(n) / 1000.0
    return p


class Tables(unittest.TestCase):
    def test_guides_are_the_ones_topotransfer_knows(self):
        with open(PRESETS, encoding="utf-8") as f:
            text = f.read()
        block = text[text.index("METAHUMAN_FACE_VERTEX"):]
        block = block[:block.index("};")]
        known = {m.group(1): int(m.group(2)) for m in re.finditer(r"'([^']+)':\s*(\d+)", block)}
        self.assertEqual({label: v for label, v, _ in mp.GUIDES}, known)

    def test_every_line_has_a_metahuman_chain(self):
        self.assertEqual({k for k, _, _ in mp.LINES}, set(mp.METAHUMAN_LINES))
        for chain in mp.METAHUMAN_LINES.values():
            self.assertEqual(len(chain), len(set(chain)))

    def test_lips_run_mouth_corner_to_mouth_corner(self):
        by_label = {label: v for label, v, _ in mp.GUIDES}
        for key in mp.LIP_LINES:
            self.assertEqual(mp.METAHUMAN_LINES[key][0], by_label["Mouth corner R"])
            self.assertEqual(mp.METAHUMAN_LINES[key][-1], by_label["Mouth corner L"])

    def test_every_guide_says_where_to_click(self):
        for label, _, _ in mp.GUIDES:
            self.assertTrue(mp.guide_hint(label), label)


class Store(unittest.TestCase):
    def test_round_trip_and_missing_file(self):
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "sub", "points.json")
            self.assertEqual(mp.load(path)["guides"], {})
            points = mp.empty("Head", 10)
            points["guides"]["Nose tip"] = {"vertex": 3, "position": [1, 2, 3]}
            mp.save(points, path)
            again = mp.load(path)
            self.assertEqual(again["guides"]["Nose tip"]["vertex"], 3)
            self.assertEqual(again["mesh"], "Head")

    def test_broken_file_is_nothing_picked(self):
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "points.json")
            with open(path, "w") as f:
                f.write("{nope")
            self.assertEqual(mp.load(path)["lines"], {})

    def test_points_of_other_topology_are_stale(self):
        points = mp.empty("Head", 10)
        self.assertIsNone(mp.stale(points, "Head", 99))  # nothing picked yet
        points["guides"]["Chin"] = {"vertex": 1, "position": [0, 0, 0]}
        self.assertIsNone(mp.stale(points, "Head", 10))
        self.assertIn("99", mp.stale(points, "Other", 99))

    def test_summary(self):
        points = mp.empty()
        points["guides"]["Chin"] = {}
        text = mp.summary(points, {"upper_lip": ["a"], "lower_lip": []}, ["eye"], [])
        self.assertEqual(text, f"1 of {len(mp.GUIDES)} points, 0 of {len(mp.LINES)} lines, 1 regions, eyes")


class Lines(unittest.TestCase):
    def test_edges_in_path_order_whatever_the_selection_order(self):
        self.assertIn(mp.chain_from_edges([(7, 2), (1, 2), (9, 1)]), ([7, 2, 1, 9], [9, 1, 2, 7]))

    def test_messages_say_what_to_fix(self):
        for edges, word in (([], "no edges"), ([(0, 1), (1, 2), (2, 0)], "closed loop"),
                            ([(0, 1), (0, 2), (0, 3)], "branch"), ([(0, 1), (2, 3)], "separate")):
            with self.assertRaisesRegex(ValueError, word):
                mp.chain_from_edges(edges)

    def test_a_closed_loop_splits_at_its_corners(self):
        # a diamond: left corner 0, top 1, right corner 2, bottom 3, plus a point more on top
        p = [[-2, 0, 0], [-1, 1, 0], [2, 0, 0], [0, -1, 0], [1, 1, 0]]
        edges = [(0, 1), (1, 4), (4, 2), (2, 3), (3, 0)]
        self.assertTrue(mp.is_ring(edges))
        self.assertFalse(mp.is_ring(edges[:-1]))
        upper, lower = mp.split_ring(mp.ring_from_edges(edges), p)
        self.assertEqual(upper, [0, 1, 4, 2])
        self.assertEqual(lower, [0, 3, 2])
        self.assertEqual(mp.split_ring(mp.ring_from_edges(list(reversed(edges))), p), (upper, lower))

    def test_two_loops_are_not_one_ring(self):
        self.assertFalse(mp.is_ring([(0, 1), (1, 2), (2, 0), (3, 4), (4, 5), (5, 3)]))

    def test_an_eyelid_line_on_the_wrong_side_says_so(self):
        p = [[-3, 0, 0], [-2, 0, 0], [2, 0, 0], [3, 0, 0]]
        self.assertIsNone(mp.line_side_problem("upper_lid_L", [2, 3], p, 0.0))
        self.assertIn("right eye", mp.line_side_problem("upper_lid_L", [0, 1], p, 0.0))
        self.assertIn("left eye", mp.line_side_problem("lower_lid_R", [2, 3], p, 0.0))
        self.assertIsNone(mp.line_side_problem("upper_lip", [0, 3], p, 0.0))

    def test_opening_is_where_two_lines_really_part(self):
        self.assertEqual(mp.opening_of([1, 2, 3, 4, 6, 7], [1, 2, 9, 6, 7]), ([2, 3, 4, 6], [2, 9, 6]))
        self.assertEqual(mp.opening_of([1, 2, 3], [1, 9, 3]), ([1, 2, 3], [1, 9, 3]))

    def test_the_metahuman_mouth_opens_short_of_its_corners_and_each_eye_to_its_corners(self):
        up, low = mp.opening_of(mp.METAHUMAN_LINES["upper_lip"], mp.METAHUMAN_LINES["lower_lip"])
        self.assertLess(len(up), len(mp.METAHUMAN_LINES["upper_lip"]))
        self.assertEqual((up[0], up[-1]), (low[0], low[-1]))
        self.assertEqual(set(up[1:-1]) & set(low[1:-1]), set())
        lid = mp.opening_of(mp.METAHUMAN_LINES["upper_lid_L"], mp.METAHUMAN_LINES["lower_lid_L"])
        self.assertEqual(lid[0], mp.METAHUMAN_LINES["upper_lid_L"])

    def test_oriented_by_rising_x(self):
        p = [[5, 0, 0], [1, 0, 0], [3, 0, 0]]
        self.assertEqual(mp.oriented([0, 2, 1], p), [1, 2, 0])
        self.assertEqual(mp.oriented([1, 2, 0], p), [1, 2, 0])

    def test_arc_length_match_of_lines_with_different_vertex_counts(self):
        base = [[x, 0, 0] for x in np.linspace(0, 1, 11)]
        custom = [[0, 5, 0], [10, 5, 0]]
        matched = mp.match_line(base, custom)
        self.assertEqual(len(matched), 11)
        self.assertAlmostEqual(matched[3][0], 3.0)
        self.assertEqual(matched[0], (0.0, 5.0, 0.0))
        self.assertEqual(matched[-1], (10.0, 5.0, 0.0))

    def test_midline_keeps_the_middles_together_when_one_side_is_longer(self):
        base = [[x, 0, 0] for x in np.linspace(-1, 1, 21)]
        custom = [[x, 0, 0] for x in np.linspace(-1, 3, 41)]  # the X > 0 side is three times as long
        plain = mp.match_line(base, custom)
        anchored = mp.match_line(base, custom, 0.0, 0.0)
        self.assertAlmostEqual(plain[10][0], 1.0)
        self.assertAlmostEqual(anchored[10][0], 0.0)
        self.assertAlmostEqual(anchored[0][0], -1.0)
        self.assertAlmostEqual(anchored[-1][0], 3.0)

    def test_a_line_that_misses_its_midline_falls_back_to_arc_length(self):
        base = [[x, 0, 0] for x in np.linspace(-1, 1, 5)]
        custom = [[x, 0, 0] for x in np.linspace(2, 4, 5)]
        self.assertAlmostEqual(mp.match_line(base, custom, 0.0, 0.0)[2][0], 3.0)

    def test_pairs_keep_both_ends_and_skip_in_between(self):
        base = fake_base()
        custom = [[0, 0, 0], [1, 0, 0]]
        chain = mp.METAHUMAN_LINES["upper_lid_L"]
        pairs = mp.line_pairs("upper_lid_L", custom, base)
        self.assertEqual(pairs[0][0], chain[0])
        self.assertEqual(pairs[-1][0], chain[-1])
        self.assertLess(len(pairs), len(chain))


class Alignment(unittest.TestCase):
    def test_similarity_recovers_a_known_transform(self):
        a = np.random.default_rng(1).normal(size=(12, 3))
        angle = 0.4
        r = np.array([[np.cos(angle), 0, np.sin(angle)], [0, 1, 0], [-np.sin(angle), 0, np.cos(angle)]])
        b = 2.5 * a @ r.T + [1, 2, 3]
        scale, rot, t = mp.fit_similarity(a, b)
        self.assertAlmostEqual(scale, 2.5)
        np.testing.assert_allclose(rot, r, atol=1e-9)
        np.testing.assert_allclose(t, [1, 2, 3], atol=1e-9)
        m = np.array(mp.similarity_matrix(scale, rot, t)).reshape(4, 4)
        h = np.c_[a, np.ones(len(a))] @ m  # Maya: row vector times matrix
        np.testing.assert_allclose(h[:, :3], b, atol=1e-9)

    def test_similarity_needs_three_pairs(self):
        with self.assertRaises(ValueError):
            mp.fit_similarity([[0, 0, 0]], [[1, 1, 1]])

    def test_boxes_meet_at_the_top_and_centre(self):
        scale, move = mp.bounds_fit([-1, 0, -1], [1, 2, 1], [8, 0, 8], [12, 4, 12])
        self.assertAlmostEqual(scale, 2.0)
        np.testing.assert_allclose(move, [10, 0, 10])

    def test_midline_from_centre_guides(self):
        points = mp.empty()
        points["guides"] = {"Chin": {"position": [0.5, 0, 0]}, "Nose tip": {"position": [0.5, 1, 0]},
                            "Ear top L": {"position": [9, 0, 0]}}
        self.assertEqual(mp.midline_x(points, 7.0), 0.5)
        self.assertEqual(mp.midline_x(mp.empty(), 7.0), 7.0)

    def test_mirrored_vertex(self):
        p = [[1, 0, 0], [-1, 0, 0], [3, 0, 0]]
        self.assertEqual(mp.mirrored_vertex(p, 0, 0.0), 1)
        self.assertEqual(mp.mirrored_vertex(p, 0, 2.0), 2)


class Guides(unittest.TestCase):
    def picked(self):
        points = mp.empty("Head", 100)
        points["guides"] = {"Nose tip": {"vertex": 1, "position": [0, 5, 9]}, "Unknown": {"vertex": 2, "position": [0, 0, 0]}}
        return points

    def test_named_guides_carry_the_metahuman_vertex_and_your_position(self):
        out = mp.launch_guides(self.picked(), fake_base())
        self.assertEqual(out["landmarks"], [{"label": "Nose tip", "group": "nose", "weight": 1.0, "base_vertex": 17088, "ref": [0.0, 5.0, 9.0]}])

    def test_lines_become_light_pairs_and_a_shared_vertex_takes_the_middle(self):
        points = self.picked()
        points["lines"] = {"upper_lip": {"vertices": [0, 1], "positions": [[-3, 1, 0], [3, 1, 0]]},
                           "lower_lip": {"vertices": [2, 3], "positions": [[-3, 0, 0], [3, 0, 0]]}}
        out = mp.launch_guides(points, fake_base())
        lines = [g for g in out["landmarks"] if g["group"] == "lines"]
        self.assertTrue(lines)
        self.assertTrue(all(g["weight"] == mp.LINE_WEIGHT for g in lines))
        self.assertEqual(len({g["base_vertex"] for g in lines}), len(lines))
        corner = mp.METAHUMAN_LINES["upper_lip"][0]  # the mouth corner is on both lip lines
        self.assertEqual(corner, mp.METAHUMAN_LINES["lower_lip"][0])
        spot = next(g for g in lines if g["base_vertex"] == corner)
        self.assertAlmostEqual(spot["ref"][1], 0.5)

    def test_regions_need_both_sides(self):
        out = mp.launch_guides(mp.empty(), fake_base(), {"upper_lip": [1, 2], "lower_lip": [3]}, {"upper_lip": [7], "mouth_bag": [8]})
        self.assertEqual(out["regions"], {"upper_lip": {"base": [1, 2], "ref": [7]}})

    def test_reference_regions_follow_the_renumbering_of_the_export(self):
        self.assertEqual(mp.reference_regions({"a": [0, 1, 2]}, None), {"a": [0, 1, 2]})
        self.assertEqual(mp.reference_regions({"a": [0, 1, 2, 9]}, [0, -1, 1]), {"a": [0, 1]})

    def test_refreshed_reads_positions_again(self):
        points = mp.empty("Head", 3)
        points["guides"]["Chin"] = {"vertex": 2, "position": [0, 0, 0]}
        points["lines"]["upper_lip"] = {"vertices": [0, 1], "positions": [[0, 0, 0], [0, 0, 0]]}
        out = mp.refreshed(points, [(1, 1, 1), (2, 2, 2), (3, 3, 3)])
        self.assertEqual(out["guides"]["Chin"]["position"], [3.0, 3.0, 3.0])
        self.assertEqual(out["lines"]["upper_lip"]["positions"][1], [2.0, 2.0, 2.0])
        self.assertEqual(points["guides"]["Chin"]["position"], [0, 0, 0])


class ExportMap(unittest.TestCase):
    def test_surviving_vertices_keep_their_order(self):
        import mm_maya

        self.assertEqual(mm_maya.vertex_map([(0, 0, 0), (1, 0, 0), (2, 0, 0)], [(0, 0, 0), (2, 0, 0)]), [0, -1, 1])

    def test_a_map_that_does_not_add_up_is_an_error(self):
        import mm_maya

        with self.assertRaises(RuntimeError):
            mm_maya.vertex_map([(0, 0, 0)], [(5, 0, 0)])


if __name__ == "__main__":
    unittest.main()
