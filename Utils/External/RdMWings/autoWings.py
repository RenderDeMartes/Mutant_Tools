from __future__ import absolute_import
# AutoWings
'''
version: 1.0.0

date: 21/04/2020

how to: 
CreateJoints()  #position base joints in place
buildWingsRef(ScapAmount, ScaptBack, SecAmount, SecBack, PrimAmount, PrimBack) #position feathers 
buildWingsSystem(ScapAmount, ScaptBack, SecAmount, SecBack, PrimAmount, PrimBack,sizeUI)  #crete the rig

mirrorWing() #mirror all system

rebuildLeftWing() #Return to buildWingsRef()

dependencies:   
math
cmds
pymel
wingModule

licence: EULA 
         https://www.eulatemplate.com/live.php?token=uvtn9mOrCrX6m7CkXYA1EPZOFrBTEj67

author:  Esteban Rodriguez <info@renderdemartes.com>


'''

from maya import cmds
import maya.mel as mel
try:
    import importlib;from importlib import reload
except:
    import imp;from imp import reload
import Mutant_Tools
from Mutant_Tools.Utils.External.RdMWings import wingModule, GlobalAttr
reload(wingModule)
reload(GlobalAttr)

import Mutant_Tools.Utils.Rigging
from Mutant_Tools.Utils.Rigging import main_mutant
reload(Mutant_Tools.Utils.Rigging.main_mutant)

mt = main_mutant.Mutant()
nc, curve_data, setup = mt.import_configs()


# *********************************************************************

def CreateJoints(*args):

    cmds.select(cl=True)

    LeftArmsJoints = []
    LeftArmsJoints.append(cmds.joint(p=(0.5, 0, 0), n='L_Clav_Guide'))
    LeftArmsJoints.append(cmds.joint(p=(5, 0, 0), n='L_Scapulars_Guide'))
    LeftArmsJoints.append(cmds.joint(p=(20, 0, -2), n='L_Secondaries_Guide'))
    LeftArmsJoints.append(cmds.joint(p=(35, 0, 1), n='L_Primaries_Guide'))
    LeftArmsJoints.append(cmds.joint(p=(45, 0, 1), n='L_End_Guide'))
    # LeftArmsJoints.append(cmds.joint(p=(50, 0, 0), n = 'L_End_JE'))

    for i in LeftArmsJoints:
        cmds.joint(i, e=True, zso=True, oj="xzy", sao='zup')

    return LeftArmsJoints



# ***********************************************************************

def buildWingsRef(ScapAmount, ScaptBack, SecAmount, SecBack, PrimAmount, PrimBack):

    # Orient the joints
    cmds.select('L_Clav_Guide', 'L_Scapulars_Guide', 'L_Secondaries_Guide', 'L_Primaries_Guide')
    cmds.joint(e=True, zso=True, oj="xzy", sao='zup')

    # CreateRef Wings
    wingModule.wingModuleFunc(amount=ScapAmount, Axis='Z', distanceBack=ScaptBack, name1='L_Scapulars_Guide',
                   name2='L_Secondaries_Guide')

    wingModule.wingModuleFunc(amount=SecAmount, Axis='Z', distanceBack=SecBack, name1='L_Secondaries_Guide', name2='L_Primaries_Guide')

    wingModule.wingModuleFunc(amount=PrimAmount, Axis='Z', distanceBack=PrimBack, name1='L_Primaries_Guide', name2='L_End_Guide')



# ***********************************************************************

def buildWingsSystem(ScapAmount, ScaptBack, SecAmount, SecBack, PrimAmount, PrimBack, sizeUI):

    # Orient the joints
    cmds.select('L_Clav_JR', 'L_Scapulars_JR', 'L_Secondaries_JR', 'L_Primaries_JR')
    cmds.joint(e=True, zso=True, oj="xzy", sao='zup')

    # CreateRef Wings
    def buildSystemSide(ScapAmount, ScaptBack, SecAmount, SecBack, PrimAmount, PrimBack, side):

        wingModule.createWings(amount=ScapAmount, Axis='Z', distanceBack=ScaptBack, colorCC=9, name1=str(side) + '_Scapulars_JR',
                    name2=str(side) + '_Secondaries_JR', size=sizeUI)

        wingModule.createWings(amount=SecAmount, Axis='Z', distanceBack=SecBack, colorCC=14, name1=str(side) + '_Secondaries_JR',
                    name2=str(side) + '_Primaries_JR', size=sizeUI)

        wingModule.createWings(amount=PrimAmount, Axis='Z', distanceBack=PrimBack, colorCC=18, name1=str(side) + '_Primaries_JR',
                    name2=str(side) + '_End_JR', size=sizeUI)

        # Clean and organize
        cmds.group(str(side) + '_Scapulars_JR_FeathersPlane', str(side) + '_Secondaries_JR_FeathersPlane',
                   str(side) + '_Primaries_JR_FeathersPlane', n=str(side) + '_Wing_Nurbs_GRP')
        cmds.setAttr(str(side) + '_Wing_Nurbs_GRP.inheritsTransform', 0)

        x = 0
        while cmds.objExists(str(side) + '_Scapulars_JR_Wing_00' + str(x)):
            lastScapular = str(side) + '_Scapulars_JR_Wing_00' + str(x)
            x = x + 1
        cmds.parentConstraint(lastScapular, str(side) + '_Secondaries_JR_Wing_000_Ctrl_Root_Grp', mo=True)

        x = 0
        while cmds.objExists(str(side) + '_Secondaries_JR_Wing_00' + str(x)):
            lastSec = str(side) + '_Secondaries_JR_Wing_00' + str(x)
            x = x + 1
        cmds.parentConstraint(lastSec, str(side) + '_Primaries_JR_Wing_000_Ctrl_Root_Grp', mo=True)

        cmds.group(str(side) + '_Clav_JR', str(side) + '_Scapulars_JR_Wing_000_Ctrl_Root_Grp',
                   str(side) + '_Secondaries_JR_Wing_000_Ctrl_Root_Grp', str(side) + '_Primaries_JR_Wing_000_Ctrl_Root_Grp',
                   str(side) + '_Wing_Nurbs_GRP', str(side) + '_Clav_JR', n=str(side) + '_Wing_AutoRig')

        cmds.parentConstraint(str(side) + '_Clav_JR', str(side) + '_Scapulars_JR_Wing_000_Ctrl_Root_Grp', mo=True)

    buildSystemSide(ScapAmount, ScaptBack, SecAmount, SecBack, PrimAmount, PrimBack, side='L')
    # buildSystemSide(ScapAmount, ScaptBack, SecAmount, SecBack, PrimAmount, PrimBack,side = 'R')

    # Clavicule
    cmds.select(cl=True)
    CC = mt.curve(input='', type='circleX', custom_name=True,
                     name='L_Clavicle'+ nc['ctrl'], tag=False, playback=False)
    mt.assign_color(CC, 'yellow')
    #CC = cmds.circle(n='L_Clavicle_JC', r=2)
    cmds.group(CC, n='L_Clavicle_JC_Root')
    cmds.delete(cmds.parentConstraint('L_Clav_JR', 'L_Clavicle_JC_Root', mo=False))
    cmds.parent('L_Clav_JR', CC)
    cmds.parent('L_Clavicle_JC_Root', 'L_Wing_AutoRig')
    cmds.spaceLocator(n=' GlobalLoc')
    GlobalAttr.globalControl(method='Left', CC='L_Scapulars_JR_Wing_000_Ctrl', GlobalCC='GlobalLoc', AttrName='GlobalRotate',
                  AttrPosition=CC)
    cmds.parent('GlobalLoc', 'L_Wing_AutoRig')

    # Scapulars no rotate
    cmds.addAttr('L_Scapulars_JR_Wing_000_Ctrl', ln="GlobalRotate", at='double', min=0, max=10, dv=0)
    cmds.setAttr('L_Scapulars_JR_Wing_000_Ctrl.GlobalRotate', e=1, keyable=True)

    x = 0
    while cmds.objExists('L_Scapulars_JR_Fthr_00' + str(x) + '_SpreadAuto_Root'):
        cmds.orientConstraint('GlobalLoc', 'L_Scapulars_JR_Wing_000_Ctrl',
                              'L_Scapulars_JR_Fthr_00' + str(x) + '_SpreadAuto_Root', mo=True)
        cmds.connectAttr('L_Scapulars_JR_Wing_000_Ctrl.GlobalRotate',
                         'L_Scapulars_JR_Fthr_00' + str(x) + '_SpreadAuto_Root_orientConstraint1.GlobalLocW0', f=True)
        cmds.setAttr('L_Scapulars_JR_Wing_000_Ctrl.GlobalRotate', 0)

        x = x + 1

    # Wing Curve and Attrs to fold and fly
    cmds.curve(n='L_Wing_CC',
               p=[(0.181341, 2.609773, -0.0599978), (0.803078, 1.394147, -0.0599978), (1.738284, 0.480369, -0.0599978),
                  (2.851947, -0.00134716, -0.0599978), (3.005523, 0.762495, -0.0599978),
                  (3.537822, 0.476033, -0.0599978), (4.064058, 0.282399, -0.0599978), (4.599892, 0.252699, -0.0599978),
                  (5.160986, 0.458036, -0.0599978), (4.851139, 1.417217, -0.0599978), (5.477233, 1.071501, -0.0599978),
                  (6.077058, 0.926849, -0.0599978), (6.66981, 0.997407, -0.0599978), (7.274687, 1.297319, -0.0599978),
                  (6.948842, 1.58797, -0.0599978), (6.704836, 1.832143, -0.0599978), (6.497205, 2.129698, -0.0599978),
                  (6.248147, 2.531322, -0.0599978), (7.379976, 2.063666, -0.0599978), (8.289775, 1.915162, -0.0599978),
                  (9.031852, 2.085179, -0.0599978), (9.660515, 2.573084, -0.0599978), (9.081065, 2.838307, -0.0599978),
                  (8.532938, 3.126768, -0.0599978), (8.053853, 3.486629, -0.0599978), (7.593965, 3.875792, -0.0599978),
                  (9.509191, 3.604948, -0.0599978), (10.964065, 3.797487, -0.0599978),
                  (11.942295, 4.460608, -0.0599978), (12.42759, 5.601509, -0.0599978), (11.4578, 5.489357, -0.0599978),
                  (10.501145, 5.403476, -0.0599978), (9.554594, 5.386299, -0.0599978), (8.607032, 5.44267, -0.0599978),
                  (8.607032, 5.583996, -0.0599978), (10.949983, 6.190262, -0.0599978),
                  (12.834602, 7.221137, -0.0599978), (14.055659, 8.537443, -0.0599978), (14.407922, 10, -0.0599978),
                  (13.846154, 9.618752, -0.0599978), (12.416518, 8.708175, -0.0599978),
                  (10.888118, 8.124579, -0.0599978), (9.276362, 7.813531, -0.0599978), (7.596659, 7.720598, -0.0599978),
                  (6.552859, 7.723692, -0.0599978), (5.508554, 7.723124, -0.0599978), (4.46627, 7.698054, -0.0599978),
                  (3.428533, 7.627644, -0.0599978), (2.073223, 7.253785, -0.0599978), (1.021656, 6.473629, -0.0599978),
                  (0.318415, 5.362829, -0.0599978), (0.00808298, 3.997036, -0.0599978),
                  (0.181341, 2.609773, -0.0599978), (0.803078, 1.394147, -0.0599978), (1.738284, 0.480369, -0.0599978)],
               k=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27,
                  28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52,
                  53, 54], d=1)
    cmds.setAttr("L_Wing_CC.overrideEnabled", 1)
    cmds.setAttr("L_Wing_CC.overrideColor", 16)
    cmds.group(n='L_Wing_CC_Auto')
    wingRoot = cmds.group(n='L_Wing_CC_Root')

    cmds.setAttr("L_Wing_CC.tx", lock=True, channelBox=False, keyable=False)
    cmds.setAttr("L_Wing_CC.ty", lock=True, channelBox=False, keyable=False)
    cmds.setAttr("L_Wing_CC.tz", lock=True, channelBox=False, keyable=False)
    cmds.setAttr("L_Wing_CC.rx", lock=True, channelBox=False, keyable=False)
    cmds.setAttr("L_Wing_CC.ry", lock=True, channelBox=False, keyable=False)
    cmds.setAttr("L_Wing_CC.rz", lock=True, channelBox=False, keyable=False)
    cmds.setAttr("L_Wing_CC.sx", lock=True, channelBox=False, keyable=False)
    cmds.setAttr("L_Wing_CC.sy", lock=True, channelBox=False, keyable=False)
    cmds.setAttr("L_Wing_CC.sz", lock=True, channelBox=False, keyable=False)
    cmds.setAttr("L_Wing_CC.v", lock=True, channelBox=False, keyable=False)

    #cmds.addAttr('L_Wing_CC', ln="WingFold", max=10, dv=0, at='double', min=0)
    #cmds.setAttr('L_Wing_CC.WingFold', e=1, keyable=True)

    cmds.addAttr('L_Wing_CC', ln="ScapularsSwing", dv=0, at='double')
    cmds.setAttr('L_Wing_CC.ScapularsSwing', e=1, keyable=True)
    cmds.addAttr('L_Wing_CC', ln="SecondariesSwing", dv=0, at='double')
    cmds.setAttr('L_Wing_CC.SecondariesSwing', e=1, keyable=True)
    cmds.addAttr('L_Wing_CC', ln="PrimariesSwing", dv=0, at='double')
    cmds.setAttr('L_Wing_CC.PrimariesSwing', e=1, keyable=True)

    cmds.delete(cmds.pointConstraint('L_Scapulars_JR_Wing_000_Ctrl_Root_Grp', wingRoot, mo=False))
    cmds.parent('L_Wing_CC_Root', 'L_Wing_AutoRig')
    cmds.parentConstraint('L_Clav_JR', 'L_Wing_CC_Root', mo=True)

    # Wing Swing
    x = 0
    while cmds.objExists('L_Scapulars_JR_Fthr_00' + str(x) + '_Ctrl_Auto_Grp'):
        cmds.connectAttr('L_Wing_CC.ScapularsSwing', 'L_Scapulars_JR_Fthr_00' + str(x) + '_Ctrl_Auto_Grp.rotateZ', f=True)
        x = x + 1

    x = 0
    while cmds.objExists('L_Secondaries_JR_Fthr_00' + str(x) + '_Ctrl_Auto_Grp'):
        cmds.connectAttr('L_Wing_CC.SecondariesSwing', 'L_Secondaries_JR_Fthr_00' + str(x) + '_Ctrl_Auto_Grp.rotateZ', f=True)
        x = x + 1

    x = 0
    while cmds.objExists('L_Primaries_JR_Fthr_00' + str(x) + '_Ctrl_Auto_Grp'):
        cmds.connectAttr('L_Wing_CC.PrimariesSwing', 'L_Primaries_JR_Fthr_00' + str(x) + '_Ctrl_Auto_Grp.rotateZ', f=True)
        x = x + 1

    cmds.rename('L_Scapulars_JR_Wing_000_Ctrl_Auto_Grp', 'L_Scapulars_JR_Wing_000_Auto2')
    cmds.group(em=True, n='L_Scapulars_JR_Wing_000_Auto')
    cmds.parent('L_Scapulars_JR_Wing_000_Auto', 'L_Scapulars_JR_Wing_000_Ctrl')

    cmds.setAttr("L_Scapulars_JR_Wing_000_Auto.translateX", 0)
    cmds.setAttr("L_Scapulars_JR_Wing_000_Auto.translateY", 0)
    cmds.setAttr("L_Scapulars_JR_Wing_000_Auto.translateZ", 0)
    cmds.setAttr("L_Scapulars_JR_Wing_000_Auto.rotateX", 0)
    cmds.setAttr("L_Scapulars_JR_Wing_000_Auto.rotateY", 0)
    cmds.setAttr("L_Scapulars_JR_Wing_000_Auto.rotateZ", 0)

    cmds.parent('L_Scapulars_JR_Wing_000_Auto', 'L_Scapulars_JR_Wing_000_Ctrl_AutoGlobalRotate')
    cmds.parent('L_Scapulars_JR_Wing_000_Ctrl', 'L_Scapulars_JR_Wing_000_Auto')

    # RefLoc for UI
    if cmds.objExists('WingRef_Loc'):
        print('loc ref exits')

    else:

        cmds.spaceLocator(n='WingRef_Loc')
        cmds.setAttr("WingRef_Loc.tx", lock=True, channelBox=False, keyable=False)
        cmds.setAttr("WingRef_Loc.ty", lock=True, channelBox=False, keyable=False)
        cmds.setAttr("WingRef_Loc.tz", lock=True, channelBox=False, keyable=False)
        cmds.setAttr("WingRef_Loc.rx", lock=True, channelBox=False, keyable=False)
        cmds.setAttr("WingRef_Loc.ry", lock=True, channelBox=False, keyable=False)
        cmds.setAttr("WingRef_Loc.rz", lock=True, channelBox=False, keyable=False)
        cmds.setAttr("WingRef_Loc.sx", lock=True, channelBox=False, keyable=False)
        cmds.setAttr("WingRef_Loc.sy", lock=True, channelBox=False, keyable=False)
        cmds.setAttr("WingRef_Loc.sz", lock=True, channelBox=False, keyable=False)
        cmds.setAttr("WingRef_Loc.v", lock=True, channelBox=False, keyable=False)

        cmds.addAttr('WingRef_Loc', ln="ScapAmount", dv=0, at='double')
        cmds.setAttr('WingRef_Loc.ScapAmount', e=1, keyable=True)
        cmds.addAttr('WingRef_Loc', ln="ScapBack", dv=0, at='double')
        cmds.setAttr('WingRef_Loc.ScapBack', e=1, keyable=True)

        cmds.addAttr('WingRef_Loc', ln="SecAmount", dv=0, at='double')
        cmds.setAttr('WingRef_Loc.SecAmount', e=1, keyable=True)
        cmds.addAttr('WingRef_Loc', ln="SecBack", dv=0, at='double')
        cmds.setAttr('WingRef_Loc.SecBack', e=1, keyable=True)

        cmds.addAttr('WingRef_Loc', ln="PrimAmount", dv=0, at='double')
        cmds.setAttr('WingRef_Loc.PrimAmount', e=1, keyable=True)
        cmds.addAttr('WingRef_Loc', ln="PrimBack", dv=0, at='double')
        cmds.setAttr('WingRef_Loc.PrimBack', e=1, keyable=True)

        cmds.setAttr('WingRef_Loc.ScapAmount', ScapAmount)
        cmds.setAttr('WingRef_Loc.ScapBack', ScaptBack)

        cmds.setAttr('WingRef_Loc.SecAmount', SecAmount)
        cmds.setAttr('WingRef_Loc.SecBack', SecBack)

        cmds.setAttr('WingRef_Loc.PrimAmount', PrimAmount)
        cmds.setAttr('WingRef_Loc.PrimBack', PrimBack)

        cmds.parent('WingRef_Loc', 'L_Wing_AutoRig')

    print('Chaning Pivots')



def mirrorWing():
    cmds.select(cl=True)
    cmds.duplicate('L_Wing_AutoRig', rr=True, un=True)
    cmds.select('L_Wing_AutoRig1')
    mel.eval('searchReplaceNames {} {} "hierarchy"'.format('L_', 'R_'))  # hierarchy

    cmds.rename('R_Wing_AutoRig1', 'R_Wing_AutoRig')
    cmds.group(em=True, n='R_Wing_AutoRig_Mirror_GRP')
    cmds.parent('R_Wing_AutoRig', 'R_Wing_AutoRig_Mirror_GRP')
    cmds.setAttr('R_Wing_AutoRig_Mirror_GRP.rotateX', 180)
    cmds.setAttr('R_Wing_AutoRig_Mirror_GRP.scaleX', -1)
    cmds.setAttr('R_Wing_AutoRig_Mirror_GRP.scaleY', -1)
    cmds.setAttr('R_Wing_AutoRig_Mirror_GRP.scaleZ', -1)



def rebuildLeftWing():

    if cmds.objExists('R_Wing_AutoRig_Mirror_GRP'):
        cmds.delete('R_Wing_AutoRig_Mirror_GRP')

    # Create base
    # Get Base Clav and wings
    cmds.duplicate('L_Clav_JR', 'L_Scapulars_JR', 'L_Secondaries_JR', 'L_Primaries_JR', 'L_End_JR', po=True)
    cmds.parent('L_Clav_JR1', w=True)

    def getPosOriginal(part, father):
        # Get Swing joints
        i = 0
        while cmds.objExists('L_' + str(part) + '_JR_Wing_00' + str(i)):

            # StartJoint
            OriginalJJ = cmds.duplicate('L_' + str(part) + '_JR_Wing_00' + str(i),
                                        n='L_' + str(part) + '_JR_Wing_00' + str(i) + '_temp', po=True)
            if i == 0:
                cmds.parent('L_' + str(part) + '_JR_Wing_00' + str(i) + '_temp', father)
            else:
                cmds.parent('L_' + str(part) + '_JR_Wing_00' + str(i) + '_temp',
                            'L_' + str(part) + '_JR_Wing_00' + str(i - 1) + '_temp')

            # Start Feather joint
            StartJJ = cmds.duplicate('L_' + str(part) + '_JR_Fthr_00' + str(i),
                                     n='L_' + str(part) + '_JR_Fthr_00' + str(i) + '_posStart', po=True)
            cmds.parent(StartJJ, OriginalJJ)

            # End Joint
            EndJJ = cmds.duplicate('L_' + str(part) + '_JR_Fthr_00' + str(i) + 'Bend03',
                                   n='L_' + str(part) + '_JR_Fthr_00' + str(i) + '_posEnd', po=True)
            cmds.parent(EndJJ, StartJJ)

            i = i + 1

    getPosOriginal(part='Scapulars', father='L_Clav_JR1|L_Scapulars_JR')
    getPosOriginal(part='Secondaries', father='L_Clav_JR1|L_Scapulars_JR|L_Secondaries_JR')
    getPosOriginal(part='Primaries', father='L_Clav_JR1|L_Scapulars_JR|L_Secondaries_JR|L_Primaries_JR')

    cmds.delete('L_Wing_AutoRig')
    cmds.rename('L_Clav_JR1', 'L_Clav_JR')
    cmds.select('L_Clav_JR')
    mel.eval('searchReplaceNames {} {} "hierarchy"'.format('_temp', ''))  # hierarchy
    cmds.parent('L_Scapulars_JR_Wing_000', w=True)
    cmds.parent('L_Secondaries_JR_Wing_000', w=True)
    cmds.parent('L_Primaries_JR_Wing_000', w=True)



def getPivot(side, part):
    x = 0
    while cmds.objExists(str(side) + '_' + str(part) + '_JR_' + str(x) + '_CC'):
        CC = str(side) + '_' + str(part) + '_JR_' + str(x) + '_CC'
        JJ = str(side) + '_' + str(part) + '_JR_Fthr_00' + str(x)
        cmds.matchTransform(CC, JJ, piv=True)
        x = x + 1

        print('pivots changed')


'''

CreateJoints()    
buildWingsRef()
buildWingsSystem()

mirrorWing()

rebuildLeftWing()

'''





