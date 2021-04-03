'''
version: 1.0.0
date: 21/04/2020

#----------------
content: 

This will create a UI for the autorriger tool. Is dinamically created based on the folders and json files

NEEDS A UPDATE :)
#----------------
how to: 
	
import Mosaic_Tools
from Mosaic_Tools.UI import load_autoRigger
reload(load_autoRigger)

AutoRigger = load_autoRigger.AutoRigger()
AutoRigger.show()

#----------------
dependencies:   

QT FILE
ICONS
MODULES FOLDER

#----------------
licence: https://www.eulatemplate.com/live.php?token=ySe25XC0bKARQymXaGQGR8i4gvXMJgVS
author:  Esteban Rodriguez <info@renderdemartes.com>

'''
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
import json
import glob

#QT WIndow!
PATH = os.path.dirname(__file__)

Title = 'Mosaic // Autor_Rigger'
Folder = PATH.replace('\UI', '') 
UI_File = 'autoRigger.ui'
IconsPath =  Folder + '/Icons/'

def maya_main_window():
    
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(long(main_window_ptr), QtWidgets.QWidget)


class AutoRigger(QtWidgets.QDialog):
    
    def __init__(self, parent=maya_main_window()):
        super(AutoRigger, self).__init__(parent)

        self.setWindowTitle(Title)
        self.setFixedSize(680,475)

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

    def create_layout(self):
        self.create_block_tabs()
        #self.ui.layout().setContentsMargins(3, 3, 3, 3)          
        #self.ui.ButtonName.setIcon(QtGui.QIcon(IconsPath+'Locator.png'))

    def create_connections(self):

        def Demo(self):
            print 'This is a DemoFunc'
        
        #self.ui.ButtonName.clicked.connect(self.Demo)
        #self.ui.ButtonName.clicked.connect(lambda: print 'this is lambda')

    def button_in_side_panel(name):
        print (name)

    def create_block_tabs(self):
        'Create scroll bar and delete Top Buttons in every tab'   

        #remove the margins in the QT DESIGNER file
        self.ui.top_layout.setContentsMargins(0, 0, 0, 0)          
        
        #create main tabs
        self.tabs = QTabWidget()
        self.tabs.setMaximumHeight(110)          
        
       #based on json files and folders create tabs with buttons
        blocks_folders = os.listdir(Folder + '/Blocks')
        print blocks_folders
        for folder in blocks_folders:

            tab = QTabWidget()
            self.tabs.addTab(tab,folder.split(' ')[1]) #this removes the number from the name
            #tab layout
            tab_layout = QGroupBox()
            tab.setLayout(tab_layout)

            #create a scroll widget per tab
            scroll_area = QScrollArea()
            scroll_area.setWidgetResizable(True)

            scroll_area.setMinimumHeight(65)          
            scroll_layout = QHBoxLayout() #create a layout for the buttons
            scroll_area.setLayout(scroll_layout)

            tab_layout.addWidget(scroll_area)

            #create all the buttons:
            for i in range (30):
                button = QPushButton(folder)
                scroll_layout.addWidget(button)      
                button.setFixedSize(50,50)

        '''
        self.tab1.layout = QVBoxLayout(self)
        self.pushButton1 = QPushButton("PyQt5 button")
        self.tab1.layout.addWidget(self.pushButton1)
        self.tab1.setLayout(self.tab1.layout)
        '''
        #parent tabs to layout
        self.ui.top_layout.addWidget(self.tabs)

    def delete_side_buttons(self):
        'Delete Side Buttons'
    def create_side_buttons(self):
        'Side Buttons'

    def create_properties_layout(self):
        'Create All Properties Stuff'
    def delete_properties_layout(self):
        'Clear All Properties Layout'



if __name__ == "__main__":

    try:
        AutoRigger_ui.close() # pylint: disable=E0601
        AutoRigger_ui.deleteLater()
    except:
        pass
    AutoRigger_ui = AutoRigger()
    AutoRigger_ui.show()

