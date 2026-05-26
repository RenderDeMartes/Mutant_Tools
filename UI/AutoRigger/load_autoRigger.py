from __future__ import absolute_import, division
'''
version: 1.0.0
date: 21/04/2020

#----------------
content:

This will create a UI for the autorriger tool. Is dinamically created based on the .json files inside the folders

#----------------
how to:
try:
    import importlib;from importlib import reload
except:
    import imp;from imp import reload

import Mutant_Tools
from Mutant_Tools.UI.AutoRigger import load_autoRigger
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
Main Mutant

#----------------
www.mutanttools.com
author:  Esteban Rodriguez <info@renderdemartes.com>

'''
#-------------------------------------------------------------------
try:
    from shiboken6 import wrapInstance
    from PySide6 import QtGui, QtCore
    from PySide6 import QtUiTools
    from PySide6 import QtWidgets
    from PySide6.QtWidgets import *
except: 
    from shiboken2 import wrapInstance #Compatibility pre 2026
    from PySide2 import QtGui,QtCore
    from PySide2 import QtUiTools
    from PySide2 import QtWidgets
    from PySide2.QtWidgets import *
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin

import maya.OpenMayaUI as omui
from functools import partial
from maya import OpenMaya
import maya.cmds as cmds
import maya.mel as mel

import os
import time
import tempfile
import re
import html

try:
    import importlib;from importlib import reload
except:
    import imp;from imp import reload

import sys
import json
from collections import OrderedDict
from pathlib import Path
'''try:
	from rstar import convention
	convention.set_project()
except Exception as e:
	cmds.warning('Error loading rstar.convention on load_AutoRigger')
'''
from Mutant_Tools.UI.AutoRigger import load_autoRiggerMenu
reload(load_autoRiggerMenu)

from Mutant_Tools.UI.CodeReader import load_codeReader
reload(load_codeReader)
log_ui = load_codeReader.Code_Reader(mode='view', code= '', config_attr = '')

import Mutant_Tools.UI
from Mutant_Tools.UI import QtMutantWindow
reload(QtMutantWindow)

import Mutant_Tools.UI.CustomWidgets.expandableWidget as expandableWidget
reload(expandableWidget)

import Mutant_Tools.UI.CustomWidgets.codeEditorWidget as codeEditorWidget
reload(codeEditorWidget)

from Mutant_Tools.Utils.Helpers import helpers
reload(Mutant_Tools.Utils.Helpers.helpers)
from Mutant_Tools.Utils.Helpers import decorators
reload(decorators)
mh = helpers.Helpers()

import Mutant_Tools.Utils.IO
from Mutant_Tools.Utils.IO import EasySkin
reload(Mutant_Tools.Utils.IO.EasySkin)

from Mutant_Tools.Utils.IO import CtrlUtils
reload(Mutant_Tools.Utils.IO.CtrlUtils)
ctrls = CtrlUtils.Ctrls()

#-------------------------------------------------------------------

#Read name conventions as nc[''] and setup as seup['']
PATH = os.path.dirname(__file__)
PATH = Path(PATH)
PATH_PARTS = PATH.parts[:-2]
FOLDER=''
for f in PATH_PARTS:
	FOLDER = os.path.join(FOLDER, f)

JSON_FILE = os.path.join(FOLDER, 'config', 'name_conventions.json')
with open(JSON_FILE) as json_file:
	nc = json.load(json_file)
#Read curve shapes info
CURVE_FILE = os.path.join(FOLDER, 'config', 'curves.json')
with open(CURVE_FILE) as curve_file:
	curve_data = json.load(curve_file)
#setup File
SETUP_FILE = os.path.join(FOLDER, 'config', 'rig_setup.json')
with open(SETUP_FILE) as setup_file:
	setup = json.load(setup_file)
#Version File
VERSION_FILE = os.path.join(FOLDER, 'config', 'version.json')
with open(VERSION_FILE) as version_file:
	version = json.load(version_file)
#-------------------------------------------------------------------

#QT WIndow!
PATH = os.path.dirname(__file__)
PATH = Path(PATH)
PATH_PARTS = PATH.parts[:-2]
FOLDER=''
for f in PATH_PARTS:
	FOLDER = os.path.join(FOLDER, f)
UI_File = 'autoRigger.ui'
IconsPath =  os.path.join(FOLDER, 'Icons')
Title = 'AutoRigger'

#-------------------------------------------------------------------

import Mutant_Tools
import Mutant_Tools.Utils.Rigging
from Mutant_Tools.Utils.Rigging import main_mutant
reload(Mutant_Tools.Utils.Rigging.main_mutant)

mt = main_mutant.Mutant()

import Mutant_Tools.UI.CustomWidgets.expandableWidget as expandableWidget
reload(expandableWidget)

#-------------------------------------------------------------------
def add_sys_folders_remove_compiled():
	#get all the paths for the blocks in the sys path
	file_path = (str(__file__))
	for folder in os.listdir(os.path.join(FOLDER , 'Blocks')):
		blocks_path = os.path.join(FOLDER, 'Blocks', folder)
		if blocks_path not in sys.path:
			sys.path.append(blocks_path)

	#Delete all pyc in the block folders so we dont need the imp.reload in the codes:
	path = os.path.join(FOLDER, 'Blocks')
	for path, subdirs, files in os.walk(path):
		for name in files:
			#print('Search: ' + os.path.join(path, name))
			if '.pyc' in str(name):
				#print (name + ': Have been deleted')
				os.remove(os.path.join(path, name))
			if '__pycache__' in str(name):
				#print (name + ': Have been deleted')
				os.remove(os.path.join(path, name))
			if 'DS_Store' in str(name):
				# print (name + ': Have been deleted')
				os.remove(os.path.join(path, name))

	# also remove pyc from UIs folder
	path = FOLDER
	for path, subdirs, files in os.walk(path):
		for name in files:
			if '.pyc' in str(name):
				#print (name + ': Have been deleted')
				os.remove(os.path.join(path, name))
			if '.DS_Store' in str(name):
				#print (name + ': Have been deleted')
				os.remove(os.path.join(path, name))
	print ('Cache removed...')

#-------------------------------------------------------------------

class FlowLayout(QtWidgets.QLayout):
	"""A layout that arranges widgets left-to-right, wrapping to the next row."""
	def __init__(self, parent=None, margin=0, spacing=-1):
		super(FlowLayout, self).__init__(parent)
		if parent is not None:
			self.setContentsMargins(margin, margin, margin, margin)
		self._item_list = []
		self._h_spacing = spacing if spacing >= 0 else 4
		self._v_spacing = spacing if spacing >= 0 else 4

	def addItem(self, item):
		self._item_list.append(item)

	def count(self):
		return len(self._item_list)

	def itemAt(self, index):
		if 0 <= index < len(self._item_list):
			return self._item_list[index]
		return None

	def takeAt(self, index):
		if 0 <= index < len(self._item_list):
			return self._item_list.pop(index)
		return None

	def expandingDirections(self):
		return QtCore.Qt.Orientations(QtCore.Qt.Orientation(0))

	def hasHeightForWidth(self):
		return True

	def heightForWidth(self, width):
		return self._do_layout(QtCore.QRect(0, 0, width, 0), test_only=True)

	def setGeometry(self, rect):
		super(FlowLayout, self).setGeometry(rect)
		self._do_layout(rect, test_only=False)

	def sizeHint(self):
		return self.minimumSize()

	def minimumSize(self):
		size = QtCore.QSize()
		for item in self._item_list:
			size = size.expandedTo(item.minimumSize())
		margins = self.contentsMargins()
		size += QtCore.QSize(margins.left() + margins.right(), margins.top() + margins.bottom())
		return size

	def _do_layout(self, rect, test_only):
		margins = self.contentsMargins()
		effective = rect.adjusted(margins.left(), margins.top(), -margins.right(), -margins.bottom())
		x = effective.x()
		y = effective.y()
		line_height = 0
		for item in self._item_list:
			widget = item.widget()
			space_x = self._h_spacing
			space_y = self._v_spacing
			next_x = x + item.sizeHint().width() + space_x
			if next_x - space_x > effective.right() and line_height > 0:
				x = effective.x()
				y = y + line_height + space_y
				next_x = x + item.sizeHint().width() + space_x
				line_height = 0
			if not test_only:
				item.setGeometry(QtCore.QRect(QtCore.QPoint(x, y), item.sizeHint()))
			x = next_x
			line_height = max(line_height, item.sizeHint().height())
		return y + line_height - rect.y() + margins.bottom()


class DraggableButton(QtWidgets.QPushButton):
	def __init__(self, block_name, *args, **kwargs):
		super(DraggableButton, self).__init__(*args, **kwargs)
		self.block_name = block_name

	def mousePressEvent(self, event):
		if event.button() == QtCore.Qt.LeftButton:
			self.drag_start_position = event.pos()
		super(DraggableButton, self).mousePressEvent(event)

	def mouseMoveEvent(self, event):
		if not (event.buttons() & QtCore.Qt.LeftButton):
			super(DraggableButton, self).mouseMoveEvent(event)
			return
		if not hasattr(self, 'drag_start_position'):
			super(DraggableButton, self).mouseMoveEvent(event)
			return
		if (event.pos() - self.drag_start_position).manhattanLength() < QtWidgets.QApplication.startDragDistance():
			super(DraggableButton, self).mouseMoveEvent(event)
			return

		drag = QtGui.QDrag(self)
		mime_data = QtCore.QMimeData()
		mime_data.setText(self.block_name)
		drag.setMimeData(mime_data)
		exec_func = getattr(drag, 'exec_', drag.exec)
		exec_func(QtCore.Qt.MoveAction)

class DraggableTabButton(QtWidgets.QPushButton):
	"""Tab button that can be dragged into the side panel to create a block at a specific position."""
	def __init__(self, json_path, *args, **kwargs):
		super(DraggableTabButton, self).__init__(*args, **kwargs)
		self.json_path = json_path

	def mousePressEvent(self, event):
		if event.button() == QtCore.Qt.LeftButton:
			self.drag_start_position = event.pos()
		super(DraggableTabButton, self).mousePressEvent(event)

	def mouseMoveEvent(self, event):
		if not (event.buttons() & QtCore.Qt.LeftButton):
			return
		if not hasattr(self, 'drag_start_position'):
			return
		if (event.pos() - self.drag_start_position).manhattanLength() < QtWidgets.QApplication.startDragDistance():
			return

		drag = QtGui.QDrag(self)
		mime_data = QtCore.QMimeData()
		mime_data.setText('create:' + self.json_path)
		drag.setMimeData(mime_data)

		# Show the button icon as the drag pixmap
		icon = self.icon()
		if not icon.isNull():
			pixmap = icon.pixmap(32, 32)
			drag.setPixmap(pixmap)
			drag.setHotSpot(QtCore.QPoint(16, 16))

		exec_func = getattr(drag, 'exec_', drag.exec)
		exec_func(QtCore.Qt.CopyAction)

class DraggableLabel(QtWidgets.QLabel):
	def __init__(self, block_name, text, *args, **kwargs):
		super(DraggableLabel, self).__init__(text, *args, **kwargs)
		self.block_name = block_name

	def mousePressEvent(self, event):
		if event.button() == QtCore.Qt.LeftButton:
			self.drag_start_position = event.pos()
			event.accept()
		else:
			super(DraggableLabel, self).mousePressEvent(event)

	def mouseMoveEvent(self, event):
		if not (event.buttons() & QtCore.Qt.LeftButton):
			super(DraggableLabel, self).mouseMoveEvent(event)
			return
		if not hasattr(self, 'drag_start_position'):
			super(DraggableLabel, self).mouseMoveEvent(event)
			return
		if (event.pos() - self.drag_start_position).manhattanLength() < QtWidgets.QApplication.startDragDistance():
			super(DraggableLabel, self).mouseMoveEvent(event)
			return

		event.accept()
		drag = QtGui.QDrag(self)
		mime_data = QtCore.QMimeData()
		mime_data.setText(self.block_name)
		drag.setMimeData(mime_data)
		exec_func = getattr(drag, 'exec_', drag.exec)
		exec_func(QtCore.Qt.MoveAction)

class DraggableBlockWidget(QtWidgets.QGroupBox):
	block_dropped = QtCore.Signal(str, str, bool)
	block_create_dropped = QtCore.Signal(str, str, bool)

	def __init__(self, block_name, *args, **kwargs):
		super(DraggableBlockWidget, self).__init__(*args, **kwargs)
		self.block_name = block_name
		self.setAcceptDrops(True)
		self.setFocusPolicy(QtCore.Qt.NoFocus)
		self._drop_indicator = None

		# Timer for auto-scrolling during drag-and-drop
		self._scroll_timer = QtCore.QTimer(self)
		self._scroll_timer.setInterval(50)
		self._scroll_timer.timeout.connect(self._do_autoscroll)

	def _do_autoscroll(self):
		scroll_area = None
		parent = self.parentWidget()
		while parent:
			if isinstance(parent, QtWidgets.QScrollArea):
				scroll_area = parent
				break
			parent = parent.parentWidget()

		if scroll_area:
			viewport = scroll_area.viewport()
			global_cursor_pos = QtGui.QCursor.pos()
			pos_in_viewport = viewport.mapFromGlobal(global_cursor_pos)

			scroll_bar = scroll_area.verticalScrollBar()
			if scroll_bar and scroll_bar.isVisible():
				margin = 40  # Trigger scrolling within 40 pixels of top/bottom
				step = 10    # Amount to scroll each tick (50ms)
				vh = viewport.height()
				vw = viewport.width()
				y = pos_in_viewport.y()
				x = pos_in_viewport.x()

				# Ensure the cursor is still within the boundaries of the scroll viewport
				if 0 <= x <= vw and 0 <= y <= vh:
					if y < margin:
						scroll_bar.setValue(max(scroll_bar.value() - step, scroll_bar.minimum()))
						return
					elif y > vh - margin:
						scroll_bar.setValue(min(scroll_bar.value() + step, scroll_bar.maximum()))
						return

		# Stop the timer if we are no longer in the scroll zone or viewport
		self._scroll_timer.stop()

	def _is_valid_drop(self, mime_data):
		if not mime_data.hasText():
			return False
		text = mime_data.text()
		if text.startswith('create:'):
			return True
		return text != self.block_name

	def dragEnterEvent(self, event):
		if self._is_valid_drop(event.mimeData()):
			event.acceptProposedAction()
			return
		event.ignore()

	def dragMoveEvent(self, event):
		if self._is_valid_drop(event.mimeData()):
			drop_above = event.pos().y() < (self.height() / 2)
			new_indicator = 'top' if drop_above else 'bottom'
			if self._drop_indicator != new_indicator:
				self._drop_indicator = new_indicator
				self.update()

			# Check for auto-scrolling
			scroll_area = None
			parent = self.parentWidget()
			while parent:
				if isinstance(parent, QtWidgets.QScrollArea):
					scroll_area = parent
					break
				parent = parent.parentWidget()

			if scroll_area:
				viewport = scroll_area.viewport()
				pos_in_viewport = self.mapTo(viewport, event.pos())
				margin = 40
				y = pos_in_viewport.y()
				if y < margin or y > viewport.height() - margin:
					if not self._scroll_timer.isActive():
						self._scroll_timer.start()
				else:
					self._scroll_timer.stop()

			event.acceptProposedAction()
			return
		event.ignore()

	def dragLeaveEvent(self, event):
		self._scroll_timer.stop()
		if self._drop_indicator is not None:
			self._drop_indicator = None
			self.update()
		event.accept()

	def dropEvent(self, event):
		self._scroll_timer.stop()
		self._drop_indicator = None
		self.update()
		text = event.mimeData().text()
		drop_above = event.pos().y() < (self.height() / 2)
		if text.startswith('create:'):
			json_path = text[7:]  # strip 'create:' prefix
			self.block_create_dropped.emit(json_path, self.block_name, drop_above)
		else:
			self.block_dropped.emit(text, self.block_name, drop_above)
		event.acceptProposedAction()

	def paintEvent(self, event):
		super(DraggableBlockWidget, self).paintEvent(event)
		if self._drop_indicator:
			painter = QtGui.QPainter(self)
			pen = QtGui.QPen(QtGui.QColor(90, 200, 250))  # Light blue separator
			pen.setWidth(4)
			painter.setPen(pen)
			rect = self.rect()
			if self._drop_indicator == 'top':
				y = rect.top() + 2
				painter.drawLine(rect.left(), y, rect.right(), y)
			elif self._drop_indicator == 'bottom':
				y = rect.bottom() - 2
				painter.drawLine(rect.left(), y, rect.right(), y)

class ListResizer(QtWidgets.QFrame):
	def __init__(self, target, *args, **kwargs):
		super(ListResizer, self).__init__(*args, **kwargs)
		self.target = target
		self.setCursor(QtCore.Qt.SizeVerCursor)
		self.setFixedHeight(8)
		self.setStyleSheet("background-color: #3a3a3a; border-radius: 4px;")
		self._is_resizing = False
	def mousePressEvent(self, event):
		if event.button() == QtCore.Qt.LeftButton:
			self._is_resizing = True
			self._start_y = event.globalPos().y()
			self._start_height = self.target.height()
	def mouseMoveEvent(self, event):
		if self._is_resizing:
			diff = event.globalPos().y() - self._start_y
			new_h = max(50, self._start_height + diff)
			if hasattr(self.target, 'is_manually_resized'):
				self.target.is_manually_resized = True
			self.target.setFixedHeight(new_h)
	def mouseReleaseEvent(self, event):
		if self._is_resizing:
			# Persist the code block height so it's remembered across sessions
			try:
				from Mutant_Tools.UI.CustomWidgets import codeEditorWidget as _cew
				if isinstance(self.target, _cew.IDECodeEditor):
					cmds.optionVar(iv=('mutant_code_block_height', self.target.height()))
			except:
				pass
		self._is_resizing = False
	def mouseDoubleClickEvent(self, event):
		if event.button() == QtCore.Qt.LeftButton:
			if hasattr(self.target, 'is_manually_resized'):
				self.target.is_manually_resized = False
				if hasattr(self.target, 'adjust_height_to_fit'):
					self.target.adjust_height_to_fit()

class SearchOverlay(QtWidgets.QFrame):
	"""Floating search bar that appears over the AutoRigger on Ctrl+F."""

	def __init__(self, parent, search_line):
		super(SearchOverlay, self).__init__(parent)
		self._search_line = search_line
		self.setFrameShape(QtWidgets.QFrame.NoFrame)
		self.setFixedHeight(38)
		self.setMinimumWidth(260)
		self.setMaximumWidth(340)
		self.setStyleSheet(
			'SearchOverlay {'
			'  background-color: #3c3f41;'
			'  border: 1px solid #5f6161;'
			'  border-radius: 4px;'
			'}'
		)

		layout = QtWidgets.QHBoxLayout(self)
		layout.setContentsMargins(8, 4, 8, 4)
		layout.setSpacing(6)



		self.field = QtWidgets.QLineEdit()
		self.field.setPlaceholderText('Search blocks...')
		self.field.setStyleSheet(
			'QLineEdit {'
			'  background-color: #45494a;'
			'  border: 1px solid #646464;'
			'  border-radius: 2px;'
			'  color: #bbbbbb;'
			'  padding: 2px 6px;'
			'  font-size: 12px;'
			'  selection-background-color: #555555;'
			'}'
			'QLineEdit:focus {'
			'  border: 1px solid #888888;'
			'}'
		)
		layout.addWidget(self.field)

		# Sync overlay field with the existing search_line
		self.field.textChanged.connect(self._on_text_changed)
		self.field.installEventFilter(self)
		self.hide()

	def popup(self):
		"""Show the overlay centered near the top of the parent."""
		p = self.parent()
		if p:
			w = min(self.maximumWidth(), int(p.width() * 0.6))
			self.setFixedWidth(max(self.minimumWidth(), w))
			x = (p.width() - self.width()) // 2
			self.move(x, 8)
		self.field.setText(self._search_line.text())
		self.show()
		self.raise_()
		self.field.setFocus()
		self.field.selectAll()

	def dismiss(self):
		"""Hide the overlay and clear the search."""
		self.field.clear()
		self.hide()

	def _on_text_changed(self, text):
		self._search_line.setText(text)

	def eventFilter(self, obj, event):
		if obj is self.field:
			if event.type() == QtCore.QEvent.KeyPress:
				if event.key() == QtCore.Qt.Key_Escape:
					self.dismiss()
					return True
				elif event.key() in (QtCore.Qt.Key_Return, QtCore.Qt.Key_Enter):
					self.hide()
					return True
			elif event.type() == QtCore.QEvent.FocusOut:
				# Small delay so clicks inside the overlay aren't interrupted
				QtCore.QTimer.singleShot(150, self._check_focus)
		return super(SearchOverlay, self).eventFilter(obj, event)

	def _check_focus(self):
		if not self.field.hasFocus() and self.isVisible():
			self.hide()


class AutoRigger(QtMutantWindow.Qt_Mutant):

	OBJECT_NAME = 'MutantAutoRiggerWindow'

	def __init__(self):
		# Close any existing instance (survives module reloads)
		for widget in QtWidgets.QApplication.topLevelWidgets():
			if widget is not self and widget.objectName() == self.OBJECT_NAME:
				try:
					widget.close()
					widget.deleteLater()
				except Exception:
					pass

		super(AutoRigger, self).__init__()
		self.setObjectName(self.OBJECT_NAME)

		#UI Init
		self.setWindowTitle(Title)
		self.set_title(Title)

		self.create_menu()

		self.resize(605, 750)

		#load blocks folders to sys and remove all the compiled info in BLOCKS and UI Folder
		if mt.check_dev_mode():
			add_sys_folders_remove_compiled()
		self.reload_ready = False

		#009_Data init
		self.current_block = None
		self.current_block_folder = None
		self.side_block_widgets = {}
		self.side_block_edit_buttons = {}

		self.designer_loader_child(path=os.path.join(FOLDER,'UI','AutoRigger'), ui_file=UI_File)

		self.create_menus()
		self.create_layout()
		self.create_connections()
		self.reload_blocks_if_isnt_working()

		#update icons
		mt.update_icons()

		#find tools updates:
		#mt.compare_versions()

		#load script job
		self.current_selected_block = False
		self.ignore_next_selection_changed = False
		self.mutant_sj = cmds.scriptJob(event=["SelectionChanged", self.mutant_script_job])

		self.recipes_dict = {}

		self.studio_name = setup['studio']
		self.ui.tabs.setTabText(1, self.studio_name)

		# Connect tab change to save active tab live
		self.ui.tabs.currentChanged.connect(
			lambda idx: cmds.optionVar(intValue=('mutant_active_tab', idx))
		)

		try:OpenMaya.MGlobal.displayInfo('<3')
		except:pass

	#-------------------------------------------------------------------

	def force_load_of_dependency_plugins(self):
		plugins_windows = ['quatNodes.mll', 'objExport.mll','lookdevKit.mll', 'matrixNodes.mll']
		plugins_linux = plugins = ['quatNodes.so', 'objExport.so','lookdevKit.so', 'matrixNodes.so']
		for w_plugin, l_plugin in zip(plugins_windows, plugins_linux):
			try:cmds.loadPlugin(w_plugin)
			except:cmds.loadPlugin(l_plugin)

	def exit_ui(self):

		close_comfirm = cmds.confirmDialog(
						title='Close Mutant Autorigger',
						message='Are you sure?',
						button=['Close', 'Stay Open'],
						defaultButton='Stay Open',
						dismissString='Stay Open',
						cancelButton = 'Stay Open')

		if close_comfirm == 'Close':
			print('Mutant is closing')
			self.close()

	#-------------------------------------------------------------------

	def mutant_script_job(self):
		if self.ignore_next_selection_changed:
			self.ignore_next_selection_changed = False
			return

		sel = cmds.ls(sl=True)
		if not sel:
			return
		if self.current_selected_block == sel[0]:
			return

		try:
			if str(sel[0]).endswith('_Block'):
				self.create_properties_layout(block = cmds.ls(sl=True)[0], scroll_to_block=True)
				self.current_selected_block = sel[0]
		except:
			pass


	#-------------------------------------------------------------------
	def reload_blocks_if_isnt_working(self):

		try:
			import exec_limb
		except:
			self.reload_all_blocks()

	#-------------------------------------------------------------------
	def create_menus(self):

		# self.menu = load_autoRiggerMenu.AutoRiggerMenu()
		# self.ui.menuLayout.addWidget(self.menu)
		# self.search_button = QPushButton()
		# #self.search_button.setFixedSize(20,20)
		# #self.ui.menuLayout.addWidget(self.search_button)

		#Relaod blocks connection in Menu
		self.menu.dev_reload.triggered.connect(self.reload_all_blocks)
		self.menu.update_all_blocks.triggered.connect(self.update_all_blocks_cmd)
		self.menu.wrap_icons.toggled.connect(self.toggle_wrap_icons)
		

	def _setup_splitter(self):
		"""Replace fixed layouts with draggable QSplitters (vertical between tabs/content, horizontal between blocks/properties)."""
		if hasattr(self, '_splitter_installed'):
			return

		main_layout = self.ui.layout()
		if main_layout is None:
			return

		# --- Horizontal splitter: side_scroll | properties ---
		# Remove the max-width constraint on side_scroll so splitter controls it
		self.ui.side_scroll.setMaximumWidth(16777215)
		self.ui.side_scroll.setMinimumWidth(120)

		# Collect all widgets from the right-side vertical layout into a container
		right_widget = QtWidgets.QWidget()
		right_layout = QtWidgets.QVBoxLayout(right_widget)
		right_layout.setContentsMargins(0, 0, 0, 0)

		v_layout = self.ui.findChild(QtWidgets.QVBoxLayout, 'verticalLayout_2')
		if v_layout:
			while v_layout.count():
				child = v_layout.takeAt(0)
				if child.widget():
					right_layout.addWidget(child.widget())
				elif child.layout():
					right_layout.addLayout(child.layout())

		self._h_splitter = QtWidgets.QSplitter(QtCore.Qt.Horizontal)
		self._h_splitter.addWidget(self.ui.side_scroll)
		self._h_splitter.addWidget(right_widget)
		self._h_splitter.setStretchFactor(0, 0)
		self._h_splitter.setStretchFactor(1, 1)
		self._h_splitter.setSizes([200, 400])
		self._h_splitter.setHandleWidth(5)

		# --- Vertical splitter: tabs on top | h_splitter on bottom ---
		# Find the tabs and the grid that holds the blocks/properties
		tabs_widget = self.ui.tabs
		# Remove tabs max height so it can shrink
		tabs_widget.setMaximumHeight(16777215)

		# Remove the menuLayout_3 wrapper around tabs so we can reparent it
		menu_layout_3 = self.ui.findChild(QtWidgets.QVBoxLayout, 'menuLayout_3')

		self._v_splitter = QtWidgets.QSplitter(QtCore.Qt.Vertical)
		self._v_splitter.addWidget(tabs_widget)
		self._v_splitter.addWidget(self._h_splitter)
		self._v_splitter.setStretchFactor(0, 0)
		self._v_splitter.setStretchFactor(1, 1)
		# Default height for tabs – enough for ~3 rows of icons
		self._v_splitter.setSizes([180, 500])
		self._v_splitter.setHandleWidth(5)

		splitter_style = 'QSplitter::handle { background-color: #3a3a3a; }'
		self._h_splitter.setStyleSheet(splitter_style)
		self._v_splitter.setStyleSheet(splitter_style)

		# Insert the vertical splitter into the main grid
		# Find gridLayout_12 and remove it since h_splitter now owns its content
		grid_12 = None
		for i in range(main_layout.count()):
			item = main_layout.itemAt(i)
			if item and item.layout() and item.layout().objectName() == 'gridLayout_12':
				grid_12 = item.layout()
				main_layout.removeItem(item)
				break

		# Remove menuLayout_3 item that held the tabs
		for i in range(main_layout.count()):
			item = main_layout.itemAt(i)
			if item and item.layout() and item.layout().objectName() == 'menuLayout_3':
				main_layout.removeItem(item)
				break

		# Add the vertical splitter spanning the content area
		main_layout.addWidget(self._v_splitter, 1, 0)

		self._splitter_installed = True

		# Connect splitter signals to save state live as the user drags
		self._h_splitter.splitterMoved.connect(self._on_splitter_moved)
		self._v_splitter.splitterMoved.connect(self._on_splitter_moved)

	# -------------------------------------------------------------------
	# UI State Persistence
	# -------------------------------------------------------------------

	def _on_splitter_moved(self, pos, index):
		"""Save splitter sizes whenever the user drags a splitter handle."""
		self._save_splitter_state()

	def _save_splitter_state(self):
		"""Save only splitter positions to optionVar."""
		try:
			if hasattr(self, '_v_splitter'):
				sizes = self._v_splitter.sizes()
				if len(sizes) == 2 and sizes[0] > 0 and sizes[1] > 0:
					cmds.optionVar(intValue=('mutant_vsplit_0', sizes[0]))
					cmds.optionVar(intValue=('mutant_vsplit_1', sizes[1]))
			if hasattr(self, '_h_splitter'):
				sizes = self._h_splitter.sizes()
				if len(sizes) == 2 and sizes[0] > 0 and sizes[1] > 0:
					cmds.optionVar(intValue=('mutant_hsplit_0', sizes[0]))
					cmds.optionVar(intValue=('mutant_hsplit_1', sizes[1]))
		except:
			pass

	def _save_ui_state(self):
		"""Save window geometry, splitter positions, and active tab to Maya optionVar."""
		try:
			# Window geometry
			geo = self.geometry()
			cmds.optionVar(intValue=('mutant_win_x', geo.x()))
			cmds.optionVar(intValue=('mutant_win_y', geo.y()))
			cmds.optionVar(intValue=('mutant_win_w', geo.width()))
			cmds.optionVar(intValue=('mutant_win_h', geo.height()))

			# Splitters
			self._save_splitter_state()

			# Active tab index
			if hasattr(self, 'ui') and hasattr(self.ui, 'tabs'):
				cmds.optionVar(intValue=('mutant_active_tab', self.ui.tabs.currentIndex()))
		except Exception as e:
			print('Mutant: could not save UI state: {}'.format(e))

	def _restore_ui_state(self):
		"""Restore window geometry, splitter positions, and active tab from Maya optionVar."""
		try:
			# Restore window geometry
			if (cmds.optionVar(ex='mutant_win_w') and cmds.optionVar(ex='mutant_win_h')):
				w = cmds.optionVar(q='mutant_win_w')
				h = cmds.optionVar(q='mutant_win_h')
				if w > 100 and h > 100:
					self.resize(w, h)

				if (cmds.optionVar(ex='mutant_win_x') and cmds.optionVar(ex='mutant_win_y')):
					x = cmds.optionVar(q='mutant_win_x')
					y = cmds.optionVar(q='mutant_win_y')
					# Validate the position is on-screen
					screen = None
					try:
						screen = QtGui.QGuiApplication.screenAt(QtCore.QPoint(x, y))
					except:
						pass
					if screen:
						self._centered_once = True  # Skip the auto-center
						self.move(x, y)

			# Restore vertical splitter sizes
			if hasattr(self, '_v_splitter'):
				if (cmds.optionVar(ex='mutant_vsplit_0') and cmds.optionVar(ex='mutant_vsplit_1')):
					s0 = cmds.optionVar(q='mutant_vsplit_0')
					s1 = cmds.optionVar(q='mutant_vsplit_1')
					if s0 > 0 and s1 > 0:
						self._v_splitter.setSizes([s0, s1])

			# Restore horizontal splitter sizes
			if hasattr(self, '_h_splitter'):
				if (cmds.optionVar(ex='mutant_hsplit_0') and cmds.optionVar(ex='mutant_hsplit_1')):
					s0 = cmds.optionVar(q='mutant_hsplit_0')
					s1 = cmds.optionVar(q='mutant_hsplit_1')
					if s0 > 0 and s1 > 0:
						self._h_splitter.setSizes([s0, s1])

			# Restore active tab
			if hasattr(self, 'ui') and hasattr(self.ui, 'tabs'):
				if cmds.optionVar(ex='mutant_active_tab'):
					tab_idx = cmds.optionVar(q='mutant_active_tab')
					if 0 <= tab_idx < self.ui.tabs.count():
						self.ui.tabs.setCurrentIndex(tab_idx)
		except Exception as e:
			print('Mutant: could not restore UI state: {}'.format(e))

	def showEvent(self, event):
		"""Restore UI state after the window is fully shown and laid out."""
		super(AutoRigger, self).showEvent(event)
		if not hasattr(self, '_state_restored'):
			self._state_restored = True
			# Use a 150ms delay to let Qt finalize all layout calculations
			QtCore.QTimer.singleShot(150, self._restore_ui_state)

	def closeEvent(self, event):
		"""Save UI state before closing."""
		self._save_ui_state()
		try:
			cmds.scriptJob(kill=self.mutant_sj, force=True)
		except:
			pass
		super(AutoRigger, self).closeEvent(event)

	# -------------------------------------------------------------------

	def toggle_wrap_icons(self, state):
		"""Toggle between wrapping FlowLayout and horizontal QHBoxLayout for tab layouts."""
		cmds.optionVar(intValue=("mutant_wrap_icons", state))
		self._setup_tab_layouts()

	def _setup_tab_layouts(self):
		"""Set up the tab layouts as either wrapping FlowLayout or horizontal QHBoxLayout,
		depending on the optionVar mutant_wrap_icons."""
		wrap = cmds.optionVar(q="mutant_wrap_icons") if cmds.optionVar(ex="mutant_wrap_icons") else True

		layout_names = [
			'presets_layout', 'studio_layout', 'biped_layout',
			'facial_layout', 'animals_layout', 'vehicles_layout',
			'clothes_layout', 'props_layout', 'games_layout',
			'data_layout', 'other_layout'
		]

		for name in layout_names:
			old_layout = getattr(self.ui, name, None)
			if old_layout is None:
				continue

			# Get the parent widget containing this layout
			parent_item = old_layout.parent()
			if parent_item is None:
				continue

			# Find which layout/widget owns old_layout and replace it
			parent_layout = None
			if hasattr(parent_item, 'layout'):
				parent_layout = parent_item.layout() if callable(parent_item.layout) else parent_item
			if parent_layout is None:
				continue

			# Extract existing widgets from the old layout
			widgets = []
			while old_layout.count():
				child = old_layout.takeAt(0)
				if child.widget():
					widgets.append(child.widget())

			# Clear everything from the parent layout
			while parent_layout.count():
				item = parent_layout.takeAt(0)
				if item.widget():
					w = item.widget()
					if w not in widgets:
						w.setParent(None)
						w.deleteLater()
				elif item.layout():
					l = item.layout()
					while l.count():
						sub_item = l.takeAt(0)
						if sub_item.widget() and sub_item.widget() not in widgets:
							sub_item.widget().deleteLater()
					l.setParent(None)

			# Now create the new layout based on the wrap setting
			if wrap:
				# Use FlowLayout
				new_layout = FlowLayout(spacing=4)
				if isinstance(parent_layout, QtWidgets.QGridLayout):
					parent_layout.addLayout(new_layout, 0, 0)
				else:
					parent_layout.addLayout(new_layout)
			else:
				# Use QHBoxLayout
				new_layout = QtWidgets.QHBoxLayout()
				new_layout.setContentsMargins(0, 0, 0, 0)
				new_layout.setSpacing(4)

				if isinstance(parent_layout, QtWidgets.QGridLayout):
					parent_layout.addLayout(new_layout, 0, 0)
					# Add the horizontal spacer to push buttons to the left
					spacer = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
					parent_layout.addItem(spacer, 0, 1)
				else:
					parent_layout.addLayout(new_layout)
					spacer = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
					parent_layout.addItem(spacer)

			# Re-add all our widgets into the new layout
			for w in widgets:
				new_layout.addWidget(w)

			# Update the attribute on self.ui to point to the new layout
			setattr(self.ui, name, new_layout)

	def create_layout(self):
		self.create_block_buttons()
		self.delete_side_buttons()

		try:self.create_all_side_buttons()
		except Exception as e:
			print(e)

		try:self.ui.layout().setContentsMargins(3, 3, 3, 3)
		except:pass
		self.ui.progressBar.setValue(0)
		self.ui.bar_label.setText('Mutant')

		#set Manual Icons
		self.ui.prebuild.setIcon(QtGui.QIcon(os.path.join(IconsPath ,'PRECODE.png')))
		self.ui.current_code.setIcon(QtGui.QIcon(os.path.join(IconsPath ,'CODE.png')))
		self.ui.postbuild.setIcon(QtGui.QIcon(os.path.join(IconsPath ,'POSTCODE.png')))
		self.ui.reload_ui.setIcon(QtGui.QIcon(os.path.join(IconsPath ,'RELOAD.png')))
		self.ui.log.setIcon(QtGui.QIcon(os.path.join(IconsPath ,'LOG.png')))
		self.ui.search_button.setIcon(QtGui.QIcon(os.path.join(IconsPath, 'RELOAD.png')))
		self.ui.search_button.setIconSize(QtCore.QSize(14, 14))
		self.ui.search_button.setStyleSheet("QPushButton { border: none; background: transparent; } QPushButton:hover { background-color: rgba(255, 255, 255, 10); border-radius: 3px; }")
		self.ui.search_button.setToolTip("Refresh and reset block search")

		# Built-in clear (X) button inside the search field
		self.ui.search_line.setClearButtonEnabled(True)

		# Setup resizable splitters and wrapping block buttons
		self._setup_splitter()
		self._setup_tab_layouts()

		# keep current scroll position on UI refresh; outliner changes handle scrolling via scriptJob


	def reload_ui(self):

		#Search delete
		self.ui.search_line.setText('')

		self.create_layout()
		#OpenMaya.MGlobal.displayInfo('<3')

		#rest propierties layout too
		for i in reversed(range(self.ui.properties_layout.count())):
			self.ui.properties_layout.itemAt(i).widget().setParent(None)
		self.ui.block_label.setText('Mutant Autorigger')

	def create_connections(self):

		self.ui.reload_ui.clicked.connect(self.reload_ui)
		self.ui.build_btn.clicked.connect(self.build_autorigger)

		self.ui.prebuild.clicked.connect(lambda : self.edit_prebuild_code(self.current_block))
		self.ui.current_code.clicked.connect(lambda : self.view_build_code(self.current_block))
		self.ui.postbuild.clicked.connect(lambda : self.edit_postbuild_code(self.current_block))
		self.ui.log.clicked.connect(lambda : self.view_log())

		self.ui.search_button.clicked.connect(self.search_command)
		self.ui.search_line.textChanged.connect(self.search_command)

		# Ctrl+F shortcut to focus the search/filter field
		try:
			search_shortcut = QtGui.QShortcut(QtGui.QKeySequence('Ctrl+F'), self)
		except AttributeError:
			search_shortcut = QtWidgets.QShortcut(QtGui.QKeySequence('Ctrl+F'), self)
		search_shortcut.activated.connect(self._focus_search)

	#-------------------------------------------------------------------
	def reload_all_blocks(self):

		if self.reload_ready and not mt.check_dev_mode():
			return True

		add_sys_folders_remove_compiled()

		#'create all the buttons in the tabs blocks'
		blocks_folders = os.listdir(os.path.join(FOLDER, 'Blocks'))

		#Progress bar
		from Mutant_Tools.UI.ProgressBar import load_progress_bar
		reload(load_progress_bar)
		cProgressBarUI = load_progress_bar.ProgressBarUI(items=blocks_folders,
														 title='Loading Mutant...')
		cProgressBarUI.show()
		avoid_folders = ['.DS_Store']

		for num, block_folder in enumerate(blocks_folders):

			if block_folder in avoid_folders:
				continue
			cProgressBarUI.set_percent(num)

			print (block_folder)
			if block_folder not in sys.path:
				sys.path.append(block_folder)

			# clean_folder_name = block_folder.split('_')[1]
			# files = os.listdir(os.path.join(FOLDER, 'Blocks', block_folder))
			#
			# for num, block_file in enumerate(files):
			# 	#print(block_file)
			#
			# 	if not '.json' in str(block_file): #if the file != a json continue with the next one
			# 		continue
			#
			# 	#read the json file with block information
			# 	real_path =  os.path.join(FOLDER, 'Blocks', block_folder,  block_file)
			# 	sys.path.append(real_path)
			#
			# 	with open(real_path, "r") as block_info:
			# 		block = json.load(block_info)
			# 		#reaload with json files info if dev mode is on, off loads faster
			# 		try:
			# 			exec(block['import'])
			# 			exec(block['imp.reload'])
			# 		except Exception as e:
			# 			print('Importing error on {}'.format(block_file), e)

		cProgressBarUI.close()

	#-------------------------------------------------------------------
	def get_all_jsons(self):
		import glob
		main_path = os.path.join(FOLDER, 'Blocks')
		json_paths = os.path.join(main_path, '*', '*.json')
		return glob.glob(json_paths)

	def get_mutant_config_attr(self, attr, config):
		attr_type = cmds.getAttr('{}.{}'.format(config, attr), type=True)

		if attr_type == 'string':
			attr = attr + '_string'
		elif attr_type == 'enum':
			attr = attr + '_enum'
		elif attr_type == 'long':
			attr = attr + '_float'
		elif attr_type == 'bool':
			attr = attr + '_bool'

		return attr

	def set_config_attr_value(self, config, attr, attr_key, value):
		attr_path = '{}.{}'.format(config, attr)
		if not cmds.attributeQuery(attr, node=config, exists=True):
			return
		if value is None:
			return

		try:
			if 'string' in attr_key:
				cmds.setAttr(attr_path, str(value), type='string')
			elif 'enum' in attr_key:
				enums = cmds.attributeQuery(attr, node=config, listEnum=True)
				if enums:
					enum_values = enums[0].split(':')
					if isinstance(value, str) and value in enum_values:
						cmds.setAttr(attr_path, enum_values.index(value))
					elif isinstance(value, (int, float)):
						cmds.setAttr(attr_path, int(value))
			elif 'float' in attr_key:
				cmds.setAttr(attr_path, int(float(value)))
			elif 'bool' in attr_key:
				if isinstance(value, str):
					cmds.setAttr(attr_path, 1 if value.strip().lower() == 'true' else 0)
				else:
					cmds.setAttr(attr_path, 1 if value else 0)
		except Exception as e:
			print('Could not set {}: {}'.format(attr_path, e))

	def get_config_attr_value(self, config, attr, attr_key):
		attr_path = '{}.{}'.format(config, attr)
		if not cmds.attributeQuery(attr, node=config, exists=True):
			return None

		try:
			if 'enum' in attr_key:
				current_index = cmds.getAttr(attr_path)
				enums = cmds.attributeQuery(attr, node=config, listEnum=True)
				if enums:
					enum_values = enums[0].split(':')
					if 0 <= int(current_index) < len(enum_values):
						return enum_values[int(current_index)]
				return current_index
			return cmds.getAttr(attr_path)
		except Exception as e:
			print('Could not read {}: {}'.format(attr_path, e))
			return None

	def update_config(self, block, config, module):
		attrs_in_json = module.get('attrs', {})
		attrs_in_config = cmds.listAttr(config, ud=True) or []

		skips = ['precode', 'postcode', 'Build_Command', 'Import_Command']
		attrs_to_recreate = []
		existing_values = {}

		# Phase 1: snapshot existing values; drop attrs not in JSON
		for attr in attrs_in_config:
			if attr in skips:
				continue
			clean_attr = self.get_mutant_config_attr(attr, config)
			if clean_attr not in attrs_in_json:
				if cmds.attributeQuery(attr, node=config, exists=True):
					try:
						cmds.deleteAttr('{}.{}'.format(config, attr))
					except Exception as e:
						print('Could not delete {}.{}: {}'.format(config, attr, e))
			else:
				attrs_to_recreate.append(attr)
				existing_values[clean_attr] = self.get_config_attr_value(config=config, attr=attr, attr_key=clean_attr)

		# Phase 2: delete attrs that will be rebuilt from JSON
		for attr in attrs_to_recreate:
			if cmds.attributeQuery(attr, node=config, exists=True):
				try:
					cmds.deleteAttr('{}.{}'.format(config, attr))
				except Exception as e:
					print('Could not delete {}.{}: {}'.format(config, attr, e))

		# Phase 3: recreate from JSON, then restore the saved value (or keep JSON default for new attrs)
		for attr in attrs_in_json:
			attr_name = attr.rsplit('_', 1)[0]
			try:
				if 'string' in attr:
					mt.string_attr(input=config, name=attr_name, string=module['attrs'][attr])
				elif 'enum' in attr:
					mt.new_enum(input=config, name=attr_name, enums=module['attrs'][attr])
				elif 'float' in attr:
					mt.new_attr_interger(input=config, name=attr_name, min=1, max=20, default=int(float(module['attrs'][attr])))
				elif 'bool' in attr:
					mt.new_boolean(input=config, name=attr_name, dv=module['attrs'][attr])
			except Exception as e:
				print('Could not create {}.{}: {}'.format(config, attr_name, e))
				continue

			value_to_set = module['attrs'][attr]
			if attr in existing_values and existing_values[attr] is not None:
				value_to_set = existing_values[attr]

			self.set_config_attr_value(config=config, attr=attr_name, attr_key=attr, value=value_to_set)

		# Update block icon if provided in JSON
		if 'Icon' in module:
			icon_name = module['Icon']
			if not icon_name.endswith('.png'):
				icon_name += '.png'
			icon_path = os.path.join(FOLDER, 'Icons', icon_name)
			if cmds.attributeQuery('iconName', node=block, exists=True):
				try:
					cmds.setAttr('{}.iconName'.format(block), icon_path, type="string")
				except Exception as e:
					print('Could not update icon for {}: {}'.format(block, e))

	def update_all_blocks_cmd(self):
		if not cmds.objExists('Mutant_Build'):
			cmds.warning('Mutant_Build was not found in scene.')
			return

		confirm = cmds.confirmDialog(
			title='Update All Blocks',
			message='Apply update_cmd to all blocks in the scene?',
			button=['Update', 'Cancel'],
			defaultButton='Update',
			cancelButton='Cancel',
			dismissString='Cancel')

		if confirm != 'Update':
			return

		jsons = self.get_all_jsons()
		json_modules = {}
		for json_file in jsons:
			if os.path.basename(json_file).lower() == 'order.json':
				continue
			try:
				with open(json_file) as block_data:
					module = json.load(block_data)
				import_cmd = module.get('import')
				if import_cmd:
					json_modules[import_cmd] = module
			except Exception:
				continue

		blocks = self.get_blocks_to_build(mode='Build Mutant Tools')
		if not blocks:
			cmds.warning('No blocks found under Mutant_Build.')
			return

		updated = 0
		skipped = 0
		failed = 0

		cmds.undoInfo(openChunk=True)
		for block in blocks:
			if not cmds.objExists(block):
				skipped += 1
				continue

			connections = cmds.listConnections(block) or []
			if len(connections) < 2:
				skipped += 1
				continue

			config = connections[1]
			if not cmds.objExists(config):
				skipped += 1
				continue

			try:
				import_cmd = cmds.getAttr('{}.Import_Command'.format(config))
			except Exception:
				skipped += 1
				continue

			module = json_modules.get(import_cmd)
			if not module:
				skipped += 1
				continue

			try:
				self.update_config(block, config, module)
				updated += 1
			except Exception as e:
				print('Failed to update {}: {}'.format(block, e))
				failed += 1
		cmds.undoInfo(closeChunk=True)

		msg = 'Update All Blocks -> Updated: {} | Skipped: {} | Failed: {}'.format(updated, skipped, failed)
		print(msg)
		cmds.inViewMessage(amg=msg, pos='midCenter', fade=True)
		self.reload_ui()

	#-------------------------------------------------------------------
	def _split_help_sentences(self, help_text):
		if not help_text:
			return []
		clean_help = str(help_text).replace('\r\n', '\n').replace('\r', '\n').strip()
		if not clean_help:
			return []
		if '\n' in clean_help:
			parts = [part.strip() for part in clean_help.split('\n') if part.strip()]
			if parts:
				return parts
		return [part.strip() for part in re.split(r'(?<=[.!?])\s+', clean_help) if part.strip()]

	def _build_help_sections(self, help_text):
		sentences = self._split_help_sentences(help_text)
		overview = ''
		how_to = ''
		fields = []
		tips = []

		for sentence in sentences:
			lower_sentence = sentence.lower()
			if lower_sentence.startswith('what this block does:'):
				overview = sentence.split(':', 1)[1].strip()
			elif lower_sentence.startswith('how to use it:'):
				how_to = sentence.split(':', 1)[1].strip()
			elif lower_sentence.startswith('tip:') or lower_sentence.startswith('tips:'):
				tips.append(sentence.split(':', 1)[1].strip())
			else:
				fields.append(sentence)

		return overview, how_to, fields, tips

	def _help_html(self, help_text, compact=False):
		if not help_text:
			return '<html><body><p style="margin:0;">No help available.</p></body></html>'

		raw_help = str(help_text).strip()
		if raw_help.startswith('<') and ('</' in raw_help or '<br' in raw_help):
			return raw_help

		overview, how_to, fields, tips = self._build_help_sections(raw_help)
		if compact and len(fields) > 6:
			fields = fields[:6] + ['More options are available in the block properties panel.']

		field_items = []
		for field in fields:
			if ':' in field:
				field_name, field_value = field.split(':', 1)
				field_items.append('<li><b>{}</b>: {}</li>'.format(html.escape(field_name.strip()), html.escape(field_value.strip())))
			else:
				field_items.append('<li>{}</li>'.format(html.escape(field.strip())))

		tip_items = ['<li>{}</li>'.format(html.escape(tip.strip())) for tip in tips if tip.strip()]

		base_size = '11px' if compact else '12px'
		heading_size = '12px' if compact else '13px'

		html_parts = [
			'<html><head>',
			'<style>',
			'body { font-family: Segoe UI, Arial, sans-serif; font-size: ' + base_size + '; color: #E8E8E8; margin: 0; padding: 0; background: transparent; }',
			'.card { background: transparent; border: none; border-radius: 0; padding: 0; }',
			'.title { font-size: ' + heading_size + '; font-weight: 600; color: #9CC7FF; margin: 0 0 4px 0; }',
			'p { margin: 0 0 8px 0; }',
			'ul { margin: 0 0 8px 16px; padding: 0; }',
			'li { margin: 0 0 4px 0; }',
			'</style>',
			'</head><body><div class="card">'
		]

		if overview:
			html_parts.append('<div class="title">Overview</div><p>{}</p>'.format(html.escape(overview)))
		if how_to:
			html_parts.append('<div class="title">How To Use</div><p>{}</p>'.format(html.escape(how_to)))
		if field_items:
			html_parts.append('<div class="title">Fields</div><ul>{}</ul>'.format(''.join(field_items)))
		if tip_items:
			html_parts.append('<div class="title">Tips</div><ul>{}</ul>'.format(''.join(tip_items)))

		html_parts.append('</div></body></html>')
		return ''.join(html_parts)

	def _block_tooltip_html(self, block_data):
		name = html.escape(str(block_data.get('Name', block_data.get('name', 'Block'))))
		description = html.escape(str(block_data.get('Description', '')))
		help_text = ''
		if isinstance(block_data.get('attrs'), dict):
			help_text = block_data['attrs'].get('Help_string', '')

		if help_text:
			# Add block name as a heading above the help HTML
			help_html = self._help_html(help_text, compact=True)
			return '<html><body><p style="margin:0 0 4px 0;"><b>{}</b></p>{}</body></html>'.format(name, help_html.replace('<html><body>', '').replace('</body></html>', ''))
		# No help, show name and description
		return '<html><body><p style="margin:0 0 2px 0;"><b>{}</b></p><p style="margin:0;">{}</p></body></html>'.format(name, description)

	#-------------------------------------------------------------------
	def create_block_buttons(self):

		if mt.check_dev_mode():
			self.reload_all_blocks()

		#first we delete all the previews items on the layouts
		for i in reversed(range(self.ui.presets_layout.count())):
			self.ui.presets_layout.itemAt(i).widget().setParent(None)
		for i in reversed(range(self.ui.studio_layout.count())):
			self.ui.studio_layout.itemAt(i).widget().setParent(None)
		for i in reversed(range(self.ui.biped_layout.count())):
			self.ui.biped_layout.itemAt(i).widget().setParent(None)
		for i in reversed(range(self.ui.facial_layout.count())):
			self.ui.facial_layout.itemAt(i).widget().setParent(None)
		for i in reversed(range(self.ui.animals_layout.count())):
			self.ui.animals_layout.itemAt(i).widget().setParent(None)
		for i in reversed(range(self.ui.vehicles_layout.count())):
			self.ui.vehicles_layout.itemAt(i).widget().setParent(None)
		for i in reversed(range(self.ui.clothes_layout.count())):
			self.ui.clothes_layout.itemAt(i).widget().setParent(None)
		for i in reversed(range(self.ui.props_layout.count())):
			self.ui.props_layout.itemAt(i).widget().setParent(None)
		for i in reversed(range(self.ui.games_layout.count())):
			self.ui.games_layout.itemAt(i).widget().setParent(None)
		for i in reversed(range(self.ui.data_layout.count())):
			self.ui.data_layout.itemAt(i).widget().setParent(None)
		for i in reversed(range(self.ui.other_layout.count())):
			self.ui.other_layout.itemAt(i).widget().setParent(None)

		#'create all the buttons in the tabs blocks'
		blocks_folders = os.listdir(os.path.join(FOLDER, 'Blocks'))
		avoid_folders = ['.DS_Store', 'OldSystems']
		for block_folder in blocks_folders:
			if block_folder in avoid_folders:
				continue
			#print (block_folder)
			clean_folder_name = block_folder.split('_')[1]
			files = sorted(os.listdir(os.path.join(FOLDER, 'Blocks', block_folder)))
			have_order = False
			if 'order.json' in files:
				have_order = True

			if have_order:
				order_path = os.path.join(FOLDER, 'Blocks', block_folder, 'order.json')
				with open(order_path, "r") as order_path:
					order_data = json.load(order_path)

				files = []
				for tittle in order_data:
					files.append(tittle+'_Tittle.json')
					order_files = order_data[tittle]
					for f in order_files:
						files.append(f)

			for block_file in files:

				if not '.json' in str(block_file): #if the file != a json continue with the next one
					continue

				if 'Tittle' in block_file:
					button = QFrame()
					button.setFrameShape(QFrame.VLine)
					button.setFrameShadow(QFrame.Sunken)
					button.setToolTip(block_file.replace('_Tittle.json', ''))
					button.setFixedHeight(15)
					button.setContentsMargins(0, 0, 0, 0)

				else:
					#read the json file with block information
					real_path =  os.path.join(FOLDER, 'Blocks', block_folder,  block_file)

					with open(real_path, "r") as block_info:
						block = json.load(block_info)
						#reaload with json files info if dev mode is on, off loads faster

					#create button
					block_name = str(block_file).split('_')[1].replace('.json', '')
					button = DraggableTabButton(real_path)
					button.clicked.connect(partial (self.create_new_block, real_path))
					button.setToolTip(self._block_tooltip_html(block))
					button.setToolTipDuration(20000)
					button.setFixedSize(40, 40)


					try:
						button.setIcon(QtGui.QIcon(os.path.join(IconsPath ,block['Icon'])))
						button.setIconSize((QtCore.QSize(35, 35)))
						button.setStyleSheet("QPushButton { text-align:right; border: none; background: transparent; } QPushButton:hover { background-color: rgba(255, 255, 255, 5); border-radius: 4px; }")
						#button.setText(block_name)
					except:
						button.setText(block_name)
						button.setStyleSheet("QPushButton { border: none; background: transparent; } QPushButton:hover { background-color: rgba(255, 255, 255, 5); border-radius: 4px; }")

					if block['Enable'] == 'False':
						button.setEnabled(False)

				#parent to correct tab
				if block_folder == '000_Presets':
					self.ui.presets_layout.addWidget(button)
				elif block_folder == '001_Studio':
					self.ui.studio_layout.addWidget(button)
				elif block_folder == '002_Biped':
					self.ui.biped_layout.addWidget(button)
				elif block_folder == '003_Facial':
					self.ui.facial_layout.addWidget(button)
				elif block_folder == '004_Animals':
					self.ui.animals_layout.addWidget(button)
				elif block_folder == '005_Clothes':
					self.ui.clothes_layout.addWidget(button)
				elif block_folder == '006_Vehicles':
					self.ui.vehicles_layout.addWidget(button)
				elif block_folder == '007_Games':
					self.ui.games_layout.addWidget(button)
				elif block_folder == '008_Props':
					self.ui.props_layout.addWidget(button)
				elif block_folder == '009_Data':
					self.ui.data_layout.addWidget(button)
				else:
					self.ui.other_layout.addWidget(button)

				if not have_order:
					button.setFixedSize(42, 42)

	#-------------------------------------------------------------------
	def create_new_block(self,bock_path):

		#this will create a new block in maya based on the info on the json files
		#read json
		with open(bock_path, "r") as block_info:
			block = json.load(block_info)

		cmds.undoInfo(openChunk=True)

		# Remember which blocks exist before creation
		existing_blocks = set(self.side_block_widgets.keys())

		exec (block['import'])
		if mt.check_dev_mode():
			try:exec (block['imp.reload'])
			except: print ('couldnt imp.reload {}'.format(bock_path))
		exec (block['exec_command'])
		mt.update_icons()

		# Rebuild the entire side panel so block names come from the real
		# Maya hierarchy (some exec scripts leave the config node selected
		# instead of the block container, which was causing wrong names).
		scroll_bar = self.ui.side_scroll.verticalScrollBar()
		saved_scroll = scroll_bar.value()
		self.delete_side_buttons()
		try:
			self.create_all_side_buttons()
		except Exception as e:
			print(e)
		QtWidgets.QApplication.processEvents()
		scroll_bar.setValue(saved_scroll)
		QtCore.QTimer.singleShot(50, lambda: self.ui.side_scroll.verticalScrollBar().setValue(saved_scroll))

		# Detect the newly created block and show its properties
		new_blocks = set(self.side_block_widgets.keys()) - existing_blocks
		if new_blocks:
			new_block = list(new_blocks)[0]
			self.create_properties_layout(block=new_block, scroll_to_block=True)

		cmds.undoInfo(closeChunk=True)

	#-------------------------------------------------------------------
	def delete_side_buttons(self):

		# this will clear the side layout so we can move stuff around
		for i in reversed(range(self.ui.side_layout.count())):
			self.ui.side_layout.itemAt(i).widget().setParent(None)
		self.side_block_widgets = {}
		self.side_block_edit_buttons = {}

		self.ui.side_scroll.setWidgetResizable(True)

	def scroll_side_panel_to_block(self, block):
		if not block:
			return

		widget = self.side_block_widgets.get(block)
		if not widget:
			return

		try:
			scroll_widget = self.ui.side_scroll.widget()
			if not scroll_widget:
				return

			top_y = widget.mapTo(scroll_widget, QtCore.QPoint(0, 0)).y()
			scroll_bar = self.ui.side_scroll.verticalScrollBar()
			top_y = max(0, min(top_y, scroll_bar.maximum()))
			scroll_bar.setValue(top_y)
		except Exception:
			try:
				scroll_bar = self.ui.side_scroll.verticalScrollBar()
				scroll_bar.setValue(widget.pos().y())
			except Exception:
				pass

	def options_side_buttonblock(self, block, layout):

		from Mutant_Tools.UI.AutoRigger import load_autoRiggerOptions
		reload(load_autoRiggerOptions)
		options = load_autoRiggerOptions.AutoRiggerOptions(autorigger_ui=self, block=block, layout=layout)
		options.show()

	def _on_block_right_click(self, block, layout, pos):
		"""Triggered by right-clicking a block name button. Opens the same options popup as the gear icon."""
		self.options_side_buttonblock(block, layout)

	#-------------------------------------------------------------------

	def create_all_side_buttons(self):

		#search_data
		search_text = self.ui.search_line.text()

		cmds.select('Mutant_Build')
		sel = cmds.ls(sl=True)
		if not sel:
			build_group = 'Mutant_Build'
		else:
			build_childs = cmds.listRelatives(sel[0], ad=True)
			for child in build_childs:
				if nc['module'] in str(child):
					build_group = sel[0]
					break
				else:
					build_group = 'Mutant_Build'

		if cmds.objExists(build_group):
			self.side_block_widgets = {}
			for num, child in enumerate(cmds.listRelatives(build_group, c=True)):
				if not child.endswith(nc['module']):
					grand_childs = cmds.listRelatives(child, c=True)
					#if not childs in group pass else parent sde button to group
					if grand_childs is None:
						continue

					# When searching, find matching children first
					if search_text:
						matching = [gc for gc in grand_childs if search_text.lower() in gc.lower()]
						if not matching:
							continue
					else:
						matching = grand_childs

					colapsable_box = expandableWidget.expandableWidget(
						parent=self.ui.side_layout,
						title=child.replace('_Build', ''),
						group_box_class=DraggableBlockWidget,
						label_class=DraggableLabel,
						block_name=child
					)
					colapsable_box.exp_box.setStyleSheet('QGroupBox { margin-top: 0; padding: 0; }')
					colapsable_box.exp_box.block_dropped.connect(self.move_outliner_to_block)
					colapsable_box.exp_box.block_create_dropped.connect(self.create_block_at_position)
					self.side_block_widgets[child] = colapsable_box.exp_box

					for grand_child in matching:
						self.create_side_button(pack_name=grand_child, index=num, block_parent=colapsable_box.layout)
				else:
					if search_text:
						if search_text.lower() in child.lower():
							self.create_side_button(pack_name=child, index=num, block_parent=None)
						else:
							continue
					else:
						self.create_side_button(pack_name=child, index=num, block_parent=None)

	#-------------------------------------------------------------------
	def create_side_button(self, pack_name = 'Mutant_Block', index = 0, block_parent = None):

		#This will create all the side buttons when the up buttons are clicked

		if block_parent == None:
			block_parent = self.ui.side_layout

		side_hbox = DraggableBlockWidget(pack_name)
		side_hbox.setStyleSheet('QGroupBox { margin-top: 0; padding: 0; }')
		side_hbox.block_dropped.connect(self.move_outliner_to_block)
		side_hbox.block_create_dropped.connect(self.create_block_at_position)
		block_parent.addWidget(side_hbox)
		self.side_block_widgets[pack_name] = side_hbox

		#propierties button
		edit_button = DraggableButton(pack_name, '')
		edit_button.setFixedHeight(50)
		edit_button.setMinimumWidth(120)
		edit_button.setStyleSheet('text-align: left; padding: 2px;')
		self.side_block_edit_buttons[pack_name] = edit_button

		# Nice display name: strip _Block suffix, split camelCase, replace underscores
		display_name = pack_name.replace(nc['module'],'')
		display_name = re.sub(r'([a-z])([A-Z])', r'\1 \2', display_name)
		display_name = re.sub(r'([A-Z]+)([A-Z][a-z])', r'\1 \2', display_name)
		display_name = display_name.replace('_', ' ').strip()

		# Horizontal layout: icon on left, word-wrap label beside it
		btn_layout = QtWidgets.QHBoxLayout(edit_button)
		btn_layout.setContentsMargins(6, 2, 4, 2)
		btn_layout.setSpacing(6)

		btn_icon_label = QtWidgets.QLabel()
		btn_icon_label.setFixedSize(30, 30)
		btn_icon_label.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents)
		btn_icon_label.setStyleSheet('background: transparent;')
		try:
			icon_path = cmds.getAttr('{}.iconName'.format(pack_name))
			btn_icon_label.setPixmap(QtGui.QPixmap(icon_path).scaled(30, 30, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))
		except:
			btn_icon_label.hide()

		btn_label = QtWidgets.QLabel(display_name)
		btn_label.setWordWrap(True)
		btn_label.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
		btn_label.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents)
		btn_label.setStyleSheet('background: transparent; color: white;')

		btn_layout.addWidget(btn_icon_label)
		btn_layout.addWidget(btn_label, 1)


		options_button = QtWidgets.QPushButton()
		options_button.setFixedSize(15,15)
		options_button.setIcon(QtGui.QIcon(os.path.join(IconsPath ,'Gear.png')))
		options_button.setToolTip('Options: {}'.format(pack_name))

		h_layout = QtWidgets.QHBoxLayout()
		h_layout.setContentsMargins(4, 12, 4, -4)
		v_layout = QtWidgets.QVBoxLayout()
		v_layout.setContentsMargins(0, 0, 0, 0)

		v_layout.addWidget(options_button, 0, QtCore.Qt.AlignVCenter)
		h_layout.addLayout(v_layout)
		h_layout.setSpacing(2)
		h_layout.addWidget(edit_button, 1)

		side_hbox.setLayout(h_layout)

		edit_button.clicked.connect(partial (self.create_properties_layout, pack_name))
		options_button.clicked.connect(partial (self.options_side_buttonblock, pack_name, side_hbox))

		# Right-click on the block name button also opens the options popup
		edit_button.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
		edit_button.customContextMenuRequested.connect(partial(self._on_block_right_click, pack_name, side_hbox))

		self.update_side_block_highlight()
		self._update_block_disabled_visual(pack_name)

	def update_side_block_highlight(self):
		active_style = "QPushButton { color: #DDE2EA; border: 1px solid rgba(180, 190, 205, 90); border-radius: 3px; background-color: rgba(180, 190, 205, 20); }"
		default_style = "QPushButton { border: none; background: transparent; } QPushButton:hover { background-color: rgba(255, 255, 255, 5); border-radius: 3px; }"

		for block_name, button in self.side_block_edit_buttons.items():
			if not button:
				continue
			if self.current_block and block_name == self.current_block:
				button.setStyleSheet(active_style)
			else:
				button.setStyleSheet(default_style)

	def move_outliner_to_block(self, source_block, target_block, drop_above):
		try:
			parent = cmds.listRelatives(source_block, parent=True)
			if not parent:
				return
			parent = parent[0]
			
			children = cmds.listRelatives(parent, children=True)
			if source_block not in children or target_block not in children:
				return
			
			source_idx = children.index(source_block)
			target_idx = children.index(target_block)
			
			# Put source at front (index 0)
			cmds.reorder(source_block, front=True)
			
			current_tgt_idx = target_idx if source_idx < target_idx else target_idx + 1
			new_idx = current_tgt_idx - 1 if drop_above else current_tgt_idx
			
			if new_idx > 0:
				cmds.reorder(source_block, relative=new_idx)
				
		except Exception as e:
			cmds.warning('Could not reorder blocks: {}'.format(e))
			
		# Refresh only the side buttons, preserving scroll position
		scroll_bar = self.ui.side_scroll.verticalScrollBar()
		saved_scroll = scroll_bar.value()
		self.delete_side_buttons()
		try:
			self.create_all_side_buttons()
		except Exception as e:
			print(e)
		# Force Qt to compute the new layout so the scrollbar range is valid
		QtWidgets.QApplication.processEvents()
		scroll_bar.setValue(saved_scroll)
		# Backup: if Qt still needs another pass, restore again shortly after
		QtCore.QTimer.singleShot(50, lambda: self.ui.side_scroll.verticalScrollBar().setValue(saved_scroll))

	def create_block_at_position(self, json_path, target_block, drop_above):
		"""Create a new block from a tab drag-drop and insert it at the drop position."""
		with open(json_path, "r") as block_info:
			block = json.load(block_info)

		cmds.undoInfo(openChunk=True)
		try:
			exec(block['import'])
			if mt.check_dev_mode():
				try: exec(block['imp.reload'])
				except: print('couldnt imp.reload {}'.format(json_path))
			exec(block['exec_command'])
			mt.update_icons()

			new_block = None
			try:
				new_block = cmds.ls(sl=True)[0]
			except:
				pass

			if new_block:
				# Reorder the new block to the drop position
				try:
					target_parent = cmds.listRelatives(target_block, parent=True)
					if target_parent:
						target_parent = target_parent[0]
						curr = new_block
						while curr:
							curr_parent = cmds.listRelatives(curr, parent=True)
							if curr_parent and curr_parent[0] == target_parent:
								new_block = curr
								break
							curr = curr_parent[0] if curr_parent else None

					parent = cmds.listRelatives(new_block, parent=True)
					if parent:
						children = cmds.listRelatives(parent[0], children=True)
						if target_block in children:
							target_idx = children.index(target_block)
							# New block is at the end, move it to front first
							cmds.reorder(new_block, front=True)
							# target_idx stays the same since we moved from after it
							new_idx = target_idx if drop_above else target_idx + 1
							if new_idx > 0:
								cmds.reorder(new_block, relative=new_idx)
				except Exception as e:
					cmds.warning('Could not reorder new block: {}'.format(e))

				# Rebuild side panel to reflect correct order and show properties
				scroll_bar = self.ui.side_scroll.verticalScrollBar()
				saved_scroll = scroll_bar.value()
				self.delete_side_buttons()
				try: self.create_all_side_buttons()
				except Exception as e: print(e)
				QtWidgets.QApplication.processEvents()
				scroll_bar.setValue(saved_scroll)
				QtCore.QTimer.singleShot(50, lambda: self.ui.side_scroll.verticalScrollBar().setValue(saved_scroll))
				self.create_properties_layout(block=new_block)

		except Exception as e:
			cmds.warning('Failed to create block: {}'.format(e))

		cmds.undoInfo(closeChunk=True)

	#-------------------------------------------------------------------
	def create_properties_layout(self, block, scroll_to_block=False):
		#'Create All Properties Stuff'
		#self.create_layout()

		# this will clear the proprieties layout so we can recreate stuff
		for i in reversed(range(self.ui.properties_layout.count())):
			self.ui.properties_layout.itemAt(i).widget().setParent(None)

		#collect data for opening logs and codes
		self.current_block = block
		self.update_side_block_highlight()

		#print (block)
		current_sel = cmds.ls(sl=True) or []
		if len(current_sel) != 1 or current_sel[0] != self.current_block:
			self.ignore_next_selection_changed = True
			cmds.select(self.current_block)
		config = self._get_block_config(block)
		if not config:
			cmds.warning("Could not find configuration for block {}".format(block))
			return
		attrs =  cmds.listAttr(config , ud=True)

		#create may q box to hold the widgets
		#side_hbox = QGroupBox(block)
		side_hbox = QGroupBox()
		self.ui.block_label.setText(block)
		if scroll_to_block:
			self.scroll_side_panel_to_block(block)

		self.ui.properties_layout.addWidget(side_hbox)
		v_layout = QtWidgets.QVBoxLayout()
		side_hbox.setLayout(v_layout)

		#get all attrs inf cofig node and get type so we can create UI depending of the type of attr

		self.check_precode(block)
		self.check_postcode(block)

		self.current_block = block

		#depending of the attr type create the UI
		enable_row = QtWidgets.QHBoxLayout()
		enable_row.setContentsMargins(3, 5, 3, 5)
		enable_label = QtWidgets.QLabel('Enable Build: ')
		enable_label.setFixedHeight(30)
		enable_check = QtWidgets.QCheckBox()
		enable_check.setChecked(self.get_block_lod_visibility(block))
		enable_check.setToolTip('Uses {}.lodVisibility'.format(block))
		enable_check.stateChanged.connect(partial(self.set_block_lod_visibility, block))
		enable_row.addWidget(enable_label)
		enable_row.addWidget(enable_check)
		enable_row.addStretch()
		v_layout.addLayout(enable_row)

		# layout_separator = QtWidgets.QLabel()
		# layout_separator.setStyleSheet("border : 5px solid grey; ")
		# layout_separator.setFixedHeight(1)
		# v_layout.addWidget(layout_separator)

		for attr in attrs:

			edit_attr =  '{}.{}'.format(config, attr)

			#if the attrs is locked dont create anyting for it
			if cmds.getAttr(edit_attr,settable = True ) == False:
				continue
			#if attr is any of this continue
			skips = ['precode', 'postcode']
			if attr in skips: continue

			#main horizontal layout for each attr. they all have a label and the if is to add specific
			h_layout = QtWidgets.QHBoxLayout()
			h_layout.setContentsMargins(3, 5, 3, 5)
			#divisor
			layout_separator = QtWidgets.QLabel()
			layout_separator.setStyleSheet("border : 5px solid grey; ")
			layout_separator.setFixedHeight(1)
			v_layout.addWidget(layout_separator)
			#label
			label = QtWidgets.QLabel(attr + ': ')
			label.setFixedHeight(50)
			v_layout.addLayout(h_layout)
			h_layout.addWidget(label)

			#check Attrs type and create a layout diferente for each one
			attr_type = cmds.getAttr('{}.{}'.format(config,attr), type = True)


			#-----------------------------------------------------------------
			if attr_type == 'string':

				#Main strings attrs UI
				#print (attr + ': is string')
				line_edit = QtWidgets.QLineEdit(cmds.getAttr('{}.{}'.format(config, attr)))
				line_edit.textChanged.connect(partial(self.lineEdit_update_attr,line_edit, edit_attr))
				h_layout.addWidget(line_edit)

				if 'Set' in attr and 'List' not in attr: #if set in name it will create a greab button
					set_button = QtWidgets.QPushButton('Set Selection')
					set_button.setFixedSize(80,30)
					set_button.clicked.connect(partial(self.lineEdit_get_selection,line_edit, edit_attr))

					select_button = QtWidgets.QPushButton()
					select_button.setFixedSize(20, 20)
					select_button.setIcon(QtGui.QIcon(os.path.join(IconsPath, 'Cursor.png')))
					select_button.clicked.connect(partial(self.lineEdit_sel_selection,line_edit, edit_attr))

					h_layout.addWidget(set_button)
					h_layout.addWidget(select_button)

				if 'File' in attr:
					file_button = QtWidgets.QPushButton('Browse')
					file_button.setFixedSize(80,35)
					file_button.clicked.connect(partial(self.lineEdit_get_file,line_edit, edit_attr))
					h_layout.addWidget(file_button)

				if 'Path' in attr:
					file_button = QtWidgets.QPushButton('Browse')
					file_button.setFixedSize(80,35)
					file_button.clicked.connect(partial(self.lineEdit_get_path,line_edit, edit_attr))
					h_layout.addWidget(file_button)

				if 'List' in attr:
					line_edit.setParent(None)
					
					list_widget = QtWidgets.QListWidget()
					list_widget.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
					list_widget.setMinimumHeight(100)

					def add_item_to_list(text, lw=list_widget, at_top=False):
						item = QtWidgets.QListWidgetItem(text)
						item.setFlags(item.flags() | QtCore.Qt.ItemIsEditable)
						if at_top:
							lw.insertItem(0, item)
						else:
							lw.addItem(item)
					
					current_text = cmds.getAttr(edit_attr)
					if current_text:
						items = [i.strip() for i in current_text.split(',') if i.strip()]
						for item_text in items:
							add_item_to_list(item_text)
						
					def update_attr_from_list(lw=list_widget, ea=edit_attr):
						items = []
						for i in range(lw.count()):
							items.append(lw.item(i).text())
						cmds.setAttr(ea, ','.join(items), type='string')

					list_widget.itemChanged.connect(lambda item, lw=list_widget, ea=edit_attr: update_attr_from_list(lw, ea))
						
					def add_selected_to_list(lw=list_widget, ea=edit_attr, attr_name=attr):
						if 'Defaults' in attr_name:
							# Special: capture selected channel box attrs + values
							sel = cmds.ls(sl=True)
							if not sel:
								cmds.warning('Select objects first.')
								return
							main_attrs = cmds.channelBox('mainChannelBox', q=True, sma=True) or []
							shape_attrs = cmds.channelBox('mainChannelBox', q=True, ssa=True) or []
							history_attrs = cmds.channelBox('mainChannelBox', q=True, sha=True) or []
							output_attrs = cmds.channelBox('mainChannelBox', q=True, soa=True) or []
							all_attrs = main_attrs + shape_attrs + history_attrs + output_attrs
							if not all_attrs:
								cmds.warning('Highlight attributes in the Channel Box first.')
								return
							existing = [lw.item(i).text() for i in range(lw.count())]
							added = 0
							for node in sel:
								for cb_attr in all_attrs:
									full = '{}.{}'.format(node, cb_attr)
									if not cmds.objExists(full):
										continue
									try:
										attr_type = cmds.getAttr(full, type=True)
										if attr_type == 'enum':
											val = cmds.getAttr(full, asString=True)
										else:
											val = cmds.getAttr(full)
										entry = '{} = {}'.format(full, val)
										# Replace if same attr already stored
										replaced = False
										for idx in range(lw.count()):
											if lw.item(idx).text().startswith(full + ' ='):
												lw.takeItem(idx)
												add_item_to_list(entry, at_top=True)
												replaced = True
												break
										if not replaced:
											add_item_to_list(entry, at_top=True)
										added += 1
									except:
										pass
							if added == 0:
								cmds.warning('No valid attributes found.')
							update_attr_from_list(lw, ea)
							return
						elif 'Rename' in attr_name:
							sel = cmds.ls(sl=True)
							if not sel:
								cmds.warning('Select controls first.')
								return
							for s in sel:
								entry = '{} = {}'.format(s, s)
								replaced = False
								for idx in range(lw.count()):
									if lw.item(idx).text().startswith(s + ' ='):
										lw.takeItem(idx)
										add_item_to_list(entry, at_top=True)
										replaced = True
										break
								if not replaced:
									add_item_to_list(entry, at_top=True)
							update_attr_from_list(lw, ea)
							return
						
						sel = cmds.ls(sl=True)
						if not sel: return
						existing = []
						for i in range(lw.count()):
							existing.append(lw.item(i).text())
						for s in sel:
							if s not in existing:
								add_item_to_list(s, at_top=True)
						update_attr_from_list(lw, ea)
						
					def remove_selected_from_list(lw=list_widget, ea=edit_attr):
						selected_items = lw.selectedItems()
						if not selected_items: return
						for item in selected_items:
							lw.takeItem(lw.row(item))
						update_attr_from_list(lw, ea)
						
					def select_all_in_list(lw=list_widget):
						items = [lw.item(i).text() for i in range(lw.count())]
						# For rename lists or default lists, extract the object name part before '='
						existing = []
						for it in items:
							obj_name = it.split('=')[0].strip() if '=' in it else it
							if cmds.objExists(obj_name):
								existing.append(obj_name)
						if existing:
							cmds.select(existing)
						else:
							cmds.select(clear=True)

					def handle_paste(lw=list_widget, ea=edit_attr, attr_name=attr):
						clipboard = QtWidgets.QApplication.clipboard()
						clipboard_text = clipboard.text()
						if not clipboard_text:
							cmds.warning('Clipboard is empty.')
							return
						
						# Split text into lines
						lines = clipboard_text.split('\n')
						added = 0
						for line in lines:
							line = line.strip()
							if not line:
								continue
							
							# Try to split by tab, equals, comma, or colon
							parts = []
							if '\t' in line:
								parts = [p.strip() for p in line.split('\t') if p.strip()]
							elif '=' in line:
								parts = [p.strip() for p in line.split('=') if p.strip()]
							elif ',' in line:
								parts = [p.strip() for p in line.split(',') if p.strip()]
							elif ':' in line:
								parts = [p.strip() for p in line.split(':') if p.strip()]
							else:
								parts = [p.strip() for p in line.split() if p.strip()]
							
							if not parts:
								continue
								
							if 'Rename' in attr_name:
								if len(parts) >= 2:
									orig = parts[0]
									new_n = parts[1]
									entry = '{} = {}'.format(orig, new_n)
								else:
									orig = parts[0]
									entry = '{} = {}'.format(orig, orig)
							else:
								# For other lists, just use the first column or full line
								orig = parts[0]
								entry = line
								
							# Avoid duplicates (or replace)
							replaced = False
							# Match prefix if it has '='
							match_prefix = orig + ' =' if '=' in entry else entry
							for idx in range(lw.count()):
								if '=' in entry:
									if lw.item(idx).text().startswith(match_prefix):
										lw.item(idx).setText(entry)
										replaced = True
										break
								else:
									if lw.item(idx).text() == entry:
										replaced = True
										break
							if not replaced:
								add_item_to_list(entry)
							added += 1
							
						if added > 0:
							update_attr_from_list(lw, ea)
							print('Pasted {} entries successfully.'.format(added))

					def handle_copy(lw=list_widget):
						items = []
						for i in range(lw.count()):
							items.append(lw.item(i).text())
						text = '\n'.join(items)
						clipboard = QtWidgets.QApplication.clipboard()
						clipboard.setText(text)
						print('Copied {} entries to clipboard.'.format(lw.count()))

					def clear_list(lw=list_widget, ea=edit_attr):
						lw.clear()
						update_attr_from_list(lw, ea)
						print('List cleared successfully.')

					# Create copy and paste shortcuts on the list widget
					copy_shortcut = QtGui.QShortcut(QtGui.QKeySequence("Ctrl+C"), list_widget)
					copy_shortcut.activated.connect(lambda lw=list_widget: handle_copy(lw))

					paste_shortcut = QtGui.QShortcut(QtGui.QKeySequence("Ctrl+V"), list_widget)
					paste_shortcut.activated.connect(lambda lw=list_widget, ea=edit_attr, an=attr: handle_paste(lw, ea, an))

					list_v_layout = QtWidgets.QVBoxLayout()
					list_v_layout.addWidget(list_widget)
					
					resizer_widget = ListResizer(list_widget)
					list_v_layout.addWidget(resizer_widget)
					
					btn_h_layout = QtWidgets.QHBoxLayout()
					add_btn = QtWidgets.QPushButton('Add Selected')
					add_btn.clicked.connect(add_selected_to_list)
					remove_btn = QtWidgets.QPushButton('Remove Selected')
					remove_btn.clicked.connect(remove_selected_from_list)
					clear_btn = QtWidgets.QPushButton('Clear')
					clear_btn.setToolTip("Clear all entries from this list")
					clear_btn.clicked.connect(lambda checked=False, lw=list_widget, ea=edit_attr: clear_list(lw, ea))
					btn_h_layout.addWidget(add_btn)
					btn_h_layout.addWidget(remove_btn)
					btn_h_layout.addWidget(clear_btn)

					copy_btn = QtWidgets.QPushButton('Copy')
					copy_btn.setToolTip("Copy all list entries to clipboard")
					copy_btn.clicked.connect(lambda checked=False, lw=list_widget: handle_copy(lw))
					btn_h_layout.addWidget(copy_btn)

					paste_btn = QtWidgets.QPushButton('Paste')
					paste_btn.setToolTip("Paste entries from clipboard (supports spreadsheet columns, tab/comma/equals/colon separated values)")
					paste_btn.clicked.connect(lambda checked=False, lw=list_widget, ea=edit_attr, an=attr: handle_paste(lw, ea, an))
					btn_h_layout.addWidget(paste_btn)
					
					if 'Set' in attr:
						select_button = QtWidgets.QPushButton()
						select_button.setFixedSize(20, 20)
						select_button.setIcon(QtGui.QIcon(os.path.join(IconsPath, 'Cursor.png')))
						select_button.clicked.connect(lambda checked=False, lw=list_widget: select_all_in_list(lw))
						btn_h_layout.addWidget(select_button)

					list_v_layout.addLayout(btn_h_layout)
					
					h_layout.addLayout(list_v_layout)

				if attr == 'Code':  # if code in name it will create a larger box
					line_edit.setParent(None)
					h_layout.removeWidget(label)
					code_v_layout = QtWidgets.QVBoxLayout()
					label.setFixedHeight(25)
					label.setStyleSheet("font-weight: bold; color: #9CC7FF;")
					code_v_layout.addWidget(label)
					code_editor = codeEditorWidget.IDECodeEditor(max_height_limit=None)
					code_editor.setPlainText(cmds.getAttr('{}.{}'.format(config, attr)))
					code_editor.set_language('python')
					code_editor.textChanged.connect(partial(self.lineEdit_update_attr, code_editor, edit_attr))
					# Restore saved code block height if available
					if cmds.optionVar(ex='mutant_code_block_height'):
						saved_h = cmds.optionVar(q='mutant_code_block_height')
						if saved_h > 50:
							code_editor.setFixedHeight(saved_h)
					code_v_layout.addWidget(code_editor)
					resizer_widget = ListResizer(code_editor)
					code_v_layout.addWidget(resizer_widget)
					h_layout.addLayout(code_v_layout)

				if attr == 'Help':  # if non string do a code box but non editable
					line_edit.setParent(None)
					help_browser = QtWidgets.QTextBrowser()
					help_browser.setOpenExternalLinks(True)
					help_browser.setReadOnly(True)
					help_browser.setMinimumHeight(180)
					help_browser.setFrameShape(QtWidgets.QFrame.NoFrame)
					help_browser.setHtml(self._help_html(cmds.getAttr('{}.{}'.format(config, attr))))
					h_layout.addWidget(help_browser)

			#-----------------------------------------------------------------
			elif attr_type == 'enum':
				#get all the options in the config combo box and add them to a custom qt cumbo box
				#print (attr + ': is enum')
				enums = cmds.attributeQuery(attr, node=config, listEnum = True)[0]
				enums = str(enums).split(':')
				#print (enums)
				enum_box = QtWidgets.QComboBox()
				enum_box.addItems(enums)
				enum_box.setCurrentIndex(cmds.getAttr(edit_attr))
				enum_box.setStyleSheet('background-color: none;')
				enum_box.currentIndexChanged.connect(partial(self.enum_update_attr,enum_box,edit_attr))

				h_layout.addWidget(enum_box)

			#-----------------------------------------------------------------
			elif attr_type == 'long':
				#print (attr + ': is long')

				int_label = QtWidgets.QLabel(str(cmds.getAttr(edit_attr)))
				int_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
				int_slider.setValue(cmds.getAttr(edit_attr))
				if cmds.getAttr(edit_attr) > 20:
					int_slider.setMaximum(100)
				else:
					int_slider.setMaximum(20)
				int_slider.setStyleSheet('background-color: none;')
				int_slider.valueChanged.connect(partial(self.slider_update_attr, int_label, int_slider, edit_attr))

				h_layout.addWidget(int_label)
				h_layout.addWidget(int_slider)

			#-----------------------------------------------------------------
			elif attr_type == 'bool':
				#print (attr + ': is bool')
				checkbox = QtWidgets.QCheckBox(attr)
				checkbox.setChecked(cmds.getAttr('{}.{}'.format(config, attr)))
				checkbox.setStyleSheet('background-color: none;')
				h_layout.addWidget(checkbox)
				label.setParent(None)
				checkbox.stateChanged.connect(partial(self.checkBox_update_attr, checkbox, edit_attr))
			#-----------------------------------------------------------------


	#-------------------------------------------------------------------

	def delete_properties_layout(self):
		# this will clear the side layout so we can move stuff around
		for i in reversed(range(self.ui.properties_layout.count())):
			self.ui.properties_layout.itemAt(i).widget().setParent(None)
		#make UI Scrolable
		self.ui.properties_scroll.setWidgetResizable(True)

	#-------------------------------------------------------------------
	def lineEdit_update_attr(self, field, attr,*args):
		try:#simple line edits
			cmds.setAttr(attr, field.text(), type = 'string')
		except:#code plain Texts
			cmds.setAttr(attr, field.toPlainText(), type = 'string')

	def lineEdit_get_selection(self, field, attr,*args):
		attr_name = attr.split('.')[-1] if '.' in attr else attr
		if 'Flat' in attr_name:
			sel = cmds.ls(sl=True, fl=True)
		else:
			sel = cmds.ls(sl=True)
		print(sel)
		#remove ugly lists keys
		nice_selection = str(sel)[1:-1]
		nice_selection = nice_selection.replace("u'", "'")
		nice_selection = nice_selection.replace("'", "")

		field.setText(nice_selection)
		cmds.setAttr(attr, nice_selection, type = 'string')

	def lineEdit_sel_selection(self, field, attr,*args):
		value = field.text()
		attr = cmds.getAttr(attr)

		if value == attr:
			print(attr)

		if ',' in value:
			value = value.split(',')

		try:
			cmds.select(value)
		except:
			cmds.warning('Selection doesnt exists')

	def lineEdit_get_file(self, field, attr, *args):
		path = mh.import_window(extension=".json")[0]
		field.setText(path)
		cmds.setAttr(attr, path, type='string')

	def lineEdit_get_path(self, field, attr, *args):
		path = mh.folder_window()
		field.setText(path)
		cmds.setAttr(attr, path, type='string')

	def slider_update_attr(self, label, slider,attr, *args):
		if slider.value() == 20:
			self.update_max_slider(slider, attr)
		cmds.setAttr(attr, slider.value())
		label.setText(str(slider.value()))

	def update_max_slider(self, slider, attr):
		print('updating value')
		cmds.addAttr(attr, edit=True, max=100)
		slider.setMaximum(100)


	def checkBox_update_attr(self, checkBox,attr, *args):
		cmds.setAttr(attr, checkBox.isChecked())

	def enum_update_attr(self, comboBox, attr, *args):
		cmds.setAttr(attr, comboBox.currentIndex())

	#-------------------------------------------------------------------
	def get_block_lod_visibility(self, block):
		attr = '{}.lodVisibility'.format(block)
		if cmds.objExists(attr):
			try:
				return bool(cmds.getAttr(attr))
			except:
				return True
		return True

	def set_block_lod_visibility(self, block, state, *args):
		attr = '{}.lodVisibility'.format(block)
		if cmds.objExists(attr):
			try:
				cmds.setAttr(attr, bool(state))
			except Exception as e:
				print('Could not set {}: {}'.format(attr, e))
		self._update_block_disabled_visual(block)

	def _update_block_disabled_visual(self, block):
		"""Dim the side-panel widget for a block when its build is disabled."""
		widget = self.side_block_widgets.get(block)
		if not widget:
			return
		enabled = self.get_block_lod_visibility(block)
		effect = widget.graphicsEffect()
		if enabled:
			widget.setGraphicsEffect(None)
		else:
			opacity = QtWidgets.QGraphicsOpacityEffect(widget)
			opacity.setOpacity(0.35)
			widget.setGraphicsEffect(opacity)

	def is_valid_block(self, block):
		if not block or not cmds.objExists(block):
			return False
		if not block.endswith(nc['module']):
			return False
		# Must have a config node connected
		conns = cmds.listConnections(block, type='network') or []
		if conns:
			return True
		# Fallback general check
		all_conns = cmds.listConnections(block) or []
		return len(all_conns) >= 2

	def _get_block_config(self, block):
		if not block or not cmds.objExists(block):
			return None
		conns = cmds.listConnections(block, type='network') or []
		if conns:
			return conns[0]
		all_conns = cmds.listConnections(block) or []
		if len(all_conns) >= 2:
			return all_conns[1]
		if len(all_conns) == 1:
			return all_conns[0]
		return None

	#-------------------------------------------------------------------

	def get_blocks_to_build(self, mode='Build Mutant Tools'):

		print(mode)

		to_build = []
		blocks = []

		if mode == 'Build Mutant Tools':
			if not cmds.objExists('Mutant_Build'):
				cmds.warning("Mutant_Build group does not exist in the scene.")
				return []
			blocks = cmds.listRelatives('Mutant_Build', c=True) or []
		elif mode == 'Build Selected Group':
			sel = cmds.ls(sl=True)
			if not sel:
				cmds.warning("Nothing selected for group build.")
				return []
			grp = sel[0]
			if not cmds.objExists(grp):
				return []
			blocks = cmds.listRelatives(grp, c=True) or []
		elif mode == 'Build Selected Block':
			blocks = cmds.ls(sl=True) or []

		for block in blocks:
			if self.is_valid_block(block):
				if self.get_block_lod_visibility(block):
					to_build.append(block)
				else:
					print('Skipped disabled block:', block)
			else:
				# If not a valid block itself, check if it's a group node containing blocks
				children = cmds.listRelatives(block, c=True) or []
				for child in children:
					if self.is_valid_block(child):
						if self.get_block_lod_visibility(child):
							to_build.append(child)
						else:
							print('Skipped disabled block:', child)

		return to_build

	def build_autorigger(self, only_progressbar=False):
		cmds.undoInfo(openChunk=True)
		build_failed = False
		failed_block = 'Unknown'
		is_skin_block = False

		try:
			self.ui.bar_label.resize(100, 200)
			self.ui.bar_label.setText('Starting the Build')

			# Get blocks to build early so we can run pre-build blocks before EVERYTHING
			blocks = self.get_blocks_to_build(mode = self.ui.build_method.currentText())

			# Collect and run pre-build blocks (RunBeforeBuild) before any plugins, rebuild cleanups, or IO
			before_code_blocks = []
			for block in blocks:
				try:
					block_config = self._get_block_config(block)
					if block_config and cmds.attributeQuery('RunBeforeBuild', n=block_config, exists=True):
						if cmds.getAttr('{}.RunBeforeBuild'.format(block_config)):
							before_code_blocks.append(block)
				except:
					pass

			if before_code_blocks:
				print('------------------------------------------------------------------------------------')
				print('Running {} pre-build block(s) before EVERYTHING...'.format(len(before_code_blocks)))
				print('------------------------------------------------------------------------------------')
				for before_block in before_code_blocks:
					failed_block = before_block + ' (Pre-Build)'
					print('Running pre-build: {}'.format(before_block))
					self.ui.bar_label.setText('Pre-Build: {}'.format(before_block))
					cmds.select(before_block)
					before_config = self._get_block_config(before_block)
					if not before_config:
						cmds.warning("Could not find configuration for pre-build block {}. Skipping.".format(before_block))
						continue
					
					# Generic block builder execution: call the block's Build_Command with force=True
					executed = False
					build_cmd = None
					if cmds.attributeQuery('Build_Command', n=before_config, exists=True):
						build_cmd = cmds.getAttr('{}.Build_Command'.format(before_config), asString=True)
					
					if build_cmd:
						build_cmd_force = build_cmd.replace('()', '(force=True)') if '()' in build_cmd else build_cmd
						
						# Ensure module is imported
						import_cmd = None
						if cmds.attributeQuery('Import_Command', n=before_config, exists=True):
							import_cmd = cmds.getAttr('{}.Import_Command'.format(before_config), asString=True)
						if import_cmd:
							try:
								exec(import_cmd)
								reload_cmd = import_cmd.replace('import ', 'reload(') + ')'
								exec(reload_cmd)
							except:
								pass
						
						try:
							eval(build_cmd_force)
							executed = True
						except Exception as e:
							print('Could not execute pre-build block via build command: {}. Error: {}. Falling back to default legacy execution.'.format(build_cmd_force, e))
					
					if not executed:
						# Legacy fallback for custom Code blocks
						before_pl = cmds.getAttr('{}.Exec'.format(before_config), asString=True)
						before_code = cmds.getAttr('{}.Code'.format(before_config), asString=True)
						if before_pl != 'Python':
							mel.eval(before_code)
						else:
							exec(before_code)
					print('Pre-build block {} completed'.format(before_block))

			#Load need plugins
			self.force_load_of_dependency_plugins()

			#Check rebuild
			rebuild = self.check_if_previous_build()
			if not rebuild:
				return False

			if rebuild == 'First Build':
				load_io = False
			elif rebuild == 'Just Rebuild':
				load_io = False
			else:
				load_io = True
			#log
			try:
				clear_se = cmds.optionVar(q="mutant_clear_script_editor") if cmds.optionVar(ex="mutant_clear_script_editor") else True
				if clear_se:
					cmds.scriptEditorInfo(ch=True)
				mt.Mutant_logger(mode = 'clear')
				mt.Mutant_logger(mode = 'stop')
			except:
				pass

			#build
			cmds.optionVar(iv=("mutant_ensure_mirror", 0))  # Reset ensure-mirror flag before build
			blocks = self.get_blocks_to_build(mode = self.ui.build_method.currentText())
			progress_max = len(blocks)
			self.ui.progressBar.setMaximum(progress_max)
			if only_progressbar:
				from Mutant_Tools.UI.ProgressBar import load_progress_bar
				reload(load_progress_bar)
				cProgressBarUI = load_progress_bar.ProgressBarUI(items=blocks,
																 title='Building Mutant...')
				cProgressBarUI.show()

			#collect deferred code blocks to run after the entire build + IO completes
			deferred_code_blocks = []

			#select each block and run the build command and make progress bar move
			for num, block in enumerate(blocks):
				failed_block = block
				is_skin_block = 'skin' in block.lower()

				if is_skin_block and not cmds.about(batch=True):
					mel.eval("paneLayout -e -manage false $gMainPane")

				if not is_skin_block:
					visual_build_enabled = cmds.optionVar(q="mutant_visual_build") if cmds.optionVar(ex="mutant_visual_build") else True
					if visual_build_enabled:
						#just for fun
						cmds.refresh()

				#log
				mt.Mutant_logger(mode = 'create')
				print ('------------------------------------------------------------------------------------')
				print ('------------------------------------------------------------------------------------')
				print ('Building: {}'.format(block))
				print ('------------------------------------------------------------------------------------')
				print ('------------------------------------------------------------------------------------')

				self.ui.bar_label.setText('Building: {}'.format(block))
				self.ui.bar_label.setToolTip('Building: {}'.format(block))

				#building
				cmds.select(block)
				config = self._get_block_config(block)
				if not config:
					cmds.warning("Could not find configuration for block {}. Skipping.".format(block))
					continue
				precode = cmds.getAttr('{}.precode'.format(config))
				import_command = cmds.getAttr('{}.Import_Command'.format(config))
				reload_command = import_command.replace('import', 'reload(')+')'.replace(' ', '')
				buid_command = cmds.getAttr('{}.Build_Command'.format(config))
				postcode = cmds.getAttr('{}.postcode'.format(config))

				self.ui.bar_label.setText(buid_command)
				self.ui.bar_label.setToolTip(buid_command)

				exec(import_command)
				exec(reload_command)
				print ('Import successfully {}'.format(import_command))
				pre_build_nodes = self.get_all_nodes()
				
				if only_progressbar:
					cProgressBarUI.set_percent(num)
				# ----------------------
				# Precode---------------
				# ----------------------
				cmds.select(block)
				print('Precode {}'.format(block))

				# Skip precode/postcode for blocks that defer execution
				skip_pre_post = False
				if cmds.attributeQuery('RunAfterBuild', n=config, exists=True) and cmds.getAttr('{}.RunAfterBuild'.format(config)):
					skip_pre_post = True
				if cmds.attributeQuery('RunBeforeBuild', n=config, exists=True) and cmds.getAttr('{}.RunBeforeBuild'.format(config)):
					skip_pre_post = True

				if precode:
					if skip_pre_post:
						print('Skipping precode for deferred block {}'.format(block))
					else:
						try:
							exec(precode)
						except:
							mel.eval(precode)

				# ----------------------
				# BUILD-----------------
				# ----------------------
				cmds.select(block)
				#Build the blocks
				recipe_obj = None
				recipe_obj = eval(buid_command)
				recipe_name = block.replace(nc['module'],'')
				add_on = {recipe_name:recipe_obj}
				self.recipes_dict.update(add_on)

				print('Build successfully {}'.format(buid_command))
				# ----------------------
				# Postcode--------------
				# ----------------------
				cmds.select(block)
				print('Postcode {}'.format(block))
				if postcode:
					if skip_pre_post:
						print('Skipping postcode for deferred block {}'.format(block))
					else:
						try:
							exec(postcode)
						except:
							mel.eval(postcode)

				post_build_nodes = self.get_all_nodes()

				#check if this is a deferred code block
				try:
					block_config = self._get_block_config(block)
					if block_config and cmds.attributeQuery('RunAfterBuild', n=block_config, exists=True):
						if cmds.getAttr('{}.RunAfterBuild'.format(block_config)):
							deferred_code_blocks.append(block)
				except:
					pass

				#succes message
				self.ui.bar_label.setText('{}'.format(block))
				self.ui.bar_label.setToolTip('Succesfull build: {}'.format(block))
				self.ui.progressBar.setValue((num + 1))

				#log
				mt.Mutant_logger(mode = 'stop')

				#Stop Block
				if block == 'Stop_Block':
					print ('User Stop')
					return

				#put build nodes only in notes
				if not cmds.attributeQuery("notes", n=block, ex=True):
					cmds.addAttr(block, ln="notes", sn="nts", dt="string")
				nodes_dif = self.get_diference_in_nodes(pre_build_nodes, post_build_nodes)
				cmds.setAttr("{}.notes".format(block), nodes_dif, type="string")

				if is_skin_block and not cmds.about(batch=True):
					mel.eval("paneLayout -e -manage true $gMainPane")

			if only_progressbar:
				cProgressBarUI.close()

			#all success message
			print('Mutant Build Complete')
			self.ui.bar_label.setText('Mutant Build Complete')
			self.ui.bar_label.setToolTip('Mutant Build Complete')

			cmds.setAttr('Mutant_Build.v', 0)
			if cmds.objExists('Mutant_Rig'):
				cmds.parent('Mutant_Rig', 'Miscellaneous_Grp')

			#IO
			if load_io:
				if not cmds.about(batch=True):
					mel.eval("paneLayout -e -manage false $gMainPane")
				try:
					ctrls.load_all(path=os.path.join(tempfile.gettempdir(), 'RebuildTempCtrls', 'tempControllers.json'))
					self._load_rebuild_skins(temp_skin_folder=os.path.join(tempfile.gettempdir(), 'RebuildTempSkin'))
					self._reorder_loaded_skin_deformers()
					# Load parent hierarchy
					temp_folder = os.path.join(tempfile.gettempdir(), 'RebuildTemp')
					skeleton_file = os.path.join(temp_folder, 'skeleton_hierarchy.txt')
					if cmds.objExists('Skeleton'):
						self.load_joint_parents("Skeleton", skeleton_file)
				finally:
					if not cmds.about(batch=True):
						mel.eval("paneLayout -e -manage true $gMainPane")

			#Run deferred blocks (RunAfterBuild) as the very last step (post-build procedures)
			if deferred_code_blocks:
				print('------------------------------------------------------------------------------------')
				print('Running {} deferred block(s)...'.format(len(deferred_code_blocks)))
				print('------------------------------------------------------------------------------------')
				for deferred_block in deferred_code_blocks:
					failed_block = deferred_block + ' (Deferred)'
					print('Running deferred: {}'.format(deferred_block))
					self.ui.bar_label.setText('Deferred: {}'.format(deferred_block))
					cmds.select(deferred_block)
					deferred_config = self._get_block_config(deferred_block)
					if not deferred_config:
						cmds.warning("Could not find configuration for deferred block {}. Skipping.".format(deferred_block))
						continue
					
					# Generic block builder execution: call the block's Build_Command with force=True
					executed = False
					build_cmd = None
					if cmds.attributeQuery('Build_Command', n=deferred_config, exists=True):
						build_cmd = cmds.getAttr('{}.Build_Command'.format(deferred_config), asString=True)
					
					if build_cmd:
						build_cmd_force = build_cmd.replace('()', '(force=True)') if '()' in build_cmd else build_cmd
						
						# Ensure module is imported
						import_cmd = None
						if cmds.attributeQuery('Import_Command', n=deferred_config, exists=True):
							import_cmd = cmds.getAttr('{}.Import_Command'.format(deferred_config), asString=True)
						if import_cmd:
							try:
								exec(import_cmd)
								reload_cmd = import_cmd.replace('import ', 'reload(') + ')'
								exec(reload_cmd)
							except:
								pass
						
						try:
							eval(build_cmd_force)
							executed = True
						except Exception as e:
							print('Could not execute deferred block via build command: {}. Error: {}. Falling back to default legacy execution.'.format(build_cmd_force, e))
					
					if not executed:
						# Legacy fallback for custom Code blocks
						deferred_pl = cmds.getAttr('{}.Exec'.format(deferred_config), asString=True)
						deferred_code = cmds.getAttr('{}.Code'.format(deferred_config), asString=True)
						if deferred_pl != 'Python':
							mel.eval(deferred_code)
						else:
							exec(deferred_code)
					print('Deferred block {} completed'.format(deferred_block))

		except Exception:
			import traceback
			traceback.print_exc()
			build_failed = True

		finally:
			cmds.undoInfo(closeChunk=True)
			if build_failed:
				mt.Mutant_logger(mode='stop')
				
				revert_on_fail = cmds.optionVar(q="mutant_revert_on_fail") if cmds.optionVar(ex="mutant_revert_on_fail") else True
				if revert_on_fail:
					cmds.warning('Build failed on "{}". Reverting to pre-build state...'.format(failed_block))
					import maya.utils
					maya.utils.executeDeferred('import maya.cmds as cmds; cmds.undo()')
				else:
					cmds.warning('Build failed on "{}". Revert on Fail is disabled, scene left as-is.'.format(failed_block))
				
				self.view_log()
				
				if only_progressbar and 'cProgressBarUI' in locals():
					cProgressBarUI.close()
				if 'is_skin_block' in locals() and is_skin_block and not cmds.about(batch=True):
					mel.eval("paneLayout -e -manage true $gMainPane")
	def save_joint_parents(self, group_name, file_path):
		"""
        Save the parent hierarchy of joints under the specified group to a file.
        :param group_name: Name of the group containing the joints.
        :param file_path: File path to save the parent hierarchy information.
        """
		joints = cmds.listRelatives(group_name, ad=True, type='joint') or []
		parent_dict = {}

		for joint in joints:
			parent = cmds.listRelatives(joint, parent=True)
			if parent:
				parent_dict[joint] = parent[0]

		with open(file_path, 'w') as file:
			for joint, parent in parent_dict.items():
				file.write(f"{joint},{parent}\n")

	def load_joint_parents(self, group_name, file_path):
		"""
        Load the parent hierarchy of joints from the provided file and apply to the joints under the specified group.
        :param group_name: Name of the group containing the joints.
        :param file_path: File path containing the parent hierarchy information.
        """
		with open(file_path, 'r') as file:
			parent_dict = {}
			for line in file:
				joint, parent = line.strip().split(',')
				parent_dict[joint] = parent

		for joint, parent in parent_dict.items():
			if cmds.objExists(joint) and cmds.objExists(parent):
				try:
					cmds.parent(joint, parent)
				except:
					pass

	def _get_rebuild_skinned_geos(self):
		skin_clusters = cmds.ls(type='skinCluster') or []
		skinned_geos = []

		for skin_cluster in skin_clusters:
			geo_shapes = cmds.skinCluster(skin_cluster, q=True, g=True) or []
			for geo_shape in geo_shapes:
				geo_shape = str(geo_shape).split('.')[0]
				if not cmds.objExists(geo_shape):
					continue

				if cmds.nodeType(geo_shape) == 'mesh':
					parents = cmds.listRelatives(geo_shape, p=True, f=True) or []
					geo_node = parents[0] if parents else geo_shape
				else:
					geo_node = geo_shape

				if geo_node not in skinned_geos:
					skinned_geos.append(geo_node)

		return skinned_geos

	def _rebuild_skin_mode_file(self, temp_skin_folder):
		return os.path.join(temp_skin_folder, 'tempSkinMode.txt')

	def _set_rebuild_skin_mode(self, temp_skin_folder, mode):
		mode_file = self._rebuild_skin_mode_file(temp_skin_folder)
		try:
			with open(mode_file, 'w') as mode_handle:
				mode_handle.write(mode)
		except Exception as e:
			cmds.warning('Could not cache rebuild skin mode ({}).'.format(e))

	def _get_rebuild_skin_mode(self, temp_skin_folder):
		mode_file = self._rebuild_skin_mode_file(temp_skin_folder)
		if not os.path.exists(mode_file):
			return 'fast'

		try:
			with open(mode_file, 'r') as mode_handle:
				mode = mode_handle.read().strip()
				if mode in ['fast', 'easy']:
					return mode
		except Exception:
			pass

		return 'fast'

	def _save_rebuild_skins(self, temp_skin_folder):
		use_fast = cmds.optionVar(q="mutant_use_fast_skin") if cmds.optionVar(ex="mutant_use_fast_skin") else True

		if use_fast:
			self._set_rebuild_skin_mode(temp_skin_folder=temp_skin_folder, mode='easy')
			EasySkin.save_all_skins_to(folder_path=temp_skin_folder)
		else:
			temp_skin_pack = os.path.join(temp_skin_folder, 'tempSkinPack.bSkinPack')
			try:
				from Mutant_Tools.Utils.IO import IOSkin
				reload(Mutant_Tools.Utils.IO.IOSkin)
				import pymel.core as pm

				skinned_geos = self._get_rebuild_skinned_geos()
				if not skinned_geos:
					cmds.warning('No skinned geometries found for IOSkin rebuild export.')
					self._set_rebuild_skin_mode(temp_skin_folder=temp_skin_folder, mode='easy')
					EasySkin.save_all_skins_to(folder_path=temp_skin_folder)
					return

				pm_geos = [pm.PyNode(geo) for geo in skinned_geos if cmds.objExists(geo)]
				IOSkin.exportSkinPack(packPath=temp_skin_pack, objs=pm_geos)
				if not os.path.exists(temp_skin_pack):
					raise IOError('Skin pack not created: {}'.format(temp_skin_pack))

				self._set_rebuild_skin_mode(temp_skin_folder=temp_skin_folder, mode='fast')
				print('IOSkin rebuild skin pack saved: {}'.format(temp_skin_pack))
			except Exception as e:
				import traceback
				traceback.print_exc()
				cmds.warning('IOSkin save unavailable ({}). Falling back to Fast Skin.'.format(e))
				self._set_rebuild_skin_mode(temp_skin_folder=temp_skin_folder, mode='easy')
				EasySkin.save_all_skins_to(folder_path=temp_skin_folder)

	def _load_rebuild_skins(self, temp_skin_folder):
		temp_skin_pack = os.path.join(temp_skin_folder, 'tempSkinPack.bSkinPack')
		skin_mode = self._get_rebuild_skin_mode(temp_skin_folder=temp_skin_folder)

		if skin_mode == 'easy':
			EasySkin.load_all_skins_from(folder_path=temp_skin_folder)
			return

		try:
			if not os.path.exists(temp_skin_pack):
				raise IOError('Skin pack not found: {}'.format(temp_skin_pack))

			from Mutant_Tools.Utils.IO import IOSkin
			reload(Mutant_Tools.Utils.IO.IOSkin)
			IOSkin.importSkinPack(filePath=temp_skin_pack)
			print('Fast rebuild skin pack loaded: {}'.format(temp_skin_pack))
		except Exception as e:
			cmds.warning('Fast rebuild skin load unavailable ({}). Falling back to EasySkin.'.format(e))
			EasySkin.load_all_skins_from(folder_path=temp_skin_folder)

	def _reorder_loaded_skin_deformers(self):
		skinned_geos = self._get_rebuild_skinned_geos()
		if not skinned_geos:
			return

		reordered = 0
		for geo in skinned_geos:
			try:
				history = cmds.listHistory(geo, pruneDagObjects=True) or []
				blend_nodes = [h for h in history if cmds.nodeType(h) == 'blendShape']
				skin_nodes = [h for h in history if cmds.nodeType(h) == 'skinCluster']
				delta_nodes = [h for h in history if cmds.nodeType(h) == 'deltaMush']

				blend = blend_nodes[0] if blend_nodes else None
				skin = skin_nodes[0] if skin_nodes else None
				delta = delta_nodes[0] if delta_nodes else None

				if skin and delta:
					cmds.reorderDeformers(delta, skin, geo)

				if blend and delta:
					cmds.reorderDeformers(delta, blend, geo)

				if blend and skin:
					cmds.reorderDeformers(skin, blend, geo)

				if blend or skin or delta:
					reordered += 1
			except Exception as e:
				cmds.warning('Could not reorder deformers on {} ({}).'.format(geo, e))

		if reordered:
			print('Reordered deformers on {} skinned geos (blendShape -> skinCluster -> deltaMush).'.format(reordered))

	#-------------------------------------------------------------------

	def get_all_nodes(self):
		return cmds.ls('*')

	def get_diference_in_nodes(self, new_list, old_list):
		dif = set(old_list).difference(set(new_list))
		return dif

	def check_if_previous_build(self):

		build_grp = 'Mutant_Tools_Grp'
		if cmds.objExists(build_grp):
			delete_comfirm = cmds.confirmDialog(
				title='Delete current build?',
				message='Are you sure you want to rebuild?',
				button=['Delete and Rebuild', 'Just Rebuild', 'Cancel'],
				defaultButton='Delete and Rebuild',
				dismissString='Cancel',
				cancelButton='Cancel')

			if delete_comfirm == 'Delete and Rebuild':

				if cmds.listRelatives('Mutant_Build', p=True):
					cmds.parent('Mutant_Build', w=True)

				#IO

				# Skeleton Hierarchy
				if cmds.objExists('Skeleton'):
					temp_folder = os.path.join(tempfile.gettempdir(), 'RebuildTemp')
					if not os.path.exists(temp_folder):
						os.mkdir(temp_folder)
					skeleton_file = os.path.join(temp_folder, 'skeleton_hierarchy.txt')
					# Save parent hierarchy to file
					self.save_joint_parents("Skeleton", skeleton_file)

				# Orient Values
				try:
					import json
					scene_name = cmds.file(q=True, sceneName=True)
					safe_scene = os.path.basename(scene_name).replace('.ma', '').replace('.mb', '') if scene_name else "untitled"
					
					temp_folder = os.path.join(tempfile.gettempdir(), 'RebuildTemp')
					if not os.path.exists(temp_folder):
						os.mkdir(temp_folder)
					
					orient_file = os.path.join(temp_folder, '{}_orient_values.json'.format(safe_scene))
					orient_data = {}
					for orient in cmds.ls('*_Orient', type='transform'):
						orient_data[orient] = {
							't': cmds.getAttr('{}.t'.format(orient))[0],
							'r': cmds.getAttr('{}.r'.format(orient))[0],
							's': cmds.getAttr('{}.s'.format(orient))[0]
						}
					with open(orient_file, 'w') as f:
						json.dump(orient_data, f)
				except Exception as e:
					print("Failed to save orient values:", e)


				# Controllers
				temp_controllers_folder = os.path.join(tempfile.gettempdir(), 'RebuildTempCtrls')
				if not os.path.exists(temp_controllers_folder):
					os.mkdir(temp_controllers_folder)
				ctrls.save_all(folder_path=os.path.join(temp_controllers_folder, 'tempControllers.json'),
							   force_validate=True)

				#Skins
				temp_skin_folder = os.path.join(tempfile.gettempdir(), 'RebuildTempSkin')
				if not os.path.exists(temp_skin_folder):
					os.mkdir(temp_skin_folder)
				else:
					try:
						import shutil
						shutil.rmtree(temp_skin_folder)
						print('Deleted: ', temp_skin_folder)
					except:
						pass
				if not os.path.exists(temp_skin_folder):
					os.mkdir(temp_skin_folder)
				self._save_rebuild_skins(temp_skin_folder=temp_skin_folder)

				#Delete
				cmds.delete(build_grp)
				if cmds.objExists('Mutant_Rig'):
					cmds.delete('Mutant_Rig')

				return temp_skin_folder, temp_controllers_folder

			elif delete_comfirm == 'Just Rebuild':
				return 'Just Rebuild'

			else:
				return False
		else:
			return 'First Build'


	#-------------------------------------------------------------------
	def check_precode(self, block):

		config = self._get_block_config(block)
		if not config:
			return

		# Precode and Postcode attrs Code
		if cmds.getAttr('{}.precode'.format(config)) != '':
			self.ui.prebuild.setIcon(QtGui.QIcon(os.path.join(IconsPath ,'PRECODE_ON.png')))
		else:
			self.ui.prebuild.setIcon(QtGui.QIcon(os.path.join(IconsPath ,'PRECODE.png')))

	#-------------------------------------------------------------------
	def check_postcode(self, block):

		config = self._get_block_config(block)
		if not config:
			return

		# Precode and Postcode attrs Code
		if cmds.getAttr('{}.postcode'.format(config)) != '':
			self.ui.postbuild.setIcon(QtGui.QIcon(os.path.join(IconsPath ,'POSTCODE_ON.png')))
		else:
			self.ui.postbuild.setIcon(QtGui.QIcon(os.path.join(IconsPath ,'POSTCODE.png')))

	#-------------------------------------------------------------------

	def edit_prebuild_code(self, block):

		config = self._get_block_config(block)
		if not config:
			return

		#get past code
		pastcode_attr = cmds.getAttr('{}.precode'.format(config))

		try:
			codeUI.close()
		except:
			pass
		reload(load_codeReader)
		codeUI = load_codeReader.Code_Reader(mode='write', code= pastcode_attr, config_attr = '{}.precode'.format(config))
		codeUI.set_path_label(code_path = '{}.precode'.format(config))
		codeUI.show()

	#-------------------------------------------------------------------

	def view_build_code(self, block):

		config = self._get_block_config(block)
		if not config:
			return

		import_command = cmds.getAttr('{}.Import_Command'.format(config))
		build_file = import_command.replace('import ', '')

		current_path = os.path.join(FOLDER, 'Blocks')
		script_name = build_file + '.py'

		# if we need find it first
		for root, dirs, files in os.walk(current_path):
			for name in files:
				if name == script_name:
					file_path = os.path.abspath(os.path.join(root, name))

		with open(file_path) as build_data:
			build_script = build_data.read()

		try:
			codeUI.close()
		except:
			pass
		reload(load_codeReader)
		codeUI = load_codeReader.Code_Reader(mode='view', code= build_script, config_attr = '')
		codeUI.set_path_label(code_path = file_path)
		codeUI.show()
	#-------------------------------------------------

	def edit_postbuild_code(self, block):
		config = self._get_block_config(block)
		if not config:
			return

		#get past code
		postcode_attr = cmds.getAttr('{}.postcode'.format(config))

		try:
			codeUI.close()
		except:
			pass

		reload(load_codeReader)
		codeUI = load_codeReader.Code_Reader(mode='write', code= postcode_attr, config_attr = '{}.postcode'.format(config))
		codeUI.set_path_label(code_path = '{}.postcode'.format(config))
		codeUI.show()
	#-------------------------------------------------------------------

	def view_log(self):

		log_file = mt.Mutant_logger(mode = 'log')
		with open(log_file) as log_data:
			log = log_data.read()

		#log
		try:
			log_ui.close()
		except:
			pass

		print(log)

		reload(load_codeReader)
		log_ui = load_codeReader.Code_Reader(mode='view', code='', config_attr='')
		log_ui.previous_code = log
		log_ui.modify_ui_based_on_mode()
		log_ui.ui.code_text.verticalScrollBar().setValue(log_ui.ui.code_text.verticalScrollBar().maximum())
		log_ui.set_path_label(code_path = os.path.join(cmds.internalVar(usd=True),'Mutant_log.txt'))
		log_ui.show()

	#-------------------------------------------------------------------

	def search_command(self):
		self.delete_side_buttons()
		self.create_all_side_buttons()

	def _focus_search(self):
		"""Show the floating search overlay, unless the code editor has focus."""
		focused = QtWidgets.QApplication.focusWidget()
		if focused and hasattr(focused, 'show_search_replace'):
			focused.show_search_replace()
			return

		if not hasattr(self, '_search_overlay'):
			self._search_overlay = SearchOverlay(self.master_ui, self.ui.search_line)
		self._search_overlay.popup()

	def show_bar_only(self):
		self.ui.menuLayout.setParent(None)
		self.ui.tabs.setParent(None)
		self.ui.side_scroll.setParent(None)
		self.ui.attrs_layout.setParent(None)
		self.ui.code_layout.setParent(None)
		self.ui.build_layout.setParent(None)
		self.ui.build_btn.setParent(None)
		self.ui.build_method.setParent(None)
		self.ui.search_layout.setParent(None)
		self.adjustSize()    
		self.show()

	#-------------------------------------------------------------------

	# CLOSE EVENTS _________________________________
	def closeEvent(self, event):

		#delete the script job created for the loading of the UI
		try:
			cmds.scriptJob(kill=self.mutant_sj)
			print ('ScripJob deleted')
			#cmds.scriptJob(ka=1)
		except:
			pass

		print ('Mutant_Tools Autorigger Closed')
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

print('''
#Import Menu
import Mutant_Tools
import Mutant_Tools.Utils
from Mutant_Tools.Utils import mt_menu
reload(Mutant_Tools.Utils.mt_menu)
mt_menu.create_mutant_menu()
mt_menu.put_in_userSetup()

#Import Main Mutant Tools
import imp
from imp import reload
import Mutant_Tools
import Mutant_Tools.Utils
from Mutant_Tools.Utils.Rigging import main_mutant
reload(Mutant_Tools.Utils.Rigging.main_mutant)
mt = main_mutant.Mutant()
''')
