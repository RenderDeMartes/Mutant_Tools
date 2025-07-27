//Maya ASCII 2024 scene
//Name: TortoiseTemplate.ma
//Last modified: Sat, Jul 26, 2025 02:17:32 PM
//Codeset: UTF-8
requires maya "2024";
requires "mtoa" "5.3.0";
requires "stereoCamera" "10.0";
currentUnit -l centimeter -a degree -t ntsc;
fileInfo "application" "maya";
fileInfo "product" "Maya 2024";
fileInfo "version" "2024";
fileInfo "cutIdentifier" "202302170737-4500172811";
fileInfo "osv" "Mac OS X 15.5";
fileInfo "UUID" "EFDCB95E-BD45-AFAE-AF2F-12B4C64967DE";
createNode transform -n "Mutant_Build";
	rename -uid "4E342371-724C-BFDC-3100-FBA73F2D648B";
createNode transform -n "Init" -p "Mutant_Build";
	rename -uid "B2F20144-8B43-3539-F51B-8CB812851ABF";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/C:\\Users\\Esteban\\Documents\\maya\\2022\\scripts\\rigging\\Mutant_Tools\\Icons\\Guide_Data";
createNode dagContainer -n "BaseA_Block" -p "Init";
	rename -uid "83428BE2-FB46-1571-0AF3-8F883C3E6AB3";
	addAttr -ci true -sn "nts" -ln "notes" -dt "string";
	setAttr ".isc" yes;
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/BaseA.png";
	setAttr ".ctor" -type "string" "PC";
	setAttr ".cdat" -type "string" "2021/09/17 18:07:43";
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
	setAttr ".nts" -type "string" "['Global_CtrlShape', 'Mover_Ctrl_tag', 'Extra_Geo_Grp', 'Mutant_Tools_Grp', 'Bind_Joints_Grp', 'Mover_CtrlShape', 'Global_Ctrl_Offset_Grp', 'Mover_Ctrl', 'Mover_Gimbal_CtrlShape', 'Mover_Gimbal_Ctrl', 'Template_Grp', 'Mover_Ctrl_Offset_Grp', 'Bind_Geo_Grp', 'Global_Ctrl', 'Rig_Ctrl_Grp', 'Miscellaneous_Grp', 'Ctrl_Grp', 'Mover_Gimbal_Ctrl_tag', 'Rig_Grp']";
createNode dagContainer -n "Root_Block" -p "Init";
	rename -uid "B694B781-6541-5CDA-AE80-8DB84F319824";
	addAttr -ci true -sn "nts" -ln "notes" -dt "string";
	setAttr ".isc" yes;
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/Root.png";
	setAttr ".ctor" -type "string" "PC";
	setAttr ".cdat" -type "string" "2021/09/17 18:10:22";
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
	setAttr ".nts" -type "string" "['Root']";
createNode transform -n "Spine" -p "Mutant_Build";
	rename -uid "F067C42A-8D4D-50F5-0088-259F42104DF6";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/";
createNode dagContainer -n "COG_Block" -p "Spine";
	rename -uid "42CD8595-A547-1FF9-DC61-6987618AC157";
	addAttr -ci true -sn "nts" -ln "notes" -dt "string";
	setAttr ".isc" yes;
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/Bone.png";
	setAttr ".ctor" -type "string" "PC";
	setAttr ".cdat" -type "string" "2021/09/17 18:10:39";
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
	setAttr ".nts" -type "string" "['COG_Jnt', 'COG_Ctrl', 'COG_Ctrl_Offset_Grp', 'COG_Ctrl_tag', 'COG_CtrlShape', 'COG_Bnd_scaleConstraint1', 'COG_Gimbal_CtrlShape', 'COG_Gimbal_Ctrl', 'COG_Jnt_scaleConstraint1', 'COG_Rig_Grp', 'COG_Bnd_parentConstraint1', 'COG_Gimbal_Ctrl_tag', 'COG_Bnd', 'COG_Jnt_parentConstraint1']";
createNode transform -n "COG_Loc" -p "COG_Block";
	rename -uid "2858D69E-A348-2E5A-DCEA-73B14D037154";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/C:\\Users\\Esteban\\Documents\\maya\\2022\\scripts\\rigging\\Mutant_Tools\\Icons\\Guide_Data";
	setAttr ".t" -type "double3" 0 25.162879467010498 -2.2115688323974609 ;
createNode locator -n "COG_LocShape" -p "COG_Loc";
	rename -uid "145C34DE-AF48-6521-4A2D-EAA2DA08DBA6";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/C:\\Users\\Esteban\\Documents\\maya\\2022\\scripts\\rigging\\Mutant_Tools\\Icons\\Guide_Data";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 9;
	setAttr ".los" -type "double3" 2 2 2 ;
createNode transform -n "Body" -p "Mutant_Build";
	rename -uid "0FC79E19-4142-EAA0-FBD0-0CB45013AEA3";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/C:\\Users\\Esteban\\Documents\\maya\\2022\\scripts\\rigging\\Mutant_Tools\\Icons\\Guide_Data";
createNode dagContainer -n "L_Clavicle_Block" -p "Body";
	rename -uid "FC2E0ADE-614E-D60C-A537-D9BEEB666EDA";
	addAttr -ci true -sn "nts" -ln "notes" -dt "string";
	setAttr ".isc" yes;
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/Clavicle.png";
	setAttr ".ctor" -type "string" "PC";
	setAttr ".cdat" -type "string" "2021/09/18 07:03:11";
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
	setAttr ".nts" -type "string" "['R_Clavicle_Jnt', 'L_Clavicle_Bnd_scaleConstraint1', 'R_Clavicle_Ctrl_Offset_Grp', 'L_Clavicle_Ctrl_AutoFK_Grp', 'L_Clavicle_Jnt_scaleConstraint1', 'R_Clavicle_Ctrl', 'L_Clavicle_Bnd_parentConstraint1', 'L_Clavicle_CtrlShape', 'R_Clavicle_JntMirror_Grp', 'R_Clavicle_Bnd', 'R_Clavicle_Jnt_parentConstraint1', 'R_Clavicle_Jnt_Ctrl_tag', 'R_Clavicle_JntMirror_Grp_scaleConstraint1', 'R_Clavicle_Bnd_parentConstraint1', 'R_Clavicle_Bnd_scaleConstraint1', 'L_Clavicle_Bnd', 'L_Clavicle_Ctrl', 'L_Clavicle_Jnt_Ctrl_tag', 'R_Clavicle_Ctrl_AutoFK_Grp', 'L_Clavicle_Jnt', 'R_Clavicle_Jnt_scaleConstraint1', 'R_Clavicle_CtrlShape', 'R_ClavicleEnd_Jnt', 'L_Clavicle_Jnt_parentConstraint1', 'L_ClavicleEnd_Jnt', 'L_Clavicle_Ctrl_Offset_Grp_parentConstraint1', 'L_Clavicle_Ctrl_Offset_Grp', 'R_Clavicle_Ctrl_AutoFK_Grp_parentConstraint1', 'R_Clavicle_Ctrl_Offset_GrpMirror_Grp']";
createNode joint -n "L_Clavicle_Guide" -p "L_Clavicle_Block";
	rename -uid "6DC10370-EA49-D4B3-5F89-229576EDAC34";
	addAttr -ci true -sn "Helper" -ln "Helper" -min 0 -max 1 -en "Hide:Show" -at "enum";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/C:\\Users\\Esteban\\Documents\\maya\\2022\\scripts\\rigging\\Mutant_Tools\\Icons\\Guide_Data";
	setAttr ".t" -type "double3" 3.0195496514783597 23.460465270630664 20.516281882542259 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 90 -3.5353859000104677 3.4647768230323037 ;
	setAttr -cb on ".Helper" 1;
createNode nurbsCurve -n "L_Clavicle_Guide_CtrlShape" -p "L_Clavicle_Guide";
	rename -uid "8C3BCECE-E745-7877-3116-7691F8228555";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/C:\\Users\\Esteban\\Documents\\maya\\2022\\scripts\\rigging\\Mutant_Tools\\Icons\\Guide_Data";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 14;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 9 0 no 3
		10 0 1 2 3 4 5 6 7 8 9
		10
		5.8966734348899621e-06 -0.21093750000000649 0.10546875000001396
		5.8966734351005649e-06 0.39872714062499426 0.10796456250001106
		5.8966734350315597e-06 0.31204110937499396 0.21365564062501169
		5.8966734350009869e-06 0.41773218749999452 0.39620432812501172
		5.8212421853385373e-06 0.97001803124999508 1.6344703939433537e-07
		5.8966734352928651e-06 0.41773260937499407 -0.39620432812499029
		5.8966734351889554e-06 0.31204110937499363 -0.2136552187499893
		3.0237721851796828e-06 0.39872714062499437 -0.10682760937498942
		5.8966734349676638e-06 -0.21093750000000666 -0.10546874999998654
		5.8966734348899621e-06 -0.21093750000000649 0.10546875000001396
		;
createNode nurbsCurve -n "L_Clavicle_Guide_Ctrl_CtrlShape" -p "L_Clavicle_Guide";
	rename -uid "919B1BC6-2E4F-D808-9380-6282E0C7819F";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/C:\\Users\\Esteban\\Documents\\maya\\2022\\scripts\\rigging\\Mutant_Tools\\Icons\\Guide_Data";
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
		-2.4110290424306941e-15 0.25068192187499383 1.1531576948933328e-14
		-1.2973144596343903e-09 0.24687365624999405 0.043530328125011591
		-2.5552022916052888e-09 0.23556403124999414 0.085738500000011666
		-3.7354566875995891e-09 0.21709729687499416 0.12534117187501187
		-4.8022056157298898e-09 0.1920337031249941 0.16113557812501197
		-5.723032200331087e-09 0.161135156249994 0.19203370312501247
		-6.4700040969816186e-09 0.12534117187499402 0.21709729687501259
		-7.0203822425236443e-09 0.085738499999993917 0.23556403125001288
		-7.3574181988333695e-09 0.043530328124993883 0.24687365625001306
		-7.4709025903388811e-09 -6.1433582355931998e-15 0.25068234375001303
		-7.3574182290386058e-09 -0.043530328125006165 0.2468736562500134
		-7.0203823020166808e-09 -0.085738500000006185 0.23556403125001366
		-6.470004183954529e-09 -0.12534117187500624 0.21709729687501381
		-5.7230323121410639e-09 -0.16113515625000621 0.19203370312501397
		-4.8022057489800342e-09 -0.19203370312500659 0.16113557812501392
		-3.7354568382410983e-09 -0.21709729687500648 0.12534117187501387
		-2.5552024550606711e-09 -0.23556403125000652 0.08573850000001397
		-1.2973146309374013e-09 -0.24687365625000654 0.043530328125013937
		-2.5849745683825139e-15 -0.2506819218750066 1.3892530314982703e-14
		-2.5676192191825037e-15 -0.24687365625000654 -0.043530328124986167
		-2.5481483201399038e-15 -0.23556403125000663 -0.085738499999986242
		-2.5271540176526727e-15 -0.21709729687500665 -0.12534117187498645
		-2.5052737177846541e-15 -0.19203370312500659 -0.16113557812498655
		-2.4831725228066614e-15 -0.16113515625000649 -0.19203370312498705
		-2.4615219905003881e-15 -0.12534117187500651 -0.21709729687498716
		-2.4409798058470304e-15 -0.085738500000006407 -0.23556445312498747
		-2.4221702387167801e-15 -0.043530328125006373 -0.24687365624998764
		-2.4056647189146738e-15 -6.3587938366427542e-15 -0.2506823437499876
		-2.3919650058706155e-15 0.043530328124993675 -0.24687365624998797
		-2.3814867703490151e-15 0.085738499999993695 -0.23556445312498825
		-2.3745490811571872e-15 0.12534117187499375 -0.21709729687498838
		-2.3713625474658343e-15 0.16113515624999372 -0.19203370312498855
		-2.3720235685887763e-15 0.1920337031249941 -0.16113557812498849
		-2.3765125066686057e-15 0.21709729687499399 -0.12534117187498844
		-2.3846929380978587e-15 0.23556403124999403 -0.085738499999988546
		-2.3963162083436612e-15 0.24687365624999405 -0.043530328124988513
		-2.4110290424306941e-15 0.25068192187499383 1.1531576948933328e-14
		0.043530328124997533 0.24687365624999391 1.2719511086560109e-14
		0.08573849999999747 0.23556403124999381 1.3907232898162669e-14
		0.12534117187499744 0.21709729687499371 1.5058627793455776e-14
		0.16113557812499738 0.19203370312499371 1.6138729789969876e-14
		0.19203370312499746 0.16113515624999339 1.7114707524520186e-14
		0.2170972968749974 0.12534117187499336 1.7956918635461291e-14
		0.23556403124999742 0.085738499999993195 1.863975582369474e-14
		0.24687365624999735 0.043530328124993155 1.9142494900312168e-14
		0.25068192187499722 -6.8929350364446312e-15 1.9449839827042599e-14
		0.24687365624999735 -0.043530328125006894 1.9552468918156179e-14
		0.23556403124999742 -0.085738500000006906 1.9447251628182656e-14
		0.2170972968749974 -0.1253411718750069 1.9137397305121455e-14
		0.19203370312499746 -0.16113515625000682 1.8632298369092652e-14
		0.16113557812499732 -0.19203370312500698 1.7947326973192244e-14
		0.12534117187499733 -0.21709729687500692 1.7103277004629586e-14
		0.085738499999997331 -0.23556403125000686 1.6125804099229073e-14
		0.043530328124997367 -0.24687365625000668 1.5044597735620484e-14
		-2.5849745683825139e-15 -0.2506819218750066 1.3892530314982703e-14
		-0.043530328125002529 -0.2468736562500064 1.2704596177355923e-14
		-0.085738500000002466 -0.2355640312500063 1.1516874365753363e-14
		-0.12534117187500243 -0.2170972968750062 1.0365479470460268e-14
		-0.16113557812500237 -0.1920337031250062 9.2853774739461709e-15
		-0.19203370312500245 -0.16113515625000588 8.3093997393958561e-15
		-0.2170972968750024 -0.12534117187500585 7.4671886284547477e-15
		-0.23556403125000241 -0.085738500000005685 6.7843514402212822e-15
		-0.24687365625000235 -0.043530328125005645 6.2816123636038664e-15
		-0.25068234375000226 -5.6092159747295793e-15 5.9742560977886999e-15
		-0.24687365625000235 0.043530328124994404 5.871638345759847e-15
		-0.23556403125000241 0.085738499999994416 5.976855635733392e-15
		-0.2170972968750024 0.12534117187499441 6.2867099587945708e-15
		-0.19203370312500245 0.16113515624999433 6.7918088948233823e-15
		-0.16113557812500232 0.19203370312499449 7.4767802907237948e-15
		-0.12534117187500232 0.21709729687499443 8.3208302592864531e-15
		-0.085738500000002327 0.23556403124999437 9.2983031646869743e-15
		-0.043530328125002363 0.24687365624999419 1.0379509528295558e-14
		-2.4110290424306941e-15 0.25068192187499383 1.1531576948933328e-14
		-1.2973144596343903e-09 0.24687365624999405 0.043530328125011591
		-2.5552022916052888e-09 0.23556403124999414 0.085738500000011666
		-3.7354566875995891e-09 0.21709729687499416 0.12534117187501187
		-4.8022056157298898e-09 0.1920337031249941 0.16113557812501197
		-5.723032200331087e-09 0.161135156249994 0.19203370312501247
		-6.4700040969816186e-09 0.12534117187499402 0.21709729687501259
		-7.0203822425236443e-09 0.085738499999993917 0.23556403125001288
		-7.3574181988333695e-09 0.043530328124993883 0.24687365625001306
		-7.4709025903388811e-09 -6.1433582355931998e-15 0.25068234375001303
		-0.077465109375002492 -5.9502847090497911e-15 0.23841295312501123
		-0.14734743750000245 -5.7866545010454113e-15 0.20280628125000935
		-0.20280628125000247 -5.6684853759158178e-15 0.14734743750000742
		-0.23841295312500244 -5.6073445285230079e-15 0.077465109375006377
		-0.25068234375000226 -5.6092159747295793e-15 5.9742560977886999e-15
		-0.23841295312500244 -5.6739177887977524e-15 -0.077465109374993776
		-0.20280628125000241 -5.795115279192893e-15 -0.14734743749999293
		-0.14734743750000223 -5.9609455522804927e-15 -0.20280628124999164
		-0.077465109375002325 -6.1551760170117656e-15 -0.23841295312498997
		-2.4056647189146738e-15 -6.3587938366427542e-15 -0.2506823437499876
		0.077465109374997496 -6.5518673823150458e-15 -0.23841295312498581
		0.14734743749999746 -6.7154975903194216e-15 -0.20280628124998393
		0.20280628124999747 -6.8336667154490136e-15 -0.147347437499982
		0.23841295312499744 -6.8948075628418266e-15 -0.077465109374980953
		0.25068192187499722 -6.8929350364446312e-15 1.9449839827042599e-14
		0.23841295312499744 -6.8282343025670821e-15 0.0774651093750192
		0.20280628124999742 -6.70703681217194e-15 0.14734743750001836
		0.14734743749999724 -6.5412065390843402e-15 0.20280628125001707
		0.077465109374997329 -6.3469760743530713e-15 0.2384129531250154
		-7.4709025903388811e-09 -6.1433582355931998e-15 0.25068234375001303
		;
createNode nurbsCurve -n "L_Clavicle_Guide_Ctrl_Ctrl_CtrlShape" -p "L_Clavicle_Guide";
	rename -uid "7A4AAA33-7846-D9AE-ED16-61974EC5233F";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/C:\\Users\\Esteban\\Documents\\maya\\2022\\scripts\\rigging\\Mutant_Tools\\Icons\\Guide_Data";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 13;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 9 0 no 3
		10 0 1 2 3 4 5 6 7 8 9
		10
		-0.21093750000000244 -0.10546875000000584 -5.8966734299608452e-06
		0.39872714062499742 -0.10796456250000737 -5.8966734135626287e-06
		0.31204110937499713 -0.21365564062500739 -5.8966734153948559e-06
		0.4177321874999973 -0.39620432812500794 -5.8966734116944781e-06
		0.97001803124999708 -1.6344703998476321e-07 -5.8212421487159794e-06
		0.41773260937499751 0.39620432812499329 -5.8966734154259665e-06
		0.31204110937499713 0.21365521874999327 -5.8966734174070902e-06
		0.39872714062499742 0.10682760937499294 -3.0237721645740905e-06
		-0.21093750000000244 0.10546874999999449 -5.8966734309541616e-06
		-0.21093750000000244 -0.10546875000000584 -5.8966734299608452e-06
		;
createNode nurbsCurve -n "L_Clavicle_Guide_Ctrl_Ctrl_Ctrl_CtrlShape" -p "L_Clavicle_Guide";
	rename -uid "23764065-1241-E69D-7581-76B77F3536E0";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/C:\\Users\\Esteban\\Documents\\maya\\2022\\scripts\\rigging\\Mutant_Tools\\Icons\\Guide_Data";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 6;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 9 0 no 3
		10 0 1 2 3 4 5 6 7 8 9
		10
		0.10546874999999754 5.8966734308882481e-06 -0.21093749999998493
		0.10796456249999727 5.8966734311438293e-06 0.39872714062501657
		0.21365564062499726 5.8966734308359599e-06 0.31204110937501878
		0.39620432812499712 5.8966734304139698e-06 0.41773218750002444
		1.6344702839470069e-07 5.8212421816657491e-06 0.97001803125001496
		-0.39620432812500256 5.8966734324428932e-06 0.41773260937500301
		-0.21365521875000257 5.896673431930074e-06 0.31204110937500734
		-0.10682760937500263 3.0237721816937902e-06 0.39872714062501102
		-0.1054687500000024 5.8966734314283434e-06 -0.21093749999999065
		0.10546874999999754 5.8966734308882481e-06 -0.21093749999998493
		;
createNode joint -n "L_ClavicleEnd_Guide" -p "L_Clavicle_Guide";
	rename -uid "AB9400DC-4341-F269-5FCB-D39B21E92EC8";
	addAttr -ci true -sn "Helper" -ln "Helper" -min 0 -max 1 -en "Hide:Show" -at "enum";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/C:\\Users\\Esteban\\Documents\\maya\\2022\\scripts\\rigging\\Mutant_Tools\\Icons\\Guide_Data";
	setAttr ".t" -type "double3" 12.035935419682772 1.7538376571406152e-15 2.3849963451907463e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" -90.121066396585249 -3.4626636004333933 -1.5317264681631078 ;
	setAttr -cb on ".Helper" 1;
createNode nurbsCurve -n "L_ClavicleEnd_Guide_CtrlShape" -p "L_ClavicleEnd_Guide";
	rename -uid "2EEC8996-3041-51B7-FDFF-26A6F97C54A2";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/C:\\Users\\Esteban\\Documents\\maya\\2022\\scripts\\rigging\\Mutant_Tools\\Icons\\Guide_Data";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 14;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 9 0 no 3
		10 0 1 2 3 4 5 6 7 8 9
		10
		5.8966734470033108e-06 -0.21093750000034403 0.10546874999996235
		5.8966734467946645e-06 0.39872714062465675 0.10796456249996192
		5.8966734468358685e-06 0.31204110937465662 0.21365564062496217
		5.8966734468195089e-06 0.41773218749965785 0.3962043281249622
		5.821242196587162e-06 0.97001803124965658 1.6344699259464544e-07
		5.8966734467333182e-06 0.41773260937465467 -0.39620432812503892
		5.8966734467893892e-06 0.31204110937465485 -0.21365521875003834
		3.0237721967713024e-06 0.39872714062465597 -0.10682760937503831
		5.8966734469803663e-06 -0.21093750000034492 -0.1054687500000379
		5.8966734470033108e-06 -0.21093750000034403 0.10546874999996235
		;
createNode nurbsCurve -n "L_ClavicleEnd_Guide_Ctrl_CtrlShape" -p "L_ClavicleEnd_Guide";
	rename -uid "12039856-7444-3E5C-6997-90B8FE8FFBB4";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/C:\\Users\\Esteban\\Documents\\maya\\2022\\scripts\\rigging\\Mutant_Tools\\Icons\\Guide_Data";
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
		9.3336479774102478e-15 0.25068192187465577 -3.8092806576813407e-14
		-1.2973026915622541e-09 0.24687365624965613 0.043530328124961888
		-2.5551904955958277e-09 0.23556403124965636 0.085738499999961859
		-3.7354448599602922e-09 0.21709729687465645 0.12534117187496177
		-4.8021937537284582e-09 0.19203370312465662 0.16113557812496182
		-5.7230203022797545e-09 0.16113515624965657 0.19203370312496237
		-6.4699921622881619e-09 0.12534117187465671 0.21709729687496224
		-7.0203702717089862e-09 0.085738499999656714 0.23556403124996228
		-7.3574061935154778e-09 0.043530328124656771 0.24687365624996233
		-7.470890553184768e-09 -3.4320674051236399e-13 0.25068234374996179
		-7.3574061636826383e-09 -0.043530328125343222 0.24687365624996238
		-7.0203702129494255e-09 -0.085738500000343276 0.23556403124996245
		-6.4699920763875166e-09 -0.12534117187534327 0.21709729687496246
		-5.7230201918482575e-09 -0.16113515625034341 0.19203370312496248
		-4.802193622121116e-09 -0.19203370312534385 0.16113557812496221
		-3.735444711176002e-09 -0.21709729687534396 0.12534117187496216
		-2.5551903341556484e-09 -0.23556403125034409 0.08573849999996222
		-1.2973025223711973e-09 -0.24687365625034424 0.043530328124962263
		9.505448971697994e-15 -0.2506819218753441 -3.7700731535565514e-14
		9.4994092047693706e-15 -0.24687365625034458 -0.043530328125037675
		9.4909427783713555e-15 -0.23556403125034481 -0.08573850000003766
		9.4803072451700265e-15 -0.2170972968753449 -0.1253411718750376
		9.4678254094761379e-15 -0.19203370312534512 -0.16113557812503759
		9.4538766952322378e-15 -0.16113515625034502 -0.19203370312503815
		9.438885097281302e-15 -0.12534117187534516 -0.21709729687503801
		9.4233058819419078e-15 -0.085738500000345219 -0.2355644531250381
		9.4076124183447318e-15 -0.043530328125345262 -0.2468736562500381
		9.3922817269894363e-15 -3.452841902229655e-13 -0.25068234375003773
		9.3777795783951595e-15 0.043530328124654731 -0.24687365625003815
		9.3645463214655483e-15 0.085738499999654771 -0.23556445312503826
		9.3529844555746686e-15 0.12534117187465482 -0.21709729687503823
		9.3434451976140421e-15 0.16113515624965496 -0.19203370312503826
		9.3362180686401115e-15 0.19203370312465534 -0.16113557812503798
		9.3315229563735371e-15 0.21709729687465551 -0.12534117187503799
		9.3295025975857553e-15 0.23556403124965564 -0.08573850000003802
		9.3302181466748518e-15 0.24687365624965579 -0.043530328125038049
		9.3336479774102478e-15 0.25068192187465577 -3.8092806576813407e-14
		0.043530328125009309 0.24687365624965468 -3.8200662113983861e-14
		0.085738500000009293 0.23556403124965361 -3.8299285085364369e-14
		0.12534117187500926 0.2170972968746526 -3.8385677146434751e-14
		0.16113557812500928 0.19203370312465165 -3.8457214030338496e-14
		0.19203370312500967 0.16113515624965058 -3.8511721336698744e-14
		0.2170972968750097 0.12534117187464996 -3.854754488071894e-14
		0.23556403125000969 0.085738499999649526 -3.8563593536504382e-14
		0.24687365625000968 0.043530328124649208 -3.8559381750470232e-14
		0.25068192187500926 -3.5089443091700287e-13 -3.8535036615624548e-14
		0.24687365625000968 -0.043530328125350785 -3.8491298838597344e-14
		0.23556403125000969 -0.085738500000350465 -3.8429495610046033e-14
		0.21709729687500975 -0.12534117187535002 -3.8351507030181574e-14
		0.19203370312500972 -0.16113515625034941 -3.8259700478709994e-14
		0.16113557812500939 -0.19203370312534881 -3.8156866795441899e-14
		0.12534117187500943 -0.21709729687534782 -3.8046129599525815e-14
		0.08573850000000946 -0.23556403125034683 -3.7930854938594865e-14
		0.043530328125009475 -0.24687365625034569 -3.7814543329536755e-14
		9.505448971697994e-15 -0.2506819218753441 -3.7700731535565514e-14
		-0.043530328124990469 -0.2468736562503433 -3.759287599839506e-14
		-0.085738499999990461 -0.23556403125034217 -3.7494253027014558e-14
		-0.12534117187499041 -0.2170972968753411 -3.740786096594417e-14
		-0.16113557812499044 -0.19203370312534021 -3.7336324082040424e-14
		-0.19203370312499082 -0.16113515625033908 -3.7281816775680196e-14
		-0.21709729687499082 -0.12534117187533847 -3.724599323165998e-14
		-0.23556403124999087 -0.085738500000338003 -3.7229944575874532e-14
		-0.24687365624999086 -0.043530328125337699 -3.7234156361908689e-14
		-0.25068234374999043 -3.3759648882687372e-13 -3.7258500422607796e-14
		-0.24687365624999086 0.043530328124662294 -3.730223927378159e-14
		-0.23556403124999087 0.085738499999661988 -3.7364042502332888e-14
		-0.21709729687499088 0.12534117187466151 -3.7442031082197353e-14
		-0.19203370312499088 0.1611351562496609 -3.7533837633668933e-14
		-0.16113557812499055 0.19203370312466025 -3.7636671316937027e-14
		-0.12534117187499058 0.21709729687465931 -3.77474085128531e-14
		-0.085738499999990628 0.23556403124965827 -3.7862683173784049e-14
		-0.043530328124990636 0.24687365624965707 -3.7978994782842159e-14
		9.3336479774102478e-15 0.25068192187465577 -3.8092806576813407e-14
		-1.2973026915622541e-09 0.24687365624965613 0.043530328124961888
		-2.5551904955958277e-09 0.23556403124965636 0.085738499999961859
		-3.7354448599602922e-09 0.21709729687465645 0.12534117187496177
		-4.8021937537284582e-09 0.19203370312465662 0.16113557812496182
		-5.7230203022797545e-09 0.16113515624965657 0.19203370312496237
		-6.4699921622881619e-09 0.12534117187465671 0.21709729687496224
		-7.0203702717089862e-09 0.085738499999656714 0.23556403124996228
		-7.3574061935154778e-09 0.043530328124656771 0.24687365624996233
		-7.470890553184768e-09 -3.4320674051236399e-13 0.25068234374996179
		-0.077465109374990529 -3.4120293312144376e-13 0.23841295312496263
		-0.14734743749999055 -3.3949694765281455e-13 0.20280628124996281
		-0.20280628124999084 -3.382557829263371e-13 0.14734743749996246
		-0.23841295312499089 -3.3760093255746516e-13 0.077465109374962648
		-0.25068234374999043 -3.3759648882687372e-13 -3.7258500422607796e-14
		-0.23841295312499089 -3.3824289980292567e-13 -0.0774651093750372
		-0.20280628124999084 -3.3947687754997745e-13 -0.14734743750003729
		-0.14734743749999055 -3.411776396544983e-13 -0.2028062812500378
		-0.077465109374990557 -3.4317870399473888e-13 -0.23841295312503802
		9.3922817269894363e-15 -3.452841902229655e-13 -0.25068234375003773
		0.077465109375009361 -3.4728799781203996e-13 -0.23841295312503846
		0.14734743750000937 -3.4899398328066947e-13 -0.20280628125003863
		0.20280628125000966 -3.5023514800714692e-13 -0.14734743750003829
		0.23841295312500971 -3.5088999837601891e-13 -0.077465109375038449
		0.25068192187500926 -3.5089443091700287e-13 -3.8535036615624548e-14
		0.23841295312500971 -3.502480311305583e-13 0.077465109374961399
		0.20280628125000966 -3.4901405338350657e-13 0.14734743749996146
		0.14734743750000937 -3.4731329127898568e-13 0.20280628124996197
		0.077465109375009389 -3.4531222693874494e-13 0.23841295312496219
		-7.470890553184768e-09 -3.4320674051236399e-13 0.25068234374996179
		;
createNode nurbsCurve -n "L_ClavicleEnd_Guide_Ctrl_Ctrl_CtrlShape" -p "L_ClavicleEnd_Guide";
	rename -uid "487BC6B1-1545-12DA-3FCC-7CA849BF3455";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/C:\\Users\\Esteban\\Documents\\maya\\2022\\scripts\\rigging\\Mutant_Tools\\Icons\\Guide_Data";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 13;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 9 0 no 3
		10 0 1 2 3 4 5 6 7 8 9
		10
		-0.21093749999999084 -0.10546875000033877 -5.896673474777228e-06
		0.39872714062501002 -0.10796456250035494 -5.8966734763275575e-06
		0.31204110937500934 -0.21365564062535275 -5.8966734760241935e-06
		0.41773218750001012 -0.39620432812535566 -5.8966734761505378e-06
		0.97001803125001063 -1.6344740122377638e-07 -5.8212422278665649e-06
		0.41773260937501 0.39620432812464512 -5.8966734767702169e-06
		0.31204110937500923 0.21365521874964771 -5.8966734763583565e-06
		0.39872714062501002 0.10682760937464528 -3.0237722264955227e-06
		-0.2109374999999909 0.10546874999966145 -5.8966734749421852e-06
		-0.21093749999999084 -0.10546875000033877 -5.896673474777228e-06
		;
createNode nurbsCurve -n "L_ClavicleEnd_Guide_Ctrl_Ctrl_Ctrl_CtrlShape" -p "L_ClavicleEnd_Guide";
	rename -uid "1DCCED88-8F49-23C2-7EC5-22AB9AFB1476";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/C:\\Users\\Esteban\\Documents\\maya\\2022\\scripts\\rigging\\Mutant_Tools\\Icons\\Guide_Data";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 6;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 9 0 no 3
		10 0 1 2 3 4 5 6 7 8 9
		10
		0.10546875000000953 5.8966730895831008e-06 -0.21093750000003847
		0.10796456250000959 5.8966730920431047e-06 0.3987271406249624
		0.21365564062500966 5.8966730888806157e-06 0.31204110937496116
		0.39620432812500994 5.8966730844767212e-06 0.4177321874999616
		1.6344704077505532e-07 5.8212418472738933e-06 0.97001803124996322
		-0.39620432812499112 5.8966731054941836e-06 0.41773260937496354
		-0.21365521874999086 5.8966731002143993e-06 0.31204110937496238
		-0.10682760937499068 3.0237718477401435e-06 0.39872714062496306
		-0.10546874999999074 5.8966730951779042e-06 -0.21093750000003786
		0.10546875000000953 5.8966730895831008e-06 -0.21093750000003847
		;
createNode dagContainer -n "L_FrHip_Block" -p "Body";
	rename -uid "0883CD2E-2542-2AA1-F65F-199607B987F9";
	addAttr -ci true -sn "nts" -ln "notes" -dt "string";
	setAttr ".isc" yes;
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/Limb.png";
	setAttr ".ctor" -type "string" "PC";
	setAttr ".cdat" -type "string" "2021/09/18 08:13:30";
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
		"['L_FrHipEnd_Bendy_Ctrl_Auto_Grp', 'L_FrAnkle_Ik_IKrp_NormalScale_LocShape', 'L_FrHip_Ctrl_1_Ctrl_Auto_Grp_parentConstraint1', 'R_FrHip_Ik_Jnt_Volume_Blend', 'R_FrKnee_Ctrl_1_Ctrl_tag', 'skinCluster2GroupParts', 'L_FrHip_Ctrl_3_Ctrl_Auto_Grp', 'L_FrKnee_Ctrl_2_CtrlShape', 'R_FrHip_Ctrl_2_CtrlShape', 'L_FrHip_BendyMid_0_Jnt', 'L_FrAnkle_Ik_IKrp_Grp', 'R_FrHip_Jnt_2_Jnt', 'R_FrKnee_Jnt_Bendy_BS', 'R_FrAnkle_Fk_Jnt_scale_Blend', 'R_FrHip_Bnd_0_Bnd_scaleConstraint1', 'R_FrAnkle_Fk_Jnt_rotate_Blend', 'R_FrHip_Fk_Jnt_translate_Blend', 'L_FrAnkle_Fk_Jnt_rotate_Blend', 'unitConversion30', 'L_FrHip_BendyMid_3_Jnt_Auto_Grp', 'skinCluster15GroupParts', 'L_FrKnee_Bnd_1_Bnd', 'R_FrHip_Ctrl_0_Ctrl_tag', 'Mutant_Rig', 'L_FrKnee_Aim_Loc_0_Aim_Loc_aimConstraint1', 'skinCluster8Set', 'R_FrAnkle_Ik_PoleVector_Ctrl_R_FrKnee_Ik_Jnt_Connected_Crv', 'L_FrAnkle_Fk_Jnt_Ctrl_tag', 'L_FrHip_Fk_Ctrl_Offset_Grp_parentConstraint1', 'R_FrKnee_Bnd_0_Bnd_parentConstraint1', 'L_FrHip_JntBendy_IK_Local_Nurb', 'L_FrHip_Jnt_Bendy_BS', 'R_FrHip_Ctrl_1_Ctrl_Auto_Grp_aimConstraint1', 'L_FrKneeMid_Bendy_Ctrl_MultDiv', 'R_FrKnee_Bottom_Handle_Ctrl_Offset_Grp', 'R_FrKnee_JntBendy_Nurb', 'unitConversion61', 'R_FrKnee_Ctrl_1_Ctrl_Auto_Grp', 'L_FrHip_Aim_Loc_0_Aim_Loc', 'L_FrAnkle_Fk_Jnt_parentConstraint1', 'R_FrHip_Twist_2_Jnt', 'R_FrKnee_Aim_Loc_0_Aim_Loc_Offset_Grp_parentConstraint1', 'L_FrHip_JntBendy_NurbShape', 'R_FrKnee_Jnt_Bendy_BSGroupId', 'R_FrKnee_Jnt_1_Jnt_parentConstraint1', 'skinCluster14Set', 'R_FrKnee_JntBendy_NurbFollicleShape5050', 'R_FrHip_Bottom_Handle_Ctrl', 'L_FrHip_Ctrl_3_CtrlShape', 'L_FrHip_Aim_Loc_2_Aim_Loc', 'R_FrKnee_NoRotate_JntCtrl_Offset_Grp', 'L_FrHip_Ik_Jnt_L_FrKnee_Ik_Jnt_Distance', 'L_FrKnee_Fk_Jnt_rotate_Blend', 'R_FrKnee_JntBendy_NurbFollicleShape1750', 'R_FrAnkle_Ik_PoleVector_Ctrl', 'skinCluster13GroupId', 'L_FrHip_JntBendy_NurbShapeOrig', 'L_FrHip_Ctrl_3_Ctrl_Root_Grp_parentConstraint1', 'R_FrAnkle_Ik_IKrp_poleVectorConstraint1', 'R_FrHip_Handle_Ctrl_Grp', 'R_FrKneeStart_Bendy_Ctrl_Auto_Grp', 'L_FrKnee_Top_Handle_Ctrl_Offset_Grp_parentConstraint1', 'bindPose12', 'L_FrHipEnd_Bendy_Ctrl_Root_Grp_parentConstraint1', 'R_FrKnee_Ribbon_Rig_Grp', 'L_FrKneeMid_Bendy_Ctrl|L_FrHip_Jnt_Switch_Loc', 'R_FrAnkle_TwistReader_JntCtrl_Offset_Grp_parentConstraint1', 'L_FrAnkle_Ik_Jnt_Stretchy_Loc', 'L_FrKnee_Jnt_0_Jnt', 'L_FrHip_Bottom_Handle_Ctrl_Offset_Grp_parentConstraint1', 'R_FrHip_Fk_Ctrl_Offset_Grp_parentConstraint1', 'skinCluster12GroupId', 'L_FrHip_Fk_Ctrl_Offset_Grp', 'L_FrAnkle_Ik_PoleVector_Ctrl_Cls', 'R_FrKnee_Fk_Ctrl', 'L_FrHip_Ik_Jnt_L_FrAnkle_Ik_Jnt_Distance_Shape', 'L_FrKnee_Ctrl_1_Ctrl_Auto_Grp_parentConstraint1', 'skinCluster1GroupParts', 'R_FrHip_Twist_1_Jnt', 'L_FrHip_Aim_Loc_2_Aim_Loc_Offset_Grp', 'L_FrHip_Ik_Jnt_Lock_Blend', 'L_FrKnee_Ctrl_1_Ctrl_Root_Grp', 'L_FrAnkle_SubIk_CtrlShape', 'L_FrKnee_Aim_Loc_1_Aim_Loc_Offset_Grp_parentConstraint1', 'R_FrKnee_BendyMid_3_Jnt_Auto_Grp', 'L_FrKnee_Ik_Jnt_Stretchy_Loc', 'R_FrHip_JntBendy_NurbFollicleShape1750', 'L_FrAnkle_Jnt', 'L_FrHip_Ctrl_2_Ctrl', 'R_FrHip_Ctrl_GrpMirror_Grp', 'L_FrKnee_Ctrl_2_Ctrl', 'R_FrAnkle_Ik_PoleVector_Ctrl_ClsHandle', 'L_FrKnee_UpVector_Loc_0_UpVector_Loc', 'L_FrKnee_JntBendy_NurbFollicleShape5050', 'unitConversion12', 'L_FrHip_Jnt_0_Fol', 'L_FrKnee_TwistStart_JntCtrl_parentConstraint1', 'R_FrKnee_Ctrl_1_Ctrl_Auto_Grp_parentConstraint1', 'L_FrAnkle_Ik_IKrp', 'L_FrKnee_Ribbon_Ctrl_Grp', 'unitConversion62', 'L_FrKnee_Ctrl_2_Ctrl_Auto_Grp_aimConstraint1', 'L_FrKnee_Ik_Jnt_ClsGroupId', 'L_FrHip_JntBendy_Other_Local_NurbShape', 'L_FrHip_JntBendy_NurbFollicle5050', 'L_FrKnee_Ctrl_2_Ctrl_ForwardAim_Grp', 'L_FrHip_Bottom_Handle_Ctrl_tag', 'L_FrHip_TwistStart_JntCtrl_CrvShapeOrig', 'R_FrHip_Aim_Loc_2_Aim_Loc_aimConstraint1', 'L_FrHip_JntBendy_NurbFollicleShape1750', 'L_FrKnee_Ctrl_0_Ctrl_Auto_Grp_parentConstraint1', 'L_FrKnee_Jnt_0_Jnt_parentConstraint1', 'L_FrKnee_Bottom_Handle_Ctrl', 'skinCluster10GroupParts', 'R_FrHip_UpVector_Loc_0_UpVector_LocShape', 'R_FrHip_Jnt_2_Jnt_parentConstraint1', 'L_FrKnee_Aim_Loc_1_Aim_Loc_aimConstraint1', 'L_FrKnee_Jnt_2_Jnt', 'L_FrKnee_Bnd_3_Bnd_scaleConstraint1', 'unitConversion20', 'L_FrHip_Ctrl_2_Ctrl_tag', 'L_FrHip_Jnt_3_FolShape', 'unitConversion46', 'skinCluster1Set', 'L_FrHip_Jnt_1_FolShape', 'R_FrAnkle_Fk_Jnt_Ctrl_tag', 'R_FrHip_BendyMid_1_Jnt', 'L_FrAnkle_Ik_CtrlShape', 'skinCluster16', 'L_FrKnee_Ik_Jnt_ClsHandle', 'L_FrKnee_Bottom_Handle_Ctrl_Offset_Grp_parentConstraint1', 'R_FrHip_Ctrl_Grp', 'R_FrHip_Aim_Loc_0_Aim_Loc_Offset_Grp', 'R_FrKnee_JntBendy_NurbShapeOrig', 'L_FrHip_Bnd_0_Bnd', 'L_FrAnkle_Fk_CtrlShape', 'R_FrKnee_Jnt_1_Jnt', 'R_FrAnkle_Ik_IKrp_TotalDistance_MultDiv', 'R_FrKnee_Jnt_1_FolShape', 'L_FrKnee_Ctrl_0_Ctrl_Auto_Grp', 'R_FrKnee_Jnt_BendyIK_Grp', 'skinCluster16GroupId', 'R_FrKnee_JntBendy_IK_Local_NurbShape', 'R_FrHipStart_Bendy_Ctrl', 'R_FrHip_UpVector_Loc_1_UpVector_Loc', 'R_FrHip_Bnd_0_Bnd_parentConstraint1', 'R_FrHip_Ctrl_0_Ctrl_Auto_Grp_parentConstraint1', 'L_FrHip_Ik_Jnt_parentConstraint1', 'R_FrKnee_Aim_Loc_3_Aim_LocShape', 'L_FrHip_Bnd_0_Bnd_scaleConstraint1', 'R_FrHip_Ctrl_0_Ctrl_Auto_Grp_aimConstraint1', 'R_FrKnee_Bnd_0_Bnd_scaleConstraint1', 'L_FrKneeEnd_Bendy_Ctrl_Auto_Grp', 'R_FrHip_Aim_Loc_1_Aim_Loc_Offset_Grp_parentConstraint1', 'R_FrHip_Ik_Jnt_NewScale_MultDiv', 'R_FrKnee_Fk_Ctrl_Offset_Grp', 'R_FrKnee_Fk_Jnt_scale_Blend', 'R_FrAnkle_TwistReader_JntCtrl_quatToEuler', 'L_FrKneeEnd_Bendy_Ctrl', 'L_FrAnkle_TwistReader_JntCtrl_decomposeMatrix', 'R_FrHip_UpVector_Loc_0_UpVector_Loc', 'R_FrKnee_Ik_Jnt_Volume_Blend', 'L_FrKnee_Jnt_3_FolShape', 'skinCluster11GroupId', 'R_FrHip_Aim_Loc_1_Aim_Loc_aimConstraint1', 'unitConversion39', 'R_FrKnee_Aim_Loc_1_Aim_Loc', 'L_FrKneeMid_Bendy_Ctrl', 'bindPose6', 'R_FrHip_Fk_Jnt_Ctrl_tag', 'L_FrHip_JntBendy_NurbFollicleShape8350', 'R_FrHip_Ctrl_0_Ctrl_Auto_Grp', 'R_FrHip_Jnt_0_Jnt', 'L_FrHip_Ik_Jnt_L_FrAnkle_Ik_Jnt_Distance_Shape_Normalize_MultDiv', 'L_FrHip_TwistStart_JntCtrl_parentConstraint1', 'L_FrAnkle_Ik_Ctrl_Root_Grp', 'L_FrKnee_Ik_Jnt_L_FrAnkle_Ik_Jnt_Distance', 'R_FrKnee_Ctrl_2_CtrlShape', 'R_FrKneeMid_Bendy_Ctrl|R_FrHip_Jnt_Switch_Loc', 'R_FrHip_Ctrl_2_Ctrl_Auto_Grp_parentConstraint1', 'R_FrKnee_Twist_1_Jnt', 'L_FrAnkle_Ik_Jnt', 'L_FrHip_Aim_Loc_2_Aim_Loc_aimConstraint1', 'R_FrHip_Ik_Jnt_R_FrAnkle_Ik_Jnt_Distance_Shape_MultDiv', 'R_FrHip_Ik_Jnt', 'R_FrKnee_Jnt_2_Jnt', 'L_FrKnee_Aim_Loc_2_Aim_Loc_aimConstraint1', 'unitConversion42', 'L_FrHip_Jnt_0_Jnt_parentConstraint1', 'L_FrAnkle_Ik_Ctrl', 'R_FrKnee_Twist_0_Jnt', 'skinCluster12Set', 'R_FrAnkle_Ik_Jnt_Stretchy_LocShape', 'R_FrKneeEnd_Bendy_Ctrl', 'R_FrKneeMid_Bendy_Ctrl_tag', 'R_FrHip_Ik_Jnt_Lock_Blend', 'L_FrAnkle_Ik_PoleVector_Ctrl_ClsHandle', 'R_FrHip_JntBendy_NurbFollicleShape5050', 'L_FrKnee_Jnt_Ribbons_Ctrl_Grp', 'L_FrKnee_Ctrl_1_Ctrl_Root_Grp_parentConstraint1', 'R_FrHip_Bnd_3_Bnd_scaleConstraint1', 'L_FrKnee_BendyMid_0_Jnt_Auto_Grp', 'L_FrHip_Aim_Loc_3_Aim_Loc_Offset_Grp', 'R_FrHip_Jnt_1_FolShape', 'L_FrKnee_JntRibbon_NurbShape', 'skinCluster5', 'L_FrKnee_Bottom_Handle_Ctrl_tag', 'L_FrHip_Ctrl_1_Ctrl_tag', 'L_FrAnkle_SubIk_Ctrl_Offset_Grp', 'L_FrHip_Ctrl_1_Ctrl_Root_Grp_parentConstraint1', 'R_FrHip_JntBendy_IK_Local_Nurb', 'L_FrKnee_Jnt_0_FolShape', 'L_FrKneeEnd_Bendy_CtrlShape', 'L_FrKnee_Bnd_1_Bnd_parentConstraint1', 'R_FrKnee_Ctrl_2_Ctrl_Auto_Grp_aimConstraint1', 'R_FrHip_Jnt_3_Jnt', 'R_FrHip_Aim_Loc_3_Aim_LocShape', 'L_FrKnee_Ctrl_3_Ctrl_ForwardAim_Grp', 'R_FrKnee_UpVector_Loc_3_UpVector_LocShape', 'R_FrHip_Rig_Grp', 'R_FrKnee_Ctrl_2_Ctrl_Auto_Grp', 'L_FrAnkle_Ik_Ctrl_tag', 'R_FrKnee_Jnt_Fol_Grp', 'L_FrHip_BendyMid_2_Jnt', 'R_FrHip_Jnt_ForwardAim_Grp_scaleConstraint1', 'L_FrHip_Jnt_1_Fol', 'L_FrKnee_Ctrl_3_Ctrl_tag', 'R_FrAnkle_Ik_Jnt_Stretchy_Loc_parentConstraint1', 'R_FrKnee_Ctrl_1_Ctrl_Auto_Grp_aimConstraint1', 'R_FrKnee_Jnt_ForwardAim_Grp_scaleConstraint1', 'L_FrKneeStart_Bendy_Ctrl', 'R_FrHip_Ik_Jnt_R_FrAnkle_Ik_Jnt_Distance_Shape_Normalize_MultDiv', 'R_FrHip_Ctrl_2_Ctrl_Auto_Grp', 'R_FrKnee_Aim_Loc_1_Aim_Loc_Offset_Grp', 'reverse2', 'R_FrAnkle_TwistEnd_JntCtrl', 'L_FrAnkle_Ik_IKrp_Stretchy_Grp', 'R_FrKnee_BendyMid_0_Jnt_AutoBend_Grp', 'R_FrHip_UpVector_Loc_2_UpVector_Loc', 'L_FrKnee_Fk_Jnt_Ctrl_tag', 'L_FrHip_Ik_Ctrl_Offset_Grp_parentConstraint1', 'unitConversion45', 'unitConversion56', 'R_FrAnkle_Ik_PoleVector_Ctrl_Cls', 'R_FrKnee_JntBendy_NurbShape', 'L_FrHipEnd_Bendy_Ctrl_tag', 'unitConversion34', 'L_FrKnee_UpVector_Loc_2_UpVector_Loc', 'L_FrHip_Jnt_0_Jnt', 'L_FrKnee_TwistStart_Grp_scaleConstraint1', 'L_FrHip_Ik_Jnt_Volume_Blend', 'R_FrHip_TwistStart_Grp_scaleConstraint1', 'R_FrHip_Top_Handle_Ctrl_tag', 'R_FrKneeMid_Bendy_Ctrl_MultDiv3', 'R_FrAnkle_Fk_Jnt_translate_Blend', 'skinCluster12GroupParts', 'L_FrHip_TwistStart_Grp', 'skinCluster6Set', 'skinCluster3Set', 'R_FrKnee_UpVector_Loc_0_UpVector_LocShape', 'R_FrKneeStart_Bendy_Ctrl_Root_Grp', 'unitConversion21', 'skinCluster14GroupId', 'R_FrAnkle_Ik_PoleVector_Ctrl_Offset_Grp', 'L_FrHip_UpVector_Loc_2_UpVector_Loc', 'L_FrHip_Ctrl_3_Ctrl_Auto_Grp_aimConstraint1', 'L_FrHip_Bottom_Handle_Ctrl', 'L_FrAnkle_Ik_PoleVector_Ctrl_ClsHandle_parentConstraint1', 'L_FrKneeStart_Bendy_CtrlShape', 'R_FrKnee_Ik_Jnt_Stretchy_Loc', 'L_FrAnkle_Ik_Jnt_Ctrl_tag', 'R_FrHip_Bnd_0_Bnd', 'R_FrKnee_Fk_Jnt_parentConstraint1', 'R_FrKnee_Ctrl_0_Ctrl_Auto_Grp_aimConstraint1', 'L_FrHip_BendyMid_0_Jnt_Auto_Grp', 'R_FrKneeEnd_Bendy_Ctrl_Root_Grp', 'R_FrKnee_Jnt_3_Jnt', 'unitConversion47', 'R_FrKnee_Bnd_1_Bnd', 'skinCluster8GroupId', 'R_FrHip_Jnt_1_Fol', 'L_FrKnee_Jnt_Bendy_BSGroupId', 'L_FrHip_Fk_Jnt_translate_Blend', 'L_FrKnee_Jnt_BendyIK_Grp', 'R_FrAnkle_Ik_IKrp_DownLock_PV_MultDiv', 'L_FrHip_Ctrl_0_CtrlShape', 'R_FrKnee_Aim_Loc_2_Aim_Loc_aimConstraint1', 'R_FrKneeMid_Bendy_Ctrl_Offset_Grp_parentConstraint1', 'L_FrHip_Ctrl_0_Ctrl_Auto_Grp_parentConstraint1', 'unitConversion8', 'unitConversion35', 'R_FrKnee_Ctrl_0_Ctrl_Auto_Grp', 'L_FrKnee_JntBendy_NurbFollicle5050', 'unitConversion64', 'L_FrAnkle_Ik_Jnt_Effector', 'skinCluster7GroupParts', 'L_FrKnee_Aim_Loc_1_Aim_Loc_Offset_Grp', 'R_FrHip_Aim_Loc_3_Aim_Loc', 'R_FrHip_Bnd_1_Bnd_parentConstraint1', 'R_FrHip_JntBendy_NurbShapeOrig', 'L_FrHip_JntBendy_NurbFollicle8350', 'L_FrKnee_Aim_Loc_1_Aim_LocShape', 'L_FrAnkle_TwistReader_JntCtrl_Offset_Grp_scaleConstraint1', 'curveShape1Orig', 'R_FrHip_JntBendy_Other_Local_NurbShape', 'L_FrHip_UpVector_Loc_2_UpVector_LocShape', 'L_FrHip_Fk_Jnt_scale_Blend', 'skinCluster4Set', 'R_FrKnee_Bnd_2_Bnd_parentConstraint1', 'L_FrKnee_Ctrl_3_Ctrl_Auto_Grp_parentConstraint1', 'R_FrHip_Bnd_2_Bnd', 'L_FrAnkle_Ik_IKrp_UpLock_PV_MultDiv', 'L_FrKnee_Ctrl_2_Ctrl_Root_Grp', 'R_FrHip_Ik_Jnt_Ctrl_Grp', 'R_FrHip_Ik_Jnt_Stretchy_LocShape', 'L_FrKnee_Ctrl_1_Ctrl_Auto_Grp', 'R_FrHip_BendyMid_0_Jnt_Auto_Grp', 'unitConversion54', 'skinCluster4GroupId', 'R_FrKneeStart_Bendy_Ctrl_Auto_Grp_pointConstraint1', 'R_FrAnkle_Fk_Ctrl_Offset_Grp', 'R_FrHip_Ik_Jnt_Stretchy_Loc', 'L_FrKnee_TwistStart_JntCtrl_CrvShape', 'L_FrKnee_Ctrl_0_Ctrl', 'skinCluster5Set', 'L_FrHip_UpVector_Loc_3_UpVector_Loc', 'L_FrKnee_JntBendy_IK_Local_NurbShape', 'R_FrHip_Bnd_1_Bnd_scaleConstraint1', 'L_FrKnee_Ctrl_0_Ctrl_Auto_Grp_aimConstraint1', 'unitConversion52', 'unitConversion11', 'R_FrHip_Jnt_1_Jnt_parentConstraint1', 'L_FrHip_Jnt_3_Jnt_parentConstraint1', 'R_FrHip_Top_Handle_Ctrl', 'R_FrHip_JntRibbon_NurbShape', 'L_FrHip_Jnt_2_Fol', 'L_FrHip_Handle_Ctrl_Grp', 'L_FrAnkle_TwistReader_JntCtrl_quatToEuler', 'R_FrAnkle_Ik_IKrp_DownLock_PV_MultDiv1', 'skinCluster16Set', 'L_FrKnee_Fk_Ctrl_Offset_Grp', 'R_FrAnkle_TwistEnd_JntCtrl_parentConstraint1', 'L_FrAnkle_Fk_Jnt_translate_Blend', 'R_FrKnee_Jnt_Local_Grp', 'L_FrHipStart_Bendy_Ctrl', 'R_FrKnee_JntBendy_NurbFollicle1750', 'L_FrKnee_BendyMid_1_Jnt', 'R_FrAnkle_Ik_IKrp_UpLock_PV_MultDiv', 'R_FrHip_Ctrl_1_Ctrl', 'curveShape2Orig', 'R_FrAnkle_Ik_IKrp', 'L_FrAnkle_Ik_PoleVector_Ctrl_ClsSet', 'R_FrHip_Ik_Ctrl_Offset_Grp', 'R_FrKnee_TwistStart_JntCtrl_parentConstraint1', 'R_FrHip_Aim_Loc_2_Aim_LocShape', 'unitConversion26', 'R_FrHip_BendyMid_3_Jnt_Root_Grp', 'L_FrAnkle_Ik_IKrp_DownLock_PV_MultDiv2', 'R_FrKnee_Aim_Loc_0_Aim_Loc_Offset_Grp', 'R_FrKnee_Top_Handle_Ctrl', 'L_FrHip_Ctrl_0_Ctrl_Root_Grp_parentConstraint1', 'unitConversion6', 'R_FrKnee_JntBendy_NurbFollicle8350', 'L_FrAnkle_Fk_Ctrl_Offset_Grp', 'skinCluster14', 'R_FrKnee_Ik_Jnt_ClsHandleShape', 'L_FrHip_Jnt_Effector', 'L_FrHip_Aim_Loc_0_Aim_LocShape', 'L_FrKnee_Ik_Jnt_NewScale_MultDiv', 'R_FrHip_Top_Handle_Ctrl_Offset_Grp_parentConstraint1', 'L_FrHip_Jnt_2_Jnt_parentConstraint1', 'R_FrHip_Jnt_QTE_MultDiv', 'L_FrKnee_Ik_Jnt_Volume_Blend', 'L_FrHip_JntBendy_Other_Local_Nurb', 'R_FrAnkle_Ik_Jnt', 'R_FrAnkle_Ik_Jnt_Ctrl_tag', 'R_FrHip_Ctrl_2_Ctrl_ForwardAim_Grp', 'unitConversion59', 'R_FrKnee_Ctrl_1_CtrlShape', 'bindPose8', 'L_FrKnee_Jnt_Bendy_BS', 'L_FrKnee_Ctrl_0_Ctrl_ForwardAim_Grp', 'L_FrHipEnd_Bendy_Ctrl_Root_Grp', 'R_FrKnee_Ctrl_2_Ctrl_Auto_Grp_parentConstraint1', 'L_FrAnkle_Ik_PoleVector_Ctrl', 'R_FrKnee_Bnd_3_Bnd_parentConstraint1', 'R_FrKnee_UpVector_Loc_0_UpVector_Loc', 'L_FrKnee_Bottom_Handle_Ctrl_Offset_Grp', 'R_FrKnee_Bottom_Handle_Ctrl', 'R_FrHip_JntBendy_NurbFollicle5050', 'L_FrHip_Ctrl_0_Ctrl_Auto_Grp', 'R_FrAnkle_Ik_Ctrl_Root_Grp', 'R_FrHip_Ctrl_GrpMirror_Grp_parentConstraint1', 'R_FrHip_TwistStart_JntCtrl_CrvShape', 'R_FrKnee_Jnt_0_Jnt_parentConstraint1', 'unitConversion49', 'L_FrHip_Jnt_Local_Grp', 'unitConversion14', 'R_FrHip_TwistStart_JntCtrl_parentConstraint1', 'R_FrKnee_Ik_Jnt', 'R_FrKnee_BendyMid_3_Jnt_AutoBend_Grp', 'L_FrHip_Aim_Loc_3_Aim_LocShape', 'R_FrHip_BendyMid_0_Jnt_AutoBend_Grp', 'R_FrHip_Jnt_3_FolShape', 'R_FrKneeMid_Bendy_Ctrl_MultDiv2', 'L_FrKnee_Aim_Loc_3_Aim_Loc_Offset_Grp_parentConstraint1', 'L_FrHip_Ik_Jnt_Stretchy_Loc', 'R_FrKnee_Jnt_2_Jnt_parentConstraint1', 'R_FrKnee_JntBendy_Other_Local_Nurb', 'R_FrKnee_Jnt_3_FolShape', 'skinCluster16GroupParts', 'R_FrKnee_Ctrl_1_Ctrl_ForwardAim_Grp', 'R_FrHip_Bottom_Handle_Ctrl_tag', 'unitConversion66', 'R_FrKnee_Twist_2_Jnt', 'unitConversion63', 'L_FrHip_Ctrl_0_Ctrl', 'R_FrHip_Bottom_Handle_Ctrl_Offset_Grp', 'L_FrHip_Ctrl_1_Ctrl_Root_Grp', 'L_FrKnee_Top_Handle_Ctrl_Offset_Grp', 'R_FrAnkle_Ik_Jnt_orientConstraint1', 'skinCluster2GroupId', 'L_FrHipStart_Bendy_Ctrl_Root_Grp_parentConstraint1', 'L_FrKnee_Ik_Jnt_ClsSet', 'L_FrKnee_JntBendy_NurbFollicleShape8350', 'L_FrAnkle_TwistEnd_JntCtrl_parentConstraint1', 'R_FrHip_Fk_CtrlShape', 'skinCluster11Set', 'L_FrHipStart_Bendy_Ctrl_Auto_Grp', 'R_FrKnee_Ik_Jnt_ClsGroupParts', 'L_FrKnee_UpVector_Loc_2_UpVector_LocShape', 'L_FrHip_Fk_Jnt_rotate_Blend', 'L_FrKnee_JntBendy_IK_Local_NurbShapeOrig', 'L_FrHip_Ik_Jnt_Stretchy_LocShape', 'L_FrKnee_Fk_Jnt', 'R_FrHip_Fk_Jnt_rotate_Blend', 'L_FrKnee_Aim_Loc_2_Aim_Loc_Offset_Grp_parentConstraint1', 'L_FrKneeStart_Bendy_Ctrl_Auto_Grp', 'unitConversion65', 'R_FrKneeStart_Bendy_Ctrl', 'curveShape1', 'R_FrKnee_Aim_Loc_1_Aim_Loc_Offset_Grp_parentConstraint1', 'L_FrHip_Aim_Loc_0_Aim_Loc_Offset_Grp', 'R_FrKnee_Ctrl_3_Ctrl_Auto_Grp', 'bindPose10', 'L_FrHipStart_Bendy_Ctrl_Root_Grp', 'L_FrKneeMid_Bendy_Ctrl_Offset_Grp_parentConstraint1', 'L_FrHip_JntRibbon_Nurb', 'R_FrKnee_Ctrl_0_Ctrl_ForwardAim_Grp', 'L_FrHip_Bnd_2_Bnd_parentConstraint1', 'L_FrKnee_Jnt_ForwardAim_Grp_scaleConstraint1', 'L_FrKnee_TwistStart_IKspl', 'L_FrKneeMid_Bendy_Ctrl_MultDiv1', 'R_FrKnee_Bottom_Handle_CtrlShape', 'L_FrAnkle_Ik_PoleVector_Ctrl_ClsHandleShape', 'R_FrHipStart_Bendy_Ctrl_Root_Grp', 'R_FrHip_Fk_Jnt_parentConstraint1', 'L_FrHip_Ctrl_0_Ctrl_Root_Grp', 'R_FrHipEnd_Bendy_CtrlShape', 'skinCluster10GroupId', 'R_FrKnee_Ctrl_3_Ctrl_Root_Grp', 'R_FrHip_Jnt_2_Fol', 'R_FrKneeMid_Bendy_CtrlShape', 'L_FrHip_Ik_Ctrl_Offset_Grp', 'L_FrKnee_BendyMid_3_Jnt_Root_Grp', 'L_FrHip_Ctrl_2_Ctrl_Auto_Grp_aimConstraint1', 'L_FrHipEnd_Bendy_Ctrl', 'R_FrHip_Jnt_Bendy_BSGroupId', 'R_FrAnkle_Ik_PoleVector_Ctrl_ClsHandle_parentConstraint1', 'L_FrHipEnd_Bendy_CtrlShape', 'R_FrHip_Ctrl_1_Ctrl_ForwardAim_Grp', 'R_FrHip_Ik_CtrlShape', 'R_FrKnee_BendyMid_0_Jnt', 'R_FrKnee_Ctrl_3_CtrlShape', 'skinCluster13Set', 'L_FrHip_Jnt_Ribbons_Ctrl_Grp', 'L_FrHip_Ik_Jnt', 'unitConversion44', 'R_FrHip_Bottom_Handle_CtrlShape', 'L_FrKnee_Ik_Jnt_Stretchy_LocShape', 'R_FrHip_TwistStart_JntCtrl_Crv', 'R_FrAnkle_Ik_IKrp_Condition', 'R_FrAnkle_Ik_Ctrl_Auto_Grp', 'R_FrHipStart_Bendy_Ctrl_Auto_Grp', 'R_FrHip_JntBendy_Other_Local_Nurb', 'L_FrHip_Aim_Loc_1_Aim_Loc_Offset_Grp', 'R_FrHip_Ik_Ctrl_tag', 'R_FrHip_Ctrl_3_Ctrl_tag', 'L_FrHip_Bnd_1_Bnd_scaleConstraint1', 'R_FrKnee_Bnd_3_Bnd', 'R_FrHip_Ctrl_0_Ctrl', 'L_FrKnee_Fk_Jnt_parentConstraint1', 'skinCluster9', 'L_FrKnee_Jnt_2_Fol', 'L_FrKnee_Fk_Jnt_translate_Blend', 'R_FrKnee_Ctrl_3_Ctrl_ForwardAim_Grp', 'L_FrAnkle_Ik_PoleVector_Ctrl_ClsGroupParts', 'R_FrHip_Bottom_Handle_Ctrl_Offset_Grp_parentConstraint1', 'L_FrHip_Ctrl_0_Ctrl_ForwardAim_Grp', 'R_FrHip_JntBendy_IK_Local_NurbShapeOrig', 'R_FrHipEnd_Bendy_Ctrl_tag', 'unitConversion7', 'R_FrKnee_Jnt_3_Jnt_parentConstraint1', 'R_FrKnee_Top_Handle_Ctrl_tag', 'R_FrHip_Aim_Loc_2_Aim_Loc_Offset_Grp_parentConstraint1', 'R_FrHip_Aim_Loc_1_Aim_Loc_Offset_Grp', 'R_FrHip_Fk_Jnt_scale_Blend', 'L_FrKnee_Ik_Jnt_Lock_Blend', 'R_FrKnee_TwistEnd_JntCtrl_parentConstraint1', 'L_FrKnee_Ik_Jnt_ClsGroupParts', 'R_FrHip_Jnt_1_Jnt', 'L_FrAnkle_Ik_Ctrl_Auto_Grp', 'R_FrAnkle_Jnt', 'R_FrKnee_Fk_CtrlShape', 'L_FrHip_Ctrl_3_Ctrl_ForwardAim_Grp', 'L_FrKnee_Ctrl_1_Ctrl', 'L_FrHip_JntBendy_IK_Local_NurbShapeOrig', 'R_FrKnee_UpVector_Loc_2_UpVector_Loc', 'L_FrHip_Ctrl_3_Ctrl_tag', 'R_FrHip_JntBendy_NurbFollicleShape8350', 'R_FrKneeMid_Bendy_Ctrl_Offset_Grp', 'L_FrHip_Ctrl_2_CtrlShape', 'L_FrHip_Ik_Jnt_L_FrKnee_Ik_Jnt_Distance_Shape', 'R_FrHip_JntRibbon_NurbShapeOrig', 'R_FrHip_Aim_Loc_0_Aim_Loc', 'R_FrHipEnd_Bendy_Ctrl_Root_Grp', 'R_FrHip_Jnt_3_Jnt_parentConstraint1', 'R_FrHip_Ctrl_2_Ctrl_Auto_Grp_aimConstraint1', 'L_FrHip_Aim_Loc_2_Aim_Loc_Offset_Grp_parentConstraint1', 'L_FrKnee_Jnt_3_Jnt_parentConstraint1', 'R_FrKnee_Ctrl_2_Ctrl_ForwardAim_Grp', 'L_FrKneeMid_Bendy_Ctrl_tag', 'R_FrHip_Jnt_0_Jnt_parentConstraint1', 'L_FrHip_TwistStart_JntCtrl_CrvShape', 'R_FrKnee_Aim_Loc_2_Aim_Loc_Offset_Grp_parentConstraint1', 'L_FrHip_Bnd_2_Bnd', 'L_FrHip_Fk_Jnt_Ctrl_tag', 'R_FrKnee_Ik_Jnt_NewScale_MultDiv', 'L_FrHip_Top_Handle_Ctrl_Offset_Grp', 'L_FrHip_Twist_3_Jnt', 'R_FrKnee_Ctrl_1_Ctrl_Root_Grp', 'L_FrHip_Jnt_3_Fol', 'R_FrKnee_UpVector_Loc_1_UpVector_LocShape', 'R_FrHip_Ctrl_3_Ctrl_Root_Grp', 'L_FrHip_Jnt_Main_Grp_parentConstraint1', 'R_FrHip_Jnt_3_Fol', 'L_FrKnee_Bnd_2_Bnd', 'unitConversion10', 'R_FrKnee_Top_Handle_CtrlShape', 'L_FrHip_Jnt_BendyIK_Grp', 'R_FrHip_Aim_Loc_2_Aim_Loc_Offset_Grp', 'R_FrKnee_BendyMid_1_Jnt', 'skinCluster11GroupParts', 'L_FrHip_Aim_Loc_1_Aim_Loc_aimConstraint1', 'L_FrKnee_Aim_Loc_0_Aim_Loc', 'R_FrKnee_Aim_Loc_0_Aim_Loc_aimConstraint1', 'R_FrKnee_Ctrl_0_Ctrl_Auto_Grp_parentConstraint1', 'R_FrHip_Jnt_2_FolShape', 'R_FrKnee_Aim_Loc_3_Aim_Loc', 'skinCluster12', 'L_FrAnkle_Fk_Jnt_scale_Blend', 'L_FrHip_Bnd_3_Bnd_parentConstraint1', 'R_FrHip_TwistStart_IKspl', 'R_FrAnkle_Ik_IKrp_Grp', 'R_FrKnee_TwistStart_IKspl', 'R_FrKnee_NoRotate_JntCtrl_Offset_Grp_parentConstraint1', 'bindPose11', 'L_FrAnkle_Ik_Jnt_PoleVector_Ctrl_tag', 'R_FrAnkle_Fk_CtrlShape', 'L_FrHip_Ik_Jnt_NewScale_MultDiv', 'L_FrKnee_Ik_Jnt_ClsHandle_parentConstraint1', 'L_FrKnee_NoRotate_JntCtrl_Offset_Grp_parentConstraint1', 'R_FrKnee_Ik_Jnt_Cls', 'L_FrHip_Twist_2_Jnt', 'L_FrHip_Aim_Loc_3_Aim_Loc_Offset_Grp_parentConstraint1', 'L_FrKnee_Ctrl_3_Ctrl_Auto_Grp_aimConstraint1', 'hyperLayout72', 'R_FrKnee_BendyMid_3_Jnt', 'L_FrHip_Ctrl_3_Ctrl_Auto_Grp_parentConstraint1', 'L_FrAnkle_Ik_IKrp_DownLock_PV_MultDiv', 'L_FrKnee_JntBendy_IK_Local_Nurb', 'R_FrKneeEnd_Bendy_Ctrl_tag', 'R_FrHip_Flip_Grp', 'R_FrKnee_BendyMid_0_Jnt_Auto_Grp', 'R_FrHip_BendyMid_0_Jnt_Root_Grp', 'L_FrAnkle_TwistReader_JntCtrl_Offset_Grp', 'skinCluster5GroupParts', 'L_FrHip_TwistStart_JntCtrl', 'R_FrHip_Ctrl_2_Ctrl_Root_Grp_parentConstraint1', 'R_FrHip_Jnt_0_FolShape', 'L_FrHip_Top_Handle_CtrlShape', 'L_FrHip_Jnt_Bendy_BSGroupParts', 'R_FrHip_Jnt_Fol_Grp', 'R_FrKnee_Ctrl_2_Ctrl_Root_Grp_parentConstraint1', 'L_FrHip_JntBendy_IK_Local_NurbShape', 'L_FrKnee_Bottom_Handle_CtrlShape', 'R_FrKneeEnd_Bendy_Ctrl_Root_Grp_parentConstraint1', 'L_FrKnee_Jnt_2_FolShape', 'R_FrAnkle_Fk_Jnt', 'unitConversion28', 'R_FrHip_Ribbon_Rig_Grp', 'R_FrKneeStart_Bendy_Ctrl_tag', 'skinCluster2Set', 'unitConversion40', 'L_FrKnee_Jnt_Effector', 'L_FrAnkle_Ik_IKrp_TotalDistance_MultDiv', 'L_FrKnee_BendyMid_0_Jnt', 'L_FrHip_Ctrl_Grp', 'L_FrKnee_BendyMid_3_Jnt_AutoBend_Grp', 'R_FrKnee_Aim_Loc_1_Aim_LocShape', 'L_FrHipEnd_Bendy_Ctrl_Auto_Grp_pointConstraint1', 'skinCluster13', 'L_FrKnee_Fk_Ctrl', 'R_FrHip_Jnt_Main_Grp_parentConstraint1', 'R_FrKnee_UpVector_Loc_3_UpVector_Loc', 'skinCluster8GroupParts', 'L_FrHip_BendyMid_0_Jnt_AutoBend_Grp', 'L_FrKnee_JntBendy_NurbFollicleShape1750', 'L_FrHip_Ik_Jnt_Stretchy_Loc_parentConstraint1', 'L_FrHip_TwistStart_JntCtrl_Crv', 'unitConversion2', 'L_FrKnee_Jnt', 'R_FrHip_Bnd_1_Bnd', 'L_FrHip_JntBendy_NurbFollicle1750', 'L_FrKnee_TwistEnd_JntCtrl', 'R_FrAnkle_Ik_Ctrl_tag', 'R_FrKnee_Ctrl_2_Ctrl_Root_Grp', 'L_FrKnee_UpVector_Loc_3_UpVector_LocShape', 'L_FrHip_Jnt_Main_Grp_scaleConstraint1', 'L_FrKnee_Top_Handle_Ctrl', 'unitConversion19', 'R_FrAnkle_Ik_PoleVector_Ctrl_ClsSet', 'L_FrAnkle_Ik_IKrp_Condition', 'L_FrHip_JntBendy_NurbFollicleShape5050', 'L_FrHip_Aim_Loc_1_Aim_Loc', 'R_FrKnee_Fk_Jnt_rotate_Blend', 'L_FrHip_BendyMid_3_Jnt_AutoBend_Grp', 'R_FrHip_Ik_Jnt_parentConstraint1', 'L_FrKnee_Jnt_ForwardAim_Grp', 'L_FrKneeMid_Bendy_Ctrl_Offset_Grp', 'skinCluster9GroupId', 'skinCluster7Set', 'R_FrAnkle_Ik_Jnt_Stretchy_Loc', 'L_FrKnee_Bnd_2_Bnd_scaleConstraint1', 'R_FrHip_Top_Handle_Ctrl_Offset_Grp', 'skinCluster15', 'L_FrKneeEnd_Bendy_Ctrl_Root_Grp_parentConstraint1', 'skinCluster9Set', 'L_FrHip_Twist_1_Jnt', 'R_FrHip_Jnt_Bendy_BSSet', 'R_FrAnkle_Ik_CtrlShape', 'unitConversion1', 'L_FrHipStart_Bendy_CtrlShape', 'L_FrHip_Jnt_Bendy_BSSet', 'R_FrAnkle_TwistReader_JntCtrl_decomposeMatrix', 'R_FrHip_Ik_Ctrl_Offset_Grp_parentConstraint1', 'R_FrHip_Ctrl_1_Ctrl_Auto_Grp_parentConstraint1', 'L_FrHip_Jnt_Main_Grp', 'R_FrKnee_Ik_Jnt_ClsHandle', 'R_FrAnkle_SubIk_Ctrl_Offset_Grp', 'L_FrKnee_Twist_1_Jnt', 'R_FrKnee_TwistStart_JntCtrl_Crv', 'R_FrKnee_Ctrl_2_Ctrl_tag', 'L_FrHip_Jnt_QTE', 'L_FrKnee_Jnt_Bendy_Fol_Grp', 'R_FrKnee_Jnt_Bendy_BSSet', 'L_FrHip_UpVector_Loc_0_UpVector_LocShape', 'unitConversion31', 'L_FrHip_Jnt_2_Jnt', 'R_FrHip_Ctrl_3_Ctrl_Root_Grp_parentConstraint1', 'L_FrHip_Fk_Jnt', 'R_FrHip_Ik_Ctrl', 'R_FrHip_Ctrl_1_Ctrl_tag', 'L_FrKnee_BendyMid_0_Jnt_AutoBend_Grp', 'L_FrHip_Ctrl_1_Ctrl_ForwardAim_Grp', 'R_FrKnee_Ctrl_3_Ctrl', 'R_FrKnee_Aim_Loc_2_Aim_Loc_Offset_Grp', 'skinCluster3GroupParts', 'R_FrKnee_Aim_Loc_3_Aim_Loc_Offset_Grp_parentConstraint1', 'R_FrAnkle_TwistReader_JntCtrl_multMatrix', 'bindPose4', 'R_FrKneeEnd_Bendy_CtrlShape', 'R_FrKnee_Fk_Jnt', 'R_FrHip_Bnd_3_Bnd_parentConstraint1', 'L_FrHip_BendyMid_3_Jnt_Root_Grp', 'unitConversion23', 'L_FrHip_Ctrl_0_Ctrl_tag', 'R_FrKnee_Twist_3_Jnt', 'L_FrKnee_Ribbon_Rig_Grp', 'R_FrAnkle_SubIk_Ctrl', 'skinCluster1', 'L_FrHip_Ctrl_1_Ctrl_Auto_Grp_aimConstraint1', 'R_FrHip_BendyMid_3_Jnt_Auto_Grp', 'L_FrKnee_JntBendy_NurbShapeOrig', 'R_FrHip_BendyMid_0_Jnt', 'L_FrHip_Jnt_0_FolShape', 'R_FrKnee_BendyMid_3_Jnt_Root_Grp', 'L_FrKnee_Ctrl_3_Ctrl', 'R_FrKneeMid_Bendy_Ctrl_MultDiv', 'R_FrHip_Ctrl_0_CtrlShape', 'R_FrHip_Ctrl_3_Ctrl_Auto_Grp_aimConstraint1', 'L_FrAnkle_Ik_CtrlMain_Reverse', 'R_FrKnee_JntRibbon_NurbShape', 'R_FrAnkle_TwistReader_JntCtrl_Offset_GrpR_FrAnkle_Jnt_Twist_Reader_Grp_Grp', 'L_FrHip_Ctrl_2_Ctrl_ForwardAim_Grp', 'L_FrKneeStart_Bendy_Ctrl_Auto_Grp_pointConstraint1', 'L_FrKnee_UpVector_Loc_3_UpVector_Loc', 'R_FrHip_Fk_Jnt', 'L_FrHip_Jnt_1_Jnt', 'skinCluster10', 'L_FrKnee_Aim_Loc_1_Aim_Loc', 'R_FrHip_Aim_Loc_0_Aim_Loc_aimConstraint1', 'L_FrKnee_Bnd_3_Bnd', 'R_FrHip_Ik_Jnt_R_FrAnkle_Ik_Jnt_Distance', 'R_FrKnee_TwistEnd_JntCtrl', 'L_FrAnkle_TwistReader_JntCtrl_multMatrix', 'L_FrKnee_Ctrl_1_Ctrl_ForwardAim_Grp', 'R_FrKnee_Ctrl_3_Ctrl_Root_Grp_parentConstraint1', 'L_FrKnee_Twist_3_Jnt', 'unitConversion57', 'R_FrKnee_UpVector_Loc_2_UpVector_LocShape', 'L_FrKnee_Ctrl_2_Ctrl_tag', 'L_FrHip_Bnd_3_Bnd_scaleConstraint1', 'L_FrAnkle_TwistReader_JntCtrl_Offset_Grp_parentConstraint1', 'L_FrKnee_Ctrl_1_CtrlShape', 'L_FrKnee_UpVector_Loc_1_UpVector_LocShape', 'L_FrKnee_Aim_Loc_3_Aim_LocShape', 'R_FrHip_Ctrl_3_Ctrl_ForwardAim_Grp', 'unitConversion32', 'R_FrHip_UpVector_Loc_1_UpVector_LocShape', 'skinCluster11', 'L_FrHip_Jnt_Bendy_BSGroupId', 'skinCluster6', 'R_FrKnee_JntBendy_NurbFollicle5050', 'R_FrKnee_Aim_Loc_0_Aim_LocShape', 'L_FrHip_UpVector_Loc_1_UpVector_Loc', 'L_FrKnee_Fk_Jnt_scale_Blend', 'R_FrHip_Jnt_Bendy_BSGroupParts', 'L_FrHip_Bnd_3_Bnd', 'L_FrAnkle_Ik_Jnt_Stretchy_LocShape', 'R_FrHip_Aim_Loc_1_Aim_LocShape', 'R_FrHip_Jnt_Main_Grp_scaleConstraint1', 'R_FrKnee_NoRotate_JntCtrl', 'R_FrHip_Jnt', 'unitConversion60', 'L_FrKnee_Jnt_Bendy_BSGroupParts', 'R_FrHipStart_Bendy_CtrlShape', 'R_FrKnee_Ik_Jnt_Stretchy_LocShape', 'skinCluster6GroupId', 'L_FrHip_Jnt_1_Jnt_parentConstraint1', 'R_FrAnkle_Ik_PoleVector_Ctrl_ClsGroupId', 'unitConversion50', 'R_FrHip_JntBendy_NurbFollicle8350', 'L_FrKnee_Bnd_2_Bnd_parentConstraint1', 'R_FrAnkle_Fk_Ctrl', 'L_FrHip_Ctrl_2_Ctrl_Root_Grp_parentConstraint1', 'L_FrHip_Ctrl_1_CtrlShape', 'R_FrHip_JntBendy_Nurb', 'R_FrKnee_Top_Handle_Ctrl_Offset_Grp', 'R_FrHip_Jnt_ForwardAim_Grp', 'R_FrHipStart_Bendy_Ctrl_tag', 'R_FrKnee_Bnd_2_Bnd_scaleConstraint1', 'L_FrKnee_Jnt_3_Jnt', 'R_FrKnee_Ctrl_1_Ctrl_Root_Grp_parentConstraint1', 'L_FrKnee_Ik_Jnt_Cls', 'R_FrHip_Ik_Jnt_Stretchy_Loc_parentConstraint1', 'L_FrKneeEnd_Bendy_Ctrl_tag', 'R_FrKnee_Jnt_0_FolShape', 'L_FrHip_Jnt_2_FolShape', 'R_FrAnkle_Ik_IKrp_parentConstraint1', 'L_FrKnee_Jnt_3_Fol', 'bindPose9', 'R_FrHip_TwistStart_JntCtrl_CrvShapeOrig', 'L_FrKnee_TwistStart_JntCtrl_CrvShapeOrig', 'R_FrKnee_BendyMid_0_Jnt_Root_Grp', 'L_FrKnee_Jnt_1_Fol', 'skinCluster7GroupId', 'L_FrHip_JntRibbon_NurbShape', 'L_FrKnee_BendyMid_0_Jnt_Root_Grp', 'R_FrHip_Jnt_Bendy_Fol_Grp', 'unitConversion55', 'L_FrKnee_Jnt_1_Jnt', 'R_FrKneeEnd_Bendy_Ctrl_Auto_Grp', 'R_FrHip_Ctrl_1_Ctrl_Auto_Grp', 'R_FrKnee_JntBendy_NurbFollicleShape8350', 'unitConversion48', 'L_FrKnee_Ctrl_0_Ctrl_tag', 'L_FrKnee_Top_Handle_Ctrl_tag', 'R_FrKneeStart_Bendy_CtrlShape', 'R_FrKnee_TwistStart_Grp', 'R_FrHip_Aim_Loc_3_Aim_Loc_Offset_Grp_parentConstraint1', 'skinCluster4GroupParts', 'R_FrHip_Ctrl_1_CtrlShape', 'bindPose7', 'L_FrHip_Aim_Loc_0_Aim_Loc_aimConstraint1', 'unitConversion9', 'L_FrHip_Ik_CtrlShape', 'unitConversion58', 'R_FrHip_JntBendy_NurbFollicle1750', 'L_FrKneeMid_Bendy_Ctrl_MultDiv2', 'R_FrHip_Aim_Loc_2_Aim_Loc', 'R_FrKnee_Jnt_3_Fol', 'R_FrHip_Jnt_BendyIK_Grp', 'bindPose5', 'R_FrKnee_TwistStart_JntCtrl', 'R_FrHip_Aim_Loc_0_Aim_LocShape', 'L_FrAnkle_Ik_IKrp_DownLock_PV_MultDiv1', 'L_FrKnee_Ik_Jnt_L_FrAnkle_Ik_Jnt_Distance_Shape', 'L_FrKnee_Ctrl_3_CtrlShape', 'L_FrKnee_JntBendy_Other_Local_Nurb', 'R_FrKnee_Ik_Jnt_R_FrAnkle_Ik_Jnt_Distance_Shape', 'L_FrHip_Jnt_Bendy_Fol_Grp', 'skinCluster15Set', 'L_FrKnee_Jnt_Fol_Grp', 'L_FrKnee_JntBendy_Other_Local_NurbShape', 'R_FrKnee_Ctrl_0_Ctrl_tag', 'L_FrHip_Fk_Ctrl_Auto_Grp', 'L_FrKnee_Aim_Loc_2_Aim_LocShape', 'R_FrHipEnd_Bendy_Ctrl_Auto_Grp', 'R_FrKnee_Bnd_3_Bnd_scaleConstraint1', 'L_FrKnee_BendyMid_3_Jnt_Auto_Grp', 'R_FrHip_Ctrl_3_CtrlShape', 'R_FrKnee_Ik_Jnt_Stretchy_Loc_parentConstraint1', 'R_FrKnee_Top_Handle_Ctrl_Offset_Grp_parentConstraint1', 'R_FrAnkle_Ik_IKrp_NormalScale_Loc', 'R_FrHip_JntBendy_NurbShape', 'L_FrHip_Fk_Jnt_parentConstraint1', 'L_FrHip_Ctrl_1_Ctrl_Auto_Grp', 'R_FrKnee_Ctrl_0_Ctrl_Root_Grp_parentConstraint1', 'L_FrKnee_Ctrl_2_Ctrl_Root_Grp_parentConstraint1', 'R_FrHip_Ik_Jnt_R_FrAnkle_Ik_Jnt_Distance_Shape', 'R_FrKnee_Aim_Loc_2_Aim_Loc', 'L_FrKnee_Ctrl_3_Ctrl_Auto_Grp', 'skinCluster6GroupParts', 'L_FrKnee_Ctrl_3_Ctrl_Root_Grp', 'skinCluster8', 'unitConversion25', 'L_FrKnee_TwistStart_Grp', 'R_FrKnee_Fk_Jnt_Ctrl_tag', 'skinCluster13GroupParts', 'L_FrAnkle_Fk_Ctrl', 'L_FrKnee_Ctrl_1_Ctrl_tag', 'R_FrHip_Fk_Ctrl_Root_Grp', 'R_FrHip_UpVector_Loc_3_UpVector_LocShape', 'R_FrHip_Bnd_3_Bnd', 'R_FrKnee_Ik_Jnt_R_FrAnkle_Ik_Jnt_Distance', 'R_FrKnee_Ctrl_0_Ctrl', 'L_FrKnee_Twist_2_Jnt', 'L_FrHip_Ctrl_0_Ctrl_Auto_Grp_aimConstraint1', 'L_FrAnkle_Ik_PoleVector_CtrlShape', 'L_FrHip_Aim_Loc_0_Aim_Loc_Offset_Grp_parentConstraint1', 'R_FrKnee_Bnd_0_Bnd', 'L_FrAnkle_Ik_IKrp_NormalScale_Loc', 'L_FrKnee_Aim_Loc_0_Aim_Loc_Offset_Grp_parentConstraint1', 'L_FrKnee_JntRibbon_NurbShapeOrig', 'unitConversion15', 'R_FrHip_Twist_3_Jnt', 'R_FrHip_Fk_Ctrl', 'L_FrHip_Ik_Jnt_L_FrAnkle_Ik_Jnt_Distance_Shape_MultDiv', 'L_FrHip_Aim_Loc_1_Aim_LocShape', 'R_FrKneeStart_Bendy_Ctrl_Root_Grp_parentConstraint1', 'skinCluster14GroupParts', 'L_FrKnee_Ik_Jnt_Stretchy_Loc_parentConstraint1', 'R_FrKnee_BendyMid_2_Jnt', 'R_FrKneeMid_Bendy_Ctrl', 'R_FrAnkle_Ik_IKrp_Stretchy_Grp', 'L_FrAnkle_SubIk_Ctrl', 'R_FrAnkle_Ik_Jnt_PoleVector_Ctrl_tag', 'R_FrAnkle_Fk_Jnt_parentConstraint1', 'R_FrKnee_TwistStart_JntCtrl_CrvShapeOrig', 'R_FrHip_Fk_Ctrl_Offset_Grp', 'L_FrKneeStart_Bendy_Ctrl_Root_Grp_parentConstraint1', 'R_FrKnee_Jnt_Bendy_Fol_Grp', 'R_FrHip_Top_Handle_CtrlShape', 'R_FrAnkle_Ik_Jnt_Effector', 'L_FrHip_Jnt_UTQ', 'L_FrKnee_BendyMid_2_Jnt', 'L_FrAnkle_Ik_Jnt_orientConstraint1', 'R_FrHip_Jnt_UTQ', 'L_FrKnee_Top_Handle_CtrlShape', 'R_FrHip_Ik_Jnt_R_FrKnee_Ik_Jnt_Distance', 'unitConversion36', 'L_FrHip_TwistStart_Grp_scaleConstraint1', 'R_FrHip_Jnt_Main_Grp', 'L_FrHip_UpVector_Loc_0_UpVector_Loc', 'R_FrKnee_Jnt_0_Jnt', 'R_FrKnee_Ribbon_Ctrl_Grp', 'L_FrKnee_Ctrl_2_Ctrl_Auto_Grp_parentConstraint1', 'unitConversion53', 'L_FrHip_Jnt', 'R_FrHipEnd_Bendy_Ctrl_Root_Grp_parentConstraint1', 'skinCluster3GroupId', 'R_FrAnkle_TwistReader_JntCtrl', 'L_FrHip_Fk_CtrlShape', 'L_FrKnee_Fk_CtrlShape', 'R_FrKnee_Jnt', 'L_FrKnee_Jnt_Local_Grp', 'R_FrKnee_Ctrl_3_Ctrl_Auto_Grp_aimConstraint1', 'L_FrKnee_Twist_0_Jnt', 'L_FrHip_Jnt_Fol_Grp', 'R_FrKnee_Ik_Jnt_ClsSet', 'R_FrHip_BendyMid_2_Jnt', 'skinCluster1GroupId', 'L_FrHip_Ctrl_2_Ctrl_Root_Grp', 'L_FrHip_Ctrl_3_Ctrl_Root_Grp', 'unitConversion22', 'L_FrHip_Top_Handle_Ctrl_tag', 'unitConversion16', 'L_FrAnkle_Ik_IKrp_parentConstraint1', 'L_FrKneeEnd_Bendy_Ctrl_Root_Grp', 'L_FrKnee_Ctrl_0_CtrlShape', 'L_FrKnee_Jnt_0_Fol', 'R_FrKnee_Ctrl_0_CtrlShape', 'L_FrKnee_Bnd_3_Bnd_parentConstraint1', 'L_FrKnee_Ctrl_3_Ctrl_Root_Grp_parentConstraint1', 'L_FrKnee_Aim_Loc_2_Aim_Loc_Offset_Grp', 'L_FrKnee_Ctrl_0_Ctrl_Root_Grp', 'L_FrKnee_Aim_Loc_0_Aim_LocShape', 'R_FrHip_Ctrl_2_Ctrl', 'L_FrAnkle_Fk_Jnt', 'R_FrKnee_Jnt_Ribbons_Ctrl_Grp', 'R_FrKnee_JntRibbon_Nurb', 'R_FrKnee_TwistStart_Grp_scaleConstraint1', 'R_FrKnee_Ctrl_0_Ctrl_Root_Grp', 'L_FrHip_Ctrl_2_Ctrl_Auto_Grp_parentConstraint1', 'R_FrKnee_Jnt_2_Fol', 'L_FrKnee_UpVector_Loc_0_UpVector_LocShape', 'L_FrKneeMid_Bendy_CtrlShape', 'R_FrHip_Jnt_QTE', 'L_FrAnkle_TwistReader_JntCtrl', 'L_FrHip_UpVector_Loc_3_UpVector_LocShape', 'skinCluster10Set', 'L_FrHip_Top_Handle_Ctrl', 'L_FrHip_Ctrl_Grp_scaleConstraint1', 'L_FrHip_Bnd_0_Bnd_parentConstraint1', 'R_FrHip_Ctrl_2_Ctrl_Root_Grp', 'R_FrKnee_Jnt_0_Fol', 'L_FrAnkle_Ik_Jnt_Stretchy_Loc_parentConstraint1', 'R_FrHip_Jnt_Bendy_BS', 'R_FrKnee_Ctrl_2_Ctrl', 'L_FrHip_Aim_Loc_1_Aim_Loc_Offset_Grp_parentConstraint1', 'bindPose1', 'R_FrHip_JntRibbon_Nurb', 'R_FrHipEnd_Bendy_Ctrl_Auto_Grp_pointConstraint1', 'R_FrKnee_Aim_Loc_2_Aim_LocShape', 'L_FrKnee_JntRibbon_Nurb', 'R_FrHip_Aim_Loc_0_Aim_Loc_Offset_Grp_parentConstraint1', 'unitConversion27', 'L_FrKnee_Bnd_0_Bnd_parentConstraint1', 'L_FrKnee_TwistStart_JntCtrl', 'R_FrHip_Ctrl_3_Ctrl', 'L_FrAnkle_Ik_IKrp_poleVectorConstraint1', 'L_FrAnkle_TwistReader_JntCtrl_Offset_GrpL_FrAnkle_Jnt_Twist_Reader_Grp_Grp', 'L_FrHip_Ik_Jnt_Ctrl_Grp', 'L_FrHipStart_Bendy_Ctrl_tag', 'R_FrHipStart_Bendy_Ctrl_Root_Grp_parentConstraint1', 'unitConversion41', 'R_FrHip_Twist_0_Jnt', 'R_FrKnee_Fk_Jnt_translate_Blend', 'L_FrHip_Bottom_Handle_CtrlShape', 'R_FrKnee_Bnd_1_Bnd_parentConstraint1', 'R_FrKnee_Aim_Loc_1_Aim_Loc_aimConstraint1', 'unitConversion29', 'L_FrHip_Ctrl_3_Ctrl', 'R_FrHip_Jnt_Ribbons_Ctrl_Grp', 'L_FrHip_BendyMid_0_Jnt_Root_Grp', 'R_FrKnee_Ik_Jnt_ClsHandle_parentConstraint1', 'L_FrKnee_Jnt_2_Jnt_parentConstraint1', 'L_FrHip_Ctrl_1_Ctrl', 'unitConversion51', 'R_FrKnee_Jnt_2_FolShape', 'R_FrKnee_JntRibbon_NurbShapeOrig', 'L_FrAnkle_TwistEnd_JntCtrl', 'R_FrKnee_Bnd_1_Bnd_scaleConstraint1', 'L_FrHip_Ik_Jnt_L_FrAnkle_Ik_Jnt_Distance', 'L_FrKneeStart_Bendy_Ctrl_Root_Grp', 'R_FrHip_TwistStart_JntCtrl', 'R_FrHip_Fk_Ctrl_Auto_Grp', 'L_FrHip_Bnd_1_Bnd', 'R_FrKnee_Bottom_Handle_Ctrl_Offset_Grp_parentConstraint1', 'skinCluster3', 'R_FrHip_Aim_Loc_1_Aim_Loc', 'R_FrHip_Ik_Jnt_R_FrKnee_Ik_Jnt_Distance_Shape', 'L_FrAnkle_Ik_PoleVector_Ctrl_ClsGroupId', 'L_FrKnee_JntBendy_Nurb', 'L_FrHip_Jnt_QTE_MultDiv', 'L_FrHip_JntRibbon_NurbShapeOrig', 'L_FrKnee_Ctrl_1_Ctrl_Auto_Grp_aimConstraint1', 'L_FrHip_Aim_Loc_3_Aim_Loc', 'R_FrAnkle_Ik_PoleVector_Ctrl_ClsGroupParts', 'L_FrKnee_Ik_Jnt', 'L_FrHip_UpVector_Loc_1_UpVector_LocShape', 'L_FrKnee_Jnt_1_Jnt_parentConstraint1', 'unitConversion33', 'R_FrKneeMid_Bendy_Ctrl_MultDiv1', 'R_FrKnee_Aim_Loc_0_Aim_Loc', 'L_FrKneeStart_Bendy_Ctrl_tag', 'unitConversion17', 'R_FrAnkle_Ik_IKrp_NormalScale_LocShape', 'R_FrHip_Ctrl_0_Ctrl_Root_Grp_parentConstraint1', 'R_FrHip_Ctrl_3_Ctrl_Auto_Grp_parentConstraint1', 'R_FrHip_UpVector_Loc_3_UpVector_Loc', 'unitConversion13', 'R_FrHip_Jnt_0_Fol', 'R_FrHip_Bnd_2_Bnd_scaleConstraint1', 'R_FrHip_Bnd_2_Bnd_parentConstraint1', 'R_FrHip_Ribbon_Ctrl_Grp', 'R_FrHip_Ctrl_2_Ctrl_tag', 'R_FrKnee_Jnt_Bendy_BSGroupParts', 'L_FrHip_Jnt_ForwardAim_Grp', 'R_FrKnee_JntBendy_IK_Local_Nurb', 'bindPose3', 'L_FrKnee_Bnd_1_Bnd_scaleConstraint1', 'L_FrKnee_Jnt_Bendy_BSSet', 'L_FrHip_Ctrl_Grp_parentConstraint1', 'R_FrKnee_JntBendy_IK_Local_NurbShapeOrig', 'unitConversion24', 'R_FrKnee_Ctrl_3_Ctrl_Auto_Grp_parentConstraint1', 'R_FrHipEnd_Bendy_Ctrl', 'R_FrAnkle_Ik_PoleVector_Ctrl_ClsHandleShape', 'L_FrHip_Ik_Ctrl_tag', 'L_FrKnee_Aim_Loc_3_Aim_Loc_Offset_Grp', 'R_FrHip_Ctrl_0_Ctrl_ForwardAim_Grp', 'R_FrKnee_Ctrl_1_Ctrl', 'L_FrHip_Bnd_2_Bnd_scaleConstraint1', 'unitConversion38', 'L_FrHip_Jnt_ForwardAim_Grp_scaleConstraint1', 'L_FrKnee_Ik_Jnt_ClsHandleShape', 'R_FrKnee_TwistStart_JntCtrl_CrvShape', 'L_FrKnee_Aim_Loc_0_Aim_Loc_Offset_Grp', 'skinCluster7', 'L_FrKnee_Ctrl_2_Ctrl_Auto_Grp', 'R_FrKnee_Ik_Jnt_ClsGroupId', 'R_FrHip_Aim_Loc_3_Aim_Loc_Offset_Grp', 'R_FrKnee_Bottom_Handle_Ctrl_tag', 'L_FrAnkle_Ik_PoleVector_Ctrl_Offset_Grp', 'R_FrHip_Ctrl_0_Ctrl_Root_Grp', 'R_FrKnee_Ctrl_3_Ctrl_tag', 'L_FrKnee_Jnt_1_FolShape', 'L_FrHip_Ik_Ctrl', 'R_FrKnee_Jnt_ForwardAim_Grp', 'R_FrHip_Ctrl_3_Ctrl_Auto_Grp', 'L_FrKnee_Aim_Loc_2_Aim_Loc', 'L_FrHip_Rig_Grp', 'L_FrHip_Top_Handle_Ctrl_Offset_Grp_parentConstraint1', 'R_FrHip_UpVector_Loc_2_UpVector_LocShape', 'R_FrHip_BendyMid_3_Jnt_AutoBend_Grp', 'L_FrKneeMid_Bendy_Ctrl_MultDiv3', 'L_FrHip_Ctrl_2_Ctrl_Auto_Grp', 'skinCluster15GroupId', 'L_FrHip_JntBendy_Nurb', 'L_FrHip_Ribbon_Rig_Grp', 'L_FrHip_TwistStart_IKspl', 'L_FrKnee_Bnd_0_Bnd_scaleConstraint1', 'unitConversion18', 'R_FrAnkle_Ik_IKrp_DownLock_PV_MultDiv2', 'L_FrAnkle_Ik_PoleVector_Ctrl_L_FrKnee_Ik_Jnt_Connected_Crv', 'R_FrAnkle_Ik_PoleVector_CtrlShape', 'curveShape2', 'bindPose2', 'R_FrHip_Ctrl_1_Ctrl_Root_Grp_parentConstraint1', 'unitConversion5', 'R_FrKnee_Bnd_2_Bnd', 'R_FrAnkle_TwistReader_JntCtrl_Offset_Grp', 'L_FrKnee_JntBendy_NurbFollicle8350', 'L_FrHip_BendyMid_3_Jnt', 'unitConversion3', 'skinCluster2', 'L_FrHip_Bottom_Handle_Ctrl_Offset_Grp', 'R_FrAnkle_SubIk_CtrlShape', 'L_FrKnee_BendyMid_3_Jnt', 'R_FrAnkle_Ik_CtrlMain_Reverse', 'L_FrKnee_Aim_Loc_3_Aim_Loc', 'skinCluster9GroupParts', 'L_FrHip_Jnt_3_Jnt', 'L_FrHip_Fk_Ctrl', 'R_FrHip_Jnt_Local_Grp', 'R_FrKnee_Jnt_1_Fol', 'R_FrAnkle_TwistReader_JntCtrl_Offset_Grp_scaleConstraint1', 'L_FrHip_Fk_Ctrl_Root_Grp', 'R_FrHip_Ctrl_1_Ctrl_Root_Grp', 'unitConversion43', 'R_FrHip_BendyMid_3_Jnt', 'L_FrKnee_JntBendy_NurbFollicle1750', 'L_FrKnee_TwistStart_JntCtrl_Crv', 'L_FrHip_BendyMid_1_Jnt', 'L_FrKnee_JntBendy_NurbShape', 'L_FrHip_Ribbon_Ctrl_Grp', 'R_FrHip_JntBendy_IK_Local_NurbShape', 'L_FrHip_Aim_Loc_2_Aim_LocShape', 'R_FrHip_Ctrl_GrpMirror_Grp_scaleConstraint1', 'L_FrKnee_Bnd_0_Bnd', 'L_FrHip_Bnd_1_Bnd_parentConstraint1', 'skinCluster5GroupId', 'R_FrKnee_Aim_Loc_3_Aim_Loc_Offset_Grp', 'L_FrKnee_UpVector_Loc_1_UpVector_Loc', 'unitConversion37', 'L_FrKnee_NoRotate_JntCtrl', 'R_FrKnee_UpVector_Loc_1_UpVector_Loc', 'L_FrKnee_NoRotate_JntCtrl_Offset_Grp', 'L_FrHip_Twist_0_Jnt', 'unitConversion4', 'R_FrHip_Jnt_Effector', 'R_FrHip_TwistStart_Grp', 'R_FrKnee_Ik_Jnt_Lock_Blend', 'reverse1', 'R_FrKnee_JntBendy_Other_Local_NurbShape', 'L_FrKnee_TwistEnd_JntCtrl_parentConstraint1', 'R_FrAnkle_Ik_Ctrl', 'R_FrKnee_Jnt_Effector', 'L_FrKnee_Ctrl_0_Ctrl_Root_Grp_parentConstraint1', 'skinCluster4']");
createNode joint -n "L_FrHip_Guide" -p "L_FrHip_Block";
	rename -uid "5757B001-E648-538E-AEAE-7F836D96EF6C";
	addAttr -ci true -sn "Helper" -ln "Helper" -min 0 -max 1 -en "Hide:Show" -at "enum";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/C:\\Users\\Esteban\\Documents\\maya\\2022\\scripts\\rigging\\Mutant_Tools\\Icons\\Guide_Data";
	setAttr ".t" -type "double3" 17.577670815727252 21.42964418528819 25.94263024786277 ;
	setAttr ".r" -type "double3" -138.21116845152761 -56.954456631234194 -32.894066639288091 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr -cb on ".Helper" 1;
createNode nurbsCurve -n "L_FrHip_Guide_CtrlShape" -p "L_FrHip_Guide";
	rename -uid "C6863468-C547-60DD-F9A9-029F9C6FAA4A";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/C:\\Users\\Esteban\\Documents\\maya\\2022\\scripts\\rigging\\Mutant_Tools\\Icons\\Guide_Data";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 14;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 9 0 no 3
		10 0 1 2 3 4 5 6 7 8 9
		10
		5.8966734376283696e-06 -0.2109375 0.10546875
		5.8966734376283696e-06 0.39872714062500003 0.10796456249999997
		5.8966734376283696e-06 0.31204110937499996 0.21365564062499998
		5.8966734376283696e-06 0.41773218749999996 0.39620432812499995
		5.8212421876283689e-06 0.97001803124999997 1.6344703125e-07
		5.8966734376283696e-06 0.41773260937500006 -0.39620432812499995
		5.8966734376283696e-06 0.31204110937499996 -0.21365521875000001
		3.0237721876283699e-06 0.39872714062500003 -0.10682760937500001
		5.8966734376283696e-06 -0.2109375 -0.10546875
		5.8966734376283696e-06 -0.2109375 0.10546875
		;
createNode nurbsCurve -n "L_FrHip_Guide_Ctrl_CtrlShape" -p "L_FrHip_Guide";
	rename -uid "BDBFD98B-4E49-F09C-AACC-CBA970A0A690";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/C:\\Users\\Esteban\\Documents\\maya\\2022\\scripts\\rigging\\Mutant_Tools\\Icons\\Guide_Data";
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
		1.2836953722228372e-16 0.25068192187499999 0
		-1.2973119028804628e-09 0.24687365624999996 0.043530328124999997
		-2.5551997153804631e-09 0.23556403125 0.085738499999999995
		-3.7354540903804627e-09 0.21709729687499998 0.12534117187500002
		-4.8022029966304623e-09 0.19203370312500001 0.16113557812500001
		-5.7230295591304631e-09 0.16113515624999999 0.19203370312500001
		-6.4700014341304637e-09 0.12534117187500002 0.21709729687499998
		-7.0203795591304622e-09 0.085738499999999995 0.23556403125
		-7.3574154966304626e-09 0.043530328124999983 0.24687365624999996
		-7.4708998716304619e-09 -1.6046192152785466e-17 0.25068234375000004
		-7.3574154966304626e-09 -0.04353032812500001 0.24687365624999996
		-7.0203795591304622e-09 -0.085738499999999995 0.23556403125
		-6.4700014341304637e-09 -0.12534117187500002 0.21709729687499998
		-5.7230295591304631e-09 -0.16113515624999999 0.19203370312500001
		-4.8022029966304623e-09 -0.19203370312500001 0.16113557812500001
		-3.7354540903804627e-09 -0.21709729687499998 0.12534117187500002
		-2.5551997153804631e-09 -0.23556403125 0.085738499999999995
		-1.2973119028804628e-09 -0.24687365624999996 0.043530328124999997
		1.2836953722228372e-16 -0.25068192187499999 0
		1.2836953722228372e-16 -0.24687365624999996 -0.043530328124999997
		1.2836953722228372e-16 -0.23556403125 -0.085738499999999995
		1.2836953722228372e-16 -0.21709729687499998 -0.12534117187500002
		1.2836953722228372e-16 -0.19203370312500001 -0.16113557812500001
		1.2836953722228372e-16 -0.16113515624999999 -0.19203370312500001
		1.2836953722228372e-16 -0.12534117187500002 -0.21709729687499998
		1.2836953722228372e-16 -0.085738499999999995 -0.23556445312500002
		1.2836953722228372e-16 -0.04353032812500001 -0.24687365624999996
		1.2836953722228372e-16 -1.6046192152785466e-17 -0.25068234375000004
		1.2836953722228372e-16 0.043530328124999983 -0.24687365624999996
		1.2836953722228372e-16 0.085738499999999995 -0.23556445312500002
		1.2836953722228372e-16 0.12534117187500002 -0.21709729687499998
		1.2836953722228372e-16 0.16113515624999999 -0.19203370312500001
		1.2836953722228372e-16 0.19203370312500001 -0.16113557812500001
		1.2836953722228372e-16 0.21709729687499998 -0.12534117187500002
		1.2836953722228372e-16 0.23556403125 -0.085738499999999995
		1.2836953722228372e-16 0.24687365624999996 -0.043530328124999997
		1.2836953722228372e-16 0.25068192187499999 0
		0.043530328125000121 0.24687365624999996 0
		0.085738500000000134 0.23556403125 0
		0.12534117187500013 0.21709729687499998 0
		0.16113557812500012 0.19203370312500001 0
		0.19203370312500012 0.16113515624999999 0
		0.21709729687500012 0.12534117187500002 0
		0.23556403125000014 0.085738499999999995 0
		0.24687365625000013 0.043530328124999983 0
		0.25068192187500016 -1.6046192152785466e-17 0
		0.24687365625000013 -0.04353032812500001 0
		0.23556403125000014 -0.085738499999999995 0
		0.21709729687500012 -0.12534117187500002 0
		0.19203370312500012 -0.16113515624999999 0
		0.16113557812500012 -0.19203370312500001 0
		0.12534117187500013 -0.21709729687499998 0
		0.085738500000000134 -0.23556403125 0
		0.043530328125000121 -0.24687365624999996 0
		1.2836953722228372e-16 -0.25068192187499999 0
		-0.043530328124999865 -0.24687365624999996 0
		-0.08573849999999987 -0.23556403125 0
		-0.12534117187499988 -0.21709729687499998 0
		-0.16113557812499987 -0.19203370312500001 0
		-0.19203370312499987 -0.16113515624999999 0
		-0.2170972968749999 -0.12534117187500002 0
		-0.23556403124999986 -0.085738499999999995 0
		-0.24687365624999985 -0.04353032812500001 0
		-0.25068234374999987 -1.6046192152785466e-17 0
		-0.24687365624999985 0.043530328124999983 0
		-0.23556403124999986 0.085738499999999995 0
		-0.2170972968749999 0.12534117187500002 0
		-0.19203370312499987 0.16113515624999999 0
		-0.16113557812499987 0.19203370312500001 0
		-0.12534117187499988 0.21709729687499998 0
		-0.08573849999999987 0.23556403125 0
		-0.043530328124999865 0.24687365624999996 0
		1.2836953722228372e-16 0.25068192187499999 0
		-1.2973119028804628e-09 0.24687365624999996 0.043530328124999997
		-2.5551997153804631e-09 0.23556403125 0.085738499999999995
		-3.7354540903804627e-09 0.21709729687499998 0.12534117187500002
		-4.8022029966304623e-09 0.19203370312500001 0.16113557812500001
		-5.7230295591304631e-09 0.16113515624999999 0.19203370312500001
		-6.4700014341304637e-09 0.12534117187500002 0.21709729687499998
		-7.0203795591304622e-09 0.085738499999999995 0.23556403125
		-7.3574154966304626e-09 0.043530328124999983 0.24687365624999996
		-7.4708998716304619e-09 -1.6046192152785466e-17 0.25068234375000004
		-0.077465109374999869 -1.6046192152785466e-17 0.23841295312500005
		-0.1473474374999999 -1.6046192152785466e-17 0.20280628125
		-0.20280628124999983 -1.6046192152785466e-17 0.14734743750000001
		-0.23841295312499988 -1.6046192152785466e-17 0.077465109374999994
		-0.25068234374999987 -1.6046192152785466e-17 0
		-0.23841295312499988 -1.6046192152785466e-17 -0.077465109374999994
		-0.20280628124999983 -1.6046192152785466e-17 -0.14734743750000001
		-0.1473474374999999 -1.6046192152785466e-17 -0.20280628125
		-0.077465109374999869 -1.6046192152785466e-17 -0.23841295312500005
		1.2836953722228372e-16 -1.6046192152785466e-17 -0.25068234375000004
		0.077465109375000132 -1.6046192152785466e-17 -0.23841295312500005
		0.14734743750000018 -1.6046192152785466e-17 -0.20280628125
		0.20280628125000011 -1.6046192152785466e-17 -0.14734743750000001
		0.23841295312500016 -1.6046192152785466e-17 -0.077465109374999994
		0.25068192187500016 -1.6046192152785466e-17 0
		0.23841295312500016 -1.6046192152785466e-17 0.077465109374999994
		0.20280628125000011 -1.6046192152785466e-17 0.14734743750000001
		0.14734743750000018 -1.6046192152785466e-17 0.20280628125
		0.077465109375000132 -1.6046192152785466e-17 0.23841295312500005
		-7.4708998716304619e-09 -1.6046192152785466e-17 0.25068234375000004
		;
createNode nurbsCurve -n "L_FrHip_Guide_Ctrl_Ctrl_CtrlShape" -p "L_FrHip_Guide";
	rename -uid "D155F681-444E-F9C6-3E69-3E8705DBBFD7";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/C:\\Users\\Esteban\\Documents\\maya\\2022\\scripts\\rigging\\Mutant_Tools\\Icons\\Guide_Data";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 13;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 9 0 no 3
		10 0 1 2 3 4 5 6 7 8 9
		10
		-0.21093749999999986 -0.10546875 -5.8966734375000001e-06
		0.3987271406250002 -0.10796456249999997 -5.8966734375000001e-06
		0.31204110937500007 -0.21365564062499998 -5.8966734375000001e-06
		0.41773218750000002 -0.39620432812499995 -5.8966734375000001e-06
		0.97001803124999997 -1.6344703126604619e-07 -5.8212421874999994e-06
		0.41773260937500012 0.39620432812499995 -5.8966734375000001e-06
		0.31204110937500007 0.21365521875000001 -5.8966734375000001e-06
		0.3987271406250002 0.10682760937499999 -3.0237721875000003e-06
		-0.21093749999999986 0.10546875 -5.8966734375000001e-06
		-0.21093749999999986 -0.10546875 -5.8966734375000001e-06
		;
createNode nurbsCurve -n "L_FrHip_Guide_Ctrl_Ctrl_Ctrl_CtrlShape" -p "L_FrHip_Guide";
	rename -uid "ABF7A81E-6F4C-8C8D-E6F6-5FA477AC77E9";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/C:\\Users\\Esteban\\Documents\\maya\\2022\\scripts\\rigging\\Mutant_Tools\\Icons\\Guide_Data";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 6;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 9 0 no 3
		10 0 1 2 3 4 5 6 7 8 9
		10
		0.10546875000000014 5.8966734374839539e-06 -0.2109375
		0.10796456250000011 5.8966734374839539e-06 0.39872714062500003
		0.21365564062500014 5.8966734374839539e-06 0.31204110937499996
		0.39620432812500012 5.8966734374839539e-06 0.41773218749999996
		1.6344703137836954e-07 5.8212421874839532e-06 0.97001803124999997
		-0.39620432812499984 5.8966734374839539e-06 0.41773260937500006
		-0.21365521874999988 5.8966734374839539e-06 0.31204110937499996
		-0.10682760937499987 3.0237721874839541e-06 0.39872714062500003
		-0.10546874999999986 5.8966734374839539e-06 -0.2109375
		0.10546875000000014 5.8966734374839539e-06 -0.2109375
		;
createNode joint -n "L_FrKnee_Guide" -p "L_FrHip_Guide";
	rename -uid "D8EC497D-F544-6E79-43BC-18BCAB689CDF";
	addAttr -ci true -sn "Helper" -ln "Helper" -min 0 -max 1 -en "Hide:Show" -at "enum";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/C:\\Users\\Esteban\\Documents\\maya\\2022\\scripts\\rigging\\Mutant_Tools\\Icons\\Guide_Data";
	setAttr ".t" -type "double3" 9.5660948671446704 6.0396132539608516e-14 -2.1316282072803006e-14 ;
	setAttr ".r" -type "double3" 0 0 61.40837360973957 ;
	setAttr ".s" -type "double3" 0.99999999999999978 0.99999999999999967 0.99999999999999989 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 7.9513867036587951e-15 0 0 ;
	setAttr -cb on ".Helper" 1;
createNode nurbsCurve -n "L_FrKnee_Guide_CtrlShape" -p "L_FrKnee_Guide";
	rename -uid "74661FA2-1C47-AA67-89F9-F68C0F2FFC7F";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/C:\\Users\\Esteban\\Documents\\maya\\2022\\scripts\\rigging\\Mutant_Tools\\Icons\\Guide_Data";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 14;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 9 0 no 3
		10 0 1 2 3 4 5 6 7 8 9
		10
		5.8966734380134782e-06 -0.21093750000000003 0.10546875
		5.8966734380134782e-06 0.39872714062500003 0.10796456249999997
		5.8966734380134782e-06 0.31204110937499996 0.21365564062499998
		5.8966734380134782e-06 0.41773218749999996 0.39620432812499995
		5.8212421880134776e-06 0.97001803124999997 1.6344703125e-07
		5.8966734380134782e-06 0.41773260937500001 -0.39620432812499995
		5.8966734380134782e-06 0.31204110937499996 -0.21365521875000001
		3.0237721880134785e-06 0.39872714062500003 -0.10682760937500001
		5.8966734380134782e-06 -0.21093750000000003 -0.10546875
		5.8966734380134782e-06 -0.21093750000000003 0.10546875
		;
createNode nurbsCurve -n "L_FrKnee_Guide_Ctrl_CtrlShape" -p "L_FrKnee_Guide";
	rename -uid "89D295DF-3743-1E90-DC70-0FACCFFF7770";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/C:\\Users\\Esteban\\Documents\\maya\\2022\\scripts\\rigging\\Mutant_Tools\\Icons\\Guide_Data";
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
		5.134781488891349e-16 0.25068192187499994 0
		-1.2973115177718512e-09 0.24687365624999991 0.043530328124999997
		-2.5551993302718514e-09 0.23556403124999997 0.085738499999999995
		-3.7354537052718511e-09 0.21709729687499996 0.12534117187500002
		-4.8022026115218507e-09 0.19203370312499998 0.16113557812500001
		-5.7230291740218515e-09 0.16113515624999994 0.19203370312500001
		-6.470001049021852e-09 0.12534117187499993 0.21709729687499998
		-7.0203791740218505e-09 0.08573849999999994 0.23556403125
		-7.357415111521851e-09 0.043530328124999934 0.24687365624999996
		-7.4708994865218502e-09 -6.4184768818501002e-17 0.25068234375000004
		-7.357415111521851e-09 -0.043530328125000059 0.24687365624999996
		-7.0203791740218505e-09 -0.085738500000000079 0.23556403125
		-6.470001049021852e-09 -0.12534117187500007 0.21709729687499998
		-5.7230291740218515e-09 -0.16113515625000008 0.19203370312500001
		-4.8022026115218507e-09 -0.19203370312500004 0.16113557812500001
		-3.7354537052718511e-09 -0.21709729687500001 0.12534117187500002
		-2.5551993302718514e-09 -0.23556403125000003 0.085738499999999995
		-1.2973115177718512e-09 -0.24687365625000005 0.043530328124999997
		5.134781488891349e-16 -0.25068192187500005 0
		5.134781488891349e-16 -0.24687365625000005 -0.043530328124999997
		5.134781488891349e-16 -0.23556403125000003 -0.085738499999999995
		5.134781488891349e-16 -0.21709729687500001 -0.12534117187500002
		5.134781488891349e-16 -0.19203370312500004 -0.16113557812500001
		5.134781488891349e-16 -0.16113515625000008 -0.19203370312500001
		5.134781488891349e-16 -0.12534117187500007 -0.21709729687499998
		5.134781488891349e-16 -0.085738500000000079 -0.23556445312500002
		5.134781488891349e-16 -0.043530328125000059 -0.24687365624999996
		5.134781488891349e-16 -6.4184768611141862e-17 -0.25068234375000004
		5.134781488891349e-16 0.043530328124999934 -0.24687365624999996
		5.134781488891349e-16 0.08573849999999994 -0.23556445312500002
		5.134781488891349e-16 0.12534117187499993 -0.21709729687499998
		5.134781488891349e-16 0.16113515624999994 -0.19203370312500001
		5.134781488891349e-16 0.19203370312499998 -0.16113557812500001
		5.134781488891349e-16 0.21709729687499996 -0.12534117187500002
		5.134781488891349e-16 0.23556403124999997 -0.085738499999999995
		5.134781488891349e-16 0.24687365624999991 -0.043530328124999997
		5.134781488891349e-16 0.25068192187499994 0
		0.04353032812500051 0.24687365624999991 0
		0.085738500000000523 0.23556403124999997 0
		0.12534117187500052 0.21709729687499996 0
		0.16113557812500051 0.19203370312499998 0
		0.19203370312500048 0.16113515624999994 0
		0.21709729687500054 0.12534117187499993 0
		0.23556403125000053 0.08573849999999994 0
		0.24687365625000049 0.043530328124999941 0
		0.25068192187500049 -5.7226947573069119e-17 0
		0.24687365625000049 -0.043530328125000059 0
		0.23556403125000053 -0.085738500000000051 0
		0.21709729687500054 -0.12534117187500007 0
		0.19203370312500048 -0.16113515625000008 0
		0.16113557812500051 -0.19203370312500004 0
		0.12534117187500052 -0.21709729687500001 0
		0.085738500000000523 -0.23556403125000003 0
		0.04353032812500051 -0.24687365625000005 0
		5.134781488891349e-16 -0.25068192187500005 0
		-0.043530328124999483 -0.24687365625000005 0
		-0.085738499999999496 -0.23556403125000003 0
		-0.12534117187499949 -0.21709729687500001 0
		-0.16113557812499951 -0.19203370312500004 0
		-0.19203370312499946 -0.16113515625000008 0
		-0.21709729687499951 -0.12534117187500007 0
		-0.23556403124999947 -0.085738500000000079 0
		-0.24687365624999946 -0.043530328125000073 0
		-0.25068234374999954 -7.1142601358598064e-17 0
		-0.24687365624999946 0.043530328124999934 0
		-0.23556403124999947 0.085738499999999926 0
		-0.21709729687499951 0.12534117187499993 0
		-0.19203370312499946 0.16113515624999994 0
		-0.16113557812499951 0.19203370312499998 0
		-0.12534117187499949 0.21709729687499996 0
		-0.085738499999999496 0.23556403124999997 0
		-0.043530328124999483 0.24687365624999991 0
		5.134781488891349e-16 0.25068192187499994 0
		-1.2973115177718512e-09 0.24687365624999991 0.043530328124999997
		-2.5551993302718514e-09 0.23556403124999997 0.085738499999999995
		-3.7354537052718511e-09 0.21709729687499996 0.12534117187500002
		-4.8022026115218507e-09 0.19203370312499998 0.16113557812500001
		-5.7230291740218515e-09 0.16113515624999994 0.19203370312500001
		-6.470001049021852e-09 0.12534117187499993 0.21709729687499998
		-7.0203791740218505e-09 0.08573849999999994 0.23556403125
		-7.357415111521851e-09 0.043530328124999934 0.24687365624999996
		-7.4708994865218502e-09 -6.4184768818501002e-17 0.25068234375000004
		-0.07746510937499948 -6.6334857311972635e-17 0.23841295312500005
		-0.14734743749999951 -6.8274481554442271e-17 0.20280628125
		-0.20280628124999947 -6.9813773685700742e-17 0.14734743750000001
		-0.23841295312499952 -7.0802057359348195e-17 0.077465109374999994
		-0.25068234374999954 -7.1142601358598064e-17 0
		-0.23841295312499952 -7.0802057359348195e-17 -0.077465109374999994
		-0.20280628124999947 -6.9813773685700742e-17 -0.14734743750000001
		-0.14734743749999951 -6.8274481554442271e-17 -0.20280628125
		-0.07746510937499948 -6.6334857311972635e-17 -0.23841295312500005
		5.134781488891349e-16 -6.4184768611141862e-17 -0.25068234375000004
		0.077465109375000507 -6.203467991031109e-17 -0.23841295312500005
		0.14734743750000054 -6.0095055667841454e-17 -0.20280628125
		0.2028062812500005 -5.8555763536582983e-17 -0.14734743750000001
		0.23841295312500055 -5.756747986293553e-17 -0.077465109374999994
		0.25068192187500049 -5.7226947573069119e-17 0
		0.23841295312500055 -5.756747986293553e-17 0.077465109374999994
		0.2028062812500005 -5.8555763536582983e-17 0.14734743750000001
		0.14734743750000054 -6.0095055667841454e-17 0.20280628125
		0.077465109375000507 -6.203467991031109e-17 0.23841295312500005
		-7.4708994865218502e-09 -6.4184768818501002e-17 0.25068234375000004
		;
createNode nurbsCurve -n "L_FrKnee_Guide_Ctrl_Ctrl_CtrlShape" -p "L_FrKnee_Guide";
	rename -uid "41143989-BB43-0C21-0ADD-26B87E158B04";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/C:\\Users\\Esteban\\Documents\\maya\\2022\\scripts\\rigging\\Mutant_Tools\\Icons\\Guide_Data";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 13;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 9 0 no 3
		10 0 1 2 3 4 5 6 7 8 9
		10
		-0.2109374999999995 -0.10546875000000007 -5.8966734375000001e-06
		0.39872714062500053 -0.10796456250000004 -5.8966734375000001e-06
		0.31204110937500051 -0.21365564062500006 -5.8966734375000001e-06
		0.41773218750000052 -0.39620432812499995 -5.8966734375000001e-06
		0.97001803125000063 -1.6344703128726138e-07 -5.8212421874999994e-06
		0.41773260937500056 0.39620432812499995 -5.8966734375000001e-06
		0.31204110937500051 0.21365521874999999 -5.8966734375000001e-06
		0.39872714062500053 0.10682760937499994 -3.0237721875000003e-06
		-0.2109374999999995 0.10546874999999993 -5.8966734375000001e-06
		-0.2109374999999995 -0.10546875000000007 -5.8966734375000001e-06
		;
createNode nurbsCurve -n "L_FrKnee_Guide_Ctrl_Ctrl_Ctrl_CtrlShape" -p "L_FrKnee_Guide";
	rename -uid "F5652E76-784B-1074-F113-5ABF449EA831";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/C:\\Users\\Esteban\\Documents\\maya\\2022\\scripts\\rigging\\Mutant_Tools\\Icons\\Guide_Data";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 6;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 9 0 no 3
		10 0 1 2 3 4 5 6 7 8 9
		10
		0.10546875000000051 5.8966734374387426e-06 -0.2109375
		0.10796456250000049 5.8966734374388121e-06 0.39872714062500003
		0.2136556406250005 5.8966734374417462e-06 0.31204110937499996
		0.3962043281250005 5.8966734374468115e-06 0.41773218749999996
		1.6344703176347815e-07 5.8212421874358146e-06 0.97001803124999997
		-0.39620432812499951 5.8966734374248183e-06 0.41773260937500006
		-0.21365521874999946 5.8966734374298844e-06 0.31204110937499996
		-0.10682760937499949 3.0237721874328501e-06 0.39872714062500003
		-0.10546874999999949 5.8966734374328879e-06 -0.2109375
		0.10546875000000051 5.8966734374387426e-06 -0.2109375
		;
createNode joint -n "L_FrAnkle_Guide" -p "L_FrKnee_Guide";
	rename -uid "EB7EA79E-914B-575F-9098-50837705CF77";
	addAttr -ci true -sn "Helper" -ln "Helper" -min 0 -max 1 -en "Hide:Show" -at "enum";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/C:\\Users\\Esteban\\Documents\\maya\\2022\\scripts\\rigging\\Mutant_Tools\\Icons\\Guide_Data";
	setAttr ".t" -type "double3" 13.624408353821497 7.1054273576010019e-15 -5.7220458504758653e-06 ;
	setAttr ".r" -type "double3" -4.9696166897867449e-17 -1.5902773407317584e-15 6.8967285907033728e-34 ;
	setAttr ".s" -type "double3" 1 1 1.0000000000000004 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" -9.5416640443905471e-15 -1.1529510720305249e-14 -7.9513867036587919e-15 ;
	setAttr -cb on ".Helper" 1;
createNode nurbsCurve -n "L_FrAnkle_Guide_CtrlShape" -p "L_FrAnkle_Guide";
	rename -uid "91FE7AB2-104F-270B-85D0-839F8C2F2948";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/C:\\Users\\Esteban\\Documents\\maya\\2022\\scripts\\rigging\\Mutant_Tools\\Icons\\Guide_Data";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 14;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 9 0 no 3
		10 0 1 2 3 4 5 6 7 8 9
		10
		5.8966734374999984e-06 -0.2109375 0.10546875000000004
		5.8966734374999984e-06 0.39872714062500003 0.10796456249999997
		5.8966734374999984e-06 0.31204110937499996 0.21365564062499995
		5.8966734374999984e-06 0.41773218749999996 0.39620432812499989
		5.8212421874999986e-06 0.97001803124999997 1.6344703129683743e-07
		5.8966734374999984e-06 0.41773260937500006 -0.39620432812499984
		5.8966734374999984e-06 0.31204110937499996 -0.21365521874999985
		3.0237721874999991e-06 0.39872714062500003 -0.10682760937499991
		5.8966734374999984e-06 -0.2109375 -0.10546874999999994
		5.8966734374999984e-06 -0.2109375 0.10546875000000004
		;
createNode nurbsCurve -n "L_FrAnkle_Guide_Ctrl_CtrlShape" -p "L_FrAnkle_Guide";
	rename -uid "22F9212C-2848-4A6F-4ABF-30A18F1257E6";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/C:\\Users\\Esteban\\Documents\\maya\\2022\\scripts\\rigging\\Mutant_Tools\\Icons\\Guide_Data";
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
		0 0.25068192187499999 4.6837533851373779e-17
		-1.2973120312499997e-09 0.24687365624999996 0.043530328125000031
		-2.555199843749999e-09 0.23556403125 0.085738500000000023
		-3.7354542187499983e-09 0.21709729687499998 0.12534117187500002
		-4.8022031249999979e-09 0.19203370312500001 0.16113557812500001
		-5.7230296874999979e-09 0.16113515624999999 0.19203370312500001
		-6.4700015624999984e-09 0.12534117187500002 0.21709729687499996
		-7.0203796874999986e-09 0.085738499999999995 0.23556403124999997
		-7.357415624999999e-09 0.043530328124999997 0.24687365624999993
		-7.4708999999999974e-09 0 0.25068234374999998
		-7.357415624999999e-09 -0.043530328124999997 0.24687365624999993
		-7.0203796874999986e-09 -0.085738499999999995 0.23556403124999997
		-6.4700015624999984e-09 -0.12534117187500002 0.21709729687499996
		-5.7230296874999979e-09 -0.16113515624999999 0.19203370312500001
		-4.8022031249999979e-09 -0.19203370312500001 0.16113557812500001
		-3.7354542187499983e-09 -0.21709729687499998 0.12534117187500002
		-2.555199843749999e-09 -0.23556403125 0.085738500000000023
		-1.2973120312499997e-09 -0.24687365624999996 0.043530328125000031
		0 -0.25068192187499999 4.6837533851373779e-17
		0 -0.24687365624999996 -0.043530328124999934
		0 -0.23556403125 -0.085738499999999912
		0 -0.21709729687499998 -0.12534117187499991
		0 -0.19203370312500001 -0.1611355781249999
		0 -0.16113515624999999 -0.19203370312499993
		0 -0.12534117187500002 -0.21709729687499985
		0 -0.085738499999999995 -0.23556445312499985
		0 -0.043530328124999997 -0.24687365624999985
		0 0 -0.25068234374999987
		0 0.043530328124999997 -0.24687365624999985
		0 0.085738499999999995 -0.23556445312499985
		0 0.12534117187500002 -0.21709729687499985
		0 0.16113515624999999 -0.19203370312499993
		0 0.19203370312500001 -0.1611355781249999
		0 0.21709729687499998 -0.12534117187499991
		0 0.23556403125 -0.085738499999999912
		0 0.24687365624999996 -0.043530328124999934
		0 0.25068192187499999 4.6837533851373779e-17
		0.043530328124999976 0.24687365624999996 4.6233429194450477e-17
		0.085738499999999968 0.23556403125 4.5647673141413483e-17
		0.12534117187499993 0.21709729687499998 4.5098075664509726e-17
		0.1611355781249999 0.19203370312500001 4.4601328489865519e-17
		0.19203370312499993 0.16113515624999999 4.4172530867456189e-17
		0.2170972968749999 0.12534117187500002 4.3824703631692428e-17
		0.23556403124999992 0.085738499999999995 4.3568426210532917e-17
		0.24687365624999993 0.043530328124999997 4.3411473634596964e-17
		0.25068192187499988 0 4.3358623332337414e-17
		0.24687365624999993 -0.043530328124999997 4.3411473634596964e-17
		0.23556403124999992 -0.085738499999999995 4.3568426210532917e-17
		0.2170972968749999 -0.12534117187500002 4.3824703631692428e-17
		0.19203370312499993 -0.16113515624999999 4.4172530867456189e-17
		0.1611355781249999 -0.19203370312500001 4.4601328489865519e-17
		0.12534117187499993 -0.21709729687499998 4.5098075664509726e-17
		0.085738499999999968 -0.23556403125 4.5647673141413483e-17
		0.043530328124999976 -0.24687365624999996 4.6233429194450477e-17
		0 -0.25068192187499999 4.6837533851373779e-17
		-0.043530328124999976 -0.24687365624999996 4.7441638508297069e-17
		-0.085738499999999968 -0.23556403125 4.8027394561334087e-17
		-0.12534117187499993 -0.21709729687499998 4.8576992038237833e-17
		-0.1611355781249999 -0.19203370312500001 4.9073739212882046e-17
		-0.19203370312499993 -0.16113515624999999 4.9502536835291376e-17
		-0.2170972968749999 -0.12534117187500002 4.9850364071055136e-17
		-0.23556403124999992 -0.085738499999999995 5.0106641492214659e-17
		-0.24687365624999993 -0.043530328124999997 5.0263594068150619e-17
		-0.25068234374999987 0 5.0316450225101886e-17
		-0.24687365624999993 0.043530328124999997 5.0263594068150619e-17
		-0.23556403124999992 0.085738499999999995 5.0106641492214659e-17
		-0.2170972968749999 0.12534117187500002 4.9850364071055136e-17
		-0.19203370312499993 0.16113515624999999 4.9502536835291376e-17
		-0.1611355781249999 0.19203370312500001 4.9073739212882046e-17
		-0.12534117187499993 0.21709729687499998 4.8576992038237833e-17
		-0.085738499999999968 0.23556403125 4.8027394561334087e-17
		-0.043530328124999976 0.24687365624999996 4.7441638508297069e-17
		0 0.25068192187499999 4.6837533851373779e-17
		-1.2973120312499997e-09 0.24687365624999996 0.043530328125000031
		-2.555199843749999e-09 0.23556403125 0.085738500000000023
		-3.7354542187499983e-09 0.21709729687499998 0.12534117187500002
		-4.8022031249999979e-09 0.19203370312500001 0.16113557812500001
		-5.7230296874999979e-09 0.16113515624999999 0.19203370312500001
		-6.4700015624999984e-09 0.12534117187500002 0.21709729687499996
		-7.0203796874999986e-09 0.085738499999999995 0.23556403124999997
		-7.357415624999999e-09 0.043530328124999997 0.24687365624999993
		-7.4708999999999974e-09 0 0.25068234374999998
		-0.07746510937499998 0 0.23841295312499999
		-0.14734743749999996 0 0.20280628125
		-0.20280628124999994 0 0.14734743750000001
		-0.23841295312499991 0 0.077465109375000049
		-0.25068234374999987 0 5.0316450225101886e-17
		-0.23841295312499991 0 -0.077465109374999924
		-0.20280628124999994 0 -0.1473474374999999
		-0.14734743749999996 0 -0.20280628124999989
		-0.07746510937499998 0 -0.23841295312499988
		0 0 -0.25068234374999987
		0.07746510937499998 0 -0.23841295312499988
		0.14734743749999996 0 -0.20280628124999989
		0.20280628124999994 0 -0.1473474374999999
		0.23841295312499991 0 -0.077465109374999952
		0.25068192187499988 0 4.3358623332337414e-17
		0.23841295312499991 0 0.077465109375000007
		0.20280628124999994 0 0.14734743750000001
		0.14734743749999996 0 0.20280628125
		0.07746510937499998 0 0.23841295312499999
		-7.4708999999999974e-09 0 0.25068234374999998
		;
createNode nurbsCurve -n "L_FrAnkle_Guide_Ctrl_Ctrl_CtrlShape" -p "L_FrAnkle_Guide";
	rename -uid "EC25389F-B64A-843C-CEB6-088334C82396";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/C:\\Users\\Esteban\\Documents\\maya\\2022\\scripts\\rigging\\Mutant_Tools\\Icons\\Guide_Data";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 13;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 9 0 no 3
		10 0 1 2 3 4 5 6 7 8 9
		10
		-0.21093749999999992 -0.10546875 -5.8966734374502335e-06
		0.39872714062499981 -0.10796456249999997 -5.8966734374586937e-06
		0.3120411093749999 -0.21365564062499998 -5.8966734374574909e-06
		0.4177321874999998 -0.39620432812499995 -5.8966734374589571e-06
		0.97001803124999952 -1.6344703125e-07 -5.8212421874666238e-06
		0.41773260937499979 0.39620432812499995 -5.8966734374589571e-06
		0.3120411093749999 0.21365521875000001 -5.8966734374574909e-06
		0.39872714062499981 0.10682760937500001 -3.0237721874586952e-06
		-0.21093749999999992 0.10546875 -5.8966734374502335e-06
		-0.21093749999999992 -0.10546875 -5.8966734374502335e-06
		;
createNode nurbsCurve -n "L_FrAnkle_Guide_Ctrl_Ctrl_Ctrl_CtrlShape" -p "L_FrAnkle_Guide";
	rename -uid "23194809-6F47-C9C2-7680-6781DE4CA04B";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/C:\\Users\\Esteban\\Documents\\maya\\2022\\scripts\\rigging\\Mutant_Tools\\Icons\\Guide_Data";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 6;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 9 0 no 3
		10 0 1 2 3 4 5 6 7 8 9
		10
		0.10546874999999996 5.8966734375000001e-06 -0.21093749999999992
		0.10796456249999994 5.8966734375000001e-06 0.39872714062499998
		0.21365564062499992 5.8966734375000001e-06 0.31204110937499996
		0.39620432812499984 5.8966734375000001e-06 0.41773218749999996
		1.6344703124999992e-07 5.8212421874999994e-06 0.97001803124999952
		-0.39620432812499984 5.8966734375000001e-06 0.41773260937500001
		-0.21365521874999985 5.8966734375000001e-06 0.31204110937499996
		-0.10682760937499992 3.0237721875000003e-06 0.39872714062499998
		-0.10546874999999996 5.8966734375000001e-06 -0.21093749999999992
		0.10546874999999996 5.8966734375000001e-06 -0.21093749999999992
		;
createNode dagContainer -n "L_Pelvis_Block" -p "Body";
	rename -uid "37C2F83F-9A48-0A4F-9185-ECBFAB94D5A6";
	addAttr -ci true -sn "nts" -ln "notes" -dt "string";
	setAttr ".isc" yes;
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/Pelvis.png";
	setAttr ".ctor" -type "string" "PC";
	setAttr ".cdat" -type "string" "2021/09/18 08:14:29";
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
	setAttr ".nts" -type "string" "['L_Pelvis_Bnd', 'R_Pelvis_Bnd_parentConstraint1', 'L_Pelvis_Bnd_parentConstraint1', 'L_Pelvis_Jnt_scaleConstraint1', 'L_Pelvis_CtrlShape', 'L_Pelvis_Jnt_Ctrl_tag', 'R_Pelvis_Jnt_Ctrl_tag', 'L_Pelvis_Ctrl_Offset_Grp_parentConstraint1', 'R_Pelvis_Ctrl_Offset_Grp', 'R_Pelvis_Jnt', 'R_Pelvis_JntMirror_Grp', 'R_Pelvis_Jnt_scaleConstraint1', 'R_Pelvis_Jnt_parentConstraint1', 'L_Pelvis_Ctrl_Offset_Grp', 'L_Pelvis_Ctrl', 'R_Pelvis_CtrlShape', 'R_PelvisEnd_Jnt', 'L_Pelvis_Jnt_parentConstraint1', 'R_Pelvis_Bnd', 'R_Pelvis_Ctrl_Offset_Grp_parentConstraint1', 'L_PelvisEnd_Jnt', 'R_Pelvis_Bnd_scaleConstraint1', 'L_Pelvis_Bnd_scaleConstraint1', 'R_Pelvis_Ctrl', 'R_Pelvis_Ctrl_Offset_GrpMirror_Grp', 'L_Pelvis_Jnt']";
createNode joint -n "L_Pelvis_Guide" -p "L_Pelvis_Block";
	rename -uid "E486BB2A-1645-DA4E-554B-BD989BE066BA";
	addAttr -ci true -sn "Helper" -ln "Helper" -min 0 -max 1 -en "Hide:Show" -at "enum";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/C:\\Users\\Esteban\\Documents\\maya\\2022\\scripts\\rigging\\Mutant_Tools\\Icons\\Guide_Data";
	setAttr ".t" -type "double3" 6.348971805970641 22.255360780363496 -32.09575525750904 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 90.000000000000014 -3.5353859000106862 3.4647768230324671 ;
	setAttr -cb on ".Helper" 1;
createNode nurbsCurve -n "L_Pelvis_Guide_CtrlShape" -p "L_Pelvis_Guide";
	rename -uid "E902C564-6D48-38EA-60A9-C798946E25C3";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/C:\\Users\\Esteban\\Documents\\maya\\2022\\scripts\\rigging\\Mutant_Tools\\Icons\\Guide_Data";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 14;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 9 0 no 3
		10 0 1 2 3 4 5 6 7 8 9
		10
		5.8966732780480942e-06 -0.21093749999995884 0.10546875000001119
		5.896673278257922e-06 0.39872714062504261 0.10796456250001212
		5.8966732779029585e-06 0.31204110937504143 0.21365564062501205
		5.8966732773809727e-06 0.41773218750004198 0.39620432812501261
		5.8212420287927227e-06 0.97001803125004349 1.6344704424459706e-07
		5.8966732798104496e-06 0.41773260937504331 -0.39620432812498807
		5.8966732792130635e-06 0.31204110937504198 -0.21365521874998827
		3.0237720289164464e-06 0.39872714062504266 -0.10682760937498803
		5.8966732786948131e-06 -0.21093749999995856 -0.10546874999998898
		5.8966732780480942e-06 -0.21093749999995884 0.10546875000001119
		;
createNode nurbsCurve -n "L_Pelvis_Guide_Ctrl_CtrlShape" -p "L_Pelvis_Guide";
	rename -uid "EF74E415-1446-A746-5D84-74B335B0B296";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/C:\\Users\\Esteban\\Documents\\maya\\2022\\scripts\\rigging\\Mutant_Tools\\Icons\\Guide_Data";
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
		-1.589639032928082e-13 0.25068192187504174 1.1838262055137291e-14
		-1.2974711299728756e-09 0.24687365625004212 0.043530328125011848
		-2.5553590759146858e-09 0.23556403125004211 0.085738500000011847
		-3.7356135789212762e-09 0.21709729687504203 0.1253411718750119
		-4.8023626038551906e-09 0.19203370312504212 0.16113557812501189
		-5.7231892721088744e-09 0.16113515625004143 0.19203370312501195
		-6.4701612367205561e-09 0.12534117187504146 0.21709729687501184
		-7.0205394324653328e-09 0.085738500000041518 0.23556403125001177
		-7.3575754196963102e-09 0.043530328125041505 0.24687365625001162
		-7.4710598219015411e-09 4.1503426545359286e-14 0.25068234375001153
		-7.3575754507524158e-09 -0.043530328124958488 0.24687365625001156
		-7.020539493634282e-09 -0.085738499999958473 0.23556403125001149
		-6.470161326143482e-09 -0.12534117187495858 0.21709729687501134
		-5.7231893870685244e-09 -0.16113515624995856 0.19203370312501133
		-4.8023627408589788e-09 -0.19203370312495879 0.16113557812501111
		-3.7356137338063311e-09 -0.21709729687495882 0.12534117187501106
		-2.5553592439745806e-09 -0.23556403124995878 0.08573850000001107
		-1.297471306101466e-09 -0.24687365624995869 0.043530328125011043
		-1.5914274883791483e-13 -0.25068192187495825 1.1032332252140053e-14
		-1.5900792925917096e-13 -0.24687365624995863 -0.043530328124988978
		-1.5887448745340452e-13 -0.23556403124995862 -0.085738499999988976
		-1.5874648086771144e-13 -0.21709729687495855 -0.12534117187498903
		-1.5862779695310002e-13 -0.19203370312495863 -0.16113557812498902
		-1.5852204327911147e-13 -0.16113515624995794 -0.19203370312498907
		-1.5843243160027901e-13 -0.12534117187495797 -0.21709729687498897
		-1.5836168553404635e-13 -0.085738499999958029 -0.23556445312498892
		-1.5831195584884071e-13 -0.043530328124958002 -0.24687365624998875
		-1.582847506104992e-13 4.1991199573054788e-14 -0.25068234374998866
		-1.5828089973915414e-13 0.043530328125041991 -0.24687365624998869
		-1.583005165887375e-13 0.085738500000041962 -0.23556445312498864
		-1.5834300867723524e-13 0.12534117187504207 -0.21709729687498847
		-1.5840708363367776e-13 0.16113515625004204 -0.19203370312498846
		-1.5849079316735687e-13 0.19203370312504228 -0.16113557812498824
		-1.5859159580814925e-13 0.21709729687504231 -0.12534117187498819
		-1.587064275579749e-13 0.23556403125004227 -0.085738499999988199
		-1.5883180066842842e-13 0.24687365625004218 -0.043530328124988173
		-1.589639032928082e-13 0.25068192187504174 1.1838262055137291e-14
		0.043530328124841179 0.24687365625004229 1.1982481307008557e-14
		0.085738499999841261 0.23556403125004249 1.211007597323649e-14
		0.12534117187484139 0.21709729687504259 1.2217167135408128e-14
		0.16113557812484158 0.19203370312504278 1.2300501382823901e-14
		0.19203370312484178 0.16113515625004238 1.2357545774879544e-14
		0.21709729687484189 0.12534117187504246 1.2386570119982224e-14
		0.23556403124984193 0.085738500000042531 1.2386688484490084e-14
		0.24687365624984195 0.043530328125042574 1.2357900023498644e-14
		0.25068192187484173 4.2590470365764947e-14 1.2301078741700649e-14
		0.24687365624984189 -0.043530328124957419 1.2217952202340317e-14
		0.23556403124984193 -0.08573849999995746 1.2111043508189261e-14
		0.21709729687484178 -0.12534117187495758 1.1983604540330145e-14
		0.19203370312484172 -0.16113515624995761 1.1839504331120197e-14
		0.16113557812484142 -0.19203370312495813 1.1683122660932913e-14
		0.12534117187484128 -0.21709729687495827 1.1519210216963303e-14
		0.085738499999841178 -0.23556403124995839 1.1352749430187205e-14
		0.043530328124840985 -0.24687365624995852 1.1188794886948378e-14
		-1.5914274883791483e-13 -0.25068192187495825 1.1032332252140053e-14
		-0.043530328125159286 -0.2468736562499588 1.0888113000268803e-14
		-0.085738500000159368 -0.235564031249959 1.0760518334040851e-14
		-0.1253411718751595 -0.2170972968749591 1.0653427171869233e-14
		-0.16113557812515966 -0.19203370312495929 1.0570092924453464e-14
		-0.19203370312515988 -0.16113515624995889 1.0513048532397807e-14
		-0.21709729687516 -0.12534117187495897 1.0484024187295125e-14
		-0.23556403125016007 -0.085738499999959042 1.0483905822787273e-14
		-0.24687365625016006 -0.043530328124959071 1.0512694283778724e-14
		-0.25068234375015985 4.0904154358819685e-14 1.0569514108544601e-14
		-0.24687365625016 0.043530328125040922 1.0652642104937043e-14
		-0.23556403125016007 0.085738500000040949 1.0759550799088102e-14
		-0.21709729687515988 0.12534117187504107 1.0886989766947259e-14
		-0.19203370312515983 0.1611351562500411 1.1031089976157148e-14
		-0.1611355781251595 0.19203370312504162 1.1187471646344445e-14
		-0.12534117187515939 0.21709729687504176 1.1351384090314068e-14
		-0.085738500000159285 0.23556403125004188 1.1517844877090149e-14
		-0.043530328125159092 0.24687365625004201 1.1681799420328958e-14
		-1.589639032928082e-13 0.25068192187504174 1.1838262055137291e-14
		-1.2974711299728756e-09 0.24687365625004212 0.043530328125011848
		-2.5553590759146858e-09 0.23556403125004211 0.085738500000011847
		-3.7356135789212762e-09 0.21709729687504203 0.1253411718750119
		-4.8023626038551906e-09 0.19203370312504212 0.16113557812501189
		-5.7231892721088744e-09 0.16113515625004143 0.19203370312501195
		-6.4701612367205561e-09 0.12534117187504146 0.21709729687501184
		-7.0205394324653328e-09 0.085738500000041518 0.23556403125001177
		-7.3575754196963102e-09 0.043530328125041505 0.24687365625001162
		-7.4710598219015411e-09 4.1503426545359286e-14 0.25068234375001153
		-0.077465109375159963 4.1254812957599596e-14 0.23841295312501146
		-0.14734743750016008 4.1054408308183729e-14 0.2028062812500111
		-0.20280628125016023 4.0921830387244317e-14 0.14734743750001084
		-0.23841295312516031 4.0870056820233231e-14 0.077465109375010638
		-0.25068234375015985 4.0904154358819685e-14 1.0569514108544601e-14
		-0.23841295312515987 4.1020786977087619e-14 -0.077465109374989405
		-0.20280628125015951 4.1208536267422604e-14 -0.1473474374999893
		-0.14734743750015891 4.1449024966321857e-14 -0.20280628124998928
		-0.077465109375158547 4.1718712410018681e-14 -0.23841295312498903
		-1.582847506104992e-13 4.1991199573054788e-14 -0.25068234374998866
		0.077465109374841856 4.2239813185942493e-14 -0.23841295312498859
		0.14734743749984197 4.2440217835358373e-14 -0.20280628124998823
		0.20280628124984212 4.2572795756297772e-14 -0.14734743749998797
		0.2384129531248422 4.2624569323308864e-14 -0.077465109374987767
		0.25068192187484173 4.2590470365764947e-14 1.2301078741700649e-14
		0.23841295312484176 4.2473839166454483e-14 0.077465109375012275
		0.2028062812498414 4.2286089876119491e-14 0.14734743750001217
		0.14734743749984081 4.2045601177220245e-14 0.20280628125001215
		0.077465109374840441 4.1775913733523395e-14 0.2384129531250119
		-7.4710598219015411e-09 4.1503426545359286e-14 0.25068234375001153
		;
createNode nurbsCurve -n "L_Pelvis_Guide_Ctrl_Ctrl_CtrlShape" -p "L_Pelvis_Guide";
	rename -uid "A8741D0E-BB40-A487-A815-D7A8B4955814";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/C:\\Users\\Esteban\\Documents\\maya\\2022\\scripts\\rigging\\Mutant_Tools\\Icons\\Guide_Data";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 13;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 9 0 no 3
		10 0 1 2 3 4 5 6 7 8 9
		10
		-0.2109375000001599 -0.10546874999995914 -5.8966734269627637e-06
		0.39872714062484255 -0.10796456249995709 -5.8966734248611741e-06
		0.31204110937484175 -0.21365564062495759 -5.8966734253304566e-06
		0.41773218749984248 -0.39620432812495771 -5.8966734252588756e-06
		0.97001803124984498 -1.6344698624006959e-07 -5.8212421727145514e-06
		0.4177326093748428 0.39620432812504397 -5.8966734239850939e-06
		0.31204110937484175 0.21365521875004329 -5.8966734246435654e-06
		0.39872714062484266 0.10682760937504332 -3.0237721745158967e-06
		-0.2109375000001599 0.1054687500000413 -5.8966734266236854e-06
		-0.2109375000001599 -0.10546874999995914 -5.8966734269627637e-06
		;
createNode nurbsCurve -n "L_Pelvis_Guide_Ctrl_Ctrl_Ctrl_CtrlShape" -p "L_Pelvis_Guide";
	rename -uid "4F2BFAD1-6C4A-C45C-CF43-ADBFE2BC2267";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/C:\\Users\\Esteban\\Documents\\maya\\2022\\scripts\\rigging\\Mutant_Tools\\Icons\\Guide_Data";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 6;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 9 0 no 3
		10 0 1 2 3 4 5 6 7 8 9
		10
		0.10546874999984206 5.8966734798072858e-06 -0.21093749999998837
		0.10796456249984013 5.8966734792225442e-06 0.39872714062501241
		0.21365564062484096 5.8966734796623652e-06 0.31204110937501223
		0.39620432812484124 5.8966734801735327e-06 0.41773218750001312
		1.634468692226655e-07 5.8212422283036051e-06 0.97001803125001218
		-0.3962043281251621 5.8966734775083028e-06 0.41773260937501044
		-0.21365521875016072 5.8966734782251239e-06 0.31204110937501078
		-0.10682760937516071 3.0237722285000923e-06 0.3987271406250113
		-0.1054687500001588 5.8966734790978076e-06 -0.21093749999998909
		0.10546874999984206 5.8966734798072858e-06 -0.21093749999998837
		;
createNode joint -n "L_PelvisEnd_Guide" -p "L_Pelvis_Guide";
	rename -uid "704FE88B-BF43-A348-8960-DC9264926229";
	addAttr -ci true -sn "Helper" -ln "Helper" -min 0 -max 1 -en "Hide:Show" -at "enum";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/C:\\Users\\Esteban\\Documents\\maya\\2022\\scripts\\rigging\\Mutant_Tools\\Icons\\Guide_Data";
	setAttr ".t" -type "double3" 5.4411303178204449 3.7451944442516688e-15 3.6515783949731231e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" -112.89156534843364 -0.23773974180532906 -1.7683047943033274 ;
	setAttr -cb on ".Helper" 1;
createNode nurbsCurve -n "L_PelvisEnd_Guide_CtrlShape" -p "L_PelvisEnd_Guide";
	rename -uid "AD14F05F-D34A-5C4E-DBA4-D8A4145F1E02";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/C:\\Users\\Esteban\\Documents\\maya\\2022\\scripts\\rigging\\Mutant_Tools\\Icons\\Guide_Data";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 14;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 9 0 no 3
		10 0 1 2 3 4 5 6 7 8 9
		10
		5.8966732670508418e-06 -0.21093750000003519 0.10546875000005206
		5.896673267375878e-06 0.39872714062496539 0.10796456250005285
		5.8966732672752945e-06 0.31204110937496465 0.21365564062505263
		5.8966732672382868e-06 0.4177321874999651 0.39620432812505291
		5.821242017736998e-06 0.97001803124996588 1.6344708482187676e-07
		5.8966732676445103e-06 0.41773260937496559 -0.39620432812494755
		5.8966732674943525e-06 0.31204110937496499 -0.21365521874994722
		3.0237720174859875e-06 0.3987271406249655 -0.1068276093749472
		5.8966732671589783e-06 -0.21093750000003503 -0.10546874999994789
		5.8966732670508418e-06 -0.21093750000003519 0.10546875000005206
		;
createNode nurbsCurve -n "L_PelvisEnd_Guide_Ctrl_CtrlShape" -p "L_PelvisEnd_Guide";
	rename -uid "1CAC96FA-8F46-A99B-2AB7-6F970E56B5EA";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/C:\\Users\\Esteban\\Documents\\maya\\2022\\scripts\\rigging\\Mutant_Tools\\Icons\\Guide_Data";
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
		-1.7014801775758173e-13 0.25068192187496485 5.2653165404369727e-14
		-1.2974822036215868e-09 0.24687365624996513 0.043530328125052621
		-2.5553700438126006e-09 0.23556403124996511 0.085738500000052606
		-3.7356244489986455e-09 0.21709729687496504 0.12534117187505239
		-4.8023733870132707e-09 0.19203370312496507 0.16113557812505247
		-5.7231999818909297e-09 0.16113515624996491 0.19203370312505255
		-6.4701718888977435e-09 0.12534117187496488 0.21709729687505244
		-7.0205500445612653e-09 0.085738499999964884 0.23556403125005246
		-7.3575860104502897e-09 0.043530328124964782 0.24687365625005236
		-7.4710704107016662e-09 -3.5222129125820312e-14 0.25068234375005177
		-7.3575860570480735e-09 -0.043530328125035198 0.24687365625005225
		-7.0205501363415004e-09 -0.085738500000035078 0.23556403125005224
		-6.4701720230713374e-09 -0.12534117187503505 0.21709729687505211
		-5.7232001543808018e-09 -0.16113515625003502 0.19203370312505216
		-4.8023735925790266e-09 -0.19203370312503518 0.16113557812505197
		-3.7356246813941469e-09 -0.2170972968750351 0.12534117187505184
		-2.5553702959761329e-09 -0.23556403125003511 0.085738500000051968
		-1.2974824678916996e-09 -0.24687365625003502 0.043530328125051983
		-1.7041636449313653e-13 -0.25068192187503491 5.2012859520413704e-14
		-1.7039201066228987e-13 -0.24687365625003502 -0.043530328124947955
		-1.7036431964664014e-13 -0.23556403125003506 -0.085738499999947912
		-1.7033413359755883e-13 -0.21709729687503493 -0.12534117187494775
		-1.7030236896904415e-13 -0.19203370312503495 -0.16113557812494783
		-1.7026999132249055e-13 -0.16113515625003486 -0.19203370312494791
		-1.7023798450548e-13 -0.12534117187503471 -0.21709729687494775
		-1.7020732076897254e-13 -0.085738500000034773 -0.23556445312494781
		-1.7017893195632344e-13 -0.043530328125034864 -0.24687365624994773
		-1.7015368056840607e-13 -3.486069926972531e-14 -0.25068234374994741
		-1.7013233417470997e-13 0.043530328124965115 -0.24687365624994762
		-1.7011554053043654e-13 0.08573849999996519 -0.23556445312494759
		-1.70103810911901e-13 0.12534117187496521 -0.21709729687494742
		-1.700975014483131e-13 0.16113515624996508 -0.19203370312494752
		-1.7009680321877128e-13 0.19203370312496529 -0.16113557812494733
		-1.7010173809620625e-13 0.21709729687496521 -0.1253411718749472
		-1.7011215611475375e-13 0.23556403124996517 -0.085738499999947274
		-1.701277405495764e-13 0.24687365624996513 -0.043530328124947316
		-1.7014801775758173e-13 0.25068192187496485 5.2653165404369727e-14
		0.043530328124829792 0.24687365624996482 5.2850480361343953e-14
		0.085738499999829729 0.23556403124996472 5.3032074305827137e-14
		0.12534117187482963 0.21709729687496451 5.3192426340436045e-14
		0.16113557812482956 0.19203370312496443 5.3326665676257845e-14
		0.19203370312482973 0.16113515624996419 5.3430712026879738e-14
		0.21709729687482965 0.12534117187496391 5.3501407529119685e-14
		0.23556403124982969 0.085738499999963927 5.3536599434158162e-14
		0.24687365624982965 0.043530328124963845 5.3535222259881523e-14
		0.25068192187482918 -3.6179447899756278e-14 5.3497316115861058e-14
		0.24687365624982965 -0.043530328125036134 5.3424034644035523e-14
		0.23556403124982964 -0.085738500000036036 5.3317601328427429e-14
		0.2170972968748297 -0.12534117187503602 5.3181254048353212e-14
		0.19203370312482967 -0.16113515625003574 5.3019131535205928e-14
		0.16113557812482945 -0.19203370312503582 5.2836162375863831e-14
		0.12534117187482929 -0.21709729687503562 5.2637904197234477e-14
		0.085738499999829479 -0.2355640312500355 5.2430383389587116e-14
		0.043530328124829543 -0.24687365625003532 5.2219901763939397e-14
		-1.7041636449313653e-13 -0.25068192187503491 5.2012859520413704e-14
		-0.043530328125170339 -0.24687365625003488 5.1815544563439491e-14
		-0.08573850000017029 -0.23556403125003472 5.1633950618956307e-14
		-0.12534117187517016 -0.21709729687503451 5.1473598584347399e-14
		-0.16113557812517007 -0.19203370312503443 5.1339359248525586e-14
		-0.19203370312517026 -0.16113515625003402 5.1235312897903693e-14
		-0.21709729687517018 -0.12534117187503407 5.1164617395663772e-14
		-0.23556403125017025 -0.085738500000033871 5.1129425490625283e-14
		-0.24687365625017019 -0.043530328125033928 5.1130802664901928e-14
		-0.25068234375016973 -3.390337861449762e-14 5.1168706849504661e-14
		-0.24687365625017019 0.043530328124966051 5.1241990280747928e-14
		-0.2355640312501702 0.085738499999966092 5.1348423596356015e-14
		-0.21709729687517024 0.12534117187496585 5.1484770876430219e-14
		-0.19203370312517021 0.16113515624996591 5.164689338957751e-14
		-0.16113557812516996 0.19203370312496582 5.1829862548919607e-14
		-0.12534117187516983 0.21709729687496562 5.2028120727548955e-14
		-0.08573850000017004 0.2355640312499655 5.2235641535196316e-14
		-0.04353032812517009 0.24687365624996527 5.2446123160844041e-14
		-1.7014801775758173e-13 0.25068192187496485 5.2653165404369727e-14
		-1.2974822036215868e-09 0.24687365624996513 0.043530328125052621
		-2.5553700438126006e-09 0.23556403124996511 0.085738500000052606
		-3.7356244489986455e-09 0.21709729687496504 0.12534117187505239
		-4.8023733870132707e-09 0.19203370312496507 0.16113557812505247
		-5.7231999818909297e-09 0.16113515624996491 0.19203370312505255
		-6.4701718888977435e-09 0.12534117187496488 0.21709729687505244
		-7.0205500445612653e-09 0.085738499999964884 0.23556403125005246
		-7.3575860104502897e-09 0.043530328124964782 0.24687365625005236
		-7.4710704107016662e-09 -3.5222129125820312e-14 0.25068234375005177
		-0.07746510937517026 -3.486161188857629e-14 0.23841295312505204
		-0.14734743750017013 -3.4518694897705651e-14 0.20280628125005171
		-0.20280628125017033 -3.4226945669022203e-14 0.14734743750005116
		-0.23841295312517022 -3.4014922594367422e-14 0.077465109375051119
		-0.25068234375016973 -3.390337861449762e-14 5.1168706849504661e-14
		-0.23841295312517027 -3.390323460891831e-14 -0.077465109374948646
		-0.20280628125017017 -3.4014502433761311e-14 -0.14734743749994841
		-0.1473474375001699 -3.4226291967251022e-14 -0.20280628124994834
		-0.07746510937517001 -3.451787181444042e-14 -0.23841295312494812
		-1.7015368056840607e-13 -3.486069926972531e-14 -0.25068234374994741
		0.077465109374829699 -3.522121654088536e-14 -0.23841295312494734
		0.14734743749982959 -3.5564133531756005e-14 -0.20280628124994701
		0.2028062812498298 -3.585588276043946e-14 -0.14734743749994653
		0.23841295312482969 -3.6067905835094228e-14 -0.077465109374946481
		0.25068192187482918 -3.6179447899756278e-14 5.3497316115861058e-14
		0.23841295312482974 -3.6179593820543346e-14 0.077465109375053284
		0.20280628124982963 -3.6068325995700357e-14 0.14734743750005305
		0.14734743749982937 -3.5856536462210647e-14 0.20280628125005304
		0.077465109374829449 -3.5564956615021217e-14 0.23841295312505281
		-7.4710704107016662e-09 -3.5222129125820312e-14 0.25068234375005177
		;
createNode nurbsCurve -n "L_PelvisEnd_Guide_Ctrl_Ctrl_CtrlShape" -p "L_PelvisEnd_Guide";
	rename -uid "EEE1CFF4-3949-1497-0136-3582CACA1A3F";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/C:\\Users\\Esteban\\Documents\\maya\\2022\\scripts\\rigging\\Mutant_Tools\\Icons\\Guide_Data";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 13;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 9 0 no 3
		10 0 1 2 3 4 5 6 7 8 9
		10
		-0.21093750000017025 -0.10546875000003403 -5.8966733862813941e-06
		0.39872714062482978 -0.10796456250003685 -5.8966733834529673e-06
		0.31204110937482904 -0.21365564062503642 -5.8966733839905656e-06
		0.41773218749982932 -0.39620432812503703 -5.896673383732816e-06
		0.97001803124982955 -1.6344707069505103e-07 -5.8212421306616949e-06
		0.41773260937482998 0.39620432812496353 -5.8966733827208098e-06
		0.31204110937482926 0.21365521874996377 -5.8966733834448366e-06
		0.39872714062482967 0.10682760937496323 -3.0237721331786505e-06
		-0.21093750000017009 0.10546874999996605 -5.8966733860119995e-06
		-0.21093750000017025 -0.10546875000003403 -5.8966733862813941e-06
		;
createNode nurbsCurve -n "L_PelvisEnd_Guide_Ctrl_Ctrl_Ctrl_CtrlShape" -p "L_PelvisEnd_Guide";
	rename -uid "EC01738C-8845-FF3E-46D0-5F96A8D6FCF0";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/C:\\Users\\Esteban\\Documents\\maya\\2022\\scripts\\rigging\\Mutant_Tools\\Icons\\Guide_Data";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 6;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 9 0 no 3
		10 0 1 2 3 4 5 6 7 8 9
		10
		0.1054687499998298 5.8966734021318514e-06 -0.2109374999999471
		0.10796456249982944 5.8966734016810172e-06 0.39872714062505271
		0.2136556406248295 5.8966734012636976e-06 0.31204110937505253
		0.39620432812482953 5.8966734003587793e-06 0.41773218750005386
		1.6344686047053881e-07 5.8212421517593095e-06 0.97001803125005237
		-0.39620432812517048 5.8966734039561189e-06 0.41773260937505025
		-0.21365521875017029 5.8966734032035844e-06 0.31204110937505042
		-0.10682760937517044 3.0237721526561206e-06 0.39872714062505193
		-0.10546875000017011 5.8966734030894526e-06 -0.2109374999999481
		0.1054687499998298 5.8966734021318514e-06 -0.2109374999999471
		;
createNode dagContainer -n "L_Hip_Block" -p "Body";
	rename -uid "DE6A70AF-9542-C9A9-31B7-4C9F103444BF";
	addAttr -ci true -sn "nts" -ln "notes" -dt "string";
	setAttr ".isc" yes;
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/Limb.png";
	setAttr ".ctor" -type "string" "PC";
	setAttr ".cdat" -type "string" "2021/09/18 08:17:31";
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
		"['L_Hip_Ik_Jnt_L_Ankle_Ik_Jnt_Distance', 'R_Hip_Top_Handle_Ctrl', 'L_Ankle_Ik_Jnt_Stretchy_LocShape', 'L_Hip_Aim_Loc_1_Aim_Loc_Offset_Grp', 'L_Knee_JntBendy_NurbShape', 'R_Knee_Jnt_Bendy_BSSet', 'L_Hip_Ctrl_0_Ctrl', 'L_Knee_JntBendy_IK_Local_NurbShapeOrig', 'L_Hip_TwistStart_JntCtrl', 'skinCluster25GroupParts', 'L_Knee_BendyMid_0_Jnt_AutoBend_Grp', 'R_Hip_Ctrl_1_CtrlShape', 'L_Hip_Ik_Jnt_parentConstraint1', 'unitConversion85', 'L_Knee_Top_Handle_Ctrl_Offset_Grp_parentConstraint1', 'L_HipEnd_Bendy_Ctrl_Root_Grp', 'L_Hip_Jnt_1_Fol', 'R_Knee_Jnt_Bendy_Fol_Grp', 'R_Ankle_Ik_IKrp_Stretchy_Grp', 'R_Ankle_Ik_PoleVector_Ctrl_ClsHandle_parentConstraint1', 'R_Hip_Ik_Ctrl_Offset_Grp_parentConstraint1', 'L_Hip_Aim_Loc_1_Aim_Loc_Offset_Grp_parentConstraint1', 'L_Ankle_Ik_Jnt_Ctrl_tag', 'unitConversion79', 'L_Ankle_Fk_Ctrl_Offset_Grp', 'R_KneeMid_Bendy_Ctrl_MultDiv3', 'R_Ankle_Ik_IKrp', 'R_Ankle_Jnt', 'unitConversion107', 'R_Hip_TwistStart_JntCtrl_parentConstraint1', 'skinCluster30GroupId', 'R_Hip_Bnd_3_Bnd_scaleConstraint1', 'L_Hip_JntBendy_NurbShapeOrig', 'R_Hip_Ctrl_2_Ctrl', 'R_Knee_Bottom_Handle_Ctrl_Offset_Grp', 'R_Hip_Aim_Loc_2_Aim_Loc', 'R_Hip_BendyMid_3_Jnt_AutoBend_Grp', 'L_Hip_Jnt_0_Jnt', 'unitConversion103', 'R_Hip_Aim_Loc_1_Aim_Loc_Offset_Grp', 'L_Hip_Ribbon_Ctrl_Grp', 'L_Ankle_SubIk_CtrlShape', 'L_Ankle_TwistReader_JntCtrl_Offset_Grp_parentConstraint1', 'skinCluster17GroupId', 'R_Ankle_TwistReader_JntCtrl_Offset_Grp', 'L_Hip_Ctrl_1_Ctrl_Auto_Grp_aimConstraint1', 'skinCluster30GroupParts', 'L_Hip_JntRibbon_NurbShapeOrig', 'L_Knee_BendyMid_3_Jnt_Auto_Grp', 'L_Knee_Ctrl_2_Ctrl_Root_Grp', 'R_Hip_Ik_Jnt_R_Knee_Ik_Jnt_Distance', 'bindPose17', 'L_Knee_Bnd_3_Bnd_parentConstraint1', 'unitConversion98', 'skinCluster22', 'R_Knee_Jnt_Bendy_BS', 'L_Knee_UpVector_Loc_0_UpVector_Loc', 'curveShape4', 'L_Knee_Top_Handle_Ctrl', 'L_Hip_Ctrl_0_Ctrl_Root_Grp', 'L_Knee_Fk_Jnt_scale_Blend', 'R_Hip_Ik_Jnt_Stretchy_Loc_parentConstraint1', 'skinCluster19Set', 'skinCluster17', 'L_Hip_Twist_3_Jnt', 'L_Knee_Ctrl_0_CtrlShape', 'R_Hip_Ik_Ctrl_Offset_Grp', 'R_Knee_TwistStart_JntCtrl_parentConstraint1', 'L_Knee_Top_Handle_Ctrl_tag', 'L_Hip_Fk_Jnt_translate_Blend', 'R_Knee_Ctrl_2_Ctrl_Auto_Grp_aimConstraint1', 'R_Knee_Jnt', 'R_Hip_Jnt_2_Jnt', 'R_Hip_Ctrl_1_Ctrl', 'R_Ankle_Fk_Jnt_scale_Blend', 'R_Hip_Fk_Ctrl_Offset_Grp', 'R_KneeStart_Bendy_Ctrl', 'unitConversion100', 'R_Ankle_Fk_Ctrl_Offset_Grp', 'R_Knee_JntRibbon_NurbShape', 'unitConversion126', 'R_Hip_Bottom_Handle_CtrlShape', 'L_Hip_Ctrl_2_Ctrl', 'R_Hip_Ctrl_0_Ctrl_tag', 'R_Knee_Ik_Jnt_R_Ankle_Ik_Jnt_Distance_Shape', 'skinCluster31GroupParts', 'L_Knee_Bottom_Handle_Ctrl_Offset_Grp_parentConstraint1', 'L_Hip_Aim_Loc_1_Aim_Loc_aimConstraint1', 'L_Hip_Bnd_0_Bnd_scaleConstraint1', 'L_Knee_Ctrl_3_Ctrl_Auto_Grp', 'skinCluster27', 'L_Knee_Ctrl_0_Ctrl_Root_Grp_parentConstraint1', 'R_Knee_Ctrl_1_Ctrl_tag', 'L_Ankle_Ik_Jnt_orientConstraint1', 'skinCluster23', 'L_Ankle_Fk_Jnt', 'L_Knee_BendyMid_2_Jnt', 'R_HipStart_Bendy_Ctrl', 'L_Hip_Ctrl_1_Ctrl_Root_Grp_parentConstraint1', 'R_KneeStart_Bendy_Ctrl_tag', 'L_Hip_Ik_Jnt_L_Knee_Ik_Jnt_Distance', 'R_Hip_JntBendy_NurbFollicleShape1750', 'L_Hip_Ik_Jnt_Volume_Blend', 'unitConversion130', 'R_Knee_Ctrl_1_Ctrl', 'L_Ankle_Ik_IKrp_Condition', 'R_Knee_Jnt_1_Jnt_parentConstraint1', 'R_Knee_JntBendy_Other_Local_Nurb', 'R_Knee_JntBendy_NurbFollicle8350', 'R_Hip_Jnt_1_Jnt_parentConstraint1', 'L_Knee_Bottom_Handle_Ctrl_Offset_Grp', 'R_Hip_Ik_Jnt_Ctrl_Grp', 'R_Knee_JntBendy_NurbFollicle1750', 'unitConversion106', 'L_Knee_Ik_Jnt_Stretchy_Loc_parentConstraint1', 'L_Knee_Jnt_Effector', 'R_Knee_Ik_Jnt_Lock_Blend', 'R_Hip_Bnd_0_Bnd_parentConstraint1', 'L_Hip_Ctrl_1_Ctrl_tag', 'curveShape4Orig', 'L_Hip_Ik_CtrlShape', 'R_Knee_Aim_Loc_2_Aim_Loc_Offset_Grp_parentConstraint1', 'R_Knee_Ctrl_3_Ctrl_tag', 'L_Knee_Twist_0_Jnt', 'L_Knee_Aim_Loc_2_Aim_Loc_Offset_Grp', 'R_Knee_JntBendy_NurbFollicleShape8350', 'unitConversion114', 'R_Knee_NoRotate_JntCtrl_Offset_Grp', 'L_Knee_UpVector_Loc_0_UpVector_LocShape', 'L_Knee_Ctrl_1_Ctrl_tag', 'L_Knee_Ribbon_Rig_Grp', 'R_Knee_Bottom_Handle_Ctrl', 'R_Knee_Ctrl_0_Ctrl_Root_Grp_parentConstraint1', 'L_Knee_Top_Handle_CtrlShape', 'R_Hip_Jnt_Ribbons_Ctrl_Grp', 'R_Knee_BendyMid_3_Jnt', 'L_Hip_Ik_Ctrl_Offset_Grp_parentConstraint1', 'L_Knee_Bottom_Handle_Ctrl', 'R_Ankle_Ik_IKrp_UpLock_PV_MultDiv', 'L_Knee_NoRotate_JntCtrl', 'L_Hip_Bnd_3_Bnd_parentConstraint1', 'R_Ankle_Ik_Jnt_Effector', 'R_Knee_JntRibbon_NurbShapeOrig', 'L_Hip_Fk_Jnt_scale_Blend', 'skinCluster18Set', 'L_HipEnd_Bendy_Ctrl_Auto_Grp_pointConstraint1', 'L_Hip_Aim_Loc_3_Aim_LocShape', 'L_KneeStart_Bendy_Ctrl_Auto_Grp', 'R_Ankle_Ik_PoleVector_Ctrl', 'L_Ankle_Fk_Jnt_rotate_Blend', 'R_Ankle_Ik_IKrp_parentConstraint1', 'R_Knee_Fk_Jnt_rotate_Blend', 'L_Knee_Ik_Jnt_ClsHandle_parentConstraint1', 'R_Hip_Jnt_2_FolShape', 'L_Knee_Jnt_Fol_Grp', 'L_Hip_Fk_Ctrl_Offset_Grp_parentConstraint1', 'R_Ankle_Ik_Jnt_Stretchy_LocShape', 'L_Knee_TwistStart_JntCtrl', 'L_Ankle_Ik_IKrp_poleVectorConstraint1', 'R_Knee_Twist_1_Jnt', 'L_Knee_Fk_Jnt_rotate_Blend', 'R_Knee_TwistStart_IKspl', 'L_Ankle_Ik_Ctrl_tag', 'L_Hip_Ctrl_2_Ctrl_tag', 'R_Knee_Aim_Loc_0_Aim_Loc_Offset_Grp', 'skinCluster29', 'L_HipEnd_Bendy_Ctrl_Auto_Grp', 'L_Hip_Fk_Jnt_parentConstraint1', 'R_Knee_TwistStart_JntCtrl_CrvShapeOrig', 'R_Knee_Ik_Jnt_ClsHandle', 'L_Knee_BendyMid_1_Jnt', 'R_Hip_Ctrl_Grp', 'R_Hip_Ctrl_GrpMirror_Grp_scaleConstraint1', 'L_Hip_Fk_Ctrl_Offset_Grp', 'L_Hip_JntRibbon_Nurb', 'R_Hip_Fk_Jnt_translate_Blend', 'R_Hip_JntBendy_IK_Local_Nurb', 'R_Ankle_TwistReader_JntCtrl_decomposeMatrix', 'R_Hip_Ctrl_1_Ctrl_Root_Grp_parentConstraint1', 'R_Hip_Fk_Jnt_scale_Blend', 'L_Knee_Twist_3_Jnt', 'R_KneeMid_Bendy_Ctrl_Offset_Grp_parentConstraint1', 'R_Ankle_Ik_IKrp_DownLock_PV_MultDiv', 'L_KneeMid_Bendy_Ctrl_MultDiv1', 'L_Hip_UpVector_Loc_1_UpVector_Loc', 'L_Knee_Ctrl_0_Ctrl_tag', 'L_Knee_Ctrl_2_Ctrl_Root_Grp_parentConstraint1', 'L_Hip_Jnt_3_Jnt', 'R_KneeMid_Bendy_CtrlShape', 'R_KneeEnd_Bendy_Ctrl_Auto_Grp', 'R_Knee_Jnt_0_FolShape', 'skinCluster31GroupId', 'L_Hip_Jnt_Fol_Grp', 'L_Hip_Jnt_1_Jnt_parentConstraint1', 'R_Knee_Top_Handle_Ctrl_Offset_Grp_parentConstraint1', 'R_Knee_Top_Handle_Ctrl', 'L_Knee_JntRibbon_Nurb', 'R_Hip_Ctrl_GrpMirror_Grp', 'R_Knee_Bnd_0_Bnd_parentConstraint1', 'skinCluster25GroupId', 'R_Hip_Ik_Jnt_R_Ankle_Ik_Jnt_Distance_Shape', 'R_Hip_Fk_CtrlShape', 'L_Knee_Fk_CtrlShape', 'R_Knee_Bnd_1_Bnd', 'unitConversion119', 'L_Ankle_Ik_IKrp', 'L_Hip_Jnt_3_Jnt_parentConstraint1', 'L_Ankle_TwistEnd_JntCtrl', 'L_Knee_Aim_Loc_0_Aim_Loc_Offset_Grp_parentConstraint1', 'skinCluster19GroupParts', 'L_Hip_Twist_2_Jnt', 'L_Hip_Bnd_3_Bnd', 'R_Knee_Ik_Jnt_ClsHandleShape', 'L_Hip_Top_Handle_Ctrl_Offset_Grp_parentConstraint1', 'R_Hip_Jnt_1_Fol', 'L_Knee_Jnt_1_FolShape', 'R_Hip_Ik_Jnt_parentConstraint1', 'L_Knee_Ctrl_1_Ctrl_Root_Grp_parentConstraint1', 'L_Hip_Jnt_Bendy_BSGroupId', 'R_Knee_Aim_Loc_2_Aim_LocShape', 'L_Ankle_TwistReader_JntCtrl', 'unitConversion110', 'R_Hip_TwistStart_Grp', 'L_Knee_Ctrl_1_CtrlShape', 'R_Knee_Ctrl_0_Ctrl_tag', 'R_Ankle_TwistReader_JntCtrl_Offset_GrpR_Ankle_Jnt_Twist_Reader_Grp_Grp', 'R_Knee_Jnt_1_FolShape', 'R_Hip_Aim_Loc_3_Aim_Loc', 'R_Knee_Ctrl_1_Ctrl_Auto_Grp_parentConstraint1', 'R_Hip_Ik_CtrlShape', 'unitConversion104', 'R_Knee_Bnd_2_Bnd', 'R_Hip_Jnt_Main_Grp_parentConstraint1', 'L_Hip_Jnt_0_Jnt_parentConstraint1', 'L_Hip_Ctrl_3_CtrlShape', 'R_Knee_BendyMid_3_Jnt_Root_Grp', 'L_Knee_Ctrl_2_Ctrl_Auto_Grp', 'reverse3', 'L_Ankle_Ik_IKrp_Grp', 'L_Knee_UpVector_Loc_3_UpVector_Loc', 'R_Knee_Ctrl_3_Ctrl_Root_Grp_parentConstraint1', 'R_Knee_Aim_Loc_2_Aim_Loc_Offset_Grp', 'skinCluster17GroupParts', 'unitConversion99', 'R_Hip_Jnt_1_Jnt', 'R_Knee_JntBendy_NurbFollicleShape1750', 'R_Hip_Jnt_Bendy_BSGroupId', 'R_Knee_Ik_Jnt_Stretchy_Loc_parentConstraint1', 'R_Knee_Bottom_Handle_Ctrl_tag', 'L_Ankle_Fk_Jnt_translate_Blend', 'skinCluster22GroupParts', 'L_Knee_Jnt_2_Jnt_parentConstraint1', 'R_Knee_UpVector_Loc_3_UpVector_LocShape', 'L_Ankle_Fk_Jnt_scale_Blend', 'L_Knee_Bnd_2_Bnd_scaleConstraint1', 'R_Hip_Ctrl_2_Ctrl_Auto_Grp', 'L_Knee_Fk_Jnt_parentConstraint1', 'R_Knee_Jnt_3_Fol', 'R_Hip_Bnd_1_Bnd_scaleConstraint1', 'R_Knee_BendyMid_3_Jnt_AutoBend_Grp', 'L_Hip_JntBendy_IK_Local_Nurb', 'R_KneeMid_Bendy_Ctrl_MultDiv', 'skinCluster26', 'L_Knee_Jnt_2_Jnt', 'R_Hip_Top_Handle_Ctrl_Offset_Grp', 'R_Knee_Ik_Jnt_Volume_Blend', 'L_Knee_Jnt_Bendy_BSGroupId', 'L_KneeEnd_Bendy_Ctrl', 'R_Hip_JntBendy_NurbFollicle8350', 'R_Knee_TwistStart_JntCtrl', 'reverse4', 'R_Hip_Bnd_1_Bnd', 'R_Knee_Fk_Jnt_Ctrl_tag', 'L_Hip_JntBendy_NurbFollicleShape8350', 'R_Knee_Top_Handle_CtrlShape', 'L_Hip_Ik_Jnt', 'R_Hip_Jnt_BendyIK_Grp', 'L_KneeStart_Bendy_Ctrl_tag', 'bindPose15', 'L_Knee_Bnd_0_Bnd_scaleConstraint1', 'L_Hip_Bottom_Handle_Ctrl_Offset_Grp_parentConstraint1', 'R_Knee_Ctrl_2_CtrlShape', 'R_Ankle_Ik_Jnt_Ctrl_tag', 'L_Hip_JntBendy_NurbFollicle5050', 'L_Knee_Bnd_1_Bnd_parentConstraint1', 'R_Hip_Jnt_ForwardAim_Grp', 'R_Hip_JntBendy_Nurb', 'unitConversion80', 'skinCluster30Set', 'L_Hip_BendyMid_0_Jnt', 'bindPose24', 'unitConversion122', 'L_Ankle_Ik_IKrp_Stretchy_Grp', 'R_Hip_Aim_Loc_0_Aim_LocShape', 'L_Hip_Jnt_QTE', 'L_Knee_JntRibbon_NurbShape', 'R_Knee_Aim_Loc_3_Aim_Loc', 'unitConversion81', 'unitConversion101', 'R_Knee_Twist_0_Jnt', 'skinCluster23GroupId', 'unitConversion127', 'L_Knee_Ctrl_3_Ctrl_Auto_Grp_aimConstraint1', 'bindPose19', 'L_Ankle_Ik_PoleVector_Ctrl_ClsGroupParts', 'L_KneeEnd_Bendy_Ctrl_Root_Grp', 'R_Knee_Ctrl_0_Ctrl_Root_Grp', 'L_Knee_UpVector_Loc_2_UpVector_Loc', 'L_Hip_Aim_Loc_2_Aim_LocShape', 'R_Hip_Ctrl_3_Ctrl_Auto_Grp_aimConstraint1', 'R_Hip_Aim_Loc_3_Aim_LocShape', 'L_Ankle_Ik_Ctrl_Root_Grp', 'L_Hip_Jnt_3_Fol', 'L_Knee_Fk_Jnt_Ctrl_tag', 'L_Knee_Aim_Loc_3_Aim_Loc_Offset_Grp', 'L_Hip_TwistStart_JntCtrl_parentConstraint1', 'R_Ankle_TwistReader_JntCtrl', 'R_Hip_Ik_Jnt_R_Ankle_Ik_Jnt_Distance', 'L_Hip_TwistStart_IKspl', 'L_Hip_Ctrl_3_Ctrl_Auto_Grp_parentConstraint1', 'R_Knee_TwistEnd_JntCtrl_parentConstraint1', 'R_Knee_Jnt_ForwardAim_Grp', 'L_Knee_Ik_Jnt_ClsHandle', 'R_Ankle_Ik_PoleVector_Ctrl_ClsGroupId', 'unitConversion109', 'L_KneeMid_Bendy_Ctrl', 'R_Knee_Ctrl_0_Ctrl_Auto_Grp_parentConstraint1', 'L_Hip_Jnt_Bendy_BSSet', 'L_Hip_Aim_Loc_0_Aim_Loc', 'R_Hip_Jnt_Bendy_BSGroupParts', 'L_Knee_TwistStart_IKspl', 'unitConversion69', 'L_Hip_JntBendy_IK_Local_NurbShapeOrig', 'L_Knee_UpVector_Loc_1_UpVector_Loc', 'L_Knee_NoRotate_JntCtrl_Offset_Grp_parentConstraint1', 'R_Knee_Bnd_0_Bnd_scaleConstraint1', 'R_Knee_UpVector_Loc_2_UpVector_Loc', 'R_Hip_Aim_Loc_1_Aim_Loc_Offset_Grp_parentConstraint1', 'curveShape3', 'L_Knee_Twist_2_Jnt', 'R_Ankle_Fk_Jnt_rotate_Blend', 'R_Hip_Jnt_Effector', 'unitConversion73', 'L_Ankle_Ik_PoleVector_Ctrl_L_Knee_Ik_Jnt_Connected_Crv', 'R_Hip_Bnd_0_Bnd_scaleConstraint1', 'L_Ankle_Ik_IKrp_TotalDistance_MultDiv', 'R_Hip_BendyMid_3_Jnt', 'L_Knee_Ctrl_2_CtrlShape', 'L_Knee_JntBendy_IK_Local_Nurb', 'R_Hip_Jnt_Main_Grp_scaleConstraint1', 'R_Hip_JntRibbon_NurbShape', 'R_Knee_Aim_Loc_2_Aim_Loc', 'L_Hip_Ik_Jnt_L_Ankle_Ik_Jnt_Distance_Shape', 'R_Knee_Jnt_1_Jnt', 'L_Knee_Aim_Loc_1_Aim_Loc_Offset_Grp_parentConstraint1', 'L_Knee_Ik_Jnt_Cls', 'L_Hip_Ik_Jnt_Ctrl_Grp', 'R_Hip_Ctrl_3_Ctrl', 'L_Knee_TwistStart_JntCtrl_CrvShapeOrig', 'L_Hip_Ctrl_0_Ctrl_ForwardAim_Grp', 'skinCluster29Set', 'skinCluster30', 'skinCluster31Set', 'L_Knee_Ik_Jnt_L_Ankle_Ik_Jnt_Distance_Shape', 'skinCluster20GroupParts', 'L_Hip_Ctrl_3_Ctrl_Auto_Grp_aimConstraint1', 'R_Hip_Ctrl_2_Ctrl_tag', 'skinCluster28GroupParts', 'L_Ankle_TwistReader_JntCtrl_Offset_GrpL_Ankle_Jnt_Twist_Reader_Grp_Grp', 'L_Knee_Ik_Jnt_Lock_Blend', 'R_Knee_Fk_Jnt_parentConstraint1', 'R_KneeMid_Bendy_Ctrl_MultDiv1', 'R_Hip_UpVector_Loc_2_UpVector_Loc', 'L_Ankle_Ik_PoleVector_Ctrl', 'skinCluster24GroupId', 'L_Ankle_Fk_Ctrl', 'skinCluster19GroupId', 'R_Knee_Jnt_2_FolShape', 'L_Hip_Bottom_Handle_Ctrl_tag', 'R_Hip_TwistStart_JntCtrl_CrvShapeOrig', 'R_Hip_Flip_Grp', 'L_Ankle_Ik_IKrp_DownLock_PV_MultDiv', 'R_Knee_Bnd_0_Bnd', 'L_HipEnd_Bendy_Ctrl_Root_Grp_parentConstraint1', 'unitConversion113', 'skinCluster22Set', 'R_Knee_Bnd_2_Bnd_scaleConstraint1', 'L_HipStart_Bendy_CtrlShape', 'R_Hip_Ctrl_0_Ctrl_Root_Grp', 'L_Ankle_Fk_Jnt_parentConstraint1', 'L_KneeMid_Bendy_Ctrl_MultDiv3', 'L_HipStart_Bendy_Ctrl', 'L_Ankle_Jnt', 'R_Knee_BendyMid_2_Jnt', 'R_Ankle_Ik_Ctrl_tag', 'unitConversion116', 'R_Hip_Jnt_ForwardAim_Grp_scaleConstraint1', 'R_KneeMid_Bendy_Ctrl|R_Hip_Jnt_Switch_Loc', 'R_Ankle_Ik_IKrp_poleVectorConstraint1', 'R_Hip_Bottom_Handle_Ctrl', 'L_Hip_TwistStart_Grp_scaleConstraint1', 'L_Knee_Ctrl_1_Ctrl_Auto_Grp_aimConstraint1', 'R_Knee_JntBendy_IK_Local_NurbShape', 'R_HipEnd_Bendy_Ctrl_Auto_Grp_pointConstraint1', 'L_Ankle_Ik_PoleVector_Ctrl_ClsHandle_parentConstraint1', 'R_Knee_Ctrl_1_Ctrl_Auto_Grp_aimConstraint1', 'L_Hip_Jnt', 'R_Hip_Rig_Grp', 'L_Ankle_Ik_Jnt_Stretchy_Loc', 'L_Ankle_Ik_Jnt', 'L_Ankle_Ik_Jnt_Effector', 'L_Knee_Ctrl_2_Ctrl_ForwardAim_Grp', 'R_Knee_Fk_Ctrl_Offset_Grp', 'skinCluster27GroupId', 'R_Hip_Ik_Jnt_Lock_Blend', 'L_Hip_Ik_Jnt_NewScale_MultDiv', 'L_Knee_Bnd_1_Bnd_scaleConstraint1', 'R_Hip_BendyMid_3_Jnt_Auto_Grp', 'R_Knee_Ctrl_3_Ctrl_Auto_Grp', 'R_KneeStart_Bendy_Ctrl_Root_Grp_parentConstraint1', 'R_Hip_Ctrl_3_Ctrl_Auto_Grp', 'L_Ankle_TwistReader_JntCtrl_decomposeMatrix', 'L_Hip_Jnt_2_Jnt_parentConstraint1', 'R_Knee_Jnt_Local_Grp', 'L_Hip_JntBendy_NurbFollicleShape1750', 'R_Hip_Ik_Jnt_Stretchy_Loc', 'L_Ankle_Fk_Jnt_Ctrl_tag', 'L_Knee_Aim_Loc_0_Aim_Loc_aimConstraint1', 'R_Knee_JntBendy_NurbFollicle5050', 'L_Ankle_Ik_CtrlMain_Reverse', 'R_Hip_Jnt_UTQ', 'R_Hip_Ctrl_0_Ctrl', 'L_Hip_JntBendy_NurbShape', 'R_Hip_Ik_Jnt', 'R_Knee_JntBendy_IK_Local_NurbShapeOrig', 'L_Knee_Ctrl_1_Ctrl', 'L_Hip_Ctrl_0_Ctrl_tag', 'R_Ankle_TwistReader_JntCtrl_multMatrix', 'R_Hip_Bottom_Handle_Ctrl_tag', 'skinCluster21GroupId', 'R_Knee_JntBendy_IK_Local_Nurb', 'L_Hip_Aim_Loc_1_Aim_LocShape', 'R_Knee_UpVector_Loc_1_UpVector_LocShape', 'L_Hip_Jnt_0_Fol', 'L_Hip_Jnt_2_Fol', 'R_Hip_BendyMid_0_Jnt_Root_Grp', 'L_HipStart_Bendy_Ctrl_Auto_Grp', 'L_Hip_Ctrl_1_Ctrl_Auto_Grp_parentConstraint1', 'L_Knee_Aim_Loc_1_Aim_Loc_Offset_Grp', 'R_Hip_BendyMid_0_Jnt_AutoBend_Grp', 'R_Knee_Jnt_3_Jnt_parentConstraint1', 'R_Hip_Bottom_Handle_Ctrl_Offset_Grp_parentConstraint1', 'L_Knee_NoRotate_JntCtrl_Offset_Grp', 'L_Hip_Jnt_Bendy_BS', 'R_Hip_BendyMid_1_Jnt', 'L_Hip_JntBendy_NurbFollicle8350', 'L_Knee_Bnd_2_Bnd', 'L_Knee_Jnt_3_FolShape', 'R_Knee_Ctrl_2_Ctrl_ForwardAim_Grp', 'R_Knee_Ctrl_2_Ctrl_tag', 'R_Hip_Ctrl_0_Ctrl_Auto_Grp_aimConstraint1', 'R_Knee_Twist_3_Jnt', 'R_Hip_Ik_Ctrl_tag', 'R_Hip_Jnt_Local_Grp', 'R_Hip_Jnt_3_FolShape', 'L_Knee_JntBendy_IK_Local_NurbShape', 'L_Knee_Jnt_1_Jnt_parentConstraint1', 'L_Knee_JntBendy_NurbFollicleShape8350', 'L_KneeEnd_Bendy_Ctrl_tag', 'L_Knee_Ik_Jnt_Stretchy_Loc', 'L_Knee_TwistStart_JntCtrl_CrvShape', 'skinCluster32Set', 'unitConversion120', 'R_Hip_JntBendy_NurbFollicleShape8350', 'L_Hip_Bnd_2_Bnd_scaleConstraint1', 'L_Knee_JntBendy_NurbFollicle8350', 'R_Hip_UpVector_Loc_2_UpVector_LocShape', 'L_Knee_Jnt_2_FolShape', 'R_Knee_Ik_Jnt_ClsHandle_parentConstraint1', 'unitConversion83', 'R_Hip_Aim_Loc_2_Aim_Loc_aimConstraint1', 'L_Knee_Ctrl_0_Ctrl_Auto_Grp_parentConstraint1', 'R_Knee_Ctrl_2_Ctrl_Root_Grp', 'R_Hip_Ctrl_3_Ctrl_Root_Grp', 'R_Knee_Aim_Loc_3_Aim_Loc_Offset_Grp_parentConstraint1', 'L_Hip_BendyMid_3_Jnt_Root_Grp', 'L_Hip_Fk_Jnt_Ctrl_tag', 'L_Hip_BendyMid_3_Jnt_Auto_Grp', 'R_Hip_Bnd_3_Bnd', 'L_Ankle_SubIk_Ctrl', 'L_HipEnd_Bendy_Ctrl', 'L_Knee_Bnd_3_Bnd', 'L_Hip_Fk_Ctrl_Root_Grp', 'skinCluster21GroupParts', 'L_Knee_Aim_Loc_1_Aim_Loc_aimConstraint1', 'L_HipEnd_Bendy_CtrlShape', 'R_Knee_Jnt_3_Jnt', 'R_Hip_Bnd_2_Bnd_scaleConstraint1', 'L_Knee_Ik_Jnt_ClsGroupId', 'L_Hip_Aim_Loc_2_Aim_Loc_Offset_Grp', 'R_Knee_Bnd_3_Bnd_parentConstraint1', 'R_Hip_Top_Handle_CtrlShape', 'R_Knee_Jnt_ForwardAim_Grp_scaleConstraint1', 'R_Knee_Aim_Loc_0_Aim_Loc', 'skinCluster21Set', 'R_Hip_Aim_Loc_2_Aim_Loc_Offset_Grp', 'R_Hip_Jnt_0_FolShape', 'R_Knee_Jnt_Effector', 'bindPose16', 'R_Hip_JntBendy_NurbFollicle1750', 'L_Hip_Rig_Grp', 'L_Knee_Fk_Jnt_translate_Blend', 'L_Knee_Fk_Ctrl_Offset_Grp', 'R_Knee_Ctrl_2_Ctrl_Root_Grp_parentConstraint1', 'L_Knee_TwistStart_JntCtrl_Crv', 'R_Hip_Bnd_1_Bnd_parentConstraint1', 'R_Knee_TwistStart_JntCtrl_Crv', 'L_Knee_Bnd_0_Bnd', 'R_Hip_Fk_Ctrl', 'R_Hip_Ctrl_1_Ctrl_Auto_Grp', 'L_KneeEnd_Bendy_Ctrl_Root_Grp_parentConstraint1', 'L_Knee_Aim_Loc_2_Aim_Loc_Offset_Grp_parentConstraint1', 'skinCluster24GroupParts', 'L_Hip_Ctrl_0_Ctrl_Root_Grp_parentConstraint1', 'R_Hip_Jnt_3_Jnt_parentConstraint1', 'R_Knee_Ctrl_3_Ctrl', 'L_Knee_Jnt_Bendy_BSGroupParts', 'L_Hip_Ctrl_2_Ctrl_Auto_Grp', 'skinCluster29GroupParts', 'R_Knee_UpVector_Loc_0_UpVector_Loc', 'L_KneeMid_Bendy_Ctrl_Offset_Grp_parentConstraint1', 'L_Hip_UpVector_Loc_0_UpVector_LocShape', 'L_Hip_Ctrl_3_Ctrl_tag', 'L_Hip_Jnt_Ribbons_Ctrl_Grp', 'L_Knee_Ribbon_Ctrl_Grp', 'L_Ankle_Ik_CtrlShape', 'R_Hip_JntRibbon_NurbShapeOrig', 'R_Hip_Ik_Jnt_Volume_Blend', 'R_Knee_Jnt_0_Fol', 'L_Ankle_TwistReader_JntCtrl_multMatrix', 'L_Hip_Bnd_1_Bnd_scaleConstraint1', 'L_Knee_Aim_Loc_1_Aim_LocShape', 'bindPose18', 'R_Hip_Aim_Loc_0_Aim_Loc_aimConstraint1', 'L_Knee_Ik_Jnt_Volume_Blend', 'skinCluster20GroupId', 'R_Ankle_Ik_IKrp_Grp', 'unitConversion111', 'L_Hip_Aim_Loc_2_Aim_Loc', 'R_HipEnd_Bendy_Ctrl_Root_Grp_parentConstraint1', 'L_Knee_Ctrl_2_Ctrl_Auto_Grp_aimConstraint1', 'L_Knee_Aim_Loc_2_Aim_LocShape', 'L_Knee_Ctrl_3_CtrlShape', 'L_Hip_Fk_Ctrl', 'R_Hip_Ctrl_2_Ctrl_ForwardAim_Grp', 'L_Hip_Twist_0_Jnt', 'L_Knee_Jnt_Bendy_BS', 'L_Knee_Jnt_Ribbons_Ctrl_Grp', 'R_Hip_Twist_2_Jnt', 'R_Hip_Aim_Loc_0_Aim_Loc_Offset_Grp', 'R_Knee_Aim_Loc_0_Aim_Loc_Offset_Grp_parentConstraint1', 'L_KneeMid_Bendy_Ctrl|L_Hip_Jnt_Switch_Loc', 'R_Ankle_Ik_Jnt_PoleVector_Ctrl_tag', 'skinCluster27Set', 'R_Hip_Ctrl_3_Ctrl_Auto_Grp_parentConstraint1', 'R_Knee_Jnt_Ribbons_Ctrl_Grp', 'skinCluster23GroupParts', 'R_Hip_Top_Handle_Ctrl_Offset_Grp_parentConstraint1', 'L_Knee_Bnd_1_Bnd', 'L_Knee_Jnt_3_Fol', 'R_Ankle_SubIk_Ctrl', 'skinCluster27GroupParts', 'L_Hip_Aim_Loc_2_Aim_Loc_aimConstraint1', 'R_Knee_Jnt_2_Jnt', 'L_Hip_Ctrl_0_Ctrl_Auto_Grp_aimConstraint1', 'skinCluster23Set', 'R_HipEnd_Bendy_Ctrl_Auto_Grp', 'R_Hip_Jnt_3_Jnt', 'R_Knee_Aim_Loc_1_Aim_Loc_Offset_Grp_parentConstraint1', 'L_Knee_Bnd_0_Bnd_parentConstraint1', 'R_Knee_Ctrl_2_Ctrl', 'R_Knee_Ctrl_3_Ctrl_Root_Grp', 'unitConversion74', 'L_Hip_Jnt_2_FolShape', 'R_Knee_Aim_Loc_0_Aim_LocShape', 'R_Knee_Aim_Loc_3_Aim_Loc_Offset_Grp', 'L_Ankle_Ik_IKrp_UpLock_PV_MultDiv', 'L_Hip_Aim_Loc_1_Aim_Loc', 'L_Knee_Ctrl_2_Ctrl_tag', 'L_Knee_Ctrl_3_Ctrl_Root_Grp', 'L_Hip_Jnt_UTQ', 'R_Knee_Jnt_0_Jnt', 'L_KneeMid_Bendy_Ctrl_Offset_Grp', 'L_Knee_JntBendy_NurbFollicleShape1750', 'L_HipStart_Bendy_Ctrl_Root_Grp', 'skinCluster31', 'R_Ankle_Ik_PoleVector_Ctrl_Offset_Grp', 'L_Knee_UpVector_Loc_1_UpVector_LocShape', 'R_Hip_Ik_Jnt_R_Knee_Ik_Jnt_Distance_Shape', 'R_Hip_Ctrl_GrpMirror_Grp_parentConstraint1', 'L_Hip_Jnt_ForwardAim_Grp', 'L_Ankle_TwistEnd_JntCtrl_parentConstraint1', 'R_Hip_TwistStart_JntCtrl_Crv', 'unitConversion94', 'R_Knee_UpVector_Loc_3_UpVector_Loc', 'L_Hip_Fk_Jnt', 'R_Knee_NoRotate_JntCtrl_Offset_Grp_parentConstraint1', 'R_Knee_Ctrl_3_Ctrl_Auto_Grp_aimConstraint1', 'R_Knee_Ctrl_0_Ctrl_Auto_Grp_aimConstraint1', 'unitConversion76', 'R_Knee_Bottom_Handle_Ctrl_Offset_Grp_parentConstraint1', 'skinCluster20Set', 'R_Ankle_Ik_IKrp_Condition', 'R_Hip_Aim_Loc_0_Aim_Loc', 'L_Knee_JntBendy_NurbFollicle1750', 'L_Hip_Top_Handle_CtrlShape', 'L_Knee_BendyMid_3_Jnt_Root_Grp', 'unitConversion93', 'R_HipStart_Bendy_Ctrl_Root_Grp_parentConstraint1', 'unitConversion95', 'R_Hip_TwistStart_Grp_scaleConstraint1', 'R_Hip_Jnt_0_Jnt_parentConstraint1', 'unitConversion131', 'unitConversion82', 'unitConversion87', 'R_Hip_Jnt', 'R_Knee_Aim_Loc_0_Aim_Loc_aimConstraint1', 'R_Hip_Twist_0_Jnt', 'R_Ankle_Fk_Jnt', 'R_Hip_Jnt_QTE', 'R_Hip_Ik_Ctrl', 'R_Ankle_Ik_IKrp_TotalDistance_MultDiv', 'bindPose13', 'unitConversion108', 'L_Knee_Jnt', 'L_Knee_Ctrl_3_Ctrl', 'L_Ankle_TwistReader_JntCtrl_Offset_Grp_scaleConstraint1', 'bindPose22', 'R_Knee_Fk_Ctrl', 'unitConversion72', 'L_Hip_Jnt_Effector', 'R_Hip_TwistStart_IKspl', 'R_Ankle_Ik_PoleVector_Ctrl_ClsSet', 'L_Knee_Ik_Jnt_ClsSet', 'L_HipEnd_Bendy_Ctrl_tag', 'R_Knee_Aim_Loc_1_Aim_Loc_Offset_Grp', 'R_Knee_Ribbon_Ctrl_Grp', 'R_Knee_Aim_Loc_1_Aim_Loc', 'R_Knee_Top_Handle_Ctrl_tag', 'L_Knee_Ctrl_0_Ctrl_Root_Grp', 'L_Hip_BendyMid_2_Jnt', 'L_Hip_Ctrl_0_Ctrl_Auto_Grp', 'R_Knee_Bnd_1_Bnd_scaleConstraint1', 'R_KneeEnd_Bendy_Ctrl_Root_Grp', 'R_Hip_BendyMid_0_Jnt', 'L_Knee_Jnt_2_Fol', 'L_Hip_Bnd_2_Bnd', 'L_Hip_JntBendy_NurbFollicle1750', 'L_Hip_BendyMid_1_Jnt', 'R_Knee_Ik_Jnt_Stretchy_Loc', 'R_Hip_JntBendy_Other_Local_NurbShape', 'R_Knee_Ik_Jnt_Stretchy_LocShape', 'unitConversion132', 'R_Hip_Aim_Loc_1_Aim_Loc', 'R_Hip_JntBendy_IK_Local_NurbShapeOrig', 'R_Hip_Bnd_0_Bnd', 'L_Hip_Aim_Loc_3_Aim_Loc', 'R_Hip_BendyMid_0_Jnt_Auto_Grp', 'L_Knee_Ctrl_0_Ctrl', 'curveShape3Orig', 'R_Hip_Bnd_2_Bnd', 'R_Hip_JntBendy_IK_Local_NurbShape', 'skinCluster18GroupParts', 'L_Hip_Top_Handle_Ctrl', 'R_Hip_Ctrl_2_Ctrl_Auto_Grp_aimConstraint1', 'L_Knee_Jnt_Bendy_BSSet', 'R_Knee_UpVector_Loc_2_UpVector_LocShape', 'R_Hip_Ctrl_0_Ctrl_Auto_Grp_parentConstraint1', 'R_HipEnd_Bendy_Ctrl_tag', 'L_Hip_Ctrl_0_Ctrl_Auto_Grp_parentConstraint1', 'L_Knee_Bnd_2_Bnd_parentConstraint1', 'R_Knee_Bnd_3_Bnd', 'L_Hip_Bnd_2_Bnd_parentConstraint1', 'L_Knee_Aim_Loc_0_Aim_Loc_Offset_Grp', 'L_Hip_Ctrl_0_CtrlShape', 'unitConversion67', 'R_Knee_JntBendy_Other_Local_NurbShape', 'L_Knee_Aim_Loc_2_Aim_Loc', 'L_Knee_JntRibbon_NurbShapeOrig', 'skinCluster19', 'R_Hip_BendyMid_2_Jnt', 'R_Ankle_TwistReader_JntCtrl_Offset_Grp_scaleConstraint1', 'L_Hip_Aim_Loc_0_Aim_LocShape', 'R_Hip_Ctrl_2_Ctrl_Root_Grp_parentConstraint1', 'R_Knee_Bnd_2_Bnd_parentConstraint1', 'R_Ankle_Ik_PoleVector_Ctrl_ClsGroupParts', 'R_Ankle_SubIk_CtrlShape', 'R_Hip_Ctrl_2_CtrlShape', 'L_Knee_Ctrl_2_Ctrl_Auto_Grp_parentConstraint1', 'R_Knee_Jnt_BendyIK_Grp', 'L_Hip_BendyMid_3_Jnt_AutoBend_Grp', 'R_Hip_UpVector_Loc_0_UpVector_LocShape', 'L_Hip_Ik_Jnt_Stretchy_Loc', 'R_Hip_Aim_Loc_2_Aim_LocShape', 'R_Knee_JntBendy_Nurb', 'L_Ankle_Ik_IKrp_DownLock_PV_MultDiv1', 'L_Hip_Jnt_Bendy_Fol_Grp', 'bindPose23', 'R_Knee_Ctrl_0_Ctrl_Auto_Grp', 'unitConversion78', 'R_Hip_UpVector_Loc_1_UpVector_LocShape', 'L_Hip_Jnt_0_FolShape', 'L_KneeStart_Bendy_Ctrl_Root_Grp', 'L_Hip_BendyMid_0_Jnt_AutoBend_Grp', 'L_Knee_Aim_Loc_1_Aim_Loc', 'L_Hip_Fk_Jnt_rotate_Blend', 'L_Hip_Jnt_QTE_MultDiv', 'L_Knee_Ctrl_1_Ctrl_Auto_Grp', 'R_Knee_Fk_Jnt_scale_Blend', 'R_Hip_Jnt_QTE_MultDiv', 'L_Hip_Ctrl_1_Ctrl_ForwardAim_Grp', 'L_Hip_JntBendy_Other_Local_Nurb', 'L_Hip_Bnd_3_Bnd_scaleConstraint1', 'R_Hip_Fk_Jnt_Ctrl_tag', 'L_Knee_TwistStart_Grp_scaleConstraint1', 'L_Ankle_Ik_IKrp_NormalScale_LocShape', 'R_Hip_TwistStart_JntCtrl_CrvShape', 'bindPose21', 'unitConversion77', 'L_Knee_TwistStart_Grp', 'R_KneeEnd_Bendy_CtrlShape', 'R_Hip_Ctrl_1_Ctrl_tag', 'L_Hip_Aim_Loc_2_Aim_Loc_Offset_Grp_parentConstraint1', 'L_Ankle_SubIk_Ctrl_Offset_Grp', 'R_Ankle_Ik_Jnt_orientConstraint1', 'unitConversion124', 'L_Hip_Bnd_1_Bnd_parentConstraint1', 'L_Hip_Jnt_Main_Grp', 'R_HipStart_Bendy_CtrlShape', 'R_Knee_Jnt_0_Jnt_parentConstraint1', 'R_Knee_Ctrl_1_Ctrl_Root_Grp', 'R_Knee_Jnt_Fol_Grp', 'L_Knee_JntBendy_NurbFollicleShape5050', 'unitConversion121', 'L_Hip_JntRibbon_NurbShape', 'unitConversion102', 'R_Hip_Jnt_Bendy_BS', 'unitConversion88', 'L_Knee_Ik_Jnt_L_Ankle_Ik_Jnt_Distance', 'R_Ankle_TwistEnd_JntCtrl', 'R_Ankle_TwistReader_JntCtrl_Offset_Grp_parentConstraint1', 'L_Ankle_TwistReader_JntCtrl_Offset_Grp', 'unitConversion96', 'L_Ankle_Ik_Jnt_Stretchy_Loc_parentConstraint1', 'unitConversion117', 'skinCluster25Set', 'L_Hip_UpVector_Loc_2_UpVector_LocShape', 'R_KneeMid_Bendy_Ctrl', 'R_Knee_Bnd_3_Bnd_scaleConstraint1', 'L_Knee_Aim_Loc_3_Aim_Loc', 'R_Knee_Jnt_Bendy_BSGroupParts', 'R_Knee_BendyMid_1_Jnt', 'R_KneeMid_Bendy_Ctrl_MultDiv2', 'R_Knee_Ik_Jnt_ClsGroupId', 'skinCluster21', 'L_Knee_Jnt_0_FolShape', 'L_Knee_BendyMid_0_Jnt', 'R_Knee_Jnt_Bendy_BSGroupId', 'L_Hip_Jnt_2_Jnt', 'L_Knee_UpVector_Loc_3_UpVector_LocShape', 'L_Knee_TwistEnd_JntCtrl_parentConstraint1', 'R_Knee_Aim_Loc_1_Aim_Loc_aimConstraint1', 'L_Hip_JntBendy_IK_Local_NurbShape', 'R_Hip_JntBendy_NurbShape', 'skinCluster25', 'L_Hip_JntBendy_Nurb', 'L_Knee_Ik_Jnt_ClsHandleShape', 'L_Hip_Aim_Loc_0_Aim_Loc_Offset_Grp_parentConstraint1', 'skinCluster28Set', 'L_Knee_Ctrl_3_Ctrl_tag', 'L_Hip_Ik_Ctrl_Offset_Grp', 'R_Hip_Jnt_2_Fol', 'R_Hip_JntBendy_NurbFollicle5050', 'L_Knee_Ik_Jnt_Stretchy_LocShape', 'R_Hip_Ik_Jnt_NewScale_MultDiv', 'L_Ankle_Ik_PoleVector_CtrlShape', 'L_Hip_Ik_Jnt_Stretchy_LocShape', 'R_Hip_Ctrl_1_Ctrl_Auto_Grp_aimConstraint1', 'R_Hip_Ik_Jnt_Stretchy_LocShape', 'L_KneeStart_Bendy_CtrlShape', 'R_KneeMid_Bendy_Ctrl_Offset_Grp', 'L_Knee_Jnt_Bendy_Fol_Grp', 'R_Knee_Jnt_2_Jnt_parentConstraint1', 'R_Hip_Bnd_3_Bnd_parentConstraint1', 'R_Knee_TwistStart_Grp', 'L_Knee_BendyMid_3_Jnt', 'R_KneeStart_Bendy_Ctrl_Auto_Grp_pointConstraint1', 'unitConversion92', 'L_Hip_UpVector_Loc_3_UpVector_Loc', 'R_Ankle_Ik_IKrp_NormalScale_LocShape', 'skinCluster32GroupId', 'L_Knee_Jnt_1_Jnt', 'unitConversion97', 'R_HipStart_Bendy_Ctrl_Auto_Grp', 'L_Knee_JntBendy_NurbShapeOrig', 'L_Knee_Jnt_ForwardAim_Grp', 'L_Hip_Fk_Ctrl_Auto_Grp', 'L_Knee_Ik_Jnt_NewScale_MultDiv', 'L_Knee_Aim_Loc_2_Aim_Loc_aimConstraint1', 'R_Knee_JntBendy_NurbShape', 'skinCluster26Set', 'L_Hip_Jnt_Main_Grp_parentConstraint1', 'R_Hip_Fk_Jnt_rotate_Blend', 'L_KneeEnd_Bendy_Ctrl_Auto_Grp', 'R_Hip_Ctrl_0_Ctrl_Root_Grp_parentConstraint1', 'R_Knee_JntRibbon_Nurb', 'L_Ankle_Ik_IKrp_DownLock_PV_MultDiv2', 'R_Knee_Ctrl_0_Ctrl', 'R_Knee_BendyMid_0_Jnt_AutoBend_Grp', 'R_Hip_Ribbon_Rig_Grp', 'L_KneeMid_Bendy_CtrlShape', 'R_Knee_Ctrl_2_Ctrl_Auto_Grp', 'L_Ankle_Ik_IKrp_parentConstraint1', 'skinCluster32', 'L_Knee_Ctrl_0_Ctrl_Auto_Grp', 'R_Ankle_Fk_Ctrl', 'skinCluster22GroupId', 'R_KneeStart_Bendy_Ctrl_Auto_Grp', 'L_Hip_Ik_Jnt_Lock_Blend', 'L_Ankle_TwistReader_JntCtrl_quatToEuler', 'L_Hip_Ribbon_Rig_Grp', 'L_Knee_JntBendy_NurbFollicle5050', 'L_Hip_Ctrl_2_Ctrl_Root_Grp', 'skinCluster18GroupId', 'R_Knee_Ctrl_1_CtrlShape', 'unitConversion123', 'L_Knee_Ctrl_0_Ctrl_Auto_Grp_aimConstraint1', 'L_Ankle_Ik_PoleVector_Ctrl_Offset_Grp', 'R_Knee_Ik_Jnt', 'R_Hip_Ctrl_2_Ctrl_Root_Grp', 'R_Knee_Bnd_1_Bnd_parentConstraint1', 'R_Knee_Ctrl_1_Ctrl_Auto_Grp', 'R_Knee_BendyMid_0_Jnt_Auto_Grp', 'R_Knee_Aim_Loc_3_Aim_LocShape', 'L_Hip_Aim_Loc_3_Aim_Loc_Offset_Grp', 'L_Knee_Jnt_3_Jnt_parentConstraint1', 'R_Ankle_Ik_Jnt', 'R_KneeStart_Bendy_Ctrl_Root_Grp', 'R_Ankle_Ik_PoleVector_Ctrl_ClsHandleShape', 'R_Hip_Bottom_Handle_Ctrl_Offset_Grp', 'R_Ankle_Ik_CtrlMain_Reverse', 'R_Knee_UpVector_Loc_1_UpVector_Loc', 'R_Knee_Ribbon_Rig_Grp', 'R_Hip_Ik_Jnt_R_Ankle_Ik_Jnt_Distance_Shape_Normalize_MultDiv', 'R_Hip_Ctrl_3_Ctrl_Root_Grp_parentConstraint1', 'R_Hip_Fk_Jnt_parentConstraint1', 'R_Ankle_Ik_IKrp_NormalScale_Loc', 'L_Hip_TwistStart_JntCtrl_CrvShapeOrig', 'L_Knee_TwistEnd_JntCtrl', 'L_Knee_Jnt_1_Fol', 'R_Hip_Top_Handle_Ctrl_tag', 'L_Knee_Fk_Jnt', 'R_Ankle_Ik_PoleVector_Ctrl_Cls', 'skinCluster20', 'R_Hip_Handle_Ctrl_Grp', 'unitConversion70', 'L_Knee_Bottom_Handle_Ctrl_tag', 'L_Hip_Ctrl_3_Ctrl_Root_Grp_parentConstraint1', 'R_Hip_Fk_Ctrl_Auto_Grp', 'skinCluster24Set', 'L_Hip_Ctrl_2_Ctrl_ForwardAim_Grp', 'L_Hip_Bottom_Handle_Ctrl', 'R_Ankle_Ik_Ctrl', 'L_KneeStart_Bendy_Ctrl_Auto_Grp_pointConstraint1', 'L_Knee_BendyMid_3_Jnt_AutoBend_Grp', 'R_Ankle_Ik_Jnt_Stretchy_Loc_parentConstraint1', 'R_Ankle_TwistReader_JntCtrl_quatToEuler', 'R_Hip_Aim_Loc_3_Aim_Loc_Offset_Grp', 'L_Ankle_Ik_PoleVector_Ctrl_ClsGroupId', 'R_Knee_Ik_Jnt_Cls', 'R_Hip_Fk_Jnt', 'L_Ankle_Fk_CtrlShape', 'R_Knee_BendyMid_3_Jnt_Auto_Grp', 'R_Knee_Fk_CtrlShape', 'L_Hip_Ctrl_1_Ctrl', 'L_Hip_Bnd_0_Bnd_parentConstraint1', 'L_Hip_BendyMid_0_Jnt_Auto_Grp', 'L_Hip_Handle_Ctrl_Grp', 'R_Ankle_Ik_PoleVector_CtrlShape', 'L_Hip_JntBendy_Other_Local_NurbShape', 'skinCluster26GroupParts', 'R_Knee_UpVector_Loc_0_UpVector_LocShape', 'L_Knee_Ctrl_0_Ctrl_ForwardAim_Grp', 'R_KneeEnd_Bendy_Ctrl_tag', 'L_Hip_Jnt_1_FolShape', 'R_Knee_Ctrl_3_CtrlShape', 'R_HipEnd_Bendy_Ctrl_Root_Grp', 'L_Ankle_Ik_PoleVector_Ctrl_ClsSet', 'L_Hip_Jnt_Main_Grp_scaleConstraint1', 'R_Knee_TwistStart_JntCtrl_CrvShape', 'L_Hip_Jnt_Bendy_BSGroupParts', 'R_Hip_UpVector_Loc_1_UpVector_Loc', 'skinCluster18', 'R_Knee_JntBendy_NurbShapeOrig', 'L_Knee_Ik_Jnt', 'L_Hip_Top_Handle_Ctrl_Offset_Grp', 'unitConversion112', 'R_Hip_Jnt_Bendy_BSSet', 'R_Knee_Aim_Loc_1_Aim_LocShape', 'L_Hip_Jnt_Local_Grp', 'R_Hip_Ctrl_3_CtrlShape', 'L_HipStart_Bendy_Ctrl_Root_Grp_parentConstraint1', 'skinCluster28', 'L_KneeMid_Bendy_Ctrl_MultDiv', 'R_Hip_Aim_Loc_2_Aim_Loc_Offset_Grp_parentConstraint1', 'R_Hip_Ik_Jnt_R_Ankle_Ik_Jnt_Distance_Shape_MultDiv', 'R_Hip_Aim_Loc_1_Aim_LocShape', 'L_Knee_Aim_Loc_3_Aim_LocShape', 'R_KneeMid_Bendy_Ctrl_tag', 'L_Hip_Ctrl_2_Ctrl_Root_Grp_parentConstraint1', 'unitConversion118', 'L_Hip_Ctrl_Grp_scaleConstraint1', 'R_Hip_Ctrl_1_Ctrl_Auto_Grp_parentConstraint1', 'R_Ankle_Ik_IKrp_DownLock_PV_MultDiv2', 'L_Knee_Ctrl_1_Ctrl_ForwardAim_Grp', 'L_Hip_UpVector_Loc_1_UpVector_LocShape', 'R_Hip_Jnt_2_Jnt_parentConstraint1', 'L_Hip_Aim_Loc_0_Aim_Loc_Offset_Grp', 'L_KneeStart_Bendy_Ctrl', 'L_Hip_Ik_Ctrl_tag', 'R_Hip_Twist_1_Jnt', 'L_Ankle_Ik_Jnt_PoleVector_Ctrl_tag', 'R_Hip_Ctrl_3_Ctrl_tag', 'skinCluster26GroupId', 'L_Hip_Jnt_3_FolShape', 'L_Knee_JntBendy_Nurb', 'skinCluster32GroupParts', 'L_Hip_Bottom_Handle_Ctrl_Offset_Grp', 'R_Hip_Aim_Loc_1_Aim_Loc_aimConstraint1', 'R_Hip_Jnt_Main_Grp', 'skinCluster29GroupId', 'L_Hip_Ik_Jnt_L_Knee_Ik_Jnt_Distance_Shape', 'L_Knee_Ctrl_1_Ctrl_Root_Grp', 'L_Knee_Ctrl_2_Ctrl', 'R_Ankle_Ik_Jnt_Stretchy_Loc', 'R_Hip_Jnt_1_FolShape', 'R_Knee_Jnt_3_FolShape', 'L_Hip_UpVector_Loc_3_UpVector_LocShape', 'R_Ankle_Ik_PoleVector_Ctrl_R_Knee_Ik_Jnt_Connected_Crv', 'R_Knee_Twist_2_Jnt', 'L_Hip_JntBendy_NurbFollicleShape5050', 'unitConversion84', 'L_Knee_Jnt_0_Jnt', 'R_Knee_BendyMid_0_Jnt', 'L_Ankle_Ik_PoleVector_Ctrl_ClsHandleShape', 'L_Knee_JntBendy_Other_Local_Nurb', 'R_Knee_Top_Handle_Ctrl_Offset_Grp', 'unitConversion125', 'L_Hip_Jnt_ForwardAim_Grp_scaleConstraint1', 'L_Knee_Jnt_3_Jnt', 'L_Knee_TwistStart_JntCtrl_parentConstraint1', 'L_Knee_Ctrl_1_Ctrl_Auto_Grp_parentConstraint1', 'L_Ankle_Ik_Ctrl_Auto_Grp', 'L_Hip_BendyMid_3_Jnt', 'unitConversion91', 'R_Hip_Jnt_Fol_Grp', 'R_Hip_Ribbon_Ctrl_Grp', 'unitConversion68', 'L_Hip_Ctrl_3_Ctrl_Auto_Grp', 'L_KneeMid_Bendy_Ctrl_tag', 'R_Knee_Fk_Jnt_translate_Blend', 'R_Hip_TwistStart_JntCtrl', 'L_Knee_Aim_Loc_0_Aim_Loc', 'L_Knee_Ik_Jnt_ClsGroupParts', 'R_Hip_Ctrl_2_Ctrl_Auto_Grp_parentConstraint1', 'R_Ankle_Fk_CtrlShape', 'R_Hip_Jnt_0_Jnt', 'R_Knee_Ctrl_0_Ctrl_ForwardAim_Grp', 'L_Hip_Ctrl_3_Ctrl_ForwardAim_Grp', 'R_Ankle_TwistEnd_JntCtrl_parentConstraint1', 'R_Hip_JntBendy_NurbFollicleShape5050', 'skinCluster28GroupId', 'L_Knee_Jnt_BendyIK_Grp', 'L_KneeMid_Bendy_Ctrl_MultDiv2', 'L_Hip_Top_Handle_Ctrl_tag', 'L_Knee_Fk_Ctrl', 'L_Knee_Jnt_ForwardAim_Grp_scaleConstraint1', 'L_Ankle_Ik_PoleVector_Ctrl_Cls', 'L_Hip_Twist_1_Jnt', 'L_Ankle_Ik_IKrp_NormalScale_Loc', 'R_Hip_JntBendy_Other_Local_Nurb', 'R_Knee_Ctrl_2_Ctrl_Auto_Grp_parentConstraint1', 'L_Knee_Jnt_Local_Grp', 'R_Hip_Ctrl_1_Ctrl_ForwardAim_Grp', 'unitConversion105', 'L_KneeStart_Bendy_Ctrl_Root_Grp_parentConstraint1', 'bindPose20', 'R_Hip_JntRibbon_Nurb', 'R_Knee_NoRotate_JntCtrl', 'R_Hip_Aim_Loc_0_Aim_Loc_Offset_Grp_parentConstraint1', 'L_Hip_TwistStart_JntCtrl_CrvShape', 'R_HipStart_Bendy_Ctrl_tag', 'R_Ankle_Ik_Ctrl_Root_Grp', 'L_Hip_TwistStart_JntCtrl_Crv', 'L_Knee_Bottom_Handle_CtrlShape', 'L_Knee_Jnt_0_Jnt_parentConstraint1', 'R_Knee_Ik_Jnt_ClsSet', 'L_Knee_Bnd_3_Bnd_scaleConstraint1', 'R_Ankle_Ik_Ctrl_Auto_Grp', 'R_Ankle_Ik_IKrp_DownLock_PV_MultDiv1', 'L_KneeEnd_Bendy_CtrlShape', 'R_Hip_Ctrl_0_Ctrl_ForwardAim_Grp', 'L_Hip_Ik_Jnt_Stretchy_Loc_parentConstraint1', 'R_Hip_BendyMid_3_Jnt_Root_Grp', 'L_Hip_TwistStart_Grp', 'R_Hip_Ctrl_0_Ctrl_Auto_Grp', 'R_Knee_Ik_Jnt_NewScale_MultDiv', 'R_Hip_UpVector_Loc_0_UpVector_Loc', 'R_Knee_Jnt_2_Fol', 'unitConversion128', 'R_Hip_Jnt_3_Fol', 'L_Hip_Ctrl_2_CtrlShape', 'L_Hip_UpVector_Loc_2_UpVector_Loc', 'R_Hip_Bnd_2_Bnd_parentConstraint1', 'L_Knee_Jnt_0_Fol', 'R_HipEnd_Bendy_CtrlShape', 'L_Hip_Ctrl_1_Ctrl_Auto_Grp', 'L_Knee_JntBendy_Other_Local_NurbShape', 'R_Ankle_SubIk_Ctrl_Offset_Grp', 'R_KneeEnd_Bendy_Ctrl', 'R_Hip_Jnt_Bendy_Fol_Grp', 'R_Hip_Fk_Ctrl_Offset_Grp_parentConstraint1', 'L_Hip_Ctrl_Grp_parentConstraint1', 'R_Knee_Ctrl_3_Ctrl_ForwardAim_Grp', 'L_Knee_BendyMid_0_Jnt_Auto_Grp', 'L_Hip_Ctrl_2_Ctrl_Auto_Grp_aimConstraint1', 'unitConversion71', 'L_Knee_Ctrl_3_Ctrl_ForwardAim_Grp', 'L_Knee_BendyMid_0_Jnt_Root_Grp', 'L_Knee_Ctrl_3_Ctrl_Root_Grp_parentConstraint1', 'R_Hip_Ctrl_3_Ctrl_ForwardAim_Grp', 'unitConversion90', 'R_Knee_Ik_Jnt_R_Ankle_Ik_Jnt_Distance', 'skinCluster24', 'L_Hip_Jnt_BendyIK_Grp', 'unitConversion129', 'L_Knee_Aim_Loc_3_Aim_Loc_Offset_Grp_parentConstraint1', 'L_Hip_Fk_CtrlShape', 'L_Hip_Ik_Jnt_L_Ankle_Ik_Jnt_Distance_Shape_MultDiv', 'unitConversion86', 'R_Hip_UpVector_Loc_3_UpVector_LocShape', 'R_Hip_Jnt_0_Fol', 'R_Hip_UpVector_Loc_3_UpVector_Loc', 'L_Knee_Twist_1_Jnt', 'R_Knee_TwistStart_Grp_scaleConstraint1', 'L_Hip_Ctrl_3_Ctrl_Root_Grp', 'R_Knee_Ctrl_3_Ctrl_Auto_Grp_parentConstraint1', 'L_Hip_Ctrl_1_Ctrl_Root_Grp', 'R_Knee_JntBendy_NurbFollicleShape5050', 'R_Hip_Aim_Loc_3_Aim_Loc_Offset_Grp_parentConstraint1', 'R_Knee_Ctrl_1_Ctrl_Root_Grp_parentConstraint1', 'L_Knee_UpVector_Loc_2_UpVector_LocShape', 'L_Knee_Aim_Loc_0_Aim_LocShape', 'R_Knee_Aim_Loc_2_Aim_Loc_aimConstraint1', 'unitConversion89', 'R_Ankle_Fk_Jnt_parentConstraint1', 'L_Hip_Ctrl_Grp', 'R_HipStart_Bendy_Ctrl_Root_Grp', 'L_Hip_Ik_Ctrl', 'L_Ankle_Ik_PoleVector_Ctrl_ClsHandle', 'L_Hip_Ik_Jnt_L_Ankle_Ik_Jnt_Distance_Shape_Normalize_MultDiv', 'L_Ankle_Ik_Ctrl', 'R_Knee_Jnt_1_Fol', 'skinCluster17Set', 'R_Hip_Twist_3_Jnt', 'R_KneeStart_Bendy_CtrlShape', 'L_Hip_UpVector_Loc_0_UpVector_Loc', 'bindPose14', 'L_Hip_Jnt_1_Jnt', 'L_Hip_Ctrl_1_CtrlShape', 'R_Knee_Ik_Jnt_ClsGroupParts', 'L_Hip_Ctrl_3_Ctrl', 'L_Hip_Bnd_0_Bnd', 'unitConversion115', 'unitConversion75', 'R_HipEnd_Bendy_Ctrl', 'R_KneeEnd_Bendy_Ctrl_Root_Grp_parentConstraint1', 'R_Hip_Ctrl_0_CtrlShape', 'L_Knee_Ctrl_3_Ctrl_Auto_Grp_parentConstraint1', 'R_Hip_JntBendy_NurbShapeOrig', 'R_Ankle_Ik_CtrlShape', 'R_Knee_Bottom_Handle_CtrlShape', 'R_Knee_Fk_Jnt', 'R_Knee_TwistEnd_JntCtrl', 'R_Ankle_Ik_PoleVector_Ctrl_ClsHandle', 'R_Knee_Ctrl_0_CtrlShape', 'L_Hip_Aim_Loc_0_Aim_Loc_aimConstraint1', 'R_Hip_Fk_Ctrl_Root_Grp', 'R_Knee_BendyMid_0_Jnt_Root_Grp', 'L_Hip_Bnd_1_Bnd', 'L_Hip_Ctrl_2_Ctrl_Auto_Grp_parentConstraint1', 'R_Ankle_Fk_Jnt_Ctrl_tag', 'L_Hip_BendyMid_0_Jnt_Root_Grp', 'L_HipStart_Bendy_Ctrl_tag', 'R_Knee_Ctrl_1_Ctrl_ForwardAim_Grp', 'R_Hip_Ctrl_1_Ctrl_Root_Grp', 'L_Hip_Bottom_Handle_CtrlShape', 'L_Hip_Aim_Loc_3_Aim_Loc_Offset_Grp_parentConstraint1', 'R_Ankle_Fk_Jnt_translate_Blend', 'L_Knee_Top_Handle_Ctrl_Offset_Grp']");
createNode joint -n "L_Hip_Guide" -p "L_Hip_Block";
	rename -uid "90F31533-4746-4B11-FC0E-9C86AEAD3790";
	addAttr -ci true -sn "Helper" -ln "Helper" -min 0 -max 1 -en "Hide:Show" -at "enum";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/C:\\Users\\Esteban\\Documents\\maya\\2022\\scripts\\rigging\\Mutant_Tools\\Icons\\Guide_Data";
	setAttr ".t" -type "double3" 13.327960930058987 20.565343961705004 -32.062755802583084 ;
	setAttr ".r" -type "double3" 9.6795670708778232 -115.40939656981423 171.24151146336709 ;
	setAttr ".s" -type "double3" 1 1.0000000000000002 1 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 90 5.710593137499643 0 ;
	setAttr -cb on ".Helper" 1;
createNode nurbsCurve -n "L_Hip_Guide_CtrlShape" -p "L_Hip_Guide";
	rename -uid "E4F7525B-1B48-A389-1BA9-97B14128FCDD";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/C:\\Users\\Esteban\\Documents\\maya\\2022\\scripts\\rigging\\Mutant_Tools\\Icons\\Guide_Data";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 14;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 9 0 no 3
		10 0 1 2 3 4 5 6 7 8 9
		10
		5.8966734385269564e-06 -0.2109375 0.10546875
		5.8966734385269564e-06 0.39872714062500003 0.10796456249999997
		5.8966734385269564e-06 0.31204110937499996 0.21365564062499998
		5.8966734385269564e-06 0.41773218749999996 0.39620432812499995
		5.8212421885269557e-06 0.97001803124999997 1.6344703125e-07
		5.8966734385269564e-06 0.41773260937500006 -0.39620432812499995
		5.8966734385269564e-06 0.31204110937499996 -0.21365521875000001
		3.0237721885269566e-06 0.39872714062500003 -0.10682760937500001
		5.8966734385269564e-06 -0.2109375 -0.10546875
		5.8966734385269564e-06 -0.2109375 0.10546875
		;
createNode nurbsCurve -n "L_Hip_Guide_Ctrl_CtrlShape" -p "L_Hip_Guide";
	rename -uid "EB1D528B-9248-A4AE-6CA9-F4B354F6180E";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/C:\\Users\\Esteban\\Documents\\maya\\2022\\scripts\\rigging\\Mutant_Tools\\Icons\\Guide_Data";
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
		1.0269562977782698e-15 0.25068192187499999 0
		-1.2973110042937023e-09 0.24687365624999996 0.043530328124999997
		-2.5551988167937025e-09 0.23556403125 0.085738499999999995
		-3.7354531917937022e-09 0.21709729687499998 0.12534117187500002
		-4.8022020980437018e-09 0.19203370312500001 0.16113557812500001
		-5.7230286605437026e-09 0.16113515624999999 0.19203370312500001
		-6.4700005355437031e-09 0.12534117187500002 0.21709729687499998
		-7.0203786605437016e-09 0.085738499999999995 0.23556403125
		-7.3574145980437021e-09 0.043530328124999997 0.24687365624999996
		-7.4708989730437013e-09 0 0.25068234375000004
		-7.3574145980437021e-09 -0.043530328124999997 0.24687365624999996
		-7.0203786605437016e-09 -0.085738499999999995 0.23556403125
		-6.4700005355437031e-09 -0.12534117187500002 0.21709729687499998
		-5.7230286605437026e-09 -0.16113515624999999 0.19203370312500001
		-4.8022020980437018e-09 -0.19203370312500001 0.16113557812500001
		-3.7354531917937022e-09 -0.21709729687499998 0.12534117187500002
		-2.5551988167937025e-09 -0.23556403125 0.085738499999999995
		-1.2973110042937023e-09 -0.24687365624999996 0.043530328124999997
		1.0269562977782698e-15 -0.25068192187499999 0
		1.0269562977782698e-15 -0.24687365624999996 -0.043530328124999997
		1.0269562977782698e-15 -0.23556403125 -0.085738499999999995
		1.0269562977782698e-15 -0.21709729687499998 -0.12534117187500002
		1.0269562977782698e-15 -0.19203370312500001 -0.16113557812500001
		1.0269562977782698e-15 -0.16113515624999999 -0.19203370312500001
		1.0269562977782698e-15 -0.12534117187500002 -0.21709729687499998
		1.0269562977782698e-15 -0.085738499999999995 -0.23556445312500002
		1.0269562977782698e-15 -0.043530328124999997 -0.24687365624999996
		1.0269562977782698e-15 0 -0.25068234375000004
		1.0269562977782698e-15 0.043530328124999997 -0.24687365624999996
		1.0269562977782698e-15 0.085738499999999995 -0.23556445312500002
		1.0269562977782698e-15 0.12534117187500002 -0.21709729687499998
		1.0269562977782698e-15 0.16113515624999999 -0.19203370312500001
		1.0269562977782698e-15 0.19203370312500001 -0.16113557812500001
		1.0269562977782698e-15 0.21709729687499998 -0.12534117187500002
		1.0269562977782698e-15 0.23556403125 -0.085738499999999995
		1.0269562977782698e-15 0.24687365624999996 -0.043530328124999997
		1.0269562977782698e-15 0.25068192187499999 0
		0.043530328125001023 0.24687365624999996 0
		0.085738500000001022 0.23556403125 0
		0.12534117187500105 0.21709729687499998 0
		0.16113557812500104 0.19203370312500001 0
		0.19203370312500104 0.16113515624999999 0
		0.21709729687500101 0.12534117187500002 0
		0.23556403125000103 0.085738499999999995 0
		0.24687365625000102 0.043530328124999997 0
		0.25068192187500105 0 0
		0.24687365625000102 -0.043530328124999997 0
		0.23556403125000103 -0.085738499999999995 0
		0.21709729687500101 -0.12534117187500002 0
		0.19203370312500104 -0.16113515624999999 0
		0.16113557812500104 -0.19203370312500001 0
		0.12534117187500105 -0.21709729687499998 0
		0.085738500000001022 -0.23556403125 0
		0.043530328125001023 -0.24687365624999996 0
		1.0269562977782698e-15 -0.25068192187499999 0
		-0.04353032812499897 -0.24687365624999996 0
		-0.085738499999998968 -0.23556403125 0
		-0.12534117187499899 -0.21709729687499998 0
		-0.16113557812499898 -0.19203370312500001 0
		-0.19203370312499898 -0.16113515624999999 0
		-0.21709729687499896 -0.12534117187500002 0
		-0.23556403124999897 -0.085738499999999995 0
		-0.24687365624999896 -0.043530328124999997 0
		-0.25068234374999898 0 0
		-0.24687365624999896 0.043530328124999997 0
		-0.23556403124999897 0.085738499999999995 0
		-0.21709729687499896 0.12534117187500002 0
		-0.19203370312499898 0.16113515624999999 0
		-0.16113557812499898 0.19203370312500001 0
		-0.12534117187499899 0.21709729687499998 0
		-0.085738499999998968 0.23556403125 0
		-0.04353032812499897 0.24687365624999996 0
		1.0269562977782698e-15 0.25068192187499999 0
		-1.2973110042937023e-09 0.24687365624999996 0.043530328124999997
		-2.5551988167937025e-09 0.23556403125 0.085738499999999995
		-3.7354531917937022e-09 0.21709729687499998 0.12534117187500002
		-4.8022020980437018e-09 0.19203370312500001 0.16113557812500001
		-5.7230286605437026e-09 0.16113515624999999 0.19203370312500001
		-6.4700005355437031e-09 0.12534117187500002 0.21709729687499998
		-7.0203786605437016e-09 0.085738499999999995 0.23556403125
		-7.3574145980437021e-09 0.043530328124999997 0.24687365624999996
		-7.4708989730437013e-09 0 0.25068234375000004
		-0.077465109374998967 0 0.23841295312500005
		-0.14734743749999901 0 0.20280628125
		-0.20280628124999894 0 0.14734743750000001
		-0.23841295312499899 0 0.077465109374999994
		-0.25068234374999898 0 0
		-0.23841295312499899 0 -0.077465109374999994
		-0.20280628124999894 0 -0.14734743750000001
		-0.14734743749999901 0 -0.20280628125
		-0.077465109374998967 0 -0.23841295312500005
		1.0269562977782698e-15 0 -0.25068234375000004
		0.077465109375001021 0 -0.23841295312500005
		0.14734743750000107 0 -0.20280628125
		0.202806281250001 0 -0.14734743750000001
		0.23841295312500105 0 -0.077465109374999994
		0.25068192187500105 0 0
		0.23841295312500105 0 0.077465109374999994
		0.202806281250001 0 0.14734743750000001
		0.14734743750000107 0 0.20280628125
		0.077465109375001021 0 0.23841295312500005
		-7.4708989730437013e-09 0 0.25068234375000004
		;
createNode nurbsCurve -n "L_Hip_Guide_Ctrl_Ctrl_CtrlShape" -p "L_Hip_Guide";
	rename -uid "19195883-9045-9013-2B3E-00975037826E";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/C:\\Users\\Esteban\\Documents\\maya\\2022\\scripts\\rigging\\Mutant_Tools\\Icons\\Guide_Data";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 13;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 9 0 no 3
		10 0 1 2 3 4 5 6 7 8 9
		10
		-0.21093749999999897 -0.10546875 -5.8966734375000001e-06
		0.39872714062500109 -0.10796456249999997 -5.8966734375000001e-06
		0.31204110937500101 -0.21365564062499998 -5.8966734375000001e-06
		0.41773218750000096 -0.39620432812499995 -5.8966734375000001e-06
		0.97001803125000097 -1.6344703125e-07 -5.8212421874999994e-06
		0.41773260937500101 0.39620432812499995 -5.8966734375000001e-06
		0.31204110937500101 0.21365521875000001 -5.8966734375000001e-06
		0.39872714062500109 0.10682760937500001 -3.0237721875000003e-06
		-0.21093749999999897 0.10546875 -5.8966734375000001e-06
		-0.21093749999999897 -0.10546875 -5.8966734375000001e-06
		;
createNode nurbsCurve -n "L_Hip_Guide_Ctrl_Ctrl_Ctrl_CtrlShape" -p "L_Hip_Guide";
	rename -uid "0E149B18-A246-2C0A-ADBC-6EBAE6E0194C";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/C:\\Users\\Esteban\\Documents\\maya\\2022\\scripts\\rigging\\Mutant_Tools\\Icons\\Guide_Data";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 6;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 9 0 no 3
		10 0 1 2 3 4 5 6 7 8 9
		10
		0.10546875000000103 5.8966734375000001e-06 -0.2109375
		0.107964562500001 5.8966734375000001e-06 0.39872714062500003
		0.21365564062500103 5.8966734375000001e-06 0.31204110937499996
		0.396204328125001 5.8966734375000001e-06 0.41773218749999996
		1.634470322769563e-07 5.8212421874999994e-06 0.97001803124999997
		-0.39620432812499895 5.8966734375000001e-06 0.41773260937500006
		-0.21365521874999899 5.8966734375000001e-06 0.31204110937499996
		-0.10682760937499898 3.0237721875000003e-06 0.39872714062500003
		-0.10546874999999897 5.8966734375000001e-06 -0.2109375
		0.10546875000000103 5.8966734375000001e-06 -0.2109375
		;
createNode joint -n "L_Knee_Guide" -p "L_Hip_Guide";
	rename -uid "14190D84-3941-C285-7799-BA8B0384454A";
	addAttr -ci true -sn "Helper" -ln "Helper" -min 0 -max 1 -en "Hide:Show" -at "enum";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/C:\\Users\\Esteban\\Documents\\maya\\2022\\scripts\\rigging\\Mutant_Tools\\Icons\\Guide_Data";
	setAttr ".t" -type "double3" 9.4416811428122465 7.1054273576010019e-15 7.1054273576010019e-15 ;
	setAttr ".r" -type "double3" 0 0 34.057748766938992 ;
	setAttr ".s" -type "double3" 0.99999999999999956 0.99999999999999978 0.99999999999999967 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 1.2722218725854073e-14 4.6714396883995425e-15 0 ;
	setAttr -cb on ".Helper" 1;
createNode nurbsCurve -n "L_Knee_Guide_CtrlShape" -p "L_Knee_Guide";
	rename -uid "5392567F-8E40-16B0-849D-E6A85253DFBA";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/C:\\Users\\Esteban\\Documents\\maya\\2022\\scripts\\rigging\\Mutant_Tools\\Icons\\Guide_Data";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 14;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 9 0 no 3
		10 0 1 2 3 4 5 6 7 8 9
		10
		5.8966734375000001e-06 -0.21093750000000003 0.10546874999999986
		5.8966734375000001e-06 0.39872714062500003 0.10796456249999986
		5.8966734375000001e-06 0.31204110937499996 0.21365564062499987
		5.8966734375000001e-06 0.41773218749999996 0.39620432812499984
		5.8212421874999994e-06 0.97001803124999997 1.6344703112163046e-07
		5.8966734375000001e-06 0.41773260937500001 -0.39620432812500012
		5.8966734375000001e-06 0.31204110937499996 -0.2136552187500001
		3.0237721875000003e-06 0.39872714062500003 -0.10682760937500013
		5.8966734375000001e-06 -0.21093750000000003 -0.10546875000000014
		5.8966734375000001e-06 -0.21093750000000003 0.10546874999999986
		;
createNode nurbsCurve -n "L_Knee_Guide_Ctrl_CtrlShape" -p "L_Knee_Guide";
	rename -uid "67BFA2AE-AF4D-1955-E798-AE948D0A85B8";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/C:\\Users\\Esteban\\Documents\\maya\\2022\\scripts\\rigging\\Mutant_Tools\\Icons\\Guide_Data";
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
		0 0.25068192187499994 -1.2836953722228372e-16
		-1.2973120312500001e-09 0.24687365624999991 0.043530328124999865
		-2.5551998437500003e-09 0.23556403124999997 0.08573849999999987
		-3.73545421875e-09 0.21709729687499996 0.12534117187499988
		-4.8022031249999996e-09 0.19203370312499998 0.16113557812499987
		-5.7230296875000004e-09 0.16113515624999994 0.19203370312499987
		-6.4700015625000009e-09 0.12534117187499993 0.2170972968749999
		-7.0203796874999994e-09 0.08573849999999994 0.23556403124999986
		-7.3574156249999999e-09 0.043530328124999934 0.24687365624999985
		-7.4708999999999991e-09 -6.4184768818501002e-17 0.25068234374999987
		-7.3574156249999999e-09 -0.043530328125000059 0.24687365624999985
		-7.0203796874999994e-09 -0.085738500000000079 0.23556403124999986
		-6.4700015625000009e-09 -0.12534117187500007 0.2170972968749999
		-5.7230296875000004e-09 -0.16113515625000008 0.19203370312499987
		-4.8022031249999996e-09 -0.19203370312500004 0.16113557812499987
		-3.73545421875e-09 -0.21709729687500001 0.12534117187499988
		-2.5551998437500003e-09 -0.23556403125000003 0.08573849999999987
		-1.2973120312500001e-09 -0.24687365625000005 0.043530328124999865
		0 -0.25068192187500005 -1.2836953722228372e-16
		0 -0.24687365625000005 -0.043530328125000121
		0 -0.23556403125000003 -0.085738500000000134
		0 -0.21709729687500001 -0.12534117187500013
		0 -0.19203370312500004 -0.16113557812500012
		0 -0.16113515625000008 -0.19203370312500012
		0 -0.12534117187500007 -0.21709729687500012
		0 -0.085738500000000079 -0.23556445312500013
		0 -0.043530328125000059 -0.24687365625000013
		0 -6.4184768611141862e-17 -0.25068234375000015
		0 0.043530328124999934 -0.24687365625000013
		0 0.08573849999999994 -0.23556445312500013
		0 0.12534117187499993 -0.21709729687500012
		0 0.16113515624999994 -0.19203370312500012
		0 0.19203370312499998 -0.16113557812500012
		0 0.21709729687499996 -0.12534117187500013
		0 0.23556403124999997 -0.085738500000000134
		0 0.24687365624999991 -0.043530328125000121
		0 0.25068192187499994 -1.2836953722228372e-16
		0.043530328124999997 0.24687365624999991 -1.2836953722228372e-16
		0.085738499999999995 0.23556403124999997 -1.2836953722228372e-16
		0.12534117187500002 0.21709729687499996 -1.2836953722228372e-16
		0.16113557812500001 0.19203370312499998 -1.2836953722228372e-16
		0.19203370312500001 0.16113515624999994 -1.2836953722228372e-16
		0.21709729687499998 0.12534117187499993 -1.2836953722228372e-16
		0.23556403125 0.08573849999999994 -1.2836953722228372e-16
		0.24687365624999996 0.043530328124999941 -1.2836953722228372e-16
		0.25068192187499999 -5.7226947573069119e-17 -1.2836953722228372e-16
		0.24687365624999996 -0.043530328125000059 -1.2836953722228372e-16
		0.23556403125 -0.085738500000000051 -1.2836953722228372e-16
		0.21709729687499998 -0.12534117187500007 -1.2836953722228372e-16
		0.19203370312500001 -0.16113515625000008 -1.2836953722228372e-16
		0.16113557812500001 -0.19203370312500004 -1.2836953722228372e-16
		0.12534117187500002 -0.21709729687500001 -1.2836953722228372e-16
		0.085738499999999995 -0.23556403125000003 -1.2836953722228372e-16
		0.043530328124999997 -0.24687365625000005 -1.2836953722228372e-16
		0 -0.25068192187500005 -1.2836953722228372e-16
		-0.043530328124999997 -0.24687365625000005 -1.2836953722228372e-16
		-0.085738499999999995 -0.23556403125000003 -1.2836953722228372e-16
		-0.12534117187500002 -0.21709729687500001 -1.2836953722228372e-16
		-0.16113557812500001 -0.19203370312500004 -1.2836953722228372e-16
		-0.19203370312500001 -0.16113515625000008 -1.2836953722228372e-16
		-0.21709729687499998 -0.12534117187500007 -1.2836953722228372e-16
		-0.23556403125 -0.085738500000000079 -1.2836953722228372e-16
		-0.24687365624999996 -0.043530328125000073 -1.2836953722228372e-16
		-0.25068234375000004 -7.1142601358598064e-17 -1.2836953722228372e-16
		-0.24687365624999996 0.043530328124999934 -1.2836953722228372e-16
		-0.23556403125 0.085738499999999926 -1.2836953722228372e-16
		-0.21709729687499998 0.12534117187499993 -1.2836953722228372e-16
		-0.19203370312500001 0.16113515624999994 -1.2836953722228372e-16
		-0.16113557812500001 0.19203370312499998 -1.2836953722228372e-16
		-0.12534117187500002 0.21709729687499996 -1.2836953722228372e-16
		-0.085738499999999995 0.23556403124999997 -1.2836953722228372e-16
		-0.043530328124999997 0.24687365624999991 -1.2836953722228372e-16
		0 0.25068192187499994 -1.2836953722228372e-16
		-1.2973120312500001e-09 0.24687365624999991 0.043530328124999865
		-2.5551998437500003e-09 0.23556403124999997 0.08573849999999987
		-3.73545421875e-09 0.21709729687499996 0.12534117187499988
		-4.8022031249999996e-09 0.19203370312499998 0.16113557812499987
		-5.7230296875000004e-09 0.16113515624999994 0.19203370312499987
		-6.4700015625000009e-09 0.12534117187499993 0.2170972968749999
		-7.0203796874999994e-09 0.08573849999999994 0.23556403124999986
		-7.3574156249999999e-09 0.043530328124999934 0.24687365624999985
		-7.4708999999999991e-09 -6.4184768818501002e-17 0.25068234374999987
		-0.077465109374999994 -6.6334857311972635e-17 0.23841295312499988
		-0.14734743750000001 -6.8274481554442271e-17 0.20280628124999983
		-0.20280628125 -6.9813773685700742e-17 0.1473474374999999
		-0.23841295312500005 -7.0802057359348195e-17 0.077465109374999869
		-0.25068234375000004 -7.1142601358598064e-17 -1.2836953722228372e-16
		-0.23841295312500005 -7.0802057359348195e-17 -0.077465109375000132
		-0.20280628125 -6.9813773685700742e-17 -0.14734743750000018
		-0.14734743750000001 -6.8274481554442271e-17 -0.20280628125000011
		-0.077465109374999994 -6.6334857311972635e-17 -0.23841295312500016
		0 -6.4184768611141862e-17 -0.25068234375000015
		0.077465109374999994 -6.203467991031109e-17 -0.23841295312500016
		0.14734743750000001 -6.0095055667841454e-17 -0.20280628125000011
		0.20280628125 -5.8555763536582983e-17 -0.14734743750000018
		0.23841295312500005 -5.756747986293553e-17 -0.077465109375000132
		0.25068192187499999 -5.7226947573069119e-17 -1.2836953722228372e-16
		0.23841295312500005 -5.756747986293553e-17 0.077465109374999869
		0.20280628125 -5.8555763536582983e-17 0.1473474374999999
		0.14734743750000001 -6.0095055667841454e-17 0.20280628124999983
		0.077465109374999994 -6.203467991031109e-17 0.23841295312499988
		-7.4708999999999991e-09 -6.4184768818501002e-17 0.25068234374999987
		;
createNode nurbsCurve -n "L_Knee_Guide_Ctrl_Ctrl_CtrlShape" -p "L_Knee_Guide";
	rename -uid "6FE166F5-6641-29D6-E3A8-029FF0EB3A1E";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/C:\\Users\\Esteban\\Documents\\maya\\2022\\scripts\\rigging\\Mutant_Tools\\Icons\\Guide_Data";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 13;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 9 0 no 3
		10 0 1 2 3 4 5 6 7 8 9
		10
		-0.2109375 -0.10546875000000007 -5.8966734376283696e-06
		0.39872714062500003 -0.10796456250000004 -5.8966734376283696e-06
		0.31204110937499996 -0.21365564062500006 -5.8966734376283696e-06
		0.41773218749999996 -0.39620432812499995 -5.8966734376283696e-06
		0.97001803124999997 -1.6344703128726138e-07 -5.8212421876283689e-06
		0.41773260937500006 0.39620432812499995 -5.8966734376283696e-06
		0.31204110937499996 0.21365521874999999 -5.8966734376283696e-06
		0.39872714062500003 0.10682760937499994 -3.0237721876283699e-06
		-0.2109375 0.10546874999999993 -5.8966734376283696e-06
		-0.2109375 -0.10546875000000007 -5.8966734376283696e-06
		;
createNode nurbsCurve -n "L_Knee_Guide_Ctrl_Ctrl_Ctrl_CtrlShape" -p "L_Knee_Guide";
	rename -uid "D3B9EE17-334E-F411-F8C8-E0B006D913C9";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/C:\\Users\\Esteban\\Documents\\maya\\2022\\scripts\\rigging\\Mutant_Tools\\Icons\\Guide_Data";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 6;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 9 0 no 3
		10 0 1 2 3 4 5 6 7 8 9
		10
		0.10546875 5.8966734374387426e-06 -0.21093750000000014
		0.10796456249999997 5.8966734374388121e-06 0.39872714062499992
		0.21365564062499998 5.8966734374417462e-06 0.3120411093749999
		0.39620432812499995 5.8966734374468115e-06 0.41773218749999991
		1.6344703125e-07 5.8212421874358146e-06 0.97001803124999997
		-0.39620432812499995 5.8966734374248183e-06 0.41773260937500001
		-0.21365521875000001 5.8966734374298844e-06 0.3120411093749999
		-0.10682760937500001 3.0237721874328501e-06 0.39872714062499992
		-0.10546875 5.8966734374328879e-06 -0.21093750000000014
		0.10546875 5.8966734374387426e-06 -0.21093750000000014
		;
createNode joint -n "L_Ankle_Guide" -p "L_Knee_Guide";
	rename -uid "9049D085-CC41-2073-BE83-02A4E7B844CA";
	addAttr -ci true -sn "Helper" -ln "Helper" -min 0 -max 1 -en "Hide:Show" -at "enum";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/C:\\Users\\Esteban\\Documents\\maya\\2022\\scripts\\rigging\\Mutant_Tools\\Icons\\Guide_Data";
	setAttr ".t" -type "double3" 7.5829834871552073 4.6185277824406512e-14 -1.7763568394002505e-14 ;
	setAttr ".s" -type "double3" 1.0000000000000002 1.0000000000000002 1.0000000000000002 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" -1.5107634736951701e-14 -2.3854160110976364e-15 -3.1805546814635152e-15 ;
	setAttr -cb on ".Helper" 1;
createNode nurbsCurve -n "L_Ankle_Guide_CtrlShape" -p "L_Ankle_Guide";
	rename -uid "9BFD9E1D-CC40-EB38-FC2F-4CBD165376C7";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/C:\\Users\\Esteban\\Documents\\maya\\2022\\scripts\\rigging\\Mutant_Tools\\Icons\\Guide_Data";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 14;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 9 0 no 3
		10 0 1 2 3 4 5 6 7 8 9
		10
		5.8966734374999984e-06 -0.2109375 0.10546875000000004
		5.8966734374999984e-06 0.39872714062500003 0.10796456249999997
		5.8966734374999984e-06 0.31204110937499996 0.21365564062499995
		5.8966734374999984e-06 0.41773218749999996 0.39620432812499989
		5.8212421874999986e-06 0.97001803124999997 1.6344703129683743e-07
		5.8966734374999984e-06 0.41773260937500006 -0.39620432812499984
		5.8966734374999984e-06 0.31204110937499996 -0.21365521874999985
		3.0237721874999991e-06 0.39872714062500003 -0.10682760937499991
		5.8966734374999984e-06 -0.2109375 -0.10546874999999994
		5.8966734374999984e-06 -0.2109375 0.10546875000000004
		;
createNode nurbsCurve -n "L_Ankle_Guide_Ctrl_CtrlShape" -p "L_Ankle_Guide";
	rename -uid "BF7946AD-3F44-85E8-19EE-0E945B70BB16";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/C:\\Users\\Esteban\\Documents\\maya\\2022\\scripts\\rigging\\Mutant_Tools\\Icons\\Guide_Data";
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
		0 0.25068192187499999 4.6837533851373779e-17
		-1.2973120312499997e-09 0.24687365624999996 0.043530328125000031
		-2.555199843749999e-09 0.23556403125000003 0.085738500000000023
		-3.7354542187499983e-09 0.21709729687500001 0.12534117187500002
		-4.8022031249999979e-09 0.19203370312500001 0.16113557812500001
		-5.7230296874999979e-09 0.16113515625000002 0.19203370312500001
		-6.4700015624999984e-09 0.12534117187500005 0.21709729687499996
		-7.0203796874999986e-09 0.085738500000000023 0.23556403124999997
		-7.357415624999999e-09 0.043530328125000024 0.24687365624999993
		-7.4708999999999974e-09 3.2092384305570931e-17 0.25068234374999998
		-7.357415624999999e-09 -0.043530328124999962 0.24687365624999993
		-7.0203796874999986e-09 -0.085738499999999981 0.23556403124999997
		-6.4700015624999984e-09 -0.12534117187499999 0.21709729687499996
		-5.7230296874999979e-09 -0.16113515624999997 0.19203370312500001
		-4.8022031249999979e-09 -0.19203370312500001 0.16113557812500001
		-3.7354542187499983e-09 -0.21709729687499996 0.12534117187500002
		-2.555199843749999e-09 -0.23556403124999997 0.085738500000000023
		-1.2973120312499997e-09 -0.24687365624999996 0.043530328125000031
		0 -0.25068192187499999 4.6837533851373779e-17
		0 -0.24687365624999996 -0.043530328124999934
		0 -0.23556403124999997 -0.085738499999999912
		0 -0.21709729687499996 -0.12534117187499991
		0 -0.19203370312500001 -0.1611355781249999
		0 -0.16113515624999997 -0.19203370312499993
		0 -0.12534117187499999 -0.21709729687499985
		0 -0.085738499999999981 -0.23556445312499985
		0 -0.043530328124999962 -0.24687365624999985
		0 3.2092384305570931e-17 -0.25068234374999987
		0 0.043530328125000024 -0.24687365624999985
		0 0.085738500000000023 -0.23556445312499985
		0 0.12534117187500005 -0.21709729687499985
		0 0.16113515625000002 -0.19203370312499993
		0 0.19203370312500001 -0.1611355781249999
		0 0.21709729687500001 -0.12534117187499991
		0 0.23556403125000003 -0.085738499999999912
		0 0.24687365624999996 -0.043530328124999934
		0 0.25068192187499999 4.6837533851373779e-17
		0.043530328124999976 0.24687365624999996 4.6233429194450477e-17
		0.085738499999999968 0.23556403125000003 4.5647673141413483e-17
		0.12534117187499993 0.21709729687500001 4.5098075664509726e-17
		0.1611355781249999 0.19203370312500001 4.4601328489865519e-17
		0.19203370312499993 0.16113515625000002 4.4172530867456189e-17
		0.2170972968749999 0.12534117187500005 4.3824703631692428e-17
		0.23556403124999992 0.085738500000000023 4.3568426210532917e-17
		0.24687365624999993 0.043530328125000024 4.3411473634596964e-17
		0.25068192187499988 3.2092384305570931e-17 4.3358623332337414e-17
		0.24687365624999993 -0.043530328124999962 4.3411473634596964e-17
		0.23556403124999992 -0.085738499999999981 4.3568426210532917e-17
		0.2170972968749999 -0.12534117187499999 4.3824703631692428e-17
		0.19203370312499993 -0.16113515624999997 4.4172530867456189e-17
		0.1611355781249999 -0.19203370312500001 4.4601328489865519e-17
		0.12534117187499993 -0.21709729687499996 4.5098075664509726e-17
		0.085738499999999968 -0.23556403124999997 4.5647673141413483e-17
		0.043530328124999976 -0.24687365624999996 4.6233429194450477e-17
		0 -0.25068192187499999 4.6837533851373779e-17
		-0.043530328124999976 -0.24687365624999996 4.7441638508297069e-17
		-0.085738499999999968 -0.23556403124999997 4.8027394561334087e-17
		-0.12534117187499993 -0.21709729687499996 4.8576992038237833e-17
		-0.1611355781249999 -0.19203370312500001 4.9073739212882046e-17
		-0.19203370312499993 -0.16113515624999997 4.9502536835291376e-17
		-0.2170972968749999 -0.12534117187499999 4.9850364071055136e-17
		-0.23556403124999992 -0.085738499999999981 5.0106641492214659e-17
		-0.24687365624999993 -0.043530328124999962 5.0263594068150619e-17
		-0.25068234374999987 3.2092384305570931e-17 5.0316450225101886e-17
		-0.24687365624999993 0.043530328125000024 5.0263594068150619e-17
		-0.23556403124999992 0.085738500000000023 5.0106641492214659e-17
		-0.2170972968749999 0.12534117187500005 4.9850364071055136e-17
		-0.19203370312499993 0.16113515625000002 4.9502536835291376e-17
		-0.1611355781249999 0.19203370312500001 4.9073739212882046e-17
		-0.12534117187499993 0.21709729687500001 4.8576992038237833e-17
		-0.085738499999999968 0.23556403125000003 4.8027394561334087e-17
		-0.043530328124999976 0.24687365624999996 4.7441638508297069e-17
		0 0.25068192187499999 4.6837533851373779e-17
		-1.2973120312499997e-09 0.24687365624999996 0.043530328125000031
		-2.555199843749999e-09 0.23556403125000003 0.085738500000000023
		-3.7354542187499983e-09 0.21709729687500001 0.12534117187500002
		-4.8022031249999979e-09 0.19203370312500001 0.16113557812500001
		-5.7230296874999979e-09 0.16113515625000002 0.19203370312500001
		-6.4700015624999984e-09 0.12534117187500005 0.21709729687499996
		-7.0203796874999986e-09 0.085738500000000023 0.23556403124999997
		-7.357415624999999e-09 0.043530328125000024 0.24687365624999993
		-7.4708999999999974e-09 3.2092384305570931e-17 0.25068234374999998
		-0.07746510937499998 3.2092384305570931e-17 0.23841295312499999
		-0.14734743749999996 3.2092384305570931e-17 0.20280628125
		-0.20280628124999994 3.2092384305570931e-17 0.14734743750000001
		-0.23841295312499991 3.2092384305570931e-17 0.077465109375000049
		-0.25068234374999987 3.2092384305570931e-17 5.0316450225101886e-17
		-0.23841295312499991 3.2092384305570931e-17 -0.077465109374999924
		-0.20280628124999994 3.2092384305570931e-17 -0.1473474374999999
		-0.14734743749999996 3.2092384305570931e-17 -0.20280628124999989
		-0.07746510937499998 3.2092384305570931e-17 -0.23841295312499988
		0 3.2092384305570931e-17 -0.25068234374999987
		0.07746510937499998 3.2092384305570931e-17 -0.23841295312499988
		0.14734743749999996 3.2092384305570931e-17 -0.20280628124999989
		0.20280628124999994 3.2092384305570931e-17 -0.1473474374999999
		0.23841295312499991 3.2092384305570931e-17 -0.077465109374999952
		0.25068192187499988 3.2092384305570931e-17 4.3358623332337414e-17
		0.23841295312499991 3.2092384305570931e-17 0.077465109375000007
		0.20280628124999994 3.2092384305570931e-17 0.14734743750000001
		0.14734743749999996 3.2092384305570931e-17 0.20280628125
		0.07746510937499998 3.2092384305570931e-17 0.23841295312499999
		-7.4708999999999974e-09 3.2092384305570931e-17 0.25068234374999998
		;
createNode nurbsCurve -n "L_Ankle_Guide_Ctrl_Ctrl_CtrlShape" -p "L_Ankle_Guide";
	rename -uid "7059F22A-C641-057A-37DD-D99BACD8859C";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/C:\\Users\\Esteban\\Documents\\maya\\2022\\scripts\\rigging\\Mutant_Tools\\Icons\\Guide_Data";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 13;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 9 0 no 3
		10 0 1 2 3 4 5 6 7 8 9
		10
		-0.21093749999999992 -0.10546874999999999 -5.8966734374502335e-06
		0.39872714062499981 -0.10796456249999996 -5.8966734374586937e-06
		0.3120411093749999 -0.21365564062499998 -5.8966734374574909e-06
		0.4177321874999998 -0.39620432812499995 -5.8966734374589571e-06
		0.97001803124999952 -1.6344703121790762e-07 -5.8212421874666238e-06
		0.41773260937499979 0.39620432812499995 -5.8966734374589571e-06
		0.3120411093749999 0.21365521875000004 -5.8966734374574909e-06
		0.39872714062499981 0.10682760937500002 -3.0237721874586952e-06
		-0.21093749999999992 0.10546875000000001 -5.8966734374502335e-06
		-0.21093749999999992 -0.10546874999999999 -5.8966734374502335e-06
		;
createNode nurbsCurve -n "L_Ankle_Guide_Ctrl_Ctrl_Ctrl_CtrlShape" -p "L_Ankle_Guide";
	rename -uid "FC893989-9849-1C04-9A6C-AE8C3F9A44A3";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/C:\\Users\\Esteban\\Documents\\maya\\2022\\scripts\\rigging\\Mutant_Tools\\Icons\\Guide_Data";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 6;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 9 0 no 3
		10 0 1 2 3 4 5 6 7 8 9
		10
		0.10546874999999996 5.8966734375320924e-06 -0.21093749999999992
		0.10796456249999994 5.8966734375320924e-06 0.39872714062499998
		0.21365564062499992 5.8966734375320924e-06 0.31204110937499996
		0.39620432812499984 5.8966734375320924e-06 0.41773218749999996
		1.6344703124999992e-07 5.8212421875320918e-06 0.97001803124999952
		-0.39620432812499984 5.8966734375320924e-06 0.41773260937500001
		-0.21365521874999985 5.8966734375320924e-06 0.31204110937499996
		-0.10682760937499992 3.0237721875320927e-06 0.39872714062499998
		-0.10546874999999996 5.8966734375320924e-06 -0.21093749999999992
		0.10546874999999996 5.8966734375320924e-06 -0.21093749999999992
		;
createNode dagContainer -n "L_Foot_Block" -p "Body";
	rename -uid "077EE77E-9848-EC55-7120-4EA7C5F66427";
	addAttr -ci true -sn "nts" -ln "notes" -dt "string";
	setAttr ".isc" yes;
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/Foot.png";
	setAttr ".ctor" -type "string" "PC";
	setAttr ".cdat" -type "string" "2021/09/18 08:41:06";
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
		"['R_Foot_Toes_RFL_Grp', 'L_Foot_Ball_Jnt_scaleConstraint1', 'L_Foot_Ankle_Jnt_BallNegative_Limit_Condition', 'L_Foot_Ankle_RFL_Grp_Auto_Grp', 'R_Foot_BallFloor_RFL_Grp_Auto_Grp', 'R_Foot_Ball_RFL_Grp_Root_Grp', 'L_Foot_Toes_Jnt', 'R_Foot_Toes_Ctrl_Offset_Grp_parentConstraint1', 'R_Foot_Toes_RFL_Grp_Root_Grp', 'R_Foot_Ankle_Ik_IKsc', 'L_Foot_BallToes_Bnd', 'unitConversion164', 'unitConversion162', 'R_Foot_Toes_Ctrl', 'unitConversion133', 'L_Foot_Toes_RFL_Grp_Auto_Grp_Offset_Grp', 'R_Foot_Ball_Ik_Jnt', 'L_Foot_Ankle_RFL_Grp_Auto_Grp_Offset_Grp', 'R_Foot_Ball_Ik_Jnt_Reverse', 'L_Foot_Ankle_Bnd', 'L_Foot_In_RFL_Grp_Root_Grp', 'unitConversion157', 'unitConversion156', 'R_Foot_BallToes_Bnd_parentConstraint1', 'R_Foot_Ankle_Bnd', 'L_Foot_Ankle_Jnt_parentConstraint1', 'R_Foot_BallFloor_RFL_Grp_Root_Grp', 'L_Foot_BallFloor_RFL_Grp_Auto_Grp', 'unitConversion147', 'L_Foot_Heel_RFL_Grp_Auto_Grp_Offset_Grp', 'L_Foot_Ankle_Jnt', 'L_Foot_Toes_RFL_Grp_Auto_Grp', 'unitConversion152', 'R_Foot_Ankle_RFL_Grp_Auto_Grp', 'L_Foot_Ankle_RFL_Grp', 'L_Foot_Ankle_Jnt_Toes_Limit_Condition1', 'L_Foot_HeelMid_RFL_Grp_Root_Grp', 'unitConversion159', 'R_Foot_Ankle_Jnt', 'L_Foot_Toes_Jnt_parentConstraint1', 'R_Foot_HeelMid_RFL_Grp_Auto_Grp_Offset_Grp', 'L_Foot_BallFloor_RFL_Grp_Auto_Grp_Offset_Grp', 'L_Foot_BallToes_Jnt_parentConstraint1', 'R_Foot_Toes_Ik_Jnt_Reverse', 'R_Foot_Toes_Ik_Jnt', 'R_Foot_Ankle_Fk_Jnt', 'R_Foot_Heel_RFL_Grp_Auto_Grp', 'unitConversion163', 'R_Foot_Toes_Ctrl_Offset_Grp_scaleConstraint1', 'R_Foot_In_RFL_Grp_Auto_Grp', 'R_Foot_Ankle_Jnt_Toes_Limit_Condition', 'L_Foot_Ankle_Jnt_Toes_Limit_Condition', 'R_Foot_Ball_Ik_Jnt_Reverse1', 'L_Foot_Toes_Ctrl', 'R_Foot_Ankle_Bnd_scaleConstraint1', 'unitConversion155', 'L_Foot_Ball_RFL_Grp_Auto_Grp_Offset_Grp', 'R_Foot_In_RFL_Grp_Root_Grp', 'unitConversion149', 'R_Foot_Toes_Jnt_parentConstraint1', 'unitConversion138', 'R_Foot_BallToes_Jnt_parentConstraint1', 'L_Foot_HeelMid_RFL_Grp_Auto_Grp', 'R_Foot_Ankle_Jnt_Toes_SubstractPlusMinAv1', 'L_Foot_Ball_Jnt', 'unitConversion144', 'R_Foot_BallToes_Bnd', 'R_Foot_Ball_Fk_Jnt', 'R_Foot_Toes_CtrlShape', 'L_Foot_Out_RFL_Grp_Auto_Grp_Offset_Grp', 'R_Foot_Ankle_Ik_Jnt_Reverse1', 'R_Foot_Ankle_RFL_Grp_Root_Grp', 'L_Foot_Toes_Ctrl_Offset_Grp', 'R_Foot_Ball_RFL_Grp', 'L_Foot_Ball_Ik_Jnt_Reverse', 'R_Foot_HeelMid_RFL_Grp', 'L_Foot_Out_RFL_Grp_Auto_Grp', 'R_Foot_Out_RFL_Grp_Root_Grp', 'unitConversion165', 'L_Foot_Ball_Ik_Jnt_Reverse1', 'unitConversion154', 'R_Foot_Ankle_GrpMirror_Grp_scaleConstraint1', 'L_Foot_Ankle_Bnd_scaleConstraint1', 'L_Foot_Toes_CtrlShape', 'L_Foot_Ball_Ik_Jnt', 'L_Foot_Heel_RFL_Grp_Auto_Grp', 'L_Foot_Toes_Ik_Jnt_Reverse1', 'L_Foot_Toes_Fk_Jnt', 'R_Foot_Ankle_Jnt_Toes_Limit_Condition1', 'L_Foot_Ankle_Grp', 'L_Foot_HeelMid_RFL_Grp_Auto_Grp_Offset_Grp', 'L_Foot_Ankle_Grp_scaleConstraint1', 'R_Foot_Ball_Jnt_parentConstraint1', 'R_Foot_Ankle_Jnt_BallNegative_Limit_Condition', 'R_Foot_Ankle_Jnt_Ball_Limit_Condition_MultDiv', 'R_Foot_Ball_Jnt_scaleConstraint1', 'R_Foot_Ankle_Ik_Jnt_Reverse', 'unitConversion150', 'unitConversion151', 'R_Foot_Out_RFL_Grp_Auto_Grp_Offset_Grp', 'L_Foot_Ankle_Jnt_scaleConstraint1', 'L_Foot_BallFloor_RFL_Grp', 'L_Foot_BallFloor_RFL_Grp_Root_Grp', 'L_Foot_In_RFL_Grp', 'L_Foot_Toes_Jnt_scaleConstraint1', 'L_Foot_Ankle_Jnt_Toes_SubstractPlusMinAv', 'R_Foot_Ball_Ik_IKsc', 'effector4', 'unitConversion136', 'L_Foot_Ball_RFL_Grp_Root_Grp', 'L_Foot_Out_RFL_Grp_Root_Grp', 'unitConversion148', 'R_Foot_Ball_Jnt', 'unitConversion161', 'L_Foot_In_RFL_Grp_Auto_Grp_Offset_Grp', 'unitConversion158', 'R_Foot_Ball_RFL_Grp_Auto_Grp', 'R_Foot_Ankle_GrpMirror_Grp', 'L_Foot_Ankle_Jnt_Toes_SubstractPlusMinAv1', 'unitConversion146', 'R_Foot_Out_RFL_Grp_Root_Grp_parentConstraint1', 'L_Foot_Ankle_Ik_IKsc', 'R_Foot_Ankle_RFL_Grp_Auto_Grp_Offset_Grp', 'L_Foot_Ankle_Fk_Jnt_parentConstraint1', 'L_Foot_Ankle_Ik_Jnt_parentConstraint1', 'unitConversion166', 'L_Foot_BallToes_Jnt', 'R_Foot_Ankle_Ik_Jnt', 'L_Foot_Toes_RFL_Grp_Root_Grp', 'L_Foot_Ankle_Ik_Jnt', 'L_Foot_Ankle_Ik_Jnt_Reverse', 'unitConversion143', 'effector2', 'L_Foot_Ankle_Fk_Jnt', 'R_Foot_Out_RFL_Grp_Auto_Grp', 'L_Foot_Ankle_Ik_Jnt_Reverse1', 'R_Foot_Ankle_Jnt_Ball_Limit_Condition', 'effector1', 'unitConversion134', 'unitConversion141', 'R_Foot_Ankle_Bnd_parentConstraint1', 'L_Foot_Toes_Ctrl_Offset_Grp_parentConstraint1', 'R_Foot_Heel_RFL_Grp_Root_Grp', 'L_Foot_Heel_RFL_Grp', 'R_Foot_BallFloor_RFL_Grp', 'L_Foot_HeelMid_RFL_Grp', 'unitConversion167', 'R_Foot_Heel_RFL_Grp', 'L_Foot_Ball_RFL_Grp', 'L_Foot_Toes_Ik_Jnt_Reverse', 'L_Foot_Heel_RFL_Grp_Root_Grp', 'R_Foot_Toes_Jnt_scaleConstraint1', 'R_Foot_BallFloor_RFL_Grp_Auto_Grp_Offset_Grp', 'L_Foot_Ankle_RFL_Grp_Root_Grp', 'L_Foot_BallToes_Bnd_parentConstraint1', 'L_Foot_Ankle_Jnt_Toes_Limit_Condition2', 'R_Foot_Ankle_Jnt_Toes_Limit_Condition2', 'R_Foot_HeelMid_RFL_Grp_Auto_Grp', 'R_Foot_Out_RFL_Grp', 'unitConversion142', 'L_Foot_Toes_RFL_Grp', 'unitConversion160', 'R_Foot_Ankle_RFL_Grp', 'L_Foot_Ball_Ik_IKsc', 'L_Foot_Ankle_Bnd_parentConstraint1', 'L_Foot_Out_RFL_Grp_Root_Grp_parentConstraint1', 'L_Foot_Toes_Ik_Jnt', 'R_Foot_Toes_Fk_Jnt', 'L_Foot_Toes_Ctrl_tag', 'R_Foot_Heel_RFL_Grp_Auto_Grp_Offset_Grp', 'unitConversion153', 'R_Foot_Toes_RFL_Grp_Auto_Grp', 'R_Foot_In_RFL_Grp', 'R_Foot_In_RFL_Grp_Auto_Grp_Offset_Grp', 'R_Foot_Ankle_Jnt_scaleConstraint1', 'unitConversion145', 'R_Foot_Toes_Ctrl_Offset_Grp', 'R_Foot_Toes_RFL_Grp_Auto_Grp_Offset_Grp', 'unitConversion168', 'R_Foot_Ankle_Ik_Jnt_parentConstraint1', 'R_Foot_Ankle_Jnt_parentConstraint1', 'unitConversion139', 'R_Foot_Toes_Ctrl_tag', 'R_Foot_Ankle_Fk_Jnt_parentConstraint1', 'R_Foot_BallToes_Jnt', 'L_Foot_Ankle_Jnt_Ball_Limit_Condition_MultDiv', 'unitConversion137', 'L_Foot_Ankle_Jnt_Ball_Limit_Condition', 'R_Foot_BallToes_Bnd_scaleConstraint1', 'unitConversion135', 'effector3', 'L_Foot_Toes_Ctrl_Offset_Grp_scaleConstraint1', 'L_Foot_Ball_Jnt_parentConstraint1', 'L_Foot_Ball_RFL_Grp_Auto_Grp', 'L_Foot_BallToes_Bnd_scaleConstraint1', 'R_Foot_Toes_Jnt', 'R_Foot_Toes_Ik_Jnt_Reverse1', 'L_Foot_Out_RFL_Grp', 'R_Foot_Ankle_Jnt_Toes_SubstractPlusMinAv', 'L_Foot_Ball_Fk_Jnt', 'unitConversion140', 'R_Foot_Ankle_Grp', 'L_Foot_In_RFL_Grp_Auto_Grp', 'R_Foot_Ball_RFL_Grp_Auto_Grp_Offset_Grp', 'R_Foot_HeelMid_RFL_Grp_Root_Grp']");
createNode joint -n "L_Foot_Ankle_Guide" -p "L_Foot_Block";
	rename -uid "4AAA4884-2D48-D06E-4091-9EAB51E09BDB";
	addAttr -ci true -sn "Helper" -ln "Helper" -min 0 -max 1 -en "Hide:Show" -at "enum";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/C:\\Users\\Esteban\\Documents\\maya\\2022\\scripts\\rigging\\Mutant_Tools\\Icons\\Guide_Data";
	setAttr ".t" -type "double3" 19.439404991425199 6.6687997650545601 -37.963116888551049 ;
	setAttr ".r" -type "double3" 92.216566236606411 39.147613242691108 -88.60021634675752 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".radi" 0.5;
	setAttr -cb on ".Helper" 1;
createNode nurbsCurve -n "L_Foot_Ankle_Guide_CtrlShape" -p "L_Foot_Ankle_Guide";
	rename -uid "08CDC41B-594A-3048-E736-039BE5A5E5C0";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/C:\\Users\\Esteban\\Documents\\maya\\2022\\scripts\\rigging\\Mutant_Tools\\Icons\\Guide_Data";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 14;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 9 0 no 3
		10 0 1 2 3 4 5 6 7 8 9
		10
		5.8966734375641848e-06 -0.21093749999999997 0.10546875000000007
		5.8966734375641848e-06 0.39872714062500003 0.10796456250000004
		5.8966734375641848e-06 0.31204110937499996 0.21365564062500006
		5.8966734375641848e-06 0.41773218749999996 0.39620432812499995
		5.8212421875641842e-06 0.97001803124999997 1.6344703131418477e-07
		5.8966734375641848e-06 0.41773260937500012 -0.39620432812499995
		5.8966734375641848e-06 0.31204110937499996 -0.21365521874999999
		3.0237721875641851e-06 0.39872714062500003 -0.10682760937499994
		5.8966734375641848e-06 -0.21093749999999997 -0.10546874999999993
		5.8966734375641848e-06 -0.21093749999999997 0.10546875000000007
		;
createNode nurbsCurve -n "L_Foot_Ankle_Guide_Ctrl_CtrlShape" -p "L_Foot_Ankle_Guide";
	rename -uid "4EB303A3-3E42-6676-F7E3-8AB65B7CD6CD";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/C:\\Users\\Esteban\\Documents\\maya\\2022\\scripts\\rigging\\Mutant_Tools\\Icons\\Guide_Data";
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
		6.4184768611141862e-17 0.25068192187500005 6.4184768611141862e-17
		-1.2973119670652315e-09 0.24687365625000005 0.043530328125000059
		-2.5551997795652317e-09 0.23556403125000003 0.085738500000000079
		-3.7354541545652313e-09 0.21709729687500001 0.12534117187500007
		-4.802203060815231e-09 0.19203370312500004 0.1611355781250001
		-5.7230296233152317e-09 0.16113515625000008 0.19203370312500004
		-6.4700014983152323e-09 0.12534117187500007 0.21709729687500001
		-7.0203796233152308e-09 0.085738500000000079 0.23556403125000003
		-7.3574155608152312e-09 0.043530328125000059 0.24687365625000005
		-7.4708999358152305e-09 6.4184768611141862e-17 0.25068234375000009
		-7.3574155608152312e-09 -0.043530328124999934 0.24687365625000005
		-7.0203796233152308e-09 -0.08573849999999994 0.23556403125000003
		-6.4700014983152323e-09 -0.12534117187499993 0.21709729687500001
		-5.7230296233152317e-09 -0.16113515624999994 0.19203370312500004
		-4.802203060815231e-09 -0.19203370312499998 0.1611355781250001
		-3.7354541545652313e-09 -0.21709729687499996 0.12534117187500007
		-2.5551997795652317e-09 -0.23556403124999997 0.085738500000000079
		-1.2973119670652315e-09 -0.24687365624999991 0.043530328125000059
		6.4184768611141862e-17 -0.25068192187499994 6.4184768611141862e-17
		6.4184768611141862e-17 -0.24687365624999991 -0.043530328124999934
		6.4184768611141862e-17 -0.23556403124999997 -0.08573849999999994
		6.4184768611141862e-17 -0.21709729687499996 -0.12534117187499993
		6.4184768611141862e-17 -0.19203370312499998 -0.16113557812499993
		6.4184768611141862e-17 -0.16113515624999994 -0.19203370312499998
		6.4184768611141862e-17 -0.12534117187499993 -0.21709729687499996
		6.4184768611141862e-17 -0.08573849999999994 -0.23556445312499999
		6.4184768611141862e-17 -0.043530328124999934 -0.24687365624999991
		6.4184768611141862e-17 6.4184768611141862e-17 -0.25068234374999998
		6.4184768611141862e-17 0.043530328125000059 -0.24687365624999991
		6.4184768611141862e-17 0.085738500000000079 -0.23556445312499999
		6.4184768611141862e-17 0.12534117187500007 -0.21709729687499996
		6.4184768611141862e-17 0.16113515625000008 -0.19203370312499998
		6.4184768611141862e-17 0.19203370312500004 -0.16113557812499993
		6.4184768611141862e-17 0.21709729687500001 -0.12534117187499993
		6.4184768611141862e-17 0.23556403125000003 -0.08573849999999994
		6.4184768611141862e-17 0.24687365625000005 -0.043530328124999934
		6.4184768611141862e-17 0.25068192187500005 6.4184768611141862e-17
		0.043530328125000059 0.24687365625000005 6.4184768611141862e-17
		0.085738500000000079 0.23556403125000003 6.4184768611141862e-17
		0.12534117187500007 0.21709729687500001 6.4184768611141862e-17
		0.1611355781250001 0.19203370312500004 6.4184768611141862e-17
		0.19203370312500004 0.16113515625000008 6.4184768611141862e-17
		0.21709729687500001 0.12534117187500007 6.4184768611141862e-17
		0.23556403125000003 0.085738500000000079 6.4184768611141862e-17
		0.24687365625000005 0.043530328125000059 6.4184768611141862e-17
		0.25068192187500005 6.4184768611141862e-17 6.4184768611141862e-17
		0.24687365625000005 -0.043530328124999934 6.4184768611141862e-17
		0.23556403125000003 -0.08573849999999994 6.4184768611141862e-17
		0.21709729687500001 -0.12534117187499993 6.4184768611141862e-17
		0.19203370312500004 -0.16113515624999994 6.4184768611141862e-17
		0.1611355781250001 -0.19203370312499998 6.4184768611141862e-17
		0.12534117187500007 -0.21709729687499996 6.4184768611141862e-17
		0.085738500000000079 -0.23556403124999997 6.4184768611141862e-17
		0.043530328125000059 -0.24687365624999991 6.4184768611141862e-17
		6.4184768611141862e-17 -0.25068192187499994 6.4184768611141862e-17
		-0.043530328124999934 -0.24687365624999991 6.4184768611141862e-17
		-0.08573849999999994 -0.23556403124999997 6.4184768611141862e-17
		-0.12534117187499993 -0.21709729687499996 6.4184768611141862e-17
		-0.16113557812499993 -0.19203370312499998 6.4184768611141862e-17
		-0.19203370312499998 -0.16113515624999994 6.4184768611141862e-17
		-0.21709729687499996 -0.12534117187499993 6.4184768611141862e-17
		-0.23556403124999997 -0.08573849999999994 6.4184768611141862e-17
		-0.24687365624999991 -0.043530328124999934 6.4184768611141862e-17
		-0.25068234374999998 6.4184768611141862e-17 6.4184768611141862e-17
		-0.24687365624999991 0.043530328125000059 6.4184768611141862e-17
		-0.23556403124999997 0.085738500000000079 6.4184768611141862e-17
		-0.21709729687499996 0.12534117187500007 6.4184768611141862e-17
		-0.19203370312499998 0.16113515625000008 6.4184768611141862e-17
		-0.16113557812499993 0.19203370312500004 6.4184768611141862e-17
		-0.12534117187499993 0.21709729687500001 6.4184768611141862e-17
		-0.08573849999999994 0.23556403125000003 6.4184768611141862e-17
		-0.043530328124999934 0.24687365625000005 6.4184768611141862e-17
		6.4184768611141862e-17 0.25068192187500005 6.4184768611141862e-17
		-1.2973119670652315e-09 0.24687365625000005 0.043530328125000059
		-2.5551997795652317e-09 0.23556403125000003 0.085738500000000079
		-3.7354541545652313e-09 0.21709729687500001 0.12534117187500007
		-4.802203060815231e-09 0.19203370312500004 0.1611355781250001
		-5.7230296233152317e-09 0.16113515625000008 0.19203370312500004
		-6.4700014983152323e-09 0.12534117187500007 0.21709729687500001
		-7.0203796233152308e-09 0.085738500000000079 0.23556403125000003
		-7.3574155608152312e-09 0.043530328125000059 0.24687365625000005
		-7.4708999358152305e-09 6.4184768611141862e-17 0.25068234375000009
		-0.077465109374999938 6.4184768611141862e-17 0.2384129531250001
		-0.14734743749999998 6.4184768611141862e-17 0.20280628125000005
		-0.20280628124999991 6.4184768611141862e-17 0.14734743750000007
		-0.23841295312499997 6.4184768611141862e-17 0.077465109375000063
		-0.25068234374999998 6.4184768611141862e-17 6.4184768611141862e-17
		-0.23841295312499997 6.4184768611141862e-17 -0.077465109374999938
		-0.20280628124999991 6.4184768611141862e-17 -0.14734743749999998
		-0.14734743749999998 6.4184768611141862e-17 -0.20280628124999991
		-0.077465109374999938 6.4184768611141862e-17 -0.23841295312499997
		6.4184768611141862e-17 6.4184768611141862e-17 -0.25068234374999998
		0.077465109375000063 6.4184768611141862e-17 -0.23841295312499997
		0.14734743750000007 6.4184768611141862e-17 -0.20280628124999991
		0.20280628125000005 6.4184768611141862e-17 -0.14734743749999998
		0.2384129531250001 6.4184768611141862e-17 -0.077465109374999938
		0.25068192187500005 6.4184768611141862e-17 6.4184768611141862e-17
		0.2384129531250001 6.4184768611141862e-17 0.077465109375000063
		0.20280628125000005 6.4184768611141862e-17 0.14734743750000007
		0.14734743750000007 6.4184768611141862e-17 0.20280628125000005
		0.077465109375000063 6.4184768611141862e-17 0.2384129531250001
		-7.4708999358152305e-09 6.4184768611141862e-17 0.25068234375000009
		;
createNode nurbsCurve -n "L_Foot_Ankle_Guide_Ctrl_Ctrl_CtrlShape" -p "L_Foot_Ankle_Guide";
	rename -uid "C76D2261-BC40-342C-8A7A-E9BA8D1648F3";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/C:\\Users\\Esteban\\Documents\\maya\\2022\\scripts\\rigging\\Mutant_Tools\\Icons\\Guide_Data";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 13;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 9 0 no 3
		10 0 1 2 3 4 5 6 7 8 9
		10
		-0.21093749999999997 -0.10546874999999993 -5.8966734374358153e-06
		0.39872714062500003 -0.10796456249999992 -5.8966734374358153e-06
		0.31204110937499996 -0.21365564062499992 -5.8966734374358153e-06
		0.41773218749999996 -0.39620432812499995 -5.8966734374358153e-06
		0.97001803124999997 -1.6344703118581523e-07 -5.8212421874358146e-06
		0.41773260937500012 0.39620432812499995 -5.8966734374358153e-06
		0.31204110937499996 0.21365521875000004 -5.8966734374358153e-06
		0.39872714062500003 0.10682760937500005 -3.0237721874358156e-06
		-0.21093749999999997 0.10546875000000007 -5.8966734374358153e-06
		-0.21093749999999997 -0.10546874999999993 -5.8966734374358153e-06
		;
createNode nurbsCurve -n "L_Foot_Ankle_Guide_Ctrl_Ctrl_Ctrl_CtrlShape" -p "L_Foot_Ankle_Guide";
	rename -uid "5688155D-4B44-9350-4680-47BF16AFAB9D";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/C:\\Users\\Esteban\\Documents\\maya\\2022\\scripts\\rigging\\Mutant_Tools\\Icons\\Guide_Data";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 6;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 9 0 no 3
		10 0 1 2 3 4 5 6 7 8 9
		10
		0.10546875000000007 5.8966734375641848e-06 -0.21093749999999997
		0.10796456250000004 5.8966734375641848e-06 0.39872714062500003
		0.21365564062500006 5.8966734375641848e-06 0.31204110937499996
		0.39620432812499995 5.8966734375641848e-06 0.41773218749999996
		1.6344703131418477e-07 5.8212421875641842e-06 0.97001803124999997
		-0.39620432812499995 5.8966734375641848e-06 0.41773260937500012
		-0.21365521874999999 5.8966734375641848e-06 0.31204110937499996
		-0.10682760937499994 3.0237721875641851e-06 0.39872714062500003
		-0.10546874999999993 5.8966734375641848e-06 -0.21093749999999997
		0.10546875000000007 5.8966734375641848e-06 -0.21093749999999997
		;
createNode joint -n "L_Foot_Heel_Guide" -p "L_Foot_Ankle_Guide";
	rename -uid "15632A2C-6446-3394-0E8F-978C05A3C7BD";
	addAttr -ci true -sn "Helper" -ln "Helper" -min 0 -max 1 -en "Hide:Show" -at "enum";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/C:\\Users\\Esteban\\Documents\\maya\\2022\\scripts\\rigging\\Mutant_Tools\\Icons\\Guide_Data";
	setAttr ".t" -type "double3" 9.5567472908366966 -1.1723420181863418 0.45922549708743787 ;
	setAttr ".r" -type "double3" 0 -13.6352918004301 0 ;
	setAttr ".s" -type "double3" 0.99999999999999989 0.99999999999999978 0.99999999999999978 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 105.3541168203888 129.16861202568089 ;
	setAttr ".radi" 0.5;
	setAttr -cb on ".Helper";
createNode nurbsCurve -n "L_Foot_Heel_Guide_CtrlShape" -p "L_Foot_Heel_Guide";
	rename -uid "81569D12-D349-D3F2-07CD-AEB773CD306C";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/C:\\Users\\Esteban\\Documents\\maya\\2022\\scripts\\rigging\\Mutant_Tools\\Icons\\Guide_Data";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 14;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 9 0 no 3
		10 0 1 2 3 4 5 6 7 8 9
		10
		5.8966734374358153e-06 -0.2109375 0.10546875
		5.8966734374358153e-06 0.39872714062500003 0.10796456249999997
		5.8966734374358153e-06 0.31204110937499996 0.21365564062499998
		5.8966734374358153e-06 0.41773218749999996 0.39620432812499995
		5.8212421874358146e-06 0.97001803124999997 1.6344703125e-07
		5.8966734374358153e-06 0.41773260937500006 -0.39620432812499995
		5.8966734374358153e-06 0.31204110937499996 -0.21365521875000001
		3.0237721874358156e-06 0.39872714062500003 -0.10682760937500001
		5.8966734374358153e-06 -0.2109375 -0.10546875
		5.8966734374358153e-06 -0.2109375 0.10546875
		;
createNode nurbsCurve -n "L_Foot_Heel_Guide_Ctrl_CtrlShape" -p "L_Foot_Heel_Guide";
	rename -uid "20019E31-EB42-12F9-EC1D-7EBC87CC925E";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/C:\\Users\\Esteban\\Documents\\maya\\2022\\scripts\\rigging\\Mutant_Tools\\Icons\\Guide_Data";
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
		-6.4184768611141862e-17 0.25068192187499999 0
		-1.2973120954347687e-09 0.24687365624999996 0.043530328124999997
		-2.5551999079347689e-09 0.23556403125 0.085738499999999995
		-3.7354542829347686e-09 0.21709729687499998 0.12534117187500002
		-4.8022031891847682e-09 0.19203370312500001 0.16113557812500001
		-5.723029751684769e-09 0.16113515624999999 0.19203370312500001
		-6.4700016266847695e-09 0.12534117187500002 0.21709729687499998
		-7.020379751684768e-09 0.085738499999999995 0.23556403125
		-7.3574156891847685e-09 0.043530328124999983 0.24687365624999996
		-7.4709000641847677e-09 -1.6046192152785466e-17 0.25068234375000004
		-7.3574156891847685e-09 -0.04353032812500001 0.24687365624999996
		-7.020379751684768e-09 -0.085738499999999995 0.23556403125
		-6.4700016266847695e-09 -0.12534117187500002 0.21709729687499998
		-5.723029751684769e-09 -0.16113515624999999 0.19203370312500001
		-4.8022031891847682e-09 -0.19203370312500001 0.16113557812500001
		-3.7354542829347686e-09 -0.21709729687499998 0.12534117187500002
		-2.5551999079347689e-09 -0.23556403125 0.085738499999999995
		-1.2973120954347687e-09 -0.24687365624999996 0.043530328124999997
		-6.4184768611141862e-17 -0.25068192187499999 0
		-6.4184768611141862e-17 -0.24687365624999996 -0.043530328124999997
		-6.4184768611141862e-17 -0.23556403125 -0.085738499999999995
		-6.4184768611141862e-17 -0.21709729687499998 -0.12534117187500002
		-6.4184768611141862e-17 -0.19203370312500001 -0.16113557812500001
		-6.4184768611141862e-17 -0.16113515624999999 -0.19203370312500001
		-6.4184768611141862e-17 -0.12534117187500002 -0.21709729687499998
		-6.4184768611141862e-17 -0.085738499999999995 -0.23556445312500002
		-6.4184768611141862e-17 -0.04353032812500001 -0.24687365624999996
		-6.4184768611141862e-17 -1.6046192152785466e-17 -0.25068234375000004
		-6.4184768611141862e-17 0.043530328124999983 -0.24687365624999996
		-6.4184768611141862e-17 0.085738499999999995 -0.23556445312500002
		-6.4184768611141862e-17 0.12534117187500002 -0.21709729687499998
		-6.4184768611141862e-17 0.16113515624999999 -0.19203370312500001
		-6.4184768611141862e-17 0.19203370312500001 -0.16113557812500001
		-6.4184768611141862e-17 0.21709729687499998 -0.12534117187500002
		-6.4184768611141862e-17 0.23556403125 -0.085738499999999995
		-6.4184768611141862e-17 0.24687365624999996 -0.043530328124999997
		-6.4184768611141862e-17 0.25068192187499999 0
		0.043530328124999934 0.24687365624999996 0
		0.08573849999999994 0.23556403125 0
		0.12534117187499993 0.21709729687499998 0
		0.16113557812499993 0.19203370312500001 0
		0.19203370312499998 0.16113515624999999 0
		0.21709729687499996 0.12534117187500002 0
		0.23556403124999997 0.085738499999999995 0
		0.24687365624999991 0.043530328124999983 0
		0.25068192187499994 -1.6046192152785466e-17 0
		0.24687365624999991 -0.04353032812500001 0
		0.23556403124999997 -0.085738499999999995 0
		0.21709729687499996 -0.12534117187500002 0
		0.19203370312499998 -0.16113515624999999 0
		0.16113557812499993 -0.19203370312500001 0
		0.12534117187499993 -0.21709729687499998 0
		0.08573849999999994 -0.23556403125 0
		0.043530328124999934 -0.24687365624999996 0
		-6.4184768611141862e-17 -0.25068192187499999 0
		-0.043530328125000059 -0.24687365624999996 0
		-0.085738500000000079 -0.23556403125 0
		-0.12534117187500007 -0.21709729687499998 0
		-0.1611355781250001 -0.19203370312500001 0
		-0.19203370312500004 -0.16113515624999999 0
		-0.21709729687500001 -0.12534117187500002 0
		-0.23556403125000003 -0.085738499999999995 0
		-0.24687365625000005 -0.04353032812500001 0
		-0.25068234375000009 -1.6046192152785466e-17 0
		-0.24687365625000005 0.043530328124999983 0
		-0.23556403125000003 0.085738499999999995 0
		-0.21709729687500001 0.12534117187500002 0
		-0.19203370312500004 0.16113515624999999 0
		-0.1611355781250001 0.19203370312500001 0
		-0.12534117187500007 0.21709729687499998 0
		-0.085738500000000079 0.23556403125 0
		-0.043530328125000059 0.24687365624999996 0
		-6.4184768611141862e-17 0.25068192187499999 0
		-1.2973120954347687e-09 0.24687365624999996 0.043530328124999997
		-2.5551999079347689e-09 0.23556403125 0.085738499999999995
		-3.7354542829347686e-09 0.21709729687499998 0.12534117187500002
		-4.8022031891847682e-09 0.19203370312500001 0.16113557812500001
		-5.723029751684769e-09 0.16113515624999999 0.19203370312500001
		-6.4700016266847695e-09 0.12534117187500002 0.21709729687499998
		-7.020379751684768e-09 0.085738499999999995 0.23556403125
		-7.3574156891847685e-09 0.043530328124999983 0.24687365624999996
		-7.4709000641847677e-09 -1.6046192152785466e-17 0.25068234375000004
		-0.077465109375000063 -1.6046192152785466e-17 0.23841295312500005
		-0.14734743750000007 -1.6046192152785466e-17 0.20280628125
		-0.20280628125000005 -1.6046192152785466e-17 0.14734743750000001
		-0.2384129531250001 -1.6046192152785466e-17 0.077465109374999994
		-0.25068234375000009 -1.6046192152785466e-17 0
		-0.2384129531250001 -1.6046192152785466e-17 -0.077465109374999994
		-0.20280628125000005 -1.6046192152785466e-17 -0.14734743750000001
		-0.14734743750000007 -1.6046192152785466e-17 -0.20280628125
		-0.077465109375000063 -1.6046192152785466e-17 -0.23841295312500005
		-6.4184768611141862e-17 -1.6046192152785466e-17 -0.25068234375000004
		0.077465109374999938 -1.6046192152785466e-17 -0.23841295312500005
		0.14734743749999998 -1.6046192152785466e-17 -0.20280628125
		0.20280628124999991 -1.6046192152785466e-17 -0.14734743750000001
		0.23841295312499997 -1.6046192152785466e-17 -0.077465109374999994
		0.25068192187499994 -1.6046192152785466e-17 0
		0.23841295312499997 -1.6046192152785466e-17 0.077465109374999994
		0.20280628124999991 -1.6046192152785466e-17 0.14734743750000001
		0.14734743749999998 -1.6046192152785466e-17 0.20280628125
		0.077465109374999938 -1.6046192152785466e-17 0.23841295312500005
		-7.4709000641847677e-09 -1.6046192152785466e-17 0.25068234375000004
		;
createNode nurbsCurve -n "L_Foot_Heel_Guide_Ctrl_Ctrl_CtrlShape" -p "L_Foot_Heel_Guide";
	rename -uid "AF878B1E-F440-E4A9-BB0D-B8BFC6EB6FE5";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/C:\\Users\\Esteban\\Documents\\maya\\2022\\scripts\\rigging\\Mutant_Tools\\Icons\\Guide_Data";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 13;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 9 0 no 3
		10 0 1 2 3 4 5 6 7 8 9
		10
		-0.21093750000000003 -0.10546875 -5.8966734375000001e-06
		0.39872714062500003 -0.10796456249999997 -5.8966734375000001e-06
		0.31204110937499996 -0.21365564062499998 -5.8966734375000001e-06
		0.41773218749999996 -0.39620432812499995 -5.8966734375000001e-06
		0.97001803124999997 -1.6344703126604619e-07 -5.8212421874999994e-06
		0.41773260937500001 0.39620432812499995 -5.8966734375000001e-06
		0.31204110937499996 0.21365521875000001 -5.8966734375000001e-06
		0.39872714062500003 0.10682760937499999 -3.0237721875000003e-06
		-0.21093750000000003 0.10546875 -5.8966734375000001e-06
		-0.21093750000000003 -0.10546875 -5.8966734375000001e-06
		;
createNode nurbsCurve -n "L_Foot_Heel_Guide_Ctrl_Ctrl_Ctrl_CtrlShape" -p "L_Foot_Heel_Guide";
	rename -uid "880780E7-734F-0978-9444-DEB01BAD3D40";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/C:\\Users\\Esteban\\Documents\\maya\\2022\\scripts\\rigging\\Mutant_Tools\\Icons\\Guide_Data";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 6;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 9 0 no 3
		10 0 1 2 3 4 5 6 7 8 9
		10
		0.10546874999999993 5.8966734374839539e-06 -0.2109375
		0.10796456249999992 5.8966734374839539e-06 0.39872714062500003
		0.21365564062499992 5.8966734374839539e-06 0.31204110937499996
		0.39620432812499995 5.8966734374839539e-06 0.41773218749999996
		1.6344703118581523e-07 5.8212421874839532e-06 0.97001803124999997
		-0.39620432812499995 5.8966734374839539e-06 0.41773260937500006
		-0.21365521875000004 5.8966734374839539e-06 0.31204110937499996
		-0.10682760937500005 3.0237721874839541e-06 0.39872714062500003
		-0.10546875000000007 5.8966734374839539e-06 -0.2109375
		0.10546874999999993 5.8966734374839539e-06 -0.2109375
		;
createNode joint -n "L_Foot_Ball_Guide" -p "L_Foot_Ankle_Guide";
	rename -uid "6084FF2A-804D-2B8D-D18B-D7BE76C069AE";
	addAttr -ci true -sn "Helper" -ln "Helper" -min 0 -max 1 -en "Hide:Show" -at "enum";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/C:\\Users\\Esteban\\Documents\\maya\\2022\\scripts\\rigging\\Mutant_Tools\\Icons\\Guide_Data";
	setAttr ".t" -type "double3" 2.6116173151952298e-16 3.9110239135560425 5.2211488889737985e-14 ;
	setAttr ".r" -type "double3" 9.838877524438681 -11.846155578884249 84.565520034377101 ;
	setAttr ".s" -type "double3" 0.99999999999999989 0.99999999999999978 0.99999999999999978 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" -12.712629942175674 -8.6822168836160074 5.3802329654006602 ;
	setAttr ".radi" 0.5;
	setAttr -cb on ".Helper";
createNode nurbsCurve -n "L_Foot_Ball_Guide_CtrlShape" -p "L_Foot_Ball_Guide";
	rename -uid "DDD60313-AB4C-D25C-BCA8-229010BEA717";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/C:\\Users\\Esteban\\Documents\\maya\\2022\\scripts\\rigging\\Mutant_Tools\\Icons\\Guide_Data";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 14;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 9 0 no 3
		10 0 1 2 3 4 5 6 7 8 9
		10
		5.8966734375000001e-06 -0.2109375 0.10546875
		5.8966734375000001e-06 0.39872714062500003 0.10796456249999997
		5.8966734375000001e-06 0.31204110937499996 0.21365564062499998
		5.8966734375000001e-06 0.41773218749999996 0.39620432812499995
		5.8212421874999994e-06 0.97001803124999997 1.6344703125e-07
		5.8966734375000001e-06 0.41773260937500006 -0.39620432812499995
		5.8966734375000001e-06 0.31204110937499996 -0.21365521875000001
		3.0237721875000003e-06 0.39872714062500003 -0.10682760937500001
		5.8966734375000001e-06 -0.2109375 -0.10546875
		5.8966734375000001e-06 -0.2109375 0.10546875
		;
createNode nurbsCurve -n "L_Foot_Ball_Guide_Ctrl_CtrlShape" -p "L_Foot_Ball_Guide";
	rename -uid "212FCBDD-E24B-FDAE-6845-E5A30F5D1C28";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/C:\\Users\\Esteban\\Documents\\maya\\2022\\scripts\\rigging\\Mutant_Tools\\Icons\\Guide_Data";
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
		0 0.25068192187499999 0
		-1.2973120312500001e-09 0.24687365624999996 0.043530328124999997
		-2.5551998437500003e-09 0.23556403125 0.085738499999999995
		-3.73545421875e-09 0.21709729687499998 0.12534117187500002
		-4.8022031249999996e-09 0.19203370312500001 0.16113557812500001
		-5.7230296875000004e-09 0.16113515624999999 0.19203370312500001
		-6.4700015625000009e-09 0.12534117187500002 0.21709729687499998
		-7.0203796874999994e-09 0.085738499999999995 0.23556403125
		-7.3574156249999999e-09 0.043530328124999997 0.24687365624999996
		-7.4708999999999991e-09 0 0.25068234375000004
		-7.3574156249999999e-09 -0.043530328124999997 0.24687365624999996
		-7.0203796874999994e-09 -0.085738499999999995 0.23556403125
		-6.4700015625000009e-09 -0.12534117187500002 0.21709729687499998
		-5.7230296875000004e-09 -0.16113515624999999 0.19203370312500001
		-4.8022031249999996e-09 -0.19203370312500001 0.16113557812500001
		-3.73545421875e-09 -0.21709729687499998 0.12534117187500002
		-2.5551998437500003e-09 -0.23556403125 0.085738499999999995
		-1.2973120312500001e-09 -0.24687365624999996 0.043530328124999997
		0 -0.25068192187499999 0
		0 -0.24687365624999996 -0.043530328124999997
		0 -0.23556403125 -0.085738499999999995
		0 -0.21709729687499998 -0.12534117187500002
		0 -0.19203370312500001 -0.16113557812500001
		0 -0.16113515624999999 -0.19203370312500001
		0 -0.12534117187500002 -0.21709729687499998
		0 -0.085738499999999995 -0.23556445312500002
		0 -0.043530328124999997 -0.24687365624999996
		0 0 -0.25068234375000004
		0 0.043530328124999997 -0.24687365624999996
		0 0.085738499999999995 -0.23556445312500002
		0 0.12534117187500002 -0.21709729687499998
		0 0.16113515624999999 -0.19203370312500001
		0 0.19203370312500001 -0.16113557812500001
		0 0.21709729687499998 -0.12534117187500002
		0 0.23556403125 -0.085738499999999995
		0 0.24687365624999996 -0.043530328124999997
		0 0.25068192187499999 0
		0.043530328124999997 0.24687365624999996 0
		0.085738499999999995 0.23556403125 0
		0.12534117187500002 0.21709729687499998 0
		0.16113557812500001 0.19203370312500001 0
		0.19203370312500001 0.16113515624999999 0
		0.21709729687499998 0.12534117187500002 0
		0.23556403125 0.085738499999999995 0
		0.24687365624999996 0.043530328124999997 0
		0.25068192187499999 0 0
		0.24687365624999996 -0.043530328124999997 0
		0.23556403125 -0.085738499999999995 0
		0.21709729687499998 -0.12534117187500002 0
		0.19203370312500001 -0.16113515624999999 0
		0.16113557812500001 -0.19203370312500001 0
		0.12534117187500002 -0.21709729687499998 0
		0.085738499999999995 -0.23556403125 0
		0.043530328124999997 -0.24687365624999996 0
		0 -0.25068192187499999 0
		-0.043530328124999997 -0.24687365624999996 0
		-0.085738499999999995 -0.23556403125 0
		-0.12534117187500002 -0.21709729687499998 0
		-0.16113557812500001 -0.19203370312500001 0
		-0.19203370312500001 -0.16113515624999999 0
		-0.21709729687499998 -0.12534117187500002 0
		-0.23556403125 -0.085738499999999995 0
		-0.24687365624999996 -0.043530328124999997 0
		-0.25068234375000004 0 0
		-0.24687365624999996 0.043530328124999997 0
		-0.23556403125 0.085738499999999995 0
		-0.21709729687499998 0.12534117187500002 0
		-0.19203370312500001 0.16113515624999999 0
		-0.16113557812500001 0.19203370312500001 0
		-0.12534117187500002 0.21709729687499998 0
		-0.085738499999999995 0.23556403125 0
		-0.043530328124999997 0.24687365624999996 0
		0 0.25068192187499999 0
		-1.2973120312500001e-09 0.24687365624999996 0.043530328124999997
		-2.5551998437500003e-09 0.23556403125 0.085738499999999995
		-3.73545421875e-09 0.21709729687499998 0.12534117187500002
		-4.8022031249999996e-09 0.19203370312500001 0.16113557812500001
		-5.7230296875000004e-09 0.16113515624999999 0.19203370312500001
		-6.4700015625000009e-09 0.12534117187500002 0.21709729687499998
		-7.0203796874999994e-09 0.085738499999999995 0.23556403125
		-7.3574156249999999e-09 0.043530328124999997 0.24687365624999996
		-7.4708999999999991e-09 0 0.25068234375000004
		-0.077465109374999994 0 0.23841295312500005
		-0.14734743750000001 0 0.20280628125
		-0.20280628125 0 0.14734743750000001
		-0.23841295312500005 0 0.077465109374999994
		-0.25068234375000004 0 0
		-0.23841295312500005 0 -0.077465109374999994
		-0.20280628125 0 -0.14734743750000001
		-0.14734743750000001 0 -0.20280628125
		-0.077465109374999994 0 -0.23841295312500005
		0 0 -0.25068234375000004
		0.077465109374999994 0 -0.23841295312500005
		0.14734743750000001 0 -0.20280628125
		0.20280628125 0 -0.14734743750000001
		0.23841295312500005 0 -0.077465109374999994
		0.25068192187499999 0 0
		0.23841295312500005 0 0.077465109374999994
		0.20280628125 0 0.14734743750000001
		0.14734743750000001 0 0.20280628125
		0.077465109374999994 0 0.23841295312500005
		-7.4708999999999991e-09 0 0.25068234375000004
		;
createNode nurbsCurve -n "L_Foot_Ball_Guide_Ctrl_Ctrl_CtrlShape" -p "L_Foot_Ball_Guide";
	rename -uid "D9796B47-7741-E760-EE0C-38B6178C9550";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/C:\\Users\\Esteban\\Documents\\maya\\2022\\scripts\\rigging\\Mutant_Tools\\Icons\\Guide_Data";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 13;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 9 0 no 3
		10 0 1 2 3 4 5 6 7 8 9
		10
		-0.2109375 -0.10546875 -5.8966734375000001e-06
		0.39872714062500003 -0.10796456249999997 -5.8966734375000001e-06
		0.31204110937499996 -0.21365564062499998 -5.8966734375000001e-06
		0.41773218749999996 -0.39620432812499995 -5.8966734375000001e-06
		0.97001803124999997 -1.6344703125e-07 -5.8212421874999994e-06
		0.41773260937500006 0.39620432812499995 -5.8966734375000001e-06
		0.31204110937499996 0.21365521875000001 -5.8966734375000001e-06
		0.39872714062500003 0.10682760937500001 -3.0237721875000003e-06
		-0.2109375 0.10546875 -5.8966734375000001e-06
		-0.2109375 -0.10546875 -5.8966734375000001e-06
		;
createNode nurbsCurve -n "L_Foot_Ball_Guide_Ctrl_Ctrl_Ctrl_CtrlShape" -p "L_Foot_Ball_Guide";
	rename -uid "304E0767-7C45-7D4C-B85D-0A8BABF1480C";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/C:\\Users\\Esteban\\Documents\\maya\\2022\\scripts\\rigging\\Mutant_Tools\\Icons\\Guide_Data";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 6;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 9 0 no 3
		10 0 1 2 3 4 5 6 7 8 9
		10
		0.10546875 5.8966734375000001e-06 -0.2109375
		0.10796456249999997 5.8966734375000001e-06 0.39872714062500003
		0.21365564062499998 5.8966734375000001e-06 0.31204110937499996
		0.39620432812499995 5.8966734375000001e-06 0.41773218749999996
		1.6344703125e-07 5.8212421874999994e-06 0.97001803124999997
		-0.39620432812499995 5.8966734375000001e-06 0.41773260937500006
		-0.21365521875000001 5.8966734375000001e-06 0.31204110937499996
		-0.10682760937500001 3.0237721875000003e-06 0.39872714062500003
		-0.10546875 5.8966734375000001e-06 -0.2109375
		0.10546875 5.8966734375000001e-06 -0.2109375
		;
createNode joint -n "L_Foot_BallFloor_Guide" -p "L_Foot_Ball_Guide";
	rename -uid "4CA0ADA8-4249-A3B4-FB75-69A7671BB9C4";
	addAttr -ci true -sn "Helper" -ln "Helper" -min 0 -max 1 -en "Hide:Show" -at "enum";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/C:\\Users\\Esteban\\Documents\\maya\\2022\\scripts\\rigging\\Mutant_Tools\\Icons\\Guide_Data";
	setAttr ".t" -type "double3" 2.5066709100701545 -3.3733849835077421 0.16544788182691578 ;
	setAttr ".r" -type "double3" 89.99999999999892 -76.36470819957033 179.98380019727588 ;
	setAttr ".s" -type "double3" 1 1.0000000000000002 1.0000000000000002 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0.0044482148263466905 15.354116191544758 39.18541143706797 ;
	setAttr ".radi" 0.5;
	setAttr -cb on ".Helper";
createNode nurbsCurve -n "L_Foot_BallFloor_Guide_CtrlShape" -p "L_Foot_BallFloor_Guide";
	rename -uid "C580254C-EE4A-046A-B347-A796ADF9887A";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/C:\\Users\\Esteban\\Documents\\maya\\2022\\scripts\\rigging\\Mutant_Tools\\Icons\\Guide_Data";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 14;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 9 0 no 3
		10 0 1 2 3 4 5 6 7 8 9
		10
		5.8966734375000001e-06 -0.21093750000000014 0.10546875000000001
		5.8966734375000001e-06 0.39872714062499992 0.10796456249999999
		5.8966734375000001e-06 0.3120411093749999 0.21365564062499998
		5.8966734375000001e-06 0.41773218749999991 0.39620432812499995
		5.8212421874999994e-06 0.97001803124999997 1.6344703128209239e-07
		5.8966734375000001e-06 0.41773260937500001 -0.39620432812499995
		5.8966734375000001e-06 0.3120411093749999 -0.21365521874999999
		3.0237721875000003e-06 0.39872714062499992 -0.10682760937499999
		5.8966734375000001e-06 -0.21093750000000014 -0.10546874999999999
		5.8966734375000001e-06 -0.21093750000000014 0.10546875000000001
		;
createNode nurbsCurve -n "L_Foot_BallFloor_Guide_Ctrl_CtrlShape" -p "L_Foot_BallFloor_Guide";
	rename -uid "1A2DCD81-9945-F568-3F37-0889EC73023F";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/C:\\Users\\Esteban\\Documents\\maya\\2022\\scripts\\rigging\\Mutant_Tools\\Icons\\Guide_Data";
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
		0 0.25068192187499988 3.2092384305570931e-17
		-1.2973120312500001e-09 0.24687365624999985 0.043530328125000024
		-2.5551998437500003e-09 0.23556403124999986 0.085738500000000023
		-3.73545421875e-09 0.2170972968749999 0.12534117187500005
		-4.8022031249999996e-09 0.19203370312499987 0.16113557812500001
		-5.7230296875000004e-09 0.16113515624999988 0.19203370312500001
		-6.4700015625000009e-09 0.12534117187499988 0.21709729687500001
		-7.0203796874999994e-09 0.08573849999999987 0.23556403125000003
		-7.3574156249999999e-09 0.043530328124999865 0.24687365624999996
		-7.4708999999999991e-09 -1.2836953722228372e-16 0.25068234375000004
		-7.3574156249999999e-09 -0.043530328125000121 0.24687365624999996
		-7.0203796874999994e-09 -0.085738500000000134 0.23556403125000003
		-6.4700015625000009e-09 -0.12534117187500013 0.21709729687500001
		-5.7230296875000004e-09 -0.16113515625000013 0.19203370312500001
		-4.8022031249999996e-09 -0.19203370312500012 0.16113557812500001
		-3.73545421875e-09 -0.21709729687500012 0.12534117187500005
		-2.5551998437500003e-09 -0.23556403125000014 0.085738500000000023
		-1.2973120312500001e-09 -0.24687365625000013 0.043530328125000024
		0 -0.25068192187500016 3.2092384305570931e-17
		0 -0.24687365625000013 -0.043530328124999962
		0 -0.23556403125000014 -0.085738499999999981
		0 -0.21709729687500012 -0.12534117187499999
		0 -0.19203370312500012 -0.16113557812500001
		0 -0.16113515625000013 -0.19203370312500001
		0 -0.12534117187500013 -0.21709729687499996
		0 -0.085738500000000134 -0.23556445312500002
		0 -0.043530328125000121 -0.24687365624999996
		0 -1.2836953722228372e-16 -0.25068234375000004
		0 0.043530328124999865 -0.24687365624999996
		0 0.08573849999999987 -0.23556445312500002
		0 0.12534117187499988 -0.21709729687499996
		0 0.16113515624999988 -0.19203370312500001
		0 0.19203370312499987 -0.16113557812500001
		0 0.2170972968749999 -0.12534117187499999
		0 0.23556403124999986 -0.085738499999999981
		0 0.24687365624999985 -0.043530328124999962
		0 0.25068192187499988 3.2092384305570931e-17
		0.043530328124999997 0.24687365624999985 3.2092384305570931e-17
		0.085738499999999995 0.23556403124999986 3.2092384305570931e-17
		0.12534117187500002 0.2170972968749999 3.2092384305570931e-17
		0.16113557812500001 0.19203370312499987 3.2092384305570931e-17
		0.19203370312500001 0.16113515624999988 3.2092384305570931e-17
		0.21709729687499998 0.12534117187499988 3.2092384305570931e-17
		0.23556403125 0.08573849999999987 3.2092384305570931e-17
		0.24687365624999996 0.043530328124999865 3.2092384305570931e-17
		0.25068192187499999 -1.2836953722228372e-16 3.2092384305570931e-17
		0.24687365624999996 -0.043530328125000121 3.2092384305570931e-17
		0.23556403125 -0.085738500000000134 3.2092384305570931e-17
		0.21709729687499998 -0.12534117187500013 3.2092384305570931e-17
		0.19203370312500001 -0.16113515625000013 3.2092384305570931e-17
		0.16113557812500001 -0.19203370312500012 3.2092384305570931e-17
		0.12534117187500002 -0.21709729687500012 3.2092384305570931e-17
		0.085738499999999995 -0.23556403125000014 3.2092384305570931e-17
		0.043530328124999997 -0.24687365625000013 3.2092384305570931e-17
		0 -0.25068192187500016 3.2092384305570931e-17
		-0.043530328124999997 -0.24687365625000013 3.2092384305570931e-17
		-0.085738499999999995 -0.23556403125000014 3.2092384305570931e-17
		-0.12534117187500002 -0.21709729687500012 3.2092384305570931e-17
		-0.16113557812500001 -0.19203370312500012 3.2092384305570931e-17
		-0.19203370312500001 -0.16113515625000013 3.2092384305570931e-17
		-0.21709729687499998 -0.12534117187500013 3.2092384305570931e-17
		-0.23556403125 -0.085738500000000134 3.2092384305570931e-17
		-0.24687365624999996 -0.043530328125000121 3.2092384305570931e-17
		-0.25068234375000004 -1.2836953722228372e-16 3.2092384305570931e-17
		-0.24687365624999996 0.043530328124999865 3.2092384305570931e-17
		-0.23556403125 0.08573849999999987 3.2092384305570931e-17
		-0.21709729687499998 0.12534117187499988 3.2092384305570931e-17
		-0.19203370312500001 0.16113515624999988 3.2092384305570931e-17
		-0.16113557812500001 0.19203370312499987 3.2092384305570931e-17
		-0.12534117187500002 0.2170972968749999 3.2092384305570931e-17
		-0.085738499999999995 0.23556403124999986 3.2092384305570931e-17
		-0.043530328124999997 0.24687365624999985 3.2092384305570931e-17
		0 0.25068192187499988 3.2092384305570931e-17
		-1.2973120312500001e-09 0.24687365624999985 0.043530328125000024
		-2.5551998437500003e-09 0.23556403124999986 0.085738500000000023
		-3.73545421875e-09 0.2170972968749999 0.12534117187500005
		-4.8022031249999996e-09 0.19203370312499987 0.16113557812500001
		-5.7230296875000004e-09 0.16113515624999988 0.19203370312500001
		-6.4700015625000009e-09 0.12534117187499988 0.21709729687500001
		-7.0203796874999994e-09 0.08573849999999987 0.23556403125000003
		-7.3574156249999999e-09 0.043530328124999865 0.24687365624999996
		-7.4708999999999991e-09 -1.2836953722228372e-16 0.25068234375000004
		-0.077465109374999994 -1.2836953722228372e-16 0.23841295312500005
		-0.14734743750000001 -1.2836953722228372e-16 0.20280628125
		-0.20280628125 -1.2836953722228372e-16 0.14734743750000001
		-0.23841295312500005 -1.2836953722228372e-16 0.077465109375000035
		-0.25068234375000004 -1.2836953722228372e-16 3.2092384305570931e-17
		-0.23841295312500005 -1.2836953722228372e-16 -0.077465109374999966
		-0.20280628125 -1.2836953722228372e-16 -0.14734743750000001
		-0.14734743750000001 -1.2836953722228372e-16 -0.20280628125
		-0.077465109374999994 -1.2836953722228372e-16 -0.23841295312500005
		0 -1.2836953722228372e-16 -0.25068234375000004
		0.077465109374999994 -1.2836953722228372e-16 -0.23841295312500005
		0.14734743750000001 -1.2836953722228372e-16 -0.20280628125
		0.20280628125 -1.2836953722228372e-16 -0.14734743750000001
		0.23841295312500005 -1.2836953722228372e-16 -0.077465109374999966
		0.25068192187499999 -1.2836953722228372e-16 3.2092384305570931e-17
		0.23841295312500005 -1.2836953722228372e-16 0.077465109375000035
		0.20280628125 -1.2836953722228372e-16 0.14734743750000001
		0.14734743750000001 -1.2836953722228372e-16 0.20280628125
		0.077465109374999994 -1.2836953722228372e-16 0.23841295312500005
		-7.4708999999999991e-09 -1.2836953722228372e-16 0.25068234375000004
		;
createNode nurbsCurve -n "L_Foot_BallFloor_Guide_Ctrl_Ctrl_CtrlShape" -p "L_Foot_BallFloor_Guide";
	rename -uid "4483B015-2244-3967-268C-ADB77C9D8278";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/C:\\Users\\Esteban\\Documents\\maya\\2022\\scripts\\rigging\\Mutant_Tools\\Icons\\Guide_Data";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 13;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 9 0 no 3
		10 0 1 2 3 4 5 6 7 8 9
		10
		-0.2109375 -0.10546875000000014 -5.8966734374679077e-06
		0.39872714062500003 -0.10796456250000011 -5.8966734374679077e-06
		0.31204110937499996 -0.21365564062500014 -5.8966734374679077e-06
		0.41773218749999996 -0.39620432812500012 -5.8966734374679077e-06
		0.97001803124999997 -1.6344703137836954e-07 -5.821242187467907e-06
		0.41773260937500006 0.39620432812499984 -5.8966734374679077e-06
		0.31204110937499996 0.21365521874999988 -5.8966734374679077e-06
		0.39872714062500003 0.10682760937499987 -3.023772187467908e-06
		-0.2109375 0.10546874999999986 -5.8966734374679077e-06
		-0.2109375 -0.10546875000000014 -5.8966734374679077e-06
		;
createNode nurbsCurve -n "L_Foot_BallFloor_Guide_Ctrl_Ctrl_Ctrl_CtrlShape" -p "L_Foot_BallFloor_Guide";
	rename -uid "BE08393A-164F-122C-D361-A1958D7AC8F2";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/C:\\Users\\Esteban\\Documents\\maya\\2022\\scripts\\rigging\\Mutant_Tools\\Icons\\Guide_Data";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 6;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 9 0 no 3
		10 0 1 2 3 4 5 6 7 8 9
		10
		0.10546875 5.8966734373716305e-06 -0.2109375
		0.10796456249999997 5.8966734373716305e-06 0.39872714062500003
		0.21365564062499998 5.8966734373716305e-06 0.31204110937499996
		0.39620432812499995 5.8966734373716305e-06 0.41773218749999996
		1.6344703125e-07 5.8212421873716299e-06 0.97001803124999997
		-0.39620432812499995 5.8966734373716305e-06 0.41773260937500006
		-0.21365521875000001 5.8966734373716305e-06 0.31204110937499996
		-0.10682760937500001 3.0237721873716308e-06 0.39872714062500003
		-0.10546875 5.8966734373716305e-06 -0.2109375
		0.10546875 5.8966734373716305e-06 -0.2109375
		;
createNode joint -n "L_Foot_Out_Guide" -p "L_Foot_BallFloor_Guide";
	rename -uid "89121654-244D-BEE7-5B0C-86888FDD122F";
	addAttr -ci true -sn "Helper" -ln "Helper" -min 0 -max 1 -en "Hide:Show" -at "enum";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/C:\\Users\\Esteban\\Documents\\maya\\2022\\scripts\\rigging\\Mutant_Tools\\Icons\\Guide_Data";
	setAttr ".t" -type "double3" -6.5600919723510813 7.815970093361102e-14 5.5938465215042452e-14 ;
	setAttr ".r" -type "double3" 90.017464481762119 25.651662170893001 166.37226802711589 ;
	setAttr ".s" -type "double3" 0.99999999999999989 0.99999999999999944 0.99999999999999967 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0.01619980268339586 5.7344604848755961e-14 13.635291800429666 ;
	setAttr ".radi" 0.5;
	setAttr -cb on ".Helper";
createNode nurbsCurve -n "L_Foot_Out_Guide_CtrlShape" -p "L_Foot_Out_Guide";
	rename -uid "26E431D2-6C40-7F4C-E617-16A1A8DF9AFE";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/C:\\Users\\Esteban\\Documents\\maya\\2022\\scripts\\rigging\\Mutant_Tools\\Icons\\Guide_Data";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 14;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 9 0 no 3
		10 0 1 2 3 4 5 6 7 8 9
		10
		5.8966734376283696e-06 -0.2109375 0.10546875
		5.8966734376283696e-06 0.39872714062500003 0.10796456249999997
		5.8966734376283696e-06 0.31204110937499996 0.21365564062499998
		5.8966734376283696e-06 0.41773218749999996 0.39620432812499995
		5.8212421876283689e-06 0.97001803124999997 1.6344703125e-07
		5.8966734376283696e-06 0.41773260937500006 -0.39620432812499995
		5.8966734376283696e-06 0.31204110937499996 -0.21365521875000001
		3.0237721876283699e-06 0.39872714062500003 -0.10682760937500001
		5.8966734376283696e-06 -0.2109375 -0.10546875
		5.8966734376283696e-06 -0.2109375 0.10546875
		;
createNode nurbsCurve -n "L_Foot_Out_Guide_Ctrl_CtrlShape" -p "L_Foot_Out_Guide";
	rename -uid "29FED800-FF45-EDA5-7798-88A5766C1BFF";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/C:\\Users\\Esteban\\Documents\\maya\\2022\\scripts\\rigging\\Mutant_Tools\\Icons\\Guide_Data";
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
		1.2836953722228372e-16 0.25068192187499999 0
		-1.2973119028804628e-09 0.24687365624999996 0.043530328124999997
		-2.5551997153804631e-09 0.23556403125 0.085738499999999995
		-3.7354540903804627e-09 0.21709729687499998 0.12534117187500002
		-4.8022029966304623e-09 0.19203370312500001 0.16113557812500001
		-5.7230295591304631e-09 0.16113515624999999 0.19203370312500001
		-6.4700014341304637e-09 0.12534117187500002 0.21709729687499998
		-7.0203795591304622e-09 0.085738499999999995 0.23556403125
		-7.3574154966304626e-09 0.043530328124999997 0.24687365624999996
		-7.4708998716304619e-09 0 0.25068234375000004
		-7.3574154966304626e-09 -0.043530328124999997 0.24687365624999996
		-7.0203795591304622e-09 -0.085738499999999995 0.23556403125
		-6.4700014341304637e-09 -0.12534117187500002 0.21709729687499998
		-5.7230295591304631e-09 -0.16113515624999999 0.19203370312500001
		-4.8022029966304623e-09 -0.19203370312500001 0.16113557812500001
		-3.7354540903804627e-09 -0.21709729687499998 0.12534117187500002
		-2.5551997153804631e-09 -0.23556403125 0.085738499999999995
		-1.2973119028804628e-09 -0.24687365624999996 0.043530328124999997
		1.2836953722228372e-16 -0.25068192187499999 0
		1.2836953722228372e-16 -0.24687365624999996 -0.043530328124999997
		1.2836953722228372e-16 -0.23556403125 -0.085738499999999995
		1.2836953722228372e-16 -0.21709729687499998 -0.12534117187500002
		1.2836953722228372e-16 -0.19203370312500001 -0.16113557812500001
		1.2836953722228372e-16 -0.16113515624999999 -0.19203370312500001
		1.2836953722228372e-16 -0.12534117187500002 -0.21709729687499998
		1.2836953722228372e-16 -0.085738499999999995 -0.23556445312500002
		1.2836953722228372e-16 -0.043530328124999997 -0.24687365624999996
		1.2836953722228372e-16 0 -0.25068234375000004
		1.2836953722228372e-16 0.043530328124999997 -0.24687365624999996
		1.2836953722228372e-16 0.085738499999999995 -0.23556445312500002
		1.2836953722228372e-16 0.12534117187500002 -0.21709729687499998
		1.2836953722228372e-16 0.16113515624999999 -0.19203370312500001
		1.2836953722228372e-16 0.19203370312500001 -0.16113557812500001
		1.2836953722228372e-16 0.21709729687499998 -0.12534117187500002
		1.2836953722228372e-16 0.23556403125 -0.085738499999999995
		1.2836953722228372e-16 0.24687365624999996 -0.043530328124999997
		1.2836953722228372e-16 0.25068192187499999 0
		0.043530328125000121 0.24687365624999996 0
		0.085738500000000134 0.23556403125 0
		0.12534117187500013 0.21709729687499998 0
		0.16113557812500012 0.19203370312500001 0
		0.19203370312500012 0.16113515624999999 0
		0.21709729687500012 0.12534117187500002 0
		0.23556403125000014 0.085738499999999995 0
		0.24687365625000013 0.043530328124999997 0
		0.25068192187500016 0 0
		0.24687365625000013 -0.043530328124999997 0
		0.23556403125000014 -0.085738499999999995 0
		0.21709729687500012 -0.12534117187500002 0
		0.19203370312500012 -0.16113515624999999 0
		0.16113557812500012 -0.19203370312500001 0
		0.12534117187500013 -0.21709729687499998 0
		0.085738500000000134 -0.23556403125 0
		0.043530328125000121 -0.24687365624999996 0
		1.2836953722228372e-16 -0.25068192187499999 0
		-0.043530328124999865 -0.24687365624999996 0
		-0.08573849999999987 -0.23556403125 0
		-0.12534117187499988 -0.21709729687499998 0
		-0.16113557812499987 -0.19203370312500001 0
		-0.19203370312499987 -0.16113515624999999 0
		-0.2170972968749999 -0.12534117187500002 0
		-0.23556403124999986 -0.085738499999999995 0
		-0.24687365624999985 -0.043530328124999997 0
		-0.25068234374999987 0 0
		-0.24687365624999985 0.043530328124999997 0
		-0.23556403124999986 0.085738499999999995 0
		-0.2170972968749999 0.12534117187500002 0
		-0.19203370312499987 0.16113515624999999 0
		-0.16113557812499987 0.19203370312500001 0
		-0.12534117187499988 0.21709729687499998 0
		-0.08573849999999987 0.23556403125 0
		-0.043530328124999865 0.24687365624999996 0
		1.2836953722228372e-16 0.25068192187499999 0
		-1.2973119028804628e-09 0.24687365624999996 0.043530328124999997
		-2.5551997153804631e-09 0.23556403125 0.085738499999999995
		-3.7354540903804627e-09 0.21709729687499998 0.12534117187500002
		-4.8022029966304623e-09 0.19203370312500001 0.16113557812500001
		-5.7230295591304631e-09 0.16113515624999999 0.19203370312500001
		-6.4700014341304637e-09 0.12534117187500002 0.21709729687499998
		-7.0203795591304622e-09 0.085738499999999995 0.23556403125
		-7.3574154966304626e-09 0.043530328124999997 0.24687365624999996
		-7.4708998716304619e-09 0 0.25068234375000004
		-0.077465109374999869 0 0.23841295312500005
		-0.1473474374999999 0 0.20280628125
		-0.20280628124999983 0 0.14734743750000001
		-0.23841295312499988 0 0.077465109374999994
		-0.25068234374999987 0 0
		-0.23841295312499988 0 -0.077465109374999994
		-0.20280628124999983 0 -0.14734743750000001
		-0.1473474374999999 0 -0.20280628125
		-0.077465109374999869 0 -0.23841295312500005
		1.2836953722228372e-16 0 -0.25068234375000004
		0.077465109375000132 0 -0.23841295312500005
		0.14734743750000018 0 -0.20280628125
		0.20280628125000011 0 -0.14734743750000001
		0.23841295312500016 0 -0.077465109374999994
		0.25068192187500016 0 0
		0.23841295312500016 0 0.077465109374999994
		0.20280628125000011 0 0.14734743750000001
		0.14734743750000018 0 0.20280628125
		0.077465109375000132 0 0.23841295312500005
		-7.4708998716304619e-09 0 0.25068234375000004
		;
createNode nurbsCurve -n "L_Foot_Out_Guide_Ctrl_Ctrl_CtrlShape" -p "L_Foot_Out_Guide";
	rename -uid "2EA6CAF5-2C4D-8E18-3A26-1A9D9EFE4AF4";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/C:\\Users\\Esteban\\Documents\\maya\\2022\\scripts\\rigging\\Mutant_Tools\\Icons\\Guide_Data";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 13;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 9 0 no 3
		10 0 1 2 3 4 5 6 7 8 9
		10
		-0.21093749999999986 -0.10546875 -5.8966734375000001e-06
		0.3987271406250002 -0.10796456249999997 -5.8966734375000001e-06
		0.31204110937500007 -0.21365564062499998 -5.8966734375000001e-06
		0.41773218750000002 -0.39620432812499995 -5.8966734375000001e-06
		0.97001803124999997 -1.6344703125e-07 -5.8212421874999994e-06
		0.41773260937500012 0.39620432812499995 -5.8966734375000001e-06
		0.31204110937500007 0.21365521875000001 -5.8966734375000001e-06
		0.3987271406250002 0.10682760937500001 -3.0237721875000003e-06
		-0.21093749999999986 0.10546875 -5.8966734375000001e-06
		-0.21093749999999986 -0.10546875 -5.8966734375000001e-06
		;
createNode nurbsCurve -n "L_Foot_Out_Guide_Ctrl_Ctrl_Ctrl_CtrlShape" -p "L_Foot_Out_Guide";
	rename -uid "15E183A8-9B40-5AC7-2B55-F6B7FD0264AE";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/C:\\Users\\Esteban\\Documents\\maya\\2022\\scripts\\rigging\\Mutant_Tools\\Icons\\Guide_Data";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 6;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 9 0 no 3
		10 0 1 2 3 4 5 6 7 8 9
		10
		0.10546875000000014 5.8966734375000001e-06 -0.2109375
		0.10796456250000011 5.8966734375000001e-06 0.39872714062500003
		0.21365564062500014 5.8966734375000001e-06 0.31204110937499996
		0.39620432812500012 5.8966734375000001e-06 0.41773218749999996
		1.6344703137836954e-07 5.8212421874999994e-06 0.97001803124999997
		-0.39620432812499984 5.8966734375000001e-06 0.41773260937500006
		-0.21365521874999988 5.8966734375000001e-06 0.31204110937499996
		-0.10682760937499987 3.0237721875000003e-06 0.39872714062500003
		-0.10546874999999986 5.8966734375000001e-06 -0.2109375
		0.10546875000000014 5.8966734375000001e-06 -0.2109375
		;
createNode joint -n "L_Foot_In_Guide" -p "L_Foot_BallFloor_Guide";
	rename -uid "DF359CAA-944D-ECD1-C995-D6841E5FE905";
	addAttr -ci true -sn "Helper" -ln "Helper" -min 0 -max 1 -en "Hide:Show" -at "enum";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/C:\\Users\\Esteban\\Documents\\maya\\2022\\scripts\\rigging\\Mutant_Tools\\Icons\\Guide_Data";
	setAttr ".t" -type "double3" 6.5600919723511044 -1.4210854715202004e-14 -5.4361237005038972e-14 ;
	setAttr ".r" -type "double3" 90.017463363953084 -25.644024263601704 166.35714990519321 ;
	setAttr ".s" -type "double3" 0.99999999999999989 0.99999999999999944 0.99999999999999967 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0.016199802683428344 -5.5443101680509104e-15 13.635291800429693 ;
	setAttr ".radi" 0.5;
	setAttr -cb on ".Helper";
createNode nurbsCurve -n "L_Foot_In_Guide_CtrlShape" -p "L_Foot_In_Guide";
	rename -uid "16CF5C58-1746-D41B-E29C-E0AECCC3CE80";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/C:\\Users\\Esteban\\Documents\\maya\\2022\\scripts\\rigging\\Mutant_Tools\\Icons\\Guide_Data";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 14;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 9 0 no 3
		10 0 1 2 3 4 5 6 7 8 9
		10
		5.8966734374679077e-06 -0.21093749999999986 0.10546875000000025
		5.8966734374679077e-06 0.3987271406250002 0.10796456250000025
		5.8966734374679077e-06 0.31204110937500007 0.21365564062500023
		5.8966734374679077e-06 0.41773218750000002 0.39620432812500028
		5.821242187467907e-06 0.97001803124999997 1.6344703150673908e-07
		5.8966734374679077e-06 0.41773260937500012 -0.39620432812499973
		5.8966734374679077e-06 0.31204110937500007 -0.21365521874999974
		3.023772187467908e-06 0.3987271406250002 -0.10682760937499973
		5.8966734374679077e-06 -0.21093749999999986 -0.10546874999999975
		5.8966734374679077e-06 -0.21093749999999986 0.10546875000000025
		;
createNode nurbsCurve -n "L_Foot_In_Guide_Ctrl_CtrlShape" -p "L_Foot_In_Guide";
	rename -uid "66AAA19A-D446-1D58-8865-0BB01346455B";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/C:\\Users\\Esteban\\Documents\\maya\\2022\\scripts\\rigging\\Mutant_Tools\\Icons\\Guide_Data";
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
		-3.2092384305570931e-17 0.25068192187500016 2.5673907444456745e-16
		-1.2973120633423844e-09 0.24687365625000013 0.043530328125000253
		-2.5551998758423846e-09 0.23556403125000014 0.085738500000000259
		-3.7354542508423843e-09 0.21709729687500012 0.12534117187500027
		-4.8022031570923839e-09 0.19203370312500012 0.16113557812500023
		-5.7230297195923847e-09 0.16113515625000013 0.19203370312500023
		-6.4700015945923852e-09 0.12534117187500013 0.21709729687500026
		-7.0203797195923837e-09 0.085738500000000134 0.23556403125000028
		-7.3574156570923842e-09 0.043530328125000121 0.24687365625000021
		-7.4709000320923834e-09 1.2836953722228372e-16 0.25068234375000026
		-7.3574156570923842e-09 -0.043530328124999865 0.24687365625000021
		-7.0203797195923837e-09 -0.08573849999999987 0.23556403125000028
		-6.4700015945923852e-09 -0.12534117187499988 0.21709729687500026
		-5.7230297195923847e-09 -0.16113515624999988 0.19203370312500023
		-4.8022031570923839e-09 -0.19203370312499987 0.16113557812500023
		-3.7354542508423843e-09 -0.2170972968749999 0.12534117187500027
		-2.5551998758423846e-09 -0.23556403124999986 0.085738500000000259
		-1.2973120633423844e-09 -0.24687365624999985 0.043530328125000253
		-3.2092384305570931e-17 -0.25068192187499988 2.5673907444456745e-16
		-3.2092384305570931e-17 -0.24687365624999985 -0.04353032812499974
		-3.2092384305570931e-17 -0.23556403124999986 -0.085738499999999745
		-3.2092384305570931e-17 -0.2170972968749999 -0.12534117187499977
		-3.2092384305570931e-17 -0.19203370312499987 -0.16113557812499973
		-3.2092384305570931e-17 -0.16113515624999988 -0.19203370312499973
		-3.2092384305570931e-17 -0.12534117187499988 -0.21709729687499973
		-3.2092384305570931e-17 -0.08573849999999987 -0.23556445312499974
		-3.2092384305570931e-17 -0.043530328124999865 -0.24687365624999974
		-3.2092384305570931e-17 1.2836953722228372e-16 -0.25068234374999976
		-3.2092384305570931e-17 0.043530328125000121 -0.24687365624999974
		-3.2092384305570931e-17 0.085738500000000134 -0.23556445312499974
		-3.2092384305570931e-17 0.12534117187500013 -0.21709729687499973
		-3.2092384305570931e-17 0.16113515625000013 -0.19203370312499973
		-3.2092384305570931e-17 0.19203370312500012 -0.16113557812499973
		-3.2092384305570931e-17 0.21709729687500012 -0.12534117187499977
		-3.2092384305570931e-17 0.23556403125000014 -0.085738499999999745
		-3.2092384305570931e-17 0.24687365625000013 -0.04353032812499974
		-3.2092384305570931e-17 0.25068192187500016 2.5673907444456745e-16
		0.043530328124999962 0.24687365625000013 2.5673907444456745e-16
		0.085738499999999981 0.23556403125000014 2.5673907444456745e-16
		0.12534117187499999 0.21709729687500012 2.5673907444456745e-16
		0.16113557812500001 0.19203370312500012 2.5673907444456745e-16
		0.19203370312500001 0.16113515625000013 2.5673907444456745e-16
		0.21709729687499996 0.12534117187500013 2.5673907444456745e-16
		0.23556403124999997 0.085738500000000134 2.5673907444456745e-16
		0.24687365624999996 0.043530328125000121 2.5673907444456745e-16
		0.25068192187499999 1.2836953722228372e-16 2.5673907444456745e-16
		0.24687365624999996 -0.043530328124999865 2.5673907444456745e-16
		0.23556403124999997 -0.08573849999999987 2.5673907444456745e-16
		0.21709729687499996 -0.12534117187499988 2.5673907444456745e-16
		0.19203370312500001 -0.16113515624999988 2.5673907444456745e-16
		0.16113557812500001 -0.19203370312499987 2.5673907444456745e-16
		0.12534117187499999 -0.2170972968749999 2.5673907444456745e-16
		0.085738499999999981 -0.23556403124999986 2.5673907444456745e-16
		0.043530328124999962 -0.24687365624999985 2.5673907444456745e-16
		-3.2092384305570931e-17 -0.25068192187499988 2.5673907444456745e-16
		-0.043530328125000024 -0.24687365624999985 2.5673907444456745e-16
		-0.085738500000000023 -0.23556403124999986 2.5673907444456745e-16
		-0.12534117187500005 -0.2170972968749999 2.5673907444456745e-16
		-0.16113557812500001 -0.19203370312499987 2.5673907444456745e-16
		-0.19203370312500001 -0.16113515624999988 2.5673907444456745e-16
		-0.21709729687500001 -0.12534117187499988 2.5673907444456745e-16
		-0.23556403125000003 -0.08573849999999987 2.5673907444456745e-16
		-0.24687365624999996 -0.043530328124999865 2.5673907444456745e-16
		-0.25068234375000004 1.2836953722228372e-16 2.5673907444456745e-16
		-0.24687365624999996 0.043530328125000121 2.5673907444456745e-16
		-0.23556403125000003 0.085738500000000134 2.5673907444456745e-16
		-0.21709729687500001 0.12534117187500013 2.5673907444456745e-16
		-0.19203370312500001 0.16113515625000013 2.5673907444456745e-16
		-0.16113557812500001 0.19203370312500012 2.5673907444456745e-16
		-0.12534117187500005 0.21709729687500012 2.5673907444456745e-16
		-0.085738500000000023 0.23556403125000014 2.5673907444456745e-16
		-0.043530328125000024 0.24687365625000013 2.5673907444456745e-16
		-3.2092384305570931e-17 0.25068192187500016 2.5673907444456745e-16
		-1.2973120633423844e-09 0.24687365625000013 0.043530328125000253
		-2.5551998758423846e-09 0.23556403125000014 0.085738500000000259
		-3.7354542508423843e-09 0.21709729687500012 0.12534117187500027
		-4.8022031570923839e-09 0.19203370312500012 0.16113557812500023
		-5.7230297195923847e-09 0.16113515625000013 0.19203370312500023
		-6.4700015945923852e-09 0.12534117187500013 0.21709729687500026
		-7.0203797195923837e-09 0.085738500000000134 0.23556403125000028
		-7.3574156570923842e-09 0.043530328125000121 0.24687365625000021
		-7.4709000320923834e-09 1.2836953722228372e-16 0.25068234375000026
		-0.077465109375000035 1.2836953722228372e-16 0.23841295312500027
		-0.14734743750000001 1.2836953722228372e-16 0.20280628125000028
		-0.20280628125 1.2836953722228372e-16 0.14734743750000029
		-0.23841295312500005 1.2836953722228372e-16 0.077465109375000257
		-0.25068234375000004 1.2836953722228372e-16 2.5673907444456745e-16
		-0.23841295312500005 1.2836953722228372e-16 -0.07746510937499973
		-0.20280628125 1.2836953722228372e-16 -0.14734743749999976
		-0.14734743750000001 1.2836953722228372e-16 -0.20280628124999975
		-0.077465109375000035 1.2836953722228372e-16 -0.2384129531249998
		-3.2092384305570931e-17 1.2836953722228372e-16 -0.25068234374999976
		0.077465109374999966 1.2836953722228372e-16 -0.2384129531249998
		0.14734743750000001 1.2836953722228372e-16 -0.20280628124999975
		0.20280628125 1.2836953722228372e-16 -0.14734743749999976
		0.23841295312500005 1.2836953722228372e-16 -0.07746510937499973
		0.25068192187499999 1.2836953722228372e-16 2.5673907444456745e-16
		0.23841295312500005 1.2836953722228372e-16 0.077465109375000257
		0.20280628125 1.2836953722228372e-16 0.14734743750000029
		0.14734743750000001 1.2836953722228372e-16 0.20280628125000028
		0.077465109374999966 1.2836953722228372e-16 0.23841295312500027
		-7.4709000320923834e-09 1.2836953722228372e-16 0.25068234375000026
		;
createNode nurbsCurve -n "L_Foot_In_Guide_Ctrl_Ctrl_CtrlShape" -p "L_Foot_In_Guide";
	rename -uid "13C992AC-C043-B142-DD92-83BF6BE27A0B";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/C:\\Users\\Esteban\\Documents\\maya\\2022\\scripts\\rigging\\Mutant_Tools\\Icons\\Guide_Data";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 13;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 9 0 no 3
		10 0 1 2 3 4 5 6 7 8 9
		10
		-0.2109375 -0.10546874999999986 -5.896673437243261e-06
		0.39872714062500003 -0.10796456249999986 -5.896673437243261e-06
		0.31204110937499996 -0.21365564062499987 -5.896673437243261e-06
		0.41773218749999996 -0.39620432812499984 -5.896673437243261e-06
		0.97001803124999997 -1.6344703112163046e-07 -5.8212421872432603e-06
		0.41773260937500006 0.39620432812500012 -5.896673437243261e-06
		0.31204110937499996 0.2136552187500001 -5.896673437243261e-06
		0.39872714062500003 0.10682760937500013 -3.0237721872432613e-06
		-0.2109375 0.10546875000000014 -5.896673437243261e-06
		-0.2109375 -0.10546874999999986 -5.896673437243261e-06
		;
createNode nurbsCurve -n "L_Foot_In_Guide_Ctrl_Ctrl_Ctrl_CtrlShape" -p "L_Foot_In_Guide";
	rename -uid "835696EA-F34D-960A-47DF-32BF452D1E48";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/C:\\Users\\Esteban\\Documents\\maya\\2022\\scripts\\rigging\\Mutant_Tools\\Icons\\Guide_Data";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 6;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 9 0 no 3
		10 0 1 2 3 4 5 6 7 8 9
		10
		0.10546874999999999 5.8966734376283696e-06 -0.21093749999999972
		0.10796456249999996 5.8966734376283696e-06 0.39872714062500036
		0.21365564062499998 5.8966734376283696e-06 0.31204110937500029
		0.39620432812499995 5.8966734376283696e-06 0.41773218750000024
		1.6344703121790762e-07 5.8212421876283689e-06 0.9700180312500003
		-0.39620432812499995 5.8966734376283696e-06 0.41773260937500023
		-0.21365521875000004 5.8966734376283696e-06 0.31204110937500029
		-0.10682760937500002 3.0237721876283699e-06 0.39872714062500036
		-0.10546875000000001 5.8966734376283696e-06 -0.21093749999999972
		0.10546874999999999 5.8966734376283696e-06 -0.21093749999999972
		;
createNode joint -n "L_Foot_Toes_Guide" -p "L_Foot_Ball_Guide";
	rename -uid "2009E1DA-C141-6A41-ABCD-1E8D6A891055";
	addAttr -ci true -sn "Helper" -ln "Helper" -min 0 -max 1 -en "Hide:Show" -at "enum";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/C:\\Users\\Esteban\\Documents\\maya\\2022\\scripts\\rigging\\Mutant_Tools\\Icons\\Guide_Data";
	setAttr ".t" -type "double3" 6.7811814691981498 0.10892320872494526 -7.3703196323826603e-14 ;
	setAttr ".r" -type "double3" -5.3690054300112816e-14 -13.635291800429794 -6.3938957138413858e-15 ;
	setAttr ".s" -type "double3" 1 1.0000000000000002 1.0000000000000002 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" -2.5444437451708134e-14 105.35411682038847 39.168612025680879 ;
	setAttr ".radi" 0.5;
	setAttr -cb on ".Helper";
createNode nurbsCurve -n "L_Foot_Toes_Guide_CtrlShape" -p "L_Foot_Toes_Guide";
	rename -uid "1949B3C5-C542-0E29-8D7D-B39EB3B94DA4";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/C:\\Users\\Esteban\\Documents\\maya\\2022\\scripts\\rigging\\Mutant_Tools\\Icons\\Guide_Data";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 14;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 9 0 no 3
		10 0 1 2 3 4 5 6 7 8 9
		10
		5.8966734376283696e-06 -0.21093749999999997 0.10546874999999949
		5.8966734376283696e-06 0.39872714062500003 0.10796456249999946
		5.8966734376283696e-06 0.31204110937499996 0.21365564062499948
		5.8966734376283696e-06 0.41773218749999996 0.39620432812499951
		5.8212421876283689e-06 0.97001803124999997 1.6344703073652185e-07
		5.8966734376283696e-06 0.41773260937500012 -0.3962043281250005
		5.8966734376283696e-06 0.31204110937499996 -0.21365521875000049
		3.0237721876283699e-06 0.39872714062500003 -0.10682760937500052
		5.8966734376283696e-06 -0.21093749999999997 -0.10546875000000051
		5.8966734376283696e-06 -0.21093749999999997 0.10546874999999949
		;
createNode nurbsCurve -n "L_Foot_Toes_Guide_Ctrl_CtrlShape" -p "L_Foot_Toes_Guide";
	rename -uid "A72BF2AB-1C4A-735E-58BB-D9A9A36400D4";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/C:\\Users\\Esteban\\Documents\\maya\\2022\\scripts\\rigging\\Mutant_Tools\\Icons\\Guide_Data";
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
		1.2836953722228372e-16 0.25068192187500005 -5.134781488891349e-16
		-1.2973119028804628e-09 0.24687365625000005 0.043530328124999483
		-2.5551997153804631e-09 0.23556403125000003 0.085738499999999496
		-3.7354540903804627e-09 0.21709729687500001 0.12534117187499949
		-4.8022029966304623e-09 0.19203370312500004 0.16113557812499951
		-5.7230295591304631e-09 0.16113515625000008 0.19203370312499946
		-6.4700014341304637e-09 0.12534117187500007 0.21709729687499951
		-7.0203795591304622e-09 0.085738500000000079 0.23556403124999947
		-7.3574154966304626e-09 0.043530328125000059 0.24687365624999946
		-7.4708998716304619e-09 6.4184768611141862e-17 0.25068234374999954
		-7.3574154966304626e-09 -0.043530328124999934 0.24687365624999946
		-7.0203795591304622e-09 -0.08573849999999994 0.23556403124999947
		-6.4700014341304637e-09 -0.12534117187499993 0.21709729687499951
		-5.7230295591304631e-09 -0.16113515624999994 0.19203370312499946
		-4.8022029966304623e-09 -0.19203370312499998 0.16113557812499951
		-3.7354540903804627e-09 -0.21709729687499996 0.12534117187499949
		-2.5551997153804631e-09 -0.23556403124999997 0.085738499999999496
		-1.2973119028804628e-09 -0.24687365624999991 0.043530328124999483
		1.2836953722228372e-16 -0.25068192187499994 -5.134781488891349e-16
		1.2836953722228372e-16 -0.24687365624999991 -0.04353032812500051
		1.2836953722228372e-16 -0.23556403124999997 -0.085738500000000523
		1.2836953722228372e-16 -0.21709729687499996 -0.12534117187500052
		1.2836953722228372e-16 -0.19203370312499998 -0.16113557812500051
		1.2836953722228372e-16 -0.16113515624999994 -0.19203370312500048
		1.2836953722228372e-16 -0.12534117187499993 -0.21709729687500054
		1.2836953722228372e-16 -0.08573849999999994 -0.23556445312500049
		1.2836953722228372e-16 -0.043530328124999934 -0.24687365625000049
		1.2836953722228372e-16 6.4184768611141862e-17 -0.25068234375000054
		1.2836953722228372e-16 0.043530328125000059 -0.24687365625000049
		1.2836953722228372e-16 0.085738500000000079 -0.23556445312500049
		1.2836953722228372e-16 0.12534117187500007 -0.21709729687500054
		1.2836953722228372e-16 0.16113515625000008 -0.19203370312500048
		1.2836953722228372e-16 0.19203370312500004 -0.16113557812500051
		1.2836953722228372e-16 0.21709729687500001 -0.12534117187500052
		1.2836953722228372e-16 0.23556403125000003 -0.085738500000000523
		1.2836953722228372e-16 0.24687365625000005 -0.04353032812500051
		1.2836953722228372e-16 0.25068192187500005 -5.134781488891349e-16
		0.043530328125000121 0.24687365625000005 -5.134781488891349e-16
		0.085738500000000134 0.23556403125000003 -5.134781488891349e-16
		0.12534117187500013 0.21709729687500001 -5.134781488891349e-16
		0.16113557812500012 0.19203370312500004 -5.134781488891349e-16
		0.19203370312500012 0.16113515625000008 -5.134781488891349e-16
		0.21709729687500012 0.12534117187500007 -5.134781488891349e-16
		0.23556403125000014 0.085738500000000079 -5.134781488891349e-16
		0.24687365625000013 0.043530328125000059 -5.134781488891349e-16
		0.25068192187500016 6.4184768611141862e-17 -5.134781488891349e-16
		0.24687365625000013 -0.043530328124999934 -5.134781488891349e-16
		0.23556403125000014 -0.08573849999999994 -5.134781488891349e-16
		0.21709729687500012 -0.12534117187499993 -5.134781488891349e-16
		0.19203370312500012 -0.16113515624999994 -5.134781488891349e-16
		0.16113557812500012 -0.19203370312499998 -5.134781488891349e-16
		0.12534117187500013 -0.21709729687499996 -5.134781488891349e-16
		0.085738500000000134 -0.23556403124999997 -5.134781488891349e-16
		0.043530328125000121 -0.24687365624999991 -5.134781488891349e-16
		1.2836953722228372e-16 -0.25068192187499994 -5.134781488891349e-16
		-0.043530328124999865 -0.24687365624999991 -5.134781488891349e-16
		-0.08573849999999987 -0.23556403124999997 -5.134781488891349e-16
		-0.12534117187499988 -0.21709729687499996 -5.134781488891349e-16
		-0.16113557812499987 -0.19203370312499998 -5.134781488891349e-16
		-0.19203370312499987 -0.16113515624999994 -5.134781488891349e-16
		-0.2170972968749999 -0.12534117187499993 -5.134781488891349e-16
		-0.23556403124999986 -0.08573849999999994 -5.134781488891349e-16
		-0.24687365624999985 -0.043530328124999934 -5.134781488891349e-16
		-0.25068234374999987 6.4184768611141862e-17 -5.134781488891349e-16
		-0.24687365624999985 0.043530328125000059 -5.134781488891349e-16
		-0.23556403124999986 0.085738500000000079 -5.134781488891349e-16
		-0.2170972968749999 0.12534117187500007 -5.134781488891349e-16
		-0.19203370312499987 0.16113515625000008 -5.134781488891349e-16
		-0.16113557812499987 0.19203370312500004 -5.134781488891349e-16
		-0.12534117187499988 0.21709729687500001 -5.134781488891349e-16
		-0.08573849999999987 0.23556403125000003 -5.134781488891349e-16
		-0.043530328124999865 0.24687365625000005 -5.134781488891349e-16
		1.2836953722228372e-16 0.25068192187500005 -5.134781488891349e-16
		-1.2973119028804628e-09 0.24687365625000005 0.043530328124999483
		-2.5551997153804631e-09 0.23556403125000003 0.085738499999999496
		-3.7354540903804627e-09 0.21709729687500001 0.12534117187499949
		-4.8022029966304623e-09 0.19203370312500004 0.16113557812499951
		-5.7230295591304631e-09 0.16113515625000008 0.19203370312499946
		-6.4700014341304637e-09 0.12534117187500007 0.21709729687499951
		-7.0203795591304622e-09 0.085738500000000079 0.23556403124999947
		-7.3574154966304626e-09 0.043530328125000059 0.24687365624999946
		-7.4708998716304619e-09 6.4184768611141862e-17 0.25068234374999954
		-0.077465109374999869 6.4184768611141862e-17 0.23841295312499952
		-0.1473474374999999 6.4184768611141862e-17 0.20280628124999947
		-0.20280628124999983 6.4184768611141862e-17 0.14734743749999951
		-0.23841295312499988 6.4184768611141862e-17 0.07746510937499948
		-0.25068234374999987 6.4184768611141862e-17 -5.134781488891349e-16
		-0.23841295312499988 6.4184768611141862e-17 -0.077465109375000507
		-0.20280628124999983 6.4184768611141862e-17 -0.14734743750000054
		-0.1473474374999999 6.4184768611141862e-17 -0.2028062812500005
		-0.077465109374999869 6.4184768611141862e-17 -0.23841295312500055
		1.2836953722228372e-16 6.4184768611141862e-17 -0.25068234375000054
		0.077465109375000132 6.4184768611141862e-17 -0.23841295312500055
		0.14734743750000018 6.4184768611141862e-17 -0.2028062812500005
		0.20280628125000011 6.4184768611141862e-17 -0.14734743750000054
		0.23841295312500016 6.4184768611141862e-17 -0.077465109375000507
		0.25068192187500016 6.4184768611141862e-17 -5.134781488891349e-16
		0.23841295312500016 6.4184768611141862e-17 0.07746510937499948
		0.20280628125000011 6.4184768611141862e-17 0.14734743749999951
		0.14734743750000018 6.4184768611141862e-17 0.20280628124999947
		0.077465109375000132 6.4184768611141862e-17 0.23841295312499952
		-7.4708998716304619e-09 6.4184768611141862e-17 0.25068234374999954
		;
createNode nurbsCurve -n "L_Foot_Toes_Guide_Ctrl_Ctrl_CtrlShape" -p "L_Foot_Toes_Guide";
	rename -uid "F1628E6F-954D-853B-AAE1-DCB455EF5FA9";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/C:\\Users\\Esteban\\Documents\\maya\\2022\\scripts\\rigging\\Mutant_Tools\\Icons\\Guide_Data";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 13;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 9 0 no 3
		10 0 1 2 3 4 5 6 7 8 9
		10
		-0.21093749999999986 -0.10546874999999993 -5.8966734380134782e-06
		0.3987271406250002 -0.10796456249999992 -5.8966734380134782e-06
		0.31204110937500007 -0.21365564062499992 -5.8966734380134782e-06
		0.41773218750000002 -0.39620432812499995 -5.8966734380134782e-06
		0.97001803124999997 -1.6344703118581523e-07 -5.8212421880134776e-06
		0.41773260937500012 0.39620432812499995 -5.8966734380134782e-06
		0.31204110937500007 0.21365521875000004 -5.8966734380134782e-06
		0.3987271406250002 0.10682760937500005 -3.0237721880134785e-06
		-0.21093749999999986 0.10546875000000007 -5.8966734380134782e-06
		-0.21093749999999986 -0.10546874999999993 -5.8966734380134782e-06
		;
createNode nurbsCurve -n "L_Foot_Toes_Guide_Ctrl_Ctrl_Ctrl_CtrlShape" -p "L_Foot_Toes_Guide";
	rename -uid "6755FBBB-E64E-C4A2-6EFE-58A2960E45C0";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/C:\\Users\\Esteban\\Documents\\maya\\2022\\scripts\\rigging\\Mutant_Tools\\Icons\\Guide_Data";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 6;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 9 0 no 3
		10 0 1 2 3 4 5 6 7 8 9
		10
		0.10546875000000014 5.8966734375641848e-06 -0.2109375000000005
		0.10796456250000011 5.8966734375641848e-06 0.39872714062499948
		0.21365564062500014 5.8966734375641848e-06 0.31204110937499946
		0.39620432812500012 5.8966734375641848e-06 0.41773218749999941
		1.6344703137836954e-07 5.8212421875641842e-06 0.97001803124999952
		-0.39620432812499984 5.8966734375641848e-06 0.41773260937499951
		-0.21365521874999988 5.8966734375641848e-06 0.31204110937499946
		-0.10682760937499987 3.0237721875641851e-06 0.39872714062499948
		-0.10546874999999986 5.8966734375641848e-06 -0.2109375000000005
		0.10546875000000014 5.8966734375641848e-06 -0.2109375000000005
		;
createNode joint -n "L_Foot_HeelMid_Guide" -p "L_Foot_Ankle_Guide";
	rename -uid "36DEB792-594E-E433-29DF-AB9D787CC472";
	addAttr -ci true -sn "Helper" -ln "Helper" -min 0 -max 1 -en "Hide:Show" -at "enum";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/C:\\Users\\Esteban\\Documents\\maya\\2022\\scripts\\rigging\\Mutant_Tools\\Icons\\Guide_Data";
	setAttr ".t" -type "double3" 7.1403296659462789 1.7937948320487962 0.34441912281562637 ;
	setAttr ".r" -type "double3" 0 -13.6352918004301 0 ;
	setAttr ".s" -type "double3" 0.99999999999999989 0.99999999999999978 0.99999999999999978 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 105.3541168203888 129.16861202568089 ;
	setAttr ".radi" 0.5;
	setAttr -cb on ".Helper";
createNode nurbsCurve -n "L_Foot_HeelMid_Guide_CtrlShape" -p "L_Foot_HeelMid_Guide";
	rename -uid "45F54CB2-A143-CA85-B398-F091D43BF88E";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/C:\\Users\\Esteban\\Documents\\maya\\2022\\scripts\\rigging\\Mutant_Tools\\Icons\\Guide_Data";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 14;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 9 0 no 3
		10 0 1 2 3 4 5 6 7 8 9
		10
		5.8966734375000001e-06 -0.2109375 0.10546874999999999
		5.8966734375000001e-06 0.39872714062500003 0.10796456249999996
		5.8966734375000001e-06 0.31204110937499996 0.21365564062499998
		5.8966734375000001e-06 0.41773218749999996 0.39620432812499995
		5.8212421874999994e-06 0.97001803124999997 1.6344703121790762e-07
		5.8966734375000001e-06 0.41773260937500006 -0.39620432812499995
		5.8966734375000001e-06 0.31204110937499996 -0.21365521875000004
		3.0237721875000003e-06 0.39872714062500003 -0.10682760937500002
		5.8966734375000001e-06 -0.2109375 -0.10546875000000001
		5.8966734375000001e-06 -0.2109375 0.10546874999999999
		;
createNode nurbsCurve -n "L_Foot_HeelMid_Guide_Ctrl_CtrlShape" -p "L_Foot_HeelMid_Guide";
	rename -uid "55ABF7EE-C540-4E84-14B1-95976745ED23";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/C:\\Users\\Esteban\\Documents\\maya\\2022\\scripts\\rigging\\Mutant_Tools\\Icons\\Guide_Data";
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
		0 0.25068192187499999 -3.2092384305570931e-17
		-1.2973120312500001e-09 0.24687365624999996 0.043530328124999962
		-2.5551998437500003e-09 0.23556403125 0.085738499999999981
		-3.73545421875e-09 0.21709729687499998 0.12534117187499999
		-4.8022031249999996e-09 0.19203370312500001 0.16113557812500001
		-5.7230296875000004e-09 0.16113515624999999 0.19203370312500001
		-6.4700015625000009e-09 0.12534117187500002 0.21709729687499996
		-7.0203796874999994e-09 0.085738499999999995 0.23556403124999997
		-7.3574156249999999e-09 0.043530328124999997 0.24687365624999996
		-7.4708999999999991e-09 0 0.25068234375000004
		-7.3574156249999999e-09 -0.043530328124999997 0.24687365624999996
		-7.0203796874999994e-09 -0.085738499999999995 0.23556403124999997
		-6.4700015625000009e-09 -0.12534117187500002 0.21709729687499996
		-5.7230296875000004e-09 -0.16113515624999999 0.19203370312500001
		-4.8022031249999996e-09 -0.19203370312500001 0.16113557812500001
		-3.73545421875e-09 -0.21709729687499998 0.12534117187499999
		-2.5551998437500003e-09 -0.23556403125 0.085738499999999981
		-1.2973120312500001e-09 -0.24687365624999996 0.043530328124999962
		0 -0.25068192187499999 -3.2092384305570931e-17
		0 -0.24687365624999996 -0.043530328125000024
		0 -0.23556403125 -0.085738500000000023
		0 -0.21709729687499998 -0.12534117187500005
		0 -0.19203370312500001 -0.16113557812500001
		0 -0.16113515624999999 -0.19203370312500001
		0 -0.12534117187500002 -0.21709729687500001
		0 -0.085738499999999995 -0.23556445312500002
		0 -0.043530328124999997 -0.24687365624999996
		0 0 -0.25068234375000004
		0 0.043530328124999997 -0.24687365624999996
		0 0.085738499999999995 -0.23556445312500002
		0 0.12534117187500002 -0.21709729687500001
		0 0.16113515624999999 -0.19203370312500001
		0 0.19203370312500001 -0.16113557812500001
		0 0.21709729687499998 -0.12534117187500005
		0 0.23556403125 -0.085738500000000023
		0 0.24687365624999996 -0.043530328125000024
		0 0.25068192187499999 -3.2092384305570931e-17
		0.043530328124999997 0.24687365624999996 -3.2092384305570931e-17
		0.085738499999999995 0.23556403125 -3.2092384305570931e-17
		0.12534117187500002 0.21709729687499998 -3.2092384305570931e-17
		0.16113557812500001 0.19203370312500001 -3.2092384305570931e-17
		0.19203370312500001 0.16113515624999999 -3.2092384305570931e-17
		0.21709729687499998 0.12534117187500002 -3.2092384305570931e-17
		0.23556403125 0.085738499999999995 -3.2092384305570931e-17
		0.24687365624999996 0.043530328124999997 -3.2092384305570931e-17
		0.25068192187499999 0 -3.2092384305570931e-17
		0.24687365624999996 -0.043530328124999997 -3.2092384305570931e-17
		0.23556403125 -0.085738499999999995 -3.2092384305570931e-17
		0.21709729687499998 -0.12534117187500002 -3.2092384305570931e-17
		0.19203370312500001 -0.16113515624999999 -3.2092384305570931e-17
		0.16113557812500001 -0.19203370312500001 -3.2092384305570931e-17
		0.12534117187500002 -0.21709729687499998 -3.2092384305570931e-17
		0.085738499999999995 -0.23556403125 -3.2092384305570931e-17
		0.043530328124999997 -0.24687365624999996 -3.2092384305570931e-17
		0 -0.25068192187499999 -3.2092384305570931e-17
		-0.043530328124999997 -0.24687365624999996 -3.2092384305570931e-17
		-0.085738499999999995 -0.23556403125 -3.2092384305570931e-17
		-0.12534117187500002 -0.21709729687499998 -3.2092384305570931e-17
		-0.16113557812500001 -0.19203370312500001 -3.2092384305570931e-17
		-0.19203370312500001 -0.16113515624999999 -3.2092384305570931e-17
		-0.21709729687499998 -0.12534117187500002 -3.2092384305570931e-17
		-0.23556403125 -0.085738499999999995 -3.2092384305570931e-17
		-0.24687365624999996 -0.043530328124999997 -3.2092384305570931e-17
		-0.25068234375000004 0 -3.2092384305570931e-17
		-0.24687365624999996 0.043530328124999997 -3.2092384305570931e-17
		-0.23556403125 0.085738499999999995 -3.2092384305570931e-17
		-0.21709729687499998 0.12534117187500002 -3.2092384305570931e-17
		-0.19203370312500001 0.16113515624999999 -3.2092384305570931e-17
		-0.16113557812500001 0.19203370312500001 -3.2092384305570931e-17
		-0.12534117187500002 0.21709729687499998 -3.2092384305570931e-17
		-0.085738499999999995 0.23556403125 -3.2092384305570931e-17
		-0.043530328124999997 0.24687365624999996 -3.2092384305570931e-17
		0 0.25068192187499999 -3.2092384305570931e-17
		-1.2973120312500001e-09 0.24687365624999996 0.043530328124999962
		-2.5551998437500003e-09 0.23556403125 0.085738499999999981
		-3.73545421875e-09 0.21709729687499998 0.12534117187499999
		-4.8022031249999996e-09 0.19203370312500001 0.16113557812500001
		-5.7230296875000004e-09 0.16113515624999999 0.19203370312500001
		-6.4700015625000009e-09 0.12534117187500002 0.21709729687499996
		-7.0203796874999994e-09 0.085738499999999995 0.23556403124999997
		-7.3574156249999999e-09 0.043530328124999997 0.24687365624999996
		-7.4708999999999991e-09 0 0.25068234375000004
		-0.077465109374999994 0 0.23841295312500005
		-0.14734743750000001 0 0.20280628125
		-0.20280628125 0 0.14734743750000001
		-0.23841295312500005 0 0.077465109374999966
		-0.25068234375000004 0 -3.2092384305570931e-17
		-0.23841295312500005 0 -0.077465109375000035
		-0.20280628125 0 -0.14734743750000001
		-0.14734743750000001 0 -0.20280628125
		-0.077465109374999994 0 -0.23841295312500005
		0 0 -0.25068234375000004
		0.077465109374999994 0 -0.23841295312500005
		0.14734743750000001 0 -0.20280628125
		0.20280628125 0 -0.14734743750000001
		0.23841295312500005 0 -0.077465109375000035
		0.25068192187499999 0 -3.2092384305570931e-17
		0.23841295312500005 0 0.077465109374999966
		0.20280628125 0 0.14734743750000001
		0.14734743750000001 0 0.20280628125
		0.077465109374999994 0 0.23841295312500005
		-7.4708999999999991e-09 0 0.25068234375000004
		;
createNode nurbsCurve -n "L_Foot_HeelMid_Guide_Ctrl_Ctrl_CtrlShape" -p "L_Foot_HeelMid_Guide";
	rename -uid "1E54D738-3747-A1C5-EBE3-EC9D85DACADC";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/C:\\Users\\Esteban\\Documents\\maya\\2022\\scripts\\rigging\\Mutant_Tools\\Icons\\Guide_Data";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 13;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 9 0 no 3
		10 0 1 2 3 4 5 6 7 8 9
		10
		-0.2109375 -0.10546875 -5.8966734375320924e-06
		0.39872714062500003 -0.10796456249999997 -5.8966734375320924e-06
		0.31204110937499996 -0.21365564062499998 -5.8966734375320924e-06
		0.41773218749999996 -0.39620432812499995 -5.8966734375320924e-06
		0.97001803124999997 -1.6344703125e-07 -5.8212421875320918e-06
		0.41773260937500006 0.39620432812499995 -5.8966734375320924e-06
		0.31204110937499996 0.21365521875000001 -5.8966734375320924e-06
		0.39872714062500003 0.10682760937500001 -3.0237721875320927e-06
		-0.2109375 0.10546875 -5.8966734375320924e-06
		-0.2109375 -0.10546875 -5.8966734375320924e-06
		;
createNode nurbsCurve -n "L_Foot_HeelMid_Guide_Ctrl_Ctrl_Ctrl_CtrlShape" -p "L_Foot_HeelMid_Guide";
	rename -uid "A1E66394-4740-A48A-93A4-BEB76E76D7C6";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/C:\\Users\\Esteban\\Documents\\maya\\2022\\scripts\\rigging\\Mutant_Tools\\Icons\\Guide_Data";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 6;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 9 0 no 3
		10 0 1 2 3 4 5 6 7 8 9
		10
		0.10546875 5.8966734375000001e-06 -0.2109375
		0.10796456249999997 5.8966734375000001e-06 0.39872714062500003
		0.21365564062499998 5.8966734375000001e-06 0.31204110937499996
		0.39620432812499995 5.8966734375000001e-06 0.41773218749999996
		1.6344703125e-07 5.8212421874999994e-06 0.97001803124999997
		-0.39620432812499995 5.8966734375000001e-06 0.41773260937500006
		-0.21365521875000001 5.8966734375000001e-06 0.31204110937499996
		-0.10682760937500001 3.0237721875000003e-06 0.39872714062500003
		-0.10546875 5.8966734375000001e-06 -0.2109375
		0.10546875 5.8966734375000001e-06 -0.2109375
		;
createNode dagContainer -n "Smart_RFL_Block" -p "Body";
	rename -uid "3B832BFD-9D4C-F8AA-C22B-B28AFC7CC4C4";
	addAttr -ci true -sn "nts" -ln "notes" -dt "string";
	setAttr ".isc" yes;
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/RFL.png";
	setAttr ".ctor" -type "string" "Esteban";
	setAttr ".cdat" -type "string" "2023/01/24 12:26:55";
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
		"['unitConversion169', 'addDoubleLinear4', 'unitConversion170', 'L_Ankle_Ik_RFL_Ctrl_Grp', 'addDoubleLinear1', 'addDoubleLinear11', 'unitConversion177', 'addDoubleLinear14', 'addDoubleLinear12', 'unitConversion171', 'R_Ankle_Ik_RFL_Reverse', 'unitConversion172', 'unitConversion179', 'R_Ankle_Ik_RFL_Ctrl_Root_Grp', 'addDoubleLinear8', 'addDoubleLinear10', 'unitConversion178', 'R_Ankle_Ik_RFL_Ctrl_GrpMirror_Grp', 'L_Ankle_Ik_RFL_CtrlShape', 'unitConversion173', 'addDoubleLinear9', 'R_Ankle_Ik_RFL_Ctrl_Root_Grp_parentConstraint1', 'unitConversion175', 'unitConversion181', 'addDoubleLinear3', 'R_Ankle_Ik_RFL_Ctrl_Auto_Grp', 'R_Ankle_Ik_RFL_Ctrl_tag', 'R_Ankle_Ik_RFL_Ctrl', 'L_Ankle_Ik_RFL_Ctrl_Auto_Grp', 'R_Ankle_Ik_RFL_CtrlShape', 'unitConversion182', 'L_Ankle_Ik_RFL_Ctrl_Root_Grp_parentConstraint1', 'L_Ankle_Ik_RFL_Ctrl_Root_Grp', 'unitConversion176', 'L_Ankle_Ik_RFL_Reverse', 'L_Ankle_Ik_RFL_Ctrl', 'unitConversion180', 'addDoubleLinear2', 'R_Ankle_Ik_RFL_Ctrl_Root_Grp_scaleConstraint1', 'L_Ankle_Ik_RFL_Ctrl_tag', 'addDoubleLinear13', 'addDoubleLinear6', 'addDoubleLinear7', 'R_Ankle_Ik_RFL_Ctrl_Grp', 'L_Ankle_Ik_RFL_Ctrl_Root_Grp_scaleConstraint1', 'unitConversion174', 'addDoubleLinear5']");
createNode dagContainer -n "L_Smart_RFL_Block" -p "Body";
	rename -uid "EC3972F5-AC43-AC83-42F9-0C81858BDC22";
	addAttr -ci true -sn "nts" -ln "notes" -dt "string";
	setAttr ".isc" yes;
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/FootBox.png";
	setAttr ".ctor" -type "string" "Esteban";
	setAttr ".cdat" -type "string" "2023/06/27 10:39:10";
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
	setAttr ".nts" -type "string" "['R_Smart_RFLAnkle_FootBox_scaleConstraint1', 'L_Smart_RFLAnkle_FootBox_scaleConstraint1', 'R_Smart_RFLBall_FootBox_parentConstraint1', 'transformGeometry1', 'R_Smart_RFLBall_FootBoxMirror_Grp', 'R_Smart_RFLAnkle_FootBox', 'L_Smart_RFLBall_FootBox_parentConstraint1', 'L_Smart_RFLBall_FootBox_scaleConstraint1', 'L_Smart_RFLBall_FootBoxShape', 'R_Smart_RFLBall_FootBoxShape', 'set10', 'set11', 'polyCube2', 'transformGeometry2', 'polyCube1', 'R_Smart_RFLBall_FootBox_scaleConstraint1', 'L_Smart_RFL_Ctrl_Grp', 'set12', 'R_Smart_RFLAnkle_FootBoxMirror_Grp', 'R_Smart_RFL1', 'materialInfo10', 'materialInfo12', 'set9', 'materialInfo9', 'R_Smart_RFLAnkle_FootBox_parentConstraint1', 'R_Smart_RFLBall_FootBox', 'L_Smart_RFLBall_FootBox', 'L_Smart_RFLAnkle_FootBox', 'L_Smart_RFL1', 'materialInfo11', 'L_Smart_RFLAnkle_FootBox_parentConstraint1', 'L_Smart_RFLAnkle_FootBoxShape', 'R_Smart_RFLAnkle_FootBoxShape']";
createNode dagContainer -n "L_FrFoot_Block" -p "Body";
	rename -uid "8B16FCE3-F245-B040-D3CB-E5B164268630";
	addAttr -ci true -sn "nts" -ln "notes" -dt "string";
	setAttr ".isc" yes;
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/Foot.png";
	setAttr ".ctor" -type "string" "PC";
	setAttr ".cdat" -type "string" "2021/09/18 08:41:06";
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
		"['L_FrFoot_Ankle_RFL_Grp_Auto_Grp', 'R_FrFoot_Ankle_Jnt_Toes_SubstractPlusMinAv', 'L_FrFoot_BallToes_Jnt_parentConstraint1', 'R_FrFoot_Out_RFL_Grp', 'L_FrFoot_Out_RFL_Grp_Auto_Grp', 'unitConversion213', 'R_FrFoot_HeelMid_RFL_Grp_Auto_Grp_Offset_Grp', 'L_FrFoot_Toes_Ctrl', 'L_FrFoot_Ball_Jnt_scaleConstraint1', 'unitConversion215', 'R_FrFoot_Ball_RFL_Grp_Auto_Grp', 'R_FrFoot_Heel_RFL_Grp_Root_Grp', 'unitConversion209', 'L_FrFoot_HeelMid_RFL_Grp_Auto_Grp_Offset_Grp', 'L_FrFoot_Ankle_Jnt_Toes_SubstractPlusMinAv1', 'unitConversion193', 'R_FrFoot_Ankle_Bnd_parentConstraint1', 'L_FrFoot_Heel_RFL_Grp_Auto_Grp', 'R_FrFoot_Ball_RFL_Grp_Root_Grp', 'R_FrFoot_Ball_Jnt_parentConstraint1', 'unitConversion189', 'L_FrFoot_Toes_Ik_Jnt', 'L_FrFoot_Ankle_Fk_Jnt_parentConstraint1', 'R_FrFoot_Ball_Ik_Jnt', 'L_FrFoot_Ankle_Bnd', 'unitConversion205', 'unitConversion194', 'effector7', 'R_FrFoot_Toes_RFL_Grp_Auto_Grp', 'unitConversion217', 'R_FrFoot_Toes_Ik_Jnt', 'L_FrFoot_In_RFL_Grp', 'L_FrFoot_Heel_RFL_Grp', 'L_FrFoot_Toes_Ctrl_Offset_Grp_scaleConstraint1', 'R_FrFoot_Ankle_Jnt_Ball_Limit_Condition_MultDiv', 'R_FrFoot_Ankle_RFL_Grp_Auto_Grp', 'L_FrFoot_Out_RFL_Grp_Auto_Grp_Offset_Grp', 'R_FrFoot_Ankle_Jnt_Toes_Limit_Condition', 'R_FrFoot_Ankle_RFL_Grp_Auto_Grp_Offset_Grp', 'L_FrFoot_Ball_RFL_Grp', 'R_FrFoot_Ball_Fk_Jnt', 'R_FrFoot_Ankle_RFL_Grp_Root_Grp', 'L_FrFoot_Ankle_Jnt_scaleConstraint1', 'L_FrFoot_Toes_RFL_Grp_Root_Grp', 'L_FrFoot_Heel_RFL_Grp_Auto_Grp_Offset_Grp', 'R_FrFoot_HeelMid_RFL_Grp_Root_Grp', 'R_FrFoot_Toes_Fk_Jnt', 'L_FrFoot_Toes_RFL_Grp_Auto_Grp', 'L_FrFoot_Toes_Jnt', 'R_FrFoot_BallFloor_RFL_Grp', 'R_FrFoot_HeelMid_RFL_Grp_Auto_Grp', 'R_FrFoot_Ankle_Jnt_Ball_Limit_Condition', 'unitConversion203', 'L_FrFoot_HeelMid_RFL_Grp', 'R_FrFoot_Out_RFL_Grp_Auto_Grp', 'R_FrFoot_Ankle_Jnt_Toes_Limit_Condition1', 'effector6', 'unitConversion184', 'R_FrFoot_Ball_RFL_Grp_Auto_Grp_Offset_Grp', 'R_FrFoot_Ankle_Jnt_BallNegative_Limit_Condition', 'L_FrFoot_Ankle_Ik_IKsc', 'L_FrFoot_Ankle_Ik_Jnt_parentConstraint1', 'R_FrFoot_Toes_Jnt_parentConstraint1', 'effector5', 'L_FrFoot_Toes_Ctrl_Offset_Grp_parentConstraint1', 'L_FrFoot_Ankle_RFL_Grp_Root_Grp', 'L_FrFoot_Ankle_Bnd_parentConstraint1', 'L_FrFoot_BallFloor_RFL_Grp_Auto_Grp_Offset_Grp', 'unitConversion191', 'L_FrFoot_BallToes_Jnt', 'R_FrFoot_Ankle_Ik_Jnt_Reverse', 'L_FrFoot_Ball_Fk_Jnt', 'R_FrFoot_Toes_Ctrl_tag', 'L_FrFoot_In_RFL_Grp_Root_Grp', 'L_FrFoot_Ankle_RFL_Grp', 'unitConversion210', 'R_FrFoot_Ball_Ik_Jnt_Reverse', 'R_FrFoot_Out_RFL_Grp_Root_Grp_parentConstraint1', 'unitConversion212', 'R_FrFoot_Toes_Ctrl', 'unitConversion206', 'L_FrFoot_Ankle_Jnt_parentConstraint1', 'R_FrFoot_Ankle_Jnt_Toes_SubstractPlusMinAv1', 'R_FrFoot_Toes_Ik_Jnt_Reverse', 'L_FrFoot_BallFloor_RFL_Grp_Auto_Grp', 'R_FrFoot_BallToes_Bnd_parentConstraint1', 'unitConversion211', 'unitConversion197', 'L_FrFoot_Ball_RFL_Grp_Auto_Grp_Offset_Grp', 'L_FrFoot_Ball_Ik_Jnt', 'R_FrFoot_Ankle_Ik_Jnt_Reverse1', 'L_FrFoot_Ankle_RFL_Grp_Auto_Grp_Offset_Grp', 'L_FrFoot_Ball_Ik_IKsc', 'L_FrFoot_Ankle_Ik_Jnt_Reverse', 'R_FrFoot_BallToes_Jnt', 'unitConversion188', 'R_FrFoot_Ball_Jnt', 'L_FrFoot_Ball_RFL_Grp_Auto_Grp', 'R_FrFoot_Ankle_Bnd', 'L_FrFoot_Toes_RFL_Grp_Auto_Grp_Offset_Grp', 'R_FrFoot_Ankle_GrpMirror_Grp_scaleConstraint1', 'R_FrFoot_Ankle_Jnt_Toes_Limit_Condition2', 'L_FrFoot_BallToes_Bnd_scaleConstraint1', 'L_FrFoot_Ankle_Jnt_Toes_SubstractPlusMinAv', 'L_FrFoot_Ankle_Bnd_scaleConstraint1', 'R_FrFoot_Ball_Ik_IKsc', 'L_FrFoot_Toes_Ctrl_Offset_Grp', 'R_FrFoot_In_RFL_Grp_Auto_Grp_Offset_Grp', 'R_FrFoot_Ankle_Jnt', 'unitConversion192', 'unitConversion207', 'L_FrFoot_HeelMid_RFL_Grp_Root_Grp', 'L_FrFoot_Ankle_Grp_scaleConstraint1', 'R_FrFoot_Toes_Ik_Jnt_Reverse1', 'L_FrFoot_Toes_Jnt_scaleConstraint1', 'L_FrFoot_Ball_Jnt', 'L_FrFoot_Ball_RFL_Grp_Root_Grp', 'L_FrFoot_Ankle_Fk_Jnt', 'unitConversion208', 'R_FrFoot_Ankle_Fk_Jnt_parentConstraint1', 'R_FrFoot_Toes_Jnt_scaleConstraint1', 'unitConversion190', 'unitConversion183', 'R_FrFoot_Heel_RFL_Grp_Auto_Grp_Offset_Grp', 'L_FrFoot_Ankle_Ik_Jnt', 'R_FrFoot_Toes_CtrlShape', 'R_FrFoot_Ball_Jnt_scaleConstraint1', 'R_FrFoot_Ball_Ik_Jnt_Reverse1', 'unitConversion187', 'L_FrFoot_BallToes_Bnd', 'L_FrFoot_Toes_CtrlShape', 'R_FrFoot_HeelMid_RFL_Grp', 'R_FrFoot_Ankle_Jnt_parentConstraint1', 'R_FrFoot_In_RFL_Grp_Auto_Grp', 'L_FrFoot_Ankle_Grp', 'L_FrFoot_Toes_Ik_Jnt_Reverse1', 'L_FrFoot_Ankle_Jnt_Ball_Limit_Condition', 'R_FrFoot_Out_RFL_Grp_Root_Grp', 'R_FrFoot_BallFloor_RFL_Grp_Auto_Grp', 'L_FrFoot_Heel_RFL_Grp_Root_Grp', 'R_FrFoot_Ankle_Grp', 'L_FrFoot_Ankle_Jnt_Toes_Limit_Condition', 'R_FrFoot_Ankle_RFL_Grp', 'L_FrFoot_In_RFL_Grp_Auto_Grp_Offset_Grp', 'L_FrFoot_Ankle_Jnt_Ball_Limit_Condition_MultDiv', 'R_FrFoot_In_RFL_Grp_Root_Grp', 'R_FrFoot_BallToes_Bnd', 'R_FrFoot_BallFloor_RFL_Grp_Auto_Grp_Offset_Grp', 'R_FrFoot_Toes_Ctrl_Offset_Grp_parentConstraint1', 'R_FrFoot_Ankle_Ik_Jnt', 'unitConversion196', 'R_FrFoot_Toes_RFL_Grp', 'R_FrFoot_BallFloor_RFL_Grp_Root_Grp', 'R_FrFoot_Ankle_Bnd_scaleConstraint1', 'R_FrFoot_Ankle_Fk_Jnt', 'L_FrFoot_Ankle_Jnt_BallNegative_Limit_Condition', 'unitConversion214', 'L_FrFoot_Out_RFL_Grp_Root_Grp', 'L_FrFoot_Ankle_Jnt_Toes_Limit_Condition2', 'L_FrFoot_Ankle_Jnt', 'unitConversion200', 'R_FrFoot_Ball_RFL_Grp', 'R_FrFoot_Ankle_Jnt_scaleConstraint1', 'R_FrFoot_BallToes_Bnd_scaleConstraint1', 'R_FrFoot_Toes_RFL_Grp_Auto_Grp_Offset_Grp', 'L_FrFoot_In_RFL_Grp_Auto_Grp', 'unitConversion202', 'unitConversion195', 'L_FrFoot_Toes_Jnt_parentConstraint1', 'R_FrFoot_Toes_Jnt', 'R_FrFoot_Toes_RFL_Grp_Root_Grp', 'L_FrFoot_Toes_Ctrl_tag', 'L_FrFoot_BallToes_Bnd_parentConstraint1', 'R_FrFoot_Out_RFL_Grp_Auto_Grp_Offset_Grp', 'L_FrFoot_BallFloor_RFL_Grp', 'L_FrFoot_Ball_Ik_Jnt_Reverse', 'R_FrFoot_Ankle_GrpMirror_Grp', 'unitConversion199', 'unitConversion218', 'R_FrFoot_Heel_RFL_Grp', 'R_FrFoot_Toes_Ctrl_Offset_Grp', 'effector8', 'L_FrFoot_Ankle_Jnt_Toes_Limit_Condition1', 'R_FrFoot_In_RFL_Grp', 'L_FrFoot_BallFloor_RFL_Grp_Root_Grp', 'unitConversion216', 'L_FrFoot_HeelMid_RFL_Grp_Auto_Grp', 'R_FrFoot_BallToes_Jnt_parentConstraint1', 'L_FrFoot_Out_RFL_Grp', 'L_FrFoot_Out_RFL_Grp_Root_Grp_parentConstraint1', 'unitConversion201', 'R_FrFoot_Toes_Ctrl_Offset_Grp_scaleConstraint1', 'L_FrFoot_Toes_Ik_Jnt_Reverse', 'L_FrFoot_Ball_Jnt_parentConstraint1', 'unitConversion186', 'L_FrFoot_Toes_Fk_Jnt', 'unitConversion185', 'L_FrFoot_Toes_RFL_Grp', 'R_FrFoot_Heel_RFL_Grp_Auto_Grp', 'L_FrFoot_Ankle_Ik_Jnt_Reverse1', 'R_FrFoot_Ankle_Ik_Jnt_parentConstraint1', 'L_FrFoot_Ball_Ik_Jnt_Reverse1', 'unitConversion204', 'unitConversion198', 'R_FrFoot_Ankle_Ik_IKsc']");
createNode joint -n "L_FrFoot_Ankle_Guide" -p "L_FrFoot_Block";
	rename -uid "24767F51-6543-5960-17A3-B2AB32AC805C";
	addAttr -ci true -sn "Helper" -ln "Helper" -min 0 -max 1 -en "Hide:Show" -at "enum";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/C:\\Users\\Esteban\\Documents\\maya\\2022\\scripts\\rigging\\Mutant_Tools\\Icons\\Guide_Data";
	setAttr ".t" -type "double3" 25.710129698582627 5.5469867608986476 35.079568038317909 ;
	setAttr ".r" -type "double3" 92.216566236606411 39.147613242691115 -88.60021634675752 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".radi" 0.5;
	setAttr -cb on ".Helper" 1;
createNode nurbsCurve -n "L_FrFoot_Ankle_Guide_CtrlShape" -p "L_FrFoot_Ankle_Guide";
	rename -uid "32A58749-7C44-E0CF-A678-C6B954600DA5";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/C:\\Users\\Esteban\\Documents\\maya\\2022\\scripts\\rigging\\Mutant_Tools\\Icons\\Guide_Data";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 14;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 9 0 no 3
		10 0 1 2 3 4 5 6 7 8 9
		10
		5.8966734375641848e-06 -0.21093749999999997 0.10546875000000007
		5.8966734375641848e-06 0.39872714062500003 0.10796456250000004
		5.8966734375641848e-06 0.31204110937499996 0.21365564062500006
		5.8966734375641848e-06 0.41773218749999996 0.39620432812499995
		5.8212421875641842e-06 0.97001803124999997 1.6344703131418477e-07
		5.8966734375641848e-06 0.41773260937500012 -0.39620432812499995
		5.8966734375641848e-06 0.31204110937499996 -0.21365521874999999
		3.0237721875641851e-06 0.39872714062500003 -0.10682760937499994
		5.8966734375641848e-06 -0.21093749999999997 -0.10546874999999993
		5.8966734375641848e-06 -0.21093749999999997 0.10546875000000007
		;
createNode nurbsCurve -n "L_FrFoot_Ankle_Guide_Ctrl_CtrlShape" -p "L_FrFoot_Ankle_Guide";
	rename -uid "1F54E584-794C-1728-4565-C3977B9DD862";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/C:\\Users\\Esteban\\Documents\\maya\\2022\\scripts\\rigging\\Mutant_Tools\\Icons\\Guide_Data";
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
		6.4184768611141862e-17 0.25068192187500005 6.4184768611141862e-17
		-1.2973119670652315e-09 0.24687365625000005 0.043530328125000059
		-2.5551997795652317e-09 0.23556403125000003 0.085738500000000079
		-3.7354541545652313e-09 0.21709729687500001 0.12534117187500007
		-4.802203060815231e-09 0.19203370312500004 0.1611355781250001
		-5.7230296233152317e-09 0.16113515625000008 0.19203370312500004
		-6.4700014983152323e-09 0.12534117187500007 0.21709729687500001
		-7.0203796233152308e-09 0.085738500000000079 0.23556403125000003
		-7.3574155608152312e-09 0.043530328125000059 0.24687365625000005
		-7.4708999358152305e-09 6.4184768611141862e-17 0.25068234375000009
		-7.3574155608152312e-09 -0.043530328124999934 0.24687365625000005
		-7.0203796233152308e-09 -0.08573849999999994 0.23556403125000003
		-6.4700014983152323e-09 -0.12534117187499993 0.21709729687500001
		-5.7230296233152317e-09 -0.16113515624999994 0.19203370312500004
		-4.802203060815231e-09 -0.19203370312499998 0.1611355781250001
		-3.7354541545652313e-09 -0.21709729687499996 0.12534117187500007
		-2.5551997795652317e-09 -0.23556403124999997 0.085738500000000079
		-1.2973119670652315e-09 -0.24687365624999991 0.043530328125000059
		6.4184768611141862e-17 -0.25068192187499994 6.4184768611141862e-17
		6.4184768611141862e-17 -0.24687365624999991 -0.043530328124999934
		6.4184768611141862e-17 -0.23556403124999997 -0.08573849999999994
		6.4184768611141862e-17 -0.21709729687499996 -0.12534117187499993
		6.4184768611141862e-17 -0.19203370312499998 -0.16113557812499993
		6.4184768611141862e-17 -0.16113515624999994 -0.19203370312499998
		6.4184768611141862e-17 -0.12534117187499993 -0.21709729687499996
		6.4184768611141862e-17 -0.08573849999999994 -0.23556445312499999
		6.4184768611141862e-17 -0.043530328124999934 -0.24687365624999991
		6.4184768611141862e-17 6.4184768611141862e-17 -0.25068234374999998
		6.4184768611141862e-17 0.043530328125000059 -0.24687365624999991
		6.4184768611141862e-17 0.085738500000000079 -0.23556445312499999
		6.4184768611141862e-17 0.12534117187500007 -0.21709729687499996
		6.4184768611141862e-17 0.16113515625000008 -0.19203370312499998
		6.4184768611141862e-17 0.19203370312500004 -0.16113557812499993
		6.4184768611141862e-17 0.21709729687500001 -0.12534117187499993
		6.4184768611141862e-17 0.23556403125000003 -0.08573849999999994
		6.4184768611141862e-17 0.24687365625000005 -0.043530328124999934
		6.4184768611141862e-17 0.25068192187500005 6.4184768611141862e-17
		0.043530328125000059 0.24687365625000005 6.4184768611141862e-17
		0.085738500000000079 0.23556403125000003 6.4184768611141862e-17
		0.12534117187500007 0.21709729687500001 6.4184768611141862e-17
		0.1611355781250001 0.19203370312500004 6.4184768611141862e-17
		0.19203370312500004 0.16113515625000008 6.4184768611141862e-17
		0.21709729687500001 0.12534117187500007 6.4184768611141862e-17
		0.23556403125000003 0.085738500000000079 6.4184768611141862e-17
		0.24687365625000005 0.043530328125000059 6.4184768611141862e-17
		0.25068192187500005 6.4184768611141862e-17 6.4184768611141862e-17
		0.24687365625000005 -0.043530328124999934 6.4184768611141862e-17
		0.23556403125000003 -0.08573849999999994 6.4184768611141862e-17
		0.21709729687500001 -0.12534117187499993 6.4184768611141862e-17
		0.19203370312500004 -0.16113515624999994 6.4184768611141862e-17
		0.1611355781250001 -0.19203370312499998 6.4184768611141862e-17
		0.12534117187500007 -0.21709729687499996 6.4184768611141862e-17
		0.085738500000000079 -0.23556403124999997 6.4184768611141862e-17
		0.043530328125000059 -0.24687365624999991 6.4184768611141862e-17
		6.4184768611141862e-17 -0.25068192187499994 6.4184768611141862e-17
		-0.043530328124999934 -0.24687365624999991 6.4184768611141862e-17
		-0.08573849999999994 -0.23556403124999997 6.4184768611141862e-17
		-0.12534117187499993 -0.21709729687499996 6.4184768611141862e-17
		-0.16113557812499993 -0.19203370312499998 6.4184768611141862e-17
		-0.19203370312499998 -0.16113515624999994 6.4184768611141862e-17
		-0.21709729687499996 -0.12534117187499993 6.4184768611141862e-17
		-0.23556403124999997 -0.08573849999999994 6.4184768611141862e-17
		-0.24687365624999991 -0.043530328124999934 6.4184768611141862e-17
		-0.25068234374999998 6.4184768611141862e-17 6.4184768611141862e-17
		-0.24687365624999991 0.043530328125000059 6.4184768611141862e-17
		-0.23556403124999997 0.085738500000000079 6.4184768611141862e-17
		-0.21709729687499996 0.12534117187500007 6.4184768611141862e-17
		-0.19203370312499998 0.16113515625000008 6.4184768611141862e-17
		-0.16113557812499993 0.19203370312500004 6.4184768611141862e-17
		-0.12534117187499993 0.21709729687500001 6.4184768611141862e-17
		-0.08573849999999994 0.23556403125000003 6.4184768611141862e-17
		-0.043530328124999934 0.24687365625000005 6.4184768611141862e-17
		6.4184768611141862e-17 0.25068192187500005 6.4184768611141862e-17
		-1.2973119670652315e-09 0.24687365625000005 0.043530328125000059
		-2.5551997795652317e-09 0.23556403125000003 0.085738500000000079
		-3.7354541545652313e-09 0.21709729687500001 0.12534117187500007
		-4.802203060815231e-09 0.19203370312500004 0.1611355781250001
		-5.7230296233152317e-09 0.16113515625000008 0.19203370312500004
		-6.4700014983152323e-09 0.12534117187500007 0.21709729687500001
		-7.0203796233152308e-09 0.085738500000000079 0.23556403125000003
		-7.3574155608152312e-09 0.043530328125000059 0.24687365625000005
		-7.4708999358152305e-09 6.4184768611141862e-17 0.25068234375000009
		-0.077465109374999938 6.4184768611141862e-17 0.2384129531250001
		-0.14734743749999998 6.4184768611141862e-17 0.20280628125000005
		-0.20280628124999991 6.4184768611141862e-17 0.14734743750000007
		-0.23841295312499997 6.4184768611141862e-17 0.077465109375000063
		-0.25068234374999998 6.4184768611141862e-17 6.4184768611141862e-17
		-0.23841295312499997 6.4184768611141862e-17 -0.077465109374999938
		-0.20280628124999991 6.4184768611141862e-17 -0.14734743749999998
		-0.14734743749999998 6.4184768611141862e-17 -0.20280628124999991
		-0.077465109374999938 6.4184768611141862e-17 -0.23841295312499997
		6.4184768611141862e-17 6.4184768611141862e-17 -0.25068234374999998
		0.077465109375000063 6.4184768611141862e-17 -0.23841295312499997
		0.14734743750000007 6.4184768611141862e-17 -0.20280628124999991
		0.20280628125000005 6.4184768611141862e-17 -0.14734743749999998
		0.2384129531250001 6.4184768611141862e-17 -0.077465109374999938
		0.25068192187500005 6.4184768611141862e-17 6.4184768611141862e-17
		0.2384129531250001 6.4184768611141862e-17 0.077465109375000063
		0.20280628125000005 6.4184768611141862e-17 0.14734743750000007
		0.14734743750000007 6.4184768611141862e-17 0.20280628125000005
		0.077465109375000063 6.4184768611141862e-17 0.2384129531250001
		-7.4708999358152305e-09 6.4184768611141862e-17 0.25068234375000009
		;
createNode nurbsCurve -n "L_FrFoot_Ankle_Guide_Ctrl_Ctrl_CtrlShape" -p "L_FrFoot_Ankle_Guide";
	rename -uid "B49E20AA-3A42-BBE1-68D0-A5ACA34C625B";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/C:\\Users\\Esteban\\Documents\\maya\\2022\\scripts\\rigging\\Mutant_Tools\\Icons\\Guide_Data";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 13;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 9 0 no 3
		10 0 1 2 3 4 5 6 7 8 9
		10
		-0.21093749999999997 -0.10546874999999993 -5.8966734374358153e-06
		0.39872714062500003 -0.10796456249999992 -5.8966734374358153e-06
		0.31204110937499996 -0.21365564062499992 -5.8966734374358153e-06
		0.41773218749999996 -0.39620432812499995 -5.8966734374358153e-06
		0.97001803124999997 -1.6344703118581523e-07 -5.8212421874358146e-06
		0.41773260937500012 0.39620432812499995 -5.8966734374358153e-06
		0.31204110937499996 0.21365521875000004 -5.8966734374358153e-06
		0.39872714062500003 0.10682760937500005 -3.0237721874358156e-06
		-0.21093749999999997 0.10546875000000007 -5.8966734374358153e-06
		-0.21093749999999997 -0.10546874999999993 -5.8966734374358153e-06
		;
createNode nurbsCurve -n "L_FrFoot_Ankle_Guide_Ctrl_Ctrl_Ctrl_CtrlShape" -p "L_FrFoot_Ankle_Guide";
	rename -uid "45C69BD2-A54C-0B57-5B13-7C8C4087AFCC";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/C:\\Users\\Esteban\\Documents\\maya\\2022\\scripts\\rigging\\Mutant_Tools\\Icons\\Guide_Data";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 6;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 9 0 no 3
		10 0 1 2 3 4 5 6 7 8 9
		10
		0.10546875000000007 5.8966734375641848e-06 -0.21093749999999997
		0.10796456250000004 5.8966734375641848e-06 0.39872714062500003
		0.21365564062500006 5.8966734375641848e-06 0.31204110937499996
		0.39620432812499995 5.8966734375641848e-06 0.41773218749999996
		1.6344703131418477e-07 5.8212421875641842e-06 0.97001803124999997
		-0.39620432812499995 5.8966734375641848e-06 0.41773260937500012
		-0.21365521874999999 5.8966734375641848e-06 0.31204110937499996
		-0.10682760937499994 3.0237721875641851e-06 0.39872714062500003
		-0.10546874999999993 5.8966734375641848e-06 -0.21093749999999997
		0.10546875000000007 5.8966734375641848e-06 -0.21093749999999997
		;
createNode joint -n "L_FrFoot_Heel_Guide" -p "L_FrFoot_Ankle_Guide";
	rename -uid "0AEF1994-9D49-27EA-F343-2682DD1E9390";
	addAttr -ci true -sn "Helper" -ln "Helper" -min 0 -max 1 -en "Hide:Show" -at "enum";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/C:\\Users\\Esteban\\Documents\\maya\\2022\\scripts\\rigging\\Mutant_Tools\\Icons\\Guide_Data";
	setAttr ".t" -type "double3" 8.8325846317065668 -2.2777058896432822 0.47121656848232613 ;
	setAttr ".r" -type "double3" -4.4132147435210811 1.7137318008143982 -0.13224212445467148 ;
	setAttr ".s" -type "double3" 0.99999999999999978 0.99999999999999978 0.99999999999999944 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" -124.75737512881491 89.999999999999886 0 ;
	setAttr ".radi" 0.5;
	setAttr -cb on ".Helper";
createNode nurbsCurve -n "L_FrFoot_Heel_Guide_CtrlShape" -p "L_FrFoot_Heel_Guide";
	rename -uid "BD12CE09-8D49-4B0A-2AF8-529657A7E32B";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/C:\\Users\\Esteban\\Documents\\maya\\2022\\scripts\\rigging\\Mutant_Tools\\Icons\\Guide_Data";
	setAttr -k off ".v" no;
	setAttr ".ove" yes;
	setAttr ".ovc" 14;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 9 0 no 3
		10 0 1 2 3 4 5 6 7 8 9
		10
		5.8966734374358153e-06 -0.2109375 0.10546875
		5.8966734374358153e-06 0.39872714062500003 0.10796456249999997
		5.8966734374358153e-06 0.31204110937499996 0.21365564062499998
		5.8966734374358153e-06 0.41773218749999996 0.39620432812499995
		5.8212421874358146e-06 0.97001803124999997 1.6344703125e-07
		5.8966734374358153e-06 0.41773260937500006 -0.39620432812499995
		5.8966734374358153e-06 0.31204110937499996 -0.21365521875000001
		3.0237721874358156e-06 0.39872714062500003 -0.10682760937500001
		5.8966734374358153e-06 -0.2109375 -0.10546875
		5.8966734374358153e-06 -0.2109375 0.10546875
		;
createNode nurbsCurve -n "L_FrFoot_Heel_Guide_Ctrl_CtrlShape" -p "L_FrFoot_Heel_Guide";
	rename -uid "6F4E6EA4-BA45-BEE5-03DF-9EB32372536E";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/C:\\Users\\Esteban\\Documents\\maya\\2022\\scripts\\rigging\\Mutant_Tools\\Icons\\Guide_Data";
	setAttr -k off ".v" no;
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
		-6.4184768611141862e-17 0.25068192187499999 0
		-1.2973120954347687e-09 0.24687365624999996 0.043530328124999997
		-2.5551999079347689e-09 0.23556403125 0.085738499999999995
		-3.7354542829347686e-09 0.21709729687499998 0.12534117187500002
		-4.8022031891847682e-09 0.19203370312500001 0.16113557812500001
		-5.723029751684769e-09 0.16113515624999999 0.19203370312500001
		-6.4700016266847695e-09 0.12534117187500002 0.21709729687499998
		-7.020379751684768e-09 0.085738499999999995 0.23556403125
		-7.3574156891847685e-09 0.043530328124999983 0.24687365624999996
		-7.4709000641847677e-09 -1.6046192152785466e-17 0.25068234375000004
		-7.3574156891847685e-09 -0.04353032812500001 0.24687365624999996
		-7.020379751684768e-09 -0.085738499999999995 0.23556403125
		-6.4700016266847695e-09 -0.12534117187500002 0.21709729687499998
		-5.723029751684769e-09 -0.16113515624999999 0.19203370312500001
		-4.8022031891847682e-09 -0.19203370312500001 0.16113557812500001
		-3.7354542829347686e-09 -0.21709729687499998 0.12534117187500002
		-2.5551999079347689e-09 -0.23556403125 0.085738499999999995
		-1.2973120954347687e-09 -0.24687365624999996 0.043530328124999997
		-6.4184768611141862e-17 -0.25068192187499999 0
		-6.4184768611141862e-17 -0.24687365624999996 -0.043530328124999997
		-6.4184768611141862e-17 -0.23556403125 -0.085738499999999995
		-6.4184768611141862e-17 -0.21709729687499998 -0.12534117187500002
		-6.4184768611141862e-17 -0.19203370312500001 -0.16113557812500001
		-6.4184768611141862e-17 -0.16113515624999999 -0.19203370312500001
		-6.4184768611141862e-17 -0.12534117187500002 -0.21709729687499998
		-6.4184768611141862e-17 -0.085738499999999995 -0.23556445312500002
		-6.4184768611141862e-17 -0.04353032812500001 -0.24687365624999996
		-6.4184768611141862e-17 -1.6046192152785466e-17 -0.25068234375000004
		-6.4184768611141862e-17 0.043530328124999983 -0.24687365624999996
		-6.4184768611141862e-17 0.085738499999999995 -0.23556445312500002
		-6.4184768611141862e-17 0.12534117187500002 -0.21709729687499998
		-6.4184768611141862e-17 0.16113515624999999 -0.19203370312500001
		-6.4184768611141862e-17 0.19203370312500001 -0.16113557812500001
		-6.4184768611141862e-17 0.21709729687499998 -0.12534117187500002
		-6.4184768611141862e-17 0.23556403125 -0.085738499999999995
		-6.4184768611141862e-17 0.24687365624999996 -0.043530328124999997
		-6.4184768611141862e-17 0.25068192187499999 0
		0.043530328124999934 0.24687365624999996 0
		0.08573849999999994 0.23556403125 0
		0.12534117187499993 0.21709729687499998 0
		0.16113557812499993 0.19203370312500001 0
		0.19203370312499998 0.16113515624999999 0
		0.21709729687499996 0.12534117187500002 0
		0.23556403124999997 0.085738499999999995 0
		0.24687365624999991 0.043530328124999983 0
		0.25068192187499994 -1.6046192152785466e-17 0
		0.24687365624999991 -0.04353032812500001 0
		0.23556403124999997 -0.085738499999999995 0
		0.21709729687499996 -0.12534117187500002 0
		0.19203370312499998 -0.16113515624999999 0
		0.16113557812499993 -0.19203370312500001 0
		0.12534117187499993 -0.21709729687499998 0
		0.08573849999999994 -0.23556403125 0
		0.043530328124999934 -0.24687365624999996 0
		-6.4184768611141862e-17 -0.25068192187499999 0
		-0.043530328125000059 -0.24687365624999996 0
		-0.085738500000000079 -0.23556403125 0
		-0.12534117187500007 -0.21709729687499998 0
		-0.1611355781250001 -0.19203370312500001 0
		-0.19203370312500004 -0.16113515624999999 0
		-0.21709729687500001 -0.12534117187500002 0
		-0.23556403125000003 -0.085738499999999995 0
		-0.24687365625000005 -0.04353032812500001 0
		-0.25068234375000009 -1.6046192152785466e-17 0
		-0.24687365625000005 0.043530328124999983 0
		-0.23556403125000003 0.085738499999999995 0
		-0.21709729687500001 0.12534117187500002 0
		-0.19203370312500004 0.16113515624999999 0
		-0.1611355781250001 0.19203370312500001 0
		-0.12534117187500007 0.21709729687499998 0
		-0.085738500000000079 0.23556403125 0
		-0.043530328125000059 0.24687365624999996 0
		-6.4184768611141862e-17 0.25068192187499999 0
		-1.2973120954347687e-09 0.24687365624999996 0.043530328124999997
		-2.5551999079347689e-09 0.23556403125 0.085738499999999995
		-3.7354542829347686e-09 0.21709729687499998 0.12534117187500002
		-4.8022031891847682e-09 0.19203370312500001 0.16113557812500001
		-5.723029751684769e-09 0.16113515624999999 0.19203370312500001
		-6.4700016266847695e-09 0.12534117187500002 0.21709729687499998
		-7.020379751684768e-09 0.085738499999999995 0.23556403125
		-7.3574156891847685e-09 0.043530328124999983 0.24687365624999996
		-7.4709000641847677e-09 -1.6046192152785466e-17 0.25068234375000004
		-0.077465109375000063 -1.6046192152785466e-17 0.23841295312500005
		-0.14734743750000007 -1.6046192152785466e-17 0.20280628125
		-0.20280628125000005 -1.6046192152785466e-17 0.14734743750000001
		-0.2384129531250001 -1.6046192152785466e-17 0.077465109374999994
		-0.25068234375000009 -1.6046192152785466e-17 0
		-0.2384129531250001 -1.6046192152785466e-17 -0.077465109374999994
		-0.20280628125000005 -1.6046192152785466e-17 -0.14734743750000001
		-0.14734743750000007 -1.6046192152785466e-17 -0.20280628125
		-0.077465109375000063 -1.6046192152785466e-17 -0.23841295312500005
		-6.4184768611141862e-17 -1.6046192152785466e-17 -0.25068234375000004
		0.077465109374999938 -1.6046192152785466e-17 -0.23841295312500005
		0.14734743749999998 -1.6046192152785466e-17 -0.20280628125
		0.20280628124999991 -1.6046192152785466e-17 -0.14734743750000001
		0.23841295312499997 -1.6046192152785466e-17 -0.077465109374999994
		0.25068192187499994 -1.6046192152785466e-17 0
		0.23841295312499997 -1.6046192152785466e-17 0.077465109374999994
		0.20280628124999991 -1.6046192152785466e-17 0.14734743750000001
		0.14734743749999998 -1.6046192152785466e-17 0.20280628125
		0.077465109374999938 -1.6046192152785466e-17 0.23841295312500005
		-7.4709000641847677e-09 -1.6046192152785466e-17 0.25068234375000004
		;
createNode nurbsCurve -n "L_FrFoot_Heel_Guide_Ctrl_Ctrl_CtrlShape" -p "L_FrFoot_Heel_Guide";
	rename -uid "EF865E16-B24D-75FE-A2B4-A5B2182F3308";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/C:\\Users\\Esteban\\Documents\\maya\\2022\\scripts\\rigging\\Mutant_Tools\\Icons\\Guide_Data";
	setAttr -k off ".v" no;
	setAttr ".ove" yes;
	setAttr ".ovc" 13;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 9 0 no 3
		10 0 1 2 3 4 5 6 7 8 9
		10
		-0.21093750000000003 -0.10546875 -5.8966734375000001e-06
		0.39872714062500003 -0.10796456249999997 -5.8966734375000001e-06
		0.31204110937499996 -0.21365564062499998 -5.8966734375000001e-06
		0.41773218749999996 -0.39620432812499995 -5.8966734375000001e-06
		0.97001803124999997 -1.6344703126604619e-07 -5.8212421874999994e-06
		0.41773260937500001 0.39620432812499995 -5.8966734375000001e-06
		0.31204110937499996 0.21365521875000001 -5.8966734375000001e-06
		0.39872714062500003 0.10682760937499999 -3.0237721875000003e-06
		-0.21093750000000003 0.10546875 -5.8966734375000001e-06
		-0.21093750000000003 -0.10546875 -5.8966734375000001e-06
		;
createNode nurbsCurve -n "L_FrFoot_Heel_Guide_Ctrl_Ctrl_Ctrl_CtrlShape" -p "L_FrFoot_Heel_Guide";
	rename -uid "9A1488CF-3843-5D1F-1941-6986FEE9B41D";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/C:\\Users\\Esteban\\Documents\\maya\\2022\\scripts\\rigging\\Mutant_Tools\\Icons\\Guide_Data";
	setAttr -k off ".v" no;
	setAttr ".ove" yes;
	setAttr ".ovc" 6;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 9 0 no 3
		10 0 1 2 3 4 5 6 7 8 9
		10
		0.10546874999999993 5.8966734374839539e-06 -0.2109375
		0.10796456249999992 5.8966734374839539e-06 0.39872714062500003
		0.21365564062499992 5.8966734374839539e-06 0.31204110937499996
		0.39620432812499995 5.8966734374839539e-06 0.41773218749999996
		1.6344703118581523e-07 5.8212421874839532e-06 0.97001803124999997
		-0.39620432812499995 5.8966734374839539e-06 0.41773260937500006
		-0.21365521875000004 5.8966734374839539e-06 0.31204110937499996
		-0.10682760937500005 3.0237721874839541e-06 0.39872714062500003
		-0.10546875000000007 5.8966734374839539e-06 -0.2109375
		0.10546874999999993 5.8966734374839539e-06 -0.2109375
		;
createNode joint -n "L_FrFoot_Ball_Guide" -p "L_FrFoot_Ankle_Guide";
	rename -uid "94FFE8CD-4545-EF2F-6028-B0A9C0699FFC";
	addAttr -ci true -sn "Helper" -ln "Helper" -min 0 -max 1 -en "Hide:Show" -at "enum";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/C:\\Users\\Esteban\\Documents\\maya\\2022\\scripts\\rigging\\Mutant_Tools\\Icons\\Guide_Data";
	setAttr ".t" -type "double3" 0.080694680162652022 2.1139366554610914 -7.8981959861223522e-15 ;
	setAttr ".r" -type "double3" -6.3560373247787974e-14 6.1311381464590445e-14 89.999999999999943 ;
	setAttr ".s" -type "double3" 0.99999999999999978 0.99999999999999978 0.99999999999999944 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" -2.0673605429512854e-14 1.2722218725854064e-14 -6.361109362927032e-15 ;
	setAttr ".radi" 0.5;
	setAttr -cb on ".Helper";
createNode nurbsCurve -n "L_FrFoot_Ball_Guide_CtrlShape" -p "L_FrFoot_Ball_Guide";
	rename -uid "05A98F45-774B-6BED-4510-2C9DA566743C";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/C:\\Users\\Esteban\\Documents\\maya\\2022\\scripts\\rigging\\Mutant_Tools\\Icons\\Guide_Data";
	setAttr -k off ".v" no;
	setAttr ".ove" yes;
	setAttr ".ovc" 14;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 9 0 no 3
		10 0 1 2 3 4 5 6 7 8 9
		10
		5.8966734375000001e-06 -0.2109375 0.10546875
		5.8966734375000001e-06 0.39872714062500003 0.10796456249999997
		5.8966734375000001e-06 0.31204110937499996 0.21365564062499998
		5.8966734375000001e-06 0.41773218749999996 0.39620432812499995
		5.8212421874999994e-06 0.97001803124999997 1.6344703125e-07
		5.8966734375000001e-06 0.41773260937500006 -0.39620432812499995
		5.8966734375000001e-06 0.31204110937499996 -0.21365521875000001
		3.0237721875000003e-06 0.39872714062500003 -0.10682760937500001
		5.8966734375000001e-06 -0.2109375 -0.10546875
		5.8966734375000001e-06 -0.2109375 0.10546875
		;
createNode nurbsCurve -n "L_FrFoot_Ball_Guide_Ctrl_CtrlShape" -p "L_FrFoot_Ball_Guide";
	rename -uid "1AE72919-6545-B4B3-A78B-CF81D545F32E";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/C:\\Users\\Esteban\\Documents\\maya\\2022\\scripts\\rigging\\Mutant_Tools\\Icons\\Guide_Data";
	setAttr -k off ".v" no;
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
		0 0.25068192187499999 0
		-1.2973120312500001e-09 0.24687365624999996 0.043530328124999997
		-2.5551998437500003e-09 0.23556403125 0.085738499999999995
		-3.73545421875e-09 0.21709729687499998 0.12534117187500002
		-4.8022031249999996e-09 0.19203370312500001 0.16113557812500001
		-5.7230296875000004e-09 0.16113515624999999 0.19203370312500001
		-6.4700015625000009e-09 0.12534117187500002 0.21709729687499998
		-7.0203796874999994e-09 0.085738499999999995 0.23556403125
		-7.3574156249999999e-09 0.043530328124999997 0.24687365624999996
		-7.4708999999999991e-09 0 0.25068234375000004
		-7.3574156249999999e-09 -0.043530328124999997 0.24687365624999996
		-7.0203796874999994e-09 -0.085738499999999995 0.23556403125
		-6.4700015625000009e-09 -0.12534117187500002 0.21709729687499998
		-5.7230296875000004e-09 -0.16113515624999999 0.19203370312500001
		-4.8022031249999996e-09 -0.19203370312500001 0.16113557812500001
		-3.73545421875e-09 -0.21709729687499998 0.12534117187500002
		-2.5551998437500003e-09 -0.23556403125 0.085738499999999995
		-1.2973120312500001e-09 -0.24687365624999996 0.043530328124999997
		0 -0.25068192187499999 0
		0 -0.24687365624999996 -0.043530328124999997
		0 -0.23556403125 -0.085738499999999995
		0 -0.21709729687499998 -0.12534117187500002
		0 -0.19203370312500001 -0.16113557812500001
		0 -0.16113515624999999 -0.19203370312500001
		0 -0.12534117187500002 -0.21709729687499998
		0 -0.085738499999999995 -0.23556445312500002
		0 -0.043530328124999997 -0.24687365624999996
		0 0 -0.25068234375000004
		0 0.043530328124999997 -0.24687365624999996
		0 0.085738499999999995 -0.23556445312500002
		0 0.12534117187500002 -0.21709729687499998
		0 0.16113515624999999 -0.19203370312500001
		0 0.19203370312500001 -0.16113557812500001
		0 0.21709729687499998 -0.12534117187500002
		0 0.23556403125 -0.085738499999999995
		0 0.24687365624999996 -0.043530328124999997
		0 0.25068192187499999 0
		0.043530328124999997 0.24687365624999996 0
		0.085738499999999995 0.23556403125 0
		0.12534117187500002 0.21709729687499998 0
		0.16113557812500001 0.19203370312500001 0
		0.19203370312500001 0.16113515624999999 0
		0.21709729687499998 0.12534117187500002 0
		0.23556403125 0.085738499999999995 0
		0.24687365624999996 0.043530328124999997 0
		0.25068192187499999 0 0
		0.24687365624999996 -0.043530328124999997 0
		0.23556403125 -0.085738499999999995 0
		0.21709729687499998 -0.12534117187500002 0
		0.19203370312500001 -0.16113515624999999 0
		0.16113557812500001 -0.19203370312500001 0
		0.12534117187500002 -0.21709729687499998 0
		0.085738499999999995 -0.23556403125 0
		0.043530328124999997 -0.24687365624999996 0
		0 -0.25068192187499999 0
		-0.043530328124999997 -0.24687365624999996 0
		-0.085738499999999995 -0.23556403125 0
		-0.12534117187500002 -0.21709729687499998 0
		-0.16113557812500001 -0.19203370312500001 0
		-0.19203370312500001 -0.16113515624999999 0
		-0.21709729687499998 -0.12534117187500002 0
		-0.23556403125 -0.085738499999999995 0
		-0.24687365624999996 -0.043530328124999997 0
		-0.25068234375000004 0 0
		-0.24687365624999996 0.043530328124999997 0
		-0.23556403125 0.085738499999999995 0
		-0.21709729687499998 0.12534117187500002 0
		-0.19203370312500001 0.16113515624999999 0
		-0.16113557812500001 0.19203370312500001 0
		-0.12534117187500002 0.21709729687499998 0
		-0.085738499999999995 0.23556403125 0
		-0.043530328124999997 0.24687365624999996 0
		0 0.25068192187499999 0
		-1.2973120312500001e-09 0.24687365624999996 0.043530328124999997
		-2.5551998437500003e-09 0.23556403125 0.085738499999999995
		-3.73545421875e-09 0.21709729687499998 0.12534117187500002
		-4.8022031249999996e-09 0.19203370312500001 0.16113557812500001
		-5.7230296875000004e-09 0.16113515624999999 0.19203370312500001
		-6.4700015625000009e-09 0.12534117187500002 0.21709729687499998
		-7.0203796874999994e-09 0.085738499999999995 0.23556403125
		-7.3574156249999999e-09 0.043530328124999997 0.24687365624999996
		-7.4708999999999991e-09 0 0.25068234375000004
		-0.077465109374999994 0 0.23841295312500005
		-0.14734743750000001 0 0.20280628125
		-0.20280628125 0 0.14734743750000001
		-0.23841295312500005 0 0.077465109374999994
		-0.25068234375000004 0 0
		-0.23841295312500005 0 -0.077465109374999994
		-0.20280628125 0 -0.14734743750000001
		-0.14734743750000001 0 -0.20280628125
		-0.077465109374999994 0 -0.23841295312500005
		0 0 -0.25068234375000004
		0.077465109374999994 0 -0.23841295312500005
		0.14734743750000001 0 -0.20280628125
		0.20280628125 0 -0.14734743750000001
		0.23841295312500005 0 -0.077465109374999994
		0.25068192187499999 0 0
		0.23841295312500005 0 0.077465109374999994
		0.20280628125 0 0.14734743750000001
		0.14734743750000001 0 0.20280628125
		0.077465109374999994 0 0.23841295312500005
		-7.4708999999999991e-09 0 0.25068234375000004
		;
createNode nurbsCurve -n "L_FrFoot_Ball_Guide_Ctrl_Ctrl_CtrlShape" -p "L_FrFoot_Ball_Guide";
	rename -uid "84A0E1C6-194C-ABC0-4FFF-ED9D56DA9022";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/C:\\Users\\Esteban\\Documents\\maya\\2022\\scripts\\rigging\\Mutant_Tools\\Icons\\Guide_Data";
	setAttr -k off ".v" no;
	setAttr ".ove" yes;
	setAttr ".ovc" 13;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 9 0 no 3
		10 0 1 2 3 4 5 6 7 8 9
		10
		-0.2109375 -0.10546875 -5.8966734375000001e-06
		0.39872714062500003 -0.10796456249999997 -5.8966734375000001e-06
		0.31204110937499996 -0.21365564062499998 -5.8966734375000001e-06
		0.41773218749999996 -0.39620432812499995 -5.8966734375000001e-06
		0.97001803124999997 -1.6344703125e-07 -5.8212421874999994e-06
		0.41773260937500006 0.39620432812499995 -5.8966734375000001e-06
		0.31204110937499996 0.21365521875000001 -5.8966734375000001e-06
		0.39872714062500003 0.10682760937500001 -3.0237721875000003e-06
		-0.2109375 0.10546875 -5.8966734375000001e-06
		-0.2109375 -0.10546875 -5.8966734375000001e-06
		;
createNode nurbsCurve -n "L_FrFoot_Ball_Guide_Ctrl_Ctrl_Ctrl_CtrlShape" -p "L_FrFoot_Ball_Guide";
	rename -uid "AB054EB2-4D4A-2F6F-55D3-2691BDC30E88";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/C:\\Users\\Esteban\\Documents\\maya\\2022\\scripts\\rigging\\Mutant_Tools\\Icons\\Guide_Data";
	setAttr -k off ".v" no;
	setAttr ".ove" yes;
	setAttr ".ovc" 6;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 9 0 no 3
		10 0 1 2 3 4 5 6 7 8 9
		10
		0.10546875 5.8966734375000001e-06 -0.2109375
		0.10796456249999997 5.8966734375000001e-06 0.39872714062500003
		0.21365564062499998 5.8966734375000001e-06 0.31204110937499996
		0.39620432812499995 5.8966734375000001e-06 0.41773218749999996
		1.6344703125e-07 5.8212421874999994e-06 0.97001803124999997
		-0.39620432812499995 5.8966734375000001e-06 0.41773260937500006
		-0.21365521875000001 5.8966734375000001e-06 0.31204110937499996
		-0.10682760937500001 3.0237721875000003e-06 0.39872714062500003
		-0.10546875 5.8966734375000001e-06 -0.2109375
		0.10546875 5.8966734375000001e-06 -0.2109375
		;
createNode joint -n "L_FrFoot_BallFloor_Guide" -p "L_FrFoot_Ball_Guide";
	rename -uid "66B81497-CE4E-CA73-C35E-0B9EE349F9A0";
	addAttr -ci true -sn "Helper" -ln "Helper" -min 0 -max 1 -en "Hide:Show" -at "enum";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/C:\\Users\\Esteban\\Documents\\maya\\2022\\scripts\\rigging\\Mutant_Tools\\Icons\\Guide_Data";
	setAttr ".t" -type "double3" 3.5081955508958762 -2.3161423873536542 0.16544788182698275 ;
	setAttr ".r" -type "double3" 89.999999999984738 -91.718825019958985 206.16861202569621 ;
	setAttr ".s" -type "double3" 1.0000000000000004 1 1 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" -1.9296866305920366e-14 -1.590277340731758e-15 13.00000000000002 ;
	setAttr ".radi" 0.5;
	setAttr -cb on ".Helper";
createNode nurbsCurve -n "L_FrFoot_BallFloor_Guide_CtrlShape" -p "L_FrFoot_BallFloor_Guide";
	rename -uid "BFEF81F4-1F49-83A1-7357-2D83CC3F0E00";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/C:\\Users\\Esteban\\Documents\\maya\\2022\\scripts\\rigging\\Mutant_Tools\\Icons\\Guide_Data";
	setAttr -k off ".v" no;
	setAttr ".ove" yes;
	setAttr ".ovc" 14;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 9 0 no 3
		10 0 1 2 3 4 5 6 7 8 9
		10
		5.8966734375000001e-06 -0.21093750000000014 0.10546875000000001
		5.8966734375000001e-06 0.39872714062499992 0.10796456249999999
		5.8966734375000001e-06 0.3120411093749999 0.21365564062499998
		5.8966734375000001e-06 0.41773218749999991 0.39620432812499995
		5.8212421874999994e-06 0.97001803124999997 1.6344703128209239e-07
		5.8966734375000001e-06 0.41773260937500001 -0.39620432812499995
		5.8966734375000001e-06 0.3120411093749999 -0.21365521874999999
		3.0237721875000003e-06 0.39872714062499992 -0.10682760937499999
		5.8966734375000001e-06 -0.21093750000000014 -0.10546874999999999
		5.8966734375000001e-06 -0.21093750000000014 0.10546875000000001
		;
createNode nurbsCurve -n "L_FrFoot_BallFloor_Guide_Ctrl_CtrlShape" -p "L_FrFoot_BallFloor_Guide";
	rename -uid "FBBA9222-094D-B226-61E1-06994DC5DD4F";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/C:\\Users\\Esteban\\Documents\\maya\\2022\\scripts\\rigging\\Mutant_Tools\\Icons\\Guide_Data";
	setAttr -k off ".v" no;
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
		0 0.25068192187499988 3.2092384305570931e-17
		-1.2973120312500001e-09 0.24687365624999985 0.043530328125000024
		-2.5551998437500003e-09 0.23556403124999986 0.085738500000000023
		-3.73545421875e-09 0.2170972968749999 0.12534117187500005
		-4.8022031249999996e-09 0.19203370312499987 0.16113557812500001
		-5.7230296875000004e-09 0.16113515624999988 0.19203370312500001
		-6.4700015625000009e-09 0.12534117187499988 0.21709729687500001
		-7.0203796874999994e-09 0.08573849999999987 0.23556403125000003
		-7.3574156249999999e-09 0.043530328124999865 0.24687365624999996
		-7.4708999999999991e-09 -1.2836953722228372e-16 0.25068234375000004
		-7.3574156249999999e-09 -0.043530328125000121 0.24687365624999996
		-7.0203796874999994e-09 -0.085738500000000134 0.23556403125000003
		-6.4700015625000009e-09 -0.12534117187500013 0.21709729687500001
		-5.7230296875000004e-09 -0.16113515625000013 0.19203370312500001
		-4.8022031249999996e-09 -0.19203370312500012 0.16113557812500001
		-3.73545421875e-09 -0.21709729687500012 0.12534117187500005
		-2.5551998437500003e-09 -0.23556403125000014 0.085738500000000023
		-1.2973120312500001e-09 -0.24687365625000013 0.043530328125000024
		0 -0.25068192187500016 3.2092384305570931e-17
		0 -0.24687365625000013 -0.043530328124999962
		0 -0.23556403125000014 -0.085738499999999981
		0 -0.21709729687500012 -0.12534117187499999
		0 -0.19203370312500012 -0.16113557812500001
		0 -0.16113515625000013 -0.19203370312500001
		0 -0.12534117187500013 -0.21709729687499996
		0 -0.085738500000000134 -0.23556445312500002
		0 -0.043530328125000121 -0.24687365624999996
		0 -1.2836953722228372e-16 -0.25068234375000004
		0 0.043530328124999865 -0.24687365624999996
		0 0.08573849999999987 -0.23556445312500002
		0 0.12534117187499988 -0.21709729687499996
		0 0.16113515624999988 -0.19203370312500001
		0 0.19203370312499987 -0.16113557812500001
		0 0.2170972968749999 -0.12534117187499999
		0 0.23556403124999986 -0.085738499999999981
		0 0.24687365624999985 -0.043530328124999962
		0 0.25068192187499988 3.2092384305570931e-17
		0.043530328124999997 0.24687365624999985 3.2092384305570931e-17
		0.085738499999999995 0.23556403124999986 3.2092384305570931e-17
		0.12534117187500002 0.2170972968749999 3.2092384305570931e-17
		0.16113557812500001 0.19203370312499987 3.2092384305570931e-17
		0.19203370312500001 0.16113515624999988 3.2092384305570931e-17
		0.21709729687499998 0.12534117187499988 3.2092384305570931e-17
		0.23556403125 0.08573849999999987 3.2092384305570931e-17
		0.24687365624999996 0.043530328124999865 3.2092384305570931e-17
		0.25068192187499999 -1.2836953722228372e-16 3.2092384305570931e-17
		0.24687365624999996 -0.043530328125000121 3.2092384305570931e-17
		0.23556403125 -0.085738500000000134 3.2092384305570931e-17
		0.21709729687499998 -0.12534117187500013 3.2092384305570931e-17
		0.19203370312500001 -0.16113515625000013 3.2092384305570931e-17
		0.16113557812500001 -0.19203370312500012 3.2092384305570931e-17
		0.12534117187500002 -0.21709729687500012 3.2092384305570931e-17
		0.085738499999999995 -0.23556403125000014 3.2092384305570931e-17
		0.043530328124999997 -0.24687365625000013 3.2092384305570931e-17
		0 -0.25068192187500016 3.2092384305570931e-17
		-0.043530328124999997 -0.24687365625000013 3.2092384305570931e-17
		-0.085738499999999995 -0.23556403125000014 3.2092384305570931e-17
		-0.12534117187500002 -0.21709729687500012 3.2092384305570931e-17
		-0.16113557812500001 -0.19203370312500012 3.2092384305570931e-17
		-0.19203370312500001 -0.16113515625000013 3.2092384305570931e-17
		-0.21709729687499998 -0.12534117187500013 3.2092384305570931e-17
		-0.23556403125 -0.085738500000000134 3.2092384305570931e-17
		-0.24687365624999996 -0.043530328125000121 3.2092384305570931e-17
		-0.25068234375000004 -1.2836953722228372e-16 3.2092384305570931e-17
		-0.24687365624999996 0.043530328124999865 3.2092384305570931e-17
		-0.23556403125 0.08573849999999987 3.2092384305570931e-17
		-0.21709729687499998 0.12534117187499988 3.2092384305570931e-17
		-0.19203370312500001 0.16113515624999988 3.2092384305570931e-17
		-0.16113557812500001 0.19203370312499987 3.2092384305570931e-17
		-0.12534117187500002 0.2170972968749999 3.2092384305570931e-17
		-0.085738499999999995 0.23556403124999986 3.2092384305570931e-17
		-0.043530328124999997 0.24687365624999985 3.2092384305570931e-17
		0 0.25068192187499988 3.2092384305570931e-17
		-1.2973120312500001e-09 0.24687365624999985 0.043530328125000024
		-2.5551998437500003e-09 0.23556403124999986 0.085738500000000023
		-3.73545421875e-09 0.2170972968749999 0.12534117187500005
		-4.8022031249999996e-09 0.19203370312499987 0.16113557812500001
		-5.7230296875000004e-09 0.16113515624999988 0.19203370312500001
		-6.4700015625000009e-09 0.12534117187499988 0.21709729687500001
		-7.0203796874999994e-09 0.08573849999999987 0.23556403125000003
		-7.3574156249999999e-09 0.043530328124999865 0.24687365624999996
		-7.4708999999999991e-09 -1.2836953722228372e-16 0.25068234375000004
		-0.077465109374999994 -1.2836953722228372e-16 0.23841295312500005
		-0.14734743750000001 -1.2836953722228372e-16 0.20280628125
		-0.20280628125 -1.2836953722228372e-16 0.14734743750000001
		-0.23841295312500005 -1.2836953722228372e-16 0.077465109375000035
		-0.25068234375000004 -1.2836953722228372e-16 3.2092384305570931e-17
		-0.23841295312500005 -1.2836953722228372e-16 -0.077465109374999966
		-0.20280628125 -1.2836953722228372e-16 -0.14734743750000001
		-0.14734743750000001 -1.2836953722228372e-16 -0.20280628125
		-0.077465109374999994 -1.2836953722228372e-16 -0.23841295312500005
		0 -1.2836953722228372e-16 -0.25068234375000004
		0.077465109374999994 -1.2836953722228372e-16 -0.23841295312500005
		0.14734743750000001 -1.2836953722228372e-16 -0.20280628125
		0.20280628125 -1.2836953722228372e-16 -0.14734743750000001
		0.23841295312500005 -1.2836953722228372e-16 -0.077465109374999966
		0.25068192187499999 -1.2836953722228372e-16 3.2092384305570931e-17
		0.23841295312500005 -1.2836953722228372e-16 0.077465109375000035
		0.20280628125 -1.2836953722228372e-16 0.14734743750000001
		0.14734743750000001 -1.2836953722228372e-16 0.20280628125
		0.077465109374999994 -1.2836953722228372e-16 0.23841295312500005
		-7.4708999999999991e-09 -1.2836953722228372e-16 0.25068234375000004
		;
createNode nurbsCurve -n "L_FrFoot_BallFloor_Guide_Ctrl_Ctrl_CtrlShape" -p "L_FrFoot_BallFloor_Guide";
	rename -uid "B0CE0274-AC4F-B529-34C7-5EA268817D4A";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/C:\\Users\\Esteban\\Documents\\maya\\2022\\scripts\\rigging\\Mutant_Tools\\Icons\\Guide_Data";
	setAttr -k off ".v" no;
	setAttr ".ove" yes;
	setAttr ".ovc" 13;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 9 0 no 3
		10 0 1 2 3 4 5 6 7 8 9
		10
		-0.2109375 -0.10546875000000014 -5.8966734374679077e-06
		0.39872714062500003 -0.10796456250000011 -5.8966734374679077e-06
		0.31204110937499996 -0.21365564062500014 -5.8966734374679077e-06
		0.41773218749999996 -0.39620432812500012 -5.8966734374679077e-06
		0.97001803124999997 -1.6344703137836954e-07 -5.821242187467907e-06
		0.41773260937500006 0.39620432812499984 -5.8966734374679077e-06
		0.31204110937499996 0.21365521874999988 -5.8966734374679077e-06
		0.39872714062500003 0.10682760937499987 -3.023772187467908e-06
		-0.2109375 0.10546874999999986 -5.8966734374679077e-06
		-0.2109375 -0.10546875000000014 -5.8966734374679077e-06
		;
createNode nurbsCurve -n "L_FrFoot_BallFloor_Guide_Ctrl_Ctrl_Ctrl_CtrlShape" -p "L_FrFoot_BallFloor_Guide";
	rename -uid "058C268D-4B49-1093-5A75-F49AD3B5C735";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/C:\\Users\\Esteban\\Documents\\maya\\2022\\scripts\\rigging\\Mutant_Tools\\Icons\\Guide_Data";
	setAttr -k off ".v" no;
	setAttr ".ove" yes;
	setAttr ".ovc" 6;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 9 0 no 3
		10 0 1 2 3 4 5 6 7 8 9
		10
		0.10546875 5.8966734373716305e-06 -0.2109375
		0.10796456249999997 5.8966734373716305e-06 0.39872714062500003
		0.21365564062499998 5.8966734373716305e-06 0.31204110937499996
		0.39620432812499995 5.8966734373716305e-06 0.41773218749999996
		1.6344703125e-07 5.8212421873716299e-06 0.97001803124999997
		-0.39620432812499995 5.8966734373716305e-06 0.41773260937500006
		-0.21365521875000001 5.8966734373716305e-06 0.31204110937499996
		-0.10682760937500001 3.0237721873716308e-06 0.39872714062500003
		-0.10546875 5.8966734373716305e-06 -0.2109375
		0.10546875 5.8966734373716305e-06 -0.2109375
		;
createNode joint -n "L_FrFoot_Out_Guide" -p "L_FrFoot_BallFloor_Guide";
	rename -uid "0615BBC1-9C4D-31DE-2930-3BB3A66373CE";
	addAttr -ci true -sn "Helper" -ln "Helper" -min 0 -max 1 -en "Hide:Show" -at "enum";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/C:\\Users\\Esteban\\Documents\\maya\\2022\\scripts\\rigging\\Mutant_Tools\\Icons\\Guide_Data";
	setAttr ".t" -type "double3" -6.5600919723510813 7.815970093361102e-14 4.9263634420582945e-14 ;
	setAttr ".r" -type "double3" 89.999999999999815 25.64784425575305 179.99999999999932 ;
	setAttr ".s" -type "double3" 0.99999999999999944 0.99999999999999967 1 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 7.9482806932276754e-15 5.1986849590816012e-15 -1.590277340731758e-15 ;
	setAttr ".radi" 0.5;
	setAttr -cb on ".Helper";
createNode nurbsCurve -n "L_FrFoot_Out_Guide_CtrlShape" -p "L_FrFoot_Out_Guide";
	rename -uid "D17BA290-9241-C823-7D43-26B4F14F6A21";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/C:\\Users\\Esteban\\Documents\\maya\\2022\\scripts\\rigging\\Mutant_Tools\\Icons\\Guide_Data";
	setAttr -k off ".v" no;
	setAttr ".ove" yes;
	setAttr ".ovc" 14;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 9 0 no 3
		10 0 1 2 3 4 5 6 7 8 9
		10
		5.8966734376283696e-06 -0.2109375 0.10546875
		5.8966734376283696e-06 0.39872714062500003 0.10796456249999997
		5.8966734376283696e-06 0.31204110937499996 0.21365564062499998
		5.8966734376283696e-06 0.41773218749999996 0.39620432812499995
		5.8212421876283689e-06 0.97001803124999997 1.6344703125e-07
		5.8966734376283696e-06 0.41773260937500006 -0.39620432812499995
		5.8966734376283696e-06 0.31204110937499996 -0.21365521875000001
		3.0237721876283699e-06 0.39872714062500003 -0.10682760937500001
		5.8966734376283696e-06 -0.2109375 -0.10546875
		5.8966734376283696e-06 -0.2109375 0.10546875
		;
createNode nurbsCurve -n "L_FrFoot_Out_Guide_Ctrl_CtrlShape" -p "L_FrFoot_Out_Guide";
	rename -uid "D4A4339B-174D-6DA6-F544-74A46CC9B523";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/C:\\Users\\Esteban\\Documents\\maya\\2022\\scripts\\rigging\\Mutant_Tools\\Icons\\Guide_Data";
	setAttr -k off ".v" no;
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
		1.2836953722228372e-16 0.25068192187499999 0
		-1.2973119028804628e-09 0.24687365624999996 0.043530328124999997
		-2.5551997153804631e-09 0.23556403125 0.085738499999999995
		-3.7354540903804627e-09 0.21709729687499998 0.12534117187500002
		-4.8022029966304623e-09 0.19203370312500001 0.16113557812500001
		-5.7230295591304631e-09 0.16113515624999999 0.19203370312500001
		-6.4700014341304637e-09 0.12534117187500002 0.21709729687499998
		-7.0203795591304622e-09 0.085738499999999995 0.23556403125
		-7.3574154966304626e-09 0.043530328124999997 0.24687365624999996
		-7.4708998716304619e-09 0 0.25068234375000004
		-7.3574154966304626e-09 -0.043530328124999997 0.24687365624999996
		-7.0203795591304622e-09 -0.085738499999999995 0.23556403125
		-6.4700014341304637e-09 -0.12534117187500002 0.21709729687499998
		-5.7230295591304631e-09 -0.16113515624999999 0.19203370312500001
		-4.8022029966304623e-09 -0.19203370312500001 0.16113557812500001
		-3.7354540903804627e-09 -0.21709729687499998 0.12534117187500002
		-2.5551997153804631e-09 -0.23556403125 0.085738499999999995
		-1.2973119028804628e-09 -0.24687365624999996 0.043530328124999997
		1.2836953722228372e-16 -0.25068192187499999 0
		1.2836953722228372e-16 -0.24687365624999996 -0.043530328124999997
		1.2836953722228372e-16 -0.23556403125 -0.085738499999999995
		1.2836953722228372e-16 -0.21709729687499998 -0.12534117187500002
		1.2836953722228372e-16 -0.19203370312500001 -0.16113557812500001
		1.2836953722228372e-16 -0.16113515624999999 -0.19203370312500001
		1.2836953722228372e-16 -0.12534117187500002 -0.21709729687499998
		1.2836953722228372e-16 -0.085738499999999995 -0.23556445312500002
		1.2836953722228372e-16 -0.043530328124999997 -0.24687365624999996
		1.2836953722228372e-16 0 -0.25068234375000004
		1.2836953722228372e-16 0.043530328124999997 -0.24687365624999996
		1.2836953722228372e-16 0.085738499999999995 -0.23556445312500002
		1.2836953722228372e-16 0.12534117187500002 -0.21709729687499998
		1.2836953722228372e-16 0.16113515624999999 -0.19203370312500001
		1.2836953722228372e-16 0.19203370312500001 -0.16113557812500001
		1.2836953722228372e-16 0.21709729687499998 -0.12534117187500002
		1.2836953722228372e-16 0.23556403125 -0.085738499999999995
		1.2836953722228372e-16 0.24687365624999996 -0.043530328124999997
		1.2836953722228372e-16 0.25068192187499999 0
		0.043530328125000121 0.24687365624999996 0
		0.085738500000000134 0.23556403125 0
		0.12534117187500013 0.21709729687499998 0
		0.16113557812500012 0.19203370312500001 0
		0.19203370312500012 0.16113515624999999 0
		0.21709729687500012 0.12534117187500002 0
		0.23556403125000014 0.085738499999999995 0
		0.24687365625000013 0.043530328124999997 0
		0.25068192187500016 0 0
		0.24687365625000013 -0.043530328124999997 0
		0.23556403125000014 -0.085738499999999995 0
		0.21709729687500012 -0.12534117187500002 0
		0.19203370312500012 -0.16113515624999999 0
		0.16113557812500012 -0.19203370312500001 0
		0.12534117187500013 -0.21709729687499998 0
		0.085738500000000134 -0.23556403125 0
		0.043530328125000121 -0.24687365624999996 0
		1.2836953722228372e-16 -0.25068192187499999 0
		-0.043530328124999865 -0.24687365624999996 0
		-0.08573849999999987 -0.23556403125 0
		-0.12534117187499988 -0.21709729687499998 0
		-0.16113557812499987 -0.19203370312500001 0
		-0.19203370312499987 -0.16113515624999999 0
		-0.2170972968749999 -0.12534117187500002 0
		-0.23556403124999986 -0.085738499999999995 0
		-0.24687365624999985 -0.043530328124999997 0
		-0.25068234374999987 0 0
		-0.24687365624999985 0.043530328124999997 0
		-0.23556403124999986 0.085738499999999995 0
		-0.2170972968749999 0.12534117187500002 0
		-0.19203370312499987 0.16113515624999999 0
		-0.16113557812499987 0.19203370312500001 0
		-0.12534117187499988 0.21709729687499998 0
		-0.08573849999999987 0.23556403125 0
		-0.043530328124999865 0.24687365624999996 0
		1.2836953722228372e-16 0.25068192187499999 0
		-1.2973119028804628e-09 0.24687365624999996 0.043530328124999997
		-2.5551997153804631e-09 0.23556403125 0.085738499999999995
		-3.7354540903804627e-09 0.21709729687499998 0.12534117187500002
		-4.8022029966304623e-09 0.19203370312500001 0.16113557812500001
		-5.7230295591304631e-09 0.16113515624999999 0.19203370312500001
		-6.4700014341304637e-09 0.12534117187500002 0.21709729687499998
		-7.0203795591304622e-09 0.085738499999999995 0.23556403125
		-7.3574154966304626e-09 0.043530328124999997 0.24687365624999996
		-7.4708998716304619e-09 0 0.25068234375000004
		-0.077465109374999869 0 0.23841295312500005
		-0.1473474374999999 0 0.20280628125
		-0.20280628124999983 0 0.14734743750000001
		-0.23841295312499988 0 0.077465109374999994
		-0.25068234374999987 0 0
		-0.23841295312499988 0 -0.077465109374999994
		-0.20280628124999983 0 -0.14734743750000001
		-0.1473474374999999 0 -0.20280628125
		-0.077465109374999869 0 -0.23841295312500005
		1.2836953722228372e-16 0 -0.25068234375000004
		0.077465109375000132 0 -0.23841295312500005
		0.14734743750000018 0 -0.20280628125
		0.20280628125000011 0 -0.14734743750000001
		0.23841295312500016 0 -0.077465109374999994
		0.25068192187500016 0 0
		0.23841295312500016 0 0.077465109374999994
		0.20280628125000011 0 0.14734743750000001
		0.14734743750000018 0 0.20280628125
		0.077465109375000132 0 0.23841295312500005
		-7.4708998716304619e-09 0 0.25068234375000004
		;
createNode nurbsCurve -n "L_FrFoot_Out_Guide_Ctrl_Ctrl_CtrlShape" -p "L_FrFoot_Out_Guide";
	rename -uid "443A6CD9-674A-54B1-2A2F-C7AFE10F9EA5";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/C:\\Users\\Esteban\\Documents\\maya\\2022\\scripts\\rigging\\Mutant_Tools\\Icons\\Guide_Data";
	setAttr -k off ".v" no;
	setAttr ".ove" yes;
	setAttr ".ovc" 13;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 9 0 no 3
		10 0 1 2 3 4 5 6 7 8 9
		10
		-0.21093749999999986 -0.10546875 -5.8966734375000001e-06
		0.3987271406250002 -0.10796456249999997 -5.8966734375000001e-06
		0.31204110937500007 -0.21365564062499998 -5.8966734375000001e-06
		0.41773218750000002 -0.39620432812499995 -5.8966734375000001e-06
		0.97001803124999997 -1.6344703125e-07 -5.8212421874999994e-06
		0.41773260937500012 0.39620432812499995 -5.8966734375000001e-06
		0.31204110937500007 0.21365521875000001 -5.8966734375000001e-06
		0.3987271406250002 0.10682760937500001 -3.0237721875000003e-06
		-0.21093749999999986 0.10546875 -5.8966734375000001e-06
		-0.21093749999999986 -0.10546875 -5.8966734375000001e-06
		;
createNode nurbsCurve -n "L_FrFoot_Out_Guide_Ctrl_Ctrl_Ctrl_CtrlShape" -p "L_FrFoot_Out_Guide";
	rename -uid "B6EA0947-9A41-C4FC-E8C7-C2B1495C9979";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/C:\\Users\\Esteban\\Documents\\maya\\2022\\scripts\\rigging\\Mutant_Tools\\Icons\\Guide_Data";
	setAttr -k off ".v" no;
	setAttr ".ove" yes;
	setAttr ".ovc" 6;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 9 0 no 3
		10 0 1 2 3 4 5 6 7 8 9
		10
		0.10546875000000014 5.8966734375000001e-06 -0.2109375
		0.10796456250000011 5.8966734375000001e-06 0.39872714062500003
		0.21365564062500014 5.8966734375000001e-06 0.31204110937499996
		0.39620432812500012 5.8966734375000001e-06 0.41773218749999996
		1.6344703137836954e-07 5.8212421874999994e-06 0.97001803124999997
		-0.39620432812499984 5.8966734375000001e-06 0.41773260937500006
		-0.21365521874999988 5.8966734375000001e-06 0.31204110937499996
		-0.10682760937499987 3.0237721875000003e-06 0.39872714062500003
		-0.10546874999999986 5.8966734375000001e-06 -0.2109375
		0.10546875000000014 5.8966734375000001e-06 -0.2109375
		;
createNode joint -n "L_FrFoot_In_Guide" -p "L_FrFoot_BallFloor_Guide";
	rename -uid "E78A3BEA-1D48-0A44-1654-BCBD0401C444";
	addAttr -ci true -sn "Helper" -ln "Helper" -min 0 -max 1 -en "Hide:Show" -at "enum";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/C:\\Users\\Esteban\\Documents\\maya\\2022\\scripts\\rigging\\Mutant_Tools\\Icons\\Guide_Data";
	setAttr ".t" -type "double3" 6.5600919723510991 7.1054273576010019e-15 -5.301547672878019e-14 ;
	setAttr ".r" -type "double3" 89.999999999999844 -25.64784425575353 179.99999999999986 ;
	setAttr ".s" -type "double3" 0.99999999999999944 0.99999999999999967 1 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 7.9482806932276754e-15 5.1986849590816012e-15 -1.590277340731758e-15 ;
	setAttr ".radi" 0.5;
	setAttr -cb on ".Helper";
createNode nurbsCurve -n "L_FrFoot_In_Guide_CtrlShape" -p "L_FrFoot_In_Guide";
	rename -uid "1F0D2D76-914B-4293-AFDA-93913195AC8F";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/C:\\Users\\Esteban\\Documents\\maya\\2022\\scripts\\rigging\\Mutant_Tools\\Icons\\Guide_Data";
	setAttr -k off ".v" no;
	setAttr ".ove" yes;
	setAttr ".ovc" 14;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 9 0 no 3
		10 0 1 2 3 4 5 6 7 8 9
		10
		5.8966734374679077e-06 -0.21093749999999986 0.10546875000000025
		5.8966734374679077e-06 0.3987271406250002 0.10796456250000025
		5.8966734374679077e-06 0.31204110937500007 0.21365564062500023
		5.8966734374679077e-06 0.41773218750000002 0.39620432812500028
		5.821242187467907e-06 0.97001803124999997 1.6344703150673908e-07
		5.8966734374679077e-06 0.41773260937500012 -0.39620432812499973
		5.8966734374679077e-06 0.31204110937500007 -0.21365521874999974
		3.023772187467908e-06 0.3987271406250002 -0.10682760937499973
		5.8966734374679077e-06 -0.21093749999999986 -0.10546874999999975
		5.8966734374679077e-06 -0.21093749999999986 0.10546875000000025
		;
createNode nurbsCurve -n "L_FrFoot_In_Guide_Ctrl_CtrlShape" -p "L_FrFoot_In_Guide";
	rename -uid "65FBA7DA-1648-8C8B-1FD6-28A7B6073827";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/C:\\Users\\Esteban\\Documents\\maya\\2022\\scripts\\rigging\\Mutant_Tools\\Icons\\Guide_Data";
	setAttr -k off ".v" no;
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
		-3.2092384305570931e-17 0.25068192187500016 2.5673907444456745e-16
		-1.2973120633423844e-09 0.24687365625000013 0.043530328125000253
		-2.5551998758423846e-09 0.23556403125000014 0.085738500000000259
		-3.7354542508423843e-09 0.21709729687500012 0.12534117187500027
		-4.8022031570923839e-09 0.19203370312500012 0.16113557812500023
		-5.7230297195923847e-09 0.16113515625000013 0.19203370312500023
		-6.4700015945923852e-09 0.12534117187500013 0.21709729687500026
		-7.0203797195923837e-09 0.085738500000000134 0.23556403125000028
		-7.3574156570923842e-09 0.043530328125000121 0.24687365625000021
		-7.4709000320923834e-09 1.2836953722228372e-16 0.25068234375000026
		-7.3574156570923842e-09 -0.043530328124999865 0.24687365625000021
		-7.0203797195923837e-09 -0.08573849999999987 0.23556403125000028
		-6.4700015945923852e-09 -0.12534117187499988 0.21709729687500026
		-5.7230297195923847e-09 -0.16113515624999988 0.19203370312500023
		-4.8022031570923839e-09 -0.19203370312499987 0.16113557812500023
		-3.7354542508423843e-09 -0.2170972968749999 0.12534117187500027
		-2.5551998758423846e-09 -0.23556403124999986 0.085738500000000259
		-1.2973120633423844e-09 -0.24687365624999985 0.043530328125000253
		-3.2092384305570931e-17 -0.25068192187499988 2.5673907444456745e-16
		-3.2092384305570931e-17 -0.24687365624999985 -0.04353032812499974
		-3.2092384305570931e-17 -0.23556403124999986 -0.085738499999999745
		-3.2092384305570931e-17 -0.2170972968749999 -0.12534117187499977
		-3.2092384305570931e-17 -0.19203370312499987 -0.16113557812499973
		-3.2092384305570931e-17 -0.16113515624999988 -0.19203370312499973
		-3.2092384305570931e-17 -0.12534117187499988 -0.21709729687499973
		-3.2092384305570931e-17 -0.08573849999999987 -0.23556445312499974
		-3.2092384305570931e-17 -0.043530328124999865 -0.24687365624999974
		-3.2092384305570931e-17 1.2836953722228372e-16 -0.25068234374999976
		-3.2092384305570931e-17 0.043530328125000121 -0.24687365624999974
		-3.2092384305570931e-17 0.085738500000000134 -0.23556445312499974
		-3.2092384305570931e-17 0.12534117187500013 -0.21709729687499973
		-3.2092384305570931e-17 0.16113515625000013 -0.19203370312499973
		-3.2092384305570931e-17 0.19203370312500012 -0.16113557812499973
		-3.2092384305570931e-17 0.21709729687500012 -0.12534117187499977
		-3.2092384305570931e-17 0.23556403125000014 -0.085738499999999745
		-3.2092384305570931e-17 0.24687365625000013 -0.04353032812499974
		-3.2092384305570931e-17 0.25068192187500016 2.5673907444456745e-16
		0.043530328124999962 0.24687365625000013 2.5673907444456745e-16
		0.085738499999999981 0.23556403125000014 2.5673907444456745e-16
		0.12534117187499999 0.21709729687500012 2.5673907444456745e-16
		0.16113557812500001 0.19203370312500012 2.5673907444456745e-16
		0.19203370312500001 0.16113515625000013 2.5673907444456745e-16
		0.21709729687499996 0.12534117187500013 2.5673907444456745e-16
		0.23556403124999997 0.085738500000000134 2.5673907444456745e-16
		0.24687365624999996 0.043530328125000121 2.5673907444456745e-16
		0.25068192187499999 1.2836953722228372e-16 2.5673907444456745e-16
		0.24687365624999996 -0.043530328124999865 2.5673907444456745e-16
		0.23556403124999997 -0.08573849999999987 2.5673907444456745e-16
		0.21709729687499996 -0.12534117187499988 2.5673907444456745e-16
		0.19203370312500001 -0.16113515624999988 2.5673907444456745e-16
		0.16113557812500001 -0.19203370312499987 2.5673907444456745e-16
		0.12534117187499999 -0.2170972968749999 2.5673907444456745e-16
		0.085738499999999981 -0.23556403124999986 2.5673907444456745e-16
		0.043530328124999962 -0.24687365624999985 2.5673907444456745e-16
		-3.2092384305570931e-17 -0.25068192187499988 2.5673907444456745e-16
		-0.043530328125000024 -0.24687365624999985 2.5673907444456745e-16
		-0.085738500000000023 -0.23556403124999986 2.5673907444456745e-16
		-0.12534117187500005 -0.2170972968749999 2.5673907444456745e-16
		-0.16113557812500001 -0.19203370312499987 2.5673907444456745e-16
		-0.19203370312500001 -0.16113515624999988 2.5673907444456745e-16
		-0.21709729687500001 -0.12534117187499988 2.5673907444456745e-16
		-0.23556403125000003 -0.08573849999999987 2.5673907444456745e-16
		-0.24687365624999996 -0.043530328124999865 2.5673907444456745e-16
		-0.25068234375000004 1.2836953722228372e-16 2.5673907444456745e-16
		-0.24687365624999996 0.043530328125000121 2.5673907444456745e-16
		-0.23556403125000003 0.085738500000000134 2.5673907444456745e-16
		-0.21709729687500001 0.12534117187500013 2.5673907444456745e-16
		-0.19203370312500001 0.16113515625000013 2.5673907444456745e-16
		-0.16113557812500001 0.19203370312500012 2.5673907444456745e-16
		-0.12534117187500005 0.21709729687500012 2.5673907444456745e-16
		-0.085738500000000023 0.23556403125000014 2.5673907444456745e-16
		-0.043530328125000024 0.24687365625000013 2.5673907444456745e-16
		-3.2092384305570931e-17 0.25068192187500016 2.5673907444456745e-16
		-1.2973120633423844e-09 0.24687365625000013 0.043530328125000253
		-2.5551998758423846e-09 0.23556403125000014 0.085738500000000259
		-3.7354542508423843e-09 0.21709729687500012 0.12534117187500027
		-4.8022031570923839e-09 0.19203370312500012 0.16113557812500023
		-5.7230297195923847e-09 0.16113515625000013 0.19203370312500023
		-6.4700015945923852e-09 0.12534117187500013 0.21709729687500026
		-7.0203797195923837e-09 0.085738500000000134 0.23556403125000028
		-7.3574156570923842e-09 0.043530328125000121 0.24687365625000021
		-7.4709000320923834e-09 1.2836953722228372e-16 0.25068234375000026
		-0.077465109375000035 1.2836953722228372e-16 0.23841295312500027
		-0.14734743750000001 1.2836953722228372e-16 0.20280628125000028
		-0.20280628125 1.2836953722228372e-16 0.14734743750000029
		-0.23841295312500005 1.2836953722228372e-16 0.077465109375000257
		-0.25068234375000004 1.2836953722228372e-16 2.5673907444456745e-16
		-0.23841295312500005 1.2836953722228372e-16 -0.07746510937499973
		-0.20280628125 1.2836953722228372e-16 -0.14734743749999976
		-0.14734743750000001 1.2836953722228372e-16 -0.20280628124999975
		-0.077465109375000035 1.2836953722228372e-16 -0.2384129531249998
		-3.2092384305570931e-17 1.2836953722228372e-16 -0.25068234374999976
		0.077465109374999966 1.2836953722228372e-16 -0.2384129531249998
		0.14734743750000001 1.2836953722228372e-16 -0.20280628124999975
		0.20280628125 1.2836953722228372e-16 -0.14734743749999976
		0.23841295312500005 1.2836953722228372e-16 -0.07746510937499973
		0.25068192187499999 1.2836953722228372e-16 2.5673907444456745e-16
		0.23841295312500005 1.2836953722228372e-16 0.077465109375000257
		0.20280628125 1.2836953722228372e-16 0.14734743750000029
		0.14734743750000001 1.2836953722228372e-16 0.20280628125000028
		0.077465109374999966 1.2836953722228372e-16 0.23841295312500027
		-7.4709000320923834e-09 1.2836953722228372e-16 0.25068234375000026
		;
createNode nurbsCurve -n "L_FrFoot_In_Guide_Ctrl_Ctrl_CtrlShape" -p "L_FrFoot_In_Guide";
	rename -uid "32B3D139-9C47-F517-F977-889F16F2FEE9";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/C:\\Users\\Esteban\\Documents\\maya\\2022\\scripts\\rigging\\Mutant_Tools\\Icons\\Guide_Data";
	setAttr -k off ".v" no;
	setAttr ".ove" yes;
	setAttr ".ovc" 13;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 9 0 no 3
		10 0 1 2 3 4 5 6 7 8 9
		10
		-0.2109375 -0.10546874999999986 -5.896673437243261e-06
		0.39872714062500003 -0.10796456249999986 -5.896673437243261e-06
		0.31204110937499996 -0.21365564062499987 -5.896673437243261e-06
		0.41773218749999996 -0.39620432812499984 -5.896673437243261e-06
		0.97001803124999997 -1.6344703112163046e-07 -5.8212421872432603e-06
		0.41773260937500006 0.39620432812500012 -5.896673437243261e-06
		0.31204110937499996 0.2136552187500001 -5.896673437243261e-06
		0.39872714062500003 0.10682760937500013 -3.0237721872432613e-06
		-0.2109375 0.10546875000000014 -5.896673437243261e-06
		-0.2109375 -0.10546874999999986 -5.896673437243261e-06
		;
createNode nurbsCurve -n "L_FrFoot_In_Guide_Ctrl_Ctrl_Ctrl_CtrlShape" -p "L_FrFoot_In_Guide";
	rename -uid "94FB3F3C-3240-657E-39F5-929E73580F04";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/C:\\Users\\Esteban\\Documents\\maya\\2022\\scripts\\rigging\\Mutant_Tools\\Icons\\Guide_Data";
	setAttr -k off ".v" no;
	setAttr ".ove" yes;
	setAttr ".ovc" 6;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 9 0 no 3
		10 0 1 2 3 4 5 6 7 8 9
		10
		0.10546874999999999 5.8966734376283696e-06 -0.21093749999999972
		0.10796456249999996 5.8966734376283696e-06 0.39872714062500036
		0.21365564062499998 5.8966734376283696e-06 0.31204110937500029
		0.39620432812499995 5.8966734376283696e-06 0.41773218750000024
		1.6344703121790762e-07 5.8212421876283689e-06 0.9700180312500003
		-0.39620432812499995 5.8966734376283696e-06 0.41773260937500023
		-0.21365521875000004 5.8966734376283696e-06 0.31204110937500029
		-0.10682760937500002 3.0237721876283699e-06 0.39872714062500036
		-0.10546875000000001 5.8966734376283696e-06 -0.21093749999999972
		0.10546874999999999 5.8966734376283696e-06 -0.21093749999999972
		;
createNode joint -n "L_FrFoot_Toes_Guide" -p "L_FrFoot_Ball_Guide";
	rename -uid "D361E1BD-D348-743B-A163-B8B3089D7732";
	addAttr -ci true -sn "Helper" -ln "Helper" -min 0 -max 1 -en "Hide:Show" -at "enum";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/C:\\Users\\Esteban\\Documents\\maya\\2022\\scripts\\rigging\\Mutant_Tools\\Icons\\Guide_Data";
	setAttr ".t" -type "double3" 6.5435010932729769 0.15662477743382081 0.047964285579524576 ;
	setAttr ".r" -type "double3" -26.195023858534189 1.5423861844435203 -0.75864572902833949 ;
	setAttr ".s" -type "double3" 1.0000000000000004 1 1 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" -12.983800197275123 89.999999999999844 0 ;
	setAttr ".radi" 0.5;
	setAttr -cb on ".Helper";
createNode nurbsCurve -n "L_FrFoot_Toes_Guide_CtrlShape" -p "L_FrFoot_Toes_Guide";
	rename -uid "FB98E080-F648-C98E-AC06-F0924E809764";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/C:\\Users\\Esteban\\Documents\\maya\\2022\\scripts\\rigging\\Mutant_Tools\\Icons\\Guide_Data";
	setAttr -k off ".v" no;
	setAttr ".ove" yes;
	setAttr ".ovc" 14;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 9 0 no 3
		10 0 1 2 3 4 5 6 7 8 9
		10
		5.8966734376283696e-06 -0.21093749999999997 0.10546874999999949
		5.8966734376283696e-06 0.39872714062500003 0.10796456249999946
		5.8966734376283696e-06 0.31204110937499996 0.21365564062499948
		5.8966734376283696e-06 0.41773218749999996 0.39620432812499951
		5.8212421876283689e-06 0.97001803124999997 1.6344703073652185e-07
		5.8966734376283696e-06 0.41773260937500012 -0.3962043281250005
		5.8966734376283696e-06 0.31204110937499996 -0.21365521875000049
		3.0237721876283699e-06 0.39872714062500003 -0.10682760937500052
		5.8966734376283696e-06 -0.21093749999999997 -0.10546875000000051
		5.8966734376283696e-06 -0.21093749999999997 0.10546874999999949
		;
createNode nurbsCurve -n "L_FrFoot_Toes_Guide_Ctrl_CtrlShape" -p "L_FrFoot_Toes_Guide";
	rename -uid "BEDB1E40-5E49-4190-1A8D-A5B1F9838480";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/C:\\Users\\Esteban\\Documents\\maya\\2022\\scripts\\rigging\\Mutant_Tools\\Icons\\Guide_Data";
	setAttr -k off ".v" no;
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
		1.2836953722228372e-16 0.25068192187500005 -5.134781488891349e-16
		-1.2973119028804628e-09 0.24687365625000005 0.043530328124999483
		-2.5551997153804631e-09 0.23556403125000003 0.085738499999999496
		-3.7354540903804627e-09 0.21709729687500001 0.12534117187499949
		-4.8022029966304623e-09 0.19203370312500004 0.16113557812499951
		-5.7230295591304631e-09 0.16113515625000008 0.19203370312499946
		-6.4700014341304637e-09 0.12534117187500007 0.21709729687499951
		-7.0203795591304622e-09 0.085738500000000079 0.23556403124999947
		-7.3574154966304626e-09 0.043530328125000059 0.24687365624999946
		-7.4708998716304619e-09 6.4184768611141862e-17 0.25068234374999954
		-7.3574154966304626e-09 -0.043530328124999934 0.24687365624999946
		-7.0203795591304622e-09 -0.08573849999999994 0.23556403124999947
		-6.4700014341304637e-09 -0.12534117187499993 0.21709729687499951
		-5.7230295591304631e-09 -0.16113515624999994 0.19203370312499946
		-4.8022029966304623e-09 -0.19203370312499998 0.16113557812499951
		-3.7354540903804627e-09 -0.21709729687499996 0.12534117187499949
		-2.5551997153804631e-09 -0.23556403124999997 0.085738499999999496
		-1.2973119028804628e-09 -0.24687365624999991 0.043530328124999483
		1.2836953722228372e-16 -0.25068192187499994 -5.134781488891349e-16
		1.2836953722228372e-16 -0.24687365624999991 -0.04353032812500051
		1.2836953722228372e-16 -0.23556403124999997 -0.085738500000000523
		1.2836953722228372e-16 -0.21709729687499996 -0.12534117187500052
		1.2836953722228372e-16 -0.19203370312499998 -0.16113557812500051
		1.2836953722228372e-16 -0.16113515624999994 -0.19203370312500048
		1.2836953722228372e-16 -0.12534117187499993 -0.21709729687500054
		1.2836953722228372e-16 -0.08573849999999994 -0.23556445312500049
		1.2836953722228372e-16 -0.043530328124999934 -0.24687365625000049
		1.2836953722228372e-16 6.4184768611141862e-17 -0.25068234375000054
		1.2836953722228372e-16 0.043530328125000059 -0.24687365625000049
		1.2836953722228372e-16 0.085738500000000079 -0.23556445312500049
		1.2836953722228372e-16 0.12534117187500007 -0.21709729687500054
		1.2836953722228372e-16 0.16113515625000008 -0.19203370312500048
		1.2836953722228372e-16 0.19203370312500004 -0.16113557812500051
		1.2836953722228372e-16 0.21709729687500001 -0.12534117187500052
		1.2836953722228372e-16 0.23556403125000003 -0.085738500000000523
		1.2836953722228372e-16 0.24687365625000005 -0.04353032812500051
		1.2836953722228372e-16 0.25068192187500005 -5.134781488891349e-16
		0.043530328125000121 0.24687365625000005 -5.134781488891349e-16
		0.085738500000000134 0.23556403125000003 -5.134781488891349e-16
		0.12534117187500013 0.21709729687500001 -5.134781488891349e-16
		0.16113557812500012 0.19203370312500004 -5.134781488891349e-16
		0.19203370312500012 0.16113515625000008 -5.134781488891349e-16
		0.21709729687500012 0.12534117187500007 -5.134781488891349e-16
		0.23556403125000014 0.085738500000000079 -5.134781488891349e-16
		0.24687365625000013 0.043530328125000059 -5.134781488891349e-16
		0.25068192187500016 6.4184768611141862e-17 -5.134781488891349e-16
		0.24687365625000013 -0.043530328124999934 -5.134781488891349e-16
		0.23556403125000014 -0.08573849999999994 -5.134781488891349e-16
		0.21709729687500012 -0.12534117187499993 -5.134781488891349e-16
		0.19203370312500012 -0.16113515624999994 -5.134781488891349e-16
		0.16113557812500012 -0.19203370312499998 -5.134781488891349e-16
		0.12534117187500013 -0.21709729687499996 -5.134781488891349e-16
		0.085738500000000134 -0.23556403124999997 -5.134781488891349e-16
		0.043530328125000121 -0.24687365624999991 -5.134781488891349e-16
		1.2836953722228372e-16 -0.25068192187499994 -5.134781488891349e-16
		-0.043530328124999865 -0.24687365624999991 -5.134781488891349e-16
		-0.08573849999999987 -0.23556403124999997 -5.134781488891349e-16
		-0.12534117187499988 -0.21709729687499996 -5.134781488891349e-16
		-0.16113557812499987 -0.19203370312499998 -5.134781488891349e-16
		-0.19203370312499987 -0.16113515624999994 -5.134781488891349e-16
		-0.2170972968749999 -0.12534117187499993 -5.134781488891349e-16
		-0.23556403124999986 -0.08573849999999994 -5.134781488891349e-16
		-0.24687365624999985 -0.043530328124999934 -5.134781488891349e-16
		-0.25068234374999987 6.4184768611141862e-17 -5.134781488891349e-16
		-0.24687365624999985 0.043530328125000059 -5.134781488891349e-16
		-0.23556403124999986 0.085738500000000079 -5.134781488891349e-16
		-0.2170972968749999 0.12534117187500007 -5.134781488891349e-16
		-0.19203370312499987 0.16113515625000008 -5.134781488891349e-16
		-0.16113557812499987 0.19203370312500004 -5.134781488891349e-16
		-0.12534117187499988 0.21709729687500001 -5.134781488891349e-16
		-0.08573849999999987 0.23556403125000003 -5.134781488891349e-16
		-0.043530328124999865 0.24687365625000005 -5.134781488891349e-16
		1.2836953722228372e-16 0.25068192187500005 -5.134781488891349e-16
		-1.2973119028804628e-09 0.24687365625000005 0.043530328124999483
		-2.5551997153804631e-09 0.23556403125000003 0.085738499999999496
		-3.7354540903804627e-09 0.21709729687500001 0.12534117187499949
		-4.8022029966304623e-09 0.19203370312500004 0.16113557812499951
		-5.7230295591304631e-09 0.16113515625000008 0.19203370312499946
		-6.4700014341304637e-09 0.12534117187500007 0.21709729687499951
		-7.0203795591304622e-09 0.085738500000000079 0.23556403124999947
		-7.3574154966304626e-09 0.043530328125000059 0.24687365624999946
		-7.4708998716304619e-09 6.4184768611141862e-17 0.25068234374999954
		-0.077465109374999869 6.4184768611141862e-17 0.23841295312499952
		-0.1473474374999999 6.4184768611141862e-17 0.20280628124999947
		-0.20280628124999983 6.4184768611141862e-17 0.14734743749999951
		-0.23841295312499988 6.4184768611141862e-17 0.07746510937499948
		-0.25068234374999987 6.4184768611141862e-17 -5.134781488891349e-16
		-0.23841295312499988 6.4184768611141862e-17 -0.077465109375000507
		-0.20280628124999983 6.4184768611141862e-17 -0.14734743750000054
		-0.1473474374999999 6.4184768611141862e-17 -0.2028062812500005
		-0.077465109374999869 6.4184768611141862e-17 -0.23841295312500055
		1.2836953722228372e-16 6.4184768611141862e-17 -0.25068234375000054
		0.077465109375000132 6.4184768611141862e-17 -0.23841295312500055
		0.14734743750000018 6.4184768611141862e-17 -0.2028062812500005
		0.20280628125000011 6.4184768611141862e-17 -0.14734743750000054
		0.23841295312500016 6.4184768611141862e-17 -0.077465109375000507
		0.25068192187500016 6.4184768611141862e-17 -5.134781488891349e-16
		0.23841295312500016 6.4184768611141862e-17 0.07746510937499948
		0.20280628125000011 6.4184768611141862e-17 0.14734743749999951
		0.14734743750000018 6.4184768611141862e-17 0.20280628124999947
		0.077465109375000132 6.4184768611141862e-17 0.23841295312499952
		-7.4708998716304619e-09 6.4184768611141862e-17 0.25068234374999954
		;
createNode nurbsCurve -n "L_FrFoot_Toes_Guide_Ctrl_Ctrl_CtrlShape" -p "L_FrFoot_Toes_Guide";
	rename -uid "54E24A03-F94E-E93C-AFC6-908542563BD9";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/C:\\Users\\Esteban\\Documents\\maya\\2022\\scripts\\rigging\\Mutant_Tools\\Icons\\Guide_Data";
	setAttr -k off ".v" no;
	setAttr ".ove" yes;
	setAttr ".ovc" 13;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 9 0 no 3
		10 0 1 2 3 4 5 6 7 8 9
		10
		-0.21093749999999986 -0.10546874999999993 -5.8966734380134782e-06
		0.3987271406250002 -0.10796456249999992 -5.8966734380134782e-06
		0.31204110937500007 -0.21365564062499992 -5.8966734380134782e-06
		0.41773218750000002 -0.39620432812499995 -5.8966734380134782e-06
		0.97001803124999997 -1.6344703118581523e-07 -5.8212421880134776e-06
		0.41773260937500012 0.39620432812499995 -5.8966734380134782e-06
		0.31204110937500007 0.21365521875000004 -5.8966734380134782e-06
		0.3987271406250002 0.10682760937500005 -3.0237721880134785e-06
		-0.21093749999999986 0.10546875000000007 -5.8966734380134782e-06
		-0.21093749999999986 -0.10546874999999993 -5.8966734380134782e-06
		;
createNode nurbsCurve -n "L_FrFoot_Toes_Guide_Ctrl_Ctrl_Ctrl_CtrlShape" -p "L_FrFoot_Toes_Guide";
	rename -uid "78E3A8C2-CB45-236D-8215-DCB8E1406B38";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/C:\\Users\\Esteban\\Documents\\maya\\2022\\scripts\\rigging\\Mutant_Tools\\Icons\\Guide_Data";
	setAttr -k off ".v" no;
	setAttr ".ove" yes;
	setAttr ".ovc" 6;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 9 0 no 3
		10 0 1 2 3 4 5 6 7 8 9
		10
		0.10546875000000014 5.8966734375641848e-06 -0.2109375000000005
		0.10796456250000011 5.8966734375641848e-06 0.39872714062499948
		0.21365564062500014 5.8966734375641848e-06 0.31204110937499946
		0.39620432812500012 5.8966734375641848e-06 0.41773218749999941
		1.6344703137836954e-07 5.8212421875641842e-06 0.97001803124999952
		-0.39620432812499984 5.8966734375641848e-06 0.41773260937499951
		-0.21365521874999988 5.8966734375641848e-06 0.31204110937499946
		-0.10682760937499987 3.0237721875641851e-06 0.39872714062499948
		-0.10546874999999986 5.8966734375641848e-06 -0.2109375000000005
		0.10546875000000014 5.8966734375641848e-06 -0.2109375000000005
		;
createNode joint -n "L_FrFoot_HeelMid_Guide" -p "L_FrFoot_Ankle_Guide";
	rename -uid "DC4B23C9-BC46-5C03-8197-B49F05B2CAF5";
	addAttr -ci true -sn "Helper" -ln "Helper" -min 0 -max 1 -en "Hide:Show" -at "enum";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/C:\\Users\\Esteban\\Documents\\maya\\2022\\scripts\\rigging\\Mutant_Tools\\Icons\\Guide_Data";
	setAttr ".t" -type "double3" 5.2383691414634006 2.1341701468012277 0.30045186103438642 ;
	setAttr ".r" -type "double3" -4.4132147435210811 1.7137318008143982 -0.13224212445467148 ;
	setAttr ".s" -type "double3" 0.99999999999999978 0.99999999999999978 0.99999999999999944 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" -124.75737512881491 89.999999999999886 0 ;
	setAttr ".radi" 0.5;
	setAttr -cb on ".Helper";
createNode nurbsCurve -n "L_FrFoot_HeelMid_Guide_CtrlShape" -p "L_FrFoot_HeelMid_Guide";
	rename -uid "2E5C990B-1543-A931-AA4D-E8A0CBFC119A";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/C:\\Users\\Esteban\\Documents\\maya\\2022\\scripts\\rigging\\Mutant_Tools\\Icons\\Guide_Data";
	setAttr -k off ".v" no;
	setAttr ".ove" yes;
	setAttr ".ovc" 14;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 9 0 no 3
		10 0 1 2 3 4 5 6 7 8 9
		10
		5.8966734375000001e-06 -0.2109375 0.10546874999999999
		5.8966734375000001e-06 0.39872714062500003 0.10796456249999996
		5.8966734375000001e-06 0.31204110937499996 0.21365564062499998
		5.8966734375000001e-06 0.41773218749999996 0.39620432812499995
		5.8212421874999994e-06 0.97001803124999997 1.6344703121790762e-07
		5.8966734375000001e-06 0.41773260937500006 -0.39620432812499995
		5.8966734375000001e-06 0.31204110937499996 -0.21365521875000004
		3.0237721875000003e-06 0.39872714062500003 -0.10682760937500002
		5.8966734375000001e-06 -0.2109375 -0.10546875000000001
		5.8966734375000001e-06 -0.2109375 0.10546874999999999
		;
createNode nurbsCurve -n "L_FrFoot_HeelMid_Guide_Ctrl_CtrlShape" -p "L_FrFoot_HeelMid_Guide";
	rename -uid "01C75A7A-8449-09B1-1846-5085DFDCF34C";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/C:\\Users\\Esteban\\Documents\\maya\\2022\\scripts\\rigging\\Mutant_Tools\\Icons\\Guide_Data";
	setAttr -k off ".v" no;
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
		0 0.25068192187499999 -3.2092384305570931e-17
		-1.2973120312500001e-09 0.24687365624999996 0.043530328124999962
		-2.5551998437500003e-09 0.23556403125 0.085738499999999981
		-3.73545421875e-09 0.21709729687499998 0.12534117187499999
		-4.8022031249999996e-09 0.19203370312500001 0.16113557812500001
		-5.7230296875000004e-09 0.16113515624999999 0.19203370312500001
		-6.4700015625000009e-09 0.12534117187500002 0.21709729687499996
		-7.0203796874999994e-09 0.085738499999999995 0.23556403124999997
		-7.3574156249999999e-09 0.043530328124999997 0.24687365624999996
		-7.4708999999999991e-09 0 0.25068234375000004
		-7.3574156249999999e-09 -0.043530328124999997 0.24687365624999996
		-7.0203796874999994e-09 -0.085738499999999995 0.23556403124999997
		-6.4700015625000009e-09 -0.12534117187500002 0.21709729687499996
		-5.7230296875000004e-09 -0.16113515624999999 0.19203370312500001
		-4.8022031249999996e-09 -0.19203370312500001 0.16113557812500001
		-3.73545421875e-09 -0.21709729687499998 0.12534117187499999
		-2.5551998437500003e-09 -0.23556403125 0.085738499999999981
		-1.2973120312500001e-09 -0.24687365624999996 0.043530328124999962
		0 -0.25068192187499999 -3.2092384305570931e-17
		0 -0.24687365624999996 -0.043530328125000024
		0 -0.23556403125 -0.085738500000000023
		0 -0.21709729687499998 -0.12534117187500005
		0 -0.19203370312500001 -0.16113557812500001
		0 -0.16113515624999999 -0.19203370312500001
		0 -0.12534117187500002 -0.21709729687500001
		0 -0.085738499999999995 -0.23556445312500002
		0 -0.043530328124999997 -0.24687365624999996
		0 0 -0.25068234375000004
		0 0.043530328124999997 -0.24687365624999996
		0 0.085738499999999995 -0.23556445312500002
		0 0.12534117187500002 -0.21709729687500001
		0 0.16113515624999999 -0.19203370312500001
		0 0.19203370312500001 -0.16113557812500001
		0 0.21709729687499998 -0.12534117187500005
		0 0.23556403125 -0.085738500000000023
		0 0.24687365624999996 -0.043530328125000024
		0 0.25068192187499999 -3.2092384305570931e-17
		0.043530328124999997 0.24687365624999996 -3.2092384305570931e-17
		0.085738499999999995 0.23556403125 -3.2092384305570931e-17
		0.12534117187500002 0.21709729687499998 -3.2092384305570931e-17
		0.16113557812500001 0.19203370312500001 -3.2092384305570931e-17
		0.19203370312500001 0.16113515624999999 -3.2092384305570931e-17
		0.21709729687499998 0.12534117187500002 -3.2092384305570931e-17
		0.23556403125 0.085738499999999995 -3.2092384305570931e-17
		0.24687365624999996 0.043530328124999997 -3.2092384305570931e-17
		0.25068192187499999 0 -3.2092384305570931e-17
		0.24687365624999996 -0.043530328124999997 -3.2092384305570931e-17
		0.23556403125 -0.085738499999999995 -3.2092384305570931e-17
		0.21709729687499998 -0.12534117187500002 -3.2092384305570931e-17
		0.19203370312500001 -0.16113515624999999 -3.2092384305570931e-17
		0.16113557812500001 -0.19203370312500001 -3.2092384305570931e-17
		0.12534117187500002 -0.21709729687499998 -3.2092384305570931e-17
		0.085738499999999995 -0.23556403125 -3.2092384305570931e-17
		0.043530328124999997 -0.24687365624999996 -3.2092384305570931e-17
		0 -0.25068192187499999 -3.2092384305570931e-17
		-0.043530328124999997 -0.24687365624999996 -3.2092384305570931e-17
		-0.085738499999999995 -0.23556403125 -3.2092384305570931e-17
		-0.12534117187500002 -0.21709729687499998 -3.2092384305570931e-17
		-0.16113557812500001 -0.19203370312500001 -3.2092384305570931e-17
		-0.19203370312500001 -0.16113515624999999 -3.2092384305570931e-17
		-0.21709729687499998 -0.12534117187500002 -3.2092384305570931e-17
		-0.23556403125 -0.085738499999999995 -3.2092384305570931e-17
		-0.24687365624999996 -0.043530328124999997 -3.2092384305570931e-17
		-0.25068234375000004 0 -3.2092384305570931e-17
		-0.24687365624999996 0.043530328124999997 -3.2092384305570931e-17
		-0.23556403125 0.085738499999999995 -3.2092384305570931e-17
		-0.21709729687499998 0.12534117187500002 -3.2092384305570931e-17
		-0.19203370312500001 0.16113515624999999 -3.2092384305570931e-17
		-0.16113557812500001 0.19203370312500001 -3.2092384305570931e-17
		-0.12534117187500002 0.21709729687499998 -3.2092384305570931e-17
		-0.085738499999999995 0.23556403125 -3.2092384305570931e-17
		-0.043530328124999997 0.24687365624999996 -3.2092384305570931e-17
		0 0.25068192187499999 -3.2092384305570931e-17
		-1.2973120312500001e-09 0.24687365624999996 0.043530328124999962
		-2.5551998437500003e-09 0.23556403125 0.085738499999999981
		-3.73545421875e-09 0.21709729687499998 0.12534117187499999
		-4.8022031249999996e-09 0.19203370312500001 0.16113557812500001
		-5.7230296875000004e-09 0.16113515624999999 0.19203370312500001
		-6.4700015625000009e-09 0.12534117187500002 0.21709729687499996
		-7.0203796874999994e-09 0.085738499999999995 0.23556403124999997
		-7.3574156249999999e-09 0.043530328124999997 0.24687365624999996
		-7.4708999999999991e-09 0 0.25068234375000004
		-0.077465109374999994 0 0.23841295312500005
		-0.14734743750000001 0 0.20280628125
		-0.20280628125 0 0.14734743750000001
		-0.23841295312500005 0 0.077465109374999966
		-0.25068234375000004 0 -3.2092384305570931e-17
		-0.23841295312500005 0 -0.077465109375000035
		-0.20280628125 0 -0.14734743750000001
		-0.14734743750000001 0 -0.20280628125
		-0.077465109374999994 0 -0.23841295312500005
		0 0 -0.25068234375000004
		0.077465109374999994 0 -0.23841295312500005
		0.14734743750000001 0 -0.20280628125
		0.20280628125 0 -0.14734743750000001
		0.23841295312500005 0 -0.077465109375000035
		0.25068192187499999 0 -3.2092384305570931e-17
		0.23841295312500005 0 0.077465109374999966
		0.20280628125 0 0.14734743750000001
		0.14734743750000001 0 0.20280628125
		0.077465109374999994 0 0.23841295312500005
		-7.4708999999999991e-09 0 0.25068234375000004
		;
createNode nurbsCurve -n "L_FrFoot_HeelMid_Guide_Ctrl_Ctrl_CtrlShape" -p "L_FrFoot_HeelMid_Guide";
	rename -uid "69320C70-DE4D-C240-E0A7-68BD348AE814";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/C:\\Users\\Esteban\\Documents\\maya\\2022\\scripts\\rigging\\Mutant_Tools\\Icons\\Guide_Data";
	setAttr -k off ".v" no;
	setAttr ".ove" yes;
	setAttr ".ovc" 13;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 9 0 no 3
		10 0 1 2 3 4 5 6 7 8 9
		10
		-0.2109375 -0.10546875 -5.8966734375320924e-06
		0.39872714062500003 -0.10796456249999997 -5.8966734375320924e-06
		0.31204110937499996 -0.21365564062499998 -5.8966734375320924e-06
		0.41773218749999996 -0.39620432812499995 -5.8966734375320924e-06
		0.97001803124999997 -1.6344703125e-07 -5.8212421875320918e-06
		0.41773260937500006 0.39620432812499995 -5.8966734375320924e-06
		0.31204110937499996 0.21365521875000001 -5.8966734375320924e-06
		0.39872714062500003 0.10682760937500001 -3.0237721875320927e-06
		-0.2109375 0.10546875 -5.8966734375320924e-06
		-0.2109375 -0.10546875 -5.8966734375320924e-06
		;
createNode nurbsCurve -n "L_FrFoot_HeelMid_Guide_Ctrl_Ctrl_Ctrl_CtrlShape" -p "L_FrFoot_HeelMid_Guide";
	rename -uid "BA8B0172-6B4B-DBF9-BA24-059D4D7CD96C";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/C:\\Users\\Esteban\\Documents\\maya\\2022\\scripts\\rigging\\Mutant_Tools\\Icons\\Guide_Data";
	setAttr -k off ".v" no;
	setAttr ".ove" yes;
	setAttr ".ovc" 6;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 9 0 no 3
		10 0 1 2 3 4 5 6 7 8 9
		10
		0.10546875 5.8966734375000001e-06 -0.2109375
		0.10796456249999997 5.8966734375000001e-06 0.39872714062500003
		0.21365564062499998 5.8966734375000001e-06 0.31204110937499996
		0.39620432812499995 5.8966734375000001e-06 0.41773218749999996
		1.6344703125e-07 5.8212421874999994e-06 0.97001803124999997
		-0.39620432812499995 5.8966734375000001e-06 0.41773260937500006
		-0.21365521875000001 5.8966734375000001e-06 0.31204110937499996
		-0.10682760937500001 3.0237721875000003e-06 0.39872714062500003
		-0.10546875 5.8966734375000001e-06 -0.2109375
		0.10546875 5.8966734375000001e-06 -0.2109375
		;
createNode dagContainer -n "L_FrFootBox_Block" -p "Body";
	rename -uid "C0178DD6-5A49-2D0F-0FE4-1BA8921D3B4F";
	addAttr -ci true -sn "nts" -ln "notes" -dt "string";
	setAttr ".isc" yes;
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/FootBox.png";
	setAttr ".ctor" -type "string" "Esteban";
	setAttr ".cdat" -type "string" "2023/06/27 10:39:10";
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
	setAttr ".nts" -type "string" "['set14', 'materialInfo16', 'R_FrFootBoxBall_FootBox', 'L_FrFootBox1', 'L_FrFootBoxBall_FootBoxShape', 'materialInfo14', 'L_FrFootBoxBall_FootBox', 'R_FrFootBoxBall_FootBoxShape', 'materialInfo13', 'R_FrFootBoxAnkle_FootBox_parentConstraint1', 'transformGeometry4', 'polyCube4', 'R_FrFootBoxAnkle_FootBox', 'R_FrFootBox1', 'set15', 'L_FrFootBoxAnkle_FootBox', 'materialInfo15', 'R_FrFootBoxAnkle_FootBoxShape', 'transformGeometry3', 'L_FrFootBoxBall_FootBox_scaleConstraint1', 'L_FrFootBoxAnkle_FootBoxShape', 'R_FrFootBoxAnkle_FootBoxMirror_Grp', 'L_FrFootBoxAnkle_FootBox_scaleConstraint1', 'set16', 'R_FrFootBoxBall_FootBox_parentConstraint1', 'R_FrFootBoxAnkle_FootBox_scaleConstraint1', 'R_FrFootBoxBall_FootBoxMirror_Grp', 'L_FrFootBoxAnkle_FootBox_parentConstraint1', 'polyCube3', 'L_FrFootBox_Ctrl_Grp', 'L_FrFootBoxBall_FootBox_parentConstraint1', 'R_FrFootBoxBall_FootBox_scaleConstraint1', 'set13']";
createNode dagContainer -n "FrSmart_RFL_Block" -p "Body";
	rename -uid "8ADA3422-5A48-8205-3123-3398E0BCD7D7";
	addAttr -ci true -sn "nts" -ln "notes" -dt "string";
	setAttr ".isc" yes;
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/RFL.png";
	setAttr ".ctor" -type "string" "Esteban";
	setAttr ".cdat" -type "string" "2023/01/24 12:26:55";
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
		"['addDoubleLinear16', 'L_FrAnkle_Ik_RFL_Ctrl_Grp', 'L_FrAnkle_Ik_RFL_Ctrl_Root_Grp_scaleConstraint1', 'R_FrAnkle_Ik_RFL_Ctrl_tag', 'L_FrAnkle_Ik_RFL_Ctrl', 'addDoubleLinear19', 'addDoubleLinear18', 'unitConversion221', 'R_FrAnkle_Ik_RFL_Ctrl_GrpMirror_Grp', 'L_FrAnkle_Ik_RFL_Ctrl_tag', 'R_FrAnkle_Ik_RFL_Ctrl_Root_Grp_parentConstraint1', 'unitConversion231', 'L_Ankle_Ik_RFL_Reverse1', 'addDoubleLinear15', 'L_FrAnkle_Ik_RFL_Ctrl_Auto_Grp', 'R_FrAnkle_Ik_RFL_Ctrl_Auto_Grp', 'unitConversion224', 'unitConversion227', 'R_FrAnkle_Ik_RFL_CtrlShape', 'unitConversion220', 'addDoubleLinear20', 'L_FrAnkle_Ik_RFL_Ctrl_Root_Grp_parentConstraint1', 'addDoubleLinear25', 'R_FrAnkle_Ik_RFL_Ctrl_Root_Grp_scaleConstraint1', 'unitConversion225', 'addDoubleLinear17', 'R_FrAnkle_Ik_RFL_Ctrl', 'R_FrAnkle_Ik_RFL_Ctrl_Grp', 'unitConversion230', 'addDoubleLinear27', 'addDoubleLinear28', 'L_FrAnkle_Ik_RFL_Ctrl_Root_Grp', 'R_Ankle_Ik_RFL_Reverse1', 'addDoubleLinear21', 'unitConversion223', 'unitConversion219', 'addDoubleLinear26', 'unitConversion228', 'unitConversion232', 'unitConversion229', 'addDoubleLinear24', 'addDoubleLinear23', 'R_FrAnkle_Ik_RFL_Ctrl_Root_Grp', 'L_FrAnkle_Ik_RFL_CtrlShape', 'unitConversion226', 'addDoubleLinear22', 'unitConversion222']");
createNode dagContainer -n "Neck_Block" -p "Body";
	rename -uid "4F77F9BD-4B42-7061-C8DB-858410628E8F";
	addAttr -ci true -sn "nts" -ln "notes" -dt "string";
	setAttr ".isc" yes;
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/Ribbon.png";
	setAttr ".ctor" -type "string" "estebanrdgz";
	setAttr ".cdat" -type "string" "2025/07/26 12:16:28";
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
		"['Neck_1_follicle_Shape4', 'Neck_1_follicle_02', 'Neck_1_01_Ctrl_Offset_Grp', 'Neck_1_follicle_04', 'Neck_1_Ctrl_02_Jnt_scaleConstraint1', 'Neck_1_Ctrl_Joints_Grp', 'Neck_1_fk_03_Ctrl_offset', 'Neck_1_fk_00_CtrlShape01', 'Neck_Ctrl_Grp_parentConstraint1', 'Neck_1_skinClusterGroupParts', 'Neck_1_03_Ctrl_constr_Grp', 'Neck_1_04_Ctrl_constr_Grp_parentConstraint1', 'Neck_1_01_Ctrl_constr_Grp', 'Neck_1_follicle_Shape3', 'Neck_1_Ctrl_01_Jnt', 'Neck_1_Ctrl_04_Jnt', 'Neck_1_ribbon_surface', 'Neck_1_fk_00_Ctrl_offset', 'Neck_1_skinClusterGroupId', 'Neck_1_Bind_03_Bnd_parentConstraint1', 'Neck_1_Ctrl_03_Jnt_Offset_Grp', 'Neck_1_03_Ctrl_Offset_Grp', 'Neck_1_03_Ctrl_tag', 'Neck_1_follicle_Shape1', 'Neck_1_ribbon_surfaceShapeOrig', 'Neck_1_Ctrl_05_Jnt_parentConstraint1', 'Neck_1_Bind_04_Bnd', 'Neck_1_Main_Ctrl', 'Neck_1_Bind_03_Bnd', 'bindPose25', 'Neck_1_02_Ctrl_constr_Grp_parentConstraint1', 'Neck_1_04_Ctrl_constr_Grp', 'Neck_1_03_CtrlShape01', 'Neck_1_Ctrl_03_Jnt', 'Neck_1_Bind_02_Bnd', 'Neck_1_Bind_02_Bnd_parentConstraint1', 'Neck_1_fk_03_Ctrl_tag', 'Neck_1_01_CtrlShape01', 'Neck_1_follicle_01_scaleConstraint1', 'Neck_1_follicle_03', 'Neck_1_Ctrl_03_Jnt_scaleConstraint1', 'Neck_1_04_Ctrl_tag', 'Neck_1_follicle_05', 'Neck_1_fk_02_CtrlShape01', 'Neck_1_04_Ctrl_Offset_Grp', 'Neck_1_fk_03_Ctrl', 'Neck_1_01_Ctrl_tag', 'Neck_1_02_Ctrl_Offset_Grp', 'Neck_1_Follicles_Grp', 'Neck_1_Main_CtrlShape', 'Neck_1_Bnd_Grp', 'Neck_Ctrl_Grp', 'Neck_1_Ctrl_05_Jnt_scaleConstraint1', 'Neck_1_Bind_03_Bnd_scaleConstraint1', 'Neck_1_fk_01_CtrlShape01', 'Neck_1_follicle_Shape2', 'Neck_1_fk_00_Ctrl', 'Neck_Rig_Grp', 'Neck_1_02_Ctrl_constr_Grp', 'Neck_1_Ctrl_01_Jnt_parentConstraint1', 'Neck_1_follicle_05_scaleConstraint1', 'Neck_1_Bind_04_Bnd_scaleConstraint1', 'Neck_1_01_Ctrl', 'Neck_1_follicle_01', 'Neck_1_01_Ctrl_constr_Grp_parentConstraint1', 'Neck_1_fk_01_Ctrl_tag', 'Neck_1_Main_Ctrl_tag', 'Neck_1_Rig_Grp', 'Neck_1_03_Ctrl', 'Neck_1_02_Ctrl', 'Neck_1_Bind_04_Bnd_parentConstraint1', 'Neck_1_fk_02_Ctrl_offset', 'Neck_1_follicle_04_scaleConstraint1', 'Neck_1_follicle_Shape5', 'Neck_1_Ctrl_01_Jnt_scaleConstraint1', 'Neck_1_fk_01_Ctrl', 'Neck_1_skinCluster', 'Neck_1_Ctrl_03_Jnt_parentConstraint1', 'Neck_1_00_Ctrl_Offset_Grp', 'Neck_Ctrl_Grp_scaleConstraint1', 'Neck_1_Ctrl_05_Jnt_Offset_Grp', 'Neck_1_00_Ctrl', 'Neck_1_Ctrl_05_Jnt', 'Neck_1_03_Ctrl_constr_Grp_parentConstraint1', 'Neck_1_Bind_02_Bnd_scaleConstraint1', 'Neck_1_00_CtrlShape01', 'Neck_1_fk_03_CtrlShape01', 'Neck_1_ribbon_surfaceShape', 'Neck_1_Ctrl_Main_Offset_Grp', 'Neck_1_Ctrl_04_Jnt_parentConstraint1', 'Neck_1_Bind_01_Bnd', 'Neck_1_fk_02_Ctrl', 'Neck_1_Bind_05_Bnd_scaleConstraint1', 'Neck_1_00_Ctrl_constr_Grp_parentConstraint1', 'Neck_1_Ctrl_02_Jnt', 'Neck_1_follicle_02_scaleConstraint1', 'Neck_1_Bind_05_Bnd', 'Neck_1_Ctrls_Grp', 'Neck_1_fk_01_Ctrl_offset', 'Neck_1_Ctrl_02_Jnt_parentConstraint1', 'Neck_1_02_Ctrl_tag', 'Neck_1_fk_00_Ctrl_tag', 'Neck_1_Ctrl_02_Jnt_Offset_Grp', 'Neck_1_00_Ctrl_tag', 'Neck_1_fk_02_Ctrl_tag', 'Neck_1_00_Ctrl_constr_Grp', 'Neck_1_04_Ctrl', 'Neck_1_Ctrl_01_Jnt_Offset_Grp', 'Neck_1_04_CtrlShape01', 'Neck_1_Bind_01_Bnd_scaleConstraint1', 'Neck_1_Ctrl_04_Jnt_scaleConstraint1', 'Neck_1_follicle_03_scaleConstraint1', 'Neck_1_02_CtrlShape01', 'Neck_1_Bind_01_Bnd_parentConstraint1', 'Neck_1_Ctrl_04_Jnt_Offset_Grp', 'Neck_1_Bind_05_Bnd_parentConstraint1', 'Neck_1_skinClusterSet']");
createNode transform -n "Neck_Guide" -p "Neck_Block";
	rename -uid "625BDA63-374B-5FB3-FC81-09B339B5BD77";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/";
	setAttr ".t" -type "double3" -2.5519545396674924e-17 34.506561350435213 38.20826673153617 ;
	setAttr ".r" -type "double3" 0 89.999999999999986 0 ;
createNode nurbsSurface -n "Neck_GuideShape" -p "Neck_Guide";
	rename -uid "42EBB2CA-8248-4399-F166-61B4B2F027D4";
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
		10 0 0 0 0.19999999999999996 0.39999999999999991 0.59999999999999998 0.80000000000000004
		 1 1 1
		6 0 0 0 1 1 1
		
		32
		9.9729139604226376 -10.076849338356453 -3.2394355311153049e-16
		10.479633054229016 -8.7726265204521745 -3.2394355311153049e-16
		10.986352148035385 -7.4684037025479002 -3.2394355311153049e-16
		11.493071241841763 -6.164180884643625 -3.2394355311153049e-16
		8.6686911425183659 -9.5701302445500787 -3.2394355311153049e-16
		9.1754102363247476 -8.2659074266458035 -3.2394355311153049e-16
		9.6821293301311133 -6.9616846087415265 -3.2394355311153049e-16
		10.188848423937488 -5.6574617908372504 -3.2394355311153049e-16
		6.0602455067098218 -8.5566920569373295 -3.2394355311153049e-16
		6.5669646005161937 -7.2524692390330543 -3.2394355311153049e-16
		7.0736836943225674 -5.9482464211287791 -3.2394355311153049e-16
		7.5804027881289402 -4.644023603224503 -3.2394355311153049e-16
		1.2710529643368818 -5.212566671225022 -6.0083515937363843e-16
		2.3165092678315946 -4.282629836674797 -6.0083515937363843e-16
		3.3619655713263099 -3.3526930021245742 -6.0083515937363843e-16
		4.4074218748210239 -2.422756167574351 -6.0083515937363843e-16
		-2.0117682402172692 -0.89297207857253003 -4.9136479306771241e-16
		-0.96631193672255677 0.036964755977693831 -4.9136479306771241e-16
		0.079144366772156499 0.96690159052791835 -4.9136479306771241e-16
		1.1246006702668707 1.8968384250781423 -4.9136479306771241e-16
		-4.8015787438679407 2.2433968319116095 -4.9136479306771241e-16
		-3.7561224403732281 3.1733336664618328 -4.9136479306771241e-16
		-2.7106661368785137 4.1032705010120578 -4.9136479306771241e-16
		-1.6652098333838012 5.0332073355622837 -4.9136479306771241e-16
		-6.6614524129683925 4.3343094389010384 -4.9136479306771241e-16
		-5.615996109473679 5.2642462734512643 -4.9136479306771241e-16
		-4.570539805978969 6.1941831080014902 -4.9136479306771241e-16
		-3.525083502484252 7.1241199425517143 -4.9136479306771241e-16
		-7.5913892475186167 5.3797657423957537 -4.9136479306771241e-16
		-6.545932944023904 6.3097025769459787 -4.9136479306771241e-16
		-5.5004766405291905 7.239639411496201 -4.9136479306771241e-16
		-4.4550203370344708 8.1695762460464234 -4.9136479306771241e-16
		
		;
	setAttr ".nufa" 4.5;
	setAttr ".nvfa" 4.5;
createNode dagContainer -n "Head_Block" -p "Body";
	rename -uid "CB7F8034-0D48-6125-0AA8-85B33AF1DCAB";
	addAttr -ci true -sn "nts" -ln "notes" -dt "string";
	setAttr ".isc" yes;
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/Bone.png";
	setAttr ".ctor" -type "string" "estebanrdgz";
	setAttr ".cdat" -type "string" "2025/07/26 12:18:38";
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
	setAttr ".nts" -type "string" "['Head_Jnt_scaleConstraint1', 'Head_Gimbal_Ctrl', 'Head_Ctrl_tag', 'Head_Jnt', 'Head_Gimbal_CtrlShape', 'Head_CtrlShape', 'Head_Gimbal_Ctrl_tag', 'Head_Ctrl_Offset_Grp', 'Head_Rig_Grp', 'Head_Jnt_parentConstraint1', 'Head_Bnd', 'Head_Bnd_parentConstraint1', 'Head_Ctrl', 'Head_Bnd_scaleConstraint1']";
createNode transform -n "Head_Loc" -p "Head_Block";
	rename -uid "F0A8C475-0A49-2AB4-BA6B-7CBFD352D859";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/";
	setAttr ".t" -type "double3" 0 42.638961416617029 45.167417349677905 ;
createNode locator -n "Head_LocShape" -p "Head_Loc";
	rename -uid "D26A8E5C-2C4A-CA44-A5AD-47AEA443DB57";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/";
	setAttr -k off ".v";
createNode dagContainer -n "L_Eyes_Block" -p "Body";
	rename -uid "7ECADF59-2141-6108-9DEC-FCB6289B2058";
	addAttr -ci true -sn "nts" -ln "notes" -dt "string";
	setAttr ".isc" yes;
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/Eyes.png";
	setAttr ".ctor" -type "string" "esteban.rodriguez";
	setAttr ".cdat" -type "string" "2022/04/06 09:14:00";
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
		"['R_Eyes_Ctrl_Offset_Grp', 'effector10', 'Eyes_Main_Ctrl_Root_Grp', 'R_Eyes_Bnd_scaleConstraint1', 'R_Eyes_Jnt', 'L_Eyes_Jnt_scaleConstraint1', 'L_Eyes_Aim_IKsc_parentConstraint1', 'effector9', 'L_Eyes_Ctrl|Eyes_Attrs_Loc', 'R_Eyes_Bnd_parentConstraint1', 'L_Eyes_Jnt', 'L_Eyes_Aim_Jnt', 'R_Eyes_Ctrl_tag', 'L_Eyes_Bnd_parentConstraint1', 'EyesEye_Grp1Mirror_Grp', 'Eyes_Rig_Grp', 'Eyes_Main_Ctrl_Offset_Grp', 'L_Eyes_Ctrl', 'L_Eyes_Jnt_parentConstraint1', 'R_Eyes_Ctrl_Offset_GrpMirror_Grp', 'R_Eyes_Jnt_scaleConstraint1', 'R_Eyes_Bnd', 'Eyes_Ctrl_Grp', 'EyesEye_Grp1', 'Eyes_Rig_Grp_scaleConstraint1', 'L_Eyes_Aim_IKsc', 'R_Eyes_Ctrl', 'EyesEye_Grp', 'Eyes_Main_Ctrl_Offset_Grp_parentConstraint1', 'Eyes_Main_CtrlShape', 'L_Eyes_Bnd_scaleConstraint1', 'R_Eyes_Aim_IKsc_parentConstraint1', 'R_Eyes_Aim_Jnt', 'R_Eyes_CtrlShape', 'Eyes_Main_Ctrl_Auto_Grp', 'R_Eyes_Jnt_parentConstraint1', 'Eyes_Main_Ctrl_tag', 'L_Eyes_Bnd', 'Eyes_Ctrl_Grp_scaleConstraint1', 'L_Eyes_Ctrl_tag', 'L_Eyes_Ctrl_Offset_Grp', 'Eyes_Main_Ctrl', 'R_Eyes_Aim_IKsc', 'L_Eyes_CtrlShape']");
createNode joint -n "L_Eyes_Guide" -p "L_Eyes_Block";
	rename -uid "EF36D0D8-A54A-CCDD-1ACC-ED815F81F0C4";
	addAttr -ci true -sn "Helper" -ln "Helper" -min 0 -max 1 -en "Hide:Show" -at "enum";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/";
	setAttr ".t" -type "double3" 4.0787029266357422 48.739971160888672 57.465255737304688 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 3.1514859026678497e-13 -89.999999999998622 0 ;
	setAttr -cb on ".Helper" 1;
createNode nurbsCurve -n "L_Eyes_Guide_CtrlShape" -p "L_Eyes_Guide";
	rename -uid "CB25CB53-4149-B723-516B-3F924515D79A";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 14;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 9 0 no 3
		10 0 1 2 3 4 5 6 7 8 9
		10
		6.674210441495945e-06 -0.23875177747085718 0.1193758887354277
		6.6742104414830905e-06 0.45130341238559674 0.12220079976646282
		6.6742104409385533e-06 0.35318693692328629 0.24182833287534214
		6.6742104399980393e-06 0.47281447003216537 0.44844794112705533
		6.5888328064157569e-06 1.0979248788845533 1.8499920494036153e-07
		6.6742104440806331e-06 0.47281494753572029 -0.44844794112705
		6.6742104431401182e-06 0.35318693692328629 -0.24182785537178167
		3.422487634005541e-06 0.45130341238559674 -0.1209139276858895
		6.6742104425827273e-06 -0.23875177747085718 -0.11937588873542238
		6.674210441495945e-06 -0.23875177747085718 0.1193758887354277
		;
createNode nurbsCurve -n "L_Eyes_Guide_Ctrl_CtrlShape" -p "L_Eyes_Guide";
	rename -uid "A6804BB2-9244-252B-94EA-05918FD50F1B";
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
		3.5527136788004966e-15 0.28373690987834571 2.6605976184718391e-15
		-1.4683726283970513e-09 0.27942648528788694 0.04927024930955208
		-2.8921260954865564e-09 0.2666255699870097 0.097044002477914282
		-4.2280093449718093e-09 0.24572380687654669 0.14186869369095645
		-5.4354202433793195e-09 0.21735532067746052 0.18238296031353998
		-6.4776674119417592e-09 0.18238248280997532 0.21735532067747029
		-7.3231353354524496e-09 0.14186869369094668 0.24572380687655646
		-7.9460865683724299e-09 0.097044002477904512 0.26662556998701947
		-8.3275642166840247e-09 0.049270249309542317 0.27942648528789671
		-8.4560126925861957e-09 -7.1054273576010019e-15 0.28373738738191023
		-8.3275642166840247e-09 -0.049270249309556528 0.27942648528789671
		-7.9460865683724299e-09 -0.097044002477918723 0.26662556998701947
		-7.3231353354524496e-09 -0.14186869369096089 0.24572380687655646
		-6.4776674119417592e-09 -0.18238248280998953 0.21735532067747029
		-5.4354202433793195e-09 -0.21735532067747473 0.18238296031353998
		-4.2280093449718093e-09 -0.2457238068765609 0.14186869369095645
		-2.8921260954865564e-09 -0.26662556998702391 0.097044002477914282
		-1.4683726283970513e-09 -0.27942648528790115 0.049270249309552094
		3.5527136788004966e-15 -0.28373690987835992 2.6684728997289123e-15
		3.7769876361716788e-15 -0.27942648528790115 -0.049270249309546751
		3.9944496712068043e-15 -0.26662556998702391 -0.097044002477908953
		4.1984878286581749e-15 -0.2457238068765609 -0.14186869369095112
		4.3829053023419704e-15 -0.21735532067747473 -0.18238296031353465
		4.5420964931182165e-15 -0.18238248280998953 -0.21735532067746496
		4.6712274139813664e-15 -0.14186869369096089 -0.24572380687655113
		4.7663726240447089e-15 -0.097044002477918723 -0.26662604749056923
		4.8246391211929734e-15 -0.049270249309556528 -0.27942648528789138
		4.8442619785158536e-15 -7.1054273576010019e-15 -0.2837373873819049
		4.8246391211929734e-15 0.049270249309542317 -0.27942648528789138
		4.7663726240447089e-15 0.097044002477904512 -0.26662604749056923
		4.6712274139813664e-15 0.14186869369094668 -0.24572380687655113
		4.5420964931182165e-15 0.18238248280997532 -0.21735532067746496
		4.3829053023419704e-15 0.21735532067746052 -0.18238296031353465
		4.1984878286581749e-15 0.24572380687654669 -0.14186869369095112
		3.9944496712068043e-15 0.2666255699870097 -0.097044002477908953
		3.7769876361716788e-15 0.27942648528788694 -0.049270249309546765
		3.5527136788004966e-15 0.28373690987834571 2.6605976184718391e-15
		0.049270249309552976 0.27942648528788694 2.661341199694823e-15
		0.09704400247791517 0.2666255699870097 2.6621818420903677e-15
		0.14186869369095734 0.24572380687654669 2.6630939798768294e-15
		0.18238296031354087 0.21735532067746052 2.6640499201041067e-15
		0.21735532067747118 0.18238248280997532 2.6650206047233378e-15
		0.24572380687655734 0.14186869369094668 2.665976538323922e-15
		0.26662556998702036 0.097044002477904512 2.6668886761103837e-15
		0.2794264852878976 0.049270249309542317 2.6677293185059284e-15
		0.28373690987835637 -7.1054273576010019e-15 2.6684728997289123e-15
		0.2794264852878976 -0.049270249309556528 2.6690968426362407e-15
		0.26662556998702036 -0.097044002477918723 2.6695821882592028e-15
		0.24572380687655734 -0.14186869369096089 2.6699141855791518e-15
		0.21735532067747118 -0.18238248280998953 2.6700827355159364e-15
		0.18238296031354087 -0.21735532067747473 2.6700827421426295e-15
		0.14186869369095734 -0.2457238068765609 2.6699141855791518e-15
		0.09704400247791517 -0.26662556998702391 2.6695821882592028e-15
		0.049270249309552976 -0.27942648528790115 2.6690968426362407e-15
		3.5527136788004966e-15 -0.28373690987835992 2.6684728997289123e-15
		-0.04927024930954587 -0.27942648528790115 2.6677293185059284e-15
		-0.097044002477908065 -0.26662556998702391 2.6668886761103837e-15
		-0.14186869369095023 -0.2457238068765609 2.665976538323922e-15
		-0.18238296031353377 -0.21735532067747473 2.6650205980966446e-15
		-0.21735532067746408 -0.18238248280998953 2.6640499134774136e-15
		-0.24572380687655024 -0.14186869369096089 2.6630939798768294e-15
		-0.26662556998701326 -0.097044002477918723 2.6621818420903677e-15
		-0.27942648528789049 -0.049270249309556528 2.661341199694823e-15
		-0.28373738738190402 -7.1054273576010019e-15 2.6605976118451464e-15
		-0.27942648528789049 0.049270249309542317 2.6599736755645111e-15
		-0.26662556998701326 0.097044002477904512 2.659488329941549e-15
		-0.24572380687655024 0.14186869369094668 2.6591563326215996e-15
		-0.21735532067746408 0.18238248280997532 2.6589877826848154e-15
		-0.18238296031353377 0.21735532067746052 2.6589877760581219e-15
		-0.14186869369095023 0.24572380687654669 2.6591563326215996e-15
		-0.097044002477908065 0.2666255699870097 2.659488329941549e-15
		-0.04927024930954587 0.27942648528788694 2.6599736755645111e-15
		3.5527136788004966e-15 0.28373690987834571 2.6605976184718391e-15
		-1.4683726283970513e-09 0.27942648528788694 0.04927024930955208
		-2.8921260954865564e-09 0.2666255699870097 0.097044002477914282
		-4.2280093449718093e-09 0.24572380687654669 0.14186869369095645
		-5.4354202433793195e-09 0.21735532067746052 0.18238296031353998
		-6.4776674119417592e-09 0.18238248280997532 0.21735532067747029
		-7.3231353354524496e-09 0.14186869369094668 0.24572380687655646
		-7.9460865683724299e-09 0.097044002477904512 0.26662556998701947
		-8.3275642166840247e-09 0.049270249309542317 0.27942648528789671
		-8.4560126925861957e-09 -7.1054273576010019e-15 0.28373738738191023
		-0.087679680261947529 -7.1054273576010019e-15 0.26985015149354086
		-0.16677671162737531 -7.1054273576010019e-15 0.22954837395290614
		-0.2295483739529007 -7.1054273576010019e-15 0.16677671162738045
		-0.26985015149353486 -7.1054273576010019e-15 0.087679680261952553
		-0.28373738738190402 -7.1054273576010019e-15 2.6605976118451464e-15
		-0.26985015149353442 -7.1054273576010019e-15 -0.087679680261947224
		-0.22954837395289915 -7.1054273576010019e-15 -0.16677671162737512
		-0.16677671162737315 -7.1054273576010019e-15 -0.22954837395290081
		-0.087679680261945142 -7.1054273576010019e-15 -0.26985015149353553
		4.8442619785158536e-15 -7.1054273576010019e-15 -0.2837373873819049
		0.087679680261954634 -7.1054273576010019e-15 -0.26985015149353553
		0.16677671162738242 -7.1054273576010019e-15 -0.22954837395290081
		0.22954837395290781 -7.1054273576010019e-15 -0.16677671162737512
		0.26985015149354197 -7.1054273576010019e-15 -0.087679680261947224
		0.28373690987835637 -7.1054273576010019e-15 2.6684728997289123e-15
		0.26985015149354152 -7.1054273576010019e-15 0.087679680261952553
		0.22954837395290625 -7.1054273576010019e-15 0.16677671162738045
		0.16677671162738025 -7.1054273576010019e-15 0.22954837395290614
		0.087679680261952248 -7.1054273576010019e-15 0.26985015149354086
		-8.4560126925861957e-09 -7.1054273576010019e-15 0.28373738738191023
		;
createNode nurbsCurve -n "L_Eyes_Guide_Ctrl_Ctrl_CtrlShape" -p "L_Eyes_Guide";
	rename -uid "971F4278-8E46-BEFC-D028-849CDC85FD7C";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 13;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 9 0 no 3
		10 0 1 2 3 4 5 6 7 8 9
		10
		-0.23875177747084647 -0.11937588873543223 -6.6742104358767564e-06
		0.45130341238560751 -0.12220079976646718 -6.6742104357139211e-06
		0.35318693692329706 -0.24182833287534658 -6.6742104357354095e-06
		0.47281447003217614 -0.4484479411270596 -6.6742104357043208e-06
		1.0979248788845639 -1.8499920915270201e-07 -6.5888327999394912e-06
		0.47281494753573089 0.44844794112704578 -6.674210435716768e-06
		0.35318693692329689 0.24182785537177728 -6.6742104357421214e-06
		0.45130341238560739 0.12091392768588514 -3.4224876271331112e-06
		-0.23875177747084653 0.11937588873541782 -6.67421043588007e-06
		-0.23875177747084647 -0.11937588873543223 -6.6742104358767564e-06
		;
createNode nurbsCurve -n "L_Eyes_Guide_Ctrl_Ctrl_Ctrl_CtrlShape" -p "L_Eyes_Guide";
	rename -uid "EE72BBA2-2A4A-78C6-A42B-17A320505072";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 6;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 9 0 no 3
		10 0 1 2 3 4 5 6 7 8 9
		10
		0.11937588873542979 6.6742104313546889e-06 -0.23875177747084736
		0.12220079976646155 6.6742104313540647e-06 0.45130341238560662
		0.2418283328753415 6.6742104313275017e-06 0.35318693692329617
		0.44844794112705383 6.6742104312816196e-06 0.47281447003217525
		1.8499920060232969e-07 6.5888327957576167e-06 1.097924878884563
		-0.44844794112705155 6.6742104314807715e-06 0.47281494753573
		-0.24182785537178236 6.6742104314348945e-06 0.353186936923296
		-0.12091392768589078 3.4224876228238586e-06 0.45130341238560651
		-0.11937588873542027 6.6742104314077022e-06 -0.23875177747084741
		0.11937588873542979 6.6742104313546889e-06 -0.23875177747084736
		;
createNode joint -n "L_Eyes_Aim_Guide" -p "L_Eyes_Guide";
	rename -uid "BACE16F9-FB4E-5DBB-9DD1-22ADC65CE8B5";
	addAttr -ci true -sn "Helper" -ln "Helper" -min 0 -max 1 -en "Hide:Show" -at "enum";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/";
	setAttr ".t" -type "double3" 31.003356141256802 1.7053025658242404e-13 1.4672707493446069e-12 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 89.999999999998622 0 ;
	setAttr -cb on ".Helper" 1;
createNode nurbsCurve -n "L_Eyes_Aim_Guide_CtrlShape" -p "L_Eyes_Aim_Guide";
	rename -uid "4F246BD0-EF4B-FF6B-DDFA-B7BE6928E922";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 14;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 9 0 no 3
		10 0 1 2 3 4 5 6 7 8 9
		10
		6.6742104353868588e-06 -0.23875177747085718 0.11937588873543925
		6.6742104353963964e-06 0.45130341238559674 0.12220079976647437
		6.6742104353933751e-06 0.35318693692328629 0.24182833287535369
		6.674210435392168e-06 0.47281447003216537 0.44844794112706687
		6.5888327997834873e-06 1.0979248788845533 1.8499921650194769e-07
		6.6742104354046143e-06 0.47281494753572029 -0.44844794112703845
		6.6742104354000869e-06 0.35318693692328629 -0.24182785537177012
		3.4224876268155835e-06 0.45130341238559674 -0.12091392768587796
		6.6742104353901724e-06 -0.23875177747085718 -0.11937588873541083
		6.6742104353868588e-06 -0.23875177747085718 0.11937588873543925
		;
createNode nurbsCurve -n "L_Eyes_Aim_Guide_Ctrl_CtrlShape" -p "L_Eyes_Aim_Guide";
	rename -uid "2B145E72-5C40-297C-04CD-EFBA6C9FEF21";
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
		-3.0908556163295938e-15 0.28373690987834571 1.4210854715201999e-14
		-1.4683790484359697e-09 0.27942648528788694 0.049270249309563634
		-2.8921322989040828e-09 0.2666255699870097 0.097044002477925828
		-4.2280153452633171e-09 0.24572380687654669 0.141868693690968
		-5.4354260602092903e-09 0.21735532067746052 0.18238296031355153
		-6.4776730705512272e-09 0.18238248280997532 0.21735532067748184
		-7.32314086588693e-09 0.14186869369094668 0.245723806876568
		-7.9460920045760128e-09 0.097044002477904512 0.26662556998703102
		-8.3275695954595761e-09 0.049270249309542317 0.27942648528790826
		-8.4560180524824796e-09 -7.1054273576010034e-15 0.28373738738192178
		-8.3275695968271009e-09 -0.049270249309556528 0.27942648528790826
		-7.9460920072695246e-09 -0.097044002477918723 0.26662556998703102
		-7.3231408698245777e-09 -0.14186869369096089 0.245723806876568
		-6.4776730756133575e-09 -0.18238248280998953 0.21735532067748184
		-5.4354260662421121e-09 -0.21735532067747473 0.18238296031355153
		-4.2280153520835222e-09 -0.2457238068765609 0.141868693690968
		-2.8921323063044293e-09 -0.26662556998702391 0.097044002477925828
		-1.4683790561916127e-09 -0.27942648528790115 0.049270249309563634
		-3.098730897586667e-15 -0.28373690987835992 1.4210854715201999e-14
		-3.0979873163636847e-15 -0.27942648528790115 -0.049270249309535212
		-3.0971466739681412e-15 -0.26662556998702391 -0.097044002477897406
		-3.0962345361816799e-15 -0.2457238068765609 -0.14186869369093957
		-3.0952785959544037e-15 -0.21735532067747473 -0.18238296031352311
		-3.0943079113351731e-15 -0.18238248280998953 -0.21735532067745342
		-3.0933519777345896e-15 -0.14186869369096089 -0.24572380687653958
		-3.092439833321436e-15 -0.097044002477918723 -0.26662604749055768
		-3.0915991975525844e-15 -0.049270249309556528 -0.27942648528787983
		-3.090855609702907e-15 -7.1054273576010003e-15 -0.28373738738189336
		-3.0902316734222721e-15 0.049270249309542317 -0.27942648528787983
		-3.0897463211726169e-15 0.097044002477904512 -0.26662604749055768
		-3.0894143304793599e-15 0.14186869369094668 -0.24572380687653958
		-3.0892457805425744e-15 0.18238248280997532 -0.21735532067745342
		-3.0892457739158813e-15 0.21735532067746052 -0.18238296031352311
		-3.0894143304793579e-15 0.24572380687654669 -0.14186869369093957
		-3.0897463277993061e-15 0.2666255699870097 -0.097044002477897406
		-3.0902316734222666e-15 0.27942648528788694 -0.049270249309535212
		-3.0908556163295938e-15 0.28373690987834571 1.4210854715201999e-14
		0.049270249309546335 0.27942648528788694 1.4435128672573183e-14
		0.097044002477908523 0.2666255699870097 1.4652590707608302e-14
		0.14186869369095068 0.24572380687654669 1.4856628865059675e-14
		0.18238296031353421 0.21735532067746052 1.5041046338743473e-14
		0.21735532067746452 0.18238248280997532 1.5200237529519723e-14
		0.24572380687655068 0.14186869369094668 1.532936845038287e-14
		0.2666255699870137 0.097044002477904512 1.54245114868909e-14
		0.27942648528789094 0.049270249309542317 1.5482780157594478e-14
		0.28373690987834971 -7.1054273576010019e-15 1.5502400841362048e-14
		0.27942648528789094 -0.049270249309556528 1.5482780157594478e-14
		0.2666255699870137 -0.097044002477918723 1.54245114868909e-14
		0.24572380687655068 -0.14186869369096089 1.532936845038287e-14
		0.21735532067746452 -0.18238248280998953 1.5200237529519723e-14
		0.18238296031353421 -0.21735532067747473 1.5041046338743473e-14
		0.14186869369095068 -0.2457238068765609 1.4856628865059675e-14
		0.097044002477908523 -0.26662556998702391 1.4652590707608302e-14
		0.049270249309546321 -0.27942648528790115 1.4435128672573183e-14
		-3.098730897586667e-15 -0.28373690987835992 1.4210854715201999e-14
		-0.049270249309552525 -0.27942648528790115 1.3986580757830812e-14
		-0.097044002477914712 -0.26662556998702391 1.3769118722795687e-14
		-0.14186869369095689 -0.2457238068765609 1.3565080565344318e-14
		-0.18238296031354043 -0.21735532067747473 1.3380663091660533e-14
		-0.21735532067747074 -0.18238248280998953 1.3221471900884272e-14
		-0.2457238068765569 -0.14186869369096089 1.3092340980021126e-14
		-0.26662556998701992 -0.097044002477918723 1.2997197943513092e-14
		-0.27942648528789715 -0.049270249309556528 1.2938929272809519e-14
		-0.28373738738191068 -7.1054273576010019e-15 1.291930641548664e-14
		-0.27942648528789715 0.049270249309542317 1.2938929272809519e-14
		-0.26662556998701992 0.097044002477904512 1.2997197943513092e-14
		-0.2457238068765569 0.14186869369094668 1.3092340980021126e-14
		-0.21735532067747074 0.18238248280997532 1.3221471900884272e-14
		-0.18238296031354043 0.21735532067746052 1.3380663091660533e-14
		-0.14186869369095689 0.24572380687654669 1.3565080565344318e-14
		-0.097044002477914712 0.2666255699870097 1.3769118722795687e-14
		-0.049270249309552511 0.27942648528788694 1.3986580757830812e-14
		-3.0908556163295938e-15 0.28373690987834571 1.4210854715201999e-14
		-1.4683790484359697e-09 0.27942648528788694 0.049270249309563634
		-2.8921322989040828e-09 0.2666255699870097 0.097044002477925828
		-4.2280153452633171e-09 0.24572380687654669 0.141868693690968
		-5.4354260602092903e-09 0.21735532067746052 0.18238296031355153
		-6.4776730705512272e-09 0.18238248280997532 0.21735532067748184
		-7.32314086588693e-09 0.14186869369094668 0.245723806876568
		-7.9460920045760128e-09 0.097044002477904512 0.26662556998703102
		-8.3275695954595761e-09 0.049270249309542317 0.27942648528790826
		-8.4560180524824796e-09 -7.1054273576010034e-15 0.28373738738192178
		-0.087679680261952983 -7.1054273576010034e-15 0.26985015149355218
		-0.16677671162738089 -7.1054273576010034e-15 0.22954837395291691
		-0.22954837395290659 -7.1054273576010034e-15 0.16677671162739091
		-0.2698501514935413 -7.1054273576010019e-15 0.087679680261962906
		-0.28373738738191068 -7.1054273576010019e-15 1.291930641548664e-14
		-0.2698501514935413 -7.1054273576010011e-15 -0.087679680261936871
		-0.22954837395290659 -7.1054273576010011e-15 -0.16677671162736465
		-0.16677671162738089 -7.1054273576010003e-15 -0.22954837395289004
		-0.087679680261952983 -7.1054273576010003e-15 -0.2698501514935242
		-3.090855609702907e-15 -7.1054273576010003e-15 -0.28373738738189336
		0.087679680261946794 -7.1054273576010003e-15 -0.26985015149352376
		0.16677671162737467 -7.1054273576010003e-15 -0.22954837395288849
		0.22954837395290037 -7.1054273576010011e-15 -0.16677671162736249
		0.26985015149353508 -7.1054273576010011e-15 -0.087679680261934484
		0.28373690987834971 -7.1054273576010019e-15 1.5502400841362048e-14
		0.26985015149353508 -7.1054273576010019e-15 0.087679680261965293
		0.22954837395290037 -7.1054273576010034e-15 0.16677671162739308
		0.16677671162737467 -7.1054273576010034e-15 0.22954837395291847
		0.087679680261946794 -7.1054273576010034e-15 0.26985015149355263
		-8.4560180524824796e-09 -7.1054273576010034e-15 0.28373738738192178
		;
createNode nurbsCurve -n "L_Eyes_Aim_Guide_Ctrl_Ctrl_CtrlShape" -p "L_Eyes_Aim_Guide";
	rename -uid "C8CD6B73-9F4B-94A6-F3BD-609893159F3E";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 13;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 9 0 no 3
		10 0 1 2 3 4 5 6 7 8 9
		10
		-0.23875177747085313 -0.11937588873543223 -6.6742104254155582e-06
		0.45130341238560084 -0.12220079976646718 -6.6742104221212692e-06
		0.3531869369232904 -0.24182833287534658 -6.6742104225896699e-06
		0.47281447003216948 -0.4484479411270596 -6.6742104220185757e-06
		1.0979248788845573 -1.8499920915270201e-07 -6.5888327834107512e-06
		0.47281494753572423 0.44844794112704578 -6.6742104220185707e-06
		0.35318693692329023 0.24182785537177728 -6.6742104225896699e-06
		0.45130341238560073 0.12091392768588514 -3.4224876135370838e-06
		-0.23875177747085319 0.11937588873541782 -6.6742104254155582e-06
		-0.23875177747085313 -0.11937588873543223 -6.6742104254155582e-06
		;
createNode nurbsCurve -n "L_Eyes_Aim_Guide_Ctrl_Ctrl_Ctrl_CtrlShape" -p "L_Eyes_Aim_Guide";
	rename -uid "B27CBDFB-4942-D967-D2FC-128BD6F65F2F";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 6;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 9 0 no 3
		10 0 1 2 3 4 5 6 7 8 9
		10
		0.11937588873542203 6.6742104313546889e-06 -0.23875177747083537
		0.12220079976645698 6.6742104313540647e-06 0.4513034123856185
		0.24182833287533637 6.6742104313275017e-06 0.3531869369233086
		0.44844794112704939 6.6742104312816196e-06 0.47281447003218896
		1.8499919893724612e-07 6.5888327957576167e-06 1.0979248788845746
		-0.44844794112705599 6.6742104314807715e-06 0.47281494753573938
		-0.2418278553717875 6.6742104314348945e-06 0.35318693692330666
		-0.12091392768589534 3.4224876228238586e-06 0.45130341238561772
		-0.11937588873542802 6.6742104314077022e-06 -0.23875177747083631
		0.11937588873542203 6.6742104313546889e-06 -0.23875177747083537
		;
createNode dagContainer -n "Tail_Block" -p "Body";
	rename -uid "FF2E8AE9-B84F-F8C3-A9DA-83AB15888769";
	addAttr -ci true -sn "nts" -ln "notes" -dt "string";
	setAttr ".isc" yes;
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/Tail.png";
	setAttr ".ctor" -type "string" "estebanrdgz";
	setAttr ".cdat" -type "string" "2025/07/26 14:02:03";
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
		"['Tail_1_01_Ctrl_constr_Grp_parentConstraint1', 'Tail_1_Follicles_Grp', 'Tail_1_Rotator_Ctrl_Offset_Grp', 'Tail_1_Ctrl_Joints_Grp', 'Tail_1_02_Ctrl_constr_Grp_parentConstraint1', 'Tail_1_fk_00_CtrlShape01', 'Tail_Ctrl_Grp', 'Tail_1_Bind_03_Bnd_scaleConstraint1', 'Tail_1_Ctrls_Grp', 'Tail_1_01_Ctrl_constr_Grp', 'Tail_1_Main_Ctrl', 'Tail_1_follicle_01', 'Tail_1_fk_01_Ctrl_offset', 'Tail_1_fk_01_Ctrl_tag', 'Tail_1_Rig_Grp', 'Tail_1_fk_00_Ctrl_tag', 'Tail_1_Ctrl_03_Jnt_Offset_Grp', 'Tail_1_fk_01_Ctrl_Auto_Grp', 'Tail_1_skinClusterGroupParts', 'Tail_1_follicle_Shape2', 'Tail_1_fk_00_Ctrl_offset', 'Tail_1_skinClusterGroupId', 'bindPose26', 'Tail_1_00_Ctrl_constr_Grp_parentConstraint1', 'Tail_1_Ctrl_01_Jnt_Offset_Grp', 'Tail_1_02_Ctrl_tag', 'Tail_1_Bind_02_Bnd_parentConstraint1', 'Tail_1_Bind_03_Bnd', 'Tail_1_fk_00_Ctrl_Auto_Grp', 'Tail_1_Bnd_Grp', 'Tail_1_01_Ctrl_tag', 'Tail_1_fk_01_Ctrl_Root_Grp', 'Tail_1_00_Ctrl_Offset_Grp', 'Tail_1_Ctrl_03_Jnt', 'Tail_1_Bind_03_Bnd_parentConstraint1', 'Tail_1_follicle_Shape3', 'Tail_1_00_Ctrl_tag', 'Tail_1_00_Ctrl_constr_Grp', 'Tail_1_ribbon_surface', 'Tail_1_ribbon_surfaceShapeOrig', 'Tail_1_follicle_02', 'Tail_1_Ctrl_02_Jnt_scaleConstraint1', 'Tail_1_Bind_02_Bnd_scaleConstraint1', 'Tail_1_skinCluster', 'Tail_1_follicle_02_scaleConstraint1', 'Tail_1_Ctrl_03_Jnt_parentConstraint1', 'Tail_1_Ctrl_03_Jnt_scaleConstraint1', 'Tail_1_Bind_01_Bnd_scaleConstraint1', 'Tail_1_Main_CtrlShape', 'Tail_1_02_Ctrl_constr_Grp', 'Tail_1_follicle_Shape1', 'Tail_1_Ctrl_01_Jnt', 'Tail_Rig_Grp', 'Tail_1_01_Ctrl', 'Tail_1_Ctrl_Main_Offset_Grp', 'Tail_1_Rotator_Ctrl_tag', 'Tail_1_00_CtrlShape01', 'Tail_1_fk_00_Ctrl', 'Tail_1_follicle_03', 'Tail_1_Bind_02_Bnd', 'Tail_1_follicle_01_scaleConstraint1', 'Tail_1_Ctrl_02_Jnt_parentConstraint1', 'Tail_1_Bind_01_Bnd_parentConstraint1', 'Tail_1_follicle_03_scaleConstraint1', 'Tail_1_00_Ctrl', 'Tail_1_02_CtrlShape01', 'Tail_1_Bind_01_Bnd', 'Tail_1_ribbon_surfaceShape', 'Tail_1_02_Ctrl_Offset_Grp', 'Tail_1_Ctrl_01_Jnt_parentConstraint1', 'Tail_1_Rotator_Ctrl', 'Tail_1_fk_00_Ctrl_Root_Grp', 'Tail_1_fk_01_Ctrl', 'Tail_Ctrl_Grp_parentConstraint1', 'Tail_1_skinClusterSet', 'Tail_1_Ctrl_02_Jnt_Offset_Grp', 'Tail_1_Ctrl_01_Jnt_scaleConstraint1', 'Tail_1_01_CtrlShape01', 'Tail_Ctrl_Grp_scaleConstraint1', 'Tail_1_Ctrl_02_Jnt', 'Tail_1_Main_Ctrl_tag', 'Tail_1_02_Ctrl', 'Tail_1_01_Ctrl_Offset_Grp', 'Tail_1_fk_01_CtrlShape01', 'Tail_1_Rotator_CtrlShape']");
createNode transform -n "Tail_Guide" -p "Tail_Block";
	rename -uid "5D3B1549-2341-E9DA-5FF8-D1BCC7577664";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/";
	setAttr ".t" -type "double3" 0 18.623619313618679 -40.414520823431012 ;
createNode nurbsSurface -n "Tail_GuideShape" -p "Tail_Guide";
	rename -uid "EA597CDB-6340-4B3E-ED1D-0DBB76C51474";
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
		8 0 0 0 0.33333333333333331 0.66666666666666663 1 1 1
		6 0 0 0 1 1 1
		
		24
		-3.751101353340412e-16 4.9767682901396384 4.6626339118843951
		-3.751101353340412e-16 5.4679263518866792 4.0100016126966702
		-3.751101353340412e-16 5.9590844136337191 3.3573693135089444
		-3.751101353340412e-16 6.450242475380759 2.7047370143212195
		-2.9175232748203215e-16 3.8890477914934287 3.8440371423059956
		-2.9175232748203215e-16 4.3802058532404704 3.1914048431182698
		-2.9175232748203215e-16 4.8713639149875085 2.5387725439305444
		-2.9175232748203215e-16 5.3625219767345502 1.886140244742819
		-1.2503671177801377e-16 1.7136067942010116 2.2068436031491956
		-1.2503671177801377e-16 2.2047648559480519 1.5542113039614702
		-1.2503671177801377e-16 2.6959229176950923 0.90157900477374475
		-1.2503671177801377e-16 3.1870809794421318 0.24894670558601922
		1.2503671177801377e-16 -1.5495547017376152 -0.24894670558600479
		1.2503671177801377e-16 -1.0583966399905749 -0.90157900477373043
		1.2503671177801377e-16 -0.56723857824353519 -1.554211303961456
		1.2503671177801377e-16 -0.076080516496494832 -2.2068436031491814
		2.9175232748203205e-16 -3.7249956990300328 -1.8861402447428044
		2.9175232748203205e-16 -3.2338376372829911 -2.5387725439305302
		2.9175232748203205e-16 -2.7426795755359525 -3.1914048431182556
		2.9175232748203205e-16 -2.2515215137889122 -3.8440371423059805
		3.751101353340412e-16 -4.8127161976762425 -2.7047370143212053
		3.751101353340412e-16 -4.3215581359292026 -3.3573693135089311
		3.751101353340412e-16 -3.8304000741821627 -4.010001612696656
		3.751101353340412e-16 -3.3392420124351219 -4.6626339118843809
		
		;
	setAttr ".nufa" 4.5;
	setAttr ".nvfa" 4.5;
createNode transform -n "Spaces" -p "Mutant_Build";
	rename -uid "A665BFD0-D44B-5105-F32E-20B7B2E1D280";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/";
createNode dagContainer -n "Eyes_Switches_Block" -p "Spaces";
	rename -uid "8C36D5C7-6C45-0AAE-47DF-5F9F50558E53";
	addAttr -ci true -sn "nts" -ln "notes" -dt "string";
	setAttr ".isc" yes;
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/SpaceSwitch.png";
	setAttr ".ctor" -type "string" "esteban.rodriguez";
	setAttr ".cdat" -type "string" "2022/09/28 13:53:10";
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
	setAttr ".nts" -type "string" "['Eyes_SwitchesMutant_Tools_Grp_Condition', 'COG_Ctrl_Eyes_Switches_LocShape', 'Mutant_Tools_Grp_Eyes_Switches_Loc', 'Eyes_SwitchesCOG_Ctrl_Condition', 'Head_Jnt_Eyes_Switches_LocShape', 'Head_Jnt_Eyes_Switches_Loc_parentConstraint1', 'Mover_Gimbal_Ctrl_Eyes_Switches_LocShape', 'COG_Ctrl_Eyes_Switches_Loc', 'Mover_Gimbal_Ctrl_Eyes_Switches_Loc_parentConstraint1', 'Eyes_Switches_Rig_Grp', 'Eyes_SwitchesHead_Jnt_Condition', 'Eyes_Main_Ctrl_Auto_SpSw_Grp', 'Mutant_Tools_Grp_Eyes_Switches_LocShape', 'Eyes_Switches_locs_Grp', 'Eyes_Switches_locs_Grp_scaleConstraint1', 'COG_Ctrl_Eyes_Switches_Loc_parentConstraint1', 'Eyes_SwitchesMover_Gimbal_Ctrl_Condition', 'Head_Jnt_Eyes_Switches_Loc', 'Mutant_Tools_Grp_Eyes_Switches_Loc_parentConstraint1', 'Mover_Gimbal_Ctrl_Eyes_Switches_Loc', 'Eyes_Main_Ctrl_Auto_SpSw_Grp_parentConstraint1']";
createNode dagContainer -n "L_IK_FrLeg_Switches_Block" -p "Spaces";
	rename -uid "B5B73ECF-214B-87A4-66FB-D29EDEF6A295";
	addAttr -ci true -sn "nts" -ln "notes" -dt "string";
	setAttr ".isc" yes;
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/SpaceSwitch.png";
	setAttr ".ctor" -type "string" "esteban.rodriguez";
	setAttr ".cdat" -type "string" "2022/09/28 14:00:50";
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
		"['R_Clavicle_Jnt_R_IK_FrLeg_Switches_Loc_parentConstraint1', 'Mutant_Tools_Grp_L_IK_FrLeg_Switches_LocShape', 'R_IK_FrLeg_Switches_locs_Grp_scaleConstraint1', 'Mutant_Tools_Grp_L_IK_FrLeg_Switches_Loc', 'R_FrAnkle_Ik_Ctrl_Auto_SpSw_Grp', 'COG_Ctrl_R_IK_FrLeg_Switches_LocShape', 'R_IK_FrLeg_Switches_locs_Grp', 'Mover_Gimbal_Ctrl_R_IK_FrLeg_Switches_Loc_parentConstraint1', 'R_IK_FrLeg_SwitchesMutant_Tools_Grp_Condition', 'Mover_Gimbal_Ctrl_L_IK_FrLeg_Switches_Loc', 'L_IK_FrLeg_Switches_locs_Grp', 'L_IK_FrLeg_Switches_Rig_Grp', 'R_IK_FrLeg_SwitchesR_Clavicle_Jnt_Condition', 'COG_Ctrl_R_IK_FrLeg_Switches_Loc_parentConstraint1', 'Mutant_Tools_Grp_R_IK_FrLeg_Switches_LocShape', 'Mover_Gimbal_Ctrl_L_IK_FrLeg_Switches_LocShape', 'Mutant_Tools_Grp_L_IK_FrLeg_Switches_Loc_parentConstraint1', 'COG_Ctrl_L_IK_FrLeg_Switches_Loc', 'L_IK_FrLeg_SwitchesL_Clavicle_Jnt_Condition', 'COG_Ctrl_R_IK_FrLeg_Switches_Loc', 'Mover_Gimbal_Ctrl_L_IK_FrLeg_Switches_Loc_parentConstraint1', 'L_Clavicle_Jnt_L_IK_FrLeg_Switches_LocShape', 'Mutant_Tools_Grp_R_IK_FrLeg_Switches_Loc_parentConstraint1', 'L_IK_FrLeg_Switches_locs_Grp_scaleConstraint1', 'L_FrAnkle_Ik_Ctrl_Auto_SpSw_Grp_parentConstraint1', 'Mutant_Tools_Grp_R_IK_FrLeg_Switches_Loc', 'L_IK_FrLeg_SwitchesMover_Gimbal_Ctrl_Condition', 'COG_Ctrl_L_IK_FrLeg_Switches_LocShape', 'R_IK_FrLeg_Switches_Rig_Grp', 'R_Clavicle_Jnt_R_IK_FrLeg_Switches_Loc', 'L_Clavicle_Jnt_L_IK_FrLeg_Switches_Loc_parentConstraint1', 'L_IK_FrLeg_SwitchesCOG_Ctrl_Condition', 'L_FrAnkle_Ik_Ctrl_Auto_SpSw_Grp', 'R_Clavicle_Jnt_R_IK_FrLeg_Switches_LocShape', 'R_FrAnkle_Ik_Ctrl_Auto_SpSw_Grp_parentConstraint1', 'L_IK_FrLeg_SwitchesMutant_Tools_Grp_Condition', 'R_IK_FrLeg_SwitchesMover_Gimbal_Ctrl_Condition', 'COG_Ctrl_L_IK_FrLeg_Switches_Loc_parentConstraint1', 'L_Clavicle_Jnt_L_IK_FrLeg_Switches_Loc', 'Mover_Gimbal_Ctrl_R_IK_FrLeg_Switches_Loc', 'Mover_Gimbal_Ctrl_R_IK_FrLeg_Switches_LocShape', 'R_IK_FrLeg_SwitchesCOG_Ctrl_Condition']");
createNode dagContainer -n "L_FK_FrLeg_Switches_Block" -p "Spaces";
	rename -uid "184D3416-244C-BDBB-688D-8DA18D56F47D";
	addAttr -ci true -sn "nts" -ln "notes" -dt "string";
	setAttr ".isc" yes;
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/SpaceSwitch.png";
	setAttr ".ctor" -type "string" "esteban.rodriguez";
	setAttr ".cdat" -type "string" "2022/09/28 14:01:25";
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
		"['Mover_Gimbal_Ctrl_R_FK_FrLeg_Switches_Loc_parentConstraint1', 'L_FrHip_Fk_Ctrl_Auto_SpSw_Grp_orientConstraint1', 'Mutant_Tools_Grp_L_FK_FrLeg_Switches_Loc_parentConstraint1', 'COG_Ctrl_R_FK_FrLeg_Switches_Loc_parentConstraint1', 'R_FK_FrLeg_Switches_Rig_Grp', 'L_FK_FrLeg_SwitchesCOG_Ctrl_Condition', 'L_FK_FrLeg_SwitchesL_Clavicle_Jnt_Condition', 'Mutant_Tools_Grp_R_FK_FrLeg_Switches_LocShape', 'COG_Ctrl_L_FK_FrLeg_Switches_Loc_parentConstraint1', 'L_FK_FrLeg_SwitchesMutant_Tools_Grp_Condition', 'R_Clavicle_Jnt_R_FK_FrLeg_Switches_LocShape', 'Mutant_Tools_Grp_L_FK_FrLeg_Switches_Loc', 'Mover_Gimbal_Ctrl_R_FK_FrLeg_Switches_Loc', 'COG_Ctrl_R_FK_FrLeg_Switches_Loc', 'COG_Ctrl_L_FK_FrLeg_Switches_LocShape', 'L_Clavicle_Jnt_L_FK_FrLeg_Switches_Loc_parentConstraint1', 'R_FK_FrLeg_SwitchesCOG_Ctrl_Condition', 'R_FK_FrLeg_SwitchesMutant_Tools_Grp_Condition', 'Mutant_Tools_Grp_R_FK_FrLeg_Switches_Loc', 'L_FK_FrLeg_Switches_locs_Grp_scaleConstraint1', 'Mover_Gimbal_Ctrl_L_FK_FrLeg_Switches_Loc', 'COG_Ctrl_R_FK_FrLeg_Switches_LocShape', 'R_FK_FrLeg_Switches_locs_Grp_scaleConstraint1', 'R_FrHip_Fk_Ctrl_Auto_SpSw_Grp', 'L_FK_FrLeg_Switches_Rig_Grp', 'L_Clavicle_Jnt_L_FK_FrLeg_Switches_Loc', 'Mover_Gimbal_Ctrl_L_FK_FrLeg_Switches_LocShape', 'Mover_Gimbal_Ctrl_L_FK_FrLeg_Switches_Loc_parentConstraint1', 'R_FK_FrLeg_SwitchesMover_Gimbal_Ctrl_Condition', 'L_FrHip_Fk_Ctrl_Auto_SpSw_Grp', 'COG_Ctrl_L_FK_FrLeg_Switches_Loc', 'L_FK_FrLeg_SwitchesMover_Gimbal_Ctrl_Condition', 'R_FrHip_Fk_Ctrl_Auto_SpSw_Grp_orientConstraint1', 'L_Clavicle_Jnt_L_FK_FrLeg_Switches_LocShape', 'R_FK_FrLeg_SwitchesR_Clavicle_Jnt_Condition', 'L_FK_FrLeg_Switches_locs_Grp', 'Mutant_Tools_Grp_L_FK_FrLeg_Switches_LocShape', 'R_FK_FrLeg_Switches_locs_Grp', 'R_Clavicle_Jnt_R_FK_FrLeg_Switches_Loc', 'R_Clavicle_Jnt_R_FK_FrLeg_Switches_Loc_parentConstraint1', 'Mutant_Tools_Grp_R_FK_FrLeg_Switches_Loc_parentConstraint1', 'Mover_Gimbal_Ctrl_R_FK_FrLeg_Switches_LocShape']");
createNode dagContainer -n "L_PV_FrLeg_Switches_Block" -p "Spaces";
	rename -uid "03A93D16-BE4B-C444-C0BA-7B8E14D9285C";
	addAttr -ci true -sn "nts" -ln "notes" -dt "string";
	setAttr ".isc" yes;
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/SpaceSwitch.png";
	setAttr ".ctor" -type "string" "esteban.rodriguez";
	setAttr ".cdat" -type "string" "2022/09/28 14:02:03";
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
		"['Mover_Gimbal_Ctrl_L_PV_FrLeg_Switches_LocShape', 'L_FrAnkle_Ik_PoleVector_Ctrl_Auto_SpSw_Grp', 'L_FrAnkle_Ik_Ctrl_L_PV_FrLeg_Switches_Loc_parentConstraint1', 'COG_Gimbal_Ctrl_L_PV_FrLeg_Switches_Loc', 'L_PV_FrLeg_SwitchesL_FrAnkle_Ik_Ctrl_Condition', 'R_FrAnkle_Ik_PoleVector_Ctrl_Auto_SpSw_Grp_parentConstraint1', 'R_PV_FrLeg_SwitchesMover_Gimbal_Ctrl_Condition', 'R_PV_FrLeg_SwitchesCOG_Gimbal_Ctrl_Condition', 'Mutant_Tools_Grp_L_PV_FrLeg_Switches_Loc_parentConstraint1', 'Mutant_Tools_Grp_R_PV_FrLeg_Switches_Loc', 'L_FrAnkle_Ik_Ctrl_L_PV_FrLeg_Switches_Loc', 'L_PV_FrLeg_Switches_Rig_Grp', 'Mover_Gimbal_Ctrl_R_PV_FrLeg_Switches_Loc_parentConstraint1', 'Mutant_Tools_Grp_R_PV_FrLeg_Switches_Loc_parentConstraint1', 'R_FrAnkle_Ik_Ctrl_R_PV_FrLeg_Switches_Loc', 'R_FrAnkle_Ik_PoleVector_Ctrl_Auto_SpSw_Grp', 'R_FrAnkle_Ik_Ctrl_R_PV_FrLeg_Switches_LocShape', 'R_PV_FrLeg_SwitchesMutant_Tools_Grp_Condition', 'L_FrAnkle_Ik_PoleVector_Ctrl_Auto_SpSw_Grp_parentConstraint1', 'Mover_Gimbal_Ctrl_L_PV_FrLeg_Switches_Loc_parentConstraint1', 'L_PV_FrLeg_Switches_locs_Grp_scaleConstraint1', 'L_FrAnkle_Ik_Ctrl_L_PV_FrLeg_Switches_LocShape', 'R_FrAnkle_Ik_Ctrl_R_PV_FrLeg_Switches_Loc_parentConstraint1', 'R_PV_FrLeg_Switches_locs_Grp_scaleConstraint1', 'Mover_Gimbal_Ctrl_R_PV_FrLeg_Switches_LocShape', 'Mover_Gimbal_Ctrl_R_PV_FrLeg_Switches_Loc', 'R_PV_FrLeg_SwitchesR_FrAnkle_Ik_Ctrl_Condition', 'COG_Gimbal_Ctrl_R_PV_FrLeg_Switches_Loc', 'COG_Gimbal_Ctrl_L_PV_FrLeg_Switches_LocShape', 'Mutant_Tools_Grp_L_PV_FrLeg_Switches_Loc', 'COG_Gimbal_Ctrl_R_PV_FrLeg_Switches_Loc_parentConstraint1', 'L_PV_FrLeg_SwitchesMover_Gimbal_Ctrl_Condition', 'L_PV_FrLeg_SwitchesMutant_Tools_Grp_Condition', 'COG_Gimbal_Ctrl_R_PV_FrLeg_Switches_LocShape', 'R_PV_FrLeg_Switches_locs_Grp', 'L_PV_FrLeg_SwitchesCOG_Gimbal_Ctrl_Condition', 'COG_Gimbal_Ctrl_L_PV_FrLeg_Switches_Loc_parentConstraint1', 'Mutant_Tools_Grp_R_PV_FrLeg_Switches_LocShape', 'Mutant_Tools_Grp_L_PV_FrLeg_Switches_LocShape', 'Mover_Gimbal_Ctrl_L_PV_FrLeg_Switches_Loc', 'R_PV_FrLeg_Switches_Rig_Grp', 'L_PV_FrLeg_Switches_locs_Grp']");
createNode dagContainer -n "L_IK_Hip_Switches_Block" -p "Spaces";
	rename -uid "5AF8A997-554B-D589-6D11-D3BC8E4EB548";
	addAttr -ci true -sn "nts" -ln "notes" -dt "string";
	setAttr ".isc" yes;
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/SpaceSwitch.png";
	setAttr ".ctor" -type "string" "esteban.rodriguez";
	setAttr ".cdat" -type "string" "2022/09/28 14:03:34";
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
		"['R_IK_Hip_Switches_locs_Grp_scaleConstraint1', 'R_Ankle_Ik_Ctrl_Auto_SpSw_Grp', 'R_IK_Hip_SwitchesMover_Gimbal_Ctrl_Condition', 'COG_Ctrl_R_IK_Hip_Switches_LocShape', 'Mover_Gimbal_Ctrl_L_IK_Hip_Switches_Loc', 'COG_Ctrl_R_IK_Hip_Switches_Loc_parentConstraint1', 'R_IK_Hip_Switches_locs_Grp', 'L_Pelvis_Jnt_L_IK_Hip_Switches_LocShape', 'L_Pelvis_Jnt_L_IK_Hip_Switches_Loc_parentConstraint1', 'L_Ankle_Ik_Ctrl_Auto_SpSw_Grp_parentConstraint1', 'R_Ankle_Ik_Ctrl_Auto_SpSw_Grp_parentConstraint1', 'Mutant_Tools_Grp_L_IK_Hip_Switches_Loc', 'Mover_Gimbal_Ctrl_R_IK_Hip_Switches_Loc', 'COG_Ctrl_L_IK_Hip_Switches_LocShape', 'L_IK_Hip_SwitchesMutant_Tools_Grp_Condition', 'Mover_Gimbal_Ctrl_L_IK_Hip_Switches_Loc_parentConstraint1', 'L_IK_Hip_Switches_locs_Grp', 'COG_Ctrl_L_IK_Hip_Switches_Loc', 'R_IK_Hip_SwitchesCOG_Ctrl_Condition', 'R_Pelvis_Jnt_R_IK_Hip_Switches_Loc', 'Mover_Gimbal_Ctrl_R_IK_Hip_Switches_Loc_parentConstraint1', 'L_IK_Hip_Switches_Rig_Grp', 'Mutant_Tools_Grp_R_IK_Hip_Switches_LocShape', 'Mutant_Tools_Grp_L_IK_Hip_Switches_Loc_parentConstraint1', 'Mover_Gimbal_Ctrl_R_IK_Hip_Switches_LocShape', 'Mover_Gimbal_Ctrl_L_IK_Hip_Switches_LocShape', 'L_IK_Hip_SwitchesL_Pelvis_Jnt_Condition', 'Mutant_Tools_Grp_L_IK_Hip_Switches_LocShape', 'L_Ankle_Ik_Ctrl_Auto_SpSw_Grp', 'R_Pelvis_Jnt_R_IK_Hip_Switches_LocShape', 'COG_Ctrl_L_IK_Hip_Switches_Loc_parentConstraint1', 'Mutant_Tools_Grp_R_IK_Hip_Switches_Loc_parentConstraint1', 'L_IK_Hip_Switches_locs_Grp_scaleConstraint1', 'COG_Ctrl_R_IK_Hip_Switches_Loc', 'L_IK_Hip_SwitchesMover_Gimbal_Ctrl_Condition', 'R_IK_Hip_Switches_Rig_Grp', 'Mutant_Tools_Grp_R_IK_Hip_Switches_Loc', 'R_Pelvis_Jnt_R_IK_Hip_Switches_Loc_parentConstraint1', 'R_IK_Hip_SwitchesMutant_Tools_Grp_Condition', 'L_IK_Hip_SwitchesCOG_Ctrl_Condition', 'L_Pelvis_Jnt_L_IK_Hip_Switches_Loc', 'R_IK_Hip_SwitchesR_Pelvis_Jnt_Condition']");
createNode dagContainer -n "L_FK_Hip_Switches_Block" -p "Spaces";
	rename -uid "FCE68F11-3241-A4EA-EEFD-32AC19A5CB1D";
	addAttr -ci true -sn "nts" -ln "notes" -dt "string";
	setAttr ".isc" yes;
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/SpaceSwitch.png";
	setAttr ".ctor" -type "string" "esteban.rodriguez";
	setAttr ".cdat" -type "string" "2022/09/28 14:04:03";
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
		"['L_Pelvis_Jnt_L_FK_Hip_Switches_Loc_parentConstraint1', 'COG_Ctrl_R_FK_Hip_Switches_Loc', 'L_FK_Hip_SwitchesL_Pelvis_Jnt_Condition', 'COG_Ctrl_R_FK_Hip_Switches_Loc_parentConstraint1', 'L_FK_Hip_SwitchesMover_Gimbal_Ctrl_Condition', 'Mover_Gimbal_Ctrl_R_FK_Hip_Switches_LocShape', 'COG_Ctrl_L_FK_Hip_Switches_LocShape', 'COG_Ctrl_R_FK_Hip_Switches_LocShape', 'Mutant_Tools_Grp_R_FK_Hip_Switches_LocShape', 'L_FK_Hip_Switches_Rig_Grp', 'R_Hip_Fk_Ctrl_Auto_SpSw_Grp', 'L_FK_Hip_SwitchesCOG_Ctrl_Condition', 'R_FK_Hip_SwitchesMutant_Tools_Grp_Condition', 'R_FK_Hip_SwitchesMover_Gimbal_Ctrl_Condition', 'R_FK_Hip_Switches_locs_Grp', 'R_FK_Hip_SwitchesR_Pelvis_Jnt_Condition', 'R_Pelvis_Jnt_R_FK_Hip_Switches_Loc_parentConstraint1', 'R_FK_Hip_SwitchesCOG_Ctrl_Condition', 'L_FK_Hip_SwitchesMutant_Tools_Grp_Condition', 'L_Hip_Fk_Ctrl_Auto_SpSw_Grp_orientConstraint1', 'R_Pelvis_Jnt_R_FK_Hip_Switches_Loc', 'L_Pelvis_Jnt_L_FK_Hip_Switches_Loc', 'L_FK_Hip_Switches_locs_Grp_scaleConstraint1', 'Mutant_Tools_Grp_R_FK_Hip_Switches_Loc_parentConstraint1', 'Mutant_Tools_Grp_L_FK_Hip_Switches_Loc_parentConstraint1', 'COG_Ctrl_L_FK_Hip_Switches_Loc_parentConstraint1', 'L_FK_Hip_Switches_locs_Grp', 'R_Pelvis_Jnt_R_FK_Hip_Switches_LocShape', 'R_FK_Hip_Switches_locs_Grp_scaleConstraint1', 'Mover_Gimbal_Ctrl_L_FK_Hip_Switches_LocShape', 'Mutant_Tools_Grp_L_FK_Hip_Switches_LocShape', 'L_Hip_Fk_Ctrl_Auto_SpSw_Grp', 'Mover_Gimbal_Ctrl_L_FK_Hip_Switches_Loc', 'Mutant_Tools_Grp_L_FK_Hip_Switches_Loc', 'R_Hip_Fk_Ctrl_Auto_SpSw_Grp_orientConstraint1', 'L_Pelvis_Jnt_L_FK_Hip_Switches_LocShape', 'COG_Ctrl_L_FK_Hip_Switches_Loc', 'Mutant_Tools_Grp_R_FK_Hip_Switches_Loc', 'R_FK_Hip_Switches_Rig_Grp', 'Mover_Gimbal_Ctrl_L_FK_Hip_Switches_Loc_parentConstraint1', 'Mover_Gimbal_Ctrl_R_FK_Hip_Switches_Loc_parentConstraint1', 'Mover_Gimbal_Ctrl_R_FK_Hip_Switches_Loc']");
createNode dagContainer -n "L_PV_Hip_Switches_Block" -p "Spaces";
	rename -uid "8B122122-0844-5B09-58F8-5AAD0F247897";
	addAttr -ci true -sn "nts" -ln "notes" -dt "string";
	setAttr ".isc" yes;
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/SpaceSwitch.png";
	setAttr ".ctor" -type "string" "esteban.rodriguez";
	setAttr ".cdat" -type "string" "2022/09/28 14:04:33";
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
		"['R_PV_Hip_Switches_locs_Grp_scaleConstraint1', 'R_PV_Hip_SwitchesR_Ankle_Ik_Ctrl_Condition', 'Mover_Gimbal_Ctrl_L_PV_Hip_Switches_LocShape', 'COG_Gimbal_Ctrl_L_PV_Hip_Switches_Loc', 'COG_Gimbal_Ctrl_R_PV_Hip_Switches_Loc_parentConstraint1', 'Mutant_Tools_Grp_L_PV_Hip_Switches_Loc', 'L_Ankle_Ik_Ctrl_L_PV_Hip_Switches_LocShape', 'R_Ankle_Ik_Ctrl_R_PV_Hip_Switches_Loc_parentConstraint1', 'Mutant_Tools_Grp_L_PV_Hip_Switches_Loc_parentConstraint1', 'Mutant_Tools_Grp_L_PV_Hip_Switches_LocShape', 'L_PV_Hip_Switches_locs_Grp', 'L_PV_Hip_SwitchesL_Ankle_Ik_Ctrl_Condition', 'R_PV_Hip_Switches_Rig_Grp', 'R_Ankle_Ik_PoleVector_Ctrl_Auto_SpSw_Grp_parentConstraint1', 'Mover_Gimbal_Ctrl_R_PV_Hip_Switches_Loc_parentConstraint1', 'L_PV_Hip_Switches_Rig_Grp', 'L_PV_Hip_SwitchesMover_Gimbal_Ctrl_Condition', 'L_Ankle_Ik_Ctrl_L_PV_Hip_Switches_Loc_parentConstraint1', 'Mover_Gimbal_Ctrl_R_PV_Hip_Switches_Loc', 'R_PV_Hip_SwitchesCOG_Gimbal_Ctrl_Condition', 'Mutant_Tools_Grp_R_PV_Hip_Switches_LocShape', 'COG_Gimbal_Ctrl_L_PV_Hip_Switches_LocShape', 'R_PV_Hip_SwitchesMutant_Tools_Grp_Condition', 'Mutant_Tools_Grp_R_PV_Hip_Switches_Loc_parentConstraint1', 'L_Ankle_Ik_PoleVector_Ctrl_Auto_SpSw_Grp', 'L_Ankle_Ik_Ctrl_L_PV_Hip_Switches_Loc', 'Mover_Gimbal_Ctrl_L_PV_Hip_Switches_Loc_parentConstraint1', 'L_PV_Hip_SwitchesMutant_Tools_Grp_Condition', 'R_PV_Hip_SwitchesMover_Gimbal_Ctrl_Condition', 'L_Ankle_Ik_PoleVector_Ctrl_Auto_SpSw_Grp_parentConstraint1', 'COG_Gimbal_Ctrl_R_PV_Hip_Switches_Loc', 'L_PV_Hip_Switches_locs_Grp_scaleConstraint1', 'Mutant_Tools_Grp_R_PV_Hip_Switches_Loc', 'L_PV_Hip_SwitchesCOG_Gimbal_Ctrl_Condition', 'R_Ankle_Ik_PoleVector_Ctrl_Auto_SpSw_Grp', 'COG_Gimbal_Ctrl_R_PV_Hip_Switches_LocShape', 'R_Ankle_Ik_Ctrl_R_PV_Hip_Switches_LocShape', 'R_PV_Hip_Switches_locs_Grp', 'Mover_Gimbal_Ctrl_R_PV_Hip_Switches_LocShape', 'Mover_Gimbal_Ctrl_L_PV_Hip_Switches_Loc', 'R_Ankle_Ik_Ctrl_R_PV_Hip_Switches_Loc', 'COG_Gimbal_Ctrl_L_PV_Hip_Switches_Loc_parentConstraint1']");
createNode transform -n "Attrs" -p "Mutant_Build";
	rename -uid "0FCEAD05-5A46-9E35-B998-5E895970072C";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/";
createNode dagContainer -n "L_Arm_Attrs_Block" -p "Attrs";
	rename -uid "9281A82D-D244-EB91-AD0C-D0B69EDC2747";
	addAttr -ci true -sn "nts" -ln "notes" -dt "string";
	setAttr ".isc" yes;
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/ProxyAttr.png";
	setAttr ".ctor" -type "string" "esteban.rodriguez";
	setAttr ".cdat" -type "string" "2022/05/03 15:20:00";
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
	setAttr ".nts" -type "string" "['L_FrHip_Jnt_Switch_Ctrl_Offset_Grp', 'L_FrHip_Jnt_Switch_Ctrl_tag', 'L_FrHip_Jnt_Switch_Ctrl', 'L_FrHip_Jnt_Switch_Ctrl_Offset_Grp_parentConstraint1', 'L_Arm_Attrs_Ctrl_Grp', 'L_FrHip_Jnt_Switch_CtrlShape', 'L_FrHip_Jnt_Switch_Ctrl_Offset_Grp_scaleConstraint1']";
createNode dagContainer -n "R_Arm_Attrs_Block" -p "Attrs";
	rename -uid "3D7D6479-9E42-08BC-FC23-B5958FFE612B";
	addAttr -ci true -sn "nts" -ln "notes" -dt "string";
	setAttr ".isc" yes;
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/ProxyAttr.png";
	setAttr ".ctor" -type "string" "esteban.rodriguez";
	setAttr ".cdat" -type "string" "2022/05/03 15:20:06";
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
	setAttr ".nts" -type "string" "['R_Arm_Attrs_Ctrl_Grp', 'R_FrHip_Jnt_Switch_Ctrl_Offset_Grp_parentConstraint1', 'R_FrHip_Jnt_Switch_Ctrl_tag', 'R_FrHip_Jnt_Switch_Ctrl_Offset_Grp', 'R_FrHip_Jnt_Switch_CtrlShape', 'R_FrHip_Jnt_Switch_Ctrl_Offset_Grp_scaleConstraint1', 'R_FrHip_Jnt_Switch_Ctrl']";
createNode dagContainer -n "L_Legs_Attrs_Block" -p "Attrs";
	rename -uid "71CD59B3-2746-BA55-07E4-1B9941E6A09C";
	addAttr -ci true -sn "nts" -ln "notes" -dt "string";
	setAttr ".isc" yes;
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/ProxyAttr.png";
	setAttr ".ctor" -type "string" "esteban.rodriguez";
	setAttr ".cdat" -type "string" "2022/05/03 15:20:16";
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
	setAttr ".nts" -type "string" "['L_Hip_Jnt_Switch_Ctrl_Offset_Grp', 'L_Legs_Attrs_Ctrl_Grp', 'L_Hip_Jnt_Switch_Ctrl', 'L_Hip_Jnt_Switch_CtrlShape', 'L_Hip_Jnt_Switch_Ctrl_tag', 'L_Hip_Jnt_Switch_Ctrl_Offset_Grp_scaleConstraint1', 'L_Hip_Jnt_Switch_Ctrl_Offset_Grp_parentConstraint1']";
createNode dagContainer -n "R_Legs_Attrs_Block" -p "Attrs";
	rename -uid "66B6EDBB-9248-877E-1746-7A9983EEB2AF";
	addAttr -ci true -sn "nts" -ln "notes" -dt "string";
	setAttr ".isc" yes;
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/ProxyAttr.png";
	setAttr ".ctor" -type "string" "esteban.rodriguez";
	setAttr ".cdat" -type "string" "2022/05/03 15:20:20";
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
	setAttr ".nts" -type "string" "['R_Hip_Jnt_Switch_Ctrl_Offset_Grp_scaleConstraint1', 'R_Hip_Jnt_Switch_Ctrl_tag', 'R_Hip_Jnt_Switch_Ctrl_Offset_Grp', 'R_Legs_Attrs_Ctrl_Grp', 'R_Hip_Jnt_Switch_Ctrl_Offset_Grp_parentConstraint1', 'R_Hip_Jnt_Switch_Ctrl', 'R_Hip_Jnt_Switch_CtrlShape']";
createNode transform -n "Data" -p "Mutant_Build";
	rename -uid "D76D11CD-C64F-5A75-5D76-AD9182CAE5AF";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/C:\\Users\\Esteban\\Documents\\maya\\2022\\scripts\\rigging\\Mutant_Tools\\Icons\\Guide_Data";
createNode dagContainer -n "Load_Skin_Block" -p "Data";
	rename -uid "87588093-B249-F31E-E8AD-19B20ABEF9C0";
	addAttr -ci true -sn "nts" -ln "notes" -dt "string";
	setAttr ".isc" yes;
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/Skin.png";
	setAttr ".ctor" -type "string" "PC";
	setAttr ".cdat" -type "string" "2021/09/19 08:58:27";
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
createNode dagContainer -n "Load_Ctrls_Block" -p "Data";
	rename -uid "63E83BE7-1849-D64B-55F8-78A805D333F6";
	addAttr -ci true -sn "nts" -ln "notes" -dt "string";
	setAttr ".isc" yes;
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/Controller.png";
	setAttr ".ctor" -type "string" "PC";
	setAttr ".cdat" -type "string" "2021/09/19 09:05:09";
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
createNode transform -n "Extras" -p "Mutant_Build";
	rename -uid "6FC8A15C-4C42-0C42-1A82-07B3F19963CE";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/C:\\Users\\Esteban\\Documents\\maya\\2022\\scripts\\rigging\\Mutant_Tools\\Icons\\Guide_Data";
createNode dagContainer -n "Unselectable_Block" -p "Extras";
	rename -uid "039B0449-284A-EA35-E86E-1CB8AF5272C7";
	addAttr -ci true -sn "nts" -ln "notes" -dt "string";
	setAttr ".isc" yes;
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/Unselectable.png";
	setAttr ".ctor" -type "string" "Stellar Creative lab";
	setAttr ".cdat" -type "string" "2022/04/26 11:26:18";
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
createNode dagContainer -n "DinamicScale_Block" -p "Extras";
	rename -uid "9D44275C-6D46-6CFC-665F-55BB91F0862E";
	addAttr -ci true -sn "nts" -ln "notes" -dt "string";
	setAttr ".isc" yes;
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/ExtraScales.png";
	setAttr ".ctor" -type "string" "info";
	setAttr ".cdat" -type "string" "2022/09/30 14:35:10";
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
	setAttr ".nts" -type "string" "['dyn_parentNode_3_offset', 'Mover_Gimbal_Ctrl_grp_scaleConstraint1', 'dyn_parentNode_0_ctrl', 'master_2_xform', 'scale_reader_dcmpMtx', 'DynamicParentsGroup', '_1_CtrlShape1', 'dyn_parentNode_1_offset', '_4_CtrlShape2', '_5_CtrlShape1', 'dyn_parentNode_1_zero', '_2_CtrlShape1', 'dyn_parentNode_3_zero', 'dyn_parentNode_0_zero', 'Mover_Gimbal_Ctrl_grp', 'dyn_parentNode_4_zero', 'Mover_Gimbal_Ctrl_grp_parentConstraint1', 'dyn_parentNode_3_ctrl', 'dyn_parentNode_4_ctrl', '_3_CtrlShape1', 'dyn_parentNode_1_ctrl', 'dyn_parentNode_2_ctrl_inverse_md', 'dyn_parentNode_1_ctrl_inverse_md', 'dyn_parentNode_2_ctrl', 'dyn_parentNode_4_ctrl_inverse_md', 'dyn_parentNode_2_offset', 'scale_reader', 'dyn_parentNode_2_zero', 'dyn_parentNode_0_ctrl_inverse_md', '_4_CtrlShape1', 'dyn_parentNode_4_offset', 'dyn_parentNode_0_offset', 'dyn_parentNode_3_ctrl_inverse_md']";
createNode dagContainer -n "Code_Block" -p "Extras";
	rename -uid "29D5B2BA-9641-422D-CD3E-EBA105C44CD0";
	addAttr -ci true -sn "nts" -ln "notes" -dt "string";
	setAttr ".isc" yes;
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/CODE.png";
	setAttr ".ctor" -type "string" "PC";
	setAttr ".cdat" -type "string" "2021/09/19 09:07:23";
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
createNode transform -n "Code_Loc" -p "Code_Block";
	rename -uid "C57CA981-2B45-4860-2903-A7ABC809C8B7";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/C:\\Users\\Esteban\\Documents\\maya\\2022\\scripts\\rigging\\Mutant_Tools\\Icons\\Guide_Data";
createNode locator -n "Code_LocShape" -p "Code_Loc";
	rename -uid "CF4D5572-3B42-5E19-607C-439BCB3F495B";
	setAttr ".icn" -type "string" "/Users/estebanrdgz/Library/Preferences/Autodesk/maya/2024/scripts/Mutant_Tools/Icons/C:\\Users\\Esteban\\Documents\\maya\\2022\\scripts\\rigging\\Mutant_Tools\\Icons\\Guide_Data";
	setAttr -k off ".v";
createNode hyperLayout -n "hyperLayout13";
	rename -uid "6C9BA44C-694E-D7C4-FD7E-27A868900543";
	setAttr ".ihi" 0;
createNode network -n "BaseA_Config";
	rename -uid "24F9B194-0D41-76E3-3BB7-B89685187BBA";
	addAttr -ci true -sn "precode" -ln "precode" -dt "string";
	addAttr -ci true -sn "Build_Command" -ln "Build_Command" -dt "string";
	addAttr -ci true -sn "Import_Command" -ln "Import_Command" -dt "string";
	addAttr -ci true -sn "Name" -ln "Name" -dt "string";
	addAttr -ci true -sn "CtrlScale" -ln "CtrlScale" -dv 4 -min 1 -max 20 -at "long";
	addAttr -ci true -sn "CtrlColor" -ln "CtrlColor" -min 0 -max 7 -en "lightBlue:blue:white:purple:green:red:yellow:grey" 
		-at "enum";
	addAttr -ci true -sn "postcode" -ln "postcode" -dt "string";
	setAttr ".precode" -type "string" "";
	setAttr -l on ".Build_Command" -type "string" "exec_baseA.build_baseA_block()";
	setAttr -l on ".Import_Command" -type "string" "import exec_baseA ";
	setAttr ".Name" -type "string" "Mutant_Tools";
	setAttr -k on ".CtrlScale";
	setAttr -cb on ".CtrlColor";
	setAttr ".postcode" -type "string" "";
createNode hyperLayout -n "hyperLayout14";
	rename -uid "E5311D7B-7844-2129-21D8-7E9840423610";
	setAttr ".ihi" 0;
createNode network -n "Root_Config";
	rename -uid "D68FEED1-F342-BB1E-2CB3-548C4F427414";
	addAttr -ci true -sn "precode" -ln "precode" -dt "string";
	addAttr -ci true -sn "Build_Command" -ln "Build_Command" -dt "string";
	addAttr -ci true -sn "Import_Command" -ln "Import_Command" -dt "string";
	addAttr -ci true -sn "SetParent" -ln "SetParent" -dt "string";
	addAttr -ci true -sn "postcode" -ln "postcode" -dt "string";
	setAttr ".precode" -type "string" "";
	setAttr -l on ".Build_Command" -type "string" "exec_root.build_root_block()";
	setAttr -l on ".Import_Command" -type "string" "import exec_root";
	setAttr ".SetParent" -type "string" "Bind_Joints_Grp";
	setAttr ".postcode" -type "string" "";
createNode hyperLayout -n "hyperLayout15";
	rename -uid "C93E1D56-EF4B-3F1D-CA1E-0E880A66C6DB";
	setAttr ".ihi" 0;
	setAttr -s 2 ".hyp";
createNode network -n "COG_Config";
	rename -uid "4F7D9D0B-A548-7587-69DB-B5AEE6ED3547";
	addAttr -ci true -sn "precode" -ln "precode" -dt "string";
	addAttr -ci true -sn "Build_Command" -ln "Build_Command" -dt "string";
	addAttr -ci true -sn "Import_Command" -ln "Import_Command" -dt "string";
	addAttr -ci true -sn "SetCtrlParent" -ln "SetCtrlParent" -dt "string";
	addAttr -ci true -sn "CtrlType" -ln "CtrlType" -min 0 -max 16 -en "sphere:cube:square:octagon:hexagon:pringle:feet:hand:circleX:circleY:circleZ:3dArrow:2dArrow:mover:2dArrow:root:cog" 
		-at "enum";
	addAttr -ci true -sn "CtrlSize" -ln "CtrlSize" -dv 4 -min 1 -max 20 -at "long";
	addAttr -ci true -sn "CtrlColor" -ln "CtrlColor" -min 0 -max 7 -en "lightBlue:blue:white:purple:green:red:yellow:grey" 
		-at "enum";
	addAttr -ci true -sn "Gimbal" -ln "Gimbal" -min 0 -max 1 -at "bool";
	addAttr -ci true -sn "CreateJoint" -ln "CreateJoint" -min 0 -max 1 -at "bool";
	addAttr -ci true -sn "SetJointParent" -ln "SetJointParent" -dt "string";
	addAttr -ci true -sn "Help" -ln "Help" -dt "string";
	addAttr -ci true -sn "postcode" -ln "postcode" -dt "string";
	setAttr ".precode" -type "string" "";
	setAttr -l on ".Build_Command" -type "string" "exec_single_fk.build_single_fk_block()";
	setAttr -l on ".Import_Command" -type "string" "import exec_single_fk";
	setAttr ".SetCtrlParent" -type "string" "Rig_Ctrl_Grp";
	setAttr -cb on ".CtrlType" 16;
	setAttr -k on ".CtrlSize";
	setAttr -cb on ".CtrlColor" 6;
	setAttr -cb on ".Gimbal" yes;
	setAttr -cb on ".CreateJoint" yes;
	setAttr ".SetJointParent" -type "string" "Miscellaneous_Grp";
	setAttr ".Help" -type "string" "Possible parent: Bone_Jnt\n";
	setAttr ".postcode" -type "string" "";
createNode hyperLayout -n "hyperLayout17";
	rename -uid "FDA8DF56-AA4B-976A-F50C-6FBE689B647D";
	setAttr ".ihi" 0;
	setAttr -s 10 ".hyp";
createNode network -n "L_Clavicle_Config";
	rename -uid "6293AD3E-834D-9660-CD2F-7A8097D10C68";
	addAttr -ci true -sn "precode" -ln "precode" -dt "string";
	addAttr -ci true -sn "Build_Command" -ln "Build_Command" -dt "string";
	addAttr -ci true -sn "Import_Command" -ln "Import_Command" -dt "string";
	addAttr -ci true -sn "SetParent" -ln "SetParent" -dt "string";
	addAttr -ci true -sn "Mirror" -ln "Mirror" -min 0 -max 2 -en "True:False:Right_Only" 
		-at "enum";
	addAttr -ci true -sn "CtrlType" -ln "CtrlType" -min 0 -max 16 -en "square:sphere:cube:octagon:hexagon:pringle:feet:hand:circleY:circleX:circleZ:3dArrow:2dArrow:mover:2dArrow:root:cog" 
		-at "enum";
	addAttr -ci true -sn "CtrlSize" -ln "CtrlSize" -dv 4 -min 1 -max 20 -at "long";
	addAttr -ci true -sn "SetGameParent" -ln "SetGameParent" -dt "string";
	addAttr -ci true -sn "Help" -ln "Help" -dt "string";
	addAttr -ci true -sn "postcode" -ln "postcode" -dt "string";
	setAttr ".precode" -type "string" "";
	setAttr -l on ".Build_Command" -type "string" "exec_clavicle.build_clavicle_block()";
	setAttr -l on ".Import_Command" -type "string" "import exec_clavicle";
	setAttr ".SetParent" -type "string" "COG_Gimbal_Ctrl";
	setAttr -cb on ".Mirror";
	setAttr -cb on ".CtrlType";
	setAttr -k on ".CtrlSize";
	setAttr ".SetGameParent" -type "string" "";
	setAttr ".Help" -type "string" "Possible parent: R_Clavicle_Jnt\n";
	setAttr ".postcode" -type "string" "";
createNode hyperLayout -n "hyperLayout18";
	rename -uid "5211AA99-8C40-8243-F6E6-5D90A3B77FF7";
	setAttr ".ihi" 0;
	setAttr -s 15 ".hyp";
createNode network -n "L_FrHip_Config";
	rename -uid "5D8DC101-DB4E-7C64-F9BD-0D9586E76673";
	addAttr -ci true -sn "precode" -ln "precode" -dt "string";
	addAttr -ci true -sn "Build_Command" -ln "Build_Command" -dt "string";
	addAttr -ci true -sn "Import_Command" -ln "Import_Command" -dt "string";
	addAttr -ci true -sn "SetParent" -ln "SetParent" -dt "string";
	addAttr -ci true -sn "Mirror" -ln "Mirror" -min 0 -max 2 -en "True:False:Right_Only" 
		-at "enum";
	addAttr -ci true -sn "CtrlSize" -ln "CtrlSize" -dv 4 -min 1 -max 20 -at "long";
	addAttr -ci true -sn "TwistAmount" -ln "TwistAmount" -dv 4 -min 1 -max 20 -at "long";
	addAttr -ci true -sn "IkCtrlType" -ln "IkCtrlType" -min 0 -max 1 -en "cube:sphere" 
		-at "enum";
	addAttr -ci true -sn "PVCtrlType" -ln "PVCtrlType" -min 0 -max 1 -en "sphere:cube" 
		-at "enum";
	addAttr -ci true -sn "IkTopCtrlType" -ln "IkTopCtrlType" -min 0 -max 5 -en "pin_cube:cube:sphere:circleY:circleX:circleY" 
		-at "enum";
	addAttr -ci true -sn "FKCtrlType" -ln "FKCtrlType" -min 0 -max 4 -en "bounding_cube:circleY:circleX:circleY:pin_cube" 
		-at "enum";
	addAttr -ci true -sn "SetGameParent" -ln "SetGameParent" -dt "string";
	addAttr -ci true -sn "Help" -ln "Help" -dt "string";
	addAttr -ci true -sn "postcode" -ln "postcode" -dt "string";
	setAttr ".precode" -type "string" "";
	setAttr -l on ".Build_Command" -type "string" "exec_limb.build_limb_block()";
	setAttr -l on ".Import_Command" -type "string" "import exec_limb";
	setAttr ".SetParent" -type "string" "L_Clavicle_Jnt";
	setAttr -cb on ".Mirror";
	setAttr -k on ".CtrlSize";
	setAttr -k on ".TwistAmount";
	setAttr -cb on ".IkCtrlType";
	setAttr -cb on ".PVCtrlType";
	setAttr -cb on ".IkTopCtrlType";
	setAttr -cb on ".FKCtrlType";
	setAttr ".SetGameParent" -type "string" "L_Clavicle_Bnd";
	setAttr ".Help" -type "string" "Possible parent: L_Wrist_Jnt\n";
	setAttr ".postcode" -type "string" "";
createNode hyperLayout -n "hyperLayout19";
	rename -uid "9CE29D78-AC48-7329-FA11-CDBC74A9653B";
	setAttr ".ihi" 0;
	setAttr -s 10 ".hyp";
createNode network -n "L_Pelvis_Config";
	rename -uid "CEEFFB8F-AD48-FF78-3D8A-0AA048114B48";
	addAttr -ci true -sn "precode" -ln "precode" -dt "string";
	addAttr -ci true -sn "Build_Command" -ln "Build_Command" -dt "string";
	addAttr -ci true -sn "Import_Command" -ln "Import_Command" -dt "string";
	addAttr -ci true -sn "SetParent" -ln "SetParent" -dt "string";
	addAttr -ci true -sn "Mirror" -ln "Mirror" -min 0 -max 2 -en "True:False:Right_Only" 
		-at "enum";
	addAttr -ci true -sn "CtrlType" -ln "CtrlType" -min 0 -max 16 -en "hexagon:sphere:cube:square:octagon:pringle:feet:hand:circleY:circleX:circleZ:3dArrow:2dArrow:mover:2dArrow:root:cog" 
		-at "enum";
	addAttr -ci true -sn "CtrlSize" -ln "CtrlSize" -dv 4 -min 1 -max 20 -at "long";
	addAttr -ci true -sn "SetGameParent" -ln "SetGameParent" -dt "string";
	addAttr -ci true -sn "Help" -ln "Help" -dt "string";
	addAttr -ci true -sn "postcode" -ln "postcode" -dt "string";
	setAttr ".precode" -type "string" "";
	setAttr -l on ".Build_Command" -type "string" "exec_pelvis.build_pelvis_block()";
	setAttr -l on ".Import_Command" -type "string" "import exec_pelvis";
	setAttr ".SetParent" -type "string" "COG_Gimbal_Ctrl";
	setAttr -cb on ".Mirror";
	setAttr -cb on ".CtrlType";
	setAttr -k on ".CtrlSize";
	setAttr ".SetGameParent" -type "string" "";
	setAttr ".Help" -type "string" "Possible parent: L_Pelvis_Jnt\n";
	setAttr ".postcode" -type "string" "";
createNode hyperLayout -n "hyperLayout20";
	rename -uid "243327C9-5545-45A3-AFCC-63A73A2A1BF3";
	setAttr ".ihi" 0;
	setAttr -s 15 ".hyp";
createNode network -n "L_Hip_Config";
	rename -uid "5B46DF27-794F-C0A4-A486-B298C8EDF59C";
	addAttr -ci true -sn "precode" -ln "precode" -dt "string";
	addAttr -ci true -sn "Build_Command" -ln "Build_Command" -dt "string";
	addAttr -ci true -sn "Import_Command" -ln "Import_Command" -dt "string";
	addAttr -ci true -sn "SetParent" -ln "SetParent" -dt "string";
	addAttr -ci true -sn "Mirror" -ln "Mirror" -min 0 -max 2 -en "True:False:Right_Only" 
		-at "enum";
	addAttr -ci true -sn "CtrlSize" -ln "CtrlSize" -dv 4 -min 1 -max 20 -at "long";
	addAttr -ci true -sn "TwistAmount" -ln "TwistAmount" -dv 4 -min 1 -max 20 -at "long";
	addAttr -ci true -sn "IkCtrlType" -ln "IkCtrlType" -min 0 -max 1 -en "cube:sphere" 
		-at "enum";
	addAttr -ci true -sn "PVCtrlType" -ln "PVCtrlType" -min 0 -max 1 -en "sphere:cube" 
		-at "enum";
	addAttr -ci true -sn "IkTopCtrlType" -ln "IkTopCtrlType" -min 0 -max 5 -en "pin_cube:cube:sphere:circleY:circleX:circleY" 
		-at "enum";
	addAttr -ci true -sn "FKCtrlType" -ln "FKCtrlType" -min 0 -max 4 -en "bounding_cube:circleY:circleX:circleY:pin_cube" 
		-at "enum";
	addAttr -ci true -sn "SetGameParent" -ln "SetGameParent" -dt "string";
	addAttr -ci true -sn "Help" -ln "Help" -dt "string";
	addAttr -ci true -sn "postcode" -ln "postcode" -dt "string";
	setAttr ".precode" -type "string" "";
	setAttr -l on ".Build_Command" -type "string" "exec_limb.build_limb_block()";
	setAttr -l on ".Import_Command" -type "string" "import exec_limb";
	setAttr ".SetParent" -type "string" "L_Pelvis_Jnt";
	setAttr -cb on ".Mirror";
	setAttr -k on ".CtrlSize";
	setAttr -k on ".TwistAmount";
	setAttr -cb on ".IkCtrlType";
	setAttr -cb on ".PVCtrlType";
	setAttr -cb on ".IkTopCtrlType";
	setAttr -cb on ".FKCtrlType";
	setAttr ".SetGameParent" -type "string" "L_Pelvis_Bnd";
	setAttr ".Help" -type "string" "Possible parent: L_Wrist_Jnt\n";
	setAttr ".postcode" -type "string" "";
createNode hyperLayout -n "NewGuide_hyperLayout23";
	rename -uid "2358EFE9-EB48-7AC1-64C1-038A088F5A85";
	setAttr ".ihi" 0;
	setAttr -s 40 ".hyp";
createNode network -n "L_Foot_Config";
	rename -uid "87D32C66-0743-54F4-2F53-88A339FA06E2";
	addAttr -ci true -sn "precode" -ln "precode" -dt "string";
	addAttr -ci true -sn "Build_Command" -ln "Build_Command" -dt "string";
	addAttr -ci true -sn "Import_Command" -ln "Import_Command" -dt "string";
	addAttr -ci true -sn "SetIKCtrl" -ln "SetIKCtrl" -dt "string";
	addAttr -ci true -sn "SetFKCtrl" -ln "SetFKCtrl" -dt "string";
	addAttr -ci true -sn "Mirror" -ln "Mirror" -min 0 -max 2 -en "True:False:Right_Only" 
		-at "enum";
	addAttr -ci true -sn "SwitchIKFKAttr" -ln "SwitchIKFKAttr" -dt "string";
	addAttr -ci true -sn "IkAttrsPosition" -ln "IkAttrsPosition" -dt "string";
	addAttr -ci true -sn "IKLeg" -ln "IKLeg" -dt "string";
	addAttr -ci true -sn "CtrlSize" -ln "CtrlSize" -dv 1 -min 1 -max 20 -at "long";
	addAttr -ci true -sn "SetGameParent" -ln "SetGameParent" -dt "string";
	addAttr -ci true -sn "Help" -ln "Help" -dt "string";
	addAttr -ci true -sn "postcode" -ln "postcode" -dt "string";
	setAttr ".precode" -type "string" "";
	setAttr -l on ".Build_Command" -type "string" "exec_foot.build_foot_block()";
	setAttr -l on ".Import_Command" -type "string" "import exec_foot";
	setAttr ".SetIKCtrl" -type "string" "L_Ankle_SubIk_Ctrl";
	setAttr ".SetFKCtrl" -type "string" "L_Ankle_Fk_Ctrl";
	setAttr -cb on ".Mirror";
	setAttr ".SwitchIKFKAttr" -type "string" "L_Hip_Jnt_Switch_Loc.Switch_IK_FK";
	setAttr ".IkAttrsPosition" -type "string" "L_Ankle_Ik_Ctrl";
	setAttr ".IKLeg" -type "string" "L_Ankle_Ik_IKrp";
	setAttr -k on ".CtrlSize" 2;
	setAttr ".SetGameParent" -type "string" "L_Knee_Twist_3_Bnd";
	setAttr ".Help" -type "string" "Possible parent: L_Foot_BallToes_Jnt\n";
	setAttr ".postcode" -type "string" "";
createNode hyperLayout -n "hyperLayout67";
	rename -uid "F356DF76-8E46-75ED-6300-37B61E280AE2";
	setAttr ".ihi" 0;
createNode network -n "Smart_RFL_Config";
	rename -uid "B046AFC4-7745-3055-E272-3F807E985BD2";
	addAttr -ci true -sn "precode" -ln "precode" -dt "string";
	addAttr -ci true -sn "Build_Command" -ln "Build_Command" -dt "string";
	addAttr -ci true -sn "Import_Command" -ln "Import_Command" -dt "string";
	addAttr -ci true -sn "SetRFLAttrsPosition" -ln "SetRFLAttrsPosition" -dt "string";
	addAttr -ci true -sn "AltMode" -ln "AltMode" -min 0 -max 1 -at "bool";
	addAttr -ci true -sn "SetFootBlockName" -ln "SetFootBlockName" -dt "string";
	addAttr -ci true -sn "Help" -ln "Help" -dt "string";
	addAttr -ci true -sn "postcode" -ln "postcode" -dt "string";
	setAttr ".precode" -type "string" "";
	setAttr -l on ".Build_Command" -type "string" "exec_smart_rfl.build_smart_rfl_block()";
	setAttr -l on ".Import_Command" -type "string" "import exec_smart_rfl";
	setAttr ".SetRFLAttrsPosition" -type "string" "L_Ankle_Ik_Ctrl";
	setAttr -cb on ".AltMode" yes;
	setAttr ".SetFootBlockName" -type "string" "L_Foot";
	setAttr ".Help" -type "string" "Will create a fancy RFL system for current Feet, Just put the name of the Feet name and the Attrs position ";
	setAttr ".postcode" -type "string" "";
createNode hyperLayout -n "hyperLayout66";
	rename -uid "A9A78873-6045-D7BA-1458-02A67C6BA1ED";
	setAttr ".ihi" 0;
createNode network -n "L_Smart_RFL_Config";
	rename -uid "55C742B6-B049-103A-E51F-CC97730D993E";
	addAttr -ci true -sn "precode" -ln "precode" -dt "string";
	addAttr -ci true -sn "Build_Command" -ln "Build_Command" -dt "string";
	addAttr -ci true -sn "Import_Command" -ln "Import_Command" -dt "string";
	addAttr -ci true -sn "SetToes" -ln "SetToes" -dt "string";
	addAttr -ci true -sn "SetBallFloor" -ln "SetBallFloor" -dt "string";
	addAttr -ci true -sn "SetHeel" -ln "SetHeel" -dt "string";
	addAttr -ci true -sn "SetIn" -ln "SetIn" -dt "string";
	addAttr -ci true -sn "SetOut" -ln "SetOut" -dt "string";
	addAttr -ci true -sn "SetBallParent" -ln "SetBallParent" -dt "string";
	addAttr -ci true -sn "SetHeelParent" -ln "SetHeelParent" -dt "string";
	addAttr -ci true -sn "Mirror" -ln "Mirror" -min 0 -max 1 -at "bool";
	addAttr -ci true -sn "Color" -ln "Color" -min 0 -max 10 -en "pink:orange:blue:light_blue:red:green:purple:yellow:cyan:gray:brown" 
		-at "enum";
	addAttr -ci true -sn "SetAttrsPosition" -ln "SetAttrsPosition" -dt "string";
	addAttr -ci true -sn "ForceYZero" -ln "ForceYZero" -min 0 -max 1 -at "bool";
	addAttr -ci true -sn "Help" -ln "Help" -dt "string";
	addAttr -ci true -sn "postcode" -ln "postcode" -dt "string";
	setAttr ".precode" -type "string" "";
	setAttr -l on ".Build_Command" -type "string" "exec_footbox.build_footbox_block()";
	setAttr -l on ".Import_Command" -type "string" "import exec_footbox";
	setAttr ".SetToes" -type "string" "L_Foot_Toes_RFL_Grp";
	setAttr ".SetBallFloor" -type "string" "L_Foot_BallFloor_RFL_Grp";
	setAttr ".SetHeel" -type "string" "L_Foot_Heel_RFL_Grp";
	setAttr ".SetIn" -type "string" "L_Foot_In_RFL_Grp";
	setAttr ".SetOut" -type "string" "L_Foot_Out_RFL_Grp";
	setAttr ".SetBallParent" -type "string" "L_Foot_Toes_Ctrl";
	setAttr ".SetHeelParent" -type "string" "L_Foot_Ankle_Bnd";
	setAttr -cb on ".Mirror" yes;
	setAttr -cb on ".Color";
	setAttr ".SetAttrsPosition" -type "string" "L_Hip_Jnt_Switch_Loc";
	setAttr -cb on ".ForceYZero" yes;
	setAttr ".Help" -type "string" "Create foot boxes for the foot block";
	setAttr ".postcode" -type "string" "";
createNode hyperLayout -n "NewGuide_hyperLayout24";
	rename -uid "1C4F3F75-BD4A-59D3-F241-149C3F6C9A42";
	setAttr ".ihi" 0;
	setAttr -s 40 ".hyp";
createNode network -n "L_FrFoot_Config";
	rename -uid "B8949457-3A4A-E693-A105-80A38B8D51F4";
	addAttr -ci true -sn "precode" -ln "precode" -dt "string";
	addAttr -ci true -sn "Build_Command" -ln "Build_Command" -dt "string";
	addAttr -ci true -sn "Import_Command" -ln "Import_Command" -dt "string";
	addAttr -ci true -sn "SetIKCtrl" -ln "SetIKCtrl" -dt "string";
	addAttr -ci true -sn "SetFKCtrl" -ln "SetFKCtrl" -dt "string";
	addAttr -ci true -sn "Mirror" -ln "Mirror" -min 0 -max 2 -en "True:False:Right_Only" 
		-at "enum";
	addAttr -ci true -sn "SwitchIKFKAttr" -ln "SwitchIKFKAttr" -dt "string";
	addAttr -ci true -sn "IkAttrsPosition" -ln "IkAttrsPosition" -dt "string";
	addAttr -ci true -sn "IKLeg" -ln "IKLeg" -dt "string";
	addAttr -ci true -sn "CtrlSize" -ln "CtrlSize" -dv 1 -min 1 -max 20 -at "long";
	addAttr -ci true -sn "SetGameParent" -ln "SetGameParent" -dt "string";
	addAttr -ci true -sn "Help" -ln "Help" -dt "string";
	addAttr -ci true -sn "postcode" -ln "postcode" -dt "string";
	setAttr ".precode" -type "string" "";
	setAttr -l on ".Build_Command" -type "string" "exec_foot.build_foot_block()";
	setAttr -l on ".Import_Command" -type "string" "import exec_foot";
	setAttr ".SetIKCtrl" -type "string" "L_FrAnkle_SubIk_Ctrl";
	setAttr ".SetFKCtrl" -type "string" "L_FrAnkle_Fk_Ctrl";
	setAttr -cb on ".Mirror";
	setAttr ".SwitchIKFKAttr" -type "string" "L_FrHip_Jnt_Switch_Loc.Switch_IK_FK";
	setAttr ".IkAttrsPosition" -type "string" "L_FrAnkle_Ik_Ctrl";
	setAttr ".IKLeg" -type "string" "L_FrAnkle_Ik_IKrp";
	setAttr -k on ".CtrlSize" 2;
	setAttr ".SetGameParent" -type "string" "L_FrKnee_Twist_3_Bnd";
	setAttr ".Help" -type "string" "Possible parent: L_Foot_BallToes_Jnt\n";
	setAttr ".postcode" -type "string" "";
createNode hyperLayout -n "hyperLayout65";
	rename -uid "9DFC61D3-0D43-FDDC-EBF2-E39DA43C29E5";
	setAttr ".ihi" 0;
createNode network -n "L_FrFootBox_Config";
	rename -uid "97593402-234A-5658-50D7-9A8B803B9A37";
	addAttr -ci true -sn "precode" -ln "precode" -dt "string";
	addAttr -ci true -sn "Build_Command" -ln "Build_Command" -dt "string";
	addAttr -ci true -sn "Import_Command" -ln "Import_Command" -dt "string";
	addAttr -ci true -sn "SetToes" -ln "SetToes" -dt "string";
	addAttr -ci true -sn "SetBallFloor" -ln "SetBallFloor" -dt "string";
	addAttr -ci true -sn "SetHeel" -ln "SetHeel" -dt "string";
	addAttr -ci true -sn "SetIn" -ln "SetIn" -dt "string";
	addAttr -ci true -sn "SetOut" -ln "SetOut" -dt "string";
	addAttr -ci true -sn "SetBallParent" -ln "SetBallParent" -dt "string";
	addAttr -ci true -sn "SetHeelParent" -ln "SetHeelParent" -dt "string";
	addAttr -ci true -sn "Mirror" -ln "Mirror" -min 0 -max 1 -at "bool";
	addAttr -ci true -sn "Color" -ln "Color" -min 0 -max 10 -en "pink:orange:blue:light_blue:red:green:purple:yellow:cyan:gray:brown" 
		-at "enum";
	addAttr -ci true -sn "SetAttrsPosition" -ln "SetAttrsPosition" -dt "string";
	addAttr -ci true -sn "ForceYZero" -ln "ForceYZero" -min 0 -max 1 -at "bool";
	addAttr -ci true -sn "Help" -ln "Help" -dt "string";
	addAttr -ci true -sn "postcode" -ln "postcode" -dt "string";
	setAttr ".precode" -type "string" "";
	setAttr -l on ".Build_Command" -type "string" "exec_footbox.build_footbox_block()";
	setAttr -l on ".Import_Command" -type "string" "import exec_footbox";
	setAttr ".SetToes" -type "string" "L_FrFoot_Toes_RFL_Grp";
	setAttr ".SetBallFloor" -type "string" "L_FrFoot_BallFloor_RFL_Grp";
	setAttr ".SetHeel" -type "string" "L_FrFoot_Heel_RFL_Grp";
	setAttr ".SetIn" -type "string" "L_FrFoot_In_RFL_Grp";
	setAttr ".SetOut" -type "string" "L_FrFoot_Out_RFL_Grp";
	setAttr ".SetBallParent" -type "string" "L_FrFoot_Toes_Ctrl";
	setAttr ".SetHeelParent" -type "string" "L_FrFoot_Ankle_Bnd";
	setAttr -cb on ".Mirror" yes;
	setAttr -cb on ".Color";
	setAttr ".SetAttrsPosition" -type "string" "L_FrHip_Jnt_Switch_Loc";
	setAttr -cb on ".ForceYZero" yes;
	setAttr ".Help" -type "string" "Create foot boxes for the foot block";
	setAttr ".postcode" -type "string" "";
createNode hyperLayout -n "hyperLayout63";
	rename -uid "5B69AE0C-1041-EE39-5306-5596D5482F65";
	setAttr ".ihi" 0;
createNode network -n "FrSmart_RFL_Config";
	rename -uid "743D6DF4-734C-5F6F-93BE-D7B3008FCC38";
	addAttr -ci true -sn "precode" -ln "precode" -dt "string";
	addAttr -ci true -sn "Build_Command" -ln "Build_Command" -dt "string";
	addAttr -ci true -sn "Import_Command" -ln "Import_Command" -dt "string";
	addAttr -ci true -sn "SetRFLAttrsPosition" -ln "SetRFLAttrsPosition" -dt "string";
	addAttr -ci true -sn "AltMode" -ln "AltMode" -min 0 -max 1 -at "bool";
	addAttr -ci true -sn "SetFootBlockName" -ln "SetFootBlockName" -dt "string";
	addAttr -ci true -sn "Help" -ln "Help" -dt "string";
	addAttr -ci true -sn "postcode" -ln "postcode" -dt "string";
	setAttr ".precode" -type "string" "";
	setAttr -l on ".Build_Command" -type "string" "exec_smart_rfl.build_smart_rfl_block()";
	setAttr -l on ".Import_Command" -type "string" "import exec_smart_rfl";
	setAttr ".SetRFLAttrsPosition" -type "string" "L_FrAnkle_Ik_Ctrl";
	setAttr -cb on ".AltMode" yes;
	setAttr ".SetFootBlockName" -type "string" "L_FrFoot";
	setAttr ".Help" -type "string" "Will create a fancy RFL system for current Feet, Just put the name of the Feet name and the Attrs position ";
	setAttr ".postcode" -type "string" "";
createNode hyperLayout -n "hyperLayout68";
	rename -uid "123E71E0-F547-F4CC-5736-77A265084FCA";
	setAttr ".ihi" 0;
	setAttr -s 2 ".hyp";
createNode network -n "Neck_Config";
	rename -uid "87504144-2B47-E58A-3489-EFB375C0ABC7";
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
	setAttr ".SetParent" -type "string" "COG_Gimbal_Ctrl";
	setAttr -cb on ".Equal" yes;
	setAttr -k on ".Ctrls";
	setAttr -k on ".Joints";
	setAttr -cb on ".Constraint" yes;
	setAttr -cb on ".AddFk" yes;
	setAttr -cb on ".Wire";
	setAttr -cb on ".MiddleCtrlPosition";
	setAttr ".Help" -type "string" "Remove constraint for a local system.";
	setAttr ".postcode" -type "string" "";
createNode hyperLayout -n "hyperLayout69";
	rename -uid "0EA8829D-2345-1CBF-273A-4098B2229642";
	setAttr ".ihi" 0;
	setAttr -s 2 ".hyp";
createNode network -n "Head_Config";
	rename -uid "39CDD5BF-9E43-4BF5-019B-68A2CA2D9A46";
	addAttr -ci true -sn "precode" -ln "precode" -dt "string";
	addAttr -ci true -sn "Build_Command" -ln "Build_Command" -dt "string";
	addAttr -ci true -sn "Import_Command" -ln "Import_Command" -dt "string";
	addAttr -ci true -sn "SetCtrlParent" -ln "SetCtrlParent" -dt "string";
	addAttr -ci true -sn "CtrlType" -ln "CtrlType" -min 0 -max 16 -en "sphere:cube:square:octagon:hexagon:pringle:feet:hand:circleX:circleY:circleZ:3dArrow:2dArrow:mover:2dArrow:root:cog" 
		-at "enum";
	addAttr -ci true -sn "CtrlSize" -ln "CtrlSize" -dv 4 -min 1 -max 20 -at "long";
	addAttr -ci true -sn "CtrlColor" -ln "CtrlColor" -min 0 -max 7 -en "lightBlue:blue:white:purple:green:red:yellow:grey" 
		-at "enum";
	addAttr -ci true -sn "Gimbal" -ln "Gimbal" -min 0 -max 1 -at "bool";
	addAttr -ci true -sn "CreateJoint" -ln "CreateJoint" -min 0 -max 1 -at "bool";
	addAttr -ci true -sn "SetJointParent" -ln "SetJointParent" -dt "string";
	addAttr -ci true -sn "Help" -ln "Help" -dt "string";
	addAttr -ci true -sn "postcode" -ln "postcode" -dt "string";
	setAttr ".precode" -type "string" "";
	setAttr -l on ".Build_Command" -type "string" "exec_single_fk.build_single_fk_block()";
	setAttr -l on ".Import_Command" -type "string" "import exec_single_fk";
	setAttr ".SetCtrlParent" -type "string" "Neck_1_04_Ctrl";
	setAttr -cb on ".CtrlType";
	setAttr -k on ".CtrlSize";
	setAttr -cb on ".CtrlColor";
	setAttr -cb on ".Gimbal" yes;
	setAttr -cb on ".CreateJoint" yes;
	setAttr ".SetJointParent" -type "string" "Miscellaneous_Grp";
	setAttr ".Help" -type "string" "Possible parent: Bone_Jnt\n";
	setAttr ".postcode" -type "string" "";
createNode hyperLayout -n "hyperLayout36";
	rename -uid "3E243C85-304B-3194-BDB8-3982F850DCDC";
	setAttr ".ihi" 0;
	setAttr -s 10 ".hyp";
createNode network -n "L_Eyes_Config";
	rename -uid "83C5218F-5842-17EA-0715-8A8C9B29E53E";
	addAttr -ci true -sn "precode" -ln "precode" -dt "string";
	addAttr -ci true -sn "Build_Command" -ln "Build_Command" -dt "string";
	addAttr -ci true -sn "Import_Command" -ln "Import_Command" -dt "string";
	addAttr -ci true -sn "SetParent" -ln "SetParent" -dt "string";
	addAttr -ci true -sn "EyesAmount" -ln "EyesAmount" -min 0 -max 1 -en "Two:One" -at "enum";
	addAttr -ci true -sn "Help" -ln "Help" -dt "string";
	addAttr -ci true -sn "CtrlSize" -ln "CtrlSize" -dv 4 -min 1 -max 20 -at "long";
	addAttr -ci true -sn "postcode" -ln "postcode" -dt "string";
	setAttr ".precode" -type "string" "";
	setAttr -l on ".Build_Command" -type "string" "exec_eyes.build_eyes_block()";
	setAttr -l on ".Import_Command" -type "string" "import exec_eyes";
	setAttr ".SetParent" -type "string" "Head_Ctrl";
	setAttr -cb on ".EyesAmount";
	setAttr ".Help" -type "string" "Possible parent: Create Eye aim system";
	setAttr -k on ".CtrlSize";
	setAttr ".postcode" -type "string" "";
createNode hyperLayout -n "hyperLayout71";
	rename -uid "B123AB32-274A-8093-D77F-8A98CA4E35B9";
	setAttr ".ihi" 0;
	setAttr -s 2 ".hyp";
createNode network -n "Tail_Config";
	rename -uid "757EA9C7-C342-04D5-A5F8-46A0D6A520C4";
	addAttr -ci true -sn "precode" -ln "precode" -dt "string";
	addAttr -ci true -sn "Build_Command" -ln "Build_Command" -dt "string";
	addAttr -ci true -sn "Import_Command" -ln "Import_Command" -dt "string";
	addAttr -ci true -sn "SetParent" -ln "SetParent" -dt "string";
	addAttr -ci true -sn "FkCtrls" -ln "FkCtrls" -dv 5 -min 1 -max 20 -at "long";
	addAttr -ci true -sn "Joints" -ln "Joints" -dv 10 -min 1 -max 20 -at "long";
	addAttr -ci true -sn "Help" -ln "Help" -dt "string";
	addAttr -ci true -sn "postcode" -ln "postcode" -dt "string";
	setAttr ".precode" -type "string" "";
	setAttr -l on ".Build_Command" -type "string" "exec_tail.build_tail_block()";
	setAttr -l on ".Import_Command" -type "string" "import exec_tail";
	setAttr ".SetParent" -type "string" "COG_Gimbal_Ctrl";
	setAttr -k on ".FkCtrls" 3;
	setAttr -k on ".Joints" 3;
	setAttr ".Help" -type "string" "Create IK/FK Tail System";
	setAttr ".postcode" -type "string" "";
createNode hyperLayout -n "hyperLayout51";
	rename -uid "93069B14-AF43-CFC2-D352-A6B283ACD791";
	setAttr ".ihi" 0;
createNode network -n "Eyes_Switches_Config";
	rename -uid "510AD41D-E543-2A61-75B4-A98E4783BEBF";
	addAttr -ci true -sn "precode" -ln "precode" -dt "string";
	addAttr -ci true -sn "Build_Command" -ln "Build_Command" -dt "string";
	addAttr -ci true -sn "Import_Command" -ln "Import_Command" -dt "string";
	addAttr -ci true -sn "Rotate" -ln "Rotate" -min 0 -max 1 -at "bool";
	addAttr -ci true -sn "Help" -ln "Help" -dt "string";
	addAttr -ci true -sn "Translate" -ln "Translate" -min 0 -max 1 -at "bool";
	addAttr -ci true -sn "SetTargetCtrl" -ln "SetTargetCtrl" -dt "string";
	addAttr -ci true -sn "Spaces" -ln "Spaces" -dt "string";
	addAttr -ci true -sn "Mirror" -ln "Mirror" -min 0 -max 1 -at "bool";
	addAttr -ci true -sn "CreateProxyOnTargetCtrl" -ln "CreateProxyOnTargetCtrl" -min 
		0 -max 1 -at "bool";
	addAttr -ci true -sn "SetAttrsHolder" -ln "SetAttrsHolder" -dt "string";
	addAttr -ci true -sn "postcode" -ln "postcode" -dt "string";
	addAttr -ci true -sn "Animbot" -ln "Animbot" -min 0 -max 1 -at "bool";
	setAttr ".precode" -type "string" "";
	setAttr -l on ".Build_Command" -type "string" "exec_spaceSwitches.build_spaceSwitches_block()";
	setAttr -l on ".Import_Command" -type "string" "import exec_spaceSwitches ";
	setAttr -cb on ".Rotate" yes;
	setAttr ".Help" -type "string" "Separate the space switches with a ','";
	setAttr -cb on ".Translate" yes;
	setAttr ".SetTargetCtrl" -type "string" "Eyes_Main_Ctrl";
	setAttr ".Spaces" -type "string" "Head_Jnt, Mover_Gimbal_Ctrl, COG_Ctrl,  Mutant_Tools_Grp";
	setAttr -cb on ".Mirror";
	setAttr -cb on ".CreateProxyOnTargetCtrl" yes;
	setAttr ".SetAttrsHolder" -type "string" "Eyes_Attrs_Loc";
	setAttr ".postcode" -type "string" "";
	setAttr -k on ".Animbot" yes;
createNode hyperLayout -n "hyperLayout54";
	rename -uid "ECF6BE84-0B42-090E-1432-B3A9E8FE8F26";
	setAttr ".ihi" 0;
createNode network -n "L_IK_FrLeg_Switches_Config";
	rename -uid "1E9264BE-7046-2565-F1AD-5FAE297DBA84";
	addAttr -ci true -sn "precode" -ln "precode" -dt "string";
	addAttr -ci true -sn "Build_Command" -ln "Build_Command" -dt "string";
	addAttr -ci true -sn "Import_Command" -ln "Import_Command" -dt "string";
	addAttr -ci true -sn "Rotate" -ln "Rotate" -min 0 -max 1 -at "bool";
	addAttr -ci true -sn "Help" -ln "Help" -dt "string";
	addAttr -ci true -sn "Translate" -ln "Translate" -min 0 -max 1 -at "bool";
	addAttr -ci true -sn "SetTargetCtrl" -ln "SetTargetCtrl" -dt "string";
	addAttr -ci true -sn "Spaces" -ln "Spaces" -dt "string";
	addAttr -ci true -sn "Mirror" -ln "Mirror" -min 0 -max 1 -at "bool";
	addAttr -ci true -sn "CreateProxyOnTargetCtrl" -ln "CreateProxyOnTargetCtrl" -min 
		0 -max 1 -at "bool";
	addAttr -ci true -sn "SetAttrsHolder" -ln "SetAttrsHolder" -dt "string";
	addAttr -ci true -sn "postcode" -ln "postcode" -dt "string";
	addAttr -ci true -sn "Animbot" -ln "Animbot" -min 0 -max 1 -at "bool";
	setAttr ".precode" -type "string" "";
	setAttr -l on ".Build_Command" -type "string" "exec_spaceSwitches.build_spaceSwitches_block()";
	setAttr -l on ".Import_Command" -type "string" "import exec_spaceSwitches ";
	setAttr -cb on ".Rotate" yes;
	setAttr ".Help" -type "string" "Separate the space switches with a ','";
	setAttr -cb on ".Translate" yes;
	setAttr ".SetTargetCtrl" -type "string" "L_FrAnkle_Ik_Ctrl";
	setAttr ".Spaces" -type "string" "Mover_Gimbal_Ctrl, COG_Ctrl, L_Clavicle_Jnt, Mutant_Tools_Grp";
	setAttr -cb on ".Mirror" yes;
	setAttr -cb on ".CreateProxyOnTargetCtrl" yes;
	setAttr ".SetAttrsHolder" -type "string" "L_FrHip_Jnt_Switch_Loc";
	setAttr ".postcode" -type "string" "";
	setAttr -k on ".Animbot" yes;
createNode hyperLayout -n "hyperLayout55";
	rename -uid "F9A40D7D-C049-51FC-DF91-5DA2253D6F2D";
	setAttr ".ihi" 0;
createNode network -n "L_FK_FrLeg_Switches_Config";
	rename -uid "A04B542B-B649-D67A-D40B-198BA60180E3";
	addAttr -ci true -sn "precode" -ln "precode" -dt "string";
	addAttr -ci true -sn "Build_Command" -ln "Build_Command" -dt "string";
	addAttr -ci true -sn "Import_Command" -ln "Import_Command" -dt "string";
	addAttr -ci true -sn "Rotate" -ln "Rotate" -min 0 -max 1 -at "bool";
	addAttr -ci true -sn "Help" -ln "Help" -dt "string";
	addAttr -ci true -sn "Translate" -ln "Translate" -min 0 -max 1 -at "bool";
	addAttr -ci true -sn "SetTargetCtrl" -ln "SetTargetCtrl" -dt "string";
	addAttr -ci true -sn "Spaces" -ln "Spaces" -dt "string";
	addAttr -ci true -sn "Mirror" -ln "Mirror" -min 0 -max 1 -at "bool";
	addAttr -ci true -sn "CreateProxyOnTargetCtrl" -ln "CreateProxyOnTargetCtrl" -min 
		0 -max 1 -at "bool";
	addAttr -ci true -sn "SetAttrsHolder" -ln "SetAttrsHolder" -dt "string";
	addAttr -ci true -sn "postcode" -ln "postcode" -dt "string";
	addAttr -ci true -sn "Animbot" -ln "Animbot" -min 0 -max 1 -at "bool";
	setAttr ".precode" -type "string" "";
	setAttr -l on ".Build_Command" -type "string" "exec_spaceSwitches.build_spaceSwitches_block()";
	setAttr -l on ".Import_Command" -type "string" "import exec_spaceSwitches ";
	setAttr -cb on ".Rotate" yes;
	setAttr ".Help" -type "string" "Separate the space switches with a ','";
	setAttr -cb on ".Translate";
	setAttr ".SetTargetCtrl" -type "string" "L_FrHip_Fk_Ctrl";
	setAttr ".Spaces" -type "string" "Mover_Gimbal_Ctrl, COG_Ctrl, L_Clavicle_Jnt, Mutant_Tools_Grp";
	setAttr -cb on ".Mirror" yes;
	setAttr -cb on ".CreateProxyOnTargetCtrl" yes;
	setAttr ".SetAttrsHolder" -type "string" "L_FrHip_Jnt_Switch_Loc";
	setAttr ".postcode" -type "string" "";
	setAttr -k on ".Animbot" yes;
createNode hyperLayout -n "hyperLayout56";
	rename -uid "20C0561F-AA44-C4D2-3FE2-CBB5FB70ABB7";
	setAttr ".ihi" 0;
createNode network -n "L_PV_FrLeg_Switches_Config";
	rename -uid "A8DBBD63-6849-CD6C-CBE9-16AC6D3AA8C1";
	addAttr -ci true -sn "precode" -ln "precode" -dt "string";
	addAttr -ci true -sn "Build_Command" -ln "Build_Command" -dt "string";
	addAttr -ci true -sn "Import_Command" -ln "Import_Command" -dt "string";
	addAttr -ci true -sn "Rotate" -ln "Rotate" -min 0 -max 1 -at "bool";
	addAttr -ci true -sn "Help" -ln "Help" -dt "string";
	addAttr -ci true -sn "Translate" -ln "Translate" -min 0 -max 1 -at "bool";
	addAttr -ci true -sn "SetTargetCtrl" -ln "SetTargetCtrl" -dt "string";
	addAttr -ci true -sn "Spaces" -ln "Spaces" -dt "string";
	addAttr -ci true -sn "Mirror" -ln "Mirror" -min 0 -max 1 -at "bool";
	addAttr -ci true -sn "CreateProxyOnTargetCtrl" -ln "CreateProxyOnTargetCtrl" -min 
		0 -max 1 -at "bool";
	addAttr -ci true -sn "SetAttrsHolder" -ln "SetAttrsHolder" -dt "string";
	addAttr -ci true -sn "postcode" -ln "postcode" -dt "string";
	addAttr -ci true -sn "Animbot" -ln "Animbot" -min 0 -max 1 -at "bool";
	setAttr ".precode" -type "string" "";
	setAttr -l on ".Build_Command" -type "string" "exec_spaceSwitches.build_spaceSwitches_block()";
	setAttr -l on ".Import_Command" -type "string" "import exec_spaceSwitches ";
	setAttr -cb on ".Rotate" yes;
	setAttr ".Help" -type "string" "Separate the space switches with a ','";
	setAttr -cb on ".Translate" yes;
	setAttr ".SetTargetCtrl" -type "string" "L_FrAnkle_Ik_PoleVector_Ctrl";
	setAttr ".Spaces" -type "string" "L_FrAnkle_Ik_Ctrl, Mover_Gimbal_Ctrl, Mutant_Tools_Grp,COG_Gimbal_Ctrl";
	setAttr -cb on ".Mirror" yes;
	setAttr -cb on ".CreateProxyOnTargetCtrl" yes;
	setAttr ".SetAttrsHolder" -type "string" "L_FrHip_Jnt_Switch_Loc";
	setAttr ".postcode" -type "string" "";
	setAttr -k on ".Animbot" yes;
createNode hyperLayout -n "hyperLayout57";
	rename -uid "74A91FF2-AD47-82ED-9245-DAA838453ECF";
	setAttr ".ihi" 0;
createNode network -n "L_IK_Hip_Switches_Config";
	rename -uid "4AE1A2D3-3A48-4985-569C-B3A48A2BD04D";
	addAttr -ci true -sn "precode" -ln "precode" -dt "string";
	addAttr -ci true -sn "Build_Command" -ln "Build_Command" -dt "string";
	addAttr -ci true -sn "Import_Command" -ln "Import_Command" -dt "string";
	addAttr -ci true -sn "Rotate" -ln "Rotate" -min 0 -max 1 -at "bool";
	addAttr -ci true -sn "Help" -ln "Help" -dt "string";
	addAttr -ci true -sn "Translate" -ln "Translate" -min 0 -max 1 -at "bool";
	addAttr -ci true -sn "SetTargetCtrl" -ln "SetTargetCtrl" -dt "string";
	addAttr -ci true -sn "Spaces" -ln "Spaces" -dt "string";
	addAttr -ci true -sn "Mirror" -ln "Mirror" -min 0 -max 1 -at "bool";
	addAttr -ci true -sn "CreateProxyOnTargetCtrl" -ln "CreateProxyOnTargetCtrl" -min 
		0 -max 1 -at "bool";
	addAttr -ci true -sn "SetAttrsHolder" -ln "SetAttrsHolder" -dt "string";
	addAttr -ci true -sn "postcode" -ln "postcode" -dt "string";
	addAttr -ci true -sn "Animbot" -ln "Animbot" -min 0 -max 1 -at "bool";
	setAttr ".precode" -type "string" "";
	setAttr -l on ".Build_Command" -type "string" "exec_spaceSwitches.build_spaceSwitches_block()";
	setAttr -l on ".Import_Command" -type "string" "import exec_spaceSwitches ";
	setAttr -cb on ".Rotate" yes;
	setAttr ".Help" -type "string" "Separate the space switches with a ','";
	setAttr -cb on ".Translate" yes;
	setAttr ".SetTargetCtrl" -type "string" "L_Ankle_Ik_Ctrl";
	setAttr ".Spaces" -type "string" "Mover_Gimbal_Ctrl, COG_Ctrl, L_Pelvis_Jnt, Mutant_Tools_Grp";
	setAttr -cb on ".Mirror" yes;
	setAttr -cb on ".CreateProxyOnTargetCtrl" yes;
	setAttr ".SetAttrsHolder" -type "string" "L_Hip_Jnt_Switch_Loc";
	setAttr ".postcode" -type "string" "";
	setAttr -k on ".Animbot" yes;
createNode hyperLayout -n "hyperLayout58";
	rename -uid "438E83FA-A544-98DC-A538-FC90C1D182FA";
	setAttr ".ihi" 0;
createNode network -n "L_FK_Hip_Switches_Config";
	rename -uid "7C74E864-3E46-FFDF-C98A-609A9C8C2305";
	addAttr -ci true -sn "precode" -ln "precode" -dt "string";
	addAttr -ci true -sn "Build_Command" -ln "Build_Command" -dt "string";
	addAttr -ci true -sn "Import_Command" -ln "Import_Command" -dt "string";
	addAttr -ci true -sn "Rotate" -ln "Rotate" -min 0 -max 1 -at "bool";
	addAttr -ci true -sn "Help" -ln "Help" -dt "string";
	addAttr -ci true -sn "Translate" -ln "Translate" -min 0 -max 1 -at "bool";
	addAttr -ci true -sn "SetTargetCtrl" -ln "SetTargetCtrl" -dt "string";
	addAttr -ci true -sn "Spaces" -ln "Spaces" -dt "string";
	addAttr -ci true -sn "Mirror" -ln "Mirror" -min 0 -max 1 -at "bool";
	addAttr -ci true -sn "CreateProxyOnTargetCtrl" -ln "CreateProxyOnTargetCtrl" -min 
		0 -max 1 -at "bool";
	addAttr -ci true -sn "SetAttrsHolder" -ln "SetAttrsHolder" -dt "string";
	addAttr -ci true -sn "postcode" -ln "postcode" -dt "string";
	addAttr -ci true -sn "Animbot" -ln "Animbot" -min 0 -max 1 -at "bool";
	setAttr ".precode" -type "string" "";
	setAttr -l on ".Build_Command" -type "string" "exec_spaceSwitches.build_spaceSwitches_block()";
	setAttr -l on ".Import_Command" -type "string" "import exec_spaceSwitches ";
	setAttr -cb on ".Rotate" yes;
	setAttr ".Help" -type "string" "Separate the space switches with a ','";
	setAttr -cb on ".Translate";
	setAttr ".SetTargetCtrl" -type "string" "L_Hip_Fk_Ctrl";
	setAttr ".Spaces" -type "string" "Mover_Gimbal_Ctrl, COG_Ctrl, L_Pelvis_Jnt, Mutant_Tools_Grp";
	setAttr -cb on ".Mirror" yes;
	setAttr -cb on ".CreateProxyOnTargetCtrl" yes;
	setAttr ".SetAttrsHolder" -type "string" "L_Hip_Jnt_Switch_Loc";
	setAttr ".postcode" -type "string" "";
	setAttr -k on ".Animbot" yes;
createNode hyperLayout -n "hyperLayout59";
	rename -uid "B99BF4EE-B84D-EE4D-72B4-6084418FFA5B";
	setAttr ".ihi" 0;
createNode network -n "L_PV_Hip_Switches_Config";
	rename -uid "567FA2C3-0949-BFF3-3869-519287B60E4C";
	addAttr -ci true -sn "precode" -ln "precode" -dt "string";
	addAttr -ci true -sn "Build_Command" -ln "Build_Command" -dt "string";
	addAttr -ci true -sn "Import_Command" -ln "Import_Command" -dt "string";
	addAttr -ci true -sn "Rotate" -ln "Rotate" -min 0 -max 1 -at "bool";
	addAttr -ci true -sn "Help" -ln "Help" -dt "string";
	addAttr -ci true -sn "Translate" -ln "Translate" -min 0 -max 1 -at "bool";
	addAttr -ci true -sn "SetTargetCtrl" -ln "SetTargetCtrl" -dt "string";
	addAttr -ci true -sn "Spaces" -ln "Spaces" -dt "string";
	addAttr -ci true -sn "Mirror" -ln "Mirror" -min 0 -max 1 -at "bool";
	addAttr -ci true -sn "CreateProxyOnTargetCtrl" -ln "CreateProxyOnTargetCtrl" -min 
		0 -max 1 -at "bool";
	addAttr -ci true -sn "SetAttrsHolder" -ln "SetAttrsHolder" -dt "string";
	addAttr -ci true -sn "postcode" -ln "postcode" -dt "string";
	addAttr -ci true -sn "Animbot" -ln "Animbot" -min 0 -max 1 -at "bool";
	setAttr ".precode" -type "string" "";
	setAttr -l on ".Build_Command" -type "string" "exec_spaceSwitches.build_spaceSwitches_block()";
	setAttr -l on ".Import_Command" -type "string" "import exec_spaceSwitches ";
	setAttr -cb on ".Rotate" yes;
	setAttr ".Help" -type "string" "Separate the space switches with a ','";
	setAttr -cb on ".Translate" yes;
	setAttr ".SetTargetCtrl" -type "string" "L_Ankle_Ik_PoleVector_Ctrl";
	setAttr ".Spaces" -type "string" "L_Ankle_Ik_Ctrl, Mover_Gimbal_Ctrl, Mutant_Tools_Grp,COG_Gimbal_Ctrl";
	setAttr -cb on ".Mirror" yes;
	setAttr -cb on ".CreateProxyOnTargetCtrl" yes;
	setAttr ".SetAttrsHolder" -type "string" "L_Hip_Jnt_Switch_Loc";
	setAttr ".postcode" -type "string" "";
	setAttr -k on ".Animbot" yes;
createNode hyperLayout -n "hyperLayout39";
	rename -uid "EB371C1E-D04B-E93C-909D-FAA7BBBEF100";
	setAttr ".ihi" 0;
createNode network -n "L_Arm_Attrs_Config";
	rename -uid "7DAD1043-1544-5C4A-5741-DCA2C292B3E0";
	addAttr -ci true -sn "precode" -ln "precode" -dt "string";
	addAttr -ci true -sn "Build_Command" -ln "Build_Command" -dt "string";
	addAttr -ci true -sn "Import_Command" -ln "Import_Command" -dt "string";
	addAttr -ci true -sn "SetParent" -ln "SetParent" -dt "string";
	addAttr -ci true -sn "Help" -ln "Help" -dt "string";
	addAttr -ci true -sn "SetCopyAttrsFrom" -ln "SetCopyAttrsFrom" -dt "string";
	addAttr -ci true -sn "postcode" -ln "postcode" -dt "string";
	addAttr -ci true -sn "CtrlShape" -ln "CtrlShape" -min 0 -max 5 -en "cross:gear:hexagon:octagon:square:2dArrow" 
		-at "enum";
	setAttr ".precode" -type "string" "";
	setAttr -l on ".Build_Command" -type "string" "exec_proxy_attr.build_proxy_attr_block()";
	setAttr -l on ".Import_Command" -type "string" "import exec_proxy_attr";
	setAttr ".SetParent" -type "string" "L_FrAnkle_Jnt";
	setAttr ".Help" -type "string" "Will duplicate and connect all proxy attrs from desire transform";
	setAttr ".SetCopyAttrsFrom" -type "string" "L_FrHip_Jnt_Switch_Loc";
	setAttr ".postcode" -type "string" "";
	setAttr -cb on ".CtrlShape" 1;
createNode hyperLayout -n "hyperLayout40";
	rename -uid "8DA0CF60-784E-C169-88CD-D198ECB75AED";
	setAttr ".ihi" 0;
createNode network -n "R_Arm_Attrs_Config";
	rename -uid "EBB36DDF-9443-EB67-D791-29B88962AD28";
	addAttr -ci true -sn "precode" -ln "precode" -dt "string";
	addAttr -ci true -sn "Build_Command" -ln "Build_Command" -dt "string";
	addAttr -ci true -sn "Import_Command" -ln "Import_Command" -dt "string";
	addAttr -ci true -sn "SetParent" -ln "SetParent" -dt "string";
	addAttr -ci true -sn "Help" -ln "Help" -dt "string";
	addAttr -ci true -sn "SetCopyAttrsFrom" -ln "SetCopyAttrsFrom" -dt "string";
	addAttr -ci true -sn "postcode" -ln "postcode" -dt "string";
	addAttr -ci true -sn "CtrlShape" -ln "CtrlShape" -min 0 -max 5 -en "cross:gear:hexagon:octagon:square:2dArrow" 
		-at "enum";
	setAttr ".precode" -type "string" "";
	setAttr -l on ".Build_Command" -type "string" "exec_proxy_attr.build_proxy_attr_block()";
	setAttr -l on ".Import_Command" -type "string" "import exec_proxy_attr";
	setAttr ".SetParent" -type "string" "R_FrAnkle_Jnt";
	setAttr ".Help" -type "string" "Will duplicate and connect all proxy attrs from desire transform";
	setAttr ".SetCopyAttrsFrom" -type "string" "R_FrHip_Jnt_Switch_Loc";
	setAttr ".postcode" -type "string" "";
	setAttr -cb on ".CtrlShape" 1;
createNode hyperLayout -n "hyperLayout41";
	rename -uid "9BA1B98A-4544-F62D-9314-F68282AE9088";
	setAttr ".ihi" 0;
createNode network -n "L_Legs_Attrs_Config";
	rename -uid "757B0E12-2642-22FB-F956-C798A249FF7E";
	addAttr -ci true -sn "precode" -ln "precode" -dt "string";
	addAttr -ci true -sn "Build_Command" -ln "Build_Command" -dt "string";
	addAttr -ci true -sn "Import_Command" -ln "Import_Command" -dt "string";
	addAttr -ci true -sn "SetParent" -ln "SetParent" -dt "string";
	addAttr -ci true -sn "Help" -ln "Help" -dt "string";
	addAttr -ci true -sn "SetCopyAttrsFrom" -ln "SetCopyAttrsFrom" -dt "string";
	addAttr -ci true -sn "postcode" -ln "postcode" -dt "string";
	addAttr -ci true -sn "CtrlShape" -ln "CtrlShape" -min 0 -max 5 -en "cross:gear:hexagon:octagon:square:2dArrow" 
		-at "enum";
	setAttr ".precode" -type "string" "";
	setAttr -l on ".Build_Command" -type "string" "exec_proxy_attr.build_proxy_attr_block()";
	setAttr -l on ".Import_Command" -type "string" "import exec_proxy_attr";
	setAttr ".SetParent" -type "string" "L_Ankle_Jnt";
	setAttr ".Help" -type "string" "Will duplicate and connect all proxy attrs from desire transform";
	setAttr ".SetCopyAttrsFrom" -type "string" "L_Hip_Jnt_Switch_Loc";
	setAttr ".postcode" -type "string" "";
	setAttr -cb on ".CtrlShape" 1;
createNode hyperLayout -n "hyperLayout42";
	rename -uid "7FA62AF4-8C42-A217-63BC-838B9CDE24B5";
	setAttr ".ihi" 0;
createNode network -n "R_Legs_Attrs_Config";
	rename -uid "1952E9F0-8D48-416C-315F-2A9A22B13B3F";
	addAttr -ci true -sn "precode" -ln "precode" -dt "string";
	addAttr -ci true -sn "Build_Command" -ln "Build_Command" -dt "string";
	addAttr -ci true -sn "Import_Command" -ln "Import_Command" -dt "string";
	addAttr -ci true -sn "SetParent" -ln "SetParent" -dt "string";
	addAttr -ci true -sn "Help" -ln "Help" -dt "string";
	addAttr -ci true -sn "SetCopyAttrsFrom" -ln "SetCopyAttrsFrom" -dt "string";
	addAttr -ci true -sn "postcode" -ln "postcode" -dt "string";
	addAttr -ci true -sn "CtrlShape" -ln "CtrlShape" -min 0 -max 5 -en "cross:gear:hexagon:octagon:square:2dArrow" 
		-at "enum";
	setAttr ".precode" -type "string" "";
	setAttr -l on ".Build_Command" -type "string" "exec_proxy_attr.build_proxy_attr_block()";
	setAttr -l on ".Import_Command" -type "string" "import exec_proxy_attr";
	setAttr ".SetParent" -type "string" "R_Ankle_Jnt";
	setAttr ".Help" -type "string" "Will duplicate and connect all proxy attrs from desire transform";
	setAttr ".SetCopyAttrsFrom" -type "string" "R_Hip_Jnt_Switch_Loc";
	setAttr ".postcode" -type "string" "";
	setAttr -cb on ".CtrlShape" 1;
createNode hyperLayout -n "hyperLayout24";
	rename -uid "CED4DD5E-F24E-8C33-FB18-549E2FEE7721";
	setAttr ".ihi" 0;
createNode network -n "Load_Skin_Config";
	rename -uid "1301E2FE-E043-78B0-5BEE-59B83BBCE4EC";
	addAttr -ci true -sn "precode" -ln "precode" -dt "string";
	addAttr -ci true -sn "Build_Command" -ln "Build_Command" -dt "string";
	addAttr -ci true -sn "Import_Command" -ln "Import_Command" -dt "string";
	addAttr -ci true -sn "Path" -ln "Path" -dt "string";
	addAttr -ci true -sn "Help" -ln "Help" -dt "string";
	addAttr -ci true -sn "postcode" -ln "postcode" -dt "string";
	setAttr ".precode" -type "string" "";
	setAttr -l on ".Build_Command" -type "string" "exec_load_skin.build_load_skin_block()";
	setAttr -l on ".Import_Command" -type "string" "import exec_load_skin";
	setAttr ".Path" -type "string" "";
	setAttr ".Help" -type "string" "Load Skin Cluster Data from Folder, you need nNgSkin tools installed for it to work.";
	setAttr ".postcode" -type "string" "";
createNode hyperLayout -n "hyperLayout25";
	rename -uid "05CD2E29-774C-B4A9-9C97-2D9BE7256428";
	setAttr ".ihi" 0;
createNode network -n "Load_Ctrls_Config";
	rename -uid "8C8B4434-DB4B-B4C9-7885-3592A3659044";
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
	setAttr ".Help" -type "string" "Load Ctrls Data from File";
	setAttr ".postcode" -type "string" "";
createNode hyperLayout -n "SausageTemplate_hyperLayout37";
	rename -uid "1D4D38F2-374D-CDCD-B515-F09E720759B8";
	setAttr ".ihi" 0;
createNode network -n "Unselectable_Config";
	rename -uid "544A3B7B-C24F-7E12-89FF-09B5319AD3B5";
	addAttr -ci true -sn "precode" -ln "precode" -dt "string";
	addAttr -ci true -sn "Build_Command" -ln "Build_Command" -dt "string";
	addAttr -ci true -sn "Import_Command" -ln "Import_Command" -dt "string";
	addAttr -ci true -sn "SetGeo" -ln "SetGeo" -dt "string";
	addAttr -ci true -sn "LockAttr" -ln "LockAttr" -dt "string";
	addAttr -ci true -sn "postcode" -ln "postcode" -dt "string";
	setAttr ".precode" -type "string" "";
	setAttr -l on ".Build_Command" -type "string" "exec_unselectable.build_unselectable_block()";
	setAttr -l on ".Import_Command" -type "string" "import exec_unselectable";
	setAttr ".SetGeo" -type "string" "geo";
	setAttr ".LockAttr" -type "string" "Global_Ctrl.Geo";
	setAttr ".postcode" -type "string" "";
createNode hyperLayout -n "hyperLayout47";
	rename -uid "7F4F68D6-1A41-D128-2CF9-EDAEC2F2E8C7";
	setAttr ".ihi" 0;
createNode network -n "DinamicScale_Config";
	rename -uid "A08A4810-7B4A-1164-DFDF-11A144E0C560";
	addAttr -ci true -sn "precode" -ln "precode" -dt "string";
	addAttr -ci true -sn "Build_Command" -ln "Build_Command" -dt "string";
	addAttr -ci true -sn "Import_Command" -ln "Import_Command" -dt "string";
	addAttr -ci true -sn "Help" -ln "Help" -dt "string";
	addAttr -ci true -sn "postcode" -ln "postcode" -dt "string";
	setAttr ".precode" -type "string" "";
	setAttr -l on ".Build_Command" -type "string" "exec_dinamic_scale.build_dinamic_scale_block()";
	setAttr -l on ".Import_Command" -type "string" "import exec_dinamic_scale";
	setAttr ".Help" -type "string" "Add Size Attrs and Extra Scale to Base";
	setAttr ".postcode" -type "string" "";
createNode hyperLayout -n "hyperLayout26";
	rename -uid "A0AEF976-3648-4663-FF54-1DB7DC116E40";
	setAttr ".ihi" 0;
	setAttr -s 2 ".hyp";
createNode network -n "Code_Config";
	rename -uid "DBB89DEB-5E4B-8895-15B5-41A05993CB85";
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
	setAttr ".Code" -type "string" "";
	setAttr ".postcode" -type "string" "";
select -ne :time1;
	setAttr ".o" 0;
select -ne :hardwareRenderingGlobals;
	setAttr ".msaa" yes;
	setAttr ".dli" 1;
	setAttr ".fprt" yes;
	setAttr ".rtfm" 1;
select -ne :renderPartition;
	setAttr -s 10 ".st";
select -ne :renderGlobalsList1;
select -ne :defaultShaderList1;
	setAttr -s 9 ".s";
select -ne :postProcessList1;
	setAttr -s 2 ".p";
select -ne :defaultRenderUtilityList1;
	setAttr -s 260 ".u";
select -ne :defaultRenderingList1;
select -ne :standardSurface1;
	setAttr ".bc" -type "float3" 0.40000001 0.40000001 0.40000001 ;
	setAttr ".sr" 0.40000000596046448;
select -ne :initialShadingGroup;
	setAttr -s 48 ".dsm";
select -ne :defaultRenderGlobals;
	addAttr -ci true -h true -sn "dss" -ln "defaultSurfaceShader" -dt "string";
	setAttr ".dss" -type "string" "lambert1";
select -ne :defaultResolution;
	setAttr ".w" 3036;
	setAttr ".h" 1627;
	setAttr ".dar" 1.8660110235214233;
select -ne :defaultColorMgtGlobals;
	setAttr ".cfe" yes;
	setAttr ".cfp" -type "string" "<MAYA_RESOURCES>/OCIO-configs/Maya-legacy/config.ocio";
	setAttr ".vtn" -type "string" "sRGB gamma (legacy)";
	setAttr ".vn" -type "string" "sRGB gamma";
	setAttr ".dn" -type "string" "legacy";
	setAttr ".wsn" -type "string" "scene-linear Rec 709/sRGB";
	setAttr ".ovt" no;
	setAttr ".povt" no;
	setAttr ".otn" -type "string" "sRGB gamma (legacy)";
	setAttr ".potn" -type "string" "sRGB gamma (legacy)";
select -ne :ikSystem;
	setAttr -s 3 ".sol";
connectAttr "hyperLayout13.msg" "BaseA_Block.hl";
connectAttr "BaseA_Config.nds" "BaseA_Block.nds";
connectAttr "hyperLayout14.msg" "Root_Block.hl";
connectAttr "Root_Config.nds" "Root_Block.nds";
connectAttr "hyperLayout15.msg" "COG_Block.hl";
connectAttr "COG_Config.nds" "COG_Block.nds";
connectAttr "hyperLayout17.msg" "L_Clavicle_Block.hl";
connectAttr "L_Clavicle_Config.nds" "L_Clavicle_Block.nds";
connectAttr "L_Clavicle_Guide.Helper" "L_Clavicle_Guide_CtrlShape.v";
connectAttr "L_Clavicle_Guide.Helper" "L_Clavicle_Guide_Ctrl_CtrlShape.v";
connectAttr "L_Clavicle_Guide.Helper" "L_Clavicle_Guide_Ctrl_Ctrl_CtrlShape.v";
connectAttr "L_Clavicle_Guide.Helper" "L_Clavicle_Guide_Ctrl_Ctrl_Ctrl_CtrlShape.v"
		;
connectAttr "L_Clavicle_Guide.s" "L_ClavicleEnd_Guide.is";
connectAttr "L_ClavicleEnd_Guide.Helper" "L_ClavicleEnd_Guide_CtrlShape.v";
connectAttr "L_ClavicleEnd_Guide.Helper" "L_ClavicleEnd_Guide_Ctrl_CtrlShape.v";
connectAttr "L_ClavicleEnd_Guide.Helper" "L_ClavicleEnd_Guide_Ctrl_Ctrl_CtrlShape.v"
		;
connectAttr "L_ClavicleEnd_Guide.Helper" "L_ClavicleEnd_Guide_Ctrl_Ctrl_Ctrl_CtrlShape.v"
		;
connectAttr "hyperLayout18.msg" "L_FrHip_Block.hl";
connectAttr "L_FrHip_Config.nds" "L_FrHip_Block.nds";
connectAttr "L_FrHip_Guide.Helper" "L_FrHip_Guide_CtrlShape.v";
connectAttr "L_FrHip_Guide.Helper" "L_FrHip_Guide_Ctrl_CtrlShape.v";
connectAttr "L_FrHip_Guide.Helper" "L_FrHip_Guide_Ctrl_Ctrl_CtrlShape.v";
connectAttr "L_FrHip_Guide.Helper" "L_FrHip_Guide_Ctrl_Ctrl_Ctrl_CtrlShape.v";
connectAttr "L_FrHip_Guide.s" "L_FrKnee_Guide.is";
connectAttr "L_FrKnee_Guide.Helper" "L_FrKnee_Guide_CtrlShape.v";
connectAttr "L_FrKnee_Guide.Helper" "L_FrKnee_Guide_Ctrl_CtrlShape.v";
connectAttr "L_FrKnee_Guide.Helper" "L_FrKnee_Guide_Ctrl_Ctrl_CtrlShape.v";
connectAttr "L_FrKnee_Guide.Helper" "L_FrKnee_Guide_Ctrl_Ctrl_Ctrl_CtrlShape.v";
connectAttr "L_FrKnee_Guide.s" "L_FrAnkle_Guide.is";
connectAttr "L_FrAnkle_Guide.Helper" "L_FrAnkle_Guide_CtrlShape.v";
connectAttr "L_FrAnkle_Guide.Helper" "L_FrAnkle_Guide_Ctrl_CtrlShape.v";
connectAttr "L_FrAnkle_Guide.Helper" "L_FrAnkle_Guide_Ctrl_Ctrl_CtrlShape.v";
connectAttr "L_FrAnkle_Guide.Helper" "L_FrAnkle_Guide_Ctrl_Ctrl_Ctrl_CtrlShape.v"
		;
connectAttr "hyperLayout19.msg" "L_Pelvis_Block.hl";
connectAttr "L_Pelvis_Config.nds" "L_Pelvis_Block.nds";
connectAttr "L_Pelvis_Guide.Helper" "L_Pelvis_Guide_CtrlShape.v";
connectAttr "L_Pelvis_Guide.Helper" "L_Pelvis_Guide_Ctrl_CtrlShape.v";
connectAttr "L_Pelvis_Guide.Helper" "L_Pelvis_Guide_Ctrl_Ctrl_CtrlShape.v";
connectAttr "L_Pelvis_Guide.Helper" "L_Pelvis_Guide_Ctrl_Ctrl_Ctrl_CtrlShape.v";
connectAttr "L_Pelvis_Guide.s" "L_PelvisEnd_Guide.is";
connectAttr "L_PelvisEnd_Guide.Helper" "L_PelvisEnd_Guide_CtrlShape.v";
connectAttr "L_PelvisEnd_Guide.Helper" "L_PelvisEnd_Guide_Ctrl_CtrlShape.v";
connectAttr "L_PelvisEnd_Guide.Helper" "L_PelvisEnd_Guide_Ctrl_Ctrl_CtrlShape.v"
		;
connectAttr "L_PelvisEnd_Guide.Helper" "L_PelvisEnd_Guide_Ctrl_Ctrl_Ctrl_CtrlShape.v"
		;
connectAttr "hyperLayout20.msg" "L_Hip_Block.hl";
connectAttr "L_Hip_Config.nds" "L_Hip_Block.nds";
connectAttr "L_Hip_Guide.Helper" "L_Hip_Guide_CtrlShape.v";
connectAttr "L_Hip_Guide.Helper" "L_Hip_Guide_Ctrl_CtrlShape.v";
connectAttr "L_Hip_Guide.Helper" "L_Hip_Guide_Ctrl_Ctrl_CtrlShape.v";
connectAttr "L_Hip_Guide.Helper" "L_Hip_Guide_Ctrl_Ctrl_Ctrl_CtrlShape.v";
connectAttr "L_Hip_Guide.s" "L_Knee_Guide.is";
connectAttr "L_Knee_Guide.Helper" "L_Knee_Guide_CtrlShape.v";
connectAttr "L_Knee_Guide.Helper" "L_Knee_Guide_Ctrl_CtrlShape.v";
connectAttr "L_Knee_Guide.Helper" "L_Knee_Guide_Ctrl_Ctrl_CtrlShape.v";
connectAttr "L_Knee_Guide.Helper" "L_Knee_Guide_Ctrl_Ctrl_Ctrl_CtrlShape.v";
connectAttr "L_Knee_Guide.s" "L_Ankle_Guide.is";
connectAttr "L_Ankle_Guide.Helper" "L_Ankle_Guide_CtrlShape.v";
connectAttr "L_Ankle_Guide.Helper" "L_Ankle_Guide_Ctrl_CtrlShape.v";
connectAttr "L_Ankle_Guide.Helper" "L_Ankle_Guide_Ctrl_Ctrl_CtrlShape.v";
connectAttr "L_Ankle_Guide.Helper" "L_Ankle_Guide_Ctrl_Ctrl_Ctrl_CtrlShape.v";
connectAttr "NewGuide_hyperLayout23.msg" "L_Foot_Block.hl";
connectAttr "L_Foot_Config.nds" "L_Foot_Block.nds";
connectAttr "L_Foot_Ankle_Guide.Helper" "L_Foot_Ankle_Guide_CtrlShape.v";
connectAttr "L_Foot_Ankle_Guide.Helper" "L_Foot_Ankle_Guide_Ctrl_CtrlShape.v";
connectAttr "L_Foot_Ankle_Guide.Helper" "L_Foot_Ankle_Guide_Ctrl_Ctrl_CtrlShape.v"
		;
connectAttr "L_Foot_Ankle_Guide.Helper" "L_Foot_Ankle_Guide_Ctrl_Ctrl_Ctrl_CtrlShape.v"
		;
connectAttr "L_Foot_Ankle_Guide.s" "L_Foot_Heel_Guide.is";
connectAttr "L_Foot_Heel_Guide.Helper" "L_Foot_Heel_Guide_CtrlShape.v";
connectAttr "L_Foot_Heel_Guide.Helper" "L_Foot_Heel_Guide_Ctrl_CtrlShape.v";
connectAttr "L_Foot_Heel_Guide.Helper" "L_Foot_Heel_Guide_Ctrl_Ctrl_CtrlShape.v"
		;
connectAttr "L_Foot_Heel_Guide.Helper" "L_Foot_Heel_Guide_Ctrl_Ctrl_Ctrl_CtrlShape.v"
		;
connectAttr "L_Foot_Ankle_Guide.s" "L_Foot_Ball_Guide.is";
connectAttr "L_Foot_Ball_Guide.Helper" "L_Foot_Ball_Guide_CtrlShape.v";
connectAttr "L_Foot_Ball_Guide.Helper" "L_Foot_Ball_Guide_Ctrl_CtrlShape.v";
connectAttr "L_Foot_Ball_Guide.Helper" "L_Foot_Ball_Guide_Ctrl_Ctrl_CtrlShape.v"
		;
connectAttr "L_Foot_Ball_Guide.Helper" "L_Foot_Ball_Guide_Ctrl_Ctrl_Ctrl_CtrlShape.v"
		;
connectAttr "L_Foot_Ball_Guide.s" "L_Foot_BallFloor_Guide.is";
connectAttr "L_Foot_BallFloor_Guide.Helper" "L_Foot_BallFloor_Guide_CtrlShape.v"
		;
connectAttr "L_Foot_BallFloor_Guide.Helper" "L_Foot_BallFloor_Guide_Ctrl_CtrlShape.v"
		;
connectAttr "L_Foot_BallFloor_Guide.Helper" "L_Foot_BallFloor_Guide_Ctrl_Ctrl_CtrlShape.v"
		;
connectAttr "L_Foot_BallFloor_Guide.Helper" "L_Foot_BallFloor_Guide_Ctrl_Ctrl_Ctrl_CtrlShape.v"
		;
connectAttr "L_Foot_BallFloor_Guide.s" "L_Foot_Out_Guide.is";
connectAttr "L_Foot_Out_Guide.Helper" "L_Foot_Out_Guide_CtrlShape.v";
connectAttr "L_Foot_Out_Guide.Helper" "L_Foot_Out_Guide_Ctrl_CtrlShape.v";
connectAttr "L_Foot_Out_Guide.Helper" "L_Foot_Out_Guide_Ctrl_Ctrl_CtrlShape.v";
connectAttr "L_Foot_Out_Guide.Helper" "L_Foot_Out_Guide_Ctrl_Ctrl_Ctrl_CtrlShape.v"
		;
connectAttr "L_Foot_BallFloor_Guide.s" "L_Foot_In_Guide.is";
connectAttr "L_Foot_In_Guide.Helper" "L_Foot_In_Guide_CtrlShape.v";
connectAttr "L_Foot_In_Guide.Helper" "L_Foot_In_Guide_Ctrl_CtrlShape.v";
connectAttr "L_Foot_In_Guide.Helper" "L_Foot_In_Guide_Ctrl_Ctrl_CtrlShape.v";
connectAttr "L_Foot_In_Guide.Helper" "L_Foot_In_Guide_Ctrl_Ctrl_Ctrl_CtrlShape.v"
		;
connectAttr "L_Foot_Ball_Guide.s" "L_Foot_Toes_Guide.is";
connectAttr "L_Foot_Toes_Guide.Helper" "L_Foot_Toes_Guide_CtrlShape.v";
connectAttr "L_Foot_Toes_Guide.Helper" "L_Foot_Toes_Guide_Ctrl_CtrlShape.v";
connectAttr "L_Foot_Toes_Guide.Helper" "L_Foot_Toes_Guide_Ctrl_Ctrl_CtrlShape.v"
		;
connectAttr "L_Foot_Toes_Guide.Helper" "L_Foot_Toes_Guide_Ctrl_Ctrl_Ctrl_CtrlShape.v"
		;
connectAttr "L_Foot_Ankle_Guide.s" "L_Foot_HeelMid_Guide.is";
connectAttr "L_Foot_HeelMid_Guide.Helper" "L_Foot_HeelMid_Guide_CtrlShape.v";
connectAttr "L_Foot_HeelMid_Guide.Helper" "L_Foot_HeelMid_Guide_Ctrl_CtrlShape.v"
		;
connectAttr "L_Foot_HeelMid_Guide.Helper" "L_Foot_HeelMid_Guide_Ctrl_Ctrl_CtrlShape.v"
		;
connectAttr "L_Foot_HeelMid_Guide.Helper" "L_Foot_HeelMid_Guide_Ctrl_Ctrl_Ctrl_CtrlShape.v"
		;
connectAttr "hyperLayout67.msg" "Smart_RFL_Block.hl";
connectAttr "Smart_RFL_Config.nds" "Smart_RFL_Block.nds";
connectAttr "hyperLayout66.msg" "L_Smart_RFL_Block.hl";
connectAttr "L_Smart_RFL_Config.nds" "L_Smart_RFL_Block.nds";
connectAttr "NewGuide_hyperLayout24.msg" "L_FrFoot_Block.hl";
connectAttr "L_FrFoot_Config.nds" "L_FrFoot_Block.nds";
connectAttr "L_FrFoot_Ankle_Guide.s" "L_FrFoot_Heel_Guide.is";
connectAttr "L_FrFoot_Ankle_Guide.s" "L_FrFoot_Ball_Guide.is";
connectAttr "L_FrFoot_Ball_Guide.s" "L_FrFoot_BallFloor_Guide.is";
connectAttr "L_FrFoot_BallFloor_Guide.s" "L_FrFoot_Out_Guide.is";
connectAttr "L_FrFoot_BallFloor_Guide.s" "L_FrFoot_In_Guide.is";
connectAttr "L_FrFoot_Ball_Guide.s" "L_FrFoot_Toes_Guide.is";
connectAttr "L_FrFoot_Ankle_Guide.s" "L_FrFoot_HeelMid_Guide.is";
connectAttr "hyperLayout65.msg" "L_FrFootBox_Block.hl";
connectAttr "L_FrFootBox_Config.nds" "L_FrFootBox_Block.nds";
connectAttr "hyperLayout63.msg" "FrSmart_RFL_Block.hl";
connectAttr "FrSmart_RFL_Config.nds" "FrSmart_RFL_Block.nds";
connectAttr "hyperLayout68.msg" "Neck_Block.hl";
connectAttr "Neck_Config.nds" "Neck_Block.nds";
connectAttr "hyperLayout69.msg" "Head_Block.hl";
connectAttr "Head_Config.nds" "Head_Block.nds";
connectAttr "hyperLayout36.msg" "L_Eyes_Block.hl";
connectAttr "L_Eyes_Config.nds" "L_Eyes_Block.nds";
connectAttr "L_Eyes_Guide.Helper" "L_Eyes_Guide_CtrlShape.v";
connectAttr "L_Eyes_Guide.Helper" "L_Eyes_Guide_Ctrl_CtrlShape.v";
connectAttr "L_Eyes_Guide.Helper" "L_Eyes_Guide_Ctrl_Ctrl_CtrlShape.v";
connectAttr "L_Eyes_Guide.Helper" "L_Eyes_Guide_Ctrl_Ctrl_Ctrl_CtrlShape.v";
connectAttr "L_Eyes_Guide.s" "L_Eyes_Aim_Guide.is";
connectAttr "L_Eyes_Aim_Guide.Helper" "L_Eyes_Aim_Guide_CtrlShape.v";
connectAttr "L_Eyes_Aim_Guide.Helper" "L_Eyes_Aim_Guide_Ctrl_CtrlShape.v";
connectAttr "L_Eyes_Aim_Guide.Helper" "L_Eyes_Aim_Guide_Ctrl_Ctrl_CtrlShape.v";
connectAttr "L_Eyes_Aim_Guide.Helper" "L_Eyes_Aim_Guide_Ctrl_Ctrl_Ctrl_CtrlShape.v"
		;
connectAttr "hyperLayout71.msg" "Tail_Block.hl";
connectAttr "Tail_Config.nds" "Tail_Block.nds";
connectAttr "hyperLayout51.msg" "Eyes_Switches_Block.hl";
connectAttr "Eyes_Switches_Config.nds" "Eyes_Switches_Block.nds";
connectAttr "hyperLayout54.msg" "L_IK_FrLeg_Switches_Block.hl";
connectAttr "L_IK_FrLeg_Switches_Config.nds" "L_IK_FrLeg_Switches_Block.nds";
connectAttr "hyperLayout55.msg" "L_FK_FrLeg_Switches_Block.hl";
connectAttr "L_FK_FrLeg_Switches_Config.nds" "L_FK_FrLeg_Switches_Block.nds";
connectAttr "hyperLayout56.msg" "L_PV_FrLeg_Switches_Block.hl";
connectAttr "L_PV_FrLeg_Switches_Config.nds" "L_PV_FrLeg_Switches_Block.nds";
connectAttr "hyperLayout57.msg" "L_IK_Hip_Switches_Block.hl";
connectAttr "L_IK_Hip_Switches_Config.nds" "L_IK_Hip_Switches_Block.nds";
connectAttr "hyperLayout58.msg" "L_FK_Hip_Switches_Block.hl";
connectAttr "L_FK_Hip_Switches_Config.nds" "L_FK_Hip_Switches_Block.nds";
connectAttr "hyperLayout59.msg" "L_PV_Hip_Switches_Block.hl";
connectAttr "L_PV_Hip_Switches_Config.nds" "L_PV_Hip_Switches_Block.nds";
connectAttr "hyperLayout39.msg" "L_Arm_Attrs_Block.hl";
connectAttr "L_Arm_Attrs_Config.nds" "L_Arm_Attrs_Block.nds";
connectAttr "hyperLayout40.msg" "R_Arm_Attrs_Block.hl";
connectAttr "R_Arm_Attrs_Config.nds" "R_Arm_Attrs_Block.nds";
connectAttr "hyperLayout41.msg" "L_Legs_Attrs_Block.hl";
connectAttr "L_Legs_Attrs_Config.nds" "L_Legs_Attrs_Block.nds";
connectAttr "hyperLayout42.msg" "R_Legs_Attrs_Block.hl";
connectAttr "R_Legs_Attrs_Config.nds" "R_Legs_Attrs_Block.nds";
connectAttr "hyperLayout24.msg" "Load_Skin_Block.hl";
connectAttr "Load_Skin_Config.nds" "Load_Skin_Block.nds";
connectAttr "hyperLayout25.msg" "Load_Ctrls_Block.hl";
connectAttr "Load_Ctrls_Config.nds" "Load_Ctrls_Block.nds";
connectAttr "SausageTemplate_hyperLayout37.msg" "Unselectable_Block.hl";
connectAttr "Unselectable_Config.nds" "Unselectable_Block.nds";
connectAttr "hyperLayout47.msg" "DinamicScale_Block.hl";
connectAttr "DinamicScale_Config.nds" "DinamicScale_Block.nds";
connectAttr "hyperLayout26.msg" "Code_Block.hl";
connectAttr "Code_Config.nds" "Code_Block.nds";
connectAttr "COG_Loc.msg" "hyperLayout15.hyp[18].dn";
connectAttr "COG_LocShape.msg" "hyperLayout15.hyp[19].dn";
connectAttr "L_Clavicle_Guide.msg" "hyperLayout17.hyp[220].dn";
connectAttr "L_Clavicle_Guide_CtrlShape.msg" "hyperLayout17.hyp[221].dn";
connectAttr "L_Clavicle_Guide_Ctrl_CtrlShape.msg" "hyperLayout17.hyp[222].dn";
connectAttr "L_Clavicle_Guide_Ctrl_Ctrl_CtrlShape.msg" "hyperLayout17.hyp[223].dn"
		;
connectAttr "L_Clavicle_Guide_Ctrl_Ctrl_Ctrl_CtrlShape.msg" "hyperLayout17.hyp[224].dn"
		;
connectAttr "L_ClavicleEnd_Guide.msg" "hyperLayout17.hyp[225].dn";
connectAttr "L_ClavicleEnd_Guide_CtrlShape.msg" "hyperLayout17.hyp[226].dn";
connectAttr "L_ClavicleEnd_Guide_Ctrl_CtrlShape.msg" "hyperLayout17.hyp[227].dn"
		;
connectAttr "L_ClavicleEnd_Guide_Ctrl_Ctrl_CtrlShape.msg" "hyperLayout17.hyp[228].dn"
		;
connectAttr "L_ClavicleEnd_Guide_Ctrl_Ctrl_Ctrl_CtrlShape.msg" "hyperLayout17.hyp[229].dn"
		;
connectAttr "L_FrHip_Guide.msg" "hyperLayout18.hyp[240].dn";
connectAttr "L_FrHip_Guide_CtrlShape.msg" "hyperLayout18.hyp[241].dn";
connectAttr "L_FrHip_Guide_Ctrl_CtrlShape.msg" "hyperLayout18.hyp[242].dn";
connectAttr "L_FrHip_Guide_Ctrl_Ctrl_CtrlShape.msg" "hyperLayout18.hyp[243].dn";
connectAttr "L_FrHip_Guide_Ctrl_Ctrl_Ctrl_CtrlShape.msg" "hyperLayout18.hyp[244].dn"
		;
connectAttr "L_FrKnee_Guide.msg" "hyperLayout18.hyp[255].dn";
connectAttr "L_FrKnee_Guide_CtrlShape.msg" "hyperLayout18.hyp[256].dn";
connectAttr "L_FrKnee_Guide_Ctrl_CtrlShape.msg" "hyperLayout18.hyp[257].dn";
connectAttr "L_FrKnee_Guide_Ctrl_Ctrl_CtrlShape.msg" "hyperLayout18.hyp[258].dn"
		;
connectAttr "L_FrKnee_Guide_Ctrl_Ctrl_Ctrl_CtrlShape.msg" "hyperLayout18.hyp[259].dn"
		;
connectAttr "L_FrAnkle_Guide.msg" "hyperLayout18.hyp[265].dn";
connectAttr "L_FrAnkle_Guide_CtrlShape.msg" "hyperLayout18.hyp[266].dn";
connectAttr "L_FrAnkle_Guide_Ctrl_CtrlShape.msg" "hyperLayout18.hyp[267].dn";
connectAttr "L_FrAnkle_Guide_Ctrl_Ctrl_CtrlShape.msg" "hyperLayout18.hyp[268].dn"
		;
connectAttr "L_FrAnkle_Guide_Ctrl_Ctrl_Ctrl_CtrlShape.msg" "hyperLayout18.hyp[269].dn"
		;
connectAttr "L_Pelvis_Guide.msg" "hyperLayout19.hyp[220].dn";
connectAttr "L_Pelvis_Guide_CtrlShape.msg" "hyperLayout19.hyp[221].dn";
connectAttr "L_Pelvis_Guide_Ctrl_CtrlShape.msg" "hyperLayout19.hyp[222].dn";
connectAttr "L_Pelvis_Guide_Ctrl_Ctrl_CtrlShape.msg" "hyperLayout19.hyp[223].dn"
		;
connectAttr "L_Pelvis_Guide_Ctrl_Ctrl_Ctrl_CtrlShape.msg" "hyperLayout19.hyp[224].dn"
		;
connectAttr "L_PelvisEnd_Guide.msg" "hyperLayout19.hyp[225].dn";
connectAttr "L_PelvisEnd_Guide_CtrlShape.msg" "hyperLayout19.hyp[226].dn";
connectAttr "L_PelvisEnd_Guide_Ctrl_CtrlShape.msg" "hyperLayout19.hyp[227].dn";
connectAttr "L_PelvisEnd_Guide_Ctrl_Ctrl_CtrlShape.msg" "hyperLayout19.hyp[228].dn"
		;
connectAttr "L_PelvisEnd_Guide_Ctrl_Ctrl_Ctrl_CtrlShape.msg" "hyperLayout19.hyp[229].dn"
		;
connectAttr "L_Hip_Guide.msg" "hyperLayout20.hyp[390].dn";
connectAttr "L_Hip_Guide_CtrlShape.msg" "hyperLayout20.hyp[391].dn";
connectAttr "L_Hip_Guide_Ctrl_CtrlShape.msg" "hyperLayout20.hyp[392].dn";
connectAttr "L_Hip_Guide_Ctrl_Ctrl_CtrlShape.msg" "hyperLayout20.hyp[393].dn";
connectAttr "L_Hip_Guide_Ctrl_Ctrl_Ctrl_CtrlShape.msg" "hyperLayout20.hyp[394].dn"
		;
connectAttr "L_Knee_Guide.msg" "hyperLayout20.hyp[395].dn";
connectAttr "L_Knee_Guide_CtrlShape.msg" "hyperLayout20.hyp[396].dn";
connectAttr "L_Knee_Guide_Ctrl_CtrlShape.msg" "hyperLayout20.hyp[397].dn";
connectAttr "L_Knee_Guide_Ctrl_Ctrl_CtrlShape.msg" "hyperLayout20.hyp[398].dn";
connectAttr "L_Knee_Guide_Ctrl_Ctrl_Ctrl_CtrlShape.msg" "hyperLayout20.hyp[399].dn"
		;
connectAttr "L_Ankle_Guide.msg" "hyperLayout20.hyp[400].dn";
connectAttr "L_Ankle_Guide_CtrlShape.msg" "hyperLayout20.hyp[401].dn";
connectAttr "L_Ankle_Guide_Ctrl_CtrlShape.msg" "hyperLayout20.hyp[402].dn";
connectAttr "L_Ankle_Guide_Ctrl_Ctrl_CtrlShape.msg" "hyperLayout20.hyp[403].dn";
connectAttr "L_Ankle_Guide_Ctrl_Ctrl_Ctrl_CtrlShape.msg" "hyperLayout20.hyp[404].dn"
		;
connectAttr "L_Foot_Ankle_Guide.msg" "NewGuide_hyperLayout23.hyp[1281].dn";
connectAttr "L_Foot_Ankle_Guide_CtrlShape.msg" "NewGuide_hyperLayout23.hyp[1282].dn"
		;
connectAttr "L_Foot_Ankle_Guide_Ctrl_CtrlShape.msg" "NewGuide_hyperLayout23.hyp[1283].dn"
		;
connectAttr "L_Foot_Ankle_Guide_Ctrl_Ctrl_CtrlShape.msg" "NewGuide_hyperLayout23.hyp[1284].dn"
		;
connectAttr "L_Foot_Ankle_Guide_Ctrl_Ctrl_Ctrl_CtrlShape.msg" "NewGuide_hyperLayout23.hyp[1285].dn"
		;
connectAttr "L_Foot_Heel_Guide.msg" "NewGuide_hyperLayout23.hyp[1286].dn";
connectAttr "L_Foot_Heel_Guide_CtrlShape.msg" "NewGuide_hyperLayout23.hyp[1287].dn"
		;
connectAttr "L_Foot_Heel_Guide_Ctrl_CtrlShape.msg" "NewGuide_hyperLayout23.hyp[1288].dn"
		;
connectAttr "L_Foot_Heel_Guide_Ctrl_Ctrl_CtrlShape.msg" "NewGuide_hyperLayout23.hyp[1289].dn"
		;
connectAttr "L_Foot_Heel_Guide_Ctrl_Ctrl_Ctrl_CtrlShape.msg" "NewGuide_hyperLayout23.hyp[1290].dn"
		;
connectAttr "L_Foot_Ball_Guide.msg" "NewGuide_hyperLayout23.hyp[1291].dn";
connectAttr "L_Foot_Ball_Guide_CtrlShape.msg" "NewGuide_hyperLayout23.hyp[1292].dn"
		;
connectAttr "L_Foot_Ball_Guide_Ctrl_CtrlShape.msg" "NewGuide_hyperLayout23.hyp[1293].dn"
		;
connectAttr "L_Foot_Ball_Guide_Ctrl_Ctrl_CtrlShape.msg" "NewGuide_hyperLayout23.hyp[1294].dn"
		;
connectAttr "L_Foot_Ball_Guide_Ctrl_Ctrl_Ctrl_CtrlShape.msg" "NewGuide_hyperLayout23.hyp[1295].dn"
		;
connectAttr "L_Foot_BallFloor_Guide.msg" "NewGuide_hyperLayout23.hyp[1296].dn";
connectAttr "L_Foot_BallFloor_Guide_CtrlShape.msg" "NewGuide_hyperLayout23.hyp[1297].dn"
		;
connectAttr "L_Foot_BallFloor_Guide_Ctrl_CtrlShape.msg" "NewGuide_hyperLayout23.hyp[1298].dn"
		;
connectAttr "L_Foot_BallFloor_Guide_Ctrl_Ctrl_CtrlShape.msg" "NewGuide_hyperLayout23.hyp[1299].dn"
		;
connectAttr "L_Foot_BallFloor_Guide_Ctrl_Ctrl_Ctrl_CtrlShape.msg" "NewGuide_hyperLayout23.hyp[1300].dn"
		;
connectAttr "L_Foot_Out_Guide.msg" "NewGuide_hyperLayout23.hyp[1301].dn";
connectAttr "L_Foot_Out_Guide_CtrlShape.msg" "NewGuide_hyperLayout23.hyp[1302].dn"
		;
connectAttr "L_Foot_Out_Guide_Ctrl_CtrlShape.msg" "NewGuide_hyperLayout23.hyp[1303].dn"
		;
connectAttr "L_Foot_Out_Guide_Ctrl_Ctrl_CtrlShape.msg" "NewGuide_hyperLayout23.hyp[1304].dn"
		;
connectAttr "L_Foot_Out_Guide_Ctrl_Ctrl_Ctrl_CtrlShape.msg" "NewGuide_hyperLayout23.hyp[1305].dn"
		;
connectAttr "L_Foot_In_Guide.msg" "NewGuide_hyperLayout23.hyp[1306].dn";
connectAttr "L_Foot_In_Guide_CtrlShape.msg" "NewGuide_hyperLayout23.hyp[1307].dn"
		;
connectAttr "L_Foot_In_Guide_Ctrl_CtrlShape.msg" "NewGuide_hyperLayout23.hyp[1308].dn"
		;
connectAttr "L_Foot_In_Guide_Ctrl_Ctrl_CtrlShape.msg" "NewGuide_hyperLayout23.hyp[1309].dn"
		;
connectAttr "L_Foot_In_Guide_Ctrl_Ctrl_Ctrl_CtrlShape.msg" "NewGuide_hyperLayout23.hyp[1310].dn"
		;
connectAttr "L_Foot_HeelMid_Guide.msg" "NewGuide_hyperLayout23.hyp[1311].dn";
connectAttr "L_Foot_HeelMid_Guide_CtrlShape.msg" "NewGuide_hyperLayout23.hyp[1312].dn"
		;
connectAttr "L_Foot_HeelMid_Guide_Ctrl_CtrlShape.msg" "NewGuide_hyperLayout23.hyp[1313].dn"
		;
connectAttr "L_Foot_HeelMid_Guide_Ctrl_Ctrl_CtrlShape.msg" "NewGuide_hyperLayout23.hyp[1314].dn"
		;
connectAttr "L_Foot_HeelMid_Guide_Ctrl_Ctrl_Ctrl_CtrlShape.msg" "NewGuide_hyperLayout23.hyp[1315].dn"
		;
connectAttr "L_Foot_Toes_Guide.msg" "NewGuide_hyperLayout23.hyp[1316].dn";
connectAttr "L_Foot_Toes_Guide_CtrlShape.msg" "NewGuide_hyperLayout23.hyp[1317].dn"
		;
connectAttr "L_Foot_Toes_Guide_Ctrl_CtrlShape.msg" "NewGuide_hyperLayout23.hyp[1318].dn"
		;
connectAttr "L_Foot_Toes_Guide_Ctrl_Ctrl_CtrlShape.msg" "NewGuide_hyperLayout23.hyp[1319].dn"
		;
connectAttr "L_Foot_Toes_Guide_Ctrl_Ctrl_Ctrl_CtrlShape.msg" "NewGuide_hyperLayout23.hyp[1320].dn"
		;
connectAttr "L_FrFoot_Ankle_Guide.msg" "NewGuide_hyperLayout24.hyp[855].dn";
connectAttr "L_FrFoot_Ankle_Guide_CtrlShape.msg" "NewGuide_hyperLayout24.hyp[856].dn"
		;
connectAttr "L_FrFoot_Ankle_Guide_Ctrl_CtrlShape.msg" "NewGuide_hyperLayout24.hyp[857].dn"
		;
connectAttr "L_FrFoot_Ankle_Guide_Ctrl_Ctrl_CtrlShape.msg" "NewGuide_hyperLayout24.hyp[858].dn"
		;
connectAttr "L_FrFoot_Ankle_Guide_Ctrl_Ctrl_Ctrl_CtrlShape.msg" "NewGuide_hyperLayout24.hyp[859].dn"
		;
connectAttr "L_FrFoot_Heel_Guide.msg" "NewGuide_hyperLayout24.hyp[895].dn";
connectAttr "L_FrFoot_Heel_Guide_CtrlShape.msg" "NewGuide_hyperLayout24.hyp[896].dn"
		;
connectAttr "L_FrFoot_Heel_Guide_Ctrl_CtrlShape.msg" "NewGuide_hyperLayout24.hyp[897].dn"
		;
connectAttr "L_FrFoot_Heel_Guide_Ctrl_Ctrl_CtrlShape.msg" "NewGuide_hyperLayout24.hyp[898].dn"
		;
connectAttr "L_FrFoot_Heel_Guide_Ctrl_Ctrl_Ctrl_CtrlShape.msg" "NewGuide_hyperLayout24.hyp[899].dn"
		;
connectAttr "L_FrFoot_Ball_Guide.msg" "NewGuide_hyperLayout24.hyp[900].dn";
connectAttr "L_FrFoot_Ball_Guide_CtrlShape.msg" "NewGuide_hyperLayout24.hyp[901].dn"
		;
connectAttr "L_FrFoot_Ball_Guide_Ctrl_CtrlShape.msg" "NewGuide_hyperLayout24.hyp[902].dn"
		;
connectAttr "L_FrFoot_Ball_Guide_Ctrl_Ctrl_CtrlShape.msg" "NewGuide_hyperLayout24.hyp[903].dn"
		;
connectAttr "L_FrFoot_Ball_Guide_Ctrl_Ctrl_Ctrl_CtrlShape.msg" "NewGuide_hyperLayout24.hyp[904].dn"
		;
connectAttr "L_FrFoot_HeelMid_Guide.msg" "NewGuide_hyperLayout24.hyp[925].dn";
connectAttr "L_FrFoot_HeelMid_Guide_CtrlShape.msg" "NewGuide_hyperLayout24.hyp[926].dn"
		;
connectAttr "L_FrFoot_HeelMid_Guide_Ctrl_CtrlShape.msg" "NewGuide_hyperLayout24.hyp[927].dn"
		;
connectAttr "L_FrFoot_HeelMid_Guide_Ctrl_Ctrl_CtrlShape.msg" "NewGuide_hyperLayout24.hyp[928].dn"
		;
connectAttr "L_FrFoot_HeelMid_Guide_Ctrl_Ctrl_Ctrl_CtrlShape.msg" "NewGuide_hyperLayout24.hyp[929].dn"
		;
connectAttr "L_FrFoot_Toes_Guide.msg" "NewGuide_hyperLayout24.hyp[930].dn";
connectAttr "L_FrFoot_Toes_Guide_CtrlShape.msg" "NewGuide_hyperLayout24.hyp[931].dn"
		;
connectAttr "L_FrFoot_Toes_Guide_Ctrl_CtrlShape.msg" "NewGuide_hyperLayout24.hyp[932].dn"
		;
connectAttr "L_FrFoot_Toes_Guide_Ctrl_Ctrl_CtrlShape.msg" "NewGuide_hyperLayout24.hyp[933].dn"
		;
connectAttr "L_FrFoot_Toes_Guide_Ctrl_Ctrl_Ctrl_CtrlShape.msg" "NewGuide_hyperLayout24.hyp[934].dn"
		;
connectAttr "L_FrFoot_BallFloor_Guide.msg" "NewGuide_hyperLayout24.hyp[935].dn";
connectAttr "L_FrFoot_BallFloor_Guide_CtrlShape.msg" "NewGuide_hyperLayout24.hyp[936].dn"
		;
connectAttr "L_FrFoot_BallFloor_Guide_Ctrl_CtrlShape.msg" "NewGuide_hyperLayout24.hyp[937].dn"
		;
connectAttr "L_FrFoot_BallFloor_Guide_Ctrl_Ctrl_CtrlShape.msg" "NewGuide_hyperLayout24.hyp[938].dn"
		;
connectAttr "L_FrFoot_BallFloor_Guide_Ctrl_Ctrl_Ctrl_CtrlShape.msg" "NewGuide_hyperLayout24.hyp[939].dn"
		;
connectAttr "L_FrFoot_In_Guide.msg" "NewGuide_hyperLayout24.hyp[950].dn";
connectAttr "L_FrFoot_In_Guide_CtrlShape.msg" "NewGuide_hyperLayout24.hyp[951].dn"
		;
connectAttr "L_FrFoot_In_Guide_Ctrl_CtrlShape.msg" "NewGuide_hyperLayout24.hyp[952].dn"
		;
connectAttr "L_FrFoot_In_Guide_Ctrl_Ctrl_CtrlShape.msg" "NewGuide_hyperLayout24.hyp[953].dn"
		;
connectAttr "L_FrFoot_In_Guide_Ctrl_Ctrl_Ctrl_CtrlShape.msg" "NewGuide_hyperLayout24.hyp[954].dn"
		;
connectAttr "L_FrFoot_Out_Guide.msg" "NewGuide_hyperLayout24.hyp[955].dn";
connectAttr "L_FrFoot_Out_Guide_CtrlShape.msg" "NewGuide_hyperLayout24.hyp[956].dn"
		;
connectAttr "L_FrFoot_Out_Guide_Ctrl_CtrlShape.msg" "NewGuide_hyperLayout24.hyp[957].dn"
		;
connectAttr "L_FrFoot_Out_Guide_Ctrl_Ctrl_CtrlShape.msg" "NewGuide_hyperLayout24.hyp[958].dn"
		;
connectAttr "L_FrFoot_Out_Guide_Ctrl_Ctrl_Ctrl_CtrlShape.msg" "NewGuide_hyperLayout24.hyp[959].dn"
		;
connectAttr "Neck_Guide.msg" "hyperLayout68.hyp[0].dn";
connectAttr "Neck_GuideShape.msg" "hyperLayout68.hyp[1].dn";
connectAttr "Head_Loc.msg" "hyperLayout69.hyp[0].dn";
connectAttr "Head_LocShape.msg" "hyperLayout69.hyp[1].dn";
connectAttr "L_Eyes_Guide.msg" "hyperLayout36.hyp[220].dn";
connectAttr "L_Eyes_Guide_CtrlShape.msg" "hyperLayout36.hyp[221].dn";
connectAttr "L_Eyes_Guide_Ctrl_CtrlShape.msg" "hyperLayout36.hyp[222].dn";
connectAttr "L_Eyes_Guide_Ctrl_Ctrl_CtrlShape.msg" "hyperLayout36.hyp[223].dn";
connectAttr "L_Eyes_Guide_Ctrl_Ctrl_Ctrl_CtrlShape.msg" "hyperLayout36.hyp[224].dn"
		;
connectAttr "L_Eyes_Aim_Guide.msg" "hyperLayout36.hyp[225].dn";
connectAttr "L_Eyes_Aim_Guide_CtrlShape.msg" "hyperLayout36.hyp[226].dn";
connectAttr "L_Eyes_Aim_Guide_Ctrl_CtrlShape.msg" "hyperLayout36.hyp[227].dn";
connectAttr "L_Eyes_Aim_Guide_Ctrl_Ctrl_CtrlShape.msg" "hyperLayout36.hyp[228].dn"
		;
connectAttr "L_Eyes_Aim_Guide_Ctrl_Ctrl_Ctrl_CtrlShape.msg" "hyperLayout36.hyp[229].dn"
		;
connectAttr "Tail_Guide.msg" "hyperLayout71.hyp[0].dn";
connectAttr "Tail_GuideShape.msg" "hyperLayout71.hyp[1].dn";
connectAttr "Code_Loc.msg" "hyperLayout26.hyp[18].dn";
connectAttr "Code_LocShape.msg" "hyperLayout26.hyp[19].dn";
connectAttr "Neck_GuideShape.iog" ":initialShadingGroup.dsm" -na;
connectAttr "Tail_GuideShape.iog" ":initialShadingGroup.dsm" -na;
dataStructure -fmt "raw" -as "name=mapManager_groundWoods_c_geo1:string=value";
dataStructure -fmt "raw" -as "name=notes_slopesGroundGrassA_Combined:string=value";
dataStructure -fmt "raw" -as "name=mapManager_pPlane6:string=value";
dataStructure -fmt "raw" -as "name=notes_mountains_parShape:string=value";
dataStructure -fmt "raw" -as "name=notes_slopesGroundGrassD_Combined:string=value";
dataStructure -fmt "raw" -as "name=mapManager_ground:string=value";
dataStructure -fmt "raw" -as "name=notes_decayLeaves_parShape:string=value";
dataStructure -fmt "raw" -as "name=mapManager_grassBase:string=value";
dataStructure -fmt "raw" -as "name=notes_wildPatchF_parShape:string=value";
dataStructure -fmt "raw" -as "name=mapManager_baseLeaves:string=value";
dataStructure -fmt "raw" -as "name=notes_snapshot_Combined:string=value";
dataStructure -fmt "raw" -as "name=mapManager_juneBackYard:string=value";
dataStructure -fmt "raw" -as "name=mapManager_slopesGroundGrassD_Combined:string=value";
dataStructure -fmt "raw" -as "name=notes_decayLeavesCarousel_parShape:string=value";
dataStructure -fmt "raw" -as "name=mapManager_trees_left:string=value";
dataStructure -fmt "raw" -as "name=mapManager_pPlane3:string=value";
dataStructure -fmt "raw" -as "name=mapManager_pPlane2:string=value";
dataStructure -fmt "raw" -as "name=notes_pPlane4:string=value";
dataStructure -fmt "raw" -as "name=notes_decayGrassesCenter_parShape:string=value";
dataStructure -fmt "raw" -as "name=notes_wildPatchDegraded_parShape:string=value";
dataStructure -fmt "raw" -as "name=mapManager_polySurface56:string=value";
dataStructure -fmt "raw" -as "name=notes_ferns_parShape:string=value";
dataStructure -fmt "raw" -as "name=notes_pPlane6:string=value";
dataStructure -fmt "raw" -as "name=notes_wildPatchA_parShape:string=value";
dataStructure -fmt "raw" -as "name=mapManager_trees_left1:string=value";
dataStructure -fmt "raw" -as "name=Curvature:float=mean:float=gaussian:float=ABS:float=RMS";
dataStructure -fmt "raw" -as "name=notes_groundC_parShape:string=value";
dataStructure -fmt "raw" -as "name=notes_left_parShape:string=value";
dataStructure -fmt "raw" -as "name=notes_wildPatchH_parShape:string=value";
dataStructure -fmt "raw" -as "name=notes_slopesGroundGrassB_Combined:string=value";
dataStructure -fmt "raw" -as "name=OffStruct:float=Offset";
dataStructure -fmt "raw" -as "name=notes_groundD_parShape:string=value";
dataStructure -fmt "raw" -as "name=faceConnectOutputStructure:bool=faceConnectOutput:string[200]=faceConnectOutputAttributes:string[200]=faceConnectOutputGroups";
dataStructure -fmt "raw" -as "name=mapManager_slopesMountainsGrass_Combined:string=value";
dataStructure -fmt "raw" -as "name=mapManager_snapshot_floor:string=value";
dataStructure -fmt "raw" -as "name=mapManager_slopesGroundGrassC_Combined:string=value";
dataStructure -fmt "raw" -as "name=mapManager_base_right:string=value";
dataStructure -fmt "raw" -as "name=mapManager_snapshot_CombinedGrass:string=value";
dataStructure -fmt "raw" -as "name=mapManager_suelo:string=value";
dataStructure -fmt "raw" -as "name=mapManager_slopesGroundGrassA_Combined:string=value";
dataStructure -fmt "raw" -as "name=notes_slopesGroundGrassC_Combined:string=value";
dataStructure -fmt "raw" -as "name=mapManager_grass_c_geo1:string=value";
dataStructure -fmt "raw" -as "name=notes_trees_left1:string=value";
dataStructure -fmt "raw" -as "name=notes_pPlane3:string=value";
dataStructure -fmt "raw" -as "name=idStructure:int32=ID";
dataStructure -fmt "raw" -as "name=NameAndID:string=name:int32=ID";
dataStructure -fmt "raw" -as "name=notes_groundWoods_c_geo1:string=value";
dataStructure -fmt "raw" -as "name=mapManager_degraded:string=value";
dataStructure -fmt "raw" -as "name=notes_grassJuneBackYard_parShape:string=value";
dataStructure -fmt "raw" -as "name=notes_groundA_parShape:string=value";
dataStructure -fmt "raw" -as "name=mapManager_base_left:string=value";
dataStructure -fmt "raw" -as "name=Blur3dMetaData:string=Blur3dValue";
dataStructure -fmt "raw" -as "name=DiffArea:float=value";
dataStructure -fmt "raw" -as "name=notes_grass_c_geo1:string=value";
dataStructure -fmt "raw" -as "name=mapManager_snapshot_Combined:string=value";
dataStructure -fmt "raw" -as "name=mapManager_pPlane4:string=value";
dataStructure -fmt "raw" -as "name=notes_baseLeaves:string=value";
dataStructure -fmt "raw" -as "name=mapManager_floorOrangeConcrete_c_geo:string=value";
dataStructure -fmt "raw" -as "name=notes_decayGrassPatchC_parShape:string=value";
dataStructure -fmt "raw" -as "name=notes_baseScatt:string=value";
dataStructure -fmt "raw" -as "name=notes_slopes_parShape:string=value";
dataStructure -fmt "raw" -as "name=mapManager_pPlane1:string=value";
dataStructure -fmt "raw" -as "name=Offset:float[3]=value";
dataStructure -fmt "raw" -as "name=notes_snapshot_CombinedGrass:string=value";
dataStructure -fmt "raw" -as "name=IdStruct:int32=ID";
dataStructure -fmt "raw" -as "name=notes_wildPatchG_parShape:string=value";
dataStructure -fmt "raw" -as "name=mapManager_grass_c_geo:string=value";
dataStructure -fmt "raw" -as "name=notes_pPlane2:string=value";
dataStructure -fmt "raw" -as "name=notes_ground_c_geo:string=value";
dataStructure -fmt "raw" -as "name=notes_juneBackYard:string=value";
dataStructure -fmt "raw" -as "name=notes_decayGrassPatchD_parShape:string=value";
dataStructure -fmt "raw" -as "name=notes_widlPatchB_parShape:string=value";
dataStructure -fmt "raw" -as "name=notes_pPlane5:string=value";
dataStructure -fmt "raw" -as "name=mapManager_slopesGroundGrassB_Combined:string=value";
dataStructure -fmt "raw" -as "name=faceConnectMarkerStructure:bool=faceConnectMarker:string[200]=faceConnectOutputGroups";
dataStructure -fmt "raw" -as "name=notes_wildPatchE_parShape:string=value";
dataStructure -fmt "raw" -as "name=mapManager_pPlane5:string=value";
dataStructure -fmt "raw" -as "name=notes_base_hojas:string=value";
dataStructure -fmt "raw" -as "name=notes_degraded:string=value";
dataStructure -fmt "raw" -as "name=notes_ground:string=value";
dataStructure -fmt "raw" -as "name=mapManager_base_hojas:string=value";
dataStructure -fmt "raw" -as "name=notes_snapshot_floor:string=value";
dataStructure -fmt "raw" -as "name=mapManager_baseScatt:string=value";
dataStructure -fmt "raw" -as "name=notes_wildPatchC_parShape:string=value";
dataStructure -fmt "raw" -as "name=notes_trees_parShape:string=value";
dataStructure -fmt "raw" -as "name=mapManager_ground_c_geo:string=value";
dataStructure -fmt "raw" -as "name=notes_decayGrassPatchA_parShape:string=value";
dataStructure -fmt "raw" -as "name=notes_polySurface56:string=value";
dataStructure -fmt "raw" -as "name=notes_pPlane1:string=value";
dataStructure -fmt "raw" -as "name=notes_base_right:string=value";
dataStructure -fmt "raw" -as "name=notes_grassBase:string=value";
dataStructure -fmt "raw" -as "name=notes_baseScatter:string=value";
dataStructure -fmt "raw" -as "name=notes_bushes_parShape:string=value";
dataStructure -fmt "raw" -as "name=notes_slopesMountainsGrass_Combined:string=value";
dataStructure -fmt "raw" -as "name=notes_base_left:string=value";
dataStructure -fmt "raw" -as "name=notes_trees_left:string=value";
dataStructure -fmt "raw" -as "name=notes_decayGrassPatchB_parShape:string=value";
dataStructure -fmt "raw" -as "name=notes_wildPatchD_parShape:string=value";
dataStructure -fmt "raw" -as "name=notes_grass_c_geo:string=value";
dataStructure -fmt "raw" -as "name=mapManager_baseScatter:string=value";
dataStructure -fmt "raw" -as "name=keyValueStructure:string=value";
dataStructure -fmt "raw" -as "name=notes_floorOrangeConcrete_c_geo:string=value";
dataStructure -fmt "raw" -as "name=DiffEdge:float=value";
dataStructure -fmt "raw" -as "name=notes_suelo:string=value";
dataStructure -fmt "raw" -as "name=OrgStruct:float[3]=Origin Point";
dataStructure -fmt "raw" -as "name=notes_groundB_parShape:string=value";
dataStructure -fmt "raw" -as "name=notes_right_parShape:string=value";
// End of TortoiseTemplate.ma
