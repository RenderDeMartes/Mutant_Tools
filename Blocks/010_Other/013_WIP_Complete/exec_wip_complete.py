from __future__ import absolute_import
from maya import cmds
import maya.mel as mel
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

TAB_FOLDER = '010_Other'
PYBLOCK_NAME = 'exec_wip_complete'

#---------------------------------------------

def create_wip_complete_block(name = 'WIP_Complete'):

    PATH = os.path.dirname(__file__)
    PATH = Path(PATH)
    PATH_PARTS = PATH.parts[:-3]
    FOLDER = ''
    for f in PATH_PARTS:
        FOLDER = os.path.join(FOLDER, f)

    MODULE_FILE = os.path.join(os.path.dirname(__file__), '013_WIP_Complete.json')
    with open(MODULE_FILE) as module_file:
        module = json.load(module_file)

    nc, curve_data, setup = mt.import_configs()

    #name checks and block creation
    name = 'WIP_Complete'
    if cmds.objExists('{}{}'.format(name, nc['module'])):
        cmds.warning('Name already exists.')
        return ''

    block = mt.create_block(name = name, icon = 'WIP_Complete', attrs = module['attrs'], build_command = module['build_command'], import_command = module['import'])
    config = block[1]
    block = block[0]

    cmds.select(block)

    print('{} Created Successfully'.format(name))

#create_wip_complete_block()

#-------------------------

def _activate_wip_mode(geo_group = 'geo'):
    """Mirrors HelperUI.activate_wip_mode() logic."""

    # studio groups
    try:
        cmds.setAttr('rig.v', 1)
        cmds.setAttr('bind.v', 1)
        cmds.setAttr('control.v', 1)
    except:
        pass

    # unlock_geo
    try:
        cmds.setAttr('Global_Ctrl.Geo', 0)
    except:
        pass
    if cmds.objExists(geo_group):
        try:
            geos = cmds.listRelatives(geo_group, ad=True)
            for each in geos:
                cmds.setAttr('{0}.overrideEnabled'.format(each), 0)
        except:
            pass

    if cmds.objExists('Mutant_Build'):
        try: cmds.parent('Mutant_Build', w=True)
        except: pass
    if cmds.objExists('Mutant_Tools_Grp'):
        try: cmds.parent('Mutant_Tools_Grp', w=True)
        except: pass
        try: cmds.parent('Ctrl_Grp', 'Mutant_Tools_Grp')
        except: pass
        try: cmds.parent('Rig_Grp', 'Mutant_Tools_Grp')
        except: pass
        try: cmds.parent('Extra_Geo_Grp', 'Mutant_Tools_Grp')
        except: pass
        cmds.setAttr('Mutant_Tools_Grp.v', 1)
    if cmds.objExists('Rig_Grp'):
        try: cmds.parent('Bind_Joints_Grp', 'Rig_Grp')
        except: pass
        cmds.setAttr('Bind_Joints_Grp.v', 1)
        cmds.setAttr('Rig_Grp.v', 1)
    if cmds.objExists('Miscellaneous_Grp'):
        cmds.setAttr('Miscellaneous_Grp.v', 1)

    # unreferece_geo
    try:
        for geo in cmds.listRelatives(geo_group, ad=True):
            cmds.setAttr('{}.overrideEnabled'.format(geo), 1)
            cmds.connectAttr('Global_Ctrl.Geo', '{}.overrideDisplayType'.format(geo), f=True)
    except:
        pass


def _activate_complete_mode(geo_group = 'geo'):
    """Mirrors HelperUI.activate_complete_mode() logic."""

    if cmds.objExists('Mutant_Build'):
        try: cmds.parent('Mutant_Build', 'Template_Grp')
        except: pass
    if cmds.objExists('Mutant_Tools_Grp'):
        try: cmds.parent('Mutant_Tools_Grp', 'rig')
        except: pass
        try: cmds.parent('Ctrl_Grp', 'control')
        except: pass
        try: cmds.parent('Rig_Grp', 'Mutant_Tools_Grp')
        except: pass
        try: cmds.parent('Extra_Geo_Grp', 'Mutant_Tools_Grp')
        except: pass
        if cmds.objExists('rig'):
            cmds.setAttr('rig.v', 0)
            cmds.setAttr('Mutant_Tools_Grp.v', 0)

    if cmds.objExists('Rig_Grp'):
        try: cmds.parent('Bind_Joints_Grp', 'bind')
        except: pass
        cmds.setAttr('Bind_Joints_Grp.v', 0)
        if cmds.objExists('bind'):
            cmds.setAttr('bind.v', 0)
        cmds.setAttr('Rig_Grp.v', 0)
    if cmds.objExists('Miscellaneous_Grp'):
        cmds.setAttr('Miscellaneous_Grp.v', 0)

    if cmds.objExists(geo_group):
        try: cmds.setAttr('{}.v'.format(geo_group), 1)
        except: cmds.setAttr('Global_Ctrl.GeoVis', 1)

    # lock_geo
    try:
        cmds.setAttr('Global_Ctrl.Geo', 2)
    except:
        pass
    if cmds.objExists(geo_group):
        try:
            geos = cmds.listRelatives(geo_group, ad=True)
            for each in geos:
                cmds.setAttr('{0}.overrideEnabled'.format(each), 0)
        except:
            pass

    if cmds.objExists('Ctrl_Grp'):
        for ctrl in cmds.listRelatives('Ctrl_Grp', c=True):
            try: cmds.setAttr('{}.v'.format(ctrl), 1)
            except: pass

    # turn_off_inherith_on_rig_childs
    if cmds.objExists('Mutant_Tools_Grp'):
        mutant_grps = cmds.listRelatives('Mutant_Tools_Grp', c=True)
        if mutant_grps:
            for c in mutant_grps:
                cmds.setAttr('{}.inheritsTransform'.format(c), 0)

    # delete_jaw_tester
    try:
        jaw_tester_bs = cmds.ls('*JawTester*', type='blendShape')
        if jaw_tester_bs:
            cmds.delete(jaw_tester_bs)
        jaw_tester_nodes = cmds.ls('*JawTester*')
        if jaw_tester_nodes:
            cmds.delete(jaw_tester_nodes)
    except:
        pass

    # Tag Controllers
    global_ctrl = 'Global_Ctrl'
    if cmds.objExists(global_ctrl):
        ctrls = cmds.ls('*_Ctrl') + cmds.ls('*_Connected_Crv')
        for ctrl in ctrls:
            if ctrl == global_ctrl:
                continue
            cmds.select(ctrl)
            mel.eval('TagAsController;')
            shapes = cmds.listRelatives(ctrl, shapes=True)
            if shapes:
                for shape in shapes:
                    if (cmds.attributeQuery('hideOnPlayback', node=shape, exists=True) and
                            cmds.attributeQuery('CtrlPlayback', node=global_ctrl, exists=True)):
                        cmds.connectAttr(
                            global_ctrl + '.CtrlPlayback',
                            cmds.listRelatives(ctrl, shapes=True)[0] + '.hideOnPlayback',
                            f=True)

        controllers = cmds.ls(type='controller')
        for tag in controllers:
            if (cmds.attributeQuery('visibilityMode', node=tag, exists=True) and
                    cmds.attributeQuery('CtrlVis', node=global_ctrl, exists=True)):
                cmds.connectAttr(global_ctrl + '.CtrlVis', tag + '.visibilityMode', f=True)


def build_wip_complete_block():

    nc, curve_data, setup = mt.import_configs()

    mt.check_is_there_is_base()

    block = cmds.ls(sl=True)
    # Safely get configuration node
    conns = cmds.listConnections(block, type='network') or []
    if not conns:
        conns = cmds.listConnections(block) or []
        if len(conns) < 2:
            cmds.warning("Could not find configuration node for WIP_Complete block {}".format(block))
            return
        config = conns[1]
    else:
        config = conns[0]
    block = block[0]

    mode = cmds.getAttr('{}.Mode'.format(config), asString=True)
    
    geo_group = 'geo'
    if cmds.attributeQuery('Geometry_Group', node=config, exists=True):
        geo_group = cmds.getAttr('{}.Geometry_Group'.format(config)) or 'geo'
    elif cmds.attributeQuery('Geometry', node=config, exists=True):
        geo_group = cmds.getAttr('{}.Geometry'.format(config)) or 'geo'

    if mode == 'WIP':
        _activate_wip_mode(geo_group)
        print('Build {} - WIP Mode Success'.format(block))
    elif mode == 'COMPLETE':
        _activate_complete_mode(geo_group)
        print('Build {} - COMPLETE Mode Success'.format(block))

#build_wip_complete_block()
