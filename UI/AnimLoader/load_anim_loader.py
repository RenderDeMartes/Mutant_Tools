from __future__ import absolute_import
'''
version: 1.0.0
date: 21/04/2020

#----------------
content:

#----------------
how to:

try:
    import importlib;from importlib import reload
except:
    import imp;from imp import reload

import Mutant_Tools
from Mutant_Tools.UI.AnimLoader import load_anim_loader
reload(load_anim_loader)

try:cAnimLoaderUI.close()
except:pass
cAnimLoaderUI = load_anim_loader.AnimLoaderUI()
cAnimLoaderUI.show()

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

import maya.OpenMayaUI as omui
from functools import partial
from maya import OpenMaya
import maya.cmds as cmds
import maya.mel as mel

import os
import tempfile

try:import user
except:pass
try:
    import importlib;from importlib import reload
except:
    import imp;from imp import reload

try:
    from Mutant_Tools.Utils.Animation import studio_library_utils, animation_utils
    reload(studio_library_utils)
    reload(animation_utils)
except:
    pass

import sys
import json
import glob
import pprint
from pathlib import Path


# -------------------------------------------------------------------

# QT WIndow!
FOLDER_NAME = 'AnimLoader'
Title = 'Animation Loader'
UI_File = 'AnimLoader.ui'

# QT WIndow!
PATH = os.path.dirname(__file__)
PATH = Path(PATH)
PATH_PARTS = PATH.parts[:-2]
FOLDER=''
for f in PATH_PARTS:
    FOLDER = os.path.join(FOLDER, f)

IconsPath = os.path.join(FOLDER, 'Icons')


# -------------------------------------------------------------------

import Mutant_Tools
import Mutant_Tools.Utils
from Mutant_Tools.Utils.Rigging import main_mutant

reload(Mutant_Tools.Utils.Rigging.main_mutant)
mt = main_mutant.Mutant()

from Mutant_Tools.Utils.Helpers import helpers
reload(Mutant_Tools.Utils.Helpers.helpers)
mh = helpers.Helpers()

import Mutant_Tools.UI
from Mutant_Tools.UI import QtMutantWindow
reload(QtMutantWindow)
Qt_Mutant = QtMutantWindow.Qt_Mutant()

from Mutant_Tools.Utils.Animation import calisthenics_utils
reload(calisthenics_utils)

# -------------------------------------------------------------------


def maya_main_window():
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)


class AnimLoaderUI(QtMutantWindow.Qt_Mutant):

    def __init__(self):
        super(AnimLoaderUI, self).__init__()

        self.setWindowTitle(Title)

        self.designer_loader_child(path=os.path.join(FOLDER, 'UI', FOLDER_NAME), ui_file=UI_File)
        self.set_title(Title)

        self.create_layout()
        self.create_connections()

        self.temp_folder = tempfile.gettempdir()
        self.clean_temp_files()


    # -------------------------------------------------------------------

    def create_layout(self):
        """

        Returns:

        """

        self.load_anims()
        self.populate_mixamo_box()
        self.populate_shows()
        self.populate_assets()

    def create_connections(self):
        """

        Returns:

        """

        self.ui.show_box.currentIndexChanged.connect(self.load_anims)

        self.ui.load_anim.clicked.connect(self.load_animation)

        self.ui.copy_anim.clicked.connect(self.copy_animation)
        self.ui.paste_anim.clicked.connect(self.paste_animation)

        self.ui.clear.clicked.connect(self.clear)

        self.ui.select_ctrls.clicked.connect(lambda: animation_utils.select_ctrls_from_sid())

        self.ui.save_anim_to_desktop.clicked.connect(self.save_anim_to_desktop)
        self.ui.load_anim_from_desktop.clicked.connect(self.load_from_dekstop)

        self.ui.GlobalTester.clicked.connect(lambda: animation_utils.global_ctrl_movements())
        self.ui.Rotate90.clicked.connect(lambda: animation_utils.create_rotate_nighty())

        self.ui.prev_key.clicked.connect(lambda: mel.eval('PreviousKey;FrameSelectedWithoutChildren;'))
        self.ui.next_key.clicked.connect(lambda: mel.eval('NextKey;FrameSelectedWithoutChildren;'))
        self.ui.next_key_2.clicked.connect(lambda: mel.eval('NextKey;'))
        self.ui.next_key_2.clicked.connect(lambda: mel.eval('NextKey;'))

        self.ui.load_mocap.clicked.connect(self.load_mixamo_mocap)
        self.ui.restore_mutant_rig.clicked.connect(self.restore_mutant_rig)

        self.ui.create_rom.clicked.connect(self.create_rom)
        self.ui.clean_rom.clicked.connect(self.clean_rom)

        self.ui.combo_shows_combo.currentIndexChanged.connect(self.populate_assets)
        self.ui.search_bar_line.returnPressed.connect(self.populate_assets)
        self.ui.run_import.clicked.connect(self.import_and_run)


    # -------------------------------------------------------------------

    def clean_temp_files(self):

        files = ['copyAnim','copyPose']
        for file in files:
            file_path = os.path.join(self.temp_folder, file)
            try:
                os.remove(file_path)
            except:
                pass


    # -------------------------------------------------------------------

    def load_anims(self):

        if self.ui.show_box.currentText() == 'SP':
            self.load_sp_anims()
        elif self.ui.show_box.currentText() == 'AnythingGoes':
            self.load_ag_anims()
        else:
            self.ui.paths_box.clear()

    def load_ag_anims(self):

        self.ui.paths_box.clear()

        anims = glob.glob('/job/anythinggoes/pipeline/studiolibrary/Rigging - ROM/*')
        print(anims)

        path_model = self.ui.paths_box.model()

        for anim in reversed(anims):
            item = QtGui.QStandardItem(str(anim))
            path_model.appendRow(item)

    def load_sp_anims(self):

        self.ui.paths_box.clear()

        anims = glob.glob('/job/sp/pipeline/studiolibrary/RIG TEST ANIM/*')
        print(anims)

        path_model = self.ui.paths_box.model()

        for anim in reversed(anims):
            item = QtGui.QStandardItem(str(anim))
            path_model.appendRow(item)

    # -------------------------------------------------------------------
    def load_animation(self):
        from Mutant_Tools.Utils.Animation import studio_library_utils
        reload(studio_library_utils)
        studio_library_utils.load_rom(path_animation= self.ui.paths_box.currentText())

    # -------------------------------------------------------------------

    def clear(self):
        from Mutant_Tools.Utils.Animation import studio_library_utils
        reload(studio_library_utils)
        studio_library_utils.delete_keys()

        #Extra fixes
        try:
            cmds.setAttr("master_2_sub_ctrl.rotateY", 0)
            cmds.setAttr("R_legIK_ctrl.autoStrech", 0)
            cmds.setAttr("L_legIK_ctrl.autoStrech", 0)
        except Exception as e:
            cmds.warning(e)

        #Extra fixes

        nodes = ['']

        mels = [
            'setAttr "L_Hip_Jnt_Switch_Loc.AnkkleBend" 0;',
            'setAttr "L_Hip_Jnt_Switch_Loc.HipBend" 0;',
            'setAttr "L_Hip_Jnt_Switch_Loc.KneeHipBend" 0;',
            'setAttr "L_Hip_Jnt_Switch_Loc.KneeAnkleBend" 0;',
            'setAttr "L_Hip_Jnt_Switch_Loc.BendyOffsets" 0;'
            'setAttr "L_Hip_Jnt_Switch_Loc.BendyTweeks" 0;'
            'setAttr "R_Hip_Jnt_Switch_Loc.AnkkleBend" 0;',
            'setAttr "R_Hip_Jnt_Switch_Loc.HipBend" 0;',
            'setAttr "R_Hip_Jnt_Switch_Loc.KneeHipBend" 0;',
            'setAttr "R_Hip_Jnt_Switch_Loc.KneeAnkleBend" 0;',
            'setAttr "R_Hip_Jnt_Switch_Loc.BendyOffsets" 0;'
            'setAttr "R_Hip_Jnt_Switch_Loc.BendyTweeks" 0;',
            'setAttr "L_ElbowMid_Bendy_Ctrl|L_Shoulder_Jnt_Switch_Loc.WristBend" 0;',
            'setAttr "L_Shoulder_Jnt_Switch_Loc.ShoulderBend" 0;',
            'setAttr "L_Shoulder_Jnt_Switch_Loc.ElbowShoulderBend" 0;',
            'setAttr "L_Shoulder_Jnt_Switch_Loc.ElbowWristBend" 0;',
            'setAttr "L_Hip_Jnt_Switch_Loc.BendyOffsets" 0;',
            'setAttr "L_Hip_Jnt_Switch_Loc.BendyTweeks" 0;',
            'setAttr "R_Shoulder_Jnt_Switch_Loc.WristBend" 0;',
            'setAttr "R_Shoulder_Jnt_Switch_Loc.ShoulderBend" 0;',
            'setAttr "R_Shoulder_Jnt_Switch_Loc.ElbowShoulderBend" 0;',
            'setAttr "R_Shoulder_Jnt_Switch_Loc.ElbowWristBend" 0;',
            'setAttr "R_Hip_Jnt_Switch_Loc.BendyOffsets" 0;',
            'setAttr "R_Hip_Jnt_Switch_Loc.BendyTweeks" 0;',
        ]
        for m in mels:
            try:
                mel.eval(m)
            except Exception as e:
                cmds.warning(e)


    # -------------------------------------------------------------------
    def save_anim_to_desktop(self):

        scene_name = cmds.promptDialog(
            title='Save Animation',
            message='Assing this Animation a Name',
            button=['OK', 'Cancel'],
            defaultButton='OK',
            cancelButton='Cancel',
            dismissString='Cancel',
            tx='')

        if scene_name == 'OK':
            scene_name = cmds.promptDialog(query=True, text=True)

            path_animation = user.home+'/Desktop/AnimLoader/{}.anim'.format(scene_name)
            studio_library_utils.save_rom(path=path_animation, objects='selection', bake=True)

    def load_from_dekstop(self):

        scene_name = cmds.promptDialog(
            title='Load Animation',
            message='Load Animation with Name:',
            button=['OK', 'Cancel'],
            defaultButton='OK',
            cancelButton='Cancel',
            dismissString='Cancel',
            tx='')

        if scene_name == 'OK':
            scene_name = cmds.promptDialog(query=True, text=True)
            path_animation = user.home+'/Desktop/AnimLoader/{}.anim'.format(scene_name)
            studio_library_utils.load_rom(path_animation=path_animation, objects='selection')

    # -------------------------------------------------------------------

    def copy_animation(self):
        path_animation = os.path.join(self.temp_folder, 'AnimLoaderCopy.anim')

        import shutil
        try:shutil.rmtree(path_animation, ignore_errors=True)
        except:pass

        studio_library_utils.save_rom(path=path_animation, objects='selection', bake=True)

    def paste_animation(self):
        path_animation = os.path.join(self.temp_folder, 'AnimLoaderCopy.anim')
        studio_library_utils.load_rom(path_animation=path_animation, objects='selection')


    # -------------------------------------------------------------------
    # -------------------------------------------------------------------
    # -------------------------MIXAMO------------------------------------
    # -------------------------------------------------------------------
    # -------------------------------------------------------------------
    # -------------------------------------------------------------------

    def populate_mixamo_box(self):

        self.ui.mixamo_mocaps.clear()

        mixamo_mocaps_path = os.path.join(FOLDER, 'Utils','Mocap','MocapFiles','Mixamo')
        print(mixamo_mocaps_path)
        mocap_files = glob.glob(os.path.join(mixamo_mocaps_path, '*.json'))
        print(mocap_files)

        omit = ['mixamo_offset_map', 'mixamo_map']
        files_clean_name = []
        for mocap_file in mocap_files:
            for o in omit:
                if o in mocap_file:
                    continue
            file_name = mocap_file.replace('.json','').replace(mixamo_mocaps_path, '').replace('\\', '').replace('/', '')
            files_clean_name.append(file_name)

        self.ui.mixamo_mocaps.addItems(files_clean_name)

    # ----------------------------------------------

    def load_mixamo_mocap(self):
        import Mutant_Tools.Utils.Mocap.Retarget
        from Mutant_Tools.Utils.Mocap.Retarget import retarget
        reload(Mutant_Tools.Utils.Mocap.Retarget.retarget)

        cRetarget = retarget.Retarget()
        cRetarget.load_mixamo_animation(anim_file=self.ui.mixamo_mocaps.currentText().replace('.json', ''))

    # ----------------------------------------------

    def restore_mutant_rig(self):
        import Mutant_Tools.Utils.Mocap.Retarget
        from Mutant_Tools.Utils.Mocap.Retarget import retarget
        reload(Mutant_Tools.Utils.Mocap.Retarget.retarget)

        cRetarget = retarget.Retarget()
        cRetarget.restore_scene()

    # ----------------------------------------------

    def create_rom(self):
        calisthenics_utils.create_rom()

    def clean_rom(self):
        calisthenics_utils.clean_rom()


    def get_user_name(self):

        try:
            from star.entities import Asset, Task, User
            self.user = User.find_current()
        except:
            self.user=None

    def populate_shows(self):

        self.get_user_name()
        if self.user:
            projects = self.user.projects
            prjs = []
            for p in projects:
                prjs.append(p.name)
            self.ui.combo_shows_combo.addItems(prjs)
            try:self.ui.combo_shows_combo.setCurrentIndex(1)
            except:pass

    def populate_assets(self):

        self.ui.combo_assets_combo.clear()
        search_bar = self.ui.search_bar_line.text()
        print(search_bar)

        try:
            from star.entities import Project
            proj_name = self.ui.combo_shows_combo.currentText()
            proj = Project.findby_name(proj_name)
            assets = []
            for ass in proj.assets:
                
                #add with search bar
                if search_bar:
                    if not search_bar.lower() in ass.name.lower():
                        continue
                
                assets.append(ass.name)
                
            self.ui.combo_assets_combo.addItems(assets)

        except Exception as e:
            print(e)
            pass


    def import_and_run(self):
        version = self.get_rig_pub_version()
        cmds.file(new=True, f=True)
        cmds.file(version.path, i=True, f=True)

        self.create_rom()

    def get_asset_object(self):
        from star.entities import Project
        proj = self.ui.combo_shows_combo.currentText()
        asset = self.ui.combo_assets_combo.currentText()
        proj = Project.findby_name(proj)

        for ass in proj.assets:
            if ass.name == asset:
                return ass

    def get_rig_pub_version(self):

        asset_object = self.get_asset_object()
        if not asset_object:
            return False
        pubs = asset_object.publishes
        if not pubs:
            return False
        rig_hi_latest = None
        rig_hi_pref = None
        for pub in pubs:
            if pub.kind.name == 'rig-hi':
                versions = pub.versions
                if not versions:
                    continue
                for version in versions:
                    if version.status != 'prf' and not version.is_latest:
                        continue
                    if version.is_latest:
                        cmds.confirmDialog(title='ROM!',
											message=str(version),
											button=['Ok'],
											defaultButton='Ok')

                        return version
                    



        return version

    # ----------------------------------------------
    # CLOSE EVENTS _________________________________
    def closeEvent(self, event):
        ''


# -------------------------------------------------------------------

if __name__ == "__main__":

    try:
        cAnimLoaderUI.close()  # pylint: disable=E0601
        cAnimLoaderUI.deleteLater()
    except:
        pass
    cAnimLoaderUI = AnimLoaderUI()
    cAnimLoaderUI.show()

# -------------------------------------------------------------------

'''
#Notes



'''