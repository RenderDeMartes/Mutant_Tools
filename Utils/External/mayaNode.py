from __future__ import absolute_import
'''
Maya Node - Generic node wrapper


Maya's API documentation:

    - MFnDependencyNode:
    http://help.autodesk.com/cloudhelp/2017/ENU/Maya-SDK/cpp_ref/class_m_fn_dependency_node.html

    - MDagPath:
    http://help.autodesk.com/view/MAYAUL/2017/ENU/?guid=__cpp_ref_class_m_dag_path_html

    - MFnDagNode:
    http://help.autodesk.com/view/MAYAUL/2017/ENU/?guid=__cpp_ref_class_m_fn_dag_node_html

    - MObjectHandle:


'''
import six

import maya.OpenMaya as om
from maya import cmds

# Globals

TRAVERSE_MAP = {'depthfirst': om.MItDependencyGraph.kDepthFirst,
                'breadthfirst': om.MItDependencyGraph.kBreadthFirst}

DIRECTION_MAP = {'upstream': om.MItDependencyGraph.kUpstream,
                 'downstream': om.MItDependencyGraph.kDownstream}

DIRECT_OVERRIDE_TYPES = ["absUniqueOverride", "absRelativeOverride"]
INDIRECT_OVERRIDE_TYPES = ["absOverride"]

class MayaNode(object):


    def __init__(self, node):
        self.dagpath    = None
        self.handle     = None
        self.dagnode    = None
        self.dependnode = None

        if isinstance(node, MayaNode):
            self.dagpath    = node.dagpath
            self.handle     = node.handle
            self.dagnode    = node.dagnode
            self.dependnode = node.dependnode

        elif isinstance(node, om.MObject):
            self.handle = om.MObjectHandle(node)
            self.dependnode = om.MFnDependencyNode(node)

        elif isinstance(node, om.MObjectHandle):
            self.handle = node
            self.dependnode = om.MFnDependencyNode(node.object())

        elif isinstance(node, six.string_types):
            selList = om.MSelectionList()
            try:
                selList.add(node)
            except RuntimeError:
                raise RuntimeError('node name "{}" does not exist'.format(node))

            obj = om.MObject()

            selList.getDependNode(0, obj)
            self.handle = om.MObjectHandle(obj)
            self.dependnode = om.MFnDependencyNode(obj)

            # For DAG objects, get getDagPath. Will fail if doesn't have dagpath.
            try:
                self.dagpath = om.MDagPath()
                selList.getDagPath(0, self.dagpath)
                self.dagnode = om.MFnDagNode(self.dagpath)
            except:
                self.dagpath = None

        elif isinstance(node, om.MDagPath):
            self.dagpath = om.MDagPath(node)
            self.dagnode = om.MFnDagNode(self.dagpath)
            self.handle = om.MObjectHandle(self.dagnode.object())
            self.dependnode = om.MFnDependencyNode(self.dagnode.object())

        if not self.dagpath:
            dp = om.MDagPath()
            try:
                om.MDagPath().getAPathTo(self.obj, dp)
            except Exception:
                self.dagpath = None
            else:
                self.dagpath = dp
                self.dagnode = om.MFnDagNode(self.dagpath)

    def __repr__(self):
        return '{}("{}")'.format(self.__class__.__name__, self.name)

    def __unicode__(self):
        return six.ensure_text(self.name)

    def __str__(self):
        return six.ensure_str(self.name)

    def __hash__(self):
        '''Returns a hash code for the internal Maya object referenced by
        the MObject within this MObjectHandle.
        '''
        return self.handle.hashCode()

    def __eq__(self, other):
        '''
        Overloaded equality test which supports comparison between MayaNodes, PyMel and strings
        '''
        if isinstance(other, MayaNode):
            return self.obj == other.obj
        elif isinstance(other, six.string_types):
            other = MayaNode(six.text_type(other))
            return self == other

        return NotImplemented

    def __ne__(self, other):
        if isinstance(other, MayaNode):
            return self.obj != other.obj
        elif isinstance(other, six.string_types):
            other = MayaNode(six.text_type(other))
            return self != other

        return NotImplemented

    @property
    def obj(self):
        if self.handle.isValid():
            return self.handle.object()
        raise RuntimeError("Object handle is invalid")

    # --------------------------------------------------------------------------
    #   Name Helpers
    # --------------------------------------------------------------------------
    @property
    def name(self):
        '''
        The partial path is the minimum path that is still unique
        '''
        if self.dagpath:
            return self.dagpath.partialPathName()
        else:
            return self.dependnode.name()

    @property
    def fullname(self):
        '''Return a string representing the full path from the root of
        the dag to this object.
        '''
        if self.dagpath:
            return self.dagpath.fullPathName()
        else:
            return self.dependnode.name()


    @property
    def shortname(self):
        '''
        Returns a plain short name, including it's namespace.
        '''
        if self.dagpath:
            return self.dagpath.partialPathName().rsplit('|', 1)[-1]
        else:
            return self.dependnode.name()


    @property
    def basename(self):
        '''
        Returns a plain short name, excluding it's namespace.
        '''
        if self.dagpath:
            return self.dagpath.partialPathName().rsplit('|', 1)[-1].rsplit(':', 1)[-1]
        else:
            return self.dependnode.name().rsplit(':', 1)[-1]

    @property
    def namespace(self):
        '''
        Returns namespace string.
        '''
        if ':' in self.shortname:
            return self.shortname.rsplit(':', 1)[0]
        else:
            return ''


    # --------------------------------------------------------------------------
    #   Hierarchy  Helpers
    # --------------------------------------------------------------------------
    @property
    def parent(self):
        '''Returns node's parent or None otherwise.'''
        if not self.dagnode:
            return None

        if self.dagnode.parentCount() == 0:
            return None
        elif self.dagnode.parentCount() == 1:
            # Return parent, unless it's kWorld - not parent.
            parent = self.dagnode.parent(0)
            if parent.apiTypeStr() != 'kWorld':
                return MayaNode(parent)
        else:
            # Couldn't find an API way to get the parent, using listRelatives does the trick.
            #parent_index = self.dagpath.instanceNumber()
            parent_path = cmds.listRelatives(self.dagnode.fullPathName(), p=True, f=True)[0]
            return MayaNode(parent_path)

    @property
    def root(self):
        '''
        Returns root node (top most node in the DAG hierarchy).
        Will return self if self is the root.

        Determines the root of the first DAG Path to the DAG Node
        attached to the Function Set.
        '''
        if not self.dagpath:
            return None

        parent = self.parent

        if not parent:
            return self

        while parent:
            if parent.parent:
                parent = parent.parent
            else:
                return parent


    # --------------------------------------------------------------------------
    #   Hierarchy  Helpers
    # --------------------------------------------------------------------------
    def iter_descendants_connections(self, filter_types=None, direction_type='downstream',
                                     traverse_type='breadthfirst'):

        for dscnd in self.iter_descendants(filter_types=filter_types,
                                           traverse_type=traverse_type):

            for conn in self._recusive_connections(dscnd, filter_types, direction_type, traverse_type):
                yield conn



    def iter_descendants(self, filter_types=None, traverse_type='breadthfirst'):
        '''
        Iterate through all descendant.

        args:
            filter_types (list): filter only given types.
                                 e.g ['transform', om.MFn.kFileTexture, om.MFn.kGeometric].
            traverse_type (str): traverse type 'depthfirst' or 'breadthfirst':
                                 e.g http://help.autodesk.com/cloudhelp/2017/ENU/Maya-SDK/cpp_ref/class_m_it_dag.html

        usage:
            MayaNode('gilbert').iter_descendants(filter_types=['transform'])
            >>> [MayaNode('transform1'), MayaNode('transform2')]

        Return: a generator of MayaNodes
        '''

        # Validation
        if not self.dagpath:
            raise TypeError('"{self.name}" type:"{self.nodeType}" does not have dagpath'.format(self=self))

        assert (isinstance(filter_types, (list, type(None)))), 'filter_types must be list or None'

        if traverse_type:
            assert (traverse_type in TRAVERSE_MAP), 'valid values are {}'.format(list(TRAVERSE_MAP.keys()))
            assert ([t for t in traverse_type if isinstance(t, six.string_types)]), 'currently only string types are supported.'
        traverse = TRAVERSE_MAP[traverse_type]

        # Bilbo journey begins
        iterator = om.MItDag()
        dag_path = om.MDagPath()
        iterator.reset(self.obj, traverse)

        while not iterator.isDone():
            iterator.getPath(dag_path)

            node = om.MFnDagNode(dag_path)

            # We don't want to return self in the iterator.
            if self.obj == node.object():
                # pylint: disable=W1622
                iterator.next()
                continue

            # Filter out by type
            if filter_types:
                for ftype in filter_types:

                    # Compare to string type ('transform', 'mesh')
                    if isinstance(ftype, six.string_types) and node.typeName() == ftype:
                        yield MayaNode(dag_path)

                    # Compare to om.Mfn type (om.MFn.kGeometric)
                    elif isinstance(ftype, int) and node.object().hasFn(ftype):
                            yield MayaNode(dag_path)

            else:
                yield MayaNode(dag_path)

            # pylint: disable=W1622
            iterator.next()

    def iter_connections(self, filter_types=None, direction_type='downstream',
                         traverse_type='breadthfirst'):
        '''
        Iterate through all connections Downstream or Upstream.

        args:
            filter_types (list): filter only given types.
                                 e.g ['transform', om.MFn.kFileTexture].
            direction_type (str): search direction 'downstream' or 'upstream'.
            traverse_type (str): traverse type 'depthfirst' or 'breadthfirst':
                                 e.g http://help.autodesk.com/cloudhelp/2017/ENU/Maya-SDK/cpp_ref/class_m_it_dag.html

        usage:
            MayaNode('gilbert').iter_connections(filter_types=['cluster'])
            >>> [MayaNode('cluster1'), MayaNode('cluster2')]

        Return: a generator of MayaNodes
        '''

        # Validation
        if direction_type:
            assert (direction_type in DIRECTION_MAP), 'valid values are {}'.format(list(DIRECTION_MAP.keys()))
        direction = DIRECTION_MAP[direction_type]

        if traverse_type:
            assert (traverse_type in TRAVERSE_MAP), 'valid values are {}'.format(list(TRAVERSE_MAP.keys()))
        traverse = TRAVERSE_MAP[traverse_type]

        # Bilbo journey begins
        iterator = om.MItDependencyGraph(self.obj, om.MFn.kInvalid, direction, traverse)

        while not iterator.isDone():
            obj = iterator.currentItem()
            node = om.MFnDependencyNode(obj)
            # pylint: disable=W1622
            iterator.next()

            if obj == self.obj:
                pass
            elif filter_types:
                for filter_type in filter_types:
                    # Compare to string type ('transform', 'mesh')
                    if isinstance(filter_type, six.string_types) and node.typeName() == filter_type:
                        yield MayaNode(obj)

                    # Compare to om.Mfn type (om.MFn.kGeometric)
                    elif isinstance(filter_type, int) and node.object().hasFn(filter_type):
                        yield MayaNode(obj)
            else:
                yield MayaNode(obj)

    @classmethod
    def _recusive_connections(cls, root, filter_types, direction_type, traverse_type, _visited=None):
        yield root

        if _visited == None:
            _visited = set()

        if root in _visited:
            return

        _visited.add(root)

        for con in root.iter_connections(filter_types=filter_types,
                                         direction_type=direction_type,
                                         traverse_type=traverse_type):
            for con_ in cls._recusive_connections(con, filter_types, direction_type, traverse_type, _visited):
                yield con_

    # --------------------------------------------------------------------------
    #   Node Helpers
    # --------------------------------------------------------------------------
    def update_internal(self, mayanode):
        '''Update internal pointer to new mayanode'''
        self.dagpath    = mayanode.dagpath
        self.handle     = mayanode.handle
        self.dagnode    = mayanode.dagnode
        self.dependnode = mayanode.dependnode

    @property
    def isValid(self):
        '''Returns the validity of the associated MObject.
        True if the MObject is still pointing to a valid internal object.
        '''
        return self.handle.isValid()

    @property
    def nodeType(self):
        '''
        Returns node type.
        '''
        if self.dagnode:
            return self.dagnode.typeName()
        else:
            return cmds.nodeType(self)

    @property
    def is_instanced(self):
        return self.dagpath.isInstanced()

    # --------------------------------------------------------------------------
    #   Attributes Helpers
    # --------------------------------------------------------------------------
    def plug(self, attribute):
        '''
        Return MPlug for given attribute

        usage example:
            MayaNode('sphere').plug('tx').setFloat(5)
            MayaNode('sphere').plug('tx').asFloat(5)
            MayaNode('sphere').plug('tx').isKeyable()

        args:
            attribute (str): Attribute string.

        returns: MayaPlug attribute
        '''
        return MayaPlug(self, attribute)

    def hasAttr(self, attr):
        '''
        Returns True if attribute exists, False otherwise.
        '''
        # NOTE: We need to validate this node exists/valid, other wise Maya will crash,
        # once self.dependnode.hasAttribute is queried.
        if not self.isValid:
            raise RuntimeError('{!r} MayaNode instance != valid. must been deleted already.'.format(self.name))

        if '.' in attr:
            if not self.dependnode.hasAttribute(attr.split('.')[0]):
                return False
            else:
                return self.dependnode.hasAttribute(attr.split('.')[-1])

        return self.dependnode.hasAttribute(attr)

    def setAttr(self, attr, *values):
        '''
        Set attribute value(s)
        '''
        if not self.hasAttr(attr):
            raise ValueError('Attribute does not exists: "{}.{}"'.format(self, attr))
        elif not cmds.getAttr("{}.{}".format(self, attr), settable=True):
            raise RuntimeError('Attribute != settable: "{}.{}"'.format(self, attr))

        # Collapse values to one argument we can pass on.
        args = []

        for arg in values:
            if hasattr(arg, '__iter__'):
                args.extend(arg)
            else:
                args.append(arg)

        attr_type = cmds.getAttr('{}.{}'.format(self, attr), type=True)
        cmd_flags = dict()

        # Build argument based on attribute type. every one is unique mama said.
        if attr_type in ('string'):
            cmd_flags['type'] = attr_type

        elif attr_type == 'stringArray':
            cmd_flags['type'] = attr_type
            args.insert(0, len(args))  # inject counter

        elif attr_type in ('TdataCompound', 'float3', 'float2',
                           'double3', 'double4', 'matrix'):
            cmd_flags['type'] = attr_type
            if isinstance(args, (list, tuple)) and \
               isinstance(args[0], (list, tuple)):
                args = list(args[0])

        args.insert(0, "{}.{}".format(self, attr))

        try:
            cmds.setAttr(*args, **cmd_flags)
        except Exception:
            raise

    def getAttr(self, attr):
        '''
        Get attribute value(s)
        '''
        if not self.hasAttr(attr):
            raise ValueError('Attribute does not exists: "{}.{}"'.format(self, attr))

        return cmds.getAttr("{}.{}".format(self, attr))

    def listConnections(self, attr, **kwargs):
        '''
        Just a cmds.listConnections wrapper
        '''
        if not self.hasAttr(attr):
            raise ValueError('Attribute does not exists: "{}.{}"'.format(self, attr))

        return cmds.listConnections('{}.{}'.format(self, attr), **kwargs)

    def hasFn(self, mfnType):
        return self.obj.hasFn(mfnType)


# --------------------------------------------------------------------------------------------------
#   Maya Plug (Attribute) API
# --------------------------------------------------------------------------------------------------
class MayaPlug(om.MPlug):
    '''
    Class representing an attribute (MPlug) on a node.

    Extending the class om.MPlug, for all the inherited functions look at:
    https://help.autodesk.com/view/MAYAUL/2018/ENU/?guid=__cpp_ref_class_m_plug_html

    usage example:
        MayaNode('sphere').plug('tx').setFloat(5)
        MayaNode('sphere').plug('tx').asFloat(5)
        MayaNode('sphere').plug('tx').isKeyable()
    '''

    def __init__(self, obj, attribute=None):
        '''
        args:
            node (MObject, MayaNode, str): The parent node of the attribute
            attribute               (str): the name of the attribute
        '''
        plug = None

        if isinstance(obj, om.MPlug):
            plug = obj
        elif isinstance(obj, om.MObject):
            plug = _get_plug(obj, attribute)
        elif isinstance(obj, MayaNode):
            plug = _get_plug(obj, attribute)
        elif isinstance(obj, six.string_types):
            sel = om.MSelectionList()
            sel.add(obj)
            mplug = om.MPlug()
            mobj = om.MObject()

            try:
                sel.getPlug(0, mplug)
                plug = mplug
            except RuntimeError:
                sel.getDependNode(0, mobj)
                plug = _get_plug(mobj, attribute)
        else:
            raise TypeError("{} != a supported object.".format(obj))

        super(MayaPlug, self).__init__(plug)

    def __hash__(self):
        node_hash = om.MObjectHandle(super(MayaPlug, self).node()).hashCode()
        attr_hash = om.MObjectHandle(self.attribute()).hashCode()
        return hash((self.__class__, node_hash, attr_hash))

    def __repr__(self):
        return '{}("{}")'.format(self.__class__.__name__, self.name())

    def __unicode__(self):
        return six.ensure_text(self.name())

    def __str__(self):
        return six.ensure_str(self.name())

    def node(self):
        return MayaNode(super(MayaPlug, self).node())

    def source(self):
        sourcePlug = super(MayaPlug, self).source()

        if sourcePlug.isNull():
            return None

        return MayaPlug(sourcePlug)

    def getOverridePlug(self):
        """ If this plug is overriden, return the current layer's override plug"""
        try:
            import maya.app.renderSetup.model.renderSetup as renderSetup
        except ImportError as e:
            cmds.warning("Legacy Render Layers are not supported by getOverridePlug. {}".format(e))
            return None

        render_setup_instance = renderSetup.instance()
        if render_setup_instance.getDefaultRenderLayer() == render_setup_instance.getVisibleRenderLayer():
            return None

        for node in cmds.listHistory(self.name()) or []:
            node = MayaNode(node)
            node_type = cmds.objectType(node)
            if node_type in DIRECT_OVERRIDE_TYPES:
                if self.node().name == node.getAttr("targetNodeName") and self.partialName() == node.getAttr("attribute"):
                    return node.plug("atv")
            elif node_type in INDIRECT_OVERRIDE_TYPES:
                for history_node in cmds.listHistory(node.name) or []:
                    if cmds.objectType(history_node) == "collection":
                        values = _get_values_from_collection_node(history_node)
                        if self.node() in values:
                            return node.plug("atv")
        return None

    def isOverriden(self):
        """Is this plug overriden in current layer?"""
        return bool(self.getOverridePlug())

    def connect(self, other, force=False):
        """
        Connect this plug to another plug as the source plug.

        Args:
            other (OpenMaya.MPlug): The destination plug.
            force (bool, optional): If the other plug is already connected,
                disconnect it. Defaults to not try to disconnect the plug.

        Raises:
            TypeError: Raised if the other plug != an OpenMaya.MPlug.
        """
        if not isinstance(other, om.MPlug):
            raise TypeError("{} != a valid Maya Plug. Expected an object that is derived from OpenMaya.MPlug.".format(other))

        modifier = om.MDGModifier()

        if force and other.isDestination():
            modifier.disconnect(other.source(), other)
            modifier.doIt()

        modifier.connect(self, other)
        modifier.doIt()

    def disconnect(self, other):
        """
        Disconnect this plug from the other plug.

        Args:
            other (OpenMaya.MPlug): The destination plug to disconnect.

        Raises:
            TypeError: Raised if the other plug != an OpenMaya.MPlug.
        """
        if not isinstance(other, om.MPlug):
            raise TypeError("{} != a valid Maya Plug. Expected an object that is derived from OpenMaya.MPlug.".format(other))

        modifier = om.MDGModifier()
        modifier.disconnect(self, other)
        modifier.doIt()

def _get_values_from_collection_node(node):
    selector = MayaNode(node).plug("selector")
    for selector_obj in cmds.listConnections(selector.name()):
        if cmds.objectType(selector_obj) == "simpleSelector":
            selector_obj = MayaNode(selector_obj)
            static_selection = selector_obj.plug("staticSelection")
            if static_selection:
                for selection in static_selection.asString().split("\n"):
                    if selection:
                        yield selection

def _get_plug(node, attribute):
    if not attribute:
        raise ValueError("Attribute must be provided if the input object is a node.")

    node = MayaNode(node)

    if isinstance(attribute, six.string_types):
        return node.dependnode.findPlug(attribute, True)
    elif isinstance(attribute, om.MObject) and attribute.hasFn(om.MFn.kAttribute):
        return node.dependnode.findPlug(attribute, True)
    else:
        raise TypeError("Attribute {} != supported.".format(attribute))
