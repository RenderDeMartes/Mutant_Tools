import pymel.core as pm

# /////////////////////////////////
#    Custom Rig Definition     //
# ///////////////////////////////

if pm.objExists("Spine_Base_Bnd"):
    pm.mel.setCharacterObject("Spine_Base_Bnd", "Character1", 1, 0)
    # Spine
    pm.mel.setCharacterObject("Spine_Belly_Bnd", "Character1", 8, 0)
    #pm.mel.setCharacterObject("Spine_3", "Character1", 23, 0)
    if pm.objExists("Spine_Chest_Bnd"):
        pm.mel.setCharacterObject("Spine_Chest_Bnd", "Character1", 24, 0)

    #if pm.objExists("Spine_4"):
        #pm.mel.setCharacterObject("Spine_4", "Character1", 24, 0)

#ROOT
if pm.objExists("Root"):
    pm.mel.setCharacterObject("Root", "Character1", 0, 0)
    
# Clavicles
if pm.objExists("L_Clavicle_Bnd"):
    pm.mel.setCharacterObject("L_Clavicle_Bnd", "Character1", 18, 0)
    pm.mel.setCharacterObject("R_Clavicle_Bnd", "Character1", 19, 0)

# Arms
if pm.objExists("L_Shoulder_Twist_0_Bnd"):
    pm.mel.setCharacterObject("L_Shoulder_Twist_0_Bnd", "Character1", 9, 0)
    pm.mel.setCharacterObject("R_Shoulder_Twist_0_Bnd", "Character1", 12, 0)
    pm.mel.setCharacterObject("L_Shoulder_Twist_1_Bnd", "Character1", 176, 0)
    pm.mel.setCharacterObject("R_Shoulder_Twist_1_Bnd", "Character1", 178, 0)
    pm.mel.setCharacterObject("L_Shoulder_Twist_2_Bnd", "Character1", 184, 0)
    pm.mel.setCharacterObject("R_Shoulder_Twist_2_Bnd", "Character1", 186, 0)

# ForeArm
if pm.objExists("L_Elbow_Twist_0_Bnd"):
    pm.mel.setCharacterObject("L_Elbow_Twist_0_Bnd", "Character1", 10, 0)
    pm.mel.setCharacterObject("R_Elbow_Twist_0_Bnd", "Character1", 13, 0)
    pm.mel.setCharacterObject("L_Elbow_Twist_1_Bnd", "Character1", 177, 0)
    pm.mel.setCharacterObject("R_Elbow_Twist_1_Bnd", "Character1", 179, 0)
    pm.mel.setCharacterObject("L_Elbow_Twist_2_Bnd", "Character1", 185, 0)
    pm.mel.setCharacterObject("R_Elbow_Twist_2_Bnd", "Character1", 187, 0)

# Palm
if pm.objExists("L_Hand_Palm_Bnd"):
    pm.mel.setCharacterObject("L_Hand_Palm_Bnd", "Character1", 11, 0)
    pm.mel.setCharacterObject("L_Hand_Palm_Bnd", "Character1", 14, 0)

# Thumb
if pm.objExists("L_Hand_Thumb_00_Bnd"):
    pm.mel.setCharacterObject("L_Hand_Thumb_00_Bnd", "Character1", 50, 0)
    pm.mel.setCharacterObject("R_Hand_Thumb_00_Bnd", "Character1", 74, 0)
    pm.mel.setCharacterObject("L_Hand_Thumb_01_Bnd", "Character1", 51, 0)
    pm.mel.setCharacterObject("R_Hand_Thumb_01_Bnd", "Character1", 75, 0)
    pm.mel.setCharacterObject("L_Hand_Thumb_02_Bnd", "Character1", 52, 0)
    pm.mel.setCharacterObject("R_Hand_Thumb_02_Bnd", "Character1", 76, 0)

# Index
if pm.objExists("L_Hand_Index_00_Bnd"):
    pm.mel.setCharacterObject("L_Hand_Index_00_Bnd", "Character1", 147, 0)
    pm.mel.setCharacterObject("R_Hand_Index_00_Bnd", "Character1", 153, 0)
    pm.mel.setCharacterObject("L_Hand_Index_01_Bnd", "Character1", 54, 0)
    pm.mel.setCharacterObject("R_Hand_Index_01_Bnd", "Character1", 78, 0)
    pm.mel.setCharacterObject("L_Hand_Index_02_Bnd", "Character1", 55, 0)
    pm.mel.setCharacterObject("R_Hand_Index_02_Bnd", "Character1", 79, 0)
    pm.mel.setCharacterObject("L_Hand_Index_03_Bnd", "Character1", 56, 0)
    pm.mel.setCharacterObject("R_Hand_Index_03_Bnd", "Character1", 80, 0)

# Middle
if pm.objExists("L_Hand_Middle_00_Bnd"):
    pm.mel.setCharacterObject("L_Hand_Middle_00_Bnd", "Character1", 148, 0)
    pm.mel.setCharacterObject("R_Hand_Middle_00_Bnd", "Character1", 154, 0)
    pm.mel.setCharacterObject("L_Hand_Middle_01_Bnd", "Character1", 58, 0)
    pm.mel.setCharacterObject("R_Hand_Middle_01_Bnd", "Character1", 82, 0)
    pm.mel.setCharacterObject("L_Hand_Middle_02_Bnd", "Character1", 59, 0)
    pm.mel.setCharacterObject("R_Hand_Middle_02_Bnd", "Character1", 83, 0)
    pm.mel.setCharacterObject("L_Hand_Middle_03_Bnd", "Character1", 60, 0)
    pm.mel.setCharacterObject("R_Hand_Middle_03_Bnd", "Character1", 84, 0)

# Ring
if pm.objExists("L_Hand_Ring_00_Bnd"):
    pm.mel.setCharacterObject("L_Hand_Ring_00_Bnd", "Character1", 149, 0)
    pm.mel.setCharacterObject("R_Hand_Ring_00_Bnd", "Character1", 155, 0)
    pm.mel.setCharacterObject("L_Hand_Ring_01_Bnd", "Character1", 62, 0)
    pm.mel.setCharacterObject("R_Hand_Ring_01_Bnd", "Character1", 86, 0)
    pm.mel.setCharacterObject("L_Hand_Ring_02_Bnd", "Character1", 63, 0)
    pm.mel.setCharacterObject("R_Hand_Ring_02_Bnd", "Character1", 87, 0)
    pm.mel.setCharacterObject("L_Hand_Ring_03_Bnd", "Character1", 64, 0)
    pm.mel.setCharacterObject("R_Hand_Ring_03_Bnd", "Character1", 88, 0)

# Pinky
if pm.objExists("L_Hand_Pinky_00_Bnd"):
    pm.mel.setCharacterObject("L_Hand_Pinky_00_Bnd", "Character1", 150, 0)
    pm.mel.setCharacterObject("R_Hand_Pinky_00_Bnd", "Character1", 156, 0)
    pm.mel.setCharacterObject("L_Hand_Pinky_01_Bnd", "Character1", 66, 0)
    pm.mel.setCharacterObject("R_Hand_Pinky_01_Bnd", "Character1", 90, 0)
    pm.mel.setCharacterObject("L_Hand_Pinky_02_Bnd", "Character1", 67, 0)
    pm.mel.setCharacterObject("R_Hand_Pinky_02_Bnd", "Character1", 91, 0)
    pm.mel.setCharacterObject("L_Hand_Pinky_03_Bnd", "Character1", 68, 0)
    pm.mel.setCharacterObject("R_Hand_Pinky_03_Bnd", "Character1", 92, 0)

# Head Neck
if pm.objExists("Neck_1_Bnd"):
    pm.mel.setCharacterObject("Neck_1_Bnd", "Character1", 20, 0)
    pm.mel.setCharacterObject("Head_Bnd", "Character1", 15, 0)

# Legs
if pm.objExists("L_Hip_Twist_0_Bnd"):
    pm.mel.setCharacterObject("L_Hip_Twist_0_Bnd", "Character1", 2, 0)
    pm.mel.setCharacterObject("R_Hip_Twist_0_Bnd", "Character1", 5, 0)
    pm.mel.setCharacterObject("L_Hip_Twist_1_Bnd", "Character1", 172, 0)
    pm.mel.setCharacterObject("R_Hip_Twist_1_Bnd", "Character1", 174, 0)
    pm.mel.setCharacterObject("L_Hip_Twist_2_Bnd", "Character1", 180, 0)
    pm.mel.setCharacterObject("R_Hip_Twist_2_Bnd", "Character1", 182, 0)

# Knee
if pm.objExists("L_Knee_Twist_0_Bnd"):
    pm.mel.setCharacterObject("L_Knee_Twist_0_Bnd", "Character1", 3, 0)
    pm.mel.setCharacterObject("R_Knee_Twist_0_Bnd", "Character1", 6, 0)
    pm.mel.setCharacterObject("L_Knee_Twist_1_Bnd", "Character1", 173, 0)
    pm.mel.setCharacterObject("R_Knee_Twist_1_Bnd", "Character1", 175, 0)
    pm.mel.setCharacterObject("L_Knee_Twist_2_Bnd", "Character1", 181, 0)
    pm.mel.setCharacterObject("R_Knee_Twist_2_Bnd", "Character1", 183, 0)

# Ankle Ball
if pm.objExists("L_Foot_Ankle_Bnd"):
    pm.mel.setCharacterObject("L_Foot_Ankle_Bnd", "Character1", 4, 0)
    pm.mel.setCharacterObject("R_Foot_Ankle_Bnd", "Character1", 7, 0)
    pm.mel.setCharacterObject("L_Foot_BallToes_Bnd", "Character1", 16, 0)
    pm.mel.setCharacterObject("R_Foot_BallToes_Bnd", "Character1", 17, 0)

# /////////Create Custom Rig Mapping
pm.mel.hikCreateCustomRig(pm.mel.hikGetCurrentCharacter())

try:
    pm.setAttr("L_Wrist_Fk_Ctrl|L_Shoulder_Jnt_Switch_Loc.Switch_IK_FK", 1)
    pm.setAttr("R_Wrist_Fk_Ctrl|R_Shoulder_Jnt_Switch_Loc.Switch_IK_FK", 1)
    pm.setAttr("L_Ankle_Fk_Ctrl|L_Hip_Jnt_Switch_Loc.Switch_IK_FK", 0)
    pm.setAttr("R_Ankle_Fk_Ctrl|R_Hip_Jnt_Switch_Loc.Switch_IK_FK", 0)

except:
    pass


# /////////////////////////////////
#    Custom Rig Controllers    //
# ///////////////////////////////


pm.mel.hikImportCustomRigMapping(pm.mel.hikGetCurrentCharacter())

'''

R IK FOOT :    0    90    90

R Clav :    180    0    0    

R Shoulder :    180    0    0 

R Elbow :    180    0    0

R Wrist :    180    0    180




'''
