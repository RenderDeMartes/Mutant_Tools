from __future__ import absolute_import
#DEMBONE POSES TO SDK
from maya import cmds
import collections
from collections import OrderedDict
import pprint
import os
from Mutant_Tools.Utils.Helpers import helpers
from pathlib import Path
#reload(Mutant_Tools.Utils.Helpers.helpers)
mh = helpers.Helpers()

PATH = os.path.dirname(__file__)
PATH = Path(PATH)
PATH_PARTS = PATH.parts[:-3]
FOLDER=''
for f in PATH_PARTS:
	FOLDER = os.path.join(FOLDER, f)
FOLDER_NAME = 'GamesCrowds'

print("".center(20, '#'))
print("Path to json is: {}".format(os.path.join(FOLDER, 'UI', FOLDER_NAME, 'crowd_utils')))


anim_dict =  mh.read_json(path=os.path.join(FOLDER, 'UI', FOLDER_NAME, 'crowd_utils'), json_file='SDKMap.json')
print('geo_grp exists = {}'.format(cmds.objExists('Geo_Grp')))
print('control_grp exists = {}'.format(cmds.objExists('Control_Grp')))

if cmds.objExists('Geo_Grp') and cmds.objExists('Control_Grp'):
    print('Using BD dict')
    anim_dict =  mh.read_json(path=os.path.join(FOLDER, 'UI', FOLDER_NAME, 'crowd_utils'), json_file='SDKMap_BD.json')
    for i in anim_dict:
        print(i)

            
def getAttName(fullname):
    parts = fullname.split('.')
    return parts[-1]
    
def getDemAnim(dem_joints=cmds.ls(sl=True)):
    """ 
    Reads DemBones imported animation and saves the 
    transform/rotation values to its corresponding 
    input_key slot in the dictionaro
		Args:
			dem_joints: DemBones joints

		Returns: anim_dict (Updated dictionary)
    """
    #run through dictionary and get translate and rotate values
    # for each fac
    for task in sorted(anim_dict.keys()):
        # move to the anim frame
        frame = anim_dict[task]['input_key']
        cmds.currentTime(frame)
        
        # get all translate and rotate values and store them in a dict 
        t_values=OrderedDict()
        r_values=OrderedDict()
        for j in dem_joints:
            t_values[j] = cmds.xform(j, q=True, ws=True, t=True)
            r_values[j] = cmds.xform(j, q=True, ws=True, ro=True)
            
        #saved recovered values to the associated control
        anim_dict[task]['t_values'] = t_values
        anim_dict[task]['r_values'] = r_values
    
    #Delete joints to avoide creating blendweights nodes early
    for j in dem_joints:
        animAttributes = cmds.listAnimatable(j)
        for attribute in animAttributes:
            numKeyframes = cmds.keyframe(attribute, query=True, keyframeCount=True)
            if (numKeyframes > 0):
                cmds.cutKey(j, attribute=getAttName(attribute), option="keys")

    print('Done getting SDK values from DemBones Animation.')
    #pprint.pprint(anim_dict)
    #pprint.pprint(anim_dict.keys)

    return anim_dict 
    
def fill_cero_controls(dem_joints):
    """ 
    Recoveres all the controls defined in the SDK dictionary 
		Args:
			dem_joints: DemBones joints

		Returns: None
    """
    #get all keyed control available
    allCtrls=[]

    # for each fac
    for task in sorted(anim_dict.keys()):
        for ctrl in anim_dict[task]['controls']:
            if cmds.objExists(ctrl) == True:
                print("task={}, control={}".format(task, ctrl))
                attr= "{a}.{t}".format(a=ctrl,t=anim_dict[task]['controls'][ctrl]['axis'])    
                allCtrls.append(attr)
    anim_dict['Cero_Animation']['controls'] = allCtrls
    print(allCtrls)
    
def cero_SDK(dem_joints):
    """ 
    Connects default Face Rig controls to default DemBones Anim pose
		Args:
			dem_joints: DemBones joints

		Returns: None
    """
    #SDK - 0 animation value (default)  
    for ctrl in anim_dict['Cero_Animation']['controls']:
        cmds.setAttr(ctrl, 0)
        
        #zero out values according to default values
        for j in dem_joints: 
            cmds.xform(j, ws=True, a=True, t=anim_dict['Cero_Animation']['t_values'][j])
            cmds.xform(j, ws=True, a=True, ro=anim_dict['Cero_Animation']['r_values'][j])
            
            #set SDK fro zeros
            for axis in ['x', 'y', 'z']:
                cmds.setDrivenKeyframe("{j}.t{a}".format(j=j,a=axis), cd=ctrl)
                cmds.setDrivenKeyframe("{j}.r{a}".format(j=j,a=axis), cd=ctrl) 
    
    print ('Cero Anim key completed.')
    
    
def anim_to_SDK(dem_joints):
    """ 
    Read SDK dictionary and connects Face Rig control to DemBones Anim pose
		Args:
			dem_joints: DemBones joints

		Returns: None
    """

    cmds.currentTime(1)

    #Set SDK values for rest of keyframes info
    for task in sorted(anim_dict.keys()):
        frame = anim_dict[task]['input_key']
        if frame > 1:
            #skips setting values on 0, does set values in other keyframes
            for ctrl in anim_dict[task]['controls']:
                if not cmds.objExists(ctrl):
                    print("{} does not exist, skipping".format(ctrl))
                    continue
                attr= "{a}.{t}".format(a=ctrl,t=anim_dict[task]['controls'][ctrl]['axis'])
                #control value with number
                cmds.setAttr(attr,float(anim_dict[task]['controls'][ctrl]['values']))
                
                #creates sdk for the values at that current frame, certain transform on control and joint animation
                for j in dem_joints: 
                
                    cmds.xform(j, ws=True, a=True, t=anim_dict[task]['t_values'][j])
                    cmds.xform(j, ws=True, a=True, ro=anim_dict[task]['r_values'][j])
                       
                    for axis in ['x', 'y', 'z']: 
                        cmds.setDrivenKeyframe("{j}.t{a}".format(j=j,a=axis), cd=attr)
                        cmds.setDrivenKeyframe("{j}.r{a}".format(j=j,a=axis), cd=attr) 
                cmds.setAttr(attr,0)
            print ('{} key completed.'.format(task))

        else: 
            print ('Not running Cero_Anim.')
             
    print ('Done.')

def connect_Face_SDK(dem_joints):
    """ 
    Connects determined FaceControls to DemBones anim poses through SDKs
		Args:
			dem_joints: DemBones joints

		Returns: None
    """
    getDemAnim(dem_joints=dem_joints)
    fill_cero_controls(dem_joints=dem_joints)
    cero_SDK(dem_joints=dem_joints)                              
    anim_to_SDK(dem_joints=dem_joints)
    
