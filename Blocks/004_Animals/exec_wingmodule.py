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
TAB_FOLDER = '004_Animals'
PYBLOCK_NAME = 'exec_wingmodule'

#Read name conventions as nc[''] and setup as seup['']
PATH = os.path.dirname(__file__)
PATH = Path(PATH)
PATH_PARTS = PATH.parts[:-2]
FOLDER=''
for f in PATH_PARTS:
	FOLDER = os.path.join(FOLDER, f)

JSON_FILE = os.path.join(FOLDER, 'config', 'name_conventions.json')
with open(JSON_FILE) as json_file:
	nc = json.load(json_file)
#Read curve shapes info
CURVE_FILE = os.path.join(FOLDER, 'config', 'curves.json')
with open(CURVE_FILE) as curve_file:
	curve_data = json.load(curve_file)
#setup File
SETUP_FILE = os.path.join(FOLDER, 'config', 'rig_setup.json')
with open(SETUP_FILE) as setup_file:
	setup = json.load(setup_file)

MODULE_FILE = os.path.join(os.path.dirname(__file__),'01_WingModule.json')
with open(MODULE_FILE) as module_file:
	module = json.load(module_file)

#---------------------------------------------

def create_wingmodule_block(name = 'WingModule'):

    nc, curve_data, setup = mt.import_configs()
    #name checks and block creation
    name = mt.ask_name(text = module['Name'])
    if cmds.objExists('{}{}'.format(name,nc['module'])):
        cmds.warning('Name already exists.')
        return ''

    block = mt.create_block(name = name, icon = 'WingModule',  attrs = module['attrs'], build_command = module['build_command'], import_command = module['import'])
    config = block[1]
    block = block[0]
    name = block.replace(nc['module'],'')

    import Mutant_Tools
    from Mutant_Tools.Utils.External.RdMWings import autoWings, wingModule, BindFeathers, autoFold
    reload(wingModule)

    amount = int(mt.ask_name(ask_for='Amount', text=5))
    axis = mt.ask_name(ask_for='Axis', text='Z')

    #Create main guides:
    first_joint = cmds.joint(p=(0.5, 0, 0), n='{}_Start_Guide'.format(name))
    last_joint = cmds.joint(p=(5, 0, 0), n='{}_End_Guide'.format(name))

    cmds.parent(first_joint, block)

    cmds.select(first_joint, last_joint)
    for i in [first_joint, last_joint]:
        cmds.joint(i, e=True, zso=True, oj="xzy", sao='zup')

    #Create Wings guides
    wingModule.wingModuleFunc(amount=amount, Axis=axis, distanceBack=1)

    cmds.parent('{}_Start_Guide_Wing_000'.format(name), block)
    cmds.select(block)

    cmds.setAttr(config+'.Amount', amount)

    print('{} Created Successfully'.format(name))

#create_wingmodule_block()

#-------------------------

def build_wingmodule_block():

    import Mutant_Tools
    from Mutant_Tools.Utils.External.RdMWings import autoWings, wingModule, BindFeathers, autoFold
    reload(wingModule)

    mt.check_is_there_is_base()

    block = cmds.ls(sl=True)
    config = cmds.listConnections(block)[1]
    block = block[0]
    guides = cmds.listRelatives(block, c=True)
    name = name = block.replace(nc['module'], '')
    amount = cmds.getAttr('{}.Amount'.format(config))

    for guide in guides:
        if guide.endswith('0'):
            feathers_guide = guide
        else:
            main_guide = guide

    main_guide = cmds.duplicate(main_guide, n=main_guide.replace('_Guide', '_JR'))[0]
    feathers_guide = cmds.duplicate(feathers_guide, n=feathers_guide.replace('_Guide', '_JR'))[0]

    cmds.select(main_guide)
    mel.eval('searchReplaceNames {} {} "hierarchy"'.format('Guide', 'JR'))
    cmds.select(feathers_guide)
    mel.eval('searchReplaceNames {} {} "hierarchy"'.format('Guide', 'JR'))

    cmds.parent(feathers_guide, main_guide)
    new_guide = main_guide
    cmds.parent(new_guide, w=True)

    to_build = [main_guide]


    #prep work for right side ------------------------------------------------------

    if cmds.getAttr('{}.Mirror'.format(config)):
        right_guide = mt.duplicate_change_names(input=main_guide, hi=True, search=nc['left'], replace =nc['right'], remove_end_number=False)[0]
        cmds.rename(right_guide, right_guide.replace('1', ''))
        to_build.append(main_guide.replace(nc['left'], nc['right']))
        print(to_build)

    print(to_build)

    clean_ctrl_grp = cmds.group(em=True, name=name + nc['ctrl'] + nc['group'])
    clean_rig_grp = cmds.group(em=True, name=name + '_Rig' + nc['group'])

    cmds.parent(clean_rig_grp, '{}{}'.format(setup['rig_groups']['misc'], nc['group']))
    cmds.parent(clean_ctrl_grp, setup['base_groups']['control'] + nc['group'])

    #build ------------------------------------------------------
    for side_guide in to_build:

        #use this locator in case parent is set to new locator
        if cmds.getAttr('{}.SetParent'.format(config)) == 'new_locator':
            block_parent = cmds.spaceLocator(n='{}'.format(str(side_guide).replace('_JR','_Parent' + nc['locator'])))
        else:
            block_parent = cmds.getAttr('{}.SetParent'.format(config))
            if side_guide.startswith(nc['right']):
                block_parent = block_parent.replace(nc['left'],nc['right'])

        #smart select the colors
        if str(side_guide).startswith(nc['left']):
            color = setup['left_color']
        elif str(side_guide).startswith(nc['right']):
            color = setup['right_color']
        else:
            color = setup['main_color']

        cmds.select(side_guide, side_guide.replace('_Start_JR', '_End_JR'))


        wingModule.createWings(amount=amount,
                               Axis='Z',
                               distanceBack=1,
                               size=1,
                               colorCC=8,
                               name1='Null',
                               name2='Null')

        side_name = side_guide.replace('_Start_JR', '')

        # Old system, hardcoded cleanup
        # Clean a bit


        # Mirror if right
        if side_name.startswith(nc['right']):
            mirror_ctrls = mt.mirror_group('{}_Start_JR_Wing_000_Ctrl_Root_Grp'.format(side_name), world=True)
            mirror_grp = mt.mirror_group('{}_Start_JR'.format(side_name), world=True)
            cmds.parent(mirror_ctrls, mirror_grp,
                        clean_ctrl_grp)

            cmds.parent('{}_Start_JR_FeathersPlane'.format(side_name),
                        clean_rig_grp)

            cmds.parentConstraint(block_parent,  mirror_ctrls, mo=True)
            cmds.scaleConstraint(block_parent,  mirror_ctrls, mo=True)


        else:
            cmds.parent('{}_Start_JR_Wing_000_Ctrl_Root_Grp'.format(side_name), '{}_Start_JR'.format(side_name),
                        clean_ctrl_grp)

            cmds.parent('{}_Start_JR_FeathersPlane'.format(side_name),
                        clean_rig_grp)

            cmds.parentConstraint(block_parent,  '{}_Start_JR_Wing_000_Ctrl_Root_Grp'.format(side_name), mo=True)
            cmds.scaleConstraint(block_parent,  '{}_Start_JR_Wing_000_Ctrl_Root_Grp'.format(side_name), mo=True)

        # Clean Outliner
        for c in cmds.listRelatives(clean_ctrl_grp, type='joint', ad=True):
            cmds.setAttr('{}.drawStyle'.format(c), 2)


    # Create Bind Joints
    bind_jnt_grp = '{}{}'.format(setup['rig_groups']['bind_joints'], nc['group'])

    grp = cmds.group(em=True, n=name + '_Bnd' + '_Grp')
    cmds.parent(grp, bind_jnt_grp)
    joints = cmds.listRelatives(clean_ctrl_grp, type='joint', ad=True)
    for jnt in joints:
        cmds.select(cl=True)
        if cmds.objExists(jnt + nc['joint_bind']):
            continue
        bind_joint = cmds.joint(n=jnt + nc['joint_bind'])
        cmds.parentConstraint(jnt, bind_joint)
        cmds.scaleConstraint(jnt, bind_joint)
        cmds.setAttr('{}.radius'.format(bind_joint), 1.5)
        cmds.parent(bind_joint, grp)



    # build complete ----------------------------------------------------
    print ('Build {} Success'.format(block))


#build_wingmodule_block()
