from __future__ import absolute_import
'''
version: 1.0.0
date: 21/04/2020

#----------------
content:

#----------------
how to:

try:
    import importlib;from importlib import reload
except:
    import imp;from imp import reload

import Mutant_Tools
from Mutant_Tools.UI.GamesCrowds.crowd_uttils import crowds_combo_utils
reload(crowds_combo_utils)

cCrowdsCombo = crowds_combo_utils.CrowdsCombo()


#----------------
dependencies:

Main Mutant

#----------------
licence: https://www.eulatemplate.com/live.php?token=FGISW7ApRfgywum6murbBmLcusKONzkv
author:  Esteban Rodriguez <info@renderdemartes.com>

'''
# -------------------------------------------------------------------

from maya import cmds
import tempfile
import pprint
import glob
import os
from collections import OrderedDict

try:
    from star.entities import Project
    from mstar.nodes.sid import Sid
except:
    pass

try:
    import importlib;from importlib import reload
except:
    import imp;from imp import reload

import Mutant_Tools
import Mutant_Tools.Utils.IO
from Mutant_Tools.Utils.IO import EasySkin
reload(Mutant_Tools.Utils.IO.EasySkin)


class CrowdsCombo(object):
    """
    A class for managing crowd combo information.

    Attributes:
        show (str): The name of the show associated with this CrowdsCombo instance.
        all_asset_objects (list): A list of all asset objects related to the show.
        kind (str): A string representing the kind of CrowdsCombo instance ('crwdrig-hi' by default).
    """
    def __init__(self, show=None):
        """
        Initializes a new CrowdsCombo instance.

        Args:
            show (str, optional): The name of the show to associate with this CrowdsCombo instance.

        Note:
            If 'show' != provided, 'all_asset_objects' will remain None until set later.
        """

        self.show = show
        self.all_asset_objects = self.get_all_assets() 
        self.kind = 'crwdrig-hi'
    
    def get_all_assets(self):
        """
        Retrieves all assets associated with the specified show.

        Returns:
            list: A list of asset objects related to the show. Returns an empty list if 'show' is None.

        Note:
            This method requires 'show' to be set to a valid show name. 
            It uses the Project class to find and retrieve the associated assets.
        """

        if not self.show:
            return        

        proj = Project.findby_name(self.show)
        assets=[]

        for ass in proj.assets:
            assets.append(ass)

        return assets
    
    def find_asset_path(self, asset_name):
        """
        Find the file path for a specific asset.

        Args:
            asset_name (str): The name of the asset to find.

        Returns:
            str or False: The file path to the Maya file for the specified asset, or False if not found.

        Note:
            This method searches for the asset in 'all_asset_objects' and returns the Maya file path
            based on certain conditions.
        """

        asset_object = None
        for ass in self.all_asset_objects:
            if ass.name == asset_name:
                asset_object = ass
                break
        
        if not asset_object:
            return False
    
        pubs = asset_object.publishes
        if not pubs:
            return False
        
        path = None
        pref=None
        latest=None
        for pub in pubs:
            if pub.kind.name == self.kind:
                versions = pub.versions
                if not versions:
                    return False
                for version in versions:
                    if version.is_latest:
                        latest = version.root
                    if version.status == 'prf':
                        pref = version.root

        if not pref:
            maya_file = glob.glob(os.path.join(latest, '*.ma'))[0]
        else:
            maya_file = glob.glob(os.path.join(pref, '*.ma'))[0]

        return maya_file
                        

    def create_combo_rig(self, paths=[], asset=None):
        """
        Create a combo rig by importing and processing multiple Maya files.

        Args:
            paths (list): List of file paths to the Maya files for combo rig creation.
            asset (str): The name of the main asset to be created.

        Returns:
            bool: True if the combo rig is successfully created, False otherwise.

        Note:
            This method imports and processes Maya files, creates a main asset, imports joint hierarchies,
            loads skin data, connects controls, and organizes the combo rig.

            If 'paths' != provided or empty, the method returns False.
        """

        #test mode
        #paths = paths[:2]

        if not paths:
            return False

        #Prepare
        files_data = OrderedDict()
        first_rig=True
        for path in paths:
            data = self.prepare_crowd_rig(path, is_main=first_rig)
            files_data[path] = data
            first_rig=False

        pprint.pprint(files_data)

        #create main asset
        cmds.file(new=True, f=True)
        combined_sid = self.create_sid_node(asset)

        #Import and reparent
        for path in files_data:
            print(path)
            print(files_data)
            first_rig = files_data[path]['is_main']
            print('Importing:', files_data[path]['temp_file'], files_data[path]['asset'])
            
            file_asset = files_data[path]['asset']
            ns=file_asset
            cmds.file(files_data[path]['temp_file'], i=True ,f=True, ns=ns)

            #reparent joints
            for jnt in files_data[path]['skl_joints']:
                parent = files_data[path]['skl_joints'][jnt]['parent']
                print(jnt, parent)
                try:
                    cmds.parent('{}:{}'.format(file_asset, jnt), 
                                '{}'.format(parent))
                except:
                    cmds.parent('{}:{}'.format(file_asset, jnt), 
                                '{}:{}'.format(file_asset, parent))
            


            #Load skin
            print(files_data[path]['skin_folder'])
            if first_rig:
                namespace=False
                avoid_rename=[]
            else:
                namespace=file_asset
                avoid_rename=common_skl_skeleton
            EasySkin.load_all_skins_from(folder_path=files_data[path]['skin_folder'],
                                         accept_errors=False,
                                         namespace=namespace,
                                         avoid_rename=avoid_rename)
            
            

            #If not first rig connect ctrls
            if not first_rig:
                for ctrl in files_data[path]['ctrls']:
                    master_ctrl = ctrl.split(':')[0]
                    if cmds.objExists(master_ctrl) and cmds.objExists('{}:{}'.format(file_asset, ctrl)):
                        attrs = cmds.listAttr(ctrl, ud=True)
                        if not attrs:
                            continue
                        for attr in attrs + ['translate','rotate','scale']:
                            print(ctrl, attr)
                            print('{}:{}.{}'.format(file_asset, ctrl, attr))
                            if cmds.attributeQuery(attr, node=ctrl, exists=True) and cmds.attributeQuery(attr, node='{}:{}'.format(file_asset, ctrl), exists=True):
                                if  not cmds.getAttr('{}:{}.{}'.format(file_asset, ctrl, attr), l=True):
                                    cmds.connectAttr('{}.{}'.format(master_ctrl, attr), '{}:{}.{}'.format(file_asset, ctrl, attr), f=True)
                            
                                    
            #reparent to one sid node
            

            #if first remove namespaces
            if first_rig:
                self.delete_namespaces()
                
                geo_grp = 'geo'

                sid_groups = cmds.listRelatives(file_asset, c=True)
                cmds.parent(sid_groups, combined_sid)
                cmds.delete(file_asset)
                self.add_geo_to_namespace(geos=cmds.listRelatives(geo_grp, ad=True), namespace=file_asset)

            first_rig=False

        #create common grps
        self.create_extra_grp()


        pprint.pprint(files_data)


    def prepare_crowd_rig(self, path, is_main=False):
        """
        Prepare a crowd rig for processing.

        Args:
            path (str): The file path to the Maya file containing the crowd rig.
            is_main (bool, optional): Indicates if the crowd rig is the main rig (default is False).

        Returns:
            dict: A dictionary containing information about the prepared crowd rig, including skeleton joints,
                  skin folder path, temporary file path, asset name, tagged controls, and whether it's the main rig.

        Note:
            This method imports and processes a Maya file, extracts skeleton joints, saves temporary skin data,
            and collects information about the crowd rig.

            If 'is_main' is True, common skeleton joints will be deleted.
        """

        cmds.file(new=True, f=True)
        cmds.file(path, i=True, f=True)
        
        asset = self.get_asset_name()

        skl_joints = []
        skin_folder = ''

        self.delete_namespaces()
        self.update_face_joints_names(asset)
        skl_joints = self.get_diference_with_common_skl()
        skin_folder = self.save_temp_skin(asset, is_main=is_main)
        ctrls = self.get_tagged_ctrls()
        print(ctrls)

        #fix dem bones root
        root=''
        for jnt in cmds.listRelatives('Head_Skl', c=True):
            if 'root' in jnt:
                root = jnt

        for attr in ['translateX','translateY','translateZ']:
            print(root, attr)
            cnc = cmds.listConnections('{}.translate.{}'.format(root, attr), p=True)[0]
            print(cnc)
            cmds.disconnectAttr(cnc, '{}.translate.{}'.format(root, attr))
        
        #unparent dif joints
        for jnt in skl_joints:
            cmds.parent(jnt, w=True)

        #delete common joints
        if not is_main:
            for jnt in common_skl_skeleton:
                if cmds.objExists(jnt):
                    cmds.delete(jnt)

        #save temp file to reimport
        temp_path = os.path.join(tempfile.gettempdir(), 'CrowdsCombo', 'Files')
        temp_file = os.path.join(temp_path, asset+'.ma')
        if not os.path.exists(temp_path):
            os.makedirs(temp_path)
        cmds.file(rename=temp_file)
        saved_temp_file = cmds.file(save=True, type="mayaAscii")



        return {'skl_joints':skl_joints,
                'skin_folder':skin_folder,
                'temp_file' : temp_file,
                'asset' : asset,
                'ctrls' : ctrls,
                'is_main' : is_main
                }
    
    def get_tagged_ctrls(self):
        """
        Get tagged control objects from the crowd rig.

        Returns:
            list: A list of control object names that have been tagged in the crowd rig.

        Note:
            This method retrieves control objects with the 'animctrl' tag from the crowd rig.
        """

        from rigSystem.assetTemplates.core import get_one_sid
        sid = get_one_sid()
        controls = sid.tag_node().get_tag_objects('animctrl')
        ctrls = []
        for ctrl in controls:
            ctrls.append(ctrl.name)

        return ctrls

    def delete_namespaces(self):
        """
        Delete all namespaces except for built-in namespaces.

        Note:
            This method removes all namespaces in the Maya scene, except for the built-in 'UI' and 'shared' namespaces.
        """

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


    def update_face_joints_names(self, asset):
        """
        Update the names of face joints with the asset name.

        Args:
            asset (str): The asset name used for renaming the face joints.

        Note:
            This method renames face joints in the 'Head_Skl' hierarchy by prefixing them with the 'asset' name.
        """
        face_joints = cmds.listRelatives('Head_Skl', ad=True, type='joint')
        for jnt in face_joints:
            cmds.rename(jnt, '{}_{}'.format(asset,jnt))


    def get_asset_name(self):
        """
        Get the asset name associated with this CrowdsCombo instance.

        Returns:
            str: The name of the asset associated with the instance.

        Note:
            This method retrieves the asset name using the 'get_one_sid' function from 'rigSystem.assetTemplates'.
        """

        from rigSystem.assetTemplates import get_hierarchy, get_one_sid
        sid = get_one_sid()
        return sid.name
         

    def get_diference_with_common_skl(self):
        """
        Get the difference between skeleton joints and common skeleton joints.

        Returns:
            dict: A dictionary containing the skeleton joints that are not common with their parent names.

        Note:
            This method finds the skeleton joints in the 'skeleton' hierarchy and identifies the ones that are not
            in the 'common_skl_skeleton' list.
        """

        skl_joints = cmds.listRelatives('skeleton', ad=True, type='joint')
        dif = {}
        for jnt in skl_joints:
            if jnt not in common_skl_skeleton:
                dif[jnt] = {'parent': cmds.listRelatives(jnt, p=True)[0]}

        return dif


    def save_temp_skin(self, asset, is_main=False):
        """
        Save temporary skin data for the crowd rig.

        Args:
            asset (str): The asset name used for creating a temporary namespace.
            is_main (bool, optional): Indicates if it's the main crowd rig (default is False).

        Returns:
            str: The path to the folder where temporary skin data is saved.

        Note:
            This method prepares and saves temporary skin data for the crowd rig, including renaming joints,
            adding namespaces, and saving selected geometries' skin weights.
        """

        self.remove_dup_names()

        temp_skin_folder = os.path.join(tempfile.gettempdir(), 'CrowdsCombo', 'Skin',asset)
        print(temp_skin_folder)
        if not os.path.exists(temp_skin_folder):
            os.makedirs(temp_skin_folder)

        #Temp rename joints
        #rename sid
        sid = cmds.rename(asset, asset+'SID')
        geos = self.find_all_geos_with_skl_skins()

        cmds.namespace(add=asset)
        if not is_main:
            
            
            skl_joints = cmds.listRelatives('skeleton', ad=True, type='joint')
            print('geos', geos)
            print('skeleton', skl_joints)
            for jnt in skl_joints:
                if jnt not in common_skl_skeleton:
                    #add namespace
                    cmds.namespace(set=asset)
                    cmds.select(jnt)
                    cmds.namespace(set=":")
                    cmds.rename(jnt, asset+':'+jnt)

            new_geos=[]
            for geo in geos:
                #add namespace
                cmds.namespace(set=asset)
                cmds.select(geo)
                cmds.namespace(set=":")
                cmds.rename(geo, asset+':'+geo)
                new_geos.append(asset+':'+geo)
            geos=new_geos

        print(geos)
        cmds.select(geos)
        EasySkin.save_selected_geos(folder_path=temp_skin_folder)

        #delete name spaces
        self.delete_namespaces()

        #delete geo history
        if not is_main:
            cmds.delete('geo', ch=True)

        #rename sid back
        cmds.rename(sid, asset)
        
        return temp_skin_folder

    def remove_dup_names(self):
        """
        Remove duplicate names in the crowd rig.

        Note:
            This method removes duplicate names in the crowd rig by appending random numbers to resolve conflicts.
        """

        from mstar.nodes.sid import Sid
        from assetChecks.projectChecks.studio.checks import CheckUniqueNames
        import random
        import maya.mel as mel

        def fix_unique_names():

            sid = Sid.find()[0]  # getting the Sid node

            # Run check:
            check = CheckUniqueNames(sid)
            result = check.run()
            for item in result.items:
                item_name = item.item
                print(item_name)
                connections=cmds.listConnections()
                if connections:
                    if 'tag' in connections:
                        continue
                real_name = item_name.split('|')[-1]
                if item_name.endswith('_Ctrl'):
                    continue
                else:
                    try:
                        print(item_name)
                        cmds.select(item_name)
                        to_rename = cmds.ls(sl=True)
                        for i in to_rename:
                            mel.eval('searchReplaceNames "{}" "{}" "selected";'.format(real_name, real_name + str(
                                random.randint(0, 100))))
                    except:
                        pass

        fix_unique_names()
        fix_unique_names()
        fix_unique_names()
    
    def find_all_geos_with_skl_skins(self):
        """
        Find all geometries with skin clusters in the crowd rig.

        Returns:
            list: A list of geometries that have skin clusters.

        Note:
            This method identifies geometries in the crowd rig that have associated skin clusters.
        """

        skins = cmds.ls(type='skinCluster')
        geos = []
        for skin in skins:
            geo = cmds.skinCluster(skin, q=True, geometry=True)[0]
            geo = cmds.listRelatives(geo, p=True)[0]
            joints = cmds.skinCluster(skin, query=True, inf=True)
            cmds.select(joints)
            joints=cmds.ls(sl=True, l=True)
            for jnt in joints:
                if 'skeleton' in jnt:
                    if geo in geos:
                        continue
                    connections=cmds.listConnections(geo)
                    if connections:
                        if 'tag' in connections:
                            geos.append(geo)
                    
        return geos

    def add_geo_to_namespace(self, geos, namespace):
        """
        Add geometries to a specified namespace.

        Args:
            geos (list): A list of geometries to be added to the namespace.
            namespace (str): The namespace to which the geometries should be added.

        Returns:
            list: A list of newly renamed geometries within the specified namespace.

        Note:
            This method adds geometries to the specified namespace and returns their new names.
        """

        cmds.namespace(add=namespace)
        pass
        new_geos = []
        for geo in geos:
            #add namespace
            cmds.namespace(set=namespace)
            cmds.select(geo)
            cmds.namespace(set=":")
            new_name = cmds.rename(geo, namespace+':'+geo)
            new_geos.append(new_name)

        return new_geos


    def create_sid_node(self, asset):
        """
        Create a SID node for the specified asset.

        Args:
            asset (str): The name of the asset for which to create a SID node.

        Returns:
            object: The created SID node.

        Note:
            This method creates a SID node for the specified asset, locks certain transformation attributes,
            and associates it with the asset and task.
        """

        print(self.show, asset)
        # Create sid node
        def lock_sid(sid_node):
            for oneAttr in ['tx', 'ty', 'tz', 'rx', 'ry', 'rz', 'sx', 'sy', 'sz']:
                cmds.setAttr('{}.{}'.format(sid_node.name, oneAttr), lock=True, k=False)

        asset_object=None
        for ass in self.all_asset_objects:
            if ass.name==asset:
                asset_object = ass
                break
        if not asset_object:
            cmds.error('Not asset found')

        sid = Sid.create('AsgardianMaleCombined')
        lock_sid(sid)
        #sid.create_default_groups(kind='crwdrig-hi')

        tasks = ['Crowd_Rig']
        for task in asset_object.tasks:
            if str(task.name) in tasks:
                rig_task = task

        sid.tag(entity=asset_object,
                        task=rig_task,
                            type='char',
                            publish_kind='crwdrig-hi'
                            )
                                    
        return sid

    def create_extra_grp(self):
        """
        Create additional groups for organizing geometries.

        Note:
            This method creates additional groups for organizing different types of geometries
            within the crowd rig hierarchy.
        """

        geo_grps = ['shared_geo','swappable_geo','props']
        swapable_grps = ['Heads_grp','Hairs_grp','Shirts_grp','Pants_grp','Bodies_grp','BubbleMan_Grp']

        for grp in geo_grps:
            grp = cmds.group(em=True, n=grp)
            cmds.parent(grp, 'geo')

        for grp in swapable_grps:
            grp = cmds.group(em=True, n=grp)
            cmds.parent(grp, 'swappable_geo')



common_skl_skeleton = [

#u'Head_End_Skl',
 #u'Head_Skl',
 u'Hips_Skl',
 u'Jaw_Skl',
 u'LeftArm_Roll_Skl',
 u'LeftArm_Skl',
 u'LeftEye_Skl',
 u'LeftFoot_Skl',
 u'LeftForeArm_Roll_Skl',
 u'LeftForeArm_Skl',
 u'LeftHandIndex1_Skl',
 u'LeftHandIndex2_Skl',
 u'LeftHandIndex3_Skl',
 u'LeftHandIndex4_Skl',
 u'LeftHandMiddle1_Skl',
 u'LeftHandMiddle2_Skl',
 u'LeftHandMiddle3_Skl',
 u'LeftHandMiddle4_Skl',
 u'LeftHandPinky1_Skl',
 u'LeftHandPinky2_Skl',
 u'LeftHandPinky3_Skl',
 u'LeftHandPinky4_Skl',
 u'LeftHandRing1_Skl',
 u'LeftHandRing2_Skl',
 u'LeftHandRing3_Skl',
 u'LeftHandRing4_Skl',
 u'LeftHandThumb1_Skl',
 u'LeftHandThumb2_Skl',
 u'LeftHandThumb3_Skl',
 u'LeftHandThumb4_Skl',
 u'LeftHand_Skl',
 u'LeftLeg_Skl',
 u'LeftShoulder_Skl',
 u'LeftToeBase_Skl',
 u'LeftToeEnd_Skl',
 u'LeftUpLeg_Skl',
 u'Neck1_Skl',
 u'Neck_Skl',
 u'RightArm_Roll_Skl',
 u'RightArm_Skl',
 u'RightEye_Skl',
 u'RightFoot_Skl',
 u'RightForeArm_Roll_Skl',
 u'RightForeArm_Skl',
 u'RightHandIndex1_Skl',
 u'RightHandIndex2_Skl',
 u'RightHandIndex3_Skl',
 u'RightHandIndex4_Skl',
 u'RightHandMiddle1_Skl',
 u'RightHandMiddle2_Skl',
 u'RightHandMiddle3_Skl',
 u'RightHandMiddle4_Skl',
 u'RightHandPinky1_Skl',
 u'RightHandPinky2_Skl',
 u'RightHandPinky3_Skl',
 u'RightHandPinky4_Skl',
 u'RightHandRing1_Skl',
 u'RightHandRing2_Skl',
 u'RightHandRing3_Skl',
 u'RightHandRing4_Skl',
 u'RightHandThumb1_Skl',
 u'RightHandThumb2_Skl',
 u'RightHandThumb3_Skl',
 u'RightHandThumb4_Skl',
 u'RightHand_Skl',
 u'RightLeg_Skl',
 u'RightShoulder_Skl',
 u'RightToeBase_Skl',
 u'RightToeEnd_Skl',
 u'RightUpLeg_Skl',
 u'Spine1_Skl',
 u'Spine2_Skl',
 u'SpineHolder_Skl',
 u'Spine_Skl'
]