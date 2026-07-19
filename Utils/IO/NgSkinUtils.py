from __future__ import absolute_import
'''
version: 1.0.0
date: 21/04/2020

#----------------

how to:
try:
    import importlib;from importlib import reload
except:
    import imp;from imp import reload

import Mutant_Tools
import Mutant_Tools.Utils.IO
from Mutant_Tools.Utils.IO import NgSkinUtils
reload(Mutant_Tools.Utils.IO.NgSkinUtils)

ngmt = NgSkinUtils.NG_Mutant()
ngmt.FUNC_NAME(argument = '')

#----------------
dependencies:

NG

#----------------
www.mutanttools.com
author:  Esteban Rodriguez <info@mutanttools.com>

'''

from maya import cmds
import webbrowser

import os
import json
from maya import cmds
try:
    import importlib;from importlib import reload
except:
    import imp;from imp import reload

import glob
from pathlib import Path

import Mutant_Tools
import Mutant_Tools.Utils.IO
from Mutant_Tools.Utils.IO import SkinUtils
reload(Mutant_Tools.Utils.IO.SkinUtils)
skin_utils = SkinUtils.Skinning()

from Mutant_Tools.Utils.Helpers import helpers
reload(Mutant_Tools.Utils.Helpers.helpers)
mh = helpers.Helpers()

#Read name conventions as nc[''] and setup as seup['']
PATH = os.path.dirname(__file__)
PATH = Path(PATH)
PATH_PARTS = PATH.parts[:-2]
FOLDER=''
for f in PATH_PARTS:
	FOLDER = os.path.join(FOLDER, f)

JSON_FILE = os.path.join(FOLDER, 'config', 'name_conventions.json')
with open(JSON_FILE) as json_file:
	nc = json.load(json_file)

try:
    import ngSkinTools2
    from ngSkinTools2 import api as ngst_api
    from ngSkinTools2.api import *
    from ngSkinTools2.api import init_layers, Layers

except Exception :
    # result = cmds.confirmDialog(title='Download ngSkinTools2',
    #                             message='We need to install ngSkinTools2 in order to use NG Mutant Utils.',
    #                             button=['Download', 'Cancel'],
    #                             defaultButton='Download',
    #                             cancelButton='Cancel',
    #                             dismissString='Cancel')


    # if result == 'Download':
    #     webbrowser.open("https://www.ngskintools.com/")

    ''

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
        ngst_api.import_json(geo, file=os.path.join(path, geo, '.json'), influences_mapping_config=config )

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
        ngst_api.export_json(geo, file=os.path.join(json_path, geo, '.json'))

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

#---------------------------------------------
# Folder-based save/load all (mirrors EasySkin.save_all_skins_to / load_all_skins_from)
#---------------------------------------------

def _ngskintools_available():
    if 'ngst_api' not in globals():
        cmds.warning('ngSkinTools2 is not installed/loaded. Cannot save/load NG Skin layers.')
        return False
    return True


def save_all_layers_to(folder_path='', accept_errors=True):

    if not _ngskintools_available():
        return

    if not folder_path:
        folder_path = mh.folder_window()
        print(folder_path)
    if not folder_path:
        return

    geos = skin_utils.get_all_geo_with_skin()
    if not geos:
        cmds.warning('No skinned geo found in the scene')
        return

    saved_geos = []
    errors = []
    from Mutant_Tools.UI.ProgressBar import load_progress_bar
    reload(load_progress_bar)
    cProgressBarUI = load_progress_bar.ProgressBarUI(items=geos, title='Saving NG Skin Layers')
    cProgressBarUI.show()
    try:
        for num, geo in enumerate(geos):
            cProgressBarUI.set_percent(num)
            try:
                skin = skin_utils.get_skin_from_geo(geo)
                if not skin:
                    continue
                # Make sure a base layer exists to export (no-op if layers already set up)
                init_layers(skin)

                safe_geo_name = geo.replace(':', '__NS__')
                json_path = os.path.join(folder_path, safe_geo_name + '.json')
                ngst_api.export_json(geo, file=json_path)
                saved_geos.append(geo)
            except Exception as e:
                errors.append('{}: {}'.format(geo, e))
                if not accept_errors:
                    raise
    finally:
        cProgressBarUI.close()

    if errors:
        for e in errors:
            print(e)
        cmds.warning('Saved {} NG Skin layer(s) with {} error(s). Check Script Editor for details.'.format(len(saved_geos), len(errors)))

    return {
        'saved_geos': saved_geos,
        'errors': errors,
    }


def load_all_layers_from(folder_path='', accept_errors=True):

    if not _ngskintools_available():
        return

    if not folder_path:
        folder_path = mh.folder_window()
    if not folder_path:
        return

    json_files = glob.glob(os.path.join(folder_path, '*.json'))
    if not json_files:
        cmds.warning('No NG Skin layer files on selected folder')
        return

    config = ngst_api.InfluenceMappingConfig()
    config.use_distance_matching = True
    config.use_name_matching = False

    loaded_geos = []
    skipped_missing = []
    errors = []
    from Mutant_Tools.UI.ProgressBar import load_progress_bar
    reload(load_progress_bar)
    cProgressBarUI = load_progress_bar.ProgressBarUI(items=json_files, title='Loading NG Skin Layers')
    cProgressBarUI.show()
    try:
        for num, file in enumerate(json_files):
            cProgressBarUI.set_percent(num)
            geo = os.path.splitext(os.path.basename(file))[0].replace('__NS__', ':')
            if not cmds.objExists(geo):
                skipped_missing.append(geo)
                continue
            try:
                ngst_api.import_json(geo, file=file, influences_mapping_config=config)
                loaded_geos.append(geo)
            except Exception as e:
                errors.append('{}: {}'.format(geo, e))
                if not accept_errors:
                    raise
    finally:
        cProgressBarUI.close()

    if errors:
        for e in errors:
            print(e)
        cmds.warning('Loaded {} NG Skin layer(s) with {} error(s). Check Script Editor for details.'.format(len(loaded_geos), len(errors)))

    print('NG Skin Layers Import Complete')
    return {
        'loaded_geos': loaded_geos,
        'skipped_missing': skipped_missing,
        'errors': errors,
    }
