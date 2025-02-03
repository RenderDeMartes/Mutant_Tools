from __future__ import absolute_import
from PySide2 import QtGui,QtCore
from PySide2 import QtUiTools
from PySide2 import QtWidgets
from shiboken2 import wrapInstance

import maya.cmds as cmds
import maya.OpenMayaUI as omui
import maya.mel as mel

import os

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

#QT WIndow!

Title = 'Create Note!'
PATH = os.path.dirname(__file__)
Folder = os.path.join(PATH)
UI_File = 'create_note.ui'
ResourcesPath =  os.path.join(Folder, 'Resources')

def maya_main_window():
    
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)

class Create_UI(QtWidgets.QDialog):
    
    def __init__(self, parent=maya_main_window()):
        super(Create_UI, self).__init__(parent)

        self.setWindowTitle(Title)
        #self.setFixedSize(682,590)
        self.init_ui()
        self.create_layout()
        self.create_connections()

    def init_ui(self):
        
        clear_temp_folder()

        #decode_image('/9j/4AAQSkZJRgABAQD/////AAD/2wBDAAEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQH/2wBDAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQH/wAARCAEsAcIDASIAAhEBAxEB/8QAHwAAAQUBAQEBAQEAAAAAAAAAAAECAwQFBgcICQoL/8QAtRAAAgEDAwIEAwUFBAQAAAF9AQIDAAQRBRIhMUEGE1FhByJxFDKBkaEII0KxwRVS0fAkM2JyggkKFhcYGRolJicoKSo0NTY3ODk6Q0RFRkdISUpTVFVWV1hZWmNkZWZnaGlqc3R1dnd4eXqDhIWGh4iJipKTlJWWl5iZmqKjpKWmp6ipqrKztLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uHi4+Tl5ufo6erx8vP09fb3+Pn6/8QAHwEAAwEBAQEBAQEBAQAAAAAAAAECAwQFBgcICQoL/8QAtREAAgECBAQDBAcFBAQAAQJ3AAECAxEEBSExBhJBUQdhcRMiMoEIFEKRobHBCSMzUvAVYnLRChYkNOEl8RcYGRomJygpKjU2Nzg5OkNERUZHSElKU1RVVldYWVpjZGVmZ2hpanN0dXZ3eHl6goOEhYaHiImKkpOUlZaXmJmaoqOkpaanqKmqsrO0tba3uLm6wsPExcbHyMnK0tPU1dbX2Nna4uPk5ebn6Onq8vP09fb3+Pn6/9oADAMBAAIRAxEAPwD836KKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigD/9k=')

        ui_path = os.path.join(Folder, UI_File)
        f = QtCore.QFile(ui_path)
        f.open(QtCore.QFile.ReadOnly)

        loader = QtUiTools.QUiLoader()
        self.ui = loader.load(f, parentWidget=self)

        f.close()

    def create_layout(self):
        
        self.ui.layout().setContentsMargins(3, 3, 3, 3)          
      
        imagePath = ResourcesPath.replace('Notes_UI', '')
        self.ui.viewport_draw.setIcon(QtGui.QIcon(os.path.join(imagePath,'draw.png')))
        self.ui.clear_viewport.setIcon(QtGui.QIcon(os.path.join(imagePath,'clear.png')))
        self.ui.capture_image.setIcon(QtGui.QIcon(os.path.join(imagePath,'capture.png')))
        self.ui.create_note.setIcon(QtGui.QIcon(os.path.join(imagePath,'add.png')))

    def create_connections(self):

        self.ui.viewport_draw.clicked.connect(self.start_grease_pencil)
        self.ui.clear_viewport.clicked.connect(lambda: cmds.delete('greasePencil*'))
        self.ui.capture_image.clicked.connect(self.capture_viewport_ui)
        self.ui.create_note.clicked.connect(self.create_file_note_ui)

    #-------------------------------
    def start_grease_pencil(self, title = 'RdM'):
        #maybe add a while loop to create infinty opens
        #this shit doesnt work so i force it :)
        for num in range(9999):
            title = str(title) + str(num)
            try:
                cmds.greasePencilCtx(title)
                cmds.setToolTo(title)
                return    
            except:
                pass            
                    
    def capture_viewport_ui(self):
        image = capture_viewport(ornaments = True if self.ui.ornaments_check.isChecked() else False)
        show_image(image)

        return image 
        
    def create_file_note_ui(self):
        
        title = self.ui.title_lineEdit.text()
        
        note= self.ui.note_TextEdit.toPlainText()
        if note == '':
            note = 'No Note Details'
            
        time_slider = int(cmds.currentTime( query=True ))

        if os.path.isfile(os.path.join(temp_folder, 'temp.jpg.{}.jpg'.format(time_slider))):
            capture = os.path.join(temp_folder, 'temp.jpg.{}.jpg'.format(time_slider))
        else:
            capture = os.path.join(temp_folder, 'temp.jpg')

        encoded_image = encode_image(capture)
        print(encode_image)

        #mode
        if self.ui.to_do.isChecked():
            mode = 0
        elif self.ui.done.isChecked():
            mode = 1
        elif self.ui.urgent.isChecked():
            mode = 2

        capture_viewport(ornaments = True if self.ui.ornaments_check.isChecked() else False)

        note = create_note_node(name = title, 
                     note = note,
                     encoded_image = encoded_image,
                     current_mode=mode)

        #load tool

        from Mutant_Tools.UI.Notes import rdm_notes_start
        reload(rdm_notes_start)
        
        notes_ui = rdm_notes_start.NotesUI()
        notes_ui.show()

        #delete all drawings
        try:
            cmds.delete('greasePencil*')    
        except:
            pass
        print (':)'),
        cmds.setToolTo('selectSuperContext')
           
        self.close()          
                                 
    #-------------------------------                    
if __name__ == "__main__":

    try:
        Create_UI_ui.close() # pylint: disable=E0601
        Create_UI_ui.deleteLater()
    except:
        pass
    Create_UI_ui = Create_UI()
    Create_UI_ui.show()


