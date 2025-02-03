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
        print('Using selected geos to blendshape.')
        face_geos = cmds.ls(sl=True)
    if len(face_geos) == 0:
        print('Please select the geometry you want to include in the MouthIn blendshape.')
        return
    if len(face_geos) > 0:
        check_facial_addOn_Grp()

        for geo in face_geos:
            if cmds.objExists(geo):
                face_geo = 'Face_{}'.format(geo.replace('hi', 'Geo'))

                skull_nodes = find_zombie_skull(face_geo)

                dup_geo = cmds.duplicate(face_geo, n='{}_BodyMouthIn'.format(geo))
                target_count = cmds.blendShape(skull_nodes[1], q=True, wc=True)
                cmds.blendShape(skull_nodes[1], edit=True, t=(skull_nodes[0], target_count+1, dup_geo[0], 1.0))
                cmds.setAttr('{}.{}'.format(skull_nodes[1], dup_geo[0]), 1)
                
                cmds.parent(dup_geo[0],'Facial_Add_Ons_Grp')
                created_geos.append(dup_geo[0])
            else:
                print('Could not create MoutRollPull blendshape for:{}'.format(geo))

    sides = ['L_', 'R_']
    bind_joints = ['Null_Local_Bnd']
    for side in sides: 
        commisure_Ctrl = '{}Lips_Sub_Ctrl'.format(side)
        cmds.select(clear=True)
        mouthIn_jnt = cmds.joint(n = '{side}MouthCorner_0_Jnt'.format(side=side), a = True)
        bind_joints.append(mouthIn_jnt)
        mouthIn_jnt_grp = cmds.group(mouthIn_jnt, n=mouthIn_jnt.replace('Jnt', 'Jnt_Grp'))
        cmds.matchTransform(mouthIn_jnt_grp, commisure_Ctrl, pos=True, rot=True) 

        if side == 'R_':
            cmds.setAttr('{}.scaleX'.format(mouthIn_jnt_grp), -1)
            cmds.setAttr('{}.scaleY'.format(mouthIn_jnt_grp), -1)

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

        if side == 'R_':
            cmds.connectAttr('{}.translateX'.format(mouthIn_ctrl), '{}.translateX'.format(mouthIn_jnt))
            cmds.connectAttr('{}.translateY'.format(mouthIn_ctrl), '{}.translateY'.format(mouthIn_jnt))
            cmds.connectAttr('{}.rotateZ'.format(mouthIn_ctrl), '{}.rotateZ'.format(mouthIn_jnt))

            #mirror 
            cmds.connectAttr('{}.scale'.format(mouthIn_ctrl), '{}.scale'.format(mouthIn_jnt))
            r_mouthIn_md = cmds.createNode('multiplyDivide', n = '{}_reverse_md'.format(mouthIn_ctrl_grp[0]))
            cmds.setAttr('{}.input2X'.format(r_mouthIn_md), -1)
            cmds.setAttr('{}.input2Y'.format(r_mouthIn_md), -1)
            cmds.setAttr('{}.input2Z'.format(r_mouthIn_md), -1)

            cmds.connectAttr('{}.rotateX'.format(mouthIn_ctrl), '{}.input1X'.format(r_mouthIn_md))
            cmds.connectAttr('{}.rotateY'.format(mouthIn_ctrl), '{}.input1Y'.format(r_mouthIn_md))
            cmds.connectAttr('{}.translateZ'.format(mouthIn_ctrl), '{}.input1Z'.format(r_mouthIn_md))

            cmds.connectAttr('{}.outputX'.format(r_mouthIn_md), '{}.rotateX'.format(mouthIn_jnt))
            cmds.connectAttr('{}.outputY'.format(r_mouthIn_md), '{}.rotateY'.format(mouthIn_jnt))
            cmds.connectAttr('{}.outputZ'.format(r_mouthIn_md), '{}.translateZ'.format(mouthIn_jnt))

            temp_constraint = cmds.parentConstraint(commisure_Ctrl, mouthIn_ctrl_grp, mo=True)

            cmds.parent(mouthIn_ctrl_grp, 'Face_Ctrl_Grp')
            cmds.parent(mouthIn_jnt_grp, 'Face_Bind_Joints_Grp')

            mirror_grp = mt.root_grp(input=mouthIn_ctrl_grp[0])
            cmds.setAttr('{}.rotateZ'.format(mirror_grp[0]), 0)
            cmds.setAttr('{}.scaleX'.format(mirror_grp[0]), -1)
            cmds.setAttr('{}.scaleY'.format(mirror_grp[0]), 1)
            cmds.setAttr('{}.scaleZ'.format(mirror_grp[0]), 1)
            cmds.xform(mouthIn_ctrl, ro=[0,0,0])
            cmds.setAttr('{}.scaleX'.format(mouthIn_ctrl_grp[0]), 1)
            cmds.setAttr('{}.scaleY'.format(mouthIn_ctrl_grp[0]), 1)
            cmds.setAttr('{}.scaleZ'.format(mouthIn_ctrl_grp[0]), 1)

            cmds.delete(temp_constraint)
            cmds.parentConstraint(commisure_Ctrl, mouthIn_ctrl_grp, mo=False)

        else:
            cmds.connectAttr('{}.rotate'.format(mouthIn_ctrl), '{}.rotate'.format(mouthIn_jnt))
            cmds.connectAttr('{}.translate'.format(mouthIn_ctrl), '{}.translate'.format(mouthIn_jnt))
            cmds.connectAttr('{}.scale'.format(mouthIn_ctrl), '{}.scale'.format(mouthIn_jnt))

            cmds.parentConstraint(commisure_Ctrl, mouthIn_ctrl_grp, mo=True)
            cmds.parent(mouthIn_ctrl_grp, 'Face_Ctrl_Grp')
            cmds.parent(mouthIn_jnt_grp, 'Face_Bind_Joints_Grp')
    
    for created_geo in created_geos:
        cmds.skinCluster(bind_joints, created_geo)

    print('MouthIn face created in Facial_Add_Ons_Grp.')


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
                cmds.addAttr(blendshape_ctrl, sn=attr_name, at='float', dv=0, min=0, max=1, h=False, k=True)

                for geo in face_geos:
                    if cmds.objExists(geo):
                        face_geo = 'Face_{}'.format(geo.replace('hi', 'Geo'))
                        skull_nodes = find_zombie_skull(face_geo)

                        dup_geo = cmds.duplicate(face_geo, n='{}_{}_{}'.format(face_geo, blendshape_ctrl, attr_name))
                        target_count = cmds.blendShape(skull_nodes[1], q=True, wc=True)
                        cmds.blendShape(skull_nodes[1], edit=True, t=(skull_nodes[0], target_count+1, dup_geo[0], 1.0))

                        cmds.connectAttr('{}.{}'.format(blendshape_ctrl, attr_name), '{}.{}'.format(skull_nodes[1], dup_geo[0]))

                        cmds.parent(dup_geo[0],'Facial_Add_Ons_Grp')
                    else:
                        print('Could not create MoutRollPull blendshape for:{}'.format(geo))

    print('Lip Roll and Lip Pull blendshapes are ready to be modelled at Facial_Add_Ons_Grp.')


def find_zombie_skull(face_geo):
    history = cmds.listHistory(face_geo, af=True, lv=2)
    zombiebsh_node = None
    for node in history:
        if cmds.nodeType(node) == "blendShape":
            bsh_node = node
    
    if cmds.objExists(face_geo):
        faceGeo_connections = cmds.listConnections(bsh_node + ".inputTarget[0].inputTargetGroup", destination=True)
        for connection in faceGeo_connections:
            if cmds.objectType(connection) == "transform":
                geometry_name = connection

        history = cmds.listHistory(geometry_name)
        for node in history:
            if cmds.nodeType(node) == "blendShape":
                zombiebsh_node = node
        
        return [geometry_name, zombiebsh_node]

    else: 
        print('Facial system does not exist.')
        return

