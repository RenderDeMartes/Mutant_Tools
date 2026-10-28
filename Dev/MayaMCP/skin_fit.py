"""Clean shell-by-shell skinning with ngSkinTools2.

Runs INSIDE Maya (live session through the bridge, or mayapy with the
ngSkinTools2 plugin). For meshes made of separate pieces (beard clumps, hair
cards, feathers...) each poly shell gets only the joints you give it:

    1. bind the mesh to exactly the given joints (fresh skinCluster)
    2. per group: select the shell vertices and run ngSkinTools
       "Assign From Closest Joint" with "Use selected influences"
    3. relax with ngSkinTools smooth floods (shells never share vertices,
       so smoothing cannot bleed weights between groups)

    from Mutant_Tools.Dev.MayaMCP import skin_fit as sf
    chains = sf.chains_under('Head_Skl', '*_Beard_*_01_Skl')
    sf.skin_shells_by_chains('Beard_Geo', chains)
"""
import maya.cmds as mc
import maya.api.OpenMaya as om


# --------------------------------------------------------------------------
# Mesh / joint queries
# --------------------------------------------------------------------------
def mesh_shells(mesh):
    """Vertex index lists, one per poly shell (connected piece) of mesh."""
    sel = om.MSelectionList()
    sel.add(mesh)
    it = om.MItMeshVertex(sel.getDagPath(0))
    adj = {}
    while not it.isDone():
        adj[it.index()] = list(it.getConnectedVertices())
        it.next()
    seen, shells = set(), []
    for start in adj:
        if start in seen:
            continue
        seen.add(start)
        stack, members = [start], []
        while stack:
            v = stack.pop()
            members.append(v)
            for n in adj[v]:
                if n not in seen:
                    seen.add(n)
                    stack.append(n)
        shells.append(sorted(members))
    return shells


def chains_under(root_parent=None, pattern='*_01_Skl'):
    """Joint chains (root first) for every joint matching pattern.

    root_parent only keeps roots parented under that node, None keeps all.
    """
    chains = []
    for root in mc.ls(pattern, type='joint'):
        if root_parent and (mc.listRelatives(root, p=True) or [''])[0] != root_parent:
            continue
        chain = [root]
        while True:
            kids = mc.listRelatives(chain[-1], c=True, type='joint') or []
            if not kids:
                break
            chain.append(kids[0])
        chains.append(chain)
    return chains


def match_shells_to_chains(mesh, chains, shells=None):
    """Pair every shell with the chain that runs through it, one chain per shell.

    Clumps can interpenetrate, so nearest vertex / inside tests are ambiguous.
    Instead each joint takes the shell vertices within 1.5x its nearest
    distance: around a joint centred in an edge loop they surround it and
    their centroid lands on the joint, on a neighbour's surface they sit on
    one side. Pairs are ranked by that off-centre ratio and assigned greedily
    so no chain is used twice.
    Returns a list of (vertex_ids, chain). Raises if a shell finds no chain.
    """
    shells = shells or mesh_shells(mesh)
    sel = om.MSelectionList()
    sel.add(mesh)
    pts = [om.MVector(p) for p in om.MFnMesh(sel.getDagPath(0)).getPoints(om.MSpace.kWorld)]
    joint_pos = [[om.MVector(*mc.xform(j, q=True, ws=True, t=True)) for j in chain]
                 for chain in chains]
    costs = []
    for si, verts in enumerate(shells):
        shell_pts = [pts[v] for v in verts]
        for ci, jpts in enumerate(joint_pos):
            score = 0.0
            for p in jpts:
                dists = [(q - p).length() for q in shell_pts]
                near = min(dists)
                ring = [q for q, d in zip(shell_pts, dists) if d <= near * 1.5 + 1e-6]
                centre = sum(ring, om.MVector()) / len(ring)
                score += (centre - p).length() / max(near, 1e-6) + near * 1e-3
            costs.append((score / len(jpts), si, ci))
    costs.sort()
    shell_chain = {}
    used = set()
    for _, si, ci in costs:
        if si in shell_chain or ci in used:
            continue
        shell_chain[si] = ci
        used.add(ci)
    groups = []
    for si, verts in enumerate(shells):
        if si not in shell_chain:
            raise RuntimeError('No chain left for shell {} of {}'.format(si, mesh))
        groups.append((verts, chains[shell_chain[si]]))
    return groups


# --------------------------------------------------------------------------
# Skinning
# --------------------------------------------------------------------------
def _vertex_components(mesh, verts):
    return ['{}.vtx[{}]'.format(mesh, v) for v in verts]


def skin_shells(mesh, groups, smooth_iterations=3, smooth_intensity=0.5,
                max_influences=2, rebind=True, keep_layers=False, name=None):
    """Skin each vertex group only to its own joints with ngSkinTools.

    groups: list of (vertex_ids, joints).
    rebind: drop any skinCluster on mesh and bind to exactly these joints.
    keep_layers: leave the ngSkinTools layer data on the skinCluster.
    Returns the skinCluster name.
    """
    import ngSkinTools2.api as ng

    if not mc.pluginInfo('ngSkinTools2', q=True, loaded=True):
        mc.loadPlugin('ngSkinTools2')

    joints = []
    for _, chain in groups:
        joints += [j for j in chain if j not in joints]

    skin = ng.get_related_skin_cluster(mesh) if not rebind else None
    if not skin:
        for old in [h for h in (mc.listHistory(mesh, pdo=True) or []) if mc.nodeType(h) == 'skinCluster']:
            mc.skinCluster(old, e=True, ub=True)
        skin = mc.skinCluster(joints, mesh, tsb=True, mi=max_influences, nw=1,
                              n=name or mesh + '_skinCluster')[0]
        mc.setAttr(skin + '.maintainMaxInfluences', 1)

    index = {}
    for info in ng.list_influences(skin):
        index[info.path.split('|')[-1]] = info.logicalIndex

    data_before = set(mc.ls(type='ngst2SkinLayerData'))
    layers = ng.init_layers(skin)
    layers.influence_limit_per_vertex = max_influences
    layer = layers.add('ShellSkin')

    for verts, chain in groups:
        mc.select(_vertex_components(mesh, verts), r=True)
        ng.assign_from_closest_joint(skin, layer, influences=[index[j] for j in chain])

    if smooth_iterations:
        settings = ng.PaintModeSettings()
        settings.mode = ng.PaintMode.smooth
        settings.intensity = smooth_intensity
        settings.iterations = smooth_iterations
        settings.use_volume_neighbours = False
        mc.select(mesh, r=True)
        ng.flood_weights(layer, settings=settings)

    mc.select(cl=True)
    if not keep_layers:
        # the weights already live on the skinCluster, the layer data is only for ngSkinTools
        new_data = set(mc.ls(type='ngst2SkinLayerData')) - data_before
        if new_data:
            mc.delete(list(new_data))
    return skin


def skin_shells_by_chains(mesh, chains, **kwargs):
    """Match shells to the nearest joint chain, then skin_shells()."""
    return skin_shells(mesh, match_shells_to_chains(mesh, chains), **kwargs)
