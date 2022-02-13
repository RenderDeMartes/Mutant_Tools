from maya import cmds
import json
import imp
import os
from pathlib import Path

import Mutant_Tools
import Mutant_Tools.Utils.Rigging
from Mutant_Tools.Utils.Rigging import main_mutant
imp.reload(Mutant_Tools.Utils.Rigging.main_mutant)

mt = main_mutant.Mutant()

from Mutant_Tools.Utils.IO import Guides
imp.reload(Mutant_Tools.Utils.IO.Guides)
guides = Guides.Guides()

#---------------------------------------------

TAB_FOLDER = '01_Presets'
PYBLOCK_NAME = 'exec_biped180'

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
#Read curve shapes info
CURVE_FILE = os.path.join(FOLDER, 'config', 'curves.json')
with open(CURVE_FILE) as curve_file:
	curve_data = json.load(curve_file)
#setup File
SETUP_FILE = os.path.join(FOLDER, 'config', 'rig_setup.json')
with open(SETUP_FILE) as setup_file:
	setup = json.load(setup_file)

MODULE_FILE = os.path.join(os.path.dirname(__file__),'02_Biped180Game.json')
with open(MODULE_FILE) as module_file:
	module = json.load(module_file)

#---------------------------------------------

def create_biped180game_block(name = 'Biped180Game'):
    #C:\Users\PC\Documents\maya\2022\scripts\Mutant_Tools\Utils\IO\Guide_Data
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
    PATH = os.path.dirname(__file__)
    PATH = Path(PATH)
    filepath = os.path.join(FOLDER, 'Utils','IO','Guide_Data','Biped180Game.ma')
    print('Loading: {}...'.format(filepath))

    cmds.file(filepath, i=True, type="mayaAscii")
    print(filepath)

    print('Created Successfully')

#build_biped180game_block()

#-------------------------

