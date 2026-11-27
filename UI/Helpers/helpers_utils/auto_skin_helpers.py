from __future__ import absolute_import
import maya.cmds as cmds
from maya.api import OpenMaya as om2
import math
import re
try:
    import ngSkinTools2.api as ngskin2
    _NGSKIN2_AVAILABLE = True
except ImportError:
    ngskin2 = None
    _NGSKIN2_AVAILABLE = False
    cmds.warning('ngSkinTools2 not found. Auto-skin helpers requiring it will be unavailable.')


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


def get_closest_joint_per_vertex(mesh, vertices=[], joints=None):
    """Closest influence per vertex. joints: only these influence names (short
    names) are candidates. Each joint is used once while there are enough
    joints for every vertex (per vertex binds), reused when there are fewer."""
    if not _NGSKIN2_AVAILABLE:
        cmds.warning('ngSkinTools2 is required for get_closest_joint_per_vertex but is not installed.')
        return {}
    influences = ngskin2.list_influences(mesh)
    if joints is not None:
        joints = set(joints)
        influences = [inf for inf in influences if inf.path_name().split('|')[-1] in joints]
    if not influences:
        raise RuntimeError('No lip joints in the skinCluster of {}'.format(mesh))
    one_each = len(influences) >= len(vertices)
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
        if one_each:
            influences.pop(current_min_index)
    return vertex_joint


def find_lip_configs():
    """Config nodes of the lip blocks in the scene (Lips v001-v003, MouthGames,
    any block with lip edges whose module is a mouth module)."""
    configs = []
    for node in cmds.ls('*.SetUpperEdge', o=True) or []:
        if not cmds.attributeQuery('SetLowerEdge', node=node, exists=True):
            continue
        command = ''
        if cmds.attributeQuery('Import_Command', node=node, exists=True):
            command = str(cmds.getAttr(node + '.Import_Command') or '').lower()
        if 'mouth' in command or 'lip' in node.lower():
            configs.append(node)
    return configs


def auto_skin_lips(joint_range=10):
    """Auto skin the lips of every lip block in the scene.

    Local Lips (GameMode off, BodyLips layer in the scene): skins BodyLips,
    everything else goes to Null_Local_Bnd first (same as before).
    Game blocks (MouthGames, Lips GameMode): skins the mesh the lip edges were
    picked on and keeps its current weights (head, jaw...) outside the lips.
    Only the block's own lip bind joints are used; missing ones are added to
    the skinCluster.
    Never silent: a green viewport message lists what got skinned, and
    cmds.error (red) says why when nothing could be skinned.
    """
    if not _NGSKIN2_AVAILABLE:
        cmds.error('Auto Skin Lips: ngSkinTools2 is not installed / loaded.')
    configs = find_lip_configs()
    if not configs:
        cmds.error('Auto Skin Lips: no Lips / MouthGames block in the scene.')
    done, failed = [], []
    for config in configs:
        try:
            done.append(_auto_skin_lip_block(config, joint_range))
        except Exception as e:
            failed.append('{}: {}'.format(config, e))

    for message in failed:
        cmds.warning('Auto Skin Lips: ' + message)
    if not done:
        cmds.error('Auto Skin Lips failed. ' + ' | '.join(failed))
    text = 'Auto Skin Lips: ' + ', '.join(done)
    if failed:
        text += ' (failed: {}, see Script Editor)'.format(len(failed))
    print(text)
    try:
        cmds.inViewMessage(amg='<hl>{}</hl>'.format(text), pos='midCenter', fade=True, fadeStayTime=2500)
    except RuntimeError:
        pass  # batch / no viewport
    return done


def _auto_skin_lip_block(config, joint_range):
    """Skin one lip block; returns a short summary, raises with the reason."""
    name = config[:-len('_Config')] if config.endswith('_Config') else config
    upper = str(cmds.getAttr(config + '.SetUpperEdge') or '')
    lower = str(cmds.getAttr(config + '.SetLowerEdge') or '')
    if '.' not in upper or '.' not in lower:
        raise RuntimeError('no lip edges set (SetUpperEdge / SetLowerEdge)')
    src_mesh = upper[:upper.index('.')]
    command = str(cmds.getAttr(config + '.Import_Command') or '').lower()         if cmds.attributeQuery('Import_Command', node=config, exists=True) else ''
    game = 'mouthgames' in command or (cmds.attributeQuery('GameMode', node=config, exists=True)
                                       and bool(cmds.getAttr(config + '.GameMode')))
    local = not game and cmds.objExists('BodyLips')
    mesh = 'BodyLips' if local else src_mesh
    if not cmds.objExists(mesh):
        raise RuntimeError('mesh {} not found'.format(mesh))

    edges = []
    for text in (upper, lower):
        edges += text.replace(src_mesh, mesh).replace(' ', '').split(',')
    edges = cmds.filterExpand(edges, sm=32)
    if not edges:
        raise RuntimeError('the lip edges {} do not exist on {}'.format(upper, mesh))

    # the block's lip bind joints: <side>_<name>_Up_Lip_NN_Bnd, legacy <name>_Up_N_Bnd
    pattern = re.compile(r'(^|_){}_(Up|Dw)_.*Bnd$'.format(re.escape(name)))
    lip_joints = [j for j in cmds.ls(type='joint') if pattern.search(j)]
    if not lip_joints:
        raise RuntimeError('no {} lip bind joints, build the rig first'.format(name))
    skin = ngskin2.get_related_skin_cluster(mesh)
    if not skin:
        raise RuntimeError('{} has no skinCluster, skin it first'.format(mesh))
    current = set(cmds.skinCluster(skin, q=True, inf=True) or [])
    missing = [j for j in lip_joints if j not in current]
    if missing:
        cmds.skinCluster(skin, e=True, ai=missing, wt=0, lw=True)
        for j in missing:
            cmds.setAttr(j + '.liw', 0)
        print('Auto Skin Lips: added {} lip joints to {}'.format(len(missing), skin))

    skin_edge_loop_joints(mesh, edges, joint_range, joints=lip_joints,
                          base_joint='Null_Local_Bnd' if local else None)
    return '{} skinned ({} lip joints, {})'.format(mesh, len(lip_joints), 'local' if local else 'game')


def skin_edge_loop_joints(mesh='', edge_loop='', joint_range=10, joints=None, base_joint='Null_Local_Bnd'):
    """joints: candidate lip joints (None = every influence). base_joint: the
    whole mesh goes to it first (local face layers); None keeps the current
    weights under the lips (game meshes skinned to head / jaw)."""
    if not _NGSKIN2_AVAILABLE:
        cmds.warning('ngSkinTools2 is required for skin_edge_loop_joints but is not installed.')
        return
    # get loop as array of ints and turn it into a set
    lips_loop_indices = [get_component_index(e) for e in edge_loop]
    lips_loop_indices = set(lips_loop_indices)

    # convert edge loop to vertices
    lips_vertices = cmds.polyListComponentConversion(edge_loop, fromEdge=True, toVertex=True)
    lips_vertices = cmds.filterExpand(lips_vertices, selectionMask=31)
    lips_vertices_index = [get_component_index(v) for v in lips_vertices]

    # get a dict associating each vertex with its closest joint
    vertex_2_joint = get_closest_joint_per_vertex(mesh, vertices=lips_vertices_index, joints=joints)

    # prepare for weight painting (the first layer starts from the current weights)
    skin_cls = ngskin2.get_related_skin_cluster(mesh)
    layers = ngskin2.init_layers(skin_cls)
    base_layer = layers.add('base weights')
    if base_joint:
        null_joint_index = next((inf.logicalIndex for inf in ngskin2.list_influences(skin_cls) if
                                 inf.path_name().split('|')[-1] == base_joint), None)
        if null_joint_index is None:
            cmds.warning('Auto skin lips: {} is not in the skinCluster, current weights kept.'.format(base_joint))
        else:
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