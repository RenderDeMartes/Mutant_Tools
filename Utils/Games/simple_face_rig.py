from __future__ import absolute_import
"""
import Mutant_Tools
try:
	import importlib;from importlib import reload
except:
	import imp;from imp import reload

import Mutant_Tools.Utils.Games.simple_face_rig as simple_face_rig
reload(simple_face_rig)

cSimple_Face_Rig = simple_face_rig.Simple_Face_Rig()
cSimple_Face_Rig.initialize_joint_setup()

#-----------------------------------------
from maya import mel
mel.eval('file -f -options "v=0;"  -ignoreVersion  -typ "mayaAscii" -o "C:/Users/rodri/Documents/maya/2024/scripts/rigging/Mutant_Tools/Assets/GameFace.ma";{addRecentFile("C:/Users/rodri/Documents/maya/2024/scripts/rigging/Mutant_Tools/Assets/GameFace.ma", "mayaAscii");};')
import Mutant_Tools
try:
	import importlib;from importlib import reload
except:
	import imp;from imp import reload

import Mutant_Tools.Utils.Games.simple_face_rig as simple_face_rig
reload(simple_face_rig)

cSimple_Face_Rig = simple_face_rig.Simple_Face_Rig()
cSimple_Face_Rig.create_mouth_setup()




"""
import os
import json
from maya import cmds, mel


#Import Main Mutant Tools
import imp
from imp import reload
import Mutant_Tools
import Mutant_Tools.Utils
from Mutant_Tools.Utils.Rigging import main_mutant
reload(Mutant_Tools.Utils.Rigging.main_mutant)
mt = main_mutant.Mutant()

nc, curve_data, setup = mt.import_configs()

from Mutant_Tools.Utils.Helpers.decorators import undo


class Simple_Face_Rig(object):
    def __init__(self):

        self.head_ctrl = 'Head_Ctrl'
        mt.check_is_there_is_base()

    def initialize_joint_setup(self):
        json_file_path = os.path.join(os.path.dirname(__file__), 'maps', 'simple_face_joints.json')
        with open(json_file_path, 'r') as json_file:
            joint_data = json.load(json_file)

        created_joints = {}

        # Create joints based on the saved data
        for joint, values in joint_data.items():
            # Create the joint
            cmds.select(cl=True)
            new_joint = cmds.joint(n=joint)

            # Apply translation, rotation, and scale
            cmds.xform(new_joint, ws=True, t=values['translation'])
            cmds.xform(new_joint, ws=True, ro=values['rotation'])
            cmds.xform(new_joint, ws=True, s=values['scale'])

            # Save the joint with its new name
            created_joints[joint] = new_joint

        # Re-parent the joints based on the saved data
        for joint, values in joint_data.items():
            if values['parent']:
                cmds.parent(created_joints[joint], created_joints[values['parent']])

        return created_joints


    def get_null_joint(self):
        null_joint = 'Null_Joint'
        if cmds.objExists(null_joint):
            return null_joint
        else:
            cmds.select(cl=True)
            return cmds.joint(n=null_joint)

    def create_brows_setup(self):
        left_joints = ['L_Brow_01_Jnt', 'L_Brow_02_Jnt', 'L_Brow_03_Jnt', 'L_Brow_04_Jnt']
        right_joints = ['R_Brow_01_Jnt', 'R_Brow_02_Jnt', 'R_Brow_03_Jnt', 'R_Brow_04_Jnt']

        for joints in [left_joints, right_joints]:

            #Side settings
            if joints[0].startswith(nc['left']):
                side = nc['left']
            else:
                side = nc['right']

            if side.startswith(nc['right']):
                color = 'red'
            elif side.startswith(nc['left']):
                color = 'blue'
            else:
                color = 'yellow'

            # Get joint positions
            joint_1_pos = cmds.xform(joints[0], q=True, ws=True, t=True)
            joint_2_pos = cmds.xform(joints[1], q=True, ws=True, t=True)
            joint_3_pos = cmds.xform(joints[2], q=True, ws=True, t=True)
            joint_4_pos = cmds.xform(joints[3], q=True, ws=True, t=True)

            # Create the NURBS curve
            #curve = cmds.curve(degree=3, p=[joint_1, joint_3, joint_4])
            #cmds.nurbsCurveToBezier()

            curve_name = joints[0].replace('_01_Jnt', 'Bezier_Curve')
            if  joints[0].startswith(nc['left']):
                mel.eval('curve -d 3 -p 0.736928 178.330444 7.9697 -p 1.079595 178.324161 7.892957 -p 1.764928 178.311596 7.739471 -p 3.458646 178.571733 7.056967 -p 4.486387 178.594274 6.397035 -p 5.000257 178.605545 6.06707 -k 0 -k 0 -k 0 -k 1 -k 2 -k 3 -k 3 -k 3 -n "{}";'.format(curve_name))
            else:
                mel.eval('curve -d 3 -p -0.737042 178.330338 7.9697 -p -1.079667 178.323961 7.89281 -p -1.764919 178.311209 7.739029 -p -3.458052 178.571829 7.056408 -p -4.485808 178.594184 6.396859 -p -4.999686 178.605362 6.067084 -k 0 -k 0 -k 0 -k 1 -k 2 -k 3 -k 3 -k 3 -n "{}";'.format(curve_name))
            cmds.nurbsCurveToBezier()

            main_curve = curve_name

            #Position the curve
            all_temp_cls = []
            for num, cv in enumerate([0,3,6,9]):
                cmds.select(f"{main_curve}.cv[{cv}]")
                try:
                    cmds.select(f"{main_curve}.cv[{cv+1}]", add=True)
                except:
                    pass
                try:
                    cmds.select(f"{main_curve}.cv[{cv-1}]", add=True)
                except:
                    pass

                temp_cls = cmds.cluster()
                all_temp_cls.append(temp_cls)

                mt.match(temp_cls, joints[num])

            cmds.delete(main_curve, constructionHistory=True)

            #Add MotionPath Locators
            loc_grp = cmds.group(em=True, name=f"{side}Locators_Main{nc['group']}")
            motion_locators = []
            motion_locators_roots = []

            for num, joint in enumerate(joints):
                loc_name = joint.replace(nc['joint'], nc['locator'])
                loc = cmds.spaceLocator(n=loc_name)[0]
                motion_locators.append(loc)
                root = mt.root_grp()
                motion_locators_roots.append(root)

                motion_path = cmds.pathAnimation(root, main_curve)
                mel.eval('source generateChannelMenu.mel;')
                mel.eval("source channelBoxCommand;")
                mel.eval('CBdeleteConnection "{}.u"'.format(motion_path))

                cmds.setAttr(f"{motion_path}.uValue", num)

                cmds.parentConstraint(loc, joint, mo=True)
                cmds.parent(root, loc_grp)

            #Move Main Pivot to Center
            center = cmds.objectCenter(loc_grp, gl=True)
            cmds.xform(loc_grp, pivots=center)

            head_pos = cmds.xform('Head_Center_Jnt', q=True, ws=True, rp=True)
            current_pivot = cmds.xform(loc_grp, q=True, ws=True, rp=True)
            cmds.xform(loc_grp, ws=True, piv=[current_pivot[0], current_pivot[1], head_pos[2]])

            #Create joints to control the main curve
            driver_joints =[]
            for num, joint in enumerate(joints):
                if num == 0:
                    continue
                cmds.select(cl=True)
                print(joints[num])
                driver_joint = cmds.joint(n=joint.replace(nc['joint'], nc['joint_ctrl']))
                mt.match(driver_joint, joint)
                driver_joints.append(driver_joint)

            skin = cmds.skinCluster(driver_joints, main_curve, sm=0, bm=1, tsb=True)[0]
            cmds.skinPercent(skin, '{}.cv[0]'.format(main_curve), tv=[driver_joints[0], 1])

            #Constraint Orient to move locators rotations
            cmds.parentConstraint(driver_joints[0], motion_locators_roots[0], mo=True, skipTranslate=['x', 'y', 'z'])
            cmds.parentConstraint(driver_joints[0], motion_locators_roots[1], mo=True, skipTranslate=['x', 'y', 'z'])
            cmds.parentConstraint(driver_joints[1], motion_locators_roots[2], mo=True, skipTranslate=['x', 'y', 'z'])
            cmds.parentConstraint(driver_joints[2], motion_locators_roots[3], mo=True, skipTranslate=['x', 'y', 'z'])

            #Organize Driver Joints
            driver_joints_grp = cmds.group(driver_joints, n=f"{side}Driver_Joints{nc['group']}")
            driver_joints_root = cmds.group(driver_joints_grp, n=f"{side}Driver_Joints_Root{nc['group']}")
            cmds.xform(driver_joints_grp, ws=True, piv=[current_pivot[0], current_pivot[1], head_pos[2]])
            cmds.xform(driver_joints_root, ws=True, piv=[current_pivot[0], current_pivot[1], head_pos[2]])


            #Create Controllers
            size = mt.get_distance_between(joints[0], joints[-1])
            null_joint = self.get_null_joint()
            cmds.select(cl=True)
            main_ctrl = mt.curve(input=null_joint,
                            type='rectangle',
                            rename=True,
                            custom_name=True,
                            name=f"{side}Main_Brow{nc['ctrl']}",
                            size=1)
            mt.rotate_shape(main_ctrl, 90,0, 90)
            mt.assign_color(color=color)
            main_root_grp = mt.root_grp()[0]
            cmds.select(cl=True)
            first_ctrl = mt.curve(input=null_joint,
                                 type='circleDoublePointIn',
                                 rename=True,
                                 custom_name=True,
                                 name=f"{side}Brow_01{nc['ctrl']}",
                                 size=1)
            mt.rotate_shape(first_ctrl, 90, 0, 90)
            mt.scale_shape(first_ctrl, x=0.30, y=0.30, z=0.30)
            mt.assign_color(color=color)
            first_root_grp = mt.root_grp(first_ctrl)[0]
            cmds.select(cl=True)
            second_ctrl = mt.curve(input=null_joint,
                                  type='circleDoublePointIn',
                                  rename=True,
                                  custom_name=True,
                                  name=f"{side}Brow_02{nc['ctrl']}",
                                  size=1)
            mt.rotate_shape(second_ctrl, 90, 0, 90)
            mt.scale_shape(second_ctrl, x=0.30, y=0.30, z=0.30)
            mt.assign_color(color=color)
            second_root_grp = mt.root_grp(second_ctrl)[0]
            cmds.select(cl=True)
            third_ctrl = mt.curve(input=null_joint,
                                   type='circleDoublePointIn',
                                   rename=True,
                                   custom_name=True,
                                   name=f"{side}Brow_03{nc['ctrl']}",
                                   size=1)
            mt.rotate_shape(third_ctrl, 90, 0, 90)
            mt.scale_shape(third_ctrl, x=0.30, y=0.30, z=0.30)
            mt.assign_color(color=color)
            third_root_grp = mt.root_grp(third_ctrl)[0]

            cmds.parent(first_root_grp, second_root_grp, third_root_grp, main_ctrl)

            cmds.move(-0.66,0,0, first_root_grp)
            cmds.move(0.66,0,0, third_root_grp)

            mt.match(main_root_grp, 'L_Brow_03_Jnt')
            cmds.move(0,0,3, main_root_grp, r=True)

            if side == nc['right']:
                main_root_grp = mt.mirror_group(main_root_grp, world=True)

            #Parent to Head
            cmds.parentConstraint(self.head_ctrl, main_root_grp, mo=True)
            cmds.scaleConstraint(self.head_ctrl, main_root_grp, mo=True)

            #cmds.parentConstraint(self.head_ctrl, loc_grp, mo=True)
            #cmds.scaleConstraint(self.head_ctrl, loc_grp, mo=True)

            #cmds.parentConstraint(self.head_ctrl, driver_joints_root, mo=True)
            #cmds.scaleConstraint(self.head_ctrl, driver_joints_root, mo=True)

            cmds.parent(main_root_grp, self.head_ctrl)

            main_brow_grp = 'Brows_Rig{}'.format(nc['group'])
            if not cmds.objExists(main_brow_grp):
                clean_rig_grp = cmds.group(em=True, n=main_brow_grp)
                cmds.parent(clean_rig_grp, setup['rig_groups']['misc'] + nc['group'])

            else:
                clean_rig_grp = main_brow_grp

            cmds.parent(main_curve, loc_grp, driver_joints_root, clean_rig_grp)

            #Connect ctrls to main system
            main_place_loc = cmds.spaceLocator(n=main_ctrl.replace(nc['ctrl'], '_PlaceLoc'))[0]
            main_place_loc_root = mt.root_grp()
            mt.match(main_place_loc_root, 'L_Main_Brow_Ctrl')
            mt.match(main_place_loc_root, 'L_Driver_Joints_Root_Grp', r=False)

            if side == nc['right']:
                main_place_loc_root = mt.mirror_group(main_place_loc_root, world=True)
            cmds.parentConstraint(main_place_loc, driver_joints_grp, mo=True)

            for attr in ['r', 't', 's']:
                cmds.connectAttr(f'{main_ctrl}.{attr}', f'{main_place_loc}.{attr}')

            cmds.parentConstraint(self.head_ctrl, main_place_loc_root, mo=True)
            cmds.scaleConstraint(self.head_ctrl, main_place_loc_root, mo=True)
            cmds.parent(main_place_loc_root, clean_rig_grp)

            #Connect sub ctrls
            driver_joints = ['L_Brow_02_JntCtrl','L_Brow_03_JntCtrl','L_Brow_04_JntCtrl']
            brow_ctrls = [first_ctrl, second_ctrl, third_ctrl]

            for jnt, ctrl in zip(driver_joints, brow_ctrls):
                loc = cmds.spaceLocator(n=ctrl.replace(nc['ctrl'], '_PlaceLoc'))[0]
                loc_root = mt.root_grp()
                mt.match(loc_root, jnt)

                if side == nc['right']:
                    loc_root = mt.mirror_group(loc_root, world=True)
                    cmds.parentConstraint(loc, jnt.replace(nc['left'], nc['right']), mo=True)
                else:
                    cmds.parentConstraint(loc,  jnt, mo=True)

                cmds.parent(loc_root, main_place_loc)

                for attr in ['r', 't']:
                    cmds.connectAttr(f'{ctrl}.{attr}', f'{loc}.{attr}')

            cmds.scaleConstraint(first_ctrl, joints[0], mo=True)
            cmds.scaleConstraint(first_ctrl, joints[1], mo=True)
            cmds.scaleConstraint(second_ctrl, joints[2], mo=True)
            cmds.scaleConstraint(third_ctrl, joints[3], mo=True)


    def create_eyes_setup(self):

        name = 'Eyes'

        eyes_pivot = ['L_Eye_Pivot_Jnt', 'R_Eye_Pivot_Jnt']
        left_eye_joints = ['L_Eye_Inner_Corner_Jnt', 'L_Up_Eye_Inner_Jnt','L_Up_Eye_Jnt','L_Up_Eye_Outter_Jnt',
                           'L_Eye_Outter_Corner_Jnt','L_Dw_Eye_Outter_Jnt','L_Dw_Eye_Jnt','L_Dw_Eye_Inner_Jnt']

        #Clean grps
        clean_ctrl_grp = cmds.group(em=True, name=name + nc['ctrl'] + nc['group'])
        clean_rig_grp = cmds.group(em=True, name=name + '_FaceRig' + nc['group'])

        cmds.parent(clean_rig_grp, '{}{}'.format(setup['rig_groups']['misc'], nc['group']))
        cmds.parent(clean_ctrl_grp, setup['base_groups']['control'] + nc['group'])

        for side in [nc['left'], nc['right']]:
            if side == nc['right']:
                pivot = eyes_pivot[-1]
                eye_joints = []
                for jnt in left_eye_joints:
                    eye_joints.append(jnt.replace(nc['left'], nc['right']))

            else:
                pivot = eyes_pivot[0]
                eye_joints = left_eye_joints

            print(pivot, eye_joints)

            # Crete blink controllers
            name = f'{side}Eyes'
            if side.startswith(nc['right']):
                color = 'red'
            elif side.startswith(nc['left']):
                color = 'blue'
            else:
                color = 'yellow'
            ctrl_size = 1
            limit_ctrls = True
            rectangle, upr_triangle, lwr_triangle = create_eye_blink_slider(name, color, ctrl_size, limit=limit_ctrls)
            rectangle_root = cmds.listRelatives(rectangle, p=True)[0]
            cmds.delete(cmds.pointConstraint(eye_joints[4], rectangle_root))
            cmds.move(0, 0, ctrl_size * 2, rectangle_root, r=True)
            cmds.parentConstraint(pivot, rectangle_root, mo=True)
            cmds.scaleConstraint(pivot, rectangle_root, mo=True)

            #Create IKs
            ik_handles = []
            ik_grp = cmds.group(n=f"{side}IK_Eyes_Grp", em=True)
            cmds.parent(ik_grp, clean_rig_grp)

            cmds.parentConstraint(pivot, ik_grp, mo=True)
            cmds.scaleConstraint(pivot, ik_grp, mo=True)

            # Joints for blink (separated into Up and Dw)
            up_joints = [
                'L_Up_Eye_Inner_Jnt',
                'L_Up_Eye_Jnt',
                'L_Up_Eye_Outter_Jnt'
            ]

            dw_joints = [
                'L_Dw_Eye_Inner_Jnt',
                'L_Dw_Eye_Jnt',
                'L_Dw_Eye_Outter_Jnt'
            ]

            up_joints_values = {
                'L_Up_Eye_Inner_Jnt':-0.5,
                'L_Up_Eye_Jnt':-0.75,
                'L_Up_Eye_Outter_Jnt':-0.5
            }

            dw_joints_values = {
                'L_Dw_Eye_Inner_Jnt':0.5,
                'L_Dw_Eye_Jnt':0.75,
                'L_Dw_Eye_Outter_Jnt':0.5
            }

            # If side is 'R_', replace 'L_' with 'R_' in joint names
            if side == 'R_':
                up_joints = [joint.replace('L_', 'R_') for joint in up_joints]
                dw_joints = [joint.replace('L_', 'R_') for joint in dw_joints]

                # Update values dictionaries to replace 'L_' with 'R_' in the keys
                up_joints_values = {joint.replace('L_', 'R_'): value for joint, value in up_joints_values.items()}
                dw_joints_values = {joint.replace('L_', 'R_'): value for joint, value in dw_joints_values.items()}

            print("Upper joints:", up_joints)
            print("Upper joint values:", up_joints_values)
            print("Lower joints:", dw_joints)
            print("Lower joint values:", dw_joints_values)


            for jnt in eye_joints:
                cmds.select(cl=True)
                sys_piv_joint = cmds.joint(n=jnt.replace('_Jnt', '_PivSysJnt'))
                driver_jnt = cmds.joint(n=jnt.replace('_Jnt', '_SysJnt'))

                mt.match(sys_piv_joint, pivot)
                mt.match(driver_jnt, jnt)

                cmds.parentConstraint(pivot, sys_piv_joint, mo=True)
                cmds.parent(sys_piv_joint, clean_rig_grp)

                #Create Ik Handle
                # create Ik Chain
                ik_handle = cmds.ikHandle(n='{}{}'.format(jnt.replace(nc['joint'], ''), nc['ik_sc']),
                                          sj=sys_piv_joint, ee=driver_jnt, sol='ikSCsolver')
                cmds.rename(ik_handle[1], '{}{}'.format(driver_jnt, nc['effector']))
                ik_handle = ik_handle[0]
                ik_handles.append(ik_handle)
                cmds.parentConstraint(driver_jnt, jnt)
                root, auto = mt.root_grp(input=ik_handle, autoRoot=True)
                cmds.parent(root, ik_grp)



                if jnt in up_joints or jnt in dw_joints:
                    if jnt in up_joints:
                        blink_ctrl = upr_triangle
                        value = up_joints_values[jnt]
                    else:
                        blink_ctrl = lwr_triangle
                        value = dw_joints_values[jnt]

                    if side == 'R_':
                        value = value*-1

                    #move the Iks with the ctrl * attr
                    mult_attr =  mt.new_attr(input= rectangle,
                                        name = jnt.replace(nc['joint'], ''),
                                        min = -100 ,
                                        max = 100,
                                        default = value)
                    md = mt.connect_md_node(in_x1=mult_attr, in_x2=f"{blink_ctrl}.ty", out_x=f"{auto}.translateY", mode='multiply')

            # mid_pos = []
            # mid_locator = cmds.spaceLocator(n=f"{side}MidPos_Eyes_Loc")[0]
            # cmds.delete(cmds.parentConstraint(eye_joints[0], eye_joints[4], mid_locator))

            #Clean a bit
            clean_ctrl_grp = cmds.group(em=True, name=name + nc['ctrl'] + nc['group'])
            clean_rig_grp = cmds.group(em=True, name=name + '_Rig' + nc['group'])

            cmds.parent(clean_rig_grp, '{}{}'.format(setup['rig_groups']['misc'], nc['group']))
            cmds.parent(clean_ctrl_grp, setup['base_groups']['control'] + nc['group'])

            cmds.parent(rectangle_root, clean_ctrl_grp)

    def create_mouth_setup(self):
        ''


#--------------------------------------
#--------------------------------------
#--------------------------------------
#--------------------------------------
def create_eye_blink_slider(name, color, ctrl_size, limit=True):

    nc, curve_data, setup = mt.import_configs()

    cmds.select(cl=True)

    ctrl_size=ctrl_size
    blink_rectangle = mt.curve(input='',
                               type='rectangle',
                               rename=True,
                               custom_name=True,
                               name=name + '_BlinkAttrs' + nc['ctrl'],
                               size=1.5)
    mt.assign_color(color=color)
    blink_rectangle_root=mt.root_grp()[0]
    cmds.rotate(90,0,0)
    mt.hide_attr(input=blink_rectangle, t=True, r=True, s=True, v=False, rotate_order=True)

    upr_blink_triangle = mt.curve(input='',
                                  type='triangle',
                                  rename=True,
                                  custom_name=True,
                                  name=name + 'UprBlink' + nc['ctrl'],
                                  size=1)
    cmds.rotate(-90, 0, 0)
    mt.assign_color(color=color)
    upr_blink_triangle_root = mt.root_grp()[0]
    cmds.setAttr(upr_blink_triangle_root + '.scaleZ', 0.5)
    cmds.setAttr(upr_blink_triangle_root + '.translateY', 1)
    cmds.makeIdentity(upr_blink_triangle, apply=True, rotate=True, translate=True, scale=True)
    cmds.makeIdentity(upr_blink_triangle_root, apply=True, rotate=True, translate=True, scale=True)
    cmds.setAttr(upr_blink_triangle_root + '.rotateZ', 180)
    cmds.setAttr(upr_blink_triangle_root + '.scaleX', 0.75)
    cmds.setAttr(upr_blink_triangle_root + '.scaleY', 0.75)
    cmds.setAttr(upr_blink_triangle_root + '.scaleZ', 0.75)
    mt.hide_attr(input=upr_blink_triangle, t=False, r=True, s=True, v=True, rotate_order=True, show=False)
    cmds.setAttr('{}.translateZ'.format(upr_blink_triangle), lock=True, keyable=False, channelBox=False)
    cmds.setAttr('{}.translateX'.format(upr_blink_triangle), lock=True, keyable=False, channelBox=False)
    if limit:
        cmds.transformLimits(upr_blink_triangle, ety=[True, True], ty=[0, 1])

    lwr_blink_triangle = mt.curve(input='',
                                  type='triangle',
                                  rename=True,
                                  custom_name=True,
                                  name=name + 'LwrBlink' + nc['ctrl'],
                                  size=1)
    cmds.rotate(-90,0,0)
    mt.assign_color(color=color)
    lwr_blink_triangle_root = mt.root_grp()[0]
    cmds.setAttr(lwr_blink_triangle_root + '.scaleZ', 0.5)
    cmds.setAttr(lwr_blink_triangle_root + '.translateY', -1)
    cmds.makeIdentity(lwr_blink_triangle, apply=True, rotate=True, translate=True, scale=True)
    cmds.makeIdentity(lwr_blink_triangle_root, apply=True, rotate=True, translate=True, scale=True)
    cmds.setAttr(lwr_blink_triangle_root + '.scaleX', 0.75)
    cmds.setAttr(lwr_blink_triangle_root + '.scaleY', 0.75)
    cmds.setAttr(lwr_blink_triangle_root + '.scaleZ', 0.75)
    mt.hide_attr(input=lwr_blink_triangle, t= False, r = True, s = True, v = True, rotate_order = True, show = False)
    if limit:
        cmds.transformLimits(lwr_blink_triangle, ety=[True, True], ty=[0, 1])
    cmds.setAttr('{}.translateZ'.format(lwr_blink_triangle), lock=True, keyable=False, channelBox=False)
    cmds.setAttr('{}.translateX'.format(lwr_blink_triangle), lock=True, keyable=False, channelBox=False)

    cmds.parent(lwr_blink_triangle_root, upr_blink_triangle_root, blink_rectangle)

    cmds.scale(1,1,1, blink_rectangle_root)

    return [blink_rectangle, upr_blink_triangle, lwr_blink_triangle]