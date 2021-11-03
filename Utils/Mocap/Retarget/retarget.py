"""
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
cRetarget.offset_map=retarget.radical_offset_map.json
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

"""

import os
import imp
import json

from  maya import mel
from maya import cmds

#-----------------------------------------------------------------------------------------------

PATH = os.path.dirname(__file__)
PATH = PATH.replace("\\Utils\\Mocap", "//Config")

JSON_FILE = (PATH + "/name_conventions.json")
with open(JSON_FILE) as json_file:
	nc = json.load(json_file)

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
        cmds.currentUnit(time="{}fps".format(fps))
        self.fps = fps

    #----------------------------------------------------------------------------

    def get_mocap_data(self, provider = None):

        if provider is None:
            provider = self.mocap_provider

        if not provider:
            cmds.error("We need to set provider as in attrs or as in self.mocap_provider")

        mocap_data = {}
        for frame in range(self.range[0], self.range[1]+1):
            cmds.currentTime(frame)
            frame_data = {}
            for jnt in provider:
                jnt_data = {}
                mocap_jnt = provider[jnt]
                if not mocap_jnt:
                    continue
                jnt_data["rotateX"] = cmds.getAttr("{}.rotateX".format(mocap_jnt))
                jnt_data["rotateY"] = cmds.getAttr("{}.rotateY".format(mocap_jnt))
                jnt_data["rotateZ"] = cmds.getAttr("{}.rotateZ".format(mocap_jnt))

                jnt_data["translateX"] = cmds.getAttr("{}.translateX".format(mocap_jnt))
                jnt_data["translateY"] = cmds.getAttr("{}.translateY".format(mocap_jnt))
                jnt_data["translateZ"] = cmds.getAttr("{}.translateZ".format(mocap_jnt))

                frame_data[jnt] = jnt_data

            mocap_data[frame] = frame_data
            
        #import pprint
        #pprint.pprint(mocap_data)
        cmds.currentTime(self.range[0])
        self.mocap_data = mocap_data

        return mocap_data

    #----------------------------------------------------------------------------

    def set_ctrls_to_fk(self):
        "TO DO LATER OR MAYBE NEVER DID"

    #----------------------------------------------------------------------------

    def apply_mocap_data(self):

        if not self.mocap_data:
            cmds.error("We need mocap data to work dude!!!")
        
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
                mocap_rotX = jnt_data["rotateX"]
                mocap_rotY = jnt_data["rotateY"]
                mocap_rotZ = jnt_data["rotateZ"]
                mocap_transX = jnt_data["translateX"]
                mocap_transY = jnt_data["translateY"]
                mocap_transZ = jnt_data["translateZ"]

                #apply the data with all the offset/mults
                rig_rotX = (mocap_rotX + offset_map[jnt]["offset"][0])*offset_map[jnt]["mult"][0]
                rig_rotY = (mocap_rotY + offset_map[jnt]["offset"][1])*offset_map[jnt]["mult"][1]
                rig_rotZ = (mocap_rotZ + offset_map[jnt]["offset"][2])*offset_map[jnt]["mult"][2]
                rig_transX = mocap_transX*offset_map[jnt]["mult"][0]
                rig_transY = mocap_transY*offset_map[jnt]["mult"][1]
                rig_transZ = mocap_transZ*offset_map[jnt]["mult"][2]

                if rig_map[jnt]:

                    cmds.setAttr("{}.rotate{}".format(rig_map[jnt], offset_map[jnt]["connection"][0]), rig_rotX)
                    cmds.setAttr("{}.rotate{}".format(rig_map[jnt], offset_map[jnt]["connection"][1]), rig_rotY)
                    cmds.setAttr("{}.rotate{}".format(rig_map[jnt], offset_map[jnt]["connection"][2]), rig_rotZ)

                    if jnt == "cog":
                        if frame == 0:
                            cog_offset = jnt_data["translateY"]*self.cog_mult
                        else:
                            if not cog_offset:
                                cog_offset = 0

                        cmds.setAttr("{}.translate{}".format(rig_map[jnt], offset_map[jnt]["connection"][0]), rig_transX)
                        cmds.setAttr("{}.translate{}".format(rig_map[jnt], offset_map[jnt]["connection"][1]), rig_transY - cog_offset)
                        cmds.setAttr("{}.translate{}".format(rig_map[jnt], offset_map[jnt]["connection"][2]), rig_transZ)

                    cmds.select(rig_map[jnt])
                    cmds.setKeyframe()

        cmds.currentTime(self.range[0])