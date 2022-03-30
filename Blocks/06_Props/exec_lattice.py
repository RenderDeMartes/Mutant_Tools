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

#---------------------------------------------

TAB_FOLDER = '06_Props'
PYBLOCK_NAME = 'exec_lattice'

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

MODULE_FILE = os.path.join(os.path.dirname(__file__),'03_Lattice.json')
with open(MODULE_FILE) as module_file:
	module = json.load(module_file)

#---------------------------------------------

def create_lattice_block(name = 'Lattice'):

    #name checks and block creation
    name = mt.ask_name(text = module['Name'])
    if cmds.objExists('{}{}'.format(name,nc['module'])):
        cmds.warning('Name already exists.')
        return ''

    block = mt.create_block(name = name, icon = 'Lattice',  attrs = module['attrs'], build_command = module['build_command'], import_command = module['import'])
    config = block[1]
    block = block[0]
      
    #cmds.getAttr('{}.AttrName'.format(config)) #get attrs from config
    #cmds.getAttr('{}.AttrName'.format(config), asString = True) #for enums
    #joint_one = mt.create_joint_guide(name = name) #guide base with shapes

    cmds.select(block)

    print('{} Created Successfully'.format(name))

#create_lattice_block()

#-------------------------

def build_lattice_block():

    mt.check_is_there_is_base()

    block = cmds.ls(sl=True)
    config = cmds.listConnections(block)[1]
    block = block[0]
    name = block.replace(nc['module'], '')
    #guide = cmds.listRelatives(block, c=True)[0]

    #groups for later cleaning
    clean_rig_grp = ''
    clean_ctrl_grp = ''
    
    #cmds.getAttr('{}.AttrName'.format(config))
    #cmds.getAttr('{}.AttrName'.format(config), asString = True)

    #orient the joints
    #new_guide = mt.duplicate_and_remove_guides(guide)
    #to_build = [new_guide]

    #use this locator in case parent is set to new locator
    if cmds.getAttr('{}.SetParent'.format(config)) == 'new_locator':
        block_parent = cmds.spaceLocator( n = '{}'.format(str(block).replace(nc['module'],'_Parent' + nc['locator'])))
    else:
        block_parent = cmds.getAttr('{}.SetParent'.format(config))

    #geo to apply lattice to
    if cmds.getAttr('{}.SetGeo'.format(config)) == 'new_cube':
        geo = cmds.polyCube( n = '{}'.format(str(block).replace(nc['module'],'_Geo')))[0]
    else:
        geo = cmds.getAttr('{}.SetParent'.format(config))

    size = cmds.getAttr('{}.CtrlSize'.format(config))
    x_amount = cmds.getAttr('{}.XAmount'.format(config))
    y_amount = cmds.getAttr('{}.YAmount'.format(config))
    z_amount = cmds.getAttr('{}.ZAmount'.format(config))

    # create lattice
    lattice_deformer = cmds.lattice(divisions=(x_amount, y_amount, z_amount), objectCentered=True, ldv=(2, 2, 2), ol=False,
                                    n='{}_Lat_'.format(name), outsideLattice=1)

    # clusters for control lattice points
    clusters =[]
    ctrls =[]
    ctrls_root =[]

    for num in range(x_amount):
        print(num)

    # center one must be relative so it can be aprented to the main lattice
    cmds.select('{}.pt[0:1][2][0]'.format(lattice_deformer[1]), '{}.pt[0:1][2][1]'.format(lattice_deformer[1]))
    cluster_deformer_top = cmds.cluster(n='{}_Top_Cls'.format(name), rel=False)
    top_ctrl = mt.curve(type='square', custom_name=True, name='{}_Top{}'.format(name, nc['ctrl']), size=size)
    mt.assign_color(color='purple')
    mt.hide_attr(v=True)
    top_grp = mt.root_grp()

    # delta mush

    cmds.select(geo)
    if cmds.getAttr('{}.DeltaMush'.format(config)):
        cmds.deltaMush(smoothingIterations=10, envelope=1, smoothingStep=0.5, pinBorderVertices=1)

    # organize a bit
    cluster_grp = cmds.group(cluster_deformer_btm, cluster_deformer_mid, cluster_deformer_top,
                             n='{}_Cls{}'.format(geo[0], nc['group']))
    ctrl_grp = cmds.group(btm_grp, mid_grp, top_grp, n='{}_Lat_Ctrl{}'.format(str(geo[0]), nc['group']))

    util_grp = cmds.group(cluster_grp, lattice_deformer[1], lattice_deformer[2],
                          n='{}_Util{}'.format(geo[0], nc['group']))

    return [util_grp, ctrl_grp, lattice_deformer]


    #clean a bit
    clean_rig_grp = cmds.group(em=True, n = '{}{}'.format(block.replace(nc['module'],'_Rig'), nc['group']))


    print ('Build {} Success'.format(block))



#build_lattice_block()
