from __future__ import absolute_import
from maya import cmds


def turn_on_render_curves():
    
    ctrl_shapes = cmds.ls(sl=True)
    
    # Iterate over each shape node and turn on render curves
    for ctrl in ctrl_shapes:
        try:
            ctrl_shape = cmds.listRelatives(ctrl, s=True)[0]
            print(ctrl_shape)
            # Check if the shape node has the aiRenderCurve attribute
            cmds.setAttr(ctrl_shape + ".aiRenderCurve", 1)
            cmds.setAttr(ctrl_shape + ".aiCurveWidth", 0.4)
            cmds.setAttr(ctrl_shape+ ".aiCurveShader", 1, 1, 1, type="double3")
            cmds.setAttr(ctrl_shape+ ".aiMatte", 0)

        except Exception as e:
            print(e, ctrl)
            pass

# Call the function to turn on render curves for all *_Ctrls objects
turn_on_render_curves()


import maya.cmds as cmds

def create_materials(color_dict):
    material_dict = {}
    for color_name, color_values in color_dict.items():
        material_name = color_name + "_material"
        if not cmds.objExists(material_name):
            material = cmds.shadingNode('lambert', asShader=True, name=material_name)
            cmds.setAttr(material + ".color", *color_values)
            material_dict[color_name] = material
        else:
            material_dict[color_name] = material_name
    return material_dict

def connect_material_to_shape(shape_node, material):
    shape=cmds.listRelatives(s=True)[0]
    cmds.connectAttr(material+'_material.outColor', shape+'.aiCurveShader', f=True)


color_dict = {
    "red": (1, 0, 0),
    "blue": (0, 0, 1),
    "light_blue": (0, 1, 1),
    "yellow": (1, 1, 0),
    "green": (0, 1, 0),
    "purple": (0.5, 0, 0.5),
    "pink": (1, 0.5, 0.5),
    "orange": (1, 0.5, 0),
    "white": (1, 1, 1),
    "cyan": (0, 1, 1),
    "magenta": (1, 0, 1),
    "lime": (0, 1, 0),
    "gray": (0.5, 0.5, 0.5),
    "brown": (0.6, 0.3, 0.1)
}


# Create Lambert materials
material_dict = create_materials(color_dict)

# Example usage:
ctrls = cmds.ls(sl=True)
for ctrl in ctrls:
    print(ctrl)
    cmds.select(ctrl)
    connect_material_to_shape(ctrl, "light_blue")

