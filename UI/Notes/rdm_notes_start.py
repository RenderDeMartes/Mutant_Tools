from __future__ import absolute_import
'''
try:notes_ui.close()
except:pass

import RdM_Notes
from RdM_Notes import rdm_notes_start
reload(RdM_Notes.rdm_notes_start)

notes_ui = rdm_notes_start.NotesUI()
notes_ui.show()

'''

from PySide2 import QtWidgets
from PySide2 import QtUiTools
from PySide2 import QtGui,QtCore
from PySide2.QtGui import QPixmap
from shiboken2 import wrapInstance
from PySide2.QtWidgets import QLabel, QMainWindow, QApplication, QWidget, QVBoxLayout, QFrame, QComboBox 

import maya.mel as mel
import maya.cmds as cmds
#import pymel.core as pm
from functools import partial
import maya.OpenMayaUI as omui

import time
try:
    import importlib;from importlib import reload
except:
    import imp;from imp import reload

import Mutant_Tools
from Mutant_Tools.UI.Notes.Utils.notes_util import *
reload (Mutant_Tools.UI.Notes.Utils.notes_util)

import tempfile
temp_folder = os.path.join(tempfile.gettempdir(), 'Notes')

#-------------------------------------------------------
#QT WIndow!

Title = 'Notes'
PATH = os.path.dirname(__file__)
Folder = os.path.join(PATH, 'Notes_UI')
UI_File = 'notes_ui.ui'
ResourcesPath =  os.path.join(Folder, 'Resources')

def maya_main_window():

    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)

class NotesUI(QtWidgets.QDialog):
    

    def __init__(self, parent=maya_main_window()):

        super(NotesUI, self).__init__(parent)

        self.setWindowTitle(Title)
        #self.setFixedSize(416,218)

        self.init_ui()
        self.create_layout()
        self.create_connections()

    def init_ui(self):      

        ui_path = os.path.join(Folder, UI_File)
        f = QtCore.QFile(ui_path)
        f.open(QtCore.QFile.ReadOnly)

        #------------------------------------
        imagePath  = os.path.join(PATH, 'Resources')
        '''
        picture = QPixmap(imagePath+"BG.jpg")
        label = QLabel(self)
        label.setPixmap(picture)
        label.setGeometry(QtCore.QRect(0, 0, picture.width(), picture.height()))
        '''
        #------------------------------------
        loader = QtUiTools.QUiLoader()
        self.ui = loader.load(f, parentWidget=self)
        f.close()
        

    def create_layout(self):

        imagePath  = cmds.internalVar(usd = True) + ResourcesPath       
        self.ui.create_file_note.setIcon(QtGui.QIcon(os.path.join(ResourcesPath.replace('Notes_UI', ''), 'add.png')))
        self.ui.create_file_note.setIconSize(QtCore.QSize(25, 25))
        #self.ui.create_personal_note.setIcon(QtGui.QIcon(imagePath+'add.png'))
        #self.ui.create_personal_note.setIconSize(QtCore.QSize(25, 25))

    def create_connections(self):

        self.reload_file_tab()
        self.ui.create_file_note.clicked.connect(self.load_create_file_note_ui)

        ''
        #self.ui.BStoUIBtn.clicked.connect(self.createSliders_ui)
        #self.ui.loadGeoBtn.clicked.connect(self.reload_ui)
    
    def reopen_window(self):
                
                self.repaint()
                self.update()                
                pos = self.pos()
                self.close()
                open_window_at(pos) 


    def load_create_file_note_ui(self):

        from Mutant_Tools.UI.Notes.Notes_UI import load_create_note
        reload(load_create_note)

        pos = self.pos()
        create_notes_ui = load_create_note.Create_UI()
        create_notes_ui.show()
        create_notes_ui.move(pos)

        self.close()

    #----------------------------------------------------------------------------------------
   
    def delete_and_reload_layout(self, layout, note = ''):
        if cmds.objExists(note):
            delete = self.delete_btn_command(note_name = note)
        if delete :
            for i in reversed(range(layout.count())): 
                layout.itemAt(i).widget().setParent(None)

    def delete_btn_command(self, note_name):
        dialog = cmds.confirmDialog( title='Delete note?', message='Delete note: {}?'.format(note_name), button=['Yes','No'], defaultButton='Np', cancelButton='No', dismissString='No' )
        if dialog =='Yes':
            cmds.delete(note_name)
            return 'Yes'
        else:
            return None

    def show_image(self, note):
        temp_image = decode_image(cmds.getAttr('{}.image'.format(note)))
        print(temp_image)
        window = cmds.window()
        cmds.paneLayout()
        cmds.image( image=temp_image )
        cmds.showWindow( window )

    def edit_note(self, text, node): 
        print (node)
        if text.isEnabled():
            text.setDisabled(True)
            cmds.setAttr('{}.notes'.format(node), text.toPlainText(), type = 'string')
            text.setPlainText(text.toPlainText())
        else:
            text.setEnabled(True)

    def change_mode(self, node, combo_box_mode, layout,  *args):
        print (node)
        mode =  (combo_box_mode.currentIndex())
        cmds.setAttr('{}.mode'.format(node), mode)
        if mode == 0:
            style_sheet = "color: rgb(255, 255, 255);"
        elif mode == 1:
            style_sheet = "color: rgb(0, 255, 0);"
        else:
            style_sheet = "color: rgb(200, 0, 0);"
        combo_box_mode.setStyleSheet(style_sheet)

    def go_to_camera_ui(self, node):
        go_to_camera(node)

    #----------------------------------------------------------------------------------------
    def reload_file_tab(self):
        
        if cmds.objExists('RdM_Notes'):
            notes = cmds.container('RdM_Notes', q = True, nl=True)
            if notes==None:
                print ('Create a note to start.'),
                return
        else:
            create_container()
            print ('Create a note to start.'),
            return

        for num, note in enumerate(notes):
            
            title = cmds.getAttr('{}.name'.format(note))
            current_mode = cmds.getAttr('{}.mode'.format(note))
            note_image = cmds.getAttr('{}.image'.format(note))
            decoded_image = decode_image(note_image)
            try:note_details = cmds.getAttr('{}.notes'.format(note))
            except: note_details = 'Th!=e was created empty'
            date = cmds.getAttr('{}.date'.format(note))

            current_ui_id = 0
            #new layout
            hbox = QtWidgets.QHBoxLayout()

            #new label            
            label = QtWidgets.QLabel(note)

            #DELETE NOTE
            delete = QtWidgets.QPushButton()
            delete.setFixedSize(15, 15)
            #delete.clicked.connect(partial (self.delete_btn_command,note))
            delete.clicked.connect(partial (self.delete_and_reload_layout, hbox, note))
            delete.setIcon(QtGui.QIcon(os.path.join(ResourcesPath.replace('Notes_UI', ''), 'delete.png')))
            delete.setIconSize(QtCore.QSize(10, 10))

            #NOTE DETAILS
            line_edit = QtWidgets.QPlainTextEdit(note_details + ' : ' + date)
            line_edit.setDisabled(True)
            line_edit.setMaximumHeight(50)
            line_edit.setToolTip(line_edit.toPlainText())

            #EDIT NOTE
            edit = QtWidgets.QPushButton()
            edit.setFixedSize(20, 20)
            edit.clicked.connect(partial (self.edit_note, line_edit, note))

            edit.setIcon(QtGui.QIcon(os.path.join(ResourcesPath.replace('Notes_UI', ''), 'edit.png')))
            edit.setIconSize(QtCore.QSize(15, 15))

            #VIEW IMAGE
            view_image = QtWidgets.QPushButton()
            view_image.setFixedSize(50, 50)
            view_image.clicked.connect(partial(self.show_image, note))
            view_image.setIcon(QtGui.QIcon(os.path.join(ResourcesPath.replace('Notes_UI', ''), 'image.png')))
            view_image.setIconSize(QtCore.QSize(60, 60))

            #GO TO CAMERA
            camera = QtWidgets.QPushButton()
            camera.setFixedSize(20, 20)
            camera.clicked.connect(partial(self.go_to_camera_ui, note))
            camera.setIcon(QtGui.QIcon(os.path.join(ResourcesPath.replace('Notes_UI', ''), 'camera.png')))
            camera.setIconSize(QtCore.QSize(20, 20))

            #SET AS
            set_as_label = QtWidgets.QLabel('Set as:')

            #MODE COMBO BOX
            menut_items = ['To Do','Done','Urgent']
            options_menu = QtWidgets.QComboBox()
            options_menu.addItems(menut_items)
            options_menu.currentIndexChanged.connect(partial (self.change_mode, note, options_menu, hbox))

            if current_mode == 0:
                style_sheet = "color: rgb(255, 255, 255);"
                options_menu.setCurrentIndex(0)
            elif current_mode == 1:
                style_sheet = "color: rgb(0, 255, 0);"
                options_menu.setCurrentIndex(1)
            else:
                style_sheet = "color: rgb(200, 0, 0);"
                options_menu.setCurrentIndex(2)
            options_menu.setStyleSheet(style_sheet)

            #new layout for the new btn
            hbox.addWidget(delete)
            hbox.addWidget(label)
            hbox.addWidget(line_edit)
            hbox.addWidget(edit)  
            hbox.addWidget(view_image)  
            hbox.addWidget(camera)  
            hbox.addWidget(set_as_label)
            hbox.addWidget(options_menu)

            #add to ui
            current_ui_id = num + 1 + current_ui_id
            self.ui.file_notes_layout.addLayout(hbox, current_ui_id + 1 , 0)  

            '''
            #add line
            line = QtWidgets.QFrame()
            line.setFrameShape(QFrame.HLine)
            line.setFrameShadow(QFrame.Sunken)
            self.ui.file_notes_layout.addWidget(line)  
            '''

        #resize to fit a nice window
        if len(notes)>4:
            self.ui.setFixedSize(self.ui.file_notes_layout.sizeHint())
        else:
            self.ui.setFixedSize(531,300)

    #----------------------------------------------------------------------------------------

#----------------------------------------
# Run Window        

if __name__ == "__main__":

    try:

        NotesUI_ui.close() # pylint: disable=E0601

        NotesUI_ui.deleteLater()

    except:

        pass

    notes_ui = NotesUI()
    notes_ui.show()


#----------------------------------------


def open_window_at(pos):

    notes_ui = NotesUI()
    notes_ui.show()
    notes_ui.move(pos)



#get and move camara