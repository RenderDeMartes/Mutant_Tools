from __future__ import absolute_import
import maya.cmds as cmds 


#Duplicate eyelid and eyebrow joints to crowd rig
def dup_joints(joints, parent_name):
    for item in joints:
        dup_skl = cmds.duplicate(item, po=True)[0]
        cmds.parent(dup_skl, parent_name)
        name_skl = dup_skl.replace("Bnd1", "Skl")
        skl_joint = cmds.rename(dup_skl, name_skl)
        cmds.parentConstraint(item, skl_joint)


#Parent eyebrows to head 
def eyebrow_crowd():
    
    eyebrows = ["L_Brow_Rig_Grp", "R_Brow_Rig_Grp"]
    for eyebrow in eyebrows:
        cmds.parentConstraint("Head_Ctrl",eyebrow, mo=True)
    
    eyebrow_grps = ["L_Brow_TweekJnts_Grp","L_Brow_DriverJnts_Grp","R_Brow_TweekJnts_Grp","R_Brow_DriverJnts_Grp"]
    for brow_grp in eyebrow_grps:
        cmds.setAttr(brow_grp+".inheritsTransform", 0)

# Parent eyelids to head 
def eyelids_crowd():
     
     eyelids = ["L_Eyelids_Scale_Grp","R_Eyelids_Scale_Grp"]
     for lid in eyelids:
         cmds.parentConstraint("Head_Ctrl", lid,mo=True)
         cmds.scaleConstraint("Head_Ctrl", lid, mo=True)
     
     eyelids_groups=["L_Eyelids_Up_AimLocators_Grp", "L_Eyelids_Dw_AimLocators_Grp", "L_Eyelids_Up_Vtx_Crv", "L_Eyelids_Dw_Vtx_Crv"]
     
     for lid_grp in eyelids_groups:
         cmds.setAttr(lid_grp+".inheritsTransform",0)
     

if not cmds.pluginInfo('ngSkinTools2', q=1, loaded=1):

    cmds.loadPlugin('ngSkinTools2')


import ngSkinTools2.api as ngskin2


def create_global_eye_rig_bardel(local_mesh):
    
    hold_mat = cmds.createNode('holdMatrix', n='Head_Skl_Inverse')
    if not cmds.objExists('Head_Skl'):
        cmds.error('Could not find head_skl')
    cmds.connectAttr('Head_Skl.worldInverseMatrix[0]', '{}.inMatrix'.format(hold_mat))
    cmds.disconnectAttr('Head_Skl.worldInverseMatrix[0]', '{}.inMatrix'.format(hold_mat))
    
    influences = ngskin2.list_influences(local_mesh)
    duplicates = []
    for inf in influences:
        inf_name = inf.path_name().split('|')[-1]
        print(inf_name)
        dup_name = inf_name.replace('Wjnt', 'Skl')
        dup_name = cmds.duplicate(inf_name, n=dup_name, parentOnly=1)[0]
        duplicates.append(dup_name)
        
        # mult each by og transform and head_skl inverse
        mult_matrix = cmds.createNode('multMatrix', n=dup_name + '_MATMUL')
        cmds.connectAttr('{}.worldMatrix[0]'.format(inf_name), '{}.matrixIn[0]'.format(mult_matrix))
        cmds.connectAttr('{}.outMatrix'.format(hold_mat), '{}.matrixIn[1]'.format(mult_matrix))
        
        decompose_mat = cmds.createNode('decomposeMatrix', n=dup_name+'m2srt')
        cmds.connectAttr('{}.matrixSum'.format(mult_matrix), '{}.inputMatrix'.format(decompose_mat))
        cmds.connectAttr('{}.outputTranslate'.format(decompose_mat), '{}.t'.format(dup_name))
        cmds.connectAttr('{}.outputRotate'.format(decompose_mat), '{}.r'.format(dup_name))
        cmds.connectAttr('{}.outputScale'.format(decompose_mat), '{}.s'.format(dup_name))
        
    cmds.parent(duplicates, 'Head_Skl')
    #duplicate_grp = cmds.group(duplicates, n='Global_Rye_Rig_Grp')
   
    
#create_global_eye_rig('eyeHead')
    