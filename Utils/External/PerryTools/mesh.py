from __future__ import absolute_import
from maya import cmds
from collections import defaultdict
from maya.api.OpenMaya import MVector, MFloatPointArray, MFloatPoint, MIntArray, MColor, MColorArray, MFnMesh, MSelectionList, MGlobal, MItSelectionList, MFnSingleIndexedComponent

def cutCharacterFromSkin( inObject, internal=False, maya2020 = False):
    """ split the character into multiple meshes based on the skinning information
    
    :param inObject: object to seperate in multiple meshes
    :type inObject: string
    :param internal: if `True` will only convert the the inner selection, if `False` will grow the selection once to cover more ground
    :type internal: bool
    :param maya2020: if `True` will use the offsetparent matrix to connect the mesh to joints , if `False` will use a decompose matrix to connect the meshes
    :type maya2020: bool
    :return: group object that holds all the meshes
    :rtype: string
    """  
    skinClusterName = skinCluster(inObject, silent=True )
    
    if skinClusterName == None:
        return
    
    expandedList = convertToVertexList(inObject)
    
    objList = []    
    indexConns = defaultdict(lambda : [])
    
    for vId, vtx in enumerate(expandedList):
        val = cmds.skinPercent(skinClusterName, vtx, q=1, v = True)
        if not val:
            continue
        index = val.index(max(val))
        joint = cmds.skinPercent(skinClusterName, vtx, q=1, t = None)[index]
        indexConns[joint].append(vtx)

    for index, (shortJointName, val) in enumerate(indexConns.items()):
        obj = extractFacesByVertices(val, internal = internal)
        if obj is None:
            continue

        newObj = cmds.rename(obj[0], "%s_%s_Proxy"%(shortJointName, inObject.split("|")[-1]))

        grp = cmds.group(n= "%s_%s_ProxyGrp"%(shortJointName, inObject.split("|")[-1]), em=1)

        if not maya2020:
            decomp = cmds.createNode("decomposeMatrix", n = "%s_%s_ProxyDCP"%(shortJointName, inObject) )
            cmds.connectAttr( "%s.worldMatrix[0]"%shortJointName, "%s.inputMatrix"%decomp )
            cmds.connectAttr( "%s.outputTranslate"%decomp, "%s.translate"%grp )
            cmds.connectAttr( "%s.outputRotate"%decomp, "%s.rotate"%grp )
        else:
            cmds.connectAttr( "%s.worldMatrix[0]"%shortJointName, "%s.offsetParentMatrix"%grp )

        cmds.parent(newObj, grp)
        objList.append(grp)

    return cmds.group(objList, n="LowRez_%s"%inObject.split("|")[-1])

def skinCluster(inObject=None, silent=False):
    """ get the skincluster from the given mesh

    :param inObject: the object to search for a skincluster attachment
    :type inObject: string
    :param silent: if `True` will return None, if `False` will open a warning dialog to tell the user no skincluster was found
    :type silent: bool
    :return: name of the skincluster node
    :rtype: string
    """
    if inObject is None:
        inObject = cmds.ls(sl=1, l=1)
    if not inObject:
        return None

    if type(inObject) in [list, tuple] and len(inObject) != 0:
        inObject = inObject[0]
    if '.' in inObject:
        inObject = inObject.split('.')[0]

    inObject = getParentShape(inObject)
    sc = cmds.ls(cmds.listHistory(inObject), type="skinCluster")
    if not sc:
        if not silent:
            cmds.confirmDialog(title='Error', message='no SkinCluster found on: %s!' % inObject, button=['Ok'], defaultButton='Ok', cancelButton='Ok', dismissString='Ok')
        return None
    return sc[0]

def convertToVertexList(inObject):
    """ convert the given input to a represented point selection for the type of object that is selected:
    polygons : vertices
    Nurbs : control vertices
    lattice : points

    :param skinMesh: the object to search for a parent
    :type skinMesh: string
    :return: for polygons a list of vertices, for Nurbs a list of control vertices, for lattice a list of points
    :rtype: list
    """
    checkObject = inObject
    if isinstance(inObject, list):
        checkObject = inObject[0]
    objType = cmds.objectType(checkObject)
    checkType = checkObject
    if objType == "transform":
        shapes = cmds.listRelatives(inObject, ad=1, s=1)
        if not shapes == []:
            checkType = inObject
        checkType = shapes[0]

    objType = cmds.objectType(checkType)
    if objType == 'mesh':
        convertedVertices = cmds.polyListComponentConversion(inObject, tv=True)
        return cmds.filterExpand(convertedVertices, sm=31, fp=1)

    if objType == "nurbsCurve" or objType == "nurbsSurface":
        if isinstance(inObject, list) and ".cv" in inObject[0]:
            return cmds.filterExpand(inObject, sm=28, fp=1)
        elif isinstance(inObject, list):
            return cmds.filterExpand('%s.cv[*]' % inObject[0], sm=28, fp=1)
        elif ".cv" in inObject:
            return cmds.filterExpand(inObject, sm=28, fp=1)
        else:
            return cmds.filterExpand('%s.cv[*]' % inObject, sm=28, fp=1)

    if objType == "lattice":
        if isinstance(inObject, list) and ".pt" in inObject[0]:
            return cmds.filterExpand(inObject, sm=46, fp=1)
        elif isinstance(inObject, list):
            return cmds.filterExpand('%s.pt[*]' % inObject[0], sm=46, fp=1)
        elif ".pt" in inObject:
            return cmds.filterExpand(inObject, sm=46, fp=1)
        else:
            return cmds.filterExpand('%s.pt[*]' % inObject, sm=46, fp=1)
    return []

def getParentShape(inObject):
    """ get the parent object of given object if the current given object is a shape

    :param inObject: the object to search for a parent
    :type inObject: string
    :return: name of the parent transform
    :rtype: string
    """
    if isinstance(object, list):
        inObject = inObject[0]

    objType = cmds.objectType(inObject)
    if objType in ['mesh', "nurbsCurve", "lattice"]:
        inObject = cmds.listRelatives(inObject, p=True, f=True)[0]
    if cmds.objectType(inObject) != "transform":
        inObject = cmds.listRelatives(inObject, p=True, f=True)[0]
    return inObject


def extractFacesByVertices(vertices, internal=False):
    """ use the given components to create a new mesh with the same skinning information

    :param vertices: the components to use as information to generate the new mesh
    :type vertices: list
    :param internal: if `True` will only convert the the inner selection, if `False` will grow the selection once to cover more ground
    :type internal: bool
    :return: new created mesh
    :rtype: string
    """
    vertices = cmds.filterExpand(vertices, sm=31)
    if not vertices:
        return None

    curMesh = vertices[0].rsplit('.', 1)[0]
    dup = cmds.duplicate(curMesh)[0]
    if cmds.listRelatives(dup, p=1):
        cmds.parent(dup, w=True)

    dup = '|' + dup
    for i, vert in enumerate(vertices):
        vertices[i] = dup + '.' + vert.rsplit('.', 1)[-1]

    cmds.polyTriangulate(dup)

    faces = cmds.polyListComponentConversion(vertices, tf=True, internal=internal)
    faces = cmds.filterExpand(faces, sm=34)
    if not faces:
        cmds.delete(dup)
        return None

    if not internal:
        vertices = cmds.filterExpand(cmds.polyListComponentConversion(faces, tv=True), sm=31)

    vertexPositions = MFloatPointArray()
    vertexMap = {}
    normals = []
    for i, vertex in enumerate(vertices):
        vertexPositions.append(MFloatPoint(*cmds.xform(vertex, q=True, ws=True, t=True)))
        vertexMap[vertex.rsplit('[', 1)[-1].split(']', 1)[0]] = i
        normals.append(cmds.polyNormalPerVertex(vertex, q=1, xyz=1)[:3])

    ids = MIntArray()
    counts = MIntArray()
    for face in faces:
        faceVertices = cmds.filterExpand(cmds.polyListComponentConversion(face, tv=True), sm=31)
        counts.append(len(faceVertices))
        for vertex in faceVertices:
            ids.append(vertexMap[vertex.rsplit('[', 1)[-1].split(']', 1)[0]])

    m = MFnMesh()
    m.create(vertexPositions, counts, ids)

    path = m.fullPathName()
    if cmds.ls(path, type='mesh'):
        path = cmds.listRelatives(path, parent=True, f=True)
    cmds.transferAttributes(dup, path, transferPositions=0, transferNormals=1, transferUVs=2, sampleSpace=0,
                            sourceUvSpace="map1", targetUvSpace="map1", searchMethod=3, flipUVs=0)
    cmds.delete(path, ch=1)
    cmds.sets(path, edit=True, forceElement="initialShadingGroup")
    cmds.delete(dup)
    return path