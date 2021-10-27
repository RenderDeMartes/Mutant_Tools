'''
version: 1.0.0
date: 21/04/2020

#----------------

how to:

import Mutant_Tools
import imp
import Mutant_Tools.Utils.Mocap
from Mutant_Tools.Utils.Mocap import retarget
imp.reload(Mutant_Tools.Utils.Mocap.retarget)
#get Mocap data
cRetarget = retarget.Retarget()
cRetarget.set_timeline(0,150)
cRetarget.mocap_provider = retarget.radical_map
mocap_data = cRetarget.get_mocap_data()
#Apply mocap
cRetarget.offset_map=retarget.radical_offset_map
cRetarget.apply_mocap_data()


#----------------
dependencies:

json
pymel
maya mel
maya.cmds

#----------------
licence: https://www.eulatemplate.com/live.php?token=FGISW7ApRfgywum6murbBmLcusKONzkv
author:  Esteban Rodriguez <info@mutanttools.com>

'''

import os
import imp
import json

from  maya import mel
from maya import cmds

#-----------------------------------------------------------------------------------------------

PATH = os.path.dirname(__file__)
PATH = PATH.replace('\\Utils\\Mocap', '//Config')

JSON_FILE = (PATH + '/name_conventions.json')
with open(JSON_FILE) as json_file:
	nc = json.load(json_file)

#-----------------------------------------------------------------------------------------------

retarget_map = {

    'root': '',

    'cog': '',
    'spine_base': '',
    'spine_belly': '',
    'spine_chest': '',

    'neck': '',
    'head': '',

    'l_hip': '',
    'l_knee': '',
    'l_ankle': '',
    'l_ball': '',
    'l_toes': '',

    'r_hip': '',
    'r_knee': '',
    'r_ankle': '',
    'r_ball': '',
    'r_toes': '',

    'l_clavicle': '',
    'r_clavicle': '',

    'l_shoulder': '',
    'l_elbow': '',
    'l_wrist': '',

    'r_shoulder': '',
    'r_elbow': '',
    'r_wrist': ''

}

mutant_map = {

    'root': 'Root',

    'cog': 'COG{}'.format(nc['ctrl']),
    'spine_base': 'Spine_Base_FK{}'.format(nc['ctrl']),
    'spine_belly': 'Spine_Belly_FK{}'.format(nc['ctrl']),
    'spine_chest': 'Spine_Chest{}'.format(nc['ctrl']),

    'neck': 'Neck{}'.format(nc['ctrl']),
    'head': 'Head{}'.format(nc['ctrl']),

    'l_hip': '{}Hip_Fk{}'.format(nc['left'], nc['ctrl']),
    'l_knee': '{}Knee_Fk{}'.format(nc['left'], nc['ctrl']),
    'l_ankle': '{}Ankle_Fk{}'.format(nc['left'], nc['ctrl']),
    'l_ball': '{}Foot_Toes{}'.format(nc['left'], nc['ctrl']),
    'l_toes': '',
    
    'r_hip': '{}Hip_Fk{}'.format(nc['right'], nc['ctrl']),
    'r_knee': '{}Knee_Fk{}'.format(nc['right'], nc['ctrl']),
    'r_ankle': '{}Ankle_Fk{}'.format(nc['right'], nc['ctrl']),
    'r_ball': '{}Foot_Toes{}'.format(nc['right'], nc['ctrl']),
    'r_toes': '',
    
    'l_clavicle': '{}Clavicle{}'.format(nc['left'], nc['ctrl']),
    'r_clavicle': '{}Clavicle{}'.format(nc['right'], nc['ctrl']),

    'l_shoulder': '{}Shoulder_Fk{}'.format(nc['left'], nc['ctrl']),
    'l_elbow': '{}Elbow_Fk{}'.format(nc['left'], nc['ctrl']),
    'l_wrist': '{}Wrist_Fk{}'.format(nc['left'], nc['ctrl']),

    'r_shoulder': '{}Shoulder_Fk{}'.format(nc['right'], nc['ctrl']),
    'r_elbow': '{}Elbow_Fk{}'.format(nc['right'], nc['ctrl']),
    'r_wrist': '{}Wrist_Fk{}'.format(nc['right'], nc['ctrl']),

}

radical_map = {

    'root': 'Root',

    'cog': 'Hips',
    'spine_base': 'Spine',
    'spine_belly': 'Spine1',
    'spine_chest': 'Spine2',

    'neck': 'Neck',
    'head': 'Head',

    'l_hip': 'LeftUpLeg',
    'l_knee': 'LeftLeg',
    'l_ankle': 'LeftFoot',
    'l_ball': 'LeftToeBase',
    'l_toes': 'LeftToeBase_End',

    'r_hip': 'RightUpLeg',
    'r_knee': 'RightLeg',
    'r_ankle': 'RightFoot',
    'r_ball': 'RightToeBase',
    'r_toes': 'RightToeBase_End',

    'l_clavicle': 'LeftShoulder',
    'r_clavicle': 'RightShoulder',

    'l_shoulder': 'LeftArm',
    'l_elbow': 'LeftForeArm',
    'l_wrist': 'LeftHand',

    'r_shoulder': 'RightArm',
    'r_elbow': 'RightForeArm',
    'r_wrist': 'RightHand'
}

rokoko_map = {

    'root': 'Reference',

    'cog': 'Hips',
    'spine_base': 'Spine',
    'spine_belly': 'Spine1',
    'spine_chest': 'Spine3',

    'neck': 'Neck',
    'head': 'Head',

    'l_hip': 'LeftUpLeg',
    'l_knee': 'LeftLeg',
    'l_ankle': 'LeftFoot',
    'l_ball': 'LeftToeBase',
    'l_toes': '',

    'r_hip': 'RightUpLeg',
    'r_knee': 'RightLeg',
    'r_ankle': 'RightFoot',
    'r_ball': 'RightToeBase',
    'r_toes': '',

    'l_clavicle': 'LeftShoulder',
    'r_clavicle': 'RightShoulder',

    'l_shoulder': 'LeftArm',
    'l_elbow': 'LeftForeArm',
    'l_wrist': 'LeftHand',

    'r_shoulder': 'RightArm',
    'r_elbow': 'RightForeArm',
    'r_wrist': 'RightHand'

}

#-----------------------------------------------------------------------------------------------

offset_map = {

    'root': {'offset':[0,0,0], 'connection':['X','Y','Z'], 'mult':[1,1,1]},

    'cog': {'offset':[0,0,0], 'connection':['X','Y','Z'], 'mult':[1,1,1]},
    'spine_base': {'offset':[0,0,0], 'connection':['X','Y','Z'], 'mult':[1,1,1]},
    'spine_belly': {'offset':[0,0,0], 'connection':['X','Y','Z'], 'mult':[1,1,1]},
    'spine_chest': {'offset':[0,0,0], 'connection':['X','Y','Z'], 'mult':[1,1,1]},

    'neck': {'offset':[0,0,0], 'connection':['X','Y','Z'], 'mult':[1,-1,-1]},
    'head': {'offset':[0,0,0], 'connection':['X','Y','Z'], 'mult':[1,-1,-1]},

    'l_hip': {'offset':[0,0,0], 'connection':['X','Y','Z'], 'mult':[1,1,1]},
    'l_knee': {'offset':[0,0,0], 'connection':['X','Y','Z'], 'mult':[1,1,1]},
    'l_ankle': {'offset':[0,0,0], 'connection':['X','Y','Z'], 'mult':[1,1,1]},
    'l_ball': {'offset':[0,0,0], 'connection':['X','Y','Z'], 'mult':[1,1,1]},
    'l_toes': {'offset':[0,0,0], 'connection':['X','Y','Z'], 'mult':[1,1,1]},

    'r_hip': {'offset':[0,0,0], 'connection':['X','Y','Z'], 'mult':[1,1,1]},
    'r_knee':{'offset':[0,0,0], 'connection':['X','Y','Z'], 'mult':[1,1,1]},
    'r_ankle': {'offset':[0,0,0], 'connection':['X','Y','Z'], 'mult':[1,1,1]},
    'r_ball': {'offset':[0,0,0], 'connection':['X','Y','Z'], 'mult':[1,1,1]},
    'r_toes': {'offset':[0,0,0], 'connection':['X','Y','Z'], 'mult':[1,1,1]},

    'l_clavicle': {'offset':[0,0,0], 'connection':['X','Y','Z'], 'mult':[1,1,1]},
    'r_clavicle': {'offset':[0,0,0], 'connection':['X','Y','Z'], 'mult':[1,1,1]},

    'l_shoulder': {'offset':[0,0,0], 'connection':['X','Y','Z'], 'mult':[1,1,1]},
    'l_elbow': {'offset':[0,0,0], 'connection':['X','Y','Z'], 'mult':[1,1,1]},
    'l_wrist': {'offset':[0,0,0], 'connection':['X','Y','Z'], 'mult':[1,1,1]},

    'r_shoulder': {'offset':[0,0,0], 'connection':['X','Y','Z'], 'mult':[1,1,1]},
    'r_elbow': {'offset':[0,0,0], 'connection':['X','Y','Z'], 'mult':[1,1,1]},
    'r_wrist': {'offset':[0,0,0], 'connection':['X','Y','Z'], 'mult':[1,1,1]},

}

radical_offset_map = {

    'root': {'offset':[0,0,0], 'connection':['X','Y','Z'], 'mult':[1,1,1]},

    'cog': {'offset':[0,0,0], 'connection':['X','Y','Z'], 'mult':[1,1,1]},
    'spine_base': {'offset':[0,0,0], 'connection':['Z','Y','X'], 'mult':[-1,1,-1]},
    'spine_belly': {'offset':[0,0,0], 'connection':['Z','Y','X'], 'mult':[-1,1,-1]},
    'spine_chest': {'offset':[0,0,0], 'connection':['Z','Y','X'], 'mult':[-1,1,-1]},

    'neck': {'offset':[0,0,0], 'connection':['X','Y','Z'], 'mult':[1,1,1]},
    'head': {'offset':[0,0,0], 'connection':['X','Y','Z'], 'mult':[1,1,1]},

    'l_hip': {'offset':[0,0,0], 'connection':['X','Y','Z'], 'mult':[1,1,1]},
    'l_knee': {'offset':[0,0,0], 'connection':['X','Y','Z'], 'mult':[1,1,1]},
    'l_ankle': {'offset':[0,0,0], 'connection':['X','Y','Z'], 'mult':[1,1,1]},
    'l_ball': {'offset':[0,0,0], 'connection':['X','Y','Z'], 'mult':[1,1,1]},
    'l_toes': {'offset':[0,0,0], 'connection':['X','Y','Z'], 'mult':[1,1,1]},

    'r_hip': {'offset':[0,0,0], 'connection':['X','Y','Z'], 'mult':[1,1,1]},
    'r_knee':{'offset':[0,0,0], 'connection':['X','Y','Z'], 'mult':[1,1,1]},
    'r_ankle': {'offset':[0,0,0], 'connection':['X','Y','Z'], 'mult':[1,1,1]},
    'r_ball': {'offset':[0,0,0], 'connection':['X','Y','Z'], 'mult':[1,1,1]},
    'r_toes': {'offset':[0,0,0], 'connection':['X','Y','Z'], 'mult':[1,1,1]},

    'l_clavicle': {'offset':[0,0,0], 'connection':['X','Y','Z'], 'mult':[1,-1,-1]},
    'r_clavicle': {'offset':[0,0,0], 'connection':['X','Y','Z'], 'mult':[-1,1,-1]},

    'l_shoulder': {'offset':[0,0,0], 'connection':['X','Y','Z'], 'mult':[1,-1,-1]},
    'l_elbow': {'offset':[0,0,0], 'connection':['X','Y','Z'], 'mult':[1,-1,-1]},
    'l_wrist': {'offset':[0,0,0], 'connection':['X','Y','Z'], 'mult':[1,-1,-1]},

    'r_shoulder': {'offset':[0,0,0], 'connection':['X','Y','Z'], 'mult':[-1,1,-1]},
    'r_elbow': {'offset':[0,0,0], 'connection':['X','Y','Z'], 'mult':[-1,1,-1]},
    'r_wrist': {'offset':[0,0,0], 'connection':['X','Y','Z'], 'mult':[-1,1,-1]},

}

rokoko_offset_map = {

    'root': {'offset':[0,0,0], 'connection':['X','Y','Z'], 'mult':[1,1,1]},

    'cog': {'offset':[0,0,0], 'connection':['X','Y','Z'], 'mult':[1,1,1]},
    'spine_base': {'offset':[0,0,0], 'connection':['X','Y','Z'], 'mult':[1,1,1]},
    'spine_belly': {'offset':[0,0,0], 'connection':['X','Y','Z'], 'mult':[1,1,1]},
    'spine_chest': {'offset':[0,0,0], 'connection':['X','Y','Z'], 'mult':[1,1,1]},

    'neck': {'offset':[0,0,0], 'connection':['X','Y','Z'], 'mult':[1,-1,-1]},
    'head': {'offset':[0,0,0], 'connection':['X','Y','Z'], 'mult':[1,-1,-1]},

    'l_hip': {'offset':[0,0,0], 'connection':['X','Y','Z'], 'mult':[1,1,1]},
    'l_knee': {'offset':[0,0,0], 'connection':['X','Y','Z'], 'mult':[1,1,1]},
    'l_ankle': {'offset':[0,0,0], 'connection':['X','Y','Z'], 'mult':[1,1,1]},
    'l_ball': {'offset':[0,0,0], 'connection':['X','Y','Z'], 'mult':[1,1,1]},
    'l_toes': {'offset':[0,0,0], 'connection':['X','Y','Z'], 'mult':[1,1,1]},

    'r_hip': {'offset':[0,0,0], 'connection':['X','Y','Z'], 'mult':[1,1,1]},
    'r_knee':{'offset':[0,0,0], 'connection':['X','Y','Z'], 'mult':[1,1,1]},
    'r_ankle': {'offset':[0,0,0], 'connection':['X','Y','Z'], 'mult':[1,1,1]},
    'r_ball': {'offset':[0,0,0], 'connection':['X','Y','Z'], 'mult':[1,1,1]},
    'r_toes': {'offset':[0,0,0], 'connection':['X','Y','Z'], 'mult':[1,1,1]},

    'l_clavicle': {'offset':[0,0,0], 'connection':['X','Y','Z'], 'mult':[1,1,1]},
    'r_clavicle': {'offset':[0,0,0], 'connection':['X','Y','Z'], 'mult':[1,1,1]},

    'l_shoulder': {'offset':[0,0,0], 'connection':['X','Y','Z'], 'mult':[1,1,1]},
    'l_elbow': {'offset':[0,0,0], 'connection':['X','Y','Z'], 'mult':[1,1,1]},
    'l_wrist': {'offset':[0,0,0], 'connection':['X','Y','Z'], 'mult':[1,1,1]},

    'r_shoulder': {'offset':[0,0,0], 'connection':['X','Y','Z'], 'mult':[1,1,1]},
    'r_elbow': {'offset':[0,0,0], 'connection':['X','Y','Z'], 'mult':[1,1,1]},
    'r_wrist': {'offset':[0,0,0], 'connection':['X','Y','Z'], 'mult':[1,1,1]},

}


#-----------------------------------------------------------------------------------------------

class Retarget(object):

    def __init__(self):

        self.mocap_provider = None  # Rokoko, Mizamo, Radical, Etc
        self.range = [0, 120]
        self.fps = 30

        self.cog_mult = 1

        self.mocap_data = {}
        self.rig_map = mutant_map
        self.offset_map = None

    #----------------------------------------------------------------------------


    def set_timeline(self, min, max):
        cmds.playbackOptions(min= min , max= max, ps=1)
        cmds.playbackOptions(ast= min , aet= max, ps=1)
        self.range = [min, max]

    def set_fps(self, fps = 30):
        cmds.currentUnit(time='{}fps'.format(fps))
        self.fps = fps

    #----------------------------------------------------------------------------

    def get_mocap_data(self, provider = None):

        if provider is None:
            provider = self.mocap_provider

        if not provider:
            cmds.error('We need to set provider as in attrs or as in self.mocap_provider')

        mocap_data = {}
        for frame in range(self.range[0], self.range[1]+1):
            cmds.currentTime(frame)
            frame_data = {}
            for jnt in provider:
                jnt_data = {}
                mocap_jnt = provider[jnt]
                if not mocap_jnt:
                    continue
                jnt_data['rotateX'] = cmds.getAttr('{}.rotateX'.format(mocap_jnt))
                jnt_data['rotateY'] = cmds.getAttr('{}.rotateY'.format(mocap_jnt))
                jnt_data['rotateZ'] = cmds.getAttr('{}.rotateZ'.format(mocap_jnt))

                jnt_data['translateX'] = cmds.getAttr('{}.translateX'.format(mocap_jnt))
                jnt_data['translateY'] = cmds.getAttr('{}.translateY'.format(mocap_jnt))
                jnt_data['translateZ'] = cmds.getAttr('{}.translateZ'.format(mocap_jnt))

                frame_data[jnt] = jnt_data

            mocap_data[frame] = frame_data
            
        #import pprint
        #pprint.pprint(mocap_data)
        cmds.currentTime(self.range[0])
        self.mocap_data = mocap_data

        return mocap_data

    #----------------------------------------------------------------------------

    def set_ctrls_to_fk(self):
        'TO DO LATER OR MAYBE NEVER DID'

    #----------------------------------------------------------------------------

    def apply_mocap_data(self):

        if not self.mocap_data:
            cmds.error('We need mocap data to work dude!!!')
        
        self.set_fps()
        self.set_timeline(self.range[0], self.range[1])
        rig_map = self.rig_map
        offset_map = self.offset_map

        for frame in range(self.range[0], self.range[1]+1):
            cmds.currentTime(frame)
            frame_data = self.mocap_data[frame]
            for jnt in frame_data:

                jnt_data = frame_data[jnt]
                #import pprint
                #pprint.pprint(jnt_data)

                #get mocap specific data
                mocap_rotX = jnt_data['rotateX']
                mocap_rotY = jnt_data['rotateY']
                mocap_rotZ = jnt_data['rotateZ']
                mocap_transX = jnt_data['translateX']
                mocap_transY = jnt_data['translateY']
                mocap_transZ = jnt_data['translateZ']

                #apply the data with all the offset/mults
                rig_rotX = (mocap_rotX + offset_map[jnt]['offset'][0])*offset_map[jnt]['mult'][0]
                rig_rotY = (mocap_rotY + offset_map[jnt]['offset'][1])*offset_map[jnt]['mult'][1]
                rig_rotZ = (mocap_rotZ + offset_map[jnt]['offset'][2])*offset_map[jnt]['mult'][2]
                rig_transX = mocap_transX*offset_map[jnt]['mult'][0]
                rig_transY = mocap_transY*offset_map[jnt]['mult'][1]
                rig_transZ = mocap_transZ*offset_map[jnt]['mult'][2]

                if rig_map[jnt]:

                    cmds.setAttr("{}.rotate{}".format(rig_map[jnt], offset_map[jnt]['connection'][0]), rig_rotX)
                    cmds.setAttr("{}.rotate{}".format(rig_map[jnt], offset_map[jnt]['connection'][1]), rig_rotY)
                    cmds.setAttr("{}.rotate{}".format(rig_map[jnt], offset_map[jnt]['connection'][2]), rig_rotZ)

                    if jnt == 'cog':
                        if frame == 0:
                            cog_offset = jnt_data['translateY']*self.cog_mult
                        else:
                            if not cog_offset:
                                cog_offset = 0

                        cmds.setAttr("{}.translate{}".format(rig_map[jnt], offset_map[jnt]['connection'][0]), rig_transX)
                        cmds.setAttr("{}.translate{}".format(rig_map[jnt], offset_map[jnt]['connection'][1]), rig_transY - cog_offset)
                        cmds.setAttr("{}.translate{}".format(rig_map[jnt], offset_map[jnt]['connection'][2]), rig_transZ)

                    cmds.select(rig_map[jnt])
                    cmds.setKeyframe()

        cmds.currentTime(self.range[0])