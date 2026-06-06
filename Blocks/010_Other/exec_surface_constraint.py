from __future__ import absolute_import, division
from maya import cmds
import json
try:
    import importlib
    from importlib import reload
except:
    import imp
    from imp import reload

import os
from pathlib import Path

import Mutant_Tools
import Mutant_Tools.Utils.Rigging
from Mutant_Tools.Utils.Rigging import main_mutant
reload(Mutant_Tools.Utils.Rigging.main_mutant)

mt = main_mutant.Mutant()

#---------------------------------------------

TAB_FOLDER = '010_Other'
PYBLOCK_NAME = 'exec_surface_constraint'

#---------------------------------------------


def get_vertex_skin_data(vertex, minimum_weight=0.01):
    """
    Gets all relevant skinning influences and weights from a vertex.

    Args:
        vertex (str):
            Vertex component name.

        minimum_weight (float):
            Minimum weight threshold to keep.

    Returns:
        tuple(list[str], list[float]):
            Relevant joints and their values.

    Raises:
        RuntimeError:
            If vertex is invalid or has no skinCluster.
    """

    # Validate vertex exists
    if not cmds.objExists(vertex):
        raise RuntimeError("Vertex does not exist: {}".format(vertex))

    # Make sure it is actually a vertex
    if ".vtx[" not in vertex:
        raise RuntimeError("{} is not a polygon vertex.".format(vertex))

    obj = vertex.split(".")[0]

    # Find skinCluster
    skin_clusters = cmds.ls(
        cmds.listHistory(obj),
        type="skinCluster"
    )

    if not skin_clusters:
        raise RuntimeError(
            "Object '{}' has no skinCluster.".format(obj)
        )

    skin_cluster = skin_clusters[0]

    # Get values
    skin_values = cmds.skinPercent(
        skin_cluster,
        vertex,
        query=True,
        value=True
    )

    joint_values = cmds.skinPercent(
        skin_cluster,
        vertex,
        query=True,
        transform=None
    )

    relevant_joints = []
    relevant_values = []

    for value, jnt in zip(skin_values, joint_values):

        if value > minimum_weight:
            relevant_joints.append(jnt)
            relevant_values.append(value)

    if not relevant_joints:
        raise RuntimeError(
            "Vertex '{}' has no valid skin influences.".format(vertex)
        )

    return relevant_joints, relevant_values


def create_surface_constraint_block(name='SurfaceConstraint'):

    # Read name conventions as nc[''] and setup as setup['']
    PATH = os.path.dirname(__file__)
    PATH = Path(PATH)
    PATH_PARTS = PATH.parts[:-2]
    FOLDER = ''
    for f in PATH_PARTS:
        FOLDER = os.path.join(FOLDER, f)

    MODULE_FILE = os.path.join(os.path.dirname(__file__), '014_SurfaceConstraint.json')
    with open(MODULE_FILE) as module_file:
        module = json.load(module_file)

    nc, curve_data, setup = mt.import_configs()

    # name checks and block creation
    name = mt.ask_name(text=module['Name'])
    if cmds.objExists('{}{}'.format(name, nc['module'])):
        cmds.warning('Name already exists.')
        return ''

    block = mt.create_block(
        name=name,
        icon='SurfaceConstraint',
        attrs=module['attrs'],
        build_command=module['build_command'],
        import_command=module['import']
    )
    config = block[1]
    block = block[0]

    cmds.select(block)

    print('{} Created Successfully'.format(name))

#create_surface_constraint_block()

#-------------------------


def build_surface_constraint_block():

    nc, curve_data, setup = mt.import_configs()
    mt.check_is_there_is_base()

    block = cmds.ls(sl=True)
    if not block:
        cmds.warning('Select the block to build.')
        return

    config = cmds.listConnections(block)[1]
    block = block[0]
    name = block.replace(nc['module'], '')

    # Get attributes from config
    vertices_str = cmds.getAttr('{}.FloatSetVertices'.format(config), asString=True).replace(' ', ' ')
    controls_str = cmds.getAttr('{}.SetControls'.format(config), asString=True)
    min_weight = cmds.getAttr('{}.MinWeight'.format(config))/100

    # Parse vertices and controls
    vertices_list = [v.strip() for v in vertices_str.split(',') if v.strip()]
    controls_list = [c.strip() for c in controls_str.split(',') if c.strip()]

    # Validate matching lengths
    if len(vertices_list) != len(controls_list):
        cmds.warning(
            'Vertices and Controls must have the same count.\n'
            'Vertices: {}\nControls: {}'.format(len(vertices_list), len(controls_list))
        )
        return

    if not vertices_list:
        cmds.warning('No vertices or controls specified.')
        return

    # Build surface constraints
    _build_surface_constraints(
        name=name,
        vertices=vertices_list,
        controls=controls_list,
        min_weight=min_weight,
        nc=nc
    )

    print('Surface constraints built for {}'.format(name))


def _build_surface_constraints(name, vertices, controls, min_weight, nc):
    """
    Create surface constraints on controls based on vertex skinning.

    Args:
        name (str): Base name for this build
        vertices (list[str]): List of vertex components
        controls (list[str]): List of control/group names
        min_weight (float): Minimum influence weight threshold (Number gets divided by 100 in build function)
        nc (dict): Naming conventions dictionary
    """

    for vertex, ctrl in zip(vertices, controls):

        # Validate both exist
        if not cmds.objExists(vertex):
            cmds.warning('Vertex does not exist: {}'.format(vertex))
            continue

        if not cmds.objExists(ctrl):
            cmds.warning('Control does not exist: {}'.format(ctrl))
            continue

        try:
            # Get skin data from vertex
            relevant_joints, relevant_values = get_vertex_skin_data(vertex, min_weight)

            # Create offset group for the control
            offset_group = mt.root_grp(input=ctrl, custom=True, custom_name='_surfConstr')[0]

            # Zero out the control's rotations and scales only if they're not locked
            for attr in ['rx', 'ry', 'rz']:
                if not cmds.getAttr('{}.{}'.format(ctrl, attr), lock=True):
                    cmds.setAttr('{}.{}'.format(ctrl, attr), 0)
            for attr in ['sx', 'sy', 'sz']:
                if not cmds.getAttr('{}.{}'.format(ctrl, attr), lock=True):
                    cmds.setAttr('{}.{}'.format(ctrl, attr), 1)

            # Zero out the offset group rotations and reset scales to 1
            for attr in ['rx', 'ry', 'rz']:
                if not cmds.getAttr('{}.{}'.format(offset_group, attr), lock=True):
                    cmds.setAttr('{}.{}'.format(offset_group, attr), 0)
            for attr in ['sx', 'sy', 'sz']:
                if not cmds.getAttr('{}.{}'.format(offset_group, attr), lock=True):
                    cmds.setAttr('{}.{}'.format(offset_group, attr), 1)

            # Create parent constraint on the offset group
            new_constraint = cmds.parentConstraint(
                relevant_joints,
                offset_group,
                mo=True
            )[0]

            # Apply weights
            for num, (jnt, val) in enumerate(zip(relevant_joints, relevant_values)):
                cmds.setAttr(
                    "{}.{}W{}".format(
                        new_constraint,
                        jnt,
                        num
                    ),
                    val
                )

            # Shortest interpolation
            cmds.setAttr(
                "{}.interpType".format(new_constraint),
                2
            )

            print('Attached {} using skinning from {}'.format(ctrl, vertex))

        except RuntimeError as e:
            cmds.warning(str(e))
            continue
