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

TAB_FOLDER = '010_Other'
PYBLOCK_NAME = 'exec_proxy_attr'

#---------------------------------------------

def create_proxy_attr_block(name = 'Proxy_Attr'):

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

    MODULE_FILE = os.path.join(os.path.dirname(__file__), '007_Proxy_Attr.json')
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

    block = mt.create_block(name = name, icon = 'ProxyAttr',  attrs = module['attrs'], build_command = module['build_command'], import_command = module['import'])
    config = block[1]
    block = block[0]
      
    #cmds.getAttr('{}.AttrName'.format(config)) #get attrs from config
    #cmds.getAttr('{}.AttrName'.format(config), asString = True) #for enums
    #joint_one = mt.create_joint_guide(name = name) #guide base with shapes

    cmds.select(block)

    print('{} Created Successfully'.format(name))

#create_proxy_attr_block()

#-------------------------

def build_proxy_attr_block():

    nc, curve_data, setup = mt.import_configs()

    block = cmds.ls(sl=True)
    config = cmds.listConnections(block)[1]
    name = block[0].replace(nc['module'], '')


    #mt.check_is_there_is_base()

    #use this locator in case parent is set to new locator
    if cmds.getAttr('{}.SetParent'.format(config)) == 'new_locator':
        block_parent = cmds.spaceLocator( n = '{}'.format(str(block).replace(nc['module'],'_Parent' + nc['locator'])))
    else:
        block_parent = cmds.getAttr('{}.SetParent'.format(config))

    attrs_from = cmds.getAttr('{}.SetCopyAttrsFrom'.format(config))

    if cmds.attributeQuery('CtrlShape', n=config, exists=True):
        shape_ctrl = cmds.getAttr(config + '.CtrlShape', asString=True)
    else:
        shape_ctrl = 'cross'


    cmds.select(cl=True)
    ctrl_name = attrs_from.replace(nc['locator'], nc['ctrl'])
    if '|' in ctrl_name:
        ctrl_name = ctrl_name.split('|')[-1]

    ctrl = mt.curve(input='',
                    type=shape_ctrl,
                    rename=True,
                    custom_name=True, name=ctrl_name,
                    size=1,
                    )
    ctrl_root = mt.root_grp()
    mt.hide_attr(input=ctrl, t=True, r=True, s=True, v=True, rotate_order=True, show=False)


    #Get aatrs from wand apply to new
    attrs = cmds.listAttr(attrs_from, ud=True)
    print('Attrs: {}'.format(attrs))
    for attr in attrs:
        cmds.select(attrs_from)
        print(attrs_from, attr)
        if '___' in attr:
            mt.line_attr(input=ctrl, name=cmds.getAttr("{}.{}".format(attrs_from, attr), asString=True))
            continue
        
        print('{}.{}'.format(attrs_from, attr))

        try:
            attr_type = cmds.getAttr('{}.{}'.format(attrs_from, attr), type=True)
        except:
            attr_type=None

        if not attr_type:
            continue

        if attr_type == 'double':
            cmds.addAttr(ctrl, ln=attr, proxy="{}.{}".format(attrs_from, attr), at="double",
                    min=cmds.attributeQuery(attr, node=attrs_from, min=True)[0],
                    max=cmds.attributeQuery(attr, node=attrs_from, max=True)[0],
                    )

        elif attr_type == 'double':
            cmds.addAttr(ctrl, ln=attr, proxy="{}.{}".format(attrs_from, attr), at="double",
                    min=cmds.attributeQuery(attr, node=attrs_from, min=True)[0],
                    max=cmds.attributeQuery(attr, node=attrs_from, max=True)[0],
                    )

        elif attr_type == 'enum':
            if 'RotateOrder' in attr:
                continue
            print(cmds.attributeQuery(attr, node=attrs_from, listEnum=True)[0])
            cmds.addAttr(ctrl, ln=attr, proxy="{}.{}".format(attrs_from, attr), at="enum",
                    en=cmds.attributeQuery(attr, node=attrs_from, listEnum=True)[0],
                    )



    #clean a bit
    clean_ctrl_grp = cmds.group(em=True, name = name + nc['ctrl'] + nc['group'])
    cmds.parent(ctrl_root, clean_ctrl_grp)

    cmds.parent(clean_ctrl_grp, setup['base_groups']['control'] + nc['group'])

    cmds.parentConstraint(block_parent, ctrl_root)

    cmds.scaleConstraint('Global_Ctrl', ctrl_root)

    print ('Build {} Success'.format(block))



#build_proxy_attr_block()
