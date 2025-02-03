from __future__ import absolute_import
from maya import cmds
import json
try:
    import importlib;from importlib import reload
except:
    import imp;from imp import reload

import os
from pathlib import Path

import Mutant_Tools
import Mutant_Tools.Utils.Rigging
from Mutant_Tools.Utils.Rigging import main_mutant
reload(Mutant_Tools.Utils.Rigging.main_mutant)

mt = main_mutant.Mutant()

from Mutant_Tools.Utils.IO import Guides
reload(Mutant_Tools.Utils.IO.Guides)
guides = Guides.Guides()

#---------------------------------------------

TAB_FOLDER = '000_Presets'
PYBLOCK_NAME = 'exec_humanFaceTemplate'

#---------------------------------------------

def create_humanFaceTemplate_block(name = 'humanFaceTemplate'):

    nc, curve_data, setup = mt.import_configs()

    # Read name conventions as nc[''] and setup as seup['']
    PATH = os.path.dirname(__file__)
    PATH = Path(PATH)
    PATH_PARTS = PATH.parts[:-2]
    FOLDER = ''
    for f in PATH_PARTS:
        FOLDER = os.path.join(FOLDER, f)

    if cmds.objExists('Mutant_Build'):
        cmds.confirmDialog(title='Ups, Sorry!',
                           message='We already have a build group in the scene, please rename it and reparent it later.',
                           button=['Ok'],
                           defaultButton='Ok',
                           cancelButton='Ok',
                           dismissString='Ok')
        return

    PATH = os.path.dirname(__file__)
    PATH = Path(PATH)
    filepath = os.path.join(FOLDER, 'Utils','IO','Guide_Data','Human_Face_Template.ma')
    print('Loading: {}...'.format(filepath))

    cmds.file(filepath, i=True, type="mayaAscii")
    print(filepath)

    print('Created Successfully')

#create_biped180_block()

#-------------------------

