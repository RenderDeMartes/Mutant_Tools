from __future__ import absolute_import
from maya import cmds
import json
try:
    import importlib;from importlib import reload
except:
    import imp;from imp import reload

import os

import Mutant_Tools
import Mutant_Tools.Utils.Rigging
from Mutant_Tools.Utils.Rigging import main_mutant
reload(Mutant_Tools.Utils.Rigging.main_mutant)

mt = main_mutant.Mutant()

# ---------------------------------------------

TAB_FOLDER = '002_Biped'
PYBLOCK_NAME = 'exec_leg_softik'


def _load_module_data():

    module_file = os.path.join(os.path.dirname(__file__), '013_LegSoftIK.json')
    with open(module_file) as module_handle:
        return json.load(module_handle)


def _replace_side(value, side_token, nc):

    if not value:
        return value

    if side_token == nc['right']:
        return value.replace(nc['left'], nc['right'])

    return value


def _attr_exists(attr_path):

    if not attr_path or '.' not in attr_path:
        return False

    node, attr_name = attr_path.split('.', 1)
    return cmds.objExists(node) and cmds.attributeQuery(attr_name, node=node, exists=True)


def _setup_locator(locator):

    shapes = cmds.listRelatives(locator, shapes=True) or []
    for shape in shapes:
        cmds.setAttr('{}.visibility'.format(shape), 0)
        cmds.setAttr('{}.overrideEnabled'.format(shape), 1)
        cmds.setAttr('{}.overrideColor'.format(shape), 6)


def _ensure_misc_group(setup, nc):

    misc_group = '{}{}'.format(setup['rig_groups']['misc'], nc['group'])
    if cmds.objExists(misc_group):
        return misc_group

    misc_group = cmds.group(empty=True, name=misc_group)
    rig_group = '{}{}'.format(setup['base_groups']['rig'], nc['group'])
    if cmds.objExists(rig_group):
        cmds.parent(misc_group, rig_group)

    return misc_group


def _ensure_locator(locator_name, parent_node):

    if cmds.objExists(locator_name):
        locator = locator_name
    else:
        locator = cmds.spaceLocator(name=locator_name)[0]

    current_parent = cmds.listRelatives(locator, parent=True) or []
    if not current_parent or current_parent[0] != parent_node:
        cmds.parent(locator, parent_node)

    for attr in ('translate', 'rotate'):
        try:
            cmds.setAttr('{}.{}'.format(locator, attr), 0, 0, 0)
        except Exception:
            pass

    _setup_locator(locator)
    return locator


def _get_distance_names(side_token):

    if side_token == 'L_':
        return 'l_pv_upLeg_joint_distance', 'l_pv_upLeg_joint_distanceShape'

    return 'r_pv_upLeg_joint_distance', 'r_pv_upLeg_joint_distanceShape'


def _ensure_distance_shape(side_token, ankle_loc, pelvis_loc, misc_group):

    dist_transform_name, dist_shape_name = _get_distance_names(side_token)
    if cmds.objExists(dist_transform_name):
        cmds.delete(dist_transform_name)

    dist_shape = cmds.distanceDimension(startPoint=(0, 0, 0), endPoint=(1, 0, 0))
    dist_transform = cmds.listRelatives(dist_shape, parent=True)[0]
    dist_transform = cmds.rename(dist_transform, dist_transform_name)
    dist_shape = cmds.listRelatives(dist_transform, shapes=True)[0]
    dist_shape = cmds.rename(dist_shape, dist_shape_name)

    start_loc = cmds.listConnections('{}.startPoint'.format(dist_shape), source=True) or []
    end_loc = cmds.listConnections('{}.endPoint'.format(dist_shape), source=True) or []

    cmds.connectAttr('{}.worldPosition[0]'.format(ankle_loc), '{}.startPoint'.format(dist_shape), force=True)
    cmds.connectAttr('{}.worldPosition[0]'.format(pelvis_loc), '{}.endPoint'.format(dist_shape), force=True)

    if start_loc:
        cmds.delete(start_loc)
    if end_loc:
        cmds.delete(end_loc)

    if misc_group:
        cmds.parent(dist_transform, misc_group)

    cmds.setAttr('{}.visibility'.format(dist_transform), 0)
    return dist_shape


def _derive_offset_group_names(ik_handle, nc):

    if nc['ik_rp'] in ik_handle:
        root_grp = ik_handle.replace(nc['ik_rp'], '{}{}'.format(nc['root'], nc['group']))
        auto_grp = ik_handle.replace(nc['ik_rp'], '{}{}'.format(nc['auto'], nc['group']))
    else:
        root_grp = '{}{}{}'.format(ik_handle, nc['root'], nc['group'])
        auto_grp = '{}{}{}'.format(ik_handle, nc['auto'], nc['group'])

    return root_grp, auto_grp


def _match_transform(source, target):

    cmds.delete(cmds.parentConstraint(source, target, mo=False))


def _ensure_ik_offset_groups(ik_handle, parent_grp, nc):

    root_grp, auto_grp = _derive_offset_group_names(ik_handle, nc)

    if not cmds.objExists(root_grp):
        root_grp = cmds.group(empty=True, name=root_grp)
        _match_transform(ik_handle, root_grp)

    if not cmds.objExists(auto_grp):
        auto_grp = cmds.group(empty=True, name=auto_grp)
        _match_transform(ik_handle, auto_grp)

    auto_parent = cmds.listRelatives(auto_grp, parent=True) or []
    if not auto_parent or auto_parent[0] != root_grp:
        cmds.parent(auto_grp, root_grp)

    root_parent = cmds.listRelatives(root_grp, parent=True) or []
    if not root_parent or root_parent[0] != parent_grp:
        cmds.parent(root_grp, parent_grp)

    ik_parent = cmds.listRelatives(ik_handle, parent=True) or []
    if not ik_parent or ik_parent[0] != auto_grp:
        cmds.parent(ik_handle, auto_grp)

    return root_grp, auto_grp


def _get_knee_pma_name(side_token):

    if side_token == 'L_':
        return 'knee_plusMinusAverage'

    return 'r_knee_plusMinusAverage'


def _ensure_knee_pma(side_token, knee_joint):

    pma_name = _get_knee_pma_name(side_token)
    current_tx = cmds.getAttr('{}.tx'.format(knee_joint))

    if cmds.objExists(pma_name):
        pma_node = pma_name
    else:
        pma_node = cmds.createNode('plusMinusAverage', name=pma_name)

    cmds.setAttr('{}.operation'.format(pma_node), 1)
    if not cmds.listConnections('{}.input1D[0]'.format(pma_node), source=True, destination=False):
        cmds.setAttr('{}.input1D[0]'.format(pma_node), current_tx)

    cmds.connectAttr('{}.output1D'.format(pma_node), '{}.tx'.format(knee_joint), force=True)
    return pma_node


def _get_attr_value(attr_path):

    node, attr_name = attr_path.split('.', 1)
    return cmds.getAttr('{}.{}'.format(node, attr_name))


def _get_normalized_chain_length(dist_shape, global_scale_attr, mover_scale_attr):

    chain_length = cmds.getAttr('{}.distance'.format(dist_shape))
    global_size = _get_attr_value(global_scale_attr)
    mover_size = _get_attr_value(mover_scale_attr)
    return chain_length / (global_size * mover_size)


def _get_expression_name(side_token):

    if side_token == 'L_':
        return 'L_SoftIk_Expression'

    return 'R_SoftIk_Expression'


def _create_expression(side_token, dist_shape, soft_attr_holder, global_scale_attr, mover_scale_attr,
                       chain_length, stretch_attr, pin_attr, auto_grp, pma_node):

    expression_name = _get_expression_name(side_token)
    expression = """
$controlDist = {dist_shape}.distance*1/({global_scale_attr}*{mover_scale_attr});
$softDist = $controlDist;
$softp = {soft_attr_holder}.SoftIk;
$chainLen = {chain_length};
$strech = {stretch_attr};
$pin = {pin_attr};
$sdif = $controlDist;

if($controlDist > ($chainLen - $softp))
{{
    if($softp > 0)
    {{
        $softDist = $chainLen - $softp*exp(-($controlDist-($chainLen-$softp))/$softp);
    }} else {{
        $softDist = $chainLen;
    }}
}}

{auto_grp}.translateY = (-1*($softDist-$controlDist)*(1-$strech))*(1-$pin);

if($controlDist > $chainLen){{$sdif = $chainLen;}}
{pma_node}.input1D[1] = (($sdif-$softDist)*$strech)*(1-$pin);
""".format(
        dist_shape=dist_shape,
        global_scale_attr=global_scale_attr,
        mover_scale_attr=mover_scale_attr,
        soft_attr_holder=soft_attr_holder,
        chain_length=chain_length,
        stretch_attr=stretch_attr,
        pin_attr=pin_attr,
        auto_grp=auto_grp,
        pma_node=pma_node
    )

    if cmds.objExists(expression_name):
        cmds.delete(expression_name)

    cmds.expression(name=expression_name, string=expression, alwaysEvaluate=True, unitConversion='all')
    return expression_name


def _ensure_soft_attr(ctrl):

    if not cmds.attributeQuery('SoftIk', node=ctrl, exists=True):
        mt.line_attr(input=ctrl, name='SoftIk')
        mt.new_attr(input=ctrl, name='SoftIk', min=0, max=100, default=0)


def _get_side_config(config, side_token, nc):

    if cmds.attributeQuery('LeftSoftIkAttrHolder', node=config, exists=True):
        soft_holder_raw = cmds.getAttr('{}.LeftSoftIkAttrHolder'.format(config))
    else:
        soft_holder_raw = cmds.getAttr('{}.LeftSoftAttrHolder'.format(config))

    return {
        'ankle_ctrl': _replace_side(cmds.getAttr('{}.LeftAnkleCtrl'.format(config)), side_token, nc),
        'soft_attr_holder': _replace_side(soft_holder_raw, side_token, nc),
        'ankle_grp': _replace_side(cmds.getAttr('{}.LeftAnkleRFLGroup'.format(config)), side_token, nc),
        'pelvis_ctrl': _replace_side(cmds.getAttr('{}.LeftPelvisCtrl'.format(config)), side_token, nc),
        'ik_handle': _replace_side(cmds.getAttr('{}.LeftIKHandle'.format(config)), side_token, nc),
        'knee_joint': _replace_side(cmds.getAttr('{}.LeftKneeIkJoint'.format(config)), side_token, nc),
        'stretch_attr': _replace_side(cmds.getAttr('{}.LeftStretchAttr'.format(config)), side_token, nc),
        'pin_attr': _replace_side(cmds.getAttr('{}.LeftPinAttr'.format(config)), side_token, nc),
        'global_scale_attr': cmds.getAttr('{}.GlobalScaleAttr'.format(config)),
        'mover_scale_attr': cmds.getAttr('{}.MoverScaleAttr'.format(config))
    }


def _validate_side_config(side_token, side_config):

    missing = []
    for node_name in ('ankle_ctrl', 'soft_attr_holder', 'ankle_grp', 'pelvis_ctrl', 'ik_handle', 'knee_joint'):
        if not cmds.objExists(side_config[node_name]):
            missing.append(side_config[node_name])

    for attr_name in ('stretch_attr', 'pin_attr', 'global_scale_attr', 'mover_scale_attr'):
        if not _attr_exists(side_config[attr_name]):
            missing.append(side_config[attr_name])

    if missing:
        cmds.warning('Skipping {} Soft IK. Missing nodes or attrs: {}'.format(side_token, ', '.join(missing)))
        return False

    return True


def create_leg_softik_block(name='LegSoftIK'):

    nc, curve_data, setup = mt.import_configs()
    module = _load_module_data()

    name = mt.ask_name(text=module['Name'])
    if not name:
        cmds.warning('Block creation cancelled: no name provided.')
        return ''

    if cmds.objExists('{}{}'.format(name, nc['module'])):
        cmds.warning('Name already exists.')
        return ''

    block = mt.create_block(name=name,
                            icon='softIkLeg',
                            attrs=module['attrs'],
                            build_command=module['build_command'],
                            import_command=module['import'])

    cmds.select(block[0])
    print('{} Created Successfully'.format(name))
    return block[0]


def build_leg_softik_block():

    nc, curve_data, setup = mt.import_configs()

    mt.check_is_there_is_base()

    block = cmds.ls(sl=True)
    if not block:
        cmds.warning('Select a Leg Soft IK block to build.')
        return

    connections = cmds.listConnections(block) or []
    if len(connections) < 2:
        cmds.warning('Unable to find the selected block config.')
        return

    config = connections[1]
    block = block[0]
    misc_group = _ensure_misc_group(setup, nc)
    side_config_L = _get_side_config(config, nc['left'], nc)
    side_config_R = _get_side_config(config, nc['right'], nc)

    sides = ['L', 'R']

    for side, holder in (('L', side_config_L['soft_attr_holder']), ('R', side_config_R['soft_attr_holder'])):
        if not cmds.objExists(holder):
            cmds.warning('Missing SoftIk attr holder for {} side: {}'.format(side, holder))
            continue
        _ensure_soft_attr(holder)

    def setup_locator(loc):
        shapes = cmds.listRelatives(loc, shapes=True) or []
        for shape in shapes:
            cmds.setAttr(shape + '.visibility', 0)
            cmds.setAttr(shape + '.overrideEnabled', 1)
            cmds.setAttr(shape + '.overrideColor', 6)

    for side in sides:
        ankle_grp = '{}_Foot_Ankle_RFL_Grp'.format(side)
        pelvis_ctrl = '{}_Pelvis_Ctrl'.format(side)

        if not cmds.objExists(ankle_grp) or not cmds.objExists(pelvis_ctrl):
            cmds.warning('Skipping {} side. Missing {} or {}'.format(side, ankle_grp, pelvis_ctrl))
            continue

        loc1 = '{}_Ankle_Dist_Loc'.format(side)
        loc2 = '{}_Pelvis_Dist_Loc'.format(side)
        if cmds.objExists(loc1):
            cmds.delete(loc1)
        if cmds.objExists(loc2):
            cmds.delete(loc2)

        loc1 = cmds.spaceLocator(name=loc1)[0]
        loc2 = cmds.spaceLocator(name=loc2)[0]

        cmds.parent(loc1, ankle_grp)
        cmds.delete(cmds.parentConstraint(ankle_grp, loc1))
        cmds.parent(loc2, pelvis_ctrl)
        cmds.delete(cmds.parentConstraint(pelvis_ctrl, loc2))

        cmds.setAttr(loc1 + '.translate', 0, 0, 0)
        cmds.setAttr(loc2 + '.translate', 0, 0, 0)

        setup_locator(loc1)
        setup_locator(loc2)

    distance_nodes = {}

    for side in sides:
        loc1 = '{}_Ankle_Dist_Loc'.format(side)
        loc2 = '{}_Pelvis_Dist_Loc'.format(side)

        if not cmds.objExists(loc1) or not cmds.objExists(loc2):
            continue

        dist_shape = cmds.distanceDimension(startPoint=(0, 0, 0), endPoint=(1, 0, 0))
        dist_transform = cmds.listRelatives(dist_shape, parent=True)[0]

        if side == 'L':
            new_transform = cmds.rename(dist_transform, 'l_pv_upLeg_joint_distance')
        else:
            new_transform = cmds.rename(dist_transform, 'r_pv_upLeg_joint_distance')

        new_shape = cmds.listRelatives(new_transform, shapes=True)[0]

        if side == 'L':
            new_shape = cmds.rename(new_shape, 'l_pv_upLeg_joint_distanceShape')
        else:
            new_shape = cmds.rename(new_shape, 'r_pv_upLeg_joint_distanceShape')

        start_loc = cmds.listConnections(new_shape + '.startPoint', source=True)[0]
        end_loc = cmds.listConnections(new_shape + '.endPoint', source=True)[0]

        cmds.connectAttr('{}.worldPosition[0]'.format(loc1), '{}.startPoint'.format(new_shape), force=True)
        cmds.connectAttr('{}.worldPosition[0]'.format(loc2), '{}.endPoint'.format(new_shape), force=True)

        cmds.delete(start_loc, end_loc)

        if cmds.objExists(misc_group):
            cmds.parent(new_transform, misc_group)

        distance_nodes[side] = new_shape
        print('{} shape node: {} | attr: {}.distance'.format(side, new_shape, new_shape))

    for side in sides:
        ik_handle = '{}_Ankle_Ik_IKrp'.format(side)
        parent_grp = '{}_Foot_Ankle_RFL_Grp'.format(side)

        if not cmds.objExists(ik_handle) or not cmds.objExists(parent_grp):
            continue

        root_grp = '{}_Ankle_Ik_Root_Grp'.format(side)
        auto_grp = '{}_Ankle_Ik_Auto_Grp'.format(side)

        if cmds.objExists(root_grp):
            cmds.delete(root_grp)
        if cmds.objExists(auto_grp):
            cmds.delete(auto_grp)

        root_grp = cmds.group(empty=True, name=root_grp)
        auto_grp = cmds.group(empty=True, name=auto_grp)

        cmds.delete(cmds.parentConstraint(ik_handle, root_grp))
        cmds.delete(cmds.parentConstraint(ik_handle, auto_grp))

        cmds.parent(auto_grp, root_grp)
        cmds.parent(root_grp, parent_grp)
        cmds.parent(ik_handle, auto_grp)

    for side in sides:
        knee_jnt = '{}_Knee_Ik_Jnt'.format(side)
        if not cmds.objExists(knee_jnt):
            continue

        current_tx = cmds.getAttr('{}.tx'.format(knee_jnt))

        if side == 'L':
            pma_name = 'knee_plusMinusAverage'
        else:
            pma_name = 'r_knee_plusMinusAverage'

        if cmds.objExists(pma_name):
            cmds.delete(pma_name)
        pma_node = cmds.createNode('plusMinusAverage', name=pma_name)

        cmds.setAttr('{}.operation'.format(pma_node), 1)
        cmds.setAttr('{}.input1D[0]'.format(pma_node), current_tx)
        cmds.connectAttr('{}.output1D'.format(pma_node), '{}.tx'.format(knee_jnt), force=True)

        print('{} knee PMA: {} | rest value set to {}'.format(side, pma_node, current_tx))

    chain_lengths = {}

    for side in sides:
        if side not in distance_nodes:
            continue

        dist_shape = distance_nodes[side]
        chain_len = cmds.getAttr('{}.distance'.format(dist_shape))

        global_size = cmds.getAttr('Global_Ctrl.sx')
        mover_size = cmds.getAttr('Mover_Ctrl.sx')
        chain_len = chain_len / (global_size * mover_size)

        chain_lengths[side] = chain_len
        print('{} chain length from distance node: {}'.format(side, chain_len))

    if 'L' not in chain_lengths or 'R' not in chain_lengths:
        cmds.warning('Could not compute both chain lengths. Soft IK expressions were not created.')
        return

    left_expression = """
$controlDist = l_pv_upLeg_joint_distanceShape.distance*1/(Global_Ctrl.sx*Mover_Ctrl.sx);
$softDist = $controlDist;
$softp = {left_soft_attr_holder}.SoftIk;
$chainLen = {left_len};
$strech = L_KneeMid_Bendy_Ctrl|L_Hip_Jnt_Switch_Loc.Stretch_On;
$pin = L_KneeMid_Bendy_Ctrl|L_Hip_Jnt_Switch_Loc.Pole_Vector_Lock;
$sdif = $controlDist;

if($controlDist > ($chainLen - $softp))
{{
    if($softp > 0)
    {{
        $softDist = $chainLen - $softp*exp(-($controlDist-($chainLen-$softp))/$softp);
    }} else {{
        $softDist = $chainLen;
    }}
}}

L_Ankle_Ik_Auto_Grp.translateY = (-1*($softDist-$controlDist)*(1-$strech))*(1-$pin);

if($controlDist > $chainLen){{$sdif = $chainLen;}}
knee_plusMinusAverage.input1D[1] = (($sdif-$softDist)*$strech)*(1-$pin);
""".format(left_soft_attr_holder=side_config_L['soft_attr_holder'], left_len=chain_lengths['L'])

    right_expression = """
$controlDist = r_pv_upLeg_joint_distanceShape.distance*1/(Global_Ctrl.sx*Mover_Ctrl.sx);
$softDist = $controlDist;
$softp = {right_soft_attr_holder}.SoftIk;
$chainLen = {right_len};
$strech = R_KneeMid_Bendy_Ctrl|R_Hip_Jnt_Switch_Loc.Stretch_On;
$pin = R_KneeMid_Bendy_Ctrl|R_Hip_Jnt_Switch_Loc.Pole_Vector_Lock;
$sdif = $controlDist;

if($controlDist > ($chainLen - $softp))
{{
    if($softp > 0)
    {{
        $softDist = $chainLen - $softp*exp(-($controlDist-($chainLen-$softp))/$softp);
    }} else {{
        $softDist = $chainLen;
    }}
}}

R_Ankle_Ik_Auto_Grp.translateY = (-1*($softDist-$controlDist)*(1-$strech))*(1-$pin);

if($controlDist > $chainLen){{$sdif = $chainLen;}}
r_knee_plusMinusAverage.input1D[1] = (($sdif-$softDist)*$strech)*(1-$pin);
""".format(right_soft_attr_holder=side_config_R['soft_attr_holder'], right_len=chain_lengths['R'])

    if cmds.objExists('L_SoftIk_Expression'):
        cmds.delete('L_SoftIk_Expression')
    if cmds.objExists('R_SoftIk_Expression'):
        cmds.delete('R_SoftIk_Expression')

    cmds.expression(name='L_SoftIk_Expression', string=left_expression, alwaysEvaluate=True, unitConversion='all')
    cmds.expression(name='R_SoftIk_Expression', string=right_expression, alwaysEvaluate=True, unitConversion='all')

    print('Expressions created | L chainLen: {} | R chainLen: {}'.format(chain_lengths['L'], chain_lengths['R']))
    cmds.select(block)