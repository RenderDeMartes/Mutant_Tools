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

    if name == 'COG':
        cmds.setAttr('{}.CtrlType'.format(single_fk_config),16)# if cog do a cog ctrl

    loc_guide = cmds.spaceLocator(n = name + nc['locator'])
    cmds.parent(loc_guide, single_fk_block)

    print('Single_fk Created Successfully')

#create_single_fk_block()

#-------------------------

def build_single_fk_block():

    mt.check_is_there_is_base()

    nc, curve_data, setup = mt.import_configs()

    block = cmds.ls(sl=True)
    config = cmds.listConnections(block)[1]
    loc_guide = cmds.listRelatives(block, c=True)[0]
    print(loc_guide)

    ctrl = mt.curve(input = loc_guide, type = cmds.getAttr('{}.CtrlType'.format(config), asString=True), rename = True,
                                       custom_name = True, name = loc_guide.replace(nc['locator'], nc['ctrl']),
                                       size = cmds.getAttr('{}.CtrlSize'.format(config)))
    mt.assign_color(input = ctrl, color = cmds.getAttr('{}.CtrlColor'.format(config), asString = True))

    root = mt.root_grp(input = ctrl)

    mt.match(root, loc_guide)
    try:cmds.parent(root, cmds.getAttr('{}.SetCtrlParent'.format(config)))
    except:pass

    #create gimbal ctrl under main
    gimbal_ctrl=''
    if cmds.getAttr('{}.Gimbal'.format(config)) == True :
        gimbal_ctrl = mt.curve(input = loc_guide, type = cmds.getAttr('{}.CtrlType'.format(config), asString=True), rename = False, custom_name = True,
                                                  name = ctrl.replace(nc['ctrl'], nc['gimbal_ctrl']),
                                                  size = cmds.getAttr('{}.CtrlSize'.format(config)) * 0.8 )
        mt.assign_color(input = gimbal_ctrl, color = cmds.getAttr('{}.CtrlColor'.format(config), asString = True))

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
            cmds.scaleConstraint(gimbal_ctrl, jnt)

        else:
            cmds.parentConstraint(ctrl, jnt)
            cmds.scaleConstraint(ctrl, jnt)



        #Create bind joint
        cmds.select(cl=True)
        bind_joint = cmds.joint(n = str(loc_guide).replace(nc['locator'], nc['joint_bind']))
        cmds.parentConstraint(jnt, bind_joint)
        cmds.scaleConstraint(jnt, bind_joint)

        cmds.parent(bind_joint, 'Bind_Joints_Grp')

    #clean if COG
    if 'COG' in str(ctrl):
        #mt.hide_attr(input = ctrl, s=True)
        if gimbal_ctrl:
            mt.hide_attr(input = gimbal_ctrl, s=True)
    else:
        mt.hide_attr(input=ctrl, s=True)
    print ('Build of single_fk was succesfull')




#build_single_fk_block()
