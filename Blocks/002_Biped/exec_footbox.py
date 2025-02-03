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
PYBLOCK_NAME = 'exec_footbox'

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

MODULE_FILE = os.path.join(os.path.dirname(__file__),'010_FootBox.json')
with open(MODULE_FILE) as module_file:
	module = json.load(module_file)

#---------------------------------------------

def create_footbox_block(name = 'L_FootBox'):

    nc, curve_data, setup = mt.import_configs()
    #name checks and block creation
    name = mt.ask_name(text = module['Name'])
    if cmds.objExists('{}{}'.format(name,nc['module'])):
        cmds.warning('Name already exists.')
        return ''

    block = mt.create_block(name = name, icon = 'FootBox',  attrs = module['attrs'], build_command = module['build_command'], import_command = module['import'])
    config = block[1]
    block = block[0]
    name = block.replace(nc['module'],'')

    #cmds.getAttr('{}.AttrName'.format(config)) #get attrs from config
    #cmds.getAttr('{}.AttrName'.format(config), asString = True) #for enums
    #joint_one = mt.create_joint_guide(name = name) #guide base with shapes

    cmds.select(block)

    print('{} Created Successfully'.format(name))

#create_footbox_block()

#-------------------------

def build_footbox_block(toes=False, ball=False, heel=False, inner=False, outter=False, color=False,
                        attrs_pos=False, force_y_zero=False, ball_parent=False, heel_parent=False,
                        mirror=False, block_build=True, name=False):

    #Need to use this function outside of Mutant UI Build.
    if block_build:
        mt.check_is_there_is_base()

        block = cmds.ls(sl=True)
        config = cmds.listConnections(block)[1]
        block = block[0]
        name = block.replace(nc['module'], '')


    #build ------------------------------------------------------


    #clean a bit
    clean_ctrl_grp = cmds.group(em=True, name = name + nc['ctrl'] + nc['group'])
    #clean_rig_grp = cmds.group(em=True, name = name + '_Rig' + nc['group'])

    #cmds.parent(clean_rig_grp, '{}{}'.format(setup['rig_groups']['misc'], nc['group']))
    cmds.parent(clean_ctrl_grp, setup['base_groups']['control'] + nc['group'])
    if not mirror:
        mirror = cmds.getAttr('{}.Mirror'.format(config))

    if not toes:
        toes = cmds.getAttr('{}.SetToes'.format(config), asString=True)
    if not ball:
        ball = cmds.getAttr('{}.SetBallFloor'.format(config), asString=True)
    if not heel:
        heel = cmds.getAttr('{}.SetHeel'.format(config), asString=True)
    if not inner:
        inner = cmds.getAttr('{}.SetIn'.format(config), asString=True)
    if not outter:
        outter = cmds.getAttr('{}.SetOut'.format(config), asString=True)
    if not color:
        color = cmds.getAttr('{}.Color'.format(config), asString=True)
    if not attrs_pos:
        attrs_pos = cmds.getAttr('{}.SetAttrsPosition'.format(config), asString=True)
    if not force_y_zero:
        force_y_zero = cmds.getAttr('{}.ForceYZero'.format(config))
    if not ball_parent:
        ball_parent = cmds.getAttr('{}.SetBallParent'.format(config), asString=True)
    if not heel_parent:
        heel_parent = cmds.getAttr('{}.SetHeelParent'.format(config), asString=True)

    if ball_parent == 'new_locator':
        ball_parent = cmds.spaceLocator(n='{}'.format(str(block).replace(nc['module'], '_BallAttrs' + nc['locator'])))[0]
    if heel_parent == 'new_locator':
        heel_parent = cmds.spaceLocator(n='{}'.format(str(block).replace(nc['module'], '_HeelAttrs' + nc['locator'])))[0]

    front_transform = toes
    back_transform = ball
    inner_transform = inner
    outer_transform = outter

    offset_y = 0
    offset_x = 0

    l_fingers_cube, r_fingers_cube = create_poly_cube_with_faces(name+'Ball', front_transform, back_transform, inner_transform, outer_transform,
                                               offset_y=offset_y, parent=ball_parent, offset_x = offset_x,  mirror=mirror, force_y_zero=force_y_zero)

    front_transform = heel
    back_transform = ball
    inner_transform = inner
    outer_transform = outter

    offset_y = 180
    offset_x = 0
    l_ankle_cube, r_ankle_cube = create_poly_cube_with_faces(name+'Ankle', front_transform, back_transform, inner_transform, outer_transform,
                                             offset_y=offset_y, offset_x=offset_x, parent=heel_parent, mirror=mirror, force_y_zero=force_y_zero)

    cmds.parent(l_ankle_cube, cmds.listRelatives(r_ankle_cube, p=True)[0],clean_ctrl_grp)
    cmds.parent(l_fingers_cube, cmds.listRelatives(r_fingers_cube, p=True)[0],clean_ctrl_grp)

    #add material
    l_material= create_lambert_material(color, name=name)
    for i in [l_ankle_cube, l_fingers_cube]:
        assign_material_to_object(l_material, objects=i)

    #create attrs
    mt.line_attr(attrs_pos, name='FootBox')
    vis_attr = mt.new_enum(input=attrs_pos, name='Vis', enums='Hide:Show', keyable=False, default=1)
    transparency_attr = mt.new_attr(input=attrs_pos, name='Transparency', min=0, max=1, default=0.75)

    cmds.connectAttr(vis_attr, '{}.v'.format(l_fingers_cube))
    cmds.connectAttr(vis_attr, '{}.v'.format(l_ankle_cube))

    cmds.connectAttr(transparency_attr, '{}.transparencyR'.format(l_material))
    cmds.connectAttr(transparency_attr, '{}.transparencyG'.format(l_material))
    cmds.connectAttr(transparency_attr, '{}.transparencyB'.format(l_material))

    if mirror:
        r_material= create_lambert_material(color, name=name.replace(nc['left'], nc['right']))
        for i in [r_ankle_cube, r_fingers_cube]:
            assign_material_to_object(r_material, objects=i)

        attrs_pos = attrs_pos.replace(nc['left'], nc['right'])

        mt.line_attr(attrs_pos, name='FootBox')
        vis_attr = mt.new_enum(input=attrs_pos, name='Vis', enums='Hide:Show', keyable=False, default=1)
        transparency_attr = mt.new_attr(input=attrs_pos, name='Transparency', min=0, max=1, default=0.75)

        cmds.connectAttr(vis_attr, '{}.v'.format(r_fingers_cube))
        cmds.connectAttr(vis_attr, '{}.v'.format(r_ankle_cube))

        cmds.connectAttr(transparency_attr, '{}.transparencyR'.format(r_material))
        cmds.connectAttr(transparency_attr, '{}.transparencyG'.format(r_material))
        cmds.connectAttr(transparency_attr, '{}.transparencyB'.format(r_material))


    # build complete ----------------------------------------------------
    if block_build:
        print ('Build {} Success'.format(block))


#build_footbox_block()

def create_lambert_material(color='light_blue', name='Name'):
    # Dictionary mapping color names to RGB values
    colors = {
        'pink': (1, 0.5, 0.5),
        'orange': (1, 0.5, 0),
        'blue': (0, 0, 1),
        'light_blue': (0.5, 0.5, 1),
        'red': (1, 0, 0),
        'green': (0, 1, 0),
        'purple': (0.5, 0, 1),
        'yellow': (1, 1, 0),
        'cyan': (0, 1, 1),
        'gray': (0.5, 0.5, 0.5),
        'brown': (0.4, 0.2, 0)
    }

    # Create a Blinn material
    material_name = cmds.shadingNode('lambert', asShader=True, name=name)

    # Set the color of the material based on the input
    if color in colors:
        cmds.setAttr(material_name + '.color', *colors[color], type='double3')
    else:
        cmds.warning("Invalid color input. Defaulting to light blue.")
        cmds.setAttr(material_name + '.color', *colors['light_blue'], type='double3')

    cmds.setAttr(material_name + '.transparency', 0.75, 0.75, 0.75, type='double3')

    return material_name


def assign_material_to_object(material_name, objects):
    # Assign the material to the currently selected objects
    cmds.select(objects)
    if objects:
        shading_group_name = cmds.sets(renderable=True, noSurfaceShader=True, empty=True)
        print('Shading group name' + shading_group_name)
        cmds.connectAttr(material_name + '.outColor', shading_group_name + '.surfaceShader', force=True)
        cmds.sets(objects, edit=True, forceElement=shading_group_name)

def create_poly_cube_with_faces(name, front, back, inner, outer, offset_y, offset_x, parent, mirror, force_y_zero):
    # Create a poly cube

    # Get the positions of the transform objects
    front_pos = cmds.xform(front, q=True, ws=True, m=True)
    back_pos = cmds.xform(back, q=True, ws=True, m=True)
    inner_pos = cmds.xform(inner, q=True, ws=True, m=True)
    outer_pos = cmds.xform(outer, q=True, ws=True, m=True)

    w = mt.get_distance_between(inner, outer)
    d = mt.get_distance_between(front, back)

    print(w, d)

    cube = cmds.polyCube(w=1, h=1, d=1, name=name+'_FootBox')[0]
    cmds.move(0, -0.5, 0.5, cube + ".scalePivot", cube + ".rotatePivot", absolute=True)
    cmds.move(0, 0.5, 0, cube, r=True)
    cmds.makeIdentity(cube, a=True, t=True, r=True, s=True)

    # cmds.scale(w, 1, d, r=True)
    print(cube, w, d)
    cmds.setAttr(cube + '.scaleX', w)
    cmds.setAttr(cube + '.scaleY', d)
    cmds.setAttr(cube + '.scaleZ', w * 0.25)

    mt.match(cube, back, t=True, r=True, s=False)
    cmds.rotate(0, offset_y, offset_x, cube, r=True)

    cmds.setAttr(cube+'.overrideEnabled', 1)
    cmds.setAttr(cube+'.overrideDisplayType', 2)

    if force_y_zero:
        cmds.setAttr(cube+'.translateY', 0)

    if mirror:
        other_cube = cmds.duplicate(cube, n=name.replace(nc['left'], nc['right'], 1)+'_FootBox')[0]
        grp = mt.mirror_group(input=other_cube, world=True)

        cmds.parentConstraint(parent, cube, mo=True)
        cmds.scaleConstraint(parent, cube, mo=True)

        cmds.parentConstraint(parent.replace(nc['left'], nc['right'], 1), other_cube, mo=True)
        cmds.scaleConstraint(parent.replace(nc['left'], nc['right'], 1), other_cube, mo=True)
        return cube, other_cube

    else:
        cmds.parentConstraint(parent, cube, mo=True)
        cmds.scaleConstraint(parent, cube, mo=True)
        return cube, cube

# Example usage

"""
front_transform = "L_Foot_Toes_RFL_Grp"
back_transform = "L_Foot_BallFloor_RFL_Grp"
inner_transform = "L_Foot_In_RFL_Grp"
outer_transform = "L_Foot_Out_RFL_Grp"

fingers_cube = create_poly_cube_with_faces(front_transform, back_transform, inner_transform, outer_transform,
                                           offset_y=0, parent='L_Foot_Toes_RFL_Grp')

front_transform = "L_Foot_Heel_RFL_Grp"
back_transform = "L_Foot_BallFloor_RFL_Grp"
inner_transform = "L_Foot_In_RFL_Grp"
outer_transform = "L_Foot_Out_RFL_Grp"

ankle_cube = create_poly_cube_with_faces(front_transform, back_transform, inner_transform, outer_transform,
                                         offset_y=180, parent='L_Foot_Ball_RFL_Grp')

material = create_lambert_material('pink')
assign_material_to_object(material)

parents:
L_Foot_Toes_Ctrl
L_Foot_Ankle_Bnd

attrs:
L_Hip_Jnt_Switch_Loc

"""