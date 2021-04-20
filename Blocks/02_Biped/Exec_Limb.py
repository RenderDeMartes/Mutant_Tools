from maya import cmds
import json
import imp
import os

import Mosaic_Tools
import Mosaic_Tools.Utils
from Mosaic_Tools.Utils import main_mosaic
imp.reload(Mosaic_Tools.Utils.main_mosaic)

mt = main_mosaic.Mosaic()

#---------------------------------------------

#Read name conventions as nc[''] and setup as seup['']
PATH = os.path.dirname(__file__)
PATH = PATH.replace('\Blocks//02_Biped', '//Config') #change this path depending of the folder

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

def create_limb_base(name = 'Limb'):

    #name checks and block creation
    name = mt.ask_name(text = name)
    if cmds.objExists('{}{}'.format(name,nc['module'])):
        cmds.warning('Name already exists.')
        return ''

    limb_block = mt.create_block(name = name, icon = 'Limb' )
    limb_config = limb_block[]
    limb_block = limb_block[0]


    #add attrs to the Limb Block for the UI to read

    #limb base create
    cmds.select(cl=True)
    joint_one = mt.create_joint_guide(name = name)
    cmds.move(0,0,0)
    joint_two = mt.create_joint_guide(name = name)
    cmds.move(10,0,0)    
    joint_three = mt.create_joint_guide(name = name)
    cmds.move(20,0,0)
    cmds.parent(joint_three, joint_two)
    cmds.parent(joint_two, joint_one)

    cmds.parent(joint_one, limb_block)
    cmds.select(cl=True)



    print('Limb Base Created Successfully'),

#create_limb_base()

#-------------------------

def build_limb_block():
    ''