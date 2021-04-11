'''
version: 1.0.0
date: 21/04/2020

#----------------
content: 

This will create a UI for the autorriger tool. Is dinamically created based on the .json files inside the folders

#----------------
how to: 
	
import Mosaic_Tools
from Mosaic_Tools.UI import load_autoRigger
reload(load_autoRigger)

try:AutoRigger.close()
except:pass
AutoRigger = load_autoRigger.AutoRigger()
AutoRigger.show()

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
import sys
import json

#-------------------------------------------------------------------

#QT WIndow!
PATH = os.path.dirname(__file__)

Title = 'Mosaic // Autor_Rigger'
Folder = PATH.replace('\UI', '') 
UI_File = 'autoRigger.ui'
IconsPath =  Folder + '/Icons/'

#-------------------------------------------------------------------
def add_sys_folders_remove_compiled():
    #get all the paths for the blocks in the sys path
    file_path = (str(__file__))
    for folder in os.listdir(Folder + '/Blocks'):
        #print (folder)
        blocks_path = file_path.replace('UI\load_autoRigger.py','Blocks//{}'.format(folder))
        #print (blocks_path)
        if blocks_path not in sys.path:
            sys.path.append(blocks_path)

    #Delete all pyc in the block folders so we dont need the reload in the codes:  
    path = Folder + '//Blocks'
    for path, subdirs, files in os.walk(path):
        for name in files:
            #print('Search: ' + os.path.join(path, name))
            if '.pyc' in str(name):
                print (name + ': Have been deleted')
                os.remove(os.path.join(path, name))
    
    # also remove pyc from UIs folder
    path = Folder 
    for path, subdirs, files in os.walk(path):
        for name in files:
            #print('Search: ' + os.path.join(path, name))
            if '.pyc' in str(name):
                print (name + ': Have been deleted')
                os.remove(os.path.join(path, name))

#-------------------------------------------------------------------


def maya_main_window():
    
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(long(main_window_ptr), QtWidgets.QWidget)


class AutoRigger(QtWidgets.QDialog):
    
    def __init__(self, parent=maya_main_window()):
        super(AutoRigger, self).__init__(parent)

        self.setWindowTitle(Title)
        #self.setFixedSize(680,475)
        #load blocks folders to sys and remove all the compiled info 
        add_sys_folders_remove_compiled()

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
        self.create_block_buttons()
        #self.ui.layout().setContentsMargins(3, 3, 3, 3)          
        #self.ui.ButtonName.setIcon(QtGui.QIcon(IconsPath+'Locator.png'))

    def create_connections(self):

        def Demo(self):
            print ('This is a DemoFunc')
        
        #self.ui.ButtonName.clicked.connect(self.Demo)
        #self.ui.ButtonName.clicked.connect(lambda: print 'this is lambda')

    def button_in_side_panel(name):
        print (name)

    def create_block_buttons(self):
        ''
        #'create all the buttons in the tabs blocks' 
        print (Folder)
        blocks_folders = os.listdir(Folder + '\\Blocks')
        #blocks_folders = ['01_Presets', '02_Biped']
        print ('Block Folders : ' + str(blocks_folders))
        
        for block_folder in blocks_folders:
            
            clean_folder_name = block_folder.split('_')[1]
            files = os.listdir(Folder + '/Blocks/' + block_folder )
            
            for block_file in files:
                #print(block_file)
                
                if not '.json' in str(block_file): #if the file is not a json continue with the next one
                    #print ('skiped' + block_file)
                    continue                
                #read the json file with block information
                real_path =  Folder + '/Blocks/' + block_folder + '/' + block_file
                #print (real_path)
                with open(real_path, "r") as block_info:
                    block = json.load(block_info)               

                #create button
                button = QPushButton(str(block_file).split('_')[1].replace('.json', ''))#get a nicer name
                button.clicked.connect(partial (self.create_new_block, real_path))
                button.setToolTip(block['Description'])
                if block['Enable'] == 'False':
                    button.setEnabled(False)

                #parent to correct tab
                if block_folder == '01_Presets':
                    self.ui.presets_layout.addWidget(button)        
                elif block_folder == '02_Biped':
                    self.ui.biped_layout.addWidget(button)              
                elif block_folder == '03_Facial':
                    self.ui.facial_layout.addWidget(button)  
                elif block_folder == '04_Animals':
                    self.ui.animals_layout.addWidget(button)  
                elif block_folder == '05_Props':
                    self.ui.props_layout.addWidget(button)  
                else:
                    self.ui.other_layout.addWidget(button)  

                button.setFixedSize(40, 40)
                
    def create_new_block(self,bock_path):
        
        #read json
        with open(bock_path, "r") as block_info:
            block = json.load(block_info) 
        
        exec block['import']
        exec block['reload']
        exec block['exec_command']

    def delete_side_buttons(self):
        'Delete Side Buttons'
    def create_side_buttons(self):
        'Side Buttons'

    def create_properties_layout(self):
        'Create All Properties Stuff'
    def delete_properties_layout(self):
        'Clear All Properties Layout'

#-------------------------------------------------------------------

if __name__ == "__main__":

    try:
        AutoRigger_ui.close() # pylint: disable=E0601
        AutoRigger_ui.deleteLater()
    except:
        pass
    AutoRigger_ui = AutoRigger()
    AutoRigger_ui.show()

#-------------------------------------------------------------------


