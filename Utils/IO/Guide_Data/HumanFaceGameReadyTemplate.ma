//Maya ASCII 2026 scene
//Name: HumanFaceGameReadyTemplate.ma
//Last modified: Thu, Feb 26, 2026 08:49:39 AM
//Codeset: 1252
requires maya "2026";
requires "stereoCamera" "10.0";
requires "mtoa" "5.5.3";
currentUnit -l centimeter -a degree -t film;
fileInfo "application" "maya";
fileInfo "product" "Maya 2026";
fileInfo "version" "2026";
fileInfo "cutIdentifier" "202507081222-4d6919b75c";
fileInfo "osv" "Windows 11 Home v2009 (Build: 26200)";
fileInfo "UUID" "259FAED4-4597-6717-C4DF-B5B3DBE81A0B";
createNode transform -n "Mutant_Build";
	rename -uid "83A4430F-436B-5CCB-FCAE-248BAC006870";
createNode transform -n "Face" -p "Mutant_Build";
	rename -uid "DBFC8AFE-4709-3A43-147B-C3B3E543A48F";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2026/scripts/Mutant_Tools/Icons/";
createNode dagContainer -n "VisAttrs_Block" -p "Face";
	rename -uid "3E47CD13-4763-E495-B41A-2C8A7475F1ED";
	addAttr -ci true -sn "nts" -ln "notes" -dt "string";
	setAttr ".isc" yes;
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2026/scripts/Mutant_Tools/Icons/VisAttrs.png";
	setAttr ".ctor" -type "string" "rodri";
	setAttr ".cdat" -type "string" "2025/12/06 12:36:32";
	setAttr -l on -k off ".v";
	setAttr -l on -k off ".tx";
	setAttr -l on -k off ".ty";
	setAttr -l on -k off ".tz";
	setAttr -l on -k off ".rx";
	setAttr -l on -k off ".ry";
	setAttr -l on -k off ".rz";
	setAttr -l on -k off ".sx";
	setAttr -l on -k off ".sy";
	setAttr -l on -k off ".sz";
	setAttr ".nts" -type "string" "['VisAttrs_Ctrl_Offset_Grp', 'VisAttrs_CtrlShape', 'VisAttrs_Ctrl_tag', 'VisAttrs_Ctrl']";
createNode transform -n "VisAttrs_Guide" -p "VisAttrs_Block";
	rename -uid "E3A0D3D8-4F37-25FC-EC83-EF83B9E0BB6D";
	addAttr -ci true -sn "RotateOrder" -ln "RotateOrder" -min 0 -max 5 -en "xyz:yzx:zxy:xzy:yxz:zyx" 
		-at "enum";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2026/scripts/Mutant_Tools/Icons/";
	setAttr -l on -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 18;
	setAttr ".t" -type "double3" 0 208.34561652549189 0 ;
	setAttr -k on ".RotateOrder";
createNode nurbsCurve -n "VisAttrs_GuideShape" -p "VisAttrs_Guide";
	rename -uid "388BAC3A-45EF-8D6A-8A4E-B1A56E721519";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2026/scripts/Mutant_Tools/Icons/";
	setAttr -k off ".v";
	setAttr ".hpb" yes;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 16 0 no 3
		17 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16
		17
		1 -1 0
		0 1 0
		0.5 -1 -0.86602500000000004
		1 -1 0
		0.5 -1 0.86602500000000004
		0 1 0
		0.5 -1 0.86602500000000004
		-0.5 -1 0.86602500000000004
		0 1 0
		-0.5 -1 0.86602500000000004
		-1 -1 -1.4901199999999998e-07
		0 1 0
		-1 -1 -1.4901199999999998e-07
		-0.5 -1 -0.86602599999999996
		0 1 0
		-0.5 -1 -0.86602599999999996
		0.5 -1 -0.86602500000000004
		;
createNode dagContainer -n "L_Brow_Block" -p "Face";
	rename -uid "232B4320-4665-9CB8-D6B7-37B79FF3B3B1";
	addAttr -ci true -sn "nts" -ln "notes" -dt "string";
	setAttr ".isc" yes;
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2026/scripts/Mutant_Tools/Icons/Brows.png";
	setAttr ".ctor" -type "string" "rodri";
	setAttr ".cdat" -type "string" "2025/12/06 12:27:44";
	setAttr -l on -k off ".v";
	setAttr -l on -k off ".tx";
	setAttr -l on -k off ".ty";
	setAttr -l on -k off ".tz";
	setAttr -l on -k off ".rx";
	setAttr -l on -k off ".ry";
	setAttr -l on -k off ".rz";
	setAttr -l on -k off ".sx";
	setAttr -l on -k off ".sy";
	setAttr -l on -k off ".sz";
	setAttr ".nts" -type "string" (
		"['L_Brow_1_LocShape', 'L_Brow_Driver0_Main_Ctrl_Offset_Grp', 'L_Brow_Driver3_Sec_Ctrl_Root_Grp_PC', 'L_Brow_Driver4_Main_Ctrl', 'R_Brow_TweekJnts_Grp', 'R_Brow_Driver4_Main_Ctrl', 'R_Brow_Driver1_Sec_Ctrl_Root_Grp_PC', 'L_Brow_1_Bnd_scaleConstraint1', 'L_Brow_0_Bnd_parentConstraint1', 'R_Brow_3_Loc_Offset_Grp', 'R_Brow_Driver4_Main_Ctrl_Offset_Grp', 'L_Brow_Driver1_Sec_Ctrl_tag', 'R_Brow_0_Jnt_Offset_Grp', 'L_Brow_2_Bnd', 'skinCluster34GroupId', 'R_Brow_Driver4_Main_CtrlShape', 'R_Brow_NurbFollicleShape1050', 'R_Brow_2_Ctrl_Offset_Grp', 'L_Brow_3_Jnt_parentConstraint1', 'R_Brow_0_Ctrl_Offset_Grp', 'R_Brow_Driver1_Jnt_Root_Grp', 'skinCluster34Set', 'L_Brow_3_Bnd_scaleConstraint1', 'L_Brow_NurbFollicleShape3050', 'unitConversion415', 'L_Brow_1_Jnt', 'R_Brow_Fol_Grp', 'R_Brow_innerAutoRot_Blend30', 'R_Brow_2_Bnd', 'R_Brow_Rig_Grp_parentConstraint1', 'L_Brow_2_Jnt', 'L_Brow_1_Loc_Offset_Grp', 'R_Brow_Driver1_Sec_Ctrl', 'R_Brow_Ctrl_GrpMirror_Grp', 'R_Brow_NurbFollicle6950', 'L_Brow_Driver0_Main_CtrlShape', 'R_Brow_Driver2_Jnt_Auto_Grp', 'R_Brow_1_CtrlShape', 'R_Brow_3_Jnt_parentConstraint1', 'R_Brow_2_Jnt_Offset_Grp', 'L_Brow_Driver4_Jnt', 'L_Brow_4_LocShape', 'R_Brow_2_Jnt_parentConstraint1', 'L_Brow_Driver1_yesRot_Loc', 'R_Brow_Driver3_yesRot_Loc_aimConstraint1', 'R_Brow_0_Bnd', 'R_Brow_1_Ctrl_tag', 'R_Brow_Driver3_Jnt_Auto_Grp', 'skinCluster34', 'L_Brow_1_Ctrl_tag', 'R_Brow_Driver3_Sec_Ctrl_tag', 'R_Brow_Driver3_Sec_Ctrl_Root_Grp', 'L_Brow_Rig_Grp', 'L_Brow_Driver3_Sec_CtrlShape', 'L_Brow_Driver0_Jnt', 'R_Brow_Driver4_Main_Ctrl_tag', 'unitConversion417', 'R_Brow_Driver3_Jnt', 'R_Brow_CtrlShape', 'L_Brow_Ctrl_Grp', 'R_Brow_4_LocShape', 'R_Brow_2_Ctrl_tag', 'R_Brow_Driver2_Main_CtrlShape', 'R_Brow_1_Jnt_Offset_Grp', 'R_Brow_Driver4_Jnt_Root_Grp', 'unitConversion412', 'L_Brow_2_CtrlShape', 'L_Brow_4_Jnt_Offset_Grp', 'L_Brow_Driver4_Jnt_Auto_Grp', 'R_Brow_0_Bnd_parentConstraint1', 'L_Brow_Driver1_yesRot_Loc_aimConstraint1', 'R_Brow_Main_Jnt_Grp', 'L_Brow_UpVector_LocShape', 'L_Brow_NurbFollicleShape5050', 'L_Brow_DriverJnts_Grp', 'L_Brow_Driver3_Sec_Ctrl_Root_Grp', 'L_Brow_NurbFollicle3050', 'R_Brow_1_Jnt_parentConstraint1', 'L_Brow_Driver4_Main_Ctrl_Offset_Grp', 'L_Brow_Driver3_noRot_Loc_Offset_Grp', 'R_Brow_3_Ctrl_tag', 'R_Brow_Driver2_Jnt', 'R_Brow_2_Bnd_scaleConstraint1', 'R_Brow_1_Ctrl_Offset_Grp', 'R_Brow_Driver4_Jnt_Auto_Grp', 'R_Brow_OutterAutoRot_Blend30', 'R_Brow_NurbFollicle1050', 'L_Brow_UpVector_Loc_parentConstraint1', 'L_Brow_2_LocShape', 'L_Brow_1_Jnt_parentConstraint1', 'L_Brow_1_Jnt_Offset_Grp', 'L_Brow_1_Bnd_parentConstraint1', 'L_Brow_NurbFollicleShape6950', 'L_Brow_Driver2_Main_Ctrl', 'R_Brow_NurbFollicleShape8950', 'R_Brow_NurbFollicle5050', 'L_Brow_TweekJnts_Grp', 'R_Brow_Nurb', 'R_Brow_Driver3_noRot_LocShape', 'R_Brow_4_Bnd_scaleConstraint1', 'R_Brow_4_Ctrl_tag', 'R_Brow_Ctrl_Grp', 'R_Brow_Driver3_yesRot_Loc_yesRot_PC', 'R_Brow_DriverJnts_Grp', 'unitConversion416', 'L_Brow_4_Ctrl_tag', 'L_Brow_Fol_Grp', 'L_Brow_NurbFollicle8950', 'L_Brow_Driver3_Jnt', 'R_Brow_0_CtrlShape', 'R_Brow_Driver1_Sec_Ctrl_Auto_Grp', 'L_Brow_0_Ctrl_tag', 'R_Brow_2_Loc_Offset_Grp', 'L_Brow_Driver3_Jnt_Root_Grp_PC', 'R_Brow_Driver1_yesRot_Loc_aimConstraint1', 'L_Brow_4_Bnd_scaleConstraint1', 'L_Brow_0_Jnt', 'R_Brow_3_Loc', 'L_Brow_3_Loc_Offset_Grp', 'R_Brow_0_Jnt', 'R_Brow_NurbFollicle3050', 'R_Brow_Driver1_Sec_Ctrl_Root_Grp', 'R_Brow_Driver3_Sec_CtrlShape', 'L_Brow_Driver2_Jnt', 'R_Brow_Driver1_yesRot_LocShape', 'L_Brow_NurbFollicle5050', 'L_Brow_2_Loc', 'R_Brow_Rig_GrpMirror_Grp', 'R_Brow_2_Ctrl', 'L_Brow_0_Jnt_parentConstraint1', 'R_Brow_3_CtrlShape', 'R_Brow_Driver1_Jnt_Auto_Grp', 'R_Brow_Driver2_Main_Ctrl_Offset_Grp', 'R_Brow_Tweeks_Ctrl_Grp', 'skinCluster33GroupId', 'L_Brow_Driver1_noRot_Loc_Offset_Grp', 'unitConversion422', 'L_Brow_Ctrl', 'L_Brow_Main_Ctrl_Grp', 'L_Brow_3_Ctrl_tag', 'L_Brow_Driver1_Sec_Ctrl', 'R_Brow_0_Bnd_scaleConstraint1', 'L_Brow_NurbFollicle6950', 'L_Brow_Driver1_noRot_Loc', 'L_Brow_Driver1_Sec_CtrlShape', 'L_Brow_3_Ctrl_Offset_Grp', 'R_Brow_1_LocShape', 'L_Brow_4_Loc_Offset_Grp', 'R_Brow_Driver1_noRot_Loc_Offset_Grp', 'L_Brow_2_Bnd_scaleConstraint1', 'L_Brow_3_Jnt_Offset_Grp', 'R_Brow_0_Ctrl', 'L_Brow_Driver4_Main_CtrlShape', 'skinCluster33GroupParts', 'R_Brow_3_Jnt_Offset_Grp', 'R_Brow_NurbFollicle8950', 'R_Brow_NurbShape', 'L_Brow_Ctrl_tag', 'R_Brow_Driver3_Sec_Ctrl_Root_Grp_PC', 'R_Brow_4_Loc_Offset_Grp', 'R_Brow_2_CtrlShape', 'R_Brow_Driver0_Main_Ctrl_tag', 'R_Brow_Driver1_noRot_Loc_noRot_PC', 'unitConversion410', 'L_Brow_UpVector_Loc', 'R_Brow_4_Jnt_Offset_Grp', 'skinCluster34GroupParts', 'L_Brow_3_LocShape', 'unitConversion421', 'R_Brow_1_Loc', 'L_Brow_Main_Jnt_Grp', 'L_Brow_3_Bnd', 'R_Brow_Rig_Grp_scaleConstraint1', 'L_Brow_Nurb', 'L_Brow_4_Ctrl', 'L_Brow_Driver0_Jnt_Auto_Grp', 'R_Brow_Driver0_Main_Ctrl', 'R_Brow_UpVector_Loc_parentConstraint1', 'bindPose28', 'L_Brow_Driver3_noRot_LocShape', 'L_Brow_4_CtrlShape', 'R_Brow_Ctrl_Grp_parentConstraint1', 'L_Brow_2_Ctrl', 'L_Brow_0_Ctrl', 'L_Brow_Ctrl_Grp_parentConstraint1', 'L_Brow_Driver2_Jnt_Root_Grp', 'R_Brow_4_Loc', 'L_Brow_0_Loc_Offset_Grp', 'L_Brow_OutterAutoRot_Blend30', 'L_Brow_Driver1_Jnt', 'R_Brow_Driver1_yesRot_Loc_Offset_Grp', 'L_Brow_4_Bnd_parentConstraint1', 'unitConversion414', 'skinCluster33Set', 'R_Brow_2_LocShape', 'R_Brow_Driver3_noRot_Loc_Offset_Grp', 'R_Brow_1_Loc_Offset_Grp', 'unitConversion418', 'L_Brow_1_Ctrl_Offset_Grp', 'R_Brow_3_Ctrl', 'L_Brow_NurbFollicleShape1050', 'L_Brow_3_CtrlShape', 'L_Brow_1_CtrlShape', 'unitConversion420', 'R_Brow_1_Bnd_scaleConstraint1', 'L_Brow_2_Ctrl_tag', 'R_Brow_0_Loc', 'L_Brow_Driver4_Main_Ctrl_tag', 'L_Brow_4_Loc', 'L_Brow_Driver1_Jnt_Root_Grp', 'R_Brow_Driver1_yesRot_Loc', 'L_Brow_1_Ctrl', 'R_Brow_0_LocShape', 'L_Brow_Driver1_noRot_Loc_noRot_PC', 'L_Brow_Ctrl_Grp_scaleConstraint1', 'R_Brow_Driver1_Sec_Ctrl_tag', 'L_Brow_0_Bnd', 'L_Brow_2_Ctrl_Offset_Grp', 'R_Brow_Ctrl_tag', 'R_Brow_2_Loc', 'L_Brow_Driver3_Jnt_Auto_Grp', 'L_Brow_Driver3_yesRot_Loc', 'unitConversion423', 'L_Brow_0_Bnd_scaleConstraint1', 'L_Brow_3_Bnd_parentConstraint1', 'L_Brow_NurbFollicle1050', 'R_Brow_3_Bnd_parentConstraint1', 'R_Brow_Driver2_Main_Ctrl_tag', 'L_Brow_CtrlShape', 'L_Brow_4_Jnt', 'skinCluster33', 'L_Brow_Rig_Grp_parentConstraint1', 'L_Brow_Driver1_Jnt_Root_Grp_PC', 'L_Brow_Driver1_Sec_Ctrl_Root_Grp', 'R_Brow_Driver1_noRot_Loc', 'R_Brow_2_Bnd_parentConstraint1', 'R_Brow_4_Ctrl', 'R_Brow_3_LocShape', 'L_Brow_Driver1_Jnt_Auto_Grp', 'R_Brow_Driver1_noRot_LocShape', 'R_Brow_Driver0_Main_CtrlShape', 'R_Brow_NurbShapeOrig', 'L_Brow_1_Bnd', 'L_Brow_0_Ctrl_Offset_Grp', 'R_Brow_Driver3_noRot_Loc_noRot_PC', 'R_Brow_NurbFollicleShape3050', 'L_Brow_Driver1_Sec_Ctrl_Auto_Grp', 'L_Brow_Driver3_noRot_Loc', 'R_Brow_2_Jnt', 'R_Brow_4_Ctrl_Offset_Grp', 'R_Brow_Driver3_yesRot_Loc', 'R_Brow_NurbFollicleShape5050', 'L_Brow_Driver2_Main_Ctrl_tag', 'L_Brow_NurbShapeOrig', 'L_Brow_3_Loc', 'R_Brow_Ctrl_Offset_Grp', 'L_Brow_Driver1_noRot_LocShape', 'R_Brow_4_CtrlShape', 'L_Brow_3_Ctrl', 'L_Brow_Driver2_Jnt_Auto_Grp', 'L_Brow_Driver1_Sec_Ctrl_Root_Grp_PC', 'L_Brow_1_Loc', 'R_Brow_Driver0_Jnt_Root_Grp', 'L_Brow_4_Bnd', 'R_Brow_1_Jnt', 'R_Brow_1_Bnd', 'R_Brow_4_Jnt', 'R_Brow_Driver3_noRot_Loc', 'L_Brow_4_Jnt_parentConstraint1', 'L_Brow_Driver0_Main_Ctrl_tag', 'R_Brow_3_Ctrl_Offset_Grp', 'L_Brow_Driver4_Jnt_Root_Grp', 'R_Brow_Driver3_Jnt_Root_Grp', 'L_Brow_innerAutoRot_Blend30', 'L_Brow_2_Jnt_Offset_Grp', 'L_Brow_Driver1_yesRot_Loc_yesRot_PC', 'L_Brow_Driver1_yesRot_Loc_Offset_Grp', 'R_Brow_Rig_Grp', 'L_Brow_NurbShape', 'L_Brow_4_Ctrl_Offset_Grp', 'R_Brow_Driver2_Main_Ctrl', 'L_Brow_0_Loc', 'unitConversion419', 'R_Brow_Driver0_Jnt_Auto_Grp', 'L_Brow_Tweeks_Ctrl_Grp', 'L_Brow_NurbFollicleShape8950', 'R_Brow_1_Bnd_parentConstraint1', 'R_Brow_Driver2_Jnt_Root_Grp', 'L_Brow_0_Jnt_Offset_Grp', 'L_Brow_2_Bnd_parentConstraint1', 'L_Brow_Driver3_Sec_Ctrl_tag', 'L_Brow_Driver3_yesRot_Loc_aimConstraint1', 'R_Brow_SecRot_Loc_Grp', 'unitConversion409', 'L_Brow_Driver3_yesRot_LocShape', 'L_Brow_2_Jnt_parentConstraint1', 'R_Brow_Driver3_Sec_Ctrl_Auto_Grp', 'R_Brow_Driver3_yesRot_LocShape', 'R_Brow_UpVector_LocShape', 'L_Brow_Driver3_Sec_Ctrl', 'L_Brow_Rig_Grp_scaleConstraint1', 'R_Brow_3_Bnd', 'L_Brow_Driver2_Main_Ctrl_Offset_Grp', 'R_Brow_0_Loc_Offset_Grp', 'R_Brow_1_Ctrl', 'R_Brow_Driver3_yesRot_Loc_Offset_Grp', 'L_Brow_0_CtrlShape', 'R_Brow_Driver1_yesRot_Loc_yesRot_PC', 'R_Brow_Driver3_Jnt_Root_Grp_PC', 'R_Brow_Driver1_Sec_CtrlShape', 'R_Brow_4_Bnd', 'L_Brow_Driver3_Sec_Ctrl_Auto_Grp', 'R_Brow_4_Jnt_parentConstraint1', 'L_Brow_0_LocShape', 'L_Brow_Driver3_noRot_Loc_noRot_PC', 'L_Brow_Ctrl_Offset_Grp', 'R_Brow_Ctrl_Grp_scaleConstraint1', 'R_Brow_0_Ctrl_tag', 'R_Brow_UpVector_Loc', 'L_Brow_Driver2_Main_CtrlShape', 'L_Brow_Driver3_yesRot_Loc_yesRot_PC', 'L_Brow_Driver3_yesRot_Loc_Offset_Grp', 'L_Brow_Driver1_yesRot_LocShape', 'L_Brow_3_Jnt', 'R_Brow_Driver3_Sec_Ctrl', 'L_Brow_2_Loc_Offset_Grp', 'R_Brow_Driver0_Jnt', 'R_Brow_3_Bnd_scaleConstraint1', 'R_Brow_3_Jnt', 'unitConversion411', 'unitConversion424', 'R_Brow_Main_Ctrl_Grp', 'R_Brow_4_Bnd_parentConstraint1', 'L_Brow_SecRot_Loc_Grp', 'L_Brow_Driver3_Jnt_Root_Grp', 'R_Brow_Driver1_Jnt', 'R_Brow_Driver0_Main_Ctrl_Offset_Grp', 'L_Brow_Driver0_Jnt_Root_Grp', 'R_Brow_Ctrl', 'L_Brow_Driver0_Main_Ctrl', 'R_Brow_Driver4_Jnt', 'R_Brow_0_Jnt_parentConstraint1', 'R_Brow_Driver1_Jnt_Root_Grp_PC', 'unitConversion413', 'bindPose27', 'R_Brow_NurbFollicleShape6950']");
createNode transform -n "L_Brow_Guide" -p "L_Brow_Block";
	rename -uid "C6E768B9-4A72-277A-2DBA-B78F2E4467DA";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2026/scripts/Mutant_Tools/Icons/";
	setAttr ".t" -type "double3" 3.615156424726103 184.2846273815513 17.808829317045852 ;
createNode nurbsSurface -n "L_Brow_GuideShape" -p "L_Brow_Guide";
	rename -uid "EB9CFE24-4F2B-6718-0C9B-1798CCB6B57C";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2026/scripts/Mutant_Tools/Icons/";
	setAttr -k off ".v";
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr ".dvu" 0;
	setAttr ".dvv" 0;
	setAttr ".cpr" 4;
	setAttr ".cps" 4;
	setAttr ".cc" -type "nurbsSurface" 
		3 3 0 0 no 
		10 0 0 0 0.20000000000000001 0.40000000000000002 0.60000000000000009 0.80000000000000004
		 1 1 1
		6 0 0 0 1 1 1
		
		32
		-1.3443723550494535 -0.54325528233915188 -0.51071472108208027
		-1.3443723550494535 0.011615258519344751 -0.51071472108208027
		-1.3443723550494535 0.56648579937784094 -0.51071472108208027
		-1.3443723550494535 1.1213563402363378 -0.51071472108208027
		-0.78950181419095156 -0.54325528233915188 -0.51071472108208027
		-0.78950181419095156 0.011615258519344751 -0.51071472108208027
		-0.78950181419095156 0.56648579937784094 -0.51071472108208027
		-0.78950181419095156 1.1213563402363378 -0.51071472108208027
		0.3384764377404495 -0.54325528233915188 -0.51683402931194722
		0.3384764377404495 0.011615258519344751 -0.51683402931194722
		0.3384764377404495 0.56648579937784094 -0.51683402931194722
		0.3384764377404495 1.1213563402363378 -0.51683402931194722
		2.314412732344747 -0.52584250192693427 -0.8586338593522358
		2.31919135391438 0.029007095156079344 -0.8592714370431187
		2.3239699754840135 0.58385669223909298 -0.85990901473400161
		2.328748597053647 1.1387062893221072 -0.86054659242488452
		4.3071474980554347 -0.55050251488271784 -1.8857185367925662
		4.3446470952913439 0.0030752648583776687 -1.8908895228362832
		4.3821466925272547 0.55665304459947262 -1.8960605088799998
		4.4196462897631648 1.1102308243405681 -1.9012314949237168
		5.8656569468506374 -0.77384698459481338 -3.2396618514029205
		5.9334434698907899 -0.22321652697384076 -3.2492745277652073
		6.0012299929309414 0.32741393064713131 -3.2588872041274937
		6.0690165159710929 0.8780443882681036 -3.2684998804897805
		6.576480723541871 -0.90362954333554024 -4.1100894516369877
		6.6495263664344622 -0.35368649564660204 -4.1204959623687758
		6.7225720093270525 0.19625655204233572 -4.130902473100563
		6.7956176522196436 0.74619959973127425 -4.1413089838323511
		6.8282386577839258 -0.94469552051255734 -4.513118727551757
		6.901284300676517 -0.39475247282361908 -4.5235252382835442
		6.9743299435691073 0.15519057486531873 -4.5339317490153324
		7.0473755864616985 0.70513362255425749 -4.5443382597471196
		
		;
	setAttr ".nufa" 4.5;
	setAttr ".nvfa" 4.5;
createNode dagContainer -n "L_Eyelids_Block" -p "Face";
	rename -uid "1F9E5CE0-4648-DAF1-3318-91BE28AC42E7";
	addAttr -ci true -sn "nts" -ln "notes" -dt "string";
	setAttr ".isc" yes;
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2026/scripts/Mutant_Tools/Icons/Eyes.png";
	setAttr ".ctor" -type "string" "rodri";
	setAttr ".cdat" -type "string" "2025/12/06 12:35:13";
	setAttr -l on -k off ".v";
	setAttr -l on -k off ".tx";
	setAttr -l on -k off ".ty";
	setAttr -l on -k off ".tz";
	setAttr -l on -k off ".rx";
	setAttr -l on -k off ".ry";
	setAttr -l on -k off ".rz";
	setAttr -l on -k off ".sx";
	setAttr -l on -k off ".sy";
	setAttr -l on -k off ".sz";
	setAttr ".nts" -type "string" (
		"['R_Eyelids_Dw_Origin_10_Jnt', 'L_Eyelids_Dw_VtxJnts_Grp', 'R_Eyelids_Ctrl_Grp_parentConstraint1', 'L_Eyelids_Blink_CrvBaseWire1Shape', 'R_Eyelids_Up_11_Ctrl_tag', 'L_Eyelids_Dw_7_Ctrl', 'L_Eyelids_Up_2_LocShape', 'L_EyelidsUprBlink_Ctrl_tag', 'L_Eyelids_LwrBlink_BSGroupParts', 'R_Eyelids_DwMid_Jnt', 'R_Eyelids_UpEnd_CtrlShape', 'R_Eyelids_UpEndMid_Ctrl_Offset_Grp_parentConstraint1', 'R_Eyelids_UpStart_Ctrl', 'L_Eyelids_Dw_BlinkTarget_CrvShapeOrig1', 'R_Eyelids_Dw_WireDriver_CrvBaseWireShape', 'L_Eyelids_Up__cv2_Bnd_parentConstraint1', 'skinCluster36Set', 'R_Eyelids_Dw_8_Jnt_Offset_Grp', 'skinCluster38GroupParts', 'L_Eyelids_DwStart_Ctrl', 'R_Eyelids_Up_VtxJnts_Grp', 'R_Eyelids_Dw_0_LocShape', 'R_Eyelids_Up__cv4_Bnd_scaleConstraint1', 'R_Eyelids_DwWireGroupParts', 'R_Eyelids_Up_Wire', 'R_Eyelids_Up_0_Loc', 'R_Eyelids_Up_1_Ctrl_OffsetPivot_Grp', 'L_Eyelids_Dw_Origin_0_Jnt', 'L_Eyelids_Dw_Origin_9_Jnt_Offset_Grp', 'R_Eyelids_Dw_8_POCI', 'L_EyelidsLwrBlink_Ctrl', 'R_Eyelids_Up__cv2_Bnd_parentConstraint1', 'L_Eyelids_BlinkAttrs_Ctrl_tag', 'L_Eyelids_Up_6_Ctrl_OffsetPivot_Grp', 'L_Eyelids_Dw_10_Ctrl_tag', 'L_Eyelids_Dw_Origin_3_Jnt_aimConstraint1', 'L_Eyelids_Up_AimLocators_Grp', 'L_Eyelids_Dw_1_Loc', 'L_Eyelids_Dw_8_Jnt_Offset_Grp', 'R_Eyelids_Dw_Origin_1_Jnt_aimConstraint1', 'L_Eyelids_Dw_5_Loc', 'L_Eyelids_DwStartMid_Ctrl_tag', 'R_Eyelids_Dw_Origin_4_Jnt', 'L_Eyelids_Dw_9_Ctrl_Offset_Grp', 'R_Eyelids_Scale_Ctrl_Offset_Grp', 'R_Eyelids_Dw_4_LocShape', 'R_Eyelids_Up_Origin_10_Jnt_aimConstraint1', 'L_Eyelids_Dw_WireDriver_CrvBaseWireShapeOrig', 'L_Eyelids_Up_Vtx_CrvShape', 'L_Eyelids_Up_WireDriver_CrvShapeOrig1', 'R_Eyelids_Dw_5_Ctrl_tag', 'R_Eyelids_Dw_10_Ctrl', 'R_Eyelids_Dw_3_Jnt', 'L_Eyelids_Up_2_Ctrl', 'R_Eyelids_LwrBlink_BS', 'R_Eyelids_Up_Scale_Ctrl_Offset_Grp', 'R_Eyelids_Dw_7_Loc', 'R_Eyelids_LwrBlink_BSGroupId', 'L_Eyelids_Dw_Scale_Ctrl_Offset_Grp', 'L_Eyelids_UprBlink_BS', 'L_Eyelids_Up_Scale_CtrlShape', 'L_Eyelids_UprBlink_BSGroupParts', 'R_Eyelids_Up_7_Ctrl', 'L_Eyelids_UpEnd_Ctrl', 'R_Eyelids_Up_9_Jnt', 'L_Eyelids_Up_3_POCI', 'R_Eyelids_UpStart_CtrlShape', 'R_Eyelids_Up_BlinkTarget_CrvShapeOrig', 'L_Eyelids_Up_6_POCI', 'L_Eyelids_Dw_Origin_10_Jnt_aimConstraint1', 'R_Eyelids_Dw_4_Ctrl_tag', 'L_Eyelids_Up_8_Ctrl_OffsetPivot_Grp', 'L_Eyelids_LwrBlink_BSSet', 'R_Eyelids_Up_9_POCI', 'R_Eyelids_Rig_GrpMirror_Grp', 'L_Eyelids_Dw_WireSet', 'R_Eyelids_Up_4_Ctrl_OffsetPivot_Grp', 'R_Eyelids_UpStartMid_CtrlShape', 'L_Eyelids_Dw_3_Jnt_Offset_Grp', 'R_Eyelids_Up_Origin_0_Jnt', 'L_Eyelids_Dw_3_Loc', 'R_Eyelids_Up_8_Ctrl', 'L_Eyelids_Blink_CrvBaseWireShapeOrig1', 'L_Eyelids_Up_Origin_8_Jnt_Offset_Grp', 'L_Eyelids_Dw__cv2_Bnd_scaleConstraint1', 'L_Eyelids_Up_9_Ctrl_OffsetPivot_Grp', 'R_Eyelids_Up_1_CtrlShape', 'L_Eyelids_UpStart_Ctrl_Offset_Grp', 'L_Eyelids_Up_7_Ctrl_tag', 'L_Eyelids_Up_Origin_9_Jnt', 'R_Eyelids_Up_2_Jnt', 'R_Eyelids_Dw_6_Jnt', 'L_Eyelids_Dw_0_Jnt', 'R_Eyelids_Dw_3_Ctrl_OffsetPivot_Grp_Offset_Grp', 'L_Eyelids_Up_Origin_7_Jnt_Offset_Grp', 'L_Eyelids_Up__cv3_Bnd', 'L_Eyelids_Dw_AimLocators_Grp', 'L_Eyelids_DwEnd_Ctrl', 'L_Eyelids_Dw_1_Jnt_Offset_Grp', 'R_Eyelids_Up_Origin_9_Jnt', 'L_Eyelids_Dw_Origin_5_Jnt_aimConstraint1', 'R_Eyelids_Dw_2_CtrlShape', 'R_Eyelids_UpEndMid_Ctrl', 'L_Eyelids_Up__cv2_Bnd', 'R_Eyelids_Dw_10_POCI', 'R_Eyelids_UpStartMid_Jnt_Offset_Grp_parentConstraint1', 'unitConversion432', 'L_Eyelids_Up_6_Jnt_Offset_Grp', 'L_Eyelids_Up_Origin_7_Jnt', 'R_Eyelids_Up_1_Ctrl', 'R_Eyelids_Up_3_CtrlShape', 'R_Eyelids_Dw_7_Jnt', 'L_Eyelids_Dw_4_Jnt_Offset_Grp', 'R_Eyelids_DwStart_Ctrl_tag', 'L_Eyelids_Up_2_Ctrl_OffsetPivot_Grp_Offset_Grp', 'L_Eyelids_Up_Origin_5_Jnt_aimConstraint1', 'L_Eyelids_Dw_Scale_Ctrl', 'L_Eyelids_Dw_6_Ctrl_OffsetPivot_Grp', 'R_Eyelids_Blink_BSGroupParts', 'L_Eyelids_DwStart_Ctrl_Offset_Grp', 'R_Eyelids_Up_9_LocShape', 'L_Eyelids_Dw_2_Ctrl_Offset_Grp', 'L_Eyelids_Up_2_POCI', 'L_Eyelids_Up_0_Ctrl_tag', 'skinCluster38Set', 'R_Eyelids_Dw_4_Loc', 'L_Eyelids_Up_Origin_11_Jnt', 'L_Eyelids_Dw_11_Ctrl_tag', 'L_Eyelids_DwStart_Ctrl_tag', 'R_Eyelids_Up_Origin_2_Jnt_aimConstraint1', 'L_Eyelids_Up_WireDriver_Crv', 'R_Eyelids_DwEnd_Jnt', 'R_EyelidsUprBlink_Ctrl_Offset_Grp', 'L_Eyelids_Up_Scale_Grp', 'L_Eyelids_Ctrl_Grp_scaleConstraint1', 'skinCluster35GroupId', 'R_Eyelids_Up_Origin_4_Jnt_Offset_Grp', 'R_Eyelids_Up_Origin_6_Jnt_Offset_Grp', 'L_Eyelids_Dw_1_Jnt', 'R_Eyelids_Up_1_Loc', 'L_Eyelids_EyePivot_Loc', 'R_Eyelids_Dw_1_Jnt', 'L_Eyelids_Dw_0_Ctrl', 'L_Eyelids_Up_Origin_0_Jnt', 'R_Eyelids_Dw_5_POCI', 'L_Eyelids_DwEndMid_Jnt', 'R_Eyelids_Up__cv3_Bnd', 'R_Eyelids_Dw_Origin_3_Jnt_aimConstraint1', 'R_Eyelids_Up_Origin_7_Jnt', 'L_Eyelids_Up_10_Ctrl_OffsetPivot_Grp_Offset_Grp', 'R_Eyelids_UpStart_Ctrl_Offset_Grp', 'R_Eyelids_Up_8_Ctrl_OffsetPivot_Grp', 'L_Eyelids_Blink_CrvShape', 'R_Eyelids_Dw_11_CtrlShape', 'L_Eyelids_Up_9_Ctrl', 'R_Eyelids_Dw_Origin_4_Jnt_Offset_Grp', 'skinCluster37Set', 'L_Eyelids_Up_3_Ctrl_OffsetPivot_Grp_Offset_Grp', 'L_Eyelids_Blink_CrvBaseWireShapeOrig', 'L_Eyelids_Dw_1_POCI', 'R_Eyelids_BlinkAttrs_Ctrl_Offset_Grp', 'L_Eyelids_Up_7_Jnt_Offset_Grp', 'L_Eyelids_Up_8_LocShape', 'L_Eyelids_UpMid_Ctrl', 'L_Eyelids_Dw_Origin_11_Jnt', 'R_Eyelids_Up_3_Ctrl_Offset_Grp', 'R_Eyelids_Up_10_POCI', 'R_Eyelids_Dw_WireSet', 'L_Eyelids_DwStartMid_Ctrl_Offset_Grp_parentConstraint1', 'L_Eyelids_UpWireGroupParts', 'R_Eyelids_Up_4_CtrlShape', 'L_Eyelids_UpWireSet', 'R_Eyelids_DwEnd_Ctrl', 'R_Eyelids_Dw_Origin_1_Jnt_Offset_Grp', 'R_Eyelids_Up_3_LocShape', 'L_Eyelids_Ctrl_Grp_parentConstraint1', 'L_Eyelids_Dw__cv4_Bnd_parentConstraint1', 'L_Eyelids_Up_WireDriver_CrvShape', 'L_Eyelids_Up_8_CtrlShape', 'R_Eyelids_Up_4_Ctrl_OffsetPivot_Grp_Offset_Grp', 'R_Eyelids_Blink_Crv', 'L_Eyelids_Up_5_Ctrl_OffsetPivot_Grp_Offset_Grp', 'L_Eyelids_Up_1_Ctrl_OffsetPivot_Grp_Offset_Grp', 'R_Eyelids_Up_4_Jnt_Offset_Grp', 'R_Eyelids_Dw_Origin_8_Jnt_aimConstraint1', 'L_Eyelids_Dw_0_LocShape', 'R_Eyelids_Dw_2_Jnt_Offset_Grp', 'R_Eyelids_Up_5_Jnt', 'L_EyelidsUprBlink_Ctrl', 'L_Eyelids_Dw_9_Ctrl', 'L_Eyelids_DwMid_Jnt', 'L_Eyelids_Dw_7_Ctrl_tag', 'R_Eyelids_Dw__cv3_Bnd', 'R_Eyelids_Dw_11_Jnt', 'R_Eyelids_Up_8_POCI', 'R_Eyelids_Dw_Origin_6_Jnt', 'L_Eyelids_Up_WireGroupParts', 'L_Eyelids_Dw_2_Ctrl_tag', 'R_Eyelids_Up_10_Jnt', 'L_Eyelids_Dw_8_Jnt', 'L_Eyelids_Dw_Origin_8_Jnt_Offset_Grp', 'R_Eyelids_Up_6_Ctrl_Offset_Grp', 'L_Eyelids_DwWireGroupParts', 'R_Eyelids_EyePivot_Loc', 'R_Eyelids_Dw_7_CtrlShape', 'L_Eyelids_Blink_CrvBaseWireShape', 'R_Eyelids_Ctrl_Grp_scaleConstraint1', 'R_Eyelids_UpEndMid_Ctrl_Offset_Grp', 'R_Eyelids_DwEndMid_Ctrl', 'L_Eyelids_Dw_5_Jnt_Offset_Grp', 'L_Eyelids_Dw_10_Ctrl_Offset_Grp', 'R_Eyelids_Up_WireDriver_CrvShapeOrig', 'L_Eyelids_Up_8_Loc', 'L_Eyelids_Up_0_Ctrl_Offset_Grp', 'R_Eyelids_Up_8_Ctrl_OffsetPivot_Grp_Offset_Grp', 'L_Eyelids_Dw_WireDriver_CrvBaseWireShape', 'L_Eyelids_Dw_Origin_6_Jnt_aimConstraint1', 'R_Eyelids_DwEnd_CtrlShape', 'L_Eyelids_Dw_1_Ctrl', 'R_Eyelids_Dw_10_Ctrl_OffsetPivot_Grp_Offset_Grp', 'L_Eyelids_Dw_6_Ctrl_OffsetPivot_Grp_Offset_Grp', 'R_Eyelids_Dw_WireDriver_CrvShapeOrig', 'R_Eyelids_Dw_5_LocShape', 'R_Eyelids_Dw_1_POCI', 'R_Eyelids_Dw__cv3_Bnd_scaleConstraint1', 'R_Eyelids_Up_Scale_Grp_Offset_Grp', 'L_Eyelids_DwEnd_Ctrl_tag', 'L_Eyelids_Dw_4_CtrlShape', 'R_Eyelids_Dw_6_Ctrl', 'L_Eyelids_Dw_Origin_1_Jnt', 'R_Eyelids_Up_Origin_11_Jnt_Offset_Grp', 'R_Eyelids_Dw_9_CtrlShape', 'R_Eyelids_Dw_6_POCI', 'R_Eyelids_Up_5_Ctrl_OffsetPivot_Grp_Offset_Grp', 'LwrBlink_MultDiv3', 'L_Eyelids_UpStart_Jnt_Offset_Grp', 'R_Eyelids_Blink_CrvBaseWireShapeOrig2', 'L_Eyelids_DwStartMid_Ctrl_Offset_Grp', 'L_Eyelids_Up_0_CtrlShape', 'R_Eyelids_UpStartMid_Ctrl_Offset_Grp_parentConstraint1', 'L_Eyelids_Dw_0_Jnt_Offset_Grp', 'skinCluster38GroupId', 'R_Eyelids_Dw_8_Loc', 'R_Eyelids_Dw_Scale_Grp_Offset_Grp', 'L_Eyelids_Dw_5_CtrlShape', 'L_Eyelids_UpStartMid_Ctrl_Offset_Grp_parentConstraint1', 'L_Eyelids_Up_Origin_9_Jnt_aimConstraint1', 'L_Eyelids_Dw_3_CtrlShape', 'L_Eyelids_Up_1_Jnt', 'L_Eyelids_Blink_CrvBaseWire1', 'L_Eyelids_Up_Origin_5_Jnt', 'R_Eyelids_Dw_1_CtrlShape', 'R_Eyelids_Dw_10_Jnt', 'R_EyelidsLwrBlink_CtrlShape', 'unitConversion431', 'L_Eyelids_Up_4_Loc', 'R_Eyelids_Up_Origin_9_Jnt_Offset_Grp', 'R_Eyelids_Blink_CrvBaseWireShapeOrig1', 'L_Eyelids_Dw_Origin_5_Jnt', 'R_Eyelids_Up_6_Jnt_Offset_Grp', 'L_Eyelids_Dw_4_Ctrl_Offset_Grp', 'R_Eyelids_Up_11_CtrlShape', 'L_Eyelids_Up_10_Jnt_Offset_Grp', 'R_Eyelids_Dw_1_Loc', 'L_Eyelids_Dw_3_Ctrl_OffsetPivot_Grp_Offset_Grp', 'R_Eyelids_Up_Origin_9_Jnt_aimConstraint1', 'R_Eyelids_Blink_CrvBaseWire1', 'R_Eyelids_Dw_BlinkTarget_CrvShape', 'L_Eyelids_Dw_Jnt_Grp', 'R_Eyelids_Up_Origin_4_Jnt', 'R_Eyelids_DwWireGroupId', 'R_Eyelids_Up_10_Jnt_Offset_Grp', 'L_Eyelids_Up_10_CtrlShape', 'R_Eyelids_Up_8_Jnt', 'L_Eyelids_Up_8_POCI', 'L_Eyelids_DwEndMid_Jnt_Offset_Grp_parentConstraint1', 'L_Eyelids_Dw_6_Ctrl', 'L_Eyelids_Up__cv4_Bnd_scaleConstraint1', 'L_Eyelids_Up_1_Ctrl_OffsetPivot_Grp', 'L_Eyelids_UpEndMid_Ctrl_Offset_Grp', 'L_Eyelids_Dw__cv2_Bnd', 'R_Eyelids_UpStartMid_Ctrl_tag', 'L_Eyelids_UpEnd_Ctrl_Offset_Grp', 'R_Eyelids_Blink_CrvShapeOrig', 'L_Eyelids_Dw_Origin_4_Jnt_aimConstraint1', 'L_Eyelids_Dw_6_Ctrl_tag', 'skinCluster37GroupParts', 'L_Eyelids_UpStart_Jnt', 'L_Eyelids_Dw_Origin_0_Jnt_aimConstraint1', 'skinCluster36', 'R_Eyelids_Up_8_CtrlShape', 'R_Eyelids_UprBlink_BSGroupParts', 'L_Eyelids_Up_3_Jnt_Offset_Grp', 'R_Eyelids_DwMid_Ctrl_tag', 'L_Eyelids_Dw_3_LocShape', 'R_Eyelids_UpEndMid_Jnt', 'R_Eyelids_Dw_4_Ctrl_Offset_Grp', 'L_Eyelids_UpStart_Ctrl', 'L_Eyelids_UpWire', 'R_Eyelids_Dw__cv4_Bnd_scaleConstraint1', 'L_Eyelids_DwMid_Jnt_Offset_Grp', 'L_Eyelids_Up_6_Ctrl', 'R_Eyelids_Dw_Origin_9_Jnt', 'L_Eyelids_Dw_4_Ctrl_tag', 'R_Eyelids_UpMid_Ctrl_tag', 'R_Eyelids_Up_3_Loc', 'L_EyelidsUprBlink_Ctrl_Offset_Grp', 'L_Eyelids_Up_4_Ctrl_OffsetPivot_Grp', 'R_Eyelids_Up_Origin_5_Jnt_Offset_Grp', 'L_Eyelids_Scale_Ctrl', 'R_Eyelids_DwEnd_Ctrl_tag', 'L_Eyelids_Up_Wire', 'R_EyelidsLwrBlink_Ctrl', 'L_Eyelids_Up_2_Jnt_Offset_Grp', 'R_Eyelids_Dw_6_Loc', 'R_Eyelids_Up_Origin_5_Jnt_aimConstraint1', 'L_Eyelids_Dw_Origin_7_Jnt', 'R_Eyelids_UpStart_Jnt_Offset_Grp', 'R_Eyelids_DwEndMid_Jnt_Offset_Grp', 'R_Eyelids_Dw_9_Jnt', 'R_Eyelids_Dw_BlinkTarget_CrvShapeOrig', 'R_Eyelids_Scale_Jnt', 'R_Eyelids_Dw_10_Jnt_Offset_Grp', 'R_Eyelids_Up_1_Jnt', 'L_Eyelids_Dw_10_Loc', 'L_Eyelids_UpStartMid_Ctrl_Offset_Grp', 'R_EyelidsLwrBlink_Ctrl_tag', 'L_Eyelids_DwStartMid_CtrlShape', 'L_Eyelids_UpEnd_Jnt', 'R_Eyelids_Up_Origin_2_Jnt', 'L_Eyelids_Blink_CrvShapeOrig2', 'R_Eyelids_Dw_11_Ctrl_tag', 'L_Eyelids_Dw_1_Ctrl_OffsetPivot_Grp_Offset_Grp', 'L_Eyelids_Dw_7_Ctrl_Offset_Grp', 'L_Eyelids_Up_7_Ctrl', 'L_Eyelids_Dw_Origin_11_Jnt_aimConstraint1', 'R_Eyelids_UpMid_Ctrl', 'R_Eyelids_Dw_2_Ctrl_OffsetPivot_Grp', 'L_Eyelids_DwStartMid_Jnt', 'L_Eyelids_Up_Origin_1_Jnt', 'R_Eyelids_Blink_CrvBaseWireShapeOrig', 'R_Eyelids_Up_10_Ctrl_tag', 'L_Eyelids_Up_0_LocShape', 'L_Eyelids_Blink_BS', 'L_Eyelids_UpVector_Loc', 'R_Eyelids_UpMid_Ctrl_Offset_Grp', 'R_Eyelids_UpStartMid_Jnt_Offset_Grp', 'L_Eyelids_Blink_Reverse', 'R_Eyelids_Blink_CrvBaseWire', 'R_Eyelids_Up_9_Jnt_Offset_Grp', 'R_Eyelids_Up_0_Ctrl_OffsetPivot_Grp', 'L_Eyelids_UpStartMid_Jnt', 'L_Eyelids_Blink_CrvBaseWire1ShapeOrig', 'R_Eyelids_DwStartMid_Ctrl_Offset_Grp', 'R_Eyelids_Up_11_Ctrl_OffsetPivot_Grp_Offset_Grp', 'R_Eyelids_Dw_5_Ctrl_Offset_Grp', 'R_Eyelids_Up_1_Ctrl_OffsetPivot_Grp_Offset_Grp', 'L_Eyelids_Up_VtxJnts_Grp', 'R_Eyelids_Blink_BSSet', 'skinCluster37GroupId', 'L_Eyelids_Up__cv3_Bnd_scaleConstraint1', 'R_Eyelids_Dw_Origin_9_Jnt_aimConstraint1', 'L_Eyelids_Dw_2_Ctrl_OffsetPivot_Grp', 'R_Eyelids_Dw_Scale_Grp', 'L_Eyelids_Up_Vtx_CrvShapeOrig', 'L_Eyelids_DwEndMid_Ctrl_Offset_Grp', 'L_Eyelids_Up_7_Ctrl_Offset_Grp', 'R_Eyelids_Up_11_Jnt_Offset_Grp', 'R_Eyelids_Dw_8_Ctrl_OffsetPivot_Grp', 'L_Eyelids_Dw_Origin_8_Jnt', 'L_Eyelids_Scale_Ctrl_tag', 'R_Eyelids_Up_2_Ctrl_OffsetPivot_Grp', 'L_Eyelids_Dw_5_POCI', 'L_Eyelids_Dw_8_CtrlShape', 'L_Eyelids_Up_3_Loc', 'R_Eyelids_Dw_5_CtrlShape', 'L_Eyelids_UpEndMid_CtrlShape', 'R_Eyelids_Up__cv2_Bnd', 'R_Eyelids_Up_5_CtrlShape', 'L_Eyelids_Up_10_Loc', 'L_Eyelids_Up_11_Ctrl_Offset_Grp', 'R_Eyelids_Dw_3_Ctrl_OffsetPivot_Grp', 'L_Eyelids_Up_2_Ctrl_tag', 'L_Eyelids_Up_11_Ctrl', 'R_Eyelids_Up_Origin_11_Jnt_aimConstraint1', 'L_Eyelids_Up_8_Ctrl_Offset_Grp', 'L_Eyelids_Blink_BSSet', 'L_Eyelids_Up_11_Jnt_Offset_Grp', 'L_Eyelids_Dw_10_Ctrl_OffsetPivot_Grp_Offset_Grp', 'R_Eyelids_Up_1_Jnt_Offset_Grp', 'R_Eyelids_Dw_7_Jnt_Offset_Grp', 'L_Eyelids_Up_10_Jnt', 'R_Eyelids_Dw__cv4_Bnd', 'L_Eyelids_Up_Origin_10_Jnt', 'R_Eyelids_Blink_CrvBaseWire1ShapeOrig1', 'R_Eyelids_Dw_1_Ctrl', 'L_Eyelids_Dw_Scale_Grp', 'R_Eyelids_Dw__cv4_Bnd_parentConstraint1', 'R_Eyelids_UpMid_CtrlShape', 'unitConversion428', 'R_Eyelids_Up_Origin_0_Jnt_Offset_Grp', 'R_Eyelids_Dw_3_Jnt_Offset_Grp', 'R_Eyelids_Up_6_POCI', 'R_Eyelids_Dw_3_Ctrl_Offset_Grp', 'R_Eyelids_Dw_2_Ctrl', 'L_Eyelids_Dw__cv4_Bnd', 'R_Eyelids_Up_10_Ctrl', 'L_Eyelids_DwStartMid_Jnt_Offset_Grp', 'R_Eyelids_DwWire', 'R_Eyelids_Dw_9_Jnt_Offset_Grp', 'L_Eyelids_Dw_9_Ctrl_OffsetPivot_Grp_Offset_Grp', 'R_Eyelids_Up_0_POCI', 'R_Eyelids_Dw_9_Loc', 'R_Eyelids_Up_6_CtrlShape', 'L_Eyelids_Up_9_Ctrl_OffsetPivot_Grp_Offset_Grp', 'R_Eyelids_Dw_Origin_2_Jnt_aimConstraint1', 'R_Eyelids_Up_3_Ctrl_OffsetPivot_Grp_Offset_Grp', 'R_Eyelids_Dw_Origin_3_Jnt_Offset_Grp', 'R_Eyelids_Up_0_Jnt', 'R_Eyelids_Dw_Scale_Ctrl_tag', 'L_Eyelids_UpMid_Ctrl_tag', 'R_Eyelids_UpWireSet', 'unitConversion429', 'R_Eyelids_Up_Origin_6_Jnt_aimConstraint1', 'R_Eyelids_LwrBlink_BSGroupParts', 'R_Eyelids_Up_Origin_10_Jnt_Offset_Grp', 'R_Eyelids_Dw_3_CtrlShape', 'R_Eyelids_Up_BlinkTarget_CrvShapeOrig1', 'R_Eyelids_Dw_0_CtrlShape', 'L_Eyelids_Blink_BSGroupParts', 'R_Eyelids_Dw_BlinkTarget_CrvShapeOrig1', 'L_Eyelids_DwEndMid_Ctrl_tag', 'L_Eyelids_Dw_6_Loc', 'R_Eyelids_DwStartMid_Ctrl_tag', 'L_Eyelids_Up_9_Jnt_Offset_Grp', 'L_Eyelids_Up_WireDriver_CrvShapeOrig', 'R_Eyelids_Dw_VtxJnts_Grp', 'L_Eyelids_Dw__cv3_Bnd_parentConstraint1', 'L_Eyelids_UpMid_CtrlShape', 'L_Eyelids_Dw_0_CtrlShape', 'L_Eyelids_Dw_10_LocShape', 'L_Eyelids_UpEndMid_Jnt', 'L_EyelidsLwrBlink_CtrlShape', 'R_Eyelids_Up_Origin_11_Jnt', 'R_Eyelids_Dw_Tweeks_Ctrl_Grp', 'R_Eyelids_Up_11_Ctrl', 'R_Eyelids_Up_Origin_7_Jnt_aimConstraint1', 'R_Eyelids_Dw_5_Ctrl', 'R_Eyelids_Dw_10_LocShape', 'L_Eyelids_Dw_0_Loc', 'L_Eyelids_UpMid_Jnt_Offset_Grp', 'R_Eyelids_Blink_CrvShape', 'L_Eyelids_Dw_9_Ctrl_tag', 'R_Eyelids_Up__cv3_Bnd_parentConstraint1', 'L_Eyelids_Up_9_Jnt', 'R_Eyelids_Ctrl_Grp', 'R_Eyelids_Up_Vtx_CrvShape', 'R_Eyelids_UpWireGroupParts', 'L_Eyelids_Up_7_CtrlShape', 'L_Eyelids_Up_Scale_Ctrl_tag', 'L_Eyelids_Dw_Origin_2_Jnt_Offset_Grp', 'R_Eyelids_DwMid_Ctrl', 'L_Eyelids_Up_WireDriver_CrvBaseWireShapeOrig', 'L_Eyelids_DwEndMid_Ctrl', 'R_Eyelids_Dw_Origin_7_Jnt_Offset_Grp', 'R_Eyelids_Dw_Vtx_CrvShapeOrig', 'R_Eyelids_Dw_4_Jnt_Offset_Grp', 'L_Eyelids_Up_10_LocShape', 'R_Eyelids_Up_WireDriver_Crv', 'L_Eyelids_Up_9_CtrlShape', 'L_Eyelids_Dw_11_Loc', 'L_Eyelids_Dw_6_Ctrl_Offset_Grp', 'R_Eyelids_Up_3_Ctrl', 'L_Eyelids_EyePivot_LocShape', 'R_Eyelids_LwrBlink_BSSet', 'L_Eyelids_Up_Origin_3_Jnt_aimConstraint1', 'R_Eyelids_UpWireGroupId', 'L_Eyelids_Up_11_Ctrl_OffsetPivot_Grp_Offset_Grp', 'R_Eyelids_Dw_3_POCI', 'R_Eyelids_Up_Scale_Ctrl', 'L_Eyelids_Dw_Origin_4_Jnt_Offset_Grp', 'R_Eyelids_Dw_Scale_Ctrl_Offset_Grp', 'R_Eyelids_Dw_10_CtrlShape', 'R_Eyelids_Dw_Origin_7_Jnt', 'L_Eyelids_UpEndMid_Jnt_Offset_Grp_parentConstraint1', 'unitConversion426', 'L_Eyelids_Up_4_Ctrl_Offset_Grp', 'R_Eyelids_DwEndMid_CtrlShape', 'L_Eyelids_UpStart_Ctrl_tag', 'L_Eyelids_Up_7_LocShape', 'L_Eyelids_Dw__cv2_Bnd_parentConstraint1', 'R_Eyelids_Dw_Jnt_Grp', 'L_Eyelids_Up_Origin_4_Jnt_aimConstraint1', 'R_Eyelids_UpEnd_Jnt_Offset_Grp', 'L_Eyelids_Dw_Origin_2_Jnt', 'L_Eyelids_Dw_1_LocShape', 'L_Eyelids_Rig_Grp_parentConstraint1', 'L_Eyelids_Dw_0_Ctrl_Offset_Grp', 'L_Eyelids_Up_10_POCI', 'L_Eyelids_Up_2_Jnt', 'R_Eyelids_Dw_6_Ctrl_OffsetPivot_Grp', 'L_Eyelids_Dw_2_CtrlShape', 'R_Eyelids_Up_10_Ctrl_Offset_Grp', 'R_Eyelids_DwStart_CtrlShape', 'bindPose32', 'L_Eyelids_Dw_0_Ctrl_tag', 'L_Eyelids_Up_1_Loc', 'R_Eyelids_Dw_1_Ctrl_tag', 'R_Eyelids_Up_9_Ctrl', 'L_Eyelids_Up__cv4_Bnd_parentConstraint1', 'R_Eyelids_Up_Origin_1_Jnt_aimConstraint1', 'R_Eyelids_Scale_Ctrl', 'R_Eyelids_Dw_Wire', 'L_Eyelids_Blink_BSGroupId', 'R_Eyelids_Up__cv4_Bnd', 'R_Eyelids_DwMid_Jnt_Offset_Grp', 'R_Eyelids_Dw_1_Ctrl_Offset_Grp', 'R_Eyelids_Dw_WireDriver_CrvBaseWire', 'R_Eyelids_Dw_8_Ctrl_OffsetPivot_Grp_Offset_Grp', 'L_Eyelids_Up_Origin_3_Jnt', 'L_Eyelids_Up_Origin_6_Jnt_aimConstraint1', 'L_Eyelids_Up_3_LocShape', 'R_Eyelids_Dw_8_CtrlShape', 'L_Eyelids_Dw_4_Jnt', 'R_Eyelids_Up_11_POCI', 'L_Eyelids_Dw_2_Jnt_Offset_Grp', 'R_Eyelids_Dw_Origin_5_Jnt', 'R_Eyelids_Dw_0_Ctrl_tag', 'L_Eyelids_Dw__cv3_Bnd', 'R_Eyelids_Dw_3_Ctrl', 'L_Eyelids_Dw_5_LocShape', 'L_Eyelids_UpVector_LocShape', 'R_Eyelids_Up_6_Jnt', 'L_Eyelids_Dw__cv3_Bnd_scaleConstraint1', 'R_Eyelids_Dw_Origin_8_Jnt_Offset_Grp', 'R_Eyelids_Up_6_Ctrl_tag', 'L_Eyelids_Dw_Origin_7_Jnt_aimConstraint1', 'L_Eyelids_Dw_11_Ctrl_OffsetPivot_Grp_Offset_Grp', 'L_Eyelids_Dw_WireGroupParts', 'R_Eyelids_Dw_Origin_2_Jnt', 'L_Eyelids_Dw_0_POCI', 'R_Eyelids_Dw_BlinkTarget_Crv', 'R_Eyelids_Up_7_Ctrl_tag', 'L_Eyelids_Up_5_Loc', 'L_Eyelids_Up_7_POCI', 'R_Eyelids_Dw_Vtx_CrvShape', 'L_Eyelids_Up_3_Ctrl', 'R_Eyelids_Up_9_CtrlShape', 'L_Eyelids_Up_5_CtrlShape', 'L_Eyelids_Dw_8_Ctrl', 'R_Eyelids_Up_Origin_3_Jnt', 'R_Eyelids_Dw_Origin_5_Jnt_aimConstraint1', 'L_Eyelids_Dw_9_Loc', 'R_Eyelids_Scale_Grp', 'R_Eyelids_Up_WireGroupParts', 'L_Eyelids_Up_Origin_2_Jnt_aimConstraint1', 'R_Eyelids_Up_AimLocators_Grp', 'L_Eyelids_UpStartMid_Ctrl', 'R_Eyelids_Up_WireSet', 'R_Eyelids_Up_Origin_0_Jnt_aimConstraint1', 'R_Eyelids_Up_8_Loc', 'R_Eyelids_Up_8_Jnt_Offset_Grp', 'R_Eyelids_Dw_Origin_10_Jnt_aimConstraint1', 'R_Eyelids_Up_BlinkTarget_Crv', 'L_Eyelids_DwMid_Ctrl_tag', 'L_Eyelids_Dw_Origin_7_Jnt_Offset_Grp', 'R_Eyelids_Dw_Vtx_Crv', 'L_Eyelids_Up_8_Ctrl_tag', 'R_Eyelids_Dw_Origin_2_Jnt_Offset_Grp', 'L_Eyelids_Up_8_Ctrl_OffsetPivot_Grp_Offset_Grp', 'L_Eyelids_Dw__cv4_Bnd_scaleConstraint1', 'L_Eyelids_Dw_10_CtrlShape', 'L_Eyelids_Dw_11_Ctrl_OffsetPivot_Grp', 'L_Eyelids_Dw_1_Ctrl_OffsetPivot_Grp', 'R_Eyelids_Dw_Origin_6_Jnt_Offset_Grp', 'R_Eyelids_Dw_WireDriver_CrvShapeOrig1', 'R_EyelidsUprBlink_Ctrl', 'R_Eyelids_Up_3_POCI', 'R_Eyelids_Scale_Ctrl_tag', 'L_Eyelids_Dw_Vtx_Crv', 'R_Eyelids_Up_3_Ctrl_tag', 'unitConversion427', 'L_Eyelids_Up_Origin_8_Jnt', 'L_EyelidsLwrBlink_Ctrl_tag', 'L_Eyelids_UpStartMid_CtrlShape', 'R_Eyelids_UpEndMid_Jnt_Offset_Grp', 'R_Eyelids_Blink_CrvShapeOrig1', 'R_Eyelids_Up_4_POCI', 'R_Eyelids_Up_4_Ctrl_tag', 'L_Eyelids_Up_4_Ctrl_OffsetPivot_Grp_Offset_Grp', 'L_Eyelids_Dw_10_Jnt', 'R_Eyelids_UpMid_Jnt_Offset_Grp', 'L_Eyelids_Up_4_Jnt_Offset_Grp', 'L_Eyelids_Blink_CrvShapeOrig1', 'R_Eyelids_Up_10_LocShape', 'L_Eyelids_Scale_CtrlShape', 'L_Eyelids_Up_0_POCI', 'L_Eyelids_UpEnd_Jnt_Offset_Grp', 'LwrBlink_MultDiv1', 'L_Eyelids_Up_7_Jnt', 'R_Eyelids_Up_WireDriver_CrvShapeOrig1', 'R_Eyelids_Up__cv2_Bnd_scaleConstraint1', 'L_Eyelids_Rig_Grp_scaleConstraint1', 'L_Eyelids_Dw_Origin_11_Jnt_Offset_Grp', 'LwrBlink_MultDiv5', 'R_Eyelids_Dw_1_Ctrl_OffsetPivot_Grp_Offset_Grp', 'R_Eyelids_DwStartMid_Ctrl_Offset_Grp_parentConstraint1', 'R_Eyelids_Dw_9_POCI', 'L_Eyelids_Up_6_Ctrl_OffsetPivot_Grp_Offset_Grp', 'R_Eyelids_Up_11_Ctrl_OffsetPivot_Grp', 'R_Eyelids_Up_BlinkTarget_CrvShape', 'R_Eyelids_Dw_11_Ctrl_Offset_Grp', 'R_Eyelids_DwWireSet', 'L_Eyelids_Scale_Jnt', 'R_Eyelids_Up_5_Ctrl_OffsetPivot_Grp', 'L_Eyelids_Up_WireGroupId', 'skinCluster37', 'L_Eyelids_Up_Origin_3_Jnt_Offset_Grp', 'R_Eyelids_Scale_Jnt_Offset_Grp', 'R_Eyelids_Up_Origin_3_Jnt_Offset_Grp', 'R_Eyelids_Up_5_Loc', 'L_Eyelids_Dw_8_Ctrl_tag', 'L_Eyelids_Rig_Grp', 'L_Eyelids_Dw_Vtx_CrvShapeOrig', 'R_Eyelids_Dw_Origin_5_Jnt_Offset_Grp', 'R_Eyelids_Dw_11_Ctrl_OffsetPivot_Grp_Offset_Grp', 'R_Eyelids_Dw_Origin_1_Jnt', 'L_Eyelids_Up_4_POCI', 'R_Eyelids_Dw_Origin_9_Jnt_Offset_Grp', 'R_Eyelids_Up_1_Ctrl_Offset_Grp', 'R_Eyelids_Dw_10_Ctrl_Offset_Grp', 'skinCluster38', 'L_Eyelids_Dw_9_Ctrl_OffsetPivot_Grp', 'R_Eyelids_Up_2_Ctrl_Offset_Grp', 'L_Eyelids_Dw_Origin_9_Jnt_aimConstraint1', 'unitConversion430', 'R_Eyelids_Dw_2_Loc', 'L_Eyelids_Up_5_Ctrl_tag', 'L_Eyelids_UpEndMid_Ctrl_Offset_Grp_parentConstraint1', 'R_Eyelids_BlinkAttrs_Ctrl', 'L_Eyelids_DwEnd_Jnt', 'L_Eyelids_Up_Origin_5_Jnt_Offset_Grp', 'bindPose31', 'R_Eyelids_Up_0_LocShape', 'R_Eyelids_Up_Origin_8_Jnt_Offset_Grp', 'L_Eyelids_Dw_4_Ctrl_OffsetPivot_Grp_Offset_Grp', 'R_Eyelids_DwEnd_Ctrl_Offset_Grp', 'R_Eyelids_Dw_Scale_Ctrl', 'R_Eyelids_Up_Scale_CtrlShape', 'R_Eyelids_UpEnd_Jnt', 'L_Eyelids_Blink_Crv', 'L_Eyelids_Dw_8_Ctrl_Offset_Grp', 'R_Eyelids_Up_10_CtrlShape', 'R_Eyelids_Dw_0_Ctrl_Offset_Grp', 'skinCluster35', 'L_Eyelids_Dw_8_Ctrl_OffsetPivot_Grp_Offset_Grp', 'L_Eyelids_DwStart_Jnt', 'R_Eyelids_Dw_2_Ctrl_OffsetPivot_Grp_Offset_Grp', 'L_Eyelids_Up_0_Ctrl_OffsetPivot_Grp_Offset_Grp', 'R_Eyelids_Dw_3_LocShape', 'bindPose30', 'R_Eyelids_Up_0_Ctrl_tag', 'L_Eyelids_Up_7_Ctrl_OffsetPivot_Grp', 'R_Eyelids_Dw_6_LocShape', 'L_Eyelids_Dw_WireDriver_Crv', 'L_Eyelids_Dw_5_Ctrl_tag', 'R_Eyelids_Dw_8_Ctrl_tag', 'R_Eyelids_Dw_Origin_11_Jnt', 'R_Eyelids_Dw_7_LocShape', 'R_Eyelids_Up_2_CtrlShape', 'L_Eyelids_DwWireSet', 'L_Eyelids_Up_5_Jnt_Offset_Grp', 'R_Eyelids_Dw_5_Loc', 'R_Eyelids_Up_2_Ctrl', 'L_Eyelids_Dw_11_CtrlShape', 'L_Eyelids_Dw_6_CtrlShape', 'R_Eyelids_UpStartMid_Ctrl_Offset_Grp', 'R_Eyelids_Dw_Origin_0_Jnt_aimConstraint1', 'R_Eyelids_Up_9_Ctrl_OffsetPivot_Grp', 'R_Eyelids_DwStartMid_Jnt_Offset_Grp', 'L_Eyelids_Up_9_Ctrl_tag', 'R_Eyelids_Dw_4_Ctrl_OffsetPivot_Grp', 'R_Eyelids_Up_11_LocShape', 'L_Eyelids_Up_7_Ctrl_OffsetPivot_Grp_Offset_Grp', 'L_Eyelids_BlinkAttrs_CtrlShape', 'L_Eyelids_Dw_8_Loc', 'R_Eyelids_Dw_11_Jnt_Offset_Grp', 'R_Eyelids_Up_10_Loc', 'L_Eyelids_Up_5_Ctrl', 'L_Eyelids_Up_6_Loc', 'R_Eyelids_Dw_Origin_11_Jnt_Offset_Grp', 'L_Eyelids_Up_0_Jnt', 'L_Eyelids_Up_Origin_0_Jnt_Offset_Grp', 'R_Eyelids_Dw_Origin_3_Jnt', 'L_Eyelids_Dw_Origin_1_Jnt_Offset_Grp', 'R_Eyelids_Dw_Origin_4_Jnt_aimConstraint1', 'R_Eyelids_DwStartMid_Jnt_Offset_Grp_parentConstraint1', 'L_Eyelids_Up_Origin_10_Jnt_aimConstraint1', 'R_Eyelids_Blink_CrvBaseWire1Shape', 'R_Eyelids_Dw_8_Ctrl', 'L_Eyelids_Dw_2_Loc', 'L_Eyelids_Dw_BlinkTarget_Crv', 'R_Eyelids_Up_Scale_Grp', 'L_Eyelids_Up_10_Ctrl', 'L_Eyelids_Scale_Grp_Offset_Grp', 'L_EyelidsLwrBlink_Ctrl_Offset_Grp', 'skinCluster35Set', 'R_Eyelids_DwStartMid_Ctrl', 'L_Eyelids_Up_Origin_4_Jnt_Offset_Grp', 'L_Eyelids_Up_3_Ctrl_Offset_Grp', 'R_Eyelids_Up_0_Ctrl', 'L_Eyelids_Up_4_LocShape', 'L_Eyelids_UpEndMid_Ctrl_tag', 'R_Eyelids_Dw__cv2_Bnd', 'L_Eyelids_Up_0_Jnt_Offset_Grp', 'R_Eyelids_Up_3_Ctrl_OffsetPivot_Grp', 'L_Eyelids_Dw_9_CtrlShape', 'R_Eyelids_Dw_1_Ctrl_OffsetPivot_Grp', 'R_Eyelids_Up_7_Loc', 'L_Eyelids_Up_WireDriver_CrvBaseWire', 'R_Eyelids_Up_4_Jnt', 'R_Eyelids_Dw_6_Ctrl_OffsetPivot_Grp_Offset_Grp', 'L_Eyelids_Dw_Tweeks_Ctrl_Grp', 'L_Eyelids_Dw_2_Ctrl', 'L_Eyelids_Dw_Ctrl_Grp', 'R_Eyelids_Dw_6_Ctrl_tag', 'R_Eyelids_Dw_6_Jnt_Offset_Grp', 'L_Eyelids_Up_3_Ctrl_OffsetPivot_Grp', 'L_Eyelids_Up_11_Ctrl_OffsetPivot_Grp', 'L_Eyelids_Up_8_Jnt', 'L_Eyelids_DwWire', 'R_Eyelids_Dw__cv3_Bnd_parentConstraint1', 'L_Eyelids_Up_1_Jnt_Offset_Grp', 'L_Eyelids_Dw_7_CtrlShape', 'R_Eyelids_Scale_CtrlShape', 'L_Eyelids_Dw_Origin_6_Jnt_Offset_Grp', 'unitConversion425', 'R_Eyelids_Up_4_LocShape', 'R_Eyelids_Dw_10_Ctrl_OffsetPivot_Grp', 'R_Eyelids_DwEndMid_Ctrl_tag', 'L_Eyelids_Dw_Origin_10_Jnt_Offset_Grp', 'L_Eyelids_Dw_7_Ctrl_OffsetPivot_Grp_Offset_Grp', 'L_Eyelids_UpEndMid_Ctrl', 'R_Eyelids_Dw_0_Loc', 'L_Eyelids_UpStartMid_Jnt_Offset_Grp', 'R_Eyelids_Dw_Origin_0_Jnt', 'L_Eyelids_Up_2_Ctrl_OffsetPivot_Grp', 'R_Eyelids_Dw_WireDriver_CrvBaseWireShapeOrig', 'R_Eyelids_Up_9_Ctrl_tag', 'R_Eyelids_BlinkAttrs_Ctrl_tag', 'L_Eyelids_Scale_Jnt_Offset_Grp', 'R_Eyelids_Dw_Origin_11_Jnt_aimConstraint1', 'L_Eyelids_Dw_10_POCI', 'R_Eyelids_Dw_0_POCI', 'R_Eyelids_Dw_9_Ctrl_Offset_Grp', 'L_Eyelids_Up_Origin_9_Jnt_Offset_Grp', 'R_Eyelids_Dw__cv2_Bnd_parentConstraint1', 'R_Eyelids_Dw_4_Ctrl_OffsetPivot_Grp_Offset_Grp', 'L_Eyelids_Dw_Scale_Ctrl_tag', 'R_Eyelids_Dw_Origin_10_Jnt_Offset_Grp', 'R_Eyelids_Dw_1_Jnt_Offset_Grp', 'R_Eyelids_Dw_WireDriver_Crv', 'L_Eyelids_Up_6_CtrlShape', 'L_Eyelids_Dw_1_Ctrl_Offset_Grp', 'L_Eyelids_Up_9_LocShape', 'skinCluster36GroupId', 'L_Eyelids_Up_Jnt_Grp', 'R_Eyelids_Dw_7_Ctrl_OffsetPivot_Grp', 'L_Eyelids_Blink_CrvBaseWire1ShapeOrig1', 'L_Eyelids_Dw_5_Ctrl', 'L_Eyelids_Dw_Origin_1_Jnt_aimConstraint1', 'L_Eyelids_BlinkAttrs_Ctrl_Offset_Grp', 'R_Eyelids_EyePivot_LocShape', 'L_Eyelids_Dw_5_Ctrl_OffsetPivot_Grp_Offset_Grp', 'R_Eyelids_Up_7_CtrlShape', 'L_Eyelids_Up_2_Ctrl_Offset_Grp', 'LwrBlink_MultDiv', 'R_Eyelids_UpStart_Ctrl_tag', 'L_Eyelids_Dw_3_Jnt', 'L_Eyelids_Up__cv2_Bnd_scaleConstraint1', 'R_Eyelids_Dw_5_Jnt', 'R_Eyelids_Up_5_Jnt_Offset_Grp', 'L_Eyelids_DwEndMid_Ctrl_Offset_Grp_parentConstraint1', 'R_Eyelids_Up_WireDriver_CrvShape', 'R_Eyelids_Up_6_Ctrl_OffsetPivot_Grp_Offset_Grp', 'L_Eyelids_Dw_11_Jnt', 'L_Eyelids_Dw_3_Ctrl_OffsetPivot_Grp', 'L_Eyelids_Dw_4_Ctrl_OffsetPivot_Grp', 'L_Eyelids_Up_9_Loc', 'R_Eyelids_Rig_Grp_parentConstraint1', 'L_Eyelids_UprBlink_BSSet', 'R_Eyelids_Up_1_Ctrl_tag', 'R_Eyelids_Dw_6_CtrlShape', 'R_Eyelids_DwStart_Jnt_Offset_Grp', 'L_EyelidsUprBlink_CtrlShape', 'L_Eyelids_UpMid_Ctrl_Offset_Grp', 'R_Eyelids_Up_Origin_2_Jnt_Offset_Grp', 'R_Eyelids_Dw_Origin_7_Jnt_aimConstraint1', 'R_Eyelids_Ctrl_GrpMirror_Grp', 'UprBlink_MultDiv', 'L_Eyelids_DwEndMid_CtrlShape', 'L_Eyelids_DwEndMid_Jnt_Offset_Grp', 'L_Eyelids_Up_4_CtrlShape', 'R_Eyelids_Up_8_Ctrl_tag', 'L_Eyelids_Up_11_Loc', 'R_Eyelids_BlinkAttrs_CtrlShape', 'R_Eyelids_Dw_WireDriver_CrvShape', 'R_Eyelids_Dw_11_Loc', 'L_Eyelids_Dw_0_Ctrl_OffsetPivot_Grp_Offset_Grp', 'L_Eyelids_Dw_Origin_6_Jnt', 'L_Eyelids_Up_8_Ctrl', 'L_Eyelids_DwWireGroupId', 'R_Eyelids_Up_Origin_6_Jnt', 'R_Eyelids_Up_Origin_5_Jnt', 'R_Eyelids_Up_Tweeks_Ctrl_Grp', 'L_Eyelids_Dw_7_Loc', 'L_Eyelids_Up_1_CtrlShape', 'L_Eyelids_LwrBlink_BS', 'R_Eyelids_DwEndMid_Jnt_Offset_Grp_parentConstraint1', 'L_Eyelids_Up_5_POCI', 'L_Eyelids_Up__cv3_Bnd_parentConstraint1', 'L_Eyelids_Dw_Origin_4_Jnt', 'L_Eyelids_Up_5_Ctrl_OffsetPivot_Grp', 'R_Eyelids_Blink_Reverse', 'L_Eyelids_Up_3_CtrlShape', 'L_Eyelids_Dw_Origin_5_Jnt_Offset_Grp', 'R_Eyelids_Up_7_Ctrl_OffsetPivot_Grp', 'R_Eyelids_Up_0_Jnt_Offset_Grp', 'L_Eyelids_Dw_10_Jnt_Offset_Grp', 'skinCluster36GroupParts', 'R_Eyelids_Dw_2_Ctrl_tag', 'R_Eyelids_Dw_11_Ctrl', 'R_Eyelids_Dw_5_Ctrl_OffsetPivot_Grp_Offset_Grp', 'L_Eyelids_Up_1_Ctrl', 'L_Eyelids_Dw_WireDriver_CrvShapeOrig', 'R_Eyelids_Up_10_Ctrl_OffsetPivot_Grp', 'L_Eyelids_Up_BlinkTarget_CrvShapeOrig1', 'L_Eyelids_Up_Origin_4_Jnt', 'L_Eyelids_Dw_6_Jnt_Offset_Grp', 'R_Eyelids_Up_Vtx_Crv', 'R_Eyelids_UpMid_Jnt', 'R_Eyelids_DwStartMid_Jnt', 'LwrBlink_MultDiv4', 'L_Eyelids_Up_5_Ctrl_Offset_Grp', 'L_Eyelids_Dw_7_LocShape', 'R_Eyelids_Up_Jnt_Grp', 'R_Eyelids_Dw_6_Ctrl_Offset_Grp', 'R_Eyelids_DwEndMid_Jnt', 'R_Eyelids_Up_Origin_3_Jnt_aimConstraint1', 'R_Eyelids_Up_Ctrl_Grp', 'L_Eyelids_Up_0_Ctrl', 'L_Eyelids_Up_11_CtrlShape', 'R_EyelidsUprBlink_CtrlShape', 'R_Eyelids_Up_6_LocShape', 'L_Eyelids_Up_Origin_1_Jnt_aimConstraint1', 'L_Eyelids_UpStart_CtrlShape', 'L_Eyelids_Dw_WireDriver_CrvBaseWire', 'L_Eyelids_Dw_1_Ctrl_tag', 'L_Eyelids_DwEnd_Ctrl_Offset_Grp', 'R_Eyelids_Dw_8_Jnt', 'R_Eyelids_Dw_2_LocShape', 'R_Eyelids_Dw_11_Ctrl_OffsetPivot_Grp', 'L_Eyelids_Up_Ctrl_Grp', 'L_Eyelids_Scale_Ctrl_Offset_Grp', 'R_Eyelids_Blink_CrvBaseWire1ShapeOrig', 'L_Eyelids_Dw_BlinkTarget_CrvShapeOrig', 'R_Eyelids_Up_11_Ctrl_Offset_Grp', 'L_Eyelids_Dw_Vtx_CrvShape', 'L_Eyelids_Up_Origin_8_Jnt_aimConstraint1', 'R_EyelidsLwrBlink_Ctrl_Offset_Grp', 'R_Eyelids_Up_7_Ctrl_OffsetPivot_Grp_Offset_Grp', 'R_Eyelids_UpStartMid_Ctrl', 'L_Eyelids_Dw_Origin_3_Jnt', 'L_Eyelids_UpWireGroupId', 'R_Eyelids_Blink_CrvBaseWireShape', 'L_Eyelids_LwrBlink_BSGroupId', 'L_Eyelids_Up_WireSet', 'L_Eyelids_Up_BlinkTarget_CrvShapeOrig', 'L_Eyelids_DwMid_Ctrl_Offset_Grp', 'L_Eyelids_Dw_Scale_Grp_Offset_Grp', 'L_Eyelids_UprBlink_BSGroupId', 'L_Eyelids_Up_Origin_11_Jnt_Offset_Grp', 'L_Eyelids_Dw_8_POCI', 'L_Eyelids_Blink_CrvBaseWireShapeOrig2', 'L_Eyelids_Dw_2_LocShape', 'R_Eyelids_Dw_2_POCI', 'L_Eyelids_Up_BlinkTarget_Crv', 'R_Eyelids_Scale_Grp_Offset_Grp', 'L_Eyelids_Up_Origin_2_Jnt', 'R_Eyelids_Up_5_Ctrl_tag', 'L_Eyelids_Dw_9_POCI', 'R_Eyelids_Up_Origin_1_Jnt', 'R_Eyelids_Up_7_POCI', 'L_Eyelids_Dw_7_Ctrl_OffsetPivot_Grp', 'L_Eyelids_Up_Tweeks_Ctrl_Grp', 'L_Eyelids_UpEndMid_Jnt_Offset_Grp', 'L_Eyelids_Dw_2_Ctrl_OffsetPivot_Grp_Offset_Grp', 'L_Eyelids_Dw_9_Jnt_Offset_Grp', 'R_Eyelids_Up_3_Jnt', 'R_Eyelids_Dw_0_Jnt', 'R_Eyelids_DwEnd_Jnt_Offset_Grp', 'L_Eyelids_Dw_6_LocShape', 'bindPose29', 'R_Eyelids_Up_10_Ctrl_OffsetPivot_Grp_Offset_Grp', 'R_Eyelids_DwEndMid_Ctrl_Offset_Grp_parentConstraint1', 'L_Eyelids_Up_7_Loc', 'L_Eyelids_Dw_5_Ctrl_Offset_Grp', 'L_Eyelids_Dw_Origin_2_Jnt_aimConstraint1', 'L_Eyelids_Up_8_Jnt_Offset_Grp', 'L_Eyelids_Dw_Wire', 'R_Eyelids_UpStartMid_Jnt', 'R_Eyelids_DwEndMid_Ctrl_Offset_Grp', 'L_Eyelids_Dw_2_POCI', 'L_Eyelids_Dw_3_Ctrl', 'R_Eyelids_Dw_Scale_CtrlShape', 'L_Eyelids_Up_10_Ctrl_tag', 'L_Eyelids_Up_11_Jnt', 'R_Eyelids_Up_9_Loc', 'R_Eyelids_Dw_10_Loc', 'R_Eyelids_Blink_CrvBaseWire1ShapeOrig2', 'L_Eyelids_Up_11_Ctrl_tag', 'L_Eyelids_Dw_Origin_8_Jnt_aimConstraint1', 'R_Eyelids_Dw_0_Ctrl', 'L_Eyelids_Ctrl_Grp', 'R_Eyelids_UprBlink_BSSet', 'L_Eyelids_Dw_3_Ctrl_Offset_Grp', 'L_Eyelids_Dw_4_Ctrl', 'R_Eyelids_Up_WireDriver_CrvBaseWire', 'R_Eyelids_UpVector_Loc', 'L_Eyelids_Blink_CrvBaseWire1ShapeOrig2', 'R_Eyelids_UpVector_LocShape', 'R_Eyelids_Blink_BS', 'R_Eyelids_Up_8_LocShape', 'L_Eyelids_Up_2_Loc', 'L_Eyelids_Dw_11_POCI', 'R_Eyelids_DwMid_Ctrl_Offset_Grp', 'L_Eyelids_Dw_11_Jnt_Offset_Grp', 'R_Eyelids_UpEnd_Ctrl', 'R_Eyelids_DwStart_Ctrl_Offset_Grp', 'L_Eyelids_Dw_3_Ctrl_tag', 'L_Eyelids_Dw_BlinkTarget_CrvShape', 'R_Eyelids_Dw_4_POCI', 'R_Eyelids_Dw_4_CtrlShape', 'R_Eyelids_Up_4_Ctrl_Offset_Grp', 'L_Eyelids_UpEnd_Ctrl_tag', 'R_Eyelids_Dw_4_Ctrl', 'L_Eyelids_Dw_10_Ctrl_OffsetPivot_Grp', 'R_Eyelids_UpStart_Jnt', 'L_Eyelids_Up_6_LocShape', 'L_Eyelids_Up_Origin_11_Jnt_aimConstraint1', 'L_Eyelids_Up_10_Ctrl_OffsetPivot_Grp', 'L_Eyelids_Dw_WireDriver_CrvShape', 'L_Eyelids_Dw_Scale_CtrlShape', 'L_Eyelids_Up_11_LocShape', 'R_Eyelids_Up_2_LocShape', 'L_Eyelids_Dw_Origin_0_Jnt_Offset_Grp', 'R_Eyelids_Up_Origin_1_Jnt_Offset_Grp', 'R_EyelidsUprBlink_Ctrl_tag', 'R_Eyelids_Dw_WireGroupParts', 'R_Eyelids_Up_2_Ctrl_OffsetPivot_Grp_Offset_Grp', 'R_Eyelids_Up_WireDriver_CrvBaseWireShapeOrig', 'R_Eyelids_Dw_9_Ctrl_tag', 'L_Eyelids_Dw_8_LocShape', 'R_Eyelids_UpEnd_Ctrl_Offset_Grp', 'R_Eyelids_Dw_9_LocShape', 'L_Eyelids_DwStartMid_Jnt_Offset_Grp_parentConstraint1', 'R_Eyelids_Dw_9_Ctrl', 'L_Eyelids_DwMid_CtrlShape', 'L_Eyelids_Up_Vtx_Crv', 'R_Eyelids_Up_3_Jnt_Offset_Grp', 'L_Eyelids_Dw_7_Jnt', 'L_Eyelids_Dw_9_Jnt', 'R_Eyelids_Up_Origin_7_Jnt_Offset_Grp', 'L_Eyelids_Dw_Origin_3_Jnt_Offset_Grp', 'R_Eyelids_Dw_Origin_6_Jnt_aimConstraint1', 'L_Eyelids_Dw_WireDriver_CrvShapeOrig1', 'skinCluster35GroupParts', 'R_Eyelids_Dw_8_Ctrl_Offset_Grp', 'L_Eyelids_Up_9_Ctrl_Offset_Grp', 'R_Eyelids_Dw_3_Ctrl_tag', 'L_Eyelids_Up_1_Ctrl_tag', 'L_Eyelids_Dw_Origin_10_Jnt', 'R_Eyelids_Up_5_LocShape', 'R_Eyelids_Dw_7_POCI', 'L_Eyelids_UpEnd_CtrlShape', 'L_Eyelids_UpStartMid_Ctrl_tag', 'L_Eyelids_Blink_CrvShapeOrig', 'R_Eyelids_Up__cv4_Bnd_parentConstraint1', 'R_Eyelids_UpEnd_Ctrl_tag', 'R_Eyelids_Up_2_Loc', 'L_Eyelids_Up_5_LocShape', 'L_Eyelids_Up_4_Ctrl', 'L_Eyelids_UpMid_Jnt', 'L_Eyelids_Scale_Grp', 'L_Eyelids_Up__cv4_Bnd', 'R_Eyelids_Up_9_Ctrl_Offset_Grp', 'R_Eyelids_Up_7_LocShape', 'R_Eyelids_Dw_8_LocShape', 'R_Eyelids_Up_11_Loc', 'R_Eyelids_Rig_Grp', 'L_Eyelids_Up_9_POCI', 'L_Eyelids_Dw_4_LocShape', 'R_Eyelids_Up_Vtx_CrvShapeOrig', 'R_Eyelids_Up_Origin_4_Jnt_aimConstraint1', 'L_Eyelids_Dw_6_POCI', 'L_Eyelids_Dw_0_Ctrl_OffsetPivot_Grp', 'R_Eyelids_Dw_9_Ctrl_OffsetPivot_Grp_Offset_Grp', 'L_Eyelids_Dw_WireGroupId', 'L_Eyelids_Up_11_POCI', 'L_Eyelids_Dw_9_LocShape', 'L_Eyelids_Up_0_Ctrl_OffsetPivot_Grp', 'L_Eyelids_Up_Scale_Ctrl_Offset_Grp', 'R_Eyelids_Dw_5_Ctrl_OffsetPivot_Grp', 'L_Eyelids_Dw_3_POCI', 'R_Eyelids_Up_Origin_10_Jnt', 'R_Eyelids_Up_2_Jnt_Offset_Grp', 'L_Eyelids_Up_Origin_6_Jnt_Offset_Grp', 'L_Eyelids_Up_3_Ctrl_tag', 'R_Eyelids_DwMid_CtrlShape', 'L_Eyelids_Dw_1_CtrlShape', 'R_Eyelids_UpEndMid_CtrlShape', 'L_Eyelids_Dw_Origin_9_Jnt', 'L_Eyelids_Up_0_Loc', 'R_Eyelids_Dw__cv2_Bnd_scaleConstraint1', 'L_Eyelids_Dw_6_Jnt', 'L_Eyelids_DwEnd_Jnt_Offset_Grp', 'R_Eyelids_Up_5_Ctrl_Offset_Grp', 'L_Eyelids_BlinkAttrs_Ctrl', 'R_Eyelids_Up_8_Ctrl_Offset_Grp', 'R_Eyelids_Up_WireGroupId', 'R_Eyelids_UpWire', 'R_Eyelids_Dw_7_Ctrl_tag', 'R_Eyelids_Dw_WireGroupId', 'L_Eyelids_Up_6_Ctrl_tag', 'L_Eyelids_Up_6_Ctrl_Offset_Grp', 'R_Eyelids_Up_WireDriver_CrvBaseWireShape', 'R_Eyelids_Dw_3_Loc', 'L_Eyelids_Dw_11_Ctrl_Offset_Grp', 'R_Eyelids_Up_1_LocShape', 'L_Eyelids_Blink_CrvBaseWire', 'R_Eyelids_Dw_Origin_0_Jnt_Offset_Grp', 'L_Eyelids_Up_Origin_7_Jnt_aimConstraint1', 'LwrBlink_MultDiv2', 'L_Eyelids_Dw_11_LocShape', 'R_Eyelids_Up_1_POCI', 'R_Eyelids_Rig_Grp_scaleConstraint1', 'R_Eyelids_Dw_AimLocators_Grp', 'R_Eyelids_Up_5_POCI', 'R_Eyelids_Dw_0_Ctrl_OffsetPivot_Grp_Offset_Grp', 'L_Eyelids_Up_WireDriver_CrvBaseWireShape', 'R_Eyelids_UpEndMid_Ctrl_tag', 'L_Eyelids_Dw_5_Jnt', 'R_Eyelids_Up_6_Loc', 'R_Eyelids_UprBlink_BSGroupId', 'UprBlink_MultDiv1', 'R_Eyelids_Up_2_POCI', 'R_Eyelids_Up_4_Loc', 'R_Eyelids_UpEndMid_Jnt_Offset_Grp_parentConstraint1', 'L_Eyelids_Up_10_Ctrl_Offset_Grp', 'R_Eyelids_Dw_2_Jnt', 'L_Eyelids_Up_Scale_Ctrl', 'R_Eyelids_Up__cv3_Bnd_scaleConstraint1', 'R_Eyelids_Dw_4_Jnt', 'R_Eyelids_Dw_Origin_8_Jnt', 'R_Eyelids_Dw_0_Ctrl_OffsetPivot_Grp', 'L_Eyelids_Dw_4_POCI', 'L_Eyelids_Up_5_Jnt', 'L_Eyelids_Dw_2_Jnt', 'L_Eyelids_Up_Origin_1_Jnt_Offset_Grp', 'R_Eyelids_Up_2_Ctrl_tag', 'R_Eyelids_Dw_11_LocShape', 'L_Eyelids_Up_Scale_Grp_Offset_Grp', 'L_Eyelids_Up_Origin_0_Jnt_aimConstraint1', 'R_Eyelids_Dw_7_Ctrl_OffsetPivot_Grp_Offset_Grp', 'R_Eyelids_Up_0_Ctrl_Offset_Grp', 'R_Eyelids_Dw_11_POCI', 'R_Eyelids_Dw_Ctrl_Grp', 'L_Eyelids_Up_BlinkTarget_CrvShape', 'R_Eyelids_UprBlink_BS', 'L_Eyelids_Dw_10_Ctrl', 'R_Eyelids_Dw_7_Ctrl', 'L_Eyelids_Up_Origin_6_Jnt', 'R_Eyelids_DwStart_Ctrl', 'L_Eyelids_DwStart_Jnt_Offset_Grp', 'L_Eyelids_UpStartMid_Jnt_Offset_Grp_parentConstraint1', 'R_Eyelids_Up_Origin_8_Jnt', 'R_Eyelids_DwStartMid_CtrlShape', 'R_Eyelids_Up_0_Ctrl_OffsetPivot_Grp_Offset_Grp', 'L_Eyelids_Dw_7_Jnt_Offset_Grp', 'R_Eyelids_Dw_0_Jnt_Offset_Grp', 'R_Eyelids_Dw_9_Ctrl_OffsetPivot_Grp', 'L_Eyelids_DwMid_Ctrl', 'L_Eyelids_Up_4_Jnt', 'L_Eyelids_Dw_8_Ctrl_OffsetPivot_Grp', 'R_Eyelids_Up_9_Ctrl_OffsetPivot_Grp_Offset_Grp', 'L_Eyelids_Up_1_LocShape', 'L_Eyelids_Dw_4_Loc', 'L_Eyelids_Up_4_Ctrl_tag', 'L_Eyelids_Dw_11_Ctrl', 'R_Eyelids_Blink_BSGroupId', 'R_Eyelids_Up_Origin_8_Jnt_aimConstraint1', 'L_Eyelids_DwStart_CtrlShape', 'R_Eyelids_Up_7_Jnt', 'R_Eyelids_Up_6_Ctrl_OffsetPivot_Grp', 'L_Eyelids_Dw_5_Ctrl_OffsetPivot_Grp', 'R_Eyelids_Up_5_Ctrl', 'R_Eyelids_Dw_10_Ctrl_tag', 'L_Eyelids_DwStartMid_Ctrl', 'R_Eyelids_DwStart_Jnt', 'R_Eyelids_Up_11_Jnt', 'L_Eyelids_Up_1_POCI', 'R_Eyelids_Dw_1_LocShape', 'R_Eyelids_Dw_7_Ctrl_Offset_Grp', 'L_Eyelids_Up_6_Jnt', 'L_Eyelids_Up_2_CtrlShape', 'R_Eyelids_Dw_5_Jnt_Offset_Grp', 'R_Eyelids_Up_7_Ctrl_Offset_Grp', 'L_Eyelids_Up_Origin_10_Jnt_Offset_Grp', 'R_Eyelids_Blink_CrvShapeOrig2', 'R_Eyelids_Dw_2_Ctrl_Offset_Grp', 'L_Eyelids_Dw_7_POCI', 'R_Eyelids_Up_0_CtrlShape', 'R_Eyelids_Up_4_Ctrl', 'L_Eyelids_Up_3_Jnt', 'R_Eyelids_Up_Scale_Ctrl_tag', 'R_Eyelids_Up_7_Jnt_Offset_Grp', 'R_Eyelids_Up_6_Ctrl', 'L_Eyelids_Up_1_Ctrl_Offset_Grp', 'L_Eyelids_DwEnd_CtrlShape', 'L_Eyelids_Up_Origin_2_Jnt_Offset_Grp']");
createNode joint -n "Eyelids_Guide" -p "L_Eyelids_Block";
	rename -uid "A5597B7D-44E8-0212-CEA5-7EAA351F5C00";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2026/scripts/Mutant_Tools/Icons/";
	setAttr ".t" -type "double3" 6.3752126693725586 180.17467498779297 11.018095016479492 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".radi" 1.5;
createNode dagContainer -n "L_Orbicularis_Block" -p "Face";
	rename -uid "22A60C0F-4CE5-0F78-3EC0-F8B837362C8D";
	addAttr -ci true -sn "nts" -ln "notes" -dt "string";
	setAttr ".isc" yes;
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2026/scripts/Mutant_Tools/Icons/Ribbon.png";
	setAttr ".ctor" -type "string" "rodri";
	setAttr ".cdat" -type "string" "2025/12/11 09:45:13";
	setAttr -l on -k off ".v";
	setAttr -l on -k off ".tx";
	setAttr -l on -k off ".ty";
	setAttr -l on -k off ".tz";
	setAttr -l on -k off ".rx";
	setAttr -l on -k off ".ry";
	setAttr -l on -k off ".rz";
	setAttr -l on -k off ".sx";
	setAttr -l on -k off ".sy";
	setAttr -l on -k off ".sz";
	setAttr ".nts" -type "string" (
		"['L_Orbicularis_1_Bind_04_Bnd_parentConstraint1', 'L_Orbicularis_1_ribbon_surface', 'L_Orbicularis_1_follicle_01_scaleConstraint1', 'L_Orbicularis_1_follicle_Shape6', 'L_Orbicularis_1_Ctrl_Joints_Grp', 'L_Orbicularis_1_00_CtrlShape01', 'L_Orbicularis_1_follicle_Shape8', 'L_Orbicularis_1_follicle_04_scaleConstraint1', 'L_Orbicularis_1_skinClusterGroupParts', 'L_Orbicularis_1_Ctrl_02_Jnt_parentConstraint1', 'L_Orbicularis_1_follicle_07_scaleConstraint1', 'L_Orbicularis_1_Bind_08_Bnd_parentConstraint1', 'L_Orbicularis_1_Ctrl_07_Jnt_scaleConstraint1', 'L_Orbicularis_1_05_Ctrl_tag', 'L_Orbicularis_1_Ctrl_03_Jnt', 'L_Orbicularis_1_02_Ctrl_tag', 'L_Orbicularis_1_follicle_Shape7', 'L_Orbicularis_1_Bind_04_Bnd_scaleConstraint1', 'L_Orbicularis_1_06_Ctrl_tag', 'L_Orbicularis_1_Bind_05_Bnd', 'L_Orbicularis_1_Ctrl_05_Jnt_scaleConstraint1', 'L_Orbicularis_1_Ctrl_05_Jnt_parentConstraint1', 'L_Orbicularis_1_Ctrl_06_Jnt_Offset_Grp', 'L_Orbicularis_1_05_Ctrl_Offset_Grp', 'L_Orbicularis_1_Bind_03_Bnd', 'L_Orbicularis_1_Bind_08_Bnd_scaleConstraint1', 'L_Orbicularis_1_Rig_Grp', 'L_Orbicularis_1_Ctrl_07_Jnt_parentConstraint1', 'L_Orbicularis_1_04_Ctrl_Offset_Grp', 'L_Orbicularis_1_Main_Ctrl_tag', 'L_Orbicularis_1_Ctrl_06_Jnt_scaleConstraint1', 'L_Orbicularis_1_02_CtrlShape01', 'L_Orbicularis_1_03_Ctrl_tag', 'L_Orbicularis_1_Ctrl_06_Jnt', 'L_Orbicularis_1_Ctrl_07_Jnt_Offset_Grp', 'L_Orbicularis_1_follicle_05', 'L_Orbicularis_Ctrl_Grp', 'L_Orbicularis_1_follicle_05_scaleConstraint1', 'L_Orbicularis_1_follicle_03_scaleConstraint1', 'L_Orbicularis_1_Bind_02_Bnd_scaleConstraint1', 'L_Orbicularis_1_follicle_Shape5', 'L_Orbicularis_1_00_Ctrl', 'L_Orbicularis_1_Ctrl_01_Jnt_Offset_Grp', 'L_Orbicularis_1_follicle_Shape2', 'L_Orbicularis_1_follicle_06_scaleConstraint1', 'L_Orbicularis_1_ribbon_surfaceShape', 'L_Orbicularis_1_Ctrl_03_Jnt_parentConstraint1', 'L_Orbicularis_1_04_Ctrl_tag', 'L_Orbicularis_1_Bind_02_Bnd_parentConstraint1', 'L_Orbicularis_1_02_Ctrl', 'L_Orbicularis_1_Ctrl_08_Jnt_scaleConstraint1', 'L_Orbicularis_1_Bind_01_Bnd', 'L_Orbicularis_1_follicle_Shape4', 'L_Orbicularis_1_03_Ctrl_Offset_Grp', 'L_Orbicularis_Rig_Grp', 'L_Orbicularis_1_Ctrl_01_Jnt_scaleConstraint1', 'L_Orbicularis_1_Bind_05_Bnd_scaleConstraint1', 'L_Orbicularis_1_skinCluster', 'L_Orbicularis_1_Ctrl_08_Jnt_parentConstraint1', 'L_Orbicularis_1_Ctrl_08_Jnt', 'L_Orbicularis_1_Bind_02_Bnd', 'L_Orbicularis_1_07_Ctrl', 'L_Orbicularis_1_Bnd_Grp', 'L_Orbicularis_1_follicle_07', 'L_Orbicularis_1_ribbon_surfaceShapeOrig', 'L_Orbicularis_1_00_Ctrl_tag', 'L_Orbicularis_1_follicle_03', 'L_Orbicularis_1_03_CtrlShape01', 'L_Orbicularis_1_Bind_01_Bnd_scaleConstraint1', 'L_Orbicularis_1_04_Ctrl', 'L_Orbicularis_1_Bind_07_Bnd_parentConstraint1', 'L_Orbicularis_1_Bind_03_Bnd_scaleConstraint1', 'L_Orbicularis_1_follicle_Shape3', 'L_Orbicularis_1_follicle_01', 'L_Orbicularis_1_skinClusterSet', 'L_Orbicularis_1_follicle_08_scaleConstraint1', 'L_Orbicularis_1_Ctrl_03_Jnt_Offset_Grp', 'L_Orbicularis_1_07_Ctrl_tag', 'L_Orbicularis_Ctrl_Grp_parentConstraint1', 'L_Orbicularis_1_Ctrl_04_Jnt_Offset_Grp', 'L_Orbicularis_1_Bind_08_Bnd', 'L_Orbicularis_1_Bind_06_Bnd', 'L_Orbicularis_1_Ctrl_01_Jnt_parentConstraint1', 'L_Orbicularis_1_Bind_05_Bnd_parentConstraint1', 'L_Orbicularis_1_01_CtrlShape01', 'L_Orbicularis_1_Ctrl_06_Jnt_parentConstraint1', 'L_Orbicularis_1_01_Ctrl', 'L_Orbicularis_1_Ctrl_04_Jnt_scaleConstraint1', 'L_Orbicularis_1_follicle_02', 'L_Orbicularis_1_Bind_06_Bnd_parentConstraint1', 'L_Orbicularis_1_Ctrl_02_Jnt_scaleConstraint1', 'L_Orbicularis_1_04_CtrlShape01', 'L_Orbicularis_1_skinClusterGroupId', 'L_Orbicularis_1_00_Ctrl_Offset_Grp', 'L_Orbicularis_1_Bind_06_Bnd_scaleConstraint1', 'L_Orbicularis_1_01_Ctrl_tag', 'L_Orbicularis_1_03_Ctrl', 'L_Orbicularis_1_07_Ctrl_Offset_Grp', 'L_Orbicularis_1_Follicles_Grp', 'L_Orbicularis_1_02_Ctrl_Offset_Grp', 'L_Orbicularis_1_05_Ctrl', 'L_Orbicularis_1_follicle_02_scaleConstraint1', 'L_Orbicularis_1_07_CtrlShape01', 'L_Orbicularis_1_Ctrls_Grp', 'L_Orbicularis_1_Ctrl_Main_Offset_Grp', 'L_Orbicularis_1_Ctrl_05_Jnt', 'L_Orbicularis_1_Bind_04_Bnd', 'L_Orbicularis_1_Ctrl_05_Jnt_Offset_Grp', 'L_Orbicularis_1_Ctrl_07_Jnt', 'L_Orbicularis_1_06_Ctrl_Offset_Grp', 'L_Orbicularis_1_Ctrl_04_Jnt', 'L_Orbicularis_1_05_CtrlShape01', 'L_Orbicularis_1_Bind_01_Bnd_parentConstraint1', 'L_Orbicularis_1_follicle_04', 'L_Orbicularis_1_Ctrl_08_Jnt_Offset_Grp', 'L_Orbicularis_1_Bind_07_Bnd_scaleConstraint1', 'L_Orbicularis_1_Ctrl_04_Jnt_parentConstraint1', 'L_Orbicularis_1_06_Ctrl', 'L_Orbicularis_1_Ctrl_02_Jnt', 'L_Orbicularis_1_follicle_08', 'L_Orbicularis_1_follicle_06', 'L_Orbicularis_1_Main_Ctrl', 'bindPose33', 'L_Orbicularis_Ctrl_Grp_scaleConstraint1', 'L_Orbicularis_1_Bind_03_Bnd_parentConstraint1', 'L_Orbicularis_1_06_CtrlShape01', 'L_Orbicularis_1_01_Ctrl_Offset_Grp', 'L_Orbicularis_1_Ctrl_02_Jnt_Offset_Grp', 'L_Orbicularis_1_Ctrl_03_Jnt_scaleConstraint1', 'L_Orbicularis_1_follicle_Shape1', 'L_Orbicularis_1_Ctrl_01_Jnt', 'L_Orbicularis_1_Bind_07_Bnd']");
createNode transform -n "L_Orbicularis_Guide" -p "L_Orbicularis_Block";
	rename -uid "3DC18106-44F9-ADAA-F35B-DBA408739281";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2026/scripts/Mutant_Tools/Icons/";
	setAttr ".t" -type "double3" 6.3752126693725586 180.17467498779297 14.518593996980398 ;
	setAttr ".r" -type "double3" 90.000000000000028 0 0 ;
	setAttr ".s" -type "double3" 2.2108883787186708 2.2108883787186708 2.2108883787186708 ;
createNode nurbsSurface -n "L_Orbicularis_GuideShape" -p "L_Orbicularis_Guide";
	rename -uid "12C8145B-41FD-D595-1B12-BC817729467A";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2026/scripts/Mutant_Tools/Icons/";
	setAttr -k off ".v";
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".tw" yes;
	setAttr -s 44 ".cp[0:43]" -type "double3" 0.49019966418191596 5.5511151231257827e-17 
		0.052925833840344216 1.0110892015110275 -0.64386552271170161 6.6613381477509392e-16 
		0.43496057081298845 -0.40420104652290689 0.12201184493811779 0.020665757476648672 
		0 0.051292794051605028 -0.081211366772246607 0 0.14167975535438904 -0.72283847299061144 
		-1.1102230246251565e-16 0.395420774079216 -0.29555490449333255 0 -0.047579191903132756 
		0 0 0 0 0 0 0 0 0 0 0 0 0.49019966418191596 0 0.052925833840344216 1.0110892015110275 
		-0.99999633238235863 9.9920072216264089e-16 0.43496057081298845 -0.40420104652290678 
		0.12201184493811779 0.020665757476648672 0 0.051292794051605028 -0.081211366772246607 
		2.7755575615628914e-17 0.14167975535438904 -0.72283847299061144 1.3877787807814457e-16 
		0.39542077407921594 -0.29555490449333255 0 -0.047579191903132756 0 0 0 0 0 0 0 0 
		0 0 0 0 0.49019966418191596 0 0.052925833840344216 1.0110892015110275 -0.99999633238236019 
		9.9920072216264089e-16 0.43496057081298845 -0.40420104652290678 0.12201184493811779 
		0.020665757476648672 0 0.051292794051605028 -0.081211366772246607 2.7755575615628914e-17 
		0.14167975535438904 -0.72283847299061144 1.3877787807814457e-16 0.39542077407921594 
		-0.29555490449333255 0 -0.047579191903132756 0 0 0 0 0 0 0 0 0 0 0 0 0.49019966418191596 
		0 0.052925833840344216 1.0110892015110275 -0.99999633238236019 9.9920072216264089e-16 
		0.43496057081298845 -0.40420104652290678 0.12201184493811779 0.020665757476648672 
		0 0.051292794051605028 -0.081211366772246607 0 0.14167975535438904 -0.72283847299061144 
		-1.1102230246251565e-16 0.395420774079216 -0.29555490449333255 0 -0.047579191903132756 
		0 0 0 0 0 0 0 0 0 0 0 0;
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr ".dvu" 0;
	setAttr ".dvv" 0;
	setAttr ".cpr" 4;
	setAttr ".cps" 4;
	setAttr ".nufa" 4.5;
	setAttr ".nvfa" 4.5;
createNode dagContainer -n "R_Orbicularis_Block" -p "Face";
	rename -uid "D55B18BD-4F3F-C355-F8E7-FB8909B38877";
	addAttr -ci true -sn "nts" -ln "notes" -dt "string";
	setAttr ".isc" yes;
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2026/scripts/Mutant_Tools/Icons/Ribbon.png";
	setAttr ".ctor" -type "string" "rodri";
	setAttr ".cdat" -type "string" "2025/12/11 09:50:16";
	setAttr -l on -k off ".v";
	setAttr -l on -k off ".tx";
	setAttr -l on -k off ".ty";
	setAttr -l on -k off ".tz";
	setAttr -l on -k off ".rx";
	setAttr -l on -k off ".ry";
	setAttr -l on -k off ".rz";
	setAttr -l on -k off ".sx";
	setAttr -l on -k off ".sy";
	setAttr -l on -k off ".sz";
	setAttr ".nts" -type "string" (
		"['R_Orbicularis_Ctrl_Grp_scaleConstraint1', 'R_Orbicularis_1_Bind_08_Bnd_scaleConstraint1', 'R_Orbicularis_1_Ctrl_04_Jnt_parentConstraint1', 'R_Orbicularis_1_Ctrl_07_Jnt_parentConstraint1', 'R_Orbicularis_1_02_CtrlShape01', 'R_Orbicularis_1_Bind_04_Bnd_parentConstraint1', 'R_Orbicularis_1_follicle_Shape5', 'R_Orbicularis_1_Bind_04_Bnd', 'R_Orbicularis_1_follicle_03_scaleConstraint1', 'R_Orbicularis_1_follicle_Shape3', 'R_Orbicularis_1_Ctrl_04_Jnt_scaleConstraint1', 'R_Orbicularis_1_Ctrl_02_Jnt_parentConstraint1', 'R_Orbicularis_1_02_Ctrl_tag', 'R_Orbicularis_1_00_CtrlShape01', 'R_Orbicularis_1_Bind_04_Bnd_scaleConstraint1', 'R_Orbicularis_1_skinClusterSet', 'R_Orbicularis_1_Ctrl_08_Jnt', 'R_Orbicularis_1_06_Ctrl', 'R_Orbicularis_1_Bind_03_Bnd_parentConstraint1', 'R_Orbicularis_1_Bind_03_Bnd', 'R_Orbicularis_1_04_Ctrl_tag', 'R_Orbicularis_1_skinClusterGroupParts', 'R_Orbicularis_1_Ctrls_Grp', 'R_Orbicularis_1_follicle_Shape8', 'R_Orbicularis_1_03_Ctrl', 'R_Orbicularis_1_Rig_Grp', 'R_Orbicularis_1_Ctrl_08_Jnt_parentConstraint1', 'R_Orbicularis_1_Bind_05_Bnd_scaleConstraint1', 'R_Orbicularis_1_06_CtrlShape01', 'R_Orbicularis_1_Ctrl_01_Jnt', 'R_Orbicularis_1_Ctrl_07_Jnt_scaleConstraint1', 'bindPose34', 'R_Orbicularis_1_follicle_Shape1', 'R_Orbicularis_1_Bind_01_Bnd_scaleConstraint1', 'R_Orbicularis_1_06_Ctrl_Offset_Grp', 'R_Orbicularis_1_Ctrl_03_Jnt', 'R_Orbicularis_1_Ctrl_07_Jnt_Offset_Grp', 'R_Orbicularis_1_Ctrl_05_Jnt_scaleConstraint1', 'R_Orbicularis_1_follicle_01_scaleConstraint1', 'R_Orbicularis_1_01_Ctrl_tag', 'R_Orbicularis_1_skinClusterGroupId', 'R_Orbicularis_1_Ctrl_Main_Offset_Grp', 'R_Orbicularis_1_07_Ctrl', 'R_Orbicularis_1_00_Ctrl_tag', 'R_Orbicularis_1_Bind_03_Bnd_scaleConstraint1', 'R_Orbicularis_1_07_Ctrl_Offset_Grp', 'R_Orbicularis_1_Bind_06_Bnd_scaleConstraint1', 'R_Orbicularis_1_follicle_Shape6', 'R_Orbicularis_1_Follicles_Grp', 'R_Orbicularis_1_follicle_04_scaleConstraint1', 'R_Orbicularis_1_03_CtrlShape01', 'R_Orbicularis_1_Ctrl_07_Jnt', 'R_Orbicularis_1_Ctrl_Joints_Grp', 'R_Orbicularis_1_Ctrl_01_Jnt_parentConstraint1', 'R_Orbicularis_1_Ctrl_06_Jnt_scaleConstraint1', 'R_Orbicularis_1_follicle_07_scaleConstraint1', 'R_Orbicularis_1_04_Ctrl_Offset_Grp', 'R_Orbicularis_1_Bind_01_Bnd', 'R_Orbicularis_1_00_Ctrl_Offset_Grp', 'R_Orbicularis_1_Ctrl_06_Jnt_Offset_Grp', 'R_Orbicularis_1_04_CtrlShape01', 'R_Orbicularis_1_Bnd_Grp', 'R_Orbicularis_1_Bind_07_Bnd', 'R_Orbicularis_1_03_Ctrl_tag', 'R_Orbicularis_1_Ctrl_06_Jnt', 'R_Orbicularis_1_follicle_Shape7', 'R_Orbicularis_1_Bind_02_Bnd', 'R_Orbicularis_1_06_Ctrl_tag', 'R_Orbicularis_1_follicle_Shape2', 'R_Orbicularis_1_Ctrl_04_Jnt_Offset_Grp', 'R_Orbicularis_1_05_CtrlShape01', 'R_Orbicularis_1_02_Ctrl', 'R_Orbicularis_1_05_Ctrl_Offset_Grp', 'R_Orbicularis_1_01_Ctrl', 'R_Orbicularis_1_skinCluster', 'R_Orbicularis_1_Bind_05_Bnd_parentConstraint1', 'R_Orbicularis_1_05_Ctrl_tag', 'R_Orbicularis_Rig_Grp', 'R_Orbicularis_1_Main_Ctrl_tag', 'R_Orbicularis_1_follicle_02', 'R_Orbicularis_1_follicle_06', 'R_Orbicularis_1_follicle_08_scaleConstraint1', 'R_Orbicularis_1_Bind_01_Bnd_parentConstraint1', 'R_Orbicularis_1_follicle_08', 'R_Orbicularis_1_follicle_01', 'R_Orbicularis_1_follicle_04', 'R_Orbicularis_1_Bind_07_Bnd_scaleConstraint1', 'R_Orbicularis_1_Ctrl_03_Jnt_Offset_Grp', 'R_Orbicularis_1_Ctrl_08_Jnt_Offset_Grp', 'R_Orbicularis_1_Ctrl_01_Jnt_scaleConstraint1', 'R_Orbicularis_1_Ctrl_04_Jnt', 'R_Orbicularis_Ctrl_Grp_parentConstraint1', 'R_Orbicularis_1_follicle_05', 'R_Orbicularis_1_Main_Ctrl', 'R_Orbicularis_1_ribbon_surface', 'R_Orbicularis_1_03_Ctrl_Offset_Grp', 'R_Orbicularis_1_follicle_03', 'R_Orbicularis_1_Bind_05_Bnd', 'R_Orbicularis_1_follicle_05_scaleConstraint1', 'R_Orbicularis_1_04_Ctrl', 'R_Orbicularis_1_follicle_07', 'R_Orbicularis_1_07_CtrlShape01', 'R_Orbicularis_1_Bind_07_Bnd_parentConstraint1', 'R_Orbicularis_1_Ctrl_05_Jnt', 'R_Orbicularis_1_Ctrl_02_Jnt_Offset_Grp', 'R_Orbicularis_1_02_Ctrl_Offset_Grp', 'R_Orbicularis_1_follicle_02_scaleConstraint1', 'R_Orbicularis_1_Bind_08_Bnd', 'R_Orbicularis_1_01_CtrlShape01', 'R_Orbicularis_1_05_Ctrl', 'R_Orbicularis_1_Bind_02_Bnd_scaleConstraint1', 'R_Orbicularis_1_Bind_06_Bnd', 'R_Orbicularis_1_Ctrl_03_Jnt_scaleConstraint1', 'R_Orbicularis_1_00_Ctrl', 'R_Orbicularis_1_follicle_06_scaleConstraint1', 'R_Orbicularis_1_Ctrl_05_Jnt_Offset_Grp', 'R_Orbicularis_1_07_Ctrl_tag', 'R_Orbicularis_1_ribbon_surfaceShape', 'R_Orbicularis_1_Ctrl_05_Jnt_parentConstraint1', 'R_Orbicularis_1_01_Ctrl_Offset_Grp', 'R_Orbicularis_1_ribbon_surfaceShapeOrig', 'R_Orbicularis_1_Bind_02_Bnd_parentConstraint1', 'R_Orbicularis_1_Ctrl_01_Jnt_Offset_Grp', 'R_Orbicularis_1_Ctrl_02_Jnt_scaleConstraint1', 'R_Orbicularis_1_Ctrl_03_Jnt_parentConstraint1', 'R_Orbicularis_1_Ctrl_08_Jnt_scaleConstraint1', 'R_Orbicularis_1_Ctrl_06_Jnt_parentConstraint1', 'R_Orbicularis_1_Bind_08_Bnd_parentConstraint1', 'R_Orbicularis_1_Ctrl_02_Jnt', 'R_Orbicularis_Ctrl_Grp', 'R_Orbicularis_1_Bind_06_Bnd_parentConstraint1', 'R_Orbicularis_1_follicle_Shape4']");
createNode transform -n "R_Orbicularis_Guide" -p "R_Orbicularis_Block";
	rename -uid "2654E0DF-4587-A436-7FEF-C9857708701B";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2026/scripts/Mutant_Tools/Icons/";
	setAttr ".t" -type "double3" -6.375 180.17467498779297 14.518593996980398 ;
	setAttr ".r" -type "double3" 90.000000000000028 0 0 ;
	setAttr ".s" -type "double3" -2.211 2.2108883787186708 2.2108883787186708 ;
createNode nurbsSurface -n "R_Orbicularis_GuideShape" -p "R_Orbicularis_Guide";
	rename -uid "13378EB0-4924-A338-9085-FB8A9590935F";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2026/scripts/Mutant_Tools/Icons/";
	setAttr -k off ".v";
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr ".dvu" 0;
	setAttr ".dvv" 0;
	setAttr ".cpr" 4;
	setAttr ".cps" 4;
	setAttr ".cc" -type "nurbsSurface" 
		3 3 0 2 no 
		6 0 0 0 1 1 1
		13 -2 -1 0 1 2 3 4 5 6 7 8 9 10
		
		44
		1.2738112890731406 -0.49999999999999989 -0.73068579105088027
		2.1192833890654152 -1.1438655227117016 5.3369407025191155e-16
		1.2185721957042128 -0.90420104652290689 0.90562346982934228
		0.020665757476648745 -0.50000000000000011 1.1594869816059932
		-0.8648229916634711 -0.5 0.92529138024561353
		-1.8310326605449998 -0.50000000000000011 0.395420774079216
		-1.0791665293845569 -0.49999999999999994 -0.83119081679435725
		-1.511240500779959e-16 -0.49999999999999994 -1.1081941875543881
		1.2738112890731406 -0.49999999999999989 -0.73068579105088027
		2.1192833890654152 -1.1438655227117016 5.3369407025191155e-16
		1.2185721957042128 -0.90420104652290689 0.90562346982934228
		1.2738112890731406 -0.1666666666666666 -0.73068579105088027
		2.1192833890654152 -1.1666629990490254 9.0376535896469238e-16
		1.2185721957042128 -0.57086771318957352 0.90562346982934228
		0.020665757476648745 -0.16666666666666671 1.1594869816059932
		-0.8648229916634711 -0.16666666666666669 0.92529138024561353
		-1.8310326605449998 -0.16666666666666652 0.39542077407921605
		-1.0791665293845569 -0.1666666666666666 -0.83119081679435725
		-1.511240500779959e-16 -0.1666666666666666 -1.1081941875543881
		1.2738112890731406 -0.1666666666666666 -0.73068579105088027
		2.1192833890654152 -1.1666629990490254 9.0376535896469238e-16
		1.2185721957042128 -0.57086771318957352 0.90562346982934228
		1.2738112890731406 0.16666666666666671 -0.73068579105088027
		2.1192833890654152 -0.83332966571569356 9.2417613895048157e-16
		1.2185721957042128 -0.23753437985624018 0.90562346982934228
		0.020665757476648745 0.1666666666666666 1.1594869816059932
		-0.8648229916634711 0.16666666666666663 0.92529138024561353
		-1.8310326605449998 0.1666666666666668 0.39542077407921605
		-1.0791665293845569 0.16666666666666671 -0.83119081679435725
		-1.511240500779959e-16 0.16666666666666671 -1.1081941875543881
		1.2738112890731406 0.16666666666666671 -0.73068579105088027
		2.1192833890654152 -0.83332966571569356 9.2417613895048157e-16
		1.2185721957042128 -0.23753437985624018 0.90562346982934228
		1.2738112890731406 0.5 -0.73068579105088027
		2.1192833890654152 -0.49999633238236019 9.4458691893627076e-16
		1.2185721957042128 0.095798953477093163 0.90562346982934228
		0.020665757476648745 0.49999999999999994 1.1594869816059932
		-0.8648229916634711 0.49999999999999994 0.92529138024561353
		-1.8310326605449998 0.49999999999999989 0.39542077407921611
		-1.0791665293845569 0.5 -0.83119081679435725
		-1.511240500779959e-16 0.50000000000000011 -1.1081941875543881
		1.2738112890731406 0.5 -0.73068579105088027
		2.1192833890654152 -0.49999633238236019 9.4458691893627076e-16
		1.2185721957042128 0.095798953477093163 0.90562346982934228
		
		;
	setAttr ".nufa" 4.5;
	setAttr ".nvfa" 4.5;
createNode dagContainer -n "Mouth_Block" -p "Face";
	rename -uid "4A22A929-4C4C-7E17-7126-0DAF122FBF67";
	addAttr -ci true -sn "nts" -ln "notes" -dt "string";
	setAttr ".isc" yes;
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2026/scripts/Mutant_Tools/Icons/MouthGames.png";
	setAttr ".ctor" -type "string" "rodri";
	setAttr ".cdat" -type "string" "2025/12/06 12:43:45";
	setAttr -l on -k off ".v";
	setAttr -l on -k off ".tx";
	setAttr -l on -k off ".ty";
	setAttr -l on -k off ".tz";
	setAttr -l on -k off ".rx";
	setAttr -l on -k off ".ry";
	setAttr -l on -k off ".rz";
	setAttr -l on -k off ".sx";
	setAttr -l on -k off ".sy";
	setAttr -l on -k off ".sz";
	setAttr ".nts" -type "string" (
		"['R_Mid_01_Mouth_Dw_Jnt_Offset_Grp', 'L_Mid_03_Mouth_Dw_Tweek_Jnt_scaleConstraint1', 'L_Mouth_Dw_Ctrl_tag', 'Mouth_Up_UpVector_4_DecomposeMatrix', 'R_Mid_01_Mouth_Up_Tweek_Ctrl_tag', 'Mouth_Up_Up_UpWireGroupParts', 'R_Mouth_Up_CtrlShape', 'L_Mouth_Up_Tweek_CtrlShape', 'Mouth_Up_UpVector_7_DecomposeMatrix', 'Mouth_Up_VectorUp_L_Loc', 'R_Mid_03_Mouth_Dw_Tweek_Ctrl_Offset_Grp_parentConstraint1', 'L_Mid_01_Mouth_Dw_Ctrl_tag', 'Mouth_Up_UpVector_R_Mid_02__POCI', 'R_Mid_02_Mouth_Up_Tweek_Ctrl_tag', 'R_Mid_02_Mouth_Up_Tweek_Jnt', 'R_Mid_01_Mouth_Dw_Ctrl_Offset_Grp_parentConstraint1', 'Mid_Mouth_Dw_Tweek_Ctrl_Offset_Grp', 'Mid_Mouth_Dw_Ctrl_tag', 'L_Mouth_Dw_Puller_Loc_parentConstraint1', 'R_Mid_02_Mouth_Up_Tweek_Ctrl_Offset_Grp', 'Mouth_Dw_VectorUp_R_Mid_02_Loc', 'Mouth_Up_Tweeks_Ctrl_Grp', 'L_Mouth_Dw_Jnt', 'Mouth_Dw_UpVector_8_DecomposeMatrix', 'L_Mid_02_Mouth_Up_Jnt_parentConstraint1', 'Mouth_Dw_0_TangentMatrix', 'Mouth_Dw_L_Mid_03__POCI', 'Mouth_Up_WireGroupParts', 'bindPose36', 'R_Mouth_Up_Tweek_Jnt_Offset_Grp', 'skinCluster40GroupId', 'Mouth_Up_Main_Ctrl_Auto_Grp', 'Mouth_Dw_WireGroupParts', 'Mouth_Ctrl_Grp_scaleConstraint1', 'L_Mid_03_Mouth_Up_Tweek_Jnt_parentConstraint1', 'Mouth_Up_L_Mid_01_Loc', 'R_Mid_01_Mouth_Up_Tweek_Jnt_Offset_Grp', 'Mouth_Dw_UpVector_5_DecomposeMatrix', 'skinCluster39GroupParts', 'L_Mid_03_Mouth_Up_Tweek_Jnt_scaleConstraint1', 'Mouth_Dw_L_Mid_02__POCI', 'L_Mid_02_Mouth_Up_Tweek_Bnd', 'Mid_Mouth_Dw_Jnt_Offset_Grp', 'Mouth_Up_0_DecomposeMatrix', 'L_Mouth_Sub_Ctrl_Offset_Grp', 'L_Mid_02_Mouth_Dw_Jnt_parentConstraint1', 'Mouth_Up_UpVector_Mid__POCI', 'Mouth_TopJaw_Loc_parentConstraint1', 'L_Mid_02_Mouth_Up_Tweek_Bnd_parentConstraint1', 'Mouth_Up_1_DecomposeMatrix', 'Mouth_Up_Up_UpWireGroupId', 'R_Mid_01_Mouth_Dw_Tweek_Jnt_Offset_Grp', 'Mid_Mouth_Up_Tweek_Ctrl_tag', 'unitConversion433', 'R_Mid_01_Mouth_Up_Tweek_Ctrl', 'Mid_Mouth_Dw_Tweek_Jnt_parentConstraint1', 'R_Mid_02_Mouth_Up_Tweek_CtrlShape', 'R_Mouth_Up_Tweek_Jnt_scaleConstraint1', 'Mid_Mouth_Dw_Tweek_Jnt_Offset_Grp', 'R_Mid_01_Mouth_Dw_Tweek_Bnd', 'R_Mouth_Up_Ctrl_Offset_Grp_parentConstraint1', 'R_Mouth_Up_Jnt_parentConstraint1', 'Mouth_Up_UpVector_R_Mid_01__POCI', 'Mouth_Dw_VectorUp_L_LocShape', 'L_Mouth_Dw_Tweek_Jnt_parentConstraint1', 'Mouth_Up_Main_Ctrl_Auto_Grp_parentConstraint1', 'L_Mid_01_Mouth_Up_Ctrl_tag', 'L_Mouth_Main_Loc_Root_Grp', 'R_Mouth_Dw_Puller_Loc_parentConstraint1', 'R_Mid_03_Mouth_Up_Tweek_Bnd_scaleConstraint1', 'L_Mid_01_Mouth_Dw_Tweek_Jnt_parentConstraint1', 'Mouth_Dw_UpVector_R_Mid_01__POCI', 'L_Mouth_Dw_Ctrl_Offset_Grp', 'R_Mid_01_Mouth_Dw_Tweek_Ctrl_tag', 'R_Mid_02_Mouth_Up_Tweek_Ctrl_Offset_Grp_parentConstraint1', 'R_Mouth_Dw_Tweek_CtrlShape', 'R_Mouth_Dw_Tweek_Jnt_Offset_Grp', 'R_Mouth_Dw_Tweek_Bnd', 'L_Mid_02_Mouth_Up_Tweek_Jnt_Offset_Grp', 'Mouth_Dw_Main_CtrlCenterRotateLips_Grp', 'Mouth_Dw_R_Mid_03__POCI', 'Mouth_Centerlips_Ctrl', 'Mid_Mouth_Up_Tweek_Jnt_parentConstraint1', 'Mouth_Up_UpVector_L__POCI', 'L_Mouth_Up_Puller_Loc_parentConstraint1', 'Mouth_Dw_Main_CtrlCenterRotateOffset_Grp', 'Mouth_Up_UpVector_4_TangentMatrix', 'R_Mid_01_Mouth_Dw_Ctrl_Offset_Grp', 'Mouth_Dw_L_Loc', 'R_Mid_02_Mouth_Up_Ctrl_tag', 'Mouth_Up_Mid__POCI', 'Mouth_Up_VectorUp_L_LocShape', 'R_Mouth_Dw_Tweek_Jnt_scaleConstraint1', 'Mouth_Center_Grp', 'Mid_Mouth_Dw_CtrlShape', 'L_Mid_01_Mouth_Dw_Jnt_Offset_Grp', 'L_Mid_01_Mouth_Up_Tweek_Jnt', 'Mouth_Dw_L_LocShape', 'R_Mid_03_Mouth_Up_Tweek_Ctrl_tag', 'L_Mouth_Dw_Jnt_scaleConstraint1', 'R_Mouth_Main_Loc_Root_Grp', 'Mouth_Up_Jnt_Grp', 'R_Mid_02_Mouth_Up_CtrlShape', 'L_Mid_01_Mouth_Dw_Tweek_Bnd_parentConstraint1', 'R_Mid_01_Mouth_Dw_Tweek_Ctrl', 'R_Mid_01_Mouth_Up_Ctrl', 'L_Mouth_Main_Ctrl_Root_Grp_parentConstraint1', 'L_Mid_03_Mouth_Up_Tweek_Ctrl_Offset_Grp_parentConstraint1', 'L_Mouth_Up_Jnt', 'L_Mouth_Up_Tweek_Ctrl_Offset_Grp', 'Mouth_Up_VectorUp_L_Mid_01_Loc', 'Mouth_Up_L_LocShape', 'Mouth_Dw_R__POCI', 'L_Mid_01_Mouth_Dw_Tweek_Bnd_scaleConstraint1', 'Mouth_Up_UpVector_R_Mid_03__POCI', 'R_Mid_02_Mouth_Up_Tweek_Jnt_scaleConstraint1', 'Mouth_Dw_UpVector_L_Mid_01__POCI', 'L_Mid_01_Mouth_Up_Jnt_parentConstraint1', 'Mouth_Dw_UpVector_2_DecomposeMatrix', 'Mouth_Up_R_Mid_03_LocShape', 'Mouth_Up_UpVector_6_DecomposeMatrix', 'R_Mid_03_Mouth_Up_Tweek_Bnd', 'Mouth_Dw_UpVector_R_Mid_03__POCI', 'Mouth_Up_Main_Loc_Auto_Grp', 'Mouth_Dw_Main_Ctrl_tag', 'Mouth_Up_UpVector_8_TangentMatrix', 'R_Mid_02_Mouth_Dw_Tweek_Jnt_scaleConstraint1', 'Mouth_Up_R_Mid_01_LocShape', 'R_Mid_01_Mouth_Dw_CtrlShape', 'Mouth_Dw_R_Mid_01_Loc', 'Mouth_Center_Ctrl_Offset_Grp', 'L_Mouth_Up_Tweek_Bnd_parentConstraint1', 'Mouth_Dw_UpVector_3_TangentMatrix', 'L_Mid_03_Mouth_Up_Tweek_CtrlShape', 'Mouth_Jaw_Ctrl_Offset_Grp', 'Mouth_Dw_Mid__POCI', 'Mouth_Up_8_DecomposeMatrix', 'R_Mid_02_Mouth_Dw_Ctrl_Offset_GrpMirror_Grp', 'L_Mouth_Up_Tweek_Jnt_scaleConstraint1', 'L_Mouth_Dw_Puller_LocShape', 'L_Mid_03_Mouth_Up_Tweek_Ctrl_tag', 'Mouth_jaw_lessThan', 'Mouth_Up_VectorUp_L_Mid_03_Loc', 'L_Mid_02_Mouth_Dw_Tweek_Jnt_scaleConstraint1', 'Mouth_Up_UpVector_5_TangentMatrix', 'Mouth_Dw_WireDriver_CrvBaseWire1', 'Mouth_Dw_VectorUp_L_Loc', 'Mouth_Dw_R_Loc', 'Mouth_Dw_VectorUp_R_LocShape', 'Mouth_Up_VectorUp_L_Mid_03_LocShape', 'Mouth_Up_UpVector_3_DecomposeMatrix', 'R_Mouth_Up_Tweek_Ctrl_tag', 'Mouth_Up_Main_Ctrl_tag', 'L_Mid_01_Mouth_Up_Tweek_CtrlShape', 'L_Mid_02_Mouth_Dw_Tweek_Ctrl', 'R_Mid_03_Mouth_Up_Tweek_Ctrl', 'Mouth_Jaw_Bnd', 'L_Mouth_Dw_Tweek_Ctrl_Offset_Grp_parentConstraint1', 'Mouth_Dw_Up_UpWireGroupParts', 'R_Mid_03_Mouth_Up_Tweek_Bnd_parentConstraint1', 'R_Mouth_Sub_Ctrl_Offset_Grp', 'R_Mouth_Up_Ctrl_Offset_Grp', 'Mouth_Up_Mid_LocShape', 'Mouth_Dw_VectorUp_L_Mid_02_LocShape', 'Mouth_Up_VectorUp_L_Mid_01_LocShape', 'Mouth_Ctrl_Grp_parentConstraint1', 'Mouth_Dw_VectorUp_L_Mid_02_Loc', 'Mid_Mouth_Up_Tweek_Ctrl', 'Mouth_Dw_0_DecomposeMatrix', 'Mouth_Up_R_Mid_01_Loc', 'Mid_Mouth_Dw_Jnt_parentConstraint1', 'Mid_Mouth_Up_Tweek_Ctrl_Offset_Grp_parentConstraint1', 'Mouth_Dw_UpVector_L__POCI', 'L_Mouth_Main_Loc_Auto_Grp', 'R_Mid_03_Mouth_Dw_Tweek_Jnt', 'L_Mid_01_Mouth_Up_Tweek_Ctrl', 'Mouth_Up_2_TangentMatrix', 'R_Mouth_Sub_Ctrl', 'L_Mid_01_Mouth_Dw_Jnt_parentConstraint1', 'Mouth_Center_Ctrl', 'Mouth_Dw_Main_Ctrl_Root_Grp_parentConstraint1', 'Mouth_Dw_WireDriver_CrvBaseWire1Shape', 'skinCluster39', 'Mouth_Dw_UpVector_2_TangentMatrix', 'Mouth_Up_Vtx_Crv', 'skinCluster40GroupParts', 'Mouth_Up_Vtx_CrvShapeOrig', 'L_Mouth_Dw_Tweek_Ctrl', 'L_Mid_01_Mouth_Dw_Tweek_Jnt_scaleConstraint1', 'Mouth_Up_WireGroupId', 'L_Mouth_Dw_Jnt_Offset_Grp', 'L_Mouth_Dw_CtrlShape', 'L_Mid_03_Mouth_Dw_Tweek_Ctrl_Offset_Grp_parentConstraint1', 'R_Mouth_Up_Tweek_CtrlShape', 'L_Mid_02_Mouth_Up_Tweek_Jnt_parentConstraint1', 'R_Mid_02_Mouth_Up_Tweek_Ctrl', 'Mid_Mouth_Up_Tweek_Bnd_parentConstraint1', 'Mid_Mouth_Up_Ctrl_Offset_Grp', 'Mouth_Up_7_TangentMatrix', 'Mouth_Up_WireDriver_CrvBaseWire1Shape', 'Mouth_Up_3_TangentMatrix', 'R_Mouth_Main_Loc', 'Mid_Mouth_Dw_Tweek_Jnt', 'L_Mouth_Main_Loc', 'R_Mid_02_Mouth_Up_Ctrl_Offset_GrpMirror_Grp', 'Mid_Mouth_Up_Ctrl_Offset_Grp_parentConstraint2', 'Mouth_Up_UpVector_8_DecomposeMatrix', 'Mouth_Dw_Vtx_CrvShape', 'R_Mid_01_Mouth_Dw_Tweek_Ctrl_Offset_GrpMirror_Grp', 'R_Mouth_Up_Jnt', 'Mouth_Up_UpVector_0_DecomposeMatrix', 'R_Mouth_Up_Puller_LocShape', 'Mouth_Jaw_Bnd_scaleConstraint1', 'R_Mid_03_Mouth_Up_Tweek_Jnt_parentConstraint1', 'Mouth_Centerlips_Grp', 'L_Mouth_Dw_Tweek_Bnd_scaleConstraint1', 'Mouth_Up_R_Mid_02_Loc', 'Mid_Mouth_Dw_Ctrl', 'R_Mouth_Up_Tweek_Ctrl', 'L_Mid_03_Mouth_Up_Tweek_Bnd_parentConstraint1', 'R_Mouth_Dw_Jnt_scaleConstraint1', 'R_Mid_01_Mouth_Dw_Jnt_parentConstraint1', 'Mouth_Up_UpVector_L_Mid_02__POCI', 'L_Mouth_Up_Ctrl_Offset_Grp', 'Mouth_Dw_R_Mid_03_Loc', 'L_Mouth_Up_Tweek_Ctrl_Offset_Grp_parentConstraint1', 'Mouth_Up_UpVector_7_TangentMatrix', 'R_Mouth_Up_Jnt_Offset_Grp', 'L_Mid_02_Mouth_Dw_Tweek_CtrlShape', 'L_Mid_01_Mouth_Up_Tweek_Bnd_parentConstraint1', 'L_Mid_02_Mouth_Up_Jnt_Offset_Grp', 'L_Mouth_Up_Tweek_Jnt_Offset_Grp', 'R_Mid_01_Mouth_Up_Tweek_Ctrl_Offset_GrpMirror_Grp', 'Mouth_Dw_L_Mid_01_Loc', 'L_Mid_01_Mouth_Up_Tweek_Jnt_scaleConstraint1', 'Mouth_Up_L_Loc', 'R_Mouth_Dw_Tweek_Ctrl', 'L_Mouth_Main_LocShape', 'R_Mouth_Dw_Tweek_Ctrl_tag', 'L_Mid_02_Mouth_Dw_Tweek_Bnd_scaleConstraint1', 'Mouth_Up_1_TangentMatrix', 'Mouth_Dw_L__POCI', 'Mid_Mouth_Dw_Tweek_Ctrl', 'Mid_Mouth_Dw_Tweek_Ctrl_tag', 'Mouth_Dw_7_TangentMatrix', 'L_Mid_03_Mouth_Dw_Tweek_Ctrl_Offset_Grp', 'R_Mid_01_Mouth_Up_Tweek_Ctrl_Offset_Grp', 'R_Mid_02_Mouth_Dw_Ctrl_Offset_Grp', 'L_Mouth_Up_Tweek_Jnt', 'R_Mid_01_Mouth_Up_Ctrl_tag', 'L_Mid_02_Mouth_Dw_Tweek_Ctrl_Offset_Grp', 'R_Mid_03_Mouth_Dw_Tweek_Bnd_scaleConstraint1', 'L_Mid_02_Mouth_Dw_Ctrl_tag', 'Mid_Mouth_Dw_Tweek_Ctrl_Offset_Grp_parentConstraint1', 'Mouth_Dw_UpVector_1_TangentMatrix', 'Mouth_Dw_Up_UpWireGroupId', 'L_Mouth_Dw_Tweek_Jnt', 'R_Mid_02_Mouth_Up_Tweek_Jnt_parentConstraint1', 'Mouth_Dw_UpVector_Crv', 'Mouth_Up_Mid_Loc', 'R_Mid_01_Mouth_Dw_Ctrl_tag', 'Mouth_Up_Main_Ctrl_Root_Grp', 'Mouth_Up_8_TangentMatrix', 'Mid_Mouth_Dw_Tweek_Jnt_scaleConstraint1', 'R_Mouth_Main_LocShape', 'Mid_Mouth_Up_Tweek_Bnd', 'Mouth_Center_CtrlShape', 'Mouth_Dw_6_DecomposeMatrix', 'Mouth_Dw_R_Mid_01__POCI', 'L_Mid_02_Mouth_Up_Tweek_Ctrl_tag', 'L_Mid_01_Mouth_Dw_CtrlShape', 'Mouth_Up_L_Mid_03__POCI', 'R_Mid_01_Mouth_Dw_Tweek_CtrlShape', 'R_Mouth_Main_Ctrl_Root_Grp_parentConstraint1', 'L_Mouth_Up_Jnt_scaleConstraint1', 'Mid_Mouth_Up_Tweek_CtrlShape', 'Mouth_Dw_UpVector_6_TangentMatrix', 'Mouth_Dw_Main_Ctrl_Root_Grp', 'Mouth_Up_R_Mid_01__POCI', 'R_Mouth_Dw_Tweek_Jnt', 'L_Mouth_Up_Tweek_Ctrl_tag', 'Mouth_Up_Main_LocShape', 'Mid_Mouth_Up_Tweek_Ctrl_Offset_Grp', 'Mouth_Dw_VectorUp_L_Mid_03_LocShape', 'Mouth_Dw_4_TangentMatrix', 'R_Mid_02_Mouth_Dw_Tweek_Jnt_Offset_Grp', 'R_Mouth_Main_Ctrl_Auto_Grp', 'L_Mid_02_Mouth_Up_Ctrl', 'Mouth_Up_Ctrl_Grp', 'L_Mouth_Up_Puller_Loc', 'Mouth_Dw_VectorUp_L_Mid_01_Loc', 'Mouth_Dw_Vtx_Crv', 'R_Mid_01_Mouth_Dw_Tweek_Ctrl_Offset_Grp', 'L_Mouth_Main_Ctrl_Auto_Grp', 'Mouth_Up_4_DecomposeMatrix', 'L_Mid_03_Mouth_Dw_Tweek_Jnt', 'Mouth_Rig_Grp', 'Mouth_Up_UpVector_0_TangentMatrix', 'Mouth_Up_VectorUp_R_Mid_01_LocShape', 'R_Mouth_Up_Tweek_Jnt_parentConstraint1', 'L_Mid_01_Mouth_Dw_Tweek_Ctrl_Offset_Grp_parentConstraint1', 'Mouth_Dw_UpVector_R_Mid_02__POCI', 'Mouth_Jaw_Bnd_parentConstraint1', 'R_Mid_01_Mouth_Dw_Tweek_Jnt_parentConstraint1', 'Mouth_Up_4_TangentMatrix', 'L_Mouth_Up_Tweek_Jnt_parentConstraint1', 'L_Mouth_Up_Jnt_Offset_Grp', 'R_Mouth_Up_Tweek_Bnd_scaleConstraint1', 'Mid_Mouth_Up_Tweek_Jnt_scaleConstraint1', 'L_Mid_01_Mouth_Up_Ctrl_Offset_Grp_parentConstraint1', 'L_Mouth_Up_Ctrl', 'Mouth_Dw_WireDriver_Crv', 'R_Mid_03_Mouth_Dw_Tweek_Bnd_parentConstraint1', 'L_Mouth_Dw_Tweek_Ctrl_tag', 'R_Mouth_Up_Tweek_Ctrl_Offset_GrpMirror_Grp', 'Mouth_Up_L_Mid_02__POCI', 'L_Mid_03_Mouth_Up_Tweek_Bnd_scaleConstraint1', 'Mouth_Centerlips_Grp_Offset_Grp', 'Mouth_Up_L_Mid_03_LocShape', 'Mouth_Jaw_CtrlShape', 'R_Mouth_Main_Ctrl', 'Mouth_Up_VectorUp_R_Loc', 'Mouth_Dw_UpVector_3_DecomposeMatrix', 'R_Mid_01_Mouth_Up_Jnt_scaleConstraint1', 'L_Mid_03_Mouth_Dw_Tweek_Bnd', 'skinCluster39Set', 'R_Mouth_Dw_Tweek_Jnt_parentConstraint1', 'Mouth_Dw_5_DecomposeMatrix', 'R_Mouth_Main_Loc_Auto_Grp', 'Mouth_Dw_Main_Loc_Root_Grp', 'Mouth_Dw_UpVector_CrvShapeOrig', 'Mouth_Dw_VtxJnts_Grp', 'R_Mid_03_Mouth_Dw_Tweek_Ctrl_Offset_GrpMirror_Grp', 'Mouth_Dw_UpVector_CrvShape', 'Mouth_Dw_VectorUp_L_Mid_01_LocShape', 'R_Mouth_Up_Jnt_scaleConstraint1', 'R_Mouth_Dw_Tweek_Bnd_parentConstraint1', 'L_Mid_01_Mouth_Up_Tweek_Ctrl_Offset_Grp', 'R_Mid_02_Mouth_Up_Tweek_Jnt_Offset_Grp', 'Mouth_Dw_R_Mid_02__POCI', 'Mouth_Jaw_Ctrl_tag', 'R_Mid_02_Mouth_Up_Tweek_Bnd', 'Mouth_Dw_Mid_LocShape', 'Mid_Mouth_Up_Ctrl_tag', 'Mouth_Up_L_Mid_02_Loc', 'L_Mid_02_Mouth_Up_Tweek_Jnt_scaleConstraint1', 'R_Mid_02_Mouth_Up_Ctrl_Offset_Grp_parentConstraint1', 'Mouth_Dw_UpVector_4_DecomposeMatrix', 'R_Mid_02_Mouth_Dw_Tweek_CtrlShape', 'R_Mouth_Up_Tweek_Jnt', 'Mid_Mouth_Up_Tweek_Jnt_Offset_Grp', 'L_Mid_02_Mouth_Dw_Tweek_Jnt', 'Mouth_Dw_Up_UpWireSet', 'Mouth_Dw_WireDriver_CrvShape', 'L_Mid_02_Mouth_Dw_Tweek_Ctrl_Offset_Grp_parentConstraint1', 'Mid_Mouth_Up_Jnt_Offset_Grp', 'R_Mouth_Up_Tweek_Bnd', 'L_Mid_02_Mouth_Dw_Tweek_Bnd_parentConstraint1', 'Mid_Mouth_Dw_Tweek_Bnd_scaleConstraint1', 'Mouth_Up_UpVector_CrvShape', 'R_Mid_01_Mouth_Up_Tweek_Jnt_scaleConstraint1', 'Mouth_Dw_Mid_Loc', 'R_Mid_03_Mouth_Dw_Tweek_Bnd', 'skinCluster39GroupId', 'R_Mouth_Sub_Ctrl_tag', 'L_Mid_02_Mouth_Dw_Tweek_Jnt_parentConstraint1', 'Mouth_Up_7_DecomposeMatrix', 'R_Mouth_Main_Ctrl_Root_Grp', 'Mouth_Up_WireDriver_CrvBaseWire1', 'Mouth_Up_UpVector_L_Mid_01__POCI', 'Mouth_Up_UpVector_1_DecomposeMatrix', 'L_Mouth_Dw_Jnt_parentConstraint1', 'Mouth_Dw_UpVector_4_TangentMatrix', 'R_Mid_02_Mouth_Up_Ctrl', 'Mouth_Up_6_TangentMatrix', 'L_Mid_02_Mouth_Up_CtrlShape', 'R_Mid_01_Mouth_Up_Ctrl_Offset_GrpMirror_Grp', 'L_Mid_02_Mouth_Dw_CtrlShape', 'L_Mouth_Dw_Ctrl', 'Mouth_Dw_Main_CtrlCenterRotate_Grp', 'L_Mouth_Dw_Tweek_Ctrl_Offset_Grp', 'Mouth_Dw_Main_Ctrl_Auto_Grp', 'Mouth_Dw_VectorUp_L_Mid_03_Loc', 'Mouth_Up_VectorUp_R_Mid_03_Loc', 'L_Mouth_Up_Ctrl_tag', 'Mouth_Dw_Main_Loc', 'Mouth_Dw_VectorUp_R_Mid_02_LocShape', 'Mouth_Dw_R_Mid_02_Loc', 'Mouth_Dw_UpVector_0_TangentMatrix', 'R_Mid_02_Mouth_Dw_Ctrl', 'R_Mouth_Dw_Puller_Loc', 'R_Mouth_Dw_Tweek_Ctrl_Offset_GrpMirror_Grp', 'R_Mid_02_Mouth_Dw_Tweek_Ctrl', 'L_Mouth_Main_Ctrl', 'L_Mouth_Sub_CtrlShape', 'L_Mid_02_Mouth_Dw_Tweek_Bnd', 'Mouth_Up_R_Mid_03_Loc', 'L_Mouth_Dw_Tweek_Bnd', 'R_Mid_01_Mouth_Dw_Ctrl_Offset_GrpMirror_Grp', 'Mouth_Up_UpVector_CrvShapeOrig', 'L_Mid_02_Mouth_Dw_Ctrl', 'R_Mouth_Dw_Puller_LocShape', 'R_Mouth_Dw_Tweek_Ctrl_Offset_Grp_parentConstraint1', 'R_Mid_02_Mouth_Dw_Jnt_Offset_Grp', 'skinCluster40', 'R_Mid_03_Mouth_Dw_Tweek_Ctrl_Offset_Grp', 'Mid_Mouth_Up_Jnt', 'R_Mouth_Dw_Tweek_Bnd_scaleConstraint1', 'Mouth_Dw_Main_LocShape', 'R_Mid_02_Mouth_Up_Tweek_Ctrl_Offset_GrpMirror_Grp', 'R_Mid_03_Mouth_Dw_Tweek_CtrlShape', 'Mouth_Up_WireDriver_CrvShapeOrig', 'Mouth_Up_WireDriver_Crv', 'Mouth_Dw_1_TangentMatrix', 'R_Mid_02_Mouth_Dw_Ctrl_Offset_Grp_parentConstraint1', 'Mouth_Up_UpVector_5_DecomposeMatrix', 'R_Mouth_Dw_CtrlShape', 'Mouth_Up_Up_UpWireSet', 'R_Mid_03_Mouth_Up_Tweek_Jnt_scaleConstraint1', 'R_Mouth_Up_Ctrl_Offset_GrpMirror_Grp', 'L_Mouth_Up_Tweek_Bnd_scaleConstraint1', 'L_Mid_01_Mouth_Up_CtrlShape', 'R_Mid_01_Mouth_Dw_Tweek_Bnd_parentConstraint1', 'Mouth_Center_Grp_Offset_Grp', 'Mid_Mouth_Up_CtrlShape', 'L_Mid_02_Mouth_Up_Tweek_Ctrl_Offset_Grp', 'L_Mouth_Sub_Ctrl_tag', 'L_Mouth_Dw_Tweek_Bnd_parentConstraint1', 'L_Mouth_Up_Ctrl_Offset_Grp_parentConstraint1', 'R_Mid_03_Mouth_Up_Tweek_Ctrl_Offset_Grp_parentConstraint1', 'Mouth_Dw_VectorUp_R_Mid_03_Loc', 'Mouth_Dw_VectorUp_R_Mid_03_LocShape', 'R_Mouth_Main_Ctrl_Root_GrpMirror_Grp', 'L_Mid_03_Mouth_Up_Tweek_Bnd', 'Mouth_Centerlips_Ctrl_tag', 'Mouth_Dw_8_DecomposeMatrix', 'L_Mouth_Up_CtrlShape', 'Mouth_Up_VectorUp_L_Mid_02_LocShape', 'Mouth_Up_WireDriver_CrvBaseWire', 'Mouth_Up_L_Mid_01__POCI', 'R_Mid_01_Mouth_Dw_Ctrl', 'L_Mid_01_Mouth_Up_Jnt_scaleConstraint1', 'Mouth_Dw_UpVector_7_DecomposeMatrix', 'Mouth_Up_R_LocShape', 'L_Mid_02_Mouth_Up_Tweek_Ctrl', 'R_Mid_02_Mouth_Up_Jnt_scaleConstraint1', 'Mouth_Centerlips_CtrlShape', 'Mouth_Up_R_Mid_02__POCI', 'R_Mid_03_Mouth_Up_Tweek_CtrlShape', 'L_Mouth_Up_Tweek_Bnd', 'R_Mid_02_Mouth_Up_Jnt_parentConstraint1', 'pairBlend2', 'R_Mid_01_Mouth_Up_Ctrl_Offset_Grp', 'Mouth_Up_VectorUp_R_Mid_02_Loc', 'Mouth_Up_Main_Ctrl_Root_Grp_parentConstraint1', 'Mouth_Ctrl_Grp', 'Mouth_Dw_WireDriver_CrvBaseWire', 'Mouth_Up_WireDriver_CrvShape', 'Mouth_Up_R_Mid_02_LocShape', 'L_Mid_01_Mouth_Up_Tweek_Jnt_Offset_Grp', 'Mid_Mouth_Dw_Jnt_scaleConstraint1', 'R_Mouth_Up_Tweek_Ctrl_Offset_Grp', 'Mouth_Dw_UpVector_6_DecomposeMatrix', 'Mouth_Up_WireSet', 'R_Mid_03_Mouth_Up_Tweek_Ctrl_Offset_Grp', 'Mouth_Dw_Wire', 'Mouth_Up_L_Mid_03_Loc', 'Mouth_Up_VectorUp_Mid_Loc', 'R_Mid_02_Mouth_Up_Jnt_Offset_Grp', 'L_Mid_02_Mouth_Up_Ctrl_Offset_Grp', 'Mid_Mouth_Up_Tweek_Bnd_scaleConstraint1', 'Mouth_Up_Up_UpWire', 'R_Mid_02_Mouth_Dw_Jnt', 'Mouth_Up_Main_CtrlCenterRotateLipsOffset_Grp', 'L_Mid_01_Mouth_Dw_Ctrl_Offset_Grp_parentConstraint1', 'Mouth_Dw_UpVector_7_TangentMatrix', 'Mouth_Dw_WireDriver_CrvShapeOrig', 'L_Mid_03_Mouth_Up_Tweek_Ctrl', 'Mouth_Up_UpVector_2_DecomposeMatrix', 'L_Mid_01_Mouth_Dw_Jnt_scaleConstraint1', 'R_Mouth_Main_Ctrl_tag', 'Mouth_Dw_UpVector_0_DecomposeMatrix', 'Mouth_TopJaw_Loc', 'R_Mid_01_Mouth_Up_Tweek_Bnd', 'R_Mid_01_Mouth_Up_Tweek_Ctrl_Offset_Grp_parentConstraint1', 'L_Mid_02_Mouth_Up_Ctrl_Offset_Grp_parentConstraint1', 'R_Mid_01_Mouth_Dw_Tweek_Bnd_scaleConstraint1', 'Mouth_Dw_2_TangentMatrix', 'Mouth_Dw_Main_CtrlCenterRotateLipsOffset_Grp', 'Mouth_Dw_L_Mid_03_Loc', 'R_Mouth_Up_Puller_Loc', 'Mid_Mouth_Up_Jnt_parentConstraint1', 'Mouth_Up_VtxJnts_Grp', 'R_Mid_02_Mouth_Dw_Ctrl_tag', 'R_Mid_03_Mouth_Up_Tweek_Jnt', 'Mouth_Dw_UpVector_1_DecomposeMatrix', 'R_Mid_02_Mouth_Dw_Jnt_parentConstraint1', 'skinCluster40Set', 'R_Mid_02_Mouth_Dw_Tweek_Jnt', 'Mid_Mouth_Dw_Ctrl_Offset_Grp', 'L_Mid_03_Mouth_Dw_Tweek_Ctrl', 'R_Mid_02_Mouth_Dw_Tweek_Ctrl_Offset_GrpMirror_Grp', 'R_Mouth_Main_Ctrl_Root_Grp_parentConstraint1_reverse', 'L_Mid_02_Mouth_Dw_Tweek_Ctrl_tag', 'L_Mid_01_Mouth_Up_Tweek_Ctrl_Offset_Grp_parentConstraint1', 'Mouth_Dw_Main_CtrlShape', 'L_Mouth_Up_Tweek_Ctrl', 'Mouth_Up_VectorUp_R_Mid_02_LocShape', 'Mouth_Up_R_Mid_03__POCI', 'Mid_Mouth_Dw_Tweek_CtrlShape', 'Mouth_Up_Main_Loc', 'Mouth_Up_R__POCI', 'Mouth_Up_L_Mid_02_LocShape', 'Mouth_Dw_L_Mid_03_LocShape', 'L_Mouth_Main_CtrlShape', 'Mouth_Up_6_DecomposeMatrix', 'R_Mouth_Up_Tweek_Bnd_parentConstraint1', 'Mouth_Up_Main_CtrlShape', 'Mouth_Dw_8_TangentMatrix', 'L_Mid_02_Mouth_Up_Jnt_scaleConstraint1', 'L_Mid_01_Mouth_Up_Ctrl', 'L_Mid_02_Mouth_Up_Ctrl_tag', 'L_Mid_02_Mouth_Up_Jnt', 'Mouth_Dw_UpVector_L_Mid_03__POCI', 'L_Mid_03_Mouth_Dw_Tweek_Jnt_parentConstraint1', 'Mouth_Dw_VectorUp_R_Loc', 'Mouth_TopJaw_LocShape', 'R_Mid_02_Mouth_Dw_Tweek_Bnd_scaleConstraint1', 'bindPose35', 'Mouth_Dw_5_TangentMatrix', 'L_Mouth_Up_Jnt_parentConstraint1', 'R_Mouth_Dw_Jnt_parentConstraint1', 'L_Mouth_Dw_Puller_Loc', 'Mouth_Dw_Tweeks_Ctrl_Grp', 'R_Mid_02_Mouth_Dw_Tweek_Ctrl_tag', 'R_Mouth_Dw_Ctrl_Offset_Grp_parentConstraint1', 'L_Mid_01_Mouth_Dw_Ctrl_Offset_Grp', 'Mouth_Up_VectorUp_R_Mid_03_LocShape', 'L_Mouth_Sub_Ctrl', 'Mouth_Dw_6_TangentMatrix', 'Mouth_Up_UpVector_1_TangentMatrix', 'R_Mouth_Sub_CtrlShape', 'Mouth_Up_2_DecomposeMatrix', 'L_Mid_01_Mouth_Dw_Tweek_CtrlShape', 'Mouth_Up_5_TangentMatrix', 'Mouth_Up_0_TangentMatrix', 'L_Mid_01_Mouth_Dw_Ctrl', 'L_Mid_01_Mouth_Up_Tweek_Jnt_parentConstraint1', 'R_Mid_01_Mouth_Up_Tweek_Jnt', 'R_Mid_02_Mouth_Up_Jnt', 'L_Mid_02_Mouth_Dw_Ctrl_Offset_Grp_parentConstraint1', 'Mouth_Up_UpVector_3_TangentMatrix', 'Mouth_Dw_VectorUp_R_Mid_01_Loc', 'Mouth_Up_L__POCI', 'R_Mid_01_Mouth_Up_Tweek_Jnt_parentConstraint1', 'Mouth_Dw_VectorUp_Mid_LocShape', 'pairBlend1', 'Mouth_Dw_WireGroupId', 'L_Mid_01_Mouth_Dw_Tweek_Ctrl_tag', 'Mid_Mouth_Dw_Jnt', 'L_Mouth_Dw_Ctrl_Offset_Grp_parentConstraint1', 'R_Mid_01_Mouth_Up_CtrlShape', 'Mouth_Dw_3_DecomposeMatrix', 'Mouth_Dw_L_Mid_01__POCI', 'R_Mouth_Dw_Jnt_Offset_Grp', 'Mouth_Dw_L_Mid_02_Loc', 'R_Mid_03_Mouth_Up_Tweek_Ctrl_Offset_GrpMirror_Grp', 'Mouth_Up_3_DecomposeMatrix', 'Mouth_Up_VectorUp_R_LocShape', 'Mouth_Up_UpVector_Crv', 'L_Mouth_Dw_Tweek_CtrlShape', 'L_Mid_01_Mouth_Dw_Tweek_Bnd', 'Mouth_Dw_UpVector_Mid__POCI', 'R_Mid_03_Mouth_Dw_Tweek_Jnt_parentConstraint1', 'R_Mid_02_Mouth_Dw_Tweek_Ctrl_Offset_Grp', 'Mid_Mouth_Dw_Ctrl_Offset_Grp_parentConstraint2', 'Mouth_Up_R_Loc', 'Mouth_Up_Vtx_CrvShape', 'Mouth_Up_UpVector_R__POCI', 'L_Mouth_Main_Ctrl_tag', 'R_Mouth_Dw_Tweek_Ctrl_Offset_Grp', 'Mouth_Up_L_Mid_01_LocShape', 'R_Mid_01_Mouth_Up_Jnt', 'R_Mid_02_Mouth_Dw_Tweek_Jnt_parentConstraint1', 'Mid_Mouth_Up_Jnt_scaleConstraint1', 'R_Mid_02_Mouth_Dw_Jnt_scaleConstraint1', 'Mid_Mouth_Dw_Tweek_Bnd_parentConstraint1', 'Mouth_Dw_L_Mid_02_LocShape', 'L_Mid_01_Mouth_Dw_Jnt', 'R_Mouth_Dw_Jnt', 'R_Mid_03_Mouth_Dw_Tweek_Ctrl_tag', 'R_Mid_02_Mouth_Up_Tweek_Bnd_scaleConstraint1', 'Mouth_Dw_UpVector_8_TangentMatrix', 'Mouth_Dw_WireSet', 'Mouth_Dw_FollowLocators_Grp', 'Mouth_Dw_R_LocShape', 'Mid_Mouth_Up_Tweek_Jnt', 'R_Mid_03_Mouth_Dw_Tweek_Ctrl', 'Mouth_Up_UpVector_2_TangentMatrix', 'Mouth_Dw_R_Mid_01_LocShape', 'Mouth_Dw_Vtx_CrvShapeOrig', 'L_Mid_01_Mouth_Up_Jnt', 'L_Mid_02_Mouth_Dw_Jnt_scaleConstraint1', 'R_Mouth_Dw_Ctrl_Offset_GrpMirror_Grp', 'R_Mid_03_Mouth_Dw_Tweek_Jnt_Offset_Grp', 'L_Mid_03_Mouth_Dw_Tweek_Bnd_parentConstraint1', 'Mid_Mouth_Dw_Tweek_Bnd', 'R_Mid_02_Mouth_Up_Ctrl_Offset_Grp', 'R_Mouth_Dw_Ctrl_Offset_Grp', 'L_Mid_01_Mouth_Dw_Tweek_Ctrl_Offset_Grp', 'R_Mouth_Dw_Ctrl_tag', 'Mouth_Up_WireDriver_CrvBaseWireShape', 'L_Mid_03_Mouth_Up_Tweek_Jnt_Offset_Grp', 'R_Mid_01_Mouth_Dw_Jnt_scaleConstraint1', 'L_Mid_01_Mouth_Up_Tweek_Bnd', 'R_Mid_01_Mouth_Dw_Tweek_Jnt_scaleConstraint1', 'L_Mid_03_Mouth_Dw_Tweek_CtrlShape', 'R_Mid_02_Mouth_Dw_Tweek_Bnd', 'L_Mid_03_Mouth_Up_Tweek_Jnt', 'R_Mid_01_Mouth_Dw_Tweek_Ctrl_Offset_Grp_parentConstraint1', 'R_Mid_02_Mouth_Dw_CtrlShape', 'Mouth_Dw_7_DecomposeMatrix', 'L_Mid_01_Mouth_Up_Ctrl_Offset_Grp', 'Mouth_Dw_VectorUp_Mid_Loc', 'Mouth_Up_VectorUp_Mid_LocShape', 'L_Mouth_Dw_Tweek_Jnt_scaleConstraint1', 'R_Mid_01_Mouth_Up_Tweek_Bnd_scaleConstraint1', 'L_Mid_02_Mouth_Up_Tweek_Jnt', 'Mouth_Dw_Main_Ctrl', 'Mouth_Dw_Up_UpWire', 'R_Mid_01_Mouth_Up_Jnt_parentConstraint1', 'L_Mouth_Main_Ctrl_Root_Grp_parentConstraint1_reverse', 'L_Mid_01_Mouth_Dw_Tweek_Jnt_Offset_Grp', 'Mouth_Dw_R_Mid_02_LocShape', 'L_Mid_03_Mouth_Dw_Tweek_Ctrl_tag', 'Mouth_Centerlips_Ctrl_Offset_Grp', 'R_Mid_01_Mouth_Up_Tweek_CtrlShape', 'Mouth_Up_Main_CtrlCenterRotateLips_Grp', 'L_Mid_01_Mouth_Dw_Tweek_Ctrl', 'L_Mid_03_Mouth_Dw_Tweek_Bnd_scaleConstraint1', 'Mouth_Up_UpVector_6_TangentMatrix', 'Mouth_Up_VectorUp_R_Mid_01_Loc', 'R_Mouth_Up_Tweek_Ctrl_Offset_Grp_parentConstraint1', 'Mouth_Up_Wire', 'Mouth_Dw_UpVector_R__POCI', 'R_Mid_03_Mouth_Dw_Tweek_Jnt_scaleConstraint1', 'L_Mouth_Up_Puller_LocShape', 'Mouth_Dw_4_DecomposeMatrix', 'L_Mouth_Main_Ctrl_Root_Grp', 'R_Mouth_Main_CtrlShape', 'Mouth_Up_5_DecomposeMatrix', 'L_Mid_03_Mouth_Dw_Tweek_Jnt_Offset_Grp', 'R_Mid_03_Mouth_Up_Tweek_Jnt_Offset_Grp', 'Mouth_Dw_2_DecomposeMatrix', 'L_Mid_01_Mouth_Up_Tweek_Bnd_scaleConstraint1', 'Mouth_Up_FollowLocators_Grp', 'R_Mouth_Up_Puller_Loc_parentConstraint1', 'R_Mouth_Up_Ctrl_tag', 'R_Mid_01_Mouth_Dw_Jnt', 'Mid_Mouth_Dw_Ctrl_Offset_Grp_parentConstraint1', 'Mouth_Up_Main_Ctrl', 'Mouth_Jaw_Ctrl', 'Mouth_Dw_WireDriver_CrvBaseWireShape', 'R_Mouth_Dw_Ctrl', 'L_Mid_02_Mouth_Dw_Tweek_Jnt_Offset_Grp', 'Mouth_Dw_UpVector_L_Mid_02__POCI', 'Mouth_jaw_reverse', 'Mouth_Dw_3_TangentMatrix', 'Mouth_Dw_UpVector_5_TangentMatrix', 'R_Mouth_Main_Loc_Root_GrpMirror_Grp', 'Mouth_Center_Ctrl_tag', 'Mouth_Dw_R_Mid_03_LocShape', 'Mid_Mouth_Up_Ctrl', 'L_Mid_02_Mouth_Dw_Jnt', 'Mid_Mouth_Up_Ctrl_Offset_Grp_parentConstraint1', 'L_Mid_02_Mouth_Up_Tweek_Bnd_scaleConstraint1', 'Mouth_Dw_Ctrl_Grp', 'L_Mid_03_Mouth_Up_Tweek_Ctrl_Offset_Grp', 'Mouth_Dw_1_DecomposeMatrix', 'L_Mid_02_Mouth_Dw_Jnt_Offset_Grp', 'Mouth_Up_UpVector_L_Mid_03__POCI', 'L_Mid_01_Mouth_Up_Tweek_Ctrl_tag', 'R_Mid_01_Mouth_Dw_Tweek_Jnt', 'L_Mid_01_Mouth_Dw_Tweek_Jnt', 'R_Mid_01_Mouth_Up_Ctrl_Offset_Grp_parentConstraint1', 'Mouth_Up_Main_Loc_Root_Grp', 'R_Mid_02_Mouth_Up_Tweek_Bnd_parentConstraint1', 'L_Mid_02_Mouth_Up_Tweek_Ctrl_Offset_Grp_parentConstraint1', 'L_Mouth_Dw_Tweek_Jnt_Offset_Grp', 'Mouth_Up_VectorUp_L_Mid_02_Loc', 'L_Mid_02_Mouth_Dw_Ctrl_Offset_Grp', 'R_Mid_01_Mouth_Up_Jnt_Offset_Grp', 'Mouth_Dw_Main_Loc_Auto_Grp', 'L_Mid_02_Mouth_Up_Tweek_CtrlShape', 'Mouth_Dw_L_Mid_01_LocShape', 'L_Mid_01_Mouth_Up_Jnt_Offset_Grp', 'Mouth_jaw_blendColors', 'R_Mid_02_Mouth_Dw_Tweek_Bnd_parentConstraint1', 'Mouth_Dw_VectorUp_R_Mid_01_LocShape', 'R_Mouth_Up_Ctrl', 'Mouth_Dw_Jnt_Grp', 'R_Mid_02_Mouth_Dw_Tweek_Ctrl_Offset_Grp_parentConstraint1', 'R_Mid_01_Mouth_Up_Tweek_Bnd_parentConstraint1']");
createNode joint -n "L_Mouth_Orient_Guide_Guide" -p "Mouth_Block";
	rename -uid "82E65958-4B37-B75D-EA68-79838DA14A3D";
	addAttr -ci true -sn "Helper" -ln "Helper" -min 0 -max 1 -en "Hide:Show" -at "enum";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2026/scripts/Mutant_Tools/Icons/";
	setAttr ".t" -type "double3" 6.0788135528564453 167.54533386230469 15.43282413482666 ;
	setAttr ".r" -type "double3" 0 35.194722365872437 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr -cb on ".Helper" 1;
createNode nurbsCurve -n "L_Mouth_Orient_Guide_Guide_CtrlShape" -p "L_Mouth_Orient_Guide_Guide";
	rename -uid "9D765415-4B6B-5714-1A55-689B88B01A5C";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2026/scripts/Mutant_Tools/Icons/";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".hpb" yes;
	setAttr ".ovc" 14;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 9 0 no 3
		10 0 1 2 3 4 5 6 7 8 9
		10
		1.3977299999999999e-05 -0.5 0.25
		1.3977299999999999e-05 0.94513100000000005 0.25591599999999998
		1.3977299999999999e-05 0.739653 0.50644299999999998
		1.3977299999999999e-05 0.99017999999999995 0.93915099999999996
		1.37985e-05 2.299302 3.8742999999999997e-07
		1.3977299999999999e-05 0.99018099999999998 -0.93915099999999996
		1.3977299999999999e-05 0.739653 -0.50644199999999995
		7.1674600000000002e-06 0.94513100000000005 -0.25322099999999997
		1.3977299999999999e-05 -0.5 -0.25
		1.3977299999999999e-05 -0.5 0.25
		;
createNode nurbsCurve -n "L_Mouth_Orient_Guide_Guide_Ctrl_CtrlShape" -p "L_Mouth_Orient_Guide_Guide";
	rename -uid "A599CA4A-4CD9-DCC1-E975-41ABF0D01217";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2026/scripts/Mutant_Tools/Icons/";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".hpb" yes;
	setAttr ".ovc" 18;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 101 0 no 3
		102 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27
		 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54
		 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81
		 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99 100 101
		102
		0 0.59420899999999999 0
		-3.0751100000000001e-09 0.58518199999999998 0.103183
		-6.0567700000000004e-09 0.55837400000000004 0.203232
		-8.8544099999999994e-09 0.51460099999999998 0.29710500000000001
		-1.1383e-08 0.45519100000000001 0.38195099999999998
		-1.3565700000000001e-08 0.38195000000000001 0.45519100000000001
		-1.5336300000000002e-08 0.29710500000000001 0.51460099999999998
		-1.6640900000000001e-08 0.203232 0.55837400000000004
		-1.7439800000000002e-08 0.103183 0.58518199999999998
		-1.7708799999999999e-08 0 0.59421000000000002
		-1.7439800000000002e-08 -0.103183 0.58518199999999998
		-1.6640900000000001e-08 -0.203232 0.55837400000000004
		-1.5336300000000002e-08 -0.29710500000000001 0.51460099999999998
		-1.3565700000000001e-08 -0.38195000000000001 0.45519100000000001
		-1.1383e-08 -0.45519100000000001 0.38195099999999998
		-8.8544099999999994e-09 -0.51460099999999998 0.29710500000000001
		-6.0567700000000004e-09 -0.55837400000000004 0.203232
		-3.0751100000000001e-09 -0.58518199999999998 0.103183
		0 -0.59420899999999999 0
		0 -0.58518199999999998 -0.103183
		0 -0.55837400000000004 -0.203232
		0 -0.51460099999999998 -0.29710500000000001
		0 -0.45519100000000001 -0.38195099999999998
		0 -0.38195000000000001 -0.45519100000000001
		0 -0.29710500000000001 -0.51460099999999998
		0 -0.203232 -0.55837499999999995
		0 -0.103183 -0.58518199999999998
		0 0 -0.59421000000000002
		0 0.103183 -0.58518199999999998
		0 0.203232 -0.55837499999999995
		0 0.29710500000000001 -0.51460099999999998
		0 0.38195000000000001 -0.45519100000000001
		0 0.45519100000000001 -0.38195099999999998
		0 0.51460099999999998 -0.29710500000000001
		0 0.55837400000000004 -0.203232
		0 0.58518199999999998 -0.103183
		0 0.59420899999999999 0
		0.103183 0.58518199999999998 0
		0.203232 0.55837400000000004 0
		0.29710500000000001 0.51460099999999998 0
		0.38195099999999998 0.45519100000000001 0
		0.45519100000000001 0.38195000000000001 0
		0.51460099999999998 0.29710500000000001 0
		0.55837400000000004 0.203232 0
		0.58518199999999998 0.103183 0
		0.59420899999999999 0 0
		0.58518199999999998 -0.103183 0
		0.55837400000000004 -0.203232 0
		0.51460099999999998 -0.29710500000000001 0
		0.45519100000000001 -0.38195000000000001 0
		0.38195099999999998 -0.45519100000000001 0
		0.29710500000000001 -0.51460099999999998 0
		0.203232 -0.55837400000000004 0
		0.103183 -0.58518199999999998 0
		0 -0.59420899999999999 0
		-0.103183 -0.58518199999999998 0
		-0.203232 -0.55837400000000004 0
		-0.29710500000000001 -0.51460099999999998 0
		-0.38195099999999998 -0.45519100000000001 0
		-0.45519100000000001 -0.38195000000000001 0
		-0.51460099999999998 -0.29710500000000001 0
		-0.55837400000000004 -0.203232 0
		-0.58518199999999998 -0.103183 0
		-0.59421000000000002 0 0
		-0.58518199999999998 0.103183 0
		-0.55837400000000004 0.203232 0
		-0.51460099999999998 0.29710500000000001 0
		-0.45519100000000001 0.38195000000000001 0
		-0.38195099999999998 0.45519100000000001 0
		-0.29710500000000001 0.51460099999999998 0
		-0.203232 0.55837400000000004 0
		-0.103183 0.58518199999999998 0
		0 0.59420899999999999 0
		-3.0751100000000001e-09 0.58518199999999998 0.103183
		-6.0567700000000004e-09 0.55837400000000004 0.203232
		-8.8544099999999994e-09 0.51460099999999998 0.29710500000000001
		-1.1383e-08 0.45519100000000001 0.38195099999999998
		-1.3565700000000001e-08 0.38195000000000001 0.45519100000000001
		-1.5336300000000002e-08 0.29710500000000001 0.51460099999999998
		-1.6640900000000001e-08 0.203232 0.55837400000000004
		-1.7439800000000002e-08 0.103183 0.58518199999999998
		-1.7708799999999999e-08 0 0.59421000000000002
		-0.18362100000000001 0 0.56512700000000005
		-0.34926800000000002 0 0.48072599999999999
		-0.48072599999999999 0 0.34926800000000002
		-0.56512700000000005 0 0.18362100000000001
		-0.59421000000000002 0 0
		-0.56512700000000005 0 -0.18362100000000001
		-0.48072599999999999 0 -0.34926800000000002
		-0.34926800000000002 0 -0.48072599999999999
		-0.18362100000000001 0 -0.56512700000000005
		0 0 -0.59421000000000002
		0.18362100000000001 0 -0.56512700000000005
		0.34926800000000002 0 -0.48072599999999999
		0.48072599999999999 0 -0.34926800000000002
		0.56512700000000005 0 -0.18362100000000001
		0.59420899999999999 0 0
		0.56512700000000005 0 0.18362100000000001
		0.48072599999999999 0 0.34926800000000002
		0.34926800000000002 0 0.48072599999999999
		0.18362100000000001 0 0.56512700000000005
		-1.7708799999999999e-08 0 0.59421000000000002
		;
createNode nurbsCurve -n "L_Mouth_Orient_Guide_Guide_Ctrl_Ctrl_CtrlShape" -p "L_Mouth_Orient_Guide_Guide";
	rename -uid "B71C6631-467D-DD81-E09A-D7B8DB66B7E4";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2026/scripts/Mutant_Tools/Icons/";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".hpb" yes;
	setAttr ".ovc" 13;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 9 0 no 3
		10 0 1 2 3 4 5 6 7 8 9
		10
		-0.5 -0.25 -1.3977299999999999e-05
		0.94513100000000005 -0.25591599999999998 -1.3977299999999999e-05
		0.739653 -0.50644299999999998 -1.3977299999999999e-05
		0.99017999999999995 -0.93915099999999996 -1.3977299999999999e-05
		2.299302 -3.8742999999999997e-07 -1.37985e-05
		0.99018099999999998 0.93915099999999996 -1.3977299999999999e-05
		0.739653 0.50644199999999995 -1.3977299999999999e-05
		0.94513100000000005 0.25322099999999997 -7.1674600000000002e-06
		-0.5 0.25 -1.3977299999999999e-05
		-0.5 -0.25 -1.3977299999999999e-05
		;
createNode nurbsCurve -n "L_Mouth_Orient_Guide_Guide_Ctrl_Ctrl_Ctrl_CtrlShape" -p
		 "L_Mouth_Orient_Guide_Guide";
	rename -uid "7EADA500-43D9-B2CE-53BD-DFA1891D3CC5";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2026/scripts/Mutant_Tools/Icons/";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".hpb" yes;
	setAttr ".ovc" 6;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 9 0 no 3
		10 0 1 2 3 4 5 6 7 8 9
		10
		0.25 1.3977299999999999e-05 -0.5
		0.25591599999999998 1.3977299999999999e-05 0.94513100000000005
		0.50644299999999998 1.3977299999999999e-05 0.739653
		0.93915099999999996 1.3977299999999999e-05 0.99017999999999995
		3.8742999999999997e-07 1.37985e-05 2.299302
		-0.93915099999999996 1.3977299999999999e-05 0.99018099999999998
		-0.50644199999999995 1.3977299999999999e-05 0.739653
		-0.25322099999999997 7.1674600000000002e-06 0.94513100000000005
		-0.25 1.3977299999999999e-05 -0.5
		0.25 1.3977299999999999e-05 -0.5
		;
createNode joint -n "Mouth_SlideCenter_Guide_Guide" -p "Mouth_Block";
	rename -uid "8498D5A4-4D16-E850-219C-B994040745F3";
	addAttr -ci true -sn "Helper" -ln "Helper" -min 0 -max 1 -en "Hide:Show" -at "enum";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2026/scripts/Mutant_Tools/Icons/";
	setAttr ".t" -type "double3" 0 167.56492181665618 12.542375871512684 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr -cb on ".Helper" 1;
createNode nurbsCurve -n "Mouth_SlideCenter_Guide_Guide_CtrlShape" -p "Mouth_SlideCenter_Guide_Guide";
	rename -uid "93E46825-40DE-D2D8-5947-2A8FDFA9584A";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2026/scripts/Mutant_Tools/Icons/";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".hpb" yes;
	setAttr ".ovc" 14;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 9 0 no 3
		10 0 1 2 3 4 5 6 7 8 9
		10
		1.3977299999999999e-05 -0.5 0.25
		1.3977299999999999e-05 0.94513100000000005 0.25591599999999998
		1.3977299999999999e-05 0.739653 0.50644299999999998
		1.3977299999999999e-05 0.99017999999999995 0.93915099999999996
		1.37985e-05 2.299302 3.8742999999999997e-07
		1.3977299999999999e-05 0.99018099999999998 -0.93915099999999996
		1.3977299999999999e-05 0.739653 -0.50644199999999995
		7.1674600000000002e-06 0.94513100000000005 -0.25322099999999997
		1.3977299999999999e-05 -0.5 -0.25
		1.3977299999999999e-05 -0.5 0.25
		;
createNode nurbsCurve -n "Mouth_SlideCenter_Guide_Guide_Ctrl_CtrlShape" -p "Mouth_SlideCenter_Guide_Guide";
	rename -uid "8796695A-48CE-CAE8-CDCE-FE96B3446997";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2026/scripts/Mutant_Tools/Icons/";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".hpb" yes;
	setAttr ".ovc" 18;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 101 0 no 3
		102 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27
		 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54
		 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81
		 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99 100 101
		102
		0 0.59420899999999999 0
		-3.0751100000000001e-09 0.58518199999999998 0.103183
		-6.0567700000000004e-09 0.55837400000000004 0.203232
		-8.8544099999999994e-09 0.51460099999999998 0.29710500000000001
		-1.1383e-08 0.45519100000000001 0.38195099999999998
		-1.3565700000000001e-08 0.38195000000000001 0.45519100000000001
		-1.5336300000000002e-08 0.29710500000000001 0.51460099999999998
		-1.6640900000000001e-08 0.203232 0.55837400000000004
		-1.7439800000000002e-08 0.103183 0.58518199999999998
		-1.7708799999999999e-08 0 0.59421000000000002
		-1.7439800000000002e-08 -0.103183 0.58518199999999998
		-1.6640900000000001e-08 -0.203232 0.55837400000000004
		-1.5336300000000002e-08 -0.29710500000000001 0.51460099999999998
		-1.3565700000000001e-08 -0.38195000000000001 0.45519100000000001
		-1.1383e-08 -0.45519100000000001 0.38195099999999998
		-8.8544099999999994e-09 -0.51460099999999998 0.29710500000000001
		-6.0567700000000004e-09 -0.55837400000000004 0.203232
		-3.0751100000000001e-09 -0.58518199999999998 0.103183
		0 -0.59420899999999999 0
		0 -0.58518199999999998 -0.103183
		0 -0.55837400000000004 -0.203232
		0 -0.51460099999999998 -0.29710500000000001
		0 -0.45519100000000001 -0.38195099999999998
		0 -0.38195000000000001 -0.45519100000000001
		0 -0.29710500000000001 -0.51460099999999998
		0 -0.203232 -0.55837499999999995
		0 -0.103183 -0.58518199999999998
		0 0 -0.59421000000000002
		0 0.103183 -0.58518199999999998
		0 0.203232 -0.55837499999999995
		0 0.29710500000000001 -0.51460099999999998
		0 0.38195000000000001 -0.45519100000000001
		0 0.45519100000000001 -0.38195099999999998
		0 0.51460099999999998 -0.29710500000000001
		0 0.55837400000000004 -0.203232
		0 0.58518199999999998 -0.103183
		0 0.59420899999999999 0
		0.103183 0.58518199999999998 0
		0.203232 0.55837400000000004 0
		0.29710500000000001 0.51460099999999998 0
		0.38195099999999998 0.45519100000000001 0
		0.45519100000000001 0.38195000000000001 0
		0.51460099999999998 0.29710500000000001 0
		0.55837400000000004 0.203232 0
		0.58518199999999998 0.103183 0
		0.59420899999999999 0 0
		0.58518199999999998 -0.103183 0
		0.55837400000000004 -0.203232 0
		0.51460099999999998 -0.29710500000000001 0
		0.45519100000000001 -0.38195000000000001 0
		0.38195099999999998 -0.45519100000000001 0
		0.29710500000000001 -0.51460099999999998 0
		0.203232 -0.55837400000000004 0
		0.103183 -0.58518199999999998 0
		0 -0.59420899999999999 0
		-0.103183 -0.58518199999999998 0
		-0.203232 -0.55837400000000004 0
		-0.29710500000000001 -0.51460099999999998 0
		-0.38195099999999998 -0.45519100000000001 0
		-0.45519100000000001 -0.38195000000000001 0
		-0.51460099999999998 -0.29710500000000001 0
		-0.55837400000000004 -0.203232 0
		-0.58518199999999998 -0.103183 0
		-0.59421000000000002 0 0
		-0.58518199999999998 0.103183 0
		-0.55837400000000004 0.203232 0
		-0.51460099999999998 0.29710500000000001 0
		-0.45519100000000001 0.38195000000000001 0
		-0.38195099999999998 0.45519100000000001 0
		-0.29710500000000001 0.51460099999999998 0
		-0.203232 0.55837400000000004 0
		-0.103183 0.58518199999999998 0
		0 0.59420899999999999 0
		-3.0751100000000001e-09 0.58518199999999998 0.103183
		-6.0567700000000004e-09 0.55837400000000004 0.203232
		-8.8544099999999994e-09 0.51460099999999998 0.29710500000000001
		-1.1383e-08 0.45519100000000001 0.38195099999999998
		-1.3565700000000001e-08 0.38195000000000001 0.45519100000000001
		-1.5336300000000002e-08 0.29710500000000001 0.51460099999999998
		-1.6640900000000001e-08 0.203232 0.55837400000000004
		-1.7439800000000002e-08 0.103183 0.58518199999999998
		-1.7708799999999999e-08 0 0.59421000000000002
		-0.18362100000000001 0 0.56512700000000005
		-0.34926800000000002 0 0.48072599999999999
		-0.48072599999999999 0 0.34926800000000002
		-0.56512700000000005 0 0.18362100000000001
		-0.59421000000000002 0 0
		-0.56512700000000005 0 -0.18362100000000001
		-0.48072599999999999 0 -0.34926800000000002
		-0.34926800000000002 0 -0.48072599999999999
		-0.18362100000000001 0 -0.56512700000000005
		0 0 -0.59421000000000002
		0.18362100000000001 0 -0.56512700000000005
		0.34926800000000002 0 -0.48072599999999999
		0.48072599999999999 0 -0.34926800000000002
		0.56512700000000005 0 -0.18362100000000001
		0.59420899999999999 0 0
		0.56512700000000005 0 0.18362100000000001
		0.48072599999999999 0 0.34926800000000002
		0.34926800000000002 0 0.48072599999999999
		0.18362100000000001 0 0.56512700000000005
		-1.7708799999999999e-08 0 0.59421000000000002
		;
createNode nurbsCurve -n "Mouth_SlideCenter_Guide_Guide_Ctrl_Ctrl_CtrlShape" -p "Mouth_SlideCenter_Guide_Guide";
	rename -uid "B1E9A191-477C-8F7E-4203-3BB95557E921";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2026/scripts/Mutant_Tools/Icons/";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".hpb" yes;
	setAttr ".ovc" 13;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 9 0 no 3
		10 0 1 2 3 4 5 6 7 8 9
		10
		-0.5 -0.25 -1.3977299999999999e-05
		0.94513100000000005 -0.25591599999999998 -1.3977299999999999e-05
		0.739653 -0.50644299999999998 -1.3977299999999999e-05
		0.99017999999999995 -0.93915099999999996 -1.3977299999999999e-05
		2.299302 -3.8742999999999997e-07 -1.37985e-05
		0.99018099999999998 0.93915099999999996 -1.3977299999999999e-05
		0.739653 0.50644199999999995 -1.3977299999999999e-05
		0.94513100000000005 0.25322099999999997 -7.1674600000000002e-06
		-0.5 0.25 -1.3977299999999999e-05
		-0.5 -0.25 -1.3977299999999999e-05
		;
createNode nurbsCurve -n "Mouth_SlideCenter_Guide_Guide_Ctrl_Ctrl_Ctrl_CtrlShape" 
		-p "Mouth_SlideCenter_Guide_Guide";
	rename -uid "D7E00B83-4D0B-C691-9C1A-C2A2743EF8BF";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2026/scripts/Mutant_Tools/Icons/";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".hpb" yes;
	setAttr ".ovc" 6;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 9 0 no 3
		10 0 1 2 3 4 5 6 7 8 9
		10
		0.25 1.3977299999999999e-05 -0.5
		0.25591599999999998 1.3977299999999999e-05 0.94513100000000005
		0.50644299999999998 1.3977299999999999e-05 0.739653
		0.93915099999999996 1.3977299999999999e-05 0.99017999999999995
		3.8742999999999997e-07 1.37985e-05 2.299302
		-0.93915099999999996 1.3977299999999999e-05 0.99018099999999998
		-0.50644199999999995 1.3977299999999999e-05 0.739653
		-0.25322099999999997 7.1674600000000002e-06 0.94513100000000005
		-0.25 1.3977299999999999e-05 -0.5
		0.25 1.3977299999999999e-05 -0.5
		;
createNode joint -n "Mouth_Jaw_Guide_Guide" -p "Mouth_Block";
	rename -uid "CDAF680C-42D7-1FBD-EC2F-03B7AEFC2EC1";
	addAttr -ci true -sn "Helper" -ln "Helper" -min 0 -max 1 -en "Hide:Show" -at "enum";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2026/scripts/Mutant_Tools/Icons/";
	setAttr ".t" -type "double3" 0 173.82236866901098 2.6846676332799406 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr -cb on ".Helper" 1;
createNode nurbsCurve -n "Mouth_Jaw_Guide_Guide_CtrlShape" -p "Mouth_Jaw_Guide_Guide";
	rename -uid "B834BAF1-408A-4981-A9BC-1E9C5BDF8D44";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2026/scripts/Mutant_Tools/Icons/";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".hpb" yes;
	setAttr ".ovc" 14;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 9 0 no 3
		10 0 1 2 3 4 5 6 7 8 9
		10
		1.3977299999999999e-05 -0.5 0.25
		1.3977299999999999e-05 0.94513100000000005 0.25591599999999998
		1.3977299999999999e-05 0.739653 0.50644299999999998
		1.3977299999999999e-05 0.99017999999999995 0.93915099999999996
		1.37985e-05 2.299302 3.8742999999999997e-07
		1.3977299999999999e-05 0.99018099999999998 -0.93915099999999996
		1.3977299999999999e-05 0.739653 -0.50644199999999995
		7.1674600000000002e-06 0.94513100000000005 -0.25322099999999997
		1.3977299999999999e-05 -0.5 -0.25
		1.3977299999999999e-05 -0.5 0.25
		;
createNode nurbsCurve -n "Mouth_Jaw_Guide_Guide_Ctrl_CtrlShape" -p "Mouth_Jaw_Guide_Guide";
	rename -uid "6E5F884F-4CC9-9249-CFEB-58B6DDD9CF03";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2026/scripts/Mutant_Tools/Icons/";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".hpb" yes;
	setAttr ".ovc" 18;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 101 0 no 3
		102 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27
		 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54
		 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81
		 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99 100 101
		102
		0 0.59420899999999999 0
		-3.0751100000000001e-09 0.58518199999999998 0.103183
		-6.0567700000000004e-09 0.55837400000000004 0.203232
		-8.8544099999999994e-09 0.51460099999999998 0.29710500000000001
		-1.1383e-08 0.45519100000000001 0.38195099999999998
		-1.3565700000000001e-08 0.38195000000000001 0.45519100000000001
		-1.5336300000000002e-08 0.29710500000000001 0.51460099999999998
		-1.6640900000000001e-08 0.203232 0.55837400000000004
		-1.7439800000000002e-08 0.103183 0.58518199999999998
		-1.7708799999999999e-08 0 0.59421000000000002
		-1.7439800000000002e-08 -0.103183 0.58518199999999998
		-1.6640900000000001e-08 -0.203232 0.55837400000000004
		-1.5336300000000002e-08 -0.29710500000000001 0.51460099999999998
		-1.3565700000000001e-08 -0.38195000000000001 0.45519100000000001
		-1.1383e-08 -0.45519100000000001 0.38195099999999998
		-8.8544099999999994e-09 -0.51460099999999998 0.29710500000000001
		-6.0567700000000004e-09 -0.55837400000000004 0.203232
		-3.0751100000000001e-09 -0.58518199999999998 0.103183
		0 -0.59420899999999999 0
		0 -0.58518199999999998 -0.103183
		0 -0.55837400000000004 -0.203232
		0 -0.51460099999999998 -0.29710500000000001
		0 -0.45519100000000001 -0.38195099999999998
		0 -0.38195000000000001 -0.45519100000000001
		0 -0.29710500000000001 -0.51460099999999998
		0 -0.203232 -0.55837499999999995
		0 -0.103183 -0.58518199999999998
		0 0 -0.59421000000000002
		0 0.103183 -0.58518199999999998
		0 0.203232 -0.55837499999999995
		0 0.29710500000000001 -0.51460099999999998
		0 0.38195000000000001 -0.45519100000000001
		0 0.45519100000000001 -0.38195099999999998
		0 0.51460099999999998 -0.29710500000000001
		0 0.55837400000000004 -0.203232
		0 0.58518199999999998 -0.103183
		0 0.59420899999999999 0
		0.103183 0.58518199999999998 0
		0.203232 0.55837400000000004 0
		0.29710500000000001 0.51460099999999998 0
		0.38195099999999998 0.45519100000000001 0
		0.45519100000000001 0.38195000000000001 0
		0.51460099999999998 0.29710500000000001 0
		0.55837400000000004 0.203232 0
		0.58518199999999998 0.103183 0
		0.59420899999999999 0 0
		0.58518199999999998 -0.103183 0
		0.55837400000000004 -0.203232 0
		0.51460099999999998 -0.29710500000000001 0
		0.45519100000000001 -0.38195000000000001 0
		0.38195099999999998 -0.45519100000000001 0
		0.29710500000000001 -0.51460099999999998 0
		0.203232 -0.55837400000000004 0
		0.103183 -0.58518199999999998 0
		0 -0.59420899999999999 0
		-0.103183 -0.58518199999999998 0
		-0.203232 -0.55837400000000004 0
		-0.29710500000000001 -0.51460099999999998 0
		-0.38195099999999998 -0.45519100000000001 0
		-0.45519100000000001 -0.38195000000000001 0
		-0.51460099999999998 -0.29710500000000001 0
		-0.55837400000000004 -0.203232 0
		-0.58518199999999998 -0.103183 0
		-0.59421000000000002 0 0
		-0.58518199999999998 0.103183 0
		-0.55837400000000004 0.203232 0
		-0.51460099999999998 0.29710500000000001 0
		-0.45519100000000001 0.38195000000000001 0
		-0.38195099999999998 0.45519100000000001 0
		-0.29710500000000001 0.51460099999999998 0
		-0.203232 0.55837400000000004 0
		-0.103183 0.58518199999999998 0
		0 0.59420899999999999 0
		-3.0751100000000001e-09 0.58518199999999998 0.103183
		-6.0567700000000004e-09 0.55837400000000004 0.203232
		-8.8544099999999994e-09 0.51460099999999998 0.29710500000000001
		-1.1383e-08 0.45519100000000001 0.38195099999999998
		-1.3565700000000001e-08 0.38195000000000001 0.45519100000000001
		-1.5336300000000002e-08 0.29710500000000001 0.51460099999999998
		-1.6640900000000001e-08 0.203232 0.55837400000000004
		-1.7439800000000002e-08 0.103183 0.58518199999999998
		-1.7708799999999999e-08 0 0.59421000000000002
		-0.18362100000000001 0 0.56512700000000005
		-0.34926800000000002 0 0.48072599999999999
		-0.48072599999999999 0 0.34926800000000002
		-0.56512700000000005 0 0.18362100000000001
		-0.59421000000000002 0 0
		-0.56512700000000005 0 -0.18362100000000001
		-0.48072599999999999 0 -0.34926800000000002
		-0.34926800000000002 0 -0.48072599999999999
		-0.18362100000000001 0 -0.56512700000000005
		0 0 -0.59421000000000002
		0.18362100000000001 0 -0.56512700000000005
		0.34926800000000002 0 -0.48072599999999999
		0.48072599999999999 0 -0.34926800000000002
		0.56512700000000005 0 -0.18362100000000001
		0.59420899999999999 0 0
		0.56512700000000005 0 0.18362100000000001
		0.48072599999999999 0 0.34926800000000002
		0.34926800000000002 0 0.48072599999999999
		0.18362100000000001 0 0.56512700000000005
		-1.7708799999999999e-08 0 0.59421000000000002
		;
createNode nurbsCurve -n "Mouth_Jaw_Guide_Guide_Ctrl_Ctrl_CtrlShape" -p "Mouth_Jaw_Guide_Guide";
	rename -uid "EAA8DA36-4ED0-A94D-8A82-8992B59F131E";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2026/scripts/Mutant_Tools/Icons/";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".hpb" yes;
	setAttr ".ovc" 13;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 9 0 no 3
		10 0 1 2 3 4 5 6 7 8 9
		10
		-0.5 -0.25 -1.3977299999999999e-05
		0.94513100000000005 -0.25591599999999998 -1.3977299999999999e-05
		0.739653 -0.50644299999999998 -1.3977299999999999e-05
		0.99017999999999995 -0.93915099999999996 -1.3977299999999999e-05
		2.299302 -3.8742999999999997e-07 -1.37985e-05
		0.99018099999999998 0.93915099999999996 -1.3977299999999999e-05
		0.739653 0.50644199999999995 -1.3977299999999999e-05
		0.94513100000000005 0.25322099999999997 -7.1674600000000002e-06
		-0.5 0.25 -1.3977299999999999e-05
		-0.5 -0.25 -1.3977299999999999e-05
		;
createNode nurbsCurve -n "Mouth_Jaw_Guide_Guide_Ctrl_Ctrl_Ctrl_CtrlShape" -p "Mouth_Jaw_Guide_Guide";
	rename -uid "3E4ACD8A-4708-B640-9990-E5910214B148";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2026/scripts/Mutant_Tools/Icons/";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".hpb" yes;
	setAttr ".ovc" 6;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 9 0 no 3
		10 0 1 2 3 4 5 6 7 8 9
		10
		0.25 1.3977299999999999e-05 -0.5
		0.25591599999999998 1.3977299999999999e-05 0.94513100000000005
		0.50644299999999998 1.3977299999999999e-05 0.739653
		0.93915099999999996 1.3977299999999999e-05 0.99017999999999995
		3.8742999999999997e-07 1.37985e-05 2.299302
		-0.93915099999999996 1.3977299999999999e-05 0.99018099999999998
		-0.50644199999999995 1.3977299999999999e-05 0.739653
		-0.25322099999999997 7.1674600000000002e-06 0.94513100000000005
		-0.25 1.3977299999999999e-05 -0.5
		0.25 1.3977299999999999e-05 -0.5
		;
createNode joint -n "Mouth_LipUp_Guide_Guide" -p "Mouth_Block";
	rename -uid "A5DE607C-4AFC-3068-7AB2-03BB9AD3A13C";
	addAttr -ci true -sn "Helper" -ln "Helper" -min 0 -max 1 -en "Hide:Show" -at "enum";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2026/scripts/Mutant_Tools/Icons/";
	setAttr ".t" -type "double3" 0 169.58000528244014 16.82071557351351 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr -cb on ".Helper" 1;
createNode nurbsCurve -n "Mouth_LipUp_Guide_Guide_CtrlShape" -p "Mouth_LipUp_Guide_Guide";
	rename -uid "5083BDC5-43CC-CECC-0712-1E87F8C765A9";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2026/scripts/Mutant_Tools/Icons/";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".hpb" yes;
	setAttr ".ovc" 14;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 9 0 no 3
		10 0 1 2 3 4 5 6 7 8 9
		10
		1.3977299999999999e-05 -0.5 0.25
		1.3977299999999999e-05 0.94513100000000005 0.25591599999999998
		1.3977299999999999e-05 0.739653 0.50644299999999998
		1.3977299999999999e-05 0.99017999999999995 0.93915099999999996
		1.37985e-05 2.299302 3.8742999999999997e-07
		1.3977299999999999e-05 0.99018099999999998 -0.93915099999999996
		1.3977299999999999e-05 0.739653 -0.50644199999999995
		7.1674600000000002e-06 0.94513100000000005 -0.25322099999999997
		1.3977299999999999e-05 -0.5 -0.25
		1.3977299999999999e-05 -0.5 0.25
		;
createNode nurbsCurve -n "Mouth_LipUp_Guide_Guide_Ctrl_CtrlShape" -p "Mouth_LipUp_Guide_Guide";
	rename -uid "4B1603B4-4660-2F06-D6E4-B79568CC3162";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2026/scripts/Mutant_Tools/Icons/";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".hpb" yes;
	setAttr ".ovc" 18;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 101 0 no 3
		102 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27
		 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54
		 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81
		 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99 100 101
		102
		0 0.59420899999999999 0
		-3.0751100000000001e-09 0.58518199999999998 0.103183
		-6.0567700000000004e-09 0.55837400000000004 0.203232
		-8.8544099999999994e-09 0.51460099999999998 0.29710500000000001
		-1.1383e-08 0.45519100000000001 0.38195099999999998
		-1.3565700000000001e-08 0.38195000000000001 0.45519100000000001
		-1.5336300000000002e-08 0.29710500000000001 0.51460099999999998
		-1.6640900000000001e-08 0.203232 0.55837400000000004
		-1.7439800000000002e-08 0.103183 0.58518199999999998
		-1.7708799999999999e-08 0 0.59421000000000002
		-1.7439800000000002e-08 -0.103183 0.58518199999999998
		-1.6640900000000001e-08 -0.203232 0.55837400000000004
		-1.5336300000000002e-08 -0.29710500000000001 0.51460099999999998
		-1.3565700000000001e-08 -0.38195000000000001 0.45519100000000001
		-1.1383e-08 -0.45519100000000001 0.38195099999999998
		-8.8544099999999994e-09 -0.51460099999999998 0.29710500000000001
		-6.0567700000000004e-09 -0.55837400000000004 0.203232
		-3.0751100000000001e-09 -0.58518199999999998 0.103183
		0 -0.59420899999999999 0
		0 -0.58518199999999998 -0.103183
		0 -0.55837400000000004 -0.203232
		0 -0.51460099999999998 -0.29710500000000001
		0 -0.45519100000000001 -0.38195099999999998
		0 -0.38195000000000001 -0.45519100000000001
		0 -0.29710500000000001 -0.51460099999999998
		0 -0.203232 -0.55837499999999995
		0 -0.103183 -0.58518199999999998
		0 0 -0.59421000000000002
		0 0.103183 -0.58518199999999998
		0 0.203232 -0.55837499999999995
		0 0.29710500000000001 -0.51460099999999998
		0 0.38195000000000001 -0.45519100000000001
		0 0.45519100000000001 -0.38195099999999998
		0 0.51460099999999998 -0.29710500000000001
		0 0.55837400000000004 -0.203232
		0 0.58518199999999998 -0.103183
		0 0.59420899999999999 0
		0.103183 0.58518199999999998 0
		0.203232 0.55837400000000004 0
		0.29710500000000001 0.51460099999999998 0
		0.38195099999999998 0.45519100000000001 0
		0.45519100000000001 0.38195000000000001 0
		0.51460099999999998 0.29710500000000001 0
		0.55837400000000004 0.203232 0
		0.58518199999999998 0.103183 0
		0.59420899999999999 0 0
		0.58518199999999998 -0.103183 0
		0.55837400000000004 -0.203232 0
		0.51460099999999998 -0.29710500000000001 0
		0.45519100000000001 -0.38195000000000001 0
		0.38195099999999998 -0.45519100000000001 0
		0.29710500000000001 -0.51460099999999998 0
		0.203232 -0.55837400000000004 0
		0.103183 -0.58518199999999998 0
		0 -0.59420899999999999 0
		-0.103183 -0.58518199999999998 0
		-0.203232 -0.55837400000000004 0
		-0.29710500000000001 -0.51460099999999998 0
		-0.38195099999999998 -0.45519100000000001 0
		-0.45519100000000001 -0.38195000000000001 0
		-0.51460099999999998 -0.29710500000000001 0
		-0.55837400000000004 -0.203232 0
		-0.58518199999999998 -0.103183 0
		-0.59421000000000002 0 0
		-0.58518199999999998 0.103183 0
		-0.55837400000000004 0.203232 0
		-0.51460099999999998 0.29710500000000001 0
		-0.45519100000000001 0.38195000000000001 0
		-0.38195099999999998 0.45519100000000001 0
		-0.29710500000000001 0.51460099999999998 0
		-0.203232 0.55837400000000004 0
		-0.103183 0.58518199999999998 0
		0 0.59420899999999999 0
		-3.0751100000000001e-09 0.58518199999999998 0.103183
		-6.0567700000000004e-09 0.55837400000000004 0.203232
		-8.8544099999999994e-09 0.51460099999999998 0.29710500000000001
		-1.1383e-08 0.45519100000000001 0.38195099999999998
		-1.3565700000000001e-08 0.38195000000000001 0.45519100000000001
		-1.5336300000000002e-08 0.29710500000000001 0.51460099999999998
		-1.6640900000000001e-08 0.203232 0.55837400000000004
		-1.7439800000000002e-08 0.103183 0.58518199999999998
		-1.7708799999999999e-08 0 0.59421000000000002
		-0.18362100000000001 0 0.56512700000000005
		-0.34926800000000002 0 0.48072599999999999
		-0.48072599999999999 0 0.34926800000000002
		-0.56512700000000005 0 0.18362100000000001
		-0.59421000000000002 0 0
		-0.56512700000000005 0 -0.18362100000000001
		-0.48072599999999999 0 -0.34926800000000002
		-0.34926800000000002 0 -0.48072599999999999
		-0.18362100000000001 0 -0.56512700000000005
		0 0 -0.59421000000000002
		0.18362100000000001 0 -0.56512700000000005
		0.34926800000000002 0 -0.48072599999999999
		0.48072599999999999 0 -0.34926800000000002
		0.56512700000000005 0 -0.18362100000000001
		0.59420899999999999 0 0
		0.56512700000000005 0 0.18362100000000001
		0.48072599999999999 0 0.34926800000000002
		0.34926800000000002 0 0.48072599999999999
		0.18362100000000001 0 0.56512700000000005
		-1.7708799999999999e-08 0 0.59421000000000002
		;
createNode nurbsCurve -n "Mouth_LipUp_Guide_Guide_Ctrl_Ctrl_CtrlShape" -p "Mouth_LipUp_Guide_Guide";
	rename -uid "2E2D54AD-4BC3-2C97-F6E8-1FAF2731495D";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2026/scripts/Mutant_Tools/Icons/";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".hpb" yes;
	setAttr ".ovc" 13;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 9 0 no 3
		10 0 1 2 3 4 5 6 7 8 9
		10
		-0.5 -0.25 -1.3977299999999999e-05
		0.94513100000000005 -0.25591599999999998 -1.3977299999999999e-05
		0.739653 -0.50644299999999998 -1.3977299999999999e-05
		0.99017999999999995 -0.93915099999999996 -1.3977299999999999e-05
		2.299302 -3.8742999999999997e-07 -1.37985e-05
		0.99018099999999998 0.93915099999999996 -1.3977299999999999e-05
		0.739653 0.50644199999999995 -1.3977299999999999e-05
		0.94513100000000005 0.25322099999999997 -7.1674600000000002e-06
		-0.5 0.25 -1.3977299999999999e-05
		-0.5 -0.25 -1.3977299999999999e-05
		;
createNode nurbsCurve -n "Mouth_LipUp_Guide_Guide_Ctrl_Ctrl_Ctrl_CtrlShape" -p "Mouth_LipUp_Guide_Guide";
	rename -uid "F49BBF53-4489-360C-469B-AD83739E43C9";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2026/scripts/Mutant_Tools/Icons/";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".hpb" yes;
	setAttr ".ovc" 6;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 9 0 no 3
		10 0 1 2 3 4 5 6 7 8 9
		10
		0.25 1.3977299999999999e-05 -0.5
		0.25591599999999998 1.3977299999999999e-05 0.94513100000000005
		0.50644299999999998 1.3977299999999999e-05 0.739653
		0.93915099999999996 1.3977299999999999e-05 0.99017999999999995
		3.8742999999999997e-07 1.37985e-05 2.299302
		-0.93915099999999996 1.3977299999999999e-05 0.99018099999999998
		-0.50644199999999995 1.3977299999999999e-05 0.739653
		-0.25322099999999997 7.1674600000000002e-06 0.94513100000000005
		-0.25 1.3977299999999999e-05 -0.5
		0.25 1.3977299999999999e-05 -0.5
		;
createNode joint -n "Mouth_LipDown_Guide_Guide" -p "Mouth_Block";
	rename -uid "A88C5952-4A65-F0E6-A76F-B9842C16AB09";
	addAttr -ci true -sn "Helper" -ln "Helper" -min 0 -max 1 -en "Hide:Show" -at "enum";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2026/scripts/Mutant_Tools/Icons/";
	setAttr ".t" -type "double3" 0 166.68645367940621 16.549619341721694 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr -cb on ".Helper" 1;
createNode nurbsCurve -n "Mouth_LipDown_Guide_Guide_CtrlShape" -p "Mouth_LipDown_Guide_Guide";
	rename -uid "8F593CBF-4326-ED9E-8F64-13844CED960A";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2026/scripts/Mutant_Tools/Icons/";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".hpb" yes;
	setAttr ".ovc" 14;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 9 0 no 3
		10 0 1 2 3 4 5 6 7 8 9
		10
		1.3977299999999999e-05 -0.5 0.25
		1.3977299999999999e-05 0.94513100000000005 0.25591599999999998
		1.3977299999999999e-05 0.739653 0.50644299999999998
		1.3977299999999999e-05 0.99017999999999995 0.93915099999999996
		1.37985e-05 2.299302 3.8742999999999997e-07
		1.3977299999999999e-05 0.99018099999999998 -0.93915099999999996
		1.3977299999999999e-05 0.739653 -0.50644199999999995
		7.1674600000000002e-06 0.94513100000000005 -0.25322099999999997
		1.3977299999999999e-05 -0.5 -0.25
		1.3977299999999999e-05 -0.5 0.25
		;
createNode nurbsCurve -n "Mouth_LipDown_Guide_Guide_Ctrl_CtrlShape" -p "Mouth_LipDown_Guide_Guide";
	rename -uid "2AB5EAA4-4C47-AE00-8561-179ABE44584B";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2026/scripts/Mutant_Tools/Icons/";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".hpb" yes;
	setAttr ".ovc" 18;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 101 0 no 3
		102 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27
		 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54
		 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81
		 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99 100 101
		102
		0 0.59420899999999999 0
		-3.0751100000000001e-09 0.58518199999999998 0.103183
		-6.0567700000000004e-09 0.55837400000000004 0.203232
		-8.8544099999999994e-09 0.51460099999999998 0.29710500000000001
		-1.1383e-08 0.45519100000000001 0.38195099999999998
		-1.3565700000000001e-08 0.38195000000000001 0.45519100000000001
		-1.5336300000000002e-08 0.29710500000000001 0.51460099999999998
		-1.6640900000000001e-08 0.203232 0.55837400000000004
		-1.7439800000000002e-08 0.103183 0.58518199999999998
		-1.7708799999999999e-08 0 0.59421000000000002
		-1.7439800000000002e-08 -0.103183 0.58518199999999998
		-1.6640900000000001e-08 -0.203232 0.55837400000000004
		-1.5336300000000002e-08 -0.29710500000000001 0.51460099999999998
		-1.3565700000000001e-08 -0.38195000000000001 0.45519100000000001
		-1.1383e-08 -0.45519100000000001 0.38195099999999998
		-8.8544099999999994e-09 -0.51460099999999998 0.29710500000000001
		-6.0567700000000004e-09 -0.55837400000000004 0.203232
		-3.0751100000000001e-09 -0.58518199999999998 0.103183
		0 -0.59420899999999999 0
		0 -0.58518199999999998 -0.103183
		0 -0.55837400000000004 -0.203232
		0 -0.51460099999999998 -0.29710500000000001
		0 -0.45519100000000001 -0.38195099999999998
		0 -0.38195000000000001 -0.45519100000000001
		0 -0.29710500000000001 -0.51460099999999998
		0 -0.203232 -0.55837499999999995
		0 -0.103183 -0.58518199999999998
		0 0 -0.59421000000000002
		0 0.103183 -0.58518199999999998
		0 0.203232 -0.55837499999999995
		0 0.29710500000000001 -0.51460099999999998
		0 0.38195000000000001 -0.45519100000000001
		0 0.45519100000000001 -0.38195099999999998
		0 0.51460099999999998 -0.29710500000000001
		0 0.55837400000000004 -0.203232
		0 0.58518199999999998 -0.103183
		0 0.59420899999999999 0
		0.103183 0.58518199999999998 0
		0.203232 0.55837400000000004 0
		0.29710500000000001 0.51460099999999998 0
		0.38195099999999998 0.45519100000000001 0
		0.45519100000000001 0.38195000000000001 0
		0.51460099999999998 0.29710500000000001 0
		0.55837400000000004 0.203232 0
		0.58518199999999998 0.103183 0
		0.59420899999999999 0 0
		0.58518199999999998 -0.103183 0
		0.55837400000000004 -0.203232 0
		0.51460099999999998 -0.29710500000000001 0
		0.45519100000000001 -0.38195000000000001 0
		0.38195099999999998 -0.45519100000000001 0
		0.29710500000000001 -0.51460099999999998 0
		0.203232 -0.55837400000000004 0
		0.103183 -0.58518199999999998 0
		0 -0.59420899999999999 0
		-0.103183 -0.58518199999999998 0
		-0.203232 -0.55837400000000004 0
		-0.29710500000000001 -0.51460099999999998 0
		-0.38195099999999998 -0.45519100000000001 0
		-0.45519100000000001 -0.38195000000000001 0
		-0.51460099999999998 -0.29710500000000001 0
		-0.55837400000000004 -0.203232 0
		-0.58518199999999998 -0.103183 0
		-0.59421000000000002 0 0
		-0.58518199999999998 0.103183 0
		-0.55837400000000004 0.203232 0
		-0.51460099999999998 0.29710500000000001 0
		-0.45519100000000001 0.38195000000000001 0
		-0.38195099999999998 0.45519100000000001 0
		-0.29710500000000001 0.51460099999999998 0
		-0.203232 0.55837400000000004 0
		-0.103183 0.58518199999999998 0
		0 0.59420899999999999 0
		-3.0751100000000001e-09 0.58518199999999998 0.103183
		-6.0567700000000004e-09 0.55837400000000004 0.203232
		-8.8544099999999994e-09 0.51460099999999998 0.29710500000000001
		-1.1383e-08 0.45519100000000001 0.38195099999999998
		-1.3565700000000001e-08 0.38195000000000001 0.45519100000000001
		-1.5336300000000002e-08 0.29710500000000001 0.51460099999999998
		-1.6640900000000001e-08 0.203232 0.55837400000000004
		-1.7439800000000002e-08 0.103183 0.58518199999999998
		-1.7708799999999999e-08 0 0.59421000000000002
		-0.18362100000000001 0 0.56512700000000005
		-0.34926800000000002 0 0.48072599999999999
		-0.48072599999999999 0 0.34926800000000002
		-0.56512700000000005 0 0.18362100000000001
		-0.59421000000000002 0 0
		-0.56512700000000005 0 -0.18362100000000001
		-0.48072599999999999 0 -0.34926800000000002
		-0.34926800000000002 0 -0.48072599999999999
		-0.18362100000000001 0 -0.56512700000000005
		0 0 -0.59421000000000002
		0.18362100000000001 0 -0.56512700000000005
		0.34926800000000002 0 -0.48072599999999999
		0.48072599999999999 0 -0.34926800000000002
		0.56512700000000005 0 -0.18362100000000001
		0.59420899999999999 0 0
		0.56512700000000005 0 0.18362100000000001
		0.48072599999999999 0 0.34926800000000002
		0.34926800000000002 0 0.48072599999999999
		0.18362100000000001 0 0.56512700000000005
		-1.7708799999999999e-08 0 0.59421000000000002
		;
createNode nurbsCurve -n "Mouth_LipDown_Guide_Guide_Ctrl_Ctrl_CtrlShape" -p "Mouth_LipDown_Guide_Guide";
	rename -uid "C5E17E44-4F8F-50CE-859B-E0A032AF7007";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2026/scripts/Mutant_Tools/Icons/";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".hpb" yes;
	setAttr ".ovc" 13;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 9 0 no 3
		10 0 1 2 3 4 5 6 7 8 9
		10
		-0.5 -0.25 -1.3977299999999999e-05
		0.94513100000000005 -0.25591599999999998 -1.3977299999999999e-05
		0.739653 -0.50644299999999998 -1.3977299999999999e-05
		0.99017999999999995 -0.93915099999999996 -1.3977299999999999e-05
		2.299302 -3.8742999999999997e-07 -1.37985e-05
		0.99018099999999998 0.93915099999999996 -1.3977299999999999e-05
		0.739653 0.50644199999999995 -1.3977299999999999e-05
		0.94513100000000005 0.25322099999999997 -7.1674600000000002e-06
		-0.5 0.25 -1.3977299999999999e-05
		-0.5 -0.25 -1.3977299999999999e-05
		;
createNode nurbsCurve -n "Mouth_LipDown_Guide_Guide_Ctrl_Ctrl_Ctrl_CtrlShape" -p "Mouth_LipDown_Guide_Guide";
	rename -uid "C463EB19-40D4-81AA-D820-068393AF2218";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2026/scripts/Mutant_Tools/Icons/";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".hpb" yes;
	setAttr ".ovc" 6;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 9 0 no 3
		10 0 1 2 3 4 5 6 7 8 9
		10
		0.25 1.3977299999999999e-05 -0.5
		0.25591599999999998 1.3977299999999999e-05 0.94513100000000005
		0.50644299999999998 1.3977299999999999e-05 0.739653
		0.93915099999999996 1.3977299999999999e-05 0.99017999999999995
		3.8742999999999997e-07 1.37985e-05 2.299302
		-0.93915099999999996 1.3977299999999999e-05 0.99018099999999998
		-0.50644199999999995 1.3977299999999999e-05 0.739653
		-0.25322099999999997 7.1674600000000002e-06 0.94513100000000005
		-0.25 1.3977299999999999e-05 -0.5
		0.25 1.3977299999999999e-05 -0.5
		;
createNode dagContainer -n "Nose_Block" -p "Face";
	rename -uid "3E7D11F6-402C-B605-C9C0-31968222F3D0";
	addAttr -ci true -sn "nts" -ln "notes" -dt "string";
	setAttr ".isc" yes;
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2026/scripts/Mutant_Tools/Icons/Chain.png";
	setAttr ".ctor" -type "string" "rodri";
	setAttr ".cdat" -type "string" "2025/12/06 13:25:24";
	setAttr -l on -k off ".v";
	setAttr -l on -k off ".tx";
	setAttr -l on -k off ".ty";
	setAttr -l on -k off ".tz";
	setAttr -l on -k off ".rx";
	setAttr -l on -k off ".ry";
	setAttr -l on -k off ".rz";
	setAttr -l on -k off ".sx";
	setAttr -l on -k off ".sy";
	setAttr -l on -k off ".sz";
	setAttr ".nts" -type "string" "['Nose_Base_Bnd_scaleConstraint1', 'Nose_Bridge_Bnd', 'Nose_Base_CtrlShape', 'Nose_Bridge_Jnt', 'Nose_Main_Ctrl_Offset_Grp', 'Nose_Bridge_Bnd_scaleConstraint1', 'Nose_Rig_Grp_scaleConstraint1', 'Nose_Bridge_CtrlShape', 'Nose_Bridge_Ctrl', 'Nose_Base_Ctrl', 'Nose_Base_Ctrl_Offset_Grp_scaleConstraint1', 'Nose_Base_Ctrl_Offset_Grp', 'Nose_Main_Bnd_scaleConstraint1', 'Nose_Base_Jnt', 'Nose_Main_Jnt_Ctrl_tag', 'Nose_Bridge_Ctrl_Offset_Grp', 'Nose_Bridge_Jnt_Ctrl_tag', 'Nose_Main_Bnd', 'Nose_Base_Ctrl_Offset_Grp_parentConstraint1', 'Nose_Main_Jnt', 'Nose_Base_Jnt_parentConstraint1', 'Nose_Base_Jnt_Ctrl_tag', 'Nose_Bridge_Bnd_parentConstraint1', 'Nose_Main_Jnt_parentConstraint1', 'Nose_Rig_Grp_parentConstraint1', 'Nose_Main_Bnd_parentConstraint1', 'Nose_Ctrl_Grp', 'Nose_Base_Bnd_parentConstraint1', 'Nose_Bridge_Jnt_parentConstraint1', 'Nose_Main_CtrlShape', 'Nose_Main_Ctrl', 'Nose_Base_Bnd', 'Nose_Rig_Grp']";
createNode joint -n "Nose_Base_Guide" -p "Nose_Block";
	rename -uid "82EBEBF0-4E3B-FCCE-E26A-A98A50E1DBD6";
	addAttr -ci true -sn "Helper" -ln "Helper" -min 0 -max 1 -en "Hide:Show" -at "enum";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2026/scripts/Mutant_Tools/Icons/";
	setAttr ".t" -type "double3" 1.8618739748205638e-15 180.740460889758 16.767461759738595 ;
	setAttr ".r" -type "double3" -90 -155.56648708689272 89.999999999999687 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr -cb on ".Helper" 1;
createNode nurbsCurve -n "Nose_Base_Guide_CtrlShape" -p "Nose_Base_Guide";
	rename -uid "B31797B7-41A1-BC07-B176-AEA548B3D47F";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2026/scripts/Mutant_Tools/Icons/";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".hpb" yes;
	setAttr ".ovc" 14;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 9 0 no 3
		10 0 1 2 3 4 5 6 7 8 9
		10
		1.3977299999999999e-05 -0.5 0.25
		1.3977299999999999e-05 0.94513100000000005 0.25591599999999998
		1.3977299999999999e-05 0.739653 0.50644299999999998
		1.3977299999999999e-05 0.99017999999999995 0.93915099999999996
		1.37985e-05 2.299302 3.8742999999999997e-07
		1.3977299999999999e-05 0.99018099999999998 -0.93915099999999996
		1.3977299999999999e-05 0.739653 -0.50644199999999995
		7.1674600000000002e-06 0.94513100000000005 -0.25322099999999997
		1.3977299999999999e-05 -0.5 -0.25
		1.3977299999999999e-05 -0.5 0.25
		;
createNode nurbsCurve -n "Nose_Base_Guide_Ctrl_CtrlShape" -p "Nose_Base_Guide";
	rename -uid "014BD4C0-4B3D-6F65-56CE-B1B920881DBB";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2026/scripts/Mutant_Tools/Icons/";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".hpb" yes;
	setAttr ".ovc" 18;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 101 0 no 3
		102 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27
		 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54
		 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81
		 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99 100 101
		102
		0 0.59420899999999999 0
		-3.0751100000000001e-09 0.58518199999999998 0.103183
		-6.0567700000000004e-09 0.55837400000000004 0.203232
		-8.8544099999999994e-09 0.51460099999999998 0.29710500000000001
		-1.1383e-08 0.45519100000000001 0.38195099999999998
		-1.3565700000000001e-08 0.38195000000000001 0.45519100000000001
		-1.5336300000000002e-08 0.29710500000000001 0.51460099999999998
		-1.6640900000000001e-08 0.203232 0.55837400000000004
		-1.7439800000000002e-08 0.103183 0.58518199999999998
		-1.7708799999999999e-08 0 0.59421000000000002
		-1.7439800000000002e-08 -0.103183 0.58518199999999998
		-1.6640900000000001e-08 -0.203232 0.55837400000000004
		-1.5336300000000002e-08 -0.29710500000000001 0.51460099999999998
		-1.3565700000000001e-08 -0.38195000000000001 0.45519100000000001
		-1.1383e-08 -0.45519100000000001 0.38195099999999998
		-8.8544099999999994e-09 -0.51460099999999998 0.29710500000000001
		-6.0567700000000004e-09 -0.55837400000000004 0.203232
		-3.0751100000000001e-09 -0.58518199999999998 0.103183
		0 -0.59420899999999999 0
		0 -0.58518199999999998 -0.103183
		0 -0.55837400000000004 -0.203232
		0 -0.51460099999999998 -0.29710500000000001
		0 -0.45519100000000001 -0.38195099999999998
		0 -0.38195000000000001 -0.45519100000000001
		0 -0.29710500000000001 -0.51460099999999998
		0 -0.203232 -0.55837499999999995
		0 -0.103183 -0.58518199999999998
		0 0 -0.59421000000000002
		0 0.103183 -0.58518199999999998
		0 0.203232 -0.55837499999999995
		0 0.29710500000000001 -0.51460099999999998
		0 0.38195000000000001 -0.45519100000000001
		0 0.45519100000000001 -0.38195099999999998
		0 0.51460099999999998 -0.29710500000000001
		0 0.55837400000000004 -0.203232
		0 0.58518199999999998 -0.103183
		0 0.59420899999999999 0
		0.103183 0.58518199999999998 0
		0.203232 0.55837400000000004 0
		0.29710500000000001 0.51460099999999998 0
		0.38195099999999998 0.45519100000000001 0
		0.45519100000000001 0.38195000000000001 0
		0.51460099999999998 0.29710500000000001 0
		0.55837400000000004 0.203232 0
		0.58518199999999998 0.103183 0
		0.59420899999999999 0 0
		0.58518199999999998 -0.103183 0
		0.55837400000000004 -0.203232 0
		0.51460099999999998 -0.29710500000000001 0
		0.45519100000000001 -0.38195000000000001 0
		0.38195099999999998 -0.45519100000000001 0
		0.29710500000000001 -0.51460099999999998 0
		0.203232 -0.55837400000000004 0
		0.103183 -0.58518199999999998 0
		0 -0.59420899999999999 0
		-0.103183 -0.58518199999999998 0
		-0.203232 -0.55837400000000004 0
		-0.29710500000000001 -0.51460099999999998 0
		-0.38195099999999998 -0.45519100000000001 0
		-0.45519100000000001 -0.38195000000000001 0
		-0.51460099999999998 -0.29710500000000001 0
		-0.55837400000000004 -0.203232 0
		-0.58518199999999998 -0.103183 0
		-0.59421000000000002 0 0
		-0.58518199999999998 0.103183 0
		-0.55837400000000004 0.203232 0
		-0.51460099999999998 0.29710500000000001 0
		-0.45519100000000001 0.38195000000000001 0
		-0.38195099999999998 0.45519100000000001 0
		-0.29710500000000001 0.51460099999999998 0
		-0.203232 0.55837400000000004 0
		-0.103183 0.58518199999999998 0
		0 0.59420899999999999 0
		-3.0751100000000001e-09 0.58518199999999998 0.103183
		-6.0567700000000004e-09 0.55837400000000004 0.203232
		-8.8544099999999994e-09 0.51460099999999998 0.29710500000000001
		-1.1383e-08 0.45519100000000001 0.38195099999999998
		-1.3565700000000001e-08 0.38195000000000001 0.45519100000000001
		-1.5336300000000002e-08 0.29710500000000001 0.51460099999999998
		-1.6640900000000001e-08 0.203232 0.55837400000000004
		-1.7439800000000002e-08 0.103183 0.58518199999999998
		-1.7708799999999999e-08 0 0.59421000000000002
		-0.18362100000000001 0 0.56512700000000005
		-0.34926800000000002 0 0.48072599999999999
		-0.48072599999999999 0 0.34926800000000002
		-0.56512700000000005 0 0.18362100000000001
		-0.59421000000000002 0 0
		-0.56512700000000005 0 -0.18362100000000001
		-0.48072599999999999 0 -0.34926800000000002
		-0.34926800000000002 0 -0.48072599999999999
		-0.18362100000000001 0 -0.56512700000000005
		0 0 -0.59421000000000002
		0.18362100000000001 0 -0.56512700000000005
		0.34926800000000002 0 -0.48072599999999999
		0.48072599999999999 0 -0.34926800000000002
		0.56512700000000005 0 -0.18362100000000001
		0.59420899999999999 0 0
		0.56512700000000005 0 0.18362100000000001
		0.48072599999999999 0 0.34926800000000002
		0.34926800000000002 0 0.48072599999999999
		0.18362100000000001 0 0.56512700000000005
		-1.7708799999999999e-08 0 0.59421000000000002
		;
createNode nurbsCurve -n "Nose_Base_Guide_Ctrl_Ctrl_CtrlShape" -p "Nose_Base_Guide";
	rename -uid "3EA7C390-42DA-6305-70DB-A396CE725602";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2026/scripts/Mutant_Tools/Icons/";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".hpb" yes;
	setAttr ".ovc" 13;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 9 0 no 3
		10 0 1 2 3 4 5 6 7 8 9
		10
		-0.5 -0.25 -1.3977299999999999e-05
		0.94513100000000005 -0.25591599999999998 -1.3977299999999999e-05
		0.739653 -0.50644299999999998 -1.3977299999999999e-05
		0.99017999999999995 -0.93915099999999996 -1.3977299999999999e-05
		2.299302 -3.8742999999999997e-07 -1.37985e-05
		0.99018099999999998 0.93915099999999996 -1.3977299999999999e-05
		0.739653 0.50644199999999995 -1.3977299999999999e-05
		0.94513100000000005 0.25322099999999997 -7.1674600000000002e-06
		-0.5 0.25 -1.3977299999999999e-05
		-0.5 -0.25 -1.3977299999999999e-05
		;
createNode nurbsCurve -n "Nose_Base_Guide_Ctrl_Ctrl_Ctrl_CtrlShape" -p "Nose_Base_Guide";
	rename -uid "4E18B3E2-4A6D-C700-C742-50BC23D9DA6A";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2026/scripts/Mutant_Tools/Icons/";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".hpb" yes;
	setAttr ".ovc" 6;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 9 0 no 3
		10 0 1 2 3 4 5 6 7 8 9
		10
		0.25 1.3977299999999999e-05 -0.5
		0.25591599999999998 1.3977299999999999e-05 0.94513100000000005
		0.50644299999999998 1.3977299999999999e-05 0.739653
		0.93915099999999996 1.3977299999999999e-05 0.99017999999999995
		3.8742999999999997e-07 1.37985e-05 2.299302
		-0.93915099999999996 1.3977299999999999e-05 0.99018099999999998
		-0.50644199999999995 1.3977299999999999e-05 0.739653
		-0.25322099999999997 7.1674600000000002e-06 0.94513100000000005
		-0.25 1.3977299999999999e-05 -0.5
		0.25 1.3977299999999999e-05 -0.5
		;
createNode joint -n "Nose_Bridge_Guide" -p "Nose_Base_Guide";
	rename -uid "1F9BF420-4D6B-EAEA-351D-869D50A7E3B5";
	addAttr -ci true -sn "Helper" -ln "Helper" -min 0 -max 1 -en "Hide:Show" -at "enum";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2026/scripts/Mutant_Tools/Icons/";
	setAttr ".t" -type "double3" 3.9111667150672078 2.7117197376469448e-14 -1.0880372778549801e-16 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr -cb on ".Helper" 1;
createNode nurbsCurve -n "Nose_Bridge_Guide_CtrlShape" -p "Nose_Bridge_Guide";
	rename -uid "43CDAC67-42C1-4A2C-A220-40B02205F522";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2026/scripts/Mutant_Tools/Icons/";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".hpb" yes;
	setAttr ".ovc" 14;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 9 0 no 3
		10 0 1 2 3 4 5 6 7 8 9
		10
		1.3977299999999999e-05 -0.5 0.25
		1.3977299999999999e-05 0.94513100000000005 0.25591599999999998
		1.3977299999999999e-05 0.739653 0.50644299999999998
		1.3977299999999999e-05 0.99017999999999995 0.93915099999999996
		1.37985e-05 2.299302 3.8742999999999997e-07
		1.3977299999999999e-05 0.99018099999999998 -0.93915099999999996
		1.3977299999999999e-05 0.739653 -0.50644199999999995
		7.1674600000000002e-06 0.94513100000000005 -0.25322099999999997
		1.3977299999999999e-05 -0.5 -0.25
		1.3977299999999999e-05 -0.5 0.25
		;
createNode nurbsCurve -n "Nose_Bridge_Guide_Ctrl_CtrlShape" -p "Nose_Bridge_Guide";
	rename -uid "63BBA561-4392-C003-5C87-ED92932ED8BF";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2026/scripts/Mutant_Tools/Icons/";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".hpb" yes;
	setAttr ".ovc" 18;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 101 0 no 3
		102 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27
		 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54
		 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81
		 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99 100 101
		102
		0 0.59420899999999999 0
		-3.0751100000000001e-09 0.58518199999999998 0.103183
		-6.0567700000000004e-09 0.55837400000000004 0.203232
		-8.8544099999999994e-09 0.51460099999999998 0.29710500000000001
		-1.1383e-08 0.45519100000000001 0.38195099999999998
		-1.3565700000000001e-08 0.38195000000000001 0.45519100000000001
		-1.5336300000000002e-08 0.29710500000000001 0.51460099999999998
		-1.6640900000000001e-08 0.203232 0.55837400000000004
		-1.7439800000000002e-08 0.103183 0.58518199999999998
		-1.7708799999999999e-08 0 0.59421000000000002
		-1.7439800000000002e-08 -0.103183 0.58518199999999998
		-1.6640900000000001e-08 -0.203232 0.55837400000000004
		-1.5336300000000002e-08 -0.29710500000000001 0.51460099999999998
		-1.3565700000000001e-08 -0.38195000000000001 0.45519100000000001
		-1.1383e-08 -0.45519100000000001 0.38195099999999998
		-8.8544099999999994e-09 -0.51460099999999998 0.29710500000000001
		-6.0567700000000004e-09 -0.55837400000000004 0.203232
		-3.0751100000000001e-09 -0.58518199999999998 0.103183
		0 -0.59420899999999999 0
		0 -0.58518199999999998 -0.103183
		0 -0.55837400000000004 -0.203232
		0 -0.51460099999999998 -0.29710500000000001
		0 -0.45519100000000001 -0.38195099999999998
		0 -0.38195000000000001 -0.45519100000000001
		0 -0.29710500000000001 -0.51460099999999998
		0 -0.203232 -0.55837499999999995
		0 -0.103183 -0.58518199999999998
		0 0 -0.59421000000000002
		0 0.103183 -0.58518199999999998
		0 0.203232 -0.55837499999999995
		0 0.29710500000000001 -0.51460099999999998
		0 0.38195000000000001 -0.45519100000000001
		0 0.45519100000000001 -0.38195099999999998
		0 0.51460099999999998 -0.29710500000000001
		0 0.55837400000000004 -0.203232
		0 0.58518199999999998 -0.103183
		0 0.59420899999999999 0
		0.103183 0.58518199999999998 0
		0.203232 0.55837400000000004 0
		0.29710500000000001 0.51460099999999998 0
		0.38195099999999998 0.45519100000000001 0
		0.45519100000000001 0.38195000000000001 0
		0.51460099999999998 0.29710500000000001 0
		0.55837400000000004 0.203232 0
		0.58518199999999998 0.103183 0
		0.59420899999999999 0 0
		0.58518199999999998 -0.103183 0
		0.55837400000000004 -0.203232 0
		0.51460099999999998 -0.29710500000000001 0
		0.45519100000000001 -0.38195000000000001 0
		0.38195099999999998 -0.45519100000000001 0
		0.29710500000000001 -0.51460099999999998 0
		0.203232 -0.55837400000000004 0
		0.103183 -0.58518199999999998 0
		0 -0.59420899999999999 0
		-0.103183 -0.58518199999999998 0
		-0.203232 -0.55837400000000004 0
		-0.29710500000000001 -0.51460099999999998 0
		-0.38195099999999998 -0.45519100000000001 0
		-0.45519100000000001 -0.38195000000000001 0
		-0.51460099999999998 -0.29710500000000001 0
		-0.55837400000000004 -0.203232 0
		-0.58518199999999998 -0.103183 0
		-0.59421000000000002 0 0
		-0.58518199999999998 0.103183 0
		-0.55837400000000004 0.203232 0
		-0.51460099999999998 0.29710500000000001 0
		-0.45519100000000001 0.38195000000000001 0
		-0.38195099999999998 0.45519100000000001 0
		-0.29710500000000001 0.51460099999999998 0
		-0.203232 0.55837400000000004 0
		-0.103183 0.58518199999999998 0
		0 0.59420899999999999 0
		-3.0751100000000001e-09 0.58518199999999998 0.103183
		-6.0567700000000004e-09 0.55837400000000004 0.203232
		-8.8544099999999994e-09 0.51460099999999998 0.29710500000000001
		-1.1383e-08 0.45519100000000001 0.38195099999999998
		-1.3565700000000001e-08 0.38195000000000001 0.45519100000000001
		-1.5336300000000002e-08 0.29710500000000001 0.51460099999999998
		-1.6640900000000001e-08 0.203232 0.55837400000000004
		-1.7439800000000002e-08 0.103183 0.58518199999999998
		-1.7708799999999999e-08 0 0.59421000000000002
		-0.18362100000000001 0 0.56512700000000005
		-0.34926800000000002 0 0.48072599999999999
		-0.48072599999999999 0 0.34926800000000002
		-0.56512700000000005 0 0.18362100000000001
		-0.59421000000000002 0 0
		-0.56512700000000005 0 -0.18362100000000001
		-0.48072599999999999 0 -0.34926800000000002
		-0.34926800000000002 0 -0.48072599999999999
		-0.18362100000000001 0 -0.56512700000000005
		0 0 -0.59421000000000002
		0.18362100000000001 0 -0.56512700000000005
		0.34926800000000002 0 -0.48072599999999999
		0.48072599999999999 0 -0.34926800000000002
		0.56512700000000005 0 -0.18362100000000001
		0.59420899999999999 0 0
		0.56512700000000005 0 0.18362100000000001
		0.48072599999999999 0 0.34926800000000002
		0.34926800000000002 0 0.48072599999999999
		0.18362100000000001 0 0.56512700000000005
		-1.7708799999999999e-08 0 0.59421000000000002
		;
createNode nurbsCurve -n "Nose_Bridge_Guide_Ctrl_Ctrl_CtrlShape" -p "Nose_Bridge_Guide";
	rename -uid "1D0D4634-408F-05FA-A191-27B4F1EDCC2B";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2026/scripts/Mutant_Tools/Icons/";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".hpb" yes;
	setAttr ".ovc" 13;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 9 0 no 3
		10 0 1 2 3 4 5 6 7 8 9
		10
		-0.5 -0.25 -1.3977299999999999e-05
		0.94513100000000005 -0.25591599999999998 -1.3977299999999999e-05
		0.739653 -0.50644299999999998 -1.3977299999999999e-05
		0.99017999999999995 -0.93915099999999996 -1.3977299999999999e-05
		2.299302 -3.8742999999999997e-07 -1.37985e-05
		0.99018099999999998 0.93915099999999996 -1.3977299999999999e-05
		0.739653 0.50644199999999995 -1.3977299999999999e-05
		0.94513100000000005 0.25322099999999997 -7.1674600000000002e-06
		-0.5 0.25 -1.3977299999999999e-05
		-0.5 -0.25 -1.3977299999999999e-05
		;
createNode nurbsCurve -n "Nose_Bridge_Guide_Ctrl_Ctrl_Ctrl_CtrlShape" -p "Nose_Bridge_Guide";
	rename -uid "117F2AE9-4A71-B02D-9D07-648E6F6F9D75";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2026/scripts/Mutant_Tools/Icons/";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".hpb" yes;
	setAttr ".ovc" 6;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 9 0 no 3
		10 0 1 2 3 4 5 6 7 8 9
		10
		0.25 1.3977299999999999e-05 -0.5
		0.25591599999999998 1.3977299999999999e-05 0.94513100000000005
		0.50644299999999998 1.3977299999999999e-05 0.739653
		0.93915099999999996 1.3977299999999999e-05 0.99017999999999995
		3.8742999999999997e-07 1.37985e-05 2.299302
		-0.93915099999999996 1.3977299999999999e-05 0.99018099999999998
		-0.50644199999999995 1.3977299999999999e-05 0.739653
		-0.25322099999999997 7.1674600000000002e-06 0.94513100000000005
		-0.25 1.3977299999999999e-05 -0.5
		0.25 1.3977299999999999e-05 -0.5
		;
createNode joint -n "Nose_Main_Guide" -p "Nose_Bridge_Guide";
	rename -uid "3D50B782-4E82-F3F0-2855-98AE5E402F50";
	addAttr -ci true -sn "Helper" -ln "Helper" -min 0 -max 1 -en "Hide:Show" -at "enum";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2026/scripts/Mutant_Tools/Icons/";
	setAttr ".t" -type "double3" 2.3571481468482349 2.6700863742235015e-14 -1.8137593040907614e-16 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr -cb on ".Helper" 1;
createNode nurbsCurve -n "Nose_Main_Guide_CtrlShape" -p "Nose_Main_Guide";
	rename -uid "BC31952E-48C5-CD43-E6B2-94B63A9908AC";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2026/scripts/Mutant_Tools/Icons/";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".hpb" yes;
	setAttr ".ovc" 14;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 9 0 no 3
		10 0 1 2 3 4 5 6 7 8 9
		10
		1.3977299999999999e-05 -0.5 0.25
		1.3977299999999999e-05 0.94513100000000005 0.25591599999999998
		1.3977299999999999e-05 0.739653 0.50644299999999998
		1.3977299999999999e-05 0.99017999999999995 0.93915099999999996
		1.37985e-05 2.299302 3.8742999999999997e-07
		1.3977299999999999e-05 0.99018099999999998 -0.93915099999999996
		1.3977299999999999e-05 0.739653 -0.50644199999999995
		7.1674600000000002e-06 0.94513100000000005 -0.25322099999999997
		1.3977299999999999e-05 -0.5 -0.25
		1.3977299999999999e-05 -0.5 0.25
		;
createNode nurbsCurve -n "Nose_Main_Guide_Ctrl_CtrlShape" -p "Nose_Main_Guide";
	rename -uid "B3B70A10-4CCE-D97E-8D13-549F04975F49";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2026/scripts/Mutant_Tools/Icons/";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".hpb" yes;
	setAttr ".ovc" 18;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 101 0 no 3
		102 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27
		 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54
		 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81
		 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99 100 101
		102
		0 0.59420899999999999 0
		-3.0751100000000001e-09 0.58518199999999998 0.103183
		-6.0567700000000004e-09 0.55837400000000004 0.203232
		-8.8544099999999994e-09 0.51460099999999998 0.29710500000000001
		-1.1383e-08 0.45519100000000001 0.38195099999999998
		-1.3565700000000001e-08 0.38195000000000001 0.45519100000000001
		-1.5336300000000002e-08 0.29710500000000001 0.51460099999999998
		-1.6640900000000001e-08 0.203232 0.55837400000000004
		-1.7439800000000002e-08 0.103183 0.58518199999999998
		-1.7708799999999999e-08 0 0.59421000000000002
		-1.7439800000000002e-08 -0.103183 0.58518199999999998
		-1.6640900000000001e-08 -0.203232 0.55837400000000004
		-1.5336300000000002e-08 -0.29710500000000001 0.51460099999999998
		-1.3565700000000001e-08 -0.38195000000000001 0.45519100000000001
		-1.1383e-08 -0.45519100000000001 0.38195099999999998
		-8.8544099999999994e-09 -0.51460099999999998 0.29710500000000001
		-6.0567700000000004e-09 -0.55837400000000004 0.203232
		-3.0751100000000001e-09 -0.58518199999999998 0.103183
		0 -0.59420899999999999 0
		0 -0.58518199999999998 -0.103183
		0 -0.55837400000000004 -0.203232
		0 -0.51460099999999998 -0.29710500000000001
		0 -0.45519100000000001 -0.38195099999999998
		0 -0.38195000000000001 -0.45519100000000001
		0 -0.29710500000000001 -0.51460099999999998
		0 -0.203232 -0.55837499999999995
		0 -0.103183 -0.58518199999999998
		0 0 -0.59421000000000002
		0 0.103183 -0.58518199999999998
		0 0.203232 -0.55837499999999995
		0 0.29710500000000001 -0.51460099999999998
		0 0.38195000000000001 -0.45519100000000001
		0 0.45519100000000001 -0.38195099999999998
		0 0.51460099999999998 -0.29710500000000001
		0 0.55837400000000004 -0.203232
		0 0.58518199999999998 -0.103183
		0 0.59420899999999999 0
		0.103183 0.58518199999999998 0
		0.203232 0.55837400000000004 0
		0.29710500000000001 0.51460099999999998 0
		0.38195099999999998 0.45519100000000001 0
		0.45519100000000001 0.38195000000000001 0
		0.51460099999999998 0.29710500000000001 0
		0.55837400000000004 0.203232 0
		0.58518199999999998 0.103183 0
		0.59420899999999999 0 0
		0.58518199999999998 -0.103183 0
		0.55837400000000004 -0.203232 0
		0.51460099999999998 -0.29710500000000001 0
		0.45519100000000001 -0.38195000000000001 0
		0.38195099999999998 -0.45519100000000001 0
		0.29710500000000001 -0.51460099999999998 0
		0.203232 -0.55837400000000004 0
		0.103183 -0.58518199999999998 0
		0 -0.59420899999999999 0
		-0.103183 -0.58518199999999998 0
		-0.203232 -0.55837400000000004 0
		-0.29710500000000001 -0.51460099999999998 0
		-0.38195099999999998 -0.45519100000000001 0
		-0.45519100000000001 -0.38195000000000001 0
		-0.51460099999999998 -0.29710500000000001 0
		-0.55837400000000004 -0.203232 0
		-0.58518199999999998 -0.103183 0
		-0.59421000000000002 0 0
		-0.58518199999999998 0.103183 0
		-0.55837400000000004 0.203232 0
		-0.51460099999999998 0.29710500000000001 0
		-0.45519100000000001 0.38195000000000001 0
		-0.38195099999999998 0.45519100000000001 0
		-0.29710500000000001 0.51460099999999998 0
		-0.203232 0.55837400000000004 0
		-0.103183 0.58518199999999998 0
		0 0.59420899999999999 0
		-3.0751100000000001e-09 0.58518199999999998 0.103183
		-6.0567700000000004e-09 0.55837400000000004 0.203232
		-8.8544099999999994e-09 0.51460099999999998 0.29710500000000001
		-1.1383e-08 0.45519100000000001 0.38195099999999998
		-1.3565700000000001e-08 0.38195000000000001 0.45519100000000001
		-1.5336300000000002e-08 0.29710500000000001 0.51460099999999998
		-1.6640900000000001e-08 0.203232 0.55837400000000004
		-1.7439800000000002e-08 0.103183 0.58518199999999998
		-1.7708799999999999e-08 0 0.59421000000000002
		-0.18362100000000001 0 0.56512700000000005
		-0.34926800000000002 0 0.48072599999999999
		-0.48072599999999999 0 0.34926800000000002
		-0.56512700000000005 0 0.18362100000000001
		-0.59421000000000002 0 0
		-0.56512700000000005 0 -0.18362100000000001
		-0.48072599999999999 0 -0.34926800000000002
		-0.34926800000000002 0 -0.48072599999999999
		-0.18362100000000001 0 -0.56512700000000005
		0 0 -0.59421000000000002
		0.18362100000000001 0 -0.56512700000000005
		0.34926800000000002 0 -0.48072599999999999
		0.48072599999999999 0 -0.34926800000000002
		0.56512700000000005 0 -0.18362100000000001
		0.59420899999999999 0 0
		0.56512700000000005 0 0.18362100000000001
		0.48072599999999999 0 0.34926800000000002
		0.34926800000000002 0 0.48072599999999999
		0.18362100000000001 0 0.56512700000000005
		-1.7708799999999999e-08 0 0.59421000000000002
		;
createNode nurbsCurve -n "Nose_Main_Guide_Ctrl_Ctrl_CtrlShape" -p "Nose_Main_Guide";
	rename -uid "84273D49-4960-D0E3-85F8-2E938E998BA5";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2026/scripts/Mutant_Tools/Icons/";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".hpb" yes;
	setAttr ".ovc" 13;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 9 0 no 3
		10 0 1 2 3 4 5 6 7 8 9
		10
		-0.5 -0.25 -1.3977299999999999e-05
		0.94513100000000005 -0.25591599999999998 -1.3977299999999999e-05
		0.739653 -0.50644299999999998 -1.3977299999999999e-05
		0.99017999999999995 -0.93915099999999996 -1.3977299999999999e-05
		2.299302 -3.8742999999999997e-07 -1.37985e-05
		0.99018099999999998 0.93915099999999996 -1.3977299999999999e-05
		0.739653 0.50644199999999995 -1.3977299999999999e-05
		0.94513100000000005 0.25322099999999997 -7.1674600000000002e-06
		-0.5 0.25 -1.3977299999999999e-05
		-0.5 -0.25 -1.3977299999999999e-05
		;
createNode nurbsCurve -n "Nose_Main_Guide_Ctrl_Ctrl_Ctrl_CtrlShape" -p "Nose_Main_Guide";
	rename -uid "D4BE9872-49F5-5976-585B-508F147118A4";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2026/scripts/Mutant_Tools/Icons/";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".hpb" yes;
	setAttr ".ovc" 6;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 9 0 no 3
		10 0 1 2 3 4 5 6 7 8 9
		10
		0.25 1.3977299999999999e-05 -0.5
		0.25591599999999998 1.3977299999999999e-05 0.94513100000000005
		0.50644299999999998 1.3977299999999999e-05 0.739653
		0.93915099999999996 1.3977299999999999e-05 0.99017999999999995
		3.8742999999999997e-07 1.37985e-05 2.299302
		-0.93915099999999996 1.3977299999999999e-05 0.99018099999999998
		-0.50644199999999995 1.3977299999999999e-05 0.739653
		-0.25322099999999997 7.1674600000000002e-06 0.94513100000000005
		-0.25 1.3977299999999999e-05 -0.5
		0.25 1.3977299999999999e-05 -0.5
		;
createNode dagContainer -n "L_Nostril_Block" -p "Face";
	rename -uid "DA1A6FBC-4FF8-1F03-7003-B2BA7E3D62D2";
	addAttr -ci true -sn "nts" -ln "notes" -dt "string";
	setAttr ".isc" yes;
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2026/scripts/Mutant_Tools/Icons/Chain.png";
	setAttr ".ctor" -type "string" "rodri";
	setAttr ".cdat" -type "string" "2025/12/06 13:26:49";
	setAttr -l on -k off ".v";
	setAttr -l on -k off ".tx";
	setAttr -l on -k off ".ty";
	setAttr -l on -k off ".tz";
	setAttr -l on -k off ".rx";
	setAttr -l on -k off ".ry";
	setAttr -l on -k off ".rz";
	setAttr -l on -k off ".sx";
	setAttr -l on -k off ".sy";
	setAttr -l on -k off ".sz";
	setAttr ".nts" -type "string" "['L_Nostril_A_Ctrl_Offset_Grp_scaleConstraint1', 'R_Nostril_A_Bnd_parentConstraint1', 'L_Nostril_Rig_Grp', 'R_Nostril_A_Bnd_scaleConstraint1', 'L_Nostril_A_Ctrl', 'L_Nostril_A_Bnd_parentConstraint1', 'R_Nostril_A_Jnt_Ctrl_tag', 'L_Nostril_Rig_Grp_parentConstraint1', 'R_Nostril_A_Jnt', 'L_Nostril_A_Ctrl_Offset_Grp', 'L_Nostril_A_Bnd', 'L_Nostril_A_CtrlShape', 'R_Nostril_A_Ctrl_Offset_GrpMirror_Grp_scaleConstraint1', 'R_Nostril_A_Jnt_parentConstraint1', 'R_Nostril_A_CtrlShape', 'L_Nostril_A_Jnt_Ctrl_tag', 'R_Nostril_A_Ctrl', 'L_Nostril_Ctrl_Grp', 'R_Nostril_A_Ctrl_Offset_GrpMirror_Grp', 'L_Nostril_Rig_Grp_scaleConstraint1', 'L_Nostril_A_Jnt', 'L_Nostril_A_Bnd_scaleConstraint1', 'R_Nostril_A_Ctrl_Offset_Grp', 'R_Nostril_A_Ctrl_Offset_GrpMirror_Grp_parentConstraint1', 'L_Nostril_A_Jnt_parentConstraint1', 'L_Nostril_A_Ctrl_Offset_Grp_parentConstraint1', 'R_Nostril_A_Bnd']";
createNode joint -n "L_Nostril_A_Guide" -p "L_Nostril_Block";
	rename -uid "93887CF9-4CB3-16B3-FDEA-88BE4898C74A";
	addAttr -ci true -sn "Helper" -ln "Helper" -min 0 -max 1 -en "Hide:Show" -at "enum";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2026/scripts/Mutant_Tools/Icons/";
	setAttr ".t" -type "double3" 3.0058220624923706 174.99281729999257 17.225582122802734 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr -cb on ".Helper" 1;
createNode nurbsCurve -n "L_Nostril_A_Guide_CtrlShape" -p "L_Nostril_A_Guide";
	rename -uid "97838DEB-41D0-47D2-79D9-868BB88D9D93";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2026/scripts/Mutant_Tools/Icons/";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".hpb" yes;
	setAttr ".ovc" 14;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 9 0 no 3
		10 0 1 2 3 4 5 6 7 8 9
		10
		1.3977299999999999e-05 -0.5 0.25
		1.3977299999999999e-05 0.94513100000000005 0.25591599999999998
		1.3977299999999999e-05 0.739653 0.50644299999999998
		1.3977299999999999e-05 0.99017999999999995 0.93915099999999996
		1.37985e-05 2.299302 3.8742999999999997e-07
		1.3977299999999999e-05 0.99018099999999998 -0.93915099999999996
		1.3977299999999999e-05 0.739653 -0.50644199999999995
		7.1674600000000002e-06 0.94513100000000005 -0.25322099999999997
		1.3977299999999999e-05 -0.5 -0.25
		1.3977299999999999e-05 -0.5 0.25
		;
createNode nurbsCurve -n "L_Nostril_A_Guide_Ctrl_CtrlShape" -p "L_Nostril_A_Guide";
	rename -uid "FE4EC223-4E43-81F3-70FB-5385F2553B0D";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2026/scripts/Mutant_Tools/Icons/";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".hpb" yes;
	setAttr ".ovc" 18;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 101 0 no 3
		102 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27
		 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54
		 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81
		 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99 100 101
		102
		0 0.59420899999999999 0
		-3.0751100000000001e-09 0.58518199999999998 0.103183
		-6.0567700000000004e-09 0.55837400000000004 0.203232
		-8.8544099999999994e-09 0.51460099999999998 0.29710500000000001
		-1.1383e-08 0.45519100000000001 0.38195099999999998
		-1.3565700000000001e-08 0.38195000000000001 0.45519100000000001
		-1.5336300000000002e-08 0.29710500000000001 0.51460099999999998
		-1.6640900000000001e-08 0.203232 0.55837400000000004
		-1.7439800000000002e-08 0.103183 0.58518199999999998
		-1.7708799999999999e-08 0 0.59421000000000002
		-1.7439800000000002e-08 -0.103183 0.58518199999999998
		-1.6640900000000001e-08 -0.203232 0.55837400000000004
		-1.5336300000000002e-08 -0.29710500000000001 0.51460099999999998
		-1.3565700000000001e-08 -0.38195000000000001 0.45519100000000001
		-1.1383e-08 -0.45519100000000001 0.38195099999999998
		-8.8544099999999994e-09 -0.51460099999999998 0.29710500000000001
		-6.0567700000000004e-09 -0.55837400000000004 0.203232
		-3.0751100000000001e-09 -0.58518199999999998 0.103183
		0 -0.59420899999999999 0
		0 -0.58518199999999998 -0.103183
		0 -0.55837400000000004 -0.203232
		0 -0.51460099999999998 -0.29710500000000001
		0 -0.45519100000000001 -0.38195099999999998
		0 -0.38195000000000001 -0.45519100000000001
		0 -0.29710500000000001 -0.51460099999999998
		0 -0.203232 -0.55837499999999995
		0 -0.103183 -0.58518199999999998
		0 0 -0.59421000000000002
		0 0.103183 -0.58518199999999998
		0 0.203232 -0.55837499999999995
		0 0.29710500000000001 -0.51460099999999998
		0 0.38195000000000001 -0.45519100000000001
		0 0.45519100000000001 -0.38195099999999998
		0 0.51460099999999998 -0.29710500000000001
		0 0.55837400000000004 -0.203232
		0 0.58518199999999998 -0.103183
		0 0.59420899999999999 0
		0.103183 0.58518199999999998 0
		0.203232 0.55837400000000004 0
		0.29710500000000001 0.51460099999999998 0
		0.38195099999999998 0.45519100000000001 0
		0.45519100000000001 0.38195000000000001 0
		0.51460099999999998 0.29710500000000001 0
		0.55837400000000004 0.203232 0
		0.58518199999999998 0.103183 0
		0.59420899999999999 0 0
		0.58518199999999998 -0.103183 0
		0.55837400000000004 -0.203232 0
		0.51460099999999998 -0.29710500000000001 0
		0.45519100000000001 -0.38195000000000001 0
		0.38195099999999998 -0.45519100000000001 0
		0.29710500000000001 -0.51460099999999998 0
		0.203232 -0.55837400000000004 0
		0.103183 -0.58518199999999998 0
		0 -0.59420899999999999 0
		-0.103183 -0.58518199999999998 0
		-0.203232 -0.55837400000000004 0
		-0.29710500000000001 -0.51460099999999998 0
		-0.38195099999999998 -0.45519100000000001 0
		-0.45519100000000001 -0.38195000000000001 0
		-0.51460099999999998 -0.29710500000000001 0
		-0.55837400000000004 -0.203232 0
		-0.58518199999999998 -0.103183 0
		-0.59421000000000002 0 0
		-0.58518199999999998 0.103183 0
		-0.55837400000000004 0.203232 0
		-0.51460099999999998 0.29710500000000001 0
		-0.45519100000000001 0.38195000000000001 0
		-0.38195099999999998 0.45519100000000001 0
		-0.29710500000000001 0.51460099999999998 0
		-0.203232 0.55837400000000004 0
		-0.103183 0.58518199999999998 0
		0 0.59420899999999999 0
		-3.0751100000000001e-09 0.58518199999999998 0.103183
		-6.0567700000000004e-09 0.55837400000000004 0.203232
		-8.8544099999999994e-09 0.51460099999999998 0.29710500000000001
		-1.1383e-08 0.45519100000000001 0.38195099999999998
		-1.3565700000000001e-08 0.38195000000000001 0.45519100000000001
		-1.5336300000000002e-08 0.29710500000000001 0.51460099999999998
		-1.6640900000000001e-08 0.203232 0.55837400000000004
		-1.7439800000000002e-08 0.103183 0.58518199999999998
		-1.7708799999999999e-08 0 0.59421000000000002
		-0.18362100000000001 0 0.56512700000000005
		-0.34926800000000002 0 0.48072599999999999
		-0.48072599999999999 0 0.34926800000000002
		-0.56512700000000005 0 0.18362100000000001
		-0.59421000000000002 0 0
		-0.56512700000000005 0 -0.18362100000000001
		-0.48072599999999999 0 -0.34926800000000002
		-0.34926800000000002 0 -0.48072599999999999
		-0.18362100000000001 0 -0.56512700000000005
		0 0 -0.59421000000000002
		0.18362100000000001 0 -0.56512700000000005
		0.34926800000000002 0 -0.48072599999999999
		0.48072599999999999 0 -0.34926800000000002
		0.56512700000000005 0 -0.18362100000000001
		0.59420899999999999 0 0
		0.56512700000000005 0 0.18362100000000001
		0.48072599999999999 0 0.34926800000000002
		0.34926800000000002 0 0.48072599999999999
		0.18362100000000001 0 0.56512700000000005
		-1.7708799999999999e-08 0 0.59421000000000002
		;
createNode nurbsCurve -n "L_Nostril_A_Guide_Ctrl_Ctrl_CtrlShape" -p "L_Nostril_A_Guide";
	rename -uid "A56B64A0-406B-5D2A-8A23-048944151CC7";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2026/scripts/Mutant_Tools/Icons/";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".hpb" yes;
	setAttr ".ovc" 13;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 9 0 no 3
		10 0 1 2 3 4 5 6 7 8 9
		10
		-0.5 -0.25 -1.3977299999999999e-05
		0.94513100000000005 -0.25591599999999998 -1.3977299999999999e-05
		0.739653 -0.50644299999999998 -1.3977299999999999e-05
		0.99017999999999995 -0.93915099999999996 -1.3977299999999999e-05
		2.299302 -3.8742999999999997e-07 -1.37985e-05
		0.99018099999999998 0.93915099999999996 -1.3977299999999999e-05
		0.739653 0.50644199999999995 -1.3977299999999999e-05
		0.94513100000000005 0.25322099999999997 -7.1674600000000002e-06
		-0.5 0.25 -1.3977299999999999e-05
		-0.5 -0.25 -1.3977299999999999e-05
		;
createNode nurbsCurve -n "L_Nostril_A_Guide_Ctrl_Ctrl_Ctrl_CtrlShape" -p "L_Nostril_A_Guide";
	rename -uid "F385B24D-4EE4-0940-B58E-EDAD03572279";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2026/scripts/Mutant_Tools/Icons/";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".hpb" yes;
	setAttr ".ovc" 6;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 9 0 no 3
		10 0 1 2 3 4 5 6 7 8 9
		10
		0.25 1.3977299999999999e-05 -0.5
		0.25591599999999998 1.3977299999999999e-05 0.94513100000000005
		0.50644299999999998 1.3977299999999999e-05 0.739653
		0.93915099999999996 1.3977299999999999e-05 0.99017999999999995
		3.8742999999999997e-07 1.37985e-05 2.299302
		-0.93915099999999996 1.3977299999999999e-05 0.99018099999999998
		-0.50644199999999995 1.3977299999999999e-05 0.739653
		-0.25322099999999997 7.1674600000000002e-06 0.94513100000000005
		-0.25 1.3977299999999999e-05 -0.5
		0.25 1.3977299999999999e-05 -0.5
		;
createNode dagContainer -n "L_Cheek_Block" -p "Face";
	rename -uid "8B8C0CA7-4CD7-1F81-E98C-EAB5841BBFC1";
	addAttr -ci true -sn "nts" -ln "notes" -dt "string";
	setAttr ".isc" yes;
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2026/scripts/Mutant_Tools/Icons/Chain.png";
	setAttr ".ctor" -type "string" "rodri";
	setAttr ".cdat" -type "string" "2025/12/06 13:30:44";
	setAttr -l on -k off ".v";
	setAttr -l on -k off ".tx";
	setAttr -l on -k off ".ty";
	setAttr -l on -k off ".tz";
	setAttr -l on -k off ".rx";
	setAttr -l on -k off ".ry";
	setAttr -l on -k off ".rz";
	setAttr -l on -k off ".sx";
	setAttr -l on -k off ".sy";
	setAttr -l on -k off ".sz";
	setAttr ".nts" -type "string" "['L_Cheek_A_Bnd_scaleConstraint1', 'L_Cheek_Rig_Grp_scaleConstraint1', 'R_Cheek_A_Bnd', 'R_Cheek_A_Jnt_parentConstraint1', 'R_Cheek_A_Jnt_Ctrl_tag', 'L_Cheek_A_Ctrl_Offset_Grp_scaleConstraint1', 'L_Cheek_A_Ctrl', 'R_Cheek_A_CtrlShape', 'R_Cheek_A_Bnd_scaleConstraint1', 'R_Cheek_A_Ctrl_Offset_GrpMirror_Grp', 'R_Cheek_A_Ctrl_Offset_GrpMirror_Grp_parentConstraint1', 'L_Cheek_A_Bnd_parentConstraint1', 'L_Cheek_Rig_Grp_parentConstraint1', 'L_Cheek_A_Ctrl_Offset_Grp_parentConstraint1', 'R_Cheek_A_Ctrl_Offset_Grp', 'L_Cheek_A_Bnd', 'R_Cheek_A_Ctrl_Offset_GrpMirror_Grp_scaleConstraint1', 'R_Cheek_A_Ctrl', 'L_Cheek_A_Jnt_Ctrl_tag', 'L_Cheek_A_CtrlShape', 'L_Cheek_A_Ctrl_Offset_Grp', 'L_Cheek_A_Jnt_parentConstraint1', 'R_Cheek_A_Jnt', 'L_Cheek_A_Jnt', 'R_Cheek_A_Bnd_parentConstraint1', 'L_Cheek_Rig_Grp', 'L_Cheek_Ctrl_Grp']";
createNode joint -n "L_Cheek_A_Guide" -p "L_Cheek_Block";
	rename -uid "9E48EF6F-4851-4372-0952-DEB691CE79F3";
	addAttr -ci true -sn "Helper" -ln "Helper" -min 0 -max 1 -en "Hide:Show" -at "enum";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2026/scripts/Mutant_Tools/Icons/";
	setAttr ".t" -type "double3" 7.6336706627396271 171.18242913540789 10.063194724874659 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr -cb on ".Helper" 1;
createNode nurbsCurve -n "L_Cheek_A_Guide_CtrlShape" -p "L_Cheek_A_Guide";
	rename -uid "0310F3FB-40C1-FE80-07DA-B6A9E77353BF";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2026/scripts/Mutant_Tools/Icons/";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".hpb" yes;
	setAttr ".ovc" 14;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 9 0 no 3
		10 0 1 2 3 4 5 6 7 8 9
		10
		1.3977299999999999e-05 -0.5 0.25
		1.3977299999999999e-05 0.94513100000000005 0.25591599999999998
		1.3977299999999999e-05 0.739653 0.50644299999999998
		1.3977299999999999e-05 0.99017999999999995 0.93915099999999996
		1.37985e-05 2.299302 3.8742999999999997e-07
		1.3977299999999999e-05 0.99018099999999998 -0.93915099999999996
		1.3977299999999999e-05 0.739653 -0.50644199999999995
		7.1674600000000002e-06 0.94513100000000005 -0.25322099999999997
		1.3977299999999999e-05 -0.5 -0.25
		1.3977299999999999e-05 -0.5 0.25
		;
createNode nurbsCurve -n "L_Cheek_A_Guide_Ctrl_CtrlShape" -p "L_Cheek_A_Guide";
	rename -uid "B1D4EE05-4C90-D380-0B0D-F49E27468DAC";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2026/scripts/Mutant_Tools/Icons/";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".hpb" yes;
	setAttr ".ovc" 18;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 101 0 no 3
		102 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27
		 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54
		 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81
		 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99 100 101
		102
		0 0.59420899999999999 0
		-3.0751100000000001e-09 0.58518199999999998 0.103183
		-6.0567700000000004e-09 0.55837400000000004 0.203232
		-8.8544099999999994e-09 0.51460099999999998 0.29710500000000001
		-1.1383e-08 0.45519100000000001 0.38195099999999998
		-1.3565700000000001e-08 0.38195000000000001 0.45519100000000001
		-1.5336300000000002e-08 0.29710500000000001 0.51460099999999998
		-1.6640900000000001e-08 0.203232 0.55837400000000004
		-1.7439800000000002e-08 0.103183 0.58518199999999998
		-1.7708799999999999e-08 0 0.59421000000000002
		-1.7439800000000002e-08 -0.103183 0.58518199999999998
		-1.6640900000000001e-08 -0.203232 0.55837400000000004
		-1.5336300000000002e-08 -0.29710500000000001 0.51460099999999998
		-1.3565700000000001e-08 -0.38195000000000001 0.45519100000000001
		-1.1383e-08 -0.45519100000000001 0.38195099999999998
		-8.8544099999999994e-09 -0.51460099999999998 0.29710500000000001
		-6.0567700000000004e-09 -0.55837400000000004 0.203232
		-3.0751100000000001e-09 -0.58518199999999998 0.103183
		0 -0.59420899999999999 0
		0 -0.58518199999999998 -0.103183
		0 -0.55837400000000004 -0.203232
		0 -0.51460099999999998 -0.29710500000000001
		0 -0.45519100000000001 -0.38195099999999998
		0 -0.38195000000000001 -0.45519100000000001
		0 -0.29710500000000001 -0.51460099999999998
		0 -0.203232 -0.55837499999999995
		0 -0.103183 -0.58518199999999998
		0 0 -0.59421000000000002
		0 0.103183 -0.58518199999999998
		0 0.203232 -0.55837499999999995
		0 0.29710500000000001 -0.51460099999999998
		0 0.38195000000000001 -0.45519100000000001
		0 0.45519100000000001 -0.38195099999999998
		0 0.51460099999999998 -0.29710500000000001
		0 0.55837400000000004 -0.203232
		0 0.58518199999999998 -0.103183
		0 0.59420899999999999 0
		0.103183 0.58518199999999998 0
		0.203232 0.55837400000000004 0
		0.29710500000000001 0.51460099999999998 0
		0.38195099999999998 0.45519100000000001 0
		0.45519100000000001 0.38195000000000001 0
		0.51460099999999998 0.29710500000000001 0
		0.55837400000000004 0.203232 0
		0.58518199999999998 0.103183 0
		0.59420899999999999 0 0
		0.58518199999999998 -0.103183 0
		0.55837400000000004 -0.203232 0
		0.51460099999999998 -0.29710500000000001 0
		0.45519100000000001 -0.38195000000000001 0
		0.38195099999999998 -0.45519100000000001 0
		0.29710500000000001 -0.51460099999999998 0
		0.203232 -0.55837400000000004 0
		0.103183 -0.58518199999999998 0
		0 -0.59420899999999999 0
		-0.103183 -0.58518199999999998 0
		-0.203232 -0.55837400000000004 0
		-0.29710500000000001 -0.51460099999999998 0
		-0.38195099999999998 -0.45519100000000001 0
		-0.45519100000000001 -0.38195000000000001 0
		-0.51460099999999998 -0.29710500000000001 0
		-0.55837400000000004 -0.203232 0
		-0.58518199999999998 -0.103183 0
		-0.59421000000000002 0 0
		-0.58518199999999998 0.103183 0
		-0.55837400000000004 0.203232 0
		-0.51460099999999998 0.29710500000000001 0
		-0.45519100000000001 0.38195000000000001 0
		-0.38195099999999998 0.45519100000000001 0
		-0.29710500000000001 0.51460099999999998 0
		-0.203232 0.55837400000000004 0
		-0.103183 0.58518199999999998 0
		0 0.59420899999999999 0
		-3.0751100000000001e-09 0.58518199999999998 0.103183
		-6.0567700000000004e-09 0.55837400000000004 0.203232
		-8.8544099999999994e-09 0.51460099999999998 0.29710500000000001
		-1.1383e-08 0.45519100000000001 0.38195099999999998
		-1.3565700000000001e-08 0.38195000000000001 0.45519100000000001
		-1.5336300000000002e-08 0.29710500000000001 0.51460099999999998
		-1.6640900000000001e-08 0.203232 0.55837400000000004
		-1.7439800000000002e-08 0.103183 0.58518199999999998
		-1.7708799999999999e-08 0 0.59421000000000002
		-0.18362100000000001 0 0.56512700000000005
		-0.34926800000000002 0 0.48072599999999999
		-0.48072599999999999 0 0.34926800000000002
		-0.56512700000000005 0 0.18362100000000001
		-0.59421000000000002 0 0
		-0.56512700000000005 0 -0.18362100000000001
		-0.48072599999999999 0 -0.34926800000000002
		-0.34926800000000002 0 -0.48072599999999999
		-0.18362100000000001 0 -0.56512700000000005
		0 0 -0.59421000000000002
		0.18362100000000001 0 -0.56512700000000005
		0.34926800000000002 0 -0.48072599999999999
		0.48072599999999999 0 -0.34926800000000002
		0.56512700000000005 0 -0.18362100000000001
		0.59420899999999999 0 0
		0.56512700000000005 0 0.18362100000000001
		0.48072599999999999 0 0.34926800000000002
		0.34926800000000002 0 0.48072599999999999
		0.18362100000000001 0 0.56512700000000005
		-1.7708799999999999e-08 0 0.59421000000000002
		;
createNode nurbsCurve -n "L_Cheek_A_Guide_Ctrl_Ctrl_CtrlShape" -p "L_Cheek_A_Guide";
	rename -uid "500690D4-4345-39F6-02F5-63BAB187A2FC";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2026/scripts/Mutant_Tools/Icons/";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".hpb" yes;
	setAttr ".ovc" 13;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 9 0 no 3
		10 0 1 2 3 4 5 6 7 8 9
		10
		-0.5 -0.25 -1.3977299999999999e-05
		0.94513100000000005 -0.25591599999999998 -1.3977299999999999e-05
		0.739653 -0.50644299999999998 -1.3977299999999999e-05
		0.99017999999999995 -0.93915099999999996 -1.3977299999999999e-05
		2.299302 -3.8742999999999997e-07 -1.37985e-05
		0.99018099999999998 0.93915099999999996 -1.3977299999999999e-05
		0.739653 0.50644199999999995 -1.3977299999999999e-05
		0.94513100000000005 0.25322099999999997 -7.1674600000000002e-06
		-0.5 0.25 -1.3977299999999999e-05
		-0.5 -0.25 -1.3977299999999999e-05
		;
createNode nurbsCurve -n "L_Cheek_A_Guide_Ctrl_Ctrl_Ctrl_CtrlShape" -p "L_Cheek_A_Guide";
	rename -uid "6F04FFF8-4C66-2113-B998-CBB411C3DBCF";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2026/scripts/Mutant_Tools/Icons/";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".hpb" yes;
	setAttr ".ovc" 6;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 9 0 no 3
		10 0 1 2 3 4 5 6 7 8 9
		10
		0.25 1.3977299999999999e-05 -0.5
		0.25591599999999998 1.3977299999999999e-05 0.94513100000000005
		0.50644299999999998 1.3977299999999999e-05 0.739653
		0.93915099999999996 1.3977299999999999e-05 0.99017999999999995
		3.8742999999999997e-07 1.37985e-05 2.299302
		-0.93915099999999996 1.3977299999999999e-05 0.99018099999999998
		-0.50644199999999995 1.3977299999999999e-05 0.739653
		-0.25322099999999997 7.1674600000000002e-06 0.94513100000000005
		-0.25 1.3977299999999999e-05 -0.5
		0.25 1.3977299999999999e-05 -0.5
		;
createNode dagContainer -n "L_CheekBone_Block" -p "Face";
	rename -uid "9A9746D3-4D70-98F7-2DAC-94892CB72ABB";
	addAttr -ci true -sn "nts" -ln "notes" -dt "string";
	setAttr ".isc" yes;
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2026/scripts/Mutant_Tools/Icons/Ribbon.png";
	setAttr ".ctor" -type "string" "rodri";
	setAttr ".cdat" -type "string" "2025/12/11 09:40:45";
	setAttr -l on -k off ".v";
	setAttr -l on -k off ".tx";
	setAttr -l on -k off ".ty";
	setAttr -l on -k off ".tz";
	setAttr -l on -k off ".rx";
	setAttr -l on -k off ".ry";
	setAttr -l on -k off ".rz";
	setAttr -l on -k off ".sx";
	setAttr -l on -k off ".sy";
	setAttr -l on -k off ".sz";
	setAttr ".nts" -type "string" (
		"['L_CheekBone_1_Ctrl_01_Jnt_Offset_Grp', 'L_CheekBone_1_Ctrl_Joints_Grp', 'L_CheekBone_1_ribbon_surfaceShape', 'L_CheekBone_1_02_Ctrl_Offset_Grp', 'L_CheekBone_1_skinCluster', 'L_CheekBone_1_Bind_01_Bnd_parentConstraint1', 'L_CheekBone_1_02_Ctrl', 'L_CheekBone_1_Bind_03_Bnd', 'L_CheekBone_1_Follicles_Grp', 'L_CheekBone_1_Main_Ctrl', 'L_CheekBone_1_01_Ctrl_tag', 'L_CheekBone_1_follicle_Shape1', 'L_CheekBone_1_Ctrl_02_Jnt', 'L_CheekBone_1_follicle_01_scaleConstraint1', 'L_CheekBone_1_ribbon_surfaceShapeOrig', 'L_CheekBone_1_ribbon_surface', 'L_CheekBone_1_Ctrl_01_Jnt_scaleConstraint1', 'L_CheekBone_1_Ctrl_03_Jnt_parentConstraint1', 'L_CheekBone_1_00_Ctrl', 'L_CheekBone_1_Rig_Grp', 'L_CheekBone_1_follicle_Shape3', 'L_CheekBone_1_Bnd_Grp', 'L_CheekBone_1_Ctrl_02_Jnt_Offset_Grp', 'L_CheekBone_1_Main_CtrlShape', 'L_CheekBone_1_skinClusterGroupParts', 'L_CheekBone_1_follicle_03_scaleConstraint1', 'L_CheekBone_Ctrl_Grp_scaleConstraint1', 'L_CheekBone_1_skinClusterGroupId', 'L_CheekBone_1_01_Ctrl_Offset_Grp', 'L_CheekBone_1_00_Ctrl_tag', 'L_CheekBone_1_Ctrl_03_Jnt_scaleConstraint1', 'L_CheekBone_1_Bind_02_Bnd_parentConstraint1', 'bindPose37', 'L_CheekBone_1_Bind_02_Bnd_scaleConstraint1', 'L_CheekBone_1_Ctrl_01_Jnt', 'L_CheekBone_1_01_CtrlShape01', 'L_CheekBone_1_Bind_01_Bnd_scaleConstraint1', 'L_CheekBone_1_02_CtrlShape01', 'L_CheekBone_1_00_Ctrl_Offset_Grp', 'L_CheekBone_1_Bind_03_Bnd_parentConstraint1', 'L_CheekBone_Ctrl_Grp', 'L_CheekBone_1_Ctrl_03_Jnt', 'L_CheekBone_1_Ctrl_03_Jnt_Offset_Grp', 'L_CheekBone_1_Bind_01_Bnd', 'L_CheekBone_1_Bind_02_Bnd', 'L_CheekBone_1_Ctrl_01_Jnt_parentConstraint1', 'L_CheekBone_1_follicle_Shape2', 'L_CheekBone_1_follicle_03', 'L_CheekBone_1_01_Ctrl', 'L_CheekBone_1_Ctrl_Main_Offset_Grp', 'L_CheekBone_Rig_Grp', 'L_CheekBone_1_Ctrl_02_Jnt_scaleConstraint1', 'L_CheekBone_1_follicle_02', 'L_CheekBone_1_02_Ctrl_tag', 'L_CheekBone_1_Ctrl_02_Jnt_parentConstraint1', 'L_CheekBone_1_follicle_01', 'L_CheekBone_1_Ctrls_Grp', 'L_CheekBone_1_follicle_02_scaleConstraint1', 'L_CheekBone_1_00_CtrlShape01', 'L_CheekBone_Ctrl_Grp_parentConstraint1', 'L_CheekBone_1_Main_Ctrl_tag', 'L_CheekBone_1_skinClusterSet', 'L_CheekBone_1_Bind_03_Bnd_scaleConstraint1']");
createNode transform -n "L_CheekBone_Guide" -p "L_CheekBone_Block";
	rename -uid "034551D5-4A59-2617-74F1-A6A8A99A6A82";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2026/scripts/Mutant_Tools/Icons/";
	setAttr ".t" -type "double3" 7.6968541145324707 176.38895171049469 14.904026031494141 ;
createNode nurbsSurface -n "L_CheekBone_GuideShape" -p "L_CheekBone_Guide";
	rename -uid "82CBBF5B-4F26-A13D-7C69-8DA70FB0F4E3";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2026/scripts/Mutant_Tools/Icons/";
	setAttr -k off ".v";
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr ".dvu" 0;
	setAttr ".dvv" 0;
	setAttr ".cpr" 4;
	setAttr ".cps" 4;
	setAttr ".cc" -type "nurbsSurface" 
		3 3 0 0 no 
		10 0 0 0 0.20000000000000001 0.40000000000000002 0.60000000000000009 0.80000000000000004
		 1 1 1
		6 0 0 0 1 1 1
		
		32
		-3.6603202419781722 -0.73206404839563444 0
		-3.6603202419781722 -0.24402134946521137 0
		-3.6603202419781722 0.24402134946521134 0
		-3.6603202419781722 0.73206404839563444 0
		-3.1722775430477506 -0.73206404839563444 0
		-3.1722775430477506 -0.24402134946521137 0
		-3.1722775430477506 0.24402134946521134 0
		-3.1722775430477506 0.73206404839563444 0
		-2.1961898124217742 -0.73206404839563444 0.0022759612475322364
		-2.1961898126092612 -0.24402134946521137 0.0022758697847858546
		-2.1961898126092612 0.24402134946521134 0.0022758697847858546
		-2.1961898126092612 0.73206404839563444 0.0022758697847858546
		-0.72836725966134297 -0.73206404839563444 0.0096685555269191426
		-0.72836726826885856 -0.24402134946521137 0.009668544550062148
		-0.72836727472448848 0.24402134946521134 0.0096685363174188362
		-0.72836726826885856 0.73206404839563444 0.009668544550062148
		0.70073647765110936 -0.73206404839563444 -0.39820479131463354
		0.70073647765110936 -0.24402134946521137 -0.39820479131463354
		0.70073652728876157 0.24402134946521134 -0.39820447844252899
		0.70073647765110936 0.73206404839563444 -0.39820479131463354
		1.9731430189306465 -0.73206404839563444 -1.2528640061802394
		1.9731430189306465 -0.24402134946521137 -1.2528640061802394
		1.9731430189306465 0.24402134946521134 -1.2528640061802394
		1.9731430189306465 0.73206404839563444 -1.2528640061802394
		2.7969966226386127 -0.73206404839563444 -1.8085527745226724
		2.7969966226386127 -0.24402134946521137 -1.8085527745226724
		2.7969966226386127 0.24402134946521134 -1.8085527745226724
		2.7969966226386127 0.73206404839563444 -1.8085527745226724
		3.2273037953522445 -0.73206404839563444 -2.0388165647513818
		3.2273037953522445 -0.24402134946521137 -2.0388165647513818
		3.2273037953522445 0.24402134946521134 -2.0388165647513818
		3.2273037953522445 0.73206404839563444 -2.0388165647513818
		
		;
	setAttr ".nufa" 4.5;
	setAttr ".nvfa" 4.5;
createNode dagContainer -n "R_CheekBone_Block" -p "Face";
	rename -uid "631C82E4-4A47-6D6B-F3E1-B5B7E3D944E9";
	addAttr -ci true -sn "nts" -ln "notes" -dt "string";
	setAttr ".isc" yes;
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2026/scripts/Mutant_Tools/Icons/Ribbon.png";
	setAttr ".ctor" -type "string" "rodri";
	setAttr ".cdat" -type "string" "2025/12/11 09:42:27";
	setAttr -l on -k off ".v";
	setAttr -l on -k off ".tx";
	setAttr -l on -k off ".ty";
	setAttr -l on -k off ".tz";
	setAttr -l on -k off ".rx";
	setAttr -l on -k off ".ry";
	setAttr -l on -k off ".rz";
	setAttr -l on -k off ".sx";
	setAttr -l on -k off ".sy";
	setAttr -l on -k off ".sz";
	setAttr ".nts" -type "string" (
		"['R_CheekBone_1_Bind_02_Bnd', 'R_CheekBone_1_ribbon_surface', 'R_CheekBone_1_follicle_02_scaleConstraint1', 'R_CheekBone_Ctrl_Grp', 'R_CheekBone_1_Bind_03_Bnd_scaleConstraint1', 'R_CheekBone_1_skinClusterGroupParts', 'R_CheekBone_1_ribbon_surfaceShape', 'R_CheekBone_1_follicle_Shape3', 'R_CheekBone_1_01_Ctrl', 'R_CheekBone_1_Ctrl_02_Jnt_parentConstraint1', 'R_CheekBone_1_follicle_03_scaleConstraint1', 'R_CheekBone_1_Main_Ctrl_tag', 'R_CheekBone_1_02_CtrlShape01', 'R_CheekBone_1_follicle_Shape1', 'R_CheekBone_1_Ctrl_01_Jnt_scaleConstraint1', 'R_CheekBone_1_01_Ctrl_tag', 'R_CheekBone_1_skinCluster', 'R_CheekBone_1_follicle_01_scaleConstraint1', 'R_CheekBone_1_follicle_01', 'R_CheekBone_1_follicle_Shape2', 'R_CheekBone_1_02_Ctrl', 'R_CheekBone_1_Ctrl_01_Jnt', 'R_CheekBone_1_Bind_02_Bnd_scaleConstraint1', 'R_CheekBone_1_Ctrl_02_Jnt', 'R_CheekBone_1_Ctrl_03_Jnt_parentConstraint1', 'R_CheekBone_1_Ctrl_03_Jnt_scaleConstraint1', 'R_CheekBone_1_follicle_02', 'R_CheekBone_1_skinClusterGroupId', 'R_CheekBone_1_Bind_01_Bnd_scaleConstraint1', 'R_CheekBone_1_Main_Ctrl', 'R_CheekBone_1_Ctrl_03_Jnt', 'R_CheekBone_1_Ctrl_01_Jnt_Offset_Grp', 'R_CheekBone_Ctrl_Grp_parentConstraint1', 'R_CheekBone_1_Bind_03_Bnd', 'R_CheekBone_1_02_Ctrl_Offset_Grp', 'R_CheekBone_1_00_Ctrl', 'R_CheekBone_1_Bind_01_Bnd', 'R_CheekBone_1_Bind_03_Bnd_parentConstraint1', 'R_CheekBone_1_follicle_03', 'R_CheekBone_1_Ctrl_01_Jnt_parentConstraint1', 'R_CheekBone_1_Ctrl_02_Jnt_scaleConstraint1', 'R_CheekBone_Rig_Grp', 'R_CheekBone_Ctrl_Grp_scaleConstraint1', 'R_CheekBone_1_Main_CtrlShape', 'R_CheekBone_1_00_CtrlShape01', 'R_CheekBone_1_skinClusterSet', 'R_CheekBone_1_Ctrl_Main_Offset_Grp', 'R_CheekBone_1_Bind_01_Bnd_parentConstraint1', 'R_CheekBone_1_Ctrl_03_Jnt_Offset_Grp', 'R_CheekBone_1_Ctrl_02_Jnt_Offset_Grp', 'R_CheekBone_1_01_CtrlShape01', 'R_CheekBone_1_00_Ctrl_tag', 'R_CheekBone_1_Bind_02_Bnd_parentConstraint1', 'R_CheekBone_1_Bnd_Grp', 'R_CheekBone_1_ribbon_surfaceShapeOrig', 'bindPose38', 'R_CheekBone_1_00_Ctrl_Offset_Grp', 'R_CheekBone_1_Follicles_Grp', 'R_CheekBone_1_Ctrl_Joints_Grp', 'R_CheekBone_1_01_Ctrl_Offset_Grp', 'R_CheekBone_1_Ctrls_Grp', 'R_CheekBone_1_02_Ctrl_tag', 'R_CheekBone_1_Rig_Grp']");
createNode transform -n "R_CheekBone_Guide" -p "R_CheekBone_Block";
	rename -uid "7B727171-47DF-BFAD-DCD1-1987FA1D6939";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2026/scripts/Mutant_Tools/Icons/";
	setAttr ".t" -type "double3" -7.697 176.38895171049469 14.904026031494141 ;
	setAttr ".s" -type "double3" -1 1 1 ;
createNode nurbsSurface -n "R_CheekBone_GuideShape" -p "R_CheekBone_Guide";
	rename -uid "7F27BFBC-4A24-F953-0547-C897E311FD30";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2026/scripts/Mutant_Tools/Icons/";
	setAttr -k off ".v";
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr ".dvu" 0;
	setAttr ".dvv" 0;
	setAttr ".cpr" 4;
	setAttr ".cps" 4;
	setAttr ".cc" -type "nurbsSurface" 
		3 3 0 0 no 
		10 0 0 0 0.20000000000000001 0.40000000000000002 0.60000000000000009 0.80000000000000004
		 1 1 1
		6 0 0 0 1 1 1
		
		32
		-3.6603202419781722 -0.73206404839563444 0
		-3.6603202419781722 -0.24402134946521137 0
		-3.6603202419781722 0.24402134946521134 0
		-3.6603202419781722 0.73206404839563444 0
		-3.1722775430477506 -0.73206404839563444 0
		-3.1722775430477506 -0.24402134946521137 0
		-3.1722775430477506 0.24402134946521134 0
		-3.1722775430477506 0.73206404839563444 0
		-2.1961898124217742 -0.73206404839563444 0.0022759612475322364
		-2.1961898126092612 -0.24402134946521137 0.0022758697847858546
		-2.1961898126092612 0.24402134946521134 0.0022758697847858546
		-2.1961898126092612 0.73206404839563444 0.0022758697847858546
		-0.72836725966134297 -0.73206404839563444 0.0096685555269191426
		-0.72836726826885856 -0.24402134946521137 0.009668544550062148
		-0.72836727472448848 0.24402134946521134 0.0096685363174188362
		-0.72836726826885856 0.73206404839563444 0.009668544550062148
		0.70073647765110936 -0.73206404839563444 -0.39820479131463354
		0.70073647765110936 -0.24402134946521137 -0.39820479131463354
		0.70073652728876157 0.24402134946521134 -0.39820447844252899
		0.70073647765110936 0.73206404839563444 -0.39820479131463354
		1.9731430189306465 -0.73206404839563444 -1.2528640061802394
		1.9731430189306465 -0.24402134946521137 -1.2528640061802394
		1.9731430189306465 0.24402134946521134 -1.2528640061802394
		1.9731430189306465 0.73206404839563444 -1.2528640061802394
		2.7969966226386127 -0.73206404839563444 -1.8085527745226724
		2.7969966226386127 -0.24402134946521137 -1.8085527745226724
		2.7969966226386127 0.24402134946521134 -1.8085527745226724
		2.7969966226386127 0.73206404839563444 -1.8085527745226724
		3.2273037953522445 -0.73206404839563444 -2.0388165647513818
		3.2273037953522445 -0.24402134946521137 -2.0388165647513818
		3.2273037953522445 0.24402134946521134 -2.0388165647513818
		3.2273037953522445 0.73206404839563444 -2.0388165647513818
		
		;
	setAttr ".nufa" 4.5;
	setAttr ".nvfa" 4.5;
createNode dagContainer -n "Mid_Brow_Block" -p "Face";
	rename -uid "98F4B460-4CE3-1ED8-2563-35A315C53D9D";
	addAttr -ci true -sn "nts" -ln "notes" -dt "string";
	setAttr ".isc" yes;
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2026/scripts/Mutant_Tools/Icons/Chain.png";
	setAttr ".ctor" -type "string" "rodri";
	setAttr ".cdat" -type "string" "2025/12/11 09:43:17";
	setAttr -l on -k off ".v";
	setAttr -l on -k off ".tx";
	setAttr -l on -k off ".ty";
	setAttr -l on -k off ".tz";
	setAttr -l on -k off ".rx";
	setAttr -l on -k off ".ry";
	setAttr -l on -k off ".rz";
	setAttr -l on -k off ".sx";
	setAttr -l on -k off ".sy";
	setAttr -l on -k off ".sz";
	setAttr ".nts" -type "string" "['Mid_Brow_A_Ctrl_Offset_Grp_scaleConstraint1', 'Mid_Brow_A_Ctrl_Offset_Grp_parentConstraint1', 'Mid_Brow_Ctrl_Grp', 'Mid_Brow_Rig_Grp', 'Mid_Brow_A_CtrlShape', 'Mid_Brow_A_Bnd', 'Mid_Brow_Rig_Grp_parentConstraint1', 'Mid_Brow_A_Jnt', 'Mid_Brow_A_Jnt_Ctrl_tag', 'Mid_Brow_A_Bnd_scaleConstraint1', 'Mid_Brow_A_Bnd_parentConstraint1', 'Mid_Brow_A_Jnt_parentConstraint1', 'Mid_Brow_Rig_Grp_scaleConstraint1', 'Mid_Brow_A_Ctrl', 'Mid_Brow_A_Ctrl_Offset_Grp']";
createNode joint -n "Mid_Brow_A_Guide" -p "Mid_Brow_Block";
	rename -uid "BF160B1C-40D4-88DA-B6C0-BBBA54C76CD1";
	addAttr -ci true -sn "Helper" -ln "Helper" -min 0 -max 1 -en "Hide:Show" -at "enum";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2026/scripts/Mutant_Tools/Icons/";
	setAttr ".t" -type "double3" 0.00012799000251106918 184.93623352050781 17.237315039856721 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr -cb on ".Helper" 1;
createNode nurbsCurve -n "Mid_Brow_A_Guide_CtrlShape" -p "Mid_Brow_A_Guide";
	rename -uid "6121A264-42FF-E430-00E3-2496286555BF";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2026/scripts/Mutant_Tools/Icons/";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".hpb" yes;
	setAttr ".ovc" 14;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 9 0 no 3
		10 0 1 2 3 4 5 6 7 8 9
		10
		1.3977299999999999e-05 -0.5 0.25
		1.3977299999999999e-05 0.94513100000000005 0.25591599999999998
		1.3977299999999999e-05 0.739653 0.50644299999999998
		1.3977299999999999e-05 0.99017999999999995 0.93915099999999996
		1.37985e-05 2.299302 3.8742999999999997e-07
		1.3977299999999999e-05 0.99018099999999998 -0.93915099999999996
		1.3977299999999999e-05 0.739653 -0.50644199999999995
		7.1674600000000002e-06 0.94513100000000005 -0.25322099999999997
		1.3977299999999999e-05 -0.5 -0.25
		1.3977299999999999e-05 -0.5 0.25
		;
createNode nurbsCurve -n "Mid_Brow_A_Guide_Ctrl_CtrlShape" -p "Mid_Brow_A_Guide";
	rename -uid "88E4E85D-4D25-A651-B466-8387FAD4F4B6";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2026/scripts/Mutant_Tools/Icons/";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".hpb" yes;
	setAttr ".ovc" 18;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 101 0 no 3
		102 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27
		 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54
		 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81
		 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99 100 101
		102
		0 0.59420899999999999 0
		-3.0751100000000001e-09 0.58518199999999998 0.103183
		-6.0567700000000004e-09 0.55837400000000004 0.203232
		-8.8544099999999994e-09 0.51460099999999998 0.29710500000000001
		-1.1383e-08 0.45519100000000001 0.38195099999999998
		-1.3565700000000001e-08 0.38195000000000001 0.45519100000000001
		-1.5336300000000002e-08 0.29710500000000001 0.51460099999999998
		-1.6640900000000001e-08 0.203232 0.55837400000000004
		-1.7439800000000002e-08 0.103183 0.58518199999999998
		-1.7708799999999999e-08 0 0.59421000000000002
		-1.7439800000000002e-08 -0.103183 0.58518199999999998
		-1.6640900000000001e-08 -0.203232 0.55837400000000004
		-1.5336300000000002e-08 -0.29710500000000001 0.51460099999999998
		-1.3565700000000001e-08 -0.38195000000000001 0.45519100000000001
		-1.1383e-08 -0.45519100000000001 0.38195099999999998
		-8.8544099999999994e-09 -0.51460099999999998 0.29710500000000001
		-6.0567700000000004e-09 -0.55837400000000004 0.203232
		-3.0751100000000001e-09 -0.58518199999999998 0.103183
		0 -0.59420899999999999 0
		0 -0.58518199999999998 -0.103183
		0 -0.55837400000000004 -0.203232
		0 -0.51460099999999998 -0.29710500000000001
		0 -0.45519100000000001 -0.38195099999999998
		0 -0.38195000000000001 -0.45519100000000001
		0 -0.29710500000000001 -0.51460099999999998
		0 -0.203232 -0.55837499999999995
		0 -0.103183 -0.58518199999999998
		0 0 -0.59421000000000002
		0 0.103183 -0.58518199999999998
		0 0.203232 -0.55837499999999995
		0 0.29710500000000001 -0.51460099999999998
		0 0.38195000000000001 -0.45519100000000001
		0 0.45519100000000001 -0.38195099999999998
		0 0.51460099999999998 -0.29710500000000001
		0 0.55837400000000004 -0.203232
		0 0.58518199999999998 -0.103183
		0 0.59420899999999999 0
		0.103183 0.58518199999999998 0
		0.203232 0.55837400000000004 0
		0.29710500000000001 0.51460099999999998 0
		0.38195099999999998 0.45519100000000001 0
		0.45519100000000001 0.38195000000000001 0
		0.51460099999999998 0.29710500000000001 0
		0.55837400000000004 0.203232 0
		0.58518199999999998 0.103183 0
		0.59420899999999999 0 0
		0.58518199999999998 -0.103183 0
		0.55837400000000004 -0.203232 0
		0.51460099999999998 -0.29710500000000001 0
		0.45519100000000001 -0.38195000000000001 0
		0.38195099999999998 -0.45519100000000001 0
		0.29710500000000001 -0.51460099999999998 0
		0.203232 -0.55837400000000004 0
		0.103183 -0.58518199999999998 0
		0 -0.59420899999999999 0
		-0.103183 -0.58518199999999998 0
		-0.203232 -0.55837400000000004 0
		-0.29710500000000001 -0.51460099999999998 0
		-0.38195099999999998 -0.45519100000000001 0
		-0.45519100000000001 -0.38195000000000001 0
		-0.51460099999999998 -0.29710500000000001 0
		-0.55837400000000004 -0.203232 0
		-0.58518199999999998 -0.103183 0
		-0.59421000000000002 0 0
		-0.58518199999999998 0.103183 0
		-0.55837400000000004 0.203232 0
		-0.51460099999999998 0.29710500000000001 0
		-0.45519100000000001 0.38195000000000001 0
		-0.38195099999999998 0.45519100000000001 0
		-0.29710500000000001 0.51460099999999998 0
		-0.203232 0.55837400000000004 0
		-0.103183 0.58518199999999998 0
		0 0.59420899999999999 0
		-3.0751100000000001e-09 0.58518199999999998 0.103183
		-6.0567700000000004e-09 0.55837400000000004 0.203232
		-8.8544099999999994e-09 0.51460099999999998 0.29710500000000001
		-1.1383e-08 0.45519100000000001 0.38195099999999998
		-1.3565700000000001e-08 0.38195000000000001 0.45519100000000001
		-1.5336300000000002e-08 0.29710500000000001 0.51460099999999998
		-1.6640900000000001e-08 0.203232 0.55837400000000004
		-1.7439800000000002e-08 0.103183 0.58518199999999998
		-1.7708799999999999e-08 0 0.59421000000000002
		-0.18362100000000001 0 0.56512700000000005
		-0.34926800000000002 0 0.48072599999999999
		-0.48072599999999999 0 0.34926800000000002
		-0.56512700000000005 0 0.18362100000000001
		-0.59421000000000002 0 0
		-0.56512700000000005 0 -0.18362100000000001
		-0.48072599999999999 0 -0.34926800000000002
		-0.34926800000000002 0 -0.48072599999999999
		-0.18362100000000001 0 -0.56512700000000005
		0 0 -0.59421000000000002
		0.18362100000000001 0 -0.56512700000000005
		0.34926800000000002 0 -0.48072599999999999
		0.48072599999999999 0 -0.34926800000000002
		0.56512700000000005 0 -0.18362100000000001
		0.59420899999999999 0 0
		0.56512700000000005 0 0.18362100000000001
		0.48072599999999999 0 0.34926800000000002
		0.34926800000000002 0 0.48072599999999999
		0.18362100000000001 0 0.56512700000000005
		-1.7708799999999999e-08 0 0.59421000000000002
		;
createNode nurbsCurve -n "Mid_Brow_A_Guide_Ctrl_Ctrl_CtrlShape" -p "Mid_Brow_A_Guide";
	rename -uid "0B1F72A8-4FF2-6239-2435-3FB9ADB1CACF";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2026/scripts/Mutant_Tools/Icons/";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".hpb" yes;
	setAttr ".ovc" 13;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 9 0 no 3
		10 0 1 2 3 4 5 6 7 8 9
		10
		-0.5 -0.25 -1.3977299999999999e-05
		0.94513100000000005 -0.25591599999999998 -1.3977299999999999e-05
		0.739653 -0.50644299999999998 -1.3977299999999999e-05
		0.99017999999999995 -0.93915099999999996 -1.3977299999999999e-05
		2.299302 -3.8742999999999997e-07 -1.37985e-05
		0.99018099999999998 0.93915099999999996 -1.3977299999999999e-05
		0.739653 0.50644199999999995 -1.3977299999999999e-05
		0.94513100000000005 0.25322099999999997 -7.1674600000000002e-06
		-0.5 0.25 -1.3977299999999999e-05
		-0.5 -0.25 -1.3977299999999999e-05
		;
createNode nurbsCurve -n "Mid_Brow_A_Guide_Ctrl_Ctrl_Ctrl_CtrlShape" -p "Mid_Brow_A_Guide";
	rename -uid "F249E579-4240-6D4B-CFC6-7E889D782860";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2026/scripts/Mutant_Tools/Icons/";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".hpb" yes;
	setAttr ".ovc" 6;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 9 0 no 3
		10 0 1 2 3 4 5 6 7 8 9
		10
		0.25 1.3977299999999999e-05 -0.5
		0.25591599999999998 1.3977299999999999e-05 0.94513100000000005
		0.50644299999999998 1.3977299999999999e-05 0.739653
		0.93915099999999996 1.3977299999999999e-05 0.99017999999999995
		3.8742999999999997e-07 1.37985e-05 2.299302
		-0.93915099999999996 1.3977299999999999e-05 0.99018099999999998
		-0.50644199999999995 1.3977299999999999e-05 0.739653
		-0.25322099999999997 7.1674600000000002e-06 0.94513100000000005
		-0.25 1.3977299999999999e-05 -0.5
		0.25 1.3977299999999999e-05 -0.5
		;
createNode dagContainer -n "PushMidBrow_Block" -p "Face";
	rename -uid "378081FE-495B-E2B8-9C7E-70B8E6C600AE";
	addAttr -ci true -sn "nts" -ln "notes" -dt "string";
	setAttr ".isc" yes;
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2026/scripts/Mutant_Tools/Icons/CODE.png";
	setAttr ".ctor" -type "string" "rodri";
	setAttr ".cdat" -type "string" "2025/12/11 16:30:27";
	setAttr -l on -k off ".v";
	setAttr -l on -k off ".tx";
	setAttr -l on -k off ".ty";
	setAttr -l on -k off ".tz";
	setAttr -l on -k off ".rx";
	setAttr -l on -k off ".ry";
	setAttr -l on -k off ".rz";
	setAttr -l on -k off ".sx";
	setAttr -l on -k off ".sy";
	setAttr -l on -k off ".sz";
	setAttr ".nts" -type "string" "['Brow_autoPush_PMA', 'Mid_Brow_A_Ctrl_Root_Grp', 'Mid_Brow_A_Ctrl_Auto_Grp', 'R_bc_autoPush', 'Mid_autoPush_MD', 'R_md_autoPush', 'L_gt_autoPush', 'L_bc_autoPush', 'Mid_Brow_A_Ctrl_Forward_Grp', 'L_md_autoPush', 'R_gt_autoPush', 'Mid_Brow_A_Ctrl_Auto_Grp_parentConstraint1']";
createNode transform -n "PushMidBrow_Loc" -p "PushMidBrow_Block";
	rename -uid "08D83B1D-464B-D390-F212-46B631CE99A5";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2026/scripts/Mutant_Tools/Icons/";
createNode locator -n "PushMidBrow_LocShape" -p "PushMidBrow_Loc";
	rename -uid "38BEA14F-4794-C17B-0854-74969600053A";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2026/scripts/Mutant_Tools/Icons/";
	setAttr -k off ".v";
createNode dagContainer -n "Mid_BrowNose_Block" -p "Face";
	rename -uid "E9DB2D49-44A6-C964-08CC-92B4B0729084";
	addAttr -ci true -sn "nts" -ln "notes" -dt "string";
	setAttr ".isc" yes;
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2026/scripts/Mutant_Tools/Icons/Chain.png";
	setAttr ".ctor" -type "string" "rodri";
	setAttr ".cdat" -type "string" "2025/12/11 09:43:48";
	setAttr -l on -k off ".v";
	setAttr -l on -k off ".tx";
	setAttr -l on -k off ".ty";
	setAttr -l on -k off ".tz";
	setAttr -l on -k off ".rx";
	setAttr -l on -k off ".ry";
	setAttr -l on -k off ".rz";
	setAttr -l on -k off ".sx";
	setAttr -l on -k off ".sy";
	setAttr -l on -k off ".sz";
	setAttr ".nts" -type "string" "['Mid_BrowNose_A_Ctrl', 'Mid_BrowNose_Rig_Grp_scaleConstraint1', 'Mid_BrowNose_A_Ctrl_Offset_Grp_scaleConstraint1', 'Mid_BrowNose_A_Ctrl_Offset_Grp_parentConstraint1', 'Mid_BrowNose_A_Jnt_parentConstraint1', 'Mid_BrowNose_A_Ctrl_Offset_Grp', 'Mid_BrowNose_Rig_Grp', 'Mid_BrowNose_A_CtrlShape', 'Mid_BrowNose_Rig_Grp_parentConstraint1', 'Mid_BrowNose_A_Bnd_parentConstraint1', 'Mid_BrowNose_Ctrl_Grp', 'Mid_BrowNose_A_Bnd', 'Mid_BrowNose_A_Jnt_Ctrl_tag', 'Mid_BrowNose_A_Bnd_scaleConstraint1', 'Mid_BrowNose_A_Jnt']";
createNode joint -n "Mid_BrowNose_A_Guide" -p "Mid_BrowNose_Block";
	rename -uid "AF744D91-4A0A-A53B-69F0-BA99752E3F1F";
	addAttr -ci true -sn "Helper" -ln "Helper" -min 0 -max 1 -en "Hide:Show" -at "enum";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2026/scripts/Mutant_Tools/Icons/";
	setAttr ".t" -type "double3" 0.00016289000632241368 182.87991780356739 17.245303624183972 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr -cb on ".Helper" 1;
createNode nurbsCurve -n "Mid_BrowNose_A_Guide_CtrlShape" -p "Mid_BrowNose_A_Guide";
	rename -uid "858E053D-4058-D6B0-AC0F-D9B1171FCEDD";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2026/scripts/Mutant_Tools/Icons/";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".hpb" yes;
	setAttr ".ovc" 14;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 9 0 no 3
		10 0 1 2 3 4 5 6 7 8 9
		10
		1.3977299999999999e-05 -0.5 0.25
		1.3977299999999999e-05 0.94513100000000005 0.25591599999999998
		1.3977299999999999e-05 0.739653 0.50644299999999998
		1.3977299999999999e-05 0.99017999999999995 0.93915099999999996
		1.37985e-05 2.299302 3.8742999999999997e-07
		1.3977299999999999e-05 0.99018099999999998 -0.93915099999999996
		1.3977299999999999e-05 0.739653 -0.50644199999999995
		7.1674600000000002e-06 0.94513100000000005 -0.25322099999999997
		1.3977299999999999e-05 -0.5 -0.25
		1.3977299999999999e-05 -0.5 0.25
		;
createNode nurbsCurve -n "Mid_BrowNose_A_Guide_Ctrl_CtrlShape" -p "Mid_BrowNose_A_Guide";
	rename -uid "2F869248-444A-F7C6-9C69-55914BCACB84";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2026/scripts/Mutant_Tools/Icons/";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".hpb" yes;
	setAttr ".ovc" 18;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 101 0 no 3
		102 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27
		 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54
		 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81
		 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99 100 101
		102
		0 0.59420899999999999 0
		-3.0751100000000001e-09 0.58518199999999998 0.103183
		-6.0567700000000004e-09 0.55837400000000004 0.203232
		-8.8544099999999994e-09 0.51460099999999998 0.29710500000000001
		-1.1383e-08 0.45519100000000001 0.38195099999999998
		-1.3565700000000001e-08 0.38195000000000001 0.45519100000000001
		-1.5336300000000002e-08 0.29710500000000001 0.51460099999999998
		-1.6640900000000001e-08 0.203232 0.55837400000000004
		-1.7439800000000002e-08 0.103183 0.58518199999999998
		-1.7708799999999999e-08 0 0.59421000000000002
		-1.7439800000000002e-08 -0.103183 0.58518199999999998
		-1.6640900000000001e-08 -0.203232 0.55837400000000004
		-1.5336300000000002e-08 -0.29710500000000001 0.51460099999999998
		-1.3565700000000001e-08 -0.38195000000000001 0.45519100000000001
		-1.1383e-08 -0.45519100000000001 0.38195099999999998
		-8.8544099999999994e-09 -0.51460099999999998 0.29710500000000001
		-6.0567700000000004e-09 -0.55837400000000004 0.203232
		-3.0751100000000001e-09 -0.58518199999999998 0.103183
		0 -0.59420899999999999 0
		0 -0.58518199999999998 -0.103183
		0 -0.55837400000000004 -0.203232
		0 -0.51460099999999998 -0.29710500000000001
		0 -0.45519100000000001 -0.38195099999999998
		0 -0.38195000000000001 -0.45519100000000001
		0 -0.29710500000000001 -0.51460099999999998
		0 -0.203232 -0.55837499999999995
		0 -0.103183 -0.58518199999999998
		0 0 -0.59421000000000002
		0 0.103183 -0.58518199999999998
		0 0.203232 -0.55837499999999995
		0 0.29710500000000001 -0.51460099999999998
		0 0.38195000000000001 -0.45519100000000001
		0 0.45519100000000001 -0.38195099999999998
		0 0.51460099999999998 -0.29710500000000001
		0 0.55837400000000004 -0.203232
		0 0.58518199999999998 -0.103183
		0 0.59420899999999999 0
		0.103183 0.58518199999999998 0
		0.203232 0.55837400000000004 0
		0.29710500000000001 0.51460099999999998 0
		0.38195099999999998 0.45519100000000001 0
		0.45519100000000001 0.38195000000000001 0
		0.51460099999999998 0.29710500000000001 0
		0.55837400000000004 0.203232 0
		0.58518199999999998 0.103183 0
		0.59420899999999999 0 0
		0.58518199999999998 -0.103183 0
		0.55837400000000004 -0.203232 0
		0.51460099999999998 -0.29710500000000001 0
		0.45519100000000001 -0.38195000000000001 0
		0.38195099999999998 -0.45519100000000001 0
		0.29710500000000001 -0.51460099999999998 0
		0.203232 -0.55837400000000004 0
		0.103183 -0.58518199999999998 0
		0 -0.59420899999999999 0
		-0.103183 -0.58518199999999998 0
		-0.203232 -0.55837400000000004 0
		-0.29710500000000001 -0.51460099999999998 0
		-0.38195099999999998 -0.45519100000000001 0
		-0.45519100000000001 -0.38195000000000001 0
		-0.51460099999999998 -0.29710500000000001 0
		-0.55837400000000004 -0.203232 0
		-0.58518199999999998 -0.103183 0
		-0.59421000000000002 0 0
		-0.58518199999999998 0.103183 0
		-0.55837400000000004 0.203232 0
		-0.51460099999999998 0.29710500000000001 0
		-0.45519100000000001 0.38195000000000001 0
		-0.38195099999999998 0.45519100000000001 0
		-0.29710500000000001 0.51460099999999998 0
		-0.203232 0.55837400000000004 0
		-0.103183 0.58518199999999998 0
		0 0.59420899999999999 0
		-3.0751100000000001e-09 0.58518199999999998 0.103183
		-6.0567700000000004e-09 0.55837400000000004 0.203232
		-8.8544099999999994e-09 0.51460099999999998 0.29710500000000001
		-1.1383e-08 0.45519100000000001 0.38195099999999998
		-1.3565700000000001e-08 0.38195000000000001 0.45519100000000001
		-1.5336300000000002e-08 0.29710500000000001 0.51460099999999998
		-1.6640900000000001e-08 0.203232 0.55837400000000004
		-1.7439800000000002e-08 0.103183 0.58518199999999998
		-1.7708799999999999e-08 0 0.59421000000000002
		-0.18362100000000001 0 0.56512700000000005
		-0.34926800000000002 0 0.48072599999999999
		-0.48072599999999999 0 0.34926800000000002
		-0.56512700000000005 0 0.18362100000000001
		-0.59421000000000002 0 0
		-0.56512700000000005 0 -0.18362100000000001
		-0.48072599999999999 0 -0.34926800000000002
		-0.34926800000000002 0 -0.48072599999999999
		-0.18362100000000001 0 -0.56512700000000005
		0 0 -0.59421000000000002
		0.18362100000000001 0 -0.56512700000000005
		0.34926800000000002 0 -0.48072599999999999
		0.48072599999999999 0 -0.34926800000000002
		0.56512700000000005 0 -0.18362100000000001
		0.59420899999999999 0 0
		0.56512700000000005 0 0.18362100000000001
		0.48072599999999999 0 0.34926800000000002
		0.34926800000000002 0 0.48072599999999999
		0.18362100000000001 0 0.56512700000000005
		-1.7708799999999999e-08 0 0.59421000000000002
		;
createNode nurbsCurve -n "Mid_BrowNose_A_Guide_Ctrl_Ctrl_CtrlShape" -p "Mid_BrowNose_A_Guide";
	rename -uid "A1CD1C0C-4910-CDC8-1D46-048AB3E79110";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2026/scripts/Mutant_Tools/Icons/";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".hpb" yes;
	setAttr ".ovc" 13;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 9 0 no 3
		10 0 1 2 3 4 5 6 7 8 9
		10
		-0.5 -0.25 -1.3977299999999999e-05
		0.94513100000000005 -0.25591599999999998 -1.3977299999999999e-05
		0.739653 -0.50644299999999998 -1.3977299999999999e-05
		0.99017999999999995 -0.93915099999999996 -1.3977299999999999e-05
		2.299302 -3.8742999999999997e-07 -1.37985e-05
		0.99018099999999998 0.93915099999999996 -1.3977299999999999e-05
		0.739653 0.50644199999999995 -1.3977299999999999e-05
		0.94513100000000005 0.25322099999999997 -7.1674600000000002e-06
		-0.5 0.25 -1.3977299999999999e-05
		-0.5 -0.25 -1.3977299999999999e-05
		;
createNode nurbsCurve -n "Mid_BrowNose_A_Guide_Ctrl_Ctrl_Ctrl_CtrlShape" -p "Mid_BrowNose_A_Guide";
	rename -uid "8659CEC9-424C-A8C0-AFE2-28A3180F20F3";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2026/scripts/Mutant_Tools/Icons/";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".hpb" yes;
	setAttr ".ovc" 6;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 9 0 no 3
		10 0 1 2 3 4 5 6 7 8 9
		10
		0.25 1.3977299999999999e-05 -0.5
		0.25591599999999998 1.3977299999999999e-05 0.94513100000000005
		0.50644299999999998 1.3977299999999999e-05 0.739653
		0.93915099999999996 1.3977299999999999e-05 0.99017999999999995
		3.8742999999999997e-07 1.37985e-05 2.299302
		-0.93915099999999996 1.3977299999999999e-05 0.99018099999999998
		-0.50644199999999995 1.3977299999999999e-05 0.739653
		-0.25322099999999997 7.1674600000000002e-06 0.94513100000000005
		-0.25 1.3977299999999999e-05 -0.5
		0.25 1.3977299999999999e-05 -0.5
		;
createNode dagContainer -n "PushBrowNose_Block" -p "Face";
	rename -uid "06A27EDC-493F-D3C2-3283-4BBF7793A42A";
	addAttr -ci true -sn "nts" -ln "notes" -dt "string";
	setAttr ".isc" yes;
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2026/scripts/Mutant_Tools/Icons/CODE.png";
	setAttr ".ctor" -type "string" "rodri";
	setAttr ".cdat" -type "string" "2025/12/11 18:00:58";
	setAttr -l on -k off ".v";
	setAttr -l on -k off ".tx";
	setAttr -l on -k off ".ty";
	setAttr -l on -k off ".tz";
	setAttr -l on -k off ".rx";
	setAttr -l on -k off ".ry";
	setAttr -l on -k off ".rz";
	setAttr -l on -k off ".sx";
	setAttr -l on -k off ".sy";
	setAttr -l on -k off ".sz";
	setAttr ".nts" -type "string" "['NoseBridge_lessThan', 'Mid_BrowNose_A_Ctrl_Root_Grp', 'Mid_BrowNose_A_Ctrl_Auto_Grp']";
createNode transform -n "PushBrowNose_Loc" -p "PushBrowNose_Block";
	rename -uid "1829B6D0-4809-6B79-5189-DBB152A2B5EA";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2026/scripts/Mutant_Tools/Icons/";
createNode locator -n "PushBrowNose_LocShape" -p "PushBrowNose_Loc";
	rename -uid "0A53C896-4458-150D-EA06-50940BEDE2B9";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2026/scripts/Mutant_Tools/Icons/";
	setAttr -k off ".v";
createNode dagContainer -n "UpperTeeth_Block" -p "Face";
	rename -uid "BC712E8C-45C6-84A3-260C-56AB086B49CC";
	addAttr -ci true -sn "nts" -ln "notes" -dt "string";
	setAttr ".isc" yes;
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2026/scripts/Mutant_Tools/Icons/Chain.png";
	setAttr ".ctor" -type "string" "rodri";
	setAttr ".cdat" -type "string" "2025/12/16 15:42:10";
	setAttr -l on -k off ".v";
	setAttr -l on -k off ".tx";
	setAttr -l on -k off ".ty";
	setAttr -l on -k off ".tz";
	setAttr -l on -k off ".rx";
	setAttr -l on -k off ".ry";
	setAttr -l on -k off ".rz";
	setAttr -l on -k off ".sx";
	setAttr -l on -k off ".sy";
	setAttr -l on -k off ".sz";
	setAttr ".nts" -type "string" "['UpperTeeth_Rig_Grp_scaleConstraint1', 'UpperTeeth_Bnd', 'UpperTeeth_Ctrl_Offset_Grp_scaleConstraint1', 'UpperTeeth_Bnd_parentConstraint1', 'UpperTeeth_Jnt', 'UpperTeeth_Rig_Grp', 'UpperTeeth_Jnt_Ctrl_tag', 'UpperTeeth_CtrlShape', 'UpperTeeth_Bnd_scaleConstraint1', 'UpperTeeth_Jnt_parentConstraint1', 'UpperTeeth_Ctrl_Offset_Grp', 'UpperTeeth_Rig_Grp_parentConstraint1', 'UpperTeeth_Ctrl_Grp', 'UpperTeeth_Ctrl_Offset_Grp_parentConstraint1', 'UpperTeeth_Ctrl']";
createNode joint -n "UpperTeeth_Guide" -p "UpperTeeth_Block";
	rename -uid "D0D0B44A-4D7C-64D6-AF61-C2AB79F72860";
	addAttr -ci true -sn "Helper" -ln "Helper" -min 0 -max 1 -en "Hide:Show" -at "enum";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2026/scripts/Mutant_Tools/Icons/";
	setAttr ".t" -type "double3" 0 169.99756622314453 15.688717362128688 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr -cb on ".Helper" 1;
createNode nurbsCurve -n "UpperTeeth_Guide_CtrlShape" -p "UpperTeeth_Guide";
	rename -uid "9135BAFF-4547-6C30-A08F-48873E310134";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2026/scripts/Mutant_Tools/Icons/";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".hpb" yes;
	setAttr ".ovc" 14;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 9 0 no 3
		10 0 1 2 3 4 5 6 7 8 9
		10
		1.3977299999999999e-05 -0.5 0.25
		1.3977299999999999e-05 0.94513100000000005 0.25591599999999998
		1.3977299999999999e-05 0.739653 0.50644299999999998
		1.3977299999999999e-05 0.99017999999999995 0.93915099999999996
		1.37985e-05 2.299302 3.8742999999999997e-07
		1.3977299999999999e-05 0.99018099999999998 -0.93915099999999996
		1.3977299999999999e-05 0.739653 -0.50644199999999995
		7.1674600000000002e-06 0.94513100000000005 -0.25322099999999997
		1.3977299999999999e-05 -0.5 -0.25
		1.3977299999999999e-05 -0.5 0.25
		;
createNode nurbsCurve -n "UpperTeeth_Guide_Ctrl_CtrlShape" -p "UpperTeeth_Guide";
	rename -uid "2CE0DAE2-4707-587E-10B5-07AD24F70B80";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2026/scripts/Mutant_Tools/Icons/";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".hpb" yes;
	setAttr ".ovc" 18;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 101 0 no 3
		102 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27
		 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54
		 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81
		 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99 100 101
		102
		0 0.59420899999999999 0
		-3.0751100000000001e-09 0.58518199999999998 0.103183
		-6.0567700000000004e-09 0.55837400000000004 0.203232
		-8.8544099999999994e-09 0.51460099999999998 0.29710500000000001
		-1.1383e-08 0.45519100000000001 0.38195099999999998
		-1.3565700000000001e-08 0.38195000000000001 0.45519100000000001
		-1.5336300000000002e-08 0.29710500000000001 0.51460099999999998
		-1.6640900000000001e-08 0.203232 0.55837400000000004
		-1.7439800000000002e-08 0.103183 0.58518199999999998
		-1.7708799999999999e-08 0 0.59421000000000002
		-1.7439800000000002e-08 -0.103183 0.58518199999999998
		-1.6640900000000001e-08 -0.203232 0.55837400000000004
		-1.5336300000000002e-08 -0.29710500000000001 0.51460099999999998
		-1.3565700000000001e-08 -0.38195000000000001 0.45519100000000001
		-1.1383e-08 -0.45519100000000001 0.38195099999999998
		-8.8544099999999994e-09 -0.51460099999999998 0.29710500000000001
		-6.0567700000000004e-09 -0.55837400000000004 0.203232
		-3.0751100000000001e-09 -0.58518199999999998 0.103183
		0 -0.59420899999999999 0
		0 -0.58518199999999998 -0.103183
		0 -0.55837400000000004 -0.203232
		0 -0.51460099999999998 -0.29710500000000001
		0 -0.45519100000000001 -0.38195099999999998
		0 -0.38195000000000001 -0.45519100000000001
		0 -0.29710500000000001 -0.51460099999999998
		0 -0.203232 -0.55837499999999995
		0 -0.103183 -0.58518199999999998
		0 0 -0.59421000000000002
		0 0.103183 -0.58518199999999998
		0 0.203232 -0.55837499999999995
		0 0.29710500000000001 -0.51460099999999998
		0 0.38195000000000001 -0.45519100000000001
		0 0.45519100000000001 -0.38195099999999998
		0 0.51460099999999998 -0.29710500000000001
		0 0.55837400000000004 -0.203232
		0 0.58518199999999998 -0.103183
		0 0.59420899999999999 0
		0.103183 0.58518199999999998 0
		0.203232 0.55837400000000004 0
		0.29710500000000001 0.51460099999999998 0
		0.38195099999999998 0.45519100000000001 0
		0.45519100000000001 0.38195000000000001 0
		0.51460099999999998 0.29710500000000001 0
		0.55837400000000004 0.203232 0
		0.58518199999999998 0.103183 0
		0.59420899999999999 0 0
		0.58518199999999998 -0.103183 0
		0.55837400000000004 -0.203232 0
		0.51460099999999998 -0.29710500000000001 0
		0.45519100000000001 -0.38195000000000001 0
		0.38195099999999998 -0.45519100000000001 0
		0.29710500000000001 -0.51460099999999998 0
		0.203232 -0.55837400000000004 0
		0.103183 -0.58518199999999998 0
		0 -0.59420899999999999 0
		-0.103183 -0.58518199999999998 0
		-0.203232 -0.55837400000000004 0
		-0.29710500000000001 -0.51460099999999998 0
		-0.38195099999999998 -0.45519100000000001 0
		-0.45519100000000001 -0.38195000000000001 0
		-0.51460099999999998 -0.29710500000000001 0
		-0.55837400000000004 -0.203232 0
		-0.58518199999999998 -0.103183 0
		-0.59421000000000002 0 0
		-0.58518199999999998 0.103183 0
		-0.55837400000000004 0.203232 0
		-0.51460099999999998 0.29710500000000001 0
		-0.45519100000000001 0.38195000000000001 0
		-0.38195099999999998 0.45519100000000001 0
		-0.29710500000000001 0.51460099999999998 0
		-0.203232 0.55837400000000004 0
		-0.103183 0.58518199999999998 0
		0 0.59420899999999999 0
		-3.0751100000000001e-09 0.58518199999999998 0.103183
		-6.0567700000000004e-09 0.55837400000000004 0.203232
		-8.8544099999999994e-09 0.51460099999999998 0.29710500000000001
		-1.1383e-08 0.45519100000000001 0.38195099999999998
		-1.3565700000000001e-08 0.38195000000000001 0.45519100000000001
		-1.5336300000000002e-08 0.29710500000000001 0.51460099999999998
		-1.6640900000000001e-08 0.203232 0.55837400000000004
		-1.7439800000000002e-08 0.103183 0.58518199999999998
		-1.7708799999999999e-08 0 0.59421000000000002
		-0.18362100000000001 0 0.56512700000000005
		-0.34926800000000002 0 0.48072599999999999
		-0.48072599999999999 0 0.34926800000000002
		-0.56512700000000005 0 0.18362100000000001
		-0.59421000000000002 0 0
		-0.56512700000000005 0 -0.18362100000000001
		-0.48072599999999999 0 -0.34926800000000002
		-0.34926800000000002 0 -0.48072599999999999
		-0.18362100000000001 0 -0.56512700000000005
		0 0 -0.59421000000000002
		0.18362100000000001 0 -0.56512700000000005
		0.34926800000000002 0 -0.48072599999999999
		0.48072599999999999 0 -0.34926800000000002
		0.56512700000000005 0 -0.18362100000000001
		0.59420899999999999 0 0
		0.56512700000000005 0 0.18362100000000001
		0.48072599999999999 0 0.34926800000000002
		0.34926800000000002 0 0.48072599999999999
		0.18362100000000001 0 0.56512700000000005
		-1.7708799999999999e-08 0 0.59421000000000002
		;
createNode nurbsCurve -n "UpperTeeth_Guide_Ctrl_Ctrl_CtrlShape" -p "UpperTeeth_Guide";
	rename -uid "BC74DE4A-4FCE-B888-E027-6F80644AB479";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2026/scripts/Mutant_Tools/Icons/";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".hpb" yes;
	setAttr ".ovc" 13;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 9 0 no 3
		10 0 1 2 3 4 5 6 7 8 9
		10
		-0.5 -0.25 -1.3977299999999999e-05
		0.94513100000000005 -0.25591599999999998 -1.3977299999999999e-05
		0.739653 -0.50644299999999998 -1.3977299999999999e-05
		0.99017999999999995 -0.93915099999999996 -1.3977299999999999e-05
		2.299302 -3.8742999999999997e-07 -1.37985e-05
		0.99018099999999998 0.93915099999999996 -1.3977299999999999e-05
		0.739653 0.50644199999999995 -1.3977299999999999e-05
		0.94513100000000005 0.25322099999999997 -7.1674600000000002e-06
		-0.5 0.25 -1.3977299999999999e-05
		-0.5 -0.25 -1.3977299999999999e-05
		;
createNode nurbsCurve -n "UpperTeeth_Guide_Ctrl_Ctrl_Ctrl_CtrlShape" -p "UpperTeeth_Guide";
	rename -uid "98634934-4117-61F0-187E-E2A7F2D23502";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2026/scripts/Mutant_Tools/Icons/";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".hpb" yes;
	setAttr ".ovc" 6;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 9 0 no 3
		10 0 1 2 3 4 5 6 7 8 9
		10
		0.25 1.3977299999999999e-05 -0.5
		0.25591599999999998 1.3977299999999999e-05 0.94513100000000005
		0.50644299999999998 1.3977299999999999e-05 0.739653
		0.93915099999999996 1.3977299999999999e-05 0.99017999999999995
		3.8742999999999997e-07 1.37985e-05 2.299302
		-0.93915099999999996 1.3977299999999999e-05 0.99018099999999998
		-0.50644199999999995 1.3977299999999999e-05 0.739653
		-0.25322099999999997 7.1674600000000002e-06 0.94513100000000005
		-0.25 1.3977299999999999e-05 -0.5
		0.25 1.3977299999999999e-05 -0.5
		;
createNode dagContainer -n "LowerTeeth_Block" -p "Face";
	rename -uid "40215D93-4F6A-5475-AB1B-E9A5764DC382";
	addAttr -ci true -sn "nts" -ln "notes" -dt "string";
	setAttr ".isc" yes;
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2026/scripts/Mutant_Tools/Icons/Chain.png";
	setAttr ".ctor" -type "string" "rodri";
	setAttr ".cdat" -type "string" "2025/12/16 15:42:26";
	setAttr -l on -k off ".v";
	setAttr -l on -k off ".tx";
	setAttr -l on -k off ".ty";
	setAttr -l on -k off ".tz";
	setAttr -l on -k off ".rx";
	setAttr -l on -k off ".ry";
	setAttr -l on -k off ".rz";
	setAttr -l on -k off ".sx";
	setAttr -l on -k off ".sy";
	setAttr -l on -k off ".sz";
	setAttr ".nts" -type "string" "['LowerTeeth_Rig_Grp_parentConstraint1', 'LowerTeeth_Ctrl_Offset_Grp_parentConstraint1', 'LowerTeeth_Jnt_Ctrl_tag', 'LowerTeeth_Ctrl_Grp', 'LowerTeeth_Bnd', 'LowerTeeth_Ctrl', 'LowerTeeth_Jnt', 'LowerTeeth_CtrlShape', 'LowerTeeth_Ctrl_Offset_Grp_scaleConstraint1', 'LowerTeeth_Jnt_parentConstraint1', 'LowerTeeth_Bnd_parentConstraint1', 'LowerTeeth_Rig_Grp', 'LowerTeeth_Bnd_scaleConstraint1', 'LowerTeeth_Rig_Grp_scaleConstraint1', 'LowerTeeth_Ctrl_Offset_Grp']";
createNode joint -n "LowerTeeth_Guide" -p "LowerTeeth_Block";
	rename -uid "45049992-443D-724C-445F-3A816B22AF71";
	addAttr -ci true -sn "Helper" -ln "Helper" -min 0 -max 1 -en "Hide:Show" -at "enum";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2026/scripts/Mutant_Tools/Icons/";
	setAttr ".t" -type "double3" 0 166.08859252929688 15.218119613713803 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr -cb on ".Helper" 1;
createNode nurbsCurve -n "LowerTeeth_Guide_CtrlShape" -p "LowerTeeth_Guide";
	rename -uid "432942A4-4E0A-68A0-7B30-D795F16D5B0C";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2026/scripts/Mutant_Tools/Icons/";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".hpb" yes;
	setAttr ".ovc" 14;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 9 0 no 3
		10 0 1 2 3 4 5 6 7 8 9
		10
		1.3977299999999999e-05 -0.5 0.25
		1.3977299999999999e-05 0.94513100000000005 0.25591599999999998
		1.3977299999999999e-05 0.739653 0.50644299999999998
		1.3977299999999999e-05 0.99017999999999995 0.93915099999999996
		1.37985e-05 2.299302 3.8742999999999997e-07
		1.3977299999999999e-05 0.99018099999999998 -0.93915099999999996
		1.3977299999999999e-05 0.739653 -0.50644199999999995
		7.1674600000000002e-06 0.94513100000000005 -0.25322099999999997
		1.3977299999999999e-05 -0.5 -0.25
		1.3977299999999999e-05 -0.5 0.25
		;
createNode nurbsCurve -n "LowerTeeth_Guide_Ctrl_CtrlShape" -p "LowerTeeth_Guide";
	rename -uid "350D7F1F-4917-EFEA-5746-4496C6F7783F";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2026/scripts/Mutant_Tools/Icons/";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".hpb" yes;
	setAttr ".ovc" 18;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 101 0 no 3
		102 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27
		 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54
		 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81
		 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99 100 101
		102
		0 0.59420899999999999 0
		-3.0751100000000001e-09 0.58518199999999998 0.103183
		-6.0567700000000004e-09 0.55837400000000004 0.203232
		-8.8544099999999994e-09 0.51460099999999998 0.29710500000000001
		-1.1383e-08 0.45519100000000001 0.38195099999999998
		-1.3565700000000001e-08 0.38195000000000001 0.45519100000000001
		-1.5336300000000002e-08 0.29710500000000001 0.51460099999999998
		-1.6640900000000001e-08 0.203232 0.55837400000000004
		-1.7439800000000002e-08 0.103183 0.58518199999999998
		-1.7708799999999999e-08 0 0.59421000000000002
		-1.7439800000000002e-08 -0.103183 0.58518199999999998
		-1.6640900000000001e-08 -0.203232 0.55837400000000004
		-1.5336300000000002e-08 -0.29710500000000001 0.51460099999999998
		-1.3565700000000001e-08 -0.38195000000000001 0.45519100000000001
		-1.1383e-08 -0.45519100000000001 0.38195099999999998
		-8.8544099999999994e-09 -0.51460099999999998 0.29710500000000001
		-6.0567700000000004e-09 -0.55837400000000004 0.203232
		-3.0751100000000001e-09 -0.58518199999999998 0.103183
		0 -0.59420899999999999 0
		0 -0.58518199999999998 -0.103183
		0 -0.55837400000000004 -0.203232
		0 -0.51460099999999998 -0.29710500000000001
		0 -0.45519100000000001 -0.38195099999999998
		0 -0.38195000000000001 -0.45519100000000001
		0 -0.29710500000000001 -0.51460099999999998
		0 -0.203232 -0.55837499999999995
		0 -0.103183 -0.58518199999999998
		0 0 -0.59421000000000002
		0 0.103183 -0.58518199999999998
		0 0.203232 -0.55837499999999995
		0 0.29710500000000001 -0.51460099999999998
		0 0.38195000000000001 -0.45519100000000001
		0 0.45519100000000001 -0.38195099999999998
		0 0.51460099999999998 -0.29710500000000001
		0 0.55837400000000004 -0.203232
		0 0.58518199999999998 -0.103183
		0 0.59420899999999999 0
		0.103183 0.58518199999999998 0
		0.203232 0.55837400000000004 0
		0.29710500000000001 0.51460099999999998 0
		0.38195099999999998 0.45519100000000001 0
		0.45519100000000001 0.38195000000000001 0
		0.51460099999999998 0.29710500000000001 0
		0.55837400000000004 0.203232 0
		0.58518199999999998 0.103183 0
		0.59420899999999999 0 0
		0.58518199999999998 -0.103183 0
		0.55837400000000004 -0.203232 0
		0.51460099999999998 -0.29710500000000001 0
		0.45519100000000001 -0.38195000000000001 0
		0.38195099999999998 -0.45519100000000001 0
		0.29710500000000001 -0.51460099999999998 0
		0.203232 -0.55837400000000004 0
		0.103183 -0.58518199999999998 0
		0 -0.59420899999999999 0
		-0.103183 -0.58518199999999998 0
		-0.203232 -0.55837400000000004 0
		-0.29710500000000001 -0.51460099999999998 0
		-0.38195099999999998 -0.45519100000000001 0
		-0.45519100000000001 -0.38195000000000001 0
		-0.51460099999999998 -0.29710500000000001 0
		-0.55837400000000004 -0.203232 0
		-0.58518199999999998 -0.103183 0
		-0.59421000000000002 0 0
		-0.58518199999999998 0.103183 0
		-0.55837400000000004 0.203232 0
		-0.51460099999999998 0.29710500000000001 0
		-0.45519100000000001 0.38195000000000001 0
		-0.38195099999999998 0.45519100000000001 0
		-0.29710500000000001 0.51460099999999998 0
		-0.203232 0.55837400000000004 0
		-0.103183 0.58518199999999998 0
		0 0.59420899999999999 0
		-3.0751100000000001e-09 0.58518199999999998 0.103183
		-6.0567700000000004e-09 0.55837400000000004 0.203232
		-8.8544099999999994e-09 0.51460099999999998 0.29710500000000001
		-1.1383e-08 0.45519100000000001 0.38195099999999998
		-1.3565700000000001e-08 0.38195000000000001 0.45519100000000001
		-1.5336300000000002e-08 0.29710500000000001 0.51460099999999998
		-1.6640900000000001e-08 0.203232 0.55837400000000004
		-1.7439800000000002e-08 0.103183 0.58518199999999998
		-1.7708799999999999e-08 0 0.59421000000000002
		-0.18362100000000001 0 0.56512700000000005
		-0.34926800000000002 0 0.48072599999999999
		-0.48072599999999999 0 0.34926800000000002
		-0.56512700000000005 0 0.18362100000000001
		-0.59421000000000002 0 0
		-0.56512700000000005 0 -0.18362100000000001
		-0.48072599999999999 0 -0.34926800000000002
		-0.34926800000000002 0 -0.48072599999999999
		-0.18362100000000001 0 -0.56512700000000005
		0 0 -0.59421000000000002
		0.18362100000000001 0 -0.56512700000000005
		0.34926800000000002 0 -0.48072599999999999
		0.48072599999999999 0 -0.34926800000000002
		0.56512700000000005 0 -0.18362100000000001
		0.59420899999999999 0 0
		0.56512700000000005 0 0.18362100000000001
		0.48072599999999999 0 0.34926800000000002
		0.34926800000000002 0 0.48072599999999999
		0.18362100000000001 0 0.56512700000000005
		-1.7708799999999999e-08 0 0.59421000000000002
		;
createNode nurbsCurve -n "LowerTeeth_Guide_Ctrl_Ctrl_CtrlShape" -p "LowerTeeth_Guide";
	rename -uid "B2E90BB7-4643-A46F-1488-4AB6B99E634A";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2026/scripts/Mutant_Tools/Icons/";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".hpb" yes;
	setAttr ".ovc" 13;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 9 0 no 3
		10 0 1 2 3 4 5 6 7 8 9
		10
		-0.5 -0.25 -1.3977299999999999e-05
		0.94513100000000005 -0.25591599999999998 -1.3977299999999999e-05
		0.739653 -0.50644299999999998 -1.3977299999999999e-05
		0.99017999999999995 -0.93915099999999996 -1.3977299999999999e-05
		2.299302 -3.8742999999999997e-07 -1.37985e-05
		0.99018099999999998 0.93915099999999996 -1.3977299999999999e-05
		0.739653 0.50644199999999995 -1.3977299999999999e-05
		0.94513100000000005 0.25322099999999997 -7.1674600000000002e-06
		-0.5 0.25 -1.3977299999999999e-05
		-0.5 -0.25 -1.3977299999999999e-05
		;
createNode nurbsCurve -n "LowerTeeth_Guide_Ctrl_Ctrl_Ctrl_CtrlShape" -p "LowerTeeth_Guide";
	rename -uid "8965DCC7-4990-40D4-C2E4-2B9E6E4C84E4";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2026/scripts/Mutant_Tools/Icons/";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".hpb" yes;
	setAttr ".ovc" 6;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 9 0 no 3
		10 0 1 2 3 4 5 6 7 8 9
		10
		0.25 1.3977299999999999e-05 -0.5
		0.25591599999999998 1.3977299999999999e-05 0.94513100000000005
		0.50644299999999998 1.3977299999999999e-05 0.739653
		0.93915099999999996 1.3977299999999999e-05 0.99017999999999995
		3.8742999999999997e-07 1.37985e-05 2.299302
		-0.93915099999999996 1.3977299999999999e-05 0.99018099999999998
		-0.50644199999999995 1.3977299999999999e-05 0.739653
		-0.25322099999999997 7.1674600000000002e-06 0.94513100000000005
		-0.25 1.3977299999999999e-05 -0.5
		0.25 1.3977299999999999e-05 -0.5
		;
createNode dagContainer -n "Tongue_Block" -p "Face";
	rename -uid "0B213220-49EA-57ED-F805-2A8474DDF035";
	addAttr -ci true -sn "nts" -ln "notes" -dt "string";
	setAttr ".isc" yes;
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2026/scripts/Mutant_Tools/Icons/Chain.png";
	setAttr ".ctor" -type "string" "rodri";
	setAttr ".cdat" -type "string" "2025/12/16 15:42:37";
	setAttr -l on -k off ".v";
	setAttr -l on -k off ".tx";
	setAttr -l on -k off ".ty";
	setAttr -l on -k off ".tz";
	setAttr -l on -k off ".rx";
	setAttr -l on -k off ".ry";
	setAttr -l on -k off ".rz";
	setAttr -l on -k off ".sx";
	setAttr -l on -k off ".sy";
	setAttr -l on -k off ".sz";
	setAttr ".nts" -type "string" (
		"['Tongue_B_Jnt_parentConstraint1', 'Tongue_D_CtrlAutoRotate_Grp', 'Tongue_B_Bnd_parentConstraint1', 'Tongue_Rig_Grp_parentConstraint1', 'Tongue_B_Bnd', 'Tongue_A_Bnd', 'Tongue_A_Ctrl', 'Tongue_A_Rotator_Ctrl_Root_Grp', 'Tongue_B_Jnt_Ctrl_tag', 'Tongue_C_Ctrl', 'Tongue_C_Bnd_scaleConstraint1', 'Tongue_A_Jnt_parentConstraint1', 'Tongue_B_Jnt', 'Tongue_Rig_Grp', 'Tongue_D_Bnd', 'Tongue_D_Ctrl_Auto_Grp', 'Tongue_C_Bnd_parentConstraint1', 'Tongue_A_Ctrl_Offset_Grp_scaleConstraint1', 'Tongue_Ctrl_Grp', 'Tongue_A_CtrlAutoRotate_Grp', 'Tongue_A_Ctrl_Offset_Grp_parentConstraint1', 'Tongue_B_Ctrl_Auto_Grp', 'Tongue_B_Ctrl_Offset_Grp', 'Tongue_D_Bnd_scaleConstraint1', 'Tongue_A_Ctrl_Offset_Grp', 'Tongue_C_Jnt_Ctrl_tag', 'Tongue_C_Bnd', 'Tongue_C_Ctrl_Root_Grp', 'Tongue_A_Rotator_Ctrl_tag', 'Tongue_C_Jnt', 'Tongue_D_Ctrl', 'Tongue_A_Bnd_scaleConstraint1', 'Tongue_A_Bnd_parentConstraint1', 'Tongue_B_CtrlShape', 'Tongue_D_Ctrl_Root_Grp', 'Tongue_Rig_Grp_scaleConstraint1', 'Tongue_A_Jnt', 'Tongue_A_Ctrl_Root_Grp', 'Tongue_C_Jnt_parentConstraint1', 'Tongue_C_Ctrl_Auto_Grp', 'Tongue_B_Ctrl', 'Tongue_C_CtrlShape', 'Tongue_C_Ctrl_Offset_Grp', 'Tongue_A_Rotator_Ctrl', 'Tongue_A_Jnt_Ctrl_tag', 'Tongue_A_Rotator_CtrlShape', 'Tongue_D_Jnt_Ctrl_tag', 'Tongue_D_CtrlShape', 'Tongue_D_Bnd_parentConstraint1', 'Tongue_A_CtrlShape', 'Tongue_A_Rotator_Ctrl_Auto_Grp', 'Tongue_B_CtrlAutoRotate_Grp', 'Tongue_D_Jnt', 'Tongue_D_Jnt_parentConstraint1', 'Tongue_C_CtrlAutoRotate_Grp', 'Tongue_B_Ctrl_Root_Grp', 'Tongue_B_Bnd_scaleConstraint1', 'Tongue_D_Ctrl_Offset_Grp', 'Tongue_A_Ctrl_Auto_Grp']");
createNode joint -n "Tongue_A_Guide" -p "Tongue_Block";
	rename -uid "A757694B-43FC-747E-58D3-FAAD8116FE0F";
	addAttr -ci true -sn "Helper" -ln "Helper" -min 0 -max 1 -en "Hide:Show" -at "enum";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2026/scripts/Mutant_Tools/Icons/";
	setAttr ".t" -type "double3" 0.020846009254455566 163.1901017019926 4.7670431137084961 ;
	setAttr ".r" -type "double3" -90 -32.687643489589895 90 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr -cb on ".Helper" 1;
createNode nurbsCurve -n "Tongue_A_Guide_CtrlShape" -p "Tongue_A_Guide";
	rename -uid "90E8D21E-4E63-265C-BD69-27A2AEB7F551";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2026/scripts/Mutant_Tools/Icons/";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".hpb" yes;
	setAttr ".ovc" 14;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 9 0 no 3
		10 0 1 2 3 4 5 6 7 8 9
		10
		1.3977299999999999e-05 -0.5 0.25
		1.3977299999999999e-05 0.94513100000000005 0.25591599999999998
		1.3977299999999999e-05 0.739653 0.50644299999999998
		1.3977299999999999e-05 0.99017999999999995 0.93915099999999996
		1.37985e-05 2.299302 3.8742999999999997e-07
		1.3977299999999999e-05 0.99018099999999998 -0.93915099999999996
		1.3977299999999999e-05 0.739653 -0.50644199999999995
		7.1674600000000002e-06 0.94513100000000005 -0.25322099999999997
		1.3977299999999999e-05 -0.5 -0.25
		1.3977299999999999e-05 -0.5 0.25
		;
createNode nurbsCurve -n "Tongue_A_Guide_Ctrl_CtrlShape" -p "Tongue_A_Guide";
	rename -uid "BA86BC7D-428D-A0C7-2224-459AD47EE376";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2026/scripts/Mutant_Tools/Icons/";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".hpb" yes;
	setAttr ".ovc" 18;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 101 0 no 3
		102 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27
		 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54
		 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81
		 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99 100 101
		102
		0 0.59420899999999999 0
		-3.0751100000000001e-09 0.58518199999999998 0.103183
		-6.0567700000000004e-09 0.55837400000000004 0.203232
		-8.8544099999999994e-09 0.51460099999999998 0.29710500000000001
		-1.1383e-08 0.45519100000000001 0.38195099999999998
		-1.3565700000000001e-08 0.38195000000000001 0.45519100000000001
		-1.5336300000000002e-08 0.29710500000000001 0.51460099999999998
		-1.6640900000000001e-08 0.203232 0.55837400000000004
		-1.7439800000000002e-08 0.103183 0.58518199999999998
		-1.7708799999999999e-08 0 0.59421000000000002
		-1.7439800000000002e-08 -0.103183 0.58518199999999998
		-1.6640900000000001e-08 -0.203232 0.55837400000000004
		-1.5336300000000002e-08 -0.29710500000000001 0.51460099999999998
		-1.3565700000000001e-08 -0.38195000000000001 0.45519100000000001
		-1.1383e-08 -0.45519100000000001 0.38195099999999998
		-8.8544099999999994e-09 -0.51460099999999998 0.29710500000000001
		-6.0567700000000004e-09 -0.55837400000000004 0.203232
		-3.0751100000000001e-09 -0.58518199999999998 0.103183
		0 -0.59420899999999999 0
		0 -0.58518199999999998 -0.103183
		0 -0.55837400000000004 -0.203232
		0 -0.51460099999999998 -0.29710500000000001
		0 -0.45519100000000001 -0.38195099999999998
		0 -0.38195000000000001 -0.45519100000000001
		0 -0.29710500000000001 -0.51460099999999998
		0 -0.203232 -0.55837499999999995
		0 -0.103183 -0.58518199999999998
		0 0 -0.59421000000000002
		0 0.103183 -0.58518199999999998
		0 0.203232 -0.55837499999999995
		0 0.29710500000000001 -0.51460099999999998
		0 0.38195000000000001 -0.45519100000000001
		0 0.45519100000000001 -0.38195099999999998
		0 0.51460099999999998 -0.29710500000000001
		0 0.55837400000000004 -0.203232
		0 0.58518199999999998 -0.103183
		0 0.59420899999999999 0
		0.103183 0.58518199999999998 0
		0.203232 0.55837400000000004 0
		0.29710500000000001 0.51460099999999998 0
		0.38195099999999998 0.45519100000000001 0
		0.45519100000000001 0.38195000000000001 0
		0.51460099999999998 0.29710500000000001 0
		0.55837400000000004 0.203232 0
		0.58518199999999998 0.103183 0
		0.59420899999999999 0 0
		0.58518199999999998 -0.103183 0
		0.55837400000000004 -0.203232 0
		0.51460099999999998 -0.29710500000000001 0
		0.45519100000000001 -0.38195000000000001 0
		0.38195099999999998 -0.45519100000000001 0
		0.29710500000000001 -0.51460099999999998 0
		0.203232 -0.55837400000000004 0
		0.103183 -0.58518199999999998 0
		0 -0.59420899999999999 0
		-0.103183 -0.58518199999999998 0
		-0.203232 -0.55837400000000004 0
		-0.29710500000000001 -0.51460099999999998 0
		-0.38195099999999998 -0.45519100000000001 0
		-0.45519100000000001 -0.38195000000000001 0
		-0.51460099999999998 -0.29710500000000001 0
		-0.55837400000000004 -0.203232 0
		-0.58518199999999998 -0.103183 0
		-0.59421000000000002 0 0
		-0.58518199999999998 0.103183 0
		-0.55837400000000004 0.203232 0
		-0.51460099999999998 0.29710500000000001 0
		-0.45519100000000001 0.38195000000000001 0
		-0.38195099999999998 0.45519100000000001 0
		-0.29710500000000001 0.51460099999999998 0
		-0.203232 0.55837400000000004 0
		-0.103183 0.58518199999999998 0
		0 0.59420899999999999 0
		-3.0751100000000001e-09 0.58518199999999998 0.103183
		-6.0567700000000004e-09 0.55837400000000004 0.203232
		-8.8544099999999994e-09 0.51460099999999998 0.29710500000000001
		-1.1383e-08 0.45519100000000001 0.38195099999999998
		-1.3565700000000001e-08 0.38195000000000001 0.45519100000000001
		-1.5336300000000002e-08 0.29710500000000001 0.51460099999999998
		-1.6640900000000001e-08 0.203232 0.55837400000000004
		-1.7439800000000002e-08 0.103183 0.58518199999999998
		-1.7708799999999999e-08 0 0.59421000000000002
		-0.18362100000000001 0 0.56512700000000005
		-0.34926800000000002 0 0.48072599999999999
		-0.48072599999999999 0 0.34926800000000002
		-0.56512700000000005 0 0.18362100000000001
		-0.59421000000000002 0 0
		-0.56512700000000005 0 -0.18362100000000001
		-0.48072599999999999 0 -0.34926800000000002
		-0.34926800000000002 0 -0.48072599999999999
		-0.18362100000000001 0 -0.56512700000000005
		0 0 -0.59421000000000002
		0.18362100000000001 0 -0.56512700000000005
		0.34926800000000002 0 -0.48072599999999999
		0.48072599999999999 0 -0.34926800000000002
		0.56512700000000005 0 -0.18362100000000001
		0.59420899999999999 0 0
		0.56512700000000005 0 0.18362100000000001
		0.48072599999999999 0 0.34926800000000002
		0.34926800000000002 0 0.48072599999999999
		0.18362100000000001 0 0.56512700000000005
		-1.7708799999999999e-08 0 0.59421000000000002
		;
createNode nurbsCurve -n "Tongue_A_Guide_Ctrl_Ctrl_CtrlShape" -p "Tongue_A_Guide";
	rename -uid "9EAC0C9C-4D89-6EA2-38EA-F78265743DDB";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2026/scripts/Mutant_Tools/Icons/";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".hpb" yes;
	setAttr ".ovc" 13;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 9 0 no 3
		10 0 1 2 3 4 5 6 7 8 9
		10
		-0.5 -0.25 -1.3977299999999999e-05
		0.94513100000000005 -0.25591599999999998 -1.3977299999999999e-05
		0.739653 -0.50644299999999998 -1.3977299999999999e-05
		0.99017999999999995 -0.93915099999999996 -1.3977299999999999e-05
		2.299302 -3.8742999999999997e-07 -1.37985e-05
		0.99018099999999998 0.93915099999999996 -1.3977299999999999e-05
		0.739653 0.50644199999999995 -1.3977299999999999e-05
		0.94513100000000005 0.25322099999999997 -7.1674600000000002e-06
		-0.5 0.25 -1.3977299999999999e-05
		-0.5 -0.25 -1.3977299999999999e-05
		;
createNode nurbsCurve -n "Tongue_A_Guide_Ctrl_Ctrl_Ctrl_CtrlShape" -p "Tongue_A_Guide";
	rename -uid "001EA905-4D27-00C0-FF97-8384016CCC91";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2026/scripts/Mutant_Tools/Icons/";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".hpb" yes;
	setAttr ".ovc" 6;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 9 0 no 3
		10 0 1 2 3 4 5 6 7 8 9
		10
		0.25 1.3977299999999999e-05 -0.5
		0.25591599999999998 1.3977299999999999e-05 0.94513100000000005
		0.50644299999999998 1.3977299999999999e-05 0.739653
		0.93915099999999996 1.3977299999999999e-05 0.99017999999999995
		3.8742999999999997e-07 1.37985e-05 2.299302
		-0.93915099999999996 1.3977299999999999e-05 0.99018099999999998
		-0.50644199999999995 1.3977299999999999e-05 0.739653
		-0.25322099999999997 7.1674600000000002e-06 0.94513100000000005
		-0.25 1.3977299999999999e-05 -0.5
		0.25 1.3977299999999999e-05 -0.5
		;
createNode joint -n "Tongue_B_Guide" -p "Tongue_A_Guide";
	rename -uid "178DCA8D-4E71-CB4D-0452-099326A201E6";
	addAttr -ci true -sn "Helper" -ln "Helper" -min 0 -max 1 -en "Hide:Show" -at "enum";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2026/scripts/Mutant_Tools/Icons/";
	setAttr ".t" -type "double3" 3.1703509931005343 -2.8421709430404007e-14 -6.7679501978978709e-19 ;
	setAttr ".r" -type "double3" 0 0 -30.835565168564891 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr -cb on ".Helper" 1;
createNode nurbsCurve -n "Tongue_B_Guide_CtrlShape" -p "Tongue_B_Guide";
	rename -uid "2FB5DA31-4EF2-D5A1-C984-6DBD82A032F6";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2026/scripts/Mutant_Tools/Icons/";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".hpb" yes;
	setAttr ".ovc" 14;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 9 0 no 3
		10 0 1 2 3 4 5 6 7 8 9
		10
		1.3977299999999999e-05 -0.5 0.25
		1.3977299999999999e-05 0.94513100000000005 0.25591599999999998
		1.3977299999999999e-05 0.739653 0.50644299999999998
		1.3977299999999999e-05 0.99017999999999995 0.93915099999999996
		1.37985e-05 2.299302 3.8742999999999997e-07
		1.3977299999999999e-05 0.99018099999999998 -0.93915099999999996
		1.3977299999999999e-05 0.739653 -0.50644199999999995
		7.1674600000000002e-06 0.94513100000000005 -0.25322099999999997
		1.3977299999999999e-05 -0.5 -0.25
		1.3977299999999999e-05 -0.5 0.25
		;
createNode nurbsCurve -n "Tongue_B_Guide_Ctrl_CtrlShape" -p "Tongue_B_Guide";
	rename -uid "E2CFC5DC-4825-D487-60D9-CFBC67151FC3";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2026/scripts/Mutant_Tools/Icons/";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".hpb" yes;
	setAttr ".ovc" 18;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 101 0 no 3
		102 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27
		 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54
		 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81
		 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99 100 101
		102
		0 0.59420899999999999 0
		-3.0751100000000001e-09 0.58518199999999998 0.103183
		-6.0567700000000004e-09 0.55837400000000004 0.203232
		-8.8544099999999994e-09 0.51460099999999998 0.29710500000000001
		-1.1383e-08 0.45519100000000001 0.38195099999999998
		-1.3565700000000001e-08 0.38195000000000001 0.45519100000000001
		-1.5336300000000002e-08 0.29710500000000001 0.51460099999999998
		-1.6640900000000001e-08 0.203232 0.55837400000000004
		-1.7439800000000002e-08 0.103183 0.58518199999999998
		-1.7708799999999999e-08 0 0.59421000000000002
		-1.7439800000000002e-08 -0.103183 0.58518199999999998
		-1.6640900000000001e-08 -0.203232 0.55837400000000004
		-1.5336300000000002e-08 -0.29710500000000001 0.51460099999999998
		-1.3565700000000001e-08 -0.38195000000000001 0.45519100000000001
		-1.1383e-08 -0.45519100000000001 0.38195099999999998
		-8.8544099999999994e-09 -0.51460099999999998 0.29710500000000001
		-6.0567700000000004e-09 -0.55837400000000004 0.203232
		-3.0751100000000001e-09 -0.58518199999999998 0.103183
		0 -0.59420899999999999 0
		0 -0.58518199999999998 -0.103183
		0 -0.55837400000000004 -0.203232
		0 -0.51460099999999998 -0.29710500000000001
		0 -0.45519100000000001 -0.38195099999999998
		0 -0.38195000000000001 -0.45519100000000001
		0 -0.29710500000000001 -0.51460099999999998
		0 -0.203232 -0.55837499999999995
		0 -0.103183 -0.58518199999999998
		0 0 -0.59421000000000002
		0 0.103183 -0.58518199999999998
		0 0.203232 -0.55837499999999995
		0 0.29710500000000001 -0.51460099999999998
		0 0.38195000000000001 -0.45519100000000001
		0 0.45519100000000001 -0.38195099999999998
		0 0.51460099999999998 -0.29710500000000001
		0 0.55837400000000004 -0.203232
		0 0.58518199999999998 -0.103183
		0 0.59420899999999999 0
		0.103183 0.58518199999999998 0
		0.203232 0.55837400000000004 0
		0.29710500000000001 0.51460099999999998 0
		0.38195099999999998 0.45519100000000001 0
		0.45519100000000001 0.38195000000000001 0
		0.51460099999999998 0.29710500000000001 0
		0.55837400000000004 0.203232 0
		0.58518199999999998 0.103183 0
		0.59420899999999999 0 0
		0.58518199999999998 -0.103183 0
		0.55837400000000004 -0.203232 0
		0.51460099999999998 -0.29710500000000001 0
		0.45519100000000001 -0.38195000000000001 0
		0.38195099999999998 -0.45519100000000001 0
		0.29710500000000001 -0.51460099999999998 0
		0.203232 -0.55837400000000004 0
		0.103183 -0.58518199999999998 0
		0 -0.59420899999999999 0
		-0.103183 -0.58518199999999998 0
		-0.203232 -0.55837400000000004 0
		-0.29710500000000001 -0.51460099999999998 0
		-0.38195099999999998 -0.45519100000000001 0
		-0.45519100000000001 -0.38195000000000001 0
		-0.51460099999999998 -0.29710500000000001 0
		-0.55837400000000004 -0.203232 0
		-0.58518199999999998 -0.103183 0
		-0.59421000000000002 0 0
		-0.58518199999999998 0.103183 0
		-0.55837400000000004 0.203232 0
		-0.51460099999999998 0.29710500000000001 0
		-0.45519100000000001 0.38195000000000001 0
		-0.38195099999999998 0.45519100000000001 0
		-0.29710500000000001 0.51460099999999998 0
		-0.203232 0.55837400000000004 0
		-0.103183 0.58518199999999998 0
		0 0.59420899999999999 0
		-3.0751100000000001e-09 0.58518199999999998 0.103183
		-6.0567700000000004e-09 0.55837400000000004 0.203232
		-8.8544099999999994e-09 0.51460099999999998 0.29710500000000001
		-1.1383e-08 0.45519100000000001 0.38195099999999998
		-1.3565700000000001e-08 0.38195000000000001 0.45519100000000001
		-1.5336300000000002e-08 0.29710500000000001 0.51460099999999998
		-1.6640900000000001e-08 0.203232 0.55837400000000004
		-1.7439800000000002e-08 0.103183 0.58518199999999998
		-1.7708799999999999e-08 0 0.59421000000000002
		-0.18362100000000001 0 0.56512700000000005
		-0.34926800000000002 0 0.48072599999999999
		-0.48072599999999999 0 0.34926800000000002
		-0.56512700000000005 0 0.18362100000000001
		-0.59421000000000002 0 0
		-0.56512700000000005 0 -0.18362100000000001
		-0.48072599999999999 0 -0.34926800000000002
		-0.34926800000000002 0 -0.48072599999999999
		-0.18362100000000001 0 -0.56512700000000005
		0 0 -0.59421000000000002
		0.18362100000000001 0 -0.56512700000000005
		0.34926800000000002 0 -0.48072599999999999
		0.48072599999999999 0 -0.34926800000000002
		0.56512700000000005 0 -0.18362100000000001
		0.59420899999999999 0 0
		0.56512700000000005 0 0.18362100000000001
		0.48072599999999999 0 0.34926800000000002
		0.34926800000000002 0 0.48072599999999999
		0.18362100000000001 0 0.56512700000000005
		-1.7708799999999999e-08 0 0.59421000000000002
		;
createNode nurbsCurve -n "Tongue_B_Guide_Ctrl_Ctrl_CtrlShape" -p "Tongue_B_Guide";
	rename -uid "18CC48A6-4EF0-7E89-0E10-B29D1624E0B3";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2026/scripts/Mutant_Tools/Icons/";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".hpb" yes;
	setAttr ".ovc" 13;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 9 0 no 3
		10 0 1 2 3 4 5 6 7 8 9
		10
		-0.5 -0.25 -1.3977299999999999e-05
		0.94513100000000005 -0.25591599999999998 -1.3977299999999999e-05
		0.739653 -0.50644299999999998 -1.3977299999999999e-05
		0.99017999999999995 -0.93915099999999996 -1.3977299999999999e-05
		2.299302 -3.8742999999999997e-07 -1.37985e-05
		0.99018099999999998 0.93915099999999996 -1.3977299999999999e-05
		0.739653 0.50644199999999995 -1.3977299999999999e-05
		0.94513100000000005 0.25322099999999997 -7.1674600000000002e-06
		-0.5 0.25 -1.3977299999999999e-05
		-0.5 -0.25 -1.3977299999999999e-05
		;
createNode nurbsCurve -n "Tongue_B_Guide_Ctrl_Ctrl_Ctrl_CtrlShape" -p "Tongue_B_Guide";
	rename -uid "88A7A130-41E6-232D-04EA-7D9900C7FA47";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2026/scripts/Mutant_Tools/Icons/";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".hpb" yes;
	setAttr ".ovc" 6;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 9 0 no 3
		10 0 1 2 3 4 5 6 7 8 9
		10
		0.25 1.3977299999999999e-05 -0.5
		0.25591599999999998 1.3977299999999999e-05 0.94513100000000005
		0.50644299999999998 1.3977299999999999e-05 0.739653
		0.93915099999999996 1.3977299999999999e-05 0.99017999999999995
		3.8742999999999997e-07 1.37985e-05 2.299302
		-0.93915099999999996 1.3977299999999999e-05 0.99018099999999998
		-0.50644199999999995 1.3977299999999999e-05 0.739653
		-0.25322099999999997 7.1674600000000002e-06 0.94513100000000005
		-0.25 1.3977299999999999e-05 -0.5
		0.25 1.3977299999999999e-05 -0.5
		;
createNode joint -n "Tongue_C_Guide" -p "Tongue_B_Guide";
	rename -uid "E81A8FAD-470D-4C73-AFF3-F7AEB85DB969";
	addAttr -ci true -sn "Helper" -ln "Helper" -min 0 -max 1 -en "Hide:Show" -at "enum";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2026/scripts/Mutant_Tools/Icons/";
	setAttr ".t" -type "double3" 3.1703509931005343 -2.8421709430404007e-14 -6.7679501978978709e-19 ;
	setAttr ".r" -type "double3" 0 0 -24.081433687844157 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr -cb on ".Helper" 1;
createNode nurbsCurve -n "Tongue_C_Guide_CtrlShape" -p "Tongue_C_Guide";
	rename -uid "3F85B307-43DB-5EE4-3279-D19CB8314136";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2026/scripts/Mutant_Tools/Icons/";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".hpb" yes;
	setAttr ".ovc" 14;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 9 0 no 3
		10 0 1 2 3 4 5 6 7 8 9
		10
		1.3977299999999999e-05 -0.5 0.25
		1.3977299999999999e-05 0.94513100000000005 0.25591599999999998
		1.3977299999999999e-05 0.739653 0.50644299999999998
		1.3977299999999999e-05 0.99017999999999995 0.93915099999999996
		1.37985e-05 2.299302 3.8742999999999997e-07
		1.3977299999999999e-05 0.99018099999999998 -0.93915099999999996
		1.3977299999999999e-05 0.739653 -0.50644199999999995
		7.1674600000000002e-06 0.94513100000000005 -0.25322099999999997
		1.3977299999999999e-05 -0.5 -0.25
		1.3977299999999999e-05 -0.5 0.25
		;
createNode nurbsCurve -n "Tongue_C_Guide_Ctrl_CtrlShape" -p "Tongue_C_Guide";
	rename -uid "AFF7F7A2-4FDB-2C58-54D6-8B81B20C6E3C";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2026/scripts/Mutant_Tools/Icons/";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".hpb" yes;
	setAttr ".ovc" 18;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 101 0 no 3
		102 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27
		 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54
		 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81
		 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99 100 101
		102
		0 0.59420899999999999 0
		-3.0751100000000001e-09 0.58518199999999998 0.103183
		-6.0567700000000004e-09 0.55837400000000004 0.203232
		-8.8544099999999994e-09 0.51460099999999998 0.29710500000000001
		-1.1383e-08 0.45519100000000001 0.38195099999999998
		-1.3565700000000001e-08 0.38195000000000001 0.45519100000000001
		-1.5336300000000002e-08 0.29710500000000001 0.51460099999999998
		-1.6640900000000001e-08 0.203232 0.55837400000000004
		-1.7439800000000002e-08 0.103183 0.58518199999999998
		-1.7708799999999999e-08 0 0.59421000000000002
		-1.7439800000000002e-08 -0.103183 0.58518199999999998
		-1.6640900000000001e-08 -0.203232 0.55837400000000004
		-1.5336300000000002e-08 -0.29710500000000001 0.51460099999999998
		-1.3565700000000001e-08 -0.38195000000000001 0.45519100000000001
		-1.1383e-08 -0.45519100000000001 0.38195099999999998
		-8.8544099999999994e-09 -0.51460099999999998 0.29710500000000001
		-6.0567700000000004e-09 -0.55837400000000004 0.203232
		-3.0751100000000001e-09 -0.58518199999999998 0.103183
		0 -0.59420899999999999 0
		0 -0.58518199999999998 -0.103183
		0 -0.55837400000000004 -0.203232
		0 -0.51460099999999998 -0.29710500000000001
		0 -0.45519100000000001 -0.38195099999999998
		0 -0.38195000000000001 -0.45519100000000001
		0 -0.29710500000000001 -0.51460099999999998
		0 -0.203232 -0.55837499999999995
		0 -0.103183 -0.58518199999999998
		0 0 -0.59421000000000002
		0 0.103183 -0.58518199999999998
		0 0.203232 -0.55837499999999995
		0 0.29710500000000001 -0.51460099999999998
		0 0.38195000000000001 -0.45519100000000001
		0 0.45519100000000001 -0.38195099999999998
		0 0.51460099999999998 -0.29710500000000001
		0 0.55837400000000004 -0.203232
		0 0.58518199999999998 -0.103183
		0 0.59420899999999999 0
		0.103183 0.58518199999999998 0
		0.203232 0.55837400000000004 0
		0.29710500000000001 0.51460099999999998 0
		0.38195099999999998 0.45519100000000001 0
		0.45519100000000001 0.38195000000000001 0
		0.51460099999999998 0.29710500000000001 0
		0.55837400000000004 0.203232 0
		0.58518199999999998 0.103183 0
		0.59420899999999999 0 0
		0.58518199999999998 -0.103183 0
		0.55837400000000004 -0.203232 0
		0.51460099999999998 -0.29710500000000001 0
		0.45519100000000001 -0.38195000000000001 0
		0.38195099999999998 -0.45519100000000001 0
		0.29710500000000001 -0.51460099999999998 0
		0.203232 -0.55837400000000004 0
		0.103183 -0.58518199999999998 0
		0 -0.59420899999999999 0
		-0.103183 -0.58518199999999998 0
		-0.203232 -0.55837400000000004 0
		-0.29710500000000001 -0.51460099999999998 0
		-0.38195099999999998 -0.45519100000000001 0
		-0.45519100000000001 -0.38195000000000001 0
		-0.51460099999999998 -0.29710500000000001 0
		-0.55837400000000004 -0.203232 0
		-0.58518199999999998 -0.103183 0
		-0.59421000000000002 0 0
		-0.58518199999999998 0.103183 0
		-0.55837400000000004 0.203232 0
		-0.51460099999999998 0.29710500000000001 0
		-0.45519100000000001 0.38195000000000001 0
		-0.38195099999999998 0.45519100000000001 0
		-0.29710500000000001 0.51460099999999998 0
		-0.203232 0.55837400000000004 0
		-0.103183 0.58518199999999998 0
		0 0.59420899999999999 0
		-3.0751100000000001e-09 0.58518199999999998 0.103183
		-6.0567700000000004e-09 0.55837400000000004 0.203232
		-8.8544099999999994e-09 0.51460099999999998 0.29710500000000001
		-1.1383e-08 0.45519100000000001 0.38195099999999998
		-1.3565700000000001e-08 0.38195000000000001 0.45519100000000001
		-1.5336300000000002e-08 0.29710500000000001 0.51460099999999998
		-1.6640900000000001e-08 0.203232 0.55837400000000004
		-1.7439800000000002e-08 0.103183 0.58518199999999998
		-1.7708799999999999e-08 0 0.59421000000000002
		-0.18362100000000001 0 0.56512700000000005
		-0.34926800000000002 0 0.48072599999999999
		-0.48072599999999999 0 0.34926800000000002
		-0.56512700000000005 0 0.18362100000000001
		-0.59421000000000002 0 0
		-0.56512700000000005 0 -0.18362100000000001
		-0.48072599999999999 0 -0.34926800000000002
		-0.34926800000000002 0 -0.48072599999999999
		-0.18362100000000001 0 -0.56512700000000005
		0 0 -0.59421000000000002
		0.18362100000000001 0 -0.56512700000000005
		0.34926800000000002 0 -0.48072599999999999
		0.48072599999999999 0 -0.34926800000000002
		0.56512700000000005 0 -0.18362100000000001
		0.59420899999999999 0 0
		0.56512700000000005 0 0.18362100000000001
		0.48072599999999999 0 0.34926800000000002
		0.34926800000000002 0 0.48072599999999999
		0.18362100000000001 0 0.56512700000000005
		-1.7708799999999999e-08 0 0.59421000000000002
		;
createNode nurbsCurve -n "Tongue_C_Guide_Ctrl_Ctrl_CtrlShape" -p "Tongue_C_Guide";
	rename -uid "2940B966-4841-1318-90B9-2CAD6A61ACAF";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2026/scripts/Mutant_Tools/Icons/";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".hpb" yes;
	setAttr ".ovc" 13;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 9 0 no 3
		10 0 1 2 3 4 5 6 7 8 9
		10
		-0.5 -0.25 -1.3977299999999999e-05
		0.94513100000000005 -0.25591599999999998 -1.3977299999999999e-05
		0.739653 -0.50644299999999998 -1.3977299999999999e-05
		0.99017999999999995 -0.93915099999999996 -1.3977299999999999e-05
		2.299302 -3.8742999999999997e-07 -1.37985e-05
		0.99018099999999998 0.93915099999999996 -1.3977299999999999e-05
		0.739653 0.50644199999999995 -1.3977299999999999e-05
		0.94513100000000005 0.25322099999999997 -7.1674600000000002e-06
		-0.5 0.25 -1.3977299999999999e-05
		-0.5 -0.25 -1.3977299999999999e-05
		;
createNode nurbsCurve -n "Tongue_C_Guide_Ctrl_Ctrl_Ctrl_CtrlShape" -p "Tongue_C_Guide";
	rename -uid "B81F1C32-4080-A85E-22E2-0CACE8861EB8";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2026/scripts/Mutant_Tools/Icons/";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".hpb" yes;
	setAttr ".ovc" 6;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 9 0 no 3
		10 0 1 2 3 4 5 6 7 8 9
		10
		0.25 1.3977299999999999e-05 -0.5
		0.25591599999999998 1.3977299999999999e-05 0.94513100000000005
		0.50644299999999998 1.3977299999999999e-05 0.739653
		0.93915099999999996 1.3977299999999999e-05 0.99017999999999995
		3.8742999999999997e-07 1.37985e-05 2.299302
		-0.93915099999999996 1.3977299999999999e-05 0.99018099999999998
		-0.50644199999999995 1.3977299999999999e-05 0.739653
		-0.25322099999999997 7.1674600000000002e-06 0.94513100000000005
		-0.25 1.3977299999999999e-05 -0.5
		0.25 1.3977299999999999e-05 -0.5
		;
createNode joint -n "Tongue_D_Guide" -p "Tongue_C_Guide";
	rename -uid "616AD732-4C75-ECD3-9029-71AE8E3DA9CF";
	addAttr -ci true -sn "Helper" -ln "Helper" -min 0 -max 1 -en "Hide:Show" -at "enum";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2026/scripts/Mutant_Tools/Icons/";
	setAttr ".t" -type "double3" 3.1703509931005343 -2.8421709430404007e-14 -6.7679501978978709e-19 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr -cb on ".Helper" 1;
createNode nurbsCurve -n "Tongue_D_Guide_CtrlShape" -p "Tongue_D_Guide";
	rename -uid "EC6717EB-42F9-C092-D4C8-D889D99F0FC8";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2026/scripts/Mutant_Tools/Icons/";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".hpb" yes;
	setAttr ".ovc" 14;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 9 0 no 3
		10 0 1 2 3 4 5 6 7 8 9
		10
		1.3977299999999999e-05 -0.5 0.25
		1.3977299999999999e-05 0.94513100000000005 0.25591599999999998
		1.3977299999999999e-05 0.739653 0.50644299999999998
		1.3977299999999999e-05 0.99017999999999995 0.93915099999999996
		1.37985e-05 2.299302 3.8742999999999997e-07
		1.3977299999999999e-05 0.99018099999999998 -0.93915099999999996
		1.3977299999999999e-05 0.739653 -0.50644199999999995
		7.1674600000000002e-06 0.94513100000000005 -0.25322099999999997
		1.3977299999999999e-05 -0.5 -0.25
		1.3977299999999999e-05 -0.5 0.25
		;
createNode nurbsCurve -n "Tongue_D_Guide_Ctrl_CtrlShape" -p "Tongue_D_Guide";
	rename -uid "C2699015-44BA-F659-0F9F-7188EF1ABC5E";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2026/scripts/Mutant_Tools/Icons/";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".hpb" yes;
	setAttr ".ovc" 18;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 101 0 no 3
		102 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27
		 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54
		 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81
		 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99 100 101
		102
		0 0.59420899999999999 0
		-3.0751100000000001e-09 0.58518199999999998 0.103183
		-6.0567700000000004e-09 0.55837400000000004 0.203232
		-8.8544099999999994e-09 0.51460099999999998 0.29710500000000001
		-1.1383e-08 0.45519100000000001 0.38195099999999998
		-1.3565700000000001e-08 0.38195000000000001 0.45519100000000001
		-1.5336300000000002e-08 0.29710500000000001 0.51460099999999998
		-1.6640900000000001e-08 0.203232 0.55837400000000004
		-1.7439800000000002e-08 0.103183 0.58518199999999998
		-1.7708799999999999e-08 0 0.59421000000000002
		-1.7439800000000002e-08 -0.103183 0.58518199999999998
		-1.6640900000000001e-08 -0.203232 0.55837400000000004
		-1.5336300000000002e-08 -0.29710500000000001 0.51460099999999998
		-1.3565700000000001e-08 -0.38195000000000001 0.45519100000000001
		-1.1383e-08 -0.45519100000000001 0.38195099999999998
		-8.8544099999999994e-09 -0.51460099999999998 0.29710500000000001
		-6.0567700000000004e-09 -0.55837400000000004 0.203232
		-3.0751100000000001e-09 -0.58518199999999998 0.103183
		0 -0.59420899999999999 0
		0 -0.58518199999999998 -0.103183
		0 -0.55837400000000004 -0.203232
		0 -0.51460099999999998 -0.29710500000000001
		0 -0.45519100000000001 -0.38195099999999998
		0 -0.38195000000000001 -0.45519100000000001
		0 -0.29710500000000001 -0.51460099999999998
		0 -0.203232 -0.55837499999999995
		0 -0.103183 -0.58518199999999998
		0 0 -0.59421000000000002
		0 0.103183 -0.58518199999999998
		0 0.203232 -0.55837499999999995
		0 0.29710500000000001 -0.51460099999999998
		0 0.38195000000000001 -0.45519100000000001
		0 0.45519100000000001 -0.38195099999999998
		0 0.51460099999999998 -0.29710500000000001
		0 0.55837400000000004 -0.203232
		0 0.58518199999999998 -0.103183
		0 0.59420899999999999 0
		0.103183 0.58518199999999998 0
		0.203232 0.55837400000000004 0
		0.29710500000000001 0.51460099999999998 0
		0.38195099999999998 0.45519100000000001 0
		0.45519100000000001 0.38195000000000001 0
		0.51460099999999998 0.29710500000000001 0
		0.55837400000000004 0.203232 0
		0.58518199999999998 0.103183 0
		0.59420899999999999 0 0
		0.58518199999999998 -0.103183 0
		0.55837400000000004 -0.203232 0
		0.51460099999999998 -0.29710500000000001 0
		0.45519100000000001 -0.38195000000000001 0
		0.38195099999999998 -0.45519100000000001 0
		0.29710500000000001 -0.51460099999999998 0
		0.203232 -0.55837400000000004 0
		0.103183 -0.58518199999999998 0
		0 -0.59420899999999999 0
		-0.103183 -0.58518199999999998 0
		-0.203232 -0.55837400000000004 0
		-0.29710500000000001 -0.51460099999999998 0
		-0.38195099999999998 -0.45519100000000001 0
		-0.45519100000000001 -0.38195000000000001 0
		-0.51460099999999998 -0.29710500000000001 0
		-0.55837400000000004 -0.203232 0
		-0.58518199999999998 -0.103183 0
		-0.59421000000000002 0 0
		-0.58518199999999998 0.103183 0
		-0.55837400000000004 0.203232 0
		-0.51460099999999998 0.29710500000000001 0
		-0.45519100000000001 0.38195000000000001 0
		-0.38195099999999998 0.45519100000000001 0
		-0.29710500000000001 0.51460099999999998 0
		-0.203232 0.55837400000000004 0
		-0.103183 0.58518199999999998 0
		0 0.59420899999999999 0
		-3.0751100000000001e-09 0.58518199999999998 0.103183
		-6.0567700000000004e-09 0.55837400000000004 0.203232
		-8.8544099999999994e-09 0.51460099999999998 0.29710500000000001
		-1.1383e-08 0.45519100000000001 0.38195099999999998
		-1.3565700000000001e-08 0.38195000000000001 0.45519100000000001
		-1.5336300000000002e-08 0.29710500000000001 0.51460099999999998
		-1.6640900000000001e-08 0.203232 0.55837400000000004
		-1.7439800000000002e-08 0.103183 0.58518199999999998
		-1.7708799999999999e-08 0 0.59421000000000002
		-0.18362100000000001 0 0.56512700000000005
		-0.34926800000000002 0 0.48072599999999999
		-0.48072599999999999 0 0.34926800000000002
		-0.56512700000000005 0 0.18362100000000001
		-0.59421000000000002 0 0
		-0.56512700000000005 0 -0.18362100000000001
		-0.48072599999999999 0 -0.34926800000000002
		-0.34926800000000002 0 -0.48072599999999999
		-0.18362100000000001 0 -0.56512700000000005
		0 0 -0.59421000000000002
		0.18362100000000001 0 -0.56512700000000005
		0.34926800000000002 0 -0.48072599999999999
		0.48072599999999999 0 -0.34926800000000002
		0.56512700000000005 0 -0.18362100000000001
		0.59420899999999999 0 0
		0.56512700000000005 0 0.18362100000000001
		0.48072599999999999 0 0.34926800000000002
		0.34926800000000002 0 0.48072599999999999
		0.18362100000000001 0 0.56512700000000005
		-1.7708799999999999e-08 0 0.59421000000000002
		;
createNode nurbsCurve -n "Tongue_D_Guide_Ctrl_Ctrl_CtrlShape" -p "Tongue_D_Guide";
	rename -uid "53F53E48-4358-BC34-C4C5-BAB6F3E74E59";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2026/scripts/Mutant_Tools/Icons/";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".hpb" yes;
	setAttr ".ovc" 13;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 9 0 no 3
		10 0 1 2 3 4 5 6 7 8 9
		10
		-0.5 -0.25 -1.3977299999999999e-05
		0.94513100000000005 -0.25591599999999998 -1.3977299999999999e-05
		0.739653 -0.50644299999999998 -1.3977299999999999e-05
		0.99017999999999995 -0.93915099999999996 -1.3977299999999999e-05
		2.299302 -3.8742999999999997e-07 -1.37985e-05
		0.99018099999999998 0.93915099999999996 -1.3977299999999999e-05
		0.739653 0.50644199999999995 -1.3977299999999999e-05
		0.94513100000000005 0.25322099999999997 -7.1674600000000002e-06
		-0.5 0.25 -1.3977299999999999e-05
		-0.5 -0.25 -1.3977299999999999e-05
		;
createNode nurbsCurve -n "Tongue_D_Guide_Ctrl_Ctrl_Ctrl_CtrlShape" -p "Tongue_D_Guide";
	rename -uid "8F018911-448F-DB62-94C3-73AA4D5C2D06";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2026/scripts/Mutant_Tools/Icons/";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".hpb" yes;
	setAttr ".ovc" 6;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 9 0 no 3
		10 0 1 2 3 4 5 6 7 8 9
		10
		0.25 1.3977299999999999e-05 -0.5
		0.25591599999999998 1.3977299999999999e-05 0.94513100000000005
		0.50644299999999998 1.3977299999999999e-05 0.739653
		0.93915099999999996 1.3977299999999999e-05 0.99017999999999995
		3.8742999999999997e-07 1.37985e-05 2.299302
		-0.93915099999999996 1.3977299999999999e-05 0.99018099999999998
		-0.50644199999999995 1.3977299999999999e-05 0.739653
		-0.25322099999999997 7.1674600000000002e-06 0.94513100000000005
		-0.25 1.3977299999999999e-05 -0.5
		0.25 1.3977299999999999e-05 -0.5
		;
createNode dagContainer -n "ConvertFace_Block" -p "Face";
	rename -uid "1878B38E-4288-6639-6312-23902E81A1D4";
	addAttr -ci true -sn "nts" -ln "notes" -dt "string";
	setAttr ".isc" yes;
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2026/scripts/Mutant_Tools/Icons/BodyGames.png";
	setAttr ".ctor" -type "string" "rodri";
	setAttr ".cdat" -type "string" "2025/12/06 13:34:40";
	setAttr -l on -k off ".v";
	setAttr -l on -k off ".tx";
	setAttr -l on -k off ".ty";
	setAttr -l on -k off ".tz";
	setAttr -l on -k off ".rx";
	setAttr -l on -k off ".ry";
	setAttr -l on -k off ".rz";
	setAttr -l on -k off ".sx";
	setAttr -l on -k off ".sy";
	setAttr -l on -k off ".sz";
	setAttr ".nts" -type "string" (
		"['L_Brow_3_Skl_parentConstraint1', 'L_Brow_2_Skl', 'L_CheekBone_1_Bind_01_Skl_parentConstraint1', 'R_Orbicularis_1_Bind_02_Skl', 'L_Orbicularis_1_Bind_01_Skl', 'Nose_Bridge_Skl', 'L_Orbicularis_1_Bind_05_Skl', 'R_Orbicularis_1_Bind_04_Skl', 'L_Nostril_A_Skl', 'L_Brow_3_Skl', 'L_Orbicularis_1_Bind_08_Skl_parentConstraint1', 'UpperTeeth_Skl', 'Mid_Brow_A_Skl_parentConstraint1', 'R_CheekBone_1_Bind_03_Skl_parentConstraint1', 'R_Eyelids_Up__cv2_Skl_parentConstraint1', 'R_CheekBone_1_Bind_03_Skl', 'Mid_Mouth_Dw_Tweek_Skl_parentConstraint1', 'L_Brow_2_Skl_parentConstraint1', 'L_Orbicularis_1_Bind_05_Skl_parentConstraint1', 'R_Mid_01_Mouth_Dw_Tweek_Skl', 'Nose_Bridge_Skl_parentConstraint1', 'R_Eyelids_Up__cv4_Skl_parentConstraint1', 'L_Nostril_A_Skl_parentConstraint1', 'R_Eyelids_Dw__cv2_Skl_parentConstraint1', 'Tongue_A_Skl_parentConstraint1', 'L_Orbicularis_1_Bind_03_Skl_parentConstraint1', 'R_Eyelids_Up__cv4_Skl', 'Tongue_C_Skl', 'UpperTeeth_Skl_parentConstraint1', 'R_Brow_0_Skl', 'L_Mid_01_Mouth_Up_Tweek_Skl_parentConstraint1', 'Tongue_B_Skl', 'R_Eyelids_Dw__cv2_Skl', 'R_Mid_02_Mouth_Dw_Tweek_Skl_parentConstraint1', 'L_CheekBone_1_Bind_03_Skl_parentConstraint1', 'L_Brow_4_Skl', 'R_Mid_01_Mouth_Dw_Tweek_Skl_parentConstraint1', 'L_Cheek_A_Skl_parentConstraint1', 'L_CheekBone_1_Bind_01_Skl', 'R_Eyelids_Dw__cv3_Skl', 'L_Brow_0_Skl', 'R_Mouth_Dw_Tweek_Skl_parentConstraint1', 'R_Cheek_A_Skl', 'L_Mouth_Up_Tweek_Skl', 'L_Orbicularis_1_Bind_08_Skl', 'Tongue_C_Skl_parentConstraint1', 'R_Orbicularis_1_Bind_01_Skl_parentConstraint1', 'R_Mid_01_Mouth_Up_Tweek_Skl_parentConstraint1', 'R_Mid_03_Mouth_Dw_Tweek_Skl', 'R_Mouth_Dw_Tweek_Skl', 'L_Eyelids_Dw__cv3_Skl', 'R_Eyelids_Up__cv3_Skl', 'Mid_BrowNose_A_Skl', 'R_Orbicularis_1_Bind_01_Skl', 'L_Mouth_Dw_Tweek_Skl', 'L_Mid_01_Mouth_Dw_Tweek_Skl', 'R_Orbicularis_1_Bind_05_Skl_parentConstraint1', 'Nose_Base_Skl_parentConstraint1', 'R_Mid_02_Mouth_Up_Tweek_Skl_parentConstraint1', 'Mouth_Jaw_Skl_parentConstraint1', 'L_Eyelids_Dw__cv4_Skl_parentConstraint1', 'Mouth_Jaw_Skl', 'L_Brow_1_Skl_parentConstraint1', 'L_Eyelids_Up__cv2_Skl', 'L_Mid_03_Mouth_Dw_Tweek_Skl_parentConstraint1', 'Nose_Base_Skl', 'R_Brow_4_Skl_parentConstraint1', 'Tongue_D_Skl_parentConstraint1', 'R_CheekBone_1_Bind_01_Skl_parentConstraint1', 'R_Orbicularis_1_Bind_03_Skl_parentConstraint1', 'L_Eyelids_Up__cv4_Skl_parentConstraint1', 'R_Orbicularis_1_Bind_06_Skl', 'R_Eyelids_Dw__cv4_Skl', 'L_Orbicularis_1_Bind_03_Skl', 'R_CheekBone_1_Bind_02_Skl_parentConstraint1', 'R_CheekBone_1_Bind_01_Skl', 'R_Orbicularis_1_Bind_03_Skl', 'L_Mid_03_Mouth_Up_Tweek_Skl', 'L_Orbicularis_1_Bind_06_Skl_parentConstraint1', 'R_Brow_0_Skl_parentConstraint1', 'R_Orbicularis_1_Bind_02_Skl_parentConstraint1', 'L_Eyelids_Up__cv2_Skl_parentConstraint1', 'R_Orbicularis_1_Bind_05_Skl', 'R_Eyelids_Dw__cv3_Skl_parentConstraint1', 'R_Brow_2_Skl', 'R_Cheek_A_Skl_parentConstraint1', 'LowerTeeth_Skl', 'R_Mid_03_Mouth_Up_Tweek_Skl', 'Tongue_A_Skl', 'R_Mid_01_Mouth_Up_Tweek_Skl', 'Tongue_B_Skl_parentConstraint1', 'R_Orbicularis_1_Bind_06_Skl_parentConstraint1', 'L_Mid_01_Mouth_Up_Tweek_Skl', 'L_Orbicularis_1_Bind_01_Skl_parentConstraint1', 'R_Nostril_A_Skl', 'L_Mid_02_Mouth_Dw_Tweek_Skl_parentConstraint1', 'R_Brow_2_Skl_parentConstraint1', 'R_Orbicularis_1_Bind_07_Skl', 'L_Cheek_A_Skl', 'L_Mid_02_Mouth_Up_Tweek_Skl', 'Mid_Brow_A_Skl', 'R_CheekBone_1_Bind_02_Skl', 'Tongue_D_Skl', 'R_Brow_1_Skl_parentConstraint1', 'Mid_BrowNose_A_Skl_parentConstraint1', 'L_Mid_03_Mouth_Up_Tweek_Skl_parentConstraint1', 'L_Eyelids_Up__cv3_Skl_parentConstraint1', 'Nose_Main_Skl', 'R_Brow_4_Skl', 'L_Orbicularis_1_Bind_04_Skl', 'Mid_Mouth_Up_Tweek_Skl_parentConstraint1', 'L_Eyelids_Dw__cv2_Skl_parentConstraint1', 'L_CheekBone_1_Bind_03_Skl', 'L_Mouth_Dw_Tweek_Skl_parentConstraint1', 'R_Orbicularis_1_Bind_08_Skl', 'L_Brow_0_Skl_parentConstraint1', 'L_Orbicularis_1_Bind_07_Skl_parentConstraint1', 'R_Mid_03_Mouth_Dw_Tweek_Skl_parentConstraint1', 'R_Brow_3_Skl_parentConstraint1', 'L_Orbicularis_1_Bind_07_Skl', 'L_Eyelids_Dw__cv2_Skl', 'L_Mid_01_Mouth_Dw_Tweek_Skl_parentConstraint1', 'L_Mid_02_Mouth_Dw_Tweek_Skl', 'R_Brow_3_Skl', 'L_Mouth_Up_Tweek_Skl_parentConstraint1', 'L_Eyelids_Up__cv4_Skl', 'R_Brow_1_Skl', 'R_Mouth_Up_Tweek_Skl_parentConstraint1', 'LowerTeeth_Skl_parentConstraint1', 'R_Orbicularis_1_Bind_08_Skl_parentConstraint1', 'L_Eyelids_Dw__cv3_Skl_parentConstraint1', 'R_Orbicularis_1_Bind_07_Skl_parentConstraint1', 'L_Brow_4_Skl_parentConstraint1', 'R_Mid_03_Mouth_Up_Tweek_Skl_parentConstraint1', 'L_CheekBone_1_Bind_02_Skl', 'R_Mid_02_Mouth_Up_Tweek_Skl', 'R_Mid_02_Mouth_Dw_Tweek_Skl', 'L_Eyelids_Up__cv3_Skl', 'Mid_Mouth_Dw_Tweek_Skl', 'L_Mid_02_Mouth_Up_Tweek_Skl_parentConstraint1', 'L_CheekBone_1_Bind_02_Skl_parentConstraint1', 'L_Orbicularis_1_Bind_04_Skl_parentConstraint1', 'L_Orbicularis_1_Bind_02_Skl', 'L_Mid_03_Mouth_Dw_Tweek_Skl', 'L_Brow_1_Skl', 'R_Eyelids_Up__cv2_Skl', 'R_Eyelids_Dw__cv4_Skl_parentConstraint1', 'R_Orbicularis_1_Bind_04_Skl_parentConstraint1', 'R_Mouth_Up_Tweek_Skl', 'R_Nostril_A_Skl_parentConstraint1', 'R_Eyelids_Up__cv3_Skl_parentConstraint1', 'L_Orbicularis_1_Bind_06_Skl', 'Mid_Mouth_Up_Tweek_Skl', 'Nose_Main_Skl_parentConstraint1', 'L_Eyelids_Dw__cv4_Skl', 'L_Orbicularis_1_Bind_02_Skl_parentConstraint1']");
createNode dagContainer -n "CheekAutomations_Block" -p "Face";
	rename -uid "23FD0D52-4F73-FC8F-09C2-DE8654701394";
	addAttr -ci true -sn "nts" -ln "notes" -dt "string";
	setAttr ".isc" yes;
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2026/scripts/Mutant_Tools/Icons/CODE.png";
	setAttr ".ctor" -type "string" "rodri";
	setAttr ".cdat" -type "string" "2025/12/11 11:47:10";
	setAttr -l on -k off ".v";
	setAttr -l on -k off ".tx";
	setAttr -l on -k off ".ty";
	setAttr -l on -k off ".tz";
	setAttr -l on -k off ".rx";
	setAttr -l on -k off ".ry";
	setAttr -l on -k off ".rz";
	setAttr -l on -k off ".sx";
	setAttr -l on -k off ".sy";
	setAttr -l on -k off ".sz";
	setAttr ".nts" -type "string" "['L_Nostril_A_Ctrl_Auto_Grp', 'L_Nostril_A_Ctrl_Auto_Grp_parentConstraint1', 'R_Cheek_A_Ctrl_Root_Grp', 'L_CheekBone_1_Main_Ctrl_Auto_Grp_parentConstraint1', 'L_Nostril_A_Ctrl_Root_Grp', 'L_Cheek_A_Ctrl_Root_Grp', 'L_Cheek_A_Ctrl_Auto_Grp_parentConstraint1', 'R_CheekBone_1_Main_Ctrl_Auto_Grp_parentConstraint1', 'R_CheekBone_1_Main_Ctrl_Root_Grp', 'R_Cheek_A_Ctrl_Auto_Grp', 'R_Nostril_A_Ctrl_Root_Grp', 'L_CheekBone_1_Main_Ctrl_Root_Grp', 'R_CheekBone_1_Main_Ctrl_Auto_Grp', 'R_Cheek_A_Ctrl_Auto_Grp_parentConstraint1', 'R_Nostril_A_Ctrl_Auto_Grp_parentConstraint1', 'R_Nostril_A_Ctrl_Auto_Grp', 'L_CheekBone_1_Main_Ctrl_Auto_Grp', 'L_Cheek_A_Ctrl_Auto_Grp']";
createNode transform -n "CheekAutomations_Loc" -p "CheekAutomations_Block";
	rename -uid "A0CE4345-4264-8536-6E92-AF80DF4B213D";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2026/scripts/Mutant_Tools/Icons/";
createNode locator -n "CheekAutomations_LocShape" -p "CheekAutomations_Loc";
	rename -uid "B1916D37-406D-7180-2A83-99B869754764";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2026/scripts/Mutant_Tools/Icons/";
	setAttr -k off ".v";
createNode dagContainer -n "CheekPushZ_Block" -p "Face";
	rename -uid "C4D7C637-45B8-76BD-79F4-669AD0E408D3";
	addAttr -ci true -sn "nts" -ln "notes" -dt "string";
	setAttr ".isc" yes;
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2026/scripts/Mutant_Tools/Icons/CODE.png";
	setAttr ".ctor" -type "string" "rodri";
	setAttr ".cdat" -type "string" "2025/12/23 07:30:22";
	setAttr -l on -k off ".v";
	setAttr -l on -k off ".tx";
	setAttr -l on -k off ".ty";
	setAttr -l on -k off ".tz";
	setAttr -l on -k off ".rx";
	setAttr -l on -k off ".ry";
	setAttr -l on -k off ".rz";
	setAttr -l on -k off ".sx";
	setAttr -l on -k off ".sy";
	setAttr -l on -k off ".sz";
	setAttr ".nts" -type "string" "['L_Cheek_WidePush_GT', 'R_Cheek_WidePush_GT', 'L_Cheek_A_Ctrl_Push_Grp', 'L_Cheek_WidePush_MD', 'R_Cheek_Push_Flip_MD', 'R_Cheek_WidePush_MD1', 'R_Cheek_Push_SUM1', 'L_Cheek_Push_SUM', 'L_Cheek_WidePush_BC', 'R_Cheek_UpPush_MD1', 'L_Cheek_UpPush_MD', 'L_Cheek_UpPush_BC', 'R_Cheek_UpPush_BC1', 'L_Cheek_UpPush_GT', 'R_Cheek_WidePush_BC1', 'R_Cheek_A_Ctrl_Push_Grp', 'R_Cheek_UpPush_GT']";
createNode transform -n "CheekPushZ_Loc" -p "CheekPushZ_Block";
	rename -uid "8F926538-40BE-CC7E-5E09-BA9612FC40CF";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2026/scripts/Mutant_Tools/Icons/";
createNode locator -n "CheekPushZ_LocShape" -p "CheekPushZ_Loc";
	rename -uid "E9BDE7AB-40C5-551C-9F7F-3FB96BDF5CE9";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2026/scripts/Mutant_Tools/Icons/";
	setAttr -k off ".v";
createNode dagContainer -n "FaceHierarchy_Block" -p "Face";
	rename -uid "55959FD4-43C6-DD22-7E19-74BABA90DF38";
	addAttr -ci true -sn "nts" -ln "notes" -dt "string";
	setAttr ".isc" yes;
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2026/scripts/Mutant_Tools/Icons/CODE.png";
	setAttr ".ctor" -type "string" "rodri";
	setAttr ".cdat" -type "string" "2025/12/06 13:42:55";
	setAttr -l on -k off ".v";
	setAttr -l on -k off ".tx";
	setAttr -l on -k off ".ty";
	setAttr -l on -k off ".tz";
	setAttr -l on -k off ".rx";
	setAttr -l on -k off ".ry";
	setAttr -l on -k off ".rz";
	setAttr -l on -k off ".sx";
	setAttr -l on -k off ".sy";
	setAttr -l on -k off ".sz";
	setAttr ".nts" -type "string" "[]";
createNode transform -n "FaceHierarchy_Loc" -p "FaceHierarchy_Block";
	rename -uid "F0E5455A-4AE2-4074-3BB4-55AEE7A25F62";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2026/scripts/Mutant_Tools/Icons/";
createNode locator -n "FaceHierarchy_LocShape" -p "FaceHierarchy_Loc";
	rename -uid "9008929D-4E01-339B-781C-37834612A50A";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2026/scripts/Mutant_Tools/Icons/";
	setAttr -k off ".v";
createNode hyperLayout -n "hyperLayout72";
	rename -uid "DBC5F9FA-4D0D-FB8A-0556-F082817BDFEE";
	setAttr ".ihi" 0;
	setAttr -s 2 ".hyp";
createNode network -n "VisAttrs_Config";
	rename -uid "05DCF2F7-471B-7A64-3C73-C4B9BD91FAD2";
	addAttr -ci true -sn "precode" -ln "precode" -dt "string";
	addAttr -ci true -sn "Build_Command" -ln "Build_Command" -dt "string";
	addAttr -ci true -sn "Import_Command" -ln "Import_Command" -dt "string";
	addAttr -ci true -sn "SetParent" -ln "SetParent" -dt "string";
	addAttr -ci true -sn "Help" -ln "Help" -dt "string";
	addAttr -ci true -sn "postcode" -ln "postcode" -dt "string";
	setAttr ".precode" -type "string" "";
	setAttr -l on ".Build_Command" -type "string" "exec_visattrs.build_visattrs_block()";
	setAttr -l on ".Import_Command" -type "string" "import exec_visattrs";
	setAttr ".SetParent" -type "string" "Head_Ctrl";
	setAttr ".Help" -type "string" "This will create a ctrl to hold vis attrs";
	setAttr ".postcode" -type "string" "";
createNode hyperLayout -n "hyperLayout70";
	rename -uid "495FC7D3-4321-8729-4943-E68435CFDE88";
	setAttr ".ihi" 0;
	setAttr -s 2 ".hyp";
createNode network -n "L_Brow_Config";
	rename -uid "7A90E250-439E-E0A7-B66B-3B96865D2943";
	addAttr -ci true -sn "precode" -ln "precode" -dt "string";
	addAttr -ci true -sn "Build_Command" -ln "Build_Command" -dt "string";
	addAttr -ci true -sn "Import_Command" -ln "Import_Command" -dt "string";
	addAttr -ci true -sn "SetParent" -ln "SetParent" -dt "string";
	addAttr -ci true -sn "Mirror" -ln "Mirror" -min 0 -max 2 -en "True:False:Right_Only" 
		-at "enum";
	addAttr -ci true -sn "SetAttrsPosition" -ln "SetAttrsPosition" -dt "string";
	addAttr -ci true -sn "CtrlSize" -ln "CtrlSize" -dv 4 -min 1 -max 20 -at "long";
	addAttr -ci true -sn "GameMode" -ln "GameMode" -min 0 -max 1 -at "bool";
	addAttr -ci true -sn "Help" -ln "Help" -dt "string";
	addAttr -ci true -sn "postcode" -ln "postcode" -dt "string";
	setAttr ".precode" -type "string" "";
	setAttr -l on ".Build_Command" -type "string" "exec_brows.build_brows_block()";
	setAttr -l on ".Import_Command" -type "string" "import exec_brows";
	setAttr ".SetParent" -type "string" "Head_Ctrl";
	setAttr -cb on ".Mirror";
	setAttr ".SetAttrsPosition" -type "string" "VisAttrs_Ctrl";
	setAttr -k on ".CtrlSize";
	setAttr -cb on ".GameMode" yes;
	setAttr ".Help" -type "string" "Will crete brows rig system";
	setAttr ".postcode" -type "string" "";
createNode hyperLayout -n "hyperLayout71";
	rename -uid "BC54691A-4B77-B475-3469-F6BCAAB16DE9";
	setAttr ".ihi" 0;
createNode network -n "L_Eyelids_Config";
	rename -uid "52A14E64-409E-1D45-6E57-688CA39CF3E6";
	addAttr -ci true -sn "precode" -ln "precode" -dt "string";
	addAttr -ci true -sn "Build_Command" -ln "Build_Command" -dt "string";
	addAttr -ci true -sn "Import_Command" -ln "Import_Command" -dt "string";
	addAttr -ci true -sn "SetParent" -ln "SetParent" -dt "string";
	addAttr -ci true -sn "SetAttrsPosition" -ln "SetAttrsPosition" -dt "string";
	addAttr -ci true -sn "Mirror" -ln "Mirror" -min 0 -max 2 -en "True:False:Right_Only" 
		-at "enum";
	addAttr -ci true -sn "SetUpperEdge" -ln "SetUpperEdge" -dt "string";
	addAttr -ci true -sn "SetLowerEdge" -ln "SetLowerEdge" -dt "string";
	addAttr -ci true -sn "SetEyePivot" -ln "SetEyePivot" -dt "string";
	addAttr -ci true -sn "CtrlSize" -ln "CtrlSize" -dv 4 -min 1 -max 20 -at "long";
	addAttr -ci true -sn "LimitCtrl" -ln "LimitCtrl" -min 0 -max 1 -at "bool";
	addAttr -ci true -sn "GameMode" -ln "GameMode" -min 0 -max 1 -at "bool";
	addAttr -ci true -sn "BindJoints" -ln "BindJoints" -min 0 -max 2 -en "PerVtx:3:1" 
		-at "enum";
	addAttr -ci true -sn "Help" -ln "Help" -dt "string";
	addAttr -ci true -sn "postcode" -ln "postcode" -dt "string";
	setAttr ".precode" -type "string" "";
	setAttr -l on ".Build_Command" -type "string" "exec_eyelids.build_eyelids_block()";
	setAttr -l on ".Import_Command" -type "string" "import exec_eyelids";
	setAttr ".SetParent" -type "string" "Head_Ctrl";
	setAttr ".SetAttrsPosition" -type "string" "VisAttrs_Ctrl";
	setAttr -cb on ".Mirror";
	setAttr ".SetUpperEdge" -type "string" "Body_Geo.e[15777], Body_Geo.e[15781], Body_Geo.e[15784], Body_Geo.e[15786], Body_Geo.e[15789], Body_Geo.e[16686], Body_Geo.e[16695], Body_Geo.e[17011], Body_Geo.e[17014], Body_Geo.e[17056], Body_Geo.e[25694]";
	setAttr ".SetLowerEdge" -type "string" "Body_Geo.e[15760], Body_Geo.e[15762], Body_Geo.e[15767:15768], Body_Geo.e[15773], Body_Geo.e[16250], Body_Geo.e[16260], Body_Geo.e[16502], Body_Geo.e[17022], Body_Geo.e[17024], Body_Geo.e[17137]";
	setAttr ".SetEyePivot" -type "string" "Eyelids_Guide";
	setAttr -k on ".CtrlSize";
	setAttr -cb on ".LimitCtrl";
	setAttr -cb on ".GameMode" yes;
	setAttr -cb on ".BindJoints" 1;
	setAttr ".Help" -type "string" "Create eyelids rig, based on Marco Giordano tutorial\n";
	setAttr ".postcode" -type "string" "";
createNode hyperLayout -n "hyperLayout86";
	rename -uid "C4BE090A-47CF-D066-F8D4-4FA1C73571A7";
	setAttr ".ihi" 0;
	setAttr -s 2 ".hyp";
createNode network -n "L_Orbicularis_Config";
	rename -uid "E4E4675E-4084-2E13-5E06-45AC3C526D1B";
	addAttr -ci true -sn "precode" -ln "precode" -dt "string";
	addAttr -ci true -sn "Build_Command" -ln "Build_Command" -dt "string";
	addAttr -ci true -sn "Import_Command" -ln "Import_Command" -dt "string";
	addAttr -ci true -sn "SetParent" -ln "SetParent" -dt "string";
	addAttr -ci true -sn "Equal" -ln "Equal" -min 0 -max 1 -at "bool";
	addAttr -ci true -sn "Ctrls" -ln "Ctrls" -dv 5 -min 1 -max 20 -at "long";
	addAttr -ci true -sn "Joints" -ln "Joints" -dv 5 -min 1 -max 20 -at "long";
	addAttr -ci true -sn "Constraint" -ln "Constraint" -min 0 -max 1 -at "bool";
	addAttr -ci true -sn "AddFk" -ln "AddFk" -min 0 -max 1 -at "bool";
	addAttr -ci true -sn "Wire" -ln "Wire" -min 0 -max 1 -at "bool";
	addAttr -ci true -sn "MiddleCtrlPosition" -ln "MiddleCtrlPosition" -min 0 -max 2 
		-en "Original:Start:End" -at "enum";
	addAttr -ci true -sn "Help" -ln "Help" -dt "string";
	addAttr -ci true -sn "postcode" -ln "postcode" -dt "string";
	setAttr ".precode" -type "string" "";
	setAttr -l on ".Build_Command" -type "string" "exec_ribbonizer.build_ribbonizer_block()";
	setAttr -l on ".Import_Command" -type "string" "import exec_ribbonizer";
	setAttr ".SetParent" -type "string" "Head_Ctrl";
	setAttr -cb on ".Equal" yes;
	setAttr -k on ".Ctrls" 8;
	setAttr -k on ".Joints" 8;
	setAttr -cb on ".Constraint" yes;
	setAttr -cb on ".AddFk";
	setAttr -cb on ".Wire";
	setAttr -cb on ".MiddleCtrlPosition";
	setAttr ".Help" -type "string" "Remove constraint for a local system.";
	setAttr ".postcode" -type "string" "cmds.delete(\"L_Orbicularis_1_Main_CtrlShape\")";
createNode makeNurbCylinder -n "makeNurbCylinder1";
	rename -uid "72B2EEBC-4C9F-755E-B538-DE87201CD3D9";
	setAttr ".ax" -type "double3" 0 1 0 ;
	setAttr ".hr" 1;
createNode hyperLayout -n "hyperLayout87";
	rename -uid "D18370F7-4C2C-F035-B195-028486EB61AE";
	setAttr ".ihi" 0;
	setAttr -s 2 ".hyp";
createNode network -n "R_Orbicularis_Config";
	rename -uid "F9A1F86E-4A1F-BBB0-A374-F78B16E2A1FA";
	addAttr -ci true -sn "precode" -ln "precode" -dt "string";
	addAttr -ci true -sn "Build_Command" -ln "Build_Command" -dt "string";
	addAttr -ci true -sn "Import_Command" -ln "Import_Command" -dt "string";
	addAttr -ci true -sn "SetParent" -ln "SetParent" -dt "string";
	addAttr -ci true -sn "Equal" -ln "Equal" -min 0 -max 1 -at "bool";
	addAttr -ci true -sn "Ctrls" -ln "Ctrls" -dv 5 -min 1 -max 20 -at "long";
	addAttr -ci true -sn "Joints" -ln "Joints" -dv 5 -min 1 -max 20 -at "long";
	addAttr -ci true -sn "Constraint" -ln "Constraint" -min 0 -max 1 -at "bool";
	addAttr -ci true -sn "AddFk" -ln "AddFk" -min 0 -max 1 -at "bool";
	addAttr -ci true -sn "Wire" -ln "Wire" -min 0 -max 1 -at "bool";
	addAttr -ci true -sn "MiddleCtrlPosition" -ln "MiddleCtrlPosition" -min 0 -max 2 
		-en "Original:Start:End" -at "enum";
	addAttr -ci true -sn "Help" -ln "Help" -dt "string";
	addAttr -ci true -sn "postcode" -ln "postcode" -dt "string";
	setAttr ".precode" -type "string" "";
	setAttr -l on ".Build_Command" -type "string" "exec_ribbonizer.build_ribbonizer_block()";
	setAttr -l on ".Import_Command" -type "string" "import exec_ribbonizer";
	setAttr ".SetParent" -type "string" "Head_Ctrl";
	setAttr -cb on ".Equal" yes;
	setAttr -k on ".Ctrls" 8;
	setAttr -k on ".Joints" 8;
	setAttr -cb on ".Constraint" yes;
	setAttr -cb on ".AddFk";
	setAttr -cb on ".Wire";
	setAttr -cb on ".MiddleCtrlPosition";
	setAttr ".Help" -type "string" "Remove constraint for a local system.";
	setAttr ".postcode" -type "string" "cmds.delete(\"R_Orbicularis_1_Main_CtrlShape\")";
createNode hyperLayout -n "hyperLayout73";
	rename -uid "16F88127-4E22-9AB9-1676-F9B52BE1D927";
	setAttr ".ihi" 0;
	setAttr -s 25 ".hyp";
createNode network -n "Mouth_Config";
	rename -uid "093E515E-4E74-74E0-0EE8-E6A354957CE5";
	addAttr -ci true -sn "precode" -ln "precode" -dt "string";
	addAttr -ci true -sn "Build_Command" -ln "Build_Command" -dt "string";
	addAttr -ci true -sn "Import_Command" -ln "Import_Command" -dt "string";
	addAttr -ci true -sn "SetParent" -ln "SetParent" -dt "string";
	addAttr -ci true -sn "SetAttrsPosition" -ln "SetAttrsPosition" -dt "string";
	addAttr -ci true -sn "SetUpperEdge" -ln "SetUpperEdge" -dt "string";
	addAttr -ci true -sn "SetLowerEdge" -ln "SetLowerEdge" -dt "string";
	addAttr -ci true -sn "TweakCtrlsAmount" -ln "TweakCtrlsAmount" -dv 7 -min 1 -max 
		20 -at "long";
	addAttr -ci true -sn "MidCtrlsAmount" -ln "MidCtrlsAmount" -dv 5 -min 1 -max 20 
		-at "long";
	addAttr -ci true -sn "CtrlSize" -ln "CtrlSize" -dv 4 -min 1 -max 20 -at "long";
	addAttr -ci true -sn "Help" -ln "Help" -dt "string";
	addAttr -ci true -sn "postcode" -ln "postcode" -dt "string";
	setAttr ".precode" -type "string" "";
	setAttr -l on ".Build_Command" -type "string" "exec_mouthgames.build_mouthgames_block()";
	setAttr -l on ".Import_Command" -type "string" "import exec_mouthgames";
	setAttr ".SetParent" -type "string" "Head_Ctrl";
	setAttr ".SetAttrsPosition" -type "string" "VisAttrs_Ctrl";
	setAttr ".SetUpperEdge" -type "string" "Body_Geo.e[2663], Body_Geo.e[2673], Body_Geo.e[2677], Body_Geo.e[2679], Body_Geo.e[2682], Body_Geo.e[2685], Body_Geo.e[2689], Body_Geo.e[2693], Body_Geo.e[2801], Body_Geo.e[2899], Body_Geo.e[16344], Body_Geo.e[16355], Body_Geo.e[16358], Body_Geo.e[16363], Body_Geo.e[16366], Body_Geo.e[16370], Body_Geo.e[16373], Body_Geo.e[16375], Body_Geo.e[16480], Body_Geo.e[16575], Body_Geo.e[27345], Body_Geo.e[27503]";
	setAttr ".SetLowerEdge" -type "string" "Body_Geo.e[2665], Body_Geo.e[2695], Body_Geo.e[2698], Body_Geo.e[2702], Body_Geo.e[2704], Body_Geo.e[2708], Body_Geo.e[2711], Body_Geo.e[2747], Body_Geo.e[2804], Body_Geo.e[2898], Body_Geo.e[16350], Body_Geo.e[16379], Body_Geo.e[16382], Body_Geo.e[16384], Body_Geo.e[16389], Body_Geo.e[16392], Body_Geo.e[16395], Body_Geo.e[16430], Body_Geo.e[16481], Body_Geo.e[16572], Body_Geo.e[27381], Body_Geo.e[27539]";
	setAttr -k on ".TweakCtrlsAmount";
	setAttr -k on ".MidCtrlsAmount";
	setAttr -k on ".CtrlSize";
	setAttr ".Help" -type "string" "Create Jaw and Lips Mouth Rig, make Numbers even and tweakers bigger\n";
	setAttr ".postcode" -type "string" "";
createNode hyperLayout -n "hyperLayout74";
	rename -uid "DF82DC80-4421-CAD0-C620-3FB556861004";
	setAttr ".ihi" 0;
	setAttr -s 15 ".hyp";
createNode network -n "Nose_Config";
	rename -uid "5FA9C9F5-419A-A14E-92FF-11B47EF6B458";
	addAttr -ci true -sn "precode" -ln "precode" -dt "string";
	addAttr -ci true -sn "Build_Command" -ln "Build_Command" -dt "string";
	addAttr -ci true -sn "Import_Command" -ln "Import_Command" -dt "string";
	addAttr -ci true -sn "SetParent" -ln "SetParent" -dt "string";
	addAttr -ci true -sn "Mirror" -ln "Mirror" -min 0 -max 1 -at "bool";
	addAttr -ci true -sn "AutoRotate" -ln "AutoRotate" -min 0 -max 1 -at "bool";
	addAttr -ci true -sn "CtrlSize" -ln "CtrlSize" -dv 1 -min 1 -max 20 -at "long";
	addAttr -ci true -sn "CtrlColor" -ln "CtrlColor" -min 0 -max 7 -en "lightBlue:blue:white:purple:green:red:yellow:grey" 
		-at "enum";
	addAttr -ci true -sn "CtrlType" -ln "CtrlType" -min 0 -max 16 -en "square:sphere:cube:octagon:hexagon:pringle:feet:hand:circleY:circleX:circleZ:3dArrow:2dArrow:mover:2dArrow:root:cog" 
		-at "enum";
	addAttr -ci true -sn "TwistAxis" -ln "TwistAxis" -min 0 -max 2 -en "X:Y:Z" -at "enum";
	addAttr -ci true -sn "Help" -ln "Help" -dt "string";
	addAttr -ci true -sn "postcode" -ln "postcode" -dt "string";
	setAttr ".precode" -type "string" "";
	setAttr -l on ".Build_Command" -type "string" "exec_chain.build_chain_block()";
	setAttr -l on ".Import_Command" -type "string" "import exec_chain";
	setAttr ".SetParent" -type "string" "Head_Ctrl";
	setAttr -cb on ".Mirror";
	setAttr -cb on ".AutoRotate";
	setAttr -k on ".CtrlSize";
	setAttr -cb on ".CtrlColor";
	setAttr -cb on ".CtrlType";
	setAttr -cb on ".TwistAxis";
	setAttr ".Help" -type "string" "Create a FK Chain";
	setAttr ".postcode" -type "string" "";
createNode hyperLayout -n "hyperLayout75";
	rename -uid "3FFB54CA-464B-EE69-FFFC-8786BF2E42F3";
	setAttr ".ihi" 0;
	setAttr -s 5 ".hyp";
createNode network -n "L_Nostril_Config";
	rename -uid "E9A2CF5C-48BC-92A7-3152-4E84E73E93F9";
	addAttr -ci true -sn "precode" -ln "precode" -dt "string";
	addAttr -ci true -sn "Build_Command" -ln "Build_Command" -dt "string";
	addAttr -ci true -sn "Import_Command" -ln "Import_Command" -dt "string";
	addAttr -ci true -sn "SetParent" -ln "SetParent" -dt "string";
	addAttr -ci true -sn "Mirror" -ln "Mirror" -min 0 -max 1 -at "bool";
	addAttr -ci true -sn "AutoRotate" -ln "AutoRotate" -min 0 -max 1 -at "bool";
	addAttr -ci true -sn "CtrlSize" -ln "CtrlSize" -dv 1 -min 1 -max 20 -at "long";
	addAttr -ci true -sn "CtrlColor" -ln "CtrlColor" -min 0 -max 7 -en "lightBlue:blue:white:purple:green:red:yellow:grey" 
		-at "enum";
	addAttr -ci true -sn "CtrlType" -ln "CtrlType" -min 0 -max 16 -en "square:sphere:cube:octagon:hexagon:pringle:feet:hand:circleY:circleX:circleZ:3dArrow:2dArrow:mover:2dArrow:root:cog" 
		-at "enum";
	addAttr -ci true -sn "TwistAxis" -ln "TwistAxis" -min 0 -max 2 -en "X:Y:Z" -at "enum";
	addAttr -ci true -sn "Help" -ln "Help" -dt "string";
	addAttr -ci true -sn "postcode" -ln "postcode" -dt "string";
	setAttr ".precode" -type "string" "";
	setAttr -l on ".Build_Command" -type "string" "exec_chain.build_chain_block()";
	setAttr -l on ".Import_Command" -type "string" "import exec_chain";
	setAttr ".SetParent" -type "string" "Nose_Main_Ctrl";
	setAttr -cb on ".Mirror" yes;
	setAttr -cb on ".AutoRotate";
	setAttr -k on ".CtrlSize";
	setAttr -cb on ".CtrlColor";
	setAttr -cb on ".CtrlType";
	setAttr -cb on ".TwistAxis";
	setAttr ".Help" -type "string" "Create a FK Chain";
	setAttr ".postcode" -type "string" "";
createNode hyperLayout -n "hyperLayout76";
	rename -uid "1818CB9C-48F3-C29C-DDB0-C4BFEFA54AD0";
	setAttr ".ihi" 0;
	setAttr -s 5 ".hyp";
createNode network -n "L_Cheek_Config";
	rename -uid "F4614D07-464B-72D7-07BB-26AA6CF73D5E";
	addAttr -ci true -sn "precode" -ln "precode" -dt "string";
	addAttr -ci true -sn "Build_Command" -ln "Build_Command" -dt "string";
	addAttr -ci true -sn "Import_Command" -ln "Import_Command" -dt "string";
	addAttr -ci true -sn "SetParent" -ln "SetParent" -dt "string";
	addAttr -ci true -sn "Mirror" -ln "Mirror" -min 0 -max 1 -at "bool";
	addAttr -ci true -sn "AutoRotate" -ln "AutoRotate" -min 0 -max 1 -at "bool";
	addAttr -ci true -sn "CtrlSize" -ln "CtrlSize" -dv 1 -min 1 -max 20 -at "long";
	addAttr -ci true -sn "CtrlColor" -ln "CtrlColor" -min 0 -max 7 -en "lightBlue:blue:white:purple:green:red:yellow:grey" 
		-at "enum";
	addAttr -ci true -sn "CtrlType" -ln "CtrlType" -min 0 -max 16 -en "square:sphere:cube:octagon:hexagon:pringle:feet:hand:circleY:circleX:circleZ:3dArrow:2dArrow:mover:2dArrow:root:cog" 
		-at "enum";
	addAttr -ci true -sn "TwistAxis" -ln "TwistAxis" -min 0 -max 2 -en "X:Y:Z" -at "enum";
	addAttr -ci true -sn "Help" -ln "Help" -dt "string";
	addAttr -ci true -sn "postcode" -ln "postcode" -dt "string";
	setAttr ".precode" -type "string" "";
	setAttr -l on ".Build_Command" -type "string" "exec_chain.build_chain_block()";
	setAttr -l on ".Import_Command" -type "string" "import exec_chain";
	setAttr ".SetParent" -type "string" "Head_Ctrl";
	setAttr -cb on ".Mirror" yes;
	setAttr -cb on ".AutoRotate";
	setAttr -k on ".CtrlSize";
	setAttr -cb on ".CtrlColor";
	setAttr -cb on ".CtrlType";
	setAttr -cb on ".TwistAxis";
	setAttr ".Help" -type "string" "Create a FK Chain";
	setAttr ".postcode" -type "string" "";
createNode hyperLayout -n "hyperLayout82";
	rename -uid "87A386D9-4E92-91DA-5324-088E4090517C";
	setAttr ".ihi" 0;
	setAttr -s 2 ".hyp";
createNode network -n "L_CheekBone_Config";
	rename -uid "B4782BC9-462A-6C70-65F8-76A58AF8D40A";
	addAttr -ci true -sn "precode" -ln "precode" -dt "string";
	addAttr -ci true -sn "Build_Command" -ln "Build_Command" -dt "string";
	addAttr -ci true -sn "Import_Command" -ln "Import_Command" -dt "string";
	addAttr -ci true -sn "SetParent" -ln "SetParent" -dt "string";
	addAttr -ci true -sn "Equal" -ln "Equal" -min 0 -max 1 -at "bool";
	addAttr -ci true -sn "Ctrls" -ln "Ctrls" -dv 5 -min 1 -max 20 -at "long";
	addAttr -ci true -sn "Joints" -ln "Joints" -dv 5 -min 1 -max 20 -at "long";
	addAttr -ci true -sn "Constraint" -ln "Constraint" -min 0 -max 1 -at "bool";
	addAttr -ci true -sn "AddFk" -ln "AddFk" -min 0 -max 1 -at "bool";
	addAttr -ci true -sn "Wire" -ln "Wire" -min 0 -max 1 -at "bool";
	addAttr -ci true -sn "MiddleCtrlPosition" -ln "MiddleCtrlPosition" -min 0 -max 2 
		-en "Original:Start:End" -at "enum";
	addAttr -ci true -sn "Help" -ln "Help" -dt "string";
	addAttr -ci true -sn "postcode" -ln "postcode" -dt "string";
	setAttr ".precode" -type "string" "";
	setAttr -l on ".Build_Command" -type "string" "exec_ribbonizer.build_ribbonizer_block()";
	setAttr -l on ".Import_Command" -type "string" "import exec_ribbonizer";
	setAttr ".SetParent" -type "string" "Head_Ctrl";
	setAttr -cb on ".Equal" yes;
	setAttr -k on ".Ctrls" 3;
	setAttr -k on ".Joints" 3;
	setAttr -cb on ".Constraint" yes;
	setAttr -cb on ".AddFk";
	setAttr -cb on ".Wire";
	setAttr -cb on ".MiddleCtrlPosition";
	setAttr ".Help" -type "string" "Remove constraint for a local system.";
	setAttr ".postcode" -type "string" "";
createNode hyperLayout -n "hyperLayout83";
	rename -uid "58C215B8-4B56-EDCC-6576-2486FF6C3CB5";
	setAttr ".ihi" 0;
	setAttr -s 2 ".hyp";
createNode network -n "R_CheekBone_Config";
	rename -uid "CF4BB9DF-4DBE-AA04-896E-CA8638E7CB13";
	addAttr -ci true -sn "precode" -ln "precode" -dt "string";
	addAttr -ci true -sn "Build_Command" -ln "Build_Command" -dt "string";
	addAttr -ci true -sn "Import_Command" -ln "Import_Command" -dt "string";
	addAttr -ci true -sn "SetParent" -ln "SetParent" -dt "string";
	addAttr -ci true -sn "Equal" -ln "Equal" -min 0 -max 1 -at "bool";
	addAttr -ci true -sn "Ctrls" -ln "Ctrls" -dv 5 -min 1 -max 20 -at "long";
	addAttr -ci true -sn "Joints" -ln "Joints" -dv 5 -min 1 -max 20 -at "long";
	addAttr -ci true -sn "Constraint" -ln "Constraint" -min 0 -max 1 -at "bool";
	addAttr -ci true -sn "AddFk" -ln "AddFk" -min 0 -max 1 -at "bool";
	addAttr -ci true -sn "Wire" -ln "Wire" -min 0 -max 1 -at "bool";
	addAttr -ci true -sn "MiddleCtrlPosition" -ln "MiddleCtrlPosition" -min 0 -max 2 
		-en "Original:Start:End" -at "enum";
	addAttr -ci true -sn "Help" -ln "Help" -dt "string";
	addAttr -ci true -sn "postcode" -ln "postcode" -dt "string";
	setAttr ".precode" -type "string" "";
	setAttr -l on ".Build_Command" -type "string" "exec_ribbonizer.build_ribbonizer_block()";
	setAttr -l on ".Import_Command" -type "string" "import exec_ribbonizer";
	setAttr ".SetParent" -type "string" "Head_Ctrl";
	setAttr -cb on ".Equal" yes;
	setAttr -k on ".Ctrls" 3;
	setAttr -k on ".Joints" 3;
	setAttr -cb on ".Constraint" yes;
	setAttr -cb on ".AddFk";
	setAttr -cb on ".Wire";
	setAttr -cb on ".MiddleCtrlPosition";
	setAttr ".Help" -type "string" "Remove constraint for a local system.";
	setAttr ".postcode" -type "string" "";
createNode hyperLayout -n "hyperLayout84";
	rename -uid "74BFB4F2-4804-6D0B-F13D-92AA66EA8574";
	setAttr ".ihi" 0;
	setAttr -s 5 ".hyp";
createNode network -n "Mid_Brow_Config";
	rename -uid "2544DC0A-47E9-55FF-D524-9D8AE76AEE9C";
	addAttr -ci true -sn "precode" -ln "precode" -dt "string";
	addAttr -ci true -sn "Build_Command" -ln "Build_Command" -dt "string";
	addAttr -ci true -sn "Import_Command" -ln "Import_Command" -dt "string";
	addAttr -ci true -sn "SetParent" -ln "SetParent" -dt "string";
	addAttr -ci true -sn "Mirror" -ln "Mirror" -min 0 -max 1 -at "bool";
	addAttr -ci true -sn "AutoRotate" -ln "AutoRotate" -min 0 -max 1 -at "bool";
	addAttr -ci true -sn "CtrlSize" -ln "CtrlSize" -dv 1 -min 1 -max 20 -at "long";
	addAttr -ci true -sn "CtrlColor" -ln "CtrlColor" -min 0 -max 7 -en "lightBlue:blue:white:purple:green:red:yellow:grey" 
		-at "enum";
	addAttr -ci true -sn "CtrlType" -ln "CtrlType" -min 0 -max 16 -en "square:sphere:cube:octagon:hexagon:pringle:feet:hand:circleY:circleX:circleZ:3dArrow:2dArrow:mover:2dArrow:root:cog" 
		-at "enum";
	addAttr -ci true -sn "TwistAxis" -ln "TwistAxis" -min 0 -max 2 -en "X:Y:Z" -at "enum";
	addAttr -ci true -sn "Help" -ln "Help" -dt "string";
	addAttr -ci true -sn "postcode" -ln "postcode" -dt "string";
	setAttr ".precode" -type "string" "";
	setAttr -l on ".Build_Command" -type "string" "exec_chain.build_chain_block()";
	setAttr -l on ".Import_Command" -type "string" "import exec_chain";
	setAttr ".SetParent" -type "string" "Head_Ctrl";
	setAttr -cb on ".Mirror";
	setAttr -cb on ".AutoRotate";
	setAttr -k on ".CtrlSize";
	setAttr -cb on ".CtrlColor" 4;
	setAttr -cb on ".CtrlType" 1;
	setAttr -cb on ".TwistAxis";
	setAttr ".Help" -type "string" "Create a FK Chain";
	setAttr ".postcode" -type "string" "";
createNode hyperLayout -n "hyperLayout91";
	rename -uid "702C86D2-471D-34B4-5CAB-32BE6EEC82CE";
	setAttr ".ihi" 0;
	setAttr -s 2 ".hyp";
createNode network -n "PushMidBrow_Config";
	rename -uid "739EACC6-4564-354A-85CF-258A56FB2090";
	addAttr -ci true -sn "precode" -ln "precode" -dt "string";
	addAttr -ci true -sn "Build_Command" -ln "Build_Command" -dt "string";
	addAttr -ci true -sn "Import_Command" -ln "Import_Command" -dt "string";
	addAttr -ci true -sn "Exec" -ln "Exec" -min 0 -max 1 -en "Python:Mel" -at "enum";
	addAttr -ci true -sn "Code" -ln "Code" -dt "string";
	addAttr -ci true -sn "postcode" -ln "postcode" -dt "string";
	setAttr ".precode" -type "string" "";
	setAttr -l on ".Build_Command" -type "string" "exec_code.build_code_block()";
	setAttr -l on ".Import_Command" -type "string" "import exec_code";
	setAttr -cb on ".Exec";
	setAttr ".Code" -type "string" (
		"import maya.cmds as cmds\nfrom Mutant_Tools.Utils.Rigging import main_mutant\nmt = main_mutant.Mutant()\n\nroot_grp, auto_grp = mt.root_grp('Mid_Brow_A_Ctrl', autoRoot=True)\nforward_grp = mt.root_grp('Mid_Brow_A_Ctrl', custom=True, custom_name='_Forward')[0]\n\n\ndriverA = 'L_Brow_Driver0_Jnt'\ndriverB = 'R_Brow_Driver0_Jnt'\ndriverC = 'Head_Ctrl'\n\npc = cmds.parentConstraint(driverA, driverB, driverC, auto_grp, mo=True, skipRotate=[\"x\", \"y\", \"z\"])[0]\nweights = cmds.listAttr(pc, ud=True)\nA_w = f\"{pc}.{weights[0]}\"\nB_w = f\"{pc}.{weights[1]}\"\nC_w = f\"{pc}.{weights[2]}\"\n\nattrA = driverA.replace(\":\", \"_\")\nattrB = driverB.replace(\":\", \"_\")\nattrC = driverC.replace(\":\", \"_\")\n\ncmds.addAttr('Mid_Brow_A_Ctrl', ln=attrA, min=0, max=1, dv=1, k=True)\ncmds.addAttr('Mid_Brow_A_Ctrl', ln=attrB, min=0, max=1, dv=1, k=True)\ncmds.addAttr('Mid_Brow_A_Ctrl', ln=attrC, min=0, max=1, dv=1, k=True)\n\ncmds.connectAttr(f\"Mid_Brow_A_Ctrl.{attrA}\", A_w, f=True)\ncmds.connectAttr(f\"Mid_Brow_A_Ctrl.{attrB}\", B_w, f=True)\ncmds.connectAttr(f\"Mid_Brow_A_Ctrl.{attrC}\", C_w, f=True)\n"
		+ "\n#Push Automation\nleft_driver = 'L_Brow_Driver0_Jnt'\nright_driver = 'R_Brow_Driver0_Jnt'\n\n\ndef setup_brow_auto_push(\n    L_driver=\"L_Brow_Driver0_Jnt\",\n    R_driver=\"R_Brow_Driver0_Main_Ctrl\",\n    mid_ctrl=\"Mid_Brow_A_Ctrl\",\n    mid_grp=forward_grp,\n):\n    # ===============================\n    #  Helper – create utility node\n    # ===============================\n    def create(name, node_type):\n        if cmds.objExists(name):\n            return name\n        return cmds.createNode(node_type, name=name)\n\n    # ============================================\n    #  LEFT SIDE NODES\n    # ============================================\n    gt_L = create(\"L_gt_autoPush\", \"condition\")       # same as greaterThan\n    md_L = create(\"L_md_autoPush\", \"multiplyDivide\")\n    bc_L = create(\"L_bc_autoPush\", \"blendColors\")\n\n    # condition node setup (GREATER THAN)\n    cmds.setAttr(gt_L + \".operation\", 2)  # 2 = Greater Than\n\n    # connect L driver\n    cmds.connectAttr(L_driver + \".translateX\", gt_L + \".firstTerm\")\n    cmds.connectAttr(L_driver + \".translateX\", md_L + \".input1X\")\n"
		+ "\n    # multiplyDivide input2X = -1\n    cmds.setAttr(md_L + \".input2X\", -1)\n\n    # blendColors\n    cmds.connectAttr(gt_L + \".outColorR\", bc_L + \".blender\")\n    cmds.connectAttr(md_L + \".outputX\", bc_L + \".color1R\")\n\n    # output ? plusMinusAverage input1D[0]\n    pma = create(\"Brow_autoPush_PMA\", \"plusMinusAverage\")\n    cmds.connectAttr(bc_L + \".outputR\", pma + \".input1D[0]\")\n\n    # ============================================\n    #  RIGHT SIDE NODES\n    # ============================================\n    gt_R = create(\"R_gt_autoPush\", \"condition\")\n    md_R = create(\"R_md_autoPush\", \"multiplyDivide\")\n    bc_R = create(\"R_bc_autoPush\", \"blendColors\")\n\n    cmds.setAttr(gt_R + \".operation\", 2)  # Greater Than\n\n    cmds.connectAttr(R_driver + \".translateX\", gt_R + \".firstTerm\")\n    cmds.connectAttr(R_driver + \".translateX\", md_R + \".input1X\")\n    cmds.setAttr(md_R + \".input2X\", -1)\n\n    cmds.connectAttr(gt_R + \".outColorR\", bc_R + \".blender\")\n    cmds.connectAttr(md_R + \".outputX\", bc_R + \".color1R\")\n\n    # output ? plusMinusAverage input1D[1]\n"
		+ "    cmds.connectAttr(bc_R + \".outputR\", pma + \".input1D[1]\")\n\n    # ============================================\n    # Add autoPush attribute on Mid Brow Ctrl\n    # ============================================\n    if not cmds.attributeQuery(\"autoPush\", node=mid_ctrl, exists=True):\n        cmds.addAttr(mid_ctrl, ln=\"autoPush\", at=\"double\", min=0, dv=1, keyable=True)\n\n    # ============================================\n    # Final multiplyDivide\n    # ============================================\n    final_md = create(\"Mid_autoPush_MD\", \"multiplyDivide\")\n\n    cmds.connectAttr(pma + \".output1D\", final_md + \".input1X\")\n    cmds.connectAttr(mid_ctrl + \".autoPush\", final_md + \".input2X\")\n\n    # to group translate Z\n    cmds.connectAttr(final_md + \".outputX\", mid_grp + \".translateZ\")\n\n    print(\"? Brow auto-push setup complete.\")\n\n\n# RUN\nsetup_brow_auto_push()\n");
	setAttr ".postcode" -type "string" "";
createNode hyperLayout -n "hyperLayout85";
	rename -uid "69F5FA0C-4E20-12CD-F76E-E4B03DEBBBE5";
	setAttr ".ihi" 0;
	setAttr -s 5 ".hyp";
createNode network -n "Mid_BrowNose_Config";
	rename -uid "492E308C-4D58-87AD-741B-228D433FFF34";
	addAttr -ci true -sn "precode" -ln "precode" -dt "string";
	addAttr -ci true -sn "Build_Command" -ln "Build_Command" -dt "string";
	addAttr -ci true -sn "Import_Command" -ln "Import_Command" -dt "string";
	addAttr -ci true -sn "SetParent" -ln "SetParent" -dt "string";
	addAttr -ci true -sn "Mirror" -ln "Mirror" -min 0 -max 1 -at "bool";
	addAttr -ci true -sn "AutoRotate" -ln "AutoRotate" -min 0 -max 1 -at "bool";
	addAttr -ci true -sn "CtrlSize" -ln "CtrlSize" -dv 1 -min 1 -max 20 -at "long";
	addAttr -ci true -sn "CtrlColor" -ln "CtrlColor" -min 0 -max 7 -en "lightBlue:blue:white:purple:green:red:yellow:grey" 
		-at "enum";
	addAttr -ci true -sn "CtrlType" -ln "CtrlType" -min 0 -max 16 -en "square:sphere:cube:octagon:hexagon:pringle:feet:hand:circleY:circleX:circleZ:3dArrow:2dArrow:mover:2dArrow:root:cog" 
		-at "enum";
	addAttr -ci true -sn "TwistAxis" -ln "TwistAxis" -min 0 -max 2 -en "X:Y:Z" -at "enum";
	addAttr -ci true -sn "Help" -ln "Help" -dt "string";
	addAttr -ci true -sn "postcode" -ln "postcode" -dt "string";
	setAttr ".precode" -type "string" "";
	setAttr -l on ".Build_Command" -type "string" "exec_chain.build_chain_block()";
	setAttr -l on ".Import_Command" -type "string" "import exec_chain";
	setAttr ".SetParent" -type "string" "Head_Ctrl";
	setAttr -cb on ".Mirror";
	setAttr -cb on ".AutoRotate";
	setAttr -k on ".CtrlSize";
	setAttr -cb on ".CtrlColor" 4;
	setAttr -cb on ".CtrlType";
	setAttr -cb on ".TwistAxis";
	setAttr ".Help" -type "string" "Create a FK Chain";
	setAttr ".postcode" -type "string" "";
createNode hyperLayout -n "hyperLayout93";
	rename -uid "923A4080-4B6B-1E1C-40D8-CBA86CE31053";
	setAttr ".ihi" 0;
	setAttr -s 2 ".hyp";
createNode network -n "PushBrowNose_Config";
	rename -uid "9949774B-4949-4E25-9F23-E28E4531CD17";
	addAttr -ci true -sn "precode" -ln "precode" -dt "string";
	addAttr -ci true -sn "Build_Command" -ln "Build_Command" -dt "string";
	addAttr -ci true -sn "Import_Command" -ln "Import_Command" -dt "string";
	addAttr -ci true -sn "Exec" -ln "Exec" -min 0 -max 1 -en "Python:Mel" -at "enum";
	addAttr -ci true -sn "Code" -ln "Code" -dt "string";
	addAttr -ci true -sn "postcode" -ln "postcode" -dt "string";
	setAttr ".precode" -type "string" "";
	setAttr -l on ".Build_Command" -type "string" "exec_code.build_code_block()";
	setAttr -l on ".Import_Command" -type "string" "import exec_code";
	setAttr -cb on ".Exec";
	setAttr ".Code" -type "string" (
		"import maya.cmds as cmds\nfrom Mutant_Tools.Utils.Rigging import main_mutant\nmt = main_mutant.Mutant()\n\nroot_grp, auto_grp = mt.root_grp('Mid_BrowNose_A_Ctrl', autoRoot=True)\n\ndef setup_nose_bridge_push(\n    mid_brow_auto_grp=\"Mid_Brow_A_Ctrl_Auto_Grp\",\n    nose_ctrl=\"Mid_BrowNose_A_Ctrl\",\n    nose_auto_grp=\"Mid_BrowNose_A_Ctrl_Auto_Grp\",\n):\n    def create(name, node_type):\n        # Must use shadingNode for math nodes\n        if cmds.objExists(name):\n            return name\n        return cmds.shadingNode(node_type, asUtility=True, name=name)\n\n    # ======================================================\n    # 1. REAL lessThan node\n    # ======================================================\n    lt = create(\"NoseBridge_lessThan\", \"lessThan\")\n\n    # EXPLICITLY match your working MEL:\n    cmds.connectAttr(f\"{mid_brow_auto_grp}.translateY\", f\"{lt}.input1\", force=True)\n\n    # input2 defaults to 0 ? correct for your setup\n    # cmds.setAttr(lt + \".input2\", 0)\n\n    # ======================================================\n"
		+ "    # 2. blendColors\n    # ======================================================\n    bc = create(\"NoseBridge_blend\", \"blendColors\")\n\n    cmds.connectAttr(f\"{lt}.output\", f\"{bc}.blender\", force=True)\n    cmds.connectAttr(f\"{mid_brow_auto_grp}.translateY\", f\"{bc}.color1R\", force=True)\n\n    # ======================================================\n    # 3. First multiplyDivide ( * -1 )\n    # ======================================================\n    md_neg = create(\"NoseBridge_md_neg\", \"multiplyDivide\")\n\n    cmds.connectAttr(f\"{bc}.outputR\", f\"{md_neg}.input1X\", force=True)\n    cmds.setAttr(f\"{md_neg}.input2X\", -1)\n\n    # ======================================================\n    # 4. Add autoPush attr\n    # ======================================================\n    if not cmds.attributeQuery(\"autoPush\", node=nose_ctrl, exists=True):\n        cmds.addAttr(nose_ctrl, ln=\"autoPush\", at=\"double\", min=0, dv=1, keyable=True)\n\n    # ======================================================\n    # 5. Second multiplyDivide (final scaling)\n"
		+ "    # ======================================================\n    md_final = create(\"NoseBridge_md_final\", \"multiplyDivide\")\n\n    cmds.connectAttr(f\"{md_neg}.outputX\", f\"{md_final}.input1X\", force=True)\n    cmds.connectAttr(f\"{nose_ctrl}.autoPush\", f\"{md_final}.input2X\", force=True)\n\n    # ======================================================\n    # 6. Output ? Nose Auto Group translateZ \n    # ======================================================\n    cmds.connectAttr(f\"{md_final}.outputX\", f\"{nose_auto_grp}.translateZ\", force=True)\n\n    print(\"? Nose bridge push (lessThan version) created successfully.\")\n\n\n# RUN\nsetup_nose_bridge_push()\n\ncmds.setAttr(\"Mid_BrowNose_A_Ctrl.autoPush\", 3)");
	setAttr ".postcode" -type "string" "";
createNode hyperLayout -n "hyperLayout102";
	rename -uid "18EEF7DB-4669-432A-8FE4-E6A20E733C54";
	setAttr ".ihi" 0;
	setAttr -s 5 ".hyp";
createNode network -n "UpperTeeth_Config";
	rename -uid "9BE013DA-4903-9D0A-DDF0-FBBF93846209";
	addAttr -ci true -sn "precode" -ln "precode" -dt "string";
	addAttr -ci true -sn "Build_Command" -ln "Build_Command" -dt "string";
	addAttr -ci true -sn "Import_Command" -ln "Import_Command" -dt "string";
	addAttr -ci true -sn "SetParent" -ln "SetParent" -dt "string";
	addAttr -ci true -sn "Mirror" -ln "Mirror" -min 0 -max 1 -at "bool";
	addAttr -ci true -sn "AutoRotate" -ln "AutoRotate" -min 0 -max 1 -at "bool";
	addAttr -ci true -sn "CtrlSize" -ln "CtrlSize" -dv 1 -min 1 -max 20 -at "long";
	addAttr -ci true -sn "CtrlColor" -ln "CtrlColor" -min 0 -max 7 -en "lightBlue:blue:white:purple:green:red:yellow:grey" 
		-at "enum";
	addAttr -ci true -sn "CtrlType" -ln "CtrlType" -min 0 -max 16 -en "square:sphere:cube:octagon:hexagon:pringle:feet:hand:circleY:circleX:circleZ:3dArrow:2dArrow:mover:2dArrow:root:cog" 
		-at "enum";
	addAttr -ci true -sn "TwistAxis" -ln "TwistAxis" -min 0 -max 2 -en "X:Y:Z" -at "enum";
	addAttr -ci true -sn "Help" -ln "Help" -dt "string";
	addAttr -ci true -sn "postcode" -ln "postcode" -dt "string";
	setAttr ".precode" -type "string" "";
	setAttr -l on ".Build_Command" -type "string" "exec_chain.build_chain_block()";
	setAttr -l on ".Import_Command" -type "string" "import exec_chain";
	setAttr ".SetParent" -type "string" "Head_Ctrl";
	setAttr -cb on ".Mirror";
	setAttr -cb on ".AutoRotate";
	setAttr -k on ".CtrlSize";
	setAttr -cb on ".CtrlColor";
	setAttr -cb on ".CtrlType";
	setAttr -cb on ".TwistAxis";
	setAttr ".Help" -type "string" "Create a FK Chain";
	setAttr ".postcode" -type "string" "";
createNode hyperLayout -n "hyperLayout103";
	rename -uid "E49F55DA-495C-FA7F-0DC5-EC8FB81B6B38";
	setAttr ".ihi" 0;
	setAttr -s 5 ".hyp";
createNode network -n "LowerTeeth_Config";
	rename -uid "C2DFCA51-4ACA-176C-374C-4D96616CEFA7";
	addAttr -ci true -sn "precode" -ln "precode" -dt "string";
	addAttr -ci true -sn "Build_Command" -ln "Build_Command" -dt "string";
	addAttr -ci true -sn "Import_Command" -ln "Import_Command" -dt "string";
	addAttr -ci true -sn "SetParent" -ln "SetParent" -dt "string";
	addAttr -ci true -sn "Mirror" -ln "Mirror" -min 0 -max 1 -at "bool";
	addAttr -ci true -sn "AutoRotate" -ln "AutoRotate" -min 0 -max 1 -at "bool";
	addAttr -ci true -sn "CtrlSize" -ln "CtrlSize" -dv 1 -min 1 -max 20 -at "long";
	addAttr -ci true -sn "CtrlColor" -ln "CtrlColor" -min 0 -max 7 -en "lightBlue:blue:white:purple:green:red:yellow:grey" 
		-at "enum";
	addAttr -ci true -sn "CtrlType" -ln "CtrlType" -min 0 -max 16 -en "square:sphere:cube:octagon:hexagon:pringle:feet:hand:circleY:circleX:circleZ:3dArrow:2dArrow:mover:2dArrow:root:cog" 
		-at "enum";
	addAttr -ci true -sn "TwistAxis" -ln "TwistAxis" -min 0 -max 2 -en "X:Y:Z" -at "enum";
	addAttr -ci true -sn "Help" -ln "Help" -dt "string";
	addAttr -ci true -sn "postcode" -ln "postcode" -dt "string";
	setAttr ".precode" -type "string" "";
	setAttr -l on ".Build_Command" -type "string" "exec_chain.build_chain_block()";
	setAttr -l on ".Import_Command" -type "string" "import exec_chain";
	setAttr ".SetParent" -type "string" "Mouth_Jaw_Ctrl";
	setAttr -cb on ".Mirror";
	setAttr -cb on ".AutoRotate";
	setAttr -k on ".CtrlSize";
	setAttr -cb on ".CtrlColor";
	setAttr -cb on ".CtrlType";
	setAttr -cb on ".TwistAxis";
	setAttr ".Help" -type "string" "Create a FK Chain";
	setAttr ".postcode" -type "string" "";
createNode hyperLayout -n "hyperLayout104";
	rename -uid "5B40EC75-4C9E-6349-7368-B1BF4B7E94FA";
	setAttr ".ihi" 0;
	setAttr -s 20 ".hyp";
createNode network -n "Tongue_Config";
	rename -uid "551394B0-4B2E-257C-9763-58953D68D5C3";
	addAttr -ci true -sn "precode" -ln "precode" -dt "string";
	addAttr -ci true -sn "Build_Command" -ln "Build_Command" -dt "string";
	addAttr -ci true -sn "Import_Command" -ln "Import_Command" -dt "string";
	addAttr -ci true -sn "SetParent" -ln "SetParent" -dt "string";
	addAttr -ci true -sn "Mirror" -ln "Mirror" -min 0 -max 1 -at "bool";
	addAttr -ci true -sn "AutoRotate" -ln "AutoRotate" -min 0 -max 1 -at "bool";
	addAttr -ci true -sn "CtrlSize" -ln "CtrlSize" -dv 1 -min 1 -max 20 -at "long";
	addAttr -ci true -sn "CtrlColor" -ln "CtrlColor" -min 0 -max 7 -en "lightBlue:blue:white:purple:green:red:yellow:grey" 
		-at "enum";
	addAttr -ci true -sn "CtrlType" -ln "CtrlType" -min 0 -max 16 -en "square:sphere:cube:octagon:hexagon:pringle:feet:hand:circleY:circleX:circleZ:3dArrow:2dArrow:mover:2dArrow:root:cog" 
		-at "enum";
	addAttr -ci true -sn "TwistAxis" -ln "TwistAxis" -min 0 -max 2 -en "X:Y:Z" -at "enum";
	addAttr -ci true -sn "Help" -ln "Help" -dt "string";
	addAttr -ci true -sn "postcode" -ln "postcode" -dt "string";
	setAttr ".precode" -type "string" "";
	setAttr -l on ".Build_Command" -type "string" "exec_chain.build_chain_block()";
	setAttr -l on ".Import_Command" -type "string" "import exec_chain";
	setAttr ".SetParent" -type "string" "Mouth_Jaw_Ctrl";
	setAttr -cb on ".Mirror";
	setAttr -cb on ".AutoRotate" yes;
	setAttr -k on ".CtrlSize";
	setAttr -cb on ".CtrlColor";
	setAttr -cb on ".CtrlType";
	setAttr -cb on ".TwistAxis";
	setAttr ".Help" -type "string" "Create a FK Chain";
	setAttr ".postcode" -type "string" "";
createNode hyperLayout -n "hyperLayout78";
	rename -uid "B064CBBA-4A8E-A31C-D8E4-A1AB9073C83A";
	setAttr ".ihi" 0;
createNode network -n "ConvertFace_Config";
	rename -uid "028D62EA-4D76-0932-EBFC-E9B35CF0841B";
	addAttr -ci true -sn "precode" -ln "precode" -dt "string";
	addAttr -ci true -sn "Build_Command" -ln "Build_Command" -dt "string";
	addAttr -ci true -sn "Import_Command" -ln "Import_Command" -dt "string";
	addAttr -ci true -sn "Engine" -ln "Engine" -min 0 -max 1 -en "unity:unreal" -at "enum";
	addAttr -ci true -sn "scale" -ln "scale" -min 0 -max 2 -en "None:Direct:Constraints" 
		-at "enum";
	addAttr -ci true -sn "Help" -ln "Help" -dt "string";
	addAttr -ci true -sn "postcode" -ln "postcode" -dt "string";
	setAttr ".precode" -type "string" "";
	setAttr -l on ".Build_Command" -type "string" "exec_convertbody.build_convertbody_block()";
	setAttr -l on ".Import_Command" -type "string" "import exec_convertbody";
	setAttr -cb on ".Engine";
	setAttr -cb on ".scale";
	setAttr ".Help" -type "string" "Will convert Mutant Bnd Joints to Games Skeleton Joints";
	setAttr ".postcode" -type "string" "";
createNode hyperLayout -n "hyperLayout89";
	rename -uid "198C15C7-4534-1F63-4101-9DBE4F433196";
	setAttr ".ihi" 0;
	setAttr -s 2 ".hyp";
createNode network -n "CheekAutomations_Config";
	rename -uid "8029F97B-4DB6-DE8C-F25A-2DBA2C628DEA";
	addAttr -ci true -sn "precode" -ln "precode" -dt "string";
	addAttr -ci true -sn "Build_Command" -ln "Build_Command" -dt "string";
	addAttr -ci true -sn "Import_Command" -ln "Import_Command" -dt "string";
	addAttr -ci true -sn "Exec" -ln "Exec" -min 0 -max 1 -en "Python:Mel" -at "enum";
	addAttr -ci true -sn "Code" -ln "Code" -dt "string";
	addAttr -ci true -sn "postcode" -ln "postcode" -dt "string";
	setAttr ".precode" -type "string" "";
	setAttr -l on ".Build_Command" -type "string" "exec_code.build_code_block()";
	setAttr -l on ".Import_Command" -type "string" "import exec_code";
	setAttr -cb on ".Exec";
	setAttr ".Code" -type "string" (
		"import maya.cmds as cmds\nfrom Mutant_Tools.Utils.Rigging import main_mutant\nmt = main_mutant.Mutant()\n\ndef setup_cheek(ctrl, driverA, driverB, rotations=True):\n    # Attribute names based on the driver controllers\n    attrA = driverA.replace(\":\", \"_\")\n    attrB = driverB.replace(\":\", \"_\")\n\n    # Add attrs\n    if not cmds.attributeQuery(attrA, node=ctrl, exists=True):\n        cmds.addAttr(ctrl, ln=attrA, min=0, max=1, dv=1, k=True)\n    if not cmds.attributeQuery(attrB, node=ctrl, exists=True):\n        cmds.addAttr(ctrl, ln=attrB, min=0, max=1, dv=1, k=True)\n\n    # Create root and auto groups\n    root_grp, auto_grp = mt.root_grp(ctrl, autoRoot=True)\n\n    # ---------------------------\n    # Constraint selection\n    # ---------------------------\n    if rotations:\n        pc = cmds.parentConstraint(driverA, driverB, auto_grp, mo=True)[0]\n    else:\n        pc = cmds.parentConstraint(driverA, driverB, auto_grp, mo=True, skipRotate=[\"x\", \"y\", \"z\"])[0]\n    \n    cmds.setAttr(pc + '.interpType', 2)  # shortest\n\n    # Get the constraint weight plugs\n"
		+ "    weights = cmds.listAttr(pc, ud=True)\n    A_w = f\"{pc}.{weights[0]}\"\n    B_w = f\"{pc}.{weights[1]}\"\n\n    # Defaults\n    cmds.setAttr(A_w, 1)\n    cmds.setAttr(B_w, 1)\n\n    # Connect attributes ? weights\n    cmds.connectAttr(f\"{ctrl}.{attrA}\", A_w, f=True)\n    cmds.connectAttr(f\"{ctrl}.{attrB}\", B_w, f=True)\n\n    return root_grp, auto_grp\n\n\n# ============================\n# CALLS\n# ============================\nsetup_cheek(\"L_Cheek_A_Ctrl\",  \"L_CheekBone_1_Main_Ctrl\", \"L_Mouth_Main_Ctrl\", rotations=True)\nsetup_cheek(\"R_Cheek_A_Ctrl\",  \"R_CheekBone_1_Main_Ctrl\", \"R_Mouth_Main_Ctrl\", rotations=True)\n\nsetup_cheek(\"L_CheekBone_1_Main_Ctrl\", \"L_CheekBone_1_Ctrl_Main_Offset_Grp\", \"L_Mouth_Main_Ctrl\", rotations=False)\nsetup_cheek(\"R_CheekBone_1_Main_Ctrl\", \"R_CheekBone_1_Ctrl_Main_Offset_Grp\", \"R_Mouth_Main_Ctrl\", rotations=False)\n\nsetup_cheek(\"L_Nostril_A_Ctrl\",  \"Head_Ctrl\", \"L_Mouth_Main_Ctrl\", rotations=False)\nsetup_cheek(\"R_Nostril_A_Ctrl\",  \"Head_Ctrl\", \"R_Mouth_Main_Ctrl\", rotations=False)\n\ncmds.connectAttr('L_Cheek_A_Ctrl.s','L_Cheek_A_Skl.s')\n"
		+ "cmds.connectAttr('R_Cheek_A_Ctrl.s','R_Cheek_A_Skl.s')\n\ncmds.setAttr('L_Cheek_A_Ctrl.L_CheekBone_1_Main_Ctrl', 0.75)\ncmds.setAttr('L_CheekBone_1_Main_Ctrl.L_Mouth_Main_Ctrl', 0.15)\ncmds.setAttr('R_Cheek_A_Ctrl.R_CheekBone_1_Main_Ctrl', 0.75)\ncmds.setAttr('R_CheekBone_1_Main_Ctrl.R_Mouth_Main_Ctrl', 0.15)\n\ncmds.setAttr('L_Nostril_A_Ctrl.L_Mouth_Main_Ctrl', 0.25)\ncmds.setAttr('R_Nostril_A_Ctrl.R_Mouth_Main_Ctrl', 0.25)\n\nattrs = [\n    \"L_CheekBone_1_Main_Ctrl_Auto_Grp.tx\",\n    \"L_CheekBone_1_Main_Ctrl_Auto_Grp.tz\",\n    \"R_CheekBone_1_Main_Ctrl_Auto_Grp.tx\",\n    \"R_CheekBone_1_Main_Ctrl_Auto_Grp.tz\",\n]\n\nfor attr in attrs:\n    connections = cmds.listConnections(attr, plugs=True, source=True, destination=False) or []\n    for src in connections:\n        cmds.disconnectAttr(src, attr)\n\nprint(\"Cheek setup done!\")");
	setAttr ".postcode" -type "string" "";
createNode hyperLayout -n "hyperLayout108";
	rename -uid "CF85BFB9-446F-43F8-49D3-1FBF8DE05130";
	setAttr ".ihi" 0;
	setAttr -s 2 ".hyp";
createNode network -n "CheekPushZ_Config";
	rename -uid "D966E184-48D6-37A7-9F9D-59A3D0543837";
	addAttr -ci true -sn "precode" -ln "precode" -dt "string";
	addAttr -ci true -sn "Build_Command" -ln "Build_Command" -dt "string";
	addAttr -ci true -sn "Import_Command" -ln "Import_Command" -dt "string";
	addAttr -ci true -sn "Exec" -ln "Exec" -min 0 -max 1 -en "Python:Mel" -at "enum";
	addAttr -ci true -sn "Code" -ln "Code" -dt "string";
	addAttr -ci true -sn "postcode" -ln "postcode" -dt "string";
	setAttr ".precode" -type "string" "";
	setAttr -l on ".Build_Command" -type "string" "exec_code.build_code_block()";
	setAttr -l on ".Import_Command" -type "string" "import exec_code";
	setAttr -cb on ".Exec";
	setAttr ".Code" -type "string" (
		"from maya import cmds\nimport Mutant_Tools\nimport Mutant_Tools.Utils.Rigging\nfrom Mutant_Tools.Utils.Rigging import main_mutant\n\nmt = main_mutant.Mutant()\nnc, curve_data, setup = mt.import_configs()\n\nl_push_grp = mt.root_grp(\n    input='L_Cheek_A_Ctrl',\n    custom=True,\n    custom_name='_Push',\n    autoRoot=False,\n    replace_nc=False\n\n)[0]\n\nr_push_grp = mt.root_grp(\n    input='R_Cheek_A_Ctrl',\n    custom=True,\n    custom_name='_Push',\n    autoRoot=False,\n    replace_nc=False\n\n)[0]\n\nimport maya.cmds as cmds\n\n\n\n\ndef build_cheek_push(side):\n    \"\"\"\n    side: 'L' or 'R'\n    \"\"\"\n\n    mouth_ctrl = f'{side}_Mouth_Main_Ctrl'\n    cheek_ctrl = f'{side}_Cheek_A_Ctrl'\n    push_grp  = f'{side}_Cheek_A_Ctrl_Push_Grp'\n\n    # --------------------------------------------------\n    # ATTRIBUTES\n    # --------------------------------------------------\n    def add_push_attrs(ctrl):\n        \"\"\"\n        Adds WidePush and UpPush attrs to the given ctrl\n        Default = 0.5, Min = 0, Keyable\n        \"\"\"\n        for attr in ['WidePush', 'UpPush']:\n"
		+ "            if not cmds.attributeQuery(attr, n=ctrl, exists=True):\n                cmds.addAttr(\n                    ctrl,\n                    ln=attr,\n                    at='double',\n                    min=0,\n                    dv=0.5\n                )\n                cmds.setAttr(f'{ctrl}.{attr}', e=True, keyable=True)\n            \n    add_push_attrs(cheek_ctrl)\n\n    # --------------------------------------------------\n    # UP PUSH CHAIN\n    # --------------------------------------------------\n    md_up = cmds.createNode(\n        'multiplyDivide',\n        n=f'{side}_Cheek_UpPush_MD'\n    )\n    cmds.connectAttr(f'{mouth_ctrl}.ty', f'{md_up}.input1X', f=True)\n    cmds.connectAttr(f'{cheek_ctrl}.UpPush', f'{md_up}.input2X', f=True)\n\n    gt_up = cmds.createNode(\n        'greaterThan',\n        n=f'{side}_Cheek_UpPush_GT'\n    )\n    cmds.connectAttr(f'{mouth_ctrl}.ty', f'{gt_up}.input1', f=True)\n    cmds.setAttr(f'{gt_up}.input2', 0)\n\n    bc_up = cmds.createNode(\n        'blendColors',\n        n=f'{side}_Cheek_UpPush_BC'\n"
		+ "    )\n    cmds.connectAttr(f'{gt_up}.output', f'{bc_up}.blender', f=True)\n    cmds.connectAttr(f'{md_up}.outputX', f'{bc_up}.color1R', f=True)\n    cmds.setAttr(f'{bc_up}.color2R', 0)\n\n    # --------------------------------------------------\n    # WIDE PUSH CHAIN\n    # --------------------------------------------------\n    md_wide = cmds.createNode(\n        'multiplyDivide',\n        n=f'{side}_Cheek_WidePush_MD'\n    )\n    cmds.connectAttr(f'{mouth_ctrl}.tx', f'{md_wide}.input1X', f=True)\n    cmds.connectAttr(f'{cheek_ctrl}.WidePush', f'{md_wide}.input2X', f=True)\n\n    gt_wide = cmds.createNode(\n        'greaterThan',\n        n=f'{side}_Cheek_WidePush_GT'\n    )\n    cmds.connectAttr(f'{mouth_ctrl}.tx', f'{gt_wide}.input1', f=True)\n    cmds.setAttr(f'{gt_wide}.input2', 0)\n\n    bc_wide = cmds.createNode(\n        'blendColors',\n        n=f'{side}_Cheek_WidePush_BC'\n    )\n    cmds.connectAttr(f'{gt_wide}.output', f'{bc_wide}.blender', f=True)\n    cmds.connectAttr(f'{md_wide}.outputX', f'{bc_wide}.color1R', f=True)\n    cmds.setAttr(f'{bc_wide}.color2R', 0)\n"
		+ "\n    # --------------------------------------------------\n    # SUM\n    # --------------------------------------------------\n    sum_node = cmds.createNode(\n        'plusMinusAverage',\n        n=f'{side}_Cheek_Push_SUM'\n    )\n    cmds.setAttr(f'{sum_node}.operation', 1)  # sum\n\n    cmds.connectAttr(f'{bc_up}.outputR', f'{sum_node}.input1D[0]', f=True)\n    cmds.connectAttr(f'{bc_wide}.outputR', f'{sum_node}.input1D[1]', f=True)\n\n    # --------------------------------------------------\n    # OUTPUT\n    # --------------------------------------------------\n    if side == 'R':\n        flip_md = cmds.createNode(\n            'multiplyDivide',\n            n=f'{side}_Cheek_Push_Flip_MD'\n        )\n        cmds.setAttr(f'{flip_md}.input2X', -1)\n\n        cmds.connectAttr(\n            f'{sum_node}.output1D',\n            f'{flip_md}.input1X',\n            f=True\n        )\n        cmds.connectAttr(\n            f'{flip_md}.outputX',\n            f'{push_grp}.translateZ',\n            f=True\n        )\n    else:\n        cmds.connectAttr(\n"
		+ "            f'{sum_node}.output1D',\n            f'{push_grp}.translateZ',\n            f=True\n        )\n    \n    \n\n# --------------------------------------------------\n# BUILD BOTH SIDES\n# --------------------------------------------------\nfor side in ['L', 'R']:\n    build_cheek_push(side)\n");
	setAttr ".postcode" -type "string" "";
createNode hyperLayout -n "hyperLayout80";
	rename -uid "978BF631-4C73-1CF4-880B-7F95A840F5B0";
	setAttr ".ihi" 0;
	setAttr -s 2 ".hyp";
createNode network -n "FaceHierarchy_Config";
	rename -uid "690E980B-48BE-5191-805A-79855398F9CD";
	addAttr -ci true -sn "precode" -ln "precode" -dt "string";
	addAttr -ci true -sn "Build_Command" -ln "Build_Command" -dt "string";
	addAttr -ci true -sn "Import_Command" -ln "Import_Command" -dt "string";
	addAttr -ci true -sn "Exec" -ln "Exec" -min 0 -max 1 -en "Python:Mel" -at "enum";
	addAttr -ci true -sn "Code" -ln "Code" -dt "string";
	addAttr -ci true -sn "postcode" -ln "postcode" -dt "string";
	setAttr ".precode" -type "string" "";
	setAttr -l on ".Build_Command" -type "string" "exec_code.build_code_block()";
	setAttr -l on ".Import_Command" -type "string" "import exec_code";
	setAttr -cb on ".Exec";
	setAttr ".Code" -type "string" (
		"from maya import cmds\n\nface_joints = [\n    'L_Brow_0_Skl', 'L_Brow_1_Skl', 'L_Brow_2_Skl', 'L_Brow_3_Skl', 'L_Brow_4_Skl',\n    'L_Cheek_A_Skl',\n    'L_Eyelids_Dw__cv2_Skl', 'L_Eyelids_Dw__cv3_Skl', 'L_Eyelids_Dw__cv4_Skl',\n    'L_Eyelids_Up__cv2_Skl', 'L_Eyelids_Up__cv3_Skl', 'L_Eyelids_Up__cv4_Skl',\n    'L_Mid_01_Mouth_Dw_Tweek_Skl', 'L_Mid_01_Mouth_Up_Tweek_Skl',\n    'L_Mid_02_Mouth_Dw_Tweek_Skl', 'L_Mid_02_Mouth_Up_Tweek_Skl',\n    'L_Mid_03_Mouth_Dw_Tweek_Skl', 'L_Mid_03_Mouth_Up_Tweek_Skl',\n    'L_Mouth_Dw_Tweek_Skl', 'L_Mouth_Up_Tweek_Skl', 'L_Nostril_A_Skl',\n    'Mid_Mouth_Dw_Tweek_Skl', 'Mid_Mouth_Up_Tweek_Skl',\n    'Mouth_Jaw_Skl', 'Nose_Base_Skl',\n\n    'R_Brow_0_Skl', 'R_Brow_1_Skl', 'R_Brow_2_Skl', 'R_Brow_3_Skl', 'R_Brow_4_Skl',\n    'R_Cheek_A_Skl',\n    'R_Eyelids_Dw__cv2_Skl', 'R_Eyelids_Dw__cv3_Skl', 'R_Eyelids_Dw__cv4_Skl',\n    'R_Eyelids_Up__cv2_Skl', 'R_Eyelids_Up__cv3_Skl', 'R_Eyelids_Up__cv4_Skl',\n    'R_Mid_01_Mouth_Dw_Tweek_Skl', 'R_Mid_01_Mouth_Up_Tweek_Skl',\n    'R_Mid_02_Mouth_Dw_Tweek_Skl', 'R_Mid_02_Mouth_Up_Tweek_Skl',\n"
		+ "    'R_Mid_03_Mouth_Dw_Tweek_Skl', 'R_Mid_03_Mouth_Up_Tweek_Skl',\n    'R_Mouth_Dw_Tweek_Skl', 'R_Mouth_Up_Tweek_Skl', 'R_Nostril_A_Skl',\n\n\n    'R_Orbicularis_1_Bind_08_Skl', 'R_Orbicularis_1_Bind_07_Skl', 'R_Orbicularis_1_Bind_06_Skl',\n    'R_Orbicularis_1_Bind_05_Skl', 'R_Orbicularis_1_Bind_04_Skl', 'R_Orbicularis_1_Bind_03_Skl',\n    'R_Orbicularis_1_Bind_02_Skl', 'R_Orbicularis_1_Bind_01_Skl',\n    'R_CheekBone_1_Bind_03_Skl', 'R_CheekBone_1_Bind_02_Skl', 'R_CheekBone_1_Bind_01_Skl',\n    'Mid_Brow_A_Skl', 'Mid_BrowNose_A_Skl',\n    'L_Orbicularis_1_Bind_08_Skl', 'L_Orbicularis_1_Bind_07_Skl', 'L_Orbicularis_1_Bind_06_Skl',\n    'L_Orbicularis_1_Bind_05_Skl', 'L_Orbicularis_1_Bind_04_Skl', 'L_Orbicularis_1_Bind_03_Skl',\n    'L_Orbicularis_1_Bind_02_Skl', 'L_Orbicularis_1_Bind_01_Skl',\n    'L_CheekBone_1_Bind_03_Skl', 'L_CheekBone_1_Bind_02_Skl', 'L_CheekBone_1_Bind_01_Skl',\n\n'Tongue_A_Skl','UpperTeeth_Skl','LowerTeeth_Skl'\n]\n\nfor jnt in face_joints:\n    cmds.parent(jnt, \"Head_Skl\")\n\n");
	setAttr ".postcode" -type "string" "";
select -ne :time1;
	setAttr -av -k on ".cch";
	setAttr -av -k on ".fzn";
	setAttr -av -cb on ".ihi";
	setAttr -av -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -k on ".o" 0;
	setAttr -av -k on ".unw";
	setAttr -av -k on ".etw";
	setAttr -av -k on ".tps";
	setAttr -av -k on ".tms";
select -ne :hardwareRenderingGlobals;
	setAttr -av -k on ".cch";
	setAttr -av -k on ".fzn";
	setAttr -av -k on ".ihi";
	setAttr -av -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -av -k on ".rm";
	setAttr -av -k on ".lm";
	setAttr ".otfna" -type "stringArray" 22 "NURBS Curves" "NURBS Surfaces" "Polygons" "Subdiv Surface" "Particles" "Particle Instance" "Fluids" "Strokes" "Image Planes" "UI" "Lights" "Cameras" "Locators" "Joints" "IK Handles" "Deformers" "Motion Trails" "Components" "Hair Systems" "Follicles" "Misc. UI" "Ornaments"  ;
	setAttr ".otfva" -type "Int32Array" 22 0 1 1 1 1 1
		 1 1 1 0 0 0 0 0 0 0 0 0
		 0 0 0 0 ;
	setAttr -av -k on ".hom";
	setAttr -av -k on ".hodm";
	setAttr -av -k on ".xry";
	setAttr -av -k on ".jxr";
	setAttr -av -k on ".sslt";
	setAttr -av -k on ".cbr";
	setAttr -av -k on ".bbr";
	setAttr -av -k on ".mhl";
	setAttr -av -k on ".cons";
	setAttr -av -k on ".vac";
	setAttr -av -k on ".hwi";
	setAttr -av -k on ".csvd";
	setAttr -av -k on ".ta";
	setAttr -av -k on ".tq";
	setAttr -av -k on ".ts";
	setAttr -av -k on ".etmr";
	setAttr -k on ".tmrm";
	setAttr -av -k on ".tmr";
	setAttr -av -k on ".aoon";
	setAttr -av -k on ".aoam";
	setAttr -av -k on ".aora";
	setAttr -av -k on ".aofr";
	setAttr -av -k on ".aosm";
	setAttr -av -k on ".hff";
	setAttr -av -k on ".hfd";
	setAttr -av -k on ".hfs";
	setAttr -av -k on ".hfe";
	setAttr -av ".hfc";
	setAttr -av -k on ".hfcr";
	setAttr -av -k on ".hfcg";
	setAttr -av -k on ".hfcb";
	setAttr -av -k on ".hfa";
	setAttr -av -k on ".mbe";
	setAttr -av -k on ".mbt";
	setAttr -av -k on ".mbsof";
	setAttr -av -k on ".mbsc";
	setAttr -av -k on ".mbc";
	setAttr -av -k on ".mbfa";
	setAttr -av -k on ".mbftb";
	setAttr -av -k on ".mbftg";
	setAttr -av -k on ".mbftr";
	setAttr -av -k on ".mbfta";
	setAttr -av -k on ".mbfe";
	setAttr -av -k on ".mbme";
	setAttr -av -k on ".mbcsx";
	setAttr -av -k on ".mbcsy";
	setAttr -av -k on ".mbasx";
	setAttr -av -k on ".mbasy";
	setAttr -av -k on ".blen";
	setAttr -av -k on ".blth";
	setAttr -av -k on ".blfr";
	setAttr -av -k on ".blfa";
	setAttr -av -k on ".blat";
	setAttr -av -k on ".msaa";
	setAttr -av -k on ".aasc";
	setAttr -av -k on ".aasq";
	setAttr -av -k on ".laa";
	setAttr -k on ".gamm";
	setAttr -k on ".gmmv";
	setAttr -k on ".fprt" yes;
	setAttr -av -k on ".rtfm" 1;
select -ne :renderPartition;
	setAttr -av -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -av -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -s 2 ".st";
	setAttr -cb on ".an";
	setAttr -cb on ".pt";
select -ne :renderGlobalsList1;
	setAttr -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -k on ".nds";
	setAttr -cb on ".bnm";
select -ne :defaultShaderList1;
	setAttr -av -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -av -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -s 6 ".s";
select -ne :postProcessList1;
	setAttr -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -av -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -s 2 ".p";
select -ne :defaultRenderingList1;
	setAttr -av -k on ".cch";
	setAttr -k on ".ihi";
	setAttr -av -k on ".nds";
	setAttr -cb on ".bnm";
select -ne :standardSurface1;
	setAttr ".bc" -type "float3" 0.40000001 0.40000001 0.40000001 ;
	setAttr ".sr" 0.5;
select -ne :openPBR_shader1;
	setAttr ".bc" -type "float3" 0.40000001 0.40000001 0.40000001 ;
	setAttr ".sr" 0.5;
select -ne :initialShadingGroup;
	setAttr -av -k on ".cch";
	setAttr -k on ".fzn";
	setAttr -av -cb on ".ihi";
	setAttr -av -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -k on ".bbx";
	setAttr -k on ".vwm";
	setAttr -k on ".tpv";
	setAttr -k on ".uit";
	setAttr -s 5 ".dsm";
	setAttr -k on ".mwc";
	setAttr -av -cb on ".an";
	setAttr -cb on ".il";
	setAttr -cb on ".vo";
	setAttr -cb on ".eo";
	setAttr -cb on ".fo";
	setAttr -cb on ".epo";
	setAttr -k on ".ro" yes;
	setAttr -k on ".hio";
	setAttr -cb on ".ai_override";
	setAttr -k on ".ai_surface_shader";
	setAttr -cb on ".ai_surface_shaderr";
	setAttr -cb on ".ai_surface_shaderg";
	setAttr -cb on ".ai_surface_shaderb";
	setAttr -k on ".ai_volume_shader";
	setAttr -cb on ".ai_volume_shaderr";
	setAttr -cb on ".ai_volume_shaderg";
	setAttr -cb on ".ai_volume_shaderb";
select -ne :initialParticleSE;
	setAttr -av -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -av -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -cb on ".mwc";
	setAttr -cb on ".an";
	setAttr -cb on ".il";
	setAttr -cb on ".vo";
	setAttr -cb on ".eo";
	setAttr -cb on ".fo";
	setAttr -cb on ".epo";
	setAttr -k on ".ro" yes;
	setAttr -cb on ".ai_override";
	setAttr -k on ".ai_surface_shader";
	setAttr -cb on ".ai_surface_shaderr";
	setAttr -cb on ".ai_surface_shaderg";
	setAttr -cb on ".ai_surface_shaderb";
	setAttr -k on ".ai_volume_shader";
	setAttr -cb on ".ai_volume_shaderr";
	setAttr -cb on ".ai_volume_shaderg";
	setAttr -cb on ".ai_volume_shaderb";
select -ne :defaultRenderGlobals;
	setAttr -av -k on ".cch";
	setAttr -av -cb on ".ihi";
	setAttr -av -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -av -k on ".macc";
	setAttr -av -k on ".macd";
	setAttr -av -k on ".macq";
	setAttr -av -k on ".mcfr";
	setAttr -cb on ".ifg";
	setAttr -av -k on ".clip";
	setAttr -av -k on ".edm";
	setAttr -av -k on ".edl";
	setAttr -av -k on ".ren" -type "string" "arnold";
	setAttr -av -k on ".esr";
	setAttr -av -k on ".ors";
	setAttr -k on ".sdf";
	setAttr -av -k on ".outf";
	setAttr -av -cb on ".imfkey";
	setAttr -av -k on ".gama";
	setAttr -av -k on ".exrc";
	setAttr -av -k on ".expt";
	setAttr -av -k on ".an";
	setAttr -cb on ".ar";
	setAttr -av -k on ".fs";
	setAttr -av -k on ".ef";
	setAttr -av -k on ".bfs";
	setAttr -av -cb on ".me";
	setAttr -cb on ".se";
	setAttr -av -k on ".be";
	setAttr -av -k on ".ep";
	setAttr -av -k on ".fec";
	setAttr -av -k on ".ofc";
	setAttr -k on ".ofe";
	setAttr -k on ".efe";
	setAttr -k on ".oft";
	setAttr -cb on ".umfn";
	setAttr -cb on ".ufe";
	setAttr -av -k on ".pff";
	setAttr -av -cb on ".peie";
	setAttr -av -k on ".ifp";
	setAttr -av -k on ".rv";
	setAttr -av -k on ".comp";
	setAttr -av -k on ".cth";
	setAttr -av -k on ".soll";
	setAttr -av -cb on ".sosl";
	setAttr -av -k on ".rd";
	setAttr -av -k on ".lp";
	setAttr -av -k on ".sp";
	setAttr -av -k on ".shs";
	setAttr -av -k on ".lpr";
	setAttr -cb on ".gv";
	setAttr -cb on ".sv";
	setAttr -av -k on ".mm";
	setAttr -av -k on ".npu";
	setAttr -av -k on ".itf";
	setAttr -av -k on ".shp";
	setAttr -cb on ".isp";
	setAttr -av -k on ".uf";
	setAttr -av -k on ".oi";
	setAttr -av -k on ".rut";
	setAttr -av -k on ".mot";
	setAttr -av -cb on ".mb";
	setAttr -av -k on ".mbf";
	setAttr -av -k on ".mbso";
	setAttr -av -k on ".mbsc";
	setAttr -av -k on ".afp";
	setAttr -av -k on ".pfb";
	setAttr -av -k on ".pram";
	setAttr -av -k on ".poam";
	setAttr -av -k on ".prlm";
	setAttr -av -k on ".polm";
	setAttr -av -k on ".prm";
	setAttr -av -k on ".pom";
	setAttr -k on ".pfrm";
	setAttr -k on ".pfom";
	setAttr -av -k on ".bll";
	setAttr -av -k on ".bls";
	setAttr -av -k on ".smv";
	setAttr -av -k on ".ubc";
	setAttr -av -k on ".mbc";
	setAttr -cb on ".mbt";
	setAttr -av -k on ".udbx";
	setAttr -av -k on ".smc";
	setAttr -av -k on ".kmv";
	setAttr -cb on ".isl";
	setAttr -cb on ".ism";
	setAttr -cb on ".imb";
	setAttr -av -k on ".rlen";
	setAttr -av -k on ".frts";
	setAttr -av -k on ".tlwd";
	setAttr -av -k on ".tlht";
	setAttr -av -k on ".jfc";
	setAttr -cb on ".rsb";
	setAttr -av -k on ".ope";
	setAttr -av -k on ".oppf";
	setAttr -av -k on ".rcp";
	setAttr -av -k on ".icp";
	setAttr -av -k on ".ocp";
	setAttr -k on ".hbl";
select -ne :defaultResolution;
	setAttr -av -k on ".cch";
	setAttr -av -k on ".ihi";
	setAttr -av -k on ".nds";
	setAttr -k on ".bnm";
	setAttr -av -k on ".w";
	setAttr -av -k on ".h";
	setAttr -av -k on ".pa" 1;
	setAttr -av -k on ".al";
	setAttr -av -k on ".dar";
	setAttr -av -k on ".ldar";
	setAttr -av -k on ".dpi";
	setAttr -av -k on ".off";
	setAttr -av -k on ".fld";
	setAttr -av -k on ".zsl";
	setAttr -av -k on ".isu";
	setAttr -av -k on ".pdu";
select -ne :defaultColorMgtGlobals;
	setAttr -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr ".cfe" yes;
	setAttr ".cfp" -type "string" "<MAYA_RESOURCES>/OCIO-configs/Maya2022-default/config.ocio";
	setAttr ".vtn" -type "string" "ACES 1.0 SDR-video (sRGB)";
	setAttr ".vn" -type "string" "ACES 1.0 SDR-video";
	setAttr ".dn" -type "string" "sRGB";
	setAttr ".wsn" -type "string" "ACEScg";
	setAttr ".otn" -type "string" "ACES 1.0 SDR-video (sRGB)";
	setAttr ".potn" -type "string" "ACES 1.0 SDR-video (sRGB)";
select -ne :hardwareRenderGlobals;
	setAttr -av -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -av -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -av -k off -cb on ".ctrs" 256;
	setAttr -av -k off -cb on ".btrs" 512;
	setAttr -av -k off -cb on ".fbfm";
	setAttr -av -k off -cb on ".ehql";
	setAttr -av -k off -cb on ".eams";
	setAttr -av -k off -cb on ".eeaa";
	setAttr -av -k off -cb on ".engm";
	setAttr -av -k off -cb on ".mes";
	setAttr -av -k off -cb on ".emb";
	setAttr -av -k off -cb on ".mbbf";
	setAttr -av -k off -cb on ".mbs";
	setAttr -av -k off -cb on ".trm";
	setAttr -av -k off -cb on ".tshc";
	setAttr -av -k off -cb on ".enpt";
	setAttr -av -k off -cb on ".clmt";
	setAttr -av -k off -cb on ".tcov";
	setAttr -av -k off -cb on ".lith";
	setAttr -av -k off -cb on ".sobc";
	setAttr -av -k off -cb on ".cuth";
	setAttr -av -k off -cb on ".hgcd";
	setAttr -av -k off -cb on ".hgci";
	setAttr -av -k off -cb on ".mgcs";
	setAttr -av -k off -cb on ".twa";
	setAttr -av -k off -cb on ".twz";
	setAttr -k on ".hwcc";
	setAttr -k on ".hwdp";
	setAttr -k on ".hwql";
	setAttr -k on ".hwfr";
	setAttr -k on ".soll";
	setAttr -k on ".sosl";
	setAttr -k on ".bswa";
	setAttr -k on ".shml";
	setAttr -k on ".hwel";
connectAttr "hyperLayout72.msg" "VisAttrs_Block.hl";
connectAttr "VisAttrs_Config.nds" "VisAttrs_Block.nds";
connectAttr "VisAttrs_Guide.RotateOrder" "VisAttrs_Guide.ro";
connectAttr "hyperLayout70.msg" "L_Brow_Block.hl";
connectAttr "L_Brow_Config.nds" "L_Brow_Block.nds";
connectAttr "hyperLayout71.msg" "L_Eyelids_Block.hl";
connectAttr "L_Eyelids_Config.nds" "L_Eyelids_Block.nds";
connectAttr "hyperLayout86.msg" "L_Orbicularis_Block.hl";
connectAttr "L_Orbicularis_Config.nds" "L_Orbicularis_Block.nds";
connectAttr "makeNurbCylinder1.os" "L_Orbicularis_GuideShape.cr";
connectAttr "hyperLayout87.msg" "R_Orbicularis_Block.hl";
connectAttr "R_Orbicularis_Config.nds" "R_Orbicularis_Block.nds";
connectAttr "hyperLayout73.msg" "Mouth_Block.hl";
connectAttr "Mouth_Config.nds" "Mouth_Block.nds";
connectAttr "L_Mouth_Orient_Guide_Guide.Helper" "L_Mouth_Orient_Guide_Guide_CtrlShape.v"
		;
connectAttr "L_Mouth_Orient_Guide_Guide.Helper" "L_Mouth_Orient_Guide_Guide_Ctrl_CtrlShape.v"
		;
connectAttr "L_Mouth_Orient_Guide_Guide.Helper" "L_Mouth_Orient_Guide_Guide_Ctrl_Ctrl_CtrlShape.v"
		;
connectAttr "L_Mouth_Orient_Guide_Guide.Helper" "L_Mouth_Orient_Guide_Guide_Ctrl_Ctrl_Ctrl_CtrlShape.v"
		;
connectAttr "Mouth_SlideCenter_Guide_Guide.Helper" "Mouth_SlideCenter_Guide_Guide_CtrlShape.v"
		;
connectAttr "Mouth_SlideCenter_Guide_Guide.Helper" "Mouth_SlideCenter_Guide_Guide_Ctrl_CtrlShape.v"
		;
connectAttr "Mouth_SlideCenter_Guide_Guide.Helper" "Mouth_SlideCenter_Guide_Guide_Ctrl_Ctrl_CtrlShape.v"
		;
connectAttr "Mouth_SlideCenter_Guide_Guide.Helper" "Mouth_SlideCenter_Guide_Guide_Ctrl_Ctrl_Ctrl_CtrlShape.v"
		;
connectAttr "Mouth_Jaw_Guide_Guide.Helper" "Mouth_Jaw_Guide_Guide_CtrlShape.v";
connectAttr "Mouth_Jaw_Guide_Guide.Helper" "Mouth_Jaw_Guide_Guide_Ctrl_CtrlShape.v"
		;
connectAttr "Mouth_Jaw_Guide_Guide.Helper" "Mouth_Jaw_Guide_Guide_Ctrl_Ctrl_CtrlShape.v"
		;
connectAttr "Mouth_Jaw_Guide_Guide.Helper" "Mouth_Jaw_Guide_Guide_Ctrl_Ctrl_Ctrl_CtrlShape.v"
		;
connectAttr "Mouth_LipUp_Guide_Guide.Helper" "Mouth_LipUp_Guide_Guide_CtrlShape.v"
		;
connectAttr "Mouth_LipUp_Guide_Guide.Helper" "Mouth_LipUp_Guide_Guide_Ctrl_CtrlShape.v"
		;
connectAttr "Mouth_LipUp_Guide_Guide.Helper" "Mouth_LipUp_Guide_Guide_Ctrl_Ctrl_CtrlShape.v"
		;
connectAttr "Mouth_LipUp_Guide_Guide.Helper" "Mouth_LipUp_Guide_Guide_Ctrl_Ctrl_Ctrl_CtrlShape.v"
		;
connectAttr "Mouth_LipDown_Guide_Guide.Helper" "Mouth_LipDown_Guide_Guide_CtrlShape.v"
		;
connectAttr "Mouth_LipDown_Guide_Guide.Helper" "Mouth_LipDown_Guide_Guide_Ctrl_CtrlShape.v"
		;
connectAttr "Mouth_LipDown_Guide_Guide.Helper" "Mouth_LipDown_Guide_Guide_Ctrl_Ctrl_CtrlShape.v"
		;
connectAttr "Mouth_LipDown_Guide_Guide.Helper" "Mouth_LipDown_Guide_Guide_Ctrl_Ctrl_Ctrl_CtrlShape.v"
		;
connectAttr "hyperLayout74.msg" "Nose_Block.hl";
connectAttr "Nose_Config.nds" "Nose_Block.nds";
connectAttr "Nose_Base_Guide.Helper" "Nose_Base_Guide_CtrlShape.v";
connectAttr "Nose_Base_Guide.Helper" "Nose_Base_Guide_Ctrl_CtrlShape.v";
connectAttr "Nose_Base_Guide.Helper" "Nose_Base_Guide_Ctrl_Ctrl_CtrlShape.v";
connectAttr "Nose_Base_Guide.Helper" "Nose_Base_Guide_Ctrl_Ctrl_Ctrl_CtrlShape.v"
		;
connectAttr "Nose_Base_Guide.s" "Nose_Bridge_Guide.is";
connectAttr "Nose_Bridge_Guide.Helper" "Nose_Bridge_Guide_CtrlShape.v";
connectAttr "Nose_Bridge_Guide.Helper" "Nose_Bridge_Guide_Ctrl_CtrlShape.v";
connectAttr "Nose_Bridge_Guide.Helper" "Nose_Bridge_Guide_Ctrl_Ctrl_CtrlShape.v"
		;
connectAttr "Nose_Bridge_Guide.Helper" "Nose_Bridge_Guide_Ctrl_Ctrl_Ctrl_CtrlShape.v"
		;
connectAttr "Nose_Bridge_Guide.s" "Nose_Main_Guide.is";
connectAttr "Nose_Main_Guide.Helper" "Nose_Main_Guide_CtrlShape.v";
connectAttr "Nose_Main_Guide.Helper" "Nose_Main_Guide_Ctrl_CtrlShape.v";
connectAttr "Nose_Main_Guide.Helper" "Nose_Main_Guide_Ctrl_Ctrl_CtrlShape.v";
connectAttr "Nose_Main_Guide.Helper" "Nose_Main_Guide_Ctrl_Ctrl_Ctrl_CtrlShape.v"
		;
connectAttr "hyperLayout75.msg" "L_Nostril_Block.hl";
connectAttr "L_Nostril_Config.nds" "L_Nostril_Block.nds";
connectAttr "L_Nostril_A_Guide.Helper" "L_Nostril_A_Guide_CtrlShape.v";
connectAttr "L_Nostril_A_Guide.Helper" "L_Nostril_A_Guide_Ctrl_CtrlShape.v";
connectAttr "L_Nostril_A_Guide.Helper" "L_Nostril_A_Guide_Ctrl_Ctrl_CtrlShape.v"
		;
connectAttr "L_Nostril_A_Guide.Helper" "L_Nostril_A_Guide_Ctrl_Ctrl_Ctrl_CtrlShape.v"
		;
connectAttr "hyperLayout76.msg" "L_Cheek_Block.hl";
connectAttr "L_Cheek_Config.nds" "L_Cheek_Block.nds";
connectAttr "L_Cheek_A_Guide.Helper" "L_Cheek_A_Guide_CtrlShape.v";
connectAttr "L_Cheek_A_Guide.Helper" "L_Cheek_A_Guide_Ctrl_CtrlShape.v";
connectAttr "L_Cheek_A_Guide.Helper" "L_Cheek_A_Guide_Ctrl_Ctrl_CtrlShape.v";
connectAttr "L_Cheek_A_Guide.Helper" "L_Cheek_A_Guide_Ctrl_Ctrl_Ctrl_CtrlShape.v"
		;
connectAttr "hyperLayout82.msg" "L_CheekBone_Block.hl";
connectAttr "L_CheekBone_Config.nds" "L_CheekBone_Block.nds";
connectAttr "hyperLayout83.msg" "R_CheekBone_Block.hl";
connectAttr "R_CheekBone_Config.nds" "R_CheekBone_Block.nds";
connectAttr "hyperLayout84.msg" "Mid_Brow_Block.hl";
connectAttr "Mid_Brow_Config.nds" "Mid_Brow_Block.nds";
connectAttr "Mid_Brow_A_Guide.Helper" "Mid_Brow_A_Guide_CtrlShape.v";
connectAttr "Mid_Brow_A_Guide.Helper" "Mid_Brow_A_Guide_Ctrl_CtrlShape.v";
connectAttr "Mid_Brow_A_Guide.Helper" "Mid_Brow_A_Guide_Ctrl_Ctrl_CtrlShape.v";
connectAttr "Mid_Brow_A_Guide.Helper" "Mid_Brow_A_Guide_Ctrl_Ctrl_Ctrl_CtrlShape.v"
		;
connectAttr "hyperLayout91.msg" "PushMidBrow_Block.hl";
connectAttr "PushMidBrow_Config.nds" "PushMidBrow_Block.nds";
connectAttr "hyperLayout85.msg" "Mid_BrowNose_Block.hl";
connectAttr "Mid_BrowNose_Config.nds" "Mid_BrowNose_Block.nds";
connectAttr "Mid_BrowNose_A_Guide.Helper" "Mid_BrowNose_A_Guide_CtrlShape.v";
connectAttr "Mid_BrowNose_A_Guide.Helper" "Mid_BrowNose_A_Guide_Ctrl_CtrlShape.v"
		;
connectAttr "Mid_BrowNose_A_Guide.Helper" "Mid_BrowNose_A_Guide_Ctrl_Ctrl_CtrlShape.v"
		;
connectAttr "Mid_BrowNose_A_Guide.Helper" "Mid_BrowNose_A_Guide_Ctrl_Ctrl_Ctrl_CtrlShape.v"
		;
connectAttr "hyperLayout93.msg" "PushBrowNose_Block.hl";
connectAttr "PushBrowNose_Config.nds" "PushBrowNose_Block.nds";
connectAttr "hyperLayout102.msg" "UpperTeeth_Block.hl";
connectAttr "UpperTeeth_Config.nds" "UpperTeeth_Block.nds";
connectAttr "UpperTeeth_Guide.Helper" "UpperTeeth_Guide_CtrlShape.v";
connectAttr "UpperTeeth_Guide.Helper" "UpperTeeth_Guide_Ctrl_CtrlShape.v";
connectAttr "UpperTeeth_Guide.Helper" "UpperTeeth_Guide_Ctrl_Ctrl_CtrlShape.v";
connectAttr "UpperTeeth_Guide.Helper" "UpperTeeth_Guide_Ctrl_Ctrl_Ctrl_CtrlShape.v"
		;
connectAttr "hyperLayout103.msg" "LowerTeeth_Block.hl";
connectAttr "LowerTeeth_Config.nds" "LowerTeeth_Block.nds";
connectAttr "LowerTeeth_Guide.Helper" "LowerTeeth_Guide_CtrlShape.v";
connectAttr "LowerTeeth_Guide.Helper" "LowerTeeth_Guide_Ctrl_CtrlShape.v";
connectAttr "LowerTeeth_Guide.Helper" "LowerTeeth_Guide_Ctrl_Ctrl_CtrlShape.v";
connectAttr "LowerTeeth_Guide.Helper" "LowerTeeth_Guide_Ctrl_Ctrl_Ctrl_CtrlShape.v"
		;
connectAttr "hyperLayout104.msg" "Tongue_Block.hl";
connectAttr "Tongue_Config.nds" "Tongue_Block.nds";
connectAttr "Tongue_A_Guide.Helper" "Tongue_A_Guide_CtrlShape.v";
connectAttr "Tongue_A_Guide.Helper" "Tongue_A_Guide_Ctrl_CtrlShape.v";
connectAttr "Tongue_A_Guide.Helper" "Tongue_A_Guide_Ctrl_Ctrl_CtrlShape.v";
connectAttr "Tongue_A_Guide.Helper" "Tongue_A_Guide_Ctrl_Ctrl_Ctrl_CtrlShape.v";
connectAttr "Tongue_A_Guide.s" "Tongue_B_Guide.is";
connectAttr "Tongue_B_Guide.Helper" "Tongue_B_Guide_CtrlShape.v";
connectAttr "Tongue_B_Guide.Helper" "Tongue_B_Guide_Ctrl_CtrlShape.v";
connectAttr "Tongue_B_Guide.Helper" "Tongue_B_Guide_Ctrl_Ctrl_CtrlShape.v";
connectAttr "Tongue_B_Guide.Helper" "Tongue_B_Guide_Ctrl_Ctrl_Ctrl_CtrlShape.v";
connectAttr "Tongue_B_Guide.s" "Tongue_C_Guide.is";
connectAttr "Tongue_C_Guide.Helper" "Tongue_C_Guide_CtrlShape.v";
connectAttr "Tongue_C_Guide.Helper" "Tongue_C_Guide_Ctrl_CtrlShape.v";
connectAttr "Tongue_C_Guide.Helper" "Tongue_C_Guide_Ctrl_Ctrl_CtrlShape.v";
connectAttr "Tongue_C_Guide.Helper" "Tongue_C_Guide_Ctrl_Ctrl_Ctrl_CtrlShape.v";
connectAttr "Tongue_C_Guide.s" "Tongue_D_Guide.is";
connectAttr "Tongue_D_Guide.Helper" "Tongue_D_Guide_CtrlShape.v";
connectAttr "Tongue_D_Guide.Helper" "Tongue_D_Guide_Ctrl_CtrlShape.v";
connectAttr "Tongue_D_Guide.Helper" "Tongue_D_Guide_Ctrl_Ctrl_CtrlShape.v";
connectAttr "Tongue_D_Guide.Helper" "Tongue_D_Guide_Ctrl_Ctrl_Ctrl_CtrlShape.v";
connectAttr "hyperLayout78.msg" "ConvertFace_Block.hl";
connectAttr "ConvertFace_Config.nds" "ConvertFace_Block.nds";
connectAttr "hyperLayout89.msg" "CheekAutomations_Block.hl";
connectAttr "CheekAutomations_Config.nds" "CheekAutomations_Block.nds";
connectAttr "hyperLayout108.msg" "CheekPushZ_Block.hl";
connectAttr "CheekPushZ_Config.nds" "CheekPushZ_Block.nds";
connectAttr "hyperLayout80.msg" "FaceHierarchy_Block.hl";
connectAttr "FaceHierarchy_Config.nds" "FaceHierarchy_Block.nds";
connectAttr "VisAttrs_Guide.msg" "hyperLayout72.hyp[0].dn";
connectAttr "VisAttrs_GuideShape.msg" "hyperLayout72.hyp[1].dn";
connectAttr "L_Brow_Guide.msg" "hyperLayout70.hyp[0].dn";
connectAttr "L_Brow_GuideShape.msg" "hyperLayout70.hyp[1].dn";
connectAttr "Eyelids_Guide.msg" "hyperLayout71.hyp[0].dn";
connectAttr "L_Orbicularis_Guide.msg" "hyperLayout86.hyp[2].dn";
connectAttr "L_Orbicularis_GuideShape.msg" "hyperLayout86.hyp[3].dn";
connectAttr "R_Orbicularis_Guide.msg" "hyperLayout87.hyp[2].dn";
connectAttr "R_Orbicularis_GuideShape.msg" "hyperLayout87.hyp[3].dn";
connectAttr "L_Mouth_Orient_Guide_Guide.msg" "hyperLayout73.hyp[0].dn";
connectAttr "L_Mouth_Orient_Guide_Guide_CtrlShape.msg" "hyperLayout73.hyp[1].dn"
		;
connectAttr "L_Mouth_Orient_Guide_Guide_Ctrl_CtrlShape.msg" "hyperLayout73.hyp[2].dn"
		;
connectAttr "L_Mouth_Orient_Guide_Guide_Ctrl_Ctrl_CtrlShape.msg" "hyperLayout73.hyp[3].dn"
		;
connectAttr "L_Mouth_Orient_Guide_Guide_Ctrl_Ctrl_Ctrl_CtrlShape.msg" "hyperLayout73.hyp[4].dn"
		;
connectAttr "Mouth_SlideCenter_Guide_Guide.msg" "hyperLayout73.hyp[5].dn";
connectAttr "Mouth_SlideCenter_Guide_Guide_CtrlShape.msg" "hyperLayout73.hyp[6].dn"
		;
connectAttr "Mouth_SlideCenter_Guide_Guide_Ctrl_CtrlShape.msg" "hyperLayout73.hyp[7].dn"
		;
connectAttr "Mouth_SlideCenter_Guide_Guide_Ctrl_Ctrl_CtrlShape.msg" "hyperLayout73.hyp[8].dn"
		;
connectAttr "Mouth_SlideCenter_Guide_Guide_Ctrl_Ctrl_Ctrl_CtrlShape.msg" "hyperLayout73.hyp[9].dn"
		;
connectAttr "Mouth_Jaw_Guide_Guide.msg" "hyperLayout73.hyp[10].dn";
connectAttr "Mouth_Jaw_Guide_Guide_CtrlShape.msg" "hyperLayout73.hyp[11].dn";
connectAttr "Mouth_Jaw_Guide_Guide_Ctrl_CtrlShape.msg" "hyperLayout73.hyp[12].dn"
		;
connectAttr "Mouth_Jaw_Guide_Guide_Ctrl_Ctrl_CtrlShape.msg" "hyperLayout73.hyp[13].dn"
		;
connectAttr "Mouth_Jaw_Guide_Guide_Ctrl_Ctrl_Ctrl_CtrlShape.msg" "hyperLayout73.hyp[14].dn"
		;
connectAttr "Mouth_LipUp_Guide_Guide.msg" "hyperLayout73.hyp[15].dn";
connectAttr "Mouth_LipUp_Guide_Guide_CtrlShape.msg" "hyperLayout73.hyp[16].dn";
connectAttr "Mouth_LipUp_Guide_Guide_Ctrl_CtrlShape.msg" "hyperLayout73.hyp[17].dn"
		;
connectAttr "Mouth_LipUp_Guide_Guide_Ctrl_Ctrl_CtrlShape.msg" "hyperLayout73.hyp[18].dn"
		;
connectAttr "Mouth_LipUp_Guide_Guide_Ctrl_Ctrl_Ctrl_CtrlShape.msg" "hyperLayout73.hyp[19].dn"
		;
connectAttr "Mouth_LipDown_Guide_Guide.msg" "hyperLayout73.hyp[20].dn";
connectAttr "Mouth_LipDown_Guide_Guide_CtrlShape.msg" "hyperLayout73.hyp[21].dn"
		;
connectAttr "Mouth_LipDown_Guide_Guide_Ctrl_CtrlShape.msg" "hyperLayout73.hyp[22].dn"
		;
connectAttr "Mouth_LipDown_Guide_Guide_Ctrl_Ctrl_CtrlShape.msg" "hyperLayout73.hyp[23].dn"
		;
connectAttr "Mouth_LipDown_Guide_Guide_Ctrl_Ctrl_Ctrl_CtrlShape.msg" "hyperLayout73.hyp[24].dn"
		;
connectAttr "Nose_Base_Guide.msg" "hyperLayout74.hyp[0].dn";
connectAttr "Nose_Base_Guide_CtrlShape.msg" "hyperLayout74.hyp[1].dn";
connectAttr "Nose_Base_Guide_Ctrl_CtrlShape.msg" "hyperLayout74.hyp[2].dn";
connectAttr "Nose_Base_Guide_Ctrl_Ctrl_CtrlShape.msg" "hyperLayout74.hyp[3].dn";
connectAttr "Nose_Base_Guide_Ctrl_Ctrl_Ctrl_CtrlShape.msg" "hyperLayout74.hyp[4].dn"
		;
connectAttr "Nose_Bridge_Guide.msg" "hyperLayout74.hyp[5].dn";
connectAttr "Nose_Bridge_Guide_CtrlShape.msg" "hyperLayout74.hyp[6].dn";
connectAttr "Nose_Bridge_Guide_Ctrl_CtrlShape.msg" "hyperLayout74.hyp[7].dn";
connectAttr "Nose_Bridge_Guide_Ctrl_Ctrl_CtrlShape.msg" "hyperLayout74.hyp[8].dn"
		;
connectAttr "Nose_Bridge_Guide_Ctrl_Ctrl_Ctrl_CtrlShape.msg" "hyperLayout74.hyp[9].dn"
		;
connectAttr "Nose_Main_Guide.msg" "hyperLayout74.hyp[10].dn";
connectAttr "Nose_Main_Guide_CtrlShape.msg" "hyperLayout74.hyp[11].dn";
connectAttr "Nose_Main_Guide_Ctrl_CtrlShape.msg" "hyperLayout74.hyp[12].dn";
connectAttr "Nose_Main_Guide_Ctrl_Ctrl_CtrlShape.msg" "hyperLayout74.hyp[13].dn"
		;
connectAttr "Nose_Main_Guide_Ctrl_Ctrl_Ctrl_CtrlShape.msg" "hyperLayout74.hyp[14].dn"
		;
connectAttr "L_Nostril_A_Guide.msg" "hyperLayout75.hyp[0].dn";
connectAttr "L_Nostril_A_Guide_CtrlShape.msg" "hyperLayout75.hyp[1].dn";
connectAttr "L_Nostril_A_Guide_Ctrl_CtrlShape.msg" "hyperLayout75.hyp[2].dn";
connectAttr "L_Nostril_A_Guide_Ctrl_Ctrl_CtrlShape.msg" "hyperLayout75.hyp[3].dn"
		;
connectAttr "L_Nostril_A_Guide_Ctrl_Ctrl_Ctrl_CtrlShape.msg" "hyperLayout75.hyp[4].dn"
		;
connectAttr "L_Cheek_A_Guide.msg" "hyperLayout76.hyp[0].dn";
connectAttr "L_Cheek_A_Guide_CtrlShape.msg" "hyperLayout76.hyp[1].dn";
connectAttr "L_Cheek_A_Guide_Ctrl_CtrlShape.msg" "hyperLayout76.hyp[2].dn";
connectAttr "L_Cheek_A_Guide_Ctrl_Ctrl_CtrlShape.msg" "hyperLayout76.hyp[3].dn";
connectAttr "L_Cheek_A_Guide_Ctrl_Ctrl_Ctrl_CtrlShape.msg" "hyperLayout76.hyp[4].dn"
		;
connectAttr "L_CheekBone_Guide.msg" "hyperLayout82.hyp[0].dn";
connectAttr "L_CheekBone_GuideShape.msg" "hyperLayout82.hyp[1].dn";
connectAttr "R_CheekBone_Guide.msg" "hyperLayout83.hyp[2].dn";
connectAttr "R_CheekBone_GuideShape.msg" "hyperLayout83.hyp[3].dn";
connectAttr "Mid_Brow_A_Guide.msg" "hyperLayout84.hyp[0].dn";
connectAttr "Mid_Brow_A_Guide_CtrlShape.msg" "hyperLayout84.hyp[1].dn";
connectAttr "Mid_Brow_A_Guide_Ctrl_CtrlShape.msg" "hyperLayout84.hyp[2].dn";
connectAttr "Mid_Brow_A_Guide_Ctrl_Ctrl_CtrlShape.msg" "hyperLayout84.hyp[3].dn"
		;
connectAttr "Mid_Brow_A_Guide_Ctrl_Ctrl_Ctrl_CtrlShape.msg" "hyperLayout84.hyp[4].dn"
		;
connectAttr "PushMidBrow_Loc.msg" "hyperLayout91.hyp[0].dn";
connectAttr "PushMidBrow_LocShape.msg" "hyperLayout91.hyp[1].dn";
connectAttr "Mid_BrowNose_A_Guide.msg" "hyperLayout85.hyp[0].dn";
connectAttr "Mid_BrowNose_A_Guide_CtrlShape.msg" "hyperLayout85.hyp[1].dn";
connectAttr "Mid_BrowNose_A_Guide_Ctrl_CtrlShape.msg" "hyperLayout85.hyp[2].dn";
connectAttr "Mid_BrowNose_A_Guide_Ctrl_Ctrl_CtrlShape.msg" "hyperLayout85.hyp[3].dn"
		;
connectAttr "Mid_BrowNose_A_Guide_Ctrl_Ctrl_Ctrl_CtrlShape.msg" "hyperLayout85.hyp[4].dn"
		;
connectAttr "PushBrowNose_Loc.msg" "hyperLayout93.hyp[0].dn";
connectAttr "PushBrowNose_LocShape.msg" "hyperLayout93.hyp[1].dn";
connectAttr "UpperTeeth_Guide.msg" "hyperLayout102.hyp[0].dn";
connectAttr "UpperTeeth_Guide_CtrlShape.msg" "hyperLayout102.hyp[1].dn";
connectAttr "UpperTeeth_Guide_Ctrl_CtrlShape.msg" "hyperLayout102.hyp[2].dn";
connectAttr "UpperTeeth_Guide_Ctrl_Ctrl_CtrlShape.msg" "hyperLayout102.hyp[3].dn"
		;
connectAttr "UpperTeeth_Guide_Ctrl_Ctrl_Ctrl_CtrlShape.msg" "hyperLayout102.hyp[4].dn"
		;
connectAttr "LowerTeeth_Guide.msg" "hyperLayout103.hyp[0].dn";
connectAttr "LowerTeeth_Guide_CtrlShape.msg" "hyperLayout103.hyp[1].dn";
connectAttr "LowerTeeth_Guide_Ctrl_CtrlShape.msg" "hyperLayout103.hyp[2].dn";
connectAttr "LowerTeeth_Guide_Ctrl_Ctrl_CtrlShape.msg" "hyperLayout103.hyp[3].dn"
		;
connectAttr "LowerTeeth_Guide_Ctrl_Ctrl_Ctrl_CtrlShape.msg" "hyperLayout103.hyp[4].dn"
		;
connectAttr "Tongue_A_Guide.msg" "hyperLayout104.hyp[0].dn";
connectAttr "Tongue_A_Guide_CtrlShape.msg" "hyperLayout104.hyp[1].dn";
connectAttr "Tongue_A_Guide_Ctrl_CtrlShape.msg" "hyperLayout104.hyp[2].dn";
connectAttr "Tongue_A_Guide_Ctrl_Ctrl_CtrlShape.msg" "hyperLayout104.hyp[3].dn";
connectAttr "Tongue_A_Guide_Ctrl_Ctrl_Ctrl_CtrlShape.msg" "hyperLayout104.hyp[4].dn"
		;
connectAttr "Tongue_B_Guide.msg" "hyperLayout104.hyp[5].dn";
connectAttr "Tongue_B_Guide_CtrlShape.msg" "hyperLayout104.hyp[6].dn";
connectAttr "Tongue_B_Guide_Ctrl_CtrlShape.msg" "hyperLayout104.hyp[7].dn";
connectAttr "Tongue_B_Guide_Ctrl_Ctrl_CtrlShape.msg" "hyperLayout104.hyp[8].dn";
connectAttr "Tongue_B_Guide_Ctrl_Ctrl_Ctrl_CtrlShape.msg" "hyperLayout104.hyp[9].dn"
		;
connectAttr "Tongue_C_Guide.msg" "hyperLayout104.hyp[10].dn";
connectAttr "Tongue_C_Guide_CtrlShape.msg" "hyperLayout104.hyp[11].dn";
connectAttr "Tongue_C_Guide_Ctrl_CtrlShape.msg" "hyperLayout104.hyp[12].dn";
connectAttr "Tongue_C_Guide_Ctrl_Ctrl_CtrlShape.msg" "hyperLayout104.hyp[13].dn"
		;
connectAttr "Tongue_C_Guide_Ctrl_Ctrl_Ctrl_CtrlShape.msg" "hyperLayout104.hyp[14].dn"
		;
connectAttr "Tongue_D_Guide.msg" "hyperLayout104.hyp[15].dn";
connectAttr "Tongue_D_Guide_CtrlShape.msg" "hyperLayout104.hyp[16].dn";
connectAttr "Tongue_D_Guide_Ctrl_CtrlShape.msg" "hyperLayout104.hyp[17].dn";
connectAttr "Tongue_D_Guide_Ctrl_Ctrl_CtrlShape.msg" "hyperLayout104.hyp[18].dn"
		;
connectAttr "Tongue_D_Guide_Ctrl_Ctrl_Ctrl_CtrlShape.msg" "hyperLayout104.hyp[19].dn"
		;
connectAttr "CheekAutomations_Loc.msg" "hyperLayout89.hyp[0].dn";
connectAttr "CheekAutomations_LocShape.msg" "hyperLayout89.hyp[1].dn";
connectAttr "CheekPushZ_Loc.msg" "hyperLayout108.hyp[0].dn";
connectAttr "CheekPushZ_LocShape.msg" "hyperLayout108.hyp[1].dn";
connectAttr "FaceHierarchy_Loc.msg" "hyperLayout80.hyp[0].dn";
connectAttr "FaceHierarchy_LocShape.msg" "hyperLayout80.hyp[1].dn";
connectAttr "L_Brow_GuideShape.iog" ":initialShadingGroup.dsm" -na;
connectAttr "L_CheekBone_GuideShape.iog" ":initialShadingGroup.dsm" -na;
connectAttr "R_CheekBone_GuideShape.iog" ":initialShadingGroup.dsm" -na;
connectAttr "L_Orbicularis_GuideShape.iog" ":initialShadingGroup.dsm" -na;
connectAttr "R_Orbicularis_GuideShape.iog" ":initialShadingGroup.dsm" -na;
dataStructure -fmt "raw" -as "name=mapManager_grass_c_geo1:string=value";
dataStructure -fmt "raw" -as "name=notes_decayGrassPatchC_parShape:string=value";
dataStructure -fmt "raw" -as "name=f_3:float[3]=value";
dataStructure -fmt "raw" -as "name=DiffArea:float=value";
dataStructure -fmt "raw" -as "name=notes_pPlane1:string=value";
dataStructure -fmt "raw" -as "name=notes_baseScatt:string=value";
dataStructure -fmt "raw" -as "name=notes_slopesGroundGrassB_Combined:string=value";
dataStructure -fmt "raw" -as "name=mapManager_grass_c_geo:string=value";
dataStructure -fmt "raw" -as "name=mapManager_ground:string=value";
dataStructure -fmt "raw" -as "name=notes_grassJuneBackYard_parShape:string=value";
dataStructure -fmt "raw" -as "name=notes_bushes_parShape:string=value";
dataStructure -fmt "raw" -as "name=Blur3dMetaData:string=Blur3dValue";
dataStructure -fmt "raw" -as "name=notes_slopesGroundGrassD_Combined:string=value";
dataStructure -fmt "raw" -as "name=notes_slopes_parShape:string=value";
dataStructure -fmt "raw" -as "name=notes_wildPatchD_parShape:string=value";
dataStructure -fmt "raw" -as "name=notes_wildPatchA_parShape:string=value";
dataStructure -fmt "raw" -as "name=mapManager_pPlane4:string=value";
dataStructure -fmt "raw" -as "name=mapManager_pPlane5:string=value";
dataStructure -fmt "raw" -as "name=mapManager_juneBackYard:string=value";
dataStructure -fmt "raw" -as "name=mapManager_slopesMountainsGrass_Combined:string=value";
dataStructure -fmt "raw" -as "name=notes_mountains_parShape:string=value";
dataStructure -fmt "raw" -as "name=notes_snapshot_floor:string=value";
dataStructure -fmt "raw" -as "name=mapManager_groundWoods_c_geo1:string=value";
dataStructure -fmt "raw" -as "name=notes_wildPatchDegraded_parShape:string=value";
dataStructure -fmt "raw" -as "name=mapManager_baseScatter:string=value";
dataStructure -fmt "raw" -as "name=notes_right_parShape:string=value";
dataStructure -fmt "raw" -as "name=IdStruct:int32=ID";
dataStructure -fmt "raw" -as "name=notes_base_hojas:string=value";
dataStructure -fmt "raw" -as "name=notes_snapshot_CombinedGrass:string=value";
dataStructure -fmt "raw" -as "name=notes_pPlane4:string=value";
dataStructure -fmt "raw" -as "name=faceConnectMarkerStructure:bool=faceConnectMarker:string[200]=faceConnectOutputGroups";
dataStructure -fmt "raw" -as "name=mapManager_pPlane6:string=value";
dataStructure -fmt "raw" -as "name=notes_trees_parShape:string=value";
dataStructure -fmt "raw" -as "name=notes_widlPatchB_parShape:string=value";
dataStructure -fmt "raw" -as "name=OffStruct:float=Offset";
dataStructure -fmt "raw" -as "name=mapManager_slopesGroundGrassD_Combined:string=value";
dataStructure -fmt "raw" -as "name=f_1:float=value";
dataStructure -fmt "raw" -as "name=notes_pPlane2:string=value";
dataStructure -fmt "raw" -as "name=notes_snapshot_Combined:string=value";
dataStructure -fmt "raw" -as "name=notes_ferns_parShape:string=value";
dataStructure -fmt "raw" -as "name=notes_decayGrassPatchA_parShape:string=value";
dataStructure -fmt "raw" -as "name=mapManager_slopesGroundGrassC_Combined:string=value";
dataStructure -fmt "raw" -as "name=notes_wildPatchE_parShape:string=value";
dataStructure -fmt "raw" -as "name=mapManager_floorOrangeConcrete_c_geo:string=value";
dataStructure -fmt "raw" -as "name=notes_base_left:string=value";
dataStructure -fmt "raw" -as "name=Curvature:float=mean:float=gaussian:float=ABS:float=RMS";
dataStructure -fmt "raw" -as "name=notes_degraded:string=value";
dataStructure -fmt "raw" -as "name=Offset:float[3]=value";
dataStructure -fmt "raw" -as "name=notes_juneBackYard:string=value";
dataStructure -fmt "raw" -as "name=mapManager_base_right:string=value";
dataStructure -fmt "raw" -as "name=notes_wildPatchH_parShape:string=value";
dataStructure -fmt "raw" -as "name=notes_pPlane5:string=value";
dataStructure -fmt "raw" -as "name=mapManager_suelo:string=value";
dataStructure -fmt "raw" -as "name=notes_slopesGroundGrassA_Combined:string=value";
dataStructure -fmt "raw" -as "name=notes_grassBase:string=value";
dataStructure -fmt "raw" -as "name=mapManager_degraded:string=value";
dataStructure -fmt "raw" -as "name=notes_floorOrangeConcrete_c_geo:string=value";
dataStructure -fmt "raw" -as "name=notes_decayGrassPatchD_parShape:string=value";
dataStructure -fmt "raw" -as "name=mapManager_pPlane2:string=value";
dataStructure -fmt "raw" -as "name=mapManager_baseScatt:string=value";
dataStructure -fmt "raw" -as "name=notes_decayGrassPatchB_parShape:string=value";
dataStructure -fmt "raw" -as "name=notes_slopesMountainsGrass_Combined:string=value";
dataStructure -fmt "raw" -as "name=faceConnectOutputStructure:bool=faceConnectOutput:string[200]=faceConnectOutputAttributes:string[200]=faceConnectOutputGroups";
dataStructure -fmt "raw" -as "name=NameAndID:string=name:int32=ID";
dataStructure -fmt "raw" -as "name=mapManager_grassBase:string=value";
dataStructure -fmt "raw" -as "name=mapManager_snapshot_floor:string=value";
dataStructure -fmt "raw" -as "name=mapManager_baseLeaves:string=value";
dataStructure -fmt "raw" -as "name=OrgStruct:float[3]=Origin Point";
dataStructure -fmt "raw" -as "name=mapManager_pPlane1:string=value";
dataStructure -fmt "raw" -as "name=mapManager_slopesGroundGrassB_Combined:string=value";
dataStructure -fmt "raw" -as "name=mapManager_base_hojas:string=value";
dataStructure -fmt "raw" -as "name=notes_wildPatchC_parShape:string=value";
dataStructure -fmt "raw" -as "name=keyValueStructure:string=value";
dataStructure -fmt "raw" -as "name=mapManager_ground_c_geo:string=value";
dataStructure -fmt "raw" -as "name=notes_groundWoods_c_geo1:string=value";
dataStructure -fmt "raw" -as "name=notes_groundC_parShape:string=value";
dataStructure -fmt "raw" -as "name=mapManager_polySurface56:string=value";
dataStructure -fmt "raw" -as "name=mapManager_base_left:string=value";
dataStructure -fmt "raw" -as "name=notes_suelo:string=value";
dataStructure -fmt "raw" -as "name=mapManager_trees_left:string=value";
dataStructure -fmt "raw" -as "name=notes_grass_c_geo:string=value";
dataStructure -fmt "raw" -as "name=notes_pPlane3:string=value";
dataStructure -fmt "raw" -as "name=notes_groundB_parShape:string=value";
dataStructure -fmt "raw" -as "name=mapManager_trees_left1:string=value";
dataStructure -fmt "raw" -as "name=notes_decayLeaves_parShape:string=value";
dataStructure -fmt "raw" -as "name=notes_slopesGroundGrassC_Combined:string=value";
dataStructure -fmt "raw" -as "name=notes_base_right:string=value";
dataStructure -fmt "raw" -as "name=notes_baseLeaves:string=value";
dataStructure -fmt "raw" -as "name=notes_pPlane6:string=value";
dataStructure -fmt "raw" -as "name=notes_wildPatchG_parShape:string=value";
dataStructure -fmt "raw" -as "name=notes_groundA_parShape:string=value";
dataStructure -fmt "raw" -as "name=notes_decayGrassesCenter_parShape:string=value";
dataStructure -fmt "raw" -as "name=notes_baseScatter:string=value";
dataStructure -fmt "raw" -as "name=DiffEdge:float=value";
dataStructure -fmt "raw" -as "name=notes_decayLeavesCarousel_parShape:string=value";
dataStructure -fmt "raw" -as "name=notes_wildPatchF_parShape:string=value";
dataStructure -fmt "raw" -as "name=notes_grass_c_geo1:string=value";
dataStructure -fmt "raw" -as "name=notes_polySurface56:string=value";
dataStructure -fmt "raw" -as "name=mapManager_snapshot_Combined:string=value";
dataStructure -fmt "raw" -as "name=notes_ground_c_geo:string=value";
dataStructure -fmt "raw" -as "name=mapManager_pPlane3:string=value";
dataStructure -fmt "raw" -as "name=mapManager_snapshot_CombinedGrass:string=value";
dataStructure -fmt "raw" -as "name=notes_ground:string=value";
dataStructure -fmt "raw" -as "name=idStructure:int32=ID";
dataStructure -fmt "raw" -as "name=notes_left_parShape:string=value";
dataStructure -fmt "raw" -as "name=mapManager_slopesGroundGrassA_Combined:string=value";
dataStructure -fmt "raw" -as "name=notes_groundD_parShape:string=value";
dataStructure -fmt "raw" -as "name=notes_trees_left:string=value";
dataStructure -fmt "raw" -as "name=notes_trees_left1:string=value";
// End of HumanFaceGameReadyTemplate.ma
