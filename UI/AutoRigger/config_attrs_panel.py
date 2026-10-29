'''
Card style view for the block config attrs in the AutoRigger properties panel.

Groups the config attrs in collapsible sections (Connections, Toggles, Choices,
Values, Lists, Text, Code, Help), shows bools as toggle chips, short enums as
segmented buttons, ints as spinbox + slider. Each attr gets a readable label,
the matching line of the block Help as tooltip, and an orange marker when its
value is not the block json default (right click -> Reset to default).
Right click also lists the values the preset templates use for that attr
(template_suggestions.json, built by template_suggestions.scan_templates).

The classic view is still in load_autoRigger (_add_classic_attr_row), the
header toggle switches between both (optionVar mutant_attr_panel_style).
'''
try:
	from PySide6 import QtGui, QtCore, QtWidgets
except ImportError:
	from PySide2 import QtGui, QtCore, QtWidgets

from functools import partial
import json
import os
import re

import maya.cmds as cmds

from Mutant_Tools.UI.AutoRigger import config_previews
from Mutant_Tools.UI.AutoRigger import config_update
from Mutant_Tools.UI.AutoRigger import template_suggestions
from Mutant_Tools.Utils.Rigging import block_hooks

STYLE_OPTION_VAR = 'mutant_attr_panel_style'
SECTION_OPTION_VAR = 'mutant_attr_section_{}'

ACCENT = '#5B8FD0'
MODIFIED = '#E0A030'

# (key, title, collapsed by default)
SECTIONS = [
	# attrs the block lists in DYNAMIC_ATTRS: editing them runs python on the guides right away
	('dynamic', 'Dynamic', False),
	('connections', 'Connections', False),
	('toggles', 'Toggles', False),
	('choices', 'Choices', False),
	('values', 'Values', False),
	('lists', 'Lists', False),
	('text', 'Text && Paths', False),
	('code', 'Code', False),
	('help', 'Help', True),
]

SKIP_ATTRS = ('precode', 'postcode', 'MutantBackup', 'Build_Command', 'Import_Command')
# maya attr type -> block json key suffix
KIND_BY_TYPE = {'string': 'string', 'enum': 'enum', 'long': 'float', 'bool': 'bool'}
NUMERIC_TYPES = ('long', 'short', 'byte', 'double', 'float', 'doubleLinear', 'doubleAngle')

PANEL_QSS = '''
QFrame#attrSection { background: rgba(255,255,255,0.025); border: 1px solid rgba(255,255,255,0.06); border-radius: 5px; }
QToolButton#attrSectionHeader { border: none; background: transparent; color: #DDDDDD; font-weight: bold; text-align: left; padding: 4px 2px; }
QToolButton#attrSectionHeader:hover { color: #FFFFFF; }
QLabel#attrSectionCount { color: #8A8A8A; padding-right: 4px; }
QFrame#attrRow { background: transparent; border: none; border-radius: 3px; }
QFrame#attrRow:hover { background: rgba(255,255,255,0.04); }
QLabel#attrLabel { color: #C8C8C8; }
QLabel#attrModifiedSummary { color: ''' + MODIFIED + '''; }
QPushButton#attrChip { background: rgba(255,255,255,0.05); color: #9A9A9A; border: 1px solid rgba(255,255,255,0.08); border-radius: 11px; padding: 3px 10px; text-align: left; }
QPushButton#attrChip:hover { border-color: rgba(255,255,255,0.25); }
QPushButton#attrChip:checked { background: ''' + ACCENT + '''; color: white; border-color: ''' + ACCENT + '''; }
QPushButton#attrChip[modified="true"] { border: 1px solid ''' + MODIFIED + '''; }
QPushButton#attrSegment { background: rgba(255,255,255,0.05); color: #A8A8A8; border: 1px solid rgba(255,255,255,0.10); border-radius: 0px; padding: 3px 8px; }
QPushButton#attrSegment[first="true"] { border-top-left-radius: 4px; border-bottom-left-radius: 4px; }
QPushButton#attrSegment[last="true"] { border-top-right-radius: 4px; border-bottom-right-radius: 4px; }
QPushButton#attrSegment:hover { color: white; }
QPushButton#attrSegment:checked { background: ''' + ACCENT + '''; color: white; border-color: ''' + ACCENT + '''; }
QPushButton#attrSmallBtn { padding: 2px 8px; }
QToolButton#attrPicker { background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.10); border-radius: 4px; padding: 2px 6px; text-align: left; }
QToolButton#attrPicker:hover { border-color: rgba(255,255,255,0.25); }
'''

SUGGEST_MENU_QSS = '''
QMenu { padding: 4px; }
QMenu::item { padding: 4px 18px 4px 8px; border-radius: 3px; }
QMenu::item:selected { background: ''' + ACCENT + '''; color: white; }
QMenu::item:disabled { color: #8A8A8A; }
QMenu::separator { height: 1px; background: rgba(255,255,255,0.10); margin: 4px 6px; }
'''
# suggestions shown directly, the rest go in a More submenu
SUGGEST_LIMIT = 15


#-------------------------------------------------------------------
def get_panel_style():
	if cmds.optionVar(exists=STYLE_OPTION_VAR):
		return cmds.optionVar(q=STYLE_OPTION_VAR)
	return 'cards'


def set_panel_style(style):
	cmds.optionVar(sv=(STYLE_OPTION_VAR, style))


def _section_collapsed(key, default):
	var = SECTION_OPTION_VAR.format(key)
	if cmds.optionVar(exists=var):
		return bool(cmds.optionVar(q=var))
	return default


def _set_section_collapsed(key, collapsed):
	cmds.optionVar(iv=(SECTION_OPTION_VAR.format(key), int(collapsed)))


#-------------------------------------------------------------------
def pretty_attr_name(attr, config=''):
	"""SetParent -> Parent, IkCtrlType -> Ik Ctrl Type, PVCtrlType -> PV Ctrl Type."""
	if attr == 'SetControls':
		return 'Controls'
	if attr == 'SetNodeList' and config and cmds.attributeQuery('Build_Command', node=config, exists=True):
		build_cmd = cmds.getAttr('{}.Build_Command'.format(config), asString=True) or ''
		if 'build_surface_constraint_block' in build_cmd:
			return 'Vertices'
	name = attr
	if re.match(r'^Set[A-Z]', name):
		name = name[3:]
	name = name.replace('_', ' ')
	name = re.sub(r'(?<=[a-z0-9])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])', ' ', name)
	return re.sub(r'\s+', ' ', name).strip()


def parse_help_fields(help_text):
	"""Map field name -> description from '- Name: description' lines of the block Help."""
	fields = {}
	if not help_text:
		return fields
	for line in str(help_text).replace('\r', '').split('\n'):
		line = line.strip()
		if not line.startswith('-') or ':' not in line:
			continue
		name, desc = line[1:].split(':', 1)
		name = name.split('(')[0].strip()
		if name and ' ' not in name:
			fields[name] = desc.strip()
	return fields


def _attr_section(attr, attr_type):
	if attr == 'Help':
		return 'help'
	if attr == 'Code':
		return 'code'
	if attr_type == 'bool':
		return 'toggles'
	if attr_type == 'enum':
		return 'choices'
	if attr_type in NUMERIC_TYPES:
		return 'values'
	if attr_type == 'string':
		if 'List' in attr:
			return 'lists'
		if 'Set' in attr:
			return 'connections'
		return 'text'
	return None


#-------------------------------------------------------------------
def get_json_defaults(ui, block, config):
	"""Attr name -> default string from the json of the block version in use."""
	try:
		sorted_versions, versions_dict = ui.get_block_versions(block)
	except Exception:
		return {}
	if not versions_dict:
		return {}
	import_cmd = cmds.getAttr('{}.Import_Command'.format(config)) or ''
	current = None
	match = re.search(r'import\s+(\w+)', import_cmd)
	if match:
		v_match = re.search(r'_(v\d+)$', match.group(1))
		current = v_match.group(1) if v_match else 'v001'
	if current not in versions_dict:
		current = sorted_versions[0]

	try:
		with open(versions_dict[current]) as f:
			data = json.load(f)
	except Exception:
		data = {}
	defaults = {}
	for key, value in (data.get('attrs') or {}).items():
		if '_' in key:
			defaults[key.rsplit('_', 1)[0]] = value
	return defaults


def _is_modified(attr_type, current, default):
	if default is None:
		return False
	try:
		if attr_type == 'bool':
			return bool(current) != (str(default).strip().lower() == 'true')
		if attr_type == 'enum':
			return int(current) != 0
		if attr_type in NUMERIC_TYPES:
			return abs(float(current) - float(default)) > 1e-6
		if attr_type == 'string':
			return (current or '') != (default or '')
	except Exception:
		return False
	return False


#-------------------------------------------------------------------
class ConfigCardsPanel(QtCore.QObject):

	def __init__(self, ui, block, config, attrs, v_layout):
		super(ConfigCardsPanel, self).__init__(v_layout.parentWidget())
		self.ui = ui
		self.block = block
		self.config = config
		self.attrs = attrs
		self.v_layout = v_layout
		self.defaults = get_json_defaults(ui, block, config)
		help_text = ''
		if cmds.attributeQuery('Help', node=config, exists=True):
			help_text = cmds.getAttr('{}.Help'.format(config)) or ''
		self.help_fields = parse_help_fields(help_text)
		self.dynamic_attrs = block_hooks.get_dynamic_attrs(config)

		self.rows = []          # (widget, section_key, search_text)
		self.sections = {}      # key -> dict(frame, body, layout, header, count)
		self.chips = []         # (chip, search_text)
		self._chip_visible = {}
		self.chip_grid = None
		self.markers = {}       # attr -> callable returning modified bool

		self.build()

	#---------------------------------------------------------------
	def build(self):
		root = QtWidgets.QWidget()
		root.setObjectName('attrCardsRoot')
		root.setStyleSheet(PANEL_QSS)
		root_layout = QtWidgets.QVBoxLayout(root)
		root_layout.setContentsMargins(0, 4, 0, 0)
		root_layout.setSpacing(6)
		self.v_layout.addWidget(root)

		# filter + modified summary
		top_row = QtWidgets.QHBoxLayout()
		self.filter_edit = QtWidgets.QLineEdit()
		self.filter_edit.setPlaceholderText('Filter attrs...')
		self.filter_edit.setClearButtonEnabled(True)
		self.filter_edit.textChanged.connect(self.apply_filter)
		self.modified_label = QtWidgets.QLabel()
		self.modified_label.setObjectName('attrModifiedSummary')
		self.modified_label.setToolTip('Attrs not at the block default. Right click an attr to reset it.')
		top_row.addWidget(self.filter_edit)
		top_row.addWidget(self.modified_label)
		root_layout.addLayout(top_row)

		grouped = dict((key, []) for key, _, _ in SECTIONS)
		for attr in self.attrs:
			if attr in SKIP_ATTRS:
				continue
			edit_attr = '{}.{}'.format(self.config, attr)
			if not cmds.getAttr(edit_attr, settable=True):
				continue
			attr_type = cmds.getAttr(edit_attr, type=True)
			key = 'dynamic' if attr in self.dynamic_attrs else _attr_section(attr, attr_type)
			if key:
				grouped[key].append((attr, attr_type))

		for key, title, collapsed in SECTIONS:
			if not grouped[key]:
				continue
			body_layout = self._add_section(root_layout, key, title, len(grouped[key]), collapsed)
			if key == 'toggles':
				self._build_chips(body_layout, grouped[key])
				continue
			for attr, attr_type in grouped[key]:
				self._build_row(body_layout, key, attr, attr_type)

		self._build_backup_section(root_layout)
		root_layout.addStretch()

		# the window stylesheet sits on an ancestor and wins over the root one,
		# a widget own stylesheet always wins, so theme every panel widget directly
		for widget in [root] + root.findChildren(QtWidgets.QWidget):
			if widget.objectName().startswith('attr'):
				widget.setStyleSheet(PANEL_QSS)
		self.update_modified_summary()

	#---------------------------------------------------------------
	def _add_section(self, parent_layout, key, title, count, collapsed_default):
		frame = QtWidgets.QFrame()
		frame.setObjectName('attrSection')
		frame_layout = QtWidgets.QVBoxLayout(frame)
		frame_layout.setContentsMargins(6, 2, 6, 6)
		frame_layout.setSpacing(2)

		header_row = QtWidgets.QHBoxLayout()
		header = QtWidgets.QToolButton()
		header.setObjectName('attrSectionHeader')
		header.setText(title)
		header.setCheckable(True)
		header.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
		header.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
		header.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
		count_label = QtWidgets.QLabel(str(count))
		count_label.setObjectName('attrSectionCount')
		header_row.addWidget(header)
		header_row.addWidget(count_label)
		frame_layout.addLayout(header_row)

		body = QtWidgets.QWidget()
		body_layout = QtWidgets.QVBoxLayout(body)
		body_layout.setContentsMargins(2, 0, 2, 2)
		body_layout.setSpacing(2)
		frame_layout.addWidget(body)

		collapsed = _section_collapsed(key, collapsed_default)

		def set_open(is_open, store=True):
			body.setVisible(is_open)
			header.setArrowType(QtCore.Qt.DownArrow if is_open else QtCore.Qt.RightArrow)
			header.blockSignals(True)
			header.setChecked(is_open)
			header.blockSignals(False)
			if store:
				_set_section_collapsed(key, not is_open)

		header.toggled.connect(set_open)
		set_open(not collapsed, store=False)

		parent_layout.addWidget(frame)
		self.sections[key] = dict(frame=frame, body=body, layout=body_layout, header=header,
								count=count_label, set_open=set_open, total=count,
								collapsed_default=collapsed_default)
		return body_layout

	#---------------------------------------------------------------
	def _tooltip(self, attr):
		desc = self.help_fields.get(attr) or self.help_fields.get(pretty_attr_name(attr).replace(' ', ''))
		tip = '<b>{}</b>'.format(attr)
		if desc:
			tip += '<br>{}'.format(desc)
		default = self.defaults.get(attr)
		if default not in (None, '') and attr not in ('Help', 'Code'):
			shown = default.split(':')[0] if ':' in str(default) else default
			tip += '<br><span style="color:#8A8A8A;">Default: {}</span>'.format(shown)
		return tip

	def _search_text(self, attr):
		return ' '.join([attr, pretty_attr_name(attr), self.help_fields.get(attr, '')]).lower()

	def _current(self, attr):
		return cmds.getAttr('{}.{}'.format(self.config, attr))

	def _attr_modified(self, attr, attr_type):
		return _is_modified(attr_type, self._current(attr), self.defaults.get(attr))

	#---------------------------------------------------------------
	def _make_row(self, section_key, attr, attr_type):
		row = QtWidgets.QFrame()
		row.setObjectName('attrRow')
		row_layout = QtWidgets.QHBoxLayout(row)
		row_layout.setContentsMargins(0, 2, 4, 2)
		row_layout.setSpacing(6)

		marker = QtWidgets.QFrame()
		marker.setFixedWidth(3)
		row_layout.addWidget(marker)

		label = QtWidgets.QLabel(pretty_attr_name(attr, self.config))
		label.setObjectName('attrLabel')
		label.setFixedWidth(110)
		label.setToolTip(self._tooltip(attr))
		row_layout.addWidget(label)

		def refresh_marker():
			modified = self._attr_modified(attr, attr_type)
			marker.setStyleSheet('background: {}; border-radius: 1px;'.format(MODIFIED if modified else 'transparent'))
			marker.setToolTip('Changed from default' if modified else '')
			return modified

		self.markers[attr] = refresh_marker
		refresh_marker()

		self._add_context_menu(row, attr, attr_type)
		self.rows.append((row, section_key, self._search_text(attr)))
		return row, row_layout

	def _changed(self, attr):
		marker = self.markers.get(attr)
		if marker:
			marker()
		self.update_modified_summary()

	#---------------------------------------------------------------
	def _build_row(self, layout, section_key, attr, attr_type):
		edit_attr = '{}.{}'.format(self.config, attr)

		if section_key in ('lists', 'code'):
			# complex widgets: reuse the classic builders inside the card
			holder = QtWidgets.QWidget()
			holder_layout = QtWidgets.QVBoxLayout(holder)
			holder_layout.setContentsMargins(0, 0, 0, 0)
			self.ui._add_classic_attr_row(holder_layout, self.config, attr, separator=False,
										  label_text=pretty_attr_name(attr, self.config))
			holder.setToolTip(self._tooltip(attr))
			if section_key == 'lists':
				self._add_context_menu(holder, attr, attr_type)
			layout.addWidget(holder)
			self.rows.append((holder, section_key, self._search_text(attr)))
			return

		if section_key == 'help':
			browser = QtWidgets.QTextBrowser()
			browser.setOpenExternalLinks(True)
			browser.setReadOnly(True)
			browser.setMinimumHeight(180)
			browser.setFrameShape(QtWidgets.QFrame.NoFrame)
			browser.setStyleSheet('background: transparent;')
			browser.setHtml(self.ui._help_html(self._current(attr)))
			layout.addWidget(browser)
			self.rows.append((browser, section_key, 'help'))
			return

		row, row_layout = self._make_row(section_key, attr, attr_type)

		if attr_type == 'enum':
			self._build_enum(row_layout, attr, edit_attr)
		elif attr_type == 'bool':
			check = QtWidgets.QCheckBox()
			check.setChecked(bool(self._current(attr)))
			check.toggled.connect(lambda _=None, c=check, ea=edit_attr, a=attr: (self.ui.checkBox_update_attr(c, ea), self._changed(a)))
			row_layout.addWidget(check)
			row_layout.addStretch()
		elif attr_type in NUMERIC_TYPES:
			self._build_number(row_layout, attr, attr_type, edit_attr)
		else:
			self._build_string(row_layout, attr, edit_attr)

		layout.addWidget(row)

	#---------------------------------------------------------------
	def _build_string(self, row_layout, attr, edit_attr):
		line_edit = QtWidgets.QLineEdit(self._current(attr) or '')
		line_edit.textChanged.connect(partial(self.ui.lineEdit_update_attr, line_edit, edit_attr))
		line_edit.textChanged.connect(lambda *_: self._changed(attr))
		self._add_line_edit_menu(line_edit, attr, 'string')
		row_layout.addWidget(line_edit)

		if 'Set' in attr:
			line_edit.setPlaceholderText('pick from scene')
			pick_btn = QtWidgets.QPushButton('Set')
			pick_btn.setObjectName('attrSmallBtn')
			pick_btn.setToolTip('Set the current selection')
			pick_btn.clicked.connect(partial(self.ui.lineEdit_get_selection, line_edit, edit_attr))
			select_btn = QtWidgets.QPushButton()
			select_btn.setFixedSize(22, 22)
			select_btn.setToolTip('Select it in the scene')
			select_btn.setIcon(QtGui.QIcon(os.path.join(self._icons_path(), 'Cursor.png')))
			select_btn.clicked.connect(partial(self.ui.lineEdit_sel_selection, line_edit, edit_attr))
			row_layout.addWidget(pick_btn)
			row_layout.addWidget(select_btn)

		if 'File' in attr or 'Path' in attr:
			browse_btn = QtWidgets.QPushButton('...')
			browse_btn.setObjectName('attrSmallBtn')
			browse_btn.setToolTip('Browse')
			handler = self.ui.lineEdit_get_file if 'File' in attr else self.ui.lineEdit_get_path
			browse_btn.clicked.connect(partial(handler, line_edit, edit_attr))
			row_layout.addWidget(browse_btn)

	def _icons_path(self):
		return os.path.join(config_previews.FOLDER, 'Icons')

	#---------------------------------------------------------------
	def _build_enum(self, row_layout, attr, edit_attr):
		enums = cmds.attributeQuery(attr, node=self.config, listEnum=True)[0].split(':')
		current = self._current(attr)

		def set_index(index, *_):
			self.ui.set_config_attr_with_hook(edit_attr, index)
			self._changed(attr)

		if config_previews.is_curve_enum(attr, enums) or config_previews.is_color_enum(attr, enums):
			self._build_visual_enum(row_layout, attr, edit_attr, enums)
			return

		if len(enums) <= 4 and sum(len(e) for e in enums) <= 30:
			seg_layout = QtWidgets.QHBoxLayout()
			seg_layout.setSpacing(0)
			group = QtWidgets.QButtonGroup(row_layout.parentWidget())
			group.setExclusive(True)
			for index, name in enumerate(enums):
				btn = QtWidgets.QPushButton(name.replace('_', ' '))
				btn.setObjectName('attrSegment')
				btn.setCheckable(True)
				btn.setChecked(index == current)
				btn.setProperty('first', index == 0)
				btn.setProperty('last', index == len(enums) - 1)
				btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
				btn.clicked.connect(partial(set_index, index))
				group.addButton(btn)
				seg_layout.addWidget(btn)
			seg_layout.addStretch()
			row_layout.addLayout(seg_layout, 1)
		else:
			combo = QtWidgets.QComboBox()
			combo.addItems(enums)
			combo.setCurrentIndex(current)
			combo.currentIndexChanged.connect(set_index)
			row_layout.addWidget(combo, 1)

	#---------------------------------------------------------------
	def _build_visual_enum(self, row_layout, attr, edit_attr, enums):
		"""Ctrl shape / color picker with previews, offers every repo curve / color, not only the json ones."""
		is_curve = config_previews.is_curve_enum(attr, enums)
		options = config_previews.extended_options(attr, enums)

		def pixmap(name, size=None):
			if is_curve:
				return config_previews.curve_pixmap(name, size or 36)
			return config_previews.color_pixmap(name, size or 18)

		button = QtWidgets.QToolButton()
		button.setObjectName('attrPicker')
		button.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
		button.setPopupMode(QtWidgets.QToolButton.InstantPopup)
		button.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
		button.setIconSize(QtCore.QSize(22, 22) if is_curve else QtCore.QSize(16, 16))
		button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

		def refresh_button():
			name = cmds.getAttr(edit_attr, asString=True) or ''
			button.setText(name)
			button.setIcon(QtGui.QIcon(pixmap(name, 22 if is_curve else 16)))

		menu = QtWidgets.QMenu(button)
		grid_widget = QtWidgets.QWidget()
		grid = QtWidgets.QGridLayout(grid_widget)
		grid.setContentsMargins(6, 6, 6, 6)
		grid.setSpacing(4)
		columns = 6 if is_curve else 4
		in_json = set(enums)

		def choose(name):
			menu.close()
			current_options = cmds.attributeQuery(attr, node=self.config, listEnum=True)[0].split(':')
			if name not in current_options:
				# repo option the block json did not list yet, appended so the old indices stay the same
				current_options.append(name)
				cmds.addAttr(edit_attr, e=True, enumName=':'.join(current_options))
			self.ui.set_config_attr_with_hook(edit_attr, current_options.index(name))
			refresh_button()
			self._changed(attr)

		for index, name in enumerate(options):
			cell = QtWidgets.QToolButton()
			cell.setAutoRaise(True)
			cell.setText(name)
			cell.setIcon(QtGui.QIcon(pixmap(name)))
			cell.setIconSize(QtCore.QSize(36, 36) if is_curve else QtCore.QSize(18, 18))
			cell.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon if is_curve else QtCore.Qt.ToolButtonTextBesideIcon)
			cell.setFixedWidth(72 if is_curve else 92)
			cell.setToolTip(name if name in in_json else '{} (repo option, not in the block json)'.format(name))
			if name not in in_json:
				cell.setStyleSheet('QToolButton { color: #8A8A8A; }')
			cell.clicked.connect(partial(choose, name))
			grid.addWidget(cell, index // columns, index % columns)

		action = QtWidgets.QWidgetAction(menu)
		action.setDefaultWidget(grid_widget)
		menu.addAction(action)
		button.setMenu(menu)
		refresh_button()
		row_layout.addWidget(button, 1)

	#---------------------------------------------------------------
	def _build_number(self, row_layout, attr, attr_type, edit_attr):
		is_int = attr_type in ('long', 'short', 'byte')
		value = self._current(attr)
		has_min = cmds.attributeQuery(attr, node=self.config, minExists=True)
		has_max = cmds.attributeQuery(attr, node=self.config, maxExists=True)
		attr_min = cmds.attributeQuery(attr, node=self.config, minimum=True)[0] if has_min else 0
		attr_max = cmds.attributeQuery(attr, node=self.config, maximum=True)[0] if has_max else 100

		if is_int:
			spin = QtWidgets.QSpinBox()
			spin.setRange(int(attr_min), 999)
		else:
			spin = QtWidgets.QDoubleSpinBox()
			spin.setDecimals(3)
			spin.setRange(attr_min, 999.0)
		spin.setValue(value)
		spin.setFixedWidth(60)

		# slider works in steps of 1 (ints) or 0.01 (floats)
		scale = 1 if is_int else 100
		slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
		slider.setRange(int(attr_min * scale), int(max(attr_max, value, 20 if is_int else 1) * scale))
		slider.setValue(int(value * scale))

		def apply_value(new_value):
			if has_max and new_value > cmds.attributeQuery(attr, node=self.config, maximum=True)[0]:
				cmds.addAttr(edit_attr, edit=True, max=max(100, new_value))
			cmds.setAttr(edit_attr, new_value)
			self._changed(attr)
			self.ui.queue_attr_hook(edit_attr)

		def on_spin(new_value):
			if new_value * scale > slider.maximum():
				slider.setMaximum(int(new_value * scale))
			slider.blockSignals(True)
			slider.setValue(int(new_value * scale))
			slider.blockSignals(False)
			apply_value(new_value)

		def on_slider(slider_value):
			new_value = slider_value if is_int else slider_value / float(scale)
			spin.blockSignals(True)
			spin.setValue(new_value)
			spin.blockSignals(False)
			apply_value(new_value)

		spin.valueChanged.connect(on_spin)
		slider.valueChanged.connect(on_slider)
		row_layout.addWidget(spin)
		row_layout.addWidget(slider, 1)

	#---------------------------------------------------------------
	def _build_chips(self, layout, attrs):
		grid_widget = QtWidgets.QWidget()
		self.chip_grid = QtWidgets.QGridLayout(grid_widget)
		self.chip_grid.setContentsMargins(0, 2, 0, 2)
		self.chip_grid.setHorizontalSpacing(6)
		self.chip_grid.setVerticalSpacing(6)
		layout.addWidget(grid_widget)

		for attr, attr_type in attrs:
			edit_attr = '{}.{}'.format(self.config, attr)
			chip = QtWidgets.QPushButton(pretty_attr_name(attr, self.config))
			chip.setObjectName('attrChip')
			chip.setCheckable(True)
			chip.setChecked(bool(self._current(attr)))
			chip.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
			chip.setToolTip(self._tooltip(attr))
			chip.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)

			def refresh_marker(c=chip, a=attr, t=attr_type):
				modified = self._attr_modified(a, t)
				c.setProperty('modified', modified)
				c.style().unpolish(c)
				c.style().polish(c)
				return modified

			def on_toggled(state, c=chip, ea=edit_attr, a=attr):
				self.ui.checkBox_update_attr(c, ea)
				self._changed(a)

			chip.toggled.connect(on_toggled)
			self.markers[attr] = refresh_marker
			refresh_marker()
			self._add_context_menu(chip, attr, attr_type)
			self.chips.append((chip, self._search_text(attr)))

		self._relayout_chips()

	def _relayout_chips(self):
		if not self.chip_grid:
			return
		for chip, _ in self.chips:
			self.chip_grid.removeWidget(chip)
		index = 0
		for chip, search in self.chips:
			if not self._chip_visible.get(chip, True):
				continue
			self.chip_grid.addWidget(chip, index // 2, index % 2)
			index += 1

	#---------------------------------------------------------------
	def _add_context_menu(self, widget, attr, attr_type):
		widget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)

		def show_menu(pos):
			menu = QtWidgets.QMenu(widget)
			suggestion_actions = self._add_suggestions_menu(menu, attr, attr_type)
			menu.addSeparator()
			default = self.defaults.get(attr)
			shown = str(default).split(':')[0] if attr_type == 'enum' and default else default
			reset_action = menu.addAction('Use default value ({})'.format(shown) if default not in (None, '') else 'Use default value')
			reset_action.setEnabled(self._attr_modified(attr, attr_type))
			backup_entry = config_update.read_backup(self.config).get(attr)
			backup_action = None
			if backup_entry:
				backup_action = menu.addAction('Restore backup value ({})'.format(backup_entry.get('value')))
			menu.addSeparator()
			copy_action = menu.addAction('Copy attr name')
			chosen = menu.exec_(widget.mapToGlobal(pos)) if hasattr(menu, 'exec_') else menu.exec(widget.mapToGlobal(pos))
			if chosen in suggestion_actions:
				self.apply_suggestion(attr, attr_type, suggestion_actions[chosen])
			elif chosen == reset_action:
				self.reset_attr(attr, attr_type)
			elif backup_action and chosen == backup_action:
				self.restore_backup(attr, attr_type)
			elif chosen == copy_action:
				QtWidgets.QApplication.clipboard().setText('{}.{}'.format(self.config, attr))

		widget.customContextMenuRequested.connect(show_menu)

	def _add_line_edit_menu(self, line_edit, attr, attr_type):
		"""Keep the normal copy / paste menu of a text field and add the template suggestions on top."""
		line_edit.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)

		def show_menu(pos):
			menu = line_edit.createStandardContextMenu()
			first = menu.actions()[0] if menu.actions() else None
			holder = QtWidgets.QMenu(menu)
			suggestion_actions = self._add_suggestions_menu(holder, attr, attr_type)
			for action in holder.actions():
				menu.insertAction(first, action)
			menu.insertSeparator(first)
			chosen = menu.exec_(line_edit.mapToGlobal(pos)) if hasattr(menu, 'exec_') else menu.exec(line_edit.mapToGlobal(pos))
			if chosen in suggestion_actions:
				self.apply_suggestion(attr, attr_type, suggestion_actions[chosen])

		line_edit.customContextMenuRequested.connect(show_menu)

	#---------------------------------------------------------------
	def _suggestion_label(self, attr_type, value):
		if attr_type == 'bool':
			return 'On' if value else 'Off'
		if attr_type == 'string':
			if value == '':
				return '(empty)'
			text = ' '.join(str(value).split())
			return text if len(text) <= 48 else text[:45] + '...'
		return str(value)

	def _same_value(self, attr, attr_type, value):
		path = '{}.{}'.format(self.config, attr)
		current = cmds.getAttr(path, asString=True) if attr_type == 'enum' else self._current(attr)
		if attr_type == 'bool':
			return bool(current) == bool(value)
		if attr_type in NUMERIC_TYPES:
			try:
				return abs(float(current) - float(value)) < 1e-6
			except (TypeError, ValueError):
				return False
		return (current or '') == (value or '')

	def _add_suggestions_menu(self, menu, attr, attr_type):
		"""'Suggestions from templates' submenu, returns action -> value."""
		actions = {}
		values = template_suggestions.suggestions(self.config, attr)
		total = template_suggestions.template_count()
		sub = menu.addMenu('Suggestions from templates')
		sub.setStyleSheet(SUGGEST_MENU_QSS)
		sub.setToolTipsVisible(True)
		if not values:
			sub.setEnabled(False)
			sub.setTitle('Suggestions from templates (none)')
			return actions

		enums = []
		if attr_type == 'enum':
			enums = cmds.attributeQuery(attr, node=self.config, listEnum=True)[0].split(':')
		is_curve = attr_type == 'enum' and config_previews.is_curve_enum(attr, enums)
		is_color = attr_type == 'enum' and config_previews.is_color_enum(attr, enums)

		header = sub.addAction('{} - used in {} templates'.format(pretty_attr_name(attr), total))
		header.setEnabled(False)
		sub.addSeparator()

		target = sub
		for index, entry in enumerate(values):
			if index == SUGGEST_LIMIT:
				target = sub.addMenu('More ({})'.format(len(values) - SUGGEST_LIMIT))
				target.setStyleSheet(SUGGEST_MENU_QSS)
				target.setToolTipsVisible(True)
			value = entry['value']
			templates = entry['templates']
			# text after the tab shows right aligned like a shortcut
			action = target.addAction('{}\t{}/{}'.format(self._suggestion_label(attr_type, value), len(templates), total))
			action.setCheckable(True)
			action.setChecked(self._same_value(attr, attr_type, value))
			if is_curve:
				action.setIcon(QtGui.QIcon(config_previews.curve_pixmap(str(value), 22)))
			elif is_color:
				action.setIcon(QtGui.QIcon(config_previews.color_pixmap(str(value), 16)))
			tip = '<b>{}</b><br>{}'.format(len(templates), '<br>'.join(templates))
			if attr_type == 'string' and len(str(value)) > 48:
				tip = '{}<hr>{}'.format(str(value)[:400], tip)
			action.setToolTip(tip)
			actions[action] = value
		return actions

	def apply_suggestion(self, attr, attr_type, value):
		edit_attr = '{}.{}'.format(self.config, attr)
		cmds.undoInfo(openChunk=True)
		try:
			if attr_type in NUMERIC_TYPES:
				if cmds.attributeQuery(attr, node=self.config, maxExists=True) and \
						value > cmds.attributeQuery(attr, node=self.config, maximum=True)[0]:
					cmds.addAttr(edit_attr, edit=True, max=max(100, value))
				cmds.setAttr(edit_attr, value)
			elif not config_update.apply_value(self.config, attr, KIND_BY_TYPE.get(attr_type, 'string'), value):
				cmds.warning('Suggestion {} does not fit {}'.format(value, edit_attr))
				return
			block_hooks.run_attr_changed(self.config, attr)
		finally:
			cmds.undoInfo(closeChunk=True)
		self._rebuild_later()

	def reset_attr(self, attr, attr_type):
		edit_attr = '{}.{}'.format(self.config, attr)
		default = self.defaults.get(attr)
		if default is None:
			return
		if attr_type == 'bool':
			self.ui.set_config_attr_with_hook(edit_attr, str(default).strip().lower() == 'true')
		elif attr_type == 'enum':
			self.ui.set_config_attr_with_hook(edit_attr, 0)
		elif attr_type in NUMERIC_TYPES:
			cmds.setAttr(edit_attr, float(default))
		else:
			cmds.setAttr(edit_attr, default, type='string')
		self._rebuild_later()

	def restore_backup(self, attr, attr_type):
		entry = config_update.read_backup(self.config).get(attr)
		if not entry:
			return
		kind = KIND_BY_TYPE.get(attr_type, 'string')
		cmds.undoInfo(openChunk=True)
		try:
			if config_update.apply_value(self.config, attr, kind, entry.get('value')):
				config_update.pop_backup(self.config, attr)
			else:
				cmds.warning('Backup value {} does not fit {}.{}'.format(entry.get('value'), self.config, attr))
		finally:
			cmds.undoInfo(closeChunk=True)
		self._rebuild_later()

	def clear_backup(self):
		answer = cmds.confirmDialog(title='Clear Backup', message='Delete the backed up values of {}?'.format(self.block),
									button=['Delete', 'Cancel'], defaultButton='Cancel', cancelButton='Cancel', dismissString='Cancel')
		if answer != 'Delete':
			return
		config_update.write_backup(self.config, {})
		self._rebuild_later()

	def _rebuild_later(self):
		# rebuild on the next tick, the sender widget lives in this panel
		block = self.block
		QtCore.QTimer.singleShot(0, lambda: self.ui.create_properties_layout(block, scroll_to_block=False))

	#---------------------------------------------------------------
	def _build_backup_section(self, parent_layout):
		backup = config_update.read_backup(self.config)
		if not backup:
			return
		body_layout = self._add_section(parent_layout, 'backup', 'Backup', len(backup), True)
		info = QtWidgets.QLabel('Values kept from other versions of this block. They come back when an attr '
								'with the same name exists again.')
		info.setWordWrap(True)
		info.setStyleSheet('color: #8A8A8A;')
		body_layout.addWidget(info)
		for attr in sorted(backup):
			value = backup[attr].get('value')
			text = '{}  =  {}'.format(pretty_attr_name(attr), value if value not in ('', None) else '""')
			label = QtWidgets.QLabel(text)
			label.setToolTip('{} ({})'.format(attr, backup[attr].get('type', '')))
			label.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse)
			body_layout.addWidget(label)
			self.rows.append((label, 'backup', self._search_text(attr)))
		clear_btn = QtWidgets.QPushButton('Clear Backup')
		clear_btn.setObjectName('attrSmallBtn')
		clear_btn.clicked.connect(self.clear_backup)
		body_layout.addWidget(clear_btn, 0, QtCore.Qt.AlignRight)

	#---------------------------------------------------------------
	def update_modified_summary(self):
		count = 0
		for attr, marker in self.markers.items():
			try:
				if self._attr_modified(attr, cmds.getAttr('{}.{}'.format(self.config, attr), type=True)):
					count += 1
			except Exception:
				pass
		self.modified_label.setText('{} changed'.format(count) if count else '')

	def apply_filter(self, text):
		text = text.strip().lower()
		visible = dict((key, 0) for key in self.sections)
		for widget, key, search in self.rows:
			show = not text or text in search
			widget.setVisible(show)
			if show:
				visible[key] += 1
		for chip, search in self.chips:
			show = not text or text in search
			chip.setVisible(show)
			self._chip_visible[chip] = show
			if show:
				visible['toggles'] = visible.get('toggles', 0) + 1
		self._relayout_chips()

		for key, section in self.sections.items():
			section['frame'].setVisible(visible.get(key, 0) > 0)
			if text:
				section['count'].setText('{}/{}'.format(visible.get(key, 0), section['total']))
				section['body'].setVisible(True)
				section['header'].setArrowType(QtCore.Qt.DownArrow)
			else:
				section['count'].setText(str(section['total']))
				section['set_open'](not _section_collapsed(key, section['collapsed_default']), store=False)


#-------------------------------------------------------------------
DIFF_STYLE = {
	'added': ('+', '#7CC77C'),
	'removed': ('-', '#E07070'),
	'changed': ('~', MODIFIED),
	'info': ('i', '#9CC7FF'),
}


DIFF_BROWSER_QSS = 'QTextBrowser { background: #2B2B2B; border: 1px solid #555555; border-radius: 3px; }'


def diff_html(rows, title=''):
	"""HTML list of config_update.diff_modules rows."""
	import html as html_lib
	parts = ['<html><body style="font-family: Segoe UI, Arial; font-size: 12px; color: #DDDDDD;">']
	if title:
		parts.append('<p style="margin:0 0 6px 0;"><b>{}</b></p>'.format(html_lib.escape(title)))
	if not rows:
		parts.append('<p style="color:#8A8A8A;">No differences in the block attrs.</p>')
	for kind, attr, text in rows:
		sign, color = DIFF_STYLE.get(kind, ('', '#DDDDDD'))
		parts.append('<p style="margin:0 0 4px 0;"><span style="color:{0}; font-weight:bold;">{1}</span> '
					 '<b>{2}</b> <span style="color:#AAAAAA;">{3}</span></p>'.format(
			color, sign, html_lib.escape(pretty_attr_name(attr) if kind != 'info' else attr), html_lib.escape(str(text))))
	parts.append('</body></html>')
	return ''.join(parts)


def _read_json(path):
	try:
		with open(path) as f:
			return json.load(f)
	except Exception:
		return {}


class VersionDiffDialog(QtWidgets.QDialog):
	"""Compare two versions of a block json, and what happens to the values of this block."""

	def __init__(self, parent, block, config, versions_dict, from_version, to_version=None):
		super(VersionDiffDialog, self).__init__(parent)
		self.setWindowTitle('{} versions'.format(block))
		self.resize(460, 380)
		self.config = config
		self.versions_dict = versions_dict
		versions = sorted(versions_dict)

		layout = QtWidgets.QVBoxLayout(self)
		row = QtWidgets.QHBoxLayout()
		self.from_box = QtWidgets.QComboBox()
		self.to_box = QtWidgets.QComboBox()
		for box in (self.from_box, self.to_box):
			for v in versions:
				box.addItem(v + ('  (current)' if v == from_version else ''), v)
		self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
		current_index = versions.index(from_version) if from_version in versions else 0
		target = to_version if to_version in versions else versions[-1]
		target_index = versions.index(target)
		if target_index == current_index:
			# already on the latest: show what this version changed from the one before
			if current_index > 0:
				current_index -= 1
			elif len(versions) > 1:
				target_index = 1
		self.from_box.setCurrentIndex(current_index)
		self.to_box.setCurrentIndex(target_index)
		row.addWidget(QtWidgets.QLabel('From'))
		row.addWidget(self.from_box, 1)
		row.addWidget(QtWidgets.QLabel('To'))
		row.addWidget(self.to_box, 1)
		layout.addLayout(row)

		self.browser = QtWidgets.QTextBrowser()
		self.browser.setStyleSheet(DIFF_BROWSER_QSS)
		layout.addWidget(self.browser, 1)
		close_btn = QtWidgets.QPushButton('Close')
		close_btn.clicked.connect(self.close)
		layout.addWidget(close_btn, 0, QtCore.Qt.AlignRight)

		self.from_box.currentIndexChanged.connect(self.refresh)
		self.to_box.currentIndexChanged.connect(self.refresh)
		self.refresh()

	def refresh(self, *args):
		old_v = self.from_box.currentData()
		new_v = self.to_box.currentData()
		rows = config_update.diff_modules(_read_json(self.versions_dict[old_v]),
										  _read_json(self.versions_dict[new_v]), self.config)
		self.browser.setHtml(diff_html(rows, '{} -> {}'.format(old_v, new_v)))


def build_cards(ui, block, config, attrs, v_layout):
	"""Entry point used by load_autoRigger.create_properties_layout."""
	return ConfigCardsPanel(ui, block, config, attrs, v_layout)
