from __future__ import absolute_import
'''
version: 1.0.0
date: 06/08/2026

#----------------
content:

ArkKit — author the 52 ARKit facial blendshapes from a Maya face rig.

Pose the rig, record each pose as a delta from a captured neutral default,
blend expressions additively to preview, and bake the results onto character
geos as ARKit-named blendshape targets. Wrapped in the Mutant Tools frameless
window (QtMutantWindow.Qt_Mutant) so it looks and behaves like the rest of
the toolset.

#----------------
how to:

try:
	import importlib;from importlib import reload
except:
	import imp;from imp import reload

import Mutant_Tools
from Mutant_Tools.UI.ArkKit import load_arkkit
reload(load_arkkit)

try:cArkKitUI.close()
except:pass
cArkKitUI = load_arkkit.ArkKitUI()
cArkKitUI.show()

#----------------
dependencies:

Main Mutant
arkkit_core (bundled alongside this loader)

#----------------
www.mutanttools.com
author:  Esteban Rodriguez <info@renderdemartes.com>

'''
# -------------------------------------------------------------------
try:
	from shiboken6 import wrapInstance
	from PySide6 import QtGui, QtCore
	from PySide6 import QtUiTools
	from PySide6 import QtWidgets
	from PySide6.QtWidgets import *
except:
	from shiboken2 import wrapInstance #Compatibility pre 2026
	from PySide2 import QtGui, QtCore
	from PySide2 import QtUiTools
	from PySide2 import QtWidgets
	from PySide2.QtWidgets import *

import maya.OpenMaya as om
import maya.OpenMayaUI as omui
from maya import cmds
import os
import re
import webbrowser
try:
	import importlib;from importlib import reload
except:
	import imp;from imp import reload

try:
	import maya.api.OpenMaya as api_om
except Exception:
	api_om = om

from pathlib import Path

# -------------------------------------------------------------------

# QT Window!
FOLDER_NAME = 'ArkKit'
Title = 'ArkKit'
REFERENCE_URL = 'https://arkit-face-blendshapes.com/'
REFERENCE_CONTEXT_URL = 'https://miniface.org/faces?utm_source=pooyadeperson&utm_medium=cheekPuff'

PATH = os.path.dirname(__file__)
PATH = Path(PATH)
PATH_PARTS = PATH.parts[:-2]
FOLDER = ''
for f in PATH_PARTS:
	FOLDER = os.path.join(FOLDER, f)

IconsPath = os.path.join(FOLDER, 'Icons')

# -------------------------------------------------------------------

import Mutant_Tools
import Mutant_Tools.UI
from Mutant_Tools.UI import QtMutantWindow
reload(QtMutantWindow)

from Mutant_Tools.UI.ArkKit.arkkit_core import config, utils, data_node, mirror
from Mutant_Tools.UI.ArkKit.arkkit_core.widgets import CollapsibleGroup, ExpressionRow

for _module in (config, utils, data_node, mirror):
	reload(_module)

# -------------------------------------------------------------------


def maya_main_window():
	main_window_ptr = omui.MQtUtil.mainWindow()
	return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)


class ArkKitUI(QtMutantWindow.Qt_Mutant):

	def __init__(self):
		super(ArkKitUI, self).__init__()

		self.setObjectName('ArkKitWindow')
		self.setWindowTitle(Title)
		self.set_title(Title)

		# -------- state --------
		self.rows = []                 # ExpressionRow, in config.EXPRESSIONS order
		self.rows_by_name = {}
		self.recording = None          # name of the row currently recording, or None
		self.combo_mode = False        # while True, other rows stay live during recording
		self.last_clicked = None       # for shift range-select
		self.last_export_dir = config.EXPORTS_DIR

		# In-memory caches, kept in sync with the ArkKit_Data node.
		self.controls = config.load_controls()
		self.defaults = {}             # {plug: value}
		self.deltas = {}               # {expr_name: {plug: delta}}
		self.mirror_signs = {}         # {control: {channel: sign}} from the snapshot

		# Plugs touched by the last blend, so the next one can reset any that
		# just went inactive without re-writing every captured channel.
		self._last_active_plugs = set()

		self.create_layout()
		self.resize(480, 780)
		self.refresh_from_scene()

	# ====================================================================
	# UI CONSTRUCTION
	# ====================================================================

	def create_layout(self):
		container = QtWidgets.QWidget()
		main = QtWidgets.QVBoxLayout(container)
		self.master_ui.mutant_Layout.addWidget(container)
		self.ui = container

		# ---- version header ----
		header_row = QtWidgets.QHBoxLayout()
		main.addLayout(header_row)

		header_row.addStretch()

		self.reference_btn = QtWidgets.QPushButton("ARKit Reference ↗")
		self.reference_btn.setToolTip(
			"Open {} in the default browser — the ARKit blendshape reference\n"
			"this tool's 52 expressions are based on.\n\n"
			"Right-click to open the Miniface reference page instead."
			.format(REFERENCE_URL)
		)
		self.reference_btn.clicked.connect(self.open_reference_site)
		self.reference_btn.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
		self.reference_btn.customContextMenuRequested.connect(self.open_reference_context_site)
		header_row.addWidget(self.reference_btn)

		version_label = QtWidgets.QLabel("v{}".format(config.VERSION))
		version_label.setStyleSheet("color: #5ADE50; font-weight: bold;")
		version_label.setToolTip("Tool version — bumps on each update; confirms a reload took.")
		header_row.addWidget(version_label)

		# ---- search row ----
		search_row = QtWidgets.QHBoxLayout()
		main.addLayout(search_row)

		self.search = QtWidgets.QLineEdit()
		self.search.setPlaceholderText("Search: jaw, mouth, eye...")
		self.search.textChanged.connect(self.filter_rows)
		search_row.addWidget(self.search)

		self.refresh_btn = QtWidgets.QPushButton("↻")
		self.refresh_btn.setFixedWidth(28)
		self.refresh_btn.setToolTip("Refresh: re-sync the UI from the ArkKit_Data node")
		self.refresh_btn.clicked.connect(self.refresh_from_scene)
		search_row.addWidget(self.refresh_btn)

		# ---- defaults / controls row ----
		setup_row = QtWidgets.QHBoxLayout()
		main.addLayout(setup_row)

		self.add_controls_btn = QtWidgets.QPushButton("Add Selected → Controls")
		self.add_controls_btn.setToolTip(
			"Append the currently selected nodes to the control list.\n"
			"Then press Save Defaults to (re)capture."
		)
		self.add_controls_btn.clicked.connect(self.add_selected_controls)
		setup_row.addWidget(self.add_controls_btn)

		self.set_defaults_btn = QtWidgets.QPushButton("Save Defaults")
		self.set_defaults_btn.setToolTip(
			"Capture the current pose of every listed control's keyable channels\n"
			"as the neutral default, and create the ArkKit_Data node."
		)
		self.set_defaults_btn.clicked.connect(self.set_defaults)
		setup_row.addWidget(self.set_defaults_btn)

		self.snapshot_btn = QtWidgets.QPushButton("Snapshot Mirror *")
		self.snapshot_btn.setToolTip(
			"Learn how each control channel mirrors, by probing the rig at its\n"
			"default pose. Run once (re-run if you change controls or MIRROR_AXIS).\n"
			"Stored on the ArkKit_Data node."
		)
		self.snapshot_btn.clicked.connect(self.snapshot_mirror)
		setup_row.addWidget(self.snapshot_btn)

		self.combo_mode_chk = QtWidgets.QCheckBox("Combo Mode")
		self.combo_mode_chk.setToolTip(
			"OFF: recording isolates one shape — other rows lock and the pose\n"
			"resets to defaults + this expression's existing delta.\n"
			"ON: other rows stay live while recording, so you can dial in an\n"
			"already-recorded shape as a reference pose (e.g. Jaw while\n"
			"recording MouthClose) and still tweak the rig by hand.\n"
			"That reference row's own contribution is subtracted back out on\n"
			"stop — only this expression's own difference gets saved."
		)
		self.combo_mode_chk.toggled.connect(self.set_combo_mode)

		self.status_label = QtWidgets.QLabel()
		self.status_label.setStyleSheet("color: #B0BEC5;")
		main.addWidget(self.status_label)

		# ---- expression rows (scrollable, grouped) ----
		scroll = QtWidgets.QScrollArea()
		scroll.setWidgetResizable(True)
		scroll_container = QtWidgets.QWidget()
		self.rows_layout = QtWidgets.QVBoxLayout(scroll_container)

		for group_name, names in config.BLENDSHAPE_GROUPS.items():
			group = CollapsibleGroup(group_name)
			self.rows_layout.addWidget(group)

			for name in names:
				row = ExpressionRow(name)
				row.clicked.connect(self.handle_click)
				row.valueChanged.connect(self.slider_changed)
				row.recordToggled.connect(self.on_record_pressed)
				row.dragStarted.connect(self.begin_undo)
				row.dragEnded.connect(self.end_undo)

				group.content_layout.addWidget(row)
				self.rows.append(row)
				self.rows_by_name[name] = row

		self.rows_layout.addStretch()
		scroll.setWidget(scroll_container)
		main.addWidget(scroll, 1)

		# ---- expression action row ----
		action_row = QtWidgets.QHBoxLayout()
		main.addLayout(action_row)

		self.zero_btn = QtWidgets.QPushButton("Zero All")
		self.zero_btn.setToolTip("Set all blend sliders to 0 (return controls to defaults).")
		self.zero_btn.clicked.connect(self.zero_all)
		action_row.addWidget(self.zero_btn)

		self.delete_btn = QtWidgets.QPushButton("Delete Selected")
		self.delete_btn.setToolTip("Clear the recorded data for the selected expression(s).")
		self.delete_btn.clicked.connect(self.delete_selected)
		action_row.addWidget(self.delete_btn)

		# ---- mirror row ----
		mirror_row = QtWidgets.QHBoxLayout()
		main.addLayout(mirror_row)

		self.combo_mode_chk.setChecked(self.combo_mode)
		mirror_row.addWidget(self.combo_mode_chk)

		self.mirror_btn = QtWidgets.QPushButton("Mirror → Opposite")
		self.mirror_btn.setToolTip(
			"Write each selected expression's mirror onto its opposite-named\n"
			"shape (e.g. eyeBlinkLeft → eyeBlinkRight). Overwrites the opposite."
		)
		self.mirror_btn.clicked.connect(self.mirror_to_opposite)
		mirror_row.addWidget(self.mirror_btn)

		self.symmetrize_btn = QtWidgets.QPushButton("Symmetrize")
		self.symmetrize_btn.setToolTip(
			"Make a pose bilaterally symmetric (copy the source side onto the\n"
			"other). While recording, this symmetrizes the LIVE rig; otherwise it\n"
			"symmetrizes the selected recorded expression(s)."
		)
		self.symmetrize_btn.clicked.connect(self.symmetrize)
		mirror_row.addWidget(self.symmetrize_btn)

		self.sym_dir = QtWidgets.QComboBox()
		self.sym_dir.addItems(["L→R", "R→L"])
		self.sym_dir.setFixedWidth(56)
		self.sym_dir.setToolTip("Symmetrize direction: which side is copied onto the other.")
		mirror_row.addWidget(self.sym_dir)

		# ---- export / import row ----
		io_row = QtWidgets.QHBoxLayout()
		main.addLayout(io_row)

		self.export_btn = QtWidgets.QPushButton("Export…")
		self.export_btn.setToolTip("Write all ArkKit data to a JSON file.")
		self.export_btn.clicked.connect(self.export_data)
		io_row.addWidget(self.export_btn)

		self.import_btn = QtWidgets.QPushButton("Import…")
		self.import_btn.setToolTip("Load ArkKit data from a JSON file onto this scene.")
		self.import_btn.clicked.connect(self.import_data)
		io_row.addWidget(self.import_btn)

		# ---- geo bake section (collapsed by default to save space) ----
		geo_group = CollapsibleGroup("Target Geos", expanded=False)
		geo_layout = geo_group.content_layout
		main.addWidget(geo_group)

		self.geo_list = QtWidgets.QListWidget()
		self.geo_list.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
		self.geo_list.setFixedHeight(90)
		geo_layout.addWidget(self.geo_list)

		geo_btn_row = QtWidgets.QHBoxLayout()
		geo_layout.addLayout(geo_btn_row)

		self.add_geo_btn = QtWidgets.QPushButton("Add Selected Geos")
		self.add_geo_btn.clicked.connect(self.add_selected_geos)
		geo_btn_row.addWidget(self.add_geo_btn)

		self.remove_geo_btn = QtWidgets.QPushButton("Remove Selected")
		self.remove_geo_btn.clicked.connect(self.remove_selected_geos)
		geo_btn_row.addWidget(self.remove_geo_btn)

		self.include_all_chk = QtWidgets.QCheckBox("Bake all 52 (empty targets for unrecorded)")
		self.include_all_chk.setChecked(True)
		self.include_all_chk.setToolTip(
			"ON: create all 52 ARKit-named targets — unrecorded ones are neutral\n"
			"(zero-effect) placeholders. Safest for full ARKit / game-engine setups.\n"
			"OFF: only bake the expressions you have recorded."
		)
		geo_layout.addWidget(self.include_all_chk)

		bake_row = QtWidgets.QHBoxLayout()
		geo_layout.addLayout(bake_row)

		self.generate_btn = QtWidgets.QPushButton("Generate Blendshapes")
		self.generate_btn.setToolTip(
			"For each expression to bake: pose the rig, duplicate each target\n"
			"geo, and add it as an ARKit-named blendshape target on that geo.\n"
			"Creates a fresh <geo>_ArkKit_BS node (use Update to edit existing ones)."
		)
		self.generate_btn.clicked.connect(self.generate_blendshapes)
		bake_row.addWidget(self.generate_btn)

		self.update_btn = QtWidgets.QPushButton("Update Selected *")
		self.update_btn.setToolTip(
			"Re-bake targets on the EXISTING blendshape node(s) from the current\n"
			"recorded data — overriding what the character already has.\n"
			"\n"
			"Left-click: update ONLY the selected expression(s).\n"
			"Right-click: update ALL recorded expressions EXCEPT the selected ones.\n"
			"\n"
			"Existing targets are replaced in place (index/alias kept); a selected\n"
			"expression not yet on the node is added. Requires an existing\n"
			"<geo>_ArkKit_BS node — run Generate first if there isn't one."
		)
		self.update_btn.clicked.connect(lambda: self.update_blendshapes(invert=False))
		self.update_btn.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
		self.update_btn.customContextMenuRequested.connect(
			lambda pos: self.update_blendshapes(invert=True)
		)
		bake_row.addWidget(self.update_btn)

		bake_row_2 = QtWidgets.QHBoxLayout()
		geo_layout.addLayout(bake_row_2)

		self.delete_node_btn = QtWidgets.QPushButton("Delete ARK Node")
		self.delete_node_btn.setToolTip(
			"Look for the ArkKit blendShape node on the currently selected meshes\n"
			"and delete it if it exists."
		)
		self.delete_node_btn.clicked.connect(self.delete_ark_nodes)
		bake_row_2.addWidget(self.delete_node_btn)

		self.delete_empty_targets_btn = QtWidgets.QPushButton("Delete Empty Targets")
		self.delete_empty_targets_btn.setToolTip(
			"Rebuild the selected mesh's blendShape node without targets that\n"
			"do not deform the mesh at weight 1.0. Preserves surviving aliases,\n"
			"values, connections, and deform stack order where possible."
		)
		self.delete_empty_targets_btn.clicked.connect(self.delete_empty_targets)
		bake_row_2.addWidget(self.delete_empty_targets_btn)

		# Buttons disabled while a recording is active. Symmetrize is
		# deliberately NOT here — symmetrizing the live pose mid-record is a
		# core part of authoring.
		self._busy_buttons = [
			self.set_defaults_btn, self.add_controls_btn, self.zero_btn,
			self.delete_btn, self.export_btn, self.import_btn,
			self.add_geo_btn, self.remove_geo_btn, self.generate_btn,
			self.update_btn, self.delete_node_btn, self.delete_empty_targets_btn,
			self.refresh_btn, self.snapshot_btn, self.mirror_btn,
		]

	def create_connections(self):
		"""Signals are wired inline in create_layout() as widgets are built."""

	def open_reference_site(self):
		webbrowser.open(REFERENCE_URL)

	def open_reference_context_site(self, pos=None):
		webbrowser.open(REFERENCE_CONTEXT_URL)

	# ====================================================================
	# REFRESH / STATUS
	# ====================================================================

	def refresh_from_scene(self):
		"""Re-sync all in-memory caches and UI indicators from the data node."""
		stored_controls = data_node.read_controls()
		if stored_controls:
			self.controls = stored_controls
		else:
			self.controls = config.load_controls()

		self.defaults = data_node.read_defaults()
		self.deltas = data_node.all_expressions()
		self.mirror_signs = data_node.read_mirror()

		for row in self.rows:
			row.set_value(0)
			row.set_has_data(row.name in self.deltas and bool(self.deltas[row.name]))
			row.set_selected(False)

		# geo list
		self.geo_list.clear()
		for geo in data_node.read_geos():
			self.geo_list.addItem(geo)

		self.update_status_label()

	def update_status_label(self):
		recorded = sum(1 for r in self.rows if r.has_data)
		defaults_state = "SET" if self.defaults else "none"
		mirror_state = "set" if data_node.has_mirror() else "none"
		self.status_label.setText(
			"Controls: {}  |  Defaults: {}  |  Mirror: {}  |  Recorded: {}/{}".format(
				len(self.controls), defaults_state, mirror_state, recorded, len(self.rows)
			)
		)

	def _set_busy(self, busy):
		"""Enable/disable everything except the active record button."""
		for btn in self._busy_buttons:
			btn.setEnabled(not busy)
		self.search.setEnabled(not busy)

	def set_combo_mode(self, state):
		self.combo_mode = bool(state)

	# ====================================================================
	# CONTROLS / DEFAULTS
	# ====================================================================

	def add_selected_controls(self):
		selected = utils.selected_transforms()
		if not selected:
			cmds.warning("ArkKit: nothing selected to add as a control.")
			return

		added = 0
		for node in selected:
			if node not in self.controls:
				self.controls.append(node)
				added += 1

		cmds.inViewMessage(
			amg="ArkKit: added <hl>{}</hl> control(s).".format(added),
			pos="midCenter", fade=True,
		)
		# Persist immediately so it survives even before Save Defaults.
		data_node.write_controls(self.controls)
		self.update_status_label()

	def set_defaults(self):
		if not self.controls:
			cmds.warning(
				"ArkKit: no controls listed. Edit data/controls.json or use "
				"'Add Selected → Controls'."
			)
			return

		plugs, missing = utils.capturable_plugs_for_controls(self.controls)

		if not plugs:
			cmds.warning("ArkKit: no capturable channels found on the listed controls.")
			return

		defaults = {}
		for plug in plugs:
			val = utils.get_plug_value(plug)
			if val is not None:
				defaults[plug] = val

		data_node.write_defaults(defaults)
		data_node.write_controls(self.controls)
		self.defaults = defaults

		msg = "ArkKit: captured {} channels from {} controls as defaults.".format(
			len(defaults), len(self.controls)
		)
		print("[ArkKit] " + msg)
		if missing:
			cmds.warning(
				"ArkKit: {} control(s) not found and skipped: {}".format(
					len(missing), ", ".join(missing[:10])
				)
			)
		cmds.inViewMessage(amg=msg, pos="midCenter", fade=True)
		self.update_status_label()

	# ====================================================================
	# RECORDING
	# ====================================================================

	def on_record_pressed(self, name):
		if self.recording == name:
			self.stop_record()
		elif self.recording is not None:
			# Auto-save the active one, then start the new one.
			self.stop_record()
			self.start_record(name)
		else:
			self.start_record(name)

	def start_record(self, name):
		if not self.defaults:
			cmds.warning("ArkKit: press 'Save Defaults' before recording.")
			return

		self.recording = name

		if not self.combo_mode:
			# Zero every slider, then pose the rig to defaults + this expression's
			# existing delta (so an already-recorded shape is refined, not lost).
			for row in self.rows:
				row.set_value(0)

			pose = dict(self.defaults)
			existing = self.deltas.get(name, {})
			for plug, d in existing.items():
				pose[plug] = self.defaults.get(plug, 0.0) + d

			cmds.undoInfo(openChunk=True)
			try:
				self._apply_pose(pose)
			finally:
				cmds.undoInfo(closeChunk=True)

		# Lock the whole UI; keep only this row's record button live.
		# In combo mode, rows stay unlocked so other recorded shapes can be
		# dialed in and blended with the live pose while this one records.
		self._set_busy(True)
		for row in self.rows:
			row.set_locked(not self.combo_mode)
			row.set_recording(False)

		active = self.rows_by_name[name]
		active.set_recording(True)
		active.record_btn.setEnabled(True)
		if not self.combo_mode:
			active.set_value(1)  # visual: this shape is being authored at full weight

	def stop_record(self):
		name = self.recording
		if name is None:
			return

		# In combo mode another row (e.g. Jaw) may be dialed in as a live
		# reference pose. Subtract its contribution back out per-channel so
		# only THIS expression's own difference is saved — otherwise the
		# reference shape's own controllers would get baked into this one.
		other_contribution = {}
		if self.combo_mode:
			for row in self.rows:
				if row.name == name:
					continue
				w = row.get_value()
				if w <= 0.0:
					continue
				other_delta = self.deltas.get(row.name)
				if not other_delta:
					continue
				for plug, dv in other_delta.items():
					other_contribution[plug] = other_contribution.get(plug, 0.0) + dv * w

		# Compute delta = current - (default + other rows' contribution)
		# for every captured channel.
		delta = {}
		for plug, dval in self.defaults.items():
			cur = utils.get_plug_value(plug)
			if cur is None:
				continue
			base = dval + other_contribution.get(plug, 0.0)
			diff = cur - base
			if abs(diff) > config.DELTA_EPSILON:
				delta[plug] = diff

		data_node.write_expression(name, delta)
		self.deltas[name] = delta

		self.recording = None

		# Unlock the UI.
		for row in self.rows:
			row.set_locked(False)
			row.set_recording(False)
		self._set_busy(False)

		active = self.rows_by_name[name]
		active.set_has_data(bool(delta))

		if not self.combo_mode:
			# Preview the freshly recorded shape at full weight; others stay at 0.
			for row in self.rows:
				row.set_value(1 if row.name == name else 0)
			self.apply_blend()

		print("[ArkKit] Recorded '{}' — {} changed channels.".format(name, len(delta)))
		self.update_status_label()

	# ====================================================================
	# BLENDING / PREVIEW
	# ====================================================================

	def slider_changed(self, name, value):
		if self.recording is not None and not self.combo_mode:
			return

		# Group-drag: dragging a selected row's slider drives every other
		# selected row's slider to the same weight, so a multi-selection
		# moves together.
		row = self.rows_by_name.get(name)
		if row is not None and row.selected:
			for r in self.get_selected():
				if r is not row:
					r.set_value(value)

		self.apply_blend()

	def apply_blend(self):
		"""Set the affected control channels to default + Σ(delta × weight).

		Only channels touched by a currently-active expression are written,
		plus any that were active on the previous blend and now need resetting
		to default. This keeps slider dragging fluid even with many controls,
		instead of re-writing every captured channel on every tick.
		"""
		if (self.recording is not None and not self.combo_mode) or not self.defaults:
			return

		pose = {}
		active_plugs = set()
		for row in self.rows:
			w = row.get_value()
			if w <= 0.0:
				continue
			delta = self.deltas.get(row.name)
			if not delta:
				continue
			for plug, d in delta.items():
				base = self.defaults.get(plug, 0.0)
				pose[plug] = pose.get(plug, base) + d * w
				active_plugs.add(plug)

		# Reset channels that were driven last time but are no longer active.
		for plug in self._last_active_plugs - active_plugs:
			pose[plug] = self.defaults.get(plug, 0.0)

		self._last_active_plugs = active_plugs
		self._apply_pose(pose)

	def _apply_pose(self, pose):
		for plug, val in pose.items():
			utils.set_plug_value(plug, val)

	def zero_all(self):
		for row in self.rows:
			row.set_value(0)
		self.apply_blend()

	# ====================================================================
	# SELECTION (multi-select for delete)
	# ====================================================================

	def handle_click(self, row):
		mods = QtWidgets.QApplication.keyboardModifiers()

		if mods == QtCore.Qt.ShiftModifier and self.last_clicked:
			start = self.rows.index(self.last_clicked)
			end = self.rows.index(row)
			for r in self.rows[min(start, end):max(start, end) + 1]:
				r.set_selected(True)
		elif mods == QtCore.Qt.ControlModifier:
			row.set_selected(not row.selected)
		else:
			for r in self.rows:
				r.set_selected(False)
			row.set_selected(True)

		self.last_clicked = row

	def get_selected(self):
		return [r for r in self.rows if r.selected]

	# ====================================================================
	# DELETE
	# ====================================================================

	def delete_selected(self):
		selected = self.get_selected()
		if not selected:
			cmds.warning("ArkKit: no expressions selected to delete.")
			return

		for row in selected:
			data_node.delete_expression(row.name)
			self.deltas.pop(row.name, None)
			row.set_has_data(False)
			row.set_value(0)
			row.set_selected(False)

		self.apply_blend()
		print("[ArkKit] Deleted {} expression(s).".format(len(selected)))
		self.update_status_label()


	# ====================================================================
	# DELETE ARK NODE
	# ====================================================================

	def delete_ark_nodes(self):
		if self.recording is not None:
			cmds.warning("ArkKit: stop recording before deleting ArkKit nodes.")
			return

		selected_geos = utils.selected_meshes()
		if not selected_geos:
			cmds.warning("ArkKit: select at least one mesh with an ArkKit blendshape node.")
			return

		deleted = 0
		cmds.undoInfo(openChunk=True)
		try:
			for geo in selected_geos:
				if not cmds.objExists(geo):
					continue
				bs = self._find_arkkit_bs(geo)
				if not bs:
					continue
				try:
					cmds.delete(bs)
					deleted += 1
				except Exception:
					pass
		finally:
			cmds.undoInfo(closeChunk=True)

		if deleted:
			msg = "ArkKit: deleted {} ArkKit node(s).".format(deleted)
			print("[ArkKit] " + msg)
			cmds.inViewMessage(amg=msg, pos="midCenter", fade=True)
		else:
			cmds.warning("ArkKit: no ArkKit blendshape nodes found on the selected meshes.")

	def delete_empty_targets(self):
		if self.recording is not None:
			cmds.warning("ArkKit: stop recording before deleting empty targets.")
			return

		selected_geos = utils.selected_meshes()
		if not selected_geos:
			cmds.warning("ArkKit: select at least one mesh with an ArkKit blendshape node.")
			return

		removed_total = 0
		updated_nodes = []
		failed = []

		cmds.undoInfo(openChunk=True)
		try:
			for geo in selected_geos:
				if not cmds.objExists(geo):
					failed.append(geo + " (missing)")
					continue
				result = self._cleanup_blendshape_empty_targets(mesh=geo)
				if result is None:
					failed.append(geo)
					continue
				new_bs, removed = result
				if removed:
					removed_total += len(removed)
					updated_nodes.append(new_bs)
		finally:
			cmds.undoInfo(closeChunk=True)

		if removed_total:
			msg = "ArkKit: deleted {} empty target(s).".format(removed_total)
			print("[ArkKit] " + msg)
			if updated_nodes:
				print("[ArkKit] Updated blendShape node(s): " + ", ".join(updated_nodes))
			cmds.inViewMessage(amg=msg, pos="midCenter", fade=True)
		else:
			cmds.warning("ArkKit: no empty blendshape targets found on the selected meshes.")

		if failed:
			cmds.warning("ArkKit: skipped " + ", ".join(failed))

	# ====================================================================
	# MIRROR / SYMMETRIZE
	# ====================================================================

	def snapshot_mirror(self):
		if not self.defaults:
			cmds.warning("ArkKit: press 'Save Defaults' before snapshotting mirror.")
			return
		if not self.controls:
			cmds.warning("ArkKit: no controls to snapshot.")
			return

		table = mirror.snapshot(self.controls, self.defaults, config.MIRROR_AXIS)
		data_node.write_mirror(table)
		self.mirror_signs = table

		# The snapshot left the rig at its neutral defaults; reflect that.
		for row in self.rows:
			row.set_value(0)
		self._last_active_plugs = set()

		count = len([k for k in table if k != "__meta__"])
		msg = "ArkKit: snapshotted mirror signs for {} control(s) (axis {}).".format(
			count, config.MIRROR_AXIS
		)
		print("[ArkKit] " + msg)
		cmds.inViewMessage(amg=msg, pos="midCenter", fade=True)
		self.update_status_label()

	def mirror_to_opposite(self):
		if self.recording is not None:
			cmds.warning("ArkKit: stop recording before mirroring.")
			return

		selected = self.get_selected()
		if not selected:
			cmds.warning("ArkKit: select the expression(s) to mirror.")
			return

		done, skipped = [], []
		for row in selected:
			delta = self.deltas.get(row.name)
			if not delta:
				skipped.append("{} (empty)".format(row.name))
				continue
			opp = config.mirror_expression_name(row.name)
			if not opp:
				skipped.append("{} (center — no opposite)".format(row.name))
				continue

			new_delta = mirror.mirror_delta(delta, self.mirror_signs)
			existed = data_node.has_expression(opp)
			data_node.write_expression(opp, new_delta)
			self.deltas[opp] = new_delta
			opp_row = self.rows_by_name.get(opp)
			if opp_row:
				opp_row.set_has_data(bool(new_delta))
			done.append("{} → {}{}".format(row.name, opp, " (overwrote)" if existed else ""))

		if done:
			print("[ArkKit] Mirrored: " + "; ".join(done))
		if skipped:
			cmds.warning("ArkKit: skipped " + "; ".join(skipped))
		if not data_node.has_mirror():
			cmds.warning("ArkKit: no mirror snapshot yet — used identity signs "
						 "(transform flips may be wrong). Run 'Snapshot Mirror'.")
		cmds.inViewMessage(amg="ArkKit: mirrored {} expression(s).".format(len(done)),
						   pos="midCenter", fade=True)
		self.update_status_label()

	def symmetrize(self):
		source_side = "L" if self.sym_dir.currentIndex() == 0 else "R"

		if not data_node.has_mirror():
			cmds.warning("ArkKit: no mirror snapshot — symmetrize uses identity "
						 "signs (transform flips may be wrong). Run 'Snapshot Mirror'.")

		# While recording, symmetrize the LIVE rig so the captured pose is symmetric.
		if self.recording is not None:
			if not self.defaults:
				cmds.warning("ArkKit: no defaults captured.")
				return
			count = mirror.symmetrize_live(self.defaults, self.mirror_signs, source_side)
			msg = "ArkKit: symmetrized live pose ({}→{}, {} channels).".format(
				source_side, "R" if source_side == "L" else "L", count)
			print("[ArkKit] " + msg)
			cmds.inViewMessage(amg=msg, pos="midCenter", fade=True)
			return

		# Otherwise symmetrize the selected recorded expression(s).
		selected = self.get_selected()
		if not selected:
			cmds.warning("ArkKit: select the expression(s) to symmetrize.")
			return

		count = 0
		for row in selected:
			delta = self.deltas.get(row.name)
			if not delta:
				continue
			new_delta = mirror.symmetrize_delta(delta, self.mirror_signs, source_side)
			data_node.write_expression(row.name, new_delta)
			self.deltas[row.name] = new_delta
			row.set_has_data(bool(new_delta))
			count += 1

		self.apply_blend()
		msg = "ArkKit: symmetrized {} expression(s) ({}→{}).".format(
			count, source_side, "R" if source_side == "L" else "L")
		print("[ArkKit] " + msg)
		cmds.inViewMessage(amg=msg, pos="midCenter", fade=True)

	# ====================================================================
	# EXPORT / IMPORT
	# ====================================================================

	def _ensure_export_dir(self):
		"""Create the default exports folder on demand so the dialog opens there."""
		try:
			if self.last_export_dir == config.EXPORTS_DIR and not os.path.isdir(config.EXPORTS_DIR):
				os.makedirs(config.EXPORTS_DIR)
		except Exception:
			pass

	def export_data(self):
		if not data_node.exists():
			cmds.warning("ArkKit: nothing to export — no ArkKit_Data node yet.")
			return

		self._ensure_export_dir()
		result = cmds.fileDialog2(
			fileMode=0, dialogStyle=2, caption="Export ArkKit Data",
			fileFilter="JSON (*.json)",
			startingDirectory=self.last_export_dir.replace(os.sep, "/"),
		)
		if not result:
			return

		path = result[0]
		if not path.lower().endswith(".json"):
			path += ".json"
		self.last_export_dir = os.path.dirname(path)

		data_node.export_json(path)
		print("[ArkKit] Exported to {}".format(path))
		cmds.inViewMessage(amg="ArkKit: exported data.", pos="midCenter", fade=True)

	def import_data(self):
		self._ensure_export_dir()
		result = cmds.fileDialog2(
			fileMode=1, dialogStyle=2, caption="Import ArkKit Data",
			fileFilter="JSON (*.json)",
			startingDirectory=self.last_export_dir.replace(os.sep, "/"),
		)
		if not result:
			return

		path = result[0]
		self.last_export_dir = os.path.dirname(path)

		try:
			data_node.import_json(path)
		except Exception as e:
			cmds.warning("ArkKit: import failed — {}".format(e))
			return

		self.refresh_from_scene()
		print("[ArkKit] Imported from {}".format(path))
		cmds.inViewMessage(amg="ArkKit: imported data.", pos="midCenter", fade=True)

	# ====================================================================
	# GEO LIST
	# ====================================================================

	def _geo_items(self):
		return [self.geo_list.item(i).text() for i in range(self.geo_list.count())]

	def add_selected_geos(self):
		meshes = utils.selected_meshes()
		if not meshes:
			cmds.warning("ArkKit: no mesh transforms selected.")
			return

		existing = set(self._geo_items())
		for geo in meshes:
			if geo not in existing:
				self.geo_list.addItem(geo)
				existing.add(geo)

		data_node.write_geos(self._geo_items())

	def remove_selected_geos(self):
		for item in self.geo_list.selectedItems():
			self.geo_list.takeItem(self.geo_list.row(item))
		data_node.write_geos(self._geo_items())

	# ====================================================================
	# BAKE
	# ====================================================================

	def generate_blendshapes(self):
		geos = self._geo_items()
		if not geos:
			cmds.warning("ArkKit: add at least one target geo.")
			return

		if not self.defaults:
			cmds.warning("ArkKit: no defaults captured — press Set Defaults first.")
			return

		# Which expressions to bake, always in canonical ARKit order.
		if self.include_all_chk.isChecked():
			names_to_bake = list(config.EXPRESSIONS)
		else:
			names_to_bake = [n for n in config.EXPRESSIONS if self.deltas.get(n)]

		if not names_to_bake:
			cmds.warning("ArkKit: no expressions to bake.")
			return

		missing_geos = [g for g in geos if not cmds.objExists(g)]
		if missing_geos:
			cmds.warning("ArkKit: missing geos, aborting: {}".format(", ".join(missing_geos)))
			return

		cmds.undoInfo(openChunk=True)
		try:
			# {geo: [(dupTransform, exprName), ...]} in expression order.
			targets = {g: [] for g in geos}

			for name in names_to_bake:
				# Unrecorded expressions bake as neutral (empty) placeholders.
				delta = self.deltas.get(name, {})
				pose = dict(self.defaults)
				for plug, d in delta.items():
					pose[plug] = self.defaults.get(plug, 0.0) + d
				self._apply_pose(pose)

				for geo in geos:
					# Keep the duplicate under the geo's original parent so it
					# shares the base transform — otherwise blendshape point
					# deltas would be skewed by a transform mismatch.
					dup = cmds.duplicate(geo, name="{}_{}".format(geo.split("|")[-1], name))[0]
					targets[geo].append((dup, name))

			# Return the rig to neutral before wiring targets.
			self._apply_pose(dict(self.defaults))
			for row in self.rows:
				row.set_value(0)

			created = []
			for geo in geos:
				bs = cmds.blendShape(geo, name="{}{}".format(geo.split("|")[-1], config.BLENDSHAPE_SUFFIX))[0]
				for index, (dup, name) in enumerate(targets[geo]):
					cmds.blendShape(bs, edit=True, target=(geo, index, dup, 1.0))
					try:
						cmds.aliasAttr(name, "{}.w[{}]".format(bs, index))
					except Exception:
						pass
					cmds.setAttr("{}.w[{}]".format(bs, index), 0)
					cmds.delete(dup)
				created.append(bs)

		finally:
			cmds.undoInfo(closeChunk=True)

		msg = "ArkKit: baked {} targets onto {} geo(s).".format(len(names_to_bake), len(geos))
		print("[ArkKit] " + msg + " Nodes: " + ", ".join(created))
		cmds.inViewMessage(amg=msg, pos="midCenter", fade=True)

	# ---- update helpers ----

	def _find_arkkit_bs(self, geo, blendshape=None):
		"""Return the ArkKit blendShape node deforming ``geo``, or None.

		Prefers the conventionally-named ``<geo>_ArkKit_BS`` node; otherwise
		falls back to the first blendShape in the geo's history.
		"""
		if blendshape and cmds.objExists(blendshape) and cmds.nodeType(blendshape) == "blendShape":
			return blendshape
		short = geo.split("|")[-1]
		candidate = "{}{}".format(short, config.BLENDSHAPE_SUFFIX)
		if cmds.objExists(candidate) and cmds.nodeType(candidate) == "blendShape":
			return candidate
		for node in (cmds.listHistory(geo) or []):
			if cmds.nodeType(node) == "blendShape":
				return node
		return None

	def _bs_alias_index_map(self, bs):
		"""Return {targetAlias: weightIndex} for a blendShape node."""
		aliases = cmds.aliasAttr(bs, query=True) or []
		result = {}
		for i in range(0, len(aliases) - 1, 2):
			alias, plug = aliases[i], aliases[i + 1]
			m = re.search(r"\[(\d+)\]", plug)
			if m:
				result[alias] = int(m.group(1))
		return result

	def _next_bs_index(self, bs):
		indices = cmds.getAttr(bs + ".weight", multiIndices=True) or []
		return (max(indices) + 1) if indices else 0

	def _replace_target_shape(self, bs, index, dup):
		"""Override an existing target's geometry in place (keeps index + alias).

		Connecting a live mesh to the target's inputGeomTarget makes the
		blendShape recompute its deltas from that mesh; breaking the connection
		bakes those deltas as the new static target.
		"""
		shapes = cmds.listRelatives(dup, shapes=True, noIntermediate=True, fullPath=True) or []
		if not shapes:
			return False
		plug = ("{}.inputTarget[0].inputTargetGroup[{}]"
				".inputTargetItem[6000].inputGeomTarget".format(bs, index))
		src = shapes[0] + ".worldMesh[0]"
		cmds.connectAttr(src, plug, force=True)
		cmds.dgeval(bs + ".outputGeometry[0]")  # force the delta recompute
		cmds.disconnectAttr(src, plug)
		return True

	def _dag(self, node):
		sl = api_om.MSelectionList()
		sl.add(node)
		return sl.getDagPath(0)

	def _mesh_shape(self, node):
		if not cmds.objExists(node):
			return None
		if cmds.nodeType(node) == "mesh":
			return node
		for shape in (cmds.listRelatives(node, s=True, ni=True, f=True) or []):
			if cmds.nodeType(shape) == "mesh":
				return shape
		return None

	def _mesh_xform(self, node):
		if not cmds.objExists(node):
			return None
		if cmds.nodeType(node) == "transform":
			return node
		parents = cmds.listRelatives(node, p=True, f=True) or []
		return parents[0] if parents else None

	def _points_world(self, mesh_shape):
		fn = api_om.MFnMesh(self._dag(mesh_shape))
		points = fn.getPoints(api_om.MSpace.kWorld)
		return [(p.x, p.y, p.z) for p in points]

	def _weight_indices(self, bs):
		return sorted(set(cmds.getAttr(bs + ".weight", mi=True) or []))

	def _set_all_weights(self, bs, value):
		for index in self._weight_indices(bs):
			try:
				cmds.setAttr("{}.w[{}]".format(bs, index), value)
			except Exception:
				pass

	def _save_weights(self, bs):
		values = {}
		for index in self._weight_indices(bs):
			try:
				values[index] = cmds.getAttr("{}.w[{}]".format(bs, index))
			except Exception:
				values[index] = 0.0
		return values

	def _alias_map(self, bs):
		aliases = cmds.aliasAttr(bs, q=True) or []
		result = {}
		for i in range(0, len(aliases) - 1, 2):
			alias = aliases[i]
			plug = aliases[i + 1]
			match = re.search(r"\[(\d+)\]", plug)
			if match:
				result[int(match.group(1))] = alias
		return result

	def _capture_weight_inputs(self, bs):
		source_map = {}
		for index in self._weight_indices(bs):
			weight_plug = "{}.weight[{}]".format(bs, index)
			source = cmds.listConnections(weight_plug, s=True, d=False, p=True) or []
			if source:
				source_map[index] = source[0]
		return source_map

	def _deformer_neighbors(self, mesh, target_deformer):
		history = cmds.listHistory(mesh, pruneDagObjects=True) or []
		def_nodes = [node for node in history if cmds.nodeType(node) in (
			"blendShape", "skinCluster", "cluster", "ffd", "nonLinear", "wire",
			"sculpt", "deltaMush", "wrap", "lattice", "shrinkWrap", "tweak"
		)]
		if target_deformer not in def_nodes:
			return None, None
		index = def_nodes.index(target_deformer)
		prev_def = def_nodes[index - 1] if index > 0 else None
		next_def = def_nodes[index + 1] if index + 1 < len(def_nodes) else None
		return prev_def, next_def

	def _is_non_deforming(self, shape, bs, index, base_points, tolerance):
		self._set_all_weights(bs, 0.0)
		cmds.setAttr("{}.w[{}]".format(bs, index), 1.0)
		try:
			cmds.dgeval(bs + ".outputGeometry[0]")
		except Exception:
			pass
		current = self._points_world(shape)
		if len(current) != len(base_points):
			return False
		for base_point, current_point in zip(base_points, current):
			if (abs(base_point[0] - current_point[0]) > tolerance or
				abs(base_point[1] - current_point[1]) > tolerance or
				abs(base_point[2] - current_point[2]) > tolerance):
				return False
		return True

	def _capture_target_mesh(self, mesh, bs, index, alias):
		self._set_all_weights(bs, 0.0)
		cmds.setAttr("{}.w[{}]".format(bs, index), 1.0)
		try:
			cmds.dgeval(bs + ".outputGeometry[0]")
		except Exception:
			pass
		safe = alias.replace(":", "_").replace("|", "_")
		return cmds.duplicate(mesh, rr=True, n="TMP_KEEP_{}".format(safe))[0]

	def _new_index_by_alias(self, bs, alias):
		aliases = cmds.aliasAttr(bs, q=True) or []
		for i in range(0, len(aliases) - 1, 2):
			if aliases[i] == alias:
				plug = aliases[i + 1]
				return int(plug.split("[")[-1].split("]")[0])
		return None

	def _cleanup_blendshape_empty_targets(self, mesh=None, blendshape=None, tolerance=1e-5):
		mesh = self._mesh_xform(mesh) or mesh
		if not mesh:
			selected = utils.selected_meshes()
			mesh = selected[0] if selected else None
		if not mesh:
			cmds.warning("ArkKit: select mesh or pass mesh='name'.")
			return None

		old_bs = self._find_arkkit_bs(mesh, blendshape)
		if not old_bs:
			cmds.warning("ArkKit: no blendShape found.")
			return None

		shape = self._mesh_shape(mesh)
		if not shape:
			cmds.warning("ArkKit: no mesh shape found.")
			return None

		old_name = old_bs
		old_alias = self._alias_map(old_bs)
		old_values = self._save_weights(old_bs)
		old_inputs = self._capture_weight_inputs(old_bs)
		prev_def, next_def = self._deformer_neighbors(mesh, old_bs)

		keep = []
		empty = []
		temp_dups = []

		cmds.undoInfo(openChunk=True)
		try:
			self._set_all_weights(old_bs, 0.0)
			try:
				cmds.dgeval(old_bs + ".outputGeometry[0]")
			except Exception:
				pass
			base_points = self._points_world(shape)

			for index in self._weight_indices(old_bs):
				try:
					if self._is_non_deforming(shape, old_bs, index, base_points, tolerance):
						empty.append(index)
					else:
						keep.append(index)
				except Exception:
					keep.append(index)

			if not keep:
				cmds.warning("ArkKit: all targets detected empty. Abort.")
				return None

			if not empty:
				print("[ArkKit] No empty targets found on {}.".format(mesh))
				return old_bs, []

			for index in keep:
				alias = old_alias.get(index, "target_{}".format(index))
				dup = self._capture_target_mesh(mesh, old_bs, index, alias)
				temp_dups.append((index, alias, dup))

			self._set_all_weights(old_bs, 0.0)
			try:
				cmds.lockNode(old_bs, lock=False)
			except Exception:
				pass
			cmds.delete(old_bs)

			target_meshes = [entry[2] for entry in temp_dups]
			new_bs = cmds.blendShape(target_meshes, mesh, n=old_name)[0]

			try:
				if prev_def and cmds.objExists(prev_def):
					cmds.reorderDeformers(prev_def, new_bs, mesh)
				elif next_def and cmds.objExists(next_def):
					cmds.reorderDeformers(new_bs, next_def, mesh)
			except Exception:
				pass

			for new_index, (_old_index, alias, _dup) in enumerate(temp_dups):
				try:
					cmds.aliasAttr(alias, "{}.weight[{}]".format(new_bs, new_index))
				except Exception:
					pass

			for old_index, alias in old_alias.items():
				if old_index not in keep:
					continue
				new_index = self._new_index_by_alias(new_bs, alias)
				if new_index is None:
					continue

				new_weight = "{}.weight[{}]".format(new_bs, new_index)
				source = old_inputs.get(old_index)
				if source and cmds.objExists(source.split(".")[0]):
					try:
						if not cmds.isConnected(source, new_weight):
							cmds.connectAttr(source, new_weight, force=True)
						continue
					except Exception:
						pass

				try:
					cmds.setAttr(new_weight, old_values.get(old_index, 0.0))
				except Exception:
					pass

			cmds.delete(target_meshes)

			print("Old blendShape:", old_name)
			print("Removed empty indices:", sorted(empty))
			print("Kept indices:", sorted(keep))
			print("New blendShape:", new_bs)
			return new_bs, empty

		finally:
			cmds.undoInfo(closeChunk=True)

	def update_blendshapes(self, invert=False):
		"""Re-bake targets on the EXISTING blendshape node(s) from recorded data.

		invert=False → update only the selected expressions.
		invert=True  → update all recorded expressions EXCEPT the selected ones.
		"""
		if self.recording is not None:
			cmds.warning("ArkKit: stop recording before updating blendshapes.")
			return
		if not self.defaults:
			cmds.warning("ArkKit: no defaults captured — press Savee Defaults first.")
			return

		geos = self._geo_items()
		if not geos:
			cmds.warning("ArkKit: add at least one target geo.")
			return

		selected_names = {r.name for r in self.get_selected()}
		if invert:
			update_names = [n for n in config.EXPRESSIONS
							if self.deltas.get(n) and n not in selected_names]
			scope = "all recorded except selected"
		else:
			update_names = [n for n in config.EXPRESSIONS
							if n in selected_names and self.deltas.get(n)]
			scope = "selected"

		if not update_names:
			cmds.warning("ArkKit: no recorded expressions to update for the '{}' scope."
						 .format(scope))
			return

		# Resolve the existing ArkKit blendShape node per geo.
		bs_for, no_bs = {}, []
		for geo in geos:
			if not cmds.objExists(geo):
				no_bs.append(geo + " (missing)")
				continue
			bs = self._find_arkkit_bs(geo)
			if bs:
				bs_for[geo] = bs
			else:
				no_bs.append(geo)

		if not bs_for:
			cmds.warning("ArkKit: no existing blendshape node found on the target "
						 "geo(s). Use 'Generate Blendshapes' first.")
			return

		cmds.undoInfo(openChunk=True)
		try:
			# Pose per expression, duplicating each geo (that has a bs node).
			work = {geo: [] for geo in bs_for}
			for name in update_names:
				pose = dict(self.defaults)
				for plug, d in self.deltas[name].items():
					pose[plug] = self.defaults.get(plug, 0.0) + d
				self._apply_pose(pose)
				for geo in bs_for:
					dup = cmds.duplicate(
						geo, name="{}_{}_ArkKitUpd".format(geo.split("|")[-1], name))[0]
					work[geo].append((dup, name))

			# Return to neutral before touching the deformers.
			self._apply_pose(dict(self.defaults))
			for row in self.rows:
				row.set_value(0)
			self._last_active_plugs = set()

			replaced = added = 0
			for geo, bs in bs_for.items():
				amap = self._bs_alias_index_map(bs)
				for dup, name in work[geo]:
					if name in amap:
						if self._replace_target_shape(bs, amap[name], dup):
							replaced += 1
					else:
						idx = self._next_bs_index(bs)
						cmds.blendShape(bs, edit=True, target=(geo, idx, dup, 1.0))
						try:
							cmds.aliasAttr(name, "{}.w[{}]".format(bs, idx))
						except Exception:
							pass
						cmds.setAttr("{}.w[{}]".format(bs, idx), 0)
						added += 1
					cmds.delete(dup)
		finally:
			cmds.undoInfo(closeChunk=True)

		msg = ("ArkKit: updated {} expression(s) ({}) on {} geo(s) — "
			   "{} replaced, {} added.".format(
				   len(update_names), scope, len(bs_for), replaced, added))
		print("[ArkKit] " + msg)
		if no_bs:
			cmds.warning("ArkKit: skipped (no existing blendshape node): "
						 + ", ".join(no_bs))
		cmds.inViewMessage(amg=msg, pos="midCenter", fade=True)

	# ====================================================================
	# FILTER / UNDO
	# ====================================================================

	def filter_rows(self):
		text = self.search.text().lower()
		filters = [f.strip() for f in text.split(",") if f.strip()]
		for row in self.rows:
			if not filters or any(f in row.name.lower() for f in filters):
				row.show()
			else:
				row.hide()

	def begin_undo(self):
		cmds.undoInfo(openChunk=True)

	def end_undo(self):
		cmds.undoInfo(closeChunk=True)

	# CLOSE EVENTS _________________________________
	def closeEvent(self, event):
		QtMutantWindow.Qt_Mutant.closeEvent(self, event)


# -------------------------------------------------------------------

if __name__ == "__main__":

	try:
		cArkKitUI.close()  # pylint: disable=E0601
		cArkKitUI.deleteLater()
	except:
		pass
	cArkKitUI = ArkKitUI()
	cArkKitUI.show()

# -------------------------------------------------------------------

'''
#Notes




'''
