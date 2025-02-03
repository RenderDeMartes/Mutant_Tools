from __future__ import absolute_import
try:from studiolibrarymaya import animitem
except:pass

from maya import cmds

def load_rom(path_animation = None, objects = 'controllers', start = 1000, end = 1600):

    if not path_animation:
        path_animation = '/job/anythinggoes/pipeline/studiolibrary/Rigging - ROM/Body_ROM_noNS.anim'

    if objects == 'controllers':
        try:
            cmds.select('*_ctrl', '*_Ctrl')
        except:
            try:
                cmds.select('*_ctrl')
            except:
                cmds.select('*_Ctrl')


    objects = cmds.ls(selection=True) or []

    # Loading an animation item
    animitem.load(path_animation, objects=objects, option="replace all", connect=False, currentTime=False)
    cmds.playbackOptions(min= start , max= end, ps=1)
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


def save_rom(path, objects = 'controllers', bake=False):

    if objects == 'controllers':
        try:
            cmds.select('*_ctrl', '*_Ctrl')
        except:
            try:
                cmds.select('*_ctrl')
            except:
                cmds.select('*_Ctrl')

    objects = cmds.ls(selection=True) or []

    start = cmds.playbackOptions(animationStartTime=True, q=True)
    end = cmds.playbackOptions(animationEndTime=True, q=True)

    animitem.save(path, objects=objects, frameRange=(start, end), bakeConnected=bake)
