'''
version: 1.0.0
date: 21/04/2020

#----------------

how to:
import imp
import Mutant_Tools
import Mutant_Tools.Utils.IO
from Mutant_Tools.Utils.IO import NgSkinUtils
imp.reload(Mutant_Tools.Utils.IO.NgSkinUtils)

ngmt = NgSkinUtils.NG_Mutant()
ngmt.FUNC_NAME(argument = '')

#----------------
dependencies:

NG

#----------------
licence: https://www.eulatemplate.com/live.php?token=FGISW7ApRfgywum6murbBmLcusKONzkv
author:  Esteban Rodriguez <info@mutanttools.com>

'''

from maya import cmds
import webbrowser

import os
import json
from maya import cmds
import imp
import glob
from pathlib import Path

import Mutant_Tools
import Mutant_Tools.Utils.IO
from Mutant_Tools.Utils.IO import SkinUtils
imp.reload(Mutant_Tools.Utils.IO.SkinUtils)
skin_utils = SkinUtils.Skinning()

from Mutant_Tools.Utils.Helpers import helpers
imp.reload(Mutant_Tools.Utils.Helpers.helpers)
mh = helpers.Helpers()

#Read name conventions as nc[''] and setup as seup['']
PATH = os.path.dirname(__file__)
PATH = Path(PATH)
PATH = os.path.join(*PATH.parts[:-2], 'Config')

JSON_FILE = (PATH + '/name_conventions.json')
with open(JSON_FILE) as json_file:
	nc = json.load(json_file)


try:
    import ngSkinTools2
    from ngSkinTools2 import api as ngst_api
    from ngSkinTools2.api import *
    from ngSkinTools2.api import init_layers, Layers

except Exception:
    result = cmds.confirmDialog(title='Download ngSkinTools2',
                                message='We need to install ngSkinTools2 in order to use NG Mutant Utils.',
                                button=['Download', 'Cancel'],
                                defaultButton='Download',
                                cancelButton='Cancel',
                                dismissString='Cancel')

    if result == 'Download':
        webbrowser.open("https://www.ngskintools.com/")

#---------------------------------------------

class NG_Mutant(object):

    def __init__(self):

        self.ng_skin = None

    #----------------------------------------------------------------------

    def load_skin_selected(self, path, geo=None):

        if geo is None:
            geo = cmds.ls(sl=True)[0]

        config = ngst_api.InfluenceMappingConfig()
        config.use_distance_matching = True
        config.use_name_matching = False
        ngst_api.import_json(geo, file=path+'\\'+geo+'.json', influences_mapping_config=config )

    #----------------------------------------------------------------------

    def delete_all_nodes(self):
        cmds.delete(cmds.ls(type='ngst2SkinLayerData'))

    #----------------------------------------------------------------------

    def save_skin_selected(self, json_path, geo=None):

        if geo is None:
            geo = cmds.ls(sl=True)[0]

        config = ngst_api.InfluenceMappingConfig()
        config.use_distance_matching = True
        config.use_name_matching = False
        ngst_api.export_json(geo, file=json_path+'\\'+geo+'.json')

    #----------------------------------------------------------------------

    def export_ng_skin_selected(self):
        path = mh.export_window(extension = ".ma")
        if path:
            self.save_skin_selected(path)

    # ----------------------------------------------------------------------------------------------------------------

    def import_ng_skin_selected(self):
        path = mh.import_window(extension = ".ma")
        if path:
            self.load_skin_selected(path)

    # ----------------------------------------------------------------------------------------------------------------

    def import_all_skins(self, keep_nodes=False, path=None):

        if path is None:
            path = mh.folder_window()
        if not path:
            return False

        geos = glob.glob(path+'\\*')

        for geo in geos:
            geo = geo.replace('.json','')
            geo = geo.replace(path+'\\','')

            try:
                skin_utils.bind_to_bnd(geo=geo)
                self.load_skin_selected(path, geo)
                print('imported success:: {}'.format(geo))
            except:
                print('Error With:: {}'.format(geo))

        if keep_nodes == False:
            print('Deleted all NgSkin nodes')
            self.delete_all_nodes()

    # ----------------------------------------------------------------------------------------------------------------

    def export_all_skins(self):
        self.initialize_all_skins()

        geos = skin_utils.get_all_geo_with_skin()

        path = mh.folder_window()
        if not path:
            return
        print(path)
        for geo in geos:
            try:
                self.save_skin_selected(path, geo)
                print('Exported success:: {}'.format(geo))
            except:
                print('Error With:: {}'.format(geo))

        self.delete_all_nodes()

    # ----------------------------------------------------------------------------------------------------------------

    def initialize_all_skins(self):
        for skin_cluster in skin_utils.get_skins():
            init_layers(skin_cluster)

    # ----------------------------------------------------------------------------------------------------------------

    def export_selected_skin(self):
        self.initialize_all_skins()

        geos = cmds.ls(sl=True)

        path = mh.folder_window()
        if not path:
            return
        print(path)
        for geo in geos:
            try:
                self.save_skin_selected(path, geo)
                print('Exported success:: {}'.format(geo))
            except:
                print('Error With:: {}'.format(geo))


        self.delete_all_nodes()

    # ----------------------------------------------------------------------------------------------------------------

    def import_selected_skins(self, keep_nodes=False, path=None):

        if path is None:
            path = mh.folder_window()
        if not path:
            return False

        geos = glob.glob(path+'\\*')
        selected_geos = []
        selectiopn = cmds.ls(sl=True)
        for g in selection:
            if g in geos:
                selected_geos.append(g)

        for geo in selected_geos:
            geo = geo.replace('.json','')
            geo = geo.replace(path+'\\','')

            try:
                skin_utils.bind_to_bnd(geo=geo)
                self.load_skin_selected(path, geo)
                print('imported success:: {}'.format(geo))
            except:
                print('Error With:: {}'.format(geo))

        if keep_nodes == False:
            print('Deleted all NgSkin nodes')
            self.delete_all_nodes()

    # ----------------------------------------------------------------------------------------------------------------
