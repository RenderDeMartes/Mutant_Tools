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
    if mirror_mode in ('True', 'Right_Only') and not name.startswith(nc['left']) and not name.startswith(nc['right']):
        name = nc['left'] + name

    #clean a bit
    clean_ctrl_grp = cmds.group(n=name+nc['ctrl']+nc['group'], em=True)
    clean_rig_grp = cmds.group(em=True, n = '{}{}'.format(block.replace(nc['module'],'_Rig'), nc['group']))
    bind_jnt_grp = '{}{}'.format(setup['rig_groups']['bind_joints'], nc['group'])

    cmds.parent(clean_rig_grp, '{}{}'.format(setup['rig_groups']['misc'], nc['group']))
    cmds.parent(clean_ctrl_grp, setup['base_groups']['control'] + nc['group'])


    #use this locator in case parent is set to new locator
    if cmds.getAttr('{}.SetParent'.format(config)) == 'new_locator':
        block_parent = cmds.spaceLocator( n = '{}'.format(str(block).replace(nc['module'],'_Parent' + nc['locator'])))
    else:
        block_parent = cmds.getAttr('{}.SetParent'.format(config))

    for num, guide in enumerate(guides):

        new_guide=cmds.duplicate(guide, n=guide.replace(nc['guide'], nc['nurb']))
        cmds.parent(new_guide, w=True)

        # Determine which sides to build based on mirror mode
        # Each entry: (side_guide, side_prefix, needs_mirror_group)
        sides_to_build = []

        # Derive left/right names robustly
        guide_name = new_guide[0] if isinstance(new_guide, list) else new_guide
        if name.startswith(nc['left']):
            right_name = name.replace(nc['left'], nc['right'], 1)
            right_guide_rename = guide_name.replace(nc['left'], nc['right'], 1)
        else:
            right_name = nc['right'] + name
            right_guide_rename = nc['right'] + guide_name

        if mirror_mode == 'Right_Only':
            # Mirror the guide to the right side, build only the right side
            miror_grp = mt.mirror_group(guide_name, world=True)
            cmds.makeIdentity(miror_grp, a=True, t=True, r=True, s=True)
            cmds.parent(guide_name, w=True)
            cmds.delete(miror_grp)
            # Rename guide to R_ side
            if right_guide_rename != guide_name:
                guide_name = cmds.rename(guide_name, right_guide_rename)
            right_prefix = right_name + '_' + str(num+1)
            sides_to_build.append((guide_name, right_prefix, False))

        elif mirror_mode == 'True':
            # Build the left side as-is
            left_prefix = name + '_' + str(num+1)
            sides_to_build.append((guide_name, left_prefix, False))

            # Duplicate and mirror for the right side
            right_guide = cmds.duplicate(guide_name, n=right_guide_rename)
            right_guide_result = right_guide[0] if isinstance(right_guide, list) else right_guide
            right_prefix = right_name + '_' + str(num+1)
            sides_to_build.append((right_guide_result, right_prefix, True))

        else:
            # No mirror - build as-is
            sides_to_build.append((guide_name, name + '_' + str(num+1), False))

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

        for side_guide, side_prefix, needs_mirror in sides_to_build:

            ctrl_grp, rig_grp, bnd_grp = Ribbonizer.ribbonize(   surf_tr=side_guide,
                                                                 equal=cmds.getAttr('{}.Equal'.format(config)),
                                                                 num_of_Ctrls=cmds.getAttr('{}.Ctrls'.format(config)),
                                                                 num_of_Jnts=cmds.getAttr('{}.Joints'.format(config)),
                                                                 prefix=side_prefix,
                                                                 constrain=cmds.getAttr('{}.Constraint'.format(config)),
                                                                 add_fk=cmds.getAttr('{}.AddFk'.format(config)),
                                                                 wire=cmds.getAttr('{}.Wire'.format(config)),
                                                                 middle_ctrl_pos=main_ctrl_pos,
                                                                 ctrl_orientation=ctrl_orientation,
                                                                 ctrl_scales=ctrl_scales,
                                                                 joint_orient=joint_orient)
            #[main_Ctrl_offset, rig_Grp, prefix + 'Bnd_Grp']

            if needs_mirror:
                # Wrap the right side output in mirror groups (negate X scale)
                ctrl_grp = mt.mirror_group(ctrl_grp, world=True)
                rig_grp = mt.mirror_group(rig_grp, world=True)
                bnd_grp = mt.mirror_group(bnd_grp, world=True)

            cmds.parent(ctrl_grp, clean_ctrl_grp)
            cmds.parent(rig_grp, clean_rig_grp)
            cmds.parent(bnd_grp, bind_jnt_grp)

        # Resolve block_parent for right side if mirroring
        side_block_parent = block_parent
        if mirror_mode == 'True' or mirror_mode == 'Right_Only':
            parent_str = cmds.getAttr('{}.SetParent'.format(config))
            if parent_str != 'new_locator' and nc['left'] in str(parent_str):
                # We handle right-side parent swap inside the loop above via mirror groups
                pass

    cmds.parentConstraint(block_parent, clean_ctrl_grp, mo=True)
    cmds.scaleConstraint(block_parent, clean_ctrl_grp, mo=True)


    print ('Build {} Success'.format(block))



#build_ribbonizer_block()
