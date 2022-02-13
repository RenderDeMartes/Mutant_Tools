"""
version: 1.0.0
date: 21/04/2020

#----------------

how to:

import Mutant_Tools
import imp
import Mutant_Tools.Utils.Mocap.Retarget
from Mutant_Tools.Utils.Mocap.Retarget import retarget
imp.reload(Mutant_Tools.Utils.Mocap.Retarget.retarget)

cRetarget = retarget.Retarget()

#get Mocap data
cRetarget.set_timeline(0,25)
cRetarget.set_fps(30)
cRetarget.set_for_mixamo()
mocap_data = cRetarget.get_mocap_data()
cRetarget.save_mocap_data_to_file()

#Apply mocap
cRetarget.set_for_mixamo()
#cRetarget.load_mocap_data_from_file()
cRetarget.mocap_data = mocap_data
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
from pathlib import Path

from  maya import mel
from maya import cmds
import Mutant_Tools
from Mutant_Tools.Utils.Helpers import helpers
imp.reload(Mutant_Tools.Utils.Helpers.helpers)
mh = helpers.Helpers()

#-----------------------------------------------------------------------------------------------

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

#-----------------------------------------------------------------------------------------------

class Retarget(object):

    def __init__(self):

        self.range = [0, 120]
        self.fps = 30

        self.cog_mult = 1

        self.rig_map = self.set_mutant_rig_map() #Mutant Map

        self.mocap_provider_map = None  # Rokoko Map, Mizamo Map, Radical Map, Etc
        self.mocap_data = {} #collected data top retarget
        self.offset_map = None # Rokoko Offset Map, Mizamo Offset Map, Radical Offset Map, Etc

    #----------------------------------------------------------------------------

    def set_mutant_rig_map(self):

        PATH = Path(os.path.dirname(__file__))
        json_data = os.path.join(*PATH.parts[:-1], 'MocapFiles', 'mutant_map.json')

        with open(json_data) as f:
            data = json.load(f)

        self.rig_map = data

        return data

    #----------------------------------------------------------------------------

    def set_timeline(self, min, max):
        cmds.playbackOptions(min= min , max= max, ps=1)
        cmds.playbackOptions(ast= min , aet= max, ps=1)
        self.range = [min, max]

    def set_fps(self, fps = 30):
        cmds.currentUnit(time="{}fps".format(fps))
        self.fps = fps

    #----------------------------------------------------------------------------

    def read_mocap_map(self, file_path = None):
        """ will read json file with mocap data

        Args:
            file_path: path to where the json file is (rembember to use \\ to define the folders)

        Returns: dictionary with data

        """
        if file_path is None:
            path = mh.import_window(extension = ".json")
            path = path[0]

        if not file_path:
            return False

        json_data = os.path.join(file_path)

        with open(json_data) as f:
            data = json.load(f)

        self.mocap_provider_map = data

        return data

    #----------------------------------------------------------------------------

    def read_offset_map(self, file_path = None):
        """ will read json file with mocap data

        Args:
            file_path: path to where the json file is (rembember to use \\ to define the folders)

        Returns: dictionary with data

        """
        if file_path is None:
            path = mh.import_window(extension = ".json")
            path = path[0]

        if not file_path:
            return False

        json_data = file_path
        json_data = os.path.join(json_data)

        with open(json_data) as f:
            data = json.load(f)

        self.offset_map = data

        return data

    #----------------------------------------------------------------------------

    def set_for_mixamo(self):
        self.read_mocap_map(os.path.dirname(__file__).replace('Retarget', 'MocapFiles\\Mixamo\\mixamo_map.json'))
        self.read_offset_map(os.path.dirname(__file__).replace('Retarget', 'MocapFiles\\Mixamo\\mixamo_offset_map.json'))

    def set_for_radical(self):
        self.read_mocap_map(os.path.dirname(__file__).replace('Retarget', 'MocapFiles\\Radical\\radical_map.json'))
        self.read_offset_map(os.path.dirname(__file__).replace('Retarget', 'MocapFiles\\Radical\\radical_offset_map.json'))

    def set_for_rokoko(self):
        self.read_mocap_map(os.path.dirname(__file__).replace('Retarget', 'MocapFiles\\Rokoko\\rokoko_map.json'))
        self.read_offset_map(os.path.dirname(__file__).replace('Retarget', 'MocapFiles\\Rokoko\\rokoko_offset_map.json'))

    #----------------------------------------------------------------------------

    def get_mocap_data(self, provider = None):

        if provider is None:
            provider = self.mocap_provider_map

        if not provider:
            cmds.error("We need to set provider as in attrs or as in self.mocap_provider_map")

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

    def save_mocap_data_to_file(self, mocap_data = None):

        if mocap_data is None:
            mocap_data = self.mocap_data

        path = mh.export_window(extension=".json")
        if not path:
            return
        path = path[0]
        mh.write_json(path, json_file = '', data = mocap_data)

    #----------------------------------------------------------------------------

    def set_ctrls_to_fk(self):
        try:
            cmds.setAttr("L_Ankle_Fk_Ctrl|L_Hip_Jnt_Switch_Loc.Switch_IK_FK", 1)
            cmds.setAttr("R_Ankle_Fk_Ctrl|R_Hip_Jnt_Switch_Loc.Switch_IK_FK", 1)
            cmds.setAttr("L_Wrist_Fk_Ctrl|L_Shoulder_Jnt_Switch_Loc.Switch_IK_FK", 1)
            cmds.setAttr("R_Wrist_Fk_Ctrl|R_Shoulder_Jnt_Switch_Loc.Switch_IK_FK", 1)
        except:
            print('We didnt manage to switch all the ctrls to FK, please do it manually.')

    #----------------------------------------------------------------------------

    def load_mocap_data_from_file(self, path = None):
        if path == None:
            read_path = mh.import_window(extension=".json")[0]
        else:
            read_path = path

        self.mocap_data= mh.read_json(path = read_path, json_file='')

    #----------------------------------------------------------------------------

    def apply_mocap_data(self):

        if not self.mocap_data:
            cmds.error("We need mocap data to work dude!!!")

        self.set_ctrls_to_fk()
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

    #----------------------------------------------------------------------------


