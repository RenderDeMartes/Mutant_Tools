from __future__ import absolute_import
'''
content: create basic folding system based on your pose

version: 1.0.0

date: 21/04/2020

how to: 
setInitialKeys()#creates a bad initial pose from frame 0 to 60
keysToSDK2() #based on that pose 0 to 60 creates an auto SDK to save the pose in wing fold attr


dependencies:   
mel
cmds
pymel
			
licence: EULA 
		 https://www.eulatemplate.com/live.php?token=uvtn9mOrCrX6m7CkXYA1EPZOFrBTEj67

author:  Esteban Rodriguez <info@renderdemartes.com>

'''

from maya import cmds
import maya.mel as mel
mel.eval("source channelBoxCommand;")

def setInitialKeys():
	
	cmds.undoInfo(openChunk=True)   

	cmds.playbackOptions( maxTime=60 )

	controllers = ['L_Scapulars_JR_Wing_000_CC','L_Secondaries_JR_Wing_000_CC','L_Primaries_JR_Wing_000_CC',
	 'L_Scapulars_JR_Spread_IN','L_Scapulars_JR_Spread_IN',
	 'L_Secondaries_JR_Spread_OUT','L_Secondaries_JR_Spread_IN',
	 'L_Primaries_JR_Spread_OUT','L_Primaries_JR_Spread_IN']
	 
	def setKeys(obj = '', rx=0,ry=0,rz=0,tx=0,ty=0,tz=0, kf = 1):
		
		cmds.currentTime(kf)
		cmds.setAttr(str(obj)+ '.rx', rx)
		cmds.setAttr(str(obj)+ '.ry', ry)
		cmds.setAttr(str(obj)+ '.rz', rz)
		cmds.setKeyframe(str(obj)+'.rotate')
		cmds.setAttr(str(obj)+ '.tx', tx)
		cmds.setAttr(str(obj)+ '.ty', ty)
		cmds.setAttr(str(obj)+ '.tz', tz)
		cmds.setKeyframe(str(obj)+'.translate')    
	
	#Frame 1
	setKeys(obj = 'L_Scapulars_JR_Wing_000_CC' , rx = 0,ry = 0,rz = 0,tx=0,ty=0,tz=0,  kf = 1)
	setKeys(obj = 'L_Secondaries_JR_Wing_000_CC' , rx = 0,ry = 0,rz = 0,tx=0,ty=0,tz=0,  kf = 1)
	setKeys(obj = 'L_Primaries_JR_Wing_000_CC' , rx = 0,ry = 0,rz = 0,tx=0,ty=0,tz=0,  kf = 1)

	setKeys(obj = 'L_Scapulars_JR_Spread_IN' , rx = 0,ry = 0,rz = 0,tx=0,ty=0,tz=0,  kf = 1)
	setKeys(obj = 'L_Scapulars_JR_Spread_OUT' , rx = 0,ry = 0,rz = 0,tx=0,ty=0,tz=0,  kf = 1)
	setKeys(obj = 'L_Secondaries_JR_Spread_OUT' , rx = 0,ry = 0,rz = 0,tx=0,ty=0,tz=0,  kf = 1)
	setKeys(obj = 'L_Secondaries_JR_Spread_IN' , rx = 0,ry = 0,rz = 0,tx=0,ty=0,tz=0,  kf = 1)
	setKeys(obj = 'L_Primaries_JR_Spread_OUT' , rx = 0,ry = 0,rz = 0,tx=0,ty=0,tz=0, kf = 1)
	setKeys(obj = 'L_Primaries_JR_Spread_IN' , rx = 0,ry = 0,rz = 0,tx=0,ty=0,tz=0,  kf = 1)
	
	#Frame 20 
	setKeys(obj = 'L_Scapulars_JR_Wing_000_CC' , rx = 22 ,ry = 35 ,rz = -15, tx=0, ty=0.3, tz=0,  kf = 20)
	setKeys(obj = 'L_Secondaries_JR_Wing_000_CC' , rx = -25 ,ry = -80 ,rz = 5 ,tx=0 ,ty=0.25 ,tz=0,  kf = 20)
	setKeys(obj = 'L_Primaries_JR_Wing_000_CC' , rx = 20,ry = 90 ,rz = 4, tx=0, ty=0, tz=0,  kf = 20)
	
	#Frame 40 
	setKeys(obj = 'L_Scapulars_JR_Wing_000_CC' , rx = 30 ,ry = 50 ,rz = -35,tx=0,ty=0.5,tz=0,  kf = 40)
	setKeys(obj = 'L_Secondaries_JR_Wing_000_CC' , rx = -80 ,ry = -110 ,rz = 45 ,tx=0,ty=0.3,tz=0,  kf = 40)
	setKeys(obj = 'L_Primaries_JR_Wing_000_CC' , rx = 25,ry = 125 ,rz = 5,tx=0,ty=0,tz=0,  kf = 40)

	#Frame 60 
	setKeys(obj = 'L_Scapulars_JR_Wing_000_CC' , rx = 20 ,ry = 40 ,rz = -42,tx=0,ty=0.4,tz=0,  kf = 60)
	setKeys(obj = 'L_Secondaries_JR_Wing_000_CC' , rx = -124 ,ry = -110 ,rz = 100 ,tx=0,ty=0.3,tz=0,  kf = 60)
	setKeys(obj = 'L_Primaries_JR_Wing_000_CC' , rx = 30 , ry = 125 ,rz = 5,tx=0,ty=0,tz=0,  kf = 60)
	
	setKeys(obj = 'L_Scapulars_JR_Spread_IN' , rx = 0,ry = -25,rz = 0,  kf = 60)
	setKeys(obj = 'L_Scapulars_JR_Spread_OUT' , rx = 0,ry = -2 ,rz = 0,  kf = 60)
	setKeys(obj = 'L_Secondaries_JR_Spread_OUT' , rx = 0,ry = 75,rz = 0,  kf = 60)
	setKeys(obj = 'L_Secondaries_JR_Spread_IN' , rx =0,ry = 33,rz = 0,  kf = 60)
	setKeys(obj = 'L_Primaries_JR_Spread_OUT' , rx = -0,ry = 0,rz = 0,  kf = 60)
	setKeys(obj = 'L_Primaries_JR_Spread_IN' , rx = 0,ry = -55,rz = 0,  kf = 60)

	cmds.setAttr("L_Primaries_JR_Spread_IN.rx", lock=True)
	cmds.setAttr("L_Scapulars_JR_Spread_IN.rx", lock=True)
	cmds.setAttr("L_Scapulars_JR_Spread_OUT.rx", lock=True)
	cmds.setAttr("L_Secondaries_JR_Spread_IN.rx", lock=True)
	cmds.setAttr("L_Secondaries_JR_Spread_OUT.rx", lock=True)
	cmds.setAttr("L_Primaries_JR_Spread_OUT.rx", lock=True)


	cmds.undoInfo(closeChunk=True)   


#setInitialKeys()

def keysToSDK1():
	
	cmds.autoKeyframe( state=True )
	
	
	Controllers =  ['L_Scapulars_JR_Wing_000_CC','L_Secondaries_JR_Wing_000_CC','L_Primaries_JR_Wing_000_CC',
	 'L_Scapulars_JR_Spread_OUT','L_Scapulars_JR_Spread_IN',
	 'L_Secondaries_JR_Spread_OUT','L_Secondaries_JR_Spread_IN',
	 'L_Primaries_JR_Spread_OUT','L_Primaries_JR_Spread_IN']
	Auto = ['L_Scapulars_JR_Wing_000_Auto','L_Secondaries_JR_Wing_000_Auto','L_Primaries_JR_Wing_000_Auto',
	 'L_Scapulars_JR_Spread_OUT_Auto','L_Scapulars_JR_Spread_IN_Auto',
	 'L_Secondaries_JR_Spread_OUT_Auto','L_Secondaries_JR_Spread_IN_Auto',
	 'L_Primaries_JR_Spread_OUT_Auto','L_Primaries_JR_Spread_IN_Auto']
   
	x = 0
	for i in Controllers:
		
		for frame in [1,20,30,40,60]:
			
			print('frame = ' +str(frame))
			
			cmds.currentTime(frame)

			#Set AutoValues
			print('i = ' + i + '_ and Auto[X] = '+ str(Auto[x]))
			
			value = cmds.getAttr(i + '.rotateX')
			cmds.setAttr(Auto[x]+'.rotateX', value)
			value = cmds.getAttr(i + '.rotateY')
			cmds.setAttr(Auto[x]+'.rotateY', value)
			value = cmds.getAttr(i + '.rotateZ')
			cmds.setAttr(Auto[x]+'.rotateZ', value)  
			value = cmds.getAttr(i + '.translateX')
			cmds.setAttr(Auto[x]+'.translateX', value)
			value = cmds.getAttr(i + '.translateY')
			cmds.setAttr(Auto[x]+'.translateY', value)
			value = cmds.getAttr(i + '.translateZ')
			cmds.setAttr(Auto[x]+'.translateZ', value)  

			cmds.setKeyframe(str(Auto[x])+'.rotate')
			cmds.setKeyframe(str(Auto[x])+'.translate')
			
		cmds.setAttr(i+'.rotateX', 0)
		cmds.setAttr(i+'.rotateY', 0)
		cmds.setAttr(i+'.rotateZ', 0)      
	
		cmds.mel.CBdeleteConnection(i+'.rotateX')
		cmds.mel.CBdeleteConnection(i+'.rotateY')
		cmds.mel.CBdeleteConnection(i+'.rotateZ')
		
		x = x +1  
	
#keysToSDK1()

def keysToSDK2():
	
	cmds.ogs(pause=1)
	
	cmds.mel.CBunlockAttr("L_Primaries_JR_Spread_IN.rx")
	cmds.mel.CBunlockAttr("L_Scapulars_JR_Spread_IN.rx")
	cmds.mel.CBunlockAttr("L_Scapulars_JR_Spread_OUT.rx")
	cmds.mel.CBunlockAttr("L_Secondaries_JR_Spread_IN.rx")
	cmds.mel.CBunlockAttr("L_Secondaries_JR_Spread_OUT.rx")
	cmds.mel.CBunlockAttr("L_Primaries_JR_Spread_OUT.rx")
		
		
	cmds.currentTime(0)
	cmds.select(cl = True)
	CC = []
	
	#Correct Feather pivots:
	x = 0    
	while cmds.objExists('L_Primaries_JR_'+str(x)+'_CC'):
		cmds.select('L_Primaries_JR_'+str(x)+'_CC')
		upNode = cmds.listRelatives('L_Primaries_JR_'+str(x)+'_CC', p = True)[0]
		#cmds.matchTransform(upNode,'L_Primaries_JR_'+str(x)+'_CC', piv = True, pos = 0, rot =0,scl =0)
		CC.append('L_Primaries_JR_'+str(x)+'_CC')
		x = x +1
	x = 0  
	while cmds.objExists('L_Secondaries_JR_'+str(x)+'_CC'):
		cmds.select('L_Secondaries_JR_'+str(x)+'_CC')
		upNode = cmds.listRelatives('L_Secondaries_JR_'+str(x)+'_CC', p = True)[0]
		#cmds.matchTransform(upNode,'L_Secondaries_JR_'+str(x)+'_CC', piv = True, pos = 0, rot =0,scl =0)
		CC.append('L_Secondaries_JR_'+str(x)+'_CC')
		x = x +1
	x = 0  
	while cmds.objExists('L_Scapulars_JR_'+str(x)+'_CC'):
		cmds.select('L_Scapulars_JR_'+str(x)+'_CC')
		upNode = cmds.listRelatives('L_Scapulars_JR_'+str(x)+'_CC', p = True)[0]
		#cmds.matchTransform(upNode,'L_Scapulars_JR_'+str(x)+'_CC', piv = True, pos = 0, rot =0,scl =0)
		CC.append('L_Scapulars_JR_'+str(x)+'_CC')
		x = x +1
		
	#Select controllers
	CC2 = ['L_Scapulars_JR_Wing_000_CC','L_Scapulars_JR_Spread_IN','L_Scapulars_JR_Spread_OUT',
				'L_Secondaries_JR_Wing_000_CC','L_Secondaries_JR_Spread_IN','L_Secondaries_JR_Spread_OUT',
				'L_Primaries_JR_Wing_000_CC','L_Primaries_JR_Spread_IN','L_Primaries_JR_Spread_OUT']

	#CC2 = ['L_Scapulars_JR_Wing_000_CC','L_Secondaries_JR_Wing_000_CC','L_Primaries_JR_Wing_000_CC']
			
			
	print(CC)  #feathers controllers
	print(CC2) #spreads and main wings controlelrs

	cmds.select(cl = True)  
	print(CC2+CC)
	cmds.select(CC, CC2)
	#Automate wing close


	for i in cmds.ls(sl = True):

		attrs = ['.tx','.ty','.tz','.rx','.ry','.rz']
		upNode = cmds.listRelatives(i, p = True)[0]
		feathersSec = ['L_Secondaries_JR_Fthr_008','L_Secondaries_JR_Fthr_007','L_Secondaries_JR_Fthr_006','L_Secondaries_JR_Fthr_005','L_Secondaries_JR_Fthr_004'
		,'L_Secondaries_JR_Fthr_003','L_Secondaries_JR_Fthr_002','L_Secondaries_JR_Fthr_001','L_Secondaries_JR_Fthr_000']

		feather = 0
		for j in attrs:
			
			originalZero = cmds.getAttr(str(upNode)+str(j))
			#print 'Folding :                                                       n/'
			#print str(upNode)+str(j)
			#print str(i)+str(j)
			#print str(feathersSec[feather]) + str(cmds.xform(feathersSec[feather],q = True, m = True, ws = True))
			
			cmds.currentTime(60)
			cmds.setAttr('L_Wing_CC.WingFold', 10)           
			try:cmds.setAttr(str(upNode)+str(j), cmds.getAttr(str(i)+str(j))+cmds.getAttr(str(upNode)+str(j)))
			except:pass
			try:cmds.setAttr(str(i)+str(j), 0)
			except:pass
			cmds.setDrivenKeyframe(upNode, currentDriver='L_Wing_CC.WingFold')
		

			#print str(feathersSec[feather]) + str(cmds.xform(feathersSec[feather],q = True, m = True, ws = True))


			cmds.currentTime(30)
			cmds.setAttr('L_Wing_CC.WingFold', 5)           
			try:cmds.setAttr(str(upNode)+str(j), cmds.getAttr(str(i)+str(j))+cmds.getAttr(str(upNode)+str(j)))
			except:pass
			try:cmds.setAttr(str(i)+str(j), 0)
			except:pass
			cmds.setDrivenKeyframe(upNode, currentDriver='L_Wing_CC.WingFold')

   
			cmds.currentTime(0)
			cmds.setAttr('L_Wing_CC.WingFold', 0)           
			try:cmds.setAttr(str(upNode)+str(j), originalZero)
			except:pass
			try:cmds.setAttr(str(i)+str(j), 0)
			except:pass
			cmds.setDrivenKeyframe(upNode, currentDriver='L_Wing_CC.WingFold')         


			feather = feather + 1

			#cmds.mel.channelBoxCommand('-break')
			cmds.mel.CBdeleteConnection(str(i)+str(j))

	cmds.ogs(pause=1)
	cmds.currentTime(60)
	cmds.setAttr('L_Wing_CC.WingFold', 10)           

'''

keysToSDK2()

'''