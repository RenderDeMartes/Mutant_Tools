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

TAB_FOLDER = '004_Animals'
PYBLOCK_NAME = 'exec_tail'

#---------------------------------------------

def create_tail_block(name = 'Tail'):

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

    MODULE_FILE = os.path.join(os.path.dirname(__file__), '02_Tail.json')
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
    amount = int(mt.ask_name(text=5, ask_for = 'Tail Nurb'))
    block = mt.create_block(name = name, icon = 'Tail',  attrs = module['attrs'], build_command = module['build_command'], import_command = module['import'])
    config = block[1]
    block = block[0]
      
    #cmds.getAttr('{}.AttrName'.format(config)) #get attrs from config
    #cmds.getAttr('{}.AttrName'.format(config), asString = True) #for enums
    #joint_one = mt.create_joint_guide(name = name) #guide base with shapes

    surface = mel.eval(
        'nurbsPlane -p 0 0 0 -ax 1 0 0 -w {} -lr 0.2 -d 3 -u {} -v 1 -ch 0 -n {};'.format(amount, amount,
            name + nc['guide']))[0]
    cmds.parent(surface, block)

    cmds.select(block)

    print('{} Created Successfully'.format(name))

#create_tail_block()

#-------------------------

def build_tail_block():

    nc, curve_data, setup = mt.import_configs()

    mt.check_is_there_is_base()

    block = cmds.ls(sl=True)
    config = cmds.listConnections(block)[1]
    block = block[0]
    guides = cmds.listRelatives(block, c=True)
    name = block.replace(nc['module'], '')

    # clean a bit
    clean_ctrl_grp = cmds.group(n=name + nc['ctrl'] + nc['group'], em=True)
    clean_rig_grp = cmds.group(em=True, n='{}{}'.format(block.replace(nc['module'], '_Rig'), nc['group']))
    bind_jnt_grp = '{}{}'.format(setup['rig_groups']['bind_joints'], nc['group'])

    cmds.parent(clean_rig_grp, '{}{}'.format(setup['rig_groups']['misc'], nc['group']))
    cmds.parent(clean_ctrl_grp, setup['base_groups']['control'] + nc['group'])

    # use this locator in case parent is set to new locator
    if cmds.getAttr('{}.SetParent'.format(config)) == 'new_locator':
        block_parent = cmds.spaceLocator(n='{}'.format(str(block).replace(nc['module'], '_Parent' + nc['locator'])))
    else:
        block_parent = cmds.getAttr('{}.SetParent'.format(config))

    for num, guide in enumerate(guides):

        new_guide = cmds.duplicate(guide, n=guide.replace(nc['guide'], nc['nurb']))
        cmds.parent(new_guide, w=True)

        ctrl_grp, rig_grp, bnd_grp = Ribbonizer.ribbonize(surf_tr=new_guide,
                                                          equal=False,
                                                          num_of_Ctrls=cmds.getAttr('{}.FkCtrls'.format(config)),
                                                          num_of_Jnts=cmds.getAttr('{}.Joints'.format(config)),
                                                          prefix=name + '_' + str(num + 1),
                                                          constrain=True,
                                                          add_fk=True,
                                                          wire=False,
                                                          middle_ctrl_pos='Start')

        print('{}_1_Main{}'.format(name, nc['ctrl']))
        rotator_ctrl = mt.curve(input='{}_1_Main{}'.format(name, nc['ctrl']),
                        type='sun',
                        rename=True,
                        custom_name=True,
                        name='{}_1_Rotator{}'.format(name, nc['ctrl']),
                        size=1)

        mt.assign_color(color='purple')
        root_grp = mt.root_grp()[0]
        mt.match(root_grp, '{}_1_Main{}'.format(name, nc['ctrl']), r=True, t=True)
        cmds.parent(root_grp, '{}_1_Main{}'.format(name, nc['ctrl']))
        mt.hide_attr(input=rotator_ctrl, t=True, r=False, s=True, v=False, rotate_order=True)

        #Tail ctrl automation
        for c in cmds.listRelatives(ctrl_grp, ad=True):
            if c.endswith(nc['ctrl']) and 'fk' in c:
                print(c)
                root, auto = mt.root_grp(input=c, autoRoot=True)
                cmds.connectAttr('{}.rotate'.format(rotator_ctrl), '{}.rotate'.format(auto))

        cmds.parent(ctrl_grp, clean_ctrl_grp)
        cmds.parent(rig_grp, clean_rig_grp)
        cmds.parent(bnd_grp, bind_jnt_grp)

        cmds.parentConstraint(block_parent, clean_ctrl_grp, mo=True)
        cmds.scaleConstraint(block_parent, clean_ctrl_grp, mo=True)


    print('Build {} Success'.format(block))

#build_tail_block()
