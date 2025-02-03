//Maya ASCII 2024 scene
//Name: humanFaceSimpleTemplate.ma
//Last modified: Thu, May 02, 2024 04:24:00 PM
//Codeset: 1252
requires maya "2024";
requires "stereoCamera" "10.0";
currentUnit -l centimeter -a degree -t film;
fileInfo "application" "maya";
fileInfo "product" "Maya 2024";
fileInfo "version" "2024";
fileInfo "cutIdentifier" "202310181224-69282f2959";
fileInfo "osv" "Windows 11 Home v2009 (Build: 22631)";
fileInfo "UUID" "3D9FD754-4413-28DE-6AB7-F58FFEEA5584";
createNode transform -n "Mutant_Build";
	rename -uid "27154000-0018-1FF3-6621-A96000000F24";
createNode transform -n "init" -p "Mutant_Build";
	rename -uid "27154000-0018-1FF3-6621-A96000000F25";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2024/scripts/rigging/Mutant_Tools/Icons/";
createNode dagContainer -n "BaseA_Block" -p "init";
	rename -uid "27154000-0018-1FF3-6621-A96000000F26";
	addAttr -ci true -sn "nts" -ln "notes" -dt "string";
	setAttr ".isc" yes;
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2024/scripts/rigging/Mutant_Tools/Icons/BaseA.png";
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
	setAttr ".nts" -type "string" "['Mutant_Tools_Grp', 'Rig_Grp', 'Bind_Joints_Grp', 'Mover_Gimbal_CtrlShape', 'Miscellaneous_Grp', 'Mover_Ctrl_Offset_Grp', 'Bind_Geo_Grp', 'Ctrl_Grp', 'Mover_Gimbal_Ctrl', 'Mover_CtrlShape', 'Global_Ctrl', 'Mover_Ctrl_tag', 'Mover_Gimbal_Ctrl_tag', 'Global_Ctrl_Offset_Grp', 'Global_CtrlShape', 'Template_Grp', 'Rig_Ctrl_Grp', 'Extra_Geo_Grp', 'Mover_Ctrl']";
createNode dagContainer -n "VisAttrs_Block" -p "init";
	rename -uid "27154000-0018-1FF3-6621-A96000000F27";
	addAttr -ci true -sn "nts" -ln "notes" -dt "string";
	setAttr ".isc" yes;
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2024/scripts/rigging/Mutant_Tools/Icons/CODE.png";
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
	rename -uid "27154000-0018-1FF3-6621-A96000000F28";
	addAttr -ci true -sn "naming" -ln "naming" -dt "string";
	addAttr -ci true -sn "anim_preset" -ln "anim_preset" -dt "string";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2024/scripts/rigging/Mutant_Tools/Icons/";
	setAttr -k off -cb on ".v";
	setAttr ".t" -type "double3" 0.10135800794241118 184.8299486276953 -0.17240603215658501 ;
	setAttr ".rp" -type "double3" 0 1.6093281918018576 0 ;
	setAttr ".sp" -type "double3" 0 1.6093281918018576 0 ;
	setAttr ".naming" -type "string" "{'side': '', 'base': 'cone', 'adjective': '', 'letter': '', 'number': '', 'position': '', 'node_type': 'ctrl', 'convention': 'default', }";
	setAttr ".anim_preset" -type "string" "{'display': ['v']}";
createNode nurbsCurve -n "Vis_GuideShape" -p "Vis_Guide";
	rename -uid "27154000-0018-1FF3-6621-A96000000F29";
	addAttr -ci true -sn "shape" -ln "shape" -dt "string";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2024/scripts/rigging/Mutant_Tools/Icons/";
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
createNode transform -n "bodyLocals" -p "Mutant_Build";
	rename -uid "27154000-0018-1FF3-6621-A96000000F2A";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2024/scripts/rigging/Mutant_Tools/Icons/";
	setAttr ".t" -type "double3" 0 148.19816716577168 0 ;
createNode dagContainer -n "SkullLocal_Block" -p "bodyLocals";
	rename -uid "27154000-0018-1FF3-6621-A96000000F2B";
	addAttr -ci true -sn "nts" -ln "notes" -dt "string";
	setAttr ".isc" yes;
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2024/scripts/rigging/Mutant_Tools/Icons/Locals.png";
	setAttr ".ctor" -type "string" "esteban.rodriguez";
	setAttr ".cdat" -type "string" "2022/05/11 14:42:05";
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
	setAttr ".nts" -type "string" "['Body_Geo_Locals_Grp', 'BodySkullShapeOrig', 'BodySkull', 'BodySkullShape', 'SkullLocal_Rig_Grp']";
createNode dagContainer -n "Locals_Block" -p "bodyLocals";
	rename -uid "27154000-0018-1FF3-6621-A96000000F2C";
	addAttr -ci true -sn "nts" -ln "notes" -dt "string";
	setAttr ".isc" yes;
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2024/scripts/rigging/Mutant_Tools/Icons/Locals.png";
	setAttr ".ctor" -type "string" "esteban.rodriguez";
	setAttr ".cdat" -type "string" "2022/04/26 10:38:22";
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
	setAttr ".nts" -type "string" "['BodyMouthUp', 'BodyMouthWide', 'BodyLips', 'Locals_Rig_Grp', 'BodySkull_Locals_Grp', 'BodyJaw', 'BodySkullShapeOrig1', 'BodyNose', 'BodyMouthDownShape', 'BodyBrowsShapeOrig', 'BodyEyesShape', 'BodyNoseShapeOrig', 'BodyCheeksShape', 'BodyMouthDown', 'BodyMouthNarrowShapeOrig', 'BodyMouthDownShapeOrig', 'BodyNoseShape', 'BodyJawShapeOrig', 'Locals_BSP', 'BodyMouthWideShape', 'BodySquash', 'BodySquashShapeOrig', 'BodyMouthNarrow', 'BodyCheeksShapeOrig', 'BodyJawShape', 'BodyMouthUpShape', 'BodyMouthWideShapeOrig', 'BodyMouthUpShapeOrig', 'BodySquashShape', 'BodyBrows', 'BodyLipsShape', 'BodyMouthNarrowShape', 'BodyBrowsShape', 'BodyCheeks', 'BodyLipsShapeOrig', 'BodyEyes', 'BodyEyesShapeOrig']";
createNode transform -n "face" -p "Mutant_Build";
	rename -uid "27154000-0018-1FF3-6621-A96000000F2D";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2024/scripts/rigging/Mutant_Tools/Icons/";
	setAttr ".t" -type "double3" 0 148.19816716577168 0 ;
createNode dagContainer -n "Skull_Block" -p "face";
	rename -uid "27154000-0018-1FF3-6621-A96000000F2E";
	addAttr -ci true -sn "nts" -ln "notes" -dt "string";
	setAttr ".isc" yes;
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2024/scripts/rigging/Mutant_Tools/Icons/Skull.png";
	setAttr ".ctor" -type "string" "esteban.rodriguez";
	setAttr ".cdat" -type "string" "2022/04/05 13:53:20";
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
	setAttr ".nts" -type "string" "['Skull_Upr_Ctrl_Offset_Grp', 'Skull_Upr_Bnd', 'Skull_Parent_LocShape', 'Skull_Ctrl_Grp_parentConstraint1', 'Skull_Rig_Grp', 'Skull_Lwr_Bnd', 'Skull_Upr_Ctrl_tag', 'Skull_Lwr_CtrlShape', 'Skull_Upr_CtrlShape', 'Skull_Lwr_Ctrl', 'Skull_Lwr_Ctrl_tag', 'Skull_Ctrl_Grp', 'Skull_Upr_Bnd_parentConstraint1', 'Skull_Lwr_Bnd_parentConstraint1', 'Skull_Upr_Jnt', 'Skull_Lwr_Jnt_Offset_Grp', 'Skull_Lwr_Ctrl_Offset_Grp', 'Skull_Parent_Loc', 'Skull_Upr_Jnt_Offset_Grp', 'Skull_Lwr_Jnt', 'Skull_Upr_Ctrl']";
createNode joint -n "Skull_Lwr_Guide" -p "Skull_Block";
	rename -uid "27154000-0018-1FF3-6621-A96000000F2F";
	addAttr -ci true -sn "Helper" -ln "Helper" -min 0 -max 1 -en "Hide:Show" -at "enum";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2024/scripts/rigging/Mutant_Tools/Icons/";
	setAttr ".t" -type "double3" 0.035793134339884847 12.670666321704715 -0.37055461571900516 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr -cb on ".Helper" 1;
createNode nurbsCurve -n "Skull_Lwr_Guide_CtrlShape" -p "Skull_Lwr_Guide";
	rename -uid "27154000-0018-1FF3-6621-A96000000F30";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2024/scripts/rigging/Mutant_Tools/Icons/";
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
createNode nurbsCurve -n "Skull_Lwr_Guide_Ctrl_CtrlShape" -p "Skull_Lwr_Guide";
	rename -uid "27154000-0018-1FF3-6621-A96000000F31";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2024/scripts/rigging/Mutant_Tools/Icons/";
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
createNode nurbsCurve -n "Skull_Lwr_Guide_Ctrl_Ctrl_CtrlShape" -p "Skull_Lwr_Guide";
	rename -uid "27154000-0018-1FF3-6621-A96000000F32";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2024/scripts/rigging/Mutant_Tools/Icons/";
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
createNode nurbsCurve -n "Skull_Lwr_Guide_Ctrl_Ctrl_Ctrl_CtrlShape" -p "Skull_Lwr_Guide";
	rename -uid "27154000-0018-1FF3-6621-A96000000F33";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2024/scripts/rigging/Mutant_Tools/Icons/";
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
createNode joint -n "Skull_Upr_Guide" -p "Skull_Lwr_Guide";
	rename -uid "27154000-0018-1FF3-6621-A96000000F34";
	addAttr -ci true -sn "Helper" -ln "Helper" -min 0 -max 1 -en "Hide:Show" -at "enum";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2024/scripts/rigging/Mutant_Tools/Icons/";
	setAttr ".t" -type "double3" -3.5666182507387845e-10 1.4112473808459072 4.0101478582243999e-08 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr -cb on ".Helper" 1;
createNode nurbsCurve -n "Skull_Upr_Guide_CtrlShape" -p "Skull_Upr_Guide";
	rename -uid "27154000-0018-1FF3-6621-A96000000F35";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2024/scripts/rigging/Mutant_Tools/Icons/";
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
createNode nurbsCurve -n "Skull_Upr_Guide_Ctrl_CtrlShape" -p "Skull_Upr_Guide";
	rename -uid "27154000-0018-1FF3-6621-A96000000F36";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2024/scripts/rigging/Mutant_Tools/Icons/";
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
createNode nurbsCurve -n "Skull_Upr_Guide_Ctrl_Ctrl_CtrlShape" -p "Skull_Upr_Guide";
	rename -uid "27154000-0018-1FF3-6621-A96000000F37";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2024/scripts/rigging/Mutant_Tools/Icons/";
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
createNode nurbsCurve -n "Skull_Upr_Guide_Ctrl_Ctrl_Ctrl_CtrlShape" -p "Skull_Upr_Guide";
	rename -uid "27154000-0018-1FF3-6621-A96000000F38";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2024/scripts/rigging/Mutant_Tools/Icons/";
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
createNode dagContainer -n "L_Eyelids_Block" -p "face";
	rename -uid "27154000-0018-1FF3-6621-A96000000F39";
	addAttr -ci true -sn "nts" -ln "notes" -dt "string";
	setAttr ".isc" yes;
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2024/scripts/rigging/Mutant_Tools/Icons/Eyes.png";
	setAttr ".ctor" -type "string" "esteban.rodriguez";
	setAttr ".cdat" -type "string" "2022/12/22 12:45:14";
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
		"['R_Eyelids_Dw_WireDriver_CrvShapeOrig', 'L_Eyelids_Dw_Scale_CtrlShape', 'L_Eyelids_Up_10_CtrlShape', 'L_Eyelids_Dw_12_POCI', 'L_Eyelids_Dw_Origin_10_Jnt_aimConstraint1', 'R_Eyelids_Dw_Origin_4_Jnt_Offset_Grp', 'L_Eyelids_UpMid_Jnt_Offset_Grp', 'L_Eyelids_Dw_6_Jnt_Offset_Grp', 'R_Eyelids_Scale_Bnd', 'R_Eyelids_Up_2_Ctrl', 'L_Eyelids_Up_Scale_Ctrl_tag', 'R_Eyelids_Dw_6_CtrlShape', 'R_Eyelids_Up_Origin_10_Jnt', 'L_Eyelids_Up_12_CtrlShape', 'L_Eyelids_Scale_Ctrl_Offset_Grp', 'R_Eyelids_Dw_10_Bnd', 'L_Eyelids_DwStart_Jnt', 'R_Eyelids_UpMid_Jnt_Offset_Grp', 'bindPose4', 'L_Eyelids_Dw_7_Loc', 'L_Eyelids_UpEnd_CtrlShape', 'R_Eyelids_Up_3_Jnt_Offset_Grp', 'R_Eyelids_Up_Origin_7_Jnt', 'R_Eyelids_Up_0_CtrlShape', 'R_Eyelids_Up_5_Bnd', 'R_Eyelids_Dw_3_Bnd', 'L_Eyelids_Up_WireDriver_ClusterCrvBaseWire_cv_6__jnt_bc', 'R_Eyelids_Dw_0_Bnd', 'L_Eyelids_Dw_7_Ctrl', 'R_Eyelids_Up_0_POCI', 'L_Eyelids_Up_WireDriver_ClusterCrvBaseWire_cv_1__jnt_bc', 'R_Eyelids_Up_13_Loc', 'L_Eyelids_Up_8_Ctrl_tag', 'R_Eyelids_Dw_7_Jnt', 'R_Eyelids_Dw_8_POCI', 'R_Eyelids_Up_5_CtrlShape', 'L_Eyelids_Dw_6_CtrlShape', 'L_Eyelids_Up_2_Bnd', 'L_Eyelids_Dw_10_Bnd', 'L_Eyelids_Up_6_Jnt', 'L_Eyelids_Dw_Vtx_CrvShapeOrig', 'L_Eyelids_UpMid_CtrlShape', 'L_Eyelids_Up_10_Bnd', 'R_Eyelids_UpStart_clusterHandleShape', 'L_Eyelids_Dw_5_Jnt', 'R_Eyelids_Dw_Origin_11_Jnt', 'R_Eyelids_Scale_Bnd_parentConstraint1', 'bindPose3', 'UprBlink_MultDiv1', 'L_Eyelids_Up_2_Ctrl_OffsetPivot_Grp_Offset_Grp', 'R_Eyelids_Up_AimLocators_Grp', 'R_Eyelids_Dw_5_Bnd', 'L_Eyelids_Dw_4_Ctrl_OffsetPivot_Grp', 'L_Eyelids_Dw_Origin_8_Jnt_aimConstraint1', 'L_Eyelids_Up_4_Bnd_parentConstraint1', 'unitConversion7', 'L_Eyelids_Up_7_Ctrl', 'R_Eyelids_Dw_12_CtrlShape', 'R_Eyelids_LwrBlink_BS', 'L_Eyelids_Up_9_Bnd_scaleConstraint1', 'R_Eyelids_Dw_12_Ctrl_OffsetPivot_Grp_Offset_Grp', 'R_Eyelids_UpMid_clusterHandleShape', 'R_Eyelids_UpEnd_Jnt_Offset_Grp', 'R_Eyelids_Blink_CrvBaseWire1ShapeOrig1', 'L_Eyelids_Up_Scale_Ctrl_Offset_Grp', 'R_Eyelids_Up_10_Ctrl', 'L_Eyelids_Dw_Origin_0_Jnt_Offset_Grp', 'R_Eyelids_Dw_11_Loc', 'R_Eyelids_DwStartMid_Jnt', 'L_Eyelids_Up_3_Bnd', 'R_Eyelids_Dw_WireDriver_ClusterCrvBaseWire_cv_0__clst_bc', 'R_Eyelids_Dw_12_Ctrl_OffsetPivot_Grp', 'L_Eyelids_Up_11_Bnd_parentConstraint1', 'L_Eyelids_UpStartMid_Ctrl_Offset_Grp', 'R_Eyelids_UpEndMid_clusterHandle', 'R_Eyelids_Up_5_Ctrl_tag', 'R_Eyelids_Up_9_Ctrl', 'R_Eyelids_Dw_10_Ctrl_tag', 'L_Eyelids_UpEndMid_Ctrl_Offset_Grp_parentConstraint1', 'L_Eyelids_Dw_8_Jnt', 'L_Eyelids_Up_3_Loc', 'R_Eyelids_UpStart_cluster1HandleShape', 'L_Eyelids_Dw_6_Loc', 'L_Eyelids_Up_Origin_1_Jnt', 'L_Eyelids_DwStartMid_Jnt_Offset_Grp', 'L_Eyelids_Up_3_Jnt_Offset_Grp', 'R_Eyelids_Dw_WireDriver_ClusterCrvBaseWireBaseWire', 'L_Eyelids_Dw_WireDriver_ClusterCrvBaseWire_cv_0__clst_bc', 'R_Eyelids_Up_10_Ctrl_OffsetPivot_Grp_Offset_Grp', 'R_Eyelids_DwEnd_cluster1HandleShape', 'R_Eyelids_Blink_CrvShape', 'R_Eyelids_Up_1_Ctrl', 'R_Eyelids_Rig_GrpMirror_Grp', 'R_Eyelids_Blink_Crv', 'R_Eyelids_Up_Scale_Ctrl', 'R_Eyelids_UpEndMid_Jnt', 'R_Eyelids_Ctrl_Grp', 'R_Eyelids_DwStartMid_Ctrl', 'R_Eyelids_Dw_12_Bnd', 'R_Eyelids_Dw_12_Bnd_parentConstraint1', 'L_Eyelids_DwStart_cluster1HandleShape', 'L_Eyelids_UpEndMid_Jnt_Offset_Grp', 'R_Eyelids_Dw_Origin_3_Jnt_aimConstraint1', 'R_Eyelids_Up_Origin_1_Jnt_Offset_Grp', 'R_Eyelids_Up_7_Ctrl_OffsetPivot_Grp_Offset_Grp', 'L_Eyelids_Up_13_Ctrl_OffsetPivot_Grp', 'L_Eyelids_Up_Origin_11_Jnt_aimConstraint1', 'R_Eyelids_Up_11_Jnt', 'R_Eyelids_Up_Origin_11_Jnt', 'R_Eyelids_Dw_12_Loc', 'L_Eyelids_Dw_4_Bnd', 'R_Eyelids_Dw_5_Loc', 'L_Eyelids_UpStart_Ctrl', 'L_Eyelids_UpStartMid_Jnt_Offset_Grp', 'R_Eyelids_Up_Origin_3_Jnt', 'L_Eyelids_Up_12_Bnd_parentConstraint1', 'R_Eyelids_Up_Origin_4_Jnt_Offset_Grp', 'R_Eyelids_DwStart_CtrlShape', 'L_Eyelids_Dw_Origin_10_Jnt', 'R_Eyelids_Up_5_Loc', 'R_Eyelids_Dw_Origin_10_Jnt_Offset_Grp', 'L_Eyelids_Up_Origin_5_Jnt', 'L_Eyelids_Up_VtxJnts_Grp', 'R_Eyelids_Up_7_CtrlShape', 'L_Eyelids_Dw_5_Bnd_parentConstraint1', 'L_Eyelids_Up_4_Jnt', 'R_Eyelids_Up_WireDriver_ClusterCrvBaseWire_cv_3__clst_rev', 'L_Eyelids_Up_Origin_11_Jnt', 'R_Eyelids_DwMid_Ctrl_Offset_Grp', 'R_Eyelids_Up_Origin_11_Jnt_aimConstraint1', 'L_Eyelids_Dw_4_Loc', 'R_Eyelids_Up_1_POCI', 'R_Eyelids_UpEndMid_Ctrl_Offset_Grp_parentConstraint1', 'L_Eyelids_Dw_Origin_3_Jnt', 'R_Eyelids_Dw_11_Bnd_scaleConstraint1', 'L_Eyelids_Up_9_Ctrl_OffsetPivot_Grp', 'L_Eyelids_Up_1_Bnd', 'L_Eyelids_Up_Origin_4_Jnt', 'R_Eyelids_Up_4_Bnd_parentConstraint1', 'L_Eyelids_Up_1_CtrlShape', 'R_Eyelids_Dw_11_Ctrl_OffsetPivot_Grp', 'R_Eyelids_Dw_WireDriver_ClusterCrvBaseWire_cv_5__clst_rev', 'R_Eyelids_Up_Origin_7_Jnt_aimConstraint1', 'L_Eyelids_Blink_Crv', 'R_Eyelids_Up_BlinkTarget_CrvShapeOrig1', 'R_Eyelids_Dw_WireDriver_ClusterCrvBaseWire_cv_0__clst_rev', 'R_Eyelids_Dw_5_Jnt', 'L_Eyelids_DwStart_Ctrl', 'L_Eyelids_DwStart_cluster1', 'R_Eyelids_Up_WireDriver_ClusterCrvBaseWire_cv_1__jnt_bc', 'L_Eyelids_Dw_11_Ctrl', 'L_Eyelids_Dw_Origin_12_Jnt_Offset_Grp', 'R_Eyelids_DwStartMid_Jnt_Offset_Grp_parentConstraint1', 'L_Eyelids_Dw_5_Ctrl', 'R_Eyelids_Up_5_Ctrl', 'R_Eyelids_Dw_WireDriver_ClusterCrvBaseWire_cv_5__jnt_bc5', 'R_Eyelids_Up_7_LocShape', 'R_Eyelids_UpEnd_CtrlShape', 'L_Eyelids_Dw_6_Bnd', 'L_Eyelids_Dw_11_Ctrl_OffsetPivot_Grp', 'R_Eyelids_Dw_1_Ctrl_Offset_Grp', 'R_Eyelids_Dw_WireDriver_ClusterCrvBaseWire_cv_1__md5', 'L_Eyelids_DwStartMid_clusterHandle', 'R_Eyelids_Up_WireDriver_CrvShape', 'L_Eyelids_Up_2_Bnd_scaleConstraint1', 'R_Eyelids_Dw_0_Jnt_Offset_Grp', 'L_Eyelids_DwEnd_Ctrl_tag', 'R_Eyelids_DwMid_clusterHandle', 'L_Eyelids_Dw_8_POCI', 'R_Eyelids_Up_8_Ctrl_OffsetPivot_Grp_Offset_Grp', 'R_Eyelids_Dw_6_Ctrl_tag', 'L_Eyelids_Up_13_Ctrl_tag', 'R_Eyelids_Up_1_Ctrl_OffsetPivot_Grp', 'L_Eyelids_Up_WireDriver_ClusterCrvBaseWire_cv_3__md5', 'R_Eyelids_Up_7_Bnd_parentConstraint1', 'R_Eyelids_Dw_4_Ctrl_OffsetPivot_Grp_Offset_Grp', 'R_Eyelids_Dw_2_Ctrl_OffsetPivot_Grp_Offset_Grp', 'R_Eyelids_UpStartMid_Ctrl_Offset_Grp', 'L_Eyelids_Scale_Grp_Offset_Grp', 'L_Eyelids_Up_3_POCI', 'L_Eyelids_UpEndMid_Ctrl', 'R_Eyelids_Up_WireDriver_ClusterCrvBaseWire_cv_1__clst_rev', 'R_Eyelids_Dw_9_Ctrl_Offset_Grp', 'L_Eyelids_Dw_WireDriver_ClusterCrvBaseWire_cv_3__clst_rev', 'L_Eyelids_Dw_WireDriver_ClusterCrvBaseWire_cv_3__clst_bc', 'L_Eyelids_Dw_Origin_9_Jnt_Offset_Grp', 'L_Eyelids_Up_Origin_2_Jnt_Offset_Grp', 'L_Eyelids_Up_9_Ctrl', 'L_Eyelids_Up_8_Bnd', 'L_Eyelids_Dw_6_Ctrl', 'R_Eyelids_Dw_0_Jnt', 'R_Eyelids_Up_8_Bnd', 'L_Eyelids_Dw_WireDriver_ClusterCrvBaseWire', 'R_Eyelids_UpStart_cluster', 'R_Eyelids_Up_Wire', 'R_Eyelids_Up_WireDriver_ClusterCrvBaseWire_cv_0__clst_bc', 'R_Eyelids_UpMid_cluster', 'L_Eyelids_Up_4_CtrlShape', 'L_Eyelids_DwEnd_Jnt', 'L_Eyelids_Dw_7_Ctrl_OffsetPivot_Grp', 'R_Eyelids_Ctrl_GrpMirror_Grp', 'R_Eyelids_Up_10_Bnd_scaleConstraint1', 'L_Eyelids_UpStartMid_clusterHandle', 'R_Eyelids_Up_Origin_5_Jnt_Offset_Grp', 'R_Eyelids_Dw_Vtx_Crv', 'L_Eyelids_Dw_11_Bnd_parentConstraint1', 'L_Eyelids_Dw_7_Bnd_parentConstraint1', 'L_Eyelids_Dw_10_Jnt_Offset_Grp', 'R_Eyelids_Up_Origin_12_Jnt_aimConstraint1', 'L_Eyelids_Dw_11_LocShape', 'L_Eyelids_Blink_CrvBaseWire1ShapeOrig1', 'L_Eyelids_EyePivot_Loc', 'L_Eyelids_Dw_3_Ctrl_OffsetPivot_Grp', 'L_Eyelids_Up_2_CtrlShape', 'L_Eyelids_Up_Origin_3_Jnt_Offset_Grp', 'R_Eyelids_Up_5_Bnd_parentConstraint1', 'R_Eyelids_Dw_2_POCI', 'R_Eyelids_Dw_BlinkTarget_CrvShapeOrig', 'R_Eyelids_Dw_0_Ctrl', 'L_Eyelids_Up_6_Jnt_Offset_Grp', 'R_Eyelids_Dw_10_CtrlShape', 'L_Eyelids_Up_WireDriver_ClusterCrvBaseWire_cv_3__clst_rev', 'L_Eyelids_Dw_0_LocShape', 'R_Eyelids_Dw_4_Ctrl_tag', 'L_Eyelids_Dw_11_CtrlShape', 'R_Eyelids_Dw_Origin_2_Jnt_aimConstraint1', 'L_Eyelids_Up_WireDriver_ClusterCrvBaseWire_cv_0__jnt_bc5', 'L_Eyelids_Dw_1_Bnd', 'L_Eyelids_Up_6_CtrlShape', 'R_Eyelids_Dw_0_Bnd_parentConstraint1', 'R_Eyelids_Dw_Origin_9_Jnt_aimConstraint1', 'R_Eyelids_Up_Origin_5_Jnt', 'L_Eyelids_DwEnd_Ctrl', 'L_Eyelids_Dw_2_Bnd', 'L_Eyelids_Up_Origin_2_Jnt_aimConstraint1', 'R_Eyelids_Up_12_Bnd_parentConstraint1', 'L_Eyelids_Up_10_LocShape', 'R_Eyelids_Up_9_Ctrl_tag', 'L_Eyelids_UpStartMid_Ctrl_Offset_Grp_parentConstraint1', 'L_Eyelids_DwStart_cluster', 'L_Eyelids_Up_WireDriver_ClusterCrvBaseWireBaseWireShape', 'R_Eyelids_Dw_9_Bnd', 'R_Eyelids_Up_8_Jnt', 'R_Eyelids_Up_13_CtrlShape', 'L_Eyelids_Up_4_LocShape', 'L_Eyelids_Up_13_CtrlShape', 'L_Eyelids_Up_9_Jnt_Offset_Grp', 'L_Eyelids_Dw_12_LocShape', 'R_Eyelids_DwMid_cluster', 'R_Eyelids_Up_13_POCI', 'R_Eyelids_Dw_WireDriver_ClusterCrvBaseWire_cv_6__clst_bc', 'L_Eyelids_Dw_10_POCI', 'L_Eyelids_Up_3_Ctrl', 'R_Eyelids_Up_6_Jnt_Offset_Grp', 'R_Eyelids_Up_7_Ctrl_OffsetPivot_Grp', 'L_Eyelids_DwStart_clusterHandle', 'L_Eyelids_Up_0_POCI', 'R_Eyelids_Up_Origin_1_Jnt_aimConstraint1', 'R_Eyelids_Dw_4_Bnd_parentConstraint1', 'L_Eyelids_Dw_0_Ctrl', 'L_Eyelids_Dw_WireDriver_ClusterCrvBaseWire_cv_1__clst_rev', 'L_Eyelids_DwEndMid_clusterHandle', 'L_Eyelids_Dw_AimLocators_Grp', 'R_Eyelids_Dw_10_POCI', 'R_Eyelids_Up_13_Bnd_parentConstraint1', 'R_Eyelids_Up_11_Ctrl_OffsetPivot_Grp', 'R_Eyelids_Dw_10_Bnd_parentConstraint1', 'L_Eyelids_Up_WireDriver_ClusterCrvBaseWire_cv_5__md5', 'L_Eyelids_Up_5_Ctrl_tag', 'R_Eyelids_Dw_9_CtrlShape', 'R_Eyelids_Dw_9_Ctrl_OffsetPivot_Grp', 'R_Eyelids_Dw_3_Ctrl_Offset_Grp', 'bindPose1', 'L_Eyelids_Dw_7_Ctrl_tag', 'L_Eyelids_Up_4_Bnd', 'R_Eyelids_Up_6_Ctrl', 'R_Eyelids_DwEndMid_Ctrl_Offset_Grp', 'R_Eyelids_Dw_WireDriver_ClusterCrvBaseWireBaseWireShape', 'R_Eyelids_Blink_CrvBaseWire1', 'R_Eyelids_UpEndMid_Ctrl_tag', 'L_Eyelids_Dw_5_Loc', 'L_Eyelids_Up_12_POCI', 'R_Eyelids_Up_2_Bnd_parentConstraint1', 'L_Eyelids_Dw_9_Bnd', 'R_Eyelids_Dw_10_Jnt_Offset_Grp', 'R_Eyelids_Up_10_LocShape', 'R_Eyelids_Dw_Origin_6_Jnt', 'L_Eyelids_Dw_Origin_6_Jnt', 'R_Eyelids_Up_Origin_3_Jnt_aimConstraint1', 'R_Eyelids_Dw_1_Jnt_Offset_Grp', 'L_Eyelids_Up_Origin_12_Jnt_Offset_Grp', 'R_Eyelids_Dw_Vtx_CrvShape', 'R_Eyelids_UpEndMid_Ctrl_Offset_Grp', 'R_Eyelids_Up_BlinkTarget_Crv', 'R_Eyelids_DwEnd_Ctrl_Offset_Grp', 'L_Eyelids_Up_6_Ctrl_Offset_Grp', 'L_Eyelids_Dw_5_Ctrl_Offset_Grp', 'L_Eyelids_DwEndMid_CtrlShape', 'L_Eyelids_Dw_2_Jnt_Offset_Grp', 'R_Eyelids_Dw_0_Bnd_scaleConstraint1', 'L_Eyelids_Up_9_Ctrl_tag', 'R_Eyelids_DwStartMid_clusterHandle', 'L_Eyelids_Up_WireDriver_ClusterCrvBaseWire_cv_1__md5', 'L_Eyelids_DwStartMid_cluster', 'L_Eyelids_Up_6_Loc', 'L_Eyelids_Dw_12_Bnd_parentConstraint1', 'L_Eyelids_Dw_10_CtrlShape', 'L_Eyelids_Up_Vtx_CrvShapeOrig', 'L_Eyelids_Blink_CrvBaseWire1Shape', 'L_Eyelids_Up_6_Bnd_parentConstraint1', 'R_Eyelids_Up_2_Ctrl_OffsetPivot_Grp_Offset_Grp', 'R_Eyelids_DwStart_clusterHandleShape', 'R_Eyelids_Dw_WireDriver_ClusterCrvBaseWire_cv_0__jnt_bc5', 'L_Eyelids_Up_0_Jnt', 'L_Eyelids_Dw_1_Ctrl_OffsetPivot_Grp', 'L_Eyelids_Up_8_Ctrl_OffsetPivot_Grp_Offset_Grp', 'L_Eyelids_Up_Origin_9_Jnt_aimConstraint1', 'R_Eyelids_Dw_WireDriver_ClusterCrvBaseWireBaseWireShapeOrig1', 'L_Eyelids_Dw_WireDriver_ClusterCrvBaseWire_cv_5__jnt_bc5', 'R_Eyelids_DwEnd_clusterHandleShape', 'R_Eyelids_DwStartMid_cluster', 'R_Eyelids_Dw_Wire', 'L_Eyelids_Up_11_POCI', 'L_Eyelids_Up_WireDriver_ClusterCrvBaseWireBaseWireShapeOrig', 'R_Eyelids_Up_Origin_0_Jnt_Offset_Grp', 'R_Eyelids_Up_5_Jnt_Offset_Grp', 'L_Eyelids_Up_13_Ctrl', 'L_Eyelids_Dw_10_Loc', 'R_Eyelids_Up_4_Bnd', 'L_Eyelids_Up_8_Jnt_Offset_Grp', 'R_Eyelids_Up_WireDriver_CrvBaseWire', 'L_Eyelids_UpMid_Ctrl_Offset_Grp', 'L_Eyelids_Up_13_Loc', 'L_Eyelids_UpMid_Jnt', 'L_Eyelids_Dw_7_Ctrl_OffsetPivot_Grp_Offset_Grp', 'R_Eyelids_Up_1_Bnd', 'L_Eyelids_Up_WireDriver_ClusterCrvBaseWire_cv_1__clst_rev', 'L_Eyelids_Dw_11_Ctrl_tag', 'R_Eyelids_Dw_WireDriver_ClusterCrvBaseWire_cv_5__md5', 'R_Eyelids_Dw_8_Ctrl_Offset_Grp', 'L_Eyelids_DwStart_Jnt_Offset_Grp', 'L_Eyelids_Dw_2_Ctrl_Offset_Grp', 'R_Eyelids_Dw_3_POCI', 'L_Eyelids_Dw_WireDriver_ClusterCrvBaseWire_cv_1__md5', 'L_Eyelids_DwStart_CtrlShape', 'R_Eyelids_Dw_11_Ctrl', 'R_Eyelids_Up_0_Bnd_scaleConstraint1', 'L_Eyelids_Up_10_Jnt_Offset_Grp', 'L_Eyelids_Blink_CrvBaseWire1', 'L_Eyelids_Up_1_Jnt_Offset_Grp', 'R_Eyelids_DwStart_Jnt_Offset_Grp', 'L_Eyelids_Dw_1_CtrlShape', 'L_Eyelids_UpStart_CtrlShape', 'LwrBlink_MultDiv5', 'R_Eyelids_Up_WireDriver_ClusterCrvBaseWire_cv_4__clst_bc', 'R_Eyelids_Dw_WireDriver_ClusterCrvBaseWireShapeOrig1', 'L_Eyelids_Blink_CrvBaseWire1ShapeOrig2', 'L_Eyelids_Blink_CrvShapeOrig1', 'L_Eyelids_Up_10_Bnd_parentConstraint1', 'R_Eyelids_Dw_WireDriver_ClusterCrvBaseWire_cv_1__jnt_bc', 'R_Eyelids_Up_Scale_Grp_Offset_Grp', 'L_Eyelids_Up_Origin_8_Jnt_aimConstraint1', 'R_Eyelids_Dw_Origin_9_Jnt_Offset_Grp', 'R_Eyelids_Up_0_Loc', 'R_Eyelids_Up_WireDriver_ClusterCrvBaseWireBaseWireShape', 'L_Eyelids_Dw_Origin_11_Jnt_aimConstraint1', 'R_Eyelids_Dw_12_Bnd_scaleConstraint1', 'R_Eyelids_Dw_Origin_7_Jnt_aimConstraint1', 'R_Eyelids_Up_7_POCI', 'L_Eyelids_Dw_2_Ctrl_tag', 'L_Eyelids_Dw_6_Ctrl_Offset_Grp', 'R_Eyelids_Up_1_Ctrl_tag', 'L_Eyelids_Dw_11_Ctrl_Offset_Grp', 'R_Eyelids_Up_6_Jnt', 'R_Eyelids_Dw_11_CtrlShape', 'R_Eyelids_Dw_9_Jnt', 'R_Eyelids_DwStartMid_Ctrl_Offset_Grp_parentConstraint1', 'L_Eyelids_Dw_11_POCI', 'L_Eyelids_Scale_CtrlShape', 'L_Eyelids_Dw_9_CtrlShape', 'L_Eyelids_Up_Origin_1_Jnt_Offset_Grp', 'R_Eyelids_Dw_12_Ctrl_Offset_Grp', 'L_Eyelids_Up_Scale_CtrlShape', 'L_Eyelids_DwEndMid_Jnt_Offset_Grp', 'R_Eyelids_UpStartMid_clusterHandle', 'R_Eyelids_Up_2_Loc', 'R_Eyelids_UpEndMid_CtrlShape', 'R_Eyelids_Up_VtxJnts_Grp', 'R_Eyelids_UpStartMid_CtrlShape', 'L_Eyelids_Dw_Origin_2_Jnt', 'L_Eyelids_DwEnd_Ctrl_Offset_Grp', 'L_Eyelids_Up_11_LocShape', 'R_Eyelids_Up_Origin_10_Jnt_aimConstraint1', 'L_Eyelids_Dw_6_Ctrl_tag', 'L_Eyelids_Dw_Origin_8_Jnt', 'L_Eyelids_Dw_WireDriver_ClusterCrvBaseWireBaseWire', 'R_Eyelids_UpMid_CtrlShape', 'L_Eyelids_Scale_Grp', 'L_Eyelids_Up_6_LocShape', 'L_Eyelids_Up_WireDriver_ClusterCrvBaseWire_cv_5__jnt_bc5', 'R_Eyelids_Up_13_Jnt_Offset_Grp', 'R_Eyelids_Up_ClusterWire', 'L_Eyelids_BlinkAttrs_Ctrl_tag', 'R_Eyelids_Up_Origin_0_Jnt', 'L_Eyelids_Scale_Jnt_Offset_Grp', 'R_Eyelids_Up_WireDriver_Crv', 'L_Eyelids_Dw_3_Jnt', 'R_Eyelids_Up_10_POCI', 'L_Eyelids_Dw_Scale_Ctrl_tag', 'L_Eyelids_Up_0_LocShape', 'L_Eyelids_Up_8_Bnd_scaleConstraint1', 'L_Eyelids_Dw_2_Ctrl_OffsetPivot_Grp', 'L_Eyelids_Dw_9_Ctrl_tag', 'R_Eyelids_Dw_1_Bnd_scaleConstraint1', 'L_Eyelids_Up_WireDriver_ClusterCrvBaseWire_cv_0__clst_rev', 'L_Eyelids_Up_7_Ctrl_OffsetPivot_Grp', 'L_Eyelids_Up_WireDriver_Crv', 'R_Eyelids_Up_11_Ctrl_OffsetPivot_Grp_Offset_Grp', 'R_Eyelids_Dw_Scale_CtrlShape', 'R_Eyelids_Dw_3_Jnt', 'R_Eyelids_Dw_5_Bnd_parentConstraint1', 'L_Eyelids_DwMid_clusterHandle', 'R_Eyelids_Dw_1_POCI', 'R_Eyelids_Dw_7_Ctrl', 'R_Eyelids_Up_4_CtrlShape', 'R_Eyelids_Up_8_Ctrl_OffsetPivot_Grp', 'R_Eyelids_Up_10_Ctrl_OffsetPivot_Grp', 'R_Eyelids_Ctrl_Grp_parentConstraint1', 'R_Eyelids_Blink_CrvShapeOrig2', 'R_Eyelids_DwEnd_Ctrl', 'L_Eyelids_Dw_8_Loc', 'R_Eyelids_UpStartMid_cluster', 'L_Eyelids_Dw_WireDriver_CrvShape', 'L_Eyelids_Dw_Origin_5_Jnt', 'L_Eyelids_DwStartMid_CtrlShape', 'L_Eyelids_Dw_3_Bnd', 'R_Eyelids_Dw_5_Ctrl', 'skinCluster3', 'R_Eyelids_UpStartMid_Ctrl_Offset_Grp_parentConstraint1', 'L_Eyelids_Up_Vtx_CrvShape', 'L_Eyelids_Dw_Origin_11_Jnt_Offset_Grp', 'L_Eyelids_Up_WireDriver_ClusterCrvBaseWire_cv_5__clst_bc', 'L_Eyelids_Up_Origin_12_Jnt', 'R_Eyelids_Scale_Ctrl_tag', 'L_Eyelids_Dw_Origin_0_Jnt_aimConstraint1', 'L_Eyelids_Up_12_Bnd', 'R_Eyelids_UpStart_cluster1Handle', 'L_Eyelids_UpStartMid_cluster', 'R_Eyelids_Dw_1_Ctrl_OffsetPivot_Grp_Offset_Grp', 'R_Eyelids_UpEnd_clusterHandle', 'L_Eyelids_Dw_4_Ctrl_tag', 'L_Eyelids_Dw_2_POCI', 'R_Eyelids_Dw_8_Jnt_Offset_Grp', 'R_Eyelids_Up_10_CtrlShape', 'L_Eyelids_Up_10_Ctrl_Offset_Grp', 'L_Eyelids_Up_Origin_4_Jnt_aimConstraint1', 'R_Eyelids_Dw_10_Ctrl_OffsetPivot_Grp', 'bindPose2', 'L_Eyelids_UpEndMid_Jnt_Offset_Grp_parentConstraint1', 'L_Eyelids_Dw_7_Jnt_Offset_Grp', 'L_Eyelids_Up_3_Bnd_parentConstraint1', 'L_Eyelids_Up_1_POCI', 'R_Eyelids_Up_WireDriver_ClusterCrvBaseWireShapeOrig', 'L_Eyelids_Dw_BlinkTarget_CrvShape', 'L_Eyelids_DwMid_Jnt', 'R_Eyelids_Dw_7_LocShape', 'R_Eyelids_Up_12_Ctrl_tag', 'R_Eyelids_Dw_1_Ctrl_tag', 'R_Eyelids_Up_13_Ctrl', 'L_Eyelids_Dw_12_Ctrl_tag', 'L_Eyelids_Up_Origin_3_Jnt_aimConstraint1', 'L_Eyelids_Blink_CrvBaseWireShapeOrig', 'R_Eyelids_Up_Ctrl_Grp', 'R_Eyelids_Blink_BS', 'LwrBlink_MultDiv3', 'L_Eyelids_Up_4_Ctrl_OffsetPivot_Grp', 'R_Eyelids_Dw_10_Bnd_scaleConstraint1', 'R_Eyelids_UpStart_clusterHandle', 'R_Eyelids_DwEnd_Ctrl_tag', 'R_Eyelids_Dw_WireDriver_ClusterCrvBaseWire_cv_2__clst_rev', 'L_EyelidsLwrBlink_Ctrl_Offset_Grp', 'L_Eyelids_Up_11_Loc', 'R_Eyelids_Up_9_Bnd_scaleConstraint1', 'R_Eyelids_Dw_Origin_8_Jnt_aimConstraint1', 'L_Eyelids_Dw_WireDriver_ClusterCrvBaseWire_cv_3__jnt_bc', 'R_Eyelids_Up_3_Ctrl_tag', 'L_Eyelids_Up_12_LocShape', 'R_Eyelids_Dw_2_Ctrl', 'LwrBlink_MultDiv', 'R_Eyelids_Up_8_Ctrl_Offset_Grp', 'L_Eyelids_Dw_Origin_1_Jnt_Offset_Grp', 'L_Eyelids_Dw_5_LocShape', 'L_Eyelids_Up_9_LocShape', 'R_Eyelids_BlinkAttrs_CtrlShape', 'R_Eyelids_Dw_Origin_0_Jnt_aimConstraint1', 'R_Eyelids_Dw_6_POCI', 'L_Eyelids_Dw_0_Ctrl_OffsetPivot_Grp_Offset_Grp', 'L_Eyelids_Dw_3_Loc', 'R_Eyelids_Dw_7_Bnd_scaleConstraint1', 'R_Eyelids_UpEnd_cluster1HandleShape', 'L_Eyelids_Dw_WireDriver_ClusterCrvBaseWire_cv_2__md5', 'R_Eyelids_Dw_Origin_9_Jnt', 'L_Eyelids_Up_4_Ctrl_tag', 'R_Eyelids_DwStart_cluster', 'L_Eyelids_Blink_CrvBaseWireShapeOrig2', 'L_Eyelids_Dw_WireDriver_ClusterCrvBaseWire_cv_5__clst_rev', 'R_Eyelids_DwEndMid_Jnt', 'R_Eyelids_Up_WireDriver_ClusterCrvBaseWire', 'R_Eyelids_Up_Origin_12_Jnt_Offset_Grp', 'L_Eyelids_UpEnd_Ctrl_Offset_Grp', 'R_Eyelids_DwStartMid_Ctrl_Offset_Grp', 'R_Eyelids_Dw_3_LocShape', 'L_Eyelids_Up_3_Ctrl_OffsetPivot_Grp', 'L_Eyelids_Dw_10_Ctrl_OffsetPivot_Grp_Offset_Grp', 'L_Eyelids_Up_11_CtrlShape', 'L_Eyelids_Blink_CrvShapeOrig2', 'R_Eyelids_DwStart_cluster1HandleShape', 'L_Eyelids_Dw_WireDriver_ClusterCrvBaseWire_cv_6__clst_rev', 'L_Eyelids_Up_13_LocShape', 'L_Eyelids_Up_12_Jnt', 'L_Eyelids_Up_13_Jnt', 'R_Eyelids_Up_WireDriver_ClusterCrvBaseWire_cv_5__clst_bc', 'L_Eyelids_DwEnd_CtrlShape', 'R_Eyelids_Dw_8_Ctrl_OffsetPivot_Grp_Offset_Grp', 'R_Eyelids_Up_12_Ctrl_Offset_Grp', 'R_EyelidsLwrBlink_Ctrl', 'LwrBlink_MultDiv4', 'L_Eyelids_Dw_3_Bnd_parentConstraint1', 'R_Eyelids_Up_12_Ctrl_OffsetPivot_Grp_Offset_Grp', 'L_Eyelids_UpMid_Ctrl_tag', 'R_Eyelids_Up_WireDriver_ClusterCrvBaseWire_cv_5__jnt_bc5', 'L_Eyelids_Dw_1_Bnd_parentConstraint1', 'L_Eyelids_Up_WireDriver_ClusterCrvBaseWire_cv_6__md5', 'L_Eyelids_Dw_WireDriver_ClusterCrvBaseWireBaseWireShapeOrig', 'R_Eyelids_Dw_8_Bnd_scaleConstraint1', 'R_Eyelids_Dw_WireDriver_CrvShape', 'L_Eyelids_UpEnd_cluster1HandleShape', 'L_Eyelids_Up_5_Ctrl_OffsetPivot_Grp', 'R_Eyelids_Up_8_Jnt_Offset_Grp', 'L_Eyelids_Dw_0_Ctrl_OffsetPivot_Grp', 'R_Eyelids_Dw_7_Loc', 'L_Eyelids_Up_7_Loc', 'R_Eyelids_Up_11_POCI', 'L_Eyelids_Up_Jnt_Grp', 'L_Eyelids_Up_7_Bnd_scaleConstraint1', 'L_Eyelids_Dw_12_Jnt', 'R_Eyelids_Dw_6_Ctrl_OffsetPivot_Grp_Offset_Grp', 'R_Eyelids_Dw_9_LocShape', 'R_Eyelids_Dw_ClusterWire', 'R_Eyelids_Up_WireDriver_ClusterCrvBaseWire_cv_0__jnt_bc5', 'R_Eyelids_Up_11_Bnd_parentConstraint1', 'L_Eyelids_Dw_Scale_Grp_Offset_Grp', 'L_Eyelids_Up_0_Ctrl_tag', 'R_Eyelids_UpEndMid_Jnt_Offset_Grp_parentConstraint1', 'unitConversion4', 'R_Eyelids_Dw_2_Loc', 'R_Eyelids_Dw_Origin_6_Jnt_aimConstraint1', 'R_Eyelids_DwStart_Ctrl_Offset_Grp', 'L_Eyelids_Up_11_Jnt_Offset_Grp', 'L_Eyelids_Up_0_Loc', 'R_Eyelids_Dw_4_Loc', 'R_Eyelids_Dw_3_Ctrl_tag', 'R_Eyelids_DwEnd_clusterHandle', 'R_Eyelids_Up_Origin_13_Jnt_Offset_Grp', 'L_Eyelids_Dw_6_Ctrl_OffsetPivot_Grp', 'L_Eyelids_Up_13_Ctrl_OffsetPivot_Grp_Offset_Grp', 'L_Eyelids_Dw_4_Bnd_parentConstraint1', 'L_Eyelids_Up_2_Jnt', 'R_Eyelids_Dw_1_Loc', 'L_Eyelids_Dw_9_POCI', 'L_Eyelids_Dw_WireDriver_ClusterCrvBaseWire_cv_4__clst_bc', 'R_Eyelids_Dw_WireDriver_ClusterCrvBaseWireShapeOrig', 'L_Eyelids_DwStartMid_Ctrl_Offset_Grp_parentConstraint1', 'R_Eyelids_Up_4_Ctrl_OffsetPivot_Grp', 'R_Eyelids_UpMid_clusterHandle', 'L_Eyelids_Dw_4_CtrlShape', 'L_Eyelids_Up_10_Bnd_scaleConstraint1', 'L_Eyelids_Blink_CrvBaseWire1ShapeOrig', 'R_Eyelids_Up_12_POCI', 'R_Eyelids_UprBlink_BS', 'L_Eyelids_Dw_WireDriver_CrvShapeOrig', 'L_Eyelids_Up_Origin_6_Jnt_aimConstraint1', 'R_Eyelids_Dw_0_Ctrl_tag', 'R_Eyelids_Dw_0_Ctrl_Offset_Grp', 'L_Eyelids_Dw_7_Bnd_scaleConstraint1', 'R_Eyelids_Up_5_Bnd_scaleConstraint1', 'L_Eyelids_Dw_VtxJnts_Grp', 'R_Eyelids_Dw_11_Ctrl_Offset_Grp', 'L_Eyelids_Up_4_Loc', 'R_Eyelids_Up_2_Jnt_Offset_Grp', 'L_Eyelids_Up_2_Ctrl_OffsetPivot_Grp', 'L_Eyelids_Dw_9_Bnd_parentConstraint1', 'L_Eyelids_Up_3_Ctrl_Offset_Grp', 'R_Eyelids_UpEndMid_cluster', 'R_Eyelids_Dw_WireDriver_ClusterCrvBaseWire_cv_3__md5', 'L_Eyelids_DwMid_Jnt_Offset_Grp', 'R_Eyelids_Dw_3_Bnd_scaleConstraint1', 'L_Eyelids_Dw_9_Bnd_scaleConstraint1', 'R_Eyelids_DwEnd_cluster1', 'R_Eyelids_UpStartMid_clusterHandleShape', 'L_Eyelids_Dw_7_CtrlShape', 'L_Eyelids_Up_0_Ctrl_OffsetPivot_Grp_Offset_Grp', 'R_Eyelids_Up_3_LocShape', 'R_Eyelids_Up_4_POCI', 'L_Eyelids_UpStart_Ctrl_Offset_Grp', 'L_Eyelids_Dw_WireDriver_ClusterCrvBaseWire_cv_0__jnt_bc5', 'R_Eyelids_Dw_7_Ctrl_OffsetPivot_Grp', 'L_Eyelids_Up_1_Ctrl', 'L_Eyelids_Up_4_Jnt_Offset_Grp', 'L_Eyelids_Dw_9_Loc', 'L_Eyelids_LwrBlink_BS', 'R_Eyelids_Dw_Origin_4_Jnt_aimConstraint1', 'R_Eyelids_Up_Origin_6_Jnt_Offset_Grp', 'L_Eyelids_UpEnd_Ctrl_tag', 'L_Eyelids_Dw_Origin_6_Jnt_aimConstraint1', 'R_Eyelids_Dw_WireDriver_ClusterCrvBaseWire_cv_4__clst_rev', 'L_Eyelids_Dw_6_Jnt', 'L_Eyelids_Up_12_Loc', 'R_Eyelids_Up_2_Bnd', 'R_Eyelids_Dw_BlinkTarget_Crv', 'L_Eyelids_UpMid_cluster', 'R_Eyelids_DwEndMid_CtrlShape', 'L_Eyelids_Dw_8_Bnd', 'L_Eyelids_Up_10_Ctrl_OffsetPivot_Grp_Offset_Grp', 'L_Eyelids_UpStart_Jnt_Offset_Grp', 'L_Eyelids_Up_Origin_3_Jnt', 'L_Eyelids_Up_13_POCI', 'R_Eyelids_Dw_5_Bnd_scaleConstraint1', 'R_Eyelids_Up_13_Jnt', 'L_Eyelids_Up_12_Ctrl_Offset_Grp', 'L_Eyelids_Dw_6_POCI', 'L_Eyelids_Up_Ctrl_Grp', 'L_Eyelids_Up_11_Ctrl_tag', 'R_Eyelids_Dw_8_Bnd', 'R_Eyelids_Up_12_CtrlShape', 'L_Eyelids_DwMid_clusterHandleShape', 'R_Eyelids_Dw_7_Ctrl_Offset_Grp', 'unitConversion3', 'L_Eyelids_Blink_CrvShape', 'R_Eyelids_Dw_4_Ctrl', 'R_Eyelids_Dw_3_Jnt_Offset_Grp', 'L_Eyelids_Up_6_Bnd', 'L_Eyelids_Up_5_CtrlShape', 'L_EyelidsUprBlink_Ctrl', 'L_Eyelids_Scale_Jnt', 'R_Eyelids_Dw_6_Jnt_Offset_Grp', 'L_Eyelids_Scale_Ctrl', 'L_Eyelids_Up_12_Ctrl_OffsetPivot_Grp', 'R_Eyelids_Up_Jnt_Grp', 'R_Eyelids_Dw_7_Jnt_Offset_Grp', 'L_Eyelids_DwEndMid_clusterHandleShape', 'L_Eyelids_Dw_1_Ctrl', 'R_Eyelids_Up_11_LocShape', 'L_Eyelids_Up_3_Bnd_scaleConstraint1', 'R_Eyelids_Dw_7_Bnd', 'L_Eyelids_UpStart_clusterHandleShape', 'R_Eyelids_Dw_Origin_12_Jnt_Offset_Grp', 'L_Eyelids_Up_0_Bnd_scaleConstraint1', 'R_Eyelids_Dw_Origin_12_Jnt_aimConstraint1', 'R_Eyelids_Dw_3_Ctrl_OffsetPivot_Grp_Offset_Grp', 'R_Eyelids_Up_WireDriver_ClusterCrvBaseWire_cv_2__md5', 'L_Eyelids_Blink_CrvShapeOrig', 'L_Eyelids_Up_8_POCI', 'L_Eyelids_Dw_0_Jnt_Offset_Grp', 'L_Eyelids_Up_2_Ctrl_Offset_Grp', 'R_Eyelids_Up_0_Ctrl_Offset_Grp', 'L_Eyelids_UpEnd_cluster1Handle', 'L_Eyelids_Up_5_Jnt', 'R_Eyelids_Dw_0_CtrlShape', 'R_Eyelids_Up_5_Ctrl_OffsetPivot_Grp', 'L_Eyelids_Up_2_LocShape', 'R_Eyelids_Dw_Origin_8_Jnt', 'R_Eyelids_Blink_CrvBaseWireShapeOrig1', 'L_Eyelids_Dw_Origin_5_Jnt_aimConstraint1', 'R_Eyelids_Dw_3_CtrlShape', 'L_Eyelids_Dw_WireDriver_CrvShapeOrig1', 'L_Eyelids_Dw_9_Ctrl_OffsetPivot_Grp', 'L_Eyelids_Dw_WireDriver_Crv', 'R_Eyelids_Up_5_Ctrl_Offset_Grp', 'R_Eyelids_DwStart_Ctrl_tag', 'L_Eyelids_DwEnd_clusterHandleShape', 'L_Eyelids_Dw_Scale_Grp', 'L_Eyelids_UpMid_clusterHandle', 'R_Eyelids_Up_1_Ctrl_OffsetPivot_Grp_Offset_Grp', 'R_Eyelids_DwWire', 'L_Eyelids_Dw_2_Ctrl_OffsetPivot_Grp_Offset_Grp', 'L_Eyelids_DwMid_cluster', 'L_Eyelids_Up_6_Ctrl_OffsetPivot_Grp', 'R_Eyelids_BlinkAttrs_Ctrl_Offset_Grp', 'R_Eyelids_Dw_1_Ctrl_OffsetPivot_Grp', 'L_Eyelids_Up_5_LocShape', 'unitConversion2', 'L_Eyelids_Up_11_Bnd', 'R_Eyelids_Up_13_Ctrl_OffsetPivot_Grp_Offset_Grp', 'R_EyelidsLwrBlink_Ctrl_Offset_Grp', 'L_Eyelids_Up_7_LocShape', 'R_Eyelids_Up_WireDriver_ClusterCrvBaseWire_cv_5__md5', 'L_Eyelids_DwStartMid_Jnt', 'L_Eyelids_Dw_7_LocShape', 'L_Eyelids_Up_Origin_13_Jnt_aimConstraint1', 'L_Eyelids_Up_WireDriver_ClusterCrvBaseWire_cv_4__clst_rev', 'R_Eyelids_UpEnd_cluster1', 'L_Eyelids_Up_3_Jnt', 'L_Eyelids_Dw_10_Ctrl_Offset_Grp', 'R_Eyelids_Up_Origin_9_Jnt_Offset_Grp', 'L_Eyelids_UpEnd_Jnt', 'L_Eyelids_Dw_9_Jnt_Offset_Grp', 'R_Eyelids_Up_WireDriver_ClusterCrvBaseWire_cv_6__clst_bc', 'R_Eyelids_DwEndMid_clusterHandleShape', 'R_Eyelids_Up_Origin_13_Jnt', 'L_Eyelids_Dw_8_Ctrl_OffsetPivot_Grp_Offset_Grp', 'R_Eyelids_Up_6_Ctrl_OffsetPivot_Grp_Offset_Grp', 'L_Eyelids_Dw_Origin_9_Jnt_aimConstraint1', 'R_Eyelids_Up_Origin_12_Jnt', 'L_Eyelids_UpStartMid_CtrlShape', 'L_Eyelids_Dw_8_Ctrl_tag', 'L_Eyelids_UpStartMid_Ctrl_tag', 'L_Eyelids_Dw_0_Ctrl_Offset_Grp', 'L_Eyelids_Up_AimLocators_Grp', 'L_Eyelids_Blink_CrvBaseWire', 'R_Eyelids_Dw_5_LocShape', 'L_EyelidsUprBlink_CtrlShape', 'L_Eyelids_BlinkAttrs_CtrlShape', 'L_EyelidsLwrBlink_Ctrl', 'L_Eyelids_UpEndMid_clusterHandleShape', 'L_Eyelids_Up_Scale_Ctrl', 'R_Eyelids_Up_WireDriver_ClusterCrvBaseWire_cv_1__clst_bc', 'L_Eyelids_DwEnd_cluster1HandleShape', 'L_Eyelids_Dw_0_Bnd_parentConstraint1', 'L_Eyelids_Dw_1_Jnt', 'R_Eyelids_UpEndMid_Jnt_Offset_Grp', 'R_Eyelids_Dw_WireDriver_ClusterCrvBaseWire_cv_3__clst_rev', 'R_Eyelids_Up_WireDriver_CrvShapeOrig1', 'L_Eyelids_Dw_2_Ctrl', 'R_Eyelids_Up_Origin_8_Jnt_Offset_Grp', 'L_Eyelids_Up_1_Ctrl_Offset_Grp', 'R_Eyelids_Dw_Scale_Grp_Offset_Grp', 'R_Eyelids_Scale_Grp', 'L_Eyelids_Dw_WireDriver_ClusterCrvBaseWire_cv_2__jnt_bc', 'L_Eyelids_Up_WireDriver_ClusterCrvBaseWireShapeOrig', 'L_Eyelids_Up_Origin_4_Jnt_Offset_Grp', 'L_Eyelids_Up_Origin_0_Jnt', 'R_Eyelids_Up_4_Ctrl', 'R_Eyelids_UpStart_Ctrl', 'R_Eyelids_Dw_11_Jnt', 'R_Eyelids_Dw_WireDriver_ClusterCrvBaseWire_cv_0__md5', 'L_Eyelids_Dw_Origin_0_Jnt', 'R_Eyelids_Dw_4_Bnd', 'L_Eyelids_UpStartMid_Jnt_Offset_Grp_parentConstraint1', 'R_Eyelids_Up_Origin_11_Jnt_Offset_Grp', 'L_Eyelids_Up_1_Bnd_scaleConstraint1', 'L_Eyelids_Dw_4_Ctrl_Offset_Grp', 'R_Eyelids_DwEndMid_clusterHandle', 'L_Eyelids_Dw_5_POCI', 'L_Eyelids_DwEndMid_Ctrl', 'R_EyelidsUprBlink_Ctrl_Offset_Grp', 'L_Eyelids_Dw_2_Jnt', 'R_Eyelids_Up_WireDriver_ClusterCrvBaseWire_cv_3__clst_bc', 'UprBlink_MultDiv', 'L_Eyelids_Up_1_Ctrl_tag', 'L_Eyelids_Up_7_Bnd', 'R_Eyelids_Up_10_Bnd', 'L_Eyelids_Up_Origin_9_Jnt', 'L_Eyelids_Up_1_LocShape', 'R_Eyelids_Up_8_Ctrl_tag', 'L_Eyelids_Dw_4_Jnt', 'R_Eyelids_Up_0_Ctrl_OffsetPivot_Grp_Offset_Grp', 'R_Eyelids_Up_2_Ctrl_Offset_Grp', 'R_Eyelids_Up_Origin_5_Jnt_aimConstraint1', 'L_Eyelids_Dw_12_Ctrl_OffsetPivot_Grp', 'L_Eyelids_Dw_9_Ctrl_Offset_Grp', 'L_EyelidsLwrBlink_CtrlShape', 'L_Eyelids_Up_5_Bnd_parentConstraint1', 'L_Eyelids_Up_Origin_8_Jnt_Offset_Grp', 'L_Eyelids_Dw_3_POCI', 'L_Eyelids_Dw_Origin_10_Jnt_Offset_Grp', 'L_Eyelids_Up_9_Jnt', 'R_Eyelids_Dw_4_Jnt_Offset_Grp', 'R_Eyelids_UpMid_Ctrl_Offset_Grp', 'R_Eyelids_Dw_4_Jnt', 'R_Eyelids_Dw_0_POCI', 'L_Eyelids_Dw_Origin_5_Jnt_Offset_Grp', 'R_Eyelids_Dw_2_Jnt', 'R_Eyelids_Dw_5_Jnt_Offset_Grp', 'R_Eyelids_UpStart_CtrlShape', 'L_Eyelids_Up_9_CtrlShape', 'R_Eyelids_Up_WireDriver_ClusterCrvBaseWire_cv_1__md5', 'R_Eyelids_Dw_Origin_7_Jnt', 'L_Eyelids_Up_1_Bnd_parentConstraint1', 'R_Eyelids_Up_4_Ctrl_OffsetPivot_Grp_Offset_Grp', 'L_Eyelids_Up_9_Loc', 'R_Eyelids_Dw_WireDriver_ClusterCrvBaseWire_cv_1__clst_bc', 'L_Eyelids_DwStart_cluster1Handle', 'L_Eyelids_Dw_3_Ctrl_OffsetPivot_Grp_Offset_Grp', 'R_Eyelids_Up_6_Ctrl_OffsetPivot_Grp', 'L_Eyelids_Dw_WireDriver_ClusterCrvBaseWire_cv_1__clst_bc', 'R_EyelidsUprBlink_Ctrl_tag', 'R_Eyelids_DwEndMid_Ctrl_tag', 'L_Eyelids_Dw_3_Ctrl_tag', 'L_Eyelids_Dw_WireDriver_ClusterCrvBaseWire_cv_6__clst_bc', 'L_Eyelids_Dw_WireDriver_ClusterCrvBaseWire_cv_4__clst_rev', 'L_Eyelids_Dw_10_Bnd_parentConstraint1', 'L_Eyelids_Up_BlinkTarget_Crv', 'L_Eyelids_Dw_Wire', 'R_Eyelids_Dw_Origin_5_Jnt_aimConstraint1', 'L_Eyelids_Dw_8_Ctrl_Offset_Grp', 'R_Eyelids_Dw_WireDriver_ClusterCrvBaseWire_cv_5__clst_bc', 'R_Eyelids_Up_WireDriver_CrvShapeOrig', 'R_Eyelids_Up_4_LocShape', 'R_Eyelids_Dw_9_Bnd_scaleConstraint1', 'L_Eyelids_Dw_Origin_12_Jnt_aimConstraint1', 'L_Eyelids_UpVector_LocShape', 'R_Eyelids_Up_4_Loc', 'L_Eyelids_Dw_10_Jnt', 'R_Eyelids_Dw_9_POCI', 'R_Eyelids_Dw_10_Ctrl_Offset_Grp', 'L_Eyelids_Dw_WireDriver_ClusterCrvBaseWireShapeOrig1', 'R_Eyelids_Dw_4_CtrlShape', 'R_Eyelids_Up_Vtx_CrvShape', 'L_Eyelids_Up_1_Jnt', 'L_Eyelids_Up_0_Ctrl_OffsetPivot_Grp', 'R_Eyelids_Up_0_Bnd_parentConstraint1', 'L_Eyelids_Rig_Grp', 'L_Eyelids_Up_2_Loc', 'R_Eyelids_Dw_8_Ctrl_tag', 'R_Eyelids_Dw_Origin_2_Jnt', 'L_Eyelids_Dw_1_POCI', 'L_Eyelids_Up_Origin_0_Jnt_aimConstraint1', 'R_Eyelids_Up_BlinkTarget_CrvShapeOrig', 'R_Eyelids_DwEnd_CtrlShape', 'L_Eyelids_Dw_Origin_4_Jnt', 'L_Eyelids_Up_2_Jnt_Offset_Grp', 'L_Eyelids_Up_WireDriver_ClusterCrvBaseWire_cv_3__clst_bc', 'R_Eyelids_UpStartMid_Jnt_Offset_Grp_parentConstraint1', 'R_Eyelids_Dw_WireDriver_ClusterCrvBaseWireShape', 'R_Eyelids_Dw_7_Bnd_parentConstraint1', 'L_Eyelids_Dw_8_Bnd_scaleConstraint1', 'L_Eyelids_Up_WireDriver_ClusterCrvBaseWire_cv_6__clst_rev', 'L_Eyelids_Up_WireDriver_ClusterCrvBaseWire', 'R_EyelidsLwrBlink_Ctrl_tag', 'R_Eyelids_Up_6_POCI', 'R_Eyelids_UpStartMid_Jnt_Offset_Grp', 'R_Eyelids_Dw_8_CtrlShape', 'R_Eyelids_Up_0_LocShape', 'R_Eyelids_DwStart_cluster1Handle', 'R_Eyelids_Up_WireDriver_ClusterCrvBaseWire_cv_4__clst_rev', 'R_Eyelids_EyePivot_Loc', 'L_Eyelids_BlinkAttrs_Ctrl_Offset_Grp', 'R_Eyelids_Up_9_Ctrl_OffsetPivot_Grp', 'L_Eyelids_Up_2_Bnd_parentConstraint1', 'R_Eyelids_Up_5_POCI', 'L_Eyelids_Up_13_Bnd_parentConstraint1', 'R_Eyelids_DwStartMid_Ctrl_tag', 'L_Eyelids_DwMid_Ctrl_Offset_Grp', 'L_Eyelids_Dw_8_Ctrl_OffsetPivot_Grp', 'R_Eyelids_DwMid_Jnt_Offset_Grp', 'L_Eyelids_Up_BlinkTarget_CrvShapeOrig1', 'L_Eyelids_UpStart_Ctrl_tag', 'R_Eyelids_Dw_7_POCI', 'L_Eyelids_Dw_WireDriver_ClusterCrvBaseWire_cv_3__md5', 'L_Eyelids_Up_10_Ctrl_OffsetPivot_Grp', 'R_Eyelids_BlinkAttrs_Ctrl', 'R_Eyelids_UpMid_Jnt', 'L_Eyelids_Up_4_Ctrl_Offset_Grp', 'L_Eyelids_Up_5_Ctrl_OffsetPivot_Grp_Offset_Grp', 'R_Eyelids_Dw_3_Bnd_parentConstraint1', 'L_Eyelids_Dw_Origin_1_Jnt_aimConstraint1', 'L_Eyelids_UpEnd_Ctrl', 'L_Eyelids_Up_4_Ctrl_OffsetPivot_Grp_Offset_Grp', 'R_Eyelids_Up_1_Jnt_Offset_Grp', 'L_Eyelids_Up_WireDriver_CrvShapeOrig', 'L_Eyelids_Blink_CrvBaseWireShapeOrig1', 'R_Eyelids_Dw_12_Ctrl_tag', 'L_Eyelids_Dw_10_LocShape', 'R_Eyelids_Dw_4_Bnd_scaleConstraint1', 'L_Eyelids_Dw_12_Bnd', 'skinCluster1', 'L_Eyelids_Up_WireDriver_ClusterCrvBaseWire_cv_0__clst_bc', 'L_Eyelids_Up_7_Jnt_Offset_Grp', 'R_Eyelids_Dw_Origin_0_Jnt_Offset_Grp', 'R_Eyelids_Up_WireDriver_ClusterCrvBaseWireBaseWireShapeOrig1', 'R_Eyelids_Dw_WireDriver_ClusterCrvBaseWire_cv_6__md5', 'L_Eyelids_Up_5_Loc', 'L_Eyelids_Dw_2_CtrlShape', 'R_Eyelids_Up_Origin_4_Jnt_aimConstraint1', 'R_Eyelids_Dw_0_Ctrl_OffsetPivot_Grp', 'R_Eyelids_Up_8_Bnd_parentConstraint1', 'L_Eyelids_Dw_WireDriver_ClusterCrvBaseWireShapeOrig', 'L_Eyelids_Up_5_Bnd', 'R_Eyelids_Up_8_LocShape', 'R_Eyelids_Dw_Origin_11_Jnt_Offset_Grp', 'R_Eyelids_UpStartMid_Jnt', 'R_Eyelids_Up_0_Jnt', 'R_Eyelids_Dw_10_Ctrl', 'L_Eyelids_Dw_0_CtrlShape', 'R_Eyelids_Dw_10_Jnt', 'R_Eyelids_Up_Vtx_CrvShapeOrig', 'L_Eyelids_Up_Origin_5_Jnt_aimConstraint1', 'skinCluster4', 'R_EyelidsLwrBlink_CtrlShape', 'L_Eyelids_Up_7_POCI', 'R_Eyelids_Up_Origin_3_Jnt_Offset_Grp', 'R_Eyelids_Dw_Origin_3_Jnt_Offset_Grp', 'R_Eyelids_Up_8_Ctrl', 'L_Eyelids_Up_12_Bnd_scaleConstraint1', 'R_Eyelids_Dw_8_Ctrl_OffsetPivot_Grp', 'R_Eyelids_Scale_Jnt', 'L_Eyelids_Up_6_Ctrl_tag', 'R_Eyelids_Up_8_CtrlShape', 'R_Eyelids_Dw_2_Bnd_scaleConstraint1', 'L_Eyelids_Dw_0_Loc', 'R_Eyelids_DwEnd_Jnt_Offset_Grp', 'R_Eyelids_Dw_Scale_Grp', 'L_Eyelids_Dw_4_LocShape', 'L_Eyelids_UpStart_Jnt', 'R_Eyelids_Dw_5_Ctrl_Offset_Grp', 'R_Eyelids_Dw_5_Ctrl_OffsetPivot_Grp_Offset_Grp', 'L_Eyelids_Dw_WireDriver_CrvBaseWireShape', 'L_Eyelids_UpEnd_cluster1', 'R_Eyelids_Up_11_Ctrl_Offset_Grp', 'R_Eyelids_Up_2_Bnd_scaleConstraint1', 'R_Eyelids_UpEnd_Ctrl_tag', 'R_Eyelids_Dw_Origin_1_Jnt_Offset_Grp', 'L_Eyelids_Up_10_Ctrl', 'L_Eyelids_Dw_9_Ctrl_OffsetPivot_Grp_Offset_Grp', 'R_Eyelids_Dw_9_Ctrl_OffsetPivot_Grp_Offset_Grp', 'L_Eyelids_Dw_Origin_6_Jnt_Offset_Grp', 'R_Eyelids_Up_WireDriver_ClusterCrvBaseWire_cv_3__jnt_bc', 'R_Eyelids_UpMid_Ctrl', 'L_Eyelids_Up_WireDriver_CrvBaseWireShapeOrig', 'L_Eyelids_Up_12_Ctrl_OffsetPivot_Grp_Offset_Grp', 'R_Eyelids_Up_3_Ctrl', 'R_Eyelids_UpEnd_cluster1Handle', 'L_Eyelids_Up_WireDriver_ClusterCrvBaseWire_cv_2__jnt_bc', 'L_Eyelids_Dw_2_LocShape', 'L_Eyelids_Up_12_Ctrl', 'R_Eyelids_DwStart_Jnt', 'L_Eyelids_Up_5_Ctrl_Offset_Grp', 'R_Eyelids_Up_Origin_9_Jnt', 'L_Eyelids_UpStartMid_clusterHandleShape', 'R_Eyelids_Up_Origin_13_Jnt_aimConstraint1', 'L_Eyelids_Dw_ClusterWire', 'L_Eyelids_Up_BlinkTarget_CrvShape', 'L_Eyelids_DwEndMid_cluster', 'R_Eyelids_Dw_9_Ctrl_tag', 'R_Eyelids_Up_3_Jnt', 'L_Eyelids_Up_10_Jnt', 'L_Eyelids_Blink_BS', 'R_Eyelids_Up_3_Bnd_scaleConstraint1', 'BodyEyesShapeOrig1', 'R_Eyelids_Up_1_Jnt', 'L_Eyelids_Up_0_Ctrl_Offset_Grp', 'R_Eyelids_Dw_2_Jnt_Offset_Grp', 'R_Eyelids_Up_WireDriver_ClusterCrvBaseWire_cv_4__md5', 'R_Eyelids_Dw_7_CtrlShape', 'R_Eyelids_Dw_Jnt_Grp', 'R_Eyelids_UpWire', 'L_Eyelids_Dw_6_LocShape', 'L_Eyelids_Scale_Bnd', 'R_Eyelids_Up_3_POCI', 'L_Eyelids_Up_Origin_12_Jnt_aimConstraint1', 'L_Eyelids_Up_9_Bnd_parentConstraint1', 'L_Eyelids_Up_WireDriver_CrvShape', 'R_Eyelids_DwEnd_Jnt', 'R_Eyelids_Up_2_Jnt', 'R_Eyelids_Up_11_Ctrl', 'R_Eyelids_Up_1_Bnd_scaleConstraint1', 'L_Eyelids_Up_WireDriver_ClusterCrvBaseWireShape', 'R_Eyelids_Dw_Origin_11_Jnt_aimConstraint1', 'R_Eyelids_Up_7_Ctrl_Offset_Grp', 'R_Eyelids_Dw_WireDriver_ClusterCrvBaseWire_cv_2__md5', 'R_Eyelids_Up_12_LocShape', 'L_Eyelids_Dw_WireDriver_ClusterCrvBaseWireBaseWireShape', 'R_Eyelids_Dw_11_LocShape', 'R_Eyelids_UpVector_LocShape', 'L_Eyelids_Up_0_Ctrl', 'R_Eyelids_DwEnd_cluster', 'L_Eyelids_Up_Vtx_Crv', 'L_Eyelids_Up_2_Ctrl', 'R_Eyelids_Blink_CrvBaseWire1ShapeOrig2', 'L_Eyelids_Dw_WireDriver_ClusterCrvBaseWire_cv_0__clst_rev', 'L_Eyelids_Up_11_Ctrl_OffsetPivot_Grp', 'R_Eyelids_Dw_Origin_6_Jnt_Offset_Grp', 'R_Eyelids_Up_2_Ctrl_OffsetPivot_Grp', 'R_Eyelids_Dw_WireDriver_ClusterCrvBaseWire_cv_6__clst_rev', 'R_Eyelids_Up_WireDriver_ClusterCrvBaseWire_cv_6__clst_rev', 'R_Eyelids_Dw_Origin_5_Jnt', 'R_Eyelids_Up_3_CtrlShape', 'L_Eyelids_Up_WireDriver_ClusterCrvBaseWire_cv_2__md5', 'L_Eyelids_Up_5_Bnd_scaleConstraint1', 'L_Eyelids_UpEndMid_clusterHandle', 'R_Eyelids_Up_9_Ctrl_Offset_Grp', 'R_Eyelids_Up_Origin_10_Jnt_Offset_Grp', 'R_Eyelids_DwMid_Jnt', 'R_Eyelids_Dw_5_CtrlShape', 'R_Eyelids_Up_12_Jnt', 'R_Eyelids_Dw_Origin_4_Jnt', 'L_Eyelids_Up_11_Jnt', 'R_Eyelids_Dw_2_Bnd', 'R_Eyelids_Dw_5_POCI', 'R_Eyelids_Dw_5_Ctrl_OffsetPivot_Grp', 'R_Eyelids_Up_2_Ctrl_tag', 'R_Eyelids_Up_WireDriver_ClusterCrvBaseWireShapeOrig1', 'R_Eyelids_UpStart_Ctrl_tag', 'L_Eyelids_UpMid_clusterHandleShape', 'R_Eyelids_Up_12_Loc', 'R_Eyelids_Dw_WireDriver_CrvBaseWireShape', 'L_Eyelids_Up_ClusterWire', 'R_Eyelids_Up_2_POCI', 'R_Eyelids_Blink_CrvBaseWire', 'L_Eyelids_DwEndMid_Ctrl_Offset_Grp_parentConstraint1', 'R_Eyelids_Dw_BlinkTarget_CrvShape', 'R_Eyelids_Up_Origin_6_Jnt', 'R_Eyelids_Dw_WireDriver_ClusterCrvBaseWire_cv_2__jnt_bc', 'L_Eyelids_Dw_12_Bnd_scaleConstraint1', 'L_Eyelids_Up_WireDriver_ClusterCrvBaseWire_cv_1__clst_bc', 'L_Eyelids_Up_3_LocShape', 'L_Eyelids_UpEnd_clusterHandle', 'L_Eyelids_Dw_Scale_Ctrl', 'R_Eyelids_Up_9_Bnd', 'L_Eyelids_Up_WireDriver_ClusterCrvBaseWire_cv_5__clst_rev', 'R_Eyelids_Up_8_Bnd_scaleConstraint1', 'L_Eyelids_Up_6_Bnd_scaleConstraint1', 'L_Eyelids_Dw_1_Bnd_scaleConstraint1', 'L_Eyelids_Dw_Origin_2_Jnt_aimConstraint1', 'L_Eyelids_Up_Origin_13_Jnt_Offset_Grp', 'R_Eyelids_Dw_2_Ctrl_tag', 'R_Eyelids_Up_6_Ctrl_Offset_Grp', 'L_Eyelids_Up_12_Ctrl_tag', 'L_Eyelids_Up_11_Ctrl_OffsetPivot_Grp_Offset_Grp', 'R_Eyelids_Dw_4_Ctrl_Offset_Grp', 'L_Eyelids_Up_4_Ctrl', 'L_Eyelids_Dw_3_Jnt_Offset_Grp', 'R_Eyelids_Up_1_LocShape', 'R_Eyelids_Up_Origin_1_Jnt', 'R_Eyelids_Dw_Origin_7_Jnt_Offset_Grp', 'R_Eyelids_Dw_1_Bnd_parentConstraint1', 'L_Eyelids_Up_WireDriver_ClusterCrvBaseWireShapeOrig1', 'L_Eyelids_Dw_9_Jnt', 'R_Eyelids_Up_3_Loc', 'L_Eyelids_Dw_6_Ctrl_OffsetPivot_Grp_Offset_Grp', 'L_Eyelids_Dw_Origin_11_Jnt', 'R_Eyelids_UpStartMid_Ctrl_tag', 'R_Eyelids_Up_3_Bnd', 'R_Eyelids_Up_3_Ctrl_OffsetPivot_Grp_Offset_Grp', 'R_Eyelids_Up_10_Jnt_Offset_Grp', 'L_Eyelids_Up_WireDriver_CrvBaseWireShape', 'L_Eyelids_DwEndMid_Ctrl_Offset_Grp', 'L_Eyelids_Up_WireDriver_CrvBaseWire', 'L_Eyelids_Dw_8_CtrlShape', 'L_Eyelids_Dw_0_Ctrl_tag', 'L_Eyelids_Dw_3_LocShape', 'LwrBlink_MultDiv2', 'L_Eyelids_Dw_WireDriver_ClusterCrvBaseWire_cv_4__md5', 'R_Eyelids_Blink_CrvBaseWire1ShapeOrig', 'R_Eyelids_BlinkAttrs_Ctrl_tag', 'L_EyelidsLwrBlink_Ctrl_tag', 'L_Eyelids_Dw_1_Ctrl_OffsetPivot_Grp_Offset_Grp', 'unitConversion1', 'L_Eyelids_Up_7_CtrlShape', 'R_Eyelids_UpEndMid_clusterHandleShape', 'L_Eyelids_Up_1_Ctrl_OffsetPivot_Grp', 'R_Eyelids_Up_6_CtrlShape', 'R_Eyelids_Dw_1_Bnd', 'R_Eyelids_Dw_6_Bnd', 'R_Eyelids_Dw_6_Ctrl_Offset_Grp', 'L_Eyelids_Dw_3_Bnd_scaleConstraint1', 'R_Eyelids_Dw_2_Ctrl_Offset_Grp', 'L_Eyelids_Dw_Origin_9_Jnt', 'L_Eyelids_UpEndMid_cluster', 'R_Eyelids_Dw_9_Loc', 'L_Eyelids_DwEndMid_Jnt', 'R_Eyelids_Dw_Origin_8_Jnt_Offset_Grp', 'L_Eyelids_UpStart_cluster1', 'L_Eyelids_Dw_0_Bnd', 'R_Eyelids_Dw_7_Ctrl_tag', 'R_Eyelids_Up_9_LocShape', 'R_Eyelids_Blink_CrvShapeOrig', 'R_Eyelids_DwStartMid_CtrlShape', 'L_Eyelids_UpStart_cluster1Handle', 'R_Eyelids_Dw_2_LocShape', 'R_Eyelids_UpStart_Jnt_Offset_Grp', 'R_Eyelids_UpEnd_Ctrl_Offset_Grp', 'L_Eyelids_Dw_12_Jnt_Offset_Grp', 'R_Eyelids_Up_13_Bnd', 'R_Eyelids_Dw_WireDriver_ClusterCrvBaseWire_cv_4__md5', 'R_Eyelids_Dw_0_Ctrl_OffsetPivot_Grp_Offset_Grp', 'L_Eyelids_UpMid_Ctrl', 'L_Eyelids_Dw_Origin_7_Jnt_Offset_Grp', 'L_Eyelids_Dw_6_Bnd_parentConstraint1', 'R_EyelidsUprBlink_CtrlShape', 'L_Eyelids_Up_0_Bnd_parentConstraint1', 'L_Eyelids_Up_Wire', 'R_Eyelids_Dw_12_Ctrl', 'R_Eyelids_Up_12_Jnt_Offset_Grp', 'R_Eyelids_Dw_1_CtrlShape', 'R_Eyelids_Dw_Origin_1_Jnt', 'R_Eyelids_Up_5_LocShape', 'R_Eyelids_Up_Origin_9_Jnt_aimConstraint1', 'L_Eyelids_Ctrl_Grp', 'L_Eyelids_Up_9_Ctrl_Offset_Grp', 'Mutant_Rig', 'R_Eyelids_Dw_2_Ctrl_OffsetPivot_Grp', 'L_Eyelids_DwStart_clusterHandleShape', 'R_Eyelids_Up_Origin_2_Jnt_aimConstraint1', 'L_Eyelids_Up_3_CtrlShape', 'R_Eyelids_Dw_3_Ctrl', 'R_Eyelids_DwEnd_cluster1Handle', 'L_Eyelids_Dw_7_POCI', 'L_Eyelids_Dw_10_Bnd_scaleConstraint1', 'R_Eyelids_Dw_9_Jnt_Offset_Grp', 'L_Eyelids_Up_WireDriver_ClusterCrvBaseWire_cv_6__clst_bc', 'R_Eyelids_Up_8_Loc', 'L_Eyelids_Up_2_Ctrl_tag', 'L_Eyelids_UpEndMid_Ctrl_tag', 'R_Eyelids_Up_WireDriver_ClusterCrvBaseWire_cv_5__clst_rev', 'R_Eyelids_Up_13_Ctrl_tag', 'L_Eyelids_Dw_9_LocShape', 'L_Eyelids_Up_Origin_2_Jnt', 'L_Eyelids_Up_WireDriver_ClusterCrvBaseWire_cv_2__clst_bc', 'R_Eyelids_Up_6_LocShape', 'L_Eyelids_Up_12_Jnt_Offset_Grp', 'L_Eyelids_Up_9_Ctrl_OffsetPivot_Grp_Offset_Grp', 'R_Eyelids_Up_0_Jnt_Offset_Grp', 'L_Eyelids_Dw_1_LocShape', 'L_Eyelids_Up_7_Jnt', 'L_Eyelids_Up_5_Ctrl', 'L_Eyelids_Up_Origin_6_Jnt', 'R_Eyelids_Up_7_Jnt', 'L_Eyelids_Up_1_Ctrl_OffsetPivot_Grp_Offset_Grp', 'L_Eyelids_Up_8_Jnt', 'R_Eyelids_UpEndMid_Ctrl', 'L_Eyelids_Up_8_Loc', 'L_Eyelids_Up_WireDriver_ClusterCrvBaseWire_cv_0__md5', 'R_Eyelids_Up_7_Loc', 'L_Eyelids_Dw_11_Bnd_scaleConstraint1', 'R_Eyelids_Up_10_Loc', 'L_Eyelids_BlinkAttrs_Ctrl', 'L_Eyelids_UpEndMid_Jnt', 'R_Eyelids_Dw_4_Ctrl_OffsetPivot_Grp', 'R_Eyelids_Rig_Grp', 'R_Eyelids_UpStart_Ctrl_Offset_Grp', 'L_Eyelids_Up_5_POCI', 'R_Eyelids_Up_8_POCI', 'R_Eyelids_UpEnd_cluster', 'R_Eyelids_DwEndMid_Ctrl_Offset_Grp_parentConstraint1', 'R_Eyelids_Up_5_Jnt', 'R_Eyelids_Dw_11_Bnd_parentConstraint1', 'R_Eyelids_Up_WireDriver_ClusterCrvBaseWire_cv_2__clst_bc', 'L_Eyelids_Up_4_Bnd_scaleConstraint1', 'L_Eyelids_DwStartMid_Ctrl_tag', 'L_Eyelids_Up_Scale_Grp_Offset_Grp', 'R_Eyelids_Dw_Ctrl_Grp', 'L_Eyelids_Up_13_Ctrl_Offset_Grp', 'R_Eyelids_Dw_Origin_1_Jnt_aimConstraint1', 'L_Eyelids_Dw_4_POCI', 'L_Eyelids_Dw_12_Ctrl', 'R_Eyelids_UpStart_cluster1', 'L_Eyelids_Dw_0_Jnt', 'R_Eyelids_Dw_WireDriver_ClusterCrvBaseWire', 'L_Eyelids_Dw_Origin_4_Jnt_Offset_Grp', 'R_Eyelids_Up_7_Bnd_scaleConstraint1', 'L_Eyelids_Up_WireDriver_ClusterCrvBaseWireBaseWireShapeOrig1', 'L_Eyelids_Dw_WireDriver_ClusterCrvBaseWire_cv_4__jnt_bc', 'R_Eyelids_Dw_9_Bnd_parentConstraint1', 'R_Eyelids_DwStart_cluster1', 'L_Eyelids_Dw_WireDriver_CrvBaseWire', 'L_Eyelids_Up_Origin_10_Jnt', 'L_Eyelids_Dw_WireDriver_ClusterCrvBaseWire_cv_5__clst_bc', 'R_Eyelids_Up_11_Jnt_Offset_Grp', 'L_Eyelids_Dw_7_Ctrl_Offset_Grp', 'L_Eyelids_Dw_11_Bnd', 'R_Eyelids_Up_WireDriver_ClusterCrvBaseWire_cv_2__jnt_bc', 'R_Eyelids_Up_0_Ctrl_tag', 'R_Eyelids_Up_WireDriver_ClusterCrvBaseWire_cv_0__clst_rev', 'R_Eyelids_Dw_WireDriver_ClusterCrvBaseWire_cv_2__clst_bc', 'L_Eyelids_Dw_3_Ctrl', 'L_Eyelids_Up_Origin_7_Jnt_Offset_Grp', 'L_Eyelids_DwEnd_cluster1', 'R_Eyelids_Dw_Origin_10_Jnt_aimConstraint1', 'R_Eyelids_Dw_7_Ctrl_OffsetPivot_Grp_Offset_Grp', 'L_Eyelids_Dw_Origin_12_Jnt', 'L_Eyelids_Up_9_POCI', 'R_Eyelids_Up_3_Bnd_parentConstraint1', 'R_Eyelids_Dw_8_Ctrl', 'L_Eyelids_Up_10_Loc', 'R_Eyelids_Up_Origin_4_Jnt', 'R_Eyelids_UpStart_Jnt', 'R_Eyelids_Dw_WireDriver_ClusterCrvBaseWire_cv_6__jnt_bc', 'R_Eyelids_Blink_CrvShapeOrig1', 'L_Eyelids_Up_8_CtrlShape', 'R_Eyelids_Up_10_Ctrl_Offset_Grp', 'R_Eyelids_Up_Tweeks_Ctrl_Grp', 'R_Eyelids_Blink_CrvBaseWireShapeOrig', 'R_Eyelids_Up_WireDriver_ClusterCrvBaseWire_cv_4__jnt_bc', 'L_Eyelids_Up_11_Bnd_scaleConstraint1', 'L_Eyelids_Up_8_LocShape', 'L_Eyelids_DwEnd_Jnt_Offset_Grp', 'R_Eyelids_Up_0_Ctrl', 'R_Eyelids_Up_9_Jnt_Offset_Grp', 'R_Eyelids_Dw_WireDriver_ClusterCrvBaseWireBaseWireShapeOrig', 'R_Eyelids_Up_Origin_8_Jnt_aimConstraint1', 'unitConversion6', 'R_Eyelids_Dw_6_Loc', 'L_Eyelids_DwWire', 'L_Eyelids_Ctrl_Grp_parentConstraint1', 'R_Eyelids_Scale_Ctrl_Offset_Grp', 'L_Eyelids_Up_Origin_10_Jnt_aimConstraint1', 'L_Eyelids_DwEndMid_Jnt_Offset_Grp_parentConstraint1', 'R_Eyelids_Dw_Scale_Ctrl', 'R_Eyelids_Up_13_LocShape', 'R_Eyelids_Up_3_Ctrl_OffsetPivot_Grp', 'R_Eyelids_Up_Origin_7_Jnt_Offset_Grp', 'R_Eyelids_Blink_CrvBaseWire1Shape', 'R_Eyelids_DwEndMid_Jnt_Offset_Grp', 'R_Eyelids_Up_9_Bnd_parentConstraint1', 'R_Eyelids_Up_6_Bnd_parentConstraint1', 'L_Eyelids_DwEndMid_Ctrl_tag', 'L_Eyelids_DwStart_Ctrl_Offset_Grp', 'L_Eyelids_Up_0_Jnt_Offset_Grp', 'R_Eyelids_Up_13_Bnd_scaleConstraint1', 'L_Eyelids_Blink_Reverse', 'L_Eyelids_Dw_10_Ctrl_OffsetPivot_Grp', 'L_Eyelids_Dw_5_Bnd_scaleConstraint1', 'R_Eyelids_Up_WireDriver_ClusterCrvBaseWire_cv_6__md5', 'L_Eyelids_Up_11_Ctrl_Offset_Grp', 'L_Eyelids_Dw_1_Ctrl_tag', 'L_Eyelids_Up_4_POCI', 'R_Eyelids_Up_6_Ctrl_tag', 'L_Eyelids_Scale_Bnd_scaleConstraint1', 'L_Eyelids_Dw_Origin_1_Jnt', 'R_Eyelids_Dw_Origin_10_Jnt', 'R_Eyelids_Dw_11_Ctrl_tag', 'R_Eyelids_Dw_Tweeks_Ctrl_Grp', 'R_Eyelids_Dw_2_CtrlShape', 'R_Eyelids_Scale_Grp_Offset_Grp', 'L_Eyelids_Dw_4_Ctrl', 'L_Eyelids_Up_Origin_1_Jnt_aimConstraint1', 'L_Eyelids_Dw_12_Ctrl_Offset_Grp', 'R_Eyelids_Up_10_Jnt', 'L_Eyelids_UpEnd_Jnt_Offset_Grp', 'R_Eyelids_Up_1_CtrlShape', 'L_Eyelids_Dw_5_Jnt_Offset_Grp', 'L_Eyelids_UpStartMid_Ctrl', 'R_Eyelids_Dw_5_Ctrl_tag', 'L_Eyelids_DwStartMid_Ctrl_Offset_Grp', 'R_Eyelids_UpMid_Ctrl_tag', 'R_Eyelids_Up_13_Ctrl_OffsetPivot_Grp', 'R_Eyelids_Up_9_Ctrl_OffsetPivot_Grp_Offset_Grp', 'L_Eyelids_Dw_Ctrl_Grp', 'L_Eyelids_Dw_Origin_2_Jnt_Offset_Grp', 'R_Eyelids_Up_Scale_Grp', 'L_Eyelids_Up_6_POCI', 'R_Eyelids_Dw_6_Jnt', 'L_Eyelids_Dw_11_Loc', 'L_Eyelids_Up_2_POCI', 'R_Eyelids_Up_12_Bnd', 'R_Eyelids_Dw_3_Loc', 'L_Eyelids_Dw_Origin_7_Jnt_aimConstraint1', 'L_Eyelids_DwEnd_cluster', 'R_Eyelids_Up_Origin_2_Jnt', 'L_Eyelids_Dw_2_Bnd_parentConstraint1', 'R_Eyelids_Dw_10_Loc', 'R_Eyelids_Up_7_Jnt_Offset_Grp', 'R_Eyelids_Up_WireDriver_CrvBaseWireShape', 'R_Eyelids_Dw_WireDriver_ClusterCrvBaseWire_cv_4__jnt_bc', 'R_Eyelids_Up_WireDriver_ClusterCrvBaseWire_cv_2__clst_rev', 'L_Eyelids_DwStartMid_clusterHandleShape', 'L_Eyelids_Dw_3_CtrlShape', 'L_Eyelids_Dw_6_Bnd_scaleConstraint1', 'R_Eyelids_Up_WireDriver_ClusterCrvBaseWireBaseWireShapeOrig', 'R_Eyelids_Dw_4_POCI', 'L_Eyelids_Up_1_Loc', 'L_Eyelids_Up_10_POCI', 'R_Eyelids_Up_6_Loc', 'L_Eyelids_UpStart_cluster1HandleShape', 'L_Eyelids_Dw_1_Jnt_Offset_Grp', 'L_Eyelids_Up_Origin_13_Jnt', 'L_Eyelids_Up_8_Ctrl_OffsetPivot_Grp', 'L_Eyelids_UpStart_clusterHandle', 'L_Eyelids_Dw_8_Bnd_parentConstraint1', 'R_Eyelids_Dw_Vtx_CrvShapeOrig', 'L_Eyelids_DwMid_Ctrl', 'R_Eyelids_Dw_11_Ctrl_OffsetPivot_Grp_Offset_Grp', 'L_Eyelids_Dw_BlinkTarget_Crv', 'R_Eyelids_Dw_8_LocShape', 'L_Eyelids_Dw_12_Ctrl_OffsetPivot_Grp_Offset_Grp', 'L_Eyelids_Up_WireDriver_ClusterCrvBaseWire_cv_4__md5', 'L_Eyelids_Dw_7_Jnt', 'R_Eyelids_Dw_Scale_Ctrl_Offset_Grp', 'L_EyelidsUprBlink_Ctrl_Offset_Grp', 'R_Eyelids_Dw_12_POCI', 'unitConversion5', 'L_Eyelids_Up_7_Ctrl_tag', 'R_Eyelids_Dw_10_LocShape', 'R_Eyelids_UpEnd_Ctrl', 'L_Eyelids_DwMid_CtrlShape', 'R_Eyelids_Up_BlinkTarget_CrvShape', 'R_Eyelids_Dw_6_Ctrl', 'L_Eyelids_Up_13_Jnt_Offset_Grp', 'R_Eyelids_DwStartMid_clusterHandleShape', 'R_Eyelids_Up_Origin_0_Jnt_aimConstraint1', 'L_Eyelids_UpEndMid_CtrlShape', 'R_Eyelids_Dw_11_Bnd', 'R_Eyelids_Dw_11_Jnt_Offset_Grp', 'R_Eyelids_Up_11_Ctrl_tag', 'L_Eyelids_Up_WireDriver_ClusterCrvBaseWire_cv_4__jnt_bc', 'L_Eyelids_Up_8_Ctrl', 'R_Eyelids_Scale_Jnt_Offset_Grp', 'R_Eyelids_DwEndMid_Ctrl', 'L_Eyelids_Up_Scale_Grp', 'R_Eyelids_Dw_8_Loc', 'L_Eyelids_Dw_5_Bnd', 'L_Eyelids_UpStart_cluster', 'L_Eyelids_Up_3_Ctrl_OffsetPivot_Grp_Offset_Grp', 'L_Eyelids_Dw_WireDriver_ClusterCrvBaseWireBaseWireShapeOrig1', 'R_Eyelids_Dw_6_LocShape', 'unitConversion8', 'L_Eyelids_Dw_8_LocShape', 'L_Eyelids_Dw_Origin_3_Jnt_aimConstraint1', 'L_Eyelids_Dw_5_Ctrl_OffsetPivot_Grp_Offset_Grp', 'R_Eyelids_Dw_1_Jnt', 'R_Eyelids_Up_Origin_6_Jnt_aimConstraint1', 'L_Eyelids_Dw_12_CtrlShape', 'L_Eyelids_Scale_Bnd_parentConstraint1', 'L_Eyelids_Up_Tweeks_Ctrl_Grp', 'L_Eyelids_Dw_8_Jnt_Offset_Grp', 'L_Eyelids_Dw_Scale_Ctrl_Offset_Grp', 'LwrBlink_MultDiv1', 'R_Eyelids_Up_1_Ctrl_Offset_Grp', 'R_Eyelids_DwStart_clusterHandle', 'R_Eyelids_Dw_WireDriver_CrvShapeOrig1', 'R_Eyelids_Up_11_Loc', 'R_Eyelids_DwEndMid_cluster', 'L_Eyelids_Dw_5_Ctrl_tag', 'R_Eyelids_Dw_6_Bnd_scaleConstraint1', 'L_EyelidsUprBlink_Ctrl_tag', 'R_Eyelids_Up_0_Bnd', 'L_Eyelids_EyePivot_LocShape', 'R_Eyelids_Up_13_Ctrl_Offset_Grp', 'R_Eyelids_DwMid_clusterHandleShape', 'L_Eyelids_Dw_2_Bnd_scaleConstraint1', 'L_Eyelids_Dw_10_Ctrl_tag', 'L_Eyelids_Dw_BlinkTarget_CrvShapeOrig', 'R_Eyelids_Dw_Origin_2_Jnt_Offset_Grp', 'L_Eyelids_Up_Origin_11_Jnt_Offset_Grp', 'L_Eyelids_Dw_5_Ctrl_OffsetPivot_Grp', 'L_Eyelids_Dw_Vtx_Crv', 'L_Eyelids_Up_Origin_10_Jnt_Offset_Grp', 'R_Eyelids_Blink_CrvBaseWireShapeOrig2', 'L_Eyelids_Up_WireDriver_ClusterCrvBaseWire_cv_3__jnt_bc', 'R_EyelidsUprBlink_Ctrl', 'R_Eyelids_Dw_WireDriver_CrvBaseWireShapeOrig', 'R_Eyelids_Up_9_CtrlShape', 'L_Eyelids_Up_WireDriver_ClusterCrvBaseWireBaseWire', 'L_Eyelids_Up_WireDriver_CrvShapeOrig1', 'hyperLayout51', 'R_Eyelids_Dw_0_Loc', 'L_Eyelids_DwEnd_cluster1Handle', 'R_Eyelids_Dw_Scale_Ctrl_tag', 'L_Eyelids_UpVector_Loc', 'L_Eyelids_Dw_12_Loc', 'R_Eyelids_Up_4_Bnd_scaleConstraint1', 'R_Eyelids_Dw_3_Ctrl_OffsetPivot_Grp', 'L_Eyelids_Up_Origin_9_Jnt_Offset_Grp', 'R_Eyelids_Scale_CtrlShape', 'R_Eyelids_DwStartMid_Jnt_Offset_Grp', 'L_Eyelids_Up_Origin_7_Jnt', 'L_Eyelids_Dw_4_Bnd_scaleConstraint1', 'L_Eyelids_Up_9_Bnd', 'L_Eyelids_Dw_WireDriver_ClusterCrvBaseWire_cv_6__jnt_bc', 'L_Eyelids_Dw_Origin_7_Jnt', 'L_Eyelids_Up_BlinkTarget_CrvShapeOrig', 'L_Eyelids_Dw_4_Jnt_Offset_Grp', 'R_Eyelids_Up_9_Jnt', 'L_Eyelids_Dw_4_Ctrl_OffsetPivot_Grp_Offset_Grp', 'R_Eyelids_Dw_WireDriver_ClusterCrvBaseWire_cv_3__clst_bc', 'R_Eyelids_Dw_WireDriver_ClusterCrvBaseWire_cv_1__clst_rev', 'R_Eyelids_Dw_WireDriver_Crv', 'L_Eyelids_Up_6_Ctrl_OffsetPivot_Grp_Offset_Grp', 'L_Eyelids_Dw_3_Ctrl_Offset_Grp', 'L_Eyelids_Dw_WireDriver_ClusterCrvBaseWire_cv_6__md5', 'L_Eyelids_Dw_11_Jnt_Offset_Grp', 'R_Eyelids_Dw_12_Jnt', 'R_Eyelids_Dw_Origin_12_Jnt', 'L_Eyelids_Dw_WireDriver_ClusterCrvBaseWire_cv_1__jnt_bc', 'R_Eyelids_Dw_10_Ctrl_OffsetPivot_Grp_Offset_Grp', 'R_Eyelids_Up_10_Ctrl_tag', 'L_Eyelids_Dw_10_Ctrl', 'R_Eyelids_Up_Scale_CtrlShape', 'L_Eyelids_UprBlink_BS', 'R_Eyelids_Dw_8_Bnd_parentConstraint1', 'L_Eyelids_Up_5_Jnt_Offset_Grp', 'R_Eyelids_Scale_Ctrl', 'R_Eyelids_Dw_Origin_3_Jnt', 'R_Eyelids_DwMid_Ctrl', 'R_Eyelids_Up_4_Jnt_Offset_Grp', 'L_Eyelids_Dw_Vtx_CrvShape', 'L_Eyelids_Dw_WireDriver_ClusterCrvBaseWire_cv_0__md5', 'R_Eyelids_Up_11_CtrlShape', 'L_Eyelids_UpWire', 'R_Eyelids_Dw_WireDriver_ClusterCrvBaseWire_cv_3__jnt_bc', 'L_Eyelids_Dw_WireDriver_CrvBaseWireShapeOrig', 'L_Eyelids_Dw_5_CtrlShape', 'R_Eyelids_Up_5_Ctrl_OffsetPivot_Grp_Offset_Grp', 'R_Eyelids_Dw_12_Jnt_Offset_Grp', 'L_Eyelids_Up_6_Ctrl', 'L_Eyelids_Dw_WireDriver_ClusterCrvBaseWireShape', 'R_Eyelids_Up_7_Bnd', 'R_Eyelids_Dw_11_POCI', 'R_Eyelids_Dw_WireDriver_CrvBaseWire', 'R_Eyelids_Up_6_Bnd', 'L_Eyelids_Dw_WireDriver_ClusterCrvBaseWire_cv_5__md5', 'R_Eyelids_Up_9_POCI', 'L_Eyelids_Up_WireDriver_ClusterCrvBaseWire_cv_4__clst_bc', 'L_Eyelids_Dw_Tweeks_Ctrl_Grp', 'R_Eyelids_DwMid_CtrlShape', 'R_Eyelids_UpVector_Loc', 'L_Eyelids_Up_3_Ctrl_tag', 'R_Eyelids_Dw_Origin_5_Jnt_Offset_Grp', 'L_Eyelids_Blink_CrvBaseWireShape', 'L_Eyelids_Dw_Origin_8_Jnt_Offset_Grp', 'L_Eyelids_Up_7_Ctrl_Offset_Grp', 'R_Eyelids_Dw_1_Ctrl', 'L_Eyelids_Dw_Jnt_Grp', 'R_Eyelids_UpEnd_clusterHandleShape', 'R_Eyelids_Dw_6_Ctrl_OffsetPivot_Grp', 'R_Eyelids_Up_WireDriver_ClusterCrvBaseWireShape', 'R_Eyelids_Up_WireDriver_ClusterCrvBaseWire_cv_0__md5', 'R_Eyelids_Up_12_Bnd_scaleConstraint1', 'R_Eyelids_Up_WireDriver_ClusterCrvBaseWire_cv_6__jnt_bc', 'R_Eyelids_Up_Origin_8_Jnt', 'R_Eyelids_Up_4_Ctrl_Offset_Grp', 'R_Eyelids_Dw_1_LocShape', 'R_Eyelids_Dw_9_Ctrl', 'L_Eyelids_Up_Origin_7_Jnt_aimConstraint1', 'L_Eyelids_Dw_9_Ctrl', 'R_Eyelids_UpEnd_Jnt', 'L_Eyelids_Dw_WireDriver_ClusterCrvBaseWire_cv_2__clst_bc', 'L_Eyelids_Dw_0_Bnd_scaleConstraint1', 'L_Eyelids_Up_8_Bnd_parentConstraint1', 'L_Eyelids_Dw_0_POCI', 'R_Eyelids_Dw_VtxJnts_Grp', 'R_Eyelids_DwMid_Ctrl_tag', 'R_Eyelids_Up_3_Ctrl_Offset_Grp', 'L_Eyelids_Up_0_CtrlShape', 'L_Eyelids_Up_Origin_6_Jnt_Offset_Grp', 'R_Eyelids_Up_WireDriver_CrvBaseWireShapeOrig', 'L_Eyelids_Dw_1_Ctrl_Offset_Grp', 'L_Eyelids_UpStartMid_Jnt', 'L_Eyelids_Up_Origin_8_Jnt', 'R_Eyelids_Dw_BlinkTarget_CrvShapeOrig1', 'skinCluster2', 'L_Eyelids_Up_8_Ctrl_Offset_Grp', 'R_Eyelids_Blink_CrvBaseWireShape', 'L_Eyelids_Dw_8_Ctrl', 'R_Eyelids_Scale_Bnd_scaleConstraint1', 'R_Eyelids_Dw_0_LocShape', 'R_Eyelids_Dw_Origin_0_Jnt', 'R_Eyelids_Dw_12_LocShape', 'R_Eyelids_Up_11_Bnd', 'R_Eyelids_Dw_AimLocators_Grp', 'L_Eyelids_Up_Origin_5_Jnt_Offset_Grp', 'L_Eyelids_Dw_Origin_4_Jnt_aimConstraint1', 'L_Eyelids_DwStartMid_Jnt_Offset_Grp_parentConstraint1', 'R_Eyelids_DwStart_Ctrl', 'L_Eyelids_Dw_1_Loc', 'L_Eyelids_Up_0_Bnd', 'R_Eyelids_Up_Scale_Ctrl_Offset_Grp', 'R_Eyelids_Up_1_Bnd_parentConstraint1', 'L_Eyelids_DwStartMid_Ctrl', 'L_Eyelids_DwEnd_clusterHandle', 'R_Eyelids_DwEndMid_Jnt_Offset_Grp_parentConstraint1', 'L_Eyelids_UpEnd_clusterHandleShape', 'L_Eyelids_UpEnd_cluster', 'L_Eyelids_UpEndMid_Ctrl_Offset_Grp', 'R_Eyelids_Up_7_Ctrl_tag', 'R_Eyelids_Up_Vtx_Crv', 'R_Eyelids_Up_Scale_Ctrl_tag', 'L_Eyelids_Up_13_Bnd', 'R_Eyelids_EyePivot_LocShape', 'L_Eyelids_Up_Origin_0_Jnt_Offset_Grp', 'L_Eyelids_Up_7_Bnd_parentConstraint1', 'L_Eyelids_Up_13_Bnd_scaleConstraint1', 'L_Eyelids_Dw_Origin_3_Jnt_Offset_Grp', 'L_Eyelids_Dw_11_Ctrl_OffsetPivot_Grp_Offset_Grp', 'L_Eyelids_Dw_11_Jnt', 'L_Eyelids_Scale_Ctrl_tag', 'R_Eyelids_Up_1_Loc', 'L_Eyelids_DwStart_Ctrl_tag', 'L_Eyelids_Up_WireDriver_ClusterCrvBaseWire_cv_2__clst_rev', 'L_Eyelids_Up_11_Ctrl', 'L_Eyelids_Dw_WireDriver_ClusterCrvBaseWire_cv_2__clst_rev', 'R_Eyelids_Up_2_LocShape', 'R_Eyelids_Up_10_Bnd_parentConstraint1', 'R_Eyelids_Blink_Reverse', 'L_Eyelids_DwMid_Ctrl_tag', 'R_Eyelids_Up_0_Ctrl_OffsetPivot_Grp', 'R_Eyelids_Up_12_Ctrl', 'L_Eyelids_Dw_BlinkTarget_CrvShapeOrig1', 'R_Eyelids_Up_WireDriver_ClusterCrvBaseWireBaseWire', 'L_Eyelids_Dw_2_Loc', 'R_Eyelids_Up_Origin_2_Jnt_Offset_Grp', 'L_Eyelids_Dw_7_Bnd', 'R_Eyelids_Up_2_CtrlShape', 'R_Eyelids_UpStartMid_Ctrl', 'R_Eyelids_Up_12_Ctrl_OffsetPivot_Grp', 'R_Eyelids_Dw_8_Jnt', 'L_Eyelids_Up_10_Ctrl_tag', 'R_Eyelids_Dw_WireDriver_ClusterCrvBaseWire_cv_4__clst_bc', 'R_Eyelids_Up_4_Jnt', 'R_Eyelids_Dw_6_Bnd_parentConstraint1', 'R_Eyelids_Up_WireDriver_ClusterCrvBaseWire_cv_3__md5', 'R_Eyelids_Up_6_Bnd_scaleConstraint1', 'L_Eyelids_Up_7_Ctrl_OffsetPivot_Grp_Offset_Grp', 'R_Eyelids_Dw_2_Bnd_parentConstraint1', 'R_Eyelids_Dw_4_LocShape', 'R_Eyelids_Up_11_Bnd_scaleConstraint1', 'R_Eyelids_Up_7_Ctrl', 'R_Eyelids_Up_4_Ctrl_tag', 'R_Eyelids_Up_9_Loc']");
createNode joint -n "Eye_Pivot" -p "L_Eyelids_Block";
	rename -uid "27154000-0018-1FF3-6621-A96000000F3A";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2024/scripts/rigging/Mutant_Tools/Icons/";
	setAttr ".t" -type "double3" 4.2601978182792664 15.575422922118946 5.3637304306030273 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".radi" 2;
createNode dagContainer -n "L_Orbicularis_Block" -p "face";
	rename -uid "27154000-0018-1FF3-6621-A96000000F3B";
	addAttr -ci true -sn "nts" -ln "notes" -dt "string";
	setAttr ".isc" yes;
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2024/scripts/rigging/Mutant_Tools/Icons/Orbicularis.png";
	setAttr ".ctor" -type "string" "info";
	setAttr ".cdat" -type "string" "2022/08/25 10:05:27";
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
		"['R_Orbicularis_Crv_2_Ctrl_Auto_Grp', 'R_Orbicularis_Crv_2_Ctrl_Root_Grp', 'R_Orbicularis_CrvBaseWire', 'R_Orbicularis_Crv_5_Ctrl_tag', 'L_Orbicularis_Crv_0_Jnt_Auto_Grp', 'R_Orbicularis_Crv_4_Ctrl_tag', 'L_Orbicularis_CrvBaseWireShapeOrig', 'L_Orbicularis_Crv_2_Jnt_Root_Grp', 'R_Orbicularis_CrvBaseWireShapeOrig', 'R_Orbicularis_Crv_3_Ctrl_Auto_Grp', 'L_Orbicularis_Crv_6_Ctrl_Auto_Grp', 'skinCluster6', 'R_Orbicularis_Rig_Grp', 'R_Orbicularis_Crv_2_Jnt_Root_Grp', 'L_Orbicularis_CrvBaseWireShape', 'L_Orbicularis_Crv_5_Jnt_Root_Grp', 'R_Orbicularis_Crv_1_CtrlShape', 'L_Orbicularis_Crv_4_CtrlShape', 'L_Orbicularis__Jnt_Grp', 'L_Orbicularis_Crv_3_Jnt_Auto_Grp', 'L_Orbicularis_Crv_6_Jnt_Root_Grp', 'R_Orbicularis_Crv_7_Ctrl_tag', 'L_Orbicularis_Crv_4_Jnt_Auto_Grp', 'R_Orbicularis_Crv_3_Ctrl', 'L_Orbicularis_Crv_1_Ctrl_Root_Grp', 'L_Orbicularis_Crv_4_Ctrl', 'R_Orbicularis_Crv_4_Ctrl_Auto_Grp', 'R_Orbicularis_Crv_2_Ctrl_tag', 'L_Orbicularis_Crv_2_Ctrl', 'R_Orbicularis_Crv_7_Ctrl_Auto_Grp', 'R_Orbicularis_Crv_5_Jnt', 'L_Orbicularis_CrvShape', 'L_Orbicularis_Crv_5_Ctrl_tag', 'L_Orbicularis_Crv_7_Ctrl_Root_Grp', 'R_Orbicularis_Crv_6_Ctrl', 'L_Orbicularis_Ctrl_Grp_parentConstraint1', 'R_Orbicularis_Crv_4_Jnt', 'L_Orbicularis_Crv_7_Jnt_Auto_Grp', 'L_Orbicularis_Crv_5_Ctrl_Auto_Grp', 'L_Orbicularis_Crv_7_Jnt_Root_Grp', 'R_Orbicularis_Crv_4_CtrlShape', 'R_Orbicularis_Crv_6_Jnt', 'R_Orbicularis_Crv_3_Jnt', 'R_Orbicularis_Crv_6_Ctrl_Root_Grp', 'R_Orbicularis_Crv_5_Ctrl', 'R_Orbicularis_Ctrl_Grp_scaleConstraint1', 'L_Orbicularis_CrvShapeOrig', 'L_Orbicularis_Crv_7_Ctrl', 'L_Orbicularis_Crv_5_CtrlShape', 'L_Orbicularis_Ctrl_Grp', 'L_Orbicularis_Crv_3_Ctrl', 'L_Orbicularis_Crv_4_Jnt', 'R_Orbicularis_Crv_1_Jnt', 'R_Orbicularis_Crv_1_Ctrl', 'R_Orbicularis_Crv_5_CtrlShape', 'L_Orbicularis_Crv_7_Ctrl_tag', 'R_Orbicularis_Crv_4_Jnt_Root_Grp', 'L_Orbicularis_Crv_1_Jnt_Root_Grp', 'L_Orbicularis_Crv_7_Ctrl_Auto_Grp', 'L_Orbicularis_Crv_3_Jnt_Root_Grp', 'R_Orbicularis_Crv_3_Ctrl_tag', 'bindPose6', 'L_Orbicularis_Crv_1_CtrlShape', 'R_Orbicularis_Crv_5_Ctrl_Auto_Grp', 'R_Orbicularis_Crv_1_Jnt_Root_Grp', 'L_Orbicularis_Crv_3_Ctrl_Auto_Grp', 'R_Orbicularis_Crv_3_Jnt_Root_Grp', 'R_Orbicularis_Crv_0_Ctrl_Root_Grp', 'bindPose5', 'L_Orbicularis_Crv_0_Jnt_Root_Grp', 'L_Orbicularis_Crv_6_Ctrl', 'R_Orbicularis_Crv_6_Ctrl_Auto_Grp', 'R_Orbicularis_Crv_1_Ctrl_Root_Grp', 'L_Orbicularis_Crv_6_Ctrl_tag', 'L_Orbicularis_Crv_1_Ctrl_tag', 'R_Orbicularis_Crv_5_Jnt_Auto_Grp', 'R_Orbicularis_Crv', 'R_Orbicularis_Crv_5_Jnt_Root_Grp', 'R_Orbicularis_Ctrl_Grp', 'R_Orbicularis_Crv_7_Ctrl', 'L_Orbicularis_Crv_6_CtrlShape', 'L_Orbicularis_Crv_2_Jnt', 'R_Orbicularis_Crv_7_Jnt_Root_Grp', 'L_Orbicularis_Crv_0_Ctrl', 'R_Orbicularis_Crv_4_Ctrl', 'R_Orbicularis_Crv_6_Jnt_Auto_Grp', 'R_Orbicularis_Crv_7_CtrlShape', 'R_Orbicularis__Jnt_Grp1', 'skinCluster5', 'R_Orbicularis_Crv_2_Jnt', 'L_Orbicularis_Crv_2_Ctrl_Auto_Grp', 'L_Orbicularis_Crv_4_Jnt_Root_Grp', 'L_Orbicularis_Crv_2_Jnt_Auto_Grp', 'L_Orbicularis_Crv_4_Ctrl_Auto_Grp', 'L_Orbicularis_Crv_1_Ctrl', 'L_Orbicularis_Crv_2_CtrlShape', 'R_Orbicularis_Crv_0_Jnt_Auto_Grp', 'L_Orbicularis_Crv', 'R_Orbicularis_Crv_Wire', 'R_Orbicularis_Crv_0_Jnt', 'L_Orbicularis_Crv_4_Ctrl_tag', 'R_Orbicularis_CrvShapeOrig', 'L_Orbicularis_Crv_1_Jnt', 'R_Orbicularis_Crv_1_Jnt_Auto_Grp', 'L_Orbicularis_Crv_3_Ctrl_tag', 'R_Orbicularis_Crv_4_Jnt_Auto_Grp', 'L_Orbicularis_CrvBaseWire', 'R_Orbicularis_Crv_3_Ctrl_Root_Grp', 'R_Orbicularis_Crv_0_Jnt_Root_Grp', 'L_Orbicularis_Ctrl_Grp_scaleConstraint1', 'L_Orbicularis_Crv_0_Ctrl_Auto_Grp', 'R_Orbicularis_Crv_0_Ctrl_Auto_Grp', 'L_Orbicularis_Crv_6_Ctrl_Root_Grp', 'L_Orbicularis__Jnt_Grp1', 'R_Orbicularis_Crv_6_Jnt_Root_Grp', 'L_Orbicularis_Crv_6_Jnt_Auto_Grp', 'L_Orbicularis_Crv_0_Jnt', 'R_Orbicularis_Crv_3_CtrlShape', 'L_Orbicularis_Crv_2_Ctrl_tag', 'R_Orbicularis_Crv_5_Ctrl_Root_Grp', 'L_Orbicularis_Crv_5_Ctrl_Root_Grp', 'L_Orbicularis_Crv_3_Ctrl_Root_Grp', 'L_Orbicularis_Crv_3_Jnt', 'R_Orbicularis_CrvBaseWireShape', 'L_Orbicularis_Crv_Wire', 'L_Orbicularis_Crv_5_Jnt', 'L_Orbicularis_Crv_5_Jnt_Auto_Grp', 'L_Orbicularis_Crv_2_Ctrl_Root_Grp', 'R_Orbicularis__Jnt_Grp', 'L_Orbicularis_Crv_3_CtrlShape', 'R_Orbicularis_Crv_2_CtrlShape', 'L_Orbicularis_Rig_Grp', 'R_Orbicularis_Crv_7_Ctrl_Root_Grp', 'L_Orbicularis_Crv_4_Ctrl_Root_Grp', 'R_Orbicularis_Ctrl_Grp_parentConstraint1', 'R_Orbicularis_Crv_0_Ctrl_tag', 'L_Orbicularis_Crv_1_Jnt_Auto_Grp', 'R_Orbicularis_Crv_0_CtrlShape', 'R_Orbicularis_Crv_1_Ctrl_Auto_Grp', 'L_Orbicularis_Crv_6_Jnt', 'R_Orbicularis_Crv_2_Jnt_Auto_Grp', 'R_Orbicularis_Crv_1_Ctrl_tag', 'L_Orbicularis_Crv_0_Ctrl_Root_Grp', 'R_Orbicularis_Crv_3_Jnt_Auto_Grp', 'R_Orbicularis_Crv_6_Ctrl_tag', 'R_Orbicularis_Crv_6_CtrlShape', 'R_Orbicularis_Crv_4_Ctrl_Root_Grp', 'L_Orbicularis_Crv_5_Ctrl', 'R_Orbicularis_CrvShape', 'R_Orbicularis_Crv_0_Ctrl', 'L_Orbicularis_Crv_1_Ctrl_Auto_Grp', 'R_Orbicularis_Crv_7_Jnt', 'L_Orbicularis_Crv_7_Jnt', 'L_Orbicularis_Crv_0_Ctrl_tag', 'R_Orbicularis_Crv_7_Jnt_Auto_Grp', 'R_Orbicularis_Crv_2_Ctrl', 'L_Orbicularis_Crv_0_CtrlShape', 'L_Orbicularis_Crv_7_CtrlShape']");
createNode transform -n "L_Orbicularis_Guide" -p "L_Orbicularis_Block";
	rename -uid "27154000-0018-1FF3-6621-A96000000F3C";
	addAttr -ci true -sn "RotateOrder" -ln "RotateOrder" -min 0 -max 5 -en "xyz:yzx:zxy:xzy:yxz:zyx" 
		-at "enum";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2024/scripts/rigging/Mutant_Tools/Icons/";
	setAttr -l on -k off ".v";
	setAttr ".ove" yes;
	setAttr ".hpb" yes;
	setAttr ".ovc" 9;
	setAttr ".t" -type "double3" 3.2556531429290771 15.09615373895096 8.8338813216584029 ;
	setAttr -cb on ".RotateOrder";
createNode nurbsCurve -n "L_Orbicularis_GuideShape" -p "L_Orbicularis_Guide";
	rename -uid "27154000-0018-1FF3-6621-A96000000F3D";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2024/scripts/rigging/Mutant_Tools/Icons/";
	setAttr -k off ".v";
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		3 8 2 no 3
		13 -2 -1 0 1 2 3 4 5 6 7 8 9 10
		11
		3.9655041340912822 1.6914150010089322 0.72323340594549723
		1.8762213503336129 1.6432678960664377 1.6001232358361013
		-0.14910922059489784 1.4152465419231952 2.0292216265580159
		-1.3657773460207556 0.12794719323992709 0.90264146139455192
		-0.39477799981000139 -1.0442993332430939 0.8243000339034281
		2.1958980658580507 -1.7611284385168049 0.40889459369510206
		4.5000822479302736 -0.91803302945883858 -0.84721074592558487
		4.6887281024105194 0.60745900982305701 -1.7016571311724284
		3.9655041340912822 1.6914150010089322 0.72323340594549723
		1.8762213503336129 1.6432678960664377 1.6001232358361013
		-0.14910922059489784 1.4152465419231952 2.0292216265580159
		;
createNode dagContainer -n "L_Brow_Block" -p "face";
	rename -uid "27154000-0018-1FF3-6621-A96000000F3E";
	addAttr -ci true -sn "nts" -ln "notes" -dt "string";
	setAttr ".isc" yes;
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2024/scripts/rigging/Mutant_Tools/Icons/Brows.png";
	setAttr ".ctor" -type "string" "esteban.rodriguez";
	setAttr ".cdat" -type "string" "2022/04/05 13:54:07";
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
		"['R_Brow_Driver3_Sec_Ctrl_Auto_Grp', 'L_Brow_Driver3_yesRot_Loc_Offset_Grp', 'L_Brow_Driver1_yesRot_Loc_Offset_Grp', 'L_Brow_Ctrl_tag', 'unitConversion9', 'L_Brow_Driver1_Sec_CtrlShape', 'C_Brow_Loc_Offset_Grp', 'R_Brow_OutterAutoRot_Blend5', 'L_Brow_0_Bnd_scaleConstraint1', 'C_Brow_CtrlShape', 'L_Brow_NurbFollicle3050', 'R_Brow_SecRot_Loc_Grp', 'L_Brow_Driver2_Main_CtrlShape', 'R_Brow_1_Bnd_scaleConstraint1', 'L_Brow_1_Bnd', 'L_Brow_1_Ctrl', 'R_Brow_NurbFollicle1050', 'L_Brow_Main_Ctrl_Grp', 'R_Brow_Driver3_Sec_Ctrl', 'L_Brow_Driver4_Jnt', 'L_Brow_CtrlShape', 'L_Brow_2_Loc_Offset_Grp', 'L_Brow_0_Ctrl_tag', 'R_Brow_2_CtrlShape', 'R_Brow_Driver3_yesRot_Loc', 'L_Brow_1_Loc_Offset_Grp', 'L_Brow_Driver1_noRot_Loc', 'L_Brow_Driver1_Jnt_Root_Grp', 'R_Brow_3_Bnd_parentConstraint1', 'R_Brow_Driver1_Jnt_Root_Grp_parentConstraint1', 'L_Brow_2_Bnd', 'unitConversion20', 'L_Brow_2_LocShape', 'R_Brow_innerAutoRot_Blend5', 'R_Brow_Ctrl_tag', 'L_Brow_2_Bnd_scaleConstraint1', 'R_Brow_Driver1_Sec_Ctrl_tag', 'L_Brow_Driver1_yesRot_Loc_Offset_Grp_parentConstraint1', 'R_Brow_UpVector_Loc', 'L_Brow_2_Jnt_parentConstraint1', 'R_Brow_Driver3_noRot_Loc_Offset_Grp', 'L_Brow_1_Bnd_parentConstraint1', 'L_Brow_Driver3_yesRot_Loc_aimConstraint1', 'R_Brow_Driver1_Jnt_Root_Grp', 'L_Brow_Driver1_yesRot_LocShape', 'R_Brow_Driver1_yesRot_LocShape', 'L_Brow_Driver1_Sec_Ctrl_Root_Grp_parentConstraint1', 'L_Brow_3_Jnt', 'unitConversion12', 'L_Brow_3_LocShape', 'L_Brow_NurbShapeOrig', 'L_Brow_OutterAutoRot_Blend5', 'C_Brow_Jnt_Offset_Grp', 'L_Brow_Driver1_noRot_LocShape', 'C_Brow_Jnt_parentConstraint1', 'L_Brow_Ctrl_Grp_parentConstraint1', 'L_Brow_2_Bnd_parentConstraint1', 'L_Brow_NurbFollicle5050', 'L_Brow_0_Jnt_parentConstraint1', 'R_Brow_Driver4_Jnt', 'L_Brow_Driver0_Jnt_Root_Grp', 'R_Brow_Driver0_Main_Ctrl_Offset_Grp', 'R_Brow_Main_Ctrl_Grp', 'L_Brow_Driver1_yesRot_Loc_aimConstraint1', 'C_Brow_Bnd', 'R_Brow_Driver4_Jnt_Auto_Grp', 'L_Brow_3_Loc_Offset_Grp', 'R_Brow_2_Ctrl_tag', 'R_Brow_Ctrl_GrpMirror_Grp', 'R_Brow_NurbFollicleShape6950', 'L_Brow_Driver3_yesRot_Loc', 'R_Brow_3_CtrlShape', 'L_Brow_4_CtrlShape', 'L_Brow_1_Ctrl_tag', 'L_Brow_3_Bnd', 'R_Brow_Driver1_yesRot_Loc', 'L_Brow_Driver2_Main_Ctrl_Offset_Grp', 'C_Brow_Ctrl_Reverse', 'L_Brow_2_Ctrl_Offset_Grp', 'L_Brow_Driver3_Sec_Ctrl_Root_Grp_parentConstraint1', 'C_Brow_Bnd_scaleConstraint1', 'R_Brow_1_Ctrl', 'L_Brow_NurbFollicleShape3050', 'L_Brow_TweekJnts_Grp', 'L_Brow_4_Jnt_Offset_Grp', 'L_Brow_Fol_Grp', 'C_Brow_Loc_Offset_Grp_pointConstraint1', 'L_Brow_3_Ctrl', 'L_Brow_4_Jnt', 'R_Brow_Driver0_Main_Ctrl_tag', 'R_Brow_Main_Jnt_Grp', 'L_Brow_Driver1_Jnt_Root_Grp_parentConstraint1', 'L_Brow_Driver3_Jnt_Auto_Grp', 'unitConversion13', 'L_Brow_Driver2_Jnt', 'L_Brow_Driver2_Main_Ctrl_tag', 'unitConversion22', 'unitConversion10', 'R_Brow_3_Jnt_parentConstraint1', 'R_Brow_Driver3_yesRot_LocShape', 'C_Brow_Null_Loc', 'R_Brow_Driver2_Main_Ctrl', 'L_Brow_Driver3_Sec_Ctrl_tag', 'R_Brow_3_Ctrl_tag', 'L_Brow_4_Ctrl_Offset_Grp', 'L_Brow_Driver0_Jnt_Auto_Grp', 'L_Brow_Rig_Grp', 'R_Brow_Driver1_Sec_CtrlShape', 'R_Brow_Ctrl_Offset_Grp', 'R_Brow_Fol_Grp', 'L_Brow_2_Jnt', 'R_Brow_Driver4_Main_Ctrl_Offset_Grp', 'L_Brow_1_Ctrl_Offset_Grp', 'L_Brow_Driver2_Jnt_Root_Grp', 'R_Brow_0_CtrlShape', 'L_Brow_Main_Jnt_Grp', 'R_Brow_1_Ctrl_Offset_Grp', 'L_Brow_3_Ctrl_tag', 'R_Brow_NurbShapeOrig', 'R_Brow_Driver1_noRot_LocShape', 'L_Brow_4_Ctrl_tag', 'L_Brow_2_CtrlShape', 'R_Brow_Ctrl', 'L_Brow_NurbFollicleShape5050', 'R_Brow_3_Ctrl', 'R_Brow_Driver4_Main_CtrlShape', 'R_Brow_0_Jnt_parentConstraint1', 'R_Brow_NurbFollicle5050', 'C_Brow_Bnd_parentConstraint1', 'R_Brow_Driver2_Jnt', 'R_Brow_NurbFollicle8950', 'unitConversion21', 'L_Brow_4_LocShape', 'R_Brow_DriverJnts_Grp', 'L_Brow_2_Jnt_Offset_Grp', 'R_Brow_Driver4_Jnt_Root_Grp', 'L_Brow_innerAutoRot_Blend5', 'L_Brow_2_Ctrl_tag', 'R_Brow_Driver2_Main_Ctrl_Offset_Grp', 'R_Brow_2_Ctrl', 'R_Brow_Driver3_Sec_CtrlShape', 'L_Brow_NurbFollicle8950', 'L_Brow_Ctrl_Offset_Grp', 'L_Brow_Driver3_Sec_Ctrl', 'L_Brow_4_Jnt_parentConstraint1', 'R_Brow_4_Jnt', 'L_Brow_NurbFollicleShape1050', 'R_Brow_Driver1_yesRot_Loc_Offset_Grp_parentConstraint1', 'L_Brow_Driver3_Jnt_Root_Grp', 'L_Brow_4_Bnd_parentConstraint1', 'C_Brow_Jnt', 'L_Brow_Driver2_Jnt_Auto_Grp', 'L_Brow_1_Jnt', 'R_Brow_4_Loc', 'R_Brow_Driver0_Main_CtrlShape', 'L_Brow_Driver0_Main_Ctrl_tag', 'L_Brow_1_Bnd_scaleConstraint1', 'L_Brow_UpVector_Loc_parentConstraint1', 'unitConversion16', 'L_Brow_3_Bnd_scaleConstraint1', 'bindPose7', 'L_Brow_UpVector_Loc', 'R_Brow_4_Bnd_parentConstraint1', 'L_Brow_0_Jnt', 'R_Brow_0_Loc', 'R_Brow_3_Loc', 'L_Brow_1_Jnt_parentConstraint1', 'R_Brow_Nurb', 'L_Brow_Driver1_Sec_Ctrl_Auto_Grp', 'L_Brow_Driver1_Sec_Ctrl_Root_Grp', 'skinCluster7', 'C_Brow_Null_LocShape', 'R_Brow_1_LocShape', 'R_Brow_Ctrl_Grp', 'R_Brow_Driver3_noRot_Loc', 'R_Brow_2_Loc', 'R_Brow_CtrlShape', 'R_Brow_Driver1_Sec_Ctrl_Root_Grp', 'R_Brow_Driver3_noRot_LocShape', 'R_Brow_2_Bnd', 'R_Brow_Driver3_yesRot_Loc_Offset_Grp_parentConstraint1', 'L_Brow_4_Ctrl', 'R_Brow_NurbShape', 'L_Brow_3_CtrlShape', 'R_Brow_1_Loc_Offset_Grp', 'L_Brow_Ctrl_Grp', 'L_Brow_0_Ctrl', 'R_Brow_Driver3_Jnt_Auto_Grp', 'C_Brow_Loc', 'L_Brow_Driver3_noRot_LocShape', 'R_Brow_Driver1_noRot_Loc_Offset_Grp_parentConstraint1', 'L_Brow_1_LocShape', 'R_Brow_TweekJnts_Grp', 'R_Brow_NurbFollicleShape8950', 'L_Brow_0_LocShape', 'L_Brow_Driver1_Sec_Ctrl_tag', 'R_Brow_4_Jnt_Offset_Grp', 'R_Brow_4_LocShape', 'R_Brow_Rig_GrpMirror_Grp', 'R_Brow_Driver2_Jnt_Root_Grp', 'R_Brow_Driver1_yesRot_Loc_Offset_Grp', 'R_Brow_Driver1_Jnt_Auto_Grp', 'R_Brow_Driver3_Jnt_Root_Grp_parentConstraint1', 'unitConversion23', 'R_Brow_Driver2_Jnt_Auto_Grp', 'R_Brow_4_Ctrl_Offset_Grp', 'R_Brow_Driver2_Main_CtrlShape', 'L_Brow_NurbFollicleShape6950', 'L_Brow_Tweeks_Ctrl_Grp', 'R_Brow_4_Loc_Offset_Grp', 'L_Brow_NurbFollicle6950', 'R_Brow_1_Ctrl_tag', 'R_Brow_NurbFollicle3050', 'L_Brow_1_CtrlShape', 'R_Brow_0_Jnt', 'L_Brow_Driver0_Main_Ctrl', 'R_Brow_Driver0_Jnt', 'R_Brow_0_LocShape', 'L_Brow_2_Ctrl', 'L_Brow_Driver0_Jnt', 'R_Brow_4_Bnd', 'unitConversion18', 'R_Brow_NurbFollicle6950', 'R_Brow_1_CtrlShape', 'C_Brow_Ctrl', 'R_Brow_2_Jnt', 'R_Brow_3_Ctrl_Offset_Grp', 'L_Brow_Driver2_Main_Ctrl', 'L_Brow_1_Jnt_Offset_Grp', 'C_Brow_Ctrl_Offset_Grp_pointConstraint1', 'unitConversion11', 'L_Brow_NurbFollicle1050', 'L_Brow_Ctrl', 'L_Brow_3_Jnt_parentConstraint1', 'L_Brow_Driver1_Jnt', 'L_Brow_Driver1_noRot_Loc_Offset_Grp_parentConstraint1', 'R_Brow_2_Ctrl_Offset_Grp', 'R_Brow_1_Jnt_Offset_Grp', 'R_Brow_4_CtrlShape', 'R_Brow_2_Bnd_scaleConstraint1', 'L_Brow_UpVector_LocShape', 'R_Brow_3_Loc_Offset_Grp', 'L_Brow_Driver3_Jnt_Root_Grp_parentConstraint1', 'L_Brow_Driver4_Main_Ctrl_Offset_Grp', 'R_Brow_2_Jnt_Offset_Grp', 'L_Brow_0_Bnd', 'R_Brow_2_LocShape', 'L_Brow_Nurb', 'L_Brow_Driver1_Sec_Ctrl', 'C_Brow_Loc_Reverse', 'R_Brow_Driver3_yesRot_Loc_aimConstraint1', 'unitConversion24', 'R_Brow_0_Ctrl', 'R_Brow_0_Loc_Offset_Grp', 'L_Brow_Driver3_yesRot_Loc_Offset_Grp_parentConstraint1', 'R_Brow_3_Bnd_scaleConstraint1', 'R_Brow_Driver3_yesRot_Loc_Offset_Grp', 'L_Brow_Driver4_Main_Ctrl_tag', 'L_Brow_4_Bnd_scaleConstraint1', 'L_Brow_Driver4_Main_Ctrl', 'R_Brow_3_LocShape', 'L_Brow_2_Loc', 'L_Brow_4_Bnd', 'L_Brow_Driver3_Jnt', 'R_Brow_0_Ctrl_Offset_Grp', 'unitConversion15', 'R_Brow_Driver4_Main_Ctrl', 'C_Brow_LocShape', 'R_Brow_4_Jnt_parentConstraint1', 'R_Brow_Driver2_Main_Ctrl_tag', 'R_Brow_0_Jnt_Offset_Grp', 'L_Brow_3_Ctrl_Offset_Grp', 'R_Brow_1_Jnt_parentConstraint1', 'L_Brow_0_Loc_Offset_Grp', 'L_Brow_0_Bnd_parentConstraint1', 'L_Brow_Driver0_Main_CtrlShape', 'R_Brow_Rig_Grp', 'R_Brow_Tweeks_Ctrl_Grp', 'L_Brow_3_Loc', 'L_Brow_Driver1_noRot_Loc_Offset_Grp', 'R_Brow_Driver3_Jnt', 'R_Brow_Driver3_Sec_Ctrl_tag', 'C_Brow_Ctrl_Offset_Grp', 'L_Brow_DriverJnts_Grp', 'L_Brow_3_Jnt_Offset_Grp', 'R_Brow_3_Bnd', 'R_Brow_UpVector_Loc_parentConstraint1', 'R_Brow_Driver3_Sec_Ctrl_Root_Grp', 'L_Brow_SecRot_Loc_Grp', 'L_Brow_4_Loc_Offset_Grp', 'L_Brow_Driver3_Sec_CtrlShape', 'L_Brow_Driver4_Jnt_Auto_Grp', 'R_Brow_Driver1_noRot_Loc', 'L_Brow_Driver4_Main_CtrlShape', 'R_Brow_1_Bnd_parentConstraint1', 'L_Brow_4_Loc', 'L_Brow_Driver4_Jnt_Root_Grp', 'R_Brow_1_Loc', 'R_Brow_4_Ctrl_tag', 'L_Brow_Driver3_yesRot_LocShape', 'R_Brow_Driver1_Sec_Ctrl', 'unitConversion17', 'L_Brow_Driver3_noRot_Loc_Offset_Grp_parentConstraint1', 'R_Brow_4_Bnd_scaleConstraint1', 'R_Brow_Driver3_Sec_Ctrl_Root_Grp_parentConstraint1', 'L_Brow_Driver0_Main_Ctrl_Offset_Grp', 'L_Brow_NurbFollicleShape8950', 'R_Brow_Driver3_noRot_Loc_Offset_Grp_parentConstraint1', 'R_Brow_NurbFollicleShape3050', 'L_Brow_0_CtrlShape', 'R_Brow_0_Bnd', 'R_Brow_Driver1_Sec_Ctrl_Auto_Grp', 'R_Brow_1_Jnt', 'R_Brow_3_Jnt_Offset_Grp', 'R_Brow_0_Ctrl_tag', 'L_Brow_0_Jnt_Offset_Grp', 'R_Brow_1_Bnd', 'L_Brow_Driver3_Sec_Ctrl_Auto_Grp', 'skinCluster8', 'R_Brow_Driver0_Jnt_Root_Grp', 'R_Brow_Driver0_Jnt_Auto_Grp', 'L_Brow_Driver3_Sec_Ctrl_Root_Grp', 'C_Brow_Ctrl_tag', 'L_Brow_NurbShape', 'R_Brow_Driver1_noRot_Loc_Offset_Grp', 'C_Brow_Jnt_scaleConstraint1', 'R_Brow_2_Bnd_parentConstraint1', 'unitConversion14', 'L_Brow_1_Loc', 'R_Brow_Driver4_Main_Ctrl_tag', 'R_Brow_Driver3_Jnt_Root_Grp', 'L_Brow_3_Bnd_parentConstraint1', 'R_Brow_Ctrl_Grp_parentConstraint1', 'R_Brow_Driver0_Main_Ctrl', 'L_Brow_0_Ctrl_Offset_Grp', 'R_Brow_3_Jnt', 'R_Brow_4_Ctrl', 'L_Brow_Driver1_yesRot_Loc', 'R_Brow_2_Loc_Offset_Grp', 'R_Brow_Driver1_Sec_Ctrl_Root_Grp_parentConstraint1', 'L_Brow_0_Loc', 'L_Brow_Driver1_Jnt_Auto_Grp', 'R_Brow_NurbFollicleShape1050', 'R_Brow_UpVector_LocShape', 'R_Brow_0_Bnd_scaleConstraint1', 'R_Brow_Driver1_Jnt', 'unitConversion19', 'R_Brow_2_Jnt_parentConstraint1', 'R_Brow_Driver1_yesRot_Loc_aimConstraint1', 'R_Brow_0_Bnd_parentConstraint1', 'R_Brow_NurbFollicleShape5050', 'bindPose8', 'L_Brow_Driver3_noRot_Loc_Offset_Grp', 'L_Brow_Driver3_noRot_Loc']");
createNode transform -n "L_Brow_Guide" -p "L_Brow_Block";
	rename -uid "27154000-0018-1FF3-6621-A96000000F3F";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2024/scripts/rigging/Mutant_Tools/Icons/";
	setAttr ".t" -type "double3" 1.6308539153929473 -105.44945673325665 0.97104483728890045 ;
createNode nurbsSurface -n "L_Brow_GuideShape" -p "L_Brow_Guide";
	rename -uid "27154000-0018-1FF3-6621-A96000000F40";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2024/scripts/rigging/Mutant_Tools/Icons/";
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
		10 0 0 0 1.9999999999999998 3.9999999999999996 6 7.9999999999999991 10 10 10
		
		6 0 0 0 1 1 1
		
		32
		-0.5594220148151906 123.46945369881088 10.720492411712605
		-0.55224542722408232 122.87286190911195 10.712950809614361
		-0.54506883963297581 122.27627011941287 10.705409207516105
		-0.53789225204186786 121.67967832971382 10.697867605417869
		-0.11797261065119145 123.44465009726693 10.667789192137269
		-0.11489648866326573 122.78811199698497 10.617252618109863
		-0.11182036667533533 122.131573896703 10.566716044082456
		-0.10874424468740924 121.47503579642104 10.516179470055036
		1.9133666109938936 123.70465660620826 10.355144837618553
		1.8292277937355186 123.10727606343598 10.320835867801136
		1.7450889764771396 122.50989552066376 10.286526897983721
		1.6609501592187597 121.9125149778915 10.252217928166289
		3.1679755367613582 123.73552891664053 9.9080195702105591
		3.1005880492043691 123.23710186390335 9.9568402604020445
		3.0332005616473854 122.73867481116622 10.005660950593532
		2.9658130740903985 122.24024775842909 10.054481640785021
		4.1913516938538766 124.00947064227124 9.4106199948602214
		4.1294040120458257 123.52736393542229 9.5015641139232514
		4.0674563302377829 123.04525722857331 9.5925082329863027
		4.0055086484297258 122.56315052172432 9.683452352049347
		5.2022982905570467 124.3054760631522 8.3422189802820856
		5.1679627177836807 123.87599009684783 8.5071165189115803
		5.133627145010311 123.44650413054346 8.6720140575410589
		5.0992915722369414 123.01701816423908 8.8369115961705411
		6.2264479310054526 123.62766081408488 7.2411963002447459
		6.2281936154776627 123.23962393548251 7.4339549088435213
		6.2299392999498817 122.85158705688005 7.6267135174423029
		6.2316849844220998 122.46355017827763 7.8194721260410747
		6.6514330808590252 122.93123012933563 5.712359879224409
		6.6600002391704347 122.56179910655639 5.9108927762530641
		6.6685673974818434 122.19236808377717 6.1094256732817147
		6.6771345557932573 121.82293706099793 6.3079585703103662
		
		;
createNode dagContainer -n "L_Cheecks_Block" -p "face";
	rename -uid "27154000-0018-1FF3-6621-A96000000F41";
	addAttr -ci true -sn "nts" -ln "notes" -dt "string";
	setAttr ".isc" yes;
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2024/scripts/rigging/Mutant_Tools/Icons/CheeksAdvance.png";
	setAttr ".ctor" -type "string" "Esteban";
	setAttr ".cdat" -type "string" "2022/10/12 11:08:04";
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
		"['L_Cheecks_5_POCI', 'R_Cheecks_1_Jnt', 'L_Cheecks_Top_Jnt', 'L_Cheecks_1_Jnt_Offset_Grp', 'L_Cheecks_Btm_Ctrl', 'R_Cheecks_Main_Jnt_Grp', 'L_Cheecks_Border_Linear_CrvShapeOrig', 'L_Cheecks_2_POCI', 'L_Cheecks_Bone_3_Ctrl_tag', 'L_Cheecks_Bone_0_Ctrl_tag', 'L_Cheecks_Bone_2_Bnd_scaleConstraint1', 'L_Cheecks_Main_Bnd_parentConstraint1', 'R_Cheecks_Bone_0_CtrlShape', 'L_Cheecks_Btm_Ctrl_Offset_Grp', 'R_Cheecks_4_Bnd_parentConstraint1', 'R_Cheecks_Border_Driver_CrvBaseWireShape', 'L_Cheecks_Bone_2_Ctrl_Offset_Grp', 'R_Cheecks_2_CtrlShape', 'L_Cheecks_Bone_0_Jnt_Offset_Grp', 'L_Cheecks_0_Jnt', 'R_Cheecks_MidBtm_CtrlShape', 'R_Cheecks_2_Ctrl_Offset_Grp', 'R_Cheecks_0_Bnd', 'R_Cheecks_4_Ctrl', 'L_Cheecks_Bone_3_Jnt_Offset_Grp', 'L_Cheecks_Bone_0_Ctrl', 'L_Cheecks_MidBtm_Ctrl_tag', 'L_Cheecks_Bone_1_Ctrl', 'L_Cheecks_1_Jnt', 'L_Cheecks_2_Ctrl_tag', 'L_Cheecks_5_Bnd_parentConstraint1', 'R_Cheecks_1_POCI', 'R_Cheecks_5_Ctrl', 'R_Cheecks_2_Jnt', 'L_Cheecks_5_Ctrl', 'R_Cheecks_Ctrl_Grp', 'L_Cheecks_5_CtrlShape', 'L_Cheecks_MidBtm_Ctrl_Offset_Grp_parentConstraint1', 'L_Cheecks_TopMid_Ctrl_tag', 'L_Cheecks_Mid_CtrlShape', 'L_Cheecks_Bone_2_Jnt', 'R_Cheecks_Bone_1_Jnt_Root_Grp', 'R_Cheecks_Bone_2_Jnt_Offset_Grp', 'L_Cheecks_TopMid_Ctrl', 'L_Cheecks_Border_Driver_Crv', 'R_Cheecks_2_Jnt_Offset_Grp', 'L_Cheecks_5_Jnt', 'L_Cheecks_Btm_CtrlShape', 'L_Cheecks_Border_Driver_CrvBaseWire', 'L_Cheecks_2_Bnd_parentConstraint1', 'bindPose10', 'R_Cheecks_Tweeks_Ctrl_Grp', 'L_Cheecks_Bone_3_Jnt_Root_Grp', 'R_Cheecks_Bone_3_Ctrl_Offset_Grp', 'L_Cheecks_Bone_1_Jnt_Root_Grp', 'L_Cheecks_Bone_1_Bnd_scaleConstraint1', 'L_Cheecks_Top_CtrlShape', 'R_Cheecks_Mid_Ctrl_tag', 'L_Cheecks_0_Ctrl_Offset_Grp', 'R_Cheecks_4_Ctrl_tag', 'R_Cheecks_Bone_1_Ctrl', 'L_Cheecks_Mid_Ctrl_tag', 'R_Cheecks_5_Bnd', 'L_Cheecks_Top_Ctrl_tag', 'L_Cheecks_Bone_3_Bnd_scaleConstraint1', 'R_Cheecks_Btm_Ctrl_tag', 'R_Cheecks_TopMid_Ctrl', 'L_Cheecks_Main_Bnd_scaleConstraint1', 'R_Cheecks_1_Bnd_parentConstraint1', 'L_Cheecks_Main_Ctrl_Offset_Grp', 'L_Cheecks_Bone_2_Ctrl', 'R_Cheecks_2_Bnd', 'R_Cheecks_Bone_3_Jnt', 'R_Cheecks_Bone_0_Bnd_parentConstraint1', 'L_Cheecks_4_Ctrl_Offset_Grp', 'L_Cheecks_TopMid_Jnt_Offset_Grp_parentConstraint1', 'R_Cheecks_Bone_3_Jnt_Auto_Grp', 'R_Cheecks_Border_Linear_Crv', 'R_Cheecks_Bone_1_CtrlShape', 'L_Cheecks_3_Ctrl_Offset_Grp', 'L_Cheecks_0_POCI', 'L_Cheecks_4_POCI', 'R_Cheecks_Main_Ctrl', 'R_Cheecks_Btm_Jnt', 'R_Cheecks_5_Ctrl_Offset_Grp', 'R_Cheecks_2_Bnd_parentConstraint1', 'L_Cheecks_2_Bnd_scaleConstraint1', 'R_Cheecks_3_Bnd_scaleConstraint1', 'L_Cheecks_Bone_2_CtrlShape', 'R_Cheecks_Mid_Ctrl_Offset_Grp', 'L_Cheecks_3_Bnd', 'L_Cheecks_MidBtm_CtrlShape', 'R_Cheecks_MidBtm_Ctrl_Offset_Grp_parentConstraint1', 'R_Cheecks_Bone_0_Ctrl_Offset_Grp', 'L_Cheecks_Main_Jnt_Grp', 'R_Cheecks_Bone_2_Ctrl_tag', 'R_Cheecks_4_CtrlShape', 'R_Cheecks_Bone_1_Bnd', 'R_Cheecks_Bone_1_Jnt_Auto_Grp', 'L_Cheecks_3_CtrlShape', 'R_Cheecks_4_Ctrl_Offset_Grp', 'L_Cheecks_Border_Linear_Crv', 'R_Cheecks_Main_Bnd_scaleConstraint1', 'L_Cheecks_1_POCI', 'L_Cheecks_Main_Bone_Ctrl_Offset_Grp', 'R_Cheecks_TweekJnts_Grp', 'R_Cheecks_Main_Ctrl_tag', 'L_Cheecks_Bone_1_Bnd_parentConstraint1', 'L_Cheecks_Border_Driver_CrvShapeOrig', 'R_Cheecks_TopMid_Jnt_Offset_Grp_parentConstraint1', 'L_Cheecks_3_POCI', 'R_Cheecks_Rig_GrpMirror_Grp', 'R_Cheecks_Mid_Jnt_Offset_Grp', 'R_Cheecks_Bone_3_Jnt_Offset_Grp', 'R_Cheecks_2_Bnd_scaleConstraint1', 'L_Cheecks_Bone_0_Jnt_Auto_Grp', 'R_Cheecks_Bone_2_Jnt_Root_Grp', 'R_Cheecks_Btm_Ctrl', 'R_Cheecks_0_Bnd_scaleConstraint1', 'L_Cheecks_Ctrl_Grp', 'L_Cheecks_MidBtm_Jnt_Offset_Grp_parentConstraint1', 'L_Cheecks_1_Bnd', 'R_Cheecks_Main_Jnt_Root_Grp', 'L_Cheecks_3_Bnd_scaleConstraint1', 'bindPose9', 'L_Cheecks_0_CtrlShape', 'R_Cheecks_0_Jnt_Offset_Grp', 'L_Cheecks_2_Ctrl_Offset_Grp', 'R_Cheecks_Top_CtrlShape', 'R_Cheecks_4_Jnt', 'R_Cheecks_Bone_2_Ctrl', 'L_Cheecks_Tweeks_Ctrl_Grp', 'L_Cheecks_MidBtm_Ctrl_Offset_Grp', 'R_Cheecks_3_POCI', 'R_Cheecks_Main_Bone_Ctrl_Offset_Grp', 'L_Cheecks_Main_Ctrl_tag', 'R_Cheecks_TopMid_Ctrl_Offset_Grp_parentConstraint1', 'R_Cheecks_0_Ctrl_tag', 'L_Cheecks_Main_Bone_Ctrl', 'L_Cheecks_Bone_2_Bnd', 'L_Cheecks_Bone_1_Jnt_Auto_Grp', 'L_Cheecks_TopMid_CtrlShape', 'R_Cheecks_Wire', 'L_Cheecks_3_Ctrl_tag', 'L_Cheecks_Main_CtrlShape', 'L_Cheecks_Main_Ctrl_Grp', 'R_Cheecks_Mid_Jnt', 'L_Cheecks_Border_Driver_CrvShape', 'L_Cheecks_Btm_Jnt', 'L_Cheecks_Mid_Ctrl_Offset_Grp', 'L_Cheecks_0_Bnd_scaleConstraint1', 'R_Cheecks_5_Jnt', 'R_Cheecks_Bone_3_Ctrl_tag', 'L_Cheecks_3_Jnt', 'L_Cheecks_Bone_0_Ctrl_Offset_Grp', 'L_Cheecks_0_Ctrl_tag', 'R_Cheecks_Bone_3_Jnt_Root_Grp', 'L_Cheecks_Main_Ctrl', 'L_Cheecks_Bone_3_CtrlShape', 'L_Cheecks_Bone_0_CtrlShape', 'L_Cheecks_Bone_2_Jnt_Auto_Grp', 'L_Cheecks_TopMid_Jnt_Offset_Grp', 'L_Cheecks_Bone_0_Bnd_scaleConstraint1', 'L_Cheecks_Btm_Jnt_Offset_Grp', 'L_Cheecks_Bone_0_Bnd', 'L_Cheecks_0_Bnd', 'L_Cheecks_Bone_3_Ctrl', 'L_Cheecks_Border_Linear_CrvShape', 'L_Cheecks_Mid_Ctrl', 'R_Cheecks_MidBtm_Ctrl', 'L_Cheecks_Bone_1_CtrlShape', 'L_Cheecks_Bone_1_Bnd', 'R_Cheecks_Btm_Jnt_Offset_Grp', 'L_Cheecks_MidBtm_Jnt', 'R_Cheecks_2_Ctrl_tag', 'L_Cheecks_1_Ctrl_Offset_Grp', 'R_Cheecks_1_Ctrl_tag', 'L_Cheecks_Bone_2_Jnt_Root_Grp', 'R_Cheecks_0_Jnt', 'R_Cheecks_1_Bnd', 'R_Cheecks_Top_Ctrl_tag', 'L_Cheecks_Bone_2_Bnd_parentConstraint1', 'L_Cheecks_Bone_1_Jnt', 'R_Cheecks_Bone_0_Ctrl', 'R_Cheecks_Border_Driver_CrvShapeOrig', 'R_Cheecks_MidBtm_Ctrl_tag', 'L_Cheecks_4_Ctrl_tag', 'R_Cheecks_Border_Driver_Crv', 'R_Cheecks_Bone_2_Bnd', 'L_Cheecks_TweekJnts_Grp', 'R_Cheecks_Btm_CtrlShape', 'R_Cheecks_3_Ctrl', 'R_Cheecks_5_Bnd_scaleConstraint1', 'R_Cheecks_Bone_0_Jnt_Auto_Grp', 'R_Cheecks_Mid_CtrlShape', 'R_Cheecks_3_Ctrl_tag', 'R_Cheecks_Bone_3_Ctrl', 'L_Cheecks_5_Ctrl_tag', 'R_Cheecks_Bone_0_Jnt_Root_Grp', 'L_Cheecks_1_Bnd_scaleConstraint1', 'R_Cheecks_TopMid_Ctrl_Offset_Grp', 'R_Cheecks_TopMid_Jnt_Offset_Grp', 'L_Cheecks_Main_Bone_CtrlShape', 'skinCluster10', 'L_Cheecks_Bone_3_Bnd_parentConstraint1', 'R_Cheecks_4_Jnt_Offset_Grp', 'R_Cheecks_0_CtrlShape', 'R_Cheecks_MidBtm_Jnt', 'L_Cheecks_5_Bnd_scaleConstraint1', 'L_Cheecks_4_Ctrl', 'R_Cheecks_Main_Bnd_parentConstraint1', 'R_Cheecks_Bone_1_Jnt', 'L_Cheecks_Bone_3_Ctrl_Offset_Grp', 'L_Cheecks_MidBtm_Ctrl', 'R_Cheecks_Main_Jnt_Auto_Grp', 'R_Cheecks_3_CtrlShape', 'R_Cheecks_Bone_0_Bnd_scaleConstraint1', 'R_Cheecks_4_Bnd', 'R_Cheecks_0_Ctrl', 'R_Cheecks_Top_Ctrl_Offset_Grp', 'L_Cheecks_Bone_1_Ctrl_tag', 'R_Cheecks_Main_Jnt', 'L_Cheecks_TopMid_Ctrl_Offset_Grp_parentConstraint1', 'skinCluster9', 'L_Cheecks_Bone_0_Bnd_parentConstraint1', 'R_Cheecks_3_Bnd', 'L_Cheecks_4_Bnd', 'R_Cheecks_Bone_2_Jnt_Auto_Grp', 'R_Cheecks_Bone_3_CtrlShape', 'R_Cheecks_Main_Bnd', 'L_Cheecks_Bone_1_Ctrl_Offset_Grp', 'R_Cheecks_1_CtrlShape', 'R_Cheecks_3_Jnt', 'R_Cheecks_Main_Bone_CtrlShape', 'L_Cheecks_Bone_0_Jnt_Root_Grp', 'R_Cheecks_Bone_0_Jnt_Offset_Grp', 'R_Cheecks_Bone_3_Bnd_parentConstraint1', 'L_Cheecks_Mid_Jnt', 'R_Cheecks_TopMid_Jnt', 'L_Cheecks_Border_Driver_CrvBaseWireShape', 'L_Cheecks_2_Jnt_Offset_Grp', 'R_Cheecks_Bone_2_Ctrl_Offset_Grp', 'L_Cheecks_5_Jnt_Offset_Grp', 'R_Cheecks_5_Jnt_Offset_Grp', 'R_Cheecks_Bone_3_Bnd_scaleConstraint1', 'R_Cheecks_Rig_Grp', 'L_Cheecks_2_Ctrl', 'R_Cheecks_MidBtm_Ctrl_Offset_Grp', 'L_Cheecks_Bone_3_Bnd', 'R_Cheecks_Mid_Ctrl', 'L_Cheecks_1_CtrlShape', 'R_Cheecks_Bone_0_Jnt', 'R_Cheecks_Main_Ctrl_Offset_Grp', 'R_Cheecks_TopMid_CtrlShape', 'L_Cheecks_3_Bnd_parentConstraint1', 'L_Cheecks_Bone_2_Ctrl_tag', 'L_Cheecks_0_Bnd_parentConstraint1', 'L_Cheecks_0_Jnt_Offset_Grp', 'L_Cheecks_Ctrl_Grp_parentConstraint1', 'L_Cheecks_Top_Jnt_Offset_Grp', 'R_Cheecks_Btm_Ctrl_Offset_Grp', 'R_Cheecks_Border_Linear_CrvShapeOrig', 'R_Cheecks_0_POCI', 'L_Cheecks_TopMid_Ctrl_Offset_Grp', 'L_Cheecks_4_Bnd_scaleConstraint1', 'R_Cheecks_Bone_1_Bnd_scaleConstraint1', 'R_Cheecks_Bone_2_Bnd_scaleConstraint1', 'R_Cheecks_TopMid_Ctrl_tag', 'L_Cheecks_Top_Ctrl', 'R_Cheecks_0_Bnd_parentConstraint1', 'L_Cheecks_2_Bnd', 'R_Cheecks_Ctrl_Grp_parentConstraint1', 'L_Cheecks_Btm_Ctrl_tag', 'L_Cheecks_3_Jnt_Offset_Grp', 'R_Cheecks_1_Ctrl', 'L_Cheecks_1_Ctrl_tag', 'R_Cheecks_Top_Ctrl', 'R_Cheecks_2_POCI', 'R_Cheecks_Main_Bone_Ctrl_tag', 'L_Cheecks_1_Bnd_parentConstraint1', 'L_Cheecks_Main_Bone_Ctrl_tag', 'L_Cheecks_Bone_3_Jnt_Auto_Grp', 'R_Cheecks_0_Ctrl_Offset_Grp', 'L_Cheecks_Main_Jnt', 'R_Cheecks_Border_Driver_CrvShape', 'L_Cheecks_Rig_Grp', 'R_Cheecks_Bone_1_Ctrl_Offset_Grp', 'R_Cheecks_1_Ctrl_Offset_Grp', 'R_Cheecks_Bone_2_Jnt', 'R_Cheecks_Bone_2_CtrlShape', 'R_Cheecks_1_Bnd_scaleConstraint1', 'L_Cheecks_1_Ctrl', 'R_Cheecks_Top_Jnt_Offset_Grp', 'R_Cheecks_Bone_1_Jnt_Offset_Grp', 'R_Cheecks_3_Jnt_Offset_Grp', 'R_Cheecks_Bone_3_Bnd', 'L_Cheecks_4_Bnd_parentConstraint1', 'R_Cheecks_3_Bnd_parentConstraint1', 'L_Cheecks_3_Ctrl', 'R_Cheecks_Bone_2_Bnd_parentConstraint1', 'L_Cheecks_MidBtm_Jnt_Offset_Grp', 'R_Cheecks_5_POCI', 'L_Cheecks_Main_Jnt_Auto_Grp', 'L_Cheecks_5_Bnd', 'R_Cheecks_Bone_0_Ctrl_tag', 'L_Cheecks_Mid_Jnt_Offset_Grp', 'R_Cheecks_Border_Linear_CrvShape', 'L_Cheecks_Wire', 'R_Cheecks_Main_CtrlShape', 'R_Cheecks_MidBtm_Jnt_Offset_Grp_parentConstraint1', 'L_Cheecks_2_Jnt', 'R_Cheecks_Main_Ctrl_Grp', 'L_Cheecks_Main_Jnt_Root_Grp', 'R_Cheecks_2_Ctrl', 'R_Cheecks_5_CtrlShape', 'L_Cheecks_Top_Ctrl_Offset_Grp', 'R_Cheecks_1_Jnt_Offset_Grp', 'R_Cheecks_MidBtm_Jnt_Offset_Grp', 'L_Cheecks_0_Ctrl', 'L_Cheecks_2_CtrlShape', 'R_Cheecks_Top_Jnt', 'R_Cheecks_3_Ctrl_Offset_Grp', 'L_Cheecks_TopMid_Jnt', 'L_Cheecks_4_Jnt', 'L_Cheecks_Bone_1_Jnt_Offset_Grp', 'R_Cheecks_4_Bnd_scaleConstraint1', 'R_Cheecks_Bone_0_Bnd', 'L_Cheecks_Bone_3_Jnt', 'L_Cheecks_5_Ctrl_Offset_Grp', 'L_Cheecks_Main_Bnd', 'R_Cheecks_Ctrl_GrpMirror_Grp', 'R_Cheecks_Bone_1_Bnd_parentConstraint1', 'L_Cheecks_Bone_0_Jnt', 'R_Cheecks_Bone_1_Ctrl_tag', 'R_Cheecks_Main_Bone_Ctrl', 'R_Cheecks_5_Ctrl_tag', 'L_Cheecks_4_Jnt_Offset_Grp', 'L_Cheecks_4_CtrlShape', 'R_Cheecks_5_Bnd_parentConstraint1', 'R_Cheecks_4_POCI', 'L_Cheecks_Bone_2_Jnt_Offset_Grp', 'R_Cheecks_Border_Driver_CrvBaseWire']");
createNode transform -n "L_Cheecks_Bone_Guide" -p "L_Cheecks_Block";
	rename -uid "27154000-0018-1FF3-6621-A96000000F42";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2024/scripts/rigging/Mutant_Tools/Icons/";
	setAttr ".ove" yes;
	setAttr ".ovc" 9;
	setAttr ".t" -type "double3" 4.1599141417601695 20.882686834291832 5.7687758624648797 ;
	setAttr ".rp" -type "double3" -1.3298191166236342 1.5924050533712659 1.6515424252077375 ;
	setAttr ".sp" -type "double3" -1.3298191166236342 1.5924050533712659 1.6515424252077375 ;
createNode nurbsCurve -n "curveShape8" -p "L_Cheecks_Bone_Guide";
	rename -uid "27154000-0018-1FF3-6621-A96000000F43";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2024/scripts/rigging/Mutant_Tools/Icons/";
	setAttr -k off ".v";
	setAttr ".cc" -type "nurbsCurve" 
		1 3 0 no 3
		4 0 1 2 3
		4
		-13.714415675268469 -9.9781623496729193 -10.049072188148475
		-1.9497202693083864 -8.7738166465478979 -0.20576373935697134
		2.7514780701538939 -7.2438178672510141 2.7187758266830677
		-1.8149350939849 -9.5036140098291249 -15.814884108314491
		;
createNode transform -n "L_Cheecks_Border_Guide" -p "L_Cheecks_Block";
	rename -uid "27154000-0018-1FF3-6621-A96000000F44";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2024/scripts/rigging/Mutant_Tools/Icons/";
	setAttr ".ove" yes;
	setAttr ".ovc" 14;
	setAttr ".t" -type "double3" 3.6158399563965151 5.2414803233009764 12.430187244266724 ;
	setAttr ".r" -type "double3" 0.3108070274634715 45.611992120441393 3.5521935370831326e-17 ;
	setAttr ".s" -type "double3" 0.99999999999999933 1 0.99999999999999933 ;
	setAttr ".rp" -type "double3" 2.4838894999999983 2.6558509999999997 0 ;
	setAttr ".rpt" -type "double3" -0.73607912745263326 -3.9075904586858071e-05 -1.7649570838577642 ;
	setAttr ".sp" -type "double3" 2.4838895000000001 2.6558509999999997 0 ;
	setAttr ".spt" -type "double3" -1.7763568394002481e-15 0 0 ;
createNode nurbsCurve -n "curveShape7" -p "L_Cheecks_Border_Guide";
	rename -uid "27154000-0018-1FF3-6621-A96000000F45";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2024/scripts/rigging/Mutant_Tools/Icons/";
	setAttr -k off ".v";
	setAttr ".cc" -type "nurbsCurve" 
		1 5 0 no 3
		6 0 1 2 3 4 5
		6
		1.04930905005244 6.665009368634605 -2.0242594950092396
		2.5237695003782745 5.384450634462743 -1.3167099566048215
		3.3883479182024523 3.5569807836232878 -1.196604902099037
		3.5682218231113474 1.7677125706631713 -1.5559704139863761
		2.7432136265335028 -0.2850249872813756 -2.2176463706453839
		1.3369172021740878 -1.2317411854564548 -2.6004252696082633
		;
createNode joint -n "L_Cheecks_Guide" -p "L_Cheecks_Block";
	rename -uid "27154000-0018-1FF3-6621-A96000000F46";
	addAttr -ci true -sn "Helper" -ln "Helper" -min 0 -max 1 -en "Hide:Show" -at "enum";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2024/scripts/rigging/Mutant_Tools/Icons/";
	setAttr ".t" -type "double3" 2.9751242410366259 7.8211158940810037 6.5047076064086138 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr -cb on ".Helper" 1;
createNode nurbsCurve -n "L_Cheecks_Guide_CtrlShape" -p "L_Cheecks_Guide";
	rename -uid "27154000-0018-1FF3-6621-A96000000F47";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2024/scripts/rigging/Mutant_Tools/Icons/";
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
createNode nurbsCurve -n "L_Cheecks_Guide_Ctrl_CtrlShape" -p "L_Cheecks_Guide";
	rename -uid "27154000-0018-1FF3-6621-A96000000F48";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2024/scripts/rigging/Mutant_Tools/Icons/";
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
createNode nurbsCurve -n "L_Cheecks_Guide_Ctrl_Ctrl_CtrlShape" -p "L_Cheecks_Guide";
	rename -uid "27154000-0018-1FF3-6621-A96000000F49";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2024/scripts/rigging/Mutant_Tools/Icons/";
	setAttr -k off ".v";
	setAttr ".ove" yes;
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
createNode nurbsCurve -n "L_Cheecks_Guide_Ctrl_Ctrl_Ctrl_CtrlShape" -p "L_Cheecks_Guide";
	rename -uid "27154000-0018-1FF3-6621-A96000000F4A";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2024/scripts/rigging/Mutant_Tools/Icons/";
	setAttr -k off ".v";
	setAttr ".ove" yes;
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
createNode dagContainer -n "Lips_Block" -p "face";
	rename -uid "27154000-0018-1FF3-6621-A96000000F4B";
	addAttr -ci true -sn "nts" -ln "notes" -dt "string";
	setAttr ".isc" yes;
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2024/scripts/rigging/Mutant_Tools/Icons/RibbonLips.png";
	setAttr ".ctor" -type "string" "esteban.rodriguez";
	setAttr ".cdat" -type "string" "2024/02/13 14:28:57";
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
		"['Lips_Centerlips_Grp', 'R_Lips_Lwr_01_FolShape', 'R_Lips_Lwr_02_Ctrl_MultDiv1', 'R_Lips_Lwr_Local_Loc', 'C_Lips_Lwr_Ctrl_MultDiv2', 'R_Lips_Lwr_01_CtrlShape', 'L_Lips_Upr_02_Ctrl_MultDiv2', 'R_Lips_Upr_02_Ctrl_MultDiv1', 'Lips_Upr_Jnt_Ctrl_Grp', 'C_Lips_Lwr_Ctrl_Jnt_Root_Grp_parentConstraint1', 'L_Lips_Lwr_02_Ctrl_Jnt', 'unitConversion27', 'R_Lips_Lwr_01_Ctrl_Jnt_Auto_Grp', 'unitConversion25', 'L_Lips_Lwr_02_Ctrl_MultDiv', 'R_Lips_Lwr_01_Ctrl_Jnt_Root_Grp_parentConstraint1', 'R_Lips_Upr_02_Ctrl_Jnt_Root_Grp_parentConstraint1', 'C_Lips_Lwr_Ctrl_tag', 'Lips_Upr_Local_Loc_Grp', 'R_Lips_Upr_02_Bnd_parentConstraint1', 'R_Lips_Lwr_Local_LocShape', 'unitConversion29', 'R_Lips_Upr_01_Ctrl_Jnt_Root_Grp_parentConstraint1', 'unitConversion40', 'L_Lips_Upr_01_Bnd_scaleConstraint1', 'R_Lips_Lwr_02_Ctrl_tag', 'R_Lips_Main_Ctrl_Offset_Grp', 'R_Lips_Upr_Local_Loc_Offset_Grp', 'R_Lips_Lwr_01_Bnd_scaleConstraint1', 'R_Lips_Upr_01_Ctrl_Jnt_Root_GrpMirror_Grp', 'L_Lips_Upr_02_Bnd', 'L_Lips_Upr_Local_LocCentralRotator_Grp', 'R_Lips_Lwr_02_Bnd_scaleConstraint1', 'L_Lips_Upr_01_Ctrl_Jnt_Root_Grp', 'unitConversion26', 'C_Lips_Lwr_Local_Loc_Offset_Grp', 'L_Lips_Upr_01_Ctrl_MultDiv', 'R_Lips_Main_Ctrl_MultDiv2', 'R_Lips_Lwr_02_Ctrl_Jnt', 'R_Lips_Upr_02_FolShape', 'R_Lips_Upr_01_Ctrl_Jnt_Root_Grp', 'unitConversion30', 'C_Lips_Upr_Ctrl_Jnt_Root_Grp_parentConstraint1', 'L_Lips_Lwr_01_Ctrl_MultDiv2', 'L_Lips_Main_CtrlShape', 'R_Lips_Main_CtrlShape', 'L_Lips_Upr_02_Ctrl_Jnt_Root_Grp_parentConstraint1', 'L_Lips_Main_Ctrl_MultDiv4', 'Lips_Lwr_NurbShape', 'Lips_Center_Ctrl_Offset_Grp', 'L_Lips_Upr_02_Bnd_parentConstraint1', 'L_Lips_Lwr_01_Bnd_scaleConstraint1', 'L_Lips_Upr_01_Bnd_parentConstraint1', 'L_Lips_Lwr_01_Bnd', 'C_Lips_Upr_Main_Ctrl_tag', 'R_Lips_Upr_01_Bnd_scaleConstraint1', 'R_Lips_Lwr_Local_LocCentralRotator_GrpMirror_Grp', 'C_Lips_Upr_Ctrl_Offset_Grp', 'C_Lips_Lwr_Bnd', 'C_Lips_Upr_Ctrl', 'skinCluster12', 'R_Lips_Upr_01_Fol', 'C_Lips_Lwr_Main_Ctrl', 'unitConversion41', 'C_Lips_Upr_Main_CtrlShape', 'Lips_Center_CtrlShape', 'L_Lips_Lwr_01_Ctrl_Offset_Grp', 'C_Lips_Lwr_Ctrl_Jnt_Auto_Grp', 'C_Lips_Upr_Ctrl_Jnt_Auto_Grp', 'bindPose12', 'R_Lips_Lwr_01_Ctrl_MultDiv1', 'L_Lips_Upr_02_Fol_Jnt', 'C_Lips_Lwr_Main_Ctrl_tag', 'Lips_Center_Ctrl_tag', 'L_Lips_Upr_02_Ctrl_MultDiv', 'R_Lips_Lwr_02_Fol', 'L_Lips_Upr_01_Ctrl_MultDiv2', 'C_Lips_Upr_Fol', 'L_Lips_Main_Ctrl_MultDiv3', 'C_Lips_Upr_Local_Loc', 'L_Lips_Sub_Ctrl_tag', 'unitConversion38', 'L_Lips_Upr_01_Ctrl_tag', 'L_Lips_Upr_01_Ctrl_Jnt_Root_Grp_parentConstraint1', 'L_Lips_Sub_Loc_Root_Grp', 'R_Lips_Upr_02_CtrlShape', 'R_Lips_Lwr_02_Ctrl', 'R_Lips_Lwr_01_Bnd_parentConstraint1', 'R_Lips_Lwr_01_Ctrl_tag', 'skinCluster11', 'C_Lips_Lwr_Ctrl_MultDiv1', 'R_Lips_Lwr_02_Ctrl_Jnt_Auto_Grp', 'R_Lips_Lwr_02_Ctrl_Offset_GrpMirror_Grp', 'L_Lips_Lwr_02_Ctrl_MultDiv1', 'L_Lips_Lwr_02_Ctrl_Offset_Grp', 'R_Lips_Upr_01_Ctrl_tag', 'L_Lips_Lwr_02_Ctrl_MultDiv2', 'L_Lips_Upr_01_Fol_Jnt', 'C_Lips_Upr_CtrlShape', 'L_Lips_Sub_Ctrl_Offset_Grp', 'R_Lips_Sub_CtrlShape', 'R_Lips_Lwr_Local_LocCentralRotator_Grp', 'L_Lips_Lwr_01_Fol_Jnt', 'L_Lips_Lwr_02_FolShape', 'C_Lips_Upr_Ctrl_MultDiv2', 'L_Lips_Sub_Ctrl', 'R_Lips_Lwr_01_Ctrl_Jnt_Root_GrpMirror_Grp', 'C_Lips_Lwr_CtrlShape', 'C_Lips_Upr_Bnd', 'L_Lips_Upr_01_Ctrl_Jnt', 'unitConversion28', 'Lips_Center_Grp_Offset_Grp', 'R_Lips_Lwr_02_Bnd', 'R_Lips_Sub_Ctrl_Offset_Grp', 'C_Lips_Upr_Local_Loc_Offset_Grp', 'C_Lips_Upr_Ctrl_Jnt_Root_Grp', 'R_Lips_Lwr_01_Ctrl', 'L_Lips_Upr_02_Ctrl_tag', 'L_Lips_Lwr_02_Ctrl_tag', 'bindPose11', 'L_Lips_Lwr_01_FolShape', 'Lips_Lwr_Local_Loc_Grp', 'Lips_Ctrl_Grp_parentConstraint1', 'R_Lips_Lwr_02_Ctrl_Jnt_Root_GrpMirror_Grp', 'R_Lips_Lwr_01_Ctrl_Jnt', 'L_Lips_Upr_02_Ctrl_Offset_Grp', 'R_Lips_Upr_01_Ctrl_Offset_Grp', 'R_Lips_Lwr_02_Fol_Jnt', 'L_Lips_Upr_02_Ctrl', 'L_Lips_Lwr_Local_LocCentralRotator_Grp', 'R_Lips_Lwr_Local_Loc_Offset_Grp', 'R_Lips_Lwr_02_Bnd_parentConstraint1', 'R_Lips_Main_Ctrl_DLOut', 'R_Lips_Main_Ctrl_DLOut2', 'L_Lips_Main_Ctrl_Offset_Grp', 'L_Lips_Upr_01_Ctrl_Offset_Grp', 'L_Lips_Sub_Loc_Auto_Grp', 'unitConversion39', 'R_Lips_Upr_01_Fol_Jnt', 'C_Lips_Lwr_Ctrl_Offset_Grp', 'R_Lips_Upr_01_Ctrl', 'R_Lips_Sub_Ctrl_tag', 'C_Lips_Upr_FolShape', 'L_Lips_Lwr_02_Ctrl_Jnt_Root_Grp_parentConstraint1', 'L_Lips_Main_Ctrl_DLOut3', 'L_Lips_Sub_CtrlShape', 'L_Lips_Sub_LocShape', 'L_Lips_Main_Ctrl', 'C_Lips_Lwr_Fol_Jnt', 'L_Lips_Upr_01_CtrlShape', 'L_Lips_Upr_01_Ctrl_MultDiv1', 'R_Lips_Main_Ctrl_DLOut3', 'R_Lips_Lwr_02_FolShape', 'L_Lips_Lwr_01_Ctrl_tag', 'L_Lips_Main_Ctrl_MultDiv1', 'L_Lips_Sub_Loc', 'C_Lips_Lwr_Ctrl_MultDiv', 'L_Lips_Lwr_Local_Loc', 'L_Lips_Lwr_02_Fol', 'Lips_Upr_Fol_Grp', 'L_Lips_Main_Ctrl_MultDiv5', 'R_Lips_Main_Ctrl', 'C_Lips_Upr_Main_Ctrl', 'unitConversion31', 'L_Lips_Upr_02_Bnd_scaleConstraint1', 'R_Lips_Lwr_02_CtrlShape', 'Lips_Ctrl_Grp', 'L_Lips_Upr_01_Ctrl', 'R_Lips_Main_Ctrl_DLOut4', 'L_Lips_Upr_02_Fol', 'L_Lips_Lwr_Local_LocShape', 'R_Lips_Upr_02_Ctrl_Jnt_Root_Grp', 'R_Lips_Upr_01_Ctrl_Jnt_Auto_Grp', 'R_Lips_Sub_Ctrl', 'L_Lips_Lwr_01_CtrlShape', 'L_Lips_Lwr_02_Bnd', 'R_Lips_Sub_Loc_Root_Grp', 'R_Lips_Upr_Local_LocShape', 'Lips_Rig_Grp', 'R_Lips_Upr_01_Ctrl_Offset_GrpMirror_Grp', 'R_Lips_Upr_01_Ctrl_MultDiv2', 'Lips_Upr_NurbShape', 'R_Lips_Lwr_01_Fol', 'R_Lips_Upr_Local_LocCentralRotator_GrpMirror_Grp', 'R_Lips_Main_Ctrl_DLOut5', 'L_Lips_Main_Ctrl_DLOut2', 'L_Lips_Main_Ctrl_MultDiv', 'L_Lips_Lwr_01_Bnd_parentConstraint1', 'L_Lips_Upr_Local_Loc', 'R_Lips_Sub_LocShape', 'R_Lips_Upr_02_Ctrl_Jnt_Root_GrpMirror_Grp', 'R_Lips_Main_Ctrl_MultDiv5', 'R_Lips_Upr_01_Bnd_parentConstraint1', 'R_Lips_Upr_Local_Loc', 'R_Lips_Lwr_02_Ctrl_MultDiv', 'Lips_Center_Grp', 'R_Lips_Upr_01_CtrlShape', 'R_Lips_Upr_02_Ctrl_Offset_GrpMirror_Grp', 'unitConversion32', 'C_Lips_Upr_Fol_Jnt', 'R_Lips_Upr_02_Bnd', 'L_Lips_Lwr_02_CtrlShape', 'R_Lips_Upr_02_Bnd_scaleConstraint1', 'Lips_Lwr_Ctrl_Grp', 'Lips_Upr_NurbShapeOrig', 'Lips_Lwr_NurbShapeOrig', 'unitConversion33', 'L_Lips_Main_Ctrl_tag', 'R_Lips_Main_Ctrl_MultDiv1', 'C_Lips_Lwr_FolShape', 'C_Lips_Upr_Ctrl_MultDiv', 'R_Lips_Upr_01_Ctrl_MultDiv1', 'R_Lips_Lwr_02_Ctrl_Offset_Grp', 'R_Lips_Upr_01_FolShape', 'C_Lips_Upr_Ctrl_MultDiv1', 'L_Lips_Upr_02_Ctrl_Jnt_Auto_Grp', 'C_Lips_Upr_Bnd_parentConstraint1', 'C_Lips_Lwr_Main_Ctrl_Offset_Grp', 'L_Lips_Upr_02_Ctrl_Jnt', 'unitConversion34', 'R_Lips_Sub_Loc', 'C_Lips_Lwr_Main_CtrlShape', 'C_Lips_Upr_Ctrl_Jnt', 'L_Lips_Upr_01_Bnd', 'Lips_Lwr_Jnt_Ctrl_Grp', 'L_Lips_Main_Ctrl_MultDiv2', 'R_Lips_Main_Ctrl_MultDiv3', 'C_Lips_Lwr_Local_LocCentralRotator_Grp', 'Lips_Center_Ctrl', 'L_Lips_Main_Ctrl_DLOut', 'C_Lips_Lwr_Bnd_scaleConstraint1', 'unitConversion36', 'R_Lips_Lwr_01_Ctrl_Jnt_Root_Grp', 'R_Lips_Upr_02_Ctrl_Jnt', 'R_Lips_Upr_02_Fol', 'C_Lips_Upr_Bnd_scaleConstraint1', 'R_Lips_Main_Ctrl_MultDiv4', 'R_Lips_Upr_02_Ctrl_MultDiv', 'R_Lips_Lwr_01_Bnd', 'C_Lips_Lwr_Local_LocShape', 'L_Lips_Lwr_01_Ctrl', 'unitConversion37', 'L_Lips_Lwr_02_Ctrl_Jnt_Root_Grp', 'R_Lips_Lwr_01_Ctrl_Offset_Grp', 'L_Lips_Lwr_02_Bnd_scaleConstraint1', 'R_Lips_Upr_02_Ctrl_Jnt_Auto_Grp', 'L_Lips_Lwr_02_Fol_Jnt', 'R_Lips_Upr_02_Ctrl_Offset_Grp', 'L_Lips_Main_Ctrl_DLOut4', 'L_Lips_Upr_01_Ctrl_Jnt_Auto_Grp', 'L_Lips_Main_Ctrl_DLOut1', 'L_Lips_Upr_02_FolShape', 'C_Lips_Upr_Main_Ctrl_Offset_Grp', 'R_Lips_Lwr_02_Ctrl_MultDiv2', 'R_Lips_Upr_Local_LocCentralRotator_Grp', 'Lips_Upr_Ctrl_Grp', 'L_Lips_Lwr_02_Bnd_parentConstraint1', 'Lips_Lwr_Fol_Grp', 'C_Lips_Lwr_Fol', 'C_Lips_Upr_Local_LocCentralRotator_Grp', 'Lips_Lwr_Nurb', 'R_Lips_Main_Ctrl_Offset_GrpMirror_Grp', 'unitConversion42', 'C_Lips_Upr_Ctrl_tag', 'R_Lips_Lwr_02_Ctrl_Jnt_Root_Grp_parentConstraint1', 'L_Lips_Upr_Local_Loc_Offset_Grp', 'L_Lips_Upr_02_Ctrl_MultDiv1', 'R_Lips_Main_Ctrl_MultDiv', 'R_Lips_Upr_02_Ctrl', 'R_Lips_Lwr_01_Ctrl_MultDiv2', 'C_Lips_Lwr_Ctrl_Jnt', 'L_Lips_Lwr_Local_Loc_Offset_Grp', 'Lips_Upr_Nurb', 'L_Lips_Lwr_01_Fol', 'R_Lips_Upr_02_Ctrl_tag', 'L_Lips_Upr_01_FolShape', 'Lips_Centerlips_Grp_Offset_Grp', 'R_Lips_Upr_01_Ctrl_MultDiv', 'R_Lips_Upr_01_Ctrl_Jnt', 'R_Lips_Upr_02_Ctrl_MultDiv2', 'L_Lips_Lwr_01_Ctrl_Jnt_Root_Grp_parentConstraint1', 'L_Lips_Lwr_02_Ctrl_Jnt_Auto_Grp', 'C_Lips_Lwr_Ctrl_Jnt_Root_Grp', 'R_Lips_Sub_Loc_Root_GrpMirror_Grp', 'R_Lips_Lwr_01_Ctrl_Offset_GrpMirror_Grp', 'R_Lips_Lwr_02_Ctrl_Jnt_Root_Grp', 'L_Lips_Lwr_01_Ctrl_Jnt_Root_Grp', 'L_Lips_Lwr_01_Ctrl_MultDiv', 'R_Lips_Upr_01_Bnd', 'R_Lips_Main_Ctrl_tag', 'L_Lips_Main_Ctrl_DLOut5', 'L_Lips_Lwr_02_Ctrl', 'L_Lips_Upr_02_Ctrl_Jnt_Root_Grp', 'C_Lips_Lwr_Ctrl', 'L_Lips_Lwr_01_Ctrl_Jnt', 'L_Lips_Upr_Local_LocShape', 'C_Lips_Lwr_Bnd_parentConstraint1', 'R_Lips_Lwr_01_Ctrl_MultDiv', 'C_Lips_Lwr_Local_Loc', 'R_Lips_Lwr_01_Fol_Jnt', 'C_Lips_Upr_Local_LocShape', 'L_Lips_Upr_02_CtrlShape', 'R_Lips_Upr_02_Fol_Jnt', 'L_Lips_Lwr_01_Ctrl_Jnt_Auto_Grp', 'unitConversion35', 'L_Lips_Lwr_01_Ctrl_MultDiv1', 'R_Lips_Sub_Loc_Auto_Grp', 'L_Lips_Upr_01_Fol', 'Lips_Ctrl_Grp_scaleConstraint1', 'R_Lips_Main_Ctrl_DLOut1']");
createNode joint -n "L_Lips_Orient_Guide_Guide" -p "Lips_Block";
	rename -uid "27154000-0018-1FF3-6621-A96000000F4C";
	addAttr -ci true -sn "Helper" -ln "Helper" -min 0 -max 1 -en "Hide:Show" -at "enum";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2024/scripts/rigging/Mutant_Tools/Icons/";
	setAttr ".t" -type "double3" 3.7783101610418517 7.8002812598038815 9.6083715298839714 ;
	setAttr ".r" -type "double3" 0.3108070274634715 45.611992120441421 1.7760967685415675e-17 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr -cb on ".Helper" 1;
createNode nurbsCurve -n "L_Lips_Orient_Guide_Guide_CtrlShape" -p "L_Lips_Orient_Guide_Guide";
	rename -uid "27154000-0018-1FF3-6621-A96000000F4D";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2024/scripts/rigging/Mutant_Tools/Icons/";
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
createNode nurbsCurve -n "L_Lips_Orient_Guide_Guide_Ctrl_CtrlShape" -p "L_Lips_Orient_Guide_Guide";
	rename -uid "27154000-0018-1FF3-6621-A96000000F4E";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2024/scripts/rigging/Mutant_Tools/Icons/";
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
createNode nurbsCurve -n "L_Lips_Orient_Guide_Guide_Ctrl_Ctrl_CtrlShape" -p "L_Lips_Orient_Guide_Guide";
	rename -uid "27154000-0018-1FF3-6621-A96000000F4F";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2024/scripts/rigging/Mutant_Tools/Icons/";
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
createNode nurbsCurve -n "L_Lips_Orient_Guide_Guide_Ctrl_Ctrl_Ctrl_CtrlShape" -p "L_Lips_Orient_Guide_Guide";
	rename -uid "27154000-0018-1FF3-6621-A96000000F50";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2024/scripts/rigging/Mutant_Tools/Icons/";
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
createNode joint -n "Lips_SlideCenter_Guide_Guide" -p "Lips_Block";
	rename -uid "27154000-0018-1FF3-6621-A96000000F51";
	addAttr -ci true -sn "Helper" -ln "Helper" -min 0 -max 1 -en "Hide:Show" -at "enum";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2024/scripts/rigging/Mutant_Tools/Icons/";
	setAttr ".t" -type "double3" 0.04632849522593574 7.8286109523068603 5.9552749389890414 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr -cb on ".Helper" 1;
createNode nurbsCurve -n "Lips_SlideCenter_Guide_Guide_CtrlShape" -p "Lips_SlideCenter_Guide_Guide";
	rename -uid "27154000-0018-1FF3-6621-A96000000F52";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2024/scripts/rigging/Mutant_Tools/Icons/";
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
createNode nurbsCurve -n "Lips_SlideCenter_Guide_Guide_Ctrl_CtrlShape" -p "Lips_SlideCenter_Guide_Guide";
	rename -uid "27154000-0018-1FF3-6621-A96000000F53";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2024/scripts/rigging/Mutant_Tools/Icons/";
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
createNode nurbsCurve -n "Lips_SlideCenter_Guide_Guide_Ctrl_Ctrl_CtrlShape" -p "Lips_SlideCenter_Guide_Guide";
	rename -uid "27154000-0018-1FF3-6621-A96000000F54";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2024/scripts/rigging/Mutant_Tools/Icons/";
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
createNode nurbsCurve -n "Lips_SlideCenter_Guide_Guide_Ctrl_Ctrl_Ctrl_CtrlShape" 
		-p "Lips_SlideCenter_Guide_Guide";
	rename -uid "27154000-0018-1FF3-6621-A96000000F55";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2024/scripts/rigging/Mutant_Tools/Icons/";
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
	rename -uid "27154000-0018-1FF3-6621-A96000000F56";
	addAttr -ci true -sn "nts" -ln "notes" -dt "string";
	setAttr ".isc" yes;
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2024/scripts/rigging/Mutant_Tools/Icons/Jaw.png";
	setAttr ".ctor" -type "string" "esteban.rodriguez";
	setAttr ".cdat" -type "string" "2022/03/25 12:07:54";
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
		"['unitConversion44', 'Jaw_Ctrl_tag', 'unitConversion50', 'JawMover_Grp', 'Jaw_Ctrl_MultDiv2', 'Jaw_Jnt', 'Jaw_Bnd', 'unitConversion48', 'unitConversion49', 'JawUpperLipPivot_Jnt_Offset_Grp', 'unitConversion43', 'JawUpperLipPivot_Jnt_parentConstraint1', 'JawGlobal_Loc', 'Jaw_Bnd_parentConstraint1', 'unitConversion54', 'JawUpperLipPivot_Bnd_parentConstraint1', 'unitConversion55', 'Jaw_Ctrl_MultDiv', 'JawUpperLipPivot_Bnd', 'remapValue48', 'Jaw_Ctrl_MultDiv1', 'JawUpperLipPivot_Jnt', 'remapValue50', 'unitConversion53', 'Jaw_Ctrl', 'Jaw_Ctrl_Grp', 'Jaw_Rig_Grp', 'unitConversion51', 'unitConversion56', 'Jaw_Ctrl_Offset_Grp', 'unitConversion45', 'unitConversion57', 'Jaw_Jnt_Fixer_Grp', 'unitConversion52', 'Jaw_Ctrl_Offset_Grp_parentConstraint1', 'JawGlobal_LocShape', 'Jaw_Ctrl_MultDiv3', 'Jaw_Jnt_Offset_Grp_parentConstraint1', 'JawLowerLip_Jnt', 'unitConversion47', 'remapValue52', 'remapValue53', 'Jaw_CtrlShape', 'remapValue46', 'remapValue54', 'unitConversion46', 'JawUpperLip_Jnt', 'Jaw_Jnt_Offset_Grp', 'remapValue51', 'JawGlobal_Loc_Offset_Grp', 'remapValue49', 'remapValue47']");
createNode joint -n "Jaw_Guide" -p "Jaw_Block";
	rename -uid "27154000-0018-1FF3-6621-A96000000F57";
	addAttr -ci true -sn "Helper" -ln "Helper" -min 0 -max 1 -en "Hide:Show" -at "enum";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2024/scripts/rigging/Mutant_Tools/Icons/";
	setAttr ".t" -type "double3" 0.039201081600744134 11.119226052295687 -0.5812015517374034 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr -cb on ".Helper" 1;
createNode nurbsCurve -n "Jaw_Guide_CtrlShape" -p "Jaw_Guide";
	rename -uid "27154000-0018-1FF3-6621-A96000000F58";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2024/scripts/rigging/Mutant_Tools/Icons/";
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
createNode nurbsCurve -n "Jaw_Guide_Ctrl_CtrlShape" -p "Jaw_Guide";
	rename -uid "27154000-0018-1FF3-6621-A96000000F59";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2024/scripts/rigging/Mutant_Tools/Icons/";
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
createNode nurbsCurve -n "Jaw_Guide_Ctrl_Ctrl_CtrlShape" -p "Jaw_Guide";
	rename -uid "27154000-0018-1FF3-6621-A96000000F5A";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2024/scripts/rigging/Mutant_Tools/Icons/";
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
createNode nurbsCurve -n "Jaw_Guide_Ctrl_Ctrl_Ctrl_CtrlShape" -p "Jaw_Guide";
	rename -uid "27154000-0018-1FF3-6621-A96000000F5B";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2024/scripts/rigging/Mutant_Tools/Icons/";
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
createNode joint -n "JawUpperLip_Guide" -p "Jaw_Guide";
	rename -uid "27154000-0018-1FF3-6621-A96000000F5C";
	addAttr -ci true -sn "Helper" -ln "Helper" -min 0 -max 1 -en "Hide:Show" -at "enum";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2024/scripts/rigging/Mutant_Tools/Icons/";
	setAttr ".t" -type "double3" 0.085450319672127836 -2.8480544636013292 12.092000098562607 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr -cb on ".Helper" 1;
createNode nurbsCurve -n "JawUpperLip_Guide_CtrlShape" -p "JawUpperLip_Guide";
	rename -uid "27154000-0018-1FF3-6621-A96000000F5D";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2024/scripts/rigging/Mutant_Tools/Icons/";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 14;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 9 0 no 3
		10 0 1 2 3 4 5 6 7 8 9
		10
		7.3741535450110648e-06 -0.26379034380785504 0.13189517190392752
		7.3741535450110648e-06 0.49863286286692382 0.13501633925186202
		7.3741535450110648e-06 0.39022663833702281 0.26718954617816315
		7.3741535450110648e-06 0.52239984526332395 0.49547793035498167
		7.2798221180653784e-06 1.2130673301961774 2.0440058580295461e-07
		7.3741535450110648e-06 0.52240037284401175 -0.49547793035498167
		7.3741535450110648e-06 0.39022663833702281 -0.26718901859747529
		3.7814134752580966e-06 0.49863286286692382 -0.13359450929873765
		7.3741535450110648e-06 -0.26379034380785504 -0.13189517190392752
		7.3741535450110648e-06 -0.26379034380785504 0.13189517190392752
		;
createNode nurbsCurve -n "JawUpperLip_Guide_Ctrl_CtrlShape" -p "JawUpperLip_Guide";
	rename -uid "27154000-0018-1FF3-6621-A96000000F5E";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2024/scripts/rigging/Mutant_Tools/Icons/";
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
		0 0.31349319280744348 0
		-1.6223686482939466e-09 0.30873072194033652 0.054437358090251804
		-3.1954348813302043e-09 0.29458733886673449 0.10722127830551605
		-4.6714157162314197e-09 0.27149354942773213 0.15674686019406553
		-6.0054509671296288e-09 0.24014998077648272 0.20150997121550815
		-7.157001333988439e-09 0.20150944363482048 0.24014998077648272
		-8.0911356994808148e-09 0.15674686019406553 0.27149354942773213
		-8.779417464544269e-09 0.10722127830551605 0.29458733886673449
		-9.2009016758804581e-09 0.054437358090251804 0.30873072194033652
		-9.3428208808490835e-09 0 0.31349372038813106
		-9.2009016758804581e-09 -0.054437358090251804 0.30873072194033652
		-8.779417464544269e-09 -0.10722127830551605 0.29458733886673449
		-8.0911356994808148e-09 -0.15674686019406553 0.27149354942773213
		-7.157001333988439e-09 -0.20150944363482048 0.24014998077648272
		-6.0054509671296288e-09 -0.24014998077648272 0.20150997121550815
		-4.6714157162314197e-09 -0.27149354942773213 0.15674686019406553
		-3.1954348813302043e-09 -0.29458733886673449 0.10722127830551605
		-1.6223686482939466e-09 -0.30873072194033652 0.054437358090251804
		0 -0.31349319280744348 0
		0 -0.30873072194033652 -0.054437358090251804
		0 -0.29458733886673449 -0.10722127830551605
		0 -0.27149354942773213 -0.15674686019406553
		0 -0.24014998077648272 -0.20150997121550815
		0 -0.20150944363482048 -0.24014998077648272
		0 -0.15674686019406553 -0.27149354942773213
		0 -0.10722127830551605 -0.29458786644742208
		0 -0.054437358090251804 -0.30873072194033652
		0 0 -0.31349372038813106
		0 0.054437358090251804 -0.30873072194033652
		0 0.10722127830551605 -0.29458786644742208
		0 0.15674686019406553 -0.27149354942773213
		0 0.20150944363482048 -0.24014998077648272
		0 0.24014998077648272 -0.20150997121550815
		0 0.27149354942773213 -0.15674686019406553
		0 0.29458733886673449 -0.10722127830551605
		0 0.30873072194033652 -0.054437358090251804
		0 0.31349319280744348 0
		0.054437358090251804 0.30873072194033652 0
		0.10722127830551605 0.29458733886673449 0
		0.15674686019406553 0.27149354942773213 0
		0.20150997121550815 0.24014998077648272 0
		0.24014998077648272 0.20150944363482048 0
		0.27149354942773213 0.15674686019406553 0
		0.29458733886673449 0.10722127830551605 0
		0.30873072194033652 0.054437358090251804 0
		0.31349319280744348 0 0
		0.30873072194033652 -0.054437358090251804 0
		0.29458733886673449 -0.10722127830551605 0
		0.27149354942773213 -0.15674686019406553 0
		0.24014998077648272 -0.20150944363482048 0
		0.20150997121550815 -0.24014998077648272 0
		0.15674686019406553 -0.27149354942773213 0
		0.10722127830551605 -0.29458733886673449 0
		0.054437358090251804 -0.30873072194033652 0
		0 -0.31349319280744348 0
		-0.054437358090251804 -0.30873072194033652 0
		-0.10722127830551605 -0.29458733886673449 0
		-0.15674686019406553 -0.27149354942773213 0
		-0.20150997121550815 -0.24014998077648272 0
		-0.24014998077648272 -0.20150944363482048 0
		-0.27149354942773213 -0.15674686019406553 0
		-0.29458733886673449 -0.10722127830551605 0
		-0.30873072194033652 -0.054437358090251804 0
		-0.31349372038813106 0 0
		-0.30873072194033652 0.054437358090251804 0
		-0.29458733886673449 0.10722127830551605 0
		-0.27149354942773213 0.15674686019406553 0
		-0.24014998077648272 0.20150944363482048 0
		-0.20150997121550815 0.24014998077648272 0
		-0.15674686019406553 0.27149354942773213 0
		-0.10722127830551605 0.29458733886673449 0
		-0.054437358090251804 0.30873072194033652 0
		0 0.31349319280744348 0
		-1.6223686482939466e-09 0.30873072194033652 0.054437358090251804
		-3.1954348813302043e-09 0.29458733886673449 0.10722127830551605
		-4.6714157162314197e-09 0.27149354942773213 0.15674686019406553
		-6.0054509671296288e-09 0.24014998077648272 0.20150997121550815
		-7.157001333988439e-09 0.20150944363482048 0.24014998077648272
		-8.0911356994808148e-09 0.15674686019406553 0.27149354942773213
		-8.779417464544269e-09 0.10722127830551605 0.29458733886673449
		-9.2009016758804581e-09 0.054437358090251804 0.30873072194033652
		-9.3428208808490835e-09 0 0.31349372038813106
		-0.096874893440684243 0 0.29815009125020336
		-0.18426705160216375 0 0.25362175363474992
		-0.25362175363474992 0 0.18426705160216375
		-0.29815009125020336 0 0.096874893440684243
		-0.31349372038813106 0 0
		-0.29815009125020336 0 -0.096874893440684243
		-0.25362175363474992 0 -0.18426705160216375
		-0.18426705160216375 0 -0.25362175363474992
		-0.096874893440684243 0 -0.29815009125020336
		0 0 -0.31349372038813106
		0.096874893440684243 0 -0.29815009125020336
		0.18426705160216375 0 -0.25362175363474992
		0.25362175363474992 0 -0.18426705160216375
		0.29815009125020336 0 -0.096874893440684243
		0.31349319280744348 0 0
		0.29815009125020336 0 0.096874893440684243
		0.25362175363474992 0 0.18426705160216375
		0.18426705160216375 0 0.25362175363474992
		0.096874893440684243 0 0.29815009125020336
		-9.3428208808490835e-09 0 0.31349372038813106
		;
createNode nurbsCurve -n "JawUpperLip_Guide_Ctrl_Ctrl_CtrlShape" -p "JawUpperLip_Guide";
	rename -uid "27154000-0018-1FF3-6621-A96000000F5F";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2024/scripts/rigging/Mutant_Tools/Icons/";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 13;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 9 0 no 3
		10 0 1 2 3 4 5 6 7 8 9
		10
		-0.26379034380785499 -0.13189517190392763 -7.3741535450696413e-06
		0.49863286286692382 -0.13501633925186193 -7.3741535449003483e-06
		0.39022663833702281 -0.2671895461781631 -7.3741535449244184e-06
		0.52239984526332406 -0.49547793035498144 -7.3741535448950679e-06
		1.2130673301961774 -2.044005855335994e-07 -7.2798221177960236e-06
		0.52240037284401153 0.49547793035498178 -7.3741535448950679e-06
		0.3902266383370227 0.26718901859747535 -7.3741535449244184e-06
		0.49863286286692382 0.13359450929873778 -3.7814134751473776e-06
		-0.26379034380785504 0.13189517190392741 -7.3741535450696413e-06
		-0.26379034380785499 -0.13189517190392763 -7.3741535450696413e-06
		;
createNode nurbsCurve -n "JawUpperLip_Guide_Ctrl_Ctrl_Ctrl_CtrlShape" -p "JawUpperLip_Guide";
	rename -uid "27154000-0018-1FF3-6621-A96000000F60";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2024/scripts/rigging/Mutant_Tools/Icons/";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 6;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 9 0 no 3
		10 0 1 2 3 4 5 6 7 8 9
		10
		0.13189517190392763 7.374153544981782e-06 -0.26379034380785499
		0.13501633925186193 7.3741535449810874e-06 0.49863286286692382
		0.2671895461781631 7.3741535449517369e-06 0.39022663833702281
		0.49547793035498144 7.3741535449010411e-06 0.52239984526332406
		2.0440058553360101e-07 7.2798221180653784e-06 1.2130673301961774
		-0.49547793035498178 7.3741535451210842e-06 0.52240037284401153
		-0.26718901859747535 7.3741535450703927e-06 0.3902266383370227
		-0.13359450929873778 3.7814134752877597e-06 0.49863286286692382
		-0.13189517190392741 7.3741535450403493e-06 -0.26379034380785504
		0.13189517190392763 7.374153544981782e-06 -0.26379034380785499
		;
createNode joint -n "JawLowerLip_Guide" -p "Jaw_Guide";
	rename -uid "27154000-0018-1FF3-6621-A96000000F61";
	addAttr -ci true -sn "Helper" -ln "Helper" -min 0 -max 1 -en "Hide:Show" -at "enum";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2024/scripts/rigging/Mutant_Tools/Icons/";
	setAttr ".t" -type "double3" -0.0060002275818890616 -3.5802060931956703 11.757904200419969 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr -cb on ".Helper" 1;
createNode nurbsCurve -n "JawLowerLip_Guide_CtrlShape" -p "JawLowerLip_Guide";
	rename -uid "27154000-0018-1FF3-6621-A96000000F62";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2024/scripts/rigging/Mutant_Tools/Icons/";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 14;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 9 0 no 3
		10 0 1 2 3 4 5 6 7 8 9
		10
		7.3741535450110648e-06 -0.26379034380785504 0.13189517190392752
		7.3741535450110648e-06 0.49863286286692382 0.13501633925186202
		7.3741535450110648e-06 0.39022663833702281 0.26718954617816315
		7.3741535450110648e-06 0.52239984526332395 0.49547793035498167
		7.2798221180653784e-06 1.2130673301961774 2.0440058580295461e-07
		7.3741535450110648e-06 0.52240037284401175 -0.49547793035498167
		7.3741535450110648e-06 0.39022663833702281 -0.26718901859747529
		3.7814134752580966e-06 0.49863286286692382 -0.13359450929873765
		7.3741535450110648e-06 -0.26379034380785504 -0.13189517190392752
		7.3741535450110648e-06 -0.26379034380785504 0.13189517190392752
		;
createNode nurbsCurve -n "JawLowerLip_Guide_Ctrl_CtrlShape" -p "JawLowerLip_Guide";
	rename -uid "27154000-0018-1FF3-6621-A96000000F63";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2024/scripts/rigging/Mutant_Tools/Icons/";
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
		0 0.31349319280744348 0
		-1.6223686482939466e-09 0.30873072194033652 0.054437358090251804
		-3.1954348813302043e-09 0.29458733886673449 0.10722127830551605
		-4.6714157162314197e-09 0.27149354942773213 0.15674686019406553
		-6.0054509671296288e-09 0.24014998077648272 0.20150997121550815
		-7.157001333988439e-09 0.20150944363482048 0.24014998077648272
		-8.0911356994808148e-09 0.15674686019406553 0.27149354942773213
		-8.779417464544269e-09 0.10722127830551605 0.29458733886673449
		-9.2009016758804581e-09 0.054437358090251804 0.30873072194033652
		-9.3428208808490835e-09 0 0.31349372038813106
		-9.2009016758804581e-09 -0.054437358090251804 0.30873072194033652
		-8.779417464544269e-09 -0.10722127830551605 0.29458733886673449
		-8.0911356994808148e-09 -0.15674686019406553 0.27149354942773213
		-7.157001333988439e-09 -0.20150944363482048 0.24014998077648272
		-6.0054509671296288e-09 -0.24014998077648272 0.20150997121550815
		-4.6714157162314197e-09 -0.27149354942773213 0.15674686019406553
		-3.1954348813302043e-09 -0.29458733886673449 0.10722127830551605
		-1.6223686482939466e-09 -0.30873072194033652 0.054437358090251804
		0 -0.31349319280744348 0
		0 -0.30873072194033652 -0.054437358090251804
		0 -0.29458733886673449 -0.10722127830551605
		0 -0.27149354942773213 -0.15674686019406553
		0 -0.24014998077648272 -0.20150997121550815
		0 -0.20150944363482048 -0.24014998077648272
		0 -0.15674686019406553 -0.27149354942773213
		0 -0.10722127830551605 -0.29458786644742208
		0 -0.054437358090251804 -0.30873072194033652
		0 0 -0.31349372038813106
		0 0.054437358090251804 -0.30873072194033652
		0 0.10722127830551605 -0.29458786644742208
		0 0.15674686019406553 -0.27149354942773213
		0 0.20150944363482048 -0.24014998077648272
		0 0.24014998077648272 -0.20150997121550815
		0 0.27149354942773213 -0.15674686019406553
		0 0.29458733886673449 -0.10722127830551605
		0 0.30873072194033652 -0.054437358090251804
		0 0.31349319280744348 0
		0.054437358090251804 0.30873072194033652 0
		0.10722127830551605 0.29458733886673449 0
		0.15674686019406553 0.27149354942773213 0
		0.20150997121550815 0.24014998077648272 0
		0.24014998077648272 0.20150944363482048 0
		0.27149354942773213 0.15674686019406553 0
		0.29458733886673449 0.10722127830551605 0
		0.30873072194033652 0.054437358090251804 0
		0.31349319280744348 0 0
		0.30873072194033652 -0.054437358090251804 0
		0.29458733886673449 -0.10722127830551605 0
		0.27149354942773213 -0.15674686019406553 0
		0.24014998077648272 -0.20150944363482048 0
		0.20150997121550815 -0.24014998077648272 0
		0.15674686019406553 -0.27149354942773213 0
		0.10722127830551605 -0.29458733886673449 0
		0.054437358090251804 -0.30873072194033652 0
		0 -0.31349319280744348 0
		-0.054437358090251804 -0.30873072194033652 0
		-0.10722127830551605 -0.29458733886673449 0
		-0.15674686019406553 -0.27149354942773213 0
		-0.20150997121550815 -0.24014998077648272 0
		-0.24014998077648272 -0.20150944363482048 0
		-0.27149354942773213 -0.15674686019406553 0
		-0.29458733886673449 -0.10722127830551605 0
		-0.30873072194033652 -0.054437358090251804 0
		-0.31349372038813106 0 0
		-0.30873072194033652 0.054437358090251804 0
		-0.29458733886673449 0.10722127830551605 0
		-0.27149354942773213 0.15674686019406553 0
		-0.24014998077648272 0.20150944363482048 0
		-0.20150997121550815 0.24014998077648272 0
		-0.15674686019406553 0.27149354942773213 0
		-0.10722127830551605 0.29458733886673449 0
		-0.054437358090251804 0.30873072194033652 0
		0 0.31349319280744348 0
		-1.6223686482939466e-09 0.30873072194033652 0.054437358090251804
		-3.1954348813302043e-09 0.29458733886673449 0.10722127830551605
		-4.6714157162314197e-09 0.27149354942773213 0.15674686019406553
		-6.0054509671296288e-09 0.24014998077648272 0.20150997121550815
		-7.157001333988439e-09 0.20150944363482048 0.24014998077648272
		-8.0911356994808148e-09 0.15674686019406553 0.27149354942773213
		-8.779417464544269e-09 0.10722127830551605 0.29458733886673449
		-9.2009016758804581e-09 0.054437358090251804 0.30873072194033652
		-9.3428208808490835e-09 0 0.31349372038813106
		-0.096874893440684243 0 0.29815009125020336
		-0.18426705160216375 0 0.25362175363474992
		-0.25362175363474992 0 0.18426705160216375
		-0.29815009125020336 0 0.096874893440684243
		-0.31349372038813106 0 0
		-0.29815009125020336 0 -0.096874893440684243
		-0.25362175363474992 0 -0.18426705160216375
		-0.18426705160216375 0 -0.25362175363474992
		-0.096874893440684243 0 -0.29815009125020336
		0 0 -0.31349372038813106
		0.096874893440684243 0 -0.29815009125020336
		0.18426705160216375 0 -0.25362175363474992
		0.25362175363474992 0 -0.18426705160216375
		0.29815009125020336 0 -0.096874893440684243
		0.31349319280744348 0 0
		0.29815009125020336 0 0.096874893440684243
		0.25362175363474992 0 0.18426705160216375
		0.18426705160216375 0 0.25362175363474992
		0.096874893440684243 0 0.29815009125020336
		-9.3428208808490835e-09 0 0.31349372038813106
		;
createNode nurbsCurve -n "JawLowerLip_Guide_Ctrl_Ctrl_CtrlShape" -p "JawLowerLip_Guide";
	rename -uid "27154000-0018-1FF3-6621-A96000000F64";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2024/scripts/rigging/Mutant_Tools/Icons/";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 13;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 9 0 no 3
		10 0 1 2 3 4 5 6 7 8 9
		10
		-0.26379034380785499 -0.13189517190392763 -7.3741535450696413e-06
		0.49863286286692382 -0.13501633925186193 -7.3741535449003483e-06
		0.39022663833702281 -0.2671895461781631 -7.3741535449244184e-06
		0.52239984526332406 -0.49547793035498144 -7.3741535448950679e-06
		1.2130673301961774 -2.044005855335994e-07 -7.2798221177960236e-06
		0.52240037284401153 0.49547793035498178 -7.3741535448950679e-06
		0.3902266383370227 0.26718901859747535 -7.3741535449244184e-06
		0.49863286286692382 0.13359450929873778 -3.7814134751473776e-06
		-0.26379034380785504 0.13189517190392741 -7.3741535450696413e-06
		-0.26379034380785499 -0.13189517190392763 -7.3741535450696413e-06
		;
createNode nurbsCurve -n "JawLowerLip_Guide_Ctrl_Ctrl_Ctrl_CtrlShape" -p "JawLowerLip_Guide";
	rename -uid "27154000-0018-1FF3-6621-A96000000F65";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2024/scripts/rigging/Mutant_Tools/Icons/";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 6;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 9 0 no 3
		10 0 1 2 3 4 5 6 7 8 9
		10
		0.13189517190392763 7.374153544981782e-06 -0.26379034380785499
		0.13501633925186193 7.3741535449810874e-06 0.49863286286692382
		0.2671895461781631 7.3741535449517369e-06 0.39022663833702281
		0.49547793035498144 7.3741535449010411e-06 0.52239984526332406
		2.0440058553360101e-07 7.2798221180653784e-06 1.2130673301961774
		-0.49547793035498178 7.3741535451210842e-06 0.52240037284401153
		-0.26718901859747535 7.3741535450703927e-06 0.3902266383370227
		-0.13359450929873778 3.7814134752877597e-06 0.49863286286692382
		-0.13189517190392741 7.3741535450403493e-06 -0.26379034380785504
		0.13189517190392763 7.374153544981782e-06 -0.26379034380785499
		;
createNode dagContainer -n "Commissures_Block" -p "face";
	rename -uid "27154000-0018-1FF3-6621-A96000000F66";
	addAttr -ci true -sn "nts" -ln "notes" -dt "string";
	setAttr ".isc" yes;
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2024/scripts/rigging/Mutant_Tools/Icons/Commissures.png";
	setAttr ".ctor" -type "string" "info";
	setAttr ".cdat" -type "string" "2022/09/09 09:19:29";
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
		"['L_Commissures_Up_Bnd_scaleConstraint1', 'L_Commissures_Narrow_Crv|curveShape40', 'unitConversion59', 'L_Commissures_Up_Crv|curveShape584', 'L_Commissures_Wide_Guide|curveShape348', 'R_Commissures_Wide_Bnd', 'L_Commissures_Down_Guide|curveShape664', 'R_Commissures_Down_Crv', 'R_Commissures_Wide_Bnd_parentConstraint1', 'L_Commissures_Down_Bnd', 'L_Commissures_Narrow_Jnt', 'L_Commissures_Narrow_Bnd_parentConstraint1', 'L_Lips_Main_Ctrl_MultDiv7', 'R_Commissures_Narrow_Jnt', 'L_Commissures_Wide_POCI', 'L_Commissures_Wide_Crv|curveShape348', 'L_Commissures_Wide_Bnd_scaleConstraint1', 'L_Commissures_Narrow_Guide|curveShape40', 'R_Commissures_Down_Crv|curveShape664', 'R_Commissures_Narrow_Bnd_parentConstraint1', 'R_Commissures_Up_Bnd_parentConstraint1', 'L_Commissures_Down_Bnd_scaleConstraint1', 'L_Commissures_Up_Jnt', 'R_Commissures_Grp', 'L_Commissures_Down_Crv', 'L_Commissures_Up_Crv', 'R_Commissures_Up_Crv', 'L_Commissures_Wide_Crv', 'Commissures_Rig_Grp', 'R_Commissures_Down_POCI', 'L_Commissures_Up_Guide|curveShape584', 'L_Commissures_Wide_Bnd', 'R_Commissures_Down_Jnt', 'R_Commissures_Up_Bnd', 'R_Commissures_Up_Crv|curveShape584', 'L_Lips_Main_Ctrl_MultDiv8', 'L_Commissures_Wide_Jnt_RemapValue', 'R_Commissures_Wide_Crv|curveShape348', 'L_Commissures_Narrow_Bnd_scaleConstraint1', 'R_Commissures_Wide_Jnt_RemapValue', 'R_Commissures_Down_Bnd', 'L_Commissures_Wide_Bnd_parentConstraint1', 'L_Lips_Main_Ctrl_MultDiv6', 'L_Commissures_Up_POCI', 'L_Commissures_Narrow_Crv', 'R_Commissures_Narrow_Crv|curveShape40', 'unitConversion60', 'L_Commissures_Down_Bnd_parentConstraint1', 'L_Commissures_Narrow_POCI', 'L_Commissures_Narrow_Jnt_RemapValue', 'R_Commissures_Down_Bnd_parentConstraint1', 'unitConversion61', 'R_Commissures_Narrow_Bnd_scaleConstraint1', 'L_Lips_Main_Ctrl_MultDiv9', 'R_Lips_Main_Ctrl_MultDiv9', 'L_Commissures_Down_Jnt', 'L_Commissures_Grp', 'R_Commissures_Wide_Bnd_scaleConstraint1', 'L_Commissures_Down_Crv|curveShape664', 'R_Commissures_Up_POCI', 'R_Commissures_Narrow_POCI', 'R_Lips_Main_Ctrl_MultDiv8', 'R_Commissures_Narrow_Jnt_RemapValue', 'unitConversion58', 'R_Commissures_Up_Jnt', 'R_Commissures_Wide_POCI', 'R_Commissures_Wide_Jnt', 'R_Commissures_Up_Bnd_scaleConstraint1', 'L_Commissures_Up_Bnd_parentConstraint1', 'R_Commissures_Down_Bnd_scaleConstraint1', 'R_Commissures_Narrow_Bnd', 'R_Commissures_GrpMirror_Grp', 'L_Commissures_Up_Bnd', 'R_Commissures_Wide_Crv', 'L_Commissures_Down_POCI', 'R_Lips_Main_Ctrl_MultDiv7', 'R_Lips_Main_Ctrl_MultDiv6', 'L_Commissures_Narrow_Bnd', 'R_Commissures_Narrow_Crv', 'L_Commissures_Wide_Jnt']");
createNode transform -n "L_Commissures_Wide_Guide" -p "Commissures_Block";
	rename -uid "27154000-0018-1FF3-6621-A96000000F67";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2024/scripts/rigging/Mutant_Tools/Icons/";
	setAttr ".ove" yes;
	setAttr ".ovc" 9;
	setAttr ".t" -type "double3" 4.3528015489147283 155.99626796536145 10.170719558662768 ;
	setAttr ".r" -type "double3" 0.27799366802132536 38.548486404048994 -0.04886969939569942 ;
	setAttr ".s" -type "double3" 1.1529266464857248 1.1529266464857248 1.1529266464857248 ;
	setAttr ".rp" -type "double3" 0 -148.19816716577168 0 ;
	setAttr ".rpt" -type "double3" -0.57449138787287657 0.0021804602141158279 -0.56234802877879686 ;
	setAttr ".sp" -type "double3" 0 -148.19816716577168 0 ;
createNode nurbsCurve -n "curveShape348" -p "L_Commissures_Wide_Guide";
	rename -uid "27154000-0018-1FF3-6621-A96000000F68";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2024/scripts/rigging/Mutant_Tools/Icons/";
	setAttr -k off ".v";
	setAttr ".cc" -type "nurbsCurve" 
		3 2 0 no 3
		7 0 0 0 1 2 2 2
		5
		0 -148.19816716577185 8.9937608104032269e-16
		0.67086847775077962 -148.19816716577185 8.9937608104032269e-16
		2.0126074458597825 -148.19816716577185 8.9937608104032269e-16
		3.3543464139687882 -148.19816716577185 8.9937608104032269e-16
		4.0252148917195649 -148.19816716577185 8.9937608104032269e-16
		;
createNode transform -n "L_Commissures_Up_Guide" -p "Commissures_Block";
	rename -uid "27154000-0018-1FF3-6621-A96000000F69";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2024/scripts/rigging/Mutant_Tools/Icons/";
	setAttr ".ove" yes;
	setAttr ".ovc" 18;
	setAttr ".t" -type "double3" 4.3528015489147283 155.99626796536145 10.170719558662768 ;
	setAttr ".r" -type "double3" 0.27799366802132536 38.548486404048994 -0.04886969939569942 ;
	setAttr ".s" -type "double3" 1.1529266464857248 1.1529266464857248 1.1529266464857248 ;
	setAttr ".rp" -type "double3" 0 -148.19816716577168 0 ;
	setAttr ".rpt" -type "double3" -0.57449138787287657 0.0021804602141158279 -0.56234802877879686 ;
	setAttr ".sp" -type "double3" 0 -148.19816716577168 0 ;
createNode nurbsCurve -n "curveShape584" -p "L_Commissures_Up_Guide";
	rename -uid "27154000-0018-1FF3-6621-A96000000F6A";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2024/scripts/rigging/Mutant_Tools/Icons/";
	setAttr -k off ".v";
	setAttr ".cc" -type "nurbsCurve" 
		3 2 0 no 3
		7 0 0 0 1 2 2 2
		5
		0 -148.19816716577182 4.8841117854278297e-16
		0 -147.68153364893175 4.8841117854278297e-16
		0 -146.6482650653497 4.8841117854278297e-16
		0 -145.61499648176732 4.8841117854278297e-16
		0 -145.09836296492742 4.8841117854278297e-16
		;
createNode transform -n "L_Commissures_Narrow_Guide" -p "Commissures_Block";
	rename -uid "27154000-0018-1FF3-6621-A96000000F6B";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2024/scripts/rigging/Mutant_Tools/Icons/";
	setAttr ".ove" yes;
	setAttr ".ovc" 14;
	setAttr ".t" -type "double3" 4.3528015489147283 155.99626796536145 10.170719558662768 ;
	setAttr ".r" -type "double3" 0.27799366802132536 38.548486404048994 -0.04886969939569942 ;
	setAttr ".s" -type "double3" 1.1529266464857248 1.1529266464857248 1.1529266464857248 ;
	setAttr ".rp" -type "double3" 0 -148.19816716577168 0 ;
	setAttr ".rpt" -type "double3" -0.57449138787287657 0.0021804602141158279 -0.56234802877879686 ;
	setAttr ".sp" -type "double3" 0 -148.19816716577168 0 ;
createNode nurbsCurve -n "curveShape40" -p "L_Commissures_Narrow_Guide";
	rename -uid "27154000-0018-1FF3-6621-A96000000F6C";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2024/scripts/rigging/Mutant_Tools/Icons/";
	setAttr -k off ".v";
	setAttr ".cc" -type "nurbsCurve" 
		3 2 0 no 3
		7 0 0 0 1 2 2 2
		5
		0 -148.19816716577182 4.5357014706307082e-16
		-0.50355769188344024 -148.19816716577182 4.5357014706307082e-16
		-1.5106745863249067 -148.19816716577182 4.5357014706307082e-16
		-2.5177914807663737 -148.19816716577182 4.5357014706307082e-16
		-3.0213491726498134 -148.19816716577182 4.5357014706307082e-16
		;
createNode transform -n "L_Commissures_Down_Guide" -p "Commissures_Block";
	rename -uid "27154000-0018-1FF3-6621-A96000000F6D";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2024/scripts/rigging/Mutant_Tools/Icons/";
	setAttr ".ove" yes;
	setAttr ".ovc" 17;
	setAttr ".t" -type "double3" 4.3528015489147283 155.99626796536145 10.170719558662768 ;
	setAttr ".r" -type "double3" 0.27799366802132536 38.548486404048994 -0.04886969939569942 ;
	setAttr ".s" -type "double3" 1.1529266464857248 1.1529266464857248 1.1529266464857248 ;
	setAttr ".rp" -type "double3" 0 -148.19816716577168 0 ;
	setAttr ".rpt" -type "double3" -0.57449138787287657 0.0021804602141158279 -0.56234802877879686 ;
	setAttr ".sp" -type "double3" 0 -148.19816716577168 0 ;
createNode nurbsCurve -n "curveShape664" -p "L_Commissures_Down_Guide";
	rename -uid "27154000-0018-1FF3-6621-A96000000F6E";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2024/scripts/rigging/Mutant_Tools/Icons/";
	setAttr -k off ".v";
	setAttr ".cc" -type "nurbsCurve" 
		3 2 0 no 3
		7 0 0 0 1 2 2 2
		5
		0 -148.19816716577182 1.0322161387165071e-15
		0 -148.9188904631886 1.0322161387165071e-15
		0 -150.36033922019402 1.0322161387165071e-15
		0 -151.80178797719964 1.0322161387165071e-15
		0 -152.52251127461653 1.0322161387165071e-15
		;
createNode dagContainer -n "Tongue_Block" -p "face";
	rename -uid "27154000-0018-1FF3-6621-A96000000F6F";
	addAttr -ci true -sn "nts" -ln "notes" -dt "string";
	setAttr ".isc" yes;
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2024/scripts/rigging/Mutant_Tools/Icons/Tongue.png";
	setAttr ".ctor" -type "string" "esteban.rodriguez";
	setAttr ".cdat" -type "string" "2022/04/26 10:37:03";
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
		"['Tongue_03_Ctrl_Offset_Grp', 'Tongue_03_Bnd', 'Tongue_04_Ctrl', 'Tongue_01_Ctrl_Auto_Grp', 'Tongue_02_Jnt_parentConstraint1', 'Tongue_04_Jnt_scaleConstraint1', 'Tongue_04_Jnt', 'Tongue_02_Jnt', 'Tongue_02_CtrlShape', 'Tongue_04_CtrlShape', 'Tongue_Main_CtrlShape', 'Tongue_01_Jnt_scaleConstraint1', 'Tongue_02_Ctrl_Offset_Grp', 'Tongue_04_Bnd', 'Tongue_03_Jnt_Ctrl_tag', 'Tongue_01_CtrlShape', 'Tongue_03_Ctrl_Root_Grp', 'Tongue_Rig_Grp', 'Tongue_04_Ctrl_Auto_Grp', 'Tongue_Ctrl_Grp_parentConstraint1', 'Tongue_03_Ctrl_Auto_Grp', 'Tongue_03_Jnt_scaleConstraint1', 'Tongue_01_Jnt', 'Tongue_02_Ctrl_Root_Grp', 'Tongue_03_Jnt', 'Tongue_02_Bnd', 'Tongue_04_Bnd_parentConstraint1', 'Tongue_04_Bnd_scaleConstraint1', 'Tongue_04_Jnt_parentConstraint1', 'Tongue_01_Ctrl_Offset_Grp', 'Tongue_05_Jnt', 'Tongue_01_Jnt_Ctrl_tag', 'Tongue_04_Ctrl_Root_Grp', 'Tongue_Main_Ctrl_Offset_Grp', 'Tongue_03_Jnt_parentConstraint1', 'Tongue_02_Ctrl', 'Tongue_03_Bnd_scaleConstraint1', 'Tongue_03_Ctrl', 'Tongue_02_Ctrl_Auto_Grp', 'Tongue_Main_Ctrl', 'Tongue_04_Jnt_Ctrl_tag', 'Tongue_02_Jnt_scaleConstraint1', 'Tongue_01_Ctrl', 'Tongue_02_Bnd_scaleConstraint1', 'Tongue_01_Ctrl_Root_Grp', 'Tongue_03_Bnd_parentConstraint1', 'Tongue_01_Bnd_parentConstraint1', 'Tongue_Ctrl_Grp', 'Tongue_01_Bnd', 'Tongue_01_Jnt_parentConstraint1', 'Tongue_01_Bnd_scaleConstraint1', 'Tongue_Main_Ctrl_tag', 'Tongue_02_Bnd_parentConstraint1', 'Tongue_02_Jnt_Ctrl_tag', 'Tongue_04_Ctrl_Offset_Grp', 'Tongue_03_CtrlShape']");
createNode joint -n "Tongue_01_Guide" -p "Tongue_Block";
	rename -uid "27154000-0018-1FF3-6621-A96000000F70";
	addAttr -ci true -sn "Helper" -ln "Helper" -min 0 -max 1 -en "Hide:Show" -at "enum";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2024/scripts/rigging/Mutant_Tools/Icons/";
	setAttr ".t" -type "double3" 0.05237771748270649 5.6720600908966503 2.9606401450076585 ;
	setAttr ".r" -type "double3" -38.426041494941096 0 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr -cb on ".Helper" 1;
createNode nurbsCurve -n "Tongue_01_Guide_CtrlShape" -p "Tongue_01_Guide";
	rename -uid "27154000-0018-1FF3-6621-A96000000F71";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2024/scripts/rigging/Mutant_Tools/Icons/";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 14;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 9 0 no 3
		10 0 1 2 3 4 5 6 7 8 9
		10
		6.8490734832988348e-06 -0.24500702865712942 0.12250351432856328
		6.8490734832988348e-06 0.46312747600348469 0.12540243749163441
		6.8490734832988348e-06 0.36244036753466524 0.24816418922840433
		6.8490734832988348e-06 0.48520211927143458 0.46019719194074316
		6.7614589698510471e-06 1.1266903020107943 1.8984614441342986e-07
		6.8490734832988348e-06 0.48520260928549203 -0.46019719194074676
		6.8490734832988348e-06 0.36244036753466524 -0.2481636992143503
		3.5121561552378916e-06 0.46312747600348469 -0.12408184960717623
		6.8490734832988348e-06 -0.24500702865712942 -0.12250351432856707
		6.8490734832988348e-06 -0.24500702865712942 0.12250351432856328
		;
createNode nurbsCurve -n "Tongue_01_Guide_Ctrl_CtrlShape" -p "Tongue_01_Guide";
	rename -uid "27154000-0018-1FF3-6621-A96000000F72";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2024/scripts/rigging/Mutant_Tools/Icons/";
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
		2.2117114679877868e-19 0.2911707629826501 -1.811834034575595e-15
		-1.5068471275664843e-09 0.28674740608727456 0.05056112047585553
		-2.967902441698123e-09 0.27361110923879378 0.099586536896090025
		-4.3387853690027915e-09 0.25216172390797659 0.14558562649835161
		-5.5778300141870532e-09 0.22304998876293644 0.18716135920523719
		-6.6473836970868897e-09 0.18716086919118261 0.22304998876293389
		-7.5150025869675186e-09 0.1455856264983541 0.25216172390797426
		-8.1542749261397061e-09 0.099586536896092759 0.27361110923879134
		-8.5457471565280636e-09 0.050561120475858243 0.28674740608727206
		-8.677560937945606e-09 9.0591701728779748e-16 0.2911712529967051
		-8.5457471565280636e-09 -0.050561120475856446 0.28674740608727206
		-8.1542749261397061e-09 -0.099586536896090927 0.27361110923879134
		-7.5150025869675186e-09 -0.14558562649835255 0.25216172390797426
		-6.6473836970868897e-09 -0.18716086919118091 0.22304998876293389
		-5.5778300141870532e-09 -0.22304998876293466 0.18716135920523719
		-4.3387853690027915e-09 -0.25216172390797503 0.14558562649835161
		-2.967902441698123e-09 -0.27361110923879212 0.099586536896090025
		-1.5068471275664843e-09 -0.28674740608727289 0.05056112047585553
		2.2117114679877868e-19 -0.29117076298264849 -1.811834034575595e-15
		2.2117114679877868e-19 -0.28674740608727289 -0.050561120475859166
		2.2117114679877868e-19 -0.27361110923879212 -0.099586536896093564
		2.2117114679877868e-19 -0.25216172390797503 -0.14558562649835516
		2.2117114679877868e-19 -0.22304998876293466 -0.18716135920524091
		2.2117114679877868e-19 -0.18716086919118091 -0.22304998876293733
		2.2117114679877868e-19 -0.14558562649835255 -0.25216172390797725
		2.2117114679877868e-19 -0.099586536896090927 -0.27361159925285183
		2.2117114679877868e-19 -0.050561120475856446 -0.28674740608727511
		2.2117114679877868e-19 9.0591701728779748e-16 -0.29117125299670821
		2.2117114679877868e-19 0.050561120475858243 -0.28674740608727511
		2.2117114679877868e-19 0.099586536896092759 -0.27361159925285183
		2.2117114679877868e-19 0.1455856264983541 -0.25216172390797725
		2.2117114679877868e-19 0.18716086919118261 -0.22304998876293733
		2.2117114679877868e-19 0.22304998876293644 -0.18716135920524091
		2.2117114679877868e-19 0.25216172390797659 -0.14558562649835516
		2.2117114679877868e-19 0.27361110923879378 -0.099586536896093564
		2.2117114679877868e-19 0.28674740608727456 -0.050561120475859166
		2.2117114679877868e-19 0.2911707629826501 -1.811834034575595e-15
		0.050561120475857355 0.28674740608727456 -1.811834034575595e-15
		0.099586536896091815 0.27361110923879378 -1.811834034575595e-15
		0.14558562649835338 0.25216172390797659 -1.811834034575595e-15
		0.1871613592052391 0.22304998876293644 -1.811834034575595e-15
		0.22304998876293558 0.18716086919118261 -1.811834034575595e-15
		0.25216172390797592 0.1455856264983541 -1.811834034575595e-15
		0.27361110923879289 0.099586536896092759 -1.811834034575595e-15
		0.28674740608727362 0.050561120475858243 -1.811834034575595e-15
		0.29117076298264943 9.0591701728779748e-16 -1.811834034575595e-15
		0.28674740608727362 -0.050561120475856446 -1.811834034575595e-15
		0.27361110923879289 -0.099586536896090927 -1.811834034575595e-15
		0.25216172390797592 -0.14558562649835255 -1.811834034575595e-15
		0.22304998876293558 -0.18716086919118091 -1.811834034575595e-15
		0.1871613592052391 -0.22304998876293466 -1.811834034575595e-15
		0.14558562649835338 -0.25216172390797503 -1.811834034575595e-15
		0.099586536896091815 -0.27361110923879212 -1.811834034575595e-15
		0.050561120475857355 -0.28674740608727289 -1.811834034575595e-15
		2.2117114679877868e-19 -0.29117076298264849 -1.811834034575595e-15
		-0.050561120475857355 -0.28674740608727289 -1.811834034575595e-15
		-0.099586536896091815 -0.27361110923879212 -1.811834034575595e-15
		-0.14558562649835338 -0.25216172390797503 -1.811834034575595e-15
		-0.1871613592052391 -0.22304998876293466 -1.811834034575595e-15
		-0.22304998876293558 -0.18716086919118091 -1.811834034575595e-15
		-0.25216172390797592 -0.14558562649835255 -1.811834034575595e-15
		-0.27361110923879289 -0.099586536896090927 -1.811834034575595e-15
		-0.28674740608727362 -0.050561120475856446 -1.811834034575595e-15
		-0.29117125299670676 9.0591701728779748e-16 -1.811834034575595e-15
		-0.28674740608727362 0.050561120475858243 -1.811834034575595e-15
		-0.27361110923879289 0.099586536896092759 -1.811834034575595e-15
		-0.25216172390797592 0.1455856264983541 -1.811834034575595e-15
		-0.22304998876293558 0.18716086919118261 -1.811834034575595e-15
		-0.1871613592052391 0.22304998876293644 -1.811834034575595e-15
		-0.14558562649835338 0.25216172390797659 -1.811834034575595e-15
		-0.099586536896091815 0.27361110923879378 -1.811834034575595e-15
		-0.050561120475857355 0.28674740608727456 -1.811834034575595e-15
		2.2117114679877868e-19 0.2911707629826501 -1.811834034575595e-15
		-1.5068471275664843e-09 0.28674740608727456 0.05056112047585553
		-2.967902441698123e-09 0.27361110923879378 0.099586536896090025
		-4.3387853690027915e-09 0.25216172390797659 0.14558562649835161
		-5.5778300141870532e-09 0.22304998876293644 0.18716135920523719
		-6.6473836970868897e-09 0.18716086919118261 0.22304998876293389
		-7.5150025869675186e-09 0.1455856264983541 0.25216172390797426
		-8.1542749261397061e-09 0.099586536896092759 0.27361110923879134
		-8.5457471565280636e-09 0.050561120475858243 0.28674740608727206
		-8.677560937945606e-09 9.0591701728779748e-16 0.2911712529967051
		-0.0899768712181018 9.0591701728779748e-16 0.27692017416783454
		-0.17114622977003721 9.0591701728779748e-16 0.23556249771645349
		-0.23556249771645515 9.0591701728779748e-16 0.17114622977003527
		-0.27692017416783599 9.0591701728779748e-16 0.089976871218100093
		-0.29117125299670676 9.0591701728779748e-16 -1.811834034575595e-15
		-0.27692017416783599 9.0591701728779748e-16 -0.089976871218103605
		-0.23556249771645515 9.0591701728779748e-16 -0.17114622977003896
		-0.17114622977003721 9.0591701728779748e-16 -0.23556249771645671
		-0.0899768712181018 9.0591701728779748e-16 -0.2769201741678376
		2.2117114679877868e-19 9.0591701728779748e-16 -0.29117125299670821
		0.0899768712181018 9.0591701728779748e-16 -0.2769201741678376
		0.17114622977003721 9.0591701728779748e-16 -0.23556249771645671
		0.23556249771645515 9.0591701728779748e-16 -0.17114622977003896
		0.27692017416783599 9.0591701728779748e-16 -0.089976871218103605
		0.29117076298264943 9.0591701728779748e-16 -1.811834034575595e-15
		0.27692017416783599 9.0591701728779748e-16 0.089976871218100093
		0.23556249771645515 9.0591701728779748e-16 0.17114622977003527
		0.17114622977003721 9.0591701728779748e-16 0.23556249771645349
		0.0899768712181018 9.0591701728779748e-16 0.27692017416783454
		-8.677560937945606e-09 9.0591701728779748e-16 0.2911712529967051
		;
createNode nurbsCurve -n "Tongue_01_Guide_Ctrl_Ctrl_CtrlShape" -p "Tongue_01_Guide";
	rename -uid "27154000-0018-1FF3-6621-A96000000F73";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2024/scripts/rigging/Mutant_Tools/Icons/";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 13;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 9 0 no 3
		10 0 1 2 3 4 5 6 7 8 9
		10
		-0.24500702865713031 -0.12250351432856439 -6.84907348516485e-06
		0.46312747600348458 -0.12540243749163538 -6.8490734850076128e-06
		0.36244036753466469 -0.24816418922840505 -6.8490734850299702e-06
		0.48520211927143447 -0.46019719194074471 -6.849073485002711e-06
		1.1266903020107943 -1.8984614506917153e-07 -6.7614589714124821e-06
		0.4852026092854918 0.46019719194074543 -6.849073485002711e-06
		0.36244036753466463 0.24816369921434969 -6.8490734850299702e-06
		0.46312747600348453 0.12408184960717529 -3.5121561569466696e-06
		-0.24500702865713037 0.12250351432856599 -6.84907348516485e-06
		-0.24500702865713031 -0.12250351432856439 -6.84907348516485e-06
		;
createNode nurbsCurve -n "Tongue_01_Guide_Ctrl_Ctrl_Ctrl_CtrlShape" -p "Tongue_01_Guide";
	rename -uid "27154000-0018-1FF3-6621-A96000000F74";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2024/scripts/rigging/Mutant_Tools/Icons/";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 6;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 9 0 no 3
		10 0 1 2 3 4 5 6 7 8 9
		10
		0.12250351432856529 6.8490734841773316e-06 -0.24500702865713209
		0.12540243749163613 6.8490734841766861e-06 0.46312747600348264
		0.24816418922840591 6.8490734841494312e-06 0.36244036753466302
		0.46019719194074493 6.8490734841023463e-06 0.48520211927143292
		1.8984614597531113e-07 6.7614589707567439e-06 1.1266903020107937
		-0.46019719194074504 6.8490734843067167e-06 0.48520260928549036
		-0.24816369921434869 6.8490734842596369e-06 0.36244036753466297
		-0.12408184960717444 3.5121561561711398e-06 0.46312747600348253
		-0.1225035143285651 6.8490734842317323e-06 -0.24500702865713209
		0.12250351432856529 6.8490734841773316e-06 -0.24500702865713209
		;
createNode joint -n "Tongue_02_Guide" -p "Tongue_01_Guide";
	rename -uid "27154000-0018-1FF3-6621-A96000000F75";
	addAttr -ci true -sn "Helper" -ln "Helper" -min 0 -max 1 -en "Hide:Show" -at "enum";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2024/scripts/rigging/Mutant_Tools/Icons/";
	setAttr ".t" -type "double3" -8.1089073650231214e-10 1.1362732550423971e-06 1.9100913398932704 ;
	setAttr ".r" -type "double3" 9.4438379730435464 0 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr -cb on ".Helper" 1;
createNode nurbsCurve -n "Tongue_02_Guide_CtrlShape" -p "Tongue_02_Guide";
	rename -uid "27154000-0018-1FF3-6621-A96000000F76";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2024/scripts/rigging/Mutant_Tools/Icons/";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 14;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 9 0 no 3
		10 0 1 2 3 4 5 6 7 8 9
		10
		6.8490734832983909e-06 -0.24500702865713037 0.12250351432856518
		6.8490734832983909e-06 0.46312747600348453 0.12540243749163624
		6.8490734832983909e-06 0.36244036753466469 0.24816418922840597
		6.8490734832983909e-06 0.48520211927143436 0.46019719194074493
		6.7614589698505982e-06 1.1266903020107943 1.8984614622526398e-07
		6.8490734832983909e-06 0.48520260928549191 -0.46019719194074493
		6.8490734832983909e-06 0.36244036753466469 -0.24816369921434858
		3.5121561552374469e-06 0.46312747600348453 -0.12408184960717429
		6.8490734832983909e-06 -0.24500702865713037 -0.12250351432856518
		6.8490734832983909e-06 -0.24500702865713037 0.12250351432856518
		;
createNode nurbsCurve -n "Tongue_02_Guide_Ctrl_CtrlShape" -p "Tongue_02_Guide";
	rename -uid "27154000-0018-1FF3-6621-A96000000F77";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2024/scripts/rigging/Mutant_Tools/Icons/";
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
		-2.2117114679877868e-19 0.29117076298264943 0
		-1.5068471280088274e-09 0.28674740608727362 0.050561120475857355
		-2.967902442140464e-09 0.27361110923879289 0.099586536896091815
		-4.3387853694451346e-09 0.25216172390797592 0.14558562649835338
		-5.5778300146294021e-09 0.22304998876293558 0.1871613592052391
		-6.6473836975292402e-09 0.1871608691911818 0.22304998876293558
		-7.5150025874098716e-09 0.14558562649835338 0.25216172390797592
		-8.1542749265820509e-09 0.099586536896091815 0.27361110923879289
		-8.545747156970415e-09 0.050561120475857355 0.28674740608727362
		-8.6775609383879474e-09 0 0.29117125299670676
		-8.545747156970415e-09 -0.050561120475857355 0.28674740608727362
		-8.1542749265820509e-09 -0.099586536896091815 0.27361110923879289
		-7.5150025874098716e-09 -0.14558562649835338 0.25216172390797592
		-6.6473836975292402e-09 -0.1871608691911818 0.22304998876293558
		-5.5778300146294021e-09 -0.22304998876293558 0.1871613592052391
		-4.3387853694451346e-09 -0.25216172390797592 0.14558562649835338
		-2.967902442140464e-09 -0.27361110923879289 0.099586536896091815
		-1.5068471280088274e-09 -0.28674740608727362 0.050561120475857355
		-2.2117114679877868e-19 -0.29117076298264943 0
		-2.2117114679877868e-19 -0.28674740608727362 -0.050561120475857355
		-2.2117114679877868e-19 -0.27361110923879289 -0.099586536896091815
		-2.2117114679877868e-19 -0.25216172390797592 -0.14558562649835338
		-2.2117114679877868e-19 -0.22304998876293558 -0.1871613592052391
		-2.2117114679877868e-19 -0.1871608691911818 -0.22304998876293558
		-2.2117114679877868e-19 -0.14558562649835338 -0.25216172390797592
		-2.2117114679877868e-19 -0.099586536896091815 -0.27361159925285011
		-2.2117114679877868e-19 -0.050561120475857355 -0.28674740608727362
		-2.2117114679877868e-19 0 -0.29117125299670676
		-2.2117114679877868e-19 0.050561120475857355 -0.28674740608727362
		-2.2117114679877868e-19 0.099586536896091815 -0.27361159925285011
		-2.2117114679877868e-19 0.14558562649835338 -0.25216172390797592
		-2.2117114679877868e-19 0.1871608691911818 -0.22304998876293558
		-2.2117114679877868e-19 0.22304998876293558 -0.1871613592052391
		-2.2117114679877868e-19 0.25216172390797592 -0.14558562649835338
		-2.2117114679877868e-19 0.27361110923879289 -0.099586536896091815
		-2.2117114679877868e-19 0.28674740608727362 -0.050561120475857355
		-2.2117114679877868e-19 0.29117076298264943 0
		0.050561120475857355 0.28674740608727362 0
		0.099586536896091815 0.27361110923879289 0
		0.14558562649835338 0.25216172390797592 0
		0.1871613592052391 0.22304998876293558 0
		0.22304998876293558 0.1871608691911818 0
		0.25216172390797592 0.14558562649835338 0
		0.27361110923879289 0.099586536896091815 0
		0.28674740608727362 0.050561120475857355 0
		0.29117076298264943 0 0
		0.28674740608727362 -0.050561120475857355 0
		0.27361110923879289 -0.099586536896091815 0
		0.25216172390797592 -0.14558562649835338 0
		0.22304998876293558 -0.1871608691911818 0
		0.1871613592052391 -0.22304998876293558 0
		0.14558562649835338 -0.25216172390797592 0
		0.099586536896091815 -0.27361110923879289 0
		0.050561120475857355 -0.28674740608727362 0
		-2.2117114679877868e-19 -0.29117076298264943 0
		-0.050561120475857355 -0.28674740608727362 0
		-0.099586536896091815 -0.27361110923879289 0
		-0.14558562649835338 -0.25216172390797592 0
		-0.1871613592052391 -0.22304998876293558 0
		-0.22304998876293558 -0.1871608691911818 0
		-0.25216172390797592 -0.14558562649835338 0
		-0.27361110923879289 -0.099586536896091815 0
		-0.28674740608727362 -0.050561120475857355 0
		-0.29117125299670676 0 0
		-0.28674740608727362 0.050561120475857355 0
		-0.27361110923879289 0.099586536896091815 0
		-0.25216172390797592 0.14558562649835338 0
		-0.22304998876293558 0.1871608691911818 0
		-0.1871613592052391 0.22304998876293558 0
		-0.14558562649835338 0.25216172390797592 0
		-0.099586536896091815 0.27361110923879289 0
		-0.050561120475857355 0.28674740608727362 0
		-2.2117114679877868e-19 0.29117076298264943 0
		-1.5068471280088274e-09 0.28674740608727362 0.050561120475857355
		-2.967902442140464e-09 0.27361110923879289 0.099586536896091815
		-4.3387853694451346e-09 0.25216172390797592 0.14558562649835338
		-5.5778300146294021e-09 0.22304998876293558 0.1871613592052391
		-6.6473836975292402e-09 0.1871608691911818 0.22304998876293558
		-7.5150025874098716e-09 0.14558562649835338 0.25216172390797592
		-8.1542749265820509e-09 0.099586536896091815 0.27361110923879289
		-8.545747156970415e-09 0.050561120475857355 0.28674740608727362
		-8.6775609383879474e-09 0 0.29117125299670676
		-0.0899768712181018 0 0.27692017416783599
		-0.17114622977003721 0 0.23556249771645515
		-0.23556249771645515 0 0.17114622977003721
		-0.27692017416783599 0 0.0899768712181018
		-0.29117125299670676 0 0
		-0.27692017416783599 0 -0.0899768712181018
		-0.23556249771645515 0 -0.17114622977003721
		-0.17114622977003721 0 -0.23556249771645515
		-0.0899768712181018 0 -0.27692017416783599
		-2.2117114679877868e-19 0 -0.29117125299670676
		0.0899768712181018 0 -0.27692017416783599
		0.17114622977003721 0 -0.23556249771645515
		0.23556249771645515 0 -0.17114622977003721
		0.27692017416783599 0 -0.0899768712181018
		0.29117076298264943 0 0
		0.27692017416783599 0 0.0899768712181018
		0.23556249771645515 0 0.17114622977003721
		0.17114622977003721 0 0.23556249771645515
		0.0899768712181018 0 0.27692017416783599
		-8.6775609383879474e-09 0 0.29117125299670676
		;
createNode nurbsCurve -n "Tongue_02_Guide_Ctrl_Ctrl_CtrlShape" -p "Tongue_02_Guide";
	rename -uid "27154000-0018-1FF3-6621-A96000000F78";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2024/scripts/rigging/Mutant_Tools/Icons/";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 13;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 9 0 no 3
		10 0 1 2 3 4 5 6 7 8 9
		10
		-0.24500702865713031 -0.12250351432856529 -6.8490734833530161e-06
		0.46312747600348458 -0.12540243749163613 -6.8490734831957788e-06
		0.36244036753466469 -0.24816418922840591 -6.8490734832181371e-06
		0.48520211927143447 -0.46019719194074493 -6.8490734831908779e-06
		1.1266903020107943 -1.8984614597508849e-07 -6.7614589696006498e-06
		0.4852026092854918 0.46019719194074504 -6.8490734831908779e-06
		0.36244036753466463 0.24816369921434869 -6.8490734832181371e-06
		0.46312747600348453 0.12408184960717444 -3.5121561551348348e-06
		-0.24500702865713037 0.1225035143285651 -6.8490734833530161e-06
		-0.24500702865713031 -0.12250351432856529 -6.8490734833530161e-06
		;
createNode nurbsCurve -n "Tongue_02_Guide_Ctrl_Ctrl_Ctrl_CtrlShape" -p "Tongue_02_Guide";
	rename -uid "27154000-0018-1FF3-6621-A96000000F79";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2024/scripts/rigging/Mutant_Tools/Icons/";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 6;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 9 0 no 3
		10 0 1 2 3 4 5 6 7 8 9
		10
		0.12250351432856529 6.8490734832714138e-06 -0.24500702865713031
		0.12540243749163613 6.8490734832707675e-06 0.46312747600348458
		0.24816418922840591 6.8490734832435108e-06 0.36244036753466469
		0.46019719194074493 6.8490734831964285e-06 0.48520211927143447
		1.8984614597486874e-07 6.7614589698508244e-06 1.1266903020107943
		-0.46019719194074504 6.8490734834007989e-06 0.4852026092854918
		-0.24816369921434869 6.8490734833537183e-06 0.36244036753466463
		-0.12408184960717444 3.5121561552652233e-06 0.46312747600348453
		-0.1225035143285651 6.8490734833258161e-06 -0.24500702865713037
		0.12250351432856529 6.8490734832714138e-06 -0.24500702865713031
		;
createNode joint -n "Tongue_03_Guide" -p "Tongue_02_Guide";
	rename -uid "27154000-0018-1FF3-6621-A96000000F7A";
	addAttr -ci true -sn "Helper" -ln "Helper" -min 0 -max 1 -en "Hide:Show" -at "enum";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2024/scripts/rigging/Mutant_Tools/Icons/";
	setAttr ".t" -type "double3" 5.9320628409409437e-09 -1.68302960901201e-07 1.9100903307522259 ;
	setAttr ".r" -type "double3" 30.590100770913732 0 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr -cb on ".Helper" 1;
createNode nurbsCurve -n "Tongue_03_Guide_CtrlShape" -p "Tongue_03_Guide";
	rename -uid "27154000-0018-1FF3-6621-A96000000F7B";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2024/scripts/rigging/Mutant_Tools/Icons/";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 14;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 9 0 no 3
		10 0 1 2 3 4 5 6 7 8 9
		10
		6.8490734832983909e-06 -0.24500702865712873 0.12250351432856518
		6.8490734832983909e-06 0.4631274760034863 0.12540243749163624
		6.8490734832983909e-06 0.3624403675346663 0.24816418922840597
		6.8490734832983909e-06 0.48520211927143619 0.46019719194074493
		6.7614589698505982e-06 1.126690302010795 1.8984614622526398e-07
		6.8490734832983909e-06 0.48520260928549352 -0.46019719194074493
		6.8490734832983909e-06 0.3624403675346663 -0.24816369921434858
		3.5121561552374469e-06 0.4631274760034863 -0.12408184960717429
		6.8490734832983909e-06 -0.24500702865712873 -0.12250351432856518
		6.8490734832983909e-06 -0.24500702865712873 0.12250351432856518
		;
createNode nurbsCurve -n "Tongue_03_Guide_Ctrl_CtrlShape" -p "Tongue_03_Guide";
	rename -uid "27154000-0018-1FF3-6621-A96000000F7C";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2024/scripts/rigging/Mutant_Tools/Icons/";
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
		-2.2117114679877868e-19 0.29117076298265088 0
		-1.5068471280088274e-09 0.28674740608727511 0.050561120475857355
		-2.967902442140464e-09 0.27361110923879461 0.099586536896091815
		-4.3387853694451346e-09 0.25216172390797725 0.14558562649835338
		-5.5778300146294021e-09 0.22304998876293733 0.1871613592052391
		-6.6473836975292402e-09 0.18716086919118363 0.22304998876293558
		-7.5150025874098716e-09 0.14558562649835516 0.25216172390797592
		-8.1542749265820509e-09 0.099586536896093564 0.27361110923879289
		-8.545747156970415e-09 0.050561120475859166 0.28674740608727362
		-8.6775609383879474e-09 1.811834034575595e-15 0.29117125299670676
		-8.545747156970415e-09 -0.05056112047585553 0.28674740608727362
		-8.1542749265820509e-09 -0.099586536896090025 0.27361110923879289
		-7.5150025874098716e-09 -0.14558562649835161 0.25216172390797592
		-6.6473836975292402e-09 -0.18716086919117988 0.22304998876293558
		-5.5778300146294021e-09 -0.22304998876293389 0.1871613592052391
		-4.3387853694451346e-09 -0.25216172390797426 0.14558562649835338
		-2.967902442140464e-09 -0.27361110923879134 0.099586536896091815
		-1.5068471280088274e-09 -0.28674740608727206 0.050561120475857355
		-2.2117114679877868e-19 -0.29117076298264782 0
		-2.2117114679877868e-19 -0.28674740608727206 -0.050561120475857355
		-2.2117114679877868e-19 -0.27361110923879134 -0.099586536896091815
		-2.2117114679877868e-19 -0.25216172390797426 -0.14558562649835338
		-2.2117114679877868e-19 -0.22304998876293389 -0.1871613592052391
		-2.2117114679877868e-19 -0.18716086919117988 -0.22304998876293558
		-2.2117114679877868e-19 -0.14558562649835161 -0.25216172390797592
		-2.2117114679877868e-19 -0.099586536896090025 -0.27361159925285011
		-2.2117114679877868e-19 -0.05056112047585553 -0.28674740608727362
		-2.2117114679877868e-19 1.811834034575595e-15 -0.29117125299670676
		-2.2117114679877868e-19 0.050561120475859166 -0.28674740608727362
		-2.2117114679877868e-19 0.099586536896093564 -0.27361159925285011
		-2.2117114679877868e-19 0.14558562649835516 -0.25216172390797592
		-2.2117114679877868e-19 0.18716086919118363 -0.22304998876293558
		-2.2117114679877868e-19 0.22304998876293733 -0.1871613592052391
		-2.2117114679877868e-19 0.25216172390797725 -0.14558562649835338
		-2.2117114679877868e-19 0.27361110923879461 -0.099586536896091815
		-2.2117114679877868e-19 0.28674740608727511 -0.050561120475857355
		-2.2117114679877868e-19 0.29117076298265088 0
		0.050561120475857355 0.28674740608727511 0
		0.099586536896091815 0.27361110923879461 0
		0.14558562649835338 0.25216172390797725 0
		0.1871613592052391 0.22304998876293733 0
		0.22304998876293558 0.18716086919118363 0
		0.25216172390797592 0.14558562649835516 0
		0.27361110923879289 0.099586536896093564 0
		0.28674740608727362 0.050561120475859166 0
		0.29117076298264943 1.811834034575595e-15 0
		0.28674740608727362 -0.05056112047585553 0
		0.27361110923879289 -0.099586536896090025 0
		0.25216172390797592 -0.14558562649835161 0
		0.22304998876293558 -0.18716086919117988 0
		0.1871613592052391 -0.22304998876293389 0
		0.14558562649835338 -0.25216172390797426 0
		0.099586536896091815 -0.27361110923879134 0
		0.050561120475857355 -0.28674740608727206 0
		-2.2117114679877868e-19 -0.29117076298264782 0
		-0.050561120475857355 -0.28674740608727206 0
		-0.099586536896091815 -0.27361110923879134 0
		-0.14558562649835338 -0.25216172390797426 0
		-0.1871613592052391 -0.22304998876293389 0
		-0.22304998876293558 -0.18716086919117988 0
		-0.25216172390797592 -0.14558562649835161 0
		-0.27361110923879289 -0.099586536896090025 0
		-0.28674740608727362 -0.05056112047585553 0
		-0.29117125299670676 1.811834034575595e-15 0
		-0.28674740608727362 0.050561120475859166 0
		-0.27361110923879289 0.099586536896093564 0
		-0.25216172390797592 0.14558562649835516 0
		-0.22304998876293558 0.18716086919118363 0
		-0.1871613592052391 0.22304998876293733 0
		-0.14558562649835338 0.25216172390797725 0
		-0.099586536896091815 0.27361110923879461 0
		-0.050561120475857355 0.28674740608727511 0
		-2.2117114679877868e-19 0.29117076298265088 0
		-1.5068471280088274e-09 0.28674740608727511 0.050561120475857355
		-2.967902442140464e-09 0.27361110923879461 0.099586536896091815
		-4.3387853694451346e-09 0.25216172390797725 0.14558562649835338
		-5.5778300146294021e-09 0.22304998876293733 0.1871613592052391
		-6.6473836975292402e-09 0.18716086919118363 0.22304998876293558
		-7.5150025874098716e-09 0.14558562649835516 0.25216172390797592
		-8.1542749265820509e-09 0.099586536896093564 0.27361110923879289
		-8.545747156970415e-09 0.050561120475859166 0.28674740608727362
		-8.6775609383879474e-09 1.811834034575595e-15 0.29117125299670676
		-0.0899768712181018 1.811834034575595e-15 0.27692017416783599
		-0.17114622977003721 1.811834034575595e-15 0.23556249771645515
		-0.23556249771645515 1.811834034575595e-15 0.17114622977003721
		-0.27692017416783599 1.811834034575595e-15 0.0899768712181018
		-0.29117125299670676 1.811834034575595e-15 0
		-0.27692017416783599 1.811834034575595e-15 -0.0899768712181018
		-0.23556249771645515 1.811834034575595e-15 -0.17114622977003721
		-0.17114622977003721 1.811834034575595e-15 -0.23556249771645515
		-0.0899768712181018 1.811834034575595e-15 -0.27692017416783599
		-2.2117114679877868e-19 1.811834034575595e-15 -0.29117125299670676
		0.0899768712181018 1.811834034575595e-15 -0.27692017416783599
		0.17114622977003721 1.811834034575595e-15 -0.23556249771645515
		0.23556249771645515 1.811834034575595e-15 -0.17114622977003721
		0.27692017416783599 1.811834034575595e-15 -0.0899768712181018
		0.29117076298264943 1.811834034575595e-15 0
		0.27692017416783599 1.811834034575595e-15 0.0899768712181018
		0.23556249771645515 1.811834034575595e-15 0.17114622977003721
		0.17114622977003721 1.811834034575595e-15 0.23556249771645515
		0.0899768712181018 1.811834034575595e-15 0.27692017416783599
		-8.6775609383879474e-09 1.811834034575595e-15 0.29117125299670676
		;
createNode nurbsCurve -n "Tongue_03_Guide_Ctrl_Ctrl_CtrlShape" -p "Tongue_03_Guide";
	rename -uid "27154000-0018-1FF3-6621-A96000000F7D";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2024/scripts/rigging/Mutant_Tools/Icons/";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 13;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 9 0 no 3
		10 0 1 2 3 4 5 6 7 8 9
		10
		-0.24500702865713031 -0.12250351432856336 -6.8490734833530161e-06
		0.46312747600348458 -0.12540243749163427 -6.8490734831957788e-06
		0.36244036753466469 -0.24816418922840427 -6.8490734832181371e-06
		0.48520211927143447 -0.46019719194074304 -6.8490734831908779e-06
		1.1266903020107943 -1.8984614416325431e-07 -6.7614589696006498e-06
		0.4852026092854918 0.46019719194074687 -6.8490734831908779e-06
		0.36244036753466463 0.24816369921435036 -6.8490734832181371e-06
		0.46312747600348453 0.12408184960717634 -3.5121561551348348e-06
		-0.24500702865713037 0.12250351432856696 -6.8490734833530161e-06
		-0.24500702865713031 -0.12250351432856336 -6.8490734833530161e-06
		;
createNode nurbsCurve -n "Tongue_03_Guide_Ctrl_Ctrl_Ctrl_CtrlShape" -p "Tongue_03_Guide";
	rename -uid "27154000-0018-1FF3-6621-A96000000F7E";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2024/scripts/rigging/Mutant_Tools/Icons/";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 6;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 9 0 no 3
		10 0 1 2 3 4 5 6 7 8 9
		10
		0.12250351432856529 6.8490734850832477e-06 -0.24500702865713031
		0.12540243749163613 6.8490734850826006e-06 0.46312747600348458
		0.24816418922840591 6.849073485055349e-06 0.36244036753466469
		0.46019719194074493 6.8490734850082641e-06 0.48520211927143447
		1.8984614597486874e-07 6.7614589716626617e-06 1.1266903020107943
		-0.46019719194074504 6.849073485212632e-06 0.4852026092854918
		-0.24816369921434869 6.8490734851655522e-06 0.36244036753466463
		-0.12408184960717444 3.5121561570770539e-06 0.46312747600348453
		-0.1225035143285651 6.8490734851376467e-06 -0.24500702865713037
		0.12250351432856529 6.8490734850832477e-06 -0.24500702865713031
		;
createNode joint -n "Tongue_04_Guide" -p "Tongue_03_Guide";
	rename -uid "27154000-0018-1FF3-6621-A96000000F7F";
	addAttr -ci true -sn "Helper" -ln "Helper" -min 0 -max 1 -en "Hide:Show" -at "enum";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2024/scripts/rigging/Mutant_Tools/Icons/";
	setAttr ".t" -type "double3" -9.7215799507721634e-09 -2.8166776644411584e-06 1.9100905738456779 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 5.5659706925611543e-15 0 0 ;
	setAttr -cb on ".Helper" 1;
createNode nurbsCurve -n "Tongue_04_Guide_CtrlShape" -p "Tongue_04_Guide";
	rename -uid "27154000-0018-1FF3-6621-A96000000F80";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2024/scripts/rigging/Mutant_Tools/Icons/";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 14;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 9 0 no 3
		10 0 1 2 3 4 5 6 7 8 9
		10
		6.8490734832988348e-06 -0.24500702865713037 0.12250351432856518
		6.8490734832988348e-06 0.46312747600348453 0.12540243749163624
		6.8490734832988348e-06 0.36244036753466469 0.24816418922840597
		6.8490734832988348e-06 0.48520211927143436 0.46019719194074493
		6.7614589698510471e-06 1.1266903020107943 1.8984614619695397e-07
		6.8490734832988348e-06 0.48520260928549191 -0.46019719194074493
		6.8490734832988348e-06 0.36244036753466469 -0.24816369921434858
		3.5121561552378916e-06 0.46312747600348453 -0.12408184960717429
		6.8490734832988348e-06 -0.24500702865713037 -0.12250351432856518
		6.8490734832988348e-06 -0.24500702865713037 0.12250351432856518
		;
createNode nurbsCurve -n "Tongue_04_Guide_Ctrl_CtrlShape" -p "Tongue_04_Guide";
	rename -uid "27154000-0018-1FF3-6621-A96000000F81";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2024/scripts/rigging/Mutant_Tools/Icons/";
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
		2.2117114679877868e-19 0.29117076298264943 -2.8309906790243671e-17
		-1.5068471275664843e-09 0.28674740608727362 0.050561120475857355
		-2.967902441698123e-09 0.27361110923879289 0.099586536896091815
		-4.3387853690027915e-09 0.25216172390797592 0.14558562649835338
		-5.5778300141870532e-09 0.22304998876293558 0.1871613592052391
		-6.6473836970868897e-09 0.1871608691911818 0.22304998876293558
		-7.5150025869675186e-09 0.14558562649835338 0.25216172390797592
		-8.1542749261397061e-09 0.099586536896091815 0.27361110923879289
		-8.5457471565280636e-09 0.050561120475857355 0.28674740608727362
		-8.677560937945606e-09 0 0.29117125299670676
		-8.5457471565280636e-09 -0.050561120475857355 0.28674740608727362
		-8.1542749261397061e-09 -0.099586536896091815 0.27361110923879289
		-7.5150025869675186e-09 -0.14558562649835338 0.25216172390797592
		-6.6473836970868897e-09 -0.1871608691911818 0.22304998876293558
		-5.5778300141870532e-09 -0.22304998876293558 0.1871613592052391
		-4.3387853690027915e-09 -0.25216172390797592 0.14558562649835338
		-2.967902441698123e-09 -0.27361110923879289 0.099586536896091815
		-1.5068471275664843e-09 -0.28674740608727362 0.050561120475857355
		2.2117114679877868e-19 -0.29117076298264943 -2.8309906790243671e-17
		2.2117114679877868e-19 -0.28674740608727362 -0.050561120475857355
		2.2117114679877868e-19 -0.27361110923879289 -0.099586536896091815
		2.2117114679877868e-19 -0.25216172390797592 -0.14558562649835338
		2.2117114679877868e-19 -0.22304998876293558 -0.1871613592052391
		2.2117114679877868e-19 -0.1871608691911818 -0.22304998876293558
		2.2117114679877868e-19 -0.14558562649835338 -0.25216172390797592
		2.2117114679877868e-19 -0.099586536896091815 -0.27361159925285011
		2.2117114679877868e-19 -0.050561120475857355 -0.28674740608727362
		2.2117114679877868e-19 0 -0.29117125299670676
		2.2117114679877868e-19 0.050561120475857355 -0.28674740608727362
		2.2117114679877868e-19 0.099586536896091815 -0.27361159925285011
		2.2117114679877868e-19 0.14558562649835338 -0.25216172390797592
		2.2117114679877868e-19 0.1871608691911818 -0.22304998876293558
		2.2117114679877868e-19 0.22304998876293558 -0.1871613592052391
		2.2117114679877868e-19 0.25216172390797592 -0.14558562649835338
		2.2117114679877868e-19 0.27361110923879289 -0.099586536896091815
		2.2117114679877868e-19 0.28674740608727362 -0.050561120475857355
		2.2117114679877868e-19 0.29117076298264943 -2.8309906790243671e-17
		0.050561120475857355 0.28674740608727362 -2.8309906790243671e-17
		0.099586536896091815 0.27361110923879289 -2.8309906790243671e-17
		0.14558562649835338 0.25216172390797592 -2.8309906790243671e-17
		0.1871613592052391 0.22304998876293558 -2.8309906790243671e-17
		0.22304998876293558 0.1871608691911818 -2.8309906790243671e-17
		0.25216172390797592 0.14558562649835338 -2.8309906790243671e-17
		0.27361110923879289 0.099586536896091815 -2.8309906790243671e-17
		0.28674740608727362 0.050561120475857355 -2.8309906790243671e-17
		0.29117076298264943 0 -2.8309906790243671e-17
		0.28674740608727362 -0.050561120475857355 -2.8309906790243671e-17
		0.27361110923879289 -0.099586536896091815 -2.8309906790243671e-17
		0.25216172390797592 -0.14558562649835338 -2.8309906790243671e-17
		0.22304998876293558 -0.1871608691911818 -2.8309906790243671e-17
		0.1871613592052391 -0.22304998876293558 -2.8309906790243671e-17
		0.14558562649835338 -0.25216172390797592 -2.8309906790243671e-17
		0.099586536896091815 -0.27361110923879289 -2.8309906790243671e-17
		0.050561120475857355 -0.28674740608727362 -2.8309906790243671e-17
		2.2117114679877868e-19 -0.29117076298264943 -2.8309906790243671e-17
		-0.050561120475857355 -0.28674740608727362 -2.8309906790243671e-17
		-0.099586536896091815 -0.27361110923879289 -2.8309906790243671e-17
		-0.14558562649835338 -0.25216172390797592 -2.8309906790243671e-17
		-0.1871613592052391 -0.22304998876293558 -2.8309906790243671e-17
		-0.22304998876293558 -0.1871608691911818 -2.8309906790243671e-17
		-0.25216172390797592 -0.14558562649835338 -2.8309906790243671e-17
		-0.27361110923879289 -0.099586536896091815 -2.8309906790243671e-17
		-0.28674740608727362 -0.050561120475857355 -2.8309906790243671e-17
		-0.29117125299670676 0 -2.8309906790243671e-17
		-0.28674740608727362 0.050561120475857355 -2.8309906790243671e-17
		-0.27361110923879289 0.099586536896091815 -2.8309906790243671e-17
		-0.25216172390797592 0.14558562649835338 -2.8309906790243671e-17
		-0.22304998876293558 0.1871608691911818 -2.8309906790243671e-17
		-0.1871613592052391 0.22304998876293558 -2.8309906790243671e-17
		-0.14558562649835338 0.25216172390797592 -2.8309906790243671e-17
		-0.099586536896091815 0.27361110923879289 -2.8309906790243671e-17
		-0.050561120475857355 0.28674740608727362 -2.8309906790243671e-17
		2.2117114679877868e-19 0.29117076298264943 -2.8309906790243671e-17
		-1.5068471275664843e-09 0.28674740608727362 0.050561120475857355
		-2.967902441698123e-09 0.27361110923879289 0.099586536896091815
		-4.3387853690027915e-09 0.25216172390797592 0.14558562649835338
		-5.5778300141870532e-09 0.22304998876293558 0.1871613592052391
		-6.6473836970868897e-09 0.1871608691911818 0.22304998876293558
		-7.5150025869675186e-09 0.14558562649835338 0.25216172390797592
		-8.1542749261397061e-09 0.099586536896091815 0.27361110923879289
		-8.5457471565280636e-09 0.050561120475857355 0.28674740608727362
		-8.677560937945606e-09 0 0.29117125299670676
		-0.0899768712181018 0 0.27692017416783599
		-0.17114622977003721 0 0.23556249771645515
		-0.23556249771645515 0 0.17114622977003721
		-0.27692017416783599 0 0.0899768712181018
		-0.29117125299670676 0 -2.8309906790243671e-17
		-0.27692017416783599 0 -0.0899768712181018
		-0.23556249771645515 0 -0.17114622977003721
		-0.17114622977003721 0 -0.23556249771645515
		-0.0899768712181018 0 -0.27692017416783599
		2.2117114679877868e-19 0 -0.29117125299670676
		0.0899768712181018 0 -0.27692017416783599
		0.17114622977003721 0 -0.23556249771645515
		0.23556249771645515 0 -0.17114622977003721
		0.27692017416783599 0 -0.0899768712181018
		0.29117076298264943 0 -2.8309906790243671e-17
		0.27692017416783599 0 0.0899768712181018
		0.23556249771645515 0 0.17114622977003721
		0.17114622977003721 0 0.23556249771645515
		0.0899768712181018 0 0.27692017416783599
		-8.677560937945606e-09 0 0.29117125299670676
		;
createNode nurbsCurve -n "Tongue_04_Guide_Ctrl_Ctrl_CtrlShape" -p "Tongue_04_Guide";
	rename -uid "27154000-0018-1FF3-6621-A96000000F82";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2024/scripts/rigging/Mutant_Tools/Icons/";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 13;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 9 0 no 3
		10 0 1 2 3 4 5 6 7 8 9
		10
		-0.24500702865713031 -0.12250351432856529 -6.8490734833813222e-06
		0.46312747600348458 -0.12540243749163613 -6.8490734832240866e-06
		0.36244036753466469 -0.24816418922840591 -6.8490734832464441e-06
		0.48520211927143447 -0.46019719194074493 -6.8490734832191849e-06
		1.1266903020107943 -1.8984614597508849e-07 -6.761458969628956e-06
		0.4852026092854918 0.46019719194074504 -6.8490734832191849e-06
		0.36244036753466463 0.24816369921434869 -6.8490734832464441e-06
		0.46312747600348453 0.12408184960717444 -3.5121561551631473e-06
		-0.24500702865713037 0.1225035143285651 -6.8490734833813222e-06
		-0.24500702865713031 -0.12250351432856529 -6.8490734833813222e-06
		;
createNode nurbsCurve -n "Tongue_04_Guide_Ctrl_Ctrl_Ctrl_CtrlShape" -p "Tongue_04_Guide";
	rename -uid "27154000-0018-1FF3-6621-A96000000F83";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2024/scripts/rigging/Mutant_Tools/Icons/";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 6;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 9 0 no 3
		10 0 1 2 3 4 5 6 7 8 9
		10
		0.12250351432856529 6.8490734832714138e-06 -0.24500702865713031
		0.12540243749163613 6.8490734832707675e-06 0.46312747600348458
		0.24816418922840591 6.8490734832435108e-06 0.36244036753466469
		0.46019719194074493 6.8490734831964285e-06 0.48520211927143447
		1.8984614597531113e-07 6.7614589698508244e-06 1.1266903020107943
		-0.46019719194074504 6.8490734834007989e-06 0.4852026092854918
		-0.24816369921434869 6.8490734833537183e-06 0.36244036753466463
		-0.12408184960717444 3.5121561552652233e-06 0.46312747600348453
		-0.1225035143285651 6.8490734833258161e-06 -0.24500702865713037
		0.12250351432856529 6.8490734832714138e-06 -0.24500702865713031
		;
createNode joint -n "Tongue_05_Guide" -p "Tongue_04_Guide";
	rename -uid "27154000-0018-1FF3-6621-A96000000F84";
	addAttr -ci true -sn "Helper" -ln "Helper" -min 0 -max 1 -en "Hide:Show" -at "enum";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2024/scripts/rigging/Mutant_Tools/Icons/";
	setAttr ".t" -type "double3" 3.4384802574671802e-09 2.0655043897477299e-06 1.9100903566818497 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" -4.7708320221952752e-15 0 0 ;
	setAttr -cb on ".Helper" 1;
createNode nurbsCurve -n "Tongue_05_Guide_CtrlShape" -p "Tongue_05_Guide";
	rename -uid "27154000-0018-1FF3-6621-A96000000F85";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2024/scripts/rigging/Mutant_Tools/Icons/";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 14;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 9 0 no 3
		10 0 1 2 3 4 5 6 7 8 9
		10
		6.8490734832986137e-06 -0.24500702865713037 0.12250351432856471
		6.8490734832986137e-06 0.46312747600348453 0.12540243749163579
		6.8490734832986137e-06 0.36244036753466469 0.2481641892284058
		6.8490734832986137e-06 0.48520211927143436 0.46019719194074493
		6.7614589698508244e-06 1.1266903020107943 1.8984614577230544e-07
		6.8490734832986137e-06 0.48520260928549191 -0.46019719194074493
		6.8490734832986137e-06 0.36244036753466469 -0.24816369921434872
		3.5121561552376701e-06 0.46312747600348453 -0.12408184960717479
		6.8490734832986137e-06 -0.24500702865713037 -0.12250351432856572
		6.8490734832986137e-06 -0.24500702865713037 0.12250351432856471
		;
createNode nurbsCurve -n "Tongue_05_Guide_Ctrl_CtrlShape" -p "Tongue_05_Guide";
	rename -uid "27154000-0018-1FF3-6621-A96000000F86";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2024/scripts/rigging/Mutant_Tools/Icons/";
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
		0 0.29117076298264943 -4.5295850864389874e-16
		-1.5068471277876553e-09 0.28674740608727362 0.050561120475856897
		-2.9679024419192954e-09 0.27361110923879289 0.099586536896091385
		-4.3387853692239614e-09 0.25216172390797592 0.14558562649835291
		-5.5778300144082273e-09 0.22304998876293558 0.18716135920523885
		-6.6473836973080621e-09 0.1871608691911818 0.22304998876293544
		-7.5150025871886951e-09 0.14558562649835338 0.25216172390797581
		-8.1542749263608793e-09 0.099586536896091815 0.27361110923879278
		-8.5457471567492401e-09 0.050561120475857355 0.2867474060872735
		-8.6775609381667759e-09 0 0.29117125299670665
		-8.5457471567492401e-09 -0.050561120475857355 0.2867474060872735
		-8.1542749263608793e-09 -0.099586536896091815 0.27361110923879278
		-7.5150025871886951e-09 -0.14558562649835338 0.25216172390797581
		-6.6473836973080621e-09 -0.1871608691911818 0.22304998876293544
		-5.5778300144082273e-09 -0.22304998876293558 0.18716135920523885
		-4.3387853692239614e-09 -0.25216172390797592 0.14558562649835291
		-2.9679024419192954e-09 -0.27361110923879289 0.099586536896091385
		-1.5068471277876553e-09 -0.28674740608727362 0.050561120475856897
		0 -0.29117076298264943 -4.5295850864389874e-16
		0 -0.28674740608727362 -0.050561120475857785
		0 -0.27361110923879289 -0.099586536896092204
		0 -0.25216172390797592 -0.14558562649835374
		0 -0.22304998876293558 -0.18716135920523941
		0 -0.1871608691911818 -0.22304998876293575
		0 -0.14558562649835338 -0.25216172390797609
		0 -0.099586536896091815 -0.27361159925285022
		0 -0.050561120475857355 -0.28674740608727378
		0 0 -0.29117125299670688
		0 0.050561120475857355 -0.28674740608727378
		0 0.099586536896091815 -0.27361159925285022
		0 0.14558562649835338 -0.25216172390797609
		0 0.1871608691911818 -0.22304998876293575
		0 0.22304998876293558 -0.18716135920523941
		0 0.25216172390797592 -0.14558562649835374
		0 0.27361110923879289 -0.099586536896092204
		0 0.28674740608727362 -0.050561120475857785
		0 0.29117076298264943 -4.5295850864389874e-16
		0.050561120475857355 0.28674740608727362 -4.5295850864389874e-16
		0.099586536896091815 0.27361110923879289 -4.5295850864389874e-16
		0.14558562649835338 0.25216172390797592 -4.5295850864389874e-16
		0.1871613592052391 0.22304998876293558 -4.5295850864389874e-16
		0.22304998876293558 0.1871608691911818 -4.5295850864389874e-16
		0.25216172390797592 0.14558562649835338 -4.5295850864389874e-16
		0.27361110923879289 0.099586536896091815 -4.5295850864389874e-16
		0.28674740608727362 0.050561120475857355 -4.5295850864389874e-16
		0.29117076298264943 0 -4.5295850864389874e-16
		0.28674740608727362 -0.050561120475857355 -4.5295850864389874e-16
		0.27361110923879289 -0.099586536896091815 -4.5295850864389874e-16
		0.25216172390797592 -0.14558562649835338 -4.5295850864389874e-16
		0.22304998876293558 -0.1871608691911818 -4.5295850864389874e-16
		0.1871613592052391 -0.22304998876293558 -4.5295850864389874e-16
		0.14558562649835338 -0.25216172390797592 -4.5295850864389874e-16
		0.099586536896091815 -0.27361110923879289 -4.5295850864389874e-16
		0.050561120475857355 -0.28674740608727362 -4.5295850864389874e-16
		0 -0.29117076298264943 -4.5295850864389874e-16
		-0.050561120475857355 -0.28674740608727362 -4.5295850864389874e-16
		-0.099586536896091815 -0.27361110923879289 -4.5295850864389874e-16
		-0.14558562649835338 -0.25216172390797592 -4.5295850864389874e-16
		-0.1871613592052391 -0.22304998876293558 -4.5295850864389874e-16
		-0.22304998876293558 -0.1871608691911818 -4.5295850864389874e-16
		-0.25216172390797592 -0.14558562649835338 -4.5295850864389874e-16
		-0.27361110923879289 -0.099586536896091815 -4.5295850864389874e-16
		-0.28674740608727362 -0.050561120475857355 -4.5295850864389874e-16
		-0.29117125299670676 0 -4.5295850864389874e-16
		-0.28674740608727362 0.050561120475857355 -4.5295850864389874e-16
		-0.27361110923879289 0.099586536896091815 -4.5295850864389874e-16
		-0.25216172390797592 0.14558562649835338 -4.5295850864389874e-16
		-0.22304998876293558 0.1871608691911818 -4.5295850864389874e-16
		-0.1871613592052391 0.22304998876293558 -4.5295850864389874e-16
		-0.14558562649835338 0.25216172390797592 -4.5295850864389874e-16
		-0.099586536896091815 0.27361110923879289 -4.5295850864389874e-16
		-0.050561120475857355 0.28674740608727362 -4.5295850864389874e-16
		0 0.29117076298264943 -4.5295850864389874e-16
		-1.5068471277876553e-09 0.28674740608727362 0.050561120475856897
		-2.9679024419192954e-09 0.27361110923879289 0.099586536896091385
		-4.3387853692239614e-09 0.25216172390797592 0.14558562649835291
		-5.5778300144082273e-09 0.22304998876293558 0.18716135920523885
		-6.6473836973080621e-09 0.1871608691911818 0.22304998876293544
		-7.5150025871886951e-09 0.14558562649835338 0.25216172390797581
		-8.1542749263608793e-09 0.099586536896091815 0.27361110923879278
		-8.5457471567492401e-09 0.050561120475857355 0.2867474060872735
		-8.6775609381667759e-09 0 0.29117125299670665
		-0.0899768712181018 0 0.27692017416783593
		-0.17114622977003721 0 0.23556249771645499
		-0.23556249771645515 0 0.17114622977003691
		-0.27692017416783599 0 0.089976871218101426
		-0.29117125299670676 0 -4.5295850864389874e-16
		-0.27692017416783599 0 -0.089976871218102258
		-0.23556249771645515 0 -0.17114622977003743
		-0.17114622977003721 0 -0.23556249771645529
		-0.0899768712181018 0 -0.27692017416783615
		0 0 -0.29117125299670688
		0.0899768712181018 0 -0.27692017416783615
		0.17114622977003721 0 -0.23556249771645529
		0.23556249771645515 0 -0.17114622977003743
		0.27692017416783599 0 -0.089976871218102258
		0.29117076298264943 0 -4.5295850864389874e-16
		0.27692017416783599 0 0.089976871218101426
		0.23556249771645515 0 0.17114622977003691
		0.17114622977003721 0 0.23556249771645499
		0.0899768712181018 0 0.27692017416783593
		-8.6775609381667759e-09 0 0.29117125299670665
		;
createNode nurbsCurve -n "Tongue_05_Guide_Ctrl_Ctrl_CtrlShape" -p "Tongue_05_Guide";
	rename -uid "27154000-0018-1FF3-6621-A96000000F87";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2024/scripts/rigging/Mutant_Tools/Icons/";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 13;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 9 0 no 3
		10 0 1 2 3 4 5 6 7 8 9
		10
		-0.24500702865713031 -0.12250351432856529 -6.8490734838059703e-06
		0.46312747600348458 -0.12540243749163613 -6.8490734836487322e-06
		0.36244036753466469 -0.24816418922840591 -6.8490734836710896e-06
		0.48520211927143447 -0.46019719194074493 -6.849073483643833e-06
		1.1266903020107943 -1.8984614597508849e-07 -6.7614589700536041e-06
		0.4852026092854918 0.46019719194074504 -6.849073483643833e-06
		0.36244036753466463 0.24816369921434869 -6.8490734836710896e-06
		0.46312747600348453 0.12408184960717444 -3.5121561555877937e-06
		-0.24500702865713037 0.1225035143285651 -6.8490734838059703e-06
		-0.24500702865713031 -0.12250351432856529 -6.8490734838059703e-06
		;
createNode nurbsCurve -n "Tongue_05_Guide_Ctrl_Ctrl_Ctrl_CtrlShape" -p "Tongue_05_Guide";
	rename -uid "27154000-0018-1FF3-6621-A96000000F88";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2024/scripts/rigging/Mutant_Tools/Icons/";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 6;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 9 0 no 3
		10 0 1 2 3 4 5 6 7 8 9
		10
		0.12250351432856529 6.8490734832714138e-06 -0.24500702865713048
		0.12540243749163613 6.8490734832707675e-06 0.46312747600348458
		0.24816418922840591 6.8490734832435108e-06 0.36244036753466458
		0.46019719194074493 6.8490734831964285e-06 0.48520211927143447
		1.8984614597509e-07 6.7614589698508244e-06 1.1266903020107943
		-0.46019719194074504 6.8490734834007989e-06 0.4852026092854918
		-0.24816369921434869 6.8490734833537183e-06 0.36244036753466452
		-0.12408184960717444 3.5121561552652233e-06 0.46312747600348453
		-0.1225035143285651 6.8490734833258161e-06 -0.24500702865713053
		0.12250351432856529 6.8490734832714138e-06 -0.24500702865713048
		;
createNode dagContainer -n "Teeth_Block" -p "face";
	rename -uid "27154000-0018-1FF3-6621-A96000000F89";
	addAttr -ci true -sn "nts" -ln "notes" -dt "string";
	setAttr ".isc" yes;
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2024/scripts/rigging/Mutant_Tools/Icons/Teeth.png";
	setAttr ".ctor" -type "string" "esteban.rodriguez";
	setAttr ".cdat" -type "string" "2022/04/26 11:02:34";
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
	setAttr ".nts" -type "string" "['Teeth_Lwr_Ctrl_Offset_Grp', 'Teeth_Lwr_Bnd_parentConstraint1', 'Teeth_Lwr_Jnt', 'Teeth_Upr_CtrlShape', 'Teeth_Upr_Ctrl_Offset_Grp', 'Teeth_Upr_Bnd', 'Teeth_Lwr_Jnt_Offset_Grp_scaleConstraint1', 'Teeth_Lwr_CtrlShape', 'Teeth_Upr_Jnt_Offset_Grp_scaleConstraint1', 'Teeth_Upr_Jnt_Offset_Grp', 'Teeth_Upr_Bnd_scaleConstraint1', 'Teeth_Upr_Bnd_parentConstraint1', 'Teeth_Upr_Jnt', 'Teeth_Lwr_Jnt_Offset_Grp_parentConstraint1', 'Teeth_Lwr_Ctrl_Offset_Grp_parentConstraint1', 'Teeth_Lwr_Bnd_scaleConstraint1', 'Teeth_Upr_Ctrl_tag', 'Teeth_Upr_Ctrl_Offset_Grp_parentConstraint1', 'Teeth_Lwr_Ctrl', 'Teeth_Ctrl_Grp', 'Teeth_Upr_Jnt_Offset_Grp_parentConstraint1', 'Teeth_Rig_Grp', 'Teeth_Lwr_Jnt_Offset_Grp', 'Teeth_Lwr_Bnd', 'Teeth_Upr_Ctrl', 'Teeth_Lwr_Ctrl_tag']";
createNode joint -n "Teeth_Lwr_Guide" -p "Teeth_Block";
	rename -uid "27154000-0018-1FF3-6621-A96000000F8A";
	addAttr -ci true -sn "Helper" -ln "Helper" -min 0 -max 1 -en "Hide:Show" -at "enum";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2024/scripts/rigging/Mutant_Tools/Icons/";
	setAttr ".t" -type "double3" 0.030614104913812834 6.5922937510123631 9.3145282882988631 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr -cb on ".Helper" 1;
createNode nurbsCurve -n "Teeth_Lwr_Guide_CtrlShape" -p "Teeth_Lwr_Guide";
	rename -uid "27154000-0018-1FF3-6621-A96000000F8B";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2024/scripts/rigging/Mutant_Tools/Icons/";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 14;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 9 0 no 3
		10 0 1 2 3 4 5 6 7 8 9
		10
		4.5762334581595966e-06 -0.16370234087268618 0.081851170436343088
		4.5762334581595966e-06 0.30944031426268537 0.083788096533548739
		4.5762334581595966e-06 0.24216585506700999 0.16581180923717176
		4.5762334581595966e-06 0.32418956777063296 0.30748243426584837
		4.5176935010635258e-06 0.75280223954649872 1.2684639584860965e-07
		4.5762334581595966e-06 0.32418989517531488 -0.30748243426584837
		4.5762334581595966e-06 0.24216585506700999 -0.16581148183248978
		2.3466599602226874e-06 0.30944031426268537 -0.082905740916244891
		4.5762334581595966e-06 -0.16370234087268618 -0.081851170436343088
		4.5762334581595966e-06 -0.16370234087268618 0.081851170436343088
		;
createNode nurbsCurve -n "Teeth_Lwr_Guide_Ctrl_CtrlShape" -p "Teeth_Lwr_Guide";
	rename -uid "27154000-0018-1FF3-6621-A96000000F8C";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2024/scripts/rigging/Mutant_Tools/Icons/";
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
		0 0.19454680853523612 0
		-1.006805410882013e-09 0.19159132647312063 0.033782597276532739
		-1.9830148542549199e-09 0.18281426176489071 0.066539108280475531
		-2.8989752880930453e-09 0.16848277663085043 0.097273567969958924
		-3.7268474923075738e-09 0.14903166448835795 0.12505254559732676
		-4.441473691153197e-09 0.12505221819264506 0.14903166448835795
		-5.0211764206515582e-09 0.097273567969958924 0.16848277663085043
		-5.4483085684565726e-09 0.066539108280475531 0.18281426176489071
		-5.7098721687029442e-09 0.033782597276532739 0.19159132647312063
		-5.7979440280924536e-09 0 0.19454713593991785
		-5.7098721687029442e-09 -0.033782597276532739 0.19159132647312063
		-5.4483085684565726e-09 -0.066539108280475531 0.18281426176489071
		-5.0211764206515582e-09 -0.097273567969958924 0.16848277663085043
		-4.441473691153197e-09 -0.12505221819264506 0.14903166448835795
		-3.7268474923075738e-09 -0.14903166448835795 0.12505254559732676
		-2.8989752880930453e-09 -0.16848277663085043 0.097273567969958924
		-1.9830148542549199e-09 -0.18281426176489071 0.066539108280475531
		-1.006805410882013e-09 -0.19159132647312063 0.033782597276532739
		0 -0.19454680853523612 0
		0 -0.19159132647312063 -0.033782597276532739
		0 -0.18281426176489071 -0.066539108280475531
		0 -0.16848277663085043 -0.097273567969958924
		0 -0.14903166448835795 -0.12505254559732676
		0 -0.12505221819264506 -0.14903166448835795
		0 -0.097273567969958924 -0.16848277663085043
		0 -0.066539108280475531 -0.18281458916957247
		0 -0.033782597276532739 -0.19159132647312063
		0 0 -0.19454713593991785
		0 0.033782597276532739 -0.19159132647312063
		0 0.066539108280475531 -0.18281458916957247
		0 0.097273567969958924 -0.16848277663085043
		0 0.12505221819264506 -0.14903166448835795
		0 0.14903166448835795 -0.12505254559732676
		0 0.16848277663085043 -0.097273567969958924
		0 0.18281426176489071 -0.066539108280475531
		0 0.19159132647312063 -0.033782597276532739
		0 0.19454680853523612 0
		0.033782597276532739 0.19159132647312063 0
		0.066539108280475531 0.18281426176489071 0
		0.097273567969958924 0.16848277663085043 0
		0.12505254559732676 0.14903166448835795 0
		0.14903166448835795 0.12505221819264506 0
		0.16848277663085043 0.097273567969958924 0
		0.18281426176489071 0.066539108280475531 0
		0.19159132647312063 0.033782597276532739 0
		0.19454680853523612 0 0
		0.19159132647312063 -0.033782597276532739 0
		0.18281426176489071 -0.066539108280475531 0
		0.16848277663085043 -0.097273567969958924 0
		0.14903166448835795 -0.12505221819264506 0
		0.12505254559732676 -0.14903166448835795 0
		0.097273567969958924 -0.16848277663085043 0
		0.066539108280475531 -0.18281426176489071 0
		0.033782597276532739 -0.19159132647312063 0
		0 -0.19454680853523612 0
		-0.033782597276532739 -0.19159132647312063 0
		-0.066539108280475531 -0.18281426176489071 0
		-0.097273567969958924 -0.16848277663085043 0
		-0.12505254559732676 -0.14903166448835795 0
		-0.14903166448835795 -0.12505221819264506 0
		-0.16848277663085043 -0.097273567969958924 0
		-0.18281426176489071 -0.066539108280475531 0
		-0.19159132647312063 -0.033782597276532739 0
		-0.19454713593991785 0 0
		-0.19159132647312063 0.033782597276532739 0
		-0.18281426176489071 0.066539108280475531 0
		-0.16848277663085043 0.097273567969958924 0
		-0.14903166448835795 0.12505221819264506 0
		-0.12505254559732676 0.14903166448835795 0
		-0.097273567969958924 0.16848277663085043 0
		-0.066539108280475531 0.18281426176489071 0
		-0.033782597276532739 0.19159132647312063 0
		0 0.19454680853523612 0
		-1.006805410882013e-09 0.19159132647312063 0.033782597276532739
		-1.9830148542549199e-09 0.18281426176489071 0.066539108280475531
		-2.8989752880930453e-09 0.16848277663085043 0.097273567969958924
		-3.7268474923075738e-09 0.14903166448835795 0.12505254559732676
		-4.441473691153197e-09 0.12505221819264506 0.14903166448835795
		-5.0211764206515582e-09 0.097273567969958924 0.16848277663085043
		-5.4483085684565726e-09 0.066539108280475531 0.18281426176489071
		-5.7098721687029442e-09 0.033782597276532739 0.19159132647312063
		-5.7979440280924536e-09 0 0.19454713593991785
		-0.060118375066767052 0 0.18502522558071716
		-0.11435197838384267 0 0.15739194303672591
		-0.15739194303672591 0 0.11435197838384267
		-0.18502522558071716 0 0.060118375066767052
		-0.19454713593991785 0 0
		-0.18502522558071716 0 -0.060118375066767052
		-0.15739194303672591 0 -0.11435197838384267
		-0.11435197838384267 0 -0.15739194303672591
		-0.060118375066767052 0 -0.18502522558071716
		0 0 -0.19454713593991785
		0.060118375066767052 0 -0.18502522558071716
		0.11435197838384267 0 -0.15739194303672591
		0.15739194303672591 0 -0.11435197838384267
		0.18502522558071716 0 -0.060118375066767052
		0.19454680853523612 0 0
		0.18502522558071716 0 0.060118375066767052
		0.15739194303672591 0 0.11435197838384267
		0.11435197838384267 0 0.15739194303672591
		0.060118375066767052 0 0.18502522558071716
		-5.7979440280924536e-09 0 0.19454713593991785
		;
createNode nurbsCurve -n "Teeth_Lwr_Guide_Ctrl_Ctrl_CtrlShape" -p "Teeth_Lwr_Guide";
	rename -uid "27154000-0018-1FF3-6621-A96000000F8D";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2024/scripts/rigging/Mutant_Tools/Icons/";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 13;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 9 0 no 3
		10 0 1 2 3 4 5 6 7 8 9
		10
		-0.16370234087268618 -0.081851170436343171 -4.5762334581959462e-06
		0.30944031426268537 -0.083788096533548628 -4.5762334580908862e-06
		0.24216585506700999 -0.1658118092371717 -4.5762334581058261e-06
		0.32418956777063301 -0.30748243426584826 -4.5762334580876107e-06
		0.75280223954649872 -1.2684639568145402e-07 -4.5176935008963714e-06
		0.32418989517531488 0.30748243426584837 -4.5762334580876107e-06
		0.24216585506700999 0.16581148183248984 -4.5762334581058261e-06
		0.30944031426268537 0.082905740916245016 -2.3466599601539795e-06
		-0.16370234087268618 0.081851170436343088 -4.5762334581959462e-06
		-0.16370234087268618 -0.081851170436343171 -4.5762334581959462e-06
		;
createNode nurbsCurve -n "Teeth_Lwr_Guide_Ctrl_Ctrl_Ctrl_CtrlShape" -p "Teeth_Lwr_Guide";
	rename -uid "27154000-0018-1FF3-6621-A96000000F8E";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2024/scripts/rigging/Mutant_Tools/Icons/";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 6;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 9 0 no 3
		10 0 1 2 3 4 5 6 7 8 9
		10
		0.081851170436343171 4.5762334581414227e-06 -0.16370234087268618
		0.083788096533548628 4.5762334581409898e-06 0.30944031426268537
		0.1658118092371717 4.5762334581227761e-06 0.24216585506700999
		0.30748243426584826 4.5762334580913198e-06 0.32418956777063301
		1.2684639568145505e-07 4.5176935010635258e-06 0.75280223954649872
		-0.30748243426584837 4.5762334582278692e-06 0.32418989517531488
		-0.16581148183248984 4.5762334581964121e-06 0.24216585506700999
		-0.082905740916245016 2.3466599602410947e-06 0.30944031426268537
		-0.081851170436343088 4.576233458177768e-06 -0.16370234087268618
		0.081851170436343171 4.5762334581414227e-06 -0.16370234087268618
		;
createNode joint -n "Teeth_Upr_Guide" -p "Teeth_Block";
	rename -uid "27154000-0018-1FF3-6621-A96000000F8F";
	addAttr -ci true -sn "Helper" -ln "Helper" -min 0 -max 1 -en "Hide:Show" -at "enum";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2024/scripts/rigging/Mutant_Tools/Icons/";
	setAttr ".t" -type "double3" 0.11556943241369 8.9863562255975467 9.6227954192187166 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr -cb on ".Helper" 1;
createNode nurbsCurve -n "Teeth_Upr_Guide_CtrlShape" -p "Teeth_Upr_Guide";
	rename -uid "27154000-0018-1FF3-6621-A96000000F90";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2024/scripts/rigging/Mutant_Tools/Icons/";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 14;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 9 0 no 3
		10 0 1 2 3 4 5 6 7 8 9
		10
		4.5762334581595966e-06 -0.16370234087268618 0.081851170436343088
		4.5762334581595966e-06 0.30944031426268537 0.083788096533548739
		4.5762334581595966e-06 0.24216585506700999 0.16581180923717176
		4.5762334581595966e-06 0.32418956777063296 0.30748243426584837
		4.5176935010635258e-06 0.75280223954649872 1.2684639584860965e-07
		4.5762334581595966e-06 0.32418989517531488 -0.30748243426584837
		4.5762334581595966e-06 0.24216585506700999 -0.16581148183248978
		2.3466599602226874e-06 0.30944031426268537 -0.082905740916244891
		4.5762334581595966e-06 -0.16370234087268618 -0.081851170436343088
		4.5762334581595966e-06 -0.16370234087268618 0.081851170436343088
		;
createNode nurbsCurve -n "Teeth_Upr_Guide_Ctrl_CtrlShape" -p "Teeth_Upr_Guide";
	rename -uid "27154000-0018-1FF3-6621-A96000000F91";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2024/scripts/rigging/Mutant_Tools/Icons/";
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
		0 0.19454680853523612 0
		-1.006805410882013e-09 0.19159132647312063 0.033782597276532739
		-1.9830148542549199e-09 0.18281426176489071 0.066539108280475531
		-2.8989752880930453e-09 0.16848277663085043 0.097273567969958924
		-3.7268474923075738e-09 0.14903166448835795 0.12505254559732676
		-4.441473691153197e-09 0.12505221819264506 0.14903166448835795
		-5.0211764206515582e-09 0.097273567969958924 0.16848277663085043
		-5.4483085684565726e-09 0.066539108280475531 0.18281426176489071
		-5.7098721687029442e-09 0.033782597276532739 0.19159132647312063
		-5.7979440280924536e-09 0 0.19454713593991785
		-5.7098721687029442e-09 -0.033782597276532739 0.19159132647312063
		-5.4483085684565726e-09 -0.066539108280475531 0.18281426176489071
		-5.0211764206515582e-09 -0.097273567969958924 0.16848277663085043
		-4.441473691153197e-09 -0.12505221819264506 0.14903166448835795
		-3.7268474923075738e-09 -0.14903166448835795 0.12505254559732676
		-2.8989752880930453e-09 -0.16848277663085043 0.097273567969958924
		-1.9830148542549199e-09 -0.18281426176489071 0.066539108280475531
		-1.006805410882013e-09 -0.19159132647312063 0.033782597276532739
		0 -0.19454680853523612 0
		0 -0.19159132647312063 -0.033782597276532739
		0 -0.18281426176489071 -0.066539108280475531
		0 -0.16848277663085043 -0.097273567969958924
		0 -0.14903166448835795 -0.12505254559732676
		0 -0.12505221819264506 -0.14903166448835795
		0 -0.097273567969958924 -0.16848277663085043
		0 -0.066539108280475531 -0.18281458916957247
		0 -0.033782597276532739 -0.19159132647312063
		0 0 -0.19454713593991785
		0 0.033782597276532739 -0.19159132647312063
		0 0.066539108280475531 -0.18281458916957247
		0 0.097273567969958924 -0.16848277663085043
		0 0.12505221819264506 -0.14903166448835795
		0 0.14903166448835795 -0.12505254559732676
		0 0.16848277663085043 -0.097273567969958924
		0 0.18281426176489071 -0.066539108280475531
		0 0.19159132647312063 -0.033782597276532739
		0 0.19454680853523612 0
		0.033782597276532739 0.19159132647312063 0
		0.066539108280475531 0.18281426176489071 0
		0.097273567969958924 0.16848277663085043 0
		0.12505254559732676 0.14903166448835795 0
		0.14903166448835795 0.12505221819264506 0
		0.16848277663085043 0.097273567969958924 0
		0.18281426176489071 0.066539108280475531 0
		0.19159132647312063 0.033782597276532739 0
		0.19454680853523612 0 0
		0.19159132647312063 -0.033782597276532739 0
		0.18281426176489071 -0.066539108280475531 0
		0.16848277663085043 -0.097273567969958924 0
		0.14903166448835795 -0.12505221819264506 0
		0.12505254559732676 -0.14903166448835795 0
		0.097273567969958924 -0.16848277663085043 0
		0.066539108280475531 -0.18281426176489071 0
		0.033782597276532739 -0.19159132647312063 0
		0 -0.19454680853523612 0
		-0.033782597276532739 -0.19159132647312063 0
		-0.066539108280475531 -0.18281426176489071 0
		-0.097273567969958924 -0.16848277663085043 0
		-0.12505254559732676 -0.14903166448835795 0
		-0.14903166448835795 -0.12505221819264506 0
		-0.16848277663085043 -0.097273567969958924 0
		-0.18281426176489071 -0.066539108280475531 0
		-0.19159132647312063 -0.033782597276532739 0
		-0.19454713593991785 0 0
		-0.19159132647312063 0.033782597276532739 0
		-0.18281426176489071 0.066539108280475531 0
		-0.16848277663085043 0.097273567969958924 0
		-0.14903166448835795 0.12505221819264506 0
		-0.12505254559732676 0.14903166448835795 0
		-0.097273567969958924 0.16848277663085043 0
		-0.066539108280475531 0.18281426176489071 0
		-0.033782597276532739 0.19159132647312063 0
		0 0.19454680853523612 0
		-1.006805410882013e-09 0.19159132647312063 0.033782597276532739
		-1.9830148542549199e-09 0.18281426176489071 0.066539108280475531
		-2.8989752880930453e-09 0.16848277663085043 0.097273567969958924
		-3.7268474923075738e-09 0.14903166448835795 0.12505254559732676
		-4.441473691153197e-09 0.12505221819264506 0.14903166448835795
		-5.0211764206515582e-09 0.097273567969958924 0.16848277663085043
		-5.4483085684565726e-09 0.066539108280475531 0.18281426176489071
		-5.7098721687029442e-09 0.033782597276532739 0.19159132647312063
		-5.7979440280924536e-09 0 0.19454713593991785
		-0.060118375066767052 0 0.18502522558071716
		-0.11435197838384267 0 0.15739194303672591
		-0.15739194303672591 0 0.11435197838384267
		-0.18502522558071716 0 0.060118375066767052
		-0.19454713593991785 0 0
		-0.18502522558071716 0 -0.060118375066767052
		-0.15739194303672591 0 -0.11435197838384267
		-0.11435197838384267 0 -0.15739194303672591
		-0.060118375066767052 0 -0.18502522558071716
		0 0 -0.19454713593991785
		0.060118375066767052 0 -0.18502522558071716
		0.11435197838384267 0 -0.15739194303672591
		0.15739194303672591 0 -0.11435197838384267
		0.18502522558071716 0 -0.060118375066767052
		0.19454680853523612 0 0
		0.18502522558071716 0 0.060118375066767052
		0.15739194303672591 0 0.11435197838384267
		0.11435197838384267 0 0.15739194303672591
		0.060118375066767052 0 0.18502522558071716
		-5.7979440280924536e-09 0 0.19454713593991785
		;
createNode nurbsCurve -n "Teeth_Upr_Guide_Ctrl_Ctrl_CtrlShape" -p "Teeth_Upr_Guide";
	rename -uid "27154000-0018-1FF3-6621-A96000000F92";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2024/scripts/rigging/Mutant_Tools/Icons/";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 13;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 9 0 no 3
		10 0 1 2 3 4 5 6 7 8 9
		10
		-0.16370234087268618 -0.081851170436343171 -4.5762334581959462e-06
		0.30944031426268537 -0.083788096533548628 -4.5762334580908862e-06
		0.24216585506700999 -0.1658118092371717 -4.5762334581058261e-06
		0.32418956777063301 -0.30748243426584826 -4.5762334580876107e-06
		0.75280223954649872 -1.2684639568145402e-07 -4.5176935008963714e-06
		0.32418989517531488 0.30748243426584837 -4.5762334580876107e-06
		0.24216585506700999 0.16581148183248984 -4.5762334581058261e-06
		0.30944031426268537 0.082905740916245016 -2.3466599601539795e-06
		-0.16370234087268618 0.081851170436343088 -4.5762334581959462e-06
		-0.16370234087268618 -0.081851170436343171 -4.5762334581959462e-06
		;
createNode nurbsCurve -n "Teeth_Upr_Guide_Ctrl_Ctrl_Ctrl_CtrlShape" -p "Teeth_Upr_Guide";
	rename -uid "27154000-0018-1FF3-6621-A96000000F93";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2024/scripts/rigging/Mutant_Tools/Icons/";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 6;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 9 0 no 3
		10 0 1 2 3 4 5 6 7 8 9
		10
		0.081851170436343171 4.5762334581414227e-06 -0.16370234087268618
		0.083788096533548628 4.5762334581409898e-06 0.30944031426268537
		0.1658118092371717 4.5762334581227761e-06 0.24216585506700999
		0.30748243426584826 4.5762334580913198e-06 0.32418956777063301
		1.2684639568145505e-07 4.5176935010635258e-06 0.75280223954649872
		-0.30748243426584837 4.5762334582278692e-06 0.32418989517531488
		-0.16581148183248984 4.5762334581964121e-06 0.24216585506700999
		-0.082905740916245016 2.3466599602410947e-06 0.30944031426268537
		-0.081851170436343088 4.576233458177768e-06 -0.16370234087268618
		0.081851170436343171 4.5762334581414227e-06 -0.16370234087268618
		;
createNode dagContainer -n "Nose_Block" -p "face";
	rename -uid "27154000-0018-1FF3-6621-A96000000F94";
	addAttr -ci true -sn "nts" -ln "notes" -dt "string";
	setAttr ".isc" yes;
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2024/scripts/rigging/Mutant_Tools/Icons/Nose.png";
	setAttr ".ctor" -type "string" "esteban.rodriguez";
	setAttr ".cdat" -type "string" "2022/07/13 12:31:23";
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
		"['L_NoseNostril_Jnt_Auto_Grp', 'R_NoseNostril_Bnd', 'R_NoseNostril_Jnt_Auto_Grp', 'R_NoseNostril_Jnt_Ctrl_tag', 'L_NoseNostrilEnd_Bnd', 'R_NoseNostril_Jnt_Root_Grp', 'L_NoseNostrilEnd_Ctrl', 'Nose_Tip_Jnt', 'L_NoseNostril_Jnt', 'Nose_Top_Jnt_Ctrl_tag', 'L_NoseNostril_Ctrl_Offset_Grp', 'R_NoseNostril_Ctrl_Offset_Grp', 'Nose_Top_Bnd', 'Nose_Base_Jnt_Auto_Grp', 'Nose_Tip_CtrlShape', 'Nose_Origin_Ctrl_Offset_Grp_parentConstraint1', 'Nose_Tip_Bnd', 'L_NoseNostrilEnd_Jnt_Ctrl_tag', 'R_NoseNostrilEnd_Jnt', 'R_NoseNostrilEnd_Bnd', 'Nose_Top_Jnt', 'Nose_Bridge_Bnd', 'Nose_Origin_Jnt_Ctrl_tag', 'L_NoseNostrilEnd_Ctrl_Offset_Grp', 'Nose_Origin_Jnt_Auto_Grp', 'Nose_Bridge_Ctrl', 'Nose_Top_CtrlShape', 'Nose_Bridge_CtrlShape', 'L_NoseNostril_Ctrl', 'Nose_Tip_Jnt_Ctrl_tag', 'L_NoseNostrilEnd_Jnt', 'Nose_Origin_Jnt_Root_Grp', 'Nose_Ctrl_Grp', 'R_NoseNostril_Jnt', 'Nose_Tip_Jnt_Root_Grp', 'R_NoseNostrilEnd_Jnt_Auto_Grp', 'Nose_Bridge_Jnt_Root_Grp', 'Nose_Base_Bnd_parentConstraint1', 'R_NoseNostrilEnd_Jnt_Root_Grp', 'Nose_Origin_Ctrl_Offset_Grp', 'R_NoseNostril_CtrlShape', 'R_NoseNostrilEnd_Bnd_parentConstraint1', 'L_NoseNostrilEnd_Jnt_Auto_Grp', 'R_NoseNostrilEnd_Ctrl_Offset_Grp', 'Nose_Bridge_Bnd_parentConstraint1', 'Nose_Origin_Bnd', 'L_NoseNostril_Jnt_Ctrl_tag', 'Nose_Base_Ctrl', 'Nose_Top_Jnt_Auto_Grp', 'Nose_Base_Jnt_Ctrl_tag', 'Nose_Tip_Jnt_Auto_Grp', 'Nose_Top_Ctrl', 'Nose_Origin_CtrlShape', 'R_NoseNostril_Bnd_parentConstraint1', 'Nose_Base_Jnt', 'Nose_Origin_Ctrl', 'Nose_Bridge_Jnt_Ctrl_tag', 'Nose_Base_CtrlShape', 'Nose_Tip_Ctrl', 'L_NoseNostril_Bnd_parentConstraint1', 'Nose_Tip_Ctrl_Offset_Grp', 'R_NoseNostrilEnd_Jnt_Ctrl_tag', 'L_NoseNostril_Bnd', 'L_NoseNostrilEnd_Jnt_Root_Grp', 'L_NoseNostril_Jnt_Root_Grp', 'Nose_Bridge_Jnt_Auto_Grp', 'L_NoseNostrilEnd_CtrlShape', 'Nose_Top_Jnt_Root_Grp', 'R_NoseNostrilEnd_Ctrl', 'Nose_Bridge_Jnt', 'Nose_Top_Bnd_parentConstraint1', 'R_NoseNostril_Ctrl', 'Nose_Rig_Grp', 'L_NoseNostrilEnd_Bnd_parentConstraint1', 'Nose_Top_Ctrl_Offset_Grp', 'Nose_Bridge_Ctrl_Offset_Grp', 'R_NoseNostrilEnd_CtrlShape', 'Nose_Tip_Bnd_parentConstraint1', 'Nose_Base_Bnd', 'Nose_Base_Jnt_Root_Grp', 'Nose_Origin_Bnd_parentConstraint1', 'Nose_Base_Ctrl_Offset_Grp', 'Nose_Origin_Jnt', 'L_NoseNostril_CtrlShape']");
createNode joint -n "Nose_Origin_Guide" -p "Nose_Block";
	rename -uid "27154000-0018-1FF3-6621-A96000000F95";
	addAttr -ci true -sn "Helper" -ln "Helper" -min 0 -max 1 -en "Hide:Show" -at "enum";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2024/scripts/rigging/Mutant_Tools/Icons/";
	setAttr ".t" -type "double3" 0.068909505750650968 15.063958889207328 10.581458495864252 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr -cb on ".Helper" 1;
createNode nurbsCurve -n "Nose_Origin_Guide_CtrlShape" -p "Nose_Origin_Guide";
	rename -uid "27154000-0018-1FF3-6621-A96000000F96";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2024/scripts/rigging/Mutant_Tools/Icons/";
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
createNode nurbsCurve -n "Nose_Origin_Guide_Ctrl_CtrlShape" -p "Nose_Origin_Guide";
	rename -uid "27154000-0018-1FF3-6621-A96000000F97";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2024/scripts/rigging/Mutant_Tools/Icons/";
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
createNode nurbsCurve -n "Nose_Origin_Guide_Ctrl_Ctrl_CtrlShape" -p "Nose_Origin_Guide";
	rename -uid "27154000-0018-1FF3-6621-A96000000F98";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2024/scripts/rigging/Mutant_Tools/Icons/";
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
createNode nurbsCurve -n "Nose_Origin_Guide_Ctrl_Ctrl_Ctrl_CtrlShape" -p "Nose_Origin_Guide";
	rename -uid "27154000-0018-1FF3-6621-A96000000F99";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2024/scripts/rigging/Mutant_Tools/Icons/";
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
createNode joint -n "Nose_Bridge_Guide" -p "Nose_Origin_Guide";
	rename -uid "27154000-0018-1FF3-6621-A96000000F9A";
	addAttr -ci true -sn "Helper" -ln "Helper" -min 0 -max 1 -en "Hide:Show" -at "enum";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2024/scripts/rigging/Mutant_Tools/Icons/";
	setAttr ".t" -type "double3" -0.057788739793339192 -0.84581940750794615 0.42611323176091354 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr -cb on ".Helper" 1;
createNode nurbsCurve -n "Nose_Bridge_Guide_CtrlShape" -p "Nose_Bridge_Guide";
	rename -uid "27154000-0018-1FF3-6621-A96000000F9B";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2024/scripts/rigging/Mutant_Tools/Icons/";
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
createNode nurbsCurve -n "Nose_Bridge_Guide_Ctrl_CtrlShape" -p "Nose_Bridge_Guide";
	rename -uid "27154000-0018-1FF3-6621-A96000000F9C";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2024/scripts/rigging/Mutant_Tools/Icons/";
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
createNode nurbsCurve -n "Nose_Bridge_Guide_Ctrl_Ctrl_CtrlShape" -p "Nose_Bridge_Guide";
	rename -uid "27154000-0018-1FF3-6621-A96000000F9D";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2024/scripts/rigging/Mutant_Tools/Icons/";
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
createNode nurbsCurve -n "Nose_Bridge_Guide_Ctrl_Ctrl_Ctrl_CtrlShape" -p "Nose_Bridge_Guide";
	rename -uid "27154000-0018-1FF3-6621-A96000000F9E";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2024/scripts/rigging/Mutant_Tools/Icons/";
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
createNode joint -n "Nose_Base_Guide" -p "Nose_Bridge_Guide";
	rename -uid "27154000-0018-1FF3-6621-A96000000F9F";
	addAttr -ci true -sn "Helper" -ln "Helper" -min 0 -max 1 -en "Hide:Show" -at "enum";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2024/scripts/rigging/Mutant_Tools/Icons/";
	setAttr ".t" -type "double3" -0.063920333098493459 -1.3410401435084509 0.70887119100710905 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr -cb on ".Helper" 1;
createNode nurbsCurve -n "Nose_Base_Guide_CtrlShape" -p "Nose_Base_Guide";
	rename -uid "27154000-0018-1FF3-6621-A96000000FA0";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2024/scripts/rigging/Mutant_Tools/Icons/";
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
createNode nurbsCurve -n "Nose_Base_Guide_Ctrl_CtrlShape" -p "Nose_Base_Guide";
	rename -uid "27154000-0018-1FF3-6621-A96000000FA1";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2024/scripts/rigging/Mutant_Tools/Icons/";
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
createNode nurbsCurve -n "Nose_Base_Guide_Ctrl_Ctrl_CtrlShape" -p "Nose_Base_Guide";
	rename -uid "27154000-0018-1FF3-6621-A96000000FA2";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2024/scripts/rigging/Mutant_Tools/Icons/";
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
createNode nurbsCurve -n "Nose_Base_Guide_Ctrl_Ctrl_Ctrl_CtrlShape" -p "Nose_Base_Guide";
	rename -uid "27154000-0018-1FF3-6621-A96000000FA3";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2024/scripts/rigging/Mutant_Tools/Icons/";
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
createNode joint -n "L_NoseNostril_Guide" -p "Nose_Base_Guide";
	rename -uid "27154000-0018-1FF3-6621-A96000000FA4";
	addAttr -ci true -sn "Helper" -ln "Helper" -min 0 -max 1 -en "Hide:Show" -at "enum";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2024/scripts/rigging/Mutant_Tools/Icons/";
	setAttr ".t" -type "double3" 1.5133166036436867 -0.85153178889746073 -0.13045483474707886 ;
	setAttr ".r" -type "double3" 0.19111790470913692 52.120612067773259 0.24213386520506183 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr -cb on ".Helper" 1;
createNode nurbsCurve -n "L_NoseNostril_Guide_CtrlShape" -p "L_NoseNostril_Guide";
	rename -uid "27154000-0018-1FF3-6621-A96000000FA5";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2024/scripts/rigging/Mutant_Tools/Icons/";
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
createNode nurbsCurve -n "L_NoseNostril_Guide_Ctrl_CtrlShape" -p "L_NoseNostril_Guide";
	rename -uid "27154000-0018-1FF3-6621-A96000000FA6";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2024/scripts/rigging/Mutant_Tools/Icons/";
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
createNode nurbsCurve -n "L_NoseNostril_Guide_Ctrl_Ctrl_CtrlShape" -p "L_NoseNostril_Guide";
	rename -uid "27154000-0018-1FF3-6621-A96000000FA7";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2024/scripts/rigging/Mutant_Tools/Icons/";
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
createNode nurbsCurve -n "L_NoseNostril_Guide_Ctrl_Ctrl_Ctrl_CtrlShape" -p "L_NoseNostril_Guide";
	rename -uid "27154000-0018-1FF3-6621-A96000000FA8";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2024/scripts/rigging/Mutant_Tools/Icons/";
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
createNode joint -n "L_NoseNostrilEnd_Guide" -p "L_NoseNostril_Guide";
	rename -uid "27154000-0018-1FF3-6621-A96000000FA9";
	addAttr -ci true -sn "Helper" -ln "Helper" -min 0 -max 1 -en "Hide:Show" -at "enum";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2024/scripts/rigging/Mutant_Tools/Icons/";
	setAttr ".t" -type "double3" 0.98818430238122978 0 -1.7763568394002505e-15 ;
	setAttr ".r" -type "double3" 0.19111790470913689 52.120612067773266 0.24213386520506189 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 -52.12086002307899 -0.14867022954971226 ;
	setAttr -cb on ".Helper" 1;
createNode nurbsCurve -n "L_NoseNostrilEnd_Guide_CtrlShape" -p "L_NoseNostrilEnd_Guide";
	rename -uid "27154000-0018-1FF3-6621-A96000000FAA";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2024/scripts/rigging/Mutant_Tools/Icons/";
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
createNode nurbsCurve -n "L_NoseNostrilEnd_Guide_Ctrl_CtrlShape" -p "L_NoseNostrilEnd_Guide";
	rename -uid "27154000-0018-1FF3-6621-A96000000FAB";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2024/scripts/rigging/Mutant_Tools/Icons/";
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
createNode nurbsCurve -n "L_NoseNostrilEnd_Guide_Ctrl_Ctrl_CtrlShape" -p "L_NoseNostrilEnd_Guide";
	rename -uid "27154000-0018-1FF3-6621-A96000000FAC";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2024/scripts/rigging/Mutant_Tools/Icons/";
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
createNode nurbsCurve -n "L_NoseNostrilEnd_Guide_Ctrl_Ctrl_Ctrl_CtrlShape" -p "L_NoseNostrilEnd_Guide";
	rename -uid "27154000-0018-1FF3-6621-A96000000FAD";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2024/scripts/rigging/Mutant_Tools/Icons/";
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
createNode joint -n "Nose_Tip_Guide" -p "Nose_Base_Guide";
	rename -uid "27154000-0018-1FF3-6621-A96000000FAE";
	addAttr -ci true -sn "Helper" -ln "Helper" -min 0 -max 1 -en "Hide:Show" -at "enum";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2024/scripts/rigging/Mutant_Tools/Icons/";
	setAttr ".t" -type "double3" -0.011235258167628687 -2.0661697600851596 0.84312012042185636 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr -cb on ".Helper" 1;
createNode nurbsCurve -n "Nose_Tip_Guide_CtrlShape" -p "Nose_Tip_Guide";
	rename -uid "27154000-0018-1FF3-6621-A96000000FAF";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2024/scripts/rigging/Mutant_Tools/Icons/";
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
createNode nurbsCurve -n "Nose_Tip_Guide_Ctrl_CtrlShape" -p "Nose_Tip_Guide";
	rename -uid "27154000-0018-1FF3-6621-A96000000FB0";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2024/scripts/rigging/Mutant_Tools/Icons/";
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
createNode nurbsCurve -n "Nose_Tip_Guide_Ctrl_Ctrl_CtrlShape" -p "Nose_Tip_Guide";
	rename -uid "27154000-0018-1FF3-6621-A96000000FB1";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2024/scripts/rigging/Mutant_Tools/Icons/";
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
createNode nurbsCurve -n "Nose_Tip_Guide_Ctrl_Ctrl_Ctrl_CtrlShape" -p "Nose_Tip_Guide";
	rename -uid "27154000-0018-1FF3-6621-A96000000FB2";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2024/scripts/rigging/Mutant_Tools/Icons/";
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
createNode joint -n "R_NoseNostril_Guide" -p "Nose_Base_Guide";
	rename -uid "27154000-0018-1FF3-6621-A96000000FB3";
	addAttr -ci true -sn "Helper" -ln "Helper" -min 0 -max 1 -en "Hide:Show" -at "enum";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2024/scripts/rigging/Mutant_Tools/Icons/";
	setAttr ".t" -type "double3" -1.5025388221781362 -0.92047015289915635 -0.30528519372604102 ;
	setAttr ".r" -type "double3" 7.0340895774285483 -52.591437680788204 -8.8296346880004517 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr -cb on ".Helper" 1;
createNode nurbsCurve -n "R_NoseNostril_Guide_CtrlShape" -p "R_NoseNostril_Guide";
	rename -uid "27154000-0018-1FF3-6621-A96000000FB4";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2024/scripts/rigging/Mutant_Tools/Icons/";
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
createNode nurbsCurve -n "R_NoseNostril_Guide_Ctrl_CtrlShape" -p "R_NoseNostril_Guide";
	rename -uid "27154000-0018-1FF3-6621-A96000000FB5";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2024/scripts/rigging/Mutant_Tools/Icons/";
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
createNode nurbsCurve -n "R_NoseNostril_Guide_Ctrl_Ctrl_CtrlShape" -p "R_NoseNostril_Guide";
	rename -uid "27154000-0018-1FF3-6621-A96000000FB6";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2024/scripts/rigging/Mutant_Tools/Icons/";
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
createNode nurbsCurve -n "R_NoseNostril_Guide_Ctrl_Ctrl_Ctrl_CtrlShape" -p "R_NoseNostril_Guide";
	rename -uid "27154000-0018-1FF3-6621-A96000000FB7";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2024/scripts/rigging/Mutant_Tools/Icons/";
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
createNode joint -n "R_NoseNostrilEnd_Guide" -p "R_NoseNostril_Guide";
	rename -uid "27154000-0018-1FF3-6621-A96000000FB8";
	addAttr -ci true -sn "Helper" -ln "Helper" -min 0 -max 1 -en "Hide:Show" -at "enum";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2024/scripts/rigging/Mutant_Tools/Icons/";
	setAttr ".t" -type "double3" -1.0130533247615405 0 -8.8817841970012523e-16 ;
	setAttr ".r" -type "double3" 7.0340895774285475 -52.591437680788204 -8.8296346880004499 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" -6.5940401619070487e-16 52.920525622157811 5.3505222274312407 ;
	setAttr -cb on ".Helper" 1;
createNode nurbsCurve -n "R_NoseNostrilEnd_Guide_CtrlShape" -p "R_NoseNostrilEnd_Guide";
	rename -uid "27154000-0018-1FF3-6621-A96000000FB9";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2024/scripts/rigging/Mutant_Tools/Icons/";
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
createNode nurbsCurve -n "R_NoseNostrilEnd_Guide_Ctrl_CtrlShape" -p "R_NoseNostrilEnd_Guide";
	rename -uid "27154000-0018-1FF3-6621-A96000000FBA";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2024/scripts/rigging/Mutant_Tools/Icons/";
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
createNode nurbsCurve -n "R_NoseNostrilEnd_Guide_Ctrl_Ctrl_CtrlShape" -p "R_NoseNostrilEnd_Guide";
	rename -uid "27154000-0018-1FF3-6621-A96000000FBB";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2024/scripts/rigging/Mutant_Tools/Icons/";
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
createNode nurbsCurve -n "R_NoseNostrilEnd_Guide_Ctrl_Ctrl_Ctrl_CtrlShape" -p "R_NoseNostrilEnd_Guide";
	rename -uid "27154000-0018-1FF3-6621-A96000000FBC";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2024/scripts/rigging/Mutant_Tools/Icons/";
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
createNode joint -n "Nose_Top_Guide" -p "Nose_Base_Guide";
	rename -uid "27154000-0018-1FF3-6621-A96000000FBD";
	addAttr -ci true -sn "Helper" -ln "Helper" -min 0 -max 1 -en "Hide:Show" -at "enum";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2024/scripts/rigging/Mutant_Tools/Icons/";
	setAttr ".t" -type "double3" -0.030730920615846216 -0.85188886604936442 1.7049900235179773 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr -cb on ".Helper" 1;
createNode nurbsCurve -n "Nose_Top_Guide_CtrlShape" -p "Nose_Top_Guide";
	rename -uid "27154000-0018-1FF3-6621-A96000000FBE";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2024/scripts/rigging/Mutant_Tools/Icons/";
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
createNode nurbsCurve -n "Nose_Top_Guide_Ctrl_CtrlShape" -p "Nose_Top_Guide";
	rename -uid "27154000-0018-1FF3-6621-A96000000FBF";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2024/scripts/rigging/Mutant_Tools/Icons/";
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
createNode nurbsCurve -n "Nose_Top_Guide_Ctrl_Ctrl_CtrlShape" -p "Nose_Top_Guide";
	rename -uid "27154000-0018-1FF3-6621-A96000000FC0";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2024/scripts/rigging/Mutant_Tools/Icons/";
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
createNode nurbsCurve -n "Nose_Top_Guide_Ctrl_Ctrl_Ctrl_CtrlShape" -p "Nose_Top_Guide";
	rename -uid "27154000-0018-1FF3-6621-A96000000FC1";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2024/scripts/rigging/Mutant_Tools/Icons/";
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
createNode transform -n "null" -p "Mutant_Build";
	rename -uid "27154000-0018-1FF3-6621-A96000000FC2";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2024/scripts/rigging/Mutant_Tools/Icons/";
	setAttr ".t" -type "double3" 0 148.19816716577168 0 ;
createNode dagContainer -n "NullJnt_Block" -p "null";
	rename -uid "27154000-0018-1FF3-6621-A96000000FC3";
	addAttr -ci true -sn "nts" -ln "notes" -dt "string";
	setAttr ".isc" yes;
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2024/scripts/rigging/Mutant_Tools/Icons/CODE.png";
	setAttr ".ctor" -type "string" "esteban.rodriguez";
	setAttr ".cdat" -type "string" "2022/04/06 09:53:31";
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
	setAttr ".nts" -type "string" "['Null_Local_Bnd']";
createNode transform -n "corectives" -p "Mutant_Build";
	rename -uid "27154000-0018-1FF3-6621-A96000000FC4";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2024/scripts/rigging/Mutant_Tools/Icons/";
	setAttr ".t" -type "double3" 0 148.19816716577168 0 ;
createNode dagContainer -n "Correctives_Block" -p "corectives";
	rename -uid "27154000-0018-1FF3-6621-A96000000FC5";
	addAttr -ci true -sn "nts" -ln "notes" -dt "string";
	setAttr ".isc" yes;
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2024/scripts/rigging/Mutant_Tools/Icons/Blendshape.png";
	setAttr ".ctor" -type "string" "esteban.rodriguez";
	setAttr ".cdat" -type "string" "2022/07/12 14:56:12";
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
	setAttr ".nts" -type "string" "['Correctives_BSP']";
createNode dagContainer -n "reorder_Block" -p "corectives";
	rename -uid "27154000-0018-1FF3-6621-A96000000FC6";
	addAttr -ci true -sn "nts" -ln "notes" -dt "string";
	setAttr ".isc" yes;
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2024/scripts/rigging/Mutant_Tools/Icons/CODE.png";
	setAttr ".ctor" -type "string" "esteban.rodriguez";
	setAttr ".cdat" -type "string" "2022/07/12 15:18:47";
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
createNode transform -n "reorder_Loc" -p "reorder_Block";
	rename -uid "27154000-0018-1FF3-6621-A96000000FC7";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2024/scripts/rigging/Mutant_Tools/Icons/";
	setAttr ".t" -type "double3" 0 -148.19816716577168 0 ;
createNode locator -n "reorder_LocShape" -p "reorder_Loc";
	rename -uid "27154000-0018-1FF3-6621-A96000000FC8";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2024/scripts/rigging/Mutant_Tools/Icons/";
	setAttr -k off ".v";
createNode transform -n "skin" -p "Mutant_Build";
	rename -uid "27154000-0018-1FF3-6621-A96000000FC9";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2024/scripts/rigging/Mutant_Tools/Icons/";
	setAttr ".t" -type "double3" 0 148.19816716577168 0 ;
createNode dagContainer -n "BindSkull_Block" -p "skin";
	rename -uid "27154000-0018-1FF3-6621-A96000000FCA";
	addAttr -ci true -sn "nts" -ln "notes" -dt "string";
	setAttr ".isc" yes;
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2024/scripts/rigging/Mutant_Tools/Icons/Skin.png";
	setAttr ".ctor" -type "string" "Stellar Creative lab";
	setAttr ".cdat" -type "string" "2022/04/29 10:53:38";
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
	setAttr ".nts" -type "string" "['skinCluster13', 'BindSkull', 'bindPose13']";
createNode dagContainer -n "BindEyelids_Block" -p "skin";
	rename -uid "27154000-0018-1FF3-6621-A96000000FCB";
	addAttr -ci true -sn "nts" -ln "notes" -dt "string";
	setAttr ".isc" yes;
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2024/scripts/rigging/Mutant_Tools/Icons/Skin.png";
	setAttr ".ctor" -type "string" "Stellar Creative lab";
	setAttr ".cdat" -type "string" "2022/04/29 10:53:45";
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
	setAttr ".nts" -type "string" "['skinCluster14', 'BindEyelids']";
createNode dagContainer -n "BindLips_Block" -p "skin";
	rename -uid "27154000-0018-1FF3-6621-A96000000FCC";
	addAttr -ci true -sn "nts" -ln "notes" -dt "string";
	setAttr ".isc" yes;
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2024/scripts/rigging/Mutant_Tools/Icons/Skin.png";
	setAttr ".ctor" -type "string" "Stellar Creative lab";
	setAttr ".cdat" -type "string" "2022/04/29 10:53:51";
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
	setAttr ".nts" -type "string" "['BindLips', 'skinCluster15', 'BodyLipsShapeOrig1']";
createNode dagContainer -n "BindBrows_Block" -p "skin";
	rename -uid "27154000-0018-1FF3-6621-A96000000FCD";
	addAttr -ci true -sn "nts" -ln "notes" -dt "string";
	setAttr ".isc" yes;
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2024/scripts/rigging/Mutant_Tools/Icons/Skin.png";
	setAttr ".ctor" -type "string" "Stellar Creative lab";
	setAttr ".cdat" -type "string" "2022/04/29 10:53:56";
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
	setAttr ".nts" -type "string" "['BodyBrowsShapeOrig1', 'skinCluster16', 'BindBrows']";
createNode dagContainer -n "BindCheeks_Block" -p "skin";
	rename -uid "27154000-0018-1FF3-6621-A96000000FCE";
	addAttr -ci true -sn "nts" -ln "notes" -dt "string";
	setAttr ".isc" yes;
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2024/scripts/rigging/Mutant_Tools/Icons/Skin.png";
	setAttr ".ctor" -type "string" "Stellar Creative lab";
	setAttr ".cdat" -type "string" "2022/04/29 10:54:06";
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
	setAttr ".nts" -type "string" "['skinCluster17', 'BodyCheeksShapeOrig1', 'BindCheeks']";
createNode dagContainer -n "BindJaw_Block" -p "skin";
	rename -uid "27154000-0018-1FF3-6621-A96000000FCF";
	addAttr -ci true -sn "nts" -ln "notes" -dt "string";
	setAttr ".isc" yes;
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2024/scripts/rigging/Mutant_Tools/Icons/Skin.png";
	setAttr ".ctor" -type "string" "Stellar Creative lab";
	setAttr ".cdat" -type "string" "2022/04/29 10:54:12";
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
	setAttr ".nts" -type "string" "['skinCluster18', 'BindJaw', 'BodyJawShapeOrig1']";
createNode dagContainer -n "BindNose_Block" -p "skin";
	rename -uid "27154000-0018-1FF3-6621-A96000000FD0";
	addAttr -ci true -sn "nts" -ln "notes" -dt "string";
	setAttr ".isc" yes;
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2024/scripts/rigging/Mutant_Tools/Icons/Skin.png";
	setAttr ".ctor" -type "string" "esteban.rodriguez";
	setAttr ".cdat" -type "string" "2022/10/07 11:58:49";
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
	setAttr ".nts" -type "string" "['skinCluster19', 'BodyNoseShapeOrig1', 'BindNose']";
createNode dagContainer -n "BindMouthUp_Block" -p "skin";
	rename -uid "27154000-0018-1FF3-6621-A96000000FD1";
	addAttr -ci true -sn "nts" -ln "notes" -dt "string";
	setAttr ".isc" yes;
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2024/scripts/rigging/Mutant_Tools/Icons/Skin.png";
	setAttr ".ctor" -type "string" "Stellar Creative lab";
	setAttr ".cdat" -type "string" "2022/04/29 10:57:20";
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
	setAttr ".nts" -type "string" "['BodyMouthUpShapeOrig1', 'BindMouthUp', 'skinCluster20']";
createNode dagContainer -n "BindMouthDown_Block" -p "skin";
	rename -uid "27154000-0018-1FF3-6621-A96000000FD2";
	addAttr -ci true -sn "nts" -ln "notes" -dt "string";
	setAttr ".isc" yes;
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2024/scripts/rigging/Mutant_Tools/Icons/Skin.png";
	setAttr ".ctor" -type "string" "Stellar Creative lab";
	setAttr ".cdat" -type "string" "2022/04/29 10:57:26";
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
	setAttr ".nts" -type "string" "['skinCluster21', 'BindMouthDown', 'BodyMouthDownShapeOrig1']";
createNode dagContainer -n "BindMouthWide_Block" -p "skin";
	rename -uid "27154000-0018-1FF3-6621-A96000000FD3";
	addAttr -ci true -sn "nts" -ln "notes" -dt "string";
	setAttr ".isc" yes;
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2024/scripts/rigging/Mutant_Tools/Icons/Skin.png";
	setAttr ".ctor" -type "string" "Stellar Creative lab";
	setAttr ".cdat" -type "string" "2022/04/29 10:57:33";
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
	setAttr ".nts" -type "string" "['BodyMouthWideShapeOrig1', 'BindMouthWide', 'skinCluster22']";
createNode dagContainer -n "BindMouthNarrow_Block" -p "skin";
	rename -uid "27154000-0018-1FF3-6621-A96000000FD4";
	addAttr -ci true -sn "nts" -ln "notes" -dt "string";
	setAttr ".isc" yes;
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2024/scripts/rigging/Mutant_Tools/Icons/Skin.png";
	setAttr ".ctor" -type "string" "Stellar Creative lab";
	setAttr ".cdat" -type "string" "2022/04/29 10:57:40";
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
	setAttr ".nts" -type "string" "['BodyMouthNarrowShapeOrig1', 'skinCluster23', 'BindMouthNarrow']";
createNode transform -n "data" -p "Mutant_Build";
	rename -uid "27154000-0018-1FF3-6621-A96000000FD5";
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2024/scripts/rigging/Mutant_Tools/Icons/";
	setAttr ".t" -type "double3" 0 148.19816716577168 0 ;
createNode dagContainer -n "Load_Ctrls_Block" -p "data";
	rename -uid "27154000-0018-1FF3-6621-A96000000FD6";
	addAttr -ci true -sn "nts" -ln "notes" -dt "string";
	setAttr ".isc" yes;
	setAttr ".icn" -type "string" "C:/Users/rodri/Documents/maya/2024/scripts/rigging/Mutant_Tools/Icons/Controller.png";
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
	rename -uid "27154000-0018-1FF3-6621-A96200001D7C";
	setAttr ".ihi" 0;
createNode network -n "SausageFaceTemplate_BaseA_Config";
	rename -uid "27154000-0018-1FF3-6621-A96200001BD0";
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
	rename -uid "27154000-0018-1FF3-6621-A96200001C42";
	setAttr ".ihi" 0;
	setAttr -s 2 ".hyp";
createNode network -n "VisAttrs_Config";
	rename -uid "27154000-0018-1FF3-6621-A96200001CAF";
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
createNode hyperLayout -n "SausageFaceTemplate_hyperLayout39";
	rename -uid "27154000-0018-1FF3-6621-A96200001B8C";
	setAttr ".ihi" 0;
createNode network -n "SkullLocal_Config";
	rename -uid "27154000-0018-1FF3-6621-A96200001EF3";
	addAttr -ci true -sn "precode" -ln "precode" -dt "string";
	addAttr -ci true -sn "Build_Command" -ln "Build_Command" -dt "string";
	addAttr -ci true -sn "Import_Command" -ln "Import_Command" -dt "string";
	addAttr -ci true -sn "SetGeo" -ln "SetGeo" -dt "string";
	addAttr -ci true -sn "NewNames" -ln "NewNames" -dt "string";
	addAttr -ci true -sn "Help" -ln "Help" -dt "string";
	addAttr -ci true -sn "postcode" -ln "postcode" -dt "string";
	setAttr ".precode" -type "string" "";
	setAttr -l on ".Build_Command" -type "string" "exec_locals.build_locals_block()";
	setAttr -l on ".Import_Command" -type "string" "import exec_locals";
	setAttr ".SetGeo" -type "string" "Body_Geo";
	setAttr ".NewNames" -type "string" "BodySkull";
	setAttr ".Help" -type "string" "Create Local Duplicates for Main Geo and Atach via BlendShape, separate names with comas ','";
	setAttr ".postcode" -type "string" "";
createNode hyperLayout -n "SausageFaceTemplate_hyperLayout17";
	rename -uid "27154000-0018-1FF3-6621-A96200001BBA";
	setAttr ".ihi" 0;
createNode network -n "Locals_Config";
	rename -uid "27154000-0018-1FF3-6621-A96200001B2D";
	addAttr -ci true -sn "precode" -ln "precode" -dt "string";
	addAttr -ci true -sn "Build_Command" -ln "Build_Command" -dt "string";
	addAttr -ci true -sn "Import_Command" -ln "Import_Command" -dt "string";
	addAttr -ci true -sn "SetGeo" -ln "SetGeo" -dt "string";
	addAttr -ci true -sn "NewNames" -ln "NewNames" -dt "string";
	addAttr -ci true -sn "Help" -ln "Help" -dt "string";
	addAttr -ci true -sn "postcode" -ln "postcode" -dt "string";
	setAttr ".precode" -type "string" "";
	setAttr -l on ".Build_Command" -type "string" "exec_locals.build_locals_block()";
	setAttr -l on ".Import_Command" -type "string" "import exec_locals";
	setAttr ".SetGeo" -type "string" "BodySkull";
	setAttr ".NewNames" -type "string" "BodyEyes,BodyLips,BodyBrows,BodyCheeks,BodyJaw,BodyNose,BodyMouthUp,BodyMouthDown,BodyMouthWide,BodyMouthNarrow,BodySquash";
	setAttr ".Help" -type "string" "Create Local Duplicates for Main Geo and Atach via BlendShape, separate names with comas ','";
	setAttr ".postcode" -type "string" "";
createNode hyperLayout -n "hyperLayout9";
	rename -uid "27154000-0018-1FF3-6621-A96200001C43";
	setAttr ".ihi" 0;
	setAttr -s 10 ".hyp";
createNode network -n "Skull_Config";
	rename -uid "27154000-0018-1FF3-6621-A96200001C12";
	addAttr -ci true -sn "precode" -ln "precode" -dt "string";
	addAttr -ci true -sn "Build_Command" -ln "Build_Command" -dt "string";
	addAttr -ci true -sn "Import_Command" -ln "Import_Command" -dt "string";
	addAttr -ci true -sn "SetParent" -ln "SetParent" -dt "string";
	addAttr -ci true -sn "CtrlType" -ln "CtrlType" -min 0 -max 4 -en "cube:square:circleX:circleY:circleZ" 
		-at "enum";
	addAttr -ci true -sn "CtrlSize" -ln "CtrlSize" -dv 4 -min 1 -max 20 -at "long";
	addAttr -ci true -sn "Help" -ln "Help" -dt "string";
	addAttr -ci true -sn "SetAttrsPosition" -ln "SetAttrsPosition" -dt "string";
	addAttr -ci true -sn "CtrlColor" -ln "CtrlColor" -min 0 -max 7 -en "lightBlue:blue:white:purple:green:red:yellow:grey" 
		-at "enum";
	addAttr -ci true -sn "postcode" -ln "postcode" -dt "string";
	setAttr ".precode" -type "string" "";
	setAttr -l on ".Build_Command" -type "string" "exec_skull.build_skull_block()";
	setAttr -l on ".Import_Command" -type "string" "import exec_skull";
	setAttr ".SetParent" -type "string" "new_locator";
	setAttr -cb on ".CtrlType";
	setAttr -k on ".CtrlSize" 1;
	setAttr ".Help" -type "string" "Possible parent: Head_Ctrl ";
	setAttr ".SetAttrsPosition" -type "string" "Vis_Ctrl";
	setAttr -cb on ".CtrlColor";
	setAttr ".postcode" -type "string" "";
createNode hyperLayout -n "hyperLayout49";
	rename -uid "27154000-0018-1FF3-6621-A96200001FDC";
	setAttr ".ihi" 0;
createNode network -n "L_Eyelids_Config";
	rename -uid "27154000-0018-1FF3-6621-A96200001E04";
	addAttr -ci true -sn "precode" -ln "precode" -dt "string";
	addAttr -ci true -sn "Build_Command" -ln "Build_Command" -dt "string";
	addAttr -ci true -sn "Import_Command" -ln "Import_Command" -dt "string";
	addAttr -ci true -sn "SetParent" -ln "SetParent" -dt "string";
	addAttr -ci true -sn "Mirror" -ln "Mirror" -min 0 -max 2 -en "True:False:Right_Only" 
		-at "enum";
	addAttr -ci true -sn "SetUpperEdge" -ln "SetUpperEdge" -dt "string";
	addAttr -ci true -sn "CtrlSize" -ln "CtrlSize" -dv 4 -min 1 -max 20 -at "long";
	addAttr -ci true -sn "Help" -ln "Help" -dt "string";
	addAttr -ci true -sn "SetAttrsPosition" -ln "SetAttrsPosition" -dt "string";
	addAttr -ci true -sn "SetEyePivot" -ln "SetEyePivot" -dt "string";
	addAttr -ci true -sn "LimitCtrl" -ln "LimitCtrl" -min 0 -max 1 -at "bool";
	addAttr -ci true -sn "SetLowerEdge" -ln "SetLowerEdge" -dt "string";
	addAttr -ci true -sn "postcode" -ln "postcode" -dt "string";
	setAttr ".precode" -type "string" "";
	setAttr -l on ".Build_Command" -type "string" "exec_eyelids.build_eyelids_block()";
	setAttr -l on ".Import_Command" -type "string" "import exec_eyelids";
	setAttr ".SetParent" -type "string" "Skull_Upr_Ctrl";
	setAttr -cb on ".Mirror";
	setAttr ".SetUpperEdge" -type "string" "Body_Geo.e[11157], Body_Geo.e[11159], Body_Geo.e[11164], Body_Geo.e[11167], Body_Geo.e[11170], Body_Geo.e[11173], Body_Geo.e[11176], Body_Geo.e[11179], Body_Geo.e[11181], Body_Geo.e[11184], Body_Geo.e[11472], Body_Geo.e[11537], Body_Geo.e[11539]";
	setAttr -k on ".CtrlSize";
	setAttr ".Help" -type "string" "Create eyelids rig, based on Marco Giordano tutorial\n";
	setAttr ".SetAttrsPosition" -type "string" "L_Eyelids_Scale_Ctrl";
	setAttr ".SetEyePivot" -type "string" "Eye_Pivot";
	setAttr -cb on ".LimitCtrl";
	setAttr ".SetLowerEdge" -type "string" "Body_Geo.e[11136], Body_Geo.e[11138], Body_Geo.e[11142], Body_Geo.e[11145], Body_Geo.e[11149:11150], Body_Geo.e[11154], Body_Geo.e[11188], Body_Geo.e[11192], Body_Geo.e[11195], Body_Geo.e[11197], Body_Geo.e[11436]";
	setAttr ".postcode" -type "string" "";
createNode hyperLayout -n "hyperLayout44";
	rename -uid "27154000-0018-1FF3-6621-A96200001FD8";
	setAttr ".ihi" 0;
	setAttr -s 2 ".hyp";
createNode network -n "L_Orbicularis_Config";
	rename -uid "27154000-0018-1FF3-6621-A96200001BA2";
	addAttr -ci true -sn "precode" -ln "precode" -dt "string";
	addAttr -ci true -sn "Build_Command" -ln "Build_Command" -dt "string";
	addAttr -ci true -sn "Import_Command" -ln "Import_Command" -dt "string";
	addAttr -ci true -sn "SetParent" -ln "SetParent" -dt "string";
	addAttr -ci true -sn "SetGeo" -ln "SetGeo" -dt "string";
	addAttr -ci true -sn "Help" -ln "Help" -dt "string";
	addAttr -ci true -sn "postcode" -ln "postcode" -dt "string";
	setAttr ".precode" -type "string" "";
	setAttr -l on ".Build_Command" -type "string" "exec_orbicularis.build_orbicularis_block()";
	setAttr -l on ".Import_Command" -type "string" "import exec_orbicularis";
	setAttr ".SetParent" -type "string" "Skull_Upr_Ctrl";
	setAttr ".SetGeo" -type "string" "BodyEyes";
	setAttr ".Help" -type "string" "Will create Orbicularis Outside Eyelids Rig";
	setAttr ".postcode" -type "string" "";
createNode hyperLayout -n "hyperLayout10";
	rename -uid "27154000-0018-1FF3-6621-A96200001D65";
	setAttr ".ihi" 0;
	setAttr -s 2 ".hyp";
createNode network -n "L_Brow_Config";
	rename -uid "27154000-0018-1FF3-6621-A963000020F9";
	addAttr -ci true -sn "precode" -ln "precode" -dt "string";
	addAttr -ci true -sn "Build_Command" -ln "Build_Command" -dt "string";
	addAttr -ci true -sn "Import_Command" -ln "Import_Command" -dt "string";
	addAttr -ci true -sn "SetParent" -ln "SetParent" -dt "string";
	addAttr -ci true -sn "Mirror" -ln "Mirror" -min 0 -max 2 -en "True:False:Right_Only" 
		-at "enum";
	addAttr -ci true -sn "SetAttrsPosition" -ln "SetAttrsPosition" -dt "string";
	addAttr -ci true -sn "Help" -ln "Help" -dt "string";
	addAttr -ci true -sn "CtrlSize" -ln "CtrlSize" -dv 4 -min 1 -max 20 -at "long";
	addAttr -ci true -sn "postcode" -ln "postcode" -dt "string";
	setAttr ".precode" -type "string" "";
	setAttr -l on ".Build_Command" -type "string" "exec_brows.build_brows_block()";
	setAttr -l on ".Import_Command" -type "string" "import exec_brows";
	setAttr ".SetParent" -type "string" "Skull_Upr_Ctrl";
	setAttr -cb on ".Mirror";
	setAttr ".SetAttrsPosition" -type "string" "L_Brow_Ctrl";
	setAttr ".Help" -type "string" "Will crete brows rig system";
	setAttr -k on ".CtrlSize" 1;
	setAttr ".postcode" -type "string" "";
createNode hyperLayout -n "hyperLayout48";
	rename -uid "27154000-0018-1FF3-6621-A96200001C49";
	setAttr ".ihi" 0;
	setAttr -s 9 ".hyp";
createNode network -n "L_Cheecks_Config";
	rename -uid "27154000-0018-1FF3-6621-A96200001B70";
	addAttr -ci true -sn "precode" -ln "precode" -dt "string";
	addAttr -ci true -sn "Build_Command" -ln "Build_Command" -dt "string";
	addAttr -ci true -sn "Import_Command" -ln "Import_Command" -dt "string";
	addAttr -ci true -sn "SetParent" -ln "SetParent" -dt "string";
	addAttr -ci true -sn "SetAttrsPosition" -ln "SetAttrsPosition" -dt "string";
	addAttr -ci true -sn "Mirror" -ln "Mirror" -min 0 -max 2 -en "True:False:Right_Only" 
		-at "enum";
	addAttr -ci true -sn "CtrlSize" -ln "CtrlSize" -dv 4 -min 1 -max 20 -at "long";
	addAttr -ci true -sn "Help" -ln "Help" -dt "string";
	addAttr -ci true -sn "postcode" -ln "postcode" -dt "string";
	setAttr ".precode" -type "string" "";
	setAttr -l on ".Build_Command" -type "string" "exec_cheeks_advance.build_cheek_block()";
	setAttr -l on ".Import_Command" -type "string" "import exec_cheeks_advance";
	setAttr ".SetParent" -type "string" "Skull_Lwr_Ctrl";
	setAttr ".SetAttrsPosition" -type "string" "L_Cheecks_Main_Ctrl";
	setAttr -cb on ".Mirror";
	setAttr -k on ".CtrlSize";
	setAttr ".Help" -type "string" "Will crete cheek rig system";
	setAttr ".postcode" -type "string" "";
createNode hyperLayout -n "hyperLayout50";
	rename -uid "27154000-0018-1FF3-6621-A96200001F3F";
	setAttr ".ihi" 0;
	setAttr -s 10 ".hyp";
createNode network -n "Lips_Config";
	rename -uid "27154000-0018-1FF3-6621-A96200001CCE";
	addAttr -ci true -sn "precode" -ln "precode" -dt "string";
	addAttr -ci true -sn "Build_Command" -ln "Build_Command" -dt "string";
	addAttr -ci true -sn "Import_Command" -ln "Import_Command" -dt "string";
	addAttr -ci true -sn "SetParent" -ln "SetParent" -dt "string";
	addAttr -ci true -sn "SetUpperEdge" -ln "SetUpperEdge" -dt "string";
	addAttr -ci true -sn "CtrlSize" -ln "CtrlSize" -dv 4 -min 1 -max 20 -at "long";
	addAttr -ci true -sn "Help" -ln "Help" -dt "string";
	addAttr -ci true -sn "SetAttrsPosition" -ln "SetAttrsPosition" -dt "string";
	addAttr -ci true -sn "SetLowerEdge" -ln "SetLowerEdge" -dt "string";
	addAttr -ci true -sn "postcode" -ln "postcode" -dt "string";
	setAttr ".precode" -type "string" "";
	setAttr -l on ".Build_Command" -type "string" "exec_ribbon_mouth.build_mouth_block()";
	setAttr -l on ".Import_Command" -type "string" "import exec_ribbon_mouth";
	setAttr ".SetParent" -type "string" "Skull_Lwr_Ctrl";
	setAttr ".SetUpperEdge" -type "string" "Body_Geo.e[10543], Body_Geo.e[10545], Body_Geo.e[10551], Body_Geo.e[10553], Body_Geo.e[10614], Body_Geo.e[10627], Body_Geo.e[11609], Body_Geo.e[11616], Body_Geo.e[11894], Body_Geo.e[11896], Body_Geo.e[21930], Body_Geo.e[21955], Body_Geo.e[22401:22402], Body_Geo.e[22405:22406]";
	setAttr -k on ".CtrlSize";
	setAttr ".Help" -type "string" "Create ribbons mouth lips rig\n";
	setAttr ".SetAttrsPosition" -type "string" "Lips_Center_Ctrl";
	setAttr ".SetLowerEdge" -type "string" "Body_Geo.e[10556], Body_Geo.e[10562], Body_Geo.e[10564], Body_Geo.e[10569], Body_Geo.e[10636], Body_Geo.e[10638], Body_Geo.e[11620], Body_Geo.e[11627], Body_Geo.e[11897], Body_Geo.e[11899], Body_Geo.e[11905], Body_Geo.e[21940], Body_Geo.e[21982], Body_Geo.e[22409:22410], Body_Geo.e[22413:22414]";
	setAttr ".postcode" -type "string" "";
createNode hyperLayout -n "hyperLayout2";
	rename -uid "27154000-0018-1FF3-6621-A96200001C41";
	setAttr ".ihi" 0;
	setAttr -s 15 ".hyp";
createNode network -n "Jaw_Config";
	rename -uid "27154000-0018-1FF3-6621-A9620000203F";
	addAttr -ci true -sn "precode" -ln "precode" -dt "string";
	addAttr -ci true -sn "Build_Command" -ln "Build_Command" -dt "string";
	addAttr -ci true -sn "Import_Command" -ln "Import_Command" -dt "string";
	addAttr -ci true -sn "SetParent" -ln "SetParent" -dt "string";
	addAttr -ci true -sn "SetAttrsPosition" -ln "SetAttrsPosition" -dt "string";
	addAttr -ci true -sn "Help" -ln "Help" -dt "string";
	addAttr -ci true -sn "CtrlType" -ln "CtrlType" -min 0 -max 3 -en "circleY:circleX:circleZ:square" 
		-at "enum";
	addAttr -ci true -sn "CtrlSize" -ln "CtrlSize" -dv 4 -min 1 -max 20 -at "long";
	addAttr -ci true -sn "postcode" -ln "postcode" -dt "string";
	setAttr ".precode" -type "string" "";
	setAttr -l on ".Build_Command" -type "string" "exec_jaw.build_jaw_block()";
	setAttr -l on ".Import_Command" -type "string" "import exec_jaw";
	setAttr ".SetParent" -type "string" "Skull_Lwr_Ctrl";
	setAttr ".SetAttrsPosition" -type "string" "Vis_Ctrl";
	setAttr ".Help" -type "string" "Possible parent: JawEnd_Jnt ";
	setAttr -cb on ".CtrlType";
	setAttr -k on ".CtrlSize" 1;
	setAttr ".postcode" -type "string" "";
createNode hyperLayout -n "hyperLayout45";
	rename -uid "27154000-0018-1FF3-6621-A96200001FD7";
	setAttr ".ihi" 0;
	setAttr -s 8 ".hyp";
createNode network -n "Commissures_Config";
	rename -uid "27154000-0018-1FF3-6621-A96200001D74";
	addAttr -ci true -sn "precode" -ln "precode" -dt "string";
	addAttr -ci true -sn "Build_Command" -ln "Build_Command" -dt "string";
	addAttr -ci true -sn "Import_Command" -ln "Import_Command" -dt "string";
	addAttr -ci true -sn "LeftCornerCtrl" -ln "LeftCornerCtrl" -dt "string";
	addAttr -ci true -sn "RightCornerCtrl" -ln "RightCornerCtrl" -dt "string";
	addAttr -ci true -sn "Help" -ln "Help" -dt "string";
	addAttr -ci true -sn "postcode" -ln "postcode" -dt "string";
	setAttr ".precode" -type "string" "";
	setAttr -l on ".Build_Command" -type "string" "exec_commissures.build_commissures_block()";
	setAttr -l on ".Import_Command" -type "string" "import exec_commissures";
	setAttr ".LeftCornerCtrl" -type "string" "L_Lips_Main_Ctrl";
	setAttr ".RightCornerCtrl" -type "string" "R_Lips_Main_Ctrl";
	setAttr ".Help" -type "string" "This will create a commissures slide systeam for the lips blendshapes";
	setAttr ".postcode" -type "string" "";
createNode hyperLayout -n "SausageFaceTemplate_hyperLayout14";
	rename -uid "27154000-0018-1FF3-6621-A96200001BBB";
	setAttr ".ihi" 0;
	setAttr -s 25 ".hyp";
createNode network -n "Tongue_Config";
	rename -uid "27154000-0018-1FF3-6621-A963000020AA";
	addAttr -ci true -sn "precode" -ln "precode" -dt "string";
	addAttr -ci true -sn "Build_Command" -ln "Build_Command" -dt "string";
	addAttr -ci true -sn "Import_Command" -ln "Import_Command" -dt "string";
	addAttr -ci true -sn "SetParent" -ln "SetParent" -dt "string";
	addAttr -ci true -sn "SetAttrsPosition" -ln "SetAttrsPosition" -dt "string";
	addAttr -ci true -sn "CtrlColor" -ln "CtrlColor" -min 0 -max 7 -en "lightBlue:blue:white:purple:green:red:yellow:grey" 
		-at "enum";
	addAttr -ci true -sn "Help" -ln "Help" -dt "string";
	addAttr -ci true -sn "CtrlSize" -ln "CtrlSize" -dv 4 -min 1 -max 20 -at "long";
	addAttr -ci true -sn "postcode" -ln "postcode" -dt "string";
	setAttr ".precode" -type "string" "";
	setAttr -l on ".Build_Command" -type "string" "exec_tongue.build_tongue_block()";
	setAttr -l on ".Import_Command" -type "string" "import exec_tongue";
	setAttr ".SetParent" -type "string" "Jaw_Ctrl";
	setAttr ".SetAttrsPosition" -type "string" "Vis_Ctrl";
	setAttr -cb on ".CtrlColor";
	setAttr ".Help" -type "string" "Create Tongue System";
	setAttr -k on ".CtrlSize" 1;
	setAttr ".postcode" -type "string" "";
createNode hyperLayout -n "SausageFaceTemplate_hyperLayout19";
	rename -uid "27154000-0018-1FF3-6621-A96200001BBD";
	setAttr ".ihi" 0;
	setAttr -s 10 ".hyp";
createNode network -n "Teeth_Config";
	rename -uid "27154000-0018-1FF3-6621-A96200001CA7";
	addAttr -ci true -sn "precode" -ln "precode" -dt "string";
	addAttr -ci true -sn "Build_Command" -ln "Build_Command" -dt "string";
	addAttr -ci true -sn "Import_Command" -ln "Import_Command" -dt "string";
	addAttr -ci true -sn "SetLwrParent" -ln "SetLwrParent" -dt "string";
	addAttr -ci true -sn "SetUprParent" -ln "SetUprParent" -dt "string";
	addAttr -ci true -sn "CtrlSize" -ln "CtrlSize" -dv 4 -min 1 -max 20 -at "long";
	addAttr -ci true -sn "LwrTeeth" -ln "LwrTeeth" -min 0 -max 1 -at "bool";
	addAttr -ci true -sn "Help" -ln "Help" -dt "string";
	addAttr -ci true -sn "SetAttrsPosition" -ln "SetAttrsPosition" -dt "string";
	addAttr -ci true -sn "UprTeeth" -ln "UprTeeth" -min 0 -max 1 -at "bool";
	addAttr -ci true -sn "postcode" -ln "postcode" -dt "string";
	setAttr ".precode" -type "string" "";
	setAttr -l on ".Build_Command" -type "string" "exec_teeth.build_teeth_block()";
	setAttr -l on ".Import_Command" -type "string" "import exec_teeth";
	setAttr ".SetLwrParent" -type "string" "Jaw_Ctrl";
	setAttr ".SetUprParent" -type "string" "Skull_Lwr_Ctrl";
	setAttr -k on ".CtrlSize" 1;
	setAttr -cb on ".LwrTeeth" yes;
	setAttr ".Help" -type "string" "Will Create Teeth System";
	setAttr ".SetAttrsPosition" -type "string" "Vis_Ctrl";
	setAttr -cb on ".UprTeeth" yes;
	setAttr ".postcode" -type "string" "";
createNode hyperLayout -n "hyperLayout43";
	rename -uid "27154000-0018-1FF3-6621-A96200001FDA";
	setAttr ".ihi" 0;
	setAttr -s 45 ".hyp";
createNode network -n "Nose_Config";
	rename -uid "27154000-0018-1FF3-6621-A96200001EC2";
	addAttr -ci true -sn "precode" -ln "precode" -dt "string";
	addAttr -ci true -sn "Build_Command" -ln "Build_Command" -dt "string";
	addAttr -ci true -sn "Import_Command" -ln "Import_Command" -dt "string";
	addAttr -ci true -sn "SetParent" -ln "SetParent" -dt "string";
	addAttr -ci true -sn "SetAttrsPosition" -ln "SetAttrsPosition" -dt "string";
	addAttr -ci true -sn "Help" -ln "Help" -dt "string";
	addAttr -ci true -sn "CtrlSize" -ln "CtrlSize" -dv 4 -min 1 -max 20 -at "long";
	addAttr -ci true -sn "postcode" -ln "postcode" -dt "string";
	setAttr ".precode" -type "string" "";
	setAttr -l on ".Build_Command" -type "string" "exec_nose.build_nose_block()";
	setAttr -l on ".Import_Command" -type "string" "import exec_nose";
	setAttr ".SetParent" -type "string" "Skull_Upr_Ctrl";
	setAttr ".SetAttrsPosition" -type "string" "Nose_Base_Ctrl";
	setAttr ".Help" -type "string" "Possible parent: ";
	setAttr -k on ".CtrlSize";
	setAttr ".postcode" -type "string" "";
createNode hyperLayout -n "SausageFaceTemplate_hyperLayout13";
	rename -uid "27154000-0018-1FF3-6621-A96200001BBC";
	setAttr ".ihi" 0;
createNode network -n "NullJnt_Config";
	rename -uid "27154000-0018-1FF3-6621-A96200001E47";
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
	setAttr ".Code" -type "string" "from maya import cmds\ncmds.select(cl=True)\ncmds.joint(n='Null_Local_Bnd')\ncmds.parent('Null_Local_Bnd', 'Bind_Joints_Grp')";
	setAttr ".postcode" -type "string" "";
createNode hyperLayout -n "hyperLayout40";
	rename -uid "27154000-0018-1FF3-6621-A963000020A5";
	setAttr ".ihi" 0;
createNode network -n "Correctives_Config";
	rename -uid "27154000-0018-1FF3-6621-A9620000201C";
	addAttr -ci true -sn "precode" -ln "precode" -dt "string";
	addAttr -ci true -sn "Build_Command" -ln "Build_Command" -dt "string";
	addAttr -ci true -sn "Import_Command" -ln "Import_Command" -dt "string";
	addAttr -ci true -sn "SetGeo" -ln "SetGeo" -dt "string";
	addAttr -ci true -sn "NewNames" -ln "NewNames" -dt "string";
	addAttr -ci true -sn "Help" -ln "Help" -dt "string";
	addAttr -ci true -sn "postcode" -ln "postcode" -dt "string";
	setAttr ".precode" -type "string" "";
	setAttr -l on ".Build_Command" -type "string" "exec_blendshape.build_blendshape_block()";
	setAttr -l on ".Import_Command" -type "string" "import exec_blendshape";
	setAttr ".SetGeo" -type "string" "BodySkull";
	setAttr ".NewNames" -type "string" "L_MouthUp_Corrective,R_MouthUp_Corrective,L_MouthDown_Corrective,R_MouthDown_Corrective,L_MouthWide_Corrective,R_MouthWide_Corrective,L_MouthNarrow_Corrective,R_MouthNarrow_Corrective,L_BrowUp,R_BrowUp,L_BrowDown,R_BrowDown,L_Puff,R_Puff";
	setAttr ".Help" -type "string" "Create Shapes for nain Geo and connect them via BlendShape, separate names with comas ','";
	setAttr ".postcode" -type "string" "";
createNode hyperLayout -n "hyperLayout42";
	rename -uid "27154000-0018-1FF3-6621-A96200001FDB";
	setAttr ".ihi" 0;
	setAttr -s 2 ".hyp";
createNode network -n "reorder_Config";
	rename -uid "27154000-0018-1FF3-6621-A963000020FD";
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
	setAttr ".Code" -type "string" "try:cmds.reorderDeformers('Correctives_BSP', 'Locals_BSP', 'BodySkull')\nexcept Exception as e:\n    print(e)\n";
	setAttr ".postcode" -type "string" "";
createNode hyperLayout -n "hyperLayout29";
	rename -uid "27154000-0018-1FF3-6621-A9630000209C";
	setAttr ".ihi" 0;
createNode network -n "BindSkull_Config";
	rename -uid "27154000-0018-1FF3-6621-A96200001DC1";
	addAttr -ci true -sn "precode" -ln "precode" -dt "string";
	addAttr -ci true -sn "Build_Command" -ln "Build_Command" -dt "string";
	addAttr -ci true -sn "Import_Command" -ln "Import_Command" -dt "string";
	addAttr -ci true -sn "SetGeo" -ln "SetGeo" -dt "string";
	addAttr -ci true -sn "SetJoints" -ln "SetJoints" -dt "string";
	addAttr -ci true -sn "Help" -ln "Help" -dt "string";
	addAttr -ci true -sn "postcode" -ln "postcode" -dt "string";
	setAttr ".precode" -type "string" "";
	setAttr -l on ".Build_Command" -type "string" "exec_skin.build_skin_block()";
	setAttr -l on ".Import_Command" -type "string" "import exec_skin";
	setAttr ".SetGeo" -type "string" "BodySkull";
	setAttr ".SetJoints" -type "string" "Skull_Lwr_Bnd, Skull_Upr_Bnd,Null_Local_Bnd";
	setAttr ".Help" -type "string" "Skin desire joints to geo, you can give names and * for overall parts, separate with ', comas', the command will select and then skin it";
	setAttr ".postcode" -type "string" "";
createNode hyperLayout -n "hyperLayout30";
	rename -uid "27154000-0018-1FF3-6621-A96200001D97";
	setAttr ".ihi" 0;
createNode network -n "BindEyelids_Config";
	rename -uid "27154000-0018-1FF3-6621-A96200001FE7";
	addAttr -ci true -sn "precode" -ln "precode" -dt "string";
	addAttr -ci true -sn "Build_Command" -ln "Build_Command" -dt "string";
	addAttr -ci true -sn "Import_Command" -ln "Import_Command" -dt "string";
	addAttr -ci true -sn "SetGeo" -ln "SetGeo" -dt "string";
	addAttr -ci true -sn "SetJoints" -ln "SetJoints" -dt "string";
	addAttr -ci true -sn "Help" -ln "Help" -dt "string";
	addAttr -ci true -sn "postcode" -ln "postcode" -dt "string";
	setAttr ".precode" -type "string" "";
	setAttr -l on ".Build_Command" -type "string" "exec_skin.build_skin_block()";
	setAttr -l on ".Import_Command" -type "string" "import exec_skin";
	setAttr ".SetGeo" -type "string" "BodyEyes";
	setAttr ".SetJoints" -type "string" "*_Eyelids_Up_*_Bnd,*_Eyelids_Dw_*_Bnd,*_Eyelids_Scale_Bnd,Null_Local_Bnd";
	setAttr ".Help" -type "string" "Skin desire joints to geo, you can give names and * for overall parts, separate with ', comas', the command will select and then skin it";
	setAttr ".postcode" -type "string" "";
createNode hyperLayout -n "hyperLayout31";
	rename -uid "27154000-0018-1FF3-6621-A96200001D98";
	setAttr ".ihi" 0;
createNode network -n "BindLips_Config";
	rename -uid "27154000-0018-1FF3-6621-A96200001DED";
	addAttr -ci true -sn "precode" -ln "precode" -dt "string";
	addAttr -ci true -sn "Build_Command" -ln "Build_Command" -dt "string";
	addAttr -ci true -sn "Import_Command" -ln "Import_Command" -dt "string";
	addAttr -ci true -sn "SetGeo" -ln "SetGeo" -dt "string";
	addAttr -ci true -sn "SetJoints" -ln "SetJoints" -dt "string";
	addAttr -ci true -sn "Help" -ln "Help" -dt "string";
	addAttr -ci true -sn "postcode" -ln "postcode" -dt "string";
	setAttr ".precode" -type "string" "";
	setAttr -l on ".Build_Command" -type "string" "exec_skin.build_skin_block()";
	setAttr -l on ".Import_Command" -type "string" "import exec_skin";
	setAttr ".SetGeo" -type "string" "BodyLips";
	setAttr ".SetJoints" -type "string" "*Lips*Bnd,Null_Local_Bnd";
	setAttr ".Help" -type "string" "Skin desire joints to geo, you can give names and * for overall parts, separate with ', comas', the command will select and then skin it";
	setAttr ".postcode" -type "string" "";
createNode hyperLayout -n "hyperLayout32";
	rename -uid "27154000-0018-1FF3-6621-A96200001D99";
	setAttr ".ihi" 0;
createNode network -n "BindBrows_Config";
	rename -uid "27154000-0018-1FF3-6621-A96100001AD2";
	addAttr -ci true -sn "precode" -ln "precode" -dt "string";
	addAttr -ci true -sn "Build_Command" -ln "Build_Command" -dt "string";
	addAttr -ci true -sn "Import_Command" -ln "Import_Command" -dt "string";
	addAttr -ci true -sn "SetGeo" -ln "SetGeo" -dt "string";
	addAttr -ci true -sn "SetJoints" -ln "SetJoints" -dt "string";
	addAttr -ci true -sn "Help" -ln "Help" -dt "string";
	addAttr -ci true -sn "postcode" -ln "postcode" -dt "string";
	setAttr ".precode" -type "string" "";
	setAttr -l on ".Build_Command" -type "string" "exec_skin.build_skin_block()";
	setAttr -l on ".Import_Command" -type "string" "import exec_skin";
	setAttr ".SetGeo" -type "string" "BodyBrows";
	setAttr ".SetJoints" -type "string" "*_Brow*Bnd,Null_Local_Bnd";
	setAttr ".Help" -type "string" "Skin desire joints to geo, you can give names and * for overall parts, separate with ', comas', the command will select and then skin it";
	setAttr ".postcode" -type "string" "";
createNode hyperLayout -n "SausageFaceTemplate_hyperLayout33";
	rename -uid "27154000-0018-1FF3-6621-A96200001EE2";
	setAttr ".ihi" 0;
createNode network -n "BindCheeks_Config";
	rename -uid "27154000-0018-1FF3-6621-A96200001FFF";
	addAttr -ci true -sn "precode" -ln "precode" -dt "string";
	addAttr -ci true -sn "Build_Command" -ln "Build_Command" -dt "string";
	addAttr -ci true -sn "Import_Command" -ln "Import_Command" -dt "string";
	addAttr -ci true -sn "SetGeo" -ln "SetGeo" -dt "string";
	addAttr -ci true -sn "SetJoints" -ln "SetJoints" -dt "string";
	addAttr -ci true -sn "Help" -ln "Help" -dt "string";
	addAttr -ci true -sn "postcode" -ln "postcode" -dt "string";
	setAttr ".precode" -type "string" "";
	setAttr -l on ".Build_Command" -type "string" "exec_skin.build_skin_block()";
	setAttr -l on ".Import_Command" -type "string" "import exec_skin";
	setAttr ".SetGeo" -type "string" "BodyCheeks";
	setAttr ".SetJoints" -type "string" "*_Cheecks_*_Bnd,Null_Local_Bnd";
	setAttr ".Help" -type "string" "Skin desire joints to geo, you can give names and * for overall parts, separate with ', comas', the command will select and then skin it";
	setAttr ".postcode" -type "string" "";
createNode hyperLayout -n "SausageFaceTemplate_hyperLayout34";
	rename -uid "27154000-0018-1FF3-6621-A96200001B8A";
	setAttr ".ihi" 0;
createNode network -n "BindJaw_Config";
	rename -uid "27154000-0018-1FF3-6621-A9620000201B";
	addAttr -ci true -sn "precode" -ln "precode" -dt "string";
	addAttr -ci true -sn "Build_Command" -ln "Build_Command" -dt "string";
	addAttr -ci true -sn "Import_Command" -ln "Import_Command" -dt "string";
	addAttr -ci true -sn "SetGeo" -ln "SetGeo" -dt "string";
	addAttr -ci true -sn "SetJoints" -ln "SetJoints" -dt "string";
	addAttr -ci true -sn "Help" -ln "Help" -dt "string";
	addAttr -ci true -sn "postcode" -ln "postcode" -dt "string";
	setAttr ".precode" -type "string" "";
	setAttr -l on ".Build_Command" -type "string" "exec_skin.build_skin_block()";
	setAttr -l on ".Import_Command" -type "string" "import exec_skin";
	setAttr ".SetGeo" -type "string" "BodyJaw";
	setAttr ".SetJoints" -type "string" "Jaw_Bnd, JawUpperLipPivot_Bnd,Null_Local_Bnd";
	setAttr ".Help" -type "string" "Skin desire joints to geo, you can give names and * for overall parts, separate with ', comas', the command will select and then skin it";
	setAttr ".postcode" -type "string" "";
createNode hyperLayout -n "CleanFaceInstall_hyperLayout47";
	rename -uid "27154000-0018-1FF3-6621-A96200001CA5";
	setAttr ".ihi" 0;
createNode network -n "BindNose_Config";
	rename -uid "27154000-0018-1FF3-6621-A96200001E94";
	addAttr -ci true -sn "precode" -ln "precode" -dt "string";
	addAttr -ci true -sn "Build_Command" -ln "Build_Command" -dt "string";
	addAttr -ci true -sn "Import_Command" -ln "Import_Command" -dt "string";
	addAttr -ci true -sn "SetGeo" -ln "SetGeo" -dt "string";
	addAttr -ci true -sn "Help" -ln "Help" -dt "string";
	addAttr -ci true -sn "SetJoints" -ln "SetJoints" -dt "string";
	addAttr -ci true -sn "postcode" -ln "postcode" -dt "string";
	setAttr ".precode" -type "string" "";
	setAttr -l on ".Build_Command" -type "string" "exec_skin.build_skin_block()";
	setAttr -l on ".Import_Command" -type "string" "import exec_skin";
	setAttr ".SetGeo" -type "string" "BodyNose";
	setAttr ".Help" -type "string" "Skin desire joints to geo, you can give names and * for overall parts, separate with ', comas', the command will select and then skin it";
	setAttr ".SetJoints" -type "string" "Nose_Origin_Bnd, R_NoseNostril_Bnd, Nose_Bridge_Bnd, Nose_Base_Bnd, Nose_Top_Bnd, L_NoseNostrilEnd_Bnd, R_NoseNostrilEnd_Bnd, Nose_Tip_Bnd, L_NoseNostril_Bnd, Null_Local_Bnd";
	setAttr ".postcode" -type "string" "";
createNode hyperLayout -n "hyperLayout35";
	rename -uid "27154000-0018-1FF3-6621-A96200001D9A";
	setAttr ".ihi" 0;
createNode network -n "BindMouthUp_Config";
	rename -uid "27154000-0018-1FF3-6621-A96200001C38";
	addAttr -ci true -sn "precode" -ln "precode" -dt "string";
	addAttr -ci true -sn "Build_Command" -ln "Build_Command" -dt "string";
	addAttr -ci true -sn "Import_Command" -ln "Import_Command" -dt "string";
	addAttr -ci true -sn "SetGeo" -ln "SetGeo" -dt "string";
	addAttr -ci true -sn "SetJoints" -ln "SetJoints" -dt "string";
	addAttr -ci true -sn "Help" -ln "Help" -dt "string";
	addAttr -ci true -sn "postcode" -ln "postcode" -dt "string";
	setAttr ".precode" -type "string" "";
	setAttr -l on ".Build_Command" -type "string" "exec_skin.build_skin_block()";
	setAttr -l on ".Import_Command" -type "string" "import exec_skin";
	setAttr ".SetGeo" -type "string" "BodyMouthUp";
	setAttr ".SetJoints" -type "string" "*_Commissures_Up_Bnd,Null_Local_Bnd";
	setAttr ".Help" -type "string" "Skin desire joints to geo, you can give names and * for overall parts, separate with ', comas', the command will select and then skin it";
	setAttr ".postcode" -type "string" "";
createNode hyperLayout -n "SausageFaceTemplate_hyperLayout36";
	rename -uid "27154000-0018-1FF3-6621-A96200001B8B";
	setAttr ".ihi" 0;
createNode network -n "BindMouthDown_Config";
	rename -uid "27154000-0018-1FF3-6621-A96200001EEF";
	addAttr -ci true -sn "precode" -ln "precode" -dt "string";
	addAttr -ci true -sn "Build_Command" -ln "Build_Command" -dt "string";
	addAttr -ci true -sn "Import_Command" -ln "Import_Command" -dt "string";
	addAttr -ci true -sn "SetGeo" -ln "SetGeo" -dt "string";
	addAttr -ci true -sn "SetJoints" -ln "SetJoints" -dt "string";
	addAttr -ci true -sn "Help" -ln "Help" -dt "string";
	addAttr -ci true -sn "postcode" -ln "postcode" -dt "string";
	setAttr ".precode" -type "string" "";
	setAttr -l on ".Build_Command" -type "string" "exec_skin.build_skin_block()";
	setAttr -l on ".Import_Command" -type "string" "import exec_skin";
	setAttr ".SetGeo" -type "string" "BodyMouthDown";
	setAttr ".SetJoints" -type "string" "*_Commissures_Down_Bnd,Null_Local_Bnd";
	setAttr ".Help" -type "string" "Skin desire joints to geo, you can give names and * for overall parts, separate with ', comas', the command will select and then skin it";
	setAttr ".postcode" -type "string" "";
createNode hyperLayout -n "CleanFaceInstall_hyperLayout37";
	rename -uid "27154000-0018-1FF3-6621-A96200001F8A";
	setAttr ".ihi" 0;
createNode network -n "BindMouthWide_Config";
	rename -uid "27154000-0018-1FF3-6621-A96200001F80";
	addAttr -ci true -sn "precode" -ln "precode" -dt "string";
	addAttr -ci true -sn "Build_Command" -ln "Build_Command" -dt "string";
	addAttr -ci true -sn "Import_Command" -ln "Import_Command" -dt "string";
	addAttr -ci true -sn "SetGeo" -ln "SetGeo" -dt "string";
	addAttr -ci true -sn "SetJoints" -ln "SetJoints" -dt "string";
	addAttr -ci true -sn "Help" -ln "Help" -dt "string";
	addAttr -ci true -sn "postcode" -ln "postcode" -dt "string";
	setAttr ".precode" -type "string" "";
	setAttr -l on ".Build_Command" -type "string" "exec_skin.build_skin_block()";
	setAttr -l on ".Import_Command" -type "string" "import exec_skin";
	setAttr ".SetGeo" -type "string" "BodyMouthWide";
	setAttr ".SetJoints" -type "string" "*_Commissures_Wide_Bnd,Null_Local_Bnd";
	setAttr ".Help" -type "string" "Skin desire joints to geo, you can give names and * for overall parts, separate with ', comas', the command will select and then skin it";
	setAttr ".postcode" -type "string" "";
createNode hyperLayout -n "SausageFaceTemplate_hyperLayout38";
	rename -uid "27154000-0018-1FF3-6621-A96200001B8D";
	setAttr ".ihi" 0;
createNode network -n "BindMouthNarrow_Config";
	rename -uid "27154000-0018-1FF3-6621-A96200001B5E";
	addAttr -ci true -sn "precode" -ln "precode" -dt "string";
	addAttr -ci true -sn "Build_Command" -ln "Build_Command" -dt "string";
	addAttr -ci true -sn "Import_Command" -ln "Import_Command" -dt "string";
	addAttr -ci true -sn "SetGeo" -ln "SetGeo" -dt "string";
	addAttr -ci true -sn "SetJoints" -ln "SetJoints" -dt "string";
	addAttr -ci true -sn "Help" -ln "Help" -dt "string";
	addAttr -ci true -sn "postcode" -ln "postcode" -dt "string";
	setAttr ".precode" -type "string" "";
	setAttr -l on ".Build_Command" -type "string" "exec_skin.build_skin_block()";
	setAttr -l on ".Import_Command" -type "string" "import exec_skin";
	setAttr ".SetGeo" -type "string" "BodyMouthNarrow";
	setAttr ".SetJoints" -type "string" "*_Commissures_Narrow_Bnd,Null_Local_Bnd";
	setAttr ".Help" -type "string" "Skin desire joints to geo, you can give names and * for overall parts, separate with ', comas', the command will select and then skin it";
	setAttr ".postcode" -type "string" "";
createNode hyperLayout -n "hyperLayout39";
	rename -uid "27154000-0018-1FF3-6621-A96200001D9C";
	setAttr ".ihi" 0;
createNode network -n "CleanFaceInstall_Load_Ctrls_Config";
	rename -uid "27154000-0018-1FF3-6621-A96200001C0E";
	addAttr -ci true -sn "precode" -ln "precode" -dt "string";
	addAttr -ci true -sn "Build_Command" -ln "Build_Command" -dt "string";
	addAttr -ci true -sn "Import_Command" -ln "Import_Command" -dt "string";
	addAttr -ci true -sn "File" -ln "File" -dt "string";
	addAttr -ci true -sn "Help" -ln "Help" -dt "string";
	addAttr -ci true -sn "postcode" -ln "postcode" -dt "string";
	setAttr ".precode" -type "string" "";
	setAttr -l on ".Build_Command" -type "string" "exec_load_ctrls.build_load_ctrls_block()";
	setAttr -l on ".Import_Command" -type "string" "import exec_load_ctrls";
	setAttr ".File" -type "string" "Simple";
	setAttr ".Help" -type "string" "Load Ctrls Data from File, you can put show keys to define the default ones.";
	setAttr ".postcode" -type "string" "";
select -ne :time1;
	setAttr ".o" 0;
select -ne :hardwareRenderingGlobals;
	setAttr ".otfna" -type "stringArray" 22 "NURBS Curves" "NURBS Surfaces" "Polygons" "Subdiv Surface" "Particles" "Particle Instance" "Fluids" "Strokes" "Image Planes" "UI" "Lights" "Cameras" "Locators" "Joints" "IK Handles" "Deformers" "Motion Trails" "Components" "Hair Systems" "Follicles" "Misc. UI" "Ornaments"  ;
	setAttr ".otfva" -type "Int32Array" 22 0 1 1 1 1 1
		 1 1 1 0 0 0 0 0 0 0 0 0
		 0 0 0 0 ;
	setAttr ".fprt" yes;
	setAttr ".rtfm" 1;
select -ne :renderPartition;
	setAttr -s 7 ".st";
select -ne :renderGlobalsList1;
select -ne :defaultShaderList1;
	setAttr -s 9 ".s";
select -ne :postProcessList1;
	setAttr -s 2 ".p";
select -ne :defaultRenderUtilityList1;
	setAttr -s 82 ".u";
select -ne :defaultRenderingList1;
select -ne :defaultTextureList1;
	setAttr -s 4 ".tx";
select -ne :standardSurface1;
	setAttr ".bc" -type "float3" 0.40000001 0.40000001 0.40000001 ;
	setAttr ".sr" 0.5;
select -ne :initialShadingGroup;
	setAttr ".ro" yes;
select -ne :initialParticleSE;
	setAttr ".ro" yes;
select -ne :defaultRenderGlobals;
	addAttr -ci true -sn "auto_pipeline" -ln "auto_pipeline" -min 0 -max 1 -at "bool";
	addAttr -ci true -sn "auto_pipeline_task_id" -ln "auto_pipeline_task_id" -at "long";
	addAttr -ci true -sn "auto_pipeline_preset_id" -ln "auto_pipeline_preset_id" -at "long";
	addAttr -ci true -h true -sn "dss" -ln "defaultSurfaceShader" -dt "string";
	setAttr ".outf" 3;
	setAttr ".exrc" 3;
	setAttr ".an" yes;
	setAttr ".pff" yes;
	setAttr ".ifp" -type "string" "<RenderLayer>/<Version>/<RenderLayer>_<Version>";
	setAttr ".rv" -type "string" "v001";
	setAttr ".auto_pipeline" yes;
	setAttr ".auto_pipeline_task_id" 356005;
	setAttr ".auto_pipeline_preset_id" 1;
	setAttr ".dss" -type "string" "standardSurface1";
select -ne :defaultResolution;
	setAttr ".w" 1920;
	setAttr ".h" 1080;
	setAttr ".pa" 1;
	setAttr ".dar" 1.7777777910232544;
select -ne :defaultColorMgtGlobals;
	setAttr ".cfe" yes;
	setAttr ".cfp" -type "string" "<MAYA_RESOURCES>/OCIO-configs/Maya2022-default/config.ocio";
	setAttr ".vtn" -type "string" "ACES 1.0 SDR-video (sRGB)";
	setAttr ".vn" -type "string" "ACES 1.0 SDR-video";
	setAttr ".dn" -type "string" "sRGB";
	setAttr ".wsn" -type "string" "ACEScg";
	setAttr ".otn" -type "string" "ACES 1.0 SDR-video (sRGB)";
	setAttr ".potn" -type "string" "ACES 1.0 SDR-video (sRGB)";
select -ne :hardwareRenderGlobals;
	setAttr ".ctrs" 256;
	setAttr ".btrs" 512;
connectAttr "hyperLayout8.msg" "BaseA_Block.hl";
connectAttr "SausageFaceTemplate_BaseA_Config.nds" "BaseA_Block.nds";
connectAttr "hyperLayout7.msg" "VisAttrs_Block.hl";
connectAttr "VisAttrs_Config.nds" "VisAttrs_Block.nds";
connectAttr "SausageFaceTemplate_hyperLayout39.msg" "SkullLocal_Block.hl";
connectAttr "SkullLocal_Config.nds" "SkullLocal_Block.nds";
connectAttr "SausageFaceTemplate_hyperLayout17.msg" "Locals_Block.hl";
connectAttr "Locals_Config.nds" "Locals_Block.nds";
connectAttr "hyperLayout9.msg" "Skull_Block.hl";
connectAttr "Skull_Config.nds" "Skull_Block.nds";
connectAttr "Skull_Lwr_Guide.Helper" "Skull_Lwr_Guide_CtrlShape.v";
connectAttr "Skull_Lwr_Guide.Helper" "Skull_Lwr_Guide_Ctrl_CtrlShape.v";
connectAttr "Skull_Lwr_Guide.Helper" "Skull_Lwr_Guide_Ctrl_Ctrl_CtrlShape.v";
connectAttr "Skull_Lwr_Guide.Helper" "Skull_Lwr_Guide_Ctrl_Ctrl_Ctrl_CtrlShape.v"
		;
connectAttr "Skull_Lwr_Guide.s" "Skull_Upr_Guide.is";
connectAttr "Skull_Upr_Guide.Helper" "Skull_Upr_Guide_CtrlShape.v";
connectAttr "Skull_Upr_Guide.Helper" "Skull_Upr_Guide_Ctrl_CtrlShape.v";
connectAttr "Skull_Upr_Guide.Helper" "Skull_Upr_Guide_Ctrl_Ctrl_CtrlShape.v";
connectAttr "Skull_Upr_Guide.Helper" "Skull_Upr_Guide_Ctrl_Ctrl_Ctrl_CtrlShape.v"
		;
connectAttr "hyperLayout49.msg" "L_Eyelids_Block.hl";
connectAttr "L_Eyelids_Config.nds" "L_Eyelids_Block.nds";
connectAttr "hyperLayout44.msg" "L_Orbicularis_Block.hl";
connectAttr "L_Orbicularis_Config.nds" "L_Orbicularis_Block.nds";
connectAttr "L_Orbicularis_Guide.RotateOrder" "L_Orbicularis_Guide.ro";
connectAttr "hyperLayout10.msg" "L_Brow_Block.hl";
connectAttr "L_Brow_Config.nds" "L_Brow_Block.nds";
connectAttr "hyperLayout48.msg" "L_Cheecks_Block.hl";
connectAttr "L_Cheecks_Config.nds" "L_Cheecks_Block.nds";
connectAttr "L_Cheecks_Guide.Helper" "L_Cheecks_Guide_CtrlShape.v";
connectAttr "L_Cheecks_Guide.Helper" "L_Cheecks_Guide_Ctrl_CtrlShape.v";
connectAttr "L_Cheecks_Guide.Helper" "L_Cheecks_Guide_Ctrl_Ctrl_CtrlShape.v";
connectAttr "L_Cheecks_Guide.Helper" "L_Cheecks_Guide_Ctrl_Ctrl_Ctrl_CtrlShape.v"
		;
connectAttr "hyperLayout50.msg" "Lips_Block.hl";
connectAttr "Lips_Config.nds" "Lips_Block.nds";
connectAttr "L_Lips_Orient_Guide_Guide.Helper" "L_Lips_Orient_Guide_Guide_CtrlShape.v"
		;
connectAttr "L_Lips_Orient_Guide_Guide.Helper" "L_Lips_Orient_Guide_Guide_Ctrl_CtrlShape.v"
		;
connectAttr "L_Lips_Orient_Guide_Guide.Helper" "L_Lips_Orient_Guide_Guide_Ctrl_Ctrl_CtrlShape.v"
		;
connectAttr "L_Lips_Orient_Guide_Guide.Helper" "L_Lips_Orient_Guide_Guide_Ctrl_Ctrl_Ctrl_CtrlShape.v"
		;
connectAttr "Lips_SlideCenter_Guide_Guide.Helper" "Lips_SlideCenter_Guide_Guide_CtrlShape.v"
		;
connectAttr "Lips_SlideCenter_Guide_Guide.Helper" "Lips_SlideCenter_Guide_Guide_Ctrl_CtrlShape.v"
		;
connectAttr "Lips_SlideCenter_Guide_Guide.Helper" "Lips_SlideCenter_Guide_Guide_Ctrl_Ctrl_CtrlShape.v"
		;
connectAttr "Lips_SlideCenter_Guide_Guide.Helper" "Lips_SlideCenter_Guide_Guide_Ctrl_Ctrl_Ctrl_CtrlShape.v"
		;
connectAttr "hyperLayout2.msg" "Jaw_Block.hl";
connectAttr "Jaw_Config.nds" "Jaw_Block.nds";
connectAttr "Jaw_Guide.Helper" "Jaw_Guide_CtrlShape.v";
connectAttr "Jaw_Guide.Helper" "Jaw_Guide_Ctrl_CtrlShape.v";
connectAttr "Jaw_Guide.Helper" "Jaw_Guide_Ctrl_Ctrl_CtrlShape.v";
connectAttr "Jaw_Guide.Helper" "Jaw_Guide_Ctrl_Ctrl_Ctrl_CtrlShape.v";
connectAttr "Jaw_Guide.s" "JawUpperLip_Guide.is";
connectAttr "JawUpperLip_Guide.Helper" "JawUpperLip_Guide_CtrlShape.v";
connectAttr "JawUpperLip_Guide.Helper" "JawUpperLip_Guide_Ctrl_CtrlShape.v";
connectAttr "JawUpperLip_Guide.Helper" "JawUpperLip_Guide_Ctrl_Ctrl_CtrlShape.v"
		;
connectAttr "JawUpperLip_Guide.Helper" "JawUpperLip_Guide_Ctrl_Ctrl_Ctrl_CtrlShape.v"
		;
connectAttr "Jaw_Guide.s" "JawLowerLip_Guide.is";
connectAttr "JawLowerLip_Guide.Helper" "JawLowerLip_Guide_CtrlShape.v";
connectAttr "JawLowerLip_Guide.Helper" "JawLowerLip_Guide_Ctrl_CtrlShape.v";
connectAttr "JawLowerLip_Guide.Helper" "JawLowerLip_Guide_Ctrl_Ctrl_CtrlShape.v"
		;
connectAttr "JawLowerLip_Guide.Helper" "JawLowerLip_Guide_Ctrl_Ctrl_Ctrl_CtrlShape.v"
		;
connectAttr "hyperLayout45.msg" "Commissures_Block.hl";
connectAttr "Commissures_Config.nds" "Commissures_Block.nds";
connectAttr "SausageFaceTemplate_hyperLayout14.msg" "Tongue_Block.hl";
connectAttr "Tongue_Config.nds" "Tongue_Block.nds";
connectAttr "Tongue_01_Guide.Helper" "Tongue_01_Guide_CtrlShape.v";
connectAttr "Tongue_01_Guide.Helper" "Tongue_01_Guide_Ctrl_CtrlShape.v";
connectAttr "Tongue_01_Guide.Helper" "Tongue_01_Guide_Ctrl_Ctrl_CtrlShape.v";
connectAttr "Tongue_01_Guide.Helper" "Tongue_01_Guide_Ctrl_Ctrl_Ctrl_CtrlShape.v"
		;
connectAttr "Tongue_01_Guide.s" "Tongue_02_Guide.is";
connectAttr "Tongue_02_Guide.Helper" "Tongue_02_Guide_CtrlShape.v";
connectAttr "Tongue_02_Guide.Helper" "Tongue_02_Guide_Ctrl_CtrlShape.v";
connectAttr "Tongue_02_Guide.Helper" "Tongue_02_Guide_Ctrl_Ctrl_CtrlShape.v";
connectAttr "Tongue_02_Guide.Helper" "Tongue_02_Guide_Ctrl_Ctrl_Ctrl_CtrlShape.v"
		;
connectAttr "Tongue_02_Guide.s" "Tongue_03_Guide.is";
connectAttr "Tongue_03_Guide.Helper" "Tongue_03_Guide_CtrlShape.v";
connectAttr "Tongue_03_Guide.Helper" "Tongue_03_Guide_Ctrl_CtrlShape.v";
connectAttr "Tongue_03_Guide.Helper" "Tongue_03_Guide_Ctrl_Ctrl_CtrlShape.v";
connectAttr "Tongue_03_Guide.Helper" "Tongue_03_Guide_Ctrl_Ctrl_Ctrl_CtrlShape.v"
		;
connectAttr "Tongue_03_Guide.s" "Tongue_04_Guide.is";
connectAttr "Tongue_04_Guide.Helper" "Tongue_04_Guide_CtrlShape.v";
connectAttr "Tongue_04_Guide.Helper" "Tongue_04_Guide_Ctrl_CtrlShape.v";
connectAttr "Tongue_04_Guide.Helper" "Tongue_04_Guide_Ctrl_Ctrl_CtrlShape.v";
connectAttr "Tongue_04_Guide.Helper" "Tongue_04_Guide_Ctrl_Ctrl_Ctrl_CtrlShape.v"
		;
connectAttr "Tongue_04_Guide.s" "Tongue_05_Guide.is";
connectAttr "Tongue_05_Guide.Helper" "Tongue_05_Guide_CtrlShape.v";
connectAttr "Tongue_05_Guide.Helper" "Tongue_05_Guide_Ctrl_CtrlShape.v";
connectAttr "Tongue_05_Guide.Helper" "Tongue_05_Guide_Ctrl_Ctrl_CtrlShape.v";
connectAttr "Tongue_05_Guide.Helper" "Tongue_05_Guide_Ctrl_Ctrl_Ctrl_CtrlShape.v"
		;
connectAttr "SausageFaceTemplate_hyperLayout19.msg" "Teeth_Block.hl";
connectAttr "Teeth_Config.nds" "Teeth_Block.nds";
connectAttr "Teeth_Lwr_Guide.Helper" "Teeth_Lwr_Guide_CtrlShape.v";
connectAttr "Teeth_Lwr_Guide.Helper" "Teeth_Lwr_Guide_Ctrl_CtrlShape.v";
connectAttr "Teeth_Lwr_Guide.Helper" "Teeth_Lwr_Guide_Ctrl_Ctrl_CtrlShape.v";
connectAttr "Teeth_Lwr_Guide.Helper" "Teeth_Lwr_Guide_Ctrl_Ctrl_Ctrl_CtrlShape.v"
		;
connectAttr "Teeth_Upr_Guide.Helper" "Teeth_Upr_Guide_CtrlShape.v";
connectAttr "Teeth_Upr_Guide.Helper" "Teeth_Upr_Guide_Ctrl_CtrlShape.v";
connectAttr "Teeth_Upr_Guide.Helper" "Teeth_Upr_Guide_Ctrl_Ctrl_CtrlShape.v";
connectAttr "Teeth_Upr_Guide.Helper" "Teeth_Upr_Guide_Ctrl_Ctrl_Ctrl_CtrlShape.v"
		;
connectAttr "hyperLayout43.msg" "Nose_Block.hl";
connectAttr "Nose_Config.nds" "Nose_Block.nds";
connectAttr "Nose_Origin_Guide.Helper" "Nose_Origin_Guide_CtrlShape.v";
connectAttr "Nose_Origin_Guide.Helper" "Nose_Origin_Guide_Ctrl_CtrlShape.v";
connectAttr "Nose_Origin_Guide.Helper" "Nose_Origin_Guide_Ctrl_Ctrl_CtrlShape.v"
		;
connectAttr "Nose_Origin_Guide.Helper" "Nose_Origin_Guide_Ctrl_Ctrl_Ctrl_CtrlShape.v"
		;
connectAttr "Nose_Origin_Guide.s" "Nose_Bridge_Guide.is";
connectAttr "Nose_Bridge_Guide.Helper" "Nose_Bridge_Guide_CtrlShape.v";
connectAttr "Nose_Bridge_Guide.Helper" "Nose_Bridge_Guide_Ctrl_CtrlShape.v";
connectAttr "Nose_Bridge_Guide.Helper" "Nose_Bridge_Guide_Ctrl_Ctrl_CtrlShape.v"
		;
connectAttr "Nose_Bridge_Guide.Helper" "Nose_Bridge_Guide_Ctrl_Ctrl_Ctrl_CtrlShape.v"
		;
connectAttr "Nose_Bridge_Guide.s" "Nose_Base_Guide.is";
connectAttr "Nose_Base_Guide.Helper" "Nose_Base_Guide_CtrlShape.v";
connectAttr "Nose_Base_Guide.Helper" "Nose_Base_Guide_Ctrl_CtrlShape.v";
connectAttr "Nose_Base_Guide.Helper" "Nose_Base_Guide_Ctrl_Ctrl_CtrlShape.v";
connectAttr "Nose_Base_Guide.Helper" "Nose_Base_Guide_Ctrl_Ctrl_Ctrl_CtrlShape.v"
		;
connectAttr "Nose_Base_Guide.s" "L_NoseNostril_Guide.is";
connectAttr "L_NoseNostril_Guide.Helper" "L_NoseNostril_Guide_CtrlShape.v";
connectAttr "L_NoseNostril_Guide.Helper" "L_NoseNostril_Guide_Ctrl_CtrlShape.v";
connectAttr "L_NoseNostril_Guide.Helper" "L_NoseNostril_Guide_Ctrl_Ctrl_CtrlShape.v"
		;
connectAttr "L_NoseNostril_Guide.Helper" "L_NoseNostril_Guide_Ctrl_Ctrl_Ctrl_CtrlShape.v"
		;
connectAttr "L_NoseNostril_Guide.s" "L_NoseNostrilEnd_Guide.is";
connectAttr "L_NoseNostrilEnd_Guide.Helper" "L_NoseNostrilEnd_Guide_CtrlShape.v"
		;
connectAttr "L_NoseNostrilEnd_Guide.Helper" "L_NoseNostrilEnd_Guide_Ctrl_CtrlShape.v"
		;
connectAttr "L_NoseNostrilEnd_Guide.Helper" "L_NoseNostrilEnd_Guide_Ctrl_Ctrl_CtrlShape.v"
		;
connectAttr "L_NoseNostrilEnd_Guide.Helper" "L_NoseNostrilEnd_Guide_Ctrl_Ctrl_Ctrl_CtrlShape.v"
		;
connectAttr "Nose_Base_Guide.s" "Nose_Tip_Guide.is";
connectAttr "Nose_Tip_Guide.Helper" "Nose_Tip_Guide_CtrlShape.v";
connectAttr "Nose_Tip_Guide.Helper" "Nose_Tip_Guide_Ctrl_CtrlShape.v";
connectAttr "Nose_Tip_Guide.Helper" "Nose_Tip_Guide_Ctrl_Ctrl_CtrlShape.v";
connectAttr "Nose_Tip_Guide.Helper" "Nose_Tip_Guide_Ctrl_Ctrl_Ctrl_CtrlShape.v";
connectAttr "Nose_Base_Guide.s" "R_NoseNostril_Guide.is";
connectAttr "R_NoseNostril_Guide.Helper" "R_NoseNostril_Guide_CtrlShape.v";
connectAttr "R_NoseNostril_Guide.Helper" "R_NoseNostril_Guide_Ctrl_CtrlShape.v";
connectAttr "R_NoseNostril_Guide.Helper" "R_NoseNostril_Guide_Ctrl_Ctrl_CtrlShape.v"
		;
connectAttr "R_NoseNostril_Guide.Helper" "R_NoseNostril_Guide_Ctrl_Ctrl_Ctrl_CtrlShape.v"
		;
connectAttr "R_NoseNostril_Guide.s" "R_NoseNostrilEnd_Guide.is";
connectAttr "R_NoseNostrilEnd_Guide.Helper" "R_NoseNostrilEnd_Guide_CtrlShape.v"
		;
connectAttr "R_NoseNostrilEnd_Guide.Helper" "R_NoseNostrilEnd_Guide_Ctrl_CtrlShape.v"
		;
connectAttr "R_NoseNostrilEnd_Guide.Helper" "R_NoseNostrilEnd_Guide_Ctrl_Ctrl_CtrlShape.v"
		;
connectAttr "R_NoseNostrilEnd_Guide.Helper" "R_NoseNostrilEnd_Guide_Ctrl_Ctrl_Ctrl_CtrlShape.v"
		;
connectAttr "Nose_Base_Guide.s" "Nose_Top_Guide.is";
connectAttr "Nose_Top_Guide.Helper" "Nose_Top_Guide_CtrlShape.v";
connectAttr "Nose_Top_Guide.Helper" "Nose_Top_Guide_Ctrl_CtrlShape.v";
connectAttr "Nose_Top_Guide.Helper" "Nose_Top_Guide_Ctrl_Ctrl_CtrlShape.v";
connectAttr "Nose_Top_Guide.Helper" "Nose_Top_Guide_Ctrl_Ctrl_Ctrl_CtrlShape.v";
connectAttr "SausageFaceTemplate_hyperLayout13.msg" "NullJnt_Block.hl";
connectAttr "NullJnt_Config.nds" "NullJnt_Block.nds";
connectAttr "hyperLayout40.msg" "Correctives_Block.hl";
connectAttr "Correctives_Config.nds" "Correctives_Block.nds";
connectAttr "hyperLayout42.msg" "reorder_Block.hl";
connectAttr "reorder_Config.nds" "reorder_Block.nds";
connectAttr "hyperLayout29.msg" "BindSkull_Block.hl";
connectAttr "BindSkull_Config.nds" "BindSkull_Block.nds";
connectAttr "hyperLayout30.msg" "BindEyelids_Block.hl";
connectAttr "BindEyelids_Config.nds" "BindEyelids_Block.nds";
connectAttr "hyperLayout31.msg" "BindLips_Block.hl";
connectAttr "BindLips_Config.nds" "BindLips_Block.nds";
connectAttr "hyperLayout32.msg" "BindBrows_Block.hl";
connectAttr "BindBrows_Config.nds" "BindBrows_Block.nds";
connectAttr "SausageFaceTemplate_hyperLayout33.msg" "BindCheeks_Block.hl";
connectAttr "BindCheeks_Config.nds" "BindCheeks_Block.nds";
connectAttr "SausageFaceTemplate_hyperLayout34.msg" "BindJaw_Block.hl";
connectAttr "BindJaw_Config.nds" "BindJaw_Block.nds";
connectAttr "CleanFaceInstall_hyperLayout47.msg" "BindNose_Block.hl";
connectAttr "BindNose_Config.nds" "BindNose_Block.nds";
connectAttr "hyperLayout35.msg" "BindMouthUp_Block.hl";
connectAttr "BindMouthUp_Config.nds" "BindMouthUp_Block.nds";
connectAttr "SausageFaceTemplate_hyperLayout36.msg" "BindMouthDown_Block.hl";
connectAttr "BindMouthDown_Config.nds" "BindMouthDown_Block.nds";
connectAttr "CleanFaceInstall_hyperLayout37.msg" "BindMouthWide_Block.hl";
connectAttr "BindMouthWide_Config.nds" "BindMouthWide_Block.nds";
connectAttr "SausageFaceTemplate_hyperLayout38.msg" "BindMouthNarrow_Block.hl";
connectAttr "BindMouthNarrow_Config.nds" "BindMouthNarrow_Block.nds";
connectAttr "hyperLayout39.msg" "Load_Ctrls_Block.hl";
connectAttr "CleanFaceInstall_Load_Ctrls_Config.nds" "Load_Ctrls_Block.nds";
connectAttr "Vis_Guide.msg" "hyperLayout7.hyp[22].dn";
connectAttr "Vis_GuideShape.msg" "hyperLayout7.hyp[23].dn";
connectAttr "Skull_Lwr_Guide.msg" "hyperLayout9.hyp[130].dn";
connectAttr "Skull_Lwr_Guide_CtrlShape.msg" "hyperLayout9.hyp[131].dn";
connectAttr "Skull_Lwr_Guide_Ctrl_CtrlShape.msg" "hyperLayout9.hyp[132].dn";
connectAttr "Skull_Lwr_Guide_Ctrl_Ctrl_CtrlShape.msg" "hyperLayout9.hyp[133].dn"
		;
connectAttr "Skull_Lwr_Guide_Ctrl_Ctrl_Ctrl_CtrlShape.msg" "hyperLayout9.hyp[134].dn"
		;
connectAttr "Skull_Upr_Guide.msg" "hyperLayout9.hyp[135].dn";
connectAttr "Skull_Upr_Guide_CtrlShape.msg" "hyperLayout9.hyp[136].dn";
connectAttr "Skull_Upr_Guide_Ctrl_CtrlShape.msg" "hyperLayout9.hyp[137].dn";
connectAttr "Skull_Upr_Guide_Ctrl_Ctrl_CtrlShape.msg" "hyperLayout9.hyp[138].dn"
		;
connectAttr "Skull_Upr_Guide_Ctrl_Ctrl_Ctrl_CtrlShape.msg" "hyperLayout9.hyp[139].dn"
		;
connectAttr "Eye_Pivot.msg" "hyperLayout49.hyp[12].dn";
connectAttr "L_Orbicularis_Guide.msg" "hyperLayout44.hyp[9].dn";
connectAttr "L_Orbicularis_GuideShape.msg" "hyperLayout44.hyp[10].dn";
connectAttr "L_Brow_Guide.msg" "hyperLayout10.hyp[22].dn";
connectAttr "L_Brow_GuideShape.msg" "hyperLayout10.hyp[23].dn";
connectAttr "L_Cheecks_Border_Guide.msg" "hyperLayout48.hyp[72].dn";
connectAttr "curveShape7.msg" "hyperLayout48.hyp[73].dn";
connectAttr "L_Cheecks_Bone_Guide.msg" "hyperLayout48.hyp[74].dn";
connectAttr "curveShape8.msg" "hyperLayout48.hyp[75].dn";
connectAttr "L_Cheecks_Guide.msg" "hyperLayout48.hyp[86].dn";
connectAttr "L_Cheecks_Guide_CtrlShape.msg" "hyperLayout48.hyp[87].dn";
connectAttr "L_Cheecks_Guide_Ctrl_CtrlShape.msg" "hyperLayout48.hyp[88].dn";
connectAttr "L_Cheecks_Guide_Ctrl_Ctrl_CtrlShape.msg" "hyperLayout48.hyp[89].dn"
		;
connectAttr "L_Cheecks_Guide_Ctrl_Ctrl_Ctrl_CtrlShape.msg" "hyperLayout48.hyp[90].dn"
		;
connectAttr "L_Lips_Orient_Guide_Guide.msg" "hyperLayout50.hyp[0].dn";
connectAttr "L_Lips_Orient_Guide_Guide_CtrlShape.msg" "hyperLayout50.hyp[1].dn";
connectAttr "L_Lips_Orient_Guide_Guide_Ctrl_CtrlShape.msg" "hyperLayout50.hyp[2].dn"
		;
connectAttr "L_Lips_Orient_Guide_Guide_Ctrl_Ctrl_CtrlShape.msg" "hyperLayout50.hyp[3].dn"
		;
connectAttr "L_Lips_Orient_Guide_Guide_Ctrl_Ctrl_Ctrl_CtrlShape.msg" "hyperLayout50.hyp[4].dn"
		;
connectAttr "Lips_SlideCenter_Guide_Guide.msg" "hyperLayout50.hyp[5].dn";
connectAttr "Lips_SlideCenter_Guide_Guide_CtrlShape.msg" "hyperLayout50.hyp[6].dn"
		;
connectAttr "Lips_SlideCenter_Guide_Guide_Ctrl_CtrlShape.msg" "hyperLayout50.hyp[7].dn"
		;
connectAttr "Lips_SlideCenter_Guide_Guide_Ctrl_Ctrl_CtrlShape.msg" "hyperLayout50.hyp[8].dn"
		;
connectAttr "Lips_SlideCenter_Guide_Guide_Ctrl_Ctrl_Ctrl_CtrlShape.msg" "hyperLayout50.hyp[9].dn"
		;
connectAttr "Jaw_Guide.msg" "hyperLayout2.hyp[205].dn";
connectAttr "Jaw_Guide_CtrlShape.msg" "hyperLayout2.hyp[206].dn";
connectAttr "Jaw_Guide_Ctrl_CtrlShape.msg" "hyperLayout2.hyp[207].dn";
connectAttr "Jaw_Guide_Ctrl_Ctrl_CtrlShape.msg" "hyperLayout2.hyp[208].dn";
connectAttr "Jaw_Guide_Ctrl_Ctrl_Ctrl_CtrlShape.msg" "hyperLayout2.hyp[209].dn";
connectAttr "JawUpperLip_Guide.msg" "hyperLayout2.hyp[210].dn";
connectAttr "JawUpperLip_Guide_CtrlShape.msg" "hyperLayout2.hyp[211].dn";
connectAttr "JawUpperLip_Guide_Ctrl_CtrlShape.msg" "hyperLayout2.hyp[212].dn";
connectAttr "JawUpperLip_Guide_Ctrl_Ctrl_CtrlShape.msg" "hyperLayout2.hyp[213].dn"
		;
connectAttr "JawUpperLip_Guide_Ctrl_Ctrl_Ctrl_CtrlShape.msg" "hyperLayout2.hyp[214].dn"
		;
connectAttr "JawLowerLip_Guide.msg" "hyperLayout2.hyp[215].dn";
connectAttr "JawLowerLip_Guide_CtrlShape.msg" "hyperLayout2.hyp[216].dn";
connectAttr "JawLowerLip_Guide_Ctrl_CtrlShape.msg" "hyperLayout2.hyp[217].dn";
connectAttr "JawLowerLip_Guide_Ctrl_Ctrl_CtrlShape.msg" "hyperLayout2.hyp[218].dn"
		;
connectAttr "JawLowerLip_Guide_Ctrl_Ctrl_Ctrl_CtrlShape.msg" "hyperLayout2.hyp[219].dn"
		;
connectAttr "L_Commissures_Down_Guide.msg" "hyperLayout45.hyp[76].dn";
connectAttr "curveShape664.msg" "hyperLayout45.hyp[77].dn";
connectAttr "L_Commissures_Narrow_Guide.msg" "hyperLayout45.hyp[78].dn";
connectAttr "curveShape40.msg" "hyperLayout45.hyp[79].dn";
connectAttr "L_Commissures_Up_Guide.msg" "hyperLayout45.hyp[80].dn";
connectAttr "curveShape584.msg" "hyperLayout45.hyp[81].dn";
connectAttr "L_Commissures_Wide_Guide.msg" "hyperLayout45.hyp[82].dn";
connectAttr "curveShape348.msg" "hyperLayout45.hyp[83].dn";
connectAttr "Tongue_01_Guide.msg" "SausageFaceTemplate_hyperLayout14.hyp[455].dn"
		;
connectAttr "Tongue_01_Guide_CtrlShape.msg" "SausageFaceTemplate_hyperLayout14.hyp[456].dn"
		;
connectAttr "Tongue_01_Guide_Ctrl_CtrlShape.msg" "SausageFaceTemplate_hyperLayout14.hyp[457].dn"
		;
connectAttr "Tongue_01_Guide_Ctrl_Ctrl_CtrlShape.msg" "SausageFaceTemplate_hyperLayout14.hyp[458].dn"
		;
connectAttr "Tongue_01_Guide_Ctrl_Ctrl_Ctrl_CtrlShape.msg" "SausageFaceTemplate_hyperLayout14.hyp[459].dn"
		;
connectAttr "Tongue_02_Guide.msg" "SausageFaceTemplate_hyperLayout14.hyp[460].dn"
		;
connectAttr "Tongue_02_Guide_CtrlShape.msg" "SausageFaceTemplate_hyperLayout14.hyp[461].dn"
		;
connectAttr "Tongue_02_Guide_Ctrl_CtrlShape.msg" "SausageFaceTemplate_hyperLayout14.hyp[462].dn"
		;
connectAttr "Tongue_02_Guide_Ctrl_Ctrl_CtrlShape.msg" "SausageFaceTemplate_hyperLayout14.hyp[463].dn"
		;
connectAttr "Tongue_02_Guide_Ctrl_Ctrl_Ctrl_CtrlShape.msg" "SausageFaceTemplate_hyperLayout14.hyp[464].dn"
		;
connectAttr "Tongue_03_Guide.msg" "SausageFaceTemplate_hyperLayout14.hyp[465].dn"
		;
connectAttr "Tongue_03_Guide_CtrlShape.msg" "SausageFaceTemplate_hyperLayout14.hyp[466].dn"
		;
connectAttr "Tongue_03_Guide_Ctrl_CtrlShape.msg" "SausageFaceTemplate_hyperLayout14.hyp[467].dn"
		;
connectAttr "Tongue_03_Guide_Ctrl_Ctrl_CtrlShape.msg" "SausageFaceTemplate_hyperLayout14.hyp[468].dn"
		;
connectAttr "Tongue_03_Guide_Ctrl_Ctrl_Ctrl_CtrlShape.msg" "SausageFaceTemplate_hyperLayout14.hyp[469].dn"
		;
connectAttr "Tongue_04_Guide.msg" "SausageFaceTemplate_hyperLayout14.hyp[470].dn"
		;
connectAttr "Tongue_04_Guide_CtrlShape.msg" "SausageFaceTemplate_hyperLayout14.hyp[471].dn"
		;
connectAttr "Tongue_04_Guide_Ctrl_CtrlShape.msg" "SausageFaceTemplate_hyperLayout14.hyp[472].dn"
		;
connectAttr "Tongue_04_Guide_Ctrl_Ctrl_CtrlShape.msg" "SausageFaceTemplate_hyperLayout14.hyp[473].dn"
		;
connectAttr "Tongue_04_Guide_Ctrl_Ctrl_Ctrl_CtrlShape.msg" "SausageFaceTemplate_hyperLayout14.hyp[474].dn"
		;
connectAttr "Tongue_05_Guide.msg" "SausageFaceTemplate_hyperLayout14.hyp[475].dn"
		;
connectAttr "Tongue_05_Guide_CtrlShape.msg" "SausageFaceTemplate_hyperLayout14.hyp[476].dn"
		;
connectAttr "Tongue_05_Guide_Ctrl_CtrlShape.msg" "SausageFaceTemplate_hyperLayout14.hyp[477].dn"
		;
connectAttr "Tongue_05_Guide_Ctrl_Ctrl_CtrlShape.msg" "SausageFaceTemplate_hyperLayout14.hyp[478].dn"
		;
connectAttr "Tongue_05_Guide_Ctrl_Ctrl_Ctrl_CtrlShape.msg" "SausageFaceTemplate_hyperLayout14.hyp[479].dn"
		;
connectAttr "Teeth_Lwr_Guide.msg" "SausageFaceTemplate_hyperLayout19.hyp[110].dn"
		;
connectAttr "Teeth_Lwr_Guide_CtrlShape.msg" "SausageFaceTemplate_hyperLayout19.hyp[111].dn"
		;
connectAttr "Teeth_Lwr_Guide_Ctrl_CtrlShape.msg" "SausageFaceTemplate_hyperLayout19.hyp[112].dn"
		;
connectAttr "Teeth_Lwr_Guide_Ctrl_Ctrl_CtrlShape.msg" "SausageFaceTemplate_hyperLayout19.hyp[113].dn"
		;
connectAttr "Teeth_Lwr_Guide_Ctrl_Ctrl_Ctrl_CtrlShape.msg" "SausageFaceTemplate_hyperLayout19.hyp[114].dn"
		;
connectAttr "Teeth_Upr_Guide.msg" "SausageFaceTemplate_hyperLayout19.hyp[115].dn"
		;
connectAttr "Teeth_Upr_Guide_CtrlShape.msg" "SausageFaceTemplate_hyperLayout19.hyp[116].dn"
		;
connectAttr "Teeth_Upr_Guide_Ctrl_CtrlShape.msg" "SausageFaceTemplate_hyperLayout19.hyp[117].dn"
		;
connectAttr "Teeth_Upr_Guide_Ctrl_Ctrl_CtrlShape.msg" "SausageFaceTemplate_hyperLayout19.hyp[118].dn"
		;
connectAttr "Teeth_Upr_Guide_Ctrl_Ctrl_Ctrl_CtrlShape.msg" "SausageFaceTemplate_hyperLayout19.hyp[119].dn"
		;
connectAttr "Nose_Origin_Guide.msg" "hyperLayout43.hyp[915].dn";
connectAttr "Nose_Origin_Guide_CtrlShape.msg" "hyperLayout43.hyp[916].dn";
connectAttr "Nose_Origin_Guide_Ctrl_CtrlShape.msg" "hyperLayout43.hyp[917].dn";
connectAttr "Nose_Origin_Guide_Ctrl_Ctrl_CtrlShape.msg" "hyperLayout43.hyp[918].dn"
		;
connectAttr "Nose_Origin_Guide_Ctrl_Ctrl_Ctrl_CtrlShape.msg" "hyperLayout43.hyp[919].dn"
		;
connectAttr "Nose_Bridge_Guide.msg" "hyperLayout43.hyp[920].dn";
connectAttr "Nose_Bridge_Guide_CtrlShape.msg" "hyperLayout43.hyp[921].dn";
connectAttr "Nose_Bridge_Guide_Ctrl_CtrlShape.msg" "hyperLayout43.hyp[922].dn";
connectAttr "Nose_Bridge_Guide_Ctrl_Ctrl_CtrlShape.msg" "hyperLayout43.hyp[923].dn"
		;
connectAttr "Nose_Bridge_Guide_Ctrl_Ctrl_Ctrl_CtrlShape.msg" "hyperLayout43.hyp[924].dn"
		;
connectAttr "Nose_Base_Guide.msg" "hyperLayout43.hyp[925].dn";
connectAttr "Nose_Base_Guide_CtrlShape.msg" "hyperLayout43.hyp[926].dn";
connectAttr "Nose_Base_Guide_Ctrl_CtrlShape.msg" "hyperLayout43.hyp[927].dn";
connectAttr "Nose_Base_Guide_Ctrl_Ctrl_CtrlShape.msg" "hyperLayout43.hyp[928].dn"
		;
connectAttr "Nose_Base_Guide_Ctrl_Ctrl_Ctrl_CtrlShape.msg" "hyperLayout43.hyp[929].dn"
		;
connectAttr "L_NoseNostril_Guide.msg" "hyperLayout43.hyp[930].dn";
connectAttr "L_NoseNostril_Guide_CtrlShape.msg" "hyperLayout43.hyp[931].dn";
connectAttr "L_NoseNostril_Guide_Ctrl_CtrlShape.msg" "hyperLayout43.hyp[932].dn"
		;
connectAttr "L_NoseNostril_Guide_Ctrl_Ctrl_CtrlShape.msg" "hyperLayout43.hyp[933].dn"
		;
connectAttr "L_NoseNostril_Guide_Ctrl_Ctrl_Ctrl_CtrlShape.msg" "hyperLayout43.hyp[934].dn"
		;
connectAttr "L_NoseNostrilEnd_Guide.msg" "hyperLayout43.hyp[935].dn";
connectAttr "L_NoseNostrilEnd_Guide_CtrlShape.msg" "hyperLayout43.hyp[936].dn";
connectAttr "L_NoseNostrilEnd_Guide_Ctrl_CtrlShape.msg" "hyperLayout43.hyp[937].dn"
		;
connectAttr "L_NoseNostrilEnd_Guide_Ctrl_Ctrl_CtrlShape.msg" "hyperLayout43.hyp[938].dn"
		;
connectAttr "L_NoseNostrilEnd_Guide_Ctrl_Ctrl_Ctrl_CtrlShape.msg" "hyperLayout43.hyp[939].dn"
		;
connectAttr "Nose_Tip_Guide.msg" "hyperLayout43.hyp[940].dn";
connectAttr "Nose_Tip_Guide_CtrlShape.msg" "hyperLayout43.hyp[941].dn";
connectAttr "Nose_Tip_Guide_Ctrl_CtrlShape.msg" "hyperLayout43.hyp[942].dn";
connectAttr "Nose_Tip_Guide_Ctrl_Ctrl_CtrlShape.msg" "hyperLayout43.hyp[943].dn"
		;
connectAttr "Nose_Tip_Guide_Ctrl_Ctrl_Ctrl_CtrlShape.msg" "hyperLayout43.hyp[944].dn"
		;
connectAttr "R_NoseNostril_Guide.msg" "hyperLayout43.hyp[945].dn";
connectAttr "R_NoseNostril_Guide_CtrlShape.msg" "hyperLayout43.hyp[946].dn";
connectAttr "R_NoseNostril_Guide_Ctrl_CtrlShape.msg" "hyperLayout43.hyp[947].dn"
		;
connectAttr "R_NoseNostril_Guide_Ctrl_Ctrl_CtrlShape.msg" "hyperLayout43.hyp[948].dn"
		;
connectAttr "R_NoseNostril_Guide_Ctrl_Ctrl_Ctrl_CtrlShape.msg" "hyperLayout43.hyp[949].dn"
		;
connectAttr "R_NoseNostrilEnd_Guide.msg" "hyperLayout43.hyp[950].dn";
connectAttr "R_NoseNostrilEnd_Guide_CtrlShape.msg" "hyperLayout43.hyp[951].dn";
connectAttr "R_NoseNostrilEnd_Guide_Ctrl_CtrlShape.msg" "hyperLayout43.hyp[952].dn"
		;
connectAttr "R_NoseNostrilEnd_Guide_Ctrl_Ctrl_CtrlShape.msg" "hyperLayout43.hyp[953].dn"
		;
connectAttr "R_NoseNostrilEnd_Guide_Ctrl_Ctrl_Ctrl_CtrlShape.msg" "hyperLayout43.hyp[954].dn"
		;
connectAttr "Nose_Top_Guide.msg" "hyperLayout43.hyp[955].dn";
connectAttr "Nose_Top_Guide_CtrlShape.msg" "hyperLayout43.hyp[956].dn";
connectAttr "Nose_Top_Guide_Ctrl_CtrlShape.msg" "hyperLayout43.hyp[957].dn";
connectAttr "Nose_Top_Guide_Ctrl_Ctrl_CtrlShape.msg" "hyperLayout43.hyp[958].dn"
		;
connectAttr "Nose_Top_Guide_Ctrl_Ctrl_Ctrl_CtrlShape.msg" "hyperLayout43.hyp[959].dn"
		;
connectAttr "reorder_Loc.msg" "hyperLayout42.hyp[8].dn";
connectAttr "reorder_LocShape.msg" "hyperLayout42.hyp[9].dn";
connectAttr "L_Brow_GuideShape.iog" ":initialShadingGroup.dsm" -na;
dataStructure -fmt "raw" -as "name=mapManager_pPlane3:string=value";
dataStructure -fmt "raw" -as "name=notes_juneBackYard:string=value";
dataStructure -fmt "raw" -as "name=notes_slopesMountainsGrass_Combined:string=value";
dataStructure -fmt "raw" -as "name=mapManager_baseScatt:string=value";
dataStructure -fmt "raw" -as "name=DiffArea:float=value";
dataStructure -fmt "raw" -as "name=notes_pPlane1:string=value";
dataStructure -fmt "raw" -as "name=notes_base_left:string=value";
dataStructure -fmt "raw" -as "name=notes_wildPatchA_parShape:string=value";
dataStructure -fmt "raw" -as "name=notes_decayGrassesCenter_parShape:string=value";
dataStructure -fmt "raw" -as "name=notes_wildPatchG_parShape:string=value";
dataStructure -fmt "raw" -as "name=notes_wildPatchH_parShape:string=value";
dataStructure -fmt "raw" -as "name=mapManager_trees_left:string=value";
dataStructure -fmt "raw" -as "name=notes_grass_c_geo:string=value";
dataStructure -fmt "raw" -as "name=notes_ferns_parShape:string=value";
dataStructure -fmt "raw" -as "name=idStructure:int32=ID";
dataStructure -fmt "raw" -as "name=notes_slopes_parShape:string=value";
dataStructure -fmt "raw" -as "name=notes_baseScatt:string=value";
dataStructure -fmt "raw" -as "name=f_3:float[3]=value";
dataStructure -fmt "raw" -as "name=notes_left_parShape:string=value";
dataStructure -fmt "raw" -as "name=mapManager_juneBackYard:string=value";
dataStructure -fmt "raw" -as "name=f_1:float=value";
dataStructure -fmt "raw" -as "name=notes_wildPatchF_parShape:string=value";
dataStructure -fmt "raw" -as "name=mapManager_grassBase:string=value";
dataStructure -fmt "raw" -as "name=mapManager_slopesGroundGrassC_Combined:string=value";
dataStructure -fmt "raw" -as "name=mapManager_grass_c_geo1:string=value";
dataStructure -fmt "raw" -as "name=notes_pPlane5:string=value";
dataStructure -fmt "raw" -as "name=DiffEdge:float=value";
dataStructure -fmt "raw" -as "name=faceConnectMarkerStructure:bool=faceConnectMarker:string[200]=faceConnectOutputGroups";
dataStructure -fmt "raw" -as "name=OffStruct:float=Offset";
dataStructure -fmt "raw" -as "name=notes_wildPatchD_parShape:string=value";
dataStructure -fmt "raw" -as "name=notes_grassBase:string=value";
dataStructure -fmt "raw" -as "name=notes_grass_c_geo1:string=value";
dataStructure -fmt "raw" -as "name=notes_wildPatchDegraded_parShape:string=value";
dataStructure -fmt "raw" -as "name=OrgStruct:float[3]=Origin Point";
dataStructure -fmt "raw" -as "name=notes_grassJuneBackYard_parShape:string=value";
dataStructure -fmt "raw" -as "name=notes_snapshot_floor:string=value";
dataStructure -fmt "raw" -as "name=mapManager_slopesGroundGrassD_Combined:string=value";
dataStructure -fmt "raw" -as "name=notes_snapshot_Combined:string=value";
dataStructure -fmt "raw" -as "name=notes_decayGrassPatchD_parShape:string=value";
dataStructure -fmt "raw" -as "name=notes_trees_left1:string=value";
dataStructure -fmt "raw" -as "name=mapManager_slopesGroundGrassB_Combined:string=value";
dataStructure -fmt "raw" -as "name=mapManager_groundWoods_c_geo1:string=value";
dataStructure -fmt "raw" -as "name=notes_groundB_parShape:string=value";
dataStructure -fmt "raw" -as "name=notes_floorOrangeConcrete_c_geo:string=value";
dataStructure -fmt "raw" -as "name=mapManager_base_left:string=value";
dataStructure -fmt "raw" -as "name=notes_decayGrassPatchC_parShape:string=value";
dataStructure -fmt "raw" -as "name=notes_suelo:string=value";
dataStructure -fmt "raw" -as "name=NameAndID:string=name:int32=ID";
dataStructure -fmt "raw" -as "name=notes_groundWoods_c_geo1:string=value";
dataStructure -fmt "raw" -as "name=mapManager_baseScatter:string=value";
dataStructure -fmt "raw" -as "name=notes_groundD_parShape:string=value";
dataStructure -fmt "raw" -as "name=notes_decayGrassPatchA_parShape:string=value";
dataStructure -fmt "raw" -as "name=notes_baseScatter:string=value";
dataStructure -fmt "raw" -as "name=notes_wildPatchE_parShape:string=value";
dataStructure -fmt "raw" -as "name=mapManager_ground_c_geo:string=value";
dataStructure -fmt "raw" -as "name=mapManager_degraded:string=value";
dataStructure -fmt "raw" -as "name=mapManager_grass_c_geo:string=value";
dataStructure -fmt "raw" -as "name=notes_pPlane6:string=value";
dataStructure -fmt "raw" -as "name=notes_decayLeavesCarousel_parShape:string=value";
dataStructure -fmt "raw" -as "name=notes_slopesGroundGrassB_Combined:string=value";
dataStructure -fmt "raw" -as "name=notes_wildPatchC_parShape:string=value";
dataStructure -fmt "raw" -as "name=mapManager_pPlane5:string=value";
dataStructure -fmt "raw" -as "name=mapManager_snapshot_Combined:string=value";
dataStructure -fmt "raw" -as "name=mapManager_ground:string=value";
dataStructure -fmt "raw" -as "name=mapManager_base_hojas:string=value";
dataStructure -fmt "raw" -as "name=notes_trees_left:string=value";
dataStructure -fmt "raw" -as "name=notes_groundA_parShape:string=value";
dataStructure -fmt "raw" -as "name=Curvature:float=mean:float=gaussian:float=ABS:float=RMS";
dataStructure -fmt "raw" -as "name=notes_pPlane2:string=value";
dataStructure -fmt "raw" -as "name=notes_bushes_parShape:string=value";
dataStructure -fmt "raw" -as "name=mapManager_trees_left1:string=value";
dataStructure -fmt "raw" -as "name=mapManager_slopesGroundGrassA_Combined:string=value";
dataStructure -fmt "raw" -as "name=Blur3dMetaData:string=Blur3dValue";
dataStructure -fmt "raw" -as "name=notes_slopesGroundGrassC_Combined:string=value";
dataStructure -fmt "raw" -as "name=mapManager_pPlane2:string=value";
dataStructure -fmt "raw" -as "name=notes_pPlane4:string=value";
dataStructure -fmt "raw" -as "name=notes_base_right:string=value";
dataStructure -fmt "raw" -as "name=notes_degraded:string=value";
dataStructure -fmt "raw" -as "name=notes_decayLeaves_parShape:string=value";
dataStructure -fmt "raw" -as "name=mapManager_suelo:string=value";
dataStructure -fmt "raw" -as "name=notes_widlPatchB_parShape:string=value";
dataStructure -fmt "raw" -as "name=mapManager_floorOrangeConcrete_c_geo:string=value";
dataStructure -fmt "raw" -as "name=notes_baseLeaves:string=value";
dataStructure -fmt "raw" -as "name=notes_polySurface56:string=value";
dataStructure -fmt "raw" -as "name=notes_ground:string=value";
dataStructure -fmt "raw" -as "name=notes_right_parShape:string=value";
dataStructure -fmt "raw" -as "name=mapManager_slopesMountainsGrass_Combined:string=value";
dataStructure -fmt "raw" -as "name=notes_decayGrassPatchB_parShape:string=value";
dataStructure -fmt "raw" -as "name=IdStruct:int32=ID";
dataStructure -fmt "raw" -as "name=mapManager_snapshot_floor:string=value";
dataStructure -fmt "raw" -as "name=notes_trees_parShape:string=value";
dataStructure -fmt "raw" -as "name=keyValueStructure:string=value";
dataStructure -fmt "raw" -as "name=notes_mountains_parShape:string=value";
dataStructure -fmt "raw" -as "name=mapManager_pPlane6:string=value";
dataStructure -fmt "raw" -as "name=notes_groundC_parShape:string=value";
dataStructure -fmt "raw" -as "name=mapManager_polySurface56:string=value";
dataStructure -fmt "raw" -as "name=mapManager_pPlane4:string=value";
dataStructure -fmt "raw" -as "name=notes_snapshot_CombinedGrass:string=value";
dataStructure -fmt "raw" -as "name=notes_ground_c_geo:string=value";
dataStructure -fmt "raw" -as "name=notes_base_hojas:string=value";
dataStructure -fmt "raw" -as "name=notes_slopesGroundGrassD_Combined:string=value";
dataStructure -fmt "raw" -as "name=notes_slopesGroundGrassA_Combined:string=value";
dataStructure -fmt "raw" -as "name=Offset:float[3]=value";
dataStructure -fmt "raw" -as "name=mapManager_pPlane1:string=value";
dataStructure -fmt "raw" -as "name=mapManager_snapshot_CombinedGrass:string=value";
dataStructure -fmt "raw" -as "name=mapManager_base_right:string=value";
dataStructure -fmt "raw" -as "name=mapManager_baseLeaves:string=value";
dataStructure -fmt "raw" -as "name=faceConnectOutputStructure:bool=faceConnectOutput:string[200]=faceConnectOutputAttributes:string[200]=faceConnectOutputGroups";
dataStructure -fmt "raw" -as "name=notes_pPlane3:string=value";
// End of humanFaceSimpleTemplate.ma
