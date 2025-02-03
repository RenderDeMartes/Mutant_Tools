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
from Mutant_Tools.UI.GamesCrowds import load_games_crowds
reload(load_games_crowds)

try:cGamesCrowds.close()
except:pass
cGamesCrowds = load_games_crowds.GamesCrowds()
cGamesCrowds.show()

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
try:
    import importlib;from importlib import reload
except:
    import imp;from imp import reload

import sys
import json
import glob
import pprint
import operator
from pathlib import Path
import traceback

from Mutant_Tools.Utils.Helpers.decorators import undo
import Mutant_Tools.Utils.Crowds.crowds_utils as crowds_utils
reload(crowds_utils)
cCrowds = crowds_utils.Crowds()

import Mutant_Tools.Utils.Games.games_utils as games_utils
reload(games_utils)
cGames = games_utils.Games()

import Mutant_Tools.Utils.Crowds.Facial.facial_utils as face_utils
reload(face_utils)
fCrowds = face_utils.DemBonesManager()



# -------------------------------------------------------------------

# QT WIndow!
FOLDER_NAME = 'GamesCrowds'
Title = 'Games-Crowds'
UI_File = 'GamesCrowds.ui'

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
reload(helpers)
mh = helpers.Helpers()

import Mutant_Tools.UI
from Mutant_Tools.UI import QtMutantWindow
reload(QtMutantWindow)
Qt_Mutant = QtMutantWindow.Qt_Mutant()

try:
    import importlib;from importlib import reload
except:
    import imp;from imp import reload

import Mutant_Tools
from Mutant_Tools.UI.GamesCrowds.crowd_utils import crowds_combo_utils
reload(crowds_combo_utils)

# -------------------------------------------------------------------


def maya_main_window():
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)


class GamesCrowds(QtMutantWindow.Qt_Mutant):

    def __init__(self):
        super(GamesCrowds, self).__init__()

        self.setWindowTitle(Title)

        self.designer_loader_child(path=os.path.join(FOLDER, 'UI', FOLDER_NAME), ui_file=UI_File)
        self.set_title(Title)
        
        self.user=None
        self.ui_assets = []


        self.create_layout()
        self.create_connections()

        

    # -------------------------------------------------------------------

    def create_layout(self):
        """

        Returns:

        """
        try:
            self.auto_change_show()
        except:
            pass
        self.populate_shows()
        self.populate_assets()

    def create_connections(self):
        """
        
        Returns:

        """
        #-------------------------------------------------
        #-------------Basemesh Import and copy------------
        #-------------------------------------------------

        self.ui.import_male_button.clicked.connect(self.import_male_basemesh)
        self.ui.import_female_button.clicked.connect(self.import_female_basemesh)
        self.ui.transfer_skinning_button.clicked.connect(self.copy_skinning_to_generic)


        #-------------------------------------------
        #----------------Crowds tab-----------------
        #-------------------------------------------

        self.ui.ImportSkeleton.clicked.connect(self.ImportSkeleton)
        self.ui.ReparentSkeleton.clicked.connect(self.ReparentSkeleton)
        self.ui.ReferenceSinning.clicked.connect(self.ReferenceSinning)
        self.ui.OneToOneSkinning.clicked.connect(self.OneToOneSkinning)
        self.ui.OffLabelSkinning.clicked.connect(self.OffLabelSkinning)

        #-------------------------------------------
        #----------------Games tab------------------
        #-------------------------------------------

        self.ui.create_game_joints_button.clicked.connect(self.create_game_joints)
        self.ui.simplify_btn.clicked.connect(self.simplify_btn)
        self.ui.import_face_skeleton_button.clicked.connect(self.import_face_skeleton)
        self.ui.setup_face_skeleton_button.clicked.connect(self.setup_face_skeleton)
        self.ui.set_max_inf_to_four_button.clicked.connect(self.set_max_inf_to_four)
        self.ui.clasic_linear_skin_button.clicked.connect(self.clasic_linear_skin)
        self.ui.delete_constriants_button.clicked.connect(self.delete_constriants)
        self.ui.SegmentScaleOn_Bttn.clicked.connect(self.turn_on_scale_compensate)
        self.ui.SegmentScaleOff_Bttn.clicked.connect(self.turn_off_scale_compensate)

        #--------------------------------------------
        #----------------DemBones tab----------------
        #--------------------------------------------
        self.ui.AnimateFaceRig.clicked.connect(self.AnimateFaceRig)
        self.ui.LoadFaceGeo.clicked.connect(lambda:self.put_selection_on_field(field=self.ui.faceGeoText))
        self.ui.ExportData.clicked.connect(self.ExportData)
        self.ui.ImportData.clicked.connect(self.ImportData)
        self.ui.ConnectFaceRig.clicked.connect(self.ConnectFaceRig)

        #-------------------------------------------
        #----------------Combo subtab---------------
        #-------------------------------------------
        self.ui.combo_shows_combo.currentIndexChanged.connect(self.populate_assets)
        self.ui.search_bar_line.returnPressed.connect(self.populate_assets)
        self.ui.filter_crowds_check.stateChanged.connect(self.populate_assets)
        self.ui.add_combo_button.clicked.connect(self.add_asset_to_ui)
        self.ui.set_combine.clicked.connect(self.set_combined_asset)
        self.ui.create_combo_button.clicked.connect(self.create_combo_rig)
        self.ui.save_combo.clicked.connect(self.save_combo_prefs)
        self.ui.load_combo.clicked.connect(self.load_combo_prefs)


    # -------------------------------------------------------------------
    
    def import_male_basemesh(self):
        print("Hello male")
        from Mutant_Tools.UI.GamesCrowds.crowd_utils import zombie_crowd_copy
        reload(zombie_crowd_copy)
        zombie_crowd_copy.import_male_basemeshes()

    def import_female_basemesh(self):
        print("Hello female")
        from Mutant_Tools.UI.GamesCrowds.crowd_utils import zombie_crowd_copy
        reload(zombie_crowd_copy)
        zombie_crowd_copy.import_female_basemeshes()

    @undo
    def copy_skinning_to_generic(self):
        print("Rawrrrr")
        from Mutant_Tools.UI.GamesCrowds.crowd_utils import zombie_crowd_copy
        reload(zombie_crowd_copy)
        zombie_crowd_copy.name_transfer_hierarchy_skins()
        zombie_crowd_copy.attachment_groups_copy()
    # -------------------------------------------------------------------

    def auto_change_show(self):
        current_show = mh.find_user_show()
        if current_show:
            self.ui.skeleton_box.setCurrentText(current_show)
            self.ui.faceGeoText.setText('C_Head_hi')
        if current_show == 'SP':
            self.ui.skeleton_box.setCurrentIndex(1)
            self.ui.faceGeoText.setText('C_Body_hi')

    def ImportSkeleton(self):
        if self.ui.skeleton_box.currentText() == 'AG':
            cCrowds.import_crowd_skeleton(skeleton='atoms')
        elif self.ui.skeleton_box.currentText() == 'SP':
            cCrowds.import_crowd_skeleton(skeleton='atoms_toon')
        elif self.ui.skeleton_box.currentText() == 'BD':
            cCrowds.import_crowd_skeleton(skeleton='atoms_toon')
    @undo
    def ReparentSkeleton(self):
        if self.ui.skeleton_box.currentText() == 'AG':
            cCrowds.match_crowd_to_rig(crowds_map='atoms_map', rig_map='mutant_map')
        elif self.ui.skeleton_box.currentText() == 'SP':
            cCrowds.match_crowd_to_rig(crowds_map='atoms_toon_map', rig_map='mutant_toon_map')
        elif self.ui.skeleton_box.currentText() == 'BD':
            cCrowds.match_crowd_to_rig(crowds_map='atoms_toon_map', rig_map='bd_toon_map')

    def ReferenceSinning(self):
        cCrowds.transfer_skin_reference(main_geo_grp='geo', crowds_map='atoms_map', main_joint='Hips',
                                        remove_reference=False)

    @undo
    def OneToOneSkinning(self):
        cCrowds.transfer_skin_one_to_one()

    @undo
    def OffLabelSkinning(self):
        cCrowds.transfer_skin_labels()
    # -------------------------------------------------------------------

    # -------------------------------------------------------------------
    # -------------------------------------------------------------------
    # ----------------------------Games Bones----------------------------
    # -------------------------------------------------------------------
    # -------------------------------------------------------------------

    @undo
    def create_game_joints(self):
        check = self.ui.skin_check.isChecked()
        cGames.create_biped_game_joints(do_skins=check)

    @undo
    def simplify_btn(self):
        cGames.convert_hero_template_skl_to_simple_skl()

    # @undo
    # def convert_eyes(self):
    # 	cGames.convert_eyes()
    #
    # @undo
    # def convert_mouth(self):
    # 	cGames.convert_mouth()
    #
    # @undo
    # def convert_eyebrows(self):
    # 	cGames.convert_eyebrows()
    #
    # @undo
    # def convert_jaw(self):
    # 	cGames.convert_jaw()


    @undo
    def import_face_skeleton(self):
        cGames.create_face_skeleton()

    @undo
    def setup_face_skeleton(self):
        cGames.setup_face_skeleton()

    @undo
    def set_max_inf_to_four(self):
        cGames.set_max_inf(inf=4)

    def clasic_linear_skin(self):
        cGames.classic_linear_skin()

    def delete_constriants(self):
        cGames.remove_constriants_in_main_skeleton()

    def turn_on_scale_compensate(self):
        cGames.set_scale_compensate_on_skl(1)
    def turn_off_scale_compensate(self):
        cGames.set_scale_compensate_on_skl(0)

    # -------------------------------------------------------------------
    # -------------------------------------------------------------------
    # ----------------------------Dem Bones------------------------------
    # -------------------------------------------------------------------
    # -------------------------------------------------------------------

    def put_selection_on_field(self, field):
        sel = cmds.ls(sl=True)
        print(sel)
        # remove ugly lists keys
        nice_selection = str(sel)[1:-1]
        nice_selection = nice_selection.replace("u'", "'")
        nice_selection = nice_selection.replace("'", "")
        field.setText(nice_selection)

    def fill_cero_controls(self, anim_dict):
        '''
        Recoveres all the controls defined in the SDK dictionary 
            Args:
                dem_joints: DemBones joints

            Returns: None
        '''
        #get all keyed control available
        allCtrls=[]
        for task in sorted(anim_dict.keys()):
            for ctrl in anim_dict[task]['controls']:
                if cmds.objExists(ctrl):
                    attr= "{a}.{t}".format(a=ctrl,t=anim_dict[task]['controls'][ctrl]['axis'])    
                    allCtrls.append(attr)
        anim_dict['Cero_Animation']['controls'] = allCtrls
        print(allCtrls)
        return anim_dict

    def ExportFaceRigData(self):
        anim_dict =  mh.read_json(path=FOLDER, json_file='SDKMap.json')

    @undo
    def AnimateFaceRig(self):
        '''
        Animates controls according to values in the SDKMap.json
        '''
        anim_dict =  mh.read_json(path=os.path.join(FOLDER, 'UI', FOLDER_NAME, 'crowd_utils'), json_file='SDKMap.json')

        if cmds.objExists('Geo_Grp') and cmds.objExists('Control_Grp'):
            print('Using bd dict')
            anim_dict =  mh.read_json(path=os.path.join(FOLDER, 'UI', FOLDER_NAME, 'crowd_utils'), json_file='SDKMap_BD.json')
            for i in anim_dict:
                print(i)

        anim_dict = self.fill_cero_controls(anim_dict)
        allkeys=[]
        for task in anim_dict.keys():
            allkeys.append(anim_dict[task]['input_key'])
        maxf = int(max(allkeys)+1)
        minf = int(min(allkeys))

        for ctrl in anim_dict['Cero_Animation']['controls']:
            k=minf
            while k < (maxf):
                cmds.setKeyframe(ctrl,t=(k,k),v=0)
                k+=1

        for task in anim_dict.keys():
            if anim_dict[task]['input_key'] > 1:
                for ctrl in anim_dict[task]['controls']:
                    if cmds.objExists(ctrl):
                        cmds.setKeyframe(ctrl, at=anim_dict[task]['controls'][ctrl]['axis'],
                                        t=(anim_dict[task]['input_key'],anim_dict[task]['input_key']),
                                        v=anim_dict[task]['controls'][ctrl]['values'])
                    else:
                        print('{} does not exist.'.format(ctrl))
        cmds.currentTime(1)
        print('Done animating SDKMap controls.')


    def ExportData(self):
        '''
        Export FBX, Alembic Cache and run DemBones process on the determined geo.
        '''
        print(fCrowds)
        try:
            fCrowds.generate_output(self.ui.faceGeoText.text())
        except Exception as e:
            print(e)
            #print("Generate Output button. Pending Face Utils implementation.")
    
    def ImportData(self):
        '''
        Import DemBones joints and geo processs on the determined geo.
        '''
        try:
            fCrowds.import_dembones_output()
        except Exception as e:
            print(e)
            #print("Import DemBones Output button. Pending Face Utils implementation")

    @undo
    def ConnectFaceRig(self):
        '''
        COnnect Dem Bones joints to Crowd Rig, Hide unwanted controls and polish skin cluster data.
        '''
        try:
            fCrowds.connect_ctrls_2_dembones()
        except Exception as e:
            print(e)
            print(traceback.format_exc())
            #print("Connect Ctrls 2 Dembones button. Pending Face Utils implementation")

    # -------------------------------------------------------------------
    # -------------------------------------------------------------------
    # ----------------------------Combo Crowd----------------------------
    # -------------------------------------------------------------------
    # -------------------------------------------------------------------
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
                    
                #Filter non crowd rigs
                if self.ui.filter_crowds_check.isChecked():
                    pubs = ass.publishes
                    if not pubs:
                        continue
                    have_crowds=False
                    for pub in pubs:
                        if pub.kind.name == 'crwdrig-hi':
                            have_crowds=True
                            break
                    if not have_crowds:
                        continue
                
                assets.append(ass.name)
                
            self.ui.combo_assets_combo.addItems(assets)

        except Exception as e:
            print(e)
            pass

    def add_asset_to_ui(self, path=None, asset=None):

        if not path:
            show = self.ui.combo_shows_combo.currentText()
            asset = self.ui.combo_assets_combo.currentText()

            cCrowdsCombo = crowds_combo_utils.CrowdsCombo(show)
            path = cCrowdsCombo.find_asset_path(asset)
            if not path:
                path = ''
            print(path)

        layout = QtWidgets.QHBoxLayout()
        self.ui.combo_layout.addLayout(layout)

        asset_edit = QLineEdit()
        asset_edit.setText(path)

        button = QtWidgets.QPushButton()
        button.setFixedSize(30,30)
        button.clicked.connect(partial (self.open_path, asset_edit))
        button.setIcon(QtGui.QIcon(os.path.join(IconsPath ,'Folder.png')))

        layout.addWidget(asset_edit)
        layout.addWidget(button)

        self.ui_assets.append([asset, asset_edit])

    def open_path(self, line_edit):
        path = line_edit.text()
        cmds.file(path, o=True, f=True)

    def set_combined_asset(self):
        asset = self.ui.combo_assets_combo.currentText()
        self.ui.combine_line.setText(asset)


    def save_combo_prefs(self):
        
        paths=[]
        for asset, line_edit in self.ui_assets:
            paths.append(line_edit.text())

        save_path = mh.export_window(extension = ".json")
        save_path = save_path[0]
        if not save_path:
            return

        data = {'paths' : paths,
                  'asset':self.ui.combine_line.text()}

        f = open(save_path, "w")
        f.write(json.dumps(data, sort_keys=1, indent=4, separators=(",", ":")))
        f.close()

        print(save_path)

    def load_combo_prefs(self):
        path = mh.import_window(extension = ".json")
        path = path[0]
        if not path:
            return False

        if not os.path.isfile(path):
            cmds.warning('Path doesnt exists', path)
            return False

        f = open(path, "r")
        data = json.loads(f.read())
        f.close()

        paths = data['paths']
        for path in paths:
            self.add_asset_to_ui(path, None)

        self.ui.combine_line.setText(data['asset'])


    def create_combo_rig(self):
        show = self.ui.combo_shows_combo.currentText()
        cCrowdsCombo = crowds_combo_utils.CrowdsCombo(show)
        paths=[]
        for asset, line_edit in self.ui_assets:
            paths.append(line_edit.text())
        asset = self.ui.combine_line.text()
        if not asset:
            cmds.error('we need a main asset')
        if not paths:
            cmds.error('we need paths')

        cCrowdsCombo.create_combo_rig(paths=paths, asset=asset)

    # CLOSE EVENTS _________________________________
    def closeEvent(self, event):
        ''


# -------------------------------------------------------------------

if __name__ == "__main__":

    try:
        cGamesCrowds.close()  # pylint: disable=E0601
        cGamesCrowds.deleteLater()
    except:
        pass
    cGamesCrowds = GamesCrowds()
    cGamesCrowds.show()

# -------------------------------------------------------------------

'''
#Notes






'''