from __future__ import absolute_import

"""

import Mutant_Tools
from Mutant_Tools.Utils.Correctives import blendshapes_correctives
reload(blendshapes_correctives)

geo = 'Body_Geo'
template = 'Hip'

cBSPCorrectives = blendshapes_correctives.BSP_Correctives(geo, template)
cBSPCorrectives.create_correctives()

#------------------------------------------

import Mutant_Tools
from Mutant_Tools.Utils.Correctives import blendshapes_correctives
reload(blendshapes_correctives)

geo = 'Body_Geo'
template = 'Hip'
blendshape_name = 'blendShape1'

cBSPCorrectives = blendshapes_correctives.BSP_Correctives(geo, template)
cBSPCorrectives.connect_correctives(geo, blendshape_name, template)

#------------------------------------------
import Mutant_Tools
from Mutant_Tools.Utils.Correctives import blendshapes_correctives
reload(blendshapes_correctives)

geo = 'Body_Geo'
template = 'Hip'
blendshape_name = 'blendShape1'

cBSPCorrectives = blendshapes_correctives.BSP_Correctives(geo, template)
cBSPCorrectives.connect_correctives(geo, blendshape_name, template, mirror=True)



"""

from maya import cmds

correctives_templates = {

    "Hip": {
            'driver': 'L_Hip_Jnt',
            'bsp_name': 'HipCorrectives',
            'shapes': ['L_HipFront', 'L_HipBack', 'L_HipOut'],
            'values': [90, -90, 90],
            'attributes': ['L_Hip_Jnt.rotateZ', 'L_Hip_Jnt.rotateZ', 'L_Hip_Jnt.rotateY'],
            'driver_sdk': ['L_Hip_Fk_Ctrl.rotateZ', 'L_Hip_Fk_Ctrl.rotateZ', 'L_Hip_Fk_Ctrl.rotateY'],
            'require_switch': ['L_Hip_Attrs_Ctrl.Switch_IK_FK', 1]
            },

    "Knee": {
            'driver': 'L_Knee_Jnt',
            'bsp_name': 'KneeCorrectives',
            'shapes': ['L_Bend'],
            'values': [-90],
            'attributes': ['L_Knee_Jnt.rotateZ'],
            'driver_sdk': ['L_Knee_Fk_Ctrl.rotateZ'],
            'require_switch': ['L_Hip_Attrs_Ctrl.Switch_IK_FK', 1]
             },

    "Ankle": {
            'driver': 'L_Ankle_Jnt',
            'bsp_name': 'AnkleCorrectives',
            'shapes': ['L_AnkleUp', 'L_AnkleDown'],
            'values': [45, -45],
            'attributes': ['L_Ankle_Jnt.rotateZ', 'L_Ankle_Jnt.rotateZ'],
            'driver_sdk': ['L_Ankle_Fk_Ctrl.rotateZ', 'L_Ankle_Fk_Ctrl.rotateZ'],
            'require_switch': ['L_Hip_Attrs_Ctrl.Switch_IK_FK', 1]
            },

    "Shoulder": {
            'driver': 'L_Shoulder_Jnt',
            'bsp_name': 'ShoulderCorrectives',
            'shapes': ['L_ShoulderUp', 'L_ShoulderDown'],
            'values': [90, -30],
            'attributes': ['L_Shoulder_Jnt.rotateY', 'L_Shoulder_Jnt.rotateY'],
            'driver_sdk': ['L_Shoulder_Fk_Ctrl.rotateY', 'L_Shoulder_Fk_Ctrl.rotateY'],
            'require_switch': ['L_Shoulder_Attrs_Ctrl.Switch_IK_FK', 1]
            },

    "Elbow": {
            'driver': 'L_Elbow_Jnt',
            'bsp_name': 'ElbowCorrectives',
            'shapes': ['L_Bend'],
            'values': [90],
            'attributes': ['L_Elbow_Jnt.rotateZ'],
            'driver_sdk': ['L_Elbow_Fk_Ctrl.rotateZ'],
            'require_switch': ['L_Shoulder_Attrs_Ctrl.Switch_IK_FK', 1]
             },

    "Wrist": {
            'driver': 'L_Wrist_Jnt',
            'bsp_name': 'WristCorrectives',
            'shapes': ['L_WristUp', 'L_WristDown', 'L_WristOut', 'L_WristIn'],
            'values': [90, -90, -90, 90],
            'attributes': ['L_Wrist_Jnt.rotateY', 'L_Wrist_Jnt.rotateY',
                           'L_Wrist_Jnt.rotateZ', 'L_Wrist_Jnt.rotateZ'],
            'driver_sdk': ['L_Wrist_Fk_Ctrl.rotateY', 'L_Wrist_Fk_Ctrl.rotateY',
                           'L_Wrist_Fk_Ctrl.rotateZ', 'L_Wrist_Fk_Ctrl.rotateZ'],
            'require_switch': ['L_Shoulder_Attrs_Ctrl.Switch_IK_FK', 1]
            },

    "Clavicle": {
            'driver': 'L_Clavicle_Ctrl',
             'bsp_name': 'ClavicleCorrectives',
             'shapes': ['L_ClavicleUp', 'L_ClavicleDown','L_ClavicleFront', 'L_ClavicleBack'],
             'values': [50, -50, 50, -50],
             'attributes': ['L_Clavicle_Ctrl.rotateY', 'L_Clavicle_Ctrl.rotateY',
                            'L_Clavicle_Ctrl.rotateZ', 'L_Clavicle_Ctrl.rotateZ'],
             'driver_sdk': ['L_Clavicle_Ctrl.rotateY', 'L_Clavicle_Ctrl.rotateY',
                            'L_Clavicle_Ctrl.rotateZ', 'L_Clavicle_Ctrl.rotateZ'],
             'require_switch': []
             },
    "Lips": {
        'driver': 'L_Lips_Main_Ctrl',
        'bsp_name': 'LipsCorrectives',
        'shapes': ['L_Commissure_Up', 'L_Commissure_Down', 'L_Commissure_Wide', 'L_Commissure_Narrow'],
        'values': [1, -1, 1, -1],
        'attributes': ['L_Lips_Main_Ctrl.ty', 'L_Lips_Main_Ctrl.ty',
                       'L_Lips_Main_Ctrl.tx', 'L_Lips_Main_Ctrl.tx'],
        'driver_sdk': ['L_Lips_Main_Ctrl.ty', 'L_Lips_Main_Ctrl.ty',
                       'L_Lips_Main_Ctrl.tx', 'L_Lips_Main_Ctrl.tx'],
        'require_switch': []
    },
}


class  BSP_Correctives(object):
    def __init__(self, geo=None, template=None):

        self.geo = geo
        self.template = template


    #-------------------------------------------------------

    def create_correctives(self, geo=None, template=None):
        if not template:
            template = self.template
        if not geo:
            geo = self.geo

        print(geo, template)

        if not cmds.objExists('Mutant_Correctives_Grp'):
            cmds.group(em=True, name='Mutant_Correctives_Grp')

        main_grp = cmds.group(em=True, name='{}_Grp'.format(template), p='Mutant_Correctives_Grp')

        for shape in correctives_templates[template]['shapes']:
            shape_geo = cmds.duplicate(geo, name=geo + '_' + shape)
            cmds.parent(shape_geo, main_grp)

    def connect_correctives(self, geo, blendshape_name, template=None, mirror=False):
        if not template:
            template = self.template

        print(geo, blendshape_name, template, mirror)

        values = correctives_templates[template]['values']
        attributes = correctives_templates[template]['attributes']
        shapes = correctives_templates[template]['shapes']
        driver_sdk = correctives_templates[template]['driver_sdk']
        require_switch = correctives_templates[template]['require_switch']


        print(geo, blendshape_name, template)
        print(values)
        print(attributes)
        print(driver_sdk)
        print(shapes)

        if mirror:
            r_attributes=[]
            for attr in attributes:
                r_attributes.append(attr.replace('L_', 'R_'))
            attributes = r_attributes

            r_driver_sdk = []
            for d in driver_sdk:
                r_driver_sdk.append(d.replace('L_', 'R_'))
            driver_sdk = r_driver_sdk

            r_shapes = []
            for s in shapes:
                r_shapes.append(s.replace('L_', 'R_'))
            shapes = r_shapes

            if require_switch:
                require_switch = [require_switch[0].replace('L_', 'R_'), require_switch[1]]

        if require_switch:
            print(require_switch)
            cmds.setAttr(require_switch[0], require_switch[1])

        for num, shape in enumerate(shapes):
            shape_name = blendshape_name + '.' + geo + '_' + shapes[num]

            cmds.setAttr(driver_sdk[num], 0)
            try:
                cmds.setAttr(shape_name, 0)
            except:
                shape_name = shape_name + 'Shape'
                cmds.setAttr(shape_name, 0)

            cmds.setDrivenKeyframe(shape_name, currentDriver=attributes[num])

            cmds.setAttr(driver_sdk[num], values[num])
            cmds.setAttr(shape_name, 1)
            cmds.setDrivenKeyframe(shape_name, currentDriver=attributes[num])

            cmds.setAttr(driver_sdk[num], 0)