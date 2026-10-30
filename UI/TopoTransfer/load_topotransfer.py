"""TopoTransfer window: send meshes to TopoTransfer in one click, get the wrapped shape back.

Opened from the Mutant Tools menu (Mutant-Tools > Misc > TopoTransfer) with the selection: the
first selected mesh is the Base (the topology to keep), a second one the Reference (the shape
to match).

    from Mutant_Tools.UI.TopoTransfer import load_topotransfer
    load_topotransfer.open_window(base='body', reference='scan')

One button exports them and opens TopoTransfer (served by Maya) with both loaded. When you
Export there, the result comes back onto a copy of the Base, `<base>_topoTransfer`: same
vertices, UVs and topology, the new shape. The work is in Utils/TopoTransfer/maya/tt_maya.py.
"""
from __future__ import absolute_import

import os
import sys
import traceback

import maya.cmds as cmds

try:
    from importlib import reload
except ImportError:  # Python 2
    pass

try:
    from PySide6 import QtCore, QtGui, QtWidgets
except ImportError:  # Maya 2024 and older
    from PySide2 import QtCore, QtGui, QtWidgets

from Mutant_Tools.UI import QtMutantWindow
reload(QtMutantWindow)

FOLDER = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TOOLS = os.path.join(FOLDER, 'Utils', 'TopoTransfer', 'maya')
if TOOLS not in sys.path:
    sys.path.insert(0, TOOLS)

import tt_bridge  # noqa: E402
import tt_app  # noqa: E402
import tt_maya  # noqa: E402
for _module in (tt_bridge, tt_app, tt_maya):
    reload(_module)

TITLE = 'TopoTransfer'
ICONS = QtMutantWindow.ICONS_FOLDER
_window = None

HELP = ('<b>Base</b>: the mesh whose topology you keep (vertex order, UVs, faces). <b>Reference</b>: '
        'the shape to match, a scan or a sculpt. Leave it empty to pick the Reference in the browser.'
        '<br><br>Send opens TopoTransfer with both loaded. Align, place landmarks if needed, Wrap, then '
        'Export OBJ: the result comes back here as a copy of the Base, <code>&lt;base&gt;_topoTransfer</code>. '
        'Keep this window open while you work in the browser: it holds the link.')

# Mutant Tools' window colours, as in the Web to Rig and Meta Mutant windows
STYLE = '''
#TopoTransfer QLabel { color: #bbbbbb; }
#TopoTransfer QLabel#Name { color: #e8e8e8; font-size: 15px; font-weight: bold; }
#TopoTransfer QLabel#Meta, #TopoTransfer QLabel#Status { color: #9da1a4; }
#TopoTransfer QLabel#Status[tone="failed"] { color: #e5847f; }
#TopoTransfer QLabel#Status[tone="done"] { color: #7cc48b; }
#TopoTransfer QLabel#Status[tone="wait"] { color: #d9b36c; }
#TopoTransfer QLabel#Field { color: #9da1a4; min-width: 64px; }
#TopoTransfer QFrame#Header { background: #323436; border: none; border-radius: 8px; }
#TopoTransfer QFrame#Setup { background: #2f3133; border: none; border-radius: 8px; }
#TopoTransfer QPushButton#Primary {
    background: #4b6eaf; color: #ffffff; border: none; border-radius: 5px; padding: 8px 16px; font-weight: bold; }
#TopoTransfer QPushButton#Primary:hover { background: #5a7fc4; }
#TopoTransfer QPushButton#Primary:pressed { background: #3f5d94; }
#TopoTransfer QPushButton#Primary:disabled { background: #4a4d50; color: #8a8d90; }
#TopoTransfer QPushButton#Ghost {
    background: transparent; color: #c8c8c8; border: 1px solid #5c5f61; border-radius: 5px; padding: 4px 10px; }
#TopoTransfer QPushButton#Ghost:hover { border-color: #7d8184; color: #ffffff; }
#TopoTransfer QPushButton#Link { background: transparent; border: none; color: #8fb0e6; padding: 2px 4px; }
#TopoTransfer QPushButton#Link:hover { color: #b5cdf3; }
#TopoTransfer QToolButton#HelpTip { border: none; background: transparent; padding: 0px; }
#TopoTransfer QToolButton#HelpTip:hover { background: #55595c; border-radius: 7px; }
#TopoTransfer QLineEdit {
    background: #2b2d2f; color: #d0d0d0; border: 1px solid #55595c; border-radius: 5px;
    padding: 3px 8px; min-height: 22px; }
#TopoTransfer QLineEdit:hover { border-color: #6d7174; }
#TopoTransfer QLineEdit:focus { border-color: #4b6eaf; }
'''


def open_window(base=None, reference=None):
    """Show the window, closing one already open."""
    global _window
    try:
        _window.close()
        _window.deleteLater()
    except Exception:
        pass
    _window = TopoTransferUI(base, reference)
    _window.show()
    return _window


def from_selection():
    """The menu's TopoTransfer: first selected mesh as the Base, a second one as the Reference."""
    meshes = tt_maya.selected_meshes()
    return open_window(meshes[0] if meshes else None, meshes[1] if len(meshes) > 1 else None)


def _icon(name):
    return QtGui.QIcon(os.path.join(ICONS, name))


def _named(widget, name):
    widget.setObjectName(name)
    return widget


def _restyle(widget, **properties):
    for key, value in properties.items():
        widget.setProperty(key, value)
    widget.style().unpolish(widget)
    widget.style().polish(widget)


def _tile(name, size, radius):
    """An icon as a rounded tile, like the Auto Rigger's."""
    scale = QtWidgets.QApplication.instance().devicePixelRatio()
    side = int(size * scale)
    source = QtGui.QPixmap(os.path.join(ICONS, name)).scaled(
        side, side, QtCore.Qt.KeepAspectRatioByExpanding, QtCore.Qt.SmoothTransformation)
    tile = QtGui.QPixmap(side, side)
    tile.fill(QtCore.Qt.transparent)
    painter = QtGui.QPainter(tile)
    painter.setRenderHint(QtGui.QPainter.Antialiasing)
    clip = QtGui.QPainterPath()
    clip.addRoundedRect(0, 0, side, side, radius * scale, radius * scale)
    painter.setClipPath(clip)
    painter.drawPixmap(0, 0, source)
    painter.end()
    tile.setDevicePixelRatio(scale)
    return tile


def _help_button(text):
    """A ? that explains: on hover, and on click (the explanation stays until the next click)."""
    button = _named(QtWidgets.QToolButton(), 'HelpTip')
    button.setIcon(_icon('Help.png'))
    button.setIconSize(QtCore.QSize(14, 14))
    button.setAutoRaise(True)
    button.setCursor(QtCore.Qt.PointingHandCursor)
    button.setToolTip(text)
    button.clicked.connect(lambda *_: QtWidgets.QWhatsThis.showText(
        button.mapToGlobal(QtCore.QPoint(0, button.height())),
        '<div style="max-width: 340px;">{}</div>'.format(button.toolTip()), button))
    return button


class TopoTransferUI(QtMutantWindow.Qt_Mutant):

    def __init__(self, base=None, reference=None):
        super(TopoTransferUI, self).__init__()
        self.setWindowTitle(TITLE)
        self.set_title(TITLE)
        self.resize(420, 360)
        self.link = None
        self.result = None

        body = _named(QtWidgets.QWidget(), 'TopoTransfer')
        body.setStyleSheet(STYLE)
        layout = QtWidgets.QVBoxLayout(body)
        layout.setContentsMargins(6, 6, 6, 6)
        layout.setSpacing(8)
        layout.addWidget(self.header())
        layout.addWidget(self.fields())
        self.send_button = _named(QtWidgets.QPushButton(' Send to TopoTransfer'), 'Primary')
        self.send_button.setIcon(_icon('TopoTransfer.png'))
        self.send_button.setCursor(QtCore.Qt.PointingHandCursor)
        self.send_button.clicked.connect(lambda *_: self.send())
        layout.addWidget(self.send_button)
        self.status = _named(QtWidgets.QLabel(), 'Status')
        self.status.setWordWrap(True)
        layout.addWidget(self.status)
        row = QtWidgets.QHBoxLayout()
        self.select_result = _named(QtWidgets.QPushButton(' Select the result'), 'Link')
        self.select_result.setCursor(QtCore.Qt.PointingHandCursor)
        self.select_result.clicked.connect(lambda *_: self.result and cmds.objExists(self.result) and cmds.select(self.result))
        self.select_result.hide()
        self.reopen = _named(QtWidgets.QPushButton(' Open the browser again'), 'Link')
        self.reopen.setCursor(QtCore.Qt.PointingHandCursor)
        self.reopen.clicked.connect(lambda *_: self.link and QtGui.QDesktopServices.openUrl(QtCore.QUrl(self.link.url)))
        self.reopen.hide()
        row.addWidget(self.select_result)
        row.addWidget(self.reopen)
        row.addStretch(1)
        layout.addLayout(row)
        layout.addStretch(1)
        self.master_ui.mutant_Layout.addWidget(body)

        self.base.setText(base or '')
        self.reference.setText(reference or '')
        self.say('Select the Base mesh (and a Reference), or type their names.' if not base else
                 'Ready: Send exports {} and opens TopoTransfer.'.format(
                     ' and '.join(n for n in (base, reference) if n)))

    # ------------------------------------------------------------------ layout

    def header(self):
        box = _named(QtWidgets.QFrame(), 'Header')
        row = QtWidgets.QHBoxLayout(box)
        row.setContentsMargins(10, 10, 10, 10)
        row.setSpacing(12)
        avatar = QtWidgets.QLabel()
        avatar.setPixmap(_tile('TopoTransfer.png', 44, 10))
        text = QtWidgets.QVBoxLayout()
        text.setSpacing(2)
        top = QtWidgets.QHBoxLayout()
        top.addWidget(_named(QtWidgets.QLabel('TopoTransfer'), 'Name'), 1)
        top.addWidget(_help_button(HELP))
        text.addLayout(top)
        meta = _named(QtWidgets.QLabel('Keep one mesh\'s topology, take another\'s shape.'), 'Meta')
        meta.setWordWrap(True)
        text.addWidget(meta)
        row.addWidget(avatar, 0, QtCore.Qt.AlignTop)
        row.addLayout(text, 1)
        return box

    def fields(self):
        box = _named(QtWidgets.QFrame(), 'Setup')
        grid = QtWidgets.QGridLayout(box)
        grid.setContentsMargins(10, 10, 10, 10)
        grid.setHorizontalSpacing(8)
        grid.setVerticalSpacing(6)
        self.base = self.field(grid, 0, 'Base', 'The mesh whose topology you keep.', 'the topology to keep')
        self.reference = self.field(grid, 1, 'Reference', 'The shape to match. Optional: leave it empty to pick '
                                    'it in the browser.', 'the shape to match (optional)')
        return box

    def field(self, grid, line, label, tip, placeholder):
        name = _named(QtWidgets.QLabel(label), 'Field')
        name.setToolTip(tip)
        edit = QtWidgets.QLineEdit()
        edit.setPlaceholderText(placeholder)
        edit.setToolTip(tip)
        pick = _named(QtWidgets.QPushButton('Use selected'), 'Ghost')
        pick.setCursor(QtCore.Qt.PointingHandCursor)
        pick.clicked.connect(lambda *_: self.use_selected(edit))
        grid.addWidget(name, line, 0)
        grid.addWidget(edit, line, 1)
        grid.addWidget(pick, line, 2)
        return edit

    # ------------------------------------------------------------------ actions

    def say(self, text, tone=''):
        self.status.setText(text)
        _restyle(self.status, tone=tone)

    def use_selected(self, edit):
        meshes = tt_maya.selected_meshes()
        if not meshes:
            self.say('Select a mesh first.', 'failed')
            return
        edit.setText(meshes[0])
        self.say('')

    def send(self):
        base, reference = self.base.text().strip(), self.reference.text().strip()
        for label, node in (('Base', base), ('Reference', reference)):
            if (label == 'Base' or node) and not (node and cmds.objExists(node)):
                self.say('{}: {} is not in the scene.'.format(label, node or 'pick a mesh'), 'failed')
                return
        if base == reference:
            self.say('Base and Reference are the same mesh.', 'failed')
            return
        if self.link:
            self.link.stop()
        self.send_button.setEnabled(False)
        self.say('Exporting...')
        QtWidgets.QApplication.processEvents()
        try:
            self.link = tt_maya.send(base, reference, on_result=self.arrived, on_error=self.failed)
        except Exception as error:
            traceback.print_exc()
            self.say('Could not send: {}'.format(error), 'failed')
            return
        finally:
            self.send_button.setEnabled(True)
        self.send_button.setText(' Send again')
        self.reopen.show()
        self.say('TopoTransfer is open in the browser with {}. Wrap there, then Export OBJ: it comes back here.'
                 .format(' and '.join(n for n in (base, reference) if n)), 'wait')

    def arrived(self, copy):
        self.result = copy
        self.select_result.show()
        self.say('Got it: {} has the wrapped shape (same topology as {}).'.format(copy, self.link.base), 'done')
        cmds.select(copy)
        self.raise_()
        self.activateWindow()

    def failed(self, message):
        self.say('The export came back but could not be applied: {}'.format(message), 'failed')

    def closeEvent(self, event):
        if self.link:
            self.link.stop()
            self.link = None
        super(TopoTransferUI, self).closeEvent(event)
