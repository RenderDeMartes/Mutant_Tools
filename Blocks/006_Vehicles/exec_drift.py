from __future__ import absolute_import, division
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

TAB_FOLDER = '006_Vehicles'
PYBLOCK_NAME = 'exec_drift'

#---------------------------------------------

def create_drift_block(name = 'Drift'):

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

    MODULE_FILE = os.path.join(os.path.dirname(__file__), '08_Drift.json')
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

    block = mt.create_block(name = name, icon = 'Drift',  attrs = module['attrs'], build_command = module['build_command'], import_command = module['import'])
    config = block[1]
    block = block[0]
      
    #cmds.getAttr('{}.AttrName'.format(config)) #get attrs from config
    #cmds.getAttr('{}.AttrName'.format(config), asString = True) #for enums
    #joint_one = mt.create_joint_guide(name = name) #guide base with shapes

    cmds.select(block)

    print('{} Created Successfully'.format(name))

#create_drift_block()

#-------------------------

def build_drift_block():

    nc, curve_data, setup = mt.import_configs()

    mt.check_is_there_is_base()

    block = cmds.ls(sl=True)
    config = cmds.listConnections(block)[1]
    block = block[0]
    name = block.replace(nc['module'],'')


    #cmds.getAttr('{}.AttrName'.format(config))
    #cmds.getAttr('{}.AttrName'.format(config), asString = True)

    #orient the joints

    #use this locator in case parent is set to new locator
    if cmds.getAttr('{}.SetParent'.format(config)) == 'new_locator':
        block_parent = cmds.spaceLocator( n = '{}'.format(str(block).replace(nc['module'],'_Parent' + nc['locator'])))
    else:
        block_parent = cmds.getAttr('{}.SetParent'.format(config))

    #Get data
    front_drift = cmds.getAttr('{}.SetFrontDrift'.format(config))
    back_drift = cmds.getAttr('{}.SetBackDrift'.format(config))

    size = cmds.getAttr('{}.tz'.format(front_drift))/2


    #Create 2 Controllers
    ctrls = []
    dyn_pivs = []
    for drift in [front_drift, back_drift]:
        ctrl = mt.curve(input=drift,
                        type='curveArrow',
                        rename=True,
                        custom_name=True,
                        name=drift.replace(nc['joint'], nc['ctrl']),
                        size=size if 'Back' in drift else size*-1)
        ctrls.append(ctrl)
        mt.assign_color(color='purple')
        root, auto = mt.root_grp(autoRoot=True)
        mt.match(root, drift, r=True, t=True)
        #cmds.parentConstraint(ctrl, drift)
        mt.hide_attr(ctrl, t= True, r = False, s = True)

        dyn = mt.dinamic_pivot(ctrl, size=size/2)
        mt.hide_attr(input=dyn, s=True)
        dyn_pivs.append(dyn)

        mt.line_attr(ctrl, name='VisToggle')
        dyn_vis_attr = mt.new_enum(input=ctrl, name='DynamicPivot', enums='Hide:Show', keyable=False)
        cmds.connectAttr(dyn_vis_attr, cmds.listRelatives(dyn, p=True)[0]+'.v')

        cmds.parent(cmds.listRelatives(dyn, p=True)[0], auto)

        cmds.parent(root, 'Rig_Ctrl_Grp')

        #make the block parent move the ctrls

        pos_data = cmds.xform(block_parent, ws=True, t=True, q=True)
        cmds.move(pos_data[0], pos_data[1], pos_data[2], '{}.rotatePivot'.format(auto))
        cmds.move(pos_data[0], pos_data[1], pos_data[2], '{}.rotatePivot'.format(root))

        cmds.connectAttr('{}.translate'.format(block_parent), '{}.translate'.format(auto))
        cmds.connectAttr('{}.rotate'.format(block_parent), '{}.rotate'.format(auto))

    #Parent to Chasis
    #2 groups over the main chasis
    # change 2 groups pivots to where the new ctrls are
    # direct connect new ctrl to new grps

    back_grp = mt.root_grp(input=block_parent, custom=True, custom_name='_BackDrift')[0]
    front_grp = mt.root_grp(input=block_parent, custom=True, custom_name='_FrontDrift')[0]

    #move Pivots
    decompose_front = cmds.createNode('decomposeMatrix', n=name+'_DecomposeFront')
    cmds.connectAttr('{}.worldMatrix[0]'.format(dyn_pivs[0]), '{}.inputMatrix'.format(decompose_front))
    cmds.connectAttr('{}.outputTranslate'.format(decompose_front), '{}.rotatePivot'.format(front_grp))

    decompose_back = cmds.createNode('decomposeMatrix', n=name+'_DecomposeBack')
    cmds.connectAttr('{}.worldMatrix[0]'.format(dyn_pivs[1]), '{}.inputMatrix'.format(decompose_back))
    cmds.connectAttr('{}.outputTranslate'.format(decompose_back), '{}.rotatePivot'.format(back_grp))


    #Connect
    cmds.connectAttr(ctrls[1]+".rotate", back_grp+".rotate")
    cmds.connectAttr(ctrls[0]+".rotate", front_grp+".rotate")

    #clean a bit
    clean_rig_grp = cmds.group(em=True, name = name + '_Rig' + nc['group'])

    cmds.parent(clean_rig_grp, '{}{}'.format(setup['rig_groups']['misc'], nc['group']))

    print ('Build {} Success'.format(block))



#build_drift_block()
