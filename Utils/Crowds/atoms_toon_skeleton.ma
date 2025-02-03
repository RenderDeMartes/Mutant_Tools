//Maya ASCII 2022 scene
//Name: atoms_toon_skeleton.ma
//Last modified: Mon, Dec 12, 2022 05:43:18 PM
//Codeset: UTF-8
requires maya "2022";
requires "stereoCamera" "10.0";
requires "mtoa" "4.2.1";
currentUnit -l centimeter -a degree -t film;
fileInfo "application" "maya";
fileInfo "product" "Maya 2022";
fileInfo "version" "2022";
fileInfo "cutIdentifier" "202102181415-29bfc1879c";
fileInfo "osv" "Mac OS X 10.16";
fileInfo "UUID" "4B81E1F2-BC44-6B0D-B33E-DB867294259A";
createNode joint -n "Hips_Skl";
	rename -uid "4EA5BF7B-A144-723D-9035-269B4FA07A85";
	addAttr -ci true -h true -sn "fbxID" -ln "filmboxTypeID" -at "short";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".t" -type "double3" 1.2542994396339689e-16 7.5492410507428351 -3.7297768838731394e-31 ;
	setAttr ".r" -type "double3" -3.1780125345961146e-30 -6.3611093629270335e-15 5.7249984266343308e-14 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 1.2542994396339689e-16 7.5492410507428351 -3.7297768838731394e-31 1;
	setAttr ".radi" 2;
	setAttr ".fbxID" 5;
createNode joint -n "LeftUpLeg_Skl" -p "Hips_Skl";
	rename -uid "722BB82C-8D46-855B-8D34-AFA2D0F24A77";
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
	setAttr ".uoc" 1;
	setAttr ".t" -type "double3" 0.59764748811721868 -1.0566100921857062 -0.21729375422000954 ;
	setAttr ".r" -type "double3" 3.1805546814635176e-15 -5.9635400277440979e-16 1.2660098517231735e-14 ;
	setAttr ".jo" -type "double3" 1.9900564001699187e-16 -2.7003134116908614 -86 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.069679017360488316 -0.99645637236797791 0.047111914702400511 0
		 0.99756405025982409 0.069756473744125413 3.4694469519536142e-18 0 -0.0032863610409734761 0.046997152446022011 0.99888961727163517 0
		 0.59764748811721879 6.4926309585571289 -0.21729375422000954 1;
	setAttr ".radi" 2;
	setAttr -k on ".atoms_poleVector" -type "double3" 10.295197723822556 -7.7403593063354492 
		23.603414965967094 ;
	setAttr ".fbxID" 5;
createNode joint -n "LeftUpLeg_Roll_01_Skl" -p "LeftUpLeg_Skl";
	rename -uid "495A6251-AD41-6AD2-48B4-5BA90F48C5A1";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 1;
	setAttr ".t" -type "double3" 0.61447802312155453 -0.042973779649674748 -0.016088567542895713 ;
	setAttr ".r" -type "double3" 3.1805546814635176e-15 9.3428793767990835e-15 -2.1742073017816986e-16 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 2.6937452844728025 0.18829495654125949 86.004427137230607 ;
	setAttr ".bps" -type "matrix" 0.99999999999999989 -1.214306433183765e-17 1.7347234759768071e-18 0
		 -1.1980434005964824e-17 0.99999999999999978 0 0 2.1684043449710089e-18 -6.9388939039072284e-18 1 0
		 0.59764748811721946 5.8765766005443085 -0.20441522108357912 1;
	setAttr ".radi" 2;
createNode joint -n "LeftUpLeg_Roll_02_Skl" -p "LeftUpLeg_Roll_01_Skl";
	rename -uid "B2A69277-6A48-8FAD-475E-45AB8C406DB7";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 2;
	setAttr ".t" -type "double3" 7.7715611723760958e-16 -0.61605435801282393 0.012878533136430531 ;
	setAttr ".r" -type "double3" -9.5416640443905503e-15 3.1805546814635168e-15 -3.1805546814635176e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.99999999999999989 -1.214306433183765e-17 1.7347234759768071e-18 0
		 -1.1980434005964824e-17 0.99999999999999978 0 0 2.1684043449710089e-18 -6.9388939039072284e-18 1 0
		 0.59764748811722024 5.2605222425314846 -0.19153668794714859 1;
	setAttr ".radi" 2;
createNode joint -n "LeftUpLeg_Roll_03_Skl" -p "LeftUpLeg_Roll_02_Skl";
	rename -uid "B2E44002-4242-E8CE-976E-80AB9F15DD57";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 3;
	setAttr ".t" -type "double3" 6.6613381477509392e-16 -0.61605435801282482 0.012878533136430448 ;
	setAttr ".r" -type "double3" 3.1805546814635176e-15 9.5416640443905503e-15 3.1805546814635176e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.99999999999999989 -1.214306433183765e-17 1.7347234759768071e-18 0
		 -1.1980434005964824e-17 0.99999999999999978 0 0 2.1684043449710089e-18 -6.9388939039072284e-18 1 0
		 0.5976474881172209 4.6444678845186598 -0.17865815481071814 1;
	setAttr ".radi" 2;
createNode joint -n "LeftUpLeg_Roll_04_Skl" -p "LeftUpLeg_Roll_03_Skl";
	rename -uid "1674A29C-F14B-7767-1A29-A29FA9665FF0";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 4;
	setAttr ".t" -type "double3" 7.7715611723760958e-16 -0.61605435801282304 0.012878533136430531 ;
	setAttr ".r" -type "double3" -9.5416640443905487e-15 1.5902773407317584e-14 9.5416640443905487e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.99999999999999989 -1.214306433183765e-17 1.7347234759768071e-18 0
		 -1.1980434005964824e-17 0.99999999999999978 0 0 2.1684043449710089e-18 -6.9388939039072284e-18 1 0
		 0.59764748811722168 4.0284135265058367 -0.16577962167428761 1;
	setAttr ".radi" 2;
createNode joint -n "LeftLeg_Skl" -p "LeftUpLeg_Roll_04_Skl";
	rename -uid "F11CB8E8-404A-AA93-E95F-21A8977560FC";
	addAttr -ci true -h true -sn "fbxID" -ln "filmboxTypeID" -at "short";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 5;
	setAttr ".t" -type "double3" 7.7715611723760958e-16 -0.61605435801282438 0.012878533136430448 ;
	setAttr ".r" -type "double3" -1.9679682091555514e-14 -7.9513867036587623e-16 1.8642274607562532e-14 ;
	setAttr ".jo" -type "double3" 9.9737017136286955e-17 2.5986865883091368 -86 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.069684736842257622 -0.99653816476791979 -0.045340088356895021 0
		 0.99756405025982398 0.069756473744125608 1.7304977767762243e-18 0 0.003162764683024078 -0.045229642180442502 0.99897160940028173 0
		 0.59764748811722246 3.4123591684930124 -0.15290108853785717 1;
	setAttr ".radi" 2;
	setAttr ".fbxID" 5;
createNode joint -n "LeftLeg_Roll_01_Skl" -p "LeftLeg_Skl";
	rename -uid "04003661-7344-255B-20F5-6782913E4BCD";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 6;
	setAttr ".t" -type "double3" 0.57538669741801307 -0.040225148621096385 0.0099560389643784664 ;
	setAttr ".r" -type "double3" -3.5781240166464568e-15 1.311978806103701e-14 1.3032819768965741e-14 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" -2.5923649646626115 -0.1812133700464873 86.004100229929861 ;
	setAttr ".bps" -type "matrix" 0.99999999999999978 -6.965998958219366e-17 -8.6736173798840355e-19 0
		 1.5268277094027116e-16 0.99999999999999978 0 0 -7.3725747729014302e-18 -1.3877787807814457e-17 1 0
		 0.5976474851369874 2.8357080924126574 -0.16904337197067493 1;
	setAttr ".radi" 2;
createNode joint -n "LeftLeg_Roll_02_Skl" -p "LeftLeg_Roll_01_Skl";
	rename -uid "1E0A0E20-094B-028D-E4F9-2D95367056A7";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 7;
	setAttr ".t" -type "double3" -2.9802349477137113e-09 -0.5766510760803536 -0.016142283432817844 ;
	setAttr ".r" -type "double3" -3.1805546814635176e-15 1.2722218725854067e-14 -3.1805546814635176e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.99999999999999978 -6.965998958219366e-17 -8.6736173798840355e-19 0
		 1.5268277094027116e-16 0.99999999999999978 0 0 -7.3725747729014302e-18 -1.3877787807814457e-17 1 0
		 0.59764748215675223 2.2590570163323025 -0.18518565540349266 1;
	setAttr ".radi" 2;
createNode joint -n "LeftLeg_Roll_03_Skl" -p "LeftLeg_Roll_02_Skl";
	rename -uid "AFA425D9-984E-EC6F-4458-94AAC67EEEC1";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".t" -type "double3" -2.9802350587360138e-09 -0.57665107608035493 -0.016142283432817678 ;
	setAttr ".r" -type "double3" -3.1805546814635176e-15 1.2722218725854067e-14 -3.1805546814635176e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.99999999999999978 -6.965998958219366e-17 -8.6736173798840355e-19 0
		 1.5268277094027116e-16 0.99999999999999978 0 0 -7.3725747729014302e-18 -1.3877787807814457e-17 1 0
		 0.59764747917651695 1.682405940251948 -0.20132793883631034 1;
	setAttr ".radi" 2;
createNode joint -n "LeftLeg_Roll_04_Skl" -p "LeftLeg_Roll_03_Skl";
	rename -uid "0F2E9405-B742-EDAF-85D8-B49EFC228C69";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".t" -type "double3" -2.9802350587360138e-09 -0.57665107608035515 -0.016142283432817622 ;
	setAttr ".r" -type "double3" -9.5416640443905503e-15 1.2722218725854067e-14 -3.1805546814635183e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.99999999999999978 -6.965998958219366e-17 -8.6736173798840355e-19 0
		 1.5268277094027116e-16 0.99999999999999978 0 0 -7.3725747729014302e-18 -1.3877787807814457e-17 1 0
		 0.59764747619628156 1.1057548641715931 -0.21747022226912802 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "L_Knee_Bnd_5_Bnd";
	setAttr ".radi" 2;
createNode joint -n "LeftFoot_Skl" -p "LeftLeg_Roll_04_Skl";
	rename -uid "FBC1996E-9D42-BFA2-72A9-FC808567F1B2";
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
	setAttr ".uoc" 1;
	setAttr ".oc" 1;
	setAttr ".t" -type "double3" -2.9802341705575941e-09 -0.57665107608035582 -0.016142283432817761 ;
	setAttr ".r" -type "double3" -9.5416640443905503e-15 1.9083328088781101e-14 -3.1805546814635183e-15 ;
	setAttr ".jo" -type "double3" -4.4163831504686586 -64.876599139049603 -85.999999999999986 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.029616453157005038 -0.42353501230587032 0.90539547108071228 0
		 0.99946542196927213 4.8594247602066957e-16 -0.03269358175214504 0 0.013846876549717411 0.90587973448524917 0.42330859979304791 0
		 0.59764747321604728 0.52910378809123726 -0.23361250570194578 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "L_Foot_Ankle_Bnd";
	setAttr ".radi" 2;
	setAttr -k on ".atoms_ikSoftDistance" 0.05;
	setAttr -k on ".atoms_ikTollerance" 0.001;
	setAttr ".fbxID" 5;
createNode joint -n "LeftToeBase_Skl" -p "LeftFoot_Skl";
	rename -uid "CF1E5EA3-1C49-586B-2FA6-939A990D11E9";
	addAttr -ci true -h true -sn "fbxID" -ln "filmboxTypeID" -at "short";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 2;
	setAttr ".t" -type "double3" 1.0879466691054183 -0.033881520977341761 0.1186034331859202 ;
	setAttr ".r" -type "double3" -1.1964352180661589e-14 -6.3778041689942856e-15 -2.3854160110976368e-15 ;
	setAttr ".jo" -type "double3" 0.77538331645781999 -22.45417856614052 9.9392333795734899e-17 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.032659827789368018 -0.045429086726437529 0.99843353996546536 0
		 0.99939400050517369 0.013518607271425002 -0.032076143965656577 0 -0.012040240987346082 0.99887609108269393 0.045843072108267824 0
		 0.59764747321604605 0.17576072876704385 0.80272304279198625 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "L_Foot_BallToes_Bnd";
	setAttr ".radi" 2;
	setAttr ".fbxID" 5;
createNode joint -n "LeftToeEnd_Skl" -p "LeftToeBase_Skl";
	rename -uid "3AD35A7E-AB40-F5B6-7ED4-E48A2A35C561";
	addAttr -ci true -h true -sn "fbxID" -ln "filmboxTypeID" -at "short";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 3;
	setAttr ".t" -type "double3" 1.6389516777431425 -0.066628493966073843 -0.10387754202041351 ;
	setAttr ".r" -type "double3" -3.7901092285701723e-14 7.5538173684758551e-15 7.7526020360673188e-15 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.032659800000000003 -0.0454291 0.99843400000000004 0
		 0.999394 0.0135186 -0.032076100000000003 0 -0.012040199999999999 0.99887599999999999 0.045843099999999998 0
		 14.200742999999999 -101.791563 21.831958 1;
	setAttr ".radi" 2;
	setAttr ".fbxID" 5;
createNode joint -n "Spine_Skl" -p "Hips_Skl";
	rename -uid "809A426A-EC45-11CA-E1FA-F4809B607086";
	addAttr -ci true -h true -sn "fbxID" -ln "filmboxTypeID" -at "short";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 1;
	setAttr ".t" -type "double3" -1.258478257327035e-15 0.83384110537595379 3.9780173014669865e-16 ;
	setAttr ".r" -type "double3" -3.1780125345961146e-30 -6.3611093629270335e-15 5.7249984266343308e-14 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -1.1330483133636381e-15 8.3830821561187889 3.9780173014669826e-16 1;
	setAttr ".radi" 2;
	setAttr ".fbxID" 5;
createNode joint -n "Spine1_Skl" -p "Spine_Skl";
	rename -uid "6B04DCEE-B440-3124-AFC0-3EB9D93687A6";
	addAttr -ci true -h true -sn "fbxID" -ln "filmboxTypeID" -at "short";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 2;
	setAttr ".t" -type "double3" -1.2584782573270375e-15 0.83384110537595291 3.7935438709091122e-16 ;
	setAttr ".r" -type "double3" -3.1780125345961146e-30 -6.3611093629270335e-15 5.7249984266343308e-14 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -2.3915265706906756e-15 9.2169232614947418 7.7715611723760948e-16 1;
	setAttr ".radi" 2;
	setAttr ".fbxID" 5;
createNode joint -n "LeftShoulder_Skl" -p "Spine1_Skl";
	rename -uid "E646FFF1-514B-32A6-4DA7-36BDB097EC51";
	addAttr -ci true -h true -sn "fbxID" -ln "filmboxTypeID" -at "short";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".t" -type "double3" 4.6623065471649197 0.93296191611756463 0.18366999924182814 ;
	setAttr ".r" -type "double3" -3.975693351829395e-16 8.3590037390325185e-18 -9.4821134754402025e-18 ;
	setAttr ".jo" -type "double3" 2.2250000000000005 0 0 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 1.0000000000000002 0 0 0 0 0.99924607144684574 0.038823816119047574 0
		 0 -0.038823816119047574 0.99924607144684574 0 4.662306547164917 10.149885177612306 0.18366999924182892 1;
	setAttr ".radi" 2;
	setAttr ".fbxID" 5;
createNode joint -n "LeftArm_Skl" -p "LeftShoulder_Skl";
	rename -uid "2F525E51-9B46-FA92-E086-40B17637CC78";
	addAttr -ci true -h true -sn "fbxID" -ln "filmboxTypeID" -at "short";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 1;
	setAttr ".t" -type "double3" 0.12298512458801358 6.7580836009994982e-05 -5.3790183961871518e-05 ;
	setAttr ".r" -type "double3" -7.5405387238019304e-15 -7.9513867036587919e-16 -5.0611797097262073e-16 ;
	setAttr ".jo" -type "double3" 0 4.1 0 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.99744078293094418 0.0027758036317540378 -0.07144354036792594 0
		 0 0.99924607144684574 0.038823816119047574 0 0.071497444332685928 -0.038724457546149817 0.99668878384461179 0
		 4.7852916717529306 10.149954795837406 0.18361887335777305 1;
	setAttr ".radi" 2;
	setAttr ".fbxID" 5;
createNode joint -n "LeftArm_Roll_01_Skl" -p "LeftArm_Skl";
	rename -uid "42390C53-E946-9A22-3EFC-4B95B66B504A";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 2;
	setAttr ".t" -type "double3" 0.58558233782930635 -0.00045124300938859108 0.030331187318443031 ;
	setAttr ".r" -type "double3" 4.551243296736187e-12 -2.3685445775191025e-29 5.9635400277440949e-16 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 87.777720542347069 -2.9650772206541132 -0.044151459470497048 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.999803529477168 1.3010426069826053e-18 -0.019821766949447164 0
		 0.019821766949447185 7.9353190685083064e-14 0.99980352947716811 0 1.560383766641138e-15 -1.0000000000000004 7.9332374003371342e-14 0
		 5.3715439796447715 10.149954795837406 0.17199603319168114 1;
	setAttr ".radi" 2;
createNode joint -n "LeftArm_Roll_02_Skl" -p "LeftArm_Roll_01_Skl";
	rename -uid "EEE72AB2-1746-2FE9-3897-C8B15364DFF2";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 3;
	setAttr ".t" -type "double3" 0.58636751182346547 -1.6653345369377348e-16 0 ;
	setAttr ".r" -type "double3" 4.5350237102648957e-12 8.9950062085140722e-14 -1.5405811738335353e-14 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.999803529477168 1.3010426069826053e-18 -0.019821766949447164 0
		 0.019821766949447185 7.9353190685083064e-14 0.99980352947716811 0 1.560383766641138e-15 -1.0000000000000004 7.9332374003371342e-14 0
		 5.9577962875366168 10.149954795837406 0.16037319302558903 1;
	setAttr ".radi" 2;
createNode joint -n "LeftArm_Roll_03_Skl" -p "LeftArm_Roll_02_Skl";
	rename -uid "038C6C29-CC44-DE16-C973-459C1E57E627";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 4;
	setAttr ".t" -type "double3" 0.58636751182346547 -2.2204460492503131e-16 1.7763568394002505e-15 ;
	setAttr ".r" -type "double3" 4.5350237102648957e-12 9.0049454418935883e-14 -1.1927080055452551e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.999803529477168 1.3010426069826053e-18 -0.019821766949447164 0
		 0.019821766949447185 7.9353190685083064e-14 0.99980352947716811 0 1.560383766641138e-15 -1.0000000000000004 7.9332374003371342e-14 0
		 6.5440485954284622 10.149954795837404 0.14875035285949686 1;
	setAttr ".radi" 2;
createNode joint -n "LeftArm_Roll_04_Skl" -p "LeftArm_Roll_03_Skl";
	rename -uid "DFC3B141-3048-59A7-1415-3D9843A4EF3C";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 5;
	setAttr ".t" -type "double3" 0.58636751182346547 -1.1102230246251565e-16 -3.5527136788005009e-15 ;
	setAttr ".r" -type "double3" 7.7650260777917957e-19 5.9635400277440949e-16 9.9392333795734924e-17 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" -89.999999999995495 0 1.135777971966863 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 1.0000000000000002 1.5742212394452246e-15 7.2858385991025898e-17 0
		 -1.5615277629739123e-15 1.0000000000000004 -7.131148169244729e-16 0 -5.2041704279181563e-17 7.3378418979628683e-16 1.0000000000000002 0
		 7.1303009033203075 10.149954795837408 0.13712751269340481 1;
	setAttr ".radi" 2;
createNode joint -n "LeftForeArm_Skl" -p "LeftArm_Roll_04_Skl";
	rename -uid "AC292D9C-004E-CC1A-14F9-FFAD6F056558";
	addAttr -ci true -h true -sn "fbxID" -ln "filmboxTypeID" -at "short";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 6;
	setAttr ".t" -type "double3" 0.58625230789185334 -7.1054273576010019e-15 -0.011622840166092496 ;
	setAttr ".r" -type "double3" -1.9748014321040096e-14 -1.4138947733747165e-14 9.477059027423326e-14 ;
	setAttr ".jo" -type "double3" 2.246789793664989 -7.9840762374929222 -0.3122313046752519 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.99029200541000173 -0.0053966143450723293 0.13889787822226848 0
		 2.1431593402505283e-17 0.99924607144684596 0.038823816119047547 0 -0.13900267630890262 -0.038446914722200722 0.98954539599116254 0
		 7.7165532112121609 10.149954795837402 0.12550467252731234 1;
	setAttr ".radi" 2;
	setAttr ".fbxID" 5;
createNode joint -n "LeftForeArm_Roll_01_Skl" -p "LeftForeArm_Skl";
	rename -uid "47E1977A-C14E-BB2E-909D-64B289A00D6F";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 7;
	setAttr ".t" -type "double3" 0.53790068609473884 0.00037822871522408263 -0.06567234378241138 ;
	setAttr ".r" -type "double3" 1.2424041724466862e-17 3.8825130388958945e-18 -2.2363275104040355e-16 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" -2.2249999999999979 7.9901395435160412 5.5201681210201615e-16 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 1.0000000000000002 -9.540979117872439e-18 0 0 2.0816681711721685e-17 1.0000000000000002 6.9388939039072284e-18 0
		 5.5511151231257827e-17 6.9388939039072284e-18 1.0000000000000002 0 8.2583605919015692 10.149954795837404 0.13524685536843084 1;
	setAttr ".radi" 2;
createNode joint -n "LeftForeArm_Roll_02_Skl" -p "LeftForeArm_Roll_01_Skl";
	rename -uid "FEFCD6FF-9341-7A13-042C-759C00B3F9CF";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".t" -type "double3" 0.54180738068940926 0 0.0097421828411187184 ;
	setAttr ".r" -type "double3" -3.2613109526725528e-17 -9.9392333795734899e-17 3.677516350442191e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 1.0000000000000002 -9.540979117872439e-18 0 0 2.0816681711721685e-17 1.0000000000000002 6.9388939039072284e-18 0
		 5.5511151231257827e-17 6.9388939039072284e-18 1.0000000000000002 0 8.8001679725909785 10.149954795837404 0.14498903820954956 1;
	setAttr ".radi" 2;
createNode joint -n "LeftForeArm_Roll_03_Skl" -p "LeftForeArm_Roll_02_Skl";
	rename -uid "ADB3C3EA-D64D-5F46-8B55-0FB1EB8AC2E1";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 1;
	setAttr ".t" -type "double3" 0.54180738068941281 0 0.0097421828411187461 ;
	setAttr ".r" -type "double3" 7.765026077791789e-19 1.3470173028717528e-36 -1.987846675914698e-16 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 1.0000000000000002 -9.540979117872439e-18 0 0 2.0816681711721685e-17 1.0000000000000002 6.9388939039072284e-18 0
		 5.5511151231257827e-17 6.9388939039072284e-18 1.0000000000000002 0 9.3419753532803913 10.149954795837404 0.15473122105066831 1;
	setAttr ".radi" 2;
createNode joint -n "LeftForeArm_Roll_04_Skl" -p "LeftForeArm_Roll_03_Skl";
	rename -uid "B5739EDC-EF4A-9476-0EC1-F4945DBD000C";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 2;
	setAttr ".t" -type "double3" 0.54180738068941103 -1.7763568394002505e-15 0.0097421828411188016 ;
	setAttr ".r" -type "double3" 1.5530052155583578e-18 2.6940346057435057e-36 -1.987846675914698e-16 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 1.0000000000000002 -9.540979117872439e-18 0 0 2.0816681711721685e-17 1.0000000000000002 6.9388939039072284e-18 0
		 5.5511151231257827e-17 6.9388939039072284e-18 1.0000000000000002 0 9.8837827339698023 10.149954795837402 0.16447340389178711 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "Elbow_Bnd_6_Bnd";
	setAttr ".radi" 2;
createNode joint -n "LeftForeArm_Roll_05_Skl" -p "LeftForeArm_Roll_04_Skl";
	rename -uid "B9D1D361-9644-4B32-185C-D891126103DF";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.34830467382350783 3.5527136788005009e-15 0.0062628440479355618 ;
	setAttr ".r" -type "double3" 89.999999999999972 -1.0301188243345507 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.99983838275922576 1.3142146396552139e-16 0.017977996590727095 0
		 -0.017977996590727036 4.4866614883509951e-16 0.99983838275922599 0 -1.3877787807814459e-16 -1.0000000000000004 4.3368086899420187e-16 0
		 10.23208740779331 10.149954795837406 0.17073624793972264 1;
	setAttr ".radi" 2;
	setAttr ".liw" yes;
createNode joint -n "LeftHand_Skl" -p "LeftForeArm_Roll_05_Skl";
	rename -uid "2903020E-9544-B606-B76B-4FBB132796F2";
	addAttr -ci true -h true -sn "fbxID" -ln "filmboxTypeID" -at "short";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 3;
	setAttr ".t" -type "double3" 0.19353398503330688 -1.4532283721876982e-08 7.1054273576010019e-15 ;
	setAttr ".r" -type "double3" 6.8287142100274448e-10 -1.2644987145345925e-07 4.865277002430455e-09 ;
	setAttr ".jo" -type "double3" -87.796578893089119 -0.309204726496001 6.9540744360545217 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.99029200541000173 -0.0053966143450723258 0.13889787822226843 0
		 2.4257184755938885e-17 0.99924607144684574 0.038823816119047519 0 -0.13900267630890253 -0.038446914722200701 0.98954539599116254 0
		 10.42559011465922 10.149954795837401 0.17421558673290621 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "LeftHand";
	setAttr ".radi" 2;
	setAttr ".fbxID" 5;
createNode joint -n "LeftHandThumb1_Skl" -p "LeftHand_Skl";
	rename -uid "EFD00D13-C74D-A634-B915-C482BD122529";
	addAttr -ci true -h true -sn "fbxID" -ln "filmboxTypeID" -at "short";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 4;
	setAttr ".t" -type "double3" 0.55319263507981198 -0.095726464036745895 0.45943966799955138 ;
	setAttr ".r" -type "double3" -1.6018544398140264e-15 4.7669573690244837e-15 -0.27818546350544965 ;
	setAttr ".jo" -type "double3" 20.952000000000009 -35.997000974577524 -32.740046608315602 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.59221199999999996 -0.46349499999999999 0.65913299999999997 0
		 0.28488799999999997 0.88561000000000001 0.366788 0 -0.75373900000000005 -0.029437000000000001 0.65651400000000004 0
		 73.223712000000006 41.736763000000003 2.8109459999999999 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "L_Hand_Thumb_00_Bnd";
	setAttr ".radi" 2;
	setAttr ".fbxID" 5;
createNode joint -n "LeftHandThumb2_Skl" -p "LeftHandThumb1_Skl";
	rename -uid "3BB432BE-5645-EAAF-1247-D3B420D7A75C";
	addAttr -ci true -h true -sn "fbxID" -ln "filmboxTypeID" -at "short";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 5;
	setAttr ".t" -type "double3" 0.68594907566816632 -0.17710076166095945 0.076259849960228721 ;
	setAttr ".r" -type "double3" -1.590277340731756e-15 -3.4190962825732814e-14 -7.9513867036587919e-15 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.59221199999999996 -0.46349499999999999 0.65913299999999997 0
		 0.28488799999999997 0.88561000000000001 0.366788 0 -0.75373900000000005 -0.029437000000000001 0.65651400000000004 0
		 74.705509000000006 40.577033999999998 4.4601870000000003 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "L_Hand_Thumb_01_Bnd";
	setAttr ".radi" 2;
	setAttr ".fbxID" 5;
createNode joint -n "LeftHandThumb3_Skl" -p "LeftHandThumb2_Skl";
	rename -uid "21866430-2241-593E-1A67-41BB1C597AA4";
	addAttr -ci true -h true -sn "fbxID" -ln "filmboxTypeID" -at "short";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 6;
	setAttr ".t" -type "double3" 0.51894104011945741 -0.13398203558005228 0.057692862723337512 ;
	setAttr ".r" -type "double3" -1.2722218725854064e-14 -1.6697912077683458e-14 -3.1805546814635144e-15 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.59221199999999996 -0.46349499999999999 0.65913299999999997 0
		 0.28488799999999997 0.88561000000000001 0.366788 0 -0.75373900000000005 -0.029437000000000001 0.65651400000000004 0
		 76.138237000000004 39.455708000000001 6.0548149999999996 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "L_Hand_Thumb_02_Bnd";
	setAttr ".radi" 2;
	setAttr ".fbxID" 5;
createNode joint -n "LeftHandThumb4_Skl" -p "LeftHandThumb3_Skl";
	rename -uid "240519E3-3349-35AC-84B4-9FBAA8BA0BCC";
	addAttr -ci true -h true -sn "fbxID" -ln "filmboxTypeID" -at "short";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 7;
	setAttr ".t" -type "double3" 0.59644502484961581 -0.16615133002479965 0.15725919511093345 ;
	setAttr ".r" -type "double3" 1.2662393692531386e-30 -2.0276036094329917e-14 -7.1562480332929135e-15 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.59221199999999996 -0.46349499999999999 0.65913299999999997 0
		 0.28488799999999997 0.88561000000000001 0.366788 0 -0.75373900000000005 -0.029437000000000001 0.65651400000000004 0
		 78.256274000000005 37.798029999999997 8.4121980000000001 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "L_Hand_Thumb_03_Bnd";
	setAttr ".radi" 2;
	setAttr ".fbxID" 5;
createNode joint -n "LeftHandIndex1_Skl" -p "LeftHand_Skl";
	rename -uid "5F2351CB-FC43-E053-B307-9AAEA8F50962";
	addAttr -ci true -h true -sn "fbxID" -ln "filmboxTypeID" -at "short";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 4;
	setAttr ".t" -type "double3" 1.8223204147454926 0.23259587101975576 0.42942059200358251 ;
	setAttr ".r" -type "double3" -6.9574633657014427e-15 7.9513867036587821e-16 -1.6697912077683464e-14 ;
	setAttr ".jo" -type "double3" -92.624894812505886 -10.07108671404985 2.9034501782211448 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.94947400000000004 0.037805100000000001 0.31156 0
		 0.31178299999999998 -1.2614399999999999e-06 -0.95015300000000003 0 -0.035920300000000002 0.99928499999999998 -0.0117882 0
		 79.32038 45.078960000000002 1.4154869999999999 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "L_Hand_Index_01_Bnd";
	setAttr ".radi" 2;
	setAttr ".fbxID" 5;
createNode joint -n "LeftHandIndex2_Skl" -p "LeftHandIndex1_Skl";
	rename -uid "C66CEB13-3E45-A716-6B65-1E802B4D8CF0";
	addAttr -ci true -h true -sn "fbxID" -ln "filmboxTypeID" -at "short";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 5;
	setAttr ".t" -type "double3" 0.54210695618083449 0.085112440835811487 -0.057701352275763895 ;
	setAttr ".r" -type "double3" -3.975693351829395e-16 -6.6208594470752346e-32 -1.9083328088781097e-14 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.94947400000000004 0.037805100000000001 0.31156 0
		 0.31178299999999998 -1.2614399999999999e-06 -0.95015300000000003 0 -0.035920300000000002 0.99928499999999998 -0.0117882 0
		 83.223555000000005 45.234372 2.6962739999999998 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "L_Hand_Index_02_Bnd";
	setAttr ".radi" 2;
	setAttr ".fbxID" 5;
createNode joint -n "LeftHandIndex3_Skl" -p "LeftHandIndex2_Skl";
	rename -uid "2DD6F309-884F-D473-53DC-F1B44B6AB162";
	addAttr -ci true -h true -sn "fbxID" -ln "filmboxTypeID" -at "short";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 6;
	setAttr ".t" -type "double3" 0.49539447688089666 0.077778439518588094 -0.0527293201093606 ;
	setAttr ".r" -type "double3" -1.9878466759146975e-16 -3.3104297235376173e-32 -1.9083328088781097e-14 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.94947400000000004 0.037805100000000001 0.31156 0
		 0.31178299999999998 -1.2614399999999999e-06 -0.95015300000000003 0 -0.035920300000000002 0.99928499999999998 -0.0117882 0
		 86.279241999999996 45.356046999999997 3.698966 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "L_Hand_Index_03_Bnd";
	setAttr ".radi" 2;
	setAttr ".fbxID" 5;
createNode joint -n "LeftHandIndex4_Skl" -p "LeftHandIndex3_Skl";
	rename -uid "C49C1779-3D4D-4357-1675-6E8BDCBA97EB";
	addAttr -ci true -h true -sn "fbxID" -ln "filmboxTypeID" -at "short";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 7;
	setAttr ".t" -type "double3" 0.61645881152652748 0.09678590825214517 -0.065615293516957607 ;
	setAttr ".r" -type "double3" -1.9878466759146975e-16 -3.3104297235376173e-32 -1.9083328088781097e-14 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.94947400000000004 0.037805100000000001 0.31156 0
		 0.31178299999999998 -1.2614399999999999e-06 -0.95015300000000003 0 -0.035920300000000002 0.99928499999999998 -0.0117882 0
		 87.634153999999995 45.410003000000003 4.1435659999999999 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "L_Hand_Index_04_Bnd";
	setAttr ".radi" 2;
	setAttr ".fbxID" 5;
createNode joint -n "LeftHandMiddle1_Skl" -p "LeftHand_Skl";
	rename -uid "9D9B280F-A148-597B-C5D2-77AB9CB1E3EA";
	addAttr -ci true -h true -sn "fbxID" -ln "filmboxTypeID" -at "short";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 4;
	setAttr ".t" -type "double3" 1.7822576879469967 0.26268855890125131 -0.27176010053485689 ;
	setAttr ".r" -type "double3" -3.9756933518293955e-16 -7.9513867036587939e-16 -1.8685758753598167e-14 ;
	setAttr ".jo" -type "double3" -91.889508154414457 8.6630230386531206 2.2369809117385699 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.99918499999999999 0.039018400000000002 -0.010341400000000001 0
		 -0.010349300000000001 -1.32754e-06 -0.999946 0 -0.039016299999999997 0.99923799999999996 0.00040248500000000001 0
		 79.480975000000001 45.198673999999997 -0.63337900000000003 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "L_Hand_Middle_01_Bnd";
	setAttr ".radi" 2;
	setAttr ".fbxID" 5;
createNode joint -n "LeftHandMiddle2_Skl" -p "LeftHandMiddle1_Skl";
	rename -uid "46BDA571-BC4A-6883-48DC-038E98291D2B";
	addAttr -ci true -h true -sn "fbxID" -ln "filmboxTypeID" -at "short";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 5;
	setAttr ".t" -type "double3" 0.55787531400183532 0.015618472034889475 -0.047829593304919982 ;
	setAttr ".r" -type "double3" -1.3032819768965738e-14 9.9392333795734721e-16 -1.6002165741113319e-14 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.99918499999999999 0.039018400000000002 -0.010341400000000001 0
		 -0.010349300000000001 -1.32754e-06 -0.999946 0 -0.039016299999999997 0.99923799999999996 0.00040248500000000001 0
		 84.613840999999994 45.399113 -0.686504 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "L_Hand_Middle_02_Bnd";
	setAttr ".radi" 2;
	setAttr ".fbxID" 5;
createNode joint -n "LeftHandMiddle3_Skl" -p "LeftHandMiddle2_Skl";
	rename -uid "003D20A3-FB4F-9C59-02D9-E486C311CA7C";
	addAttr -ci true -h true -sn "fbxID" -ln "filmboxTypeID" -at "short";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 6;
	setAttr ".t" -type "double3" 0.55502762973534203 0.015538747272092313 -0.047585446312025326 ;
	setAttr ".r" -type "double3" -1.3032819768965738e-14 9.9392333795734721e-16 -1.6002165741113319e-14 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.99918499999999999 0.039018400000000002 -0.010341400000000001 0
		 -0.010349300000000001 -1.32754e-06 -0.999946 0 -0.039016299999999997 0.99923799999999996 0.00040248500000000001 0
		 87.690378999999993 45.519261 -0.71834500000000001 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "L_Hand_Middle_03_Bnd";
	setAttr ".radi" 2;
	setAttr ".fbxID" 5;
createNode joint -n "LeftHandMiddle4_Skl" -p "LeftHandMiddle3_Skl";
	rename -uid "B15ED132-0A42-8946-75B2-2E8CF12D75E7";
	addAttr -ci true -h true -sn "fbxID" -ln "filmboxTypeID" -at "short";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 7;
	setAttr ".t" -type "double3" 0.71588588485274407 0.020042191135040133 -0.061376673005343108 ;
	setAttr ".r" -type "double3" -1.3032819768965738e-14 9.9392333795734721e-16 -1.6002165741113319e-14 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.99918499999999999 0.039018400000000002 -0.010341400000000001 0
		 -0.010349300000000001 -1.32754e-06 -0.999946 0 -0.039016299999999997 0.99923799999999996 0.00040248500000000001 0
		 88.929873000000001 45.567661999999999 -0.73117399999999999 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "L_Hand_Middle_04_Bnd";
	setAttr ".radi" 2;
	setAttr ".fbxID" 5;
createNode joint -n "LeftHandPinky1_Skl" -p "LeftHand_Skl";
	rename -uid "295CBCC5-5E40-124B-BD57-57B27D9AF0EB";
	addAttr -ci true -h true -sn "fbxID" -ln "filmboxTypeID" -at "short";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 4;
	setAttr ".t" -type "double3" 1.4983939199179659 0.074067312905013338 -0.96036659993071405 ;
	setAttr ".r" -type "double3" -1.5107634736951707e-14 -3.1805546814635203e-15 -2.2263882770244621e-14 ;
	setAttr ".jo" -type "double3" -91.389698993413305 39.162501576716991 0.81521132727196166 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.85553599999999996 0.031119399999999998 -0.51680700000000002 0
		 -0.51705699999999999 -1.1363700000000001e-06 -0.85595100000000002 0 -0.026637299999999999 0.99951599999999996 0.0160895 0
		 79.345203999999995 45.061750000000004 -5.2753969999999999 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "L_Hand_Pinky_01_Bnd";
	setAttr ".radi" 2;
	setAttr ".fbxID" 5;
createNode joint -n "LeftHandPinky2_Skl" -p "LeftHandPinky1_Skl";
	rename -uid "C5301C13-AA41-3579-977F-F699D3BFA3A4";
	addAttr -ci true -h true -sn "fbxID" -ln "filmboxTypeID" -at "short";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 5;
	setAttr ".t" -type "double3" 0.43407198954623638 -0.13319051610579713 -0.092261299884327741 ;
	setAttr ".r" -type "double3" -3.1805546814635152e-15 -9.5416640443905503e-15 -2.0673605429512861e-14 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.85553599999999996 0.031119399999999998 -0.51680700000000002 0
		 -0.51705699999999999 -1.1363700000000001e-06 -0.85595100000000002 0 -0.026637299999999999 0.99951599999999996 0.0160895 0
		 81.543488999999994 45.141711000000001 -6.6033220000000004 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "L_Hand_Pinky_02_Bnd";
	setAttr ".radi" 2;
	setAttr ".fbxID" 5;
createNode joint -n "LeftHandPinky3_Skl" -p "LeftHandPinky2_Skl";
	rename -uid "A906C941-2645-98E8-263C-B4BF09069E6E";
	addAttr -ci true -h true -sn "fbxID" -ln "filmboxTypeID" -at "short";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 6;
	setAttr ".t" -type "double3" 0.46466713094580214 -0.14257831990672631 -0.098764247744716371 ;
	setAttr ".r" -type "double3" -3.1805546814635152e-15 -9.5416640443905503e-15 -2.0673605429512861e-14 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.85553599999999996 0.031119399999999998 -0.51680700000000002 0
		 -0.51705699999999999 -1.1363700000000001e-06 -0.85595100000000002 0 -0.026637299999999999 0.99951599999999996 0.0160895 0
		 83.284497999999999 45.205019 -7.6550180000000001 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "L_Hand_Pinky_03_Bnd";
	setAttr ".radi" 2;
	setAttr ".fbxID" 5;
createNode joint -n "LeftHandPinky4_Skl" -p "LeftHandPinky3_Skl";
	rename -uid "AD4944E3-3543-3DEE-3243-D48F0EC9AA85";
	addAttr -ci true -h true -sn "fbxID" -ln "filmboxTypeID" -at "short";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 7;
	setAttr ".t" -type "double3" 0.58579401764463235 -0.17974485666153672 -0.12450957176217159 ;
	setAttr ".r" -type "double3" -3.1805546814635152e-15 -9.5416640443905503e-15 -2.0673605429512861e-14 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.85553599999999996 0.031119399999999998 -0.51680700000000002 0
		 -0.51705699999999999 -1.1363700000000001e-06 -0.85595100000000002 0 -0.026637299999999999 0.99951599999999996 0.0160895 0
		 84.008825000000002 45.231369999999998 -8.0925639999999994 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "L_Hand_Pinky_04_Bnd";
	setAttr ".radi" 2;
	setAttr ".fbxID" 5;
createNode joint -n "Neck_Skl" -p "Spine1_Skl";
	rename -uid "65E3B35A-384B-3ABA-C82E-999D447EE420";
	addAttr -ci true -h true -sn "fbxID" -ln "filmboxTypeID" -at "short";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 4;
	setAttr ".t" -type "double3" 2.3909483295320164e-15 1.4036690250699557 -0.010385682880812408 ;
	setAttr ".r" -type "double3" 0 -1.590277340731758e-15 0 ;
	setAttr ".jo" -type "double3" 180 -24.775140568832406 90 ;
	setAttr ".bps" -type "matrix" 0 0.90795938450044844 0.41905817746175483 0 1.0000000000000002 -4.4408920985006271e-16 1.6653345369377358e-16 0
		 2.2204460492503141e-16 0.41905817746175483 -0.90795938450044855 0 -5.7824115865919865e-19 10.620592286564698 -0.01038568288081163 1;
	setAttr ".radi" 2;
	setAttr ".fbxID" 5;
createNode joint -n "Neck1_Skl" -p "Neck_Skl";
	rename -uid "22EDA820-3443-4BD0-5863-00B677166DB8";
	addAttr -ci true -h true -sn "fbxID" -ln "filmboxTypeID" -at "short";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 5;
	setAttr ".t" -type "double3" 1.0193653561853946 -1.2585877263182838e-16 0.50952585485934332 ;
	setAttr ".r" -type "double3" -2.1140600669270041e-14 -7.9513867036587856e-15 3.5676081304495498e-14 ;
	setAttr ".jo" -type "double3" 0 -3.6429049134946543 0 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 1.4108238180255238e-17 0.9327508463777382 0.36052164786821567 0
		 1.0000000000000002 -4.4408920985006271e-16 1.6653345369377358e-16 0 2.2159594804906174e-16 0.36052164786821567 -0.93275084637773831 0
		 -1.3299546649155628e-17 11.759655604054871 -0.045841076115261926 1;
	setAttr ".radi" 2;
	setAttr ".fbxID" 5;
createNode joint -n "Head_Skl" -p "Neck1_Skl";
	rename -uid "5E70802C-D14A-DFD5-FBEE-46B3EF6A0460";
	addAttr -ci true -h true -sn "fbxID" -ln "filmboxTypeID" -at "short";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".t" -type "double3" 2.6289022740416979 -1.9776237540409306e-15 1.0984751162137876 ;
	setAttr ".r" -type "double3" -1.2293200501427038e-14 -6.3611093629270304e-15 3.7440402148713956e-14 ;
	setAttr ".jo" -type "double3" 180 -21.671383840628618 0 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 9.4942568351699249e-17 0.99995572711427061 -0.0094097721210968932 0
		 -1.0000000000000002 4.4293684511918202e-16 -2.8899271174372915e-16 0 -3.2318766138695292e-16 0.0094097721210968932 0.99995572711427061 0
		 -1.7104164864695942e-15 14.607790484251247 -0.12266849056654242 1;
	setAttr ".radi" 2;
	setAttr ".fbxID" 5;
createNode joint -n "Head_End_Skl" -p "Head_Skl";
	rename -uid "DAA8B356-3F42-B54A-1C5A-2793A32C409F";
	addAttr -ci true -h true -sn "fbxID" -ln "filmboxTypeID" -at "short";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 1;
	setAttr ".t" -type "double3" 5.4669484486493802 6.8744558724448559e-15 -4.4395043197198447e-14 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0 0.99995599999999996 -0.0094097699999999996 0 -1 0 0 0
		 0 0.0094097699999999996 0.99995599999999996 0 0 77.252600000000001 -0.38434000000000001 1;
	setAttr ".radi" 2;
	setAttr ".fbxID" 5;
createNode joint -n "LeftEye_Skl" -p "Head_Skl";
	rename -uid "8DF13B09-504E-58E6-D65B-4DB249844F53";
	addAttr -ci true -h true -sn "fbxID" -ln "filmboxTypeID" -at "short";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 1;
	setAttr ".t" -type "double3" 3.7875569696438642 -1.0734931067563622 4.104038651364827 ;
	setAttr ".r" -type "double3" -4.9696166897869422e-17 -8.8956138747182728e-15 2.544501982866397e-14 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 9.4942568351699249e-17 0.99995572711427061 -0.0094097721210968932 0
		 -1.0000000000000002 4.4293684511918202e-16 -2.8899271174372915e-16 0 -3.2318766138695292e-16 0.0094097721210968932 0.99995572711427061 0
		 1.0734931067563596 18.433797836303714 3.9455484151840214 1;
	setAttr ".radi" 2;
	setAttr ".fbxID" 5;
createNode joint -n "RightEye_Skl" -p "Head_Skl";
	rename -uid "E33E73CF-CE48-1112-B4BA-FA9E14863C34";
	addAttr -ci true -h true -sn "fbxID" -ln "filmboxTypeID" -at "short";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 1;
	setAttr ".t" -type "double3" 3.7875569696438678 1.0734931067563571 4.1040386513648253 ;
	setAttr ".r" -type "double3" 180 180 -179.99999999999997 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" -4.7161132141309881e-16 0.99995572711427061 -0.0094097721210970164 0
		 -1.0000000000000002 -1.2474432640087556e-16 -4.0612082679667694e-16 0 -4.4565234130168836e-16 0.0094097721210970164 0.99995572711427061 0
		 -1.0734931067563598 18.433797836303718 3.9455484151840179 1;
	setAttr ".radi" 2;
	setAttr ".fbxID" 5;
createNode joint -n "Jaw_Skl" -p "Head_Skl";
	rename -uid "511BDF1F-5048-1CF7-D40E-E1B913FDB33A";
	addAttr -ci true -h true -sn "fbxID" -ln "filmboxTypeID" -at "short";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 1;
	setAttr ".t" -type "double3" 1.8814444774178209 -1.5802983666497432e-15 0.15010180422462008 ;
	setAttr ".r" -type "double3" 0.53914818529086705 0 -89.999999999999986 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0 0.99995599999999996 -0.0094097699999999996 0 -1 0 0 0
		 0 0.0094097699999999996 0.99995599999999996 0 0 77.252600000000001 -0.38434000000000001 1;
	setAttr ".radi" 2;
	setAttr ".fbxID" 5;
createNode joint -n "RightShoulder_Skl" -p "Spine1_Skl";
	rename -uid "8D65280C-CB48-41B0-B73D-2180A7822084";
	addAttr -ci true -h true -sn "fbxID" -ln "filmboxTypeID" -at "short";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 4;
	setAttr ".t" -type "double3" -4.6623065471649143 0.93296191611756285 0.18366999924182728 ;
	setAttr ".r" -type "double3" -3.1805546814635168e-15 8.4193086954318098e-18 -6.3766885269927852e-18 ;
	setAttr ".jo" -type "double3" -177.77500000000026 0 0 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 1.0000000000000002 0 0 0 0 -0.99924607144684607 -0.03882381611904305 0
		 0 0.03882381611904305 -0.99924607144684607 0 -4.662306547164917 10.149885177612305 0.18366999924182806 1;
	setAttr ".radi" 2;
	setAttr ".fbxID" 5;
createNode joint -n "RightArm_Skl" -p "RightShoulder_Skl";
	rename -uid "8AC263D5-694F-4AAD-0BEE-E690299F3728";
	addAttr -ci true -h true -sn "fbxID" -ln "filmboxTypeID" -at "short";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 5;
	setAttr ".t" -type "double3" -0.12298560142516646 -6.7580257459454174e-05 5.3805073888496535e-05 ;
	setAttr ".r" -type "double3" -1.7896058190099712e-14 -1.5902773407317584e-14 -1.6816496888849572e-16 ;
	setAttr ".jo" -type "double3" 0 4.100000000000005 0 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.99744078293094418 -0.0027758036317537182 0.071443540367926064 0
		 0 -0.99924607144684607 -0.03882381611904305 0 0.071497444332686025 0.038724457546145299 -0.99668878384461213 0
		 -4.7852921485900834 10.149954795837374 0.18361885845660994 1;
	setAttr ".radi" 2;
	setAttr ".fbxID" 5;
createNode joint -n "RightArm_Roll_01_Skl" -p "RightArm_Skl";
	rename -uid "FF95E260-3342-B656-9568-A490BB120A4C";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 6;
	setAttr ".t" -type "double3" -0.5855780195371052 0.00040607363757949599 -0.030329099954744032 ;
	setAttr ".r" -type "double3" 4.5260535521398291e-12 -5.5659706925619243e-15 1.948089742396382e-14 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" -92.228603108732457 -5.234920346141708 0.044277032274393481 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.99980352947716788 -7.8062556418956319e-18 -0.019821766949447178 0
		 0.019821766949447178 7.8902162581329094e-14 0.99980352947716811 0 1.5534448727372308e-15 -1.0000000000000004 7.8860529217905651e-14 0
		 -5.3715400000000004 10.15 0.1719959999999999 1;
	setAttr ".radi" 2;
createNode joint -n "RightArm_Roll_02_Skl" -p "RightArm_Roll_01_Skl";
	rename -uid "2EBA19D0-B345-96C7-2339-6DA974B79335";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 7;
	setAttr ".t" -type "double3" -0.58591442879403299 -0.023241425514896025 -3.5527136788005009e-15 ;
	setAttr ".r" -type "double3" 4.5170236033139652e-12 -1.9480897423964751e-14 1.8089404750822984e-14 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.99980352947716788 -7.8062556418956319e-18 -0.019821766949447178 0
		 0.019821766949447178 7.8902162581329094e-14 0.99980352947716811 0 1.5534448727372308e-15 -1.0000000000000004 7.8860529217905651e-14 0
		 -5.9578000000000024 10.150000000000002 0.16037299999999993 1;
	setAttr ".radi" 2;
createNode joint -n "RightArm_Roll_03_Skl" -p "RightArm_Roll_02_Skl";
	rename -uid "275FD536-2C42-11B6-9CD6-BC8662E93087";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".t" -type "double3" -0.58590443075873644 -0.023241227297226545 0 ;
	setAttr ".r" -type "double3" 4.5170251563191803e-12 -1.9580289757760501e-14 1.8387581752210186e-14 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.99980352947716788 -7.8062556418956319e-18 -0.019821766949447178 0
		 0.019821766949447178 7.8902162581329094e-14 0.99980352947716811 0 1.5534448727372308e-15 -1.0000000000000004 7.8860529217905651e-14 0
		 -6.544050000000003 10.15 0.14874999999999991 1;
	setAttr ".radi" 2;
createNode joint -n "RightArm_Roll_04_Skl" -p "RightArm_Roll_03_Skl";
	rename -uid "C19FEA2A-6D44-C4F5-5FB5-06ACDF6AF174";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 1;
	setAttr ".t" -type "double3" -0.58590445058050111 -0.023240227493696929 0 ;
	setAttr ".r" -type "double3" 1.2722995228461846e-14 3.975693351829396e-15 -9.9392333795734455e-17 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" -89.999999999995566 -1.2702340259094921e-13 1.1357779719668633 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 1.0000000000000002 1.5561755565517334e-15 6.9388939039072284e-17 0
		 -1.5562491348303085e-15 1.0000000000000007 -1.4627224285365729e-15 0 -6.245004513504484e-17 1.5042705496007884e-15 1.0000000000000004 0
		 -7.130300000000001 10.149999999999999 0.13712799999999997 1;
	setAttr ".radi" 2;
createNode joint -n "RightForeArm_Skl" -p "RightArm_Roll_04_Skl";
	rename -uid "9C0B27D2-1B4D-A59B-0823-2291B0F5B730";
	addAttr -ci true -h true -sn "fbxID" -ln "filmboxTypeID" -at "short";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 2;
	setAttr ".t" -type "double3" -0.58625368804930034 -4.5204162594458808e-05 -0.011623342373848766 ;
	setAttr ".r" -type "double3" 3.84544841991208e-08 3.1745301929992827e-14 1.7952536351209712e-07 ;
	setAttr ".jo" -type "double3" -177.75320396322778 7.9840762164612924 0.3122318459790418 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.99029200541000162 0.0053966237011699664 -0.1388978778587554 0
		 -5.6914529315208752e-09 -0.99924606725748011 -0.038823923944659597 0 -0.1390026763089032 0.038447022291573034 -0.98954539181175238 0
		 -7.7165536880493013 10.149954795837402 0.12550465762615115 1;
	setAttr ".radi" 2;
	setAttr ".fbxID" 5;
createNode joint -n "RightForeArm_Roll_01_Skl" -p "RightForeArm_Skl";
	rename -uid "BFCBCDBC-8E4D-94FC-545E-5ABBF658464F";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 3;
	setAttr ".t" -type "double3" -0.53789940593669794 -0.00042340295739862199 0.06567377536615604 ;
	setAttr ".r" -type "double3" 2.5185085580709898e-14 -1.5902773407317588e-15 1.242404172446683e-16 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 177.77499377161365 7.9901395435160714 -3.2929300714413219e-07 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 1.0000000000000002 -5.6871619592488432e-09 -2.2096460772225157e-10 0
		 5.6871619557793962e-09 1.0000000000000004 -7.9888275161810185e-10 0 2.2096457996667596e-10 7.9888277243478356e-10 1.0000000000000004 0
		 -8.2583599999999979 10.149999999999999 0.13524699999999973 1;
	setAttr ".radi" 2;
createNode joint -n "RightForeArm_Roll_02_Skl" -p "RightForeArm_Roll_01_Skl";
	rename -uid "33E5B86E-F544-A825-C6A1-F28B820DCA4E";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 4;
	setAttr ".t" -type "double3" -0.5418099999999999 -1.7763568394002505e-15 0.0097419999999996121 ;
	setAttr ".r" -type "double3" 0 0 1.9878466759146985e-16 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 1.0000000000000002 -5.6871619592488432e-09 -2.2096460772225157e-10 0
		 5.6871619557793962e-09 1.0000000000000004 -7.9888275161810185e-10 0 2.2096457996667596e-10 7.9888277243478356e-10 1.0000000000000004 0
		 -8.8001699999978431 10.15000000308914 0.14498900011971996 1;
	setAttr ".radi" 2;
createNode joint -n "RightForeArm_Roll_03_Skl" -p "RightForeArm_Roll_02_Skl";
	rename -uid "CEDA724D-1C4B-4E3F-15B4-D6BD33B27ED7";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 5;
	setAttr ".t" -type "double3" -0.54181000000000168 -1.7763568394002505e-15 0.009742 ;
	setAttr ".r" -type "double3" 0 0 1.9878466759146985e-16 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 1.0000000000000002 -5.6871619592488432e-09 -2.2096460772225157e-10 0
		 5.6871619557793962e-09 1.0000000000000004 -7.9888275161810185e-10 0 2.2096457996667596e-10 7.9888277243478356e-10 1.0000000000000004 0
		 -9.3419799999956936 10.150000006178281 0.15473100023944111 1;
	setAttr ".radi" 2;
createNode joint -n "RightForeArm_Roll_04_Skl" -p "RightForeArm_Roll_03_Skl";
	rename -uid "014569C0-174E-BE47-F041-6B85525949C1";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 6;
	setAttr ".t" -type "double3" -0.54180000000000028 0 0.0097419999999999729 ;
	setAttr ".r" -type "double3" 0 0 1.9878466759146985e-16 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 1.0000000000000002 -5.6871619592488432e-09 -2.2096460772225157e-10 0
		 5.6871619557793962e-09 1.0000000000000004 -7.9888275161810185e-10 0 2.2096457996667596e-10 7.9888277243478356e-10 1.0000000000000004 0
		 -9.883779999993541 10.150000009267368 0.16447300035915974 1;
	setAttr ".radi" 2;
createNode joint -n "RightForeArm_Roll_05_Skl" -p "RightForeArm_Roll_04_Skl";
	rename -uid "31707A5D-4949-FF3A-301E-059F353AB199";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -0.34830788463804474 -4.5215415855892616e-05 0.0062632326024011364 ;
	setAttr ".r" -type "double3" -90 -178.96988117566545 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 4.5772629004841938e-08 -1.2660339704565203e-08 3.2585037761250055e-07 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" -0.99983838275525327 5.7006052991472057e-09 0.017977996811656186 0
		 0.017977996811656159 6.9650998882855888e-10 0.99983838275525361 0 5.6871619533538305e-09 1.0000000000000002 -7.9888297240604427e-10 0
		 -10.232087884630459 10.149954795837401 0.17073623303856078 1;
	setAttr ".radi" 2;
	setAttr ".liw" yes;
createNode joint -n "RightHand_Skl" -p "RightForeArm_Roll_05_Skl";
	rename -uid "6454D39C-064C-D55F-637A-DD8226C5EC61";
	addAttr -ci true -h true -sn "fbxID" -ln "filmboxTypeID" -at "short";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".t" -type "double3" 0.19353398503330688 -1.4575048657566869e-08 -1.1032543767441894e-09 ;
	setAttr ".r" -type "double3" -6.8331000476308388e-11 1.2650923412310445e-08 3.2880624907545448e-07 ;
	setAttr ".jo" -type "double3" -87.79655376442787 -0.30920559161824696 -173.04592559723235 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.99029200541000162 0.0053966237011699673 -0.1388978778587554 0
		 -5.1690803370456473e-08 -0.99924605453437487 -0.03882425140918163 0 -0.13900267630889368 0.038447352966283418 -0.98954537896392192 0
		 -10.425590591496373 10.149954795837402 0.17421557183174352 1;
	setAttr ".radi" 2;
	setAttr ".fbxID" 5;
createNode joint -n "RightHandThumb1_Skl" -p "RightHand_Skl";
	rename -uid "5D177587-8448-5D48-BDF6-899A110C399B";
	addAttr -ci true -h true -sn "fbxID" -ln "filmboxTypeID" -at "short";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 1;
	setAttr ".t" -type "double3" -0.55319263597612078 0.095726257358535349 -0.45943970998271544 ;
	setAttr ".r" -type "double3" 4.4527765540489235e-14 1.669791207768347e-14 -1.4312496066585821e-14 ;
	setAttr ".jo" -type "double3" 20.952 -35.997014564769991 -32.740030717041677 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.59221199999999996 0.46349499999999999 -0.65913299999999997 0
		 0.28488799999999997 -0.88561000000000001 -0.366788 0 -0.75373999999999997 0.029437399999999999 -0.65651400000000004 0
		 -73.223698999999996 41.736671999999999 2.8109489999999999 1;
	setAttr ".radi" 2;
	setAttr ".fbxID" 5;
createNode joint -n "RightHandThumb2_Skl" -p "RightHandThumb1_Skl";
	rename -uid "077D1E57-6940-FBE5-E15B-78BE57293747";
	addAttr -ci true -h true -sn "fbxID" -ln "filmboxTypeID" -at "short";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 2;
	setAttr ".t" -type "double3" -0.68508112508585706 0.18042908217403841 -0.076259932230072103 ;
	setAttr ".r" -type "double3" 1.4312496066585827e-14 4.7670188018941711e-30 -3.8166656177562201e-14 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.59221199999999996 0.46349499999999999 -0.65913299999999997 0
		 0.28488799999999997 -0.88561000000000001 -0.366788 0 -0.75373999999999997 0.029437399999999999 -0.65651400000000004 0
		 -74.705752000000004 40.576894000000003 4.4601179999999996 1;
	setAttr ".radi" 2;
	setAttr ".fbxID" 5;
createNode joint -n "RightHandThumb3_Skl" -p "RightHandThumb2_Skl";
	rename -uid "66CC3BE6-E743-113B-AA47-589E6DE051D8";
	addAttr -ci true -h true -sn "fbxID" -ln "filmboxTypeID" -at "short";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 3;
	setAttr ".t" -type "double3" -0.51828440948328014 0.13650000982947041 -0.057692924962930547 ;
	setAttr ".r" -type "double3" 9.5416640443905471e-15 6.3611093629270351e-15 -3.1805546814635155e-14 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.59221199999999996 0.46349499999999999 -0.65913299999999997 0
		 0.28488799999999997 -0.88561000000000001 -0.366788 0 -0.75373999999999997 0.029437399999999999 -0.65651400000000004 0
		 -76.138164000000003 39.455626000000002 6.0548080000000004 1;
	setAttr ".radi" 2;
	setAttr ".fbxID" 5;
createNode joint -n "RightHandThumb4_Skl" -p "RightHandThumb3_Skl";
	rename -uid "03F293C7-5C4D-32DC-8B65-47A906181BEE";
	addAttr -ci true -h true -sn "fbxID" -ln "filmboxTypeID" -at "short";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 4;
	setAttr ".t" -type "double3" -0.59563129126991754 0.16904517962418097 -0.15725927219010938 ;
	setAttr ".r" -type "double3" -2.8249000307521001e-30 1.2722218725854064e-14 -2.5444437451708128e-14 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.59221199999999996 0.46349499999999999 -0.65913299999999997 0
		 0.28488799999999997 -0.88561000000000001 -0.366788 0 -0.75373999999999997 0.029437399999999999 -0.65651400000000004 0
		 -78.256521000000006 37.797904000000003 8.4121539999999992 1;
	setAttr ".radi" 2;
	setAttr ".fbxID" 5;
createNode joint -n "RightHandIndex1_Skl" -p "RightHand_Skl";
	rename -uid "183DF52B-234A-3CD9-A83E-4D986EC4F580";
	addAttr -ci true -h true -sn "fbxID" -ln "filmboxTypeID" -at "short";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 1;
	setAttr ".t" -type "double3" -1.8223204125676666 -0.23259607641542601 -0.42942048999285798 ;
	setAttr ".r" -type "double3" 360 7.9513867036587856e-15 1.5902773407317574e-14 ;
	setAttr ".jo" -type "double3" -92.624920301475669 -10.071085441213672 2.903455171943607 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.94947400000000004 -0.037805100000000001 -0.31156 0
		 0.31178299999999998 1.2614399999999999e-06 0.95015300000000003 0 -0.035920300000000002 -0.99928499999999998 0.0117882 0
		 -79.320398999999995 45.078671999999997 1.415489 1;
	setAttr ".radi" 2;
	setAttr ".fbxID" 5;
createNode joint -n "RightHandIndex2_Skl" -p "RightHandIndex1_Skl";
	rename -uid "F7265CF1-AF4E-16B1-2638-C6AC28FDCBC9";
	addAttr -ci true -h true -sn "fbxID" -ln "filmboxTypeID" -at "short";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 2;
	setAttr ".t" -type "double3" -0.54210695618083982 -0.085112440835814596 0.057701352275760343 ;
	setAttr ".r" -type "double3" 7.951386703658788e-16 -4.7708320221952752e-15 1.1131941385122309e-14 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.94947400000000004 -0.037805100000000001 -0.31156 0
		 0.31178299999999998 1.2614399999999999e-06 0.95015300000000003 0 -0.035920300000000002 -0.99928499999999998 0.0117882 0
		 -83.223597999999996 45.234672000000003 2.696269 1;
	setAttr ".radi" 2;
	setAttr ".fbxID" 5;
createNode joint -n "RightHandIndex3_Skl" -p "RightHandIndex2_Skl";
	rename -uid "270BBE54-5C44-6E43-EA14-8CA78DAD6EDF";
	addAttr -ci true -h true -sn "fbxID" -ln "filmboxTypeID" -at "short";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 3;
	setAttr ".t" -type "double3" -0.49539447688089133 -0.077778439518584097 0.052729320109367706 ;
	setAttr ".r" -type "double3" 5.963540027744088e-16 -4.7708320221952752e-15 1.4312496066585827e-14 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.94947400000000004 -0.037805100000000001 -0.31156 0
		 0.31178299999999998 1.2614399999999999e-06 0.95015300000000003 0 -0.035920300000000002 -0.99928499999999998 0.0117882 0
		 -86.279197999999994 45.355671999999998 3.698969 1;
	setAttr ".radi" 2;
	setAttr ".fbxID" 5;
createNode joint -n "RightHandIndex4_Skl" -p "RightHandIndex3_Skl";
	rename -uid "315EB9B8-1848-C312-E153-B08ADD4BF41A";
	addAttr -ci true -h true -sn "fbxID" -ln "filmboxTypeID" -at "short";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 4;
	setAttr ".t" -type "double3" -0.61645881152652748 -0.096785908252144726 0.065615293516954054 ;
	setAttr ".r" -type "double3" 5.963540027744088e-16 -4.7708320221952752e-15 1.4312496066585827e-14 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.94947400000000004 -0.037805100000000001 -0.31156 0
		 0.31178299999999998 1.2614399999999999e-06 0.95015300000000003 0 -0.035920300000000002 -0.99928499999999998 0.0117882 0
		 -87.634197999999998 45.409672 4.1435690000000003 1;
	setAttr ".radi" 2;
	setAttr ".fbxID" 5;
createNode joint -n "RightHandMiddle1_Skl" -p "RightHand_Skl";
	rename -uid "51DDB9BA-6D49-8BA0-58DB-ECAC3E18E05A";
	addAttr -ci true -h true -sn "fbxID" -ln "filmboxTypeID" -at "short";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 1;
	setAttr ".t" -type "double3" -1.7822576854874121 -0.26268845640167093 0.2717602157434067 ;
	setAttr ".r" -type "double3" 4.4726550208080719e-16 2.3854160110976376e-15 9.9392333795734903e-15 ;
	setAttr ".jo" -type "double3" -91.889533553517197 8.6630240194866186 2.2369776225226219 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.99918499999999999 -0.039018400000000002 0.010341400000000001 0
		 -0.010349300000000001 1.32754e-06 0.999946 0 -0.039016299999999997 -0.99923799999999996 -0.00040248500000000001 0
		 -79.480998999999997 45.198672000000002 -0.63338000000000005 1;
	setAttr ".radi" 2;
	setAttr ".fbxID" 5;
createNode joint -n "RightHandMiddle2_Skl" -p "RightHandMiddle1_Skl";
	rename -uid "A794D124-4542-8FFC-816F-E48156C101E9";
	addAttr -ci true -h true -sn "fbxID" -ln "filmboxTypeID" -at "short";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 2;
	setAttr ".t" -type "double3" -0.55787531400181933 -0.015618472034890141 0.047829593304919982 ;
	setAttr ".r" -type "double3" 1.4908850069360225e-16 -1.7890620083232284e-15 8.1501713712502619e-15 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.99918499999999999 -0.039018400000000002 0.010341400000000001 0
		 -0.010349300000000001 1.32754e-06 0.999946 0 -0.039016299999999997 -0.99923799999999996 -0.00040248500000000001 0
		 -84.613798000000003 45.398671999999998 -0.686504 1;
	setAttr ".radi" 2;
	setAttr ".fbxID" 5;
createNode joint -n "RightHandMiddle3_Skl" -p "RightHandMiddle2_Skl";
	rename -uid "252E38CA-F046-12FA-B994-63AD72E6B079";
	addAttr -ci true -h true -sn "fbxID" -ln "filmboxTypeID" -at "short";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 3;
	setAttr ".t" -type "double3" -0.55502762973534558 -0.015538747272092035 0.047585446312028878 ;
	setAttr ".r" -type "double3" 1.4908850069360225e-16 -1.7890620083232284e-15 8.1501713712502619e-15 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.99918499999999999 -0.039018400000000002 0.010341400000000001 0
		 -0.010349300000000001 1.32754e-06 0.999946 0 -0.039016299999999997 -0.99923799999999996 -0.00040248500000000001 0
		 -87.690398999999999 45.519672 -0.71834600000000004 1;
	setAttr ".radi" 2;
	setAttr ".fbxID" 5;
createNode joint -n "RightHandMiddle4_Skl" -p "RightHandMiddle3_Skl";
	rename -uid "92D730B2-FF46-3A65-DE0A-2CB016E2E4E6";
	addAttr -ci true -h true -sn "fbxID" -ln "filmboxTypeID" -at "short";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 4;
	setAttr ".t" -type "double3" -0.71588588485276006 -0.020042191135039883 0.061376673005350213 ;
	setAttr ".r" -type "double3" 1.4908850069360225e-16 -1.7890620083232284e-15 8.1501713712502619e-15 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.99918499999999999 -0.039018400000000002 0.010341400000000001 0
		 -0.010349300000000001 1.32754e-06 0.999946 0 -0.039016299999999997 -0.99923799999999996 -0.00040248500000000001 0
		 -88.929899000000006 45.567672000000002 -0.73117500000000002 1;
	setAttr ".radi" 2;
	setAttr ".fbxID" 5;
createNode joint -n "RightHandPinky1_Skl" -p "RightHand_Skl";
	rename -uid "69DCC400-D246-ED98-90C3-058626AA497A";
	addAttr -ci true -h true -sn "fbxID" -ln "filmboxTypeID" -at "short";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 1;
	setAttr ".t" -type "double3" -1.4983939192244726 -0.074066905742142808 0.96036663241467424 ;
	setAttr ".r" -type "double3" 2.4649298781342254e-14 -9.5416640443905503e-15 -2.0524664285933237e-30 ;
	setAttr ".jo" -type "double3" -91.389731399010898 39.162501934231805 0.81519139889378778 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.85553599999999996 -0.031119399999999998 0.51680700000000002 0
		 -0.51705699999999999 1.1363700000000001e-06 0.85595100000000002 0 -0.026637299999999999 -0.99951599999999996 -0.0160895 0
		 -79.345198999999994 45.061672000000002 -5.2754009999999996 1;
	setAttr ".radi" 2;
	setAttr ".fbxID" 5;
createNode joint -n "RightHandPinky2_Skl" -p "RightHandPinky1_Skl";
	rename -uid "3B708688-2F42-E9E9-B259-F8A9FCE057A6";
	addAttr -ci true -h true -sn "fbxID" -ln "filmboxTypeID" -at "short";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 2;
	setAttr ".t" -type "double3" -0.43407198954624526 0.13319051610579091 0.092261299884297543 ;
	setAttr ".r" -type "double3" 1.1131941385122304e-14 -9.5416640443905503e-15 1.5902773407317578e-14 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.85553599999999996 -0.031119399999999998 0.51680700000000002 0
		 -0.51705699999999999 1.1363700000000001e-06 0.85595100000000002 0 -0.026637299999999999 -0.99951599999999996 -0.0160895 0
		 -81.543498999999997 45.141672 -6.6033210000000002 1;
	setAttr ".radi" 2;
	setAttr ".fbxID" 5;
createNode joint -n "RightHandPinky3_Skl" -p "RightHandPinky2_Skl";
	rename -uid "4C03D557-904E-8D29-2465-89B3BC48A30B";
	addAttr -ci true -h true -sn "fbxID" -ln "filmboxTypeID" -at "short";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 3;
	setAttr ".t" -type "double3" -0.46466713094579681 0.14257831990672454 0.098764247744714595 ;
	setAttr ".r" -type "double3" 1.1131941385122304e-14 -9.5416640443905503e-15 1.5902773407317578e-14 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.85553599999999996 -0.031119399999999998 0.51680700000000002 0
		 -0.51705699999999999 1.1363700000000001e-06 0.85595100000000002 0 -0.026637299999999999 -0.99951599999999996 -0.0160895 0
		 -83.284498999999997 45.204672000000002 -7.6550209999999996 1;
	setAttr ".radi" 2;
	setAttr ".fbxID" 5;
createNode joint -n "RightHandPinky4_Skl" -p "RightHandPinky3_Skl";
	rename -uid "6B3B5868-2848-28E1-67DF-59A0523E675A";
	addAttr -ci true -h true -sn "fbxID" -ln "filmboxTypeID" -at "short";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 4;
	setAttr ".t" -type "double3" -0.58579401764463235 0.1797448566615385 0.12450957176217692 ;
	setAttr ".r" -type "double3" 1.0336802714756427e-14 -1.2722218725854064e-14 9.5416640443905471e-15 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.85553599999999996 -0.031119399999999998 0.51680700000000002 0
		 -0.51705699999999999 1.1363700000000001e-06 0.85595100000000002 0 -0.026637299999999999 -0.99951599999999996 -0.0160895 0
		 -84.008798999999996 45.231672000000003 -8.0925609999999999 1;
	setAttr ".radi" 2;
	setAttr ".fbxID" 5;
createNode joint -n "RightUpLeg_Skl" -p "Hips_Skl";
	rename -uid "397F6BD3-CD46-FD27-444D-CEAD2F8927A7";
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
	setAttr ".uoc" 1;
	setAttr ".oc" 1;
	setAttr ".t" -type "double3" -0.59764748811721846 -1.0566100921857062 -0.21729375422003686 ;
	setAttr ".r" -type "double3" -1.7655625192200634e-31 -3.1805546814635168e-15 6.3611093629270335e-15 ;
	setAttr ".jo" -type "double3" -179.99999999999986 2.7003134116908623 86.000000000000085 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.06967901736048665 0.99645637236797813 -0.047111914702400531 0
		 0.99756405025982431 -0.069756473744123859 -2.338407245616736e-15 0 -0.0032863610409757382 -0.046997152446021873 -0.99888961727163528 0
		 -0.59764748811721835 6.4926309585571289 -0.21729375422003686 1;
	setAttr ".radi" 2;
	setAttr -k on ".atoms_poleVector" -type "double3" -10.295199966395105 -7.740328311920166 
		23.603416763902558 ;
	setAttr ".fbxID" 5;
createNode joint -n "RightUpLeg_Roll_01_Skl" -p "RightUpLeg_Skl";
	rename -uid "7ED9152E-E44E-612B-2B26-94B2AD654D4E";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 2;
	setAttr ".t" -type "double3" -0.61447461211641397 0.042974029443822337 0.016088185335909916 ;
	setAttr ".r" -type "double3" 9.1440947092076103e-15 3.3793393490549868e-15 2.6966208789650188e-31 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" -177.30625471552722 0.18829495654138859 86.004427137230707 ;
	setAttr ".bps" -type "matrix" 1 6.478107980600889e-18 -4.3368086899420177e-18 0 6.9388939039072284e-18 0.99999999999999989 4.8572257327350599e-17 0
		 1.0408340855860843e-17 -3.4694469519536142e-17 1.0000000000000002 0 -0.59764699999999982 5.8765799999999979 -0.20441500000000001 1;
	setAttr ".radi" 2;
createNode joint -n "RightUpLeg_Roll_02_Skl" -p "RightUpLeg_Roll_01_Skl";
	rename -uid "6C62501C-B34A-E7DA-48A4-E5998B04C116";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 3;
	setAttr ".t" -type "double3" -1.1102230246251565e-16 -0.61606 0.012877999999999945 ;
	setAttr ".r" -type "double3" -6.3611093629270351e-15 6.3611093629270335e-15 -6.3611093629270351e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 6.478107980600889e-18 -4.3368086899420177e-18 0 6.9388939039072284e-18 0.99999999999999989 4.8572257327350599e-17 0
		 1.0408340855860843e-17 -3.4694469519536142e-17 1.0000000000000002 0 -0.59764699999999993 5.2605199999999979 -0.1915370000000001 1;
	setAttr ".radi" 2;
createNode joint -n "RightUpLeg_Roll_03_Skl" -p "RightUpLeg_Roll_02_Skl";
	rename -uid "DFCD6559-6649-0C20-BAF3-359132807FB0";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 4;
	setAttr ".t" -type "double3" 2.2204460492503131e-16 -0.61605000000000043 0.012878999999999974 ;
	setAttr ".r" -type "double3" 3.1805546814635286e-15 -9.5416640443905456e-15 -1.4312496066585825e-13 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 6.478107980600889e-18 -4.3368086899420177e-18 0 6.9388939039072284e-18 0.99999999999999989 4.8572257327350599e-17 0
		 1.0408340855860843e-17 -3.4694469519536142e-17 1.0000000000000002 0 -0.59764699999999971 4.6444699999999974 -0.17865800000000015 1;
	setAttr ".radi" 2;
createNode joint -n "RightUpLeg_Roll_04_Skl" -p "RightUpLeg_Roll_03_Skl";
	rename -uid "B2720B75-8D47-6FBC-1EAC-80ABDD5B8C90";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 5;
	setAttr ".t" -type "double3" 0 -0.61606 0.012877999999999973 ;
	setAttr ".r" -type "double3" -9.5416640443905487e-15 1.5902773407317584e-14 9.5416640443905487e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 6.478107980600889e-18 -4.3368086899420177e-18 0 6.9388939039072284e-18 0.99999999999999989 4.8572257327350599e-17 0
		 1.0408340855860843e-17 -3.4694469519536142e-17 1.0000000000000002 0 -0.59764699999999971 4.0284099999999974 -0.1657800000000002 1;
	setAttr ".radi" 2;
createNode joint -n "RightLeg_Skl" -p "RightUpLeg_Roll_04_Skl";
	rename -uid "255C3F0D-4045-881D-0D03-7B9E9B4CBF95";
	addAttr -ci true -h true -sn "fbxID" -ln "filmboxTypeID" -at "short";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 6;
	setAttr ".t" -type "double3" -4.8811722608288477e-07 -0.61605083150700146 0.012878911462122528 ;
	setAttr ".r" -type "double3" -1.113194138512231e-14 1.0138018047164965e-14 1.272221872585407e-14 ;
	setAttr ".jo" -type "double3" -179.99999999999986 -2.5986865883091337 86.000000000000085 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.069684736842256179 0.99653816476792001 0.045340088356895028 0
		 0.9975640502598242 -0.069756473744123845 -2.3495911664035782e-15 0 0.0031627646830216546 0.04522964218044264 -0.99897160940028162 0
		 -0.59764748811722579 3.4123591684929959 -0.15290108853787771 1;
	setAttr ".radi" 2;
	setAttr ".fbxID" 5;
createNode joint -n "RightLeg_Roll_01_Skl" -p "RightLeg_Skl";
	rename -uid "BA91FFC1-7E4F-5E65-3054-A0A5FBA73E2A";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 7;
	setAttr ".t" -type "double3" -0.5753847457625807 0.040225499509749629 -0.009956322738674861 ;
	setAttr ".r" -type "double3" -6.4008662964453275e-14 5.1684013573782215e-15 1.2722218725854064e-14 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 177.40763503533742 -0.18121337004634938 86.004100229929961 ;
	setAttr ".bps" -type "matrix" 0.99999999999999978 7.2018129307349632e-17 -6.5052130349130266e-18 0
		 1.8252543573793467e-16 0.99999999999999967 -4.8572257327350599e-17 0 2.7321894746634712e-17 8.3266726846886741e-17 0.99999999999999967 0
		 -0.59764699999999993 2.835709999999998 -0.16904300000000014 1;
	setAttr ".radi" 2;
createNode joint -n "RightLeg_Roll_02_Skl" -p "RightLeg_Roll_01_Skl";
	rename -uid "84417536-DB4A-AE7A-1C94-70A6F9E51180";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".t" -type "double3" -1.1102230246251565e-16 -0.57665000000000033 -0.016142999999999491 ;
	setAttr ".r" -type "double3" -6.3611093629270335e-15 6.3611093629270335e-15 6.3611093629270335e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.99999999999999978 7.2018129307349632e-17 -6.5052130349130266e-18 0
		 1.8252543573793467e-16 0.99999999999999967 -4.8572257327350599e-17 0 2.7321894746634712e-17 8.3266726846886741e-17 0.99999999999999967 0
		 -0.59764700000000015 2.2590599999999972 -0.1851860000000001 1;
	setAttr ".radi" 2;
createNode joint -n "RightLeg_Roll_03_Skl" -p "RightLeg_Roll_02_Skl";
	rename -uid "38876050-F14E-AB22-B588-AA9C5675904F";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 1;
	setAttr ".t" -type "double3" -1.1102230246251565e-16 -0.57665000000000011 -0.016141999999999573 ;
	setAttr ".r" -type "double3" -6.3611093629270335e-15 1.2722218725854067e-14 -7.0622500768802555e-31 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.99999999999999978 7.2018129307349632e-17 -6.5052130349130266e-18 0
		 1.8252543573793467e-16 0.99999999999999967 -4.8572257327350599e-17 0 2.7321894746634712e-17 8.3266726846886741e-17 0.99999999999999967 0
		 -0.59764700000000037 1.6824099999999975 -0.20132800000000017 1;
	setAttr ".radi" 2;
createNode joint -n "RightLeg_Roll_04_Skl" -p "RightLeg_Roll_03_Skl";
	rename -uid "52FCA68C-D643-4614-31E7-EABC3FED2CB8";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 2;
	setAttr ".t" -type "double3" -2.2204460492503131e-16 -0.57666 -0.016141999999999546 ;
	setAttr ".r" -type "double3" -3.1805546814635176e-15 1.2722218725854067e-14 -3.1805546814635176e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.99999999999999978 7.2018129307349632e-17 -6.5052130349130266e-18 0
		 1.8252543573793467e-16 0.99999999999999967 -4.8572257327350599e-17 0 2.7321894746634712e-17 8.3266726846886741e-17 0.99999999999999967 0
		 -0.59764700000000071 1.105749999999998 -0.21747000000000019 1;
	setAttr ".radi" 2;
createNode joint -n "RightFoot_Skl" -p "RightLeg_Roll_04_Skl";
	rename -uid "D4E54649-C34D-4C10-72C1-3CA57BA3360C";
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
	setAttr ".t" -type "double3" -4.7321604557115649e-07 -0.57664621190875931 -0.016142505701942866 ;
	setAttr ".r" -type "double3" 180 180.00000000000003 -180 ;
	setAttr ".jo" -type "double3" 175.58361684953286 64.876599139049645 86.000000000000369 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.029616453157002277 0.42353501230586932 -0.90539547108071261 0
		 0.99946542196927257 -1.7244777266613427e-14 0.032693581752133972 0 0.013846876549697115 -0.90587973448524961 -0.42330859979304747 0
		 -0.59764747321604639 0.5291037880912387 -0.23361250570194356 1;
	setAttr ".radi" 2;
	setAttr -k on ".atoms_ikSoftDistance" 0.05;
	setAttr -k on ".atoms_ikTollerance" 0.001;
	setAttr ".fbxID" 5;
createNode joint -n "RightToeBase_Skl" -p "RightFoot_Skl";
	rename -uid "1691218B-E14B-7EC4-6DE4-BDBE9A584E0C";
	addAttr -ci true -h true -sn "fbxID" -ln "filmboxTypeID" -at "short";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".oc" 1;
	setAttr ".t" -type "double3" -1.0879466691054174 0.033881520977334989 -0.11860343318591882 ;
	setAttr ".r" -type "double3" 180 180.00000000000011 -180 ;
	setAttr ".jo" -type "double3" 0.77538331646094538 -22.454178566140531 -1.4908850069360235e-16 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.032659827789357831 0.045429086726435974 -0.99843353996546558 0
		 0.99939400050517313 -0.013518607271496574 0.032076143965643122 0 -0.012040240987418644 -0.99887609108269282 -0.04584307210826849 0
		 -0.59764747321604628 0.17576072876704374 0.8027230427919867 1;
	setAttr ".radi" 2;
	setAttr ".fbxID" 5;
createNode joint -n "RightToeEnd_Skl" -p "RightToeBase_Skl";
	rename -uid "9685B6BC-ED4D-5624-29EC-6BB495A08BC2";
	addAttr -ci true -h true -sn "fbxID" -ln "filmboxTypeID" -at "short";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".oc" 2;
	setAttr ".t" -type "double3" -1.6389516777431417 0.066628493966064184 0.10387754202041181 ;
	setAttr ".r" -type "double3" -179.99999999999997 179.99999999999994 179.99999999999997 ;
	setAttr ".jo" -type "double3" 3.4150945850063708e-06 0 0 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.032659800000000003 0.0454291 -0.99843400000000004 0
		 0.999394 -0.0135187 0.032076100000000003 0 -0.0120403 -0.99887599999999999 -0.045843099999999998 0
		 -14.200699999999999 -101.791568 21.831999 1;
	setAttr ".radi" 2;
	setAttr ".fbxID" 5;
createNode joint -n "SpineHolder_Skl" -p "Hips_Skl";
	rename -uid "0BF0240A-7040-A231-E213-8697370BC5B6";
	addAttr -ci true -h true -sn "fbxID" -ln "filmboxTypeID" -at "short";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 1;
	setAttr ".t" -type "double3" 4.4408920985006124e-16 -0.83384110537595202 2.4651903288156619e-31 ;
	setAttr ".r" -type "double3" 1.2722218725854053e-14 -1.2722218725854081e-14 1.2722218725854067e-13 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1;
	setAttr ".radi" 2;
	setAttr ".fbxID" 5;
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
	setAttr ".ren" -type "string" "arnold";
select -ne :defaultResolution;
	setAttr ".pa" 1;
select -ne :defaultColorMgtGlobals;
	setAttr ".cfe" yes;
	setAttr ".cfp" -type "string" "<MAYA_RESOURCES>/OCIO-configs/Maya2022-default/config.ocio";
	setAttr ".wsn" -type "string" "ACEScg";
select -ne :hardwareRenderGlobals;
	setAttr ".ctrs" 256;
	setAttr ".btrs" 512;
connectAttr "Hips_Skl.s" "LeftUpLeg_Skl.is";
connectAttr "LeftUpLeg_Skl.s" "LeftUpLeg_Roll_01_Skl.is";
connectAttr "LeftUpLeg_Roll_01_Skl.s" "LeftUpLeg_Roll_02_Skl.is";
connectAttr "LeftUpLeg_Roll_02_Skl.s" "LeftUpLeg_Roll_03_Skl.is";
connectAttr "LeftUpLeg_Roll_03_Skl.s" "LeftUpLeg_Roll_04_Skl.is";
connectAttr "LeftUpLeg_Roll_04_Skl.s" "LeftLeg_Skl.is";
connectAttr "LeftLeg_Skl.s" "LeftLeg_Roll_01_Skl.is";
connectAttr "LeftLeg_Roll_01_Skl.s" "LeftLeg_Roll_02_Skl.is";
connectAttr "LeftLeg_Roll_02_Skl.s" "LeftLeg_Roll_03_Skl.is";
connectAttr "LeftLeg_Roll_03_Skl.s" "LeftLeg_Roll_04_Skl.is";
connectAttr "LeftLeg_Roll_04_Skl.s" "LeftFoot_Skl.is";
connectAttr "LeftFoot_Skl.s" "LeftToeBase_Skl.is";
connectAttr "LeftToeBase_Skl.s" "LeftToeEnd_Skl.is";
connectAttr "Hips_Skl.s" "Spine_Skl.is";
connectAttr "Spine_Skl.s" "Spine1_Skl.is";
connectAttr "Spine1_Skl.s" "LeftShoulder_Skl.is";
connectAttr "LeftShoulder_Skl.s" "LeftArm_Skl.is";
connectAttr "LeftArm_Skl.s" "LeftArm_Roll_01_Skl.is";
connectAttr "LeftArm_Roll_01_Skl.s" "LeftArm_Roll_02_Skl.is";
connectAttr "LeftArm_Roll_02_Skl.s" "LeftArm_Roll_03_Skl.is";
connectAttr "LeftArm_Roll_03_Skl.s" "LeftArm_Roll_04_Skl.is";
connectAttr "LeftArm_Roll_04_Skl.s" "LeftForeArm_Skl.is";
connectAttr "LeftForeArm_Skl.s" "LeftForeArm_Roll_01_Skl.is";
connectAttr "LeftForeArm_Roll_01_Skl.s" "LeftForeArm_Roll_02_Skl.is";
connectAttr "LeftForeArm_Roll_02_Skl.s" "LeftForeArm_Roll_03_Skl.is";
connectAttr "LeftForeArm_Roll_03_Skl.s" "LeftForeArm_Roll_04_Skl.is";
connectAttr "LeftForeArm_Roll_04_Skl.s" "LeftForeArm_Roll_05_Skl.is";
connectAttr "LeftForeArm_Roll_05_Skl.s" "LeftHand_Skl.is";
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
connectAttr "LeftHand_Skl.s" "LeftHandPinky1_Skl.is";
connectAttr "LeftHandPinky1_Skl.s" "LeftHandPinky2_Skl.is";
connectAttr "LeftHandPinky2_Skl.s" "LeftHandPinky3_Skl.is";
connectAttr "LeftHandPinky3_Skl.s" "LeftHandPinky4_Skl.is";
connectAttr "Spine1_Skl.s" "Neck_Skl.is";
connectAttr "Neck_Skl.s" "Neck1_Skl.is";
connectAttr "Neck1_Skl.s" "Head_Skl.is";
connectAttr "Head_Skl.s" "Head_End_Skl.is";
connectAttr "Head_Skl.s" "LeftEye_Skl.is";
connectAttr "Head_Skl.s" "RightEye_Skl.is";
connectAttr "Head_Skl.s" "Jaw_Skl.is";
connectAttr "Spine1_Skl.s" "RightShoulder_Skl.is";
connectAttr "RightShoulder_Skl.s" "RightArm_Skl.is";
connectAttr "RightArm_Skl.s" "RightArm_Roll_01_Skl.is";
connectAttr "RightArm_Roll_01_Skl.s" "RightArm_Roll_02_Skl.is";
connectAttr "RightArm_Roll_02_Skl.s" "RightArm_Roll_03_Skl.is";
connectAttr "RightArm_Roll_03_Skl.s" "RightArm_Roll_04_Skl.is";
connectAttr "RightArm_Roll_04_Skl.s" "RightForeArm_Skl.is";
connectAttr "RightForeArm_Skl.s" "RightForeArm_Roll_01_Skl.is";
connectAttr "RightForeArm_Roll_01_Skl.s" "RightForeArm_Roll_02_Skl.is";
connectAttr "RightForeArm_Roll_02_Skl.s" "RightForeArm_Roll_03_Skl.is";
connectAttr "RightForeArm_Roll_03_Skl.s" "RightForeArm_Roll_04_Skl.is";
connectAttr "RightForeArm_Roll_04_Skl.s" "RightForeArm_Roll_05_Skl.is";
connectAttr "RightForeArm_Roll_05_Skl.s" "RightHand_Skl.is";
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
connectAttr "RightHand_Skl.s" "RightHandPinky1_Skl.is";
connectAttr "RightHandPinky1_Skl.s" "RightHandPinky2_Skl.is";
connectAttr "RightHandPinky2_Skl.s" "RightHandPinky3_Skl.is";
connectAttr "RightHandPinky3_Skl.s" "RightHandPinky4_Skl.is";
connectAttr "Hips_Skl.s" "RightUpLeg_Skl.is";
connectAttr "RightUpLeg_Skl.s" "RightUpLeg_Roll_01_Skl.is";
connectAttr "RightUpLeg_Roll_01_Skl.s" "RightUpLeg_Roll_02_Skl.is";
connectAttr "RightUpLeg_Roll_02_Skl.s" "RightUpLeg_Roll_03_Skl.is";
connectAttr "RightUpLeg_Roll_03_Skl.s" "RightUpLeg_Roll_04_Skl.is";
connectAttr "RightUpLeg_Roll_04_Skl.s" "RightLeg_Skl.is";
connectAttr "RightLeg_Skl.s" "RightLeg_Roll_01_Skl.is";
connectAttr "RightLeg_Roll_01_Skl.s" "RightLeg_Roll_02_Skl.is";
connectAttr "RightLeg_Roll_02_Skl.s" "RightLeg_Roll_03_Skl.is";
connectAttr "RightLeg_Roll_03_Skl.s" "RightLeg_Roll_04_Skl.is";
connectAttr "RightLeg_Roll_04_Skl.s" "RightFoot_Skl.is";
connectAttr "RightFoot_Skl.s" "RightToeBase_Skl.is";
connectAttr "RightToeBase_Skl.s" "RightToeEnd_Skl.is";
connectAttr "Hips_Skl.s" "SpineHolder_Skl.is";
dataStructure -fmt "raw" -as "name=NameAndID:string=name:int32=ID";
dataStructure -fmt "raw" -as "name=mapManager_suelo:string=value";
dataStructure -fmt "raw" -as "name=notes_trees_left:string=value";
dataStructure -fmt "raw" -as "name=notes_decayGrassPatchB_parShape:string=value";
dataStructure -fmt "raw" -as "name=notes_pPlane2:string=value";
dataStructure -fmt "raw" -as "name=notes_groundWoods_c_geo1:string=value";
dataStructure -fmt "raw" -as "name=mapManager_baseLeaves:string=value";
dataStructure -fmt "raw" -as "name=f_1:float=value";
dataStructure -fmt "raw" -as "name=notes_juneBackYard:string=value";
dataStructure -fmt "raw" -as "name=mapManager_pPlane2:string=value";
dataStructure -fmt "raw" -as "name=notes_slopesGroundGrassA_Combined:string=value";
dataStructure -fmt "raw" -as "name=notes_grass_c_geo:string=value";
dataStructure -fmt "raw" -as "name=mapManager_base_hojas:string=value";
dataStructure -fmt "raw" -as "name=notes_pPlane6:string=value";
dataStructure -fmt "raw" -as "name=mapManager_pPlane3:string=value";
dataStructure -fmt "raw" -as "name=notes_base_left:string=value";
dataStructure -fmt "raw" -as "name=notes_slopesGroundGrassB_Combined:string=value";
dataStructure -fmt "raw" -as "name=keyValueStructure:string=value";
dataStructure -fmt "raw" -as "name=Offset:float[3]=value";
dataStructure -fmt "raw" -as "name=OrgStruct:float[3]=Origin Point";
dataStructure -fmt "raw" -as "name=notes_decayGrassPatchA_parShape:string=value";
dataStructure -fmt "raw" -as "name=mapManager_baseScatt:string=value";
dataStructure -fmt "raw" -as "name=mapManager_groundWoods_c_geo1:string=value";
dataStructure -fmt "raw" -as "name=faceConnectMarkerStructure:bool=faceConnectMarker:string[200]=faceConnectOutputGroups";
dataStructure -fmt "raw" -as "name=Curvature:float=mean:float=gaussian:float=ABS:float=RMS";
dataStructure -fmt "raw" -as "name=notes_degraded:string=value";
dataStructure -fmt "raw" -as "name=mapManager_pPlane6:string=value";
dataStructure -fmt "raw" -as "name=notes_grassBase:string=value";
dataStructure -fmt "raw" -as "name=notes_wildPatchH_parShape:string=value";
dataStructure -fmt "raw" -as "name=mapManager_grass_c_geo:string=value";
dataStructure -fmt "raw" -as "name=notes_wildPatchC_parShape:string=value";
dataStructure -fmt "raw" -as "name=mapManager_snapshot_Combined:string=value";
dataStructure -fmt "raw" -as "name=mapManager_grassBase:string=value";
dataStructure -fmt "raw" -as "name=externalContentTablZ:string=nodZ:string=key:string=upath:uint32=upathcrc:string=rpath:string=roles";
dataStructure -fmt "raw" -as "name=notes_bushes_parShape:string=value";
dataStructure -fmt "raw" -as "name=notes_groundD_parShape:string=value";
dataStructure -fmt "raw" -as "name=notes_slopesGroundGrassD_Combined:string=value";
dataStructure -fmt "raw" -as "name=mapManager_pPlane1:string=value";
dataStructure -fmt "raw" -as "name=notes_decayGrassPatchC_parShape:string=value";
dataStructure -fmt "raw" -as "name=notes_widlPatchB_parShape:string=value";
dataStructure -fmt "raw" -as "name=mapManager_ground_c_geo:string=value";
dataStructure -fmt "raw" -as "name=mapManager_base_right:string=value";
dataStructure -fmt "raw" -as "name=mapManager_slopesMountainsGrass_Combined:string=value";
dataStructure -fmt "raw" -as "name=notes_groundA_parShape:string=value";
dataStructure -fmt "raw" -as "name=notes_pPlane3:string=value";
dataStructure -fmt "raw" -as "name=DiffArea:float=value";
dataStructure -fmt "raw" -as "name=IdStruct:int32=ID";
dataStructure -fmt "raw" -as "name=mapManager_grass_c_geo1:string=value";
dataStructure -fmt "raw" -as "name=notes_wildPatchF_parShape:string=value";
dataStructure -fmt "raw" -as "name=notes_groundB_parShape:string=value";
dataStructure -fmt "raw" -as "name=mapManager_degraded:string=value";
dataStructure -fmt "raw" -as "name=notes_grassJuneBackYard_parShape:string=value";
dataStructure -fmt "raw" -as "name=notes_wildPatchD_parShape:string=value";
dataStructure -fmt "raw" -as "name=notes_pPlane5:string=value";
dataStructure -fmt "raw" -as "name=notes_mountains_parShape:string=value";
dataStructure -fmt "raw" -as "name=mapManager_juneBackYard:string=value";
dataStructure -fmt "raw" -as "name=notes_trees_left1:string=value";
dataStructure -fmt "raw" -as "name=notes_slopesGroundGrassC_Combined:string=value";
dataStructure -fmt "raw" -as "name=Blur3dMetaData:string=Blur3dValue";
dataStructure -fmt "raw" -as "name=notes_ferns_parShape:string=value";
dataStructure -fmt "raw" -as "name=mapManager_baseScatter:string=value";
dataStructure -fmt "raw" -as "name=notes_groundC_parShape:string=value";
dataStructure -fmt "raw" -as "name=OffStruct:float=Offset";
dataStructure -fmt "raw" -as "name=notes_right_parShape:string=value";
dataStructure -fmt "raw" -as "name=mapManager_trees_left1:string=value";
dataStructure -fmt "raw" -as "name=notes_ground:string=value";
dataStructure -fmt "raw" -as "name=notes_baseScatter:string=value";
dataStructure -fmt "raw" -as "name=mapManager_polySurface56:string=value";
dataStructure -fmt "raw" -as "name=notes_snapshot_Combined:string=value";
dataStructure -fmt "raw" -as "name=notes_snapshot_floor:string=value";
dataStructure -fmt "raw" -as "name=notes_base_right:string=value";
dataStructure -fmt "raw" -as "name=DiffEdge:float=value";
dataStructure -fmt "raw" -as "name=mapManager_ground:string=value";
dataStructure -fmt "raw" -as "name=notes_decayGrassesCenter_parShape:string=value";
dataStructure -fmt "raw" -as "name=notes_pPlane1:string=value";
dataStructure -fmt "raw" -as "name=notes_baseLeaves:string=value";
dataStructure -fmt "raw" -as "name=notes_decayLeaves_parShape:string=value";
dataStructure -fmt "raw" -as "name=notes_wildPatchE_parShape:string=value";
dataStructure -fmt "raw" -as "name=mapManager_slopesGroundGrassC_Combined:string=value";
dataStructure -fmt "raw" -as "name=f_3:float[3]=value";
dataStructure -fmt "raw" -as "name=mapManager_trees_left:string=value";
dataStructure -fmt "raw" -as "name=notes_left_parShape:string=value";
dataStructure -fmt "raw" -as "name=notes_snapshot_CombinedGrass:string=value";
dataStructure -fmt "raw" -as "name=notes_wildPatchA_parShape:string=value";
dataStructure -fmt "raw" -as "name=notes_wildPatchDegraded_parShape:string=value";
dataStructure -fmt "raw" -as "name=mapManager_snapshot_CombinedGrass:string=value";
dataStructure -fmt "raw" -as "name=notes_slopes_parShape:string=value";
dataStructure -fmt "raw" -as "name=mapManager_slopesGroundGrassA_Combined:string=value";
dataStructure -fmt "raw" -as "name=mapManager_base_left:string=value";
dataStructure -fmt "raw" -as "name=notes_ground_c_geo:string=value";
dataStructure -fmt "raw" -as "name=notes_slopesMountainsGrass_Combined:string=value";
dataStructure -fmt "raw" -as "name=notes_pPlane4:string=value";
dataStructure -fmt "raw" -as "name=faceConnectOutputStructure:bool=faceConnectOutput:string[200]=faceConnectOutputAttributes:string[200]=faceConnectOutputGroups";
dataStructure -fmt "raw" -as "name=notes_floorOrangeConcrete_c_geo:string=value";
dataStructure -fmt "raw" -as "name=notes_decayLeavesCarousel_parShape:string=value";
dataStructure -fmt "raw" -as "name=notes_suelo:string=value";
dataStructure -fmt "raw" -as "name=notes_polySurface56:string=value";
dataStructure -fmt "raw" -as "name=mapManager_slopesGroundGrassD_Combined:string=value";
dataStructure -fmt "raw" -as "name=notes_wildPatchG_parShape:string=value";
dataStructure -fmt "raw" -as "name=mapManager_pPlane5:string=value";
dataStructure -fmt "raw" -as "name=mapManager_floorOrangeConcrete_c_geo:string=value";
dataStructure -fmt "raw" -as "name=mapManager_snapshot_floor:string=value";
dataStructure -fmt "raw" -as "name=notes_baseScatt:string=value";
dataStructure -fmt "raw" -as "name=notes_base_hojas:string=value";
dataStructure -fmt "raw" -as "name=notes_trees_parShape:string=value";
dataStructure -fmt "raw" -as "name=mapManager_pPlane4:string=value";
dataStructure -fmt "raw" -as "name=notes_grass_c_geo1:string=value";
dataStructure -fmt "raw" -as "name=notes_decayGrassPatchD_parShape:string=value";
dataStructure -fmt "raw" -as "name=idStructure:int32=ID";
dataStructure -fmt "raw" -as "name=mapManager_slopesGroundGrassB_Combined:string=value";
// End of atoms_toon_skeleton.ma
