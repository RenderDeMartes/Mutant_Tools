from __future__ import absolute_import
import os
import glob

from maya import cmds, mel

animations_path = "D:\\Modelos\\New-FBX-BVH_Z-OO\\Truebone_Z-OO\\Dog"
animations = glob.glob(animations_path+'\\*.fbx') 

print(animations)


#--------------------------------------------------

#First import fbx and match size with legs

#Go to bind pose
cmds.autoKeyframe(state=True)
cmds.currentTime(-1)
mel.eval('gotoBindPose;')

#--------------------------------------------------
"""

MANUAL STEP MATCH SOURCE Anim to rig

"""

#--------------------------------------------------

legs_map = {


    'L_FrBall_Ik_Ctrl':'Bip01_L_Finger0',
    'L_FrFoot_Toes_Ctrl':'Bip01_L_Finger01',
    'L_BkBall_Ik_Ctrl':'Bip01_L_Toe01',
    'L_BkFoot_Toes_Ctrl':'Bip01_L_Toe02'
    
    }
    
clavs_map = {
    
    'L_Clavicle_Ctrl':'Bip01_L_Clavicle',
    'L_Pelvis_Ctrl':'Bip01_L_Thigh'
    
    }
    
tail_map = { 
    'Tail_1_Rotator_Ctrl':'Bip01_Spine0_Tail'

    }
    
head_map = {

    'Head_Ctrl':'Bip01_Head',
    'Neck_Ctrl':'Bip01_Neck'

    }
    
    
spine_map = {
    'Spine_0_Frw_Ctrl':'Bip01_Pelvis',
    'Spine_1_Frw_Ctrl':'Bip01_Spine1',
    'Spine_2_Frw_Ctrl':'Bip01_Spine3',
        
    #'Spine_1_Ik_Ctrl':'Bip01_Spine',
    #'Spine_2_Ik_Ctrl':'Bip01_Spine2'
    
}


#Legs 
for leg in legs_map:
    print(leg)
    cmds.pointConstraint(legs_map[leg], leg, mo=True)
    cmds.pointConstraint(legs_map[leg].replace('L_', 'R_'), leg.replace('L_', 'R_'), mo=True)

    #cmds.pointConstraint(legs_map[leg], leg, mo=True)
    #cmds.orientConstraint(legs_map[leg], leg, mo=True)


cmds.setAttr('R_BkKnee_IkPV_Ctrl.Follow', 2)
cmds.setAttr('R_FrKnee_IkPV_Ctrl.Follow', 2)
cmds.setAttr('L_FrKnee_IkPV_Ctrl.Follow', 2)
cmds.setAttr('L_BkKnee_IkPV_Ctrl.Follow', 2)



#Clavs 
for i in clavs_map:
    cmds.pointConstraint(clavs_map[i], i, mo=True)
    cmds.orientConstraint(clavs_map[i], i, mo=True)
    
#Tail 
for i in tail_map:
    cmds.orientConstraint(tail_map[i], i, mo=True)
    
#Head 
for i in head_map:
    #cmds.pointConstraint(head_map[i], i, mo=True)
    cmds.orientConstraint(head_map[i], i, mo=True)

#Spine 
for i in spine_map:
    #cmds.pointConstraint(head_map[i], i, mo=True)
    cmds.orientConstraint(spine_map[i], i, mo=True)
     

#--------------------------------------------------
"""

MANUAL STEP Remove X axis from legs

"""

#--------------------------------------------------
























    
    

