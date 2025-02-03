from __future__ import absolute_import
'''
version: 1.0.0
date: 21/04/2020

#----------------
content:

This will create a UI for the autorriger menu tool.

#----------------
how to:

import Mutant_Tools
from Mutant_Tools.UI.RigTools.Tabs import load_SkinTab
reload(load_SkinTab)

try:cSkin_ui.close()
except:pass
cSkin_ui = load_SkinTab.SkinTab()
cSkin_ui.show()

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
# -------------------------------------------------------------------
from shiboken2 import wrapInstance
from PySide2 import QtGui, QtCore
from PySide2 import QtUiTools
from PySide2 import QtWidgets
from PySide2.QtWidgets import *
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin
from builtins import round

import maya.OpenMaya as OpenMaya
import maya.OpenMayaUI as omui
from functools import partial
# import pymel.core as pm
import maya.cmds as cmds
import maya.mel as mel
from pathlib import Path

import os
try:
    import importlib;from importlib import reload
except:
    import imp;from imp import reload

import sys
import json
import glob
import collections

try:from urllib.request import Request, urlopen
except:pass

import Mutant_Tools
from Mutant_Tools.UI.WebsiteViewer import load_website_viewer
reload(load_website_viewer)
viewer = load_website_viewer.WebsiteViewerUI()

from Mutant_Tools.Utils.Helpers import helpers
reload(Mutant_Tools.Utils.Helpers.helpers)
mh = helpers.Helpers()

from Mutant_Tools.Utils.IO import SkinUtils
reload(Mutant_Tools.Utils.IO.SkinUtils)
skin = SkinUtils.Skinning()

from Mutant_Tools.Utils.IO import NgSkinUtils
reload(Mutant_Tools.Utils.IO.NgSkinUtils)
ngmt = NgSkinUtils.NG_Mutant()

from Mutant_Tools.Utils.IO import CtrlUtils
reload(Mutant_Tools.Utils.IO.CtrlUtils)
ctrls = CtrlUtils.Ctrls()

from Mutant_Tools.Utils.IO import Guides
reload(Mutant_Tools.Utils.IO.Guides)
guides = Guides.Guides()

import Mutant_Tools.Utils.Helpers
from Mutant_Tools.Utils.Helpers import helpers
reload(Mutant_Tools.Utils.Helpers.helpers)
mh = helpers.Helpers()

from Mutant_Tools.Utils.IO import SkinUtils
reload(SkinUtils)
ms = SkinUtils.Skinning()

import Mutant_Tools
import Mutant_Tools.Utils
from Mutant_Tools.Utils.Rigging import main_mutant

reload(Mutant_Tools.Utils.Rigging.main_mutant)
mt = main_mutant.Mutant()
# -------------------------------------------------------------------

#Read name conventions as nc[''] and setup as setup['']
PATH = os.path.dirname(__file__)
PATH = Path(PATH)
PATH_PARTS = PATH.parts[:-3]
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

# -------------------------------------------------------------------

#QT WIndow!
PATH = os.path.dirname(__file__)
PATH = Path(PATH)
PATH_PARTS = PATH.parts[:-3]
FOLDER=''
for p in PATH_PARTS:
	FOLDER = os.path.join(FOLDER, p)
PATH = os.path.join(FOLDER, 'UI')

ICONS_FOLDER = os.path.join(FOLDER,'Icons')

Title = 'Skin-Tab'
UI_File = 'Skin.ui'



# -------------------------------------------------------------------

def maya_main_window():
	main_window_ptr = omui.MQtUtil.mainWindow()
	return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)

class SkinTab(QtWidgets.QDialog):

	def __init__(self, parent=maya_main_window()):
		super(SkinTab, self).__init__(parent)

		self.setWindowTitle(Title)

		self.shows = ['Sandbox', 'AnythingGoes', 'SP']
		self.assests_by_type = []

		self.init_ui()
		self.create_layout()
		self.create_connections()

		try:
			self.populate_assets_type()
			self.populate_from_sid_note()
		except Exception as e:
			cmds.warning(e)

	def init_ui(self):
		UIPath = os.path.join(FOLDER,'UI','RigTools','Tabs',UI_File)
		f = QtCore.QFile(os.path.join(UIPath))
		f.open(QtCore.QFile.ReadOnly)

		loader = QtUiTools.QUiLoader()
		self.ui = loader.load(f, parentWidget=self)

		f.close()

	# -------------------------------------------------------------------

	def create_layout(self):
		self.curveWidget = self.populate_ui_curve(self.ui.curveEditorLyt)
		self.ui.shows_combo.addItems(self.shows)
		self.ui.null_check.setChecked(True)

	# -------------------------------------------------------------------

	def create_connections(self):

		self.ui.meshNameLoadBtn.clicked.connect(lambda:self.ui.meshNameLoadField.setText(str(cmds.ls(sl=True)[0])))
		self.ui.mirrorBox.setChecked(True)
		self.sidesGrp= QtWidgets.QButtonGroup(self)
		self.sidesGrp.addButton(self.ui.defaultBox)
		self.sidesGrp.addButton(self.ui.strongCenterBox)
		self.sidesGrp.addButton(self.ui.bigFallBox)
		self.sidesGrp.addButton(self.ui.customBox)
		self.ui.customField.setText("0,1,2,1,0,2")
		self.ui.falloffValueLabel.setText("35")
		self.ui.expandValueLabel.setText("4")
		self.ui.defaultBox.setChecked(True)
		curve_values = {'Curve_Editor': self.curveWidget.convert_UI_data(), 'Strong_Center':"0,1,2,1,0,2", 'Big_Falloff': "0.80303,0,1,0,0.506024,1", "Custom": self.ui.customField.text()}
		self.ui.falloffSlider.valueChanged.connect(lambda:self.ui.falloffValueLabel.setText(str(self.ui.falloffSlider.value())))
		self.ui.expandSlider.valueChanged.connect(lambda:self.ui.expandValueLabel.setText(str(self.ui.expandSlider.value())))
		self.ui.softSelectBtn.clicked.connect(lambda: ms.soft_select_skin_pass(
														mirror=self.ui.mirrorBox.isChecked(),
														expand=0,
														curve=curve_values[self.sidesGrp.checkedButton().text()],
														falloff=float('.'+self.ui.falloffValueLabel.text()),
														mesh=self.ui.meshNameLoadField.text(),
														joint_dict=cmds.ls(sl=True)))
		self.ui.growSelectBtn.clicked.connect(lambda: ms.soft_select_skin_pass(
														mirror=self.ui.mirrorBox.isChecked(),
														expand=int(self.ui.expandValueLabel.text()),
														falloff=0,
														mesh=self.ui.meshNameLoadField.text(),
														joint_dict=cmds.ls(sl=True)))
		self.ui.combinedBtn.clicked.connect(lambda: ms.soft_select_skin_pass(
														mirror=self.ui.mirrorBox.isChecked(),
														expand=int(self.ui.expandValueLabel.text()),
														curve=curve_values[self.sidesGrp.checkedButton().text()],
														falloff=float('.'+self.ui.falloffValueLabel.text()),
														mesh=self.ui.meshNameLoadField.text(),
														joint_dict=cmds.ls(sl=True)))
		self.ui.combinedBtn.clicked.connect(lambda:self.curveWidget.convert_UI_data())

		self.ui.dualquatnonriging_btn.clicked.connect(self.makes_dual_quaternion_non_rigids)
		self.ui.deltascale_btn.clicked.connect(self.connect_deltas_to_global_ctrl)
		self.ui.offskin_btn.clicked.connect(self.turn_off_skins)
		self.ui.on_skins.clicked.connect(self.turn_on_skins)

		self.ui.load_button.clicked.connect(self.list_assests_by_type)
		self.ui.shows_combo.currentIndexChanged.connect(self.populate_assets_type)
		self.ui.assets_type_combo.currentIndexChanged.connect(self.populate_assets)
		self.ui.version_load_button.clicked.connect(self.populate_versions)
		self.ui.versions_combo.currentIndexChanged.connect(self.populate_skin_versions)
		self.ui.skin_versions_combo.currentIndexChanged.connect(self.populate_geos)

		self.ui.load_skin_button.clicked.connect(self.load_skin)

		self.ui.ref_copy_btn.clicked.connect(lambda: self.reference_and_copy(version_path=None, geos=[], mode = 'HelloThere'))
		self.ui.ref_copy_uv_btn.clicked.connect(lambda: self.reference_and_copy(version_path=None, geos=[], mode = 'UV'))

		self.ui.save_skin_button.clicked.connect(self.save_skin)
		self.ui.select_bind_jnts.clicked.connect(lambda: self.select_bind_joints(mesh=self.ui.meshNameLoadField.text(),
												 		 null_jnt_check=self.ui.null_check.isChecked()))

		self.ui.copy_skin_to_nurb.clicked.connect(lambda: self.copy_skin_nurb(geo=cmds.ls(sl=True)[0],
																			  nurb=cmds.ls(sl=True)[1]))
		self.ui.click_copy_button.clicked.connect(self.click_copy)
	# -------------------------------------------------------------------

	def populate_ui_curve(self, layout):
		""" Create Curve Graph Editor

		Args:
			layout: where to put the shelf in the qt ui from designer

		Returns: None

		"""
		bezier = Bezier()
		layout.addWidget(bezier)
		layout.setAlignment(QtCore.Qt.AlignHCenter)
		# layout.setAlignment(QtCore.Qt.AlignVCenter)
		return bezier

	# -------------------------------------------------------------------
	def makes_dual_quaternion_non_rigids(self):
		scs = cmds.ls(type='skinCluster')
		if not scs:
			return
		for skin in scs:
			cmds.setAttr(skin + '.skinningMethod', 1)
			cmds.setAttr(skin + '.dqsSupportNonRigid', 1)

	# -------------------------------------------------------------------
	def connect_deltas_to_global_ctrl(self):
		deltas = cmds.ls(type='deltaMush')
		if not deltas:
			return
		for dm in deltas:
			cmds.connectAttr('Global_Ctrl.rigScale', dm + '.scale.scaleX')
			cmds.connectAttr('Global_Ctrl.rigScale', dm + '.scale.scaleY')
			cmds.connectAttr('Global_Ctrl.rigScale', dm + '.scale.scaleZ')

	# -------------------------------------------------------------------
	def turn_off_skins(self):
		scs = cmds.ls(type='skinCluster')
		if not scs:
			return
		for skin in scs:
			cmds.skinCluster(skin, edit=True, mjm=False)

	def turn_on_skins(self):
		scs = cmds.ls(type='skinCluster')
		if not scs:
			return
		for skin in scs:
			cmds.skinCluster(skin, edit=True, mjm=True)

	# -------------------------------------------------------------------
	def populate_from_sid_note(self):
		from rigSystem.assetTemplates.core import (get_one_sid, validate_sid)
		try:
			sid = get_one_sid()
			sid = validate_sid(sid)
			show,asset = sid.breadcrumb.split('/')
			asset_type = sid.type

			self.ui.shows_combo.setCurrentText(show)
			self.ui.assets_type_combo.setCurrentText(asset_type)
			self.ui.assets_combo.setCurrentText(asset)

			self.populate_versions()
		except:
			pass

	# -------------------------------------------------------------------

	def list_assests_by_type(self):
		from star.entities import Project

		project_name = self.ui.shows_combo.currentText()
		proj = Project.findby_name(project_name)

		types = []
		assets_by_types = {}

		for ass in proj.assets:
			if ass.type in types:
				continue
			else:
				types.append(ass.type)
				assets_by_types[ass.type] = []

		for ass in proj.assets:
			updated_list = assets_by_types[ass.type]
			updated_list.append(ass.name)
			assets_by_types[ass.type] = updated_list

		self.assets_by_types = assets_by_types
		return assets_by_types

	# -------------------------------------------------------------------

	def populate_assets_type(self):

		self.ui.assets_type_combo.clear()

		self.list_assests_by_type()

		list_assests_by_type = self.assets_by_types
		asset_types = []
		for type in list_assests_by_type:
			if type == 'char':
				asset_types.insert(0, type)
			else:
				asset_types.append(type)

		self.ui.assets_type_combo.addItems(asset_types)

	# -------------------------------------------------------------------

	def populate_assets(self):

		self.ui.assets_combo.clear()

		list_assests_by_type = self.assets_by_types
		current_type = self.ui.assets_type_combo.currentText()
		if not current_type:
			return
		assets = list_assests_by_type[current_type]

		self.ui.assets_combo.addItems(assets)

	# -------------------------------------------------------------------

	def clear_geos(self):
		self.ui.versions_combo.clear()
		self.ui.skin_versions_combo.clear()
		self.ui.geos_combo.clear()

	# -------------------------------------------------------------------
	def populate_versions(self):

		self.ui.versions_combo.clear()

		from star.entities import Project

		asset = self.ui.assets_combo.currentText()
		asset_type = self.ui.assets_type_combo.currentText()
		show = self.ui.shows_combo.currentText()

		proj = Project.findby_name(show)
		for ass in proj.assets:
			if asset == str(ass.name):
				root = ass.wip_root

		versions_path = root + '/rigging/*/maya/scenes/*'
		versions = glob.glob(versions_path)
		versions.sort(key=os.path.getmtime)

		versions_with_skinning = []
		for version in versions:
			#see if it have skinning
			skinning_path = version.split('scenes')[0]
			skinning_files = glob.glob(skinning_path+'/data/*Skin*json')
			if not skinning_files:
				continue
			#order in the dict
			versions_with_skinning.append(version)

		if not versions_with_skinning:
			self.ui.versions_combo.addItems(['None'])


		versions_with_skinning = reversed(versions_with_skinning)
		self.ui.versions_combo.addItems(versions_with_skinning)

	# -------------------------------------------------------------------

	def populate_skin_versions(self):

		self.ui.skin_versions_combo.clear()

		skinning_path = self.ui.versions_combo.currentText()
		if skinning_path == 'None':
			self.ui.skin_versions_combo.addItems(['None'])
			return

		skinning_files = glob.glob(skinning_path.split('scenes')[0] + '/data/*Skin*json')
		skinning_files.sort(key=os.path.getmtime)
		skinning_files=reversed(skinning_files)
		self.ui.skin_versions_combo.addItems(skinning_files)


	# -------------------------------------------------------------------


	def populate_geos(self):

		self.ui.geos_combo.clear()

		file_version = self.ui.skin_versions_combo.currentText()
		if file_version == 'None':
			self.ui.geos_combo.addItems(['None'])
			return

		self.ui.geos_combo.addItems(['Everything'])

		from rigSystem.utils.io.core import IO
		skin_data = IO.read_json(file_version)

		geos = []
		for geo in skin_data:
			geos.append(geo)

		self.ui.geos_combo.addItems(geos)

	# -------------------------------------------------------------------

	def load_skin(self):
		from rigSystem.utils.io.core import IO
		from rigSystem.utils.io import skin

		warnings = []

		skin_file = self.ui.skin_versions_combo.currentText()
		geo = self.ui.geos_combo.currentText()
		if skin_file == 'None':
			return

		skin_data = IO.read_json(skin_file)
		print('Loading {} in {}').format(geo, skin_file)

		if geo != 'Everything':
			geo = geo
			print('Loading {}'.format(geo))
			skin.load(skin_data, geo)
			return True
		else:
			all_geos = [self.ui.geos_combo.itemText(i) for i in range(self.ui.geos_combo.count())]
			for geo in all_geos:
				print('Loading {}'.format(geo))
				try:
					skin.load(skin_data,  geo)
				except Exception as e:
					print(e)
					warnings.append(e)

		cmds.confirmDialog(warnings)
		import pprint
		pprint.pprint(warnings)

	# -------------------------------------------------------------------

	def reference_and_copy(self, version_path=None, geos=[], mode = 'UV'):
		if not version_path:
			version_path = self.ui.versions_combo.currentText()

		if not geos:
			geos = [self.ui.geos_combo.itemText(i) for i in range(self.ui.geos_combo.count())]

		cmds.file(version_path, ignoreVersion=True, namespace='SkinningRef',
									mergeNamespacesOnClash=False, r=True)

		if not geos:
			cmds.error('We Need geos to copy skin')

		error_messages = []
		for geo in geos:
			if cmds.objExists(geo):
				if cmds.objExists('SkinningRef:'+geo):
					cmds.select('SkinningRef:'+geo, geo)
					try:
						if mode == 'UV':
							mel.eval('copySkinWeights  -noMirror -surfaceAssociation closestPoint -uvSpace map1 map1 -influenceAssociation oneToOne -influenceAssociation label -normalize;')
						else:
							mel.eval('copySkinWeights  -noMirror -surfaceAssociation closestPoint -influenceAssociation oneToOne -influenceAssociation label -normalize;')
					except Exception as E:
						error_messages.append(E)

				else:
					error_messages.append('SkinningRef:'+geo + ' Doesnt Exists')
			else:
				error_messages.append(geo + ' Doesnt Exists')

		fname = cmds.referenceQuery('SkinningRef:Global_Ctrl', filename=True)
		cmds.file(fname, rr=True)

		import pprint
		pprint.pprint(error_messages)

	# -------------------------------------------------------------------

	def save_skin(self):
		from rigSystem.utils.io import skin
		import os
		from rigSystem.utils.io.core import IO
		from rstar.nodes.skinCluster import SkinCluster as Skin
		from rigSystem.assetTemplates import Character
		from rigSystem.assetTemplates.core import (get_one_sid, validate_sid)

		skin_clusters = Skin.find()

		sid = get_one_sid()
		sid = validate_sid(sid)

		data = skin.save()

		version = sid.version
		name = str(sid) + '_SkinCluster_V0'
		path = os.path.join(cmds.workspace(rd=True, q=True) + 'data', '{}{}.json'.format(name, version))

		while os.path.exists(path):
			version = version + 1
			path = os.path.join(cmds.workspace(rd=True, q=True) + 'data', '{}{}.json'.format(name, version + 1))

		IO.write_json(path, data)
		print(path)

	# -------------------------------------------------------------------

	def select_bind_joints(self, mesh=None, null_jnt_check=None):

		if mesh == '':
			mesh = cmds.ls(sl=True)[0]

		jnts = cmds.skinCluster(mesh, inf=True, q=True)
		
		if null_jnt_check == True:
			if cmds.objExists("Null_Local_Bnd"):
				jnts.remove("Null_Local_Bnd")
			else:
				cmds.warning("Null_Local_Bnd doesn't exist")

		return cmds.select(jnts)

	# -------------------------------------------------------------------

	def copy_skin_nurb(self, geo=None, nurb=None):
    
		#get spans values of nurb
		spans_u = cmds.getAttr('{0}.spansU'.format(nurb))
		spans_v = cmds.getAttr('{0}.spansV'.format(nurb))
		
		#get degree values of nurb
		degree_u = cmds.getAttr('{0}.degreeU'.format(nurb))
		degree_v = cmds.getAttr('{0}.degreeV'.format(nurb))

		#sum spans to degree
		sum_u = spans_u + degree_u
		sum_v = spans_v + degree_v
		
		#multiply result of sums u and v values
		cp_nurb = sum_u * sum_v
		
		#nurb with all cp
		all_cp_nurb = '{0}.cp[0:{1}]'.format(nurb, cp_nurb)
		
		#copyskin
		cmds.copySkinWeights(geo, all_cp_nurb, nm=True, sa='closestPoint', ia='oneToOne')

		cmds.select(geo)

	def click_copy(self):
		geos = cmds.ls(sl=True)
		source = geos[0]
		destination = geos[-1]

		joints = cmds.skinCluster(source, q=True, inf=True)
		try:
			cmds.skinCluster(joints, destination, sm=0, bm=1, tsb=True)
		except:
			cmds.select(destination)
			mel.eval('doDetachSkin "2" { "1","1" }')
			cmds.skinCluster(joints, destination, sm=0, bm=1, tsb=True)


		cmds.copySkinWeights(source, destination, noMirror=True,
							 surfaceAssociation='closestComponent', influenceAssociation=('oneToOne', 'label'),
							 normalize=True)

	# CLOSE EVENTS _________________________________
	def closeEvent(self, event):
		''


# -------------------------------------------------------------------

if __name__ == "__main__":

	try:
		SkinTab.close()  # pylint: disable=E0601
		SkinTab.deleteLater()
	except:
		pass
	cSkin_ui = SkinTab()
	cSkin_ui.show()

# -------------------------------------------------------------------


try:
	from PySide.QtGui import *
	from PySide.QtCore import *
except ImportError:
	from PySide2.QtGui import *
	from PySide2.QtCore import *
	from PySide2.QtWidgets import *


class Bezier(QWidget):
	valueChanged = Signal()

	def __init__(self):
		QWidget.__init__(self)
		self.points = [[0.0, 0.0], [1.0 / 3, 0.0], [2.0 / 3, 1.0], [1.0, 1.0]]
		self.__movePoint = 0
		self.__mirror = False
		self.__adsorb = False
		self.setFixedSize(200, 180)

	def paintEvent(self, event):
		QWidget.paintEvent(self, event)
		painter = QPainter(self)
		# background
		painter.setBrush(QBrush(QColor(120, 120, 120), Qt.SolidPattern))
		painter.setPen(QPen(QColor(0, 0, 0), 1, Qt.SolidLine))
		painter.drawRect(0, 0, self.width() - 1, self.height() - 1)
		# curve
		painter.setBrush(QBrush(QColor(100, 100, 100), Qt.SolidPattern))
		points = [QPointF((self.width() - 1) * p[0], (self.height() - 1) * p[1]) for p in self.points]
		path = QPainterPath()
		path.moveTo(0, self.height() - 1)
		path.lineTo(points[0])
		path.cubicTo(*points[1:])
		path.lineTo(self.width() - 1, self.height() - 1)
		painter.drawPath(path)
		# grid
		painter.setPen(QPen(QColor(200, 200, 200), 1, Qt.DotLine))
		w_step = (self.width() - 1) / 6.0
		h_step = (self.height() - 1) / 6.0
		for i in range(1, 6):
			w = w_step * i
			h = h_step * i
			painter.drawLine(w, 0, w, self.height())
			painter.drawLine(0, h, self.width(), h)
		# control point
		painter.setPen(QPen(QColor(0, 0, 0), 1, Qt.SolidLine))
		painter.setBrush(QBrush(QColor(200, 200, 200), Qt.SolidPattern))
		painter.drawEllipse(points[1], 6, 6)
		painter.drawEllipse(points[2], 6, 6)
		# edge
		painter.setPen(QPen(QColor(0, 0, 0), 1, Qt.SolidLine))
		edge_points = []
		for w, h in zip([0, 0, 1, 1, 0], [0, 1, 1, 0, 0]):
			p = QPointF(w * (self.width() - 1), h * (self.height() - 1))
			edge_points.extend([p, p])
		painter.drawLines(edge_points[1:-1])
		# control line
		painter.setPen(QPen(QColor(200, 200, 200), 1, Qt.DashLine))
		painter.drawLine(points[0], points[1])
		painter.drawLine(points[3], points[2])
		painter.end()

	def mousePressEvent(self, event):
		self.setFocus()
		QWidget.mousePressEvent(self, event)
		points = [QPointF((self.width() - 1) * p[0], (self.height() - 1) * p[1]) for p in self.points]
		p = QPointF(event.pos()) - points[1]
		length = (p.x() ** 2 + p.y() ** 2) ** 0.5
		if length < 10:
			self.__movePoint = 1
			return
		p = QPointF(event.pos()) - points[2]
		length = (p.x() ** 2 + p.y() ** 2) ** 0.5
		if length < 10:
			self.__movePoint = 2
			return
		self.__movePoint = 0

	def mouseMoveEvent(self, event):
		if self.__movePoint == 1:
			p = QPointF(event.pos())
			x = max(min(float(p.x()) / (self.width() - 1), 1.0), 0.0)
			y = max(min(float(p.y()) / (self.height() - 1), 1.0), 0.0)
			if self.__adsorb:
				x = round(x * 12) / 12.0
				y = round(y * 12) / 12.0
			if self.__mirror:
				mx = (1 - x)
				my = (1 - y)
				self.points[2] = [mx, my]
			self.points[1] = [x, y]
			self.update()
			self.valueChanged.emit()
		if self.__movePoint == 2:
			p = QPointF(event.pos())
			x = max(min(float(p.x()) / (self.width() - 1), 1.0), 0.0)
			y = max(min(float(p.y()) / (self.height() - 1), 1.0), 0.0)
			if self.__adsorb:
				x = round(x * 6) / 6.0
				y = round(y * 6) / 6.0
			if self.__mirror:
				mx = (1 - x)
				my = (1 - y)
				self.points[1] = [mx, my]
			self.points[2] = [x, y]
			self.update()
			self.valueChanged.emit()

	def keyPressEvent(self, event):
		QWidget.keyPressEvent(self, event)
		# Key X snap to the grid
		if event.key() == Qt.Key_X:
			self.__adsorb = True
		# Key Shift mirror the bezier curve
		if event.modifiers() == Qt.ShiftModifier:
			self.__mirror = True

	def keyReleaseEvent(self, event):
		QWidget.keyReleaseEvent(self, event)
		self.__mirror = False
		self.__adsorb = False

	def convert_UI_data(self):
		data = self.get_ui_kwargs()
		point_data = []
		for pointX, pointY in zip(data['xs'], data['ys']):
			point_data.append(str(pointX))
			point_data.append(str(pointY))
			point_data.append(str(2))
		# data = [str(pointX), str(pointY), str(2)]
		# temp_string = ",".join(data)
		soft_string = ",".join(point_data)
		#print("Curve Editor values: " + soft_string)
		return soft_string

	def get_ui_kwargs(self):
		return dict(
			r=0,
			xs=[x for x, y in self.points],
			ys=[1 - y for x, y in self.points],
		)

