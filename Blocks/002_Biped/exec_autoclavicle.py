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

        auto_clav_attr = '{}.AutoClavicle'.format(clav_ctrl)
        if not cmds.attributeQuery('AutoClavicle', node=clav_ctrl, exists=True):
            mt.line_attr(input=clav_ctrl, name='Auto Clavicle')
            auto_clav_attr = mt.new_attr(input=clav_ctrl, name='AutoClavicle', min=0, max=1, default=1)

        # create root for shoulder FK ctrl and drive it with switchable weight
        clav_auto_grp = mt.root_grp(input=clav_ctrl, custom=True, custom_name='AutoClavicleFk_Root')[0]

        src_attr = '{}.rotate'.format(fk_ctrl)
        dst_attr = '{}.rotate'.format(clav_auto_grp)
        mt.connect_md_node(in_x1=src_attr,
                           in_x2=auto_clav_attr,
                           out_x=dst_attr,
                           mode='mult',
                           name='{}_AutoClavicle'.format(fk_ctrl),
                           force=True,
                           vector=True)
    

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