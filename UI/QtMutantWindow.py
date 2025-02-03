# -*- coding: utf-8 -*-
from __future__ import absolute_import, division
'''
version: 1.0.0
date: 21/04/2020

#----------------
content:

This will create a UI for the autorriger tool. Is dinamically created based on the .json files inside the folders

#----------------
how to:
import Mutant_Tools.UI
from Mutant_Tools.UI import QtMutantWindow
reload(QtMutantWindow)
mtui = QtMutantWindow.Qt_Mutant()
mtui.show()

#----------------
dependencies:

QT FILE
ICONS
JSON FILES
Main Mutant

#----------------
licence: https://www.eulatemplate.com/live.php?token=FGISW7ApRfgywum6murbBmLcusKONzkv
author:  Esteban Rodriguez <info@renderdemartes.com>

'''
import sys
import os
import platform
import  json

from maya import cmds
from maya import mel
from pathlib import Path

from PySide2 import QtUiTools
from PySide2 import QtWidgets
from PySide2.QtWidgets import *
from PySide2 import QtGui,QtCore
from shiboken2 import wrapInstance


from maya.app.general.mayaMixin import MayaQWidgetDockableMixin
import maya.OpenMayaUI as omui
try:
    import importlib;from importlib import reload
except:
    import imp;from imp import reload

from Mutant_Tools.UI.AutoRigger import load_autoRiggerMenu
reload(load_autoRiggerMenu)

#--------------------------------------------------------------------------------
PATH = os.path.dirname(__file__)
PATH = Path(PATH)
PATH_PARTS = PATH.parts[:-1]
FOLDER=''
for p in PATH_PARTS:
	FOLDER = os.path.join(FOLDER, p)
PATH = os.path.join(FOLDER, 'UI')
ICONS_FOLDER = os.path.join(FOLDER,'Icons')

#--------------------------------------------------------------------------------

python_version = sys.version[0]
def get_maya_main_window():
	main_window_ptr = omui.MQtUtil.mainWindow()
	return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)

#--------------------------------------------------------------------------------

class Qt_Mutant(QtWidgets.QMainWindow):

	# ------------------------------------------------
	def __init__(self, parent=get_maya_main_window()):
		"""
        Initialize the Qt_Mutant instance.

        Args:
            parent (QtWidgets.QWidget): Parent widget for the main window.
                Defaults to the Maya main window.
        """
		super(Qt_Mutant, self).__init__(parent)
		#super().__init__(parent)


		self.setObjectName('MainMutantWindow')
		self.setWindowTitle('Mutant Tools')
		self.current_size_mode = 'small'
		
		self.designer_loader(path = PATH, ui_file = 'QtMutantWindow.ui')
		
		self.add_size_grip(layout = self.master_ui.size_grip_layout)
		self.popup_mode = False
		self.make_frameless()
		self.set_margins()
		self.move_to_center_screen()
		self.set_title()
		self.set_stylesheet(widget = self.master_ui)

		self.connect_buttons()

		self.minimize_state = False
		self.minimize_size = self.master_ui.size()

	# -------------------------------------------------

	def connect_buttons(self):
		"""Connect button signals to their respective slots."""
		self.master_ui.close_button.clicked.connect(self.exit_ui)
		self.master_ui.max_button.clicked.connect(self.check_size)
		self.master_ui.min_button.clicked.connect(self.minimize)

	# ------------------------------------------------

	def exit_ui(self):
		"""Close the Mutant Tools UI."""
		self.close()

	def create_menu(self):
		self.menu = load_autoRiggerMenu.AutoRiggerMenu()
		self.master_ui.menuLayout.addWidget(self.menu)

	# ------------------------------------------------

	def designer_loader(self, path, ui_file):
		"""
        Load the main UI from a designer file.

        Args:
            path (str): The path to the directory containing the UI file.
            ui_file (str): The name of the UI file.
        """

		ui_file = os.path.join(path, ui_file)
		f = QtCore.QFile(ui_file)
		f.open(QtCore.QFile.ReadOnly)

		loader = QtUiTools.QUiLoader()
		self.master_ui = loader.load(f, parentWidget=self)

		f.close()

	def designer_loader_child(self, path, ui_file):
		"""
        Load child UI elements and add them to the main UI.

        Args:
            path (str): The path to the directory containing the UI file.
            ui_file (str): The name of the UI file.
        """
		ui_file = os.path.join(path, ui_file)
		#print(ui_file)
		f = QtCore.QFile(ui_file)
		f.open(QtCore.QFile.ReadOnly)

		loader = QtUiTools.QUiLoader()
		self.ui = loader.load(f, parentWidget=None)

		self.master_ui.mutant_Layout.addWidget(self.ui)

		f.close()

	# ------------------------------------------------

	def set_margins(self, top=5, buttom=5, right=8, left=8):
		"""
        Set the margins for the main UI layout.

        Args:
            top (int): Top margin value. Defaults to 5.
            buttom (int): Bottom margin value. Defaults to 5.
            right (int): Right margin value. Defaults to 8.
            left (int): Left margin value. Defaults to 8.
        """
		self.master_ui.layout().setContentsMargins(left, top, right, buttom)

	# ------------------------------------------------
	def set_title(self, text='Mutant'):
		"""
        Set the title for the main UI.

        Args:
            text (str): The text to set as the title. Defaults to 'Mutant'.
        """
		self.master_ui.child_title_label.setText(text)

	# ------------------------------------------------

	def read_stylesheet(self, path, stylesheet):
		"""
        Read and return the contents of a stylesheet file.

        Args:
            path (str): The path to the directory containing the stylesheet file.
            stylesheet (str): The name of the stylesheet file.

        Returns:
            str: The contents of the stylesheet file.
        """
		css_file = os.path.join(path, stylesheet)
		with open(css_file) as f:
			css = f.read()

		return css

	def set_stylesheet(self, widget):
		"""
        Set the stylesheet for a given widget.

        Args:
            widget (QtWidgets.QWidget): The widget for which to set the stylesheet.
        """

		file_path = os.path.join(os.path.dirname(__file__), 'Stylesheets')
		css = self.read_stylesheet(path =file_path, stylesheet='FramelessMutant.css')

		widget.setStyleSheet(css)

	# ------------------------------------------------

	def make_frameless(self):
		"""Make the main UI frameless."""
		self.oldPos = self.pos()
		self.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.FramelessWindowHint | QtCore.Qt.CustomizeWindowHint)

		return

	# ------------------------------------------------

	def move_top_corner(self):
		"""Move the main UI to the top left corner of the screen."""

		self.move(25,25)

	def move_to_center_screen(self):
		"""Move the main UI to the center of the screen."""
		qtRectangle = self.frameGeometry()
		centerPoint = QDesktopWidget().availableGeometry().center()
		qtRectangle.moveCenter(centerPoint)
		self.move(qtRectangle.topLeft())
		centerPoint = QDesktopWidget().availableGeometry().center()
		qtRectangle.moveCenter(centerPoint)
		self.move(qtRectangle.topLeft()/2)

	def mousePressEvent(self, event):
		"""
        Handle mouse press event to grab the current position of the UI.

        Args:
            event: The mouse press event.
        """
		self.scale = False
		self.oldPos = event.globalPos()
		if self.popup_mode:
			self.close()

	# ------------------------------------------------
	def mouseDoubleClickEvent(self, event):
		"""
        Handle mouse double-click event. Scale with double click

        Args:
            event: The mouse double-click event.
        """
		#scale with double click
		if event.button() == QtCore.Qt.RightButton:
			self.check_size()

	# ------------------------------------------------

	def mouseMoveEvent(self, event):
		"""
        Handle mouse move event to move the frameless UI.

        Args:
            event: The mouse move event.
        """
		if self.scale ==  True:
			return

		if self.current_size_mode == 'big':
			#self.check_size()
			return

		if event.buttons() == QtCore.Qt.NoButton:
			"Simple mouse motion"
		elif event.buttons() == QtCore.Qt.LeftButton:
			"Left click drag"
			delta = QtCore.QPoint(event.globalPos() - self.oldPos)
			self.move(self.x() + delta.x(), self.y() + delta.y())
			self.oldPos = event.globalPos()
		elif event.buttons() == QtCore.Qt.RightButton:
			"Right click drag"
	# ------------------------------------------------

	def open_over_mouse(self):
		"""Open the UI over the mouse cursor position."""
		point = QtGui.QCursor.pos()
		self.move(point.x(), point.y())

	def resizeEvent(self, event):
		"""
        Handle resize event.

        Args:
            event: The resize event.
        """
		#avoid move when scaling the windown
		self.scale = True


	def enable_popup_mode(self):
		"""Enable popup mode for the UI."""
		self.popup_mode = True
		self.setWindowFlags(QtCore.Qt.Popup)

	def closeEvent(self, event):
		"""Handle the close event for the UI."""
		try:
			cmds.deleteUI('myToolDock')
		except:
			pass
	# ------------------------------------------------

	def add_size_grip(self, layout):
		"""
        Add a size grip to the specified layout.

        Args:
            layout: The layout to which the size grip should be added.
        """
		self.size_grip = QSizeGrip(self)
		layout.addWidget(self.size_grip, 0, QtCore.Qt.AlignBottom | QtCore.Qt.AlignRight)
		size_image = '{}'.format(os.path.join(ICONS_FOLDER, 'sizeGrip.png'))
		self.size_grip.setStyleSheet('\nimage: url({});\nwidth: 8px;\nmax-height: 8px;\n'.format(size_image))

	# ------------------------------------------------

	def check_size(self):
		"""Toggle between small and big size modes for the UI."""
		if self.current_size_mode == 'small':
			self.showMaximized()
			self.current_size_mode = 'big'
		else:
			self.current_size_mode = 'small'
			self.setWindowState(QtCore.Qt.WindowNoState)

	# ------------------------------------------------

	def add_icons_based_on_json(self, json_file):
		"""
        Add icons to buttons based on data from a JSON file.

        Args:
            json_file (str): The path to the JSON file containing icon data.
        """

		with open(json_file) as icons_file:
			icons_data = json.load(icons_file)

		for b in icons_data:
			button = self.findChild(QtWidgets.QPushButton, b)
			icon=os.path.join(ICONS_FOLDER, '{}.png'.format(icons_data[b]))
			if not icon:
				continue
			if os.path.exists(icon):
				button.setIcon(QtGui.QIcon(icon))
				button.setIconSize(QtCore.QSize(20, 20))

	# ------------------------------------------------

	def dock_left_setup(self):
		"""Set up the UI for docking on the left side."""
		'''Doesnt Work Yet'''
		#http://www.jason-parks.com/artoftech/?p=439
		if cmds.window('myTool_window', q=1, ex=1):
			cmds.deleteUI('myTool_window')

		if cmds.dockControl('myToolDock', q=1, ex=1):
			cmds.deleteUI('myToolDock')
		allowedAreas = ['right', 'left']
		try:
			floatingLayout = cmds.paneLayout(configuration='single', width=300, height=400)
			cmds.dockControl('myToolDock', area='left', allowedArea=allowedAreas,
							 content=floatingLayout, label='Mutant_Tols')
			cmds.control('MainMutantWindow', e=True, p=floatingLayout)
		except:
			pass

	def dock_left(self):
		"""Dock the UI on the left side."""
		self.dock_left_setup()
		self.dock_left_setup()

	def dock_right_setup(self):
		"""Set up the UI for docking on the right side."""
		#http://www.jason-parks.com/artoftech/?p=439
		'''Doesnt Work Yet'''

		if cmds.window('myTool_window', q=1, ex=1):
			cmds.deleteUI('myTool_window')

		if cmds.dockControl('myToolDock', q=1, ex=1):
			cmds.deleteUI('myToolDock')
		allowedAreas = ['right', 'left']
		try:
			floatingLayout = cmds.paneLayout(configuration='single', width=300, height=400)
			cmds.dockControl('myToolDock', area='right', allowedArea=allowedAreas,
							 content=floatingLayout, label='Mutant_Tols')
			cmds.control('MainMutantWindow', e=True, p=floatingLayout)
		except:
			pass

	def dock_right(self):
		"""Dock the UI on the right side."""
		self.dock_right_setup()
		self.dock_right_setup()

	# ------------------------------------------------

	def create_separator(self):
		"""Create and return a horizontal separator."""
		separator = QtWidgets.QLabel()
		separator.setStyleSheet("border : 5px solid grey; ")
		separator.setFixedHeight(1)

		return separator

	# ------------------------------------------------

	def create_vertical_separator(self):
		"""Create and return a vertical separator."""
		separator = QtWidgets.QLabel()
		separator.setStyleSheet("border : 5px solid grey; ")
		separator.setFixedWidth(1)

		return separator

	# ------------------------------------------------

	def minimize(self):
		"""Minimize or restore the UI."""

		if not self.minimize_state:
			self.minimize_state = True
			self.minimize_size = self.master_ui.size()
			self.ui.hide()
			self.setFixedSize(0, 0)
		else:
			self.minimize_state = False
			self.resize(self.minimize_size)
			self.setFixedSize(self.minimize_size)
			self.ui.show()
			self.setMaximumSize(100000, 100000)
			self.setMinimumSize(0, 0)