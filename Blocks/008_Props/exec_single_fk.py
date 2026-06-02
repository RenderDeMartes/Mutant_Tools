from __future__ import absolute_import
from maya import cmds
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

TAB_FOLDER = '008_Props'
PYBLOCK_NAME = 'exec_single_fk'


#---------------------------------------------

def create_single_fk_block(name = 'Bone'):

    # Read name conventions as nc[''] and setup as seup['']
    PATH = os.path.dirname(__file__)
    PATH = Path(PATH)
    PATH_PARTS = PATH.parts[:-2]
    FOLDER = ''
    for f in PATH_PARTS:
        FOLDER = os.path.join(FOLDER, f)

    MODULE_FILE = os.path.join(os.path.dirname(__file__), '01_Single_FK.json')
    with open(MODULE_FILE) as module_file:
        module = json.load(module_file)

    nc, curve_data, setup = mt.import_configs()

    #name checks and block creation
    name = mt.ask_name(text = name)
    if cmds.objExists('{}{}'.format(name,nc['module'])):
        cmds.warning('Name already exists.')
        return ''

    single_fk_block = mt.create_block(name = name, icon = 'Bone',  attrs = module['attrs'], build_command = module['build_command'], import_command = module['import'])
    single_fk_config = single_fk_block[1]
    single_fk_block = single_fk_block[0]

    # Indent ShowOrientAttrs so it appears as a sub-option of CtrlOrientOffset
    cmds.addAttr('{}.ShowOrientAttrs'.format(single_fk_config), e=True, niceName=u'\u00A0\u00A0\u00A0\u00A0\u2514 Show Orient Attrs')

    if name == 'COG':
        cmds.setAttr('{}.CtrlType'.format(single_fk_config),16)# if cog do a cog ctrl

    loc_guide = cmds.spaceLocator(n = name + nc['locator'])
    cmds.parent(loc_guide, single_fk_block)

    print('Single_fk Created Successfully')

#create_single_fk_block()

#-------------------------

def _build_single_fk_side(name, loc_guide, config, nc, setup, is_mirror_side=False):
    """Build a single FK side. Extracted so mirror can call it twice.
    
    Args:
        name: Side-prefixed name (e.g. 'L_Bone' or 'R_Bone')
        loc_guide: The locator guide to position from
        config: Config network node name
        nc: Naming conventions dict
        setup: Rig setup dict
        is_mirror_side: If True, wrap ctrl root in a mirror group
    
    Returns:
        dict with 'root', 'ctrl', 'jnt', 'bind_jnt', 'rig_grp' keys (values may be None)
    """

    def _resolve_parent_target(attr_names, default_target):
        """Return a valid parent target from config attr or fallback to default."""
        target = default_target

        if isinstance(attr_names, str):
            attr_names = [attr_names]

        for attr_name in attr_names:
            if cmds.attributeQuery(attr_name, node=config, exists=True):
                custom_target = cmds.getAttr('{}.{}'.format(config, attr_name))
                if custom_target:
                    if cmds.objExists(custom_target):
                        target = custom_target
                        break
                    else:
                        cmds.warning('Parent target {} does not exist, falling back to {}'.format(custom_target, default_target))

        return target

    ctrl = mt.curve(input = loc_guide, type = cmds.getAttr('{}.CtrlType'.format(config), asString=True), rename = True,
                                       custom_name = True, name = name + nc['ctrl'],
                                       size = cmds.getAttr('{}.CtrlSize'.format(config)))
    mt.assign_color(input = ctrl, color = cmds.getAttr('{}.CtrlColor'.format(config), asString = True))

    root = mt.root_grp(input = ctrl)

    # Refresh ctrl reference — root_grp reparents ctrl, so the old DAG path may be stale
    ctrl = cmds.listRelatives(root, children=True, type='transform')[0]

    mt.match(root, loc_guide)

    # If mirror side, wrap root in mirror group before parenting
    if is_mirror_side:
        root = mt.mirror_group(root, world=True)

    default_ctrl_parent = '{}{}'.format(setup['base_groups']['control'], nc['group'])
    ctrl_parent_target = _resolve_parent_target(['SetCtrlParentHierarchy', 'SetCtrlParent_Hierarchy', 'SetCtrlParent'], default_ctrl_parent)
    if cmds.objExists(ctrl_parent_target):
        cmds.parent(root, ctrl_parent_target)
    else:
        cmds.warning('Could not parent {}. Missing target {}'.format(root, ctrl_parent_target))

    #create orientation offset above ctrl if enabled
    orient_name = None
    driven_node = None
    if cmds.attributeQuery('CtrlOrientOffset', node=config, exists=True) and cmds.getAttr('{}.CtrlOrientOffset'.format(config)) == True:
        orient_name = name + '_Orient'

        # Capture existing orient values before rebuild (if a previous build exists)
        saved_orient = None
        if cmds.objExists(orient_name):
            saved_orient = {
                't': cmds.getAttr('{}.t'.format(orient_name))[0],
                'r': cmds.getAttr('{}.r'.format(orient_name))[0],
                's': cmds.getAttr('{}.s'.format(orient_name))[0],
            }
            cmds.warning('ORIENT SAVE: captured values from scene node {}'.format(orient_name))
        else:
            # Fall back to checking the RebuildTemp JSON file (for "Delete and Rebuild")
            import os, tempfile, json
            scene_name = cmds.file(q=True, sceneName=True)
            safe_scene = os.path.basename(scene_name).replace('.ma', '').replace('.mb', '') if scene_name else "untitled"
            temp_orient_file = os.path.join(tempfile.gettempdir(), 'RebuildTemp', '{}_orient_values.json'.format(safe_scene))
            
            # Fallback for older saves
            if not os.path.exists(temp_orient_file):
                temp_orient_file = os.path.join(tempfile.gettempdir(), 'RebuildTemp', 'orient_values.json')

            if os.path.exists(temp_orient_file):
                try:
                    with open(temp_orient_file, 'r') as f:
                        all_orients = json.load(f)
                        if orient_name in all_orients:
                            saved_orient = all_orients[orient_name]
                            cmds.warning('ORIENT SAVE: restored values from JSON file for {}'.format(orient_name))
                except Exception as e:
                    cmds.warning("Failed to read orient values from temp file: {}".format(e))
            
            if not saved_orient:
                cmds.warning('ORIENT SAVE: no existing {} found in scene or JSON'.format(orient_name))

        orient_node = cmds.group(em=True, name=orient_name)
        # Find the direct parent of ctrl (could be root or root's child)
        ctrl_parent = cmds.listRelatives(ctrl, parent=True)[0]
        cmds.parent(orient_node, ctrl_parent)
        # Zero out the Orient transform (it inherits root's position via hierarchy)
        for attr in ['tx','ty','tz','rx','ry','rz']:
            cmds.setAttr('{}.{}'.format(orient_node, attr), 0)
        for attr in ['sx','sy','sz']:
            cmds.setAttr('{}.{}'.format(orient_node, attr), 1)
        # Make TRS channel box visible but not keyable (for manual orient tweaking)
        for attr in ['tx','ty','tz','rx','ry','rz','sx','sy','sz']:
            cmds.setAttr('{}.{}'.format(orient_node, attr), keyable=False, channelBox=True)

        # Re-parent ctrl under Orient FIRST so it maintains 0,0,0 local transforms
        cmds.parent(ctrl, orient_node)

        # Restore saved orient values from previous build
        if saved_orient:
            cmds.warning('ORIENT SAVE: restored values from JSON file for {}'.format(orient_node))
            cmds.setAttr('{}.tx'.format(orient_node), saved_orient['t'][0])
            cmds.setAttr('{}.ty'.format(orient_node), saved_orient['t'][1])
            cmds.setAttr('{}.tz'.format(orient_node), saved_orient['t'][2])
            cmds.setAttr('{}.rx'.format(orient_node), saved_orient['r'][0])
            cmds.setAttr('{}.ry'.format(orient_node), saved_orient['r'][1])
            cmds.setAttr('{}.rz'.format(orient_node), saved_orient['r'][2])
            cmds.setAttr('{}.sx'.format(orient_node), saved_orient['s'][0])
            cmds.setAttr('{}.sy'.format(orient_node), saved_orient['s'][1])
            cmds.setAttr('{}.sz'.format(orient_node), saved_orient['s'][2])

        # Add proxy attributes on the ctrl to expose the orient values
        # Separator
        cmds.addAttr(ctrl, longName='ctrlOrient', niceName='_________',
                     attributeType='enum', enumName='Ctrl Orient', keyable=True)
        cmds.setAttr('{}.ctrlOrient'.format(ctrl), lock=True)

        # Orient Translate (proxy)
        for axis in ['X', 'Y', 'Z']:
            attr_name = 'orientTranslate{}'.format(axis)
            cmds.addAttr(ctrl, longName=attr_name, attributeType='doubleLinear',
                         usedAsProxy=True)
            cmds.setAttr('{}.{}'.format(ctrl, attr_name), channelBox=True)
            cmds.connectAttr('{}.t{}'.format(orient_node, axis.lower()),
                             '{}.{}'.format(ctrl, attr_name))

        # Orient Rotate (proxy)
        for axis in ['X', 'Y', 'Z']:
            attr_name = 'orientRotate{}'.format(axis)
            cmds.addAttr(ctrl, longName=attr_name, attributeType='doubleAngle',
                         usedAsProxy=True)
            cmds.setAttr('{}.{}'.format(ctrl, attr_name), channelBox=True)
            cmds.connectAttr('{}.r{}'.format(orient_node, axis.lower()),
                             '{}.{}'.format(ctrl, attr_name))

        # Orient Scale (proxy)
        for axis in ['X', 'Y', 'Z']:
            attr_name = 'orientScale{}'.format(axis)
            cmds.addAttr(ctrl, longName=attr_name, attributeType='double',
                         defaultValue=1.0, usedAsProxy=True)
            cmds.setAttr('{}.{}'.format(ctrl, attr_name), channelBox=True)
            cmds.connectAttr('{}.s{}'.format(orient_node, axis.lower()),
                             '{}.{}'.format(ctrl, attr_name))

        # Hide orient proxy attrs if ShowOrientAttrs is off
        if cmds.getAttr('{}.ShowOrientAttrs'.format(config)) == False:
            cmds.setAttr('{}.ctrlOrient'.format(ctrl), channelBox=False)
            for prefix in ['orientTranslate', 'orientRotate', 'orientScale']:
                for axis in ['X', 'Y', 'Z']:
                    cmds.setAttr('{}.{}{}'.format(ctrl, prefix, axis), channelBox=False)

        # Create driven node + matrix math to negate the orient for joint driving
        # This ensures rotating _Orient only changes ctrl orientation, not the joint
        # Math: Orient.inverseMatrix * ctrl.matrix * Orient.matrix
        driven_node = cmds.group(em=True, name=name + '_Driven')
        cmds.parent(driven_node, ctrl_parent)
        cmds.setAttr('{}.tx'.format(driven_node), 0)
        cmds.setAttr('{}.ty'.format(driven_node), 0)
        cmds.setAttr('{}.tz'.format(driven_node), 0)

        # To prevent the joint from translating when the control is scaled, while keeping the scale aligned with the rotated space
        ctrl_dcmp = cmds.createNode('decomposeMatrix', name=name + '_Ctrl_Decomp')
        ctrl_comp_tr = cmds.createNode('composeMatrix', name=name + '_Ctrl_TR_Comp')
        
        cmds.connectAttr('{}.m'.format(ctrl), '{}.imat'.format(ctrl_dcmp))
        cmds.connectAttr('{}.ot'.format(ctrl_dcmp), '{}.it'.format(ctrl_comp_tr))
        cmds.connectAttr('{}.or'.format(ctrl_dcmp), '{}.ir'.format(ctrl_comp_tr))
        cmds.connectAttr('{}.osh'.format(ctrl_dcmp), '{}.ish'.format(ctrl_comp_tr))
        
        ctrl_comp_s = cmds.createNode('composeMatrix', name=name + '_Ctrl_S_Comp')
        cmds.connectAttr('{}.os'.format(ctrl_dcmp), '{}.is'.format(ctrl_comp_s))
        
        orient_dcmp = cmds.createNode('decomposeMatrix', name=name + '_Orient_Decomp')
        orient_comp_r = cmds.createNode('composeMatrix', name=name + '_Orient_R_Comp')
        cmds.connectAttr('{}.m'.format(orient_node), '{}.imat'.format(orient_dcmp))
        cmds.connectAttr('{}.or'.format(orient_dcmp), '{}.ir'.format(orient_comp_r))
        
        orient_comp_r_inv = cmds.createNode('inverseMatrix', name=name + '_Orient_R_Inv')
        cmds.connectAttr('{}.outputMatrix'.format(orient_comp_r), '{}.inputMatrix'.format(orient_comp_r_inv))
        
        m1 = cmds.createNode('multMatrix', name=name + '_M1')
        cmds.connectAttr('{}.im'.format(orient_node), '{}.i[0]'.format(m1))
        cmds.connectAttr('{}.outputMatrix'.format(ctrl_comp_tr), '{}.i[1]'.format(m1))
        cmds.connectAttr('{}.m'.format(orient_node), '{}.i[2]'.format(m1))
        
        m2 = cmds.createNode('multMatrix', name=name + '_M2')
        cmds.connectAttr('{}.outputMatrix'.format(orient_comp_r_inv), '{}.i[0]'.format(m2))
        cmds.connectAttr('{}.outputMatrix'.format(ctrl_comp_s), '{}.i[1]'.format(m2))
        cmds.connectAttr('{}.outputMatrix'.format(orient_comp_r), '{}.i[2]'.format(m2))
        
        m_final = cmds.createNode('multMatrix', name=name + '_M_Final')
        cmds.connectAttr('{}.matrixSum'.format(m2), '{}.i[0]'.format(m_final))
        cmds.connectAttr('{}.matrixSum'.format(m1), '{}.i[1]'.format(m_final))

        final_dcmp = cmds.createNode('decomposeMatrix', name=name + '_Final_Decomp')
        cmds.connectAttr('{}.matrixSum'.format(m_final), '{}.imat'.format(final_dcmp))

        cmds.connectAttr('{}.ot'.format(final_dcmp), '{}.t'.format(driven_node))
        cmds.connectAttr('{}.or'.format(final_dcmp), '{}.r'.format(driven_node))
        cmds.connectAttr('{}.os'.format(final_dcmp), '{}.s'.format(driven_node))
        cmds.connectAttr('{}.osh'.format(final_dcmp), '{}.sh'.format(driven_node))

        # Lock driven channels AFTER connections are established
        for attr in ['tx','ty','tz','rx','ry','rz','sx','sy','sz']:
            cmds.setAttr('{}.{}'.format(driven_node, attr), lock=True)

    #create gimbal ctrl under main
    gimbal_ctrl=''
    if cmds.getAttr('{}.Gimbal'.format(config)) == True :
        gimbal_ctrl = mt.curve(input = loc_guide, type = cmds.getAttr('{}.CtrlType'.format(config), asString=True), rename = False, custom_name = True,
                                                  name = name + nc['gimbal_ctrl'],
                                                  size = cmds.getAttr('{}.CtrlSize'.format(config)) * 0.8 )
        mt.assign_color(input = gimbal_ctrl, color = cmds.getAttr('{}.CtrlColor'.format(config), asString = True))

        cmds.parent(gimbal_ctrl, ctrl)
        
        # Zero out local transforms to ensure clean gimbal values
        cmds.setAttr('{}.t'.format(gimbal_ctrl), 0, 0, 0)
        cmds.setAttr('{}.r'.format(gimbal_ctrl), 0, 0, 0)
        cmds.setAttr('{}.s'.format(gimbal_ctrl), 1, 1, 1)

        #gimbal vis attrs
        show_gimbal_attr = mt.new_enum(input= ctrl, name = 'Gimbal', enums = 'Hide:Show')
        cmds.connectAttr(show_gimbal_attr, '{}.v'.format(cmds.listRelatives(gimbal_ctrl, shapes= True)[0]))

    #create joint and joint steps if True
    jnt = None
    bind_joint = None
    clean_rig_grp = None

    if cmds.getAttr('{}.CreateJoint'.format(config)) == True :
        cmds.select(cl=True)
        jnt = cmds.joint(n = name + nc['joint'])
        # Position joint at the guide's world-space transform
        guide_pos = cmds.xform(loc_guide, q=True, ws=True, t=True)
        guide_rot = cmds.xform(loc_guide, q=True, ws=True, ro=True)
        cmds.xform(jnt, ws=True, t=guide_pos)
        cmds.xform(jnt, ws=True, ro=guide_rot)

        clean_rig_grp = cmds.group(em=True, name=name + '_Rig' + nc['group'])
        default_joint_parent = '{}{}'.format(setup['rig_groups']['misc'], nc['group'])
        joint_parent_target = _resolve_parent_target(['SetJointParentHierarchy', 'SetJointParent_Hierarchy', 'SetJointParent'], default_joint_parent)
        if cmds.objExists(joint_parent_target):
            cmds.parent(clean_rig_grp, joint_parent_target)
        else:
            cmds.warning('Could not parent {}. Missing target {}'.format(clean_rig_grp, joint_parent_target))

        cmds.parent(jnt, clean_rig_grp)

        #parent to ctrl or gimbal, or driven if offset active
        has_offset = cmds.attributeQuery('CtrlOrientOffset', node=config, exists=True) and cmds.getAttr('{}.CtrlOrientOffset'.format(config))

        if has_offset:
            # If gimbal exists, add its local matrix into the driven chain
            if cmds.objExists(gimbal_ctrl):
                # Combine gimbal and ctrl before stripping scale
                ctrl_mm = cmds.createNode('multMatrix', name=name + '_Ctrl_MultMtx')
                cmds.connectAttr('{}.m'.format(gimbal_ctrl), '{}.i[0]'.format(ctrl_mm))
                cmds.connectAttr('{}.m'.format(ctrl), '{}.i[1]'.format(ctrl_mm))

                cmds.disconnectAttr('{}.m'.format(ctrl), '{}.imat'.format(name + '_Ctrl_Decomp'))
                cmds.connectAttr('{}.matrixSum'.format(ctrl_mm), '{}.imat'.format(name + '_Ctrl_Decomp'))

            cmds.parentConstraint(driven_node, jnt, mo=True)
            cmds.scaleConstraint(driven_node, jnt, mo=True)

        elif cmds.objExists(gimbal_ctrl):
            cmds.parentConstraint(gimbal_ctrl, jnt)
            cmds.scaleConstraint(gimbal_ctrl, jnt)

        else:
            cmds.parentConstraint(ctrl, jnt)
            cmds.scaleConstraint(ctrl, jnt)

        #Create bind joint
        cmds.select(cl=True)
        bind_joint = cmds.joint(n = name + nc['joint_bind'])
        cmds.parentConstraint(jnt, bind_joint)
        cmds.scaleConstraint(jnt, bind_joint)

        cmds.parent(bind_joint, 'Bind_Joints_Grp')

    #clean if COG
    if 'COG' in str(ctrl):
        if gimbal_ctrl:
            mt.hide_attr(input = gimbal_ctrl, s=True)

    return {'root': root, 'ctrl': ctrl, 'jnt': jnt, 'bind_jnt': bind_joint, 'rig_grp': clean_rig_grp}


def build_single_fk_block():

    mt.check_is_there_is_base()

    nc, curve_data, setup = mt.import_configs()
    block = cmds.ls(sl=True)

    name = block[0].replace(nc['module'], '')

    config = cmds.listConnections(block)[1]
    loc_guide = cmds.listRelatives(block, c=True, fullPath=True)[0]
    print(loc_guide)

    # Read mirror setting
    try:
        mirror_mode = cmds.getAttr('{}.Mirror'.format(config), asString=True)
    except:
        mirror_mode = 'False'

    # Auto-prepend L_ when mirroring if the name doesn't already have a side prefix
    if mirror_mode in ('True', 'Right_Only') and not name.startswith(nc['left']) and not name.startswith(nc['right']):
        name = nc['left'] + name

    # Determine which sides to build
    if mirror_mode == 'True':
        # Build left side, then mirrored right side
        right_name = name.replace(nc['left'], nc['right'], 1)
        _build_single_fk_side(name, loc_guide, config, nc, setup, is_mirror_side=False)
        _build_single_fk_side(right_name, loc_guide, config, nc, setup, is_mirror_side=True)

    elif mirror_mode == 'Right_Only':
        # Build only the right side (mirrored)
        right_name = name.replace(nc['left'], nc['right'], 1)
        _build_single_fk_side(right_name, loc_guide, config, nc, setup, is_mirror_side=True)

    else:
        # No mirror - build as-is
        _build_single_fk_side(name, loc_guide, config, nc, setup, is_mirror_side=False)

    print ('Build of single_fk was succesfull')



#build_single_fk_block()
