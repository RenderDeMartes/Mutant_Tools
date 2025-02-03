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

TAB_FOLDER = '002_Biped'
PYBLOCK_NAME = 'exec_spine'

# ---------------------------------------------

def create_spine_block(name='Spine'):

    # Read name conventions as nc[''] and setup as seup['']
    PATH = os.path.dirname(__file__)
    PATH = Path(PATH)
    PATH_PARTS = PATH.parts[:-2]
    FOLDER = ''
    for f in PATH_PARTS:
        FOLDER = os.path.join(FOLDER, f)

    MODULE_FILE = os.path.join(os.path.dirname(__file__), '001_SimpleSpine.json')
    with open(MODULE_FILE) as module_file:
        module = json.load(module_file)

    nc, curve_data, setup = mt.import_configs()

    name = mt.ask_name(text=module['Name'])
    if cmds.objExists('{}{}'.format(name, nc['module'])):
        cmds.warning('Name already exists.')
        return ''

    block = mt.create_block(name=name, icon='SimpleSpine', attrs=module['attrs'], build_command=module['build_command'],
                            import_command=module['import'])
    config = block[1]
    block = block[0]

    cmds.select(cl=True)
    spineRoot_guide = mt.create_joint_guide(name=name + '_Root')
    cmds.parent(spineRoot_guide, block)
    spineBase_guide = mt.create_joint_guide(name=name + '_Base')
    cmds.move(0, 2, 0)
    spineBelly_guide = mt.create_joint_guide(name=name + '_Belly')
    cmds.move(0, 4, 0)
    spineChest_guide = mt.create_joint_guide(name=name + '_Chest')
    cmds.move(0, 6, 0)
    spineEnd_guide = mt.create_joint_guide(name=name + '_End')
    cmds.move(0, 8, 0)

    cmds.parent(spineBase_guide, spineRoot_guide)
    cmds.parent(spineBelly_guide, spineBase_guide)
    cmds.parent(spineChest_guide, spineBelly_guide)
    cmds.parent(spineEnd_guide, spineChest_guide)

    cmds.select(block)
    # mt.orient_joint(input = spineBase_guide)
    # cmds.setAttr("{}.jointOrientX".format(spineInv_guide), 0)
    # cmds.setAttr("{}.jointOrientY".format(spineInv_guide), 0)
    # cmds.setAttr("{}.jointOrientZ".format(spineInv_guide), 0)

    print('{} Created Successfully'.format(name))


# create_spine_block()

# -------------------------

def build_spine_block():

    nc, curve_data, setup = mt.import_configs()

    mt.check_is_there_is_base()

    block = cmds.ls(sl=True)
    config = cmds.listConnections(block)[1]
    block = block[0]
    guide = cmds.listRelatives(block, c=True)[0]
    name = block.replace(nc['module'], '')

    ctrl_size = cmds.getAttr('{}.CtrlSize'.format(config))
    # cmds.getAttr('{}.AttrName'.format(config), asString = True)

    # groups for later cleaning
    clean_ctrl_grp = cmds.group(em=True, name=name + nc['ctrl'] + nc['group'])
    clean_rig_grp = cmds.group(em=True, name=name + '_Rig' + nc['group'])

    # orient the joints
    mt.orient_joint(input=guide)
    new_guide = mt.duplicate_and_remove_guides(guide)

    cmds.setAttr('{}_End{}.jointOrientX'.format(name, nc['joint']), 0)
    cmds.setAttr('{}_End{}.jointOrientY'.format(name, nc['joint']), 0)
    cmds.setAttr('{}_End{}.jointOrientZ'.format(name, nc['joint']), 0)

    # use this locator in case parent is set to new locator
    if cmds.getAttr('{}.SetParent'.format(config)) == 'new_locator':
        block_parent = cmds.spaceLocator(n='{}'.format(str(block).replace(nc['module'], '_Parent' + nc['locator'])))
    else:
        block_parent = cmds.getAttr('{}.SetParent'.format(config))

    game_parent = cmds.getAttr('{}.SetGameParent'.format(config))

    spine_joints = [new_guide,
                    '{}_Base{}'.format(name, nc['joint']),
                    '{}_Belly{}'.format(name, nc['joint']),
                    '{}_Chest{}'.format(name, nc['joint']),
                    '{}_End{}'.format(name, nc['joint']),
                    ]

    back_distance = cmds.getAttr(spine_joints[2] + '.translateX')

    # build
    # create curve
    # curve -d 3 -p -4.975538 -0.0440359 0 -p -4.973703 0.623842 0 -p -4.970034 1.959596 0 -p -4.988382 3.471494 0 -p -4.997556 4.227444 0 -k 0 -k 0 -k 0 -k 1 -k 2 -k 2 -k 2 ;
    root_pos = cmds.xform(spine_joints[0], q=True, ws=True, t=True)
    base_pos = cmds.xform(spine_joints[1], q=True, ws=True, t=True)
    belly_pos = cmds.xform(spine_joints[2], q=True, ws=True, t=True)
    chest_pos = cmds.xform(spine_joints[3], q=True, ws=True, t=True)
    end_pos = cmds.xform(spine_joints[4], q=True, ws=True, t=True)

    spine_cv = cmds.curve(d=3, p=[root_pos, base_pos, belly_pos, chest_pos, end_pos], k=[0, 0, 0, 1, 2, 2, 2],
                          n=name + '_Main' + nc['curve'])
    spine_cv = cmds.rebuildCurve(keepRange=0, ch=False, rebuildType=3, kcp=1, kep=1, kt=0, s=4, d=3, tol=0.01)[0]
    spine_cv_shape = cmds.listRelatives(spine_cv, s=True)[0]
    cmds.setAttr('{}.inheritsTransform'.format(spine_cv), 0)

    # create locator clusters
    cluster_locators = []
    cluster_locs_grp = cmds.group(em=True, n=name + '_Cls' + nc["locator"] + nc['group'])
    spine_ik_ctrls = []

    for num, jnt in enumerate(spine_joints):
        # create cluster locators
        loc = cmds.spaceLocator(n=jnt.replace(nc['joint'], '_Cls' + nc['locator']))[0]
        cmds.parent(loc, cluster_locs_grp)
        cluster_locators.append(loc)
        cmds.delete(cmds.pointConstraint(jnt, loc, mo=False))
        decomposeNode = cmds.createNode('decomposeMatrix', n=loc.replace(nc['locator'], '_decomposeMatrix'))
        cmds.connectAttr("{}.worldMatrix[0]".format(loc), "{}.inputMatrix".format(decomposeNode))
        cmds.connectAttr('{}.outputTranslate'.format(decomposeNode), '{}.controlPoints[{}]'.format(spine_cv_shape, num))

        # create ik controllers
        type = 'sphere'
        if 'Belly' in jnt:
            type = 'circle_point'
            custom_name = jnt.replace(nc['joint'], '_IK' + nc['ctrl'])
            hide_shape=False
        else:
            type = 'locator'
            custom_name = jnt.replace(nc['joint'], '_IK' + nc['locator'])
            hide_shape = True
        ctrl = mt.curve(input=jnt,
                        type=type,
                        rename=True,
                        custom_name=True, name=custom_name,
                        size=ctrl_size,
                        )
        cmds.delete(cmds.pointConstraint(jnt, ctrl))
        #cmds.move(0, 0, back_distance, '{}.cv[0:101]'.format(ctrl), r=True)

        mt.assign_color(ctrl, 'yellow')
        root = mt.root_grp(input=ctrl)
        cmds.parentConstraint(ctrl, loc, mo=True)
        spine_ik_ctrls.append(ctrl)

        if hide_shape:
            cmds.setAttr(cmds.listRelatives(ctrl, s=True)[0]+'.v', 0)
            cmds.setAttr("{}.visibility".format(ctrl), lock=False)
            cmds.setAttr(ctrl + '.v', 0)
            cmds.setAttr("{}.visibility".format(ctrl), lock=True)

    # Belly is going to be purple
    mt.assign_color(spine_ik_ctrls[2], 'purple')


    # Create FK controllers
    base_ik_ctrl = mt.curve(input=spine_joints[0],
                            type='pringle_point',
                            rename=True,
                            custom_name=True, name=name + '_Bottom_Ik' + nc['ctrl'],
                            size=ctrl_size * 1.5
                            )
    cmds.rotate(0, 0, 0)
    base_ik_ctrl_root = mt.root_grp()
    mt.assign_color(base_ik_ctrl, 'purple')
    mt.match(base_ik_ctrl_root, spine_joints[1], r=False)

    base_ctrl = mt.curve(input=spine_joints[1],
                         type='square',
                         rename=True,
                         custom_name=True, name=spine_joints[1].replace(nc['joint'], '_FK' + nc['ctrl']),
                         size=ctrl_size * 1.5
                         )
    cmds.rotate(0, 0, 0)
    base_ctrl_root = mt.root_grp()
    mt.assign_color(base_ctrl, 'lightBlue')
    mt.match(base_ctrl_root, spine_joints[1], r=False)

    belly_ctrl = mt.curve(input=spine_joints[2],
                          type='square',
                          rename=True,
                          custom_name=True, name=spine_joints[2].replace(nc['joint'], '_FK' + nc['ctrl']),
                          size=ctrl_size * 1.5
                          )
    cmds.rotate(0, 0, 0)
    belly_ctrl_root = mt.root_grp()
    mt.assign_color(belly_ctrl, 'lightBlue')
    mt.match(belly_ctrl_root, spine_joints[2], r=False)

    chest_ctrl_fk = mt.curve(input=spine_joints[3],
                          type='square',
                          rename=True,
                          custom_name=True, name=spine_joints[3].replace(nc['joint'], '_FK' + nc['ctrl']),
                          size=ctrl_size * 1.5
                          )
    cmds.rotate(0, 0, 0)
    chest_fk_ctrl_root = mt.root_grp()
    mt.assign_color(chest_ctrl_fk, 'green')
    mt.match(chest_fk_ctrl_root, spine_joints[3], r=False)

    chest_ctrl = mt.curve(input=spine_joints[4],
                          type='pringle_point',
                          rename=True,
                          custom_name=True, name=spine_joints[3].replace(nc['joint'], '_Top_IK' + nc['ctrl']),
                          size=ctrl_size * 1.5
                          )
    cmds.rotate(0, 0, 0)
    chest_ctrl_root = mt.root_grp()
    mt.assign_color(chest_ctrl, 'purple')
    mt.match(chest_ctrl_root, spine_joints[3], r=False)

    # Create hierarchy
    cmds.parent(belly_ctrl_root, base_ctrl)
    cmds.parent(chest_fk_ctrl_root, belly_ctrl)
    cmds.parent(chest_ctrl_root, chest_ctrl_fk)

    cmds.parent(cmds.listRelatives(spine_ik_ctrls[0], p=True), base_ik_ctrl)
    cmds.parent(cmds.listRelatives(spine_ik_ctrls[1], p=True), base_ik_ctrl)
    cmds.parent(cmds.listRelatives(spine_ik_ctrls[2], p=True), base_ctrl)
    cmds.parent(cmds.listRelatives(spine_ik_ctrls[3], p=True), chest_ctrl)
    cmds.parent(cmds.listRelatives(spine_ik_ctrls[4], p=True), chest_ctrl)

    # create locators that follows and connect to joints
    # setup to find parameters
    temp_loc = cmds.spaceLocator()[0]
    near_point_node = cmds.createNode('nearestPointOnCurve')
    cmds.connectAttr("{}.worldSpace[0]".format(spine_cv_shape), '{}.inputCurve'.format(near_point_node))
    cmds.connectAttr("{}.translate".format(temp_loc), "{}.inPosition".format(near_point_node))

    parent_locators = []
    for jnt in spine_joints:
        # position temp loc to find parameters
        cmds.delete(cmds.pointConstraint(jnt, temp_loc))
        param = cmds.getAttr('{}.result.parameter'.format(near_point_node))

        parent_locator = cmds.spaceLocator(n=jnt.replace(nc['joint'], '_Parent' + nc['locator']))[0]
        parent_locators.append(parent_locator)
        onCurveInfo = cmds.createNode('pointOnCurveInfo', n=jnt.replace(nc['joint'], '_POCI'))
        cmds.connectAttr("{}.worldSpace[0]".format(spine_cv_shape), '{}.inputCurve'.format(onCurveInfo))
        cmds.setAttr('{}.parameter'.format(onCurveInfo), param)
        cmds.connectAttr('{}.result.position'.format(onCurveInfo), '{}.translate'.format(parent_locator))
        cmds.parentConstraint(parent_locator, jnt, mo=True)

    # delete setup to find parameters
    cmds.delete(temp_loc, near_point_node)
    parent_locators_grp = cmds.group(parent_locators, n=name + '_Parents' + nc['locator'] + nc['group'])
    cmds.parent(parent_locators_grp, clean_rig_grp)
    cmds.setAttr('{}.inheritsTransform'.format(parent_locators_grp), 0)

    # Aim and Twists
    twist_locators = []
    twist_locators_roots = []
    twist_locators_grp = cmds.group(em=True, n=name + '_Twists' + nc['locator'] + nc['group'])
    for loc in parent_locators:
        twist_loc = cmds.spaceLocator(n=loc.replace('Parent', 'Twist'))[0]
        root, auto = mt.root_grp(twist_loc, autoRoot=True)
        twist_locators.append(twist_loc)
        cmds.delete(cmds.pointConstraint(loc, twist_loc, mo=False))
        cmds.move(0, 0, back_distance * -2, r=True)
        cmds.parent(root, twist_locators_grp)
        twist_locators_roots.append(root)

    cmds.parent(twist_locators_grp, clean_rig_grp)

    # twist joints hierarchies
    cmds.parentConstraint(chest_ctrl, twist_locators_roots[-1], mo=True)
    cmds.parentConstraint(base_ik_ctrl, twist_locators_roots[0], mo=True)
    mid_parent = cmds.parentConstraint(twist_locators[-1], twist_locators[0], twist_locators_roots[2], mo=True)[0]
    cmds.setAttr('{}.interpType'.format(mid_parent), 2)
    bot_mid_parent = cmds.parentConstraint(twist_locators[0], twist_locators[2], twist_locators_roots[1], mo=True)[0]
    cmds.setAttr('{}.interpType'.format(bot_mid_parent), 2)
    top_mid_parent = cmds.parentConstraint(twist_locators[-1], twist_locators[2], twist_locators_roots[3], mo=True)[0]
    cmds.setAttr('{}.interpType'.format(top_mid_parent), 2)


    # aims
    cmds.aimConstraint(parent_locators[1], parent_locators[0], aimVector=(0, 1, 0), upVector=(0, 0, -1),
                       worldUpType="object", worldUpObject=twist_locators[0])
    cmds.aimConstraint(parent_locators[2], parent_locators[1], aimVector=(0, 1, 0), upVector=(0, 0, -1),
                       worldUpType="object", worldUpObject=twist_locators[1])
    cmds.aimConstraint(parent_locators[3], parent_locators[2], aimVector=(0, 1, 0), upVector=(0, 0, -1),
                       worldUpType="object", worldUpObject=twist_locators[2])
    cmds.aimConstraint(parent_locators[4], parent_locators[3], aimVector=(0, 1, 0), upVector=(0, 0, -1),
                       worldUpType="object", worldUpObject=twist_locators[3])
    # create up vector for last loc
    up_loc = cmds.spaceLocator(n=name + '_UpVector' + nc['locator'])[0]
    cmds.parent(up_loc, clean_rig_grp)
    cmds.delete(cmds.parentConstraint(spine_joints[4], up_loc, mo=False))
    cmds.move(0, 1, 0, r=True)
    cmds.parentConstraint(chest_ctrl, up_loc, mo=True)
    cmds.aimConstraint(up_loc, parent_locators[4], aimVector=(0, 1, 0), upVector=(0, 0, -1), worldUpType="object",
                       worldUpObject=twist_locators[4])

    # Share attrs locator
    all_controllers = [chest_ctrl, belly_ctrl, base_ctrl, base_ik_ctrl] + spine_ik_ctrls
    for ctrl in all_controllers:
        cmds.select(ctrl)
        if cmds.objectType(ctrl) == 'transform':
            spine_attrs_loc = mt.shape_with_attr(input='', obj_name='{}_Attrs'.format(name), attr_name='Test').split('.')[0]
    new_config_attr_loc = cmds.spaceLocator(n=name+'_Config'+nc['locator'])[0]

    mel.eval('catch (`deleteAttr -attribute "Test" "{}|Spine_Attrs_Loc"`);'.format(base_ik_ctrl))
    show_ik_ctrls_attr = mt.new_enum(input=spine_attrs_loc, name='ikCtrls', enums='Hide:Show', keyable=False)
    #show_extra_ik_ctrls_attr = mt.new_enum(input=spine_attrs_loc, name='ikCtrlsExtra', enums='Hide:Show', keyable=False)
    show_fk_ctrls_attr = mt.new_enum(input=spine_attrs_loc, name='fkCtrls', enums='Hide:Show', keyable=False)
    cmds.setAttr(show_ik_ctrls_attr, 1)
    #cmds.setAttr(show_extra_ik_ctrls_attr, 0)
    cmds.setAttr(show_fk_ctrls_attr, 1)

    for ctrl in spine_ik_ctrls[2:-2] + [base_ik_ctrl, chest_ctrl]:
        shape = cmds.listRelatives(ctrl, s=True)[0]
        cmds.connectAttr(show_ik_ctrls_attr, '{}.v'.format(shape))
    # for ctrl in [spine_ik_ctrls[0], spine_ik_ctrls[-1], spine_ik_ctrls[1], spine_ik_ctrls[-2]]:
    #     shape = cmds.listRelatives(ctrl, s=True)[0]
    #     cmds.connectAttr(show_extra_ik_ctrls_attr, '{}.v'.format(shape), f=True)
    for ctrl in [belly_ctrl, base_ctrl, chest_ctrl_fk]:
        shape = cmds.listRelatives(ctrl, s=True)[0]
        cmds.connectAttr(show_fk_ctrls_attr, '{}.v'.format(shape))

    # Belly IK Ctrl offsets other Iks
    mt.line_attr(input=new_config_attr_loc, name='MidOffsets')

    mid01_attr = mt.new_attr(input=new_config_attr_loc, name='Mid02Follow', min=0, max=1, default=0.5)
    mid02_attr = mt.new_attr(input=new_config_attr_loc, name='Mid01Follow', min=0, max=1, default=0.5)

    pc2 = cmds.parentConstraint(spine_ik_ctrls[0], spine_ik_ctrls[2], cmds.listRelatives(spine_ik_ctrls[1], p=True)[0], mo=True)[0]
    cmds.setAttr('{}.interpType'.format(pc2), 2)
    cmds.connectAttr(mid02_attr, '{}.{}W0'.format(pc2, spine_ik_ctrls[0]))

    reverse_node2 = cmds.createNode('reverse', n=spine_ik_ctrls[1] + '_Reverse')
    cmds.connectAttr(mid02_attr, '{}.input.inputX'.format(reverse_node2))
    cmds.connectAttr('{}.output.outputX'.format(reverse_node2), '{}.{}W1'.format(pc2, spine_ik_ctrls[2]))

    pc1 = cmds.parentConstraint(spine_ik_ctrls[2], spine_ik_ctrls[4], cmds.listRelatives(spine_ik_ctrls[3], p=True)[0], mo=True)[0]
    cmds.setAttr('{}.interpType'.format(pc1), 2)
    cmds.connectAttr(mid01_attr, '{}.{}W0'.format(pc1, spine_ik_ctrls[2]))
    reverse_node1 = cmds.createNode('reverse', n=spine_ik_ctrls[3] + '_Reverse')
    cmds.connectAttr(mid01_attr, '{}.input.inputX'.format(reverse_node1))
    cmds.connectAttr('{}.output.outputX'.format(reverse_node1), '{}.{}W1'.format(pc1, spine_ik_ctrls[4]))

    # Volumen Preservation
    curve_info_node = cmds.createNode('curveInfo', n=name + '_CurveInfo')
    cmds.connectAttr('{}.worldSpace[0]'.format(spine_cv_shape), '{}.inputCurve'.format(curve_info_node))
    curve_lenght = cmds.getAttr('{}.arcLength'.format(curve_info_node))

    #Normalize scale
    normalize_loc = cmds.spaceLocator(n=name + '_NormalScale' + nc['locator'])[0]
    cmds.connectAttr('Global_Ctrl.scale', normalize_loc+'.scale')
    normal_md = mt.connect_md_node(in_x1="{}.arcLength".format(curve_info_node), in_x2=str(normalize_loc) + '.scaleX',
                                     out_x='', mode='divide', name='{}_Normalize'.format(name))
    cmds.parent(normalize_loc, clean_rig_grp)

    mt.line_attr(input=new_config_attr_loc, name='Squash')

    squash_attrs = []
    for jnt in reversed(spine_joints):
        clean_name = jnt.replace(name, '').replace(nc['joint'], '') + 'Squash'
        squash_attr = mt.new_attr(input=new_config_attr_loc, name=clean_name, min=0, max=1, default=1)
        squash_attrs.append(squash_attr)
        cmds.setAttr(squash_attr, 1)

        remap_node = cmds.createNode('remapValue', name=jnt + '_RemapValue')
        cmds.setAttr(remap_node + '.outputMin', 1)
        md = mt.connect_md_node(in_x1=curve_lenght, in_x2=normal_md+'.output.outputX',
                                out_x='{}.outputMax'.format(remap_node), mode='divide')
        cmds.connectAttr('{}.outColor.outColorR'.format(remap_node), '{}.scaleY'.format(jnt))
        cmds.connectAttr('{}.outColor.outColorR'.format(remap_node), '{}.scaleZ'.format(jnt))
        cmds.connectAttr(squash_attr, remap_node + '.inputValue')

    cmds.setAttr(squash_attrs[0], 0)
    cmds.setAttr(squash_attrs[1], 0.25)
    cmds.setAttr(squash_attrs[2], 0.5)
    cmds.setAttr(squash_attrs[3], 1)
    cmds.setAttr(squash_attrs[4], 0)


    #Fix Twist on spine
    cmds.parentConstraint(spine_ik_ctrls[2], cmds.listRelatives(twist_locators[2], p=True)[0], mo=True)

    mt.line_attr(input=new_config_attr_loc, name='Twist')
    mid_twist_attr = mt.new_attr(input=new_config_attr_loc, name='MidTwist', min=0, max=1, default=0.5)

    mid_orient = cmds.orientConstraint(base_ik_ctrl, chest_ctrl, cmds.listRelatives(spine_ik_ctrls[2], p=True)[0],
                                       skip=['x', 'z'], mo=True)[0]
    cmds.setAttr('{}.interpType'.format(mid_orient), 2)
    cmds.connectAttr(mid_twist_attr, '{}.{}W1'.format(mid_orient, chest_ctrl))

    twist_reverse_node = cmds.createNode('reverse', n=mid_orient + '_Reverse')
    cmds.connectAttr(mid_twist_attr, '{}.input.inputX'.format(twist_reverse_node))
    cmds.connectAttr('{}.output.outputX'.format(twist_reverse_node), '{}.{}W0'.format(mid_orient, base_ik_ctrl))

    #Fix scale when rotate chest and base iks
    #Compensate nodes
    #base_root, base_auto = mt.root_grp(input=spine_ik_ctrls[0], autoRoot=True)
    #base_chest, base_chest = mt.root_grp(input=spine_ik_ctrls[-1], autoRoot=True)

    #btm_condition_compensate = cmds.shadingNode('condition', n=spine_ik_ctrls[0] + 'BtmCompensate', au=True)

    #btm_md_compensate = mt.connect_md_node(in_x1=compensate_base_attr,in_x2= '{}.colorIfTrueR'.format(btm_condition_compensate), out_x = '{}.translateY'.format(base_auto), mode = 'multiply')

    #setAttr "condition1.colorIfTrueR" 1;
    #setAttr "condition1.firstTerm" 1;


    # bind joints
    bind_joints = []
    for jnt in spine_joints:
        try:
            cmds.select(bind_joint)
        except:
            pass
        bind_joint = cmds.joint(n=jnt.replace(nc['joint'], nc['joint_bind']))
        cmds.delete(cmds.parentConstraint(jnt, bind_joint, mo=False))
        cmds.delete(cmds.scaleConstraint(jnt, bind_joint, mo=False))
        cmds.makeIdentity(a=True, t=True, s=True, r=True)
        cmds.parentConstraint(jnt, bind_joint, mo=False)
        cmds.scaleConstraint(jnt, bind_joint, mo=True)
        cmds.setAttr('{}.segmentScaleCompensate'.format(bind_joint), 0)
        cmds.setAttr('{}.inheritsTransform'.format(bind_joint), 0)
        #cmds.setAttr('{}.inheritsTransform'.format(jnt), 0)

        # clean bind joints and radius to 1.5
        bind_joints.append(bind_joint)
        cmds.setAttr('{}.radius'.format(bind_joint), 2)

    # fix bind joint end scale
    cmds.connectAttr('Global_Ctrl.scale', bind_joints[-1]+'.scale', f=True)

    # game parents for bind joints
    if cmds.objExists(game_parent):
        cmds.parent(bind_joints[0], game_parent)

    else:
        bind_jnt_grp = '{}{}'.format(setup['rig_groups']['bind_joints'], nc['group'])
        if cmds.objExists(bind_jnt_grp):
            cmds.parent(bind_joints[0], bind_jnt_grp)

    # parent to block parent
    cmds.parentConstraint(block_parent, clean_ctrl_grp, mo=True)
    cmds.scaleConstraint('Global_Ctrl', clean_ctrl_grp, mo=True)
    cmds.scaleConstraint('Global_Ctrl', clean_rig_grp, mo=True)

    # parent system
    cmds.parent(new_config_attr_loc, spine_cv, spine_joints[0], cluster_locs_grp, clean_rig_grp)
    cmds.parent(base_ik_ctrl_root, base_ctrl_root, clean_ctrl_grp)

    cmds.parent(clean_rig_grp, '{}{}'.format(setup['rig_groups']['misc'], nc['group']))
    cmds.parent(clean_ctrl_grp, setup['base_groups']['control'] + nc['group'])

    #Fix twist on chest
    cmds.setAttr('{}_Chest_Twist_Loc_Root_Grp_parentConstraint1.{}_End_Twist_LocW0'.format(name, name), 0)