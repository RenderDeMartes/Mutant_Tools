from __future__ import absolute_import
"""
version: 1.0.0
date: 21/04/2020

#----------------

how to:

#Maps are the ones that reads the mocap file for saving
#Offset maps are the one to connect to Mutant Tools, Mixamo offset is the connection between Mixamo and Mutant

import Mutant_Tools
try:
    import importlib;from importlib import reload
except:
    import imp;from imp import reload

import Mutant_Tools.Utils.Mocap.Retarget
from Mutant_Tools.Utils.Mocap.Retarget import retarget
reload(Mutant_Tools.Utils.Mocap.Retarget.retarget)

cRetarget = retarget.Retarget()

#get Mocap data
#Need to set the time line, remove namespaces and create missing items from the mocap maps for saving, example 'group' in mixamo_map
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

#Load Mixamo that have been already created:
cRetarget.mocap_data
cRetarget.load_mixamo_animation(anim_file = 'walking')

#Resotore the rig to non mocap state:
cRetarget.restore_scene()

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
import glob
try:
    import importlib;from importlib import reload
except:
    import imp;from imp import reload

import json
from pathlib import Path

from  maya import mel
from maya import cmds
import Mutant_Tools
from Mutant_Tools.Utils.Helpers import helpers
reload(Mutant_Tools.Utils.Helpers.helpers)
mh = helpers.Helpers()

from Mutant_Tools.Utils.Animation import animation_utils
reload(animation_utils)
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
        self.fps = 24

        self.cog_mult = 1
        self.skip_cog_translate = False

        self.rig_map = self.set_mutant_rig_map() #Mutant Map

        self.mocap_provider_map = None  # Rokoko Map, Mizamo Map, Radical Map, Etc
        self.mocap_data = {} #collected data top retarget
        self.offset_map = None # Rokoko Offset Map, Mizamo Offset Map, Radical Offset Map, Etc

        self.a_pose_fixer = 35

    #----------------------------------------------------------------------------

    def set_mutant_rig_map(self):

        PATH = Path(os.path.dirname(__file__))
        json_data = os.path.join(FOLDER, 'Utils', 'Mocap', 'Retarget', 'Maps', 'mutant_map.json')

        with open(json_data) as f:
            data = json.load(f)

        self.rig_map = data

        return data

    #----------------------------------------------------------------------------

    def set_timeline(self, min, max):
        cmds.playbackOptions(min= min , max= max, ps=1)
        cmds.playbackOptions(ast= min , aet= max, ps=1)
        self.range = [min, max]

    def set_fps(self, fps = 24):
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

        self.read_mocap_map(os.path.join(FOLDER, 'Utils', 'Mocap', 'Retarget', 'Maps', 'mixamo_map.json'))
        self.read_offset_map(os.path.join(FOLDER, 'Utils', 'Mocap', 'Retarget', 'Maps', 'mixamo_offset_map.json'))

    def set_for_radical(self):
        self.read_mocap_map(os.path.join(FOLDER, 'Utils', 'Mocap', 'Retarget', 'Maps', 'radical_map.json'))
        self.read_offset_map(os.path.join(FOLDER, 'Utils', 'Mocap', 'Retarget', 'Maps', 'radical_offset_map.json'))


    def set_for_rokoko(self):
        self.read_mocap_map(os.path.join(FOLDER, 'Utils', 'Mocap', 'Retarget', 'Maps', 'rokoko_map.json'))
        self.read_offset_map(os.path.join(FOLDER, 'Utils', 'Mocap', 'Retarget', 'Maps', 'rokoko_offset_map.json'))


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

    def save_mocap_data_to_file(self, path=None, mocap_data = None):

        if mocap_data is None:
            mocap_data = self.mocap_data

        if not path:
            path = mh.export_window(extension=".json")
        if not path:
            return
        path = os.path.join(path[0])

        with open(path, 'w') as f:
            json.dump(mocap_data, f, ensure_ascii=False, indent=4)

        print('Saved: {}'.format(path))

    #----------------------------------------------------------------------------

    def set_ctrls_to_fk(self):
        try:
            cmds.setAttr("L_Ankle_Fk_Ctrl|L_Hip_Jnt_Switch_Loc.Switch_IK_FK", 1)
            cmds.setAttr("R_Ankle_Fk_Ctrl|R_Hip_Jnt_Switch_Loc.Switch_IK_FK", 1)
            cmds.setAttr("L_Wrist_Fk_Ctrl|L_Shoulder_Jnt_Switch_Loc.Switch_IK_FK", 1)
            cmds.setAttr("R_Wrist_Fk_Ctrl|R_Shoulder_Jnt_Switch_Loc.Switch_IK_FK", 1)
            cmds.setAttr("Head_Ctrl|Neck_Attrs_Loc.HeadSpace", 2)
            cmds.setAttr("L_ElbowMid_Bendy_Ctrl|L_Shoulder_Jnt_Switch_Loc.FK_Arms", 2)
            cmds.setAttr("R_ElbowMid_Bendy_Ctrl|R_Shoulder_Jnt_Switch_Loc.FK_Arms", 2)
            cmds.setAttr("R_KneeMid_Bendy_Ctrl|R_Hip_Jnt_Switch_Loc.FK_Arms", 2)
            cmds.setAttr("L_KneeMid_Bendy_Ctrl|L_Hip_Jnt_Switch_Loc.FK_Arms", 2)
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
        self.set_timeline(self.range[0], self.range[1])

        print('Range:', self.range)

        rig_map = self.rig_map
        offset_map = self.offset_map

        for frame in range(self.range[0], self.range[1]+1):
            cmds.currentTime(frame)
            try:frame_data = self.mocap_data[str(frame)]
            except:continue
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

                    a_pose_fixer = self.a_pose_fixer
                    if jnt == "l_clavicle" or jnt == "r_clavicle":
                        new_value = cmds.getAttr("{}.rotate{}".format(rig_map[jnt], offset_map[jnt]["connection"][0])) + a_pose_fixer
                        cmds.setAttr("{}.rotate{}".format(rig_map[jnt], offset_map[jnt]["connection"][0]), new_value)

                    if jnt == "cog":
                        if frame == 0:
                            cog_offset = jnt_data["translateY"]*self.cog_mult
                        else:
                            if not cog_offset:
                                cog_offset = 0

                        if self.skip_cog_translate:
                             continue

                        cmds.setAttr("{}.translate{}".format(rig_map[jnt], offset_map[jnt]["connection"][0]), rig_transX)
                        cmds.setAttr("{}.translate{}".format(rig_map[jnt], offset_map[jnt]["connection"][1]), rig_transY - cog_offset)
                        cmds.setAttr("{}.translate{}".format(rig_map[jnt], offset_map[jnt]["connection"][2]), rig_transZ)

                    cmds.select(rig_map[jnt])
                    cmds.setKeyframe()

        cmds.currentTime(self.range[0])

    #----------------------------------------------------------------------------

    def load_mixamo_animation(self, anim_file = 'walking'):

        try:
            self.restore_scene()
        except:
            pass

        self.set_for_mixamo()

        anim_path = os.path.join(FOLDER, 'Utils','Mocap','MocapFiles','Mixamo')
        self.mocap_data= mh.read_json(path = anim_path, json_file=anim_file+'.json')

        # import pprint
        # pprint.pprint(self.mocap_data)

        frames = []
        for frame in self.mocap_data:
            frames.append(int(frame))
        frames.sort()

        self.range = [frames[0], frames[-1]]
        self.set_timeline(frames[0], frames[-1]+1)

        self.apply_mocap_data()

    #----------------------------------------------------------------------------

    def restore_scene(self):
        try:
            cmds.setAttr("L_Ankle_Fk_Ctrl|L_Hip_Jnt_Switch_Loc.Switch_IK_FK", 0)
            cmds.setAttr("R_Ankle_Fk_Ctrl|R_Hip_Jnt_Switch_Loc.Switch_IK_FK", 0)
            cmds.setAttr("L_Wrist_Fk_Ctrl|L_Shoulder_Jnt_Switch_Loc.Switch_IK_FK", 0)
            cmds.setAttr("R_Wrist_Fk_Ctrl|R_Shoulder_Jnt_Switch_Loc.Switch_IK_FK", 0)
            cmds.setAttr("Head_Ctrl|Neck_Attrs_Loc.HeadSpace", 0)
            cmds.setAttr("L_ElbowMid_Bendy_Ctrl|L_Shoulder_Jnt_Switch_Loc.FK_Arms", 0)
            cmds.setAttr("R_ElbowMid_Bendy_Ctrl|R_Shoulder_Jnt_Switch_Loc.FK_Arms", 0)
            cmds.setAttr("R_KneeMid_Bendy_Ctrl|R_Hip_Jnt_Switch_Loc.FK_Arms", 0)
            cmds.setAttr("L_KneeMid_Bendy_Ctrl|L_Hip_Jnt_Switch_Loc.FK_Arms", 0)
        except:
            print('We didnt manage to retore the scene please do it manually.')

        ctrls = cmds.ls('*_Ctrl')

        animation_utils.delete_keys()

        attrs = ['translateX','translateY','translateZ','rotateX','rotateY','rotateZ','scaleX','scaleY','ScaleZ']
        for ctrl in ctrls:
            for attr in attrs:
                value = 0
                if 'scale' in attr:
                    value=1
                try:
                    cmds.setAttr('{}.{}'.format(ctrl, attr), value)
                except:
                    pass

    #----------------------------------------------------------------------------

    def batch_save(self, origin_folder, destination_folder, set_for = 'mixamo'):

        cmds.file(new=True, f=True)

        if set_for == 'mixamo':
            self.set_for_mixamo()

        mocap_files = glob.glob(os.path.join(origin_folder, '*'))
        print(mocap_files)

        for mocap_file in mocap_files:
            cmds.file(new=True, f=True)

            print(mocap_file)

            name = mocap_file.replace(origin_folder, '').replace('\\', '').replace('.fbx', '').replace(' ', '_').lower()
            print(name)

            #Open mocap file and clean it
            cmds.file(mocap_file, i=True, type='FBX')
            cmds.select(all=True, hi=True)
            cmds.snapKey()
            cmds.snapKey()

            self.delete_name_spaces()

            cmds.group('Hips', n='group')

            #Get all Keys
            obj = "Hips"  # Object to check animation range with.
            all_keys = sorted(cmds.keyframe(obj, q=True) or [])  # Get all the keys and sort them by order. We use `or []` in-case it has no keys, which will use an empty list instead so it doesn't crash `sort`.
            if all_keys:  # Check to see if it at least has one key.
                print(all_keys[0], all_keys[-1])

            self.range = [int(all_keys[0]), int(all_keys[-1])]
            self.set_timeline(int(all_keys[0]), int(all_keys[-1]))
            self.set_fps(24)
            mocap_data = self.get_mocap_data()

            #self.save_mocap_data_to_file(path=os.path.join(destination_folder, name+'.json'), mocap_data=mocap_data)
            with open(os.path.join(destination_folder, name+'.json'), 'w') as f:
                json.dump(mocap_data, f, ensure_ascii=False, indent=4)

            print(os.path.join(destination_folder, name+'.json'))

    #----------------------------------------------------------------------------

    def delete_name_spaces(self):
        # Set root namespace
        cmds.namespace(setNamespace=':')

        # Collect all namespaces except for the Maya built ins.
        all_namespaces = [x for x in cmds.namespaceInfo(listOnlyNamespaces=True, recurse=True) if
                          x != "UI" and x != "shared"]

        if all_namespaces:
            # Sort by hierarchy, deepest first.
            all_namespaces.sort(key=len, reverse=True)
            for namespace in all_namespaces:
                # When a deep namespace is removed, it also removes the root. So check here to see if these still exist.
                if cmds.namespace(exists=namespace) is True:
                    cmds.namespace(removeNamespace=namespace, mergeNamespaceWithRoot=True)

    #----------------------------------------------------------------------------
