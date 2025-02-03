from __future__ import absolute_import
"""
#Usefull links:
https://github.com/EpicGames/MetaHuman-DNA-Calibration/tree/main
https://dev.epicgames.com/community/learning/tutorials/EoPj/metahuman-dna-calibration-deep-dive
https://forums.unrealengine.com/t/how-to-use-metahuman-facial-control-rig-inside-ue5-with-another-mesh-that-has-same-joints/1177281/2

#Require steps:
#DNA files: C:\\Users\\rodri\\Documents\\maya\\2024\\scripts\\rigging\\Mutant_Tools\\Utils\\MetaHuman\\dna_calibration\\data\\dna_files\\Taro.dna
#C:/Users/rodri/Documents/maya/2024/scripts/rigging/Mutant_Tools/Utils/MetaHuman/dna_calibration/data/dna_files
#Node name: rl4Embedded_*

import Mutant_Tools
from Mutant_Tools.Utils.Unreal.MetaHuman import meta_mutant
reload(meta_mutant)


cMeta_Mutant = meta_mutant.Meta_Mutant()

#Create template metahuman rig
cMeta_Mutant.create_simple_metahuman()

FACIAL_C_TeethUpper
FACIAL_C_TeethLower

FACIAL_C_Tongue1

FACIAL_R_EyeParallel
FACIAL_L_EyeParallel

#-------------------------------------------
 
import Mutant_Tools
from Mutant_Tools.Utils.MetaHuman import meta_mutant
reload(meta_mutant)

cMeta_Mutant = meta_mutant.Meta_Mutant()
#cMeta_Mutant.view_dna()

#Create template metahuman rig
#cMeta_Mutant.create_simple_metahuman()

cMeta_Mutant.create_custom_metahuman(new_geo='C:\\Users\\rodri\\Documents\\maya\\projects\\default\\scenes\\Carolyn\\Wrapped_Head.obj')


#-------------------------------------------

import Mutant_Tools
from Mutant_Tools.Utils.Unreal.MetaHuman import meta_mutant
reload(meta_mutant)

cMeta_Mutant = meta_mutant.Meta_Mutant()
cMeta_Mutant.save_current_pose_to_json('left_lip_dw')


"""
import os
import json
from maya import cmds, mel
from os import makedirs
from sys import platform
from pathlib import Path
from math import isclose
from os import path as ospath
from sys import path as syspath

try:
    import importlib;from importlib import reload
except:
    import imp;from imp import reload

import Mutant_Tools.Utils.Wrap
from Mutant_Tools.Utils.Wrap import wrap_utils
import imp
imp.reload(wrap_utils)
cWrap = wrap_utils.Wrap3D()

from Mutant_Tools.Utils.Wrap.Skeletor import Skeletor
reload(Skeletor)
cSkeletor = Skeletor.Skeletor()

#Unreal MetaHuman Weird Imports

ROOT_DIR = os.path.join(os.path.dirname(__file__), 'dna_calibration')
#ROOT_DIR = 'C:\\dna_calibration'
print('ROOT:', ROOT_DIR )


MAYA_VERSION = "2022"  # or 2023
ROOT_LIB_DIR = f"{ROOT_DIR}/lib/Maya{MAYA_VERSION}"
if platform == "win32":
    LIB_DIR = f"{ROOT_LIB_DIR}/windows"
elif platform == "linux":
    LIB_DIR = f"{ROOT_LIB_DIR}/linux"
else:
    raise OSError(
        "OS not supported, please compile dependencies and add value to LIB_DIR"
    )

# Adds directories to path
syspath.insert(0, ROOT_DIR)
syspath.insert(0, LIB_DIR)

# Define the new path you want to add
new_path = os.path.join(ospath.dirname(ospath.abspath(__file__)), 'dna_calibration')

# Get the current MAYA_MODULE_PATH
maya_module_path = os.getenv('MAYA_MODULE_PATH', '')

# Append the new path to the existing MAYA_MODULE_PATH
if maya_module_path:
    updated_path = maya_module_path + os.pathsep + new_path
else:
    updated_path = new_path

# Set the updated MAYA_MODULE_PATH
os.environ['MAYA_MODULE_PATH'] = updated_path

#--------------------------------------------------------------------
#--------------------------------------------------------------------
#--------------------------------------------------------------------

how_to_use = """
Will only work on Maya 2022
Check if pymel is installed: import pymel.core as pm

Install Quixel Bridge App
Download MetaHuman-DNA-Calibration-main from GitHub
Create an empty folder in C: called dna_calibration
Put contents from MetaHuman-DNA-Calibration-main into C:/dna_calibration

Check if exists or create a folder in: C:/Users/user/Documents/maya/2022/ called plug-ins
Put embeddedRL4.mll in C:/Users/user/Documents/maya/2022/plug-ins

Enable embeddedRL4.mll and restart Maya     
"""

try:
    from dna import DataLayer_All, FileStream, Status, BinaryStreamReader, BinaryStreamWriter
    from dnacalib import (
        DNACalibDNAReader,
        SetVertexPositionsCommand,
        VectorOperation_Subtract,
        CalculateMeshLowerLODsCommand
    )
    import maya.OpenMaya as om
    from dna_viewer import (
        DNA,
        Config,
        RigConfig,
        build_meshes,
        build_rig,
        get_skin_weights_from_scene,
        set_skin_weights_to_scene
    )
    from dnacalib import (
        CommandSequence,
        DNACalibDNAReader,
        RenameJointCommand,
        ScaleCommand,
        SetBlendShapeTargetDeltasCommand,
        SetVertexPositionsCommand,
        CalculateMeshLowerLODsCommand,
        VectorOperation_Add,
        VectorOperation_Interpolate,
        SetNeutralJointTranslationsCommand,
        SetNeutralJointRotationsCommand,
        SetLODsCommand,
        TranslateCommand,
        SetSkinWeightsCommand,
        RemoveJointCommand,
        RotateCommand
    )

    from dna import (
        BinaryStreamReader,
        BinaryStreamWriter,
        JSONStreamWriter,
        DataLayer_All,
        DataLayer_Behavior,
        FileStream,
        Status,
    )
except:
    cmds.warning(how_to_use)

def load_embeddedRL4():
    """
    Loads the embeddedRL4 plugin based on the Maya version.

    Raises:
        Exception: If the Maya version is unsupported.
    """
    # Determine the Maya version
    maya_version = cmds.about(version=True)

    # Define the plugin path based on the Maya version
    if maya_version.startswith("2022"):
        plugin_path = os.path.join(ROOT_DIR, "lib", "Maya2022", "windows", "embeddedRL4.mll")
    elif maya_version.startswith("2023"):
        plugin_path = os.path.join(ROOT_DIR, "lib", "Maya2023", "windows", "embeddedRL4.mll")
    else:
        raise Exception(f"Unsupported Maya version: {maya_version}")

    # Load the plugin
    cmds.loadPlugin(plugin_path)

def view_dna():
    """
    Displays the DNA Viewer.
    """
    import dna_viewer
    dna_viewer.show()

def ensure_path_exists(path):
    """
    Ensures that the specified path exists by creating it if necessary.

    Args:
        path (str): The directory path to check or create.

    Returns:
        str: The verified or created path.
    """
    if not os.path.exists(path):
        os.makedirs(path)
    return path

class Meta_Mutant(object):
    """
    A class used to manage Meta Mutant configurations and operations.
    """
    def __init__(self):
        """
        Initializes the Meta_Mutant class by checking installation status and
        setting up necessary directories.
        """
        self.check_installation_status()
        self.load_needed_plugins()

        self.meta_mutant_folder = self.initialize_meta_mutant_folder()
        print(self.meta_mutant_folder)

        self.ROOT_DIR = ROOT_DIR
        self.CHARACTER_NAME = 'Taro'
        self.CHARACTER_DNA = os.path.join(ROOT_DIR, 'data', 'dna_files', f'{self.CHARACTER_NAME}.dna')
        self.ANALOG_GUI = os.path.join(ROOT_DIR, 'data', 'analog_gui.ma')
        self.GUI = os.path.join(ROOT_DIR, 'data', 'gui.ma')
        self.ADDITIONAL_ASSEMBLE_SCRIPT = os.path.join(ROOT_DIR, 'data', 'additional_assemble_script.py')

        self.character_folder = os.path.join(self.meta_mutant_folder, self.CHARACTER_NAME)

        self.meta_data = self.get_pose_metadata()

    def get_pose_metadata(self):
        script_dir = os.path.dirname(os.path.realpath(__file__))
        json_file_path = os.path.join(script_dir, 'meta_poses.json')

        # Read old poses
        meta_data = self.read_json(json_file_path)
        return meta_data

    def check_installation_status(self):
        """
        Checks if the required installations and configurations are in place.
        Provides instructions if they are missing.
        """

        try:
            import dna_viewer
            import dnacalib
        except ImportError:
            print(how_to_use)

    def create_simple_metahuman(self, character_name=None, dna_path=None):
        """
        Creates a simple MetaHuman rig using the DNA viewer and configuration.
        """
        from dna_viewer import DNA, RigConfig, build_rig
        if not character_name:
            CHARACTER_NAME = self.CHARACTER_NAME
            CHARACTER_DNA = self.CHARACTER_DNA
        else:
            CHARACTER_NAME = character_name
            CHARACTER_DNA = os.path.join(ROOT_DIR, 'data', 'dna_files', f'{character_name}.dna')

        if dna_path:
            CHARACTER_DNA = dna_path

        ANALOG_GUI = self.ANALOG_GUI
        GUI = self.GUI
        ADDITIONAL_ASSEMBLE_SCRIPT = self.ADDITIONAL_ASSEMBLE_SCRIPT

        dna = DNA(CHARACTER_DNA)

        config = RigConfig(
            gui_path=GUI,
            analog_gui_path=ANALOG_GUI,
            aas_path=ADDITIONAL_ASSEMBLE_SCRIPT,
        )

        # Creates the rig
        build_rig(dna=dna, config=config)

    def view_dna(self):
        """
        Displays the DNA Viewer.
        """
        view_dna()

    def initialize_meta_mutant_folder(self):
        """
        Initializes the Meta Mutant folder in the Maya scripts directory.

        Returns:
            str: The path to the Meta Mutant folder.
        """
        scripts_path = os.path.join(cmds.internalVar(usd=True), 'Meta_Mutant')
        ensure_path_exists(scripts_path)
        return scripts_path

    def read_dna(self, path):
        read_dna()

    def save_dna(self, reader, path):
        save_dna()
        
    def get_rl4_node(self):
        rl4_nodes = cmds.ls(type='embeddedNodeRL4')
        #Asumes only one exists in the scene
        if not rl4_nodes:
            cmds.error('Not a single embeddedNodeRL4 was found!')
        if len(rl4_nodes)>1:
            cmds.warning('Multiple embeddedNodeRL4 nodes were found, using only first one found...')
        return rl4_nodes[0]

    def get_dna_in_scene(self):
        node = self.get_rl4_node()
        dna = cmds.getAttr(f'{node}.dnaFilePath')
        if os.path.isfile(dna):
            return dna
        else:
            cmds.error('DNA File Doesnt Exists!')

    def load_needed_plugins(self):
        cmds.loadPlugin("nearestPointOnMesh.mll")
        cmds.loadPlugin("fbxmaya.mll")
        try:
            load_embeddedRL4()
        except:
            cmds.warning(how_to_use)

    def create_custom_metahuman(self, new_geo=None, use_skeletor=True, custom_data={}, custom_data_positions={}):

        print(custom_data)
        print(custom_data_positions)

        if not new_geo:
            cmds.error('We need a new geo to do the stuff...')


        WORK_DIR = self.meta_mutant_folder
        output_dir = os.path.join(self.character_folder, 'output')
        temp_dir = os.path.join(self.character_folder, 'temp')
        joint_position_file = f"{temp_dir}/joint_position.json"

        # Create folders
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)

        # Step 1: Read DNA and build scene
        show_meshes(self.CHARACTER_DNA)
        reader = read_dna(self.CHARACTER_DNA)
        calibrated = DNACalibDNAReader(reader)



        #Surface_joints is assing down in og scripts
        surface_joints = cmds.listRelatives('spine_04', ad=True, type='joint')

        # ----------------------------------------
        cmds.ls(surface_joints)
        block_order = cWrap.get_order_of_blocks(use_selection=True)
        hierarchy_array = Skeletor.unparent_hierarchy(surface_joints)
        # ----------------------------------------

        find_and_save_joint_positions_in_file(reader, surface_joints, joint_position_file)

        # ----------------------------------------
        Skeletor.parent_hierarchy(hierarchy_array)
        cWrap.reorder_block_guides(block_order)
        # ----------------------------------------

        #Import new head to scene
        # Consts
        up_axis = "y"
        head_mesh = "head_lod0_mesh"
        facial_root_joints = ["FACIAL_C_FacialRoot", "FACIAL_C_Neck1Root", "FACIAL_C_Neck2Root"]
        neck_joints = ["head", "neck_01", "neck_02"]
        root_joint = "spine_04"
        add_vtx_color = False
        fbx_root = "root"
        character_name = "Ada"

        # In-between DNA paths
        mesh_dna_folder = os.path.join(self.character_folder, 'dna')
        ensure_path_exists(mesh_dna_folder)
        mesh_dna = os.path.join(mesh_dna_folder, f"{self.CHARACTER_NAME}_mesh.dna")
        jnt_dna = os.path.join(mesh_dna_folder, f"{self.CHARACTER_NAME}_jnt.dna")


        #Import New Geo
        cmds.file(new_geo, i=True, mergeNamespacesOnClash=True, namespace=":")
        cmds.makeIdentity('transf0', s = True, t = True, r = True, a = True)

        #Save positions
        run_vertices_command(
            calibrated, get_mesh_vertex_positions_from_scene(head_mesh),
            get_mesh_vertex_positions_from_scene("transf0"), 0
        )

        save_dna(calibrated, mesh_dna)

        #Update Joints - Snap to vertices
        show_meshes(mesh_dna) #Shoulde be new geo with bad joints pos

        #This will make joints snap into correct pos
        if not use_skeletor:
            # ----------------------------------------
            cmds.ls(surface_joints)
            block_order = cWrap.get_order_of_blocks(use_selection=True)
            hierarchy_array = Skeletor.unparent_hierarchy(surface_joints)
            # ----------------------------------------

            jnt_data = {}
            with open(joint_position_file) as jnt_file:
                jnt_data = json.load(jnt_file)

            for jnt_name, vertex_id in jnt_data.items():
                vtx_position = cmds.xform(f"{head_mesh}.vtx[{vertex_id}]", q=True, worldSpace=True, t=True)
                cmds.xform(jnt_name, ws=True, translation=vtx_position)

            # ----------------------------------------
            Skeletor.parent_hierarchy(hierarchy_array)
            cWrap.reorder_block_guides(block_order)
            #----------------------------------------

        else:
            cmds.ls(surface_joints)
            block_order = cWrap.get_order_of_blocks(use_selection=True)
            cmds.rename('head_lod0_mesh', 'transf0')

            #skeletor_file = os.path.join(os.path.dirname(__file__), 'meta_components', 'transf0.skeletor')
            cSkeletor.dirpath = os.path.join(os.path.dirname(__file__), 'meta_components')
            node_array = cSkeletor.load_data(mesh='transf0', dirpath=cSkeletor.dirpath)
            cSkeletor.place_all(mesh='transf0', node_Array=node_array)

            cWrap.reorder_block_guides(block_order)

            cmds.rename('transf0', 'head_lod0_mesh')

        self.meta_joint_custom_placement(surface_joints=surface_joints, positions=custom_data_positions)

        reader = read_dna(mesh_dna)
        calibrated = DNACalibDNAReader(reader)
        run_joints_command(reader, calibrated)

        # Save DNA with correct joints position
        save_dna(calibrated, jnt_dna)

        # Final DNA
        final_dna =os.path.join(mesh_dna_folder, f"{self.CHARACTER_NAME}_final.dna")
        rotated_dna = os.path.join(mesh_dna_folder ,f"{self.CHARACTER_NAME}_final.rotated.dna")

        # Step 4: Change anim setup
        reader = read_dna(jnt_dna)

        stream = FileStream(final_dna, FileStream.AccessMode_Write, FileStream.OpenMode_Binary)
        writer = BinaryStreamWriter(stream)
        writer.setFrom(reader)

        new_lods = [2, 3, 4]
        anim_lods = reader.getAnimatedMapLODs()
        for lod in new_lods:
            writer.setLODAnimatedMapMapping(lod, 0)
            anim_lods[lod] = anim_lods[0]

        writer.setAnimatedMapLODs(anim_lods)
        writer.write()
        if not Status.isOk():
            status = Status.get()
            raise RuntimeError(f"Error saving DNA: {status.message}")

        #check Final Result
        assemble_scene(final_dna, self.ANALOG_GUI, self.GUI, self.ADDITIONAL_ASSEMBLE_SCRIPT)

        #clean a bit
        self.clean_build()

    def clean_build(self):
        for grp in cmds.listRelatives('geometry_grp', c=True):
            if '0' in grp:
                continue
            cmds.setAttr(f'{grp}.v', 0)

        for geo in cmds.listRelatives('head_lod0_grp', c=True):
            if 'head' in geo:
                continue
            cmds.setAttr(f'{geo}.v', 0)

    def create_position_locators(self, position_data={}):
        """
        'L_Eye': '',
        'R_Eye': '',
        'TongueStart': '',
        'TongueLeft': '',
        'TongueUp': '',
        'UpTeeth': '',
        'DwTeeth': '',

        Args:
            require_data:

        Returns:

        """

        if not position_data:
            return False

        grp_name = 'MetaMutant_Custom_Loc_Grp'
        if cmds.objExists(grp_name):
            cmds.delete(grp_name)
        grp_loc = cmds.group(em=True, name=grp_name)

        for i in position_data:
            if not position_data[i]:
                continue

            loc = cmds.spaceLocator(n=i+'_Loc')
            cmds.parent(loc, grp_loc)
            if ',' in position_data[i]:
                data = position_data[i].replace(' ', '')
                position_data[i] = data.split(',')
            cmds.select(position_data[i])
            temp_cls = cmds.cluster()
            cmds.delete(cmds.parentConstraint(temp_cls, loc))
            cmds.delete(temp_cls)

        if not cmds.listRelatives(grp_loc, c=True):
            cmds.delete(grp_loc)
            return False

        return True

    def meta_joint_custom_placement(self,surface_joints, positions):

        hierarchy_array = Skeletor.unparent_hierarchy(surface_joints)
        #---------------------------------------------

        # CUSTOM LOCATORS
        custom_locators_grp = 'MetaMutant_Custom_Loc_Grp'
        custom_mapping = {
            'L_Eye_Loc': 'FACIAL_L_Eye',
            'R_Eye_Loc': 'FACIAL_R_Eye',
            'TongueStart_Loc': 'FACIAL_C_Tongue1',
            'TongueEnd_Loc': 'FACIAL_C_Tongue4',
            'TongueRight_Loc': 'FACIAL_R_TongueSide2',
            'TongueLeft_Loc': 'FACIAL_L_TongueSide2',
            'TongueUp_Loc': 'FACIAL_C_TongueUpper2',
            'Jaw_Loc': 'FACIAL_C_Jaw',
            'UpTeeth_Loc': 'FACIAL_C_TeethUpper',
            'DwTeeth_Loc': 'FACIAL_C_TeethLower',
        }

        print('#'*20)
        print('#'*20)
        print(positions)
        print('#'*20)
        print('#'*20)

        for jnt in custom_mapping:
            try:
                cmds.setAttr(f'{custom_mapping[jnt]}.tx', positions[jnt.replace('_Loc', '')][0])
                cmds.setAttr(f'{custom_mapping[jnt]}.ty', positions[jnt.replace('_Loc', '')][1])
                cmds.setAttr(f'{custom_mapping[jnt]}.tz', positions[jnt.replace('_Loc', '')][2])
            except:
                pass



        #Extra Position Tongue
        cmds.setAttr('FACIAL_C_TongueUpper3.ty',cmds.getAttr('FACIAL_C_TongueUpper2.ty'))
        cmds.setAttr('FACIAL_C_TongueLower3.ty',cmds.getAttr('FACIAL_C_TongueUpper2.ty')-1)
        cmds.setAttr('FACIAL_L_TongueSide3.tx',cmds.getAttr('FACIAL_L_TongueSide2.tx'))
        cmds.setAttr('FACIAL_R_TongueSide3.tx',cmds.getAttr('FACIAL_R_TongueSide2.tx'))

        pos1 = cmds.xform('FACIAL_C_Tongue1', q=True, ws=True, t=True)
        pos4 = cmds.xform('FACIAL_C_Tongue4', q=True, ws=True, t=True)

        weight2 = 0.25  # Closer to FACIAL_C_Tongue1
        weight3 = 0.75  # Closer to FACIAL_C_Tongue4

        pos2 = [(1 - weight2) * p1 + weight2 * p4 for p1, p4 in zip(pos1, pos4)]
        pos3 = [(1 - weight3) * p1 + weight3 * p4 for p1, p4 in zip(pos1, pos4)]

        # Position the joints
        cmds.xform('FACIAL_C_Tongue2', ws=True, t=pos2)
        cmds.xform('FACIAL_C_Tongue3', ws=True, t=pos3)

        cmds.setAttr('FACIAL_C_TongueUpper3.tz', cmds.getAttr('FACIAL_C_Tongue3.tz'))
        cmds.setAttr('FACIAL_C_TongueLower3.tz', cmds.getAttr('FACIAL_C_Tongue3.tz'))
        cmds.setAttr('FACIAL_L_TongueSide3.tz', cmds.getAttr('FACIAL_C_Tongue3.tz'))
        cmds.setAttr('FACIAL_R_TongueSide3.tz', cmds.getAttr('FACIAL_C_Tongue3.tz'))

        cmds.setAttr('FACIAL_C_TongueUpper2.tz', cmds.getAttr('FACIAL_C_Tongue2.tz'))
        cmds.setAttr('FACIAL_L_TongueSide2.tz', cmds.getAttr('FACIAL_C_Tongue2.tz'))
        cmds.setAttr('FACIAL_R_TongueSide2.tz', cmds.getAttr('FACIAL_C_Tongue2.tz'))

        #Place joints with pivots
        #Eyes
        eye_joints = ['FACIAL_L_EyelidUpperA', 'FACIAL_L_EyelidUpperB', 'FACIAL_L_EyelidLowerA', 'FACIAL_L_EyelidLowerB']

        for jnt in eye_joints:
            cmds.delete(cmds.parentConstraint('FACIAL_L_Eye', jnt))
            cmds.delete(cmds.parentConstraint('FACIAL_R_Eye', jnt.replace('_L_', '_R_')))


        #Place Jaw
        cmds.delete(cmds.parentConstraint('FACIAL_C_Jaw','FACIAL_C_LowerLipRotation'))

        #---------------------------------------------
        Skeletor.parent_hierarchy(hierarchy_array)

    # --------------------------------------------------------------------------
    # --------------------------------------------------------------------------
    # ------------------------   BLENDSHAPES  ----------------------------------
    # --------------------------------------------------------------------------
    # --------------------------------------------------------------------------

    def animate(self):


        poses_length = len(self.meta_data)
        print(poses_length)

        default_pose = self.get_default_pose()

        poses_order = ['default','smile','sad','narrow','wide','jaw_open','roll_out',
                       'roll_in','lips_left','lips_right','nose_wrinkle', 'left_lip_up',
                       'right_lip_up', 'right_lip_dw', 'left_lip_dw'
                       ]

        for num, pose in enumerate(self.meta_data):
            print(num, pose)
            cmds.currentTime(num)

            pose_name = poses_order[num]
            pose_data = self.meta_data[pose_name]

            self.apply_pose(default_pose)
            self.select_meta_ctrls()
            cmds.setKeyframe()

            self.apply_pose(pose_data)
            self.select_meta_ctrls()
            cmds.setKeyframe()

        cmds.refresh()


    def get_default_pose(self):
        default_pose = self.meta_data['default']
        return default_pose

    def select_meta_ctrls(self):
        ctrls = cmds.ls('CTRL_*', type='transform')
        avoid_this = ['CTRL_expressions', 'CTRL_faceGUI']
        clean_ctrls = []
        for ctrl in ctrls:
            if ctrl in avoid_this:
                continue
            clean_ctrls.append(ctrl)
        cmds.select(clean_ctrls)
        return clean_ctrls

    def apply_pose(self, pose_data):
        avoid_this = ['CTRL_expressions', 'CTRL_faceGUI']
        for ctrl in pose_data:
            if ctrl in avoid_this:
                continue
            attrs = pose_data[ctrl]
            for attr in attrs:
                try:
                    cmds.setAttr(f"{ctrl}.{attr}", attrs[attr])
                except:
                    pass

    def save_current_pose_to_json(self, pose_name):
        script_dir = os.path.dirname(os.path.realpath(__file__))
        json_file_path = os.path.join(script_dir, 'meta_poses.json')

        #Read old poses
        meta_data = self.read_json(json_file_path)

        #Add new pose
        meta_data[pose_name] = self.get_current_meta_pose()

        with open(json_file_path, 'w') as json_file:
            json.dump(meta_data, json_file, indent=4)

    def get_current_meta_pose(self):
        # Find all controllers with the naming pattern 'CTRL_*'
        ctrls = cmds.ls('CTRL_*', type='transform')  # Ensure we only get transform nodes
        meta_pose = {}

        # Iterate through the controllers
        avoid_this = ['CTRL_expressions', 'CTRL_faceGUI']
        for ctrl in ctrls:
            if ctrl in avoid_this:
                continue
            # Get all keyable attributes (channels) on the controller
            keyable_attrs = cmds.listAttr(ctrl, keyable=True) or []

            # Create a dictionary to store the current values of the attributes
            attr_values = {}
            for attr in keyable_attrs:
                # Get the full attribute name (e.g., "CTRL_translateX")
                full_attr = f"{ctrl}.{attr}"
                if cmds.objExists(full_attr):
                    # Retrieve the current value of the attribute
                    attr_values[attr] = cmds.getAttr(full_attr)

            # Add the controller and its attributes to the meta_pose dictionary
            meta_pose[ctrl] = attr_values

        return meta_pose

    def read_json(self, file_path):
        """Read data from a JSON file if exists."""
        if os.path.exists(file_path):
            with open(file_path, 'r') as json_file:
                try:
                    return json.load(json_file)
                except json.JSONDecodeError:
                    print(f"Warning: {file_path} is empty or corrupted. Starting fresh.")
                    return {}
        return {}

    def extract_shapes(self, main_geo=None):
        if not main_geo:
            cmds.warning('We need main Geo')
            return
        cmds.select(main_geo)

        extract_grp = 'MetaMutant_Extract_Grp'
        if not cmds.objExists(extract_grp):
            cmds.group(em=True, n=extract_grp)

        poses_order = ['default', 'smile', 'sad', 'narrow', 'wide', 'jaw_open', 'roll_out',
                       'roll_in', 'lips_left', 'lips_right', 'nose_wrinkle', 'left_lip_up',
                       'right_lip_up', 'right_lip_dw', 'left_lip_dw'
                       ]

        for num, pose in enumerate(self.meta_data):
            print(num, pose)
            cmds.currentTime(num)

            pose_name = poses_order[num]
            new_geo = cmds.duplicate(main_geo, n="MetaMutant_"+pose_name)
            cmds.parent(new_geo, extract_grp)

    def save_extracted_shapes_as_temp(self):
        import tempfile

        temp_path = os.path.join(tempfile.gettempdir(), 'MetaMutant')
        dirt_temp_file = os.path.join(temp_path, 'MetaMutant_Shapes.ma')
        if not os.path.exists(temp_path):
            os.makedirs(temp_path)
        cmds.file(rename=dirt_temp_file)
        cmds.file(save=True, type="mayaAscii")

    def load_extracted_shapes_as_temp(self):
        import tempfile
        temp_path = os.path.join(tempfile.gettempdir(), 'MetaMutant')
        clean_temp_file = os.path.join(temp_path, 'MetaMutant_Shapes.ma')

        cmds.file(clean_temp_file, i=True)

    def open_shapes(self):
        mel.eval('SHAPES;')

    def connect_shapes_to_mutant_face(self):
        ''

#--------------------------
#--------------------------
#--------------------------
#--------------------------

#Unreal Fest Cmds Videos

#--------------------------
#--------------------------
#--------------------------
#--------------------------


# Imports
#from vtx_color import MESH_SHADER_MAPPING, VTX_COLOR_MESHES, VTX_COLOR_VALUES

surface_joints = ['FACIAL_C_NeckB', 'FACIAL_L_NeckB1', 'FACIAL_R_NeckB1', 'FACIAL_L_NeckB2', 'FACIAL_R_NeckB2',
                  'FACIAL_C_12IPV_NeckB1', 'FACIAL_C_12IPV_NeckB2', 'FACIAL_L_12IPV_NeckB3', 'FACIAL_R_12IPV_NeckB3',
                  'FACIAL_L_12IPV_NeckB4', 'FACIAL_R_12IPV_NeckB4', 'FACIAL_L_12IPV_NeckB5', 'FACIAL_R_12IPV_NeckB5',
                  'FACIAL_L_12IPV_NeckB6', 'FACIAL_R_12IPV_NeckB6', 'FACIAL_L_12IPV_NeckB7', 'FACIAL_R_12IPV_NeckB7',
                  'FACIAL_C_NeckBackB', 'FACIAL_L_NeckBackB', 'FACIAL_R_NeckBackB', 'FACIAL_C_12IPV_NeckBackB1',
                  'FACIAL_C_12IPV_NeckBackB2', 'FACIAL_L_12IPV_NeckBackB1', 'FACIAL_R_12IPV_NeckBackB1',
                  'FACIAL_L_12IPV_NeckBackB2', 'FACIAL_R_12IPV_NeckBackB2', 'FACIAL_C_AdamsApple',
                  'FACIAL_C_12IPV_AdamsA1', 'FACIAL_C_12IPV_AdamsA2', 'FACIAL_L_NeckA1', 'FACIAL_R_NeckA1',
                  'FACIAL_L_NeckA2', 'FACIAL_R_NeckA2', 'FACIAL_L_NeckA3', 'FACIAL_R_NeckA3', 'FACIAL_L_12IPV_NeckA1',
                  'FACIAL_R_12IPV_NeckA1', 'FACIAL_L_12IPV_NeckA2', 'FACIAL_R_12IPV_NeckA2', 'FACIAL_L_12IPV_NeckA3',
                  'FACIAL_R_12IPV_NeckA3', 'FACIAL_L_12IPV_NeckA4', 'FACIAL_R_12IPV_NeckA4', 'FACIAL_L_12IPV_NeckA5',
                  'FACIAL_R_12IPV_NeckA5', 'FACIAL_L_12IPV_NeckA6', 'FACIAL_R_12IPV_NeckA6', 'FACIAL_C_NeckBackA',
                  'FACIAL_L_NeckBackA', 'FACIAL_R_NeckBackA', 'FACIAL_C_12IPV_NeckBackA1', 'FACIAL_C_12IPV_NeckBackA2',
                  'FACIAL_L_12IPV_NeckBackA1', 'FACIAL_R_12IPV_NeckBackA1', 'FACIAL_L_12IPV_NeckBackA2',
                  'FACIAL_R_12IPV_NeckBackA2', 'FACIAL_C_Hair1', 'FACIAL_L_12IPV_Hair1', 'FACIAL_R_12IPV_Hair1',
                  'FACIAL_C_Hair2', 'FACIAL_C_Hair3', 'FACIAL_C_Hair4', 'FACIAL_C_Hair5', 'FACIAL_C_Hair6',
                  'FACIAL_L_HairA1', 'FACIAL_R_HairA1', 'FACIAL_L_HairA2', 'FACIAL_R_HairA2', 'FACIAL_L_HairA3',
                  'FACIAL_R_HairA3', 'FACIAL_L_HairA4', 'FACIAL_R_HairA4', 'FACIAL_L_HairA5', 'FACIAL_R_HairA5',
                  'FACIAL_L_HairA6', 'FACIAL_R_HairA6', 'FACIAL_L_HairB1', 'FACIAL_R_HairB1', 'FACIAL_L_HairB2',
                  'FACIAL_R_HairB2', 'FACIAL_L_HairB3', 'FACIAL_R_HairB3', 'FACIAL_L_HairB4', 'FACIAL_R_HairB4',
                  'FACIAL_L_HairB5', 'FACIAL_R_HairB5', 'FACIAL_L_Temple', 'FACIAL_R_Temple', 'FACIAL_L_12IPV_Temple1',
                  'FACIAL_R_12IPV_Temple1', 'FACIAL_L_12IPV_Temple2', 'FACIAL_R_12IPV_Temple2',
                  'FACIAL_L_12IPV_Temple3', 'FACIAL_R_12IPV_Temple3', 'FACIAL_L_12IPV_Temple4',
                  'FACIAL_R_12IPV_Temple4', 'FACIAL_L_HairC1', 'FACIAL_R_HairC1', 'FACIAL_L_HairC2', 'FACIAL_R_HairC2',
                  'FACIAL_L_HairC3', 'FACIAL_R_HairC3', 'FACIAL_L_HairC4', 'FACIAL_R_HairC4', 'FACIAL_L_Sideburn1',
                  'FACIAL_R_Sideburn1', 'FACIAL_L_Sideburn2', 'FACIAL_R_Sideburn2', 'FACIAL_L_Sideburn3',
                  'FACIAL_R_Sideburn3', 'FACIAL_L_Sideburn4', 'FACIAL_R_Sideburn4', 'FACIAL_L_Sideburn5',
                  'FACIAL_R_Sideburn5', 'FACIAL_L_Sideburn6', 'FACIAL_R_Sideburn6', 'FACIAL_C_ForeheadSkin',
                  'FACIAL_L_ForeheadInSkin', 'FACIAL_R_ForeheadInSkin', 'FACIAL_L_12IPV_ForeheadSkin1',
                  'FACIAL_R_12IPV_ForeheadSkin1', 'FACIAL_L_12IPV_ForeheadSkin2', 'FACIAL_R_12IPV_ForeheadSkin2',
                  'FACIAL_L_12IPV_ForeheadSkin3', 'FACIAL_R_12IPV_ForeheadSkin3', 'FACIAL_L_12IPV_ForeheadSkin4',
                  'FACIAL_R_12IPV_ForeheadSkin4', 'FACIAL_L_12IPV_ForeheadSkin5', 'FACIAL_R_12IPV_ForeheadSkin5',
                  'FACIAL_L_12IPV_ForeheadSkin6', 'FACIAL_R_12IPV_ForeheadSkin6', 'FACIAL_L_ForeheadMidSkin',
                  'FACIAL_R_ForeheadMidSkin', 'FACIAL_L_ForeheadOutSkin', 'FACIAL_R_ForeheadOutSkin',
                  'FACIAL_C_Forehead1', 'FACIAL_L_Forehead1', 'FACIAL_R_Forehead1', 'FACIAL_C_Forehead2',
                  'FACIAL_L_Forehead2', 'FACIAL_R_Forehead2', 'FACIAL_C_Forehead3', 'FACIAL_L_Forehead3',
                  'FACIAL_R_Forehead3', 'FACIAL_C_12IPV_Forehead1', 'FACIAL_L_12IPV_Forehead1',
                  'FACIAL_R_12IPV_Forehead1', 'FACIAL_C_12IPV_Forehead2', 'FACIAL_L_12IPV_Forehead2',
                  'FACIAL_R_12IPV_Forehead2', 'FACIAL_C_12IPV_Forehead3', 'FACIAL_L_12IPV_Forehead3',
                  'FACIAL_R_12IPV_Forehead3', 'FACIAL_C_12IPV_Forehead4', 'FACIAL_L_12IPV_Forehead4',
                  'FACIAL_R_12IPV_Forehead4', 'FACIAL_C_12IPV_Forehead5', 'FACIAL_L_12IPV_Forehead5',
                  'FACIAL_R_12IPV_Forehead5', 'FACIAL_C_12IPV_Forehead6', 'FACIAL_L_12IPV_Forehead6',
                  'FACIAL_R_12IPV_Forehead6', 'FACIAL_L_ForeheadInA1', 'FACIAL_L_ForeheadInA2', 'FACIAL_L_ForeheadInA3',
                  'FACIAL_L_ForeheadInB1', 'FACIAL_L_ForeheadInB2', 'FACIAL_L_12IPV_ForeheadIn1',
                  'FACIAL_L_12IPV_ForeheadIn2', 'FACIAL_L_12IPV_ForeheadIn3', 'FACIAL_L_12IPV_ForeheadIn4',
                  'FACIAL_L_12IPV_ForeheadIn5', 'FACIAL_L_12IPV_ForeheadIn6', 'FACIAL_L_12IPV_ForeheadIn7',
                  'FACIAL_L_12IPV_ForeheadIn8', 'FACIAL_L_12IPV_ForeheadIn9', 'FACIAL_L_12IPV_ForeheadIn10',
                  'FACIAL_L_12IPV_ForeheadIn11', 'FACIAL_L_12IPV_ForeheadIn12', 'FACIAL_L_12IPV_ForeheadIn13',
                  'FACIAL_L_12IPV_ForeheadIn14', 'FACIAL_R_ForeheadInA1', 'FACIAL_R_ForeheadInA2',
                  'FACIAL_R_ForeheadInA3', 'FACIAL_R_ForeheadInB1', 'FACIAL_R_ForeheadInB2',
                  'FACIAL_R_12IPV_ForeheadIn1', 'FACIAL_R_12IPV_ForeheadIn2', 'FACIAL_R_12IPV_ForeheadIn3',
                  'FACIAL_R_12IPV_ForeheadIn5', 'FACIAL_R_12IPV_ForeheadIn4', 'FACIAL_R_12IPV_ForeheadIn6',
                  'FACIAL_R_12IPV_ForeheadIn7', 'FACIAL_R_12IPV_ForeheadIn8', 'FACIAL_R_12IPV_ForeheadIn9',
                  'FACIAL_R_12IPV_ForeheadIn10', 'FACIAL_R_12IPV_ForeheadIn12', 'FACIAL_R_12IPV_ForeheadIn11',
                  'FACIAL_R_12IPV_ForeheadIn13', 'FACIAL_R_12IPV_ForeheadIn14', 'FACIAL_L_ForeheadMid1',
                  'FACIAL_L_ForeheadMid2', 'FACIAL_L_12IPV_ForeheadMid15', 'FACIAL_L_12IPV_ForeheadMid16',
                  'FACIAL_L_12IPV_ForeheadMid17', 'FACIAL_L_12IPV_ForeheadMid18', 'FACIAL_L_12IPV_ForeheadMid19',
                  'FACIAL_L_12IPV_ForeheadMid20', 'FACIAL_L_12IPV_ForeheadMid21', 'FACIAL_L_12IPV_ForeheadMid22',
                  'FACIAL_R_ForeheadMid1', 'FACIAL_R_ForeheadMid2', 'FACIAL_R_12IPV_ForeheadMid15',
                  'FACIAL_R_12IPV_ForeheadMid16', 'FACIAL_R_12IPV_ForeheadMid17', 'FACIAL_R_12IPV_ForeheadMid18',
                  'FACIAL_R_12IPV_ForeheadMid19', 'FACIAL_R_12IPV_ForeheadMid20', 'FACIAL_R_12IPV_ForeheadMid21',
                  'FACIAL_R_12IPV_ForeheadMid22', 'FACIAL_L_ForeheadOutA1', 'FACIAL_L_ForeheadOutA2',
                  'FACIAL_L_ForeheadOutB1', 'FACIAL_L_ForeheadOutB2', 'FACIAL_L_12IPV_ForeheadOut23',
                  'FACIAL_L_12IPV_ForeheadOut24', 'FACIAL_L_12IPV_ForeheadOut25', 'FACIAL_L_12IPV_ForeheadOut26',
                  'FACIAL_L_12IPV_ForeheadOut27', 'FACIAL_L_12IPV_ForeheadOut28', 'FACIAL_L_12IPV_ForeheadOut29',
                  'FACIAL_L_12IPV_ForeheadOut30', 'FACIAL_L_12IPV_ForeheadOut31', 'FACIAL_L_12IPV_ForeheadOut32',
                  'FACIAL_R_ForeheadOutA1', 'FACIAL_R_ForeheadOutA2', 'FACIAL_R_ForeheadOutB1',
                  'FACIAL_R_ForeheadOutB2', 'FACIAL_R_12IPV_ForeheadOut23', 'FACIAL_R_12IPV_ForeheadOut24',
                  'FACIAL_R_12IPV_ForeheadOut25', 'FACIAL_R_12IPV_ForeheadOut26', 'FACIAL_R_12IPV_ForeheadOut27',
                  'FACIAL_R_12IPV_ForeheadOut28', 'FACIAL_R_12IPV_ForeheadOut29', 'FACIAL_R_12IPV_ForeheadOut30',
                  'FACIAL_R_12IPV_ForeheadOut31', 'FACIAL_R_12IPV_ForeheadOut32', 'FACIAL_L_12IPV_EyesackU0',
                  'FACIAL_R_12IPV_EyesackU0', 'FACIAL_L_EyesackUpper1', 'FACIAL_L_EyesackUpper2',
                  'FACIAL_L_EyesackUpper3', 'FACIAL_R_EyesackUpper1', 'FACIAL_R_EyesackUpper2',
                  'FACIAL_R_EyesackUpper3', 'FACIAL_L_EyesackUpper4', 'FACIAL_R_EyesackUpper4',
                  'FACIAL_L_EyelidUpperFurrow1', 'FACIAL_L_EyelidUpperFurrow2', 'FACIAL_L_EyelidUpperFurrow3',
                  'FACIAL_R_EyelidUpperFurrow1', 'FACIAL_R_EyelidUpperFurrow2', 'FACIAL_R_EyelidUpperFurrow3',
                  'FACIAL_L_EyelidUpperB1', 'FACIAL_L_EyelidUpperB2', 'FACIAL_L_EyelidUpperB3',
                  'FACIAL_R_EyelidUpperB1', 'FACIAL_R_EyelidUpperB2', 'FACIAL_R_EyelidUpperB3',
                  'FACIAL_L_EyelidUpperA1', 'FACIAL_L_EyelashesUpperA1', 'FACIAL_L_EyelidUpperA2',
                  'FACIAL_L_EyelashesUpperA2', 'FACIAL_L_EyelidUpperA3', 'FACIAL_L_EyelashesUpperA3',
                  'FACIAL_R_EyelidUpperA1', 'FACIAL_R_EyelashesUpperA1', 'FACIAL_R_EyelidUpperA2',
                  'FACIAL_R_EyelashesUpperA2', 'FACIAL_R_EyelidUpperA3', 'FACIAL_R_EyelashesUpperA3',
                  'FACIAL_L_EyelidLowerA1', 'FACIAL_L_EyelidLowerA2', 'FACIAL_L_EyelidLowerA3',
                  'FACIAL_R_EyelidLowerA1', 'FACIAL_R_EyelidLowerA2', 'FACIAL_R_EyelidLowerA3',
                  'FACIAL_L_EyelidLowerB1', 'FACIAL_L_EyelidLowerB2', 'FACIAL_L_EyelidLowerB3',
                  'FACIAL_R_EyelidLowerB1', 'FACIAL_R_EyelidLowerB2', 'FACIAL_R_EyelidLowerB3',
                  'FACIAL_L_EyeCornerInner1', 'FACIAL_L_EyeCornerInner2', 'FACIAL_R_EyeCornerInner1',
                  'FACIAL_R_EyeCornerInner2', 'FACIAL_L_EyeCornerOuter1', 'FACIAL_L_EyelashesCornerOuter1',
                  'FACIAL_L_EyeCornerOuter2', 'FACIAL_R_EyeCornerOuter1', 'FACIAL_R_EyelashesCornerOuter1',
                  'FACIAL_R_EyeCornerOuter2', 'FACIAL_L_12IPV_EyeCornerO1', 'FACIAL_R_12IPV_EyeCornerO1',
                  'FACIAL_L_12IPV_EyeCornerO2', 'FACIAL_R_12IPV_EyeCornerO2', 'FACIAL_L_EyesackLower1',
                  'FACIAL_L_EyesackLower2', 'FACIAL_L_12IPV_EyesackL1', 'FACIAL_L_12IPV_EyesackL2',
                  'FACIAL_L_12IPV_EyesackL3', 'FACIAL_L_12IPV_EyesackL4', 'FACIAL_L_12IPV_EyesackL5',
                  'FACIAL_L_12IPV_EyesackL6', 'FACIAL_L_12IPV_EyesackL7', 'FACIAL_L_12IPV_EyesackL8',
                  'FACIAL_R_EyesackLower1', 'FACIAL_R_EyesackLower2', 'FACIAL_R_12IPV_EyesackL1',
                  'FACIAL_R_12IPV_EyesackL2', 'FACIAL_R_12IPV_EyesackL3', 'FACIAL_R_12IPV_EyesackL4',
                  'FACIAL_R_12IPV_EyesackL5', 'FACIAL_R_12IPV_EyesackL6', 'FACIAL_R_12IPV_EyesackL7',
                  'FACIAL_R_12IPV_EyesackL8', 'FACIAL_L_CheekInner1', 'FACIAL_L_CheekInner2', 'FACIAL_L_CheekInner3',
                  'FACIAL_L_CheekInner4', 'FACIAL_R_CheekInner1', 'FACIAL_R_CheekInner2', 'FACIAL_R_CheekInner3',
                  'FACIAL_R_CheekInner4', 'FACIAL_L_CheekOuter1', 'FACIAL_L_CheekOuter2', 'FACIAL_L_CheekOuter3',
                  'FACIAL_R_CheekOuter1', 'FACIAL_R_CheekOuter2', 'FACIAL_R_CheekOuter3', 'FACIAL_L_CheekOuter4',
                  'FACIAL_R_CheekOuter4', 'FACIAL_L_12IPV_CheekOuter1', 'FACIAL_R_12IPV_CheekOuter1',
                  'FACIAL_L_12IPV_CheekOuter2', 'FACIAL_R_12IPV_CheekOuter2', 'FACIAL_L_12IPV_CheekOuter3',
                  'FACIAL_R_12IPV_CheekOuter3', 'FACIAL_L_12IPV_CheekOuter4', 'FACIAL_R_12IPV_CheekOuter4',
                  'FACIAL_C_12IPV_NoseBridge1', 'FACIAL_L_12IPV_NoseBridge1', 'FACIAL_R_12IPV_NoseBridge1',
                  'FACIAL_C_12IPV_NoseBridge2', 'FACIAL_L_12IPV_NoseBridge2', 'FACIAL_R_12IPV_NoseBridge2',
                  'FACIAL_L_NoseBridge', 'FACIAL_R_NoseBridge', 'FACIAL_C_NoseUpper', 'FACIAL_L_NoseUpper',
                  'FACIAL_R_NoseUpper', 'FACIAL_C_12IPV_NoseUpper1', 'FACIAL_C_12IPV_NoseUpper2',
                  'FACIAL_L_12IPV_NoseUpper1', 'FACIAL_R_12IPV_NoseUpper1', 'FACIAL_L_12IPV_NoseUpper2',
                  'FACIAL_R_12IPV_NoseUpper2', 'FACIAL_L_12IPV_NoseUpper3', 'FACIAL_R_12IPV_NoseUpper3',
                  'FACIAL_L_12IPV_NoseUpper4', 'FACIAL_R_12IPV_NoseUpper4', 'FACIAL_L_12IPV_NoseUpper5',
                  'FACIAL_R_12IPV_NoseUpper5', 'FACIAL_L_12IPV_NoseUpper6', 'FACIAL_R_12IPV_NoseUpper6',
                  'FACIAL_L_NasolabialBulge1', 'FACIAL_R_NasolabialBulge1', 'FACIAL_L_12IPV_NasolabialB13',
                  'FACIAL_R_12IPV_NasolabialB13', 'FACIAL_L_12IPV_NasolabialB14', 'FACIAL_R_12IPV_NasolabialB14',
                  'FACIAL_L_12IPV_NasolabialB15', 'FACIAL_R_12IPV_NasolabialB15', 'FACIAL_L_NasolabialBulge2',
                  'FACIAL_L_NasolabialBulge3', 'FACIAL_L_12IPV_NasolabialB1', 'FACIAL_L_12IPV_NasolabialB2',
                  'FACIAL_L_12IPV_NasolabialB3', 'FACIAL_L_12IPV_NasolabialB4', 'FACIAL_L_12IPV_NasolabialB5',
                  'FACIAL_L_12IPV_NasolabialB6', 'FACIAL_L_12IPV_NasolabialB7', 'FACIAL_L_12IPV_NasolabialB8',
                  'FACIAL_L_12IPV_NasolabialB9', 'FACIAL_L_12IPV_NasolabialB10', 'FACIAL_L_12IPV_NasolabialB11',
                  'FACIAL_L_12IPV_NasolabialB12', 'FACIAL_R_NasolabialBulge2', 'FACIAL_R_NasolabialBulge3',
                  'FACIAL_R_12IPV_NasolabialB1', 'FACIAL_R_12IPV_NasolabialB2', 'FACIAL_R_12IPV_NasolabialB3',
                  'FACIAL_R_12IPV_NasolabialB4', 'FACIAL_R_12IPV_NasolabialB5', 'FACIAL_R_12IPV_NasolabialB6',
                  'FACIAL_R_12IPV_NasolabialB7', 'FACIAL_R_12IPV_NasolabialB8', 'FACIAL_R_12IPV_NasolabialB9',
                  'FACIAL_R_12IPV_NasolabialB10', 'FACIAL_R_12IPV_NasolabialB11', 'FACIAL_R_12IPV_NasolabialB12',
                  'FACIAL_L_NasolabialFurrow', 'FACIAL_R_NasolabialFurrow', 'FACIAL_L_12IPV_NasolabialF1',
                  'FACIAL_R_12IPV_NasolabialF1', 'FACIAL_L_12IPV_NasolabialF2', 'FACIAL_R_12IPV_NasolabialF2',
                  'FACIAL_L_12IPV_NasolabialF3', 'FACIAL_R_12IPV_NasolabialF3', 'FACIAL_L_12IPV_NasolabialF4',
                  'FACIAL_R_12IPV_NasolabialF4', 'FACIAL_L_12IPV_NasolabialF5', 'FACIAL_R_12IPV_NasolabialF5',
                  'FACIAL_L_12IPV_NasolabialF6', 'FACIAL_R_12IPV_NasolabialF6', 'FACIAL_L_12IPV_NasolabialF7',
                  'FACIAL_R_12IPV_NasolabialF7', 'FACIAL_L_12IPV_NasolabialF8', 'FACIAL_R_12IPV_NasolabialF8',
                  'FACIAL_L_12IPV_NasolabialF9', 'FACIAL_R_12IPV_NasolabialF9', 'FACIAL_L_CheekLower1',
                  'FACIAL_L_CheekLower2', 'FACIAL_L_12IPV_CheekL1', 'FACIAL_L_12IPV_CheekL2', 'FACIAL_L_12IPV_CheekL3',
                  'FACIAL_L_12IPV_CheekL4', 'FACIAL_R_CheekLower1', 'FACIAL_R_CheekLower2', 'FACIAL_R_12IPV_CheekL1',
                  'FACIAL_R_12IPV_CheekL2', 'FACIAL_R_12IPV_CheekL3', 'FACIAL_R_12IPV_CheekL4',
                  'FACIAL_L_NostrilThickness3', 'FACIAL_R_NostrilThickness3', 'FACIAL_C_12IPV_NoseL1',
                  'FACIAL_C_12IPV_NoseL2', 'FACIAL_C_12IPV_NoseTip1', 'FACIAL_C_12IPV_NoseTip2',
                  'FACIAL_C_12IPV_NoseTip3', 'FACIAL_L_12IPV_NoseTip1', 'FACIAL_R_12IPV_NoseTip1',
                  'FACIAL_L_12IPV_NoseTip2', 'FACIAL_R_12IPV_NoseTip2', 'FACIAL_L_12IPV_NoseTip3',
                  'FACIAL_R_12IPV_NoseTip3', 'FACIAL_L_NostrilThickness1', 'FACIAL_L_NostrilThickness2',
                  'FACIAL_L_12IPV_Nostril1', 'FACIAL_L_12IPV_Nostril2', 'FACIAL_L_12IPV_Nostril3',
                  'FACIAL_L_12IPV_Nostril4', 'FACIAL_L_12IPV_Nostril5', 'FACIAL_L_12IPV_Nostril6',
                  'FACIAL_L_12IPV_Nostril7', 'FACIAL_L_12IPV_Nostril8', 'FACIAL_L_12IPV_Nostril9',
                  'FACIAL_L_12IPV_Nostril10', 'FACIAL_L_12IPV_Nostril11', 'FACIAL_L_12IPV_Nostril12',
                  'FACIAL_L_12IPV_Nostril13', 'FACIAL_L_12IPV_Nostril14', 'FACIAL_R_NostrilThickness1',
                  'FACIAL_R_NostrilThickness2', 'FACIAL_R_12IPV_Nostril1', 'FACIAL_R_12IPV_Nostril2',
                  'FACIAL_R_12IPV_Nostril3', 'FACIAL_R_12IPV_Nostril4', 'FACIAL_R_12IPV_Nostril5',
                  'FACIAL_R_12IPV_Nostril6', 'FACIAL_R_12IPV_Nostril7', 'FACIAL_R_12IPV_Nostril8',
                  'FACIAL_R_12IPV_Nostril9', 'FACIAL_R_12IPV_Nostril10', 'FACIAL_R_12IPV_Nostril11',
                  'FACIAL_R_12IPV_Nostril12', 'FACIAL_R_12IPV_Nostril13', 'FACIAL_R_12IPV_Nostril14',
                  'FACIAL_C_LipUpperSkin', 'FACIAL_L_LipUpperSkin', 'FACIAL_R_LipUpperSkin',
                  'FACIAL_L_LipUpperOuterSkin', 'FACIAL_R_LipUpperOuterSkin', 'FACIAL_C_12IPV_LipUpperSkin1',
                  'FACIAL_C_12IPV_LipUpperSkin2', 'FACIAL_L_12IPV_LipUpperSkin', 'FACIAL_R_12IPV_LipUpperSkin',
                  'FACIAL_L_12IPV_LipUpperOuterSkin1', 'FACIAL_R_12IPV_LipUpperOuterSkin1',
                  'FACIAL_L_12IPV_LipUpperOuterSkin2', 'FACIAL_R_12IPV_LipUpperOuterSkin2',
                  'FACIAL_L_12IPV_MouthInteriorUpper1', 'FACIAL_R_12IPV_MouthInteriorUpper1',
                  'FACIAL_L_12IPV_MouthInteriorUpper2', 'FACIAL_R_12IPV_MouthInteriorUpper2', 'FACIAL_C_LipUpper1',
                  'FACIAL_C_LipUpper2', 'FACIAL_C_LipUpper3', 'FACIAL_L_12IPV_LipUpper1', 'FACIAL_R_12IPV_LipUpper1',
                  'FACIAL_L_12IPV_LipUpper2', 'FACIAL_R_12IPV_LipUpper2', 'FACIAL_L_12IPV_LipUpper3',
                  'FACIAL_R_12IPV_LipUpper3', 'FACIAL_L_12IPV_LipUpper4', 'FACIAL_R_12IPV_LipUpper4',
                  'FACIAL_L_12IPV_LipUpper5', 'FACIAL_R_12IPV_LipUpper5', 'FACIAL_L_LipUpper1', 'FACIAL_L_LipUpper2',
                  'FACIAL_L_LipUpper3', 'FACIAL_L_12IPV_LipUpper6', 'FACIAL_L_12IPV_LipUpper7',
                  'FACIAL_L_12IPV_LipUpper8', 'FACIAL_L_12IPV_LipUpper9', 'FACIAL_L_12IPV_LipUpper10',
                  'FACIAL_L_12IPV_LipUpper11', 'FACIAL_L_12IPV_LipUpper12', 'FACIAL_L_12IPV_LipUpper13',
                  'FACIAL_L_12IPV_LipUpper14', 'FACIAL_L_12IPV_LipUpper15', 'FACIAL_R_LipUpper1', 'FACIAL_R_LipUpper2',
                  'FACIAL_R_LipUpper3', 'FACIAL_R_12IPV_LipUpper6', 'FACIAL_R_12IPV_LipUpper7',
                  'FACIAL_R_12IPV_LipUpper8', 'FACIAL_R_12IPV_LipUpper9', 'FACIAL_R_12IPV_LipUpper10',
                  'FACIAL_R_12IPV_LipUpper11', 'FACIAL_R_12IPV_LipUpper12', 'FACIAL_R_12IPV_LipUpper13',
                  'FACIAL_R_12IPV_LipUpper14', 'FACIAL_R_12IPV_LipUpper15', 'FACIAL_L_LipUpperOuter1',
                  'FACIAL_L_LipUpperOuter2', 'FACIAL_L_LipUpperOuter3', 'FACIAL_L_12IPV_LipUpper16',
                  'FACIAL_L_12IPV_LipUpper17', 'FACIAL_L_12IPV_LipUpper18', 'FACIAL_L_12IPV_LipUpper19',
                  'FACIAL_L_12IPV_LipUpper20', 'FACIAL_L_12IPV_LipUpper21', 'FACIAL_L_12IPV_LipUpper22',
                  'FACIAL_L_12IPV_LipUpper23', 'FACIAL_L_12IPV_LipUpper24', 'FACIAL_R_LipUpperOuter1',
                  'FACIAL_R_LipUpperOuter2', 'FACIAL_R_LipUpperOuter3', 'FACIAL_R_12IPV_LipUpper16',
                  'FACIAL_R_12IPV_LipUpper17', 'FACIAL_R_12IPV_LipUpper18', 'FACIAL_R_12IPV_LipUpper19',
                  'FACIAL_R_12IPV_LipUpper20', 'FACIAL_R_12IPV_LipUpper21', 'FACIAL_R_12IPV_LipUpper22',
                  'FACIAL_R_12IPV_LipUpper23', 'FACIAL_R_12IPV_LipUpper24', 'FACIAL_L_LipCorner1',
                  'FACIAL_L_LipCorner2', 'FACIAL_L_LipCorner3', 'FACIAL_L_12IPV_LipCorner1',
                  'FACIAL_L_12IPV_LipCorner2', 'FACIAL_L_12IPV_LipCorner3', 'FACIAL_R_LipCorner1',
                  'FACIAL_R_LipCorner2', 'FACIAL_R_LipCorner3', 'FACIAL_R_12IPV_LipCorner1',
                  'FACIAL_R_12IPV_LipCorner2', 'FACIAL_R_12IPV_LipCorner3', 'FACIAL_L_JawBulge', 'FACIAL_R_JawBulge',
                  'FACIAL_L_JawRecess', 'FACIAL_R_JawRecess', 'FACIAL_L_Masseter', 'FACIAL_R_Masseter',
                  'FACIAL_C_UnderChin', 'FACIAL_L_12IPV_UnderChin1', 'FACIAL_R_12IPV_UnderChin1',
                  'FACIAL_L_12IPV_UnderChin2', 'FACIAL_R_12IPV_UnderChin2', 'FACIAL_L_UnderChin', 'FACIAL_R_UnderChin',
                  'FACIAL_L_12IPV_UnderChin3', 'FACIAL_R_12IPV_UnderChin3', 'FACIAL_L_12IPV_UnderChin4',
                  'FACIAL_R_12IPV_UnderChin4', 'FACIAL_L_12IPV_UnderChin5', 'FACIAL_R_12IPV_UnderChin5',
                  'FACIAL_L_12IPV_UnderChin6', 'FACIAL_R_12IPV_UnderChin6', 'FACIAL_C_LipLowerSkin',
                  'FACIAL_L_LipLowerSkin', 'FACIAL_R_LipLowerSkin', 'FACIAL_L_LipLowerOuterSkin',
                  'FACIAL_R_LipLowerOuterSkin', 'FACIAL_C_12IPV_LipLowerSkin1', 'FACIAL_C_12IPV_LipLowerSkin2',
                  'FACIAL_L_12IPV_LipLowerSkin', 'FACIAL_R_12IPV_LipLowerSkin', 'FACIAL_L_12IPV_LipLowerOuterSkin1',
                  'FACIAL_R_12IPV_LipLowerOuterSkin1', 'FACIAL_L_12IPV_LipLowerOuterSkin2',
                  'FACIAL_R_12IPV_LipLowerOuterSkin2', 'FACIAL_L_12IPV_LipLowerOuterSkin3',
                  'FACIAL_R_12IPV_LipLowerOuterSkin3', 'FACIAL_L_12IPV_MouthInteriorLower1',
                  'FACIAL_R_12IPV_MouthInteriorLower1', 'FACIAL_L_12IPV_MouthInteriorLower2',
                  'FACIAL_R_12IPV_MouthInteriorLower2', 'FACIAL_C_LipLower1', 'FACIAL_C_LipLower2',
                  'FACIAL_C_LipLower3', 'FACIAL_L_12IPV_LipLower1', 'FACIAL_R_12IPV_LipLower1',
                  'FACIAL_L_12IPV_LipLower2', 'FACIAL_R_12IPV_LipLower2', 'FACIAL_L_12IPV_LipLower3',
                  'FACIAL_R_12IPV_LipLower3', 'FACIAL_L_12IPV_LipLower4', 'FACIAL_R_12IPV_LipLower4',
                  'FACIAL_L_12IPV_LipLower5', 'FACIAL_R_12IPV_LipLower5', 'FACIAL_L_LipLower1', 'FACIAL_L_LipLower2',
                  'FACIAL_L_LipLower3', 'FACIAL_L_12IPV_LipLower6', 'FACIAL_L_12IPV_LipLower7',
                  'FACIAL_L_12IPV_LipLower8', 'FACIAL_L_12IPV_LipLower9', 'FACIAL_L_12IPV_LipLower10',
                  'FACIAL_L_12IPV_LipLower11', 'FACIAL_L_12IPV_LipLower12', 'FACIAL_L_12IPV_LipLower13',
                  'FACIAL_L_12IPV_LipLower14', 'FACIAL_L_12IPV_LipLower15', 'FACIAL_R_LipLower1', 'FACIAL_R_LipLower2',
                  'FACIAL_R_LipLower3', 'FACIAL_R_12IPV_LipLower6', 'FACIAL_R_12IPV_LipLower7',
                  'FACIAL_R_12IPV_LipLower8', 'FACIAL_R_12IPV_LipLower9', 'FACIAL_R_12IPV_LipLower10',
                  'FACIAL_R_12IPV_LipLower11', 'FACIAL_R_12IPV_LipLower12', 'FACIAL_R_12IPV_LipLower13',
                  'FACIAL_R_12IPV_LipLower14', 'FACIAL_R_12IPV_LipLower15', 'FACIAL_L_LipLowerOuter1',
                  'FACIAL_L_LipLowerOuter2', 'FACIAL_L_LipLowerOuter3', 'FACIAL_L_12IPV_LipLower16',
                  'FACIAL_L_12IPV_LipLower17', 'FACIAL_L_12IPV_LipLower18', 'FACIAL_L_12IPV_LipLower19',
                  'FACIAL_L_12IPV_LipLower20', 'FACIAL_L_12IPV_LipLower21', 'FACIAL_L_12IPV_LipLower22',
                  'FACIAL_L_12IPV_LipLower23', 'FACIAL_L_12IPV_LipLower24', 'FACIAL_R_LipLowerOuter1',
                  'FACIAL_R_LipLowerOuter2', 'FACIAL_R_LipLowerOuter3', 'FACIAL_R_12IPV_LipLower16',
                  'FACIAL_R_12IPV_LipLower17', 'FACIAL_R_12IPV_LipLower18', 'FACIAL_R_12IPV_LipLower19',
                  'FACIAL_R_12IPV_LipLower20', 'FACIAL_R_12IPV_LipLower21', 'FACIAL_R_12IPV_LipLower22',
                  'FACIAL_R_12IPV_LipLower23', 'FACIAL_R_12IPV_LipLower24', 'FACIAL_C_Jawline',
                  'FACIAL_L_12IPV_Jawline1', 'FACIAL_R_12IPV_Jawline1', 'FACIAL_L_12IPV_Jawline2',
                  'FACIAL_R_12IPV_Jawline2', 'FACIAL_L_Jawline1', 'FACIAL_L_Jawline2', 'FACIAL_L_12IPV_Jawline3',
                  'FACIAL_L_12IPV_Jawline4', 'FACIAL_L_12IPV_Jawline5', 'FACIAL_L_12IPV_Jawline6', 'FACIAL_R_Jawline1',
                  'FACIAL_R_Jawline2', 'FACIAL_R_12IPV_Jawline3', 'FACIAL_R_12IPV_Jawline4', 'FACIAL_R_12IPV_Jawline5',
                  'FACIAL_R_12IPV_Jawline6', 'FACIAL_L_ChinSide', 'FACIAL_R_ChinSide', 'FACIAL_L_12IPV_ChinS1',
                  'FACIAL_R_12IPV_ChinS1', 'FACIAL_L_12IPV_ChinS2', 'FACIAL_R_12IPV_ChinS2', 'FACIAL_L_12IPV_ChinS3',
                  'FACIAL_R_12IPV_ChinS3', 'FACIAL_L_12IPV_ChinS4', 'FACIAL_R_12IPV_ChinS4', 'FACIAL_C_Chin1',
                  'FACIAL_L_Chin1', 'FACIAL_R_Chin1', 'FACIAL_C_Chin2', 'FACIAL_L_Chin2', 'FACIAL_R_Chin2',
                  'FACIAL_C_Chin3', 'FACIAL_L_Chin3', 'FACIAL_R_Chin3', 'FACIAL_L_12IPV_Chin1', 'FACIAL_R_12IPV_Chin1',
                  'FACIAL_L_12IPV_Chin2', 'FACIAL_R_12IPV_Chin2', 'FACIAL_C_12IPV_Chin3', 'FACIAL_C_12IPV_Chin4',
                  'FACIAL_L_12IPV_Chin5', 'FACIAL_R_12IPV_Chin5', 'FACIAL_L_12IPV_Chin6', 'FACIAL_R_12IPV_Chin6',
                  'FACIAL_L_12IPV_Chin7', 'FACIAL_R_12IPV_Chin7', 'FACIAL_L_12IPV_Chin8', 'FACIAL_R_12IPV_Chin8',
                  'FACIAL_L_12IPV_Chin9', 'FACIAL_R_12IPV_Chin9', 'FACIAL_L_12IPV_Chin10', 'FACIAL_R_12IPV_Chin10',
                  'FACIAL_L_12IPV_Chin11', 'FACIAL_R_12IPV_Chin11', 'FACIAL_L_12IPV_Chin12', 'FACIAL_R_12IPV_Chin12',
                  'FACIAL_L_12IPV_Chin13', 'FACIAL_R_12IPV_Chin13', 'FACIAL_L_12IPV_Chin14', 'FACIAL_R_12IPV_Chin14',
                  'FACIAL_C_NoseBridge', 'FACIAL_L_Ear', 'FACIAL_L_Ear1', 'FACIAL_L_Ear2', 'FACIAL_L_Ear3',
                  'FACIAL_L_Ear4', 'FACIAL_R_Ear', 'FACIAL_R_Ear1', 'FACIAL_R_Ear2', 'FACIAL_R_Ear3', 'FACIAL_R_Ear4']

def read_dna(path):
    stream = FileStream(path, FileStream.AccessMode_Read, FileStream.OpenMode_Binary)
    reader = BinaryStreamReader(stream, DataLayer_All)
    reader.read()
    if not Status.isOk():
        status = Status.get()
        raise RuntimeError(f"Error loading DNA: {status.message}")
    return reader


def save_dna(reader, path):
    stream = FileStream(path, FileStream.AccessMode_Write, FileStream.OpenMode_Binary)
    writer = BinaryStreamWriter(stream)
    writer.setFrom(reader)
    writer.write()

    if not Status.isOk():
        status = Status.get()
        raise RuntimeError(f"Error saving DNA: {status.message}")

    print(f"DNA {path} successfully saved.")


def show_meshes(dna_path, add_skinning=False, add_blend_shapes=False):
    cmds.file(force=True, new=True)

    dna = DNA(dna_path)

    # Builds and returns the created mesh paths in the scene
    config = Config(
        add_joints=True,
        add_blend_shapes=add_blend_shapes,
        add_skin_cluster=add_skinning,
        add_ctrl_attributes_on_root_joint=True,
        add_animated_map_attributes_on_root_joint=True,
        add_mesh_name_to_blend_shape_channel_name=True,
        add_key_frames=True
    )

    # Build meshes
    build_meshes(dna, config)


def assemble_scene(dna_path, analog_gui_path, gui_path,
                   additional_assemble_script):
    dna = DNA(dna_path)
    config = RigConfig(
        gui_path=gui_path,
        analog_gui_path=analog_gui_path,
        aas_path=additional_assemble_script,
        add_animated_map_attributes_on_root_joint=True,
        add_key_frames=True,
        add_mesh_name_to_blend_shape_channel_name=True
    )

    # Creates the rig
    build_rig(dna=dna, config=config)

    translation = cmds.xform("neck_01", ws=True, query=True, translation=True)
    cmds.xform("CTRL_faceGUI", ws=True, t=[translation[0] + 20, translation[1] + 5, translation[2]])


def get_mesh_vertex_positions_from_scene(meshName):
    try:
        sel = om.MSelectionList()
        sel.add(meshName)

        dag_path = om.MDagPath()
        sel.getDagPath(0, dag_path)

        mf_mesh = om.MFnMesh(dag_path)
        positions = om.MPointArray()

        mf_mesh.getPoints(positions, om.MSpace.kObject)
        return [
            [positions[i].x, positions[i].y, positions[i].z]
            for i in range(positions.length())
        ]
    except RuntimeError:
        print(f"{meshName} is missing, skipping it")
        return None


def run_joints_command(reader, calibrated):
    # Making arrays for joints' transformations and their corresponding mapping arrays
    joint_translations = []
    joint_rotations = []

    for i in range(reader.getJointCount()):
        joint_name = reader.getJointName(i)

        translation = cmds.xform(joint_name, query=True, translation=True)
        joint_translations.append(translation)

        rotation = cmds.joint(joint_name, query=True, orientation=True)
        joint_rotations.append(rotation)

    set_new_joints_translations = SetNeutralJointTranslationsCommand(joint_translations)
    set_new_joints_rotations = SetNeutralJointRotationsCommand(joint_rotations)

    # Abstraction to collect all commands into a sequence, and run them with only one invocation
    commands = CommandSequence()

    commands.add(set_new_joints_translations)
    commands.add(set_new_joints_rotations)

    commands.run(calibrated)
    # verify that everything went fine
    if not Status.isOk():
        status = Status.get()
        raise RuntimeError(f"Error do_joints_command: {status.message}")


def run_vertices_command(
        calibrated, old_vertices_positions, new_vertices_positions, mesh_index
):
    # making deltas between old vertices positions and new one
    deltas = []
    for new_vertex, old_vertex in zip(new_vertices_positions, old_vertices_positions):
        delta = []
        for new, old in zip(new_vertex, old_vertex):
            delta.append(new - old)
        deltas.append(delta)

    new_neutral_mesh = SetVertexPositionsCommand(
        mesh_index, deltas, VectorOperation_Add
    )

    commands = CommandSequence()

    # Add new vertex position deltas (NOT ABSOLUTE VALUES) onto existing vertex positions
    commands.add(new_neutral_mesh)

    # Recalculate lower LODs based on LOD0
    calculate_command = CalculateMeshLowerLODsCommand()
    commands.add(calculate_command)

    commands.run(calibrated)

    # verify that everything went fine
    if not Status.isOk():
        status = Status.get()
        raise RuntimeError(f"Error do_vertices_command: {status.message}")


def transfer_joints_positions_distance(a, b):
    return pow((a[0] - b[0]), 2) + pow((a[1] - b[1]), 2) + pow((a[2] - b[2]), 2)


def find_and_save_joint_positions_in_file(reader, joints, file_path):
    mesh = reader.getMeshName(0)
    output = {}
    for joint_name in joints:
        cmds.select(joint_name)

        joint_pos = cmds.xform(joint_name, q=True, ws=True, translation=True)
        near_point = mel.eval(f"nearestPointOnMesh {mesh}")
        cmds.setAttr(f"{near_point}.inPositionX", joint_pos[0])
        cmds.setAttr(f"{near_point}.inPositionY", joint_pos[1])
        cmds.setAttr(f"{near_point}.inPositionZ", joint_pos[2])
        best_face = cmds.getAttr(f"{near_point}.nearestFaceIndex")

        face_vtx_str = cmds.polyInfo(f"{mesh}.f[{best_face}]", fv=True)
        buffer = face_vtx_str[0].split()
        closest_vtx = 0
        dist = 10000
        for v in range(2, len(buffer)):
            vtx = buffer[v]
            vtx_pos = cmds.xform(f"{mesh}.vtx[{vtx}]", q=True, ws=True, translation=True)
            new_dist = transfer_joints_positions_distance(joint_pos, vtx_pos)
            if new_dist < dist:
                dist = new_dist
                closest_vtx = vtx
        output[joint_name] = closest_vtx

    with open(file_path, 'w') as out_file:
        json.dump(output, out_file, indent=4)


def prepare_rotated_dna(dna_path, rotated_dna_path):
    reader = read_dna(dna_path)

    # Copies DNA contents and will serve as input/output parameter to commands
    calibrated = DNACalibDNAReader(reader)

    # Modifies calibrated DNA in-place
    rotate = RotateCommand([90.0, 0.0, 0.0], [0.0, 0.0, 0.0])
    rotate.run(calibrated)

    save_dna(calibrated, rotated_dna_path)
    return DNA(rotated_dna_path)


def get_dna(dna_path, rotated_dna_path):
    if up_axis == "z":
        return prepare_rotated_dna(dna_path, rotated_dna_path)
    return DNA(dna_path)


def build_meshes_for_lod(dna, lod):
    # Create config
    config = Config(
        group_by_lod=False,
        create_display_layers=False,
        lod_filter=[lod],
        add_mesh_name_to_blend_shape_channel_name=True,
    )

    # Builds and returns the created mesh paths in the scene
    return build_meshes(dna, config)


def create_skin_cluster(influences, mesh, skin_cluster_name, maximum_influences):
    cmds.select(influences[0], replace=True)
    cmds.select(mesh, add=True)
    skinCluster = cmds.skinCluster(
        toSelectedBones=True,
        name=skin_cluster_name,
        maximumInfluences=maximum_influences,
        skinMethod=0,
        obeyMaxInfluences=True,
    )
    if len(influences) > 1:
        cmds.skinCluster(
            skinCluster, edit=True, addInfluence=influences[1:], weight=0.0
        )
    return skinCluster


def create_head_and_body_scene(mesh_names, body_file, neck_joints, root_joint, facial_root_joints):
    scene_mesh_names = []
    skinweights = []

    for mesh_name in mesh_names:
        if cmds.objExists(mesh_name):
            scene_mesh_names.append(mesh_name)
            skinweights.append(get_skin_weights_from_scene(mesh_name))
            cmds.delete(f"{mesh_name}_skinCluster")

    for facial_joint in facial_root_joints:
        cmds.parent(facial_joint, world=True)
    cmds.delete(root_joint)

    cmds.file(body_file, options="v=0", type="mayaAscii", i=True)
    if up_axis == "y":
        cmds.joint("root", edit=True, orientation=[-90.0, 0.0, 0.0])
    for facial_joint, neck_joint in zip(facial_root_joints, neck_joints):
        cmds.parent(facial_joint, neck_joint)

    for mesh_name, skinweight in zip(scene_mesh_names, skinweights):
        create_skin_cluster(
            skinweight.joints,
            mesh_name,
            f"{mesh_name}_skinCluster",
            skinweight.no_of_influences,
        )
        set_skin_weights_to_scene(mesh_name, skinweight)


def set_fbx_options(orientation):
    # Executes FBX relate commands from the imported plugin
    min_time = cmds.playbackOptions(minTime=True, query=True)
    max_time = cmds.playbackOptions(maxTime=True, query=True)

    cmds.FBXResetExport()
    mel.eval("FBXExportBakeComplexAnimation -v true")
    mel.eval(f"FBXExportBakeComplexStart -v {min_time}")
    mel.eval(f"FBXExportBakeComplexEnd -v {max_time}")
    mel.eval("FBXExportConstraints -v true")
    mel.eval("FBXExportSkeletonDefinitions -v true")
    mel.eval("FBXExportInputConnections -v true")
    mel.eval("FBXExportSmoothingGroups -v true")
    mel.eval("FBXExportSkins -v true")
    mel.eval("FBXExportShapes -v true")
    mel.eval("FBXExportCameras -v false")
    mel.eval("FBXExportLights -v false")
    cmds.FBXExportUpAxis(orientation)
    # Deselects objects in Maya
    cmds.select(clear=True)


def create_shader(name):
    cmds.shadingNode("blinn", asShader=True, name=name)

    shading_group = str(
        cmds.sets(
            renderable=True,
            noSurfaceShader=True,
            empty=True,
            name=f"{name}SG",
        )
    )
    cmds.connectAttr(f"{name}.outColor", f"{shading_group}.surfaceShader")
    return shading_group


def add_shader(lod):
    for shader_name, meshes in MESH_SHADER_MAPPING.items():
        shading_group = create_shader(shader_name)
        for mesh in meshes:
            if f"lod{lod}" in mesh:
                try:
                    cmds.select(mesh, replace=True)
                    cmds.sets(edit=True, forceElement=shading_group)
                except Exception as e:
                    print(f"Skipped adding shader for mesh {mesh}. Reason {e}")


def set_vertex_color(lod):
    for m, mesh_name in enumerate(VTX_COLOR_MESHES):
        try:
            if f"lod{lod}" in mesh_name:
                cmds.select(mesh_name)
                for v, rgb in enumerate(VTX_COLOR_VALUES[m]):
                    cmds.polyColorPerVertex(f"{mesh_name}.vtx[{v}]", g=rgb[1], b=rgb[2])
        except Exception as e:
            print(f"Skipped adding vtx color for mesh {mesh_name}. Reason {e}")
            continue


def export_fbx(lod_num, meshes, root_jnt, chr_name, fbx_dir):
    # Selects every mesh in the given lod
    for item in meshes:
        cmds.select(item, add=True)
    # Adds facial root joint to selection
    cmds.select(root_jnt, add=True)
    # Sets the file path
    export_file_name = f"{fbx_dir}/{chr_name}_lod{lod_num}.fbx"
    # Exports the fbx
    mel.eval(f'FBXExport -f "{export_file_name}" -s true')


def export_fbx_for_lod(dna, lod, add_vtx_color, chr_name, body_file, fbx_dir, neck_joints, root_joint, fbx_root_jnt,
                       facial_root_joints, orientation):
    # Creates the meshes for the given lod
    result = build_meshes_for_lod(dna, lod)
    meshes = result.get_all_meshes()
    # Executes FBX relate commands from the imported plugin
    create_head_and_body_scene(meshes, body_file, neck_joints, root_joint, facial_root_joints)
    set_fbx_options(orientation)
    # Saves the result
    if add_vtx_color:
        add_shader(lod)
        set_vertex_color(lod)
    export_fbx(lod, meshes, fbx_root_jnt, chr_name, fbx_dir)

# ---------------------------
all_meta_ctrls = ['CTRL_L_nose',
 'CTRL_R_brow_down',
 'CTRL_L_mouth_lipSticky',
 'CTRL_L_mouth_funnelU',
 'CTRL_R_mouth_stickyInnerU',
 'CTRL_L_mouth_lipsTowardsTeethD',
 'CTRL_L_eye_cheekRaise',
 'CTRL_L_mouth_sharpCornerPull',
 'CTRL_R_mouth_cornerSharpnessU',
 'CTRL_R_mouth_lipsBlow',
 'CTRL_R_eye_eyelidD',
 'CTRL_R_mouth_pushPullU',
 'CTRL_C_eye_parallelLook',
 'CTRL_R_jaw_ChinRaiseD',
 'CTRL_L_mouth_towardsU',
 'CTRL_L_mouth_lipBiteD',
 'CTRL_R_mouth_cornerSharpnessD',
 'CTRL_C_tongue',
 'CTRL_L_mouth_pushPullD',
 'CTRL_C_mouth_lipShiftU',
 'CTRL_L_eye_eyelidD',
 'CTRL_C_teethU',
 'CTRL_L_eyelashes_tweakerOut',
 'CTRL_faceTweakersGUI',
 'CTRL_L_mouth_stretchLipsClose',
 'CTRL_C_neck_swallow',
 'CTRL_R_mouth_lipsRollU',
 'CTRL_R_mouth_suckBlow',
 'CTRL_L_mouth_pressU',
 'CTRL_R_eye_blink',
 'CTRL_R_eye_eyelidU',
 'CTRL_L_jaw_chinCompress',
 'CTRL_R_mouth_lipsTowardsTeethU',
 'CTRL_L_mouth_cornerPull',
 'CTRL_L_brow_raiseIn',
 'CTRL_L_mouth_suckBlow',
 'CTRL_L_mouth_lipsTogetherD',
 'CTRL_C_tongue_tip',
 'CTRL_R_ear_up',
 'CTRL_R_mouth_lipsRollD',
 'CTRL_R_neck_stretch',
 'CTRL_L_eye_squintInner',
 'CTRL_R_mouth_pushPullD',
 'CTRL_L_mouth_lipsTogetherU',
 'CTRL_R_mouth_cornerDepress',
 'CTRL_L_mouth_purseU',
 'CTRL_R_jaw_clench',
 'CTRL_L_mouth_upperLipRaise',
 'CTRL_L_mouth_cornerSharpnessU',
 'CTRL_R_mouth_thicknessD',
 'CTRL_eyesAimFollowHead',
 'CTRL_R_mouth_funnelU',
 'CTRL_rigLogicSwitch',
 'CTRL_L_neck_stretch',
 'CTRL_L_brow_lateral',
 'CTRL_C_mouth_stickyD',
 'CTRL_R_eyelashes_tweakerOut',
 'CTRL_L_mouth_lipsTowardsTeethU',
 'CTRL_L_mouth_lowerLipDepress',
 'CTRL_L_mouth_tightenU',
 'CTRL_R_mouth_purseU',
 'CTRL_L_mouth_pushPullU',
 'CTRL_R_mouth_lipBiteU',
 'CTRL_R_eye_pupil',
 'CTRL_C_tongue_press',
 'CTRL_R_mouth_towardsD',
 'CTRL_R_eye',
 'CTRL_C_teethD',
 'CTRL_L_mouth_lipBiteU',
 'CTRL_C_jaw',
 'CTRL_L_ear_up',
 'CTRL_L_brow_raiseOut',
 'CTRL_C_mouth_lipShiftD',
 'CTRL_lookAtSwitch',
 'CTRL_R_mouth_purseD',
 'CTRL_L_mouth_stickyOuterD',
 'CTRL_L_eye_blink',
 'CTRL_L_mouth_cornerSharpnessD',
 'CTRL_R_mouth_tightenU',
 'CTRL_L_eye_eyelidU',
 'CTRL_L_mouth_cornerDepress',
 'CTRL_C_tongue_roll',
 'CTRL_L_mouth_stickyInnerU',
 'CTRL_L_mouth_towardsD',
 'CTRL_C_jaw_fwdBack',
 'CTRL_R_eye_lidPress',
 'CTRL_C_teeth_fwdBackD',
 'CTRL_L_mouth_lipsPressU',
 'CTRL_R_mouth_funnelD',
 'CTRL_L_mouth_stickyOuterU',
 'CTRL_C_tongue_narrowWide',
 'CTRL_L_mouth_funnelD',
 'CTRL_R_mouth_tightenD',
 'CTRL_R_mouth_sharpCornerPull',
 'CTRL_L_mouth_lipsRollD',
 'CTRL_R_mouth_stickyInnerD',
 'CTRL_L_eye_pupil',
 'CTRL_R_mouth_corner',
 'CTRL_L_jaw_clench',
 'CTRL_L_mouth_thicknessU',
 'CTRL_R_eye_squintInner',
 'CTRL_C_eye',
 'CTRL_R_nose_nasolabialDeepen',
 'CTRL_R_eye_faceScrunch',
 'CTRL_R_mouth_upperLipRaise',
 'CTRL_L_mouth_stickyInnerD',
 'CTRL_L_mouth_dimple',
 'CTRL_L_eyelashes_tweakerIn',
 'CTRL_faceGUIfollowHead',
 'CTRL_neck_throatExhaleInhale',
 'CTRL_R_mouth_lipsTogetherD',
 'CTRL_R_jaw_ChinRaiseU',
 'CTRL_L_mouth_purseD',
 'CTRL_C_mouth_stickyU',
 'CTRL_L_eye_faceScrunch',
 'CTRL_R_mouth_lipsTowardsTeethD',
 'CTRL_R_brow_raiseOut',
 'CTRL_R_mouth_lipsPressU',
 'CTRL_R_mouth_dimple',
 'CTRL_R_mouth_thicknessU',
 'CTRL_R_neck_mastoidContract',
 'CTRL_C_tongue_inOut',
 'CTRL_C_mouth',
 'CTRL_R_brow_lateral',
 'CTRL_R_mouth_lowerLipDepress',
 'CTRL_R_mouth_lipSticky',
 'CTRL_L_jaw_ChinRaiseU',
 'CTRL_L_mouth_stretch',
 'CTRL_R_mouth_stickyOuterD',
 'CTRL_L_jaw_ChinRaiseD',
 'CTRL_R_nose',
 'CTRL_R_mouth_lipBiteD',
 'CTRL_R_mouth_lipsTogetherU',
 'CTRL_R_mouth_towardsU',
 'CTRL_R_jaw_chinCompress',
 'CTRL_C_jaw_openExtreme',
 'CTRL_R_mouth_pressD',
 'CTRL_L_eye',
 'CTRL_R_nose_wrinkleUpper',
 'CTRL_L_brow_down',
 'CTRL_L_mouth_lipsRollU',
 'CTRL_L_nose_nasolabialDeepen',
 'CTRL_L_mouth_tightenD',
 'CTRL_L_neck_mastoidContract',
 'CTRL_C_teeth_fwdBackU',
 'CTRL_neck_throatUpDown',
 'CTRL_R_eye_cheekRaise',
 'CTRL_L_mouth_lipsBlow',
 'CTRL_R_mouth_stretch',
 'CTRL_R_mouth_stretchLipsClose',
 'CTRL_L_mouth_corner',
 'CTRL_L_mouth_pressD',
 'CTRL_L_mouth_thicknessD',
 'CTRL_L_nose_wrinkleUpper',
 'CTRL_R_mouth_cornerPull',
 'CTRL_L_eye_lidPress',
 'CTRL_faceGUI',
 'CTRL_R_mouth_stickyOuterU',
 'CTRL_R_brow_raiseIn',
 'CTRL_R_eyelashes_tweakerIn',
 'CTRL_neck_digastricUpDown',
 'CTRL_R_mouth_pressU']