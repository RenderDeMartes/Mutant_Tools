from __future__ import absolute_import
'''
content: easy bind of the feathes by selecting them in order
version: 1.0.0

date: 21/04/2020

how to: 
bindWings(side = '', feather = 'Part')

dependencies:   
cmds
            
licence: EULA 
         https://www.eulatemplate.com/live.php?token=uvtn9mOrCrX6m7CkXYA1EPZOFrBTEj67

author:  Esteban Rodriguez <info@renderdemartes.com>

'''

from maya import cmds
def bindWings(side, feather, bone = True):
    
    cmds.undoInfo(openChunk=True)   
    x = 0
    for i in cmds.ls(sl = True):
        cmds.select(cl = True)
        cmds.select(i,str(side)+str(feather)+'_JR_Fthr_00'+str(x),
                     str(side)+str(feather)+'_JR_Fthr_00'+str(x)+'Bend01',
                     str(side)+str(feather)+'_JR_Fthr_00'+str(x)+'Bend02', add = True)
        if bone:
            cmds.select(str(side)+str(feather)+'_JR_Wing_00'+str(x), add)             
            
        cmds.skinCluster(tsb = True, mi = 4)
        cmds.select(cl = True)
        x = x+1

    cmds.undoInfo(closeChunk=True)     
          
#bindWings(side = 'L_', feather = 'Scapulars')
#bindWings(side = 'R_', feather = 'Scapulars')

#bindWings(side = 'L_', feather = 'Secondaries')
#bindWings(side = 'R_', feather = 'Secondaries')

#bindWings(side = 'L_', feather = 'Primaries')
#bindWings(side = 'R_', feather = 'Primaries')