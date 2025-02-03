from __future__ import absolute_import
try:
    import importlib;from importlib import reload
except:
    import imp;from imp import reload
import maya.cmds as cmds
import maya.mel as mel
import sys 
import os
import platform
import subprocess
import Mutant_Tools.Utils.Crowds.Facial.poses_to_sdk as p2sdk
reload(p2sdk)
import Mutant_Tools.Utils.Crowds.Facial.eyelids_local2crowd as eye2crowd
reload(eye2crowd)



class DemBonesManager(object):
    DEMBONES_DIR = 'dembones'

    ALEMBIC_DIR = 'alembic'
    FBX_DIR = 'fbx'
    OUTPUT_DIR = 'output'

    PROJECT_DIR = ''

    @classmethod
    def set_current_project_dir(cls):
        cls.PROJECT_DIR = cmds.workspace(query=1, rootDirectory=True)

    @classmethod
    def is_dembones_dir_valid(cls):
        target_path = os.path.join(cls.PROJECT_DIR, cls.DEMBONES_DIR)
        alembic_path = os.path.join(cls.PROJECT_DIR, cls.DEMBONES_DIR)
        fbx_path = os.path.join(cls.PROJECT_DIR, cls.DEMBONES_DIR)
        output_path = os.path.join(cls.PROJECT_DIR, cls.DEMBONES_DIR)
        return os.path.exists(target_path) and os.path.exists(alembic_path) and os.path.exists(fbx_path) and os.path.exists(output_path)

    @classmethod
    def initialize_directories(cls):
        try:
            cls.set_current_project_dir()
            
            target_path = os.path.join(cls.PROJECT_DIR, cls.DEMBONES_DIR)
            os.mkdir(target_path)

            alembic_path = os.path.join(target_path, cls.ALEMBIC_DIR)
            fbx_path = os.path.join(target_path, cls.FBX_DIR)
            output_path = os.path.join(target_path, cls.OUTPUT_DIR)

            os.mkdir(alembic_path)
            os.mkdir(fbx_path)
            os.mkdir(output_path)

        except Exception as e:
            print(e)

    @classmethod
    def export_alembic(cls, start_frame, end_frame, target_geometry):
        cmds.loadPlugin('AbcExport', quiet=1)
        file = os.path.join(cls.PROJECT_DIR, cls.DEMBONES_DIR, cls.ALEMBIC_DIR, target_geometry.split('|')[-1] + '.abc')
        job_arg = "-root {} -file {} -frameRange {} {}".format(target_geometry, file, start_frame, end_frame)
        cmds.AbcExport(j=job_arg)
        return file
    
    @classmethod
    def export_fbx(cls, reference_frame, target_geometry):
        cmds.loadPlugin('fbxmaya', quiet=1)
        file = os.path.join(cls.PROJECT_DIR, cls.DEMBONES_DIR, cls.FBX_DIR, target_geometry.split('|')[-1] + '.fbx')
        cmds.currentTime(reference_frame)
        # TODO: change to export just target_geometry
        #mel.eval('FBXExportInputConnections -v false')
        #mel.eval('FBXExport -f "{}.fbx" -s'.format(file))
        cmds.select(clear=1)
        cmds.select(target_geometry)
        cmds.file(file, force=1, options="v=0;", type="FBX export", es=1, ch=0)
        #file -force -options "v=0;" -typ "FBX export" -pr -es 
        return file

    @classmethod
    def generate_output(cls, target_geometry):

        cls.set_current_project_dir()

        if not cls.is_dembones_dir_valid():
            cls.initialize_directories()

        start_frame = cmds.playbackOptions(query=True, minTime=True)
        ctrls = cmds.ls("*_Ctrl")
        end_frame = cmds.findKeyframe(ctrls, which='last')
        cmds.playbackOptions(max=end_frame)

        if not cmds.objExists(target_geometry):
            cmds.error('{} does not exist'.format(target_geometry))
            return

        alembic = cls.export_alembic(start_frame, end_frame, target_geometry)
        fbx = cls.export_fbx(start_frame, target_geometry)

        output_file = os.path.join(cls.PROJECT_DIR, cls.DEMBONES_DIR, cls.OUTPUT_DIR,
                                   target_geometry.split('|')[-1] + '.fbx')

        script_dir = os.path.dirname(os.path.abspath(__file__))

        # Platform-specific setup
        if platform.system() == "Linux":
            dembones_cmd = "DemBones"  # Assuming it's in the default path
        elif platform.system() == "Windows":
            dembones_dir = 'C:\\Users\\rodri\\Documents\\maya\\2024\\scripts\\rigging\\Mutant_Tools\\Utils\\External\\DemBones\\bin\\Windows'
            dembones_cmd = os.path.join(dembones_dir, "DemBones.exe")
        else:
            raise RuntimeError("Unsupported operating system")

        output_file = os.path.join(cls.PROJECT_DIR, cls.DEMBONES_DIR, cls.OUTPUT_DIR,
                                   target_geometry.split('|')[-1] + '.fbx')
        amount = 69
        cmd = [dembones_cmd, "-a={}".format(alembic), "-i={}".format(fbx), "-o={}".format(output_file), "-b={}".format(amount)]
        #cmd = [dembones_cmd, "-a={}".format(alembic), "-i={}".format(fbx), "-o={}".format(output_file), "-b=100", "--weightsSmooth=0.5", "-n=100", "--tolerance=0.001", "--patience=10"]

        print(cmd)

        try:
            result = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
            print("DemBones output = {}".format(result.decode()))
        except subprocess.CalledProcessError as e:
            print("DemBones failed with error code {}: {}".format(e.returncode, e.output.decode()))

        return

    @classmethod
    def import_dembones_output(cls):

        cls.set_current_project_dir()

        if not cls.is_dembones_dir_valid():
            cls.initialize_directories()

        mel.eval("FBXImportMode -v add")
        namespace = 'Dembones'
        dembones_output_dir = os.path.join(cls.PROJECT_DIR, cls.DEMBONES_DIR, cls.OUTPUT_DIR)
        output_file = os.listdir(dembones_output_dir)[0]
        
        cmds.file(os.path.join(dembones_output_dir, output_file), i=True, type="FBX", ra=True, namespace=namespace)

        dembones_joints = cmds.ls('{}:*'.format(namespace), type='joint')
        for index, joint in enumerate(dembones_joints):
            dembones_joints[index] = cmds.rename(joint, joint.replace("joint", "DemJoint_"))

        #grp_dembones_joints = cmds.group(dembones_joints, n="DemJoints_GRP")
        cmds.select(clear=1)
        dembones_root_joint = cmds.joint(n="{}:root".format(namespace))
        cmds.parent(dembones_joints, dembones_root_joint)
        cmds.parent(dembones_root_joint, 'Head_Skl')


        mesh_dembones = cmds.ls("{}:*".format(namespace), type='mesh')
        mesh_dembones = cmds.listRelatives(mesh_dembones, p=1)[0]
        root_geo_dembones = cmds.ls("{}:*".format(namespace), assemblies=1)
        #print("Root Dembones = {}".format(root_geo_dembones))

        #cmds.group(grp_dembones_joints, mesh_dembones, n='DemBones_GRP')
        cmds.parent(mesh_dembones, w=True)
        
        #cmds.parent(grp_dembones_joints, 'Head_Skl')

        cmds.delete(root_geo_dembones)




    @classmethod
    def connect_ctrls_2_dembones(cls):
        dem_joints = cmds.ls("Dembones:*", type='joint')
        p2sdk.connect_Face_SDK(dem_joints=dem_joints)
        cmds.select("*_Ctrl")
        cmds.cutKey(clear=1)
        cmds.select(clear=1)

        if cmds.objExists('Mutant_Tools_Grp'):
            eye_joints = cmds.ls("*Eyelids*Bnd")
            eye2crowd.dup_joints(eye_joints, 'Head_Skl')
            eye2crowd.eyelids_crowd()
        elif cmds.objExists('eyeHead'):
            eye2crowd.create_global_eye_rig_bardel('eyeHead')

            
    