"""WebToRig window: rig a character placed on mutanttools.com/web-to-rig/.

Opened by the Drag_into_Maya.py that comes in the website's download, with the
download's folder:

    from Mutant_Tools.UI.WebToRig import load_web_to_rig
    load_web_to_rig.open_window(folder)

The Rig tab runs the stages in order, each with its own progress bar: Mutant
Tools (already there by now), the character on Manny with its skin, the
template guides, the build. The Extra tab tries animation on the rig.
"""
from __future__ import absolute_import

import traceback

import maya.cmds as cmds

try:
    from importlib import reload
except ImportError:  # Python 2
    pass

try:
    from PySide6 import QtWidgets
except ImportError:  # Maya 2024 and older
    from PySide2 import QtWidgets

import Mutant_Tools
from Mutant_Tools.UI import QtMutantWindow
from Mutant_Tools.UI.WebToRig import web_to_rig
reload(QtMutantWindow)
reload(web_to_rig)

TITLE = 'Web to Rig'
FIRST_ANIMATION = ('skinning_test', 'walking')
_window = None


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


class Stage(QtWidgets.QFrame):
    """One step of the workflow: what it does, a button, its progress."""

    def __init__(self, title, text, button, action, parent=None):
        super(Stage, self).__init__(parent)
        self.action = action
        self.name = title
        self.setFrameShape(QtWidgets.QFrame.StyledPanel)
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(12, 10, 12, 10)
        layout.setSpacing(6)
        self.title = QtWidgets.QLabel('<b>{}</b>'.format(title))
        info = QtWidgets.QLabel(text)
        info.setWordWrap(True)
        self.row = QtWidgets.QHBoxLayout()
        self.button = QtWidgets.QPushButton(button)
        self.button.setMinimumHeight(30)
        self.bar = QtWidgets.QProgressBar()
        self.bar.setRange(0, 100)
        self.bar.setValue(0)
        self.row.addWidget(self.button, 0)
        self.row.addWidget(self.bar, 1)
        self.status = QtWidgets.QLabel('')
        self.status.setWordWrap(True)
        layout.addWidget(self.title)
        layout.addWidget(info)
        layout.addLayout(self.row)
        layout.addWidget(self.status)
        self.button.clicked.connect(self.run)
        self.next = None

    def report(self, percent, text):
        self.bar.setValue(int(percent))
        self.status.setText(text)
        QtWidgets.QApplication.processEvents()

    def finish(self, text):
        self.report(100, text)
        self.title.setText(u'<b>{}  ✓</b>'.format(self.name))
        if self.next:
            self.next.setEnabled(True)

    def run(self):
        self.button.setEnabled(False)
        cmds.undoInfo(openChunk=True, chunkName='WebToRig')
        try:
            self.action(self)
        except Exception as error:
            traceback.print_exc()
            self.report(0, 'Stopped: {}'.format(error))
        finally:
            cmds.undoInfo(closeChunk=True)
            self.button.setEnabled(True)


class WebToRigUI(QtMutantWindow.Qt_Mutant):

    def __init__(self, folder=None):
        super(WebToRigUI, self).__init__()
        self.folder = folder
        self.setWindowTitle(TITLE)
        self.set_title(TITLE)
        self.resize(460, 660)

        body = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(body)
        layout.setContentsMargins(4, 4, 4, 4)
        self.source = QtWidgets.QLabel()
        self.source.setWordWrap(True)
        pick = QtWidgets.QPushButton('Choose another download folder...')
        pick.clicked.connect(self.choose_folder)
        layout.addWidget(self.source)
        layout.addWidget(pick)

        tabs = QtWidgets.QTabWidget()
        tabs.addTab(self.rig_tab(), 'Rig')
        tabs.addTab(self.extra_tab(), 'Extra')
        layout.addWidget(tabs, 1)
        self.master_ui.mutant_Layout.addWidget(body)
        self.show_folder()

    # ------------------------------------------------------------------

    def rig_tab(self):
        page = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(page)
        installed = Stage('1  Mutant Tools', 'Installed and loaded.', 'Ready', lambda s: s.finish('Ready.'))
        character = Stage(
            '2  Import the character',
            'Imports the character from the download, stands it as the website showed it, builds Unreal\'s '
            'Manny skeleton fitted to it and loads its skin from the skin pack. Any skeleton the file came '
            'with is removed.',
            'Import character', self.do_import)
        template = Stage(
            '3  Place the template',
            'Imports the HumanUnrealGameTemplate guides and moves them where the website placed the joints; '
            'the face guides follow the head. Check them, and move any guide you want, before building. The '
            'face blocks are switched off for now: their eyelids and lips need edges picked on your mesh.',
            'Place template', self.do_template)
        build = Stage(
            '4  Build the rig',
            'Builds the Mutant Tools body rig from the guides, then constrains the Manny joints to it, so the '
            'skinned character moves with the controls. Set up the face later and rebuild.',
            'Build rig', self.do_build)
        installed.next, character.next, template.next = character, template, build
        for stage in (template, build):
            stage.setEnabled(False)
        for stage in (installed, character, template, build):
            layout.addWidget(stage)
        layout.addStretch(1)
        installed.finish('Mutant Tools is ready.')
        return page

    def extra_tab(self):
        page = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(page)
        self.animation = Stage(
            'Test the rig with animation',
            'Keys one of Mutant Tools\' Mixamo animations onto the rig\'s FK controls, as the Anim Loader does. '
            'The skinned character follows through the Manny skeleton. Build the rig first.',
            'Apply', self.do_animation)
        self.clips = QtWidgets.QComboBox()
        names = web_to_rig.animations()
        self.clips.addItems(names)
        for name in FIRST_ANIMATION:
            if name in names:
                self.clips.setCurrentIndex(names.index(name))
                break
        self.animation.row.insertWidget(0, self.clips, 1)
        clear = QtWidgets.QPushButton('Remove the animation')
        clear.clicked.connect(self.do_clear)
        loader = QtWidgets.QPushButton('Open the Anim Loader')
        loader.clicked.connect(web_to_rig.open_anim_loader)
        layout.addWidget(self.animation)
        layout.addWidget(clear)
        layout.addWidget(loader)
        layout.addStretch(1)
        return page

    # ------------------------------------------------------------------

    def show_folder(self):
        if not self.folder:
            self.source.setText('No download folder chosen.')
            return
        try:
            manifest = web_to_rig.read_manifest(self.folder)
            self.source.setText('<b>{}</b><br>{}'.format(manifest.get('model', ''), self.folder))
        except Exception as error:
            self.source.setText(str(error))

    def choose_folder(self):
        picked = cmds.fileDialog2(fileMode=3, caption='The unzipped Web to Rig download')
        if picked:
            self.folder = picked[0]
            self.show_folder()

    def do_import(self, stage):
        meshes = web_to_rig.import_character(self.folder, stage.report)
        stage.finish('Imported {} mesh(es) on Manny, skinned.'.format(len(meshes)))

    def do_template(self, stage):
        guides = web_to_rig.place_template(self.folder, stage.report)
        stage.finish('Placed {} guides. Check them, then build.'.format(len(guides)))

    def do_build(self, stage):
        driven = web_to_rig.build_rig(stage.report)
        stage.finish('Rig built: {} Manny joints follow it. Try it in the Extra tab.'.format(len(driven)))

    def do_animation(self, stage):
        web_to_rig.apply_animation(self.clips.currentText(), stage.report)

    def do_clear(self):
        try:
            web_to_rig.remove_animation()
            self.animation.report(0, 'Animation removed: the keys are off and every control is back to its value '
                                     'from before the first animation.')
        except Exception as error:
            traceback.print_exc()
            self.animation.report(0, 'Stopped: {}'.format(error))
