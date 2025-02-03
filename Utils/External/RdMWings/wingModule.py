from __future__ import absolute_import, division
from maya import cmds

try:
    import importlib;from importlib import reload
except:
    import imp;from imp import reload
import os
from pathlib import Path

import Mutant_Tools
import Mutant_Tools.Utils.Rigging
from Mutant_Tools.Utils.Rigging import main_mutant
reload(Mutant_Tools.Utils.Rigging.main_mutant)

mt = main_mutant.Mutant()
nc, curve_data, setup = mt.import_configs()

#***********************************************************************
#***********************************************************************

def rootAuto():
    
    #Conseguir la seleccion para ejecutarle un loop
    Selection = cmds.ls(sl=1)
    
    for i in Selection:

        Padre = cmds.listRelatives(i, p =1)

        Root = cmds.group(em=1, n = str(i) + '_Auto')
        Contraint01 = cmds.parentConstraint(i, Root, mo =0)
        cmds.delete(Contraint01)
        
        cmds.parent(i,Root)
        if Padre:  
            cmds.parent(Root, Padre)    
     
        Auto = cmds.group(em=1, n = str(i) + '_Root')
        Contraint01 = cmds.parentConstraint(Root, Auto, mo =0)
        cmds.delete(Contraint01)
        
        cmds.parent(Root, Auto)
        if Padre:
            cmds.parent(Auto, Padre) 
            
    
#***********************************************************************
#***********************************************************************

def wingModuleFunc(name1 = 'Null',
    name2 = 'Null',
    amount = 10,
    Axis = 'Z',
    distanceBack = 0.5
    ):
    
    cmds.undoInfo(openChunk=True)   
    
    
    #inputs
    if name1 == 'Null':
        
        jointsSel = cmds.ls(sl = True)
        cmds.select(cl=True)
        
    else:
        cmds.select(name1, name2)
        jointsSel = cmds.ls(sl = True)
        cmds.select(cl=True)
    
    
    distance =cmds.getAttr(str(jointsSel[1])+'.translateX')
        
    
    
    #BigRadius for parents
    for i in jointsSel:
        cmds.setAttr(str(i)+'.radius',2)
        
    #NewJoints parent to world
    basejoints = []
    
    for i in range(0,amount):
        
        try:
            cmds.select(str(jointsSel[0])+'_Wing_00'+str(i-1))
            
        except:
            cmds.select(str(jointsSel[0]))
            
        newJoint = cmds.joint(n = str(jointsSel[0])+'_Wing_00'+str(i))
        basejoints.append(newJoint)
        
        cmds.setAttr(newJoint + '.translateX', distance/amount)
        
    cmds.parent (basejoints[0],w = True)
    
    
    #Feather joints pos
    
    for j in range(0,amount):
        
        cmds.select(basejoints[j])
          
        newJoint2 = cmds.joint(n = str(jointsSel[0])+'_Fthr_00'+str(j)+'_posStart')
        cmds.setAttr(newJoint2 + '.translate' +str(Axis), -distanceBack)
        newJoint3 = cmds.joint(n = str(jointsSel[0])+'_Fthr_00'+str(j)+'_posEnd')
        cmds.setAttr(newJoint3 + '.translate' +str(Axis), -distanceBack*3)
       
       
    cmds.select(jointsSel) 

    cmds.undoInfo(closeChunk=True)   

#***********************************************************************
#***********************************************************************

def createWings(name1 = 'Null',
    name2 = 'Null',
    amount = 10,
    Axis = 'Z',
    distanceBack = 0.5,
    size = 2,  #CurveRadius
    colorCC = 13):

    cmds.undoInfo(openChunk=True)   
    
    #inputs
    if name1 == 'Null':
        
        jointsSel = cmds.ls(sl = True)
        cmds.select(cl=True)
        
    else:
        cmds.select(name1, name2)
        jointsSel = cmds.ls(sl = True)
        cmds.select(cl=True)
    
    
    #create a fake baseJoints
    basejoints = []
    for i in range(0,amount):
        basejoints.append(str(jointsSel[0])+'_Wing_00'+str(i))

    #Create the joints for each feather in correct hy
    
    bindFeathers = []
    for j in range(0,amount ):
        

        cmds.select(basejoints[j])
        bindFeathers.append(basejoints[j])
          
        newJoint2 = cmds.joint(n = str(jointsSel[0])+'_Fthr_00'+str(j))
       
        NewGrp1 = cmds.group(n = str(jointsSel[0])+'_Fthr_00'+str(j)+'_AutoJnt')
        RootGrp = cmds.group(n = str(jointsSel[0])+'_Fthr_00'+str(j)+'_RootJnt')
        SpreadGrp = cmds.group(n = str(jointsSel[0])+'_Fthr_00'+str(j)+'_SpreadCtrlGrp')
        SpreadAutoGrp = cmds.group(n = str(jointsSel[0])+'_Fthr_00'+str(j)+'_SpreadAuto')
            
        #cmds.setAttr(RootGrp + '.translate' +str(Axis), -distanceBack)
        cmds.delete(cmds.parentConstraint(str(jointsSel[0])+'_Fthr_00'+str(j)+'_posStart', SpreadAutoGrp, mo = False))
        cmds.setAttr(newJoint2 + '.radius', 0.5)
        
        
        distanceBack = - cmds.getAttr(str(jointsSel[0])+'_Fthr_00'+str(j) + '_posEnd.translate' + str(Axis)) / 3
        #Feathers for Bend joints
        cmds.select(newJoint2)
        newJoint3 = cmds.joint(n = str(jointsSel[0])+'_Fthr_00'+str(j)+'Bend01')
        NewGrp2 = cmds.group(n = str(jointsSel[0])+'_Fthr_00'+str(j)+'_BendJnt1')        
        cmds.setAttr(NewGrp2 + '.translate' +str(Axis), -distanceBack)
        cmds.setAttr(newJoint3 + '.radius', 0.5)
        
        cmds.select(newJoint3)
        newJoint4 = cmds.joint(n = str(jointsSel[0])+'_Fthr_00'+str(j)+'Bend02')
        NewGrp3 = cmds.group(n = str(jointsSel[0])+'_Fthr_00'+str(j)+'_BendJnt2')        
        cmds.setAttr(NewGrp3 + '.translate' +str(Axis), -distanceBack)
        cmds.setAttr(newJoint4 + '.radius', 0.5)
                
        cmds.select(newJoint4)
        newJoint5 = cmds.joint(n = str(jointsSel[0])+'_Fthr_00'+str(j)+'Bend03')
        NewGrp4 = cmds.group(n = str(jointsSel[0])+'_Fthr_00'+str(j)+'_BendJnt3')        
        cmds.setAttr(NewGrp4 + '.translate' +str(Axis), -distanceBack)
        cmds.setAttr(newJoint5 + '.radius', 0.5) 
    
        #Delete ref joint
        cmds.delete(str(jointsSel[0])+'_Fthr_00'+str(j)+'_posStart')
    
        #Bind Set
        bindFeathers.append(newJoint2)
        bindFeathers.append(newJoint3)
        bindFeathers.append(newJoint4)
        bindFeathers.append(newJoint5)
                 
    #Create Controllers and auto_groups for each
    wingsControllers = []
    for cc in range(0,amount):
        controller_curve = mt.curve(input='', custom_name=True, name=str(jointsSel[0])+'_Fthr_00'+str(cc)+nc['ctrl'], size=size, type='circle_point',  tag=False, playback=False)
        root_group, auto_group = mt.root_grp(autoRoot=True)

        #Shape the cv ad color ir
        mt.rotate_shape(controller_curve, -90,90,0)
        cmds.setAttr(str(controller_curve) + 'Shape.overrideEnabled', 1)
        cmds.setAttr(str(controller_curve) + 'Shape.overrideColor', colorCC)
       
        #Parent to bone
        cmds.delete(cmds.parentConstraint(basejoints[cc],root_group,  mo=False))
        cmds.parentConstraint(controller_curve, basejoints[cc])
        
        try:
            cmds.parent(root_group, wingsControllers[-1])
        except:
            pass
        wingsControllers.append(controller_curve)

    print(wingsControllers)
    
    
#***********************************************************************

    #Cube Master Controller
    cmds.select(cl=True)
    Cube = mt.curve(input='', type='cube', custom_name=True, name=str(basejoints[0]) + nc['ctrl'], size=size,  tag=False, playback=False)
    mt.match(Cube, jointsSel[0])
    RootCube, AutoCube = mt.root_grp(autoRoot=True)
    cmds.setAttr(Cube + '.overrideEnabled', 1)
    cmds.setAttr(Cube + '.overrideColor', colorCC)    


    cmds.parentConstraint(Cube,jointsSel[0], mo=True)
    cmds.parent(jointsSel[0]+'_Fthr_000_Ctrl_Root_Grp',Cube)
    cmds.parent(jointsSel[0]+'_Wing_000',Cube)        
    

    #CleanMasterController and Create Attrs
    cmds.setAttr(Cube+".sx", lock=True, channelBox=False, keyable=False)
    cmds.setAttr(Cube+".sy", lock=True, channelBox=False, keyable=False)
    cmds.setAttr(Cube+".sz", lock=True, channelBox=False, keyable=False)
    cmds.setAttr(Cube+".v", lock=True, channelBox=False, keyable=False)
    
    cmds.addAttr(Cube, ln="_", en=".:", at="enum")
    cmds.setAttr(Cube+'._', e=1, keyable=True)
    cmds.addAttr(Cube, ln="Secundary", en="Hide:Show:", at = "enum" , dv = 1)
    cmds.setAttr(Cube+'.Secundary', e=1, keyable=True)

    #ConnectAttrs
    cmds.connectAttr(Cube + '.Secundary', jointsSel[0] + '_Fthr_000_Ctrl_Root_Grp.visibility', f=1)
    

  
    #***********************************************************************

    #Create Wing Bend
    cmds.select(cl=True)
    BendCC = mt.curve(input='', type='sphere', custom_name=True, name=str(jointsSel[0]) + '_Bend_CC', size=size,  tag=False, playback=False)
    mt.hide_attr(t=True,s=True)
    AutoBend = cmds.group(BendCC, n = str(BendCC)+'_Auto'+nc['group'])
    RootBend = cmds.group(AutoBend,n = str(BendCC)+'_Root'+nc['group'])
    
    cmds.setAttr(BendCC + '.overrideEnabled', 1)
    cmds.setAttr(BendCC + '.overrideColor', colorCC)
    
    cmds.delete(cmds.parentConstraint(jointsSel[0],jointsSel[-1], RootBend, mo = False))    
    #cmds.setAttr(RootBend + '.tz', -size*5)

    #midValue = int(math.floor(amount/2))
    
    cmds.parent(RootBend, jointsSel[0])
    

    #Parent Sphere to joints
    #cmds.parent(RootBend, str(jointsSel[0])+'_Fthr_00'+str(midValue)+'_BendJnt2')

    for b in range(0,amount):
        #rotate X
        cmds.connectAttr(str(BendCC)+".rx", str(jointsSel[0])+'_Fthr_00'+str(b)+'_AutoJnt.rotateX')
        cmds.connectAttr(str(BendCC)+".ry", str(jointsSel[0])+'_Fthr_00'+str(b)+'_AutoJnt.rotateY')

        for i in range(1,4):
            cmds.connectAttr(str(BendCC)+".rx", str(jointsSel[0])+'_Fthr_00'+str(b)+'_BendJnt'+str(i)+'.rotateX')
            cmds.connectAttr(str(BendCC)+".ry", str(jointsSel[0])+'_Fthr_00'+str(b)+'_BendJnt'+str(i)+'.rotateY')


#***********************************************************************

    #Create Twist
    for b in range(0,amount):
        #rotate Z
        cmds.connectAttr(str(BendCC)+".rz", str(jointsSel[0])+'_Fthr_00'+str(b)+'_SpreadCtrlGrp.rotateZ')
        for i in range(1,4):
            cmds.connectAttr(str(BendCC)+".rz", str(jointsSel[0])+'_Fthr_00'+str(b)+'_BendJnt'+str(i)+'.rotateZ')



    
#***********************************************************************
    
    #Create Spread Controllers
    
    def spreadControllers(mode, cornerJoint, index):
       
       
        #Create Spread Controllers
        cmds.select(cl=True)
        spreadCube = mt.curve(input='', custom_name=True, name=cornerJoint+'_Spread_'+mode+nc['ctrl'], size=size, type='cube',  tag=False, playback=False)
        Auto = cmds.group(n = cornerJoint+'_Spread_'+mode+'_Auto'+nc['group'])
        Root = cmds.group(n = cornerJoint+'_Spread_'+mode+'_Root'+nc['group'])
               
        cmds.delete(cmds.parentConstraint(cornerJoint+'_Fthr_00' + str(index),Root, mo = False))
        
        cmds.move(0, 0, 0.5, Root+'.scalePivot', Root+'.rotatePivot', r=1)        
        cmds.move(0, 0, 0.5, Auto+'.scalePivot', Auto+'.rotatePivot', r=1)        
        cmds.move(0, 0, 0.5, spreadCube+'.scalePivot', spreadCube+'.rotatePivot', r=1)        

        mt.scale_shape(x=1, y=1, z=size*4)

        cmds.makeIdentity(Root, s = True, t = False, r = False, a = True)
        cmds.parent(Root, Cube)

        mt.hide_attr(t=True, s=True)


        return Root, Auto, spreadCube


    #Create System
    InRoot, InAuto, InCube = spreadControllers(mode='In', cornerJoint = jointsSel[0], index = 0)
    OutRoot, OutAuto, OutCube = spreadControllers(mode='Out', cornerJoint = jointsSel[0], index = amount -1)

    #Connect Spread to Joints
    #Save root position
  
    for i in range(0,amount):
        cmds.select(jointsSel[0]+'_Fthr_00'+str(i)+'_SpreadAuto')
        rootAuto()

    def connectAttrMult(input, output, value, nodeName):

        MultNode = cmds.shadingNode('multiplyDivide', asUtility=1, n = nodeName)
        cmds.connectAttr(input, str(MultNode)+'.input1.input1X')
        cmds.setAttr(str(MultNode)+'.input2.input2X', value)
        cmds.connectAttr(str(MultNode)+'.output.outputX', output)
        cmds.setAttr(MultNode+'.operation', 1)
    
    if amount > 9:
        lotsVariable = 0.1
        
    elif 5 < amount < 10:
        lotsVariable = 0.2
                
    elif amount == 5:
        lotsVariable = 0.3
        
    elif amount < 5: 
        lotsVariable = 0.5 
    
    #NormalSpread OUT Side
    x = 0

    while cmds.objExists(jointsSel[0]+'_Fthr_00'+str(x)+'_SpreadCtrlGrp'):
        connectAttrMult(input=jointsSel[0]+'_Spread_Out_Ctrl'+".ry", output = str(jointsSel[0])+'_Fthr_00'+str(x)+'_SpreadCtrlGrp.rotateY', value = (x + 1)* lotsVariable  , nodeName = str(jointsSel[0])+'_Fthr_00NodeSpread' + str(x))
        connectAttrMult(input=jointsSel[0]+'_Spread_Out_Ctrl'+".rx", output = str(jointsSel[0])+'_Fthr_00'+str(x)+'_RootJnt.rotateX', value = (x + 1)* lotsVariable  , nodeName = str(jointsSel[0])+'_Fthr_00NodeSpread' + str(x))
        connectAttrMult(input=jointsSel[0]+'_Spread_Out_Auto_Grp'+".ry", output = str(jointsSel[0])+'_Fthr_00'+str(x)+'_SpreadAuto_Auto.rotateY', value = (x + 1)* lotsVariable  , nodeName = str(jointsSel[0])+'_Fthr_00NodeSpread' + str(x))
        connectAttrMult(input=jointsSel[0]+'_Spread_Out_Auto_Grp'+".rx", output = str(jointsSel[0])+'_Fthr_00'+str(x)+'_SpreadAuto_Auto.rotateX', value = (x + 1)* lotsVariable  , nodeName = str(jointsSel[0])+'_Fthr_00NodeSpread' + str(x))


        x = x + 1
        
    #NormalSpread IN Side
    x = amount - 1
    y = 0
    while cmds.objExists(jointsSel[0]+'_Fthr_00'+str(x)+'_SpreadCtrlGrp'):
        connectAttrMult(input=jointsSel[0]+'_Spread_In_Ctrl'+".ry", output = str(jointsSel[0])+'_Fthr_00'+str(x)+'_RootJnt.rotateY', value = (y + 1) * lotsVariable  , nodeName = str(jointsSel[0])+'_Fthr_00NodeSpread' + str(x))
        connectAttrMult(input=jointsSel[0]+'_Spread_In_Ctrl'+".rx", output = str(jointsSel[0])+'_Fthr_00'+str(x)+'_SpreadAuto.rotateX', value = (y + 1) * lotsVariable  , nodeName = str(jointsSel[0])+'_Fthr_00NodeSpread' + str(x))
        connectAttrMult(input=jointsSel[0]+'_Spread_In_Auto_Grp'+".ry", output = str(jointsSel[0])+'_Fthr_00'+str(x)+'_SpreadAuto.rotateY', value = (y + 1) * lotsVariable  , nodeName = str(jointsSel[0])+'_Fthr_00NodeSpread' + str(x))
        connectAttrMult(input=jointsSel[0]+'_Spread_In_Auto_Grp'+".rx", output = str(jointsSel[0])+'_Fthr_00'+str(x)+'_SpreadCtrlGrp.rotateX', value = (y + 1) * lotsVariable  , nodeName = str(jointsSel[0])+'_Fthr_00NodeSpread' + str(x))

        x = x - 1
        y = y + 1 

    #***********************************************************************
    #Controllers for each Feather

    #New Attr for hide
    cmds.addAttr(Cube, ln="Feathers", en="Hide:Show:", at = "enum" , dv = 1)
    cmds.setAttr(Cube+'.Feathers', e=1, keyable=True)
            
    for f in range(0,amount):
        Feather = str(jointsSel[0])+'_Fthr_00'+str(f)+'_RootJnt'
        cmds.select(cl=True)
        Curve = mt.curve(input='', size=size, type='pin_cube', custom_name=True, name=str(jointsSel[0])+'_'+ str(f)+nc['ctrl'],  tag=False, playback=False)
        mt.match(Curve, Feather)
        CurveGrp = mt.root_grp(custom=True, custom_name=str(jointsSel[0])+ '_' + str(f)+ "_CC_AutoFold"+nc['group'])[0]
        #CurveGrp = cmds.group(Curve, n =str(jointsSel[0])+ '_' + str(f)+ "_CC_AutoFold"+nc['group'])
        #cmds.delete(cmds.parentConstraint(Feather, CurveGrp, mo=False))
        cmds.parent(CurveGrp,Feather)
        cmds.parent(str(jointsSel[0])+'_Fthr_00'+str(f)+'_AutoJnt', Curve)
        #cmds.rotate(-90,90,0, str(Curve)+'.cv[0:14] ')
        cmds.connectAttr(str(Cube)+'.Feathers', str(CurveGrp)+'.visibility', f=True )

        mt.line_attr(Curve, name='Bends')
        bend_attr_x = mt.new_attr(Curve, name='BendX', min=-999, max=999)
        bend_attr_y = mt.new_attr(Curve, name='BendY', min=-999, max=999)
        bend_attr_z = mt.new_attr(Curve, name='BendZ', min=-999, max=999)

        childs = cmds.listRelatives(Feather, ad=True, type='joint')
        for jnt in childs:
            cmds.connectAttr(bend_attr_x, jnt+'.rx')
            cmds.connectAttr(bend_attr_y, jnt+'.ry')
            cmds.connectAttr(bend_attr_z, jnt+'.rz')

    cmds.setAttr(str(Cube)+'.Feathers', 1)

#***********************************************************************
    #Create nurbs Plane
    ribbonPlane =cmds.nurbsPlane(ch=1, d=1, v=1, p=(0, 0, 0), u=1, w=1, ax=(0, 1, 0), lr=1, n = jointsSel[0]+'_FeathersPlane')
    cluster01 = cmds.cluster(ribbonPlane[0] + '.cv[0][0:1]')
    cluster02 = cmds.cluster(ribbonPlane[0] + '.cv[1][0:1]')
 
    cmds.delete(cmds.parentConstraint(jointsSel[0], cluster01, mo=False))
    cmds.delete(cmds.parentConstraint(str(jointsSel[0])+'_Wing_00'+str(amount-1), cluster02, mo=False))

    cmds.delete(ribbonPlane,ch=True)
    

    cluster03 = cmds.cluster(ribbonPlane[0] + '.cv[1][1] ')
    cluster04 = cmds.cluster(ribbonPlane[0] + '.cv[0][1] ')
    
    cmds.delete(cmds.parentConstraint(str(jointsSel[0])+'_Fthr_00'+str(amount-1)+'Bend03', cluster03, mo=False))
    cmds.delete(cmds.parentConstraint(str(jointsSel[0])+'_Fthr_000Bend03', cluster04, mo=False))
    
    
    cmds.delete(ribbonPlane[0],ch=True)
     
    cmds.rebuildSurface(ribbonPlane[0], rt=0, kc=0, fr=0, end=1, sv=6, su=(amount-1)*2, kr=0, dir=2, kcp=0, tol=0.01, dv=3, du=3, rpo=1)
    
    
#***********************************************************************
    #Create Bind Sets
    #Bind Feathers // bindFeathers //
     
    cmds.select(cl = True)
    cmds.skinCluster(bindFeathers, ribbonPlane[0], sm =0 , bm =0, tsb  = True )

     
              
    cmds.undoInfo(closeChunk=True)   


'''
wingModuleFunc(amount = 10 , Axis = 'Z',distanceBack = 2)      
      
createWings(amount = 10 , Axis = 'Z',distanceBack = 2,size = 2,colorCC = 13)
'''


