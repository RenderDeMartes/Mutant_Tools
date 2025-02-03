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

#Sebastian was here :)

#---------------------------------------------

TAB_FOLDER = '002_Biped'
PYBLOCK_NAME = 'exec_hair'

#---------------------------------------------

def create_hair_block(name = 'Hair'):

    #---------------------------------------------------
    #---------------------------------------------------
    #---------------------------------------------------

    letters = string.ascii_uppercase

    # Read name conventions as nc[''] and setup as seup['']
    PATH = os.path.dirname(__file__)
    PATH = Path(PATH)
    PATH_PARTS = PATH.parts[:-2]
    FOLDER = ''
    for f in PATH_PARTS:
        FOLDER = os.path.join(FOLDER, f)

    MODULE_FILE = os.path.join(os.path.dirname(__file__), '011_Hair.json')
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

    #Getting number of chains needed and length of chains. 
    chain_amount = mt.ask_name(ask_for='Number of chains', text='5')
    chain_length = mt.ask_name(ask_for='Joint per chain', text='5')

    block = mt.create_block(name = name, icon = 'Hair',  attrs = module['attrs'], build_command = module['build_command'], import_command = module['import'])
    config = block[1]
    block = block[0]

    cmds.select(cl=True)
      
    #cmds.getAttr('{}.AttrName'.format(config)) #get attrs from config
    #cmds.getAttr('{}.AttrName'.format(config), asString = True) #for enums
    #joint_one = mt.create_joint_guide(name = name) #guide base with shapes

    main_joints=[]
    first_chain_joint = True
    #Looping for all chain parents. 
    for chain_number in range(int(chain_amount)):
        #Reseting the first-joint-in-chain indicator.
        first_chain_joint = True

        #Looping for all chain joints. 
        for chain_joint in range(int(chain_length)):
            jnt = cmds.joint(n=name+'_'+letters[chain_number]+'_'+"{:02d}".format(chain_joint+1)+nc['guide'])
            #print("Joint created is: {}".format(jnt))
            #If joint is first in chain and isn't the first joint created take it out of hierarchy. 
            if first_chain_joint:
                #print("'{}' is first joint in chain".format(jnt))
                if cmds.listRelatives(jnt, parent=True):
                    cmds.parent(jnt, world=True)
                    #print("Took '{}' out of hierarchy".format(jnt))
                #print("Setting translateZ attribute to {} for joint {}.".format(chain_number, jnt))
                cmds.setAttr("{}.translateZ".format(jnt), chain_number)
                cmds.setAttr("{}.translateX".format(jnt), 0)
                main_joints.append(jnt)
            else:
                #Offset next created joint. 
                cmds.setAttr("{}.translateX".format(jnt), 1)
            #Turn off first-joint-in-chain indicator. 
            first_chain_joint = False

    for main_joint in main_joints:
        cmds.setAttr("{}.rotateZ".format(main_joint), -90)
        cmds.makeIdentity(main_joint, rotate=True, apply=True)

    cmds.parent(main_joints, block)
    cmds.select(block)

    print('{} Created Successfully'.format(name))

#create_hair_block()




#-------------------------------

def build_hair_block():

    print('Start of build hair block func')

    nc, curve_data, setup = mt.import_configs()

    mt.check_is_there_is_base()

    block = cmds.ls(sl=True)
    config = cmds.listConnections(block)[1]
    block = block[0]
    guides = cmds.listRelatives(block, c=True)
    name = block.replace(nc['module'],'')

    clean_ctrl_grp = cmds.group(em=True, name=name + nc['ctrl'] + nc['group'])
    clean_rig_grp = cmds.group(em=True, name=name + '_Rig' + nc['group'])

    cmds.parent(clean_rig_grp, '{}{}'.format(setup['rig_groups']['misc'], nc['group']))
    cmds.parent(clean_ctrl_grp, setup['base_groups']['control'] + nc['group'])

    to_build = []
    to_mirror = []
    fk_ctrl_roots = []
    all_fk_ctrls = []
    fk_systems_info_dict = {}

    for guide in guides:

        #Getting the guide parent and the guide hierarchy.
        new_guide = mt.duplicate_and_remove_guides(guide)
        guide_childs=cmds.listRelatives(new_guide, ad=True)
        if guide_childs:
            all_guides = [new_guide]+guide_childs
        else:
            all_guides = [new_guide]


        #If guide HAS LEFT prefix and mirror is on. Create mirrored guide. 
        if new_guide.startswith(nc['left']) and cmds.getAttr('{}.Mirror'.format(config)):
            if guide.replace(nc['left'],nc['right']) not in guides:
                right_guide = cmds.mirrorJoint(new_guide, mirrorYZ = True, mirrorBehavior=True, searchReplace = (nc['left'],nc['right']))[0]
                #right_guide = mt.duplicate_change_names(input=new_guide, hi=True, search=nc['left'], replace=nc['right'])[0]
                #mt.orient_joint(input=right_guide)
                to_build.append(right_guide)
                to_mirror.append(right_guide)
            else:
                print("Guide {} already has a corresponding right side guide.".format(guide))
            to_build.append(new_guide)

        #For cases where mirroring is off or guide doesn't start with left just add to build. 
        else:
            to_build.append(new_guide)

    #Getting the build guides's hierchies. 
    for guide in to_build:
        guide_childs_build=cmds.listRelatives(guide, ad=True)
        if guide_childs_build:
            guide_hierarchy = [guide] + list(reversed(guide_childs_build))
        else:
            guide_hierarchy = [guide]
        cmds.select(guide_hierarchy)

        #Settting proper colors.
        color = cmds.getAttr('{}.CtrlColor'.format(config), asString=True)
        is_right_side = guide.startswith(nc['right'])

        # if mirror is set, ignore ctrlColor attr and use default side colors
        if cmds.getAttr('{}.Mirror'.format(config)):
            if guide.startswith(nc['left']):
                color = setup['left_color']
            elif is_right_side:
                color = setup['right_color']
        
        # Creating the FK Chain. 
        fk_system = mt.fk_chain(input='',
                        size=cmds.getAttr('{}.CtrlSize'.format(config)),
                        color=color,
                        curve_type=cmds.getAttr('{}.CtrlType'.format(config), asString=True),
                        scale=True,
                        twist_axis=cmds.getAttr('{}.TwistAxis'.format(config), asString=True),
                        world_orient=False)
        
        for ctrl in fk_system:
            all_fk_ctrls.append(ctrl)
        
        fk_systems_info_dict[fk_system[0]] = fk_system

        #fixing scaling on jnt hierarchy. 
        for jnt in guide_hierarchy:
            cmds.setAttr("{}.segmentScaleCompensate".format(jnt), 0)

        #Creating bind joints:
        bind_joints = []
        for i, joint in enumerate(guide_hierarchy):
            bind_joint = cmds.duplicate(joint, n=joint.replace(nc['joint'], nc['joint_bind']), parentOnly=1)[0]
            cmds.parentConstraint(joint, bind_joint)
            cmds.scaleConstraint(joint, bind_joint)
            bind_joints.append(bind_joint)
            if i > 0:
                cmds.parent(bind_joint, bind_joints[i-1])

        #Cleaning up a bit
        ctrl_root = cmds.listRelatives(fk_system[0], p=1)[0]
        fk_ctrl_roots.append(ctrl_root)
        cmds.parent(ctrl_root, clean_ctrl_grp)
        #print('fk system = {}'.format(fk_system))
        cmds.parent(guide, clean_rig_grp)

        bind_jnt_grp = '{}{}'.format(setup['rig_groups']['bind_joints'], nc['group'])
        if cmds.objExists(bind_jnt_grp):
            cmds.parent(bind_joints[0], bind_jnt_grp)

    #use this locator in case parent is set to new locator
    if cmds.getAttr('{}.SetParent'.format(config)) == 'new_locator':
        loc_name = '{}'.format(str(block).replace(nc['module'],'_Parent' + nc['locator']))

        block_parent = cmds.spaceLocator( n = loc_name)
        cmds.parentConstraint(block_parent, clean_ctrl_grp, maintainOffset=1)
        cmds.scaleConstraint(block_parent, clean_ctrl_grp, maintainOffset=1)
    else:
        block_parent = cmds.getAttr('{}.SetParent'.format(config))
        cmds.parentConstraint(block_parent, clean_ctrl_grp, maintainOffset=1)
        cmds.scaleConstraint(block_parent, clean_ctrl_grp, maintainOffset=1)

    #SUB AUTO ROTATES
    if cmds.getAttr('{}.SubAutoRotate'.format(config)):
        for top_ctrl in list(fk_systems_info_dict.keys()):
            #Creating parent grp if none exists. 
            if not cmds.objExists("{}_SubRotators{}".format(name, nc['group'])):
                sub_rotators_parent = cmds.createNode("transform", name="{}_SubRotators{}".format(name, nc['group']))
                cmds.parent(sub_rotators_parent, clean_ctrl_grp)
            #Creating sub rotator ctrl. 
            sub_rotator_top_ctrl_name = "_".join(top_ctrl.split("_")[0:-2])
            sub_ctrl_autorotate = mt.curve(input = '', type = 'sphere', rename=True, custom_name=True, name='{}_Rotator{}'.format(sub_rotator_top_ctrl_name, nc['ctrl']), size=cmds.getAttr('{}.CtrlSize'.format(config)))
            sub_ctrl_autorotate_offset, sub_ctrl_autorotate_offset_root = mt.root_grp(sub_ctrl_autorotate, autoRoot=True)
            sub_ctrl_autorotate_offset = cmds.rename(sub_ctrl_autorotate_offset, sub_ctrl_autorotate_offset.replace("_Root", "_SubRoot"))
            sub_ctrl_autorotate_offset_root = cmds.rename(sub_ctrl_autorotate_offset_root, sub_ctrl_autorotate_offset_root.replace("_Auto", "_SubAuto"))
            #Connecting sub rotators and parenting them.
            subAutoRotate_new_offset = mt.connect_object_to_offsets(driver_ctrl=sub_ctrl_autorotate, driven_ctrls=fk_systems_info_dict[top_ctrl], offset_name='SubAutoRotate', auto_root=False)
            cmds.parent(sub_ctrl_autorotate_offset, sub_rotators_parent)

            #Placing rotator at start of chain and orienting it. 
            top_ctrl_translations = cmds.xform(top_ctrl, q=True, translation=True, worldSpace=True)
            top_ctrl_rotations = cmds.xform(top_ctrl, q=True, rotation=True, worldSpace=True)
            cmds.xform(sub_ctrl_autorotate_offset, translation=top_ctrl_translations, worldSpace=True)
            cmds.xform(sub_ctrl_autorotate_offset, rotation=top_ctrl_rotations, worldSpace=True)
            cmds.setAttr("{}.ty".format(sub_ctrl_autorotate_offset), int(cmds.getAttr("{}.ty".format(sub_ctrl_autorotate_offset)) + cmds.getAttr('{}.CtrlSize'.format(config))))




    #MAIN AUTO ROTATE
    if cmds.getAttr('{}.AutoRotate'.format(config)):
        ctrl_autorotate = mt.curve(input = '', type = 'sphere', rename=True, custom_name=True, name='{}_Rotator{}'.format(name, nc['ctrl']), size=cmds.getAttr('{}.CtrlSize'.format(config)))
        ctrl_autorotate_offset, ctrl_autorotate_offset_root = mt.root_grp(ctrl_autorotate, autoRoot=True)

        mt.connect_object_to_offsets(driver_ctrl=ctrl_autorotate, driven_ctrls=all_fk_ctrls, offset_name='AutoRotate', auto_root=False)
        cmds.parent(ctrl_autorotate_offset, clean_ctrl_grp)

        block_setParent = cmds.getAttr('{}.SetParent'.format(config))

        if block_setParent != 'new_locator':
            if cmds.objExists(block_setParent):
                cmds.xform(ctrl_autorotate_offset, rotation=[0,0,0], absolute=True)
                block_parent_transforms = cmds.xform(block_setParent, q=True, translation=True, worldSpace=True)
                cmds.xform(ctrl_autorotate_offset, translation=block_parent_transforms, worldSpace=True)

    #LOCKING
    #Getting values from UI. 
    lock_pin = cmds.getAttr('{}.SetLockPin'.format(config))
    lock_guides_string = cmds.getAttr('{}.SetLockGuides'.format(config))
    if lock_guides_string:
        lock_guides = lock_guides_string.replace(' ', '').split(',')
    else:
        lock_guides=[]
    lock_attrs_holder = cmds.getAttr('{}.SetLockAttrs'.format(config))

    print("Lock pin is: {}".format(lock_pin))
    print("Lock guides are: {}".format(lock_guides))
    print("Lock attributes holder is: {}".format(lock_attrs_holder))
    
    #Determining if mirroring is on and if yes then adding the right guide into list. 
    if cmds.getAttr('{}.Mirror'.format(config)):
        for guide in lock_guides:
            if guide.replace(nc['left'], nc['right']) not in lock_guides:
                lock_guides.append(guide.replace(nc['left'], nc['right']))
    
    #If all three text boxes have values then create locks. 
    if lock_pin and lock_guides and lock_attrs_holder:

        #Adding division attr
        if cmds.attributeQuery("________________", node=lock_attrs_holder, exists=True):
            cmds.setAttr("{}.________________".format(lock_attrs_holder), lock=False)
            print("'lock' Division attribute already exists")
            cmds.deleteAttr("{}.________________".format(lock_attrs_holder,))
                
        cmds.addAttr(lock_attrs_holder, at="enum", en="Locks:", ln="________________", keyable=True)
        cmds.setAttr("{}.________________".format(lock_attrs_holder), lock=True)
        
        #Creating locks. 
        for guide in lock_guides:
            attribute_name = guide.replace(nc['guide'], "")
            create_hair_locks(attrs_holder=lock_attrs_holder, driven_objects=[guide], attr_name=attribute_name, pin_joint=lock_pin)
    
    #If only some of the text boxes have values then error and report it.  
    elif lock_pin or lock_guides or lock_attrs_holder:

        error_message="""
        ("#--------------------------Lock Error--------------------------------#")
        ("If you want to create the Locks you must fill in all three text boxes.")
        ("#--------------------------Lock Error--------------------------------#")
        """
        cmds.error(error_message)
    


    print('Build {} Success'.format(block))



#build_hair_block()


#-------------------------------------------------------------------------------------------------
def create_local_offset(ctrl_sel=[], suffix="Offset_grp", base="", replace="", zero_scale=True):
        
    """
    Description:
    Create local offset groups for the given controllers, allowing for easy manipulation and control.

    Args:
        ctrl_sel (list): List of controllers to create local offset groups for.
        suffix (str): Suffix to be added to the names of the local offset groups.
        base (str): Base string to be replaced in the local offset group names.
        replace (str): String to replace the base in the local offset group names.
        zero_scale (bool): Flag to determine whether to set scale attributes to zero or not.

    Returns:
        list: A list of newly created local offset groups.

    Example:
        create_local_offset(ctrl_sel=["my_ctrl_1", "my_ctrl_2"], suffix="Lock_grp", base="_Offset_grp", replace="offset", zero_scale=True)
    """
    
    if not ctrl_sel:
        ctrl_sel = cmds.ls(sl=True)
        
    #Defining Attribute lists.
    attrs_0 = ["translateX", "translateY", "translateZ", "rotateX", "rotateY", "rotateZ"]
    attrs_1 = ["scaleX", "scaleY", "scaleZ"]

    new_offset_grps = []

    for ctrl in ctrl_sel:
        
        #Creating ctrl offset group and placing it in hierarcy so it keeps it's values.
        LocalOffset_group = cmds.group(name="{}_{}".format(ctrl, suffix), empty=True)

        if base:
            if not replace:
                new_name=LocalOffset_group.replace(base, "")
                LocalOffset_group = cmds.rename(LocalOffset_group, new_name)
            if replace:
                new_name=LocalOffset_group.replace(base, replace)
                LocalOffset_group = cmds.rename(LocalOffset_group, new_name)

        cmds.parent(LocalOffset_group, ctrl)

        #Setting attributes to 0 and 1. 
        for attr in attrs_0:
            cmds.setAttr("{}.{}".format(LocalOffset_group, attr), 0)
        if zero_scale == True:
            for attr in attrs_1:
                cmds.setAttr("{}.{}".format(LocalOffset_group, attr), 1)
            
        ctrl_parent = cmds.listRelatives(ctrl, parent=True)
        
        #Placing ctrl inside offset group.
        if ctrl_parent:
            cmds.parent(LocalOffset_group, ctrl_parent)
            cmds.parent(ctrl, LocalOffset_group)
            
        else:
            cmds.parent(LocalOffset_group, world=True)
            cmds.parent(ctrl, LocalOffset_group)
        
        new_offset_grps.append(LocalOffset_group)
    
    return new_offset_grps
        

#create_local_offset(suffix="Lock_grp", base="_Offset_grp")



#----------------------------------------------------------------------------------------------------

def create_hair_locks(attrs_holder="", driven_objects=[], attr_name="", pin_joint=""):

    """
    Description:
    Will create a parent constraint between a the parent of a control, the specified pin joint and a newly created offset group
    for every object in the driven objects list. I'll create an attribute to toggle the influence of the parent constraint on specified
    attribute holder.

    Args:
        attrs_holder (str): The control that will have the lock attributes.
        driven_objects (list): List of objects to be driven by the hair locks.
        attr_name (str): The name of the attribute used for controlling the hair locks.
        pin_joint (str): The name of the object that will pin the controls.

    Returns:
        None/False

    Note:
        This function assumes that certain configurations are set up and that specific attributes exist.

    Example:
        create_hair_locks(attrs_holder="my_ctrl", driven_objects=["hair_ctrl_1", "hair_ctrl_2"], attr_name="pin", pin_joint="spine_joint")
    """

    nc, curve_data, setup = mt.import_configs()

    #Determine important info and criteria fullfilment based on selection.

    if not driven_objects:
        driven_objects = cmds.ls(sl=True)

    driven_ctrls = []
    
    for obj in driven_objects:
        if obj.endswith(nc['guide']):
            obj = obj.replace(nc['guide'], nc['ctrl'])
        driven_ctrls.append(obj)

    driven_objects = driven_ctrls

    error_ctrls = []

    for ctrl in driven_objects:

        ctrl_lock_parent = cmds.listRelatives(ctrl, ap=True)
        if ctrl_lock_parent: ctrl_lock_parent=ctrl_lock_parent[0]
        
        ctrl_lock_offset = create_local_offset(ctrl_sel=[ctrl], suffix="Lock_grp", base="_Offset_grp")[0]
        
        #Checking if parent objects exist for selected controller.
        if not ctrl_lock_parent:
            cmds.error("For {}: Please select a controller with an offset group".format(ctrl))
            error_ctrls.append(ctrl)
            continue


        #Creating parent constraint with head and ctrl local parent
        controller_constraint = cmds.parentConstraint(ctrl_lock_parent, pin_joint, ctrl_lock_offset, mo=True)[0]
        cmds.setAttr("{}.interpType".format(controller_constraint), 2)
        
        attribute_name = attr_name
        
        if cmds.attributeQuery("{}_lock".format(attribute_name), node=attrs_holder, exists=True):
            print("'{}_lock' Attribute already exists".format(attribute_name))
            cmds.deleteAttr("{}.{}_lock".format(attrs_holder,attribute_name))
            
        cmds.addAttr(attrs_holder, attributeType="float", min=0, max=1, dv=1, r=True, k=True, nn="{} Lock".format(attribute_name), ln="{}_lock".format(attribute_name))
        
        
        #Extracting the name of the attributes to control the influences for.
        lock_hair_attr = "{}.{}_lock".format(attrs_holder,attribute_name)
         
        
        #Directing connecting the new attributes to the controller constraint
        cmds.connectAttr(lock_hair_attr, "{}.{}W1".format(controller_constraint, pin_joint), f=True)
        
        
        #Creating inverse node and connecting controlling attribute to that and then to the controller constraint. 
        reverse_node = cmds.shadingNode('reverse', asUtility=True, name="{}_Lock_reverse".format(attribute_name))
        cmds.connectAttr(lock_hair_attr, "{}.inputX".format(reverse_node), f=True)
        cmds.connectAttr("{}.output.outputX".format(reverse_node), "{}.{}W0".format(controller_constraint, ctrl_lock_parent), f=True)
        
    if error_ctrls:
        print(error_ctrls)
