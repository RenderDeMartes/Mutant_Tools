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


from Mutant_Tools.Utils.Animation import animation_utils
reload(animation_utils)

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


from maya import cmds

def set_time_slider(start, end):
    cmds.playbackOptions(min=start, max=end, ps=1)
    cmds.currentTime(1000)

def delete_keys():

    cmds.playbackOptions(min= 0 , max= 200, ps=1)
    cmds.currentTime(1)
    try:
        cmds.select('*_ctrl')
    except:
        cmds.select('*_Ctrl')

    mySel = cmds.ls(sl=1)  # my current selection
    cmds.cutKey(mySel, s=True)  # delete key command

def check_rotations(ctrl=None):

    if not ctrl:
        ctrl = cmds.ls(sl=True)[0]

def select_ctrls_from_sid(sid= None):

    if not sid:
        sel = cmds.ls(sl=True, l=True)[0]
        if cmds.nodeType(sel)=='sid':
            print('Sid Node:', sel)
        else:
            print('Sid Node Not Found, Searching...')
            splited_name = sel.split('|')
            for name in splited_name:
                if cmds.objExists(name):
                    if cmds.nodeType(name)=='sid':
                        sid = name
                        print('Sid Node found:', sid)

    sid_controllers = []
    for node in cmds.listRelatives(sid, ad=True):
        if node.endswith('_ctrl') or node.endswith('_Ctrl'):
            sid_controllers.append(node)

    cmds.select(sid_controllers)
    return sid_controllers

def global_ctrl_movements():

    delete_keys()

    master_ctrl = 'Global_Ctrl'
    if not cmds.objExists(master_ctrl):
        master_ctrl = 'master_ctrl'

    animation = {
                 1: {'translate': [0, 0, 0], 'rotate': [0, 0, 0], 'scale': [1, 1, 1]},
                 10: {'translate': [500, 500, 500], 'rotate': [0, 0, 0], 'scale': [1, 1, 1]},
                 20: {'translate': [500, 500, 500], 'rotate': [0, 0, 180], 'scale': [1, 1, 1]},
                 30: {'translate': [500, 500, 500], 'rotate': [0, 180, 180], 'scale': [1, 1, 1]},
                 40: {'translate': [500, 500, 500], 'rotate': [0, 180, 180], 'scale': [1, 1, 1]},
                 50: {'translate': [500, 500, 500], 'rotate': [0, 180, 180], 'scale': [10, 10, 10]},
                 60: {'translate': [500, 500, 500], 'rotate': [0, 180, 180], 'scale': [0.1, 0.1, 0.1]},
                 70: {'translate': [0, 0, 0], 'rotate': [0, 0, 0], 'scale': [1, 1, 1]}
                }

    for frame in animation:
        cmds.currentTime(frame)
        anim_frame = animation[frame]
        translate = anim_frame['translate']
        rotation = anim_frame['rotate']
        scale = anim_frame['scale']

        cmds.select(master_ctrl)
        cmds.move(translate[0], translate[1], translate[2])
        cmds.rotate(rotation[0], rotation[1], rotation[2])
        try:
            cmds.setAttr('{}.size'.format(master_ctrl), scale[0])
        except:
            cmds.scale(scale[0], scale[1], scale[2])

        cmds.setKeyframe()

    cmds.currentTime(1)

def create_rotate_nighty(ctrl=None, start_frame=0):

    if not ctrl:
        ctrl = cmds.ls(sl=True)[0]

    animation = {
                 1: {'translate': [0, 0, 0], 'rotate': [0, 0, 0], 'scale': [1, 1, 1]},
                 10: {'translate': [0, 0, 0], 'rotate': [0, 0, 90], 'scale': [1, 1, 1]},
                 20: {'translate': [0, 0, 0], 'rotate': [0, 0, 0], 'scale': [1, 1, 1]},
                 30: {'translate': [0, 0, 0], 'rotate': [0, 0, -90], 'scale': [1, 1, 1]},
                 40: {'translate': [0, 0, 0], 'rotate': [0, 0, 0], 'scale': [1, 1, 1]},
                 50: {'translate': [0, 0, 0], 'rotate': [0, 90, 0], 'scale': [1, 1, 1]},
                 60: {'translate': [0, 0, 0], 'rotate': [0, 0, 0], 'scale': [1, 1, 1]},
                 70: {'translate': [0, 0, 0], 'rotate': [0, -90, 0], 'scale': [1, 1, 1]},
                 80: {'translate': [0, 0, 0], 'rotate': [0, 0, 0], 'scale': [1, 1, 1]},
                 90: {'translate': [0, 0, 0], 'rotate': [90, 0, 0], 'scale': [1, 1, 1]},
                 100: {'translate': [0, 0, 0], 'rotate': [0, 0, 0], 'scale': [1, 1, 1]},
                 110: {'translate': [0, 0, 0], 'rotate': [-90, 0, 0], 'scale': [1, 1, 1]}
            }

    for frame in animation:
        cmds.currentTime(start_frame+frame)
        anim_frame = animation[start_frame+frame]
        translate = anim_frame['translate']
        rotation = anim_frame['rotate']
        scale = anim_frame['scale']

        cmds.select(ctrl)
        cmds.setAttr('{}.translateX'.format(ctrl), translate[0])
        cmds.setAttr('{}.translateY'.format(ctrl), translate[1])
        cmds.setAttr('{}.translateZ'.format(ctrl), translate[2])

        cmds.setAttr('{}.rotateX'.format(ctrl), rotation[0])
        cmds.setAttr('{}.rotateY'.format(ctrl), rotation[1])
        cmds.setAttr('{}.rotateZ'.format(ctrl), rotation[2])

        cmds.setAttr('{}.scaleX'.format(ctrl), scale[0])
        cmds.setAttr('{}.scaleY'.format(ctrl), scale[1])
        cmds.setAttr('{}.scaleZ'.format(ctrl), scale[2])


        cmds.setKeyframe()
        cmds.currentTime(1)


def create_follow_cam():
    ''

def create_anim_instances(geo='geo', poses_positions=None):
    """

    Args:
        geo: string geo to duplicate/instance
        poses_positions: dictionary with positions for instances

    Returns: instances


    """

    if not poses_positions:
        poses_positions = {
            'left': [-150, 0, 0, 0, -90, 0, 0.5, 0.5, 0.5],
            'right': [-150, 100, 0, 0, 90, 0, 0.5, 0.5, 0.5],
            'back': [150, 0, 0, 0, 180, 0, 0.5, 0.5, 0.5],
            '3_4_front': [150, 100, 0, 0, 45, 0, 0.5, 0.5, 0.5],
        }

    instances = []
    for pose in poses_positions:
        instance = cmds.instance(geo)[0]
        cmds.parent(instance, w=True)
        cmds.group()
        cmds.move(poses_positions[pose][0], poses_positions[pose][1], poses_positions[pose][2])
        cmds.rotate(poses_positions[pose][3], poses_positions[pose][4], poses_positions[pose][5])
        cmds.scale(poses_positions[pose][6], poses_positions[pose][7], poses_positions[pose][8])
        instances.append(instance)


    return instances
