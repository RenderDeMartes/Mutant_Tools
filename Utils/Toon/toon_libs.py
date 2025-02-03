from __future__ import absolute_import, division
"""

Libs to crete toon lines and expression lines

from rigging.Mutant_Tools.Utils.Toon import toon_libs
import imp
imp.reload(toon_libs)


cmds.select('curve1')
toon_libs.convert_curve_to_pe(curve='curve1')
toon_libs.create_curve_rig(curve='curve1')
toon_libs.connect_pe_to_ribbon(stroke='curve1_Stroke')

toon_node, toon_shape = toon_libs.create_toon_outline('tRex')
toon_libs.convert_outline_to_curves(toon_shape)

exmpale use:
from Mutant_Tools.Utils.Toon import toon_libs
import imp
imp.reload(toon_libs)


curves = cmds.listRelatives('curvesFace1', c=True)

for curve in curves:
    stroke = toon_libs.convert_curve_to_pe(curve=curve)
    toon_libs.connect_stroke_to_render(stroke=stroke, curve=curve)
    toon_libs.create_curve_rig(curve=curve, size = 0.5)
    toon_libs.connect_pe_to_ribbon(stroke=stroke)

face_geo = 'C_Head_hi'

toon_node, toon_shape = toon_libs.create_toon_outline(face_geo)
#toon_libs.convert_outline_to_curves(toon_shape)
toon_libs.convert_outline_to_geo(toon_shape)


"""

#Notes
'''
require preset for paint effects
require preset for ramp

controllers aim axis are not good
limitation in big shapes as in forehead
limit in circular shapes
limit in start and end attrs( need to find a diferent way)
pipeline, modelling or rigging should implement this


'''

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
nc, curve_data, setup = mt.import_configs()

# -----------------------------------------------------------------------------------------------------

def create_curve_rig(curve, tweeks=5, direction='V', size=1, color='lightBlue'):

    size=size/3

    joints_grp = cmds.group(em=True, n = curve + nc['joint']+ nc['group'])
    main_ctrls_grp = cmds.group(em=True, n = curve + nc['ctrl'] + '_Main' + nc['group'])
    tweeks_ctrls_grp = cmds.group(em=True, n = curve + nc['ctrl'] + '_Tweeks' + nc['group'])
    ctrls_grp = cmds.group(em=True, n = curve + nc['ctrl'] + nc['group'])
    cmds.parent(tweeks_ctrls_grp, ctrls_grp)
    cmds.parent(main_ctrls_grp, ctrls_grp)
    misc_group = cmds.group(em=True, n = curve + '_Misc' + nc['group'])

    #duplciate curve to convert to nurbs to add folls
    ribbon_surface = cmds.bevel(curve, ch=False, w=0, d=0.01, ed=0, ct=2, bst=1, n=curve+nc['nurb'], js=True)[0]
    ribbon_surface = cmds.rebuildSurface(ribbon_surface, ch=False, dv=3, du=3, su=0, sv=tweeks-1)[0]

    cmds.parent(ribbon_surface, misc_group)
    #cmds.parent(curve, misc_group)

    # Create follicles
    cmds.select(ribbon_surface)
    if direction == 'U':
        mel.eval("createHair {} 1 10 0 0 0 0 5 0 1 2 1;".format(tweeks))
    else:
        mel.eval("createHair 1 {} 10 0 0 0 0 5 0 1 2 1;".format(tweeks))

    cmds.delete('hairSystem1', 'pfxHair1', 'nucleus1')
    cmds.setAttr(ribbon_surface + '.inheritsTransform', 0)

    fol_grp = cmds.rename('hairSystem1Follicles', curve + nc['follicle'] + nc['group'])
    cmds.parent(fol_grp, misc_group)
    follicles = []
    for num, fol in enumerate(cmds.listRelatives(fol_grp, c=True)):
        gc = cmds.listRelatives(fol, c=True)
        cmds.delete(gc[-1])
        fol = cmds.rename(fol,  curve+nc['follicle']+'_'+str(num))
        follicles.append(fol)

    #add joints to follicles
    fol_joints =[]
    tweek_ctrls = []

    for num, fol in enumerate(follicles):
        cmds.select(cl=True)
        fol_joint = cmds.joint(n='{}{}_{}{}'.format(curve,nc['follicle'] ,num, nc['joint']))
        fol_joints.append(fol_joint)
        cmds.delete(cmds.parentConstraint(fol, fol_joint))
        cmds.parent(fol_joint, fol)
        if direction == 'U':
            cmds.setAttr('{}.parameterV'.format(fol), 0)
        else:
            cmds.setAttr('{}.parameterU'.format(fol), 0)


        #ctrls
        ctrl = mt.curve(  input=fol_joint,
                          type='sphere',
                          rename=True,
                          custom_name=True,
                          name=fol_joint.replace(nc['joint'], '_Tweek'+nc['ctrl']),
                          size=size)

        mt.assign_color(color=color)
        root_grp = mt.root_grp()[0]
        mt.match(root_grp, fol_joint, r=True, t=True)

        #put in borders first and last
        if num == 0:
            cmds.setAttr('{}.parameter{}'.format(fol, direction), 0)
        if num == tweeks-1:
            cmds.setAttr('{}.parameter{}'.format(fol, direction), 1)

        #constraint
        cmds.parentConstraint(ctrl, fol_joint)
        cmds.scaleConstraint(ctrl, fol_joint)
        tweek_ctrls.append(ctrl)

        cmds.parentConstraint(fol, root_grp, mo=True)

        cmds.parent(root_grp, tweeks_ctrls_grp)


    #skin tweeks joints to curve
    cmds.skinCluster(fol_joints, curve, tsb=True)

    #Main ctrls
    ctrl_joints = []
    main_ctrls =[]

    for num, fol in enumerate([follicles[0], follicles[len(follicles)//2], follicles[-1]]):
        cmds.select(cl=True)
        ctrl_joint = cmds.joint(n='{}{}_{}{}'.format(curve,nc['follicle'] ,num, nc['joint_ctrl']))
        mt.match(ctrl_joint, fol)
        ctrl_joints.append(ctrl_joint)

        # ctrls
        ctrl = mt.curve(input=ctrl_joint,
                        type='cube',
                        rename=True,
                        custom_name=True,
                        name=ctrl_joint.replace(nc['joint_ctrl'], nc['ctrl']),
                        size=size*1.5)

        mt.assign_color(color=color)
        root_grp = mt.root_grp()[0]
        mt.match(root_grp, ctrl_joint, r=True, t=True)
        mt.hide_attr(ctrl, s=True)
        cmds.parentConstraint(ctrl, ctrl_joint)
        cmds.scaleConstraint(ctrl, ctrl_joint)
        main_ctrls.append(ctrl)

        cmds.parent(root_grp, main_ctrls_grp)
        cmds.parent(ctrl_joint, joints_grp)

    cmds.skinCluster(ctrl_joints, ribbon_surface, tsb=True)

    #Create center and main controller

    center_ctrl = mt.curve(input=ctrl_joint,
                         type='square',
                         rename=True,
                         custom_name=True,
                         name=curve + '_Center' + nc['ctrl'],
                         size=size * 2.5)

    mt.assign_color(color=color)
    center_root_grp = mt.root_grp()[0]
    mt.match(center_root_grp, main_ctrls[1], r=True, t=True)
    cmds.parent(center_root_grp, ctrls_grp)

    #make center ctrl aim to center
    cmds.parentConstraint(center_ctrl, cmds.listRelatives(main_ctrls[1], p=True)[0], mo=True)
    #cmds.aimConstraint(center_ctrl, cmds.listRelatives(main_ctrls[0], p=True)[0], aimVector=(0, 1, 0), upVector=(-1, 0, 0), mo=True)
    #cmds.aimConstraint(center_ctrl, cmds.listRelatives(main_ctrls[-1], p=True)[0], aimVector=(0, -1, 0), upVector=(-1, 0, 0), mo=True)

    #Crate mover controllers
    main_ctrl = mt.curve(input=ctrl_joint,
                            type='mover',
                            rename=True,
                            custom_name=True,
                            name=curve + '_Main'+nc['ctrl'],
                            size=size*2)

    mt.assign_color(color=color)
    offset_grp = mt.root_grp()[0]
    root, auto = mt.root_grp(main_ctrl, autoRoot=True)
    mt.match(offset_grp, main_ctrls[1], r=True, t=True)
    cmds.parent(offset_grp, ctrls_grp)
    cmds.parent(main_ctrls_grp, main_ctrl)
    cmds.parent(tweeks_ctrls_grp, main_ctrl)
    cmds.parent(center_root_grp, main_ctrl)

    return {}

#create_curve_rig(curve='curve1')

# -----------------------------------------------------------------------------------------------------

def convert_curve_to_pe(curve='', make_pretty=True, resolution = 5):
    """
    convert a curve to pe
    """


    cmds.select(curve)
    # attach paint effect to curve
    try:
        mel.eval('source "/usr/autodesk/maya2022/Examples/Paint_Effects/Airbrush/defaultPaint.mel";')
    except Exception as e:
        cmds.warning(e)
    cmds.AttachBrushToCurves()
    stroke_transform = cmds.ls(sl=True)[0]
    stroke_transform = cmds.rename(stroke_transform, curve+'_Stroke')
    cmds.pickWalk(d='down')
    stroke_shape = cmds.ls(sl=True)[0]
    #mel.eval('applyPresetToNode "|{}|{}" "" "" "Brows" 1;'.format(stroke_transform, stroke_shape))
    brush = cmds.listConnections('{}.brush'.format(stroke_shape))[0]
    cmds.setAttr('{}.pressureMap1'.format(stroke_shape), 2)

    if make_pretty:
        #make it pretty
        cmds.setAttr('{}.pressureScale[0].pressureScale_Interp'.format(stroke_shape), 3)
        cmds.setAttr('{}.pressureScale[0].pressureScale_Position'.format(stroke_shape), 0)
        cmds.setAttr('{}.pressureScale[0].pressureScale_FloatValue'.format(stroke_shape), 0.1)

        cmds.setAttr('{}.pressureScale[1].pressureScale_Interp'.format(stroke_shape), 3)
        cmds.setAttr('{}.pressureScale[1].pressureScale_Position'.format(stroke_shape), 0.5)
        cmds.setAttr('{}.pressureScale[1].pressureScale_FloatValue'.format(stroke_shape), 0.9)

        cmds.setAttr('{}.pressureScale[2].pressureScale_Interp'.format(stroke_shape), 3)
        cmds.setAttr('{}.pressureScale[2].pressureScale_Position'.format(stroke_shape), 1)
        cmds.setAttr('{}.pressureScale[2].pressureScale_FloatValue'.format(stroke_shape), 0.1)

        cmds.setAttr('{}.tubeSections'.format(brush), resolution)
        cmds.setAttr('{}.sampleDensity'.format(stroke_shape), 5)

    return stroke_transform

# -----------------------------------------------------------------------------------------------------

def connect_pe_to_ribbon(stroke):

    if not stroke:
        cmds.error('We need a stroke')

    main_ctrl = stroke.replace('_Stroke', '_Main'+nc['ctrl'])
    if not cmds.objExists(main_ctrl):
        cmds.error("no main control matches naming: stroke.replace('_Stroke', '_Main'+nc['ctrl'])")

    #connections to brush


    #connections to paint effect
    #attrs in stroke shape
    attrs = {'minClip':['topLenght', 0, 1, 0], #max length 1 full
             'maxClip':['bottomLenght', 0, 1, 1], #min lenght 0 full
             'sampleDensity':['smooth', 1, 5, 2], #amount of loops 1 is one to 1, 2 is smooth 0 is linear
             'line':'Thickness',
             'pressureScale[0].pressureScale_FloatValue':['startThickness', 0, 2, 0.1], #0 to be thin 1 to be normal 2 to be tick
             'pressureScale[1].pressureScale_FloatValue':['midThickness', 0, 2, 0.9], #0 to be thin 1 to be normal 2 to be tick
             'pressureScale[2].pressureScale_FloatValue':['endThickness', 0, 2, 0.1] #0 to be thin 1 to be normal 2 to be tick
             }

    for attr in attrs:
        if attr == 'line':
            mt.line_attr(input=ctrl_attr, name=attrs[attr])
            continue
        name = attrs[attr][0]
        min = attrs[attr][1]
        max = attrs[attr][2]
        default = attrs[attr][3]
        ctrl_attr = mt.new_attr(input=main_ctrl, name=name, min=min, max=max, default=default)
        #auto_attr = mt.new_attr(input=cmds.listRelatives(main_ctrl, p=True)[0], name='Auto'+name, min=min, max=max, default=0)

        cmds.connectAttr(ctrl_attr, '{}.{}'.format(stroke, attr))



# -----------------------------------------------------------------------------------------------------

def create_toon_outline(geometry):

    cmds.select(geometry)
    mel.eval('AssignNewPfxToon;')
    toon_shape = cmds.ls(sl=True)[0]
    cmds.pickWalk(d='up')
    toon_node = cmds.ls(sl=True)[0]

    return toon_node, toon_shape

# -----------------------------------------------------------------------------------------------------

def convert_outline_to_curves(toon_node_shape):

    if not toon_node_shape:
        cmds.error('No toon_node')

    cmds.select(toon_node_shape)
    mel.eval('doPaintEffectsToCurve( 0);')
    curves_grp = toon_node_shape + 'Curves'
    if not cmds.objExists(curves_grp):
        cmds.error('Need to input shape node to get curves folder. We are currently getting: {}'.fromat(curves_grp))

    #clean_grp = cmds.group(em=True, n=toon_node_shape+'_Strokes'+nc['group'])

    # for cruve in cmds.listRelatives(curves_grp, c=True):
    #     stroke = convert_curve_to_pe(curve=cruve, make_pretty=True)
    #     cmds.parent(stroke, clean_grp)

    return curves_grp

# -----------------------------------------------------------------------------------------------------
def convert_outline_to_geo(toon_node_shape):

    if not toon_node_shape:
        cmds.error('No toon_node')

    cmds.select(toon_node_shape)
    mel.eval('ConvertPaintEffectsToPoly;')


# -----------------------------------------------------------------------------------------------------
def create_camara_based_curve():
    ''

# -----------------------------------------------------------------------------------------------------

def connect_stroke_to_render(stroke, curve, points=5):

    curve_shapes = cmds.listRelatives(curve, s=True)
    stroke_shape = stroke+'Shape'

    ramp = cmds.createNode('ramp', n=curve+'Render_Remap')

    #connect output
    for shape in curve_shapes:
        cmds.connectAttr('{}.outColorR'.format(ramp), '{}.aiCurveWidth'.format(shape), f=True)

    cmds.select(curve)
    cmds.pickWalk(d='Down')
    forced_shape = cmds.ls(sl=True)[0]
    cmds.connectAttr('{}.outColorR'.format(ramp), '{}.aiCurveWidth'.format(forced_shape), f=True)

    for num in range(points):

        float_math = cmds.createNode('floatMath', n=curve+str(num)+'FloatMath')

        # cmds.connectAttr('{}.pressureScale[{}].pressureScale_Position'.format(stroke_shape, num),
        #                  '{}.floatA'.format(float_math), f=True)
        # cmds.connectAttr('{}.outFloat'.format(float_math),
        #                  '{}.colorEntryList[{}].position'.format(ramp, num), f=True)

        cmds.connectAttr('{}.pressureScale[{}].pressureScale_Position'.format(stroke_shape, num),
                         '{}.colorEntryList[{}].position'.format(ramp, num), f=True)

        #connect ramps

        cmds.connectAttr('{}.pressureScale[{}].pressureScale_FloatValue'.format(stroke_shape, num),
                 '{}.colorEntryList[{}].color.colorR'.format(ramp, num), f=True)
        cmds.connectAttr('{}.pressureScale[{}].pressureScale_FloatValue'.format(stroke_shape, num),
                 '{}.colorEntryList[{}].color.colorG'.format(ramp, num), f=True)
        cmds.connectAttr('{}.pressureScale[{}].pressureScale_FloatValue'.format(stroke_shape, num),
                 '{}.colorEntryList[{}].color.colorB'.format(ramp, num), f=True)
        
        
        #apply marvel preset:
        mel.eval('applyPresetToNode "{}" "" "" "MarvelRamp" 1;'.format(ramp))