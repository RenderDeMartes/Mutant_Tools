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

from Mutant_Tools.Utils.External import Ribbonizer
reload(Ribbonizer)
#---------------------------------------------

TAB_FOLDER = '005_Clothes'
PYBLOCK_NAME = 'exec_skirt'

#---------------------------------------------

def create_skirt_block(name = 'Skirt'):

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

    MODULE_FILE = os.path.join(os.path.dirname(__file__), '04_Skirt.json')
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

    block = mt.create_block(name = name, icon = 'Skirt',  attrs = module['attrs'], build_command = module['build_command'], import_command = module['import'])
    config = block[1]
    block = block[0]

    names= ['Fr','L_Fr','L','L_Bk','Bk','R_Bk','R', 'R_Fr']

    rotate = 0
    for num in range(8):
        surface = mel.eval(
            'nurbsPlane -p 0 0 0 -ax 0 0 1 -w 1 -lr 5 -d 3 -u 1 -v 5 -ch 1 -n {};'.format(
                name + '_' + names[num] + nc['guide']))[0]

        cmds.move(0,0,3)
        cmds.move(0.0, 0.0, 0.0, '{}.rotatePivot'.format(surface))
        cmds.rotate(0,rotate,0)
        cmds.parent(surface, block)

        rotate=rotate+45

    cmds.select(block)

    print('{} Created Successfully'.format(name))

#create_skirt_block()

#-------------------------

def build_skirt_block():
    nc, curve_data, setup = mt.import_configs()

    mt.check_is_there_is_base()

    block = cmds.ls(sl=True)
    config = cmds.listConnections(block)[1]
    block = block[0]
    guides = cmds.listRelatives(block, c=True)
    name = block.replace(nc['module'], '')

    # cmds.getAttr('{}.AttrName'.format(config))
    # cmds.getAttr('{}.AttrName'.format(config), asString = True)

    # clean a bit
    clean_ctrl_grp = cmds.group(n=name + nc['ctrl'] + nc['group'], em=True)
    clean_rig_grp = cmds.group(em=True, n='{}{}'.format(block.replace(nc['module'], '_Rig'), nc['group']))
    bind_jnt_grp = '{}{}'.format(setup['rig_groups']['bind_joints'], nc['group'])

    cmds.parent(clean_rig_grp, '{}{}'.format(setup['rig_groups']['misc'], nc['group']))
    cmds.parent(clean_ctrl_grp, setup['base_groups']['control'] + nc['group'])

    # use this locator in case parent is set to new locator
    if cmds.getAttr('{}.SetParent'.format(config)) == 'new_locator':
        block_parent = cmds.spaceLocator(n='{}'.format(str(block).replace(nc['module'], '_Parent' + nc['locator'])))[0]
    else:
        block_parent = cmds.getAttr('{}.SetParent'.format(config))

    left_parent = cmds.spaceLocator(n='{}'.format(str(block).replace(nc['module'], '_LeftParent' + nc['locator'])))[0]
    right_parent = cmds.spaceLocator(n='{}'.format(str(block).replace(nc['module'], '_RightParent' + nc['locator'])))[0]
    cmds.parent(left_parent, right_parent, clean_rig_grp)

    # Master ctrl
    ctrl_parent = mt.curve(input=block_parent,
                           type='octagon',
                           rename=True,
                           custom_name=True,
                           name=name + '_Master' + nc['ctrl'],
                           size=5)
    cmds.rotate(0,0,0)
    mt.assign_color(color='orange')
    root_grp = mt.root_grp()[0]
    mt.match(root_grp, block_parent, r=True, t=True)
    cmds.parentConstraint(block_parent, root_grp)

    #individual ctrls
    master_ctrls = []
    autos = []

    for num, guide in enumerate(guides):
        new_guide = cmds.duplicate(guide, n=guide.replace(nc['guide'], nc['nurb']))
        cmds.parent(new_guide, w=True)

        ctrl_grp, rig_grp, bnd_grp = Ribbonizer.ribbonize(surf_tr=new_guide,
                                                          equal=True,
                                                          num_of_Ctrls=5,
                                                          num_of_Jnts=10,
                                                          prefix=new_guide[0].replace(nc['nurb'], ''),
                                                          constrain=True,
                                                          add_fk=True,
                                                          wire=False,
                                                          middle_ctrl_pos='Start')

        master_ctrl = new_guide[0].replace(nc['nurb'], '') + '_Main' + nc['ctrl']
        master_ctrls.append(master_ctrl)
        root, auto = mt.root_grp(input = master_ctrl, autoRoot=True)
        autos.append(auto)

        cmds.parent(ctrl_grp, clean_ctrl_grp)
        cmds.parent(rig_grp, clean_rig_grp)
        cmds.parent(bnd_grp, bind_jnt_grp)

        if 'R_Fr' in str(guide) or 'R_Bk' in str(guide) or 'L_Fr' in str(guide) or 'L_Bk' in str(guide):
            cmds.setAttr('{}.overrideColor'.format(master_ctrl), 9)

    #automated system for legs
    print(master_ctrls)

    #cmds.parentConstraint(ctrl_parent, clean_ctrl_grp, mo=True)
    cmds.scaleConstraint(ctrl_parent, clean_ctrl_grp, mo=True)
    cmds.parentConstraint(ctrl_parent, clean_ctrl_grp, mo=True)

    #autos : ['Skirt_Fr_Main_Ctrl', 'Skirt_L_Fr_Main_Ctrl', 'Skirt_L_Main_Ctrl', 'Skirt_L_Bk_Main_Ctrl', 'Skirt_Bk_Main_Ctrl', 'Skirt_R_Bk_Main_Ctrl', 'Skirt_R_Main_Ctrl', 'Skirt_R_Fr_Main_Ctrl']

    #hard coding is life!
    oc1=cmds.orientConstraint(ctrl_parent, left_parent, autos[1], mo=True)[0]
    cmds.setAttr('{}.interpType'.format(oc1), 2)
    oc2=cmds.orientConstraint(master_ctrls[1], master_ctrls[7], autos[0], mo=True)[0]
    cmds.setAttr('{}.interpType'.format(oc2), 2)
    oc3=cmds.orientConstraint(master_ctrls[1], master_ctrls[3], autos[2], mo=True)[0]
    cmds.setAttr('{}.interpType'.format(oc3), 2)
    oc4=cmds.orientConstraint(ctrl_parent, left_parent, autos[3], mo=True)[0]
    cmds.setAttr('{}.interpType'.format(oc4), 2)
    oc5=cmds.orientConstraint(master_ctrls[3], master_ctrls[5], autos[4], mo=True)[0]
    cmds.setAttr('{}.interpType'.format(oc5), 2)
    oc6=cmds.orientConstraint(ctrl_parent, right_parent, autos[5], mo=True)[0]
    cmds.setAttr('{}.interpType'.format(oc6), 2)
    oc7=cmds.orientConstraint(master_ctrls[5], master_ctrls[7], autos[6], mo=True)[0]
    cmds.setAttr('{}.interpType'.format(oc7), 2)
    oc8=cmds.orientConstraint(ctrl_parent, right_parent, autos[7], mo=True)[0]
    cmds.setAttr('{}.interpType'.format(oc8), 2)

    #Limit the main auto ctrls
    #front left leg----------------
    mt.line_attr(input=master_ctrls[1], name='Skirt')
    left_front_follow_attr = mt.new_attr(input=master_ctrls[1], name='FollowLeg', min=0, max=1, default=1)
    #left_front_limit_attr = mt.new_attr(input=master_ctrls[1], name='AutomationLimit', min=0, max=180, default=0)

    cmds.connectAttr(left_front_follow_attr, oc1+'.{}W1'.format(left_parent))
    reverse_node = cmds.createNode('reverse', n=master_ctrls[1] + '_Reverse')
    cmds.connectAttr(left_front_follow_attr, '{}.input.inputX'.format(reverse_node))
    cmds.connectAttr('{}.output.outputX'.format(reverse_node), oc1+'.{}W0'.format(ctrl_parent))

    # cmds.transformLimits(autos[1], erz=[False, True], ery=[False, True], erx=[False, False])
    # #mt.connect_md_node(in_x1=left_front_limit_attr, in_x2=1, out_x=autos[1] + '.maxRotLimit.maxRotXLimit', mode='multiply')
    # mt.connect_md_node(in_x1=left_front_limit_attr, in_x2=1, out_x=autos[1] + '.maxRotLimit.maxRotYLimit', mode='multiply')
    # mt.connect_md_node(in_x1=left_front_limit_attr, in_x2=1, out_x=autos[1] + '.maxRotLimit.maxRotZLimit', mode='multiply')

    #back left leg--------------------
    mt.line_attr(input=master_ctrls[3], name='Skirt')
    left_back_follow_attr = mt.new_attr(input=master_ctrls[3], name='FollowLeg', min=0, max=1, default=1)
    #left_back_limit_attr = mt.new_attr(input=master_ctrls[3], name='AutomationLimit', min=0, max=180, default=0)

    cmds.connectAttr(left_back_follow_attr, oc4+'.{}W1'.format(left_parent))
    reverse_node = cmds.createNode('reverse', n=master_ctrls[3] + '_Reverse')
    cmds.connectAttr(left_back_follow_attr, '{}.input.inputX'.format(reverse_node))
    cmds.connectAttr('{}.output.outputX'.format(reverse_node), oc4+'.{}W0'.format(ctrl_parent))

    # front right leg--------------------
    mt.line_attr(input=master_ctrls[7], name='Skirt')
    right_front_follow_attr = mt.new_attr(input=master_ctrls[7], name='FollowLeg', min=0, max=1, default=1)
    # right_front_limit_attr = mt.new_attr(input=master_ctrls[7], name='AutomationLimit', min=0, max=180, default=0)

    cmds.connectAttr(right_front_follow_attr, oc8 + '.{}W1'.format(right_parent))
    reverse_node = cmds.createNode('reverse', n=master_ctrls[7] + '_Reverse')
    cmds.connectAttr(right_front_follow_attr, '{}.input.inputX'.format(reverse_node))
    cmds.connectAttr('{}.output.outputX'.format(reverse_node), oc8 + '.{}W0'.format(ctrl_parent))

    # back right leg--------------------w
    mt.line_attr(input=master_ctrls[5], name='Skirt')
    right_back_follow_attr = mt.new_attr(input=master_ctrls[5], name='FollowLeg', min=0, max=1, default=1)
    # right_front_limit_attr = mt.new_attr(input=master_ctrls[5], name='AutomationLimit', min=0, max=180, default=0)

    cmds.connectAttr(right_back_follow_attr, oc6 + '.{}W1'.format(right_parent))
    reverse_node = cmds.createNode('reverse', n=master_ctrls[5] + '_Reverse')
    cmds.connectAttr(right_back_follow_attr, '{}.input.inputX'.format(reverse_node))
    cmds.connectAttr('{}.output.outputX'.format(reverse_node), oc6 + '.{}W0'.format(ctrl_parent))

    #Create adicional parent systems, new 2 ctrls and 1 master ctrl

    # Side ctrls
    side_ctrl = []
    side_autos = []
    side_parent = [name+'_L_Main'+nc['ctrl'], name+'_R_Main'+nc['ctrl']]
    names = ['L', 'R_']
    for num,loc in enumerate([left_parent, right_parent]):
        ctrl = mt.curve(input=side_parent[num],
                        type='hexagon',
                        rename=True,
                        custom_name=True,
                        name=names[num]+'_'+name+nc['ctrl'],
                        size=1.5)
        cmds.rotate(0,0,0)
        if loc.startswith(nc['right']):
            color = 'red'
        elif loc.startswith(nc['left']):
            color = 'blue'
        else:
            color = 'yellow'
        mt.assign_color(color=color)
        root_grp = mt.root_grp()[0]
        mt.match(root_grp, side_parent[num], r=False, t=True)
        cmds.parent(root_grp, ctrl_parent)
        cmds.parentConstraint(ctrl, loc, mo=False)
        mt.hide_attr(input=ctrl, s=True, t=True)

    print ('Build {} Success'.format(block))



#build_skirt_block()
