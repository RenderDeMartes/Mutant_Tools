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
PYBLOCK_NAME = 'exec_dinamic_scale'

#---------------------------------------------

def create_dinamic_scale_block(name = 'DinamicScale'):

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

    MODULE_FILE = os.path.join(os.path.dirname(__file__), '09_DinamicScale.json')
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

    block = mt.create_block(name = name, icon = 'ExtraScales',  attrs = module['attrs'], build_command = module['build_command'], import_command = module['import'])
    config = block[1]
    block = block[0]
      
    #cmds.getAttr('{}.AttrName'.format(config)) #get attrs from config
    #cmds.getAttr('{}.AttrName'.format(config), asString = True) #for enums
    #joint_one = mt.create_joint_guide(name = name) #guide base with shapes

    cmds.select(block)

    print('{} Created Successfully'.format(name))

#create_dinamicscale_block()

#-------------------------

def build_dinamic_scale_block():

    #By Ricardo Quiros

    topCtrl = 'Global_Ctrl'
    midCtrl = 'Mover_Ctrl'
    botCtrl = 'Mover_Gimbal_Ctrl'
    sRd = 'scale_reader'

    def createSizeAttr(node):
        cmds.addAttr(node, ln='size', dv=1, k=True, min=0.1)
        cmds.setAttr('{}.sx'.format(node), l=False)
        cmds.setAttr('{}.sy'.format(node), l=False)
        cmds.setAttr('{}.sz'.format(node), l=False)
        cmds.connectAttr('{}.size'.format(node), '{}.sx'.format(node), f=True)
        cmds.connectAttr('{}.size'.format(node), '{}.sy'.format(node), f=True)
        cmds.connectAttr('{}.size'.format(node), '{}.sz'.format(node), f=True)
        cmds.setAttr('{}.sx'.format(node), l=True)
        cmds.setAttr('{}.sy'.format(node), l=True)
        cmds.setAttr('{}.sz'.format(node), l=True)

    createSizeAttr('{}'.format(topCtrl))

    if cmds.objExists(sRd) != 1:
        sRd = cmds.createNode('transform', n=sRd, p=botCtrl)
        dM = cmds.createNode('decomposeMatrix', n='{}_dcmpMtx'.format(sRd))
        cmds.addAttr(sRd, ln='size', dv=1, k=True, min=0.1)
        cmds.connectAttr('{}.sy'.format(sRd), '{}.size'.format(sRd), f=True)
        cmds.connectAttr('{}.worldMatrix'.format(botCtrl), '{}.inputMatrix'.format(dM))
        cmds.connectAttr('{}.outputScale'.format(dM), '{}.scale'.format(sRd))
        cmds.connectAttr('{}.outputTranslate'.format(dM), '{}.translate'.format(sRd))
        cmds.connectAttr('{}.outputRotate'.format(dM), '{}.rotate'.format(sRd))
        cmds.setAttr("{}.inheritsTransform".format(sRd), 0)

    conects = cmds.listConnections('{}.scale'.format(topCtrl), t='scaleConstraint')

    if conects:
        for i in conects:
            cmds.connectAttr('{}.parentMatrix[0]'.format(sRd), '{}.target[0].targetParentMatrix'.format(i), f=True)
            cmds.connectAttr('{}.scale'.format(sRd), '{}.target[0].targetScale.'.format(i), f=True)
            if cmds.listConnections('{}.target[1].targetParentMatrix'.format(i)):
                cmds.connectAttr('{}.parentMatrix[0]'.format(sRd), '{}.target[1].targetParentMatrix'.format(i), f=True)
                cmds.connectAttr('{}.scale'.format(sRd), '{}.target[1].targetScale.'.format(i), f=True)

    dconects = cmds.listConnections('{}.scale'.format(topCtrl), p=True)

    if dconects:
        dconects = [s for s in dconects if not s.startswith('{}'.format(topCtrl))]
        for e in dconects:
            cmds.connectAttr('{}.scale'.format(sRd), e, f=True)

    createSizeAttr('{}'.format(botCtrl))
    createSizeAttr('{}'.format(midCtrl))

    ##############################################################################################

    numberOfControls = 5

    gimbalZero = cmds.createNode('transform', n='Mover_Gimbal_Ctrl_grp')
    cmds.parent(gimbalZero, midCtrl)
    cmds.parent(botCtrl, gimbalZero)
    cmds.addAttr(topCtrl, ln='dynamicPivots', dv=0, k=True, min=0, max=1)

    DynGrp = cmds.createNode('transform', n='DynamicParentsGroup')
    cmds.connectAttr('{}.dynamicPivots'.format(topCtrl), '{}.visibility'.format(DynGrp))
    cmds.parent(DynGrp, midCtrl)

    for i in range(numberOfControls):

        zero = cmds.createNode('transform', n='dyn_parentNode_{}_zero'.format(i))
        offset = cmds.createNode('transform', n='dyn_parentNode_{}_offset'.format(i))
        node = cmds.createNode('transform', n='dyn_parentNode_{}_ctrl'.format(i))
        inv = cmds.createNode('multiplyDivide', n='{}_inverse_md'.format(node))
        cmds.parent(node, zero)
        cmds.parent(zero, offset)
        cmds.setAttr('{}.tz'.format(offset), i * -5)
        cmds.setAttr('{}.input2X'.format(inv), -1)
        cmds.setAttr('{}.input2Y'.format(inv), -1)
        cmds.setAttr('{}.input2Z'.format(inv), -1)
        cmds.connectAttr('{}.translate'.format(node), '{}.input1'.format(inv))
        mt.text_curves(name_text=str(i + 1), font='Arial', color='purple')
        shape = cmds.listRelatives('_{}_Ctrl'.format(i + 1), s=True)

        for e in shape:
            cmds.parent(e, node, r=True, s=True)
        cmds.delete('_{}_Ctrl'.format(i + 1))

        if i == 0:
            xForm = cmds.createNode('transform', n='master_2_xform')
            cmds.connectAttr('{}.output'.format(inv), '{}.translate'.format(xForm))
            cmds.parentConstraint(xForm, gimbalZero, mo=True)
            cmds.scaleConstraint(xForm, gimbalZero, mo=True)
            cmds.parent(xForm, node)
        elif i == numberOfControls - 1:
            cmds.connectAttr('{}.output'.format(inv), 'dyn_parentNode_{}_zero.translate'.format(i - 1))
            cmds.parent('dyn_parentNode_{}_offset'.format(i - 1), node)
            cmds.parent(offset, DynGrp)
        else:
            cmds.connectAttr('{}.output'.format(inv), 'dyn_parentNode_{}_zero.translate'.format(i - 1))
            cmds.parent('dyn_parentNode_{}_offset'.format(i - 1), node)

    locSpineList = ['Spine_Root_Parent_Loc','Spine_Base_Parent_Loc','Spine_Belly_Parent_Loc',
                    'Spine_Chest_Parent_Loc', 'Spine_End_Parent_Loc']
    for i in locSpineList:
        if cmds.objExists(i):
            cmds.connectAttr('{}.scale'.format(sRd), '{}.scale'.format(i), f = True)

#build_dinamicscale_block()
