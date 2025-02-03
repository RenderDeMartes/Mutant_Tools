from __future__ import absolute_import
from maya import cmds
try:
    import importlib;from importlib import reload
except:
    import imp;from imp import reload

from collections import OrderedDict
from Mutant_Tools.UI.RigTools.Tabs import load_CtrlsTab
reload(load_CtrlsTab)
import Mutant_Tools
import Mutant_Tools.Utils.Rigging
from Mutant_Tools.Utils.Rigging import main_mutant

import maya.mel as mel

mt = main_mutant.Mutant()
nc, curve_data, setup = mt.import_configs()		

class PushSystem(object):

    """
    Class representing a push system for rigging in Maya.

    Attributes:
        sides (list): List of sides for the push system.
        original_joint (str): Original joint associated with the push system.
        section (str): Section identifier for the push system.
        templateA (str): Name of the first template joint.
        templateB (str): Name of the second template joint.
        templateC (str): Name of the third template joint.
        vis_Ctrl (OrderedDict): Dictionary mapping joint names to visibility control names.

    Methods:
        create_push_joints(section=None, source=None, side=['N']): Create push system joints.
        identify_push_joints(section=None, source=None, side=['N']): Identify push system joints.
        create_push_system(block=False): Create the entire push system.

    Examples:
        >>> push_system = PushSystem()
        >>> push_system.create_push_joints(source='L_Knee_Bnd_0_Bnd', side='front')
        'L_Knee_Bnd_0_Bnd_Corrective_A_Jnt'
        >>> push_system.create_push_system()
        'Build Push System Success'
    """

    def __init__(self):
        super(PushSystem, self).__init__()
        self.sides = None
        self.original_joint = None
        self.section = None
        self.templateA = None
        self.templateB = None
        self.templateC = None

        self.vis_Ctrl = OrderedDict({'L_Clavicle_Bnd' :'L_Clavicle_Ctrl', 
                                    'R_Clavicle_Bnd':'R_Clavicle_Ctrl',
                                    'L_Elbow_Bnd_0_Bnd' :'L_Shoulder_Jnt_Switch_Loc', 
                                    'R_Elbow_Bnd_0_Bnd':'R_Shoulder_Jnt_Switch_Loc',
                                    'L_Hip_Bnd_0_Bnd' :'L_Pelvis_Ctrl', 
                                    'R_Hip_Bnd_0_Bnd':'R_Pelvis_Ctrl'})

    def create_push_joints(self, section=None, source=None, side=['N']):

        """
        Create push system joints.

        Args:
            section (str): Section identifier for the push system.
            source (str): Original joint associated with the push system.
            side (list): List of sides for the push system.

        Returns:
            str: Name of the first template joint.

        Example:
            >>> push_system = PushSystem()
            >>> push_system.create_push_joints(source='L_Knee_Bnd_0_Bnd', side='front')
            'L_Knee_Bnd_0_Bnd_Corrective_A_Jnt'
        """
     
        cmds.select(clear=True)
        self.sides =  [side[0]]
        if not source and not section:
            cmds.warning('{} does not exist, try with another joint.'.format(source))
            return 
        #this else is extra, could be edited
        else: 
            self.original_joint = source
            
            #adding this section attribute to make it block compatible
            if section:
                self.section = '{}_{}'.format(section, side[0])
                suffix = 'Guide'
            else: 
                self.section = '{}_{}'.format(source.split('_Bnd')[0], side[0])
                suffix = 'Jnt'
            self.templateA = cmds.joint(n='{}_Corrective_A_{}'.format(self.section, suffix))
            self.templateB = cmds.joint(n='{}_Corrective_B_{}'.format(self.section, suffix))
            self.templateC = cmds.joint(n='{}_Corrective_C_{}'.format(self.section, suffix))
            
            if source:
                cmds.matchTransform(self.templateA, source)
                cmds.matchTransform(self.templateB, source)
                cmds.matchTransform(self.templateC, source)

            cmds.select(clear=True)
        return self.templateA

    def identify_push_joints(self, section=None, source=None, side=['N']):

        """
        Identify push system joints.

        Args:
            section (str): Section identifier for the push system.
            source (str): Original joint associated with the push system.
            side (list): List of sides for the push system.

        Returns:
            None

        Example:
            >>> push_system = PushSystem()
            >>> push_system.identify_push_joints(source='L_Knee_Bnd_0_Bnd', side='front')
        """

        try:
           if not source:
              cmds.warning('{} does not exist, try with another joint.'.format(source))
              return 
           print(side)
           self.sides = [side[0]]
           self.original_joint = source
           if section:
               self.section = '{}_{}'.format(section, side[0])
               suffix = 'Jnt'
           else: 
               self.section = '{}_{}'.format(source.split('_Bnd')[0], side[0])
               suffix = 'Jnt'
           self.templateA = '{}_Corrective_A_{}'.format(self.section, suffix)
           self.templateB = '{}_Corrective_B_{}'.format(self.section, suffix)
           self.templateC = '{}_Corrective_C_{}'.format(self.section, suffix)
        except:
            cmds.warning('Could not find the joints asssociated with {}_{}'.format(source, side))

    def create_push_system(self, block=False):

        """
        Create the entire push system.

        Args:
            block (bool): Flag indicating whether to create the push system as a block.

        Returns:
            str: Success message.

        Example:
            >>> push_system = PushSystem()
            >>> push_system.create_push_system()
            'Build Push System Success'
        """

        #cmds.select(clear=True)
        print(self.sides)
        for side in self.sides:
            joint_checkList = [self.templateA, self.templateB, self.templateC]
            for check in joint_checkList:
                if not cmds.objExists(check):
                    cmds.warning('{} does not exist, try with another joint before bouilding.'.format(check))
                    return 
                    
            #Groups and cleanups
            zero_grp = cmds.group(n='{}_Push_Zero_Grp'.format(self.section), w=True, em=True)
            main_grp = cmds.group(n='{}_Push_Grp'.format(self.section), w=True, em=True)
            #cmds.parent(self.templateA, zero_grp)
            cmds.parent(zero_grp, main_grp)
            cmds.matchTransform(main_grp, self.templateB)
            cmds.parent(self.templateA, '{}_Push_Zero_Grp'.format(self.section))
            
            #controls
            created_ctrls = []
            for joint in joint_checkList:
                ctrl = mt.curve(input=joint,
                    type='sphere',
                    rename=True,
                    custom_name=True,
                    name=joint.replace(nc['joint'], nc['ctrl']),
                    size=1.6)
                #mt.assign_color(color=color)
                root_grp = mt.root_grp()[0]
                mt.match(root_grp, joint, r=True, t=True)
                cmds.parentConstraint(ctrl, joint, mo=True)
                created_ctrls.append(ctrl)

                cmds.select(ctrl)
                mel.eval('TagAsController;')

            cmds.parent(self.templateC.replace('Jnt', 'Ctrl_Offset_Grp'), self.templateB.replace('Jnt', 'Ctrl'))
            cmds.parent(self.templateB.replace('Jnt', 'Ctrl_Offset_Grp'), self.templateA.replace('Jnt', 'Ctrl'))

            cmds.select(clear=True)

            zero_ctrl_grp = cmds.group(n='{}_Ctrl_Push_Zero_Grp'.format(self.section), w=True, em=True)
            main_ctrl_grp = cmds.group(n='{}_Ctrl_Push_Grp'.format(self.section), w=True, em=True)
            offset_main_ctrl_grp = cmds.group(n='{}_Offset_Ctrl_Push_Grp'.format(self.section), w=True, em=True)
            
            cmds.parent(zero_ctrl_grp, main_ctrl_grp, r=True)
            cmds.parent(main_ctrl_grp, offset_main_ctrl_grp, r=True)
            
            cmds.matchTransform(offset_main_ctrl_grp, self.templateA)
            cmds.matchTransform(main_ctrl_grp, self.templateB)
            
            cmds.parent(self.templateA.replace('Jnt', 'Ctrl_Offset_Grp'), zero_ctrl_grp, r=True)
            cmds.matchTransform(self.templateA.replace('Jnt', 'Ctrl_Offset_Grp'), offset_main_ctrl_grp)

            #Shared node
            if created_ctrls:
            # CREATE LOCATOR WITH FIRST SELECTION AS PARENT AND TOGGLE VISIBILITY
               nuShape = cmds.createNode('locator', name = '{}_options'.format(self.section), parent = created_ctrls[0])
               cmds.setAttr('{0}.visibility'.format(nuShape), 0)
            # LOCKS AND HIDES IT'S ATTRIBUTES
               cmds.setAttr('{0}.lpx'.format(nuShape), k=0, cb=0)
               cmds.setAttr('{0}.lpy'.format(nuShape), k=0, cb=0)
               cmds.setAttr('{0}.lpz'.format(nuShape), k=0, cb=0)
               cmds.setAttr('{0}.lsx'.format(nuShape), k=0, cb=0)
               cmds.setAttr('{0}.lsy'.format(nuShape), k=0, cb=0)
               cmds.setAttr('{0}.lsz'.format(nuShape), k=0, cb=0)
            for item in created_ctrls[1:]:
               cmds.parent( nuShape, item, shape = True, addObject = True)
            if not created_ctrls:
               LOG.fatal("Please select controllers or objects first.")

            #Locators
            locator_translate = cmds.spaceLocator(n='{}_Translate_Loc'.format(self.section))
            locator_rotate = cmds.spaceLocator(n='{}_Rotate_Loc'.format(self.section))
            cmds.matchTransform(locator_translate, self.templateB)
            cmds.matchTransform(locator_rotate, self.templateC)
            cmds.parent(locator_rotate, locator_translate)
            cmds.parent(locator_translate, main_grp)
            
            #Loc Parent constraints 
            #TODO Potential problem here if the initial joint isnt named 
            if 'Clavicle' in self.original_joint:
                parent_joint = 'Spine_End_Bnd'
            else:
                try:
                    parent_joint = cmds.listRelatives(self.original_joint, parent=True, type='joint')
                except: 
                    cmds.warning('Parent joint may not exist, setting Spine_End_Bnd as default parent')
                    parent_joint = 'Spine_End_Bnd'
            cmds.parentConstraint(parent_joint, self.original_joint, locator_translate, mo=True, sr=['x','y','z'])
            cmds.parentConstraint(parent_joint, self.original_joint, locator_rotate, mo=True, sr=['x','y','z'])
            
            #nodes
            vp_position_normal_node = cmds.createNode("vectorProduct", n='{}_Position_normal_vp'.format(self.section))
            vp_normal_node = cmds.createNode("vectorProduct", n='{}_normal_vp'.format(self.section))
            cmds.setAttr(vp_position_normal_node + ".operation", 1)
            cmds.setAttr(vp_normal_node + ".operation", 1)
            
            cmds.connectAttr('{}.translate'.format(locator_translate[0]), '{}.input1'.format(vp_position_normal_node))
            cmds.connectAttr('{}.translate'.format(locator_rotate[0]), '{}.input2'.format(vp_position_normal_node))
            cmds.connectAttr('{}.translate'.format(locator_rotate[0]), '{}.input2'.format(vp_normal_node))
            cmds.setAttr(vp_normal_node + ".input1X", 1) #THIS IS WHERE THE DIRECTION IS? 
            
            md_intersection_node = cmds.createNode("multiplyDivide", n='{}_intersection_md'.format(self.section))
            cmds.setAttr(md_intersection_node + ".operation", 2)
            cmds.connectAttr('{}.output'.format(vp_position_normal_node), '{}.input1'.format(md_intersection_node))
            cmds.connectAttr('{}.output'.format(vp_normal_node),'{}.input2'.format(md_intersection_node))

            condition_node = cmds.createNode("condition", n='{}_condition'.format(self.section))
            inverted_directions = ['R_Clavicle', 'R_Shoulder', 'R_Elbow', 'R_Hand']
            for inverted_direction in inverted_directions:
                if inverted_direction in self.section:
                    cmds.setAttr(condition_node + ".operation", 2)
                else:
                    cmds.setAttr(condition_node + ".operation", 4)

            cmds.setAttr(condition_node + ".colorIfFalseR", cmds.getAttr(md_intersection_node + ".outputX"))
            cmds.setAttr(condition_node + ".colorIfFalseG", cmds.getAttr(md_intersection_node + ".outputX"))
            cmds.setAttr(condition_node + ".colorIfFalseB", cmds.getAttr(md_intersection_node + ".outputX"))
            cmds.setAttr(condition_node + ".secondTerm", cmds.getAttr(md_intersection_node + ".outputX"))
            cmds.connectAttr('{}.output'.format(md_intersection_node), '{}.colorIfTrue'.format(condition_node))
            cmds.connectAttr('{}.outputX'.format(md_intersection_node), '{}.firstTerm'.format(condition_node))
            
            bc_clamp_node = cmds.createNode("blendColors", n='{}_clamp_bc'.format(self.section))
            cmds.connectAttr('{}.output'.format(md_intersection_node), '{}.color2'.format(bc_clamp_node))
            cmds.connectAttr('{}.outColor'.format(condition_node),'{}.color1'.format(bc_clamp_node))
            
            md_distance_node = cmds.createNode("multiplyDivide", n='{}_distance_md'.format(self.section))
            cmds.setAttr(md_distance_node + ".operation", 1)
            cmds.connectAttr('{}.output'.format(bc_clamp_node), '{}.input2'.format(md_distance_node))
            cmds.setAttr(md_distance_node + ".input1X", 1) #THIS IS WHERE THE DIRECTION IS? 
            
            #cmds.connectAttr('{}.output'.format(md_distance_node),'{}.translate'.format(zero_grp))
            cmds.connectAttr('{}.output'.format(md_distance_node),'{}.translate'.format(zero_ctrl_grp))
            
            cmds.orientConstraint(self.original_joint, self.templateB.replace('Jnt', 'Ctrl_Offset_Grp'), mo=True)
            cmds.parentConstraint(parent_joint, main_grp, mo=True)
            cmds.parentConstraint(parent_joint, main_ctrl_grp, mo=True)
 
            #shared node attributes
            cmds.addAttr('{}_options'.format(self.section), 
                                            longName='Clamp', 
                                            at='float', 
                                            max=1, 
                                            min=0,
                                            dv=1,
                                            k=True,
                                            h=False)
            cmds.connectAttr('{}_options.{}'.format(self.section, 'Clamp'), 
                            '{}.blender'.format(bc_clamp_node))

            cmds.addAttr('{}_options'.format(self.section), 
                                            longName='MultiplyFactorY', 
                                            at='float', 
                                            dv=0,
                                            k=True,
                                            h=False)
            cmds.connectAttr('{}_options.{}'.format(self.section, 'MultiplyFactorY'), 
                            '{}.input1Y'.format(md_distance_node))
            cmds.addAttr('{}_options'.format(self.section), 
                                            longName='MultiplyFactorZ', 
                                            at='float', 
                                            dv=0,
                                            k=True,
                                            h=False)
            cmds.connectAttr('{}_options.{}'.format(self.section, 'MultiplyFactorZ'), 
                            '{}.input1Z'.format(md_distance_node))
            cmds.addAttr('{}_options'.format(self.section), 
                                            longName='MultiplyFactor', 
                                            at='float', 
                                            dv=1,
                                            k=True,
                                            h=False)
            cmds.connectAttr('{}_options.{}'.format(self.section, 'MultiplyFactor'), 
                            '{}.input1X'.format(md_distance_node))
            cmds.addAttr('{}_options'.format(self.section), 
                                            longName='ExtraControlVisibility', 
                                            at='bool', 
                                            dv=False,
                                            k=True,
                                            h=False)
            cmds.connectAttr('{}_options.{}'.format(self.section, 'ExtraControlVisibility'), 
                            '{}Shape.visibility'.format(self.templateA.replace(nc['joint'], nc['ctrl'])))
            cmds.connectAttr('{}_options.{}'.format(self.section, 'ExtraControlVisibility'), 
                            '{}Shape.visibility'.format(self.templateC.replace(nc['joint'], nc['ctrl'])))

            #System visibility 
            if self.original_joint in self.vis_Ctrl:
                system_visibility_target = self.vis_Ctrl[self.original_joint]
            else:
                system_visibility_target = 'Global_Ctrl'

            if cmds.attributeQuery('PushSystemVisibility', node=system_visibility_target, exists=True):
                cmds.connectAttr('{}.{}'.format(system_visibility_target, 'PushSystemVisibility'), 
                            '{}.visibility'.format(offset_main_ctrl_grp))
            else:
                cmds.addAttr('{}'.format(system_visibility_target), 
                                                longName='PushSystemVisibility', 
                                                at='bool', 
                                                dv=True,
                                                k=True,
                                                h=False)
                cmds.connectAttr('{}.{}'.format(system_visibility_target, 'PushSystemVisibility'), 
                                '{}.visibility'.format(offset_main_ctrl_grp))

            #final parents
            if not block:
                if cmds.objExists('PushCorrectives_Rig_Grp'):
                    cmds.parent(main_grp, 'PushCorrectives_Rig_Grp')
                else: 
                    cmds.group(n='PushCorrectives_Rig_Grp', w=True, em=True)
                    cmds.parent(main_grp, 'PushCorrectives_Rig_Grp')
                    cmds.parent('PushCorrectives_Rig_Grp', 'Bind_Joints_Grp')

                if cmds.objExists('PushCorrectives_Ctrl_Grp'):
                    cmds.parent(offset_main_ctrl_grp, 'PushCorrectives_Ctrl_Grp')
                else: 
                    cmds.group(n='PushCorrectives_Ctrl_Grp', w=True, em=True)
                    cmds.parent(offset_main_ctrl_grp, 'PushCorrectives_Ctrl_Grp')
                    cmds.parent('PushCorrectives_Ctrl_Grp', 'Global_Ctrl_Offset_Grp')

