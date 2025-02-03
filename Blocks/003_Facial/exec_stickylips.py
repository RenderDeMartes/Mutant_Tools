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

TAB_FOLDER = '002_Biped'
PYBLOCK_NAME = 'exec_stickylips'

#---------------------------------------------

def create_stickylips_block(name = 'StickyLips'):

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

    MODULE_FILE = os.path.join(os.path.dirname(__file__), '016_StickyLips.json')
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

    block = mt.create_block(name = name, icon = 'Sticky',  attrs = module['attrs'], build_command = module['build_command'], import_command = module['import'])
    config = block[1]
    block = block[0]
      
    #cmds.getAttr('{}.AttrName'.format(config)) #get attrs from config
    #cmds.getAttr('{}.AttrName'.format(config), asString = True) #for enums
    #joint_one = mt.create_joint_guide(name = name) #guide base with shapes

    cmds.select(block)

    print('{} Created Successfully'.format(name))

#create_stickylips_block()

#-------------------------

def build_stickylips_block():

    nc, curve_data, setup = mt.import_configs()

    mt.check_is_there_is_base()

    block = cmds.ls(sl=True)
    config = cmds.listConnections(block)[1]
    block = block[0]
    name = block.replace(nc['module'],'')

    #cmds.getAttr('{}.AttrName'.format(config))
    #cmds.getAttr('{}.AttrName'.format(config), asString = True)

    jaw_bone = cmds.getAttr('{}.SetJawBone'.format(config))
    notjaw_bone = cmds.getAttr('{}.SetNotJawBone'.format(config))
    left_ctrl = cmds.getAttr('{}.SetLeftMouthCtrl'.format(config))
    right_ctrl = left_ctrl.replace(nc['left'], nc['right'])
    mouth_edge = cmds.getAttr('{}.SetMouthEdge'.format(config)).split(',')
    face_geo = cmds.getAttr('{}.SetFaceGeo'.format(config)).split(',')

    #Build
    cmds.select(mouth_edge)
    # mel.eval('performPolyToCurveSetup OptionBoxWindow|formLayout108|tabLayout5|formLayout110|polyToCurveOptionsFormLayout 1;')
    linear_curve = cmds.polyToCurve(form=0,
                                    degree=1,
                                    # conformToSmoothMeshPreview=1,
                                    n=name + '_Edge' + nc['curve'],
                                    ch=False)

    skin = cmds.skinCluster(linear_curve, [jaw_bone, notjaw_bone], tsb=True)

    wire = cmds.wire(face_geo, n="{}_Wire".format(name), w=linear_curve)
    print(wire)
    base_skin=cmds.skinCluster(linear_curve[0]+'BaseWire', [jaw_bone, notjaw_bone], tsb=True)
    cmds.copySkinWeights(face_geo, linear_curve[0]+'BaseWire', nm=True, sa='closestPoint', ia='oneToOne')

    mt.line_attr(left_ctrl, name='StickyLips')
    mt.line_attr(right_ctrl, name='StickyLips')

    l_sticky_attr = mt.new_attr(input=left_ctrl, name='Sticky', default=0, min=0, max=99999)
    r_sticky_attr = mt.new_attr(input=right_ctrl, name='Sticky', default=0,  min=0, max=99999)

    blend_falloff = cmds.createNode("blendFalloff", n=name + '_blendFalloff')
    left_primitive_falloff = cmds.createNode("primitiveFalloff", n='L_'+ name + '_primitiveFalloff')
    cmds.setAttr('{}.primitive'.format(left_primitive_falloff), 1)
    right_primitive_falloff = cmds.createNode("primitiveFalloff", n='R_'+ name + '_primitiveFalloff')
    cmds.setAttr('{}.primitive'.format(right_primitive_falloff), 1)

    cmds.connectAttr('{}.outputWeightFunction'.format(left_primitive_falloff),
                     '{}.target[0].weightFunction'.format(blend_falloff))
    cmds.connectAttr('{}.outputWeightFunction'.format(right_primitive_falloff),
                     '{}.target[1].weightFunction'.format(blend_falloff))

    mt.match(left_primitive_falloff, left_ctrl, r=False, t=True)
    mt.match(right_primitive_falloff, right_ctrl, r=False, t=True)

    cmds.setAttr('{}.rotateY'.format(left_primitive_falloff), 180)
    cmds.setAttr('{}.target[1].mode'.format(blend_falloff), 3)

    left_primitive_root, left_primitive_auto = mt.root_grp(left_primitive_falloff, autoRoot=True)
    right_primitive_root, right_primitive_auto = mt.root_grp(right_primitive_falloff, autoRoot=True)

    cmds.connectAttr('{}.outputWeightFunction'.format(blend_falloff),
                     '{}.weightFunction[0]'.format(wire[0]))

    cmds.connectAttr(l_sticky_attr, left_primitive_auto+'.tx')
    cmds.connectAttr(r_sticky_attr, right_primitive_auto+'.tx')

    #clean a bit
    clean_rig_grp = cmds.group(em=True, name = name + '_Rig' + nc['group'])

    cmds.parent(left_primitive_root, right_primitive_root, linear_curve, linear_curve[0]+'BaseWire', clean_rig_grp)

    cmds.parent(clean_rig_grp, '{}{}'.format(setup['rig_groups']['misc'], nc['group']))

    print ('Build {} Success'.format(block))



#build_stickylips_block()


"""
Wire method min 12

create curve with og shape of mouth
linear curve
skin curve to jaw skin, curve needs to stays in the middle
use a corner vts of jaw to make curve stay 100% in the middle
wire from new curve to jaw face

skin the new base wire and match it to the main wire curve

if you move jaw no it will stay close

min17:25

crete 2 primite falloff
create 2 blendfollofs

createNode "blendFalloff"
createNode "primitiveFalloff"
setAttr "primitiveFalloff1.primitive" 1;

connectAttr -f primitiveFalloff1.outputWeightFunction blendFalloff1.target[0].weightFunction;


blend fall off output to wire weight funtion [0]

create custom attrs in jaw for right and left
conect tx of falloff to a custom attr in jaw

"""
