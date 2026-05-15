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

class DraggableBlockWidget(QtWidgets.QGroupBox):
	block_dropped = QtCore.Signal(str, str, bool)

	def __init__(self, block_name, *args, **kwargs):
		super(DraggableBlockWidget, self).__init__(*args, **kwargs)
		self.block_name = block_name
		self.setAcceptDrops(True)
		self.setFocusPolicy(QtCore.Qt.NoFocus)
		self._drop_indicator = None

	def dragEnterEvent(self, event):
		if event.mimeData().hasText():
			source_block = event.mimeData().text()
			if source_block != self.block_name:
				event.acceptProposedAction()
				return
		event.ignore()

	def dragMoveEvent(self, event):
		if event.mimeData().hasText():
			source_block = event.mimeData().text()
			if source_block != self.block_name:
				drop_above = event.pos().y() < (self.height() / 2)
				new_indicator = 'top' if drop_above else 'bottom'
				if self._drop_indicator != new_indicator:
					self._drop_indicator = new_indicator
					self.update()
				event.acceptProposedAction()
				return
		event.ignore()

	def dragLeaveEvent(self, event):
		if self._drop_indicator is not None:
			self._drop_indicator = None
			self.update()
		event.accept()

	def dropEvent(self, event):
		self._drop_indicator = None
		self.update()
		source_block = event.mimeData().text()
		drop_above = event.pos().y() < (self.height() / 2)
		self.block_dropped.emit(source_block, self.block_name, drop_above)
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
			self.target.setMinimumHeight(new_h)
	def mouseReleaseEvent(self, event):
		self._is_resizing = False

class AutoRigger(QtMutantWindow.Qt_Mutant):

	def __init__(self):
		super(AutoRigger, self).__init__()

		#UI Init
		self.setWindowTitle(Title)
		self.set_title(Title)

		self.create_menu()

		self.resize(605, 652)

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

		h_splitter = QtWidgets.QSplitter(QtCore.Qt.Horizontal)
		h_splitter.addWidget(self.ui.side_scroll)
		h_splitter.addWidget(right_widget)
		h_splitter.setStretchFactor(0, 0)
		h_splitter.setStretchFactor(1, 1)
		h_splitter.setSizes([200, 400])
		h_splitter.setHandleWidth(5)

		# --- Vertical splitter: tabs on top | h_splitter on bottom ---
		# Find the tabs and the grid that holds the blocks/properties
		tabs_widget = self.ui.tabs
		# Remove tabs max height so it can shrink
		tabs_widget.setMaximumHeight(16777215)

		# Remove the menuLayout_3 wrapper around tabs so we can reparent it
		menu_layout_3 = self.ui.findChild(QtWidgets.QVBoxLayout, 'menuLayout_3')

		v_splitter = QtWidgets.QSplitter(QtCore.Qt.Vertical)
		v_splitter.addWidget(tabs_widget)
		v_splitter.addWidget(h_splitter)
		v_splitter.setStretchFactor(0, 0)
		v_splitter.setStretchFactor(1, 1)
		# Start with tabs compact (just enough for 2 rows of icons ~120px)
		v_splitter.setSizes([120, 500])
		v_splitter.setHandleWidth(5)

		splitter_style = 'QSplitter::handle { background-color: #3a3a3a; }'
		h_splitter.setStyleSheet(splitter_style)
		v_splitter.setStyleSheet(splitter_style)

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
		main_layout.addWidget(v_splitter, 1, 0)

		self._splitter_installed = True

	def _convert_tab_layouts_to_flow(self):
		"""Replace each tab's QHBoxLayout with a FlowLayout so buttons wrap."""
		if hasattr(self, '_flow_installed'):
			return
		self._flow_installed = True

		# Map layout name -> attribute name on self.ui
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

			# Move any existing widgets from the old layout
			widgets = []
			while old_layout.count():
				child = old_layout.takeAt(0)
				if child.widget():
					widgets.append(child.widget())

			# Clear everything from the parent grid (old layout + spacers)
			while parent_layout.count():
				child = parent_layout.takeAt(0)
				if child.widget():
					child.widget().deleteLater()

			# Create a new FlowLayout and add it as the sole item
			flow = FlowLayout(spacing=4)
			if isinstance(parent_layout, QtWidgets.QGridLayout):
				parent_layout.addLayout(flow, 0, 0)
			else:
				parent_layout.addLayout(flow)

			for w in widgets:
				flow.addWidget(w)

			# Point the attribute to the new flow layout
			setattr(self.ui, name, flow)

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

		# Setup resizable splitters and wrapping block buttons
		self._setup_splitter()
		self._convert_tab_layouts_to_flow()

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

		try:
			if 'string' in attr_key:
				cmds.setAttr(attr_path, str(value), type='string')
			elif 'enum' in attr_key:
				enums = cmds.attributeQuery(attr, node=config, listEnum=True)
				if enums:
					enum_values = enums[0].split(':')
					if isinstance(value, str) and value in enum_values:
						cmds.setAttr(attr_path, enum_values.index(value))
					elif isinstance(value, int):
						cmds.setAttr(attr_path, value)
			elif 'float' in attr_key:
				cmds.setAttr(attr_path, int(value))
			elif 'bool' in attr_key:
				cmds.setAttr(attr_path, bool(value))
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

		for attr in attrs_in_config:
			if attr in skips:
				continue
			clean_attr = self.get_mutant_config_attr(attr, config)
			if clean_attr not in attrs_in_json:
				if cmds.attributeQuery(attr, node=config, exists=True):
					cmds.deleteAttr('{}.{}'.format(config, attr))
			else:
				attrs_to_recreate.append(attr)
				existing_values[clean_attr] = self.get_config_attr_value(config=config, attr=attr, attr_key=clean_attr)

		for attr in attrs_to_recreate:
			if cmds.attributeQuery(attr, node=config, exists=True):
				cmds.deleteAttr('{}.{}'.format(config, attr))

		for attr in attrs_in_json:
			attr_name = attr.split('_')[0]
			if 'string' in attr:
				mt.string_attr(input=config, name=attr_name, string=module['attrs'][attr])
			elif 'enum' in attr:
				mt.new_enum(input=config, name=attr_name, enums=module['attrs'][attr])
			elif 'float' in attr:
				mt.new_attr_interger(input=config, name=attr_name, min=1, max=20, default=int(module['attrs'][attr]))
			elif 'bool' in attr:
				mt.new_boolean(input=config, name=attr_name, dv=module['attrs'][attr])

			value_to_set = module['attrs'][attr]
			if attr in existing_values:
				value_to_set = existing_values[attr]

			self.set_config_attr_value(config=config, attr=attr_name, attr_key=attr, value=value_to_set)

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
					button = QPushButton()#give a nicer name
					button.clicked.connect(partial (self.create_new_block, real_path))
					button.clicked.connect(self.create_layout)
					button.setToolTip(self._block_tooltip_html(block))
					button.setToolTipDuration(20000)
					button.setFixedSize(40, 40)


					try:
						button.setIcon(QtGui.QIcon(os.path.join(IconsPath ,block['Icon'])))
						button.setIconSize((QtCore.QSize(35, 35)))
						button.setStyleSheet("text-align:right;")
						#button.setText(block_name)
					except:
						button.setText(block_name)

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

		exec (block['import'])
		if mt.check_dev_mode():
			try:exec (block['imp.reload'])
			except: print ('couldnt imp.reload {}'.format(bock_path))
		exec (block['exec_command'])
		mt.update_icons()
		self.create_properties_layout(block = cmds.ls(sl=True)[0])

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

					colapsable_box = expandableWidget.expandableWidget(parent=self.ui.side_layout, title=child.replace('_Build', ''))
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
		block_parent.addWidget(side_hbox)
		self.side_block_widgets[pack_name] = side_hbox

		#propierties button
		edit_button = DraggableButton(pack_name, '')
		edit_button.setFixedHeight(50)
		edit_button.setMinimumWidth(120)
		edit_button.setStyleSheet('text-align: left; padding: 2px;')
		self.side_block_edit_buttons[pack_name] = edit_button

		# Nice display name: strip _Block suffix and replace underscores with spaces
		display_name = pack_name.replace(nc['module'],'').replace('_', ' ').strip()

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

	def update_side_block_highlight(self):
		active_style = "QPushButton { color: #DDE2EA; border: 1px solid rgba(180, 190, 205, 90); border-radius: 3px; background-color: rgba(180, 190, 205, 20); }"
		default_style = ""

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
			
		# Refresh the UI layout
		self.create_layout()

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
		config = cmds.listConnections(block)[1]
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
					
					current_text = cmds.getAttr(edit_attr)
					if current_text:
						items = [i.strip() for i in current_text.split(',') if i.strip()]
						list_widget.addItems(items)
						
					def update_attr_from_list(lw=list_widget, ea=edit_attr):
						items = []
						for i in range(lw.count()):
							items.append(lw.item(i).text())
						cmds.setAttr(ea, ','.join(items), type='string')
						
					def add_selected_to_list(lw=list_widget, ea=edit_attr):
						sel = cmds.ls(sl=True)
						if not sel: return
						existing = []
						for i in range(lw.count()):
							existing.append(lw.item(i).text())
						for s in sel:
							if s not in existing:
								lw.addItem(s)
						update_attr_from_list(lw, ea)
						
					def remove_selected_from_list(lw=list_widget, ea=edit_attr):
						selected_items = lw.selectedItems()
						if not selected_items: return
						for item in selected_items:
							lw.takeItem(lw.row(item))
						update_attr_from_list(lw, ea)
						
					def select_all_in_list(lw=list_widget):
						items = [lw.item(i).text() for i in range(lw.count())]
						existing = [i for i in items if cmds.objExists(i)]
						if existing:
							cmds.select(existing)
						else:
							cmds.select(clear=True)

					list_v_layout = QtWidgets.QVBoxLayout()
					list_v_layout.addWidget(list_widget)
					
					resizer_widget = ListResizer(list_widget)
					list_v_layout.addWidget(resizer_widget)
					
					btn_h_layout = QtWidgets.QHBoxLayout()
					add_btn = QtWidgets.QPushButton('Add Selected')
					add_btn.clicked.connect(add_selected_to_list)
					remove_btn = QtWidgets.QPushButton('Remove Selected')
					remove_btn.clicked.connect(remove_selected_from_list)
					btn_h_layout.addWidget(add_btn)
					btn_h_layout.addWidget(remove_btn)
					
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
					code_editor = codeEditorWidget.IDECodeEditor()
					code_editor.setPlainText(cmds.getAttr('{}.{}'.format(config, attr)))
					code_editor.set_language('python')
					code_editor.textChanged.connect(partial(self.lineEdit_update_attr, code_editor, edit_attr))
					h_layout.addWidget(code_editor)

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

	#-------------------------------------------------------------------

	def get_blocks_to_build(self, mode='Build Mutant Tools'):

		print(mode)

		to_build = []

		if mode == 'Build Mutant Tools':
			blocks = cmds.listRelatives('Mutant_Build', c=True)
		elif mode == 'Build Selected Group':
			grp = cmds.ls(sl=True)[0]
			blocks = cmds.listRelatives(grp, c=True)
		elif mode == 'Build Selected Block':
			blocks = cmds.ls(sl=True)

		for block in blocks:
			if not block.endswith(nc['module']):
				grand_childs = cmds.listRelatives(block, c=True)
				if not grand_childs:
					continue
				for grand_child in grand_childs:
					if self.get_block_lod_visibility(grand_child):
						to_build.append(grand_child)
					else:
						print('Skipped disabled block:', grand_child)
			else:
				if self.get_block_lod_visibility(block):
					to_build.append(block)
				else:
					print('Skipped disabled block:', block)

		return to_build

	def build_autorigger(self, only_progressbar=False):
		cmds.undoInfo(openChunk=True)
		build_failed = False
		failed_block = 'Unknown'
		is_skin_block = False

		try:
			self.ui.bar_label.resize(100, 200)
			self.ui.bar_label.setText('Starting the Build')

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
				config = cmds.listConnections(block)[1]
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
				if precode:
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
					try:
						exec(postcode)
					except:
						mel.eval(postcode)

				post_build_nodes = self.get_all_nodes()

				#check if this is a deferred code block
				try:
					block_config = cmds.listConnections(block)[1]
					if cmds.attributeQuery('RunAfterBuild', n=block_config, exists=True):
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

			#Run deferred code blocks (RunAfterBuild) as the very last step
			if deferred_code_blocks:
				print('------------------------------------------------------------------------------------')
				print('Running {} deferred Code block(s)...'.format(len(deferred_code_blocks)))
				print('------------------------------------------------------------------------------------')
				for deferred_block in deferred_code_blocks:
					failed_block = deferred_block + ' (Deferred)'
					print('Running deferred: {}'.format(deferred_block))
					self.ui.bar_label.setText('Deferred: {}'.format(deferred_block))
					cmds.select(deferred_block)
					deferred_config = cmds.listConnections(deferred_block)[1]
					deferred_pl = cmds.getAttr('{}.Exec'.format(deferred_config), asString=True)
					deferred_code = cmds.getAttr('{}.Code'.format(deferred_config), asString=True)
					if deferred_pl != 'Python':
						mel.eval(deferred_code)
					else:
						exec(deferred_code)
					print('Deferred code block {} completed'.format(deferred_block))

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

		config = cmds.listConnections(block)[1]

		# Precode and Postcode attrs Code
		if cmds.getAttr('{}.precode'.format(config)) != '':
			self.ui.prebuild.setIcon(QtGui.QIcon(os.path.join(IconsPath ,'PRECODE_ON.png')))
		else:
			self.ui.prebuild.setIcon(QtGui.QIcon(os.path.join(IconsPath ,'PRECODE.png')))

	#-------------------------------------------------------------------
	def check_postcode(self, block):

		config = cmds.listConnections(block)[1]

		# Precode and Postcode attrs Code
		if cmds.getAttr('{}.postcode'.format(config)) != '':
			self.ui.postbuild.setIcon(QtGui.QIcon(os.path.join(IconsPath ,'POSTCODE_ON.png')))
		else:
			self.ui.postbuild.setIcon(QtGui.QIcon(os.path.join(IconsPath ,'POSTCODE.png')))

	#-------------------------------------------------------------------

	def edit_prebuild_code(self, block):

		config = cmds.listConnections(block)[1]

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

		config = cmds.listConnections(block)[1]

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
		config = cmds.listConnections(block)[1]

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

