//Maya ASCII 2022 scene
//Name: animation.ma
//Last modified: Fri, Dec 15, 2023 12:25:42 PM
//Codeset: UTF-8
requires maya "2022";
requires "stereoCamera" "10.0";
requires "mtoa" "5.2.2.4";
currentUnit -l centimeter -a degree -t film;
fileInfo "application" "maya";
fileInfo "product" "Maya 2022";
fileInfo "version" "2022";
fileInfo "cutIdentifier" "202110272215-ad32f8f1e6";
fileInfo "osv" "Linux 3.10.0-1160.76.1.el7.x86_64 #1 SMP Wed Aug 10 16:21:17 UTC 2022 x86_64";
fileInfo "UUID" "5CEB0D80-0000-0D99-657C-B6460001A493";
createNode animCurveTU -n "CURVE1";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A14A";
	setAttr ".tan" 9;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
	setAttr -s 11 ".kot[0:10]"  5 5 5 5 5 5 5 5 
		5 5 5;
createNode animCurveTL -n "CURVE2";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A14B";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
createNode animCurveTL -n "CURVE3";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A14C";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
createNode animCurveTL -n "CURVE4";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A14D";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
createNode animCurveTU -n "CURVE5";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A151";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1 2 1 3 1 4 1 5 1 6 1 7 1 8 1 9 1 10 1
		 11 1;
createNode animCurveTU -n "CURVE6";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A155";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
createNode animCurveTU -n "CURVE7";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A152";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1 2 1 3 1 4 1 5 1 6 1 7 1 8 1 9 1 10 1
		 11 1;
createNode animCurveTU -n "CURVE8";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A153";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1 2 1 3 1 4 1 5 1 6 1 7 1 8 1 9 1 10 1
		 11 1;
createNode animCurveTA -n "CURVE9";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A14E";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
createNode animCurveTA -n "CURVE10";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A14F";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
createNode animCurveTA -n "CURVE11";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A150";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
createNode animCurveTU -n "CURVE12";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A154";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 -1.5 2 -1.5 3 -1.5 4 -1.5 5 -1.5 6 -1.5
		 7 -1.5 8 -1.5 9 -1.5 10 -1.5 11 -1.5;
createNode animCurveTL -n "CURVE14";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A157";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
createNode animCurveTL -n "CURVE15";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A158";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 -0.18000000000000002 6 0 7 0 8 0 9 0
		 10 0 11 0;
createNode animCurveTL -n "CURVE16";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A159";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
createNode animCurveTL -n "CURVE18";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A15B";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
createNode animCurveTL -n "CURVE19";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A15C";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 -0.17368561185685394 7 0 8 0 9 0
		 10 0 11 -0.17368561185685394;
createNode animCurveTL -n "CURVE20";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A15D";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
createNode animCurveTL -n "CURVE22";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A15F";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
createNode animCurveTL -n "CURVE23";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A160";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
createNode animCurveTL -n "CURVE24";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A161";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
createNode animCurveTU -n "CURVE26";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A163";
	setAttr ".tan" 9;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
	setAttr -s 11 ".kot[0:10]"  5 5 5 5 5 5 5 5 
		5 5 5;
createNode animCurveTL -n "CURVE27";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A164";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0.14753817361435884
		 10 0.21436465518425996 11 0;
createNode animCurveTL -n "CURVE28";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A165";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0.12586526908754081
		 10 0.12586526908748397 11 0;
createNode animCurveTL -n "CURVE29";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A166";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0.17902442550226283
		 10 0.2162634498017324 11 0;
createNode animCurveTU -n "CURVE30";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A16A";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1 2 1 3 1 4 1 5 1 6 1 7 1 8 1 9 1 10 1
		 11 1;
createNode animCurveTU -n "CURVE31";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A16B";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1 2 1 3 1 4 1 5 1 6 1 7 1 8 1 9 1 10 1
		 11 1;
createNode animCurveTU -n "CURVE32";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A16C";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1 2 1 3 1 4 1 5 1 6 1 7 1 8 1 9 1 10 1
		 11 1;
createNode animCurveTA -n "CURVE33";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A167";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
createNode animCurveTA -n "CURVE34";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A168";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 -78.496561542175542
		 11 0;
createNode animCurveTA -n "CURVE35";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A169";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
createNode animCurveTU -n "CURVE37";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A174";
	setAttr ".tan" 9;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0 12 0 13 0 14 0 15 0 16 0 17 0 18 0 19 0 20 0 21 0 22 0;
	setAttr -s 22 ".kot[0:21]"  5 5 5 5 5 5 5 5 
		5 5 5 5 5 5 5 5 5 5 5 5 5 5;
createNode animCurveTU -n "CURVE38";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A177";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0.25 2 0.25 3 0.25 4 0.25 5 0.25 6 0.25
		 7 0.25 8 0.25 9 0.25 10 0.25 11 0.25 12 0.25 13 0.25 14 0.25 15 0.25 16 0.25 17 0.25
		 18 0.25 19 0.25 20 0.25 21 0.25 22 0.25;
createNode animCurveTL -n "CURVE39";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A16F";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0.16000000000000003 2 0.014561714455147645 3 0.1 4 0.1 5 0.17 6 0.19426376082174363
		 7 0.03 8 0.030000000000000006 9 0.6992511994644599 10 0.67 11 -0.30000000000000004 12 0.12 13 0.17000000000000004 14 -0.22843167999740221 15 -0.2784316799974022
		 16 -0.078431679997402193 17 0 18 -0.15000000000000002 19 0.13 20 -0.89843167999740225 21 -0.51843167999740225 22 -0.2784316799974022;
createNode animCurveTL -n "CURVE40";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A16E";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 -0.32999999999999996 2 -0.1825471037162604 3 -0.20308998783350024 4 -0.1739299901509288 5 -0.073089987833500236
		 6 0 7 -0.33000000000000007 8 -0.33000000000000007 9 0.58495193845262938 10 0.62000000000000011 11 0.06894295992749154 12 0.080000000000000016 13 0.24000000000000002 14 -0.17439119648845666
		 15 -0.17439119648845663 16 0.065608803511543412 17 0 18 0 19 -0.0004606966634587772 20 -0.17439119648845663 21 -0.17439119648845663 22 -0.17439119648845663;
createNode animCurveTL -n "CURVE41";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A170";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0 12 0 13 0 14 0 15 0 16 0 17 0 18 0 19 0 20 0 21 0 22 0;
createNode animCurveTU -n "CURVE42";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A176";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 1 2 1 3 1 4 1 5 1 6 1 7 1 8 1 9 1 10 1
		 11 1 12 1 13 1 14 1 15 1 16 1 17 1 18 1 19 1 20 1 21 1 22 1;
createNode animCurveTA -n "CURVE43";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A171";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0 12 0 13 0 14 0 15 0 16 0 17 0 18 0 19 0 20 0 21 0 22 0;
createNode animCurveTA -n "CURVE44";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A172";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0 12 0 13 0 14 0 15 0 16 0 17 0 18 0 19 0 20 0 21 0 22 0;
createNode animCurveTA -n "CURVE45";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A173";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0 12 0 13 0 14 0 15 0 16 0 17 0 18 0 19 0 20 0 21 0 22 0;
createNode animCurveTU -n "CURVE46";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A175";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 1 2 1 3 1 4 1 5 1 6 1 7 1 8 1 9 1 10 1
		 11 1 12 1 13 1 14 1 15 1 16 1 17 1 18 1 19 1 20 1 21 1 22 1;
createNode animCurveTL -n "CURVE48";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A179";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
createNode animCurveTL -n "CURVE49";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A17A";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
createNode animCurveTL -n "CURVE50";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A17B";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
createNode animCurveTU -n "CURVE52";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A186";
	setAttr ".tan" 9;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0 12 0 13 0 14 0 15 0 16 0 17 0 18 0 19 0 20 0 21 0 22 0;
	setAttr -s 22 ".kot[0:21]"  5 5 5 5 5 5 5 5 
		5 5 5 5 5 5 5 5 5 5 5 5 5 5;
createNode animCurveTL -n "CURVE53";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A17D";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 -0.00040868337673116695 2 0.01150024669643265 3 -0.00072610695608821274 4 0.00072610695608821274 5 -0.00072610695608821274
		 6 0 7 0 8 0 9 0 10 0 11 0 12 0 13 0 14 0 15 0 16 0 17 0 18 0 19 0 20 0 21 0 22 0;
createNode animCurveTL -n "CURVE54";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A17E";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0.031604449685332305 2 0.47130700927465341 3 0.020231767983432292 4 0.020231767983432292 5 0.020231767983432292
		 6 0 7 0 8 0 9 0 10 0.55 11 0.080734902737360489 12 0.012912324668141989 13 0.102912324668142 14 0 15 0 16 0.18000000000000002 17 0 18 0
		 19 -0.070460696663458791 20 0.071469805474720913 21 0 22 -0.38652409850092345;
createNode animCurveTL -n "CURVE55";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A17F";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 -8.6069139933787321e-06 2 0.030166113809233508 3 -5.5097648825608303e-06 4 -5.509764882560832e-06 5 -5.509764882560832e-06
		 6 0 7 0 8 0 9 0 10 0 11 0 12 0 13 0 14 0 15 0 16 0 17 0 18 0 19 0 20 0 21 0 22 0.074594044218251526;
createNode animCurveTU -n "CURVE56";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A183";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 1 2 1 3 1 4 1 5 1 6 1 7 1 8 1 9 1 10 1
		 11 1 12 1 13 1 14 1 15 1 16 1 17 1 18 1 19 1 20 1 21 1 22 1;
createNode animCurveTU -n "CURVE57";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A187";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0.62000000000000011 2 0.21000000000000002 3 0.62000000000000011 4 0.62000000000000011 5 0
		 6 0 7 0.62000000000000011 8 0.62000000000000011 9 0.38000000000000006 10 0.28 11 0.51499999999999935 12 0.60000000000000009 13 0.74 14 1 15 1 16 1
		 17 0.48000000000000009 18 0 19 0.14333333333333334 20 1 21 1 22 1;
createNode animCurveTU -n "CURVE58";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A184";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 1 2 1 3 1 4 1 5 1 6 1 7 1 8 1 9 1 10 1
		 11 1 12 1 13 1 14 1 15 1 16 1 17 1 18 1 19 1 20 1 21 1 22 1;
createNode animCurveTU -n "CURVE59";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A185";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 1 2 1 3 1 4 1 5 1 6 1 7 1 8 1 9 1 10 1
		 11 1 12 1 13 1 14 1 15 1 16 1 17 1 18 1 19 1 20 1 21 1 22 1;
createNode animCurveTU -n "CURVE60";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A188";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0.05000000000000001 2 0.29000000000000004 3 0.12000000000000002 4 0.12000000000000002 5 0.18400000000000005
		 6 0.080000000000000016 7 0 8 0 9 0.090000000000000011 10 0.080000000000000016 11 0 12 0.134 13 0.114 14 0 15 0.17 16 0.17 17 0
		 18 0.080000000000000016 19 0.13 20 0 21 0 22 0.07;
createNode animCurveTA -n "CURVE61";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A180";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 -0.015602189373616794 2 9.3965078401455031 3 -0.01558177246827519 4 -0.015581772468274316 5 -0.015593454425728679
		 6 8.0228670159339099 7 0 8 0 9 0 10 0 11 0 12 0 13 0 14 0 15 0 16 0 17 0 18 0 19 0 20 0 21 0
		 22 13.931095464698046;
createNode animCurveTA -n "CURVE62";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A181";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0.00020175498025795774 2 -0.00038063036938065347 3 -0.0008230340727349584 4 0.0008230340727349584 5 0.00055964042179761499
		 6 0 7 0 8 0 9 0 10 0 11 0 12 0 13 0 14 0 15 0 16 0 17 0 18 0 19 0 20 0 21 0 22 0;
createNode animCurveTA -n "CURVE63";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A182";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0.74086168578551947 2 -1.3978072454561092 3 -3.0235710195624663 4 3.0235710195624663 5 2.0554314670204286
		 6 0 7 0 8 0 9 0 10 0 11 0 12 0 13 0 14 0 15 0 16 0 17 0 18 0 19 0 20 0 21 0 22 0;
createNode animCurveTU -n "CURVE64";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A189";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0.14 12 0 13 0 14 0.06 15 0.06 16 0 17 0.21000000000000002 18 0.090000000000000011 19 0 20 0.14 21 0.06 22 0.22000000000000003;
createNode animCurveTL -n "CURVE66";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A18B";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 -0.16773463469593017 7 0 8 0 9 0
		 10 0 11 -0.16773463469593017;
createNode animCurveTL -n "CURVE67";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A18C";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
createNode animCurveTL -n "CURVE68";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A18D";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
createNode animCurveTL -n "CURVE70";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A18F";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 -0.1416409371459908 9 0
		 10 0 11 0;
createNode animCurveTL -n "CURVE71";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A190";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 -0.071474414255210325 4 -0.27 5 -0.30000000000000004 6 0 7 -0.30000000000000004
		 8 -0.1062307028935828 9 0 10 -0.15000000000000002 11 0;
createNode animCurveTL -n "CURVE72";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A191";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
createNode animCurveTL -n "CURVE74";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A193";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
createNode animCurveTL -n "CURVE75";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A194";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 -0.22000000000000003 2 0 3 -0.27 4 -0.071474414255210339 5 -0.13 6 0
		 7 -0.25 8 -0.1770511714894373 9 -0.2 10 -0.2 11 0;
createNode animCurveTL -n "CURVE76";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A195";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
createNode animCurveTL -n "CURVE78";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A197";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
createNode animCurveTL -n "CURVE79";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A198";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 -0.088525585744732863 5 -0.2 6 0.07 7 0 8 0
		 9 0 10 0 11 0.07;
createNode animCurveTL -n "CURVE80";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A199";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
createNode animCurveTL -n "CURVE82";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A19B";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 -0.24000000000000005 2 -0.24000000000000005 3 -0.24000000000000005 4 -0.24000000000000005 5 -0.24000000000000005
		 6 0 7 0 8 0 9 0 10 0 11 0;
createNode animCurveTL -n "CURVE83";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A19C";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
createNode animCurveTL -n "CURVE84";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A19D";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
createNode animCurveTU -n "CURVE86";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A1A8";
	setAttr ".tan" 9;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0 12 0 13 0 14 0 15 0 16 0 17 0 18 0 19 0 20 0 21 0 22 0;
	setAttr -s 22 ".kot[0:21]"  5 5 5 5 5 5 5 5 
		5 5 5 5 5 5 5 5 5 5 5 5 5 5;
createNode animCurveTL -n "CURVE87";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A19F";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0 12 0 13 0 14 0 15 0 16 0 17 0 18 0 19 0 20 0 21 0 22 0;
createNode animCurveTL -n "CURVE88";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A1A0";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0 12 0 13 0 14 0 15 0 16 0 17 -0.29734454027487772 18 0 19 0 20 0 21 0 22 0;
createNode animCurveTL -n "CURVE89";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A1A1";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0 12 0 13 0 14 0 15 0 16 0 17 0 18 0 19 0 20 0 21 0 22 0;
createNode animCurveTU -n "CURVE90";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A1A5";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 1 2 1 3 1 4 1 5 1 6 1 7 1 8 1 9 1 10 1
		 11 1 12 1 13 1 14 1 15 1 16 1 17 1 18 1 19 1 20 1 21 1 22 1;
createNode animCurveTU -n "CURVE91";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A1A6";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 1 2 1 3 1 4 1 5 1 6 1 7 1 8 1 9 1 10 1
		 11 1 12 1 13 1 14 1 15 1 16 1 17 1 18 1 19 1 20 1 21 1 22 1;
createNode animCurveTU -n "CURVE92";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A1A7";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 1 2 1 3 1 4 1 5 1 6 1 7 1 8 1 9 1 10 1
		 11 1 12 1 13 1 14 1 15 1 16 1 17 1 18 1 19 1 20 1 21 1 22 1;
createNode animCurveTA -n "CURVE93";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A1A2";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0 12 0 13 0 14 0 15 0 16 0 17 0 18 0 19 0 20 0 21 0 22 0;
createNode animCurveTA -n "CURVE94";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A1A3";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0 12 0 13 0 14 0 15 0 16 0 17 0 18 0 19 0 20 0 21 0 22 0;
createNode animCurveTA -n "CURVE95";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A1A4";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0 12 0 13 0 14 0 15 0 16 0 17 0 18 0 19 0 20 0 21 0 22 0;
createNode animCurveTU -n "CURVE97";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A1AA";
	setAttr ".tan" 9;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
	setAttr -s 11 ".kot[0:10]"  5 5 5 5 5 5 5 5 
		5 5 5;
createNode animCurveTL -n "CURVE98";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A1AB";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0.096616565669555635 2 0.096616565669555635 3 0.096616565669555635 4 0.23435678372989677 5 0.096616565669555621
		 6 0 7 0.096616565669555635 8 0.096616565669555635 9 0.13446514576027963 10 0.37399024755755167 11 0;
createNode animCurveTL -n "CURVE99";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A1AC";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0.30233771847193225 2 0.30233771847193225 3 0.30233771847193225 4 0.57258242537261594 5 0.30233771847193225
		 6 0 7 0.30233771847193225 8 0.30233771847193225 9 0.15116885923596615 10 0.45232295116773003 11 0;
createNode animCurveTL -n "CURVE100";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A1AD";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0.082156411134494789 5 0 6 0.16783902694371672 7 0 8 0
		 9 0.083919513471857402 10 0 11 0.16783902694371672;
createNode animCurveTU -n "CURVE101";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A1B1";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1 2 1 3 1 4 1 5 1 6 1 7 1 8 1 9 1 10 1
		 11 1;
createNode animCurveTU -n "CURVE102";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A1B2";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1 2 1 3 1 4 1 5 1 6 1 7 1 8 1 9 1 10 1
		 11 1;
createNode animCurveTU -n "CURVE103";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A1B3";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1 2 1 3 1 4 1 5 1 6 1 7 1 8 1 9 1 10 1
		 11 1;
createNode animCurveTA -n "CURVE104";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A1AE";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
createNode animCurveTA -n "CURVE105";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A1AF";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
createNode animCurveTA -n "CURVE106";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A1B0";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
createNode animCurveTU -n "CURVE108";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A1B5";
	setAttr ".tan" 9;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
	setAttr -s 11 ".kot[0:10]"  5 5 5 5 5 5 5 5 
		5 5 5;
createNode animCurveTL -n "CURVE109";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A1B6";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
createNode animCurveTL -n "CURVE110";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A1B7";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 -0.17000000000000004 8 -0.17000000000000004
		 9 0 10 0 11 0;
createNode animCurveTL -n "CURVE111";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A1B8";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
createNode animCurveTU -n "CURVE112";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A1BC";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1 2 1 3 1 4 1 5 1 6 1 7 1 8 1 9 1 10 1
		 11 1;
createNode animCurveTU -n "CURVE113";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A1BD";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1 2 1 3 1 4 1 5 1 6 1 7 1 8 1 9 1 10 1
		 11 1;
createNode animCurveTU -n "CURVE114";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A1BE";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1 2 1 3 1 4 1 5 1 6 1 7 1 8 1 9 1 10 1
		 11 1;
createNode animCurveTA -n "CURVE115";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A1B9";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
createNode animCurveTA -n "CURVE116";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A1BA";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
createNode animCurveTA -n "CURVE117";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A1BB";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
createNode animCurveTU -n "CURVE119";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A1C0";
	setAttr ".tan" 9;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
	setAttr -s 11 ".kot[0:10]"  5 5 5 5 5 5 5 5 
		5 5 5;
createNode animCurveTL -n "CURVE120";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A1C1";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
createNode animCurveTL -n "CURVE121";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A1C2";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
createNode animCurveTL -n "CURVE122";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A1C3";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
createNode animCurveTU -n "CURVE123";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A1C7";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1 2 1 3 1 4 1 5 1 6 1 7 1 8 1 9 1 10 1
		 11 1;
createNode animCurveTU -n "CURVE124";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A1C8";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1 2 1 3 1 4 1 5 1 6 1 7 1 8 1 9 1 10 1
		 11 1;
createNode animCurveTU -n "CURVE125";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A1C9";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1 2 1 3 1 4 1 5 1 6 1 7 1 8 1 9 1 10 1
		 11 1;
createNode animCurveTA -n "CURVE126";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A1C4";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
createNode animCurveTA -n "CURVE127";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A1C5";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
createNode animCurveTA -n "CURVE128";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A1C6";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
createNode animCurveTL -n "CURVE130";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A1CB";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
createNode animCurveTL -n "CURVE131";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A1CC";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0.70000000000000018 2 0 3 0.33000000000000007 4 0 5 0.31000000000000005 6 0 7 0.31000000000000005
		 8 0.31000000000000005 9 0.36322897907849661 10 0.44322897907849662 11 0;
createNode animCurveTL -n "CURVE132";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A1CD";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
createNode animCurveTL -n "CURVE134";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A1CF";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
createNode animCurveTL -n "CURVE135";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A1D0";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0.70273702621782386 2 0.30098699153212588 3 0 4 0.52475628863842938 5 0.64934605434047377
		 6 0.35429395307207368 7 0.41000000000000003 8 0.37 9 0.48328187438310538 10 0.80570771186753476 11 0.35429395307207368;
createNode animCurveTL -n "CURVE136";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A1D1";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
createNode animCurveTL -n "CURVE138";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A1D3";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
createNode animCurveTL -n "CURVE139";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A1D4";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
createNode animCurveTL -n "CURVE140";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A1D5";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
createNode animCurveTL -n "CURVE142";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A1D7";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
createNode animCurveTL -n "CURVE143";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A1D8";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
createNode animCurveTL -n "CURVE144";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A1D9";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
createNode animCurveTU -n "CURVE146";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A1E4";
	setAttr ".tan" 9;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0 12 0 13 0 14 0 15 0 16 0 17 0 18 0 19 0 20 0 21 0 22 0;
	setAttr -s 22 ".kot[0:21]"  5 5 5 5 5 5 5 5 
		5 5 5 5 5 5 5 5 5 5 5 5 5 5;
createNode animCurveTL -n "CURVE147";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A1DB";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0 12 0 13 0 14 0 15 0 16 0 17 0 18 0 19 0 20 0 21 0 22 0;
createNode animCurveTL -n "CURVE148";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A1DC";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 -0.14999999999999983 12 0 13 0 14 -0.30000000000000004 15 -0.30000000000000004 16 -0.30000000000000004 17 0 18 0 19 0 20 -0.30000000000000004 21 -0.30000000000000004
		 22 -0.30000000000000004;
createNode animCurveTL -n "CURVE149";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A1DD";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0 12 0 13 0 14 0 15 0 16 0 17 0 18 0 19 0 20 0 21 0 22 0;
createNode animCurveTU -n "CURVE150";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A1E1";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 1.1 2 1.1 3 1.1 4 1.1 5 1.1 6 1.1 7 1.1
		 8 1.1 9 1.1 10 1.1 11 1.1 12 1.1 13 1.1 14 1.1 15 1.1 16 1.1 17 1.1 18 1.1 19 1.1
		 20 1.1 21 1.1 22 1.1;
createNode animCurveTU -n "CURVE151";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A1E2";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 1 2 1 3 1 4 1 5 1 6 1 7 1 8 1 9 1 10 1
		 11 1 12 1 13 1 14 1 15 1 16 1 17 1 18 1 19 1 20 1 21 1 22 1;
createNode animCurveTU -n "CURVE152";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A1E3";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 1 2 1 3 1 4 1 5 1 6 1 7 1 8 1 9 1 10 1
		 11 1 12 1 13 1 14 1 15 1 16 1 17 1 18 1 19 1 20 1 21 1 22 1;
createNode animCurveTA -n "CURVE153";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A1DE";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0 12 0 13 0 14 0 15 0 16 0 17 0 18 0 19 0 20 0 21 0 22 0;
createNode animCurveTA -n "CURVE154";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A1DF";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0 12 0 13 0 14 0 15 0 16 0 17 0 18 0 19 0 20 0 21 0 22 0;
createNode animCurveTA -n "CURVE155";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A1E0";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0 12 0 13 0 14 0 15 0 16 0 17 0 18 0 19 0 20 0 21 0 22 0;
createNode animCurveTU -n "CURVE157";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A1EF";
	setAttr ".tan" 9;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0 12 0 13 0 14 0 15 0 16 0 17 0 18 0 19 0 20 0 21 0 22 0;
	setAttr -s 22 ".kot[0:21]"  5 5 5 5 5 5 5 5 
		5 5 5 5 5 5 5 5 5 5 5 5 5 5;
createNode animCurveTL -n "CURVE158";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A1E6";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0 12 0 13 0 14 0 15 0 16 0 17 0 18 0 19 0 20 0 21 0 22 0;
createNode animCurveTL -n "CURVE159";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A1E7";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 -0.19905291220402432 3 0.57000000000000006 4 0 5 0.17000000000000004 6 0 7 0
		 8 0 9 0 10 -0.15000000000000002 11 -0.63599151632887474 12 0.22999999999999998 13 0 14 0.16000000000000003 15 0.16000000000000003 16 0 17 -0.32000000000000006 18 0.25904912591299567
		 19 0 20 0 21 0.16000000000000003 22 0.28;
createNode animCurveTL -n "CURVE160";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A1E8";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0 12 0 13 0 14 0 15 0 16 0 17 0 18 0 19 0 20 0 21 0 22 0;
createNode animCurveTU -n "CURVE161";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A1EC";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 1 2 1 3 1 4 1 5 1 6 1 7 1 8 1 9 1 10 1
		 11 1 12 1 13 1 14 1 15 1 16 1 17 1 18 1 19 1 20 1 21 1 22 1;
createNode animCurveTU -n "CURVE162";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A1ED";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 1 2 1 3 1 4 1 5 1 6 1 7 1 8 1 9 1 10 1
		 11 1 12 1 13 1 14 1 15 1 16 1 17 1 18 1 19 1 20 1 21 1 22 1;
createNode animCurveTU -n "CURVE163";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A1EE";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 1 2 1 3 1 4 1 5 1 6 1 7 1 8 1 9 1 10 1
		 11 1 12 1 13 1 14 1 15 1 16 1 17 1 18 1 19 1 20 1 21 1 22 1;
createNode animCurveTA -n "CURVE164";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A1E9";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0 12 0 13 0 14 0 15 0 16 0 17 0 18 0 19 0 20 0 21 0 22 0;
createNode animCurveTA -n "CURVE165";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A1EA";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0 12 0 13 0 14 0 15 0 16 0 17 0 18 0 19 0 20 0 21 0 22 0;
createNode animCurveTA -n "CURVE166";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A1EB";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0 12 0 13 0 14 0 15 0 16 0 17 0 18 -17.627249688341351 19 0 20 0 21 0 22 0;
createNode animCurveTU -n "CURVE168";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A1FA";
	setAttr ".tan" 9;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0 12 0 13 0 14 0 15 0 16 0 17 0 18 0 19 0 20 0 21 0 22 0;
	setAttr -s 22 ".kot[0:21]"  5 5 5 5 5 5 5 5 
		5 5 5 5 5 5 5 5 5 5 5 5 5 5;
createNode animCurveTL -n "CURVE169";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A1F3";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0.07 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0.1 12 0 13 0.0018539852200607537 14 0.10999999999999999 15 0 16 0 17 0 18 0 19 0 20 0 21 0.10999999999999999 22 0.10999999999999999;
createNode animCurveTL -n "CURVE170";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A1F1";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 0 3 0 4 0.18000000000000002 5 0 6 0 7 0 8 0 9 0
		 10 0 11 -0.25 12 -0.090000000000000024 13 -0.16389741815905576 14 0.19000000000000003 15 0 16 0 17 0 18 0 19 -0.0004606966634587772 20 0.080000000000000016
		 21 0.19000000000000003 22 0.19000000000000003;
createNode animCurveTL -n "CURVE171";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A1F2";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 -0.17000000000000004 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0
		 10 0 11 0.05 12 0 13 -0.034889098822055931 14 -0.19000000000000003 15 0 16 0 17 0 18 0 19 0 20 0 21 -0.19000000000000003 22 -0.19000000000000003;
createNode animCurveTU -n "CURVE172";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A1F7";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 1 2 0.99999999999999978 3 0.99999999999999978 4 0.99999999999999978 5 0.99999999999999978
		 6 1 7 0.99999999999999978 8 0.99999999999999978 9 0.99999999999999978 10 0.99999999999999978 11 1 12 0.99999999999999978 13 0.99999999999999978 14 0.99999999999999978 15 0.99999999999999978
		 16 0.99999999999999978 17 0.99999999999999978 18 0.99999999999999978 19 0.99999999999999978 20 0.99999999999999978 21 0.99999999999999978 22 0.99999999999999978;
createNode animCurveTU -n "CURVE173";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A1F8";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 1 2 1 3 1 4 1 5 1 6 1 7 1 8 1 9 1 10 1
		 11 1 12 1 13 1 14 1 15 1 16 1 17 1 18 1 19 1 20 1 21 1 22 1;
createNode animCurveTU -n "CURVE174";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A1F9";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 1 2 1 3 1 4 1 5 1 6 1 7 1 8 1 9 1 10 1
		 11 1 12 1 13 1 14 1 15 1 16 1 17 1 18 1 19 1 20 1 21 1 22 1;
createNode animCurveTA -n "CURVE175";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A1F4";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0 12 0 13 0 14 0 15 0 16 0 17 0 18 0 19 0 20 0 21 0 22 0;
createNode animCurveTA -n "CURVE176";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A1F5";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0 12 0 13 0 14 0 15 0 16 0 17 0 18 0 19 0 20 0 21 0 22 0;
createNode animCurveTA -n "CURVE177";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A1F6";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 7.104676659622208 12 0 13 0 14 10.886198107485642 15 0 16 0 17 0 18 0 19 0 20 0 21 10.886198107485642 22 10.886198107485642;
createNode animCurveTL -n "CURVE179";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A1FC";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0.078634834098057022 7 0 8 0 9 0
		 10 0 11 0.078634834098057022;
createNode animCurveTL -n "CURVE180";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A1FD";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0.29466641655124354 7 0 8 0 9 0
		 10 -0.003926914531465181 11 0.29466641655124354;
createNode animCurveTL -n "CURVE181";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A1FE";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
createNode animCurveTU -n "CURVE183";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A200";
	setAttr ".tan" 9;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
	setAttr -s 11 ".kot[0:10]"  5 5 5 5 5 5 5 5 
		5 5 5;
createNode animCurveTL -n "CURVE184";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A201";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 -0.12000000000000002 8 -0.28
		 9 0 10 0 11 0;
createNode animCurveTL -n "CURVE185";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A202";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 -0.28 2 -0.059999999999999942 3 0.36384017232392935 4 0 5 -0.32000000000000006 6 0
		 7 -0.32000000000000006 8 -0.35000000000000003 9 -0.06 10 -0.060000000000000012 11 0;
createNode animCurveTL -n "CURVE186";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A203";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
createNode animCurveTU -n "CURVE187";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A207";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1 2 1 3 1 4 1 5 1 6 1 7 1 8 1 9 1 10 1
		 11 1;
createNode animCurveTU -n "CURVE188";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A208";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1 2 1 3 1 4 1 5 1 6 1 7 1 8 1 9 1 10 1
		 11 1;
createNode animCurveTU -n "CURVE189";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A209";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1 2 1 3 1 4 1 5 1 6 1 7 1 8 1 9 1 10 1
		 11 1;
createNode animCurveTA -n "CURVE190";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A204";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
createNode animCurveTA -n "CURVE191";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A205";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
createNode animCurveTA -n "CURVE192";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A206";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 -24.751776749651565 3 0 4 4.3544792429942571 5 4.0107045659157627 6 0 7 7.677634454753032
		 8 0 9 0 10 0 11 0;
createNode animCurveTU -n "CURVE194";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A20B";
	setAttr ".tan" 9;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
	setAttr -s 11 ".kot[0:10]"  5 5 5 5 5 5 5 5 
		5 5 5;
createNode animCurveTL -n "CURVE195";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A20C";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 -0.47000000000000003 2 -0.8685255857162435 3 -0.57335914867928006 4 -0.72 5 -0.84
		 6 0 7 -0.41000000000000003 8 -0.41000000000000003 9 0 10 0 11 0;
createNode animCurveTL -n "CURVE196";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A20D";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 -0.54 2 -1.4355767572341982 3 0.12007112331046654 4 -0.23615219096362794 5 -0.16000000000000003
		 6 0.12 7 0.78 8 0.56 9 0.29000000000000004 10 0.21782900764751406 11 0.12;
createNode animCurveTL -n "CURVE197";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A20E";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
createNode animCurveTU -n "CURVE198";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A212";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1 2 1 3 1 4 1 5 1 6 1 7 1 8 1 9 1 10 1
		 11 1;
createNode animCurveTU -n "CURVE199";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A213";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1 2 1 3 1 4 1 5 1 6 1 7 1 8 1 9 1 10 1
		 11 1;
createNode animCurveTU -n "CURVE200";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A214";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1 2 1 3 1 4 1 5 1 6 1 7 1 8 1 9 1 10 1
		 11 1;
createNode animCurveTA -n "CURVE201";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A20F";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
createNode animCurveTA -n "CURVE202";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A210";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
createNode animCurveTA -n "CURVE203";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A211";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 -27.997135838187518 3 -5.5385314884367531 4 -12.719663051904277 5 -5.3858032742297404
		 6 0 7 -30.137580023881309 8 -13.865578642165932 9 -13.407212406061262 10 -13.407212406061262 11 0;
createNode animCurveTL -n "CURVE205";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A216";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 -0.24000000000000005 2 -0.24000000000000005 3 -0.24000000000000005 4 -0.24000000000000005 5 -0.24000000000000005
		 6 0 7 0 8 0 9 0 10 0 11 0;
createNode animCurveTL -n "CURVE206";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A217";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
createNode animCurveTL -n "CURVE207";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A218";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
createNode animCurveTU -n "CURVE209";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A223";
	setAttr ".tan" 9;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0 12 0 13 0 14 0 15 0 16 0 17 0 18 0 19 0 20 0 21 0 22 0;
	setAttr -s 22 ".kot[0:21]"  5 5 5 5 5 5 5 5 
		5 5 5 5 5 5 5 5 5 5 5 5 5 5;
createNode animCurveTL -n "CURVE210";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A21A";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 0.20597038920865737 3 0 4 0 5 0 6 0 7 0 8 0 9 0
		 10 0 11 -0.060698490740581902 12 0 13 0 14 -0.17 15 0 16 0 17 0 18 0 19 0 20 0.020000000000000004 21 -0.16999999999999998 22 -0.17;
createNode animCurveTL -n "CURVE211";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A21B";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 -0.21539888175778232 3 0 4 0 5 0 6 0 7 0.1 8 0.1
		 9 0 10 -0.009999999999999995 11 0.26000000000000034 12 0 13 0.41000000000000003 14 -0.06 15 -0.060000000000000012 16 -0.090000000000000011 17 0 18 0 19 -0.0004606966634587772
		 20 -0.11000000000000001 21 -0.060000000000000012 22 0.15000000000000002;
createNode animCurveTL -n "CURVE212";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A21C";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 -0.036478395646162204 3 0 4 0 5 0 6 0 7 0 8 0 9 0
		 10 0 11 0 12 0 13 0 14 0 15 0 16 0 17 0 18 0 19 0 20 0 21 0 22 0;
createNode animCurveTU -n "CURVE213";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A220";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 1 2 1 3 1 4 1 5 1 6 1 7 1 8 1 9 1 10 1
		 11 1 12 1 13 1 14 1 15 1 16 1 17 1 18 1 19 1 20 1 21 1 22 1;
createNode animCurveTU -n "CURVE214";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A221";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 1 2 1 3 1 4 1 5 1 6 1 7 1 8 1 9 1 10 1
		 11 1 12 1 13 1 14 1 15 1 16 1 17 1 18 1 19 1 20 1 21 1 22 1;
createNode animCurveTU -n "CURVE215";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A222";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 1 2 1 3 1 4 1 5 1 6 1 7 1 8 1 9 1 10 1
		 11 1 12 1 13 1 14 1 15 1 16 1 17 1 18 1 19 1 20 1 21 1 22 1;
createNode animCurveTA -n "CURVE216";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A21D";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 -17.791091154649134 3 0 4 0 5 0 6 0 7 0 8 0 9 0
		 10 0 11 0 12 0 13 0 14 0 15 0 16 0 17 0 18 0 19 0 20 0 21 0 22 5.9961394406512651;
createNode animCurveTA -n "CURVE217";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A21E";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 -15.993736847417619 3 0 4 0 5 0 6 0 7 0 8 0 9 0
		 10 0 11 0 12 0 13 0 14 0 15 0 16 0 17 0 18 0 19 0 20 0 21 0 22 0;
createNode animCurveTA -n "CURVE218";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A21F";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 -10.997959995258739 3 0 4 0 5 0 6 0 7 0 8 0 9 0
		 10 -17.417916971977029 11 0 12 0 13 0 14 7.3338597776745376 15 7.3338597776745376 16 0 17 0 18 0 19 0 20 -8.9381416040408439 21 7.3338597776745376
		 22 7.3338597776745376;
createNode animCurveTU -n "CURVE220";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A225";
	setAttr ".tan" 9;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
	setAttr -s 11 ".kot[0:10]"  5 5 5 5 5 5 5 5 
		5 5 5;
createNode animCurveTL -n "CURVE221";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A226";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
createNode animCurveTL -n "CURVE222";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A227";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
createNode animCurveTL -n "CURVE223";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A228";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
createNode animCurveTU -n "CURVE224";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A22C";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1 2 1 3 1 4 1 5 1 6 1 7 1 8 1 9 1 10 1
		 11 1;
createNode animCurveTU -n "CURVE225";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A22D";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1 2 1 3 1 4 1 5 1 6 1 7 1 8 1 9 1 10 1
		 11 1;
createNode animCurveTU -n "CURVE226";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A22E";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1 2 1 3 1 4 1 5 1 6 1 7 1 8 1 9 1 10 1
		 11 1;
createNode animCurveTA -n "CURVE227";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A229";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
createNode animCurveTA -n "CURVE228";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A22A";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
createNode animCurveTA -n "CURVE229";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A22B";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
createNode animCurveTU -n "CURVE231";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A239";
	setAttr ".tan" 9;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0 12 0 13 0 14 0 15 0 16 0 17 0 18 0 19 0 20 0 21 0 22 0;
	setAttr -s 22 ".kot[0:21]"  5 5 5 5 5 5 5 5 
		5 5 5 5 5 5 5 5 5 5 5 5 5 5;
createNode animCurveTL -n "CURVE232";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A230";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0.07 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0.1 12 0 13 0.065896294730020344 14 0.10999999999999999 15 0 16 0 17 0 18 0 19 0 20 0 21 0.10999999999999999 22 0.10999999999999999;
createNode animCurveTL -n "CURVE233";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A231";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 -0.37384399930205453 3 0.18 4 0 5 0 6 0 7 0 8 0
		 9 0 10 0 11 -0.25 12 -0.090000000000000024 13 -0.23823958722644631 14 0.19000000000000003 15 0 16 0 17 0 18 0 19 -0.0004606966634587772 20 0.080000000000000016
		 21 0.19000000000000003 22 0.19000000000000003;
createNode animCurveTL -n "CURVE234";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A232";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 -0.17000000000000004 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0
		 10 0 11 0.05 12 0 13 0 14 -0.19000000000000003 15 0 16 0 17 0 18 0 19 0 20 0 21 -0.19000000000000003 22 -0.19000000000000003;
createNode animCurveTU -n "CURVE235";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A236";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 1 2 1 3 1 4 1 5 1 6 1 7 1 8 1 9 1 10 1
		 11 1 12 1 13 1 14 1 15 1 16 1 17 1 18 1 19 1 20 1 21 1 22 1;
createNode animCurveTU -n "CURVE236";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A237";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 1 2 1 3 1 4 1 5 1 6 1 7 1 8 1 9 1 10 1
		 11 1 12 1 13 1 14 1 15 1 16 1 17 1 18 1 19 1 20 1 21 1 22 1;
createNode animCurveTU -n "CURVE237";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A238";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 1 2 1 3 1 4 1 5 1 6 1 7 1 8 1 9 1 10 1
		 11 1 12 1 13 1 14 1 15 1 16 1 17 1 18 1 19 1 20 1 21 1 22 1;
createNode animCurveTA -n "CURVE238";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A233";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 4.1679324898825323 3 0 4 0 5 0 6 0 7 0 8 0 9 0
		 10 0 11 0 12 0 13 0 14 0 15 0 16 0 17 0 18 0 19 0 20 0 21 0 22 0;
createNode animCurveTA -n "CURVE239";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A234";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0 12 0 13 0 14 0 15 0 16 0 17 0 18 0 19 0 20 0 21 0 22 0;
createNode animCurveTA -n "CURVE240";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A235";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 7.104676659622208 12 0 13 0 14 10.886198107485642 15 0 16 0 17 0 18 0 19 0 20 0 21 10.886198107485642 22 10.886198107485642;
createNode animCurveTU -n "CURVE242";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A23B";
	setAttr ".tan" 9;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
	setAttr -s 11 ".kot[0:10]"  5 5 5 5 5 5 5 5 
		5 5 5;
createNode animCurveTL -n "CURVE243";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A23C";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
createNode animCurveTL -n "CURVE244";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A23D";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
createNode animCurveTL -n "CURVE245";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A23E";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
createNode animCurveTU -n "CURVE246";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A242";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1 2 1 3 1 4 1 5 1 6 1 7 1 8 1 9 1 10 1
		 11 1;
createNode animCurveTU -n "CURVE247";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A243";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1 2 1 3 1 4 1 5 1 6 1 7 1 8 1 9 1 10 1
		 11 1;
createNode animCurveTU -n "CURVE248";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A244";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1 2 1 3 1 4 1 5 1 6 1 7 1 8 1 9 1 10 1
		 11 1;
createNode animCurveTA -n "CURVE249";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A23F";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
createNode animCurveTA -n "CURVE250";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A240";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
createNode animCurveTA -n "CURVE251";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A241";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
createNode animCurveTU -n "CURVE253";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A246";
	setAttr ".tan" 9;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
	setAttr -s 11 ".kot[0:10]"  5 5 5 5 5 5 5 5 
		5 5 5;
createNode animCurveTL -n "CURVE254";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A247";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
createNode animCurveTL -n "CURVE255";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A248";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
createNode animCurveTL -n "CURVE256";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A249";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
createNode animCurveTU -n "CURVE257";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A24D";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1 2 1 3 1 4 1 5 1 6 1 7 1 8 1 9 1 10 1
		 11 1;
createNode animCurveTU -n "CURVE258";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A24E";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1 2 1 3 1 4 1 5 1 6 1 7 1 8 1 9 1 10 1
		 11 1;
createNode animCurveTU -n "CURVE259";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A24F";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1 2 1 3 1 4 1 5 1 6 1 7 1 8 1 9 1 10 1
		 11 1;
createNode animCurveTA -n "CURVE260";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A24A";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
createNode animCurveTA -n "CURVE261";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A24B";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
createNode animCurveTA -n "CURVE262";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A24C";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
createNode animCurveTU -n "CURVE264";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A25A";
	setAttr ".tan" 9;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0 12 0 13 0 14 0 15 0 16 0 17 0 18 0 19 0 20 0 21 0 22 0;
	setAttr -s 22 ".kot[0:21]"  5 5 5 5 5 5 5 5 
		5 5 5 5 5 5 5 5 5 5 5 5 5 5;
createNode animCurveTL -n "CURVE265";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A251";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0 12 0 13 0 14 0 15 0 16 0 17 0 18 0 19 0 20 0 21 0 22 0;
createNode animCurveTL -n "CURVE266";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A252";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0 12 0 13 0 14 0 15 0 16 0 17 0 18 0 19 0 20 0 21 0 22 0;
createNode animCurveTL -n "CURVE267";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A253";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0 12 0 13 0 14 0 15 0 16 0 17 0 18 0 19 0 20 0 21 0 22 0;
createNode animCurveTU -n "CURVE268";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A257";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 1 2 1 3 1 4 1 5 1 6 1 7 1 8 1 9 1 10 1
		 11 1 12 1 13 1 14 1 15 1 16 1 17 1 18 1 19 1 20 1 21 1 22 1;
createNode animCurveTU -n "CURVE269";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A258";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 1.0000000000000002 2 1.0000000000000002 3 1.0000000000000002 4 1.0000000000000002 5 1.0000000000000002
		 6 1.0000000000000002 7 1.0000000000000002 8 1.0000000000000002 9 1.0000000000000002 10 1.0000000000000002 11 1 12 1 13 1 14 1 15 1 16 1 17 1
		 18 1 19 1 20 1 21 1 22 1;
createNode animCurveTU -n "CURVE270";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A259";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 1.0000000000000002 2 1.0000000000000002 3 1.0000000000000002 4 1.0000000000000002 5 1.0000000000000002
		 6 1.0000000000000002 7 1.0000000000000002 8 1.0000000000000002 9 1.0000000000000002 10 1.0000000000000002 11 1 12 1 13 1 14 1 15 1 16 1 17 1
		 18 1 19 1 20 1 21 1 22 1;
createNode animCurveTA -n "CURVE271";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A254";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0 12 0 13 0 14 0 15 0 16 0 17 0 18 0 19 0 20 0 21 0 22 0;
createNode animCurveTA -n "CURVE272";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A255";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0 12 0 13 0 14 0 15 0 16 0 17 0 18 0 19 0 20 0 21 0 22 0;
createNode animCurveTA -n "CURVE273";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A256";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0 12 0 13 0 14 0 15 0 16 0 17 0 18 0 19 0 20 0 21 0 22 0;
createNode animCurveTU -n "CURVE275";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A25C";
	setAttr ".tan" 9;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
	setAttr -s 11 ".kot[0:10]"  5 5 5 5 5 5 5 5 
		5 5 5;
createNode animCurveTL -n "CURVE276";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A262";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0.040000000000000008 9 0
		 10 0 11 0;
createNode animCurveTL -n "CURVE277";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A263";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 -0.27000000000000007 2 0 3 -0.31000000000000005 4 -0.31000000000000005 5 -0.31000000000000005
		 6 -0.41000000000000009 7 -0.60393088552915764 8 -0.31484604740820993 9 0 10 -0.07 11 -0.41000000000000009;
createNode animCurveTL -n "CURVE278";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A264";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
createNode animCurveTU -n "CURVE279";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A25E";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
createNode animCurveTU -n "CURVE280";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A265";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1 2 1 3 1 4 1 5 1 6 1 7 1 8 1 9 1 10 1
		 11 1;
createNode animCurveTU -n "CURVE281";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A266";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1 2 1 3 1 4 1 5 1 6 1 7 1 8 1 9 1 10 1
		 11 1;
createNode animCurveTU -n "CURVE282";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A267";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1 2 1 3 1 4 1 5 1 6 1 7 1 8 1 9 1 10 1
		 11 1;
createNode animCurveTA -n "CURVE283";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A25F";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
createNode animCurveTA -n "CURVE284";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A260";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
createNode animCurveTA -n "CURVE285";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A261";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 -2.5210142985756221 4 -2.5210142985756221 5 -0.34377467707849396 6 0 7 -4.2398876839680915
		 8 -11.573747461642633 9 0 10 0 11 0;
createNode animCurveTU -n "CURVE286";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A25D";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
createNode animCurveTU -n "CURVE288";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A272";
	setAttr ".tan" 9;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0 12 0 13 0 14 0 15 0 16 0 17 0 18 0 19 0 20 0 21 0 22 0;
	setAttr -s 22 ".kot[0:21]"  5 5 5 5 5 5 5 5 
		5 5 5 5 5 5 5 5 5 5 5 5 5 5;
createNode animCurveTL -n "CURVE289";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A269";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0 12 0 13 0 14 0.07 15 0 16 0 17 0 18 0 19 0 20 0 21 0.07 22 0.07;
createNode animCurveTL -n "CURVE290";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A26A";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 -0.090000000000000011 2 -0.24495468991398184 3 0 4 0 5 0 6 0 7 0 8 0
		 9 0 10 0 11 -0.16000000000000025 12 -0.17000000000000004 13 -0.26 14 0 15 0 16 -0.21000000000000002 17 -0.17000000000000004 18 0 19 -0.0004606966634587772
		 20 0 21 0 22 0.26;
createNode animCurveTL -n "CURVE291";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A26B";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0 12 0 13 0 14 0 15 0 16 0 17 0 18 0 19 0 20 0 21 0 22 0;
createNode animCurveTU -n "CURVE292";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A26F";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 1 2 1 3 1 4 1 5 1 6 1 7 1 8 1 9 1 10 1
		 11 1 12 1 13 1 14 1 15 1 16 1 17 1 18 1 19 1 20 1 21 1 22 1;
createNode animCurveTU -n "CURVE293";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A270";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 1 2 1 3 1 4 1 5 1 6 1 7 1 8 1 9 1 10 1
		 11 1 12 1 13 1 14 1 15 1 16 1 17 1 18 1 19 1 20 1 21 1 22 1;
createNode animCurveTU -n "CURVE294";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A271";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 1 2 1 3 1 4 1 5 1 6 1 7 1 8 1 9 1 10 1
		 11 1 12 1 13 1 14 1 15 1 16 1 17 1 18 1 19 1 20 1 21 1 22 1;
createNode animCurveTA -n "CURVE295";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A26C";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0 12 0 13 0 14 0 15 0 16 0 17 0 18 0 19 0 20 0 21 0 22 0;
createNode animCurveTA -n "CURVE296";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A26D";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0 12 0 13 0 14 0 15 0 16 0 17 0 18 0 19 0 20 0 21 0 22 0;
createNode animCurveTA -n "CURVE297";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A26E";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0 12 0 13 0 14 0 15 0 16 0 17 0 18 0 19 0 20 0 21 0 22 0;
createNode animCurveTL -n "CURVE299";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A274";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
createNode animCurveTL -n "CURVE300";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A275";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
createNode animCurveTL -n "CURVE301";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A276";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
createNode animCurveTU -n "CURVE303";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A281";
	setAttr ".tan" 9;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0 12 0 13 0 14 0 15 0 16 0 17 0 18 0 19 0 20 0 21 0 22 0;
	setAttr -s 22 ".kot[0:21]"  5 5 5 5 5 5 5 5 
		5 5 5 5 5 5 5 5 5 5 5 5 5 5;
createNode animCurveTL -n "CURVE304";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A278";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 -0.00040868337673116706 2 0.011101018859471335 3 -0.00072610695608821448 4 0.00072610695608821382 5 -0.00072610695608821382
		 6 0 7 0 8 0 9 0 10 0 11 0 12 0 13 0 14 0 15 0 16 0 17 0 18 0 19 0 20 0 21 0 22 0;
createNode animCurveTL -n "CURVE305";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A279";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0.23056488754828025 2 -0.20601896347006682 3 0.15956628637655051 4 0.15956628637655054 5 0.33956628637655056
		 6 0 7 0.25000000000000006 8 0 9 0 10 -0.41000000000000009 11 -0.10259727463998675 12 -0.41696882490093123 13 -0.21696882490093125 14 -0.72000000000000008 15 0.020000000000000018
		 16 0.07 17 -0.13 18 0.090000000000000024 19 -0.00046069666345877058 20 -0.14 21 -0.39 22 -0.27192305070821704;
createNode animCurveTL -n "CURVE306";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A27A";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 -0.0080392140879972374 2 -0.15386394877436496 3 -0.005146348562209746 4 -0.0051463485622097582 5 -0.0051463485622097582
		 6 0 7 0 8 0 9 0 10 0 11 0 12 0 13 0 14 0 15 -0.060000000000000012 16 -0.060000000000000012 17 0 18 0 19 0 20 0
		 21 0 22 -0.0063832745016352294;
createNode animCurveTU -n "CURVE307";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A282";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 1 2 1 3 1 4 1 5 1 6 0 7 1 8 1 9 0 10 0
		 11 1 12 1 13 1 14 1 15 1 16 1 17 1 18 0 19 0.50000000000000011 20 1 21 1 22 1;
createNode animCurveTU -n "CURVE308";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A27E";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 1 2 1 3 1 4 1 5 1 6 1 7 1 8 1 9 1 10 1
		 11 1 12 1 13 1 14 1 15 1.1333333329697717 16 1 17 1 18 1 19 1 20 1 21 1 22 1;
createNode animCurveTU -n "CURVE309";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A27F";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 1 2 1 3 1 4 1 5 1 6 1 7 1 8 1 9 1 10 1
		 11 1 12 1 13 1 14 1 15 1 16 1 17 1 18 1 19 1 20 1 21 1 22 1;
createNode animCurveTU -n "CURVE310";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A280";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 1 2 1 3 1 4 1 5 1 6 1 7 1 8 1 9 1 10 1
		 11 1 12 1 13 1 14 1 15 1 16 1 17 1 18 1 19 1 20 1 21 1 22 1;
createNode animCurveTU -n "CURVE311";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A283";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0.14 2 0 3 0.12000000000000002 4 0.12000000000000002 5 0.18400000000000005 6 0.080000000000000016
		 7 0.1 8 0.1 9 0.090000000000000011 10 0.16000000000000003 11 0 12 0.13 13 0.07 14 0 15 0.66000000000000014 16 0.66000000000000014 17 0
		 18 0.07 19 0.26 20 0 21 0 22 0.35000000000000003;
createNode animCurveTA -n "CURVE312";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A27B";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 -14.735060713909077 2 -35.411981325784012 3 -14.716615993893495 4 -14.716615993893495 5 -14.727169906483859
		 6 8.0228670159339117 7 -23.94963583646841 8 -23.94963583646841 9 0 10 0 11 0 12 0 13 0 14 0 15 25.324734544782391 16 8.9381416040408475 17 0
		 18 0 19 0 20 0 21 0 22 0;
createNode animCurveTA -n "CURVE313";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A27C";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0.18844784613359708 2 -4.7706638020925256 3 -0.76877097327050503 4 0.76877097327050548 5 0.52273458082967816
		 6 0 7 0 8 0 9 0 10 0 11 0 12 0 13 0 14 0 15 0 16 0 17 0 18 0 19 0 20 0 21 0 22 0;
createNode animCurveTA -n "CURVE314";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A27D";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0.71649517697558884 2 0 3 -2.924292538764683 4 2.924292538764683 5 0 6 0 7 0
		 8 0 9 1.9113146058248682 10 4.8128454790989155 11 0 12 0 13 0 14 0 15 0 16 0 17 0 18 0 19 0 20 0 21 0 22 0;
createNode animCurveTU -n "CURVE315";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A284";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0 12 0 13 0 14 0.14 15 0 16 0 17 0.17000000000000004 18 0.090000000000000011 19 0 20 0.14 21 0.14 22 0.54;
createNode animCurveTU -n "CURVE317";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A286";
	setAttr ".tan" 9;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
	setAttr -s 11 ".kot[0:10]"  5 5 5 5 5 5 5 5 
		5 5 5;
createNode animCurveTL -n "CURVE318";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A287";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 -0.019371019831588367 4 0.019371019831588367 5 0 6 0 7 0 8 0
		 9 0 10 0 11 0;
createNode animCurveTL -n "CURVE319";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A288";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
createNode animCurveTL -n "CURVE320";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A289";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
createNode animCurveTU -n "CURVE321";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A28D";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1 2 1 3 1 4 1 5 1 6 1 7 1 8 1 9 1 10 1
		 11 1;
createNode animCurveTU -n "CURVE322";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A28E";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1 2 1 3 1 4 1 5 1 6 1 7 1 8 1 9 1 10 1
		 11 1;
createNode animCurveTU -n "CURVE323";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A28F";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1 2 1 3 1 4 1 5 1 6 1 7 1 8 1 9 1 10 1
		 11 1;
createNode animCurveTA -n "CURVE324";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A28A";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
createNode animCurveTA -n "CURVE325";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A28B";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
createNode animCurveTA -n "CURVE326";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A28C";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 -0.57713639423140062 4 0.57713639423140062 5 0 6 0 7 0 8 0
		 9 0 10 0 11 0;
createNode animCurveTU -n "CURVE328";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A29A";
	setAttr ".tan" 9;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0 12 0 13 0 14 0 15 0 16 0 17 0 18 0 19 0 20 0 21 0 22 0;
	setAttr -s 22 ".kot[0:21]"  5 5 5 5 5 5 5 5 
		5 5 5 5 5 5 5 5 5 5 5 5 5 5;
createNode animCurveTL -n "CURVE329";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A291";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 0.46764220632924625 3 0 4 0 5 0 6 0 7 0 8 0 9 0
		 10 0.25 11 0 12 0.22245077100627991 13 0.22245077100627991 14 0.13 15 0.13 16 0.13 17 0 18 0 19 0 20 0.13 21 0.13
		 22 0.13;
createNode animCurveTL -n "CURVE330";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A292";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0.15040828147166968
		 10 0 11 0 12 -0.12976444140419061 13 -0.12976444140419061 14 0.18999999999999997 15 0.26 16 0.26 17 0 18 0 19 -0.0004606966634587772 20 0
		 21 0.19 22 0.26;
createNode animCurveTL -n "CURVE331";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A293";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0 12 0 13 0 14 -0.51000000000000012 15 0 16 0 17 0 18 0 19 0 20 0 21 0 22 0;
createNode animCurveTU -n "CURVE332";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A297";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 1 2 1 3 1 4 1 5 1 6 1 7 1 8 1 9 1 10 1
		 11 1 12 1 13 1 14 1 15 1 16 1 17 1 18 1 19 1 20 1 21 1 22 1;
createNode animCurveTU -n "CURVE333";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A298";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 1 2 1 3 1 4 1 5 1 6 1 7 1 8 1 9 1 10 1
		 11 1 12 1 13 1 14 1 15 1 16 1 17 1 18 1 19 1 20 1 21 1 22 1;
createNode animCurveTU -n "CURVE334";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A299";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 1 2 1 3 1 4 1 5 1 6 1 7 1 8 1 9 1 10 1
		 11 1 12 1 13 1 14 1 15 1 16 1 17 1 18 1 19 1 20 1 21 1 22 1;
createNode animCurveTA -n "CURVE335";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A294";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0 12 0 13 0 14 0 15 0 16 0 17 0 18 0 19 0 20 0 21 0 22 3.5861642606402628;
createNode animCurveTA -n "CURVE336";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A295";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0 12 0 13 0 14 0 15 0 16 0 17 0 18 0 19 0 20 0 21 0 22 0.12335389145613423;
createNode animCurveTA -n "CURVE337";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A296";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0 12 -11.986035391099904 13 -11.986035391099904 14 40.79459501331462 15 0 16 0 17 0 18 0 19 0 20 0 21 0 22 -12.236200738685465;
createNode animCurveTU -n "CURVE339";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A2A5";
	setAttr ".tan" 9;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0 12 0 13 0 14 0 15 0 16 0 17 0 18 0 19 0 20 0 21 0 22 0;
	setAttr -s 22 ".kot[0:21]"  5 5 5 5 5 5 5 5 
		5 5 5 5 5 5 5 5 5 5 5 5 5 5;
createNode animCurveTL -n "CURVE340";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A29E";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0 12 0 13 0 14 0 15 0 16 0 17 0 18 0 19 0 20 0 21 0 22 0;
createNode animCurveTL -n "CURVE341";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A29C";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 -0.19905291220402432 3 0 4 0.57000000000000006 5 0.17000000000000004 6 0 7 0
		 8 0 9 0 10 -0.05 11 -0.63599151632887474 12 0.22999999999999998 13 0 14 0.16000000000000003 15 0.16000000000000003 16 0 17 -0.32000000000000006 18 0
		 19 -0.0004606966634587772 20 0 21 0.16000000000000003 22 0.28;
createNode animCurveTL -n "CURVE342";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A29D";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0 12 0 13 0 14 0 15 0 16 0 17 0 18 0 19 0 20 0 21 0 22 0;
createNode animCurveTU -n "CURVE343";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A2A2";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 1 2 1 3 1 4 1 5 1 6 1 7 1 8 1 9 1 10 1
		 11 1 12 1 13 1 14 1 15 1 16 1 17 1 18 1 19 1 20 1 21 1 22 1;
createNode animCurveTU -n "CURVE344";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A2A3";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 1 2 1 3 1 4 1 5 1 6 1 7 1 8 1 9 1 10 1
		 11 1 12 1 13 1 14 1 15 1 16 1 17 1 18 1 19 1 20 1 21 1 22 1;
createNode animCurveTU -n "CURVE345";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A2A4";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 1 2 1 3 1 4 1 5 1 6 1 7 1 8 1 9 1 10 1
		 11 1 12 1 13 1 14 1 15 1 16 1 17 1 18 1 19 1 20 1 21 1 22 1;
createNode animCurveTA -n "CURVE346";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A29F";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0 12 0 13 0 14 0 15 0 16 0 17 0 18 0 19 0 20 0 21 0 22 0;
createNode animCurveTA -n "CURVE347";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A2A0";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0 12 0 13 0 14 0 15 0 16 0 17 0 18 0 19 0 20 0 21 0 22 0;
createNode animCurveTA -n "CURVE348";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A2A1";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0 12 0 13 0 14 0 15 0 16 0 17 0 18 0 19 0 20 0 21 0 22 0;
createNode animCurveTU -n "CURVE350";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A2A7";
	setAttr ".tan" 9;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
	setAttr -s 11 ".kot[0:10]"  5 5 5 5 5 5 5 5 
		5 5 5;
createNode animCurveTL -n "CURVE351";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A2A8";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
createNode animCurveTL -n "CURVE352";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A2A9";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
createNode animCurveTL -n "CURVE353";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A2AA";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
createNode animCurveTU -n "CURVE354";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A2AE";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1 2 1 3 1 4 1 5 1 6 1 7 1 8 1 9 1 10 1
		 11 1;
createNode animCurveTU -n "CURVE355";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A2AF";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1 2 1 3 1 4 1 5 1 6 1 7 1 8 1 9 1 10 1
		 11 1;
createNode animCurveTU -n "CURVE356";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A2B0";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1 2 1 3 1 4 1 5 1 6 1 7 1 8 1 9 1 10 1
		 11 1;
createNode animCurveTA -n "CURVE357";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A2AB";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
createNode animCurveTA -n "CURVE358";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A2AC";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
createNode animCurveTA -n "CURVE359";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A2AD";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
createNode animCurveTU -n "CURVE361";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A2B8";
	setAttr ".tan" 9;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0 12 0 13 0 14 0 15 0 16 0 17 0 18 0 19 0 20 0 21 0 22 0;
	setAttr -s 22 ".kot[0:21]"  5 5 5 5 5 5 5 5 
		5 5 5 5 5 5 5 5 5 5 5 5 5 5;
createNode animCurveTL -n "CURVE362";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A2B2";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0 12 0 13 0 14 0 15 0 16 0 17 0 18 0 19 0 20 0 21 0 22 0;
createNode animCurveTL -n "CURVE363";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A2B3";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0 12 0 13 0 14 0 15 0 16 0 17 0 18 0 19 -0.0004606966634587772 20 0 21 0 22 0;
createNode animCurveTL -n "CURVE364";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A2B4";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0 12 0 13 0 14 0 15 0.14 16 0.14 17 0 18 0 19 0 20 0.14 21 0.14 22 0.14;
createNode animCurveTA -n "CURVE365";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A2B6";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0 12 0 13 0 14 0 15 0 16 0 17 0 18 0 19 0 20 0 21 0 22 0;
createNode animCurveTU -n "CURVE366";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A2BA";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0 12 0 13 0 14 0 15 0 16 0 17 0 18 0 19 0 20 0 21 0 22 0;
createNode animCurveTA -n "CURVE367";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A2B5";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 21.198190953059338 3 0 4 0 5 0 6 0 7 0 8 2.6356058576017873
		 9 0 10 0 11 7.048662583734405 12 0 13 0.80214091318315239 14 0 15 1.8360283516691933 16 1.8360283516691933 17 4.2398876839680915 18 -0.45836623610465832 19 -0.2291831180523293
		 20 5.2737751224541327 21 1.8360283516691933 22 1.1484789975122054;
createNode animCurveTU -n "CURVE368";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A2B9";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0 12 0 13 0 14 0 15 0 16 0 17 0 18 0 19 0 20 0 21 0 22 0;
createNode animCurveTA -n "CURVE369";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A2B7";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0 12 0 13 0 14 0 15 0 16 0 17 0 18 0 19 0 20 0 21 0 22 0;
createNode animCurveTU -n "CURVE370";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A2BB";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 1 2 1 3 1 4 1 5 1 6 1 7 1 8 1 9 1 10 1
		 11 1 12 1 13 1 14 1 15 1 16 1 17 1 18 1 19 1 20 1 21 1 22 1;
createNode animCurveTU -n "CURVE372";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A2BD";
	setAttr ".tan" 9;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
	setAttr -s 11 ".kot[0:10]"  5 5 5 5 5 5 5 5 
		5 5 5;
createNode animCurveTL -n "CURVE373";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A2BE";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 -0.47000000000000003 2 -0.8685255857162435 3 -0.72 4 -0.57335914867928006 5 -0.84
		 6 0 7 -0.41000000000000003 8 -0.41000000000000003 9 0 10 0 11 0;
createNode animCurveTL -n "CURVE374";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A2BF";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 -0.54000000000000015 2 -1.3755767572341981 3 -0.23615219096362794 4 0.12007112331046649 5 -0.16000000000000003
		 6 0.12 7 0.78 8 0.56 9 0.62884234833907737 10 0.49106136293887692 11 0.12;
createNode animCurveTL -n "CURVE375";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A2C0";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
createNode animCurveTU -n "CURVE376";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A2C4";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1 2 1 3 1 4 1 5 1 6 1 7 1 8 1 9 1 10 1
		 11 1;
createNode animCurveTU -n "CURVE377";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A2C5";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1 2 1 3 1 4 1 5 1 6 1 7 1 8 1 9 1 10 1
		 11 1;
createNode animCurveTU -n "CURVE378";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A2C6";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1 2 1 3 1 4 1 5 1 6 1 7 1 8 1 9 1 10 1
		 11 1;
createNode animCurveTA -n "CURVE379";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A2C1";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
createNode animCurveTA -n "CURVE380";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A2C2";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
createNode animCurveTA -n "CURVE381";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A2C3";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 -29.268165043442053 3 -12.719663051904277 4 -5.5385314884367531 5 -5.3858032742297404
		 6 0 7 -30.137580023881309 8 -15.699043586584558 9 0 10 0 11 0;
createNode animCurveTU -n "CURVE383";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A2C8";
	setAttr ".tan" 9;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
	setAttr -s 11 ".kot[0:10]"  5 5 5 5 5 5 5 5 
		5 5 5;
createNode animCurveTL -n "CURVE384";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A2C9";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
createNode animCurveTL -n "CURVE385";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A2CA";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
createNode animCurveTL -n "CURVE386";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A2CB";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
createNode animCurveTU -n "CURVE387";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A2CF";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1 2 1 3 1 4 1 5 1 6 1 7 1 8 1 9 1 10 1
		 11 1;
createNode animCurveTU -n "CURVE388";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A2D0";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1 2 1 3 1 4 1 5 1 6 1 7 1 8 1 9 1 10 1
		 11 1;
createNode animCurveTU -n "CURVE389";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A2D1";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1 2 1 3 1 4 1 5 1 6 1 7 1 8 1 9 1 10 1
		 11 1;
createNode animCurveTA -n "CURVE390";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A2CC";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 1.5962613028335095 3 0.0074900186419655243 4 0.0074900186419655321 5 0 6 0 7 0
		 8 0 9 0 10 0 11 0;
createNode animCurveTA -n "CURVE391";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A2CD";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 -1.0312968355828498 4 1.0312968355828498 5 0 6 0 7 0 8 0
		 9 0 10 0 11 0;
createNode animCurveTA -n "CURVE392";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A2CE";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 -0.41613827509930174 4 0.41613827509930174 5 0 6 0 7 0 8 0
		 9 0.4583662361046586 10 0.4583662361046586 11 0;
createNode animCurveTL -n "CURVE394";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A2D3";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0.080000000000000016 3 0 4 0 5 0 6 0.010000000000000002 7 0.1
		 8 0.11000000000000001 9 -0.01999999999999999 10 0.05 11 0.010000000000000002;
createNode animCurveTL -n "CURVE395";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A2D4";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1.21 2 0.45999999999999996 3 0.94000000000000006 4 0.9 5 1.11 6 0.43999999999999995
		 7 0.63000000000000012 8 0.64 9 1.0074641002061195 10 1.0574641002061196 11 0.44;
createNode animCurveTU -n "CURVE397";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A2DF";
	setAttr ".tan" 9;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0 12 0 13 0 14 0 15 0 16 0 17 0 18 0 19 0 20 0 21 0 22 0;
	setAttr -s 22 ".kot[0:21]"  5 5 5 5 5 5 5 5 
		5 5 5 5 5 5 5 5 5 5 5 5 5 5;
createNode animCurveTL -n "CURVE398";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A2D8";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 0.69944414173468905 3 0 4 0 5 0 6 0 7 0 8 0 9 0
		 10 0 11 0.19772088978249677 12 0 13 0 14 0.14 15 0.28 16 0.14 17 0 18 0 19 0 20 0.14 21 0.14 22 0.14;
createNode animCurveTL -n "CURVE399";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A2D6";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 0.1371134258168599 3 0 4 0 5 0 6 0 7 0 8 0 9 0
		 10 0 11 0 12 0 13 0.090000000000000011 14 0 15 0 16 0.12000000000000002 17 0 18 0 19 -0.0004606966634587772 20 0 21 0 22 -0.38;
createNode animCurveTL -n "CURVE400";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A2D7";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 0.022003414043991108 3 0 4 0 5 0 6 0 7 0 8 0 9 0
		 10 0 11 0 12 0 13 0 14 0 15 0 16 0 17 0 18 0 19 0 20 0 21 0 22 0;
createNode animCurveTU -n "CURVE401";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A2DC";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 1 2 0.99999999999999933 3 0.99999999999999933 4 0.99999999999999933 5 0.99999999999999933
		 6 1 7 0.99999999999999933 8 0.99999999999999933 9 0.99999999999999933 10 0.99999999999999933 11 0.99999999999999933 12 0.99999999999999933 13 0.99999999999999933 14 0.99999999999999933
		 15 0.99999999999999933 16 0.99999999999999933 17 0.99999999999999933 18 0.99999999999999933 19 0.99999999999999933 20 0.99999999999999933 21 0.99999999999999933 22 0.99999999999999933;
createNode animCurveTU -n "CURVE402";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A2DD";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 1 2 0.99999999999999978 3 0.99999999999999978 4 0.99999999999999978 5 0.99999999999999978
		 6 1 7 0.99999999999999978 8 0.99999999999999978 9 0.99999999999999978 10 0.99999999999999978 11 0.99999999999999978 12 0.99999999999999978 13 0.82277268796079173 14 0.99999999999999978
		 15 0.99999999999999978 16 0.99999999999999978 17 0.99999999999999978 18 0.99999999999999978 19 0.99999999999999978 20 0.99999999999999978 21 0.99999999999999978 22 0.99999999999999978;
createNode animCurveTU -n "CURVE403";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A2DE";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 1 2 1.0000000000000007 3 1.0000000000000007 4 1.0000000000000007 5 1.0000000000000007
		 6 1 7 1.0000000000000007 8 1.0000000000000007 9 1.0000000000000007 10 1.0000000000000007 11 1.0000000000000007 12 1.0000000000000007 13 1.0000000000000007 14 1.0000000000000007
		 15 1.0000000000000007 16 1.0000000000000007 17 1.0000000000000007 18 1.0000000000000007 19 1.0000000000000007 20 1.0000000000000007 21 1.0000000000000007 22 1.0000000000000007;
createNode animCurveTA -n "CURVE404";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A2D9";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 -22.589710954883149 3 0 4 0 5 0 6 0 7 0 8 0 9 0
		 10 0 11 0 12 0 13 0 14 0 15 0 16 0 17 0 18 0 19 0 20 0 21 0 22 0;
createNode animCurveTA -n "CURVE405";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A2DB";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0 12 0 13 0 14 0 15 0 16 0 17 0 18 0 19 0 20 0 21 0 22 0;
createNode animCurveTA -n "CURVE406";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A2DA";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 4.4502425122695257 12 0 13 -2.1772396214971286 14 0 15 0 16 -7.4484513367007024 17 0 18 0 19 0 20 0 21 0 22 0;
createNode animCurveTU -n "CURVE408";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A2E1";
	setAttr ".tan" 9;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
	setAttr -s 11 ".kot[0:10]"  5 5 5 5 5 5 5 5 
		5 5 5;
createNode animCurveTL -n "CURVE409";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A2E2";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 -0.12000000000000002 8 -0.28
		 9 0 10 0 11 0;
createNode animCurveTL -n "CURVE410";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A2E3";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 -0.28 2 0.20000000000000007 3 0 4 0.36384017232392935 5 -0.32 6 0
		 7 -0.32000000000000006 8 -0.25000000000000006 9 -0.23263190130324576 10 -0.23263190130324576 11 0;
createNode animCurveTL -n "CURVE411";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A2E4";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
createNode animCurveTU -n "CURVE412";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A2E8";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1 2 1 3 1 4 1 5 1 6 1 7 1 8 1 9 1 10 1
		 11 1;
createNode animCurveTU -n "CURVE413";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A2E9";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1 2 1 3 1 4 1 5 1 6 1 7 1 8 1 9 1 10 1
		 11 1;
createNode animCurveTU -n "CURVE414";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A2EA";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1 2 1 3 1 4 1 5 1 6 1 7 1 8 1 9 1 10 1
		 11 1;
createNode animCurveTA -n "CURVE415";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A2E5";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
createNode animCurveTA -n "CURVE416";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A2E6";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
createNode animCurveTA -n "CURVE417";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A2E7";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 -24.751776749651565 3 4.3544792429942554 4 0 5 4.0107045659157627 6 0 7 7.677634454753032
		 8 0 9 -2.7720954750488387 10 -2.7720954750488387 11 0;
createNode animCurveTU -n "CURVE419";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A2EC";
	setAttr ".tan" 9;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
	setAttr -s 11 ".kot[0:10]"  5 5 5 5 5 5 5 5 
		5 5 5;
createNode animCurveTL -n "CURVE420";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A2F2";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0.040000000000000008 9 0
		 10 0 11 0;
createNode animCurveTL -n "CURVE421";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A2F3";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 -0.27000000000000007 2 0 3 -0.31000000000000005 4 -0.31000000000000005 5 -0.31000000000000005
		 6 -0.41000000000000009 7 -0.60393088552915764 8 -0.31484604740820993 9 0 10 -0.07 11 -0.41000000000000009;
createNode animCurveTL -n "CURVE422";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A2F4";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
createNode animCurveTU -n "CURVE423";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A2EE";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
createNode animCurveTU -n "CURVE424";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A2F5";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1 2 1 3 1 4 1 5 1 6 1 7 1 8 1 9 1 10 1
		 11 1;
createNode animCurveTU -n "CURVE425";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A2F6";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1 2 1 3 1 4 1 5 1 6 1 7 1 8 1 9 1 10 1
		 11 1;
createNode animCurveTU -n "CURVE426";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A2F7";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1 2 1 3 1 4 1 5 1 6 1 7 1 8 1 9 1 10 1
		 11 1;
createNode animCurveTA -n "CURVE427";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A2EF";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
createNode animCurveTA -n "CURVE428";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A2F0";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
createNode animCurveTA -n "CURVE429";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A2F1";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 -2.5210142985756221 4 -2.5210142985756221 5 -0.34377467707849396 6 0 7 -4.2398876839680915
		 8 -11.573747461642633 9 0 10 0 11 0;
createNode animCurveTU -n "CURVE430";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A2ED";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
createNode animCurveTL -n "CURVE432";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A2F9";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
createNode animCurveTL -n "CURVE433";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A2FA";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
createNode animCurveTL -n "CURVE434";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A2FB";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
createNode animCurveTL -n "CURVE436";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A2FD";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 -0.16773463469593017 7 0 8 0 9 0
		 10 0 11 -0.16773463469593017;
createNode animCurveTL -n "CURVE437";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A2FE";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
createNode animCurveTL -n "CURVE438";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A2FF";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
createNode animCurveTU -n "CURVE440";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A30A";
	setAttr ".tan" 9;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0 12 0 13 0 14 0 15 0 16 0 17 0 18 0 19 0 20 0 21 0 22 0;
	setAttr -s 22 ".kot[0:21]"  5 5 5 5 5 5 5 5 
		5 5 5 5 5 5 5 5 5 5 5 5 5 5;
createNode animCurveTL -n "CURVE441";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A301";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0 12 0 13 0 14 0 15 0 16 0 17 0 18 0 19 0 20 0 21 0 22 0;
createNode animCurveTL -n "CURVE442";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A302";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0 12 0 13 0 14 0 15 0 16 0 17 0 18 0 19 0 20 0 21 0 22 0.040000000000000008;
createNode animCurveTL -n "CURVE443";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A303";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0 12 0 13 0 14 0 15 0 16 0 17 0 18 0 19 0 20 0 21 0 22 0;
createNode animCurveTU -n "CURVE444";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A307";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 1 2 1 3 1 4 1 5 1 6 1 7 1 8 1 9 1 10 1.1400000000000001
		 11 1 12 1 13 1 14 1 15 1 16 1 17 1 18 1 19 1 20 1 21 1 22 1;
createNode animCurveTU -n "CURVE445";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A308";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 1 2 1 3 1 4 1 5 1 6 1 7 1 8 1 9 1 10 1
		 11 1 12 1 13 1 14 1 15 1 16 1 17 1 18 1 19 1 20 1 21 1 22 1;
createNode animCurveTU -n "CURVE446";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A309";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 1 2 1 3 1 4 1 5 1 6 1 7 1 8 1 9 1 10 1
		 11 1 12 1 13 1 14 1 15 1 16 1 17 1 18 1 19 1 20 1 21 1 22 1;
createNode animCurveTA -n "CURVE447";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A304";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0 12 0 13 0 14 0 15 0 16 0 17 0 18 0 19 0 20 0 21 0 22 0;
createNode animCurveTA -n "CURVE448";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A305";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0 12 0 13 0 14 0 15 0 16 0 17 0 18 0 19 0 20 0 21 0 22 0;
createNode animCurveTA -n "CURVE449";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A306";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0 12 0 13 0 14 0 15 0 16 0 17 0 18 0 19 0 20 0 21 0 22 0;
createNode animCurveTL -n "CURVE451";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A30C";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0.35000000000000003 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0.097229187713364418
		 10 0.097229187713364418 11 0;
createNode animCurveTL -n "CURVE452";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A30D";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 -0.32000000000000006 2 0 3 -0.088525585744732863 4 0 5 -0.10000000000000003 6 0.07
		 7 -0.1885255857447044 8 0 9 0.076022785899137912 10 0.036022785899137932 11 0.07;
createNode animCurveTL -n "CURVE453";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A30E";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
createNode animCurveTL -n "CURVE455";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A310";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0.10623070285949332 4 0 5 0 6 0 7 0 8 0 9 0
		 10 0 11 0;
createNode animCurveTL -n "CURVE456";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A311";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 -0.60000000000000009 2 0 3 -0.41606417995733991 4 -0.58000000000000007 5 -0.54 6 -0.42000000000000004
		 7 -0.28 8 0 9 -0.42000000000000004 10 -0.48000000000000004 11 -0.42000000000000004;
createNode animCurveTL -n "CURVE457";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A312";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
createNode animCurveTU -n "CURVE459";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A31D";
	setAttr ".tan" 9;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0 12 0 13 0 14 0 15 0 16 0 17 0 18 0 19 0 20 0 21 0 22 0;
	setAttr -s 22 ".kot[0:21]"  5 5 5 5 5 5 5 5 
		5 5 5 5 5 5 5 5 5 5 5 5 5 5;
createNode animCurveTL -n "CURVE460";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A316";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0.86 8 0.86 9 0
		 10 0 11 0 12 0 13 0 14 0 15 0 16 0 17 0 18 0 19 0 20 0 21 0 22 0;
createNode animCurveTL -n "CURVE461";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A314";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 0 3 0 4 0 5 0.17000000000000004 6 0 7 0 8 0 9 0
		 10 -0.11000000000000001 11 0 12 0 13 0.16000000000000003 14 0 15 0 16 0 17 0.28 18 0 19 -0.0004606966634587772 20 0 21 0 22 0;
createNode animCurveTL -n "CURVE462";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A315";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0 12 0 13 0 14 0 15 0 16 0 17 0 18 0 19 0 20 0 21 0 22 0;
createNode animCurveTU -n "CURVE463";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A31A";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 1 2 1 3 1 4 1 5 1 6 1 7 1 8 1 9 1 10 1
		 11 1 12 1 13 1 14 1 15 1 16 1 17 1 18 1 19 1 20 1 21 1 22 1;
createNode animCurveTU -n "CURVE464";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A31B";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 1 2 1 3 1 4 1 5 1 6 1 7 1 8 1 9 1 10 1
		 11 1 12 1 13 1 14 1 15 1 16 1 17 1 18 1 19 1 20 1 21 1 22 1;
createNode animCurveTU -n "CURVE465";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A31C";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 1 2 1 3 1 4 1 5 1 6 1 7 1 8 1 9 1 10 1
		 11 1 12 1 13 1 14 1 15 1 16 1 17 1 18 1 19 1 20 1 21 1 22 1;
createNode animCurveTA -n "CURVE466";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A317";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0 12 0 13 0 14 0 15 0 16 0 17 0 18 0 19 0 20 0 21 0 22 0;
createNode animCurveTA -n "CURVE467";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A318";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0 12 0 13 0 14 0 15 0 16 0 17 0 18 0 19 0 20 0 21 0 22 0;
createNode animCurveTA -n "CURVE468";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A319";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0 12 0 13 0 14 0 15 0 16 0 17 0 18 0 19 0 20 0 21 0 22 0;
createNode animCurveTL -n "CURVE470";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A31F";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0.080000000000000016 3 0 4 0 5 0 6 0.010000000000000002 7 0.18000000000000002
		 8 0.11000000000000001 9 -0.01999999999999999 10 0.19 11 0.010000000000000002;
createNode animCurveTL -n "CURVE471";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A320";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1.21 2 0.52 3 0.9 4 0.94000000000000006 5 1.11 6 0.43999999999999995
		 7 0.78000000000000025 8 0.64 9 1.0540000000000003 10 1.1040000000000003 11 0.44;
createNode animCurveTU -n "CURVE473";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A32B";
	setAttr ".tan" 9;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0 12 0 13 0 14 0 15 0 16 0 17 0 18 0 19 0 20 0 21 0 22 0;
	setAttr -s 22 ".kot[0:21]"  5 5 5 5 5 5 5 5 
		5 5 5 5 5 5 5 5 5 5 5 5 5 5;
createNode animCurveTL -n "CURVE474";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A322";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0 12 0 13 0 14 0 15 0 16 0 17 0 18 0 19 0 20 0 21 0 22 0;
createNode animCurveTL -n "CURVE475";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A323";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0.071875962189436177 12 0.14375192437887216 13 0.14375192437887216 14 0 15 0 16 0 17 0 18 0 19 -0.0004606966634587772 20 0 21 0 22 0;
createNode animCurveTL -n "CURVE476";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A324";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0 12 0 13 0 14 0 15 0 16 0 17 0 18 0 19 0 20 0 21 0 22 0;
createNode animCurveTU -n "CURVE477";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A328";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 1 2 1 3 1 4 1 5 1 6 1 7 1 8 1 9 1 10 1
		 11 1 12 1 13 1 14 1 15 1 16 1 17 1 18 1 19 1 20 1 21 1 22 1;
createNode animCurveTU -n "CURVE478";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A329";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 1 2 1 3 1 4 1 5 1 6 1 7 1 8 1 9 1 10 1
		 11 1 12 1 13 1 14 1 15 1 16 1 17 1 18 1 19 1 20 1 21 1 22 1;
createNode animCurveTU -n "CURVE479";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A32A";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 1 2 1 3 1 4 1 5 1 6 1 7 1 8 1 9 1 10 1
		 11 1 12 1 13 1 14 1 15 1 16 1 17 1 18 1 19 1 20 1 21 1 22 1;
createNode animCurveTA -n "CURVE480";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A325";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0 12 0 13 0 14 0 15 0 16 0 17 0 18 0 19 0 20 0 21 0 22 0;
createNode animCurveTA -n "CURVE481";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A326";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0 12 0 13 0 14 0 15 0 16 0 17 0 18 0 19 0 20 0 21 0 22 0;
createNode animCurveTA -n "CURVE482";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A327";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0 12 0 13 0 14 0 15 0 16 0 17 0 18 0 19 0 20 0 21 0 22 0;
createNode animCurveTU -n "CURVE484";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A336";
	setAttr ".tan" 9;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0 12 0 13 0 14 0 15 0 16 0 17 0 18 0 19 0 20 0 21 0 22 0;
	setAttr -s 22 ".kot[0:21]"  5 5 5 5 5 5 5 5 
		5 5 5 5 5 5 5 5 5 5 5 5 5 5;
createNode animCurveTL -n "CURVE485";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A32F";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 0.496357567396703 3 0 4 0 5 0 6 0 7 0 8 0 9 0
		 10 0.25 11 0 12 0.24508409798750441 13 0.24508409798750441 14 0.13 15 0.13 16 0.13 17 0 18 0 19 0 20 0.13 21 0.13
		 22 0.13;
createNode animCurveTL -n "CURVE486";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A32D";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0 12 -0.16686394330796572 13 -0.16686394330796572 14 0.19 15 0.26 16 0.26 17 0 18 0 19 -0.0004606966634587772 20 0 21 0.19
		 22 0.26;
createNode animCurveTL -n "CURVE487";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A32E";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0 12 0 13 0 14 -0.51000000000000012 15 0 16 0 17 0 18 0 19 0 20 0 21 0 22 0;
createNode animCurveTU -n "CURVE488";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A335";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 1 2 0.99999999999999989 3 0.99999999999999989 4 0.99999999999999989 5 0.99999999999999989
		 6 1 7 0.99999999999999989 8 0.99999999999999989 9 0.99999999999999989 10 0.99999999999999989 11 0.99999999999999989 12 0.99999999999999989 13 0.99999999999999989 14 0.99999999999999989
		 15 0.99999999999999989 16 0.99999999999999989 17 0.99999999999999989 18 0.99999999999999989 19 0.99999999999999989 20 0.99999999999999989 21 0.99999999999999989 22 0.99999999999999989;
createNode animCurveTU -n "CURVE489";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A333";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 1 2 1.0000000000000002 3 1.0000000000000002 4 1.0000000000000002 5 1.0000000000000002
		 6 1 7 1.0000000000000002 8 1.0000000000000002 9 1.0000000000000002 10 1.0000000000000002 11 1.0000000000000002 12 1.0000000000000002 13 1.0000000000000002 14 1.0000000000000002
		 15 1.0000000000000002 16 1.0000000000000002 17 1.0000000000000002 18 1.0000000000000002 19 1.0000000000000002 20 1.0000000000000002 21 1.0000000000000002 22 1.0000000000000002;
createNode animCurveTU -n "CURVE490";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A334";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 1 2 1 3 1 4 1 5 1 6 1 7 1 8 1 9 1 10 1
		 11 1 12 1 13 1 14 1 15 1 16 1 17 1 18 1 19 1 20 1 21 1 22 1;
createNode animCurveTA -n "CURVE491";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A330";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0 12 0 13 0 14 0 15 0 16 0 17 0 18 0 19 0 20 0 21 0 22 3.5861642606402628;
createNode animCurveTA -n "CURVE492";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A331";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0 12 0 13 0 14 0 15 0 16 0 17 0 18 0 19 0 20 0 21 0 22 0.12335389145613423;
createNode animCurveTA -n "CURVE493";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A332";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0 12 -8.5539315486552709 13 -8.5539315486552709 14 40.79459501331462 15 0 16 0 17 0 18 0 19 0 20 0 21 0 22 -12.236200738685465;
createNode animCurveTL -n "CURVE495";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A338";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
createNode animCurveTL -n "CURVE496";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A339";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
createNode animCurveTL -n "CURVE497";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A33A";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
createNode animCurveTU -n "CURVE499";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A345";
	setAttr ".tan" 9;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0 12 0 13 0 14 0 15 0 16 0 17 0 18 0 19 0 20 0 21 0 22 0;
	setAttr -s 22 ".kot[0:21]"  5 5 5 5 5 5 5 5 
		5 5 5 5 5 5 5 5 5 5 5 5 5 5;
createNode animCurveTL -n "CURVE500";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A33C";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0 12 0 13 0 14 0 15 0 16 0 17 0 18 0 19 0 20 0 21 0 22 0;
createNode animCurveTL -n "CURVE501";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A33D";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0 12 0 13 -0.14 14 -0.040000000000000008 15 -0.15000000000000002 16 -0.15000000000000002 17 0 18 0 19 -0.0004606966634587772 20 0 21 -0.040000000000000008
		 22 -0.07;
createNode animCurveTL -n "CURVE502";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A33E";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0 12 0 13 0 14 0 15 0 16 0 17 0 18 0 19 0 20 0 21 0 22 0;
createNode animCurveTU -n "CURVE503";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A342";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 1 2 1 3 1 4 1 5 1 6 1 7 1 8 1 9 1 10 1
		 11 1 12 1 13 1 14 1 15 1 16 1 17 1 18 1 19 1 20 1 21 1 22 1;
createNode animCurveTU -n "CURVE504";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A343";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 1 2 1 3 1 4 1 5 1 6 1 7 1 8 1 9 1 10 1
		 11 1 12 1 13 1 14 1 15 1 16 1 17 1 18 1 19 1 20 1 21 1 22 1;
createNode animCurveTU -n "CURVE505";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A344";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 1 2 1 3 1 4 1 5 1 6 1 7 1 8 1 9 1 10 1
		 11 1 12 1 13 1 14 1 15 1 16 1 17 1 18 1 19 1 20 1 21 1 22 1;
createNode animCurveTA -n "CURVE506";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A33F";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0 12 0 13 0 14 0 15 0 16 0 17 0 18 0 19 0 20 0 21 0 22 0;
createNode animCurveTA -n "CURVE507";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A340";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0 12 0 13 0 14 0 15 0 16 0 17 0 18 0 19 0 20 0 21 0 22 0;
createNode animCurveTA -n "CURVE508";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A341";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0 12 0 13 0 14 0 15 0 16 0 17 0 18 0 19 0 20 0 21 0 22 0;
createNode animCurveTU -n "CURVE510";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A347";
	setAttr ".tan" 9;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
	setAttr -s 11 ".kot[0:10]"  5 5 5 5 5 5 5 5 
		5 5 5;
createNode animCurveTL -n "CURVE511";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A348";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
createNode animCurveTL -n "CURVE512";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A349";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
createNode animCurveTL -n "CURVE513";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A34A";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
createNode animCurveTU -n "CURVE514";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A34E";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1 2 1 3 1 4 1 5 1 6 1 7 1 8 1 9 1 10 1
		 11 1;
createNode animCurveTU -n "CURVE515";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A352";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
createNode animCurveTU -n "CURVE516";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A34F";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1 2 1 3 1 4 1 5 1 6 1 7 1 8 1 9 1 10 1
		 11 1;
createNode animCurveTU -n "CURVE517";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A350";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1 2 1 3 1 4 1 5 1 6 1 7 1 8 1 9 1 10 1
		 11 1;
createNode animCurveTA -n "CURVE518";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A34B";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
createNode animCurveTA -n "CURVE519";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A34C";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
createNode animCurveTA -n "CURVE520";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A34D";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
createNode animCurveTU -n "CURVE521";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A351";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 -1.5 2 -1.5 3 -1.5 4 -1.5 5 -1.5 6 -1.5
		 7 -1.5 8 -1.5 9 -1.5 10 -1.5 11 -1.5;
createNode animCurveTU -n "CURVE523";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A354";
	setAttr ".tan" 9;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
	setAttr -s 11 ".kot[0:10]"  5 5 5 5 5 5 5 5 
		5 5 5;
createNode animCurveTL -n "CURVE524";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A355";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
createNode animCurveTL -n "CURVE525";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A356";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 -0.012914539160028852 5 0 6 0.16034798658367322 7 0 8 0
		 9 0.98589820372228587 10 0.52011997840398294 11 0.16034798658367322;
createNode animCurveTL -n "CURVE526";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A357";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0.28926265145166763 7 0 8 0 9 0
		 10 0 11 0.28926265145166763;
createNode animCurveTU -n "CURVE527";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A35B";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1 2 1 3 1 4 1 5 1 6 1 7 1 8 1 9 1 10 1
		 11 1;
createNode animCurveTU -n "CURVE528";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A35C";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1 2 1 3 1 4 1 5 1 6 1 7 1 8 1 9 1 10 1
		 11 1;
createNode animCurveTU -n "CURVE529";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A35D";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1 2 1 3 1 4 1 5 1 6 1 7 1 8 1 9 1 10 1
		 11 1;
createNode animCurveTA -n "CURVE530";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A358";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
createNode animCurveTA -n "CURVE531";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A359";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
createNode animCurveTA -n "CURVE532";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A35A";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
createNode animCurveTU -n "CURVE534";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A35F";
	setAttr ".tan" 9;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
	setAttr -s 11 ".kot[0:10]"  5 5 5 5 5 5 5 5 
		5 5 5;
createNode animCurveTL -n "CURVE535";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A360";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0.23435678372989677 2 0.23435678372989677 3 0.23435678372989677 4 0.096616565669555621 5 0.23435678372989677
		 6 0 7 0.23435678372989677 8 0.23435678372989677 9 0.32051364665539861 10 0.5117304656178927 11 0;
createNode animCurveTL -n "CURVE536";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A361";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0.57258242537261594 2 0.57258242537261594 3 0.57258242537261594 4 0.30233771847193225 5 0.57258242537261594
		 6 0 7 0.57258242537261594 8 0.57258242537261594 9 0.57258242537261594 10 0.72256765806841372 11 0;
createNode animCurveTL -n "CURVE537";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A362";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0.082156411134494789 2 0.082156411134494789 3 0.082156411134494789 4 0 5 0.082156411134494789
		 6 0.16783902694371672 7 0.082156411134494789 8 0.082156411134494789 9 0.082156411134494789 10 0.082156411134494789 11 0.16783902694371672;
createNode animCurveTU -n "CURVE538";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A366";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1 2 1 3 1 4 1 5 1 6 1 7 1 8 1 9 1 10 1
		 11 1;
createNode animCurveTU -n "CURVE539";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A367";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1 2 1 3 1 4 1 5 1 6 1 7 1 8 1 9 1 10 1
		 11 1;
createNode animCurveTU -n "CURVE540";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A368";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1 2 1 3 1 4 1 5 1 6 1 7 1 8 1 9 1 10 1
		 11 1;
createNode animCurveTA -n "CURVE541";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A363";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
createNode animCurveTA -n "CURVE542";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A364";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
createNode animCurveTA -n "CURVE543";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A365";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
createNode animCurveTU -n "CURVE545";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A373";
	setAttr ".tan" 9;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0 12 0 13 0 14 0 15 0 16 0 17 0 18 0 19 0 20 0 21 0 22 0;
	setAttr -s 22 ".kot[0:21]"  5 5 5 5 5 5 5 5 
		5 5 5 5 5 5 5 5 5 5 5 5 5 5;
createNode animCurveTL -n "CURVE546";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A36A";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0.86 8 0.86 9 0
		 10 0 11 0 12 0 13 0 14 0 15 0 16 0 17 0 18 0 19 0 20 0 21 0 22 0;
createNode animCurveTL -n "CURVE547";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A36B";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 0 3 0 4 0 5 0.17000000000000004 6 0 7 0 8 0 9 0
		 10 -0.11000000000000001 11 0 12 0 13 0.16000000000000003 14 0 15 0 16 0 17 0.28 18 0.30000000000000004 19 -0.00046069666345877058 20 0 21 0
		 22 0;
createNode animCurveTL -n "CURVE548";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A36C";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0 12 0 13 0 14 0 15 0 16 0 17 0 18 0 19 0 20 0 21 0 22 0;
createNode animCurveTU -n "CURVE549";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A370";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 1 2 1 3 1 4 1 5 1 6 1 7 1 8 1 9 1 10 1
		 11 1 12 1 13 1 14 1 15 1 16 1 17 1 18 1 19 1 20 1 21 1 22 1;
createNode animCurveTU -n "CURVE550";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A371";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 1 2 1 3 1 4 1 5 1 6 1 7 1 8 1 9 1 10 1
		 11 1 12 1 13 1 14 1 15 1 16 1 17 1 18 1 19 1 20 1 21 1 22 1;
createNode animCurveTU -n "CURVE551";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A372";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 1 2 1 3 1 4 1 5 1 6 1 7 1 8 1 9 1 10 1
		 11 1 12 1 13 1 14 1 15 1 16 1 17 1 18 1 19 1 20 1 21 1 22 1;
createNode animCurveTA -n "CURVE552";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A36D";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0 12 0 13 0 14 0 15 0 16 0 17 0 18 0 19 0 20 0 21 0 22 0;
createNode animCurveTA -n "CURVE553";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A36E";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0 12 0 13 0 14 0 15 0 16 0 17 0 18 0 19 0 20 0 21 0 22 0;
createNode animCurveTA -n "CURVE554";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A36F";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0 12 0 13 0 14 0 15 0 16 0 17 0 18 0 19 0 20 0 21 0 22 0;
createNode animCurveTU -n "CURVE556";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A375";
	setAttr ".tan" 9;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
	setAttr -s 11 ".kot[0:10]"  5 5 5 5 5 5 5 5 
		5 5 5;
createNode animCurveTL -n "CURVE557";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A376";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
createNode animCurveTL -n "CURVE558";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A377";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
createNode animCurveTL -n "CURVE559";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A378";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
createNode animCurveTU -n "CURVE560";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A37C";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1 2 1 3 1 4 1 5 1 6 1 7 1 8 1 9 1 10 1
		 11 1;
createNode animCurveTU -n "CURVE561";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A37D";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1 2 1 3 1 4 1 5 1 6 1 7 1 8 1 9 1 10 1
		 11 1;
createNode animCurveTU -n "CURVE562";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A37E";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1 2 1 3 1 4 1 5 1 6 1 7 1 8 1 9 1 10 1
		 11 1;
createNode animCurveTA -n "CURVE563";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A379";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
createNode animCurveTA -n "CURVE564";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A37A";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
createNode animCurveTA -n "CURVE565";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A37B";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
createNode animCurveTU -n "CURVE567";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A380";
	setAttr ".tan" 9;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
	setAttr -s 11 ".kot[0:10]"  5 5 5 5 5 5 5 5 
		5 5 5;
createNode animCurveTL -n "CURVE568";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A381";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0.02506267664759709 3 -0.064622582294660516 4 0 5 0 6 0 7 0 8 -0.060000000000000012
		 9 -0.034314238554179657 10 -0.034314238554179657 11 0;
createNode animCurveTL -n "CURVE569";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A382";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0.29603172839910236 3 0.09634537764671397 4 0 5 0 6 0 7 -0.01999999999999999
		 8 -0.080000000000000016 9 0.011297177867963262 10 0.011297177867963259 11 0;
createNode animCurveTL -n "CURVE570";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A383";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 -0.00025680213367838177 3 0.00054144057440188805 4 0 5 0 6 0 7 0 8 0
		 9 0 10 0 11 0;
createNode animCurveTU -n "CURVE571";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A387";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1 2 1 3 1 4 1 5 1 6 1.0000000000000002 7 1 8 1 9 1
		 10 1 11 1.0000000000000002;
createNode animCurveTU -n "CURVE572";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A388";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1 2 1 3 1 4 1 5 1 6 0.99999999999999989 7 1 8 1 9 1
		 10 1 11 0.99999999999999989;
createNode animCurveTU -n "CURVE573";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A389";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1 2 1 3 1 4 1 5 1 6 1.0000000000000002 7 1 8 1 9 1
		 10 1 11 1.0000000000000002;
createNode animCurveTA -n "CURVE574";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A384";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 -0.11560040519553637 3 0 4 0 5 0 6 0 7 0 8 0 9 0
		 10 0 11 0;
createNode animCurveTA -n "CURVE575";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A385";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0.2509305489265844 3 0 4 0 5 0 6 0 7 0 8 0 9 0
		 10 0 11 0;
createNode animCurveTA -n "CURVE576";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A386";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 -11.356674700454295 3 -1.0852137614911508 4 0 5 0 6 0 7 0 8 0
		 9 0 10 0 11 0;
createNode animCurveTL -n "CURVE578";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A38B";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
createNode animCurveTL -n "CURVE579";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A38C";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
createNode animCurveTL -n "CURVE580";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A38D";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
createNode animCurveTL -n "CURVE582";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A38F";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
createNode animCurveTL -n "CURVE583";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A390";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0.15934605434050211 3 0 4 0.18000000000000002 5 0.11000000000000001 6 -0.088573488268018419
		 7 0.23000000000000004 8 0.06 9 0.12246140578733612 10 0.12246140578733612 11 -0.088573488268018419;
createNode animCurveTL -n "CURVE584";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A391";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
createNode animCurveTU -n "CURVE586";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A393";
	setAttr ".tan" 9;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
	setAttr -s 11 ".kot[0:10]"  5 5 5 5 5 5 5 5 
		5 5 5;
createNode animCurveTL -n "CURVE587";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A394";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
createNode animCurveTL -n "CURVE588";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A395";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 -0.012914539160028852 2 -0.012914539160028852 3 -0.012914539160028852 4 0 5 -0.012914539160028852
		 6 0.16034798658367322 7 -0.012914539160028854 8 -0.012914539160028852 9 1.5311519186423936 10 1.0653736933240907 11 0.16034798658367322;
createNode animCurveTL -n "CURVE589";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A396";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0.28926265145166763 7 0 8 0 9 0.083676861630363517
		 10 0.083676861630363517 11 0.28926265145166763;
createNode animCurveTU -n "CURVE590";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A39A";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1 2 1 3 1 4 1 5 1 6 1 7 1 8 1 9 1 10 1
		 11 1;
createNode animCurveTU -n "CURVE591";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A39B";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1 2 1 3 1 4 1 5 1 6 1 7 1 8 1 9 1 10 1
		 11 1;
createNode animCurveTU -n "CURVE592";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A39C";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1 2 1 3 1 4 1 5 1 6 1 7 1 8 1 9 1 10 1
		 11 1;
createNode animCurveTA -n "CURVE593";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A397";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
createNode animCurveTA -n "CURVE594";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A398";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
createNode animCurveTA -n "CURVE595";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A399";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
createNode animCurveTU -n "CURVE597";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A3A7";
	setAttr ".tan" 9;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0 12 0 13 0 14 0 15 0 16 0 17 0 18 0 19 0 20 0 21 0 22 0;
	setAttr -s 22 ".kot[0:21]"  5 5 5 5 5 5 5 5 
		5 5 5 5 5 5 5 5 5 5 5 5 5 5;
createNode animCurveTL -n "CURVE598";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A39E";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0 12 0 13 0 14 0 15 0 16 0 17 0 18 0 19 0 20 0 21 0 22 0;
createNode animCurveTL -n "CURVE599";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A39F";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0 12 0 13 0 14 0 15 0 16 0 17 0 18 0 19 0 20 0 21 0 22 0;
createNode animCurveTL -n "CURVE600";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A3A0";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0 12 0 13 0 14 0 15 0 16 0 17 0 18 0 19 0 20 0 21 0 22 0;
createNode animCurveTU -n "CURVE601";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A3A4";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 1 2 1 3 1 4 1 5 1 6 1 7 1 8 1 9 1 10 1
		 11 1 12 1 13 1 14 1 15 1 16 1 17 1 18 1 19 1 20 1 21 1 22 1;
createNode animCurveTU -n "CURVE602";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A3A5";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 1 2 1 3 1 4 1 5 1 6 1 7 1 8 1 9 1 10 1
		 11 1 12 1 13 1 14 1 15 1 16 1 17 1 18 1 19 1 20 1 21 1 22 1;
createNode animCurveTU -n "CURVE603";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A3A6";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 1 2 1 3 1 4 1 5 1 6 1 7 1 8 1 9 1 10 1
		 11 1 12 1 13 1 14 1 15 1 16 1 17 1 18 1 19 1 20 1 21 1 22 1;
createNode animCurveTA -n "CURVE604";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A3A1";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0 12 0 13 0 14 0 15 0 16 0 17 0 18 0 19 0 20 0 21 0 22 0;
createNode animCurveTA -n "CURVE605";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A3A2";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0 12 0 13 0 14 0 15 0 16 0 17 0 18 0 19 0 20 0 21 0 22 0;
createNode animCurveTA -n "CURVE606";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A3A3";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0 12 0 13 0 14 0 15 0 16 0 17 0 18 0 19 0 20 0 21 0 22 0;
createNode animCurveTL -n "CURVE608";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A3A9";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
createNode animCurveTL -n "CURVE609";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A3AA";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
createNode animCurveTL -n "CURVE610";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A3AB";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
createNode animCurveTL -n "CURVE612";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A3AD";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
createNode animCurveTL -n "CURVE613";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A3AE";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0.39000000000000007 2 0 3 0 4 0.33000000000000007 5 0.45376929710633207 6 0 7 0.31000000000000005
		 8 0.31000000000000005 9 0.31016652293629976 10 0.39016652293629978 11 0;
createNode animCurveTL -n "CURVE614";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A3AF";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
createNode animCurveTL -n "CURVE616";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A3B1";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0.078634834098057022 7 0 8 0 9 0
		 10 0 11 0.078634834098057022;
createNode animCurveTL -n "CURVE617";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A3B2";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0.080000000000000016 6 0.29466641655124354 7 0 8 0
		 9 0 10 0 11 0.29466641655124354;
createNode animCurveTL -n "CURVE618";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A3B3";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
createNode animCurveTU -n "CURVE620";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A3BE";
	setAttr ".tan" 9;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0 12 0 13 0 14 0 15 0 16 0 17 0 18 0 19 0 20 0 21 0 22 0;
	setAttr -s 22 ".kot[0:21]"  5 5 5 5 5 5 5 5 
		5 5 5 5 5 5 5 5 5 5 5 5 5 5;
createNode animCurveTL -n "CURVE621";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A3B5";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0 12 0 13 0 14 0 15 0 16 0 17 0 18 0 19 0 20 0 21 0 22 0;
createNode animCurveTL -n "CURVE622";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A3B6";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0.040000000000000008 8 0.040000000000000008
		 9 0 10 0 11 0 12 0 13 0 14 0 15 0 16 0 17 0 18 0 19 -0.0004606966634587772 20 0 21 0 22 0.080000000000000016;
createNode animCurveTL -n "CURVE623";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A3B7";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0 12 0 13 0 14 0 15 0 16 0 17 0 18 0 19 0 20 0 21 0 22 0;
createNode animCurveTU -n "CURVE624";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A3BB";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 1 2 1 3 1 4 1 5 1 6 1 7 1 8 1 9 1 10 1
		 11 1 12 1 13 1 14 1 15 1 16 1 17 1 18 1 19 1 20 1 21 1 22 1;
createNode animCurveTU -n "CURVE625";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A3BC";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 1 2 1 3 1 4 1 5 1 6 1 7 1 8 1 9 1 10 1
		 11 1 12 1 13 1 14 1 15 1 16 1 17 1 18 1 19 0.6222222329078676 20 1 21 1 22 1;
createNode animCurveTU -n "CURVE626";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A3BD";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 1 2 1 3 1 4 1 5 1 6 1 7 1 8 1 9 1 10 1
		 11 1 12 1 13 1 14 1 15 1 16 1 17 1 18 1 19 1 20 1 21 1 22 1;
createNode animCurveTA -n "CURVE627";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A3B8";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 -4.0107045659157627 2 -1.3750987083139758 3 -3.1530879438387198 4 -3.1530879438387198 5 0.62058246491916469
		 6 0 7 -2.0626480624709633 8 0.57295779513082357 9 -2.9793805346802809 10 0 11 -1.088619810748563 12 0 13 0 14 -3.5523383298111044 15 -2.1772396214971286 16 -2.1772396214971286
		 17 0 18 0 19 -3.2595874208240039 20 -2.1772396214971286 21 -2.1772396214971286 22 -2.7501974166279521;
createNode animCurveTA -n "CURVE628";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A3B9";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 0 3 -0.16256184859811001 4 0.16256184859811001 5 0 6 0 7 0 8 0
		 9 0 10 0 11 0 12 0 13 0 14 0 15 0 16 0 17 0 18 0 19 0 20 0 21 0 22 0;
createNode animCurveTA -n "CURVE629";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A3BA";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 1.8334649444186344 3 -1.3884101755674472 4 1.3884101755674472 5 0 6 0 7 0
		 8 0 9 0 10 0 11 0 12 0 13 0 14 0 15 0 16 0 17 0 18 0 19 0 20 0 21 0 22 0;
createNode animCurveTU -n "CURVE631";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A3C9";
	setAttr ".tan" 9;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0 12 0 13 0 14 0 15 0 16 0 17 0 18 0 19 0 20 0 21 0 22 0;
	setAttr -s 22 ".kot[0:21]"  5 5 5 5 5 5 5 5 
		5 5 5 5 5 5 5 5 5 5 5 5 5 5;
createNode animCurveTL -n "CURVE632";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A3C0";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 0.69944414173468916 3 0 4 0 5 0 6 0 7 0 8 0 9 0
		 10 0 11 0.19772088978249691 12 0 13 0 14 0.14 15 0.28 16 0.14 17 0 18 0 19 0 20 0.14 21 0.14 22 0.14;
createNode animCurveTL -n "CURVE633";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A3C1";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 0.1371134258168599 3 0 4 0 5 0 6 0 7 0 8 0 9 0
		 10 0 11 0 12 0 13 0.090000000000000011 14 0 15 0 16 0.12000000000000002 17 0 18 0 19 -0.0004606966634587772 20 0 21 0 22 -0.38;
createNode animCurveTL -n "CURVE634";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A3C2";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 0.022003414043991122 3 0 4 0 5 0 6 0 7 0 8 0 9 0
		 10 0 11 0 12 0 13 0 14 0 15 0 16 0 17 0 18 0 19 0 20 0 21 0 22 0;
createNode animCurveTU -n "CURVE635";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A3C6";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 1 2 1 3 1 4 1 5 1 6 1 7 1 8 1 9 1 10 1
		 11 1 12 1 13 1 14 1 15 1 16 1 17 1 18 1 19 1 20 1 21 1 22 1;
createNode animCurveTU -n "CURVE636";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A3C7";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 1 2 1 3 1 4 1 5 1 6 1 7 1 8 1 9 1 10 1
		 11 1 12 1 13 0.82277268796079195 14 1 15 1 16 1 17 1 18 1 19 1 20 1 21 1 22 1;
createNode animCurveTU -n "CURVE637";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A3C8";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 1 2 1 3 1 4 1 5 1 6 1 7 1 8 1 9 1 10 1
		 11 1 12 1 13 1 14 1 15 1 16 1 17 1 18 1 19 1 20 1 21 1 22 1;
createNode animCurveTA -n "CURVE638";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A3C3";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 -22.589710954883149 3 0 4 0 5 0 6 0 7 0 8 0 9 0
		 10 0 11 0 12 0 13 0 14 0 15 0 16 0 17 0 18 0 19 0 20 0 21 0 22 0;
createNode animCurveTA -n "CURVE639";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A3C4";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0 12 0 13 0 14 0 15 0 16 0 17 0 18 0 19 0 20 0 21 0 22 0;
createNode animCurveTA -n "CURVE640";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A3C5";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 4.4502425122695257 12 0 13 -2.1772396214971286 14 0 15 0 16 -7.4484513367007024 17 0 18 0 19 0 20 0 21 0 22 0;
createNode animCurveTU -n "CURVE642";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A3D1";
	setAttr ".tan" 9;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0 12 0 13 0 14 0 15 0 16 0 17 0 18 0 19 0 20 0 21 0 22 0;
	setAttr -s 22 ".kot[0:21]"  5 5 5 5 5 5 5 5 
		5 5 5 5 5 5 5 5 5 5 5 5 5 5;
createNode animCurveTU -n "CURVE643";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A3D4";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0.25 2 0.25 3 0.25 4 0.25 5 0.25 6 0.25
		 7 0.25 8 0.25 9 0.25 10 0.25 11 0.25 12 0.25 13 0.25 14 0.25 15 0.25 16 0.25 17 0.25
		 18 0.25 19 0.25 20 0.25 21 0.25 22 0.25;
createNode animCurveTL -n "CURVE644";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A3CB";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0.16000000000000003 2 0.056034580744222268 3 0.1 4 0.1 5 0.17 6 0.19426376082174363
		 7 0.03 8 0.030000000000000006 9 0.42 10 0.67 11 -0.30000000000000004 12 0.12 13 0.17000000000000004 14 -0.22843167999740221 15 -0.2784316799974022 16 -0.078431679997402193
		 17 0 18 -0.15000000000000002 19 0.13 20 -0.89843167999740225 21 -0.51843167999740225 22 -0.2784316799974022;
createNode animCurveTL -n "CURVE645";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A3CC";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 -0.32999999999999996 2 -0.27234092932186205 3 -0.1739299901509288 4 -0.20308998783350024 5 -0.043929990150928799
		 6 0 7 -0.27000000000000007 8 -0.27000000000000007 9 0.34 10 0.62000000000000011 11 0.06894295992749154 12 0.080000000000000016 13 0.24000000000000002 14 -0.17439119648845666 15 -0.17439119648845663
		 16 0.065608803511543412 17 0 18 0 19 -0.0004606966634587772 20 -0.17439119648845663 21 -0.17439119648845663 22 -0.17439119648845663;
createNode animCurveTL -n "CURVE646";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A3CD";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 0.033616835188205456 3 0 4 0 5 0 6 0 7 0 8 0 9 0
		 10 0 11 0 12 0 13 0 14 0 15 0 16 0 17 0 18 0 19 0 20 0 21 0 22 0;
createNode animCurveTU -n "CURVE647";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A3D3";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 1 2 1 3 1 4 1 5 1 6 1 7 1 8 1 9 1 10 1
		 11 1 12 1 13 1 14 1 15 1 16 1 17 1 18 1 19 1 20 1 21 1 22 1;
createNode animCurveTA -n "CURVE648";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A3CE";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0 12 0 13 0 14 0 15 0 16 0 17 0 18 0 19 0 20 0 21 0 22 0;
createNode animCurveTA -n "CURVE649";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A3CF";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0 12 0 13 0 14 0 15 0 16 0 17 0 18 0 19 0 20 0 21 0 22 0;
createNode animCurveTA -n "CURVE650";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A3D0";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0 12 0 13 0 14 0 15 0 16 0 17 0 18 0 19 0 20 0 21 0 22 0;
createNode animCurveTU -n "CURVE651";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A3D2";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 1 2 1 3 1 4 1 5 1 6 1 7 1 8 1 9 1 10 1
		 11 1 12 1 13 1 14 1 15 1 16 1 17 1 18 1 19 1 20 1 21 1 22 1;
createNode animCurveTU -n "CURVE653";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A3D6";
	setAttr ".tan" 9;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
	setAttr -s 11 ".kot[0:10]"  5 5 5 5 5 5 5 5 
		5 5 5;
createNode animCurveTL -n "CURVE654";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A3D7";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 -0.080000000000000016 2 0 3 -0.080000000000000016 4 0.06 5 -0.2 6 0
		 7 -0.07 8 -0.16000000000000003 9 0.0079478736618736612 10 0.0079478736618736716 11 0;
createNode animCurveTL -n "CURVE655";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A3D8";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 -0.12000000000000002 2 -0.17000000000000004 3 -0.22000000000000003 4 0.24000000000000005 5 -0.080000000000000016
		 6 0.28 7 0.22000000000000003 8 -0.11000000000000004 9 0.11191975405177004 10 0.26191975405177004 11 0.28;
createNode animCurveTL -n "CURVE656";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A3D9";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
createNode animCurveTU -n "CURVE657";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A3DD";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1 2 1 3 1 4 1 5 1 6 1 7 1 8 1 9 1 10 1
		 11 1;
createNode animCurveTU -n "CURVE658";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A3DE";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1 2 1 3 1 4 1 5 1 6 1 7 1 8 1 9 1 10 1
		 11 1;
createNode animCurveTU -n "CURVE659";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A3DF";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1 2 1 3 1 4 1 5 1 6 1 7 1 8 1 9 1 10 1
		 11 1;
createNode animCurveTA -n "CURVE660";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A3DA";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
createNode animCurveTA -n "CURVE661";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A3DB";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
createNode animCurveTA -n "CURVE662";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A3DC";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 -25.095551426730061 4 -11.688339020668794 5 -5.3858032742297404 6 0 7 -15.933445258173935
		 8 6.5265003109543382 9 1.260507149287811 10 1.2605071492878113 11 0;
createNode animCurveTL -n "CURVE664";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A3E1";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 -0.10623070285949332 5 0 6 0 7 0 8 0 9 0
		 10 0 11 0;
createNode animCurveTL -n "CURVE665";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A3E2";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 -0.38000000000000006 2 0 3 -0.58000000000000007 4 -0.41606417995733991 5 -0.53 6 -0.42000000000000004
		 7 -0.23999999999999996 8 0 9 -0.42775099308246245 10 -0.51775099308246242 11 -0.42000000000000004;
createNode animCurveTL -n "CURVE666";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A3E3";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
createNode animCurveTU -n "CURVE668";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A3EE";
	setAttr ".tan" 9;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0 12 0 13 0 14 0 15 0 16 0 17 0 18 0 19 0 20 0 21 0 22 0;
	setAttr -s 22 ".kot[0:21]"  5 5 5 5 5 5 5 5 
		5 5 5 5 5 5 5 5 5 5 5 5 5 5;
createNode animCurveTL -n "CURVE669";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A3E7";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0 12 0 13 0 14 0.07 15 0 16 0 17 0 18 0 19 0 20 0 21 0.07 22 0.07;
createNode animCurveTL -n "CURVE670";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A3E5";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 -0.090000000000000011 2 -0.24495468991398184 3 0 4 0 5 0 6 0 7 0 8 0
		 9 0 10 0 11 -0.16000000000000025 12 -0.17000000000000004 13 -0.26 14 0 15 0 16 -0.21000000000000002 17 -0.17000000000000004 18 0 19 -0.0004606966634587772
		 20 0 21 0 22 0.26;
createNode animCurveTL -n "CURVE671";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A3E6";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0 12 0 13 0 14 0 15 0 16 0 17 0 18 0 19 0 20 0 21 0 22 0;
createNode animCurveTU -n "CURVE672";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A3EB";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 1 2 0.99999999999999978 3 0.99999999999999978 4 0.99999999999999978 5 0.99999999999999978
		 6 1 7 0.99999999999999978 8 0.99999999999999978 9 0.99999999999999978 10 0.99999999999999978 11 0.99999999999999978 12 0.99999999999999978 13 0.99999999999999978 14 0.99999999999999978
		 15 0.99999999999999978 16 0.99999999999999978 17 0.99999999999999978 18 0.99999999999999978 19 0.99999999999999978 20 0.99999999999999978 21 0.99999999999999978 22 0.99999999999999978;
createNode animCurveTU -n "CURVE673";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A3EC";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 1 2 1 3 1 4 1 5 1 6 1 7 1 8 1 9 1 10 1
		 11 1 12 1 13 1 14 1 15 1 16 1 17 1 18 1 19 1 20 1 21 1 22 1;
createNode animCurveTU -n "CURVE674";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A3ED";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 1 2 1 3 1 4 1 5 1 6 1 7 1 8 1 9 1 10 1
		 11 1 12 1 13 1 14 1 15 1 16 1 17 1 18 1 19 1 20 1 21 1 22 1;
createNode animCurveTA -n "CURVE675";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A3E8";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0 12 0 13 0 14 0 15 0 16 0 17 0 18 0 19 0 20 0 21 0 22 0;
createNode animCurveTA -n "CURVE676";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A3E9";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0 12 0 13 0 14 0 15 0 16 0 17 0 18 0 19 0 20 0 21 0 22 0;
createNode animCurveTA -n "CURVE677";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A3EA";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0 12 0 13 0 14 0 15 0 16 0 17 0 18 0 19 0 20 0 21 0 22 0;
createNode animCurveTL -n "CURVE679";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A3F0";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0.049999999999999989 2 0.11000000000000001 3 0.010000000000000009 4 -0.05 5 -0.049999999999999989
		 6 -0.090000000000000011 7 -0.15 8 -0.093578155073438127 9 -0.1 10 -0.16000000000000003 11 -0.090000000000000011;
createNode animCurveTL -n "CURVE680";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A3F1";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 -0.46000000000000008 3 -0.16000000000000003 4 -0.020000000000000018 5 0.14 6 0
		 7 0 8 -0.32209998240470916 9 0.070000000000000062 10 0.13000000000000006 11 0;
createNode animCurveTU -n "CURVE682";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A3FC";
	setAttr ".tan" 9;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0 12 0 13 0 14 0 15 0 16 0 17 0 18 0 19 0 20 0 21 0 22 0;
	setAttr -s 22 ".kot[0:21]"  5 5 5 5 5 5 5 5 
		5 5 5 5 5 5 5 5 5 5 5 5 5 5;
createNode animCurveTL -n "CURVE683";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A3F3";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0 12 0 13 0 14 0 15 0 16 0 17 0 18 0 19 0 20 0 21 0 22 0;
createNode animCurveTL -n "CURVE684";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A3F4";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0 12 0 13 0 14 0 15 0 16 0 17 0 18 0 19 0 20 0 21 0 22 0;
createNode animCurveTL -n "CURVE685";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A3F5";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0 12 0 13 0 14 0 15 0 16 0 17 0 18 0 19 0 20 0 21 0 22 0;
createNode animCurveTU -n "CURVE686";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A3F9";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 1 2 1 3 1 4 1 5 1 6 1 7 1 8 1 9 1 10 1
		 11 1 12 1 13 1 14 1 15 1 16 1 17 1 18 1 19 1 20 1 21 1 22 1;
createNode animCurveTU -n "CURVE687";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A3FA";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 1 2 1 3 1 4 1 5 1 6 1 7 1 8 1 9 1 10 1
		 11 1 12 1 13 1 14 1 15 1 16 1 17 1 18 1 19 1 20 1 21 1 22 1;
createNode animCurveTU -n "CURVE688";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A3FB";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 1 2 1 3 1 4 1 5 1 6 1 7 1 8 1 9 1 10 1
		 11 1 12 1 13 1 14 1 15 1 16 1 17 1 18 1 19 1 20 1 21 1 22 1;
createNode animCurveTA -n "CURVE689";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A3F6";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0 12 0 13 0 14 0 15 0 16 0 17 -10.323796418459514 18 0 19 0 20 0 21 0 22 0;
createNode animCurveTA -n "CURVE690";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A3F7";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0 12 0 13 0 14 0 15 0 16 0 17 0 18 0 19 0 20 0 21 0 22 0;
createNode animCurveTA -n "CURVE691";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A3F8";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0 12 0 13 0 14 0 15 0 16 0 17 0 18 0 19 0 20 0 21 0 22 0;
createNode animCurveTU -n "CURVE693";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A407";
	setAttr ".tan" 9;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0 12 0 13 0 14 0 15 0 16 0 17 0 18 0 19 0 20 0 21 0 22 0;
	setAttr -s 22 ".kot[0:21]"  5 5 5 5 5 5 5 5 
		5 5 5 5 5 5 5 5 5 5 5 5 5 5;
createNode animCurveTL -n "CURVE694";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A3FE";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0 12 0 13 0 14 0 15 0 16 0 17 0 18 0 19 0 20 0 21 0 22 0;
createNode animCurveTL -n "CURVE695";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A3FF";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0 12 0 13 0 14 0 15 0 16 0 17 0 18 0 19 0 20 0 21 0 22 0.040000000000000008;
createNode animCurveTL -n "CURVE696";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A400";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0 12 0 13 0 14 0 15 0 16 0 17 0 18 0 19 0 20 0 21 0 22 0;
createNode animCurveTU -n "CURVE697";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A404";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 1 2 1 3 1 4 1 5 1 6 1 7 1 8 1 9 1 10 1.1400000000000001
		 11 1 12 1 13 1 14 1 15 1 16 1 17 1 18 1 19 1 20 1 21 1 22 1;
createNode animCurveTU -n "CURVE698";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A405";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 1 2 1 3 1 4 1 5 1 6 1 7 1 8 1 9 1 10 1
		 11 1 12 1 13 1 14 1 15 1 16 1 17 1 18 1 19 1 20 1 21 1 22 1;
createNode animCurveTU -n "CURVE699";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A406";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 1 2 1 3 1 4 1 5 1 6 1 7 1 8 1 9 1 10 1
		 11 1 12 1 13 1 14 1 15 1 16 1 17 1 18 1 19 1 20 1 21 1 22 1;
createNode animCurveTA -n "CURVE700";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A401";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0 12 0 13 0 14 0 15 0 16 0 17 0 18 0 19 0 20 0 21 0 22 0;
createNode animCurveTA -n "CURVE701";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A402";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0 12 0 13 0 14 0 15 0 16 0 17 0 18 0 19 0 20 0 21 0 22 0;
createNode animCurveTA -n "CURVE702";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A403";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0 12 0 13 0 14 0 15 0 16 0 17 0 18 0 19 0 20 0 21 0 22 0;
createNode animCurveTL -n "CURVE704";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A409";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
createNode animCurveTL -n "CURVE705";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A40A";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
createNode animCurveTL -n "CURVE706";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A40B";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
createNode animCurveTU -n "CURVE708";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A40D";
	setAttr ".tan" 9;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
	setAttr -s 11 ".kot[0:10]"  5 5 5 5 5 5 5 5 
		5 5 5;
createNode animCurveTL -n "CURVE709";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A40E";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 -0.080000000000000016 2 0 3 0.060000000000000012 4 -0.08 5 -0.20000000000000004 6 0
		 7 -0.07 8 -0.16000000000000003 9 0 10 0 11 0;
createNode animCurveTL -n "CURVE710";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A40F";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 -0.12 2 -0.17000000000000004 3 0.24000000000000005 4 -0.22000000000000003 5 -0.23000000000000007
		 6 0.28 7 0.22000000000000003 8 -0.11000000000000004 9 0.27 10 0.31000000000000005 11 0.28;
createNode animCurveTL -n "CURVE711";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A410";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
createNode animCurveTU -n "CURVE712";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A414";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1 2 1 3 1 4 1 5 1 6 1 7 1 8 1 9 1 10 1
		 11 1;
createNode animCurveTU -n "CURVE713";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A415";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1 2 1 3 1 4 1 5 1 6 1 7 1 8 1 9 1 10 1
		 11 1;
createNode animCurveTU -n "CURVE714";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A416";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1 2 1 3 1 4 1 5 1 6 1 7 1 8 1 9 1 10 1
		 11 1;
createNode animCurveTA -n "CURVE715";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A411";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
createNode animCurveTA -n "CURVE716";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A412";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
createNode animCurveTA -n "CURVE717";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A413";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 -11.688339020668794 4 -25.095551426730061 5 -5.3858032742297404 6 0 7 -15.933445258173931
		 8 6.5265003109543418 9 0 10 0 11 0;
createNode animCurveTU -n "CURVE719";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A421";
	setAttr ".tan" 9;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0 12 0 13 0 14 0 15 0 16 0 17 0 18 0 19 0 20 0 21 0 22 0;
	setAttr -s 22 ".kot[0:21]"  5 5 5 5 5 5 5 5 
		5 5 5 5 5 5 5 5 5 5 5 5 5 5;
createNode animCurveTL -n "CURVE720";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A418";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0 12 0 13 0 14 0 15 0 16 0 17 0 18 0 19 0 20 0 21 0 22 0;
createNode animCurveTL -n "CURVE721";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A419";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0 12 0 13 0 14 0 15 0 16 0 17 0 18 0 19 0 20 0 21 0 22 0;
createNode animCurveTL -n "CURVE722";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A41A";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0 12 0 13 0 14 0 15 0 16 0 17 0 18 0 19 0 20 0 21 0 22 0;
createNode animCurveTU -n "CURVE723";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A41E";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 1 2 1 3 1 4 1 5 1 6 1 7 1 8 1 9 1 10 1
		 11 1 12 1 13 1 14 1 15 1 16 1 17 1 18 1 19 1 20 1 21 1 22 1;
createNode animCurveTU -n "CURVE724";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A41F";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 1 2 1 3 1 4 1 5 1 6 1 7 1 8 1 9 1 10 1
		 11 1 12 1 13 1 14 1 15 1 16 1 17 1 18 1 19 1 20 1 21 1 22 1;
createNode animCurveTU -n "CURVE725";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A420";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 1 2 1 3 1 4 1 5 1 6 1 7 1 8 1 9 1 10 1
		 11 1 12 1 13 1 14 1 15 1 16 1 17 1 18 1 19 1 20 1 21 1 22 1;
createNode animCurveTA -n "CURVE726";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A41B";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0 12 0 13 0 14 0 15 0 16 0 17 0 18 0 19 0 20 0 21 0 22 0;
createNode animCurveTA -n "CURVE727";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A41C";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0 12 0 13 0 14 0 15 0 16 0 17 0 18 0 19 0 20 0 21 0 22 0;
createNode animCurveTA -n "CURVE728";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A41D";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0 12 0 13 0 14 0 15 0 16 0 17 0 18 0 19 0 20 0 21 0 22 0;
createNode animCurveTL -n "CURVE730";
	rename -uid "5CEB0D80-0000-0D99-657C-B6450001A423";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
createNode animCurveTL -n "CURVE731";
	rename -uid "5CEB0D80-0000-0D99-657C-B6460001A424";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
createNode animCurveTL -n "CURVE732";
	rename -uid "5CEB0D80-0000-0D99-657C-B6460001A425";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
createNode animCurveTU -n "CURVE734";
	rename -uid "5CEB0D80-0000-0D99-657C-B6460001A427";
	setAttr ".tan" 9;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
	setAttr -s 11 ".kot[0:10]"  5 5 5 5 5 5 5 5 
		5 5 5;
createNode animCurveTL -n "CURVE735";
	rename -uid "5CEB0D80-0000-0D99-657C-B6460001A428";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
createNode animCurveTL -n "CURVE736";
	rename -uid "5CEB0D80-0000-0D99-657C-B6460001A429";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 -0.17000000000000004 8 -0.17000000000000004
		 9 0 10 0 11 0;
createNode animCurveTL -n "CURVE737";
	rename -uid "5CEB0D80-0000-0D99-657C-B6460001A42A";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
createNode animCurveTU -n "CURVE738";
	rename -uid "5CEB0D80-0000-0D99-657C-B6460001A42E";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1 2 1 3 1 4 1 5 1 6 1 7 1 8 1 9 1 10 1
		 11 1;
createNode animCurveTU -n "CURVE739";
	rename -uid "5CEB0D80-0000-0D99-657C-B6460001A42F";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1 2 1 3 1 4 1 5 1 6 1 7 1 8 1 9 1 10 1
		 11 1;
createNode animCurveTU -n "CURVE740";
	rename -uid "5CEB0D80-0000-0D99-657C-B6460001A430";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1 2 1 3 1 4 1 5 1 6 1 7 1 8 1 9 1 10 1
		 11 1;
createNode animCurveTA -n "CURVE741";
	rename -uid "5CEB0D80-0000-0D99-657C-B6460001A42B";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
createNode animCurveTA -n "CURVE742";
	rename -uid "5CEB0D80-0000-0D99-657C-B6460001A42C";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
createNode animCurveTA -n "CURVE743";
	rename -uid "5CEB0D80-0000-0D99-657C-B6460001A42D";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
createNode animCurveTU -n "CURVE745";
	rename -uid "5CEB0D80-0000-0D99-657C-B6460001A432";
	setAttr ".tan" 9;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
	setAttr -s 11 ".kot[0:10]"  5 5 5 5 5 5 5 5 
		5 5 5;
createNode animCurveTL -n "CURVE746";
	rename -uid "5CEB0D80-0000-0D99-657C-B6460001A433";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 -0.024984993395597333 3 0 4 0 5 0 6 0 7 0 8 -0.060000000000000012
		 9 0 10 0 11 0;
createNode animCurveTL -n "CURVE747";
	rename -uid "5CEB0D80-0000-0D99-657C-B6460001A434";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0.29603280331369225 3 0 4 0.040000000000000008 5 0 6 0 7 -0.01999999999999999
		 8 -0.080000000000000016 9 0.016677174630956915 10 0.016677174630956922 11 0;
createNode animCurveTL -n "CURVE748";
	rename -uid "5CEB0D80-0000-0D99-657C-B6460001A435";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0.0019197748594978943 3 0 4 0 5 0 6 0 7 0 8 0 9 0
		 10 0 11 0;
createNode animCurveTU -n "CURVE749";
	rename -uid "5CEB0D80-0000-0D99-657C-B6460001A439";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1 2 1 3 1 4 1 5 1 6 1 7 1 8 1 9 1 10 1
		 11 1;
createNode animCurveTU -n "CURVE750";
	rename -uid "5CEB0D80-0000-0D99-657C-B6460001A43A";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1 2 1 3 1 4 1 5 1 6 1.0000000000000002 7 1 8 1 9 1
		 10 1 11 1.0000000000000002;
createNode animCurveTU -n "CURVE751";
	rename -uid "5CEB0D80-0000-0D99-657C-B6460001A43B";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1 2 1 3 1 4 1 5 1 6 1.0000000000000002 7 1 8 1 9 1
		 10 1 11 1.0000000000000002;
createNode animCurveTA -n "CURVE752";
	rename -uid "5CEB0D80-0000-0D99-657C-B6460001A436";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0.8642268920935855 3 0 4 0 5 0 6 0 7 0 8 0 9 0
		 10 0 11 0;
createNode animCurveTA -n "CURVE753";
	rename -uid "5CEB0D80-0000-0D99-657C-B6460001A437";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0.26766188657152262 3 0 4 0 5 0 6 0 7 0 8 0 9 0
		 10 0 11 0;
createNode animCurveTA -n "CURVE754";
	rename -uid "5CEB0D80-0000-0D99-657C-B6460001A438";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 11.325822412289396 3 0 4 0 5 0 6 0 7 0 8 0 9 0
		 10 0 11 0;
createNode animCurveTL -n "CURVE756";
	rename -uid "5CEB0D80-0000-0D99-657C-B6460001A43D";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
createNode animCurveTL -n "CURVE757";
	rename -uid "5CEB0D80-0000-0D99-657C-B6460001A43E";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0.10623070289369649 3 0.18000000000000002 4 0 5 -0.030000000000000006 6 -0.088573488268018419
		 7 0.38 8 0.20999999999999996 9 0 10 0 11 -0.088573488268018419;
createNode animCurveTL -n "CURVE758";
	rename -uid "5CEB0D80-0000-0D99-657C-B6460001A43F";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
createNode animCurveTL -n "CURVE760";
	rename -uid "5CEB0D80-0000-0D99-657C-B6460001A441";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0.1 6 0 7 0 8 0 9 0 10 0
		 11 0;
createNode animCurveTL -n "CURVE761";
	rename -uid "5CEB0D80-0000-0D99-657C-B6460001A442";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0.69652658959362246 2 0.35410234297890303 3 0.52475628863842938 4 0 5 0.8 6 0.35429395307207368
		 7 0.38000000000000006 8 0.34000000000000008 9 0.40762433249849328 10 0.62762433249849336 11 0.35429395307207368;
createNode animCurveTL -n "CURVE762";
	rename -uid "5CEB0D80-0000-0D99-657C-B6460001A443";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
createNode animCurveTL -n "CURVE764";
	rename -uid "5CEB0D80-0000-0D99-657C-B6460001A445";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 -0.09159095007444118 7 0 8 0 9 0
		 10 0 11 -0.09159095007444118;
createNode animCurveTL -n "CURVE765";
	rename -uid "5CEB0D80-0000-0D99-657C-B6460001A446";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 -0.21374567943081502 7 0 8 0 9 0
		 10 0 11 -0.21374567943081502;
createNode animCurveTL -n "CURVE766";
	rename -uid "5CEB0D80-0000-0D99-657C-B6460001A447";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
createNode animCurveTU -n "CURVE768";
	rename -uid "5CEB0D80-0000-0D99-657C-B6460001A449";
	setAttr ".tan" 9;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
	setAttr -s 11 ".kot[0:10]"  5 5 5 5 5 5 5 5 
		5 5 5;
createNode animCurveTL -n "CURVE769";
	rename -uid "5CEB0D80-0000-0D99-657C-B6460001A44A";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
createNode animCurveTL -n "CURVE770";
	rename -uid "5CEB0D80-0000-0D99-657C-B6460001A44B";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
createNode animCurveTL -n "CURVE771";
	rename -uid "5CEB0D80-0000-0D99-657C-B6460001A44C";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
createNode animCurveTU -n "CURVE772";
	rename -uid "5CEB0D80-0000-0D99-657C-B6460001A450";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1 2 1 3 1 4 1 5 1 6 1 7 1 8 1 9 1 10 1
		 11 1;
createNode animCurveTU -n "CURVE773";
	rename -uid "5CEB0D80-0000-0D99-657C-B6460001A451";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1 2 1 3 1 4 1 5 1 6 1 7 1 8 1 9 1 10 1
		 11 1;
createNode animCurveTU -n "CURVE774";
	rename -uid "5CEB0D80-0000-0D99-657C-B6460001A452";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1 2 1 3 1 4 1 5 1 6 1 7 1 8 1 9 1 10 1
		 11 1;
createNode animCurveTA -n "CURVE775";
	rename -uid "5CEB0D80-0000-0D99-657C-B6460001A44D";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
createNode animCurveTA -n "CURVE776";
	rename -uid "5CEB0D80-0000-0D99-657C-B6460001A44E";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
createNode animCurveTA -n "CURVE777";
	rename -uid "5CEB0D80-0000-0D99-657C-B6460001A44F";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
createNode animCurveTU -n "CURVE779";
	rename -uid "5CEB0D80-0000-0D99-657C-B6460001A45D";
	setAttr ".tan" 9;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0 12 0 13 0 14 0 15 0 16 0 17 0 18 0 19 0 20 0 21 0 22 0;
	setAttr -s 22 ".kot[0:21]"  5 5 5 5 5 5 5 5 
		5 5 5 5 5 5 5 5 5 5 5 5 5 5;
createNode animCurveTL -n "CURVE780";
	rename -uid "5CEB0D80-0000-0D99-657C-B6460001A454";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0 12 0 13 0 14 0 15 0 16 0 17 0 18 0 19 0 20 0 21 0 22 0;
createNode animCurveTL -n "CURVE781";
	rename -uid "5CEB0D80-0000-0D99-657C-B6460001A455";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 0 3 0.030000000000000006 4 0.030000000000000006 5 0.030000000000000006 6 0 7 0.030000000000000006
		 8 0.030000000000000006 9 0 10 0 11 0 12 0.080000000000000016 13 0 14 0 15 0 16 0 17 0 18 0 19 -0.0004606966634587772 20 0 21 0
		 22 0;
createNode animCurveTL -n "CURVE782";
	rename -uid "5CEB0D80-0000-0D99-657C-B6460001A456";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0 12 0 13 0 14 0 15 0 16 0 17 0 18 0 19 0 20 0 21 0 22 0;
createNode animCurveTU -n "CURVE783";
	rename -uid "5CEB0D80-0000-0D99-657C-B6460001A45A";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 1 2 1 3 1 4 1 5 1 6 1 7 1 8 1 9 1 10 1
		 11 1 12 1 13 1 14 1 15 1 16 1 17 1 18 1 19 1 20 1 21 1 22 1;
createNode animCurveTU -n "CURVE784";
	rename -uid "5CEB0D80-0000-0D99-657C-B6460001A45B";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 1 2 1 3 1 4 1 5 1 6 1 7 1 8 1 9 1 10 1
		 11 1 12 1 13 1 14 1 15 1 16 1 17 1 18 1 19 1 20 1 21 1 22 1;
createNode animCurveTU -n "CURVE785";
	rename -uid "5CEB0D80-0000-0D99-657C-B6460001A45C";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 1 2 1 3 1 4 1 5 1 6 1 7 1 8 1 9 1 10 1
		 11 1 12 1 13 1 14 1 15 1 16 1 17 1 18 1 19 1 20 1 21 1 22 1;
createNode animCurveTA -n "CURVE786";
	rename -uid "5CEB0D80-0000-0D99-657C-B6460001A459";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0 12 0 13 0 14 0 15 0 16 0 17 0 18 0 19 0 20 0 21 0 22 0;
createNode animCurveTA -n "CURVE787";
	rename -uid "5CEB0D80-0000-0D99-657C-B6460001A457";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0 12 0 13 0 14 0 15 0 16 0 17 0 18 0 19 0 20 0 21 0 22 0;
createNode animCurveTA -n "CURVE788";
	rename -uid "5CEB0D80-0000-0D99-657C-B6460001A458";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 0 3 -1.6044792429942574 4 1.6044792429942574 5 0 6 0 7 1.1459155902616467
		 8 1.1459155902616467 9 0.80214091318315262 10 1.2605071492878113 11 0 12 0 13 0 14 0 15 0 16 0 17 0 18 0 19 0 20 0 21 0
		 22 0;
createNode animCurveTU -n "CURVE790";
	rename -uid "5CEB0D80-0000-0D99-657C-B6460001A468";
	setAttr ".tan" 9;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0 12 0 13 0 14 0 15 0 16 0 17 0 18 0 19 0 20 0 21 0 22 0;
	setAttr -s 22 ".kot[0:21]"  5 5 5 5 5 5 5 5 
		5 5 5 5 5 5 5 5 5 5 5 5 5 5;
createNode animCurveTL -n "CURVE791";
	rename -uid "5CEB0D80-0000-0D99-657C-B6460001A45F";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0 12 0 13 0 14 0 15 0 16 0 17 0 18 0 19 0 20 0 21 0 22 0;
createNode animCurveTL -n "CURVE792";
	rename -uid "5CEB0D80-0000-0D99-657C-B6460001A460";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0 12 0 13 0 14 0 15 0 16 0 17 0 18 0 19 0 20 0 21 0 22 0;
createNode animCurveTL -n "CURVE793";
	rename -uid "5CEB0D80-0000-0D99-657C-B6460001A461";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0 12 0 13 0 14 0 15 0 16 0 17 0 18 0 19 0 20 0 21 0 22 0;
createNode animCurveTU -n "CURVE794";
	rename -uid "5CEB0D80-0000-0D99-657C-B6460001A465";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 1 2 1 3 1 4 1 5 1 6 1 7 1 8 1 9 1 10 1
		 11 1 12 1 13 1 14 1 15 1 16 1 17 0.86999999999999988 18 1 19 1 20 1 21 1 22 1;
createNode animCurveTU -n "CURVE795";
	rename -uid "5CEB0D80-0000-0D99-657C-B6460001A466";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 1.0000000000000009 2 1.0000000000000009 3 1.0000000000000009 4 1.0000000000000009 5 1.0000000000000009
		 6 1.0000000000000009 7 1.0000000000000009 8 1.0000000000000009 9 1.0000000000000009 10 1.0000000000000009 11 1 12 1 13 1 14 1 15 1 16 1 17 1
		 18 1 19 1 20 1 21 1 22 1;
createNode animCurveTU -n "CURVE796";
	rename -uid "5CEB0D80-0000-0D99-657C-B6460001A467";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 1.0000000000000009 2 1.0000000000000009 3 1.0000000000000009 4 1.0000000000000009 5 1.0000000000000009
		 6 1.0000000000000009 7 1.0000000000000009 8 1.0000000000000009 9 1.0000000000000009 10 1.0000000000000009 11 1 12 1 13 1 14 1 15 1 16 1 17 1
		 18 1 19 1 20 1 21 1 22 1;
createNode animCurveTA -n "CURVE797";
	rename -uid "5CEB0D80-0000-0D99-657C-B6460001A462";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0 12 0 13 0 14 0 15 0 16 0 17 -54.064889138526674 18 0 19 0 20 0 21 0 22 0;
createNode animCurveTA -n "CURVE798";
	rename -uid "5CEB0D80-0000-0D99-657C-B6460001A463";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0 12 0 13 0 14 0 15 0 16 0 17 0 18 0 19 0 20 0 21 0 22 0;
createNode animCurveTA -n "CURVE799";
	rename -uid "5CEB0D80-0000-0D99-657C-B6460001A464";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0 12 0 13 0 14 0 15 0 16 0 17 0 18 0 19 0 20 0 21 0 22 0;
createNode animCurveTL -n "CURVE801";
	rename -uid "5CEB0D80-0000-0D99-657C-B6460001A46A";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
createNode animCurveTL -n "CURVE802";
	rename -uid "5CEB0D80-0000-0D99-657C-B6460001A46B";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 -0.17368561185685394 7 0 8 0 9 0
		 10 0 11 -0.17368561185685394;
createNode animCurveTL -n "CURVE803";
	rename -uid "5CEB0D80-0000-0D99-657C-B6460001A46C";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
createNode animCurveTU -n "CURVE805";
	rename -uid "5CEB0D80-0000-0D99-657C-B6460001A46E";
	setAttr ".tan" 9;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
	setAttr -s 11 ".kot[0:10]"  5 5 5 5 5 5 5 5 
		5 5 5;
createNode animCurveTL -n "CURVE806";
	rename -uid "5CEB0D80-0000-0D99-657C-B6460001A470";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
createNode animCurveTL -n "CURVE807";
	rename -uid "5CEB0D80-0000-0D99-657C-B6460001A471";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
createNode animCurveTL -n "CURVE808";
	rename -uid "5CEB0D80-0000-0D99-657C-B6460001A472";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
createNode animCurveTU -n "CURVE809";
	rename -uid "5CEB0D80-0000-0D99-657C-B6460001A476";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1 2 1 3 1 4 1 5 1 6 1 7 1 8 1 9 1 10 1
		 11 1;
createNode animCurveTU -n "CURVE810";
	rename -uid "5CEB0D80-0000-0D99-657C-B6460001A477";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1 2 1 3 1 4 1 5 1 6 1 7 1 8 1 9 1 10 1
		 11 1;
createNode animCurveTU -n "CURVE811";
	rename -uid "5CEB0D80-0000-0D99-657C-B6460001A478";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1 2 1 3 1 4 1 5 1 6 1 7 1 8 1 9 1 10 1
		 11 1;
createNode animCurveTA -n "CURVE812";
	rename -uid "5CEB0D80-0000-0D99-657C-B6460001A473";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
createNode animCurveTA -n "CURVE813";
	rename -uid "5CEB0D80-0000-0D99-657C-B6460001A474";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
createNode animCurveTA -n "CURVE814";
	rename -uid "5CEB0D80-0000-0D99-657C-B6460001A475";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
createNode animCurveTU -n "CURVE815";
	rename -uid "5CEB0D80-0000-0D99-657C-B6460001A46F";
	setAttr ".tan" 9;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
	setAttr -s 11 ".kot[0:10]"  5 5 5 5 5 5 5 5 
		5 5 5;
createNode animCurveTL -n "CURVE817";
	rename -uid "5CEB0D80-0000-0D99-657C-B6460001A47A";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0.049999999999999989 2 0.14 3 -0.049999999999999989 4 0.010000000000000009 5 -0.049999999999999989
		 6 -0.009999999999999995 7 -0.15000000000000002 8 -0.093578155073438127 9 -0.090519622529315072 10 -0.15051962252931508 11 -0.009999999999999995;
createNode animCurveTL -n "CURVE818";
	rename -uid "5CEB0D80-0000-0D99-657C-B6460001A47B";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 -0.57000000000000006 3 -0.020000000000000018 4 -0.16000000000000003 5 0.14 6 -0.010000000000000009
		 7 0 8 -0.32209998240470916 9 0.04336139063333877 10 0.11336139063333874 11 -0.010000000000000009;
createNode animCurveTL -n "CURVE820";
	rename -uid "5CEB0D80-0000-0D99-657C-B6460001A47D";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
createNode animCurveTL -n "CURVE821";
	rename -uid "5CEB0D80-0000-0D99-657C-B6460001A47E";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
createNode animCurveTL -n "CURVE822";
	rename -uid "5CEB0D80-0000-0D99-657C-B6460001A47F";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
createNode animCurveTL -n "CURVE824";
	rename -uid "5CEB0D80-0000-0D99-657C-B6460001A481";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 -0.09159095007444118 7 0 8 0 9 0
		 10 0 11 -0.09159095007444118;
createNode animCurveTL -n "CURVE825";
	rename -uid "5CEB0D80-0000-0D99-657C-B6460001A482";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 -0.21374567943081502 7 0 8 0 9 0
		 10 0 11 -0.21374567943081502;
createNode animCurveTL -n "CURVE826";
	rename -uid "5CEB0D80-0000-0D99-657C-B6460001A483";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
createNode animCurveTL -n "CURVE828";
	rename -uid "5CEB0D80-0000-0D99-657C-B6460001A485";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
createNode animCurveTL -n "CURVE829";
	rename -uid "5CEB0D80-0000-0D99-657C-B6460001A486";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
createNode animCurveTL -n "CURVE830";
	rename -uid "5CEB0D80-0000-0D99-657C-B6460001A487";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0;
createNode animCurveTU -n "CURVE832";
	rename -uid "5CEB0D80-0000-0D99-657C-B6460001A492";
	setAttr ".tan" 9;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0
		 11 0 12 0 13 0 14 0 15 0 16 0 17 0 18 0 19 0 20 0 21 0 22 0;
	setAttr -s 22 ".kot[0:21]"  5 5 5 5 5 5 5 5 
		5 5 5 5 5 5 5 5 5 5 5 5 5 5;
createNode animCurveTL -n "CURVE833";
	rename -uid "5CEB0D80-0000-0D99-657C-B6460001A48B";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 0.20597038263463877 3 0 4 0 5 0 6 0 7 0 8 0 9 0
		 10 0 11 -0.060698491290020987 12 0 13 0 14 -0.17 15 0 16 0 17 0 18 0 19 0 20 0.020000000000000004 21 -0.16999999999999998 22 -0.17;
createNode animCurveTL -n "CURVE834";
	rename -uid "5CEB0D80-0000-0D99-657C-B6460001A48A";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 -0.21539888610554114 3 0 4 0 5 0 6 0 7 0.1 8 0.1
		 9 0 10 -0.009999999999999995 11 0.26000000000000034 12 0 13 0.41000000000000003 14 -0.06 15 -0.060000000000000012 16 -0.090000000000000011 17 0 18 0 19 -0.0004606966634587772
		 20 -0.11000000000000001 21 -0.060000000000000012 22 0.15000000000000002;
createNode animCurveTL -n "CURVE835";
	rename -uid "5CEB0D80-0000-0D99-657C-B6460001A489";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 -0.036478397425464874 3 0 4 0 5 0 6 0 7 0 8 0 9 0
		 10 0 11 0 12 0 13 0 14 0 15 0 16 0 17 0 18 0 19 0 20 0 21 0 22 0;
createNode animCurveTU -n "CURVE836";
	rename -uid "5CEB0D80-0000-0D99-657C-B6460001A48F";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 1 2 1 3 1 4 1 5 1 6 1 7 1 8 1 9 1 10 1
		 11 1 12 1 13 1 14 1 15 1 16 1 17 1 18 1 19 1 20 1 21 1 22 1;
createNode animCurveTU -n "CURVE837";
	rename -uid "5CEB0D80-0000-0D99-657C-B6460001A490";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 1 2 1 3 1 4 1 5 1 6 1 7 1 8 1 9 1 10 1
		 11 1 12 1 13 1 14 1 15 1 16 1 17 1 18 1 19 1 20 1 21 1 22 1;
createNode animCurveTU -n "CURVE838";
	rename -uid "5CEB0D80-0000-0D99-657C-B6460001A491";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 1 2 1.0000000000000007 3 1.0000000000000007 4 1.0000000000000007 5 1.0000000000000007
		 6 1 7 1.0000000000000007 8 1.0000000000000007 9 1.0000000000000007 10 1.0000000000000007 11 1.0000000000000007 12 1.0000000000000007 13 1.0000000000000007 14 1.0000000000000007
		 15 1.0000000000000007 16 1.0000000000000007 17 1.0000000000000007 18 1.0000000000000007 19 1.0000000000000007 20 1.0000000000000007 21 1.0000000000000007 22 1.0000000000000007;
createNode animCurveTA -n "CURVE839";
	rename -uid "5CEB0D80-0000-0D99-657C-B6460001A48C";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 -17.791091154649134 3 0 4 0 5 0 6 0 7 0 8 0 9 0
		 10 0 11 0 12 0 13 0 14 0 15 0 16 0 17 0 18 0 19 0 20 0 21 0 22 5.9961394406512651;
createNode animCurveTA -n "CURVE840";
	rename -uid "5CEB0D80-0000-0D99-657C-B6460001A48D";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 -15.993736847417619 3 0 4 0 5 0 6 0 7 0 8 0 9 0
		 10 0 11 0 12 0 13 0 14 0 15 0 16 0 17 0 18 0 19 0 20 0 21 0 22 0;
createNode animCurveTA -n "CURVE841";
	rename -uid "5CEB0D80-0000-0D99-657C-B6460001A48E";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0 2 -10.997959995258739 3 0 4 0 5 0 6 0 7 0 8 0 9 0
		 10 -17.417916971977029 11 0 12 0 13 0 14 7.3338597776745376 15 7.3338597776745376 16 0 17 0 18 0 19 0 20 -8.9381416040408439 21 7.3338597776745376
		 22 7.3338597776745376;
// End