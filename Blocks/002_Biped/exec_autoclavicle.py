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
    ik_joint = fk_shoulder_ctrl.replace('_FK'+nc['ctrl'], nc['joint'])

    to_build_ik = [ik_joint]
    if mirror == 'True':
        to_build_ik.append(ik_joint.replace(nc['left'], nc['right']))

    to_build_fk = [fk_shoulder_ctrl]
    if mirror == 'True':
        to_build_fk.append(fk_shoulder_ctrl.replace(nc['left'], nc['right']))
    
    

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
            mt.new_attr(input=clav_ctrl, name='AutoClavicle', min=0, max=1, default=1)

        # create per-axis range attrs on clavicle
        for axis_name in ['X', 'Y', 'Z']:
            if not cmds.attributeQuery('AutoClavicle{}_Start'.format(axis_name), node=clav_ctrl, exists=True):
                mt.new_attr(input=clav_ctrl, name='AutoClavicle{}_Start'.format(axis_name), min=-180, max=180, default=10)
            if not cmds.attributeQuery('AutoClavicle{}_Stop'.format(axis_name), node=clav_ctrl, exists=True):
                mt.new_attr(input=clav_ctrl, name='AutoClavicle{}_Stop'.format(axis_name), min=-180, max=180, default=90)

        # create root for shoulder FK ctrl
        clav_auto_grp = mt.root_grp(input=clav_ctrl, custom=True, custom_name='AutoClavicleFk_Root')[0]

        # create per-axis remapValue nodes before multiplyDivide
        node_name = fk_ctrl.replace('|', '_').replace(':', '_')
        md_node = cmds.createNode('multiplyDivide', n='{}_AutoClavicle_MD'.format(node_name))
        cmds.setAttr('{}.operation'.format(md_node), 1)

        for i, axis in enumerate(['X', 'Y', 'Z']):
            # create remapValue for this axis
            remap_node = cmds.createNode('remapValue', n='{}_AutoClavicle_Remap{}'.format(node_name, axis))

            # connect input rotation axis
            cmds.connectAttr('{}.rotate{}'.format(fk_ctrl, axis), '{}.inputValue'.format(remap_node), f=True)

            # connect start/stop range from clavicle ctrl
            cmds.connectAttr('{}.AutoClavicle{}_Start'.format(clav_ctrl, axis), '{}.inputMin'.format(remap_node), f=True)
            cmds.connectAttr('{}.AutoClavicle{}_Stop'.format(clav_ctrl, axis), '{}.inputMax'.format(remap_node), f=True)
            cmds.setAttr('{}.outputMin'.format(remap_node), 0)
            cmds.setAttr('{}.outputMax'.format(remap_node), 1)

            # connect remapped value to multiplyDivide input1
            if i == 0:
                md_input = 'input1X'
            elif i == 1:
                md_input = 'input1Y'
            else:
                md_input = 'input1Z'

            cmds.connectAttr('{}.outValue'.format(remap_node), '{}.{}'.format(md_node, md_input), f=True)

            # connect original rotation to multiplyDivide input2
            cmds.connectAttr('{}.rotate{}'.format(fk_ctrl, axis), '{}.input2{}'.format(md_node, axis), f=True)

        # create final on/off multiply node
        final_md = cmds.createNode('multiplyDivide', n='{}_AutoClavicle_OnOff_MD'.format(node_name))
        cmds.setAttr('{}.operation'.format(final_md), 1)
        
        # connect first MD output to final MD input1
        cmds.connectAttr('{}.output'.format(md_node), '{}.input1'.format(final_md), f=True)
        
        # connect AutoClavicle on/off attr to input2
        cmds.setAttr('{}.input2X'.format(final_md), 1)
        cmds.setAttr('{}.input2Y'.format(final_md), 1)
        cmds.setAttr('{}.input2Z'.format(final_md), 1)
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

        reader, reader_group, quad_loc = mt.create_joint_reader(joint, push_joint_name=joint + '_Reader', return_all=True)

        if cmds.objExists(misc_group) and cmds.objExists(reader):
            cmds.parent(reader_group, clean_rig_grp)
            print('Joint reader created for {} and parented to {}'.format(joint, misc_group))