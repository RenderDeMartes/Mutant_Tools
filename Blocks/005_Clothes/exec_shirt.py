from __future__ import absolute_import
from maya import cmds, mel
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

from Mutant_Tools.Utils.External import Ribbonizer
reload(Ribbonizer)

#---------------------------------------------

TAB_FOLDER = '005_Clothes'
PYBLOCK_NAME = 'exec_shirt'

#---------------------------------------------

def create_shirt_block(name = 'Shirt'):

    #---------------------------------------------------
    #---------------------------------------------------
    #---------------------------------------------------


    # Read name conventions as nc[''] and setup as seup['']
    PATH = os.path.dirname(__file__)
    PATH = Path(PATH)
    PATH_PARTS = PATH.parts[:-2]
    FOLDER = ''
    for f in PATH_PARTS:
        FOLDER = os.path.join(FOLDER, f)

    MODULE_FILE = os.path.join(os.path.dirname(__file__), '06_Shirt.json')
    with open(MODULE_FILE) as module_file:
        module = json.load(module_file)

    nc, curve_data, setup = mt.import_configs()

    #---------------------------------------------------
    #---------------------------------------------------
    #---------------------------------------------------

    #name checks and block creation
    name = mt.ask_name(text = module['Name'])
    if cmds.objExists('{}{}'.format(name,nc['module'])):
        cmds.warning('Name already exists.')
        return ''

    block = mt.create_block(name = name, icon = 'Shirt',  attrs = module['attrs'], build_command = module['build_command'], import_command = module['import'])
    config = block[1]
    block = block[0]

    shirt = ['']
    shirt_nurbs = []
    for shirt_name in shirt:
        cmds.select(cl=True)
        circle = mt.curve(type='circleY', name=name + shirt_name + nc['guide'], custom_name=True)
        cmds.parent(circle, block)
        shirt_nurbs.append(circle)

    cmds.select(block)

    print('{} Created Successfully'.format(name))

#create_shirt_block()

#-------------------------

def build_shirt_block():

    nc, curve_data, setup = mt.import_configs()

    mt.check_is_there_is_base()

    block = cmds.ls(sl=True)
    config = cmds.listConnections(block)[1]
    block = block[0]
    guides = cmds.listRelatives(block, ad=True, type='transform')
    name = block.replace(nc['module'],'')

    #use this locator in case parent is set to new locator
    if cmds.getAttr('{}.SetParent'.format(config)) == 'new_locator':
        block_parent = cmds.spaceLocator( n = '{}'.format(str(block).replace(nc['module'],'_Parent' + nc['locator'])))
    else:
        block_parent = cmds.getAttr('{}.SetParent'.format(config))

    if cmds.getAttr('{}.SetGeo'.format(config)) == 'new_cube':
        geos = cmds.polyCube(n = '{}'.format(str(block).replace(nc['module'],'_Geo')))
    else:
        geos = cmds.getAttr('{}.SetGeo'.format(config)).replace(' ', '').split(',')

    #clean a bit
    clean_ctrl_grp = cmds.group(n=name+nc['ctrl']+nc['group'], em=True)
    clean_rig_grp = cmds.group(em=True, n = '{}{}'.format(block.replace(nc['module'],'_RibbonRig'), nc['group']))
    bind_jnt_grp = '{}{}'.format(setup['rig_groups']['bind_joints'], nc['group'])

    cmds.parent(clean_rig_grp, '{}{}'.format(setup['rig_groups']['misc'], nc['group']))
    cmds.parent(clean_ctrl_grp, setup['base_groups']['control'] + nc['group'])

    for guide in guides:
        print(guide)
        new_guide = cmds.duplicate(guide, n = guide.replace(nc['guide'], nc['curve']))
        cmds.parent(new_guide, w=True)
        surface = cmds.bevel(new_guide, w=0, d=1, ed=0, ch=False, n=guide.replace(nc['guide'], nc['nurb']))
        cmds.reverseSurface(ch=False)

        center = cmds.objectCenter(surface, gl=True)
        cmds.xform(surface, pivots=center)
        cmds.delete(cmds.pointConstraint(new_guide, surface))

        ctrl_grp, rig_grp, bnd_grp = Ribbonizer.ribbonize(   surf_tr=surface,
                                                             equal=False,
                                                             num_of_Ctrls=8,
                                                             num_of_Jnts=8,
                                                             prefix=guide.replace(nc['guide'], ''),
                                                             constrain=False,
                                                             add_fk=False,
                                                             wire=False,
                                                             middle_ctrl_pos='Cloth')

        joints = cmds.listRelatives(bnd_grp, ad=True, type='joint')
        cmds.skinCluster(joints, new_guide)

        cmds.parent(ctrl_grp, clean_ctrl_grp)
        cmds.parent(rig_grp, clean_rig_grp)
        cmds.parent(bnd_grp, bind_jnt_grp)

        cmds.parentConstraint(block_parent, clean_ctrl_grp, mo=True)
        cmds.scaleConstraint(block_parent, clean_ctrl_grp, mo=True)

        #do the wire
        wire = cmds.wire(geos[0], n="{}_Wire".format(name), w=new_guide)[0]
        cmds.parent(new_guide, clean_rig_grp)
        print(wire)
        cmds.setAttr('{}.dropoffDistance[0]'.format(wire), cmds.getAttr('{}.WireDropoff'.format(config))*10)
        cmds.parent(new_guide[0]+'BaseWire', clean_rig_grp)

        for geo in geos:
            try:mel.eval('deformer -e -g {} {};'.format(geo, wire))
            except:pass


    print ('Build {} Success'.format(block))



#build_shirt_block()
