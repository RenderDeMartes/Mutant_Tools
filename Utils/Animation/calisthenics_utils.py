from __future__ import absolute_import
"""
version: 1.0.0
date: 21/04/2020

#----------------

how to:

import Mutant_Tools
try:
    import importlib;from importlib import reload
except:
    import imp;from imp import reload


from Mutant_Tools.Utils.Animation import calisthenics_utils
reload(calisthenics_utils)

#----------------
dependencies:

json
pymel
maya mel
maya.cmds
studio library

#----------------
licence: https://www.eulatemplate.com/live.php?token=FGISW7ApRfgywum6murbBmLcusKONzkv
author:  Esteban Rodriguez <info@mutanttools.com>

"""


try:
    import importlib;
    from importlib import reload
except:
    import imp;
    from imp import reload
from maya import cmds
try:
    from rigSystem.assetTemplates.core import get_one_sid
    from studiolibrarymaya import animitem
except:
    pass
from Mutant_Tools.Utils.Animation import studio_library_utils
reload(studio_library_utils)

import os


def set_timeline():
    cmds.playbackOptions(min=1, max=530)

def load_animtion():
    sid = get_one_sid()
    anim_path = '/job/anythinggoes/pipeline/studiolibrary/Rigging - ROM/ROMs/Rom2.anim'
    anim_path = os.path.join(anim_path)

    objects = cmds.ls(':'.join([sid.namespace or "", '*_ctrl']))
    objects.extend(cmds.ls(':'.join([sid.namespace or "", '*_Ctrl'])))

    animitem.load(anim_path, objects=objects, option="replace all", connect=False, currentTime=False)

def show_only_polys():
    panelNames = cmds.getPanel(type='modelPanel')
    for each in panelNames:
        cmds.modelEditor(each, e=True, nurbsCurves=False, joints=False, dynamics=False, pivots=False, cameras=False)


def set_camera_angle():
    cameras = ['body_cam', 'face_cam']
    for cam in cameras:
        if cmds.objExists(cam + '1'):
            cmds.delete(cam + '1')
        cmds.camera(name=cam)

    # Body Cam
    cmds.move(240, 170, 475, 'body_cam1')
    cmds.rotate(-5, 25, 0, 'body_cam1')

    cmds.lookThru('body_cam1')

    # FaceCam
    if cmds.objExists('Head_Ctrl'):
        cmds.delete(cmds.parentConstraint('Head_Ctrl', 'face_cam1'))
        cmds.setAttr('face_cam1.tz', 75)
        cmds.parentConstraint('Head_Ctrl', 'face_cam1', mo=True)


def create_copies():
    move_map = {
        'left_instance': [-145, 0, 45, 0, -90, 0, 1, 1, 1],
        'right_instance': [145, 0, -45, 0, 90, 0, 1, 1, 1],
        'up_instance': [90, 220, -45, 90, 0, 90, 0.5, 0.5, 0.5],
    }

    geo = 'geo'
    for side in move_map:
        if cmds.objExists(side):
            cmds.delete(side)
        instance_obj = cmds.duplicate(geo, instanceLeaf=True, name=side)[0]
        cmds.parent(instance_obj, w=True)
        print(move_map[side])
        cmds.move(move_map[side][0], move_map[side][1], move_map[side][2], instance_obj)
        cmds.rotate(move_map[side][3], move_map[side][4], move_map[side][5], instance_obj)

    cmds.select(cl=True)


def create_sectret_node():
    from datetime import date
    today = date.today()
    node= 'calisthenics_{}_{}_{}'.format(today.day, today.month, today.year)
    if not cmds.objExists(node):
        cmds.createNode('network', n=node)

def clean_rom():
    cmds.playbackOptions(min=0, max=200, ps=1)
    cmds.currentTime(1)

    cmds.select('*_Ctrl')

    mySel = cmds.ls(sl=1)
    cmds.cutKey(mySel, s=True)

    instances = ['left_instance', 'right_instance', 'up_instance']
    for ins in instances:
        if cmds.objExists(ins):
            cmds.delete(ins)

    cameras = ['body_cam1', 'face_cam1']
    for cam in cameras:
        if cmds.objExists(cam):
            cmds.delete(cam)

    create_sectret_node()

# clean_rom()

def create_rom():
    set_timeline()
    load_animtion()
    show_only_polys()
    set_camera_angle()
    create_copies()
    create_sectret_node()