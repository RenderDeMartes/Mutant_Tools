import pyside2uic

myUI = 'C://Users//rodri//OneDrive//Documents//maya//2022//scripts//Mutant_Tools//UI//blockBuilder.ui'
myPY = 'C://Users//rodri//OneDrive//Documents//maya//2022//scripts//Mutant_Tools//UI//TEST.py'

with open(myPY, 'w') as thePython:
    pyside2uic.compileUi(myUI, thePython,False, 4, False)


'''

import os
from maya import cmds
import maya.OpenMayaUI as omui
from shiboken2 import wrapInstance




def getMayaWindow():
    ptr = omui.MQtUtil.mainWindow()
    if ptr:
        return wrapInstance(long(ptr), QtWidgets.QmainWindow)
        
def run():
    global win
    win = Ui_Form(parent = getMayaWindow())
    win.show



'''