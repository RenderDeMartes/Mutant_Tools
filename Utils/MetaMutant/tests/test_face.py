"""mm_face: the RigLogic steps on a tiny hand-made behaviour (no DNA, no Maya)."""

import os
import sys
import unittest

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import mm_face  # noqa: E402


def behaviour():
    # GUI 0 (a -1..1 slider) -> raw 0 on its positive half, raw 1 on its negative half; GUI 1 -> raw 2
    # PSD 3 = 0.5 * raw0 * raw2; joint 0: tx from raw0 (2 cm), rx from PSD 3 (90 degrees); shape 0 = raw 1
    return {
        "gui_names": np.array(["CTRL_C_a.ty", "CTRL_C_b.ty"]),
        "joint_names": np.array(["j0"]),
        "channel_names": np.array(["s0"]),
        "raw_count": np.int32(3), "psd_count": np.int32(1),
        "gui_in": np.array([0, 0, 1], np.int32), "gui_out": np.array([0, 1, 2], np.int32),
        "gui_from": np.array([0, -1, 0], np.float32), "gui_to": np.array([1, 0, 1], np.float32),
        "gui_slope": np.array([1, -1, 2], np.float32), "gui_cut": np.array([0, 0, 0], np.float32),
        "psd_rows": np.array([3, 3], np.int32), "psd_cols": np.array([0, 2], np.int32),
        "psd_values": np.array([0.5, 1.0], np.float32),
        "joint_out": np.array([0, 3], np.int32), "joint_in": np.array([0, 3], np.int32),
        "joint_val": np.array([2.0, 90.0], np.float32), "joint_offsets": np.array([0, 1, 2], np.int64),
        "joint_count": np.int32(1), "neutral_t": np.array([[1.0, 2.0, 3.0]], np.float32),
        "shape_in": np.array([1], np.int32), "shape_out": np.array([0], np.int32),
    }


class TestFace(unittest.TestCase):
    def test_neutral_is_the_rest_pose(self):
        joints, shapes = mm_face.evaluate(behaviour(), [0, 0])
        np.testing.assert_allclose(joints, [1, 2, 3, 0, 0, 0, 1, 1, 1])
        self.assertEqual(shapes.tolist(), [0])

    def test_ranges_clamp_and_correctives(self):
        b = behaviour()
        c = mm_face.controls(b, np.array([0.8, 0.9], np.float32))
        np.testing.assert_allclose(c, [0.8, 0, 1.0, 0.5 * 0.8 * 1.0], rtol=1e-6)  # raw 2 = 1.8 clamped to 1
        joints, _ = mm_face.evaluate(b, [0.8, 0.9])
        self.assertAlmostEqual(float(joints[0]), 1 + 2 * 0.8, places=5)
        self.assertAlmostEqual(float(joints[3]), 90 * 0.4, places=4)

    def test_negative_half_drives_the_other_raw_control_and_shape(self):
        _, shapes = mm_face.evaluate(behaviour(), [-0.5, 0])
        self.assertAlmostEqual(float(shapes[0]), 0.5, places=6)


if __name__ == "__main__":
    unittest.main()
