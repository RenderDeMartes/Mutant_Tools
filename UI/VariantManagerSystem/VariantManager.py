from __future__ import absolute_import
try:
    import importlib;from importlib import reload
except:
    import imp;from imp import reload

import sys
import traceback

from mstar.nodes.sid import Sid
from star import entities
from mstar.nodes.mayaNode import MayaNode

from maya import cmds, mel
from maya.api import OpenMaya as om2

from Mutant_Tools.Utils.Helpers.decorators import undo

class VariantManager():
    VARIANT_ATTR = "variant"
    MAIN_MESH = 'C_Body_hi'
    VARIANT_TEXTURE_NODE = 'Variant_Layered_Texture'
    ALPHA_SDK_STRING = 'SDK_{}_alpha_gain'

    def __init__(self):
        self.added_variants = []
        self.initialize_variant_list()
        


    def initialize_variant_list(self):
        self.sid_node = Sid.find()
        if self.sid_node:
            self.sid_node = self.sid_node[0]
        else:
            return False
        self.variant_list = self.sid_node.entity.variants
        print(self.variant_list)

    @undo
    def update_main_ctrl(self):
        
        self.main_ctrl = MayaNode(cmds.ls("*Global_Ctrl", long=True, recursive=True)[0])

        if not self.main_ctrl.hasAttr(self.VARIANT_ATTR):
            cmds.addAttr(self.main_ctrl.fullname,
            longName=self.VARIANT_ATTR,
            attributeType='enum',
            enumName=':'.join(self.variant_list),
            keyable=True)

        variant_attr_values = cmds.attributeQuery(
            self.VARIANT_ATTR,
            node=self.main_ctrl.fullname,
            listEnum=True
        )[0].split(':')

        self.system_outdated = False

        if variant_attr_values != self.variant_list:
            self.system_outdated = True
            self.added_variants = [v for v in self.variant_list if v not in variant_attr_values]
            curr_variants = [v for v in variant_attr_values if v in self.variant_list]
            new_variant_list  = curr_variants + self.added_variants

            cmds.addAttr(
                "{}.{}".format(self.main_ctrl.fullname, self.VARIANT_ATTR),
                edit=True,
                enumName=':'.join(new_variant_list)
            )
    
    @undo
    def _getMaterialFromMesh(self, mesh=''):
        if mesh is None or not cmds.objExists(mesh):
            cmds.error("Must have a valid mesh selection")
        
        cmds.select(clear=1)
        cmds.select(mesh)
        cmds.hyperShade(shaderNetworksSelectMaterialNodes=1)
        materials = cmds.ls(sl=1)

        if len(materials) > 1:
            cmds.warning("Selected mesh has more than one material, returning first one")
        print(materials)

        return materials[0]

    @undo
    def update_variant_system(self):
        self.update_main_ctrl()
        self.get_main_material()

        input_connections = cmds.listConnections(self.main_material, destination=False)

        if not input_connections:
            self.create_variant_setup()
        elif self.VARIANT_TEXTURE_NODE in input_connections:
            # variant system already exists
            # check if it is updated
            for variant in self.added_variants:
                self.create_variant_file_node(variant)

            self.connect_variants_2_layer_texture()
        else:
            self.create_variant_setup()
            

        return self.get_existing_variant_files()

    def get_main_material(self):
        if cmds.objExists(self.MAIN_MESH):
            self.main_material = self._getMaterialFromMesh(self.MAIN_MESH)
            print("Main mesh = {} main material = {}".format(self.MAIN_MESH, self.main_material))
        else:
            cmds.error('Could not find main material')

    def get_existing_variant_files(self):
        self.variant_file_dict = {i:{} for i in self.variant_list}
        
        for i in self.variant_file_dict.keys():
            self.variant_file_dict[i] = cmds.getAttr('F_{}.fileTextureName'.format(i))


        return self.variant_file_dict


    @undo
    def connect_variants_2_layer_texture(self):

        layered_texture_node = self.VARIANT_TEXTURE_NODE
        for i, variant in enumerate(self.variant_list):
            file_node = 'F_{}'.format(variant)

            # clean up
            for attribute in [file_node + '.outAlpha', file_node + '.outColor']:
                destinationAttrs = cmds.listConnections(attribute, plugs=True, source=False) or []
                for destAttr in destinationAttrs:
                    cmds.disconnectAttr(attribute, destAttr)

            source = cmds.listConnections(file_node + '.alphaGain', destination=False)[0]
            if cmds.objExists(source):
                cmds.delete(source)

            # reconnect

            cmds.connectAttr('{}.outColor'.format(file_node), '{0}.inputs[{1}].color'.format(layered_texture_node, i))
            cmds.connectAttr('{}.outAlpha'.format(file_node), '{0}.inputs[{1}].alpha'.format(layered_texture_node, i))


            # sdk setup

            alpha_gain_sdk = cmds.createNode('animCurveUU', n=self.ALPHA_SDK_STRING.format(file_node))


            cmds.connectAttr('Global_Ctrl.variant', '{}.input'.format(alpha_gain_sdk))
            cmds.connectAttr('{}.output'.format(alpha_gain_sdk), '{}.alphaGain'.format(file_node))

            # set anim curve value to 0 (visible) unless it's enum corresponding to node

            for j in range(len(self.variant_list)):
                if j == i:
                    cmds.setKeyframe(alpha_gain_sdk, f=j, v=1)
                else:
                    cmds.setKeyframe(alpha_gain_sdk, f=j, v=0)

        mel.eval("generateAllUvTilePreviews;")


    @undo
    def create_variant_file_node(self, variant_name):
        file_node = cmds.shadingNode('file', asTexture=1, isColorManaged=1, n='F_{0}'.format(variant_name))
        place_texture_node = cmds.shadingNode('place2dTexture', asUtility=1, n='PT2d_{0}'.format(variant_name))

        # place texture node - file node setup
        
        cmds.connectAttr('{}.coverage'.format(place_texture_node), '{}.coverage'.format(file_node))
        cmds.connectAttr('{}.translateFrame'.format(place_texture_node), '{}.translateFrame'.format(file_node))
        cmds.connectAttr('{}.rotateFrame'.format(place_texture_node), '{}.rotateFrame'.format(file_node))
        cmds.connectAttr('{}.mirrorU'.format(place_texture_node), '{}.mirrorU'.format(file_node))
        cmds.connectAttr('{}.mirrorV'.format(place_texture_node), '{}.mirrorV'.format(file_node))
        cmds.connectAttr('{}.stagger'.format(place_texture_node), '{}.stagger'.format(file_node))
        cmds.connectAttr('{}.wrapU'.format(place_texture_node), '{}.wrapU'.format(file_node))
        cmds.connectAttr('{}.wrapV'.format(place_texture_node), '{}.wrapV'.format(file_node))
        cmds.connectAttr('{}.repeatUV'.format(place_texture_node), '{}.repeatUV'.format(file_node))
        cmds.connectAttr('{}.offset'.format(place_texture_node), '{}.offset'.format(file_node))
        cmds.connectAttr('{}.rotateUV'.format(place_texture_node), '{}.rotateUV'.format(file_node))
        cmds.connectAttr('{}.noiseUV'.format(place_texture_node), '{}.noiseUV'.format(file_node))
        cmds.connectAttr('{}.vertexUvOne'.format(place_texture_node), '{}.vertexUvOne'.format(file_node))
        cmds.connectAttr('{}.vertexUvTwo'.format(place_texture_node), '{}.vertexUvTwo'.format(file_node))
        cmds.connectAttr('{}.vertexUvThree'.format(place_texture_node), '{}.vertexUvThree'.format(file_node))
        cmds.connectAttr('{}.vertexCameraOne'.format(place_texture_node), '{}.vertexCameraOne'.format(file_node))

        cmds.connectAttr('{}.outUV'.format(place_texture_node), '{}.uv'.format(file_node))
        cmds.connectAttr('{}.outUvFilterSize'.format(place_texture_node), '{}.uvFilterSize'.format(file_node))

        # sets uv tiling mode to udim

        cmds.setAttr('{}.uvTilingMode'.format(file_node), 3)

        return file_node

    @undo
    def create_variant_setup(self):

        # check for global_ctlr and get the variants
        
        variants = self.variant_list
        variants_length = len(variants)

        print('Variants: {0}'.format(variants))


        layered_texture_node = cmds.shadingNode('layeredTexture', asTexture=1, n=self.VARIANT_TEXTURE_NODE)
        
        # connect to material color

        cmds.connectAttr('{}.outColor'.format(layered_texture_node), '{}.color'.format(self.main_material), f=1)


        for i, variant in enumerate(variants):
            file_node = self.create_variant_file_node(variant)

            # connects file texture color to material color

            cmds.connectAttr('{}.outColor'.format(file_node), '{0}.inputs[{1}].color'.format(layered_texture_node, i))
            cmds.connectAttr('{}.outAlpha'.format(file_node), '{0}.inputs[{1}].alpha'.format(layered_texture_node, i))


            # sdk setup

            alpha_gain_sdk = cmds.createNode('animCurveUU', n=self.ALPHA_SDK_STRING.format(file_node))


            cmds.connectAttr('Global_Ctrl.variant', '{}.input'.format(alpha_gain_sdk))
            cmds.connectAttr('{}.output'.format(alpha_gain_sdk), '{}.alphaGain'.format(file_node))

            # set anim curve value to 0 (visible) unless it's enum corresponding to node

            for j in range(variants_length):
                if j == i:
                    cmds.setKeyframe(alpha_gain_sdk, f=j, v=1)
                else:
                    cmds.setKeyframe(alpha_gain_sdk, f=j, v=0)

        # refresh textures and previews

        mel.eval("generateAllUvTilePreviews;")
        #mel.eval("AEReloadAllTextures;")

    @undo
    def set_variant_file_path(self, variant, path):
        file_node = 'F_{}'.format(variant)
        cmds.setAttr('{}.fileTextureName'.format(file_node), path, type='string')
    
    @undo
    def set_active_variant(self, variant):
        variant_index = self.variant_list.index(variant)
        cmds.setAttr(self.main_ctrl.name + '.variant', variant_index)

    def reload_udims(self):
        mel.eval("generateAllUvTilePreviews;")

    def open_hyper_shade(self):
        mel_cmd = """
        // open HyperShape window
        HypershadeWindow;
        // clear graph display
        hyperShadePanelGraphCommand("hyperShadePanel1", "clearGraph");
        // select your material here
        select -r lambert1;
        // display selected material and connections.
        // evalDeferred is used because this function must be called after the hypergraph is ready.
        evalDeferred("hyperShadePanelGraphCommand(\\"hyperShadePanel1\\", \\"showUpAndDownstream\\")");"""
        mel.eval(mel_cmd)

    def set_selected_2_variant_viz(self, variant):
        selected = cmds.ls(sl=1)
        for geometry in selected:
            cmds.connectAttr(self.ALPHA_SDK_STRING.format('F_' + variant) + '.output', '{}.visibility'.format(geometry))

    def break_sdk_viz_connections(self):
        for variant in self.variant_list:
            variant_sdk = self.ALPHA_SDK_STRING.format("F_"+variant)
            connections = cmds.listConnections(variant_sdk, source=0, destination=1, p=1)
            for connection in connections:
                if connection.endswith('visibility'):
                    cmds.disconnectAttr('{}.output'.format(variant_sdk), connection)
                    cmds.setAttr(connection.split('.')[0] + '.visibility', 1)
            print(connections)
