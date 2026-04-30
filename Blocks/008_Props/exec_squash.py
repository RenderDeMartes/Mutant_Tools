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

#---------------------------------------------

TAB_FOLDER = '008_Props'
PYBLOCK_NAME = 'exec_squash'


#---------------------------------------------

def create_squash_block(name = 'Squash'):

    # Read name conventions as nc[''] and setup as seup['']
    PATH = os.path.dirname(__file__)
    PATH = Path(PATH)
    PATH_PARTS = PATH.parts[:-2]
    FOLDER = ''
    for f in PATH_PARTS:
        FOLDER = os.path.join(FOLDER, f)

    MODULE_FILE = os.path.join(os.path.dirname(__file__), '06_Squash.json')
    with open(MODULE_FILE) as module_file:
        module = json.load(module_file)

    nc, curve_data, setup = mt.import_configs()
    #name checks and block creation
    name = mt.ask_name(text = module['Name'])
    if cmds.objExists('{}{}'.format(name,nc['module'])):
        cmds.warning('Name already exists.')
        return ''

    block = mt.create_block(name = name, icon = 'Squash',  attrs = module['attrs'], build_command = module['build_command'], import_command = module['import'])
    config = block[1]
    block = block[0]
      
    #cmds.getAttr('{}.AttrName'.format(config)) #get attrs from config
    #cmds.getAttr('{}.AttrName'.format(config), asString = True) #for enums
    #joint_one = mt.create_joint_guide(name = name) #guide base with shapes

    cmds.select(block)

    print('{} Created Successfully'.format(name))

#create_squash_block()

#-------------------------

def build_squash_block():

    nc, curve_data, setup = mt.import_configs()

    mt.check_is_there_is_base()

    block = cmds.ls(sl=True)
    config = cmds.listConnections(block)[1]
    block = block[0]
    name = block.replace(nc['module'],'')

    #use this locator in case parent is set to new locator
    if cmds.getAttr('{}.SetParent'.format(config)) == 'new_locator':
        block_parent = cmds.spaceLocator( n = '{}'.format(str(block).replace(nc['module'],'_Parent' + nc['locator'])))
    else:
        block_parent = cmds.getAttr('{}.SetParent'.format(config))

    geos = cmds.getAttr('{}.SetGeo'.format(config), asString=True)
    if ',' in geos:
        geos = geos.split(',')
    else:
        geos = [geos]
    cmds.select(geos)
    rig_grp, ctrl_group = mt.bend_and_squash(name=name, geo=None, parent_grp=block_parent)

    for g in geos:
        reorder_deformers(g)

    #clean a bit
    clean_ctrl_grp = cmds.group(em=True, name = name + nc['ctrl'] + nc['group'])
    clean_rig_grp = cmds.group(em=True, name = name + '_Rig' + nc['group'])

    cmds.parent(clean_rig_grp, '{}{}'.format(setup['rig_groups']['misc'], nc['group']))
    cmds.parent(clean_ctrl_grp, setup['base_groups']['control'] + nc['group'])

    cmds.parent(rig_grp, clean_rig_grp)
    cmds.parent(ctrl_group, clean_ctrl_grp)



    print ('Build {} Success'.format(block))



#build_squash_block()


def reorder_deformers(geo):
    """
    Ensures correct deformer order:
    skinCluster (bottom) → bend front → bend side → squash (top)
    """

    history = cmds.listHistory(geo, pruneDagObjects=True) or []

    skin = None
    bends = []
    squash = None

    for node in history:
        if cmds.nodeType(node) == "skinCluster":
            skin = node
        elif cmds.nodeType(node) == "nonLinear":
            # detect type via name
            if "SS_" in node:
                squash = node
            elif "Side" in node:
                bends.append(("side", node))
            elif "Front_Back" in node:
                bends.append(("front", node))

    # sort bends properly
    bend_front = next((n for t, n in bends if t == "front"), None)
    bend_side = next((n for t, n in bends if t == "side"), None)

    # -----------------------------
    # 🔥 REORDER STACK
    # -----------------------------
    try:
        if skin and bend_front:
            cmds.reorderDeformers(skin, bend_front, geo)

        if bend_front and bend_side:
            cmds.reorderDeformers(bend_front, bend_side, geo)

        if bend_side and squash:
            cmds.reorderDeformers(bend_side, squash, geo)

    except Exception as e:
        print(f"[Reorder Warning] {geo}: {e}")