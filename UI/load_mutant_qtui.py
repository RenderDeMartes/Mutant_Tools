'''
version: 1.0.0
date: 21/04/2020

#----------------
content: 

This will create a UI for the autorriger tool. Is dinamically created based on the .json files inside the folders

#----------------
how to: 
	
import Mutant_Tools
from Mutant_Tools.UI import load_name
imp.reload(load_name)

try:name.close()
except:pass
name = load_name.name()
name.show()

#----------------
dependencies:   

QT FILE
ICONS
JSON FILES
Main Mutant

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
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin

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

Title = 'UI NAME'
Folder = PATH.replace('\\UI', '') #where the qt designer file is
UI_File = 'name.ui'
IconsPath =  Folder + '/Icons/' #icons path
#-------------------------------------------------------------------

import Mutant_Tools
import Mutant_Tools.Utils.Rigging
from Mutant_Tools.Utils.Rigging import main_mutant
imp.reload(Mutant_Tools.Utils.Rigging.main_mutant)

mt = main_mutant.Mutant()


#-------------------------------------------------------------------


def maya_main_window(dockable=True):
    
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)


class name(MayaQWidgetDockableMixin, QtWidgets.QMainWindow):
    
    def __init__(self, parent=maya_main_window()):
        super(name, self).__init__(parent)

        self.setWindowTitle(Title)
        #self.setFixedSize(680,475)

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
        self.ui.button.setIcon(QtGui.QIcon(IconsPath + 'icon.ong'))
        
    def create_connections(self):
        ''
        #self.ui.buttonName.clicked.connect(self.create_layout)

    #-------------------------------------------------------------------

    # CLOSE EVENTS _________________________________
    def closeEvent(self, event):
        ''

#-------------------------------------------------------------------

if __name__ == "__main__":

    try:
        name_ui.close() # pylint: disable=E0601
        name_ui.deleteLater()
    except:
        pass
    name_ui = name()
    name_ui.show()

#-------------------------------------------------------------------

