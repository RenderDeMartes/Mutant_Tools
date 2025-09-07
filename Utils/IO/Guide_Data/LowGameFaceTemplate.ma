//Maya ASCII 2024 scene
//Name: LowGameFace.ma
//Last modified: Sun, Sep 07, 2025 11:04:14 AM
//Codeset: UTF-8
requires maya "2024";
requires "mtoa" "5.3.0";
requires "stereoCamera" "10.0";
currentUnit -l centimeter -a degree -t film;
fileInfo "application" "maya";
fileInfo "product" "Maya 2024";
fileInfo "version" "2024";
fileInfo "cutIdentifier" "202302170737-4500172811";
fileInfo "osv" "Mac OS X 15.6.1";
fileInfo "UUID" "EFC4188B-B240-D570-E010-A2A36E00C794";
createNode transform -n "Mutant_Build";
	rename -uid "EA88F421-724A-AA62-CC17-36B5D835C2A7";
createNode transform -n "init" -p "Mutant_Build";
	rename -uid "9B351D0B-1D45-F2D7-CD6B-2EAAF189EBF3";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/";
createNode dagContainer -n "BaseA_Block" -p "init";
	rename -uid "E6D40A9F-824B-6775-CE4D-CC9AC8CF2B12";
	addAttr -ci true -sn "nts" -ln "notes" -dt "string";
	setAttr ".isc" yes;
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/BaseA.png";
	setAttr ".ctor" -type "string" "esteban.rodriguez";
	setAttr ".cdat" -type "string" "2022/03/25 12:37:02";
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
	setAttr ".nts" -type "string" "['Mover_CtrlShape', 'Global_Ctrl', 'Mutant_Tools_Grp', 'Miscellaneous_Grp', 'Extra_Geo_Grp', 'Bind_Geo_Grp', 'Mover_Gimbal_Ctrl_tag', 'Template_Grp', 'Mover_Ctrl', 'Mover_Ctrl_tag', 'Rig_Ctrl_Grp', 'Mover_Gimbal_Ctrl', 'Mover_Gimbal_CtrlShape', 'Global_CtrlShape', 'Global_Ctrl_Offset_Grp', 'Mover_Ctrl_Offset_Grp', 'Rig_Grp', 'Bind_Joints_Grp', 'Ctrl_Grp']";
createNode dagContainer -n "VisAttrs_Block" -p "init";
	rename -uid "04EA4613-1444-F4AD-1540-04A320C2C59A";
	addAttr -ci true -sn "nts" -ln "notes" -dt "string";
	setAttr ".isc" yes;
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/CODE.png";
	setAttr ".ctor" -type "string" "esteban.rodriguez";
	setAttr ".cdat" -type "string" "2022/03/25 12:36:00";
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
	setAttr ".nts" -type "string" "['Vis_CtrlShape', 'Vis_Ctrl']";
createNode transform -n "Vis_Guide" -p "VisAttrs_Block";
	rename -uid "01C7005C-8E4A-FF38-2B6E-868DE1903B4B";
	addAttr -ci true -sn "naming" -ln "naming" -dt "string";
	addAttr -ci true -sn "anim_preset" -ln "anim_preset" -dt "string";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/";
	setAttr -k off -cb on ".v";
	setAttr ".t" -type "double3" 0 206.57086945533794 124.93169734859592 ;
	setAttr ".rp" -type "double3" 0 1.6093281918018576 0 ;
	setAttr ".sp" -type "double3" 0 1.6093281918018576 0 ;
	setAttr ".naming" -type "string" "{'side': '', 'base': 'cone', 'adjective': '', 'letter': '', 'number': '', 'position': '', 'node_type': 'ctrl', 'convention': 'default', }";
	setAttr ".anim_preset" -type "string" "{'display': ['v']}";
createNode nurbsCurve -n "Vis_GuideShape" -p "Vis_Guide";
	rename -uid "39AC7560-DE49-F835-1AA8-D9B26EF0A350";
	addAttr -ci true -sn "shape" -ln "shape" -dt "string";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 1;
	setAttr ".cc" -type "nurbsCurve" 
		1 16 0 no 3
		17 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16
		17
		0.67397383765980889 0.26138051648225513 1.1673563855186713
		-0.67397383765980889 0.26138051648225513 1.1673563855186713
		0 2.9572758671214849 0
		0.67397383765980889 0.26138051648225513 1.1673563855186713
		1.3479476753196178 0.26138051648225513 0
		0 2.9572758671214849 0
		0.67397383765980889 0.26138051648225513 -1.1673563855186713
		1.3479476753196178 0.26138051648225513 0
		0 2.9572758671214849 0
		-0.67397383765980889 0.26138051648225513 -1.1673577334663472
		0.67397383765980889 0.26138051648225513 -1.1673563855186713
		0 2.9572758671214849 0
		-1.3479476753196178 0.26138051648225513 -2.1412148822452118e-07
		-0.67397383765980889 0.26138051648225513 -1.1673577334663472
		0 2.9572758671214849 0
		-0.67397383765980889 0.26138051648225513 1.1673563855186713
		-1.3479476753196178 0.26138051648225513 -2.1412148822452118e-07
		;
	setAttr -k on ".shape" -type "string" "cone";
createNode dagContainer -n "FakeParentAndRoot_Block" -p "init";
	rename -uid "5B30CB24-FD4F-009D-C083-CD8B005EA610";
	addAttr -ci true -sn "nts" -ln "notes" -dt "string";
	setAttr ".isc" yes;
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/CODE.png";
	setAttr ".ctor" -type "string" "estebanrdgz";
	setAttr ".cdat" -type "string" "2025/09/04 21:22:26";
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
	setAttr ".nts" -type "string" "['Head_CtrlShape', 'Root_Bnd', 'Head_Ctrl']";
createNode transform -n "FakeParentAndRoot_Loc" -p "FakeParentAndRoot_Block";
	rename -uid "F944F68D-9644-01A7-2723-EE8B771247C5";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/";
createNode locator -n "FakeParentAndRoot_LocShape" -p "FakeParentAndRoot_Loc";
	rename -uid "D0DDAE1C-7D42-5133-1CCA-F68BFAFA10BA";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/";
	setAttr -k off ".v";
createNode transform -n "face" -p "Mutant_Build";
	rename -uid "6540C2C1-0A43-98B1-F419-51BA3F81C964";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/";
	setAttr ".t" -type "double3" 0 148.19816716577168 0 ;
createNode dagContainer -n "L_Brow_Block" -p "face";
	rename -uid "0BE5D0A8-3F41-4EBA-384A-5998722FC2CF";
	addAttr -ci true -sn "nts" -ln "notes" -dt "string";
	setAttr ".isc" yes;
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/Brows.png";
	setAttr ".ctor" -type "string" "estebanrdgz";
	setAttr ".cdat" -type "string" "2025/09/04 19:04:57";
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
		"['L_Brow_Driver2_Main_CtrlShape', 'L_Brow_Driver4_Main_Ctrl', 'L_Brow_2_Bnd', 'L_Brow_Driver2_Jnt', 'R_Brow_Driver2_Main_Ctrl_Offset_Grp', 'L_Brow_Driver0_Main_Ctrl', 'R_Brow_Driver1_yesRot_Loc_Offset_Grp', 'R_Brow_Main_Ctrl_Grp', 'R_Brow_Driver0_Jnt_Auto_Grp', 'R_Brow_Driver3_noRot_Loc_Offset_Grp', 'R_Brow_0_Loc_Offset_Grp', 'L_Brow_Driver3_Sec_Ctrl_Auto_Grp', 'R_Brow_4_CtrlShape', 'R_Brow_2_LocShape', 'R_Brow_Ctrl_Grp_scaleConstraint1', 'L_Brow_3_Bnd_scaleConstraint1', 'unitConversion15', 'L_Brow_2_Ctrl', 'R_Brow_Driver0_Jnt_Root_Grp', 'L_Brow_Driver4_Main_Ctrl_tag', 'L_Brow_2_Bnd_parentConstraint1', 'R_Brow_4_Loc_Offset_Grp', 'R_Brow_Driver2_Jnt_Auto_Grp', 'L_Brow_Ctrl_Offset_Grp', 'L_Brow_Driver3_yesRot_Loc_yesRot_PC', 'R_Brow_Fol_Grp', 'unitConversion12', 'L_Brow_UpVector_Loc_parentConstraint1', 'L_Brow_Driver3_Sec_Ctrl_Root_Grp', 'L_Brow_3_Bnd_parentConstraint1', 'L_Brow_0_Bnd_scaleConstraint1', 'R_Brow_Driver2_Main_Ctrl_tag', 'L_Brow_1_CtrlShape', 'L_Brow_DriverJnts_Grp', 'L_Brow_0_CtrlShape', 'R_Brow_Driver3_Jnt_Root_Grp', 'L_Brow_Rig_Grp_scaleConstraint1', 'R_Brow_Driver0_Main_CtrlShape', 'R_Brow_0_Bnd', 'R_Brow_Driver3_Sec_Ctrl_tag', 'R_Brow_3_CtrlShape', 'R_Brow_4_Ctrl_tag', 'L_Brow_Driver2_Main_Ctrl_tag', 'R_Brow_Driver2_Jnt_Root_Grp', 'R_Brow_0_Ctrl', 'L_Brow_1_Jnt_Offset_Grp', 'L_Brow_Rig_Grp', 'L_Brow_Driver4_Main_Ctrl_Offset_Grp', 'R_Brow_2_Jnt', 'R_Brow_0_Jnt_Offset_Grp', 'R_Brow_NurbFollicle3050', 'unitConversion9', 'L_Brow_NurbFollicleShape3050', 'unitConversion14', 'R_Brow_0_Ctrl_Offset_Grp', 'R_Brow_Driver1_Jnt_Root_Grp_PC', 'L_Brow_Driver0_Main_CtrlShape', 'L_Brow_2_Ctrl_Offset_Grp', 'R_Brow_CtrlShape', 'skinCluster1', 'L_Brow_4_Ctrl_tag', 'L_Brow_Ctrl', 'R_Brow_NurbFollicleShape6950', 'L_Brow_1_Ctrl_tag', 'L_Brow_Driver1_yesRot_Loc_yesRot_PC', 'R_Brow_Driver4_Jnt_Root_Grp', 'R_Brow_1_Ctrl_Offset_Grp', 'R_Brow_Rig_Grp_parentConstraint1', 'L_Brow_0_Ctrl_tag', 'L_Brow_4_Jnt', 'R_Brow_3_Ctrl_tag', 'R_Brow_NurbShape', 'L_Brow_0_Jnt_Offset_Grp', 'R_Brow_4_LocShape', 'skinCluster2GroupId', 'L_Brow_1_Bnd', 'L_Brow_2_Loc', 'R_Brow_3_LocShape', 'R_Brow_Driver1_yesRot_Loc', 'L_Brow_Nurb', 'R_Brow_Driver1_Sec_Ctrl_Auto_Grp', 'R_Brow_3_Jnt_parentConstraint1', 'R_Brow_Ctrl_Offset_Grp', 'L_Brow_Main_Ctrl_Grp', 'L_Brow_4_CtrlShape', 'R_Brow_Main_Jnt_Grp', 'L_Brow_Driver0_Jnt', 'L_Brow_Driver2_Jnt_Root_Grp', 'R_Brow_NurbFollicle5050', 'R_Brow_Tweeks_Ctrl_Grp', 'R_Brow_4_Jnt', 'L_Brow_4_Ctrl_Offset_Grp', 'L_Brow_Driver1_Sec_Ctrl_tag', 'L_Brow_Main_Jnt_Grp', 'R_Brow_3_Bnd_scaleConstraint1', 'R_Brow_Driver1_Sec_Ctrl_Root_Grp_PC', 'L_Brow_Driver2_Main_Ctrl', 'R_Brow_NurbFollicleShape5050', 'L_Brow_NurbFollicle5050', 'R_Brow_NurbFollicleShape3050', 'L_Brow_3_Loc_Offset_Grp', 'R_Brow_Driver4_Main_Ctrl', 'R_Brow_UpVector_LocShape', 'L_Brow_NurbFollicle1050', 'L_Brow_NurbFollicleShape5050', 'R_Brow_Rig_Grp', 'L_Brow_Driver1_yesRot_Loc', 'R_Brow_Driver1_Jnt_Auto_Grp', 'skinCluster1Set', 'R_Brow_3_Loc_Offset_Grp', 'L_Brow_Driver1_Jnt_Root_Grp', 'L_Brow_CtrlShape', 'L_Brow_Fol_Grp', 'R_Brow_Driver3_yesRot_Loc_yesRot_PC', 'L_Brow_Driver3_Jnt_Root_Grp', 'R_Brow_4_Ctrl', 'L_Brow_UpVector_LocShape', 'R_Brow_Driver1_Sec_Ctrl_tag', 'L_Brow_2_Ctrl_tag', 'R_Brow_1_Jnt', 'L_Brow_1_Loc', 'L_Brow_Driver1_Sec_Ctrl_Auto_Grp', 'R_Brow_Driver1_noRot_Loc_noRot_PC', 'R_Brow_Ctrl_Grp_parentConstraint1', 'L_Brow_2_Jnt_Offset_Grp', 'R_Brow_2_Ctrl', 'L_Brow_NurbFollicleShape8950', 'R_Brow_4_Ctrl_Offset_Grp', 'unitConversion13', 'R_Brow_2_Bnd_parentConstraint1', 'L_Brow_4_Bnd_scaleConstraint1', 'R_Brow_Driver1_yesRot_Loc_aimConstraint1', 'R_Brow_4_Jnt_parentConstraint1', 'L_Brow_Tweeks_Ctrl_Grp', 'L_Brow_Driver4_Jnt_Root_Grp', 'L_Brow_Driver4_Jnt', 'L_Brow_Driver3_noRot_Loc_Offset_Grp', 'R_Brow_Driver0_Main_Ctrl', 'L_Brow_Driver3_Sec_Ctrl_tag', 'L_Brow_Driver3_yesRot_LocShape', 'R_Brow_1_Bnd_scaleConstraint1', 'R_Brow_1_Jnt_parentConstraint1', 'L_Brow_Driver1_Jnt', 'L_Brow_1_Jnt_parentConstraint1', 'L_Brow_0_Ctrl', 'R_Brow_Ctrl_tag', 'R_Brow_Driver3_noRot_Loc', 'L_Brow_4_Jnt_Offset_Grp', 'skinCluster2GroupParts', 'unitConversion11', 'R_Brow_Driver1_Sec_Ctrl_Root_Grp', 'R_Brow_Driver1_noRot_LocShape', 'L_Brow_Driver2_Main_Ctrl_Offset_Grp', 'R_Brow_4_Bnd_parentConstraint1', 'R_Brow_0_Bnd_scaleConstraint1', 'R_Brow_3_Jnt', 'R_Brow_Driver1_Jnt', 'R_Brow_UpVector_Loc', 'L_Brow_Driver1_Sec_CtrlShape', 'L_Brow_Driver0_Main_Ctrl_Offset_Grp', 'R_Brow_Driver4_Main_Ctrl_tag', 'L_Brow_NurbFollicle8950', 'L_Brow_Driver1_Sec_Ctrl_Root_Grp_PC', 'L_Brow_3_Bnd', 'L_Brow_Driver1_yesRot_Loc_aimConstraint1', 'L_Brow_Driver3_Jnt', 'R_Brow_0_Loc', 'R_Brow_Driver1_Sec_CtrlShape', 'L_Brow_3_Ctrl_Offset_Grp', 'R_Brow_Driver3_Sec_Ctrl_Auto_Grp', 'R_Brow_3_Bnd_parentConstraint1', 'L_Brow_0_LocShape', 'L_Brow_0_Bnd_parentConstraint1', 'L_Brow_Driver3_noRot_Loc_noRot_PC', 'R_Brow_Driver1_Sec_Ctrl', 'unitConversion16', 'L_Brow_Driver1_yesRot_Loc_Offset_Grp', 'L_Brow_Driver1_Jnt_Root_Grp_PC', 'L_Brow_NurbFollicle3050', 'R_Brow_Driver4_Main_Ctrl_Offset_Grp', 'R_Brow_3_Loc', 'R_Brow_Driver3_noRot_Loc_noRot_PC', 'R_Brow_Driver3_noRot_LocShape', 'R_Brow_1_Bnd', 'L_Brow_Driver3_noRot_LocShape', 'R_Brow_UpVector_Loc_parentConstraint1', 'R_Brow_Nurb', 'L_Brow_0_Jnt', 'L_Brow_4_Jnt_parentConstraint1', 'R_Brow_4_Bnd_scaleConstraint1', 'L_Brow_3_Jnt_parentConstraint1', 'R_Brow_Ctrl', 'L_Brow_NurbShape', 'L_Brow_3_Ctrl_tag', 'R_Brow_Driver1_noRot_Loc_Offset_Grp', 'L_Brow_4_Bnd_parentConstraint1', 'R_Brow_NurbFollicle8950', 'L_Brow_Ctrl_Grp_scaleConstraint1', 'L_Brow_2_Jnt', 'R_Brow_NurbFollicle6950', 'skinCluster2', 'unitConversion10', 'L_Brow_Driver3_Sec_Ctrl_Root_Grp_PC', 'R_Brow_2_Ctrl_Offset_Grp', 'R_Brow_NurbFollicleShape8950', 'unitConversion6', 'L_Brow_Driver4_Jnt_Auto_Grp', 'L_Brow_3_Ctrl', 'R_Brow_Driver3_Jnt', 'R_Brow_0_Bnd_parentConstraint1', 'L_Brow_0_Jnt_parentConstraint1', 'R_Brow_Rig_Grp_scaleConstraint1', 'L_Brow_1_Bnd_parentConstraint1', 'R_Brow_SecRot_Loc_Grp', 'L_Brow_Driver3_Sec_CtrlShape', 'L_Brow_Driver3_Sec_Ctrl', 'L_Brow_Driver3_yesRot_Loc_Offset_Grp', 'R_Brow_Driver4_Jnt_Auto_Grp', 'R_Brow_Driver3_yesRot_LocShape', 'unitConversion5', 'unitConversion7', 'unitConversion4', 'L_Brow_OutterAutoRot_Blend10', 'L_Brow_Driver1_noRot_Loc_Offset_Grp', 'R_Brow_3_Jnt_Offset_Grp', 'R_Brow_NurbFollicle1050', 'R_Brow_Driver0_Main_Ctrl_Offset_Grp', 'unitConversion1', 'R_Brow_1_LocShape', 'R_Brow_0_LocShape', 'R_Brow_3_Ctrl', 'R_Brow_NurbFollicleShape1050', 'L_Brow_1_LocShape', 'L_Brow_NurbShapeOrig', 'unitConversion8', 'R_Brow_Driver3_Jnt_Auto_Grp', 'L_Brow_Driver1_yesRot_LocShape', 'L_Brow_Driver3_yesRot_Loc', 'L_Brow_UpVector_Loc', 'R_Brow_innerAutoRot_Blend10', 'R_Brow_Driver3_yesRot_Loc', 'R_Brow_Driver2_Jnt', 'L_Brow_Ctrl_Grp_parentConstraint1', 'R_Brow_Driver1_noRot_Loc', 'L_Brow_4_Loc_Offset_Grp', 'R_Brow_Driver3_Jnt_Root_Grp_PC', 'unitConversion2', 'R_Brow_1_Jnt_Offset_Grp', 'R_Brow_1_Loc_Offset_Grp', 'R_Brow_Driver4_Jnt', 'L_Brow_1_Ctrl', 'R_Brow_2_Ctrl_tag', 'L_Brow_1_Bnd_scaleConstraint1', 'L_Brow_3_LocShape', 'R_Brow_2_Jnt_parentConstraint1', 'skinCluster1GroupParts', 'skinCluster2Set', 'R_Brow_2_Loc_Offset_Grp', 'R_Brow_NurbShapeOrig', 'L_Brow_Driver1_noRot_Loc', 'R_Brow_OutterAutoRot_Blend10', 'R_Brow_DriverJnts_Grp', 'R_Brow_Driver0_Main_Ctrl_tag', 'L_Brow_Driver3_yesRot_Loc_aimConstraint1', 'R_Brow_2_Bnd_scaleConstraint1', 'skinCluster1GroupId', 'R_Brow_4_Loc', 'L_Brow_Driver4_Main_CtrlShape', 'R_Brow_1_Bnd_parentConstraint1', 'R_Brow_Driver3_Sec_Ctrl_Root_Grp', 'R_Brow_Driver3_yesRot_Loc_Offset_Grp', 'R_Brow_Driver2_Main_CtrlShape', 'L_Brow_2_Jnt_parentConstraint1', 'R_Brow_TweekJnts_Grp', 'R_Brow_3_Ctrl_Offset_Grp', 'R_Brow_3_Bnd', 'L_Brow_2_Bnd_scaleConstraint1', 'L_Brow_1_Jnt', 'R_Brow_2_Bnd', 'L_Brow_1_Ctrl_Offset_Grp', 'L_Brow_2_LocShape', 'R_Brow_Ctrl_GrpMirror_Grp', 'R_Brow_Driver3_Sec_CtrlShape', 'L_Brow_4_Ctrl', 'R_Brow_0_Ctrl_tag', 'L_Brow_Ctrl_tag', 'R_Brow_Driver1_Jnt_Root_Grp', 'L_Brow_Driver3_noRot_Loc', 'R_Brow_1_Loc', 'L_Brow_Driver0_Jnt_Auto_Grp', 'L_Brow_Driver1_Sec_Ctrl_Root_Grp', 'L_Brow_0_Loc', 'L_Brow_4_Loc', 'L_Brow_Driver2_Jnt_Auto_Grp', 'L_Brow_3_Jnt', 'L_Brow_3_CtrlShape', 'L_Brow_NurbFollicle6950', 'R_Brow_Driver4_Main_CtrlShape', 'L_Brow_Driver3_Jnt_Root_Grp_PC', 'R_Brow_2_Loc', 'R_Brow_1_Ctrl', 'R_Brow_Driver1_yesRot_LocShape', 'L_Brow_TweekJnts_Grp', 'L_Brow_SecRot_Loc_Grp', 'L_Brow_Rig_Grp_parentConstraint1', 'L_Brow_Ctrl_Grp', 'R_Brow_Driver2_Main_Ctrl', 'L_Brow_NurbFollicleShape6950', 'R_Brow_2_CtrlShape', 'L_Brow_Driver1_noRot_Loc_noRot_PC', 'L_Brow_Driver1_Sec_Ctrl', 'bindPose1', 'L_Brow_4_LocShape', 'L_Brow_1_Loc_Offset_Grp', 'L_Brow_NurbFollicleShape1050', 'L_Brow_innerAutoRot_Blend10', 'R_Brow_Driver3_Sec_Ctrl', 'R_Brow_1_CtrlShape', 'L_Brow_2_Loc_Offset_Grp', 'L_Brow_3_Jnt_Offset_Grp', 'R_Brow_Driver3_Sec_Ctrl_Root_Grp_PC', 'L_Brow_Driver1_Jnt_Auto_Grp', 'R_Brow_4_Bnd', 'R_Brow_Ctrl_Grp', 'L_Brow_Driver0_Jnt_Root_Grp', 'R_Brow_Driver0_Jnt', 'R_Brow_Driver1_yesRot_Loc_yesRot_PC', 'L_Brow_0_Bnd', 'unitConversion3', 'R_Brow_0_CtrlShape', 'R_Brow_0_Jnt_parentConstraint1', 'L_Brow_0_Loc_Offset_Grp', 'L_Brow_2_CtrlShape', 'R_Brow_Rig_GrpMirror_Grp', 'L_Brow_Driver0_Main_Ctrl_tag', 'L_Brow_Driver1_noRot_LocShape', 'L_Brow_Driver3_Jnt_Auto_Grp', 'R_Brow_0_Jnt', 'L_Brow_0_Ctrl_Offset_Grp', 'R_Brow_1_Ctrl_tag', 'R_Brow_Driver3_yesRot_Loc_aimConstraint1', 'R_Brow_4_Jnt_Offset_Grp', 'L_Brow_4_Bnd', 'L_Brow_3_Loc', 'R_Brow_2_Jnt_Offset_Grp', 'bindPose2']");
createNode transform -n "L_Brow_Guide" -p "L_Brow_Block";
	rename -uid "27191AA3-DD4B-F89A-0398-A5BC6E7FE911";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/";
	setAttr ".t" -type "double3" 22.36043372445889 32.421867587877472 144.27355983741583 ;
	setAttr ".r" -type "double3" 1.1861357135917552 6.2461083336079311 -1.2574895013137439 ;
	setAttr ".s" -type "double3" 0.69147977336066024 0.69147977336066024 0.69147977336066024 ;
createNode nurbsSurface -n "L_Brow_GuideShape" -p "L_Brow_Guide";
	rename -uid "620277D5-014F-745D-23E1-B9B2BADACC48";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/";
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
		-8.4758317286852041 -4.0515295859955769 3.0901706723928091
		-8.6616799215722686 -2.8088020654313284 3.5448714607314344
		-8.8475281144593385 -1.5660745448670803 3.9995722490700603
		-9.0333763073464013 -0.32334702430283535 4.454273037408683
		-7.5054720472242336 -3.6113535775034746 2.2837519113103175
		-7.6913202401112999 -2.3686260569392266 2.7384526996489438
		-7.8771684329983662 -1.1258985363749785 3.1931534879875692
		-8.0630166258854299 0.11682898418926516 3.6478542763261927
		-5.5102813749398303 -2.7092259585618117 0.9063433973327113
		-5.680101147753569 -1.4520379270612136 1.2778359387309657
		-5.8498406363122895 -0.19475325600125831 1.5969673595783354
		-6.0195010514407228 1.0626283257885365 1.9526477480516093
		-2.5714438898517935 -1.5084292325044841 -0.85134968902657226
		-2.3875505518331384 -0.2276345767265171 -0.73096964817478061
		-2.1940734079865876 1.0544533936967933 -0.8125939685552408
		-1.9795593259917277 2.3321405350147724 -0.95117238152117634
		1.2527246577847206 -3.0723908456551836 -3.5249835834138361
		2.0109903898900132 -2.0103709906443239 -3.5494684199461073
		2.810752818636943 -0.99233615286831145 -3.7363980835796236
		3.6123504942486941 0.032176196262314959 -3.9874745132869918
		4.3132823990541027 -6.9379834317690596 -6.8117191761495519
		5.3509671924853137 -6.096036689056346 -6.8191118815536349
		6.3886519859165229 -5.2540899463436341 -6.8244272713136658
		7.4263382525905559 -4.4121482396757132 -6.8244289388352026
		5.6567436362635846 -9.2098006131645835 -8.2852222685687842
		6.7511740226623589 -8.4430632543447874 -8.2852222685687842
		7.845604409061127 -7.6763258955249976 -8.2852222685687842
		8.9400347954598978 -6.9095885367052068 -8.2852222685687842
		6.3307735662710787 -10.171901687615831 -8.922175346963698
		7.4252039526698494 -9.4051643287960385 -8.922175346963698
		8.5196343390686202 -8.6384269699762459 -8.922175346963698
		9.6140647254673901 -7.8716896111564569 -8.922175346963698
		
		;
	setAttr ".nufa" 4.5;
	setAttr ".nvfa" 4.5;
createNode dagContainer -n "L_Eyelids_Block" -p "face";
	rename -uid "DF0B6FE9-4340-6AE5-0F06-48B9262DD026";
	addAttr -ci true -sn "nts" -ln "notes" -dt "string";
	setAttr ".isc" yes;
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/Eyes.png";
	setAttr ".ctor" -type "string" "estebanrdgz";
	setAttr ".cdat" -type "string" "2025/09/04 19:05:15";
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
		"['L_Eyelids_Blink_CrvBaseWire1ShapeOrig', 'R_Eyelids_Dw_2_Loc', 'L_Eyelids_UpEndMid_Jnt_Offset_Grp', 'R_Eyelids_Dw_7_Ctrl_OffsetPivot_Grp', 'L_Eyelids_Dw_Origin_5_Jnt_aimConstraint1', 'R_Eyelids_UpStart_Jnt', 'L_Eyelids_UpEndMid_Jnt', 'L_Eyelids_Up_Wire', 'L_Eyelids_Up_WireDriver_CrvShapeOrig1', 'R_Eyelids_Up_6_Jnt', 'L_Eyelids_DwMid_Ctrl', 'R_Eyelids_Up_4_LocShape', 'R_Eyelids_EyePivot_Loc', 'R_Eyelids_Dw_VtxJnts_Grp', 'L_Eyelids_UpEndMid_Ctrl', 'R_Eyelids_Rig_Grp_scaleConstraint1', 'R_Eyelids_Dw__cv3_Bnd', 'L_Eyelids_Dw_Scale_CtrlShape', 'R_Eyelids_Up_0_LocShape', 'L_Eyelids_Up_BlinkTarget_CrvShape', 'R_Eyelids_Up_3_Loc', 'R_Eyelids_Up_Origin_2_Jnt_Offset_Grp', 'R_Eyelids_Up_Origin_0_Jnt', 'L_Eyelids_Dw_2_Loc', 'L_Eyelids_Dw_Origin_6_Jnt', 'R_Eyelids_Dw_5_Ctrl_tag', 'R_Eyelids_LwrBlink_BSSet', 'R_Eyelids_Up_0_Ctrl', 'R_Eyelids_BlinkAttrs_CtrlShape', 'L_EyelidsLwrBlink_CtrlShape', 'unitConversion24', 'L_Eyelids_Dw_WireGroupId', 'R_Eyelids_Up_8_Ctrl_OffsetPivot_Grp', 'L_Eyelids_DwStartMid_Ctrl_tag', 'L_Eyelids_DwMid_CtrlShape', 'R_Eyelids_Up_5_CtrlShape', 'L_Eyelids_Dw_0_Jnt_Offset_Grp', 'R_Eyelids_BlinkAttrs_Ctrl', 'L_Eyelids_DwEnd_Ctrl_tag', 'L_Eyelids_Up_8_Ctrl_Offset_Grp', 'L_Eyelids_Up_Origin_7_Jnt', 'L_Eyelids_Up_Vtx_Crv', 'R_Eyelids_Up_0_Jnt_Offset_Grp', 'L_Eyelids_Dw_Scale_Ctrl_Offset_Grp', 'R_Eyelids_UpMid_Ctrl_tag', 'R_Eyelids_Ctrl_GrpMirror_Grp', 'L_Eyelids_Up_WireSet', 'L_Eyelids_Dw_5_Jnt', 'R_Eyelids_DwEndMid_Jnt', 'L_Eyelids_Up_0_Loc', 'skinCluster6', 'R_Eyelids_Up_AimLocators_Grp', 'L_Eyelids_Dw_7_Jnt', 'L_Eyelids_Up_0_Ctrl_Offset_Grp', 'R_Eyelids_Up_Vtx_Crv', 'L_Eyelids_Dw_Scale_Ctrl', 'R_Eyelids_Dw_2_Ctrl_OffsetPivot_Grp', 'L_Eyelids_Up_5_Ctrl', 'L_Eyelids_Blink_BSGroupId', 'R_Eyelids_Up_2_Ctrl_OffsetPivot_Grp', 'R_Eyelids_Up_WireDriver_Crv', 'L_Eyelids_Dw_5_Ctrl', 'L_Eyelids_Dw_4_CtrlShape', 'R_Eyelids_Up_5_POCI', 'L_Eyelids_Dw_Origin_4_Jnt_Offset_Grp', 'R_Eyelids_Dw_7_Loc', 'L_Eyelids_Dw_5_POCI', 'R_Eyelids_UpEndMid_Ctrl_Offset_Grp_parentConstraint1', 'L_Eyelids_DwStartMid_Jnt', 'L_Eyelids_LwrBlink_BSGroupParts', 'R_Eyelids_Dw_Origin_4_Jnt_aimConstraint1', 'L_Eyelids_Scale_Grp', 'L_Eyelids_Dw_WireDriver_CrvBaseWireShape', 'R_Eyelids_Up_5_Loc', 'L_Eyelids_Up_7_Ctrl_OffsetPivot_Grp_Offset_Grp', 'L_Eyelids_Up_Origin_0_Jnt_aimConstraint1', 'L_Eyelids_Dw_WireSet', 'R_Eyelids_Up_Scale_Grp_Offset_Grp', 'R_Eyelids_Dw_1_Ctrl_Offset_Grp', 'L_Eyelids_Dw_6_Ctrl_Offset_Grp', 'L_Eyelids_DwStartMid_Ctrl_Offset_Grp', 'L_Eyelids_UprBlink_BSGroupId', 'L_Eyelids_Up_4_Ctrl_OffsetPivot_Grp_Offset_Grp', 'R_Eyelids_Up_Origin_1_Jnt_aimConstraint1', 'L_Eyelids_Dw_4_Loc', 'L_Eyelids_Up_Origin_5_Jnt_Offset_Grp', 'R_Eyelids_DwMid_Jnt', 'L_Eyelids_UpMid_Jnt', 'R_Eyelids_Up_6_Ctrl_OffsetPivot_Grp', 'R_Eyelids_Up_WireDriver_CrvBaseWireShapeOrig', 'L_Eyelids_Dw_4_Ctrl_tag', 'R_Eyelids_Dw_6_POCI', 'R_Eyelids_UpStartMid_Ctrl_Offset_Grp', 'L_Eyelids_EyePivot_Loc', 'R_Eyelids_Dw_1_LocShape', 'R_Eyelids_UpWireGroupId', 'R_Eyelids_Dw_3_CtrlShape', 'R_Eyelids_DwMid_Jnt_Offset_Grp', 'R_Eyelids_Blink_CrvShapeOrig1', 'R_Eyelids_DwWireSet', 'L_Eyelids_Up_6_Ctrl_Offset_Grp', 'L_Eyelids_Dw_Origin_7_Jnt_aimConstraint1', 'skinCluster5GroupParts', 'R_Eyelids_Dw_6_CtrlShape', 'R_Eyelids_Dw_WireDriver_CrvBaseWire', 'L_Eyelids_Up_6_Jnt_Offset_Grp', 'L_Eyelids_Dw_1_CtrlShape', 'R_Eyelids_Dw_4_Ctrl', 'R_Eyelids_Dw_3_Jnt', 'R_Eyelids_Up_1_Ctrl', 'R_Eyelids_Blink_CrvBaseWire', 'L_Eyelids_Dw_Wire', 'R_Eyelids_Dw_3_Ctrl', 'L_Eyelids_Dw_3_Ctrl_OffsetPivot_Grp_Offset_Grp', 'R_Eyelids_UprBlink_BSSet', 'hyperLayout56', 'L_Eyelids_Up_Origin_1_Jnt_aimConstraint1', 'R_Eyelids_Up_Scale_CtrlShape', 'L_Eyelids_DwStartMid_Jnt_Offset_Grp', 'L_Eyelids_UpMid_Ctrl', 'L_Eyelids_Up_Jnt_Grp', 'L_Eyelids_Dw_3_POCI', 'R_Eyelids_Up_WireDriver_CrvShape', 'skinCluster5GroupId', 'R_Eyelids_Up_Jnt_Grp', 'R_Eyelids_Up_8_Ctrl_Offset_Grp', 'skinCluster6Set', 'R_Eyelids_Scale_Ctrl_Offset_Grp', 'L_Eyelids_Up_BlinkTarget_CrvShapeOrig', 'L_Eyelids_Up_6_Ctrl_OffsetPivot_Grp', 'L_Eyelids_UpMid_Jnt_Offset_Grp', 'L_Eyelids_Up_3_Ctrl', 'L_Eyelids_Dw_4_Jnt_Offset_Grp', 'L_Eyelids_Dw_2_Ctrl_tag', 'L_Eyelids_DwStart_Ctrl_tag', 'R_Eyelids_Dw_4_POCI', 'L_Eyelids_Dw_2_Ctrl_Offset_Grp', 'R_Eyelids_Dw_Wire', 'L_Eyelids_Up_1_Ctrl_tag', 'UprBlink_MultDiv1', 'R_Eyelids_Scale_CtrlShape', 'R_EyelidsLwrBlink_Ctrl_Offset_Grp', 'L_Eyelids_DwStart_CtrlShape', 'R_Eyelids_Up_Origin_8_Jnt_Offset_Grp', 'L_Eyelids_UpStartMid_Ctrl_Offset_Grp', 'L_Eyelids_Up_4_LocShape', 'L_Eyelids_Up_2_Ctrl_tag', 'R_Eyelids_Dw_Origin_3_Jnt_aimConstraint1', 'R_Eyelids_Dw_6_Ctrl_OffsetPivot_Grp', 'unitConversion23', 'L_Eyelids_DwStart_Ctrl_Offset_Grp', 'R_Eyelids_Up_6_POCI', 'L_Eyelids_UpMid_Ctrl_tag', 'R_Eyelids_Up_4_Ctrl_Offset_Grp', 'L_Eyelids_Up_Scale_Grp_Offset_Grp', 'L_Eyelids_Blink_CrvBaseWire1ShapeOrig1', 'R_Eyelids_UpEnd_Jnt', 'R_Eyelids_Up_3_POCI', 'R_Eyelids_Dw_WireGroupParts', 'R_Eyelids_Dw_Origin_1_Jnt_aimConstraint1', 'R_Eyelids_Dw_4_Ctrl_tag', 'R_Eyelids_Dw_Origin_4_Jnt', 'L_Eyelids_Up_0_Jnt', 'L_Eyelids_Up_Origin_1_Jnt_Offset_Grp', 'L_Eyelids_Dw_Origin_1_Jnt', 'R_Eyelids_DwStart_Jnt_Offset_Grp', 'L_Eyelids_UpWireGroupParts', 'R_Eyelids_Up_7_CtrlShape', 'L_Eyelids_Up_8_Loc', 'L_Eyelids_Up__cv3_Bnd', 'R_Eyelids_Up_8_Jnt_Offset_Grp', 'L_Eyelids_UpWireSet', 'LwrBlink_MultDiv', 'R_Eyelids_Dw_2_POCI', 'R_Eyelids_Blink_CrvBaseWireShape', 'L_Eyelids_Scale_CtrlShape', 'R_Eyelids_Blink_CrvBaseWireShapeOrig', 'R_Eyelids_Scale_Grp', 'R_Eyelids_Up_4_Ctrl_tag', 'L_Eyelids_UpStart_Jnt', 'R_Eyelids_Up_0_Ctrl_OffsetPivot_Grp_Offset_Grp', 'L_Eyelids_Dw_7_POCI', 'L_Eyelids_Dw_5_Ctrl_Offset_Grp', 'R_Eyelids_Blink_Reverse', 'L_Eyelids_Up_WireDriver_CrvShape', 'R_Eyelids_DwEndMid_Ctrl_tag', 'L_Eyelids_Dw_2_Jnt', 'R_Eyelids_Up_3_CtrlShape', 'L_Eyelids_Up_Scale_Ctrl_Offset_Grp', 'R_Eyelids_UpVector_Loc', 'R_Eyelids_Up_WireDriver_CrvBaseWire', 'L_Eyelids_DwMid_Jnt', 'L_Eyelids_Dw_4_POCI', 'L_Eyelids_Dw_Origin_0_Jnt_Offset_Grp', 'L_Eyelids_Up_1_Ctrl_OffsetPivot_Grp_Offset_Grp', 'L_Eyelids_Dw_0_Ctrl_Offset_Grp', 'L_Eyelids_Dw_1_LocShape', 'L_EyelidsLwrBlink_Ctrl_tag', 'L_Eyelids_Blink_Crv', 'R_Eyelids_UpVector_LocShape', 'L_Eyelids_Dw__cv3_Bnd_parentConstraint1', 'unitConversion19', 'L_Eyelids_Dw_5_Ctrl_tag', 'L_Eyelids_UpWire', 'R_Eyelids_UpStartMid_CtrlShape', 'L_Eyelids_Dw_Origin_1_Jnt_aimConstraint1', 'R_Eyelids_Blink_CrvShapeOrig', 'R_Eyelids_Dw_6_LocShape', 'R_Eyelids_Up_Scale_Ctrl', 'L_Eyelids_Dw_Origin_2_Jnt_aimConstraint1', 'L_Eyelids_Dw_3_CtrlShape', 'skinCluster4Set', 'R_Eyelids_Dw_Scale_Ctrl_tag', 'L_Eyelids_Up_Origin_2_Jnt', 'R_Eyelids_Up_Origin_2_Jnt', 'R_Eyelids_Dw_WireSet', 'L_Eyelids_Dw_3_Ctrl_Offset_Grp', 'R_Eyelids_Up_4_POCI', 'L_Eyelids_Up_8_POCI', 'L_Eyelids_UpStart_Ctrl_tag', 'R_Eyelids_Up_8_LocShape', 'L_Eyelids_DwEnd_CtrlShape', 'R_Eyelids_Up_Origin_4_Jnt_Offset_Grp', 'L_Eyelids_Dw_2_Jnt_Offset_Grp', 'L_Eyelids_Up_2_Jnt', 'R_Eyelids_Up_1_Loc', 'L_Eyelids_Up_3_POCI', 'R_Eyelids_Up_Origin_5_Jnt', 'L_Eyelids_Up_0_POCI', 'R_Eyelids_UpEnd_Ctrl', 'R_Eyelids_Dw_1_Loc', 'L_Eyelids_Up_5_Ctrl_Offset_Grp', 'L_Eyelids_DwEnd_Jnt', 'R_Eyelids_Dw_BlinkTarget_CrvShapeOrig1', 'L_Eyelids_Dw_7_Ctrl_OffsetPivot_Grp', 'L_Eyelids_Dw_0_Ctrl_OffsetPivot_Grp_Offset_Grp', 'R_Eyelids_DwMid_Ctrl', 'L_Eyelids_Dw_6_POCI', 'L_Eyelids_UpEndMid_Ctrl_Offset_Grp_parentConstraint1', 'R_Eyelids_DwEndMid_Ctrl', 'R_Eyelids_Dw_Origin_5_Jnt_Offset_Grp', 'R_Eyelids_DwEndMid_CtrlShape', 'L_Eyelids_Dw_3_Ctrl_tag', 'R_Eyelids_Dw_Scale_Grp', 'L_Eyelids_Scale_Grp_Offset_Grp', 'L_Eyelids_Dw_Vtx_CrvShapeOrig', 'L_EyelidsUprBlink_Ctrl_tag', 'L_Eyelids_Up_4_Jnt_Offset_Grp', 'L_Eyelids_Dw_Tweeks_Ctrl_Grp', 'R_EyelidsUprBlink_Ctrl', 'R_Eyelids_Rig_Grp', 'R_Eyelids_Dw_Ctrl_Grp', 'R_Eyelids_Up_Origin_6_Jnt', 'L_Eyelids_Dw_BlinkTarget_CrvShape', 'R_Eyelids_Dw_Scale_Ctrl_Offset_Grp', 'R_Eyelids_UpMid_CtrlShape', 'L_Eyelids_Up_7_Ctrl_Offset_Grp', 'L_Eyelids_Dw_WireDriver_CrvShapeOrig1', 'R_Eyelids_Up_3_LocShape', 'L_Eyelids_Dw_6_LocShape', 'L_Eyelids_Up_2_Ctrl', 'L_Eyelids_DwEndMid_Ctrl', 'L_Eyelids_EyePivot_LocShape', 'R_Eyelids_Dw_Origin_7_Jnt', 'R_Eyelids_Up_WireSet', 'R_Eyelids_Dw_3_LocShape', 'R_Eyelids_Up_Origin_8_Jnt_aimConstraint1', 'R_Eyelids_DwStartMid_Ctrl_Offset_Grp_parentConstraint1', 'L_EyelidsLwrBlink_Ctrl', 'R_Eyelids_Up_Origin_8_Jnt', 'L_Eyelids_Up_0_CtrlShape', 'L_Eyelids_Dw_4_Ctrl_Offset_Grp', 'L_Eyelids_Dw_WireDriver_CrvShape', 'R_Eyelids_Blink_CrvBaseWire1ShapeOrig1', 'L_Eyelids_DwEnd_Ctrl', 'R_EyelidsLwrBlink_Ctrl_tag', 'L_Eyelids_Dw_1_Ctrl_OffsetPivot_Grp_Offset_Grp', 'R_Eyelids_Dw_Origin_1_Jnt_Offset_Grp', 'R_Eyelids_UprBlink_BS', 'L_Eyelids_Dw_3_LocShape', 'R_Eyelids_Up_8_Ctrl_OffsetPivot_Grp_Offset_Grp', 'L_Eyelids_DwEndMid_CtrlShape', 'L_Eyelids_Blink_CrvBaseWire1ShapeOrig2', 'R_Eyelids_Up_5_Jnt_Offset_Grp', 'L_Eyelids_DwStartMid_Ctrl_Offset_Grp_parentConstraint1', 'L_Eyelids_Dw_Origin_4_Jnt_aimConstraint1', 'L_Eyelids_Dw_Origin_6_Jnt_Offset_Grp', 'R_Eyelids_Up_Origin_6_Jnt_aimConstraint1', 'Mutant_Rig', 'UprBlink_MultDiv', 'R_Eyelids_Scale_Ctrl', 'L_Eyelids_UpEnd_Jnt', 'L_Eyelids_BlinkAttrs_CtrlShape', 'L_Eyelids_Up_7_Jnt', 'L_Eyelids_Up_6_LocShape', 'R_Eyelids_Up_Origin_7_Jnt_aimConstraint1', 'R_Eyelids_EyePivot_LocShape', 'L_Eyelids_Up_3_Jnt_Offset_Grp', 'L_Eyelids_UpEnd_Ctrl_Offset_Grp', 'L_Eyelids_Blink_CrvShapeOrig', 'R_Eyelids_Dw_6_Ctrl', 'L_Eyelids_Up_0_Ctrl_OffsetPivot_Grp', 'R_Eyelids_Dw_5_POCI', 'R_Eyelids_Up_7_Ctrl_tag', 'L_Eyelids_Dw_0_Ctrl', 'L_Eyelids_Up_8_Ctrl_OffsetPivot_Grp_Offset_Grp', 'R_Eyelids_DwMid_Ctrl_tag', 'R_Eyelids_Dw_Origin_2_Jnt_Offset_Grp', 'R_Eyelids_Dw__cv3_Bnd_parentConstraint1', 'L_Eyelids_Up_2_Loc', 'unitConversion22', 'R_Eyelids_Blink_CrvShapeOrig2', 'R_Eyelids_Dw_6_Loc', 'L_Eyelids_UpEnd_Ctrl_tag', 'R_Eyelids_Up_2_Ctrl', 'R_Eyelids_DwEnd_CtrlShape', 'L_Eyelids_DwStartMid_Ctrl', 'R_Eyelids_Up__cv3_Bnd_parentConstraint1', 'R_Eyelids_Up_1_Jnt', 'L_EyelidsUprBlink_Ctrl_Offset_Grp', 'L_Eyelids_Blink_CrvBaseWireShapeOrig1', 'L_Eyelids_Dw_Origin_5_Jnt_Offset_Grp', 'skinCluster5', 'skinCluster4GroupId', 'R_Eyelids_Up_2_LocShape', 'L_Eyelids_Up_4_POCI', 'L_Eyelids_Scale_Ctrl', 'R_Eyelids_Dw_0_Ctrl_OffsetPivot_Grp', 'skinCluster5Set', 'R_Eyelids_Up_1_Ctrl_OffsetPivot_Grp', 'R_Eyelids_Dw_1_Ctrl_OffsetPivot_Grp', 'R_Eyelids_Up_4_CtrlShape', 'L_Eyelids_Dw_Scale_Grp_Offset_Grp', 'L_Eyelids_Up_6_Ctrl_OffsetPivot_Grp_Offset_Grp', 'L_Eyelids_Up_Origin_4_Jnt_Offset_Grp', 'R_Eyelids_Up_WireGroupId', 'L_Eyelids_Up_4_Ctrl_Offset_Grp', 'R_Eyelids_Up_6_Ctrl_Offset_Grp', 'R_Eyelids_Up_7_LocShape', 'R_Eyelids_Up_6_CtrlShape', 'R_Eyelids_UpMid_Jnt', 'L_Eyelids_Dw_6_Jnt', 'L_Eyelids_UpEndMid_Jnt_Offset_Grp_parentConstraint1', 'R_Eyelids_Up_BlinkTarget_CrvShape', 'R_Eyelids_DwWireGroupParts', 'R_Eyelids_Up_1_Ctrl_tag', 'R_Eyelids_Up_1_LocShape', 'L_Eyelids_Up_Scale_Grp', 'L_Eyelids_Dw_4_Jnt', 'L_Eyelids_UpStartMid_CtrlShape', 'L_Eyelids_Dw_0_LocShape', 'L_Eyelids_Up_6_CtrlShape', 'L_Eyelids_Up_2_POCI', 'L_Eyelids_Up_4_Jnt', 'R_Eyelids_Up_6_Ctrl_OffsetPivot_Grp_Offset_Grp', 'L_Eyelids_Ctrl_Grp_parentConstraint1', 'L_Eyelids_Up_5_Jnt', 'R_Eyelids_DwStart_CtrlShape', 'L_Eyelids_Dw_BlinkTarget_CrvShapeOrig1', 'R_Eyelids_Dw_Origin_0_Jnt_aimConstraint1', 'L_Eyelids_Dw_0_POCI', 'L_Eyelids_UpStartMid_Jnt_Offset_Grp', 'L_Eyelids_LwrBlink_BS', 'L_Eyelids_Up_Origin_8_Jnt_aimConstraint1', 'R_Eyelids_Dw_7_LocShape', 'R_Eyelids_UpWire', 'L_Eyelids_UpStartMid_Jnt', 'L_Eyelids_Up_Origin_6_Jnt_aimConstraint1', 'L_Eyelids_Dw_Vtx_CrvShape', 'L_Eyelids_DwMid_Ctrl_Offset_Grp', 'R_Eyelids_Up_7_Ctrl_OffsetPivot_Grp', 'R_Eyelids_Dw_1_Jnt_Offset_Grp', 'R_Eyelids_Dw_6_Ctrl_tag', 'R_Eyelids_Dw_0_Ctrl_Offset_Grp', 'L_Eyelids_Dw_WireDriver_CrvBaseWire', 'L_Eyelids_Dw_BlinkTarget_Crv', 'R_Eyelids_Up_1_Jnt_Offset_Grp', 'R_Eyelids_Up_Scale_Ctrl_tag', 'R_Eyelids_Dw_3_Ctrl_OffsetPivot_Grp_Offset_Grp', 'R_Eyelids_DwEnd_Ctrl_tag', 'R_Eyelids_Up_6_Ctrl_tag', 'L_Eyelids_Dw_7_CtrlShape', 'R_Eyelids_Dw_Origin_1_Jnt', 'L_Eyelids_Dw_3_Loc', 'L_Eyelids_Dw_6_Ctrl_OffsetPivot_Grp', 'L_Eyelids_Dw_1_Ctrl_Offset_Grp', 'L_Eyelids_Dw_WireDriver_CrvShapeOrig', 'R_EyelidsUprBlink_CtrlShape', 'R_Eyelids_UpStartMid_Jnt_Offset_Grp_parentConstraint1', 'R_Eyelids_Dw_WireDriver_CrvShape', 'L_Eyelids_Dw_6_Ctrl', 'L_Eyelids_DwEnd_Jnt_Offset_Grp', 'R_Eyelids_Dw_3_Loc', 'R_Eyelids_Up_BlinkTarget_CrvShapeOrig1', 'L_Eyelids_Dw_6_Loc', 'L_Eyelids_Dw_Origin_2_Jnt', 'R_Eyelids_UpStart_CtrlShape', 'R_Eyelids_Up_2_Ctrl_Offset_Grp', 'L_Eyelids_DwMid_Ctrl_tag', 'L_Eyelids_Dw_4_LocShape', 'L_Eyelids_Dw_7_Ctrl', 'L_Eyelids_Dw_0_Jnt', 'L_Eyelids_Dw_6_Ctrl_tag', 'skinCluster6GroupId', 'R_Eyelids_Dw_6_Jnt', 'L_Eyelids_UpStartMid_Ctrl_tag', 'L_Eyelids_DwWire', 'L_Eyelids_Scale_Jnt_Offset_Grp', 'R_Eyelids_Dw_7_Ctrl_Offset_Grp', 'L_Eyelids_Dw_Vtx_Crv', 'R_Eyelids_UpWireGroupParts', 'R_Eyelids_LwrBlink_BS', 'R_Eyelids_Up_5_Ctrl_OffsetPivot_Grp', 'R_Eyelids_Up_0_Ctrl_Offset_Grp', 'L_Eyelids_Up_Origin_4_Jnt', 'L_EyelidsUprBlink_CtrlShape', 'R_Eyelids_Up_Scale_Ctrl_Offset_Grp', 'L_Eyelids_DwEndMid_Ctrl_tag', 'R_Eyelids_Up_Origin_1_Jnt_Offset_Grp', 'L_Eyelids_BlinkAttrs_Ctrl_Offset_Grp', 'R_Eyelids_Dw_0_Jnt', 'L_Eyelids_Up_2_Ctrl_OffsetPivot_Grp', 'L_Eyelids_UpStart_CtrlShape', 'L_Eyelids_Dw_1_Loc', 'L_Eyelids_Up_2_LocShape', 'L_Eyelids_Up_Origin_0_Jnt', 'L_Eyelids_Dw_5_CtrlShape', 'R_Eyelids_Up_4_Loc', 'R_Eyelids_UpEnd_CtrlShape', 'R_Eyelids_Dw_3_Jnt_Offset_Grp', 'R_Eyelids_Dw_2_Jnt_Offset_Grp', 'L_Eyelids_LwrBlink_BSSet', 'L_Eyelids_Dw_6_Ctrl_OffsetPivot_Grp_Offset_Grp', 'R_Eyelids_Dw_5_Ctrl_OffsetPivot_Grp', 'L_Eyelids_Up_1_Ctrl', 'L_Eyelids_UprBlink_BSGroupParts', 'L_Eyelids_Up_WireGroupParts', 'L_Eyelids_Up_1_LocShape', 'R_Eyelids_Up_Tweeks_Ctrl_Grp', 'L_EyelidsLwrBlink_Ctrl_Offset_Grp', 'L_Eyelids_Dw_Ctrl_Grp', 'R_Eyelids_DwStartMid_Ctrl_tag', 'L_Eyelids_Up_Scale_Ctrl_tag', 'L_Eyelids_DwWireGroupParts', 'L_Eyelids_UpVector_LocShape', 'L_Eyelids_Up_2_Ctrl_Offset_Grp', 'L_Eyelids_Up_3_Ctrl_OffsetPivot_Grp_Offset_Grp', 'R_Eyelids_Up_3_Jnt', 'R_Eyelids_DwStartMid_Jnt_Offset_Grp', 'L_Eyelids_Dw_2_Ctrl', 'R_Eyelids_Dw_3_Ctrl_Offset_Grp', 'R_Eyelids_LwrBlink_BSGroupId', 'R_Eyelids_Scale_Grp_Offset_Grp', 'L_Eyelids_Dw_VtxJnts_Grp', 'L_Eyelids_Up_3_LocShape', 'L_Eyelids_Up_8_Jnt_Offset_Grp', 'L_Eyelids_Dw_6_CtrlShape', 'L_Eyelids_Dw_Origin_1_Jnt_Offset_Grp', 'R_Eyelids_Up_WireGroupParts', 'L_Eyelids_Up_1_Loc', 'R_Eyelids_Dw_BlinkTarget_Crv', 'L_Eyelids_Up_Origin_3_Jnt_aimConstraint1', 'R_Eyelids_DwEndMid_Ctrl_Offset_Grp_parentConstraint1', 'R_Eyelids_DwEndMid_Ctrl_Offset_Grp', 'L_Eyelids_Blink_CrvBaseWireShapeOrig2', 'R_Eyelids_Up_6_Loc', 'R_Eyelids_UpEndMid_Ctrl_Offset_Grp', 'L_Eyelids_Up_3_Ctrl_tag', 'L_Eyelids_Up_5_POCI', 'L_Eyelids_Up_4_Ctrl_OffsetPivot_Grp', 'L_Eyelids_Up_4_CtrlShape', 'L_Eyelids_Dw_7_Ctrl_Offset_Grp', 'L_Eyelids_Scale_Ctrl_Offset_Grp', 'R_Eyelids_Dw_4_Ctrl_OffsetPivot_Grp_Offset_Grp', 'R_Eyelids_UpEndMid_Jnt', 'L_Eyelids_Up_8_Jnt', 'R_Eyelids_Up_7_Ctrl_OffsetPivot_Grp_Offset_Grp', 'L_Eyelids_Ctrl_Grp_scaleConstraint1', 'R_Eyelids_Dw_1_Ctrl_OffsetPivot_Grp_Offset_Grp', 'R_Eyelids_Dw_Scale_Ctrl', 'L_Eyelids_Dw_Scale_Grp', 'L_Eyelids_Dw_2_Ctrl_OffsetPivot_Grp_Offset_Grp', 'R_Eyelids_Dw_1_Ctrl', 'R_Eyelids_Up_7_POCI', 'L_Eyelids_Up_5_CtrlShape', 'R_Eyelids_UpEnd_Ctrl_tag', 'L_Eyelids_Up_5_LocShape', 'R_Eyelids_Up_5_Ctrl_OffsetPivot_Grp_Offset_Grp', 'R_Eyelids_Up_Origin_4_Jnt', 'R_Eyelids_Up_0_Ctrl_OffsetPivot_Grp', 'R_Eyelids_Dw_Scale_CtrlShape', 'R_Eyelids_Up_8_POCI', 'R_Eyelids_Up_BlinkTarget_Crv', 'R_Eyelids_Dw_0_Loc', 'R_Eyelids_Dw_2_CtrlShape', 'L_Eyelids_UpVector_Loc', 'L_Eyelids_Up_8_Ctrl', 'L_Eyelids_Blink_CrvShape', 'R_Eyelids_Dw_4_LocShape', 'L_Eyelids_Up_0_Jnt_Offset_Grp', 'R_Eyelids_Dw_2_Jnt', 'R_Eyelids_Dw_4_Loc', 'R_Eyelids_DwEnd_Jnt_Offset_Grp', 'L_Eyelids_Up_3_Ctrl_Offset_Grp', 'R_Eyelids_Dw_4_Jnt_Offset_Grp', 'R_Eyelids_Dw_5_LocShape', 'R_Eyelids_Up_5_Jnt', 'skinCluster3GroupId', 'L_Eyelids_Dw_Origin_3_Jnt_Offset_Grp', 'L_Eyelids_Dw_AimLocators_Grp', 'R_Eyelids_Ctrl_Grp_scaleConstraint1', 'R_Eyelids_Up_4_Jnt_Offset_Grp', 'L_Eyelids_Up_Origin_3_Jnt', 'L_Eyelids_Up_BlinkTarget_Crv', 'L_Eyelids_Up_1_Jnt', 'R_Eyelids_Up_2_Jnt_Offset_Grp', 'R_Eyelids_Dw_4_Jnt', 'L_Eyelids_Up_2_Ctrl_OffsetPivot_Grp_Offset_Grp', 'L_Eyelids_Up_1_Jnt_Offset_Grp', 'L_Eyelids_Up_3_Jnt', 'L_Eyelids_DwEndMid_Jnt_Offset_Grp', 'L_Eyelids_Dw_Jnt_Grp', 'L_Eyelids_Dw_0_Ctrl_OffsetPivot_Grp', 'R_Eyelids_Up_WireDriver_CrvShapeOrig', 'R_Eyelids_Ctrl_Grp_parentConstraint1', 'L_Eyelids_Dw_2_LocShape', 'L_Eyelids_Up_Ctrl_Grp', 'R_Eyelids_Dw_7_CtrlShape', 'R_Eyelids_Dw_2_Ctrl_tag', 'L_Eyelids_UpStart_Ctrl', 'R_Eyelids_Up_5_Ctrl', 'L_Eyelids_Up_3_Loc', 'R_Eyelids_Up_8_CtrlShape', 'R_Eyelids_Up_WireDriver_CrvShapeOrig1', 'R_Eyelids_Scale_Ctrl_tag', 'L_Eyelids_UpStart_Jnt_Offset_Grp', 'R_Eyelids_DwStart_Ctrl_Offset_Grp', 'L_Eyelids_Up_4_Ctrl', 'R_Eyelids_Up_0_POCI', 'L_Eyelids_Dw_Origin_2_Jnt_Offset_Grp', 'R_Eyelids_Dw_2_Ctrl', 'R_Eyelids_Up_Origin_0_Jnt_Offset_Grp', 'L_Eyelids_Up_1_CtrlShape', 'R_Eyelids_Dw_Origin_3_Jnt_Offset_Grp', 'R_Eyelids_Dw_WireDriver_CrvBaseWireShapeOrig', 'R_Eyelids_Up_7_Loc', 'L_Eyelids_Dw_Origin_3_Jnt_aimConstraint1', 'R_Eyelids_Blink_BSSet', 'L_Eyelids_Ctrl_Grp', 'L_Eyelids_UpMid_CtrlShape', 'L_Eyelids_UpMid_Ctrl_Offset_Grp', 'L_Eyelids_Up_WireDriver_Crv', 'R_Eyelids_UpEnd_Jnt_Offset_Grp', 'L_Eyelids_Blink_BS', 'L_Eyelids_Blink_CrvBaseWireShapeOrig', 'unitConversion18', 'L_Eyelids_UpStartMid_Jnt_Offset_Grp_parentConstraint1', 'L_Eyelids_Dw_5_Jnt_Offset_Grp', 'R_EyelidsLwrBlink_Ctrl', 'R_Eyelids_Up_3_Jnt_Offset_Grp', 'unitConversion17', 'R_Eyelids_Blink_CrvBaseWire1Shape', 'R_Eyelids_Up_Scale_Grp', 'R_Eyelids_Up_8_Ctrl_tag', 'R_Eyelids_Dw_6_Ctrl_Offset_Grp', 'L_Eyelids_Dw_7_Ctrl_tag', 'R_Eyelids_Dw_Vtx_Crv', 'L_Eyelids_UpEndMid_CtrlShape', 'R_Eyelids_Up_Ctrl_Grp', 'skinCluster3', 'R_Eyelids_Dw_5_Ctrl', 'L_Eyelids_Up_Scale_CtrlShape', 'R_Eyelids_Blink_CrvBaseWireShapeOrig1', 'L_Eyelids_DwEnd_Ctrl_Offset_Grp', 'R_Eyelids_Up_0_Ctrl_tag', 'R_Eyelids_Dw_0_CtrlShape', 'R_Eyelids_Up__cv3_Bnd', 'R_Eyelids_Up_8_Loc', 'unitConversion21', 'R_Eyelids_Dw_Origin_6_Jnt_aimConstraint1', 'L_Eyelids_Up_6_Loc', 'L_Eyelids_Dw_1_Ctrl_tag', 'L_Eyelids_Up_WireDriver_CrvBaseWireShape', 'L_Eyelids_Up_0_LocShape', 'R_Eyelids_UpStart_Ctrl_Offset_Grp', 'R_Eyelids_Dw_Origin_7_Jnt_aimConstraint1', 'L_Eyelids_Dw_WireGroupParts', 'R_Eyelids_Up_Vtx_CrvShape', 'L_Eyelids_Dw_Origin_0_Jnt', 'R_Eyelids_Up_3_Ctrl_OffsetPivot_Grp', 'R_Eyelids_Dw_WireDriver_CrvShapeOrig', 'L_Eyelids_Up_Origin_4_Jnt_aimConstraint1', 'L_Eyelids_Blink_CrvBaseWire', 'L_Eyelids_Up_Origin_7_Jnt_Offset_Grp', 'R_Eyelids_Dw_1_Ctrl_tag', 'L_Eyelids_Up_BlinkTarget_CrvShapeOrig1', 'L_Eyelids_Dw_7_Ctrl_OffsetPivot_Grp_Offset_Grp', 'R_Eyelids_DwMid_CtrlShape', 'L_Eyelids_Dw_Scale_Ctrl_tag', 'LwrBlink_MultDiv4', 'L_Eyelids_Up_8_LocShape', 'R_Eyelids_Dw_BlinkTarget_CrvShape', 'R_Eyelids_Dw_Origin_6_Jnt_Offset_Grp', 'L_Eyelids_Dw_Origin_6_Jnt_aimConstraint1', 'L_Eyelids_Up_5_Ctrl_OffsetPivot_Grp_Offset_Grp', 'L_Eyelids_Scale_Jnt', 'R_Eyelids_Dw__cv3_Bnd_scaleConstraint1', 'R_Eyelids_Dw_Vtx_CrvShape', 'L_Eyelids_DwStartMid_CtrlShape', 'L_Eyelids_DwWireSet', 'R_Eyelids_DwStartMid_CtrlShape', 'R_Eyelids_UpEndMid_Ctrl', 'R_Eyelids_UpStart_Jnt_Offset_Grp', 'L_Eyelids_Up_7_Ctrl', 'L_Eyelids_Dw_5_Loc', 'L_Eyelids_Dw_1_Jnt_Offset_Grp', 'L_Eyelids_Blink_BSGroupParts', 'L_Eyelids_Up__cv3_Bnd_scaleConstraint1', 'R_Eyelids_DwStartMid_Jnt_Offset_Grp_parentConstraint1', 'R_Eyelids_Up_Vtx_CrvShapeOrig', 'R_Eyelids_Up_3_Ctrl', 'L_Eyelids_Up_5_Ctrl_tag', 'R_EyelidsUprBlink_Ctrl_tag', 'R_Eyelids_Dw_0_LocShape', 'R_Eyelids_Dw_Origin_6_Jnt', 'R_Eyelids_Dw_3_Ctrl_OffsetPivot_Grp', 'R_Eyelids_UpEndMid_Jnt_Offset_Grp_parentConstraint1', 'L_Eyelids_Up_1_Ctrl_OffsetPivot_Grp', 'skinCluster6GroupParts', 'L_Eyelids_Up_3_CtrlShape', 'R_Eyelids_Scale_Jnt_Offset_Grp', 'R_Eyelids_Up_Origin_4_Jnt_aimConstraint1', 'R_Eyelids_Blink_BS', 'L_Eyelids_UpEndMid_Ctrl_tag', 'R_EyelidsLwrBlink_CtrlShape', 'R_Eyelids_Dw_1_CtrlShape', 'R_Eyelids_Up_Origin_1_Jnt', 'R_Eyelids_Up_Origin_6_Jnt_Offset_Grp', 'L_Eyelids_Dw_Origin_0_Jnt_aimConstraint1', 'R_Eyelids_Dw_Origin_0_Jnt', 'L_Eyelids_Dw_1_Jnt', 'L_Eyelids_DwEndMid_Jnt', 'L_Eyelids_Dw_5_LocShape', 'R_Eyelids_Dw_7_Ctrl_tag', 'L_Eyelids_Up_7_Ctrl_OffsetPivot_Grp', 'R_Eyelids_Dw_0_POCI', 'R_Eyelids_BlinkAttrs_Ctrl_tag', 'L_Eyelids_UpEnd_Ctrl', 'R_Eyelids_Up_0_Jnt', 'R_Eyelids_Dw_0_Jnt_Offset_Grp', 'R_Eyelids_Up_1_CtrlShape', 'R_Eyelids_UprBlink_BSGroupParts', 'L_Eyelids_Dw__cv3_Bnd', 'R_Eyelids_Dw_0_Ctrl', 'R_Eyelids_Dw_1_POCI', 'R_Eyelids_Up_Origin_5_Jnt_Offset_Grp', 'L_Eyelids_Dw_7_LocShape', 'R_Eyelids_Dw_Vtx_CrvShapeOrig', 'L_Eyelids_DwStart_Jnt_Offset_Grp', 'R_Eyelids_UpEndMid_CtrlShape', 'R_Eyelids_Dw_5_Ctrl_OffsetPivot_Grp_Offset_Grp', 'L_Eyelids_Up_8_Ctrl_tag', 'L_Eyelids_Up_8_Ctrl_OffsetPivot_Grp', 'R_Eyelids_UpMid_Ctrl_Offset_Grp', 'skinCluster3Set', 'L_Eyelids_DwEndMid_Ctrl_Offset_Grp', 'L_Eyelids_Up_5_Jnt_Offset_Grp', 'R_Eyelids_Up_5_LocShape', 'L_Eyelids_UpStartMid_Ctrl', 'L_Eyelids_Blink_CrvBaseWireShape', 'L_Eyelids_UpEnd_CtrlShape', 'R_Eyelids_DwEnd_Jnt', 'L_Eyelids_Dw_6_Jnt_Offset_Grp', 'L_Eyelids_Up_WireGroupId', 'L_Eyelids_DwStart_Jnt', 'R_Eyelids_UpStartMid_Ctrl_Offset_Grp_parentConstraint1', 'L_Eyelids_Up_VtxJnts_Grp', 'R_Eyelids_Dw_Origin_7_Jnt_Offset_Grp', 'L_Eyelids_Up_WireDriver_CrvShapeOrig', 'L_Eyelids_UpEnd_Jnt_Offset_Grp', 'R_Eyelids_DwWire', 'L_Eyelids_DwStart_Ctrl', 'R_Eyelids_LwrBlink_BSGroupParts', 'R_Eyelids_Up_Origin_3_Jnt_Offset_Grp', 'R_Eyelids_Up_7_Jnt_Offset_Grp', 'R_Eyelids_Scale_Jnt', 'L_Eyelids_Up_7_LocShape', 'R_Eyelids_Up_3_Ctrl_tag', 'L_Eyelids_Up_0_Ctrl_tag', 'R_Eyelids_Up_2_CtrlShape', 'R_Eyelids_Dw_3_POCI', 'R_Eyelids_DwStart_Ctrl', 'L_Eyelids_Up_Origin_6_Jnt', 'R_Eyelids_Dw_5_Loc', 'R_Eyelids_UpStartMid_Ctrl', 'skinCluster4', 'R_Eyelids_UpStartMid_Ctrl_tag', 'R_Eyelids_UpEnd_Ctrl_Offset_Grp', 'R_Eyelids_Blink_BSGroupId', 'L_Eyelids_Up_Origin_2_Jnt_Offset_Grp', 'R_Eyelids_UpEndMid_Jnt_Offset_Grp', 'R_Eyelids_Up_4_Ctrl', 'R_Eyelids_Dw_5_Jnt_Offset_Grp', 'R_Eyelids_Rig_Grp_parentConstraint1', 'R_Eyelids_Up_1_POCI', 'R_Eyelids_Dw_2_LocShape', 'L_Eyelids_Up_7_POCI', 'L_Eyelids_Dw_1_POCI', 'R_Eyelids_UpStartMid_Jnt', 'R_Eyelids_Dw_7_Ctrl', 'R_Eyelids_Up_Origin_7_Jnt', 'R_Eyelids_UpStart_Ctrl', 'L_Eyelids_Dw_4_Ctrl_OffsetPivot_Grp_Offset_Grp', 'L_Eyelids_Dw_Origin_5_Jnt', 'bindPose3', 'R_Eyelids_Dw_7_Jnt', 'R_Eyelids_Dw_7_Jnt_Offset_Grp', 'L_Eyelids_Dw_5_Ctrl_OffsetPivot_Grp', 'L_Eyelids_Dw_Origin_4_Jnt', 'R_Eyelids_UprBlink_BSGroupId', 'R_Eyelids_Dw_4_Ctrl_OffsetPivot_Grp', 'R_Eyelids_Dw_0_Ctrl_tag', 'L_Eyelids_Up_4_Loc', 'L_Eyelids_DwStartMid_Jnt_Offset_Grp_parentConstraint1', 'bindPose6', 'R_Eyelids_UpEndMid_Ctrl_tag', 'R_Eyelids_Dw_Origin_3_Jnt', 'R_Eyelids_UpMid_Jnt_Offset_Grp', 'R_Eyelids_Dw_Origin_5_Jnt', 'R_Eyelids_Up_6_LocShape', 'R_Eyelids_Up_3_Ctrl_OffsetPivot_Grp_Offset_Grp', 'L_Eyelids_DwWireGroupId', 'R_Eyelids_Dw_Scale_Grp_Offset_Grp', 'R_Eyelids_Dw_2_Ctrl_OffsetPivot_Grp_Offset_Grp', 'R_Eyelids_Up_2_Ctrl_tag', 'L_Eyelids_Dw_0_CtrlShape', 'R_Eyelids_Up_2_Ctrl_OffsetPivot_Grp_Offset_Grp', 'R_Eyelids_Dw_WireDriver_CrvShapeOrig1', 'R_Eyelids_Up_0_CtrlShape', 'L_Eyelids_Blink_CrvShapeOrig1', 'R_Eyelids_Up_WireDriver_CrvBaseWireShape', 'L_Eyelids_Up_Origin_5_Jnt', 'R_Eyelids_UpWireSet', 'L_Eyelids_UpEndMid_Ctrl_Offset_Grp', 'L_Eyelids_Up_Origin_8_Jnt', 'R_Eyelids_Up_Origin_3_Jnt_aimConstraint1', 'L_Eyelids_UpStartMid_Ctrl_Offset_Grp_parentConstraint1', 'LwrBlink_MultDiv1', 'L_Eyelids_Rig_Grp_scaleConstraint1', 'L_Eyelids_Up_8_CtrlShape', 'L_Eyelids_Dw_2_POCI', 'L_Eyelids_Dw_3_Ctrl', 'L_Eyelids_Up_6_POCI', 'L_Eyelids_Dw__cv3_Bnd_scaleConstraint1', 'LwrBlink_MultDiv5', 'R_Eyelids_Up_Origin_0_Jnt_aimConstraint1', 'L_Eyelids_Up_6_Ctrl', 'R_Eyelids_Dw_3_Ctrl_tag', 'R_Eyelids_Blink_Crv', 'R_Eyelids_Up_VtxJnts_Grp', 'bindPose4', 'L_Eyelids_UpStart_Ctrl_Offset_Grp', 'L_Eyelids_Dw_Origin_7_Jnt', 'R_Eyelids_UpMid_Ctrl', 'R_Eyelids_Up_7_Ctrl', 'R_Eyelids_Dw_Origin_2_Jnt', 'L_Eyelids_Rig_Grp', 'R_Eyelids_Up_3_Ctrl_Offset_Grp', 'L_Eyelids_Dw_2_Ctrl_OffsetPivot_Grp', 'R_Eyelids_DwStartMid_Ctrl', 'L_Eyelids_Up_WireDriver_CrvBaseWire', 'R_Eyelids_Dw_Origin_5_Jnt_aimConstraint1', 'R_Eyelids_Up_BlinkTarget_CrvShapeOrig', 'R_Eyelids_Up_1_Ctrl_Offset_Grp', 'L_Eyelids_Blink_BSSet', 'R_Eyelids_BlinkAttrs_Ctrl_Offset_Grp', 'R_EyelidsUprBlink_Ctrl_Offset_Grp', 'L_Eyelids_Up_7_Jnt_Offset_Grp', 'L_Eyelids_Dw_WireDriver_Crv', 'unitConversion20', 'L_Eyelids_Blink_Reverse', 'R_Eyelids_Up_5_Ctrl_tag', 'LwrBlink_MultDiv2', 'L_Eyelids_Dw_Origin_3_Jnt', 'R_Eyelids_DwStartMid_Ctrl_Offset_Grp', 'R_Eyelids_Dw_AimLocators_Grp', 'L_Eyelids_Up_Origin_1_Jnt', 'L_Eyelids_Up_Vtx_CrvShapeOrig', 'L_Eyelids_Dw_5_Ctrl_OffsetPivot_Grp_Offset_Grp', 'R_Eyelids_Blink_CrvBaseWire1', 'L_Eyelids_Rig_Grp_parentConstraint1', 'R_Eyelids_DwStartMid_Jnt', 'L_Eyelids_Up_4_Ctrl_tag', 'R_Eyelids_Dw_2_Ctrl_Offset_Grp', 'R_Eyelids_Dw_WireDriver_Crv', 'R_Eyelids_DwEndMid_Jnt_Offset_Grp_parentConstraint1', 'L_Eyelids_Up_Origin_8_Jnt_Offset_Grp', 'R_Eyelids_Dw_1_Jnt', 'L_Eyelids_Up_Origin_0_Jnt_Offset_Grp', 'L_Eyelids_Up_7_Ctrl_tag', 'R_Eyelids_DwEndMid_Jnt_Offset_Grp', 'R_Eyelids_UpStart_Ctrl_tag', 'R_Eyelids_Up_5_Ctrl_Offset_Grp', 'R_Eyelids_Up_4_Ctrl_OffsetPivot_Grp_Offset_Grp', 'L_Eyelids_Dw_4_Ctrl_OffsetPivot_Grp', 'L_Eyelids_Up_2_CtrlShape', 'L_Eyelids_Up_WireDriver_CrvBaseWireShapeOrig', 'R_Eyelids_Dw_Origin_2_Jnt_aimConstraint1', 'R_Eyelids_Dw_6_Jnt_Offset_Grp', 'R_Eyelids_Up_Origin_2_Jnt_aimConstraint1', 'L_Eyelids_Dw_4_Ctrl', 'R_Eyelids_Up_4_Jnt', 'R_Eyelids_Up_4_Ctrl_OffsetPivot_Grp', 'R_Eyelids_Dw_Tweeks_Ctrl_Grp', 'R_Eyelids_Dw_5_Ctrl_Offset_Grp', 'R_Eyelids_Dw_4_CtrlShape', 'L_Eyelids_Dw_1_Ctrl', 'L_Eyelids_Scale_Ctrl_tag', 'R_Eyelids_Blink_CrvShape', 'L_Eyelids_Dw_7_Loc', 'L_Eyelids_Up_Vtx_CrvShape', 'skinCluster3GroupParts', 'R_Eyelids_Dw_6_Ctrl_OffsetPivot_Grp_Offset_Grp', 'R_Eyelids_Dw_Origin_0_Jnt_Offset_Grp', 'R_Eyelids_Dw_5_Jnt', 'R_Eyelids_Ctrl_Grp', 'L_Eyelids_UprBlink_BS', 'L_Eyelids_Up_1_POCI', 'R_Eyelids_Up_6_Jnt_Offset_Grp', 'L_Eyelids_Dw_2_CtrlShape', 'R_Eyelids_UpStartMid_Jnt_Offset_Grp', 'L_Eyelids_Blink_CrvBaseWire1Shape', 'L_Eyelids_LwrBlink_BSGroupId', 'L_Eyelids_Up_Origin_2_Jnt_aimConstraint1', 'R_Eyelids_Blink_CrvBaseWireShapeOrig2', 'L_Eyelids_Up_7_CtrlShape', 'L_Eyelids_UprBlink_BSSet', 'R_Eyelids_DwEnd_Ctrl', 'R_Eyelids_Up_2_Jnt', 'R_Eyelids_Up_7_Jnt', 'L_Eyelids_Dw_0_Ctrl_tag', 'L_Eyelids_Up_Tweeks_Ctrl_Grp', 'L_Eyelids_Up_6_Ctrl_tag', 'L_Eyelids_DwEndMid_Jnt_Offset_Grp_parentConstraint1', 'L_Eyelids_Up__cv3_Bnd_parentConstraint1', 'R_Eyelids_Up_Origin_3_Jnt', 'L_Eyelids_Up_2_Jnt_Offset_Grp', 'R_Eyelids_Blink_CrvBaseWire1ShapeOrig', 'R_Eyelids_Dw_WireGroupId', 'R_Eyelids_DwStart_Jnt', 'R_Eyelids_Up_2_Loc', 'L_Eyelids_Dw_3_Ctrl_OffsetPivot_Grp', 'L_Eyelids_DwEndMid_Ctrl_Offset_Grp_parentConstraint1', 'L_Eyelids_Dw_1_Ctrl_OffsetPivot_Grp', 'R_Eyelids_Up_Origin_7_Jnt_Offset_Grp', 'R_Eyelids_Up_Wire', 'R_Eyelids_Dw_7_POCI', 'L_Eyelids_Up_3_Ctrl_OffsetPivot_Grp', 'R_Eyelids_Up_8_Ctrl', 'R_Eyelids_DwMid_Ctrl_Offset_Grp', 'L_Eyelids_Dw_3_Jnt', 'R_Eyelids_Blink_BSGroupParts', 'L_Eyelids_Up_5_Loc', 'R_Eyelids_Dw_BlinkTarget_CrvShapeOrig', 'L_Eyelids_Up_5_Ctrl_OffsetPivot_Grp', 'R_Eyelids_Blink_CrvBaseWire1ShapeOrig2', 'L_Eyelids_UpWireGroupId', 'L_Eyelids_Up_0_Ctrl', 'R_Eyelids_Up__cv3_Bnd_scaleConstraint1', 'R_Eyelids_Dw_5_CtrlShape', 'R_Eyelids_Up_8_Jnt', 'R_Eyelids_Up_Origin_5_Jnt_aimConstraint1', 'R_Eyelids_Up_1_Ctrl_OffsetPivot_Grp_Offset_Grp', 'L_Eyelids_Up_Origin_7_Jnt_aimConstraint1', 'R_Eyelids_Up_6_Ctrl', 'L_Eyelids_Dw_3_Jnt_Offset_Grp', 'R_Eyelids_Up_7_Ctrl_Offset_Grp', 'L_Eyelids_Dw_BlinkTarget_CrvShapeOrig', 'R_Eyelids_DwStart_Ctrl_tag', 'L_Eyelids_Up_6_Jnt', 'R_Eyelids_DwEnd_Ctrl_Offset_Grp', 'L_Eyelids_Up_1_Ctrl_Offset_Grp', 'L_Eyelids_Blink_CrvBaseWire1', 'L_Eyelids_Dw_Origin_7_Jnt_Offset_Grp', 'R_Eyelids_Dw_0_Ctrl_OffsetPivot_Grp_Offset_Grp', 'L_Eyelids_Up_0_Ctrl_OffsetPivot_Grp_Offset_Grp', 'R_Eyelids_Dw_Jnt_Grp', 'L_Eyelids_Up_AimLocators_Grp', 'R_Eyelids_Dw_Origin_4_Jnt_Offset_Grp', 'R_Eyelids_Up_0_Loc', 'R_Eyelids_Dw_7_Ctrl_OffsetPivot_Grp_Offset_Grp', 'R_Eyelids_DwWireGroupId', 'LwrBlink_MultDiv3', 'L_Eyelids_Dw_7_Jnt_Offset_Grp', 'R_Eyelids_Dw_4_Ctrl_Offset_Grp', 'L_Eyelids_Dw_WireDriver_CrvBaseWireShapeOrig', 'R_Eyelids_Rig_GrpMirror_Grp', 'bindPose5', 'L_Eyelids_Up_Origin_6_Jnt_Offset_Grp', 'L_Eyelids_Up_Origin_3_Jnt_Offset_Grp', 'L_Eyelids_DwMid_Jnt_Offset_Grp', 'skinCluster4GroupParts', 'L_Eyelids_Blink_CrvShapeOrig2', 'L_EyelidsUprBlink_Ctrl', 'L_Eyelids_Dw_0_Loc', 'L_Eyelids_Up_Scale_Ctrl', 'L_Eyelids_BlinkAttrs_Ctrl', 'L_Eyelids_Up_Origin_5_Jnt_aimConstraint1', 'L_Eyelids_BlinkAttrs_Ctrl_tag', 'R_Eyelids_Dw_WireDriver_CrvBaseWireShape', 'L_Eyelids_Up_7_Loc', 'R_Eyelids_Up_2_POCI']");
createNode joint -n "EyePivot" -p "L_Eyelids_Block";
	rename -uid "AB46007A-EC42-9842-743A-9D8A7721A8E9";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/";
	setAttr ".t" -type "double3" 15.806531429290771 24.386816659911915 141.32936859130859 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
createNode dagContainer -n "L_Ear_Block" -p "face";
	rename -uid "92F4560B-2549-612F-9AB6-6DB4B062584D";
	addAttr -ci true -sn "nts" -ln "notes" -dt "string";
	setAttr ".isc" yes;
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/Chain.png";
	setAttr ".ctor" -type "string" "estebanrdgz";
	setAttr ".cdat" -type "string" "2025/09/04 19:06:23";
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
	setAttr ".nts" -type "string" "['R_Ear_A_Ctrl_Offset_Grp_parentConstraint1', 'L_Ear_A_Bnd_Bnd_parentConstraint1', 'L_Ear_A_Jnt_Jnt_Ctrl_tag', 'R_Ear_A_Bnd_Bnd_scaleConstraint1', 'L_Ear_Rig_Grp', 'L_Ear_A_Bnd_Bnd', 'R_Ear_A_Jnt_Jnt_Ctrl_tag', 'L_Ear_A_Ctrl', 'L_Ear_A_Jnt_Jnt', 'R_Ear_A_Jnt_Jnt', 'R_Ear_A_Jnt_Jnt_scaleConstraint1', 'L_Ear_Ctrl_Grp', 'R_Ear_A_Bnd_Bnd', 'L_Ear_A_Jnt_Jnt_scaleConstraint1', 'L_Ear_A_Ctrl_Offset_Grp_parentConstraint1', 'R_Ear_A_Jnt_Jnt_parentConstraint1', 'R_Ear_A_CtrlShape', 'R_Ear_A_Ctrl_Offset_Grp', 'R_Ear_A_Bnd_Bnd_parentConstraint1', 'L_Ear_A_Bnd_Bnd_scaleConstraint1', 'L_Ear_A_Jnt_Jnt_parentConstraint1', 'L_Ear_A_Ctrl_Offset_Grp', 'L_Ear_A_CtrlShape', 'R_Ear_A_Ctrl']";
createNode joint -n "L_Ear_A_Guide_Guide" -p "L_Ear_Block";
	rename -uid "A18DDEDF-6F4A-1E2F-E1A0-19B5D67676F8";
	addAttr -ci true -sn "Helper" -ln "Helper" -min 0 -max 1 -en "Hide:Show" -at "enum";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/";
	setAttr ".t" -type "double3" 27.416750160833679 38.563907511098648 113.37795672134081 ;
	setAttr ".r" -type "double3" -24.170159390446695 -22.024987316633954 -6.4612538896715819 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr -cb on ".Helper" 1;
createNode nurbsCurve -n "L_Ear_A_Guide_Guide_CtrlShape" -p "L_Ear_A_Guide_Guide";
	rename -uid "1CCC809C-3649-EAF9-B378-88B4BBA02EC4";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/";
	setAttr -k off ".v";
	setAttr ".ove" yes;
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
createNode nurbsCurve -n "L_Ear_A_Guide_Guide_Ctrl_CtrlShape" -p "L_Ear_A_Guide_Guide";
	rename -uid "2991B3F7-1C41-BCB2-7C71-0DB0D53878EE";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/";
	setAttr -k off ".v";
	setAttr ".ove" yes;
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
createNode nurbsCurve -n "L_Ear_A_Guide_Guide_Ctrl_Ctrl_CtrlShape" -p "L_Ear_A_Guide_Guide";
	rename -uid "3C52BA04-D648-B2D6-3BB7-A4A39E2F6615";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 13;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 9 0 no 3
		10 0 1 2 3 4 5 6 7 8 9
		10
		-0.49999999999999994 -0.25000000000000011 -1.3977300000111021e-05
		0.94513100000000017 -0.25591599999999975 -1.3977299999790138e-05
		0.73965300000000012 -0.50644299999999987 -1.3977299999835763e-05
		0.99018000000000017 -0.93915099999999974 -1.3977299999780135e-05
		2.299302 -3.8742999948945234e-07 -1.3798499999489453e-05
		0.99018099999999976 0.93915100000000018 -1.3977299999780135e-05
		0.73965299999999989 0.50644200000000006 -1.3977299999835763e-05
		0.94513099999999994 0.2532210000000002 -7.1674599997901393e-06
		-0.5 0.24999999999999989 -1.3977300000111021e-05
		-0.49999999999999994 -0.25000000000000011 -1.3977300000111021e-05
		;
createNode nurbsCurve -n "L_Ear_A_Guide_Guide_Ctrl_Ctrl_Ctrl_CtrlShape" -p "L_Ear_A_Guide_Guide";
	rename -uid "73D399EC-2E4B-197A-9349-2A812927200C";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 6;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 9 0 no 3
		10 0 1 2 3 4 5 6 7 8 9
		10
		0.25000000000000011 1.3977299999944488e-05 -0.49999999999999994
		0.25591599999999975 1.3977299999943175e-05 0.94513100000000017
		0.50644299999999987 1.3977299999887547e-05 0.73965300000000012
		0.93915099999999974 1.3977299999791466e-05 0.99018000000000017
		3.8742999948945541e-07 1.37985e-05 2.299302
		-0.93915100000000018 1.3977300000208532e-05 0.99018099999999976
		-0.50644200000000006 1.3977300000112451e-05 0.73965299999999989
		-0.2532210000000002 7.1674600000562262e-06 0.94513099999999994
		-0.24999999999999989 1.397730000005551e-05 -0.5
		0.25000000000000011 1.3977299999944488e-05 -0.49999999999999994
		;
createNode dagContainer -n "Nose_Block" -p "face";
	rename -uid "9D5E4F25-2145-E93E-7721-A0AD3D4DAE40";
	addAttr -ci true -sn "nts" -ln "notes" -dt "string";
	setAttr ".isc" yes;
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/Chain.png";
	setAttr ".ctor" -type "string" "estebanrdgz";
	setAttr ".cdat" -type "string" "2025/09/04 19:06:39";
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
	setAttr ".nts" -type "string" "['Nose_A_Jnt_Jnt_scaleConstraint1', 'Nose_A_CtrlShape', 'Nose_A_Ctrl_Offset_Grp_parentConstraint1', 'Nose_A_Jnt_Jnt', 'Nose_Ctrl_Grp', 'Nose_A_Bnd_Bnd_parentConstraint1', 'Nose_A_Jnt_Jnt_parentConstraint1', 'Nose_A_Ctrl', 'Nose_Rig_Grp', 'Nose_A_Jnt_Jnt_Ctrl_tag', 'Nose_A_Bnd_Bnd_scaleConstraint1', 'Nose_A_Ctrl_Offset_Grp', 'Nose_A_Bnd_Bnd']";
createNode joint -n "Nose_A_Guide_Guide" -p "Nose_Block";
	rename -uid "4AFED99A-5E47-CB77-693E-44A638045D4D";
	addAttr -ci true -sn "Helper" -ln "Helper" -min 0 -max 1 -en "Hide:Show" -at "enum";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/";
	setAttr ".t" -type "double3" 0 17.810929485619852 160.60664873683177 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr -cb on ".Helper" 1;
createNode nurbsCurve -n "Nose_A_Guide_Guide_CtrlShape" -p "Nose_A_Guide_Guide";
	rename -uid "98537291-0A49-EE96-48BB-14982220AA48";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/";
	setAttr -k off ".v";
	setAttr ".ove" yes;
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
createNode nurbsCurve -n "Nose_A_Guide_Guide_Ctrl_CtrlShape" -p "Nose_A_Guide_Guide";
	rename -uid "5ABCC87D-C04D-DDFD-8EE1-72977DC3F993";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/";
	setAttr -k off ".v";
	setAttr ".ove" yes;
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
createNode nurbsCurve -n "Nose_A_Guide_Guide_Ctrl_Ctrl_CtrlShape" -p "Nose_A_Guide_Guide";
	rename -uid "9B59E446-D34E-E842-5440-E4AAA7CFA3FD";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 13;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 9 0 no 3
		10 0 1 2 3 4 5 6 7 8 9
		10
		-0.49999999999999994 -0.25000000000000011 -1.3977300000111021e-05
		0.94513100000000017 -0.25591599999999975 -1.3977299999790138e-05
		0.73965300000000012 -0.50644299999999987 -1.3977299999835763e-05
		0.99018000000000017 -0.93915099999999974 -1.3977299999780135e-05
		2.299302 -3.8742999948945234e-07 -1.3798499999489453e-05
		0.99018099999999976 0.93915100000000018 -1.3977299999780135e-05
		0.73965299999999989 0.50644200000000006 -1.3977299999835763e-05
		0.94513099999999994 0.2532210000000002 -7.1674599997901393e-06
		-0.5 0.24999999999999989 -1.3977300000111021e-05
		-0.49999999999999994 -0.25000000000000011 -1.3977300000111021e-05
		;
createNode nurbsCurve -n "Nose_A_Guide_Guide_Ctrl_Ctrl_Ctrl_CtrlShape" -p "Nose_A_Guide_Guide";
	rename -uid "1981FBB3-CB48-ACA8-DBFF-B3AD250AB9DA";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 6;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 9 0 no 3
		10 0 1 2 3 4 5 6 7 8 9
		10
		0.25000000000000011 1.3977299999944488e-05 -0.49999999999999994
		0.25591599999999975 1.3977299999943175e-05 0.94513100000000017
		0.50644299999999987 1.3977299999887547e-05 0.73965300000000012
		0.93915099999999974 1.3977299999791466e-05 0.99018000000000017
		3.8742999948945541e-07 1.37985e-05 2.299302
		-0.93915100000000018 1.3977300000208532e-05 0.99018099999999976
		-0.50644200000000006 1.3977300000112451e-05 0.73965299999999989
		-0.2532210000000002 7.1674600000562262e-06 0.94513099999999994
		-0.24999999999999989 1.397730000005551e-05 -0.5
		0.25000000000000011 1.3977299999944488e-05 -0.49999999999999994
		;
createNode dagContainer -n "L_Lip_Block" -p "face";
	rename -uid "11E780D6-B94E-2634-97DE-FC8EFA59B586";
	addAttr -ci true -sn "nts" -ln "notes" -dt "string";
	setAttr ".isc" yes;
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/Chain.png";
	setAttr ".ctor" -type "string" "estebanrdgz";
	setAttr ".cdat" -type "string" "2025/09/04 19:06:58";
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
		"['R_Lip_B_Bnd_Bnd_parentConstraint1', 'R_Lip_A_Ctrl', 'R_Lip_B_Ctrl_Offset_Grp', 'R_Lip_B_Jnt_Jnt_scaleConstraint1', 'L_Lip_A_Bnd_Bnd_parentConstraint1', 'R_Lip_B_CtrlShape', 'L_Lip_A_Ctrl_Offset_Grp', 'L_Lip_A_Jnt_Jnt_parentConstraint1', 'L_Lip_B_Bnd_Bnd_parentConstraint1', 'R_Lip_A_Jnt_Jnt', 'R_Lip_B_Bnd_Bnd', 'R_Lip_B_Ctrl', 'L_Lip_A_Jnt_Jnt_scaleConstraint1', 'L_Lip_B_Bnd_Bnd_scaleConstraint1', 'R_Lip_A_Bnd_Bnd', 'R_Lip_A_CtrlShape', 'R_Lip_B_Bnd_Bnd_scaleConstraint1', 'L_Lip_B_Jnt_Jnt_Ctrl_tag', 'L_Lip_B_Jnt_Jnt_scaleConstraint1', 'L_Lip_Rig_Grp', 'L_Lip_A_Bnd_Bnd', 'L_Lip_B_CtrlShape', 'L_Lip_B_Ctrl', 'R_Lip_A_Bnd_Bnd_scaleConstraint1', 'R_Lip_A_Ctrl_Offset_Grp_parentConstraint1', 'L_Lip_B_Jnt_Jnt', 'L_Lip_A_Bnd_Bnd_scaleConstraint1', 'R_Lip_A_Jnt_Jnt_scaleConstraint1', 'L_Lip_A_Ctrl', 'L_Lip_A_CtrlShape', 'R_Lip_A_Jnt_Jnt_parentConstraint1', 'R_Lip_B_Jnt_Jnt', 'R_Lip_A_Jnt_Jnt_Ctrl_tag', 'R_Lip_A_Ctrl_Offset_Grp', 'L_Lip_A_Jnt_Jnt_Ctrl_tag', 'L_Lip_B_Ctrl_Offset_Grp', 'R_Lip_A_Bnd_Bnd_parentConstraint1', 'L_Lip_A_Jnt_Jnt', 'L_Lip_A_Ctrl_Offset_Grp_parentConstraint1', 'R_Lip_B_Jnt_Jnt_Ctrl_tag', 'L_Lip_Ctrl_Grp', 'L_Lip_B_Bnd_Bnd', 'R_Lip_B_Jnt_Jnt_parentConstraint1', 'L_Lip_B_Jnt_Jnt_parentConstraint1']");
createNode joint -n "L_Lip_A_Guide_Guide" -p "L_Lip_Block";
	rename -uid "CA3CC30E-8C4D-7F8A-5861-969A67DCB95C";
	addAttr -ci true -sn "Helper" -ln "Helper" -min 0 -max 1 -en "Hide:Show" -at "enum";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/";
	setAttr ".t" -type "double3" 1.270459427805321 1.402303259345075 140.59601764904937 ;
	setAttr ".r" -type "double3" 0 43.628913765436899 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 -75.000000000000028 0 ;
	setAttr -cb on ".Helper" 1;
createNode nurbsCurve -n "L_Lip_A_Guide_Guide_CtrlShape" -p "L_Lip_A_Guide_Guide";
	rename -uid "4BD5C0AB-5A4A-37B1-CAA1-A2B323BB998B";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/";
	setAttr -k off ".v";
	setAttr ".ove" yes;
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
createNode nurbsCurve -n "L_Lip_A_Guide_Guide_Ctrl_CtrlShape" -p "L_Lip_A_Guide_Guide";
	rename -uid "B2F4FCA0-2243-0747-6920-C59C80C0E098";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/";
	setAttr -k off ".v";
	setAttr ".ove" yes;
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
createNode nurbsCurve -n "L_Lip_A_Guide_Guide_Ctrl_Ctrl_CtrlShape" -p "L_Lip_A_Guide_Guide";
	rename -uid "375A67B0-2C48-8FBB-915F-048AD28472CA";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 13;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 9 0 no 3
		10 0 1 2 3 4 5 6 7 8 9
		10
		-0.49999999999999994 -0.25000000000000011 -1.3977300000111021e-05
		0.94513100000000017 -0.25591599999999975 -1.3977299999790138e-05
		0.73965300000000012 -0.50644299999999987 -1.3977299999835763e-05
		0.99018000000000017 -0.93915099999999974 -1.3977299999780135e-05
		2.299302 -3.8742999948945234e-07 -1.3798499999489453e-05
		0.99018099999999976 0.93915100000000018 -1.3977299999780135e-05
		0.73965299999999989 0.50644200000000006 -1.3977299999835763e-05
		0.94513099999999994 0.2532210000000002 -7.1674599997901393e-06
		-0.5 0.24999999999999989 -1.3977300000111021e-05
		-0.49999999999999994 -0.25000000000000011 -1.3977300000111021e-05
		;
createNode nurbsCurve -n "L_Lip_A_Guide_Guide_Ctrl_Ctrl_Ctrl_CtrlShape" -p "L_Lip_A_Guide_Guide";
	rename -uid "8B0A65DE-EE4C-83D8-05B6-D694456172E1";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 6;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 9 0 no 3
		10 0 1 2 3 4 5 6 7 8 9
		10
		0.25000000000000011 1.3977299999944488e-05 -0.49999999999999994
		0.25591599999999975 1.3977299999943175e-05 0.94513100000000017
		0.50644299999999987 1.3977299999887547e-05 0.73965300000000012
		0.93915099999999974 1.3977299999791466e-05 0.99018000000000017
		3.8742999948945541e-07 1.37985e-05 2.299302
		-0.93915100000000018 1.3977300000208532e-05 0.99018099999999976
		-0.50644200000000006 1.3977300000112451e-05 0.73965299999999989
		-0.2532210000000002 7.1674600000562262e-06 0.94513099999999994
		-0.24999999999999989 1.397730000005551e-05 -0.5
		0.25000000000000011 1.3977299999944488e-05 -0.49999999999999994
		;
createNode joint -n "L_Lip_B_Guide_Guide" -p "L_Lip_A_Guide_Guide";
	rename -uid "DB3FD0AA-B748-0945-5069-31B4E1D44D6B";
	addAttr -ci true -sn "Helper" -ln "Helper" -min 0 -max 1 -en "Hide:Show" -at "enum";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/";
	setAttr ".t" -type "double3" 17.725550934496297 -2.8421709430404007e-14 0 ;
	setAttr ".r" -type "double3" 0 -75.000000000000014 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 75.000000000000028 0 ;
	setAttr -cb on ".Helper" 1;
createNode nurbsCurve -n "L_Lip_B_Guide_Guide_CtrlShape" -p "L_Lip_B_Guide_Guide";
	rename -uid "C06AF7D6-D34D-18D4-5240-71A9EE2B64BC";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/";
	setAttr -k off ".v";
	setAttr ".ove" yes;
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
createNode nurbsCurve -n "L_Lip_B_Guide_Guide_Ctrl_CtrlShape" -p "L_Lip_B_Guide_Guide";
	rename -uid "1FF1BAD3-C64D-06F6-0FCC-B8867F143DB0";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/";
	setAttr -k off ".v";
	setAttr ".ove" yes;
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
createNode nurbsCurve -n "L_Lip_B_Guide_Guide_Ctrl_Ctrl_CtrlShape" -p "L_Lip_B_Guide_Guide";
	rename -uid "F66E1439-8347-D0C8-7FC7-C0A924446516";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 13;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 9 0 no 3
		10 0 1 2 3 4 5 6 7 8 9
		10
		-0.49999999999999994 -0.25000000000000011 -1.3977300000111021e-05
		0.94513100000000017 -0.25591599999999975 -1.3977299999790138e-05
		0.73965300000000012 -0.50644299999999987 -1.3977299999835763e-05
		0.99018000000000017 -0.93915099999999974 -1.3977299999780135e-05
		2.299302 -3.8742999948945234e-07 -1.3798499999489453e-05
		0.99018099999999976 0.93915100000000018 -1.3977299999780135e-05
		0.73965299999999989 0.50644200000000006 -1.3977299999835763e-05
		0.94513099999999994 0.2532210000000002 -7.1674599997901393e-06
		-0.5 0.24999999999999989 -1.3977300000111021e-05
		-0.49999999999999994 -0.25000000000000011 -1.3977300000111021e-05
		;
createNode nurbsCurve -n "L_Lip_B_Guide_Guide_Ctrl_Ctrl_Ctrl_CtrlShape" -p "L_Lip_B_Guide_Guide";
	rename -uid "6A42DC76-AE4E-5B18-EBA9-69B410619FB2";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 6;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 9 0 no 3
		10 0 1 2 3 4 5 6 7 8 9
		10
		0.25000000000000011 1.3977299999944488e-05 -0.49999999999999994
		0.25591599999999975 1.3977299999943175e-05 0.94513100000000017
		0.50644299999999987 1.3977299999887547e-05 0.73965300000000012
		0.93915099999999974 1.3977299999791466e-05 0.99018000000000017
		3.8742999948945541e-07 1.37985e-05 2.299302
		-0.93915100000000018 1.3977300000208532e-05 0.99018099999999976
		-0.50644200000000006 1.3977300000112451e-05 0.73965299999999989
		-0.2532210000000002 7.1674600000562262e-06 0.94513099999999994
		-0.24999999999999989 1.397730000005551e-05 -0.5
		0.25000000000000011 1.3977299999944488e-05 -0.49999999999999994
		;
createNode dagContainer -n "UprLip_Block" -p "face";
	rename -uid "4EB6E91E-8344-6763-FFAA-C183F37D3E09";
	addAttr -ci true -sn "nts" -ln "notes" -dt "string";
	setAttr ".isc" yes;
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/Chain.png";
	setAttr ".ctor" -type "string" "estebanrdgz";
	setAttr ".cdat" -type "string" "2025/09/04 19:07:14";
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
	setAttr ".nts" -type "string" "['UprLip_A_Ctrl', 'UprLip_A_Jnt_Jnt_parentConstraint1', 'UprLip_Ctrl_Grp', 'UprLip_A_Bnd_Bnd', 'UprLip_A_CtrlShape', 'UprLip_Rig_Grp', 'UprLip_A_Ctrl_Offset_Grp_parentConstraint1', 'UprLip_A_Bnd_Bnd_scaleConstraint1', 'UprLip_A_Jnt_Jnt_scaleConstraint1', 'UprLip_A_Jnt_Jnt', 'UprLip_A_Ctrl_Offset_Grp', 'UprLip_A_Jnt_Jnt_Ctrl_tag', 'UprLip_A_Bnd_Bnd_parentConstraint1']";
createNode joint -n "UprLip_A_Guide_Guide" -p "UprLip_Block";
	rename -uid "E99A5DC0-1942-CBAE-0F59-68AF7B8ED458";
	addAttr -ci true -sn "Helper" -ln "Helper" -min 0 -max 1 -en "Hide:Show" -at "enum";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/";
	setAttr ".t" -type "double3" 0 9.1100144468180133 163.83911830554462 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr -cb on ".Helper" 1;
createNode nurbsCurve -n "UprLip_A_Guide_Guide_CtrlShape" -p "UprLip_A_Guide_Guide";
	rename -uid "66FA74F3-4541-542A-C851-E18EA9894BA1";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/";
	setAttr -k off ".v";
	setAttr ".ove" yes;
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
createNode nurbsCurve -n "UprLip_A_Guide_Guide_Ctrl_CtrlShape" -p "UprLip_A_Guide_Guide";
	rename -uid "7B491E83-8E4F-4A64-58E5-88818756F82F";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/";
	setAttr -k off ".v";
	setAttr ".ove" yes;
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
createNode nurbsCurve -n "UprLip_A_Guide_Guide_Ctrl_Ctrl_CtrlShape" -p "UprLip_A_Guide_Guide";
	rename -uid "EAE6EC61-7949-5D03-1A1D-919A367A966E";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 13;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 9 0 no 3
		10 0 1 2 3 4 5 6 7 8 9
		10
		-0.49999999999999994 -0.25000000000000011 -1.3977300000111021e-05
		0.94513100000000017 -0.25591599999999975 -1.3977299999790138e-05
		0.73965300000000012 -0.50644299999999987 -1.3977299999835763e-05
		0.99018000000000017 -0.93915099999999974 -1.3977299999780135e-05
		2.299302 -3.8742999948945234e-07 -1.3798499999489453e-05
		0.99018099999999976 0.93915100000000018 -1.3977299999780135e-05
		0.73965299999999989 0.50644200000000006 -1.3977299999835763e-05
		0.94513099999999994 0.2532210000000002 -7.1674599997901393e-06
		-0.5 0.24999999999999989 -1.3977300000111021e-05
		-0.49999999999999994 -0.25000000000000011 -1.3977300000111021e-05
		;
createNode nurbsCurve -n "UprLip_A_Guide_Guide_Ctrl_Ctrl_Ctrl_CtrlShape" -p "UprLip_A_Guide_Guide";
	rename -uid "2E7BFB31-E946-7150-7477-22A276A025C4";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 6;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 9 0 no 3
		10 0 1 2 3 4 5 6 7 8 9
		10
		0.25000000000000011 1.3977299999944488e-05 -0.49999999999999994
		0.25591599999999975 1.3977299999943175e-05 0.94513100000000017
		0.50644299999999987 1.3977299999887547e-05 0.73965300000000012
		0.93915099999999974 1.3977299999791466e-05 0.99018000000000017
		3.8742999948945541e-07 1.37985e-05 2.299302
		-0.93915100000000018 1.3977300000208532e-05 0.99018099999999976
		-0.50644200000000006 1.3977300000112451e-05 0.73965299999999989
		-0.2532210000000002 7.1674600000562262e-06 0.94513099999999994
		-0.24999999999999989 1.397730000005551e-05 -0.5
		0.25000000000000011 1.3977299999944488e-05 -0.49999999999999994
		;
createNode dagContainer -n "LwrLip_Block" -p "face";
	rename -uid "33685C1F-1A4B-244A-318B-2FBAE31955C3";
	addAttr -ci true -sn "nts" -ln "notes" -dt "string";
	setAttr ".isc" yes;
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/Chain.png";
	setAttr ".ctor" -type "string" "estebanrdgz";
	setAttr ".cdat" -type "string" "2025/09/04 19:07:19";
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
	setAttr ".nts" -type "string" "['LwrLip_A_Jnt_Jnt_scaleConstraint1', 'LwrLip_A_Bnd_Bnd_scaleConstraint1', 'LwrLip_A_Bnd_Bnd', 'LwrLip_A_Ctrl', 'LwrLip_Ctrl_Grp', 'LwrLip_A_Jnt_Jnt_Ctrl_tag', 'LwrLip_A_Jnt_Jnt_parentConstraint1', 'LwrLip_A_Bnd_Bnd_parentConstraint1', 'LwrLip_A_Ctrl_Offset_Grp', 'LwrLip_A_CtrlShape', 'LwrLip_A_Jnt_Jnt', 'LwrLip_Rig_Grp', 'LwrLip_A_Ctrl_Offset_Grp_parentConstraint1']";
createNode joint -n "LwrLip_A_Guide_Guide" -p "LwrLip_Block";
	rename -uid "6CDF01F0-364B-AFB5-DCD7-0C9155198FB5";
	addAttr -ci true -sn "Helper" -ln "Helper" -min 0 -max 1 -en "Hide:Show" -at "enum";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/";
	setAttr ".t" -type "double3" 0 -5.894293372908777 160.04139565590998 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr -cb on ".Helper" 1;
createNode nurbsCurve -n "LwrLip_A_Guide_Guide_CtrlShape" -p "LwrLip_A_Guide_Guide";
	rename -uid "9A6FA0C3-9E49-7C91-7911-DFA0D235D728";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/";
	setAttr -k off ".v";
	setAttr ".ove" yes;
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
createNode nurbsCurve -n "LwrLip_A_Guide_Guide_Ctrl_CtrlShape" -p "LwrLip_A_Guide_Guide";
	rename -uid "85CA54AB-E440-9899-23D3-F2BACA23920D";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/";
	setAttr -k off ".v";
	setAttr ".ove" yes;
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
createNode nurbsCurve -n "LwrLip_A_Guide_Guide_Ctrl_Ctrl_CtrlShape" -p "LwrLip_A_Guide_Guide";
	rename -uid "722D0733-C04B-E113-6888-BE89A7FDEC75";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 13;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 9 0 no 3
		10 0 1 2 3 4 5 6 7 8 9
		10
		-0.49999999999999994 -0.25000000000000011 -1.3977300000111021e-05
		0.94513100000000017 -0.25591599999999975 -1.3977299999790138e-05
		0.73965300000000012 -0.50644299999999987 -1.3977299999835763e-05
		0.99018000000000017 -0.93915099999999974 -1.3977299999780135e-05
		2.299302 -3.8742999948945234e-07 -1.3798499999489453e-05
		0.99018099999999976 0.93915100000000018 -1.3977299999780135e-05
		0.73965299999999989 0.50644200000000006 -1.3977299999835763e-05
		0.94513099999999994 0.2532210000000002 -7.1674599997901393e-06
		-0.5 0.24999999999999989 -1.3977300000111021e-05
		-0.49999999999999994 -0.25000000000000011 -1.3977300000111021e-05
		;
createNode nurbsCurve -n "LwrLip_A_Guide_Guide_Ctrl_Ctrl_Ctrl_CtrlShape" -p "LwrLip_A_Guide_Guide";
	rename -uid "9C3C7757-DB4D-AD97-372F-53B3C74BBE4E";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 6;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 9 0 no 3
		10 0 1 2 3 4 5 6 7 8 9
		10
		0.25000000000000011 1.3977299999944488e-05 -0.49999999999999994
		0.25591599999999975 1.3977299999943175e-05 0.94513100000000017
		0.50644299999999987 1.3977299999887547e-05 0.73965300000000012
		0.93915099999999974 1.3977299999791466e-05 0.99018000000000017
		3.8742999948945541e-07 1.37985e-05 2.299302
		-0.93915100000000018 1.3977300000208532e-05 0.99018099999999976
		-0.50644200000000006 1.3977300000112451e-05 0.73965299999999989
		-0.2532210000000002 7.1674600000562262e-06 0.94513099999999994
		-0.24999999999999989 1.397730000005551e-05 -0.5
		0.25000000000000011 1.3977299999944488e-05 -0.49999999999999994
		;
createNode dagContainer -n "Jaw_Block" -p "face";
	rename -uid "BC98098B-CE4E-F77F-22E3-B2A335918246";
	addAttr -ci true -sn "nts" -ln "notes" -dt "string";
	setAttr ".isc" yes;
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/Chain.png";
	setAttr ".ctor" -type "string" "estebanrdgz";
	setAttr ".cdat" -type "string" "2025/09/04 19:07:29";
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
	setAttr ".nts" -type "string" "['Jaw_A_Jnt_Jnt_parentConstraint1', 'Jaw_A_Bnd_Bnd_parentConstraint1', 'Jaw_Ctrl_Grp', 'Jaw_A_Jnt_Jnt_scaleConstraint1', 'Jaw_A_CtrlShape', 'Jaw_A_Ctrl_Offset_Grp', 'Jaw_A_Jnt_Jnt_Ctrl_tag', 'Jaw_A_Ctrl', 'Jaw_A_Ctrl_Offset_Grp_parentConstraint1', 'Jaw_A_Jnt_Jnt', 'Jaw_A_Bnd_Bnd_scaleConstraint1', 'Jaw_Rig_Grp', 'Jaw_A_Bnd_Bnd']";
createNode joint -n "Jaw_A_Guide_Guide" -p "Jaw_Block";
	rename -uid "8827C931-FC4C-0667-D3F0-00B0EE78FBE5";
	addAttr -ci true -sn "Helper" -ln "Helper" -min 0 -max 1 -en "Hide:Show" -at "enum";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/";
	setAttr ".t" -type "double3" 0 13.862563067532079 122.30066256049606 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr -cb on ".Helper" 1;
createNode nurbsCurve -n "Jaw_A_Guide_Guide_CtrlShape" -p "Jaw_A_Guide_Guide";
	rename -uid "77624EED-2D40-CFDB-55DC-19AF28DADBB0";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/";
	setAttr -k off ".v";
	setAttr ".ove" yes;
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
createNode nurbsCurve -n "Jaw_A_Guide_Guide_Ctrl_CtrlShape" -p "Jaw_A_Guide_Guide";
	rename -uid "AB4D020E-3C4E-4B39-16F1-FD8C98990C31";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/";
	setAttr -k off ".v";
	setAttr ".ove" yes;
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
createNode nurbsCurve -n "Jaw_A_Guide_Guide_Ctrl_Ctrl_CtrlShape" -p "Jaw_A_Guide_Guide";
	rename -uid "74482B38-D542-9883-34C4-5894A23F013F";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 13;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 9 0 no 3
		10 0 1 2 3 4 5 6 7 8 9
		10
		-0.49999999999999994 -0.25000000000000011 -1.3977300000111021e-05
		0.94513100000000017 -0.25591599999999975 -1.3977299999790138e-05
		0.73965300000000012 -0.50644299999999987 -1.3977299999835763e-05
		0.99018000000000017 -0.93915099999999974 -1.3977299999780135e-05
		2.299302 -3.8742999948945234e-07 -1.3798499999489453e-05
		0.99018099999999976 0.93915100000000018 -1.3977299999780135e-05
		0.73965299999999989 0.50644200000000006 -1.3977299999835763e-05
		0.94513099999999994 0.2532210000000002 -7.1674599997901393e-06
		-0.5 0.24999999999999989 -1.3977300000111021e-05
		-0.49999999999999994 -0.25000000000000011 -1.3977300000111021e-05
		;
createNode nurbsCurve -n "Jaw_A_Guide_Guide_Ctrl_Ctrl_Ctrl_CtrlShape" -p "Jaw_A_Guide_Guide";
	rename -uid "E950CC9B-9540-914D-D514-2888C1A3E865";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 6;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 9 0 no 3
		10 0 1 2 3 4 5 6 7 8 9
		10
		0.25000000000000011 1.3977299999944488e-05 -0.49999999999999994
		0.25591599999999975 1.3977299999943175e-05 0.94513100000000017
		0.50644299999999987 1.3977299999887547e-05 0.73965300000000012
		0.93915099999999974 1.3977299999791466e-05 0.99018000000000017
		3.8742999948945541e-07 1.37985e-05 2.299302
		-0.93915100000000018 1.3977300000208532e-05 0.99018099999999976
		-0.50644200000000006 1.3977300000112451e-05 0.73965299999999989
		-0.2532210000000002 7.1674600000562262e-06 0.94513099999999994
		-0.24999999999999989 1.397730000005551e-05 -0.5
		0.25000000000000011 1.3977299999944488e-05 -0.49999999999999994
		;
createNode dagContainer -n "L_Cheek_Block" -p "face";
	rename -uid "A355D953-1748-8B39-C101-5F954DA0C0C9";
	addAttr -ci true -sn "nts" -ln "notes" -dt "string";
	setAttr ".isc" yes;
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/Chain.png";
	setAttr ".ctor" -type "string" "estebanrdgz";
	setAttr ".cdat" -type "string" "2025/09/05 09:44:08";
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
	setAttr ".nts" -type "string" "['R_Cheek_Bnd_Bnd_parentConstraint1', 'R_Cheek_CtrlShape', 'R_Cheek_Jnt_Jnt_parentConstraint1', 'R_Cheek_Bnd_Bnd', 'L_Cheek_Bnd_Bnd', 'R_Cheek_Jnt_Jnt_scaleConstraint1', 'L_Cheek_Ctrl_Grp', 'L_Cheek_Bnd_Bnd_scaleConstraint1', 'L_Cheek_Bnd_Bnd_parentConstraint1', 'R_Cheek_Bnd_Bnd_scaleConstraint1', 'L_Cheek_Ctrl', 'R_Cheek_Ctrl_Offset_Grp', 'R_Cheek_Ctrl', 'R_Cheek_Ctrl_Offset_Grp_parentConstraint1', 'L_Cheek_CtrlShape', 'L_Cheek_Ctrl_Offset_Grp', 'R_Cheek_Jnt_Jnt_Ctrl_tag', 'L_Cheek_Ctrl_Offset_Grp_parentConstraint1', 'L_Cheek_Jnt_Jnt_parentConstraint1', 'R_Cheek_Jnt_Jnt', 'L_Cheek_Jnt_Jnt', 'L_Cheek_Jnt_Jnt_scaleConstraint1', 'L_Cheek_Rig_Grp', 'L_Cheek_Jnt_Jnt_Ctrl_tag']";
createNode joint -n "L_Cheek_Guide_Guide" -p "L_Cheek_Block";
	rename -uid "07FEF3DF-0C42-E21A-4C90-40864A23D7AA";
	addAttr -ci true -sn "Helper" -ln "Helper" -min 0 -max 1 -en "Hide:Show" -at "enum";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/";
	setAttr ".t" -type "double3" 15.552401703035336 6.9987977614416366 143.64400837641239 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr -cb on ".Helper" 1;
createNode nurbsCurve -n "L_Cheek_Guide_Guide_CtrlShape" -p "L_Cheek_Guide_Guide";
	rename -uid "69FA2242-3146-BB20-7A7F-D5B593B52278";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/";
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
createNode nurbsCurve -n "L_Cheek_Guide_Guide_Ctrl_CtrlShape" -p "L_Cheek_Guide_Guide";
	rename -uid "6E66F0AC-944F-2E9B-A620-5BAA179B8EB3";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/";
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
createNode nurbsCurve -n "L_Cheek_Guide_Guide_Ctrl_Ctrl_CtrlShape" -p "L_Cheek_Guide_Guide";
	rename -uid "3A83DBDA-EE49-9B83-F591-CD900E3F7AB5";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".hpb" yes;
	setAttr ".ovc" 13;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 9 0 no 3
		10 0 1 2 3 4 5 6 7 8 9
		10
		-0.49999999999999994 -0.25000000000000011 -1.3977300000111021e-05
		0.94513100000000017 -0.25591599999999975 -1.3977299999790138e-05
		0.73965300000000012 -0.50644299999999987 -1.3977299999835763e-05
		0.99018000000000017 -0.93915099999999974 -1.3977299999780135e-05
		2.299302 -3.8742999948945234e-07 -1.3798499999489453e-05
		0.99018099999999976 0.93915100000000018 -1.3977299999780135e-05
		0.73965299999999989 0.50644200000000006 -1.3977299999835763e-05
		0.94513099999999994 0.2532210000000002 -7.1674599997901393e-06
		-0.5 0.24999999999999989 -1.3977300000111021e-05
		-0.49999999999999994 -0.25000000000000011 -1.3977300000111021e-05
		;
createNode nurbsCurve -n "L_Cheek_Guide_Guide_Ctrl_Ctrl_Ctrl_CtrlShape" -p "L_Cheek_Guide_Guide";
	rename -uid "5AA319AF-CF41-E089-83EA-AC81CAC21FB4";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".hpb" yes;
	setAttr ".ovc" 6;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 9 0 no 3
		10 0 1 2 3 4 5 6 7 8 9
		10
		0.25000000000000011 1.3977299999944488e-05 -0.49999999999999994
		0.25591599999999975 1.3977299999943175e-05 0.94513100000000017
		0.50644299999999987 1.3977299999887547e-05 0.73965300000000012
		0.93915099999999974 1.3977299999791466e-05 0.99018000000000017
		3.8742999948945541e-07 1.37985e-05 2.299302
		-0.93915100000000018 1.3977300000208532e-05 0.99018099999999976
		-0.50644200000000006 1.3977300000112451e-05 0.73965299999999989
		-0.2532210000000002 7.1674600000562262e-06 0.94513099999999994
		-0.24999999999999989 1.397730000005551e-05 -0.5
		0.25000000000000011 1.3977299999944488e-05 -0.49999999999999994
		;
createNode dagContainer -n "CreateSkl_Block" -p "face";
	rename -uid "5E54D1BB-6E4C-BB1D-43F8-C0BA5D314880";
	addAttr -ci true -sn "nts" -ln "notes" -dt "string";
	setAttr ".isc" yes;
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/BodyGames.png";
	setAttr ".ctor" -type "string" "estebanrdgz";
	setAttr ".cdat" -type "string" "2025/09/04 21:29:14";
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
		"['R_Cheek_Skl_Skl_parentConstraint1', 'L_Cheek_Skl_Skl_parentConstraint1', 'L_Eyelids_Up__cv3_Skl_parentConstraint1', 'Nose_A_Skl_Skl', 'R_Brow_2_Skl', 'UprLip_A_Skl_Skl_parentConstraint1', 'Nose_A_Skl_Skl_parentConstraint1', 'R_Lip_A_Skl_Skl_parentConstraint1', 'R_Eyelids_Up__cv3_Skl_parentConstraint1', 'L_Eyelids_Dw__cv3_Skl_parentConstraint1', 'L_Brow_0_Skl_parentConstraint1', 'L_Eyelids_Up__cv3_Skl', 'Skeleton', 'R_Ear_A_Skl_Skl_parentConstraint1', 'R_Ear_A_Skl_Skl', 'R_Brow_1_Skl_parentConstraint1', 'L_Cheek_Skl_Skl', 'R_Eyelids_Dw__cv3_Skl_parentConstraint1', 'L_Brow_1_Skl', 'UprLip_A_Skl_Skl', 'R_Cheek_Skl_Skl', 'R_Brow_3_Skl_parentConstraint1', 'L_Brow_2_Skl_parentConstraint1', 'R_Eyelids_Up__cv3_Skl', 'L_Ear_A_Skl_Skl', 'L_Lip_A_Skl_Skl', 'R_Brow_0_Skl', 'L_Brow_1_Skl_parentConstraint1', 'LwrLip_A_Skl_Skl_parentConstraint1', 'L_Brow_0_Skl', 'L_Brow_4_Skl', 'L_Brow_3_Skl', 'R_Brow_2_Skl_parentConstraint1', 'R_Eyelids_Dw__cv3_Skl', 'R_Brow_0_Skl_parentConstraint1', 'R_Lip_A_Skl_Skl', 'L_Lip_B_Skl_Skl', 'L_Lip_A_Skl_Skl_parentConstraint1', 'R_Lip_B_Skl_Skl_parentConstraint1', 'L_Brow_2_Skl', 'R_Brow_4_Skl', 'L_Brow_3_Skl_parentConstraint1', 'L_Lip_B_Skl_Skl_parentConstraint1', 'L_Eyelids_Dw__cv3_Skl', 'R_Brow_1_Skl', 'R_Lip_B_Skl_Skl', 'Root_Skl_parentConstraint1', 'Jaw_A_Skl_Skl_parentConstraint1', 'Root_Skl_scaleConstraint1', 'Root_Bnd_parentConstraint1', 'Root_Skl', 'Jaw_A_Skl_Skl', 'L_Brow_4_Skl_parentConstraint1', 'R_Brow_4_Skl_parentConstraint1', 'R_Brow_3_Skl', 'L_Ear_A_Skl_Skl_parentConstraint1', 'LwrLip_A_Skl_Skl']");
createNode dagContainer -n "CleanCustomFace_Block" -p "face";
	rename -uid "3658BC3B-3E48-D505-8E36-CAB8D5DBCDE2";
	addAttr -ci true -sn "nts" -ln "notes" -dt "string";
	setAttr ".isc" yes;
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/CODE.png";
	setAttr ".ctor" -type "string" "estebanrdgz";
	setAttr ".cdat" -type "string" "2025/09/04 19:07:45";
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
	setAttr ".nts" -type "string" "['R_Cheek_Skl', 'R_Lip_CtrlShape', 'R_Lip_A_Skl', 'L_Lip_A_Skl', 'LwrLip_Ctrl', 'L_Ear_Ctrl', 'L_Ear_A_Skl', 'R_Ear_A_Skl', 'R_Eyelids_Up_Skl', 'L_Cheek_Skl', 'L_Lip_CtrlShape', 'R_Lip_Ctrl', 'UprLip_Ctrl', 'L_Eyelids_Up_Skl', 'L_Eyelids_Dw_Skl', 'Jaw_A_Skl', 'Nose_A_Skl', 'Nose_Ctrl', 'LwrLip_A_Skl', 'R_Ear_Ctrl', 'UprLip_A_Skl', 'UprLip_CtrlShape', 'Nose_CtrlShape', 'R_Ear_CtrlShape', 'R_Eyelids_Dw_Skl', 'L_Ear_CtrlShape', 'L_Lip_Ctrl', 'LwrLip_CtrlShape']";
createNode transform -n "CleanCustomFace_Loc" -p "CleanCustomFace_Block";
	rename -uid "0399AEC1-8344-9EA2-5CD9-B6853EB72E48";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/";
createNode locator -n "CleanCustomFace_LocShape" -p "CleanCustomFace_Loc";
	rename -uid "27A17DEE-C149-D2A3-DE2F-34BBA6B3C1D4";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/";
	setAttr -k off ".v";
createNode dagContainer -n "CreateAutomations_Block" -p "face";
	rename -uid "CA4D1EDC-D140-D2EF-6676-3AA092B5C296";
	addAttr -ci true -sn "nts" -ln "notes" -dt "string";
	setAttr ".isc" yes;
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/CODE.png";
	setAttr ".ctor" -type "string" "estebanrdgz";
	setAttr ".cdat" -type "string" "2025/09/04 19:07:50";
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
	setAttr ".nts" -type "string" "['L_Lip_Ctrl_Auto_Grp', 'LwrLip_Ctrl_Auto_Grp', 'R_Lip_Ctrl_Root_Grp', 'L_Lip_Ctrl_Auto_Grp_parentConstraint1', 'LwrLip_Ctrl_Auto_Grp_parentConstraint1', 'UprLip_Ctrl_Auto_Grp', 'LwrLip_Ctrl_Root_Grp', 'R_Cheek_Ctrl_Root_Grp', 'L_Lip_Ctrl_Root_Grp', 'UprLip_Ctrl_Root_Grp', 'R_Cheek_Ctrl_Auto_Grp_parentConstraint1', 'L_Cheek_Ctrl_Auto_Grp_parentConstraint1', 'L_Cheek_Ctrl_Root_Grp', 'R_Lip_Ctrl_Auto_Grp', 'R_Cheek_Ctrl_Auto_Grp', 'L_Cheek_Ctrl_Auto_Grp', 'R_Lip_Ctrl_Auto_Grp_parentConstraint1']";
createNode transform -n "CreateAutomations_Loc" -p "CreateAutomations_Block";
	rename -uid "A31057FE-F545-A2CF-4AD7-06980732F376";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/";
createNode locator -n "CreateAutomations_LocShape" -p "CreateAutomations_Loc";
	rename -uid "B20C931F-ED4D-3F81-A7DF-5F84E18254D1";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/";
	setAttr -k off ".v";
createNode transform -n "data" -p "Mutant_Build";
	rename -uid "80327511-EF44-1422-713A-AC9C8BBA5A88";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/";
	setAttr ".t" -type "double3" 0 148.19816716577168 0 ;
createNode dagContainer -n "Load_Ctrls_Block" -p "data";
	rename -uid "E157F936-5940-22A6-C3C7-EFA5776B2399";
	addAttr -ci true -sn "nts" -ln "notes" -dt "string";
	setAttr ".isc" yes;
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/Controller.png";
	setAttr ".ctor" -type "string" "esteban.rodriguez";
	setAttr ".cdat" -type "string" "2022/07/12 12:58:07";
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
createNode hyperLayout -n "hyperLayout8";
	rename -uid "8B579287-2547-D834-0F85-CA926766A321";
	setAttr ".ihi" 0;
createNode network -n "SausageFaceTemplate_BaseA_Config";
	rename -uid "9CC0E072-A741-4B57-CCC8-2DBD5ABEB2FC";
	addAttr -ci true -sn "precode" -ln "precode" -dt "string";
	addAttr -ci true -sn "Build_Command" -ln "Build_Command" -dt "string";
	addAttr -ci true -sn "Import_Command" -ln "Import_Command" -dt "string";
	addAttr -ci true -sn "CtrlColor" -ln "CtrlColor" -min 0 -max 7 -en "lightBlue:blue:white:purple:green:red:yellow:grey" 
		-at "enum";
	addAttr -ci true -sn "CtrlScale" -ln "CtrlScale" -dv 4 -min 1 -max 20 -at "long";
	addAttr -ci true -sn "Name" -ln "Name" -dt "string";
	addAttr -ci true -sn "postcode" -ln "postcode" -dt "string";
	setAttr ".precode" -type "string" "";
	setAttr -l on ".Build_Command" -type "string" "exec_baseA.build_baseA_block()";
	setAttr -l on ".Import_Command" -type "string" "import exec_baseA ";
	setAttr -cb on ".CtrlColor";
	setAttr -k on ".CtrlScale";
	setAttr ".Name" -type "string" "Mutant_Tools";
	setAttr ".postcode" -type "string" "";
createNode hyperLayout -n "hyperLayout7";
	rename -uid "318C2FFE-0D4C-A3AF-4FAD-D1988899995F";
	setAttr ".ihi" 0;
	setAttr -s 2 ".hyp";
createNode network -n "VisAttrs_Config";
	rename -uid "A9CE6DCC-9F48-A99A-4442-1FBD0E21273C";
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
	setAttr ".Code" -type "string" "from maya import cmds, mel\nvis_ctrl = cmds.duplicate('Vis_Guide', n ='Vis_Ctrl')\ncmds.parent('Vis_Ctrl', 'Ctrl_Grp')\n\n#mel.eval('setAttr -lock true -keyable false -channelBox false \"Vis_Ctrl.tx\";')\n#mel.eval('setAttr -lock true -keyable false -channelBox false \"Vis_Ctrl.ty\";')\n#mel.eval('setAttr -lock true -keyable false -channelBox false \"Vis_Ctrl.tz\";')\nmel.eval('setAttr -lock true -keyable false -channelBox false \"Vis_Ctrl.rx\";')\nmel.eval('setAttr -lock true -keyable false -channelBox false \"Vis_Ctrl.ry\";')\nmel.eval('setAttr -lock true -keyable false -channelBox false \"Vis_Ctrl.rz\";')\nmel.eval('setAttr -lock true -keyable false -channelBox false \"Vis_Ctrl.sx\";')\nmel.eval('setAttr -lock true -keyable false -channelBox false \"Vis_Ctrl.sy\";')\nmel.eval('setAttr -lock true -keyable false -channelBox false \"Vis_Ctrl.sz\";')\nmel.eval('setAttr -lock true -keyable false -channelBox false \"Vis_Ctrl.v\";')\n";
	setAttr ".postcode" -type "string" "";
createNode hyperLayout -n "hyperLayout51";
	rename -uid "9FC4349B-554B-3FB7-766F-8F9363B42B35";
	setAttr ".ihi" 0;
	setAttr -s 2 ".hyp";
createNode network -n "FakeParentAndRoot_Config";
	rename -uid "F1AF968F-3142-0BD2-108B-EB965797FDC7";
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
	setAttr ".Code" -type "string" "if not cmds.objExists('Head_Ctrl'):\n    cmds.spaceLocator(n='Head_Ctrl')\nif not cmds.objExists('Root_Bnd'):\n    cmds.select(cl=True)\n    cmds.joint(n='Root_Bnd') \n    cmds.parent('Root_Bnd','Bind_Joints_Grp')\n \n    \n    ";
	setAttr ".postcode" -type "string" "";
createNode hyperLayout -n "hyperLayout40";
	rename -uid "C39EF2E3-3B44-5BC2-7462-64947C9251C2";
	setAttr ".ihi" 0;
	setAttr -s 2 ".hyp";
createNode network -n "L_Brow_Config";
	rename -uid "7356B990-884F-F7A3-04DA-02ABF74BAB34";
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
	setAttr ".SetAttrsPosition" -type "string" "Vis_Ctrl";
	setAttr -k on ".CtrlSize";
	setAttr -cb on ".GameMode" yes;
	setAttr ".Help" -type "string" "Will crete brows rig system";
	setAttr ".postcode" -type "string" "";
createNode hyperLayout -n "hyperLayout41";
	rename -uid "C75F3937-0C43-FC00-FFD3-FEA95C4951DD";
	setAttr ".ihi" 0;
createNode network -n "L_Eyelids_Config";
	rename -uid "0B9361B1-3A4D-8ABC-7B3F-DB9E2F12746D";
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
	setAttr ".SetAttrsPosition" -type "string" "Vis_Ctrl";
	setAttr -cb on ".Mirror";
	setAttr ".SetUpperEdge" -type "string" "sloth_body_mesh.e[6047], sloth_body_mesh.e[6049], sloth_body_mesh.e[6051], sloth_body_mesh.e[6053], sloth_body_mesh.e[6055], sloth_body_mesh.e[6057], sloth_body_mesh.e[6059], sloth_body_mesh.e[6061]";
	setAttr ".SetLowerEdge" -type "string" "sloth_body_mesh.e[5992], sloth_body_mesh.e[6041], sloth_body_mesh.e[6043], sloth_body_mesh.e[6045], sloth_body_mesh.e[6063], sloth_body_mesh.e[6065:6066]";
	setAttr ".SetEyePivot" -type "string" "EyePivot";
	setAttr -k on ".CtrlSize";
	setAttr -cb on ".LimitCtrl";
	setAttr -cb on ".GameMode" yes;
	setAttr -cb on ".BindJoints" 2;
	setAttr ".Help" -type "string" "Create eyelids rig, based on Marco Giordano tutorial\n";
	setAttr ".postcode" -type "string" "";
createNode hyperLayout -n "hyperLayout42";
	rename -uid "B41C2CF6-BF41-C870-D0AF-D88F19E3B2DB";
	setAttr ".ihi" 0;
	setAttr -s 5 ".hyp";
createNode network -n "L_Ear_Config";
	rename -uid "9838C417-C648-8920-DEF6-39AF00CFE6BC";
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
	setAttr -cb on ".CtrlType" 4;
	setAttr -cb on ".TwistAxis";
	setAttr ".Help" -type "string" "Create a FK Chain";
	setAttr ".postcode" -type "string" "";
createNode hyperLayout -n "hyperLayout43";
	rename -uid "4755081C-5549-A6DC-F375-388872B21B15";
	setAttr ".ihi" 0;
	setAttr -s 5 ".hyp";
createNode network -n "Nose_Config";
	rename -uid "530B6AA9-B24C-35B5-F14B-C394F8E7FD04";
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
	setAttr -cb on ".CtrlType" 2;
	setAttr -cb on ".TwistAxis";
	setAttr ".Help" -type "string" "Create a FK Chain";
	setAttr ".postcode" -type "string" "";
createNode hyperLayout -n "hyperLayout44";
	rename -uid "A56FD1F6-6943-39E1-9672-86B480FB98D9";
	setAttr ".ihi" 0;
	setAttr -s 10 ".hyp";
createNode network -n "L_Lip_Config";
	rename -uid "9B2955CF-DD43-64E8-88E4-2C952F0B2FBA";
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
createNode hyperLayout -n "hyperLayout45";
	rename -uid "FE5E6EC7-FF49-ADF3-D54E-859AD676268C";
	setAttr ".ihi" 0;
	setAttr -s 5 ".hyp";
createNode network -n "UprLip_Config";
	rename -uid "06D955E9-2B4C-DDF1-08BC-EE9B27428F75";
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
createNode hyperLayout -n "hyperLayout46";
	rename -uid "7E21185E-0C4A-D567-073C-0DAA0BF96503";
	setAttr ".ihi" 0;
	setAttr -s 5 ".hyp";
createNode network -n "LwrLip_Config";
	rename -uid "83946571-014A-9AC8-5829-0196E1D7DA98";
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
createNode hyperLayout -n "hyperLayout47";
	rename -uid "E4C0B142-094D-8BEB-5204-43ABAA74D5FF";
	setAttr ".ihi" 0;
	setAttr -s 5 ".hyp";
createNode network -n "Jaw_Config";
	rename -uid "F9D4ECA2-FE47-EB4B-63B3-AC8FAB7F0EDC";
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
createNode hyperLayout -n "hyperLayout55";
	rename -uid "94DA1DC0-CE41-691B-9DC0-CBABA38D4094";
	setAttr ".ihi" 0;
	setAttr -s 5 ".hyp";
createNode network -n "L_Cheek_Config";
	rename -uid "C1555EEA-EC44-8843-1DBF-D9AAE03E83F3";
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
	setAttr -cb on ".CtrlType" 9;
	setAttr -cb on ".TwistAxis";
	setAttr ".Help" -type "string" "Create a FK Chain";
	setAttr ".postcode" -type "string" "";
createNode hyperLayout -n "hyperLayout53";
	rename -uid "EA819E88-BA43-0CA5-E668-839A70FC6365";
	setAttr ".ihi" 0;
createNode network -n "CreateSkl_Config";
	rename -uid "C6AE6DA5-2F49-CEF0-3D5C-28B40C9B1E86";
	addAttr -ci true -sn "precode" -ln "precode" -dt "string";
	addAttr -ci true -sn "Build_Command" -ln "Build_Command" -dt "string";
	addAttr -ci true -sn "Import_Command" -ln "Import_Command" -dt "string";
	addAttr -ci true -sn "Engine" -ln "Engine" -min 0 -max 1 -en "unity:unreal" -at "enum";
	addAttr -ci true -sn "Help" -ln "Help" -dt "string";
	addAttr -ci true -sn "postcode" -ln "postcode" -dt "string";
	setAttr ".precode" -type "string" "";
	setAttr -l on ".Build_Command" -type "string" "exec_convertbody.build_convertbody_block()";
	setAttr -l on ".Import_Command" -type "string" "import exec_convertbody";
	setAttr -cb on ".Engine";
	setAttr ".Help" -type "string" "Will convert Mutant Body Template to Games";
	setAttr ".postcode" -type "string" "";
createNode hyperLayout -n "hyperLayout48";
	rename -uid "7516A402-AB4F-A689-2C98-39B662C149EB";
	setAttr ".ihi" 0;
	setAttr -s 2 ".hyp";
createNode network -n "CleanCustomFace_Config";
	rename -uid "476C9E74-AF4E-0E78-E588-DBA7FF9257CC";
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
	setAttr ".Code" -type "string" "cmds.delete('L_Lip_B_Ctrl_Offset_Grp','R_Lip_B_Ctrl_Offset_Grp', 'L_Brow_1_Skl', 'L_Brow_3_Skl', 'R_Brow_1_Skl', 'R_Brow_3_Skl', 'L_Lip_B_Skl_Skl', 'R_Lip_B_Skl_Skl')\nnew_names = {\n'L_Lip_A_Ctrl':'L_Lip_Ctrl',\n'L_Brow_2_Skl': 'L_Brow_1_Skl',\n'L_Brow_4_Skl': 'L_Brow_2_Skl',\n'UprLip_A_Ctrl':'UprLip_Ctrl',\n'LwrLip_A_Ctrl':'LwrLip_Ctrl',\n'Nose_A_Ctrl':'Nose_Ctrl',\n'L_Ear_A_Ctrl':'L_Ear_Ctrl'\n\n}\n\nfor name in new_names:\n    cmds.rename(name, new_names[name])\n    if 'L_' in name:\n        cmds.rename(name.replace('L_', 'R_'), new_names[name].replace('L_', 'R_'))\n\n\ndouble_skl = cmds.ls('*_Skl_Skl')\nfor skl in double_skl:\n    cmds.rename(skl, skl.replace('_Skl_Skl', '_Skl'))\n    \ncmds.rename('R_Eyelids_Dw__cv3_Skl', 'R_Eyelids_Dw_Skl')\ncmds.rename('L_Eyelids_Dw__cv3_Skl', 'L_Eyelids_Dw_Skl')\ncmds.rename('R_Eyelids_Up__cv3_Skl', 'R_Eyelids_Up_Skl')\ncmds.rename('L_Eyelids_Up__cv3_Skl', 'L_Eyelids_Up_Skl')";
	setAttr ".postcode" -type "string" "";
createNode hyperLayout -n "hyperLayout49";
	rename -uid "18670CF8-D241-4F32-20EA-81AD6853A28E";
	setAttr ".ihi" 0;
	setAttr -s 2 ".hyp";
createNode network -n "CreateAutomations_Config";
	rename -uid "9A76AAB9-B048-7FD5-73BB-8BA371EFDFF3";
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
		"#Import Main Mutant Tools\nimport imp\nfrom imp import reload\nimport Mutant_Tools\nimport Mutant_Tools.Utils\nfrom Mutant_Tools.Utils.Rigging import main_mutant\nreload(Mutant_Tools.Utils.Rigging.main_mutant)\nmt = main_mutant.Mutant()\n\nmouth_ctrls = ['L_Lip_Ctrl','R_Lip_Ctrl','LwrLip_Ctrl','UprLip_Ctrl', 'L_Cheek_Ctrl', 'R_Cheek_Ctrl']\nfor ctrl in mouth_ctrls:\n    cmds.select(ctrl)\n    mt.root_grp(autoRoot=True)\n    \n\ncmds.parentConstraint('Jaw_A_Ctrl','LwrLip_Ctrl_Auto_Grp', mo=True)\ncmds.parentConstraint('Jaw_A_Ctrl','Head_Ctrl','L_Lip_Ctrl_Auto_Grp', mo=True)\ncmds.parentConstraint('Jaw_A_Ctrl','Head_Ctrl','R_Lip_Ctrl_Auto_Grp', mo=True)\ncmds.setAttr(\"L_Lip_Ctrl_Auto_Grp_parentConstraint1.interpType\", 2)\ncmds.setAttr(\"R_Lip_Ctrl_Auto_Grp_parentConstraint1.interpType\", 2)\n\n#CheeckAutomation\ncmds.parentConstraint('L_Lip_Ctrl','Head_Ctrl','L_Cheek_Ctrl_Auto_Grp', mo=True)\ncmds.setAttr(\"L_Cheek_Ctrl_Auto_Grp_parentConstraint1.interpType\", 2)\ncmds.setAttr (\"L_Cheek_Ctrl_Auto_Grp_parentConstraint1.Head_CtrlW1\", 3)\ncmds.parentConstraint('R_Lip_Ctrl','Head_Ctrl','R_Cheek_Ctrl_Auto_Grp', mo=True)\n"
		+ "cmds.setAttr(\"R_Cheek_Ctrl_Auto_Grp_parentConstraint1.interpType\", 2)\ncmds.setAttr (\"R_Cheek_Ctrl_Auto_Grp_parentConstraint1.Head_CtrlW1\", 3)\n");
	setAttr ".postcode" -type "string" "";
createNode hyperLayout -n "hyperLayout39";
	rename -uid "8C4760D7-5342-3C6A-5106-018B3110B8AD";
	setAttr ".ihi" 0;
createNode network -n "Load_Ctrls_Config";
	rename -uid "671E3F49-0F43-0AF8-4ACA-4A814C2483B1";
	addAttr -ci true -sn "precode" -ln "precode" -dt "string";
	addAttr -ci true -sn "Build_Command" -ln "Build_Command" -dt "string";
	addAttr -ci true -sn "Import_Command" -ln "Import_Command" -dt "string";
	addAttr -ci true -sn "File" -ln "File" -dt "string";
	addAttr -ci true -sn "Help" -ln "Help" -dt "string";
	addAttr -ci true -sn "postcode" -ln "postcode" -dt "string";
	setAttr ".precode" -type "string" "";
	setAttr -l on ".Build_Command" -type "string" "exec_load_ctrls.build_load_ctrls_block()";
	setAttr -l on ".Import_Command" -type "string" "import exec_load_ctrls";
	setAttr ".File" -type "string" "AG";
	setAttr ".Help" -type "string" "Load Ctrls Data from File, you can put show keys to define the default ones.";
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
	setAttr -k on ".cons";
	setAttr -k on ".vac";
	setAttr -av -k on ".hwi";
	setAttr -k on ".csvd";
	setAttr -av -k on ".ta" 5;
	setAttr -av -k on ".tq";
	setAttr -k on ".ts";
	setAttr -av -k on ".etmr";
	setAttr -av -k on ".tmr";
	setAttr -av -k on ".aoon" yes;
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
	setAttr -k on ".mbsc";
	setAttr -k on ".mbc";
	setAttr -k on ".mbfa";
	setAttr -k on ".mbftb";
	setAttr -k on ".mbftg";
	setAttr -k on ".mbftr";
	setAttr -av -k on ".mbfta";
	setAttr -k on ".mbfe";
	setAttr -k on ".mbme";
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
	setAttr -k on ".laa";
	setAttr -k on ".fprt" yes;
	setAttr -k on ".rtfm" 1;
select -ne :renderPartition;
	setAttr -av -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -av -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -s 9 ".st";
	setAttr -cb on ".an";
	setAttr -cb on ".pt";
select -ne :renderGlobalsList1;
	setAttr -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -k on ".nds";
	setAttr -cb on ".bnm";
select -ne :defaultShaderList1;
	setAttr -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -s 12 ".s";
select -ne :postProcessList1;
	setAttr -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -av -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -s 2 ".p";
select -ne :defaultRenderUtilityList1;
	setAttr -av -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -av -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -s 63 ".u";
select -ne :defaultRenderingList1;
	setAttr -av -k on ".cch";
	setAttr -k on ".ihi";
	setAttr -av -k on ".nds";
	setAttr -cb on ".bnm";
select -ne :defaultTextureList1;
	setAttr -av -k on ".cch";
	setAttr -k on ".fzn";
	setAttr -cb on ".ihi";
	setAttr -av -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -s 8 ".tx";
select -ne :standardSurface1;
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
	setAttr -s 3 ".dsm";
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
	setAttr -k on ".fzn";
	setAttr -cb on ".ihi";
	setAttr -av -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -k on ".bbx";
	setAttr -k on ".vwm";
	setAttr -k on ".tpv";
	setAttr -k on ".uit";
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
select -ne :defaultRenderGlobals;
	addAttr -ci true -h true -sn "dss" -ln "defaultSurfaceShader" -dt "string";
	setAttr -av -k on ".cch";
	setAttr -av -k on ".ihi";
	setAttr -av -k on ".nds";
	setAttr -k on ".bnm";
	setAttr -av -k on ".macc";
	setAttr -av -k on ".macd";
	setAttr -av -k on ".macq";
	setAttr -av -k on ".mcfr";
	setAttr -k on ".ifg";
	setAttr -av -k on ".clip";
	setAttr -av -k on ".edm";
	setAttr -av -k on ".edl";
	setAttr -av -cb on ".ren" -type "string" "mayaHardware2";
	setAttr -av -k on ".esr";
	setAttr -av -k on ".ors";
	setAttr -k on ".sdf";
	setAttr -av -k on ".outf";
	setAttr -av -k on ".imfkey" -type "string" "exr";
	setAttr -av -k on ".gama";
	setAttr -av -k on ".exrc";
	setAttr -av -k on ".expt";
	setAttr -av -k on ".an";
	setAttr -k on ".ar";
	setAttr -av -k on ".fs";
	setAttr -av -k on ".ef";
	setAttr -av -k on ".bfs";
	setAttr -av -k on ".me";
	setAttr -k on ".se";
	setAttr -av -k on ".be";
	setAttr -av -cb on ".ep";
	setAttr -av -k on ".fec";
	setAttr -av -k on ".ofc";
	setAttr -k on ".ofe";
	setAttr -k on ".efe";
	setAttr -cb on ".oft";
	setAttr -k on ".umfn";
	setAttr -k on ".ufe";
	setAttr -av -cb on ".pff";
	setAttr -av -k on ".peie";
	setAttr -av -cb on ".ifp";
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
	setAttr -k on ".gv";
	setAttr -k on ".sv";
	setAttr -av -k on ".mm";
	setAttr -av -k on ".npu";
	setAttr -av -k on ".itf";
	setAttr -av -k on ".shp";
	setAttr -k on ".isp";
	setAttr -av -k on ".uf";
	setAttr -av -k on ".oi";
	setAttr -av -k on ".rut";
	setAttr -av -k on ".mot";
	setAttr -av -k on ".mb";
	setAttr -av -k on ".mbf";
	setAttr -av -k on ".mbso";
	setAttr -av -k on ".mbsc";
	setAttr -av -k on ".afp";
	setAttr -av -k on ".pfb";
	setAttr -av -k on ".pram";
	setAttr -av -k on ".poam";
	setAttr -av -k on ".prlm";
	setAttr -av -k on ".polm";
	setAttr -av -cb on ".prm";
	setAttr -av -cb on ".pom";
	setAttr -k on ".pfrm";
	setAttr -k on ".pfom";
	setAttr -av -k on ".bll";
	setAttr -av -k on ".bls";
	setAttr -av -k on ".smv";
	setAttr -av -k on ".ubc";
	setAttr -av -k on ".mbc";
	setAttr -k on ".mbt";
	setAttr -av -k on ".udbx";
	setAttr -av -k on ".smc";
	setAttr -av -k on ".kmv";
	setAttr -k on ".isl";
	setAttr -k on ".ism";
	setAttr -k on ".imb";
	setAttr -av -k on ".rlen";
	setAttr -av -k on ".frts";
	setAttr -av -k on ".tlwd";
	setAttr -av -k on ".tlht";
	setAttr -av -k on ".jfc";
	setAttr -k on ".rsb";
	setAttr -av -k on ".ope";
	setAttr -av -k on ".oppf";
	setAttr -av -k on ".rcp";
	setAttr -av -k on ".icp";
	setAttr -av -k on ".ocp";
	setAttr -k on ".hbl";
	setAttr ".dss" -type "string" "standardSurface1";
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
	setAttr -av -cb on ".ihi";
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
	setAttr -av -k on ".hwcc";
	setAttr -av -k on ".hwdp";
	setAttr -av -k on ".hwql";
	setAttr -av -k on ".hwfr";
	setAttr -av -k on ".soll";
	setAttr -av -k on ".sosl";
	setAttr -av -k on ".bswa";
	setAttr -av -k on ".shml";
	setAttr -av -k on ".hwel";
connectAttr "hyperLayout8.msg" "BaseA_Block.hl";
connectAttr "SausageFaceTemplate_BaseA_Config.nds" "BaseA_Block.nds";
connectAttr "hyperLayout7.msg" "VisAttrs_Block.hl";
connectAttr "VisAttrs_Config.nds" "VisAttrs_Block.nds";
connectAttr "hyperLayout51.msg" "FakeParentAndRoot_Block.hl";
connectAttr "FakeParentAndRoot_Config.nds" "FakeParentAndRoot_Block.nds";
connectAttr "hyperLayout40.msg" "L_Brow_Block.hl";
connectAttr "L_Brow_Config.nds" "L_Brow_Block.nds";
connectAttr "hyperLayout41.msg" "L_Eyelids_Block.hl";
connectAttr "L_Eyelids_Config.nds" "L_Eyelids_Block.nds";
connectAttr "hyperLayout42.msg" "L_Ear_Block.hl";
connectAttr "L_Ear_Config.nds" "L_Ear_Block.nds";
connectAttr "L_Ear_A_Guide_Guide.Helper" "L_Ear_A_Guide_Guide_CtrlShape.v";
connectAttr "L_Ear_A_Guide_Guide.Helper" "L_Ear_A_Guide_Guide_Ctrl_CtrlShape.v";
connectAttr "L_Ear_A_Guide_Guide.Helper" "L_Ear_A_Guide_Guide_Ctrl_Ctrl_CtrlShape.v"
		;
connectAttr "L_Ear_A_Guide_Guide.Helper" "L_Ear_A_Guide_Guide_Ctrl_Ctrl_Ctrl_CtrlShape.v"
		;
connectAttr "hyperLayout43.msg" "Nose_Block.hl";
connectAttr "Nose_Config.nds" "Nose_Block.nds";
connectAttr "Nose_A_Guide_Guide.Helper" "Nose_A_Guide_Guide_CtrlShape.v";
connectAttr "Nose_A_Guide_Guide.Helper" "Nose_A_Guide_Guide_Ctrl_CtrlShape.v";
connectAttr "Nose_A_Guide_Guide.Helper" "Nose_A_Guide_Guide_Ctrl_Ctrl_CtrlShape.v"
		;
connectAttr "Nose_A_Guide_Guide.Helper" "Nose_A_Guide_Guide_Ctrl_Ctrl_Ctrl_CtrlShape.v"
		;
connectAttr "hyperLayout44.msg" "L_Lip_Block.hl";
connectAttr "L_Lip_Config.nds" "L_Lip_Block.nds";
connectAttr "L_Lip_A_Guide_Guide.Helper" "L_Lip_A_Guide_Guide_CtrlShape.v";
connectAttr "L_Lip_A_Guide_Guide.Helper" "L_Lip_A_Guide_Guide_Ctrl_CtrlShape.v";
connectAttr "L_Lip_A_Guide_Guide.Helper" "L_Lip_A_Guide_Guide_Ctrl_Ctrl_CtrlShape.v"
		;
connectAttr "L_Lip_A_Guide_Guide.Helper" "L_Lip_A_Guide_Guide_Ctrl_Ctrl_Ctrl_CtrlShape.v"
		;
connectAttr "L_Lip_A_Guide_Guide.s" "L_Lip_B_Guide_Guide.is";
connectAttr "L_Lip_B_Guide_Guide.Helper" "L_Lip_B_Guide_Guide_CtrlShape.v";
connectAttr "L_Lip_B_Guide_Guide.Helper" "L_Lip_B_Guide_Guide_Ctrl_CtrlShape.v";
connectAttr "L_Lip_B_Guide_Guide.Helper" "L_Lip_B_Guide_Guide_Ctrl_Ctrl_CtrlShape.v"
		;
connectAttr "L_Lip_B_Guide_Guide.Helper" "L_Lip_B_Guide_Guide_Ctrl_Ctrl_Ctrl_CtrlShape.v"
		;
connectAttr "hyperLayout45.msg" "UprLip_Block.hl";
connectAttr "UprLip_Config.nds" "UprLip_Block.nds";
connectAttr "UprLip_A_Guide_Guide.Helper" "UprLip_A_Guide_Guide_CtrlShape.v";
connectAttr "UprLip_A_Guide_Guide.Helper" "UprLip_A_Guide_Guide_Ctrl_CtrlShape.v"
		;
connectAttr "UprLip_A_Guide_Guide.Helper" "UprLip_A_Guide_Guide_Ctrl_Ctrl_CtrlShape.v"
		;
connectAttr "UprLip_A_Guide_Guide.Helper" "UprLip_A_Guide_Guide_Ctrl_Ctrl_Ctrl_CtrlShape.v"
		;
connectAttr "hyperLayout46.msg" "LwrLip_Block.hl";
connectAttr "LwrLip_Config.nds" "LwrLip_Block.nds";
connectAttr "LwrLip_A_Guide_Guide.Helper" "LwrLip_A_Guide_Guide_CtrlShape.v";
connectAttr "LwrLip_A_Guide_Guide.Helper" "LwrLip_A_Guide_Guide_Ctrl_CtrlShape.v"
		;
connectAttr "LwrLip_A_Guide_Guide.Helper" "LwrLip_A_Guide_Guide_Ctrl_Ctrl_CtrlShape.v"
		;
connectAttr "LwrLip_A_Guide_Guide.Helper" "LwrLip_A_Guide_Guide_Ctrl_Ctrl_Ctrl_CtrlShape.v"
		;
connectAttr "hyperLayout47.msg" "Jaw_Block.hl";
connectAttr "Jaw_Config.nds" "Jaw_Block.nds";
connectAttr "Jaw_A_Guide_Guide.Helper" "Jaw_A_Guide_Guide_CtrlShape.v";
connectAttr "Jaw_A_Guide_Guide.Helper" "Jaw_A_Guide_Guide_Ctrl_CtrlShape.v";
connectAttr "Jaw_A_Guide_Guide.Helper" "Jaw_A_Guide_Guide_Ctrl_Ctrl_CtrlShape.v"
		;
connectAttr "Jaw_A_Guide_Guide.Helper" "Jaw_A_Guide_Guide_Ctrl_Ctrl_Ctrl_CtrlShape.v"
		;
connectAttr "hyperLayout55.msg" "L_Cheek_Block.hl";
connectAttr "L_Cheek_Config.nds" "L_Cheek_Block.nds";
connectAttr "L_Cheek_Guide_Guide.Helper" "L_Cheek_Guide_Guide_CtrlShape.v";
connectAttr "L_Cheek_Guide_Guide.Helper" "L_Cheek_Guide_Guide_Ctrl_CtrlShape.v";
connectAttr "L_Cheek_Guide_Guide.Helper" "L_Cheek_Guide_Guide_Ctrl_Ctrl_CtrlShape.v"
		;
connectAttr "L_Cheek_Guide_Guide.Helper" "L_Cheek_Guide_Guide_Ctrl_Ctrl_Ctrl_CtrlShape.v"
		;
connectAttr "hyperLayout53.msg" "CreateSkl_Block.hl";
connectAttr "CreateSkl_Config.nds" "CreateSkl_Block.nds";
connectAttr "hyperLayout48.msg" "CleanCustomFace_Block.hl";
connectAttr "CleanCustomFace_Config.nds" "CleanCustomFace_Block.nds";
connectAttr "hyperLayout49.msg" "CreateAutomations_Block.hl";
connectAttr "CreateAutomations_Config.nds" "CreateAutomations_Block.nds";
connectAttr "hyperLayout39.msg" "Load_Ctrls_Block.hl";
connectAttr "Load_Ctrls_Config.nds" "Load_Ctrls_Block.nds";
connectAttr "Vis_Guide.msg" "hyperLayout7.hyp[4].dn";
connectAttr "Vis_GuideShape.msg" "hyperLayout7.hyp[5].dn";
connectAttr "FakeParentAndRoot_Loc.msg" "hyperLayout51.hyp[0].dn";
connectAttr "FakeParentAndRoot_LocShape.msg" "hyperLayout51.hyp[1].dn";
connectAttr "L_Brow_Guide.msg" "hyperLayout40.hyp[0].dn";
connectAttr "L_Brow_GuideShape.msg" "hyperLayout40.hyp[1].dn";
connectAttr "EyePivot.msg" "hyperLayout41.hyp[0].dn";
connectAttr "L_Ear_A_Guide_Guide.msg" "hyperLayout42.hyp[0].dn";
connectAttr "L_Ear_A_Guide_Guide_CtrlShape.msg" "hyperLayout42.hyp[1].dn";
connectAttr "L_Ear_A_Guide_Guide_Ctrl_CtrlShape.msg" "hyperLayout42.hyp[2].dn";
connectAttr "L_Ear_A_Guide_Guide_Ctrl_Ctrl_CtrlShape.msg" "hyperLayout42.hyp[3].dn"
		;
connectAttr "L_Ear_A_Guide_Guide_Ctrl_Ctrl_Ctrl_CtrlShape.msg" "hyperLayout42.hyp[4].dn"
		;
connectAttr "Nose_A_Guide_Guide.msg" "hyperLayout43.hyp[0].dn";
connectAttr "Nose_A_Guide_Guide_CtrlShape.msg" "hyperLayout43.hyp[1].dn";
connectAttr "Nose_A_Guide_Guide_Ctrl_CtrlShape.msg" "hyperLayout43.hyp[2].dn";
connectAttr "Nose_A_Guide_Guide_Ctrl_Ctrl_CtrlShape.msg" "hyperLayout43.hyp[3].dn"
		;
connectAttr "Nose_A_Guide_Guide_Ctrl_Ctrl_Ctrl_CtrlShape.msg" "hyperLayout43.hyp[4].dn"
		;
connectAttr "L_Lip_A_Guide_Guide.msg" "hyperLayout44.hyp[10].dn";
connectAttr "L_Lip_A_Guide_Guide_CtrlShape.msg" "hyperLayout44.hyp[11].dn";
connectAttr "L_Lip_A_Guide_Guide_Ctrl_CtrlShape.msg" "hyperLayout44.hyp[12].dn";
connectAttr "L_Lip_A_Guide_Guide_Ctrl_Ctrl_CtrlShape.msg" "hyperLayout44.hyp[13].dn"
		;
connectAttr "L_Lip_A_Guide_Guide_Ctrl_Ctrl_Ctrl_CtrlShape.msg" "hyperLayout44.hyp[14].dn"
		;
connectAttr "L_Lip_B_Guide_Guide.msg" "hyperLayout44.hyp[15].dn";
connectAttr "L_Lip_B_Guide_Guide_CtrlShape.msg" "hyperLayout44.hyp[16].dn";
connectAttr "L_Lip_B_Guide_Guide_Ctrl_CtrlShape.msg" "hyperLayout44.hyp[17].dn";
connectAttr "L_Lip_B_Guide_Guide_Ctrl_Ctrl_CtrlShape.msg" "hyperLayout44.hyp[18].dn"
		;
connectAttr "L_Lip_B_Guide_Guide_Ctrl_Ctrl_Ctrl_CtrlShape.msg" "hyperLayout44.hyp[19].dn"
		;
connectAttr "UprLip_A_Guide_Guide.msg" "hyperLayout45.hyp[0].dn";
connectAttr "UprLip_A_Guide_Guide_CtrlShape.msg" "hyperLayout45.hyp[1].dn";
connectAttr "UprLip_A_Guide_Guide_Ctrl_CtrlShape.msg" "hyperLayout45.hyp[2].dn";
connectAttr "UprLip_A_Guide_Guide_Ctrl_Ctrl_CtrlShape.msg" "hyperLayout45.hyp[3].dn"
		;
connectAttr "UprLip_A_Guide_Guide_Ctrl_Ctrl_Ctrl_CtrlShape.msg" "hyperLayout45.hyp[4].dn"
		;
connectAttr "LwrLip_A_Guide_Guide.msg" "hyperLayout46.hyp[0].dn";
connectAttr "LwrLip_A_Guide_Guide_CtrlShape.msg" "hyperLayout46.hyp[1].dn";
connectAttr "LwrLip_A_Guide_Guide_Ctrl_CtrlShape.msg" "hyperLayout46.hyp[2].dn";
connectAttr "LwrLip_A_Guide_Guide_Ctrl_Ctrl_CtrlShape.msg" "hyperLayout46.hyp[3].dn"
		;
connectAttr "LwrLip_A_Guide_Guide_Ctrl_Ctrl_Ctrl_CtrlShape.msg" "hyperLayout46.hyp[4].dn"
		;
connectAttr "Jaw_A_Guide_Guide.msg" "hyperLayout47.hyp[0].dn";
connectAttr "Jaw_A_Guide_Guide_CtrlShape.msg" "hyperLayout47.hyp[1].dn";
connectAttr "Jaw_A_Guide_Guide_Ctrl_CtrlShape.msg" "hyperLayout47.hyp[2].dn";
connectAttr "Jaw_A_Guide_Guide_Ctrl_Ctrl_CtrlShape.msg" "hyperLayout47.hyp[3].dn"
		;
connectAttr "Jaw_A_Guide_Guide_Ctrl_Ctrl_Ctrl_CtrlShape.msg" "hyperLayout47.hyp[4].dn"
		;
connectAttr "L_Cheek_Guide_Guide.msg" "hyperLayout55.hyp[0].dn";
connectAttr "L_Cheek_Guide_Guide_CtrlShape.msg" "hyperLayout55.hyp[1].dn";
connectAttr "L_Cheek_Guide_Guide_Ctrl_CtrlShape.msg" "hyperLayout55.hyp[2].dn";
connectAttr "L_Cheek_Guide_Guide_Ctrl_Ctrl_CtrlShape.msg" "hyperLayout55.hyp[3].dn"
		;
connectAttr "L_Cheek_Guide_Guide_Ctrl_Ctrl_Ctrl_CtrlShape.msg" "hyperLayout55.hyp[4].dn"
		;
connectAttr "CleanCustomFace_Loc.msg" "hyperLayout48.hyp[0].dn";
connectAttr "CleanCustomFace_LocShape.msg" "hyperLayout48.hyp[1].dn";
connectAttr "CreateAutomations_Loc.msg" "hyperLayout49.hyp[0].dn";
connectAttr "CreateAutomations_LocShape.msg" "hyperLayout49.hyp[1].dn";
connectAttr "L_Brow_GuideShape.iog" ":initialShadingGroup.dsm" -na;
dataStructure -fmt "raw" -as "name=DiffEdge:float=value";
dataStructure -fmt "raw" -as "name=notes_right_parShape:string=value";
dataStructure -fmt "raw" -as "name=keyValueStructure:string=value";
dataStructure -fmt "raw" -as "name=notes_trees_left1:string=value";
dataStructure -fmt "raw" -as "name=notes_baseScatt:string=value";
dataStructure -fmt "raw" -as "name=notes_decayGrassesCenter_parShape:string=value";
dataStructure -fmt "raw" -as "name=f_1:float=value";
dataStructure -fmt "raw" -as "name=notes_base_right:string=value";
dataStructure -fmt "raw" -as "name=notes_decayGrassPatchA_parShape:string=value";
dataStructure -fmt "raw" -as "name=notes_bushes_parShape:string=value";
dataStructure -fmt "raw" -as "name=mapManager_slopesGroundGrassA_Combined:string=value";
dataStructure -fmt "raw" -as "name=notes_polySurface56:string=value";
dataStructure -fmt "raw" -as "name=notes_decayGrassPatchD_parShape:string=value";
dataStructure -fmt "raw" -as "name=notes_snapshot_floor:string=value";
dataStructure -fmt "raw" -as "name=notes_ground_c_geo:string=value";
dataStructure -fmt "raw" -as "name=notes_groundA_parShape:string=value";
dataStructure -fmt "raw" -as "name=notes_decayGrassPatchB_parShape:string=value";
dataStructure -fmt "raw" -as "name=notes_pPlane3:string=value";
dataStructure -fmt "raw" -as "name=notes_pPlane4:string=value";
dataStructure -fmt "raw" -as "name=notes_pPlane1:string=value";
dataStructure -fmt "raw" -as "name=notes_grassBase:string=value";
dataStructure -fmt "raw" -as "name=notes_wildPatchF_parShape:string=value";
dataStructure -fmt "raw" -as "name=notes_decayGrassPatchC_parShape:string=value";
dataStructure -fmt "raw" -as "name=notes_pPlane5:string=value";
dataStructure -fmt "raw" -as "name=mapManager_pPlane5:string=value";
dataStructure -fmt "raw" -as "name=notes_slopesGroundGrassA_Combined:string=value";
dataStructure -fmt "raw" -as "name=mapManager_grassBase:string=value";
dataStructure -fmt "raw" -as "name=mapManager_baseScatter:string=value";
dataStructure -fmt "raw" -as "name=mapManager_slopesGroundGrassD_Combined:string=value";
dataStructure -fmt "raw" -as "name=notes_grassJuneBackYard_parShape:string=value";
dataStructure -fmt "raw" -as "name=mapManager_pPlane2:string=value";
dataStructure -fmt "raw" -as "name=notes_groundWoods_c_geo1:string=value";
dataStructure -fmt "raw" -as "name=notes_ground:string=value";
dataStructure -fmt "raw" -as "name=notes_wildPatchC_parShape:string=value";
dataStructure -fmt "raw" -as "name=mapManager_snapshot_CombinedGrass:string=value";
dataStructure -fmt "raw" -as "name=notes_groundC_parShape:string=value";
dataStructure -fmt "raw" -as "name=faceConnectOutputStructure:bool=faceConnectOutput:string[200]=faceConnectOutputAttributes:string[200]=faceConnectOutputGroups";
dataStructure -fmt "raw" -as "name=notes_baseScatter:string=value";
dataStructure -fmt "raw" -as "name=notes_pPlane2:string=value";
dataStructure -fmt "raw" -as "name=mapManager_suelo:string=value";
dataStructure -fmt "raw" -as "name=notes_floorOrangeConcrete_c_geo:string=value";
dataStructure -fmt "raw" -as "name=OrgStruct:float[3]=Origin Point";
dataStructure -fmt "raw" -as "name=notes_groundD_parShape:string=value";
dataStructure -fmt "raw" -as "name=NameAndID:string=name:int32=ID";
dataStructure -fmt "raw" -as "name=notes_wildPatchE_parShape:string=value";
dataStructure -fmt "raw" -as "name=notes_slopes_parShape:string=value";
dataStructure -fmt "raw" -as "name=f_3:float[3]=value";
dataStructure -fmt "raw" -as "name=mapManager_ground:string=value";
dataStructure -fmt "raw" -as "name=Offset:float[3]=value";
dataStructure -fmt "raw" -as "name=notes_decayLeaves_parShape:string=value";
dataStructure -fmt "raw" -as "name=mapManager_snapshot_floor:string=value";
dataStructure -fmt "raw" -as "name=notes_ferns_parShape:string=value";
dataStructure -fmt "raw" -as "name=mapManager_base_right:string=value";
dataStructure -fmt "raw" -as "name=mapManager_slopesGroundGrassB_Combined:string=value";
dataStructure -fmt "raw" -as "name=mapManager_pPlane3:string=value";
dataStructure -fmt "raw" -as "name=notes_wildPatchDegraded_parShape:string=value";
dataStructure -fmt "raw" -as "name=mapManager_pPlane1:string=value";
dataStructure -fmt "raw" -as "name=faceConnectMarkerStructure:bool=faceConnectMarker:string[200]=faceConnectOutputGroups";
dataStructure -fmt "raw" -as "name=notes_grass_c_geo1:string=value";
dataStructure -fmt "raw" -as "name=notes_wildPatchA_parShape:string=value";
dataStructure -fmt "raw" -as "name=notes_baseLeaves:string=value";
dataStructure -fmt "raw" -as "name=mapManager_floorOrangeConcrete_c_geo:string=value";
dataStructure -fmt "raw" -as "name=notes_mountains_parShape:string=value";
dataStructure -fmt "raw" -as "name=notes_pPlane6:string=value";
dataStructure -fmt "raw" -as "name=notes_groundB_parShape:string=value";
dataStructure -fmt "raw" -as "name=notes_grass_c_geo:string=value";
dataStructure -fmt "raw" -as "name=idStructure:int32=ID";
dataStructure -fmt "raw" -as "name=notes_suelo:string=value";
dataStructure -fmt "raw" -as "name=notes_snapshot_CombinedGrass:string=value";
dataStructure -fmt "raw" -as "name=mapManager_juneBackYard:string=value";
dataStructure -fmt "raw" -as "name=mapManager_baseScatt:string=value";
dataStructure -fmt "raw" -as "name=notes_slopesGroundGrassD_Combined:string=value";
dataStructure -fmt "raw" -as "name=Blur3dMetaData:string=Blur3dValue";
dataStructure -fmt "raw" -as "name=mapManager_grass_c_geo1:string=value";
dataStructure -fmt "raw" -as "name=mapManager_polySurface56:string=value";
dataStructure -fmt "raw" -as "name=mapManager_snapshot_Combined:string=value";
dataStructure -fmt "raw" -as "name=mapManager_groundWoods_c_geo1:string=value";
dataStructure -fmt "raw" -as "name=mapManager_slopesMountainsGrass_Combined:string=value";
dataStructure -fmt "raw" -as "name=mapManager_pPlane4:string=value";
dataStructure -fmt "raw" -as "name=notes_snapshot_Combined:string=value";
dataStructure -fmt "raw" -as "name=notes_wildPatchG_parShape:string=value";
dataStructure -fmt "raw" -as "name=mapManager_degraded:string=value";
dataStructure -fmt "raw" -as "name=notes_slopesGroundGrassB_Combined:string=value";
dataStructure -fmt "raw" -as "name=mapManager_grass_c_geo:string=value";
dataStructure -fmt "raw" -as "name=notes_decayLeavesCarousel_parShape:string=value";
dataStructure -fmt "raw" -as "name=mapManager_slopesGroundGrassC_Combined:string=value";
dataStructure -fmt "raw" -as "name=notes_trees_parShape:string=value";
dataStructure -fmt "raw" -as "name=Curvature:float=mean:float=gaussian:float=ABS:float=RMS";
dataStructure -fmt "raw" -as "name=mapManager_trees_left1:string=value";
dataStructure -fmt "raw" -as "name=OffStruct:float=Offset";
dataStructure -fmt "raw" -as "name=mapManager_base_hojas:string=value";
dataStructure -fmt "raw" -as "name=notes_wildPatchH_parShape:string=value";
dataStructure -fmt "raw" -as "name=notes_base_left:string=value";
dataStructure -fmt "raw" -as "name=notes_slopesGroundGrassC_Combined:string=value";
dataStructure -fmt "raw" -as "name=mapManager_pPlane6:string=value";
dataStructure -fmt "raw" -as "name=notes_left_parShape:string=value";
dataStructure -fmt "raw" -as "name=notes_base_hojas:string=value";
dataStructure -fmt "raw" -as "name=mapManager_ground_c_geo:string=value";
dataStructure -fmt "raw" -as "name=IdStruct:int32=ID";
dataStructure -fmt "raw" -as "name=notes_trees_left:string=value";
dataStructure -fmt "raw" -as "name=DiffArea:float=value";
dataStructure -fmt "raw" -as "name=notes_degraded:string=value";
dataStructure -fmt "raw" -as "name=notes_wildPatchD_parShape:string=value";
dataStructure -fmt "raw" -as "name=notes_widlPatchB_parShape:string=value";
dataStructure -fmt "raw" -as "name=notes_juneBackYard:string=value";
dataStructure -fmt "raw" -as "name=mapManager_base_left:string=value";
dataStructure -fmt "raw" -as "name=notes_slopesMountainsGrass_Combined:string=value";
dataStructure -fmt "raw" -as "name=mapManager_trees_left:string=value";
dataStructure -fmt "raw" -as "name=mapManager_baseLeaves:string=value";
// End of LowGameFace.ma
