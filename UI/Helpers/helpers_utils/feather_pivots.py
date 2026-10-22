from __future__ import absolute_import, division
"""
---------------Feather Pivots: move the PivotX / Y / Z of the Wings v002 feather ctrls-----------------
"""

# Select feather ctrls (the first ctrl of every feather, it has Pivots > PivotX / PivotY / PivotZ from the
# Wings v002 build) and drag the sliders. The sliders jog: dragging adds to the pivot, releasing goes back to
# the middle, a full drag is 10 units times the speed (slider x0.1 to x10, or type any). The boxes set the value right away.
# Test Rotation turns the ctrls (-180 / 180) to see them turn on the new pivot, Zero Rotation puts them back.
# Double click a slider or press its reset icon: pivot / rotate back to 0, speed back to x0.25.
# Mirror L > R copies every L feather pivot to the same R feather, mirrored in world X.
# Toggle Geo shows / hides the geo in the field (names or wildcards, space or comma separated) to see the ctrls.

import math

import maya.cmds as cmds
import maya.OpenMayaUI as omui
import maya.api.OpenMaya as om

try:
	from shiboken6 import wrapInstance
	from PySide6 import QtCore, QtGui, QtWidgets
except ImportError:
	from shiboken2 import wrapInstance #Compatibility pre 2026
	from PySide2 import QtCore, QtGui, QtWidgets


PIVOT_ATTRS = ('PivotX', 'PivotY', 'PivotZ')
ROTATE_ATTRS = ('rx', 'ry', 'rz')
SLIDER_RANGE = 100
SLIDER_UNITS = 10.0  # units of a full drag at x1
SPEED_RANGE = 10.0  # speed slider from x1/10 to x10
DEFAULT_SPEED = 0.25
DEFAULT_GEO = 'Lf_Fea_SC_Geo_Grp'
WINDOW_NAME = 'MutantFeatherPivots'
RESET_ICON = ':/refresh.png'


def has_pivots(node):
	return all(cmds.attributeQuery(attr, n=node, exists=True) for attr in PIVOT_ATTRS)


def selected_feather_ctrls():
	return [node for node in cmds.ls(sl=True, type='transform') or [] if has_pivots(node)]


def _settable(plug):
	return cmds.getAttr(plug, settable=True)


def _mirror_signs(left, right):
	"""Per axis sign from the L ctrl to the R ctrl: R frame = signs * L frame mirrored in world X."""
	mirror_x = om.MMatrix([-1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1])
	frame = lambda node: om.MTransformationMatrix(om.MMatrix(cmds.getAttr(node + '.worldMatrix[0]'))).asRotateMatrix()
	to_right = frame(right) * mirror_x * frame(left).inverse()
	return [1 if to_right.getElement(i, i) >= 0 else -1 for i in range(3)]


def mirror_pivots_to_right():
	cmds.undoInfo(openChunk=True, chunkName='MirrorFeatherPivots')
	try:
		mirrored = []
		for left in cmds.ls('L_*', type='transform'):
			right = 'R_' + left[2:]
			if not has_pivots(left) or not cmds.objExists(right) or not has_pivots(right):
				continue
			for attr, sign in zip(PIVOT_ATTRS, _mirror_signs(left, right)):
				plug = '{}.{}'.format(right, attr)
				if _settable(plug):
					cmds.setAttr(plug, cmds.getAttr('{}.{}'.format(left, attr)) * sign)
			mirrored.append(right)
	finally:
		cmds.undoInfo(closeChunk=True)
	print('Feather Pivots: mirrored {} feathers to R'.format(len(mirrored)))
	return mirrored


def toggle_geo(names):
	"""Hide the nodes if any is visible, show them if all are hidden."""
	nodes = cmds.ls(names.replace(',', ' ').split(), type='transform') or []
	plugs = [node + '.visibility' for node in nodes if _settable(node + '.visibility')]
	if not plugs:
		cmds.warning('Feather Pivots: no geo to toggle in "{}"'.format(names))
		return None
	visible = not any(cmds.getAttr(plug) for plug in plugs)
	cmds.undoInfo(openChunk=True, chunkName='FeatherPivotsToggleGeo')
	try:
		for plug in plugs:
			cmds.setAttr(plug, visible)
	finally:
		cmds.undoInfo(closeChunk=True)
	return visible


#-------------------------------------------------

def maya_main_window():
	return wrapInstance(int(omui.MQtUtil.mainWindow()), QtWidgets.QWidget)


class JogSlider(QtWidgets.QSlider):
	"""Only dragging moves it, no wheel / keys, so every move is one undo. Double click resets it."""

	reset = QtCore.Signal()

	def __init__(self, parent=None):
		super(JogSlider, self).__init__(QtCore.Qt.Horizontal, parent)
		self.setRange(-SLIDER_RANGE, SLIDER_RANGE)
		self.setValue(0)
		self.setFocusPolicy(QtCore.Qt.NoFocus)

	def wheelEvent(self, event):
		event.ignore()

	def mouseDoubleClickEvent(self, event):
		self.reset.emit()


def _reset_button():
	button = QtWidgets.QToolButton()
	button.setIcon(QtGui.QIcon(RESET_ICON))
	button.setAutoRaise(True)
	button.setToolTip('Reset')
	return button


def _value_box(minimum, maximum):
	box = QtWidgets.QDoubleSpinBox()
	box.setRange(minimum, maximum)
	box.setDecimals(3)
	box.setKeyboardTracking(False)
	box.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
	box.setFixedWidth(70)
	return box


# a tool window, not a QDialog: a dialog closes on Esc and presses its default button on Enter
class FeatherPivotsUI(QtWidgets.QWidget):

	def __init__(self, parent=None):
		super(FeatherPivotsUI, self).__init__(parent or maya_main_window())
		self.setObjectName(WINDOW_NAME)
		self.setWindowTitle('Feather Pivots')
		self.setWindowFlags(QtCore.Qt.Tool)
		self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
		self.setMinimumWidth(300)

		self.ctrls = []
		self.drag_start = {}
		self.speed = DEFAULT_SPEED
		self.job = None

		self.create_layout()
		self.create_connections()
		self.set_speed(self.speed)
		self.selection_changed()
		self.job = cmds.scriptJob(event=['SelectionChanged', self.selection_changed], killWithScene=False)

	def create_layout(self):
		layout = QtWidgets.QVBoxLayout(self)
		layout.setContentsMargins(6, 6, 6, 6)
		layout.setSpacing(4)

		self.selection_label = QtWidgets.QLabel()
		self.selection_label.setWordWrap(True)
		layout.addWidget(self.selection_label)

		speed_row = QtWidgets.QHBoxLayout()
		speed_row.addWidget(QtWidgets.QLabel('Speed'))
		self.speed_slider = JogSlider()
		self.speed_box = _value_box(0.001, 1000)
		self.speed_box.setValue(self.speed)
		self.speed_reset = _reset_button()
		speed_row.addWidget(self.speed_slider)
		speed_row.addWidget(self.speed_box)
		speed_row.addWidget(self.speed_reset)
		layout.addLayout(speed_row)

		self.axis_widgets = QtWidgets.QWidget()
		grid = QtWidgets.QGridLayout(self.axis_widgets)
		grid.setContentsMargins(0, 0, 0, 0)
		self.sliders = []
		self.boxes = []
		self.zero_buttons = []
		for row, attr in enumerate(PIVOT_ATTRS):
			grid.addWidget(QtWidgets.QLabel(attr[-1]), row, 0)
			slider = JogSlider()
			box = _value_box(-100000, 100000)
			zero = _reset_button()
			grid.addWidget(slider, row, 1)
			grid.addWidget(box, row, 2)
			grid.addWidget(zero, row, 3)
			self.sliders.append(slider)
			self.boxes.append(box)
			self.zero_buttons.append(zero)
		layout.addWidget(self.axis_widgets)

		# test the pivot: turn the ctrl, Zero puts it back
		self.rotate_widgets = QtWidgets.QGroupBox('Test Rotation')
		rotate_grid = QtWidgets.QGridLayout(self.rotate_widgets)
		rotate_grid.setContentsMargins(4, 4, 4, 4)
		self.rotate_sliders = []
		self.rotate_labels = []
		self.rotate_zero_buttons = []
		for row, attr in enumerate(ROTATE_ATTRS):
			rotate_grid.addWidget(QtWidgets.QLabel(attr[-1].upper()), row, 0)
			slider = JogSlider()
			slider.setRange(-180, 180)
			label = QtWidgets.QLabel('0')
			label.setFixedWidth(34)
			zero = _reset_button()
			rotate_grid.addWidget(slider, row, 1)
			rotate_grid.addWidget(label, row, 2)
			rotate_grid.addWidget(zero, row, 3)
			self.rotate_sliders.append(slider)
			self.rotate_labels.append(label)
			self.rotate_zero_buttons.append(zero)
		self.zero_rotate_button = QtWidgets.QPushButton('Zero Rotation')
		rotate_grid.addWidget(self.zero_rotate_button, len(ROTATE_ATTRS), 0, 1, 4)
		layout.addWidget(self.rotate_widgets)

		geo_row = QtWidgets.QHBoxLayout()
		geo_row.addWidget(QtWidgets.QLabel('Geo'))
		self.geo_field = QtWidgets.QLineEdit(DEFAULT_GEO)
		self.geo_field.setToolTip('Names or wildcards, space or comma separated')
		self.geo_button = QtWidgets.QPushButton('Toggle Geo')
		geo_row.addWidget(self.geo_field)
		geo_row.addWidget(self.geo_button)
		layout.addLayout(geo_row)

		self.mirror_button = QtWidgets.QPushButton('Mirror L > R')
		self.mirror_button.setMinimumHeight(26)
		layout.addWidget(self.mirror_button)

	def create_connections(self):
		self.speed_slider.valueChanged.connect(self.speed_slider_changed)
		self.speed_box.valueChanged.connect(self.set_speed)
		self.speed_slider.reset.connect(lambda: self.speed_box.setValue(DEFAULT_SPEED))
		self.speed_reset.clicked.connect(lambda: self.speed_box.setValue(DEFAULT_SPEED))
		for attr, slider, box, zero in zip(PIVOT_ATTRS, self.sliders, self.boxes, self.zero_buttons):
			slider.sliderPressed.connect(lambda attr=attr: self.drag_pressed(attr))
			slider.sliderMoved.connect(lambda value, attr=attr: self.drag_moved(attr, value))
			slider.sliderReleased.connect(lambda slider=slider: self.drag_released(slider))
			slider.reset.connect(lambda attr=attr: self.set_value([attr], 0))
			box.valueChanged.connect(lambda value, attr=attr: self.set_value([attr], value))
			zero.clicked.connect(lambda checked=False, attr=attr: self.set_value([attr], 0))
		for attr, slider, zero in zip(ROTATE_ATTRS, self.rotate_sliders, self.rotate_zero_buttons):
			slider.sliderPressed.connect(lambda: cmds.undoInfo(openChunk=True, chunkName='FeatherPivotsRotate'))
			slider.sliderMoved.connect(lambda value, attr=attr: self.rotate_moved(attr, value))
			slider.sliderReleased.connect(lambda: cmds.undoInfo(closeChunk=True))
			slider.reset.connect(lambda attr=attr: self.set_value([attr], 0))
			zero.clicked.connect(lambda checked=False, attr=attr: self.set_value([attr], 0))
		self.zero_rotate_button.clicked.connect(lambda checked=False: self.set_value(ROTATE_ATTRS, 0))
		self.mirror_button.clicked.connect(self.mirror)
		self.geo_button.clicked.connect(lambda checked=False: toggle_geo(self.geo_field.text()))
		self.geo_field.returnPressed.connect(lambda: toggle_geo(self.geo_field.text()))

	#-------------------------------------------------

	def speed_slider_changed(self, value):
		# log: middle x1, ends x0.1 / x10
		self.speed_box.setValue(round(SPEED_RANGE ** (value / float(SLIDER_RANGE)), 3))

	def set_speed(self, value):
		self.speed = value
		self.speed_slider.blockSignals(True)
		self.speed_slider.setValue(int(round(math.log(value, SPEED_RANGE) * SLIDER_RANGE)))
		self.speed_slider.blockSignals(False)

	def selection_changed(self):
		self.ctrls = selected_feather_ctrls()
		self.axis_widgets.setEnabled(bool(self.ctrls))
		self.rotate_widgets.setEnabled(bool(self.ctrls))
		if not self.ctrls:
			self.selection_label.setText('Select a feather ctrl with Pivots')
		elif len(self.ctrls) == 1:
			self.selection_label.setText(self.ctrls[0])
		else:
			self.selection_label.setText('{} feather ctrls'.format(len(self.ctrls)))
		self.refresh_boxes()

	def refresh_boxes(self):
		for attr, box in zip(PIVOT_ATTRS, self.boxes):
			box.blockSignals(True)
			box.setValue(cmds.getAttr('{}.{}'.format(self.ctrls[0], attr)) if self.ctrls else 0)
			box.blockSignals(False)
		for attr, slider, label in zip(ROTATE_ATTRS, self.rotate_sliders, self.rotate_labels):
			value = cmds.getAttr('{}.{}'.format(self.ctrls[0], attr)) if self.ctrls else 0
			slider.blockSignals(True)
			slider.setValue(int(round(max(-180, min(180, value)))))
			slider.blockSignals(False)
			label.setText('{:g}'.format(round(value, 1)))

	def _plugs(self, attr):
		plugs = ['{}.{}'.format(ctrl, attr) for ctrl in self.ctrls if cmds.objExists(ctrl)]
		return [plug for plug in plugs if _settable(plug)]

	def drag_pressed(self, attr):
		cmds.undoInfo(openChunk=True, chunkName='FeatherPivots')
		self.drag_start = dict((plug, cmds.getAttr(plug)) for plug in self._plugs(attr))

	def drag_moved(self, attr, value):
		offset = value / float(SLIDER_RANGE) * SLIDER_UNITS * self.speed
		for plug, start in self.drag_start.items():
			cmds.setAttr(plug, start + offset)
		self.refresh_boxes()

	def drag_released(self, slider):
		self.drag_start = {}
		slider.blockSignals(True)
		slider.setValue(0)
		slider.blockSignals(False)
		cmds.undoInfo(closeChunk=True)
		self.refresh_boxes()

	def set_value(self, attrs, value):
		cmds.undoInfo(openChunk=True, chunkName='FeatherPivots')
		try:
			for attr in attrs:
				for plug in self._plugs(attr):
					cmds.setAttr(plug, value)
		finally:
			cmds.undoInfo(closeChunk=True)
		self.refresh_boxes()

	def rotate_moved(self, attr, value):
		for plug in self._plugs(attr):
			cmds.setAttr(plug, value)
		self.refresh_boxes()

	def mirror(self):
		mirror_pivots_to_right()
		self.refresh_boxes()

	#-------------------------------------------------

	def kill_job(self):
		if self.job and cmds.scriptJob(exists=self.job):
			cmds.scriptJob(kill=self.job, force=True)
		self.job = None

	def closeEvent(self, event):
		self.kill_job()
		QtWidgets.QWidget.closeEvent(self, event)


def show():
	# an open one (maybe from before a reload, another class): kill its job and close it
	for widget in QtWidgets.QApplication.topLevelWidgets():
		if widget.objectName() == WINDOW_NAME:
			job = getattr(widget, 'job', None)
			if job and cmds.scriptJob(exists=job):
				cmds.scriptJob(kill=job, force=True)
			widget.job = None
			widget.deleteLater()
	window = FeatherPivotsUI()
	window.show()
	return window
