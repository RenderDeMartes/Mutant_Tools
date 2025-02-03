from __future__ import absolute_import, division
'''
version: 1.0.0
date: 21/04/2020

#----------------

how to:

import Mutant_Tools
try:
    import importlib;from importlib import reload
except:
    import imp;from imp import reload

from Mutant_Tools.Utils.Animation import reference_refresher
reload(reference_refresher)
cRefresher = reference_refresher.Refresher()

cRefresher.refresh_all_assets_references()

#----------------
dependencies:

maya cmds
maya mel
pymel


#----------------
licence: https://www.eulatemplate.com/live.php?token=FGISW7ApRfgywum6murbBmLcusKONzkv
author:  Esteban Rodriguez <info@mutanttools.com>

'''
try:
    import importlib;from importlib import reload
except:
    import imp;from imp import reload

import six
import os
import uuid
import tempfile
import pymel.core as pm
from maya import cmds, mel

from Mutant_Tools.Utils.Animation import studio_library_utils, animation_utils
reload(studio_library_utils)
reload(animation_utils)

try:
    from studiolibrarymaya import animitem
except Exception as e:
    cmds.error(e)

class Refresher(object):
    """
    Will Refresh animation reference nodes affected by issue cause by reference edits

    """
    def __init__(self):
        """
                Initialize the Refresher class.
        """
        super(Refresher, self).__init__()

        self.reference_objects = self.get_reference_objects()
        self.assets_reference_objects = self.filter_reference_only_assets()

    def pause_viewport(self):
        """
        Pause the Maya viewport.
        """
        mel.eval('ogs - pause;')

    def get_reference_objects(self):
        """
        Get a list of reference objects in the scene.

        Returns:
            List of reference objects.
        """
        return pm.listReferences()

    def get_reference_object_namespace(self, reference_object):
        """
        Get the namespace of a reference object.

        Args:
            reference_object: Reference object to retrieve the namespace from.

        Returns:
            Namespace of the reference object.
        """
        return reference_object.fullNamespace

    def get_ctrls_in_reference(self, namespace=None):
        """
        Get control objects within the specified namespace.

        Args:
            namespace: Namespace to search for control objects. If None, selects all control objects.

        Returns:
            List of control objects in the given namespace.
        """
        try:cmds.select('{}:*_Ctrl'.format(namespace))
        except:cmds.select('{}:*_ctrl'.format(namespace))

        ctrls = animation_utils.select_ctrls_from_sid()
        return ctrls

    def clean_reference(self, reference_object):
        """
        Clean and reload a reference object.

        Args:
            reference_object: Reference object to clean and reload.
        """
        reference_object.unload()
        reference_object.clean()
        reference_object.load()

    def clean_all_references(self, references=None):
        """
        Clean and reload a list of reference objects.

        Args:
            references: List of reference objects to clean and reload. If None, uses assets_reference_objects.
        """
        if not references:
            references = self.assets_reference_objects

        for ref in references:
            self.clean_reference(ref)

    def get_sid_from_reference_object(self, reference_object):
        """
        Get the name of the 'sid' node associated with a reference object.

        Args:
            reference_object: Reference object to retrieve the 'sid' node name from.

        Returns:
            Name of the 'sid' node.
        """
        nodes = reference_object.nodes()
        for n in nodes:
            if n.type() == 'sid':
                return n.name()

    def filter_reference_only_assets(self):
        """
        Filter and return a list of reference objects associated with asset types (prop, char, vhcl).

        Returns:
            List of reference objects associated with assets.
        """
        #assets chars and props
        assets_refs_objects = []
        for ref in self.reference_objects:
            sid_name = self.get_sid_from_reference_object(reference_object=ref)
            type = cmds.getAttr('{}.type'.format(sid_name))
            if type == 'prop' or type == 'char' or type == 'vhcl':
                assets_refs_objects.append(ref)

        return assets_refs_objects

    def save_temp_animation(self, reference_object):
        """
        Save a temporary animation file for a given reference object.

        Args:
            reference_object: Reference object to save the animation for.

        Returns:
            Path to the temporary animation file.
        """
        temp_folder = os.path.join(tempfile.gettempdir(), 'Refresher', str(uuid.uuid4().hex+'.anim'))


        ns = self.get_reference_object_namespace(reference_object)
        ctrls = self.get_ctrls_in_reference(namespace=ns)
        cmds.select(ctrls)

        objects = cmds.ls(selection=True) or []

        keys_data = cmds.keyframe(ctrls, q=True)
        if not keys_data:
            return False

        start = cmds.playbackOptions(animationStartTime=True, q=True)
        end = cmds.playbackOptions(animationEndTime=True, q=True)

        animitem.save(path=temp_folder, objects=objects, frameRange=(start, end), bakeConnected=False)
        print(temp_folder)

        return temp_folder

    def load_temp_animation(self, reference_object, folder):
        """
        Load a temporary animation file onto a reference object.

        Args:
            reference_object: Reference object to load the animation onto.
            folder: Path to the temporary animation file.

        Returns:
            True if the animation is successfully loaded, False otherwise.
        """
        ns = self.get_reference_object_namespace(reference_object)
        ctrls = self.get_ctrls_in_reference(namespace=ns)
        cmds.select(ctrls)

        objects = cmds.ls(selection=True) or []

        animitem.load(folder, objects=objects, option="replace all", connect=False, currentTime=False)

        return True

    def refresh_reference(self, reference_object):
        """
        Refresh a reference object by cleaning, saving, and loading animation.

        Args:
            reference_object: Reference object to refresh.

        Returns:
            True if the refresh process is successful, False otherwise.
        """
        folder = self.save_temp_animation(reference_object)
        if not folder:
            return False
        self.clean_reference(reference_object)
        self.load_temp_animation(reference_object, folder)

        return True

    def refresh_all_assets_references(self):
        """
        Refresh all asset-related reference objects.

        Returns:
            True if the refresh process is successful, False otherwise.
        """
        self.pause_viewport()

        #contraints_map = self.get_constraints_connections()
        shared_data = self.save_shared_locs_anim()

        for ref in self.assets_reference_objects:
            self.refresh_reference(ref)

        self.apply_shared_locs_anim(shared_data)
        #self.reconnet_constriants(contraints_map)

        self.pause_viewport()

        cmds.select(cl=True)

        return True

    def get_constriants_in_scene(self):

        pr_constriants = cmds.ls('*', type='parentConstraint')
        p_constriants = cmds.ls('*', type='pointConstraint')
        o_constriants = cmds.ls('*', type='orientConstraint')

        return pr_constriants, p_constriants, o_constriants

    def get_constraints_connections(self):

        pr_constriants, p_constriants, o_constriants = self.get_constriants_in_scene()

        connections = {}
        for c in pr_constriants + p_constriants + o_constriants:
            print(c)
            destination = cmds.listConnections(c+'.constraintParentInverseMatrix')
            source = cmds.listConnections(c+'.target[0].targetRotate')
            type = cmds.nodeType(c)
            print(c, destination, source, type)
            connections[c] = {'destination':destination, 'source':source, 'type':type}

        return connections

    def reconnet_constriants(self, contraints_map):

        for c in contraints_map:
            destination = contraints_map[c]['destination']
            source = contraints_map[c]['source']
            type = contraints_map[c]['type']
            print(c, destination, source, type)

            if not source or not destination:
                cmds.warning('Error With {} {} {} [}'.format(c, destination, source, type))
                continue

            if type == 'parentConstraint':
                cmds.parentConstraint(source, destination, mo=True)
            elif type == 'orientConstraint':
                cmds.orientConstraint(source, destination, mo=True)
            elif type == 'scaleConstraint':
                cmds.scaleConstraint(source, destination, mo=True)
            else:
                cmds.warning('Issues with: {} {} {} {}'.format(c, destination, source, type))

    def save_shared_locs_anim(self):
        data = {}
        objectNames = cmds.ls(['*:*Switch_Loc'])
        for o in objectNames:
            attributes = cmds.listAttr(o, ud=True)
            if not attributes:
                continue
            for attr in attributes:
                # all the time value
                frames = cmds.keyframe(o, q=1, at=attr)
                # all the attribute value associated
                values = cmds.keyframe(o, q=1, at=attr, valueChange=True)
                if not values:
                    continue
                # store it in the dictionary with key 'objectName.attribute'
                data['{}.{}'.format(o, attr)] = list(zip(frames, values))

        return data

    def apply_shared_locs_anim(self, data):
        for k, v in six.iteritems(data):
            for t, x in v:
                o, a = k.split('.')
                cmds.setKeyframe(o, time=t, attribute=a, value=x)