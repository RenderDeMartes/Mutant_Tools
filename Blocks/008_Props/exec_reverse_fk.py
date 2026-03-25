from __future__ import absolute_import
from maya import cmds
import json
try:
    import importlib;from importlib import reload
except:
    import imp;from imp import reload
import os
from pathlib import Path
import string

import Mutant_Tools
import Mutant_Tools.Utils.Rigging
from Mutant_Tools.Utils.Rigging import main_mutant
reload(Mutant_Tools.Utils.Rigging.main_mutant)

mt = main_mutant.Mutant()

#---------------------------------------------

TAB_FOLDER = '008_Props'
PYBLOCK_NAME = 'exec_reverse_fk'

#---------------------------------------------

def create_reverse_fk_block(name = 'BidirectionalChain'):
    """
    Create guides for a bidirectional FK chain (forward and reverse capable)
    """
    
    letters = string.ascii_uppercase
    
    PATH = os.path.dirname(__file__)
    PATH = Path(PATH)
    PATH_PARTS = PATH.parts[:-2]
    FOLDER = ''
    for f in PATH_PARTS:
        FOLDER = os.path.join(FOLDER, f)
    
    MODULE_FILE = os.path.join(os.path.dirname(__file__), '11_ReverseFk.json')
    with open(MODULE_FILE) as module_file:
        module = json.load(module_file)
    
    nc, curve_data, setup = mt.import_configs()
    
    # Name checks and block creation
    name = mt.ask_name(text = module['Name'])
    if cmds.objExists('{}{}'.format(name, nc['module'])):
        cmds.warning('Name already exists.')
        return ''
    
    amount = mt.ask_name(ask_for='Amount of Joints', text='5')
    
    block = mt.create_block(name = name, icon = 'Chain', attrs = module['attrs'], 
                           build_command = module['build_command'], 
                           import_command = module['import'])
    config = block[1]
    block = block[0]
    
    cmds.select(cl=True)
    
    joints = []
    jnt = None
    for i in range(int(amount)):
        parent = jnt
        jnt = mt.create_joint_guide(name=name + '_' + letters[i])
        cmds.move(i, 0, 0)
        if parent:
            cmds.parent(jnt, parent)
        joints.append(jnt)
    
    cmds.parent(joints[0], block)
    cmds.select(block)
    
    print('{} Reverse FK Created Successfully'.format(name))

#---------------------------------------------

def build_reverse_fk_block():
    """
    Build bidirectional FK chain with forward and reverse controls
    Joints are constrained to BOTH FK systems with blendable weights
    Direction is always BOTH for simultaneous control
    """
    
    print('Start of build reverse FK func')
    
    nc, curve_data, setup = mt.import_configs()
    
    mt.check_is_there_is_base()
    
    block = cmds.ls(sl=True)
    config = cmds.listConnections(block)[1]
    block = block[0]
    guides = cmds.listRelatives(block, c=True)
    name = block.replace(nc['module'], '')
    
    # Main groups
    clean_ctrl_grp = cmds.group(em=True, name=name + nc['ctrl'] + nc['group'])
    clean_rig_grp = cmds.group(em=True, name=name + '_Rig' + nc['group'])
    
    cmds.parent(clean_rig_grp, '{}{}'.format(setup['rig_groups']['misc'], nc['group']))
    cmds.parent(clean_ctrl_grp, setup['base_groups']['control'] + nc['group'])
    
    # Process each guide hierarchy
    for guide in guides:
        
        new_guide = mt.duplicate_and_remove_guides(guide)
        guide_childs = cmds.listRelatives(new_guide, ad=True)
        if guide_childs:
            all_guides = [new_guide] + guide_childs
        else:
            all_guides = [new_guide]
        
        if not new_guide.startswith(nc['left']) and cmds.getAttr('{}.Mirror'.format(config)):
            name = nc['left'] + name
            new_guide = nc['left'] + new_guide
            for guide in all_guides:
                guide = cmds.rename(guide, nc['left'] + guide)
        
        to_build = [new_guide]
        mirror = cmds.getAttr('{}.Mirror'.format(config))
        
        if mirror:
            right_guide = mt.duplicate_change_names(input=new_guide, hi=True, 
                                                   search=nc['left'], replace=nc['right'])[0]
            to_build.append(right_guide)
        
        for guide_root in to_build:
            guide_childs_build = cmds.listRelatives(guide_root, ad=True)
            if guide_childs_build:
                guide_hierarchy = [guide_root] + list(reversed(guide_childs_build))
            else:
                guide_hierarchy = [guide_root]
            
            is_right_side = guide_root.startswith(nc['right'])
            color = cmds.getAttr('{}.CtrlColor'.format(config), asString=True)
            
            if mirror:
                if guide_root.startswith(nc['left']):
                    color = setup['left_color']
                elif is_right_side:
                    color = setup['right_color']
            
            # ===== FORWARD FK SYSTEM (using mt.fk_chain) =====
            cmds.select(guide_hierarchy)
            fk_forward_ctrls = mt.fk_chain(input='',
                                    size=cmds.getAttr('{}.CtrlSize'.format(config)),
                                    color=color,
                                    curve_type=cmds.getAttr('{}.CtrlType'.format(config), asString=True),
                                    scale=True,
                                    twist_axis=cmds.getAttr('{}.TwistAxis'.format(config), asString=True),
                                    world_orient=False,
                                    direct_scale=True)
            
            # Get root of forward controls
            fk_forward_root = cmds.listRelatives(fk_forward_ctrls[0], p=1)[0]
            
            # Create group for forward ctrls
            fk_fwd_grp = cmds.group(em=True, name=name + '_FK_Fwd' + nc['group'])
            cmds.parent(fk_forward_root, fk_fwd_grp)
            
            # ===== REVERSE FK MANUAL BUILD =====
            # Create reverse controls manually (avoid duplicate guide issues)
            fk_reverse_ctrls = []
            fk_reverse_roots = []  # Track offset groups
            reverse_hierarchy = list(reversed(guide_hierarchy))
            
            for i, jnt in enumerate(reverse_hierarchy):
                # Create rev ctrl
                rev_ctrl = mt.curve(input=jnt, 
                                   type=cmds.getAttr('{}.CtrlType'.format(config), asString=True), 
                                   rename=False, 
                                   custom_name=True,
                                   name=jnt.replace(nc['joint'], '') + '_Rev' + nc['ctrl'],
                                   size=cmds.getAttr('{}.CtrlSize'.format(config)) * 0.85)
                
                mt.assign_color(rev_ctrl, color)
                mt.hide_attr(rev_ctrl, s=True, v=True)
                
                # Match position to joint
                cmds.delete(cmds.parentConstraint(jnt, rev_ctrl))
                
                # Create root group
                rev_root = mt.root_grp(input=rev_ctrl)
                fk_reverse_roots.append(rev_root)
                
                # Parent reverse controls in reverse chain order (tip controls parent)
                if i > 0:
                    cmds.parent(rev_root, fk_reverse_ctrls[i-1])
                
                fk_reverse_ctrls.append(rev_ctrl)
            
            # Parent reverse root to group (get the FIRST control's root, which is the chain root)
            fk_rev_grp = cmds.group(em=True, name=name + '_FK_Rev' + nc['group'])
            cmds.parent(fk_reverse_roots[0], fk_rev_grp)
            
            # ===== PARENT BOTH GROUPS TO CONTROL HIERARCHY =====
            cmds.parent(fk_fwd_grp, clean_ctrl_grp)
            cmds.parent(fk_rev_grp, clean_ctrl_grp)
            
            # ===== CREATE CONSTRAINT SYSTEM WITH BLENDING =====
            # Delete existing forward FK constraints and replace with dual constraints
            for i, jnt in enumerate(guide_hierarchy):
                # Find and delete existing parent constraints on this joint (from mt.fk_chain)
                pc_list = cmds.listConnections(jnt, s=True, d=False, type='parentConstraint')
                if pc_list:
                    for pc in pc_list:
                        try:
                            cmds.delete(pc)
                        except:
                            pass
                
                # Get matching controls
                fwd_ctrl = fk_forward_ctrls[i] if i < len(fk_forward_ctrls) else fk_forward_ctrls[-1]
                
                # Reverse: use reverse ctrl (from opposite end of chain)
                rev_idx = len(guide_hierarchy) - 1 - i
                rev_ctrl = fk_reverse_ctrls[rev_idx] if rev_idx < len(fk_reverse_ctrls) else fk_reverse_ctrls[0]
                
                # Create parent constraint with BOTH controls (maintains offset)
                pc = cmds.parentConstraint(fwd_ctrl, rev_ctrl, jnt, mo=True)[0]
                
                # Get constraint weight alias names
                pc_weights = cmds.parentConstraint(pc, q=True, weightAliasList=True)
                
                # Create blend attribute on first forward ctrl
                if i == 0:
                    blend_attr = mt.new_attr(input=fk_forward_ctrls[0], 
                                            name='FK_Direction',
                                            min=0, max=1, default=0.5)
                
                # Use setDrivenKey to drive constraint weights
                if len(pc_weights) == 2:
                    # Set keys for forward weight (weight[0])
                    cmds.setDrivenKeyframe('{}.{}'.format(pc, pc_weights[0]), 
                                         cd='{}.FK_Direction'.format(fk_forward_ctrls[0]),
                                         v=1, dv=0)  # At FK_Direction=0, forward=1
                    cmds.setDrivenKeyframe('{}.{}'.format(pc, pc_weights[0]), 
                                         cd='{}.FK_Direction'.format(fk_forward_ctrls[0]),
                                         v=0, dv=1)  # At FK_Direction=1, forward=0
                    
                    # Set keys for reverse weight (weight[1])
                    cmds.setDrivenKeyframe('{}.{}'.format(pc, pc_weights[1]), 
                                         cd='{}.FK_Direction'.format(fk_forward_ctrls[0]),
                                         v=0, dv=0)  # At FK_Direction=0, reverse=0
                    cmds.setDrivenKeyframe('{}.{}'.format(pc, pc_weights[1]), 
                                         cd='{}.FK_Direction'.format(fk_forward_ctrls[0]),
                                         v=1, dv=1)  # At FK_Direction=1, reverse=1
            
            # ===== SETUP RIG HIERARCHY =====
            guide_parent = cmds.listRelatives(guide_root, p=True)
            if guide_parent:
                parent_of_guide_parent = cmds.listRelatives(guide_parent[0], p=True)
                if parent_of_guide_parent:
                    cmds.parent(parent_of_guide_parent, clean_rig_grp)
            else:
                cmds.parent(guide_root, clean_rig_grp)
            
            # ===== SETUP PARENT CONSTRAINT =====
            if cmds.getAttr('{}.SetParent'.format(config)) == 'new_locator':
                loc_name = '{}'.format(str(block).replace(nc['module'], '_Parent' + nc['locator']))
                if is_right_side:
                    loc_name = loc_name.replace(nc['left'], nc['right'])
                block_parent = cmds.spaceLocator(n=loc_name)
            else:
                block_parent = cmds.getAttr('{}.SetParent'.format(config))
                if is_right_side:
                    block_parent = block_parent.replace(nc['left'], nc['right'])
            
            # Parent constraint the control groups
            cmds.parentConstraint(block_parent, fk_fwd_grp, maintainOffset=True)
            cmds.parentConstraint(block_parent, fk_rev_grp, maintainOffset=True)
            cmds.parentConstraint(block_parent, clean_rig_grp, maintainOffset=True)
            
            print('Bidirectional FK built for: {}'.format(guide_root))
    
    cmds.select(block)
    print('Reverse FK Block Build Complete!')

