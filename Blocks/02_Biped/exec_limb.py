from maya import cmds
import json
import imp
import os
from pathlib import Path

import Mutant_Tools
import Mutant_Tools.Utils.Rigging
from Mutant_Tools.Utils.Rigging import main_mutant
imp.reload(Mutant_Tools.Utils.Rigging.main_mutant)

mt = main_mutant.Mutant()

#---------------------------------------------

#---------------------------------------------

TAB_FOLDER = '02_Biped'
PYBLOCK_NAME = 'exec_head'

#Read name conventions as nc[''] and setup as seup['']
PATH = os.path.dirname(__file__)
PATH = Path(PATH)
PATH_PARTS = PATH.parts[:-2]
FOLDER=''
for f in PATH_PARTS:
	FOLDER = os.path.join(FOLDER, f)

JSON_FILE = os.path.join(FOLDER, 'config', 'name_conventions.json')
with open(JSON_FILE) as json_file:
	nc = json.load(json_file)
#Read curve shapes info
CURVE_FILE = os.path.join(FOLDER, 'config', 'curves.json')
with open(CURVE_FILE) as curve_file:
	curve_data = json.load(curve_file)
#setup File
SETUP_FILE = os.path.join(FOLDER, 'config', 'rig_setup.json')
with open(SETUP_FILE) as setup_file:
	setup = json.load(setup_file)

MODULE_FILE = os.path.join(os.path.dirname(__file__),'04_Limb.json')
with open(MODULE_FILE) as module_file:
	module = json.load(module_file)




def create_limb_block(name = 'Limb'):

    #name checks and block creation
    name = mt.ask_name(text = module['Name'],
                       ask_for = 'Limb Names (Separete with a , ), Needs to start with L_ or R_ ',
                       check_split = True)

    if cmds.objExists('{}{}'.format(name.split(',')[0],nc['module'])):
        cmds.warning('Name already exists.')
        return ''

    limb_block = mt.create_block(name = name.split(',')[0], icon = 'Limb',  attrs = module['attrs'], build_command = module['build_command'], import_command = module['import'])
    limb_config = limb_block[1]
    limb_block = limb_block[0]

    name = name.split(',')
    #limb base create
    cmds.select(cl=True)
    joint_one = mt.create_joint_guide(name = name[0])
    cmds.move(5,0,0)
    joint_two = mt.create_joint_guide(name = name[1])
    cmds.move(15,0,-1)
    joint_three = mt.create_joint_guide(name = name[2])
    cmds.move(25,0,0)
    cmds.parent(joint_three, joint_two)
    cmds.parent(joint_two, joint_one)

    cmds.parent(joint_one, limb_block)

    cmds.select()
    mt.orient_joint(input = joint_one)
    mt.orient_joint(input = joint_two)
    mt.orient_joint(input = joint_three)

    cmds.select(limb_block)

    cmds.setAttr("{}.jointOrientX".format(joint_three), 0)
    cmds.setAttr("{}.jointOrientY".format(joint_three), 0)
    cmds.setAttr("{}.jointOrientZ".format(joint_three), 0)

    print('Limb Base Created Successfully'),

#create_limb_base()

#-------------------------

def build_limb_block():

    mt.check_is_there_is_base()

    block = cmds.ls(sl=True)
    config = cmds.listConnections(block)[1]
    block = block[0]
    guide = cmds.listRelatives(block, c=True)[0]

    new_guide = mt.duplicate_and_remove_guides(guide)
    print (new_guide)
    to_build = [new_guide]


    #orient the joints

    mt.orient_joint(input = new_guide)
    #force last joint to orient
    joint_three = cmds.listRelatives(new_guide, ad=True)[-2]
    cmds.setAttr("{}.jointOrientX".format(joint_three), 0)
    cmds.setAttr("{}.jointOrientY".format(joint_three), 0)
    cmds.setAttr("{}.jointOrientZ".format(joint_three), 0)

    #i have no idea why bt this shit doesnt work if we dont unparent and then aprent them

    joint_two = cmds.listRelatives(joint_three, p=True)
    cmds.parent(joint_three, w=True)
    cmds.parent(joint_two, w=True)
    cmds.parent(joint_two, new_guide)
    cmds.parent(joint_three, joint_two)

    #ctrl attrs
    ctrl_size = cmds.getAttr('{}.CtrlSize'.format(config))
    game_parent = cmds.getAttr('{}.SetGameParent'.format(config), asString = True)
    twist_amount = cmds.getAttr('{}.TwistAmount'.format(config))

    #use this group for later cleaning, just assign them when you create the top on hierarchy
    clean_rig_grp = ''
    clean_ctrl_grp = ''

    #prep work for right side ------------------------------------------------------

    #if mirror is set only to right we need to build on left for mirror behavior then putt it back to righ side
    if cmds.getAttr('{}.Mirror'.format(config), asString = True) == 'Right_Only':
        right_guide = mirror = cmds.mirrorJoint(new_guide, mirrorYZ = True, mirrorBehavior=True, searchReplace = (nc['left'],nc['right']))[0]
        mt.orient_joint(input = right_guide)
        to_build.append(right_guide)
        cmds.delete(new_guide)
        to_build.remove(new_guide)

    elif cmds.getAttr('{}.Mirror'.format(config), asString = True) == 'True':
        #right_guide = cmds.mirrorJoint(new_guide, mirrorYZ = True, mirrorBehavior=True, searchReplace = (nc['left'],nc['right']))[0]
        right_guide = mt.duplicate_change_names(input=new_guide, hi=True, search=nc['left'], replace=nc['right'])[0]
        mt.orient_joint(input = right_guide)
        to_build.append(right_guide)

        print (to_build)

    #build ------------------------------------------------------
    for side_guide in to_build:

        #use this locator in case parent is set to new locator
        if cmds.getAttr('{}.SetParent'.format(config)) == 'new_locator':
            block_parent = cmds.spaceLocator( n = '{}'.format(str(side_guide).replace(nc['joint'],'_Parent' + nc['locator'])))
        else:
            block_parent = cmds.getAttr('{}.SetParent'.format(config))
            if side_guide.startswith(nc['right']):
                block_parent = block_parent.replace(nc['left'],nc['right'])

        #smart select the colors
        if str(side_guide).startswith(nc['left']):
            color = setup['left_color']
        elif str(side_guide).startswith(nc['right']):
            color = setup['right_color']
        else:
            color = setup['main_color']


        #main funcion -------------------------------------------
        cmds.select(side_guide, hi=True)
        limb_a = cmds.ls(sl=True)[0]
        limb_b = cmds.ls(sl=True)[1]
        limb_c = cmds.ls(sl=True)[2]

        ikfk = mt.twist_fk_ik(start = '', mid = '', end = '', size = ctrl_size, color = color, twist_amount = twist_amount)

        print ('----------------IK FK------------------')

        #clean a bit
        print (ikfk['ik_fk'])
        cmds.connectAttr('Global_Ctrl.scale', '{}.scale'.format(ikfk['ik_fk'][4][5][1]))

        #ikfk['ik_fk'[#]]
        #[0] ['L_Shoulder_Jnt', 'L_Elbow_Jnt', 'L_Wrist_Jnt'],
        #[1] ['L_Shoulder_Ik_Jnt', 'L_Elbow_Ik_Jnt', 'L_Wrist_Ik_Jnt'],
        #[2] ['L_Shoulder_Fk_Jnt', 'L_Elbow_Fk_Jnt', 'L_Wrist_Fk_Jnt'],
        #[3] ['L_Shoulder_Fk_Ctrl', 'L_Elbow_Fk_Ctrl', 'L_Wrist_Fk_Ctrl'],
        #[4] ['L_Wrist_Ik_Ctrl', 'L_Wrist_Ik_PoleVector_Ctrl', 'L_Shoulder_Ik_Ctrl', 'L_Wrist_Ik_IKrp', 'L_Wrist_Ik_PoleVector_Ctrl_L_Elbow_Ik_Jnt_Connected_Crv', ('L_Wrist_Ik_IKrp_Stretchy_Grp', 'L_Wrist_Ik_IKrp_NormalScale_Loc', ['L_Wrist_Ik_Jnt_Stretchy_Loc'], ['L_Shoulder_Ik_Jnt_Stretchy_Loc'], ['L_Elbow_Ik_Jnt_Stretchy_Loc'], 'L_Shoulder_Ik_Jnt_L_Wrist_Ik_Jnt_Distance_Shape', 'L_Elbow_Ik_Jnt_L_Wrist_Ik_Jnt_Distance_Shape', 'L_Shoulder_Ik_Jnt_L_Elbow_Ik_Jnt_Distance_Shape')], ['L_Shoulder_Fk_Ctrl_Offset_Grp', 'L_Wrist_Ik_Ctrl_Offset_Grp', 'L_Shoulder_Ik_Ctrl_Offset_Grp', 'L_Shoulder_Ik_Jnt_Ctrl_Grp'])
        #[5] ['L_Shoulder_Fk_Ctrl_Offset_Grp', 'L_Wrist_Ik_Ctrl_Offset_Grp', 'L_Shoulder_Ik_Ctrl_Offset_Grp', 'L_Shoulder_Ik_Jnt_Ctrl_Grp'])

        print (ikfk['upper_twist'])
        print (ikfk['lower_twist'])

        clean_rig_grp = cmds.group(em=True, n = side_guide.replace(nc['joint'],'_Rig'+ nc['group']))
        clean_ctrl_grp = cmds.group(em=True, n = side_guide.replace(nc['joint'],nc['ctrl']) + nc['group'])

        cmds.parent(ikfk['upper_twist']['twist_grp'], clean_rig_grp)

        cmds.parent(ikfk['lower_twist']['twist_grp'], clean_rig_grp)

        cmds.parent(ikfk['ik_fk'][0][0], clean_rig_grp)
        cmds.parent(ikfk['ik_fk'][1][0], clean_rig_grp)
        cmds.parent(ikfk['ik_fk'][2][0], clean_rig_grp)

        cmds.parent(ikfk['ik_fk'][4][5][0], clean_rig_grp)
        cmds.parent(cmds.listRelatives(ikfk['ik_fk'][4][3], p=True), clean_rig_grp)

        cmds.scaleConstraint('Rig_Ctrl_Grp' , ikfk['upper_twist']['twist_grp'] ,mo=True)
        cmds.scaleConstraint('Rig_Ctrl_Grp' , ikfk['lower_twist']['twist_grp'] ,mo=True)

        cmds.parent(ikfk['ik_fk'][5][0], clean_ctrl_grp)
        cmds.parent(cmds.listRelatives(ikfk['ik_fk'][4][0], p=True), clean_ctrl_grp)
        cmds.parent(cmds.listRelatives(cmds.listRelatives(ikfk['ik_fk'][4][1], p=True), p=True), clean_ctrl_grp)

        #flip right rig  to right side -------------------------
        #check if the mirror attrs to Only_Right or mirror to True
        if cmds.getAttr('{}.Mirror'.format(config), asString = True) == 'Right_Only':

            mirror_ctrl_grp = mt.mirror_group(clean_ctrl_grp, world = True)
            cmds.parentConstraint(block_parent, ikfk['ik_fk'][5][0] , mo = True)
            cmds.parentConstraint(block_parent, cmds.listRelatives(ikfk['ik_fk'][4][2], p=True) , mo = True)
            clean_ctrl_grp = mirror_ctrl_grp

        elif cmds.getAttr('{}.Mirror'.format(config), asString = True) == 'True':
            ''
            if str(side_guide).startswith(nc['right']) :
                mirror_ctrl_grp = mt.mirror_group(clean_ctrl_grp, world = True)

                cmds.parentConstraint(block_parent, ikfk['ik_fk'][5][0] , mo = True)
                cmds.parentConstraint(block_parent, cmds.listRelatives(ikfk['ik_fk'][4][2], p=True) , mo = True)
                cmds.orientConstraint(block_parent, ikfk['upper_twist']['no_rotate'] , mo = True)

                clean_ctrl_grp = mirror_ctrl_grp
            else:
                cmds.parentConstraint(block_parent, ikfk['ik_fk'][5][0] , mo = True)
                cmds.parentConstraint(block_parent, cmds.listRelatives(ikfk['ik_fk'][4][2], p=True) , mo = True)
                cmds.orientConstraint(block_parent, ikfk['upper_twist']['no_rotate'] , mo = True)

                clean_ctrl_grp = clean_ctrl_grp

        else: #only left side

                cmds.parentConstraint(block_parent, ikfk['ik_fk'][5][0] , mo = True)
                cmds.parentConstraint(block_parent, cmds.listRelatives(ikfk['ik_fk'][4][2], p=True) , mo = True)
                cmds.orientConstraint(block_parent, ikfk['upper_twist']['no_rotate'] , mo = True)

        #blends
        '''
        blends_grp = mt.root_grp(input = '', custom = True, custom_name = 'Blends', autoRoot = False, replace_nc = False)[0]
        blends_grp = blends_grp.replace('_AutoFK','')
        bends = cmds.getAttr('{}.Blends'.format(config).split(':'))
        for blend in bends:
            ''
            #cmds.orientConstraint()
        '''

        #create bind Joints for the skin -------------------------
        #bind joints
        bind_joints = []
        twist_joints = ikfk['upper_twist']['joints'] + ikfk['lower_twist']['joints']
        bind_joint = ''

        for jnt in twist_joints:
            try: cmds.select(bind_joint)
            except:pass
            #bind_joint = mt.duplicate_change_names( input = jnt, hi = False, search=nc['joint'], replace = nc['joint_bind'])[0]
            #cmds.delete(cmds.pickWalk(bind_joints, d='down'))#clean the dirty constraint
            #cmds.delete(cmds.listRelatives(bind_joint, ad=True))
            bind_joint = cmds.joint(n = jnt.replace(nc['joint'], nc['joint_bind']))
            #mt.orient_joint(input=bind_joint)
            cmds.delete(cmds.parentConstraint(jnt, bind_joint, mo=False))
            cmds.delete(cmds.scaleConstraint(jnt, bind_joint, mo=False))
            cmds.makeIdentity(a=True,t=True,s=True,r=True)
            cmds.parentConstraint(jnt, bind_joint, mo=False)
            cmds.scaleConstraint(jnt, bind_joint, mo=True)
            cmds.setAttr('{}.segmentScaleCompensate'.format(bind_joint), 0)
            cmds.setAttr('{}.inheritsTransform'.format(bind_joint), 0)

            #cmds.connectAttr('{}.scaleX'.format(jnt),'{}.scaleX'.format(bind_joint) )
            #cmds.connectAttr('{}.scaleY'.format(jnt),'{}.scaleY'.format(bind_joint) )
            #cmds.connectAttr('{}.scaleZ'.format(jnt),'{}.scaleX'.format(bind_joint) )

            #clean bind joints and radius to 1.5
            print (bind_joint)

            bind_joints.append(bind_joint)
            cmds.setAttr('{}.radius'.format(bind_joint), 2)

        #Finish -------------------------------------------

        #game parents for bind joints
        game_parent = cmds.getAttr('{}.SetGameParent'.format(config))
        if side_guide.startswith(nc['right']):
            game_parent = game_parent.replace(nc['left'],nc['right'])

        if cmds.objExists(game_parent):
            cmds.parent(bind_joints[0], game_parent)

        else:
            bind_jnt_grp = '{}{}'.format(setup['rig_groups']['bind_joints'], nc['group'])
            if cmds.objExists(bind_jnt_grp):
                cmds.parent(bind_joints[0], bind_jnt_grp)

        #clean ctrls
        cmds.parent(clean_ctrl_grp, setup['base_groups']['control']+ nc['group'])
        cmds.parentConstraint('Rig_Ctrl_Grp' , clean_ctrl_grp,mo=True)
        cmds.scaleConstraint('Rig_Ctrl_Grp' , clean_ctrl_grp,mo=True)

        #parent rig
        cmds.parent(clean_rig_grp, '{}{}'.format(setup['rig_groups']['misc'], nc['group']))

        #connected
        cmds.parent(ikfk['ik_fk'][4][4], clean_ctrl_grp)

        #stretchy fixes to make it scalable
        main_jnt_grp = cmds.group(em=True, n = side_guide + '_Main' + nc['group'])
        cmds.parent(main_jnt_grp, cmds.listRelatives(ikfk['ik_fk'][0][0],p=True))
        cmds.parent(ikfk['ik_fk'][0][0], ikfk['ik_fk'][1][0], ikfk['ik_fk'][2][0], main_jnt_grp)

        cmds.scaleConstraint('Global_Ctrl', main_jnt_grp)
