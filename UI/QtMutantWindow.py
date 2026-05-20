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
www.mutanttools.com
author:  Esteban Rodriguez <info@renderdemartes.com>

'''
import sys
import os
import platform
import  json

from maya import cmds
from maya import mel
from pathlib import Path


try:
    from shiboken6 import wrapInstance
    from PySide6 import QtUiTools
    from PySide6 import QtWidgets
    from PySide6.QtWidgets import *
    from PySide6 import QtGui, QtCore
except: 
    from shiboken2 import wrapInstance #Compatibility pre 2026
    from PySide2 import QtUiTools
    from PySide2 import QtWidgets
    from PySide2.QtWidgets import *
    from PySide2 import QtGui,QtCore

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

HOTKEYS_CONFIG_FILE = os.path.join(FOLDER, 'Config', 'hotkeys.json')


def _default_mutant_hotkeys_config():
    return {
        'set_name': 'Mutant_UI_Hotkeys',
        'source_set': 'Maya_Default',
        'fallback_set': 'Maya_Default',
        'category': 'Mutant Tools',
        'actions': {
            'reset_ctrls_zero': {
                'annotation': 'Mutant reset all *_Ctrl transforms to 0,0,0',
                'command_language': 'mel',
                'command': 'python("import Mutant_Tools.UI.QtMutantWindow as qmw;qmw.reset_mutant_ctrls_to_zero_hotkey_action()")'
            },
            'reset_ctrls_default': {
                'annotation': 'Mutant reset all *_Ctrl transforms to default values',
                'command_language': 'mel',
                'command': 'python("import Mutant_Tools.UI.QtMutantWindow as qmw;qmw.reset_mutant_ctrls_to_default_hotkey_action()")'
            },
            'copy_vertex_weights': {
                'annotation': 'Mutant copy vertex weights',
                'command_language': 'mel',
                'command': 'python("import Mutant_Tools.UI.QtMutantWindow as qmw;qmw.copy_vertex_weights_hotkey_action()")'
            },
            'paste_vertex_weights': {
                'annotation': 'Mutant paste vertex weights',
                'command_language': 'mel',
                'command': 'python("import Mutant_Tools.UI.QtMutantWindow as qmw;qmw.paste_vertex_weights_hotkey_action()")'
            }
        },
        'bindings': [
            {
                'key': 't',
                'shift': False,
                'ctrl': False,
                'alt': False,
                'action': 'reset_ctrls_zero',
                'runtime_command': 'MutantResetCtrlsRuntimeCommand',
                'name_command': 'MutantResetCtrlsNameCommand',
                'description': 'Reset all *_Ctrl transforms to 0,0,0'
            },
            {
                'key': 't',
                'shift': True,
                'ctrl': False,
                'alt': False,
                'action': 'reset_ctrls_default',
                'runtime_command': 'MutantResetCtrlsShiftRuntimeCommand',
                'name_command': 'MutantResetCtrlsShiftNameCommand',
                'description': 'Reset all *_Ctrl transforms to default values'
            }
        ]
    }


def _load_mutant_hotkeys_config():
    config = _default_mutant_hotkeys_config()

    if not os.path.exists(HOTKEYS_CONFIG_FILE):
        return config

    try:
        with open(HOTKEYS_CONFIG_FILE, 'r') as json_file:
            hotkeys_data = json.load(json_file)
    except Exception as e:
        cmds.warning('Mutant hotkeys config could not be read ({}). Using defaults.'.format(e))
        return config

    if not isinstance(hotkeys_data, dict):
        return config

    mutant_hotkeys = hotkeys_data.get('mutant_hotkeys', {})
    if not isinstance(mutant_hotkeys, dict):
        return config

    string_fields = [
        'set_name',
        'source_set',
        'fallback_set',
        'category'
    ]
    for field in string_fields:
        value = mutant_hotkeys.get(field)
        if isinstance(value, str) and value:
            config[field] = value

    actions = mutant_hotkeys.get('actions')
    if isinstance(actions, dict):
        valid_actions = {}
        for action_name, action_data in actions.items():
            if not isinstance(action_name, str) or not action_name:
                continue
            if not isinstance(action_data, dict):
                continue

            command = action_data.get('command')
            if not isinstance(command, str) or not command:
                continue

            valid_actions[action_name] = {
                'annotation': str(action_data.get('annotation', action_name)),
                'command_language': str(action_data.get('command_language', 'mel')),
                'command': command
            }

        if valid_actions:
            config['actions'] = valid_actions

    legacy_command = mutant_hotkeys.get('command')
    if isinstance(legacy_command, str) and legacy_command:
        config['actions']['reset_ctrls_zero'] = {
            'annotation': str(mutant_hotkeys.get('annotation', 'Mutant reset all *_Ctrl transforms')),
            'command_language': str(mutant_hotkeys.get('command_language', 'mel')),
            'command': legacy_command
        }

    bindings = mutant_hotkeys.get('bindings')
    if isinstance(bindings, list):
        valid_bindings = []
        for binding in bindings:
            if not isinstance(binding, dict):
                continue

            key = binding.get('key')
            if not isinstance(key, str) or not key:
                continue

            action = binding.get('action', 'reset_ctrls_zero')
            if not isinstance(action, str) or not action:
                action = 'reset_ctrls_zero'

            runtime_command = binding.get('runtime_command')
            if not isinstance(runtime_command, str):
                runtime_command = ''

            name_command = binding.get('name_command')
            if not isinstance(name_command, str):
                name_command = ''

            description = binding.get('description')
            if not isinstance(description, str):
                description = ''

            valid_bindings.append({
                'key': key,
                'shift': bool(binding.get('shift', False)),
                'ctrl': bool(binding.get('ctrl', False)),
                'alt': bool(binding.get('alt', False)),
                'action': action,
                'runtime_command': runtime_command,
                'name_command': name_command,
                'description': description
            })

        if valid_bindings:
            config['bindings'] = valid_bindings

    return config


MUTANT_HOTKEYS_CONFIG = _load_mutant_hotkeys_config()
MUTANT_HOTKEY_SET = MUTANT_HOTKEYS_CONFIG['set_name']


def _focus_is_text_editable():
    focused_widget = QtWidgets.QApplication.focusWidget()
    if not focused_widget:
        return False

    text_widgets = (
        QtWidgets.QLineEdit,
        QtWidgets.QTextEdit,
        QtWidgets.QPlainTextEdit,
        QtWidgets.QComboBox,
        QtWidgets.QSpinBox,
        QtWidgets.QDoubleSpinBox
    )

    if isinstance(focused_widget, text_widgets):
        return True

    if isinstance(focused_widget, QtWidgets.QAbstractSpinBox):
        return True

    return False


def _set_attr_if_settable(node, attr, value):
    attr_name = '{}.{}'.format(node, attr)
    if not cmds.objExists(attr_name):
        return

    try:
        if not cmds.getAttr(attr_name, settable=True):
            return
    except:
        return

    try:
        cmds.setAttr(attr_name, value)
    except:
        pass


def _get_mutant_ctrl_transforms():
    controls = cmds.ls('*_Ctrl', type='transform') or []
    namespaced_controls = cmds.ls('*:*_Ctrl', type='transform') or []
    return sorted(set(controls + namespaced_controls))


def _set_attr_to_default_if_settable(node, attr):
    attr_name = '{}.{}'.format(node, attr)
    if not cmds.objExists(attr_name):
        return

    try:
        if not cmds.getAttr(attr_name, settable=True):
            return
    except:
        return

    try:
        default_values = cmds.attributeQuery(attr, node=node, listDefault=True)
    except:
        return

    if not default_values:
        return

    try:
        cmds.setAttr(attr_name, default_values[0])
    except:
        pass


def reset_mutant_ctrls_to_zero_hotkey_action():
    if _focus_is_text_editable():
        return

    all_controls = _get_mutant_ctrl_transforms()

    if not all_controls:
        cmds.warning('No *_Ctrl transforms found to reset.')
        return

    for control in all_controls:
        _set_attr_if_settable(control, 'tx', 0)
        _set_attr_if_settable(control, 'ty', 0)
        _set_attr_if_settable(control, 'tz', 0)

        _set_attr_if_settable(control, 'rx', 0)
        _set_attr_if_settable(control, 'ry', 0)
        _set_attr_if_settable(control, 'rz', 0)

        _set_attr_if_settable(control, 'sx', 0)
        _set_attr_if_settable(control, 'sy', 0)
        _set_attr_if_settable(control, 'sz', 0)

    print('Mutant: reset {} controls to 0,0,0 with suffix _Ctrl'.format(len(all_controls)))


def reset_mutant_ctrls_to_default_hotkey_action():
    if _focus_is_text_editable():
        return

    all_controls = _get_mutant_ctrl_transforms()

    if not all_controls:
        cmds.warning('No *_Ctrl transforms found to reset.')
        return

    for control in all_controls:
        _set_attr_to_default_if_settable(control, 'tx')
        _set_attr_to_default_if_settable(control, 'ty')
        _set_attr_to_default_if_settable(control, 'tz')

        _set_attr_to_default_if_settable(control, 'rx')
        _set_attr_to_default_if_settable(control, 'ry')
        _set_attr_to_default_if_settable(control, 'rz')

        _set_attr_to_default_if_settable(control, 'sx')
        _set_attr_to_default_if_settable(control, 'sy')
        _set_attr_to_default_if_settable(control, 'sz')

    print('Mutant: reset {} controls to default values with suffix _Ctrl'.format(len(all_controls)))


def reset_mutant_ctrls_hotkey_action():
    reset_mutant_ctrls_to_zero_hotkey_action()


def _run_vertex_weights_mel_commands(command_list):
    for command in command_list:
        try:
            mel.eval(command)
            return True
        except:
            pass
    return False


def copy_vertex_weights_hotkey_action():
    if _focus_is_text_editable():
        return

    success = _run_vertex_weights_mel_commands([
        'artAttrSkinWeightCopy;',
        'performCopyWeights false;',
        'performCopySkinWeights false;'
    ])

    if success:
        print('Mutant: copied vertex weights')
    else:
        cmds.warning('Mutant: could not copy vertex weights. Open Paint Skin Weights and select vertices.')


def paste_vertex_weights_hotkey_action():
    if _focus_is_text_editable():
        return

    success = _run_vertex_weights_mel_commands([
        'artAttrSkinWeightPaste;',
        'performPasteWeights false;'
    ])

    if success:
        print('Mutant: pasted vertex weights')
    else:
        cmds.warning('Mutant: could not paste vertex weights. Open Paint Skin Weights and select vertices.')


def _ensure_mutant_hotkey_command(runtime_command_name, name_command_name, action_data):
    command_string = action_data.get('command', '')
    annotation = action_data.get('annotation', 'Mutant hotkey command')
    category = MUTANT_HOTKEYS_CONFIG.get('category', 'Mutant Tools')
    command_language = action_data.get('command_language', 'mel')

    if not command_string:
        return False

    try:
        if not cmds.runTimeCommand(runtime_command_name, exists=True):
            cmds.runTimeCommand(runtime_command_name,
                                annotation=annotation,
                                category=category,
                                commandLanguage=command_language,
                                command=command_string)
    except:
        return False

    try:
        if not cmds.nameCommand(name_command_name, exists=True):
            cmds.nameCommand(name_command_name,
                             annotation=annotation,
                             command=runtime_command_name)
            return True
    except:
        try:
            cmds.nameCommand(name_command_name,
                             annotation=annotation,
                             command=runtime_command_name)
            return True
        except:
            return False

    return True


def _hotkey_to_string(binding):
    key_name = str(binding.get('key', '')).upper()
    parts = []
    if binding.get('ctrl', False):
        parts.append('Ctrl')
    if binding.get('shift', False):
        parts.append('Shift')
    if binding.get('alt', False):
        parts.append('Alt')
    parts.append(key_name)
    return '+'.join(parts)


def _print_mutant_hotkeys_mapping():
    print('Mutant hotkeys map:')
    actions = MUTANT_HOTKEYS_CONFIG.get('actions', {})
    for binding in MUTANT_HOTKEYS_CONFIG.get('bindings', []):
        action_name = binding.get('action', 'reset_ctrls_zero')
        action_data = actions.get(action_name, {})
        action_label = binding.get('description') or action_data.get('annotation') or action_name
        print('  {} -> {}'.format(_hotkey_to_string(binding), action_label))


def _ensure_mutant_hotkey_set(source_set):
    source_set_from_config = MUTANT_HOTKEYS_CONFIG.get('source_set')
    if source_set:
        source_to_use = source_set
    else:
        source_to_use = source_set_from_config

    try:
        if not cmds.hotkeySet(MUTANT_HOTKEY_SET, exists=True):
            if source_to_use:
                cmds.hotkeySet(MUTANT_HOTKEY_SET, source=source_to_use)
            else:
                cmds.hotkeySet(MUTANT_HOTKEY_SET)
    except:
        return

    actions = MUTANT_HOTKEYS_CONFIG.get('actions', {})

    for index, binding in enumerate(MUTANT_HOTKEYS_CONFIG.get('bindings', []), start=1):
        key = binding.get('key')
        if not key:
            continue

        action_name = binding.get('action', 'reset_ctrls_zero')
        action_data = actions.get(action_name)
        if not isinstance(action_data, dict):
            continue

        runtime_command_name = binding.get('runtime_command') or 'MutantHotkeyRuntimeCommand{}'.format(index)
        name_command_name = binding.get('name_command') or 'MutantHotkeyNameCommand{}'.format(index)

        if not _ensure_mutant_hotkey_command(runtime_command_name, name_command_name, action_data):
            continue

        hotkey_kwargs = {
            'k': key,
            'name': name_command_name
        }

        if binding.get('shift', False):
            hotkey_kwargs['sht'] = True
        if binding.get('ctrl', False):
            hotkey_kwargs['ctl'] = True
        if binding.get('alt', False):
            hotkey_kwargs['alt'] = True

        try:
            cmds.hotkey(**hotkey_kwargs)
        except:
            pass


def is_mutant_hotkeys_active():
    try:
        return cmds.hotkeySet(query=True, current=True) == MUTANT_HOTKEY_SET
    except:
        return False


def set_mutant_hotkeys_enabled(enabled=True):
    if enabled:
        current_set = None
        try:
            current_set = cmds.hotkeySet(query=True, current=True)
        except:
            current_set = None

        _ensure_mutant_hotkey_set(current_set)

        try:
            cmds.hotkeySet(MUTANT_HOTKEY_SET, edit=True, current=True)
            _print_mutant_hotkeys_mapping()
            return True
        except:
            return False

    fallback_set = MUTANT_HOTKEYS_CONFIG.get('fallback_set', 'Maya_Default')

    try:
        if cmds.hotkeySet(fallback_set, exists=True):
            cmds.hotkeySet(fallback_set, edit=True, current=True)
            return True
    except:
        pass

    cmds.warning('Could not switch to {} hotkeys.'.format(fallback_set))
    return False


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

        self.setMouseTracking(True)
        self.grip_margin = 10
        self._resize_dir = None
        self._resizing = False
        self._window_dragging = False

        self.setObjectName('MainMutantWindow')
        self.setWindowTitle('Mutant Tools')
        self.current_size_mode = 'small'

        self.designer_loader(path = PATH, ui_file = 'QtMutantWindow.ui')

        self._centered_once = False

        self.add_size_grip(layout = self.master_ui.size_grip_layout)
        self.popup_mode = False
        self.make_frameless()
        self.set_margins()
        self.move_to_center_screen()
        self.set_title()
        self.set_stylesheet(widget = self.master_ui)

        # Enable mouse tracking on child widgets so the resize cursor
        # appears when hovering over the window edges.
        self._enable_mouse_tracking_recursive(self.master_ui)
        self.master_ui.installEventFilter(self)

        # Apply saved window mode preference (standard vs frameless)
        self._standard_window_mode = False
        if cmds.optionVar(ex='mutant_standard_window') and cmds.optionVar(q='mutant_standard_window'):
            self.apply_window_mode(standard=True)

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
        if sys.platform == 'darwin':  # macOS
            flags = QtCore.Qt.Window | QtCore.Qt.FramelessWindowHint | QtCore.Qt.CustomizeWindowHint | QtCore.Qt.WindowStaysOnTopHint
        else:  # Windows and Linux
            flags = QtCore.Qt.Window | QtCore.Qt.FramelessWindowHint | QtCore.Qt.CustomizeWindowHint
        self.setWindowFlags(flags)
        return

    def apply_window_mode(self, standard=False):
        """Switch between standard OS window and custom frameless window.

        Args:
            standard (bool): If True, use a normal OS-decorated window.
                If False, use the custom frameless style.
        """
        was_visible = self.isVisible()
        pos = self.pos()
        size = self.size()
        self._standard_window_mode = standard

        if standard:
            # Standard OS window with native title bar
            if sys.platform == 'darwin':
                flags = QtCore.Qt.Window | QtCore.Qt.WindowStaysOnTopHint
            else:
                flags = QtCore.Qt.Window
            title = self.windowTitle() or 'Mutant Tools'
            self.setWindowFlags(flags)
            self.setWindowTitle(title)
            # Hide the custom title bar and size grip since the OS provides them
            self.master_ui.top_frame.hide()
            self.master_ui.size_grip_box.hide()
            self.size_grip.hide()
            self.set_margins(top=0, buttom=0, right=0, left=0)
        else:
            # Custom frameless window
            self.make_frameless()
            self.master_ui.top_frame.show()
            self.master_ui.size_grip_box.show()
            self.size_grip.show()
            self.set_margins()

        if was_visible:
            self.show()
            self.move(pos)
            self.resize(size)

    def toggle_standard_window(self, standard=True):
        """Toggle between standard and frameless window modes.

        Args:
            standard (bool): Whether to enable standard window mode.
        """
        cmds.optionVar(intValue=('mutant_standard_window', int(standard)))
        self.apply_window_mode(standard=standard)

    # ------------------------------------------------

    def move_top_corner(self):
        """Move the main UI to the top left corner of the screen."""

        self.move(25,25)


    def move_to_center_screen(self):
        """Move the main UI to the center of the screen."""
        screen = None

        try:
            # Prefer the screen under mouse cursor (multi-monitor friendly)
            screen = QtGui.QGuiApplication.screenAt(QtGui.QCursor.pos())
        except:
            screen = None

        if not screen:
            app = QtWidgets.QApplication.instance() or QtWidgets.QApplication([])
            screen = app.primaryScreen()

        if not screen:
            return

        available_geo = screen.availableGeometry()

        # Use final window size when visible, otherwise use best hint available
        size = self.size()
        if not self.isVisible() or size.width() <= 0 or size.height() <= 0:
            hint = self.sizeHint()
            if hint.isValid():
                size = hint
            else:
                master_hint = self.master_ui.sizeHint()
                if master_hint.isValid():
                    size = master_hint

        centered_x = available_geo.x() + int((available_geo.width() - size.width()) / 2)
        x = centered_x - int(available_geo.width() / 4)
        y = available_geo.y() + int((available_geo.height() - size.height()) / 2)
        self.move(x, y)

    def showEvent(self, event):
        """Center once after first show so final size is used."""
        QtWidgets.QMainWindow.showEvent(self, event)
        if not self._centered_once:
            self._centered_once = True
            QtCore.QTimer.singleShot(0, self.move_to_center_screen)

    def _enable_mouse_tracking_recursive(self, widget):
        """Enable mouse tracking on a widget and all its children."""
        widget.setMouseTracking(True)
        for child in widget.findChildren(QtWidgets.QWidget):
            child.setMouseTracking(True)

    def eventFilter(self, obj, event):
        """Intercept mouse moves on child widgets to show resize cursors at window edges."""
        if event.type() == QtCore.QEvent.WindowDeactivate:
            self._reset_resize_state()
        elif event.type() == QtCore.QEvent.MouseMove and not self._resizing:
            if self.current_size_mode != 'big' and not getattr(self, 'popup_mode', False):
                # Map the position from the child widget to the main window
                window_pos = self.mapFromGlobal(obj.mapToGlobal(event.pos()))
                direction = self._get_resize_direction(window_pos)
                if direction:
                    self._set_resize_cursor(direction)
                    return False
                else:
                    self.unsetCursor()
                    if obj is not self:
                        obj.unsetCursor()
        return QtWidgets.QMainWindow.eventFilter(self, obj, event)

    def _get_resize_direction(self, pos):
        rect = self.rect()
        x, y, w, h = pos.x(), pos.y(), rect.width(), rect.height()
        m = self.grip_margin
        dir = ""
        if y <= m: dir += "top"
        elif y >= h - m: dir += "bottom"
        if x <= m: dir += ("_" if dir else "") + "left"
        elif x >= w - m: dir += ("_" if dir else "") + "right"
        return dir

    def _set_resize_cursor(self, dir):
        if dir in ['top', 'bottom']: self.setCursor(QtCore.Qt.SizeVerCursor)
        elif dir in ['left', 'right']: self.setCursor(QtCore.Qt.SizeHorCursor)
        elif dir in ['top_left', 'bottom_right']: self.setCursor(QtCore.Qt.SizeFDiagCursor)
        elif dir in ['top_right', 'bottom_left']: self.setCursor(QtCore.Qt.SizeBDiagCursor)
        else: self.unsetCursor()

    def mousePressEvent(self, event):
        """
        Handle mouse press event to grab the current position of the UI.
        """
        self.scale = False
        self.oldPos = event.globalPos()
        self.oldGeom = self.geometry()
        
        dir = self._get_resize_direction(event.pos())
        if dir:
            self._resize_dir = dir
            self._resizing = True
            self._window_dragging = False
        else:
            self._resizing = False
            self._resize_dir = None
            self._window_dragging = True

        if self.popup_mode:
            self.close()

    def mouseDoubleClickEvent(self, event):
        """
        Handle mouse double-click event. Scale with double click
        """
        if event.button() == QtCore.Qt.RightButton:
            self.check_size()

    def mouseMoveEvent(self, event):
        """
        Handle mouse move event to move or resize the frameless UI.
        """
        if self.current_size_mode == 'big':
            return

        if event.buttons() == QtCore.Qt.NoButton:
            if getattr(self, 'popup_mode', False):
                self.unsetCursor()
            else:
                self.scale = False
                dir = self._get_resize_direction(event.pos())
                self._set_resize_cursor(dir)
        elif event.buttons() == QtCore.Qt.LeftButton:
            if self._resizing and self._resize_dir:
                delta = event.globalPos() - self.oldPos
                geom = QtCore.QRect(self.oldGeom)
                d = self._resize_dir
                if 'left' in d:
                    geom.setLeft(geom.left() + delta.x())
                elif 'right' in d:
                    geom.setRight(geom.right() + delta.x())
                if 'top' in d:
                    geom.setTop(geom.top() + delta.y())
                elif 'bottom' in d:
                    geom.setBottom(geom.bottom() + delta.y())
                
                # Fallback to minimal dimensions to avoid weird squashing
                if geom.width() < self.minimumWidth():
                    if 'left' in d: geom.setLeft(geom.right() - self.minimumWidth())
                    else: geom.setRight(geom.left() + self.minimumWidth())
                if geom.height() < self.minimumHeight():
                    if 'top' in d: geom.setTop(geom.bottom() - self.minimumHeight())
                    else: geom.setBottom(geom.top() + self.minimumHeight())
                    
                self.setGeometry(geom)
            elif getattr(self, '_window_dragging', False):
                delta = QtCore.QPoint(event.globalPos() - self.oldPos)
                self.move(self.x() + delta.x(), self.y() + delta.y())
                self.oldPos = event.globalPos()
        elif event.buttons() == QtCore.Qt.RightButton:
            pass

    def _reset_resize_state(self):
        """Clear all resize/drag state and restore the default cursor."""
        self._resizing = False
        self._resize_dir = None
        self.scale = False
        self._window_dragging = False
        self.unsetCursor()

    def mouseReleaseEvent(self, event):
        self._reset_resize_state()

    def leaveEvent(self, event):
        """Reset cursor when the mouse leaves the window."""
        self._reset_resize_state()
        QtWidgets.QMainWindow.leaveEvent(self, event)

    def open_over_mouse(self):
        """Open the UI over the mouse cursor position."""
        self._centered_once = True
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
        QtWidgets.QMainWindow.closeEvent(self, event)
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