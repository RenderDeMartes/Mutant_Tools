from __future__ import absolute_import, division
from maya import cmds, mel
import json
try:
    import importlib;from importlib import reload
except:
    import imp;from imp import reload

import os
from pathlib import Path

import Mutant_Tools
import Mutant_Tools.Utils.Rigging
from Mutant_Tools.Utils.Rigging import main_mutant

reload(Mutant_Tools.Utils.Rigging.main_mutant)

mt = main_mutant.Mutant()

# ---------------------------------------------

TAB_FOLDER = '003_Facial'
PYBLOCK_NAME = 'exec_cheek_advance'

# Read name conventions as nc[''] and setup as seup['']
PATH = os.path.dirname(__file__)
PATH = Path(PATH)
PATH_PARTS = PATH.parts[:-2]
FOLDER = ''
for f in PATH_PARTS:
    FOLDER = os.path.join(FOLDER, f)

# ---------------------------------------------

def create_cheek_block(name='Cheek'):

    # Read name conventions as nc[''] and setup as seup['']
    PATH = os.path.dirname(__file__)
    PATH = Path(PATH)
    PATH_PARTS = PATH.parts[:-2]
    FOLDER = ''
    for f in PATH_PARTS:
        FOLDER = os.path.join(FOLDER, f)

    MODULE_FILE = os.path.join(os.path.dirname(__file__), '007_CheeksAdvance.json')
    with open(MODULE_FILE) as module_file:
        module = json.load(module_file)

    nc, curve_data, setup = mt.import_configs()

    # name checks and block creation
    name = mt.ask_name(text=module['Name'])
    if cmds.objExists('{}{}'.format(name, nc['module'])):
        cmds.warning('Name already exists.')
        return ''

    block = mt.create_block(name=name, icon='CheeksAdvance', attrs=module['attrs'], build_command=module['build_command'],
                            import_command=module['import'])
    config = block[1]
    block = block[0]

    cv = mel.eval('curve -d 1 -p 1.337479 5.579198 0 -p 2.522103 4.623856 0 -p 3.362804 3.305484 0 -p 3.6303 1.987112 0 -p 3.362804 0.840701 0 -p 2.655851 -0.267496 0 -k 0 -k 1 -k 2 -k 3 -k 4 -k 5  -n {};'.format(name+'_Border'+nc['guide']))
    mt.assign_color(color='green')
    cheeck_guide = mt.create_joint_guide(name=name)
    cmds.move(4, 5, -2)
    cmds.parent(cv, block)
    cmds.parent(cheeck_guide, block)

    #center the pivots
    center = cmds.objectCenter(cv, gl=True)
    cmds.xform(cv, pivots=center)

    #Check bone curve
    bone_cv = mel.eval('curve -d 1 -p 0.874865 9.080194 0 -p 3.611615 8.587086 0 -p 6.200433 8.537775 0 -p 7.679757 10.288309 0 -k 0 -k 1 -k 2 -k 3 -n {};'.format(name+'_Bone'+nc['guide']))
    mt.assign_color(color='purple')
    cmds.parent(bone_cv, block)

    cmds.select(block)

    print('{} Created Successfully'.format(name))


# create_cheek_block()

# -------------------------

def build_cheek_block():

    nc, curve_data, setup = mt.import_configs()

    mt.check_is_there_is_base()

    block = cmds.ls(sl=True)
    config = cmds.listConnections(block)[1]
    block = block[0]
    joint_guide = cmds.listRelatives(block, c=True, type='joint')[0]
    childs = cmds.listRelatives(block, c=True)
    for c in childs:
        if 'Border' in c:
            border_curve=c
        if 'Bone' in c:
            bone_curve = c
    name = joint_guide.replace(nc['guide'], '')

    # use this locator in case parent is set to new locator
    if cmds.getAttr('{}.SetParent'.format(config)) == 'new_locator':
        block_parent = cmds.spaceLocator(n='{}'.format(str(block).replace(nc['module'], '_Parent' + nc['locator'])))
    else:
        block_parent = cmds.getAttr('{}.SetParent'.format(config))

    ctrl_size = cmds.getAttr('{}.CtrlSize'.format(config))
    mirror_attr = cmds.getAttr('{}.Mirror'.format(config), asString=True)

    to_build = [name]


    if mirror_attr == 'True':
        to_build = [name, name.replace(nc['left'], nc['right'])]

    for name in to_build:

        new_guide = mt.duplicate_and_remove_guides(joint_guide)
        new_guide = cmds.rename(new_guide, name+'_Main'+nc['joint'])

        # side settings
        if name.startswith(nc['right']):
            color = 'red'
        elif name.startswith(nc['left']):
            color = 'blue'
        else:
            color = 'yellow'

        linear_curve = cmds.duplicate(border_curve, n=border_curve.replace(nc['guide'], '_Linear' + nc['curve']), rc=True)[0]
        cmds.parent(linear_curve, w=True)
        if name.startswith(nc['right']):
            linear_curve = cmds.rename(linear_curve, linear_curve.replace(nc['left'], nc['right']).replace(nc['curve']+'1', nc['curve']))
        linear_curve_shape = cmds.listRelatives(linear_curve, s=True)[0]
        linear_curve_shape = cmds.rename(linear_curve_shape, linear_curve+'Shape')
        linear_curve_cvs = cmds.getAttr('{}.spans'.format(linear_curve_shape)) + 1
        print(linear_curve, linear_curve_shape)


        smooth_curve = cmds.duplicate(linear_curve, n=linear_curve.replace('_Linear' + nc['curve'], '_Driver' + nc['curve']))
        smooth_curve = cmds.rebuildCurve(keepRange=0, ch=False, rebuildType=3, kcp=1, kep=1, kt=0, s=3, d=3, tol=0.01)[0]

        wire = cmds.wire(linear_curve, n="{}_Wire".format(name), w=smooth_curve)
        cmds.setAttr('{}.dropoffDistance[0]'.format(wire[0]), 999)
        wire_base = wire[1] + 'BaseWire'

        tweek_joints = []
        tweek_controllers = []
        points_on_curve_infos = []

        tweek_joints_grp = cmds.group(em=True, n='{}_TweekJnts{}'.format(name, nc['group']))
        tweek_ctrl_grp = cmds.group(em=True, n='{}_Tweeks{}{}'.format(name, nc['ctrl'], nc['group']))

        #create tweek joints
        for num in range(linear_curve_cvs):
            #Create twwek joints
            cmds.select(cl=True)
            jnt = cmds.joint(n='{}_{}{}'.format(name, num, nc['joint']))
            tweek_joints.append(jnt)
            cmds.select('{}.cv[{}]'.format(linear_curve, num))
            temp_cls = cmds.cluster()
            cmds.delete(cmds.parentConstraint(temp_cls, jnt))
            cmds.delete(temp_cls)
            cmds.parent(jnt, tweek_joints_grp)
            jnt_root = mt.root_grp()[0]

            # point on curve info per cv
            poci = cmds.createNode('pointOnCurveInfo', n='{}_{}_POCI'.format(name, num))
            points_on_curve_infos.append(poci)
            cmds.connectAttr('{}.worldSpace[0]'.format(linear_curve_shape), '{}.inputCurve'.format(poci))
            cmds.connectAttr('{}.position'.format(poci), '{}.translate'.format(jnt_root))
            cmds.setAttr('{}.parameter'.format(poci), num)

            #Create controller
            ctrl = mt.curve(input=jnt,
                            type='square',
                            rename=True,
                            custom_name=True,
                            name=jnt.replace(nc['joint'], nc['ctrl']),
                            size=ctrl_size / 2)
            tweek_controllers.append(ctrl)
            mt.assign_color(color=color)
            ctrl_root = mt.root_grp()[0]
            mt.match(ctrl_root, jnt, r=True, t=True)

            cmds.parent(ctrl_root, tweek_ctrl_grp)

            # Connect directy to threat as local
            cmds.connectAttr('{}.rotate'.format(ctrl), '{}.rotate'.format(jnt))
            cmds.connectAttr('{}.translate'.format(ctrl), '{}.translate'.format(jnt))
            cmds.connectAttr('{}.scale'.format(ctrl), '{}.scale'.format(jnt))
            cmds.connectAttr('{}.rotate'.format(jnt_root), '{}.rotate'.format(ctrl_root))
            cmds.connectAttr('{}.translate'.format(jnt_root), '{}.translate'.format(ctrl_root))


        #Create 5 joints to control the smooth curve
        main_names = ['Top','TopMid','Mid','MidBtm','Btm']
        main_jnts = []
        main_jnts_root = []
        main_ctrls = []
        main_ctrls_roots = []

        main_ctrls_grp = cmds.group(em=True, n='{}_Main{}{}'.format(name, nc['ctrl'], nc['group']))
        main_joints_grp = cmds.group(em=True, n='{}_Main{}{}'.format(name, nc['joint'], nc['group']))

        cmds.parent(tweek_ctrl_grp, main_ctrls_grp)

        for jnt_name in main_names:
            cmds.select(cl=True)
            jnt = cmds.joint(n = name + '_' +jnt_name + nc['joint'])
            main_jnts.append(jnt)
            jnt_root=mt.root_grp()[0]
            main_jnts_root.append(jnt_root)
            cmds.parent(jnt_root, main_joints_grp)

        cmds.delete(cmds.parentConstraint(tweek_joints[0], main_jnts_root[0]))
        cmds.delete(cmds.parentConstraint(tweek_joints[-1], main_jnts_root[-1]))
        cmds.delete(cmds.parentConstraint(tweek_joints, main_jnts_root[2]))
        cmds.delete(cmds.parentConstraint(main_jnts_root[0], main_jnts_root[2], main_jnts_root[1]))
        cmds.delete(cmds.parentConstraint(main_jnts_root[-1], main_jnts_root[2], main_jnts_root[3]))

        #position over the curve
        for jnt in main_jnts:
            temp_loc = cmds.spaceLocator()[0]
            cmds.delete(cmds.parentConstraint(jnt, temp_loc))
            temp_nearest_point = cmds.createNode('nearestPointOnCurve')
            temp_decompose = cmds.createNode('decomposeMatrix')
            cmds.connectAttr('{}.worldSpace[0]'.format(smooth_curve),
                             '{}.inputCurve'.format(temp_nearest_point))
            cmds.connectAttr('{}.worldMatrix[0]'.format(temp_loc), '{}.inputMatrix'.format(temp_decompose))
            cmds.connectAttr('{}.outputTranslate'.format(temp_decompose),
                             '{}.inPosition'.format(temp_nearest_point))
            pos = cmds.getAttr('{}.result.position'.format(temp_nearest_point))[0]
            print(pos)
            cmds.setAttr(cmds.listRelatives(jnt, p=True)[0]+'.translateX', pos[0])
            cmds.setAttr(cmds.listRelatives(jnt, p=True)[0]+'.translateY', pos[1])
            cmds.setAttr(cmds.listRelatives(jnt, p=True)[0]+'.translateZ', pos[2])
            cmds.delete(temp_nearest_point, temp_decompose, temp_loc)

            #create controller for main joints
            #Create controller
            ctrl = mt.curve(input=jnt,
                            type='sphere',
                            rename=True,
                            custom_name=True,
                            name= jnt.replace(nc['joint'], nc['ctrl']),
                            size=ctrl_size)
            main_ctrls.append(ctrl)
            mt.assign_color(color=color)
            ctrl_root = mt.root_grp()[0]
            main_ctrls_roots.append(ctrl_root)
            mt.match(ctrl_root, jnt, r=True, t=True)
            cmds.parent(ctrl_root, main_ctrls_grp)
            # Connect directy to threat as local
            cmds.connectAttr('{}.rotate'.format(ctrl), '{}.rotate'.format(jnt))
            cmds.connectAttr('{}.translate'.format(ctrl), '{}.translate'.format(jnt))
            cmds.connectAttr('{}.scale'.format(ctrl), '{}.scale'.format(jnt))

        cmds.skinCluster(main_jnts, smooth_curve, sm=0, bm=1, tsb=True)
        # sm = 0 - classical linear skinning (default). 1 - dual quaternion (volume preserving), 2 - a weighted blend between the two
        # bm = 1 - Closest distance between a joint, considering the skeleton hierarchy, and a point of the geometry. 2 - Surface heat map diffusion. 3 - Geodesic voxel binding. geomBind

        #Create mid parentConstraints
        pc = cmds.parentConstraint(main_jnts[0], main_jnts[2], main_jnts_root[1], mo=True)[0]
        cmds.setAttr('{}.interpType'.format(pc), 2)
        pc = cmds.parentConstraint(main_jnts[4], main_jnts[2], main_jnts_root[3], mo=True)[0]
        cmds.setAttr('{}.interpType'.format(pc), 2)
        pc = cmds.parentConstraint(main_ctrls[0], main_ctrls[2], main_ctrls_roots[1], mo=True)[0]
        cmds.setAttr('{}.interpType'.format(pc), 2)
        pc = cmds.parentConstraint(main_ctrls[4], main_ctrls[2], main_ctrls_roots[3], mo=True)[0]
        cmds.setAttr('{}.interpType'.format(pc), 2)

        #Create main cheeck controller
        cheeck_ctrl = mt.curve(input=new_guide,
                        type='cube',
                        rename=True,
                        custom_name=True,
                        name=new_guide.replace(nc['joint'], nc['ctrl']),
                        size=ctrl_size)
        mt.assign_color(color=color)
        cheeck_root = mt.root_grp()[0]
        mt.match(cheeck_root, new_guide, r=True, t=True)

        cmds.select(new_guide)
        new_guide_root, new_guide_auto = mt.root_grp(autoRoot=True)

        cmds.connectAttr('{}.rotate'.format(cheeck_ctrl), '{}.rotate'.format(new_guide))
        cmds.connectAttr('{}.translate'.format(cheeck_ctrl), '{}.translate'.format(new_guide))
        cmds.connectAttr('{}.scale'.format(cheeck_ctrl), '{}.scale'.format(new_guide))

        cmds.parent(cheeck_root, main_ctrls_grp)
        cmds.parent(new_guide_root, main_joints_grp)


        #Create Check Bone Rig

        bone_linear_curve = cmds.duplicate(bone_curve, n=bone_curve.replace(nc['guide'], nc['curve']), rc=True)[0]
        cmds.parent(bone_linear_curve, w=True)
        if name.startswith(nc['right']):
            bone_linear_curve = cmds.rename(bone_linear_curve, bone_linear_curve.replace(nc['left'], nc['right']).replace(nc['curve']+'1', nc['curve']))
        bone_linear_curve_shape = cmds.listRelatives(bone_linear_curve, s=True)[0]
        bone_linear_curve_shape = cmds.rename(bone_linear_curve_shape, bone_linear_curve+'Shape')
        bone_linear_curve_cvs = cmds.getAttr('{}.spans'.format(bone_linear_curve_shape)) + 1
        print(bone_linear_curve, bone_linear_curve_shape)

        bone_tweeks_ctrls = []
        bone_tweeks_ctrls_roots = []
        bone_joints = []

        for num in range(bone_linear_curve_cvs):
            #Create bone twwek joints
            cmds.select(cl=True)
            jnt = cmds.joint(n='{}_{}{}'.format(name+'_Bone', num, nc['joint']))
            tweek_joints.append(jnt)
            bone_joints.append(jnt)
            cmds.select('{}.cv[{}]'.format(bone_linear_curve, num))
            temp_cls = cmds.cluster()
            cmds.delete(cmds.parentConstraint(temp_cls, jnt))
            cmds.delete(temp_cls)
            cmds.parent(jnt, tweek_joints_grp)
            jnt_root = mt.root_grp()[0]
            #Create controller
            ctrl = mt.curve(input=jnt,
                            type='square',
                            rename=True,
                            custom_name=True,
                            name=jnt.replace(nc['joint'], nc['ctrl']),
                            size=ctrl_size / 2)
            bone_tweeks_ctrls.append(ctrl)
            mt.assign_color(color=color)
            ctrl_root = mt.root_grp()[0]
            mt.match(ctrl_root, jnt, r=True, t=True)
            bone_tweeks_ctrls_roots.append(ctrl_root)
            cmds.parent(ctrl_root, tweek_ctrl_grp)

            # Connect directy to threat as local
            cmds.connectAttr('{}.rotate'.format(ctrl), '{}.rotate'.format(jnt))
            cmds.connectAttr('{}.translate'.format(ctrl), '{}.translate'.format(jnt))
            cmds.connectAttr('{}.scale'.format(ctrl), '{}.scale'.format(jnt))

        cmds.delete(bone_linear_curve)

        #Create Main Bone Ctrl
        bone_cheeck_ctrl = mt.curve(input=new_guide,
                               type='cube',
                               rename=True,
                               custom_name=True,
                               name=new_guide.replace(nc['joint'], '_Bone'+nc['ctrl']),
                               size=ctrl_size*0.75)
        mt.assign_color(color=color)
        bone_cheeck_root = mt.root_grp()[0]
        mt.match(bone_cheeck_root, bone_tweeks_ctrls[1], r=True, t=True)
        cmds.parent(bone_cheeck_root, main_ctrls_grp)

        for r in bone_tweeks_ctrls_roots:
            cmds.parent(r, bone_cheeck_ctrl)

        for b in bone_joints:
            root, auto = mt.root_grp(b, autoRoot=True)
            center = cmds.objectCenter(bone_cheeck_ctrl, gl=True)
            cmds.xform(auto, pivots=center, ws=True)

            cmds.connectAttr('{}.rotate'.format(bone_cheeck_ctrl), '{}.rotate'.format(auto))
            cmds.connectAttr('{}.translate'.format(bone_cheeck_ctrl), '{}.translate'.format(auto))
            cmds.connectAttr('{}.scale'.format(bone_cheeck_ctrl), '{}.scale'.format(auto))


        #clean a bit
        clean_ctrl_grp = cmds.group(em=True, name=name + nc['ctrl'] + nc['group'])
        clean_rig_grp = cmds.group(em=True, name=name + '_Rig' + nc['group'])

        cmds.parent(main_joints_grp,linear_curve,wire_base,smooth_curve, tweek_joints_grp, clean_rig_grp)
        cmds.parent(main_ctrls_grp, clean_ctrl_grp)

        #mirror
        if cmds.getAttr('{}.Mirror'.format(config), asString=True) == 'Right_Only':

            mirror_ctrl_grp = mt.mirror_group(clean_ctrl_grp, world=True)
            mirror_rig_grp = mt.mirror_group(clean_rig_grp, world=True)

            cmds.parent(mirror_ctrl_grp, setup['base_groups']['control'] + nc['group'])
            cmds.parent(mirror_rig_grp, '{}{}'.format(setup['rig_groups']['misc'], nc['group']))

        elif cmds.getAttr('{}.Mirror'.format(config), asString=True) == 'True':

            if str(new_guide).startswith(nc['right']):
                mirror_ctrl_grp = mt.mirror_group(clean_ctrl_grp, world=True)
                mirror_rig_grp = mt.mirror_group(clean_rig_grp, world=True)

                cmds.parent(mirror_ctrl_grp, setup['base_groups']['control'] + nc['group'])
                cmds.parent(mirror_rig_grp, '{}{}'.format(setup['rig_groups']['misc'], nc['group']))

            else:
                cmds.parent(clean_rig_grp, '{}{}'.format(setup['rig_groups']['misc'], nc['group']))
                cmds.parent(clean_ctrl_grp, setup['base_groups']['control'] + nc['group'])

        else:
            cmds.parent(clean_rig_grp, '{}{}'.format(setup['rig_groups']['misc'], nc['group']))
            cmds.parent(clean_ctrl_grp, setup['base_groups']['control'] + nc['group'])

        #Parent to block poarents


        #create bind joints
        bind_jnt_grp = '{}{}'.format(setup['rig_groups']['bind_joints'], nc['group'])
        for jnt in tweek_joints + [new_guide]:
            cmds.select(cl=True)
            bind_joint = cmds.joint(n=jnt.replace(nc['joint'], nc['joint_bind']))
            cmds.parentConstraint(jnt, bind_joint)
            cmds.scaleConstraint(jnt, bind_joint)
            cmds.setAttr('{}.radius'.format(bind_joint), 1.5)
            cmds.parent(bind_joint, bind_jnt_grp)

        # vis

        attrs_position = cmds.getAttr('{}.SetAttrsPosition'.format(config), asString=True)

        if attrs_position == 'new_locator':
            guide_attrs_position = cmds.spaceLocator(n=name + '_Attrs' + nc['locator'])[0]
        else:
            guide_attrs_position = attrs_position

        if cheeck_ctrl.startswith(nc['right']) and guide_attrs_position.startswith(nc['left']):
            guide_attrs_position = guide_attrs_position.replace(nc['left'], nc['right'])

        if not cmds.attributeQuery("cheeksMainCtrls", n=guide_attrs_position, ex=True):
            mt.line_attr(input=guide_attrs_position, name='Cheeks_Vis')
            main_ctrl_attr = mt.new_enum(input=guide_attrs_position, name='cheeksMainCtrls', enums='Hide:Show',
                                         keyable=False)
            mid_ctrl_attr = mt.new_enum(input=guide_attrs_position, name='cheeksMidCtrls', enums='Hide:Show',
                                        keyable=False)
            show_tweeks_attr = mt.new_enum(input=guide_attrs_position, name='cheeksTweekCtrls', enums='Hide:Show',
                                           keyable=False)

        cmds.setAttr(main_ctrl_attr, 1)

        #Vis switches
        if guide_attrs_position == cheeck_ctrl:
            for ctrl in main_ctrls:
                shape = cmds.listRelatives(ctrl, s=True)[0]
                cmds.connectAttr(main_ctrl_attr, '{}.v'.format(shape))
        else:
            for ctrl in main_ctrls + [cheeck_ctrl]:
                shape = cmds.listRelatives(ctrl, s=True)[0]
                cmds.connectAttr(main_ctrl_attr, '{}.v'.format(shape))

        for ctrl in [main_ctrls[1], main_ctrls[3]]:
            shape = cmds.listRelatives(ctrl, s=True)[0]
            cmds.connectAttr(mid_ctrl_attr, '{}.v'.format(shape),f=True)
        for ctrl in tweek_controllers + bone_tweeks_ctrls:
            shape = cmds.listRelatives(ctrl, s=True)[0]
            cmds.connectAttr(show_tweeks_attr, '{}.v'.format(shape))

        #Block Parent
        cmds.parentConstraint(block_parent, clean_ctrl_grp, mo=True)