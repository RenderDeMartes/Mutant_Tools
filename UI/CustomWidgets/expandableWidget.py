'''
version: 1.0.0
date: 21/04/2020

#----------------
content:

#----------------
how to:

import Mutant_Tools.UI
from Mutant_Tools.UI import QtMutantWindow
imp.reload(QtMutantWindow)
import Mutant_Tools.UI.CustomWidgets.expandableWidget as expandableWidget
imp.reload(expandableWidget)
try:
    mtui.close()
except:
    pass
mtui = QtMutantWindow.Qt_Mutant()
mtui.show()

exp = mtui.colapsable_widget()

#----------------
dependencies:


#----------------
licence: https://www.eulatemplate.com/live.php?token=FGISW7ApRfgywum6murbBmLcusKONzkv
author:  Esteban Rodriguez <info@renderdemartes.com>

'''




import os
from maya import cmds
from maya import mel
import PySide2
from PySide2 import QtUiTools
from PySide2 import QtWidgets
from PySide2.QtWidgets import *
from PySide2 import QtGui,QtCore
from shiboken2 import wrapInstance

from maya.app.general.mayaMixin import MayaQWidgetDockableMixin
import maya.OpenMayaUI as omui
from pathlib import Path

#--------------------------------------------------------------------------------
PATH = os.path.dirname(__file__)
PATH = Path(PATH)
FOLDER = os.path.join(*PATH.parts[:-2])
ICONS_FOLDER = os.path.join(FOLDER, 'Icons')

#------------------------------------------------------------------------------

class expandableWidget(QtWidgets.QDialog):

    def __init__(self, parent=None, title='ExpandableWidget'):

        self.parent = parent
        self.title = title
        self.layout = ''

        self.create_widget()
        self.create_connections()

    #-----------------------------------------------------------------------------------------------------------------

    def create_widget(self):
        #Top Part
        exp_box = QGroupBox()
        self.parent.addWidget(exp_box)

        main_layout = QtWidgets.QVBoxLayout()
        exp_box.setLayout(main_layout)

        h_layout = QtWidgets.QHBoxLayout()

        main_layout.addLayout(h_layout)

        self.open_button = QtWidgets.QPushButton()
        self.label = QtWidgets.QLabel(self.title)

        self.open_button.setFixedSize(15,15)
        self.open_button.setIconSize(QtCore.QSize(10,10))
        self.open_button.setIcon(QtGui.QIcon(ICONS_FOLDER + 'DDown.png'))
        #self.label_button.setStyleSheet("QPushButton{\n    border-style: none;\n    border-width: 0;\n}")

        h_layout.addWidget(self.open_button)
        h_layout.addWidget(self.label)

        separator = self.create_separator()
        #h_layout.addWidget(separator)

        #Botom Part
        v_layout = QtWidgets.QVBoxLayout()
        main_layout.addLayout(v_layout)

        self.frame = QtWidgets.QFrame()
        frame_layout = QtWidgets.QVBoxLayout()
        self.frame.setLayout(frame_layout)
        self.frame.setFrameShadow(QFrame.Plain)
        self.frame.setFrameShape(QFrame.Box)
        self.frame.setContentsMargins(0, 0, 0, 0)

        v_layout.addWidget(self.frame)

        self.layout = frame_layout
        return frame_layout

    #-----------------------------------------------------------------------------------------------------------------

    def create_separator(self):
        separator = QtWidgets.QLabel()
        separator.setStyleSheet("border : 5px solid grey; ")
        separator.setFixedHeight(1)

        return separator

    #-----------------------------------------------------------------------------------------------------------------

    def create_connections(self):
        self.open_button.clicked.connect(lambda: self.toggle_state())
        #self.label_button.clicked.connect(self.toggle_state)

    def toggle_state(self):
        if self.frame.isVisible():
            self.frame.hide()
        else:
            self.frame.show()
        self.change_button_icon()

    def collapse(self):
        self.frame.hide()
        self.change_button_icon()

    def expand(self):
        self.frame.show()
        self.change_button_icon()

    def change_button_icon(self):
        if self.frame.isVisible():
            self.open_button.setIcon(QtGui.QIcon(ICONS_FOLDER + 'DDown.png'))
        else:
            self.open_button.setIcon(QtGui.QIcon(ICONS_FOLDER + 'DRight.png'))



