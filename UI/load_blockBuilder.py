'''
version: 1.0.0
date: 21/04/2020

#----------------
content: 

This will create a UI for the autorriger tool. Is dinamically created based on the .json files inside the folders

#----------------
how to: 
	
import Mosaic_Tools
from Mosaic_Tools.UI import load_blockBuilder
import imp
imp.reload(load_blockBuilder)

try:BlockBuilder.close()
except:pass
BlockBuilder = load_blockBuilder.BlockBuilder()
BlockBuilder.show()

#----------------
dependencies:   

QT FILE
ICONS
JSON FILES
Main Mosaic

#----------------
licence: https://www.eulatemplate.com/live.php?token=ySe25XC0bKARQymXaGQGR8i4gvXMJgVS
author:  Esteban Rodriguez <info@renderdemartes.com>

'''
#-------------------------------------------------------------------
from shiboken2 import wrapInstance
from PySide2 import QtGui,QtCore
from PySide2 import QtUiTools
from PySide2 import QtWidgets
from PySide2.QtWidgets import *

import maya.OpenMayaUI as omui
from functools import partial
#import pymel.core as pm
import maya.cmds as cmds
import maya.mel as mel

import os
import imp
import sys
import json

#-------------------------------------------------------------------

#Read name conventions as nc[''] and setup as seup['']
PATH = os.path.dirname(__file__)
PATH = PATH.replace('\\UI', '//Config') #change this path depending of the folder

JSON_FILE = (PATH + '/name_conventions.json')
with open(JSON_FILE) as json_file:
	nc = json.load(json_file)
#Read curve shapes info
CURVE_FILE = (PATH + '/curves.json')
with open(CURVE_FILE) as curve_file:
	curve_data = json.load(curve_file)
#setup File
SETUP_FILE = (PATH+'/rig_setup.json')
with open(SETUP_FILE) as setup_file:
	setup = json.load(setup_file)	


#-------------------------------------------------------------------

#QT WIndow!
PATH = os.path.dirname(__file__)

Title = 'Mosaic // Block Builder'
Folder = PATH.replace('\\UI', '') 
UI_File = 'blockBuilder.ui'
IconsPath =  Folder + '/Icons/'
#-------------------------------------------------------------------

import Mosaic_Tools
import Mosaic_Tools.Utils
from Mosaic_Tools.Utils import main_mosaic
imp.reload(Mosaic_Tools.Utils.main_mosaic)

mt = main_mosaic.Mosaic()


#-------------------------------------------------------------------


def maya_main_window(dockable=True):
    
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)


class BlockBuilder(QtWidgets.QDialog):
    
    def __init__(self, parent=maya_main_window()):
        super(BlockBuilder, self).__init__(parent)

        self.setWindowTitle(Title)
        self.setFixedSize(453,545)

        self.init_ui()
        self.create_layout()
        self.create_connections()


    def init_ui(self):
        
        UIPath  = Folder + '/UI/'
        f = QtCore.QFile(UIPath + UI_File)
        f.open(QtCore.QFile.ReadOnly)

        loader = QtUiTools.QUiLoader()
        self.ui = loader.load(f, parentWidget=self)

        f.close()
    #-------------------------------------------------------------------

    def create_layout(self):

        self.ui.layout().setContentsMargins(3, 3, 3, 3)          

    def create_connections(self):
        ''
        #self.ui.buttonName.clicked.connect(self.create_layout)

    #-------------------------------------------------------------------


    #-------------------------------------------------------------------

    # CLOSE EVENTS _________________________________
    def closeEvent(self, event):
        ''

#-------------------------------------------------------------------

if __name__ == "__main__":

    try:
        BlockBuilder_ui.close() # pylint: disable=E0601
        BlockBuilder_ui.deleteLater()
    except:
        pass
    BlockBuilder_ui = BlockBuilder()
    BlockBuilder_ui.show()

#-------------------------------------------------------------------


'''
#create script Job for laoding the UI
def mosaic_script_job():
    try:
        sel = cmds.ls(sl=True)[-1]
        if str(sel).endswith('_Block'):
            self.create_layout()
    except:pass
mosaic_sj = cmds.scriptJob(event=["SelectionChanged", mosaic_script_job])
       

#cmds.scriptJob(kill=mosaic_sj)
#cmds.scriptJob(ka=1)


'''