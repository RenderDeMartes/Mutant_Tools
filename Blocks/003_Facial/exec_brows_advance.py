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
PYBLOCK_NAME = 'exec_brows_advance'

#Read name conventions as nc[''] and setup as seup['']
PATH = os.path.dirname(__file__)
PATH = Path(PATH)
PATH_PARTS = PATH.parts[:-2]
FOLDER=''
for f in PATH_PARTS:
    FOLDER = os.path.join(FOLDER, f)

# ---------------------------------------------

def create_brows_advance_block(name='L_Brow'):

    # Read name conventions as nc[''] and setup as seup['']
    PATH = os.path.dirname(__file__)
    PATH = Path(PATH)
    PATH_PARTS = PATH.parts[:-2]
    FOLDER = ''
    for f in PATH_PARTS:
        FOLDER = os.path.join(FOLDER, f)

    MODULE_FILE = os.path.join(os.path.dirname(__file__), '009_BrowsAdvance.json')
    with open(MODULE_FILE) as module_file:
        module = json.load(module_file)

    nc, curve_data, setup = mt.import_configs()

    # name checks and block creation
    name = mt.ask_name(text=module['Name'])
    if cmds.objExists('{}{}'.format(name, nc['module'])):
        cmds.warning('Name already exists.')
        return ''

    block = mt.create_block(name=name, icon='L_BrowAdvance', attrs=module['attrs'], build_command=module['build_command'],
                            import_command=module['import'])
    config = block[1]
    block = block[0]

    surface = mel.eval(
        'nurbsPlane -p 0 0 0 -ax 0 0 1 -w 5 -lr 1 -d 3 -u 3 -v 5 -ch 1 -n {};'.format(
            name + nc['guide']))[0]
    cmds.move(4,5,0)

    cmds.select(surface+'Shape')
    mel.eval("createHair {} 1 10 0 0 0 0 5 0 1 2 1;".format(7))

    cmds.delete('hairSystem1', 'pfxHair1', 'nucleus1')
    # cmds.setAttr(surface + '.inheritsTransform', 0)

    for C in range(1, 8):
        cmds.delete('curve' + str(C))
    fol_grp = cmds.rename('hairSystem1Follicles', name + nc['follicle'] + nc['group'])

    follicles = cmds.ls(name + nc['follicle'] + nc['group'], dag=True, type='follicle')

    for num, fol in enumerate(follicles[1:-1]):
        guide = mt.create_joint_guide(name = name + '_' + str(num))
        cmds.parent(guide, fol)
        cmds.setAttr('{}.translateX'.format(guide), 0)
        cmds.setAttr('{}.translateY'.format(guide), 0)
        cmds.setAttr('{}.translateZ'.format(guide), 0)

    cmds.delete(cmds.listRelatives(follicles[0], p=True), cmds.listRelatives(follicles[-1], p=True))

    cmds.parent(surface, block)
    cmds.parent(fol_grp, block)

    cmds.select(block)

    print('{} Created Successfully'.format(name))


#create_brow_block()

#-------------------------

def build_brows_advance_block():

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

    joints_guides = []
    fol_guides = []
    for num in range(5):
        jnt_guide = '{}_{}{}'.format(name, num, nc['guide'])
        joints_guides.append(jnt_guide)
        fol_guides.append(cmds.listRelatives(jnt_guide, p=True)[0])

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
    main_ctrl_attr = mt.new_enum(input=guide_attrs_position, name='browsMainCtrls', enums='Hide:Show', keyable=False)
    mid_ctrl_attr = mt.new_enum(input=guide_attrs_position, name='browsMidCtrls', enums='Hide:Show', keyable=False)
    show_tweeks_attr = mt.new_enum(input=guide_attrs_position, name='browsTweekCtrls', enums='Hide:Show', keyable=False)

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
        surface_shape = cmds.listRelatives(surface, s=True)[0]
        surface_shape = cmds.rename(surface_shape, surface + 'Shape')
        cmds.setAttr(surface + '.inheritsTransform', 0)

        tweek_joints = []
        tweek_controllers = []
        follicles = []

        tweek_ctrl_grp = cmds.group(em=True, n='{}_Tweeks{}{}'.format(name, nc['ctrl'], nc['group']))

        clean_ctrl_grp = cmds.group(em=True, name=name + nc['ctrl'] + nc['group'])
        clean_rig_grp = cmds.group(em=True, name=name + '_Rig' + nc['group'])


        #Create folicles in same pos as the guide
        cmds.select(surface + 'Shape')
        mel.eval("createHair {} 1 10 0 0 0 0 5 0 1 2 1;".format(5))

        cmds.delete('hairSystem1', 'pfxHair1', 'nucleus1')
        # cmds.setAttr(surface + '.inheritsTransform', 0)

        for C in range(1, 6):
            cmds.delete('curve' + str(C))
        fol_grp = cmds.rename('hairSystem1Follicles', name + nc['follicle'] + nc['group'])

        follicles = cmds.ls(name + nc['follicle'] + nc['group'], dag=True, type='follicle')

        #Put a tweek joint in every fol
        for num, guide_jnt in enumerate(joints_guides):
            cmds.select(cl=True)
            jnt = cmds.joint(n='{}_{}{}'.format(name, num, nc['joint']))
            cmds.delete(cmds.parentConstraint(guide_jnt, jnt))
            tweek_joints.append(jnt)

        #Put fol as same as guides
        params_u = []
        params_v = []
        num=0
        for fol,fol_guide in zip(follicles, fol_guides):
            #Get U V Values
            closest_point_on_sruface_node = cmds.createNode('closestPointOnSurface', n=name + fol + '_CPOS')
            decompose_matrix = cmds.createNode('decomposeMatrix', n=name + fol + '_decomposeMatrix')

            cmds.connectAttr('{}.worldSpace[0]'.format(surface),
                             '{}.inputSurface'.format(closest_point_on_sruface_node))
            cmds.connectAttr('{}.worldMatrix[0]'.format(tweek_joints[num]), '{}.inputMatrix'.format(decompose_matrix))
            cmds.connectAttr('{}.outputTranslate'.format(decompose_matrix),
                             '{}.inPosition'.format(closest_point_on_sruface_node))
            print(closest_point_on_sruface_node)
            # cmds.connectAttr('{}.result.parameterU'.format(closest_point_on_sruface_node), '{}.translate'.format(driver_locator))

            u = cmds.getAttr('{}.result.parameterU'.format(closest_point_on_sruface_node))
            v = cmds.getAttr('{}.result.parameterV'.format(closest_point_on_sruface_node))

            cmds.setAttr('{}.parameterU'.format(fol), u)
            cmds.setAttr('{}.parameterV'.format(fol), v)

            params_u.append(['{}.parameterU'.format(fol), u])
            params_v.append(['{}.parameterV'.format(fol), v])

            cmds.delete(closest_point_on_sruface_node, decompose_matrix)

            #put joint inside fol
            cmds.parent(tweek_joints[num], fol)
            num = num+1

        #Create master locator to control the mult divides with an attr
        master_locator = cmds.spaceLocator(n='{}_Master{}'.format(name,  nc['locator']))[0]
        master_locator_rot = mt.root_grp()[0]
        cmds.delete(cmds.parentConstraint(tweek_joints[2], master_locator_rot))
        fol_multiplayer_attr = mt.new_attr(input=master_locator, name='Div_Movement', min=0, max=100, default=5)

        master_ctrl = mt.curve(input=master_locator,
                            type='cube',
                            rename=True,
                            custom_name=True,
                            name=name + nc['ctrl'],
                            size=ctrl_size)
        mt.assign_color(color=color)
        master_ctrl_root = mt.root_grp()[0]
        mt.match(master_ctrl, master_locator, r=False, t=True)

        cmds.connectAttr('{}.rotate'.format(master_ctrl), '{}.rotate'.format(master_locator))
        cmds.connectAttr('{}.translate'.format(master_ctrl), '{}.translate'.format(master_locator))

        cmds.select(
        '{}.cv[0]'.format(master_ctrl),
        '{}.cv[3:5]'.format(master_ctrl),
        '{}.cv[11:12]'.format(master_ctrl),
        '{}.cv[14:15]'.format(master_ctrl),
        )
        temp_cluster=cmds.cluster()
        cmds.delete(cmds.pointConstraint(fol_guides[0],temp_cluster))
        cmds.select(
        '{}.cv[1:2]'.format(master_ctrl),
        '{}.cv[6:10]'.format(master_ctrl),
        '{}.cv[13]'.format(master_ctrl),
        )
        temp_clusterB=cmds.cluster()
        cmds.delete(cmds.pointConstraint(fol_guides[-1],temp_clusterB))
        cmds.delete(master_ctrl, ch=True)

        local_locators = []
        world_locators = []

        #Create system per joint
        for num, tweek_joint in enumerate(tweek_joints):
            # Create driver locator to drive without afecting local space of joint
            local_fol_locator = cmds.spaceLocator(n='{}_LocalSpace_{}{}'.format(name, num, nc['locator']))[0]
            cmds.delete(cmds.parentConstraint(tweek_joint, local_fol_locator))
            local_loc_root_grp, local_loc_auto_grp = mt.root_grp(autoRoot=True)
            local_locators.append(local_fol_locator)

            world_fol_locator = cmds.spaceLocator(n='{}_WorldSpace_{}{}'.format(name, num, nc['locator']))[0]
            cmds.delete(cmds.pointConstraint(tweek_joint, world_fol_locator))
            world_loc_root_grp = mt.root_grp()[0]
            world_locators.append(world_fol_locator)
            cmds.parent(world_loc_root_grp, clean_rig_grp)

            cmds.parent(local_loc_root_grp, master_locator)

            #Local drives world
            cmds.parentConstraint(local_fol_locator, world_fol_locator, mo=True)

            #Connect world locator to follicle
            mdu = mt.connect_md_node(in_x1='{}.translateX'.format(world_fol_locator),
                               in_x2=fol_multiplayer_attr,
                               out_x=params_u[num][0],
                               mode='divide', name='',
                               force=True)

            mdv = mt.connect_md_node(in_x1='{}.translateY'.format(world_fol_locator),
                               in_x2=fol_multiplayer_attr,
                               out_x=params_v[num][0],
                               mode='divide', name='',
                               force=True)

            dlu = mt.replace_connection_with_doublelinear(input=params_u[num][0].split('.')[0],
                                                         attr=params_u[num][0].split('.')[1],
                                                         name=tweek_joint+'_UFolMove_DL')
            cmds.setAttr('{}.input2'.format(dlu), params_u[num][1])

            dlv = mt.replace_connection_with_doublelinear(input=params_v[num][0].split('.')[0],
                                                         attr=params_v[num][0].split('.')[1],
                                                         name=tweek_joint+'_VFolMove_DL')
            cmds.setAttr('{}.input2'.format(dlv), params_v[num][1])

            #Create tweek controllers
            # Create controller
            ctrl = mt.curve(input=tweek_joint,
                            type='square',
                            rename=True,
                            custom_name=True,
                            name=tweek_joint.replace(nc['joint'], nc['ctrl']),
                            size=ctrl_size / 2)
            tweek_controllers.append(ctrl)
            mt.assign_color(color=color)
            ctrl_root = mt.root_grp()[0]
            mt.match(ctrl_root, tweek_joint, r=False, t=True)

            cmds.parent(ctrl_root, tweek_ctrl_grp)

            # Connect directy to threat as local
            cmds.connectAttr('{}.rotate'.format(ctrl), '{}.rotate'.format(tweek_joint))
            cmds.connectAttr('{}.translate'.format(ctrl), '{}.translate'.format(tweek_joint))
            cmds.connectAttr('{}.scale'.format(ctrl), '{}.scale'.format(tweek_joint))
            cmds.connectAttr('{}.rotate'.format(cmds.listRelatives(tweek_joint, p=True)[0]), '{}.rotate'.format(ctrl_root))
            cmds.connectAttr('{}.translate'.format(cmds.listRelatives(tweek_joint, p=True)[0]), '{}.translate'.format(ctrl_root))


        #Create the system for main/mid 5 sphere controllers

        #Create a ribbon with curve position
        curve = cmds.curve(d=1, p=[cmds.xform(tweek_joints[0], t=True, q=True, ws=True),
                                   cmds.xform(tweek_joints[1], t=True, q=True, ws=True),
                                   cmds.xform(tweek_joints[2], t=True, q=True, ws=True),
                                   cmds.xform(tweek_joints[3], t=True, q=True, ws=True),
                                   cmds.xform(tweek_joints[4], t=True, q=True, ws=True)],
                                   k=[0,1,2,3,4], n= "{}_Ribbon".format(name))

        ribbon_surface = cmds.bevel(curve, ch=False, w=0, d=0.01, ed=0, ct=2, bst=1, n=curve + nc['nurb'], js=True)[
            0]
        ribbon_surface = cmds.rebuildSurface(ribbon_surface, ch=False, dv=3, du=3, su=0, sv=4, kr=True)[0]
        cmds.delete(curve)
        cmds.select(ribbon_surface)

        mel.eval("createHair 1 5 10 0 0 1 0 5 0 1 2 1;")

        cmds.delete('hairSystem1', 'pfxHair1', 'nucleus1')

        ribbon_fol_grp = cmds.rename('hairSystem1Follicles', curve + '_Ribbon' + nc['follicle'] + nc['group'])
        cmds.parent(ribbon_fol_grp, clean_rig_grp)
        ribbon_follicles = []
        main_ctrls =[]
        driver_joints = []
        driver_locs = []
        for num, fol in enumerate(cmds.listRelatives(ribbon_fol_grp, c=True)):
            print(num, fol)
            gc = cmds.listRelatives(fol, c=True)
            cmds.delete(gc[-1])
            ribbon_follicles.append(fol)

            driver_loc = cmds.spaceLocator(name=name+'Driver'+str(num)+'_Main'+nc['locator'])[0]
            driver_loc_root = mt.root_grp()[0]
            mt.match(driver_loc_root, local_locators[num], r=True, t=True)
            driver_locs.append(driver_loc)

            #Create mid main controllers
            ctrl = mt.curve(input=local_locators[num],
                            type='sphere',
                            rename=True,
                            custom_name=True,
                            name=name+'_Driver'+str(num)+'_Main'+nc['ctrl'],
                            size=ctrl_size/2)
            mt.assign_color(color=color)
            ctrl_root = mt.root_grp()[0]
            main_ctrls.append(ctrl)
            mt.match(ctrl_root, local_locators[num], r=True, t=True)

            cmds.connectAttr('{}.rotate'.format(ctrl), '{}.rotate'.format(driver_loc))
            cmds.connectAttr('{}.translate'.format(ctrl), '{}.translate'.format(driver_loc))
            cmds.connectAttr('{}.scale'.format(ctrl), '{}.scale'.format(driver_loc))

            cmds.select(cl=True)
            driver_joint = cmds.joint(n=name+'_Driver'+str(num)+'_Main'+nc['joint'])
            driver_joint_root = mt.root_grp()[0]
            mt.match(driver_joint, fol, r=False, t=True)
            cmds.parent(driver_joint_root, driver_loc)
            driver_joints.append(driver_joint)

            cmds.parentConstraint(fol, cmds.listRelatives(local_locators[num], p=True), mo=True)

            cmds.parent(driver_loc_root, master_locator)
            cmds.parent(ctrl_root, master_ctrl)

        #Manage Rotation by doing an offset grp over the tweek joint and the tweek ctrl
        #Also translate Z
        #L_BrowDriver4_Main_Loc controlls the grps rotate and tz
        for num, ctrl in enumerate(main_ctrls):
            offset_jnt = mt.root_grp(input=tweek_joints[num], custom=True, custom_name='Offset')[0]
            offset_tweek_ctrl = mt.root_grp(input=tweek_controllers[num], custom=True, custom_name='Offset')[0]

            cmds.connectAttr('{}.rotate'.format(cmds.listRelatives(local_locators[num],p=True)[0]), '{}.rotate'.format(offset_jnt))
            cmds.connectAttr('{}.rotate'.format(cmds.listRelatives(local_locators[num],p=True)[0]), '{}.rotate'.format(offset_tweek_ctrl))
            cmds.connectAttr('{}.translateZ'.format(cmds.listRelatives(local_locators[num],p=True)[0]), '{}.translateZ'.format(offset_jnt))
            cmds.connectAttr('{}.translateZ'.format(cmds.listRelatives(local_locators[num],p=True)[0]), '{}.translateZ'.format(offset_tweek_ctrl))


        cmds.select(driver_joints, ribbon_surface)
        skin = cmds.skinCluster(toSelectedBones=True)[0]

        #Switches vis
        cmds.setAttr(main_ctrl_attr, 1)

        for ctrl in tweek_controllers:
            shape = cmds.listRelatives(ctrl, s=True)[0]
            cmds.connectAttr(show_tweeks_attr, '{}.v'.format(shape))
        for ctrl in [main_ctrls[1], main_ctrls[3]]:
            shape = cmds.listRelatives(ctrl, s=True)[0]
            cmds.connectAttr(mid_ctrl_attr, '{}.v'.format(shape))
        for ctrl in [main_ctrls[0], main_ctrls[2], main_ctrls[4], master_ctrl]:
            shape = cmds.listRelatives(ctrl, s=True)[0]
            cmds.connectAttr(main_ctrl_attr, '{}.v'.format(shape))


        #clean a bit
        cmds.parent(ribbon_surface, fol_grp, master_locator_rot, surface, clean_rig_grp)
        cmds.parent(master_ctrl_root, tweek_ctrl_grp, clean_ctrl_grp)

        #mirror
        if cmds.getAttr('{}.Mirror'.format(config), asString=True) == 'Right_Only':

            clean_ctrl_grp = mt.mirror_group(clean_ctrl_grp, world=True)
            clean_rig_grp = mt.mirror_group(clean_rig_grp, world=True)

            cmds.parent(clean_ctrl_grp, setup['base_groups']['control'] + nc['group'])
            cmds.parent(clean_rig_grp, '{}{}'.format(setup['rig_groups']['misc'], nc['group']))

        elif cmds.getAttr('{}.Mirror'.format(config), asString=True) == 'True':

            if str(name).startswith(nc['right']):
                clean_ctrl_grp = mt.mirror_group(clean_ctrl_grp, world=True)
                clean_rig_grp = mt.mirror_group(clean_rig_grp, world=True)

                cmds.parent(clean_ctrl_grp, setup['base_groups']['control'] + nc['group'])
                cmds.parent(clean_rig_grp, '{}{}'.format(setup['rig_groups']['misc'], nc['group']))

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

