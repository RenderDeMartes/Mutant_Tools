from maya import cmds, OpenMaya
import maya.mel as mel
import json
import imp
import os
from pathlib import Path

import Mutant_Tools
import Mutant_Tools.Utils.Rigging
from Mutant_Tools.Utils.Rigging import main_mutant
imp.reload(Mutant_Tools.Utils.Rigging.main_mutant)

mt = main_mutant.Mutant()

#---------------------------------------------

TAB_FOLDER = '03_Facial'
PYBLOCK_NAME = 'exec_brows'

#Read name conventions as nc[''] and setup as seup['']
PATH = os.path.dirname(__file__)
PATH = Path(PATH)
PATH_PARTS = PATH.parts[:-2]
FOLDER=''
for f in PATH_PARTS:
    FOLDER = os.path.join(FOLDER, f)

JSON_FILE = os.path.join(FOLDER, 'config', 'name_conventions.json')
with open(JSON_FILE) as json_file:
    nc = json.load(json_file)
#Read curve shapes info
CURVE_FILE = os.path.join(FOLDER, 'config', 'curves.json')
with open(CURVE_FILE) as curve_file:
    curve_data = json.load(curve_file)
#setup File
SETUP_FILE = os.path.join(FOLDER, 'config', 'rig_setup.json')
with open(SETUP_FILE) as setup_file:
    setup = json.load(setup_file)

MODULE_FILE = os.path.join(os.path.dirname(__file__),'07_Brows.json')
with open(MODULE_FILE) as module_file:
    module = json.load(module_file)


# ---------------------------------------------

def create_brows_block(name='L_Brow'):
    # name checks and block creation
    name = mt.ask_name(text=module['Name'])
    if cmds.objExists('{}{}'.format(name, nc['module'])):
        cmds.warning('Name already exists.')
        return ''

    block = mt.create_block(name=name, icon='Brows', attrs=module['attrs'], build_command=module['build_command'],
                            import_command=module['import'])
    config = block[1]
    block = block[0]

    cv = mel.eval(
        'curve -d 3 -p 3 4 0 -p 3.583333 4.285714 0 -p 4.75 4.857143 0 -p 8 6.571429 0 -p 11.25 4.857143 0 -p 12.416667 4.285714 0 -p 13 4 0 -k 0 -k 0 -k 0 -k 1 -k 2 -k 3 -k 4 -k 4 -k 4 -n {};'.format(
            name + nc['guide']))
    mt.assign_color(color='green')

    cmds.parent(cv, block)

    cmds.select(block)

    print('{} Created Successfully'.format(name))


#create_brow_block()

#-------------------------

def build_brows_block():
    mt.check_is_there_is_base()

    block = cmds.ls(sl=True)
    config = cmds.listConnections(block)[1]
    block = block[0]
    guide = cmds.listRelatives(block, c=True)[0]

    # use this locator in case parent is set to new locator
    if cmds.getAttr('{}.SetParent'.format(config)) == 'new_locator':
        block_parent = cmds.spaceLocator(n='{}'.format(str(block).replace(nc['module'], '_Parent' + nc['locator'])))
    else:
        block_parent = cmds.getAttr('{}.SetParent'.format(config))

    name = guide.replace(nc['guide'], '')

    ctrl_size = cmds.getAttr('{}.CtrlSize'.format(config))
    mirror_attr = cmds.getAttr('{}.Mirror'.format(config), asString=True)
    attrs_position = cmds.getAttr('{}.SetAttrsPosition'.format(config), asString = True)

    to_build = [guide]

    if mirror_attr == 'True':
        to_build = [name, name.replace(nc['left'], nc['right'])]

    #hide ctrls
    if name.startswith(nc['right']):
        attrs_position = attrs_position.replace(nc['left'], nc['right'])

    if attrs_position == 'new_locator':
        guide_attrs_position = cmds.spaceLocator(n=name+'_Attrs'+nc['locator'])[0]
    else:
        guide_attrs_position = attrs_position

    mt.line_attr(input=guide_attrs_position, name='Brows_Vis')
    main_ctrl_attr = mt.new_enum(input=guide_attrs_position, name='browsMainCtrls', enums='Hide:Show')
    mid_ctrl_attr = mt.new_enum(input=guide_attrs_position, name='browsMidCtrls', enums='Hide:Show')
    show_tweeks_attr = mt.new_enum(input=guide_attrs_position, name='browsTweekCtrls', enums='Hide:Show')

    for name in to_build:

        # side settings
        if name.startswith(nc['right']):
            color = 'red'
        elif name.startswith(nc['left']):
            color = 'blue'
        else:
            color = 'yellow'

        curve = cmds.duplicate(guide, n=guide.replace(nc['guide'], nc['curve']), rc=True)[0]
        cmds.parent(curve, w=True)
        if name.startswith(nc['right']):
            curve = cmds.rename(curve, curve.replace(nc['left'], nc['right']).replace(nc['curve'] + '1',
                                                                                             nc['curve']))
        curve_shape = cmds.listRelatives(curve, s=True)[0]
        curve_shape = cmds.rename(curve_shape, curve + 'Shape')
        curve_cvs = cmds.getAttr('{}.spans'.format(curve)) + 1


        tweek_joints = []
        tweek_controllers = []
        points_on_curve_infos = []

        tweek_joints_grp = cmds.group(em=True, n='{}_TweekJnts{}'.format(name, nc['group']))
        tweek_ctrl_grp = cmds.group(em=True, n='{}_Tweeks{}{}'.format(name, nc['ctrl'], nc['group']))
        driver_joints_grp = cmds.group(em=True, n='{}_DriverJnts{}'.format(name, nc['group']))

        driver_joints = []
        driver_joints_roots = []

        # create tweek joints
        for num in range(curve_cvs):
            # Create tweek joints
            cmds.select(cl=True)
            jnt = cmds.joint(n='{}_{}{}'.format(name, num, nc['joint']))
            tweek_joints.append(jnt)
            cmds.select('{}.cv[{}]'.format(curve, num))
            temp_cls = cmds.cluster()
            cmds.delete(cmds.parentConstraint(temp_cls, jnt))
            cmds.delete(temp_cls)
            cmds.parent(jnt, tweek_joints_grp)
            jnt_root = mt.root_grp()[0]

            # point on curve info per cv
            poci = cmds.createNode('pointOnCurveInfo', n='{}_{}_POCI'.format(name, num))
            points_on_curve_infos.append(poci)
            cmds.connectAttr('{}.worldSpace[0]'.format(curve), '{}.inputCurve'.format(poci))
            cmds.connectAttr('{}.position'.format(poci), '{}.translate'.format(jnt_root))
            cmds.setAttr('{}.parameter'.format(poci), num)

            # Create controller
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

            #Driver joints
            cmds.select(cl=True)
            driver_jnt = cmds.joint(n='{}_Driver{}{}'.format(name, num, nc['joint']))
            driver_joints.append(driver_jnt)
            cmds.select('{}.cv[{}]'.format(curve, num))
            cmds.delete(cmds.parentConstraint(jnt, driver_jnt))
            cmds.parent(driver_jnt, driver_joints_grp)
            driver_jnt_root = mt.root_grp()[0]
            driver_joints_roots.append(driver_jnt_root)

        #create 3 main controllers
        main_ctrls_grp = cmds.group(em=True, n='{}_Main{}{}'.format(name, nc['ctrl'], nc['group']))
        main_joints_grp = cmds.group(em=True, n='{}_Main{}{}'.format(name, nc['joint'], nc['group']))

        main_ctrls = []
        main_ctrls_roots = []


        to_main_ctrl = [driver_joints[0], driver_joints[2], driver_joints[4]]
        for num, jnt in enumerate(to_main_ctrl):
            ctrl = mt.curve(input=jnt,
                            type='sphere',
                            rename=True,
                            custom_name=True,
                            name=jnt.replace(nc['joint'], '_Main' + nc['ctrl']),
                            size=ctrl_size)
            mt.assign_color(color=color)
            ctrl_root = mt.root_grp()[0]
            main_ctrls.append(ctrl)
            main_ctrls_roots.append(ctrl_root)
            mt.match(ctrl_root, jnt, r=True, t=True)
            cmds.parent(ctrl_root, main_ctrls_grp)
            # Connect directy to threat as local
            cmds.connectAttr('{}.rotate'.format(ctrl), '{}.rotate'.format(jnt))
            cmds.connectAttr('{}.translate'.format(ctrl), '{}.translate'.format(jnt))
            cmds.connectAttr('{}.scale'.format(ctrl), '{}.scale'.format(jnt))

        to_sec_ctrl = [driver_joints[1], driver_joints[3]]
        sec_ctrls = []
        sec_ctrls_roots = []

        for num, jnt in enumerate(to_sec_ctrl):
            ctrl = mt.curve(input=jnt,
                            type='sphere',
                            rename=True,
                            custom_name=True,
                            name=jnt.replace(nc['joint'], '_Sec' + nc['ctrl']),
                            size=ctrl_size*0.75)
            mt.assign_color(color=color)
            ctrl_root = mt.root_grp()[0]
            sec_ctrls.append(ctrl)
            sec_ctrls_roots.append(ctrl_root)
            mt.match(ctrl_root, jnt, r=True, t=True)
            cmds.parent(ctrl_root, main_ctrls_grp)
            # Connect directy to threat as local
            cmds.connectAttr('{}.rotate'.format(ctrl), '{}.rotate'.format(jnt))
            cmds.connectAttr('{}.translate'.format(ctrl), '{}.translate'.format(jnt))
            cmds.connectAttr('{}.scale'.format(ctrl), '{}.scale'.format(jnt))

        #Create mid parentConstraints
        pc = cmds.parentConstraint(driver_joints[0], driver_joints[2], driver_joints_roots[1], mo=True)[0]
        cmds.setAttr('{}.interpType'.format(pc), 2)
        pc = cmds.parentConstraint(driver_joints[4], driver_joints[2], driver_joints_roots[3], mo=True)[0]
        cmds.setAttr('{}.interpType'.format(pc), 2)

        pc = cmds.parentConstraint(main_ctrls[0], main_ctrls[1], sec_ctrls_roots[0], mo=True)[0]
        cmds.setAttr('{}.interpType'.format(pc), 2)
        pc = cmds.parentConstraint(main_ctrls[2], main_ctrls[1], sec_ctrls_roots[1], mo=True)[0]
        cmds.setAttr('{}.interpType'.format(pc), 2)

        cmds.skinCluster(driver_joints, curve, sm=0, bm=1, tsb=True)

        #Main Brow Ctrl
        brow_ctrl = mt.curve(input='',
                        type='cube',
                        rename=True,
                        custom_name=True,
                        name=name + nc['ctrl'],
                        size=ctrl_size)
        mt.assign_color(color=color)
        brow_root = mt.root_grp()[0]
        mt.match(brow_root, main_ctrls[1], r=True, t=True)

        center = cmds.objectCenter(main_ctrls[1], gl=True)
        cmds.xform(driver_joints_grp, pivots=center)

        cmds.select(
        '{}.cv[0]'.format(brow_ctrl),
        '{}.cv[3:5]'.format(brow_ctrl),
        '{}.cv[11:12]'.format(brow_ctrl),
        '{}.cv[14:15]'.format(brow_ctrl),
        )
        temp_cluster=cmds.cluster()
        cmds.delete(cmds.pointConstraint(main_ctrls[0],temp_cluster))
        cmds.select(
        '{}.cv[1:2]'.format(brow_ctrl),
        '{}.cv[6:10]'.format(brow_ctrl),
        '{}.cv[13]'.format(brow_ctrl),
        )
        temp_clusterB=cmds.cluster()
        cmds.delete(cmds.pointConstraint(main_ctrls[-1],temp_clusterB))
        cmds.delete(brow_ctrl, ch=True)

        cmds.parent(tweek_ctrl_grp, main_ctrls_grp, brow_ctrl)


        cmds.connectAttr('{}.rotate'.format(brow_ctrl), '{}.rotate'.format(driver_joints_grp))
        cmds.connectAttr('{}.translate'.format(brow_ctrl), '{}.translate'.format(driver_joints_grp))
        cmds.connectAttr('{}.scale'.format(brow_ctrl), '{}.scale'.format(driver_joints_grp))


        cmds.setAttr(main_ctrl_attr, 1)

        for ctrl in tweek_controllers:
            shape = cmds.listRelatives(ctrl, s=True)[0]
            cmds.connectAttr(show_tweeks_attr, '{}.v'.format(shape))
        for ctrl in sec_ctrls:
            shape = cmds.listRelatives(ctrl, s=True)[0]
            cmds.connectAttr(mid_ctrl_attr, '{}.v'.format(shape))
        for ctrl in main_ctrls + [brow_ctrl]:
            shape = cmds.listRelatives(ctrl, s=True)[0]
            cmds.connectAttr(main_ctrl_attr, '{}.v'.format(shape))

        #clean a bit
        clean_ctrl_grp = cmds.group(em=True, name=name + nc['ctrl'] + nc['group'])
        clean_rig_grp = cmds.group(em=True, name=name + '_Rig' + nc['group'])

        cmds.parent(tweek_joints_grp, driver_joints_grp, main_joints_grp, curve, clean_rig_grp)
        cmds.parent(brow_root, clean_ctrl_grp)

        #mirror
        if cmds.getAttr('{}.Mirror'.format(config), asString=True) == 'Right_Only':

            mirror_ctrl_grp = mt.mirror_group(clean_ctrl_grp, world=True)
            mirror_rig_grp = mt.mirror_group(clean_rig_grp, world=True)

            cmds.parent(mirror_ctrl_grp, setup['base_groups']['control'] + nc['group'])
            cmds.parent(mirror_rig_grp, '{}{}'.format(setup['rig_groups']['misc'], nc['group']))

        elif cmds.getAttr('{}.Mirror'.format(config), asString=True) == 'True':

            if str(name).startswith(nc['right']):
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

        #create bind joints
        bind_jnt_grp = '{}{}'.format(setup['rig_groups']['bind_joints'], nc['group'])
        for jnt in tweek_joints:
            cmds.select(cl=True)
            bind_joint = cmds.joint(n=jnt.replace(nc['joint'], nc['joint_bind']))
            cmds.parentConstraint(jnt, bind_joint)
            cmds.scaleConstraint(jnt, bind_joint)
            cmds.setAttr('{}.radius'.format(bind_joint), 1.5)
            cmds.parent(bind_joint, bind_jnt_grp)


        #Block Parent
        cmds.parentConstraint(block_parent, clean_ctrl_grp, mo=True)