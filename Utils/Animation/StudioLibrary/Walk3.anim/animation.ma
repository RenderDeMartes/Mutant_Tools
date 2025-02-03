//Maya ASCII 2022 scene
//Name: animation.ma
//Last modified: Fri, Dec 15, 2023 12:16:12 PM
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
fileInfo "UUID" "B7197D80-0000-6BA2-657C-B40C00021FA6";
createNode animCurveTU -n "CURVE1";
	rename -uid "B7197D80-0000-6BA2-657C-B40B00021CE7";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE2";
	rename -uid "B7197D80-0000-6BA2-657C-B40B00021CE8";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE3";
	rename -uid "B7197D80-0000-6BA2-657C-B40B00021CE9";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE4";
	rename -uid "B7197D80-0000-6BA2-657C-B40B00021CEA";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE5";
	rename -uid "B7197D80-0000-6BA2-657C-B40B00021CEE";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1.0000000000000002 3 1.0000000000000002 6 1.0000000000000002 8 1.0000000000000002 10 1.0000000000000002
		 13 1.0000000000000002 15 1.0000000000000002 18 1.0000000000000002 20 1.0000000000000002 22 1.0000000000000002 25 1.0000000000000002;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE6";
	rename -uid "B7197D80-0000-6BA2-657C-B40B00021CEF";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1.0000000000000002 3 1.0000000000000002 6 1.0000000000000002 8 1.0000000000000002 10 1.0000000000000002
		 13 1.0000000000000002 15 1.0000000000000002 18 1.0000000000000002 20 1.0000000000000002 22 1.0000000000000002 25 1.0000000000000002;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE7";
	rename -uid "B7197D80-0000-6BA2-657C-B40B00021CF0";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1.0000000000000002 3 1.0000000000000002 6 1.0000000000000002 8 1.0000000000000002 10 1.0000000000000002
		 13 1.0000000000000002 15 1.0000000000000002 18 1.0000000000000002 20 1.0000000000000002 22 1.0000000000000002 25 1.0000000000000002;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE8";
	rename -uid "B7197D80-0000-6BA2-657C-B40B00021CEB";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE9";
	rename -uid "B7197D80-0000-6BA2-657C-B40B00021CEC";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE10";
	rename -uid "B7197D80-0000-6BA2-657C-B40B00021CED";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 -5.1421455695746801 3 -5.1421455695746801 6 -5.1421455695746801 8 -5.1421455695746801 10 -5.1421455695746801
		 13 -5.1421455695746801 15 -5.1421455695746801 18 -5.1421455695746801 20 -5.1421455695746801 22 -5.1421455695746801 25 -5.1421455695746801;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE12";
	rename -uid "B7197D80-0000-6BA2-657C-B40B00021CF2";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 12 ".ktv[0:11]"  1 3 3 3 6 3 8 3 10 3 12.999999829931973 3 13 3 15 3
		 18 3 20 3 22 3 25 3;
	setAttr -s 12 ".kit[11]"  1;
	setAttr -s 12 ".kot[0:11]"  1 18 18 18 18 18 18 18 
		18 18 18 1;
	setAttr -s 12 ".kix[11]"  1;
	setAttr -s 12 ".kiy[11]"  0;
	setAttr -s 12 ".kox[0:11]"  1 1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 12 ".koy[0:11]"  0 0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE13";
	rename -uid "B7197D80-0000-6BA2-657C-B40B00021CF3";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 12 ".ktv[0:11]"  1 0 3 0 6 0 8 0 10 0 12.999999829931973 0 13 0 15 0
		 18 0 20 0 22 0 25 0;
	setAttr -s 12 ".kit[11]"  1;
	setAttr -s 12 ".kot[0:11]"  1 18 18 18 18 18 18 18 
		18 18 18 1;
	setAttr -s 12 ".kix[11]"  1;
	setAttr -s 12 ".kiy[11]"  0;
	setAttr -s 12 ".kox[0:11]"  1 1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 12 ".koy[0:11]"  0 0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE14";
	rename -uid "B7197D80-0000-6BA2-657C-B40B00021CF4";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 12 ".ktv[0:11]"  1 0 3 0 6 0 8 0 10 0 12.999999829931973 0 13 0 15 0
		 18 0 20 0 22 0 25 0;
	setAttr -s 12 ".kit[11]"  1;
	setAttr -s 12 ".kot[0:11]"  1 18 18 18 18 18 18 18 
		18 18 18 1;
	setAttr -s 12 ".kix[11]"  1;
	setAttr -s 12 ".kiy[11]"  0;
	setAttr -s 12 ".kox[0:11]"  1 1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 12 ".koy[0:11]"  0 0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE15";
	rename -uid "B7197D80-0000-6BA2-657C-B40B00021CF5";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 12 ".ktv[0:11]"  1 0 3 0 6 0 8 0 10 0 12.999999829931973 0 13 0 15 0
		 18 0 20 0 22 0 25 0;
	setAttr -s 12 ".kit[11]"  1;
	setAttr -s 12 ".kot[0:11]"  1 18 18 18 18 18 18 18 
		18 18 18 1;
	setAttr -s 12 ".kix[11]"  1;
	setAttr -s 12 ".kiy[11]"  0;
	setAttr -s 12 ".kox[0:11]"  1 1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 12 ".koy[0:11]"  0 0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE16";
	rename -uid "B7197D80-0000-6BA2-657C-B40B00021CF6";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 12 ".ktv[0:11]"  1 0 3 0 6 0 8 0 10 0 12.999999829931973 0 13 0 15 0
		 18 0 20 0 22 0 25 0;
	setAttr -s 12 ".kit[11]"  1;
	setAttr -s 12 ".kot[0:11]"  1 18 18 18 18 18 18 18 
		18 18 18 1;
	setAttr -s 12 ".kix[11]"  1;
	setAttr -s 12 ".kiy[11]"  0;
	setAttr -s 12 ".kox[0:11]"  1 1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 12 ".koy[0:11]"  0 0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE17";
	rename -uid "B7197D80-0000-6BA2-657C-B40B00021CF7";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 12 ".ktv[0:11]"  1 -37.608229531745188 3 -37.608229531745188 6 -37.608229531745188 8 -37.608229531745188 10 -37.608229531745188
		 12.999999829931973 -37.608229531745188 13 -37.608229531745188 15 -37.608229531745188 18 -37.608229531745188 20 -37.608229531745188 22 -37.608229531745188 25 -37.608229531745188;
	setAttr -s 12 ".kit[11]"  1;
	setAttr -s 12 ".kot[0:11]"  1 18 18 18 18 18 18 18 
		18 18 18 1;
	setAttr -s 12 ".kix[11]"  1;
	setAttr -s 12 ".kiy[11]"  0;
	setAttr -s 12 ".kox[0:11]"  1 1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 12 ".koy[0:11]"  0 0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE18";
	rename -uid "B7197D80-0000-6BA2-657C-B40B00021CF8";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 14 ".ktv[0:13]"  1 -11.171031891821766 3 -8.8996876604060802 4 -5.646180133353651 6 3.9921069278295347 7 9.8997382320516287
		 8 13.012660743983346 10 16.753283492878062 12.999999829931973 18.548999999999992 13 18.549269962179174 15 14.665687035957037 18 -0.51450427907132945 20 -6.0674002632788024 22 -8.9428130962911325
		 25 -11.171031891821766;
	setAttr -s 14 ".kit[13]"  1;
	setAttr -s 14 ".kot[0:13]"  1 18 18 18 18 18 18 18 
		18 18 18 18 18 1;
	setAttr -s 14 ".kix[13]"  1;
	setAttr -s 14 ".kiy[13]"  0;
	setAttr -s 14 ".kox[0:13]"  1 0.79178751712982554 0.48563590162916326 0.41842872836703254 0.4678158558814301 0.72249253924373502 0.90717328540395004 
		0.96996719286153676 1 0.53069450422411601 0.49894525271393092 0.74974207156162986 0.91948113430156808 1;
	setAttr -s 14 ".koy[0:13]"  0 0.61079663368210069 0.8741611813898108 0.90824963488963095 0.88382595853817569 0.69137871730126321 0.42075721057327525 
		0.24323578020577127 0 -0.84756317946588489 -0.86663350661870409 -0.6617301762278005 -0.39313412935473013 0;
createNode animCurveTU -n "CURVE20";
	rename -uid "B7197D80-0000-6BA2-657C-B40B00021CFF";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 13 ".ktv[0:12]"  1 0 3 0 6 0 8 0 10 0 12 0 13 0 15 0 18 0
		 20 0 22 0 24 0 25 0;
	setAttr -s 13 ".kit[12]"  1;
	setAttr -s 13 ".kot[0:12]"  1 18 18 18 18 18 18 18 
		18 18 18 18 1;
	setAttr -s 13 ".kix[12]"  1;
	setAttr -s 13 ".kiy[12]"  0;
	setAttr -s 13 ".kox[0:12]"  1 1 1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 13 ".koy[0:12]"  0 0 0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE21";
	rename -uid "B7197D80-0000-6BA2-657C-B40B00021CFD";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 14 ".ktv[0:13]"  1 25.5 3 49.202058087359966 6 0 8 0 10 0 12 0.90864917395458611 13 0
		 13.000000170068027 0 15 0 18 0 20 5.0553935860053958 22 11.847552335066473 24 19.548725193956308 25 25.5;
	setAttr -s 14 ".kit[13]"  1;
	setAttr -s 14 ".kot[0:13]"  1 18 18 18 18 18 18 18 
		18 18 18 18 18 1;
	setAttr -s 14 ".kix[13]"  0.0025405359341316765;
	setAttr -s 14 ".kiy[13]"  0.99999677283337651;
	setAttr -s 14 ".kox[0:13]"  0.0025405359341316765 1 1 1 1 1 1 1 1 1 0.014066211563838282 0.01149878111625705 
		0.0091554836193396653 0.0025405359341316765;
	setAttr -s 14 ".koy[0:13]"  0.99999677283337651 0 0 0 0 0 0 0 0 0 0.99990106595214767 0.99993388683094464 
		0.99995808768152672 0.99999677283337651;
createNode animCurveTU -n "CURVE22";
	rename -uid "B7197D80-0000-6BA2-657C-B40B00021D01";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 13 ".ktv[0:12]"  1 0 3 0 6 0 8 0 10 0 12 0 13 0 15 0 18 0
		 20 0 22 0 24 0 25 0;
	setAttr -s 13 ".kit[12]"  1;
	setAttr -s 13 ".kot[0:12]"  1 18 18 18 18 18 18 18 
		18 18 18 18 1;
	setAttr -s 13 ".kix[12]"  1;
	setAttr -s 13 ".kiy[12]"  0;
	setAttr -s 13 ".kox[0:12]"  1 1 1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 13 ".koy[0:12]"  0 0 0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE23";
	rename -uid "B7197D80-0000-6BA2-657C-B40B00021D00";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 13 ".ktv[0:12]"  1 0 3 0 6 0 8 0 10 0 12 0 13 0 15 0 18 0
		 20 0 22 0 24 0 25 0;
	setAttr -s 13 ".kit[12]"  1;
	setAttr -s 13 ".kot[0:12]"  1 18 18 18 18 18 18 18 
		18 18 18 18 1;
	setAttr -s 13 ".kix[12]"  1;
	setAttr -s 13 ".kiy[12]"  0;
	setAttr -s 13 ".kox[0:12]"  1 1 1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 13 ".koy[0:12]"  0 0 0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE24";
	rename -uid "B7197D80-0000-6BA2-657C-B40B00021D04";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 13 ".ktv[0:12]"  1 0 3 0 6 0 8 0 10 0 12 0 13 0 15 0 18 0
		 20 0 22 0 24 0 25 0;
	setAttr -s 13 ".kit[12]"  1;
	setAttr -s 13 ".kot[0:12]"  1 18 18 18 18 18 18 18 
		18 18 18 18 1;
	setAttr -s 13 ".kix[12]"  1;
	setAttr -s 13 ".kiy[12]"  0;
	setAttr -s 13 ".kox[0:12]"  1 1 1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 13 ".koy[0:12]"  0 0 0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE25";
	rename -uid "B7197D80-0000-6BA2-657C-B40B00021CFA";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 13 ".ktv[0:12]"  1 0 3 0 6 0 8 0 10 0 12 0 13 0 15 0 18 0
		 20 0 22 0 24 0 25 0;
	setAttr -s 13 ".kit[12]"  1;
	setAttr -s 13 ".kot[0:12]"  1 18 18 18 18 18 18 18 
		18 18 18 18 1;
	setAttr -s 13 ".kix[12]"  1;
	setAttr -s 13 ".kiy[12]"  0;
	setAttr -s 13 ".kox[0:12]"  1 1 1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 13 ".koy[0:12]"  0 0 0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE26";
	rename -uid "B7197D80-0000-6BA2-657C-B40B00021D10";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 13 ".ktv[0:12]"  1 1.0000000000000002 3 1.0000000000000002 6 1.0000000000000002 8 1.0000000000000002 10 1.0000000000000002
		 12 1.0000000000000002 13 1.0000000000000002 15 1.0000000000000002 18 1.0000000000000002 20 1.0000000000000002 22 1.0000000000000002 24 1.0000000000000002 25 1.0000000000000002;
	setAttr -s 13 ".kit[12]"  1;
	setAttr -s 13 ".kot[0:12]"  1 18 18 18 18 18 18 18 
		18 18 18 18 1;
	setAttr -s 13 ".kix[12]"  1;
	setAttr -s 13 ".kiy[12]"  0;
	setAttr -s 13 ".kox[0:12]"  1 1 1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 13 ".koy[0:12]"  0 0 0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE27";
	rename -uid "B7197D80-0000-6BA2-657C-B40B00021D11";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 13 ".ktv[0:12]"  1 1 3 1 6 1 8 1 10 1 12 1 13 1 15 1 18 1
		 20 1 22 1 24 1 25 1;
	setAttr -s 13 ".kit[12]"  1;
	setAttr -s 13 ".kot[0:12]"  1 18 18 18 18 18 18 18 
		18 18 18 18 1;
	setAttr -s 13 ".kix[12]"  1;
	setAttr -s 13 ".kiy[12]"  0;
	setAttr -s 13 ".kox[0:12]"  1 1 1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 13 ".koy[0:12]"  0 0 0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE28";
	rename -uid "B7197D80-0000-6BA2-657C-B40B00021D12";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 13 ".ktv[0:12]"  1 1.0000000000000002 3 1.0000000000000002 6 1.0000000000000002 8 1.0000000000000002 10 1.0000000000000002
		 12 1.0000000000000002 13 1.0000000000000002 15 1.0000000000000002 18 1.0000000000000002 20 1.0000000000000002 22 1.0000000000000002 24 1.0000000000000002 25 1.0000000000000002;
	setAttr -s 13 ".kit[12]"  1;
	setAttr -s 13 ".kot[0:12]"  1 18 18 18 18 18 18 18 
		18 18 18 18 1;
	setAttr -s 13 ".kix[12]"  1;
	setAttr -s 13 ".kiy[12]"  0;
	setAttr -s 13 ".kox[0:12]"  1 1 1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 13 ".koy[0:12]"  0 0 0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE29";
	rename -uid "B7197D80-0000-6BA2-657C-B40B00021D0D";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 13 ".ktv[0:12]"  1 0 3 0 6 0 8 0 10 0 12 0 13 0 15 0 18 0
		 20 0 22 0 24 0 25 0;
	setAttr -s 13 ".kit[12]"  1;
	setAttr -s 13 ".kot[0:12]"  1 18 18 18 18 18 18 18 
		18 18 18 18 1;
	setAttr -s 13 ".kix[12]"  1;
	setAttr -s 13 ".kiy[12]"  0;
	setAttr -s 13 ".kox[0:12]"  1 1 1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 13 ".koy[0:12]"  0 0 0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE30";
	rename -uid "B7197D80-0000-6BA2-657C-B40B00021D0E";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 13 ".ktv[0:12]"  1 0 3 0 6 0 8 0 10 0 12 0 13 0 15 0 18 0
		 20 0 22 0 24 0 25 0;
	setAttr -s 13 ".kit[12]"  1;
	setAttr -s 13 ".kot[0:12]"  1 18 18 18 18 18 18 18 
		18 18 18 18 1;
	setAttr -s 13 ".kix[12]"  1;
	setAttr -s 13 ".kiy[12]"  0;
	setAttr -s 13 ".kox[0:12]"  1 1 1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 13 ".koy[0:12]"  0 0 0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE31";
	rename -uid "B7197D80-0000-6BA2-657C-B40B00021D0F";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 13 ".ktv[0:12]"  1 0 3 0 6 0 8 0 10 0 12 0 13 0 15 0 18 0
		 20 0 22 0 24 0 25 0;
	setAttr -s 13 ".kit[12]"  1;
	setAttr -s 13 ".kot[0:12]"  1 18 18 18 18 18 18 18 
		18 18 18 18 1;
	setAttr -s 13 ".kix[12]"  1;
	setAttr -s 13 ".kiy[12]"  0;
	setAttr -s 13 ".kox[0:12]"  1 1 1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 13 ".koy[0:12]"  0 0 0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE32";
	rename -uid "B7197D80-0000-6BA2-657C-B40B00021CFB";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 13 ".ktv[0:12]"  1 45 3 45 6 45 8 45 10 45 12 45 13 45 15 45
		 18 45 20 45 22 45 24 45 25 45;
	setAttr -s 13 ".kit[12]"  1;
	setAttr -s 13 ".kot[0:12]"  1 18 18 18 18 18 18 18 
		18 18 18 18 1;
	setAttr -s 13 ".kix[12]"  1;
	setAttr -s 13 ".kiy[12]"  0;
	setAttr -s 13 ".kox[0:12]"  1 1 1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 13 ".koy[0:12]"  0 0 0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE33";
	rename -uid "B7197D80-0000-6BA2-657C-B40B00021D07";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 13 ".ktv[0:12]"  1 0 3 0 6 0 8 0 10 0 12 0 13 0 15 0 18 0
		 20 0 22 0 24 0 25 0;
	setAttr -s 13 ".kit[12]"  1;
	setAttr -s 13 ".kot[0:12]"  1 18 18 18 18 18 18 18 
		18 18 18 18 1;
	setAttr -s 13 ".kix[12]"  1;
	setAttr -s 13 ".kiy[12]"  0;
	setAttr -s 13 ".kox[0:12]"  1 1 1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 13 ".koy[0:12]"  0 0 0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE34";
	rename -uid "B7197D80-0000-6BA2-657C-B40B00021D0A";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 13 ".ktv[0:12]"  1 -3.9611037234042552 3 -3.9611037234042552 6 -3.9611037234042552 8 -3.9611037234042552 10 -3.9611037234042552
		 12 -3.9611037234042552 13 -3.9611037234042552 15 -3.9611037234042552 18 -3.9611037234042552 20 -3.9611037234042552 22 -3.9611037234042552 24 -3.9611037234042552 25 -3.9611037234042552;
	setAttr -s 13 ".kit[12]"  1;
	setAttr -s 13 ".kot[0:12]"  1 18 18 18 18 18 18 18 
		18 18 18 18 1;
	setAttr -s 13 ".kix[12]"  1;
	setAttr -s 13 ".kiy[12]"  0;
	setAttr -s 13 ".kox[0:12]"  1 1 1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 13 ".koy[0:12]"  0 0 0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE35";
	rename -uid "B7197D80-0000-6BA2-657C-B40B00021D0B";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 14 ".ktv[0:13]"  1 -0.33631908556432782 3 3.5630800421865256 6 26.880096110186852 8 12.19384740163329 10 3.41764697949659
		 12 0.45695639303020297 13 -0.33631908556432782 15 -0.33631908556432782 15.000000170068027 -0.33631908556432782 17 -0.33631908556432782 20 -0.33631908556432782 22 -0.33631908556432782 24 -0.33631908556432782
		 25 -0.33631908556432782;
	setAttr -s 14 ".kit[13]"  1;
	setAttr -s 14 ".kot[0:13]"  1 18 18 18 18 18 18 18 
		18 18 18 18 18 1;
	setAttr -s 14 ".kix[13]"  1;
	setAttr -s 14 ".kiy[13]"  0;
	setAttr -s 14 ".kox[0:13]"  1 0.0076544698677573067 1 0.0071033701922140272 0.014198808286163154 0.033279672117954247 1 1 1 1 
		1 1 1 1;
	setAttr -s 14 ".koy[0:13]"  0 0.99997070411639744 0 -0.99997477074769858 -0.99989919184048381 -0.99944607829723431 0 0 0 0 
		0 0 0 0;
createNode animCurveTL -n "CURVE36";
	rename -uid "B7197D80-0000-6BA2-657C-B40B00021D0C";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 13 ".ktv[0:12]"  1 -34.711331349843725 3 -46.645403666604373 4 -49.410843550997441 5 -44.684102621560989 6 -31.099248719040389
		 8 5.7256823731851458 10 32.997175028526485 12 39.777488554075717 12.999999829931973 36.893102550718353 13 36.893102550718105 15 24.95903023395746 24 -28.744295191463912 25 -34.711331349843725;
	setAttr -s 13 ".kit[0:12]"  2 18 18 18 18 18 18 18 
		2 2 2 2 1;
	setAttr -s 13 ".kot[0:12]"  1 18 18 18 18 18 18 18 
		2 2 2 2 18;
	setAttr -s 13 ".kix[12]"  0.0069826375729593639;
	setAttr -s 13 ".kiy[12]"  -0.99997562108909677;
	setAttr -s 13 ".kox[0:12]"  0.0069826375729593621 0.0085033760981317996 1 0.0045508035310266705 0.0024796696854554679 0.0026002402861763228 0.0048944443496054544 
		1 0.99999999938416606 0.0069826375729591687 0.0069826375729593656 0.0069826375729597758 1;
	setAttr -s 13 ".koy[0:12]"  -0.99997562108909654 -0.99996384564389806 0 0.99998964503999843 0.99999692561439957 0.9999966193695129 0.99998802213551963 
		0 -3.5095126965168978e-05 -0.99997562108909654 -0.99997562108909677 -0.99997562108909677 0;
createNode animCurveTU -n "CURVE37";
	rename -uid "B7197D80-0000-6BA2-657C-B40B00021CFE";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 14 ".ktv[0:13]"  1 0 3 9.256077348066281 6 59.100000000000009 8 26.827696793004169 10 -8.9616887140989228
		 12 -27.7659485584274 13 -16.264052943330874 14 0 15 0 18 0 20 0 22 0 24 0 25 0;
	setAttr -s 14 ".kit[13]"  1;
	setAttr -s 14 ".kot[0:13]"  1 18 18 18 18 18 18 18 
		18 18 18 18 18 1;
	setAttr -s 14 ".kix[13]"  1;
	setAttr -s 14 ".kiy[13]"  0;
	setAttr -s 14 ".kox[0:13]"  1 0.0035250768009640167 1 0.002448751568115381 0.0030528441348295268 1 0.003001264582800756 1 1 1 
		1 1 1 1;
	setAttr -s 14 ".koy[0:13]"  0 0.9999937868974722 0 -0.99999700180338424 -0.99999534006048674 0 0.99999549619530992 0 0 0 
		0 0 0 0;
createNode animCurveTU -n "CURVE38";
	rename -uid "B7197D80-0000-6BA2-657C-B40B00021D03";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 13 ".ktv[0:12]"  1 0 3 0 6 0 8 0 10 0 12 0 13 0 15 0 18 0
		 20 0 22 0 24 0 25 0;
	setAttr -s 13 ".kit[12]"  1;
	setAttr -s 13 ".kot[0:12]"  1 18 18 18 18 18 18 18 
		18 18 18 18 1;
	setAttr -s 13 ".kix[12]"  1;
	setAttr -s 13 ".kiy[12]"  0;
	setAttr -s 13 ".kox[0:12]"  1 1 1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 13 ".koy[0:12]"  0 0 0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE39";
	rename -uid "B7197D80-0000-6BA2-657C-B40B00021D02";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 13 ".ktv[0:12]"  1 0 3 0 6 0 8 0 10 0 12 0 13 0 15 0 18 0
		 20 0 22 0 24 0 25 0;
	setAttr -s 13 ".kit[12]"  1;
	setAttr -s 13 ".kot[0:12]"  1 18 18 18 18 18 18 18 
		18 18 18 18 1;
	setAttr -s 13 ".kix[12]"  1;
	setAttr -s 13 ".kiy[12]"  0;
	setAttr -s 13 ".kox[0:12]"  1 1 1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 13 ".koy[0:12]"  0 0 0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE40";
	rename -uid "B7197D80-0000-6BA2-657C-B40B00021D05";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 13 ".ktv[0:12]"  1 0 3 0 6 0 8 0 10 0 12 0 13 0 15 0 18 0
		 20 0 22 0 24 0 25 0;
	setAttr -s 13 ".kit[12]"  1;
	setAttr -s 13 ".kot[0:12]"  1 18 18 18 18 18 18 18 
		18 18 18 18 1;
	setAttr -s 13 ".kix[12]"  1;
	setAttr -s 13 ".kiy[12]"  0;
	setAttr -s 13 ".kox[0:12]"  1 1 1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 13 ".koy[0:12]"  0 0 0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE41";
	rename -uid "B7197D80-0000-6BA2-657C-B40B00021D06";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 13 ".ktv[0:12]"  1 0 3 0 6 0 8 0 10 0 12 0 13 0 15 0 18 0
		 20 0 22 0 24 0 25 0;
	setAttr -s 13 ".kit[12]"  1;
	setAttr -s 13 ".kot[0:12]"  1 18 18 18 18 18 18 18 
		18 18 18 18 1;
	setAttr -s 13 ".kix[12]"  1;
	setAttr -s 13 ".kiy[12]"  0;
	setAttr -s 13 ".kox[0:12]"  1 1 1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 13 ".koy[0:12]"  0 0 0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE42";
	rename -uid "B7197D80-0000-6BA2-657C-B40B00021D08";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 13 ".ktv[0:12]"  1 0 3 0 6 0 8 0 10 0 12 0 13 0 15 0 18 0
		 20 0 22 0 24 0 25 0;
	setAttr -s 13 ".kit[12]"  1;
	setAttr -s 13 ".kot[0:12]"  1 18 18 18 18 18 18 18 
		18 18 18 18 1;
	setAttr -s 13 ".kix[12]"  1;
	setAttr -s 13 ".kiy[12]"  0;
	setAttr -s 13 ".kox[0:12]"  1 1 1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 13 ".koy[0:12]"  0 0 0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE43";
	rename -uid "B7197D80-0000-6BA2-657C-B40B00021CFC";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 13 ".ktv[0:12]"  1 90 3 90 6 90 8 90 10 90 12 90 13 90 15 90
		 18 90 20 90 22 90 24 90 25 90;
	setAttr -s 13 ".kit[12]"  1;
	setAttr -s 13 ".kot[0:12]"  1 18 18 18 18 18 18 18 
		18 18 18 18 1;
	setAttr -s 13 ".kix[12]"  1;
	setAttr -s 13 ".kiy[12]"  0;
	setAttr -s 13 ".kox[0:12]"  1 1 1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 13 ".koy[0:12]"  0 0 0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE44";
	rename -uid "B7197D80-0000-6BA2-657C-B40B00021D09";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 13 ".ktv[0:12]"  1 0 3 0 6 0 8 0 10 0 12 0 13 0 15 0 18 0
		 20 0 22 0 24 0 25 0;
	setAttr -s 13 ".kit[12]"  1;
	setAttr -s 13 ".kot[0:12]"  1 18 18 18 18 18 18 18 
		18 18 18 18 1;
	setAttr -s 13 ".kix[12]"  1;
	setAttr -s 13 ".kiy[12]"  0;
	setAttr -s 13 ".kox[0:12]"  1 1 1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 13 ".koy[0:12]"  0 0 0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE46";
	rename -uid "B7197D80-0000-6BA2-657C-B40B00021D14";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE47";
	rename -uid "B7197D80-0000-6BA2-657C-B40B00021D15";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE48";
	rename -uid "B7197D80-0000-6BA2-657C-B40B00021D16";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE49";
	rename -uid "B7197D80-0000-6BA2-657C-B40B00021D17";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE50";
	rename -uid "B7197D80-0000-6BA2-657C-B40B00021D1B";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1.0000000000000002 3 1.0000000000000002 6 1.0000000000000002 8 1.0000000000000002 10 1.0000000000000002
		 13 1.0000000000000002 15 1.0000000000000002 18 1.0000000000000002 20 1.0000000000000002 22 1.0000000000000002 25 1.0000000000000002;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE51";
	rename -uid "B7197D80-0000-6BA2-657C-B40B00021D1C";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1 3 1 6 1 8 1 10 1 13 1 15 1 18 1 20 1
		 22 1 25 1;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE52";
	rename -uid "B7197D80-0000-6BA2-657C-B40B00021D1D";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1 3 1 6 1 8 1 10 1 13 1 15 1 18 1 20 1
		 22 1 25 1;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE53";
	rename -uid "B7197D80-0000-6BA2-657C-B40B00021D18";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE54";
	rename -uid "B7197D80-0000-6BA2-657C-B40B00021D19";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 9.565175890006417 3 9.565175890006417 6 9.565175890006417 8 9.565175890006417 10 9.565175890006417
		 13 9.565175890006417 15 9.565175890006417 18 9.565175890006417 20 9.565175890006417 22 9.565175890006417 25 9.565175890006417;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE55";
	rename -uid "B7197D80-0000-6BA2-657C-B40B00021D1A";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE57";
	rename -uid "B7197D80-0000-6BA2-657C-B40B00021D1F";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE58";
	rename -uid "B7197D80-0000-6BA2-657C-B40B00021D20";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE59";
	rename -uid "B7197D80-0000-6BA2-657C-B40B00021D21";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE60";
	rename -uid "B7197D80-0000-6BA2-657C-B40B00021D22";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE61";
	rename -uid "B7197D80-0000-6BA2-657C-B40B00021D26";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0.99999999999999956 3 0.99999999999999956 6 0.99999999999999956 8 0.99999999999999956 10 0.99999999999999956
		 13 0.99999999999999956 15 0.99999999999999956 18 0.99999999999999956 20 0.99999999999999956 22 0.99999999999999956 25 0.99999999999999956;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE62";
	rename -uid "B7197D80-0000-6BA2-657C-B40B00021D27";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1 3 1 6 1 8 1 10 1 13 1 15 1 18 1 20 1
		 22 1 25 1;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE63";
	rename -uid "B7197D80-0000-6BA2-657C-B40B00021D28";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1 3 1 6 1 8 1 10 1 13 1 15 1 18 1 20 1
		 22 1 25 1;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE64";
	rename -uid "B7197D80-0000-6BA2-657C-B40B00021D23";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE65";
	rename -uid "B7197D80-0000-6BA2-657C-B40B00021D24";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE66";
	rename -uid "B7197D80-0000-6BA2-657C-B40B00021D25";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 -16.004111880308876 3 -16.004111880308876 6 -16.004111880308876 8 -16.004111880308876 10 -16.004111880308876
		 13 -16.004111880308876 15 -16.004111880308876 18 -16.004111880308876 20 -16.004111880308876 22 -16.004111880308876 25 -16.004111880308876;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE68";
	rename -uid "B7197D80-0000-6BA2-657C-B40B00021D2A";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 12 ".ktv[0:11]"  1 0 3 0 6 0 8 0 10 0 12.999999829931973 0 13 0 15 0
		 18 0 20 0 22 0 25 0;
	setAttr -s 12 ".kit[11]"  1;
	setAttr -s 12 ".kot[0:11]"  1 18 18 18 18 18 18 18 
		18 18 18 1;
	setAttr -s 12 ".kix[11]"  1;
	setAttr -s 12 ".kiy[11]"  0;
	setAttr -s 12 ".kox[0:11]"  1 1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 12 ".koy[0:11]"  0 0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE69";
	rename -uid "B7197D80-0000-6BA2-657C-B40B00021D2B";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 12 ".ktv[0:11]"  1 0 3 0 6 0 8 0 10 0 12.999999829931973 0 13 0 15 0
		 18 0 20 0 22 0 25 0;
	setAttr -s 12 ".kit[11]"  1;
	setAttr -s 12 ".kot[0:11]"  1 18 18 18 18 18 18 18 
		18 18 18 1;
	setAttr -s 12 ".kix[11]"  1;
	setAttr -s 12 ".kiy[11]"  0;
	setAttr -s 12 ".kox[0:11]"  1 1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 12 ".koy[0:11]"  0 0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE70";
	rename -uid "B7197D80-0000-6BA2-657C-B40B00021D2C";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 12 ".ktv[0:11]"  1 0 3 0 6 0 8 0 10 0 12.999999829931973 0 13 0 15 0
		 18 0 20 0 22 0 25 0;
	setAttr -s 12 ".kit[11]"  1;
	setAttr -s 12 ".kot[0:11]"  1 18 18 18 18 18 18 18 
		18 18 18 1;
	setAttr -s 12 ".kix[11]"  1;
	setAttr -s 12 ".kiy[11]"  0;
	setAttr -s 12 ".kox[0:11]"  1 1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 12 ".koy[0:11]"  0 0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE71";
	rename -uid "B7197D80-0000-6BA2-657C-B40B00021D2D";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 12 ".ktv[0:11]"  1 0 3 0 6 0 8 0 10 0 12.999999829931973 0 13 0 15 0
		 18 0 20 0 22 0 25 0;
	setAttr -s 12 ".kit[11]"  1;
	setAttr -s 12 ".kot[0:11]"  1 18 18 18 18 18 18 18 
		18 18 18 1;
	setAttr -s 12 ".kix[11]"  1;
	setAttr -s 12 ".kiy[11]"  0;
	setAttr -s 12 ".kox[0:11]"  1 1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 12 ".koy[0:11]"  0 0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE72";
	rename -uid "B7197D80-0000-6BA2-657C-B40B00021D2E";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 12 ".ktv[0:11]"  1 0 3 0 6 0 8 0 10 0 12.999999829931973 0 13 0 15 0
		 18 0 20 0 22 0 25 0;
	setAttr -s 12 ".kit[11]"  1;
	setAttr -s 12 ".kot[0:11]"  1 18 18 18 18 18 18 18 
		18 18 18 1;
	setAttr -s 12 ".kix[11]"  1;
	setAttr -s 12 ".kiy[11]"  0;
	setAttr -s 12 ".kox[0:11]"  1 1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 12 ".koy[0:11]"  0 0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE73";
	rename -uid "B7197D80-0000-6BA2-657C-B40B00021D2F";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 12 ".ktv[0:11]"  1 0 3 0 6 0 8 0 10 0 12.999999829931973 0 13 0 15 0
		 18 0 20 0 22 0 25 0;
	setAttr -s 12 ".kit[11]"  1;
	setAttr -s 12 ".kot[0:11]"  1 18 18 18 18 18 18 18 
		18 18 18 1;
	setAttr -s 12 ".kix[11]"  1;
	setAttr -s 12 ".kiy[11]"  0;
	setAttr -s 12 ".kox[0:11]"  1 1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 12 ".koy[0:11]"  0 0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE74";
	rename -uid "B7197D80-0000-6BA2-657C-B40B00021D30";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 12 ".ktv[0:11]"  1 -18.380712912870933 3 -21.176494380670352 6 -23.743540134295163 8 -18.150471490102031 10 -14.81968867815015
		 12.999999829931973 -9.6696395251405178 13 -9.6696392331877377 15 -5.0559828573291874 18 5.1566769867447446 20 2.3355936742608812 22 -9.5963427663786565 25 -18.380712912870933;
	setAttr -s 12 ".kit[11]"  1;
	setAttr -s 12 ".kot[0:11]"  1 18 18 18 18 18 18 18 
		18 18 18 1;
	setAttr -s 12 ".kix[11]"  0.49472294142197659;
	setAttr -s 12 ".kiy[11]"  -0.8690507529660092;
	setAttr -s 12 ".kox[0:11]"  1 0.91216876417772208 1 0.730628647892831 0.81519494740001819 0.81188739411218924 0.71912662647103442 
		0.62711283484298941 1 0.54338062391927067 0.49924870507984442 1;
	setAttr -s 12 ".koy[0:11]"  0 -0.40981476993696486 0 0.68277505730532773 0.57918666916071315 0.58381406225074672 0.69487905069903289 
		0.77892842570751608 0 -0.83948644869890787 -0.86645872981700556 0;
createNode animCurveTU -n "CURVE76";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021D32";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0 20 0 25 0;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTL -n "CURVE77";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021D33";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0 20 -7.1054273576010019e-15 25 0;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTL -n "CURVE78";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021D34";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0 20 1.4210854715202004e-14 25 0;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTL -n "CURVE79";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021D35";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 3.5527136788005009e-15 20 -3.5527136788005009e-15 25 3.5527136788005009e-15;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTU -n "CURVE80";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021D39";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0.99999999999999967 20 1 25 0.99999999999999967;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTU -n "CURVE81";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021D3A";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 1 20 0.99999999999999956 25 1;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTU -n "CURVE82";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021D3B";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 1 20 0.99999999999999967 25 1;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTA -n "CURVE83";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021D36";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0 20 0 25 0;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTA -n "CURVE84";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021D37";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0 20 0 25 0;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTA -n "CURVE85";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021D38";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 -89.290444184297073 20 -89.290444184297073 25 -89.290444184297073;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTU -n "CURVE87";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021D3D";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE88";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021D41";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE89";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021D42";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE90";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021D43";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE91";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021D44";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1 3 1 6 1 8 1 10 1 13 1 15 1 18 1 20 1
		 22 1 25 1;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE92";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021D45";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1 3 1 6 1 8 1 10 1 13 1 15 1 18 1 20 1
		 22 1 25 1;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE93";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021D46";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1 3 1 6 1 8 1 10 1 13 1 15 1 18 1 20 1
		 22 1 25 1;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE94";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021D3E";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 -1.3841759021686419 2 -0.47776970116336731 2.9999998299319728 0.81141814305901716 3 0.81112765504921946
		 4 2.1943266393928065 5 2.6571399508654516 6 2.3378287408094707 7 1.5034521849696394 8 0.29139498690860693 10 -1.2575339566081607 12 -1.6995231976120571 13 -1.412503421175535 14 -0.5344904943906289
		 15 0.81112765504921946 16 2.1466143104122009 17 2.6571399508654516 18 2.3378702704179819 19 1.5035698521937593 20 0.29155418374124104 22 -1.2575339566081607 24 -1.6995231976120571 25 -1.3841759021686419;
	setAttr -s 22 ".kit[21]"  1;
	setAttr -s 22 ".kot[0:21]"  1 18 18 18 18 18 18 18 
		18 18 18 18 18 18 18 18 18 18 18 18 18 1;
	setAttr -s 22 ".kix[21]"  1;
	setAttr -s 22 ".kiy[21]"  0;
	setAttr -s 22 ".kox[0:21]"  1 0.90854419363369032 1 1 0.93271524375197246 1 0.97202708910276403 0.91913416255115199 0.93306677418823292 
		0.9789500862736924 1 0.97149764770681146 0.9065130417302284 0.8719369703114902 0.93271524375197257 1 0.97203255772148278 0.91914236418691064 0.93306162903539025 0.97894682534041899 1 1;
	setAttr -s 22 ".koy[0:21]"  0 0.41778876027785583 0 0 0.36061374637234556 0 -0.23486876772020354 -0.39394465503594833 -0.35970320391395599 
		-0.20409980055044197 0 0.23704919426172297 0.42217781226991224 0.48961813671883081 0.3606137463723455 0 -0.23484613415901082 -0.39392551879371379 -0.35971655010830933 -0.20411544075820198 0 0;
createNode animCurveTA -n "CURVE95";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021D3F";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 7 ".ktv[0:6]"  1 11.754110833333334 3 9.2601083333333349 10 -8.197905 13 -11.7543025
		 15 -9.2602966666666671 22 8.1977450000000012 25 11.754110833333334;
	setAttr -s 7 ".kit[6]"  1;
	setAttr -s 7 ".kot[0:6]"  1 18 18 18 18 18 1;
	setAttr -s 7 ".kix[6]"  1;
	setAttr -s 7 ".kiy[6]"  0;
	setAttr -s 7 ".kox[0:6]"  1 0.73277976953723334 0.75062059876416576 1 0.73277923101751541 0.75062065074396855 1;
	setAttr -s 7 ".koy[0:6]"  0 -0.68046587670283598 -0.66073346873828431 0 0.68046645662323346 0.66073340968706973 0;
createNode animCurveTA -n "CURVE96";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021D40";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 5 ".ktv[0:4]"  1 0 6 -7.0119538461538458 13 0 18 7.0123076923076928 25 0;
	setAttr -s 5 ".kit[4]"  1;
	setAttr -s 5 ".kot[0:4]"  1 18 18 18 1;
	setAttr -s 5 ".kix[4]"  1;
	setAttr -s 5 ".kiy[4]"  0;
	setAttr -s 5 ".kox[0:4]"  1 1 0.89815381474866474 1 1;
	setAttr -s 5 ".koy[0:4]"  0 0 0.43968139038674503 0 0;
createNode animCurveTU -n "CURVE98";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021D48";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE99";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021D49";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE100";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021D4A";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE101";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021D4B";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE102";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021D4F";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1 3 1 6 1 8 1 10 1 13 1 15 1 18 1 20 1
		 22 1 25 1;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE103";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021D50";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0.99999999999999989 3 0.99999999999999989 6 0.99999999999999989 8 0.99999999999999989 10 0.99999999999999989
		 13 0.99999999999999989 15 0.99999999999999989 18 0.99999999999999989 20 0.99999999999999989 22 0.99999999999999989 25 0.99999999999999989;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE104";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021D51";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0.99999999999999989 3 0.99999999999999989 6 0.99999999999999989 8 0.99999999999999989 10 0.99999999999999989
		 13 0.99999999999999989 15 0.99999999999999989 18 0.99999999999999989 20 0.99999999999999989 22 0.99999999999999989 25 0.99999999999999989;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE105";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021D4C";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 0.83495504376705154 2 0.45426449784903794 2.9999998299319728 -0.087194499014311505 3 -0.087072699006052828
		 4 -0.66801631855761123 5 -0.86239779179140863 6 -0.72828716266094495 7 -0.37784879880254851 8 0.1312151758553303 10 0.78176540014581675 12 0.96740079278416702 13 0.84685238457704215 14 0.47808689947090477
		 15 -0.087072699006052828 16 -0.64797685719329301 17 -0.86239779179140863 18 -0.72830438266211794 19 -0.37789835880592249 20 0.13114839585078375 22 0.78176540014581675 24 0.96740079278416702 25 0.83495504376705154;
	setAttr -s 22 ".kit[21]"  1;
	setAttr -s 22 ".kot[0:21]"  1 18 18 18 18 18 18 18 
		18 18 18 18 18 18 18 18 18 18 18 18 18 1;
	setAttr -s 22 ".kix[21]"  0.9942745399584243;
	setAttr -s 22 ".kiy[21]"  -0.10685569329925211;
	setAttr -s 22 ".kox[0:21]"  1 0.98185557419180758 1 1 0.98707090156975241 1 0.99488996618815639 0.98418096468423777 0.98714436074120104 
		0.99618807940485632 1 0.99478975910945555 0.98140215221519 0.97329809547121582 0.98707090156975241 1 0.99489100345350812 0.98418274586976595 0.98714328296116061 0.99618747399799212 1 1;
	setAttr -s 22 ".koy[0:21]"  0 -0.18963024924435409 0 0 -0.16028423276877884 0 0.10096511862088284 0.17716610497835938 0.15983119550590053 
		0.087231361629081725 0 -0.10194770802206127 -0.19196305797572885 -0.22954480467243049 -0.16028423276877879 0 0.10095489709405757 0.17715620997370513 0.15983785191456465 0.087238275140557625 0 0;
createNode animCurveTA -n "CURVE106";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021D4D";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE107";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021D4E";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE109";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021D53";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE110";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021D54";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE111";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021D55";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE112";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021D56";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE113";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021D5A";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1 3 1 6 1 8 1 10 1 13 1 15 1 18 1 20 1
		 22 1 25 1;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE114";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021D5B";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0.99999999999999978 3 0.99999999999999978 6 0.99999999999999978 8 0.99999999999999978 10 0.99999999999999978
		 13 0.99999999999999978 15 0.99999999999999978 18 0.99999999999999978 20 0.99999999999999978 22 0.99999999999999978 25 0.99999999999999978;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE115";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021D5C";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0.99999999999999989 3 0.99999999999999989 6 0.99999999999999989 8 0.99999999999999989 10 0.99999999999999989
		 13 0.99999999999999989 15 0.99999999999999989 18 0.99999999999999989 20 0.99999999999999989 22 0.99999999999999989 25 0.99999999999999989;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE116";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021D57";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE117";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021D58";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 -2.574738921613474 3 -2.574738921613474 6 -2.574738921613474 8 -2.574738921613474 10 -2.574738921613474
		 13 -2.574738921613474 15 -2.574738921613474 18 -2.574738921613474 20 -2.574738921613474 22 -2.574738921613474 25 -2.574738921613474;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE118";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021D59";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE120";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021D5E";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE121";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021D5F";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE122";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021D60";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE123";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021D61";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE124";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021D65";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1.0000000000000002 3 1.0000000000000002 6 1.0000000000000002 8 1.0000000000000002 10 1.0000000000000002
		 13 1.0000000000000002 15 1.0000000000000002 18 1.0000000000000002 20 1.0000000000000002 22 1.0000000000000002 25 1.0000000000000002;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE125";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021D66";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1.0000000000000002 3 1.0000000000000002 6 1.0000000000000002 8 1.0000000000000002 10 1.0000000000000002
		 13 1.0000000000000002 15 1.0000000000000002 18 1.0000000000000002 20 1.0000000000000002 22 1.0000000000000002 25 1.0000000000000002;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE126";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021D67";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1.0000000000000004 3 1.0000000000000004 6 1.0000000000000004 8 1.0000000000000004 10 1.0000000000000004
		 13 1.0000000000000004 15 1.0000000000000004 18 1.0000000000000004 20 1.0000000000000004 22 1.0000000000000004 25 1.0000000000000004;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE127";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021D62";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE128";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021D63";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE129";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021D64";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 -24.183597580285252 3 -24.183597580285252 6 -24.183597580285252 8 -24.183597580285252 10 -24.183597580285252
		 13 -24.183597580285252 15 -24.183597580285252 18 -24.183597580285252 20 -24.183597580285252 22 -24.183597580285252 25 -24.183597580285252;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE131";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021D69";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 4 ".ktv[0:3]"  1 0 13 0 18 0 25 0;
	setAttr -s 4 ".kit[2:3]"  9 1;
	setAttr -s 4 ".kot[0:3]"  1 18 5 1;
	setAttr -s 4 ".kix[3]"  1;
	setAttr -s 4 ".kiy[3]"  0;
	setAttr -s 4 ".kox[0:3]"  1 1 0 1;
	setAttr -s 4 ".koy[0:3]"  0 0 0 0;
createNode animCurveTL -n "CURVE132";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021D6B";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 20 ".ktv[0:19]"  1 0 2 1.6011592009422193 3 1.1732534802508487 4 0.28813300258538427 5 -0.22253157008110752
		 6 0 8 0 9 -0.16864269047186345 10 -0.084321345235931724 11 0.98829199735743223 12 1.1605653525823956 12.999999829931973 0.45078022929093031 13 0.45078022929086853 14 0 15 0.39712212807965575
		 17 0 18 0 20 0 24 0 25 0;
	setAttr -s 20 ".kit[19]"  1;
	setAttr -s 20 ".kot[0:19]"  1 18 18 18 18 18 18 18 
		18 18 18 18 18 18 18 18 18 18 18 1;
	setAttr -s 20 ".kix[19]"  1;
	setAttr -s 20 ".kiy[19]"  0;
	setAttr -s 20 ".kox[0:19]"  1 1 0.063339181615325979 0.059597434248727321 1 1 1 1 0.16252386276348571 0.080360484933234264 
		1 0.99999999965790998 0.99999999965790998 1 1 1 1 1 1 1;
	setAttr -s 20 ".koy[0:19]"  0 0 -0.99799205812085534 -0.99822249315018374 0 0 0 0 0.98670461336330839 0.99676586642064302 
		0 -2.615683682338778e-05 -2.6156836823387777e-05 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE133";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021D6A";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 23 ".ktv[0:22]"  1 1.7683662182556583 2 -1.942088624456346 3 -1.0820322175046384 4 0.37505662640867354 5 0.54676043120328655
		 6 0 8 -0.38491431180819946 9 -0.9899207788411053 10 2.1374413178449503 11 7.2904117321438742 12 5.6046804293273409 12.999999829931973 4.9040857040112442 13 4.9040857040112176 14 -0.40686592116282611
		 15 -2.1893205428798845 16 -1.8604807621657491 17 -0.91524903313619976 18 3.4274125923953651 19 1.7493228333280919 20 2.6730049926483108 22 2.2377101397927706 24 3.6566032299909668 25 1.7683662182556583;
	setAttr -s 23 ".kit[22]"  1;
	setAttr -s 23 ".kot[0:22]"  1 18 18 18 18 18 18 18 
		18 18 18 18 18 18 18 18 18 18 18 18 18 18 1;
	setAttr -s 23 ".kix[22]"  1;
	setAttr -s 23 ".kiy[22]"  0;
	setAttr -s 23 ".kox[0:22]"  1 1 0.035940558360756464 0.080625314920488869 1 0.13297550088185164 0.1252779148260387 1 0.010063498460465224 
		1 0.034899908753238083 0.99999999993637434 0.99999999993637423 0.01174718892203497 1 0.065267646958824713 0.015757312329690097 1 1 1 1 1 1;
	setAttr -s 23 ".koy[0:22]"  0 0 0.99935392942876689 0.99674448009205063 0 -0.99111932488738241 -0.992121688129455 0 0.99994936171725013 
		0 -0.99939081262988194 -1.1280576530747829e-05 -1.1280576530747827e-05 -0.99993099939567343 0 0.99786779397897107 0.99987584584694555 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE134";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021D6C";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 4 ".ktv[0:3]"  1 0 13 0 18 0 25 0;
	setAttr -s 4 ".kit[3]"  1;
	setAttr -s 4 ".kot[0:3]"  1 18 18 1;
	setAttr -s 4 ".kix[3]"  1;
	setAttr -s 4 ".kiy[3]"  0;
	setAttr -s 4 ".kox[0:3]"  1 1 1 1;
	setAttr -s 4 ".koy[0:3]"  0 0 0 0;
createNode animCurveTU -n "CURVE135";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021D70";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 4 ".ktv[0:3]"  1 1 13 1 18 1 25 1;
	setAttr -s 4 ".kit[3]"  1;
	setAttr -s 4 ".kot[0:3]"  1 18 18 1;
	setAttr -s 4 ".kix[3]"  1;
	setAttr -s 4 ".kiy[3]"  0;
	setAttr -s 4 ".kox[0:3]"  1 1 1 1;
	setAttr -s 4 ".koy[0:3]"  0 0 0 0;
createNode animCurveTU -n "CURVE136";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021D71";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 4 ".ktv[0:3]"  1 1 13 1 18 1 25 1;
	setAttr -s 4 ".kit[3]"  1;
	setAttr -s 4 ".kot[0:3]"  1 18 18 1;
	setAttr -s 4 ".kix[3]"  1;
	setAttr -s 4 ".kiy[3]"  0;
	setAttr -s 4 ".kox[0:3]"  1 1 1 1;
	setAttr -s 4 ".koy[0:3]"  0 0 0 0;
createNode animCurveTU -n "CURVE137";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021D72";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 4 ".ktv[0:3]"  1 1 13 1 18 1 25 1;
	setAttr -s 4 ".kit[3]"  1;
	setAttr -s 4 ".kot[0:3]"  1 18 18 1;
	setAttr -s 4 ".kix[3]"  1;
	setAttr -s 4 ".kiy[3]"  0;
	setAttr -s 4 ".kox[0:3]"  1 1 1 1;
	setAttr -s 4 ".koy[0:3]"  0 0 0 0;
createNode animCurveTA -n "CURVE138";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021D6D";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 4 ".ktv[0:3]"  1 0 13 0 18 0 25 0;
	setAttr -s 4 ".kit[3]"  1;
	setAttr -s 4 ".kot[0:3]"  1 18 18 1;
	setAttr -s 4 ".kix[3]"  1;
	setAttr -s 4 ".kiy[3]"  0;
	setAttr -s 4 ".kox[0:3]"  1 1 1 1;
	setAttr -s 4 ".koy[0:3]"  0 0 0 0;
createNode animCurveTA -n "CURVE139";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021D6E";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 4 ".ktv[0:3]"  1 0 13 0 18 0 25 0;
	setAttr -s 4 ".kit[3]"  1;
	setAttr -s 4 ".kot[0:3]"  1 18 18 1;
	setAttr -s 4 ".kix[3]"  1;
	setAttr -s 4 ".kiy[3]"  0;
	setAttr -s 4 ".kox[0:3]"  1 1 1 1;
	setAttr -s 4 ".koy[0:3]"  0 0 0 0;
createNode animCurveTA -n "CURVE140";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021D6F";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 4 ".ktv[0:3]"  1 0 13 0 18 0 25 0;
	setAttr -s 4 ".kit[3]"  1;
	setAttr -s 4 ".kot[0:3]"  1 18 18 1;
	setAttr -s 4 ".kix[3]"  1;
	setAttr -s 4 ".kiy[3]"  0;
	setAttr -s 4 ".kox[0:3]"  1 1 1 1;
	setAttr -s 4 ".koy[0:3]"  0 0 0 0;
createNode animCurveTU -n "CURVE142";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021D74";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE143";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021D75";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE144";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021D76";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE145";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021D77";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE146";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021D7B";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0.99999999999999978 3 0.99999999999999978 6 0.99999999999999978 8 0.99999999999999978 10 0.99999999999999978
		 13 0.99999999999999978 15 0.99999999999999978 18 0.99999999999999978 20 0.99999999999999978 22 0.99999999999999978 25 0.99999999999999978;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE147";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021D7C";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1.0000000000000007 3 1.0000000000000007 6 1.0000000000000007 8 1.0000000000000007 10 1.0000000000000007
		 13 1.0000000000000007 15 1.0000000000000007 18 1.0000000000000007 20 1.0000000000000007 22 1.0000000000000007 25 1.0000000000000007;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE148";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021D7D";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1.0000000000000007 3 1.0000000000000007 6 1.0000000000000007 8 1.0000000000000007 10 1.0000000000000007
		 13 1.0000000000000007 15 1.0000000000000007 18 1.0000000000000007 20 1.0000000000000007 22 1.0000000000000007 25 1.0000000000000007;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE149";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021D78";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE150";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021D79";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE151";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021D7A";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 -16.004111880308876 3 -16.004111880308876 6 -16.004111880308876 8 -16.004111880308876 10 -16.004111880308876
		 13 -16.004111880308876 15 -16.004111880308876 18 -16.004111880308876 20 -16.004111880308876 22 -16.004111880308876 25 -16.004111880308876;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE153";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021D7F";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE154";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021D80";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE155";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021D81";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE156";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021D82";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE157";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021D86";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1 3 1 6 1 8 1 10 1 13 1 15 1 18 1 20 1
		 22 1 25 1;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE158";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021D87";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1 3 1 6 1 8 1 10 1 13 1 15 1 18 1 20 1
		 22 1 25 1;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE159";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021D88";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1 3 1 6 1 8 1 10 1 13 1 15 1 18 1 20 1
		 22 1 25 1;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE160";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021D83";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE161";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021D84";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1.7349117590792646 3 1.7349117590792646 6 1.7349117590792646 8 1.7349117590792646 10 1.7349117590792646
		 13 1.7349117590792646 15 1.7349117590792646 18 1.7349117590792646 20 1.7349117590792646 22 1.7349117590792646 25 1.7349117590792646;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE162";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021D85";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE164";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021D8A";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE165";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021D8B";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE166";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021D8C";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE167";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021D8D";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE168";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021D91";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1 3 1 6 1 8 1 10 1 13 1 15 1 18 1 20 1
		 22 1 25 1;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE169";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021D92";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1.0000000000000002 3 1.0000000000000002 6 1.0000000000000002 8 1.0000000000000002 10 1.0000000000000002
		 13 1.0000000000000002 15 1.0000000000000002 18 1.0000000000000002 20 1.0000000000000002 22 1.0000000000000002 25 1.0000000000000002;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE170";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021D93";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1 3 1 6 1 8 1 10 1 13 1 15 1 18 1 20 1
		 22 1 25 1;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE171";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021D8E";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE172";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021D8F";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE173";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021D90";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 -16.004111880308876 3 -16.004111880308876 6 -16.004111880308876 8 -16.004111880308876 10 -16.004111880308876
		 13 -16.004111880308876 15 -16.004111880308876 18 -16.004111880308876 20 -16.004111880308876 22 -16.004111880308876 25 -16.004111880308876;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE175";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021D95";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0 20 0 25 0;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTL -n "CURVE176";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021D96";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 1.4210854715202004e-14 20 0 25 1.4210854715202004e-14;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTL -n "CURVE177";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021D97";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 3.5527136788005009e-15 20 0 25 3.5527136788005009e-15;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTL -n "CURVE178";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021D98";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 1.4210854715202004e-14 20 0 25 1.4210854715202004e-14;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTU -n "CURVE179";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021D9C";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0.99999999999999933 20 1 25 0.99999999999999933;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTU -n "CURVE180";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021D9D";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0.99999999999999989 20 0.99999999999999967 25 0.99999999999999989;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTU -n "CURVE181";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021D9E";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0.99999999999999956 20 1 25 0.99999999999999956;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTA -n "CURVE182";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021D99";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 9.621692495944421 20 9.621692495944421 25 9.621692495944421;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTA -n "CURVE183";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021D9A";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 -12.355628023535985 20 -12.355628023535987 25 -12.355628023535985;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTA -n "CURVE184";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021D9B";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 -0.68485988447622193 20 -0.68485988447622193 25 -0.68485988447622193;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTU -n "CURVE186";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021DA0";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0 20 0 25 0;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTL -n "CURVE187";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021DA1";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 2.1316282072803006e-14 20 7.1054273576010019e-15 25 2.1316282072803006e-14;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTL -n "CURVE188";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021DA2";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0 20 0 25 0;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTL -n "CURVE189";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021DA3";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0 20 3.5527136788005009e-15 25 0;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTU -n "CURVE190";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021DA7";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0.99999999999999967 20 1.0000000000000002 25 0.99999999999999967;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTU -n "CURVE191";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021DA8";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 1 20 1.0000000000000007 25 1;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTU -n "CURVE192";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021DA9";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0.99999999999999978 20 1.0000000000000007 25 0.99999999999999978;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTA -n "CURVE193";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021DA4";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0 20 0 25 0;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTA -n "CURVE194";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021DA5";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0 20 0 25 0;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTA -n "CURVE195";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021DA6";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 -87.000039476070498 20 -87.000039476070498 25 -87.000039476070498;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTU -n "CURVE197";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021DAB";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0 20 0 25 0;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTL -n "CURVE198";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021DAC";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 7.1054273576010019e-15 20 0 25 7.1054273576010019e-15;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTL -n "CURVE199";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021DAD";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0 20 0 25 0;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTL -n "CURVE200";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021DAE";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 -2.6645352591003757e-15 20 5.3290705182007514e-15 25 -2.6645352591003757e-15;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTU -n "CURVE201";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021DB2";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0.999999999999999 20 0.99999999999999978 25 0.999999999999999;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTU -n "CURVE202";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021DB3";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0.99999999999999878 20 0.99999999999999978 25 0.99999999999999878;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTU -n "CURVE203";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021DB4";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 1.0000000000000002 20 1.0000000000000009 25 1.0000000000000002;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTA -n "CURVE204";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021DAF";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0.62747866133307717 20 0.62747866133307717 25 0.62747866133307717;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTA -n "CURVE205";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021DB0";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 -4.7696644985950334 20 -4.7696644985950334 25 -4.7696644985950334;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTA -n "CURVE206";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021DB1";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 -21.854123253093604 20 -21.854123253093604 25 -21.854123253093604;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTU -n "CURVE208";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021DB6";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE209";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021DB7";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE210";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021DB8";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE211";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021DB9";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE212";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021DBD";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1.0000000000000002 3 1.0000000000000002 6 1.0000000000000002 8 1.0000000000000002 10 1.0000000000000002
		 13 1.0000000000000002 15 1.0000000000000002 18 1.0000000000000002 20 1.0000000000000002 22 1.0000000000000002 25 1.0000000000000002;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE213";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021DBE";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1.0000000000000011 3 1.0000000000000011 6 1.0000000000000011 8 1.0000000000000011 10 1.0000000000000011
		 13 1.0000000000000011 15 1.0000000000000011 18 1.0000000000000011 20 1.0000000000000011 22 1.0000000000000011 25 1.0000000000000011;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE214";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021DBF";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1.0000000000000002 3 1.0000000000000002 6 1.0000000000000002 8 1.0000000000000002 10 1.0000000000000002
		 13 1.0000000000000002 15 1.0000000000000002 18 1.0000000000000002 20 1.0000000000000002 22 1.0000000000000002 25 1.0000000000000002;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE215";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021DBA";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE216";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021DBB";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE217";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021DBC";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 -13.281297366785457 3 -13.281297366785457 6 -13.281297366785457 8 -13.281297366785457 10 -13.281297366785457
		 13 -13.281297366785457 15 -13.281297366785457 18 -13.281297366785457 20 -13.281297366785457 22 -13.281297366785457 25 -13.281297366785457;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE219";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021DC1";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE220";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021DC2";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE221";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021DC3";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE222";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021DC4";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE223";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021DC8";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1 3 1 6 1 8 1 10 1 13 1 15 1 18 1 20 1
		 22 1 25 1;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE224";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021DC9";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1 3 1 6 1 8 1 10 1 13 1 15 1 18 1 20 1
		 22 1 25 1;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE225";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021DCA";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1 3 1 6 1 8 1 10 1 13 1 15 1 18 1 20 1
		 22 1 25 1;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE226";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021DC5";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE227";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021DC6";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 -8.0990838333569179 3 -8.0990838333569179 6 -8.0990838333569179 8 -8.0990838333569179 10 -8.0990838333569179
		 13 -8.0990838333569179 15 -8.0990838333569179 18 -8.0990838333569179 20 -8.0990838333569179 22 -8.0990838333569179 25 -8.0990838333569179;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE228";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021DC7";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE230";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021DCC";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 3 3 3 6 3 8 3 10 3 13 3 15 3 18 3 20 3
		 22 3 25 3;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE231";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021DCD";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE232";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021DCE";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE233";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021DCF";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE234";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021DD0";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0 13 0 25 0;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTA -n "CURVE235";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021DD1";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 -40.254616081343258 3 -40.254616081343258 6 -40.254616081343258 8 -40.254616081343258 10 -40.254616081343258
		 13 -40.254616081343258 15 -40.254616081343258 18 -40.254616081343258 20 -40.254616081343258 22 -40.254616081343258 25 -40.254616081343258;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE236";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021DD2";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 13 ".ktv[0:12]"  1 18.549269962179174 3 14.665687035957037 6 -0.51450427907132945 8 -6.0674002632788024 10 -8.9428130962911325
		 13 -11.171031891821766 15 -8.8996876604060802 16 -5.646180133353651 18 3.9921069278295347 19 9.8997382320516287 20 13.012660743983346 22 16.753283492878062 25 18.549269962179174;
	setAttr -s 13 ".kit[12]"  1;
	setAttr -s 13 ".kot[0:12]"  1 18 18 18 18 18 18 18 
		18 18 18 18 1;
	setAttr -s 13 ".kix[12]"  1;
	setAttr -s 13 ".kiy[12]"  0;
	setAttr -s 13 ".kox[0:12]"  1 0.53069450422411601 0.49894525271393086 0.74974207156162997 0.91948113430156797 1 0.79178751712982554 
		0.48563590162916326 0.41842872836703243 0.46781585588143032 0.72249253924373502 0.90716545948189853 1;
	setAttr -s 13 ".koy[0:12]"  0 -0.84756317946588489 -0.8666335066187042 -0.66173017622780039 -0.39313412935473019 0 0.61079663368210069 
		0.8741611813898108 0.90824963488963095 0.88382595853817547 0.69137871730126321 0.42077408323588111 0;
createNode animCurveTU -n "CURVE238";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021DD4";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE239";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021DD8";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE240";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021DD9";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE241";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021DDA";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE242";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021DDB";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1 3 1 6 1 8 1 10 1 13 1 15 1 18 1 20 1
		 22 1 25 1;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE243";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021DDC";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1 3 1 6 1 8 1 10 1 13 1 15 1 18 1 20 1
		 22 1 25 1;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE244";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021DDD";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1 3 1 6 1 8 1 10 1 13 1 15 1 18 1 20 1
		 22 1 25 1;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE245";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021DD5";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE246";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021DD6";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 7 ".ktv[0:6]"  1 -15.40821076923077 3 -12.138877692307691 10 10.746456923076924 13 15.408461538461538 15 12.139123076923077
		 22 -10.746247692307692 25 -15.40821076923077;
	setAttr -s 7 ".kyts[1:6]" yes yes no yes yes no;
	setAttr -s 7 ".kit[6]"  1;
	setAttr -s 7 ".kot[0:6]"  1 18 18 18 18 18 1;
	setAttr -s 7 ".kix[6]"  1;
	setAttr -s 7 ".kiy[6]"  0;
	setAttr -s 7 ".kox[0:6]"  1 0.63476987054762035 0.65491300479314218 1 0.63476926862529048 0.65491307790072717 1;
	setAttr -s 7 ".koy[0:6]"  0 0.77270124333079548 0.75570427824170605 0 -0.77270173780632445 -0.75570421488476314 0;
createNode animCurveTA -n "CURVE247";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021DD7";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 9 ".ktv[0:8]"  1 0 3 1.7091637284640935 6 6.8366549138563739 10 1.7168372520187953 13 0 15 -1.70925
		 18 -6.837 22 -1.7170000000000005 25 0;
	setAttr -s 9 ".kyts[1:8]" yes no no no yes no no no;
	setAttr -s 9 ".kit[8]"  1;
	setAttr -s 9 ".kot[0:8]"  1 18 18 18 18 18 18 18 
		1;
	setAttr -s 9 ".kix[8]"  1;
	setAttr -s 9 ".kiy[8]"  0;
	setAttr -s 9 ".kox[0:8]"  1 0.86775016115412884 1 0.92554255657349482 0.961190907750333 0.86773934194943525 1 0.92553585853340758 
		1;
	setAttr -s 9 ".koy[0:8]"  0 0.49700066178726909 0 -0.37864360019865551 -0.27588410403299934 -0.49701955135905973 0 0.37865997222947656 
		0;
createNode animCurveTU -n "CURVE249";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021DDF";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 5 ".ktv[0:4]"  1 0 12 0 13 0 15 0 25 0;
	setAttr -s 5 ".kit[4]"  1;
	setAttr -s 5 ".kot[0:4]"  1 18 18 18 1;
	setAttr -s 5 ".kix[4]"  1;
	setAttr -s 5 ".kiy[4]"  0;
	setAttr -s 5 ".kox[0:4]"  1 1 1 1 1;
	setAttr -s 5 ".koy[0:4]"  0 0 0 0 0;
createNode animCurveTL -n "CURVE250";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021DE0";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 5 ".ktv[0:4]"  1 0 12 0 13 0 15 0 25 0;
	setAttr -s 5 ".kit[4]"  1;
	setAttr -s 5 ".kot[0:4]"  1 18 18 18 1;
	setAttr -s 5 ".kix[4]"  1;
	setAttr -s 5 ".kiy[4]"  0;
	setAttr -s 5 ".kox[0:4]"  1 1 1 1 1;
	setAttr -s 5 ".koy[0:4]"  0 0 0 0 0;
createNode animCurveTL -n "CURVE251";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021DE1";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 5 ".ktv[0:4]"  1 0 12 0 13 0 15 0 25 0;
	setAttr -s 5 ".kit[4]"  1;
	setAttr -s 5 ".kot[0:4]"  1 18 18 18 1;
	setAttr -s 5 ".kix[4]"  1;
	setAttr -s 5 ".kiy[4]"  0;
	setAttr -s 5 ".kox[0:4]"  1 1 1 1 1;
	setAttr -s 5 ".koy[0:4]"  0 0 0 0 0;
createNode animCurveTL -n "CURVE252";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021DE2";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 5 ".ktv[0:4]"  1 0 12 0 13 0 15 0 25 0;
	setAttr -s 5 ".kit[4]"  1;
	setAttr -s 5 ".kot[0:4]"  1 18 18 18 1;
	setAttr -s 5 ".kix[4]"  1;
	setAttr -s 5 ".kiy[4]"  0;
	setAttr -s 5 ".kox[0:4]"  1 1 1 1 1;
	setAttr -s 5 ".koy[0:4]"  0 0 0 0 0;
createNode animCurveTU -n "CURVE253";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021DE6";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 5 ".ktv[0:4]"  1 1.0000000000000002 12 1.0000000000000002 13 1.0000000000000002 15 1.0000000000000002 25 1.0000000000000002;
	setAttr -s 5 ".kit[4]"  1;
	setAttr -s 5 ".kot[0:4]"  1 18 18 18 1;
	setAttr -s 5 ".kix[4]"  1;
	setAttr -s 5 ".kiy[4]"  0;
	setAttr -s 5 ".kox[0:4]"  1 1 1 1 1;
	setAttr -s 5 ".koy[0:4]"  0 0 0 0 0;
createNode animCurveTU -n "CURVE254";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021DE7";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 5 ".ktv[0:4]"  1 0.99999999999999989 12 0.99999999999999989 13 0.99999999999999989 15 0.99999999999999989 25 0.99999999999999989;
	setAttr -s 5 ".kit[4]"  1;
	setAttr -s 5 ".kot[0:4]"  1 18 18 18 1;
	setAttr -s 5 ".kix[4]"  1;
	setAttr -s 5 ".kiy[4]"  0;
	setAttr -s 5 ".kox[0:4]"  1 1 1 1 1;
	setAttr -s 5 ".koy[0:4]"  0 0 0 0 0;
createNode animCurveTU -n "CURVE255";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021DE8";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 5 ".ktv[0:4]"  1 1 12 1 13 1 15 1 25 1;
	setAttr -s 5 ".kit[4]"  1;
	setAttr -s 5 ".kot[0:4]"  1 18 18 18 1;
	setAttr -s 5 ".kix[4]"  1;
	setAttr -s 5 ".kiy[4]"  0;
	setAttr -s 5 ".kox[0:4]"  1 1 1 1 1;
	setAttr -s 5 ".koy[0:4]"  0 0 0 0 0;
createNode animCurveTA -n "CURVE256";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021DE3";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 5 ".ktv[0:4]"  1 0 12 0 13 0 15 0 25 0;
	setAttr -s 5 ".kit[4]"  1;
	setAttr -s 5 ".kot[0:4]"  1 18 18 18 1;
	setAttr -s 5 ".kix[4]"  1;
	setAttr -s 5 ".kiy[4]"  0;
	setAttr -s 5 ".kox[0:4]"  1 1 1 1 1;
	setAttr -s 5 ".koy[0:4]"  0 0 0 0 0;
createNode animCurveTA -n "CURVE257";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021DE4";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 5 ".ktv[0:4]"  1 0 12 0 13 0 15 0 25 0;
	setAttr -s 5 ".kit[4]"  1;
	setAttr -s 5 ".kot[0:4]"  1 18 18 18 1;
	setAttr -s 5 ".kix[4]"  1;
	setAttr -s 5 ".kiy[4]"  0;
	setAttr -s 5 ".kox[0:4]"  1 1 1 1 1;
	setAttr -s 5 ".koy[0:4]"  0 0 0 0 0;
createNode animCurveTA -n "CURVE258";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021DE5";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 6 ".ktv[0:5]"  1 0 12 0 13 5.0200609289598281 14 8.1745851549035962 15 0 25 0;
	setAttr -s 6 ".kit[5]"  1;
	setAttr -s 6 ".kot[0:5]"  1 18 18 18 18 1;
	setAttr -s 6 ".kix[5]"  1;
	setAttr -s 6 ".kiy[5]"  0;
	setAttr -s 6 ".kox[0:5]"  1 1 0.50435488319965371 1 1 1;
	setAttr -s 6 ".koy[0:5]"  0 0 0.86349646889414888 0 0 0;
createNode animCurveTU -n "CURVE260";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021DEA";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0 20 0 25 0;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTL -n "CURVE261";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021DEB";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0 20 -7.1054273576010019e-15 25 0;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTL -n "CURVE262";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021DEC";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 1.4210854715202004e-14 20 1.4210854715202004e-14 25 1.4210854715202004e-14;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTL -n "CURVE263";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021DED";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 1.7763568394002505e-15 20 8.8817841970012523e-16 25 1.7763568394002505e-15;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTU -n "CURVE264";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021DF1";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 1.0000000000000002 20 1.0000000000000004 25 1.0000000000000002;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTU -n "CURVE265";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021DF2";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 1.0000000000000002 20 1.0000000000000002 25 1.0000000000000002;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTU -n "CURVE266";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021DF3";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 1.0000000000000004 20 0.99999999999999967 25 1.0000000000000004;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTA -n "CURVE267";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021DEE";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0 20 0 25 0;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTA -n "CURVE268";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021DEF";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0 20 0 25 0;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTA -n "CURVE269";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021DF0";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 -77.652545175089656 20 -77.652545175089656 25 -77.652545175089656;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTU -n "CURVE271";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021DF5";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0 20 0 25 0;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTL -n "CURVE272";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021DF6";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 -1.4210854715202004e-14 20 -7.1054273576010019e-15 25 -1.4210854715202004e-14;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTL -n "CURVE273";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021DF7";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0 20 -1.4210854715202004e-14 25 0;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTL -n "CURVE274";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021DF8";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 2.2204460492503131e-16 20 8.8817841970012523e-16 25 2.2204460492503131e-16;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTU -n "CURVE275";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021DFC";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 1.0000000000000002 20 1.0000000000000016 25 1.0000000000000002;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTU -n "CURVE276";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021DFD";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 1.0000000000000011 20 1.0000000000000007 25 1.0000000000000011;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTU -n "CURVE277";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021DFE";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 1.0000000000000002 20 0.99999999999999989 25 1.0000000000000002;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTA -n "CURVE278";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021DF9";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 5.7160089625777575 20 5.7160089625777575 25 5.7160089625777575;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTA -n "CURVE279";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021DFA";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 -11.816804184501121 20 -11.816804184501121 25 -11.816804184501121;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTA -n "CURVE280";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021DFB";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 -26.048814328401694 20 -26.048814328401694 25 -26.048814328401694;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTU -n "CURVE282";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021E00";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0 20 0 25 0;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTL -n "CURVE283";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021E01";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 -1.4210854715202004e-14 20 2.8421709430404007e-14 25 -1.4210854715202004e-14;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTL -n "CURVE284";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021E02";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 3.5527136788005009e-15 20 1.7763568394002505e-15 25 3.5527136788005009e-15;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTL -n "CURVE285";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021E03";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0 20 -1.4210854715202004e-14 25 0;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTU -n "CURVE286";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021E07";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0.99999999999999956 20 0.99999999999999944 25 0.99999999999999956;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTU -n "CURVE287";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021E08";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0.99999999999999989 20 0.99999999999999933 25 0.99999999999999989;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTU -n "CURVE288";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021E09";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0.99999999999999956 20 0.99999999999999944 25 0.99999999999999956;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTA -n "CURVE289";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021E04";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 31.486797465577592 20 31.486797465577592 25 31.486797465577592;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTA -n "CURVE290";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021E05";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 9.171166235157985 20 9.171166235157985 25 9.171166235157985;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTA -n "CURVE291";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021E06";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 -3.9710956032536928 20 -3.9710956032536928 25 -3.9710956032536928;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTU -n "CURVE293";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021E0B";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0 20 0 25 0;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTL -n "CURVE294";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021E0C";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 -1.4210854715202004e-14 20 -1.4210854715202004e-14 25 -1.4210854715202004e-14;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTL -n "CURVE295";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021E0D";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 3.5527136788005009e-15 20 5.3290705182007514e-15 25 3.5527136788005009e-15;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTL -n "CURVE296";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021E0E";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0 20 1.4210854715202004e-14 25 0;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTU -n "CURVE297";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021E12";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 1.0000000000000002 20 1.0000000000000002 25 1.0000000000000002;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTU -n "CURVE298";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021E13";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0.99999999999999978 20 0.99999999999999978 25 0.99999999999999978;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTU -n "CURVE299";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021E14";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 1 20 0.99999999999999978 25 1;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTA -n "CURVE300";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021E0F";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0 20 0 25 0;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTA -n "CURVE301";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021E10";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0 20 0 25 0;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTA -n "CURVE302";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021E11";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 -27.431059773198989 20 -27.431059773198989 25 -27.431059773198989;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTU -n "CURVE304";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021E16";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE305";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021E17";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE306";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021E18";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE307";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021E19";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE308";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021E1D";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1.0000000000000002 3 1.0000000000000002 6 1.0000000000000002 8 1.0000000000000002 10 1.0000000000000002
		 13 1.0000000000000002 15 1.0000000000000002 18 1.0000000000000002 20 1.0000000000000002 22 1.0000000000000002 25 1.0000000000000002;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE309";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021E1E";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1.0000000000000004 3 1.0000000000000004 6 1.0000000000000004 8 1.0000000000000004 10 1.0000000000000004
		 13 1.0000000000000004 15 1.0000000000000004 18 1.0000000000000004 20 1.0000000000000004 22 1.0000000000000004 25 1.0000000000000004;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE310";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021E1F";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1.0000000000000004 3 1.0000000000000004 6 1.0000000000000004 8 1.0000000000000004 10 1.0000000000000004
		 13 1.0000000000000004 15 1.0000000000000004 18 1.0000000000000004 20 1.0000000000000004 22 1.0000000000000004 25 1.0000000000000004;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE311";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021E1A";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE312";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021E1B";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE313";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021E1C";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 -10.753573818184966 3 -10.753573818184966 6 -10.753573818184966 8 -10.753573818184966 10 -10.753573818184966
		 13 -10.753573818184966 15 -10.753573818184966 18 -10.753573818184966 20 -10.753573818184966 22 -10.753573818184966 25 -10.753573818184966;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE315";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021E21";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE316";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021E22";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE317";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021E23";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE318";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021E24";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE319";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021E28";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0.99999999999999978 3 0.99999999999999978 6 0.99999999999999978 8 0.99999999999999978 10 0.99999999999999978
		 13 0.99999999999999978 15 0.99999999999999978 18 0.99999999999999978 20 0.99999999999999978 22 0.99999999999999978 25 0.99999999999999978;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE320";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021E29";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0.99999999999999989 3 0.99999999999999989 6 0.99999999999999989 8 0.99999999999999989 10 0.99999999999999989
		 13 0.99999999999999989 15 0.99999999999999989 18 0.99999999999999989 20 0.99999999999999989 22 0.99999999999999989 25 0.99999999999999989;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE321";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021E2A";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0.99999999999999989 3 0.99999999999999989 6 0.99999999999999989 8 0.99999999999999989 10 0.99999999999999989
		 13 0.99999999999999989 15 0.99999999999999989 18 0.99999999999999989 20 0.99999999999999989 22 0.99999999999999989 25 0.99999999999999989;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE322";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021E25";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE323";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021E26";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 9.565175890006417 3 9.565175890006417 6 9.565175890006417 8 9.565175890006417 10 9.565175890006417
		 13 9.565175890006417 15 9.565175890006417 18 9.565175890006417 20 9.565175890006417 22 9.565175890006417 25 9.565175890006417;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE324";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021E27";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE326";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021E2C";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0 20 0 25 0;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTL -n "CURVE327";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021E2D";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0 20 -7.1054273576010019e-15 25 0;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTL -n "CURVE328";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021E2E";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0 20 0 25 0;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTL -n "CURVE329";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021E2F";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 -3.1086244689504383e-15 20 1.7763568394002505e-15 25 -3.1086244689504383e-15;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTU -n "CURVE330";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021E33";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0.99999999999999978 20 1.0000000000000002 25 0.99999999999999978;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTU -n "CURVE331";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021E34";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 1.0000000000000004 20 1.0000000000000004 25 1.0000000000000004;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTU -n "CURVE332";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021E35";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 1.0000000000000004 20 1.0000000000000004 25 1.0000000000000004;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTA -n "CURVE333";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021E30";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0 20 0 25 0;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTA -n "CURVE334";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021E31";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0 20 0 25 0;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTA -n "CURVE335";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021E32";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 -50.474943234804122 20 -50.47494323480413 25 -50.474943234804122;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTU -n "CURVE337";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021E37";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0 3 0 25 0;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTL -n "CURVE338";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021E38";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0 3 0 25 0;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTL -n "CURVE339";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021E39";
	setAttr ".tan" 1;
	setAttr ".wgt" no;
	setAttr -s 21 ".ktv[0:20]"  1 0 2 0 3 0 4 0 5 0 6 0 8 0 10 0 11 0 12 0
		 13 0 14 0 15 0 16 0 17 0 18 0 20 0 22 0 23 0 24 0 25 0;
	setAttr -s 21 ".kix[0:20]"  1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 
		1;
	setAttr -s 21 ".kiy[0:20]"  0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 
		0;
	setAttr -s 21 ".kox[0:20]"  1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 
		1;
	setAttr -s 21 ".koy[0:20]"  0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 
		0;
createNode animCurveTL -n "CURVE340";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021E3A";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0 3 0 25 0;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTU -n "CURVE341";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021E3E";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 1 3 1 25 1;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTU -n "CURVE342";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021E3F";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 1 3 1 25 1;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTU -n "CURVE343";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021E40";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 1 3 1 25 1;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTA -n "CURVE344";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021E3B";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 -0.90079365387032029 2 -0.68065934372160219 3 -0.047924873961041364 3.9999998299319728 0.85201776338109037
		 4 0.85181498257841604 5 1.817383923922065 6 2.1404597533989542 7 1.9175583555937548 8 1.335105579945894 9 0.48900548962871038 11 -0.59225447161813993 13 -0.90079365387032029 14 -0.70043391907046904
		 15 -0.087519926363867379 16 0.85181498257841604 17 1.7840774051172479 18 2.1404597533989542 19 1.9175873461443398 20 1.3351877198392199 21 0.48911662007262474 23 -0.59225447161813993 25 -0.90079365387032029;
	setAttr -s 22 ".kit[21]"  1;
	setAttr -s 22 ".kot[0:21]"  1 18 18 18 18 18 18 18 
		18 18 18 18 18 18 18 18 18 18 18 18 18 1;
	setAttr -s 22 ".kix[21]"  1;
	setAttr -s 22 ".kiy[21]"  0;
	setAttr -s 22 ".kox[0:21]"  1 0.98441854683834473 0.95214649191017675 1 1 0.96545504309063601 1 0.98607122865843444 0.95803817795292023 
		0.96564497231771607 0.98957447145632049 1 0.98580177641574507 0.95100548081550385 0.93102712118801767 0.96545504309063623 1 0.98607401069495726 0.95804270387131019 0.96564219317066335 0.98957283009552277 1;
	setAttr -s 22 ".koy[0:21]"  0 0.1758411915356628 0.30564204217211954 0 0 0.26056968313842255 0 -0.16632357623634014 -0.28664062793792622 
		-0.25986494076253819 -0.14402210053302197 0 0.16791324431253601 0.30917402131950278 0.36494999604377598 0.26056968313842255 0 -0.16630708172522701 -0.28662550053850616 -0.25987526771232194 -0.14403337785644554 0;
createNode animCurveTA -n "CURVE345";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021E3C";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 7 ".ktv[0:6]"  1 1.959018 3 1.543351 10 -1.366318 13 -1.959051
		 15 -1.543383 22 1.366291 25 1.959018;
	setAttr -s 7 ".kit[6]"  1;
	setAttr -s 7 ".kot[0:6]"  1 18 18 18 18 18 1;
	setAttr -s 7 ".kix[6]"  1;
	setAttr -s 7 ".kiy[6]"  0;
	setAttr -s 7 ".kox[0:6]"  1 0.98823435902361856 0.98940900312622282 1 0.98823431731179323 0.98940900907832963 1;
	setAttr -s 7 ".koy[0:6]"  0 -0.15294721849441278 -0.14515448505910519 0 0.15294748800583202 0.14515444448806081 0;
createNode animCurveTA -n "CURVE346";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021E3D";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0 3 0 25 0;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTU -n "CURVE348";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021E42";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE349";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021E43";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE350";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021E44";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE351";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021E45";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE352";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021E46";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE353";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021E47";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE354";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021E48";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 -9.6696392331877377 3 -5.0559828573291874 6 5.1566769867447446 8 2.3355936742608812 10 -9.5963427663786565
		 13 -18.380712912870933 15 -21.176494380670352 18 -23.743540134295163 20 -18.150471490102031 22 -14.81968867815015 25 -9.6696392331877377;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 0.62711283484298941 1 0.54338062391927078 0.49924870507984431 0.71774271017655 0.91216876417772208 
		1 0.73062864789283088 0.81519494728751285 1;
	setAttr -s 11 ".koy[0:10]"  0 0.77892842570751608 0 -0.83948644869890787 -0.86645872981700556 -0.69630841010892652 -0.40981476993696481 
		0 0.68277505730532784 0.5791866693190626 0;
createNode animCurveTU -n "CURVE356";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021E4A";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE357";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021E4B";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE358";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021E4C";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE359";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021E4D";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE360";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021E4E";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 7 ".ktv[0:6]"  1 31.852191390029503 3 32.81088764043507 6 30.772976564553094 8 29.274554577276618 15 26.858370873464523
		 18 27.508994346479859 25 31.852191390029503;
	setAttr -s 7 ".kit[6]"  1;
	setAttr -s 7 ".kot[0:6]"  1 18 18 18 18 18 1;
	setAttr -s 7 ".kix[6]"  0.85659725963363598;
	setAttr -s 7 ".kiy[6]"  0.51598559552389167;
	setAttr -s 7 ".kox[0:6]"  1 1 0.95880781446460828 0.98380476841479814 1 0.97881449700351519 1;
	setAttr -s 7 ".koy[0:6]"  0 0 -0.28405558421126204 -0.1792433475594154 0 0.20474906704489693 0;
createNode animCurveTA -n "CURVE361";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021E4F";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE362";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021E50";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 8 ".ktv[0:7]"  1 1.5522074829890398 3 8.3844696333566162 6 2.7163630952308191 8 0.51740249432967955 10 0
		 13 -0.51740249432967944 18 -5.2404627173249505 25 1.5522074829890398;
	setAttr -s 8 ".kit[7]"  1;
	setAttr -s 8 ".kot[0:7]"  1 18 18 18 18 18 18 1;
	setAttr -s 8 ".kix[7]"  0.64949832687804687;
	setAttr -s 8 ".kiy[7]"  0.76036302078850326;
	setAttr -s 8 ".kox[0:7]"  1 1 0.83496627424295 0.96184276914119582 0.99626333039741988 0.9773105208956212 1 1;
	setAttr -s 8 ".koy[0:7]"  0 0 -0.55030111836779572 -0.27360279137975957 -0.08636768206592893 -0.21181158076632509 0 0;
createNode animCurveTU -n "CURVE364";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021E52";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0 13 0 25 0;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTL -n "CURVE365";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021E53";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0 13 0 25 0;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTL -n "CURVE366";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021E54";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0 13 0 25 0;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTL -n "CURVE367";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021E55";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0 13 0 25 0;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTU -n "CURVE368";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021E59";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 1 13 1 25 1;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTU -n "CURVE369";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021E5A";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 1 13 1 25 1;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTU -n "CURVE370";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021E5B";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 1 13 1 25 1;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTA -n "CURVE371";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021E56";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0 13 0 25 0;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTA -n "CURVE372";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021E57";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 -8.544 13 8.5441077391367592 25 -8.544;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTA -n "CURVE373";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021E58";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0 13 0 25 0;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 18;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTU -n "CURVE375";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021E5D";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0 20 0 25 0;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTL -n "CURVE376";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021E5E";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0 20 7.1054273576010019e-15 25 0;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTL -n "CURVE377";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021E5F";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0 20 -1.4210854715202004e-14 25 0;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTL -n "CURVE378";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021E60";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0 20 8.8817841970012523e-16 25 0;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTU -n "CURVE379";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021E64";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 1 20 1 25 1;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTU -n "CURVE380";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021E65";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 1 20 0.99999999999999989 25 1;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTU -n "CURVE381";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021E66";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 1 20 0.99999999999999989 25 1;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTA -n "CURVE382";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021E61";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0 20 0 25 0;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTA -n "CURVE383";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021E62";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0 20 0 25 0;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTA -n "CURVE384";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021E63";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0 20 0 25 0;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTU -n "CURVE386";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021E68";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0 20 0 25 0;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTL -n "CURVE387";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021E69";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0 20 0 25 0;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTL -n "CURVE388";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021E6A";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 -1.4210854715202004e-14 20 0 25 -1.4210854715202004e-14;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTL -n "CURVE389";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021E6B";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 1.7763568394002505e-15 20 0 25 1.7763568394002505e-15;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTU -n "CURVE390";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021E6F";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0.99999999999999956 20 1 25 0.99999999999999956;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTU -n "CURVE391";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021E70";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 1 20 1.0000000000000004 25 1;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTU -n "CURVE392";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021E71";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 1.0000000000000004 20 1 25 1.0000000000000004;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTA -n "CURVE393";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021E6C";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0 20 0 25 0;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTA -n "CURVE394";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021E6D";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0 20 0 25 0;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTA -n "CURVE395";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021E6E";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 -27.297073028821604 20 -27.297073028821604 25 -27.297073028821604;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTU -n "CURVE397";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021E73";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE398";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021E74";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE399";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021E75";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE400";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021E76";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE401";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021E7A";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1.0000000000000004 3 1.0000000000000004 6 1.0000000000000004 8 1.0000000000000004 10 1.0000000000000004
		 13 1.0000000000000004 15 1.0000000000000004 18 1.0000000000000004 20 1.0000000000000004 22 1.0000000000000004 25 1.0000000000000004;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE402";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021E7B";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1.0000000000000002 3 1.0000000000000002 6 1.0000000000000002 8 1.0000000000000002 10 1.0000000000000002
		 13 1.0000000000000002 15 1.0000000000000002 18 1.0000000000000002 20 1.0000000000000002 22 1.0000000000000002 25 1.0000000000000002;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE403";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021E7C";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1.0000000000000004 3 1.0000000000000004 6 1.0000000000000004 8 1.0000000000000004 10 1.0000000000000004
		 13 1.0000000000000004 15 1.0000000000000004 18 1.0000000000000004 20 1.0000000000000004 22 1.0000000000000004 25 1.0000000000000004;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE404";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021E77";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE405";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021E78";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE406";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021E79";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 -5.1421455695746801 3 -5.1421455695746801 6 -5.1421455695746801 8 -5.1421455695746801 10 -5.1421455695746801
		 13 -5.1421455695746801 15 -5.1421455695746801 18 -5.1421455695746801 20 -5.1421455695746801 22 -5.1421455695746801 25 -5.1421455695746801;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE408";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021E7E";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0 20 0 25 0;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTL -n "CURVE409";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021E7F";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 2.8421709430404007e-14 20 0 25 2.8421709430404007e-14;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTL -n "CURVE410";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021E80";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 -1.4210854715202004e-14 20 0 25 -1.4210854715202004e-14;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTL -n "CURVE411";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021E81";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 3.5527136788005009e-15 20 7.1054273576010019e-15 25 3.5527136788005009e-15;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTU -n "CURVE412";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021E85";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0.99999999999999944 20 1.0000000000000002 25 0.99999999999999944;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTU -n "CURVE413";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021E86";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0.99999999999999978 20 1.0000000000000002 25 0.99999999999999978;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTU -n "CURVE414";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021E87";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0.99999999999999933 20 1.0000000000000002 25 0.99999999999999933;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTA -n "CURVE415";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021E82";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 -23.448475290155759 20 -23.448475290155759 25 -23.448475290155759;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTA -n "CURVE416";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021E83";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 6.0250169398918949 20 6.0250169398918949 25 6.0250169398918949;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTA -n "CURVE417";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021E84";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 -18.548744260170427 20 -18.548744260170427 25 -18.548744260170427;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTL -n "CURVE419";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021E89";
	setAttr ".tan" 1;
	setAttr ".wgt" no;
	setAttr -s 2 ".ktv[0:1]"  1 0.025543644213995423 25 0.025543644213995423;
	setAttr -s 2 ".kit[0:1]"  18 1;
	setAttr -s 2 ".kot[1]"  18;
	setAttr -s 2 ".kix[1]"  1;
	setAttr -s 2 ".kiy[1]"  0;
	setAttr -s 2 ".kox[0:1]"  1 1;
	setAttr -s 2 ".koy[0:1]"  0 0;
createNode animCurveTL -n "CURVE420";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021E8A";
	setAttr ".tan" 1;
	setAttr ".wgt" no;
	setAttr -s 2 ".ktv[0:1]"  1 0.0014949268639392577 25 0.0014949268639392577;
	setAttr -s 2 ".kit[0:1]"  18 1;
	setAttr -s 2 ".kot[1]"  18;
	setAttr -s 2 ".kix[1]"  1;
	setAttr -s 2 ".kiy[1]"  0;
	setAttr -s 2 ".kox[0:1]"  1 1;
	setAttr -s 2 ".koy[0:1]"  0 0;
createNode animCurveTL -n "CURVE421";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021E8B";
	setAttr ".tan" 1;
	setAttr ".wgt" no;
	setAttr -s 2 ".ktv[0:1]"  1 -0.0019942131665628402 25 -0.0019942131665628402;
	setAttr -s 2 ".kit[0:1]"  18 1;
	setAttr -s 2 ".kot[1]"  18;
	setAttr -s 2 ".kix[1]"  1;
	setAttr -s 2 ".kiy[1]"  0;
	setAttr -s 2 ".kox[0:1]"  1 1;
	setAttr -s 2 ".koy[0:1]"  0 0;
createNode animCurveTU -n "CURVE423";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021E8D";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0 20 0 25 0;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTL -n "CURVE424";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021E8E";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0 20 3.5527136788005009e-15 25 0;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTL -n "CURVE425";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021E8F";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 -2.8421709430404007e-14 20 1.4210854715202004e-14 25 -2.8421709430404007e-14;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTL -n "CURVE426";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021E90";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 -1.7763568394002505e-15 20 -5.3290705182007514e-15 25 -1.7763568394002505e-15;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTU -n "CURVE427";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021E94";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 1 20 1.0000000000000002 25 1;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTU -n "CURVE428";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021E95";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 1 20 1.0000000000000002 25 1;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTU -n "CURVE429";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021E96";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0.99999999999999989 20 1.0000000000000002 25 0.99999999999999989;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTA -n "CURVE430";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021E91";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 -4.9522089969467213 20 -4.9522089969467213 25 -4.9522089969467213;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTA -n "CURVE431";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021E92";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 2.8802955279843494 20 2.8802955279843494 25 2.8802955279843494;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTA -n "CURVE432";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021E93";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 -0.3432699137982661 20 -0.3432699137982661 25 -0.3432699137982661;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTU -n "CURVE434";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021E98";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE435";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021E99";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE436";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021E9A";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE437";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021E9B";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE438";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021E9C";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE439";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021E9D";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE440";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021E9E";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE442";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021EA0";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE443";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021EA1";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE444";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021EA2";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE445";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021EA3";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE446";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021EA7";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1 3 1 6 1 8 1 10 1 13 1 15 1 18 1 20 1
		 22 1 25 1;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE447";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021EA8";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1 3 1 6 1 8 1 10 1 13 1 15 1 18 1 20 1
		 22 1 25 1;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE448";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021EA9";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1 3 1 6 1 8 1 10 1 13 1 15 1 18 1 20 1
		 22 1 25 1;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE449";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021EA4";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE450";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021EA5";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE451";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021EA6";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE453";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021EAB";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0 20 0 25 0;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTL -n "CURVE454";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021EAC";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 7.1054273576010019e-15 20 -7.1054273576010019e-15 25 7.1054273576010019e-15;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTL -n "CURVE455";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021EAD";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 1.4210854715202004e-14 20 1.4210854715202004e-14 25 1.4210854715202004e-14;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTL -n "CURVE456";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021EAE";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 -8.8817841970012523e-16 20 0 25 -8.8817841970012523e-16;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTU -n "CURVE457";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021EB2";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 1.0000000000000004 20 1.0000000000000007 25 1.0000000000000004;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTU -n "CURVE458";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021EB3";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 1 20 1.0000000000000007 25 1;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTU -n "CURVE459";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021EB4";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 1.0000000000000002 20 0.99999999999999944 25 1.0000000000000002;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTA -n "CURVE460";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021EAF";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0 20 0 25 0;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTA -n "CURVE461";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021EB0";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0 20 0 25 0;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTA -n "CURVE462";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021EB1";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 -41.795578870282704 20 -41.795578870282704 25 -41.795578870282704;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTU -n "CURVE464";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021EB6";
	setAttr ".tan" 1;
	setAttr ".wgt" no;
	setAttr -s 2 ".ktv[0:1]"  1 0 25 0;
	setAttr -s 2 ".kit[0:1]"  18 1;
	setAttr -s 2 ".kix[1]"  1;
	setAttr -s 2 ".kiy[1]"  0;
	setAttr -s 2 ".kox[0:1]"  1 1;
	setAttr -s 2 ".koy[0:1]"  0 0;
createNode animCurveTL -n "CURVE465";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021EB7";
	setAttr ".tan" 1;
	setAttr ".wgt" no;
	setAttr -s 2 ".ktv[0:1]"  1 0 25 0;
	setAttr -s 2 ".kit[0:1]"  18 1;
	setAttr -s 2 ".kix[1]"  1;
	setAttr -s 2 ".kiy[1]"  0;
	setAttr -s 2 ".kox[0:1]"  1 1;
	setAttr -s 2 ".koy[0:1]"  0 0;
createNode animCurveTL -n "CURVE466";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021EB8";
	setAttr ".tan" 1;
	setAttr ".wgt" no;
	setAttr -s 2 ".ktv[0:1]"  1 0 25 0;
	setAttr -s 2 ".kit[0:1]"  18 1;
	setAttr -s 2 ".kix[1]"  1;
	setAttr -s 2 ".kiy[1]"  0;
	setAttr -s 2 ".kox[0:1]"  1 1;
	setAttr -s 2 ".koy[0:1]"  0 0;
createNode animCurveTL -n "CURVE467";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021EB9";
	setAttr ".tan" 1;
	setAttr ".wgt" no;
	setAttr -s 2 ".ktv[0:1]"  1 0 25 0;
	setAttr -s 2 ".kit[0:1]"  18 1;
	setAttr -s 2 ".kix[1]"  1;
	setAttr -s 2 ".kiy[1]"  0;
	setAttr -s 2 ".kox[0:1]"  1 1;
	setAttr -s 2 ".koy[0:1]"  0 0;
createNode animCurveTU -n "CURVE468";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021EBD";
	setAttr ".tan" 1;
	setAttr ".wgt" no;
	setAttr -s 2 ".ktv[0:1]"  1 1.0000000000000002 25 1.0000000000000002;
	setAttr -s 2 ".kit[0:1]"  18 1;
	setAttr -s 2 ".kix[1]"  1;
	setAttr -s 2 ".kiy[1]"  0;
	setAttr -s 2 ".kox[0:1]"  1 1;
	setAttr -s 2 ".koy[0:1]"  0 0;
createNode animCurveTU -n "CURVE469";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021EBE";
	setAttr ".tan" 1;
	setAttr ".wgt" no;
	setAttr -s 2 ".ktv[0:1]"  1 0.99999999999999989 25 0.99999999999999989;
	setAttr -s 2 ".kit[0:1]"  18 1;
	setAttr -s 2 ".kix[1]"  1;
	setAttr -s 2 ".kiy[1]"  0;
	setAttr -s 2 ".kox[0:1]"  1 1;
	setAttr -s 2 ".koy[0:1]"  0 0;
createNode animCurveTU -n "CURVE470";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021EBF";
	setAttr ".tan" 1;
	setAttr ".wgt" no;
	setAttr -s 2 ".ktv[0:1]"  1 1 25 1;
	setAttr -s 2 ".kit[0:1]"  18 1;
	setAttr -s 2 ".kix[1]"  1;
	setAttr -s 2 ".kiy[1]"  0;
	setAttr -s 2 ".kox[0:1]"  1 1;
	setAttr -s 2 ".koy[0:1]"  0 0;
createNode animCurveTA -n "CURVE471";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021EBA";
	setAttr ".tan" 1;
	setAttr ".wgt" no;
	setAttr -s 2 ".ktv[0:1]"  1 0 25 0;
	setAttr -s 2 ".kit[0:1]"  18 1;
	setAttr -s 2 ".kix[1]"  1;
	setAttr -s 2 ".kiy[1]"  0;
	setAttr -s 2 ".kox[0:1]"  1 1;
	setAttr -s 2 ".koy[0:1]"  0 0;
createNode animCurveTA -n "CURVE472";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021EBB";
	setAttr ".tan" 1;
	setAttr ".wgt" no;
	setAttr -s 2 ".ktv[0:1]"  1 0 25 0;
	setAttr -s 2 ".kit[0:1]"  18 1;
	setAttr -s 2 ".kix[1]"  1;
	setAttr -s 2 ".kiy[1]"  0;
	setAttr -s 2 ".kox[0:1]"  1 1;
	setAttr -s 2 ".koy[0:1]"  0 0;
createNode animCurveTA -n "CURVE473";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021EBC";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 7 ".ktv[0:6]"  1 5.0200609289598281 2 8.1745851549035962 3 0 12.999999829931973 0 13 0 24 0
		 25 5.0200609289598281;
	setAttr -s 7 ".kit[6]"  1;
	setAttr -s 7 ".kot[0:6]"  1 18 18 18 18 1 18;
	setAttr -s 7 ".kix[6]"  0.50435488319963218;
	setAttr -s 7 ".kiy[6]"  0.86349646889416154;
	setAttr -s 7 ".kox[0:6]"  0.50435488319963218 1 1 1 1 1 1;
	setAttr -s 7 ".koy[0:6]"  0.86349646889416154 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE475";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021EC1";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0 20 0 25 0;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTL -n "CURVE476";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021EC2";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0 20 0 25 0;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTL -n "CURVE477";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021EC3";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 1.4210854715202004e-14 20 0 25 1.4210854715202004e-14;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTL -n "CURVE478";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021EC4";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 -1.7763568394002505e-15 20 0 25 -1.7763568394002505e-15;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTU -n "CURVE479";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021EC8";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 1.0000000000000004 20 0.99999999999999956 25 1.0000000000000004;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTU -n "CURVE480";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021EC9";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0.99999999999999944 20 0.99999999999999911 25 0.99999999999999944;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTU -n "CURVE481";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021ECA";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 1.0000000000000011 20 0.99999999999999822 25 1.0000000000000011;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTA -n "CURVE482";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021EC5";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 -4.6262668968794545 20 -4.6262668968794545 25 -4.6262668968794545;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTA -n "CURVE483";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021EC6";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 -6.1164618584068524 20 -6.1164618584068524 25 -6.1164618584068524;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTA -n "CURVE484";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021EC7";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 -27.167641811252388 20 -27.167641811252388 25 -27.167641811252388;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTU -n "CURVE486";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021ECC";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE487";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021ECD";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE488";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021ECE";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE489";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021ECF";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE490";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021ED3";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1.0000000000000002 3 1.0000000000000002 6 1.0000000000000002 8 1.0000000000000002 10 1.0000000000000002
		 13 1.0000000000000002 15 1.0000000000000002 18 1.0000000000000002 20 1.0000000000000002 22 1.0000000000000002 25 1.0000000000000002;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE491";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021ED4";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1 3 1 6 1 8 1 10 1 13 1 15 1 18 1 20 1
		 22 1 25 1;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE492";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021ED5";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1.0000000000000002 3 1.0000000000000002 6 1.0000000000000002 8 1.0000000000000002 10 1.0000000000000002
		 13 1.0000000000000002 15 1.0000000000000002 18 1.0000000000000002 20 1.0000000000000002 22 1.0000000000000002 25 1.0000000000000002;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE493";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021ED0";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE494";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021ED1";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE495";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021ED2";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 -19.88365918056531 3 -19.88365918056531 6 -19.88365918056531 8 -19.88365918056531 10 -19.88365918056531
		 13 -19.88365918056531 15 -19.88365918056531 18 -19.88365918056531 20 -19.88365918056531 22 -19.88365918056531 25 -19.88365918056531;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE497";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021ED7";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE498";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021ED8";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE499";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021ED9";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE500";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021EDA";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE501";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021EDE";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1.0000000000000007 3 1.0000000000000007 6 1.0000000000000007 8 1.0000000000000007 10 1.0000000000000007
		 13 1.0000000000000007 15 1.0000000000000007 18 1.0000000000000007 20 1.0000000000000007 22 1.0000000000000007 25 1.0000000000000007;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE502";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021EDF";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0.99999999999999978 3 0.99999999999999978 6 0.99999999999999978 8 0.99999999999999978 10 0.99999999999999978
		 13 0.99999999999999978 15 0.99999999999999978 18 0.99999999999999978 20 0.99999999999999978 22 0.99999999999999978 25 0.99999999999999978;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE503";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021EE0";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1.0000000000000011 3 1.0000000000000011 6 1.0000000000000011 8 1.0000000000000011 10 1.0000000000000011
		 13 1.0000000000000011 15 1.0000000000000011 18 1.0000000000000011 20 1.0000000000000011 22 1.0000000000000011 25 1.0000000000000011;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE504";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021EDB";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE505";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021EDC";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE506";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021EDD";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 -13.281297366785457 3 -13.281297366785457 6 -13.281297366785457 8 -13.281297366785457 10 -13.281297366785457
		 13 -13.281297366785457 15 -13.281297366785457 18 -13.281297366785457 20 -13.281297366785457 22 -13.281297366785457 25 -13.281297366785457;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE508";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021EE2";
	setAttr ".tan" 5;
	setAttr ".wgt" no;
	setAttr -s 2 ".ktv[0:1]"  1 0 25 0;
	setAttr -s 2 ".kit[0:1]"  9 1;
	setAttr -s 2 ".kix[1]"  1;
	setAttr -s 2 ".kiy[1]"  0;
createNode animCurveTL -n "CURVE509";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021EE3";
	setAttr ".tan" 1;
	setAttr ".wgt" no;
	setAttr -s 2 ".ktv[0:1]"  1 0 25 0;
	setAttr -s 2 ".kit[0:1]"  18 1;
	setAttr -s 2 ".kix[1]"  1;
	setAttr -s 2 ".kiy[1]"  0;
	setAttr -s 2 ".kox[0:1]"  1 1;
	setAttr -s 2 ".koy[0:1]"  0 0;
createNode animCurveTL -n "CURVE510";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021EE4";
	setAttr ".tan" 1;
	setAttr ".wgt" no;
	setAttr -s 2 ".ktv[0:1]"  1 0 25 0;
	setAttr -s 2 ".kit[0:1]"  18 1;
	setAttr -s 2 ".kix[1]"  1;
	setAttr -s 2 ".kiy[1]"  0;
	setAttr -s 2 ".kox[0:1]"  1 1;
	setAttr -s 2 ".koy[0:1]"  0 0;
createNode animCurveTL -n "CURVE511";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021EE5";
	setAttr ".tan" 1;
	setAttr ".wgt" no;
	setAttr -s 2 ".ktv[0:1]"  1 0 25 0;
	setAttr -s 2 ".kit[0:1]"  18 1;
	setAttr -s 2 ".kix[1]"  1;
	setAttr -s 2 ".kiy[1]"  0;
	setAttr -s 2 ".kox[0:1]"  1 1;
	setAttr -s 2 ".koy[0:1]"  0 0;
createNode animCurveTA -n "CURVE512";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021EE6";
	setAttr ".tan" 1;
	setAttr ".wgt" no;
	setAttr -s 2 ".ktv[0:1]"  1 0 25 0;
	setAttr -s 2 ".kit[0:1]"  18 1;
	setAttr -s 2 ".kix[1]"  1;
	setAttr -s 2 ".kiy[1]"  0;
	setAttr -s 2 ".kox[0:1]"  1 1;
	setAttr -s 2 ".koy[0:1]"  0 0;
createNode animCurveTA -n "CURVE513";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021EE7";
	setAttr ".tan" 1;
	setAttr ".wgt" no;
	setAttr -s 2 ".ktv[0:1]"  1 0 25 0;
	setAttr -s 2 ".kit[0:1]"  18 1;
	setAttr -s 2 ".kix[1]"  1;
	setAttr -s 2 ".kiy[1]"  0;
	setAttr -s 2 ".kox[0:1]"  1 1;
	setAttr -s 2 ".koy[0:1]"  0 0;
createNode animCurveTA -n "CURVE514";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021EE8";
	setAttr ".tan" 1;
	setAttr ".wgt" no;
	setAttr -s 2 ".ktv[0:1]"  1 0.0033187320688542153 25 0.0033187320688542153;
	setAttr -s 2 ".kit[0:1]"  18 1;
	setAttr -s 2 ".kix[1]"  0.99999130382138879;
	setAttr -s 2 ".kiy[1]"  0.0041704054477923027;
	setAttr -s 2 ".kox[0:1]"  1 0.99999130382138868;
	setAttr -s 2 ".koy[0:1]"  0 0.0041704054477923018;
createNode animCurveTU -n "CURVE516";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021EEA";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0 20 0 25 0;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTL -n "CURVE517";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021EEB";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0 20 -1.4210854715202004e-14 25 0;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTL -n "CURVE518";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021EEC";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0 20 -1.4210854715202004e-14 25 0;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTL -n "CURVE519";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021EED";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0 20 0 25 0;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTU -n "CURVE520";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021EF1";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 1 20 0.99999999999999989 25 1;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTU -n "CURVE521";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021EF2";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 1 20 1 25 1;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTU -n "CURVE522";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021EF3";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 1 20 0.99999999999999989 25 1;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTA -n "CURVE523";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021EEE";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0 20 0 25 0;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTA -n "CURVE524";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021EEF";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0 20 0 25 0;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTA -n "CURVE525";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021EF0";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0 20 0 25 0;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTU -n "CURVE527";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021EF5";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0 20 0 25 0;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTL -n "CURVE528";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021EF6";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 -7.1054273576010019e-15 20 -1.0658141036401503e-14 25 -7.1054273576010019e-15;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTL -n "CURVE529";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021EF7";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 1.4210854715202004e-14 20 0 25 1.4210854715202004e-14;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTL -n "CURVE530";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021EF8";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 -3.5527136788005009e-15 20 7.1054273576010019e-15 25 -3.5527136788005009e-15;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTU -n "CURVE531";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021EFC";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0.99999999999999989 20 0.99999999999999989 25 0.99999999999999989;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTU -n "CURVE532";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021EFD";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0.99999999999999989 20 0.99999999999999989 25 0.99999999999999989;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTU -n "CURVE533";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021EFE";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0.99999999999999989 20 1 25 0.99999999999999989;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTA -n "CURVE534";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021EF9";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0 20 0 25 0;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTA -n "CURVE535";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021EFA";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 3.5785767482094708 20 3.5785767482094708 25 3.5785767482094708;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTA -n "CURVE536";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021EFB";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 11.025921648855906 20 11.025921648855906 25 11.025921648855906;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTU -n "CURVE538";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021F00";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 14 ".ktv[0:13]"  1 0 2 0 5 0 8 0 12 0 13 0 14 0 15 0 17 0
		 18 0 20 0 22 0 24 0 25 0;
	setAttr -s 14 ".kit[13]"  1;
	setAttr -s 14 ".kot[0:13]"  1 18 18 18 18 18 18 18 
		18 18 18 18 18 1;
	setAttr -s 14 ".kix[13]"  1;
	setAttr -s 14 ".kiy[13]"  0;
	setAttr -s 14 ".kox[0:13]"  1 1 1 1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 14 ".koy[0:13]"  0 0 0 0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE539";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021F02";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 18 ".ktv[0:17]"  1 0.45078022929086853 2 0 3 0.39712212807965575 5 0 8 0 12 0 13 0
		 14 1.6011592009422193 15 1.1732534802508487 16 0.28813300258538427 17 -0.22253157008110752 18 0 20 0 21 -0.16864269047186345 22 -0.084321345235931724 23 0.98829199735743223 24 1.1605653525823956
		 25 0.45078022929086853;
	setAttr -s 18 ".kit[17]"  1;
	setAttr -s 18 ".kot[0:17]"  1 18 18 18 18 18 18 18 
		18 18 18 18 18 18 18 18 18 1;
	setAttr -s 18 ".kix[17]"  1;
	setAttr -s 18 ".kiy[17]"  0;
	setAttr -s 18 ".kox[0:17]"  1 1 1 1 1 1 1 1 0.063339181615325924 0.059597434248727349 1 1 1 1 0.16252386276348546 
		0.080360484933234166 1 1;
	setAttr -s 18 ".koy[0:17]"  0 0 0 0 0 0 0 0 -0.99799205812085534 -0.99822249315018374 0 0 0 0 0.98670461336330828 
		0.99676586642064302 0 0;
createNode animCurveTL -n "CURVE540";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021F01";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 22 ".ktv[0:21]"  1 4.9040857040112176 2 -0.40686592116282611 3 -2.1893205428798845 4 -1.8604807621657491 5 -0.91524903313619976
		 6 3.9193232471385007 7 1.7493228333280919 8 2.6730049926483108 10 2.2377101397927706 12 3.6566032299909668 13 1.7683662182556583 14 -1.942088624456346 15 -1.0820322175046384 16 0.37505662640867354
		 17 0.54676043120328655 18 0 20 -0.38491431180819946 21 -0.9899207788411053 22 2.1374413178449503 23 7.2904117321438742 24 5.6046804293273409 25 4.9040857040112176;
	setAttr -s 22 ".kit[21]"  1;
	setAttr -s 22 ".kot[0:21]"  1 18 18 18 18 18 18 18 
		18 18 18 18 18 18 18 18 18 18 18 18 18 1;
	setAttr -s 22 ".kix[21]"  1;
	setAttr -s 22 ".kiy[21]"  0;
	setAttr -s 22 ".kox[0:21]"  1 0.011747188922034964 1 0.065267646958824699 0.014692047864672987 1 1 1 1 1 0.014882780824504884 
		1 0.035940558360756436 0.08062531492048898 1 0.1329755008818517 0.1252779148260387 1 0.010063498460465234 1 0.034899911717302626 1;
	setAttr -s 22 ".koy[0:21]"  0 -0.9999309993956732 0 0.99786779397897107 0.99989206603990133 0 0 0 0 0 -0.99988924528416134 
		0 0.99935392942876711 0.99674448009205063 0 -0.99111932488738241 -0.992121688129455 0 0.99994936171725035 0 -0.99939081252637318 0;
createNode animCurveTL -n "CURVE541";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021F03";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 14 ".ktv[0:13]"  1 0 2 0 5 0 8 0 12 0 13 0 14 0 15 0 17 0
		 18 0 20 0 22 0 24 0 25 0;
	setAttr -s 14 ".kit[13]"  1;
	setAttr -s 14 ".kot[0:13]"  1 18 18 18 18 18 18 18 
		18 18 18 18 18 1;
	setAttr -s 14 ".kix[13]"  1;
	setAttr -s 14 ".kiy[13]"  0;
	setAttr -s 14 ".kox[0:13]"  1 1 1 1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 14 ".koy[0:13]"  0 0 0 0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE542";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021F07";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 14 ".ktv[0:13]"  1 1 2 1 5 1 8 1 12 1 13 1 14 1 15 1 17 1
		 18 1 20 1 22 1 24 1 25 1;
	setAttr -s 14 ".kit[13]"  1;
	setAttr -s 14 ".kot[0:13]"  1 18 18 18 18 18 18 18 
		18 18 18 18 18 1;
	setAttr -s 14 ".kix[13]"  1;
	setAttr -s 14 ".kiy[13]"  0;
	setAttr -s 14 ".kox[0:13]"  1 1 1 1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 14 ".koy[0:13]"  0 0 0 0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE543";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021F08";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 14 ".ktv[0:13]"  1 1 2 1 5 1 8 1 12 1 13 1 14 1 15 1 17 1
		 18 1 20 1 22 1 24 1 25 1;
	setAttr -s 14 ".kit[13]"  1;
	setAttr -s 14 ".kot[0:13]"  1 18 18 18 18 18 18 18 
		18 18 18 18 18 1;
	setAttr -s 14 ".kix[13]"  1;
	setAttr -s 14 ".kiy[13]"  0;
	setAttr -s 14 ".kox[0:13]"  1 1 1 1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 14 ".koy[0:13]"  0 0 0 0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE544";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021F09";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 14 ".ktv[0:13]"  1 1 2 1 5 1 8 1 12 1 13 1 14 1 15 1 17 1
		 18 1 20 1 22 1 24 1 25 1;
	setAttr -s 14 ".kit[13]"  1;
	setAttr -s 14 ".kot[0:13]"  1 18 18 18 18 18 18 18 
		18 18 18 18 18 1;
	setAttr -s 14 ".kix[13]"  1;
	setAttr -s 14 ".kiy[13]"  0;
	setAttr -s 14 ".kox[0:13]"  1 1 1 1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 14 ".koy[0:13]"  0 0 0 0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE545";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021F04";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 14 ".ktv[0:13]"  1 0 2 0 5 0 8 0 12 0 13 0 14 0 15 0 17 0
		 18 0 20 0 22 0 24 0 25 0;
	setAttr -s 14 ".kit[13]"  1;
	setAttr -s 14 ".kot[0:13]"  1 18 18 18 18 18 18 18 
		18 18 18 18 18 1;
	setAttr -s 14 ".kix[13]"  1;
	setAttr -s 14 ".kiy[13]"  0;
	setAttr -s 14 ".kox[0:13]"  1 1 1 1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 14 ".koy[0:13]"  0 0 0 0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE546";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021F05";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 14 ".ktv[0:13]"  1 0 2 0 5 0 8 0 12 0 13 0 14 0 15 0 17 0
		 18 0 20 0 22 0 24 0 25 0;
	setAttr -s 14 ".kit[13]"  1;
	setAttr -s 14 ".kot[0:13]"  1 18 18 18 18 18 18 18 
		18 18 18 18 18 1;
	setAttr -s 14 ".kix[13]"  1;
	setAttr -s 14 ".kiy[13]"  0;
	setAttr -s 14 ".kox[0:13]"  1 1 1 1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 14 ".koy[0:13]"  0 0 0 0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE547";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021F06";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 14 ".ktv[0:13]"  1 0 2 0 5 0 8 0 12 0 13 0 14 0 15 0 17 0
		 18 0 20 0 22 0 24 0 25 0;
	setAttr -s 14 ".kit[13]"  1;
	setAttr -s 14 ".kot[0:13]"  1 18 18 18 18 18 18 18 
		18 18 18 18 18 1;
	setAttr -s 14 ".kix[13]"  1;
	setAttr -s 14 ".kiy[13]"  0;
	setAttr -s 14 ".kox[0:13]"  1 1 1 1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 14 ".koy[0:13]"  0 0 0 0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE549";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021F10";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 13 ".ktv[0:12]"  1 0 3 0 6 0 8 0 10 0 12 0 13 0 15 0 18 0
		 20 0 22 0 24 0 25 0;
	setAttr -s 13 ".kit[12]"  1;
	setAttr -s 13 ".kot[0:12]"  1 18 18 18 18 18 18 18 
		18 18 18 18 1;
	setAttr -s 13 ".kix[12]"  1;
	setAttr -s 13 ".kiy[12]"  0;
	setAttr -s 13 ".kox[0:12]"  1 1 1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 13 ".koy[0:12]"  0 0 0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE550";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021F0E";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 13 ".ktv[0:12]"  1 0 3 0 6 0 8 5.0553935860053958 10 11.847552335066473 12 19.548725193956308
		 13 25.5 15 49.202058087359966 18 0 20 0 22 0 24 0.90864917395458611 25 0;
	setAttr -s 13 ".kit[12]"  1;
	setAttr -s 13 ".kot[0:12]"  1 18 18 18 18 18 18 18 
		18 18 18 18 1;
	setAttr -s 13 ".kix[12]"  1;
	setAttr -s 13 ".kiy[12]"  0;
	setAttr -s 13 ".kox[0:12]"  1 1 1 0.014066211563838284 0.011498781116257054 0.0091554836193396532 0.0042153403084920198 1 1 1 
		1 1 1;
	setAttr -s 13 ".koy[0:12]"  0 0 0 0.99990106595214767 0.99993388683094464 0.99995808768152672 0.99999111541357388 0 0 0 
		0 0 0;
createNode animCurveTU -n "CURVE551";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021F12";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 13 ".ktv[0:12]"  1 0 3 0 6 0 8 0 10 0 12 0 13 0 15 0 18 0
		 20 0 22 0 24 0 25 0;
	setAttr -s 13 ".kit[12]"  1;
	setAttr -s 13 ".kot[0:12]"  1 18 18 18 18 18 18 18 
		18 18 18 18 1;
	setAttr -s 13 ".kix[12]"  1;
	setAttr -s 13 ".kiy[12]"  0;
	setAttr -s 13 ".kox[0:12]"  1 1 1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 13 ".koy[0:12]"  0 0 0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE552";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021F11";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 13 ".ktv[0:12]"  1 0 3 0 6 0 8 0 10 0 12 0 13 0 15 0 18 0
		 20 0 22 0 24 0 25 0;
	setAttr -s 13 ".kit[12]"  1;
	setAttr -s 13 ".kot[0:12]"  1 18 18 18 18 18 18 18 
		18 18 18 18 1;
	setAttr -s 13 ".kix[12]"  1;
	setAttr -s 13 ".kiy[12]"  0;
	setAttr -s 13 ".kox[0:12]"  1 1 1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 13 ".koy[0:12]"  0 0 0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE553";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021F15";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 13 ".ktv[0:12]"  1 0 3 0 6 0 8 0 10 0 12 0 13 0 15 0 18 0
		 20 0 22 0 24 0 25 0;
	setAttr -s 13 ".kit[12]"  1;
	setAttr -s 13 ".kot[0:12]"  1 18 18 18 18 18 18 18 
		18 18 18 18 1;
	setAttr -s 13 ".kix[12]"  1;
	setAttr -s 13 ".kiy[12]"  0;
	setAttr -s 13 ".kox[0:12]"  1 1 1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 13 ".koy[0:12]"  0 0 0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE554";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021F0B";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 13 ".ktv[0:12]"  1 0 3 0 6 0 8 0 10 0 12 0 13 0 15 0 18 0
		 20 0 22 0 24 0 25 0;
	setAttr -s 13 ".kit[12]"  1;
	setAttr -s 13 ".kot[0:12]"  1 18 18 18 18 18 18 18 
		18 18 18 18 1;
	setAttr -s 13 ".kix[12]"  1;
	setAttr -s 13 ".kiy[12]"  0;
	setAttr -s 13 ".kox[0:12]"  1 1 1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 13 ".koy[0:12]"  0 0 0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE555";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021F21";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 13 ".ktv[0:12]"  1 1 3 1 6 1 8 1 10 1 12 1 13 1 15 1 18 1
		 20 1 22 1 24 1 25 1;
	setAttr -s 13 ".kit[12]"  1;
	setAttr -s 13 ".kot[0:12]"  1 18 18 18 18 18 18 18 
		18 18 18 18 1;
	setAttr -s 13 ".kix[12]"  1;
	setAttr -s 13 ".kiy[12]"  0;
	setAttr -s 13 ".kox[0:12]"  1 1 1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 13 ".koy[0:12]"  0 0 0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE556";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021F22";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 13 ".ktv[0:12]"  1 1 3 1 6 1 8 1 10 1 12 1 13 1 15 1 18 1
		 20 1 22 1 24 1 25 1;
	setAttr -s 13 ".kit[12]"  1;
	setAttr -s 13 ".kot[0:12]"  1 18 18 18 18 18 18 18 
		18 18 18 18 1;
	setAttr -s 13 ".kix[12]"  1;
	setAttr -s 13 ".kiy[12]"  0;
	setAttr -s 13 ".kox[0:12]"  1 1 1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 13 ".koy[0:12]"  0 0 0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE557";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021F23";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 13 ".ktv[0:12]"  1 1 3 1 6 1 8 1 10 1 12 1 13 1 15 1 18 1
		 20 1 22 1 24 1 25 1;
	setAttr -s 13 ".kit[12]"  1;
	setAttr -s 13 ".kot[0:12]"  1 18 18 18 18 18 18 18 
		18 18 18 18 1;
	setAttr -s 13 ".kix[12]"  1;
	setAttr -s 13 ".kiy[12]"  0;
	setAttr -s 13 ".kox[0:12]"  1 1 1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 13 ".koy[0:12]"  0 0 0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE558";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021F1E";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 13 ".ktv[0:12]"  1 0 3 0 6 0 8 0 10 0 12 0 13 0 15 0 18 0
		 20 0 22 0 24 0 25 0;
	setAttr -s 13 ".kit[12]"  1;
	setAttr -s 13 ".kot[0:12]"  1 18 18 18 18 18 18 18 
		18 18 18 18 1;
	setAttr -s 13 ".kix[12]"  1;
	setAttr -s 13 ".kiy[12]"  0;
	setAttr -s 13 ".kox[0:12]"  1 1 1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 13 ".koy[0:12]"  0 0 0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE559";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021F1F";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 13 ".ktv[0:12]"  1 0 3 0 6 0 8 0 10 0 12 0 13 0 15 0 18 0
		 20 0 22 0 24 0 25 0;
	setAttr -s 13 ".kit[12]"  1;
	setAttr -s 13 ".kot[0:12]"  1 18 18 18 18 18 18 18 
		18 18 18 18 1;
	setAttr -s 13 ".kix[12]"  1;
	setAttr -s 13 ".kiy[12]"  0;
	setAttr -s 13 ".kox[0:12]"  1 1 1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 13 ".koy[0:12]"  0 0 0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE560";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021F20";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 13 ".ktv[0:12]"  1 0 3 0 6 0 8 0 10 0 12 0 13 0 15 0 18 0
		 20 0 22 0 24 0 25 0;
	setAttr -s 13 ".kit[12]"  1;
	setAttr -s 13 ".kot[0:12]"  1 18 18 18 18 18 18 18 
		18 18 18 18 1;
	setAttr -s 13 ".kix[12]"  1;
	setAttr -s 13 ".kiy[12]"  0;
	setAttr -s 13 ".kox[0:12]"  1 1 1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 13 ".koy[0:12]"  0 0 0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE561";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021F0C";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 13 ".ktv[0:12]"  1 45 3 45 6 45 8 45 10 45 12 45 13 45 15 45
		 18 45 20 45 22 45 24 45 25 45;
	setAttr -s 13 ".kit[12]"  1;
	setAttr -s 13 ".kot[0:12]"  1 18 18 18 18 18 18 18 
		18 18 18 18 1;
	setAttr -s 13 ".kix[12]"  1;
	setAttr -s 13 ".kiy[12]"  0;
	setAttr -s 13 ".kox[0:12]"  1 1 1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 13 ".koy[0:12]"  0 0 0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE562";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021F18";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 13 ".ktv[0:12]"  1 0 3 0 6 0 8 0 10 0 12 0 13 0 15 0 18 0
		 20 0 22 0 24 0 25 0;
	setAttr -s 13 ".kit[12]"  1;
	setAttr -s 13 ".kot[0:12]"  1 18 18 18 18 18 18 18 
		18 18 18 18 1;
	setAttr -s 13 ".kix[12]"  1;
	setAttr -s 13 ".kiy[12]"  0;
	setAttr -s 13 ".kox[0:12]"  1 1 1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 13 ".koy[0:12]"  0 0 0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE563";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021F1B";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 13 ".ktv[0:12]"  1 -3.9611037234042552 3 -3.9611037234042552 6 -3.9611037234042552 8 -3.9611037234042552 10 -3.9611037234042552
		 12 -3.9611037234042552 13 -3.9611037234042552 15 -3.9611037234042552 18 -3.9611037234042552 20 -3.9611037234042552 22 -3.9611037234042552 24 -3.9611037234042552 25 -3.9611037234042552;
	setAttr -s 13 ".kit[12]"  1;
	setAttr -s 13 ".kot[0:12]"  1 18 18 18 18 18 18 18 
		18 18 18 18 1;
	setAttr -s 13 ".kix[12]"  1;
	setAttr -s 13 ".kiy[12]"  0;
	setAttr -s 13 ".kox[0:12]"  1 1 1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 13 ".koy[0:12]"  0 0 0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE564";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021F1C";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 13 ".ktv[0:12]"  1 -0.33631908556432782 3 -0.33631908556432782 6 -0.33631908556432782 8 -0.33631908556432782 10 -0.33631908556432782
		 12 -0.33631908556432782 13 -0.33631908556432782 15 3.5630800421865256 18 26.880096110186852 20 12.19384740163329 22 3.41764697949659 24 0.45695639303020297 25 -0.33631908556432782;
	setAttr -s 13 ".kit[12]"  1;
	setAttr -s 13 ".kot[0:12]"  1 18 18 18 18 18 18 18 
		18 18 18 18 1;
	setAttr -s 13 ".kix[12]"  1;
	setAttr -s 13 ".kiy[12]"  0;
	setAttr -s 13 ".kox[0:12]"  1 1 1 1 1 1 1 0.0076544698677573084 1 0.0071033701922140254 0.014198808286163151 0.033279672117954295 
		1;
	setAttr -s 13 ".koy[0:12]"  0 0 0 0 0 0 0 0.99997070411639744 0 -0.99997477074769858 -0.99989919184048393 -0.99944607829723431 
		0;
createNode animCurveTL -n "CURVE565";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021F1D";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 36.893102550718105 12 -28.744295191463912 13 -34.711331349843725 15 -46.645403666604373 16 -49.410843550997441
		 17 -44.684102621560989 18 -31.099248719040389 20 5.7256823731851458 22 32.997175028526485 24 39.777488554075717 25 36.893102550718105;
	setAttr -s 11 ".kit[0:10]"  2 2 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kot[0:10]"  1 2 18 18 18 18 18 18 
		18 18 2;
	setAttr -s 11 ".kix[10]"  0.014444086158805497;
	setAttr -s 11 ".kiy[10]"  -0.99989567874605656;
	setAttr -s 11 ".kox[0:10]"  0.0069826375729593656 0.0069826375729597568 0.006982637572959363 0.0085033760981317996 1 0.0045508035310266723 0.0024796696854554687 
		0.0026002402861763224 0.0048944443496054535 1 1;
	setAttr -s 11 ".koy[0:10]"  -0.99997562108909666 -0.99997562108909677 -0.99997562108909654 -0.99996384564389806 0 0.99998964503999843 0.99999692561439957 
		0.9999966193695129 0.99998802213551963 0 0;
createNode animCurveTU -n "CURVE566";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021F0F";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 15 ".ktv[0:14]"  1 -16.264052943330874 2 0 3 0 6 0 8 0 10 0 12 0 12.999999829931973 0
		 13 0 15 9.256077348066281 18 59.100000000000009 20 26.827696793004169 22 -8.9616887140989228 24 -27.7659485584274 25 -16.264052943330874;
	setAttr -s 15 ".kit[14]"  1;
	setAttr -s 15 ".kot[0:14]"  1 18 18 18 18 18 18 18 
		18 18 18 18 18 18 1;
	setAttr -s 15 ".kix[14]"  0.0030012645828005838;
	setAttr -s 15 ".kiy[14]"  0.99999549619530992;
	setAttr -s 15 ".kox[0:14]"  1 1 1 1 1 1 1 1 1 0.0035250768009640167 1 0.0024487515681153806 0.0030528441348295255 
		1 1;
	setAttr -s 15 ".koy[0:14]"  0 0 0 0 0 0 0 0 0 0.9999937868974722 0 -0.99999700180338424 -0.99999534006048674 
		0 0;
createNode animCurveTU -n "CURVE567";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021F14";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 13 ".ktv[0:12]"  1 0 3 0 6 0 8 0 10 0 12 0 13 0 15 0 18 0
		 20 0 22 0 24 0 25 0;
	setAttr -s 13 ".kit[12]"  1;
	setAttr -s 13 ".kot[0:12]"  1 18 18 18 18 18 18 18 
		18 18 18 18 1;
	setAttr -s 13 ".kix[12]"  1;
	setAttr -s 13 ".kiy[12]"  0;
	setAttr -s 13 ".kox[0:12]"  1 1 1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 13 ".koy[0:12]"  0 0 0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE568";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021F13";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 13 ".ktv[0:12]"  1 0 3 0 6 0 8 0 10 0 12 0 13 0 15 0 18 0
		 20 0 22 0 24 0 25 0;
	setAttr -s 13 ".kit[12]"  1;
	setAttr -s 13 ".kot[0:12]"  1 18 18 18 18 18 18 18 
		18 18 18 18 1;
	setAttr -s 13 ".kix[12]"  1;
	setAttr -s 13 ".kiy[12]"  0;
	setAttr -s 13 ".kox[0:12]"  1 1 1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 13 ".koy[0:12]"  0 0 0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE569";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021F16";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 13 ".ktv[0:12]"  1 0 3 0 6 0 8 0 10 0 12 0 13 0 15 0 18 0
		 20 0 22 0 24 0 25 0;
	setAttr -s 13 ".kit[12]"  1;
	setAttr -s 13 ".kot[0:12]"  1 18 18 18 18 18 18 18 
		18 18 18 18 1;
	setAttr -s 13 ".kix[12]"  1;
	setAttr -s 13 ".kiy[12]"  0;
	setAttr -s 13 ".kox[0:12]"  1 1 1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 13 ".koy[0:12]"  0 0 0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE570";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021F17";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 13 ".ktv[0:12]"  1 0 3 0 6 0 8 0 10 0 12 0 13 0 15 0 18 0
		 20 0 22 0 24 0 25 0;
	setAttr -s 13 ".kit[12]"  1;
	setAttr -s 13 ".kot[0:12]"  1 18 18 18 18 18 18 18 
		18 18 18 18 1;
	setAttr -s 13 ".kix[12]"  1;
	setAttr -s 13 ".kiy[12]"  0;
	setAttr -s 13 ".kox[0:12]"  1 1 1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 13 ".koy[0:12]"  0 0 0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE571";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021F19";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 13 ".ktv[0:12]"  1 0 3 0 6 0 8 0 10 0 12 0 13 0 15 0 18 0
		 20 0 22 0 24 0 25 0;
	setAttr -s 13 ".kit[12]"  1;
	setAttr -s 13 ".kot[0:12]"  1 18 18 18 18 18 18 18 
		18 18 18 18 1;
	setAttr -s 13 ".kix[12]"  1;
	setAttr -s 13 ".kiy[12]"  0;
	setAttr -s 13 ".kox[0:12]"  1 1 1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 13 ".koy[0:12]"  0 0 0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE572";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021F0D";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 13 ".ktv[0:12]"  1 90 3 90 6 90 8 90 10 90 12 90 13 90 15 90
		 18 90 20 90 22 90 24 90 25 90;
	setAttr -s 13 ".kit[12]"  1;
	setAttr -s 13 ".kot[0:12]"  1 18 18 18 18 18 18 18 
		18 18 18 18 1;
	setAttr -s 13 ".kix[12]"  1;
	setAttr -s 13 ".kiy[12]"  0;
	setAttr -s 13 ".kox[0:12]"  1 1 1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 13 ".koy[0:12]"  0 0 0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE573";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021F1A";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 13 ".ktv[0:12]"  1 0 3 0 6 0 8 0 10 0 12 0 13 0 15 0 18 0
		 20 0 22 0 24 0 25 0;
	setAttr -s 13 ".kit[12]"  1;
	setAttr -s 13 ".kot[0:12]"  1 18 18 18 18 18 18 18 
		18 18 18 18 1;
	setAttr -s 13 ".kix[12]"  1;
	setAttr -s 13 ".kiy[12]"  0;
	setAttr -s 13 ".kox[0:12]"  1 1 1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 13 ".koy[0:12]"  0 0 0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE575";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021F25";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE576";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021F26";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE577";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021F27";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE578";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021F28";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE579";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021F2C";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1.0000000000000002 3 1.0000000000000002 6 1.0000000000000002 8 1.0000000000000002 10 1.0000000000000002
		 13 1.0000000000000002 15 1.0000000000000002 18 1.0000000000000002 20 1.0000000000000002 22 1.0000000000000002 25 1.0000000000000002;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE580";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021F2D";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1.0000000000000002 3 1.0000000000000002 6 1.0000000000000002 8 1.0000000000000002 10 1.0000000000000002
		 13 1.0000000000000002 15 1.0000000000000002 18 1.0000000000000002 20 1.0000000000000002 22 1.0000000000000002 25 1.0000000000000002;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE581";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021F2E";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1.0000000000000004 3 1.0000000000000004 6 1.0000000000000004 8 1.0000000000000004 10 1.0000000000000004
		 13 1.0000000000000004 15 1.0000000000000004 18 1.0000000000000004 20 1.0000000000000004 22 1.0000000000000004 25 1.0000000000000004;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE582";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021F29";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE583";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021F2A";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE584";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021F2B";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 -24.183597580285252 3 -24.183597580285252 6 -24.183597580285252 8 -24.183597580285252 10 -24.183597580285252
		 13 -24.183597580285252 15 -24.183597580285252 18 -24.183597580285252 20 -24.183597580285252 22 -24.183597580285252 25 -24.183597580285252;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE586";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021F30";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE587";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021F31";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 1.3154153666531898 6 2.6308307333063796 8 2.4898396874481095 10 1.6598889752325938
		 13 0 15 -1.3155 18 -2.631 20 -2.49 22 -1.6599958500000001 25 0;
	setAttr -s 11 ".kyts[1:10]" yes no yes yes no yes no yes yes no;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 0.078942048780411334 1 0.19330212597458596 0.083382012975073749 0.069847846293330948 0.078937001651558369 
		1 0.19329030905297323 0.083376681948547873 1;
	setAttr -s 11 ".koy[0:10]"  0 0.99687920679205222 0 -0.98113928068022294 -0.9965176565983288 -0.99755765666360519 -0.99687960645719997 
		0 0.98114160875288858 0.99651810264904406 0;
createNode animCurveTL -n "CURVE588";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021F32";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 21 ".ktv[0:20]"  1 -2.951696651869931 2 -4.5504006997639772 3 -5.0853210627669556 4 -4.7162607683376701 5 -3.7518869586669106
		 6 -2.3509889149691632 8 -0.56073352989324754 10 -0.049881445394944275 11 -0.38161920045705661 12 -1.3964287299750744 13 -2.951696651869931 14 -4.4952547358568973 15 -5.0853210627669556 16 -4.7163083558565617
		 17 -3.7520229230065958 18 -2.351172466827737 20 -0.56073352989324754 22 -0.049881445394944275 23 -0.41436057208854465 24 -1.4619862115284836 25 -2.951696651869931;
	setAttr -s 21 ".kit[20]"  1;
	setAttr -s 21 ".kot[0:20]"  1 18 18 18 18 18 18 18 
		18 18 18 18 18 18 18 18 18 18 18 18 1;
	setAttr -s 21 ".kix[20]"  0.01831033531854857;
	setAttr -s 21 ".kiy[20]"  -0.99983235175729446;
	setAttr -s 21 ".kox[0:20]"  1 0.039027414850465167 1 0.062373590421300924 0.035210185520909147 0.039140773415789927 0.07223965822141272 
		1 0.061768501957013285 0.032407413159495607 0.02688218610413301 0.039027414850465181 1 0.062379926277732936 0.035212207135823237 0.039139108384400725 0.072233926423534933 1 0.058911070119888893 0.032825145424391827 1;
	setAttr -s 21 ".koy[0:20]"  0 -0.99923814022989021 0 0.99805287195516645 0.99937992917387675 0.99923370632520891 0.99738730279668875 
		0 -0.99809050299358448 -0.99947474183808649 -0.99963860873330757 -0.99923814022989021 0 0.99805247597387614 0.99937985794622863 0.99923377154441406 0.99738771792790748 0 -0.99826323473186651 -0.99946110971256286 0;
createNode animCurveTL -n "CURVE589";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021F33";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 -0.38618716021801447 3 -0.38618716021801447 6 -0.38618716021801447 8 -0.38618716021801447 10 -0.38618716021801447
		 13 -0.38618716021801447 15 -0.38618716021801447 18 -0.38618716021801447 20 -0.38618716021801447 22 -0.38618716021801447 25 -0.38618716021801447;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE590";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021F37";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1 3 1 6 1 8 1 10 1 13 1 15 1 18 1 20 1
		 22 1 25 1;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE591";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021F38";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1 3 1 6 1 8 1 10 1 13 1 15 1 18 1 20 1
		 22 1 25 1;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE592";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021F39";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1 3 1 6 1 8 1 10 1 13 1 15 1 18 1 20 1
		 22 1 25 1;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE593";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021F34";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE594";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021F35";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE595";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021F36";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 9 ".ktv[0:8]"  1 -0.23599999999999996 3 1.7570000000000001 6 3.7499999999999996 10 2.4999937499999998 13 0.23599999999999988
		 15 -1.7569999999999997 18 -3.7499999999999991 22 -2.4999937499999998 25 -0.23599999999999996;
	setAttr -s 9 ".kyts[1:8]" yes no yes no yes no yes no;
	setAttr -s 9 ".kit[8]"  1;
	setAttr -s 9 ".kot[0:8]"  1 18 18 18 18 18 18 18 
		1;
	setAttr -s 9 ".kix[8]"  1;
	setAttr -s 9 ".kiy[8]"  0;
	setAttr -s 9 ".kox[0:8]"  1 0.94851327622244741 1 0.97859888856070176 0.94189390257904904 0.94851327622244741 1 0.97859888856070176 
		1;
	setAttr -s 9 ".koy[0:8]"  0 0.31673737517028078 0 -0.20577710102865943 -0.3359105182699833 -0.31673737517028067 0 0.20577710102865929 
		0;
createNode animCurveTU -n "CURVE597";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021F3B";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE598";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021F3C";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE599";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021F3D";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE600";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021F3E";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE601";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021F3F";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE602";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021F40";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE603";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021F41";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE605";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021F43";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE606";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021F44";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE607";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021F45";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE608";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021F46";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE609";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021F4A";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1.0000000000000002 3 1.0000000000000002 6 1.0000000000000002 8 1.0000000000000002 10 1.0000000000000002
		 13 1.0000000000000002 15 1.0000000000000002 18 1.0000000000000002 20 1.0000000000000002 22 1.0000000000000002 25 1.0000000000000002;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE610";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021F4B";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1 3 1 6 1 8 1 10 1 13 1 15 1 18 1 20 1
		 22 1 25 1;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE611";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021F4C";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1 3 1 6 1 8 1 10 1 13 1 15 1 18 1 20 1
		 22 1 25 1;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE612";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021F47";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE613";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021F48";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 6.4680312672739753 3 6.4680312672739753 6 6.4680312672739753 8 6.4680312672739753 10 6.4680312672739753
		 13 6.4680312672739753 15 6.4680312672739753 18 6.4680312672739753 20 6.4680312672739753 22 6.4680312672739753 25 6.4680312672739753;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE614";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021F49";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE616";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021F4E";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0 20 0 25 0;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTL -n "CURVE617";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021F4F";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0 20 -1.4210854715202004e-14 25 0;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTL -n "CURVE618";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021F50";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 -1.4210854715202004e-14 20 1.4210854715202004e-14 25 -1.4210854715202004e-14;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTL -n "CURVE619";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021F51";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 2.2204460492503131e-16 20 0 25 2.2204460492503131e-16;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTU -n "CURVE620";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021F55";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 1.0000000000000002 20 1.0000000000000009 25 1.0000000000000002;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTU -n "CURVE621";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021F56";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 1.0000000000000002 20 1.0000000000000011 25 1.0000000000000002;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTU -n "CURVE622";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021F57";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 1.0000000000000004 20 1.0000000000000007 25 1.0000000000000004;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTA -n "CURVE623";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021F52";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0 20 0 25 0;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTA -n "CURVE624";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021F53";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0 20 0 25 0;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTA -n "CURVE625";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021F54";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 -48.274488841200522 20 -48.274488841200522 25 -48.274488841200522;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTU -n "CURVE627";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021F59";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0 20 0 25 0;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTL -n "CURVE628";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021F5A";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 1.4210854715202004e-14 20 0 25 1.4210854715202004e-14;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTL -n "CURVE629";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021F5B";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 -1.4210854715202004e-14 20 0 25 -1.4210854715202004e-14;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTL -n "CURVE630";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021F5C";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 2.2204460492503131e-16 20 0 25 2.2204460492503131e-16;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTU -n "CURVE631";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021F60";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 1.0000000000000002 20 1.0000000000000004 25 1.0000000000000002;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTU -n "CURVE632";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021F61";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 1.0000000000000002 20 1.0000000000000007 25 1.0000000000000002;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTU -n "CURVE633";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021F62";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 1.0000000000000004 20 1.0000000000000004 25 1.0000000000000004;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTA -n "CURVE634";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021F5D";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0 20 0 25 0;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTA -n "CURVE635";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021F5E";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0 20 0 25 0;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTA -n "CURVE636";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021F5F";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 -60.017584779578563 20 -60.017584779578563 25 -60.017584779578563;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTU -n "CURVE638";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021F64";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 9 ".ktv[0:8]"  1 0 6 0 8 0 13 0 15 0 18 0 20 0 22 0 25 0;
	setAttr -s 9 ".kit[8]"  1;
	setAttr -s 9 ".kot[0:8]"  1 18 18 18 18 18 18 18 
		1;
	setAttr -s 9 ".kix[8]"  1;
	setAttr -s 9 ".kiy[8]"  0;
	setAttr -s 9 ".kox[0:8]"  1 1 1 1 1 1 1 1 1;
	setAttr -s 9 ".koy[0:8]"  0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE639";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021F65";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 9 ".ktv[0:8]"  1 0 6 0 8 0 13 0 15 0 18 0 20 0 22 0 25 0;
	setAttr -s 9 ".kit[8]"  1;
	setAttr -s 9 ".kot[0:8]"  1 18 18 18 18 18 18 18 
		1;
	setAttr -s 9 ".kix[8]"  1;
	setAttr -s 9 ".kiy[8]"  0;
	setAttr -s 9 ".kox[0:8]"  1 1 1 1 1 1 1 1 1;
	setAttr -s 9 ".koy[0:8]"  0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE640";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021F66";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 9 ".ktv[0:8]"  1 0 6 0 8 0 13 0 15 0 18 0 20 0 22 0 25 0;
	setAttr -s 9 ".kit[8]"  1;
	setAttr -s 9 ".kot[0:8]"  1 18 18 18 18 18 18 18 
		1;
	setAttr -s 9 ".kix[8]"  1;
	setAttr -s 9 ".kiy[8]"  0;
	setAttr -s 9 ".kox[0:8]"  1 1 1 1 1 1 1 1 1;
	setAttr -s 9 ".koy[0:8]"  0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE641";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021F67";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 9 ".ktv[0:8]"  1 0 6 0 8 0 13 0 15 0 18 0 20 0 22 0 25 0;
	setAttr -s 9 ".kit[8]"  1;
	setAttr -s 9 ".kot[0:8]"  1 18 18 18 18 18 18 18 
		1;
	setAttr -s 9 ".kix[8]"  1;
	setAttr -s 9 ".kiy[8]"  0;
	setAttr -s 9 ".kox[0:8]"  1 1 1 1 1 1 1 1 1;
	setAttr -s 9 ".koy[0:8]"  0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE642";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021F68";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 9 ".ktv[0:8]"  1 27.159847915894265 3 26.858370873464523 6 27.508994346479859 12.999999829931973 31.852191284509704
		 13 31.852191390029503 15 32.81088764043507 18 30.772976564553094 20 29.274554577276618 25 27.159847915894265;
	setAttr -s 9 ".kit[8]"  1;
	setAttr -s 9 ".kot[0:8]"  1 18 18 18 18 18 18 18 
		1;
	setAttr -s 9 ".kix[8]"  1;
	setAttr -s 9 ".kiy[8]"  0;
	setAttr -s 9 ".kox[0:8]"  1 1 0.97881449717270963 0.96784694419528694 0.98043165499380092 1 0.95880781446460817 0.97741559957015944 
		1;
	setAttr -s 9 ".koy[0:8]"  0 0 0.2047490662360531 0.25153984299081761 0.19685977213772379 0 -0.28405558421126192 -0.21132615956597955 
		0;
createNode animCurveTA -n "CURVE643";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021F69";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 9 ".ktv[0:8]"  1 6.206277544716289 6 6.206277544716289 8 6.206277544716289 13 6.206277544716289 15 6.206277544716289
		 18 6.206277544716289 20 6.206277544716289 22 6.206277544716289 25 6.206277544716289;
	setAttr -s 9 ".kit[8]"  1;
	setAttr -s 9 ".kot[0:8]"  1 18 18 18 18 18 18 18 
		1;
	setAttr -s 9 ".kix[8]"  1;
	setAttr -s 9 ".kiy[8]"  0;
	setAttr -s 9 ".kox[0:8]"  1 1 1 1 1 1 1 1 1;
	setAttr -s 9 ".koy[0:8]"  0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE644";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021F6A";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 9 ".ktv[0:8]"  1 -0.51740249432967944 6 -5.2404627173249505 12.999999829931973 1.5522073179582518 13 1.5522074829890398
		 15 8.3844696333566162 18 2.7163630952308191 20 0.51740249432967955 22 0 25 -0.51740249432967944;
	setAttr -s 9 ".kit[8]"  1;
	setAttr -s 9 ".kot[0:8]"  1 18 18 18 18 18 18 18 
		1;
	setAttr -s 9 ".kix[8]"  0.93912295622520625;
	setAttr -s 9 ".kiy[8]"  -0.34358124671004603;
	setAttr -s 9 ".kox[0:8]"  1 1 0.92639470628618581 0.63410925468678081 1 0.83496627424295011 0.96184276914119582 0.99626333039741988 
		1;
	setAttr -s 9 ".koy[0:8]"  0 0 0.37655391136586491 0.77324346303125979 0 -0.55030111836779561 -0.27360279137975962 -0.086367682065928916 
		0;
createNode animCurveTU -n "CURVE646";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021F6C";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0 20 0 25 0;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTL -n "CURVE647";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021F6D";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0 20 1.4210854715202004e-14 25 0;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTL -n "CURVE648";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021F6E";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0 20 0 25 0;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTL -n "CURVE649";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021F6F";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0 20 0 25 0;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTU -n "CURVE650";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021F73";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 1 20 1 25 1;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTU -n "CURVE651";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021F74";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0.99999999999999978 20 0.99999999999999956 25 0.99999999999999978;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTU -n "CURVE652";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021F75";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0.99999999999999978 20 1 25 0.99999999999999978;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTA -n "CURVE653";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021F70";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 14.551420345553764 20 14.551420345553764 25 14.551420345553764;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTA -n "CURVE654";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021F71";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 13.626510510141751 20 13.626510510141751 25 13.626510510141751;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTA -n "CURVE655";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021F72";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 -3.8448947422912889 20 -3.8448947422912889 25 -3.8448947422912889;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTU -n "CURVE657";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021F77";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE658";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021F78";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE659";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021F79";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE660";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021F7A";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE661";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021F7E";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1 3 1 6 1 8 1 10 1 13 1 15 1 18 1 20 1
		 22 1 25 1;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE662";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021F7F";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0.99999999999999989 3 0.99999999999999989 6 0.99999999999999989 8 0.99999999999999989 10 0.99999999999999989
		 13 0.99999999999999989 15 0.99999999999999989 18 0.99999999999999989 20 0.99999999999999989 22 0.99999999999999989 25 0.99999999999999989;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE663";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021F80";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 1 3 1 6 1 8 1 10 1 13 1 15 1 18 1 20 1
		 22 1 25 1;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE664";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021F7B";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE665";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021F7C";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE666";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021F7D";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 -13.281297366785457 3 -13.281297366785457 6 -13.281297366785457 8 -13.281297366785457 10 -13.281297366785457
		 13 -13.281297366785457 15 -13.281297366785457 18 -13.281297366785457 20 -13.281297366785457 22 -13.281297366785457 25 -13.281297366785457;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE668";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021F82";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE669";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021F83";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE670";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021F84";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE671";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021F85";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE672";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021F89";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0.99999999999999978 3 0.99999999999999978 6 0.99999999999999978 8 0.99999999999999978 10 0.99999999999999978
		 13 0.99999999999999978 15 0.99999999999999978 18 0.99999999999999978 20 0.99999999999999978 22 0.99999999999999978 25 0.99999999999999978;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE673";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021F8A";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0.99999999999999911 3 0.99999999999999911 6 0.99999999999999911 8 0.99999999999999911 10 0.99999999999999911
		 13 0.99999999999999911 15 0.99999999999999911 18 0.99999999999999911 20 0.99999999999999911 22 0.99999999999999911 25 0.99999999999999911;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE674";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021F8B";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0.99999999999999967 3 0.99999999999999967 6 0.99999999999999967 8 0.99999999999999967 10 0.99999999999999967
		 13 0.99999999999999967 15 0.99999999999999967 18 0.99999999999999967 20 0.99999999999999967 22 0.99999999999999967 25 0.99999999999999967;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE675";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021F86";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE676";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021F87";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE677";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021F88";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 -19.88365918056531 3 -19.88365918056531 6 -19.88365918056531 8 -19.88365918056531 10 -19.88365918056531
		 13 -19.88365918056531 15 -19.88365918056531 18 -19.88365918056531 20 -19.88365918056531 22 -19.88365918056531 25 -19.88365918056531;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE679";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021F8D";
	setAttr ".tan" 1;
	setAttr ".wgt" no;
	setAttr -s 2 ".ktv[0:1]"  1 0.025543644214023827 25 0.025543644214023827;
	setAttr -s 2 ".kit[0:1]"  18 1;
	setAttr -s 2 ".kix[1]"  1;
	setAttr -s 2 ".kiy[1]"  0;
	setAttr -s 2 ".kox[0:1]"  1 1;
	setAttr -s 2 ".koy[0:1]"  0 0;
createNode animCurveTL -n "CURVE680";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021F8E";
	setAttr ".tan" 1;
	setAttr ".wgt" no;
	setAttr -s 2 ".ktv[0:1]"  1 0.0014949268639410348 25 0.0014949268639410348;
	setAttr -s 2 ".kit[0:1]"  18 1;
	setAttr -s 2 ".kix[1]"  1;
	setAttr -s 2 ".kiy[1]"  0;
	setAttr -s 2 ".kox[0:1]"  1 1;
	setAttr -s 2 ".koy[0:1]"  0 0;
createNode animCurveTL -n "CURVE681";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021F8F";
	setAttr ".tan" 1;
	setAttr ".wgt" no;
	setAttr -s 2 ".ktv[0:1]"  1 -0.0019942131665912572 25 -0.0019942131665912572;
	setAttr -s 2 ".kit[0:1]"  18 1;
	setAttr -s 2 ".kix[1]"  1;
	setAttr -s 2 ".kiy[1]"  0;
	setAttr -s 2 ".kox[0:1]"  1 1;
	setAttr -s 2 ".koy[0:1]"  0 0;
createNode animCurveTU -n "CURVE683";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021F91";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0 20 0 25 0;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTL -n "CURVE684";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021F92";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 7.1054273576010019e-15 20 -7.1054273576010019e-15 25 7.1054273576010019e-15;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTL -n "CURVE685";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021F93";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 -1.4210854715202004e-14 20 0 25 -1.4210854715202004e-14;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTL -n "CURVE686";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021F94";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0 20 0 25 0;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTU -n "CURVE687";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021F98";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 1 20 0.99999999999999978 25 1;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTU -n "CURVE688";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021F99";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0.99999999999999978 20 0.99999999999999956 25 0.99999999999999978;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTU -n "CURVE689";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021F9A";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 1.0000000000000002 20 0.99999999999999967 25 1.0000000000000002;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTA -n "CURVE690";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021F95";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0 20 0 25 0;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTA -n "CURVE691";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021F96";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0 20 0 25 0;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTA -n "CURVE692";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021F97";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0 20 0 25 0;
	setAttr -s 3 ".kit[2]"  1;
	setAttr -s 3 ".kot[0:2]"  1 18 1;
	setAttr -s 3 ".kix[2]"  1;
	setAttr -s 3 ".kiy[2]"  0;
	setAttr -s 3 ".kox[0:2]"  1 1 1;
	setAttr -s 3 ".koy[0:2]"  0 0 0;
createNode animCurveTU -n "CURVE694";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021F9C";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE695";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021F9D";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE696";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021F9E";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE697";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021F9F";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE698";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021FA3";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0.99999999999999978 3 0.99999999999999978 6 0.99999999999999978 8 0.99999999999999978 10 0.99999999999999978
		 13 0.99999999999999978 15 0.99999999999999978 18 0.99999999999999978 20 0.99999999999999978 22 0.99999999999999978 25 0.99999999999999978;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE699";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021FA4";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0.99999999999999989 3 0.99999999999999989 6 0.99999999999999989 8 0.99999999999999989 10 0.99999999999999989
		 13 0.99999999999999989 15 0.99999999999999989 18 0.99999999999999989 20 0.99999999999999989 22 0.99999999999999989 25 0.99999999999999989;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE700";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021FA5";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0.99999999999999967 3 0.99999999999999967 6 0.99999999999999967 8 0.99999999999999967 10 0.99999999999999967
		 13 0.99999999999999967 15 0.99999999999999967 18 0.99999999999999967 20 0.99999999999999967 22 0.99999999999999967 25 0.99999999999999967;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE701";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021FA0";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE702";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021FA1";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 0 3 0 6 0 8 0 10 0 13 0 15 0 18 0 20 0
		 22 0 25 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE703";
	rename -uid "B7197D80-0000-6BA2-657C-B40C00021FA2";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  1 -3.6408012963077039 3 -3.6408012963077039 6 -3.6408012963077039 8 -3.6408012963077039 10 -3.6408012963077039
		 13 -3.6408012963077039 15 -3.6408012963077039 18 -3.6408012963077039 20 -3.6408012963077039 22 -3.6408012963077039 25 -3.6408012963077039;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 18 18 18 18 18 18 18 
		18 18 1;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 1 1 1 1 1 1 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0 0 0 0 0 0 0 0 0;
// End