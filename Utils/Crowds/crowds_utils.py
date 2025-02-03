from __future__ import absolute_import
"""
version: 1.0.0
date: 19/07/2022

modified: 25/05/2023

#----------------

how to:

import Mutant_Tools
try:
    import importlib;from importlib import reload
except:
    import imp;from imp import reload

import Mutant_Tools.Utils.Crowds.crowds_utils as crowds_utils
reload(crowds_utils)

cCrowds = crowds_utils.Crowds()

cCrowds.import_crowd_skeleton(skeleton='atoms')
cCrowds.match_crowd_to_rig(crowds_map='atoms_map', rig_map='mutant_map')

cCrowds.transfer_skin_reference(main_geo_grp = 'geo', crowds_map = 'atoms_map', main_joint = 'Hips', remove_reference=False)

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
from maya import cmds, mel
import os
import glob
import json
import pprint
from pathlib import Path
import tempfile

try:
    import importlib;from importlib import reload
except:
    import imp;from imp import reload


import Mutant_Tools
import Mutant_Tools.Utils
from Mutant_Tools.Utils.Rigging import main_mutant
reload(Mutant_Tools.Utils.Rigging.main_mutant)
mt = main_mutant.Mutant()

import Mutant_Tools.Utils.Helpers
from Mutant_Tools.Utils.Helpers import helpers
reload(Mutant_Tools.Utils.Helpers.helpers)
mh = helpers.Helpers()

from Mutant_Tools.Utils.IO import EasySkin
reload(Mutant_Tools.Utils.IO.EasySkin)

from Mutant_Tools.Utils.IO import SkinUtils
reload(Mutant_Tools.Utils.IO.SkinUtils)
cSkin = SkinUtils.Skinning()

nc, curve_data, setup = mt.import_configs()

# -------------------------------------------------------------------

import Mutant_Tools
from Mutant_Tools.Utils.Misc import label_joints
reload(label_joints)

# -------------------------------------------------------------------

# Read name conventions as nc[''] and setup as seup['']
PATH = os.path.dirname(__file__)
PATH = Path(PATH)
PATH_PARTS = PATH.parts[:-2]
FOLDER=''
for f in PATH_PARTS:
	FOLDER = os.path.join(FOLDER, f)


# ------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------

class Crowds(object):

    def __init__(self, crowds_map={}, rig_map={}):
        """ Crowds Class to convert rigs to Crowd agents rigs

        Args:
            crowds_map: dictionary with bone_name -> crowd_bone_name
            rig_map: dictionary with bone_name -> rig_bone_name

        """
        super(Crowds, self).__init__()

        self.crowds_map = crowds_map
        self.rig_map = rig_map

    # ------------------------------------------------------------------------------------------

    def import_crowd_skeleton(self, skeleton='atoms'):
        """

        Args:
            skeleton: string name of desire skeleton to be imported: available: atoms

        Returns: None

        """

        if not skeleton:
            cmds.error('Please choose a skeleton, Example: atoms')

        elif skeleton == 'atoms':
            cmds.file(os.path.join(FOLDER, 'Utils', 'Crowds', 'atoms_skeleton.ma'), i=True)
            label_joints.mass_label_joints()
            remapLabels()

        elif skeleton == 'atoms_toon':
            cmds.file(os.path.join(FOLDER, 'Utils', 'Crowds', 'atoms_toon_skeleton.ma'), i=True)

        if cmds.objExists('scale_reader'):
            cmds.scaleConstraint('scale_reader', 'Hips_Skl')


    # ------------------------------------------------------------------------------------------

    def delete_mutant_build(self):
        if cmds.objExists('Mutant_Build'):
            cmds.delete('Mutant_Build')

    # ------------------------------------------------------------------------------------------


    def match_crowd_to_rig(self, crowds_map=None, rig_map=None):
        """

        Args:
            rig_map: rig_map: dictionary with bone_name -> rig_bone_name
            crowds_map: crowds_map: dictionary with bone_name -> crowd_bone_name

        Returns: None

        """

        if not crowds_map:
            crowds_map = 'atoms_map'

        if not rig_map:
            rig_map = 'mutant_map'

        self.rig_map = mh.read_json(path=os.path.join(FOLDER, 'Utils', 'Crowds'), json_file=rig_map+'.json')
        self.crowds_map = mh.read_json(path=os.path.join(FOLDER, 'Utils', 'Crowds'), json_file=crowds_map+'.json')

        rig_map = self.rig_map
        crowds_map = self.crowds_map

        print('#'*10, 'Crowds_map', '#'*10)
        pprint.pprint(self.crowds_map)
        print('#'*10, 'Rig_Map', '#'*10)
        pprint.pprint(self.rig_map)
        print('#'*25)

        self.delete_mutant_build()

        delete_this = []
        #Point to match
        for name in crowds_map:
            c = crowds_map[name]
            r = rig_map[name]
            print(c, r)
            if not c:
                continue
            #Position
            if cmds.objExists(r):
                print(r,c)
                try:cmds.delete(cmds.pointConstraint(r, c))
                except:pass
                cmds.parentConstraint(r, c, mo=True)
            #Position right
            if r.startswith('L_'):
                rr = r.replace('L_', 'R_')
                rc = c.replace('Left', 'Right')
                print(rc, rr)
                if cmds.objExists(rr):
                    cmds.delete(cmds.pointConstraint(rr, rc))
                    cmds.parentConstraint(rr, rc, mo=True)


    # ------------------------------------------------------------------------------------------

    def transfer_skin_reference(self, main_geo_grp = 'geo', crowds_map = 'atoms_map', main_joint = 'Hips', remove_reference=True):
        """

        Args:
            main_geo_grp: string with name of main geo group to transfet the skinning from

        Returns:

        """

        if not cmds.objExists(main_geo_grp):
            cmds.error('Geo Grp Doesnt Exists')

        #Generate temp files with skinning
        temp_folder = tempfile.gettempdir()
        temp_file = os.path.join(temp_folder, 'TempSkinning.ma')
        #mel.eval('file -force -options "v=0;" -typ "mayaAscii" -pr -es "{};'.format(temp_file))
        cmds.file(temp_file, f=True, type="mayaAscii", pr=True, ea=True)

        #Unbind skin
        cmds.select(main_geo_grp)
        mel.eval('doDetachSkin "2" { "1","1" };')

        #Bind crowd rig
        if not self.crowds_map:
            self.crowds_map = mh.read_json(path=os.path.join(FOLDER, 'Utils', 'Crowds'), json_file=crowds_map+'.json')

        #Skin the geo
        if not main_joint:
            cmds.error('We need a mian joint for skinning')

        for geo in cmds.listRelatives(main_geo_grp, ad=True, type='transform'):
            print('Skinning:',geo)
            try:
                cmds.skinCluster(geo, main_joint, omi=True, normalizeWeights=True, mi=4)
            except:
                pass

        #Reference and transfer skin
        cmds.file(temp_file, ignoreVersion=True, namespace='SkinningRef',
                  mergeNamespacesOnClash=False, r=True)

        for geo in cmds.listRelatives(main_geo_grp, ad=True, type='transform'):
            try:
                cmds.select('SkinningRef:'+geo, geo)
                mel.eval('copySkinWeights  -noMirror -surfaceAssociation closestPoint -influenceAssociation closestJoint;')
            except:
                print('Copy Fail:', geo)

        if remove_reference:
            try:
                fname = cmds.referenceQuery('SkinningRef:Global_Ctrl', filename=True)
            except:
                fname = cmds.referenceQuery('SkinningRef:master_ctrl', filename=True)

            cmds.file(fname, rr=True)

    def transfer_skin_one_to_one(self, crowds_map='atoms_map', rig_map='mutant_map'):

        temp_folder = os.path.join(tempfile.gettempdir(), 'TempSkin')
        if not os.path.exists(temp_folder):
            os.mkdir(temp_folder)

        #Save Skins
        EasySkin.save_all_skins_to(folder_path=temp_folder)

        #Load Skins with diferences of joints names
        skin_files = glob.glob(os.path.join(temp_folder, '*.json'))
        if not skin_files:
            cmds.warning('No Skin Files on Selected Folder')

        for file in skin_files:
            #---------------------------------------------------
            geo = os.path.basename(file).replace('.json', '')
            print(file, geo)

            if not cmds.objExists(geo):
                continue
            print(cmds.nodeType(geo))
            if cmds.nodeType(geo) != 'mesh':
                continue

            #---------------------------------------------------

            # Load File
            skin_data = cSkin.load_data(path=file)
            #pprint.pprint(skin_data)

            #---------------------------------------------------


            #unbind and load new
            cmds.select(geo)
            try:
                mel.eval('doDetachSkin "2" { "1","1" }')
            except:
                pass

            #ReSkin
            print(file)
            self.set_weights_slow_with_replace_names(geo=geo, skin_data=skin_data)

            #Normalize
            cmds.select(geo)
            mel.eval('NormalizeWeights;')

    def set_weights_slow_with_replace_names(self, geo=None, skin_data=None):

        if not geo:
            return False
        if not skin_data:
            return False

        skin = cSkin.get_skin_from_geo(geo)
        if not skin:
            new_inf = []
            for joint in skinning_map:
                new_inf.append(skinning_map[joint])
            skin = cmds.skinCluster(geo, new_inf, tsb=True)[0]

        for geo_name in skin_data:
            data = skin_data[geo_name]
            pprint.pprint(data)
            weigths_data = data['weights']
            for vertex in weigths_data:
                vtx_data = weigths_data[vertex]
                already_used = {}
                for jnt in vtx_data:
                    print('old:', joint, '--->  new:', skinning_map[jnt])
                    paint_value = vtx_data[jnt]
                    print(already_used)
                    print(vtx_data[jnt])
                    if skinning_map[jnt] in already_used:
                        print(already_used[skinning_map[jnt]], vtx_data[jnt])
                        paint_value = already_used[skinning_map[jnt]] + vtx_data[jnt]
                    cmds.skinPercent(skin, "{}.vtx[{}]".format(geo, vertex), r=False, nrm=True, tv=[skinning_map[jnt], paint_value])
                    already_used[skinning_map[jnt]] = paint_value
        # if remove_unused:
        #     self.remove_unused_influences()


    def transfer_skin_labels(self):

        label_joints.mass_label_joints()

        if cmds.objExists('Hips_Skl'):

            crowd_joints_selection = cmds.ls(cmds.listRelatives("Hips_Skl", allDescendents=True), type="joint")
            crowd_joints_selection.append("Hips_Skl")
            cmds.select(crowd_joints_selection)
            label_joints.mass_label_joints()
            cmds.select(cl=True)

            dup_geos = cmds.duplicate('geo', name='crowd_backup_geo')
            SkinUtils.name_transfer_hierarchy_skins(source_parent=['geo'], target_parent=['crowd_backup_geo'], infl_asso="oneToOne", uv_transfer=False)
            
            #cmds.select('geo', hi=True)
            #mel.eval('doDetachSkin "2" { "1","1" }')
            crowd_jnts = remapLabels()
            anti_crowd_jnts=[]
            for i in skinning_map:
                anti_crowd_jnts.append(i)

            ori_geo = cmds.ls('geo', dag=1, type=['mesh'])
            all_ori_mesh = cmds.listRelatives(ori_geo, parent=True, fullPath=True)
            ori_mesh = []

            for mesh in all_ori_mesh:
                if mesh not in ori_mesh:
                    ori_mesh.append(mesh)

            for geo in ori_mesh:
                geo_skinCluster = cmds.ls(cmds.listHistory(geo), type="skinCluster")

                if geo_skinCluster:
                    geo_skinCluster = geo_skinCluster[0]

                    #for geo_skinCluster in cmds.ls(cmds.listHistory(geo), type="skinCluster")[0]:
                        #try:
                    existingjoints = cmds.skinCluster(geo_skinCluster, q=True, inf=True)
                    for jnt in crowd_jnts:
                        if jnt not in existingjoints:
                            cmds.skinCluster(geo_skinCluster, e=True, ai=jnt, lockWeights=False, wt=1.0, fnw=True)

                    existingjoints = cmds.skinCluster(geo_skinCluster, q=True, inf=True)
                    for jnt in anti_crowd_jnts:
                        if jnt in existingjoints:
                            cmds.skinCluster(geo_skinCluster, e=True, ri=jnt)
            



            SkinUtils.name_transfer_hierarchy_skins(source_parent=['crowd_backup_geo'], target_parent=['geo'], uv_transfer=False)
            
            print('Influences transfered to Crowd Skeleton.')
            print('Left a crowd_backup_geo group with original skin weights.')
            print('Please turn off Wire and BSH deformers on the geos to avoid double transforms.')
        else:    
            print('Could not find Hips_Skl as the parent of the crowd skeleton')
            
sides = ['L', 'R']

relabel_mirror_map= {'UpLeg_Skl': ['Pelvis_Bnd', 'Hip_Bnd_0_Bnd', 'Hip_Bnd_1_Bnd', 'Hip_Bnd_2_Bnd', 'Hip_Bnd_3_Bnd'],
                    'Leg_Skl': ['Knee_Bnd_0_Bnd', 'Knee_Bnd_1_Bnd', 'Knee_Bnd_2_Bnd', 'Knee_Bnd_3_Bnd'],
                    'Foot_Skl': ['Foot_Ankle_Bnd'],   
                    'ToeBase_Skl': ['Foot_BallToes_Bnd'],                 
                    'Shoulder_Skl': ['Clavicle_Bnd'],
                    'Arm_Skl':['Shoulder_Bnd_0_Bnd', 'Shoulder_Bnd_1_Bnd'],
                    'Arm_Roll_Skl':['Shoulder_Bnd_2_Bnd', 'Shoulder_Bnd_3_Bnd'],
                    'ForeArm_Skl':['Elbow_Bnd_0_Bnd', 'Elbow_Bnd_1_Bnd'], 
                    'ForeArm_Roll_Skl':['Elbow_Bnd_2_Bnd', 'Elbow_Bnd_3_Bnd'],
                    'Hand_Skl': ['Hand_Palm_Bnd', 'Hand_OutterCup_Bnd', 'Hand_Index_00_Bnd', 
                                'Hand_Middle_00_Bnd', 'Hand_InnerCup_Bnd', 'Hand_Ring_00_Bnd', 
                                'Hand_Pinky_00_Bnd'],
                                             
                    'HandPinky1_Skl':['Hand_Pinky_01_Bnd'],
                    'HandPinky2_Skl':['Hand_Pinky_02_Bnd'],
                    'HandPinky3_Skl':['Hand_Pinky_03_Bnd'],
                    'HandPinky4_Skl':['Hand_Pinky_04_Bnd'],
                    'HandRing1_Skl':['Hand_Ring_01_Bnd'],
                    'HandRing2_Skl':['Hand_Ring_02_Bnd'],
                    'HandRing3_Skl':['Hand_Ring_03_Bnd'],
                    'HandRing4_Skl':['Hand_Ring_04_Bnd'],
                    'HandMiddle1_Skl':['Hand_Middle_01_Bnd'],
                    'HandMiddle2_Skl':['Hand_Middle_02_Bnd'],
                    'HandMiddle3_Skl':['Hand_Middle_03_Bnd'],
                    'HandMiddle4_Skl':['Hand_Middle_04_Bnd'],
                    'HandIndex1_Skl':['Hand_Index_01_Bnd'],
                    'HandIndex2_Skl':['Hand_Index_02_Bnd'],
                    'HandIndex3_Skl':['Hand_Index_03_Bnd'],
                    'HandIndex4_Skl':['Hand_Index_04_Bnd'],
                    'HandThumb1_Skl':['Hand_Thumb_00_Bnd'],
                    'HandThumb2_Skl':['Hand_Thumb_01_Bnd'],
                    'HandThumb3_Skl':['Hand_Thumb_02_Bnd', 'Hand_Thumb_03_Bnd'],
                    'Eye_Skl': ['Eyes_Bnd']
                    } 

relabel_map= {'SpineHolder_Skl': ['Spine_Root_Bnd'], 
                'Hips_Skl': ['Spine_Base_Bnd'], 
                'Spine_Skl': ['Spine_Belly_Bnd'],
                'Spine1_Skl': ['Spine_Chest_Bnd','Spine_End_Bnd'], 
                        
                'Neck_Skl': ['Neck_1_Bnd'], 
                'Neck1_Skl': ['Neck_2_Bnd', 'Neck_3_Bnd'],
                'Head_Skl': ['Head_Bnd'],                             
                }

skinning_map = {

    #'Root': 'Hips_Skl',
    'COG_Bnd': 'Hips_Skl',
    'Spine_Root_Bnd': 'SpineHolder_Skl',
    'Spine_Base_Bnd': 'Hips_Skl',
    'Spine_Belly_Bnd': 'Spine_Skl',
    'Spine_Chest_Bnd': 'Spine1_Skl',
    'Spine_End_Bnd': 'Spine1_Skl',

    'L_Clavicle_Bnd': 'LeftShoulder_Skl',
    'R_Clavicle_Bnd': 'RightShoulder_Skl',

    'L_Shoulder_Bnd_0_Bnd': 'LeftArm_Skl',
    'L_Shoulder_Bnd_1_Bnd': 'LeftArm_Skl',
    'L_Shoulder_Bnd_2_Bnd': 'LeftArm_Roll_Skl',
    'L_Shoulder_Bnd_3_Bnd': 'LeftArm_Roll_Skl',
    'L_Elbow_Bnd_0_Bnd': 'LeftForeArm_Skl',
    'L_Elbow_Bnd_1_Bnd': 'LeftForeArm_Skl',
    'L_Elbow_Bnd_2_Bnd': 'LeftForeArm_Roll_Skl',
    'L_Elbow_Bnd_3_Bnd': 'LeftForeArm_Roll_Skl',
    'R_Shoulder_Bnd_0_Bnd': 'RightArm_Skl',
    'R_Shoulder_Bnd_1_Bnd': 'RightArm_Skl',
    'R_Shoulder_Bnd_2_Bnd': 'RightArm_Roll_Skl',
    'R_Shoulder_Bnd_3_Bnd': 'RightArm_Roll_Skl',
    'R_Elbow_Bnd_0_Bnd': 'RightForeArm_Skl',
    'R_Elbow_Bnd_1_Bnd': 'RightForeArm_Skl',
    'R_Elbow_Bnd_2_Bnd': 'RightForeArm_Roll_Skl',
    'R_Elbow_Bnd_3_Bnd': 'RightForeArm_Roll_Skl',

    'L_Hand_Palm_Bnd': 'LeftHand_Skl',
    'L_Hand_Index_00_Bnd': 'LeftHand_Skl',
    'L_Hand_Index_01_Bnd': 'LeftHandIndex1_Skl',
    'L_Hand_Index_02_Bnd': 'LeftHandIndex2_Skl',
    'L_Hand_Index_03_Bnd': 'LeftHandIndex3_Skl',
    'L_Hand_Index_04_Bnd': 'LeftHandIndex4_Skl',
    'L_Hand_Middle_00_Bnd': 'LeftHand_Skl',
    'L_Hand_Middle_01_Bnd': 'LeftHandMiddle1_Skl',
    'L_Hand_Middle_02_Bnd': 'LeftHandMiddle2_Skl',
    'L_Hand_Middle_03_Bnd': 'LeftHandMiddle3_Skl',
    'L_Hand_Middle_04_Bnd': 'LeftHandMiddle4_Skl',
    'L_Hand_InnerCup_Bnd': 'LeftHand_Skl',
    'L_Hand_Thumb_00_Bnd': 'LeftHandThumb1_Skl',
    'L_Hand_Thumb_01_Bnd': 'LeftHandThumb2_Skl',
    'L_Hand_Thumb_02_Bnd': 'LeftHandThumb3_Skl',
    'L_Hand_Thumb_03_Bnd': 'LeftHandThumb3_Skl',
    'L_Hand_OutterCup_Bnd': 'LeftHand_Skl',
    'L_Hand_Ring_00_Bnd': 'LeftHand_Skl',
    'L_Hand_Ring_01_Bnd': 'LeftHandRing1_Skl',
    'L_Hand_Ring_02_Bnd': 'LeftHandRing2_Skl',
    'L_Hand_Ring_03_Bnd': 'LeftHandRing3_Skl',
    'L_Hand_Ring_04_Bnd': 'LeftHandRing4_Skl',
    'R_Hand_Palm_Bnd': 'RightHand_Skl',
    'R_Hand_Index_00_Bnd': 'RightHand_Skl',
    'R_Hand_Index_01_Bnd': 'RightHandIndex1_Skl',
    'R_Hand_Index_02_Bnd': 'RightHandIndex2_Skl',
    'R_Hand_Index_03_Bnd': 'RightHandIndex3_Skl',
    'R_Hand_Index_04_Bnd': 'RightHandIndex4_Skl',
    'R_Hand_Middle_00_Bnd': 'RightHand_Skl',
    'R_Hand_Middle_01_Bnd': 'RightHandMiddle1_Skl',
    'R_Hand_Middle_02_Bnd': 'RightHandMiddle2_Skl',
    'R_Hand_Middle_03_Bnd': 'RightHandMiddle3_Skl',
    'R_Hand_Middle_04_Bnd': 'RightHandMiddle4_Skl',
    'R_Hand_InnerCup_Bnd': 'RightHand_Skl',
    'R_Hand_Thumb_00_Bnd': 'RightHandThumb1_Skl',
    'R_Hand_Thumb_01_Bnd': 'RightHandThumb2_Skl',
    'R_Hand_Thumb_03_Bnd': 'RightHandThumb3_Skl',
    'R_Hand_Thumb_02_Bnd': 'RightHandThumb3_Skl',
    'R_Hand_OutterCup_Bnd': 'RightHand_Skl',
    'R_Hand_Pinky_00_Bnd': 'RightHand_Skl',
    'R_Hand_Pinky_01_Bnd': 'RightHandPinky1_Skl',
    'R_Hand_Pinky_02_Bnd': 'RightHandPinky2_Skl',
    'R_Hand_Pinky_03_Bnd': 'RightHandPinky3_Skl',
    'R_Hand_Pinky_04_Bnd': 'RightHandPinky4_Skl',
    'R_Hand_Ring_00_Bnd': 'RightHand_Skl',
    'R_Hand_Ring_01_Bnd': 'RightHandRing1_Skl',
    'R_Hand_Ring_02_Bnd': 'RightHandRing2_Skl',
    'R_Hand_Ring_03_Bnd': 'RightHandRing3_Skl',
    'R_Hand_Ring_04_Bnd': 'RightHandRing4_Skl',

    'L_Pelvis_Bnd': 'Hips_Skl',
    'L_Hip_Bnd_0_Bnd': 'LeftUpLeg_Skl',
    'L_Hip_Bnd_1_Bnd': 'LeftUpLeg_Skl',
    'L_Hip_Bnd_2_Bnd': 'LeftUpLeg_Skl',
    'L_Hip_Bnd_3_Bnd': 'LeftUpLeg_Skl',
    'L_Knee_Bnd_0_Bnd': 'LeftLeg_Skl',
    'L_Knee_Bnd_1_Bnd': 'LeftLeg_Skl',
    'L_Knee_Bnd_2_Bnd': 'LeftLeg_Skl',
    'L_Knee_Bnd_3_Bnd': 'LeftLeg_Skl',
    'R_Pelvis_Bnd': 'Hips_Skl',
    'R_Hip_Bnd_0_Bnd': 'RightUpLeg_Skl',
    'R_Hip_Bnd_1_Bnd': 'RightUpLeg_Skl',
    'R_Hip_Bnd_2_Bnd': 'RightUpLeg_Skl',
    'R_Hip_Bnd_3_Bnd': 'RightUpLeg_Skl',
    'R_Knee_Bnd_0_Bnd': 'RightLeg_Skl',
    'R_Knee_Bnd_1_Bnd': 'RightLeg_Skl',
    'R_Knee_Bnd_2_Bnd': 'RightLeg_Skl',
    'R_Knee_Bnd_3_Bnd': 'RightLeg_Skl',

    'L_Foot_Ankle_Bnd': 'LeftFoot_Skl',
    'L_Foot_BallToes_Bnd': 'LeftToeBase_Skl',
    'R_Foot_Ankle_Bnd': 'RightFoot_Skl',
    'R_Foot_BallToes_Bnd': 'RightToeBase_Skl',

    'Neck_1_Bnd': 'Neck_Skl',
    'Neck_2_Bnd': 'Neck1_Skl',
    'Neck_3_Bnd': 'Neck1_Skl',
    'Head_Bnd': 'Head_Skl',
    'L_Eyes_Bnd': 'LeftEye_Skl',
    'R_Eyes_Bnd': 'RightEye_Skl',

}

def remapLabels(relabel_build_mirror_joints=relabel_mirror_map, relabel_build_joints=relabel_map):
    """
    #Description :
        Will change the label on the Mutant build to its destiny Crowd skeleton joint. 

    #Args:
        relabel_build_mirror_joints(dictionary): Origin and Target equivalence of joints that have a left and right build.  
        relabel_build_joints(dictionary): Origin and Target equivalence of joints that do not have a left and right build.  

    # Return: 
        crowd_jnts(list): Joints from the target dictionary 
    """
    crowd_jnts = []
    for source_jnt in relabel_build_joints.keys():
       #print(source_jnt)
       crowd_jnts.append('{source_jnt}'.format(source_jnt=source_jnt))
       for dest_jnt in relabel_build_joints[source_jnt]:
            #print(dest_jnt)
            cmds.setAttr('{}.otherType'.format(dest_jnt), source_jnt, type='string')
       
    for side in sides: 
        #print('L')
        for source_jnt in relabel_build_mirror_joints.keys():
            #print(source_jnt)
            if side == 'L':
                crowd_jnts.append('Left{source_jnt}'.format(side=side,source_jnt=source_jnt))
            else:
                crowd_jnts.append('Right{source_jnt}'.format(side=side,source_jnt=source_jnt))

            for dest_jnt in relabel_build_mirror_joints[source_jnt]:
                #print(dest_jnt)
                cmds.setAttr('{side}_{dest_jnt}.otherType'.format(side=side,dest_jnt=dest_jnt), source_jnt, type='string')
    
    """
    #Fixing weird thumb error exceptions. I don't care.
    cmds.setAttr("L_Hand_Thumb_00_Bnd.otherType", "HandThumb1_Skl", type="string")
    cmds.setAttr("R_Hand_Thumb_00_Bnd.otherType", "HandThumb1_Skl", type="string")
    cmds.setAttr("L_Hand_Thumb_01_Bnd.otherType", "HandThumb2_Skl", type="string")
    cmds.setAttr("R_Hand_Thumb_01_Bnd.otherType", "HandThumb2_Skl", type="string")
    cmds.setAttr("L_Hand_Thumb_02_Bnd.otherType", "HandThumb3_Skl", type="string")
    cmds.setAttr("R_Hand_Thumb_02_Bnd.otherType", "HandThumb3_Skl", type="string")
    cmds.warning("RAN THE HARD CODE FIXESSSSSSSSSSSSSSSSSSSSSSSSSSSSSS")
    """
    

    return crowd_jnts

def mass_label_crowd_joints():
    """
    #Description :
        Label joints based on selection.

    #Instructions:
        Select either the specific joints you wish to label, the group they are under and run script. If nothing is selected
        it will look for Mutant's "Hips_Skl" and label every joint in there; if the group doesn't exist then it will error.

    # Return: None
    """

    ###DEFINING LIST SCENARIOS BASED ON SELECTION###
    bind_joint_sel = cmds.ls(sl=True)

    # Check if selection has only one element.
    if len(bind_joint_sel) == 1:

        ##If element is joint run as normal.
        if cmds.objectType(bind_joint_sel[0]) == "joint":
            bind_joint_sel = cmds.ls(sl=True, type="joint")
            print("List contains one joint.")

        # If element is transform take all children joints.
        elif cmds.objectType(bind_joint_sel[0]) == "transform":
            bind_joint_sel = cmds.listRelatives(bind_joint_sel[0], allDescendents=True, type="joint")
            print("List contains one transform node. Taking all children joints.")

    # Check if selection has more than one element. If yes, take only the joints.
    elif len(bind_joint_sel) > 1:
        bind_joint_sel = cmds.ls(sl=True, type="joint")

    # When nothing is selected look for the mutant "Hips_Skl" and apply it to all it's children.
    else:
        bind_joint_sel = cmds.listRelatives("Hips_Skl", allDescendents=True, type="joint")
        bind_joint_sel.append("Hips_Skl")

    # If the mutant "Bind_Joints_Grp" does not exist then ask for a selection.
    if not bind_joint_sel:
        cmds.error("No Hips_Skl joint chain found. Please select the joints you wish to add labels to.")

    # Setting the naming on the joints.
    for bind_joint in bind_joint_sel:

        # Determining Label side based on initial letter.
        if bind_joint.startswith("Left"):
            cmds.setAttr("{}.side".format(bind_joint), 1)
        elif bind_joint.startswith("Right"):
            cmds.setAttr("{}.side".format(bind_joint), 2)


        # If no letter and no exception as first split, set as center.
        else:
            cmds.setAttr("{}.side".format(bind_joint), 0)

        # Setting type to "Other" for costume name.
        cmds.setAttr("{}.type".format(bind_joint), 18)

        # Determining what name to write in label box.
        if bind_joint.startswith("Left"):
            label_name = bind_joint[4:]

        # Determining what name to write in label box.
        elif bind_joint.startswith("Right"):
            label_name = bind_joint[5:]

        else:
            label_name = bind_joint

            # Setting the label name on the joint
        cmds.setAttr("{}.otherType".format(bind_joint), label_name, type="string")

    cmds.warning("Crowd joints have been labeled without error. Thank you.")