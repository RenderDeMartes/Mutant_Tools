"""
Export every mesh object of a .blend file to OBJ, preserving vertex order.

    blender -b input.blend --python tools/blender_export_meshes.py -- <out_dir> [name_filter] [multires_level]

* Vertex order and polygon connectivity are written exactly as in the mesh
  data (no triangulation, no merging), so the files can serve as Base meshes.
* Generative modifiers that complete the shape (Mirror, Solidify, ...) are
  applied; Subdivision Surface and Multires are skipped so the base cage
  topology is exported. With `multires_level` > 0, Multires is evaluated at
  that level instead (high-resolution sculpt, useful as a Reference) and the
  file name gets a `_mr<level>` suffix.
* Coordinates are converted from Blender's Z-up to Y-up (x, z, -y), metres.
* UVs of the active UV layer are written per face corner.
* An inventory (inventory.json) lists objects, counts, modifiers and the
  output file names.
"""

import bpy
import json
import os
import re
import sys

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
if not argv:
    raise SystemExit("usage: blender -b file.blend --python blender_export_meshes.py -- <out_dir> [name_filter]")
out_dir = os.path.abspath(argv[0])
name_filter = re.compile(argv[1], re.I) if len(argv) > 1 and argv[1] else None
multires_level = int(argv[2]) if len(argv) > 2 else 0
os.makedirs(out_dir, exist_ok=True)

SKIP_MODIFIERS = {"SUBSURF", "MULTIRES"}
depsgraph = bpy.context.evaluated_depsgraph_get()
inventory = {"blend": bpy.data.filepath, "objects": []}


def safe(name):
    return re.sub(r"[^A-Za-z0-9_.-]+", "_", name).strip("_") or "mesh"


for obj in bpy.data.objects:
    if obj.type != "MESH":
        continue
    entry = {
        "name": obj.name,
        "collections": [c.name for c in obj.users_collection],
        "modifiers": [f"{m.type}:{m.name}" for m in obj.modifiers],
        "raw_vertices": len(obj.data.vertices),
        "raw_faces": len(obj.data.polygons),
    }
    if name_filter and not name_filter.search(obj.name):
        entry["skipped"] = "name filter"
        inventory["objects"].append(entry)
        continue
    # temporarily disable subdivision so the cage is exported
    toggled = []
    restore_levels = []
    has_multires = False
    for m in obj.modifiers:
        if m.type == "MULTIRES" and multires_level > 0:
            has_multires = True
            restore_levels.append((m, m.levels))
            m.levels = min(multires_level, m.total_levels)
            entry["multires_total_levels"] = m.total_levels
            continue
        if m.type in SKIP_MODIFIERS and m.show_viewport:
            m.show_viewport = False
            toggled.append(m)
    if multires_level > 0 and not has_multires:
        entry["skipped"] = "no multires"
        inventory["objects"].append(entry)
        continue
    bpy.context.view_layer.update()
    depsgraph = bpy.context.evaluated_depsgraph_get()
    ev = obj.evaluated_get(depsgraph)
    mesh = ev.to_mesh()
    try:
        mw = obj.matrix_world
        uv = mesh.uv_layers.active
        suffix = f"_mr{multires_level}" if multires_level > 0 else ""
        path = os.path.join(out_dir, safe(obj.name) + suffix + ".obj")
        with open(path, "w", newline="\n") as f:
            f.write(f"# exported from {os.path.basename(bpy.data.filepath)} object '{obj.name}' (CC0 source)\n")
            f.write(f"o {safe(obj.name)}\n")
            for v in mesh.vertices:
                w = mw @ v.co
                f.write(f"v {w.x:.6f} {w.z:.6f} {-w.y:.6f}\n")
            if uv:
                for d in uv.data:
                    f.write(f"vt {d.uv.x:.6f} {d.uv.y:.6f}\n")
            for p in mesh.polygons:
                if uv:
                    corners = " ".join(f"{mesh.loops[li].vertex_index + 1}/{li + 1}" for li in p.loop_indices)
                else:
                    corners = " ".join(str(vi + 1) for vi in p.vertices)
                f.write(f"f {corners}\n")
        sizes = {}
        for p in mesh.polygons:
            k = str(min(len(p.vertices), 5))
            sizes[k] = sizes.get(k, 0) + 1
        entry.update(
            file=os.path.basename(path),
            vertices=len(mesh.vertices),
            faces=len(mesh.polygons),
            polygon_sizes=sizes,
            has_uv=bool(uv),
            dimensions_m=[round(obj.dimensions.x, 4), round(obj.dimensions.z, 4), round(obj.dimensions.y, 4)],
        )
    finally:
        ev.to_mesh_clear()
        for m in toggled:
            m.show_viewport = True
        for m, lv in restore_levels:
            m.levels = lv
    inventory["objects"].append(entry)

inv_name = f"inventory_mr{multires_level}.json" if multires_level > 0 else "inventory.json"
with open(os.path.join(out_dir, inv_name), "w") as f:
    json.dump(inventory, f, indent=2)
print(f"exported {sum(1 for o in inventory['objects'] if 'file' in o)} meshes to {out_dir}")
