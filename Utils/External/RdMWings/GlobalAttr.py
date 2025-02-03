from __future__ import absolute_import
from maya import cmds

def globalControl(method, CC, GlobalCC, AttrName, AttrPosition ):


    '''
    method = 'Left'
    
    selection = cmds.ls(sl = True)
    CC = selection[0]
    print 'this is the controller' + str(CC)
    
    GlobalCC = selection[-1]
    print 'this is the global' + str(GlobalCC)
    
    AttrName = 'Global'
    AttrPosition = CC
    
    '''    
    
  
    # Create Root Auto GRP
    if cmds.objExists(str(CC)+'_Auto'+str(AttrName)):
        
        cmds.error('Change Name of auto group first')
    else:
        AutoGRP = cmds.group(n = str(CC)+'_Auto'+str(AttrName), empty = True)


    
    cmds.delete(cmds.parentConstraint(CC,AutoGRP, mo = False))
    cmds.delete(cmds.scaleConstraint(CC,AutoGRP, mo = False))


    
    upHy = cmds.listRelatives(CC, p = 1)
    cmds.parent(AutoGRP,upHy)
    
    cmds.setAttr(str(AutoGRP) + '.rx', 0)   
    cmds.setAttr(str(AutoGRP) + '.ry', 0)   
    cmds.setAttr(str(AutoGRP) + '.rz', 0)   
    cmds.setAttr(str(AutoGRP) + '.tx', 0)   
    cmds.setAttr(str(AutoGRP) + '.ty', 0)   
    cmds.setAttr(str(AutoGRP) + '.tz', 0)   
    
    cmds.parent(CC, AutoGRP)
 
   

    #CreateLocator and do constriant
    
    loc = cmds.spaceLocator(n = str(CC) + '_loc' + str(AttrName) )
    if method == 'Right':
        locGRP = cmds.group(loc, n = str(CC) + '_loc' + str(AttrName) + '_GRP')
    
    cmds.delete(cmds.orientConstraint(GlobalCC,loc, mo = False))
    cmds.delete(cmds.pointConstraint(CC,loc, mo = False))
    
    try:
        cmds.parent(locGRP, cmds.listRelatives(AutoGRP, p = True))
    except:
        cmds.parent(loc, cmds.listRelatives(AutoGRP, p = True))
        
    
    #OC = cmds.orientConstraint(loc, GlobalCC, AutoGRP, mo = True)
    
    # #Create Switch
    #
    #     #New Attr
    # Attr = cmds.addAttr(AttrPosition, ln =AttrName , max=1, dv=0, at='double', min=0)
    # cmds.setAttr(AttrPosition +'.' + AttrName , e=1, keyable=True)
    #
    #     #ConnectAttr
    #
    # cmds.connectAttr(AttrPosition +'.' + AttrName, str(OC[0])+ '.'+str(loc[0])+'W0', f=1)
    #
    # RN = cmds.shadingNode('reverse', asUtility=1, n = str(AttrName)+'_Reverse')
    #
    # cmds.connectAttr(AttrPosition +'.' + AttrName, str(RN)+'.inputX', f=1)
    # cmds.connectAttr(str(RN)+'.outputX', str(OC[0])+'.'+str(GlobalCC)+'W1', f=1)


    
'''   
 
globalControl(method = 'Left' , CC = 'L_Clavicule_CC', GlobalCC = 'Michael_MasterControl', AttrName = 'Global' , AttrPosition = 'L_Palm_CC')    


'''


def deleteGlobal(method , CC, GlobalCC, AttrName, AttrPosition ):

    cmds.undoInfo(openChunk=True)
    
    '''
    
    selection = cmds.ls(sl = True)
    CC = selection[0]
    print 'this is the controller' + str(CC)
    
    GlobalCC = selection[-1]
    print 'this is the global' + str(GlobalCC)
    
    AttrName = 'Global'
    AttrPosition = CC
    
    '''

    try:
        cmds.delete(str(CC) + '_loc' + str(AttrName) + '_GRP')
    except:
        cmds.delete(str(CC) + '_loc' + str(AttrName))
        
    cmds.deleteAttr(AttrPosition +'.' + AttrName)
    cmds.parent(CC, cmds.listRelatives(CC + '_Auto' +str(AttrName), p = True))
    cmds.delete(CC + '_Auto'+str(AttrName))
        
    cmds.undoInfo(closeChunk=True)
   
'''

deleteGlobal(method = 'Left' , CC = 'L_Clavicule_CC', GlobalCC = 'Michael_MasterControl', AttrName = 'Global' , AttrPosition = 'L_Palm_CC')    

'''