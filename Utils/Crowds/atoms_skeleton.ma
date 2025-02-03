//Maya ASCII 2022 scene
//Name: atoms_skeleton.ma
//Last modified: Mon, Nov 07, 2022 04:36:13 PM
//Codeset: 1252
requires maya "2022";
requires "stereoCamera" "10.0";
requires "stereoCamera" "10.0";
currentUnit -l centimeter -a degree -t film;
fileInfo "application" "maya";
fileInfo "product" "Maya 2022";
fileInfo "version" "2022";
fileInfo "cutIdentifier" "202205171752-c25c06f306";
fileInfo "osv" "Windows 10 Home v2009 (Build: 22621)";
fileInfo "UUID" "F6DFA2B3-4DD1-A457-5E2F-BFB8CC435DD9";
createNode transform -s -n "persp";
	rename -uid "802F3EB9-4571-C181-64E3-54A70CD28AB9";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 38.742365800046876 137.4708643394703 195.85123664029342 ;
	setAttr ".r" -type "double3" -11.138352729603467 10.200000000000292 4.0395357585802664e-16 ;
createNode camera -s -n "perspShape" -p "persp";
	rename -uid "27A4C473-43DF-5C2C-A5DD-6D9398F2DA82";
	setAttr -k off ".v" no;
	setAttr ".fl" 34.999999999999993;
	setAttr ".coi" 250.80576144305087;
	setAttr ".imn" -type "string" "persp";
	setAttr ".den" -type "string" "persp_depth";
	setAttr ".man" -type "string" "persp_mask";
	setAttr ".hc" -type "string" "viewSet -p %camera";
createNode transform -s -n "top";
	rename -uid "A7E68D65-475A-1CD5-B84B-828DCEB82F75";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 0 1000.1 0 ;
	setAttr ".r" -type "double3" -90 0 0 ;
createNode camera -s -n "topShape" -p "top";
	rename -uid "4FC81D26-4F24-5F56-AAAE-C7AD8D58D94E";
	setAttr -k off ".v" no;
	setAttr ".rnd" no;
	setAttr ".coi" 1000.1;
	setAttr ".ow" 30;
	setAttr ".imn" -type "string" "top";
	setAttr ".den" -type "string" "top_depth";
	setAttr ".man" -type "string" "top_mask";
	setAttr ".hc" -type "string" "viewSet -t %camera";
	setAttr ".o" yes;
createNode transform -s -n "front";
	rename -uid "243781F7-4904-E3BA-CFA7-D183C2E21034";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 0 0 1000.1 ;
createNode camera -s -n "frontShape" -p "front";
	rename -uid "B3CE32D1-4602-A35A-8BFC-1C9451C86723";
	setAttr -k off ".v" no;
	setAttr ".rnd" no;
	setAttr ".coi" 1000.1;
	setAttr ".ow" 30;
	setAttr ".imn" -type "string" "front";
	setAttr ".den" -type "string" "front_depth";
	setAttr ".man" -type "string" "front_mask";
	setAttr ".hc" -type "string" "viewSet -f %camera";
	setAttr ".o" yes;
createNode transform -s -n "side";
	rename -uid "7282E603-459D-AB1B-D9CA-11A772A99C7A";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 1000.1 0 0 ;
	setAttr ".r" -type "double3" 0 90 0 ;
createNode camera -s -n "sideShape" -p "side";
	rename -uid "58762371-4D75-08C2-17FF-E993FCFBF9B6";
	setAttr -k off ".v" no;
	setAttr ".rnd" no;
	setAttr ".coi" 1000.1;
	setAttr ".ow" 30;
	setAttr ".imn" -type "string" "side";
	setAttr ".den" -type "string" "side_depth";
	setAttr ".man" -type "string" "side_mask";
	setAttr ".hc" -type "string" "viewSet -s %camera";
	setAttr ".o" yes;
createNode joint -n "Hips_Skl";
	rename -uid "1F5D7D6B-4716-D9A3-C944-77B8ECB33656";
	addAttr -ci true -h true -sn "fbxID" -ln "filmboxTypeID" -at "short";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0 101.52418518066406 0 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1;
	setAttr ".radi" 2;
	setAttr ".fbxID" 5;
createNode joint -n "LeftUpLeg_Skl" -p "Hips_Skl";
	rename -uid "5E5D547F-4831-11D1-B1C5-BF9D8427B391";
	addAttr -is true -ci true -k true -sn "atoms_poleVector" -ln "atoms_poleVector" 
		-at "double3" -nc 3;
	addAttr -is true -ci true -sn "atoms_poleVector0" -ln "atoms_poleVector0" -at "double" 
		-p "atoms_poleVector";
	addAttr -is true -ci true -sn "atoms_poleVector1" -ln "atoms_poleVector1" -at "double" 
		-p "atoms_poleVector";
	addAttr -is true -ci true -sn "atoms_poleVector2" -ln "atoms_poleVector2" -at "double" 
		-p "atoms_poleVector";
	addAttr -ci true -h true -sn "fbxID" -ln "filmboxTypeID" -at "short";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 7.4505167007446289 -7.7403593063354492 1.5381205081939697 ;
	setAttr ".r" -type "double3" 3.7161762674835631e-16 0 2.458345708049626e-17 ;
	setAttr ".jo" -type "double3" 1.9900564001699187e-16 -2.7003134116908614 -86 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.069679000000000005 -0.99645600000000001 0.047111899999999998 0
		 0.99756400000000001 0.069756499999999999 0 0 -0.0032863599999999999 0.046997200000000003 0.99888999999999994 0
		 7.4505169999999996 -7.7403589999999998 1.5381210000000001 1;
	setAttr ".radi" 3;
	setAttr -k on ".atoms_poleVector" -type "double3" 10.295197723822556 -7.7403593063354492 
		23.603414965967094 ;
	setAttr ".fbxID" 5;
createNode joint -n "LeftLeg_Skl" -p "LeftUpLeg_Skl";
	rename -uid "49066210-4EBB-CF09-A22E-8A92903BAB1A";
	addAttr -ci true -h true -sn "fbxID" -ln "filmboxTypeID" -at "short";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 40.825504302978516 -3.5527136788005009e-15 -2.6645352591003757e-15 ;
	setAttr ".r" -type "double3" 0 -7.9513867964737758e-16 0 ;
	setAttr ".jo" -type "double3" 0 5.2989999999999977 0 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.069684700000000002 -0.99653800000000003 -0.045340100000000001 0
		 0.99756400000000001 0.069756499999999999 0 0 0.0031627600000000001 -0.045229600000000002 0.99897199999999997 0
		 10.295197999999999 -48.421193000000002 3.4614880000000001 1;
	setAttr ".radi" 3;
	setAttr ".fbxID" 5;
createNode joint -n "LeftFoot_Skl" -p "LeftLeg_Skl";
	rename -uid "DC477B4A-4629-B613-78D6-319FD13846D3";
	addAttr -is true -ci true -k true -sn "atoms_ikMaxIterations" -ln "atoms_ikMaxIterations" 
		-smn 0 -smx 0 -at "long";
	addAttr -is true -ci true -k true -sn "atoms_ikSoftDistance" -ln "atoms_ikSoftDistance" 
		-smn 0 -smx 0 -at "double";
	addAttr -is true -ci true -k true -sn "atoms_ikSolver" -ln "atoms_ikSolver" -smn 
		0 -smx 0 -at "long";
	addAttr -is true -ci true -k true -sn "atoms_ikTollerance" -ln "atoms_ikTollerance" 
		-smn 0 -smx 0 -at "double";
	addAttr -ci true -h true -sn "fbxID" -ln "filmboxTypeID" -at "short";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 46.434268951416016 -3.5527136788005009e-15 7.7715611723760958e-16 ;
	setAttr ".r" -type "double3" 1.8884542384310686e-15 1.9083328735053535e-14 9.9392338926389137e-16 ;
	setAttr ".jo" -type "double3" -4.4163831504686577 -67.475285727358724 1.5902773407317584e-15 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.0296165 -0.42353499999999999 0.90539499999999995 0
		 0.99946500000000005 0 -0.032693600000000003 0 0.013846900000000001 0.90588000000000002 0.42330899999999999 0
		 13.530958 -94.694714000000005 1.3561540000000001 1;
	setAttr ".radi" 3;
	setAttr -k on ".atoms_ikSoftDistance" 0.05;
	setAttr -k on ".atoms_ikTollerance" 0.001;
	setAttr ".fbxID" 5;
createNode joint -n "LeftToeBase_Skl" -p "LeftFoot_Skl";
	rename -uid "71FE6241-43CD-B52B-1156-05A851967487";
	addAttr -ci true -h true -sn "fbxID" -ln "filmboxTypeID" -at "short";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 16.124929428100586 0 0 ;
	setAttr ".r" -type "double3" -1.9878466991184439e-16 6.3611094371790206e-15 9.9392334955922197e-17 ;
	setAttr ".jo" -type "double3" 0.77538331645781999 -22.45417856614052 9.9392333795734899e-17 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.032659800000000003 -0.0454291 0.99843400000000004 0
		 0.999394 0.0135186 -0.032076100000000003 0 -0.012040199999999999 0.99887599999999999 0.045843099999999998 0
		 14.008521 -101.524187 15.955591999999999 1;
	setAttr ".radi" 3;
	setAttr ".fbxID" 5;
createNode joint -n "LeftToeEnd_Skl" -p "LeftToeBase_Skl";
	rename -uid "1D0DD8BE-4439-B93E-2B92-CA9E41C0A12E";
	addAttr -ci true -h true -sn "fbxID" -ln "filmboxTypeID" -at "short";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 5.885584831237793 0 2.2204460492503131e-15 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.032659800000000003 -0.0454291 0.99843400000000004 0
		 0.999394 0.0135186 -0.032076100000000003 0 -0.012040199999999999 0.99887599999999999 0.045843099999999998 0
		 14.200742999999999 -101.791563 21.831958 1;
	setAttr ".radi" 3;
	setAttr ".fbxID" 5;
createNode joint -n "Spine_Skl" -p "Hips_Skl";
	rename -uid "2753F3BC-44B4-3980-25A3-3386A5C97AAF";
	addAttr -ci true -h true -sn "fbxID" -ln "filmboxTypeID" -at "short";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0 8.181279182434082 0.47847628593444824 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 8.181279 0.47847600000000001 1;
	setAttr ".radi" 3;
	setAttr ".fbxID" 5;
createNode joint -n "Spine1_Skl" -p "Spine_Skl";
	rename -uid "A77F5570-4949-D415-01BD-4FAFECC9E2B5";
	addAttr -ci true -h true -sn "fbxID" -ln "filmboxTypeID" -at "short";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0 20.212757110595703 -4.5429515838623047 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 28.394036 -4.0644749999999998 1;
	setAttr ".radi" 3;
	setAttr ".fbxID" 5;
createNode joint -n "Spine2_Skl" -p "Spine1_Skl";
	rename -uid "92EF1CDD-4B13-5D36-5A6C-E68865D7FD63";
	addAttr -ci true -h true -sn "fbxID" -ln "filmboxTypeID" -at "short";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0 14.036942481994629 -4.6122117042541504 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 42.430979000000001 -8.6766869999999994 1;
	setAttr ".radi" 3;
	setAttr ".fbxID" 5;
createNode joint -n "LeftShoulder_Skl" -p "Spine2_Skl";
	rename -uid "AB032DEA-42A3-E13C-6D3B-998AAA5DA919";
	addAttr -ci true -h true -sn "fbxID" -ln "filmboxTypeID" -at "short";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 4.4481034278869629 2.2392442226409912 13.301911354064941 ;
	setAttr ".r" -type "double3" -3.9756933982368879e-16 0 0 ;
	setAttr ".jo" -type "double3" 2.2250000000000005 0 0 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 0.99924599999999997 0.038823799999999999 0
		 0 -0.038823799999999999 0.99924599999999997 0 4.4481029999999997 44.670223 4.6252240000000002 1;
	setAttr ".radi" 3;
	setAttr ".fbxID" 5;
createNode joint -n "LeftArm_Skl" -p "LeftShoulder_Skl";
	rename -uid "90830B22-4CC6-7F6A-C118-9F965301F1C6";
	addAttr -ci true -h true -sn "fbxID" -ln "filmboxTypeID" -at "short";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 16.164669036865234 -0.47509044408798218 -8.302577018737793 ;
	setAttr ".jo" -type "double3" 0 4.1 0 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.99744100000000002 0.0027758000000000001 -0.071443499999999993 0
		 0 0.99924599999999997 0.038823799999999999 0 0.071497400000000003 -0.038724500000000002 0.99668900000000005 0
		 20.612772 44.517828000000002 -3.6895380000000002 1;
	setAttr ".radi" 3;
	setAttr ".fbxID" 5;
createNode joint -n "LeftArm_Roll_Skl" -p "LeftArm_Skl";
	rename -uid "F853D15E-4402-D4B1-16FD-81B07E7D5B61";
	addAttr -is true -ci true -k true -sn "atoms_skipIk" -ln "atoms_skipIk" -min 0 
		-max 1 -at "bool";
	addAttr -ci true -h true -sn "fbxID" -ln "filmboxTypeID" -at "short";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 12.737104415893555 -8.5265128291212022e-14 -2.042810365310288e-14 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.99744100000000002 0.0027758000000000001 -0.071443499999999993 0
		 0 0.99924599999999997 0.038823799999999999 0 0.071497400000000003 -0.038724500000000002 0.99668900000000005 0
		 33.317279999999997 44.553184000000002 -4.5995220000000003 1;
	setAttr ".radi" 3;
	setAttr ".fbxID" 5;
createNode joint -n "LeftForeArm_Skl" -p "LeftArm_Roll_Skl";
	rename -uid "70BB07FA-41C4-9AE8-BA43-EBB998F15040";
	addAttr -ci true -h true -sn "fbxID" -ln "filmboxTypeID" -at "short";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 11.069648742675781 -4.1894286368915346e-06 3.5511175155988894e-07 ;
	setAttr ".jo" -type "double3" 0 -12.090139543516054 0 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.99029199999999995 -0.0053966099999999996 0.13889799999999999 0
		 0 0.99924599999999997 0.038823799999999999 0 -0.13900299999999999 -0.038446899999999999 0.98954500000000001 0
		 44.358598999999998 44.583907000000004 -5.3903759999999998 1;
	setAttr ".radi" 3;
	setAttr ".fbxID" 5;
createNode joint -n "LeftForeArm_Roll_Skl" -p "LeftForeArm_Skl";
	rename -uid "A328C201-4A06-DB49-D2BA-849F83A3D66C";
	addAttr -is true -ci true -k true -sn "atoms_skipIk" -ln "atoms_skipIk" -min 0 
		-max 1 -at "bool";
	addAttr -ci true -h true -sn "fbxID" -ln "filmboxTypeID" -at "short";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 10.701000213623047 2.8421709430404007e-14 2.8421709430404007e-14 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.99029199999999995 -0.0053966099999999996 0.13889799999999999 0
		 0 0.99924599999999997 0.038823799999999999 0 -0.13900299999999999 -0.038446899999999999 0.98954500000000001 0
		 54.955714 44.526158000000002 -3.9040300000000001 1;
	setAttr ".radi" 3;
	setAttr ".fbxID" 5;
createNode joint -n "LeftHand_Skl" -p "LeftForeArm_Roll_Skl";
	rename -uid "B7DFC03C-46A4-1580-9BFA-1AB88933C413";
	addAttr -ci true -h true -sn "fbxID" -ln "filmboxTypeID" -at "short";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 14.426703453063965 5.8903140143229393e-09 -4.2672873235005682e-08 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.99029199999999995 -0.0053966099999999996 0.13889799999999999 0
		 0 0.99924599999999997 0.038823799999999999 0 -0.13900299999999999 -0.038446899999999999 0.98954500000000001 0
		 69.242362999999997 44.448303000000003 -1.9001920000000001 1;
	setAttr ".radi" 3;
	setAttr ".fbxID" 5;
createNode joint -n "LeftHandThumb1_Skl" -p "LeftHand_Skl";
	rename -uid "8742522A-49BB-2EAD-8132-F8A2836E4BCA";
	addAttr -ci true -h true -sn "fbxID" -ln "filmboxTypeID" -at "short";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 4.6116981506347656 -2.5265908241271973 4.2127165794372559 ;
	setAttr ".r" -type "double3" 0 0 -0.27818546350544227 ;
	setAttr ".jo" -type "double3" 20.952000000000009 -35.997000974577524 -32.740046608315602 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.59221199999999996 -0.46349499999999999 0.65913299999999997 0
		 0.28488799999999997 0.88561000000000001 0.366788 0 -0.75373900000000005 -0.029437000000000001 0.65651400000000004 0
		 73.223712000000006 41.736763000000003 2.8109459999999999 1;
	setAttr ".radi" 3;
	setAttr ".fbxID" 5;
createNode joint -n "LeftHandThumb2_Skl" -p "LeftHandThumb1_Skl";
	rename -uid "ABF0C649-4484-2A82-AE26-1A9D84BB5A04";
	addAttr -ci true -h true -sn "fbxID" -ln "filmboxTypeID" -at "short";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 2.5021369457244873 0 -4.9737991503207013e-14 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.59221199999999996 -0.46349499999999999 0.65913299999999997 0
		 0.28488799999999997 0.88561000000000001 0.366788 0 -0.75373900000000005 -0.029437000000000001 0.65651400000000004 0
		 74.705509000000006 40.577033999999998 4.4601870000000003 1;
	setAttr ".radi" 3;
	setAttr ".fbxID" 5;
createNode joint -n "LeftHandThumb3_Skl" -p "LeftHandThumb2_Skl";
	rename -uid "E1E5AB6C-4171-C970-B8FE-8B933C097393";
	addAttr -ci true -h true -sn "fbxID" -ln "filmboxTypeID" -at "short";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 2.4192807674407959 8.5265128291212022e-14 2.8421709430404007e-14 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.59221199999999996 -0.46349499999999999 0.65913299999999997 0
		 0.28488799999999997 0.88561000000000001 0.366788 0 -0.75373900000000005 -0.029437000000000001 0.65651400000000004 0
		 76.138237000000004 39.455708000000001 6.0548149999999996 1;
	setAttr ".radi" 3;
	setAttr ".fbxID" 5;
createNode joint -n "LeftHandThumb4_Skl" -p "LeftHandThumb3_Skl";
	rename -uid "23910D0D-48AF-75D6-05B7-21B914A06E5A";
	addAttr -ci true -h true -sn "fbxID" -ln "filmboxTypeID" -at "short";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 3.5764837265014648 6.6476691245043185e-06 3.5309903978486545e-06 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.59221199999999996 -0.46349499999999999 0.65913299999999997 0
		 0.28488799999999997 0.88561000000000001 0.366788 0 -0.75373900000000005 -0.029437000000000001 0.65651400000000004 0
		 78.256274000000005 37.798029999999997 8.4121980000000001 1;
	setAttr ".radi" 3;
	setAttr ".fbxID" 5;
createNode joint -n "LeftHandIndex1_Skl" -p "LeftHand_Skl";
	rename -uid "0E784675-4D7A-4B64-B265-59901A5A6FC1";
	addAttr -ci true -h true -sn "fbxID" -ln "filmboxTypeID" -at "short";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 10.43731689453125 0.75890904664993286 1.8558968305587769 ;
	setAttr ".r" -type "double3" -1.2722218874358041e-14 -1.4908850309562779e-15 1.5902773592947552e-15 ;
	setAttr ".jo" -type "double3" -92.624894812505886 -10.07108671404985 2.9034501782211448 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.94947400000000004 0.037805100000000001 0.31156 0
		 0.31178299999999998 -1.2614399999999999e-06 -0.95015300000000003 0 -0.035920300000000002 0.99928499999999998 -0.0117882 0
		 79.32038 45.078960000000002 1.4154869999999999 1;
	setAttr ".radi" 3;
	setAttr ".fbxID" 5;
createNode joint -n "LeftHandIndex2_Skl" -p "LeftHandIndex1_Skl";
	rename -uid "86E397DA-4536-14C2-7FA8-F3830A6D875B";
	addAttr -ci true -h true -sn "fbxID" -ln "filmboxTypeID" -at "short";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 4.1108813285827637 7.1054273576010019e-15 -2.8421709430404007e-14 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.94947400000000004 0.037805100000000001 0.31156 0
		 0.31178299999999998 -1.2614399999999999e-06 -0.95015300000000003 0 -0.035920300000000002 0.99928499999999998 -0.0117882 0
		 83.223555000000005 45.234372 2.6962739999999998 1;
	setAttr ".radi" 3;
	setAttr ".fbxID" 5;
createNode joint -n "LeftHandIndex3_Skl" -p "LeftHandIndex2_Skl";
	rename -uid "34398E70-4D1C-84DA-A84E-268E650844D9";
	addAttr -ci true -h true -sn "fbxID" -ln "filmboxTypeID" -at "short";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 3.2182943820953369 8.8188826907753537e-08 6.8323693085403647e-06 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.94947400000000004 0.037805100000000001 0.31156 0
		 0.31178299999999998 -1.2614399999999999e-06 -0.95015300000000003 0 -0.035920300000000002 0.99928499999999998 -0.0117882 0
		 86.279241999999996 45.356046999999997 3.698966 1;
	setAttr ".radi" 3;
	setAttr ".fbxID" 5;
createNode joint -n "LeftHandIndex4_Skl" -p "LeftHandIndex3_Skl";
	rename -uid "900BE91A-4F5C-C834-8BA1-1BB1C4A7D2A9";
	addAttr -ci true -h true -sn "fbxID" -ln "filmboxTypeID" -at "short";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 1.4270132780075073 -2.6926846885544364e-07 7.2289249146706425e-06 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.94947400000000004 0.037805100000000001 0.31156 0
		 0.31178299999999998 -1.2614399999999999e-06 -0.95015300000000003 0 -0.035920300000000002 0.99928499999999998 -0.0117882 0
		 87.634153999999995 45.410003000000003 4.1435659999999999 1;
	setAttr ".radi" 3;
	setAttr ".fbxID" 5;
createNode joint -n "LeftHandMiddle1_Skl" -p "LeftHand_Skl";
	rename -uid "50EAAEB4-4909-845A-D16B-639827499B18";
	addAttr -ci true -h true -sn "fbxID" -ln "filmboxTypeID" -at "short";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 10.311123847961426 0.79898828268051147 -0.198475182056427 ;
	setAttr ".r" -type "double3" 0 -2.9817701148521149e-16 0 ;
	setAttr ".jo" -type "double3" -91.889508154414457 8.6630230386531206 2.2369809117385699 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.99918499999999999 0.039018400000000002 -0.010341400000000001 0
		 -0.010349300000000001 -1.32754e-06 -0.999946 0 -0.039016299999999997 0.99923799999999996 0.00040248500000000001 0
		 79.480975000000001 45.198673999999997 -0.63337900000000003 1;
	setAttr ".radi" 3;
	setAttr ".fbxID" 5;
createNode joint -n "LeftHandMiddle2_Skl" -p "LeftHandMiddle1_Skl";
	rename -uid "F81DA56D-4ECB-727B-B948-7E94CA1D5995";
	addAttr -ci true -h true -sn "fbxID" -ln "filmboxTypeID" -at "short";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 5.1370525360107422 -2.7200464103316335e-15 5.6843418860808015e-14 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.99918499999999999 0.039018400000000002 -0.010341400000000001 0
		 -0.010349300000000001 -1.32754e-06 -0.999946 0 -0.039016299999999997 0.99923799999999996 0.00040248500000000001 0
		 84.613840999999994 45.399113 -0.686504 1;
	setAttr ".radi" 3;
	setAttr ".fbxID" 5;
createNode joint -n "LeftHandMiddle3_Skl" -p "LeftHandMiddle2_Skl";
	rename -uid "3D1EB608-47FE-3178-6053-D6A6ED8CFB0B";
	addAttr -ci true -h true -sn "fbxID" -ln "filmboxTypeID" -at "short";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 3.0790479183197021 7.3435231229268538e-08 8.2634360296651721e-06 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.99918499999999999 0.039018400000000002 -0.010341400000000001 0
		 -0.010349300000000001 -1.32754e-06 -0.999946 0 -0.039016299999999997 0.99923799999999996 0.00040248500000000001 0
		 87.690378999999993 45.519261 -0.71834500000000001 1;
	setAttr ".radi" 3;
	setAttr ".fbxID" 5;
createNode joint -n "LeftHandMiddle4_Skl" -p "LeftHandMiddle3_Skl";
	rename -uid "C4AA951F-4630-39FE-FF7A-6EB26560C9D9";
	addAttr -ci true -h true -sn "fbxID" -ln "filmboxTypeID" -at "short";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 1.2405053377151489 -1.6861086749031529e-08 -1.6242124729615171e-06 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.99918499999999999 0.039018400000000002 -0.010341400000000001 0
		 -0.010349300000000001 -1.32754e-06 -0.999946 0 -0.039016299999999997 0.99923799999999996 0.00040248500000000001 0
		 88.929873000000001 45.567661999999999 -0.73117399999999999 1;
	setAttr ".radi" 3;
	setAttr ".fbxID" 5;
createNode joint -n "LeftHandRing1_Skl" -p "LeftHand_Skl";
	rename -uid "941602D3-49AA-9698-D13F-B7AEEF5887F3";
	addAttr -ci true -h true -sn "fbxID" -ln "filmboxTypeID" -at "short";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 10.027972221374512 0.71468943357467651 -2.4364504814147949 ;
	setAttr ".r" -type "double3" -1.2324649561004132e-14 1.6896696876332325e-15 3.1805547185895103e-15 ;
	setAttr ".jo" -type "double3" -91.112316126121669 26.749437857137593 2.2133837172985733 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.946218 0.046951199999999998 -0.320104 0 -0.32045800000000002 -1.2576e-06 -0.94726299999999997 0
		 -0.044475500000000001 0.99889700000000003 0.015044699999999999 0 79.511657 45.202010000000001 -2.8905590000000001 1;
	setAttr ".radi" 3;
	setAttr ".fbxID" 5;
createNode joint -n "LeftHandRing2_Skl" -p "LeftHandRing1_Skl";
	rename -uid "BA9B03D6-4578-F78D-E8CB-DFB6DC9B47D1";
	addAttr -ci true -h true -sn "fbxID" -ln "filmboxTypeID" -at "short";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 4.2291297912597656 -0.0035663763992488384 -0.007434304803609848 ;
	setAttr ".r" -type "double3" -6.2120209347451373e-18 -3.9756933982368879e-16 -1.0773973877199492e-16 ;
	setAttr ".jo" -type "double3" -0.033546838367436889 1.488747215989104 -0.71435944667219287 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.95097500000000001 0.0209797 -0.308556 0 -0.30862400000000001 -1.2628e-06 -0.95118400000000003 0
		 -0.019956000000000002 0.99978 0.0064736500000000001 0 83.514809999999997 45.393146999999999 -4.2410550000000002 1;
	setAttr ".radi" 3;
	setAttr ".fbxID" 5;
createNode joint -n "LeftHandRing3_Skl" -p "LeftHandRing2_Skl";
	rename -uid "CF1E905A-4259-6B33-49A8-E088D7D27C58";
	addAttr -ci true -h true -sn "fbxID" -ln "filmboxTypeID" -at "short";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 2.7839624881744385 0.0013519180938601494 0.0028215954080224037 ;
	setAttr ".r" -type "double3" -1.5530052336862843e-18 1.9878466991184439e-16 2.7735701774231714e-17 ;
	setAttr ".jo" -type "double3" 0.0090221334617140506 -0.89684666926722345 0.42974754307148233 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.94820499999999996 0.036625400000000002 -0.31554199999999999 0
		 -0.31575399999999998 -1.2596899999999999e-06 -0.94884100000000005 0 -0.034752100000000001 0.99932900000000002 0.0115634 0
		 86.161814000000007 45.454374000000001 -5.1013310000000001 1;
	setAttr ".radi" 3;
	setAttr ".fbxID" 5;
createNode joint -n "LeftHandRing4_Skl" -p "LeftHandRing3_Skl";
	rename -uid "84ECE369-4865-FC11-5956-2FA7EF2ABF09";
	addAttr -ci true -h true -sn "fbxID" -ln "filmboxTypeID" -at "short";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 1.2494219541549683 -2.1316282072803006e-14 0 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.94820499999999996 0.036625400000000002 -0.31554199999999999 0
		 -0.31575399999999998 -1.2596899999999999e-06 -0.94884100000000005 0 -0.034752100000000001 0.99932900000000002 0.0115634 0
		 87.346521999999993 45.500135 -5.4955759999999998 1;
	setAttr ".radi" 3;
	setAttr ".fbxID" 5;
createNode joint -n "LeftHandPinky1_Skl" -p "LeftHand_Skl";
	rename -uid "5681FE6D-498B-C60F-5B9B-7EAE3E014081";
	addAttr -ci true -h true -sn "fbxID" -ln "filmboxTypeID" -at "short";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 9.5326433181762695 0.48194694519042969 -4.7678260803222656 ;
	setAttr ".r" -type "double3" -2.5643222828909508e-14 2.9817700619125557e-15 6.3611094371790206e-15 ;
	setAttr ".jo" -type "double3" -91.389698993413305 39.162501576716991 0.81521132727196166 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.85553599999999996 0.031119399999999998 -0.51680700000000002 0
		 -0.51705699999999999 -1.1363700000000001e-06 -0.85595100000000002 0 -0.026637299999999999 0.99951599999999996 0.0160895 0
		 79.345203999999995 45.061750000000004 -5.2753969999999999 1;
	setAttr ".radi" 3;
	setAttr ".fbxID" 5;
createNode joint -n "LeftHandPinky2_Skl" -p "LeftHandPinky1_Skl";
	rename -uid "4BDDBDBD-4078-5CE6-740F-2CA04D9A5F11";
	addAttr -ci true -h true -sn "fbxID" -ln "filmboxTypeID" -at "short";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 2.5694811344146729 -1.4210854715202004e-14 -1.9895196601282805e-13 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.85553599999999996 0.031119399999999998 -0.51680700000000002 0
		 -0.51705699999999999 -1.1363700000000001e-06 -0.85595100000000002 0 -0.026637299999999999 0.99951599999999996 0.0160895 0
		 81.543488999999994 45.141711000000001 -6.6033220000000004 1;
	setAttr ".radi" 3;
	setAttr ".fbxID" 5;
createNode joint -n "LeftHandPinky3_Skl" -p "LeftHandPinky2_Skl";
	rename -uid "3E9AE423-49ED-9825-E4B6-02A57E2B919D";
	addAttr -ci true -h true -sn "fbxID" -ln "filmboxTypeID" -at "short";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 2.0349900722503662 -1.5278934597517946e-06 -1.9682473066495731e-05 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.85553599999999996 0.031119399999999998 -0.51680700000000002 0
		 -0.51705699999999999 -1.1363700000000001e-06 -0.85595100000000002 0 -0.026637299999999999 0.99951599999999996 0.0160895 0
		 83.284497999999999 45.205019 -7.6550180000000001 1;
	setAttr ".radi" 3;
	setAttr ".fbxID" 5;
createNode joint -n "LeftHandPinky4_Skl" -p "LeftHandPinky3_Skl";
	rename -uid "0CEA7610-461C-0B14-117C-CE8253C1E6EA";
	addAttr -ci true -h true -sn "fbxID" -ln "filmboxTypeID" -at "short";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.84663504362106323 -3.5948198728874559e-07 4.5876572585257236e-06 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.85553599999999996 0.031119399999999998 -0.51680700000000002 0
		 -0.51705699999999999 -1.1363700000000001e-06 -0.85595100000000002 0 -0.026637299999999999 0.99951599999999996 0.0160895 0
		 84.008825000000002 45.231369999999998 -8.0925639999999994 1;
	setAttr ".radi" 3;
	setAttr ".fbxID" 5;
createNode joint -n "Neck_Skl" -p "Spine2_Skl";
	rename -uid "A9D879EB-47B0-5D83-2595-E8BB1087373E";
	addAttr -ci true -h true -sn "fbxID" -ln "filmboxTypeID" -at "short";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0 9.1061992645263672 4.2158932685852051 ;
	setAttr ".r" -type "double3" 5.2202801475542508e-15 3.1805547185895103e-15 1.2722218874358041e-14 ;
	setAttr ".jo" -type "double3" 180 -24.775140568832406 90 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0 0.90795899999999996 0.41905799999999999 0 1 0 0 0
		 0 0.41905799999999999 -0.90795899999999996 0 0 51.537177999999997 -4.4607939999999999 1;
	setAttr ".radi" 3;
	setAttr ".fbxID" 5;
createNode joint -n "Neck1_Skl" -p "Neck_Skl";
	rename -uid "D4F2F736-4FC3-4843-EAF7-3382FFC9B6F5";
	addAttr -ci true -h true -sn "fbxID" -ln "filmboxTypeID" -at "short";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 4.169499397277832 -3.1554436208840472e-30 2.8421709430404007e-14 ;
	setAttr ".jo" -type "double3" 0 -3.6429049134946543 0 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0 0.932751 0.36052200000000001 0 1 0 0 0 0 0.36052200000000001 -0.932751 0
		 0 55.322913999999997 -2.7135310000000001 1;
	setAttr ".radi" 3;
	setAttr ".fbxID" 5;
createNode joint -n "Head_Skl" -p "Neck1_Skl";
	rename -uid "13D45981-4521-6434-798D-9F851ABE4D39";
	addAttr -ci true -h true -sn "fbxID" -ln "filmboxTypeID" -at "short";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 6.8658542633056641 3.1554436208840472e-30 0 ;
	setAttr ".r" -type "double3" -7.0622501593165195e-31 -3.1805547185895103e-15 0 ;
	setAttr ".jo" -type "double3" 180 -21.671383840628618 0 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0 0.99995599999999996 -0.0094097699999999996 0 -1 0 0 0
		 0 0.0094097699999999996 0.99995599999999996 0 0 61.727046000000001 -0.23824200000000001 1;
	setAttr ".radi" 3;
	setAttr ".fbxID" 5;
createNode joint -n "Head_End_Skl" -p "Head_Skl";
	rename -uid "E97068F8-4224-EC4C-312F-CDB74F911499";
	addAttr -ci true -h true -sn "fbxID" -ln "filmboxTypeID" -at "short";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 15.526242256164551 6.8744558724448575e-15 -4.4408920985006262e-14 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0 0.99995599999999996 -0.0094097699999999996 0 -1 0 0 0
		 0 0.0094097699999999996 0.99995599999999996 0 0 77.252600000000001 -0.38434000000000001 1;
	setAttr ".radi" 3;
	setAttr ".fbxID" 5;
createNode joint -n "LeftEye_Skl" -p "Head_Skl";
	rename -uid "9DD7C846-4E9F-9188-E24A-C68858A404B5";
	addAttr -ci true -h true -sn "fbxID" -ln "filmboxTypeID" -at "short";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 7.2540580844057434 -4.179184271395795 7.1966059707155203 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0 0.99995599999999996 -0.0094097699999999996 0 -1 0 0 0
		 0 0.0094097699999999996 0.99995599999999996 0 0 77.252600000000001 -0.38434000000000001 1;
	setAttr ".radi" 3;
	setAttr ".fbxID" 5;
createNode joint -n "RightEye_Skl" -p "Head_Skl";
	rename -uid "E27F03BE-4C56-75C5-06F7-7AB303B70C03";
	addAttr -ci true -h true -sn "fbxID" -ln "filmboxTypeID" -at "short";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 7.2540580844057434 4.179 7.1966059707155203 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0 0.99995599999999996 -0.0094097699999999996 0 -1 0 0 0
		 0 0.0094097699999999996 0.99995599999999996 0 0 77.252600000000001 -0.38434000000000001 1;
	setAttr ".radi" 3;
	setAttr ".fbxID" 5;
createNode joint -n "Jaw_Skl" -p "Head_Skl";
	rename -uid "AD534D16-4495-1910-1DC1-8986D5294CC1";
	addAttr -ci true -h true -sn "fbxID" -ln "filmboxTypeID" -at "short";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0 0 7.1966059707155203 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0 0.99995599999999996 -0.0094097699999999996 0 -1 0 0 0
		 0 0.0094097699999999996 0.99995599999999996 0 0 77.252600000000001 -0.38434000000000001 1;
	setAttr ".radi" 3;
	setAttr ".fbxID" 5;
createNode joint -n "RightShoulder_Skl" -p "Spine2_Skl";
	rename -uid "F50EB649-4116-5492-8FC4-A2AC2FEEC59D";
	addAttr -ci true -h true -sn "fbxID" -ln "filmboxTypeID" -at "short";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -4.4481000900268555 2.2396931648254395 13.301906585693359 ;
	setAttr ".jo" -type "double3" -177.77500000000026 0 0 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 -0.99924599999999997 -0.038823799999999999 0
		 0 0.038823799999999999 -0.99924599999999997 0 -4.4481000000000002 44.670672000000003 4.6252199999999997 1;
	setAttr ".radi" 3;
	setAttr ".fbxID" 5;
createNode joint -n "RightArm_Skl" -p "RightShoulder_Skl";
	rename -uid "23F12392-4A92-3BFD-982F-D7BD69D1100B";
	addAttr -ci true -h true -sn "fbxID" -ln "filmboxTypeID" -at "short";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -16.164699554443359 0.47569537162780762 8.30255126953125 ;
	setAttr ".jo" -type "double3" 0 4.100000000000005 0 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.99744100000000002 -0.0027758000000000001 0.071443499999999993 0
		 0 -0.99924599999999997 -0.038823799999999999 0 0.071497400000000003 0.038724500000000002 -0.99668900000000005 0
		 -20.6128 44.517671999999997 -3.68954 1;
	setAttr ".radi" 3;
	setAttr ".fbxID" 5;
createNode joint -n "RightArm_Roll_Skl" -p "RightArm_Skl";
	rename -uid "70ABE4A6-4A0E-06DE-4C9F-CCBD880D824F";
	addAttr -is true -ci true -k true -sn "atoms_skipIk" -ln "atoms_skipIk" -min 0 
		-max 1 -at "bool";
	addAttr -ci true -h true -sn "fbxID" -ln "filmboxTypeID" -at "short";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -12.737098693847656 -0.00064396235393360257 2.1658470359398052e-05 ;
	setAttr ".jo" -type "double3" 2.5613209387547812e-06 0 0 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.99744100000000002 -0.0027758000000000001 0.071443499999999993 0
		 3.19618e-09 -0.99924599999999997 -0.038823900000000001 0 0.071497400000000003 0.038724500000000002 -0.99668900000000005 0
		 -33.317300000000003 44.553671999999999 -4.5995200000000001 1;
	setAttr ".radi" 3;
	setAttr ".fbxID" 5;
createNode joint -n "RightForeArm_Skl" -p "RightArm_Roll_Skl";
	rename -uid "C2936AE4-4C5F-72D3-F57F-DAB5DD1CDBDB";
	addAttr -ci true -h true -sn "fbxID" -ln "filmboxTypeID" -at "short";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -11.06962776184082 0.00072682107565924525 -2.1706824554712512e-05 ;
	setAttr ".r" -type "double3" -7.5830333676088102e-22 1.5902773592947552e-15 0 ;
	setAttr ".jo" -type "double3" 3.6634124373868582e-06 -12.090139543516074 0 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.99029199999999995 0.0053966200000000004 -0.13889799999999999 0
		 -5.6914499999999998e-09 -0.99924599999999997 -0.038823900000000001 0 -0.13900299999999999 0.038447000000000002 -0.98954500000000001 0
		 -44.358600000000003 44.583672 -5.3903800000000004 1;
	setAttr ".radi" 3;
	setAttr ".fbxID" 5;
createNode joint -n "RightForeArm_Roll_Skl" -p "RightForeArm_Skl";
	rename -uid "3085199F-4FA6-E888-CA8E-279E4C2CD033";
	addAttr -is true -ci true -k true -sn "atoms_skipIk" -ln "atoms_skipIk" -min 0 
		-max 1 -at "bool";
	addAttr -ci true -h true -sn "fbxID" -ln "filmboxTypeID" -at "short";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -10.700986862182617 0.00025039285537786782 -1.5459299902431667e-05 ;
	setAttr ".r" -type "double3" -7.5830333676088102e-22 0 0 ;
	setAttr ".jo" -type "double3" 6.0971633888818185e-06 0 0 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.99029199999999995 0.0053966200000000004 -0.13889799999999999 0
		 -2.0483500000000003e-08 -0.99924599999999997 -0.038823999999999997 0 -0.13900299999999999 0.038447099999999998 -0.98954500000000001 0
		 -54.955699000000003 44.525672 -3.9040309999999998 1;
	setAttr ".radi" 3;
	setAttr ".fbxID" 5;
createNode joint -n "RightHand_Skl" -p "RightForeArm_Roll_Skl";
	rename -uid "D726964F-4DE8-7699-5BDE-7EA23FC87E20";
	addAttr -ci true -h true -sn "fbxID" -ln "filmboxTypeID" -at "short";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -14.426749229431152 -0.00085490325000137091 3.8477068301290274e-05 ;
	setAttr ".r" -type "double3" -1.516606673521762e-21 0 0 ;
	setAttr ".jo" -type "double3" 1.2863397010924443e-05 0 0 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.99029199999999995 0.0053966200000000004 -0.13889799999999999 0
		 -5.1690799999999999e-08 -0.99924599999999997 -0.038824299999999999 0 -0.13900299999999999 0.0384474 -0.98954500000000001 0
		 -69.242399000000006 44.448672000000002 -1.900191 1;
	setAttr ".radi" 3;
	setAttr ".fbxID" 5;
createNode joint -n "RightHandThumb1_Skl" -p "RightHand_Skl";
	rename -uid "36A82AF1-471D-0208-9C8E-3C8FD77EB9D1";
	addAttr -ci true -h true -sn "fbxID" -ln "filmboxTypeID" -at "short";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -4.6116523742675781 2.5270490646362305 -4.2127447128295898 ;
	setAttr ".r" -type "double3" -1.5902773592947552e-15 -3.1805547185895103e-15 -4.7708321837633839e-15 ;
	setAttr ".jo" -type "double3" 20.952 -35.997014564769991 -32.740030717041677 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.59221199999999996 0.46349499999999999 -0.65913299999999997 0
		 0.28488799999999997 -0.88561000000000001 -0.366788 0 -0.75373999999999997 0.029437399999999999 -0.65651400000000004 0
		 -73.223698999999996 41.736671999999999 2.8109489999999999 1;
	setAttr ".radi" 3;
	setAttr ".fbxID" 5;
createNode joint -n "RightHandThumb2_Skl" -p "RightHandThumb1_Skl";
	rename -uid "BD4019A7-4A08-C4A2-8726-8F98D0BA723E";
	addAttr -ci true -h true -sn "fbxID" -ln "filmboxTypeID" -at "short";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -2.5022637844085693 -3.2028513032855699e-06 0.00023935106582939625 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.59221199999999996 0.46349499999999999 -0.65913299999999997 0
		 0.28488799999999997 -0.88561000000000001 -0.366788 0 -0.75373999999999997 0.029437399999999999 -0.65651400000000004 0
		 -74.705752000000004 40.576894000000003 4.4601179999999996 1;
	setAttr ".radi" 3;
	setAttr ".fbxID" 5;
createNode joint -n "RightHandThumb3_Skl" -p "RightHandThumb2_Skl";
	rename -uid "7EE1D57B-4576-D6D1-F96E-FBB43CBE5DDF";
	addAttr -ci true -h true -sn "fbxID" -ln "filmboxTypeID" -at "short";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -2.4191079139709473 1.5742412870167755e-05 -0.00027714017778635025 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.59221199999999996 0.46349499999999999 -0.65913299999999997 0
		 0.28488799999999997 -0.88561000000000001 -0.366788 0 -0.75373999999999997 0.029437399999999999 -0.65651400000000004 0
		 -76.138164000000003 39.455626000000002 6.0548080000000004 1;
	setAttr ".radi" 3;
	setAttr ".fbxID" 5;
createNode joint -n "RightHandThumb4_Skl" -p "RightHandThumb3_Skl";
	rename -uid "0A0B38E1-4A5B-647B-2B1F-D39636650BC8";
	addAttr -ci true -h true -sn "fbxID" -ln "filmboxTypeID" -at "short";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -3.5766677856445312 -4.4972366595175117e-05 0.00026035419432446361 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.59221199999999996 0.46349499999999999 -0.65913299999999997 0
		 0.28488799999999997 -0.88561000000000001 -0.366788 0 -0.75373999999999997 0.029437399999999999 -0.65651400000000004 0
		 -78.256521000000006 37.797904000000003 8.4121539999999992 1;
	setAttr ".radi" 3;
	setAttr ".fbxID" 5;
createNode joint -n "RightHandIndex1_Skl" -p "RightHand_Skl";
	rename -uid "CCE123F3-4DA5-B5F6-E573-4381AC2A3F41";
	addAttr -ci true -h true -sn "fbxID" -ln "filmboxTypeID" -at "short";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -10.43730354309082 -0.75825327634811401 -1.8559249639511108 ;
	setAttr ".r" -type "double3" -3.9756933982368879e-16 -2.9817701148521149e-16 3.1805547185895103e-15 ;
	setAttr ".jo" -type "double3" -92.624920301475669 -10.071085441213672 2.903455171943607 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.94947400000000004 -0.037805100000000001 -0.31156 0
		 0.31178299999999998 1.2614399999999999e-06 0.95015300000000003 0 -0.035920300000000002 -0.99928499999999998 0.0117882 0
		 -79.320398999999995 45.078671999999997 1.415489 1;
	setAttr ".radi" 3;
	setAttr ".fbxID" 5;
createNode joint -n "RightHandIndex2_Skl" -p "RightHandIndex1_Skl";
	rename -uid "EEC72C27-49FE-6620-DED2-FE9B9FEE526D";
	addAttr -ci true -h true -sn "fbxID" -ln "filmboxTypeID" -at "short";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -4.1109247207641602 -1.3790253433398902e-05 -0.00058630347484722733 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.94947400000000004 -0.037805100000000001 -0.31156 0
		 0.31178299999999998 1.2614399999999999e-06 0.95015300000000003 0 -0.035920300000000002 -0.99928499999999998 0.0117882 0
		 -83.223597999999996 45.234672000000003 2.696269 1;
	setAttr ".radi" 3;
	setAttr ".fbxID" 5;
createNode joint -n "RightHandIndex3_Skl" -p "RightHandIndex2_Skl";
	rename -uid "DB1F3877-46C9-9E97-9E09-53BC8FDBEA32";
	addAttr -ci true -h true -sn "fbxID" -ln "filmboxTypeID" -at "short";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -3.2181887626647949 3.4790449717547745e-05 0.00066457345383241773 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.94947400000000004 -0.037805100000000001 -0.31156 0
		 0.31178299999999998 1.2614399999999999e-06 0.95015300000000003 0 -0.035920300000000002 -0.99928499999999998 0.0117882 0
		 -86.279197999999994 45.355671999999998 3.698969 1;
	setAttr ".radi" 3;
	setAttr ".fbxID" 5;
createNode joint -n "RightHandIndex4_Skl" -p "RightHandIndex3_Skl";
	rename -uid "84DDF11A-4843-CF3B-1A2D-5591417DBF0B";
	addAttr -ci true -h true -sn "fbxID" -ln "filmboxTypeID" -at "short";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -1.4270985126495361 -2.771367144305259e-05 -4.8366848204750568e-05 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.94947400000000004 -0.037805100000000001 -0.31156 0
		 0.31178299999999998 1.2614399999999999e-06 0.95015300000000003 0 -0.035920300000000002 -0.99928499999999998 0.0117882 0
		 -87.634197999999998 45.409672 4.1435690000000003 1;
	setAttr ".radi" 3;
	setAttr ".fbxID" 5;
createNode joint -n "RightHandMiddle1_Skl" -p "RightHand_Skl";
	rename -uid "DD77911D-4857-FE7E-7AD7-C2B090A7BF75";
	addAttr -ci true -h true -sn "fbxID" -ln "filmboxTypeID" -at "short";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -10.311113357543945 -0.79861700534820557 0.19846133887767792 ;
	setAttr ".r" -type "double3" -1.1927080247650223e-14 6.4605018713966163e-16 4.2070043562751291e-32 ;
	setAttr ".jo" -type "double3" -91.889533553517197 8.6630240194866186 2.2369776225226219 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.99918499999999999 -0.039018400000000002 0.010341400000000001 0
		 -0.010349300000000001 1.32754e-06 0.999946 0 -0.039016299999999997 -0.99923799999999996 -0.00040248500000000001 0
		 -79.480998999999997 45.198672000000002 -0.63338000000000005 1;
	setAttr ".radi" 3;
	setAttr ".fbxID" 5;
createNode joint -n "RightHandMiddle2_Skl" -p "RightHandMiddle1_Skl";
	rename -uid "F513BA66-485D-7E3A-C1C6-9081C640D5C3";
	addAttr -ci true -h true -sn "fbxID" -ln "filmboxTypeID" -at "short";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -5.1369695663452148 -1.6759980780989281e-07 0.00043647640268318355 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.99918499999999999 -0.039018400000000002 0.010341400000000001 0
		 -0.010349300000000001 1.32754e-06 0.999946 0 -0.039016299999999997 -0.99923799999999996 -0.00040248500000000001 0
		 -84.613798000000003 45.398671999999998 -0.686504 1;
	setAttr ".radi" 3;
	setAttr ".fbxID" 5;
createNode joint -n "RightHandMiddle3_Skl" -p "RightHandMiddle2_Skl";
	rename -uid "7568ED65-4720-CD26-499A-46A4F6D16A67";
	addAttr -ci true -h true -sn "fbxID" -ln "filmboxTypeID" -at "short";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -3.0791430473327637 4.232876165133348e-07 -0.00085753586608916521 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.99918499999999999 -0.039018400000000002 0.010341400000000001 0
		 -0.010349300000000001 1.32754e-06 0.999946 0 -0.039016299999999997 -0.99923799999999996 -0.00040248500000000001 0
		 -87.690398999999999 45.519672 -0.71834600000000004 1;
	setAttr ".radi" 3;
	setAttr ".fbxID" 5;
createNode joint -n "RightHandMiddle4_Skl" -p "RightHandMiddle3_Skl";
	rename -uid "9073280D-484E-CD4E-BDEE-95A9A30A84BF";
	addAttr -ci true -h true -sn "fbxID" -ln "filmboxTypeID" -at "short";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -1.2404953241348267 -3.3176536362589104e-07 0.00040240245289169252 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.99918499999999999 -0.039018400000000002 0.010341400000000001 0
		 -0.010349300000000001 1.32754e-06 0.999946 0 -0.039016299999999997 -0.99923799999999996 -0.00040248500000000001 0
		 -88.929899000000006 45.567672000000002 -0.73117500000000002 1;
	setAttr ".radi" 3;
	setAttr ".fbxID" 5;
createNode joint -n "RightHandRing1_Skl" -p "RightHand_Skl";
	rename -uid "A852E295-44AA-F2DB-D884-11A6EDEA2E79";
	addAttr -ci true -h true -sn "fbxID" -ln "filmboxTypeID" -at "short";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -10.027981758117676 -0.71398138999938965 2.436427116394043 ;
	setAttr ".r" -type "double3" -1.2225257020907418e-14 -2.037542836817903e-15 0 ;
	setAttr ".jo" -type "double3" -91.112344245048874 26.749438827627849 2.2133715977287824 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.946218 -0.046951199999999998 0.320104 0 -0.32045800000000002 1.2576e-06 0.94726299999999997 0
		 -0.044475500000000001 -0.99889700000000003 -0.015044699999999999 0 -79.511698999999993 45.201672000000002 -2.8905609999999999 1;
	setAttr ".radi" 3;
	setAttr ".fbxID" 5;
createNode joint -n "RightHandRing2_Skl" -p "RightHandRing1_Skl";
	rename -uid "DDDEE70D-4F5A-32CF-F580-CB9D168F246A";
	addAttr -ci true -h true -sn "fbxID" -ln "filmboxTypeID" -at "short";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -4.2290711402893066 0.0035550582688301802 0.0075682317838072777 ;
	setAttr ".r" -type "double3" 1.2424041869490275e-17 0 -2.3295079022282148e-18 ;
	setAttr ".jo" -type "double3" -0.033546838592720868 1.4887472159890935 -0.71435944667219842 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.95097500000000001 -0.0209797 0.308556 0 -0.30862400000000001 1.2628100000000001e-06 0.95118400000000003 0
		 -0.019956000000000002 -0.99978 -0.0064736500000000001 0 -83.514798999999996 45.392671999999997 -4.2410509999999997 1;
	setAttr ".radi" 3;
	setAttr ".fbxID" 5;
createNode joint -n "RightHandRing3_Skl" -p "RightHandRing2_Skl";
	rename -uid "85B47159-4E73-84CC-F76F-D2976B18E93F";
	addAttr -ci true -h true -sn "fbxID" -ln "filmboxTypeID" -at "short";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -2.7839756011962891 -0.0013568820431828499 -0.003593730041757226 ;
	setAttr ".r" -type "double3" 1.5530052336862843e-18 0 5.3166163677841448e-17 ;
	setAttr ".jo" -type "double3" 0.0090221341385255758 -0.89684666926889656 0.42974754306794954 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.94820499999999996 -0.036625400000000002 0.31554199999999999 0
		 -0.31575399999999998 1.2596899999999999e-06 0.94884100000000005 0 -0.034752100000000001 -0.99932900000000002 -0.0115634 0
		 -86.161799000000002 45.454672000000002 -5.1013310000000001 1;
	setAttr ".radi" 3;
	setAttr ".fbxID" 5;
createNode joint -n "RightHandRing4_Skl" -p "RightHandRing3_Skl";
	rename -uid "B93A5A09-4749-5853-F4A9-1B9289520E9A";
	addAttr -ci true -h true -sn "fbxID" -ln "filmboxTypeID" -at "short";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -1.2493884563446045 -7.4126764957327396e-06 0.00075987004674971104 ;
	setAttr ".jo" -type "double3" 3.0783246591999756e-06 0 0 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.94820499999999996 -0.036625400000000002 0.31554199999999999 0
		 -0.31575399999999998 1.206e-06 0.94884100000000005 0 -0.034752100000000001 -0.99932900000000002 -0.011563500000000001 0
		 -87.346498999999994 45.499671999999997 -5.4955809999999996 1;
	setAttr ".radi" 3;
	setAttr ".fbxID" 5;
createNode joint -n "RightHandPinky1_Skl" -p "RightHand_Skl";
	rename -uid "8D45AD4D-47B0-BA0F-73EB-838FA33158D7";
	addAttr -ci true -h true -sn "fbxID" -ln "filmboxTypeID" -at "short";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -9.5326042175292969 -0.48149731755256653 4.7678079605102539 ;
	setAttr ".r" -type "double3" 1.2026472787746937e-14 3.0811623902510326e-15 6.3611094371790206e-15 ;
	setAttr ".jo" -type "double3" -91.389731399010898 39.162501934231805 0.81519139889378778 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.85553599999999996 -0.031119399999999998 0.51680700000000002 0
		 -0.51705699999999999 1.1363700000000001e-06 0.85595100000000002 0 -0.026637299999999999 -0.99951599999999996 -0.0160895 0
		 -79.345198999999994 45.061672000000002 -5.2754009999999996 1;
	setAttr ".radi" 3;
	setAttr ".fbxID" 5;
createNode joint -n "RightHandPinky2_Skl" -p "RightHandPinky1_Skl";
	rename -uid "CFF38012-469D-D7E1-2244-88B1B057C6F9";
	addAttr -ci true -h true -sn "fbxID" -ln "filmboxTypeID" -at "short";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -2.5694930553436279 1.2411222996888682e-05 -3.8973470509517938e-05 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.85553599999999996 -0.031119399999999998 0.51680700000000002 0
		 -0.51705699999999999 1.1363700000000001e-06 0.85595100000000002 0 -0.026637299999999999 -0.99951599999999996 -0.0160895 0
		 -81.543498999999997 45.141672 -6.6033210000000002 1;
	setAttr ".radi" 3;
	setAttr ".fbxID" 5;
createNode joint -n "RightHandPinky3_Skl" -p "RightHandPinky2_Skl";
	rename -uid "B950664E-433B-5FE7-F667-5FA255CBD3A8";
	addAttr -ci true -h true -sn "fbxID" -ln "filmboxTypeID" -at "short";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -2.0349748134613037 -7.0657615651725791e-06 0.00032732752151787281 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.85553599999999996 -0.031119399999999998 0.51680700000000002 0
		 -0.51705699999999999 1.1363700000000001e-06 0.85595100000000002 0 -0.026637299999999999 -0.99951599999999996 -0.0160895 0
		 -83.284498999999997 45.204672000000002 -7.6550209999999996 1;
	setAttr ".radi" 3;
	setAttr ".fbxID" 5;
createNode joint -n "RightHandPinky4_Skl" -p "RightHandPinky3_Skl";
	rename -uid "421FC712-4ECF-6E50-443A-EDAE70CF4D9E";
	addAttr -ci true -h true -sn "fbxID" -ln "filmboxTypeID" -at "short";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -0.84662878513336182 -8.2631340774241835e-06 -0.00065374840050935745 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.85553599999999996 -0.031119399999999998 0.51680700000000002 0
		 -0.51705699999999999 1.1363700000000001e-06 0.85595100000000002 0 -0.026637299999999999 -0.99951599999999996 -0.0160895 0
		 -84.008798999999996 45.231672000000003 -8.0925609999999999 1;
	setAttr ".radi" 3;
	setAttr ".fbxID" 5;
createNode joint -n "RightUpLeg_Skl" -p "Hips_Skl";
	rename -uid "B037663B-4A1F-1493-C73A-F2A1C802255F";
	addAttr -is true -ci true -k true -sn "atoms_poleVector" -ln "atoms_poleVector" 
		-at "double3" -nc 3;
	addAttr -is true -ci true -sn "atoms_poleVector0" -ln "atoms_poleVector0" -at "double" 
		-p "atoms_poleVector";
	addAttr -is true -ci true -sn "atoms_poleVector1" -ln "atoms_poleVector1" -at "double" 
		-p "atoms_poleVector";
	addAttr -is true -ci true -sn "atoms_poleVector2" -ln "atoms_poleVector2" -at "double" 
		-p "atoms_poleVector";
	addAttr -ci true -h true -sn "fbxID" -ln "filmboxTypeID" -at "short";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -7.4505200386047363 -7.740328311920166 1.5381200313568115 ;
	setAttr ".r" -type "double3" -9.9404631492036166e-16 -7.9513867964737758e-16 1.5611639898646776e-15 ;
	setAttr ".jo" -type "double3" -179.99999999999986 2.7003134116908623 86.000000000000085 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.069679000000000005 0.99645600000000001 -0.047111899999999998 0
		 0.99756400000000001 -0.069756499999999999 0 0 -0.0032863599999999999 -0.046997200000000003 -0.99888999999999994 0
		 -7.45052 -7.7403279999999999 1.5381199999999999 1;
	setAttr ".radi" 3;
	setAttr -k on ".atoms_poleVector" -type "double3" -10.295199966395105 -7.740328311920166 
		23.603416763902558 ;
	setAttr ".fbxID" 5;
createNode joint -n "RightLeg_Skl" -p "RightUpLeg_Skl";
	rename -uid "911B9F9F-4919-4DBB-7DC0-8DBF08335BA3";
	addAttr -ci true -h true -sn "fbxID" -ln "filmboxTypeID" -at "short";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -40.825569152832031 5.6302442317246459e-06 7.8129568237272906e-07 ;
	setAttr ".r" -type "double3" 0 -7.9513867964737758e-16 0 ;
	setAttr ".jo" -type "double3" 0 5.2989999999999995 0 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.069684700000000002 0.99653800000000003 0.045340100000000001 0
		 0.99756400000000001 -0.069756499999999999 0 0 0.0031627600000000001 0.045229600000000002 -0.99897199999999997 0
		 -10.295199999999999 -48.421227000000002 3.46149 1;
	setAttr ".radi" 3;
	setAttr ".fbxID" 5;
createNode joint -n "RightFoot_Skl" -p "RightLeg_Skl";
	rename -uid "8DF92BDA-4822-C5DD-854B-77BC5E5F271B";
	addAttr -is true -ci true -k true -sn "atoms_ikMaxIterations" -ln "atoms_ikMaxIterations" 
		-smn 0 -smx 0 -at "long";
	addAttr -is true -ci true -k true -sn "atoms_ikSoftDistance" -ln "atoms_ikSoftDistance" 
		-smn 0 -smx 0 -at "double";
	addAttr -is true -ci true -k true -sn "atoms_ikSolver" -ln "atoms_ikSolver" -smn 
		0 -smx 0 -at "long";
	addAttr -is true -ci true -k true -sn "atoms_ikTollerance" -ln "atoms_ikTollerance" 
		-smn 0 -smx 0 -at "double";
	addAttr -ci true -h true -sn "fbxID" -ln "filmboxTypeID" -at "short";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -46.434242248535156 -4.2263596697011963e-05 7.4190329542034306e-06 ;
	setAttr ".r" -type "double3" -1.192708045940846e-15 0 0 ;
	setAttr ".jo" -type "double3" -4.4163831504674604 -67.475285727358781 -7.9513867036587939e-16 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.0296165 0.42353499999999999 -0.90539499999999995 0
		 0.99946500000000005 0 0.032693600000000003 0 0.013846900000000001 -0.90588000000000002 -0.42330899999999999 0
		 -13.531000000000001 -94.694719000000006 1.35615 1;
	setAttr ".radi" 3;
	setAttr -k on ".atoms_ikSoftDistance" 0.05;
	setAttr -k on ".atoms_ikTollerance" 0.001;
	setAttr ".fbxID" 5;
createNode joint -n "RightToeBase_Skl" -p "RightFoot_Skl";
	rename -uid "95DEBD94-4BC2-BB82-CC17-05AE47BD71C9";
	addAttr -ci true -h true -sn "fbxID" -ln "filmboxTypeID" -at "short";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -16.124937057495117 6.3573119405191392e-05 -6.1505261328420602e-06 ;
	setAttr ".r" -type "double3" 9.9392334955922197e-17 3.1805547185895103e-15 -4.9696167477961099e-17 ;
	setAttr ".jo" -type "double3" 0.77538331646094538 -22.454178566140531 -1.4908850069360235e-16 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.032659800000000003 0.0454291 -0.99843400000000004 0
		 0.999394 -0.0135186 0.032076100000000003 0 -0.012040199999999999 -0.99887599999999999 -0.045843099999999998 0
		 -14.0085 -101.524188 15.9556 1;
	setAttr ".radi" 3;
	setAttr ".fbxID" 5;
createNode joint -n "RightToeEnd_Skl" -p "RightToeBase_Skl";
	rename -uid "255CD660-448F-173C-0156-6F8DA95ADBDB";
	addAttr -ci true -h true -sn "fbxID" -ln "filmboxTypeID" -at "short";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -5.8856186866760254 2.333071461180225e-05 1.3946144008514239e-06 ;
	setAttr ".jo" -type "double3" 3.4150945850063708e-06 0 0 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.032659800000000003 0.0454291 -0.99843400000000004 0
		 0.999394 -0.0135187 0.032076100000000003 0 -0.0120403 -0.99887599999999999 -0.045843099999999998 0
		 -14.200699999999999 -101.791568 21.831999 1;
	setAttr ".radi" 3;
	setAttr ".fbxID" 5;
createNode joint -n "SpineHolder_Skl" -p "Hips_Skl";
	rename -uid "5B1E9BC3-4481-7A4E-9D6A-57810C1263CD";
	addAttr -ci true -h true -sn "fbxID" -ln "filmboxTypeID" -at "short";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0 -8.3644107444011127 0 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1;
	setAttr ".radi" 2;
	setAttr ".fbxID" 5;
createNode lightLinker -s -n "lightLinker1";
	rename -uid "EF49FEB4-4D7B-7100-3B3B-5EACE2377509";
	setAttr -s 2 ".lnk";
	setAttr -s 2 ".slnk";
createNode shapeEditorManager -n "shapeEditorManager";
	rename -uid "55ED3D60-47E3-9608-DAB3-A897E3368A0E";
createNode poseInterpolatorManager -n "poseInterpolatorManager";
	rename -uid "B4F1C9C1-4C57-2DB4-32F1-D9B4F23E920E";
createNode displayLayerManager -n "layerManager";
	rename -uid "55611E64-472F-F61E-33B6-D6A10C801E49";
createNode displayLayer -n "defaultLayer";
	rename -uid "CF50AE44-4C18-B74C-FEE2-548B30326D75";
createNode renderLayerManager -n "renderLayerManager";
	rename -uid "E6A5B760-4F00-B52F-239A-5696DDD9A512";
createNode renderLayer -n "defaultRenderLayer";
	rename -uid "23146628-4EA4-389B-4E5E-67B4CB57DCE8";
	setAttr ".g" yes;
createNode network -n "Mutant_Tools";
	rename -uid "0531AE8C-49BF-3209-F0A5-6E9F6886935E";
	addAttr -ci true -sn "Date" -ln "Date" -dt "string";
	addAttr -ci true -sn "Version" -ln "Version" -dt "string";
	setAttr -l on ".Date" -type "string" "Mon Nov  7 15:31:23 2022";
	setAttr -l on ".Version" -type "string" "1.01";
createNode script -n "uiConfigurationScriptNode";
	rename -uid "D5EF1C97-4583-DEC9-B8C6-09833F569629";
	setAttr ".b" -type "string" (
		"// Maya Mel UI Configuration File.\n//\n//  This script is machine generated.  Edit at your own risk.\n//\n//\n\nglobal string $gMainPane;\nif (`paneLayout -exists $gMainPane`) {\n\n\tglobal int $gUseScenePanelConfig;\n\tint    $useSceneConfig = $gUseScenePanelConfig;\n\tint    $nodeEditorPanelVisible = stringArrayContains(\"nodeEditorPanel1\", `getPanel -vis`);\n\tint    $nodeEditorWorkspaceControlOpen = (`workspaceControl -exists nodeEditorPanel1Window` && `workspaceControl -q -visible nodeEditorPanel1Window`);\n\tint    $menusOkayInPanels = `optionVar -q allowMenusInPanels`;\n\tint    $nVisPanes = `paneLayout -q -nvp $gMainPane`;\n\tint    $nPanes = 0;\n\tstring $editorName;\n\tstring $panelName;\n\tstring $itemFilterName;\n\tstring $panelConfig;\n\n\t//\n\t//  get current state of the UI\n\t//\n\tsceneUIReplacement -update $gMainPane;\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"modelPanel\" (localizedPanelLabel(\"Top View\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tmodelPanel -edit -l (localizedPanelLabel(\"Top View\")) -mbv $menusOkayInPanels  $panelName;\n"
		+ "\t\t$editorName = $panelName;\n        modelEditor -e \n            -camera \"|top\" \n            -useInteractiveMode 0\n            -displayLights \"default\" \n            -displayAppearance \"smoothShaded\" \n            -activeOnly 0\n            -ignorePanZoom 0\n            -wireframeOnShaded 0\n            -headsUpDisplay 1\n            -holdOuts 1\n            -selectionHiliteDisplay 1\n            -useDefaultMaterial 0\n            -bufferMode \"double\" \n            -twoSidedLighting 0\n            -backfaceCulling 0\n            -xray 0\n            -jointXray 0\n            -activeComponentsXray 0\n            -displayTextures 0\n            -smoothWireframe 0\n            -lineWidth 1\n            -textureAnisotropic 0\n            -textureHilight 1\n            -textureSampling 2\n            -textureDisplay \"modulate\" \n            -textureMaxSize 32768\n            -fogging 0\n            -fogSource \"fragment\" \n            -fogMode \"linear\" \n            -fogStart 0\n            -fogEnd 100\n            -fogDensity 0.1\n            -fogColor 0.5 0.5 0.5 1 \n"
		+ "            -depthOfFieldPreview 1\n            -maxConstantTransparency 1\n            -rendererName \"vp2Renderer\" \n            -objectFilterShowInHUD 1\n            -isFiltered 0\n            -colorResolution 256 256 \n            -bumpResolution 512 512 \n            -textureCompression 0\n            -transparencyAlgorithm \"frontAndBackCull\" \n            -transpInShadows 0\n            -cullingOverride \"none\" \n            -lowQualityLighting 0\n            -maximumNumHardwareLights 1\n            -occlusionCulling 0\n            -shadingModel 0\n            -useBaseRenderer 0\n            -useReducedRenderer 0\n            -smallObjectCulling 0\n            -smallObjectThreshold -1 \n            -interactiveDisableShadows 0\n            -interactiveBackFaceCull 0\n            -sortTransparent 1\n            -controllers 1\n            -nurbsCurves 1\n            -nurbsSurfaces 1\n            -polymeshes 1\n            -subdivSurfaces 1\n            -planes 1\n            -lights 1\n            -cameras 1\n            -controlVertices 1\n"
		+ "            -hulls 1\n            -grid 1\n            -imagePlane 1\n            -joints 1\n            -ikHandles 1\n            -deformers 1\n            -dynamics 1\n            -particleInstancers 1\n            -fluids 1\n            -hairSystems 1\n            -follicles 1\n            -nCloths 1\n            -nParticles 1\n            -nRigids 1\n            -dynamicConstraints 1\n            -locators 1\n            -manipulators 1\n            -pluginShapes 1\n            -dimensions 1\n            -handles 1\n            -pivots 1\n            -textures 1\n            -strokes 1\n            -motionTrails 1\n            -clipGhosts 1\n            -greasePencils 1\n            -shadows 0\n            -captureSequenceNumber -1\n            -width 1\n            -height 1\n            -sceneRenderFilter 0\n            $editorName;\n        modelEditor -e -viewSelected 0 $editorName;\n        modelEditor -e \n            -pluginObjects \"gpuCacheDisplayFilter\" 1 \n            $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n"
		+ "\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"modelPanel\" (localizedPanelLabel(\"Side View\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tmodelPanel -edit -l (localizedPanelLabel(\"Side View\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        modelEditor -e \n            -camera \"|side\" \n            -useInteractiveMode 0\n            -displayLights \"default\" \n            -displayAppearance \"smoothShaded\" \n            -activeOnly 0\n            -ignorePanZoom 0\n            -wireframeOnShaded 0\n            -headsUpDisplay 1\n            -holdOuts 1\n            -selectionHiliteDisplay 1\n            -useDefaultMaterial 0\n            -bufferMode \"double\" \n            -twoSidedLighting 0\n            -backfaceCulling 0\n            -xray 0\n            -jointXray 0\n            -activeComponentsXray 0\n            -displayTextures 0\n            -smoothWireframe 0\n            -lineWidth 1\n            -textureAnisotropic 0\n            -textureHilight 1\n            -textureSampling 2\n"
		+ "            -textureDisplay \"modulate\" \n            -textureMaxSize 32768\n            -fogging 0\n            -fogSource \"fragment\" \n            -fogMode \"linear\" \n            -fogStart 0\n            -fogEnd 100\n            -fogDensity 0.1\n            -fogColor 0.5 0.5 0.5 1 \n            -depthOfFieldPreview 1\n            -maxConstantTransparency 1\n            -rendererName \"vp2Renderer\" \n            -objectFilterShowInHUD 1\n            -isFiltered 0\n            -colorResolution 256 256 \n            -bumpResolution 512 512 \n            -textureCompression 0\n            -transparencyAlgorithm \"frontAndBackCull\" \n            -transpInShadows 0\n            -cullingOverride \"none\" \n            -lowQualityLighting 0\n            -maximumNumHardwareLights 1\n            -occlusionCulling 0\n            -shadingModel 0\n            -useBaseRenderer 0\n            -useReducedRenderer 0\n            -smallObjectCulling 0\n            -smallObjectThreshold -1 \n            -interactiveDisableShadows 0\n            -interactiveBackFaceCull 0\n"
		+ "            -sortTransparent 1\n            -controllers 1\n            -nurbsCurves 1\n            -nurbsSurfaces 1\n            -polymeshes 1\n            -subdivSurfaces 1\n            -planes 1\n            -lights 1\n            -cameras 1\n            -controlVertices 1\n            -hulls 1\n            -grid 1\n            -imagePlane 1\n            -joints 1\n            -ikHandles 1\n            -deformers 1\n            -dynamics 1\n            -particleInstancers 1\n            -fluids 1\n            -hairSystems 1\n            -follicles 1\n            -nCloths 1\n            -nParticles 1\n            -nRigids 1\n            -dynamicConstraints 1\n            -locators 1\n            -manipulators 1\n            -pluginShapes 1\n            -dimensions 1\n            -handles 1\n            -pivots 1\n            -textures 1\n            -strokes 1\n            -motionTrails 1\n            -clipGhosts 1\n            -greasePencils 1\n            -shadows 0\n            -captureSequenceNumber -1\n            -width 1\n            -height 1\n"
		+ "            -sceneRenderFilter 0\n            $editorName;\n        modelEditor -e -viewSelected 0 $editorName;\n        modelEditor -e \n            -pluginObjects \"gpuCacheDisplayFilter\" 1 \n            $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"modelPanel\" (localizedPanelLabel(\"Front View\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tmodelPanel -edit -l (localizedPanelLabel(\"Front View\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        modelEditor -e \n            -camera \"|front\" \n            -useInteractiveMode 0\n            -displayLights \"default\" \n            -displayAppearance \"smoothShaded\" \n            -activeOnly 0\n            -ignorePanZoom 0\n            -wireframeOnShaded 0\n            -headsUpDisplay 1\n            -holdOuts 1\n            -selectionHiliteDisplay 1\n            -useDefaultMaterial 0\n            -bufferMode \"double\" \n            -twoSidedLighting 0\n            -backfaceCulling 0\n"
		+ "            -xray 0\n            -jointXray 0\n            -activeComponentsXray 0\n            -displayTextures 0\n            -smoothWireframe 0\n            -lineWidth 1\n            -textureAnisotropic 0\n            -textureHilight 1\n            -textureSampling 2\n            -textureDisplay \"modulate\" \n            -textureMaxSize 32768\n            -fogging 0\n            -fogSource \"fragment\" \n            -fogMode \"linear\" \n            -fogStart 0\n            -fogEnd 100\n            -fogDensity 0.1\n            -fogColor 0.5 0.5 0.5 1 \n            -depthOfFieldPreview 1\n            -maxConstantTransparency 1\n            -rendererName \"vp2Renderer\" \n            -objectFilterShowInHUD 1\n            -isFiltered 0\n            -colorResolution 256 256 \n            -bumpResolution 512 512 \n            -textureCompression 0\n            -transparencyAlgorithm \"frontAndBackCull\" \n            -transpInShadows 0\n            -cullingOverride \"none\" \n            -lowQualityLighting 0\n            -maximumNumHardwareLights 1\n            -occlusionCulling 0\n"
		+ "            -shadingModel 0\n            -useBaseRenderer 0\n            -useReducedRenderer 0\n            -smallObjectCulling 0\n            -smallObjectThreshold -1 \n            -interactiveDisableShadows 0\n            -interactiveBackFaceCull 0\n            -sortTransparent 1\n            -controllers 1\n            -nurbsCurves 1\n            -nurbsSurfaces 1\n            -polymeshes 1\n            -subdivSurfaces 1\n            -planes 1\n            -lights 1\n            -cameras 1\n            -controlVertices 1\n            -hulls 1\n            -grid 1\n            -imagePlane 1\n            -joints 1\n            -ikHandles 1\n            -deformers 1\n            -dynamics 1\n            -particleInstancers 1\n            -fluids 1\n            -hairSystems 1\n            -follicles 1\n            -nCloths 1\n            -nParticles 1\n            -nRigids 1\n            -dynamicConstraints 1\n            -locators 1\n            -manipulators 1\n            -pluginShapes 1\n            -dimensions 1\n            -handles 1\n            -pivots 1\n"
		+ "            -textures 1\n            -strokes 1\n            -motionTrails 1\n            -clipGhosts 1\n            -greasePencils 1\n            -shadows 0\n            -captureSequenceNumber -1\n            -width 1\n            -height 1\n            -sceneRenderFilter 0\n            $editorName;\n        modelEditor -e -viewSelected 0 $editorName;\n        modelEditor -e \n            -pluginObjects \"gpuCacheDisplayFilter\" 1 \n            $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"modelPanel\" (localizedPanelLabel(\"Persp View\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tmodelPanel -edit -l (localizedPanelLabel(\"Persp View\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        modelEditor -e \n            -camera \"|persp\" \n            -useInteractiveMode 0\n            -displayLights \"default\" \n            -displayAppearance \"smoothShaded\" \n            -activeOnly 0\n            -ignorePanZoom 0\n"
		+ "            -wireframeOnShaded 0\n            -headsUpDisplay 1\n            -holdOuts 1\n            -selectionHiliteDisplay 1\n            -useDefaultMaterial 0\n            -bufferMode \"double\" \n            -twoSidedLighting 0\n            -backfaceCulling 0\n            -xray 0\n            -jointXray 0\n            -activeComponentsXray 0\n            -displayTextures 0\n            -smoothWireframe 0\n            -lineWidth 1\n            -textureAnisotropic 0\n            -textureHilight 1\n            -textureSampling 2\n            -textureDisplay \"modulate\" \n            -textureMaxSize 32768\n            -fogging 0\n            -fogSource \"fragment\" \n            -fogMode \"linear\" \n            -fogStart 0\n            -fogEnd 100\n            -fogDensity 0.1\n            -fogColor 0.5 0.5 0.5 1 \n            -depthOfFieldPreview 1\n            -maxConstantTransparency 1\n            -rendererName \"vp2Renderer\" \n            -objectFilterShowInHUD 1\n            -isFiltered 0\n            -colorResolution 256 256 \n            -bumpResolution 512 512 \n"
		+ "            -textureCompression 0\n            -transparencyAlgorithm \"frontAndBackCull\" \n            -transpInShadows 0\n            -cullingOverride \"none\" \n            -lowQualityLighting 0\n            -maximumNumHardwareLights 1\n            -occlusionCulling 0\n            -shadingModel 0\n            -useBaseRenderer 0\n            -useReducedRenderer 0\n            -smallObjectCulling 0\n            -smallObjectThreshold -1 \n            -interactiveDisableShadows 0\n            -interactiveBackFaceCull 0\n            -sortTransparent 1\n            -controllers 1\n            -nurbsCurves 1\n            -nurbsSurfaces 1\n            -polymeshes 1\n            -subdivSurfaces 1\n            -planes 1\n            -lights 1\n            -cameras 1\n            -controlVertices 1\n            -hulls 1\n            -grid 1\n            -imagePlane 1\n            -joints 1\n            -ikHandles 1\n            -deformers 1\n            -dynamics 1\n            -particleInstancers 1\n            -fluids 1\n            -hairSystems 1\n            -follicles 1\n"
		+ "            -nCloths 1\n            -nParticles 1\n            -nRigids 1\n            -dynamicConstraints 1\n            -locators 1\n            -manipulators 1\n            -pluginShapes 1\n            -dimensions 1\n            -handles 1\n            -pivots 1\n            -textures 1\n            -strokes 1\n            -motionTrails 1\n            -clipGhosts 1\n            -greasePencils 1\n            -shadows 0\n            -captureSequenceNumber -1\n            -width 952\n            -height 726\n            -sceneRenderFilter 0\n            $editorName;\n        modelEditor -e -viewSelected 0 $editorName;\n        modelEditor -e \n            -pluginObjects \"gpuCacheDisplayFilter\" 1 \n            $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"outlinerPanel\" (localizedPanelLabel(\"ToggledOutliner\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\toutlinerPanel -edit -l (localizedPanelLabel(\"ToggledOutliner\")) -mbv $menusOkayInPanels  $panelName;\n"
		+ "\t\t$editorName = $panelName;\n        outlinerEditor -e \n            -docTag \"isolOutln_fromSeln\" \n            -showShapes 0\n            -showAssignedMaterials 0\n            -showTimeEditor 1\n            -showReferenceNodes 1\n            -showReferenceMembers 1\n            -showAttributes 0\n            -showConnected 0\n            -showAnimCurvesOnly 0\n            -showMuteInfo 0\n            -organizeByLayer 1\n            -organizeByClip 1\n            -showAnimLayerWeight 1\n            -autoExpandLayers 1\n            -autoExpand 0\n            -showDagOnly 1\n            -showAssets 1\n            -showContainedOnly 1\n            -showPublishedAsConnected 0\n            -showParentContainers 0\n            -showContainerContents 1\n            -ignoreDagHierarchy 0\n            -expandConnections 0\n            -showUpstreamCurves 1\n            -showUnitlessCurves 1\n            -showCompounds 1\n            -showLeafs 1\n            -showNumericAttrsOnly 0\n            -highlightActive 1\n            -autoSelectNewObjects 0\n"
		+ "            -doNotSelectNewObjects 0\n            -dropIsParent 1\n            -transmitFilters 0\n            -setFilter \"defaultSetFilter\" \n            -showSetMembers 1\n            -allowMultiSelection 1\n            -alwaysToggleSelect 0\n            -directSelect 0\n            -isSet 0\n            -isSetMember 0\n            -displayMode \"DAG\" \n            -expandObjects 0\n            -setsIgnoreFilters 1\n            -containersIgnoreFilters 0\n            -editAttrName 0\n            -showAttrValues 0\n            -highlightSecondary 0\n            -showUVAttrsOnly 0\n            -showTextureNodesOnly 0\n            -attrAlphaOrder \"default\" \n            -animLayerFilterOptions \"allAffecting\" \n            -sortOrder \"none\" \n            -longNames 0\n            -niceNames 1\n            -selectCommand \"print(\\\"\\\")\" \n            -showNamespace 1\n            -showPinIcons 0\n            -mapMotionTrails 0\n            -ignoreHiddenAttribute 0\n            -ignoreOutlinerColor 0\n            -renderFilterVisible 0\n            -renderFilterIndex 0\n"
		+ "            -selectionOrder \"chronological\" \n            -expandAttribute 0\n            $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"outlinerPanel\" (localizedPanelLabel(\"Outliner\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\toutlinerPanel -edit -l (localizedPanelLabel(\"Outliner\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        outlinerEditor -e \n            -showShapes 0\n            -showAssignedMaterials 0\n            -showTimeEditor 1\n            -showReferenceNodes 0\n            -showReferenceMembers 0\n            -showAttributes 0\n            -showConnected 0\n            -showAnimCurvesOnly 0\n            -showMuteInfo 0\n            -organizeByLayer 1\n            -organizeByClip 1\n            -showAnimLayerWeight 1\n            -autoExpandLayers 1\n            -autoExpand 0\n            -showDagOnly 1\n            -showAssets 1\n            -showContainedOnly 1\n            -showPublishedAsConnected 0\n"
		+ "            -showParentContainers 0\n            -showContainerContents 1\n            -ignoreDagHierarchy 0\n            -expandConnections 0\n            -showUpstreamCurves 1\n            -showUnitlessCurves 1\n            -showCompounds 1\n            -showLeafs 1\n            -showNumericAttrsOnly 0\n            -highlightActive 1\n            -autoSelectNewObjects 0\n            -doNotSelectNewObjects 0\n            -dropIsParent 1\n            -transmitFilters 0\n            -setFilter \"defaultSetFilter\" \n            -showSetMembers 1\n            -allowMultiSelection 1\n            -alwaysToggleSelect 0\n            -directSelect 0\n            -displayMode \"DAG\" \n            -expandObjects 0\n            -setsIgnoreFilters 1\n            -containersIgnoreFilters 0\n            -editAttrName 0\n            -showAttrValues 0\n            -highlightSecondary 0\n            -showUVAttrsOnly 0\n            -showTextureNodesOnly 0\n            -attrAlphaOrder \"default\" \n            -animLayerFilterOptions \"allAffecting\" \n            -sortOrder \"none\" \n"
		+ "            -longNames 0\n            -niceNames 1\n            -showNamespace 1\n            -showPinIcons 0\n            -mapMotionTrails 0\n            -ignoreHiddenAttribute 0\n            -ignoreOutlinerColor 0\n            -renderFilterVisible 0\n            $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"graphEditor\" (localizedPanelLabel(\"Graph Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Graph Editor\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = ($panelName+\"OutlineEd\");\n            outlinerEditor -e \n                -showShapes 1\n                -showAssignedMaterials 0\n                -showTimeEditor 1\n                -showReferenceNodes 0\n                -showReferenceMembers 0\n                -showAttributes 1\n                -showConnected 1\n                -showAnimCurvesOnly 1\n                -showMuteInfo 0\n                -organizeByLayer 1\n"
		+ "                -organizeByClip 1\n                -showAnimLayerWeight 1\n                -autoExpandLayers 1\n                -autoExpand 1\n                -showDagOnly 0\n                -showAssets 1\n                -showContainedOnly 0\n                -showPublishedAsConnected 0\n                -showParentContainers 0\n                -showContainerContents 0\n                -ignoreDagHierarchy 0\n                -expandConnections 1\n                -showUpstreamCurves 1\n                -showUnitlessCurves 1\n                -showCompounds 0\n                -showLeafs 1\n                -showNumericAttrsOnly 1\n                -highlightActive 0\n                -autoSelectNewObjects 1\n                -doNotSelectNewObjects 0\n                -dropIsParent 1\n                -transmitFilters 1\n                -setFilter \"0\" \n                -showSetMembers 0\n                -allowMultiSelection 1\n                -alwaysToggleSelect 0\n                -directSelect 0\n                -displayMode \"DAG\" \n                -expandObjects 0\n"
		+ "                -setsIgnoreFilters 1\n                -containersIgnoreFilters 0\n                -editAttrName 0\n                -showAttrValues 0\n                -highlightSecondary 0\n                -showUVAttrsOnly 0\n                -showTextureNodesOnly 0\n                -attrAlphaOrder \"default\" \n                -animLayerFilterOptions \"allAffecting\" \n                -sortOrder \"none\" \n                -longNames 0\n                -niceNames 1\n                -showNamespace 1\n                -showPinIcons 1\n                -mapMotionTrails 1\n                -ignoreHiddenAttribute 0\n                -ignoreOutlinerColor 0\n                -renderFilterVisible 0\n                $editorName;\n\n\t\t\t$editorName = ($panelName+\"GraphEd\");\n            animCurveEditor -e \n                -displayValues 0\n                -snapTime \"integer\" \n                -snapValue \"none\" \n                -showPlayRangeShades \"on\" \n                -lockPlayRangeShades \"off\" \n                -smoothness \"fine\" \n                -resultSamples 1\n"
		+ "                -resultScreenSamples 0\n                -resultUpdate \"delayed\" \n                -showUpstreamCurves 1\n                -keyMinScale 1\n                -stackedCurvesMin -1\n                -stackedCurvesMax 1\n                -stackedCurvesSpace 0.2\n                -preSelectionHighlight 0\n                -constrainDrag 0\n                -valueLinesToggle 1\n                -highlightAffectedCurves 0\n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"dopeSheetPanel\" (localizedPanelLabel(\"Dope Sheet\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Dope Sheet\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = ($panelName+\"OutlineEd\");\n            outlinerEditor -e \n                -showShapes 1\n                -showAssignedMaterials 0\n                -showTimeEditor 1\n                -showReferenceNodes 0\n                -showReferenceMembers 0\n"
		+ "                -showAttributes 1\n                -showConnected 1\n                -showAnimCurvesOnly 1\n                -showMuteInfo 0\n                -organizeByLayer 1\n                -organizeByClip 1\n                -showAnimLayerWeight 1\n                -autoExpandLayers 1\n                -autoExpand 0\n                -showDagOnly 0\n                -showAssets 1\n                -showContainedOnly 0\n                -showPublishedAsConnected 0\n                -showParentContainers 0\n                -showContainerContents 0\n                -ignoreDagHierarchy 0\n                -expandConnections 1\n                -showUpstreamCurves 1\n                -showUnitlessCurves 0\n                -showCompounds 1\n                -showLeafs 1\n                -showNumericAttrsOnly 1\n                -highlightActive 0\n                -autoSelectNewObjects 0\n                -doNotSelectNewObjects 1\n                -dropIsParent 1\n                -transmitFilters 0\n                -setFilter \"0\" \n                -showSetMembers 0\n"
		+ "                -allowMultiSelection 1\n                -alwaysToggleSelect 0\n                -directSelect 0\n                -displayMode \"DAG\" \n                -expandObjects 0\n                -setsIgnoreFilters 1\n                -containersIgnoreFilters 0\n                -editAttrName 0\n                -showAttrValues 0\n                -highlightSecondary 0\n                -showUVAttrsOnly 0\n                -showTextureNodesOnly 0\n                -attrAlphaOrder \"default\" \n                -animLayerFilterOptions \"allAffecting\" \n                -sortOrder \"none\" \n                -longNames 0\n                -niceNames 1\n                -showNamespace 1\n                -showPinIcons 0\n                -mapMotionTrails 1\n                -ignoreHiddenAttribute 0\n                -ignoreOutlinerColor 0\n                -renderFilterVisible 0\n                $editorName;\n\n\t\t\t$editorName = ($panelName+\"DopeSheetEd\");\n            dopeSheetEditor -e \n                -displayValues 0\n                -snapTime \"integer\" \n"
		+ "                -snapValue \"none\" \n                -outliner \"dopeSheetPanel1OutlineEd\" \n                -showSummary 1\n                -showScene 0\n                -hierarchyBelow 0\n                -showTicks 1\n                -selectionWindow 0 0 0 0 \n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"timeEditorPanel\" (localizedPanelLabel(\"Time Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Time Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"clipEditorPanel\" (localizedPanelLabel(\"Trax Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Trax Editor\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = clipEditorNameFromPanel($panelName);\n"
		+ "            clipEditor -e \n                -displayValues 0\n                -snapTime \"none\" \n                -snapValue \"none\" \n                -initialized 0\n                -manageSequencer 0 \n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"sequenceEditorPanel\" (localizedPanelLabel(\"Camera Sequencer\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Camera Sequencer\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = sequenceEditorNameFromPanel($panelName);\n            clipEditor -e \n                -displayValues 0\n                -snapTime \"none\" \n                -snapValue \"none\" \n                -initialized 0\n                -manageSequencer 1 \n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"hyperGraphPanel\" (localizedPanelLabel(\"Hypergraph Hierarchy\")) `;\n"
		+ "\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Hypergraph Hierarchy\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = ($panelName+\"HyperGraphEd\");\n            hyperGraph -e \n                -graphLayoutStyle \"hierarchicalLayout\" \n                -orientation \"horiz\" \n                -mergeConnections 0\n                -zoom 1\n                -animateTransition 0\n                -showRelationships 1\n                -showShapes 0\n                -showDeformers 0\n                -showExpressions 0\n                -showConstraints 0\n                -showConnectionFromSelected 0\n                -showConnectionToSelected 0\n                -showConstraintLabels 0\n                -showUnderworld 0\n                -showInvisible 0\n                -transitionFrames 1\n                -opaqueContainers 0\n                -freeform 0\n                -imagePosition 0 0 \n                -imageScale 1\n                -imageEnabled 0\n                -graphType \"DAG\" \n"
		+ "                -heatMapDisplay 0\n                -updateSelection 1\n                -updateNodeAdded 1\n                -useDrawOverrideColor 0\n                -limitGraphTraversal -1\n                -range 0 0 \n                -iconSize \"smallIcons\" \n                -showCachedConnections 0\n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"hyperShadePanel\" (localizedPanelLabel(\"Hypershade\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Hypershade\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"visorPanel\" (localizedPanelLabel(\"Visor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Visor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n"
		+ "\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"nodeEditorPanel\" (localizedPanelLabel(\"Node Editor\")) `;\n\tif ($nodeEditorPanelVisible || $nodeEditorWorkspaceControlOpen) {\n\t\tif (\"\" == $panelName) {\n\t\t\tif ($useSceneConfig) {\n\t\t\t\t$panelName = `scriptedPanel -unParent  -type \"nodeEditorPanel\" -l (localizedPanelLabel(\"Node Editor\")) -mbv $menusOkayInPanels `;\n\n\t\t\t$editorName = ($panelName+\"NodeEditorEd\");\n            nodeEditor -e \n                -allAttributes 0\n                -allNodes 0\n                -autoSizeNodes 1\n                -consistentNameSize 1\n                -createNodeCommand \"nodeEdCreateNodeCommand\" \n                -connectNodeOnCreation 0\n                -connectOnDrop 0\n                -copyConnectionsOnPaste 0\n                -connectionStyle \"bezier\" \n                -defaultPinnedState 0\n                -additiveGraphingMode 0\n                -settingsChangedCallback \"nodeEdSyncControls\" \n                -traversalDepthLimit -1\n                -keyPressCommand \"nodeEdKeyPressCommand\" \n"
		+ "                -nodeTitleMode \"name\" \n                -gridSnap 0\n                -gridVisibility 1\n                -crosshairOnEdgeDragging 0\n                -popupMenuScript \"nodeEdBuildPanelMenus\" \n                -showNamespace 1\n                -showShapes 1\n                -showSGShapes 0\n                -showTransforms 1\n                -useAssets 1\n                -syncedSelection 1\n                -extendToShapes 1\n                -editorMode \"default\" \n                -hasWatchpoint 0\n                $editorName;\n\t\t\t}\n\t\t} else {\n\t\t\t$label = `panel -q -label $panelName`;\n\t\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Node Editor\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = ($panelName+\"NodeEditorEd\");\n            nodeEditor -e \n                -allAttributes 0\n                -allNodes 0\n                -autoSizeNodes 1\n                -consistentNameSize 1\n                -createNodeCommand \"nodeEdCreateNodeCommand\" \n                -connectNodeOnCreation 0\n                -connectOnDrop 0\n"
		+ "                -copyConnectionsOnPaste 0\n                -connectionStyle \"bezier\" \n                -defaultPinnedState 0\n                -additiveGraphingMode 0\n                -settingsChangedCallback \"nodeEdSyncControls\" \n                -traversalDepthLimit -1\n                -keyPressCommand \"nodeEdKeyPressCommand\" \n                -nodeTitleMode \"name\" \n                -gridSnap 0\n                -gridVisibility 1\n                -crosshairOnEdgeDragging 0\n                -popupMenuScript \"nodeEdBuildPanelMenus\" \n                -showNamespace 1\n                -showShapes 1\n                -showSGShapes 0\n                -showTransforms 1\n                -useAssets 1\n                -syncedSelection 1\n                -extendToShapes 1\n                -editorMode \"default\" \n                -hasWatchpoint 0\n                $editorName;\n\t\t\tif (!$useSceneConfig) {\n\t\t\t\tpanel -e -l $label $panelName;\n\t\t\t}\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"createNodePanel\" (localizedPanelLabel(\"Create Node\")) `;\n"
		+ "\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Create Node\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"polyTexturePlacementPanel\" (localizedPanelLabel(\"UV Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"UV Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"renderWindowPanel\" (localizedPanelLabel(\"Render View\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Render View\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"shapePanel\" (localizedPanelLabel(\"Shape Editor\")) `;\n"
		+ "\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tshapePanel -edit -l (localizedPanelLabel(\"Shape Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"posePanel\" (localizedPanelLabel(\"Pose Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tposePanel -edit -l (localizedPanelLabel(\"Pose Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"dynRelEdPanel\" (localizedPanelLabel(\"Dynamic Relationships\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Dynamic Relationships\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"relationshipPanel\" (localizedPanelLabel(\"Relationship Editor\")) `;\n"
		+ "\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Relationship Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"referenceEditorPanel\" (localizedPanelLabel(\"Reference Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Reference Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"componentEditorPanel\" (localizedPanelLabel(\"Component Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Component Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"dynPaintScriptedPanelType\" (localizedPanelLabel(\"Paint Effects\")) `;\n"
		+ "\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Paint Effects\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"scriptEditorPanel\" (localizedPanelLabel(\"Script Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Script Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"profilerPanel\" (localizedPanelLabel(\"Profiler Tool\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Profiler Tool\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"contentBrowserPanel\" (localizedPanelLabel(\"Content Browser\")) `;\n"
		+ "\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Content Browser\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"Stereo\" (localizedPanelLabel(\"Stereo\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Stereo\")) -mbv $menusOkayInPanels  $panelName;\n{ string $editorName = ($panelName+\"Editor\");\n            stereoCameraView -e \n                -camera \"|:persp\" \n                -useInteractiveMode 0\n                -displayLights \"default\" \n                -displayAppearance \"wireframe\" \n                -activeOnly 0\n                -ignorePanZoom 0\n                -wireframeOnShaded 0\n                -headsUpDisplay 1\n                -holdOuts 1\n                -selectionHiliteDisplay 1\n                -useDefaultMaterial 0\n                -bufferMode \"double\" \n                -twoSidedLighting 1\n"
		+ "                -backfaceCulling 0\n                -xray 0\n                -jointXray 0\n                -activeComponentsXray 0\n                -displayTextures 0\n                -smoothWireframe 0\n                -lineWidth 1\n                -textureAnisotropic 0\n                -textureHilight 1\n                -textureSampling 2\n                -textureDisplay \"modulate\" \n                -textureMaxSize 32768\n                -fogging 0\n                -fogSource \"fragment\" \n                -fogMode \"linear\" \n                -fogStart 0\n                -fogEnd 100\n                -fogDensity 0.1\n                -fogColor 0.5 0.5 0.5 1 \n                -depthOfFieldPreview 1\n                -maxConstantTransparency 1\n                -objectFilterShowInHUD 1\n                -isFiltered 0\n                -colorResolution 4 4 \n                -bumpResolution 4 4 \n                -textureCompression 0\n                -transparencyAlgorithm \"frontAndBackCull\" \n                -transpInShadows 0\n                -cullingOverride \"none\" \n"
		+ "                -lowQualityLighting 0\n                -maximumNumHardwareLights 0\n                -occlusionCulling 0\n                -shadingModel 0\n                -useBaseRenderer 0\n                -useReducedRenderer 0\n                -smallObjectCulling 0\n                -smallObjectThreshold -1 \n                -interactiveDisableShadows 0\n                -interactiveBackFaceCull 0\n                -sortTransparent 1\n                -controllers 1\n                -nurbsCurves 1\n                -nurbsSurfaces 1\n                -polymeshes 1\n                -subdivSurfaces 1\n                -planes 1\n                -lights 1\n                -cameras 1\n                -controlVertices 1\n                -hulls 1\n                -grid 1\n                -imagePlane 1\n                -joints 1\n                -ikHandles 1\n                -deformers 1\n                -dynamics 1\n                -particleInstancers 1\n                -fluids 1\n                -hairSystems 1\n                -follicles 1\n                -nCloths 1\n"
		+ "                -nParticles 1\n                -nRigids 1\n                -dynamicConstraints 1\n                -locators 1\n                -manipulators 1\n                -pluginShapes 1\n                -dimensions 1\n                -handles 1\n                -pivots 1\n                -textures 1\n                -strokes 1\n                -motionTrails 1\n                -clipGhosts 1\n                -greasePencils 1\n                -shadows 0\n                -captureSequenceNumber -1\n                -width 0\n                -height 0\n                -sceneRenderFilter 0\n                -displayMode \"centerEye\" \n                -viewColor 0 0 0 1 \n                -useCustomBackground 1\n                $editorName;\n            stereoCameraView -e -viewSelected 0 $editorName;\n            stereoCameraView -e \n                -pluginObjects \"gpuCacheDisplayFilter\" 1 \n                $editorName; };\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\tif ($useSceneConfig) {\n        string $configName = `getPanel -cwl (localizedPanelLabel(\"Current Layout\"))`;\n"
		+ "        if (\"\" != $configName) {\n\t\t\tpanelConfiguration -edit -label (localizedPanelLabel(\"Current Layout\")) \n\t\t\t\t-userCreated false\n\t\t\t\t-defaultImage \"vacantCell.xP:/\"\n\t\t\t\t-image \"\"\n\t\t\t\t-sc false\n\t\t\t\t-configString \"global string $gMainPane; paneLayout -e -cn \\\"single\\\" -ps 1 100 100 $gMainPane;\"\n\t\t\t\t-removeAllPanels\n\t\t\t\t-ap false\n\t\t\t\t\t(localizedPanelLabel(\"Persp View\")) \n\t\t\t\t\t\"modelPanel\"\n"
		+ "\t\t\t\t\t\"$panelName = `modelPanel -unParent -l (localizedPanelLabel(\\\"Persp View\\\")) -mbv $menusOkayInPanels `;\\n$editorName = $panelName;\\nmodelEditor -e \\n    -cam `findStartUpCamera persp` \\n    -useInteractiveMode 0\\n    -displayLights \\\"default\\\" \\n    -displayAppearance \\\"smoothShaded\\\" \\n    -activeOnly 0\\n    -ignorePanZoom 0\\n    -wireframeOnShaded 0\\n    -headsUpDisplay 1\\n    -holdOuts 1\\n    -selectionHiliteDisplay 1\\n    -useDefaultMaterial 0\\n    -bufferMode \\\"double\\\" \\n    -twoSidedLighting 0\\n    -backfaceCulling 0\\n    -xray 0\\n    -jointXray 0\\n    -activeComponentsXray 0\\n    -displayTextures 0\\n    -smoothWireframe 0\\n    -lineWidth 1\\n    -textureAnisotropic 0\\n    -textureHilight 1\\n    -textureSampling 2\\n    -textureDisplay \\\"modulate\\\" \\n    -textureMaxSize 32768\\n    -fogging 0\\n    -fogSource \\\"fragment\\\" \\n    -fogMode \\\"linear\\\" \\n    -fogStart 0\\n    -fogEnd 100\\n    -fogDensity 0.1\\n    -fogColor 0.5 0.5 0.5 1 \\n    -depthOfFieldPreview 1\\n    -maxConstantTransparency 1\\n    -rendererName \\\"vp2Renderer\\\" \\n    -objectFilterShowInHUD 1\\n    -isFiltered 0\\n    -colorResolution 256 256 \\n    -bumpResolution 512 512 \\n    -textureCompression 0\\n    -transparencyAlgorithm \\\"frontAndBackCull\\\" \\n    -transpInShadows 0\\n    -cullingOverride \\\"none\\\" \\n    -lowQualityLighting 0\\n    -maximumNumHardwareLights 1\\n    -occlusionCulling 0\\n    -shadingModel 0\\n    -useBaseRenderer 0\\n    -useReducedRenderer 0\\n    -smallObjectCulling 0\\n    -smallObjectThreshold -1 \\n    -interactiveDisableShadows 0\\n    -interactiveBackFaceCull 0\\n    -sortTransparent 1\\n    -controllers 1\\n    -nurbsCurves 1\\n    -nurbsSurfaces 1\\n    -polymeshes 1\\n    -subdivSurfaces 1\\n    -planes 1\\n    -lights 1\\n    -cameras 1\\n    -controlVertices 1\\n    -hulls 1\\n    -grid 1\\n    -imagePlane 1\\n    -joints 1\\n    -ikHandles 1\\n    -deformers 1\\n    -dynamics 1\\n    -particleInstancers 1\\n    -fluids 1\\n    -hairSystems 1\\n    -follicles 1\\n    -nCloths 1\\n    -nParticles 1\\n    -nRigids 1\\n    -dynamicConstraints 1\\n    -locators 1\\n    -manipulators 1\\n    -pluginShapes 1\\n    -dimensions 1\\n    -handles 1\\n    -pivots 1\\n    -textures 1\\n    -strokes 1\\n    -motionTrails 1\\n    -clipGhosts 1\\n    -greasePencils 1\\n    -shadows 0\\n    -captureSequenceNumber -1\\n    -width 952\\n    -height 726\\n    -sceneRenderFilter 0\\n    $editorName;\\nmodelEditor -e -viewSelected 0 $editorName;\\nmodelEditor -e \\n    -pluginObjects \\\"gpuCacheDisplayFilter\\\" 1 \\n    $editorName\"\n"
		+ "\t\t\t\t\t\"modelPanel -edit -l (localizedPanelLabel(\\\"Persp View\\\")) -mbv $menusOkayInPanels  $panelName;\\n$editorName = $panelName;\\nmodelEditor -e \\n    -cam `findStartUpCamera persp` \\n    -useInteractiveMode 0\\n    -displayLights \\\"default\\\" \\n    -displayAppearance \\\"smoothShaded\\\" \\n    -activeOnly 0\\n    -ignorePanZoom 0\\n    -wireframeOnShaded 0\\n    -headsUpDisplay 1\\n    -holdOuts 1\\n    -selectionHiliteDisplay 1\\n    -useDefaultMaterial 0\\n    -bufferMode \\\"double\\\" \\n    -twoSidedLighting 0\\n    -backfaceCulling 0\\n    -xray 0\\n    -jointXray 0\\n    -activeComponentsXray 0\\n    -displayTextures 0\\n    -smoothWireframe 0\\n    -lineWidth 1\\n    -textureAnisotropic 0\\n    -textureHilight 1\\n    -textureSampling 2\\n    -textureDisplay \\\"modulate\\\" \\n    -textureMaxSize 32768\\n    -fogging 0\\n    -fogSource \\\"fragment\\\" \\n    -fogMode \\\"linear\\\" \\n    -fogStart 0\\n    -fogEnd 100\\n    -fogDensity 0.1\\n    -fogColor 0.5 0.5 0.5 1 \\n    -depthOfFieldPreview 1\\n    -maxConstantTransparency 1\\n    -rendererName \\\"vp2Renderer\\\" \\n    -objectFilterShowInHUD 1\\n    -isFiltered 0\\n    -colorResolution 256 256 \\n    -bumpResolution 512 512 \\n    -textureCompression 0\\n    -transparencyAlgorithm \\\"frontAndBackCull\\\" \\n    -transpInShadows 0\\n    -cullingOverride \\\"none\\\" \\n    -lowQualityLighting 0\\n    -maximumNumHardwareLights 1\\n    -occlusionCulling 0\\n    -shadingModel 0\\n    -useBaseRenderer 0\\n    -useReducedRenderer 0\\n    -smallObjectCulling 0\\n    -smallObjectThreshold -1 \\n    -interactiveDisableShadows 0\\n    -interactiveBackFaceCull 0\\n    -sortTransparent 1\\n    -controllers 1\\n    -nurbsCurves 1\\n    -nurbsSurfaces 1\\n    -polymeshes 1\\n    -subdivSurfaces 1\\n    -planes 1\\n    -lights 1\\n    -cameras 1\\n    -controlVertices 1\\n    -hulls 1\\n    -grid 1\\n    -imagePlane 1\\n    -joints 1\\n    -ikHandles 1\\n    -deformers 1\\n    -dynamics 1\\n    -particleInstancers 1\\n    -fluids 1\\n    -hairSystems 1\\n    -follicles 1\\n    -nCloths 1\\n    -nParticles 1\\n    -nRigids 1\\n    -dynamicConstraints 1\\n    -locators 1\\n    -manipulators 1\\n    -pluginShapes 1\\n    -dimensions 1\\n    -handles 1\\n    -pivots 1\\n    -textures 1\\n    -strokes 1\\n    -motionTrails 1\\n    -clipGhosts 1\\n    -greasePencils 1\\n    -shadows 0\\n    -captureSequenceNumber -1\\n    -width 952\\n    -height 726\\n    -sceneRenderFilter 0\\n    $editorName;\\nmodelEditor -e -viewSelected 0 $editorName;\\nmodelEditor -e \\n    -pluginObjects \\\"gpuCacheDisplayFilter\\\" 1 \\n    $editorName\"\n"
		+ "\t\t\t\t$configName;\n\n            setNamedPanelLayout (localizedPanelLabel(\"Current Layout\"));\n        }\n\n        panelHistory -e -clear mainPanelHistory;\n        sceneUIReplacement -clear;\n\t}\n\n\ngrid -spacing 5 -size 12 -divisions 5 -displayAxes yes -displayGridLines yes -displayDivisionLines yes -displayPerspectiveLabels no -displayOrthographicLabels no -displayAxesBold yes -perspectiveLabelPosition axis -orthographicLabelPosition edge;\nviewManip -drawCompass 0 -compassAngle 0 -frontParameters \"\" -homeParameters \"\" -selectionLockParameters \"\";\n}\n");
	setAttr ".st" 3;
createNode script -n "sceneConfigurationScriptNode";
	rename -uid "45E073A4-4A76-E124-9629-8884330B7762";
	setAttr ".b" -type "string" "playbackOptions -min 1 -max 120 -ast 1 -aet 200 ";
	setAttr ".st" 6;
select -ne :time1;
	setAttr ".o" 1;
	setAttr ".unw" 1;
select -ne :hardwareRenderingGlobals;
	setAttr ".otfna" -type "stringArray" 22 "NURBS Curves" "NURBS Surfaces" "Polygons" "Subdiv Surface" "Particles" "Particle Instance" "Fluids" "Strokes" "Image Planes" "UI" "Lights" "Cameras" "Locators" "Joints" "IK Handles" "Deformers" "Motion Trails" "Components" "Hair Systems" "Follicles" "Misc. UI" "Ornaments"  ;
	setAttr ".otfva" -type "Int32Array" 22 0 1 1 1 1 1
		 1 1 1 0 0 0 0 0 0 0 0 0
		 0 0 0 0 ;
	setAttr ".fprt" yes;
select -ne :renderPartition;
	setAttr -s 2 ".st";
select -ne :renderGlobalsList1;
select -ne :defaultShaderList1;
	setAttr -s 5 ".s";
select -ne :postProcessList1;
	setAttr -s 2 ".p";
select -ne :defaultRenderingList1;
select -ne :initialShadingGroup;
	setAttr ".ro" yes;
select -ne :initialParticleSE;
	setAttr ".ro" yes;
select -ne :defaultRenderGlobals;
	addAttr -ci true -h true -sn "dss" -ln "defaultSurfaceShader" -dt "string";
	setAttr ".ren" -type "string" "arnold";
	setAttr ".dss" -type "string" "lambert1";
select -ne :defaultResolution;
	setAttr ".pa" 1;
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
select -ne :ikSystem;
	setAttr -s 4 ".sol";
connectAttr "Hips_Skl.s" "LeftUpLeg_Skl.is";
connectAttr "LeftUpLeg_Skl.s" "LeftLeg_Skl.is";
connectAttr "LeftLeg_Skl.s" "LeftFoot_Skl.is";
connectAttr "LeftFoot_Skl.s" "LeftToeBase_Skl.is";
connectAttr "LeftToeBase_Skl.s" "LeftToeEnd_Skl.is";
connectAttr "Hips_Skl.s" "Spine_Skl.is";
connectAttr "Spine_Skl.s" "Spine1_Skl.is";
connectAttr "Spine1_Skl.s" "Spine2_Skl.is";
connectAttr "Spine2_Skl.s" "LeftShoulder_Skl.is";
connectAttr "LeftShoulder_Skl.s" "LeftArm_Skl.is";
connectAttr "LeftArm_Skl.s" "LeftArm_Roll_Skl.is";
connectAttr "LeftArm_Roll_Skl.s" "LeftForeArm_Skl.is";
connectAttr "LeftForeArm_Skl.s" "LeftForeArm_Roll_Skl.is";
connectAttr "LeftForeArm_Roll_Skl.s" "LeftHand_Skl.is";
connectAttr "LeftHand_Skl.s" "LeftHandThumb1_Skl.is";
connectAttr "LeftHandThumb1_Skl.s" "LeftHandThumb2_Skl.is";
connectAttr "LeftHandThumb2_Skl.s" "LeftHandThumb3_Skl.is";
connectAttr "LeftHandThumb3_Skl.s" "LeftHandThumb4_Skl.is";
connectAttr "LeftHand_Skl.s" "LeftHandIndex1_Skl.is";
connectAttr "LeftHandIndex1_Skl.s" "LeftHandIndex2_Skl.is";
connectAttr "LeftHandIndex2_Skl.s" "LeftHandIndex3_Skl.is";
connectAttr "LeftHandIndex3_Skl.s" "LeftHandIndex4_Skl.is";
connectAttr "LeftHand_Skl.s" "LeftHandMiddle1_Skl.is";
connectAttr "LeftHandMiddle1_Skl.s" "LeftHandMiddle2_Skl.is";
connectAttr "LeftHandMiddle2_Skl.s" "LeftHandMiddle3_Skl.is";
connectAttr "LeftHandMiddle3_Skl.s" "LeftHandMiddle4_Skl.is";
connectAttr "LeftHand_Skl.s" "LeftHandRing1_Skl.is";
connectAttr "LeftHandRing1_Skl.s" "LeftHandRing2_Skl.is";
connectAttr "LeftHandRing2_Skl.s" "LeftHandRing3_Skl.is";
connectAttr "LeftHandRing3_Skl.s" "LeftHandRing4_Skl.is";
connectAttr "LeftHand_Skl.s" "LeftHandPinky1_Skl.is";
connectAttr "LeftHandPinky1_Skl.s" "LeftHandPinky2_Skl.is";
connectAttr "LeftHandPinky2_Skl.s" "LeftHandPinky3_Skl.is";
connectAttr "LeftHandPinky3_Skl.s" "LeftHandPinky4_Skl.is";
connectAttr "Spine2_Skl.s" "Neck_Skl.is";
connectAttr "Neck_Skl.s" "Neck1_Skl.is";
connectAttr "Neck1_Skl.s" "Head_Skl.is";
connectAttr "Head_Skl.s" "Head_End_Skl.is";
connectAttr "Head_Skl.s" "LeftEye_Skl.is";
connectAttr "Head_Skl.s" "RightEye_Skl.is";
connectAttr "Head_Skl.s" "Jaw_Skl.is";
connectAttr "Spine2_Skl.s" "RightShoulder_Skl.is";
connectAttr "RightShoulder_Skl.s" "RightArm_Skl.is";
connectAttr "RightArm_Skl.s" "RightArm_Roll_Skl.is";
connectAttr "RightArm_Roll_Skl.s" "RightForeArm_Skl.is";
connectAttr "RightForeArm_Skl.s" "RightForeArm_Roll_Skl.is";
connectAttr "RightForeArm_Roll_Skl.s" "RightHand_Skl.is";
connectAttr "RightHand_Skl.s" "RightHandThumb1_Skl.is";
connectAttr "RightHandThumb1_Skl.s" "RightHandThumb2_Skl.is";
connectAttr "RightHandThumb2_Skl.s" "RightHandThumb3_Skl.is";
connectAttr "RightHandThumb3_Skl.s" "RightHandThumb4_Skl.is";
connectAttr "RightHand_Skl.s" "RightHandIndex1_Skl.is";
connectAttr "RightHandIndex1_Skl.s" "RightHandIndex2_Skl.is";
connectAttr "RightHandIndex2_Skl.s" "RightHandIndex3_Skl.is";
connectAttr "RightHandIndex3_Skl.s" "RightHandIndex4_Skl.is";
connectAttr "RightHand_Skl.s" "RightHandMiddle1_Skl.is";
connectAttr "RightHandMiddle1_Skl.s" "RightHandMiddle2_Skl.is";
connectAttr "RightHandMiddle2_Skl.s" "RightHandMiddle3_Skl.is";
connectAttr "RightHandMiddle3_Skl.s" "RightHandMiddle4_Skl.is";
connectAttr "RightHand_Skl.s" "RightHandRing1_Skl.is";
connectAttr "RightHandRing1_Skl.s" "RightHandRing2_Skl.is";
connectAttr "RightHandRing2_Skl.s" "RightHandRing3_Skl.is";
connectAttr "RightHandRing3_Skl.s" "RightHandRing4_Skl.is";
connectAttr "RightHand_Skl.s" "RightHandPinky1_Skl.is";
connectAttr "RightHandPinky1_Skl.s" "RightHandPinky2_Skl.is";
connectAttr "RightHandPinky2_Skl.s" "RightHandPinky3_Skl.is";
connectAttr "RightHandPinky3_Skl.s" "RightHandPinky4_Skl.is";
connectAttr "Hips_Skl.s" "RightUpLeg_Skl.is";
connectAttr "RightUpLeg_Skl.s" "RightLeg_Skl.is";
connectAttr "RightLeg_Skl.s" "RightFoot_Skl.is";
connectAttr "RightFoot_Skl.s" "RightToeBase_Skl.is";
connectAttr "RightToeBase_Skl.s" "RightToeEnd_Skl.is";
connectAttr "Hips_Skl.s" "SpineHolder_Skl.is";
relationship "link" ":lightLinker1" ":initialShadingGroup.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" ":initialParticleSE.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" ":initialShadingGroup.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" ":initialParticleSE.message" ":defaultLightSet.message";
connectAttr "layerManager.dli[0]" "defaultLayer.id";
connectAttr "renderLayerManager.rlmi[0]" "defaultRenderLayer.rlid";
connectAttr "defaultRenderLayer.msg" ":defaultRenderingList1.r" -na;
// End of atoms_skeleton.ma
