from __future__ import absolute_import
try:
    import importlib;from importlib import reload
except:
    import imp;from imp import reload

import sys
import os
from pathlib import Path

from PySide2 import QtGui, QtWidgets, QtCore
from shiboken2 import wrapInstance

import maya.cmds as cmds
import maya.OpenMayaUI as omui
import Mutant_Tools.UI.VariantManagerSystem.VariantManager as vm

import Mutant_Tools
import Mutant_Tools.Utils.Helpers
from Mutant_Tools.Utils.Helpers import helpers
reload(Mutant_Tools.Utils.Helpers.helpers)

import Mutant_Tools.UI.QtMutantWindow as qMutantWindow

mh = helpers.Helpers()

# QT WIndow!
FOLDER_NAME = 'VariantManagerSystem'
Title = 'VariantManager'
UI_File = 'VariantManager.ui'

# QT WIndow!
PATH = os.path.dirname(__file__)
PATH = Path(PATH)
PATH_PARTS = PATH.parts[:-2]
FOLDER=''
for f in PATH_PARTS:
	FOLDER = os.path.join(FOLDER, f)

IconsPath = os.path.join(FOLDER, 'Icons')

def maya_main_window():
	main_window_ptr = omui.MQtUtil.mainWindow()
	return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)


class VariantManagerUI(qMutantWindow.Qt_Mutant):


    def __init__(self, parent=None):
        super(VariantManagerUI, self).__init__()

        self.setWindowTitle(Title)

        self.designer_loader_child(path=os.path.join(FOLDER, 'UI', FOLDER_NAME), ui_file=UI_File)
        self.set_title(Title)

        self.variant_manager = vm.VariantManager()
        self.variants_ui_dict = {}

        self.create_layout()
        self.create_connections()

        self.make_frameless()


    def create_widgets(self):

        self.title_lb = QtWidgets.QLabel("ESETEBAN EL MEJOR SUPERVISOR DEL MUNDO!!!1<3")
        self.title_lb.setAlignment(QtCore.Qt.AlignCenter)
        font = QtGui.QFont()
        font.bold = True
        font.setCapitalization(QtGui.QFont.Capitalize)
        font.setPointSize(20)
        self.title_lb.setFont(font)

        #QtWidgets.QWidget.parent()
        


    def create_layout(self):

        self.variants_grid = self.ui.variants_gridLayout



    def create_connections(self):
        
        self.ui.reloadUdims_bttn.clicked.connect(self.variant_manager.reload_udims)
        self.ui.openHpShade_bttn.clicked.connect(self.variant_manager.open_hyper_shade)
        self.ui.break_connections_btn.clicked.connect(self.variant_manager.break_sdk_viz_connections)
        self.ui.loadMesh_bttn.clicked.connect(self.load_mesh_cb)
        self.ui.loadMesh_bttn.clicked.connect(self.initialize_variants_dict)


    def initialize_variants_dict(self):
        self.clear_variants_grid()
        
        var_dic = self.variant_manager.update_variant_system()

        variant_list = self.variant_manager.variant_list
        checked=False
        for item in variant_list:
            self.variants_ui_dict[item] = self.Variant(item, var_dic[item], self.variant_manager)
            self.addVariantItem(self.variants_ui_dict[item])

            if not checked:
                self.variants_ui_dict[item].active_variant_rb.setChecked(True)
                checked=True


    def addVariantItem(self, variant_item):

        
        self.variants_grid.addWidget(variant_item.name, self.current_row_index, 0, 1, 1)
        self.variants_grid.addWidget(variant_item.file_path_le, self.current_row_index, 1, 1, 1)
        self.variants_grid.addWidget(variant_item.set_file_btn, self.current_row_index, 2, 1, 1)
        self.variants_grid.addWidget(variant_item.active_variant_rb, self.current_row_index, 3, 1, 1, QtCore.Qt.AlignHCenter)
        self.variants_grid.addWidget(variant_item.set_geo_btn, self.current_row_index, 4, 1, 1)

        self.current_row_index += 1


    def clear_variants_grid(self):
        
        self.current_row_index = 1
        for i in self.variants_ui_dict:
            self.variants_ui_dict[i].delete_variant()

    def load_mesh_cb(self):

        selection = cmds.ls(sl=1)[0]
        print(selection)
        #QtWidgets.QLineEdit.sette
        self.ui.loadMesh_le.setText(selection)
        self.variant_manager.MAIN_MESH = selection




    class Variant():

        def __init__(self, name, file_path, variant_manager):
            self.name = QtWidgets.QLabel(name)
            self.file_path_le = QtWidgets.QLineEdit(file_path)
            self.set_file_btn = QtWidgets.QPushButton('Search')
            self.active_variant_rb = QtWidgets.QRadioButton()
            self.set_geo_btn = QtWidgets.QPushButton('Set Geo')
            self.variant_manager = variant_manager
            self.set_file_btn.clicked.connect(self.search_file)
            self.active_variant_rb.clicked.connect(self.set_active_variant)
            self.set_geo_btn.clicked.connect(self.set_selected_2_variant_viz)
            
            self.set_geo_btn.setMinimumSize(30,30)
            self.active_variant_rb.setMinimumSize(30,30)
            self.set_file_btn.setMinimumSize(30,30)
            self.file_path_le.setMinimumSize(30,30)


        def search_file(self):

            result =  mh.import_window('.png')
            print('search result = {}'.format(result))
            self.file_path_le.setText(result[0])
            self.variant_manager.set_variant_file_path(self.name.text(), result[0])

        def delete_variant(self):
            self.name.deleteLater()
            self.file_path_le.deleteLater()
            self.set_file_btn.deleteLater()
            self.active_variant_rb.deleteLater()
            self.set_geo_btn.deleteLater()

        def set_active_variant(self):
            self.variant_manager.set_active_variant(self.name.text())

        def set_selected_2_variant_viz(self):
            self.variant_manager.set_selected_2_variant_viz(self.name.text())






if __name__ == "__main__":
    try:
        variantManager_dg.close()
        variantManager_dg.deleteLater()
    except:
        pass

    variantManager_dg = VariantManagerUI()
    variantManager_dg.show()

    #4.17