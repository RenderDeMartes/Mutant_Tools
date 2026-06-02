from __future__ import absolute_import
from maya import cmds, mel
import json
try:
    import importlib;from importlib import reload
except:
    import imp;from imp import reload
import os
from pathlib import Path

import Mutant_Tools
import Mutant_Tools.Utils.Rigging
from Mutant_Tools.Utils.Rigging import main_mutant
reload(Mutant_Tools.Utils.Rigging.main_mutant)

mt = main_mutant.Mutant()

from Mutant_Tools.Utils.External import Ribbonizer
reload(Ribbonizer)

#---------------------------------------------

TAB_FOLDER = '008_Props'
PYBLOCK_NAME = 'exec_ribbonizer'

#---------------------------------------------

def create_ribbonizer_block(name = 'Ribbonizer'):

    #---------------------------------------------------
    #---------------------------------------------------
    #---------------------------------------------------


    # Read name conventions as nc[''] and setup as seup['']
    PATH = os.path.dirname(__file__)
    PATH = Path(PATH)
    PATH_PARTS = PATH.parts[:-2]
    FOLDER = ''
    for f in PATH_PARTS:
        FOLDER = os.path.join(FOLDER, f)

    MODULE_FILE = os.path.join(os.path.dirname(__file__), '07_Ribbonizer.json')
    with open(MODULE_FILE) as module_file:
        module = json.load(module_file)

    nc, curve_data, setup = mt.import_configs()

    #---------------------------------------------------
    #---------------------------------------------------
    #---------------------------------------------------

    #name checks and block creation
    name = mt.ask_name(text = module['Name'])
    if cmds.objExists('{}{}'.format(name,nc['module'])):
        cmds.warning('Name already exists.')
        return ''

    block = mt.create_block(name = name, icon = 'Ribbon',  attrs = module['attrs'], build_command = module['build_command'], import_command = module['import'])
    config = block[1]
    block = block[0]

    surface = mel.eval(
        'nurbsPlane -p 0 0 0 -ax 0 0 1 -w 5 -lr 0.2 -d 3 -u 5 -v 1 -ch 0 -n {};'.format(
            name + nc['guide']))[0]
    cmds.parent(surface, block)
    cmds.select(block)

    print('{} Created Successfully'.format(name))

#create_ribbonizer_block()

#-------------------------

def build_ribbonizer_block():

    nc, curve_data, setup = mt.import_configs()

    mt.check_is_there_is_base()

    block = cmds.ls(sl=True)
    config = cmds.listConnections(block)[1]
    block = block[0]
    guides = cmds.listRelatives(block, c=True)
    name = block.replace(nc['module'],'')

    #cmds.getAttr('{}.AttrName'.format(config))
    #cmds.getAttr('{}.AttrName'.format(config), asString = True)

    # Read mirror setting
    try:
        mirror_mode = cmds.getAttr('{}.Mirror'.format(config), asString=True)
    except:
        mirror_mode = 'False'

    # Auto-prepend L_ when mirroring if the name doesn't already have a side prefix
    if mirror_mode == 'True' and not name.startswith(nc['left']) and not name.startswith(nc['right']):
        name = nc['left'] + name

    #clean a bit
    clean_ctrl_grp = cmds.group(n=name+nc['ctrl']+nc['group'], em=True)
    clean_rig_grp = cmds.group(em=True, n = '{}{}'.format(block.replace(nc['module'],'_Rig'), nc['group']))
    bind_jnt_grp = '{}{}'.format(setup['rig_groups']['bind_joints'], nc['group'])

    cmds.parent(clean_rig_grp, '{}{}'.format(setup['rig_groups']['misc'], nc['group']))
    cmds.parent(clean_ctrl_grp, setup['base_groups']['control'] + nc['group'])
    
    if mirror_mode == 'True':
        r_name = name.replace(nc['left'], nc['right'], 1) if name.startswith(nc['left']) else nc['right'] + name
        r_block = block.replace(nc['left'], nc['right'], 1) if block.startswith(nc['left']) else nc['right'] + block
        
        r_clean_ctrl_grp = cmds.group(n=r_name+nc['ctrl']+nc['group'], em=True)
        r_clean_rig_grp = cmds.group(em=True, n = '{}{}'.format(r_block.replace(nc['module'],'_Rig'), nc['group']))
        
        cmds.parent(r_clean_rig_grp, '{}{}'.format(setup['rig_groups']['misc'], nc['group']))
        cmds.parent(r_clean_ctrl_grp, setup['base_groups']['control'] + nc['group'])

    #use this locator in case parent is set to new locator
    if cmds.getAttr('{}.SetParent'.format(config)) == 'new_locator':
        block_parent = cmds.spaceLocator( n = '{}'.format(str(block).replace(nc['module'],'_Parent' + nc['locator'])))[0]
        if mirror_mode == 'True':
            r_block_loc_name = str(block).replace(nc['left'], nc['right'], 1) if str(block).startswith(nc['left']) else nc['right'] + str(block)
            r_block_parent = cmds.spaceLocator( n = '{}'.format(r_block_loc_name.replace(nc['module'],'_Parent' + nc['locator'])))[0]
    else:
        block_parent = cmds.getAttr('{}.SetParent'.format(config))
        if mirror_mode == 'True':
            r_block_parent = block_parent.replace(nc['left'], nc['right'], 1) if block_parent.startswith(nc['left']) else block_parent
            if not cmds.objExists(r_block_parent):
                r_block_parent = block_parent

    if cmds.objExists(block_parent):
        cmds.matchTransform(clean_ctrl_grp, block_parent, pos=True, piv=True)
        cmds.matchTransform(clean_rig_grp, block_parent, pos=True, piv=True)
        
    if mirror_mode == 'True' and cmds.objExists(r_block_parent):
        cmds.matchTransform(r_clean_ctrl_grp, r_block_parent, pos=True, piv=True)
        cmds.matchTransform(r_clean_rig_grp, r_block_parent, pos=True, piv=True)

    for num, guide in enumerate(guides):

        new_guide=cmds.duplicate(guide, n=guide.replace(nc['guide'], nc['nurb']))
        cmds.parent(new_guide, w=True)

        guide_name = new_guide[0] if isinstance(new_guide, list) else new_guide

        # Derive left/right names robustly
        if name.startswith(nc['left']):
            right_name = name.replace(nc['left'], nc['right'], 1)
        else:
            right_name = nc['right'] + name

        # Read ribbonizer config attrs once
        try:
            main_ctrl_pos = cmds.getAttr('{}.MiddleCtrlPosition'.format(config), asString=True)
        except:
            main_ctrl_pos = 'Original'

        try:
            ctrl_orientation = cmds.getAttr('{}.CtrlOrientation'.format(config), asString=True)
        except:
            ctrl_orientation = 'SurfaceNormal'

        try:
            ctrl_scales = cmds.getAttr('{}.CtrlScales'.format(config))
        except:
            ctrl_scales = False

        try:
            joint_orient = cmds.getAttr('{}.JointOrient'.format(config))
        except:
            joint_orient = False

        try:
            fk_on_last = cmds.getAttr('{}.FkOnLast'.format(config))
        except:
            fk_on_last = False

        try:
            gimbal = cmds.getAttr('{}.Gimbal'.format(config))
        except:
            gimbal = False

        ribbonize_kwargs = dict(
            equal=cmds.getAttr('{}.Equal'.format(config)),
            num_of_Ctrls=cmds.getAttr('{}.Ctrls'.format(config)),
            num_of_Jnts=cmds.getAttr('{}.Joints'.format(config)),
            constrain=cmds.getAttr('{}.Constraint'.format(config)),
            add_fk=cmds.getAttr('{}.AddFk'.format(config)),
            wire=cmds.getAttr('{}.Wire'.format(config)),
            middle_ctrl_pos=main_ctrl_pos,
            ctrl_orientation=ctrl_orientation,
            ctrl_scales=ctrl_scales,
            joint_orient=joint_orient,
            fk_on_last=fk_on_last,
            gimbal=gimbal,
        )

        if mirror_mode == 'Right_Only':
            right_guide_rename = guide_name.replace(nc['left'], nc['right'], 1) if nc['left'] in guide_name else nc['right'] + guide_name
            right_guide = cmds.duplicate(guide_name, n=right_guide_rename)
            right_guide_result = right_guide[0] if isinstance(right_guide, list) else right_guide
            try:
                cmds.parent(right_guide_result, w=True)
            except:
                pass

            right_prefix = right_name + '_' + str(num+1)
            r_ctrl_grp, r_rig_grp, r_bnd_grp = Ribbonizer.ribbonize(
                surf_tr=right_guide_result, prefix=right_prefix, **ribbonize_kwargs)

            # Wrap the right side outputs with mirror_group (adds -1 scale + 180 rotateX)
            r_ctrl_mirror = mt.mirror_group(r_ctrl_grp, world=True)
            r_rig_mirror = mt.mirror_group(r_rig_grp, world=True)

            cmds.parent(r_ctrl_mirror, r_clean_ctrl_grp)
            cmds.parent(r_rig_mirror, r_clean_rig_grp)
            cmds.parent(r_bnd_grp, bind_jnt_grp)

        elif mirror_mode == 'True':
            # Duplicate the guide for the right side BEFORE ribbonize (it renames the input surface)
            right_guide_rename = guide_name.replace(nc['left'], nc['right'], 1) if nc['left'] in guide_name else nc['right'] + guide_name
            right_guide = cmds.duplicate(guide_name, n=right_guide_rename)
            right_guide_result = right_guide[0] if isinstance(right_guide, list) else right_guide
            try:
                cmds.parent(right_guide_result, w=True)
            except:
                pass

            # --- Left side: build from the original guide ---
            left_prefix = name + '_' + str(num+1)
            ctrl_grp, rig_grp, bnd_grp = Ribbonizer.ribbonize(
                surf_tr=guide_name, prefix=left_prefix, **ribbonize_kwargs)

            # Add identity wrapper group so hierarchy depth matches the mirrored side
            left_wrapper = cmds.group(ctrl_grp, n='{}Mirror{}'.format(ctrl_grp, nc['group']))
            cmds.xform(left_wrapper, rp=(0,0,0), sp=(0,0,0))
            cmds.parent(left_wrapper, clean_ctrl_grp)
            cmds.parent(rig_grp, clean_rig_grp)
            cmds.parent(bnd_grp, bind_jnt_grp)

            # --- Right side: build from the pre-duplicated guide, then wrap with mirror_group ---
            right_prefix = right_name + '_' + str(num+1)
            r_ctrl_grp, r_rig_grp, r_bnd_grp = Ribbonizer.ribbonize(
                surf_tr=right_guide_result, prefix=right_prefix, **ribbonize_kwargs)

            # Wrap the right side outputs with mirror_group (adds -1 scale + 180 rotateX)
            r_ctrl_mirror = mt.mirror_group(r_ctrl_grp, world=True)
            r_rig_mirror = mt.mirror_group(r_rig_grp, world=True)

            cmds.parent(r_ctrl_mirror, r_clean_ctrl_grp)
            cmds.parent(r_rig_mirror, r_clean_rig_grp)
            cmds.parent(r_bnd_grp, bind_jnt_grp)

        else:
            # No mirror - build as-is (no wrapper groups needed)
            side_prefix = name + '_' + str(num+1)
            ctrl_grp, rig_grp, bnd_grp = Ribbonizer.ribbonize(
                surf_tr=guide_name, prefix=side_prefix, **ribbonize_kwargs)

            cmds.parent(ctrl_grp, clean_ctrl_grp)
            cmds.parent(rig_grp, clean_rig_grp)
            cmds.parent(bnd_grp, bind_jnt_grp)

    cmds.parentConstraint(block_parent, clean_ctrl_grp, mo=True)
    cmds.scaleConstraint(block_parent, clean_ctrl_grp, mo=True)
    #cmds.scaleConstraint(block_parent, clean_rig_grp, mo=True) # Commented out to prevent double transforms on surface
    
    if mirror_mode == 'True':
        cmds.parentConstraint(r_block_parent, r_clean_ctrl_grp, mo=True)
        cmds.scaleConstraint(r_block_parent, r_clean_ctrl_grp, mo=True)
        #cmds.scaleConstraint(r_block_parent, r_clean_rig_grp, mo=True) # Commented out to prevent double transforms on surface


    print ('Build {} Success'.format(block))



#build_ribbonizer_block()
