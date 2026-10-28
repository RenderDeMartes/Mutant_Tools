from __future__ import absolute_import
from maya import cmds
import json
try:
    import importlib;from importlib import reload
except:
    import imp;from imp import reload

import os
from pathlib import Path
from maya.api import OpenMaya as om

import Mutant_Tools
import Mutant_Tools.Utils.Rigging
from Mutant_Tools.Utils.Rigging import main_mutant
reload(Mutant_Tools.Utils.Rigging.main_mutant)

mt = main_mutant.Mutant()

#---------------------------------------------
TAB_FOLDER = '003_Facial'
PYBLOCK_NAME = 'exec_faceautomations'

#Read name conventions as nc[''] and setup as seup['']
PATH = os.path.dirname(__file__)
PATH = Path(PATH)
PATH_PARTS = PATH.parts[:-3]
FOLDER=''
for f in PATH_PARTS:
	FOLDER = os.path.join(FOLDER, f)

JSON_FILE = os.path.join(FOLDER, 'config', 'name_conventions.json')
with open(JSON_FILE) as json_file:
	nc = json.load(json_file)

MODULE_FILE = os.path.join(os.path.dirname(__file__), '019_FaceAutomations_v001.json')
with open(MODULE_FILE) as module_file:
    module = json.load(module_file)

# Defaults of the keyable weight attrs the block adds to the ctrls (block
# _float attrs are integers 1-20, so the weights live on the ctrls instead)
WEIGHTS = {
    'CheekBoneWeight': 0.75,       # cheek follow of the cheekbone
    'CheekMouthWeight': 1.0,       # cheek follow of the mouth corner
    'CheekBoneMouthWeight': 0.15,  # cheekbone follow of the mouth corner
    'CheekWidePush': 0.5,          # cheek push per unit of corner tx
    'CheekUpPush': 0.5,            # cheek push per unit of corner ty
    'NostrilNoseWeight': 3.0,      # nostril follow of the nose
    'NostrilLipWeight': 0.5,       # nostril follow of the upper lip
    'NostrilCornerWeight': 0.0,    # nostril follow of the mouth corner
    'NostrilHeadWeight': 1.0,      # HeadAndCorner mode: nostril follow of the head
    'NostrilHeadCornerWeight': 0.25,  # HeadAndCorner mode: nostril follow of the mouth corner
}

#---------------------------------------------

def create_faceautomations_block(name = 'FaceAutomations'):

    nc, curve_data, setup = mt.import_configs()

    #name checks and block creation
    name = mt.ask_name(text = module['Name'])
    if cmds.objExists('{}{}'.format(name,nc['module'])):
        cmds.warning('Name already exists.')
        return ''

    block = mt.create_block(name = name, icon = 'FaceAutomations',  attrs = module['attrs'], build_command = module['build_command'], import_command = module['import'])
    config = block[1]
    block = block[0]

    cmds.select(block)

    print('{} Created Successfully'.format(name))

#create_faceautomations_block()

#-------------------------

def build_faceautomations_block():
    """Cheek and nostril automations, built after the cheek, cheekbone,
    nose and mouth blocks. Every Set field is the left side node, the right
    side is the same name with the right prefix."""

    nc, curve_data, setup = mt.import_configs()

    mt.check_is_there_is_base()

    block = cmds.ls(sl=True)
    config = cmds.listConnections(block)[1]
    block = block[0]

    defaults = dict((key.rsplit('_', 1)[0], value) for key, value in module['attrs'].items())

    def config_value(attr):
        """Block attr, or its JSON default on blocks made before it existed."""
        if cmds.attributeQuery(attr, n=config, exists=True):
            return cmds.getAttr('{}.{}'.format(config, attr))
        value = defaults.get(attr)
        if value in ('True', 'False'):
            return value == 'True'
        return value

    sides = [nc['left'], nc['right']]

    def node(attr, side):
        """Set field for this side, None (with a warning) when missing."""
        name = (config_value(attr) or '').strip()
        if not name:
            return None
        name = side_name(name, side)
        if not cmds.objExists(name):
            cmds.warning('{}: {} not found, skipped.'.format(block, name))
            return None
        return name

    # Cheek follows the cheekbone and the mouth corner (weights on the cheek ctrl)
    if config_value('CheekFollow'):
        for side in sides:
            cheek, cheekbone, corner = [node(a, side) for a in ('SetCheekCtrl', 'SetCheekBoneCtrl', 'SetMouthCornerCtrl')]
            if cheek and cheekbone and corner:
                weighted_follow(cheek, [(cheekbone, WEIGHTS['CheekBoneWeight']),
                                        (corner, WEIGHTS['CheekMouthWeight'])])
            if config_value('CheekScaleToJoint'):
                joint = node('SetCheekJoint', side)
                if cheek and joint:
                    cmds.connectAttr(cheek + '.scale', joint + '.scale', f=True)

    # Cheekbone rides up and down with the mouth corner (translate Y only)
    if config_value('CheekBoneFollow'):
        for side in sides:
            cheekbone, offset, corner = [node(a, side) for a in ('SetCheekBoneCtrl', 'SetCheekBoneOffset', 'SetMouthCornerCtrl')]
            if cheekbone and offset and corner:
                weighted_follow(cheekbone, [(offset, 1.0), (corner, WEIGHTS['CheekBoneMouthWeight'])],
                                skip_translate=('x', 'z'), skip_rotate=('x', 'y', 'z'))

    # Cheek puffs out when the mouth corner goes up or wide
    if config_value('CheekPush'):
        pushes = {}
        for side in sides:
            cheek, corner = [node(a, side) for a in ('SetCheekCtrl', 'SetMouthCornerCtrl')]
            if cheek and corner:
                pushes[side] = cheek_push(cheek, corner, WEIGHTS['CheekWidePush'], WEIGHTS['CheekUpPush'])
        # the right push goes the mirrored way of the left one, whatever the
        # cheek group frames ended up being
        if len(pushes) == 2:
            left, right = pushes[nc['left']], pushes[nc['right']]
            if (mirrored(push_axis(left['group'])) * push_axis(right['group'])) < 0:
                cmds.setAttr(right['sign'] + '.input2X', -1)

    # Nostril follow, NostrilMode:
    #   NoseLipCorner: between the nose, the upper lip and the mouth corner
    #   HeadAndCorner: head plus a bit of the mouth corner, translate only
    if config_value('NostrilFollow'):
        if cmds.attributeQuery('NostrilMode', n=config, exists=True):
            nostril_mode = cmds.getAttr(config + '.NostrilMode', asString=True)
        else:
            nostril_mode = defaults['NostrilMode'].split(':')[0]
        for side in sides:
            if nostril_mode == 'HeadAndCorner':
                nostril, head, corner = [node(a, side) for a in ('SetNostrilCtrl', 'SetHeadCtrl', 'SetMouthCornerCtrl')]
                if nostril and head and corner:
                    weighted_follow(nostril, [(head, WEIGHTS['NostrilHeadWeight']),
                                              (corner, WEIGHTS['NostrilHeadCornerWeight'])],
                                    skip_rotate=('x', 'y', 'z'))
                continue
            nostril, nose, lip, sub = [node(a, side) for a in ('SetNostrilCtrl', 'SetNoseCtrl', 'SetUpperLipCtrl', 'SetMouthSubCtrl')]
            if nostril and nose and lip and sub:
                weighted_follow(nostril, [(nose, WEIGHTS['NostrilNoseWeight']),
                                          (lip, WEIGHTS['NostrilLipWeight']),
                                          (sub, WEIGHTS['NostrilCornerWeight'])],
                                attr_names=['NoseInfluence', 'LipInfluence', 'MouthCornerInfluence'])

    cmds.select(block)
    print('Build {} Success'.format(block))

#build_faceautomations_block()

#------------------------------------
#-----------Extra Functions----------
#------------------------------------

def side_name(name, side):
    """Swap the left / right prefix of a Set field to this side (center
    names like Nose_Main_Ctrl stay the same)."""
    for prefix in (nc['left'], nc['right']):
        if name.startswith(prefix):
            return side + name[len(prefix):]
    return name


def insert_group(ctrl, suffix):
    """Group right above ctrl at its exact rest frame. An identity group +
    relative parent keeps the ctrl channels clean on mirrored ctrls
    (mt.root_grp matches with a parentConstraint, which drops the mirror and
    leaves the ctrl with scale -1)."""
    name = ctrl + suffix + nc['group']
    if cmds.objExists(name):
        return name
    grp = cmds.createNode('transform', n=name, p=cmds.listRelatives(ctrl, p=True)[0])
    cmds.parent(ctrl, grp, r=True)
    return grp


def weighted_follow(ctrl, drivers, attr_names=None, skip_translate=(), skip_rotate=()):
    """Root + Auto groups above ctrl, the Auto group follows every driver
    (parentConstraint mo=True, shortest), and each weight is a keyable attr
    on the ctrl (named after its driver unless attr_names is given)."""
    insert_group(ctrl, nc['root'])
    auto = insert_group(ctrl, nc['auto'])
    names = attr_names or [d.replace(':', '_') for d, _ in drivers]

    kwargs = {'mo': True}
    if skip_translate:
        kwargs['skipTranslate'] = list(skip_translate)
    if skip_rotate:
        kwargs['skipRotate'] = list(skip_rotate)
    pc = cmds.parentConstraint([d for d, _ in drivers], auto, **kwargs)[0]
    cmds.setAttr(pc + '.interpType', 2)

    weights = cmds.parentConstraint(pc, q=True, wal=True)
    for (driver, default), attr, weight in zip(drivers, names, weights):
        if not cmds.attributeQuery(attr, n=ctrl, exists=True):
            cmds.addAttr(ctrl, ln=attr, at='double', min=0, dv=default, k=True)
        cmds.connectAttr('{}.{}'.format(ctrl, attr), '{}.{}'.format(pc, weight), f=True)
    return auto


def cheek_push(cheek, corner, wide_default, up_default):
    """Push group above the cheek ctrl, moved along its Z by the positive
    side of the corner tx (WidePush) and ty (UpPush)."""
    push = insert_group(cheek, '_Push')
    for attr, default in (('WidePush', wide_default), ('UpPush', up_default)):
        if not cmds.attributeQuery(attr, n=cheek, exists=True):
            cmds.addAttr(cheek, ln=attr, at='double', min=0, dv=default, k=True)

    # only the positive side of each corner channel pushes
    clamp = cmds.createNode('clamp', n=cheek + '_Push_Clamp')
    cmds.setAttr(clamp + '.max', 1e6, 1e6, 0)
    cmds.connectAttr(corner + '.tx', clamp + '.inputR')
    cmds.connectAttr(corner + '.ty', clamp + '.inputG')

    amount = cmds.createNode('multiplyDivide', n=cheek + '_Push_MD')
    cmds.connectAttr(clamp + '.outputR', amount + '.input1X')
    cmds.connectAttr(clamp + '.outputG', amount + '.input1Y')
    cmds.connectAttr(cheek + '.WidePush', amount + '.input2X')
    cmds.connectAttr(cheek + '.UpPush', amount + '.input2Y')

    total = cmds.createNode('plusMinusAverage', n=cheek + '_Push_PMA')
    cmds.connectAttr(amount + '.outputX', total + '.input1D[0]')
    cmds.connectAttr(amount + '.outputY', total + '.input1D[1]')

    sign = cmds.createNode('multiplyDivide', n=cheek + '_Push_Sign_MD')
    cmds.connectAttr(total + '.output1D', sign + '.input1X')
    cmds.connectAttr(sign + '.outputX', push + '.translateZ')
    return {'group': push, 'sign': sign}


def push_axis(group):
    m = cmds.xform(group, q=True, ws=True, m=True)
    return om.MVector(m[8:11]).normal()


def mirrored(vector):
    return om.MVector(-vector.x, vector.y, vector.z)
