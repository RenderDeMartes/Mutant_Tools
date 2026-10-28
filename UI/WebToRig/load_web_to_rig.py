"""WebToRig window: rig a character placed on mutanttools.com/web-to-rig/.

Opened by the Drag_into_Maya.py that comes in the website's download, with the
download's folder:

    from Mutant_Tools.UI.WebToRig import load_web_to_rig
    load_web_to_rig.open_window(folder)

The Rig tab is a numbered path: Mutant Tools (already there by now), the
character on Manny with its skin, the template guides, the build. The step to
do next is lit, with the window's one blue button; a step that ran says what
it did, and can run again. The Extra tab tries animation on the built rig:
one of Mutant Tools' Mixamo animations, or an FBX animation through HumanIK.
Police tape across the corner says it is a beta.
"""
from __future__ import absolute_import

import os
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

import Mutant_Tools
from Mutant_Tools.UI import QtMutantWindow
from Mutant_Tools.UI.WebToRig import web_to_rig
reload(QtMutantWindow)
reload(web_to_rig)

TITLE = 'Web to Rig'
FIRST_ANIMATION = ('skinning_test', 'walking')
ICONS = os.path.join(web_to_rig.FOLDER, 'Icons')
STUDIO = 'https://bluetaperigging.com'
RIG = 'Mutant_Tools_Grp'
_window = None

# Mutant Tools' own window colours (UI/Stylesheets/FramelessMutant.css), with
# its selection blue for the one thing to do next, green for done and red for
# stopped
STYLE = '''
#WebToRig QLabel { color: #bbbbbb; }
#WebToRig QLabel#Name { color: #e8e8e8; font-size: 15px; font-weight: bold; }
#WebToRig QLabel#Meta, #WebToRig QLabel#Text, #WebToRig QLabel#Status { color: #9da1a4; }
#WebToRig QLabel#Meta[tone="failed"], #WebToRig QLabel#Status[tone="failed"] { color: #e5847f; }
#WebToRig QLabel#Status[tone="done"] { color: #7cc48b; }
#WebToRig QLabel#Text[tone="wait"] { color: #d9b36c; }
#WebToRig QLabel#Title { color: #e2e2e2; font-size: 13px; font-weight: bold; }
#WebToRig QLabel#Title[state="locked"], #WebToRig QLabel#Text[state="locked"] { color: #6c7073; }
#WebToRig QLabel#Badge { border-radius: 14px; font-size: 12px; font-weight: bold; }
#WebToRig QLabel#Badge[state="locked"] { border: 2px solid #55595c; background: #3c3f41; color: #75797c; }
#WebToRig QLabel#Badge[state="ready"], #WebToRig QLabel#Badge[state="running"] {
    border: 2px solid #4b6eaf; background: #4b6eaf; color: #ffffff; }
#WebToRig QLabel#Badge[state="done"] { border: 2px solid #59a869; background: #59a869; color: #ffffff; }
#WebToRig QLabel#Badge[state="failed"] { border: 2px solid #c75450; background: #c75450; color: #ffffff; }
#WebToRig QFrame#Rail { background: #4a4d50; border: none; }
#WebToRig QFrame#Rail[state="done"] { background: #59a869; }
#WebToRig QFrame#Rail[state="none"] { background: transparent; }
#WebToRig QFrame#Card { background: transparent; border: 1px solid transparent; border-radius: 8px; }
#WebToRig QFrame#Card[state="ready"], #WebToRig QFrame#Card[state="running"] {
    background: #45494a; border: 1px solid #55595c; }
#WebToRig QFrame#Card[state="failed"] { background: #45494a; border: 1px solid #7a4643; }
#WebToRig QFrame#Header { background: #323436; border: none; border-radius: 8px; }
#WebToRig QFrame#Note { background: #2f3133; border: none; border-radius: 6px; }
#WebToRig QFrame#Ready { background: #394a3d; border: 1px solid #4f6b55; border-radius: 8px; }
#WebToRig QPushButton#Primary {
    background: #4b6eaf; color: #ffffff; border: none; border-radius: 5px; padding: 6px 16px; font-weight: bold; }
#WebToRig QPushButton#Primary:hover { background: #5a7fc4; }
#WebToRig QPushButton#Primary:pressed { background: #3f5d94; }
#WebToRig QPushButton#Primary:disabled { background: #4a4d50; color: #8a8d90; }
#WebToRig QPushButton#Ghost {
    background: transparent; color: #c8c8c8; border: 1px solid #5c5f61; border-radius: 5px; padding: 5px 12px; }
#WebToRig QPushButton#Ghost:hover { border-color: #7d8184; color: #ffffff; }
#WebToRig QPushButton#Link { background: transparent; border: none; color: #8fb0e6; padding: 2px 4px; }
#WebToRig QPushButton#Link:hover { color: #b5cdf3; }
#WebToRig QProgressBar { background: #2b2d2f; border: none; border-radius: 2px; min-height: 4px; max-height: 4px; }
#WebToRig QProgressBar::chunk { background: #4b6eaf; border-radius: 2px; }
#WebToRig QScrollArea { background: transparent; border: none; }
#WebToRig QComboBox, #WebToRig QLineEdit {
    background: #2f3133; color: #d0d0d0; border: 1px solid #55595c; border-radius: 5px;
    padding: 3px 8px; min-height: 22px; }
#WebToRig QComboBox:hover, #WebToRig QLineEdit:hover { border-color: #6d7174; }
#WebToRig QComboBox:focus, #WebToRig QLineEdit:focus { border-color: #4b6eaf; }
#WebToRig QComboBox::drop-down { border: none; width: 22px; }
#WebToRig QComboBox::down-arrow { image: url(ARROW); width: 10px; height: 10px; }
'''.replace('ARROW', os.path.join(ICONS, 'DDown.png').replace('\\', '/'))


def open_window(folder=None):
    """Show the window, closing one already open."""
    global _window
    try:
        _window.close()
        _window.deleteLater()
    except Exception:
        pass
    _window = WebToRigUI(folder)
    _window.show()
    return _window


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
    """A block icon as a rounded tile, like the Auto Rigger's."""
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


class Tape(QtWidgets.QWidget):
    """Police tape across the top right corner: a beta, a proof of concept.
    Every click goes through it."""

    SIDE = 160
    TEXT = u'BETA  •  PROOF OF CONCEPT'

    def __init__(self, parent):
        super(Tape, self).__init__(parent)
        self.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents)
        self.setFixedSize(self.SIDE, self.SIDE)

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        # from the top edge down to the right one, running off both
        reach = 140
        painter.translate(self.SIDE - reach / 2.0, reach / 2.0)
        painter.rotate(45)
        band = QtCore.QRectF(-140, -12, 280, 24)
        painter.setPen(QtCore.Qt.NoPen)
        painter.setBrush(QtGui.QColor('#f2c300'))
        painter.drawRect(band)
        painter.setBrush(QtGui.QColor('#202020'))
        for edge in (band.top(), band.bottom() - 3):
            x = band.left()
            while x < band.right():
                painter.drawPolygon(QtGui.QPolygonF([
                    QtCore.QPointF(x, edge), QtCore.QPointF(x + 5, edge),
                    QtCore.QPointF(x + 8, edge + 3), QtCore.QPointF(x + 3, edge + 3)]))
                x += 10
        font = painter.font()
        font.setBold(True)
        font.setPixelSize(10)
        font.setLetterSpacing(QtGui.QFont.AbsoluteSpacing, 0.6)
        painter.setFont(font)
        painter.setPen(QtGui.QColor('#202020'))
        painter.drawText(band, QtCore.Qt.AlignCenter, self.TEXT)
        painter.end()


class Body(QtWidgets.QWidget):
    """The window's content, with the tape kept in its top right corner."""

    tape = None

    def resizeEvent(self, event):
        super(Body, self).resizeEvent(event)
        if self.tape:
            self.tape.move(self.width() - self.tape.width(), 0)
            self.tape.raise_()


class Task(QtWidgets.QWidget):
    """One thing to do: what it is for, its button, its progress while it runs
    and what it did. Numbered, it is a step on the Rig tab's path, its badge on
    a line that runs down through every step; done, it folds to its result."""

    busy = False

    def __init__(self, title, text, button, icon, action, number=None, tip='', again=''):
        super(Task, self).__init__()
        self.action, self.number, self.again, self.label = action, number, again, button
        self.after = self.changed = None
        self.state = ''
        outer = QtWidgets.QHBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(10)
        self.badge = self.rail_in = self.rail_out = None
        if number is not None:
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
        gap = 3 if number is not None else 0
        holder.setContentsMargins(0, gap, 0, gap)
        self.card = _named(QtWidgets.QFrame(), 'Card')
        holder.addWidget(self.card)
        outer.addLayout(holder, 1)

        self.body = QtWidgets.QVBoxLayout(self.card)
        self.body.setContentsMargins(12, 12, 12, 10)
        self.body.setSpacing(6)
        head = QtWidgets.QHBoxLayout()
        self.title = _named(QtWidgets.QLabel(title), 'Title')
        head.addWidget(self.title, 1)
        if tip:
            info = QtWidgets.QLabel()
            info.setPixmap(_icon('Help.png').pixmap(14, 14))
            info.setToolTip(tip)
            head.addWidget(info)
        # only a step that can run twice offers to: the build rebuilds, while
        # the import and the template would find their own work in the way
        self.redo = _named(QtWidgets.QPushButton(' ' + again), 'Link')
        self.redo.setIcon(_icon('RELOAD.png'))
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
        if number is not None:
            self.row.addStretch(1)
        self.bar = QtWidgets.QProgressBar()
        self.bar.setRange(0, 100)
        self.bar.setTextVisible(False)
        self.status = _named(QtWidgets.QLabel(), 'Status')
        self.status.setWordWrap(True)
        self.body.addLayout(head)
        self.body.addWidget(self.text)
        self.body.addLayout(self.row)
        self.body.addWidget(self.bar)
        self.body.addWidget(self.status)
        self.set_state('ready')

    def set_state(self, state, status=None, tone=''):
        """locked, ready, running, done or failed; with what to say under it."""
        self.state = state
        for widget in (self.card, self.title, self.text, self.badge):
            if widget is not None:
                _restyle(widget, state=state)
        if self.badge is not None:
            self.badge.setText(u'✓' if state == 'done' else '!' if state == 'failed' else str(self.number))
        self.button.setVisible(state not in ('locked', 'done'))
        self.button.setEnabled(state != 'running')
        self.button.setText('Working...' if state == 'running' else 'Try again' if state == 'failed' else self.label)
        self.redo.setVisible(state == 'done' and bool(self.again))
        self.text.setVisible(state != 'done')
        self.bar.setVisible(state == 'running')
        if status is not None:
            self.status.setText(status)
            _restyle(self.status, tone=tone)
        self.status.setVisible(bool(self.status.text()) and state != 'locked')
        if self.changed:
            self.changed()

    def report(self, percent, text):
        self.bar.setValue(int(percent))
        self.status.setText(text)
        _restyle(self.status, tone='')
        self.status.setVisible(True)
        QtWidgets.QApplication.processEvents()

    def run(self):
        if Task.busy:
            return
        Task.busy = True
        self.bar.setValue(0)
        self.set_state('running', '')
        QtWidgets.QApplication.processEvents()
        cmds.undoInfo(openChunk=True, chunkName='WebToRig')
        try:
            said = self.action(self)
        except Exception as error:
            traceback.print_exc()
            self.set_state('failed', 'Stopped: {}'.format(error), 'failed')
            return
        finally:
            cmds.undoInfo(closeChunk=True)
            Task.busy = False
        self.set_state('done' if self.number is not None else 'ready', said or self.status.text(), 'done')
        if self.after:
            self.after(self)


class WebToRigUI(QtMutantWindow.Qt_Mutant):

    def __init__(self, folder=None):
        super(WebToRigUI, self).__init__()
        self.folder = folder
        self.has_download = False
        self.setWindowTitle(TITLE)
        self.set_title(TITLE)
        self.resize(440, 700)

        body = _named(Body(), 'WebToRig')
        body.setStyleSheet(STYLE)
        layout = QtWidgets.QVBoxLayout(body)
        layout.setContentsMargins(6, 6, 6, 6)
        layout.setSpacing(8)
        layout.addWidget(self.header())
        layout.addWidget(self.note())
        self.tabs = QtWidgets.QTabWidget()
        self.tabs.addTab(_scrolling(self.rig_tab()), 'Rig')
        self.tabs.addTab(_scrolling(self.extra_tab()), 'Extra')
        self.tabs.currentChanged.connect(self.refresh_extra)
        layout.addWidget(self.tabs, 1)
        body.tape = Tape(body)
        self.master_ui.mutant_Layout.addWidget(body)
        self.show_folder()

    # ------------------------------------------------------------------

    def header(self):
        box = _named(QtWidgets.QFrame(), 'Header')
        row = QtWidgets.QHBoxLayout(box)
        row.setContentsMargins(10, 10, 120, 10)  # clear of the tape
        row.setSpacing(12)
        avatar = QtWidgets.QLabel()
        avatar.setPixmap(_tile('HumanGameUnreal.png', 44, 10))
        text = QtWidgets.QVBoxLayout()
        text.setSpacing(2)
        self.name = _named(QtWidgets.QLabel(), 'Name')
        self.meta = _named(QtWidgets.QLabel(), 'Meta')
        self.meta.setWordWrap(True)
        self.pick = _named(QtWidgets.QPushButton(), 'Link')
        self.pick.setIcon(_icon('Folder.png'))
        self.pick.setCursor(QtCore.Qt.PointingHandCursor)
        self.pick.clicked.connect(self.choose_folder)
        pick = QtWidgets.QHBoxLayout()
        pick.setContentsMargins(0, 2, 0, 0)
        pick.addWidget(self.pick)
        pick.addStretch(1)
        text.addWidget(self.name)
        text.addWidget(self.meta)
        text.addLayout(pick)
        row.addWidget(avatar, 0, QtCore.Qt.AlignTop)
        row.addLayout(text, 1)
        return box

    def note(self):
        box = _named(QtWidgets.QFrame(), 'Note')
        row = QtWidgets.QHBoxLayout(box)
        row.setContentsMargins(10, 7, 64, 7)
        text = QtWidgets.QLabel(
            'A beta, and a proof of concept only. Need rigs you can ship? Contact '
            '<a href="{0}" style="color: #8fb0e6;">bluetaperigging.com</a>'.format(STUDIO))
        text.setWordWrap(True)
        text.setOpenExternalLinks(True)
        text.setTextInteractionFlags(QtCore.Qt.TextBrowserInteraction)
        row.addWidget(text)
        return box

    def rig_tab(self):
        page = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(page)
        layout.setContentsMargins(6, 8, 6, 6)
        layout.setSpacing(0)
        self.steps = [
            Task('Mutant Tools', 'Installed and ready.', '', None, None, number=1),
            Task('Import the character',
                 'Brings your character in standing as it did on the website, on Unreal\'s Manny skeleton, '
                 'with its skin.',
                 'Import character', 'ImportGeo.png', self.do_import, number=2,
                 tip='Imports the model from the download, lines it up with the skeleton you placed, builds '
                     'Manny fitted to it and loads the skin pack. Any skeleton the file came with is removed.'),
            Task('Place the guides',
                 'Lays the Mutant Tools template on the joints you placed. Look them over in the viewport and '
                 'move any you like.',
                 'Place guides', 'ImportGuide.png', self.do_template, number=3,
                 tip='Imports the HumanUnrealGameTemplate guides and moves them onto the website\'s joints, eyes '
                     'and foot pivots; the rest of the face follows the head. The face blocks stay off until '
                     'their eyelid and lip edges are picked on your mesh.'),
            Task('Build the rig',
                 'Builds the body rig and hooks Manny to it, so the skin moves with the controls.',
                 'Build rig', 'Build.png', self.do_build, number=4, again='Build again',
                 tip='Runs the Mutant Tools build from the guides, then constrains each Manny joint to its bind '
                     'joint. For the face, pick its edges, switch its blocks on and build again.'),
        ]
        for step in self.steps:
            step.after = self.step_done
            step.changed = self.show_progress
            layout.addWidget(step)
        self.steps[0].set_state('done', 'Installed and loaded.', 'done')
        self.ready = self.ready_panel()
        layout.addSpacing(12)
        layout.addWidget(self.ready)
        layout.addStretch(1)
        return page

    def ready_panel(self):
        box = _named(QtWidgets.QFrame(), 'Ready')
        row = QtWidgets.QHBoxLayout(box)
        row.setContentsMargins(12, 12, 12, 12)
        row.setSpacing(12)
        mark = QtWidgets.QLabel()
        mark.setPixmap(_icon('Complete.png').pixmap(28, 28))
        text = QtWidgets.QVBoxLayout()
        text.setSpacing(2)
        info = _named(QtWidgets.QLabel('Select any control in the viewport and pose it, or try it with an '
                                       'animation.'), 'Text')
        info.setWordWrap(True)
        text.addWidget(_named(QtWidgets.QLabel('Your rig is ready'), 'Title'))
        text.addWidget(info)
        go = _named(QtWidgets.QPushButton(u'Try it  →'), 'Primary')
        go.setCursor(QtCore.Qt.PointingHandCursor)
        go.clicked.connect(lambda: self.tabs.setCurrentIndex(1))
        row.addWidget(mark, 0, QtCore.Qt.AlignTop)
        row.addLayout(text, 1)
        row.addWidget(go, 0, QtCore.Qt.AlignVCenter)
        box.hide()
        return box

    def extra_tab(self):
        page = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(page)
        layout.setContentsMargins(6, 10, 6, 6)
        layout.setSpacing(10)
        self.intro = _named(QtWidgets.QLabel(), 'Text')
        self.intro.setWordWrap(True)

        names = web_to_rig.animations()
        self.animation = Task(
            'Built-in animations',
            'One of the {} clips that come with Mutant Tools, keyed on the FK controls.'.format(len(names)),
            'Apply', None, self.do_animation,
            tip='The clips Mutant Tools ships with (Utils/Mocap/MocapFiles/Mixamo), the ones its Anim Loader '
                'plays, keyed onto the rig\'s FK controls. The skinned character follows through the Manny '
                'skeleton.')
        self.clips = QtWidgets.QComboBox()
        self.clips.addItems(names)
        for name in FIRST_ANIMATION:
            if name in names:
                self.clips.setCurrentIndex(names.index(name))
                break
        self.animation.row.insertWidget(0, self.clips, 1)

        self.hik = Task(
            'Your own FBX, through HumanIK',
            'An animation on a Mixamo skeleton, from mixamo.com or your own, retargeted with Maya\'s HumanIK.',
            'Apply', None, self.do_hik,
            tip='Retargets an FBX animation with a Mixamo skeleton (from mixamo.com, with or without skin) onto '
                'the rig with Maya\'s HumanIK: the FBX\'s skeleton and the rig are characterized, the rig\'s FK '
                'controls are mapped to it, and the motion is baked onto them. The FBX and the HumanIK '
                'characters are removed afterwards.')
        self.fbx = QtWidgets.QLineEdit()
        self.fbx.setPlaceholderText('Choose an FBX animation...')
        browse = _named(QtWidgets.QPushButton(' Browse'), 'Ghost')
        browse.setIcon(_icon('Folder.png'))
        browse.clicked.connect(self.choose_fbx)
        self.hik.row.insertWidget(0, self.fbx, 1)
        self.hik.row.insertWidget(1, browse)
        self.applied = self.animation

        clear = _named(QtWidgets.QPushButton(' Remove the animation'), 'Ghost')
        clear.setIcon(_icon('RELOAD.png'))
        clear.clicked.connect(self.do_clear)
        loader = _named(QtWidgets.QPushButton('Open the Anim Loader'), 'Link')
        loader.clicked.connect(web_to_rig.open_anim_loader)
        tools = QtWidgets.QHBoxLayout()
        tools.addWidget(clear)
        tools.addStretch(1)
        tools.addWidget(loader)

        layout.addWidget(self.intro)
        layout.addWidget(self.animation)
        layout.addWidget(self.hik)
        layout.addLayout(tools)
        layout.addStretch(1)
        return page

    # ------------------------------------------------------------------

    def show_folder(self):
        """Read the download and start the path over at its first step."""
        manifest, problem = None, ''
        if self.folder:
            try:
                manifest = web_to_rig.read_manifest(self.folder)
            except Exception as error:
                problem = str(error)
        self.has_download = bool(manifest)
        if manifest:
            self.name.setText(manifest.get('model') or os.path.basename(self.folder))
        else:
            self.name.setText('Choose your download')
        # without a download, choosing one is the thing to do: the blue button
        self.pick.setText(' Change folder' if manifest else ' Choose the download folder')
        self.pick.setToolTip(self.folder or 'The unzipped Web to Rig download')
        _restyle(_named(self.pick, 'Link' if manifest else 'Primary'))
        for step in self.steps[1:]:
            step.set_state('locked', '')
        if manifest:
            self.steps[1].set_state('ready', '')
        self.ready.hide()
        self.show_progress(problem)
        self.refresh_extra()

    def show_progress(self, problem=''):
        """Under the name: which step is next, or why none can start. Down the
        path: the line is green as far as the steps are done."""
        if not hasattr(self, 'meta'):
            return
        for i, step in enumerate(self.steps):
            _restyle(step.rail_in, state='none' if i == 0 else self.steps[i - 1].state)
            _restyle(step.rail_out, state='none' if step is self.steps[-1] else step.state)
        todo = [step for step in self.steps if step.state != 'done']
        if problem or not self.has_download:
            text = problem or 'Unzip the download from mutanttools.com/web-to-rig and choose its folder.'
        elif todo:
            text = 'Step {} of {}: {}'.format(self.steps.index(todo[0]) + 1, len(self.steps), todo[0].title.text())
        else:
            text = 'All {} steps done: the rig is built.'.format(len(self.steps))
        self.meta.setText(text)
        _restyle(self.meta, tone='failed' if problem else '')

    def step_done(self, step):
        """The next step lights up; any after it wait for it again."""
        later = self.steps[self.steps.index(step) + 1:]
        for i, other in enumerate(later):
            other.set_state('ready' if i == 0 else 'locked', '')
        self.ready.setVisible(not later)
        self.refresh_extra()

    def refresh_extra(self, *args):
        """Animation needs a built rig: say so, and hold the buttons till then."""
        built = cmds.objExists(RIG)
        self.intro.setText('Put some motion on the rig to see how it moves. Remove it when you are done: every '
                           'control goes back where it was.' if built else
                           'Build the rig on the Rig tab first, then try it here.')
        _restyle(self.intro, tone='' if built else 'wait')
        for task in (self.animation, self.hik):
            task.button.setEnabled(built and task.state != 'running')

    def choose_folder(self):
        picked = cmds.fileDialog2(fileMode=3, caption='The unzipped Web to Rig download')
        if picked:
            self.folder = picked[0]
            self.show_folder()

    def do_import(self, task):
        meshes = web_to_rig.import_character(self.folder, task.report)
        return 'Imported {} mesh{} on Manny, skinned.'.format(len(meshes), '' if len(meshes) == 1 else 'es')

    def do_template(self, task):
        guides = web_to_rig.place_template(self.folder, task.report)
        return 'Placed {} guides. Look them over, then build.'.format(len(guides))

    def do_build(self, task):
        driven = web_to_rig.build_rig(task.report)
        return 'Built. {} Manny joints follow the rig.'.format(len(driven))

    def do_animation(self, task):
        self.applied = task
        web_to_rig.apply_animation(self.clips.currentText(), task.report)

    def choose_fbx(self):
        picked = cmds.fileDialog2(fileMode=1, fileFilter='FBX (*.fbx)', caption='An FBX animation with a Mixamo skeleton')
        if picked:
            self.fbx.setText(picked[0])

    def do_hik(self, task):
        if not self.fbx.text().strip():
            self.choose_fbx()
        if not self.fbx.text().strip():
            raise RuntimeError('Choose the animation FBX first.')
        self.applied = task
        web_to_rig.apply_hik_animation(self.fbx.text().strip(), task.report)

    def do_clear(self):
        try:
            web_to_rig.remove_animation()
        except Exception as error:
            traceback.print_exc()
            self.applied.set_state('failed', 'Stopped: {}'.format(error), 'failed')
            return
        for task in (self.animation, self.hik):
            task.set_state('ready', '')
        self.applied.set_state('ready', 'Animation removed: the keys are off and every control is back where it '
                                        'was.', 'done')
