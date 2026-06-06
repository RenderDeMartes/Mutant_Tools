from maya import cmds
import os
import json

from Mutant_Tools.Utils.Rigging import main_mutant
mt = main_mutant.Mutant()

def create_auto_clavicle_block():
    nc, curve_data, setup = mt.import_configs()
    # Inline JSON load
    json_file = '012_AutoClavicle.json'
    folder = os.path.dirname(__file__)
    path = os.path.join(folder, json_file)
    with open(path, 'r') as handle:
        module = json.load(handle)
    name = mt.ask_name(module.get('Name', 'AutoClavicle'))
    if not name:
        cmds.warning('Block creation cancelled: no name provided.')
        return
    block = mt.create_block(
        name=name,
        icon='AutoClavicle',
        attrs=module.get('attrs', {}),
        build_command=module.get('build_command', 'build_auto_clavicle_block'),
        import_command=module.get('import', 'create_auto_clavicle_block')
    )
    if block and cmds.objExists(block):
        cmds.select(block)
        print('Created block: {}'.format(block))

def build_auto_clavicle_block():
    nc, curve_data, setup = mt.import_configs()

    mt.check_is_there_is_base()

    block = cmds.ls(sl=True)
    config = cmds.listConnections(block)[1]
    block = block[0]
    name = block.replace(nc['module'],'')

    # Inline attr read
    clavicle_ctrl = cmds.getAttr('{}.ClavicleCtrl'.format(config), asString = True)
    fk_shoulder_ctrl = cmds.getAttr('{}.FKShoulderCtrl'.format(config), asString = True)
    mirror = cmds.getAttr('{}.Mirror'.format(config), asString = True)
    misc_group = 'Miscellaneous_Grp'

    clean_rig_grp = cmds.group(empty=True, name=name + '_Rig_Grp')
    if cmds.objExists(misc_group):
        cmds.parent(clean_rig_grp, misc_group)

    # Find ik shoulder joint based on FK shoulder ctrl naming
    ik_joint = fk_shoulder_ctrl.replace('_Fk'+nc['ctrl'], '_Ik'+nc['joint'])

    to_build_ik = [ik_joint]
    if mirror == 'True':
        to_build_ik.append(ik_joint.replace(nc['left'], nc['right']))

    to_build_fk = [fk_shoulder_ctrl]
    if mirror == 'True':
        to_build_fk.append(fk_shoulder_ctrl.replace(nc['left'], nc['right']))
    
    print('#$ Auto Clavicle Build Summary $#')    
    print("#"*40)
    print("$"*40)
    print('Building Auto Clavicle for FK controls: {}'.format(to_build_fk))
    print(fk_shoulder_ctrl)
    print('Building Auto Clavicle for IK controls: {}'.format(to_build_ik))
    print(ik_joint)
    print("$"*40)
    print("#"*40)

    # Fk Setup
    for fk_ctrl in to_build_fk:
        side_shoulder = 'Left' if nc['left'] in fk_ctrl else 'Right'
        if side_shoulder == 'Left':
            clav_ctrl = clavicle_ctrl
        else:
            clav_ctrl = clavicle_ctrl.replace(nc['left'], nc['right'])

        if not cmds.objExists(fk_ctrl):
            cmds.warning('FK shoulder control not found, skipping: {}'.format(fk_ctrl))
            continue
        if not cmds.objExists(clav_ctrl):
            cmds.warning('Clavicle control not found, skipping: {}'.format(clav_ctrl))
            continue

        if not cmds.attributeQuery('AutoClavicle', node=clav_ctrl, exists=True):
            mt.line_attr(input=clav_ctrl, name='Auto Clavicle')
            mt.new_attr(input=clav_ctrl, name='AutoClavicle', min=0, max=1, default=0.4)

        # create per-axis range attrs on clavicle
        for axis_name in ['X', 'Y', 'Z']:
            if not cmds.attributeQuery('AutoClavicle{}_Start'.format(axis_name), node=clav_ctrl, exists=True):
                mt.new_attr(input=clav_ctrl, name='AutoClavicle{}_Start'.format(axis_name), min=-90, max=90, default=0)
            if not cmds.attributeQuery('AutoClavicle{}_Stop'.format(axis_name), node=clav_ctrl, exists=True):
                mt.new_attr(input=clav_ctrl, name='AutoClavicle{}_Stop'.format(axis_name), min=-90, max=90, default=90)
            if not cmds.attributeQuery('AutoClavicle{}_NegStart'.format(axis_name), node=clav_ctrl, exists=True):
                mt.new_attr(input=clav_ctrl, name='AutoClavicle{}_NegStart'.format(axis_name), min=-90, max=90, default=0)
            if not cmds.attributeQuery('AutoClavicle{}_NegStop'.format(axis_name), node=clav_ctrl, exists=True):
                mt.new_attr(input=clav_ctrl, name='AutoClavicle{}_NegStop'.format(axis_name), min=-90, max=90, default=-90)

        # create root for shoulder FK ctrl
        clav_auto_grp = mt.root_grp(input=clav_ctrl, custom=True, custom_name='AutoClavicleFk_Auto')[0]
        clav_root_grp = mt.root_grp(input=clav_ctrl, custom=True, custom_name='AutoClavicleFk_Root')[0]

        # check translate, rotate are 0,0,0 and fix if not in clav_auto_grp, clav_root_grp and clav ctrl
        for obj in [clav_auto_grp, clav_root_grp, clav_ctrl]:
            cmds.setAttr('{}.translate'.format(obj), 0, 0, 0)
            cmds.setAttr('{}.rotate'.format(obj), 0, 0, 0)  
            try:
                cmds.setAttr('{}.scale'.format(obj), 1, 1, 1)
            except:
                pass


        # create per-axis remapValue nodes
        node_name = fk_ctrl.replace('|', '_').replace(':', '_')

        for i, axis in enumerate(['X', 'Y', 'Z']):
            # create remapValue for this axis (positive and negative)
            remap_pos = cmds.createNode('remapValue', n='{}_AutoClavicle_Remap{}Pos'.format(node_name, axis))
            remap_neg = cmds.createNode('remapValue', n='{}_AutoClavicle_Remap{}Neg'.format(node_name, axis))
            cond_node = cmds.createNode('condition', n='{}_AutoClavicle_Cond{}'.format(node_name, axis))

            # connect input rotation axis
            cmds.connectAttr('{}.rotate{}'.format(fk_ctrl, axis), '{}.inputValue'.format(remap_pos), f=True)
            cmds.connectAttr('{}.rotate{}'.format(fk_ctrl, axis), '{}.inputValue'.format(remap_neg), f=True)

            # positive range - output 0 to 180
            cmds.connectAttr('{}.AutoClavicle{}_Start'.format(clav_ctrl, axis), '{}.inputMin'.format(remap_pos), f=True)
            cmds.connectAttr('{}.AutoClavicle{}_Stop'.format(clav_ctrl, axis), '{}.inputMax'.format(remap_pos), f=True)
            cmds.setAttr('{}.outputMin'.format(remap_pos), 0)
            cmds.setAttr('{}.outputMax'.format(remap_pos), 90)

            # negative range - output 0 to -180
            cmds.connectAttr('{}.AutoClavicle{}_NegStop'.format(clav_ctrl, axis), '{}.inputMin'.format(remap_neg), f=True)
            cmds.connectAttr('{}.AutoClavicle{}_NegStart'.format(clav_ctrl, axis), '{}.inputMax'.format(remap_neg), f=True)
            cmds.setAttr('{}.outputMin'.format(remap_neg), -90)
            cmds.setAttr('{}.outputMax'.format(remap_neg), 0)

            # choose pos/neg based on rotation sign
            cmds.setAttr('{}.operation'.format(cond_node), 2)
            cmds.setAttr('{}.secondTerm'.format(cond_node), 0)
            cmds.connectAttr('{}.rotate{}'.format(fk_ctrl, axis), '{}.firstTerm'.format(cond_node), f=True)
            cmds.connectAttr('{}.outValue'.format(remap_pos), '{}.colorIfTrueR'.format(cond_node), f=True)
            cmds.connectAttr('{}.outValue'.format(remap_neg), '{}.colorIfFalseR'.format(cond_node), f=True)

            # connect remapped value to on/off multiply
            if i == 0:
                md_input = 'input1X'
            elif i == 1:
                md_input = 'input1Y'
            else:
                md_input = 'input1Z'

        # create on/off multiply node
        final_md = cmds.createNode('multiplyDivide', n='{}_AutoClavicle_OnOff_MD'.format(node_name))
        cmds.setAttr('{}.operation'.format(final_md), 1)

        # connect condition outputs to on/off MD
        for i, axis in enumerate(['X', 'Y', 'Z']):
            cond_node = '{}_AutoClavicle_Cond{}'.format(node_name, axis)
            if i == 0:
                md_input = 'input1X'
            elif i == 1:
                md_input = 'input1Y'
            else:
                md_input = 'input1Z'
            cmds.connectAttr('{}.outColorR'.format(cond_node), '{}.{}'.format(final_md, md_input), f=True)
        
        # connect AutoClavicle on/off attr to input2
        cmds.connectAttr('{}.AutoClavicle'.format(clav_ctrl), '{}.input2X'.format(final_md), f=True)
        cmds.connectAttr('{}.AutoClavicle'.format(clav_ctrl), '{}.input2Y'.format(final_md), f=True)
        cmds.connectAttr('{}.AutoClavicle'.format(clav_ctrl), '{}.input2Z'.format(final_md), f=True)

        # connect final output to auto clavicle group
        cmds.connectAttr('{}.output'.format(final_md), '{}.rotate'.format(clav_auto_grp), f=True)
    

    # Ik Setup
    for joint in to_build_ik:
        side_shoulder = 'Left' if nc['left'] in joint else 'Right'
        if side_shoulder == 'Left':
            clav_ctrl = clavicle_ctrl
        else:
            clav_ctrl = clavicle_ctrl.replace(nc['left'], nc['right'])

        if not cmds.objExists(joint):
            cmds.warning('Joint not found, skipping: {}'.format(joint))
            continue
        
        auto_clav_joint = cmds.joint(name=joint.replace(nc['joint'], '_AutoClavicleIk_Joint'), p=(0,0,0))
        auto_clav_joint_root = mt.root_grp(input=auto_clav_joint)[0]

        auto_clav_joint_quad = cmds.joint(name=joint.replace(nc['joint'], '_AutoClavicleIk_JointQuad'), p=(0,0,0))
        cmds.parent(auto_clav_joint_quad, auto_clav_joint_root)

        # Convert rotation through euler to avoid quaternion flipping
        euler_to_quat = cmds.createNode('eulerToQuat', n='{}_EulerToQuat'.format(auto_clav_joint.replace('|', '_').replace(':', '_')))
        quat_to_euler = cmds.createNode('quatToEuler', n='{}_QuatToEuler'.format(auto_clav_joint.replace('|', '_').replace(':', '_')))
        
        cmds.connectAttr('{}.rotate'.format(auto_clav_joint), '{}.inputRotate'.format(euler_to_quat), f=True)
        cmds.connectAttr('{}.outputQuat'.format(euler_to_quat), '{}.inputQuat'.format(quat_to_euler), f=True)
        cmds.connectAttr('{}.outputRotate'.format(quat_to_euler), '{}.rotate'.format(auto_clav_joint_quad), f=True)

        side_token = nc['left'] if joint.startswith(nc['left']) else nc['right']
        side_fk_ctrl = None
        for fk_ctrl in to_build_fk:
            if fk_ctrl.startswith(side_token):
                side_fk_ctrl = fk_ctrl
                break
        
        cmds.parent(auto_clav_joint_root, clean_rig_grp)
        cmds.delete(cmds.parentConstraint(side_fk_ctrl, auto_clav_joint_root, mo=False))


        wrist_aim_loc = cmds.spaceLocator(name=joint.replace(nc['joint'], '_WristAim_Loc'))[0]
        if side_token == nc['left']:
            cmds.delete(cmds.parentConstraint('L_Wrist_Ik_Ctrl', wrist_aim_loc, mo=False))
            cmds.connectAttr('L_Wrist_Ik_Ctrl.xformMatrix', '{}.offsetParentMatrix'.format(wrist_aim_loc), force=True)        
        else:
            cmds.delete(cmds.parentConstraint('R_Wrist_Ik_Ctrl', wrist_aim_loc, mo=False))
            cmds.connectAttr('R_Wrist_Ik_Ctrl.xformMatrix', '{}.offsetParentMatrix'.format(wrist_aim_loc), force=True)

        cmds.parent(wrist_aim_loc, clean_rig_grp)

        cmds.aimConstraint(
            wrist_aim_loc,
            auto_clav_joint,
            mo=True,
            aimVector=(0, 1, 0),
            upVector=(-1, 0, 0),
            worldUpType='vector',
            worldUpVector=(0, 1, 0)
        )
        
        # reader, reader_group, quad_loc = mt.create_joint_reader(auto_clav_joint, push_joint_name=joint + '_Reader', return_all=True)

        quad_loc = auto_clav_joint_quad

        if not cmds.objExists(clav_ctrl):
            cmds.warning('Clavicle control not found, skipping IK setup: {}'.format(clav_ctrl))
            continue
        if not cmds.objExists(quad_loc):
            cmds.warning('Quad loc not found, skipping IK setup: {}'.format(quad_loc))
            continue

        if not cmds.attributeQuery('AutoClavicle', node=clav_ctrl, exists=True):
            mt.line_attr(input=clav_ctrl, name='Auto Clavicle')
            mt.new_attr(input=clav_ctrl, name='AutoClavicle', min=0, max=1, default=0.25)

        for axis_name in ['X', 'Y', 'Z']:
            if not cmds.attributeQuery('AutoClavicle{}_Start'.format(axis_name), node=clav_ctrl, exists=True):
                mt.new_attr(input=clav_ctrl, name='AutoClavicle{}_Start'.format(axis_name), min=-90, max=90, default=0, keyable=True)
            if not cmds.attributeQuery('AutoClavicle{}_Stop'.format(axis_name), node=clav_ctrl, exists=True):
                mt.new_attr(input=clav_ctrl, name='AutoClavicle{}_Stop'.format(axis_name), min=-90, max=90, default=90, keyable=False)
            if not cmds.attributeQuery('AutoClavicle{}_NegStart'.format(axis_name), node=clav_ctrl, exists=True):
                mt.new_attr(input=clav_ctrl, name='AutoClavicle{}_NegStart'.format(axis_name), min=-90, max=90, default=0, keyable=True)
            if not cmds.attributeQuery('AutoClavicle{}_NegStop'.format(axis_name), node=clav_ctrl, exists=True):
                mt.new_attr(input=clav_ctrl, name='AutoClavicle{}_NegStop'.format(axis_name), min=-90, max=90, default=-90, keyable=False)

        clav_auto_grp = mt.root_grp(input=clav_ctrl, custom=True, custom_name='AutoClavicleIk_Auto')[0]
        clav_root_grp = mt.root_grp(input=clav_ctrl, custom=True, custom_name='AutoClavicleIk_Root')[0]

        for obj in [clav_auto_grp, clav_root_grp, clav_ctrl]:
            cmds.setAttr('{}.translate'.format(obj), 0, 0, 0)
            cmds.setAttr('{}.rotate'.format(obj), 0, 0, 0)
            try:
                cmds.setAttr('{}.scale'.format(obj), 1, 1, 1)
            except:
                pass

        node_name = quad_loc.replace('|', '_').replace(':', '_')

        for axis in ['X', 'Y', 'Z']:
            remap_pos = cmds.createNode('remapValue', n='{}_AutoClavicleIk_Remap{}Pos'.format(node_name, axis))
            remap_neg = cmds.createNode('remapValue', n='{}_AutoClavicleIk_Remap{}Neg'.format(node_name, axis))
            cond_node = cmds.createNode('condition', n='{}_AutoClavicleIk_Cond{}'.format(node_name, axis))

            cmds.connectAttr('{}.rotate{}'.format(quad_loc, axis), '{}.inputValue'.format(remap_pos), f=True)
            cmds.connectAttr('{}.rotate{}'.format(quad_loc, axis), '{}.inputValue'.format(remap_neg), f=True)

            cmds.connectAttr('{}.AutoClavicle{}_Start'.format(clav_ctrl, axis), '{}.inputMin'.format(remap_pos), f=True)
            cmds.connectAttr('{}.AutoClavicle{}_Stop'.format(clav_ctrl, axis), '{}.inputMax'.format(remap_pos), f=True)
            cmds.setAttr('{}.outputMin'.format(remap_pos), 0)
            cmds.setAttr('{}.outputMax'.format(remap_pos), 90)

            cmds.connectAttr('{}.AutoClavicle{}_NegStop'.format(clav_ctrl, axis), '{}.inputMin'.format(remap_neg), f=True)
            cmds.connectAttr('{}.AutoClavicle{}_NegStart'.format(clav_ctrl, axis), '{}.inputMax'.format(remap_neg), f=True)
            cmds.setAttr('{}.outputMin'.format(remap_neg), -90)
            cmds.setAttr('{}.outputMax'.format(remap_neg), 0)

            cmds.setAttr('{}.operation'.format(cond_node), 2)
            cmds.setAttr('{}.secondTerm'.format(cond_node), 0)
            cmds.connectAttr('{}.rotate{}'.format(quad_loc, axis), '{}.firstTerm'.format(cond_node), f=True)
            cmds.connectAttr('{}.outValue'.format(remap_pos), '{}.colorIfTrueR'.format(cond_node), f=True)
            cmds.connectAttr('{}.outValue'.format(remap_neg), '{}.colorIfFalseR'.format(cond_node), f=True)

        final_md = cmds.createNode('multiplyDivide', n='{}_AutoClavicleIk_OnOff_MD'.format(node_name))
        cmds.setAttr('{}.operation'.format(final_md), 1)

        for i, axis in enumerate(['X', 'Y', 'Z']):
            cond_node = '{}_AutoClavicleIk_Cond{}'.format(node_name, axis)
            if i == 0:
                md_input = 'input1X'
            elif i == 1:
                md_input = 'input1Y'
            else:
                md_input = 'input1Z'
            cmds.connectAttr('{}.outColorR'.format(cond_node), '{}.{}'.format(final_md, md_input), f=True)

        cmds.connectAttr('{}.AutoClavicle'.format(clav_ctrl), '{}.input2X'.format(final_md), f=True)
        cmds.connectAttr('{}.AutoClavicle'.format(clav_ctrl), '{}.input2Y'.format(final_md), f=True)
        cmds.connectAttr('{}.AutoClavicle'.format(clav_ctrl), '{}.input2Z'.format(final_md), f=True)

        cmds.connectAttr('{}.output'.format(final_md), '{}.rotate'.format(clav_auto_grp), f=True)

        # if cmds.objExists(clean_rig_grp) and cmds.objExists(reader_group):
        #     cmds.parent(reader_group, clean_rig_grp)
        #     print('Joint reader created for {} and parented to {}'.format(joint, clean_rig_grp))
        