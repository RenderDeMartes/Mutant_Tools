from maya import cmds
from maya import OpenMaya

import json
import imp
import os
from pathlib import Path

import Mutant_Tools
import Mutant_Tools.Utils.Rigging
from Mutant_Tools.Utils.Rigging import main_mutant
imp.reload(Mutant_Tools.Utils.Rigging.main_mutant)

mt = main_mutant.Mutant()

#---------------------------------------------

TAB_FOLDER = '02_Biped'
PYBLOCK_NAME = 'exec_head'

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

MODULE_FILE = os.path.join(os.path.dirname(__file__),'05_Head.json')
with open(MODULE_FILE) as module_file:
	module = json.load(module_file)



#---------------------------------------------

def create_head_block(name = 'Head'):

    #name checks and block creation
    name = mt.ask_name(text = module['Name'], ask_for = 'Neck and Head Names (Separete with a , )')

    if cmds.objExists('{}{}'.format(name.replace(',','_'),nc['module'])):
        cmds.warning('Name already exists.')
        return ''

   
    block = mt.create_block(name = name, icon = 'HeadNeck',  attrs = module['attrs'], build_command = module['build_command'], import_command = module['import'])
    config = block[1]
    block = block[0]
    
    neck_name = name.split(',')[0]
    head_name = name.split(',')[1]

    cmds.select(cl=True)
    neck_guide = mt.create_joint_guide(name = neck_name)
    cmds.move(0,0,0)
    head_guide = mt.create_joint_guide(name = head_name)
    cmds.move(0,5,1.5)
    head_guideEnd = mt.create_joint_guide(name = head_name + 'End')
    cmds.move(0,8.5,1.5)

    cmds.parent(head_guideEnd, head_guide)
    cmds.parent(head_guide, neck_guide)
    cmds.parent(neck_guide, block)
    cmds.select(block)

    mt.orient_joint(input = neck_guide)
    cmds.setAttr("{}.jointOrientX".format(head_guideEnd), 0)
    cmds.setAttr("{}.jointOrientY".format(head_guideEnd), 0)
    cmds.setAttr("{}.jointOrientZ".format(head_guideEnd), 0)

    print('{} Created Successfully'.format(name))

#create_head_block()

#-------------------------

def build_head_block():

    mt.check_is_there_is_base()

    block = cmds.ls(sl=True)
    config = cmds.listConnections(block)[1]
    block = block[0]
    guide = cmds.listRelatives(block, c=True)[0]

    #groups for later cleaning
    clean_rig_grp = ''
    clean_ctrl_grp = ''

    #cmds.getAttr('{}.AttrName'.format(config))
    #cmds.getAttr('{}.AttrName'.format(config), asString = True)

    #orient the joints
    mt.orient_joint(input = guide)
    new_guide = mt.duplicate_and_remove_guides(guide)

    #use this locator in case parent is set to new locator
    if cmds.getAttr('{}.SetParent'.format(config)) == 'new_locator':
        block_parent = cmds.spaceLocator( n = '{}'.format(str(block).replace(nc['module'],'_Parent' + nc['locator'])))
    else:
        block_parent = cmds.getAttr('{}.SetParent'.format(config))

    #config--------------------------

    ribbon_amount = cmds.getAttr('{}.SecundaryRibbon'.format(config))
    ctrl_type = cmds.getAttr('{}.HeadCtrlType'.format(config), asString = True)
    ctrl_size = cmds.getAttr('{}.CtrlSize'.format(config))
    ctrl_color = cmds.getAttr('{}.CtrlColor'.format(config), asString = True)

    neck_joint = new_guide
    head_joint = cmds.listRelatives(new_guide, c=True)[0]

    game_parent = cmds.getAttr('{}.SetGameParent'.format(config), asString = True)


    #Build--------------------------
    cmds.select(neck_joint)
    dumb_head = cmds.joint(n = head_joint.replace(nc['joint'], nc['null'] + nc['joint']))
    mt.match(dumb_head , head_joint)
    cmds.pointConstraint(head_joint, dumb_head)

    ribbon = mt.ribbon_between(start=neck_joint, end=dumb_head, divisions=ribbon_amount , name=str(neck_joint).replace(nc['joint'], ''), size = ctrl_size)
    
    '''
    ribbon =    {'surface':[basic_ribbon['surface'],ctrl_surface], 
				'follicles':basic_ribbon['follicles'],
				'fol_joints':basic_ribbon['fol_joints'],
				'ctrl_joints':basic_ribbon['ctrl_joints'],
				'controllers':basic_ribbon['controllers'],
				'controllers_grp':basic_ribbon['controllers_grp']}
    '''

    #Fk chain neck and head
    cmds.select(neck_joint, head_joint)
    fk_chain = mt.fk_chain(input = '', 
                           size = ctrl_size, 
                           color = ctrl_color, 
                           curve_type = ctrl_type)
    
    #blends#changed name to offset since blends are now a dif block
    neck_blends_grp = mt.root_grp(input = fk_chain[0], custom = True, custom_name = '_Offset', autoRoot = False, replace_nc = False)[0]
    head_blends_grp = mt.root_grp(input = fk_chain[1], custom = True, custom_name = '_Root', autoRoot = False, replace_nc = False)[0]


    #bind joints
    bind_joints = []
    for jnt in ribbon['fol_joints']:
        try: last_bind_joint = bind_joint
        except:pass
        bind_joint = mt.duplicate_change_names( input = jnt, hi = False, search=nc['follicle']+nc['joint'], replace = nc['joint_bind'])[0]
        cmds.delete(cmds.pickWalk(bind_joint, d='down'))#clean th dirty constraint
        cmds.parentConstraint(jnt, bind_joint)
        cmds.scaleConstraint(jnt, bind_joint)
        cmds.setAttr('{}.segmentScaleCompensate'.format(bind_joint), 0)

        #clean bind joints and radius to 1.5
        cmds.setAttr('{}.radius'.format(bind_joint), 1.5)
        print (bind_joint)
        try:
            cmds.parent(bind_joint,last_bind_joint)
        except:
            cmds.parent(bind_joint, w=True)
        
        bind_joints.append(bind_joint)

    cmds.select(cl=True)
    head_bind_joint = cmds.joint(n = head_joint.replace(nc['joint'], nc['joint_bind']))
    cmds.parentConstraint(head_joint, head_bind_joint, mo=False)
    cmds.scaleConstraint(head_joint, head_bind_joint)
    cmds.parent(head_bind_joint, bind_joints[-1])
    bind_joints.append(head_bind_joint)
    cmds.setAttr('{}.radius'.format(head_bind_joint), 1.5)

    #parent to game
    if cmds.objExists(game_parent):
        cmds.parent(bind_joints[0], game_parent)
    else: 
        cmds.parent(bind_joints[0], 'Bind_Joints_Grp')

    #parent system
    cmds.parentConstraint(block_parent, cmds.listRelatives(neck_blends_grp, p=True), mo=True)

    #clean a bit
    cmds.parent(ribbon['controllers_grp'], fk_chain[0])
    clean_rig_grp = cmds.group(em=True, n = '{}{}'.format(block.replace(nc['module'],'_Rig'), nc['group']))
    cmds.parent(clean_rig_grp, setup['rig_groups']['misc']+ nc['group'])

    cmds.parent(cmds.listRelatives(neck_blends_grp, p=True),setup['base_groups']['control'] + nc['group'])
    cmds.parent(cmds.listRelatives(cmds.listRelatives(ribbon['fol_joints'][0], p=True),p=True),clean_rig_grp)
    cmds.parent(cmds.listRelatives(ribbon['surface'][0], p=True),clean_rig_grp)
    cmds.parent(neck_joint,clean_rig_grp)
    cmds.parent(cmds.listRelatives(ribbon['ctrl_joints'][0], p=True),clean_rig_grp)

    cmds.parent(ribbon['ctrl_fol_grp'],clean_rig_grp)

    #scale
    cmds.scaleConstraint('Rig_Ctrl_Grp', cmds.listRelatives(neck_blends_grp, p=True), mo=True)
    cmds.scaleConstraint('Rig_Ctrl_Grp', cmds.listRelatives(ribbon['ctrl_joints'][0], p=True), mo=True)
    cmds.setAttr('{}.segmentScaleCompensate'.format(head_joint), 0)

    #done
    print ('Build {} Success'.format(block))


#build_head_block()

