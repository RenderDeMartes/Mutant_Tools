from __future__ import absolute_import
from maya import cmds
try:
    import importlib;from importlib import reload
except:
    import imp;from imp import reload
import Mutant_Tools
import Mutant_Tools.Utils.Rigging
from Mutant_Tools.Utils.Rigging import main_mutant
reload(Mutant_Tools.Utils.Rigging.main_mutant)

mt = main_mutant.Mutant()
nc = mt.import_configs()

def check_facial_addOn_Grp():
    if cmds.objExists('Facial_Add_Ons_Grp'):
            print('AddOn group exists.')
    else:
        cmds.group(em=True, p='Locals_Rig_Grp', n='Facial_Add_Ons_Grp')
        cmds.select(clear=True)


def create_MouthIn(face_geos=[], mirror=True):
    '''

    '''
    created_geos = []
    if len(face_geos) == 0: 
        face_geos = cmds.ls(sl=True)
    if len(face_geos) == 0:
        print('Please select the geometry you want to include in the MouthIn blendshape.')
        return
    if len(face_geos) > 0:
        check_facial_addOn_Grp()

        for geo in face_geos:
            face_geo = 'Face_{}'.format(geo.replace('hi', 'Geo'))

            skull_nodes = find_zombie_skull(face_geo)

            dup_geo = cmds.duplicate(face_geo, n='{}_BodyMouthIn'.format(geo))
            target_count = cmds.blendShape(skull_nodes[1], q=True, wc=True)
            cmds.blendShape(skull_nodes[1], edit=True, t=(skull_nodes[0], target_count+1, dup_geo[0], 1.0))
            cmds.setAttr('{}.{}'.format(skull_nodes[1], dup_geo[0]), 1)
            
            cmds.parent(dup_geo[0],'Facial_Add_Ons_Grp')
            created_geos.append(dup_geo[0])

    sides = ['L_', 'R_']
    bind_joints = ['Null_Local_Bnd']
    for side in sides: 
        commisure_Ctrl = '{}Lips_Sub_Ctrl'.format(side)
        cmds.select(clear=True)
        mouthIn_jnt = cmds.joint(n = '{side}MouthCorner_0_Jnt'.format(side=side), a = True)
        bind_joints.append(mouthIn_jnt)
        mouthIn_jnt_grp = cmds.group(mouthIn_jnt, n=mouthIn_jnt.replace('Jnt', 'Jnt_Grp'))
        cmds.matchTransform(mouthIn_jnt_grp, commisure_Ctrl, pos=True, rot=True) 

        mouthIn_ctrl = mt.curve(input=mouthIn_jnt,
            type='sphere',
            rename=True,
            custom_name=True,
            name=mouthIn_jnt.replace('_Jnt', '_Ctrl'),
            size=0.5)
        mt.assign_color(color='yellow')
        mouthIn_ctrl_grp = mt.root_grp(input=mouthIn_ctrl)
        #mouthIn_ctrl_grp = cmds.group(mouthIn_ctrl, n=mouthIn_ctrl.replace('Ctrl', 'Grp'))
        cmds.matchTransform(mouthIn_ctrl_grp, commisure_Ctrl, pos=True, rot=True) 

        cmds.setAttr('{}.scaleX'.format(mouthIn_ctrl_grp[0]), -1)
        cmds.setAttr('{}.scaleY'.format(mouthIn_ctrl_grp[0]), -1)

        cmds.connectAttr('{}.rotate'.format(mouthIn_ctrl), '{}.rotate'.format(mouthIn_jnt))
        cmds.connectAttr('{}.translate'.format(mouthIn_ctrl), '{}.translate'.format(mouthIn_jnt))
        cmds.connectAttr('{}.scale'.format(mouthIn_ctrl), '{}.scale'.format(mouthIn_jnt))

        cmds.parentConstraint(commisure_Ctrl, mouthIn_ctrl_grp, mo=True)
    
        cmds.parent(mouthIn_ctrl_grp, 'Face_Ctrl_Grp')
        cmds.parent(mouthIn_jnt_grp, 'Face_Bind_Joints_Grp')
    
    for created_geo in created_geos:
        cmds.skinCluster(bind_joints, created_geo)

    print('MouthIn face created in Facial_Add_Ons_Grp.')
    cmds.select(dup_geo[0])


def create_Mouth_RollPull(face_geos=[], mirror=True):
    '''

    '''
    if len(face_geos) == 0: 
        face_geos = cmds.ls(sl=True)
    if len(face_geos) == 0:
        print('Please select the geometry you want to include in the Lip Roll and Lip Pull blendshapes.')
        return
    if len(face_geos) > 0:
        check_facial_addOn_Grp()

        attr_names = ['Lip_Roll', 'Lip_Pull']
        blendshape_ctrls = ['Lips_Up_Main_Ctrl', 'Lips_Dw_Main_Ctrl']

        for blendshape_ctrl in blendshape_ctrls:
            for attr_name in attr_names:
                print(blendshape_ctrl)
                cmds.addAttr(blendshape_ctrl, sn=attr_name, at='float', dv=0, min=0, max=0, h=False, k=True)

                for geo in face_geos:
                    face_geo = 'Face_{}'.format(geo.replace('hi', 'Geo'))
                    skull_nodes = find_zombie_skull(face_geo)

                    dup_geo = cmds.duplicate(face_geo, n='{}_{}_{}'.format(face_geo, blendshape_ctrl, attr_name))
                    target_count = cmds.blendShape(skull_nodes[1], q=True, wc=True)
                    cmds.blendShape(skull_nodes[1], edit=True, t=(skull_nodes[0], target_count+1, dup_geo[0], 1.0))

                    cmds.connectAttr('{}.{}'.format(blendshape_ctrl, attr_name), '{}.{}'.format(skull_nodes[1], dup_geo[0]))

                    cmds.parent(dup_geo[0],'Facial_Add_Ons_Grp')

    cmds.select(dup_geo[0])
    print('Lip Roll and Lip Pull blendshapes are ready to be modelled at Facial_Add_Ons_Grp.')


def find_zombie_skull(face_geo):
    history = cmds.listHistory(face_geo, af=True, lv=1)
    for node in history:
        if cmds.nodeType(node) == "blendShape":
            bsh_node = node
    
    if cmds.objExists(face_geo):
        faceGeo_connections = cmds.listConnections(bsh_node + ".inputTarget[0].inputTargetGroup", destination=True)
        for connection in faceGeo_connections:
            if cmds.objectType(connection) == "transform":
                geometry_name = connection

        history = cmds.listHistory(geometry_name, af=True, lv=1)
        for node in history:
            if cmds.nodeType(node) == "blendShape":
                zombiebsh_node = node
        
        return [geometry_name, zombiebsh_node]

    else: 
        print('Facial system does not exist.')
        return

