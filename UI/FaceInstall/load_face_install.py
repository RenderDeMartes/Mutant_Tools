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
from Mutant_Tools.UI.FaceInstall import load_face_install
reload(load_face_install)

try:cFaceInstallUI.close()
except:pass
cFaceInstallUI = load_face_install.FaceInstallUI()
cFaceInstallUI.show()

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
import time

from Mutant_Tools.Utils.Helpers.decorators import undo

try:
    from rigSystem.assetTemplates.core import (get_one_sid, validate_sid)
    from star.entities import Project
except:
    pass
import glob

try:
    import importlib;from importlib import reload
except:
    import imp;from imp import reload

import sys
import json
import glob
import pprint
from pathlib import Path

from Mutant_Tools.Utils.Helpers.decorators import undo

# -------------------------------------------------------------------

# QT WIndow!
FOLDER_NAME = 'FaceInstall'
Title = 'Face Install'
UI_File = 'FaceInstall.ui'

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
nc, curve_data, setup = mt.import_configs()

from Mutant_Tools.Utils.Helpers import helpers
reload(Mutant_Tools.Utils.Helpers.helpers)
mh = helpers.Helpers()

import Mutant_Tools.UI
from Mutant_Tools.UI import QtMutantWindow
reload(QtMutantWindow)
Qt_Mutant = QtMutantWindow.Qt_Mutant()

# -------------------------------------------------------------------


def maya_main_window():
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)


class FaceInstallUI(QtMutantWindow.Qt_Mutant):

    def __init__(self):
        super(FaceInstallUI, self).__init__()

        self.setWindowTitle(Title)

        self.designer_loader_child(path=os.path.join(FOLDER, 'UI', FOLDER_NAME), ui_file=UI_File)
        self.set_title(Title)

        self.scenes = self.load_scenes()

        self.create_layout()
        self.create_connections()

        self.temp_folder = tempfile.gettempdir()
        self.clean_temp_files()


    # -------------------------------------------------------------------

    def create_layout(self):
        """

        Returns:

        """
        self.populate_combo_boxes()
        self.set_ui_based_on_node()
        self.connect_check_buttons()
        try:
            self.auto_change_show()
        except:
            pass

    def create_connections(self):
        """

        Returns:

        """

        self.ui.populate_body_line.clicked.connect(self.populate_body_line)
        self.ui.populate_face_line.clicked.connect(self.populate_face_line)

        self.ui.openBodyFile.clicked.connect(lambda: self.open_clean(rig='Body'))
        self.ui.openFaceFile.clicked.connect(lambda: self.open_clean(rig='Face'))

        self.ui.installFaceBtn.clicked.connect(self.install_face)

        self.ui.openInstalledFace.clicked.connect(self.from_installed_open_face)
        self.ui.openInstalledBody.clicked.connect(self.from_installed_open_body)

        self.ui.head_sns.clicked.connect(lambda: mt.bend_and_squash_head(cmds.ls(sl=True)[0], 'Skull_Upr_Ctrl'))
        self.ui.addToSnS.clicked.connect(self.add_to_face_sns)

        self.ui.custom_code.textChanged.connect(self.update_attr)
        self.ui.load_from_node.clicked.connect(self.load_from_node)
        self.ui.run.clicked.connect(self.run_custom_code)

        self.ui.mouth_control_follow_setup.clicked.connect(self.mouth_control_follow_setup)
        self.ui.eyelids_control_follow_setup.clicked.connect(self.eyelids_control_follow_setup)
        self.ui.add_rivets.clicked.connect(self.add_rivets)
        self.ui.remove_rivets.clicked.connect(self.remove_rivets)
        self.ui.extra_eyes_button.clicked.connect(self.extra_eyes_button)
        self.ui.create_MouthIn.clicked.connect(self.create_MouthIn)
        self.ui.create_Mouth_RollPull.clicked.connect(self.create_Mouth_RollPull)
        #self.ui.eye_postbuild.clicked.connect(self.eye_postbuild)
        #self.ui.mouth_postbuild.clicked.connect(self.mouth_postbuild)

        self.ui.create_MouthIn.setToolTip('Select _hi geos that make up the mouth area.')
        self.ui.create_Mouth_RollPull.setToolTip('Select _hi geos that make up the mouth area.')
        #self.ui.eye_postbuild.setToolTip('Select only the eyelash/geo that have existing connections to the BodyEyes setup. Remember to clean the wire influence.')
        #self.ui.mouth_postbuild.setToolTip('No selection needed. Will remove all existing facial rivets.')

        self.ui.zero_all.clicked.connect(self.zero_all)
        self.ui.eyes_follow_head.clicked.connect(self.eyes_follow_head)
        self.ui.show_all_face_ctrls.clicked.connect(lambda: self.change_face_vis_to_animation_requests(show=True))
        self.ui.restore_vis_switches_a.clicked.connect(lambda: self.change_face_vis_to_animation_requests(restore=True, mode='A'))
        self.ui.restore_vis_switches_b.clicked.connect(lambda: self.change_face_vis_to_animation_requests(restore=True, mode='B'))

        self.ui.frame_face.clicked.connect(self.frame_face)
        self.ui.frame_body.clicked.connect(self.frame_body)
        self.ui.move_master.clicked.connect(self.move_master)
        self.ui.restore_master.clicked.connect(self.restore_master)


    # -------------------------------------------------------------------

    def auto_change_show(self):
        current_show = mh.find_user_show()
        if current_show:
            self.ui.attrs_mode_box.setCurrentText(current_show)
        if current_show == 'SP':
            self.ui.show_tabs.setCurrentIndex(1)

    def populate_face_line(self):
        file = mh.import_window(extension="maya_file")
        print(file)
        self.ui.custom_face.setText(file[0])

    def populate_body_line(self):
        file = mh.import_window(extension="maya_file")
        print(file)
        self.ui.custom_body.setText(file[0])

    def set_ui_based_on_node(self):


        data_node = 'Mutant_FaceInstall'

        if not cmds.objExists(data_node):
            return
        face_file = cmds.getAttr('{}.Face'.format(data_node), asString=True)
        body_file = cmds.getAttr('{}.Body'.format(data_node), asString=True)

        self.ui.faceBox.setCurrentText(face_file)
        self.ui.bodyBox.setCurrentText(body_file)


    def load_scenes(self):
        try:
            sid = get_one_sid()
            sid = validate_sid(sid)
            sid.create_rig_group()
            show, asset = sid.breadcrumb.split('/')
            asset_type = sid.type

            proj = Project.findby_name(show)
            for ass in proj.assets:
                if asset == str(ass.name):
                    root = ass.wip_root

            versions_path = root + '/rigging/*/maya/scenes/*.ma'
            versions = glob.glob(versions_path)
            versions.sort(key=os.path.getmtime)

            return versions
        except:
            return []

    # -------------------------------------------------------------------
    def populate_combo_boxes(self):

        self.ui.faceBox.clear()
        self.ui.bodyBox.clear()

        facial_words = ['Face','Facial']
        face_model = self.ui.faceBox.model()
        for scene in reversed(self.scenes):
            item = QtGui.QStandardItem(str(scene))
            for word in facial_words:
                if word in scene:
                    item.setForeground(QtGui.QColor('orange'))
            face_model.appendRow(item)

        body_words = ['Body']
        body_model = self.ui.bodyBox.model()
        for scene in reversed(self.scenes):
            item = QtGui.QStandardItem(str(scene))
            for word in body_words:
                if word in scene:
                    item.setForeground(QtGui.QColor('lightgreen'))
            body_model.appendRow(item)

    # -------------------------------------------------------------------

    def try_face_install(self):
        current_file = cmds.file(q=True, sn=True)
        try:
            self.install_face()
        except Exception as e:
            cmds.warning(e)
            cmds.confirmDialog(m=e)
            cmds.file(m=current_file, open=True)

    # -------------------------------------------------------------------

    def install_face(self):

        errors = []

        self.clean_temp_files()
        cmds.file(new=True, force=True)

        #clean the face
        face_path = self.open_clean(rig='Face')

        add_prefix_to = ['geo','tag','control','rig','bind','Mutant_Build','Mutant_Tools_Grp',
                         'Extra_Geo_Grp', 'Geo_Grp','Ctrl_Grp','Rig_Grp','Miscellaneous_Grp','Bind_Joints_Grp','Template_Grp','Bind_Geo_Grp',
                         'Mutant_Rig','Global_Ctrl_Offset_Grp','Global_Ctrl','Mover_Ctrl_Offset_Grp','Mover_Ctrl',
                        'Mover_Gimbal_Ctrl','Rig_Ctrl_Grp']

        for i in add_prefix_to:
            if cmds.objExists(i):
                cmds.rename(i, 'Face_'+i)

        #Add prefix to face geo
        for geo in cmds.listRelatives('Face_geo', ad=True, type='transform'):
            cmds.rename(geo, 'Face_'+geo)


        #rename sid
        try:
            sid = get_one_sid()
            sid=cmds.rename(sid, 'Face_'+str(sid))
            sid_to_delete = sid
        except:
            sid_to_delete = False

        temp_face = os.path.join(self.temp_folder, 'CleanFaceInstall.ma')
        cmds.file(rename=temp_face)
        saved_temp_face = cmds.file(save=True, type="mayaAscii")

        #------------------------------------------------------------------------------------------
        #clean the body
        body_path = self.open_clean(rig='Body')

        temp_body = os.path.join(self.temp_folder, 'CleanBodyInstall.ma')
        cmds.file(rename=temp_body)
        saved_temp_body = cmds.file(save=True, type="mayaAscii")

        #When ready to install do this:
        print(saved_temp_body, saved_temp_face)
        cmds.file(new=True, force=True)

        cmds.file(saved_temp_body, i=True)
        cmds.file(saved_temp_face, i=True)

        success_file = os.path.join(self.temp_folder, 'FaceInstallSuccess.ma')
        cmds.file(rename=success_file)

        #Connect face to body
        #Reparent everything

        parent_mapping = {  'Face_Ctrl_Grp': 'Ctrl_Grp',
                            'Face_Rig_Grp': 'Rig_Grp',
                            'Face_Rig_Ctrl_Grp': 'Rig_Ctrl_Grp',
                            'Face_Geo_Grp': 'Geo_Grp',
                            'Face_Extra_Geo_Grp': 'Extra_Geo_Grp',
                            'Face_Mutant_Build': 'Template_Grp',
                            'Skull_Parent_Loc': 'Rig_Grp',
                            'Face_geo': 'Rig_Grp',
                            'Face_bind' : 'bind'
                            }

        for i in parent_mapping:
            if cmds.objExists(i):
                cmds.parent(i, parent_mapping[i])

        if cmds.objExists('Face_Global_Ctrl_Offset_Grp'):
            cmds.delete('Face_Global_Ctrl_Offset_Grp')
        if cmds.objExists('Face_Mutant_Tools_Grp'):
            cmds.delete('Face_Mutant_Tools_Grp')

        #Connect Face to Body
        cmds.parentConstraint('Head_Ctrl', 'Skull_Parent_Loc', mo=True)
        cmds.scaleConstraint('Head_Ctrl', 'Skull_Parent_Loc', mo=True)
        cmds.parentConstraint('Head_Ctrl', 'Face_Ctrl_Grp', mo=True)
        cmds.scaleConstraint('Head_Ctrl', 'Face_Ctrl_Grp', mo=True)

        #Delete bind sets
        sets = cmds.ls(type='objectSet')
        for set in sets:
            if 'Bind' in set:
                cmds.delete(set)

        #Delete Sid
        if sid_to_delete:
            cmds.delete(str(sid_to_delete))

        #Delete parent to eyes
        if cmds.objExists('L_Eyes_Jnt_parentConstraint1'):
            cmds.delete('L_Eyes_Jnt_parentConstraint1')
            cmds.parentConstraint('Skull_Upr_Ctrl','L_Eyes_Jnt', mo=True)

        if cmds.objExists('R_Eyes_Jnt_parentConstraint1'):
            cmds.delete('R_Eyes_Jnt_parentConstraint1')
            cmds.parentConstraint('Skull_Upr_Ctrl','R_Eyes_Jnt', mo=True)

        #Create Node
        network_data_node = cmds.createNode('network', n='Mutant_FaceInstall')
        mt.string_attr(network_data_node, 'Date', time.ctime())
        mt.string_attr(network_data_node, 'Face', face_path)
        mt.string_attr(network_data_node, 'Body', body_path)
        mt.string_attr(network_data_node, 'Code', 'from maya import cmds')

        self.connect_node_to_master(node=network_data_node)

        #Do Bsp per geo
        #bsp = cmds.blendShape('Face_geo', 'geo', n='FaceInstall_BSP', frontOfChain=True)[0]
        #cmds.setAttr('{}.Face_geo'.format(bsp), 1)
        for geo in cmds.listRelatives('geo', ad=True, type='transform'):
            #Skips grps
            if geo.endswith('_grp'):
                continue
            try:
                bsp = cmds.blendShape('Face_{}'.format(geo), geo, n='FaceInstall_{}_BSP'.format(geo), frontOfChain=True)[0]
                cmds.setAttr('{}.Face_{}'.format(bsp, geo), 1)
            except Exception as e:
                errors.append(e)

        #Delete temp files
        if not mt.check_dev_mode():
            self.clean_temp_files()

        #Comfim install
        if not errors:
            message = 'Face Install Success'
        else:
            message = str(errors)

        cmds.confirmDialog(title='Face Install issue, Sorry!', m=message)
        cmds.select(network_data_node)

        import pprint
        pprint.pprint(message)

        self.remove_studio_tags_from_face()

        #Custom Steps requested by animation
        self.eyes_follow_head()
        if self.ui.attrs_mode_box.currentText()=='AG':
            self.change_face_vis_to_animation_requests(restore=True, mode='AG')
        elif self.ui.attrs_mode_box.currentText()=='SP':
            self.change_face_vis_to_animation_requests(restore=True, mode='SP')
        elif self.ui.attrs_mode_box.currentText()=='Duck':
            self.change_face_vis_to_animation_requests(restore=True, mode='Duck')
            self.put_attrs_on_head_ctrl()

        self.create_rivets_set()

    #--------------------------------------------------------------------
    def put_attrs_on_head_ctrl(self):
        attrs_from = 'Vis_Ctrl'
        if cmds.objExists(attrs_from):
            ctrl = 'Head_Ctrl'
            attrs = cmds.listAttr(attrs_from, ud=True)
            print('Attrs: {}'.format(attrs))
            for attr in attrs:
                cmds.select(attrs_from)
                print(attrs_from, attr)
                if '___' in attr:
                    mt.line_attr(input=ctrl, name=cmds.getAttr("{}.{}".format(attrs_from, attr), asString=True))
                    continue

                print('{}.{}'.format(attrs_from, attr))

                try:
                    attr_type = cmds.getAttr('{}.{}'.format(attrs_from, attr), type=True)
                except:
                    attr_type = None

                if not attr_type:
                    continue

                if attr_type == 'double':
                    cmds.addAttr(ctrl, ln=attr, proxy="{}.{}".format(attrs_from, attr), at="double",
                                 min=cmds.attributeQuery(attr, node=attrs_from, min=True)[0],
                                 max=cmds.attributeQuery(attr, node=attrs_from, max=True)[0],
                                 )

                elif attr_type == 'double':
                    cmds.addAttr(ctrl, ln=attr, proxy="{}.{}".format(attrs_from, attr), at="double",
                                 min=cmds.attributeQuery(attr, node=attrs_from, min=True)[0],
                                 max=cmds.attributeQuery(attr, node=attrs_from, max=True)[0],
                                 )

                elif attr_type == 'enum':
                    if 'RotateOrder' in attr:
                        continue
                    print(cmds.attributeQuery(attr, node=attrs_from, listEnum=True)[0])
                    cmds.addAttr(ctrl, ln=attr, proxy="{}.{}".format(attrs_from, attr), at="enum",
                                 en=cmds.attributeQuery(attr, node=attrs_from, listEnum=True)[0],
                                 )
        cmds.setAttr(cmds.listRelatives(attrs_from, s=True)[0]+'.v', 0)

    # -------------------------------------------------------------------

    def open_clean(self, rig='Face'):

        cmds.file(new=True, force=True)

        if rig == 'Face':
            if self.ui.custom_face.text():
                file_path = self.ui.custom_face.text()
            else:
                file_path = self.ui.faceBox.currentText()
        else:
            if self.ui.custom_body.text():
                file_path = self.ui.custom_body.text()
            else:
                file_path = self.ui.bodyBox.currentText()


        cmds.file(file_path, open=True)
        self.remove_shapes_node()

        return file_path

    # -------------------------------------------------------------------

    def import_clean(self, rig='Face'):

        cmds.file(new=True, force=True)
        if rig == 'Face':
            file_path = self.ui.faceBox.currentText()
        else:
            file_path = self.ui.bodyBox.currentText()

        cmds.file(file_path, i=True)
        self.remove_shapes_node()

        return file_path

    # -------------------------------------------------------------------
    def remove_shapes_node(self):
        if cmds.objExists('defaultLegacyAssetGlobals'):
            cmds.lockNode('defaultLegacyAssetGlobals', l=False)
            cmds.delete('defaultLegacyAssetGlobals')

    # -------------------------------------------------------------------

    def clean_temp_files(self):
        temp_body = os.path.join(self.temp_folder, 'CleanBodyInstall.ma')
        temp_face = os.path.join(self.temp_folder, 'CleanFaceInstall.ma')
        success_file = os.path.join(self.temp_folder, 'FaceInstallSuccess.ma')
        try:
            os.remove(temp_body)
        except:
            pass
        try:
            os.remove(temp_face)
        except:
            pass
        try:
            os.remove(success_file)
        except:
            pass

    # -------------------------------------------------------------------

    def from_installed_open_face(self):
        data_node = 'Mutant_FaceInstall'
        face_file = cmds.getAttr('{}.Face'.format(data_node), asString=True)
        cmds.file(face_file, open=True, f=True)

    # -------------------------------------------------------------------

    def from_installed_open_body(self):
        data_node = 'Mutant_FaceInstall'
        body_file = cmds.getAttr('{}.Body'.format(data_node), asString=True)
        cmds.file(body_file, open=True, f=True)

    # -------------------------------------------------------------------

    def load_from_node(self):
        attr = 'Mutant_FaceInstall.Code'
        code = cmds.getAttr(attr, asString=True)
        self.ui.custom_code.setPlainText(code)

    def run_custom_code(self):
        attr = 'Mutant_FaceInstall.Code'
        try:exec(cmds.getAttr(attr, asString=True))
        except:mel.eval(cmds.getAttr(attr, asString=True))

    def update_attr(self):
        attr = 'Mutant_FaceInstall.Code'
        code_text = self.ui.custom_code.toPlainText()
        cmds.setAttr(attr, code_text, type='string')

    # -------------------------------------------------------------------

    def add_to_face_sns(self):

        sel = cmds.ls(sl=True)
        mt.mirror_group(input=cmds.ls(sl=True), world=False)
        for each in sel:
            cmds.deformer("SS_Head_Bend_Side", e=True, g=each)
            cmds.deformer("SS_Head_Bend_Front_Back", e=True, g=each)
            cmds.deformer("SS_Head", e=True, g=each)
            print('Added', each)

    # -------------------------------------------------------------------

    def remove_studio_tags_from_face(self):

        if not cmds.objExists('Face_geo'):
            return

        face_geos = cmds.listRelatives('Face_geo', ad=True)
        for geo in face_geos:
            try:geo = cmds.rename(geo, geo.replace('_hi', '_Geo'))
            except:continue
            connections = cmds.listConnections(geo+'.message', p=True)
            if not connections:
                continue
            else:
                for c in connections:
                    cmds.disconnectAttr(geo+'.message', c)


    @undo
    def add_rivets(self):
        sel=cmds.ls(sl=True)
        mt.rivets_ctrls(geometry=sel[-1], selection_ctrls=sel[:-1])
    
    @undo 
    def remove_rivets(self):
        sel=cmds.ls(sl=True)
        mt.remove_rivets_ctrls(selection_ctrls=sel[:-1])

    @undo
    def mouth_control_follow_setup(self, name='Lips'):
        cmds.parentConstraint('Jaw_Ctrl','{}_Dw_Main_Ctrl_Offset_Grp'.format(name), mo = True)
        cmds.parentConstraint('Jaw_Ctrl','Skull_Lwr_Ctrl','L_{}_Main_Ctrl_Offset_Grp'.format(name), mo = True)
        cmds.parentConstraint('Jaw_Ctrl','Skull_Lwr_Ctrl','R_{}_Main_Ctrl_Offset_Grp'.format(name), mo = True)

        cmds.group('{}_Dw_Main_Ctrl'.format(name), n = '{}_Dw_Main_Ctrl_{}Center_Follow_Grp'.format(name, name))
        cmds.group('L_{}_Main_Ctrl'.format(name), n = 'L_{}_Main_Ctrl_{}Center_Follow_Grp'.format(name,name))
        cmds.group('R_{}_Main_Ctrl'.format(name), n = 'R_{}_Main_Ctrl_{}Center_Follow_Grp'.format(name, name))

        lips_controls=['{}_Dw_Main_Ctrl_{}Center_Follow_Grp'.format(name, name),
                    'L_{}_Main_Ctrl_{}Center_Follow_Grp'.format(name, name),
                    'R_{}_Main_Ctrl_{}Center_Follow_Grp'.format(name, name)]
        for lips_control in lips_controls:
            cmds.matchTransform(lips_control, '{}_Center_Ctrl'.format(name), piv = True)
            cmds.connectAttr('{}_Center_Ctrl.translate'.format(name), '{}.translate'.format(lips_control))
            #cmds.connectAttr('{}_Center_Ctrl.rotate'.format(name), '{}.rotate'.format(lips_control))
            cmds.connectAttr('{}_Center_Ctrl.scale'.format(name), '{}.scale'.format(lips_control))

        #R side fixes
        md = cmds.createNode('multiplyDivide', n = 'R_{}_Main_Ctrl_{}Center_Follow_reverse_multiply'.format(name, name))
        cmds.setAttr('{}.input2X'.format(md), -1)
        cmds.setAttr('{}.input2Y'.format(md), -1)
        cmds.setAttr('{}.input2Z'.format(md), -1)
        cmds.connectAttr('{}_Center_Ctrl.tx'.format(name), '{}.input1X'.format(md))
        cmds.connectAttr('{}_Center_Ctrl.ry'.format(name), '{}.input1Y'.format(md))
        cmds.connectAttr('{}_Center_Ctrl.rz'.format(name), '{}.input1Z'.format(md))
        cmds.connectAttr('{}.outputX'.format(md), 'R_{}_Main_Ctrl_{}Center_Follow_Grp.tx'.format(name, name), f = True)
        cmds.connectAttr('{}.outputY'.format(md), 'R_{}_Main_Ctrl_{}Center_Follow_Grp.ry'.format(name, name), f = True)
        cmds.connectAttr('{}.outputZ'.format(md), 'R_{}_Main_Ctrl_{}Center_Follow_Grp.rz'.format(name, name), f = True)

        #Master Rotation fixes on Z w
        sides=['L_', 'R_']
        for side in sides:
            offset_grp = cmds.group('{}{}_Main_Ctrl_{}Center_Follow_Grp'.format(side, name, name), n = '{}Lip_Main_Ctrl_{}Center_Follow_Offset_Grp').format(side, name)
            zero_grp = cmds.group(w=True, em=True, n = '{}{}_Main_Ctrl_rZ_grp'.format(side, name))
            main_offset_ctrl = cmds.group(zero_grp, n = '{}{}_Main_Ctrl_rZ_Offset_grp'.format(side, name))
            cmds.matchTransform(main_offset_ctrl, '{}_Center_Ctrl'.format(name), pos=True, rot=True)
            cmds.connectAttr('{}_Center_Ctrl.rotate'.format(name), '{}.rotate'.format(zero_grp))
            cmds.parent(main_offset_ctrl, '{}{}_Main_Ctrl_Offset_Grp'.format(side, name))
            cmds.parent(offset_grp, zero_grp)

            cmds.setAttr('{}{}_Main_Ctrl_Offset_Grp_parentConstraint1.interpType'.format(side, name), 2)

        print('Finished setting up rivet-less mouth follow setup. ')


    @undo 
    def eyelids_control_follow_setup(self):
        sides = ['L_', 'R_']
    
        for side in sides: 
            cmds.group('{}Eyelids_UpMid_Ctrl'.format(side), n = '{}Eyelids_UpMid_Ctrl_Blinks_Follow_Grp'.format(side))
            cmds.group('{}Eyelids_DwMid_Ctrl'.format(side), n = '{}Eyelids_DwMid_Ctrl_Blinks_Follow_Grp'.format(side))
            cmds.connectAttr('{}EyelidsUprBlink_Ctrl.tx'.format(side), '{}Eyelids_UpMid_Ctrl_Blinks_Follow_Grp.tx'.format(side))
            cmds.connectAttr('{}EyelidsLwrBlink_Ctrl.tx'.format(side), '{}Eyelids_DwMid_Ctrl_Blinks_Follow_Grp.tx'.format(side))
            multD_LU = cmds.createNode('multDoubleLinear', n = '{}Eyelids_UpMid_Ctrl_Blinks_Follow_Grp_ty_mult'.format(side))
            multD_LD = cmds.createNode('multDoubleLinear', n = '{}Eyelids_UpMid_Ctrl_Blinks_Follow_Grp_ty_mult'.format(side))
            cmds.setAttr('{}.input2'.format(multD_LU), -1)
            cmds.setAttr('{}.input2'.format(multD_LD), 0.5)
            cmds.connectAttr('{}EyelidsUprBlink_Ctrl.ty'.format(side), '{}.input1'.format(multD_LU))
            cmds.connectAttr('{}EyelidsLwrBlink_Ctrl.ty'.format(side), '{}.input1'.format(multD_LD))
            cmds.connectAttr('{}.output'.format(multD_LU), '{}Eyelids_UpMid_Ctrl_Blinks_Follow_Grp.ty'.format(side), f = True)
            cmds.connectAttr('{}.output'.format(multD_LD), '{}Eyelids_DwMid_Ctrl_Blinks_Follow_Grp.ty'.format(side), f = True)

        print('Finished setting up rivet-less eyelids follow setup. ')

        #expose the multiply divide to be able to manipulate the influence of this control?

    @undo
    def extra_eyes_button(self):
        self.build_extra_eyes()

    @undo
    def build_extra_eyes(self):
        try:
            from rigSystem.build.face.eye import matchingEyes
            reload(matchingEyes)
        except:
            return False

        #fix eyes_names:
        rename = False
        if cmds.objExists('L_eye_grp'):
            cmds.rename('L_eye_grp', 'L_Eye_grp')
            rename = True
        if cmds.objExists('R_eye_grp'):
            cmds.rename('R_eye_grp', 'R_Eye_grp')
            rename = True
        if cmds.objExists('L_cornea_hi'):
            cmds.rename('L_cornea_hi', 'L_Cornea_hi')
            rename = True
        if cmds.objExists('L_eyeInner_hi'):
            cmds.rename('L_eyeInner_hi', 'L_EyeInner_hi')
            rename = True
        if cmds.objExists('L_eyeOuter_hi'):
            cmds.rename('L_eyeOuter_hi', 'L_EyeOuter_hi')
            rename = True

        if cmds.objExists('R_cornea_hi'):
            cmds.rename('R_cornea_hi', 'R_Cornea_hi')
            rename = True
        if cmds.objExists('R_eyeInner_hi'):
            cmds.rename('R_eyeInner_hi', 'R_EyeInner_hi')
            rename = True
        if cmds.objExists('R_eyeOuter_hi'):
            cmds.rename('R_eyeOuter_hi', 'R_EyeOuter_hi')
            rename = True

        #Fix delete skin and reappy at the end
        geos = ['L_Cornea_hi','L_EyeInner_hi','L_EyeOuter_hi','R_Cornea_hi','R_EyeInner_hi','R_EyeOuter_hi']
        for geo in geos:
            #delete history
            cmds.delete(geo, ch=True)


        #matchingEyes.createEyeSetup()
        # Brings in the BaseMesh_Eyes from the marketplace
        matchingEyes.loadBaseMeshEyes()
        # Duplicates char eye geometries
        duplicates, charEyesGeo = matchingEyes.fromCharSid()
        # List set up eye groups and geometries
        basemeshGroups = matchingEyes.fromBasemeshEyesSid()
        # Parent char eye duplicated geometries under eye setup group
        matchingEyes.parentShapeUnderSetupGrp(basemeshGroups, duplicates)
        # Apply eye setup blendshapes
        eyeSetupGrps = matchingEyes.applyBlendshapes()
        # Parent eye setup group under rig group from char sid
        matchingEyes.parentEyeSetupGrp(eyeSetupGrps)
        # Connect iris and pupil scale attribute to eyes controls
        matchingEyes.connectEyeScaleAttr()
        # Apply final eye blendshapes
        matchingEyes.applyFinalBlendshapes(charEyesGeo, eyeSetupGrps)
        # remove namespace
        matchingEyes.removeNamespaces()

        # Delete Basemesh_Eyes1 sid from scene
        matchingEyes.cmds.delete('Basemesh_Eyes1')

        # re skin
        for geo in ['L_Cornea_hi', 'L_EyeInner_hi', 'L_EyeOuter_hi']:
            cmds.skinCluster(geo, 'L_Eyes_Bnd', tsb=True)

        for geo in ['R_Cornea_hi', 'R_EyeInner_hi', 'R_EyeOuter_hi']:
            cmds.skinCluster(geo, 'R_Eyes_Bnd', tsb=True)

        if rename:
            try:cmds.rename('L_Eye_grp', 'R_eye_grp')
            except:pass
            try:cmds.rename('R_Eye_grp', 'R_eye_grp')
            except:pass
            try:cmds.rename('L_cornea_hi', 'L_Cornea_hi')
            except:pass
            try:cmds.rename('L_eyeInner_hi', 'L_EyeInner_hi')
            except:pass
            try:cmds.rename('L_eyeOuter_hi', 'L_EyeOuter_hi')
            except:pass
            try:cmds.rename('R_cornea_hi', 'R_Cornea_hi')
            except:pass
            try:cmds.rename('R_eyeInner_hi', 'R_EyeInner_hi')
            except:pass
            try:cmds.rename('R_eyeOuter_hi', 'R_EyeOuter_hi')
            except:pass

        cmds.warning('Blendshapes deleted from eyes, please redo them if face rig.')

    # -------------------------------------------------------------------

    def connect_node_to_master(self, node):
        cmds.connectAttr('Mutant_Tools_Grp.nodeState', '{}.nodeState'.format(node))

    # -------------------------------------------------------------------

    def auto_connect_rivets(self):
        ''

    @undo
    def change_face_vis_to_animation_requests(self, show=False, restore=False, mode='AG'):

        all_attrs = ['skullMainCtrls','eyeMidCtrls','eyeTweekCtrls','eyeScaleCtrls','lipsMainCtrls','lipsCenterCtrls','lipsMidCtrls','lipsTweekCtrls','browsMainCtrls',
                     'browsMidCtrls','browsTweekCtrls','cheeksMainCtrls','cheeksMidCtrls','cheeksTweekCtrls','jawMainCtrls','TongueMainCtrl','TongueTweekCtrls','TeethVis','noseMainCtrls',
                     'noseMidCtrls', 'noseTweekCtrls']
        if show:
            for attr in all_attrs and cmds.attributeQuery(attr, node='Vis_Ctrl', exists=True):
                cmds.setAttr('Vis_Ctrl.{}'.format(attr), 1)

        desire_attrs_ag = ['eyeMidCtrls','lipsMainCtrls','lipsMidCtrls','browsMainCtrls','browsMidCtrls','cheeksMainCtrls','jawMainCtrls','TongueMainCtrl']
        desire_attrs_sp = ['eyeMidCtrls','lipsMainCtrls','lipsMidCtrls','browsMainCtrls','browsMidCtrls','cheeksMainCtrls','jawMainCtrls','TongueMainCtrl']
        desire_attrs_duck = ['eyeMidCtrls','lipsMainCtrls','lipsMidCtrls','browsMainCtrls','browsMidCtrls','cheeksMainCtrls','jawMainCtrls','TongueMainCtrl']

        if restore:
            for attr in all_attrs:
                if not cmds.attributeQuery(attr, node='Vis_Ctrl', exists=True):
                    continue
                if cmds.attributeQuery(attr, node='Vis_Ctrl', exists=True):
                    if attr in desire_attrs_ag and mode == 'AG':
                        cmds.setAttr('Vis_Ctrl.{}'.format(attr), 1)
                    elif attr in desire_attrs_sp and mode == 'SP':
                        cmds.setAttr('Vis_Ctrl.{}'.format(attr), 1)
                    elif attr in desire_attrs_duck and mode == 'Duck':
                        cmds.setAttr('Vis_Ctrl.{}'.format(attr), 1)
                    else:
                        cmds.setAttr('Vis_Ctrl.{}'.format(attr), 0)

    def eyes_follow_head(self):
        cmds.setAttr('Eyes_Main_Ctrl.Follow', 0)

    def frame_face(self):
        attr_value = cmds.getAttr('Vis_Ctrl.skullMainCtrls')
        cmds.setAttr('Vis_Ctrl.skullMainCtrls', 1)
        cmds.select('Skull_Lwr_Ctrl','Skull_Upr_Ctrl')
        mel.eval('FrameSelectedWithoutChildren;')
        cmds.setAttr('Vis_Ctrl.skullMainCtrls', attr_value)
        cmds.select(cl=True)
    def frame_body(self):
        cmds.select('Mutant_Tools_Grp')
        mel.eval('FrameSelectedWithoutChildren;')
        cmds.select(cl=True)

    @undo
    def move_master(self):
        cmds.setAttr('Global_Ctrl.translateX', 300)
        cmds.setAttr('Global_Ctrl.translateY', 300)
        cmds.setAttr('Global_Ctrl.translateZ', 300)
        cmds.setAttr('Global_Ctrl.rotateX', 300)
        cmds.setAttr('Global_Ctrl.rotateY', 300)
        cmds.setAttr('Global_Ctrl.rotateZ', 300)
        try:
            cmds.setAttr('Global_Ctrl.scaleX', 5)
            cmds.setAttr('Global_Ctrl.scaleY', 5)
            cmds.setAttr('Global_Ctrl.scaleZ', 5)
        except:
            cmds.setAttr('Global_Ctrl.size', 5)

    @undo
    def restore_master(self):
        cmds.setAttr('Global_Ctrl.translateX', 0)
        cmds.setAttr('Global_Ctrl.translateY', 0)
        cmds.setAttr('Global_Ctrl.translateZ', 0)
        cmds.setAttr('Global_Ctrl.rotateX', 0)
        cmds.setAttr('Global_Ctrl.rotateY', 0)
        cmds.setAttr('Global_Ctrl.rotateZ', 0)
        try:
            cmds.setAttr('Global_Ctrl.scaleX', 1)
            cmds.setAttr('Global_Ctrl.scaleY', 1)
            cmds.setAttr('Global_Ctrl.scaleZ', 1)
        except:
            cmds.setAttr('Global_Ctrl.size', 1)

    # -------------------------------------------------------------------

    #Main Mutant Overwrites
    def mouseDoubleClickEvent(self, event):
        pass

    # ------------------------------------------------

    def mouseMoveEvent(self, event):
        """Move Frameless Ui with it

        Args:
            event:not sure but qt understand it

        Returns:

        """
        if self.scale ==  True:
            return

        if self.current_size_mode == 'big':
            #self.check_size()
            return

        if event.buttons() == QtCore.Qt.NoButton:
            "Simple mouse motion"
        elif event.buttons() == QtCore.Qt.LeftButton:
            delta = QtCore.QPoint(event.globalPos() - self.oldPos)
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.oldPos = event.globalPos()
        elif event.buttons() == QtCore.Qt.RightButton:
            "Right click drag"


    # -------------------------------------------------------------------

    def connect_check_buttons(self):
        for widget in checks_map:
            exec('self.ui.{}.valueChanged.connect(partial(self.connect_slider, checks_map[widget], self.ui.{}))'.format(widget, widget))
            exec('self.ui.{}.setObjectName("{}")'.format(widget, widget))
            exec('self.ui.{}.installEventFilter(self)'.format(widget))

    @undo
    def connect_slider(self, attr, slider, *args):

        slider_value = slider.value() / 10.0
        print(slider_value)

        if isinstance(attr, str) == True:
            cmds.select(attr.split('.')[0])
            cmds.setAttr(attr, slider_value)
        else:
            exec('global check_value; check_value = self.ui.{}.isChecked()'.format(attr[0]))
            if check_value:
                cmds.setAttr(attr[2], slider_value)
                cmds.select(attr[2].split('.')[0])
            else:
                cmds.setAttr(attr[1], slider_value)
                cmds.select(attr[1].split('.')[0])

    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.MouseButtonDblClick:

            if isinstance(checks_map[obj.objectName()], str):
                cmds.setAttr(checks_map[obj.objectName()], 0)
            else:
                cmds.setAttr(checks_map[obj.objectName()][1], 0)
                cmds.setAttr(checks_map[obj.objectName()][2], 0)
            obj.setSliderPosition(0)

        return QtCore.QObject.eventFilter(self, obj, event)

    @undo
    def zero_all(self):
        ctrls = cmds.ls('*{}'.format(nc['ctrl']))
        attrs = [".tx", ".ty", ".tz", ".rx", ".ry", ".rz", ".sx", ".sy", ".sz"]

        for ctrl in ctrls:
            if ctrl == 'Vis_Ctrl':
                continue
            for attr in attrs:
                try:
                    if 's' in attr:
                        cmds.setAttr('{}{}'.format(ctrl , attr), 1)
                    else:
                        cmds.setAttr('{}{}'.format(ctrl , attr), 0)
                except:
                    pass

        for widget in checks_map:
            exec('self.ui.{}.setSliderPosition(0)'.format(widget))

    # -------------------------------------------------------------------

    @undo
    def create_rivets_set(self):
        rivet_targets = [u'R_Cheecks_Mid_Ctrl', u'R_Cheecks_2_Ctrl', u'R_Cheecks_3_Ctrl', u'R_Cheecks_1_Ctrl',
                         u'R_Eyelids_UpStartMid_Ctrl', u'L_Cheecks_1_Ctrl', u'R_Lips_Dw_Ctrl', u'L_Cheecks_0_Ctrl',
                         u'L_Cheecks_3_Ctrl', u'R_Eyelids_Dw_Scale_Ctrl', u'L_Lips_Dw_Ctrl', u'L_Cheecks_2_Ctrl',
                         u'R_Cheecks_0_Ctrl', u'R_Eyelids_DwStart_Ctrl', u'L_Eyelids_Dw_Scale_Ctrl',
                         u'L_Mid_02Lips_Up_Ctrl', u'R_Brow_Driver0_Main_Ctrl', u'L_Brow_Ctrl', u'L_Eyelids_UpMid_Ctrl',
                         u'R_Mid_02Lips_Dw_Ctrl', u'L_Eyelids_UpStartMid_Ctrl', u'R_Mid_01Lips_Up_Ctrl',
                         u'R_Lips_Up_Ctrl', u'R_Mid_01Lips_Dw_Ctrl', u'L_Lips_Up_Ctrl', u'Lips_Dw_Main_Ctrl',
                         u'_MidLips_Dw_Ctrl', u'L_Mid_02Lips_Dw_Ctrl', u'L_Eyelids_UpEnd_Ctrl',
                         u'L_Brow_Driver4_Main_Ctrl', u'L_Eyelids_UpStart_Ctrl', u'L_Mid_01Lips_Dw_Ctrl',
                         u'L_Eyelids_DwEnd_Ctrl', u'L_Eyelids_DwEndMid_Ctrl', u'L_Eyelids_DwStartMid_Ctrl',
                         u'_MidLips_Up_Ctrl', u'L_Brow_Driver2_Main_Ctrl', u'L_Cheecks_Btm_Ctrl',
                         u'L_Eyelids_DwMid_Ctrl', u'R_Brow_Driver4_Main_Ctrl', u'R_Eyelids_UpMid_Ctrl',
                         u'R_Eyelids_DwMid_Ctrl', u'Lips_Up_Main_Ctrl', u'R_Eyelids_DwStartMid_Ctrl',
                         u'L_Cheecks_Mid_Ctrl', u'R_Lips_Main_Ctrl', u'R_Eyelids_DwEnd_Ctrl', u'L_Eyelids_DwStart_Ctrl',
                         u'L_Mid_01Lips_Up_Ctrl', u'R_Eyelids_Up_Scale_Ctrl', u'L_Cheecks_5_Ctrl',
                         u'R_Mid_02Lips_Up_Ctrl', u'L_Lips_Main_Ctrl', u'R_Eyelids_UpEndMid_Ctrl',
                         u'L_Brow_Driver0_Main_Ctrl', u'R_Eyelids_UpEnd_Ctrl', u'R_Cheecks_5_Ctrl',
                         u'L_Eyelids_UpEndMid_Ctrl', u'R_Cheecks_4_Ctrl', u'R_Brow_Driver2_Main_Ctrl', u'R_Brow_Ctrl',
                         u'R_Cheecks_Btm_Ctrl', u'L_Cheecks_Top_Ctrl', u'R_Cheecks_Top_Ctrl', u'R_Eyelids_UpStart_Ctrl',
                         u'L_Eyelids_Up_Scale_Ctrl', u'R_Eyelids_DwEndMid_Ctrl', u'L_Cheecks_4_Ctrl']
        cmds.select('Lips_Up_*_Ctrl')
        rivet_targets.extend(cmds.ls(sl=1))
        cmds.select('Lips_Dw_*_Ctrl')
        rivet_targets.extend(cmds.ls(sl=1))
        cmds.select(clear=1)
        cmds.select(rivet_targets)
        rivet_targets.remove('Lips_Up_Main_Ctrl')
        rivet_targets.remove('Lips_Dw_Main_Ctrl')

        return cmds.sets(n="Face_For_Rivets" )

    # -------------------------------------------------------------------
    @undo
    def eye_postbuild(self):
        from Mutant_Tools.UI.FaceInstall.faceinstall_utils import postbuilds_faceinstall
        reload(postbuilds_faceinstall)
        postbuilds_faceinstall.update_eyes(mirror='True')

    @undo
    def mouth_postbuild(self):
        from Mutant_Tools.UI.FaceInstall.faceinstall_utils import postbuilds_faceinstall
        reload(postbuilds_faceinstall)
        postbuilds_faceinstall.lip_postbuilds()

    @undo
    def create_MouthIn(self):
        from Mutant_Tools.UI.FaceInstall.faceinstall_utils import mouth_faceinstall
        reload(mouth_faceinstall)
        mouth_faceinstall.create_MouthIn()

    @undo
    def create_Mouth_RollPull(self):
        from Mutant_Tools.UI.FaceInstall.faceinstall_utils import mouth_faceinstall
        reload(mouth_faceinstall)
        mouth_faceinstall.create_Mouth_RollPull()

    # -------------------------------------------------------------------


    # CLOSE EVENTS _________________________________
    def closeEvent(self, event):
        ''


# -------------------------------------------------------------------

if __name__ == "__main__":

    try:
        cFaceInstallUI.close()  # pylint: disable=E0601
        cFaceInstallUI.deleteLater()
    except:
        pass
    cFaceInstallUI = FaceInstallUI()
    cFaceInstallUI.show()

# -------------------------------------------------------------------

checks_map = {

    'right_up_blink': 'R_EyelidsUprBlink_Ctrl.translateY',
    'left_up_blink':'L_EyelidsUprBlink_Ctrl.translateY',
    'right_dw_blink':'R_EyelidsLwrBlink_Ctrl.translateY',
    'left_dw_blink':'L_EyelidsLwrBlink_Ctrl.translateY',
    'right_eye_1' : 'R_Eyelids_UpEnd_Ctrl.translateY',
    'right_eye_2' : 'R_Eyelids_UpEndMid_Ctrl.translateY',
    'right_eye_3' : 'R_Eyelids_UpMid_Ctrl.translateY',
    'right_eye_4' : 'R_Eyelids_UpStartMid_Ctrl.translateY',
    'right_eye_5' : 'R_Eyelids_UpStart_Ctrl.translateY',
    'right_eye_6' : 'R_Eyelids_DwEnd_Ctrl.translateY',
    'right_eye_7' : 'R_Eyelids_DwEndMid_Ctrl.translateY',
    'right_eye_8' : 'R_Eyelids_DwMid_Ctrl.translateY',
    'right_eye_9' : 'R_Eyelids_DwStartMid_Ctrl.translateY',
    'right_eye_10' : 'R_Eyelids_DwStart_Ctrl.translateY',
    'left_eye_1' : 'L_Eyelids_UpEnd_Ctrl.translateY',
    'left_eye_2' : 'L_Eyelids_UpEndMid_Ctrl.translateY',
    'left_eye_3' : 'L_Eyelids_UpMid_Ctrl.translateY',
    'left_eye_4' : 'L_Eyelids_UpStartMid_Ctrl.translateY',
    'left_eye_5' : 'L_Eyelids_UpStart_Ctrl.translateY',
    'left_eye_6' : 'L_Eyelids_DwEnd_Ctrl.translateY',
    'left_eye_7' : 'L_Eyelids_DwEndMid_Ctrl.translateY',
    'left_eye_8' : 'L_Eyelids_DwMid_Ctrl.translateY',
    'left_eye_9' : 'L_Eyelids_DwStartMid_Ctrl.translateY',
    'left_eye_10' : 'L_Eyelids_DwStart_Ctrl.translateY',

    'jaw':'Jaw_Ctrl.rotateX',

    'left_lip_updown': ['left_sub_check', 'L_Lips_Main_Ctrl.translateY', 'L_Lips_Sub_Ctrl.translateY'],
    'right_lip_updown': ['right_sub_check','R_Lips_Main_Ctrl.translateY', 'R_Lips_Sub_Ctrl.translateY'],
    'left_lip_sides': ['left_sub_check','L_Lips_Main_Ctrl.translateX', 'L_Lips_Sub_Ctrl.translateX'],
    'right_lip_sides': ['right_sub_check','R_Lips_Main_Ctrl.translateX', 'R_Lips_Sub_Ctrl.translateX'],

    'lip_up' : 'Lips_Up_Main_Ctrl.translateY',
    'lip_down' : 'Lips_Dw_Main_Ctrl.translateY',
    'up_lip_1': 'R_Lips_Up_Ctrl.translateY',
    'up_lip_2': 'R_Mid_02Lips_Up_Ctrl.translateY',
    'up_lip_3': 'R_Mid_01Lips_Up_Ctrl.translateY',
    'up_lip_4': '_MidLips_Up_Ctrl.translateY',
    'up_lip_5': 'L_Mid_01Lips_Up_Ctrl.translateY',
    'up_lip_6': 'L_Mid_02Lips_Up_Ctrl.translateY',
    'up_lip_7': 'L_Lips_Up_Ctrl.translateY',
    'down_lip_1': 'R_Lips_Dw_Ctrl.translateY',
    'down_lip_2': 'R_Mid_02Lips_Dw_Ctrl.translateY',
    'down_lip_3': 'R_Mid_01Lips_Dw_Ctrl.translateY',
    'down_lip_4': '_MidLips_Dw_Ctrl.translateY',
    'down_lip_5': 'L_Mid_01Lips_Dw_Ctrl.translateY',
    'down_lip_6': 'L_Mid_02Lips_Dw_Ctrl.translateY',
    'down_lip_7': 'L_Lips_Dw_Ctrl.translateY',

    'left_brow_up' : 'L_Brow_Ctrl.translateY',
    'left_brow_sides': 'L_Brow_Ctrl.translateX',
    'right_brow_up': 'R_Brow_Ctrl.translateY',
    'right_brow_sides': 'R_Brow_Ctrl.translateX',

    'right_brow_up_1' : 'R_Brow_Driver0_Main_Ctrl.translateY',
    'right_brow_up_2': 'R_Brow_Driver1_Sec_Ctrl.translateY',
    'right_brow_up_3': 'R_Brow_Driver2_Main_Ctrl.translateY',
    'right_brow_up_4': 'R_Brow_Driver3_Sec_Ctrl.translateY',
    'right_brow_up_5': 'R_Brow_Driver4_Main_Ctrl.translateY',
    'left_brow_up_1': 'L_Brow_Driver4_Main_Ctrl.translateY',
    'left_brow_up_2': 'L_Brow_Driver3_Sec_Ctrl.translateY',
    'left_brow_up_3': 'L_Brow_Driver2_Main_Ctrl.translateY',
    'left_brow_up_4': 'L_Brow_Driver1_Sec_Ctrl.translateY',
    'left_brow_up_5': 'L_Brow_Driver0_Main_Ctrl.translateY',

    'right_brow_sides_1': 'R_Brow_Driver0_Main_Ctrl.translateX',
    'right_brow_sides_2': 'R_Brow_Driver1_Sec_Ctrl.translateX',
    'right_brow_sides_3': 'R_Brow_Driver2_Main_Ctrl.translateX',
    'right_brow_sides_4': 'R_Brow_Driver3_Sec_Ctrl.translateX',
    'right_brow_sides_5': 'R_Brow_Driver4_Main_Ctrl.translateX',
    'left_brow_sides_1': 'L_Brow_Driver4_Main_Ctrl.translateX',
    'left_brow_sides_2': 'L_Brow_Driver3_Sec_Ctrl.translateX',
    'left_brow_sides_3': 'L_Brow_Driver2_Main_Ctrl.translateX',
    'left_brow_sides_4': 'L_Brow_Driver1_Sec_Ctrl.translateX',
    'left_brow_sides_5': 'L_Brow_Driver0_Main_Ctrl.translateX',

}