from __future__ import absolute_import, division
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

import maya.cmds as cmds
from maya.api import OpenMaya as om2
import math as math
import ngSkinTools2.api as ngskin2


def create_pupil_dilation(eye_center='', eye_tip='', edges=[], iris_loop=[], side='', eye_mesh='', ctrl=''):
    ####################### CREATE JOINTS ################################

    # sometimes the input feeds in incorrectly, if problem persists try cmds.filterExpand(sm=32)
    edges = cmds.filterExpand(edges, sm=32)
    loops = [cmds.polySelectSp(edge, q=True, loop=True) for edge in edges]

    cmds.joint(eye_center, e=1, oj='xyz', sao='yup', zso=1)

    jnts = []

    for i, loop in enumerate(loops):
        cluster = cmds.cluster(loop)
        cmds.select(clear=1)
        if i > 0:
            cmds.select(jnts[i - 1])
        jnt = cmds.joint(n='{}_Eye_PupilDilation_{:02}_jnt'.format(side, i))
        cmds.delete(cmds.parentConstraint(cluster, jnt))
        cmds.delete(cmds.orientConstraint(eye_center, jnt))
        cmds.makeIdentity(jnt, apply=1, r=1)
        cmds.delete(cluster)
        jnts.append(jnt)

    #cmds.joint(jnts, e=1, oj='xyz', sao='yup', zso=1)
    #cmds.setAttr('{}.jointOrient'.format(jnts[-1]), 0, 0, 0, type='double3')

    joints_parent = cmds.group(em=1, n='{}_PupilDilationJoints_grp'.format(side))
    cmds.delete(cmds.parentConstraint(eye_center, joints_parent))
    cmds.parent(jnts, joints_parent)

    for j in jnts:
        
        cmds.setAttr('{}.ty'.format(j), 0)
        cmds.setAttr('{}.tz'.format(j), 0)

        offset = cmds.group(em=1, n='{}_offset'.format(j))
        cmds.parent(offset, joints_parent)
        cmds.delete(cmds.parentConstraint(j, offset))
        cmds.parent(j, offset)

    ##################### SKIN EYE ##############################

    if not eye_mesh:
        cmds.error('Must provide a valid mesh, given mesh is: {}'.format(eye_mesh))

    skin_cls = cmds.skinCluster(jnts, eye_mesh, tsb=1)[0]
    layers = ngskin2.init_layers(skin_cls)

    base_layer = layers.add('base weights')

    ngskin2.assign_from_closest_joint(skin_cls, base_layer, [0])

    settings = ngskin2.FloodSettings()
    settings.mode = ngskin2.PaintMode.replace
    settings.intensity = 1

    for i, jnt in enumerate(jnts):
        cmds.select(loops[i])
        ngskin2.flood_weights(layer=base_layer, influence=i, settings=settings)

    ####################### GRAPH SETUP ############################

    eye_center_pos = cmds.xform(eye_center, q=1, t=1, ws=1)
    eye_tip_pos = cmds.xform(eye_tip, q=1, t=1, ws=1)
    eye_center_pos = om2.MVector(eye_center_pos)
    eye_tip_pos = om2.MVector(eye_tip_pos)
    displacement = eye_tip_pos - eye_center_pos
    radius = displacement.length()

    def distance2angle(target_distance, max_distance):
        distance_normalized = target_distance / max_distance
        theta = math.asin(distance_normalized)
        return math.degrees(theta)

    def linearAttenuationFromMidpoint(value, start, end):
        midpoint = (start + end) / 2
        result = 1 - abs(value - midpoint) / (midpoint - start)
        return max(0, result)

    iris_cluster = cmds.cluster(iris_loop)
    iris_pos = cmds.xform(iris_cluster, q=1, rp=1, ws=1)
    iris_pos = om2.MVector(iris_pos)
    print('eye_center_pos = {}. /n iris_pos = {}'.format(eye_center_pos, iris_pos))
    center_to_iris = iris_pos - eye_center_pos
    iris_angle = distance2angle(center_to_iris.length(), radius)
    cmds.delete(iris_cluster)

    # sub_jnts = jnts[1:-1]
    jnts_offsets = [cmds.listRelatives(j, p=1)[0] for j in jnts]
    for j in jnts_offsets:
        tx = cmds.getAttr('{}.tx'.format(j))
        print('joint = {}, tx = {}, radius = {}'.format(j, tx, radius))
        theta = distance2angle(tx, radius)

        iris_atten = cmds.createNode('floatMath', n=j + '_irisAtten')
        cmds.setAttr('{}.operation'.format(iris_atten), 2)
        cmds.connectAttr('{}.iris'.format(ctrl), '{}.floatA'.format(iris_atten))
        iris_atten_value = linearAttenuationFromMidpoint(theta, 0, 90)
        cmds.setAttr('{}.floatB'.format(iris_atten), iris_atten_value)

        pupil_atten = cmds.createNode('floatMath', n=j + '_pupilAtten')
        cmds.setAttr('{}.operation'.format(pupil_atten), 2)
        cmds.connectAttr('{}.pupil'.format(ctrl), '{}.floatA'.format(pupil_atten))
        pupil_atten_value = linearAttenuationFromMidpoint(theta, iris_angle, 90)
        cmds.setAttr('{}.floatB'.format(pupil_atten), pupil_atten_value)

        added_offsets = cmds.createNode('floatMath', n=j + '_addedOffsets')
        cmds.connectAttr('{}.outFloat'.format(pupil_atten), '{}.floatA'.format(added_offsets))
        cmds.connectAttr('{}.outFloat'.format(iris_atten), '{}.floatB'.format(added_offsets))

        angle_offset = cmds.createNode('floatMath', n=j + '_angleOffset')
        cmds.connectAttr('{}.outFloat'.format(added_offsets), '{}.floatA'.format(angle_offset))
        # cmds.connectAttr('ctrl.pupil', '{}.floatA'.format(angle_offset))
        cmds.setAttr('{}.floatB'.format(angle_offset), theta)

        remap_90 = cmds.createNode('remapValue', n='{}_clamp'.format(j))
        cmds.connectAttr('{}.outFloat'.format(angle_offset), '{}.inputValue'.format(remap_90))
        cmds.setAttr('{}.inputMax'.format(remap_90), 90)
        cmds.setAttr('{}.outputMax'.format(remap_90), 90)

        double_angle = cmds.createNode('floatMath', n=j + '_doubleAngle')
        cmds.setAttr('{}.operation'.format(double_angle), 2)
        cmds.setAttr('{}.floatB'.format(double_angle), 2)
        cmds.connectAttr('{}.outValue'.format(remap_90), '{}.floatA'.format(double_angle))

        sincos = cmds.createNode('eulerToQuat', n=j + 'sincos')
        cmds.connectAttr('{}.outFloat'.format(double_angle), '{}.inputRotateX'.format(sincos))

        remap2radius = cmds.createNode('remapValue', n=j + '_remap2Radius')
        # cmds.setAttr('{}.value[0].value_Interp'.format(remap2radius), 2)
        cmds.setAttr('{}.outputMax'.format(remap2radius), radius)
        cmds.connectAttr('{}.outputQuatX'.format(sincos), '{}.inputValue'.format(remap2radius))
        cmds.connectAttr('{}.outValue'.format(remap2radius), '{}.tx'.format(j))

        scale_reciprocate = cmds.createNode('floatMath', n=j + '_reciprocate')
        cmds.setAttr('{}.operation'.format(scale_reciprocate), 2)
        cmds.connectAttr('{}.outputQuatW'.format(sincos), '{}.floatA'.format(scale_reciprocate))
        reciprocate = 1.0 / cmds.getAttr('{}.floatA'.format(scale_reciprocate))
        cmds.setAttr('{}.floatB'.format(scale_reciprocate), reciprocate)
        cmds.connectAttr('{}.outFloat'.format(scale_reciprocate), '{}.sy'.format(j))
        cmds.connectAttr('{}.outFloat'.format(scale_reciprocate), '{}.sz'.format(j))

    return joints_parent
    #---------------------------------------------

TAB_FOLDER = '003_Facial'
PYBLOCK_NAME = 'exec_pupil_dilation'


#---------------------------------------------

def create_pupil_dilation_block(name = 'Pupil_Dilation'):

    nc, curve_data, setup = mt.import_configs()

    # Read name conventions as nc[''] and setup as setup['']
    PATH = os.path.dirname(__file__)
    PATH = Path(PATH)
    PATH_PARTS = PATH.parts[:-2]
    FOLDER = ''
    for f in PATH_PARTS:
        FOLDER = os.path.join(FOLDER, f)

    MODULE_FILE = os.path.join(os.path.dirname(__file__), '017_PupilDilation.json')
    with open(MODULE_FILE) as module_file:
        module = json.load(module_file)


    #name checks and block creation
    name = mt.ask_name(text = module['Name'])
    if cmds.objExists('{}{}'.format(name,nc['module'])):
        cmds.warning('Name already exists.')
        return ''

    block, config = mt.create_block(name = name, icon = 'Pupil',  attrs = module['attrs'], build_command = module['build_command'], import_command = module['import'])

    side = ''
    if nc['left'] in name:
        side = nc['left']
    elif nc['right'] in name:
        side = nc['right']

    eye_center = mt.create_joint_guide(name = side + 'eyeCenter')
    cmds.move(2,0,0)
    eye_tip = mt.create_joint_guide(name = side + 'eyeTip')
    cmds.move(2,0,5)
    cmds.parent(eye_tip, eye_center)
    cmds.parent(eye_center, block)
    cmds.select(block)

    print('{} Created Successfully'.format(name))

#create_eyes_block()


def build_pupil_dilation_block():

    nc, curve_data, setup = mt.import_configs()

    mt.check_is_there_is_base()

    block = cmds.ls(sl=True)
    config = cmds.listConnections(block)[1]
    block = block[0]
    guide = cmds.listRelatives(block, c=True)[0]

    name = block.replace('_Block', '')

    # groups for later cleaning
    clean_rig_grp = cmds.group(em=True, name=name+'_Rig'+nc['group'])
    cmds.parent(clean_rig_grp, '{}{}'.format(setup['rig_groups']['misc'], nc['group']))

    mt.orient_joint(input=guide)
    new_guide = mt.duplicate_and_remove_guides(guide)
    eye_center = new_guide
    eye_tip = cmds.listRelatives(eye_center, c=1)[0]

    eye_mesh = cmds.getAttr('{}.SetEyeMesh'.format(config))
    eye_edge_ring = cmds.getAttr('{}.SetEyeEdgeRing'.format(config)).replace(' ', '')
    iris_edge_loop = cmds.getAttr('{}.SetIrisEdgeLoop'.format(config)).replace(' ', '')
    eye_blend_shape_node = cmds.getAttr('{}.SetBlendShapeNode'.format(config))
    target_ctrl = cmds.getAttr('{}.SetTargetCtrl'.format(config))

    mirror = cmds.getAttr('{}.Mirror'.format(config))

    if not cmds.objExists(eye_mesh):
        raise Exception('Could not find {}'.format(eye_mesh))

    eye_mesh_copy = cmds.duplicate(eye_mesh, n=eye_mesh.replace('_hi', '') + '_bs')[0]
    # convert selections to duplicate mesh components
    # TODO: search another solution, since this is pretty fucking stupid
    eye_edge_ring = eye_edge_ring.replace(eye_mesh, eye_mesh_copy)
    iris_edge_loop = iris_edge_loop.replace(eye_mesh, eye_mesh_copy)

    def attach_mesh_copy_to_bs_node(bs_node, og_mesh, mesh_copy):

        if bs_node == 'new_blendshape_node':
            bs_node = cmds.blendShape(mesh_copy, og_mesh)[0]
            cmds.setAttr('{}.{}'.format(bs_node, mesh_copy), 1)

        elif not cmds.objExists(bs_node):
            raise Exception('Could not find {}'.format(bs_node))

        else:
            target_index = cmds.blendShape(bs_node, q=1, weightCount=1)
            cmds.blendShape(bs_node, e=1, t=(og_mesh, target_index, mesh_copy, 1))

    attach_mesh_copy_to_bs_node(eye_blend_shape_node, eye_mesh, eye_mesh_copy)

    # check and add dilation attrs to target ctrl
    def check_ctrl_attrs(ctrl=''):

        if not cmds.attributeQuery('iris', n=ctrl, exists=1):
            cmds.addAttr(ctrl, ln='iris', k=1)
        if not cmds.attributeQuery('pupil', n=ctrl, exists=1):
            cmds.addAttr(ctrl, ln='pupil', k=1)

    check_ctrl_attrs(target_ctrl)

    jnts_parent = create_pupil_dilation(eye_center=eye_center, eye_tip=eye_tip, edges=eye_edge_ring.split(','), iris_loop=iris_edge_loop.split(','), side='L', eye_mesh=eye_mesh_copy, ctrl=target_ctrl)

    cmds.parent(eye_center, clean_rig_grp)
    cmds.parent(eye_mesh_copy, clean_rig_grp)
    cmds.parent(jnts_parent, clean_rig_grp)

    if mirror:
        #mirrorJoint -mirrorYZ -mirrorBehavior -searchReplace "L_" "R_";
        r_eye_center, r_eye_tip = cmds.mirrorJoint(eye_center, mirrorYZ=1, searchReplace=('L_', 'R_'))
        r_edges = eye_edge_ring.replace(nc['left'], nc['right'])
        r_iris_loop = iris_edge_loop.replace(nc['left'], nc['right'])
        print('r_iris_loop = {}'.format(r_iris_loop))
        r_eye_mesh = eye_mesh.replace(nc['left'], nc['right'])
        r_eye_mesh_copy = cmds.duplicate(r_eye_mesh, n=r_eye_mesh.replace('_hi', '') + '_bs')[0]
        r_bs_node = eye_blend_shape_node.replace(nc['left'], nc['right'])
        attach_mesh_copy_to_bs_node(r_bs_node, r_eye_mesh, r_eye_mesh_copy)
        r_target_ctrl = target_ctrl.replace(nc['left'], nc['right'])
        check_ctrl_attrs(r_target_ctrl)
        r_jnts_parent = create_pupil_dilation(eye_center=r_eye_center, eye_tip=r_eye_tip, edges=r_edges.split(','),
                              iris_loop=r_iris_loop.split(','), side='R', eye_mesh=r_eye_mesh_copy, ctrl=r_target_ctrl)

        r_clean_rig_grp = cmds.group(em=1, n=clean_rig_grp.replace(nc['left'], nc['right']))
        cmds.parent(r_clean_rig_grp, '{}{}'.format(setup['rig_groups']['misc'], nc['group']))

        cmds.parent(r_eye_center, r_clean_rig_grp)
        cmds.parent(r_eye_mesh_copy, r_clean_rig_grp)
        cmds.parent(r_jnts_parent, r_clean_rig_grp)



