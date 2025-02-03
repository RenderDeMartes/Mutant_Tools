from __future__ import absolute_import, division
from maya import cmds, OpenMaya
import maya.mel as mel
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

#---------------------------------------------

TAB_FOLDER = '003_Facial'
PYBLOCK_NAME = 'exec_brows'

#Read name conventions as nc[''] and setup as seup['']
PATH = os.path.dirname(__file__)
PATH = Path(PATH)
PATH_PARTS = PATH.parts[:-2]
FOLDER=''
for f in PATH_PARTS:
    FOLDER = os.path.join(FOLDER, f)

# ---------------------------------------------

def create_brows_block(name='L_Brow'):

    # Read name conventions as nc[''] and setup as seup['']
    PATH = os.path.dirname(__file__)
    PATH = Path(PATH)
    PATH_PARTS = PATH.parts[:-2]
    FOLDER = ''
    for f in PATH_PARTS:
        FOLDER = os.path.join(FOLDER, f)

    MODULE_FILE = os.path.join(os.path.dirname(__file__), '008_Brows.json')
    with open(MODULE_FILE) as module_file:
        module = json.load(module_file)

    nc, curve_data, setup = mt.import_configs()

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
        'nurbsPlane -p 0 0 0 -ax 0 0 1 -w 5 -lr 0.2 -d 3 -u 5 -v 1 -ch 0 -n {};'.format(
            name + nc['guide']))
    cmds.move(4,5,0)

    cmds.parent(cv, block)

    cmds.select(block)

    print('{} Created Successfully'.format(name))


#create_brow_block()

#-------------------------

def build_brows_block():

    nc, curve_data, setup = mt.import_configs()

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

    all_ctrls = []
    for name in to_build:

        # side settings
        if name.startswith(nc['right']):
            color = 'red'
        elif name.startswith(nc['left']):
            color = 'blue'
        else:
            color = 'yellow'

        surface = cmds.duplicate(guide, n=guide.replace(nc['guide'], nc['nurb']), rc=True)[0]
        cmds.parent(surface, world=True)
        if name.startswith(nc['right']):
            surface = cmds.rename(surface, surface.replace(nc['left'], nc['right']).replace(nc['nurb'] + '1',
                                                                                                     nc['nurb']))
        if cmds.getAttr('{}.Mirror'.format(config), asString=True) == 'Right_Only':
            surface_temp_grp = mt.mirror_group(surface, world=True)
            cmds.parent(surface, w=True)
            cmds.makeIdentity(surface, s=True)
            cmds.delete(surface_temp_grp)

        surface_shape = cmds.listRelatives(surface, s=True)[0]
        surface_shape = cmds.rename(surface_shape, surface + 'Shape')

        tweek_joints = []
        tweek_controllers = []
        follicles = []

        tweek_joints_grp = cmds.group(em=True, n='{}_TweekJnts{}'.format(name, nc['group']))
        tweek_ctrl_grp = cmds.group(em=True, n='{}_Tweeks{}{}'.format(name, nc['ctrl'], nc['group']))
        driver_joints_grp = cmds.group(em=True, n='{}_DriverJnts{}'.format(name, nc['group']))

        driver_joints = []
        driver_joints_roots = []

        tweek_locators = []

        # Create follicles
        cmds.select(surface_shape)
        mel.eval("createHair {} 1 10 0 0 0 0 5 0 1 2 1;".format(5))

        cmds.delete('hairSystem1', 'pfxHair1', 'nucleus1')
        #cmds.setAttr(surface + '.inheritsTransform', 0)

        for C in range(1,6):
            cmds.delete('curve' + str(C))
        fol_grp = cmds.rename('hairSystem1Follicles', name + nc['follicle'] + nc['group'])

        follicles = cmds.ls(name + nc['follicle'] + nc['group'], dag=True, type='follicle')

        # create tweek joints
        for num, fol in enumerate(follicles):
            fol = cmds.listRelatives(fol, p=True)[0]
            # Create tweek joints
            cmds.select(cl=True)
            jnt = cmds.joint(n='{}_{}{}'.format(name, num, nc['joint']))
            tweek_joints.append(jnt)
            cmds.delete(cmds.pointConstraint(fol, jnt))
            cmds.parent(jnt, tweek_joints_grp)
            jnt_root = mt.root_grp()[0]

            #Locators as dummy locators
            loc = cmds.spaceLocator(n=jnt.replace(nc['joint'], nc['locator']))[0]
            tweek_locators.append(loc)
            mt.match(loc, jnt, r=False, t=True)
            locator_root = mt.root_grp()[0]
            # Connect directy to threat as local
            cmds.connectAttr('{}.rotate'.format(fol), '{}.rotate'.format(locator_root))
            cmds.connectAttr('{}.translate'.format(fol), '{}.translate'.format(locator_root))
            cmds.connectAttr('{}.scale'.format(fol), '{}.scale'.format(locator_root))

            cmds.parent(locator_root, tweek_joints_grp)

            cmds.parentConstraint(loc, jnt)

            # Create controller
            ctrl = mt.curve(input=jnt,
                            type='square',
                            rename=True,
                            custom_name=True,
                            name=jnt.replace(nc['joint'], nc['ctrl']),
                            size=ctrl_size / 2)
            all_ctrls.append(ctrl)
            tweek_controllers.append(ctrl)
            mt.assign_color(color=color)
            ctrl_root = mt.root_grp()[0]
            mt.match(ctrl_root, jnt, r=False, t=True)

            cmds.parent(ctrl_root, tweek_ctrl_grp)

            # Connect directy to threat as local
            cmds.connectAttr('{}.rotate'.format(ctrl), '{}.rotate'.format(loc))
            cmds.connectAttr('{}.translate'.format(ctrl), '{}.translate'.format(loc))
            cmds.connectAttr('{}.scale'.format(ctrl), '{}.scale'.format(loc))
            cmds.connectAttr('{}.rotate'.format(locator_root), '{}.rotate'.format(ctrl_root))
            cmds.connectAttr('{}.translate'.format(locator_root), '{}.translate'.format(ctrl_root))

            # Driver joints
            cmds.select(cl=True)
            driver_jnt = cmds.joint(n='{}_Driver{}{}'.format(name, num, nc['joint']))
            driver_joints.append(driver_jnt)
            cmds.delete(cmds.pointConstraint(jnt, driver_jnt))
            cmds.parent(driver_jnt, driver_joints_grp)
            driver_jnt_root = mt.root_grp(autoRoot=True)[0]
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
        no_rot_locators = []
        yes_rot_locators = []

        yes_no_loc_grp = cmds.group(em=True, n= name+'_SecRot'+nc['locator']+nc['group'])

        for num, jnt in enumerate(to_sec_ctrl):
            ctrl = mt.curve(input=jnt,
                            type='sphere',
                            rename=True,
                            custom_name=True,
                            name=jnt.replace(nc['joint'], '_Sec' + nc['ctrl']),
                            size=ctrl_size*0.75)
            mt.assign_color(color=color)
            ctrl_root = mt.root_grp(autoRoot=True)[0]
            sec_ctrls.append(ctrl)
            sec_ctrls_roots.append(ctrl_root)
            mt.match(ctrl_root, jnt, r=True, t=True)
            cmds.parent(ctrl_root, main_ctrls_grp)
            # Connect directy to threat as local
            cmds.connectAttr('{}.rotate'.format(ctrl), '{}.rotate'.format(jnt))
            cmds.connectAttr('{}.translate'.format(ctrl), '{}.translate'.format(jnt))
            cmds.connectAttr('{}.scale'.format(ctrl), '{}.scale'.format(jnt))

            #create rotation ctrls
            no_rot = cmds.spaceLocator(n=jnt.replace(nc['joint'], '_noRot' + nc['locator']))[0]
            no_rot_root= mt.root_grp()[0]
            yes_rot = cmds.spaceLocator(n=jnt.replace(nc['joint'], '_yesRot' + nc['locator']))[0]
            yes_rot_root= mt.root_grp()[0]
            cmds.delete(cmds.parentConstraint(jnt, yes_rot_root))
            cmds.delete(cmds.parentConstraint(jnt, no_rot_root))
            no_rot_locators.append(no_rot)
            yes_rot_locators.append(yes_rot)
            cmds.parent(no_rot_root, yes_rot_root, yes_no_loc_grp)

        #Create mid parentConstraints
        pc = cmds.parentConstraint(driver_joints[0], driver_joints[2], driver_joints_roots[1], mo=True)[0]
        cmds.setAttr('{}.interpType'.format(pc), 2)
        pc = cmds.parentConstraint(driver_joints[4], driver_joints[2], driver_joints_roots[3], mo=True)[0]
        cmds.setAttr('{}.interpType'.format(pc), 2)

        pc = cmds.parentConstraint(main_ctrls[0], main_ctrls[1], sec_ctrls_roots[0], mo=True)[0]
        cmds.setAttr('{}.interpType'.format(pc), 2)
        pc = cmds.parentConstraint(main_ctrls[2], main_ctrls[1], sec_ctrls_roots[1], mo=True)[0]
        cmds.setAttr('{}.interpType'.format(pc), 2)

        cmds.skinCluster(driver_joints, surface, sm=0, bm=1, tsb=True)
        # sm = 0 - classical linear skinning (default). 1 - dual quaternion (volume preserving), 2 - a weighted blend between the two
        # bm = 1 - Closest distance between a joint, considering the skeleton hierarchy, and a point of the geometry. 2 - Surface heat map diffusion. 3 - Geodesic voxel binding. geomBind

        pc = cmds.parentConstraint(driver_joints[0], driver_joints[2], cmds.listRelatives(no_rot_locators[0],p=True)[0], mo=True)[0]
        cmds.setAttr('{}.interpType'.format(pc), 2)
        pc = cmds.parentConstraint(driver_joints[2], driver_joints[4], cmds.listRelatives(no_rot_locators[1],p=True)[0], mo=True)[0]
        cmds.setAttr('{}.interpType'.format(pc), 2)
        pc = cmds.parentConstraint(driver_joints[0], driver_joints[2], cmds.listRelatives(yes_rot_locators[0],p=True)[0], mo=True)[0]
        cmds.setAttr('{}.interpType'.format(pc), 2)
        pc = cmds.parentConstraint(driver_joints[2], driver_joints[4], cmds.listRelatives(yes_rot_locators[1],p=True)[0], mo=True)[0]
        cmds.setAttr('{}.interpType'.format(pc), 2)


        #Orient constraint to aim to center
        up_vector = cmds.spaceLocator(n=name+'_UpVector'+nc['locator'])[0]
        cmds.delete(cmds.parentConstraint(driver_joints[2], up_vector))
        cmds.move(0, ctrl_size*2, 0 , up_vector,r=True)
        cmds.parentConstraint(driver_joints[2], up_vector, mo=True)

        cmds.aimConstraint(driver_joints[2], yes_rot_locators[0],
                           aimVector=(1, 0, 0), upVector=(0, 1, 0), worldUpType='object',
                           worldUpObject=up_vector, mo=True)
        cmds.aimConstraint(driver_joints[2], yes_rot_locators[1],
                           aimVector=(-1, 0, 0), upVector=(0, 1, 0), worldUpType='object',
                           worldUpObject=up_vector, mo=True)
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

        cmds.parent(main_ctrls_grp, brow_ctrl)
        cmds.parent(tweek_ctrl_grp, brow_root) #to avoid double transforms


        cmds.connectAttr('{}.rotate'.format(brow_ctrl), '{}.rotate'.format(driver_joints_grp))
        cmds.connectAttr('{}.translate'.format(brow_ctrl), '{}.translate'.format(driver_joints_grp))
        cmds.connectAttr('{}.scale'.format(brow_ctrl), '{}.scale'.format(driver_joints_grp))

        #autoRotate Attrs
        mt.line_attr(input=brow_ctrl, name='AutoRotate', lines=10)
        inner_auto_rotate_attr = mt.new_attr(input= brow_ctrl,
                                            name = 'InnerRotate',
                                            min = 0 ,
                                            max = 1,
                                            default = 0)
        outer_auto_rotate_attr = mt.new_attr(input= brow_ctrl,
                                            name = 'OuterRotate',
                                            min = 0 ,
                                            max = 1,
                                            default = 0)
        blend_node = cmds.shadingNode('blendColors', asUtility=True, n='{}_innerAutoRot{}'.format(name, nc['blend']))
        # connect to blend node
        cmds.connectAttr('{}.rotate.rotateZ'.format(yes_rot_locators[0]), '{}.color1.color1R'.format(blend_node), f=1)
        cmds.connectAttr('{}.rotate.rotateZ'.format(no_rot_locators[0]), '{}.color2.color2R'.format(blend_node), f=1)
        cmds.connectAttr('{}'.format(inner_auto_rotate_attr), '{}.blender'.format(blend_node), f=1)
        cmds.connectAttr('{}.output.outputR'.format(blend_node), '{}.rotate.rotateZ'.format(cmds.listRelatives(driver_joints[1], p=True)[0]), f=1)
        cmds.connectAttr('{}.output.outputR'.format(blend_node), '{}.rotate.rotateZ'.format(cmds.listRelatives(sec_ctrls[0], p=True)[0]), f=1)

        blend_node = cmds.shadingNode('blendColors', asUtility=True, n='{}_OutterAutoRot{}'.format(name, nc['blend']))
        cmds.connectAttr('{}.rotate.rotateZ'.format(yes_rot_locators[1]), '{}.color1.color1R'.format(blend_node), f=1)
        cmds.connectAttr('{}.rotate.rotateZ'.format(no_rot_locators[1]), '{}.color2.color2R'.format(blend_node), f=1)
        cmds.connectAttr('{}'.format(outer_auto_rotate_attr), '{}.blender'.format(blend_node), f=1)
        cmds.connectAttr('{}.output.outputR'.format(blend_node), '{}.rotate.rotateZ'.format(cmds.listRelatives(driver_joints[3], p=True)[0]), f=1)
        cmds.connectAttr('{}.output.outputR'.format(blend_node), '{}.rotate.rotateZ'.format(cmds.listRelatives(sec_ctrls[1], p=True)[0]), f=1)

        #Switches vis

        if brow_ctrl.startswith(nc['right']) and guide_attrs_position.startswith(nc['left']):
            guide_attrs_position = guide_attrs_position.replace(nc['left'], nc['right'])

        if not cmds.attributeQuery('browsMainCtrls', node=guide_attrs_position, exists=True):
            mt.line_attr(input=guide_attrs_position, name='Brows_Vis')
            main_ctrl_attr = mt.new_enum(input=guide_attrs_position, name='browsMainCtrls', enums='Hide:Show',
                                         keyable=False)
        else:
            main_ctrl_attr = '{}.browsMainCtrls'.format(guide_attrs_position)
        if not cmds.attributeQuery('browsMidCtrls', node=guide_attrs_position, exists=True):
            mid_ctrl_attr = mt.new_enum(input=guide_attrs_position, name='browsMidCtrls', enums='Hide:Show',
                                        keyable=False)
        else:
            mid_ctrl_attr = '{}.browsMidCtrls'.format(guide_attrs_position)
        if not cmds.attributeQuery('browsTweekCtrls', node=guide_attrs_position, exists=True):
            show_tweeks_attr = mt.new_enum(input=guide_attrs_position, name='browsTweekCtrls', enums='Hide:Show',
                                           keyable=False)
        else:
            show_tweeks_attr = '{}.browsTweekCtrls'.format(guide_attrs_position)


        cmds.setAttr(main_ctrl_attr, 1)

        for ctrl in tweek_controllers:
            shape = cmds.listRelatives(ctrl, s=True)[0]
            cmds.connectAttr(show_tweeks_attr, '{}.v'.format(shape))
        for ctrl in sec_ctrls:
            shape = cmds.listRelatives(ctrl, s=True)[0]
            cmds.connectAttr(mid_ctrl_attr, '{}.v'.format(shape))
        if guide_attrs_position == brow_ctrl:
            for ctrl in main_ctrls:
                shape = cmds.listRelatives(ctrl, s=True)[0]
                cmds.connectAttr(main_ctrl_attr, '{}.v'.format(shape))
        else:
            for ctrl in main_ctrls + [brow_ctrl]:
                shape = cmds.listRelatives(ctrl, s=True)[0]
                cmds.connectAttr(main_ctrl_attr, '{}.v'.format(shape))
        #clean a bit
        clean_ctrl_grp = cmds.group(em=True, name=name + nc['ctrl'] + nc['group'])
        clean_rig_grp = cmds.group(em=True, name=name + '_Rig' + nc['group'])

        cmds.parent(tweek_joints_grp, driver_joints_grp, main_joints_grp, surface, fol_grp, up_vector, yes_no_loc_grp, clean_rig_grp)
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

    #Create extra brow ctrl in the Middle

    if cmds.objExists('L_Brow_Driver0_Main_Ctrl') and cmds.objExists('R_Brow_Driver0_Main_Ctrl'):

        drivers = cmds.ls('*_Driver0_Main_Ctrl')

        cmds.select(cl=True)
        curve = mt.curve(type='sphere', custom_name=True, name=name.replace(nc['right'], nc['center']) + nc['ctrl'])
        root = mt.root_grp()
        shape = cmds.listRelatives(curve, s=True)[0]
        cmds.connectAttr(main_ctrl_attr, '{}.v'.format(shape))

        center_brow_loc = cmds.spaceLocator(n=name.replace(nc['right'], nc['center']) + nc['locator'])[0]
        root_loc = mt.root_grp()
        null_loc = cmds.spaceLocator(n=name.replace(nc['right'], nc['center'])+'_Null' + nc['locator'])[0]

        cmds.select(cl=True)
        center_brow_jnt = cmds.joint(n=name.replace(nc['right'], nc['center']) + nc['joint'])
        root_joint = mt.root_grp()


        cmds.delete(cmds.pointConstraint(drivers, root))
        cmds.delete(cmds.pointConstraint(drivers, root_loc))
        cmds.delete(cmds.pointConstraint(drivers, root_joint))
        cmds.delete(cmds.pointConstraint(drivers, null_loc))

        cmds.pointConstraint(null_loc, 'L_Brow_Driver0_Main_Ctrl', 'R_Brow_Driver0_Main_Ctrl', root, mo=True)
        cmds.pointConstraint(null_loc, 'L_Brow_Driver0_Jnt', 'R_Brow_Driver0_Jnt', root_loc, mo=True)

        cmds.parentConstraint(center_brow_loc, center_brow_jnt)
        cmds.scaleConstraint(center_brow_loc, center_brow_jnt)

        cmds.connectAttr('{}.rotate'.format(curve), '{}.rotate'.format(center_brow_loc))
        cmds.connectAttr('{}.translate'.format(curve), '{}.translate'.format(center_brow_loc))
        cmds.connectAttr('{}.scale'.format(curve), '{}.scale'.format(center_brow_loc))

        for jnt in [center_brow_jnt]:
            cmds.select(cl=True)
            bind_joint = cmds.joint(n=jnt.replace(nc['joint'], nc['joint_bind']))
            cmds.parentConstraint(jnt, bind_joint)
            cmds.scaleConstraint(jnt, bind_joint)
            cmds.setAttr('{}.radius'.format(bind_joint), 1.5)
            cmds.parent(bind_joint, bind_jnt_grp)

        cmds.parent(null_loc, root_joint, root_loc, clean_rig_grp)
        cmds.parent(root, clean_ctrl_grp)

        mult_attr = mt.new_attr(curve, name='FollowSides', default=0)
        reverse_node = cmds.shadingNode('reverse', asUtility=True, name="{}_Reverse".format(curve))
        cmds.connectAttr(mult_attr, "{}.inputX".format(reverse_node), f=True)
        cmds.connectAttr("{}.output.outputX".format(reverse_node),  "C_Brow_Ctrl_Offset_Grp_pointConstraint1.C_Brow_Null_LocW0", f=True)
        cmds.connectAttr(mult_attr,  "C_Brow_Ctrl_Offset_Grp_pointConstraint1.L_Brow_Driver0_Main_CtrlW1", f=True)
        cmds.connectAttr(mult_attr,  "C_Brow_Ctrl_Offset_Grp_pointConstraint1.R_Brow_Driver0_Main_CtrlW2", f=True)

        reverse_node = cmds.shadingNode('reverse', asUtility=True, name="{}_Reverse".format(center_brow_loc))
        cmds.connectAttr(mult_attr, "{}.inputX".format(reverse_node), f=True)
        cmds.connectAttr("{}.output.outputX".format(reverse_node),
                         "C_Brow_Loc_Offset_Grp_pointConstraint1.C_Brow_Null_LocW0", f=True)
        cmds.connectAttr(mult_attr, "C_Brow_Loc_Offset_Grp_pointConstraint1.L_Brow_Driver0_JntW1", f=True)
        cmds.connectAttr(mult_attr, "C_Brow_Loc_Offset_Grp_pointConstraint1.R_Brow_Driver0_JntW2", f=True)
