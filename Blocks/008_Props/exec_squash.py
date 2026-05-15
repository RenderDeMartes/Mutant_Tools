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
      
    loc_guide = cmds.spaceLocator(n = name + nc['locator'])[0]
    cmds.parent(loc_guide, block)

    bend_guide = cmds.spaceLocator(n = name + "_Bend_Guide" + nc['locator'])[0]
    cmds.parent(bend_guide, block)
    cmds.setAttr(bend_guide + '.ty', 2)

    squash_guide = cmds.spaceLocator(n = name + "_Squash_Guide" + nc['locator'])[0]
    cmds.parent(squash_guide, block)
    cmds.setAttr(squash_guide + '.ty', 4)

    #cmds.getAttr('{}.AttrName'.format(config)) #get attrs from config
    #cmds.getAttr('{}.AttrName'.format(config), asString = True) #for enums
    #joint_one = mt.create_joint_guide(name = name) #guide base with shapes

    if cmds.attributeQuery('UseCustomPivots', node=config, exists=True):
        cmds.connectAttr(config + '.UseCustomPivots', bend_guide + '.v')
        cmds.connectAttr(config + '.UseCustomPivots', squash_guide + '.v')

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

    try:
        guides = cmds.listRelatives(block, c=True, fullPath=True, type='transform') or []
        loc_guide = None
        bend_guide = None
        squash_guide = None
        for guide in guides:
            shapes = cmds.listRelatives(guide, s=True, type='locator')
            if shapes:
                short_name = guide.split('|')[-1]
                if "Bend_Guide" in short_name:
                    bend_guide = guide
                elif "Squash_Guide" in short_name:
                    squash_guide = guide
                else:
                    loc_guide = guide
    except:
        loc_guide = None
        bend_guide = None
        squash_guide = None

    #use this locator in case parent is set to new locator
    if cmds.getAttr('{}.SetParent'.format(config)) == 'new_locator':
        block_parent = cmds.spaceLocator( n = '{}'.format(str(block).replace(nc['module'],'_Parent' + nc['locator'])))
    else:
        block_parent = cmds.getAttr('{}.SetParent'.format(config))

    # Get Squash and Bend booleans
    try:
        squash_enabled = cmds.getAttr('{}.Squash'.format(config))
    except:
        squash_enabled = True
    try:
        bend_enabled = cmds.getAttr('{}.Bend'.format(config))
    except:
        bend_enabled = True

    try:
        use_custom_pivots = cmds.getAttr('{}.UseCustomPivots'.format(config))
    except:
        use_custom_pivots = False

    if not use_custom_pivots:
        bend_guide = None
        squash_guide = None

    geos_attr = cmds.getAttr('{}.SetGeo'.format(config), asString=True)
    if geos_attr:
        if ',' in geos_attr:
            geos = [g.strip() for g in geos_attr.split(',') if g.strip()]
        else:
            geos = [geos_attr.strip()]
    else:
        geos = []
    
    dummy_geo = None
    if not geos:
        dummy_geo = cmds.polyCube(n=name + '_Squash_Dummy_Geo')[0]
        cmds.setAttr(dummy_geo + '.v', 0)
        geos = [dummy_geo]
    
    cmds.select(geos)
    rig_grp, ctrl_group = mt.bend_and_squash(
        name=name, 
        geo=geos, 
        parent_grp=block_parent, 
        squash_enabled=squash_enabled, 
        bend_enabled=bend_enabled, 
        ctrl_guide=loc_guide,
        bend_guide=bend_guide,
        squash_guide=squash_guide
    )

    for g in geos:
        reorder_deformers(g)

    # Apply custom deformer values defined in the block config
    ctrl = "{}_Ctrl_Offset_Ctrl".format(name)
    param_map = {
        'SquashMult':         'SS_{}_mult'.format(name),
        'SquashFactor':       'SS_{}_factor'.format(name),
        'SquashLowBound':     'SS_{}_lowBound'.format(name),
        'SquashHighBound':    'SS_{}_highBound'.format(name),
        'BendFrontMult':      '{}_Bend_Front_Back_mult'.format(name),
        'BendFrontCurvature': '{}_Bend_Front_Back_curvature'.format(name),
        'BendFrontLowBound':  '{}_Bend_Front_Back_lowBound'.format(name),
        'BendFrontHighBound': '{}_Bend_Front_Back_highBound'.format(name),
        'BendSideMult':       '{}_Bend_Side_mult'.format(name),
        'BendSideCurvature':  '{}_Bend_Side_curvature'.format(name),
        'BendSideLowBound':   '{}_Bend_Side_lowBound'.format(name),
        'BendSideHighBound':  '{}_Bend_Side_highBound'.format(name),
    }
    for config_attr, ctrl_attr in param_map.items():
        if cmds.attributeQuery(config_attr, node=config, exists=True):
            if cmds.attributeQuery(ctrl_attr, node=ctrl, exists=True):
                val = cmds.getAttr('{}.{}'.format(config, config_attr), asString=True)
                val = float(val)
                cmds.setAttr('{}.{}'.format(ctrl, ctrl_attr), val)

    # Lock secondary attrs if requested
    try:
        lock_secondary = cmds.getAttr('{}.LockSecondaryAttrs'.format(config))
    except:
        lock_secondary = False
    if lock_secondary:
        secondary_attrs = [
            '{}_Bend_Front_Back_curvature'.format(name),
            '{}_Bend_Front_Back_lowBound'.format(name),
            '{}_Bend_Front_Back_highBound'.format(name),
            '{}_Bend_Side_curvature'.format(name),
            '{}_Bend_Side_lowBound'.format(name),
            '{}_Bend_Side_highBound'.format(name),
            'SS_{}_factor'.format(name),
            'SS_{}_lowBound'.format(name),
            'SS_{}_highBound'.format(name),
        ]
        for attr in secondary_attrs:
            if cmds.attributeQuery(attr, node=ctrl, exists=True):
                full = '{}.{}'.format(ctrl, attr)
                cmds.setAttr(full, lock=True, keyable=False, channelBox=False)

    #clean a bit
    clean_ctrl_grp = cmds.group(em=True, name = name + nc['ctrl'] + nc['group'])
    clean_rig_grp = cmds.group(em=True, name = name + '_Rig' + nc['group'])

    if dummy_geo:
        cmds.parent(dummy_geo, clean_rig_grp)

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