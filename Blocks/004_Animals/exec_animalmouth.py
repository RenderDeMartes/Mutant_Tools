from __future__ import absolute_import, division
from maya import cmds
import json
try:
    import importlib;from importlib import reload
except:
    import imp;from imp import reload
import os
from pathlib import Path
import pprint

import Mutant_Tools
import Mutant_Tools.Utils.Rigging
from Mutant_Tools.Utils.Rigging import main_mutant
reload(Mutant_Tools.Utils.Rigging.main_mutant)

mt = main_mutant.Mutant()

#---------------------------------------------

TAB_FOLDER = '004_Animals'
PYBLOCK_NAME = 'exec_animalmouth'

#---------------------------------------------

def create_animalmouth_block(name = 'AnimalMouth'):

    #---------------------------------------------------
    #---------------------------------------------------
    #---------------------------------------------------


    # Read name conventions as nc[''] and setup as seup['']
    PATH = os.path.dirname(__file__)
    PATH = Path(PATH)
    PATH_PARTS = PATH.parts[:-2]
    FOLDER = ''
    for f in PATH_PARTS:
        FOLDER = os.path.join(FOLDER, f)

    MODULE_FILE = os.path.join(os.path.dirname(__file__), '06_AnimalMouth.json')
    with open(MODULE_FILE) as module_file:
        module = json.load(module_file)

    nc, curve_data, setup = mt.import_configs()

    #---------------------------------------------------
    #---------------------------------------------------
    #---------------------------------------------------

    #name checks and block creation
    name = mt.ask_name(text = module['Name'])
    if cmds.objExists('{}{}'.format(name,nc['module'])):
        cmds.warning('Name already exists.')
        return ''
    side_amount = mt.ask_name(ask_for = 'SideAmount', text=3)
    side_amount = int(side_amount)

    block = mt.create_block(name = name, icon = 'AnimalMouth',  attrs = module['attrs'], build_command = module['build_command'], import_command = module['import'])
    config = block[1]
    block = block[0]

    left_orient_lip = mt.create_joint_guide(name=nc['left'] + name + '_Orient')
    cmds.move(3, 0.5, (side_amount+1)*-1)
    cmds.rotate(0, 90, 0)
    cmds.parent(left_orient_lip, block)


    upr_grp = cmds.group(em=True, n=nc['left'] + name+'_Upr'+nc['group'])
    mouthCenter = mt.create_joint_guide(name=name + '_Upr_Center')
    cmds.move(0, 1, 0)
    cmds.parent(mouthCenter, upr_grp)

    for num in range(side_amount):
        guide = mt.create_joint_guide(name=nc['left'] + name + 'Upr_'+ str(num))
        cmds.move(3, 1, (num)*-1)
        cmds.rotate(0, 90, 0)
        cmds.parent(guide, upr_grp)

    lwr_grp = cmds.group(em=True, n=nc['left'] + name + '_Lwr' + nc['group'])
    mouthCenter = mt.create_joint_guide(name=name + '_Lwr_Center')
    cmds.parent(mouthCenter, lwr_grp)
    for num in range(side_amount):
        guide = mt.create_joint_guide(name=nc['left'] + name + 'Lwr_' + str(num))
        cmds.move(3, 0, (num) * -1)
        cmds.rotate(0, 90, 0)
        cmds.parent(guide, lwr_grp)

    cmds.parent(lwr_grp, upr_grp, block)
    cmds.select(block)

    print('{} Created Successfully'.format(name))

#create_animalmouth_block()

#-------------------------

def build_animalmouth_block():

    nc, curve_data, setup = mt.import_configs()

    mt.check_is_there_is_base()

    block = cmds.ls(sl=True)
    config = cmds.listConnections(block)[1]
    block = block[0]
    guides = cmds.listRelatives(block, c=True)
    name = block.replace(nc['module'],'')


    #use this locator in case parent is set to new locator
    if cmds.getAttr('{}.SetParent'.format(config)) == 'new_locator':
        block_parent = cmds.spaceLocator( n = '{}'.format(str(block).replace(nc['module'],'_Parent' + nc['locator'])))
    else:
        block_parent = cmds.getAttr('{}.SetParent'.format(config))

    #Clean groups for later
    clean_ctrl_grp = cmds.group(em=True, name=name + nc['ctrl'] + nc['group'])
    clean_rig_grp = cmds.group(em=True, name=name + '_Rig' + nc['group'])

    cmds.parent(clean_rig_grp, '{}{}'.format(setup['rig_groups']['misc'], nc['group']))
    cmds.parent(clean_ctrl_grp, setup['base_groups']['control'] + nc['group'])

    cmds.parentConstraint(block_parent, clean_ctrl_grp, mo=True)
    cmds.scaleConstraint(block_parent, clean_ctrl_grp, mo=True)

    number_guides = []
    for guide in guides:
        if 'Orient' in guide:
            orient_guide = guide
        elif 'Upr' in guide:
            upr_grp = guide
        else:
            lwr_grp = guide

    modes_data = {}

    for grp in [upr_grp, lwr_grp]:

        if 'Upr' in grp:
            mode = 'Up'
            color = 'yellow'
        else:
            mode = 'Dw'
            color = 'purple'

        mode_dic = {}

        guides = cmds.listRelatives(grp, c=True)
        number_guides = []
        for guide in guides:
            if 'Center' in guide:
                center_guide = guide
            else:
                number_guides.append(guide)

        number_guides = sorted(number_guides)

        lips_guides = [center_guide]+number_guides+[orient_guide]

        print('#'*20)
        print(lips_guides)

        # Retrieve the positions of the joints
        positions = [cmds.xform(joint, query=True, translation=True, worldSpace=True) for joint in lips_guides]
        mirrored_positions = [[-pos[0], pos[1], pos[2]] for pos in positions]

        # Create the curve with CVs at the positions of the joints
        l_lips_curve = cmds.curve(degree=3, point=positions, n="{}{}_{}{}".format(nc['left'], name,mode, nc['curve']))
        r_lips_curve = cmds.curve(degree=3, point=mirrored_positions, n="{}{}_{}{}".format(nc['right'], name, mode, nc['curve']))

        lips_curve = cmds.attachCurve(l_lips_curve, r_lips_curve, ch=False, rpo=False, kmk=True, m=1, bb=0.5, bki=True, p=0.1, n= name+'_'+mode+nc['curve'])[0]
        cvs = cmds.getAttr('{}.spans'.format(lips_curve)) + 3

        cmds.parent(lips_curve, clean_rig_grp)

        cmds.delete(r_lips_curve)
        cmds.delete(l_lips_curve)

        #Make sure curve is in correct orientation
        cmds.select('{}.cv[0]'.format(lips_curve))
        zero_cls = cmds.cluster()[1]
        cmds.select('{}.cv[{}]'.format(lips_curve, cvs))
        one_cls = cmds.cluster()[1]
        if cmds.getAttr('{}.originX'.format(zero_cls)) < cmds.getAttr('{}.originX'.format(one_cls)):
            cmds.reverseCurve(lips_curve, ch=False, replaceOriginal=True)
        cmds.delete(zero_cls, one_cls)

        # Create clusters per CV
        all_cls = []
        for num in range(cvs):
            cluster = cmds.cluster(f'{lips_curve}.cv[{num}]')[1]
            all_cls.append(cluster)

        cmds.parent(all_cls, clean_rig_grp)

        # Organize clusters and rename them
        # Find the middle element index
        middle_index = len(all_cls) // 2

        # Separate the list into left and right parts
        left_clusters = all_cls[:middle_index]
        left_clusters = reversed(left_clusters)
        right_clusters = all_cls[middle_index + 1:]

        print('#' * 20)
        print(all_cls[middle_index])
        print('#' * 20)
        print(left_clusters)
        print('#' * 20)
        print(right_clusters)

        #Rename the clusters
        left_cls = []
        right_cls = []

        center_cls = cmds.rename(all_cls[middle_index], f"C_{name}_{mode}{nc['cluster']}")
        # Rename left clusters
        right_ctrls = []
        right_locs = []
        left_ctrls = []
        left_locs =[]

        size = mt.get_distance_between(number_guides[1], number_guides[2])

        # Create groups for organize and mirror
        left_loc_grp = cmds.group(em=True, n=f"{nc['left']}{mode}_{name}_Loc{nc['group']}")
        left_ctrl_grp = cmds.group(em=True, n=f"{nc['left']}{mode}_{name}_Ctrl{nc['group']}")
        right_loc_grp = cmds.group(em=True, n=f"{nc['right']}{mode}_{name}_Loc{nc['group']}")
        right_ctrl_grp = cmds.group(em=True, n=f"{nc['right']}{mode}_{name}_Ctrl{nc['group']}")


        for index, cluster in enumerate(left_clusters):
            cls = cmds.rename(cluster, f"{nc['left']}{name}_{mode}_{index}{nc['cluster']}")
            left_cls.append(cls)

            guide = lips_guides[index+1]
            left_loc = cmds.spaceLocator(n=cls.replace(nc['cluster'], nc['locator']))[0]
            left_loc_root, left_loc_auto = mt.root_grp(autoRoot=True)
            cmds.parent(left_loc_root, left_loc_grp)
            right_loc = cmds.spaceLocator(n=left_loc.replace(nc['left'], nc['right']))[0]
            right_loc_root = mt.root_grp()
            cmds.parent(right_loc_root, right_loc_grp)

            mt.match(left_loc_root, guide)
            mt.match(right_loc_root, guide)

            left_ctrl = mt.curve(input=guide,
                            type='sphere',
                            rename=True,
                            custom_name=True,
                            name=left_loc.replace(nc['locator'], nc['ctrl']),
                            size=size)
            left_ctrls.append(left_ctrl)
            mt.assign_color(color=color)
            left_root_grp = mt.root_grp()[0]
            cmds.parent(left_root_grp, left_ctrl_grp)
            mt.match(left_root_grp, guide, r=True, t=True)
            # Fancy way to make ctrls keep correct distance
            trans_attr = mt.new_attr(left_root_grp, name='ConnectMult', min=0.1, max=9999, default=1.5)

            mt.connect_md_node(in_x1='{}.translateX'.format(left_ctrl), in_x2=trans_attr,
                               out_x='{}.translateX'.format(left_loc), mode='multiply')
            mt.connect_md_node(in_x1='{}.translateY'.format(left_ctrl), in_x2=trans_attr,
                               out_x='{}.translateY'.format(left_loc), mode='multiply')
            mt.connect_md_node(in_x1='{}.translateZ'.format(left_ctrl), in_x2=trans_attr,
                               out_x='{}.translateZ'.format(left_loc), mode='multiply')
            mt.connect_md_node(in_x1='{}.rotateX'.format(left_ctrl), in_x2=1,
                               out_x='{}.rotateX'.format(left_loc), mode='multiply')
            mt.connect_md_node(in_x1='{}.rotateY'.format(left_ctrl), in_x2=1,
                               out_x='{}.rotateY'.format(left_loc), mode='multiply')
            mt.connect_md_node(in_x1='{}.rotateZ'.format(left_ctrl), in_x2=1,
                               out_x='{}.rotateZ'.format(left_loc), mode='multiply')

            #Clean a bit inital shapes
            if 'Up' in left_ctrl:
                mt.translate_shape(input=left_ctrl, x=0, y=0.5, z=0)
            else:
                mt.translate_shape(input=left_ctrl, x=0, y=-0.5, z=0)

            cmds.parentConstraint(left_loc, cls, mo=True)


            #Right Side
            right_ctrl = mt.curve(input=guide,
                                 type='sphere',
                                 rename=True,
                                 custom_name=True,
                                 name=right_loc.replace(nc['locator'], nc['ctrl']),
                                 size=size)

            mt.assign_color(color=color)
            right_root_grp = mt.root_grp()[0]
            cmds.parent(right_root_grp, right_ctrl_grp)

            mt.match(right_root_grp, guide, r=True, t=True)

            #Fancy way to make ctrls keep correct distance
            trans_attr = mt.new_attr(right_root_grp, name='ConnectMult', min=0.1, max=9999, default=1.5)

            mt.connect_md_node(in_x1='{}.translateX'.format(right_ctrl), in_x2=trans_attr,
                               out_x='{}.translateX'.format(right_loc), mode='multiply')
            mt.connect_md_node(in_x1='{}.translateY'.format(right_ctrl), in_x2=trans_attr,
                               out_x='{}.translateY'.format(right_loc), mode='multiply')
            mt.connect_md_node(in_x1='{}.translateZ'.format(right_ctrl), in_x2=trans_attr,
                               out_x='{}.translateZ'.format(right_loc), mode='multiply')
            mt.connect_md_node(in_x1='{}.rotateX'.format(right_ctrl), in_x2=1,
                               out_x='{}.rotateX'.format(right_loc), mode='multiply')
            mt.connect_md_node(in_x1='{}.rotateY'.format(right_ctrl), in_x2=1,
                               out_x='{}.rotateY'.format(right_loc), mode='multiply')
            mt.connect_md_node(in_x1='{}.rotateZ'.format(right_ctrl), in_x2=1,
                               out_x='{}.rotateZ'.format(right_loc), mode='multiply')

            #Clean a bit initial shapes
            if 'Up' in right_ctrl:
                mt.translate_shape(input=right_ctrl, x=0, y=0.5, z=0)
            else:
                mt.translate_shape(input=right_ctrl, x=0, y=-0.5, z=0)

            right_ctrls.append(right_ctrl)
            right_locs.append(right_loc)
            left_locs.append(left_loc)

        mirror_ctrl_grp = mt.mirror_group(right_ctrl_grp, world=True)
        mirror_loc_grp = mt.mirror_group(right_loc_grp, world=True)

        cmds.parent(mirror_ctrl_grp, left_ctrl_grp, clean_ctrl_grp)
        cmds.parent(mirror_loc_grp, left_loc_grp, clean_rig_grp)

        # Rename right clusters
        for index, cluster in enumerate(right_clusters):
            cls = cmds.rename(cluster, f"{nc['right']}{name}_{mode}_{index}{nc['cluster']}")
            right_cls.append(cls)

            cmds.parentConstraint(right_locs[index], cls, mo=True)

        #Create Center Front Controllers
        center_loc = cmds.spaceLocator(n=center_cls.replace(nc['cluster'], nc['locator']))[0]
        center_loc_root = mt.root_grp()

        guide = center_guide
        mt.match(center_loc_root, guide)
        ctrl = mt.curve(input=guide,
                        type='sphere',
                        rename=True,
                        custom_name=True,
                        name=center_loc.replace(nc['locator'], nc['ctrl']),
                        size=size)
        mt.assign_color(color=color)
        root_grp = mt.root_grp()[0]
        mt.match(root_grp, guide, r=True, t=True)
        trans_attr = mt.new_attr(root_grp, name='ConnectMult', min=0.1, max=9999, default=1.5)

        mt.connect_md_node(in_x1='{}.translateX'.format(ctrl), in_x2=trans_attr,
                           out_x='{}.translateX'.format(center_loc), mode='multiply')
        mt.connect_md_node(in_x1='{}.translateY'.format(ctrl), in_x2=trans_attr,
                           out_x='{}.translateY'.format(center_loc), mode='multiply')
        mt.connect_md_node(in_x1='{}.translateZ'.format(ctrl), in_x2=trans_attr,
                           out_x='{}.translateZ'.format(center_loc), mode='multiply')
        mt.connect_md_node(in_x1='{}.rotateX'.format(ctrl), in_x2=1,
                           out_x='{}.rotateX'.format(center_loc), mode='multiply')
        mt.connect_md_node(in_x1='{}.rotateY'.format(ctrl), in_x2=1,
                           out_x='{}.rotateY'.format(center_loc), mode='multiply')
        mt.connect_md_node(in_x1='{}.rotateZ'.format(ctrl), in_x2=1,
                           out_x='{}.rotateZ'.format(center_loc), mode='multiply')
        # Clean a bit inital shapes
        if 'Up' in ctrl:
            mt.translate_shape(input=ctrl, x=0, y=0.5, z=0)
        else:
            mt.translate_shape(input=ctrl, x=0, y=-0.5, z=0)

        cmds.parentConstraint(center_loc, center_cls, mo=True)

        cmds.parent(root_grp, clean_ctrl_grp)
        cmds.parent(center_loc_root, clean_rig_grp)

        #Create up front center
        #Lips_Up_Main_Ctrl
        main_center_loc = cmds.spaceLocator(n=name+'_'+ mode +'_Main' + nc['locator'])[0]
        root_loc_grp = mt.root_grp()[0]
        mt.match(root_loc_grp, center_loc, r=True, t=True)

        main_center_ctrl = mt.curve(input=main_center_loc,
                        type='square',
                        rename=True,
                        custom_name=True,
                        name=name+'_'+mode+'_Main'+nc['ctrl'],
                        size=size*1.5)
        mt.assign_color(color=color)
        root_grp = mt.root_grp()[0]
        mt.match(root_grp, center_loc, r=True, t=True)

        # Fancy way to make ctrls keep correct distance
        trans_attr = mt.new_attr(root_grp, name='ConnectMult', min=0.1, max=9999, default=1)

        mt.connect_md_node(in_x1='{}.translateX'.format(main_center_ctrl), in_x2=trans_attr,
                           out_x='{}.translateX'.format(main_center_loc), mode='multiply')
        mt.connect_md_node(in_x1='{}.translateY'.format(main_center_ctrl), in_x2=trans_attr,
                           out_x='{}.translateY'.format(main_center_loc), mode='multiply')
        mt.connect_md_node(in_x1='{}.translateZ'.format(main_center_ctrl), in_x2=trans_attr,
                           out_x='{}.translateZ'.format(main_center_loc), mode='multiply')
        mt.connect_md_node(in_x1='{}.rotateX'.format(main_center_ctrl), in_x2=1,
                           out_x='{}.rotateX'.format(main_center_loc), mode='multiply')
        mt.connect_md_node(in_x1='{}.rotateY'.format(main_center_ctrl), in_x2=1,
                           out_x='{}.rotateY'.format(main_center_loc), mode='multiply')
        mt.connect_md_node(in_x1='{}.rotateZ'.format(main_center_ctrl), in_x2=1,
                           out_x='{}.rotateZ'.format(main_center_loc), mode='multiply')
        mt.connect_md_node(in_x1='{}.scaleX'.format(main_center_ctrl), in_x2=1,
                           out_x='{}.scaleX'.format(main_center_loc), mode='multiply')
        mt.connect_md_node(in_x1='{}.scaleY'.format(main_center_ctrl), in_x2=1,
                           out_x='{}.scaleY'.format(main_center_loc), mode='multiply')
        mt.connect_md_node(in_x1='{}.scaleZ'.format(main_center_ctrl), in_x2=1,
                           out_x='{}.scaleZ'.format(main_center_loc), mode='multiply')

        cmds.parent(root_grp, clean_ctrl_grp)
        cmds.parent(root_loc_grp, clean_rig_grp)

        #Organize
        mode_dic['Center_Loc'] = center_loc
        mode_dic['Left_Locs'] = left_locs
        mode_dic['Right_Locs'] = right_locs
        mode_dic['Center_Ctr'] = ctrl
        mode_dic['Left_Ctrs'] = left_ctrls
        mode_dic['Right_Ctrs'] = right_ctrls
        mode_dic['Main_Center_Loc'] = main_center_loc
        mode_dic['Main_Center_Ctr'] = main_center_ctrl

        modes_data[mode] = mode_dic

    #Create Corner Setup
    pprint.pprint(modes_data)

    for side in [nc['left'], nc['right']]:

        loc = cmds.spaceLocator(n=side + name + '_Main' + nc['locator'])[0]
        loc_root, loc_auto = mt.root_grp(autoRoot=True)
        cmds.delete(cmds.parentConstraint(orient_guide, loc_root))

        side_main_ctrl = mt.curve(input='',
                                  type='square',
                                  rename=True,
                                  custom_name=True,
                                  name=side + name + '_Main' + nc['ctrl'],
                                  size=size*1.5)

        if side == nc['right']:
            mt.assign_color(color='red')
        else:
            mt.assign_color(color='blue')
        left_main_ctrl_root = mt.root_grp()[0]

        # Attrs
        mt.line_attr(input=side_main_ctrl, name='Lips')
        mode_attr = mt.new_enum(input=side_main_ctrl, name='mode', enums='BSP:RIG')
        move_mult_attr = mt.new_attr(input=side_main_ctrl, name='MovementMult', min=0.1, max=10, default=1)
        sub_move_mult_attr = mt.new_attr(input=side_main_ctrl, name='SubMovementMult', min=0.1, max=10, default=1)

        # Make pretty
        cmds.select('{}.cv[0:4]'.format(side_main_ctrl))
        cmds.rotate(90, 0, 0, r=True)
        # cmds.select('{}.cv[2:3]'.format(side_main_ctrl))
        # cmds.scale(0,ctrl_size/3,0,r=True)
        # cmds.move(ctrl_size/2,0,0,r=True)
        mt.hide_attr(side_main_ctrl, s=True)

        # create sub controller with modes in case we dont use BS
        sub_main_ctrl = mt.curve(input='',
                                 type='square',
                                 rename=True,
                                 custom_name=True,
                                 name=side + name + '_Sub' + nc['ctrl'],
                                 size=size / 2)
        if side == nc['right']:
            mt.assign_color(color='red')
        else:
            mt.assign_color(color='blue')
        left_sub_ctrl_root = mt.root_grp()[0]

        cmds.select('{}.cv[0:4]'.format(sub_main_ctrl))
        cmds.rotate(90, 0, 0, r=True)
        # cmds.select('{}.cv[2:3]'.format(sub_main_ctrl))
        # cmds.scale(0,ctrl_size/4,0,r=True)
        # cmds.move(ctrl_size/2,0,0,r=True)
        mt.hide_attr(sub_main_ctrl, s=True)
        # cmds.select('{}.cv[0:4]'.format(sub_main_ctrl))
        # cmds.scale(ctrl_size/4,ctrl_size/4,ctrl_size/4,r=True)

        cmds.parent(left_sub_ctrl_root, side_main_ctrl)

        # direct connect with mult
        mt.connect_md_node(in_x1=sub_move_mult_attr, in_x2='{}.rotate'.format(sub_main_ctrl),
                           out_x='{}.rotate'.format(loc), mode='multiply', vector=True)
        mt.connect_md_node(in_x1=sub_move_mult_attr, in_x2='{}.translate'.format(sub_main_ctrl),
                           out_x='{}.translate'.format(loc), mode='multiply', vector=True)
        # mt.connect_md_node(in_x1=sub_move_mult_attr, in_x2='{}.scale'.format(sub_main_ctrl), out_x= '{}.scale'.format(loc), mode='multiply', vector=True )

        # -----------------------------------------------------
        # Connect main siude ctrl
        md_rotate = mt.connect_md_node(in_x1=move_mult_attr, in_x2='{}.rotate'.format(side_main_ctrl),
                                       out_x='{}.rotate'.format(loc_auto), mode='multiply', vector=True)
        md_translate = mt.connect_md_node(in_x1=move_mult_attr, in_x2='{}.translate'.format(side_main_ctrl),
                                          out_x='{}.translate'.format(loc_auto), mode='multiply', vector=True)
        # md_scale = mt.connect_md_node(in_x1=move_mult_attr, in_x2='{}.scale'.format(side_main_ctrl), out_x= '{}.scale'.format(loc_auto), mode='multiply', vector=True )

        mt.connect_md_node(in_x1=mode_attr, in_x2='{}.output'.format(md_rotate), out_x='{}.rotate'.format(loc_auto),
                           mode='multiply', vector=True, force=True)
        mt.connect_md_node(in_x1=mode_attr, in_x2='{}.output'.format(md_translate),
                           out_x='{}.translate'.format(loc_auto), mode='multiply', vector=True, force=True)
        # mt.connect_md_node(in_x1=mode_attr, in_x2='{}.output'.format(md_scale), out_x= '{}.scale'.format(loc_auto), mode='multiply', vector=True, force=True)

        # Flip
        if side == nc['right']:
            loc_root = mt.mirror_group(loc_root, world=True)
            left_main_ctrl_root = mt.mirror_group(left_main_ctrl_root, world=True)

        cmds.parent(loc_root, clean_rig_grp)
        cmds.parent(left_main_ctrl_root, clean_ctrl_grp)

        pprint.pprint(modes_data)
        #Manual Connections to Cluster locators
        for mode in modes_data:
            center_loc = modes_data[mode]['Center_Loc']
            left_locs = modes_data[mode]['Left_Locs']
            right_locs = modes_data[mode]['Right_Locs']
            center_ctrl = modes_data[mode]['Center_Ctr']
            left_ctrls = modes_data[mode]['Left_Ctrs']
            right_ctrls = modes_data[mode]['Right_Ctrs']
            main_center_loc = modes_data[mode]['Main_Center_Loc']
            main_center_ctrl = modes_data[mode]['Main_Center_Ctr']

            forward = list(enumerate(left_locs))
            backward = list(reversed(forward))

            if side == nc['left']:
                list_to_use = left_locs
            else:
                list_to_use = right_locs

            for num, side_loc in enumerate(list_to_use):
                auto = cmds.listRelatives(side_loc, p=True)
                pc = cmds.parentConstraint(main_center_loc, loc, auto, mo=True)[0]
                cmds.setAttr(pc + '.' + main_center_loc + 'W0', backward[num][0])
                cmds.setAttr(pc + '.' + loc + 'W1', forward[num][0])
                cmds.setAttr(pc + '.interpType', 2)  # shortest

            auto = cmds.listRelatives(center_loc, p=True)
            pc = cmds.parentConstraint(main_center_loc, auto, mo=True)[0]

    #--------------------------------------------------------------------------------------


    print ('Build {} Success'.format(block))



#build_animalmouth_block()
