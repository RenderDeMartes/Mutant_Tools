"""
Meta Mutant face board math: what RigLogic does, from the DNA's behaviour data, in numpy.
No Epic plugin: the face board's controls feed `evaluate`, which gives the joint changes and
blendshape weights (same steps as OpenRigLogic, MIT):

1. GUI controls -> raw controls: range table (from <= value <= to: slope * value + cut; the first
   matching range of each input/output pair counts), clamped to 0..1
2. PSD correctives: weight * product of their (0..1 clamped) inputs, at most 1
3. joints: per joint group, LOD0 rows x inputs weights; output index = joint * 9 + attribute
   (tx ty tz rx ry rz sx sy sz; cm and degrees), added to the neutral joint
4. blendshape channels: weight[output] = control[input]

    beh = export_behaviour(reader, "face_behaviour.npz")   # once, from the DNA (needs the dna module)
    beh = load_behaviour("face_behaviour.npz")             # anywhere numpy is
    joints, shapes = evaluate(beh, gui_values)
"""

from __future__ import annotations

from typing import Dict, Tuple

import numpy as np

ATTRS = ("tx", "ty", "tz", "rx", "ry", "rz", "sx", "sy", "sz")


def export_behaviour(r, path: str = "") -> Dict[str, np.ndarray]:
    """Everything `evaluate` needs from a DNA reader (LOD0), optionally saved as .npz."""
    gui_in = np.array(r.getGUIToRawInputIndices(), dtype=np.int32)
    gui_out = np.array(r.getGUIToRawOutputIndices(), dtype=np.int32)
    lo = np.array(r.getGUIToRawFromValues(), dtype=np.float32)
    hi = np.array(r.getGUIToRawToValues(), dtype=np.float32)
    lo, hi = np.minimum(lo, hi), np.maximum(lo, hi)  # DNAs may store them reversed
    groups_in, groups_out, groups_val, offsets = [], [], [], [0]
    for g in range(r.getJointGroupCount()):
        cols = np.array(r.getJointGroupInputIndices(g), dtype=np.int32)
        rows = int((list(r.getJointGroupLODs(g)) or [0])[0])
        out = np.array(r.getJointGroupOutputIndices(g), dtype=np.int32)[:rows]
        vals = np.array(r.getJointGroupValues(g), dtype=np.float32)
        vals = vals.reshape(-1, len(cols))[:rows] if len(cols) else np.zeros((0, 0), np.float32)
        # flattened: each row's weights against its group's inputs
        for row in range(rows):
            groups_out.append(out[row])
            groups_in.append(cols)
            groups_val.append(vals[row])
            offsets.append(offsets[-1] + len(cols))
    n = r.getJointCount()
    beh = {
        "gui_names": np.array([r.getGUIControlName(i) for i in range(r.getGUIControlCount())]),
        "joint_names": np.array([r.getJointName(i) for i in range(n)]),
        "channel_names": np.array([r.getBlendShapeChannelName(i) for i in range(r.getBlendShapeChannelCount())]),
        "raw_count": np.int32(r.getRawControlCount()),
        "psd_count": np.int32(r.getPSDCount()),
        "gui_in": gui_in, "gui_out": gui_out, "gui_from": lo, "gui_to": hi,
        "gui_slope": np.array(r.getGUIToRawSlopeValues(), dtype=np.float32),
        "gui_cut": np.array(r.getGUIToRawCutValues(), dtype=np.float32),
        "psd_rows": np.array(r.getPSDRowIndices(), dtype=np.int32),
        "psd_cols": np.array(r.getPSDColumnIndices(), dtype=np.int32),
        "psd_values": np.array(r.getPSDValues(), dtype=np.float32),
        "joint_out": np.array(groups_out, dtype=np.int32),
        "joint_in": np.concatenate(groups_in) if groups_in else np.zeros(0, np.int32),
        "joint_val": np.concatenate(groups_val) if groups_val else np.zeros(0, np.float32),
        "joint_offsets": np.array(offsets, dtype=np.int64),
        "joint_count": np.int32(n),
        "neutral_t": np.stack([np.array(r.getNeutralJointTranslationXs()), np.array(r.getNeutralJointTranslationYs()),
                               np.array(r.getNeutralJointTranslationZs())], axis=1).astype(np.float32),
        "shape_in": np.array(r.getBlendShapeChannelInputIndices(), dtype=np.int32)[: int(list(r.getBlendShapeChannelLODs())[0])],
        "shape_out": np.array(r.getBlendShapeChannelOutputIndices(), dtype=np.int32)[: int(list(r.getBlendShapeChannelLODs())[0])],
    }
    if path:
        np.savez_compressed(path, **beh)
    return beh


def load_behaviour(path: str) -> Dict[str, np.ndarray]:
    with np.load(path, allow_pickle=False) as f:
        return {k: f[k] for k in f.files}


def controls(beh, gui: np.ndarray) -> np.ndarray:
    """GUI values -> raw + PSD control values (steps 1 and 2)."""
    raw_n, psd_n = int(beh["raw_count"]), int(beh["psd_count"])
    out = np.zeros(raw_n + psd_n, dtype=np.float32)
    done = set()  # (input, output) pairs that already matched a range
    for i, o, lo, hi, s, c in zip(beh["gui_in"], beh["gui_out"], beh["gui_from"], beh["gui_to"], beh["gui_slope"], beh["gui_cut"]):
        v = gui[i]
        if (i, o) not in done and lo <= v <= hi:
            out[o] += s * v + c
            done.add((i, o))
    out[:raw_n] = np.clip(out[:raw_n], 0.0, 1.0)
    clamped = np.clip(out, 0.0, 1.0)
    psd = np.ones(psd_n, dtype=np.float32)
    rows = beh["psd_rows"] - raw_n
    np.multiply.at(psd, rows, beh["psd_values"] * clamped[beh["psd_cols"]])
    used = np.zeros(psd_n, dtype=bool)
    used[rows] = True
    out[raw_n:] = np.where(used, np.minimum(1.0, psd), 0.0)
    return out


def evaluate(beh, gui) -> Tuple[np.ndarray, np.ndarray]:
    """GUI values -> (joint attribute values, joint * 9 + attribute, absolute; blendshape weights)."""
    c = controls(beh, np.asarray(gui, dtype=np.float32))
    contrib = beh["joint_val"] * c[beh["joint_in"]]
    sums = np.add.reduceat(contrib, beh["joint_offsets"][:-1]) if len(contrib) else np.zeros(0, np.float32)
    sums[np.diff(beh["joint_offsets"]) == 0] = 0.0
    n = int(beh["joint_count"])
    delta = np.zeros(n * 9, dtype=np.float32)
    np.add.at(delta, beh["joint_out"], sums)
    absolute = delta.reshape(n, 9)
    absolute[:, 0:3] += beh["neutral_t"]  # rotations stay deltas: the neutral rotation is the jointOrient
    absolute[:, 6:9] += 1.0
    shapes = np.zeros(len(beh["channel_names"]), dtype=np.float32)
    shapes[beh["shape_out"]] = c[beh["shape_in"]]
    return absolute.reshape(-1), shapes


def animated(beh) -> np.ndarray:
    """Joint attribute indices any control can move (the ones to connect)."""
    return np.unique(beh["joint_out"])
