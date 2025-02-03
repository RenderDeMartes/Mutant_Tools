from __future__ import absolute_import
"""

import Mutant_Tools
from Mutant_Tools.Utils.LODs import lods_utils
reload(lods_utils)


lods_utils.convert_high_to_mid()
lods_utils.convert_mid_to_low()
lods_utils.convert_high_to_proxy()
"""
try:
    import importlib;from importlib import reload
except:
    import imp;from imp import reload
from maya import cmds, mel
from rigSystem.assetTemplates.core import (get_one_sid, validate_sid)

from maya import cmds
import maya.mel as mel
mel.eval("source channelBoxCommand;")

def convert_high_to_mid():
    """ Will convert High rig into mid rig LOD

    Returns (bool): True if success

    """

    inverse_groups = cmds.ls('*_Inverse_Grp')
    rivets = cmds.ls('Rivet*')

    mel.eval('source generateChannelMenu.mel;')

    #Disconnect inverse groups for rivets
    mel.eval('source generateChannelMenu.mel;')
    if inverse_groups:
        for grp in inverse_groups:
            mel.eval('CBdeleteConnection "{}.tx";'.format(grp))
            mel.eval('CBdeleteConnection "{}.ty";'.format(grp))
            mel.eval('CBdeleteConnection "{}.tz";'.format(grp))

    #Delete rivets related nodes
    if rivets:
        cmds.delete(rivets)

    #Changer task to rig mid
    sid = get_one_sid()
    sid = validate_sid(sid)
    sid.tag(publish_kind='rig-mid')

    return True

def convert_mid_to_low():
    """ Will convert Mid Rig into Low Rig LOD

    Returns (bool): True if success

    """
    if cmds.objExists('C_Tongue_hi'):
        try:cmds.skinCluster('C_Tongue_hi', 'Head_Bnd')
        except:pass
    else:
        try:change_tongue_skinning()
        except:pass

    #Do convertion
    to_delete = ['Face_Ctrls_Grp', 'Face_Rig', 'Face_Bind', 'Face_Ctrl_Grp',
                 'Face_geo', 'Pivot_Head_SS_Grp_Offset', 'Face_bind', 'Face_Rig_Grp',
                 'faceBind_rgrp', 'faceRig_rid']

    for node in to_delete:
        if cmds.objExists(node):
            cmds.delete(node)

    #Rebind to head geo
    if cmds.objExists('C_Facial_grp'):
        for geo in cmds.listRelatives('C_Facial_grp', ad=True):
            try:
                cmds.select(geo, 'Head_Bnd')
                cmds.skinCluster(tsb=True)
            except Exception as e:
                print(e)

    #Changer task to rig mid
    sid = get_one_sid()
    sid = validate_sid(sid)
    sid.tag(publish_kind='rig-low')

    try:
        cmds.parentConstraint('Head_Bnd', 'EyesEye_Grp', mo=True)
    except:
        pass
    try:
        cmds.parentConstraint('Head_Bnd', 'EyesEye_Grp1Mirror_Grp', mo=True)
    except:
        pass

    return True

def convert_high_to_low():
    """ Will convert High to Mid and Mid to Low in one step

    Returns (bool): True if success

    """

    convert_high_to_mid()
    convert_mid_to_low()

    return True

def convert_high_to_proxy():

    try:convert_high_to_low()
    except:pass

    from Mutant_Tools.Utils.External.PerryTools import mesh
    reload(mesh)
    geos = cmds.listRelatives('geo', ad=True, type='transform')
    for geo in geos:
        try:
            if 'grp' in geo or 'Grp' in geo:
                continue
            if 'prxy' in geo:
                cmds.delete(geo)
                continue
            if 'Ref' in geo:
                cmds.delete(geo)
                continue
            #Get the material
            shader = shadersFromObject(geo)
            vtx_color = get_vertex_color(geo)
        except:
            pass

        #Cut geo
        try:
            proxy_geo = mesh.cutCharacterFromSkin(inObject=geo, internal=False, maya2020 = False)
            if proxy_geo:
                #re assign material
                print(geo, shader, vtx_color)
                if shader:
                    cmds.select(proxy_geo)
                    try:cmds.hyperShade(assign=shader)
                    except:pass
                if vtx_color:
                    for subgeo in cmds.listRelatives(proxy_geo, ad=True, type='mesh'):
                        try:assing_vertex_color(subgeo, vtx_color)
                        except:pass
                #Organize
                cmds.delete(geo)
                cmds.parent(proxy_geo, 'geo')
        except:
            pass


    print('Done Creating Proxy')

def shadersFromObject(obj):
    if cmds.objExists(obj):
        cmds.select(obj)
    else:
        return False
    try:cmds.hyperShade(obj, shaderNetworksSelectMaterialNodes=True)
    except:return False
    shaders = cmds.ls(selection=True)
    #shader = cmds.listConnections(shaders[0]+'.outColor')
    if shaders:
        return shaders[0]
    else:
        return False

def get_vertex_color(geo):
    try:
        cmds.select('{}.vtx[0]'.format(geo))
        color = cmds.polyColorPerVertex(query=True, rgb=True)
        return color
    except:
        return False

def assing_vertex_color(geo, color):
    vtx = cmds.ls(geo + '.vtx[*]', fl=True)
    cmds.select(vtx)
    cmds.polyColorPerVertex(rgb=color)

def change_tongue_skinning():

    face_geos = []

    tongue_skins = get_skin_with_joint('Tongue_01_Bnd')
    if tongue_skins:
        for skin in tongue_skins:
            geo = get_geometry_with_skin(skin)[0]
            face_geos.append(geo)
            cmds.delete(skin)
    if not face_geos:
        return
    for geo in face_geos:
        #geo=geo.replace('Face_', '').replace('_Geo', '_Hi')
        print(cmds.listRelatives(geo, p=True)[0], 'Head_Bnd')
        cmds.skinCluster(cmds.listRelatives(geo, p=True)[0], 'Head_Bnd', tsb=True)
        cmds.select(cmds.listRelatives(geo, p=True)[0], 'Head_Bnd')

def get_skin_with_joint(joint=''):

    skins_with_joint = []
    skins = cmds.ls(type='skinCluster')
    for skin in skins:
        jnts =cmds.skinCluster(skin, query=True, inf=True)
        if joint in jnts:
            skins_with_joint.append(skin)

    return skins_with_joint

def get_geometry_with_skin(skin=''):
    geo = cmds.skinCluster(skin, q=True, geometry=True)
    return geo

