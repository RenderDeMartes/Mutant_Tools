from __future__ import absolute_import
from maya import cmds
try:
    import importlib;from importlib import reload
except:
    import imp;from imp import reload


def hideSelection (hideT= True, hideR = True, hideS = True, hideV = True, *args):
    
    selection = cmds.ls(sl=True)
    cmds.undoInfo(openChunk=True)

    if (hideT):
        for T in selection:
            cmds.setAttr(str(T)+'.translateX',lock = True, keyable = False, channelBox = False)
            cmds.setAttr(str(T)+'.translateY',lock = True, keyable = False, channelBox = False)
            cmds.setAttr(str(T)+'.translateZ',lock = True, keyable = False, channelBox = False)

    if (hideR):
        for R in selection:
            cmds.setAttr(str(R)+'.rotateX',lock = True, keyable = False, channelBox = False)
            cmds.setAttr(str(R)+'.rotateY',lock = True, keyable = False, channelBox = False)
            cmds.setAttr(str(R)+'.rotateZ',lock = True, keyable = False, channelBox = False)

    if (hideS):
        for S in selection:
            cmds.setAttr(str(S)+'.scaleX',lock = True, keyable = False, channelBox = False)
            cmds.setAttr(str(S)+'.scaleY',lock = True, keyable = False, channelBox = False)
            cmds.setAttr(str(S)+'.scaleZ',lock = True, keyable = False, channelBox = False)
        
    if (hideV):
        for V in selection:
            cmds.setAttr(str(V)+'.visibility',lock = True, keyable = False, channelBox = False)

    cmds.undoInfo(closeChunk=True)
    


def showAll(*args):
    
    
    sel=cmds.ls(sl=1)

    cmds.undoInfo(openChunk=True)
    
    for eachObj in sel:
    	ud=cmds.listAttr(eachObj, ud=1)
    	cmds.setAttr((str(eachObj) + ".tx"), 
    		k=True)
    	cmds.setAttr((str(eachObj) + ".ty"), 
    		k=True)
    	cmds.setAttr((str(eachObj) + ".tz"), 
    		k=True)
    	cmds.setAttr((str(eachObj) + ".rx"), 
    		k=True)
    	cmds.setAttr((str(eachObj) + ".ry"), 
    		k=True)
    	cmds.setAttr((str(eachObj) + ".rz"), 
    		k=True)
    	cmds.setAttr((str(eachObj) + ".sx"), 
    		k=True)
    	cmds.setAttr((str(eachObj) + ".sy"), 
    		k=True)
    	cmds.setAttr((str(eachObj) + ".sz"), 
    		k=True)
    	cmds.setAttr((str(eachObj) + ".v"), 
    		k=True)
    	cmds.setAttr((str(eachObj) + ".tx"), 
    		l=False)
    	cmds.setAttr((str(eachObj) + ".ty"), 
    		l=False)
    	cmds.setAttr((str(eachObj) + ".tz"), 
    		l=False)
    	cmds.setAttr((str(eachObj) + ".rx"), 
    		l=False)
    	cmds.setAttr((str(eachObj) + ".ry"), 
    		l=False)
    	cmds.setAttr((str(eachObj) + ".rz"), 
    		l=False)
    	cmds.setAttr((str(eachObj) + ".sx"), 
    		l=False)
    	cmds.setAttr((str(eachObj) + ".sy"), 
    		l=False)
    	cmds.setAttr((str(eachObj) + ".sz"), 
    		l=False)
    	cmds.setAttr((str(eachObj) + ".v"), 
    		l=False)
    	for each in ud:
    		cmds.setAttr((str(eachObj) + "." + str(each)), 
    			k=True)
    		cmds.setAttr((str(eachObj) + "." + str(each)), 
    			l=False)
    cmds.undoInfo(closeChunk=True)
    		