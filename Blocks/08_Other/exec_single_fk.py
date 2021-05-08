from maya import cmds
import json
import imp
import os

import Mosaic_Tools
import Mosaic_Tools.Utils
from Mosaic_Tools.Utils import main_mosaic
imp.reload(Mosaic_Tools.Utils.main_mosaic)

mt = main_mosaic.Mosaic()

#---------------------------------------------

TAB_FOLDER = '08_Other'
PYBLOCK_NAME = 'exec_single_fk'

#Read name conventions as nc[''] and setup as seup['']
PATH = os.path.dirname(__file__)
PATH = PATH.replace('\Blocks//{}'.format(TAB_FOLDER), '//Config') #change this path depending of the folder

JSON_FILE = (PATH + '/name_conventions.json')
with open(JSON_FILE) as json_file:
	nc = json.load(json_file)
#Read curve shapes info
CURVE_FILE = (PATH + '/curves.json')
with open(CURVE_FILE) as curve_file:
	curve_data = json.load(curve_file)
#setup File
SETUP_FILE = (PATH+'/rig_setup.json')
with open(SETUP_FILE) as setup_file:
	setup = json.load(setup_file)	

MODULE_FILE = (os.path.dirname(__file__) +'/02_Single_FK.json')
with open(MODULE_FILE) as module_file:
	module = json.load(module_file)

#---------------------------------------------

def create_single_fk_block(name = 'Bone'):

    #name checks and block creation
    name = mt.ask_name(text = name)
    if cmds.objExists('{}{}'.format(name,nc['module'])):
        cmds.warning('Name already exists.')
        return ''

    single_fk_block = mt.create_block(name = name, icon = 'Bone',  attrs = module['attrs'], build_command = module['build_command'], import_command = module['import'])
    single_fk_config = single_fk_block[1]
    single_fk_block = single_fk_block[0]

    if name == 'COG':
        cmds.setAttr('{}.CtrlType'.format(single_fk_config),16)# if cog do a cog ctrl

    loc_guide = cmds.spaceLocator(n = name + nc['locator'])
    cmds.parent(loc_guide, single_fk_block)

    print('Single_fk Created Successfully')

#create_single_fk_block()

#-------------------------

def build_single_fk_block():

    block = cmds.ls(sl=True)
    config = cmds.listConnections(block)[1]
    loc_guide = cmds.listRelatives(block, c=True)[0]
    print(loc_guide)

    ctrl = mt.curve(input = loc_guide, type = cmds.getAttr('{}.CtrlType'.format(config), asString=True), rename = True, custom_name = False, name = '', 
                                       size = cmds.getAttr('{}.CtrlSize'.format(config)))
    mt.asign_color(input = ctrl, color = cmds.getAttr('{}.CtrlColor'.format(config), asString = True))

    root = mt.root_grp(input = ctrl)

    mt.match(root, loc_guide)
    try:cmds.parent(root, cmds.getAttr('{}.SetCtrlParent'.format(config)))
    except:pass

    #create gimbal ctrl under main
    if cmds.getAttr('{}.Gimbal'.format(config)) == True : 
        gimbal_ctrl = mt.curve(input = loc_guide, type = cmds.getAttr('{}.CtrlType'.format(config), asString=True), rename = False, custom_name = True, 
                                                  name = ctrl.replace(nc['ctrl'], nc['gimbal_ctrl']), 
                                                  size = cmds.getAttr('{}.CtrlSize'.format(config)) * 0.8 )        
        mt.asign_color(input = gimbal_ctrl, color = cmds.getAttr('{}.CtrlColor'.format(config), asString = True))

        cmds.parent(gimbal_ctrl, ctrl)
        
        #gimbal vis attrs
        show_gimbal_attr = mt.new_enum(input= ctrl, name = 'Gimbal', enums = 'Hide:Show')
        cmds.connectAttr(show_gimbal_attr, '{}.v'.format(cmds.listRelatives(gimbal_ctrl, shapes= True)[0]))

    #create joint and joint steps if True
    if cmds.getAttr('{}.CreateJoint'.format(config)) == True : 
        cmds.select(cl=True)
        jnt = cmds.joint(n = str(loc_guide).replace(nc['locator'], nc['joint']))
        cmds.delete(cmds.parentConstraint(loc_guide,jnt , mo=False ))
        
        #cmds.delete(loc_guide)

        try:cmds.parent(jnt, cmds.getAttr('{}.SetJointParent'.format(config)))
        except:pass

        #parent to ctlr or tr gimbal
        if cmds.objExists(gimbal_ctrl):
            cmds.parentConstraint(gimbal_ctrl, jnt)
        else:
            cmds.parentConstraint(ctrl, jnt)


    #clean if COG
    if 'COG' in str(ctrl):
        mt.hide_attr(input = ctrl, s=True)
        mt.hide_attr(input = gimbal_ctrl, s=True)

    print ('Build of single_fk was succesfull')



#build_single_fk_block()
