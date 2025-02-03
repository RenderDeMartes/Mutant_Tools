from __future__ import absolute_import
"""
SCRIPT TO  TRANSFER SKINNING FROM ZOMBIE BASEMESHES TO GENERIC ZOMBIES

date = October28, 2022
author = Sebastian Cisneros Sojo

"""

from maya import cmds

FEMALE_BASEMESH_PATH = "/job/anythinggoes/assets/char/BasemeshFZombieA/wip/rigging/sebastian.cisneros/maya/scenes/BasemeshFZombieA_rigging_sebastianc_CrowdRig_v021.ma"
MALE_BASEMESH_PATH = "/job/anythinggoes/assets/char/BasemeshMZombieA/wip/rigging/sebastian.cisneros/maya/scenes/BasemeshMZombieA_rigging_sebastianc_CrowdRig_v024.ma"


#define function to select joints from skin clusters. 
def sel_cluster_joints(obj):
	cluster_jnts = cmds.skinCluster(obj, inf = True, q = True)
	return(cluster_jnts)


#helper function to for the organize_outliner function. 
def sort_children(item=None, entire_hierarchy=True, case_sensitive=False):
	"""
	Gets children of item and sorts them by alphabetical order
	
	param: entire_hierarchy, determines whether to go through all the children and childrens children
	param: case_sensitive, whether to sort the items with case or not
	"""
	import pymel.core as pm
	
	item_children = item.getChildren(type="transform")
	if not item_children:
		return
	
	
	# set "entire_hierarchy" to False to skip this
	if entire_hierarchy:
		for child_item in item_children:
			sort_children(item=child_item, entire_hierarchy=entire_hierarchy, case_sensitive=case_sensitive)
	
	
	# Sorting methods
	if case_sensitive:
		sorted_children = sorted(item_children)                           # case sensitive alphabet sort
	else:
		sorted_children = sorted(item_children, key=lambda s: s.lower())  # case insensitive alphabet sort
	
	
	sorted_children.reverse()  # reverse list as we reorder bottom to top
	
	for sorted_item in sorted_children:
		pm.reorder(sorted_item, front=True)  # the actual reorder command



#define function to transfer weights the first selected object to all the rest. 
def bulk_copy_weights(affected_objs=[], inf_asso="label", max_inf=12, uv_transf=False, skinning_method=2):

	from maya import cmds

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




#Function to organize outliner alphabetically. 
def organize_outliner(*args):
	import pymel.core as pm
	for top_node in pm.selected():
		sort_children(top_node)




#IMPORTING MALE OF FEMALE BASEMESHES
def import_female_basemeshes():
	cmds.file(FEMALE_BASEMESH_PATH, i=True, type="mayaAscii") 

def import_male_basemeshes():
	cmds.file(MALE_BASEMESH_PATH, i=True, type="mayaAscii") 



def name_transfer_hierarchy_skins():
	base_hierarchy_skinned_geos = []
	base_hierarchy_skinClusters = []
	name_copied_objs = []

	#Define hierarchies by selection order.
	hierarchy_parent_1 = [cmds.ls(sl=True)[0]]
	hierarchy_parent_2 = [cmds.ls(sl=True)[1]]

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

	for num in range(len(base_hierarchy_skinned_geos)):
		base_short_name = base_hierarchy_skinned_geos[num].split("|")[-1]

		for obj in hierarchy_2:
			target_short_name = obj.split("|")[-1]

			if base_short_name == target_short_name:
				bulk_copy_weights([base_hierarchy_skinned_geos[num], obj])
				print("Weights copied from {} to {}.".format(base_hierarchy_skinned_geos[num], obj))
				name_copied_objs.append(target_short_name)

			else:
				continue

	print("Weights copied through naming to:")
	for copied_obj in name_copied_objs:
		print(copied_obj)
	cmds.select([hierarchy_parent_1[0], hierarchy_parent_2[0]])

	return hierarchy_2
		



def attachment_groups_copy():
	
	head_attachment_full_path = []
	head_full_path = []
	body_attachment_full_path = []
	body_full_path = []
	
	
	#Define hierarchies by selection order.
	hierarchy_parent_1 = [cmds.ls(sl=True)[0]]
	hierarchy_parent_2 = [cmds.ls(sl=True)[1]]

	#Make lists out of hierarchy elements.
	hierarchy_1 = cmds.listRelatives(str(hierarchy_parent_1[0]), allDescendents=True, type='transform', fullPath=True)
	hierarchy_2 = cmds.listRelatives(str(hierarchy_parent_2[0]), allDescendents=True, type='transform', fullPath=True)

	hierarchy_2_short_names = cmds.listRelatives(str(hierarchy_parent_2[0]), allDescendents=True, type='transform')

	#Define objects head and body objects and their groups to copy to based on naming
	for obj in hierarchy_2:
		target_short_name = obj.split("|")[-1]

		if target_short_name.lower() == "head_attachments_grp":
			head_attachment_full_path = obj

		elif target_short_name.lower() == "c_head_hi":
			head_full_path = obj

		elif target_short_name.lower() == "body_attachments_grp":
			body_attachment_full_path = obj

		elif target_short_name.lower() == "c_body_hi":
			body_full_path = obj



	#If head exists on hierarchy proceed.
	if head_full_path:
		#if head attachment group exists in hierarchy proceed.
		if head_attachment_full_path:
			#get all objects inside group.
			head_attachment_hierarchy = cmds.listRelatives(head_attachment_full_path, allDescendents=True, type='transform', fullPath=True)
			if head_attachment_hierarchy:
				for obj in head_attachment_hierarchy:
					#Copy weights from head to all objects inside group. "Try" is used to avoid stopping script if there are groups inside.
					try:
						bulk_copy_weights([head_full_path, obj])
					except:
						continue
		else:
			cmds.warning("No body attachments group to copy weights to.")
	else:
		cmds.warning("No new head geo to copy weights from. ")

	#If head exists on hierarchy proceed.
	if body_full_path:
		#if head attachment group exists in hierarchy proceed.
		if body_attachment_full_path:
			#get all objects inside group.
			body_attachment_hierarchy = cmds.listRelatives(body_attachment_full_path, allDescendents=True, type='transform', fullPath=True)
			if body_attachment_hierarchy:
				#Copy weights from head to all objects inside group. "Try" is used to avoid stopping script if there are groups inside.
				for obj in body_attachment_hierarchy:
					try:
						bulk_copy_weights([body_full_path, obj])
					except:
						continue
		else:
			cmds.warning("No body attachments group to copy weights to.")
	else:
		cmds.warning("No new body geo to copy weights from. ")




#import_female_basemeshes()
#import_male_basemeshes()
#name_transfer_hierarchy_skins()
#attachment_groups_copy()