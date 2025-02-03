//Maya ASCII 2022 scene
//Name: animation.ma
//Last modified: Fri, Dec 15, 2023 12:13:40 PM
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
fileInfo "UUID" "B7197D80-0000-6BA2-657C-B37400016995";
createNode animCurveTU -n "CURVE1";
	rename -uid "B7197D80-0000-6BA2-657C-B373000166DF";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE2";
	rename -uid "B7197D80-0000-6BA2-657C-B373000166E0";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE3";
	rename -uid "B7197D80-0000-6BA2-657C-B373000166E1";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE4";
	rename -uid "B7197D80-0000-6BA2-657C-B373000166E2";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE5";
	rename -uid "B7197D80-0000-6BA2-657C-B373000166E6";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1.0000000000000002 3 1.0000000000000002 6 1.0000000000000002 8 1.0000000000000002 10 1.0000000000000002
		 13 1.0000000000000002 15 1.0000000000000002 18 1.0000000000000002 20 1.0000000000000002 22 1.0000000000000002 25 1.0000000000000002;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE6";
	rename -uid "B7197D80-0000-6BA2-657C-B373000166E7";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1.0000000000000002 3 1.0000000000000002 6 1.0000000000000002 8 1.0000000000000002 10 1.0000000000000002
		 13 1.0000000000000002 15 1.0000000000000002 18 1.0000000000000002 20 1.0000000000000002 22 1.0000000000000002 25 1.0000000000000002;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE7";
	rename -uid "B7197D80-0000-6BA2-657C-B373000166E8";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1.0000000000000002 3 1.0000000000000002 6 1.0000000000000002 8 1.0000000000000002 10 1.0000000000000002
		 13 1.0000000000000002 15 1.0000000000000002 18 1.0000000000000002 20 1.0000000000000002 22 1.0000000000000002 25 1.0000000000000002;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE8";
	rename -uid "B7197D80-0000-6BA2-657C-B373000166E3";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE9";
	rename -uid "B7197D80-0000-6BA2-657C-B373000166E4";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE10";
	rename -uid "B7197D80-0000-6BA2-657C-B373000166E5";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 -5.1421455695746801 3 -5.1421455695746801 6 -5.1421455695746801 8 -5.1421455695746801 10 -5.1421455695746801
		 13 -5.1421455695746801 15 -5.1421455695746801 18 -5.1421455695746801 20 -5.1421455695746801 22 -5.1421455695746801 25 -5.1421455695746801;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE12";
	rename -uid "B7197D80-0000-6BA2-657C-B373000166EA";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 12 ".ktv[0:11]"  1 3 3 3 6 3 8 3 10 3 12.999999829931973 3 13 3 15 3
		 18 3 20 3 22 3 25 3;
	setAttr -s 12 ".kit[11]"  1;
	setAttr -s 12 ".kot[0:11]"  1 18 18 18 18 18 18 18 
		18 18 18 18;
	setAttr -s 12 ".kix[11]"  1;
	setAttr -s 12 ".kiy[11]"  0;
	setAttr -s 12 ".kox[0:11]"  1 1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 12 ".koy[0:11]"  0 0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE13";
	rename -uid "B7197D80-0000-6BA2-657C-B373000166EC";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 12 ".ktv[0:11]"  1 0 3 0 6 0 8 0 10 0 12.999999829931973 0 13 0 15 0
		 18 0 20 0 22 0 25 0;
	setAttr -s 12 ".kit[11]"  1;
	setAttr -s 12 ".kot[0:11]"  1 18 18 18 18 18 18 18 
		18 18 18 18;
	setAttr -s 12 ".kix[11]"  1;
	setAttr -s 12 ".kiy[11]"  0;
	setAttr -s 12 ".kox[0:11]"  1 1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 12 ".koy[0:11]"  0 0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE14";
	rename -uid "B7197D80-0000-6BA2-657C-B373000166ED";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 12 ".ktv[0:11]"  1 0 3 0 6 0 8 0 10 0 12.999999829931973 0 13 0 15 0
		 18 0 20 0 22 0 25 0;
	setAttr -s 12 ".kit[11]"  1;
	setAttr -s 12 ".kot[0:11]"  1 18 18 18 18 18 18 18 
		18 18 18 18;
	setAttr -s 12 ".kix[11]"  1;
	setAttr -s 12 ".kiy[11]"  0;
	setAttr -s 12 ".kox[0:11]"  1 1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 12 ".koy[0:11]"  0 0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE15";
	rename -uid "B7197D80-0000-6BA2-657C-B373000166EE";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 12 ".ktv[0:11]"  1 0 3 0 6 0 8 0 10 0 12.999999829931973 0 13 0 15 0
		 18 0 20 0 22 0 25 0;
	setAttr -s 12 ".kit[11]"  1;
	setAttr -s 12 ".kot[0:11]"  1 18 18 18 18 18 18 18 
		18 18 18 18;
	setAttr -s 12 ".kix[11]"  1;
	setAttr -s 12 ".kiy[11]"  0;
	setAttr -s 12 ".kox[0:11]"  1 1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 12 ".koy[0:11]"  0 0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE16";
	rename -uid "B7197D80-0000-6BA2-657C-B373000166EF";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 12 ".ktv[0:11]"  1 0 3 0 6 0 8 0 10 0 12.999999829931973 0 13 0 15 0
		 18 0 20 0 22 0 25 0;
	setAttr -s 12 ".kit[11]"  1;
	setAttr -s 12 ".kot[0:11]"  1 18 18 18 18 18 18 18 
		18 18 18 18;
	setAttr -s 12 ".kix[11]"  1;
	setAttr -s 12 ".kiy[11]"  0;
	setAttr -s 12 ".kox[0:11]"  1 1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 12 ".koy[0:11]"  0 0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE17";
	rename -uid "B7197D80-0000-6BA2-657C-B373000166F0";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 12 ".ktv[0:11]"  1 -37.608229531745188 3 -37.608229531745188 6 -37.608229531745188 8 -37.608229531745188 10 -37.608229531745188
		 12.999999829931973 -37.608229531745188 13 -37.608229531745188 15 -37.608229531745188 18 -37.608229531745188 20 -37.608229531745188 22 -37.608229531745188 25 -37.608229531745188;
	setAttr -s 12 ".kit[11]"  1;
	setAttr -s 12 ".kot[0:11]"  1 18 18 18 18 18 18 18 
		18 18 18 18;
	setAttr -s 12 ".kix[11]"  1;
	setAttr -s 12 ".kiy[11]"  0;
	setAttr -s 12 ".kox[0:11]"  1 1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 12 ".koy[0:11]"  0 0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE18";
	rename -uid "B7197D80-0000-6BA2-657C-B373000166F1";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 14 ".ktv[0:13]"  1 -11.171031891821766 3 -8.8996876604060802 4 -5.646180133353651 6 3.9921069278295347 7 9.8997382320516287
		 8 13.012660743983346 10 16.753283492878062 12.999999829931973 18.548999999999992 13 18.549269962179174 15 14.665687035957037 18 -0.51450427907132945 20 -6.0674002632788024 22 -8.9428130962911325
		 25 -11.171031891821766;
	setAttr -s 14 ".kit[13]"  1;
	setAttr -s 14 ".kot[0:13]"  1 18 18 18 18 18 18 18 
		18 18 18 18 18 18;
	setAttr -s 14 ".kix[13]"  1;
	setAttr -s 14 ".kiy[13]"  0;
	setAttr -s 14 ".kox[0:13]"  1 0.79178751712982554 0.48563590162916326 0.41842872836703254 0.4678158558814301 0.72249253924373502 0.90717328540395004 
		0.96996719286153676 1 0.53069450422411601 0.49894525271393092 0.74974207156162986 0.91948113430156808 1;
	setAttr -s 14 ".koy[0:13]"  0 0.61079663368210069 0.8741611813898108 0.90824963488963095 0.88382595853817569 0.69137871730126321 0.42075721057327525 
		0.24323578020577127 0 -0.84756317946588489 -0.86663350661870409 -0.6617301762278005 -0.39313412935473013 0;
createNode animCurveTU -n "CURVE19";
	rename -uid "B7197D80-0000-6BA2-657C-B373000166EB";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 12 ".ktv[0:11]"  1 0 3 0 6 0 8 0 10 0 12.999999829931973 0 13 0 15 0
		 18 0 20 0 22 0 25 0;
	setAttr -s 12 ".kit[4:11]"  1 18 18 18 18 18 9 18;
	setAttr -s 12 ".kot[4:11]"  5 18 18 18 18 18 5 18;
	setAttr -s 12 ".kix[4:11]"  0.02777777798473835 1 1 1 1 1 1 1;
	setAttr -s 12 ".kiy[4:11]"  0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE21";
	rename -uid "B7197D80-0000-6BA2-657C-B373000166F8";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 13 ".ktv[0:12]"  1 0 3 0 6 0 8 0 10 0 12 0 13 0 15 0 18 0
		 20 0 22 0 24 0 25 0;
	setAttr -s 13 ".kit[12]"  1;
	setAttr -s 13 ".kot[0:12]"  1 18 18 18 18 18 18 18 
		18 18 18 18 18;
	setAttr -s 13 ".kix[12]"  1;
	setAttr -s 13 ".kiy[12]"  0;
	setAttr -s 13 ".kox[0:12]"  1 1 1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 13 ".koy[0:12]"  0 0 0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE22";
	rename -uid "B7197D80-0000-6BA2-657C-B373000166F6";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 14 ".ktv[0:13]"  1 25.5 3 49.202058087359966 6 0 8 0 10 0 12 0.90864917395458611 13 0
		 13.000000170068027 0 15 0 18 0 20 5.0553935860053958 22 11.847552335066473 24 19.548725193956308 25 25.5;
	setAttr -s 14 ".kit[13]"  1;
	setAttr -s 14 ".kot[0:13]"  1 18 18 18 18 18 18 18 
		18 18 18 18 18 18;
	setAttr -s 14 ".kix[13]"  1;
	setAttr -s 14 ".kiy[13]"  0;
	setAttr -s 14 ".kox[0:13]"  1 1 1 1 1 1 1 1 1 1 0.014066211563838282 0.01149878111625705 0.0091554836193396653 
		1;
	setAttr -s 14 ".koy[0:13]"  0 0 0 0 0 0 0 0 0 0 0.99990106595214767 0.99993388683094464 0.99995808768152672 
		0;
createNode animCurveTU -n "CURVE23";
	rename -uid "B7197D80-0000-6BA2-657C-B373000166FA";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 13 ".ktv[0:12]"  1 0 3 0 6 0 8 0 10 0 12 0 13 0 15 0 18 0
		 20 0 22 0 24 0 25 0;
	setAttr -s 13 ".kit[12]"  1;
	setAttr -s 13 ".kot[0:12]"  1 18 18 18 18 18 18 18 
		18 18 18 18 18;
	setAttr -s 13 ".kix[12]"  1;
	setAttr -s 13 ".kiy[12]"  0;
	setAttr -s 13 ".kox[0:12]"  1 1 1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 13 ".koy[0:12]"  0 0 0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE24";
	rename -uid "B7197D80-0000-6BA2-657C-B373000166F9";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 13 ".ktv[0:12]"  1 0 3 0 6 0 8 0 10 0 12 0 13 0 15 0 18 0
		 20 0 22 0 24 0 25 0;
	setAttr -s 13 ".kit[12]"  1;
	setAttr -s 13 ".kot[0:12]"  1 18 18 18 18 18 18 18 
		18 18 18 18 18;
	setAttr -s 13 ".kix[12]"  1;
	setAttr -s 13 ".kiy[12]"  0;
	setAttr -s 13 ".kox[0:12]"  1 1 1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 13 ".koy[0:12]"  0 0 0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE25";
	rename -uid "B7197D80-0000-6BA2-657C-B373000166FD";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 13 ".ktv[0:12]"  1 0 3 0 6 0 8 0 10 0 12 0 13 0 15 0 18 0
		 20 0 22 0 24 0 25 0;
	setAttr -s 13 ".kit[12]"  1;
	setAttr -s 13 ".kot[0:12]"  1 18 18 18 18 18 18 18 
		18 18 18 18 18;
	setAttr -s 13 ".kix[12]"  1;
	setAttr -s 13 ".kiy[12]"  0;
	setAttr -s 13 ".kox[0:12]"  1 1 1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 13 ".koy[0:12]"  0 0 0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE26";
	rename -uid "B7197D80-0000-6BA2-657C-B373000166F3";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 13 ".ktv[0:12]"  1 0 3 0 6 0 8 0 10 0 12 0 13 0 15 0 18 0
		 20 0 22 0 24 0 25 0;
	setAttr -s 13 ".kit[12]"  1;
	setAttr -s 13 ".kot[0:12]"  1 18 18 18 18 18 18 18 
		18 18 18 18 18;
	setAttr -s 13 ".kix[12]"  1;
	setAttr -s 13 ".kiy[12]"  0;
	setAttr -s 13 ".kox[0:12]"  1 1 1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 13 ".koy[0:12]"  0 0 0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE27";
	rename -uid "B7197D80-0000-6BA2-657C-B3730001670B";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 13 ".ktv[0:12]"  1 1.0000000000000002 3 1.0000000000000002 6 1.0000000000000002 8 1.0000000000000002 10 1.0000000000000002
		 12 1.0000000000000002 13 1.0000000000000002 15 1.0000000000000002 18 1.0000000000000002 20 1.0000000000000002 22 1.0000000000000002 24 1.0000000000000002 25 1.0000000000000002;
	setAttr -s 13 ".kit[12]"  1;
	setAttr -s 13 ".kot[0:12]"  1 18 18 18 18 18 18 18 
		18 18 18 18 18;
	setAttr -s 13 ".kix[12]"  1;
	setAttr -s 13 ".kiy[12]"  0;
	setAttr -s 13 ".kox[0:12]"  1 1 1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 13 ".koy[0:12]"  0 0 0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE28";
	rename -uid "B7197D80-0000-6BA2-657C-B3730001670C";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 13 ".ktv[0:12]"  1 1 3 1 6 1 8 1 10 1 12 1 13 1 15 1 18 1
		 20 1 22 1 24 1 25 1;
	setAttr -s 13 ".kit[12]"  1;
	setAttr -s 13 ".kot[0:12]"  1 18 18 18 18 18 18 18 
		18 18 18 18 18;
	setAttr -s 13 ".kix[12]"  1;
	setAttr -s 13 ".kiy[12]"  0;
	setAttr -s 13 ".kox[0:12]"  1 1 1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 13 ".koy[0:12]"  0 0 0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE29";
	rename -uid "B7197D80-0000-6BA2-657C-B3730001670D";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 13 ".ktv[0:12]"  1 1.0000000000000002 3 1.0000000000000002 6 1.0000000000000002 8 1.0000000000000002 10 1.0000000000000002
		 12 1.0000000000000002 13 1.0000000000000002 15 1.0000000000000002 18 1.0000000000000002 20 1.0000000000000002 22 1.0000000000000002 24 1.0000000000000002 25 1.0000000000000002;
	setAttr -s 13 ".kit[12]"  1;
	setAttr -s 13 ".kot[0:12]"  1 18 18 18 18 18 18 18 
		18 18 18 18 18;
	setAttr -s 13 ".kix[12]"  1;
	setAttr -s 13 ".kiy[12]"  0;
	setAttr -s 13 ".kox[0:12]"  1 1 1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 13 ".koy[0:12]"  0 0 0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE30";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016708";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 13 ".ktv[0:12]"  1 0 3 0 6 0 8 0 10 0 12 0 13 0 15 0 18 0
		 20 0 22 0 24 0 25 0;
	setAttr -s 13 ".kit[12]"  1;
	setAttr -s 13 ".kot[0:12]"  1 18 18 18 18 18 18 18 
		18 18 18 18 18;
	setAttr -s 13 ".kix[12]"  1;
	setAttr -s 13 ".kiy[12]"  0;
	setAttr -s 13 ".kox[0:12]"  1 1 1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 13 ".koy[0:12]"  0 0 0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE31";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016709";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 13 ".ktv[0:12]"  1 0 3 0 6 0 8 0 10 0 12 0 13 0 15 0 18 0
		 20 0 22 0 24 0 25 0;
	setAttr -s 13 ".kit[12]"  1;
	setAttr -s 13 ".kot[0:12]"  1 18 18 18 18 18 18 18 
		18 18 18 18 18;
	setAttr -s 13 ".kix[12]"  1;
	setAttr -s 13 ".kiy[12]"  0;
	setAttr -s 13 ".kox[0:12]"  1 1 1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 13 ".koy[0:12]"  0 0 0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE32";
	rename -uid "B7197D80-0000-6BA2-657C-B3730001670A";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 13 ".ktv[0:12]"  1 0 3 0 6 0 8 0 10 0 12 0 13 0 15 0 18 0
		 20 0 22 0 24 0 25 0;
	setAttr -s 13 ".kit[12]"  1;
	setAttr -s 13 ".kot[0:12]"  1 18 18 18 18 18 18 18 
		18 18 18 18 18;
	setAttr -s 13 ".kix[12]"  1;
	setAttr -s 13 ".kiy[12]"  0;
	setAttr -s 13 ".kox[0:12]"  1 1 1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 13 ".koy[0:12]"  0 0 0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE33";
	rename -uid "B7197D80-0000-6BA2-657C-B373000166F4";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 13 ".ktv[0:12]"  1 45 3 45 6 45 8 45 10 45 12 45 13 45 15 45
		 18 45 20 45 22 45 24 45 25 45;
	setAttr -s 13 ".kit[12]"  1;
	setAttr -s 13 ".kot[0:12]"  1 18 18 18 18 18 18 18 
		18 18 18 18 18;
	setAttr -s 13 ".kix[12]"  1;
	setAttr -s 13 ".kiy[12]"  0;
	setAttr -s 13 ".kox[0:12]"  1 1 1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 13 ".koy[0:12]"  0 0 0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE34";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016700";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 13 ".ktv[0:12]"  1 0 3 0 6 0 8 0 10 0 12 0 13 0 15 0 18 0
		 20 0 22 0 24 0 25 0;
	setAttr -s 13 ".kit[12]"  1;
	setAttr -s 13 ".kot[0:12]"  1 18 18 18 18 18 18 18 
		18 18 18 18 18;
	setAttr -s 13 ".kix[12]"  1;
	setAttr -s 13 ".kiy[12]"  0;
	setAttr -s 13 ".kox[0:12]"  1 1 1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 13 ".koy[0:12]"  0 0 0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE35";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016705";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 13 ".ktv[0:12]"  1 -3.9611037234042552 3 -3.9611037234042552 6 -3.9611037234042552 8 -3.9611037234042552 10 -3.9611037234042552
		 12 -3.9611037234042552 13 -3.9611037234042552 15 -3.9611037234042552 18 -3.9611037234042552 20 -3.9611037234042552 22 -3.9611037234042552 24 -3.9611037234042552 25 -3.9611037234042552;
	setAttr -s 13 ".kit[12]"  1;
	setAttr -s 13 ".kot[0:12]"  1 18 18 18 18 18 18 18 
		18 18 18 18 18;
	setAttr -s 13 ".kix[12]"  1;
	setAttr -s 13 ".kiy[12]"  0;
	setAttr -s 13 ".kox[0:12]"  1 1 1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 13 ".koy[0:12]"  0 0 0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE36";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016706";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 14 ".ktv[0:13]"  1 -0.33631908556432782 3 3.5630800421865256 6 26.880096110186852 8 12.19384740163329 10 3.41764697949659
		 12 0.45695639303020297 13 -0.33631908556432782 15 -0.33631908556432782 15.000000170068027 -0.33631908556432782 17 -0.33631908556432782 20 -0.33631908556432782 22 -0.33631908556432782 24 -0.33631908556432782
		 25 -0.33631908556432782;
	setAttr -s 14 ".kit[13]"  1;
	setAttr -s 14 ".kot[0:13]"  1 18 18 18 18 18 18 18 
		18 18 18 18 18 18;
	setAttr -s 14 ".kix[13]"  1;
	setAttr -s 14 ".kiy[13]"  0;
	setAttr -s 14 ".kox[0:13]"  1 0.0076544698677573067 1 0.0071033701922140272 0.014198808286163154 0.033279672117954247 1 1 1 1 
		1 1 1 1;
	setAttr -s 14 ".koy[0:13]"  0 0.99997070411639744 0 -0.99997477074769858 -0.99989919184048381 -0.99944607829723431 0 0 0 0 
		0 0 0 0;
createNode animCurveTL -n "CURVE37";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016707";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 13 ".ktv[0:12]"  1 -34.711331349843725 3 -46.645403666604373 4 -49.410843550997441 5 -44.684102621560989 6 -31.099248719040389
		 8 5.7256823731851458 10 32.997175028526485 12 39.777488554075717 12.999999829931973 36.893102550718353 13 36.893102550718105 15 24.95903023395746 24 -28.744295191463912 25 -34.711331349843725;
	setAttr -s 13 ".kit[12]"  1;
	setAttr -s 13 ".kot[0:12]"  1 18 18 18 18 18 18 18 
		18 18 18 18 18;
	setAttr -s 13 ".kix[12]"  1;
	setAttr -s 13 ".kiy[12]"  0;
	setAttr -s 13 ".kox[0:12]"  1 0.0085033760981317996 1 0.0045508035310266705 0.0024796696854554679 0.0026002402861763228 0.0048944443496054544 
		1 0.99999999445749432 0.99999999445749421 0.0069826375729593292 0.0069826375729594055 1;
	setAttr -s 13 ".koy[0:12]"  0 -0.99996384564389806 0 0.99998964503999843 0.99999692561439957 0.9999966193695129 0.99998802213551963 
		0 -0.00010528538037680043 -0.00010528538037680043 -0.99997562108909677 -0.99997562108909654 0;
createNode animCurveTU -n "CURVE38";
	rename -uid "B7197D80-0000-6BA2-657C-B373000166F7";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 14 ".ktv[0:13]"  1 0 3 9.256077348066281 6 59.100000000000009 8 26.827696793004169 10 -8.9616887140989228
		 12 -27.7659485584274 13 -16.264052943330874 14 0 15 0 18 0 20 0 22 0 24 0 25 0;
	setAttr -s 14 ".kit[13]"  1;
	setAttr -s 14 ".kot[0:13]"  1 18 18 18 18 18 18 18 
		18 18 18 18 18 18;
	setAttr -s 14 ".kix[13]"  1;
	setAttr -s 14 ".kiy[13]"  0;
	setAttr -s 14 ".kox[0:13]"  1 0.0035250768009640167 1 0.002448751568115381 0.0030528441348295268 1 0.003001264582800756 1 1 1 
		1 1 1 1;
	setAttr -s 14 ".koy[0:13]"  0 0.9999937868974722 0 -0.99999700180338424 -0.99999534006048674 0 0.99999549619530992 0 0 0 
		0 0 0 0;
createNode animCurveTU -n "CURVE39";
	rename -uid "B7197D80-0000-6BA2-657C-B373000166FC";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 13 ".ktv[0:12]"  1 0 3 0 6 0 8 0 10 0 12 0 13 0 15 0 18 0
		 20 0 22 0 24 0 25 0;
	setAttr -s 13 ".kit[12]"  1;
	setAttr -s 13 ".kot[0:12]"  1 18 18 18 18 18 18 18 
		18 18 18 18 18;
	setAttr -s 13 ".kix[12]"  1;
	setAttr -s 13 ".kiy[12]"  0;
	setAttr -s 13 ".kox[0:12]"  1 1 1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 13 ".koy[0:12]"  0 0 0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE40";
	rename -uid "B7197D80-0000-6BA2-657C-B373000166FB";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 13 ".ktv[0:12]"  1 0 3 0 6 0 8 0 10 0 12 0 13 0 15 0 18 0
		 20 0 22 0 24 0 25 0;
	setAttr -s 13 ".kit[12]"  1;
	setAttr -s 13 ".kot[0:12]"  1 18 18 18 18 18 18 18 
		18 18 18 18 18;
	setAttr -s 13 ".kix[12]"  1;
	setAttr -s 13 ".kiy[12]"  0;
	setAttr -s 13 ".kox[0:12]"  1 1 1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 13 ".koy[0:12]"  0 0 0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE41";
	rename -uid "B7197D80-0000-6BA2-657C-B373000166FE";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 13 ".ktv[0:12]"  1 0 3 0 6 0 8 0 10 0 12 0 13 0 15 0 18 0
		 20 0 22 0 24 0 25 0;
	setAttr -s 13 ".kit[12]"  1;
	setAttr -s 13 ".kot[0:12]"  1 18 18 18 18 18 18 18 
		18 18 18 18 18;
	setAttr -s 13 ".kix[12]"  1;
	setAttr -s 13 ".kiy[12]"  0;
	setAttr -s 13 ".kox[0:12]"  1 1 1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 13 ".koy[0:12]"  0 0 0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE42";
	rename -uid "B7197D80-0000-6BA2-657C-B373000166FF";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 13 ".ktv[0:12]"  1 0 3 0 6 0 8 0 10 0 12 0 13 0 15 0 18 0
		 20 0 22 0 24 0 25 0;
	setAttr -s 13 ".kit[12]"  1;
	setAttr -s 13 ".kot[0:12]"  1 18 18 18 18 18 18 18 
		18 18 18 18 18;
	setAttr -s 13 ".kix[12]"  1;
	setAttr -s 13 ".kiy[12]"  0;
	setAttr -s 13 ".kox[0:12]"  1 1 1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 13 ".koy[0:12]"  0 0 0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE43";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016701";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 13 ".ktv[0:12]"  1 0 3 0 6 0 8 0 10 0 12 0 13 0 15 0 18 0
		 20 0 22 0 24 0 25 0;
	setAttr -s 13 ".kit[12]"  1;
	setAttr -s 13 ".kot[0:12]"  1 18 18 18 18 18 18 18 
		18 18 18 18 18;
	setAttr -s 13 ".kix[12]"  1;
	setAttr -s 13 ".kiy[12]"  0;
	setAttr -s 13 ".kox[0:12]"  1 1 1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 13 ".koy[0:12]"  0 0 0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE44";
	rename -uid "B7197D80-0000-6BA2-657C-B373000166F5";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 13 ".ktv[0:12]"  1 90 3 90 6 90 8 90 10 90 12 90 13 90 15 90
		 18 90 20 90 22 90 24 90 25 90;
	setAttr -s 13 ".kit[12]"  1;
	setAttr -s 13 ".kot[0:12]"  1 18 18 18 18 18 18 18 
		18 18 18 18 18;
	setAttr -s 13 ".kix[12]"  1;
	setAttr -s 13 ".kiy[12]"  0;
	setAttr -s 13 ".kox[0:12]"  1 1 1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 13 ".koy[0:12]"  0 0 0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE45";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016704";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 13 ".ktv[0:12]"  1 0 3 0 6 0 8 0 10 0 12 0 13 0 15 0 18 0
		 20 0 22 0 24 0 25 0;
	setAttr -s 13 ".kit[1:12]"  9 18 18 9 9 18 1 18 
		18 1 9 1;
	setAttr -s 13 ".kot[1:12]"  5 18 18 5 5 18 5 18 
		18 5 5 1;
	setAttr -s 13 ".kix[7:12]"  0.02777777798473835 1 1 0.02777777798473835 1 0.013888888992369175;
	setAttr -s 13 ".kiy[7:12]"  0 0 0 0 0 0;
	setAttr -s 13 ".kox[12]"  0.013888888992369175;
	setAttr -s 13 ".koy[12]"  0;
createNode animCurveTU -n "CURVE46";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016703";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 13 ".ktv[0:12]"  1 1 3 1 6 1 8 1 10 1 12 1 13 1 15 1 18 1
		 20 1 22 1 24 1 25 1;
	setAttr -s 13 ".kit[12]"  1;
	setAttr -s 13 ".kot[0:12]"  1 18 18 18 18 18 18 18 
		18 18 18 18 18;
	setAttr -s 13 ".kix[12]"  1;
	setAttr -s 13 ".kiy[12]"  0;
	setAttr -s 13 ".kox[0:12]"  1 1 1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 13 ".koy[0:12]"  0 0 0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE47";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016702";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 13 ".ktv[0:12]"  1 0 3 0 6 0 8 0 10 0 12 0 13 0 15 0 18 0
		 20 0 22 0 24 0 25 0;
	setAttr -s 13 ".kit[12]"  1;
	setAttr -s 13 ".kot[0:12]"  1 18 18 18 18 18 18 18 
		18 18 18 18 18;
	setAttr -s 13 ".kix[12]"  1;
	setAttr -s 13 ".kiy[12]"  0;
	setAttr -s 13 ".kox[0:12]"  1 1 1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 13 ".koy[0:12]"  0 0 0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE49";
	rename -uid "B7197D80-0000-6BA2-657C-B3730001670F";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE50";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016710";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE51";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016711";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE52";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016712";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE53";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016716";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1.0000000000000002 3 1.0000000000000002 6 1.0000000000000002 8 1.0000000000000002 10 1.0000000000000002
		 13 1.0000000000000002 15 1.0000000000000002 18 1.0000000000000002 20 1.0000000000000002 22 1.0000000000000002 25 1.0000000000000002;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE54";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016717";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1 3 1 6 1 8 1 10 1 13 1 15 1 18 1 20 1
		 22 1 25 1;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE55";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016718";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1 3 1 6 1 8 1 10 1 13 1 15 1 18 1 20 1
		 22 1 25 1;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE56";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016713";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE57";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016714";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 9.565175890006417 3 9.565175890006417 6 9.565175890006417 8 9.565175890006417 10 9.565175890006417
		 13 9.565175890006417 15 9.565175890006417 18 9.565175890006417 20 9.565175890006417 22 9.565175890006417 25 9.565175890006417;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE58";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016715";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE60";
	rename -uid "B7197D80-0000-6BA2-657C-B3730001671A";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE61";
	rename -uid "B7197D80-0000-6BA2-657C-B3730001671B";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE62";
	rename -uid "B7197D80-0000-6BA2-657C-B3730001671C";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE63";
	rename -uid "B7197D80-0000-6BA2-657C-B3730001671D";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE64";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016721";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0.99999999999999956 3 0.99999999999999956 6 0.99999999999999956 8 0.99999999999999956 10 0.99999999999999956
		 13 0.99999999999999956 15 0.99999999999999956 18 0.99999999999999956 20 0.99999999999999956 22 0.99999999999999956 25 0.99999999999999956;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE65";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016722";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1 3 1 6 1 8 1 10 1 13 1 15 1 18 1 20 1
		 22 1 25 1;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE66";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016723";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1 3 1 6 1 8 1 10 1 13 1 15 1 18 1 20 1
		 22 1 25 1;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE67";
	rename -uid "B7197D80-0000-6BA2-657C-B3730001671E";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE68";
	rename -uid "B7197D80-0000-6BA2-657C-B3730001671F";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE69";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016720";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 -16.004111880308876 3 -16.004111880308876 6 -16.004111880308876 8 -16.004111880308876 10 -16.004111880308876
		 13 -16.004111880308876 15 -16.004111880308876 18 -16.004111880308876 20 -16.004111880308876 22 -16.004111880308876 25 -16.004111880308876;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE71";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016725";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 12 ".ktv[0:11]"  1 0 3 0 6 0 8 0 10 0 12.999999829931973 0 13 0 15 0
		 18 0 20 0 22 0 25 0;
	setAttr -s 12 ".kit[11]"  1;
	setAttr -s 12 ".kot[0:11]"  1 18 18 18 18 18 18 18 
		18 18 18 18;
	setAttr -s 12 ".kix[11]"  1;
	setAttr -s 12 ".kiy[11]"  0;
	setAttr -s 12 ".kox[0:11]"  1 1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 12 ".koy[0:11]"  0 0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE72";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016726";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 12 ".ktv[0:11]"  1 0 3 0 6 0 8 0 10 0 12.999999829931973 0 13 0 15 0
		 18 0 20 0 22 0 25 0;
	setAttr -s 12 ".kit[11]"  1;
	setAttr -s 12 ".kot[0:11]"  1 18 18 18 18 18 18 18 
		18 18 18 18;
	setAttr -s 12 ".kix[11]"  1;
	setAttr -s 12 ".kiy[11]"  0;
	setAttr -s 12 ".kox[0:11]"  1 1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 12 ".koy[0:11]"  0 0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE73";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016727";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 12 ".ktv[0:11]"  1 0 3 0 6 0 8 0 10 0 12.999999829931973 0 13 0 15 0
		 18 0 20 0 22 0 25 0;
	setAttr -s 12 ".kit[11]"  1;
	setAttr -s 12 ".kot[0:11]"  1 18 18 18 18 18 18 18 
		18 18 18 18;
	setAttr -s 12 ".kix[11]"  1;
	setAttr -s 12 ".kiy[11]"  0;
	setAttr -s 12 ".kox[0:11]"  1 1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 12 ".koy[0:11]"  0 0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE74";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016728";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 12 ".ktv[0:11]"  1 0 3 0 6 0 8 0 10 0 12.999999829931973 0 13 0 15 0
		 18 0 20 0 22 0 25 0;
	setAttr -s 12 ".kit[11]"  1;
	setAttr -s 12 ".kot[0:11]"  1 18 18 18 18 18 18 18 
		18 18 18 18;
	setAttr -s 12 ".kix[11]"  1;
	setAttr -s 12 ".kiy[11]"  0;
	setAttr -s 12 ".kox[0:11]"  1 1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 12 ".koy[0:11]"  0 0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE75";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016729";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 12 ".ktv[0:11]"  1 0 3 0 6 0 8 0 10 0 12.999999829931973 0 13 0 15 0
		 18 0 20 0 22 0 25 0;
	setAttr -s 12 ".kit[11]"  1;
	setAttr -s 12 ".kot[0:11]"  1 18 18 18 18 18 18 18 
		18 18 18 18;
	setAttr -s 12 ".kix[11]"  1;
	setAttr -s 12 ".kiy[11]"  0;
	setAttr -s 12 ".kox[0:11]"  1 1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 12 ".koy[0:11]"  0 0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE76";
	rename -uid "B7197D80-0000-6BA2-657C-B3730001672A";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 12 ".ktv[0:11]"  1 0 3 0 6 0 8 0 10 0 12.999999829931973 0 13 0 15 0
		 18 0 20 0 22 0 25 0;
	setAttr -s 12 ".kit[11]"  1;
	setAttr -s 12 ".kot[0:11]"  1 18 18 18 18 18 18 18 
		18 18 18 18;
	setAttr -s 12 ".kix[11]"  1;
	setAttr -s 12 ".kiy[11]"  0;
	setAttr -s 12 ".kox[0:11]"  1 1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 12 ".koy[0:11]"  0 0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE77";
	rename -uid "B7197D80-0000-6BA2-657C-B3730001672B";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 12 ".ktv[0:11]"  1 -18.380712912870933 3 -21.176494380670352 6 -23.743540134295163 8 -18.150471490102031 10 -14.81968867815015
		 12.999999829931973 -9.6696395251405178 13 -9.6696392331877377 15 -5.0559828573291874 18 5.1566769867447446 20 2.3355936742608812 22 -9.5963427663786565 25 -18.380712912870933;
	setAttr -s 12 ".kit[11]"  1;
	setAttr -s 12 ".kot[0:11]"  1 18 18 18 18 18 18 18 
		18 18 18 18;
	setAttr -s 12 ".kix[11]"  1;
	setAttr -s 12 ".kiy[11]"  0;
	setAttr -s 12 ".kox[0:11]"  1 0.91216876417772208 1 0.730628647892831 0.81519494740001819 0.81188739411218924 0.71912662647103442 
		0.62711283484298941 1 0.54338062391927067 0.49924870507984442 1;
	setAttr -s 12 ".koy[0:11]"  0 -0.40981476993696486 0 0.68277505730532773 0.57918666916071315 0.58381406225074672 0.69487905069903289 
		0.77892842570751608 0 -0.83948644869890787 -0.86645872981700556 0;
createNode animCurveTU -n "CURVE79";
	rename -uid "B7197D80-0000-6BA2-657C-B3730001672D";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0 20 0 25 0;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTL -n "CURVE80";
	rename -uid "B7197D80-0000-6BA2-657C-B3730001672E";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0 20 0 25 0;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTL -n "CURVE81";
	rename -uid "B7197D80-0000-6BA2-657C-B3730001672F";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0 20 0 25 0;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTL -n "CURVE82";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016730";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 3.5527136788005009e-15 20 3.5527136788005009e-15 25 3.5527136788005009e-15;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTU -n "CURVE83";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016734";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0.99999999999999967 20 0.99999999999999967 25 0.99999999999999967;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTU -n "CURVE84";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016735";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 1 20 1 25 1;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTU -n "CURVE85";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016736";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 1 20 1 25 1;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTA -n "CURVE86";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016731";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0 20 0 25 0;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTA -n "CURVE87";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016732";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0 20 0 25 0;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTA -n "CURVE88";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016733";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 -16.004111880308876 20 -16.004111880308876 25 -16.004111880308876;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTU -n "CURVE90";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016738";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE91";
	rename -uid "B7197D80-0000-6BA2-657C-B3730001673C";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE92";
	rename -uid "B7197D80-0000-6BA2-657C-B3730001673D";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE93";
	rename -uid "B7197D80-0000-6BA2-657C-B3730001673E";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE94";
	rename -uid "B7197D80-0000-6BA2-657C-B3730001673F";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1 3 1 6 1 8 1 10 1 13 1 15 1 18 1 20 1
		 22 1 25 1;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE95";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016740";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1 3 1 6 1 8 1 10 1 13 1 15 1 18 1 20 1
		 22 1 25 1;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE96";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016741";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1 3 1 6 1 8 1 10 1 13 1 15 1 18 1 20 1
		 22 1 25 1;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE97";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016739";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 -1.3841759021686419 2 -0.47776970116336731 2.9999998299319728 0.81141814305901716 3 0.81112765504921946
		 4 2.1943266393928065 5 2.6571399508654516 6 2.3378287408094707 7 1.5034521849696394 8 0.29139498690860693 10 -1.2575339566081607 12 -1.6995231976120571 13 -1.412503421175535 14 -0.5344904943906289
		 15 0.81112765504921946 16 2.1466143104122009 17 2.6571399508654516 18 2.3378702704179819 19 1.5035698521937593 20 0.29155418374124104 22 -1.2575339566081607 24 -1.6995231976120571 25 -1.3841759021686419;
	setAttr -s 22 ".kit[21]"  1;
	setAttr -s 22 ".kot[0:21]"  1 18 18 18 18 18 18 18 
		18 18 18 18 18 18 18 18 18 18 18 18 18 18;
	setAttr -s 22 ".kix[21]"  1;
	setAttr -s 22 ".kiy[21]"  0;
	setAttr -s 22 ".kox[0:21]"  1 0.90854419363369032 1 1 0.93271524375197246 1 0.97202708910276403 0.91913416255115199 0.93306677418823292 
		0.9789500862736924 1 0.97149764770681146 0.9065130417302284 0.8719369703114902 0.93271524375197257 1 0.97203255772148278 0.91914236418691064 0.93306162903539025 0.97894682534041899 1 1;
	setAttr -s 22 ".koy[0:21]"  0 0.41778876027785583 0 0 0.36061374637234556 0 -0.23486876772020354 -0.39394465503594833 -0.35970320391395599 
		-0.20409980055044197 0 0.23704919426172297 0.42217781226991224 0.48961813671883081 0.3606137463723455 0 -0.23484613415901082 -0.39392551879371379 -0.35971655010830933 -0.20411544075820198 0 0;
createNode animCurveTA -n "CURVE98";
	rename -uid "B7197D80-0000-6BA2-657C-B3730001673A";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 7 ".ktv[0:6]"  1 11.754110833333334 3 9.2601083333333349 10 -8.197905 13 -11.7543025
		 15 -9.2602966666666671 22 8.1977450000000012 25 11.754110833333334;
	setAttr -s 7 ".kit[6]"  1;
	setAttr -s 7 ".kot[0:6]"  1 18 18 18 18 18 18;
	setAttr -s 7 ".kix[6]"  1;
	setAttr -s 7 ".kiy[6]"  0;
	setAttr -s 7 ".kox[0:6]"  1 0.73277976953723334 0.75062059876416576 1 0.73277923101751541 0.75062065074396855 1;
	setAttr -s 7 ".koy[0:6]"  0 -0.68046587670283598 -0.66073346873828431 0 0.68046645662323346 0.66073340968706973 0;
createNode animCurveTA -n "CURVE99";
	rename -uid "B7197D80-0000-6BA2-657C-B3730001673B";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 5 ".ktv[0:4]"  1 0 6 -7.0119538461538458 13 0 18 7.0123076923076928 25 0;
	setAttr -s 5 ".kit[4]"  1;
	setAttr -s 5 ".kot[0:4]"  1 18 18 18 18;
	setAttr -s 5 ".kix[4]"  1;
	setAttr -s 5 ".kiy[4]"  0;
	setAttr -s 5 ".kox[0:4]"  1 1 0.89815381474866474 1 1;
	setAttr -s 5 ".koy[0:4]"  0 0 0.43968139038674503 0 0;
createNode animCurveTU -n "CURVE101";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016743";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE102";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016745";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE103";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016746";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE104";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016747";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE105";
	rename -uid "B7197D80-0000-6BA2-657C-B3730001674B";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1 3 1 6 1 8 1 10 1 13 1 15 1 18 1 20 1
		 22 1 25 1;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE106";
	rename -uid "B7197D80-0000-6BA2-657C-B3730001674C";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0.99999999999999989 3 0.99999999999999989 6 0.99999999999999989 8 0.99999999999999989 10 0.99999999999999989
		 13 0.99999999999999989 15 0.99999999999999989 18 0.99999999999999989 20 0.99999999999999989 22 0.99999999999999989 25 0.99999999999999989;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE107";
	rename -uid "B7197D80-0000-6BA2-657C-B3730001674D";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0.99999999999999989 3 0.99999999999999989 6 0.99999999999999989 8 0.99999999999999989 10 0.99999999999999989
		 13 0.99999999999999989 15 0.99999999999999989 18 0.99999999999999989 20 0.99999999999999989 22 0.99999999999999989 25 0.99999999999999989;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE108";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016748";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0.83495504376705154 2 0.45426449784903794 2.9999998299319728 -0.087194499014311505 3 -0.087072699006052828
		 4 -0.66801631855761123 5 -0.86239779179140863 6 -0.72828716266094495 7 -0.37784879880254851 8 0.1312151758553303 10 0.78176540014581675 12 0.96740079278416702 13 0.84685238457704215 14 0.47808689947090477
		 15 -0.087072699006052828 16 -0.64797685719329301 17 -0.86239779179140863 18 -0.72830438266211794 19 -0.37789835880592249 20 0.13114839585078375 22 0.78176540014581675 24 0.96740079278416702 25 0.83495504376705154;
	setAttr -s 22 ".kit[21]"  1;
	setAttr -s 22 ".kot[0:21]"  1 18 18 18 18 18 18 18 
		18 18 18 18 18 18 18 18 18 18 18 18 18 18;
	setAttr -s 22 ".kix[21]"  1;
	setAttr -s 22 ".kiy[21]"  0;
	setAttr -s 22 ".kox[0:21]"  1 0.98185557419180758 1 1 0.98707090156975241 1 0.99488996618815639 0.98418096468423777 0.98714436074120104 
		0.99618807940485632 1 0.99478975910945555 0.98140215221519 0.97329809547121582 0.98707090156975241 1 0.99489100345350812 0.98418274586976595 0.98714328296116061 0.99618747399799212 1 1;
	setAttr -s 22 ".koy[0:21]"  0 -0.18963024924435409 0 0 -0.16028423276877884 0 0.10096511862088284 0.17716610497835938 0.15983119550590053 
		0.087231361629081725 0 -0.10194770802206127 -0.19196305797572885 -0.22954480467243049 -0.16028423276877879 0 0.10095489709405757 0.17715620997370513 0.15983785191456465 0.087238275140557625 0 0;
createNode animCurveTA -n "CURVE109";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016749";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE110";
	rename -uid "B7197D80-0000-6BA2-657C-B3730001674A";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE111";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016744";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1 3 1 6 1 8 1 10 1 13 1 15 1 18 1 20 1
		 22 1 25 1;
	setAttr -s 11 ".kit[4:10]"  9 18 18 18 18 1 18;
	setAttr -s 11 ".kot[4:10]"  5 18 18 18 18 5 18;
	setAttr -s 11 ".kix[9:10]"  0.02777777798473835 1;
	setAttr -s 11 ".kiy[9:10]"  0 0;
createNode animCurveTU -n "CURVE113";
	rename -uid "B7197D80-0000-6BA2-657C-B3730001674F";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE114";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016750";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE115";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016751";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE116";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016752";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE117";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016756";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1 3 1 6 1 8 1 10 1 13 1 15 1 18 1 20 1
		 22 1 25 1;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE118";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016757";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0.99999999999999978 3 0.99999999999999978 6 0.99999999999999978 8 0.99999999999999978 10 0.99999999999999978
		 13 0.99999999999999978 15 0.99999999999999978 18 0.99999999999999978 20 0.99999999999999978 22 0.99999999999999978 25 0.99999999999999978;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE119";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016758";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0.99999999999999989 3 0.99999999999999989 6 0.99999999999999989 8 0.99999999999999989 10 0.99999999999999989
		 13 0.99999999999999989 15 0.99999999999999989 18 0.99999999999999989 20 0.99999999999999989 22 0.99999999999999989 25 0.99999999999999989;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE120";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016753";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE121";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016754";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 -2.574738921613474 3 -2.574738921613474 6 -2.574738921613474 8 -2.574738921613474 10 -2.574738921613474
		 13 -2.574738921613474 15 -2.574738921613474 18 -2.574738921613474 20 -2.574738921613474 22 -2.574738921613474 25 -2.574738921613474;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE122";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016755";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE124";
	rename -uid "B7197D80-0000-6BA2-657C-B3730001675A";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE125";
	rename -uid "B7197D80-0000-6BA2-657C-B3730001675B";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE126";
	rename -uid "B7197D80-0000-6BA2-657C-B3730001675C";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE127";
	rename -uid "B7197D80-0000-6BA2-657C-B3730001675D";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE128";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016761";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1.0000000000000002 3 1.0000000000000002 6 1.0000000000000002 8 1.0000000000000002 10 1.0000000000000002
		 13 1.0000000000000002 15 1.0000000000000002 18 1.0000000000000002 20 1.0000000000000002 22 1.0000000000000002 25 1.0000000000000002;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE129";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016762";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1.0000000000000002 3 1.0000000000000002 6 1.0000000000000002 8 1.0000000000000002 10 1.0000000000000002
		 13 1.0000000000000002 15 1.0000000000000002 18 1.0000000000000002 20 1.0000000000000002 22 1.0000000000000002 25 1.0000000000000002;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE130";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016763";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1.0000000000000004 3 1.0000000000000004 6 1.0000000000000004 8 1.0000000000000004 10 1.0000000000000004
		 13 1.0000000000000004 15 1.0000000000000004 18 1.0000000000000004 20 1.0000000000000004 22 1.0000000000000004 25 1.0000000000000004;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE131";
	rename -uid "B7197D80-0000-6BA2-657C-B3730001675E";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE132";
	rename -uid "B7197D80-0000-6BA2-657C-B3730001675F";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE133";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016760";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 -24.183597580285252 3 -24.183597580285252 6 -24.183597580285252 8 -24.183597580285252 10 -24.183597580285252
		 13 -24.183597580285252 15 -24.183597580285252 18 -24.183597580285252 20 -24.183597580285252 22 -24.183597580285252 25 -24.183597580285252;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE135";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016765";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0 13 0 25 0;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTL -n "CURVE136";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016767";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 19 ".ktv[0:18]"  1 0 2 1.6011592009422193 3 1.1732534802508487 4 0.28813300258538427 5 -0.22253157008110752
		 6 0 8 0 9 -0.16864269047186345 10 -0.084321345235931724 11 0.98829199735743223 12 1.1605653525823956 12.999999829931973 0.45078022929093031 13 0.45078022929086853 14 0 15 0.39712212807965575
		 17 0 20 0 24 0 25 0;
	setAttr -s 19 ".kit[18]"  1;
	setAttr -s 19 ".kot[0:18]"  1 18 18 18 18 18 18 18 
		18 18 18 18 18 18 18 18 18 18 18;
	setAttr -s 19 ".kix[18]"  1;
	setAttr -s 19 ".kiy[18]"  0;
	setAttr -s 19 ".kox[0:18]"  1 1 0.063339181615325979 0.059597434248727321 1 1 1 1 0.16252386276348571 0.080360484933234264 
		1 0.99999999965790998 0.99999999965790998 1 1 1 1 1 1;
	setAttr -s 19 ".koy[0:18]"  0 0 -0.99799205812085534 -0.99822249315018374 0 0 0 0 0.98670461336330839 0.99676586642064302 
		0 -2.615683682338778e-05 -2.6156836823387777e-05 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE137";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016766";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 23 ".ktv[0:22]"  1 1.7683662182556583 2 -1.942088624456346 3 -1.0820322175046384 4 0.37505662640867354 5 0.54676043120328655
		 6 0 8 -0.38491431180819946 9 -0.9899207788411053 10 2.1374413178449503 11 7.2904117321438742 12 5.6046804293273409 12.999999829931973 4.9040857040112442 13 4.9040857040112176 14 -0.40686592116282611
		 15 -2.1893205428798845 16 -1.8604807621657491 17 -0.91524903313619976 18 1.4086724044673353 19 1.7493228333280919 20 2.6730049926483108 22 2.2377101397927706 24 3.6566032299909668 25 1.7683662182556583;
	setAttr -s 23 ".kit[22]"  1;
	setAttr -s 23 ".kot[0:22]"  1 18 18 18 18 18 18 18 
		18 18 18 18 18 18 18 18 18 18 18 18 18 18 18;
	setAttr -s 23 ".kix[22]"  1;
	setAttr -s 23 ".kiy[22]"  0;
	setAttr -s 23 ".kox[0:22]"  1 1 0.035940558360756464 0.080625314920488869 1 0.13297550088185164 0.1252779148260387 1 0.010063498460465224 
		1 0.034899908753238083 0.99999999993637434 0.99999999993637423 0.01174718892203497 1 0.065267646958824713 0.02548252347571292 0.040737830134319135 0.065768225322010238 1 1 1 1;
	setAttr -s 23 ".koy[0:22]"  0 0 0.99935392942876689 0.99674448009205063 0 -0.99111932488738241 -0.992121688129455 0 0.99994936171725013 
		0 -0.99939081262988194 -1.1280576530747829e-05 -1.1280576530747827e-05 -0.99993099939567343 0 0.99786779397897107 0.99967526777314519 0.9991698700400985 0.99783492649736072 0 0 0 0;
createNode animCurveTL -n "CURVE138";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016768";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0 13 0 25 0;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTU -n "CURVE139";
	rename -uid "B7197D80-0000-6BA2-657C-B3730001676C";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 1 13 1 25 1;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTU -n "CURVE140";
	rename -uid "B7197D80-0000-6BA2-657C-B3730001676D";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 1 13 1 25 1;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTU -n "CURVE141";
	rename -uid "B7197D80-0000-6BA2-657C-B3730001676E";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 1 13 1 25 1;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTA -n "CURVE142";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016769";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0 13 0 25 0;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTA -n "CURVE143";
	rename -uid "B7197D80-0000-6BA2-657C-B3730001676A";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0 13 0 25 0;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTA -n "CURVE144";
	rename -uid "B7197D80-0000-6BA2-657C-B3730001676B";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0 13 0 25 0;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTU -n "CURVE146";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016770";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE147";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016771";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE148";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016772";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE149";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016773";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE150";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016777";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0.99999999999999978 3 0.99999999999999978 6 0.99999999999999978 8 0.99999999999999978 10 0.99999999999999978
		 13 0.99999999999999978 15 0.99999999999999978 18 0.99999999999999978 20 0.99999999999999978 22 0.99999999999999978 25 0.99999999999999978;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE151";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016778";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1.0000000000000007 3 1.0000000000000007 6 1.0000000000000007 8 1.0000000000000007 10 1.0000000000000007
		 13 1.0000000000000007 15 1.0000000000000007 18 1.0000000000000007 20 1.0000000000000007 22 1.0000000000000007 25 1.0000000000000007;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE152";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016779";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1.0000000000000007 3 1.0000000000000007 6 1.0000000000000007 8 1.0000000000000007 10 1.0000000000000007
		 13 1.0000000000000007 15 1.0000000000000007 18 1.0000000000000007 20 1.0000000000000007 22 1.0000000000000007 25 1.0000000000000007;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE153";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016774";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE154";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016775";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE155";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016776";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 -16.004111880308876 3 -16.004111880308876 6 -16.004111880308876 8 -16.004111880308876 10 -16.004111880308876
		 13 -16.004111880308876 15 -16.004111880308876 18 -16.004111880308876 20 -16.004111880308876 22 -16.004111880308876 25 -16.004111880308876;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE157";
	rename -uid "B7197D80-0000-6BA2-657C-B3730001677B";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE158";
	rename -uid "B7197D80-0000-6BA2-657C-B3730001677C";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE159";
	rename -uid "B7197D80-0000-6BA2-657C-B3730001677D";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE160";
	rename -uid "B7197D80-0000-6BA2-657C-B3730001677E";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE161";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016782";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1 3 1 6 1 8 1 10 1 13 1 15 1 18 1 20 1
		 22 1 25 1;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE162";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016783";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1 3 1 6 1 8 1 10 1 13 1 15 1 18 1 20 1
		 22 1 25 1;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE163";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016784";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1 3 1 6 1 8 1 10 1 13 1 15 1 18 1 20 1
		 22 1 25 1;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE164";
	rename -uid "B7197D80-0000-6BA2-657C-B3730001677F";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE165";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016780";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1.7349117590792646 3 1.7349117590792646 6 1.7349117590792646 8 1.7349117590792646 10 1.7349117590792646
		 13 1.7349117590792646 15 1.7349117590792646 18 1.7349117590792646 20 1.7349117590792646 22 1.7349117590792646 25 1.7349117590792646;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE166";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016781";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE168";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016786";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE169";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016787";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE170";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016788";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE171";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016789";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE172";
	rename -uid "B7197D80-0000-6BA2-657C-B3730001678D";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1 3 1 6 1 8 1 10 1 13 1 15 1 18 1 20 1
		 22 1 25 1;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE173";
	rename -uid "B7197D80-0000-6BA2-657C-B3730001678E";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1.0000000000000002 3 1.0000000000000002 6 1.0000000000000002 8 1.0000000000000002 10 1.0000000000000002
		 13 1.0000000000000002 15 1.0000000000000002 18 1.0000000000000002 20 1.0000000000000002 22 1.0000000000000002 25 1.0000000000000002;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE174";
	rename -uid "B7197D80-0000-6BA2-657C-B3730001678F";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1 3 1 6 1 8 1 10 1 13 1 15 1 18 1 20 1
		 22 1 25 1;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE175";
	rename -uid "B7197D80-0000-6BA2-657C-B3730001678A";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE176";
	rename -uid "B7197D80-0000-6BA2-657C-B3730001678B";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE177";
	rename -uid "B7197D80-0000-6BA2-657C-B3730001678C";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 -16.004111880308876 3 -16.004111880308876 6 -16.004111880308876 8 -16.004111880308876 10 -16.004111880308876
		 13 -16.004111880308876 15 -16.004111880308876 18 -16.004111880308876 20 -16.004111880308876 22 -16.004111880308876 25 -16.004111880308876;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE179";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016791";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0 20 0 25 0;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTL -n "CURVE180";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016792";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 1.4210854715202004e-14 20 1.4210854715202004e-14 25 1.4210854715202004e-14;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTL -n "CURVE181";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016793";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 3.5527136788005009e-15 20 3.5527136788005009e-15 25 3.5527136788005009e-15;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTL -n "CURVE182";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016794";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 1.4210854715202004e-14 20 1.4210854715202004e-14 25 1.4210854715202004e-14;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTU -n "CURVE183";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016798";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0.99999999999999933 20 0.99999999999999933 25 0.99999999999999933;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTU -n "CURVE184";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016799";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0.99999999999999989 20 0.99999999999999989 25 0.99999999999999989;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTU -n "CURVE185";
	rename -uid "B7197D80-0000-6BA2-657C-B3730001679A";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0.99999999999999956 20 0.99999999999999956 25 0.99999999999999956;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTA -n "CURVE186";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016795";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0 20 0 25 0;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTA -n "CURVE187";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016796";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 9.565175890006417 20 9.565175890006417 25 9.565175890006417;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTA -n "CURVE188";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016797";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0 20 0 25 0;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTU -n "CURVE190";
	rename -uid "B7197D80-0000-6BA2-657C-B3730001679C";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0 20 0 25 0;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTL -n "CURVE191";
	rename -uid "B7197D80-0000-6BA2-657C-B3730001679D";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 2.1316282072803006e-14 20 2.1316282072803006e-14 25 2.1316282072803006e-14;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTL -n "CURVE192";
	rename -uid "B7197D80-0000-6BA2-657C-B3730001679E";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0 20 0 25 0;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTL -n "CURVE193";
	rename -uid "B7197D80-0000-6BA2-657C-B3730001679F";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0 20 0 25 0;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTU -n "CURVE194";
	rename -uid "B7197D80-0000-6BA2-657C-B373000167A3";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0.99999999999999967 20 0.99999999999999967 25 0.99999999999999967;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTU -n "CURVE195";
	rename -uid "B7197D80-0000-6BA2-657C-B373000167A4";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 1 20 1 25 1;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTU -n "CURVE196";
	rename -uid "B7197D80-0000-6BA2-657C-B373000167A5";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0.99999999999999978 20 0.99999999999999978 25 0.99999999999999978;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTA -n "CURVE197";
	rename -uid "B7197D80-0000-6BA2-657C-B373000167A0";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0 20 0 25 0;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTA -n "CURVE198";
	rename -uid "B7197D80-0000-6BA2-657C-B373000167A1";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0 20 0 25 0;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTA -n "CURVE199";
	rename -uid "B7197D80-0000-6BA2-657C-B373000167A2";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 -5.1421455695746801 20 -5.1421455695746801 25 -5.1421455695746801;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTU -n "CURVE201";
	rename -uid "B7197D80-0000-6BA2-657C-B373000167A7";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0 20 0 25 0;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTL -n "CURVE202";
	rename -uid "B7197D80-0000-6BA2-657C-B373000167A8";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 7.1054273576010019e-15 20 7.1054273576010019e-15 25 7.1054273576010019e-15;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTL -n "CURVE203";
	rename -uid "B7197D80-0000-6BA2-657C-B373000167A9";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0 20 0 25 0;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTL -n "CURVE204";
	rename -uid "B7197D80-0000-6BA2-657C-B373000167AA";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 -2.6645352591003757e-15 20 -2.6645352591003757e-15 25 -2.6645352591003757e-15;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTU -n "CURVE205";
	rename -uid "B7197D80-0000-6BA2-657C-B373000167AE";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0.999999999999999 20 0.999999999999999 25 0.999999999999999;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTU -n "CURVE206";
	rename -uid "B7197D80-0000-6BA2-657C-B373000167AF";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0.99999999999999878 20 0.99999999999999878 25 0.99999999999999878;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTU -n "CURVE207";
	rename -uid "B7197D80-0000-6BA2-657C-B373000167B0";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 1.0000000000000002 20 1.0000000000000002 25 1.0000000000000002;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTA -n "CURVE208";
	rename -uid "B7197D80-0000-6BA2-657C-B373000167AB";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0 20 0 25 0;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTA -n "CURVE209";
	rename -uid "B7197D80-0000-6BA2-657C-B373000167AC";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0 20 0 25 0;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTA -n "CURVE210";
	rename -uid "B7197D80-0000-6BA2-657C-B373000167AD";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 -16.004111880308876 20 -16.004111880308876 25 -16.004111880308876;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTU -n "CURVE212";
	rename -uid "B7197D80-0000-6BA2-657C-B373000167B2";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE213";
	rename -uid "B7197D80-0000-6BA2-657C-B373000167B3";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE214";
	rename -uid "B7197D80-0000-6BA2-657C-B373000167B4";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE215";
	rename -uid "B7197D80-0000-6BA2-657C-B373000167B5";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE216";
	rename -uid "B7197D80-0000-6BA2-657C-B373000167B9";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1.0000000000000002 3 1.0000000000000002 6 1.0000000000000002 8 1.0000000000000002 10 1.0000000000000002
		 13 1.0000000000000002 15 1.0000000000000002 18 1.0000000000000002 20 1.0000000000000002 22 1.0000000000000002 25 1.0000000000000002;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE217";
	rename -uid "B7197D80-0000-6BA2-657C-B373000167BA";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1.0000000000000011 3 1.0000000000000011 6 1.0000000000000011 8 1.0000000000000011 10 1.0000000000000011
		 13 1.0000000000000011 15 1.0000000000000011 18 1.0000000000000011 20 1.0000000000000011 22 1.0000000000000011 25 1.0000000000000011;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE218";
	rename -uid "B7197D80-0000-6BA2-657C-B373000167BB";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1.0000000000000002 3 1.0000000000000002 6 1.0000000000000002 8 1.0000000000000002 10 1.0000000000000002
		 13 1.0000000000000002 15 1.0000000000000002 18 1.0000000000000002 20 1.0000000000000002 22 1.0000000000000002 25 1.0000000000000002;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE219";
	rename -uid "B7197D80-0000-6BA2-657C-B373000167B6";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE220";
	rename -uid "B7197D80-0000-6BA2-657C-B373000167B7";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE221";
	rename -uid "B7197D80-0000-6BA2-657C-B373000167B8";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 -13.281297366785457 3 -13.281297366785457 6 -13.281297366785457 8 -13.281297366785457 10 -13.281297366785457
		 13 -13.281297366785457 15 -13.281297366785457 18 -13.281297366785457 20 -13.281297366785457 22 -13.281297366785457 25 -13.281297366785457;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE223";
	rename -uid "B7197D80-0000-6BA2-657C-B373000167BD";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE224";
	rename -uid "B7197D80-0000-6BA2-657C-B373000167BE";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE225";
	rename -uid "B7197D80-0000-6BA2-657C-B373000167BF";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE226";
	rename -uid "B7197D80-0000-6BA2-657C-B373000167C0";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE227";
	rename -uid "B7197D80-0000-6BA2-657C-B373000167C4";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1 3 1 6 1 8 1 10 1 13 1 15 1 18 1 20 1
		 22 1 25 1;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE228";
	rename -uid "B7197D80-0000-6BA2-657C-B373000167C5";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1 3 1 6 1 8 1 10 1 13 1 15 1 18 1 20 1
		 22 1 25 1;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE229";
	rename -uid "B7197D80-0000-6BA2-657C-B373000167C6";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1 3 1 6 1 8 1 10 1 13 1 15 1 18 1 20 1
		 22 1 25 1;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE230";
	rename -uid "B7197D80-0000-6BA2-657C-B373000167C1";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE231";
	rename -uid "B7197D80-0000-6BA2-657C-B373000167C2";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 -8.0990838333569179 3 -8.0990838333569179 6 -8.0990838333569179 8 -8.0990838333569179 10 -8.0990838333569179
		 13 -8.0990838333569179 15 -8.0990838333569179 18 -8.0990838333569179 20 -8.0990838333569179 22 -8.0990838333569179 25 -8.0990838333569179;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE232";
	rename -uid "B7197D80-0000-6BA2-657C-B373000167C3";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE234";
	rename -uid "B7197D80-0000-6BA2-657C-B373000167C8";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 3 3 3 6 3 8 3 10 3 13 3 15 3 18 3 20 3
		 22 3 25 3;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE235";
	rename -uid "B7197D80-0000-6BA2-657C-B373000167C9";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE236";
	rename -uid "B7197D80-0000-6BA2-657C-B373000167CA";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE237";
	rename -uid "B7197D80-0000-6BA2-657C-B373000167CB";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE238";
	rename -uid "B7197D80-0000-6BA2-657C-B373000167CC";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0 13 0 25 0;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTA -n "CURVE239";
	rename -uid "B7197D80-0000-6BA2-657C-B373000167CD";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 -40.254616081343258 3 -40.254616081343258 6 -40.254616081343258 8 -40.254616081343258 10 -40.254616081343258
		 13 -40.254616081343258 15 -40.254616081343258 18 -40.254616081343258 20 -40.254616081343258 22 -40.254616081343258 25 -40.254616081343258;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE240";
	rename -uid "B7197D80-0000-6BA2-657C-B373000167CE";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 13 ".ktv[0:12]"  1 18.549269962179174 3 14.665687035957037 6 -0.51450427907132945 8 -6.0674002632788024 10 -8.9428130962911325
		 13 -11.171031891821766 15 -8.8996876604060802 16 -5.646180133353651 18 3.9921069278295347 19 9.8997382320516287 20 13.012660743983346 22 16.753283492878062 25 18.549;
	setAttr -s 13 ".kit[12]"  1;
	setAttr -s 13 ".kot[0:12]"  1 18 18 18 18 18 18 18 
		18 18 18 18 18;
	setAttr -s 13 ".kix[12]"  1;
	setAttr -s 13 ".kiy[12]"  0;
	setAttr -s 13 ".kox[0:12]"  1 0.53069450422411601 0.49894525271393086 0.74974207156162997 0.91948113430156797 1 0.79178751712982554 
		0.48563590162916326 0.41842872836703243 0.46781585588143032 0.72249253924373502 0.90717329086663345 1;
	setAttr -s 13 ".koy[0:12]"  0 -0.84756317946588489 -0.8666335066187042 -0.66173017622780039 -0.39313412935473019 0 0.61079663368210069 
		0.8741611813898108 0.90824963488963095 0.88382595853817547 0.69137871730126321 0.42075719879546014 0;
createNode animCurveTU -n "CURVE242";
	rename -uid "B7197D80-0000-6BA2-657C-B373000167D0";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE243";
	rename -uid "B7197D80-0000-6BA2-657C-B373000167D4";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE244";
	rename -uid "B7197D80-0000-6BA2-657C-B373000167D5";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE245";
	rename -uid "B7197D80-0000-6BA2-657C-B373000167D6";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE246";
	rename -uid "B7197D80-0000-6BA2-657C-B373000167D7";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1 3 1 6 1 8 1 10 1 13 1 15 1 18 1 20 1
		 22 1 25 1;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE247";
	rename -uid "B7197D80-0000-6BA2-657C-B373000167D8";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1 3 1 6 1 8 1 10 1 13 1 15 1 18 1 20 1
		 22 1 25 1;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE248";
	rename -uid "B7197D80-0000-6BA2-657C-B373000167D9";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1 3 1 6 1 8 1 10 1 13 1 15 1 18 1 20 1
		 22 1 25 1;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE249";
	rename -uid "B7197D80-0000-6BA2-657C-B373000167D1";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE250";
	rename -uid "B7197D80-0000-6BA2-657C-B373000167D2";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 7 ".ktv[0:6]"  1 -15.40821076923077 3 -12.138877692307691 10 10.746456923076924 13 15.408461538461538 15 12.139123076923077
		 22 -10.746247692307692 25 -15.40821076923077;
	setAttr -s 7 ".kyts[1:6]" yes yes no yes yes no;
	setAttr -s 7 ".kit[6]"  1;
	setAttr -s 7 ".kot[0:6]"  1 18 18 18 18 18 18;
	setAttr -s 7 ".kix[6]"  1;
	setAttr -s 7 ".kiy[6]"  0;
	setAttr -s 7 ".kox[0:6]"  1 0.63476987054762035 0.65491300479314218 1 0.63476926862529048 0.65491307790072717 1;
	setAttr -s 7 ".koy[0:6]"  0 0.77270124333079548 0.75570427824170605 0 -0.77270173780632445 -0.75570421488476314 0;
createNode animCurveTA -n "CURVE251";
	rename -uid "B7197D80-0000-6BA2-657C-B373000167D3";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 9 ".ktv[0:8]"  1 0 3 1.7091637284640935 6 6.8366549138563739 10 1.7168372520187953 13 0 15 -1.70925
		 18 -6.837 22 -1.7170000000000005 25 0;
	setAttr -s 9 ".kyts[1:8]" yes no no no yes no no no;
	setAttr -s 9 ".kit[8]"  1;
	setAttr -s 9 ".kot[0:8]"  1 18 18 18 18 18 18 18 
		18;
	setAttr -s 9 ".kix[8]"  1;
	setAttr -s 9 ".kiy[8]"  0;
	setAttr -s 9 ".kox[0:8]"  1 0.86775016115412884 1 0.92554255657349482 0.961190907750333 0.86773934194943525 1 0.92553585853340758 
		1;
	setAttr -s 9 ".koy[0:8]"  0 0.49700066178726909 0 -0.37864360019865551 -0.27588410403299934 -0.49701955135905973 0 0.37865997222947656 
		0;
createNode animCurveTU -n "CURVE253";
	rename -uid "B7197D80-0000-6BA2-657C-B373000167DB";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 5 ".ktv[0:4]"  1 0 12 0 13 0 15 0 25 0;
	setAttr -s 5 ".kit[4]"  1;
	setAttr -s 5 ".kot[0:4]"  1 18 18 18 18;
	setAttr -s 5 ".kix[4]"  1;
	setAttr -s 5 ".kiy[4]"  0;
	setAttr -s 5 ".kox[0:4]"  1 1 1 1 1;
	setAttr -s 5 ".koy[0:4]"  0 0 0 0 0;
createNode animCurveTL -n "CURVE254";
	rename -uid "B7197D80-0000-6BA2-657C-B373000167DC";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 5 ".ktv[0:4]"  1 0 12 0 13 0 15 0 25 0;
	setAttr -s 5 ".kit[4]"  1;
	setAttr -s 5 ".kot[0:4]"  1 18 18 18 18;
	setAttr -s 5 ".kix[4]"  1;
	setAttr -s 5 ".kiy[4]"  0;
	setAttr -s 5 ".kox[0:4]"  1 1 1 1 1;
	setAttr -s 5 ".koy[0:4]"  0 0 0 0 0;
createNode animCurveTL -n "CURVE255";
	rename -uid "B7197D80-0000-6BA2-657C-B373000167DD";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 5 ".ktv[0:4]"  1 0 12 0 13 0 15 0 25 0;
	setAttr -s 5 ".kit[4]"  1;
	setAttr -s 5 ".kot[0:4]"  1 18 18 18 18;
	setAttr -s 5 ".kix[4]"  1;
	setAttr -s 5 ".kiy[4]"  0;
	setAttr -s 5 ".kox[0:4]"  1 1 1 1 1;
	setAttr -s 5 ".koy[0:4]"  0 0 0 0 0;
createNode animCurveTL -n "CURVE256";
	rename -uid "B7197D80-0000-6BA2-657C-B373000167DE";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 5 ".ktv[0:4]"  1 0 12 0 13 0 15 0 25 0;
	setAttr -s 5 ".kit[4]"  1;
	setAttr -s 5 ".kot[0:4]"  1 18 18 18 18;
	setAttr -s 5 ".kix[4]"  1;
	setAttr -s 5 ".kiy[4]"  0;
	setAttr -s 5 ".kox[0:4]"  1 1 1 1 1;
	setAttr -s 5 ".koy[0:4]"  0 0 0 0 0;
createNode animCurveTU -n "CURVE257";
	rename -uid "B7197D80-0000-6BA2-657C-B373000167E2";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 5 ".ktv[0:4]"  1 1.0000000000000002 12 1.0000000000000002 13 1.0000000000000002 15 1.0000000000000002 25 1.0000000000000002;
	setAttr -s 5 ".kit[4]"  1;
	setAttr -s 5 ".kot[0:4]"  1 18 18 18 18;
	setAttr -s 5 ".kix[4]"  1;
	setAttr -s 5 ".kiy[4]"  0;
	setAttr -s 5 ".kox[0:4]"  1 1 1 1 1;
	setAttr -s 5 ".koy[0:4]"  0 0 0 0 0;
createNode animCurveTU -n "CURVE258";
	rename -uid "B7197D80-0000-6BA2-657C-B373000167E3";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 5 ".ktv[0:4]"  1 0.99999999999999989 12 0.99999999999999989 13 0.99999999999999989 15 0.99999999999999989 25 0.99999999999999989;
	setAttr -s 5 ".kit[4]"  1;
	setAttr -s 5 ".kot[0:4]"  1 18 18 18 18;
	setAttr -s 5 ".kix[4]"  1;
	setAttr -s 5 ".kiy[4]"  0;
	setAttr -s 5 ".kox[0:4]"  1 1 1 1 1;
	setAttr -s 5 ".koy[0:4]"  0 0 0 0 0;
createNode animCurveTU -n "CURVE259";
	rename -uid "B7197D80-0000-6BA2-657C-B373000167E4";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 5 ".ktv[0:4]"  1 1 12 1 13 1 15 1 25 1;
	setAttr -s 5 ".kit[4]"  1;
	setAttr -s 5 ".kot[0:4]"  1 18 18 18 18;
	setAttr -s 5 ".kix[4]"  1;
	setAttr -s 5 ".kiy[4]"  0;
	setAttr -s 5 ".kox[0:4]"  1 1 1 1 1;
	setAttr -s 5 ".koy[0:4]"  0 0 0 0 0;
createNode animCurveTA -n "CURVE260";
	rename -uid "B7197D80-0000-6BA2-657C-B373000167DF";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 5 ".ktv[0:4]"  1 0 12 0 13 0 15 0 25 0;
	setAttr -s 5 ".kit[4]"  1;
	setAttr -s 5 ".kot[0:4]"  1 18 18 18 18;
	setAttr -s 5 ".kix[4]"  1;
	setAttr -s 5 ".kiy[4]"  0;
	setAttr -s 5 ".kox[0:4]"  1 1 1 1 1;
	setAttr -s 5 ".koy[0:4]"  0 0 0 0 0;
createNode animCurveTA -n "CURVE261";
	rename -uid "B7197D80-0000-6BA2-657C-B373000167E0";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 5 ".ktv[0:4]"  1 0 12 0 13 0 15 0 25 0;
	setAttr -s 5 ".kit[4]"  1;
	setAttr -s 5 ".kot[0:4]"  1 18 18 18 18;
	setAttr -s 5 ".kix[4]"  1;
	setAttr -s 5 ".kiy[4]"  0;
	setAttr -s 5 ".kox[0:4]"  1 1 1 1 1;
	setAttr -s 5 ".koy[0:4]"  0 0 0 0 0;
createNode animCurveTA -n "CURVE262";
	rename -uid "B7197D80-0000-6BA2-657C-B373000167E1";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 6 ".ktv[0:5]"  1 0 12 0 13 5.0200609289598281 14 8.1745851549035962 15 0 25 0;
	setAttr -s 6 ".kit[5]"  1;
	setAttr -s 6 ".kot[0:5]"  1 18 18 18 18 18;
	setAttr -s 6 ".kix[5]"  1;
	setAttr -s 6 ".kiy[5]"  0;
	setAttr -s 6 ".kox[0:5]"  1 1 0.50435488319965371 1 1 1;
	setAttr -s 6 ".koy[0:5]"  0 0 0.86349646889414888 0 0 0;
createNode animCurveTU -n "CURVE264";
	rename -uid "B7197D80-0000-6BA2-657C-B373000167E6";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0 20 0 25 0;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTL -n "CURVE265";
	rename -uid "B7197D80-0000-6BA2-657C-B373000167E7";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0 20 0 25 0;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTL -n "CURVE266";
	rename -uid "B7197D80-0000-6BA2-657C-B373000167E8";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 1.4210854715202004e-14 20 1.4210854715202004e-14 25 1.4210854715202004e-14;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTL -n "CURVE267";
	rename -uid "B7197D80-0000-6BA2-657C-B373000167E9";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 1.7763568394002505e-15 20 1.7763568394002505e-15 25 1.7763568394002505e-15;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTU -n "CURVE268";
	rename -uid "B7197D80-0000-6BA2-657C-B373000167ED";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 1.0000000000000002 20 1.0000000000000002 25 1.0000000000000002;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTU -n "CURVE269";
	rename -uid "B7197D80-0000-6BA2-657C-B373000167EE";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 1.0000000000000002 20 1.0000000000000002 25 1.0000000000000002;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTU -n "CURVE270";
	rename -uid "B7197D80-0000-6BA2-657C-B373000167EF";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 1.0000000000000004 20 1.0000000000000004 25 1.0000000000000004;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTA -n "CURVE271";
	rename -uid "B7197D80-0000-6BA2-657C-B373000167EA";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0 20 0 25 0;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTA -n "CURVE272";
	rename -uid "B7197D80-0000-6BA2-657C-B373000167EB";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0 20 0 25 0;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTA -n "CURVE273";
	rename -uid "B7197D80-0000-6BA2-657C-B373000167EC";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 -19.88365918056531 20 -19.88365918056531 25 -19.88365918056531;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTU -n "CURVE275";
	rename -uid "B7197D80-0000-6BA2-657C-B373000167F1";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0 20 0 25 0;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTL -n "CURVE276";
	rename -uid "B7197D80-0000-6BA2-657C-B373000167F2";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 -1.4210854715202004e-14 20 -1.4210854715202004e-14 25 -1.4210854715202004e-14;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTL -n "CURVE277";
	rename -uid "B7197D80-0000-6BA2-657C-B373000167F3";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0 20 0 25 0;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTL -n "CURVE278";
	rename -uid "B7197D80-0000-6BA2-657C-B373000167F4";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 2.2204460492503131e-16 20 2.2204460492503131e-16 25 2.2204460492503131e-16;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTU -n "CURVE279";
	rename -uid "B7197D80-0000-6BA2-657C-B373000167F8";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 1.0000000000000002 20 1.0000000000000002 25 1.0000000000000002;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTU -n "CURVE280";
	rename -uid "B7197D80-0000-6BA2-657C-B373000167F9";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 1.0000000000000011 20 1.0000000000000011 25 1.0000000000000011;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTU -n "CURVE281";
	rename -uid "B7197D80-0000-6BA2-657C-B373000167FA";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 1.0000000000000002 20 1.0000000000000002 25 1.0000000000000002;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTA -n "CURVE282";
	rename -uid "B7197D80-0000-6BA2-657C-B373000167F5";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0 20 0 25 0;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTA -n "CURVE283";
	rename -uid "B7197D80-0000-6BA2-657C-B373000167F6";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0 20 0 25 0;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTA -n "CURVE284";
	rename -uid "B7197D80-0000-6BA2-657C-B373000167F7";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 -13.281297366785457 20 -13.281297366785457 25 -13.281297366785457;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTU -n "CURVE286";
	rename -uid "B7197D80-0000-6BA2-657C-B373000167FC";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0 20 0 25 0;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTL -n "CURVE287";
	rename -uid "B7197D80-0000-6BA2-657C-B373000167FD";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 -1.4210854715202004e-14 20 -1.4210854715202004e-14 25 -1.4210854715202004e-14;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTL -n "CURVE288";
	rename -uid "B7197D80-0000-6BA2-657C-B373000167FE";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 3.5527136788005009e-15 20 3.5527136788005009e-15 25 3.5527136788005009e-15;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTL -n "CURVE289";
	rename -uid "B7197D80-0000-6BA2-657C-B373000167FF";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0 20 0 25 0;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTU -n "CURVE290";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016803";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0.99999999999999956 20 0.99999999999999956 25 0.99999999999999956;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTU -n "CURVE291";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016804";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0.99999999999999989 20 0.99999999999999989 25 0.99999999999999989;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTU -n "CURVE292";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016805";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0.99999999999999956 20 0.99999999999999956 25 0.99999999999999956;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTA -n "CURVE293";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016800";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0 20 0 25 0;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTA -n "CURVE294";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016801";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0 20 0 25 0;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTA -n "CURVE295";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016802";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 -3.6408012963077039 20 -3.6408012963077039 25 -3.6408012963077039;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTU -n "CURVE297";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016807";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0 20 0 25 0;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTL -n "CURVE298";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016808";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 -1.4210854715202004e-14 20 -1.4210854715202004e-14 25 -1.4210854715202004e-14;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTL -n "CURVE299";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016809";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 3.5527136788005009e-15 20 3.5527136788005009e-15 25 3.5527136788005009e-15;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTL -n "CURVE300";
	rename -uid "B7197D80-0000-6BA2-657C-B3730001680A";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0 20 0 25 0;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTU -n "CURVE301";
	rename -uid "B7197D80-0000-6BA2-657C-B3730001680E";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 1.0000000000000002 20 1.0000000000000002 25 1.0000000000000002;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTU -n "CURVE302";
	rename -uid "B7197D80-0000-6BA2-657C-B3730001680F";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0.99999999999999978 20 0.99999999999999978 25 0.99999999999999978;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTU -n "CURVE303";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016810";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 1 20 1 25 1;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTA -n "CURVE304";
	rename -uid "B7197D80-0000-6BA2-657C-B3730001680B";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0 20 0 25 0;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTA -n "CURVE305";
	rename -uid "B7197D80-0000-6BA2-657C-B3730001680C";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0 20 0 25 0;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTA -n "CURVE306";
	rename -uid "B7197D80-0000-6BA2-657C-B3730001680D";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 -10.753573818184966 20 -10.753573818184966 25 -10.753573818184966;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTU -n "CURVE308";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016812";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE309";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016813";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE310";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016814";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE311";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016815";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE312";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016819";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1.0000000000000002 3 1.0000000000000002 6 1.0000000000000002 8 1.0000000000000002 10 1.0000000000000002
		 13 1.0000000000000002 15 1.0000000000000002 18 1.0000000000000002 20 1.0000000000000002 22 1.0000000000000002 25 1.0000000000000002;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE313";
	rename -uid "B7197D80-0000-6BA2-657C-B3730001681A";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1.0000000000000004 3 1.0000000000000004 6 1.0000000000000004 8 1.0000000000000004 10 1.0000000000000004
		 13 1.0000000000000004 15 1.0000000000000004 18 1.0000000000000004 20 1.0000000000000004 22 1.0000000000000004 25 1.0000000000000004;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE314";
	rename -uid "B7197D80-0000-6BA2-657C-B3730001681B";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1.0000000000000004 3 1.0000000000000004 6 1.0000000000000004 8 1.0000000000000004 10 1.0000000000000004
		 13 1.0000000000000004 15 1.0000000000000004 18 1.0000000000000004 20 1.0000000000000004 22 1.0000000000000004 25 1.0000000000000004;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE315";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016816";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE316";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016817";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE317";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016818";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 -10.753573818184966 3 -10.753573818184966 6 -10.753573818184966 8 -10.753573818184966 10 -10.753573818184966
		 13 -10.753573818184966 15 -10.753573818184966 18 -10.753573818184966 20 -10.753573818184966 22 -10.753573818184966 25 -10.753573818184966;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE319";
	rename -uid "B7197D80-0000-6BA2-657C-B3730001681D";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE320";
	rename -uid "B7197D80-0000-6BA2-657C-B3730001681E";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE321";
	rename -uid "B7197D80-0000-6BA2-657C-B3730001681F";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE322";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016820";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE323";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016824";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0.99999999999999978 3 0.99999999999999978 6 0.99999999999999978 8 0.99999999999999978 10 0.99999999999999978
		 13 0.99999999999999978 15 0.99999999999999978 18 0.99999999999999978 20 0.99999999999999978 22 0.99999999999999978 25 0.99999999999999978;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE324";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016825";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0.99999999999999989 3 0.99999999999999989 6 0.99999999999999989 8 0.99999999999999989 10 0.99999999999999989
		 13 0.99999999999999989 15 0.99999999999999989 18 0.99999999999999989 20 0.99999999999999989 22 0.99999999999999989 25 0.99999999999999989;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE325";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016826";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0.99999999999999989 3 0.99999999999999989 6 0.99999999999999989 8 0.99999999999999989 10 0.99999999999999989
		 13 0.99999999999999989 15 0.99999999999999989 18 0.99999999999999989 20 0.99999999999999989 22 0.99999999999999989 25 0.99999999999999989;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE326";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016821";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE327";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016822";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 9.565175890006417 3 9.565175890006417 6 9.565175890006417 8 9.565175890006417 10 9.565175890006417
		 13 9.565175890006417 15 9.565175890006417 18 9.565175890006417 20 9.565175890006417 22 9.565175890006417 25 9.565175890006417;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE328";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016823";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE330";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016828";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0 20 0 25 0;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTL -n "CURVE331";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016829";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0 20 0 25 0;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTL -n "CURVE332";
	rename -uid "B7197D80-0000-6BA2-657C-B3730001682A";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0 20 0 25 0;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTL -n "CURVE333";
	rename -uid "B7197D80-0000-6BA2-657C-B3730001682B";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 -3.1086244689504383e-15 20 -3.1086244689504383e-15 25 -3.1086244689504383e-15;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTU -n "CURVE334";
	rename -uid "B7197D80-0000-6BA2-657C-B3730001682F";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0.99999999999999978 20 0.99999999999999978 25 0.99999999999999978;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTU -n "CURVE335";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016830";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 1.0000000000000004 20 1.0000000000000004 25 1.0000000000000004;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTU -n "CURVE336";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016831";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 1.0000000000000004 20 1.0000000000000004 25 1.0000000000000004;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTA -n "CURVE337";
	rename -uid "B7197D80-0000-6BA2-657C-B3730001682C";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0 20 0 25 0;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTA -n "CURVE338";
	rename -uid "B7197D80-0000-6BA2-657C-B3730001682D";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0 20 0 25 0;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTA -n "CURVE339";
	rename -uid "B7197D80-0000-6BA2-657C-B3730001682E";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 -16.004111880308876 20 -16.004111880308876 25 -16.004111880308876;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTU -n "CURVE341";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016833";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0 3 0 25 0;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTL -n "CURVE342";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016835";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0 3 0 25 0;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTL -n "CURVE343";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016836";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 21 ".ktv[0:20]"  1 0.086388911854149153 2 0.24625931514139293 3 0.29975135093907335 4 0.26284532184291809 5 0.16640794178197896
		 6 0.026318138728504484 8 -0.15270739809694217 10 -0.20379260606676994 11 -0.17061883087226343 12 -0.069137878873988465 13 0.086388911854149153 14 0.24074471880250042 15 0.29975135093907335 16 0.26285008059476245
		 17 0.16642153821581979 18 0.026336493914189352 20 -0.15270739809694217 22 -0.20379260606676994 23 -0.16734469373987892 24 -0.062582130780246173 25 0.086422544084525793;
	setAttr -s 21 ".kit[20]"  1;
	setAttr -s 21 ".kot[0:20]"  1 18 18 18 18 18 18 18 
		18 18 18 18 18 18 18 18 18 18 18 18 18;
	setAttr -s 21 ".kix[20]"  1;
	setAttr -s 21 ".kiy[20]"  0;
	setAttr -s 21 ".kox[0:20]"  1 0.36380746242607059 1 0.52997014031380663 0.33229935683455808 0.36472518560012701 0.58659003690931932 
		1 0.52624342067518448 0.30843594572866678 0.25969278173337634 0.36380746242607065 1 0.5300090035436037 0.33231635014133992 0.36471171350566006 0.58655934771650831 1 0.50823550749907942 0.31199334932176714 1;
	setAttr -s 21 ".koy[0:20]"  0 0.9314741704862799 0 -0.84801630313087972 -0.9431739698737126 -0.9311152125214972 -0.80988402169614593 
		0 0.85033397097615759 0.95124511424893154 0.96569128561646489 0.93147417048627978 0 -0.84799201420928261 -0.94316798261430534 -0.93112048953492865 -0.80990624865251182 0 0.86121813085719079 0.9500842857236329 0;
createNode animCurveTL -n "CURVE344";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016837";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0 3 0 25 0;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTU -n "CURVE345";
	rename -uid "B7197D80-0000-6BA2-657C-B3730001683B";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 1 3 1 25 1;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTU -n "CURVE346";
	rename -uid "B7197D80-0000-6BA2-657C-B3730001683C";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 1 3 1 25 1;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTU -n "CURVE347";
	rename -uid "B7197D80-0000-6BA2-657C-B3730001683D";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 1 3 1 25 1;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTA -n "CURVE348";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016838";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 -0.90079365387032029 2 -0.68065934372160219 3 -0.047924873961041364 3.9999998299319728 0.85201776338109037
		 4 0.85181498257841604 5 1.817383923922065 6 2.1404597533989542 7 1.9175583555937548 8 1.335105579945894 9 0.48900548962871038 11 -0.59225447161813993 13 -0.90079365387032029 14 -0.70043391907046904
		 15 -0.087519926363867379 16 0.85181498257841604 17 1.7840774051172479 18 2.1404597533989542 19 1.9175873461443398 20 1.3351877198392199 21 0.48911662007262474 23 -0.59225447161813993 25 -0.90079365387032029;
	setAttr -s 22 ".kit[21]"  1;
	setAttr -s 22 ".kot[0:21]"  1 18 18 18 18 18 18 18 
		18 18 18 18 18 18 18 18 18 18 18 18 18 18;
	setAttr -s 22 ".kix[21]"  1;
	setAttr -s 22 ".kiy[21]"  0;
	setAttr -s 22 ".kox[0:21]"  1 0.98441854683834473 0.95214649191017675 1 1 0.96545504309063601 1 0.98607122865843444 0.95803817795292023 
		0.96564497231771607 0.98957447145632049 1 0.98580177641574507 0.95100548081550385 0.93102712118801767 0.96545504309063623 1 0.98607401069495726 0.95804270387131019 0.96564219317066335 0.98957283009552277 1;
	setAttr -s 22 ".koy[0:21]"  0 0.1758411915356628 0.30564204217211954 0 0 0.26056968313842255 0 -0.16632357623634014 -0.28664062793792622 
		-0.25986494076253819 -0.14402210053302197 0 0.16791324431253601 0.30917402131950278 0.36494999604377598 0.26056968313842255 0 -0.16630708172522701 -0.28662550053850616 -0.25987526771232194 -0.14403337785644554 0;
createNode animCurveTA -n "CURVE349";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016839";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 7 ".ktv[0:6]"  1 1.959018 3 1.543351 10 -1.366318 13 -1.959051
		 15 -1.543383 22 1.366291 25 1.959018;
	setAttr -s 7 ".kit[6]"  1;
	setAttr -s 7 ".kot[0:6]"  1 18 18 18 18 18 18;
	setAttr -s 7 ".kix[6]"  1;
	setAttr -s 7 ".kiy[6]"  0;
	setAttr -s 7 ".kox[0:6]"  1 0.98823435902361856 0.98940900312622282 1 0.98823431731179323 0.98940900907832963 1;
	setAttr -s 7 ".koy[0:6]"  0 -0.15294721849441278 -0.14515448505910519 0 0.15294748800583202 0.14515444448806081 0;
createNode animCurveTA -n "CURVE350";
	rename -uid "B7197D80-0000-6BA2-657C-B3730001683A";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0 3 0 25 0;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTU -n "CURVE351";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016834";
	setAttr ".tan" 9;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0 3 0 25 0;
	setAttr -s 3 ".kit[2]"  18;
	setAttr -s 3 ".kot[0:2]"  5 5 18;
createNode animCurveTU -n "CURVE353";
	rename -uid "B7197D80-0000-6BA2-657C-B3730001683F";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE354";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016840";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE355";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016841";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE356";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016842";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE357";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016843";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE358";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016844";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE359";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016845";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 -9.6696392331877377 3 -5.0559828573291874 6 5.1566769867447446 8 2.3355936742608812 10 -9.5963427663786565
		 13 -18.380712912870933 15 -21.176494380670352 18 -23.743540134295163 20 -18.150471490102031 22 -14.81968867815015 25 -9.6696392331877377;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 0.62711283484298941 1 0.54338062391927078 0.49924870507984431 0.71774271017655 0.91216876417772208 
		1 0.73062864789283088 0.81519494728751285 1;
	setAttr -s 11 ".koy[0:10]"  0 0.77892842570751608 0 -0.83948644869890787 -0.86645872981700556 -0.69630841010892652 -0.40981476993696481 
		0 0.68277505730532784 0.5791866693190626 0;
createNode animCurveTU -n "CURVE361";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016847";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE362";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016848";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE363";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016849";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE364";
	rename -uid "B7197D80-0000-6BA2-657C-B3730001684A";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE365";
	rename -uid "B7197D80-0000-6BA2-657C-B3730001684B";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 7 ".ktv[0:6]"  1 31.852191390029503 3 32.81088764043507 6 30.772976564553094 8 29.274554577276618 15 26.858370873464523
		 18 27.508994346479859 25 31.852191390029503;
	setAttr -s 7 ".kit[6]"  1;
	setAttr -s 7 ".kot[0:6]"  1 18 18 18 18 18 18;
	setAttr -s 7 ".kix[6]"  1;
	setAttr -s 7 ".kiy[6]"  0;
	setAttr -s 7 ".kox[0:6]"  1 1 0.95880781446460828 0.98380476841479814 1 0.97881449700351519 1;
	setAttr -s 7 ".koy[0:6]"  0 0 -0.28405558421126204 -0.1792433475594154 0 0.20474906704489693 0;
createNode animCurveTA -n "CURVE366";
	rename -uid "B7197D80-0000-6BA2-657C-B3730001684C";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE367";
	rename -uid "B7197D80-0000-6BA2-657C-B3730001684D";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 8 ".ktv[0:7]"  1 1.5522074829890398 3 8.3844696333566162 6 2.7163630952308191 8 0.51740249432967955 10 0
		 13 -0.51740249432967944 18 -5.2404627173249505 25 1.5522074829890398;
	setAttr -s 8 ".kit[7]"  1;
	setAttr -s 8 ".kot[0:7]"  1 18 18 18 18 18 18 18;
	setAttr -s 8 ".kix[7]"  1;
	setAttr -s 8 ".kiy[7]"  0;
	setAttr -s 8 ".kox[0:7]"  1 1 0.83496627424295 0.96184276914119582 0.99626333039741988 0.9773105208956212 1 1;
	setAttr -s 8 ".koy[0:7]"  0 0 -0.55030111836779572 -0.27360279137975957 -0.08636768206592893 -0.21181158076632509 0 0;
createNode animCurveTU -n "CURVE369";
	rename -uid "B7197D80-0000-6BA2-657C-B3730001684F";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0 13 0 25 0;
	setAttr -s 3 ".kit[1:2]"  1 18;
	setAttr -s 3 ".kot[0:2]"  5 5 18;
	setAttr -s 3 ".kix[1:2]"  1 1;
	setAttr -s 3 ".kiy[1:2]"  0 0;
createNode animCurveTL -n "CURVE370";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016850";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0 13 0 25 0;
	setAttr -s 3 ".kit[1:2]"  1 18;
	setAttr -s 3 ".kot[0:2]"  5 5 18;
	setAttr -s 3 ".kix[1:2]"  1 1;
	setAttr -s 3 ".kiy[1:2]"  0 0;
createNode animCurveTL -n "CURVE371";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016851";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0 13 0 25 0;
	setAttr -s 3 ".kit[1:2]"  1 18;
	setAttr -s 3 ".kot[0:2]"  5 5 18;
	setAttr -s 3 ".kix[1:2]"  1 1;
	setAttr -s 3 ".kiy[1:2]"  0 0;
createNode animCurveTL -n "CURVE372";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016852";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0 13 0 25 0;
	setAttr -s 3 ".kit[1:2]"  1 18;
	setAttr -s 3 ".kot[0:2]"  5 5 18;
	setAttr -s 3 ".kix[1:2]"  1 1;
	setAttr -s 3 ".kiy[1:2]"  0 0;
createNode animCurveTU -n "CURVE373";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016856";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 1 13 1 25 1;
	setAttr -s 3 ".kit[1:2]"  1 18;
	setAttr -s 3 ".kot[0:2]"  5 5 18;
	setAttr -s 3 ".kix[1:2]"  1 1;
	setAttr -s 3 ".kiy[1:2]"  0 0;
createNode animCurveTU -n "CURVE374";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016857";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 1 13 1 25 1;
	setAttr -s 3 ".kit[1:2]"  1 18;
	setAttr -s 3 ".kot[0:2]"  5 5 18;
	setAttr -s 3 ".kix[1:2]"  1 1;
	setAttr -s 3 ".kiy[1:2]"  0 0;
createNode animCurveTU -n "CURVE375";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016858";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 1 13 1 25 1;
	setAttr -s 3 ".kit[1:2]"  1 18;
	setAttr -s 3 ".kot[0:2]"  5 5 18;
	setAttr -s 3 ".kix[1:2]"  1 1;
	setAttr -s 3 ".kiy[1:2]"  0 0;
createNode animCurveTA -n "CURVE376";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016853";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0 13 0 25 0;
	setAttr -s 3 ".kit[1:2]"  1 18;
	setAttr -s 3 ".kot[0:2]"  5 5 18;
	setAttr -s 3 ".kix[1:2]"  1 1;
	setAttr -s 3 ".kiy[1:2]"  0 0;
createNode animCurveTA -n "CURVE377";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016854";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 -8.544 13 8.5441077391367592 25 -8.544;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTA -n "CURVE378";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016855";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0 13 0 25 0;
	setAttr -s 3 ".kit[1:2]"  1 18;
	setAttr -s 3 ".kot[0:2]"  5 5 18;
	setAttr -s 3 ".kix[1:2]"  1 1;
	setAttr -s 3 ".kiy[1:2]"  0 0;
createNode animCurveTU -n "CURVE380";
	rename -uid "B7197D80-0000-6BA2-657C-B3730001685A";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0 20 0 25 0;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTL -n "CURVE381";
	rename -uid "B7197D80-0000-6BA2-657C-B3730001685B";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0 20 0 25 0;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTL -n "CURVE382";
	rename -uid "B7197D80-0000-6BA2-657C-B3730001685C";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0 20 0 25 0;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTL -n "CURVE383";
	rename -uid "B7197D80-0000-6BA2-657C-B3730001685D";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0 20 0 25 0;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTU -n "CURVE384";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016861";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 1 20 1 25 1;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTU -n "CURVE385";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016862";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 1 20 1 25 1;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTU -n "CURVE386";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016863";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 1 20 1 25 1;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTA -n "CURVE387";
	rename -uid "B7197D80-0000-6BA2-657C-B3730001685E";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0 20 0 25 0;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTA -n "CURVE388";
	rename -uid "B7197D80-0000-6BA2-657C-B3730001685F";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 -8.0990838333569179 20 -8.0990838333569179 25 -8.0990838333569179;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTA -n "CURVE389";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016860";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0 20 0 25 0;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTU -n "CURVE391";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016865";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0 20 0 25 0;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTL -n "CURVE392";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016866";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0 20 0 25 0;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTL -n "CURVE393";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016867";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 -1.4210854715202004e-14 20 -1.4210854715202004e-14 25 -1.4210854715202004e-14;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTL -n "CURVE394";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016868";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 1.7763568394002505e-15 20 1.7763568394002505e-15 25 1.7763568394002505e-15;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTU -n "CURVE395";
	rename -uid "B7197D80-0000-6BA2-657C-B3730001686C";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0.99999999999999956 20 0.99999999999999956 25 0.99999999999999956;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTU -n "CURVE396";
	rename -uid "B7197D80-0000-6BA2-657C-B3730001686D";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 1 20 1 25 1;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTU -n "CURVE397";
	rename -uid "B7197D80-0000-6BA2-657C-B3730001686E";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 1.0000000000000004 20 1.0000000000000004 25 1.0000000000000004;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTA -n "CURVE398";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016869";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0 20 0 25 0;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTA -n "CURVE399";
	rename -uid "B7197D80-0000-6BA2-657C-B3730001686A";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0 20 0 25 0;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTA -n "CURVE400";
	rename -uid "B7197D80-0000-6BA2-657C-B3730001686B";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 -5.1421455695746801 20 -5.1421455695746801 25 -5.1421455695746801;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTU -n "CURVE402";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016870";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE403";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016871";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE404";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016872";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE405";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016873";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE406";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016877";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1.0000000000000004 3 1.0000000000000004 6 1.0000000000000004 8 1.0000000000000004 10 1.0000000000000004
		 13 1.0000000000000004 15 1.0000000000000004 18 1.0000000000000004 20 1.0000000000000004 22 1.0000000000000004 25 1.0000000000000004;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE407";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016878";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1.0000000000000002 3 1.0000000000000002 6 1.0000000000000002 8 1.0000000000000002 10 1.0000000000000002
		 13 1.0000000000000002 15 1.0000000000000002 18 1.0000000000000002 20 1.0000000000000002 22 1.0000000000000002 25 1.0000000000000002;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE408";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016879";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1.0000000000000004 3 1.0000000000000004 6 1.0000000000000004 8 1.0000000000000004 10 1.0000000000000004
		 13 1.0000000000000004 15 1.0000000000000004 18 1.0000000000000004 20 1.0000000000000004 22 1.0000000000000004 25 1.0000000000000004;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE409";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016874";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE410";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016875";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE411";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016876";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 -5.1421455695746801 3 -5.1421455695746801 6 -5.1421455695746801 8 -5.1421455695746801 10 -5.1421455695746801
		 13 -5.1421455695746801 15 -5.1421455695746801 18 -5.1421455695746801 20 -5.1421455695746801 22 -5.1421455695746801 25 -5.1421455695746801;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE413";
	rename -uid "B7197D80-0000-6BA2-657C-B3730001687B";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0 20 0 25 0;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTL -n "CURVE414";
	rename -uid "B7197D80-0000-6BA2-657C-B3730001687C";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 2.8421709430404007e-14 20 2.8421709430404007e-14 25 2.8421709430404007e-14;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTL -n "CURVE415";
	rename -uid "B7197D80-0000-6BA2-657C-B3730001687D";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 -1.4210854715202004e-14 20 -1.4210854715202004e-14 25 -1.4210854715202004e-14;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTL -n "CURVE416";
	rename -uid "B7197D80-0000-6BA2-657C-B3730001687E";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 3.5527136788005009e-15 20 3.5527136788005009e-15 25 3.5527136788005009e-15;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTU -n "CURVE417";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016882";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0.99999999999999944 20 0.99999999999999944 25 0.99999999999999944;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTU -n "CURVE418";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016883";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0.99999999999999978 20 0.99999999999999978 25 0.99999999999999978;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTU -n "CURVE419";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016884";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0.99999999999999933 20 0.99999999999999933 25 0.99999999999999933;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTA -n "CURVE420";
	rename -uid "B7197D80-0000-6BA2-657C-B3730001687F";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0 20 0 25 0;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTA -n "CURVE421";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016880";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0 20 0 25 0;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTA -n "CURVE422";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016881";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 -13.281297366785457 20 -13.281297366785457 25 -13.281297366785457;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTU -n "CURVE424";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016886";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0 20 0 25 0;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTL -n "CURVE425";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016887";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0 20 0 25 0;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTL -n "CURVE426";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016888";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 -2.8421709430404007e-14 20 -2.8421709430404007e-14 25 -2.8421709430404007e-14;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTL -n "CURVE427";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016889";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 -1.7763568394002505e-15 20 -1.7763568394002505e-15 25 -1.7763568394002505e-15;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTU -n "CURVE428";
	rename -uid "B7197D80-0000-6BA2-657C-B3730001688D";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 1 20 1 25 1;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTU -n "CURVE429";
	rename -uid "B7197D80-0000-6BA2-657C-B3730001688E";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 1 20 1 25 1;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTU -n "CURVE430";
	rename -uid "B7197D80-0000-6BA2-657C-B3730001688F";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0.99999999999999989 20 0.99999999999999989 25 0.99999999999999989;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTA -n "CURVE431";
	rename -uid "B7197D80-0000-6BA2-657C-B3730001688A";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0 20 0 25 0;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTA -n "CURVE432";
	rename -uid "B7197D80-0000-6BA2-657C-B3730001688B";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 1.7349117590792646 20 1.7349117590792646 25 1.7349117590792646;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTA -n "CURVE433";
	rename -uid "B7197D80-0000-6BA2-657C-B3730001688C";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0 20 0 25 0;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTU -n "CURVE435";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016891";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE436";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016892";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE437";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016893";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE438";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016894";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE439";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016895";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE440";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016896";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE441";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016897";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE443";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016899";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE444";
	rename -uid "B7197D80-0000-6BA2-657C-B3730001689A";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE445";
	rename -uid "B7197D80-0000-6BA2-657C-B3730001689B";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE446";
	rename -uid "B7197D80-0000-6BA2-657C-B3730001689C";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE447";
	rename -uid "B7197D80-0000-6BA2-657C-B373000168A0";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1 3 1 6 1 8 1 10 1 13 1 15 1 18 1 20 1
		 22 1 25 1;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE448";
	rename -uid "B7197D80-0000-6BA2-657C-B373000168A1";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1 3 1 6 1 8 1 10 1 13 1 15 1 18 1 20 1
		 22 1 25 1;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE449";
	rename -uid "B7197D80-0000-6BA2-657C-B373000168A2";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1 3 1 6 1 8 1 10 1 13 1 15 1 18 1 20 1
		 22 1 25 1;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE450";
	rename -uid "B7197D80-0000-6BA2-657C-B3730001689D";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE451";
	rename -uid "B7197D80-0000-6BA2-657C-B3730001689E";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE452";
	rename -uid "B7197D80-0000-6BA2-657C-B3730001689F";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE454";
	rename -uid "B7197D80-0000-6BA2-657C-B373000168A4";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0 20 0 25 0;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTL -n "CURVE455";
	rename -uid "B7197D80-0000-6BA2-657C-B373000168A5";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 7.1054273576010019e-15 20 7.1054273576010019e-15 25 7.1054273576010019e-15;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTL -n "CURVE456";
	rename -uid "B7197D80-0000-6BA2-657C-B373000168A6";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 1.4210854715202004e-14 20 1.4210854715202004e-14 25 1.4210854715202004e-14;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTL -n "CURVE457";
	rename -uid "B7197D80-0000-6BA2-657C-B373000168A7";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 -8.8817841970012523e-16 20 -8.8817841970012523e-16 25 -8.8817841970012523e-16;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTU -n "CURVE458";
	rename -uid "B7197D80-0000-6BA2-657C-B373000168AB";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 1.0000000000000004 20 1.0000000000000004 25 1.0000000000000004;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTU -n "CURVE459";
	rename -uid "B7197D80-0000-6BA2-657C-B373000168AC";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 1 20 1 25 1;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTU -n "CURVE460";
	rename -uid "B7197D80-0000-6BA2-657C-B373000168AD";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 1.0000000000000002 20 1.0000000000000002 25 1.0000000000000002;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTA -n "CURVE461";
	rename -uid "B7197D80-0000-6BA2-657C-B373000168A8";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0 20 0 25 0;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTA -n "CURVE462";
	rename -uid "B7197D80-0000-6BA2-657C-B373000168A9";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0 20 0 25 0;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTA -n "CURVE463";
	rename -uid "B7197D80-0000-6BA2-657C-B373000168AA";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 -19.88365918056531 20 -19.88365918056531 25 -19.88365918056531;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTU -n "CURVE465";
	rename -uid "B7197D80-0000-6BA2-657C-B373000168AF";
	setAttr ".tan" 1;
	setAttr ".wgt" no;
	setAttr -s 2 ".ktv[0:1]"  1 0 25 0;
	setAttr -s 2 ".kit[0:1]"  18 1;
	setAttr -s 2 ".kot[1]"  18;
	setAttr -s 2 ".kix[1]"  1;
	setAttr -s 2 ".kiy[1]"  0;
	setAttr -s 2 ".kox[0:1]"  1 1;
	setAttr -s 2 ".koy[0:1]"  0 0;
createNode animCurveTL -n "CURVE466";
	rename -uid "B7197D80-0000-6BA2-657C-B373000168B0";
	setAttr ".tan" 1;
	setAttr ".wgt" no;
	setAttr -s 2 ".ktv[0:1]"  1 0 25 0;
	setAttr -s 2 ".kit[0:1]"  18 1;
	setAttr -s 2 ".kot[1]"  18;
	setAttr -s 2 ".kix[1]"  1;
	setAttr -s 2 ".kiy[1]"  0;
	setAttr -s 2 ".kox[0:1]"  1 1;
	setAttr -s 2 ".koy[0:1]"  0 0;
createNode animCurveTL -n "CURVE467";
	rename -uid "B7197D80-0000-6BA2-657C-B373000168B1";
	setAttr ".tan" 1;
	setAttr ".wgt" no;
	setAttr -s 2 ".ktv[0:1]"  1 0 25 0;
	setAttr -s 2 ".kit[0:1]"  18 1;
	setAttr -s 2 ".kot[1]"  18;
	setAttr -s 2 ".kix[1]"  1;
	setAttr -s 2 ".kiy[1]"  0;
	setAttr -s 2 ".kox[0:1]"  1 1;
	setAttr -s 2 ".koy[0:1]"  0 0;
createNode animCurveTL -n "CURVE468";
	rename -uid "B7197D80-0000-6BA2-657C-B373000168B2";
	setAttr ".tan" 1;
	setAttr ".wgt" no;
	setAttr -s 2 ".ktv[0:1]"  1 0 25 0;
	setAttr -s 2 ".kit[0:1]"  18 1;
	setAttr -s 2 ".kot[1]"  18;
	setAttr -s 2 ".kix[1]"  1;
	setAttr -s 2 ".kiy[1]"  0;
	setAttr -s 2 ".kox[0:1]"  1 1;
	setAttr -s 2 ".koy[0:1]"  0 0;
createNode animCurveTU -n "CURVE469";
	rename -uid "B7197D80-0000-6BA2-657C-B373000168B6";
	setAttr ".tan" 1;
	setAttr ".wgt" no;
	setAttr -s 2 ".ktv[0:1]"  1 1.0000000000000002 25 1.0000000000000002;
	setAttr -s 2 ".kit[0:1]"  18 1;
	setAttr -s 2 ".kot[1]"  18;
	setAttr -s 2 ".kix[1]"  1;
	setAttr -s 2 ".kiy[1]"  0;
	setAttr -s 2 ".kox[0:1]"  1 1;
	setAttr -s 2 ".koy[0:1]"  0 0;
createNode animCurveTU -n "CURVE470";
	rename -uid "B7197D80-0000-6BA2-657C-B373000168B7";
	setAttr ".tan" 1;
	setAttr ".wgt" no;
	setAttr -s 2 ".ktv[0:1]"  1 0.99999999999999989 25 0.99999999999999989;
	setAttr -s 2 ".kit[0:1]"  18 1;
	setAttr -s 2 ".kot[1]"  18;
	setAttr -s 2 ".kix[1]"  1;
	setAttr -s 2 ".kiy[1]"  0;
	setAttr -s 2 ".kox[0:1]"  1 1;
	setAttr -s 2 ".koy[0:1]"  0 0;
createNode animCurveTU -n "CURVE471";
	rename -uid "B7197D80-0000-6BA2-657C-B373000168B8";
	setAttr ".tan" 1;
	setAttr ".wgt" no;
	setAttr -s 2 ".ktv[0:1]"  1 1 25 1;
	setAttr -s 2 ".kit[0:1]"  18 1;
	setAttr -s 2 ".kot[1]"  18;
	setAttr -s 2 ".kix[1]"  1;
	setAttr -s 2 ".kiy[1]"  0;
	setAttr -s 2 ".kox[0:1]"  1 1;
	setAttr -s 2 ".koy[0:1]"  0 0;
createNode animCurveTA -n "CURVE472";
	rename -uid "B7197D80-0000-6BA2-657C-B373000168B3";
	setAttr ".tan" 1;
	setAttr ".wgt" no;
	setAttr -s 2 ".ktv[0:1]"  1 0 25 0;
	setAttr -s 2 ".kit[0:1]"  18 1;
	setAttr -s 2 ".kot[1]"  18;
	setAttr -s 2 ".kix[1]"  1;
	setAttr -s 2 ".kiy[1]"  0;
	setAttr -s 2 ".kox[0:1]"  1 1;
	setAttr -s 2 ".koy[0:1]"  0 0;
createNode animCurveTA -n "CURVE473";
	rename -uid "B7197D80-0000-6BA2-657C-B373000168B4";
	setAttr ".tan" 1;
	setAttr ".wgt" no;
	setAttr -s 2 ".ktv[0:1]"  1 0 25 0;
	setAttr -s 2 ".kit[0:1]"  18 1;
	setAttr -s 2 ".kot[1]"  18;
	setAttr -s 2 ".kix[1]"  1;
	setAttr -s 2 ".kiy[1]"  0;
	setAttr -s 2 ".kox[0:1]"  1 1;
	setAttr -s 2 ".koy[0:1]"  0 0;
createNode animCurveTA -n "CURVE474";
	rename -uid "B7197D80-0000-6BA2-657C-B373000168B5";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 7 ".ktv[0:6]"  1 0 2 5.0200609289598281 3 8.1745851549035962 4 0 13.999999829931973 0 14 0
		 25 0;
	setAttr -s 7 ".kit[6]"  1;
	setAttr -s 7 ".kot[0:6]"  1 18 18 18 18 18 18;
	setAttr -s 7 ".kix[6]"  1;
	setAttr -s 7 ".kiy[6]"  0;
	setAttr -s 7 ".kox[0:6]"  1 0.5043548831996536 1 1 1 1 1;
	setAttr -s 7 ".koy[0:6]"  0 0.86349646889414888 0 0 0 0 0;
createNode animCurveTU -n "CURVE476";
	rename -uid "B7197D80-0000-6BA2-657C-B373000168BA";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0 20 0 25 0;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTL -n "CURVE477";
	rename -uid "B7197D80-0000-6BA2-657C-B373000168BB";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0 20 0 25 0;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTL -n "CURVE478";
	rename -uid "B7197D80-0000-6BA2-657C-B373000168BC";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 1.4210854715202004e-14 20 1.4210854715202004e-14 25 1.4210854715202004e-14;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTL -n "CURVE479";
	rename -uid "B7197D80-0000-6BA2-657C-B373000168BD";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 -1.7763568394002505e-15 20 -1.7763568394002505e-15 25 -1.7763568394002505e-15;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTU -n "CURVE480";
	rename -uid "B7197D80-0000-6BA2-657C-B373000168C1";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 1.0000000000000004 20 1.0000000000000004 25 1.0000000000000004;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTU -n "CURVE481";
	rename -uid "B7197D80-0000-6BA2-657C-B373000168C2";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0.99999999999999944 20 0.99999999999999944 25 0.99999999999999944;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTU -n "CURVE482";
	rename -uid "B7197D80-0000-6BA2-657C-B373000168C3";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 1.0000000000000011 20 1.0000000000000011 25 1.0000000000000011;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTA -n "CURVE483";
	rename -uid "B7197D80-0000-6BA2-657C-B373000168BE";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0 20 0 25 0;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTA -n "CURVE484";
	rename -uid "B7197D80-0000-6BA2-657C-B373000168BF";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0 20 0 25 0;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTA -n "CURVE485";
	rename -uid "B7197D80-0000-6BA2-657C-B373000168C0";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 -13.281297366785457 20 -13.281297366785457 25 -13.281297366785457;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTU -n "CURVE487";
	rename -uid "B7197D80-0000-6BA2-657C-B373000168C5";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE488";
	rename -uid "B7197D80-0000-6BA2-657C-B373000168C6";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE489";
	rename -uid "B7197D80-0000-6BA2-657C-B373000168C7";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE490";
	rename -uid "B7197D80-0000-6BA2-657C-B373000168C8";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE491";
	rename -uid "B7197D80-0000-6BA2-657C-B373000168CC";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1.0000000000000002 3 1.0000000000000002 6 1.0000000000000002 8 1.0000000000000002 10 1.0000000000000002
		 13 1.0000000000000002 15 1.0000000000000002 18 1.0000000000000002 20 1.0000000000000002 22 1.0000000000000002 25 1.0000000000000002;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE492";
	rename -uid "B7197D80-0000-6BA2-657C-B373000168CD";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1 3 1 6 1 8 1 10 1 13 1 15 1 18 1 20 1
		 22 1 25 1;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE493";
	rename -uid "B7197D80-0000-6BA2-657C-B373000168CE";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1.0000000000000002 3 1.0000000000000002 6 1.0000000000000002 8 1.0000000000000002 10 1.0000000000000002
		 13 1.0000000000000002 15 1.0000000000000002 18 1.0000000000000002 20 1.0000000000000002 22 1.0000000000000002 25 1.0000000000000002;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE494";
	rename -uid "B7197D80-0000-6BA2-657C-B373000168C9";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE495";
	rename -uid "B7197D80-0000-6BA2-657C-B373000168CA";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE496";
	rename -uid "B7197D80-0000-6BA2-657C-B373000168CB";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 -19.88365918056531 3 -19.88365918056531 6 -19.88365918056531 8 -19.88365918056531 10 -19.88365918056531
		 13 -19.88365918056531 15 -19.88365918056531 18 -19.88365918056531 20 -19.88365918056531 22 -19.88365918056531 25 -19.88365918056531;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE498";
	rename -uid "B7197D80-0000-6BA2-657C-B373000168D0";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE499";
	rename -uid "B7197D80-0000-6BA2-657C-B373000168D1";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE500";
	rename -uid "B7197D80-0000-6BA2-657C-B373000168D2";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE501";
	rename -uid "B7197D80-0000-6BA2-657C-B373000168D3";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE502";
	rename -uid "B7197D80-0000-6BA2-657C-B373000168D7";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1.0000000000000007 3 1.0000000000000007 6 1.0000000000000007 8 1.0000000000000007 10 1.0000000000000007
		 13 1.0000000000000007 15 1.0000000000000007 18 1.0000000000000007 20 1.0000000000000007 22 1.0000000000000007 25 1.0000000000000007;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE503";
	rename -uid "B7197D80-0000-6BA2-657C-B373000168D8";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0.99999999999999978 3 0.99999999999999978 6 0.99999999999999978 8 0.99999999999999978 10 0.99999999999999978
		 13 0.99999999999999978 15 0.99999999999999978 18 0.99999999999999978 20 0.99999999999999978 22 0.99999999999999978 25 0.99999999999999978;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE504";
	rename -uid "B7197D80-0000-6BA2-657C-B373000168D9";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1.0000000000000011 3 1.0000000000000011 6 1.0000000000000011 8 1.0000000000000011 10 1.0000000000000011
		 13 1.0000000000000011 15 1.0000000000000011 18 1.0000000000000011 20 1.0000000000000011 22 1.0000000000000011 25 1.0000000000000011;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE505";
	rename -uid "B7197D80-0000-6BA2-657C-B373000168D4";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE506";
	rename -uid "B7197D80-0000-6BA2-657C-B373000168D5";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE507";
	rename -uid "B7197D80-0000-6BA2-657C-B373000168D6";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 -13.281297366785457 3 -13.281297366785457 6 -13.281297366785457 8 -13.281297366785457 10 -13.281297366785457
		 13 -13.281297366785457 15 -13.281297366785457 18 -13.281297366785457 20 -13.281297366785457 22 -13.281297366785457 25 -13.281297366785457;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE509";
	rename -uid "B7197D80-0000-6BA2-657C-B373000168DB";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0 20 0 25 0;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTL -n "CURVE510";
	rename -uid "B7197D80-0000-6BA2-657C-B373000168DC";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0 20 0 25 0;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTL -n "CURVE511";
	rename -uid "B7197D80-0000-6BA2-657C-B373000168DD";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0 20 0 25 0;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTL -n "CURVE512";
	rename -uid "B7197D80-0000-6BA2-657C-B373000168DE";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0 20 0 25 0;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTU -n "CURVE513";
	rename -uid "B7197D80-0000-6BA2-657C-B373000168E2";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 1 20 1 25 1;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTU -n "CURVE514";
	rename -uid "B7197D80-0000-6BA2-657C-B373000168E3";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 1 20 1 25 1;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTU -n "CURVE515";
	rename -uid "B7197D80-0000-6BA2-657C-B373000168E4";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 1 20 1 25 1;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTA -n "CURVE516";
	rename -uid "B7197D80-0000-6BA2-657C-B373000168DF";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0 20 0 25 0;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTA -n "CURVE517";
	rename -uid "B7197D80-0000-6BA2-657C-B373000168E0";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0 20 0 25 0;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTA -n "CURVE518";
	rename -uid "B7197D80-0000-6BA2-657C-B373000168E1";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0 20 0 25 0;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTU -n "CURVE520";
	rename -uid "B7197D80-0000-6BA2-657C-B373000168E6";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0 20 0 25 0;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTL -n "CURVE521";
	rename -uid "B7197D80-0000-6BA2-657C-B373000168E7";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 -7.1054273576010019e-15 20 -7.1054273576010019e-15 25 -7.1054273576010019e-15;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTL -n "CURVE522";
	rename -uid "B7197D80-0000-6BA2-657C-B373000168E8";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 1.4210854715202004e-14 20 1.4210854715202004e-14 25 1.4210854715202004e-14;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTL -n "CURVE523";
	rename -uid "B7197D80-0000-6BA2-657C-B373000168E9";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 -3.5527136788005009e-15 20 -3.5527136788005009e-15 25 -3.5527136788005009e-15;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTU -n "CURVE524";
	rename -uid "B7197D80-0000-6BA2-657C-B373000168ED";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0.99999999999999989 20 0.99999999999999989 25 0.99999999999999989;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTU -n "CURVE525";
	rename -uid "B7197D80-0000-6BA2-657C-B373000168EE";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0.99999999999999989 20 0.99999999999999989 25 0.99999999999999989;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTU -n "CURVE526";
	rename -uid "B7197D80-0000-6BA2-657C-B373000168EF";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0.99999999999999989 20 0.99999999999999989 25 0.99999999999999989;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTA -n "CURVE527";
	rename -uid "B7197D80-0000-6BA2-657C-B373000168EA";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0 20 0 25 0;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTA -n "CURVE528";
	rename -uid "B7197D80-0000-6BA2-657C-B373000168EB";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 6.4680312672739753 20 6.4680312672739753 25 6.4680312672739753;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTA -n "CURVE529";
	rename -uid "B7197D80-0000-6BA2-657C-B373000168EC";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0 20 0 25 0;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTU -n "CURVE531";
	rename -uid "B7197D80-0000-6BA2-657C-B373000168F1";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 14 ".ktv[0:13]"  1 0 2 0 5 0 8 0 12 0 13 0 14 0 15 0 17 0
		 18 0 20 0 22 0 24 0 25 0;
	setAttr -s 14 ".kit[13]"  1;
	setAttr -s 14 ".kot[0:13]"  1 18 18 18 18 18 18 18 
		18 18 18 18 18 18;
	setAttr -s 14 ".kix[13]"  1;
	setAttr -s 14 ".kiy[13]"  0;
	setAttr -s 14 ".kox[0:13]"  1 1 1 1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 14 ".koy[0:13]"  0 0 0 0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE532";
	rename -uid "B7197D80-0000-6BA2-657C-B373000168F3";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 18 ".ktv[0:17]"  1 0.45078022929086853 2 0 3 0.39712212807965575 5 0 8 0 12 0 13 0
		 14 1.6011592009422193 15 1.1732534802508487 16 0.28813300258538427 17 -0.22253157008110752 18 0 20 0 21 -0.16864269047186345 22 -0.084321345235931724 23 0.98829199735743223 24 1.1605653525823956
		 25 0.45078022929086853;
	setAttr -s 18 ".kit[17]"  1;
	setAttr -s 18 ".kot[0:17]"  1 18 18 18 18 18 18 18 
		18 18 18 18 18 18 18 18 18 18;
	setAttr -s 18 ".kix[17]"  1;
	setAttr -s 18 ".kiy[17]"  0;
	setAttr -s 18 ".kox[0:17]"  1 1 1 1 1 1 1 1 0.063339181615325924 0.059597434248727349 1 1 1 1 0.16252386276348546 
		0.080360484933234166 1 1;
	setAttr -s 18 ".koy[0:17]"  0 0 0 0 0 0 0 0 -0.99799205812085534 -0.99822249315018374 0 0 0 0 0.98670461336330828 
		0.99676586642064302 0 0;
createNode animCurveTL -n "CURVE533";
	rename -uid "B7197D80-0000-6BA2-657C-B373000168F2";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 4.9040857040112176 2 -0.40686592116282611 3 -2.1893205428798845 4 -1.8604807621657491 5 -0.91524903313619976
		 6 1.4086724044673353 7 1.7493228333280919 8 2.6730049926483108 10 2.2377101397927706 12 3.6566032299909668 13 1.7683662182556583 14 -1.942088624456346 15 -1.0820322175046384 16 0.37505662640867354
		 17 0.54676043120328655 18 0 20 -0.38491431180819946 21 -0.9899207788411053 22 2.1374413178449503 23 7.2904117321438742 24 5.6046804293273409 25 4.9040857040112176;
	setAttr -s 22 ".kit[21]"  1;
	setAttr -s 22 ".kot[0:21]"  1 18 18 18 18 18 18 18 
		18 18 18 18 18 18 18 18 18 18 18 18 18 18;
	setAttr -s 22 ".kix[21]"  1;
	setAttr -s 22 ".kiy[21]"  0;
	setAttr -s 22 ".kox[0:21]"  1 0.011747188922034964 1 0.065267646958824699 0.02548252347571291 0.04073783013431919 0.065768225322010182 
		1 1 1 0.014882780824504884 1 0.035940558360756436 0.08062531492048898 1 0.1329755008818517 0.1252779148260387 1 0.010063498460465234 1 0.034899911717302626 1;
	setAttr -s 22 ".koy[0:21]"  0 -0.9999309993956732 0 0.99786779397897107 0.99967526777314519 0.9991698700400985 0.99783492649736072 
		0 0 0 -0.99988924528416134 0 0.99935392942876711 0.99674448009205063 0 -0.99111932488738241 -0.992121688129455 0 0.99994936171725035 0 -0.99939081252637318 0;
createNode animCurveTL -n "CURVE534";
	rename -uid "B7197D80-0000-6BA2-657C-B373000168F4";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 14 ".ktv[0:13]"  1 0 2 0 5 0 8 0 12 0 13 0 14 0 15 0 17 0
		 18 0 20 0 22 0 24 0 25 0;
	setAttr -s 14 ".kit[13]"  1;
	setAttr -s 14 ".kot[0:13]"  1 18 18 18 18 18 18 18 
		18 18 18 18 18 18;
	setAttr -s 14 ".kix[13]"  1;
	setAttr -s 14 ".kiy[13]"  0;
	setAttr -s 14 ".kox[0:13]"  1 1 1 1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 14 ".koy[0:13]"  0 0 0 0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE535";
	rename -uid "B7197D80-0000-6BA2-657C-B373000168F8";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 14 ".ktv[0:13]"  1 1 2 1 5 1 8 1 12 1 13 1 14 1 15 1 17 1
		 18 1 20 1 22 1 24 1 25 1;
	setAttr -s 14 ".kit[13]"  1;
	setAttr -s 14 ".kot[0:13]"  1 18 18 18 18 18 18 18 
		18 18 18 18 18 18;
	setAttr -s 14 ".kix[13]"  1;
	setAttr -s 14 ".kiy[13]"  0;
	setAttr -s 14 ".kox[0:13]"  1 1 1 1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 14 ".koy[0:13]"  0 0 0 0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE536";
	rename -uid "B7197D80-0000-6BA2-657C-B373000168F9";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 14 ".ktv[0:13]"  1 1 2 1 5 1 8 1 12 1 13 1 14 1 15 1 17 1
		 18 1 20 1 22 1 24 1 25 1;
	setAttr -s 14 ".kit[13]"  1;
	setAttr -s 14 ".kot[0:13]"  1 18 18 18 18 18 18 18 
		18 18 18 18 18 18;
	setAttr -s 14 ".kix[13]"  1;
	setAttr -s 14 ".kiy[13]"  0;
	setAttr -s 14 ".kox[0:13]"  1 1 1 1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 14 ".koy[0:13]"  0 0 0 0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE537";
	rename -uid "B7197D80-0000-6BA2-657C-B373000168FA";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 14 ".ktv[0:13]"  1 1 2 1 5 1 8 1 12 1 13 1 14 1 15 1 17 1
		 18 1 20 1 22 1 24 1 25 1;
	setAttr -s 14 ".kit[13]"  1;
	setAttr -s 14 ".kot[0:13]"  1 18 18 18 18 18 18 18 
		18 18 18 18 18 18;
	setAttr -s 14 ".kix[13]"  1;
	setAttr -s 14 ".kiy[13]"  0;
	setAttr -s 14 ".kox[0:13]"  1 1 1 1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 14 ".koy[0:13]"  0 0 0 0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE538";
	rename -uid "B7197D80-0000-6BA2-657C-B373000168F5";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 14 ".ktv[0:13]"  1 0 2 0 5 0 8 0 12 0 13 0 14 0 15 0 17 0
		 18 0 20 0 22 0 24 0 25 0;
	setAttr -s 14 ".kit[13]"  1;
	setAttr -s 14 ".kot[0:13]"  1 18 18 18 18 18 18 18 
		18 18 18 18 18 18;
	setAttr -s 14 ".kix[13]"  1;
	setAttr -s 14 ".kiy[13]"  0;
	setAttr -s 14 ".kox[0:13]"  1 1 1 1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 14 ".koy[0:13]"  0 0 0 0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE539";
	rename -uid "B7197D80-0000-6BA2-657C-B373000168F6";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 14 ".ktv[0:13]"  1 0 2 0 5 0 8 0 12 0 13 0 14 0 15 0 17 0
		 18 0 20 0 22 0 24 0 25 0;
	setAttr -s 14 ".kit[13]"  1;
	setAttr -s 14 ".kot[0:13]"  1 18 18 18 18 18 18 18 
		18 18 18 18 18 18;
	setAttr -s 14 ".kix[13]"  1;
	setAttr -s 14 ".kiy[13]"  0;
	setAttr -s 14 ".kox[0:13]"  1 1 1 1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 14 ".koy[0:13]"  0 0 0 0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE540";
	rename -uid "B7197D80-0000-6BA2-657C-B373000168F7";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 14 ".ktv[0:13]"  1 0 2 0 5 0 8 0 12 0 13 0 14 0 15 0 17 0
		 18 0 20 0 22 0 24 0 25 0;
	setAttr -s 14 ".kit[13]"  1;
	setAttr -s 14 ".kot[0:13]"  1 18 18 18 18 18 18 18 
		18 18 18 18 18 18;
	setAttr -s 14 ".kix[13]"  1;
	setAttr -s 14 ".kiy[13]"  0;
	setAttr -s 14 ".kox[0:13]"  1 1 1 1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 14 ".koy[0:13]"  0 0 0 0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE542";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016901";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 13 ".ktv[0:12]"  1 0 3 0 6 0 8 0 10 0 12 0 13 0 15 0 18 0
		 20 0 22 0 24 0 25 0;
	setAttr -s 13 ".kit[12]"  1;
	setAttr -s 13 ".kot[0:12]"  1 18 18 18 18 18 18 18 
		18 18 18 18 18;
	setAttr -s 13 ".kix[12]"  1;
	setAttr -s 13 ".kiy[12]"  0;
	setAttr -s 13 ".kox[0:12]"  1 1 1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 13 ".koy[0:12]"  0 0 0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE543";
	rename -uid "B7197D80-0000-6BA2-657C-B373000168FF";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 13 ".ktv[0:12]"  1 0 3 0 6 0 8 5.0553935860053958 10 11.847552335066473 12 19.548725193956308
		 13 25.5 15 49.202058087359966 18 0 20 0 22 0 24 0.90864917395458611 25 0;
	setAttr -s 13 ".kit[12]"  1;
	setAttr -s 13 ".kot[0:12]"  1 18 18 18 18 18 18 18 
		18 18 18 18 18;
	setAttr -s 13 ".kix[12]"  1;
	setAttr -s 13 ".kiy[12]"  0;
	setAttr -s 13 ".kox[0:12]"  1 1 1 0.014066211563838284 0.011498781116257054 0.0091554836193396532 0.0042153403084920198 1 1 1 
		1 1 1;
	setAttr -s 13 ".koy[0:12]"  0 0 0 0.99990106595214767 0.99993388683094464 0.99995808768152672 0.99999111541357388 0 0 0 
		0 0 0;
createNode animCurveTU -n "CURVE544";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016903";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 13 ".ktv[0:12]"  1 0 3 0 6 0 8 0 10 0 12 0 13 0 15 0 18 0
		 20 0 22 0 24 0 25 0;
	setAttr -s 13 ".kit[12]"  1;
	setAttr -s 13 ".kot[0:12]"  1 18 18 18 18 18 18 18 
		18 18 18 18 18;
	setAttr -s 13 ".kix[12]"  1;
	setAttr -s 13 ".kiy[12]"  0;
	setAttr -s 13 ".kox[0:12]"  1 1 1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 13 ".koy[0:12]"  0 0 0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE545";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016902";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 13 ".ktv[0:12]"  1 0 3 0 6 0 8 0 10 0 12 0 13 0 15 0 18 0
		 20 0 22 0 24 0 25 0;
	setAttr -s 13 ".kit[12]"  1;
	setAttr -s 13 ".kot[0:12]"  1 18 18 18 18 18 18 18 
		18 18 18 18 18;
	setAttr -s 13 ".kix[12]"  1;
	setAttr -s 13 ".kiy[12]"  0;
	setAttr -s 13 ".kox[0:12]"  1 1 1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 13 ".koy[0:12]"  0 0 0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE546";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016906";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 13 ".ktv[0:12]"  1 0 3 0 6 0 8 0 10 0 12 0 13 0 15 0 18 0
		 20 0 22 0 24 0 25 0;
	setAttr -s 13 ".kit[12]"  1;
	setAttr -s 13 ".kot[0:12]"  1 18 18 18 18 18 18 18 
		18 18 18 18 18;
	setAttr -s 13 ".kix[12]"  1;
	setAttr -s 13 ".kiy[12]"  0;
	setAttr -s 13 ".kox[0:12]"  1 1 1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 13 ".koy[0:12]"  0 0 0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE547";
	rename -uid "B7197D80-0000-6BA2-657C-B373000168FC";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 13 ".ktv[0:12]"  1 0 3 0 6 0 8 0 10 0 12 0 13 0 15 0 18 0
		 20 0 22 0 24 0 25 0;
	setAttr -s 13 ".kit[12]"  1;
	setAttr -s 13 ".kot[0:12]"  1 18 18 18 18 18 18 18 
		18 18 18 18 18;
	setAttr -s 13 ".kix[12]"  1;
	setAttr -s 13 ".kiy[12]"  0;
	setAttr -s 13 ".kox[0:12]"  1 1 1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 13 ".koy[0:12]"  0 0 0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE548";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016914";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 13 ".ktv[0:12]"  1 1 3 1 6 1 8 1 10 1 12 1 13 1 15 1 18 1
		 20 1 22 1 24 1 25 1;
	setAttr -s 13 ".kit[12]"  1;
	setAttr -s 13 ".kot[0:12]"  1 18 18 18 18 18 18 18 
		18 18 18 18 18;
	setAttr -s 13 ".kix[12]"  1;
	setAttr -s 13 ".kiy[12]"  0;
	setAttr -s 13 ".kox[0:12]"  1 1 1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 13 ".koy[0:12]"  0 0 0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE549";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016915";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 13 ".ktv[0:12]"  1 1 3 1 6 1 8 1 10 1 12 1 13 1 15 1 18 1
		 20 1 22 1 24 1 25 1;
	setAttr -s 13 ".kit[12]"  1;
	setAttr -s 13 ".kot[0:12]"  1 18 18 18 18 18 18 18 
		18 18 18 18 18;
	setAttr -s 13 ".kix[12]"  1;
	setAttr -s 13 ".kiy[12]"  0;
	setAttr -s 13 ".kox[0:12]"  1 1 1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 13 ".koy[0:12]"  0 0 0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE550";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016916";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 13 ".ktv[0:12]"  1 1 3 1 6 1 8 1 10 1 12 1 13 1 15 1 18 1
		 20 1 22 1 24 1 25 1;
	setAttr -s 13 ".kit[12]"  1;
	setAttr -s 13 ".kot[0:12]"  1 18 18 18 18 18 18 18 
		18 18 18 18 18;
	setAttr -s 13 ".kix[12]"  1;
	setAttr -s 13 ".kiy[12]"  0;
	setAttr -s 13 ".kox[0:12]"  1 1 1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 13 ".koy[0:12]"  0 0 0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE551";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016911";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 13 ".ktv[0:12]"  1 0 3 0 6 0 8 0 10 0 12 0 13 0 15 0 18 0
		 20 0 22 0 24 0 25 0;
	setAttr -s 13 ".kit[12]"  1;
	setAttr -s 13 ".kot[0:12]"  1 18 18 18 18 18 18 18 
		18 18 18 18 18;
	setAttr -s 13 ".kix[12]"  1;
	setAttr -s 13 ".kiy[12]"  0;
	setAttr -s 13 ".kox[0:12]"  1 1 1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 13 ".koy[0:12]"  0 0 0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE552";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016912";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 13 ".ktv[0:12]"  1 0 3 0 6 0 8 0 10 0 12 0 13 0 15 0 18 0
		 20 0 22 0 24 0 25 0;
	setAttr -s 13 ".kit[12]"  1;
	setAttr -s 13 ".kot[0:12]"  1 18 18 18 18 18 18 18 
		18 18 18 18 18;
	setAttr -s 13 ".kix[12]"  1;
	setAttr -s 13 ".kiy[12]"  0;
	setAttr -s 13 ".kox[0:12]"  1 1 1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 13 ".koy[0:12]"  0 0 0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE553";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016913";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 13 ".ktv[0:12]"  1 0 3 0 6 0 8 0 10 0 12 0 13 0 15 0 18 0
		 20 0 22 0 24 0 25 0;
	setAttr -s 13 ".kit[12]"  1;
	setAttr -s 13 ".kot[0:12]"  1 18 18 18 18 18 18 18 
		18 18 18 18 18;
	setAttr -s 13 ".kix[12]"  1;
	setAttr -s 13 ".kiy[12]"  0;
	setAttr -s 13 ".kox[0:12]"  1 1 1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 13 ".koy[0:12]"  0 0 0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE554";
	rename -uid "B7197D80-0000-6BA2-657C-B373000168FD";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 13 ".ktv[0:12]"  1 45 3 45 6 45 8 45 10 45 12 45 13 45 15 45
		 18 45 20 45 22 45 24 45 25 45;
	setAttr -s 13 ".kit[12]"  1;
	setAttr -s 13 ".kot[0:12]"  1 18 18 18 18 18 18 18 
		18 18 18 18 18;
	setAttr -s 13 ".kix[12]"  1;
	setAttr -s 13 ".kiy[12]"  0;
	setAttr -s 13 ".kox[0:12]"  1 1 1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 13 ".koy[0:12]"  0 0 0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE555";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016909";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 13 ".ktv[0:12]"  1 0 3 0 6 0 8 0 10 0 12 0 13 0 15 0 18 0
		 20 0 22 0 24 0 25 0;
	setAttr -s 13 ".kit[12]"  1;
	setAttr -s 13 ".kot[0:12]"  1 18 18 18 18 18 18 18 
		18 18 18 18 18;
	setAttr -s 13 ".kix[12]"  1;
	setAttr -s 13 ".kiy[12]"  0;
	setAttr -s 13 ".kox[0:12]"  1 1 1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 13 ".koy[0:12]"  0 0 0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE556";
	rename -uid "B7197D80-0000-6BA2-657C-B3730001690E";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 13 ".ktv[0:12]"  1 -3.9611037234042552 3 -3.9611037234042552 6 -3.9611037234042552 8 -3.9611037234042552 10 -3.9611037234042552
		 12 -3.9611037234042552 13 -3.9611037234042552 15 -3.9611037234042552 18 -3.9611037234042552 20 -3.9611037234042552 22 -3.9611037234042552 24 -3.9611037234042552 25 -3.9611037234042552;
	setAttr -s 13 ".kit[12]"  1;
	setAttr -s 13 ".kot[0:12]"  1 18 18 18 18 18 18 18 
		18 18 18 18 18;
	setAttr -s 13 ".kix[12]"  1;
	setAttr -s 13 ".kiy[12]"  0;
	setAttr -s 13 ".kox[0:12]"  1 1 1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 13 ".koy[0:12]"  0 0 0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE557";
	rename -uid "B7197D80-0000-6BA2-657C-B3730001690F";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 13 ".ktv[0:12]"  1 -0.33631908556432782 3 -0.33631908556432782 6 -0.33631908556432782 8 -0.33631908556432782 10 -0.33631908556432782
		 12 -0.33631908556432782 13 -0.33631908556432782 15 3.5630800421865256 18 26.880096110186852 20 12.19384740163329 22 3.41764697949659 24 0.45695639303020297 25 -0.33631908556432782;
	setAttr -s 13 ".kit[12]"  1;
	setAttr -s 13 ".kot[0:12]"  1 18 18 18 18 18 18 18 
		18 18 18 18 18;
	setAttr -s 13 ".kix[12]"  1;
	setAttr -s 13 ".kiy[12]"  0;
	setAttr -s 13 ".kox[0:12]"  1 1 1 1 1 1 1 0.0076544698677573084 1 0.0071033701922140254 0.014198808286163151 0.033279672117954295 
		1;
	setAttr -s 13 ".koy[0:12]"  0 0 0 0 0 0 0 0.99997070411639744 0 -0.99997477074769858 -0.99989919184048393 -0.99944607829723431 
		0;
createNode animCurveTL -n "CURVE558";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016910";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 36.893102550718105 12 -28.744295191463912 13 -34.711331349843725 15 -46.645403666604373 16 -49.410843550997441
		 17 -44.684102621560989 18 -31.099248719040389 20 5.7256823731851458 22 32.997175028526485 24 39.777488554075717 25 36.893102550718105;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 0.0069826375729593639 0.006982637572959363 0.0085033760981317996 1 0.0045508035310266723 0.0024796696854554687 
		0.0026002402861763224 0.0048944443496054535 1 1;
	setAttr -s 11 ".koy[0:10]"  0 -0.99997562108909677 -0.99997562108909654 -0.99996384564389806 0 0.99998964503999843 0.99999692561439957 
		0.9999966193695129 0.99998802213551963 0 0;
createNode animCurveTU -n "CURVE559";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016900";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 15 ".ktv[0:14]"  1 -16.264052943330874 2 0 3 0 6 0 8 0 10 0 12 0 12.999999829931973 0
		 13 0 15 9.256077348066281 18 59.100000000000009 20 26.827696793004169 22 -8.9616887140989228 24 -27.7659485584274 25 -16.264052943330874;
	setAttr -s 15 ".kit[14]"  1;
	setAttr -s 15 ".kot[0:14]"  1 18 18 18 18 18 18 18 
		18 18 18 18 18 18 18;
	setAttr -s 15 ".kix[14]"  1;
	setAttr -s 15 ".kiy[14]"  0;
	setAttr -s 15 ".kox[0:14]"  1 1 1 1 1 1 1 1 1 0.0035250768009640167 1 0.0024487515681153806 0.0030528441348295255 
		1 1;
	setAttr -s 15 ".koy[0:14]"  0 0 0 0 0 0 0 0 0 0.9999937868974722 0 -0.99999700180338424 -0.99999534006048674 
		0 0;
createNode animCurveTU -n "CURVE560";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016905";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 13 ".ktv[0:12]"  1 0 3 0 6 0 8 0 10 0 12 0 13 0 15 0 18 0
		 20 0 22 0 24 0 25 0;
	setAttr -s 13 ".kit[12]"  1;
	setAttr -s 13 ".kot[0:12]"  1 18 18 18 18 18 18 18 
		18 18 18 18 18;
	setAttr -s 13 ".kix[12]"  1;
	setAttr -s 13 ".kiy[12]"  0;
	setAttr -s 13 ".kox[0:12]"  1 1 1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 13 ".koy[0:12]"  0 0 0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE561";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016904";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 13 ".ktv[0:12]"  1 0 3 0 6 0 8 0 10 0 12 0 13 0 15 0 18 0
		 20 0 22 0 24 0 25 0;
	setAttr -s 13 ".kit[12]"  1;
	setAttr -s 13 ".kot[0:12]"  1 18 18 18 18 18 18 18 
		18 18 18 18 18;
	setAttr -s 13 ".kix[12]"  1;
	setAttr -s 13 ".kiy[12]"  0;
	setAttr -s 13 ".kox[0:12]"  1 1 1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 13 ".koy[0:12]"  0 0 0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE562";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016907";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 13 ".ktv[0:12]"  1 0 3 0 6 0 8 0 10 0 12 0 13 0 15 0 18 0
		 20 0 22 0 24 0 25 0;
	setAttr -s 13 ".kit[12]"  1;
	setAttr -s 13 ".kot[0:12]"  1 18 18 18 18 18 18 18 
		18 18 18 18 18;
	setAttr -s 13 ".kix[12]"  1;
	setAttr -s 13 ".kiy[12]"  0;
	setAttr -s 13 ".kox[0:12]"  1 1 1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 13 ".koy[0:12]"  0 0 0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE563";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016908";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 13 ".ktv[0:12]"  1 0 3 0 6 0 8 0 10 0 12 0 13 0 15 0 18 0
		 20 0 22 0 24 0 25 0;
	setAttr -s 13 ".kit[12]"  1;
	setAttr -s 13 ".kot[0:12]"  1 18 18 18 18 18 18 18 
		18 18 18 18 18;
	setAttr -s 13 ".kix[12]"  1;
	setAttr -s 13 ".kiy[12]"  0;
	setAttr -s 13 ".kox[0:12]"  1 1 1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 13 ".koy[0:12]"  0 0 0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE564";
	rename -uid "B7197D80-0000-6BA2-657C-B3730001690A";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 13 ".ktv[0:12]"  1 0 3 0 6 0 8 0 10 0 12 0 13 0 15 0 18 0
		 20 0 22 0 24 0 25 0;
	setAttr -s 13 ".kit[12]"  1;
	setAttr -s 13 ".kot[0:12]"  1 18 18 18 18 18 18 18 
		18 18 18 18 18;
	setAttr -s 13 ".kix[12]"  1;
	setAttr -s 13 ".kiy[12]"  0;
	setAttr -s 13 ".kox[0:12]"  1 1 1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 13 ".koy[0:12]"  0 0 0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE565";
	rename -uid "B7197D80-0000-6BA2-657C-B373000168FE";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 13 ".ktv[0:12]"  1 90 3 90 6 90 8 90 10 90 12 90 13 90 15 90
		 18 90 20 90 22 90 24 90 25 90;
	setAttr -s 13 ".kit[12]"  1;
	setAttr -s 13 ".kot[0:12]"  1 18 18 18 18 18 18 18 
		18 18 18 18 18;
	setAttr -s 13 ".kix[12]"  1;
	setAttr -s 13 ".kiy[12]"  0;
	setAttr -s 13 ".kox[0:12]"  1 1 1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 13 ".koy[0:12]"  0 0 0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE566";
	rename -uid "B7197D80-0000-6BA2-657C-B3730001690D";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 13 ".ktv[0:12]"  1 0 3 0 6 0 8 0 10 0 12 0 13 0 15 0 18 0
		 20 0 22 0 24 0 25 0;
	setAttr -s 13 ".kit[1:12]"  9 18 18 9 9 18 1 18 
		18 1 9 18;
	setAttr -s 13 ".kot[1:12]"  5 18 18 5 5 18 5 18 
		18 5 5 18;
	setAttr -s 13 ".kix[7:12]"  0.02777777798473835 1 1 0.02777777798473835 1 1;
	setAttr -s 13 ".kiy[7:12]"  0 0 0 0 0 0;
createNode animCurveTU -n "CURVE567";
	rename -uid "B7197D80-0000-6BA2-657C-B3730001690B";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 13 ".ktv[0:12]"  1 0 3 0 6 0 8 0 10 0 12 0 13 0 15 0 18 0
		 20 0 22 0 24 0 25 0;
	setAttr -s 13 ".kit[12]"  1;
	setAttr -s 13 ".kot[0:12]"  1 18 18 18 18 18 18 18 
		18 18 18 18 18;
	setAttr -s 13 ".kix[12]"  1;
	setAttr -s 13 ".kiy[12]"  0;
	setAttr -s 13 ".kox[0:12]"  1 1 1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 13 ".koy[0:12]"  0 0 0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE568";
	rename -uid "B7197D80-0000-6BA2-657C-B3730001690C";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 13 ".ktv[0:12]"  1 1 3 1 6 1 8 1 10 1 12 1 13 1 15 1 18 1
		 20 1 22 1 24 1 25 1;
	setAttr -s 13 ".kit[12]"  1;
	setAttr -s 13 ".kot[0:12]"  1 18 18 18 18 18 18 18 
		18 18 18 18 18;
	setAttr -s 13 ".kix[12]"  1;
	setAttr -s 13 ".kiy[12]"  0;
	setAttr -s 13 ".kox[0:12]"  1 1 1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 13 ".koy[0:12]"  0 0 0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE570";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016918";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE571";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016919";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE572";
	rename -uid "B7197D80-0000-6BA2-657C-B3730001691A";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE573";
	rename -uid "B7197D80-0000-6BA2-657C-B3730001691B";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE574";
	rename -uid "B7197D80-0000-6BA2-657C-B3730001691F";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1.0000000000000002 3 1.0000000000000002 6 1.0000000000000002 8 1.0000000000000002 10 1.0000000000000002
		 13 1.0000000000000002 15 1.0000000000000002 18 1.0000000000000002 20 1.0000000000000002 22 1.0000000000000002 25 1.0000000000000002;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE575";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016920";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1.0000000000000002 3 1.0000000000000002 6 1.0000000000000002 8 1.0000000000000002 10 1.0000000000000002
		 13 1.0000000000000002 15 1.0000000000000002 18 1.0000000000000002 20 1.0000000000000002 22 1.0000000000000002 25 1.0000000000000002;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE576";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016921";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1.0000000000000004 3 1.0000000000000004 6 1.0000000000000004 8 1.0000000000000004 10 1.0000000000000004
		 13 1.0000000000000004 15 1.0000000000000004 18 1.0000000000000004 20 1.0000000000000004 22 1.0000000000000004 25 1.0000000000000004;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE577";
	rename -uid "B7197D80-0000-6BA2-657C-B3730001691C";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE578";
	rename -uid "B7197D80-0000-6BA2-657C-B3730001691D";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE579";
	rename -uid "B7197D80-0000-6BA2-657C-B3730001691E";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 -24.183597580285252 3 -24.183597580285252 6 -24.183597580285252 8 -24.183597580285252 10 -24.183597580285252
		 13 -24.183597580285252 15 -24.183597580285252 18 -24.183597580285252 20 -24.183597580285252 22 -24.183597580285252 25 -24.183597580285252;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE581";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016923";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE582";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016924";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 1.3154153666531898 6 2.6308307333063796 8 2.4898396874481095 10 1.6598889752325938
		 13 0 15 -1.3155 18 -2.631 20 -2.49 22 -1.6599958500000001 25 0;
	setAttr -s 11 ".kyts[1:10]" yes no yes yes no yes no yes yes no;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 0.078942048780411334 1 0.19330212597458596 0.083382012975073749 0.069847846293330948 0.078937001651558369 
		1 0.19329030905297323 0.083376681948547873 1;
	setAttr -s 11 ".koy[0:10]"  0 0.99687920679205222 0 -0.98113928068022294 -0.9965176565983288 -0.99755765666360519 -0.99687960645719997 
		0 0.98114160875288858 0.99651810264904406 0;
createNode animCurveTL -n "CURVE583";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016925";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 21 ".ktv[0:20]"  1 -2.951696651869931 2 -4.5504006997639772 3 -5.0853210627669556 4 -4.7162607683376701 5 -3.7518869586669106
		 6 -2.3509889149691632 8 -0.56073352989324754 10 -0.049881445394944275 11 -0.38161920045705661 12 -1.3964287299750744 13 -2.951696651869931 14 -4.4952547358568973 15 -5.0853210627669556 16 -4.7163083558565617
		 17 -3.7520229230065958 18 -2.351172466827737 20 -0.56073352989324754 22 -0.049881445394944275 23 -0.41436057208854465 24 -1.4619862115284836 25 -2.9520329741768569;
	setAttr -s 21 ".kit[20]"  1;
	setAttr -s 21 ".kot[0:20]"  1 18 18 18 18 18 18 18 
		18 18 18 18 18 18 18 18 18 18 18 18 18;
	setAttr -s 21 ".kix[20]"  1;
	setAttr -s 21 ".kiy[20]"  0;
	setAttr -s 21 ".kox[0:20]"  1 0.039027414850465167 1 0.062373590421300924 0.035210185520909147 0.039140773415789927 0.07223965822141272 
		1 0.061768501957013285 0.032407413159495607 0.02688218610413301 0.039027414850465181 1 0.062379926277732936 0.035212207135823237 0.039139108384400725 0.072233926423534933 1 0.058911070119888893 0.032820799735137185 1;
	setAttr -s 21 ".koy[0:20]"  0 -0.99923814022989021 0 0.99805287195516645 0.99937992917387675 0.99923370632520891 0.99738730279668875 
		0 -0.99809050299358448 -0.99947474183808649 -0.99963860873330757 -0.99923814022989021 0 0.99805247597387614 0.99937985794622863 0.99923377154441406 0.99738771792790748 0 -0.99826323473186651 -0.99946125242789985 0;
createNode animCurveTL -n "CURVE584";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016926";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 -0.38618716021801447 3 -0.38618716021801447 6 -0.38618716021801447 8 -0.38618716021801447 10 -0.38618716021801447
		 13 -0.38618716021801447 15 -0.38618716021801447 18 -0.38618716021801447 20 -0.38618716021801447 22 -0.38618716021801447 25 -0.38618716021801447;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE585";
	rename -uid "B7197D80-0000-6BA2-657C-B3730001692A";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1 3 1 6 1 8 1 10 1 13 1 15 1 18 1 20 1
		 22 1 25 1;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE586";
	rename -uid "B7197D80-0000-6BA2-657C-B3730001692B";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1 3 1 6 1 8 1 10 1 13 1 15 1 18 1 20 1
		 22 1 25 1;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE587";
	rename -uid "B7197D80-0000-6BA2-657C-B3730001692C";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1 3 1 6 1 8 1 10 1 13 1 15 1 18 1 20 1
		 22 1 25 1;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE588";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016927";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE589";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016928";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE590";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016929";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 9 ".ktv[0:8]"  1 -0.23599999999999996 3 1.7570000000000001 6 3.7499999999999996 10 2.4999937499999998 13 0.23599999999999988
		 15 -1.7569999999999997 18 -3.7499999999999991 22 -2.4999937499999998 25 -0.23601398601398585;
	setAttr -s 9 ".kyts[1:8]" yes no yes no yes no yes no;
	setAttr -s 9 ".kit[8]"  1;
	setAttr -s 9 ".kot[0:8]"  1 18 18 18 18 18 18 18 
		18;
	setAttr -s 9 ".kix[8]"  1;
	setAttr -s 9 ".kiy[8]"  0;
	setAttr -s 9 ".kox[0:8]"  1 0.94851327622244741 1 0.97859888856070176 0.94189390257904904 0.94851327622244741 1 0.97859905348713006 
		1;
	setAttr -s 9 ".koy[0:8]"  0 0.31673737517028078 0 -0.20577710102865943 -0.3359105182699833 -0.31673737517028067 0 0.2057763166987224 
		0;
createNode animCurveTU -n "CURVE592";
	rename -uid "B7197D80-0000-6BA2-657C-B3730001692E";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE593";
	rename -uid "B7197D80-0000-6BA2-657C-B3730001692F";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE594";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016930";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE595";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016931";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE596";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016932";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE597";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016933";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE598";
	rename -uid "B7197D80-0000-6BA2-657C-B37300016934";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE600";
	rename -uid "B7197D80-0000-6BA2-657C-B37400016936";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE601";
	rename -uid "B7197D80-0000-6BA2-657C-B37400016937";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE602";
	rename -uid "B7197D80-0000-6BA2-657C-B37400016938";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE603";
	rename -uid "B7197D80-0000-6BA2-657C-B37400016939";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE604";
	rename -uid "B7197D80-0000-6BA2-657C-B3740001693D";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1.0000000000000002 3 1.0000000000000002 6 1.0000000000000002 8 1.0000000000000002 10 1.0000000000000002
		 13 1.0000000000000002 15 1.0000000000000002 18 1.0000000000000002 20 1.0000000000000002 22 1.0000000000000002 25 1.0000000000000002;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE605";
	rename -uid "B7197D80-0000-6BA2-657C-B3740001693E";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1 3 1 6 1 8 1 10 1 13 1 15 1 18 1 20 1
		 22 1 25 1;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE606";
	rename -uid "B7197D80-0000-6BA2-657C-B3740001693F";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1 3 1 6 1 8 1 10 1 13 1 15 1 18 1 20 1
		 22 1 25 1;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE607";
	rename -uid "B7197D80-0000-6BA2-657C-B3740001693A";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE608";
	rename -uid "B7197D80-0000-6BA2-657C-B3740001693B";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 6.4680312672739753 3 6.4680312672739753 6 6.4680312672739753 8 6.4680312672739753 10 6.4680312672739753
		 13 6.4680312672739753 15 6.4680312672739753 18 6.4680312672739753 20 6.4680312672739753 22 6.4680312672739753 25 6.4680312672739753;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE609";
	rename -uid "B7197D80-0000-6BA2-657C-B3740001693C";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE611";
	rename -uid "B7197D80-0000-6BA2-657C-B37400016941";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0 20 0 25 0;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTL -n "CURVE612";
	rename -uid "B7197D80-0000-6BA2-657C-B37400016942";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0 20 0 25 0;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTL -n "CURVE613";
	rename -uid "B7197D80-0000-6BA2-657C-B37400016943";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 -1.4210854715202004e-14 20 -1.4210854715202004e-14 25 -1.4210854715202004e-14;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTL -n "CURVE614";
	rename -uid "B7197D80-0000-6BA2-657C-B37400016944";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 2.2204460492503131e-16 20 2.2204460492503131e-16 25 2.2204460492503131e-16;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTU -n "CURVE615";
	rename -uid "B7197D80-0000-6BA2-657C-B37400016948";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 1.0000000000000002 20 1.0000000000000002 25 1.0000000000000002;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTU -n "CURVE616";
	rename -uid "B7197D80-0000-6BA2-657C-B37400016949";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 1.0000000000000002 20 1.0000000000000002 25 1.0000000000000002;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTU -n "CURVE617";
	rename -uid "B7197D80-0000-6BA2-657C-B3740001694A";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 1.0000000000000004 20 1.0000000000000004 25 1.0000000000000004;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTA -n "CURVE618";
	rename -uid "B7197D80-0000-6BA2-657C-B37400016945";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0 20 0 25 0;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTA -n "CURVE619";
	rename -uid "B7197D80-0000-6BA2-657C-B37400016946";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0 20 0 25 0;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTA -n "CURVE620";
	rename -uid "B7197D80-0000-6BA2-657C-B37400016947";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 -24.183597580285252 20 -24.183597580285252 25 -24.183597580285252;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTU -n "CURVE622";
	rename -uid "B7197D80-0000-6BA2-657C-B3740001694C";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0 20 0 25 0;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTL -n "CURVE623";
	rename -uid "B7197D80-0000-6BA2-657C-B3740001694D";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 1.4210854715202004e-14 20 1.4210854715202004e-14 25 1.4210854715202004e-14;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTL -n "CURVE624";
	rename -uid "B7197D80-0000-6BA2-657C-B3740001694E";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 -1.4210854715202004e-14 20 -1.4210854715202004e-14 25 -1.4210854715202004e-14;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTL -n "CURVE625";
	rename -uid "B7197D80-0000-6BA2-657C-B3740001694F";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 2.2204460492503131e-16 20 2.2204460492503131e-16 25 2.2204460492503131e-16;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTU -n "CURVE626";
	rename -uid "B7197D80-0000-6BA2-657C-B37400016953";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 1.0000000000000002 20 1.0000000000000002 25 1.0000000000000002;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTU -n "CURVE627";
	rename -uid "B7197D80-0000-6BA2-657C-B37400016954";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 1.0000000000000002 20 1.0000000000000002 25 1.0000000000000002;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTU -n "CURVE628";
	rename -uid "B7197D80-0000-6BA2-657C-B37400016955";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 1.0000000000000004 20 1.0000000000000004 25 1.0000000000000004;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTA -n "CURVE629";
	rename -uid "B7197D80-0000-6BA2-657C-B37400016950";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0 20 0 25 0;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTA -n "CURVE630";
	rename -uid "B7197D80-0000-6BA2-657C-B37400016951";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0 20 0 25 0;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTA -n "CURVE631";
	rename -uid "B7197D80-0000-6BA2-657C-B37400016952";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 -24.183597580285252 20 -24.183597580285252 25 -24.183597580285252;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTU -n "CURVE633";
	rename -uid "B7197D80-0000-6BA2-657C-B37400016957";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 9 ".ktv[0:8]"  1 0 6 0 8 0 13 0 15 0 18 0 20 0 22 0 25 0;
	setAttr -s 9 ".kit[8]"  1;
	setAttr -s 9 ".kot[0:8]"  1 18 18 18 18 18 18 18 
		18;
	setAttr -s 9 ".kix[8]"  1;
	setAttr -s 9 ".kiy[8]"  0;
	setAttr -s 9 ".kox[0:8]"  1 1 1 1 1 1 1 1 1;
	setAttr -s 9 ".koy[0:8]"  0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE634";
	rename -uid "B7197D80-0000-6BA2-657C-B37400016958";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 9 ".ktv[0:8]"  1 0 6 0 8 0 13 0 15 0 18 0 20 0 22 0 25 0;
	setAttr -s 9 ".kit[8]"  1;
	setAttr -s 9 ".kot[0:8]"  1 18 18 18 18 18 18 18 
		18;
	setAttr -s 9 ".kix[8]"  1;
	setAttr -s 9 ".kiy[8]"  0;
	setAttr -s 9 ".kox[0:8]"  1 1 1 1 1 1 1 1 1;
	setAttr -s 9 ".koy[0:8]"  0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE635";
	rename -uid "B7197D80-0000-6BA2-657C-B37400016959";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 9 ".ktv[0:8]"  1 0 6 0 8 0 13 0 15 0 18 0 20 0 22 0 25 0;
	setAttr -s 9 ".kit[8]"  1;
	setAttr -s 9 ".kot[0:8]"  1 18 18 18 18 18 18 18 
		18;
	setAttr -s 9 ".kix[8]"  1;
	setAttr -s 9 ".kiy[8]"  0;
	setAttr -s 9 ".kox[0:8]"  1 1 1 1 1 1 1 1 1;
	setAttr -s 9 ".koy[0:8]"  0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE636";
	rename -uid "B7197D80-0000-6BA2-657C-B3740001695A";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 9 ".ktv[0:8]"  1 0 6 0 8 0 13 0 15 0 18 0 20 0 22 0 25 0;
	setAttr -s 9 ".kit[8]"  1;
	setAttr -s 9 ".kot[0:8]"  1 18 18 18 18 18 18 18 
		18;
	setAttr -s 9 ".kix[8]"  1;
	setAttr -s 9 ".kiy[8]"  0;
	setAttr -s 9 ".kox[0:8]"  1 1 1 1 1 1 1 1 1;
	setAttr -s 9 ".koy[0:8]"  0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE637";
	rename -uid "B7197D80-0000-6BA2-657C-B3740001695B";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 9 ".ktv[0:8]"  1 27.159847915894265 3 26.858370873464523 6 27.508994346479859 12.999999829931973 31.852191284509704
		 13 31.852191390029503 15 32.81088764043507 18 30.772976564553094 20 29.274554577276618 25 27.159847915894265;
	setAttr -s 9 ".kit[8]"  1;
	setAttr -s 9 ".kot[0:8]"  1 18 18 18 18 18 18 18 
		18;
	setAttr -s 9 ".kix[8]"  1;
	setAttr -s 9 ".kiy[8]"  0;
	setAttr -s 9 ".kox[0:8]"  1 1 0.97881449717270963 0.96784694419528694 0.98043165499380092 1 0.95880781446460817 0.97741559957015944 
		1;
	setAttr -s 9 ".koy[0:8]"  0 0 0.2047490662360531 0.25153984299081761 0.19685977213772379 0 -0.28405558421126192 -0.21132615956597955 
		0;
createNode animCurveTA -n "CURVE638";
	rename -uid "B7197D80-0000-6BA2-657C-B3740001695C";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 9 ".ktv[0:8]"  1 6.206277544716289 6 6.206277544716289 8 6.206277544716289 13 6.206277544716289 15 6.206277544716289
		 18 6.206277544716289 20 6.206277544716289 22 6.206277544716289 25 6.206277544716289;
	setAttr -s 9 ".kit[8]"  1;
	setAttr -s 9 ".kot[0:8]"  1 18 18 18 18 18 18 18 
		18;
	setAttr -s 9 ".kix[8]"  1;
	setAttr -s 9 ".kiy[8]"  0;
	setAttr -s 9 ".kox[0:8]"  1 1 1 1 1 1 1 1 1;
	setAttr -s 9 ".koy[0:8]"  0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE639";
	rename -uid "B7197D80-0000-6BA2-657C-B3740001695D";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 9 ".ktv[0:8]"  1 -0.51740249432967944 6 -5.2404627173249505 12.999999829931973 1.5522073179582518 13 1.5522074829890398
		 15 8.3844696333566162 18 2.7163630952308191 20 0.51740249432967955 22 0 25 -0.51740249432967944;
	setAttr -s 9 ".kit[8]"  1;
	setAttr -s 9 ".kot[0:8]"  1 18 18 18 18 18 18 18 
		18;
	setAttr -s 9 ".kix[8]"  1;
	setAttr -s 9 ".kiy[8]"  0;
	setAttr -s 9 ".kox[0:8]"  1 1 0.92639470628618581 0.63410925468678081 1 0.83496627424295011 0.96184276914119582 0.99626333039741988 
		1;
	setAttr -s 9 ".koy[0:8]"  0 0 0.37655391136586491 0.77324346303125979 0 -0.55030111836779561 -0.27360279137975962 -0.086367682065928916 
		0;
createNode animCurveTU -n "CURVE641";
	rename -uid "B7197D80-0000-6BA2-657C-B3740001695F";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0 20 0 25 0;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTL -n "CURVE642";
	rename -uid "B7197D80-0000-6BA2-657C-B37400016960";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0 20 0 25 0;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTL -n "CURVE643";
	rename -uid "B7197D80-0000-6BA2-657C-B37400016961";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0 20 0 25 0;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTL -n "CURVE644";
	rename -uid "B7197D80-0000-6BA2-657C-B37400016962";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0 20 0 25 0;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTU -n "CURVE645";
	rename -uid "B7197D80-0000-6BA2-657C-B37400016966";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 1 20 1 25 1;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTU -n "CURVE646";
	rename -uid "B7197D80-0000-6BA2-657C-B37400016967";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0.99999999999999978 20 0.99999999999999978 25 0.99999999999999978;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTU -n "CURVE647";
	rename -uid "B7197D80-0000-6BA2-657C-B37400016968";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0.99999999999999978 20 0.99999999999999978 25 0.99999999999999978;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTA -n "CURVE648";
	rename -uid "B7197D80-0000-6BA2-657C-B37400016963";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0 20 0 25 0;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTA -n "CURVE649";
	rename -uid "B7197D80-0000-6BA2-657C-B37400016964";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 9.565175890006417 20 9.565175890006417 25 9.565175890006417;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTA -n "CURVE650";
	rename -uid "B7197D80-0000-6BA2-657C-B37400016965";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0 20 0 25 0;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTU -n "CURVE652";
	rename -uid "B7197D80-0000-6BA2-657C-B3740001696A";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE653";
	rename -uid "B7197D80-0000-6BA2-657C-B3740001696B";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE654";
	rename -uid "B7197D80-0000-6BA2-657C-B3740001696C";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE655";
	rename -uid "B7197D80-0000-6BA2-657C-B3740001696D";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE656";
	rename -uid "B7197D80-0000-6BA2-657C-B37400016971";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1 3 1 6 1 8 1 10 1 13 1 15 1 18 1 20 1
		 22 1 25 1;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE657";
	rename -uid "B7197D80-0000-6BA2-657C-B37400016972";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0.99999999999999989 3 0.99999999999999989 6 0.99999999999999989 8 0.99999999999999989 10 0.99999999999999989
		 13 0.99999999999999989 15 0.99999999999999989 18 0.99999999999999989 20 0.99999999999999989 22 0.99999999999999989 25 0.99999999999999989;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE658";
	rename -uid "B7197D80-0000-6BA2-657C-B37400016973";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1 3 1 6 1 8 1 10 1 13 1 15 1 18 1 20 1
		 22 1 25 1;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE659";
	rename -uid "B7197D80-0000-6BA2-657C-B3740001696E";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE660";
	rename -uid "B7197D80-0000-6BA2-657C-B3740001696F";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE661";
	rename -uid "B7197D80-0000-6BA2-657C-B37400016970";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 -13.281297366785457 3 -13.281297366785457 6 -13.281297366785457 8 -13.281297366785457 10 -13.281297366785457
		 13 -13.281297366785457 15 -13.281297366785457 18 -13.281297366785457 20 -13.281297366785457 22 -13.281297366785457 25 -13.281297366785457;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE663";
	rename -uid "B7197D80-0000-6BA2-657C-B37400016975";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE664";
	rename -uid "B7197D80-0000-6BA2-657C-B37400016976";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE665";
	rename -uid "B7197D80-0000-6BA2-657C-B37400016977";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE666";
	rename -uid "B7197D80-0000-6BA2-657C-B37400016978";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE667";
	rename -uid "B7197D80-0000-6BA2-657C-B3740001697C";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0.99999999999999978 3 0.99999999999999978 6 0.99999999999999978 8 0.99999999999999978 10 0.99999999999999978
		 13 0.99999999999999978 15 0.99999999999999978 18 0.99999999999999978 20 0.99999999999999978 22 0.99999999999999978 25 0.99999999999999978;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE668";
	rename -uid "B7197D80-0000-6BA2-657C-B3740001697D";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0.99999999999999911 3 0.99999999999999911 6 0.99999999999999911 8 0.99999999999999911 10 0.99999999999999911
		 13 0.99999999999999911 15 0.99999999999999911 18 0.99999999999999911 20 0.99999999999999911 22 0.99999999999999911 25 0.99999999999999911;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE669";
	rename -uid "B7197D80-0000-6BA2-657C-B3740001697E";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0.99999999999999967 3 0.99999999999999967 6 0.99999999999999967 8 0.99999999999999967 10 0.99999999999999967
		 13 0.99999999999999967 15 0.99999999999999967 18 0.99999999999999967 20 0.99999999999999967 22 0.99999999999999967 25 0.99999999999999967;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE670";
	rename -uid "B7197D80-0000-6BA2-657C-B37400016979";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE671";
	rename -uid "B7197D80-0000-6BA2-657C-B3740001697A";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE672";
	rename -uid "B7197D80-0000-6BA2-657C-B3740001697B";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 -19.88365918056531 3 -19.88365918056531 6 -19.88365918056531 8 -19.88365918056531 10 -19.88365918056531
		 13 -19.88365918056531 15 -19.88365918056531 18 -19.88365918056531 20 -19.88365918056531 22 -19.88365918056531 25 -19.88365918056531;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE674";
	rename -uid "B7197D80-0000-6BA2-657C-B37400016980";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0 20 0 25 0;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTL -n "CURVE675";
	rename -uid "B7197D80-0000-6BA2-657C-B37400016981";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 7.1054273576010019e-15 20 7.1054273576010019e-15 25 7.1054273576010019e-15;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTL -n "CURVE676";
	rename -uid "B7197D80-0000-6BA2-657C-B37400016982";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 -1.4210854715202004e-14 20 -1.4210854715202004e-14 25 -1.4210854715202004e-14;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTL -n "CURVE677";
	rename -uid "B7197D80-0000-6BA2-657C-B37400016983";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0 20 0 25 0;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTU -n "CURVE678";
	rename -uid "B7197D80-0000-6BA2-657C-B37400016987";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 1 20 1 25 1;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTU -n "CURVE679";
	rename -uid "B7197D80-0000-6BA2-657C-B37400016988";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0.99999999999999978 20 0.99999999999999978 25 0.99999999999999978;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTU -n "CURVE680";
	rename -uid "B7197D80-0000-6BA2-657C-B37400016989";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 1.0000000000000002 20 1.0000000000000002 25 1.0000000000000002;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTA -n "CURVE681";
	rename -uid "B7197D80-0000-6BA2-657C-B37400016984";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0 20 0 25 0;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTA -n "CURVE682";
	rename -uid "B7197D80-0000-6BA2-657C-B37400016985";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 -2.574738921613474 20 -2.574738921613474 25 -2.574738921613474;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTA -n "CURVE683";
	rename -uid "B7197D80-0000-6BA2-657C-B37400016986";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0 20 0 25 0;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTU -n "CURVE685";
	rename -uid "B7197D80-0000-6BA2-657C-B3740001698B";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE686";
	rename -uid "B7197D80-0000-6BA2-657C-B3740001698C";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE687";
	rename -uid "B7197D80-0000-6BA2-657C-B3740001698D";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE688";
	rename -uid "B7197D80-0000-6BA2-657C-B3740001698E";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE689";
	rename -uid "B7197D80-0000-6BA2-657C-B37400016992";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0.99999999999999978 3 0.99999999999999978 6 0.99999999999999978 8 0.99999999999999978 10 0.99999999999999978
		 13 0.99999999999999978 15 0.99999999999999978 18 0.99999999999999978 20 0.99999999999999978 22 0.99999999999999978 25 0.99999999999999978;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE690";
	rename -uid "B7197D80-0000-6BA2-657C-B37400016993";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0.99999999999999989 3 0.99999999999999989 6 0.99999999999999989 8 0.99999999999999989 10 0.99999999999999989
		 13 0.99999999999999989 15 0.99999999999999989 18 0.99999999999999989 20 0.99999999999999989 22 0.99999999999999989 25 0.99999999999999989;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE691";
	rename -uid "B7197D80-0000-6BA2-657C-B37400016994";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0.99999999999999967 3 0.99999999999999967 6 0.99999999999999967 8 0.99999999999999967 10 0.99999999999999967
		 13 0.99999999999999967 15 0.99999999999999967 18 0.99999999999999967 20 0.99999999999999967 22 0.99999999999999967 25 0.99999999999999967;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE692";
	rename -uid "B7197D80-0000-6BA2-657C-B3740001698F";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE693";
	rename -uid "B7197D80-0000-6BA2-657C-B37400016990";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE694";
	rename -uid "B7197D80-0000-6BA2-657C-B37400016991";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 -3.6408012963077039 3 -3.6408012963077039 6 -3.6408012963077039 8 -3.6408012963077039 10 -3.6408012963077039
		 13 -3.6408012963077039 15 -3.6408012963077039 18 -3.6408012963077039 20 -3.6408012963077039 22 -3.6408012963077039 25 -3.6408012963077039;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 18;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
// End