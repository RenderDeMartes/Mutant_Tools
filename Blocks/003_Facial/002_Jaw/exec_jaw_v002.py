from __future__ import absolute_import
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

#---------------------------------------------

TAB_FOLDER = '003_Facial'
PYBLOCK_NAME = 'exec_jaw'
# GameNames: the MouthGames jaw names, whatever the block is called
GAME_NAME = 'Mouth_Jaw'

# Jaw v002: Jaw v001 + the MouthGames v003 jaw extras.
# - Dynamic pivot: the JawPivot guide sets where the jaw rotates,
#   JawPivot_Ctrl moves it in the scene (Jaw_Ctrl.PivotCtrl shows it).
#   It drives the rotatePivot of the Jaw_Ctrl and of the local rig locator.
# - JawFollow_Null under Jaw_Ctrl: what the Lips v003 / Teeth / Tongue blocks
#   follow (constraints on the ctrl read its rotatePivot and jump when it moves).
# GameMode off = local rig (the jaw joints only see the Jaw_Ctrl channels),
# on = the rig follows SetParent in world space, same as v001.

#Read name conventions as nc[''] and setup as seup['']
PATH = os.path.dirname(__file__)
PATH = Path(PATH)
PATH_PARTS = PATH.parts[:-3]
FOLDER=''
for f in PATH_PARTS:
	FOLDER = os.path.join(FOLDER, f)


#---------------------------------------------

def create_jaw_block(name = 'Jaw'):

    MODULE_FILE = os.path.join(os.path.dirname(__file__), '002_Jaw_v002.json')
    with open(MODULE_FILE) as module_file:
        module = json.load(module_file)
    nc, curve_data, setup = mt.import_configs()
    #name checks and block creation
    name = mt.ask_name(text = module['Name'])
    if cmds.objExists('{}{}'.format(name,nc['module'])):
        cmds.warning('Name already exists.')
        return ''

    block = mt.create_block(name = name, icon = 'Jaw',  attrs = module['attrs'], build_command = module['build_command'], import_command = module['import'])
    config = block[1]
    block = block[0]

    jaw_start = mt.create_joint_guide(name = name)
    cmds.move(0,3,0)
    jaw_upper_lip = mt.create_joint_guide(name = name + 'UpperLip')
    cmds.move(0,1.5,3)
    jaw_lower_lip = mt.create_joint_guide(name = name + 'LowerLip')
    cmds.move(0,1.4,3)

    cmds.parent(jaw_upper_lip, jaw_start)
    cmds.parent(jaw_lower_lip, jaw_start)

    cmds.parent(jaw_start, block)

    # rest position of the jaw rotation pivot (JawPivot_Ctrl starts here)
    jaw_pivot = mt.create_joint_guide(name = name + 'Pivot')
    cmds.move(0,3,0)
    cmds.parent(jaw_pivot, block)

    cmds.select(block)

    print('{} Created Successfully'.format(name))

#create_jaw_block()

#-------------------------

def build_jaw_block():

    nc, curve_data, setup = mt.import_configs()

    mt.check_is_there_is_base()

    block = cmds.ls(sl=True)
    config = cmds.listConnections(block)[1]
    block = block[0]

    # Jaw v001 blocks have no pivot guide, the jaw then rotates on the Jaw guide
    guide = None
    pivot_guide = None
    for child in cmds.listRelatives(block, c=True) or []:
        if not child.endswith(nc['guide']):
            continue
        if child.endswith('Pivot' + nc['guide']):
            pivot_guide = child
        elif guide is None:
            guide = child
    name = guide.replace(nc['guide'], '')

    #use this locator in case parent is set to new locator
    if cmds.getAttr('{}.SetParent'.format(config)) == 'new_locator':
        block_parent = cmds.spaceLocator( n = '{}'.format(str(block).replace(nc['module'],'_Parent' + nc['locator'])))[0]
    else:
        block_parent = cmds.getAttr('{}.SetParent'.format(config))

    ctrl_size = cmds.getAttr('{}.CtrlSize'.format(config))
    ctrl_type = cmds.getAttr('{}.CtrlType'.format(config), asString = True)

    # Game Attrs Compatibility
    if cmds.attributeQuery('GameMode', n=config, exists=True):
        game_mode = cmds.getAttr(config + '.GameMode')
    else:
        game_mode = False
    game_names = cmds.attributeQuery('GameNames', n=config, exists=True) and cmds.getAttr(config + '.GameNames')

    pivot_rest = cmds.xform(pivot_guide or guide, q=True, ws=True, t=True)

    #Build
    new_guide = mt.duplicate_and_remove_guides(guide)
    # GameNames: Mouth_Jaw_Ctrl, Mouth_JawPivot_Ctrl, Mouth_JawFollow_Null,
    # Mouth_Jaw_Bnd... like the MouthGames jaw, so animation transfers
    # between the local and the game rigs
    if game_names and name != GAME_NAME:
        chain = [new_guide] + (cmds.listRelatives(new_guide, ad=True, type='joint', f=True) or [])
        for jnt in sorted(chain, key=lambda n: -cmds.ls(n, l=True)[0].count('|')):
            short = jnt.split('|')[-1]
            if short.startswith(name):
                renamed = cmds.rename(jnt, GAME_NAME + short[len(name):])
                if jnt == new_guide:
                    new_guide = renamed
        name = GAME_NAME
    cmds.select(new_guide)
    jaw_pivot_joint = new_guide
    # by name: listRelatives -ad order is not the guide order
    lip_joints = cmds.listRelatives(new_guide, ad=True, type='joint') or []
    upper_lip = [j for j in lip_joints if 'UpperLip' in j][0]
    lower_lip = [j for j in lip_joints if 'LowerLip' in j][0]
    print([jaw_pivot_joint, upper_lip, lower_lip])

    # v002: jaw frame aimed at the middle of the lips, Y up, like the
    # MouthGames jaw, so Jaw_Ctrl values transfer between local and game rigs
    aim_frame = cmds.createNode('transform', n=name + '_AimFrame_Temp')
    mt.match(aim_frame, jaw_pivot_joint, t=True)
    lips_middle = cmds.spaceLocator()[0]
    cmds.delete(cmds.pointConstraint(upper_lip, lower_lip, lips_middle))
    cmds.delete(cmds.aimConstraint(lips_middle, aim_frame, aimVector=(0, 0, 1), upVector=(0, 1, 0),
                                   worldUpType='vector', mo=False))
    cmds.delete(lips_middle)

    jaw_jnt_root = mt.root_grp(input=jaw_pivot_joint)
    jaw_jnt_mover = cmds.group(em=True, n =jaw_pivot_joint.replace(nc['joint'], 'Mover'+nc['group']))
    cmds.delete(cmds.pointConstraint(jaw_jnt_root, jaw_jnt_mover))
    cmds.parent(jaw_jnt_mover, jaw_jnt_root)
    cmds.parent(jaw_pivot_joint, jaw_jnt_mover)

    cmds.select(cl=True)
    upper_pivot_joint = cmds.joint(n =  name +'UpperLipPivot' + nc['joint'])
    cmds.delete(cmds.parentConstraint(aim_frame, upper_pivot_joint))
    cmds.parent(upper_lip, upper_pivot_joint)

    upper_root = mt.root_grp(upper_pivot_joint)

    global_locator = cmds.spaceLocator(n=name + 'Global' + nc['locator'])[0]
    global_locator_root = mt.root_grp()
    cmds.delete(cmds.parentConstraint(aim_frame, global_locator_root))
    cmds.delete(aim_frame)
    cmds.delete(cmds.parentConstraint(global_locator, upper_root))
    # v002: the jaw joints follow a null under the locator, not the locator:
    # constraints read the locator rotatePivot and would jump when it moves
    global_follow = cmds.createNode('transform', n=name + 'Global_Follow' + nc['null'], p=global_locator)
    cmds.parentConstraint(global_follow, jaw_jnt_root)
    cmds.makeIdentity(upper_pivot_joint, apply=True, r=True)
    cmds.parentConstraint(global_follow, upper_pivot_joint, mo=True)

    #Jaw controller
    jaw_ctrl = mt.curve(input=global_locator,
                          type=ctrl_type,
                          rename=True,
                          custom_name=True,
                          name=name + nc['ctrl'],
                          size=ctrl_size)
    mt.assign_color(color='purple')
    jaw_ctrl_root = mt.root_grp()[0]
    cmds.connectAttr(jaw_ctrl+'.rotate', global_locator+'.rotate')
    cmds.connectAttr('{}.translate'.format(jaw_ctrl), '{}.translate'.format(jaw_jnt_mover))

    # Lips v003 / Teeth / Tongue follow this null, not the ctrl
    jaw_follow = cmds.createNode('transform', n=name + 'Follow' + nc['null'], p=jaw_ctrl)

    #New attrs
    mt.line_attr(input=jaw_ctrl, name='Jaw')
    follow_switch_attr = mt.new_enum(input=jaw_ctrl, name='UpperFollow', enums='On:Off')
    up_limit = mt.new_attr(input=jaw_ctrl, name='UpperLipBreak', min=0, max=90, default=0)
    side_limits = mt.new_attr(input=jaw_ctrl, name='SideBreaks', min=0, max=90, default=0)
    pivot_vis_attr = mt.new_enum(input=jaw_ctrl, name='PivotCtrl', enums='Hide:Show', keyable=False)

    #Limits
    cmds.transformLimits(upper_pivot_joint, erz=[True, True],ery=[True, True], erx=[False, True], rx=[0,0])
    mt.connect_md_node(in_x1=up_limit, in_x2=1, out_x=upper_pivot_joint+'.maxRotLimit.maxRotXLimit', mode='multiply')
    mt.connect_md_node(in_x1=side_limits, in_x2=-1, out_x=upper_pivot_joint+'.minRotLimit.minRotYLimit', mode='multiply')
    mt.connect_md_node(in_x1=side_limits, in_x2=1, out_x=upper_pivot_joint+'.maxRotLimit.maxRotYLimit', mode='multiply')

    mt.hide_attr(input=jaw_ctrl, s=True)

    # Dynamic pivot: JawPivot_Ctrl moves the rotatePivot of the jaw ctrl and
    # of the local rig locator (same frame: the ctrl was made on the locator)
    cmds.select(cl=True)
    jaw_pivot_ctrl = mt.curve(input='',
                              type='sphere',
                              rename=True,
                              custom_name=True,
                              name=name + 'Pivot' + nc['ctrl'],
                              size=ctrl_size / 6.0)
    mt.assign_color(color='yellow')
    jaw_pivot_root = mt.root_grp()[0]
    cmds.parent(jaw_pivot_root, jaw_ctrl_root)
    cmds.xform(jaw_pivot_root, os=True, t=(0, 0, 0), ro=(0, 0, 0))
    # rides the jaw translate (rotatePivot lives in jaw_ctrl's object space)
    jaw_pivot_follow = mt.root_grp(input=jaw_pivot_ctrl, custom=True, custom_name='JawTranslate',
                                   autoRoot=False, replace_nc=False)[0]
    cmds.connectAttr(jaw_ctrl + '.translate', jaw_pivot_follow + '.translate')
    cmds.xform(jaw_pivot_root, ws=True, t=pivot_rest)
    rest_local = cmds.getAttr(jaw_pivot_root + '.translate')[0]
    cmds.xform(jaw_pivot_root, os=True, t=(0, 0, 0))
    cmds.setAttr(jaw_pivot_ctrl + '.translate', 0, 0, 0)
    pivot_sum = cmds.createNode('plusMinusAverage', n=name + 'Pivot_PMA')
    cmds.setAttr(pivot_sum + '.input3D[0]', *rest_local)
    cmds.connectAttr(jaw_pivot_ctrl + '.translate', pivot_sum + '.input3D[1]')
    for node in [jaw_ctrl, global_locator]:
        cmds.connectAttr(pivot_sum + '.output3D', node + '.rotatePivot')
        cmds.connectAttr(pivot_sum + '.output3D', node + '.scalePivot')
    # pivot ctrl shape sits on the pivot: offset its CVs, not its transform
    cmds.move(rest_local[0], rest_local[1], rest_local[2], jaw_pivot_ctrl + '.cv[*]', r=True, os=True)
    mt.hide_attr(jaw_pivot_ctrl, r=True, s=True)
    for shape in cmds.listRelatives(jaw_pivot_ctrl, s=True) or []:
        cmds.connectAttr(pivot_vis_attr, shape + '.v')

    #Auto Front
    jaw_jnt_fixer = auto_grp = mt.root_grp(input = jaw_pivot_joint, custom = True, custom_name = '_Fixer', autoRoot = False, replace_nc = False)[0]
    mt.connect_remap_value(jaw_ctrl+'.rotateX', jaw_jnt_fixer+'.translateX')
    mt.connect_remap_value(jaw_ctrl+'.rotateX', jaw_jnt_fixer+'.translateY')
    mt.connect_remap_value(jaw_ctrl+'.rotateX', jaw_jnt_fixer+'.translateZ')
    mt.connect_remap_value(jaw_ctrl+'.rotateX', jaw_jnt_fixer+'.rotateX')
    mt.connect_remap_value(jaw_ctrl+'.rotateX', jaw_jnt_fixer+'.rotateY')
    mt.connect_remap_value(jaw_ctrl+'.rotateX', jaw_jnt_fixer+'.rotateZ')
    mt.connect_remap_value(jaw_ctrl+'.rotateX', jaw_jnt_fixer+'.scaleX', value=1)
    mt.connect_remap_value(jaw_ctrl+'.rotateX', jaw_jnt_fixer+'.scaleY', value=1)
    mt.connect_remap_value(jaw_ctrl+'.rotateX', jaw_jnt_fixer+'.scaleZ', value=1)

    #On Off Attr
    mt.connect_md_node(in_x1=follow_switch_attr, in_x2=1, out_x=upper_pivot_joint + '.minRotXLimitEnable',
                       mode='multiply')

    #Bind joints
    bind_jnt_grp = '{}{}'.format(setup['rig_groups']['bind_joints'], nc['group'])
    for jnt in [jaw_pivot_joint, upper_pivot_joint]:
        cmds.select(cl=True)
        bind_joint = cmds.joint(n = jnt.replace(nc['joint'], nc['joint_bind']))
        cmds.parentConstraint(jnt, bind_joint)
        cmds.setAttr('{}.radius'.format(bind_joint), 1.5)
        cmds.parent(bind_joint, bind_jnt_grp)


    #Clean
    clean_ctrl_grp = cmds.group(em=True, name = name + nc['ctrl'] + nc['group'])
    clean_rig_grp = cmds.group(em=True, name = name + '_Rig' + nc['group'])

    #Parent system
    cmds.parentConstraint(block_parent, jaw_ctrl_root, mo=True)
    if game_mode:
        cmds.parentConstraint(block_parent, clean_rig_grp, mo=True)
        cmds.scaleConstraint(block_parent, clean_rig_grp, mo=True)

    cmds.parent(jaw_ctrl_root, clean_ctrl_grp)
    cmds.parent(jaw_jnt_root, upper_root, global_locator_root, clean_rig_grp)

    cmds.parent(clean_rig_grp, '{}{}'.format(setup['rig_groups']['misc'], nc['group']))
    cmds.parent(clean_ctrl_grp, setup['base_groups']['control'] + nc['group'])

    #VIS
    # hide ctrls
    attrs_position = cmds.getAttr('{}.SetAttrsPosition'.format(config), asString=True)
    if attrs_position == 'new_locator':
        guide_attrs_position = cmds.spaceLocator(n=name + '_Attrs' + nc['locator'])[0]
    else:
        guide_attrs_position = attrs_position

    mt.line_attr(input=guide_attrs_position, name='Jaw_Vis')
    main_ctrl_attr = mt.new_enum(input=guide_attrs_position, name='jawMainCtrls', enums='Hide:Show', keyable=False)
    cmds.setAttr(main_ctrl_attr, 1)
    for ctrl in [jaw_ctrl]:
        shape = cmds.listRelatives(ctrl, s=True)[0]
        cmds.connectAttr(main_ctrl_attr, '{}.v'.format(shape))

    print('Build {} Success'.format(block))

#build_jaw_block()
