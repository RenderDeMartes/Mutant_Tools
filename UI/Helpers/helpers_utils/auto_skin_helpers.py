from __future__ import absolute_import
import maya.cmds as cmds
from maya.api import OpenMaya as om2
import math
import ngSkinTools2.api as ngskin2


def get_component_index(component):
    s, e = component.index('['), component.index(']')
    return int(component[s + 1:e])


def traverseAndAdd(dag_path=None, edge=None, steps=10, joint_edges={}, current_step=0, edge_loop={}):
    # print("curren_step = {} , steps = {}".format(current_step, steps))
    if current_step < steps:
        current_step += 1
        # create iterator and set it to target edge
        edge_it = om2.MItMeshEdge(dag_path)
        edge_it.setIndex(edge)

        connected_edges = edge_it.getConnectedEdges()
        # print('connected edges = {}'.format(connected_edges))
        for connected_edge in connected_edges:
            if connected_edge in edge_loop and connected_edge not in joint_edges:
                joint_edges.add(connected_edge)
                traverseAndAdd(dag_path, connected_edge, steps, joint_edges, current_step, edge_loop)


def get_closest_joint_per_vertex(mesh, vertices=[]):
    influences = ngskin2.list_influences(mesh)
    vertex_joint = {}

    for vertex in vertices:
        current_min_distance = 1000
        current_min_joint = ()
        current_min_index = None
        for index, inf in enumerate(influences):
            vertex_pos = cmds.xform('{}.vtx[{}]'.format(mesh, vertex), q=1, t=1, ws=1)
            # print(vertex_pos)
            vertex_pos = om2.MVector(*vertex_pos)
            joint_pos = inf.pivot
            # print(joint_pos)
            joint_pos = om2.MVector(*joint_pos)
            distance = (joint_pos - vertex_pos).length()
            if distance < current_min_distance:
                current_min_distance = distance
                current_min_joint = inf
                current_min_index = index
        vertex_joint[vertex] = current_min_joint
        influences.pop(current_min_index)
    return vertex_joint


def skin_edge_loop_joints(mesh='', edge_loop='', joint_range=10):
    # get loop as array of ints and turn it into a set
    lips_loop_indices = [get_component_index(e) for e in edge_loop]
    lips_loop_indices = set(lips_loop_indices)

    # convert edge loop to vertices
    lips_vertices = cmds.polyListComponentConversion(edge_loop, fromEdge=True, toVertex=True)
    lips_vertices = cmds.filterExpand(lips_vertices, selectionMask=31)
    lips_vertices_index = [get_component_index(v) for v in lips_vertices]

    # get a dict associating each vertex with its closest joint
    vertex_2_joint = get_closest_joint_per_vertex(mesh, vertices=lips_vertices_index)

    # prepare for weight painting
    skin_cls = ngskin2.get_related_skin_cluster(mesh)
    layers = ngskin2.init_layers(skin_cls)
    base_layer = layers.add('base weights')
    null_joint_index = next((inf.logicalIndex for inf in ngskin2.list_influences(skin_cls) if
                             inf.path_name().split('|')[-1] == 'Null_Local_Bnd'), None)
    ngskin2.assign_from_closest_joint(skin_cls, base_layer, [null_joint_index])

    target_joints_layer = layers.add('target_joints')

    try:
        settings = ngskin2.FloodSettings()
        settings.mode = ngskin2.PaintMode.replace
        settings.intensity = 1
    except:
        from ngSkinTools2.api import (
            Layers,
            NamedPaintTarget,
            PaintModeSettings,
            flood_weights,
            PaintMode
        )
        settings = PaintModeSettings()
        settings.mode = PaintMode.replace
        settings.intensity = 1

    # convert selection to selection list

    cmds.select(lips_vertices)

    selection_list = om2.MSelectionList()
    selection_list = om2.MGlobal.getActiveSelectionList()

    it_sel_list = om2.MItSelectionList(selection_list, om2.MFn.kMeshVertComponent)

    while not it_sel_list.isDone():
        dagPath, component = it_sel_list.getComponent()
        vert_it = om2.MItMeshVertex(dagPath, component)
        while not vert_it.isDone():
            #print(vert_it.index())
            cmds.select(clear=1)
            # om.MItMeshVertex.getConnectedEdges
            edges = vert_it.getConnectedEdges()
            perp_edges = []
            for e in edges:
                if e not in lips_loop_indices:
                    perp_edges.append(e)
                    cmds.select('{}.e[{}]'.format(mesh, e), add=1)
            # continue
            edge_loop = set(cmds.polySelect(mesh, el=perp_edges[0], noSelection=1))
            joint_edges = set(perp_edges)
            traverseAndAdd(dagPath, perp_edges[0], joint_range, joint_edges, 0, edge_loop)
            traverseAndAdd(dagPath, perp_edges[1], joint_range, joint_edges, 0, edge_loop)
            for joint_edge in joint_edges:
                cmds.select('{}.e[{}]'.format(mesh, joint_edge), add=1)

            try:
                ngskin2.flood_weights(layer=target_joints_layer, influence=vertex_2_joint[vert_it.index()].logicalIndex,
                                  settings=settings)
            except:
                ngskin2.flood_weights(target=target_joints_layer, influence=vertex_2_joint[vert_it.index()].logicalIndex,
                                      settings=settings)

            next(vert_it)
        next(it_sel_list)

    print('Skinned {} with autoskin'.format(mesh))