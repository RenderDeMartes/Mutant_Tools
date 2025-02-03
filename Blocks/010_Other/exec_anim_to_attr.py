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

#---------------------------------------------

TAB_FOLDER = '010_Other'
PYBLOCK_NAME = 'exec_posetoattr'

#---------------------------------------------

def create_animtoattr_block(name = 'PoseToAttr'):

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

    MODULE_FILE = os.path.join(os.path.dirname(__file__), '009_Anim_To_Attr.json')
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

    block = mt.create_block(name = name, icon = 'AnimToAttr',  attrs = module['attrs'], build_command = module['build_command'], import_command = module['import'])
    config = block[1]
    block = block[0]

    cmds.select(block)

    print('{} Created Successfully'.format(name))

#create_posetoattr_block()

#-------------------------

def build_animtoattr_block():

    mel.eval('ogs - pause;')

    import pprint

    nc, curve_data, setup = mt.import_configs()

    block = cmds.ls(sl=True)[0]
    config = cmds.listConnections(block)[1]

    attr_node = cmds.getAttr('{}.SetNewAttrNode'.format(config))
    attr_name = cmds.getAttr('{}.NewAttrName'.format(config))
    if attr_node == 'new_locator':
        attr_node = cmds.spaceLocator(n='{}'.format(block.replace(nc['module'], 'AttrNode' + nc['locator'])))[0]
    if cmds.attributeQuery(attr_name, node=attr_node, ex=True):
        anim_attr = '{}.{}'.format(attr_node, attr_name)
    else:
        anim_attr = mt.new_attr(input= attr_node, name = attr_name, min = 0 , max = 1, default = 0)


    cmds.currentTime(-1)
    nodes = cmds.getAttr('{}.SetObject'.format(config))
    nodes = nodes.replace(' ', '')
    nodes = nodes.split(',')
    clean_nodes = []
    for node in nodes:
        if cmds.objExists(node):
            clean_nodes.append(node)
    print(clean_nodes)
    cmds.select(clean_nodes)
    print('Nodes are:', cmds.ls(sl=True, type='transform'))

    cmds.select(nodes)
    print('Nodes are:', cmds.ls(sl=True, type='transform'))

    for node in cmds.ls(sl=True, type='transform'):
        if not cmds.objExists(node):
            continue

        current_frame = cmds.currentTime(0)

        print(node)
        anim = {}
        keys_frames=cmds.keyframe(node, q=True)

        if not keys_frames:
            continue
        for frame in keys_frames:
            cmds.select(node)
            current_frame = cmds.currentTime(frame)
            print(current_frame)
            if current_frame in anim:
                continue
            anim[current_frame] = [
                                    cmds.getAttr('{}.tx'.format(node)),
                                    cmds.getAttr('{}.ty'.format(node)),
                                    cmds.getAttr('{}.tz'.format(node)),
                                    cmds.getAttr('{}.rx'.format(node)),
                                    cmds.getAttr('{}.ry'.format(node)),
                                    cmds.getAttr('{}.rz'.format(node)),
                                    cmds.getAttr('{}.sx'.format(node)),
                                    cmds.getAttr('{}.sy'.format(node)),
                                    cmds.getAttr('{}.sz'.format(node)),
                                    cmds.getAttr('{}.v'.format(node)),
                                    ]
            cmds.select(node)

        pprint.pprint(anim)

        cmds.cutKey(node, s=True)
        cmds.currentTime(0)

        attrs = ['translateX','translateY','translateZ','rotateX','rotateY','rotateZ','scaleX','scaleY','scaleZ','visibility']

        new_node = mt.root_grp(custom = True, custom_name = 'SDK_AnimationPose')[0]

        step = float(cmds.getAttr('{}.AnimStep'.format(config)))
        print('Step is: {}'.format(step))
        cmds.setAttr(anim_attr, 0)

        current_step = 0

        for frame in anim:

            cmds.currentTime(frame)
            try:cmds.setAttr(anim_attr, current_step)
            except Exception as e:
                cmds.error(e, 'We need to made the step a bit smaller')

            for num, value in enumerate(anim[frame]):
                try:
                    cmds.setAttr('{}.{}'.format(new_node, attrs[num]), value)
                    cmds.setDrivenKeyframe('{}.{}'.format(new_node, attrs[num]), currentDriver=anim_attr)
                except:
                    pass

            current_step = current_step + step

        cmds.setAttr(anim_attr, 0)

    current_frame = cmds.currentTime(1)

    mel.eval('ogs - pause;')

    print ('Build {} Success'.format(block))

#build_posetoattr_block()
