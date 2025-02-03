from __future__ import absolute_import
'''
version: 1.0.0
date: 21/04/2020

#----------------

how to:

try:
    import importlib;from importlib import reload
except:
    import imp;from imp import reload

import Mutant_Tools
import Mutant_Tools.Utils.Wrap.FACS
from Mutant_Tools.Utils.Wrap.FACS import facs_utils
reload(facs_utils)
cWrapFACS = facs_utils.WrapFACS()


cWrapFACS.init_scene(force=True)
cWrapFACS.new_face='Body_Geo'
cWrapFACS.create_new_shapes()

#----------------
dependencies:

Wrap3D
maya cmds
maya mel
pymel


#----------------
licence: https://www.eulatemplate.com/live.php?token=FGISW7ApRfgywum6murbBmLcusKONzkv
author:  Esteban Rodriguez <info@mutanttools.com>

'''

from pathlib import Path
from maya import cmds
import os

try:
    import importlib;from importlib import reload
except:
    import imp;from imp import reload

import Mutant_Tools
import Mutant_Tools.Utils.Rigging
from Mutant_Tools.Utils.Rigging import main_mutant
reload(Mutant_Tools.Utils.Rigging.main_mutant)
mt = main_mutant.Mutant()

PATH = os.path.dirname(__file__)
PATH = Path(PATH)
PATH_PARTS = PATH.parts[:-3]
FOLDER = ''
for f in PATH_PARTS:
	FOLDER = os.path.join(FOLDER, f)

class WrapFACS(object):

    def __init__(self):
        super(WrapFACS, self).__init__()

        self.facs_file = 'FACS_Rig_01.ma'
        self.facs_path = os.path.join(FOLDER, 'Utils', 'Wrap', 'FACS', self.facs_file)

        self.new_face = None #face to tranfer shapes to
        self.transf0_face = 'transf0' #Wrapped face
        self.wrap_base_mesh = 'WrapBaseMesh' #Face with blendshapes oringal

        self.targets_grp = 'Targets'
        self.targets = self.get_targets()
        self.targets_bsp = 'Targets_BSP'

        self.wrap = None

    def init_scene(self, force):

        if not cmds.objExists(self.transf0_face):
            cmds.error("We need {} for the FACS transfer to work, please use Zombinator to create it".format(self.transf0_face))

        self.import_facs_file(force=force)
        self.create_initial_blendshape()

        return True

    def import_facs_file(self, force=False):
        if force:
            for i in [self.wrap_base_mesh, self.targets_grp, self.targets_bsp]:
                if cmds.objExists(i):
                    cmds.delete(i)

        if cmds.objExists(self.wrap_base_mesh):
            cmds.error("{} Geo already exists in scene, please delete before importing".format(self.wrap_base_mesh))

        if cmds.objExists(self.targets_grp):
            cmds.error("{} Group already exists in scene, please delete before importing".format(self.targets_grp))

        if cmds.objExists(self.targets_bsp):
            cmds.error("{} Blendshape node already exists in scene, please delete before importing".format(self.targets_bsp))
        print(self.facs_path)
        cmds.file(self.facs_path, i=True, type="mayaAscii", mergeNamespacesOnClash=False, rpr='')

        return True

    def open_facs_file(self):
        print(self.facs_path)
        cmds.file(self.facs_path, open=True, type="mayaAscii", f=True)

    def get_targets(self):
        if cmds.objExists(self.targets_grp):
            return cmds.listRelatives(self.targets_grp, c=True, type='transform')
        else:
            return []


    def create_initial_blendshape(self):

        targets = self.get_targets()
        print(self.transf0_face, self.wrap_base_mesh)
        print('Targets', targets)
        bsp = cmds.blendShape(self.transf0_face, targets, self.wrap_base_mesh, n=self.targets_bsp, w=[0, 1])

        return True


    def transfer_with_wrap(self, wrap_base_mesh=None, destination_mesh=None):
        if not wrap_base_mesh:
            wrap_base_mesh = self.wrap_base_mesh #meshA with facs

        if not destination_mesh:
            destination_mesh = self.new_face #meshB new geo

        cmds.select(destination_mesh, wrap_base_mesh)
        cmds.CreateWrap()
        wrap = cmds.listConnections('%s.worldMatrix[0]'%cmds.listRelatives(destination_mesh, c=True)[0], plugs=True)[0].split('.')[0]
        return wrap

    def createProximityWrap(self, source, target):
        """https://gist.github.com/MongoWobbler/f6cd5fa7d9ae9a60d89fb6052f6078b6
        Creates a proximity with the given source and target transforms.
        Args:
            source (pm.nodetypes.Transform): Transform with skinned mesh that will drive given target.
            target (pm.nodetypes.Transform): Transform with mesh shape that will be driven by given source.
        Returns:
            (pm.nodetypes.ProximityWrap): Proximity wrap node created.
        """
        # implementing with maya.cmds since PyMel raises the following warning for every attribute set.
        # Warning: pymel.core.general : Could not create desired MFn. Defaulting to MFnDependencyNode.
        import maya.cmds as cmds
        import maya.internal.nodes.proximitywrap.node_interface as node_interface
        import pymel.core as pm

        source = pm.PyNode(source)
        target = pm.PyNode(target)

        deformer = cmds.deformer(target.name(), type='proximityWrap', name=target.name(stripNamespace=True) + '_pWrap')[0]
        
        # personal preference of proximity wrap attributes, these could be exposed as kwargs too!
        cmds.setAttr(deformer + '.maxDrivers', 1)
        cmds.setAttr(deformer + '.falloffScale', 1.4)
        cmds.setAttr(deformer + '.smoothInfluences', 5)
        cmds.setAttr(deformer + '.smoothNormals', 5)

        proximity_interface = node_interface.NodeInterface(deformer)
        proximity_interface.addDriver(source.getShapes()[-1].name())  # last shape should be the deformed shape
        return deformer

    def transfer_with_proximity_wrap(self, wrap_base_mesh=None, destination_mesh=None):

        """
        THIS ONE DOESNT WORK YET

        Args:
            wrap_base_mesh:
            destination_mesh:

        Returns:

        """

        if not wrap_base_mesh:
            wrap_base_mesh = self.wrap_base_mesh #meshA with facs

        if not destination_mesh:
            destination_mesh = self.new_face #meshB new geo

        deformer = self.createProximityWrap(wrap_base_mesh, destination_mesh)
        return deformer
        


    def  crate_new_shape(self, wrap_base_mesh=None, new_face=None, name='Shape'):
        if not wrap_base_mesh:
            wrap_base_mesh = self.wrap_base_mesh

        if not new_face:
            new_face = self.new_face

        dup_new_face = cmds.duplicate(new_face, n=new_face+'_'+name+'Target')[0]
        cmds.parent(dup_new_face, w=True)

        return dup_new_face

    def create_new_shapes(self, wrap_base_mesh=None, new_face=None, targets=[], mode='NotProximity', apply_delta=True, delta_attrs={'distanceWeight':1, 'smoothingIterations':2}):
        if not wrap_base_mesh:
            wrap_base_mesh = self.wrap_base_mesh

        if not new_face:
            new_face = self.new_face

        if not targets:
            targets = self.get_targets()

        #Turn Bsp Targets off exept the transf0
        for t in targets:
            cmds.setAttr('{}.{}'.format(self.targets_bsp, t), 0)

        if mode == 'Proximity':
            self.wrap = self.transfer_with_proximity_wrap(wrap_base_mesh=wrap_base_mesh, destination_mesh=new_face)
        else:
            self.wrap= self.transfer_with_wrap(wrap_base_mesh=wrap_base_mesh, destination_mesh=new_face)
        
    
        if apply_delta:
            #create delta
            delta = cmds.deltaMush(self.new_face, n='Zombinator_DeltaMush')[0]
            if delta_attrs:
                for attr in delta_attrs:
                    cmds.setAttr('{}.{}'.format(delta, attr), delta_attrs[attr])

        new_geos = []
        for target in targets:
            print(target)
            print(self.targets_bsp, target)
            # Turn Bsp Targets on
            cmds.setAttr('{}.{}'.format(self.targets_bsp, target), 1)
            dup_geo = self.crate_new_shape(wrap_base_mesh=wrap_base_mesh, new_face=new_face,
                                           name=target)
            new_geos.append(dup_geo)
            cmds.setAttr('{}.{}'.format(self.targets_bsp, target), 0)

        if self.wrap:
            cmds.delete(self.wrap)
            self.wrap = None

        if apply_delta:
            if delta:
                cmds.delete(delta)

        #Turn Bsp Targets off exept the transf0
        for t in targets:
            cmds.setAttr('{}.{}'.format(self.targets_bsp, t), 0)

        print('New Geos', new_geos)
        return new_geos

    def clean_scene(self):
        nodes = [self.targets_bsp, self.targets_grp, self.wrap_base_mesh]
        for n in nodes:
            if cmds.objExists(n):
                cmds.delete(n)