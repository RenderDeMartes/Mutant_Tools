"""
Tests for Meta Mutant's DNA side (pure Python; no Maya / DNACalib / OpenRigLogic needed).

    python -m unittest discover -s tests -v
"""

import math
import os
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))

import mm_core as core  # noqa: E402
import mm_dna  # noqa: E402


def close(a, b, tol=1e-9):
    return all(abs(x - y) <= tol for x, y in zip(a, b))


class FakeReader:
    """Minimal stand-in for dna.BinaryStreamReader (same method names)."""

    def __init__(self):
        # mesh 0: head quad (4 vertices), mesh 1: eye triangle (3 vertices)
        self.meshes = [
            {"name": "head_lod0_mesh", "pos": [(0, 0, 0), (1, 0, 0), (1, 1, 0), (0, 1, 0)], "uv": [(0, 0), (1, 0), (1, 1), (0, 1)], "faces": [[0, 1, 2, 3]]},
            {"name": "eyeLeft_lod0_mesh", "pos": [(0.2, 0.5, 0.1), (0.3, 0.5, 0.1), (0.25, 0.6, 0.1)], "uv": [(0, 0), (1, 0), (0, 1)], "faces": [[0, 1, 2]]},
        ]
        # joints: root -> head (rotated 90° about Z) -> FACIAL_C_Jaw
        self.joints = ["root", "head", "FACIAL_C_Jaw", "FACIAL_L_Eye"]
        self.parents = [0, 0, 1, 1]
        self.t = [(0, 0, 0), (0, 1, 0), (0.5, 0, 0), (0.5, -0.2, 0.1)]
        self.r = [(0, 0, 0), (0, 0, 90), (0, 0, 0), (0, 0, 0)]
        # skin: head quad influenced by jaw (verts 0,1) and head (2,3); eye by FACIAL_L_Eye only
        self.skin = {0: [[(2, 1.0)], [(2, 0.5), (1, 0.5)], [(1, 1.0)], [(1, 1.0)]], 1: [[(3, 1.0)]] * 3}

    # meshes
    def getMeshIndicesForLOD(self, lod):
        return [0, 1]

    def getMeshName(self, m):
        return self.meshes[m]["name"]

    def getVertexPositionXs(self, m):
        return [p[0] for p in self.meshes[m]["pos"]]

    def getVertexPositionYs(self, m):
        return [p[1] for p in self.meshes[m]["pos"]]

    def getVertexPositionZs(self, m):
        return [p[2] for p in self.meshes[m]["pos"]]

    def getVertexTextureCoordinateUs(self, m):
        return [u for u, _ in self.meshes[m]["uv"]]

    def getVertexTextureCoordinateVs(self, m):
        return [v for _, v in self.meshes[m]["uv"]]

    def getVertexLayoutPositionIndices(self, m):
        return list(range(len(self.meshes[m]["pos"])))

    def getVertexLayoutTextureCoordinateIndices(self, m):
        return list(range(len(self.meshes[m]["uv"])))

    def getFaceCount(self, m):
        return len(self.meshes[m]["faces"])

    def getFaceVertexLayoutIndices(self, m, f):
        return self.meshes[m]["faces"][f]

    # joints
    def getJointCount(self):
        return len(self.joints)

    def getJointName(self, j):
        return self.joints[j]

    def getJointParentIndex(self, j):
        return self.parents[j]

    def getNeutralJointTranslationXs(self):
        return [t[0] for t in self.t]

    def getNeutralJointTranslationYs(self):
        return [t[1] for t in self.t]

    def getNeutralJointTranslationZs(self):
        return [t[2] for t in self.t]

    def getNeutralJointRotationXs(self):
        return [r[0] for r in self.r]

    def getNeutralJointRotationYs(self):
        return [r[1] for r in self.r]

    def getNeutralJointRotationZs(self):
        return [r[2] for r in self.r]

    # skin
    def getSkinWeightsCount(self, m):
        return len(self.skin.get(m, []))

    def getSkinWeightsJointIndices(self, m, v):
        return [j for j, _ in self.skin[m][v]]

    def getSkinWeightsValues(self, m, v):
        return [w for _, w in self.skin[m][v]]


class FakeDnac:
    """Records DNACalib commands instead of executing them."""

    VectorOperation_Add = "add"
    log = []

    class DNACalibDNAReader:
        def __init__(self, r):
            self.r = r

    class _Cmd:
        def __init__(self, kind, *args):
            self.kind, self.args = kind, args

        def run(self, target):
            FakeDnac.log.append((self.kind,) + self.args)

    @staticmethod
    def SetVertexPositionsCommand(mesh, positions, op):
        return FakeDnac._Cmd("positions", mesh, positions, op)

    @staticmethod
    def SetNeutralJointTranslationsCommand(translations):
        return FakeDnac._Cmd("joints", translations)

    @staticmethod
    def CalculateMeshLowerLODsCommand(mesh):
        return FakeDnac._Cmd("lods", mesh)


class FakeWriter:
    """Stand-in for dna.BinaryStreamWriter: records every call in order."""

    def __init__(self, stream):
        self.stream = stream
        self.calls = []

    def setFrom(self, reader):
        self.calls.append(("setFrom", reader))

    def setVertexPositions(self, mesh, positions):
        self.calls.append(("setVertexPositions", mesh, positions))

    def setNeutralJointTranslations(self, translations):
        self.calls.append(("setNeutralJointTranslations", translations))

    def write(self):
        self.calls.append(("write",))


class FakeDna:
    """Stand-in for OpenRigLogic's `dna` module (only what mm_dna's writer backend touches)."""

    writers = []

    class FileStream:
        AccessMode_Write = "write"
        OpenMode_Binary = "binary"

        def __init__(self, path, access, mode):
            self.path, self.access, self.mode = path, access, mode

    @staticmethod
    def BinaryStreamWriter(stream):
        w = FakeWriter(stream)
        FakeDna.writers.append(w)
        return w

    class Status:
        @staticmethod
        def isOk():
            return True


def write_wrapped(tmp, r):
    """Export `r`, then fake a TopoTransfer result: DNA-space +0.5 z on every vertex, saved in
    reference space with an alignment header. Returns (manifest, wrapped obj)."""
    obj = os.path.join(tmp, "mh.obj")
    manifest = mm_dna.export_obj("fake.dna", obj, reader=r)
    exported = core.read_obj_positions(obj)
    align = [2, 0, 0, 0, 0, 2, 0, 0, 0, 0, 2, 0, 10, 0, 0, 1]  # scale 2, offset x 10
    wrapped = os.path.join(tmp, "wrapped.obj")
    with open(wrapped, "w") as f:
        f.write("# Exported by TopoTransfer\n# space: reference coordinates\n")
        f.write("# topotransfer-alignment base_to_reference column_major " + " ".join(str(v) for v in align) + "\n")
        for p in exported.positions:
            q = core.mat4_apply(align, (p[0], p[1], p[2] + 0.5))
            f.write(f"v {q[0]} {q[1]} {q[2]}\n")
    return manifest, wrapped


class TestMath(unittest.TestCase):
    def test_euler_xyz(self):
        Rz = core.euler_xyz_deg(0, 0, 90)
        self.assertTrue(close(core._mv(Rz, (1, 0, 0)), (0, 1, 0), 1e-12))
        R = core.euler_xyz_deg(30, -40, 70)
        # orthonormal
        for i in range(3):
            for j in range(3):
                d = sum(R[k][i] * R[k][j] for k in range(3))
                self.assertAlmostEqual(d, 1.0 if i == j else 0.0, places=12)
        # XYZ order: x applied first
        Rx, Ry, Rz2 = core.euler_xyz_deg(30, 0, 0), core.euler_xyz_deg(0, -40, 0), core.euler_xyz_deg(0, 0, 70)
        composed = core._mm(Rz2, core._mm(Ry, Rx))
        for i in range(3):
            self.assertTrue(close(R[i], composed[i], 1e-12))

    def test_joint_world_and_local_moves(self):
        r = FakeReader()
        sk = core.skeleton_from_reader(r)
        world, rot = core.joint_world(sk)
        self.assertTrue(close(world[1], (0, 1, 0)))
        # head rotated 90° about Z: child local +X becomes world +Y
        self.assertTrue(close(world[2], (0, 1.5, 0), 1e-12))
        # move the jaw by d in world; eye (sibling) must not move
        d = {2: (0.1, -0.2, 0.3)}
        new_t = core.local_translations_after_move(sk, rot, d)
        moved = core.Skeleton(sk.names, sk.parents, new_t, sk.rotations)
        w2, _ = core.joint_world(moved)
        self.assertTrue(close(w2[2], (0.1, 1.3, 0.3), 1e-12))
        self.assertTrue(close(w2[3], world[3], 1e-12))
        # moving a parent keeps unmoved children in place
        new_t = core.local_translations_after_move(sk, rot, {1: (1, 2, 3)})
        w3, _ = core.joint_world(core.Skeleton(sk.names, sk.parents, new_t, sk.rotations))
        self.assertTrue(close(w3[1], (1, 3, 3), 1e-12))
        self.assertTrue(close(w3[2], world[2], 1e-12))

    def test_joint_deltas(self):
        skin = {0: [[(0, 1.0)], [(0, 0.5), (1, 0.5)], [(1, 1.0)]]}
        deltas = {0: [(1, 0, 0), (0, 1, 0), (0, 0, 1)]}
        out, w = core.skin_weighted_joint_deltas(3, skin, deltas)
        self.assertTrue(close(out[0], (1 / 1.5, 0.5 / 1.5, 0)))
        self.assertTrue(close(out[1], (0, 0.5 / 1.5, 1 / 1.5)))
        self.assertNotIn(2, out)
        near = core.nearest_vertex_deltas({5: (0, 0, 0)}, [(0, 0, 0), (10, 0, 0)], [(1, 2, 3), (9, 9, 9)], k=1)
        self.assertTrue(close(near[5], (1, 2, 3)))

    def test_alignment_inverse(self):
        a = math.radians(30)
        s = 1.7
        m = [s * math.cos(a), s * math.sin(a), 0, 0, -s * math.sin(a), s * math.cos(a), 0, 0, 0, 0, s, 0, 3, -2, 5, 1]
        inv = core.mat4_inverse(m)
        p = (0.3, -1.2, 4.0)
        self.assertTrue(close(core.mat4_apply(inv, core.mat4_apply(m, p)), p, 1e-12))


class TestPipeline(unittest.TestCase):
    def test_export_wrap_calibrate(self):
        r = FakeReader()
        with tempfile.TemporaryDirectory() as tmp:
            # simulate TopoTransfer: result exported in *reference* space with an alignment header;
            # true DNA-space result = original + (0, 0, 0.5) on the head, eye follows rigidly (+0.5 z)
            manifest, wrapped = write_wrapped(tmp, r)
            blocks = core.read_manifest(manifest)
            self.assertEqual([(b.name, b.vertex_count, b.offset) for b in blocks], [("head_lod0_mesh", 4, 0), ("eyeLeft_lod0_mesh", 3, 4)])
            exported = core.read_obj_positions(os.path.join(tmp, "mh.obj"))
            self.assertEqual(len(exported.positions), 7)
            FakeDnac.log = []
            report = mm_dna.calibrate("fake.dna", manifest, wrapped, "", reader=r, dnac_module=FakeDnac)
            pos_cmds = [c for c in FakeDnac.log if c[0] == "positions"]
            self.assertEqual(len(pos_cmds), 2)
            for _, mesh, deltas, op in pos_cmds:
                self.assertEqual(op, "add")
                for d in deltas:
                    self.assertTrue(close(d, (0, 0, 0.5), 1e-9))
            joints = [c for c in FakeDnac.log if c[0] == "joints"][0][1]
            sk = core.skeleton_from_reader(r)
            new = core.Skeleton(sk.names, sk.parents, [tuple(t) for t in joints], sk.rotations)
            w_old, _ = core.joint_world(sk)
            w_new, _ = core.joint_world(new)
            # facial joints moved with their skin (+0.5 z); root and head untouched (default filter = FACIAL_*)
            for j, name in enumerate(sk.names):
                expect = (0, 0, 0.5) if name.startswith("FACIAL_") else (0, 0, 0)
                got = tuple(w_new[j][k] - w_old[j][k] for k in range(3))
                self.assertTrue(close(got, expect, 1e-9), f"{name}: {got}")
            self.assertTrue(any("lower LODs" in line for line in report))

    def test_writer_backend_matches_dnacalib(self):
        r = FakeReader()
        with tempfile.TemporaryDirectory() as tmp:
            manifest, wrapped = write_wrapped(tmp, r)
            FakeDnac.log = []
            calib_report = mm_dna.calibrate("fake.dna", manifest, wrapped, "", reader=r, dnac_module=FakeDnac, backend="dnacalib")
            FakeDna.writers = []
            report = mm_dna.calibrate("fake.dna", manifest, wrapped, "out.dna", reader=r, backend="writer", dna_module=FakeDna)
        self.assertIn("backend: DNACalib", calib_report)
        self.assertIn("backend: OpenRigLogic dna.BinaryStreamWriter", report)
        self.assertEqual(len(FakeDna.writers), 1)
        w = FakeDna.writers[0]
        self.assertEqual((w.stream.path, w.stream.access, w.stream.mode), ("out.dna", "write", "binary"))
        kinds = [c[0] for c in w.calls]
        # copy first, then overwrite LOD0 meshes and joints, write last
        self.assertEqual(kinds, ["setFrom", "setVertexPositions", "setVertexPositions", "setNeutralJointTranslations", "write"])
        self.assertIs(w.calls[0][1], r)

        # positions: writer gets absolute old + delta, DNACalib gets the delta with VectorOperation_Add
        dnac_pos = {c[1]: c[2] for c in FakeDnac.log if c[0] == "positions"}
        writer_pos = {c[1]: c[2] for c in w.calls if c[0] == "setVertexPositions"}
        self.assertEqual(sorted(writer_pos), sorted(dnac_pos))
        for mesh, deltas in dnac_pos.items():
            old = core.read_mesh_positions(r, mesh)
            self.assertEqual(len(writer_pos[mesh]), len(old))
            for o, d, p in zip(old, deltas, writer_pos[mesh]):
                self.assertTrue(close(p, (o[0] + d[0], o[1] + d[1], o[2] + d[2]), 1e-12))
                self.assertTrue(close(p, (o[0], o[1], o[2] + 0.5), 1e-9))

        # joints: identical full translation list
        dnac_joints = [c for c in FakeDnac.log if c[0] == "joints"][0][1]
        writer_joints = [c for c in w.calls if c[0] == "setNeutralJointTranslations"][0][1]
        self.assertEqual(len(writer_joints), r.getJointCount())
        for a, b in zip(dnac_joints, writer_joints):
            self.assertTrue(close(a, b, 0))

        self.assertTrue(any("lower LODs are unchanged" in line for line in report))
        self.assertIn("written out.dna", report)

    def test_writer_backend_dry_run_writes_nothing(self):
        r = FakeReader()
        with tempfile.TemporaryDirectory() as tmp:
            manifest, wrapped = write_wrapped(tmp, r)
            FakeDna.writers = []
            report = mm_dna.calibrate("fake.dna", manifest, wrapped, "", reader=r, backend="writer", dna_module=FakeDna)
        self.assertEqual(FakeDna.writers, [])
        self.assertFalse(any(line.startswith("written") for line in report))

    def test_backend_selection(self):
        orig = mm_dna._dnacalib_module
        try:
            mm_dna._dnacalib_module = lambda: None
            self.assertEqual(mm_dna.resolve_backend("auto"), ("writer", None))
            self.assertEqual(mm_dna.resolve_backend("auto", FakeDnac), ("dnacalib", FakeDnac))
            with self.assertRaises(SystemExit):
                mm_dna.resolve_backend("dnacalib")
            mm_dna._dnacalib_module = lambda: FakeDnac
            self.assertEqual(mm_dna.resolve_backend("auto"), ("dnacalib", FakeDnac))
            self.assertEqual(mm_dna.resolve_backend("writer"), ("writer", None))
            with self.assertRaises(ValueError):
                mm_dna.resolve_backend("bogus")
        finally:
            mm_dna._dnacalib_module = orig

    def test_vertex_count_mismatch_is_reported(self):
        r = FakeReader()
        with tempfile.TemporaryDirectory() as tmp:
            obj = os.path.join(tmp, "mh.obj")
            manifest = mm_dna.export_obj("fake.dna", obj, reader=r)
            bad = os.path.join(tmp, "bad.obj")
            with open(bad, "w") as f:
                f.write("v 0 0 0\n")
            with self.assertRaises(ValueError) as ctx:
                mm_dna.calibrate("fake.dna", manifest, bad, "", reader=r, dnac_module=FakeDnac)
            self.assertIn("expects 7", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()
