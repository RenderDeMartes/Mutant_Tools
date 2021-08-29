'''
version: 1.0.0
date: 21/04/2020

#----------------

how to:

import Mutant_Tools
import Mutant_Tools.Utils.Deformers
from Mutant_Tools.Utils.Deformers import NgSkinUtils
imp.reload(Mutant_Tools.Utils.Deformers.NgSkinUtils)

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

import Mutant_Tools
import Mutant_Tools.Utils.Deformers
from Mutant_Tools.Utils.Deformers import SkinUtils
imp.reload(Mutant_Tools.Utils.Deformers.SkinUtils)
skin = SkinUtils.Skinning()

#Read name conventions as nc[''] and setup as seup['']
PATH = os.path.dirname(__file__)
PATH = PATH.replace('\\Utils\\Deformers', '//Config')

JSON_FILE = (PATH + '/name_conventions.json')
with open(JSON_FILE) as json_file:
	nc = json.load(json_file)


try:
    import ngSkinTools2
    from ngSkinTools2 import api as ngst_api
    from ngSkinTools2.api import *

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
        ''

    #----------------------------------------------------------------------

    def load_skin(self, json_path, geo=None):


        if geo is None:
            geo = cmds.ls(sl=True)[0]

        config = ngst_api.InfluenceMappingConfig()
        config.use_distance_matching = True
        config.use_name_matching = False
        ngst_api.import_json(geo, file=json_path, influences_mapping_config=config )

    #----------------------------------------------------------------------

    def delete_all_nodes(self):
        cmds.delete(cmds.ls(type='ngst2SkinLayerData'))
