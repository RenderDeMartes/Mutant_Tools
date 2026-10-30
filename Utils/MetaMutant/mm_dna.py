"""
DNA side of the MetaHuman <-> TopoTransfer pipeline.

Needs Epic's `dna` Python module. Either source works:
  * OpenRigLogic (MIT): https://github.com/EpicGames/OpenRigLogic — DNA read/write
    library + RigLogic, built from source with its Python wrapper. Enough for both
    commands below (calibration goes through `dna.BinaryStreamWriter`).
  * MetaHuman-DNA-Calibration: https://github.com/EpicGames/MetaHuman-DNA-Calibration
    — ships `dna` and `dnacalib` prebuilt. When `dnacalib` is importable it is used
    for calibration (adds lower-LOD recalculation).

Two commands (run with `mayapy` or any Python that can import `dna`, e.g. after
adding the folders with the Python modules to PYTHONPATH / sys.path):

  export     DNA  ->  combined LOD0 OBJ (+ manifest) to use as TopoTransfer Base
  calibrate  DNA + wrapped OBJ from TopoTransfer  ->  calibrated DNA
             (new neutral meshes, facial joints moved with the skin they drive,
              blendshape deltas kept, lower LODs recomputed with DNACalib only)

    python mm_dna.py export    head.dna  out/mh_head_lod0.obj
    python mm_dna.py calibrate head.dna  out/mh_head_lod0.manifest.json  wrapped.obj  head_custom.dna [--backend auto|dnacalib|writer]
"""

from __future__ import annotations

import argparse
import os
import sys
from typing import Callable, List, Optional, Sequence

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mm_core as core  # noqa: E402

#: LOD0 meshes exported by default (substring match on DNA mesh names)
DEFAULT_MESHES = ("head", "teeth", "saliva", "eyeLeft", "eyeRight", "eyeshell", "eyelashes", "eyeEdge", "cartilage")

#: calibration backends: "auto" = DNACalib if importable, else the OpenRigLogic writer
BACKENDS = ("auto", "dnacalib", "writer")


def _dna_module():
    try:
        import dna  # type: ignore
    except ImportError as e:  # pragma: no cover - environment specific
        raise SystemExit(
            "Could not import Epic's 'dna' module. Build OpenRigLogic with its Python wrapper (or use "
            "MetaHuman-DNA-Calibration's lib folders) and add it to sys.path (see the Meta Mutant README.md). Original error: %s" % e
        )
    return dna


def _dnacalib_module():
    """Epic's DNACalib module, or None when it is not installed."""
    try:
        import dnacalib  # type: ignore
    except ImportError:
        return None
    return dnacalib


def load_dna(path: str, dna_module=None):
    dna = dna_module or _dna_module()
    stream = dna.FileStream(path, dna.FileStream.AccessMode_Read, dna.FileStream.OpenMode_Binary)
    reader = dna.BinaryStreamReader(stream, dna.DataLayer_All)
    reader.read()
    if not dna.Status.isOk():
        raise RuntimeError(f"Error loading DNA {path}: {dna.Status.get().message}")
    return reader


def save_dna(reader, path: str, dna_module=None, edit: Optional[Callable] = None) -> None:
    """Copy `reader` into a `dna.BinaryStreamWriter` (setFrom), let `edit(writer)` overwrite parts, write to `path`."""
    dna = dna_module or _dna_module()
    stream = dna.FileStream(path, dna.FileStream.AccessMode_Write, dna.FileStream.OpenMode_Binary)
    writer = dna.BinaryStreamWriter(stream)
    writer.setFrom(reader)
    if edit is not None:
        edit(writer)
    writer.write()
    if not dna.Status.isOk():
        raise RuntimeError(f"Error saving DNA {path}: {dna.Status.get().message}")


def mesh_indices_for_lod(r, lod: int, include: Sequence[str]) -> List[int]:
    idx = list(r.getMeshIndicesForLOD(lod))
    return [m for m in idx if any(key.lower() in r.getMeshName(m).lower() for key in include)]


def mesh_geometry(r, m: int) -> dict:
    """Positions (unique vertices, DNA order), UVs and faces of DNA mesh `m`."""
    positions = core.read_mesh_positions(r, m)
    us, vs = r.getVertexTextureCoordinateUs(m), r.getVertexTextureCoordinateVs(m)
    uvs = [(us[i], vs[i]) for i in range(len(us))]
    lp = r.getVertexLayoutPositionIndices(m)
    lt = r.getVertexLayoutTextureCoordinateIndices(m)
    faces = []
    for f in range(r.getFaceCount(m)):
        layouts = r.getFaceVertexLayoutIndices(m, f)
        faces.append([(lp[l], lt[l]) for l in layouts])
    return {"name": r.getMeshName(m), "dna_index": m, "positions": positions, "uvs": uvs, "faces": faces}


def export_obj(dna_path: str, out_obj: str, lod: int = 0, include: Sequence[str] = DEFAULT_MESHES, reader=None) -> str:
    """Write the selected LOD meshes as one OBJ (+ <name>.manifest.json). Returns the manifest path."""
    r = reader if reader is not None else load_dna(dna_path)
    meshes = [mesh_geometry(r, m) for m in mesh_indices_for_lod(r, lod, include)]
    if not meshes:
        raise RuntimeError(f"No LOD{lod} meshes matching {include} in {dna_path}")
    header = [
        f"MetaHuman LOD{lod} meshes exported from {os.path.basename(dna_path)} for TopoTransfer (DNA space, vertex order preserved)",
        "Use as the Base mesh. The head should be Fit; eyes, teeth, lashes etc. Follow.",
    ]
    blocks = core.write_obj(out_obj, meshes, header)
    manifest = os.path.splitext(out_obj)[0] + ".manifest.json"
    core.write_manifest(manifest, os.path.abspath(dna_path), lod, blocks)
    return manifest


def resolve_backend(backend: str = "auto", dnac_module=None):
    """Pick the calibration backend. Returns ("dnacalib", module) or ("writer", None)."""
    if backend not in BACKENDS:
        raise ValueError(f"unknown backend {backend!r}; expected one of {BACKENDS}")
    if backend == "writer":
        return "writer", None
    dnac = dnac_module if dnac_module is not None else _dnacalib_module()
    if dnac is not None:
        return "dnacalib", dnac
    if backend == "dnacalib":
        raise SystemExit("backend 'dnacalib' requested but Epic's 'dnacalib' module is not importable (see the Meta Mutant README.md)")
    return "writer", None


def _apply_dnacalib(dnac, r, plan: core.CalibrationPlan, update_lower_lods: bool):
    """DNACalib commands on a DNACalibDNAReader copy of `r`; returns the calibrated reader."""
    calibrated = dnac.DNACalibDNAReader(r)
    for mesh, deltas in plan.mesh_deltas.items():
        cmd = dnac.SetVertexPositionsCommand(mesh, [list(d) for d in deltas], dnac.VectorOperation_Add)
        cmd.run(calibrated)
    cmd = dnac.SetNeutralJointTranslationsCommand([list(t) for t in plan.joint_translations])
    cmd.run(calibrated)
    if update_lower_lods and hasattr(dnac, "CalculateMeshLowerLODsCommand"):
        for mesh in plan.mesh_deltas:
            try:
                dnac.CalculateMeshLowerLODsCommand(mesh).run(calibrated)
            except Exception as e:  # pragma: no cover - depends on DNA content / version
                plan.report.append(f"lower LODs for mesh {mesh} not recalculated: {e}")
        plan.report.append("lower LODs recalculated from LOD0")
    elif update_lower_lods:
        plan.report.append("this DNACalib version has no CalculateMeshLowerLODsCommand; lower LODs are unchanged")
    return calibrated


def write_plan(writer, r, plan: core.CalibrationPlan) -> None:
    """
    Overwrite a writer that already holds a copy of `r` (writer.setFrom(r)) with the plan,
    using only OpenRigLogic's dna.Writer API: absolute LOD0 positions (old + delta) per
    wrapped mesh and every neutral joint translation. Everything else (skin weights,
    blendshape deltas, lower LODs, behaviour) stays as copied.
    """
    for mesh, deltas in plan.mesh_deltas.items():
        old = core.read_mesh_positions(r, mesh)
        writer.setVertexPositions(mesh, [[o[0] + d[0], o[1] + d[1], o[2] + d[2]] for o, d in zip(old, deltas)])
    writer.setNeutralJointTranslations([list(t) for t in plan.joint_translations])


def calibrate(
    dna_path: str,
    manifest_path: str,
    wrapped_obj: str,
    out_dna: str,
    joint_filter: Callable[[str], bool] = core.default_joint_filter,
    update_lower_lods: bool = True,
    reader=None,
    dnac_module=None,
    backend: str = "auto",
    dna_module=None,
    eyes: Sequence[Sequence[core.Vec3]] = (),
    teeth: Sequence[core.Vec3] = (),
) -> List[str]:
    """
    Apply the wrapped neutral meshes and moved joints to a copy of the DNA. Returns a report.

    eyes / teeth: the artist's eye and teeth points in DNA space (optional); the MetaHuman eyes and
    teeth are fitted onto them first (core.fit_parts), so their joints follow too.

    backend: "dnacalib" (Epic's DNACalib commands, recalculates lower LODs), "writer"
    (OpenRigLogic dna.BinaryStreamWriter only; lower LODs unchanged) or "auto"
    (DNACalib when importable, otherwise the writer).
    """
    kind, dnac = resolve_backend(backend, dnac_module)
    r = reader if reader is not None else load_dna(dna_path, dna_module)
    blocks = core.read_manifest(manifest_path)
    wrapped = core.read_obj_positions(wrapped_obj)
    positions = core.to_dna_space(wrapped)
    new_positions = core.split_positions(positions, blocks)
    fitted = core.fit_parts(new_positions, blocks, eyes, teeth)
    plan = core.build_calibration_plan(r, new_positions, joint_filter=joint_filter)
    plan.report[:0] = fitted

    if kind == "dnacalib":
        plan.report.append("backend: DNACalib")
        calibrated = _apply_dnacalib(dnac, r, plan, update_lower_lods)
        save = (lambda: save_dna(calibrated, out_dna, dna_module)) if out_dna else None
    else:
        plan.report.append("backend: OpenRigLogic dna.BinaryStreamWriter")
        plan.report.append("lower LODs are unchanged (recalculating them needs DNACalib): they still have the original shape")
        save = (lambda: save_dna(r, out_dna, dna_module, edit=lambda w: write_plan(w, r, plan))) if out_dna else None
    plan.report.append("blendshape target deltas kept (they are relative to the neutral mesh)")
    if save is not None:
        save()
        plan.report.append(f"written {out_dna}")
    return plan.report


def main(argv: Optional[Sequence[str]] = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    e = sub.add_parser("export", help="DNA -> combined LOD OBJ + manifest")
    e.add_argument("dna")
    e.add_argument("obj")
    e.add_argument("--lod", type=int, default=0)
    e.add_argument("--meshes", default=",".join(DEFAULT_MESHES), help="comma-separated mesh name substrings")
    c = sub.add_parser("calibrate", help="DNA + wrapped OBJ -> calibrated DNA")
    c.add_argument("dna")
    c.add_argument("manifest")
    c.add_argument("wrapped_obj")
    c.add_argument("out_dna")
    c.add_argument("--joints", default="FACIAL_", help="move joints whose name starts with any of these comma-separated prefixes ('' = all)")
    c.add_argument("--no-lower-lods", action="store_true")
    c.add_argument("--backend", choices=BACKENDS, default="auto", help="auto = DNACalib if importable, else the OpenRigLogic writer")
    a = ap.parse_args(argv)
    if a.cmd == "export":
        manifest = export_obj(a.dna, a.obj, a.lod, [s for s in a.meshes.split(",") if s])
        print(f"wrote {a.obj}\nwrote {manifest}")
    else:
        prefixes = [p for p in a.joints.split(",")]
        flt = (lambda n: True) if prefixes == [""] else (lambda n: any(n.startswith(p) for p in prefixes))
        for line in calibrate(a.dna, a.manifest, a.wrapped_obj, a.out_dna, joint_filter=flt, update_lower_lods=not a.no_lower_lods, backend=a.backend):
            print(line)
    return 0


if __name__ == "__main__":
    sys.exit(main())
