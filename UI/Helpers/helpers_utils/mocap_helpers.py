from __future__ import absolute_import
from maya import cmds
import os
import tempfile
import shutil

"""
---------------Fix Legs Orients (Mocap tab)-----------------
"""

# -------------------------------------------------------------
# JOINTS
# -------------------------------------------------------------

JOINTS = [
    "thigh_l",
    "thigh_twist_01_l",
    "calf_l",
    "calf_twist_01_l",
    "calf_twist_02_l",
    "foot_l",

    "thigh_r",
    "thigh_twist_01_r",
    "calf_r",
    "calf_twist_01_r",
    "calf_twist_02_r",
    "foot_r",
]

CONSTRAINT_TYPES = (
    "parentConstraint",
    "orientConstraint",
    "pointConstraint",
    "scaleConstraint",
    "aimConstraint",
)

# -------------------------------------------------------------
# SKIN SAVE / REMOVE / RESTORE
# (Save whatever skin -ng or normal- lives on the geos bound to JOINTS,
#  remove it so the orient fix doesn't drag the bind pose, then restore it)
# -------------------------------------------------------------

def _ngskintools_api():
    try:
        from ngSkinTools2 import api as ngst_api
        from ngSkinTools2.api import init_layers
        return ngst_api, init_layers
    except Exception:
        return None, None


def _ng_layers_node(skin):
    nodes = cmds.listConnections(skin, type='ngst2SkinLayerData') or []
    return nodes[0] if nodes else None


def find_skinned_geos_for_joints(joints):
    from Mutant_Tools.Utils.IO import SkinUtils
    try:
        import importlib; importlib.reload(SkinUtils)
    except Exception:
        import imp; imp.reload(SkinUtils)
    cSkin = SkinUtils.Skinning()

    affected = []
    for geo in cSkin.get_all_geo_with_skin():
        influences = cSkin.get_influences(geo) or []
        if any(j in influences for j in joints):
            affected.append(geo)
    return affected


def save_skins_for_geos(geos, folder):
    from Mutant_Tools.Utils.IO import SkinUtils
    try:
        import importlib; importlib.reload(SkinUtils)
    except Exception:
        import imp; imp.reload(SkinUtils)
    cSkin = SkinUtils.Skinning()

    ngst_api, init_layers = _ngskintools_api()

    saved = []
    for geo in geos:
        skin = cSkin.get_skin_from_geo(geo)
        influences = cSkin.get_influences(geo)
        safe_name = geo.replace(':', '__NS__')

        use_ng = bool(ngst_api) and skin and _ng_layers_node(skin) is not None

        if use_ng:
            init_layers(skin)
            file_path = os.path.join(folder, safe_name + '.ng.json')
            config = ngst_api.InfluenceMappingConfig()
            config.use_distance_matching = True
            config.use_name_matching = False
            ngst_api.export_json(geo, file=file_path)
            saved.append({'geo': geo, 'mode': 'ng', 'file': file_path, 'influences': influences})
        else:
            data = cSkin.get_weights(geo)
            file_path = os.path.join(folder, safe_name + '.json')
            cSkin.save(data=data, path=file_path)
            saved.append({'geo': geo, 'mode': 'normal', 'file': file_path, 'influences': influences})

    return saved


def remove_skins(saved):
    for entry in saved:
        geo = entry['geo']
        if not cmds.objExists(geo):
            continue
        skin = cmds.ls(cmds.listHistory(geo), type='skinCluster')
        if skin:
            cmds.delete(skin[0])


def restore_skins_for_geos(saved):
    from Mutant_Tools.Utils.IO import SkinUtils
    try:
        import importlib; importlib.reload(SkinUtils)
    except Exception:
        import imp; imp.reload(SkinUtils)
    cSkin = SkinUtils.Skinning()

    ngst_api, _ = _ngskintools_api()

    for entry in saved:
        geo = entry['geo']
        if not cmds.objExists(geo):
            continue

        if entry['mode'] == 'ng' and ngst_api:
            cmds.skinCluster(geo, entry['influences'], tsb=True)
            config = ngst_api.InfluenceMappingConfig()
            config.use_distance_matching = True
            config.use_name_matching = False
            ngst_api.import_json(geo, file=entry['file'], influences_mapping_config=config)
        else:
            skin_data = cSkin.load_data(path=entry['file'])
            cSkin.set_weights(all_data=skin_data, geometry=geo, remove_unused=True)


# -------------------------------------------------------------
# CONSTRAINTS SAVE / RESTORE (on the leg JOINTS themselves)
# -------------------------------------------------------------

def save_state(joints=None):

    joints = JOINTS if joints is None else joints

    data = {}

    for j in joints:

        parent = cmds.listRelatives(j, p=True)
        parent = parent[0] if parent else None

        constraints = []

        for ctype in CONSTRAINT_TYPES:

            cons = cmds.listConnections(
                j,
                type=ctype,
                source=True,
                destination=False
            ) or []

            for c in set(cons):

                if ctype == "parentConstraint":
                    targets = cmds.parentConstraint(c, q=True, targetList=True) or []

                elif ctype == "orientConstraint":
                    targets = cmds.orientConstraint(c, q=True, targetList=True) or []

                elif ctype == "pointConstraint":
                    targets = cmds.pointConstraint(c, q=True, targetList=True) or []

                elif ctype == "scaleConstraint":
                    targets = cmds.scaleConstraint(c, q=True, targetList=True) or []

                elif ctype == "aimConstraint":
                    targets = cmds.aimConstraint(c, q=True, targetList=True) or []

                else:
                    targets = []

                constraints.append({
                    "name": c,
                    "type": ctype,
                    "targets": targets
                })

        data[j] = {
            "parent": parent,
            "constraints": constraints
        }

    return data


def delete_constraints(data):

    for info in data.values():
        for c in info["constraints"]:
            if cmds.objExists(c["name"]):
                cmds.delete(c["name"])


def parent_world(joints=None):

    joints = JOINTS if joints is None else joints

    for j in joints:
        if cmds.objExists(j):
            cmds.parent(j, world=True)


def restore_hierarchy(data, joints=None):

    joints = JOINTS if joints is None else joints

    for j in joints:

        parent = data[j]["parent"]

        if parent and cmds.objExists(parent):
            cmds.parent(j, parent)


def restore_constraints(data, joints=None):

    joints = JOINTS if joints is None else joints

    for joint in joints:

        for c in data[joint]["constraints"]:

            t = c["targets"]

            if c["type"] == "parentConstraint":
                cmds.parentConstraint(
                    t,
                    joint,
                    mo=True,
                    n=c["name"]
                )

            elif c["type"] == "orientConstraint":
                cmds.orientConstraint(
                    t,
                    joint,
                    mo=True,
                    n=c["name"]
                )

            elif c["type"] == "pointConstraint":
                cmds.pointConstraint(
                    t,
                    joint,
                    mo=True,
                    n=c["name"]
                )

            elif c["type"] == "scaleConstraint":
                cmds.scaleConstraint(
                    t,
                    joint,
                    mo=True,
                    n=c["name"]
                )

            elif c["type"] == "aimConstraint":
                cmds.aimConstraint(
                    t,
                    joint,
                    mo=True,
                    n=c["name"]
                )


# -------------------------------------------------------------
# REORIENT THIGHS
# -------------------------------------------------------------

def orient_thighs():

    # LEFT
    cmds.joint(
        "thigh_l",
        e=True,
        oj="xdown",
        sao="zdown",
        ch=False,
        zso=True
    )

    # RIGHT
    cmds.joint(
        "thigh_r",
        e=True,
        oj="xup",
        sao="zup",
        ch=False,
        zso=True
    )


def aim_legs():

    # -------------------------------------------------
    # LEFT
    # Aim X- at calf_l
    # Up = +Y using L_Hip_Jnt_Switch_Loc
    # -------------------------------------------------

    ac = cmds.aimConstraint(
        "calf_l",
        "thigh_l",
        aimVector=(-1, 0, 0),
        upVector=(0, 1, 0),
        worldUpType="vector",
        worldUpVector=(0, 0, -1)   # World Front (+Z)
    )

    cmds.delete(ac)

    # thigh_twist_01_l aims at calf_l, same convention as thigh_l
    ac = cmds.aimConstraint(
        "calf_l",
        "thigh_twist_01_l",
        aimVector=(-1, 0, 0),
        upVector=(0, 1, 0),
        worldUpType="vector",
        worldUpVector=(0, 0, -1)
    )

    cmds.delete(ac)

    # calf_l aims at foot_l
    ac = cmds.aimConstraint(
        "foot_l",
        "calf_l",
        aimVector=(-1, 0, 0),
        upVector=(0, 1, 0),
        worldUpType="vector",
        worldUpVector=(0, 0, -1)
    )

    cmds.delete(ac)

    # calf_twist_01_l aims at foot_l, same convention as calf_l
    ac = cmds.aimConstraint(
        "foot_l",
        "calf_twist_01_l",
        aimVector=(-1, 0, 0),
        upVector=(0, 1, 0),
        worldUpType="vector",
        worldUpVector=(0, 0, -1)
    )

    cmds.delete(ac)

    # -------------------------------------------------
    # RIGHT
    # Aim X+ at calf_r
    # Up = +Y using R_Hip_Jnt_Switch_Loc
    # -------------------------------------------------

    ac = cmds.aimConstraint(
        "calf_r",
        "thigh_r",
        aimVector=(1, 0, 0),
        upVector=(0, 1, 0),
        worldUpType="vector",
        worldUpVector=(0, 0, 1)   # World Front (+Z)
    )

    cmds.delete(ac)

    # thigh_twist_01_r aims at calf_r, same convention as thigh_r
    ac = cmds.aimConstraint(
        "calf_r",
        "thigh_twist_01_r",
        aimVector=(1, 0, 0),
        upVector=(0, 1, 0),
        worldUpType="vector",
        worldUpVector=(0, 0, 1)
    )

    cmds.delete(ac)

    # calf_r aims at foot_r
    ac = cmds.aimConstraint(
        "foot_r",
        "calf_r",
        aimVector=(1, 0, 0),
        upVector=(0, 1, 0),
        worldUpType="vector",
        worldUpVector=(0, 0, 1)
    )

    cmds.delete(ac)

    # calf_twist_01_r aims at foot_r, same convention as calf_r
    ac = cmds.aimConstraint(
        "foot_r",
        "calf_twist_01_r",
        aimVector=(1, 0, 0),
        upVector=(0, 1, 0),
        worldUpType="vector",
        worldUpVector=(0, 0, 1)
    )

    cmds.delete(ac)


# -------------------------------------------------------------
# MAIN
# -------------------------------------------------------------

def fix_legs_orient():

    affected_geos = find_skinned_geos_for_joints(JOINTS)

    temp_folder = tempfile.mkdtemp(prefix='mutant_fix_legs_orient_')
    saved_skins = save_skins_for_geos(affected_geos, temp_folder) if affected_geos else []

    try:
        remove_skins(saved_skins)

        state = save_state()
        delete_constraints(state)
        parent_world()
        aim_legs()
        restore_hierarchy(state)
        restore_constraints(state)

        restore_skins_for_geos(saved_skins)

    except Exception:
        cmds.warning('Fix Legs Orients failed, saved skin data kept at: {}'.format(temp_folder))
        raise
    else:
        shutil.rmtree(temp_folder, ignore_errors=True)

    print("Finished.")

    if cmds.objExists("thigh_l"):
        cmds.select("thigh_l")


# -------------------------------------------------------------
# THUMB ORIENT (nudge by increments, L / R)
# -------------------------------------------------------------

THUMB_JOINTS_L = ["thumb_01_l", "thumb_02_l", "thumb_03_l"]
THUMB_JOINTS_R = ["thumb_01_r", "thumb_02_r", "thumb_03_r"]


def nudge_thumb_orient(joints, amount):

    existing_joints = [j for j in joints if cmds.objExists(j)]
    if not existing_joints:
        cmds.warning('None of these joints exist in the scene: {}'.format(', '.join(joints)))
        return

    selection = cmds.ls(sl=True) or []

    affected_geos = find_skinned_geos_for_joints(existing_joints)

    temp_folder = tempfile.mkdtemp(prefix='mutant_thumb_orient_')
    saved_skins = save_skins_for_geos(affected_geos, temp_folder) if affected_geos else []

    restored = False

    try:
        remove_skins(saved_skins)

        state = save_state(existing_joints)
        delete_constraints(state)

        try:
            parent_world(existing_joints)

            for j in existing_joints:
                current = cmds.getAttr('{}.rotateX'.format(j))
                cmds.setAttr('{}.rotateX'.format(j), current + amount)

        finally:
            # Always put the hierarchy and constraints back, even if a
            # rotate failed partway (e.g. a locked/connected rotateX).
            restore_hierarchy(state, existing_joints)
            restore_constraints(state, existing_joints)

        restore_skins_for_geos(saved_skins)
        restored = True

    finally:
        if restored:
            shutil.rmtree(temp_folder, ignore_errors=True)
        else:
            cmds.warning('Thumb Orient nudge hit an error, saved skin data kept at: {}'.format(temp_folder))

        if selection:
            existing_selection = [s for s in selection if cmds.objExists(s)]
            if existing_selection:
                cmds.select(existing_selection)
        else:
            cmds.select(clear=True)


def nudge_thumb_orient_left(amount):
    nudge_thumb_orient(THUMB_JOINTS_L, amount)


def nudge_thumb_orient_right(amount):
    nudge_thumb_orient(THUMB_JOINTS_R, amount)
