from maya import cmds
import json
import os

import Mosaic_Tools
import Mosaic_Tools.Utils
from Mosaic_Tools.Utils import main_mosaic
reload(Mosaic_Tools.Utils.main_mosaic)

mt = main_mosaic.Mosaic()

#---------------------------------------------

#Read name conventions as nc[''] and setup as seup['']
PATH = os.path.dirname(__file__)
PATH = PATH.replace('\Blocks//07_Other', '//Config') #change this path depending of the folder

JSON_FILE = (PATH + '/name_conventions.json')
with open(JSON_FILE) as json_file:
	nc = json.load(json_file)
#Read curve shapes info
CURVE_FILE = (PATH + '/curves.json')
with open(CURVE_FILE) as curve_file:
	curve_data = json.load(curve_file)
#setup File
SETUP_FILE = (PATH+'/rig_setup.json')
with open(SETUP_FILE) as setup_file:
	setup = json.load(setup_file)	

#---------------------------------------------

def create_BaseA():

    mt.build_base(size = 3, name = 'Mosaic_Tools')
    print('BaseA Created Successfully'),

#create_limb_base()

#-------------------------

def build_limb_block():
    ''