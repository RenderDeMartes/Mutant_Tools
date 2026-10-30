"""Meta Mutant window: your own head with the MetaHuman rig.

Opened from the Mutant Tools menu (Mutant-Tools > Misc > Meta Mutant), with
the selected mesh as your head:

    from Mutant_Tools.UI.MetaMutant import load_meta_mutant
    load_meta_mutant.open_window(head='myHead')

A numbered path of three steps. 1 exports the MetaHuman head from the DNA and
your head, and opens TopoTransfer (served by Maya itself) with both loaded.
2 happens in the browser: wrap, then Export sends the result back here and the
step lights up done. 3 calibrates the DNA to the wrapped head, builds the rig
and transfers skin and blendshapes to a copy of your head, <head>_MH.

The work itself is in Utils/MetaMutant (mm_controller); this is only its
window. Settings live in the work folder (meta_mutant.json), the last work
folder in an optionVar.
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
PIPELINE = os.path.join(FOLDER, 'Utils', 'MetaMutant')
if PIPELINE not in sys.path:
    sys.path.insert(0, PIPELINE)

import mm_workflow as wf  # noqa: E402  (puts TopoTransfer's maya/ on sys.path too)
import tt_bridge  # noqa: E402
import tt_app  # noqa: E402
import mm_controller  # noqa: E402
import mm_regions  # noqa: E402
import mm_epic  # noqa: E402
for _module in (tt_bridge, tt_app, wf, mm_regions, mm_controller, mm_epic):
    reload(_module)

TITLE = 'Meta Mutant'
ICONS = QtMutantWindow.ICONS_FOLDER
OPTION_VAR = 'metaMutant_workDir'
_window = None

# the same colours as the Web to Rig window: Mutant Tools' own, its selection
# blue for the one thing to do next, green for done and red for stopped
STYLE = '''
#MetaMutant QLabel { color: #bbbbbb; }
#MetaMutant QLabel#Name { color: #e8e8e8; font-size: 15px; font-weight: bold; }
#MetaMutant QLabel#Meta, #MetaMutant QLabel#Text, #MetaMutant QLabel#Status { color: #9da1a4; }
#MetaMutant QLabel#Meta[tone="failed"], #MetaMutant QLabel#Status[tone="failed"] { color: #e5847f; }
#MetaMutant QLabel#Status[tone="done"] { color: #7cc48b; }
#MetaMutant QLabel#Field { color: #9da1a4; min-width: 70px; }
#MetaMutant QLabel#Title { color: #e2e2e2; font-size: 13px; font-weight: bold; }
#MetaMutant QLabel#Title[state="locked"], #MetaMutant QLabel#Text[state="locked"] { color: #6c7073; }
#MetaMutant QLabel#Badge { border-radius: 14px; font-size: 12px; font-weight: bold; }
#MetaMutant QLabel#Badge[state="locked"] { border: 2px solid #55595c; background: #3c3f41; color: #75797c; }
#MetaMutant QLabel#Badge[state="ready"], #MetaMutant QLabel#Badge[state="running"] {
    border: 2px solid #4b6eaf; background: #4b6eaf; color: #ffffff; }
#MetaMutant QLabel#Badge[state="done"] { border: 2px solid #59a869; background: #59a869; color: #ffffff; }
#MetaMutant QLabel#Badge[state="failed"] { border: 2px solid #c75450; background: #c75450; color: #ffffff; }
#MetaMutant QFrame#Rail { background: #4a4d50; border: none; }
#MetaMutant QFrame#Rail[state="done"] { background: #59a869; }
#MetaMutant QFrame#Rail[state="none"] { background: transparent; }
#MetaMutant QFrame#Card { background: transparent; border: 1px solid transparent; border-radius: 8px; }
#MetaMutant QFrame#Card[state="ready"], #MetaMutant QFrame#Card[state="running"] {
    background: #45494a; border: 1px solid #55595c; }
#MetaMutant QFrame#Card[state="failed"] { background: #45494a; border: 1px solid #7a4643; }
#MetaMutant QFrame#Header { background: #323436; border: none; border-radius: 8px; }
#MetaMutant QFrame#Setup { background: #2f3133; border: none; border-radius: 8px; }
#MetaMutant QFrame#Ready { background: #394a3d; border: 1px solid #4f6b55; border-radius: 8px; }
#MetaMutant QPushButton#Primary {
    background: #4b6eaf; color: #ffffff; border: none; border-radius: 5px; padding: 6px 16px; font-weight: bold; }
#MetaMutant QPushButton#Primary:hover { background: #5a7fc4; }
#MetaMutant QPushButton#Primary:pressed { background: #3f5d94; }
#MetaMutant QPushButton#Primary:disabled { background: #4a4d50; color: #8a8d90; }
#MetaMutant QPushButton#Ghost {
    background: transparent; color: #c8c8c8; border: 1px solid #5c5f61; border-radius: 5px; padding: 4px 10px; }
#MetaMutant QPushButton#Ghost:hover { border-color: #7d8184; color: #ffffff; }
#MetaMutant QPushButton#Link { background: transparent; border: none; color: #8fb0e6; padding: 2px 4px; }
#MetaMutant QPushButton#Link:hover { color: #b5cdf3; }
#MetaMutant QScrollArea { background: transparent; border: none; }
#MetaMutant QComboBox, #MetaMutant QLineEdit {
    background: #2b2d2f; color: #d0d0d0; border: 1px solid #55595c; border-radius: 5px;
    padding: 3px 8px; min-height: 22px; }
#MetaMutant QComboBox:hover, #MetaMutant QLineEdit:hover { border-color: #6d7174; }
#MetaMutant QComboBox:focus, #MetaMutant QLineEdit:focus { border-color: #4b6eaf; }
#MetaMutant QComboBox::drop-down { border: none; width: 22px; }
#MetaMutant QComboBox::down-arrow { image: url(ARROW); width: 10px; height: 10px; }
#MetaMutant QCheckBox { color: #bbbbbb; }
#MetaMutant QToolButton#HelpTip { border: none; background: transparent; padding: 0px; }
#MetaMutant QToolButton#HelpTip:hover { background: #55595c; border-radius: 7px; }
#MetaMutant QMenuBar#Menu { background: transparent; color: #c8c8c8; }
#MetaMutant QMenuBar#Menu::item { padding: 3px 10px; border-radius: 4px; }
#MetaMutant QMenuBar#Menu::item:selected { background: #45494a; }
#MetaMutant QProgressBar { background: #2b2d2f; border: none; border-radius: 3px; min-height: 6px; max-height: 6px; }
#MetaMutant QProgressBar::chunk { background: #4b6eaf; border-radius: 3px; }
#MetaMutant QPlainTextEdit#Log {
    background: #262829; color: #a9adb0; border: none; border-radius: 6px; font-family: Consolas, monospace;
    font-size: 11px; }
'''.replace('ARROW', os.path.join(ICONS, 'DDown.png').replace('\\', '/'))


def open_window(head=None):
    """Show the window, closing one already open; `head` fills in your head mesh."""
    global _window
    try:
        _window.close()
        _window.deleteLater()
    except Exception:
        pass
    _window = MetaMutantUI(head)
    _window.show()
    return _window


def from_selection():
    """The menu's Meta Mutant: the window, with the selected mesh as your head when one is selected."""
    meshes = mm_controller.selected_meshes()
    if len(meshes) > 1:
        cmds.warning('Meta Mutant: {} meshes selected, using {}'.format(len(meshes), meshes[0]))
    return open_window(meshes[0] if meshes else None)


def open_app():
    """The TopoTransfer app on its own, served by Maya."""
    try:
        url = tt_app.open_app()
        print('[TopoTransfer] app at {}'.format(url))
    except Exception as error:
        cmds.warning('TopoTransfer: {}'.format(error))


_tutorial = None


def open_tutorial():
    """The Meta Mutant tutorial (simple steps with pictures), rendered in a Maya window."""
    global _tutorial
    try:
        _tutorial.close()
        _tutorial.deleteLater()
    except Exception:
        pass
    _tutorial = TutorialWindow(os.path.join(PIPELINE, 'tutorial', 'TUTORIAL.md'), _window)
    _tutorial.show()
    return _tutorial


class TutorialWindow(QtWidgets.QDialog):

    def __init__(self, path, parent=None):
        super(TutorialWindow, self).__init__(parent)
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.Window)
        self.setWindowTitle('Meta Mutant tutorial')
        self.resize(760, 820)
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        text = QtWidgets.QTextBrowser()
        text.setOpenExternalLinks(True)
        text.setSearchPaths([os.path.dirname(path)])
        text.setStyleSheet('QTextBrowser { background: #2b2d2f; color: #d0d0d0; border: none; padding: 12px 18px; }')
        text.document().setDefaultStyleSheet('a { color: #8fb0e6; } code, pre { color: #e6c27a; }')
        try:
            with open(path, encoding='utf-8') as f:
                text.setMarkdown(f.read())
        except OSError as error:
            text.setPlainText('The tutorial is missing: {}'.format(error))
        layout.addWidget(text)


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


def _icon(name):
    return QtGui.QIcon(os.path.join(ICONS, name))


def _named(widget, name):
    widget.setObjectName(name)
    return widget


def _restyle(widget, **properties):
    """Set the properties the stylesheet reads, and have it read them again."""
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


def _scrolling(page):
    area = QtWidgets.QScrollArea()
    area.setWidgetResizable(True)
    area.setFrameShape(QtWidgets.QFrame.NoFrame)
    area.setWidget(page)
    return area


class Waiting(Exception):
    """A step that hands over to the browser: not a failure, nothing done yet."""


class Step(QtWidgets.QWidget):
    """One step on the path: its badge on a line running down through every
    step, what it is for, its button and what it did."""

    busy = False

    def __init__(self, number, title, text, button, icon, action, tip='', again=''):
        super(Step, self).__init__()
        self.number, self.action, self.label, self.again = number, action, button, again
        self.after = self.changed = None
        self.state = ''
        outer = QtWidgets.QHBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(10)
        column = QtWidgets.QVBoxLayout()
        column.setSpacing(0)
        self.rail_in = _named(QtWidgets.QFrame(), 'Rail')
        self.rail_in.setFixedSize(2, 10)
        self.badge = _named(QtWidgets.QLabel(str(number)), 'Badge')
        self.badge.setFixedSize(28, 28)
        self.badge.setAlignment(QtCore.Qt.AlignCenter)
        self.rail_out = _named(QtWidgets.QFrame(), 'Rail')
        self.rail_out.setFixedWidth(2)
        column.addWidget(self.rail_in, 0, QtCore.Qt.AlignHCenter)
        column.addWidget(self.badge, 0, QtCore.Qt.AlignHCenter)
        column.addWidget(self.rail_out, 1, QtCore.Qt.AlignHCenter)
        outer.addLayout(column)
        holder = QtWidgets.QVBoxLayout()
        holder.setContentsMargins(0, 3, 0, 3)
        self.card = _named(QtWidgets.QFrame(), 'Card')
        holder.addWidget(self.card)
        outer.addLayout(holder, 1)

        body = QtWidgets.QVBoxLayout(self.card)
        body.setContentsMargins(12, 12, 12, 10)
        body.setSpacing(6)
        head = QtWidgets.QHBoxLayout()
        self.title = _named(QtWidgets.QLabel(title), 'Title')
        head.addWidget(self.title, 1)
        if tip:
            head.addWidget(_help_button(tip))
        self.redo = _named(QtWidgets.QPushButton(' ' + again), 'Link')
        self.redo.setIcon(_icon('RELOAD.png'))
        self.redo.setCursor(QtCore.Qt.PointingHandCursor)
        self.redo.clicked.connect(self.run)
        head.addWidget(self.redo)
        self.text = _named(QtWidgets.QLabel(text), 'Text')
        self.text.setWordWrap(True)
        self.row = QtWidgets.QHBoxLayout()
        self.button = _named(QtWidgets.QPushButton(button), 'Primary')
        if icon:
            self.button.setIcon(_icon(icon))
        self.button.setCursor(QtCore.Qt.PointingHandCursor)
        self.button.clicked.connect(self.run)
        self.row.addWidget(self.button)
        self.row.addStretch(1)
        self.status = _named(QtWidgets.QLabel(), 'Status')
        self.status.setWordWrap(True)
        body.addLayout(head)
        body.addWidget(self.text)
        body.addLayout(self.row)
        body.addWidget(self.status)
        self.set_state('locked')

    def set_state(self, state, status=None, tone=''):
        """locked, ready, running, done or failed; with what to say under it."""
        self.state = state
        for widget in (self.card, self.title, self.text, self.badge):
            _restyle(widget, state=state)
        self.badge.setText(u'✓' if state == 'done' else '!' if state == 'failed' else str(self.number))
        self.button.setVisible(state not in ('locked', 'done'))
        self.button.setEnabled(state != 'running')
        self.button.setText('Working...' if state == 'running' else 'Try again' if state == 'failed' else self.label)
        self.redo.setVisible(state == 'done' and bool(self.again))
        self.text.setVisible(state != 'done')
        if status is not None:
            self.status.setText(status)
            _restyle(self.status, tone=tone)
        self.status.setVisible(bool(self.status.text()) and state != 'locked')
        if self.changed:
            self.changed()

    def report(self, text):
        """The latest line of the log, while the step runs."""
        if self.state == 'running':
            self.status.setText(text)
            self.status.setVisible(True)
            QtWidgets.QApplication.processEvents()

    def run(self):
        if Step.busy:
            return
        Step.busy = True
        self.set_state('running', '')
        QtWidgets.QApplication.processEvents()
        try:
            said = self.action(self)
        except Waiting:
            return
        except Exception as error:
            traceback.print_exc()
            self.set_state('failed', 'Stopped: {}'.format(error), 'failed')
            if self.after:
                self.after(self, False)
            return
        finally:
            Step.busy = False
        self.set_state('done', said or self.status.text(), 'done')
        if self.after:
            self.after(self, True)




class EpicDialog(QtWidgets.QDialog):
    """Epic's licence first: Download stays off until it is accepted."""

    def __init__(self, folder, parent=None):
        super(EpicDialog, self).__init__(parent)
        self.setObjectName('MetaMutant')
        self.setStyleSheet(STYLE)
        self.setWindowTitle('Sample DNA from Epic')
        self.setMinimumWidth(440)
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 12)
        layout.setSpacing(10)
        layout.addWidget(_named(QtWidgets.QLabel('Ada, Epic\'s sample MetaHuman head'), 'Title'))
        text = _named(QtWidgets.QLabel(
            'Only needed when you have no MetaHuman DNA of your own. Meta Mutant downloads <b>Ada.dna</b> '
            '(about 70 MB) from Epic\'s <a href="{repo}" style="color: #8fb0e6;">MetaHuman-DNA-Calibration</a> '
            'on GitHub into<br><code>{folder}</code><br><br>'
            'It comes under Epic\'s own <a href="{licence}" style="color: #8fb0e6;">MetaHuman DNA Calibration '
            'License</a>: use it in your work, but don\'t share or commit it. Mutant Tools does not include it '
            'for that reason.'.format(repo=mm_epic.REPO_URL, licence=mm_epic.LICENSE_URL, folder=folder)), 'Text')
        text.setWordWrap(True)
        text.setOpenExternalLinks(True)
        text.setTextInteractionFlags(QtCore.Qt.TextBrowserInteraction)
        layout.addWidget(text)
        self.accept_box = QtWidgets.QCheckBox('I have read and accept Epic\'s licence')
        layout.addWidget(self.accept_box)
        row = QtWidgets.QHBoxLayout()
        row.addStretch(1)
        cancel = _named(QtWidgets.QPushButton('Cancel'), 'Ghost')
        cancel.clicked.connect(self.reject)
        self.go = _named(QtWidgets.QPushButton('Download'), 'Primary')
        self.go.setEnabled(False)
        self.go.clicked.connect(self.accept)
        self.accept_box.toggled.connect(self.go.setEnabled)
        row.addWidget(cancel)
        row.addWidget(self.go)
        layout.addLayout(row)

    def exec_(self):
        run = getattr(super(EpicDialog, self), 'exec', None) or super(EpicDialog, self).exec_
        return run() and self.accept_box.isChecked()


def default_work_dir(head):
    """<project>/data/MetaMutant/<head>: each head keeps its own files and settings."""
    root = os.path.join(cmds.workspace(q=True, rootDirectory=True), 'data', 'MetaMutant')
    return os.path.normpath(os.path.join(root, _safe_name(head)) if head else root)


def _safe_name(name):
    return ''.join(c if c.isalnum() or c in '_-.' else '_' for c in name.split('|')[-1].split(':')[-1]) or 'head'


class MetaMutantUI(QtMutantWindow.Qt_Mutant):

    def __init__(self, head=None):
        super(MetaMutantUI, self).__init__()
        self.setWindowTitle(TITLE)
        self.set_title(TITLE)
        self.resize(460, 760)
        self.workflow = mm_controller.Workflow(self.load_settings(head), log=self.log, on_change=self.result_arrived)

        body = _named(QtWidgets.QWidget(), 'MetaMutant')
        body.setStyleSheet(STYLE)
        layout = QtWidgets.QVBoxLayout(body)
        layout.setContentsMargins(6, 6, 6, 6)
        layout.setSpacing(8)
        layout.addWidget(self.menu_bar())
        layout.addWidget(self.header())
        page = QtWidgets.QWidget()
        column = QtWidgets.QVBoxLayout(page)
        column.setContentsMargins(0, 0, 0, 0)
        column.setSpacing(8)
        column.addWidget(self.setup())
        column.addLayout(self.path())
        column.addStretch(1)
        layout.addWidget(_scrolling(page), 1)
        self.logs = _named(QtWidgets.QPlainTextEdit(), 'Log')
        self.logs.setReadOnly(True)
        self.logs.setFixedHeight(110)
        layout.addWidget(self.logs)
        self.master_ui.mutant_Layout.addWidget(body)
        self.show_settings()
        if not self.dna.text().strip():  # Epic's sample already downloaded: use it
            got = self.epic_found()
            if got:
                self.use_epic(got)
        self.refresh()

    # ------------------------------------------------------------------ settings

    def load_settings(self, head):
        """The head's own settings (its work folder), else the last work folder's."""
        if head:
            work = default_work_dir(head)
        else:
            work = cmds.optionVar(q=OPTION_VAR) if cmds.optionVar(exists=OPTION_VAR) else default_work_dir('')
        settings = wf.load_settings(wf.paths(work).settings)
        if head and not settings.dna_path and cmds.optionVar(exists=OPTION_VAR):  # a new head: keep the last DNA
            settings.dna_path = wf.load_settings(wf.paths(cmds.optionVar(q=OPTION_VAR)).settings).dna_path
        settings.work_dir = work
        if head:
            settings.custom_mesh = head
        return settings

    def show_settings(self):
        s = self.workflow.s
        self.dna.setText(s.dna_path)
        self.head.setText(s.custom_mesh)
        self.eyes.setText(' '.join(s.eyes))
        self.teeth.setText(' '.join(s.teeth))
        for key, edit in self.region_edits.items():
            edit.setText(' '.join((s.regions or {}).get(key, [])))
        self.show_regions(self.regions_box.isVisible())

    def read_settings(self):
        s = self.workflow.s
        s.dna_path = self.dna.text().strip()
        s.custom_mesh = self.head.text().strip()
        s.eyes = self.eyes.text().split()
        s.teeth = self.teeth.text().split()
        s.regions = {k: e.text().split() for k, e in self.region_edits.items() if e.text().split()}

    def save_settings(self):
        self.read_settings()
        if self.workflow.s.work_dir:
            try:
                self.workflow.save()
                cmds.optionVar(stringValue=(OPTION_VAR, self.workflow.s.work_dir))
            except OSError as error:
                self.log('could not save the settings: {}'.format(error))

    def use_work_dir(self, work):
        """Switch to another work folder, bringing back what was saved there."""
        work = os.path.normpath(work)
        if os.path.normcase(work) == os.path.normcase(self.workflow.s.work_dir):
            return
        self.save_settings()
        self.workflow.stop_link()
        dna = self.workflow.s.dna_path
        self.workflow.s = wf.load_settings(wf.paths(work).settings)
        self.workflow.s.work_dir = work
        self.workflow.s.dna_path = self.workflow.s.dna_path or dna
        self.workflow.applied = False
        for step in self.steps:
            step.set_state('locked', '')
        self.show_settings()
        self.log('work folder: {}'.format(work))
        self.refresh()

    # ------------------------------------------------------------------ layout

    def menu_bar(self):
        bar = _named(QtWidgets.QMenuBar(), 'Menu')
        files = bar.addMenu('File')
        files.addAction('Open the work folder').triggered.connect(lambda *_: self.open_work_folder())
        files.addAction('Change the work folder...').triggered.connect(lambda *_: self.change_work_folder())
        epic = bar.addMenu('Epic Files')
        self.act_download = epic.addAction('Download the sample DNA...')
        self.act_download.triggered.connect(lambda *_: self.update_epic(force=False))
        self.act_again = epic.addAction('Download it again')
        self.act_again.triggered.connect(lambda *_: self.update_epic(force=True))
        self.act_use = epic.addAction('Use the sample DNA')
        self.act_use.triggered.connect(lambda *_: self.epic_found() and self.use_epic(self.epic_found()))
        epic.addSeparator()
        epic.addAction('Open containing folder').triggered.connect(lambda *_: self.open_epic_folder())
        self.act_delete = epic.addAction('Delete the download...')
        self.act_delete.triggered.connect(lambda *_: self.delete_epic())
        epic.addSeparator()
        epic.addAction('Epic\'s licence').triggered.connect(
            lambda *_: QtGui.QDesktopServices.openUrl(QtCore.QUrl(mm_epic.LICENSE_URL)))
        epic.aboutToShow.connect(self.epic_menu_shown)
        help_menu = bar.addMenu('Help')
        help_menu.addAction('Tutorial').triggered.connect(lambda *_: open_tutorial())
        help_menu.addAction('Open TopoTransfer').triggered.connect(lambda *_: open_app())
        self.epic_menu_shown()
        return bar

    def header(self):
        box = _named(QtWidgets.QFrame(), 'Header')
        row = QtWidgets.QHBoxLayout(box)
        row.setContentsMargins(10, 10, 10, 10)
        row.setSpacing(12)
        avatar = QtWidgets.QLabel()
        avatar.setPixmap(_tile('MetaMutant.png', 44, 10))
        text = QtWidgets.QVBoxLayout()
        text.setSpacing(2)
        text.addWidget(_named(QtWidgets.QLabel('Meta Mutant'), 'Name'))
        self.meta = _named(QtWidgets.QLabel(), 'Meta')
        self.meta.setWordWrap(True)
        text.addWidget(self.meta)
        links = QtWidgets.QHBoxLayout()
        links.setContentsMargins(0, 2, 0, 0)
        for label, icon, slot in ((' Tutorial', 'Help.png', open_tutorial),
                                  (' Open TopoTransfer', 'TopoTransfer.png', open_app)):
            link = _named(QtWidgets.QPushButton(label), 'Link')
            link.setIcon(_icon(icon))
            link.setCursor(QtCore.Qt.PointingHandCursor)
            link.clicked.connect(lambda *_, run=slot: run())  # without the `checked` argument
            links.addWidget(link)
        links.addStretch(1)
        text.addLayout(links)
        row.addWidget(avatar, 0, QtCore.Qt.AlignTop)
        row.addLayout(text, 1)
        return box

    def field(self, grid, line, label, tip, placeholder, button, slot):
        name = _named(QtWidgets.QLabel(label), 'Field')
        name.setToolTip(tip)
        edit = QtWidgets.QLineEdit()
        edit.setPlaceholderText(placeholder)
        edit.setToolTip(tip)
        edit.editingFinished.connect(self.fields_changed)
        pick = _named(QtWidgets.QPushButton(button), 'Ghost')
        pick.setCursor(QtCore.Qt.PointingHandCursor)
        pick.clicked.connect(lambda *_: slot())
        grid.addWidget(name, line, 0)
        grid.addWidget(edit, line, 1)
        grid.addWidget(pick, line, 2)
        return edit

    def setup(self):
        box = _named(QtWidgets.QFrame(), 'Setup')
        grid = QtWidgets.QGridLayout(box)
        grid.setContentsMargins(10, 10, 10, 10)
        grid.setHorizontalSpacing(8)
        grid.setVerticalSpacing(6)
        # no DNA yet: Epic's sample head, downloaded from Epic after accepting its licence (shown
        # only while Head DNA is empty)
        self.epic = _named(QtWidgets.QPushButton(' Get the sample DNA from Epic...'), 'Link')
        self.epic.setIcon(_icon('ImportGeo.png'))
        self.epic.setCursor(QtCore.Qt.PointingHandCursor)
        self.epic.setToolTip('No MetaHuman DNA of your own? Downloads Ada.dna from Epic\'s MetaHuman-DNA-Calibration '
                             'on GitHub into {}, and fills it in.'.format(self.epic_root()))
        self.epic.clicked.connect(lambda *_: self.get_epic())
        grid.addWidget(self.epic, 0, 1, 1, 2, QtCore.Qt.AlignLeft)
        self.epic_bar = QtWidgets.QProgressBar()
        self.epic_bar.setRange(0, 1000)
        self.epic_bar.setTextVisible(False)
        self.epic_bar.hide()
        grid.addWidget(self.epic_bar, 1, 1, 1, 2)
        self.dna = self.field(
            grid, 2, 'Head DNA', 'The MetaHuman head .dna to start from: your own MetaHuman\'s, or Epic\'s sample.',
            'head.dna', 'Browse', lambda: self.browse_dna())
        self.dna.textChanged.connect(lambda text: self.epic.setVisible(not text.strip()))
        self.head = self.field(
            grid, 3, 'Your head', 'Your head mesh in the scene. It is not changed: step 3 rigs a copy, <head>_MH.',
            'select it, then Use selected', 'Use selected', lambda: self.use_selected())
        self.eyes = self.field(
            grid, 4, 'Eyes', 'Optional. Your eyeballs: select the two eye meshes, or the faces of each eye on your '
            'head mesh, then Use selected. The MetaHuman eyes are fitted onto them and they follow the eye joints.',
            'optional: eye meshes or their faces', 'Use selected', lambda: self.use_part(self.eyes))
        self.teeth = self.field(
            grid, 5, 'Teeth', 'Optional. Your teeth, gums and tongue: select their meshes, or their faces on your '
            'head mesh, then Use selected. The MetaHuman teeth (with the tongue) are fitted onto them and they follow '
            'the jaw and teeth joints.', 'optional: teeth & tongue, meshes or faces', 'Use selected',
            lambda: self.use_part(self.teeth))
        # optional face regions: lips, eyelids, mouth bag, eye sockets (region-to-region skin transfer)
        self.regions_toggle = _named(QtWidgets.QPushButton(), 'Link')
        self.regions_toggle.setCursor(QtCore.Qt.PointingHandCursor)
        self.regions_toggle.setToolTip(
            'Optional, for cleaner lips and eyelids. Select the faces (or vertices) of each region on your head and '
            'press Use selected: each region then takes its skin weights and blendshapes only from the same region '
            'of the MetaHuman, so the upper lip never opens with the jaw and the lids do not stick together. The '
            'MetaHuman side is found on its own. Eye sockets take the skin around the eye and stay still in the '
            'shapes.')
        self.regions_toggle.clicked.connect(lambda *_: self.show_regions(not self.regions_box.isVisible()))
        grid.addWidget(self.regions_toggle, 6, 0, 1, 3, QtCore.Qt.AlignLeft)
        self.regions_box = QtWidgets.QWidget()
        sub = QtWidgets.QGridLayout(self.regions_box)
        sub.setContentsMargins(0, 0, 0, 0)
        sub.setHorizontalSpacing(8)
        sub.setVerticalSpacing(4)
        self.region_edits = {}
        for line, (key, label) in enumerate(mm_regions.REGIONS):
            self.region_edits[key] = self.field(
                sub, line, label, 'Optional. Select the {} faces or vertices on your head mesh, then Use selected '
                '(clear the field to leave it out).'.format(label.lower()), 'optional: faces of your head',
                'Use selected', (lambda k: lambda: self.use_region(k))(key))
        grid.addWidget(self.regions_box, 7, 0, 1, 3)
        self.show_regions(False)
        return box

    def show_regions(self, visible):
        self.regions_box.setVisible(visible)
        picked = sum(1 for e in self.region_edits.values() if e.text().strip())
        self.regions_toggle.setText('{} Face regions: lips, eyelids, mouth{}'.format(
            '▾' if visible else '▸', ' ({} picked)'.format(picked) if picked else ''))

    def use_region(self, key):
        """A face region: the selected faces / vertices of your head, as they are."""
        picked = cmds.ls(selection=True) or []
        if not picked or not all('.' in p for p in picked):
            cmds.warning('Meta Mutant: select faces or vertices of your head mesh first')
            return
        self.region_edits[key].setText(' '.join(picked))
        self.log('{}: {} item(s)'.format(dict(mm_regions.REGIONS)[key], len(picked)))
        self.fields_changed()
        self.show_regions(True)

    def path(self):
        layout = QtWidgets.QVBoxLayout()
        layout.setContentsMargins(6, 4, 6, 0)
        layout.setSpacing(0)
        self.steps = [
            Step(1, 'Prepare',
                 'Exports the MetaHuman head from the DNA and your head, and opens TopoTransfer in the browser '
                 'with both loaded.',
                 'Export and open TopoTransfer', 'ImportGeo.png', self.do_prepare, again='Export again',
                 tip='Writes mh_head_lod0.obj (with its manifest) and custom_head.obj, world space, to the work '
                     'folder (picked eyes and teeth are left out of it). Maya serves TopoTransfer itself, linked to '
                     'this window.'),
            Step(2, 'Wrap in TopoTransfer',
                 'In the browser: place the landmarks, Wrap, then Export. The wrapped head comes back here on '
                 'its own.',
                 'Open TopoTransfer again', 'TopoTransfer.png', self.do_wrap, again='Open again',
                 tip='The MetaHuman head is the Base, your head the Reference. Export sends the wrapped Base '
                     '(same vertices, your shape) to the work folder. Closed the browser? Open it again, or pick '
                     'an exported OBJ.'),
            Step(3, 'Apply to my head',
                 'Calibrates the DNA to the wrapped head, builds the MetaHuman rig and transfers its skin and '
                 'blendshapes to a copy of your head.',
                 'Apply to my head', 'Skin.png', self.do_apply, again='Apply again',
                 tip='The MetaHuman eyes and teeth are fitted onto yours, the neutral meshes and facial joints move '
                     'to the wrap (head_custom.dna), the rig is built from it (joints, meshes, skin, blendshapes), '
                     'and <head>_MH gets the skin and blendshapes. Applying again replaces the earlier result.'),
        ]
        self.pick_obj = _named(QtWidgets.QPushButton('Pick OBJ'), 'Ghost')
        self.pick_obj.setIcon(_icon('Folder.png'))
        self.pick_obj.setToolTip('Use an OBJ exported from TopoTransfer by hand')
        self.pick_obj.clicked.connect(lambda *_: self.pick_wrapped())
        self.steps[1].row.insertWidget(1, self.pick_obj)
        for step in self.steps:
            step.after = self.step_done
            step.changed = self.show_progress
            layout.addWidget(step)
        self.ready = self.ready_panel()
        layout.addSpacing(10)
        layout.addWidget(self.ready)
        return layout

    def ready_panel(self):
        box = _named(QtWidgets.QFrame(), 'Ready')
        row = QtWidgets.QHBoxLayout(box)
        row.setContentsMargins(12, 12, 12, 12)
        row.setSpacing(12)
        mark = QtWidgets.QLabel()
        mark.setPixmap(_icon('Complete.png').pixmap(28, 28))
        text = QtWidgets.QVBoxLayout()
        text.setSpacing(2)
        self.ready_text = _named(QtWidgets.QLabel(), 'Text')
        self.ready_text.setWordWrap(True)
        text.addWidget(_named(QtWidgets.QLabel('Your head is rigged'), 'Title'))
        text.addWidget(self.ready_text)
        row.addWidget(mark, 0, QtCore.Qt.AlignTop)
        row.addLayout(text, 1)
        box.hide()
        return box

    # ------------------------------------------------------------------ state

    @staticmethod
    def maya_version():
        return cmds.about(version=True).split()[0]

    def supported(self):
        return self.maya_version() == mm_controller.MAYA_VERSION

    def refresh(self):
        """Light the steps from what is on disk: done as far as their files are there."""
        self.read_settings()
        if not self.supported():
            for step in self.steps:
                step.set_state('locked', '')
            self.show_progress('Meta Mutant needs Maya {} (this is Maya {}).'.format(
                mm_controller.MAYA_VERSION, self.maya_version()))
            return
        done = self.workflow.status()
        flags = [done['prepare'], done['prepare'] and done['wrap'], done['prepare'] and done['wrap'] and done['apply']]
        ready = True
        for step, finished in zip(self.steps, flags):
            if step.state == 'running':
                continue
            if finished:
                if step.state != 'done':
                    step.set_state('done', '', 'done')
            elif ready:
                if step.state not in ('ready', 'failed'):
                    step.set_state('ready', '')
                ready = False
            else:
                step.set_state('locked', '')
                ready = False
        self.ready.setVisible(all(flags))
        self.show_progress()

    def show_progress(self, problem=''):
        """Under the name: which step is next. Down the path: the line is green as far as the steps are done."""
        if not hasattr(self, 'meta') or not hasattr(self, 'steps'):
            return
        for i, step in enumerate(self.steps):
            _restyle(step.rail_in, state='none' if i == 0 else self.steps[i - 1].state)
            _restyle(step.rail_out, state='none' if step is self.steps[-1] else step.state)
        self.pick_obj.setVisible(self.steps[1].state in ('ready', 'failed'))
        todo = [step for step in self.steps if step.state != 'done']
        if not problem and not self.supported():
            problem = 'Meta Mutant needs Maya {} (this is Maya {}).'.format(mm_controller.MAYA_VERSION, self.maya_version())
        if problem:
            text = problem
        elif not self.workflow.s.dna_path or not self.workflow.s.custom_mesh:
            text = 'Choose the head DNA and your head mesh to start.'
        elif todo:
            text = 'Step {} of {}: {}'.format(self.steps.index(todo[0]) + 1, len(self.steps), todo[0].title.text())
        else:
            text = 'All {} steps done: {}_MH has the MetaHuman rig.'.format(len(self.steps), self.workflow.s.custom_mesh)
        self.meta.setText(text)
        _restyle(self.meta, tone='failed' if problem else '')

    def step_done(self, step, ok):
        self.save_settings()
        if ok:
            later = self.steps[self.steps.index(step) + 1:]
            for i, other in enumerate(later):
                other.set_state('ready' if i == 0 else 'locked', '')
        self.ready_text.setText('{}_MH has the MetaHuman rig: skin, joints and blendshapes. Your head is as it '
                                'was.'.format(self.workflow.s.custom_mesh))
        self.ready.setVisible(all(other.state == 'done' for other in self.steps))
        self.show_progress()

    def result_arrived(self):
        """TopoTransfer's Export came back through the link."""
        self.steps[1].set_state('done', 'Wrapped head received: {}'.format(
            os.path.basename(self.workflow.s.wrapped_obj)), 'done')
        self.step_done(self.steps[1], True)
        self.raise_()
        self.activateWindow()

    def log(self, text):
        print('[Meta Mutant] {}'.format(text))
        self.logs.appendPlainText(text)
        for step in self.steps:
            step.report(text)

    # ------------------------------------------------------------------ actions

    def fields_changed(self):
        self.read_settings()
        self.save_settings()
        self.refresh()

    def browse_dna(self):
        start = self.dna.text().strip()
        options = {'startingDirectory': os.path.dirname(start)} if start else {}
        picked = cmds.fileDialog2(fileMode=1, dialogStyle=2, fileFilter='DNA (*.dna)', **options)
        if picked:
            self.dna.setText(picked[0])
            self.fields_changed()

    def use_selected(self):
        meshes = mm_controller.selected_meshes()
        if not meshes:
            cmds.warning('Meta Mutant: select your head mesh first')
            return
        self.head.setText(meshes[0])
        self.use_work_dir(default_work_dir(meshes[0]))
        self.head.setText(meshes[0])
        self.fields_changed()

    def use_part(self, edit):
        """Eyes / teeth: the selected meshes and / or faces, as they are."""
        picked = cmds.ls(selection=True) or []
        if not picked:
            cmds.warning('Meta Mutant: select the meshes or faces first (or clear the field to leave it out)')
            return
        edit.setText(' '.join(picked))
        self.log('{}: {}'.format('eyes' if edit is self.eyes else 'teeth', ' '.join(picked)))
        self.fields_changed()

    def pick_wrapped(self):
        picked = cmds.fileDialog2(fileMode=1, dialogStyle=2, fileFilter='OBJ (*.obj)',
                                  startingDirectory=self.workflow.s.work_dir or '',
                                  caption='The OBJ exported from TopoTransfer')
        if picked:
            self.workflow.s.wrapped_obj = picked[0]
            self.log('using {}'.format(picked[0]))
            self.result_arrived()

    def open_work_folder(self):
        work = self.workflow.s.work_dir
        if work:
            os.makedirs(work, exist_ok=True)
            QtGui.QDesktopServices.openUrl(QtCore.QUrl.fromLocalFile(work))

    def change_work_folder(self):
        picked = cmds.fileDialog2(fileMode=3, dialogStyle=2, startingDirectory=self.workflow.s.work_dir or '',
                                  caption='Work folder for this head')
        if picked:
            self.use_work_dir(picked[0])

    # ------------------------------------------------------------------ Epic's sample DNA

    def epic_root(self):
        return os.path.normpath(mm_epic.default_dir(cmds.internalVar(userAppDir=True)))

    def epic_found(self):
        return mm_epic.found(self.epic_root())

    def get_epic(self):
        """Epic's sample DNA: downloaded once, after the licence is accepted, then filled in."""
        got = self.epic_found()
        if got is None:
            if not EpicDialog(self.epic_root(), self).exec_():
                return
            got = self.run_download()
        if got:
            self.use_epic(got)

    def run_download(self, force=False):
        """Download (or update) the sample DNA with the progress bar; the EpicFiles, or None when it failed."""
        what = 'Downloading' if force or self.epic_found() is None else 'Updating'
        self.epic.setVisible(True)
        self.epic.setEnabled(False)
        self.epic.setText(' {} from Epic...'.format(what))
        self.epic_bar.setValue(0)
        self.epic_bar.show()
        QtWidgets.QApplication.processEvents()

        def fraction(value):
            if int(value * 1000) != self.epic_bar.value():
                self.epic_bar.setValue(int(value * 1000))
                self.epic.setText(' {} from Epic... {}%'.format(what, int(value * 100)))
                QtWidgets.QApplication.processEvents()

        try:
            got = mm_epic.download(self.epic_root(), accepted=True, progress=lambda text: None, fraction=fraction,
                                   force=force)
            self.log('{} Epic\'s sample DNA in {}'.format('downloaded' if what == 'Downloading' else 'updated', got.root))
            return got
        except Exception as error:
            traceback.print_exc()
            self.log('Epic\'s sample DNA could not be downloaded: {}'.format(error))
            return None
        finally:
            self.epic_bar.hide()
            self.epic.setEnabled(True)
            self.epic.setText(' Get the sample DNA from Epic...')
            self.epic.setVisible(not self.dna.text().strip())

    def update_epic(self, force=False):
        """Menu: Update (only what changed at Epic) or Download again (everything)."""
        if self.epic_found() is None:
            self.get_epic()
            return
        self.run_download(force=force)

    def open_epic_folder(self):
        path = mm_epic.folder(self.epic_root())
        path = path if os.path.isdir(path) else self.epic_root()
        if not os.path.isdir(path):
            self.log('nothing downloaded from Epic yet ({} does not exist)'.format(path))
            return
        QtGui.QDesktopServices.openUrl(QtCore.QUrl.fromLocalFile(path))

    def delete_epic(self):
        path = mm_epic.folder(self.epic_root())
        if not os.path.isdir(path):
            self.log('nothing downloaded from Epic to delete')
            return
        answer = QtWidgets.QMessageBox.question(
            self, 'Delete Epic\'s sample DNA', 'Delete the download from Epic?\n\n{}\n\nYou can download it again '
            'from the Epic Files menu.'.format(path))
        if answer != QtWidgets.QMessageBox.Yes:
            return
        try:
            mm_epic.remove(self.epic_root())
        except Exception as error:
            traceback.print_exc()
            self.log('could not delete {}: {}'.format(path, error))
            return
        inside = os.path.normcase(os.path.abspath(path))
        if self.dna.text().strip() and os.path.normcase(os.path.abspath(self.dna.text().strip())).startswith(inside):
            self.dna.setText('')
        self.log('deleted {}'.format(path))
        self.fields_changed()

    def epic_menu_shown(self):
        """Grey out what does not apply: nothing to update, use or delete before the first download."""
        have = self.epic_found() is not None
        self.act_download.setText('Update the sample DNA' if have else 'Download the sample DNA...')
        for action in (self.act_again, self.act_use, self.act_delete):
            action.setEnabled(have)

    def use_epic(self, got):
        self.dna.setText(got.dna)
        self.log('Head DNA: Epic\'s sample, {}'.format(got.dna))
        self.fields_changed()

    # ------------------------------------------------------------------ the steps

    def do_prepare(self, step):
        self.read_settings()
        self.workflow.s.wrapped_obj = ''  # a new export waits for a new wrap
        self.workflow.applied = False
        self.workflow.prepare()
        return 'Exported, and TopoTransfer is open in the browser with both heads.'

    def do_wrap(self, step):
        self.read_settings()
        self.workflow.open_app()
        # done when the export comes back (result_arrived), not when the browser opens
        step.set_state('ready', 'Waiting for TopoTransfer\'s Export...', '')
        raise Waiting()

    def do_apply(self, step):
        self.read_settings()
        self.workflow.apply_all()
        return 'Rigged {}_MH.'.format(self.workflow.s.custom_mesh)

    def closeEvent(self, event):
        self.save_settings()
        self.workflow.stop_link()
        super(MetaMutantUI, self).closeEvent(event)
