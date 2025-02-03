from __future__ import absolute_import
from maya import cmds
from maya import mel
from maya.api import OpenMaya as om2
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
import operator

mt = main_mutant.Mutant()

#---------------------------------------------

TAB_FOLDER = '010_Other'
PYBLOCK_NAME = 'exec_softMod'

#---------------------------------------------


def create_softMod_block(name='target_switches'):
    # Read name conventions as nc[''] and setup as seup['']
    PATH = os.path.dirname(__file__)
    PATH = Path(PATH)
    PATH_PARTS = PATH.parts[:-2]
    FOLDER = ''
    for f in PATH_PARTS:
        FOLDER = os.path.join(FOLDER, f)

    MODULE_FILE = os.path.join(os.path.dirname(__file__), '011_SoftMod.json')
    with open(MODULE_FILE) as module_file:
        module = json.load(module_file)

    nc, curve_data, setup = mt.import_configs()
    #name checks and block creation
    name = mt.ask_name(text = module['Name'])
    if cmds.objExists('{}{}'.format(name,nc['module'])):
        cmds.warning('Name already exists.')
        return ''

    block = mt.create_block(name = name, icon = 'SoftMod',  attrs = module['attrs'], build_command = module['build_command'], import_command = module['import'])
    config = block[1]
    block = block[0]

    print('{} Created succesfully'.format(name))



def build_softMod_block():
    mt.check_is_there_is_base()

    nc, curve_data, setup = mt.import_configs()
    block = cmds.ls(sl=True)
    config = cmds.listConnections(block)[1]
    block = block[0]

    vertex = cmds.getAttr('{}.SetTargetVertex'.format(config))
    ctrl_parent = cmds.getAttr('{}.SetControlParent'.format(config))

    softMod, softMod_handle, ctrl, root = mt.create_softmod(vertex, block.replace(nc['module'], ''))

    cmds.parent(root, ctrl_parent)


    if cmds.getAttr('{}.Mirror'.format(config)):

        if block.startswith('L_'):

            vertex_pos = cmds.xform(vertex, q=1, t=1, ws=1)
            vertex_pos[0] *= -1
            vertex_pos = om2.MPoint(vertex_pos)
            meshFn = om2.MFnMesh(mt.get_dag_path(vertex.split('.')[0]))
            mirror_vtx_id = mt.get_closest_vertex(meshFn, vertex_pos)
            mirror_vtx = vertex.split('[')[0] + '[{}]'.format(mirror_vtx_id)
            print(mirror_vtx)
            m_softMod, m_softModHandle, m_ctrl, m_root = mt.create_softmod(mirror_vtx, block.replace(nc['module'], '').replace('L_', 'R_'))

            m_ctrl_parent = ctrl_parent.replace('L_', 'R_')
            print('mirror ctrl parent = {}'.format(m_ctrl_parent))
            if cmds.objExists(m_ctrl_parent):
                print('Mirror parent exists')
                cmds.parent(m_root, m_ctrl_parent)
            else:
                cmds.parent(m_root, ctrl_parent)

        else:
            print('Block must start with "L_" for mirror to work')
        

    print('Build {} sucess'.format(block))