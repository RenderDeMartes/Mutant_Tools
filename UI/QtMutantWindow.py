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
imp.reload(QtMutantWindow)
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

import os
from maya import cmds
from maya import mel

from PySide2 import QtUiTools
from PySide2 import QtWidgets
from PySide2.QtWidgets import *
from PySide2 import QtGui,QtCore
from shiboken2 import wrapInstance

from maya.app.general.mayaMixin import MayaQWidgetDockableMixin
import maya.OpenMayaUI as omui

import imp
import Mutant_Tools.UI.CustomWidgets.expandableWidget as expandableWidget
imp.reload(expandableWidget)

#--------------------------------------------------------------------------------
PATH = os.path.dirname(__file__)
FOLDER = PATH.replace('\\UI', '')
ICONS_FOLDER = FOLDER + '//Icons//'

#--------------------------------------------------------------------------------

def get_maya_main_window():
	main_window_ptr = omui.MQtUtil.mainWindow()
	return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)

#--------------------------------------------------------------------------------

class Qt_Mutant(QtWidgets.QMainWindow):

	# ------------------------------------------------
	def __init__(self, parent=get_maya_main_window(), *args, **kwargs):
		super().__init__(parent)

		self.setObjectName('MainMutantWindow')
		self.setWindowTitle('Mutant Tools')
		self.current_size_mode = 'small'

		self.designer_loader(path = PATH, ui_file = '/QtMutantWindow.ui')

		self.add_size_grip(layout = self.master_ui.size_grip_layout)
		self.make_frameless()
		self.set_margins()
		self.move_top_corner()
		self.set_title()
		self.set_stylesheet(widget = self.master_ui)

		self.connect_buttons()

	def connect_buttons(self):
		self.master_ui.close_button.clicked.connect(self.close)
		self.master_ui.max_button.clicked.connect(self.check_size)

	# ------------------------------------------------

	def designer_loader(self, path, ui_file):
		f = QtCore.QFile(path + ui_file)
		f.open(QtCore.QFile.ReadOnly)

		loader = QtUiTools.QUiLoader()
		self.master_ui = loader.load(f, parentWidget=self)

		f.close()

	def designer_loader_child(self, path, ui_file):
		f = QtCore.QFile(path + ui_file)
		f.open(QtCore.QFile.ReadOnly)

		loader = QtUiTools.QUiLoader()
		self.ui = loader.load(f, parentWidget=None)

		self.master_ui.mutant_Layout.addWidget(self.ui)

		f.close()

	# ------------------------------------------------

	def set_margins(self, top=5, buttom=5, right=8, left=8):
		self.master_ui.layout().setContentsMargins(left, top, right, buttom)

	# ------------------------------------------------
	def set_title(self, text = 'Mutant'):
		self.master_ui.child_title_label.setText(text)

	# ------------------------------------------------

	def read_stylesheet(self, path , stylesheet):
		css_file = path + '/' + stylesheet
		with open(css_file) as f:
			css = f.read()

		return css

	def set_stylesheet(self, widget):
		css = self.read_stylesheet(path = os.path.dirname(__file__) + '\\Stylesheets',
													stylesheet = 'FramelessMutant.css')

		widget.setStyleSheet(css)

	# ------------------------------------------------

	def make_frameless(self):
		""" Make UI Frameless

		Returns:

		"""
		self.oldPos = self.pos()
		self.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.FramelessWindowHint | QtCore.Qt.CustomizeWindowHint)
		#https://python-forum.io/thread-25568.html

	# ------------------------------------------------

	def move_top_corner(self):
		"""	Move to screen center

		Returns:

		"""

		self.move(25,25)


	def mousePressEvent(self, event):
		"""	Event when mouse is press to grab the current position of the UI


		Args:
			event: not sure but qt understand it

		Returns:

		"""
		self.scale = False
		self.oldPos = event.globalPos()

	# ------------------------------------------------
	def mouseDoubleClickEvent(self, event):
		#scale with double click
		if event.button() == QtCore.Qt.RightButton:
			self.check_size()

	# ------------------------------------------------

	def mouseMoveEvent(self, event):
		"""Move Frameless Ui with it

		Args:
			event:not sure but qt understand it

		Returns:

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

	def resizeEvent(self, event):
		"""

		Args:
			event:not sure but qt understand it

		Returns:

		"""
		#avoid move when scaling the windown
		self.scale = True


	def closeEvent(self, event):
		try:
			cmds.deleteUI('myToolDock')
		except:
			pass
	# ------------------------------------------------

	def add_size_grip(self, layout):
		"""Add size grip to layouts

		Args:
			layout: layout name to put the size grip

		Returns:

		"""
		self.size_grip = QSizeGrip(self)
		layout.addWidget(self.size_grip, 0, QtCore.Qt.AlignBottom | QtCore.Qt.AlignRight)
		size_image = '{}sizeGrip.png'.format(ICONS_FOLDER).replace('\\', '/')
		self.size_grip.setStyleSheet('\nimage: url({});\nwidth: 8px;\nmax-height: 8px;\n'.format(size_image))

	# ------------------------------------------------

	def check_size(self):
		if self.current_size_mode == 'small':
			self.showMaximized()
			self.current_size_mode = 'big'
		else:
			self.current_size_mode = 'small'
			self.setWindowState(QtCore.Qt.WindowNoState)

	# ------------------------------------------------

	def dock_left_setup(self):
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
		self.dock_left_setup()
		self.dock_left_setup()


	def dock_right_setup(self):
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
		self.dock_right_setup()
		self.dock_right_setup()

	# ------------------------------------------------

	def create_separator(self):
		separator = QtWidgets.QLabel()
		separator.setStyleSheet("border : 5px solid grey; ")
		separator.setFixedHeight(1)

		return separator

	# ------------------------------------------------

	def create_vertical_separator(self):
		separator = QtWidgets.QLabel()
		separator.setStyleSheet("border : 5px solid grey; ")
		separator.setFixedWidth(1)

		return separator