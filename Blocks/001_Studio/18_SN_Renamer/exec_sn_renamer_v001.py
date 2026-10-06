from __future__ import absolute_import
from maya import cmds
try:
    import importlib;from importlib import reload
except:
    import imp;from imp import reload

import Mutant_Tools
import Mutant_Tools.Utils.Rigging
from Mutant_Tools.Utils.Rigging import main_mutant
reload(Mutant_Tools.Utils.Rigging.main_mutant)

mt = main_mutant.Mutant()

from Mutant_Tools.Utils.IO import CtrlUtils

#---------------------------------------------

TAB_FOLDER = '001_Studio'
PYBLOCK_NAME = 'exec_sn_renamer'

#---------------------------------------------

# Everything this block needs lives in this file -- no external JSON is read.
# MODULE mirrors 18_SN_Renamer.json, which exists only so the Mutant UI can
# discover the block and draw its button.
MODULE = {
    'Name': 'SN_Renamer',
    'import': 'import exec_sn_renamer_v001',
    'build_command': 'exec_sn_renamer_v001.build_sn_renamer_block()',
    'attrs': {
        'RunBeforeLoadCtrls_bool': 'True',
        'RunAfterBuild_bool': 'False',
    },
}

# Never rename anything living under these groups (block guides, etc).
EXCLUDE_GROUPS = ['Mutant_Build']

# Old control name -> new control name. Groups are only for human sorting;
# every entry is merged into one flat lookup at build time.
NAME_MAPPING = {
    'Global': {
        'Global_Ctrl': 'M_Global',
        'Mover_Ctrl': 'M_Mover',
        'Mover_Gimbal_Ctrl': 'M_MoverGimbal',
    },
    'Spine': {
        'COG_Ctrl': 'M_Body',
        'COG_Gimbal_Ctrl': 'M_BodyGimbal',
        'Spine_Chest_Top_IK_Ctrl': 'M_Chest',
        'Spine_Belly_IK_Ctrl': 'M_SpineMid',
        'Spine_Bottom_Ik_Ctrl': 'M_Hips',
        'Spine_Attrs_Ctrl': 'M_SpineAttrs',
        'Spine_Base_IK_Ctrl': 'M_SpineBend1',
        'Spine_Chest_IK_Ctrl': 'M_SpineBend2',
        'Spine_Belly_FK_Ctrl': 'M_SpineBellyFK',
        'Spine_Base_FK_Ctrl': 'M_SpineBaseFK',
        'Spine_End_IK_Ctrl': 'M_SpineTopIK',
        'Spine_Root_IK_Ctrl': 'M_SpineRootIK',
    },
    'Spine_Bee': {
        'Spine_Chest_FK_Ctrl': 'M_SpineChestFK',
    },
    'Head_Neck': {
        'FrontFace_Global_Ctrl': 'M_FrontFaceGlobal',
        'FrontFace_Mover_Ctrl': 'M_FrontFaceMover',
        'FrontFace_Mover_Gimbal_Ctrl': 'M_FrontFaceMoverGimbal',
        'LeftFace_Global_Ctrl': 'L_FaceGlobal',
        'LeftFace_Mover_Ctrl': 'L_FaceMover',
        'LeftFace_Mover_Gimbal_Ctrl': 'L_FaceMoverGimbal',
        'RightFace_Global_Ctrl': 'R_FaceGlobal',
        'RightFace_Mover_Ctrl': 'R_FaceMover',
        'RightFace_Mover_Gimbal_Ctrl': 'R_FaceMoverGimbal',
        'Head_Ctrl': 'M_Head',
        'UprSkull_Ctrl': 'M_UpFace',
        'Squash_Ctrl_Offset_Ctrl': 'M_UpHeadSquash',
        'LowerSnS_Ctrl_Offset_Ctrl': 'M_LoHeadSquash',
        'Neck_1_Ctrl': 'M_NeckBend1',
        'Neck_2_Ctrl': 'M_NeckBend2',
        'Neck_3_Ctrl': 'M_NeckBend3',
        'Neck_Ctrl': 'M_Neck',
    },
    'Jaw': {
        'Dinamic_Pivot_Jaw_Ctrl': 'M_JawPivot',
        'Dinamic_Pivot_LeftJaw_Ctrl': 'M_JawPivot_LFace',
        'Dinamic_Pivot_RightJaw_Ctrl': 'M_JawPivot_RFace',
        'L_SubJaw_Local_Ctrl': 'M_Jaw_LFace',
        'LeftJaw_Ctrl': 'M_JawSlide_LFace',
        'RightSubJaw_Ctrl': 'M_JawSlideSub_RFace',
        'LeftSubJaw_Ctrl': 'M_JawSlideSub_LFace',
        'SubJaw_Ctrl': 'M_JawSub',
        'Jaw_Ctrl': 'M_JawSlide',
        'RightJaw_Ctrl': 'M_JawSlide_RFace',
        'C_SubJaw_Local_Ctrl': 'M_Jaw',
        'R_SubJaw_Local_Ctrl': 'M_Jaw_RFace',
        'C_SubChin_Local_Ctrl': 'M_Chin',
        'R_SubChin_Local_Ctrl': 'M_Chin_RFace',
        'L_SubChin_Local_Ctrl': 'M_Chin_LFace',
    },
    'Teeth': {
        'Teeth_Lwr_Ctrl': 'M_LoTeeth',
        'Teeth_Upr_Ctrl': 'M_UpTeeth',
        'LeftTeeth_Lwr_Ctrl': 'M_LoTeeth_LFace',
        'LeftTeeth_Upr_Ctrl': 'M_UpTeeth_LFace',
        'RightTeeth_Lwr_Ctrl': 'M_LoTeeth_RFace',
        'RightTeeth_Upr_Ctrl': 'M_UpTeeth_RFace',
        'DwTeethTweak_1_00_Ctrl': 'L_LoTeethTweak3',
        'DwTeethTweak_1_01_Ctrl': 'L_LoTeethTweak2',
        'DwTeethTweak_1_02_Ctrl': 'M_LoTeethTweak1',
        'DwTeethTweak_1_03_Ctrl': 'R_LoTeethTweak2',
        'DwTeethTweak_1_04_Ctrl': 'R_LoTeethTweak3',
        'RightDwTeethTweak_1_00_Ctrl': 'L_LoTeethTweak3_RFace',
        'RightDwTeethTweak_1_01_Ctrl': 'L_LoTeethTweak2_RFace',
        'RightDwTeethTweak_1_02_Ctrl': 'L_LoTeethTweak1_RFace',
        'RightDwTeethTweak_1_03_Ctrl': 'R_LoTeethTweak2_RFace',
        'RightDwTeethTweak_1_04_Ctrl': 'R_LoTeethTweak3_RFace',
        'RightDwTeethTweak_1_Main_Ctrl': 'M_LoTeethMid_RFace',
        'RightUpTeethTweak_1_00_Ctrl': 'L_UpTeethTweak3_RFace',
        'RightUpTeethTweak_1_01_Ctrl': 'L_UpTeethTweak2_RFace',
        'RightUpTeethTweak_1_02_Ctrl': 'L_UpTeethTweak1_RFace',
        'RightUpTeethTweak_1_03_Ctrl': 'R_UpTeethTweak2_RFace',
        'RightUpTeethTweak_1_04_Ctrl': 'R_UpTeethTweak3_RFace',
        'RightUpTeethTweak_1_Main_Ctrl': 'M_UpTeethMid_RFace',
        'DwTeethTweak_1_Main_Ctrl': 'M_LoTeethMid',
        'L_DwMolar_A_Ctrl': 'L_LoMolarA',
        'L_DwMolar_B_Ctrl': 'L_LoMolarB',
        'L_LeftDwMolar_A_Ctrl': 'L_LoMolarA_LFace',
        'L_LeftDwMolar_B_Ctrl': 'L_LoMolarB_LFace',
        'L_LeftUpMolar_A_Ctrl': 'L_UpMolarA_LFace',
        'L_LeftUpMolar_B_Ctrl': 'L_UpMolarB_LFace',
        'L_RightDwMolar_A_Ctrl': 'L_LoMolarA_RFace',
        'L_RightDwMolar_B_Ctrl': 'L_LoMolarB_RFace',
        'L_RightUpMolar_A_Ctrl': 'L_UpMolarA_RFace',
        'L_RightUpMolar_B_Ctrl': 'L_UpMolarB_RFace',
        'L_UpMolar_A_Ctrl': 'L_UpMolarA',
        'L_UpMolar_B_Ctrl': 'L_UpMolarB',
        'LeftDwTeethTweak_1_00_Ctrl': 'L_LoTeethTweak3_LFace',
        'LeftDwTeethTweak_1_01_Ctrl': 'L_LoTeethTweak2_LFace',
        'LeftDwTeethTweak_1_02_Ctrl': 'L_LoTeethTweak1_LFace',
        'LeftDwTeethTweak_1_03_Ctrl': 'R_LoTeethTweak2_LFace',
        'LeftDwTeethTweak_1_04_Ctrl': 'R_LoTeethTweak3_LFace',
        'LeftDwTeethTweak_1_Main_Ctrl': 'M_LoTeethMid_LFace',
        'LeftUpTeethTweak_1_00_Ctrl': 'L_UpTeethTweak3_LFace',
        'LeftUpTeethTweak_1_01_Ctrl': 'L_UpTeethTweak2_LFace',
        'LeftUpTeethTweak_1_02_Ctrl': 'L_UpTeethTweak1_LFace',
        'LeftUpTeethTweak_1_03_Ctrl': 'R_UpTeethTweak2_LFace',
        'LeftUpTeethTweak_1_04_Ctrl': 'R_UpTeethTweak3_LFace',
        'LeftUpTeethTweak_1_Main_Ctrl': 'M_UpTeethMid_LFace',
        'R_DwMolar_A_Ctrl': 'R_LoMolarA',
        'R_DwMolar_B_Ctrl': 'R_LoMolarB',
        'R_LeftDwMolar_A_Ctrl': 'R_LoMolarA_LFace',
        'R_LeftDwMolar_B_Ctrl': 'R_LoMolarB_LFace',
        'R_LeftUpMolar_A_Ctrl': 'R_UpMolarA_LFace',
        'R_LeftUpMolar_B_Ctrl': 'R_UpMolarB_LFace',
        'R_RightDwMolar_A_Ctrl': 'R_LoMolarA_RFace',
        'R_RightDwMolar_B_Ctrl': 'R_LoMolarB_RFace',
        'R_RightUpMolar_A_Ctrl': 'R_UpMolarA_RFace',
        'R_RightUpMolar_B_Ctrl': 'R_UpMolarB_RFace',
        'R_UpMolar_A_Ctrl': 'R_UpMolarA',
        'R_UpMolar_B_Ctrl': 'R_UpMolarB',
        'UpTeethTweak_1_00_Ctrl': 'L_UpTeethTweak3',
        'UpTeethTweak_1_01_Ctrl': 'L_UpTeethTweak2',
        'UpTeethTweak_1_02_Ctrl': 'M_UpTeethTweak1',
        'UpTeethTweak_1_03_Ctrl': 'R_UpTeethTweak2',
        'UpTeethTweak_1_04_Ctrl': 'R_UpTeethTweak3',
        'UpTeethTweak_1_Main_Ctrl': 'M_UpTeethMid',
    },
    'Tongue': {
        'LeftTongue_01_Ctrl': 'M_LeftTongueBase',
        'LeftTongue_02_Ctrl': 'M_LeftTongueMid1',
        'LeftTongue_03_Ctrl': 'M_LeftTongueMid2',
        'LeftTongue_04_Ctrl': 'M_LeftTongueTip',
        'LeftTongue_Main_Ctrl': 'M_LeftTongueCurl',
        'LeftUvula_Mover_Ctrl': 'M_UvulaStart_LFace',
        'LeftUvula_Mid_Ctrl': 'M_Uvula_LFace',
        'LeftUvula_Start_Ctrl': 'M_UvulaBase_LFace',
        'RightTongue_01_Ctrl': 'M_RightTongueBase',
        'RightTongue_02_Ctrl': 'M_RightTongueMid1',
        'RightTongue_03_Ctrl': 'M_RightTongueMid2',
        'RightTongue_04_Ctrl': 'M_RightTongueTip',
        'RightTongue_Main_Ctrl': 'M_RightTongueCurl',
        'RightUvula_Mover_Ctrl': 'M_UvulaStart_RFace',
        'RightUvula_Mid_Ctrl': 'M_Uvula_RFace',
        'RightUvula_Start_Ctrl': 'M_UvulaBase_RFace',
        'Tongue_01_Ctrl': 'M_TongueBase',
        'Tongue_02_Ctrl': 'M_TongueMid1',
        'Tongue_03_Ctrl': 'M_TongueMid2',
        'Tongue_04_Ctrl': 'M_TongueTip',
        'Tongue_Main_Ctrl': 'M_TongueCurl',
        'Uvula_Mover_Ctrl': 'M_UvulaBase',
        'Uvula_Mid_Ctrl': 'M_UvulaMid',
        'Uvula_Start_Ctrl': 'M_UvulaStart',
    },
    'Brow': {
        'L_Brow_0_Ctrl': 'L_Brow0',
        'L_Brow_1_Ctrl': 'L_Brow1',
        'L_Brow_2_Ctrl': 'L_Brow2',
        'L_Brow_3_Ctrl': 'L_Brow3',
        'L_Brow_4_Ctrl': 'L_Brow4',
        'L_Brow_Ctrl': 'L_Brow',
        'L_Brow_Driver0_Main_Ctrl': 'L_BrowInner',
        'L_Brow_Driver1_Sec_Ctrl': 'L_BrowInMid',
        'L_Brow_Driver2_Main_Ctrl': 'L_BrowMiddle',
        'L_Brow_Driver3_Sec_Ctrl': 'L_BrowMidOut',
        'L_Brow_Driver4_Main_Ctrl': 'L_BrowOuter',
        'L_LeftBrow_0_Ctrl': 'L_LeftBrow0',
        'L_LeftBrow_1_Ctrl': 'L_LeftBrow1',
        'L_LeftBrow_2_Ctrl': 'L_LeftBrow2',
        'L_LeftBrow_3_Ctrl': 'L_LeftBrow3',
        'L_LeftBrow_4_Ctrl': 'L_LeftBrow4',
        'L_LeftBrow_Ctrl': 'L_LeftBrow',
        'L_LeftBrow_Driver0_Main_Ctrl': 'L_LeftBrowDriverMain0',
        'L_LeftBrow_Driver1_Sec_Ctrl': 'L_LeftBrowDriverSec1',
        'L_LeftBrow_Driver2_Main_Ctrl': 'L_LeftBrowDriverMain2',
        'L_LeftBrow_Driver3_Sec_Ctrl': 'L_LeftBrowDriverSec3',
        'L_LeftBrow_Driver4_Main_Ctrl': 'L_LeftBrowDriverMain4',
        'L_RightBrow_0_Ctrl': 'L_RightBrow0',
        'L_RightBrow_1_Ctrl': 'L_RightBrow1',
        'L_RightBrow_2_Ctrl': 'L_RightBrow2',
        'L_RightBrow_3_Ctrl': 'L_RightBrow3',
        'L_RightBrow_4_Ctrl': 'L_RightBrow4',
        'L_RightBrow_Ctrl': 'L_RightBrow',
        'L_RightBrow_Driver0_Main_Ctrl': 'L_RightBrowDriverMain0',
        'L_RightBrow_Driver1_Sec_Ctrl': 'L_RightBrowDriverSec1',
        'L_RightBrow_Driver2_Main_Ctrl': 'L_RightBrowDriverMain2',
        'L_RightBrow_Driver3_Sec_Ctrl': 'L_RightBrowDriverSec3',
        'L_RightBrow_Driver4_Main_Ctrl': 'L_RightBrowDriverMain4',
        'R_Brow_0_Ctrl': 'R_Brow0',
        'R_Brow_1_Ctrl': 'R_Brow1',
        'R_Brow_2_Ctrl': 'R_Brow2',
        'R_Brow_3_Ctrl': 'R_Brow3',
        'R_Brow_4_Ctrl': 'R_Brow4',
        'R_Brow_Ctrl': 'R_Brow',
        'R_Brow_Driver0_Main_Ctrl': 'R_BrowInner',
        'R_Brow_Driver1_Sec_Ctrl': 'R_BrowInMid',
        'R_Brow_Driver2_Main_Ctrl': 'R_BrowMiddle',
        'R_Brow_Driver3_Sec_Ctrl': 'R_BrowMidOut',
        'R_Brow_Driver4_Main_Ctrl': 'R_BrowOuter',
        'R_LeftBrow_0_Ctrl': 'R_LeftBrow0',
        'R_LeftBrow_1_Ctrl': 'R_LeftBrow1',
        'R_LeftBrow_2_Ctrl': 'R_LeftBrow2',
        'R_LeftBrow_3_Ctrl': 'R_LeftBrow3',
        'R_LeftBrow_4_Ctrl': 'R_LeftBrow4',
        'R_LeftBrow_Ctrl': 'R_LeftBrow',
        'R_LeftBrow_Driver0_Main_Ctrl': 'R_LeftBrowDriverMain0',
        'R_LeftBrow_Driver1_Sec_Ctrl': 'R_LeftBrowDriverSec1',
        'R_LeftBrow_Driver2_Main_Ctrl': 'R_LeftBrowDriverMain2',
        'R_LeftBrow_Driver3_Sec_Ctrl': 'R_LeftBrowDriverSec3',
        'R_LeftBrow_Driver4_Main_Ctrl': 'R_LeftBrowDriverMain4',
        'R_RightBrow_0_Ctrl': 'R_RightBrow0',
        'R_RightBrow_1_Ctrl': 'R_RightBrow1',
        'R_RightBrow_2_Ctrl': 'R_RightBrow2',
        'R_RightBrow_3_Ctrl': 'R_RightBrow3',
        'R_RightBrow_4_Ctrl': 'R_RightBrow4',
        'R_RightBrow_Ctrl': 'R_RightBrow',
        'R_RightBrow_Driver0_Main_Ctrl': 'R_RightBrowDriverMain0',
        'R_RightBrow_Driver1_Sec_Ctrl': 'R_RightBrowDriverSec1',
        'R_RightBrow_Driver2_Main_Ctrl': 'R_RightBrowDriverMain2',
        'R_RightBrow_Driver3_Sec_Ctrl': 'R_RightBrowDriverSec3',
        'R_RightBrow_Driver4_Main_Ctrl': 'R_RightBrowDriverMain4',
    },
    'Eye': {
        'Eyes_Global_Ctrl': 'M_EyesGlobal',
        'Eyes_Mover_Ctrl': 'M_EyesMover',
        'Eyes_Mover_Gimbal_Ctrl': 'M_EyesMoverGimbal',
        'EyesAim_Ctrl': 'M_EyesAim',
        'L_Eye_Jnt_Ctrl': 'L_EyeSocket',
        'R_Eye_Jnt_Ctrl': 'R_EyeSocket',
        'L_EyesOutFront_Ctrl': 'L_EyesOutFront',
        'L_EyesOutFrontPivot_Ctrl': 'L_EyesOutFrontPivot',
        'R_EyesOutFront_Ctrl': 'R_EyesOutFront',
        'R_EyesOutFrontPivot_Ctrl': 'R_EyesOutFrontPivot',
        'L_Squash_Ctrl': 'L_EyeSquash',
        'L_Squash_Deformer_Ctrl': 'L_EyeSquashPivot',
        'R_Squash_Ctrl': 'R_EyeSquash',
        'R_Squash_Deformer_Ctrl': 'R_EyeSquashPivot',
        'L_Blink_Frame_Ctrl': 'L_BlinkFrame',
        'R_Blink_Frame_Ctrl': 'R_BlinkFrame',
        'L_Up_Blink_Ctrl': 'L_UpBlink',
        'R_Up_Blink_Ctrl': 'R_UpBlink',
        'L_Dw_Blink_Ctrl': 'L_LoBlink',
        'R_Dw_Blink_Ctrl': 'R_LoBlink',
        'L_Up_Lid_Jnt_Ctrl': 'L_UpLid',
        'R_Up_Lid_Jnt_Ctrl': 'R_UpLid',
        'L_Dw_Lid_Jnt_Ctrl': 'L_LoLid',
        'R_Dw_Lid_Jnt_Ctrl': 'R_LoLid',
        'L_Up_01_Blink_End_Local_Ctrl': 'L_UpLidInner',
        'L_Up_02_Blink_End_Local_Ctrl': 'L_UpLidInMid',
        'L_Up_03_Blink_End_Local_Ctrl': 'L_UpLidMid',
        'L_Up_04_Blink_End_Local_Ctrl': 'L_UpLidMidOut',
        'L_Up_05_Blink_End_Local_Ctrl': 'L_UpLidOuter',
        'R_Up_01_Blink_End_Local_Ctrl': 'R_UpLidInner',
        'R_Up_02_Blink_End_Local_Ctrl': 'R_UpLidInMid',
        'R_Up_03_Blink_End_Local_Ctrl': 'R_UpLidMid',
        'R_Up_04_Blink_End_Local_Ctrl': 'R_UpLidMidOut',
        'R_Up_05_Blink_End_Local_Ctrl': 'R_UpLidOuter',
        'L_Top_0_Cls_Ctrl': 'L_UpEyeInner',
        'L_Top_1_Cls_Ctrl': 'L_UpEyeMid',
        'L_Top_2_Cls_Ctrl': 'L_UpEyeOuter',
        'L_Top_EyeTweak_Ctrl': 'L_UpEye',
        'R_Top_0_Cls_Ctrl': 'R_UpEyeInner',
        'R_Top_1_Cls_Ctrl': 'R_UpEyeMid',
        'R_Top_2_Cls_Ctrl': 'R_UpEyeOuter',
        'R_Top_EyeTweak_Ctrl': 'R_UpEye',
        'L_Dw_01_Blink_End_Local_Ctrl': 'L_LoLidInner',
        'L_Dw_02_Blink_End_Local_Ctrl': 'L_LoLidInMid',
        'L_Dw_03_Blink_End_Local_Ctrl': 'L_LoLidMid',
        'L_Dw_04_Blink_End_Local_Ctrl': 'L_LoLidMidOut',
        'L_Dw_05_Blink_End_Local_Ctrl': 'L_LoLidOuter',
        'R_Dw_01_Blink_End_Local_Ctrl': 'R_LoLidInner',
        'R_Dw_02_Blink_End_Local_Ctrl': 'R_LoLidInMid',
        'R_Dw_03_Blink_End_Local_Ctrl': 'R_LoLidMid',
        'R_Dw_04_Blink_End_Local_Ctrl': 'R_LoLidMidOut',
        'R_Dw_05_Blink_End_Local_Ctrl': 'R_LoLidOuter',
        'L_Btm_0_Cls_Ctrl': 'L_LoEyeInner',
        'L_Btm_1_Cls_Ctrl': 'L_LoEyeMid',
        'L_Btm_2_Cls_Ctrl': 'L_LoEyeOuter',
        'L_Btm_EyeTweak_Ctrl': 'L_LoEyeBottom',
        'R_Btm_0_Cls_Ctrl': 'R_LoEyeInner',
        'R_Btm_1_Cls_Ctrl': 'R_LoEyeMid',
        'R_Btm_2_Cls_Ctrl': 'R_LoEyeOuter',
        'R_Btm_EyeTweak_Ctrl': 'R_LoEyeBottom',
        'L_In_EyeTweak_Ctrl': 'L_InEye',
        'R_In_EyeTweak_Ctrl': 'R_InEye',
        'L_Out_EyeTweak_Ctrl': 'L_EyeOuter',
        'R_Out_EyeTweak_Ctrl': 'R_EyeOuter',
        'L_Mid_0_Cls_Ctrl': 'L_EyeTweakInner',
        'L_Mid_1_Cls_Ctrl': 'L_EyeTweakOuter',
        'R_Mid_0_Cls_Ctrl': 'R_EyeTweakInner',
        'R_Mid_1_Cls_Ctrl': 'R_EyeTweakOuter',
        'L_Pupil_Ctrl': 'L_Pupil',
        'R_Pupil_Ctrl': 'R_Pupil',
        'L_PupilOffset_Ctrl': 'L_PupilOffset',
        'R_PupilOffset_Ctrl': 'R_PupilOffset',
        'L_PupilSlide_Ctrl': 'L_PupilAim',
        'R_PupilSlide_Ctrl': 'R_PupilAim',
        'L_UpPupil_Jnt_Ctrl': 'L_UpPupil',
        'R_UpPupil_Jnt_Ctrl': 'R_UpPupil',
        'L_DwPupil_Jnt_Ctrl': 'L_LoPupil',
        'R_DwPupil_Jnt_Ctrl': 'R_LoPupil',
        'L_InPupil_Jnt4_Ctrl': 'L_InPupil',
        'R_InPupil_Jnt4_Ctrl': 'R_InPupil',
        'L_OutPupil_Jnt_Ctrl': 'L_OutPupil',
        'R_OutPupil_Jnt_Ctrl': 'R_OutPupil',
        'L_Pupil_SoftMod_Ctrl': 'L_PupilSoftMod',
        'L_Pupil_SoftMod_Pivot_Ctrl': 'L_PupilSoftModPivot',
        'Loc_L_Pupil_SoftMod_Ctrl': 'L_LocPupilSoftMod',
        'R_Pupil_SoftMod_Ctrl': 'R_PupilSoftMod',
        'R_Pupil_SoftMod_Pivot_Ctrl': 'R_PupilSoftModPivot',
        'Loc_R_Pupil_SoftMod_Ctrl': 'R_LocPupilSoftMod',
    },
    'Mouth': {
        'M_Mouth_Rotator_Ctrl': 'M_Mouth',
        'R_Mouth_Rotator_Ctrl': 'M_Mouth_RFace',
        'L_Mouth_Rotator_Ctrl': 'M_Mouth_LFace',
        'C_MoutMoverLocal_Ctrl': 'C_MouthMover',
        'R_MoutMoverLocal_Ctrl': 'R_MouthMover',
        'L_MoutMoverLocal_Ctrl': 'L_MouthMover',
        'Dw_Fr_MouthTweak_Ctrl': 'M_LoMouthTweak',
        'Dw_LeftLip_A_Ctrl': 'M_LoLeftLipA',
        'Dw_LeftLipEndSlide_Ctrl': 'M_LoLeftLipEndSlide',
        'Dw_LeftLipMidSlide_Ctrl': 'M_LoLeftLipMidSlide',
        'Dw_LeftLipSlide_Ctrl': 'M_LoLeftLipSlide',
        'Dw_Lip_A_Ctrl': 'M_LoLipMid',
        'Dw_LipEndSlide_Ctrl': 'M_LoLipEndSlide',
        'Dw_LipMidSlide_Ctrl': 'M_LoLipMidSlide',
        'Dw_LipSlide_Ctrl': 'M_LoLipSlide',
        'Dw_RightLip_A_Ctrl': 'M_LoRightLipA',
        'Dw_RightLipEndSlide_Ctrl': 'M_LoRightLipEndSlide',
        'Dw_RightLipMidSlide_Ctrl': 'M_LoRightLipMidSlide',
        'Dw_RightLipSlide_Ctrl': 'M_LoRightLipSlide',
        'DwLeft_Left_MouthTweak_Ctrl': 'L_LoLeftMouthTweak',
        'DwRight_Right_MouthTweak_Ctrl': 'R_LoRightMouthTweak',
        'Fr_Dw_LeftLip_Ctrl': 'M_LoLip_LFace',
        'Fr_Dw_Lip_Ctrl': 'M_LoLip',
        'Fr_Dw_RightLip_Ctrl': 'M_LoLip_RFace',
        'Fr_Up_LeftLip_Ctrl': 'M_UpLip_LFace',
        'Fr_Up_Lip_Ctrl': 'M_UpLip',
        'Fr_Up_RightLip_Ctrl': 'M_UpLip_RFace',
        'L_Corner_Fr_MouthTweak_Ctrl': 'L_CornerMouthTweak',
        'L_Dw_01_Fr_MouthTweak_Ctrl': 'L_LoMouthTweak1',
        'L_Dw_02_Fr_MouthTweak_Ctrl': 'L_LoMouthTweak2',
        'L_Dw_03_Fr_MouthTweak_Ctrl': 'L_LoMouthTweak3',
        'L_Dw_LeftLipEndSlide_Ctrl': 'L_LoLeftLipEndSlide',
        'L_Dw_LeftLipMidSlide_Ctrl': 'L_LoLeftLipMidSlide',
        'L_Dw_LeftLipSlide_Ctrl': 'L_LoLeftLipSlide',
        'L_Dw_LipEndSlide_Ctrl': 'L_LoLipEndSlide',
        'L_Dw_LipMidSlide_Ctrl': 'L_LoLipMidSlide',
        'L_Dw_LipSlide_Ctrl': 'L_LoLipSlide',
        'L_Dw_RightLipEndSlide_Ctrl': 'L_LoRightLipEndSlide',
        'L_Dw_RightLipMidSlide_Ctrl': 'L_LoRightLipMidSlide',
        'L_Dw_RightLipSlide_Ctrl': 'L_LoRightLipSlide',
        'L_DwLeftLip_A_Ctrl': 'L_LoLeftLipA',
        'L_DwLeftLipMid01_Ctrl': 'L_LoLeftLipMid1',
        'L_DwLeftLipMid02_Ctrl': 'L_LoLeftLipMid2',
        'L_DwLip_A_Ctrl': 'L_LoLip1',
        'L_DwLipMid01_Ctrl': 'L_LoLip3',
        'L_DwLipMid02_Ctrl': 'L_LoLip2',
        'L_DwMid01_LeftLipSlide_Ctrl': 'L_LoMid1_LeftLipSlide',
        'L_DwMid01_LipSlide_Ctrl': 'L_LoMid1_LipSlide',
        'L_DwMid01_RightLipSlide_Ctrl': 'L_LoMid1_RightLipSlide',
        'L_DwMid02_LeftLipSlide_Ctrl': 'L_LoMid2_LeftLipSlide',
        'L_DwMid02_LipSlide_Ctrl': 'L_LoMid2_LipSlide',
        'L_DwMid02_RightLipSlide_Ctrl': 'L_LoMid2_RightLipSlide',
        'L_DwRightLip_A_Ctrl': 'L_LoRightLipA',
        'L_DwRightLipMid01_Ctrl': 'L_LoRightLipMid1',
        'L_DwRightLipMid02_Ctrl': 'L_LoRightLipMid2',
        'L_Fr_LeftLip_Ctrl': 'L_Mouth_LFace',
        'L_Fr_Lip_Ctrl': 'L_Mouth',
        'L_Fr_RightLip_Ctrl': 'L_Mouth_RFace',
        'L_LeftCorner_Left_MouthTweak_Ctrl': 'L_LeftCornerLeftMouthTweak',
        'L_LeftDw_01_Left_MouthTweak_Ctrl': 'L_LeftDwLeftMouthTweak1',
        'L_LeftDw_02_Left_MouthTweak_Ctrl': 'L_LeftDwLeftMouthTweak2',
        'L_LeftDw_03_Left_MouthTweak_Ctrl': 'L_LeftDwLeftMouthTweak3',
        'L_LeftLip_A_Ctrl': 'L_LeftLipA',
        'L_LeftLipEndSlide_Ctrl': 'L_LeftLipEndSlide',
        'L_LeftLipMidSlide_Ctrl': 'L_LeftLipMidSlide',
        'L_LeftLipSlide_Ctrl': 'L_LeftLipSlide',
        'L_LeftUp_01_Left_MouthTweak_Ctrl': 'L_LeftUpLeftMouthTweak1',
        'L_LeftUp_02_Left_MouthTweak_Ctrl': 'L_LeftUpLeftMouthTweak2',
        'L_LeftUp_03_Left_MouthTweak_Ctrl': 'L_LeftUpLeftMouthTweak3',
        'L_Lip_A_Ctrl': 'L_OutLip',
        'L_LipEndSlide_Ctrl': 'L_LipEndSlide',
        'L_LipMidSlide_Ctrl': 'L_LipMidSlide',
        'L_LipSlide_Ctrl': 'L_LipSlide',
        'L_LwrWrapSlide_Ctrl': 'L_LwrWrapSlide',
        'L_RightCorner_Right_MouthTweak_Ctrl': 'L_RightCornerRightMouthTweak',
        'L_RightDw_01_Right_MouthTweak_Ctrl': 'L_RightDwRightMouthTweak1',
        'L_RightDw_02_Right_MouthTweak_Ctrl': 'L_RightDwRightMouthTweak2',
        'L_RightDw_03_Right_MouthTweak_Ctrl': 'L_RightDwRightMouthTweak3',
        'L_RightLip_A_Ctrl': 'L_RightLipA',
        'L_RightLipEndSlide_Ctrl': 'L_RightLipEndSlide',
        'L_RightLipMidSlide_Ctrl': 'L_RightLipMidSlide',
        'L_RightLipSlide_Ctrl': 'L_RightLipSlide',
        'L_RightUp_01_Right_MouthTweak_Ctrl': 'L_RightUpRightMouthTweak1',
        'L_RightUp_02_Right_MouthTweak_Ctrl': 'L_RightUpRightMouthTweak2',
        'L_RightUp_03_Right_MouthTweak_Ctrl': 'L_RightUpRightMouthTweak3',
        'L_Up_01_Fr_MouthTweak_Ctrl': 'L_UpMouthTweak3',
        'L_Up_02_Fr_MouthTweak_Ctrl': 'L_UpMouthTweak2',
        'L_Up_03_Fr_MouthTweak_Ctrl': 'L_UpMouthTweak1',
        'L_Up_LeftLipEndSlide_Ctrl': 'L_UpLeftLipEndSlide',
        'L_Up_LeftLipMidSlide_Ctrl': 'L_UpLeftLipMidSlide',
        'L_Up_LeftLipSlide_Ctrl': 'L_UpLeftLipSlide',
        'L_Up_LipEndSlide_Ctrl': 'L_UpLipEndSlide',
        'L_Up_LipMidSlide_Ctrl': 'L_UpLipMidSlide',
        'L_Up_LipSlide_Ctrl': 'L_UpLipSlide',
        'L_Up_RightLipEndSlide_Ctrl': 'L_UpRightLipEndSlide',
        'L_Up_RightLipMidSlide_Ctrl': 'L_UpRightLipMidSlide',
        'L_Up_RightLipSlide_Ctrl': 'L_UpRightLipSlide',
        'L_UpLeftLip_A_Ctrl': 'L_UpLeftLipA',
        'L_UpLeftLipMid01_Ctrl': 'L_UpLeftLipMid1',
        'L_UpLeftLipMid02_Ctrl': 'L_UpLeftLipMid2',
        'L_UpLip_A_Ctrl': 'L_UpLip2',
        'L_UpLipMid01_Ctrl': 'L_UpLip3',
        'L_UpLipMid02_Ctrl': 'L_UpLip1',
        'L_UpMid01_LeftLipSlide_Ctrl': 'L_UpMid1_LeftLipSlide',
        'L_UpMid01_LipSlide_Ctrl': 'L_UpMid1_LipSlide',
        'L_UpMid01_RightLipSlide_Ctrl': 'L_UpMid1_RightLipSlide',
        'L_UpMid02_LeftLipSlide_Ctrl': 'L_UpMid2_LeftLipSlide',
        'L_UpMid02_LipSlide_Ctrl': 'L_UpMid2_LipSlide',
        'L_UpMid02_RightLipSlide_Ctrl': 'L_UpMid2_RightLipSlide',
        'L_UpRightLip_A_Ctrl': 'L_UpRightLipA',
        'L_UpRightLipMid01_Ctrl': 'L_UpRightLipMid1',
        'L_UpRightLipMid02_Ctrl': 'L_UpRightLipMid2',
        'L_UprWrapSlide_Ctrl': 'L_UprWrapSlide',
        'LeftUp_Left_MouthTweak_Ctrl': 'L_UpLeftMouthTweak',
        'Mouth_Rotator_Ctrl': 'M_MouthRotator',
        'R_Corner_Fr_MouthTweak_Ctrl': 'R_CornerMouthTweak',
        'R_Dw_01_Fr_MouthTweak_Ctrl': 'R_LoMouthTweak1',
        'R_Dw_02_Fr_MouthTweak_Ctrl': 'R_LoMouthTweak2',
        'R_Dw_03_Fr_MouthTweak_Ctrl': 'R_LoMouthTweak3',
        'R_Dw_LeftLipEndSlide_Ctrl': 'R_LoLeftLipEndSlide',
        'R_Dw_LeftLipMidSlide_Ctrl': 'R_LoLeftLipMidSlide',
        'R_Dw_LeftLipSlide_Ctrl': 'R_LoLeftLipSlide',
        'R_Dw_LipEndSlide_Ctrl': 'R_LoLipEndSlide',
        'R_Dw_LipMidSlide_Ctrl': 'R_LoLipMidSlide',
        'R_Dw_LipSlide_Ctrl': 'R_LoLipSlide',
        'R_Dw_RightLipEndSlide_Ctrl': 'R_LoRightLipEndSlide',
        'R_Dw_RightLipMidSlide_Ctrl': 'R_LoRightLipMidSlide',
        'R_Dw_RightLipSlide_Ctrl': 'R_LoRightLipSlide',
        'R_DwLeftLip_A_Ctrl': 'R_LoLeftLipA',
        'R_DwLeftLipMid01_Ctrl': 'R_LoLeftLipMid1',
        'R_DwLeftLipMid02_Ctrl': 'R_LoLeftLipMid2',
        'R_DwLip_A_Ctrl': 'R_LoLip1',
        'R_DwLipMid01_Ctrl': 'R_LoLip3',
        'R_DwLipMid02_Ctrl': 'R_LoLip2',
        'R_DwMid01_LeftLipSlide_Ctrl': 'R_LoMid1_LeftLipSlide',
        'R_DwMid01_LipSlide_Ctrl': 'R_LoMid1_LipSlide',
        'R_DwMid01_RightLipSlide_Ctrl': 'R_LoMid1_RightLipSlide',
        'R_DwMid02_LeftLipSlide_Ctrl': 'R_LoMid2_LeftLipSlide',
        'R_DwMid02_LipSlide_Ctrl': 'R_LoMid2_LipSlide',
        'R_DwMid02_RightLipSlide_Ctrl': 'R_LoMid2_RightLipSlide',
        'R_DwRightLip_A_Ctrl': 'R_LoRightLipA',
        'R_DwRightLipMid01_Ctrl': 'R_LoRightLipMid1',
        'R_DwRightLipMid02_Ctrl': 'R_LoRightLipMid2',
        'R_Fr_LeftLip_Ctrl': 'R_Mouth_LFace',
        'R_Fr_Lip_Ctrl': 'R_Mouth',
        'R_Fr_RightLip_Ctrl': 'R_Mouth_RFace',
        'R_LeftCorner_Left_MouthTweak_Ctrl': 'R_LeftCornerLeftMouthTweak',
        'R_LeftDw_01_Left_MouthTweak_Ctrl': 'R_LeftDwLeftMouthTweak1',
        'R_LeftDw_02_Left_MouthTweak_Ctrl': 'R_LeftDwLeftMouthTweak2',
        'R_LeftDw_03_Left_MouthTweak_Ctrl': 'R_LeftDwLeftMouthTweak3',
        'R_LeftLip_A_Ctrl': 'R_LeftLipA',
        'R_LeftLipEndSlide_Ctrl': 'R_LeftLipEndSlide',
        'R_LeftLipMidSlide_Ctrl': 'R_LeftLipMidSlide',
        'R_LeftLipSlide_Ctrl': 'R_LeftLipSlide',
        'R_LeftUp_01_Left_MouthTweak_Ctrl': 'R_LeftUpLeftMouthTweak1',
        'R_LeftUp_02_Left_MouthTweak_Ctrl': 'R_LeftUpLeftMouthTweak2',
        'R_LeftUp_03_Left_MouthTweak_Ctrl': 'R_LeftUpLeftMouthTweak3',
        'R_Lip_A_Ctrl': 'R_LipA',
        'R_LipEndSlide_Ctrl': 'R_LipEndSlide',
        'R_LipMidSlide_Ctrl': 'R_LipMidSlide',
        'R_LipSlide_Ctrl': 'R_LipSlide',
        'R_LwrWrapSlide_Ctrl': 'R_LwrWrapSlide',
        'R_RightCorner_Right_MouthTweak_Ctrl': 'R_RightCornerRightMouthTweak',
        'R_RightDw_01_Right_MouthTweak_Ctrl': 'R_RightDwRightMouthTweak1',
        'R_RightDw_02_Right_MouthTweak_Ctrl': 'R_RightDwRightMouthTweak2',
        'R_RightDw_03_Right_MouthTweak_Ctrl': 'R_RightDwRightMouthTweak3',
        'R_RightLip_A_Ctrl': 'R_RightLipA',
        'R_RightLipEndSlide_Ctrl': 'R_RightLipEndSlide',
        'R_RightLipMidSlide_Ctrl': 'R_RightLipMidSlide',
        'R_RightLipSlide_Ctrl': 'R_RightLipSlide',
        'R_RightUp_01_Right_MouthTweak_Ctrl': 'R_RightUpRightMouthTweak1',
        'R_RightUp_02_Right_MouthTweak_Ctrl': 'R_RightUpRightMouthTweak2',
        'R_RightUp_03_Right_MouthTweak_Ctrl': 'R_RightUpRightMouthTweak3',
        'R_Up_01_Fr_MouthTweak_Ctrl': 'R_UpMouthTweak3',
        'R_Up_02_Fr_MouthTweak_Ctrl': 'R_UpMouthTweak2',
        'R_Up_03_Fr_MouthTweak_Ctrl': 'R_UpMouthTweak1',
        'R_Up_LeftLipEndSlide_Ctrl': 'R_UpLeftLipEndSlide',
        'R_Up_LeftLipMidSlide_Ctrl': 'R_UpLeftLipMidSlide',
        'R_Up_LeftLipSlide_Ctrl': 'R_UpLeftLipSlide',
        'R_Up_LipEndSlide_Ctrl': 'R_UpLipEndSlide',
        'R_Up_LipMidSlide_Ctrl': 'R_UpLipMidSlide',
        'R_Up_LipSlide_Ctrl': 'R_UpLipSlide',
        'R_Up_RightLipEndSlide_Ctrl': 'R_UpRightLipEndSlide',
        'R_Up_RightLipMidSlide_Ctrl': 'R_UpRightLipMidSlide',
        'R_Up_RightLipSlide_Ctrl': 'R_UpRightLipSlide',
        'R_UpLeftLip_A_Ctrl': 'R_UpLeftLipA',
        'R_UpLeftLipMid01_Ctrl': 'R_UpLeftLipMid1',
        'R_UpLeftLipMid02_Ctrl': 'R_UpLeftLipMid2',
        'R_UpLip_A_Ctrl': 'R_UpLip2',
        'R_UpLipMid01_Ctrl': 'R_UpLip3',
        'R_UpLipMid02_Ctrl': 'R_UpLip1',
        'R_UpMid01_LeftLipSlide_Ctrl': 'R_UpMid1_LeftLipSlide',
        'R_UpMid01_LipSlide_Ctrl': 'R_UpMid1_LipSlide',
        'R_UpMid01_RightLipSlide_Ctrl': 'R_UpMid1_RightLipSlide',
        'R_UpMid02_LeftLipSlide_Ctrl': 'R_UpMid2_LeftLipSlide',
        'R_UpMid02_LipSlide_Ctrl': 'R_UpMid2_LipSlide',
        'R_UpMid02_RightLipSlide_Ctrl': 'R_UpMid2_RightLipSlide',
        'R_UpRightLip_A_Ctrl': 'R_UpRightLipA',
        'R_UpRightLipMid01_Ctrl': 'R_UpRightLipMid1',
        'R_UpRightLipMid02_Ctrl': 'R_UpRightLipMid2',
        'R_UprWrapSlide_Ctrl': 'R_UprWrapSlide',
        'RightUp_Right_MouthTweak_Ctrl': 'R_RightUpMouthTweak',
        'Up_Fr_MouthTweak_Ctrl': 'M_UpMouthTweakMid',
        'Up_LeftLip_A_Ctrl': 'M_UpLeftLipA',
        'Up_LeftLipEndSlide_Ctrl': 'M_UpLeftLipEndSlide',
        'Up_LeftLipMidSlide_Ctrl': 'M_UpLeftLipMidSlide',
        'Up_LeftLipSlide_Ctrl': 'M_UpLeftLipSlide',
        'Up_Lip_A_Ctrl': 'M_UpLipMid',
        'Up_LipEndSlide_Ctrl': 'M_UpLipEndSlide',
        'Up_LipMidSlide_Ctrl': 'M_UpLipMidSlide',
        'Up_LipSlide_Ctrl': 'M_UpLipSlide',
        'Up_RightLip_A_Ctrl': 'M_UpRightLipA',
        'Up_RightLipEndSlide_Ctrl': 'M_UpRightLipEndSlide',
        'Up_RightLipMidSlide_Ctrl': 'M_UpRightLipMidSlide',
        'Up_RightLipSlide_Ctrl': 'M_UpRightLipSlide',
    },
    'Arm': {
        'L_ArmSwing_Ctrl': 'L_ArmSwing',
        'L_Clavicle_Ctrl': 'L_Clavicle',
        'L_Elbow_Bottom_Handle_Ctrl': 'L_ElbowBottomHandle',
        'L_Elbow_Ctrl_0_Ctrl': 'L_Elbow0',
        'L_Elbow_Ctrl_1_Ctrl': 'L_Elbow1',
        'L_Elbow_Ctrl_2_Ctrl': 'L_Elbow2',
        'L_Elbow_Fk_Ctrl': 'L_ElbowFK',
        'L_Elbow_Top_Handle_Ctrl': 'L_ElbowTopHandle',
        'L_ElbowEnd_Bendy_Ctrl': 'L_ElbowEndBendy',
        'L_ElbowMid_Bendy_Ctrl': 'L_ElbowMidBendy',
        'L_ElbowStart_Bendy_Ctrl': 'L_ElbowStartBendy',
        'L_Shoulder_Bottom_Handle_Ctrl': 'L_ShoulderBottomHandle',
        'L_Shoulder_Ctrl_0_Ctrl': 'L_Shoulder0',
        'L_Shoulder_Ctrl_1_Ctrl': 'L_Shoulder1',
        'L_Shoulder_Ctrl_2_Ctrl': 'L_Shoulder2',
        'L_Shoulder_Fk_Ctrl': 'L_ShoulderFK',
        'L_Shoulder_Ik_Ctrl': 'L_ShoulderIK',
        'L_Shoulder_Jnt_Switch_Ctrl': 'L_Arm',
        'L_Shoulder_Top_Handle_Ctrl': 'L_ShoulderTopHandle',
        'L_ShoulderEnd_Bendy_Ctrl': 'L_ShoulderEndBendy',
        'L_ShoulderStart_Bendy_Ctrl': 'L_ShoulderStartBendy',
        'R_ArmSwing_Ctrl': 'R_ArmSwing',
        'R_Clavicle_Ctrl': 'R_Clavicle',
        'R_Elbow_Bottom_Handle_Ctrl': 'R_ElbowBottomHandle',
        'R_Elbow_Ctrl_0_Ctrl': 'R_Elbow0',
        'R_Elbow_Ctrl_1_Ctrl': 'R_Elbow1',
        'R_Elbow_Ctrl_2_Ctrl': 'R_Elbow2',
        'R_Elbow_Fk_Ctrl': 'R_ElbowFK',
        'R_Elbow_Top_Handle_Ctrl': 'R_ElbowTopHandle',
        'R_ElbowEnd_Bendy_Ctrl': 'R_ElbowEndBendy',
        'R_ElbowMid_Bendy_Ctrl': 'R_ElbowMidBendy',
        'R_ElbowStart_Bendy_Ctrl': 'R_ElbowStartBendy',
        'R_Shoulder_Bottom_Handle_Ctrl': 'R_ShoulderBottomHandle',
        'R_Shoulder_Ctrl_0_Ctrl': 'R_Shoulder0',
        'R_Shoulder_Ctrl_1_Ctrl': 'R_Shoulder1',
        'R_Shoulder_Ctrl_2_Ctrl': 'R_Shoulder2',
        'R_Shoulder_Fk_Ctrl': 'R_ShoulderFK',
        'R_Shoulder_Ik_Ctrl': 'R_ShoulderIK',
        'R_Shoulder_Jnt_Switch_Ctrl': 'R_Arm',
        'R_Shoulder_Top_Handle_Ctrl': 'R_ShoulderTopHandle',
        'R_ShoulderEnd_Bendy_Ctrl': 'R_ShoulderEndBendy',
        'R_ShoulderStart_Bendy_Ctrl': 'R_ShoulderStartBendy',
    },
    'Hand': {
        'L_Hand_Index_00_Ctrl': 'L_IndexMeta',
        'L_Hand_Index_01_Ctrl': 'L_IndexBase',
        'L_Hand_Index_02_Ctrl': 'L_IndexMid',
        'L_Hand_Index_03_Ctrl': 'L_IndexTip',
        'L_Hand_InnerCup_Ctrl': 'L_ThumbCup',
        'L_Hand_Middle_00_Ctrl': 'L_MiddleMeta',
        'L_Hand_Middle_01_Ctrl': 'L_MiddleBase',
        'L_Hand_Middle_02_Ctrl': 'L_MiddleMid',
        'L_Hand_Middle_03_Ctrl': 'L_MiddleTip',
        'L_Hand_Middle_03_Smart_Ctrl': 'L_FingersSmart',
        'L_Hand_OutterCup_Ctrl': 'L_PinkieCup',
        'L_Hand_Palm_Ctrl': 'L_Fingers',
        'L_Hand_Pinky_00_Ctrl': 'L_PinkyMeta',
        'L_Hand_Pinky_01_Ctrl': 'L_PinkyBase',
        'L_Hand_Pinky_02_Ctrl': 'L_PinkyMid',
        'L_Hand_Pinky_03_Ctrl': 'L_PinkyTip',
        'L_Hand_Thumb_00_Ctrl': 'L_ThumbMeta',
        'L_Hand_Thumb_01_Ctrl': 'L_ThumbBase',
        'L_Hand_Thumb_02_Ctrl': 'L_ThumbMid',
        'L_Hand_Wrist_Ctrl': 'L_Wrist',
        'L_Wrist_Fk_Ctrl': 'L_HandFK',
        'L_Wrist_Ik_Ctrl': 'L_Hand',
        'L_Wrist_Ik_PoleVector_Ctrl': 'L_WristIKPV',
        'L_Wrist_SubIk_Ctrl': 'L_WristSubIK',
        'R_Hand_Index_00_Ctrl': 'R_IndexMeta',
        'R_Hand_Index_01_Ctrl': 'R_IndexBase',
        'R_Hand_Index_02_Ctrl': 'R_IndexMid',
        'R_Hand_Index_03_Ctrl': 'R_IndexTip',
        'R_Hand_InnerCup_Ctrl': 'R_ThumbCup',
        'R_Hand_Middle_00_Ctrl': 'R_MiddleMeta',
        'R_Hand_Middle_01_Ctrl': 'R_MiddleBase',
        'R_Hand_Middle_02_Ctrl': 'R_MiddleMid',
        'R_Hand_Middle_03_Ctrl': 'R_MiddleTip',
        'R_Hand_Middle_03_Smart_Ctrl': 'R_FingersSmart',
        'R_Hand_OutterCup_Ctrl': 'R_PinkieCup',
        'R_Hand_Palm_Ctrl': 'R_Fingers',
        'R_Hand_Pinky_00_Ctrl': 'R_PinkyMeta',
        'R_Hand_Pinky_01_Ctrl': 'R_PinkyBase',
        'R_Hand_Pinky_02_Ctrl': 'R_PinkyMid',
        'R_Hand_Pinky_03_Ctrl': 'R_PinkyTip',
        'R_Hand_Thumb_00_Ctrl': 'R_ThumbMeta',
        'R_Hand_Thumb_01_Ctrl': 'R_ThumbBase',
        'R_Hand_Thumb_02_Ctrl': 'R_ThumbMid',
        'R_Hand_Wrist_Ctrl': 'R_Wrist',
        'R_Wrist_Fk_Ctrl': 'R_HandFK',
        'R_Wrist_Ik_Ctrl': 'R_Hand',
        'R_Wrist_Ik_PoleVector_Ctrl': 'R_WristIKPV',
        'R_Wrist_SubIk_Ctrl': 'R_WristSubIK',
    },
    'Leg': {
        'L_Ankle_Fk_Ctrl': 'L_FootFK',
        'L_Ankle_Ik_Ctrl': 'L_Foot',
        'L_Ankle_Ik_PoleVector_Ctrl': 'L_LegPV',
        'L_Ankle_Ik_RFL_Ctrl': 'L_FootIKRFL',
        'L_Ankle_SubIk_Ctrl': 'L_FootGimbleIK',
        'L_BkSandal_Ctrl': 'L_SandalBall',
        'L_BkSandal_End_Ctrl': 'L_SandalBack',
        'L_BkSandal_Mid_Ctrl': 'L_SandalMid',
        'L_Butt_A_Ctrl': 'L_ButtA',
        'L_Butt_B_Ctrl': 'L_ButtB',
        'L_Foot_Scale_Ctrl': 'L_FootScale',
        'L_Foot_Toes_Ctrl': 'L_FootToes',
        'L_FrSandal_Ctrl': 'L_FrSandal',
        'L_Hip_Bottom_Handle_Ctrl': 'L_KneeUpHandle',
        'L_Hip_Ctrl_0_Ctrl': 'L_LegBend1',
        'L_Hip_Ctrl_1_Ctrl': 'L_LegBend2',
        'L_Hip_Ctrl_2_Ctrl': 'L_LegBend3',
        'L_Hip_Fk_Ctrl': 'L_HipFK',
        'L_Hip_Ik_Ctrl': 'L_HipIK',
        'L_Hip_Jnt_Switch_Ctrl': 'L_Leg',
        'L_Hip_Top_Handle_Ctrl': 'L_HipTopHandle',
        'L_HipEnd_Bendy_Ctrl': 'L_KneeUpBendy',
        'L_HipStart_Bendy_Ctrl': 'L_LegStartBendy',
        'L_Knee_Bottom_Handle_Ctrl': 'L_KneeBottomHandle',
        'L_Knee_Ctrl_0_Ctrl': 'L_LegBend4',
        'L_Knee_Ctrl_1_Ctrl': 'L_LegBend5',
        'L_Knee_Ctrl_2_Ctrl': 'L_LegBend6',
        'L_Knee_Fk_Ctrl': 'L_Knee',
        'L_Knee_Top_Handle_Ctrl': 'L_KneeTopHandle',
        'L_KneeEnd_Bendy_Ctrl': 'L_KneeEndBendy',
        'L_KneeMid_Bendy_Ctrl': 'L_KneeMidBendy',
        'L_KneeStart_Bendy_Ctrl': 'L_KneeStartBendy',
        'L_Pelvis_Ctrl': 'L_Hip',
        'L_Sandal_Ctrl': 'L_Sandal',
        'L_SandalStrap_Ctrl': 'L_SandalStrap',
        'L_Toes_A_01_Ctrl': 'L_BigToeBase',
        'L_Toes_A_02_Ctrl': 'L_BigToeMid',
        'L_Toes_B_01_Ctrl': 'L_MiddleToeBase',
        'L_Toes_B_02_Ctrl': 'L_MiddleToeMid',
        'L_Toes_C_01_Ctrl': 'L_PinkyToeBase',
        'L_Toes_C_02_Ctrl': 'L_PinkyToeMid',
        'R_Ankle_Fk_Ctrl': 'R_FootFK',
        'R_Ankle_Ik_Ctrl': 'R_Foot',
        'R_Ankle_Ik_PoleVector_Ctrl': 'R_LegPV',
        'R_Ankle_Ik_RFL_Ctrl': 'R_FootIKRFL',
        'R_Ankle_SubIk_Ctrl': 'R_FootGimbleIK',
        'R_BkSandal_Ctrl': 'R_SandalBall',
        'R_BkSandal_End_Ctrl': 'R_SandalBack',
        'R_BkSandal_Mid_Ctrl': 'R_SandalMid',
        'R_Butt_A_Ctrl': 'R_ButtA',
        'R_Butt_B_Ctrl': 'R_ButtB',
        'R_Foot_Scale_Ctrl': 'R_FootScale',
        'R_Foot_Toes_Ctrl': 'R_FootToes',
        'R_FrSandal_Ctrl': 'R_FrSandal',
        'R_Hip_Bottom_Handle_Ctrl': 'R_KneeUpHandle',
        'R_Hip_Ctrl_0_Ctrl': 'R_LegBend1',
        'R_Hip_Ctrl_1_Ctrl': 'R_LegBend2',
        'R_Hip_Ctrl_2_Ctrl': 'R_LegBend3',
        'R_Hip_Fk_Ctrl': 'R_HipFK',
        'R_Hip_Ik_Ctrl': 'R_HipIK',
        'R_Hip_Jnt_Switch_Ctrl': 'R_Leg',
        'R_Hip_Top_Handle_Ctrl': 'R_HipTopHandle',
        'R_HipEnd_Bendy_Ctrl': 'R_KneeUpBendy',
        'R_HipStart_Bendy_Ctrl': 'R_LegStartBendy',
        'R_Knee_Bottom_Handle_Ctrl': 'R_KneeBottomHandle',
        'R_Knee_Ctrl_0_Ctrl': 'R_LegBend4',
        'R_Knee_Ctrl_1_Ctrl': 'R_LegBend5',
        'R_Knee_Ctrl_2_Ctrl': 'R_LegBend6',
        'R_Knee_Fk_Ctrl': 'R_Knee',
        'R_Knee_Top_Handle_Ctrl': 'R_KneeTopHandle',
        'R_KneeEnd_Bendy_Ctrl': 'R_KneeEndBendy',
        'R_KneeMid_Bendy_Ctrl': 'R_KneeMidBendy',
        'R_KneeStart_Bendy_Ctrl': 'R_KneeStartBendy',
        'R_Pelvis_Ctrl': 'R_Hip',
        'R_Sandal_Ctrl': 'R_Sandal',
        'R_SandalStrap_Ctrl': 'R_SandalStrap',
        'R_Toes_A_01_Ctrl': 'R_BigToeBase',
        'R_Toes_A_02_Ctrl': 'R_BigToeMid',
        'R_Toes_B_01_Ctrl': 'R_MiddleToeBase',
        'R_Toes_B_02_Ctrl': 'R_MiddleToeMid',
        'R_Toes_C_01_Ctrl': 'R_PinkyToeBase',
        'R_Toes_C_02_Ctrl': 'R_PinkyToeMid',
    },
    'Cap': {
        'Cap_A_Ctrl': 'M_CapBase',
        'Cap_B_Ctrl': 'M_CapBrimBase',
        'Cap_C_Ctrl': 'M_CapBrimMid',
        'Cap_D_Ctrl': 'M_CapBrimEnd',
        'Cap_Top_Ctrl': 'M_CapTop',
    },
}

#---------------------------------------------

def _flatten_mapping(data):
    flat = {}
    for key, value in data.items():
        if isinstance(value, dict):
            flat.update(_flatten_mapping(value))
        else:
            flat[key] = value
    return flat


def _match_prefix(name, table):
    """Return (matched_key, remaining_suffix) or (None, None).

    Exact name first, then progressively shorter leading token runs on '_'
    boundaries, so the LONGEST matching key wins. "L_Ankle_Fk_Ctrl_Offset_Grp"
    matches "L_Ankle_Fk_Ctrl" and keeps "_Offset_Grp"; "Jaw_Ctrl" inside
    "Dinamic_Pivot_Jaw_Ctrl" does NOT match.
    """
    if name in table:
        return name, ''
    parts = name.split('_')
    for i in range(len(parts) - 1, 0, -1):
        prefix = '_'.join(parts[:i])
        if prefix in table:
            return prefix, name[len(prefix):]
    return None, None


def _under_excluded(full_path):
    # ancestors only -- the leaf is the node being renamed
    for seg in full_path.split('|')[:-1]:
        if seg.split(':')[-1] in EXCLUDE_GROUPS:
            return True
    return False


def rename_nodes():
    mapping = _flatten_mapping(NAME_MAPPING)

    # Shapes are skipped -- Maya renames them with their transform.
    nodes = cmds.ls(type=['transform', 'joint'], long=True) or []
    nodes = [n for n in nodes if not cmds.objectType(n, isAType='shape')]
    nodes = [n for n in nodes if not _under_excluded(n)]
    # deepest first so parent paths stay valid while renaming
    nodes.sort(key=lambda x: x.count('|'), reverse=True)

    renamed = 0
    for node in nodes:
        short_name = node.split('|')[-1]
        key, suffix = _match_prefix(short_name, mapping)
        if key is None:
            continue
        new_name = mapping[key] + suffix
        if new_name == short_name:
            continue

        # Maya auto-renames locator shapes with the transform; keep their names.
        locators = [
            s.split('|')[-1]
            for s in (cmds.listRelatives(node, shapes=True, fullPath=True) or [])
            if cmds.nodeType(s) == 'locator'
        ]

        # renamed controllers lose the _Ctrl ending, tag them so save/load ctrls still finds them
        if short_name.endswith(CtrlUtils.nc['ctrl']):
            CtrlUtils.tag_controller(node)

        try:
            result = cmds.rename(node, new_name)
        except Exception as e:
            print('Skipped renaming {}: {}'.format(short_name, e))
            continue

        if result.split('|')[-1] != new_name:
            cmds.warning('{} wanted {} but got {} (name collision?)'.format(
                short_name, new_name, result.split('|')[-1]))
        print('Renamed: {} -> {}'.format(short_name, result))
        renamed += 1

        if locators:
            new_shapes = [
                s for s in (cmds.listRelatives(result, shapes=True, fullPath=True) or [])
                if cmds.nodeType(s) == 'locator'
            ]
            for shape, loc_name in zip(new_shapes, locators):
                if shape.split('|')[-1] != loc_name:
                    cmds.rename(shape, loc_name)

    print('Name Replacer: {} objects renamed.'.format(renamed))
    return renamed

#---------------------------------------------

def create_sn_renamer_block(name = 'SN_Renamer'):

    nc, curve_data, setup = mt.import_configs()
    #name checks and block creation
    name = mt.ask_name(text = MODULE['Name'])
    if cmds.objExists('{}{}'.format(name,nc['module'])):
        cmds.warning('Name already exists.')
        return ''

    block = mt.create_block(name = name, icon = 'Rename',  attrs = MODULE['attrs'], build_command = MODULE['build_command'], import_command = MODULE['import'])
    config = block[1]
    block = block[0]

    cmds.select(block)

    print('{} Created Successfully'.format(name))

#create_sn_renamer_block()

#-------------------------

def build_sn_renamer_block(force=False):

    block = cmds.ls(sl=True)
    if not block:
        cmds.warning("Please select the SN_Renamer block to build.")
        return

    conns = cmds.listConnections(block, type='network') or []
    config = conns[0] if conns else None
    block = block[0]

    # Same contract as the Code block: when a phase toggle is on, the builder
    # skips this pass and calls back with force=True in that phase.
    # RunBeforeLoadCtrls = after skins load, before controllers load.
    # RunAfterBuild      = very last step of the build.
    for phase in ('RunBeforeLoadCtrls', 'RunAfterBuild'):
        if config and cmds.attributeQuery(phase, n=config, exists=True):
            if cmds.getAttr('{}.{}'.format(config, phase)) and not force:
                print('SN_Renamer block {} deferred ({})'.format(block, phase))
                return

    rename_nodes()

    print ('Build {} Success'.format(block))

#build_sn_renamer_block()
