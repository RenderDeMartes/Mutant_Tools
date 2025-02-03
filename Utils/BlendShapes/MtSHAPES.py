from __future__ import absolute_import
try:
    import importlib;from importlib import reload
except:
    import imp;from imp import reload


import maya.cmds as cmds
import maya.mel as mel

'''
Usage:

from Mutant_Tools.Utils.BlendShapes.MtSHAPES import MtSHAPES


sphereShapes = MtSHAPES('pSphere1')
sphereShapes.split_target('star', 0.1)
sphereShapes.add_target_posed('targetMesh')

'''

class MtSHAPES(object):
    '''
        Initialize the object with the name of the target mesh as argument.
        It's blendshape node will automatically be loaded as a member variable.

    '''
    def __init__(self, mesh):
        if not cmds.pluginInfo("SHAPESTools.mll", q=1, loaded=True):
            try:
                cmds.loadPlugin("SHAPESTools.mll")
            except Exception as e:
                cmds.error("Failed to load shapes plugin, maybe try buying it next time ")
                print(e)

        if not cmds.pluginInfo("invertShape.so", q=1, loaded=True):
            try:
                cmds.loadPlugin("invertShape.so")
            except Exception as e:
                print(e)
        
        self.mesh = mesh
        self.blend_shape = self._get_mesh_blend_shape_nodes(mesh)
            
    def _get_mesh_blend_shape_nodes(self, mesh):
        '''
        returns single node if only one is present, returns a list if multiple bs nodes are found
        '''
        blend_shape = cmds.ls(cmds.listHistory(mesh), type='blendShape')
        
        return blend_shape[0] if len(blend_shape) == 1 else blend_shape
            
    def get_target_shapes(self):
        attr = '{}.w'.format(self.blend_shape)
        weight_list = cmds.listAttr(attr, m=1)
        return weight_list
            
    def get_target_name_by_index(self, index):
        return self.get_target_shapes()[index]
        
    def get_index_by_target_name(self, name):
        return self.get_target_shapes().index(name)
        
    def get_valid_target_index(self):
        return len(self.get_target_shapes())
            
    def split_target(self, og_target_name, blend=0.1):
        #og_target_name = self.get_target_name_by_index(blend_shape, target_index) 
        target_index = self.get_index_by_target_name(og_target_name)
        left_duplicate_index = mel.eval('blendShapeDuplicateTarget("{}", {})'.format(self.blend_shape, target_index))
        mel.eval('blendShapeRenameTargetAlias {} {} {}'.format(self.blend_shape, left_duplicate_index, "L_" + og_target_name))
        right_duplicate_index = mel.eval('blendShapeDuplicateTarget("{}", {})'.format(self.blend_shape, target_index))
        mel.eval('blendShapeRenameTargetAlias {} {} {}'.format(self.blend_shape, right_duplicate_index, "R_" + og_target_name))
        
        og_shape = cmds.listRelatives(self.mesh, shapes=1, fullPath=1)[1]
        
        cmds.br_blendShapeSplitTarget(self.blend_shape, 
            axis='x', 
            invert=1, 
            blend=blend, 
            center=0, 
            index=left_duplicate_index, 
            originalMesh=og_shape, 
            tolerance=0.001)
        cmds.br_blendShapeSplitTarget(self.blend_shape, 
            axis='x', 
            invert=-1, 
            blend=blend, 
            center=0, 
            index=right_duplicate_index, 
            originalMesh=og_shape, 
            tolerance=0.001)
        
    def add_target_posed(self, target_mesh):
        #invert shape will throw out the deltas between the based pose base and the target corrective
        delta_mesh = cmds.invertShape(self.mesh, target_mesh)
        valid_index = self.get_valid_target_index()
        cmds.blendShape(self.blend_shape, edit=True, t=(self.mesh, valid_index, delta_mesh, 1.0))
        cmds.delete(delta_mesh)
        