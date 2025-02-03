from __future__ import absolute_import
from __future__ import absolute_import, division, print_function

import math

from six.moves import range

import maya.api.OpenMaya as om2
import maya.OpenMaya as om
from maya import cmds

from .mayaNode import MayaNode


class GeoNode(MayaNode):
    '''
    Generic Geo node.

    MFnMesh:
    https://help.autodesk.com/view/MAYAUL/2018/ENU/?guid=__cpp_ref_class_m_fn_mesh_html
    '''

    def __init__(self, node):
        super(GeoNode, self).__init__(node=node)

        # create api 2.0 attribs
        sel = om2.MSelectionList()
        sel.add(self.dagpath.fullPathName())
        self.dagpath2 = sel.getDagPath(0)
        self.depend2 = om2.MFnDependencyNode(sel.getDependNode(0))

        # We need to confirm given node or its child is MFnMesh, otherwise the
        # code will error down the class.
        self.transform_dag_path2 = self.__get_transform_dag_path2(self.dagpath2)
        self.mesh_dag_path2 = self.__get_mesh_dag_path2(self.dagpath2)

        if not self.mesh_dag_path2:
            raise TypeError("Given object {!r} is a {!r}. Expected a 'kMesh' or a transform with a child 'kMesh'".format(self.fullname, self.nodeType))

        self.transform2 = om2.MFnTransform(self.transform_dag_path2)
        self.mfn2 = om2.MFnMesh(self.mesh_dag_path2)

    # ------ bbox methods ------
    def get_bBox(self):
        return cmds.xform(self, q=True,
                          boundingBoxInvisible=True,
                          worldSpace=True)
        # xmin, ymin, zmin, xmax, ymax, zmax

    def get_corners(self):
        bBox = self.get_bBox()
        # get the corenrs of the object
        xmin = bBox[0]
        ymin = bBox[1]
        zmin = bBox[2]
        xmax = bBox[3]
        ymax = bBox[4]
        zmax = bBox[5]

        # Re-map to 8 corners
        corners = []

        corners.append([xmin, ymin, zmin])
        corners.append([xmax, ymin, zmin])

        corners.append([xmin, ymax, zmin])
        corners.append([xmin, ymin, zmax])

        corners.append([xmax, ymax, zmin])
        corners.append([xmax, ymin, zmax])

        corners.append([xmax, ymax, zmax])
        corners.append([xmin, ymax, zmax])

        return corners

    # ------ vertex position methods ------
    def vtxToOrigin(self):
        '''
        Set all vertices of a mesh to absolute zero (origin).
        '''
        zeroArray = om2.MFloatPointArray()
        # MUST USE cmds.polyEvaluate here instead of self.mfn2.numVertices or Maya will crash in many cases :(
        zeroArray.copy([(0, 0, 0) for x in range(cmds.polyEvaluate(self.fullname, vertex=True))])
        self.mfn2.setPoints(zeroArray)

    def bakeLocalVtx(self):
        '''
        Bake vertex translations using a deformer and deleting history.
        Does not work on tiny values (like 2.2e-07).
        In that case, use vtxToOrigin method first (to ensure large enough values), then bake,
        then reset the points positions, and bake again.
        '''
        isIntermediate = False

        # intermediate object has to be disabled to add a deformer
        if cmds.getAttr("{}.intermediateObject".format(self.fullname)) is True:
            isIntermediate = True
            cmds.setAttr("{}.intermediateObject".format(self.fullname), False)

        inmesh_plug = self.plug("inMesh")
        source_plug = None

        # If there's a source plug to the inMesh, then disconnect, clean up the
        # verts, and reconnect. This may completely undo the fix done with the
        # cluster trick, though.
        if inmesh_plug.isDestination():
            source_plug = inmesh_plug.source()
            source_plug.disconnect(inmesh_plug)

        cmds.cluster(self.fullname)
        cmds.delete(self.fullname, ch=True)

        if source_plug:
            source_plug.connect(inmesh_plug)

        if isIntermediate:
            cmds.setAttr("{}.intermediateObject".format(self.fullname), True)

        self.mfn2.syncObject()

    def zeroLocalVtx(self):
        '''Zero out a meshes local vertex translations.
        Much faster than API iterating over .pnts attribute and setting x, y, z plugs zero.
        '''
        pts = self.mfn2.getPoints(om2.MSpace.kPreTransform)
        vtxVals = self.localVtx

        # subtract local vertex translation vectors from object space point positions
        zeroedVals = (pts[x] - vtxVals[x] for x in range(self.mfn2.numVertices))

        self.mfn2.setPoints(zeroedVals, om2.MSpace.kPreTransform)

    def setVertexPositions(self, zeroPos, realPos):
        '''
        Set worldspace vertices with specific worldspace coordinates, and local vertex values.
        Local vertex values are to be precalculated ( the difference between the give zeroPos and realPos )
        Args:
            zeroPos (MPointArray): The worldspace vertex positions when the meshes local vtx translates are zeroed.
            realPos (MPointArray): The real worldspace vertex positions, including local vtx translates.
        '''
        # first set all vertices to origin, and bake local vtx translates
        # this step is to prevent tiny e-07 vtx translate values. baking does not work when
        # the mesh has these tiny values so this just makes sure theres a big enough difference that
        # they DO get frozen.
        mesh.vtxToOrigin()
        mesh.bakeLocalVtx()

        # set vertices to zeroed position, bake again and then set real positions to
        # restore vertex positions and local vertex values from pre-replace.
        mesh.mfn2.setPoints(zeroPos, om2.MSpace.kWorld)
        mesh.bakeLocalVtx()
        mesh.mfn2.setPoints(realPos, om2.MSpace.kWorld)

    @property
    def localVtx(self):
        '''
        Get mesh local vertex translation values.
        Returns:
        MVectorArray of the meshes local vertex translations.
        '''
        localVals = cmds.getAttr(self.fullname + '.pnts[*]')
        result = om2.MVectorArray()
        result.setLength(self.mfn2.numVertices)
        result.copy(localVals)
        return result

    @property
    def worldVtxPosition(self):
        '''Get the world position of the vtx'''
        wSpace = om.MSpace.kWorld
        return self._vertexPosition(wSpace)

    @property
    def objectVtxPosition(self):
        '''Get the object position of the vtx'''
        oSpace = om.MSpace.kObject
        return self._vertexPosition(oSpace)

    @property
    def vtxOrder(self):
        '''Get the order of the vtx's'''
        # Check mesh has vertex before, other wise mfn2.getVertices() will raise
        # a runtime error msg that won't help much.
        if not self.vtxCount:
            raise RuntimeError('Mesh {!r} is an empty mesh which has no vertex'.format(self))

        meshVtxCount, meshVtxArray = self.mfn2.getVertices()
        return [meshVtxArray[i] for i in range(len(meshVtxArray))]

    @property
    def vtxCount(self):
        '''Get the count of the vtx's'''
        return cmds.polyEvaluate(self.name, vertex=True)


    @property
    def nanVertices(self):
        '''
        Get NaN and inf vertex ids
        '''
        nanVerts = []

        pts = self.mfn2.getPoints()

        for i in range(len(pts)):
            for e in pts[i]:
                if math.isnan(e) or math.isinf(e):
                    nanVerts.append('{}.vtx[{}]'.format(self, i))

                    return nanVerts

    # ------ face methods ------
    @property
    def faceCount(self):
        '''Get the count of the face's'''
        return cmds.polyEvaluate(self.name, face=True)

    # ------ pivot methods ------
    @property
    def worldPivot(self):
        '''Get world pivot
        '''
        transform = cmds.listRelatives(self.name, p=True, fullPath=True)
        transform = transform[0] if transform else None
        if not transform:
            raise ValueError('Could not find {}\'s transform, weird'.format(self.name))
        pivots = cmds.xform(transform, q=True, ws=True, pivots=True)
        return pivots

    # ------ uv methods ------
    def clearUVs(self):
        '''
        Clear all UVs, delete non-default UV sets, and rename default UV set to "map1".
        '''

        uvSetAttrs = self.uvSetAttrs
        meshPath = self.mfn2.fullPathName()

        for s in self.mfn2.getUVSetNames():
            setIndex = uvSetAttrs[s]['index']
            if setIndex == 0:
                self.mfn2.clearUVs(s)
                if s != 'map1':
                    self.mfn2.renameUVSet(s, 'map1')
            else:
                self.mfn2.deleteUVSet(s)
                # remove now-empty uvSet array attribute for this set's index as well
                cmds.removeMultiInstance('{0}.uvSet[{1}]'.format(meshPath, setIndex))

    @property
    def uvSetAttrs(self):
        '''
        Get connected plug, and index into .uvSet array attribute for each UV set on the given mesh.
        Returns:
        Dictionary of {uv set name:{'index':<index into array>, 'connections':[connections list]}, ...}
        '''
        setIndices = {}  # init empty dict to hold uvSetName:arrayIndex
        nodePath = self.mfn2.fullPathName()
        uvSetIndices = cmds.getAttr('{}.uvSet'.format(nodePath), multiIndices=True)
        uvSetIndices = [int(lng) for lng in uvSetIndices]  # longs to ints
        for x in uvSetIndices:
            setNameAttr = '{0}.uvSet[{1}].uvSetName'.format(nodePath, x)
            uvSetName = cmds.getAttr(setNameAttr)
            if uvSetName != None:
                setIndices[uvSetName] = {'index': x}
                uvSetConnection = cmds.listConnections(setNameAttr, p=True)
                setIndices[uvSetName]['connections'] = uvSetConnection

        return setIndices

    @property
    def uvSetNames(self):
        '''Just get the UV sets names, if not uv sets found, returns empty list

        returns:
            uv_sets (list): a list of the uv set names

        '''
        uv_sets = set()
        if self.mfn2.getUVSetNames():
            for uv_set in self.mfn2.getUVSetNames():
                uv_sets.add(uv_set)
            return list(uv_sets)
        else:
            return []

    # ------ other methods ------
    @property
    def hasHistory(self):
        '''
        Check for construction history. Using interest level 1 to skip auxilary nodes.
        '''
        return cmds.listHistory(self.fullname, pdo=True, interestLevel=1) != None

    @property
    def isIntermediate(self):
        '''Is the mesh an intermediate shape.'''
        return cmds.getAttr('{}.intermediateObject'.format(self.fullname))

    def setIntermediate(self, state):
            '''Set intermediate object state.'''
            cmds.setAttr('{}.intermediateObject'.format(self.fullname), state)

    def forceSyncMesh(self):
        '''
        Force a mesh to refresh/update/sync to prevent Maya crashing. In some unpredictable cases
        after an MFnMesh.copyInplace() call, NONE of MFnMesh.updateSurface(), MFnMesh.syncObject(),
        cmds.refresh(), ogs(reset=True) or forcing DG evaluation on the node cause it to
        actually update properly. If MFnMesh.setPoints() is then called on the copyInPlaced mesh,
        using point values from the source mesh in the copy, maya crashes because it has the wrong
        number of points. We have to refresh using this method first.

        By setting the displaySmoothness to the same value it already is for that mesh, it is
        somehow always forced to refresh. Probably because maya sux.
        '''
        sel = cmds.ls(sl=True)
        cmds.select(self, r=True)  # displaySmoothness command is garbage and work only on selection
        intermediateState = self.isIntermediate
        self.setIntermediate(False)  # have to disable intermediate for this to work
        cmds.displaySmoothness(po=int(cmds.displaySmoothness(q=True, po=True)[0]))
        self.setIntermediate(intermediateState)
        cmds.select(sel)  # restore original selection

    # ------ shading methods ------
    @property
    def shadingEngines(self):
        '''
        Get the shading engines for the mesh
        Returns:
            List of maya shadingEngine names
        '''
        con = cmds.listConnections(self.fullname, t='shadingEngine') or []
        return list(set(con))

    def setShader(self, shadingEngines):
        '''
        Assign a shadingEngine, unless more than one shadingEngine is in list.
        Args:
            shadingEngines (list): List of shading engines.
        '''
        if len(shadingEngines) == 1:
            cmds.sets(self.fullname, fe=shadingEngines[0])

    def removeShader(self):
        '''
        Make mesh green by disconnecting it's shader. Redshift will render it as bright red.
        '''
        shapePlugs = cmds.listConnections('{}'.format(self.fullname), c=True, t='shadingEngine') or []
        sgPlugs = cmds.listConnections('{}'.format(self.fullname), p=True, t='shadingEngine')
        shapePlugs = [shapePlugs[x] for x in range(0, len(shapePlugs), 2)]  # only want plugs on mesh

        for i in range(len(shapePlugs)):
            try:
                cmds.disconnectAttr(shapePlugs[i], sgPlugs[i])
            except RuntimeError:
                cmds.disconnectAttr(sgPlugs[i], shapePlugs[i])

    def __get_transform_dag_path2(self, dag_path2):
        if dag_path2.node().hasFn(om2.MFn.kTransform):
            return dag_path2

        # Copy the dag path so we don't affect the previous one.
        # Assume that the parent is a transform. Most likely true.
        parent_dag_path = om2.MDagPath(dag_path2)
        parent_dag_path.pop()

        return parent_dag_path

    def __get_mesh_dag_path2(self, dag_path2):
        if dag_path2.node().hasFn(om2.MFn.kMesh):
            return dag_path2

        child_dag_path = None

        for index in range(dag_path2.childCount()):
            obj = dag_path2.child(index)

            if not obj.hasFn(om2.MFn.kMesh):
                continue
            elif om2.MFnDagNode(obj).findPlug("intermediateObject", True).asBool():
                continue

            if child_dag_path:
                raise ValueError("Multiple non-intermediate meshes found for '{}'".format(dag_path2.partialPathName()))

            child_dag_path = om2.MDagPath(dag_path2)
            child_dag_path.push(obj)

        return child_dag_path

    def _vertexPosition(self, space):
        '''Return vertex position by given space'''
        # Check mesh has vertex before, other wise mfn2.getVertices() will raise
        # a runtime error msg that won't help much.
        if not self.vtxCount:
            raise RuntimeError('Mesh {!r} is an empty mesh which has no vertex'.format(self))
        result = dict()
        mPointArray = self.mfn2.getPoints(space)

        for x in range(0, len(mPointArray)):
            result[x] = ([mPointArray[x][0], mPointArray[x][1], mPointArray[x][2]])

        return result
