from __future__ import absolute_import
'''
version: 1.0.0
date: 21/04/2020

#----------------

how to:
try:
    import importlib;from importlib import reload
except:
    import imp;from imp import reload

import Mutant_Tools
import Mutant_Tools.Utils.IO
from Mutant_Tools.Utils.IO import SkinUtils
reload(Mutant_Tools.Utils.IO.SkinUtils)


skin = SkinUtils.Skinning()
skin.FUNC_NAME(argument = '')

#save
skin = SkinUtils.Skinning()
data = skin.get_weights('WrapBaseMesh')
skin.save(data=data)

#load
skin = SkinUtils.Skinning()
data = skin.load_data(path='C://Users//info//Documents//maya//2022//scripts//rigging//Mutant_Tools//Utils//Wrap//Skins//WrapBaseMesh.json')
skin.set_weights(all_data=data, geometry='WrapBaseMesh', remove_unused=True)


#----------------
dependencies:

#----------------
licence: https://www.eulatemplate.com/live.php?token=FGISW7ApRfgywum6murbBmLcusKONzkv
author:  Esteban Rodriguez <info@mutanttools.com>

'''
import six
import os
import json
try:
    import importlib;from importlib import reload
except:
    import imp;from imp import reload

import operator
from maya import cmds, OpenMaya
import maya.OpenMayaAnim as oma

import maya.OpenMaya as om
import Mutant_Tools
import maya.mel as mel
from pathlib import Path
from collections import OrderedDict
from Mutant_Tools.Utils.External.mayaNode import MayaNode
from Mutant_Tools.Utils.External.geoNode import GeoNode

from Mutant_Tools.Utils.Helpers import helpers
reload(Mutant_Tools.Utils.Helpers.helpers)
mh = helpers.Helpers()

#Read name conventions as nc[''] and setup as seup['']
PATH = os.path.dirname(__file__)
PATH = Path(PATH)
PATH_PARTS = PATH.parts[:-2]
FOLDER=''
for f in PATH_PARTS:
    FOLDER = os.path.join(FOLDER, f)

JSON_FILE = os.path.join(FOLDER, 'config', 'name_conventions.json')
with open(JSON_FILE) as json_file:
    nc = json.load(json_file)

COUNT_KEY = 'count'
INFLUENCE_KEY = 'influences'
WEIGHT_KEY = 'weights'
GEO_KEY = 'geo'

#----------------------------------------------------------

class Skinning(MayaNode):

    def __init__(self):

        self.bind_joints = cmds.ls('*{}'.format(nc['joint_bind']))
        self.skin_nodes = cmds.ls('*{}'.format(nc['skin_cluster']))

        self.mfn_skin = None
        self.end_message = ''

    # ----------------------------------------------------------
    def update_properties(self):
        self.bind_joints = cmds.ls('*{}'.format(nc['joint_bind']))
        self.skin_nodes = cmds.ls('*{}'.format(nc['skin_cluster']))

    # ----------------------------------------------------------

    def bind_to_bnd(self, geo=None):

        if geo is None:
            geo = cmds.ls(sl=True)

        self.update_properties()
        try: mel.eval('doDetachSkin "2" { "1","1" };')
        except: pass
        skin = self.bind_skin(joints=self.bind_joints, geo=geo)
        return skin

    # ----------------------------------------------------------

    def deformable_dual_quaternion(self, skin = None):
        if skin == None:
            skin = cmds.ls(sl=True)

        try:
            cmds.setAttr('{}.skinningMethod'.format(skin), 1)
            cmds.setAttr('{}.dqsSupportNonRigid'.format(skin), 1)
        except:
            cmds.warning('No skin selected.')

    # ----------------------------------------------------------

    def get_skins(self):
        return cmds.ls(typ='skinCluster')

    # ----------------------------------------------------------
    def get_all_geo_with_skin(self):

        skinned_geos = []
        skins = self.get_skins()
        shapes = set(sum([cmds.skinCluster(c, q=1, g=1) for c in skins], []))
        for s in shapes:
            if cmds.nodeType(s) == 'mesh':
                transform_node = cmds.listRelatives(s, p=True)
                if transform_node:
                    skinned_geos.append(transform_node[0])

        return skinned_geos

    # ----------------------------------------------------------

    def rename_skin_clusters(self, input):
        return cmds.rename(input, input + nc['skin_cluster'])

    #----------------------------------------------------------

    def bind_skin(self, joints=None, geo=None):

        if joints == None:
            joints = self.bind_joints
        if geo == None:
            geo = cmds.ls(sl=True)

        if  not type(geo) == 'list':
            geo = [geo]

        for transform in geo:
            if cmds.nodeType(transform) == 'transform':
                cmds.select(joints,transform)
                skin = cmds.skinCluster(toSelectedBones=True)[0]
                skin=cmds.rename(skin, '{}{}'.format(transform, nc['skin_cluster']))
                self.deformable_dual_quaternion(skin=skin)

        return skin

    #----------------------------------------------------------

    def soft_select_skin_pass(self, expand=3, falloff=0.35, curve="0.80303,0,1,0,0.506024,1", mode=1, mesh=None, joint_dict=None, mirror=False, vertex_dict=False):
        """
        Assigns first Pass skin weights from joint to the soft select selection of the closest vertex on the mesh.
        Call example: mesh=(mesh's name as string), joint_dict(provided as a joint set):
            try:
                import importlib;from importlib import reload
            except:
                import imp;from imp import reload

            import Mutant_Tools
            from Mutant_Tools.Utils.IO import SkinUtils
            reload(SkinUtils)
            skinning = SkinUtils.Skinning()
            data = skinning.soft_select_skin_pass(mirror=True,  mesh='Local_EyeLids', joint_dict=cmds.ls(sl=True))
        Args:
            expand (int): Number of neighbouring vertices to include in the select (avoids vertices in the closestVert function)
            falloff(int): Radius value for skin assignment
            curve(string): In thruple order, first number is the point order, then x and y.
            mode (int): 0 - volume, 1 - surface, 2 - global
            mesh (string): Name of the geo
            joint_dict(list): Joints to be skinned (must match order with vertex)
            mirror (bool): Will apply a closestComponent, closestJoint skin mirror to the skinCluster
            vertexDict (bool): if vertex selection not provided, will try to get closest vertex
        """

        selectionVrts = self._create_joint_vertex_dict(mesh, joint_dict, vertex_dict=vertex_dict)
        allVerts = []

        if selectionVrts:

            #----------------------- Skin Cluster logic to define if it exists
            print("Starting auto-skinning.")
            for pair in selectionVrts:
                string = pair.split(':')
                jnt = string[0]
                vrtx = string[1]
                allVerts.append(vrtx)

            for pair in selectionVrts:
                #-------sdefine what is what
                string = pair.split(':')
                jnt = string[0]
                vrtx = string[1]
                cmds.select(vrtx)
                self._expand_selection(cycles=expand, my_Vert=vrtx, closest_verts=allVerts)

                #------- soft selection turn on and then access the info from OpenMaya
                cmds.softSelect(sse=True, ssd=falloff, ssf=mode, ssc=curve)
                softElementData = self._softSelection()
                selection = ["%s.vtx[%d]" % (el[0], el[1])for el in softElementData ]
                #print ('Pair on {jnt} is {sel}'.format(jnt=jnt, sel= selection))

                #-------- skinCLuster retrieval and make sure joints are bound
                model = softElementData[0]
                cluster = cmds.ls(cmds.listHistory(model[0]), type='skinCluster')
                if len(cluster) == 0:
                    print("No Skin Cluster found, creating one with selected joints.")
                    cmds.skinCluster(joint_dict, mesh)
                    cluster = cmds.ls(cmds.listHistory(model[0]), type='skinCluster')
                bound_joints = cmds.skinCluster(cluster[0], q=True, inf=True)
                for element in joint_dict:
                    if not element in bound_joints:
                        cmds.skinCluster(cluster[0], e=True, ai=element)

                #-------- assignment
                for i in range(len(softElementData)):
                    cmds.skinPercent(cluster[0], selection[i], r=True, nrm = True, tv=[jnt, softElementData[i][2]])

            if mirror:
                orig_skinCluster = [obj for obj in cmds.listHistory(mesh) if cmds.nodeType(obj) == "skinCluster"][0]
                cmds.copySkinWeights( ss=orig_skinCluster, ds=orig_skinCluster, mirrorMode='YZ', mirrorInverse=False, sa='closestComponent', ia=[ "closestJoint",  "closestJoint"] )

            print("Finished auto-skinning.")

    def _softSelection(self):
        """Properly recover sets and vertex in order.
        Args:
            mesh(string): Mesh to check vertex
            joint_dict(list): Position of maya node
        Return:
            elements(dict): [Path, component selection, weight influence]
        """

        selection = OpenMaya.MSelectionList()
        softSelection = OpenMaya.MRichSelection()
        OpenMaya.MGlobal.getRichSelection(softSelection)
        softSelection.getSelection(selection)
        dagPath = OpenMaya.MDagPath()
        component = OpenMaya.MObject()
        iter = OpenMaya.MItSelectionList( selection,OpenMaya.MFn.kMeshVertComponent )
        elements = []
        while not iter.isDone():
            iter.getDagPath( dagPath, component )
            dagPath.pop()
            node = dagPath.fullPathName()
            fnComp = OpenMaya.MFnSingleIndexedComponent(component)
            for i in range(fnComp.elementCount()):
                elements.append([node, fnComp.element(i), fnComp.weight(i).influence()] )
            next(iter)
        return elements

    def _expand_selection(self, my_Vert, closest_verts, cycles):
        """From my_Vert, grow selection and skip side vertices existing in closest_verts.
        Args:
            my_Vert(string): Vert starting point
            closest_verts(list): List of neighbouring vertices to be ignored
            cycles(int): Number of times to run the Grow selection
        """
        safe_selection = []
        for cycle in range(cycles):
            mel.eval('PolySelectTraverse 5')
            temp_selection = cmds.ls(sl=True, fl=True)
            safe_selection = [vert for vert in temp_selection if vert not in closest_verts]
            safe_selection.append(my_Vert)
            cmds.select(safe_selection)

    # ----------------------------------------------------------

    def _create_joint_vertex_dict(self, mesh, joint_dict, vertex_dict=False):
        """Match up vertex selection and joint list.
        Args:
            mesh(string): Mesh to check vertex
            joint_dict(list): Position of maya node
            vertex_dict(bool): will access the hand selected vertex order for more accuracy
        Returns:
            joint_vertex_dict (dict): joint and the closes vertex to it
        """

        joint_vertex_dict = []
        vertex_select_dict = []
        if vertex_dict==False:
            cmds.ls(sl=True)
            if (cmds.selectPref(tso=True, q=True)==0):
                sel_list = cmds.selectPref(tso=True)
            vertex_select_dict = cmds.ls(orderedSelection=True)

        counter = 0
        for jnt in joint_dict:
            ws_pos = cmds.xform(jnt, t=True, q=True, ws=True)
            position = om.MFloatVector(float(ws_pos[0]), float(ws_pos[1]), float(ws_pos[2]))
            if vertex_dict==False:
                element = getClosestVertex(mesh,position)
            else:
                element = vertex_select_dict[counter]
            joint_vertex_dict.append('{jnt}:{element}'.format(jnt=jnt, element=element))
            counter += 1

        return joint_vertex_dict

    # ----------------------------------------------------------

    def get_influences(self, geo):

        skin = self.get_skin_from_geo(geo)
        return cmds.skinCluster(skin, q=True, influence=True)

    def get_associations(self, geo):
        skin = self.get_skin_from_geo(geo)
        return cmds.skinCluster(skin, g=True, q=True)

    def getSkinCluster(self, dag):
        """A convenience function for finding the skinCluster deforming a mesh.

        params:
          dag (MDagPath): A MDagPath for the mesh we want to investigate.
        """

        # useful one-liner for finding a skinCluster on a mesh
        skin_cluster = cmds.ls(cmds.listHistory(dag), type="skinCluster")

        if len(skin_cluster) > 0:
            # get the MObject for that skinCluster node if there is one
            sel = om.MSelectionList()
            sel.add(skin_cluster[0])
            skin_cluster_obj = om.MObject()
            sel.getDependNode(0, skin_cluster_obj)

            return skin_cluster[0], skin_cluster_obj

        else:
            raise RuntimeError("Selected mesh has no skinCluster")

    def get_weights(self, geo):

        skin_cluster = self.get_skin_from_geo(geo)

        # get the MFnSkinCluster for skinCluster
        clusterNode, clusterObject = self.getSkinCluster(geo)
        self.mfn_skin = oma.MFnSkinCluster(clusterObject)

        data = OrderedDict()
        infs_names, weights = self.get_weight()
        geo = geo

        all_data = OrderedDict()

        data[COUNT_KEY] = cmds.polyEvaluate(geo, v=True)
        data[INFLUENCE_KEY] = infs_names
        data[WEIGHT_KEY] = weights
        data[GEO_KEY] = geo

        all_data[geo] = data

        return all_data



    def get_weight(self):
        """
        Faster way to get weight information (use oma to get the plug)

        Used for getting data for json file

        Return:
            inf_names (list): [inf_basename]
                Eg -- ['lw_headSS_jnt']
            weights (dict): {vertex (int): {inf_basename (str): value (float)}}
                Eg -- {0: {u'lw_headSS_jnt': 1.0}
        """
        normalize = False

        # Get the infleunce objects from the skin cluster
        inf_ids, inf_names = self.get_influences_index_map()

        # Get the MPlug for the weightList
        wl_plug = self.mfn_skin.findPlug('weightList')
        w_plug = self.mfn_skin.findPlug('weights')
        wl_attr = wl_plug.attribute()
        w_attr = w_plug.attribute()
        w_inf_ids = om.MIntArray()

        # Actually grab the data from the MPlugs
        weights = OrderedDict()
        for v_id in range(wl_plug.numElements()):
            v_weights = dict()
            w_plug.selectAncestorLogicalIndex(v_id, wl_attr)
            w_plug.getExistingArrayAttributeIndices(w_inf_ids)
            inf_plug = om.MPlug(w_plug)
            for inf_id in w_inf_ids:
                inf_plug.selectAncestorLogicalIndex(inf_id, w_attr)
                try:
                    value = inf_plug.asDouble()
                    v_weights[inf_ids[inf_id]] = value
                except KeyError:
                    # Assume removed infleuence
                    pass
            weights[v_id] = v_weights
        return [list(inf_names.keys()), weights]

    def get_influences_index_map(self):
        """
        Get the map of infleunce indexes to names and vice versa.

        Return:
            inf_ids (dict): {inf_id (int): inf_basename (str)}
                Eg -- {0 : u'lw_headSS_jnt'}
            inf_names (dict): {inf_basename (str): inf_id (int)}
                Eg -- {u'lw_headSS_jnt': 0}
        """
        # Get the infleunce objects from the skin cluster
        inf_dags = om.MDagPathArray()
        self.mfn_skin.influenceObjects(inf_dags)

        # In the MPlug each infleunce is represented as a index
        # Need 2 maps to make the file ecitable outside of maya and settable
        ## inf_ids = {inf_id: inf_names} Used to have the inf_name in the weight dict
        ## inf_name = {inf_name: inf_id} Used for unpacking the data and setting it later
        inf_ids = dict()
        inf_names = dict()
        for x in range(inf_dags.length()):
            inf_name = MayaNode(inf_dags[x]).basename
            inf_id = int(self.mfn_skin.indexForInfluenceObject(inf_dags[x]))
            inf_ids[inf_id] = inf_name ## <--- This is {index: basename}
            inf_names[inf_name] = inf_id ## <--- This is {basename: index}

        return inf_ids, inf_names

    # ----------------------------------------------------------

    def save(self, data=None, path=None):

        if not path:
            path = mh.export_window(extension=".json")
            if not path:
                return
            path=path[0]

        if not data:
            return

        self.save_data(path=path, data=data)

    #----------------------------------------------------------

    def save_data(self, path=None,data=None):

        f = open(path, "w")
        f.write(json.dumps(data, sort_keys=1, indent=4, separators=(",", ":")))
        f.close()

    #----------------------------------------------------------

    def load_data(self, path=None):

        if not path:
            path = mh.export_window(extension=".json")
            if not path:
                return
            path=path[0]

        with open(path) as data_file:
            return json.load(data_file)

    def set_weights_slow(self, geo=None, skin_data=None, remove_unused=True):

        if not geo:
            return False
        if not skin_data:
            return False

        skin = self.get_skin_from_geo(geo)
        if not skin:
            skin = cmds.skinCluster(geo, skin_data[INFLUENCE_KEY], tsb=True)

        weigths_data = skin_data['weights']
        for vertex in weigths_data:
            vtx_data = weigths_data[vertex]
            for jnt in vtx_data:
                cmds.skinPercent(skin, "{}.vtx[{}]".format(geo, vertex), r=False, nrm=True, tv=[jnt, vtx_data[jnt]])

        # if remove_unused:
        #     self.remove_unused_influences()

    def set_weights(self, all_data, geometry=None, remove_unused=True,  namespace=False, crowd_joints=[]):
        """
            Will load all of the data that it can.

            Gives warning messages as it goes and saves RuntimeError for the end:
                - Might be easier to troubleshoot this way!
            """
        geometry = geometry or all_data
        print(geometry)
        if not isinstance(geometry, list):
            geometry = [geometry]

        loaded = list()
        fails = list()

        for geo, data in six.iteritems(all_data):
            if not cmds.objExists(geo):
                continue
            if geo not in geometry:
                print('{} not specified to be loaded'.format(geo))
                continue
            # Ensure same vert count
            if len(cmds.ls(geo)) != 1:
                print('Looked for {}, found {}'.format(geo, cmds.ls(geo)))
                fails.append(geo)
                continue
            # Ensure that this is actually a mesh!
            try:
                GeoNode(geo)
            except:
                print('{} not supported as not of type MESH'.format(geo))
                fails.append(geo)
                continue
            count = len(GeoNode(geo).mfn2.getPoints())
            if count != data[COUNT_KEY]:
                print('Vertex count for {} was {} now {}'.format(geo, data[COUNT_KEY], count))
                fails.append(geo)
                continue
            # Check that all the influences exist
            missing = [i for i in data[INFLUENCE_KEY] if not cmds.objExists(i)]
            if missing and not namespace:
                print('Influences for {} are missing \n {}'.format(geo, missing))
                fails.append(geo)
                continue
            # Find and match the influences on existing skinCluster or build a new one!
            skin = self.get_skin_from_geo(geo)
            if not skin: #Crowds support
                print('Adding Skin to:', geo)
                if crowd_joints and namespace:
                    joints=[]
                    for jnt in data[INFLUENCE_KEY]:
                        if jnt.split(':')[-1] in crowd_joints:
                            joints.append(jnt.split(':')[-1])
                        else:
                            joints.append(jnt)
                    data[INFLUENCE_KEY] = joints
                skin = cmds.skinCluster(geo, data[INFLUENCE_KEY], tsb=True)[0]
            # get the MFnSkinCluster for skinCluster
            clusterNode, clusterObject = self.getSkinCluster(geo)
            self.mfn_skin = oma.MFnSkinCluster(clusterObject)
            self.set_weight(data[INFLUENCE_KEY], data[WEIGHT_KEY], skin, namespace)
            print('Done')

            # if remove_unused:
            #     self.remove_unused_influences(skin)
            loaded.append(geo)

        if fails:
            msg = 'Could not load data on the following, see warning messages above:'
            raise RuntimeError('{} \n{}'.format(msg, fails))

        return loaded

    def set_weight(self, inf_names, weights, skin, namespace=False):
        """
        Set weights with a cmds.setAttr() straight into the plug. Faster than
        skin percent and get undo for free.

        WARNING: Maya will not do any validation of the data! You need to check
        that you are safe to plug ;) Call _validate_weight_plug_data 1st!

        Used for setting data from json file

        Args:
            inf_names (list): [inf_basename]
                Eg -- ['lw_headSS_jnt']
            weights (dict): {vertex (int): {inf_basename (str): value (float)}}
                Eg -- {0: {u'lw_headSS_jnt': 1.0}
        """
        self.set_normalize(0, skin)
        self.prune_values(skin=skin, tolerance=100, normalize=False)

        # Get the name to id influence map
        current_ids, current_names = self.get_influences_index_map()
        attr_str = '{}.weightList[{}].weights[{}]'
        for vertex, data in six.iteritems(weights):
            valid_data = dict()
            for inf_name, values in six.iteritems(data):
                cmds.select(inf_name)
                if namespace:
                    valid_data[current_names[inf_name.replace('{}:'.format(namespace), '')]] = values
                else:
                    valid_data[current_names[inf_name]] = values
            for inf_id, value in six.iteritems(valid_data):
                cmds.setAttr(attr_str.format(skin, vertex, inf_id), value)

        self.set_normalize(1, skin)


    def prune_values(self, skin, tolerance=0.01, normalize=True):
        """
        Prune skin infleunce values
        """
        geo = self.get_geo_from_skin(skin)
        cmds.skinPercent(skin, geo, normalize=normalize, pruneWeights=tolerance)

    def unlock(self, influences, skin):
        """
        Unlock specified influences of the skinCluster

        Args:
            influences (MayaNode)
        """

        if not isinstance(influences, list):
            influences = [influences]

        for i in influences:
            cmds.skinCluster(skin, edit=True, inf=i, lockWeights=False)


    def set_normalize(self, value, skin):
        """
        Set maya to do/or not do weight normalization.
        """
        cmds.setAttr('{}.normalizeWeights'.format(skin), value)


    def remove_unused_influences(self, skin):
        """
        Remove unused influences
        """
        print('Removing')
        # Get all unused influences
        weighted = set(self.get_weighted_influences(skin=skin))
        all_inf = set(self.get_influences(geo=self.get_geo_from_skin(skin)))
        unused = list(all_inf - weighted)

        # Actually Remove influences
        # node_state = cmds.getAttr("{}.nodeState".format(self))
        # cmds.setAttr("{}.nodeState".format(self), 1)
        cmds.skinCluster(skin, removeInfluence=unused, edit=True)
        # cmds.setAttr("{}.nodeState".format( self ), node_state)
        print('Removed')

    def get_weighted_influences(self, skin, base_name=False):
        """
        Get weighted influences

        Return the base_name of the influence for saving out skin weights to json
        """
        infs = [MayaNode(i) for i in cmds.skinCluster(skin, q=True, wi=True)]
        if not base_name:
            return infs
        return [i.basename for i in infs]

    # ----------------------------------------------------------

    def get_skin_from_geo(self, geo):
        if 'Shape' in geo:
            geo = cmds.listRelatives(geo, p=True)[0]
        skins = cmds.ls(type='skinCluster')
        for skin in skins:
            skin_geo = self.get_geo_from_skin(skin)
            if skin_geo == geo:
                return skin
            parent= cmds.listRelatives(skin_geo,p=True)
            if parent:
                if parent[0] == geo:
                    return skin
        return False

    # ----------------------------------------------------------

    def get_geo_from_skin(self, skin):
        geo = cmds.skinCluster(skin, q=True, geometry=True)
        return geo

    # ----------------------------------------------------------


#-----------------------------------------------------------


def getClosestVertex(mayaMesh,pos=[0,0,0]):
    import maya.api.OpenMaya as om
    """Get closest vertex on mayaMesh from maya node.
    Args:
        mayaMesh(string): Mesh to check vertex
        pos(list): Position of maya node
    Return:
        closest(dict): Vertex
    """
    mVector = om.MPoint(pos)#using MVector type to represent position
    selectionList = om.MSelectionList()
    selectionList.add(mayaMesh)
    dPath = selectionList.getDagPath(0)
    mMesh = om.MFnMesh(dPath) #changed from dPath to dag
    ID = mMesh.getClosestPoint(mVector, space=om.MSpace.kWorld)[1] #getting closest face ID
    list=cmds.ls(cmds.polyListComponentConversion (mayaMesh+'.f['+str(ID)+']',ff=True,tv=True),flatten=True)#face's vertices list
    #setting vertex [0] as the closest one
    d=mVector-om.MVector(cmds.xform(list[0],t=True,ws=True,q=True))
    smallestDist2=d.x*d.x+d.y*d.y+d.z*d.z #using distance squared to compare distance
    closest=list[0]
    #iterating from vertex [1]
    for i in range(1,len(list)) :
        d=mVector-om.MVector(cmds.xform(list[i],t=True,ws=True,q=True))
        d2=d.x*d.x+d.y*d.y+d.z*d.z
        if d2<smallestDist2:
            smallestDist2=d2
            closest=list[i]
    return closest

#-----------------------------------------------------------
"""
SCRIPT TO  TRANSFER SKINNING FROM HIERARCHY TO HIERARCHY BASED ON NAMING
date = November 4, 2022
author = Sebastian Cisneros Sojo, Luis Motta
"""

#define function to select joints from skin clusters. 
def sel_cluster_joints(obj):
	cluster_jnts = cmds.skinCluster(obj, inf = True, q = True)
	return(cluster_jnts)

#define function to transfer weights the first selected object to all the rest. 
def bulk_copy_weights(affected_objs=[], inf_asso="label", max_inf=12, uv_transf=False, skinning_method=2):
	#define all objects that will have their weights copied from the first selected object.    
	if not affected_objs:
		affected_objs = cmds.ls(sl=True, type="transform")
	
	#find the source skinCluster
	obj_hist = cmds.listHistory(affected_objs[0])
	
	if obj_hist:
		source_skinCluster = cmds.ls(obj_hist, type="skinCluster")
	else:
		print("Source '{}' has no deformer history.".format(affected_objs[0]))
	
	#Determine if the source object has a skin cluster and report it if it doesn't.    
	if source_skinCluster:
		#copy weights from source object to all target objects, regardless of if they have already a skinCluster.
		for num in range(1,len(affected_objs)):
			source_joints = sel_cluster_joints(affected_objs[0])
			
			
			#Create new skin cluster from target's joints if it doesn't have one, pass if it does. 
			try:
				new_skinCluster = cmds.skinCluster(source_joints, affected_objs[num], toSelectedBones=True, dropoffRate=6,
				removeUnusedInfluence=False, bindMethod=0, skinMethod=skinning_method, ignoreHierarchy=True, maximumInfluences=max_inf, obeyMaxInfluences=True)
			except:
				print(affected_objs[num] + " already has a skinCluster connected or is just a group.")
			
			#find the target skinCluster
			new_obj_hist = cmds.listHistory(affected_objs[num])
			target_skinCluster = cmds.ls(new_obj_hist, type="skinCluster")
			

			#copy weights from source to target.
			if uv_transf == False:
				cmds.copySkinWeights(sourceSkin=source_skinCluster[0], destinationSkin=target_skinCluster[0], influenceAssociation=inf_asso, surfaceAssociation="closestPoint", noMirror=True)
			
			else:
				cmds.copySkinWeights(sourceSkin=source_skinCluster[0], destinationSkin=target_skinCluster[0], influenceAssociation=inf_asso, surfaceAssociation="closestPoint", noMirror=True, 
				uvSpace=["map1", "map1"])
	else:
		print("Source '{}' object has no skin cluster to copy from.".format(affected_objs[0]))
	
	cmds.select(cl=True)

#Define funcion that uses bulk copy weights to transfer skinning from objects from one hierarchy to another based on naming.
def name_transfer_hierarchy_skins(source_parent=[], target_parent=[], infl_asso="label", uv_transfer=True):
    base_hierarchy_skinned_geos = []
    base_hierarchy_skinClusters = []
    name_copied_objs = []
    if not source_parent or not target_parent:
        parent_selection = cmds.ls(sl=True)
        if len(parent_selection) == 2:
            #Define hierarchies by selection order.
            hierarchy_parent_1 = [cmds.ls(sl=True)[0]]
            hierarchy_parent_2 = [cmds.ls(sl=True)[1]]
    else:
        hierarchy_parent_1 = source_parent
        hierarchy_parent_2 = target_parent
    #else:
    #   cmds.error("Please specify two hierarchy parents or select two and only two objects.")

    #Make lists out of hierarchy elements.
    hierarchy_1 = cmds.listRelatives(str(hierarchy_parent_1[0]), allDescendents=True, type='transform', fullPath=True)
    hierarchy_2 = cmds.listRelatives(str(hierarchy_parent_2[0]), allDescendents=True, type='transform', fullPath=True)

    #Determine which objects in hierachy_1 have skin cluster and add them to list.
    for obj in hierarchy_1:

        #Determine if object in the source hierarchy has history.
        obj_hist = cmds.listHistory(obj)

        #Determine if object in the source hierarchy has a skinCluster.
        if obj_hist:
            obj_skinCluster = cmds.ls(obj_hist, type="skinCluster")
            if obj_skinCluster:
                base_hierarchy_skinned_geos.append(obj)
                base_hierarchy_skinClusters.append(obj_skinCluster)
            else:
                continue
        else:
            continue

    #Getting the short name of base obj with skinning.
    for num in range(len(base_hierarchy_skinned_geos)):
        base_short_name = base_hierarchy_skinned_geos[num].split("|")[-1]
        #Getting the short name of target obj without skinning.
        for obj in hierarchy_2:
            target_short_name = obj.split("|")[-1]
            #Compare object by object until it finds a name match. When found, bulk copy weights.
            if base_short_name == target_short_name:
                bulk_copy_weights([base_hierarchy_skinned_geos[num], obj], uv_transf=uv_transfer, inf_asso=infl_asso)
                #print("Weights copied from {} to {}.".format(base_hierarchy_skinned_geos[num], obj))
                name_copied_objs.append(target_short_name)
            else:
                continue

    #Reporting copied objects.
    #print("Weights copied through naming to:")
    #for copied_obj in name_copied_objs:
    #	print(copied_obj)
    cmds.select(hierarchy_parent_1, hierarchy_parent_2)

    return hierarchy_2
