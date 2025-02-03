from __future__ import absolute_import
'''
    SCRIPT NAME:
        fari_deformersWeightsEditor

    AUTHOR:
        Paolo Farinello - paolo.farinello@gmail.com

    DESCRIPTION:
        Enables operations such as import/export, copy, mirror and flip on deformers weights, focusing on deformers which differ from the skinCluster.
        Affected deformers are: blendShape, cluster, ffd, nonLinear, shrinkWrap and wire deformers.

    INSTALL:
        1. Put the script file in Maya scripts folder (usually C:/Users/User/Documents/maya/20xx/scripts)
        2. Depending on the Python version supported by Maya, type the following in a python tab of the script editor:
            PYTHON 2.X
            import fari_deformersWeightsEditor; reload(fari_deformersWeightsEditor)

            PYTHON <= 3.3
            import imp; import fari_deformersWeightsEditor; imp.reload(fari_deformersWeightsEditor)

            PYTHON >= 3.4
            import importlib; import fari_deformersWeightsEditor; importlib.reload(fari_deformersWeightsEditor)

    LOG:
        Version: 1.0.0
        Date: 10 August 2021
        - First release

        Version: 2.0.0
        Date: 10 May 2022
        - Upgrade for newer versions of Maya installing Python 3.X. PyMEL for Python 3 is required to be installed. More information on how to install PyMEL can be found at the following link: https://knowledge.autodesk.com/support/maya/learn-explore/caas/CloudHelp/cloudhelp/2022/ENU/Maya-Scripting/files/GUID-2AA5EFCE-53B1-46A0-8E43-4CD0B2C72FB4-htm.html
        - Compatibility with older versions of Maya, equipped with Python 2.7, can be achieved installing Python future package, which is available for download at the following link: https://pypi.org/project/future/
          (Compatibility with versions of Maya prior to 2016 != guaranteed. Note also that versions of Maya prior to 2018 do not support painting ffd weights)
        - Mirror, flip and copy operations now work much faster
          (True only in Maya supporting newer versions of the api)
'''

from __future__ import absolute_import, division, print_function
from builtins import ascii, bytes, chr, dict, filter, hex, input, int, map, next, oct, open, pow, range, round, str, \
    super, zip
from builtins import object as builtin_object
import os, sys, json, math
import pymel.core as pmc
import maya.api.OpenMaya as om
import maya.api.OpenMayaAnim as oma


class DeformersWeightsEditor(builtin_object):

    @classmethod
    def showUI(cls):
        win = cls()
        win.create()
        pmc.textFieldButtonGrp(win.importExportGroup, edit=True, fileName=win.working_dir)
        return win

    def __init__(self):
        super(DeformersWeightsEditor, self).__init__()
        self.win_name = 'DWEwindow'
        self.win_title = 'Deformers Weights Editor'
        self.win_size = (600, 540)
        self_input_mesh = []
        self.working_dir = pmc.workspace(query=True, directory=True)
        if int(pmc.about(version=True)) < 2018:
            self.valid_deformers = ['blendShape', 'cluster', 'nonLinear', 'shrinkWrap', 'wire']
        else:
            self.valid_deformers = ['blendShape', 'cluster', 'ffd', 'nonLinear', 'shrinkWrap', 'wire']
        self.symmetry_axis = {1: 0, 2: 1, 3: 2}
        self.copy_source_info = []
        self.copy_target_info = []

    def create(self):
        if (pmc.window(self.win_name, exists=True)):
            pmc.deleteUI(self.win_name, window=True)
        pmc.window(self.win_name, title=self.win_title, widthHeight=self.win_size, sizeable=True)

        self.mainForm = pmc.formLayout(numberOfDivisions=100)
        self.deformerFrame = pmc.frameLayout(parent=self.mainForm, label='Deformer Select', collapsable=True)
        self.importExportFrame = pmc.frameLayout(parent=self.mainForm, label='Weights Import/Export', collapsable=True)
        self.mirrorFrame = pmc.frameLayout(parent=self.mainForm, label='Weights Mirror', collapsable=True)
        self.copyFrame = pmc.frameLayout(parent=self.mainForm, label='Weights Copy', collapsable=True)
        pmc.formLayout(self.mainForm, edit=True,
                       attachForm=([self.deformerFrame, 'top', 0], [self.deformerFrame, 'left', 0],
                                   [self.deformerFrame, 'right', 0], [self.importExportFrame, 'left', 0],
                                   [self.importExportFrame, 'right', 0], [self.mirrorFrame, 'left', 0],
                                   [self.mirrorFrame, 'right', 0], [self.copyFrame, 'left', 0],
                                   [self.copyFrame, 'right', 0]),
                       attachControl=([self.importExportFrame, 'top', 10, self.deformerFrame],
                                      [self.mirrorFrame, 'top', 10, self.importExportFrame],
                                      [self.copyFrame, 'top', 10, self.mirrorFrame]))

        self.deformerForm = pmc.formLayout(parent=self.deformerFrame, numberOfDivisions=100)
        self.meshGroup = pmc.textFieldButtonGrp(parent=self.deformerForm, label='Mesh:', buttonLabel='   <<<   ',
                                                adjustableColumn=2, columnAttach3=['left', 'left', 'left'],
                                                columnWidth3=[30, 100, 100], columnOffset3=[0, 32, 15],
                                                buttonCommand=self.mesh_button_command,
                                                changeCommand=self.mesh_field_command)
        self.deformersText = pmc.text(parent=self.deformerForm, label='Deformers:')
        self.deformersList = pmc.textScrollList(parent=self.deformerForm, allowMultiSelection=False, numberOfRows=1,
                                                height=100, width=440)
        pmc.formLayout(self.deformerForm, edit=True,
                       attachForm=(
                       [self.meshGroup, 'top', 5], [self.meshGroup, 'left', 10], [self.meshGroup, 'right', 10],
                       [self.deformersText, 'left', 10], [self.deformersList, 'right', 40]),
                       attachControl=(
                       [self.deformersText, 'top', 5, self.meshGroup], [self.deformersList, 'top', 5, self.meshGroup],
                       [self.deformersList, 'left', 10, self.deformersText]))

        self.importExportForm = pmc.formLayout(parent=self.importExportFrame, numberOfDivisions=100)
        self.importExportGroup = pmc.textFieldButtonGrp(parent=self.importExportForm, label='Start Directory:',
                                                        buttonLabel='  Browse  ', adjustableColumn=2,
                                                        columnAttach3=['left', 'left', 'left'],
                                                        columnWidth3=[75, 100, 100], columnOffset3=[0, 15, 15],
                                                        buttonCommand=self.dir_button_command,
                                                        changeCommand=self.dir_field_command)
        self.loadParameters = pmc.text(parent=self.importExportForm, label='Load Parameters:')
        self.loadVertices = pmc.radioButtonGrp(parent=self.importExportForm, numberOfRadioButtons=2, label='ALGORITHM',
                                               labelArray2=['vertex index', 'vertex position'], select=1,
                                               columnAttach3=['left', 'left', 'left'], columnWidth3=[72, 100, 100],
                                               columnOffset3=[0, 0, 0], onCommand1=self.index_algorithm,
                                               onCommand2=self.position_algorithm)
        self.loadTolerance = pmc.textFieldGrp(parent=self.importExportForm, label='TOLERANCE', adjustableColumn=2,
                                              columnAttach2=['left', 'left'], columnWidth2=[68, 100],
                                              columnOffset2=[0, 0], text='0.1', enable=False,
                                              changeCommand=self.set_tolerance,
                                              annotation='Tolerance must be of type "float". Only positive, non-zero values are allowed')
        self.saveButton = pmc.button(parent=self.importExportForm, label='Save Weights', width=150,
                                     command=self.save_weights,
                                     annotation='Select the vertices whose weights to be saved')
        self.loadButton = pmc.button(parent=self.importExportForm, label='Load Weights', width=150,
                                     command=self.load_weights,
                                     annotation='Select the vertices whose weights to be loaded')
        pmc.formLayout(self.importExportForm, edit=True,
                       attachForm=([self.importExportGroup, 'top', 5], [self.importExportGroup, 'left', 10],
                                   [self.importExportGroup, 'right', 10], [self.loadParameters, 'left', 10],
                                   [self.loadVertices, 'left', 50], [self.saveButton, 'left', 125]),
                       attachControl=([self.loadParameters, 'top', 5, self.importExportGroup],
                                      [self.loadVertices, 'top', 5, self.loadParameters],
                                      [self.loadTolerance, 'top', 5, self.loadParameters],
                                      [self.loadTolerance, 'left', 50, self.loadVertices],
                                      [self.saveButton, 'top', 10, self.loadVertices],
                                      [self.loadButton, 'top', 10, self.loadVertices],
                                      [self.loadButton, 'left', 50, self.saveButton]))

        self.mirrorForm = pmc.formLayout(parent=self.mirrorFrame, numberOfDivisions=100)
        self.symmetryPlane = pmc.radioButtonGrp(parent=self.mirrorForm, numberOfRadioButtons=3, label='Symmetry Plane:',
                                                labelArray3=['YZ', 'XZ', 'XY'], select=1,
                                                columnAttach4=['left', 'left', 'left', 'left'],
                                                columnOffset4=[0, 0, 0, 0], columnWidth4=[100, 80, 80, 80],
                                                annotation='Symmertry plane refers to the selected mesh local axes')
        self.symmetryDirection = pmc.radioButtonGrp(parent=self.mirrorForm, numberOfRadioButtons=2, label='Direction:',
                                                    labelArray2=['from positive to negative',
                                                                 'from negative to positive'], select=1,
                                                    columnAttach3=['left', 'left', 'left'], columnOffset3=[0, 0, 0],
                                                    columnWidth3=[100, 200, 200])
        self.mirrorButton = pmc.button(parent=self.mirrorForm, label='Mirror Weights', command=self.mirror_weights,
                                       annotation='Select the vertices whose weights to be mirrored', width=150)
        self.flipButton = pmc.button(parent=self.mirrorForm, label='Flip Weights', command=self.flip_weights,
                                     annotation='Select the vertices whose weights to be flipped', width=150)
        pmc.formLayout(self.mirrorForm, edit=True,
                       attachForm=([self.symmetryPlane, 'top', 5], [self.symmetryPlane, 'left', 10],
                                   [self.symmetryDirection, 'left', 10], [self.mirrorButton, 'left', 125]),
                       attachControl=([self.symmetryDirection, 'top', 5, self.symmetryPlane],
                                      [self.mirrorButton, 'top', 10, self.symmetryDirection],
                                      [self.flipButton, 'top', 10, self.symmetryDirection],
                                      [self.flipButton, 'left', 50, self.mirrorButton]))

        self.copyForm = pmc.formLayout(parent=self.copyFrame, numberOfDivisions=100)
        self.sourceButton = pmc.button(parent=self.copyForm, label='Source', command=self.copy_source,
                                       annotation='Select the deformer to copy weights from', width=100)
        self.sourceText = pmc.text(parent=self.copyForm,
                                   label=' - Select a valid deformer from the deformers list above')
        self.targetButton = pmc.button(parent=self.copyForm, label='Target', command=self.copy_target,
                                       annotation='Select the deformer to copy weights to', width=100)
        self.targetText = pmc.text(parent=self.copyForm,
                                   label=' - Select a valid deformer from the deformers list above')
        self.copyButton = pmc.button(parent=self.copyForm, label='Copy', command=self.copy_weights,
                                     annotation='Select valid source and target deformers', width=150)
        pmc.formLayout(self.copyForm, edit=True,
                       attachForm=(
                       [self.sourceButton, 'top', 7], [self.sourceButton, 'left', 10], [self.sourceText, 'top', 12],
                       [self.targetButton, 'left', 10], [self.copyButton, 'left', 225]),
                       attachControl=([self.sourceText, 'left', 10, self.sourceButton],
                                      [self.targetButton, 'top', 7, self.sourceButton],
                                      [self.targetText, 'top', 17, self.sourceText],
                                      [self.targetText, 'left', 10, self.targetButton],
                                      [self.copyButton, 'top', 5, self.targetButton]))

        pmc.showWindow()

    def get_deformers_legacy(self):
        # fill deformers_list
        deformers_list = []
        deformer_sets = pmc.listSets(type=2, object=self.input_mesh)
        deformer_names = [deformer_sets[index].getAttr('usedBy[0]') for index in range(0, len(deformer_sets))]
        for d_name in deformer_names:
            d_type = pmc.objectType(d_name)
            if d_type in self.valid_deformers:
                deformers_list.append({'Name': d_name, 'Type': d_type})

        if deformers_list:
            def custom_sort(list_element):
                return list_element['Type'] + list_element['Name']

            deformers_list.sort(key=custom_sort)
            return deformers_list

        else:
            return None

    def get_deformers(self):
        # fill deformers_list
        deformers_list = []
        deformer_names = pmc.findDeformers(self.input_mesh)
        for d_name in deformer_names:
            d_type = pmc.objectType(d_name)
            if d_type in self.valid_deformers:
                deformers_list.append({'Name': d_name, 'Type': d_type})

        if deformers_list:
            def custom_sort(list_element):
                return list_element['Type'] + list_element['Name']

            deformers_list.sort(key=custom_sort)
            return deformers_list

        else:
            return None

    def get_target_shape(self, target):
        target_shape = None

        if pmc.objExists(target):
            sel_list = pmc.ls(target)
            shape_list = pmc.listRelatives(sel_list[0], shapes=True, path=True, noIntermediate=True)
            if shape_list:
                target_shape = shape_list[0]
            else:
                target_shape = sel_list[0]

        return target_shape

    def get_dag_path(self, target):
        sel_list = om.MSelectionList()
        sel_list.add(str(target))
        target_path = sel_list.getDagPath(0)

        return target_path

    def get_depend_node(self, target):
        sel_list = om.MSelectionList()
        sel_list.add(target)
        target_node = sel_list.getDependNode(0)

        return target_node

    def is_a_mesh(self, target_shape):
        return_value = False

        target_type = pmc.objectType(target_shape)
        if target_type == 'mesh':
            return_value = True

        return return_value

    def deformers_scroll_list(self):
        # preliminary operations
        pmc.textScrollList(self.deformersList, edit=True, removeAll=True)

        # fill deformer scroll list
        if 'findDeformers' in dir(pmc):
            deformers_list = self.get_deformers()
        else:
            deformers_list = self.get_deformers_legacy()
        if deformers_list:
            for d_item in deformers_list:
                list_entry = d_item['Type'] + ' - ' + d_item['Name']
                pmc.textScrollList(self.deformersList, edit=True, append=list_entry)

        else:
            pmc.warning('No valid deformer affects the selected mesh')

    def find_target_index(self, deformer_node, target_path):
        target_index = []
        deformer_fnSet = oma.MFnGeometryFilter(deformer_node)
        output_geo_num = deformer_fnSet.numOutputConnections()
        for conn_index in range(0, output_geo_num):
            plug_index = deformer_fnSet.indexForOutputConnection(conn_index)
            output_geo = deformer_fnSet.getPathAtIndex(plug_index)
            if (output_geo == target_path):
                target_index.append(plug_index)
                break

        return target_index

    def get_deformer_weights_legacy(self, target=None, deformer_name=None, ID=None):
        # preliminary operations
        weights_map = {}
        target_path = None
        selected_deformer = None
        vtx_components = []
        members_ID = []
        non_members_ID = []

        # input validation
        if target != None:
            target_shape = self.get_target_shape(target)
            if target_shape != None:
                if self.is_a_mesh(target_shape):
                    target_path = self.get_dag_path(target_shape)
        else:
            if self.input_mesh:
                target_path = self.get_dag_path(self.input_mesh)
        if target_path is None:
            raise ValueError('Select a valid mesh')

        if deformer_name != None:
            if pmc.objExists(deformer_name):
                if pmc.objectType(deformer_name) in self.valid_deformers:
                    selected_deformer = deformer_name
        else:
            deformers_list_entry = pmc.textScrollList(self.deformersList, query=True, selectItem=True)
            if deformers_list_entry:
                selected_deformer = deformers_list_entry[0].split(' - ')[1]
        if selected_deformer is None:
            raise ValueError('Select a valid deformer')
        deformer_node = self.get_depend_node(selected_deformer)
        deformer_fnSet = om.MFnDependencyNode(deformer_node)
        target_index = self.find_target_index(deformer_node, target_path)
        if not target_index:
            raise ValueError('"{Name1}" does not affect "{Name2}"'.format(Name1=selected_deformer, Name2=target_path))

        sel_list = om.MSelectionList()
        sel_list.add(oma.MFnGeometryFilter(deformer_node).deformerSet)
        deformer_set = om.MFnDependencyNode(sel_list.getDependNode(0)).name()
        if ID != None:
            target_vtx_num = om.MFnMesh(target_path).numVertices
            target_vtx_ID = range(0, target_vtx_num)
            if max(ID) > target_vtx_num:
                raise ValueError(
                    'Mesh "{Name}" does not contain selected vertices: vertex ID out of range'.format(Name=target_path))
            vtx_comp_fnSet = om.MFnSingleIndexedComponent()
            vtx_comp = vtx_comp_fnSet.create(om.MFn.kMeshVertComponent)
            vtx_comp_fnSet.addElements(ID)
            vtx_components.append((target_path, vtx_comp))
        else:
            selection = om.MGlobal.getActiveSelectionList()
            selection_iterator = om.MItSelectionList(selection, om.MFn.kMeshVertComponent)
            if selection_iterator.isDone():
                raise ValueError('Select the vertices to read deformer weights from')
            while not selection_iterator.isDone():
                current_component = selection_iterator.getComponent()
                if not current_component[0] == target_path:
                    raise ValueError('Selected vertices do not belong to mesh "{Name}"'.format(Name=target_path))
                vtx_components.append((current_component[0], current_component[1]))
                next(selection_iterator)
        for comp_item in vtx_components:
            vtx_iterator = om.MItMeshVertex(comp_item[0], comp_item[1])
            while not vtx_iterator.isDone():
                vtx_name = '{Name1}.vtx[{Name2}]'.format(Name1=str(target_path), Name2=str(vtx_iterator.index()))
                if pmc.sets(deformer_set, isMember=vtx_name):
                    members_ID.append(vtx_iterator.index())
                else:
                    non_members_ID.append(vtx_iterator.index())
                next(vtx_iterator)

        # get weights
        members_ID_not_listed = members_ID
        weights_list_plug = deformer_fnSet.findPlug('weightList', True)
        weights_list_array = weights_list_plug.getExistingArrayAttributeIndices()
        if target_index[0] in weights_list_array:
            weights_plug = weights_list_plug.elementByLogicalIndex(target_index[0]).child(0)
            weights_array = weights_plug.getExistingArrayAttributeIndices()
            for index in weights_array:
                if index in members_ID:
                    weights_map.setdefault(index, weights_plug.elementByLogicalIndex(index).asFloat())
                    members_ID_not_listed.remove(index)
        for index in members_ID_not_listed:
            weights_map.setdefault(index, 1)
        for index in non_members_ID:
            weights_map.setdefault(index, 0)

        return weights_map

    def get_deformer_weights(self, target=None, deformer_name=None, ID=None):
        # preliminary operations
        weights_map = {}
        target_path = None
        selected_deformer = None
        vtx_components = []
        members_ID = []
        non_members_ID = []

        # input validation
        if target != None:
            target_shape = self.get_target_shape(target)
            if target_shape != None:
                if self.is_a_mesh(target_shape):
                    target_path = self.get_dag_path(target_shape)
        else:
            if self.input_mesh:
                target_path = self.get_dag_path(self.input_mesh)
        if target_path is None:
            raise ValueError('Select a valid mesh')

        if deformer_name != None:
            if pmc.objExists(deformer_name):
                if pmc.objectType(deformer_name) in self.valid_deformers:
                    selected_deformer = deformer_name
        else:
            deformers_list_entry = pmc.textScrollList(self.deformersList, query=True, selectItem=True)
            if deformers_list_entry:
                selected_deformer = deformers_list_entry[0].split(' - ')[1]
        if selected_deformer is None:
            raise ValueError('Select a valid deformer')
        deformer_node = self.get_depend_node(selected_deformer)
        deformer_fnSet = om.MFnDependencyNode(deformer_node)
        target_index = self.find_target_index(deformer_node, target_path)
        if not target_index:
            raise ValueError('"{Name1}" does not affect "{Name2}"'.format(Name1=selected_deformer, Name2=target_path))

        deformer_set = oma.MFnGeometryFilter(deformer_node).deformerSet
        deformer_set_members = om.MFnSet(deformer_set).getMembers(flatten=True)
        if ID != None:
            target_vtx_num = om.MFnMesh(target_path).numVertices
            target_vtx_ID = range(0, target_vtx_num)
            if max(ID) > target_vtx_num:
                raise ValueError(
                    'Mesh "{Name}" does not contain selected vertices: vertex ID out of range'.format(Name=target_path))
            vtx_comp_fnSet = om.MFnSingleIndexedComponent()
            vtx_comp = vtx_comp_fnSet.create(om.MFn.kMeshVertComponent)
            vtx_comp_fnSet.addElements(ID)
            vtx_components.append((target_path, vtx_comp))
        else:
            selection = om.MGlobal.getActiveSelectionList()
            selection_iterator = om.MItSelectionList(selection, om.MFn.kMeshVertComponent)
            if selection_iterator.isDone():
                raise ValueError('Select the vertices to read deformer weights from')
            while not selection_iterator.isDone():
                current_component = selection_iterator.getComponent()
                if not current_component[0] == target_path:
                    raise ValueError('Selected vertices do not belong to mesh "{Name}"'.format(Name=target_path))
                vtx_components.append((current_component[0], current_component[1]))
                next(selection_iterator)
        for comp_item in vtx_components:
            vtx_iterator = om.MItMeshVertex(comp_item[0], comp_item[1])
            while not vtx_iterator.isDone():
                current_vtx_comp = vtx_iterator.currentItem()
                if deformer_set_members.hasItem((comp_item[0], current_vtx_comp)):
                    members_ID.append(vtx_iterator.index())
                else:
                    non_members_ID.append(vtx_iterator.index())
                next(vtx_iterator)

        # get weights
        members_ID_not_listed = members_ID
        weights_list_plug = deformer_fnSet.findPlug('weightList', True)
        weights_list_array = weights_list_plug.getExistingArrayAttributeIndices()
        if target_index[0] in weights_list_array:
            weights_plug = weights_list_plug.elementByLogicalIndex(target_index[0]).child(0)
            weights_array = weights_plug.getExistingArrayAttributeIndices()
            for index in weights_array:
                if index in members_ID:
                    weights_map.setdefault(index, weights_plug.elementByLogicalIndex(index).asFloat())
                    members_ID_not_listed.remove(index)
        for index in members_ID_not_listed:
            weights_map.setdefault(index, 1)
        for index in non_members_ID:
            weights_map.setdefault(index, 0)

        return weights_map

    def get_deformer_weights_future(self, target=None, deformer_name=None, ID=None):
        # preliminary operations
        weights_map = {}
        target_path = None
        selected_deformer = None
        vtx_components = []
        members_ID = []

        # input validation
        if target != None:
            target_shape = self.get_target_shape(target)
            if target_shape != None:
                if self.is_a_mesh(target_shape):
                    target_path = self.get_dag_path(target_shape)
        else:
            if self.input_mesh:
                target_path = self.get_dag_path(self.input_mesh)
        if target_path is None:
            raise ValueError('Select a valid mesh')

        if deformer_name != None:
            if pmc.objExists(deformer_name):
                if pmc.objectType(deformer_name) in self.valid_deformers:
                    selected_deformer = deformer_name
        else:
            deformers_list_entry = pmc.textScrollList(self.deformersList, query=True, selectItem=True)
            if deformers_list_entry:
                selected_deformer = deformers_list_entry[0].split(' - ')[1]
        if selected_deformer is None:
            raise ValueError('Select a valid deformer')
        deformer_node = self.get_depend_node(selected_deformer)
        deformer_fnSet = om.MFnDependencyNode(deformer_node)
        target_index = self.find_target_index(deformer_node, target_path)
        if not target_index:
            raise ValueError('"{Name1}" does not affect "{Name2}"'.format(Name1=selected_deformer, Name2=target_path))

        if ID != None:
            target_vtx_num = om.MFnMesh(target_path).numVertices
            target_vtx_ID = range(0, target_vtx_num)
            if max(ID) > target_vtx_num:
                raise ValueError(
                    'Mesh "{Name}" does not contain selected vertices: vertex ID out of range'.format(Name=target_path))
            vtx_comp_fnSet = om.MFnSingleIndexedComponent()
            vtx_comp = vtx_comp_fnSet.create(om.MFn.kMeshVertComponent)
            vtx_comp_fnSet.addElements(ID)
            vtx_components.append((target_path, vtx_comp))
        else:
            selection = om.MGlobal.getActiveSelectionList()
            selection_iterator = om.MItSelectionList(selection, om.MFn.kMeshVertComponent)
            if selection_iterator.isDone():
                raise ValueError('Select the vertices to read deformer weights from')
            while not selection_iterator.isDone():
                current_component = selection_iterator.getComponent()
                if not current_component[0] == target_path:
                    raise ValueError('Selected vertices do not belong to mesh "{Name}"'.format(Name=target_path))
                vtx_components.append((current_component[0], current_component[1]))
                next(selection_iterator)
        for comp_item in vtx_components:
            vtx_iterator = om.MItMeshVertex(comp_item[0], comp_item[1])
            while not vtx_iterator.isDone():
                members_ID.append(vtx_iterator.index())
                next(vtx_iterator)

        # get weights
        members_ID_not_listed = members_ID
        weights_list_plug = deformer_fnSet.findPlug('weightList', True)
        weights_list_array = weights_list_plug.getExistingArrayAttributeIndices()
        if target_index[0] in weights_list_array:
            weights_plug = weights_list_plug.elementByLogicalIndex(target_index[0]).child(0)
            weights_array = weights_plug.getExistingArrayAttributeIndices()
            for index in weights_array:
                if index in members_ID:
                    weights_map.setdefault(index, weights_plug.elementByLogicalIndex(index).asFloat())
                    members_ID_not_listed.remove(index)
        for index in members_ID_not_listed:
            weights_map.setdefault(index, 1)

        return weights_map

    def get_blendShape_weights_legacy(self, target=None, deformer_name=None, ID=None):
        # preliminary operations
        weights_map = {}
        target_path = None
        selected_deformer = None
        vtx_components = []
        members_ID = []
        non_members_ID = []

        # input validation
        if target != None:
            target_shape = self.get_target_shape(target)
            if target_shape != None:
                if self.is_a_mesh(target_shape):
                    target_path = self.get_dag_path(target_shape)
        else:
            if self.input_mesh:
                target_path = self.get_dag_path(self.input_mesh)
        if target_path is None:
            raise ValueError('Select a valid mesh')

        if deformer_name != None:
            if pmc.objExists(deformer_name):
                if pmc.objectType(deformer_name) in self.valid_deformers:
                    selected_deformer = deformer_name
        else:
            deformers_list_entry = pmc.textScrollList(self.deformersList, query=True, selectItem=True)
            if deformers_list_entry:
                selected_deformer = deformers_list_entry[0].split(' - ')[1]
        if selected_deformer is None:
            raise ValueError('Select a valid deformer')
        deformer_node = self.get_depend_node(selected_deformer)
        deformer_fnSet = om.MFnDependencyNode(deformer_node)
        target_index = self.find_target_index(deformer_node, target_path)
        if not target_index:
            raise ValueError('"{Name1}" does not affect "{Name2}"'.format(Name1=selected_deformer, Name2=target_path))

        sel_list = om.MSelectionList()
        sel_list.add(oma.MFnGeometryFilter(deformer_node).deformerSet)
        deformer_set = om.MFnDependencyNode(sel_list.getDependNode(0)).name()
        if ID != None:
            target_vtx_num = om.MFnMesh(target_path).numVertices
            target_vtx_ID = range(0, target_vtx_num)
            if max(ID) > target_vtx_num:
                raise ValueError(
                    'Mesh "{Name}" does not contain selected vertices: vertex ID out of range'.format(Name=target_path))
            vtx_comp_fnSet = om.MFnSingleIndexedComponent()
            vtx_comp = vtx_comp_fnSet.create(om.MFn.kMeshVertComponent)
            vtx_comp_fnSet.addElements(ID)
            vtx_components.append((target_path, vtx_comp))
        else:
            selection = om.MGlobal.getActiveSelectionList()
            selection_iterator = om.MItSelectionList(selection, om.MFn.kMeshVertComponent)
            if selection_iterator.isDone():
                raise ValueError('Select the vertices to read deformer weights from')
            while not selection_iterator.isDone():
                current_component = selection_iterator.getComponent()
                if not current_component[0] == target_path:
                    raise ValueError('Selected vertices do not belong to mesh "{Name}"'.format(Name=target_path))
                vtx_components.append((current_component[0], current_component[1]))
                next(selection_iterator)
        for comp_item in vtx_components:
            vtx_iterator = om.MItMeshVertex(comp_item[0], comp_item[1])
            while not vtx_iterator.isDone():
                vtx_name = '{Name1}.vtx[{Name2}]'.format(Name1=str(target_path), Name2=str(vtx_iterator.index()))
                if pmc.sets(deformer_set, isMember=vtx_name):
                    members_ID.append(vtx_iterator.index())
                else:
                    non_members_ID.append(vtx_iterator.index())
                next(vtx_iterator)

        # get weights
        members_ID_not_listed = members_ID
        input_target_plug = deformer_fnSet.findPlug('inputTarget', True)
        input_target_array = input_target_plug.getExistingArrayAttributeIndices()
        if target_index[0] in input_target_array:
            weights_plug = input_target_plug.elementByLogicalIndex(target_index[0]).child(1)
            weights_array = weights_plug.getExistingArrayAttributeIndices()
            for index in weights_array:
                if index in members_ID:
                    weights_map.setdefault(index, weights_plug.elementByLogicalIndex(index).asFloat())
                    members_ID_not_listed.remove(index)
        for index in members_ID_not_listed:
            weights_map.setdefault(index, 1)
        for index in non_members_ID:
            weights_map.setdefault(index, 0)

        return weights_map

    def get_blendShape_weights(self, target=None, deformer_name=None, ID=None):
        # preliminary operations
        weights_map = {}
        target_path = None
        selected_deformer = None
        vtx_components = []
        members_ID = []
        non_members_ID = []

        # input validation
        if target != None:
            target_shape = self.get_target_shape(target)
            if target_shape != None:
                if self.is_a_mesh(target_shape):
                    target_path = self.get_dag_path(target_shape)
        else:
            if self.input_mesh:
                target_path = self.get_dag_path(self.input_mesh)
        if target_path is None:
            raise ValueError('Select a valid mesh')

        if deformer_name != None:
            if pmc.objExists(deformer_name):
                if pmc.objectType(deformer_name) in self.valid_deformers:
                    selected_deformer = deformer_name
        else:
            deformers_list_entry = pmc.textScrollList(self.deformersList, query=True, selectItem=True)
            if deformers_list_entry:
                selected_deformer = deformers_list_entry[0].split(' - ')[1]
        if selected_deformer is None:
            raise ValueError('Select a valid deformer')
        deformer_node = self.get_depend_node(selected_deformer)
        deformer_fnSet = om.MFnDependencyNode(deformer_node)
        target_index = self.find_target_index(deformer_node, target_path)
        if not target_index:
            raise ValueError('"{Name1}" does not affect "{Name2}"'.format(Name1=selected_deformer, Name2=target_path))

        deformer_set = oma.MFnGeometryFilter(deformer_node).deformerSet
        deformer_set_members = om.MFnSet(deformer_set).getMembers(flatten=True)
        if ID != None:
            target_vtx_num = om.MFnMesh(target_path).numVertices
            target_vtx_ID = range(0, target_vtx_num)
            if max(ID) > target_vtx_num:
                raise ValueError(
                    'Mesh "{Name}" does not contain selected vertices: vertex ID out of range'.format(Name=target_path))
            vtx_comp_fnSet = om.MFnSingleIndexedComponent()
            vtx_comp = vtx_comp_fnSet.create(om.MFn.kMeshVertComponent)
            vtx_comp_fnSet.addElements(ID)
            vtx_components.append((target_path, vtx_comp))
        else:
            selection = om.MGlobal.getActiveSelectionList()
            selection_iterator = om.MItSelectionList(selection, om.MFn.kMeshVertComponent)
            if selection_iterator.isDone():
                raise ValueError('Select the vertices to read deformer weights from')
            while not selection_iterator.isDone():
                current_component = selection_iterator.getComponent()
                if not current_component[0] == target_path:
                    raise ValueError('Selected vertices do not belong to mesh "{Name}"'.format(Name=target_path))
                vtx_components.append((current_component[0], current_component[1]))
                next(selection_iterator)
        for comp_item in vtx_components:
            vtx_iterator = om.MItMeshVertex(comp_item[0], comp_item[1])
            while not vtx_iterator.isDone():
                current_vtx_comp = vtx_iterator.currentItem()
                if deformer_set_members.hasItem((comp_item[0], current_vtx_comp)):
                    members_ID.append(vtx_iterator.index())
                else:
                    non_members_ID.append(vtx_iterator.index())
                next(vtx_iterator)

        # get weights
        members_ID_not_listed = members_ID
        input_target_plug = deformer_fnSet.findPlug('inputTarget', True)
        input_target_array = input_target_plug.getExistingArrayAttributeIndices()
        if target_index[0] in input_target_array:
            weights_plug = input_target_plug.elementByLogicalIndex(target_index[0]).child(1)
            weights_array = weights_plug.getExistingArrayAttributeIndices()
            for index in weights_array:
                if index in members_ID:
                    weights_map.setdefault(index, weights_plug.elementByLogicalIndex(index).asFloat())
                    members_ID_not_listed.remove(index)
        for index in members_ID_not_listed:
            weights_map.setdefault(index, 1)
        for index in non_members_ID:
            weights_map.setdefault(index, 0)

        return weights_map

    def get_blendShape_weights_future(self, target=None, deformer_name=None, ID=None):
        # preliminary operations
        weights_map = {}
        target_path = None
        selected_deformer = None
        vtx_components = []
        members_ID = []

        # input validation
        if target != None:
            target_shape = self.get_target_shape(target)
            if target_shape != None:
                if self.is_a_mesh(target_shape):
                    target_path = self.get_dag_path(target_shape)
        else:
            if self.input_mesh:
                target_path = self.get_dag_path(self.input_mesh)
        if target_path is None:
            raise ValueError('Select a valid mesh')

        if deformer_name != None:
            if pmc.objExists(deformer_name):
                if pmc.objectType(deformer_name) in self.valid_deformers:
                    selected_deformer = deformer_name
        else:
            deformers_list_entry = pmc.textScrollList(self.deformersList, query=True, selectItem=True)
            if deformers_list_entry:
                selected_deformer = deformers_list_entry[0].split(' - ')[1]
        if selected_deformer is None:
            raise ValueError('Select a valid deformer')
        deformer_node = self.get_depend_node(selected_deformer)
        deformer_fnSet = om.MFnDependencyNode(deformer_node)
        target_index = self.find_target_index(deformer_node, target_path)
        if not target_index:
            raise ValueError('"{Name1}" does not affect "{Name2}"'.format(Name1=selected_deformer, Name2=target_path))

        if ID != None:
            target_vtx_num = om.MFnMesh(target_path).numVertices
            target_vtx_ID = range(0, target_vtx_num)
            if max(ID) > target_vtx_num:
                raise ValueError(
                    'Mesh "{Name}" does not contain selected vertices: vertex ID out of range'.format(Name=target_path))
            vtx_comp_fnSet = om.MFnSingleIndexedComponent()
            vtx_comp = vtx_comp_fnSet.create(om.MFn.kMeshVertComponent)
            vtx_comp_fnSet.addElements(ID)
            vtx_components.append((target_path, vtx_comp))
        else:
            selection = om.MGlobal.getActiveSelectionList()
            selection_iterator = om.MItSelectionList(selection, om.MFn.kMeshVertComponent)
            if selection_iterator.isDone():
                raise ValueError('Select the vertices to read deformer weights from')
            while not selection_iterator.isDone():
                current_component = selection_iterator.getComponent()
                if not current_component[0] == target_path:
                    raise ValueError('Selected vertices do not belong to mesh "{Name}"'.format(Name=target_path))
                vtx_components.append((current_component[0], current_component[1]))
                next(selection_iterator)
        for comp_item in vtx_components:
            vtx_iterator = om.MItMeshVertex(comp_item[0], comp_item[1])
            while not vtx_iterator.isDone():
                members_ID.append(vtx_iterator.index())
                next(vtx_iterator)

        # get weights
        members_ID_not_listed = members_ID
        input_target_plug = deformer_fnSet.findPlug('inputTarget', True)
        input_target_array = input_target_plug.getExistingArrayAttributeIndices()
        if target_index[0] in input_target_array:
            weights_plug = input_target_plug.elementByLogicalIndex(target_index[0]).child(1)
            weights_array = weights_plug.getExistingArrayAttributeIndices()
            for index in weights_array:
                if index in members_ID:
                    weights_map.setdefault(index, weights_plug.elementByLogicalIndex(index).asFloat())
                    members_ID_not_listed.remove(index)
        for index in members_ID_not_listed:
            weights_map.setdefault(index, 1)

        return weights_map

    def set_deformer_weights(self, weights_map, import_deformer, target=None, deformer_name=None, ID=None):
        # preliminary operations
        target_path = None
        selected_deformer = None
        vtx_ID = []
        status = 'failure'

        # input validation
        if target != None:
            target_shape = self.get_target_shape(target)
            if target_shape != None:
                if self.is_a_mesh(target_shape):
                    target_path = self.get_dag_path(target_shape)
        else:
            if self.input_mesh:
                target_path = self.get_dag_path(self.input_mesh)
        if target_path is None:
            raise ValueError('Select a valid mesh')

        if deformer_name != None:
            if pmc.objExists(deformer_name):
                if pmc.objectType(deformer_name) in self.valid_deformers:
                    selected_deformer = deformer_name
        else:
            deformers_list_entry = pmc.textScrollList(self.deformersList, query=True, selectItem=True)
            if deformers_list_entry:
                selected_deformer = deformers_list_entry[0].split(' - ')[1]
        if selected_deformer is None:
            raise ValueError('Select a valid deformer')
        deformer_node = self.get_depend_node(selected_deformer)
        deformer_fnSet = om.MFnDependencyNode(deformer_node)
        target_index = self.find_target_index(deformer_node, target_path)
        if not target_index:
            raise ValueError('"{Name1}" does not affect "{Name2}"'.format(Name1=selected_deformer, Name2=target_path))
        if not (selected_deformer == import_deformer):
            answer = pmc.confirmDialog(title='Confirm',
                                       message='You are trying to import weights of "{Name1}" deformer into "{Name2}" deformer. Proceed anyway?'.format(
                                           Name1=import_deformer, Name2=selected_deformer), button=['Yes', 'No'],
                                       defaultButton='Yes', cancelButton='No', dismissString='No')
            if answer == 'No':
                status = 'aborted'
                return status

        if ID != None:
            target_vtx_num = om.MFnMesh(target_path).numVertices
            target_vtx_ID = range(0, target_vtx_num)
            if max(ID) > target_vtx_num:
                raise ValueError(
                    'Mesh "{Name}" does not contain selected vertices: vertex ID out of range'.format(Name=target_path))
            vtx_ID = ID
        else:
            selection = om.MGlobal.getActiveSelectionList()
            selection_iterator = om.MItSelectionList(selection, om.MFn.kMeshVertComponent)
            if selection_iterator.isDone():
                raise ValueError('Select the vertices to set deformer weights to')
            while not selection_iterator.isDone():
                current_component = selection_iterator.getComponent()
                if not current_component[0] == target_path:
                    raise ValueError('Selected vertices do not belong to mesh "{Name}"'.format(Name=target_path))
                vtx_iterator = om.MItMeshVertex(current_component[0], current_component[1])
                while not vtx_iterator.isDone():
                    vtx_ID.append(vtx_iterator.index())
                    next(vtx_iterator)
                next(selection_iterator)

        # set weights
        weights_list_plug = deformer_fnSet.findPlug('weightList', True)
        weights_plug = weights_list_plug.elementByLogicalIndex(target_index[0]).child(0)
        if weights_map:
            weights_map_items = [(int(key_entry), weights_map[key_entry]) for key_entry in weights_map.keys()]
            weights_map_valid_items = [item for item in weights_map_items if item[0] in vtx_ID]
            if weights_map_valid_items:
                for item in weights_map_valid_items:
                    weights_plug.elementByLogicalIndex(item[0]).setFloat(item[1])
                status = 'complete'

        return status

    def set_blendShape_weights(self, weights_map, import_deformer, target=None, deformer_name=None, ID=None):
        # preliminary operations
        target_path = None
        selected_deformer = None
        vtx_ID = []
        status = 'failure'

        # input validation
        if target != None:
            target_shape = self.get_target_shape(target)
            if target_shape != None:
                if self.is_a_mesh(target_shape):
                    target_path = self.get_dag_path(target_shape)
        else:
            if self.input_mesh:
                target_path = self.get_dag_path(self.input_mesh)
        if target_path is None:
            raise ValueError('Select a valid mesh')

        if deformer_name != None:
            if pmc.objExists(deformer_name):
                if pmc.objectType(deformer_name) in self.valid_deformers:
                    selected_deformer = deformer_name
        else:
            deformers_list_entry = pmc.textScrollList(self.deformersList, query=True, selectItem=True)
            if deformers_list_entry:
                selected_deformer = deformers_list_entry[0].split(' - ')[1]
        if selected_deformer is None:
            raise ValueError('Select a valid deformer')
        deformer_node = self.get_depend_node(selected_deformer)
        deformer_fnSet = om.MFnDependencyNode(deformer_node)
        target_index = self.find_target_index(deformer_node, target_path)
        if not target_index:
            raise ValueError('"{Name1}" does not affect "{Name2}"'.format(Name1=selected_deformer, Name2=target_path))
        if not (selected_deformer == import_deformer):
            answer = pmc.confirmDialog(title='Confirm',
                                       message='You are trying to import weights of "{Name1}" deformer into "{Name2}" deformer. Proceed anyway?'.format(
                                           Name1=import_deformer, Name2=selected_deformer), button=['Yes', 'No'],
                                       defaultButton='Yes', cancelButton='No', dismissString='No')
            if answer == 'No':
                status = 'aborted'
                return status

        if ID != None:
            target_vtx_num = om.MFnMesh(target_path).numVertices
            target_vtx_ID = range(0, target_vtx_num)
            if max(ID) > target_vtx_num:
                raise ValueError(
                    'Mesh "{Name}" does not contain selected vertices: vertex ID out of range'.format(Name=target_path))
            vtx_ID = ID
        else:
            selection = om.MGlobal.getActiveSelectionList()
            selection_iterator = om.MItSelectionList(selection, om.MFn.kMeshVertComponent)
            if selection_iterator.isDone():
                raise ValueError('Select the vertices to set deformer weights to')
            while not selection_iterator.isDone():
                current_component = selection_iterator.getComponent()
                if not current_component[0] == target_path:
                    raise ValueError('Selected vertices do not belong to mesh "{Name}"'.format(Name=target_path))
                vtx_iterator = om.MItMeshVertex(current_component[0], current_component[1])
                while not vtx_iterator.isDone():
                    vtx_ID.append(vtx_iterator.index())
                    next(vtx_iterator)
                next(selection_iterator)

        # set weights
        input_target_plug = deformer_fnSet.findPlug('inputTarget', True)
        weights_plug = input_target_plug.elementByLogicalIndex(target_index[0]).child(1)
        if weights_map:
            weights_map_items = [(int(key_entry), weights_map[key_entry]) for key_entry in weights_map.keys()]
            weights_map_valid_items = [item for item in weights_map_items if item[0] in vtx_ID]
            if weights_map_valid_items:
                for item in weights_map_valid_items:
                    weights_plug.elementByLogicalIndex(item[0]).setFloat(item[1])
                status = 'complete'

        return status

    def get_vertices_position(self):
        # preliminary operations
        input_mesh_path = self.get_dag_path(self.input_mesh)
        coordinates_table = {}

        # input validation
        components_selection = om.MGlobal.getActiveSelectionList()
        components_iterator = om.MItSelectionList(components_selection, om.MFn.kMeshVertComponent)
        if components_iterator.isDone():
            raise ValueError('Select the mesh vertices to access their position')

        # read vertices position
        while not components_iterator.isDone():
            current_component = components_iterator.getComponent()
            vertices_iterator = om.MItMeshVertex(current_component[0], current_component[1])
            if not (current_component[0].extendToShape(0) == input_mesh_path):
                pmc.warning('Skipping component: the selected vertices do not belong to mesh "{Name}"'.format(
                    Name=input_mesh_path))

            while not vertices_iterator.isDone():
                vtx_ID = vertices_iterator.index()
                vtx_position = vertices_iterator.position(om.MSpace.kWorld)
                coordinates_table.setdefault(vtx_ID, [vtx_position.x, vtx_position.y, vtx_position.z])
                next(vertices_iterator)
            next(components_iterator)

        return coordinates_table

    def find_closest_vertices(self, source_point, target_points_map, tolerance_val):
        # build bounding box
        radius_vector = om.MVector([tolerance_val, tolerance_val, tolerance_val])
        BB_min = source_point - radius_vector
        BB_max = source_point + radius_vector
        bounding_box = om.MBoundingBox(BB_min, BB_max)

        # find closest vertices
        closest_vertices = {}
        target_items = target_points_map.items()
        for item in target_items:
            current_point = om.MPoint(item[1])
            if bounding_box.contains(current_point):
                distance = source_point.distanceTo(current_point)
                if not distance > tolerance_val:
                    closest_vertices.setdefault(item[0], distance)

        return closest_vertices

    def average_weights_map(self, coordinates_table, weights_map):
        # preliminary operations
        avg_weights_map = {}
        vtx_components = []

        # input validation
        input_tolerance = pmc.textFieldGrp(self.loadTolerance, query=True, text=True)
        try:
            tolerance_val = float(input_tolerance)
            if tolerance_val <= 0:
                raise
        except:
            tolerance_val = 0.1

        if not self.input_mesh:
            raise ValueError('Select a valid mesh')
        target_path = self.get_dag_path(self.input_mesh)

        points_table = {item[0]: om.MPoint(item[1]) for item in coordinates_table.items()}

        selection = om.MGlobal.getActiveSelectionList()
        selection_iterator = om.MItSelectionList(selection, om.MFn.kMeshVertComponent)
        while not selection_iterator.isDone():
            current_component = selection_iterator.getComponent()
            if not current_component[0] == target_path:
                raise ValueError('Selected vertices do not belong to mesh "{Name}"'.format(Name=target_path))
            vtx_components.append((current_component[0], current_component[1]))
            next(selection_iterator)
        if not vtx_components:
            raise ValueError('Select the mesh vertices to calculate their average deformer weights')

        # calculate average weights (average weighted by e^-distance)
        comp_num = len(vtx_components)
        for comp_index, comp_item in enumerate(vtx_components):
            vtx_iterator = om.MItMeshVertex(comp_item[0], comp_item[1])
            vtx_num = vtx_iterator.count()
            comp_step = comp_index + 1
            pBar_title = '...Step {Name1} of {Name2}...'.format(Name1=str(comp_step), Name2=str(comp_num))
            pBar_win_name = 'PBwindow'
            if pmc.window(pBar_win_name, exists=True):
                pmc.deleteUI(pBar_win_name)
            pmc.window(pBar_win_name, title=pBar_title, sizeable=False, widthHeight=[350, 50])
            pBar_layout = pmc.formLayout(numberOfDivisions=100)
            pBar_control = pmc.progressBar(parent=pBar_layout, width=330, height=30, minValue=0, maxValue=vtx_num,
                                           progress=0)
            pmc.formLayout(pBar_layout, edit=True, attachForm=([pBar_control, 'left', 10], [pBar_control, 'top', 10]))
            pmc.showWindow(pBar_win_name)

            while not vtx_iterator.isDone():
                vtx_index = vtx_iterator.index()
                vtx_point = vtx_iterator.position(om.MSpace.kWorld)
                closest_vtx = self.find_closest_vertices(vtx_point, coordinates_table, tolerance_val)
                avg_weight = 0
                if closest_vtx:
                    num_elements = [weights_map[index] * math.exp(-(closest_vtx[index])) for index in
                                    closest_vtx.keys()]
                    den_elements = [math.exp(-(closest_vtx[index])) for index in closest_vtx.keys()]
                    avg_weight = sum(num_elements) / sum(den_elements)
                avg_weights_map.setdefault(str(vtx_index), avg_weight)
                pmc.progressBar(pBar_control, edit=True, step=1)
                next(vtx_iterator)
            pmc.deleteUI(pBar_win_name)

            return avg_weights_map

    def barycenter(self, vec_A, vec_B, vec_C, vec_P, tolerance_val=0.001):
        barycentric_coor = [0, 0, 0]
        vec_AB = vec_B - vec_A
        vec_AC = vec_C - vec_A
        vec_BC = vec_C - vec_B
        vec_CA = vec_A - vec_C
        vec_AP = vec_P - vec_A
        vec_BP = vec_P - vec_B
        vec_CP = vec_P - vec_C
        vec_normal = vec_AB ^ vec_AC
        factor = 1 / (vec_normal * vec_normal)

        bar_u = (vec_BC ^ vec_BP) * vec_normal * factor
        if bar_u < -tolerance_val:
            return barycentric_coor

        bar_v = (vec_CA ^ vec_CP) * vec_normal * factor
        if bar_v < -tolerance_val:
            return barycentric_coor

        bar_w = (vec_AB ^ vec_AP) * vec_normal * factor
        if bar_w < -tolerance_val:
            return barycentric_coor

        barycentric_coor = [bar_u, bar_v, bar_w]
        return barycentric_coor

    def mirror_routine_legacy(self):
        # input validation
        if not self.input_mesh:
            raise ValueError('Select a valid mesh')
        target_path = self.get_dag_path(self.input_mesh)
        target_fnSet = om.MFnMesh(target_path)

        deformers_list_entry = pmc.textScrollList(self.deformersList, query=True, selectItem=True)
        if not deformers_list_entry:
            raise ValueError('Select a valid deformer')
        deformer_type = deformers_list_entry[0].split(' - ')[0]
        selected_deformer = deformers_list_entry[0].split(' - ')[1]
        deformer_node = self.get_depend_node(selected_deformer)

        sym_dir = pmc.radioButtonGrp(self.symmetryDirection, query=True, select=True)
        sym_plane = pmc.radioButtonGrp(self.symmetryPlane, query=True, select=True)
        sym_axis = self.symmetry_axis[sym_plane]
        mirror_transformation = om.MMatrix().setElement(sym_axis, sym_axis, -1)

        # gather data
        routine_choice = 'future'
        try:
            deformer_set = oma.MFnGeometryFilter(deformer_node).deformerSet
            routine_choice = 'legacy'
        except:
            pass
        try:
            deformer_set_members = om.MFnSet(deformer_set).getMemebrs(faltten=True)
            routine_choice = 'standard'
        except:
            pass
        target_vtx_num = target_fnSet.numVertices
        overall_vtx_ID = [index for index in range(0, target_vtx_num)]
        if deformer_type == 'blendShape':
            if routine_choice == 'legacy':
                weights_map = self.get_blendShape_weights_legacy(ID=overall_vtx_ID)
            elif routine_choice == 'standard':
                weights_map = self.get_blendShape_weights(ID=overall_vtx_ID)
            elif routine_choice == 'future':
                weights_map = self.get_blendShape_weights_future(ID=overall_vtx_ID)
        else:
            if routine_choice == 'legacy':
                weights_map = self.get_deformer_weights_legacy(ID=overall_vtx_ID)
            elif routine_choice == 'standard':
                weights_map = self.get_deformer_weights(ID=overall_vtx_ID)
            elif routine_choice == 'future':
                weights_map = self.get_deformer_weights_future(ID=overall_vtx_ID)

        coordinates_table = self.get_vertices_position()
        vtx_ID = [index for index in coordinates_table.keys()]
        if sym_dir == 1:  # from positive to negative
            vtx_to_mirror = [index for index in vtx_ID if coordinates_table[index][sym_axis] < 0]
        elif sym_dir == 2:  # from negative to positive
            vtx_to_mirror = [index for index in vtx_ID if coordinates_table[index][sym_axis] > 0]
        vtx_to_mirror_num = len(vtx_to_mirror)

        mirror_weights_map = {index: weights_map[index] for index in vtx_ID}

        output_message = {}
        output_message.setdefault('complete', 'Mirror operation ended successfully \n')
        output_message.setdefault('failure', 'No weights were set: stored vertices IDs do not match with selection \n')
        output_message.setdefault('aborted', 'Mirror operation aborted \n')

        pBar_title = '...Mirroring weights...'
        pBar_win_name = 'PBwindow'
        if pmc.window(pBar_win_name, exists=True):
            pmc.deleteUI(pBar_win_name)
        pmc.window(pBar_win_name, title=pBar_title, sizeable=False, widthHeight=[350, 50])
        pBar_layout = pmc.formLayout(numberOfDivisions=100)
        pBar_control = pmc.progressBar(parent=pBar_layout, width=330, height=30, minValue=0, maxValue=vtx_to_mirror_num,
                                       progress=0)
        pmc.formLayout(pBar_layout, edit=True, attachForm=([pBar_control, 'left', 10], [pBar_control, 'top', 10]))
        pmc.showWindow(pBar_win_name)

        # mirror weights
        for id in vtx_to_mirror:
            current_point = om.MPoint(coordinates_table[id])
            mirror_point = current_point * mirror_transformation
            closest_point = target_fnSet.getClosestPoint(mirror_point, om.MSpace.kWorld)

            if closest_point:
                face_component_fnSet = om.MFnSingleIndexedComponent()
                face_component = face_component_fnSet.create(om.MFn.kMeshPolygonComponent)
                face_component_fnSet.addElement(closest_point[1])
                faces_iterator = om.MItMeshPolygon(target_path, face_component)
                face_triangles = faces_iterator.getTriangles(om.MSpace.kWorld)
                tri_num = len(face_triangles)
                for counter in range(0, tri_num):
                    vec_A = om.MVector(face_triangles[0][0 + counter * 3])
                    vec_B = om.MVector(face_triangles[0][1 + counter * 3])
                    vec_C = om.MVector(face_triangles[0][2 + counter * 3])
                    vec_P = om.MVector(closest_point[0])
                    bar_coor = self.barycenter(vec_A, vec_B, vec_C, vec_P)
                    if max(bar_coor) > 0:
                        break

                bar_weight = bar_coor[0] * weights_map[face_triangles[1][0 + counter * 3]] + bar_coor[1] * weights_map[
                    face_triangles[1][1 + counter * 3]] + bar_coor[2] * weights_map[face_triangles[1][2 + counter * 3]]
                mirror_weights_map[id] = bar_weight

            pmc.progressBar(pBar_control, edit=True, step=1)

        pmc.deleteUI(pBar_win_name)

        if deformer_type == 'blendShape':
            status = self.set_blendShape_weights(mirror_weights_map, selected_deformer)
        else:
            status = self.set_deformer_weights(mirror_weights_map, selected_deformer)
        sys.stdout.write(output_message[status])
        sys.stdout.flush()

    def mirror_routine(self):
        # input validation
        if not self.input_mesh:
            raise ValueError('Select a valid mesh')
        target_path = self.get_dag_path(self.input_mesh)
        target_fnSet = om.MFnMesh(target_path)
        target_node = target_path.node()
        target_matrix = target_path.inclusiveMatrixInverse()
        target_intersector = om.MMeshIntersector()
        target_intersector.create(target_node, target_matrix)

        deformers_list_entry = pmc.textScrollList(self.deformersList, query=True, selectItem=True)
        if not deformers_list_entry:
            raise ValueError('Select a valid deformer')
        deformer_type = deformers_list_entry[0].split(' - ')[0]
        selected_deformer = deformers_list_entry[0].split(' - ')[1]
        deformer_node = self.get_depend_node(selected_deformer)

        sym_dir = pmc.radioButtonGrp(self.symmetryDirection, query=True, select=True)
        sym_plane = pmc.radioButtonGrp(self.symmetryPlane, query=True, select=True)
        sym_axis = self.symmetry_axis[sym_plane]
        mirror_transformation = om.MMatrix().setElement(sym_axis, sym_axis, -1)

        # gather data
        routine_choice = 'future'
        try:
            deformer_set = oma.MFnGeometryFilter(deformer_node).deformerSet
            routine_choice = 'legacy'
        except:
            pass
        try:
            deformer_set_members = om.MFnSet(deformer_set).getMemebrs(faltten=True)
            routine_choice = 'standard'
        except:
            pass
        target_vtx_num = target_fnSet.numVertices
        overall_vtx_ID = [index for index in range(0, target_vtx_num)]
        if deformer_type == 'blendShape':
            if routine_choice == 'legacy':
                weights_map = self.get_blendShape_weights_legacy(ID=overall_vtx_ID)
            elif routine_choice == 'standard':
                weights_map = self.get_blendShape_weights(ID=overall_vtx_ID)
            elif routine_choice == 'future':
                weights_map = self.get_blendShape_weights_future(ID=overall_vtx_ID)
        else:
            if routine_choice == 'legacy':
                weights_map = self.get_deformer_weights_legacy(ID=overall_vtx_ID)
            elif routine_choice == 'standard':
                weights_map = self.get_deformer_weights(ID=overall_vtx_ID)
            elif routine_choice == 'future':
                weights_map = self.get_deformer_weights_future(ID=overall_vtx_ID)

        coordinates_table = self.get_vertices_position()
        vtx_ID = [index for index in coordinates_table.keys()]
        if sym_dir == 1:  # from positive to negative
            vtx_to_mirror = [index for index in vtx_ID if coordinates_table[index][sym_axis] < 0]
        elif sym_dir == 2:  # from negative to positive
            vtx_to_mirror = [index for index in vtx_ID if coordinates_table[index][sym_axis] > 0]
        vtx_to_mirror_num = len(vtx_to_mirror)

        mirror_weights_map = {index: weights_map[index] for index in vtx_ID}

        output_message = {}
        output_message.setdefault('complete', 'Mirror operation ended successfully \n')
        output_message.setdefault('failure', 'No weights were set: stored vertices IDs do not match with selection \n')
        output_message.setdefault('aborted', 'Mirror operation aborted \n')

        pBar_title = '...Mirroring weights...'
        pBar_win_name = 'PBwindow'
        if pmc.window(pBar_win_name, exists=True):
            pmc.deleteUI(pBar_win_name)
        pmc.window(pBar_win_name, title=pBar_title, sizeable=False, widthHeight=[350, 50])
        pBar_layout = pmc.formLayout(numberOfDivisions=100)
        pBar_control = pmc.progressBar(parent=pBar_layout, width=330, height=30, minValue=0, maxValue=vtx_to_mirror_num,
                                       progress=0)
        pmc.formLayout(pBar_layout, edit=True, attachForm=([pBar_control, 'left', 10], [pBar_control, 'top', 10]))
        pmc.showWindow(pBar_win_name)

        # mirror weights
        for id in vtx_to_mirror:
            current_point = om.MPoint(coordinates_table[id])
            mirror_point = current_point * mirror_transformation
            closest_point = target_intersector.getClosestPoint(mirror_point)

            if closest_point:
                bar_coor = closest_point.barycentricCoords
                intersec_face = closest_point.face
                intersec_tri = closest_point.triangle

                face_component_fnSet = om.MFnSingleIndexedComponent()
                face_component = face_component_fnSet.create(om.MFn.kMeshPolygonComponent)
                face_component_fnSet.addElement(intersec_face)
                faces_iterator = om.MItMeshPolygon(target_path, face_component)
                bar_vtx = faces_iterator.getTriangle(intersec_tri)
                bar_vtx_ID = bar_vtx[1]

                bar_weight = bar_coor[0] * weights_map[bar_vtx_ID[0]] + bar_coor[1] * weights_map[bar_vtx_ID[1]] + (
                            1 - bar_coor[0] - bar_coor[1]) * weights_map[bar_vtx_ID[2]]
                mirror_weights_map[id] = bar_weight

            pmc.progressBar(pBar_control, edit=True, step=1)

        pmc.deleteUI(pBar_win_name)

        if deformer_type == 'blendShape':
            status = self.set_blendShape_weights(mirror_weights_map, selected_deformer)
        else:
            status = self.set_deformer_weights(mirror_weights_map, selected_deformer)
        sys.stdout.write(output_message[status])
        sys.stdout.flush()

    def flip_routine_legacy(self):
        # input validation
        if not self.input_mesh:
            raise ValueError('Select a valid mesh')
        target_path = self.get_dag_path(self.input_mesh)
        target_fnSet = om.MFnMesh(target_path)

        deformers_list_entry = pmc.textScrollList(self.deformersList, query=True, selectItem=True)
        if not deformers_list_entry:
            raise ValueError('Select a valid deformer')
        deformer_type = deformers_list_entry[0].split(' - ')[0]
        selected_deformer = deformers_list_entry[0].split(' - ')[1]
        deformer_node = self.get_depend_node(selected_deformer)

        sym_plane = pmc.radioButtonGrp(self.symmetryPlane, query=True, select=True)
        sym_axis = self.symmetry_axis[sym_plane]
        mirror_transformation = om.MMatrix().setElement(sym_axis, sym_axis, -1)

        # gather data
        routine_choice = 'future'
        try:
            deformer_set = oma.MFnGeometryFilter(deformer_node).deformerSet
            routine_choice = 'legacy'
        except:
            pass
        try:
            deformer_set_members = om.MFnSet(deformer_set).getMemebrs(faltten=True)
            routine_choice = 'standard'
        except:
            pass
        target_vtx_num = target_fnSet.numVertices
        overall_vtx_ID = [index for index in range(0, target_vtx_num)]
        if deformer_type == 'blendShape':
            if routine_choice == 'legacy':
                weights_map = self.get_blendShape_weights_legacy(ID=overall_vtx_ID)
            elif routine_choice == 'standard':
                weights_map = self.get_blendShape_weights(ID=overall_vtx_ID)
            elif routine_choice == 'future':
                weights_map = self.get_blendShape_weights_future(ID=overall_vtx_ID)
        else:
            if routine_choice == 'legacy':
                weights_map = self.get_deformer_weights_legacy(ID=overall_vtx_ID)
            elif routine_choice == 'standard':
                weights_map = self.get_deformer_weights(ID=overall_vtx_ID)
            elif routine_choice == 'future':
                weights_map = self.get_deformer_weights_future(ID=overall_vtx_ID)

        coordinates_table = self.get_vertices_position()
        vtx_ID = [index for index in coordinates_table.keys()]
        vtx_num = len(vtx_ID)

        flip_weights_map = {index: weights_map[index] for index in vtx_ID}

        output_message = {}
        output_message.setdefault('complete', 'Flip operation ended successfully \n')
        output_message.setdefault('failure', 'No weights were set: stored vertices IDs do not match with selection \n')
        output_message.setdefault('aborted', 'Flip operation aborted \n')

        pBar_title = '...Flipping weights...'
        pBar_win_name = 'PBwindow'
        if pmc.window(pBar_win_name, exists=True):
            pmc.deleteUI(pBar_win_name)
        pmc.window(pBar_win_name, title=pBar_title, sizeable=False, widthHeight=[350, 50])
        pBar_layout = pmc.formLayout(numberOfDivisions=100)
        pBar_control = pmc.progressBar(parent=pBar_layout, width=330, height=30, minValue=0, maxValue=vtx_num,
                                       progress=0)
        pmc.formLayout(pBar_layout, edit=True, attachForm=([pBar_control, 'left', 10], [pBar_control, 'top', 10]))
        pmc.showWindow(pBar_win_name)

        # flipping weights
        for id in vtx_ID:
            current_point = om.MPoint(coordinates_table[id])
            mirror_point = current_point * mirror_transformation
            closest_point = target_fnSet.getClosestPoint(mirror_point, om.MSpace.kWorld)

            if closest_point:
                face_component_fnSet = om.MFnSingleIndexedComponent()
                face_component = face_component_fnSet.create(om.MFn.kMeshPolygonComponent)
                face_component_fnSet.addElement(closest_point[1])
                faces_iterator = om.MItMeshPolygon(target_path, face_component)
                face_triangles = faces_iterator.getTriangles(om.MSpace.kWorld)
                tri_num = len(face_triangles)
                for counter in range(0, tri_num):
                    vec_A = om.MVector(face_triangles[0][0 + counter * 3])
                    vec_B = om.MVector(face_triangles[0][1 + counter * 3])
                    vec_C = om.MVector(face_triangles[0][2 + counter * 3])
                    vec_P = om.MVector(closest_point[0])
                    bar_coor = self.barycenter(vec_A, vec_B, vec_C, vec_P)
                    if max(bar_coor) > 0:
                        break

                bar_weight = bar_coor[0] * weights_map[face_triangles[1][0 + counter * 3]] + bar_coor[1] * weights_map[
                    face_triangles[1][1 + counter * 3]] + bar_coor[2] * weights_map[face_triangles[1][2 + counter * 3]]
                flip_weights_map[id] = bar_weight

            pmc.progressBar(pBar_control, edit=True, step=1)

        pmc.deleteUI(pBar_win_name)

        if deformer_type == 'blendShape':
            status = self.set_blendShape_weights(flip_weights_map, selected_deformer)
        else:
            status = self.set_deformer_weights(flip_weights_map, selected_deformer)
        sys.stdout.write(output_message[status])
        sys.stdout.flush()

    def flip_routine(self):
        # input validation
        if not self.input_mesh:
            raise ValueError('Select a valid mesh')
        target_path = self.get_dag_path(self.input_mesh)
        target_fnSet = om.MFnMesh(target_path)
        target_node = target_path.node()
        target_matrix = target_path.inclusiveMatrixInverse()
        target_intersector = om.MMeshIntersector()
        target_intersector.create(target_node, target_matrix)

        deformers_list_entry = pmc.textScrollList(self.deformersList, query=True, selectItem=True)
        if not deformers_list_entry:
            raise ValueError('Select a valid deformer')
        deformer_type = deformers_list_entry[0].split(' - ')[0]
        selected_deformer = deformers_list_entry[0].split(' - ')[1]
        deformer_node = self.get_depend_node(selected_deformer)

        sym_plane = pmc.radioButtonGrp(self.symmetryPlane, query=True, select=True)
        sym_axis = self.symmetry_axis[sym_plane]
        mirror_transformation = om.MMatrix().setElement(sym_axis, sym_axis, -1)

        # gather data
        routine_choice = 'future'
        try:
            deformer_set = oma.MFnGeometryFilter(deformer_node).deformerSet
            routine_choice = 'legacy'
        except:
            pass
        try:
            deformer_set_members = om.MFnSet(deformer_set).getMemebrs(faltten=True)
            routine_choice = 'standard'
        except:
            pass
        target_vtx_num = target_fnSet.numVertices
        overall_vtx_ID = [index for index in range(0, target_vtx_num)]
        if deformer_type == 'blendShape':
            if routine_choice == 'legacy':
                weights_map = self.get_blendShape_weights_legacy(ID=overall_vtx_ID)
            elif routine_choice == 'standard':
                weights_map = self.get_blendShape_weights(ID=overall_vtx_ID)
            elif routine_choice == 'future':
                weights_map = self.get_blendShape_weights_future(ID=overall_vtx_ID)
        else:
            if routine_choice == 'legacy':
                weights_map = self.get_deformer_weights_legacy(ID=overall_vtx_ID)
            elif routine_choice == 'standard':
                weights_map = self.get_deformer_weights(ID=overall_vtx_ID)
            elif routine_choice == 'future':
                weights_map = self.get_deformer_weights_future(ID=overall_vtx_ID)

        coordinates_table = self.get_vertices_position()
        vtx_ID = [index for index in coordinates_table.keys()]
        vtx_num = len(vtx_ID)

        flip_weights_map = {index: weights_map[index] for index in vtx_ID}

        output_message = {}
        output_message.setdefault('complete', 'Flip operation ended successfully \n')
        output_message.setdefault('failure', 'No weights were set: stored vertices IDs do not match with selection \n')
        output_message.setdefault('aborted', 'Flip operation aborted \n')

        pBar_title = '...Flipping weights...'
        pBar_win_name = 'PBwindow'
        if pmc.window(pBar_win_name, exists=True):
            pmc.deleteUI(pBar_win_name)
        pmc.window(pBar_win_name, title=pBar_title, sizeable=False, widthHeight=[350, 50])
        pBar_layout = pmc.formLayout(numberOfDivisions=100)
        pBar_control = pmc.progressBar(parent=pBar_layout, width=330, height=30, minValue=0, maxValue=vtx_num,
                                       progress=0)
        pmc.formLayout(pBar_layout, edit=True, attachForm=([pBar_control, 'left', 10], [pBar_control, 'top', 10]))
        pmc.showWindow(pBar_win_name)

        # flipping weights
        for id in vtx_ID:
            current_point = om.MPoint(coordinates_table[id])
            mirror_point = current_point * mirror_transformation
            closest_point = target_intersector.getClosestPoint(mirror_point)

            if closest_point:
                bar_coor = closest_point.barycentricCoords
                intersec_face = closest_point.face
                intersec_tri = closest_point.triangle

                face_component_fnSet = om.MFnSingleIndexedComponent()
                face_component = face_component_fnSet.create(om.MFn.kMeshPolygonComponent)
                face_component_fnSet.addElement(intersec_face)
                faces_iterator = om.MItMeshPolygon(target_path, face_component)
                bar_vtx = faces_iterator.getTriangle(intersec_tri)
                bar_vtx_ID = bar_vtx[1]

                bar_weight = bar_coor[0] * weights_map[bar_vtx_ID[0]] + bar_coor[1] * weights_map[bar_vtx_ID[1]] + (
                            1 - bar_coor[0] - bar_coor[1]) * weights_map[bar_vtx_ID[2]]
                flip_weights_map[id] = bar_weight

            pmc.progressBar(pBar_control, edit=True, step=1)

        pmc.deleteUI(pBar_win_name)

        if deformer_type == 'blendShape':
            status = self.set_blendShape_weights(flip_weights_map, selected_deformer)
        else:
            status = self.set_deformer_weights(flip_weights_map, selected_deformer)
        sys.stdout.write(output_message[status])
        sys.stdout.flush()

    def copy_routine_legacy(self):
        # input validation
        if not self.copy_source_info:
            raise ValueError('Select a valid source')
        source_mesh = self.copy_source_info[0]
        if not pmc.objExists(source_mesh):
            raise ValueError('Mesh {Name} no longer exists'.format(Name=str(source_mesh)))
        source_path = self.get_dag_path(source_mesh)
        source_deformer = self.copy_source_info[1][1]
        if not pmc.objExists(source_deformer):
            raise ValueError('Deformer {Name} no longer exists'.format(Name=source_deformer))
        source_deformer_type = self.copy_source_info[1][0]
        source_deformer_node = self.get_depend_node(source_deformer)

        if not self.copy_target_info:
            raise ValueError('Select a valid target')
        target_mesh = self.copy_target_info[0]
        if not pmc.objExists(target_mesh):
            raise ValueError('Mesh {Name} no longer exists'.format(Name=str(target_mesh)))
        target_path = self.get_dag_path(target_mesh)
        target_deformer = self.copy_target_info[1][1]
        if not pmc.objExists(target_deformer):
            raise ValueError('Deformer {Name} no longer exists'.format(Name=target_deformer))
        target_deformer_type = self.copy_target_info[1][0]

        # copy weights from source to target
        routine_choice = 'future'
        try:
            deformer_set = oma.MFnGeometryFilter(deformer_node).deformerSet
            routine_choice = 'legacy'
        except:
            pass
        try:
            deformer_set_members = om.MFnSet(deformer_set).getMemebrs(faltten=True)
            routine_choice = 'standard'
        except:
            pass
        source_fnSet = om.MFnMesh(source_path)
        source_vtx_num = source_fnSet.numVertices
        source_vtx_ID = [index for index in range(0, source_vtx_num)]
        if source_deformer_type == 'blendShape':
            if routine_choice == 'legacy':
                source_weights_map = self.get_blendShape_weights_legacy(target=source_mesh,
                                                                        deformer_name=source_deformer, ID=source_vtx_ID)
            elif routine_choice == 'standard':
                source_weights_map = self.get_blendShape_weights(target=source_mesh, deformer_name=source_deformer,
                                                                 ID=source_vtx_ID)
            elif routine_choice == 'future':
                source_weights_map = self.get_blendShape_weights_future(target=source_mesh,
                                                                        deformer_name=source_deformer, ID=source_vtx_ID)
        else:
            if routine_choice == 'legacy':
                source_weights_map = self.get_deformer_weights_legacy(target=source_mesh, deformer_name=source_deformer,
                                                                      ID=source_vtx_ID)
            elif routine_choice == 'standard':
                source_weights_map = self.get_deformer_weights(target=source_mesh, deformer_name=source_deformer,
                                                               ID=source_vtx_ID)
            elif routine_choice == 'future':
                source_weights_map = self.get_deformer_weights_future(target=source_mesh, deformer_name=source_deformer,
                                                                      ID=source_vtx_ID)

        target_fnSet = om.MFnMesh(target_path)
        target_vtx_num = target_fnSet.numVertices
        target_vtx_ID = [index for index in range(0, target_vtx_num)]
        target_points = target_fnSet.getPoints(om.MSpace.kWorld)
        target_weights_map = {index: 0 for index in target_vtx_ID}

        output_message = {}
        output_message.setdefault('complete', 'Copy operation ended successfully \n')
        output_message.setdefault('failure', 'No weights were set: stored vertices IDs do not match with selection \n')
        output_message.setdefault('aborted', 'Copy operation aborted \n')

        pBar_title = '...Copying weights...'
        pBar_win_name = 'PBwindow'
        if pmc.window(pBar_win_name, exists=True):
            pmc.deleteUI(pBar_win_name)
        pmc.window(pBar_win_name, title=pBar_title, sizeable=False, widthHeight=[350, 50])
        pBar_layout = pmc.formLayout(numberOfDivisions=100)
        pBar_control = pmc.progressBar(parent=pBar_layout, width=330, height=30, minValue=0, maxValue=target_vtx_num,
                                       progress=0)
        pmc.formLayout(pBar_layout, edit=True, attachForm=([pBar_control, 'left', 10], [pBar_control, 'top', 10]))
        pmc.showWindow(pBar_win_name)

        for id in target_vtx_ID:
            current_point = target_points[id]
            closest_point = source_fnSet.getClosestPoint(current_point, om.MSpace.kWorld)

            if closest_point:
                face_component_fnSet = om.MFnSingleIndexedComponent()
                face_component = face_component_fnSet.create(om.MFn.kMeshPolygonComponent)
                face_component_fnSet.addElement(closest_point[1])
                face_iterator = om.MItMeshPolygon(source_path, face_component)
                face_triangles = face_iterator.getTriangles(om.MSpace.kWorld)
                tri_num = len(face_triangles)
                for counter in range(0, tri_num):
                    vec_A = om.MVector(face_triangles[0][0 + counter * 3])
                    vec_B = om.MVector(face_triangles[0][1 + counter * 3])
                    vec_C = om.MVector(face_triangles[0][2 + counter * 3])
                    vec_P = om.MVector(closest_point[0])
                    bar_coor = self.barycenter(vec_A, vec_B, vec_C, vec_P)
                    if max(bar_coor) > 0:
                        break

                bar_weight = bar_coor[0] * source_weights_map[face_triangles[1][0 + counter * 3]] + bar_coor[1] * \
                             source_weights_map[face_triangles[1][1 + counter * 3]] + bar_coor[2] * source_weights_map[
                                 face_triangles[1][2 + counter * 3]]
                target_weights_map[id] = bar_weight

            pmc.progressBar(pBar_control, edit=True, step=1)

        pmc.deleteUI(pBar_win_name)

        if target_deformer_type == 'blendShape':
            status = self.set_blendShape_weights(target_weights_map, source_deformer, target=target_mesh,
                                                 deformer_name=target_deformer, ID=target_vtx_ID)
        else:
            status = self.set_deformer_weights(target_weights_map, source_deformer, target=target_mesh,
                                               deformer_name=target_deformer, ID=target_vtx_ID)
        sys.stdout.write(output_message[status])
        sys.stdout.flush()

    def copy_routine(self):
        # input validation
        if not self.copy_source_info:
            raise ValueError('Select a valid source')
        source_mesh = self.copy_source_info[0]
        if not pmc.objExists(source_mesh):
            raise ValueError('Mesh {Name} no longer exists'.format(Name=str(source_mesh)))
        source_path = self.get_dag_path(source_mesh)
        source_deformer = self.copy_source_info[1][1]
        if not pmc.objExists(source_deformer):
            raise ValueError('Deformer {Name} no longer exists'.format(Name=source_deformer))
        source_deformer_type = self.copy_source_info[1][0]
        source_deformer_node = self.get_depend_node(source_deformer)

        if not self.copy_target_info:
            raise ValueError('Select a valid target')
        target_mesh = self.copy_target_info[0]
        if not pmc.objExists(target_mesh):
            raise ValueError('Mesh {Name} no longer exists'.format(Name=str(target_mesh)))
        target_path = self.get_dag_path(target_mesh)
        target_deformer = self.copy_target_info[1][1]
        if not pmc.objExists(target_deformer):
            raise ValueError('Deformer {Name} no longer exists'.format(Name=target_deformer))
        target_deformer_type = self.copy_target_info[1][0]

        # copy weights from source to target
        routine_choice = 'future'
        try:
            deformer_set = oma.MFnGeometryFilter(deformer_node).deformerSet
            routine_choice = 'legacy'
        except:
            pass
        try:
            deformer_set_members = om.MFnSet(deformer_set).getMemebrs(faltten=True)
            routine_choice = 'standard'
        except:
            pass
        source_fnSet = om.MFnMesh(source_path)
        source_vtx_num = source_fnSet.numVertices
        source_vtx_ID = [index for index in range(0, source_vtx_num)]
        if source_deformer_type == 'blendShape':
            if routine_choice == 'legacy':
                source_weights_map = self.get_blendShape_weights_legacy(target=source_mesh,
                                                                        deformer_name=source_deformer, ID=source_vtx_ID)
            elif routine_choice == 'standard':
                source_weights_map = self.get_blendShape_weights(target=source_mesh, deformer_name=source_deformer,
                                                                 ID=source_vtx_ID)
            elif routine_choice == 'future':
                source_weights_map = self.get_blendShape_weights_future(target=source_mesh,
                                                                        deformer_name=source_deformer, ID=source_vtx_ID)
        else:
            if routine_choice == 'legacy':
                source_weights_map = self.get_deformer_weights_legacy(target=source_mesh, deformer_name=source_deformer,
                                                                      ID=source_vtx_ID)
            elif routine_choice == 'standard':
                source_weights_map = self.get_deformer_weights(target=source_mesh, deformer_name=source_deformer,
                                                               ID=source_vtx_ID)
            elif routine_choice == 'future':
                source_weights_map = self.get_deformer_weights_future(target=source_mesh, deformer_name=source_deformer,
                                                                      ID=source_vtx_ID)

        source_node = source_path.node()
        source_matrix = source_path.inclusiveMatrixInverse()
        source_intersector = om.MMeshIntersector()
        source_intersector.create(source_node, source_matrix)

        target_fnSet = om.MFnMesh(target_path)
        target_vtx_num = target_fnSet.numVertices
        target_vtx_ID = [index for index in range(0, target_vtx_num)]
        target_points = target_fnSet.getPoints(om.MSpace.kWorld)
        target_weights_map = {index: 0 for index in target_vtx_ID}

        output_message = {}
        output_message.setdefault('complete', 'Copy operation ended successfully \n')
        output_message.setdefault('failure', 'No weights were set: stored vertices IDs do not match with selection \n')
        output_message.setdefault('aborted', 'Copy operation aborted \n')

        pBar_title = '...Copying weights...'
        pBar_win_name = 'PBwindow'
        if pmc.window(pBar_win_name, exists=True):
            pmc.deleteUI(pBar_win_name)
        pmc.window(pBar_win_name, title=pBar_title, sizeable=False, widthHeight=[350, 50])
        pBar_layout = pmc.formLayout(numberOfDivisions=100)
        pBar_control = pmc.progressBar(parent=pBar_layout, width=330, height=30, minValue=0, maxValue=target_vtx_num,
                                       progress=0)
        pmc.formLayout(pBar_layout, edit=True, attachForm=([pBar_control, 'left', 10], [pBar_control, 'top', 10]))
        pmc.showWindow(pBar_win_name)

        for id in target_vtx_ID:
            current_point = target_points[id]
            closest_point = source_intersector.getClosestPoint(current_point)

            if closest_point:
                bar_coor = closest_point.barycentricCoords
                intersec_face = closest_point.face
                intersec_tri = closest_point.triangle

                face_component_fnSet = om.MFnSingleIndexedComponent()
                face_component = face_component_fnSet.create(om.MFn.kMeshPolygonComponent)
                face_component_fnSet.addElement(intersec_face)
                face_iterator = om.MItMeshPolygon(source_path, face_component)
                bar_vtx = face_iterator.getTriangle(intersec_tri)
                bar_vtx_ID = bar_vtx[1]

                bar_weight = bar_coor[0] * source_weights_map[bar_vtx_ID[0]] + bar_coor[1] * source_weights_map[
                    bar_vtx_ID[1]] + (1 - bar_coor[0] - bar_coor[1]) * source_weights_map[bar_vtx_ID[2]]
                target_weights_map[id] = bar_weight

            pmc.progressBar(pBar_control, edit=True, step=1)

        pmc.deleteUI(pBar_win_name)

        if target_deformer_type == 'blendShape':
            status = self.set_blendShape_weights(target_weights_map, source_deformer, target=target_mesh,
                                                 deformer_name=target_deformer, ID=target_vtx_ID)
        else:
            status = self.set_deformer_weights(target_weights_map, source_deformer, target=target_mesh,
                                               deformer_name=target_deformer, ID=target_vtx_ID)
        sys.stdout.write(output_message[status])
        sys.stdout.flush()

    def mesh_field_command(self, *args):
        self.input_mesh = []

        target = pmc.textFieldButtonGrp(self.meshGroup, query=True, text=True)
        target_shape = self.get_target_shape(target)
        if target_shape != None:
            if self.is_a_mesh(target_shape):
                self.input_mesh = target_shape
                self.deformers_scroll_list()
                return

        pmc.warning('Select a valid mesh')

    def mesh_button_command(self, *args):
        self.input_mesh = []

        selection = pmc.ls(selection=True)
        if selection:
            target = selection[-1]
            pmc.textFieldButtonGrp(self.meshGroup, edit=True, text=str(target))
            target_shape = self.get_target_shape(target)
            if target_shape != None:
                if self.is_a_mesh(target_shape):
                    self.input_mesh = target_shape
                    self.deformers_scroll_list()
                    return

        pmc.warning('Select a valid mesh')

    def dir_field_command(self, *args):
        start_dir = pmc.textFieldButtonGrp(self.importExportGroup, query=True, fileName=True)
        if not os.path.isdir(start_dir):
            pmc.warning('Directory not found: default start directory will be used instead')

    def dir_button_command(self, *args):
        input_dir = pmc.textFieldButtonGrp(self.importExportGroup, query=True, fileName=True)
        if not os.path.isdir(input_dir):
            input_dir = self.working_dir
        start_dir = pmc.fileDialog2(dialogStyle=1, caption='Select Start Directory', startingDirectory=input_dir,
                                    fileMode=3)
        if start_dir:
            pmc.textFieldButtonGrp(self.importExportGroup, edit=True, fileName=start_dir[0])

    def index_algorithm(self, *args):
        pmc.textFieldGrp(self.loadTolerance, edit=True, enable=False)

    def position_algorithm(self, *args):
        pmc.textFieldGrp(self.loadTolerance, edit=True, enable=True)

    def set_tolerance(self, *args):
        input_tolerance = pmc.textFieldGrp(self.loadTolerance, query=True, text=True)
        try:
            tolerance_val = float(input_tolerance)
            if tolerance_val <= 0:
                raise
        except:
            pmc.warning(
                'Tolerance must be of type "float". Only positive, non-zero values are allowed. A default tolerance of 0.1 is applied otherwise')

    def save_weights(self, *args):
        # input validation
        if not self.input_mesh:
            raise ValueError('Select a valid mesh')
        target_path = self.get_dag_path(self.input_mesh)
        target_transform = om.MFnDagNode(target_path).parent(0)
        target_name = om.MFnDependencyNode(target_transform).name()

        deformers_list_entry = pmc.textScrollList(self.deformersList, query=True, selectItem=True)
        if not deformers_list_entry:
            raise ValueError('Select a valid deformer')
        deformer_type = deformers_list_entry[0].split(' - ')[0]
        selected_deformer = deformers_list_entry[0].split(' - ')[1]
        deformer_node = self.get_depend_node(selected_deformer)

        start_dir = pmc.textFieldButtonGrp(self.importExportGroup, query=True, fileName=True)
        if not os.path.isdir(start_dir):
            start_dir = self.working_dir
        save_file = pmc.fileDialog2(dialogStyle=1, caption='Save As', startingDirectory=start_dir, fileMode=0,
                                    fileFilter='*.json')
        if not save_file:
            sys.stdout.write('Save operation aborted \n')
            sys.stdout.flush()
            return
        file_name = save_file[0]

        # gather data
        routine_choice = 'future'
        try:
            deformer_set = oma.MFnGeometryFilter(deformer_node).deformerSet
            routine_choice = 'legacy'
        except:
            pass
        try:
            deformer_set_members = om.MFnSet(deformer_set).getMemebrs(faltten=True)
            routine_choice = 'standard'
        except:
            pass
        if deformer_type == 'blendShape':
            if routine_choice == 'legacy':
                weights_map = self.get_blendShape_weights_legacy()
            elif routine_choice == 'standard':
                weights_map = self.get_blendShape_weights()
            elif routine_choice == 'future':
                weights_map = self.get_blendShape_weights_future()
        else:
            if routine_choice == 'legacy':
                weights_map = self.get_deformer_weights_legacy()
            elif routine_choice == 'standard':
                weights_map = self.get_deformer_weights()
            elif routine_choice == 'future':
                weights_map = self.get_deformer_weights_future()
        vtx_count = len(weights_map)

        coordinates_table = self.get_vertices_position()

        file_header = {}
        file_header.setdefault('FILE NAME', file_name)
        file_header.setdefault('MESH NAME', target_name)
        file_header.setdefault('DEFORMER NAME', selected_deformer)
        file_header.setdefault('VERTICES COUNT', vtx_count)

        export_data = {}
        export_data.setdefault('header', file_header)
        export_data.setdefault('weightsMap', weights_map)
        export_data.setdefault('coordinatesTable', coordinates_table)

        # save weights
        with open(file_name, mode='w', encoding='utf-8') as export_file:
            export_file.write(str(json.dumps(export_data, indent=4, sort_keys=True)))
        sys.stdout.write('Save operation ended successfully')
        sys.stdout.flush()

    def load_weights(self, *args):
        # input validation
        deformers_list_entry = pmc.textScrollList(self.deformersList, query=True, selectItem=True)
        if not deformers_list_entry:
            raise ValueError('Select a valid deformer')
        deformer_type = deformers_list_entry[0].split(' - ')[0]

        # gather data
        start_dir = pmc.textFieldButtonGrp(self.importExportGroup, query=True, fileName=True)
        if not os.path.isdir(start_dir):
            start_dir = self.working_dir
        load_file = pmc.fileDialog2(dialogStyle=1, caption='Load', startingDirectory=start_dir, fileMode=1,
                                    fileFilter='*.json')
        if not load_file:
            sys.stdout.write('Load operation aborted')
            sys.stdout.flush()
            return
        file_name = load_file[0]

        with open(file_name, mode='r', encoding='utf-8') as import_file:
            import_data = json.load(import_file)
        try:
            header = import_data['header']
        except:
            raise KeyError('Unable to find "header" key in import file')
        try:
            coordinates_table = import_data['coordinatesTable']
        except:
            raise KeyError('Unable to find "coordinatesTable" key in import file')
        try:
            weights_map = import_data['weightsMap']
        except:
            raise KeyError('Unable to find "weightsMap" key in import file')

        output_message = {}
        output_message.setdefault('complete', 'Load operation ended successfully \n')
        output_message.setdefault('failure', 'No weights were set: stored vertices IDs do not match with selection \n')
        output_message.setdefault('aborted', 'Load operation aborted \n')

        algorithm = pmc.radioButtonGrp(self.loadVertices, query=True, select=True)

        # load weights
        if algorithm == 1:  # load by vertex ID
            if deformer_type == 'blendShape':
                status = self.set_blendShape_weights(weights_map, header['DEFORMER NAME'])
            else:
                status = self.set_deformer_weights(weights_map, header['DEFORMER NAME'])

        elif algorithm == 2:  # load by vertex position
            avg_weights_map = self.average_weights_map(coordinates_table, weights_map)
            if deformer_type == 'blendShape':
                status = self.set_blendShape_weights(avg_weights_map, header['DEFORMER NAME'])
            else:
                status = self.set_deformer_weights(avg_weights_map, header['DEFORMER NAME'])

        sys.stdout.write(output_message[status])
        sys.stdout.flush()

    def mirror_weights(self, *args):
        # choose routine
        selection_list = om.MGlobal.getActiveSelectionList()

        dummy = pmc.polyCube()
        dummy_mesh = self.get_target_shape(dummy[0])
        dummy_path = self.get_dag_path(dummy_mesh)
        dummy_node = dummy_path.node()
        dummy_matrix = dummy_path.inclusiveMatrix()
        routine_choice = 'legacy'
        try:
            dummy_intersector = om.MMeshIntersector()
            dummy_intersector.create(dummy_node, dummy_matrix)
            routine_choice = 'new'
        except:
            pass

        pmc.delete(dummy)
        om.MGlobal.setActiveSelectionList(selection_list)

        # mirror routine
        if routine_choice == 'legacy':
            self.mirror_routine_legacy()
        elif routine_choice == 'new':
            self.mirror_routine()

    def flip_weights(self, *args):
        # choose routine
        selection_list = om.MGlobal.getActiveSelectionList()

        dummy = pmc.polyCube()
        dummy_mesh = self.get_target_shape(dummy[0])
        dummy_path = self.get_dag_path(dummy_mesh)
        dummy_node = dummy_path.node()
        dummy_matrix = dummy_path.inclusiveMatrix()
        routine_choice = 'legacy'
        try:
            dummy_intersector = om.MMeshIntersector()
            dummy_intersector.create(dummy_node, dummy_matrix)
            routine_choice = 'new'
        except:
            pass

        pmc.delete(dummy)
        om.MGlobal.setActiveSelectionList(selection_list)

        # flip routine
        if routine_choice == 'legacy':
            self.flip_routine_legacy()
        elif routine_choice == 'new':
            self.flip_routine()

    def copy_source(self, *args):
        # input validation
        if not self.input_mesh:
            raise ValueError('Select a valid mesh')
        source_mesh = self.input_mesh

        deformers_list_entry = pmc.textScrollList(self.deformersList, query=True, selectItem=True)
        if not deformers_list_entry:
            raise ValueError('Select a valid deformer')
        deformer_type = deformers_list_entry[0].split(' - ')[0]
        selected_deformer = deformers_list_entry[0].split(' - ')[1]

        # store info
        user_message = '{Name1}    ->    {Name2}'.format(Name1=str(source_mesh), Name2=selected_deformer)
        pmc.text(self.sourceText, edit=True, label=user_message)
        self.copy_source_info = []
        self.copy_source_info.append(source_mesh)
        self.copy_source_info.append((deformer_type, selected_deformer))

    def copy_target(self, *args):
        # input validation
        if not self.input_mesh:
            raise ValueError('Select a valid mesh')
        target_mesh = self.input_mesh

        deformers_list_entry = pmc.textScrollList(self.deformersList, query=True, selectItem=True)
        if not deformers_list_entry:
            raise ValueError('Select a valid deformer')
        deformer_type = deformers_list_entry[0].split(' - ')[0]
        selected_deformer = deformers_list_entry[0].split(' - ')[1]

        # store info
        user_message = '{Name1}    ->    {Name2}'.format(Name1=str(target_mesh), Name2=selected_deformer)
        pmc.text(self.targetText, edit=True, label=user_message)
        self.copy_target_info = []
        self.copy_target_info.append(target_mesh)
        self.copy_target_info.append((deformer_type, selected_deformer))

    def copy_weights(self, *args):
        # choose routine
        selection_list = om.MGlobal.getActiveSelectionList()

        dummy = pmc.polyCube()
        dummy_mesh = self.get_target_shape(dummy[0])
        dummy_path = self.get_dag_path(dummy_mesh)
        dummy_node = dummy_path.node()
        dummy_matrix = dummy_path.inclusiveMatrix()
        routine_choice = 'legacy'
        try:
            dummy_intersector = om.MMeshIntersector()
            dummy_intersector.create(dummy_node, dummy_matrix)
            routine_choice = 'new'
        except:
            pass

        pmc.delete(dummy)
        om.MGlobal.setActiveSelectionList(selection_list)

        # copy routine
        if routine_choice == 'legacy':
            self.copy_routine_legacy()
        elif routine_choice == 'new':
            self.copy_routine()


