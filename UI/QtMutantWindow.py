import os

from PySide2 import QtUiTools
from PySide2 import QtWidgets
from PySide2.QtWidgets import *
from PySide2 import QtGui,QtCore
from shiboken2 import wrapInstance

from maya.app.general.mayaMixin import MayaQWidgetDockableMixin

import maya.OpenMayaUI as omui

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
	def __init__(self, parent=get_maya_main_window()):
		super(Qt_Mutant, self).__init__(parent)

		self.setWindowTitle('Mutant Tools')

		self.designer_loader(path = PATH, ui_file = '/QtMutantWindow.ui')

		self.add_size_grip(layout = self.master_ui.size_grip_layout)
		self.make_frameless()
		self.set_margins()
		self.move_top_corner()

		self.connect_buttons()

	def connect_buttons(self):
		self.master_ui.close_button.clicked.connect(self.close)

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

	def set_margins(self, top=10, buttom=10, right=10, left=10):
		self.master_ui.layout().setContentsMargins(left, top, right, buttom)

	# ------------------------------------------------
	def set_title(self, text = 'Mt'):
		self.master_ui.child_title_label.setText(text)

	# ------------------------------------------------

	def read_stylesheet(self, path , stylesheet):
		css_file = path + '/' + stylesheet
		with open('dog_breeds.txt') as f:
			css = f

		return css

	# ------------------------------------------------

	def make_frameless(self):
		""" Make UI Frameless

		Returns:

		"""
		self.oldPos = self.pos()
		self.setWindowFlags(QtCore.Qt.Tool | QtCore.Qt.FramelessWindowHint | QtCore.Qt.CustomizeWindowHint)
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

	def mouseMoveEvent(self, event):
		"""Move Frameless Ui with it

		Args:
			event:not sure but qt understand it

		Returns:

		"""
		if self.scale ==  True:
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

	def resizeEvent(self, event):
		"""

		Args:
			event:not sure but qt understand it

		Returns:

		"""
		self.scale = True

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
		print (size_image)
		self.size_grip.setStyleSheet('\nimage: url({});\nwidth: 8px;\nmax-height: 8px;\n'.format(size_image))

	# ------------------------------------------------

	def make_big_or_small(self):
		''

	def dock_left(self):
		''

	def dock_right(self):
		''
