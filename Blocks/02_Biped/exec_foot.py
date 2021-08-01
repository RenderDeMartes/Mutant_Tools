from maya import cmds
import json
import imp
import os

import Mutant_Tools
import Mutant_Tools.Utils
from Mutant_Tools.Utils import main_mutant
imp.reload(Mutant_Tools.Utils.main_mutant)

mt = main_mutant.Mutant()

#---------------------------------------------

TAB_FOLDER = '02_Biped'
PYBLOCK_NAME = 'exec_foot'

#Read name conventions as nc[''] and setup as seup['']
PATH = os.path.dirname(__file__)
PATH = PATH.replace('\Blocks//{}'.format(TAB_FOLDER), '//Config') #change this path depending of the folder

JSON_FILE = (PATH + '/name_conventions.json')
with open(JSON_FILE) as json_file:
    nc = json.load(json_file)
#Read curve shapes info
CURVE_FILE = (PATH + '/curves.json')
with open(CURVE_FILE) as curve_file:
    curve_data = json.load(curve_file)
#setup File
SETUP_FILE = (PATH+'/rig_setup.json')
with open(SETUP_FILE) as setup_file:
    setup = json.load(setup_file)

MODULE_FILE = (os.path.dirname(__file__) +'/07_Foot.json')
with open(MODULE_FILE) as module_file:
    module = json.load(module_file)

#---------------------------------------------

def create_foot_block(name = 'Foot'):

    #name checks and block creation
    name = mt.ask_name(text = module['Name'])
    if cmds.objExists('{}{}'.format(name,nc['module'])):
        cmds.warning('Name already exists.')
        return ''

    block = mt.create_block(name = name, icon = 'Foot',  attrs = module['attrs'], build_command = module['build_command'], import_command = module['import'])
    config = block[1]
    block = block[0]

    ankle = mt.create_joint_guide(name = name + '_Ankle')
    #cmds.setAttr('{}.Helper'.format(ankle), 0)
    cmds.move(2,1.5,-1.5)

    ball = mt.create_joint_guide(name = name + '_Ball')
    cmds.setAttr('{}.Helper'.format(ball), 0)
    cmds.move(2,0.5,0)

    ball_floor = mt.create_joint_guide(name = name + '_BallFloor')
    cmds.setAttr('{}.Helper'.format(ball_floor), 0)
    cmds.move(2,0,0)

    in_floor = mt.create_joint_guide(name = name + '_In')
    cmds.setAttr('{}.Helper'.format(in_floor), 0)
    cmds.move(1,0,0)

    out_floor = mt.create_joint_guide(name = name + '_Out')
    cmds.setAttr('{}.Helper'.format(out_floor), 0)
    cmds.move(3,0,0)

    toes = mt.create_joint_guide(name = name + '_Toes')
    cmds.setAttr('{}.Helper'.format(toes), 0)
    cmds.move(2,0,1.5)

    heel_mid = mt.create_joint_guide(name = name + '_HeelMid')
    cmds.setAttr('{}.Helper'.format(heel_mid), 0)
    cmds.move(2,0,-1.5)

    heel = mt.create_joint_guide(name = name + '_Heel')
    cmds.setAttr('{}.Helper'.format(heel), 0)
    cmds.move(2,0,-2)


    cmds.parent(heel, ankle)
    cmds.parent(toes, ball)
    cmds.parent(ball_floor, ball)
    cmds.parent(in_floor, ball_floor)
    cmds.parent(out_floor, ball_floor)
    cmds.parent(ball, ankle)
    cmds.parent(heel_mid, ankle)
    cmds.parent(ankle, block)

    cmds.select(block)

    print('{} Created Successfully'.format(name))

#create_foot_block()

#-------------------------

def build_foot_block():

    mt.check_is_there_is_base()

    block = cmds.ls(sl=True)
    config = cmds.listConnections(block)[1]
    block = block[0]
    guide = cmds.listRelatives(block, c=True)[0]

    #orient the joints
    mt.orient_joint(input = guide)
    new_guide = mt.duplicate_and_remove_guides(guide)
    print (new_guide)
    to_build = [new_guide]

    #use this group for later cleaning, just assign them when you create the top on hierarchy
    clean_rig_grp = ''
    clean_ctrl_grp = ''

    #get attrs
    ikfk_switch_attr = cmds.getAttr('{}.SwitchIKFKAttr'.format(config), asString=True)
    rfl_attr = cmds.getAttr('{}.IkAttrsPosition'.format(config), asString=True)
    block_parent_ik = cmds.getAttr('{}.SetIKParent'.format(config), asString=True)
    block_parent_fk = cmds.getAttr('{}.SetFKParent'.format(config), asString=True)
    main_ik = cmds.getAttr('{}.IKLeg'.format(config), asString=True)
    size = cmds.getAttr('{}.CtrlSize'.format(config), asString=True)

    #prep work for right side ------------------------------------------------------

    #if mirror is set only to right we need to build on left for mirror behavior then putt it back to righ side
    if cmds.getAttr('{}.Mirror'.format(config), asString = True) == 'Right_Only':
        miror_grp = mt.mirror_group(new_guide, world = True)
        cmds.makeIdentity(miror_grp, a=True, t=True, r=True, s=True)
        cmds.parent(new_guide, w = True)
        cmds.delete(miror_grp)
        mt.orient_joint(input = new_guide)

    elif cmds.getAttr('{}.Mirror'.format(config), asString = True) == 'True':
        right_guide = mt.duplicate_change_names(input = new_guide, hi = True, search=nc['left'], replace =nc['right'])[0]
        to_build.append(right_guide)
        print (to_build)


    #build ------------------------------------------------------
    for side_guide in to_build:

        #smart select the colors
        if str(side_guide).startswith(nc['left']):
            color = setup['left_color']
        elif str(side_guide).startswith(nc['right']):
            color = setup['right_color']
        else:
            color = setup['main_color']


        #main funcion -------------------------------------------
        #change joints order
        all_joints = cmds.listRelatives(side_guide, c=True, ad=True)
        all_joints.insert(0,side_guide)
        print (all_joints)
        rbl_jnts = [all_joints[1], all_joints[3],all_joints[4],all_joints[5],all_joints[7]]

        #all_joints : ['L_Foot_Ankle_Jnt', 'L_Foot_Heel_Jnt', 'L_Foot_Toes_Jnt', 'L_Foot_In_Jnt',
        #              'L_Foot_Out_Jnt', 'L_Foot_BallFloor_Jnt', 'L_Foot_Ball_Jnt', 'L_Foot_HeelMid_Jnt']
        for jnt in all_joints:
            try:cmds.parent(jnt, w=True)
            except:pass

        #hardcoded parents

        cmds.parent(all_joints[6],all_joints[0])
        cmds.parent(all_joints[2],all_joints[6])
        cmds.parent(all_joints[7],all_joints[1])
        cmds.parent(all_joints[5],all_joints[7])
        cmds.parent(all_joints[1],all_joints[3])
        cmds.parent(all_joints[3],all_joints[4])

        #create missing rfl joints

        #create groups for RFL in correct order
        rfl_main_grps = []
        for jnt in rbl_jnts:
            main_grp = cmds.group(em=True, n = jnt.replace(nc['joint'], '_RFL' + nc['group']))
            cmds.delete(cmds.parentConstraint(jnt,main_grp,mo=False))
            rfl_main_grps.append(main_grp)

        for jnt in all_joints[0],all_joints[2],all_joints[6]:
            main_grp = cmds.group(em=True, n = jnt.replace(nc['joint'], '_RFL' + nc['group']))
            cmds.delete(cmds.parentConstraint(jnt,main_grp,mo=False))
            rfl_main_grps.append(main_grp)

        print (rfl_main_grps)

        #hardcoded parents... again
        #['L_Foot_Heel_RFL_Grp' 0 , 'L_Foot_In_RFL_Grp' 1 , 'L_Foot_Out_RFL_Grp' 2 , 'L_Foot_BallFloor_RFL_Grp' 3,
        # 'L_Foot_HeelMid_RFL_Grp' 4 , 'L_Foot_Ankle_RFL_Grp' 5 , 'L_Foot_Toes_RFL_Grp' 6 , 'L_Foot_Ball_RFL_Grp' 7 ]

        cmds.parent(rfl_main_grps[5],rfl_main_grps[7])
        cmds.parent(rfl_main_grps[7],rfl_main_grps[6])
        cmds.parent(rfl_main_grps[6],rfl_main_grps[3])
        cmds.parent(rfl_main_grps[3],rfl_main_grps[4])
        cmds.parent(rfl_main_grps[4],rfl_main_grps[0])
        cmds.parent(rfl_main_grps[0],rfl_main_grps[1])
        cmds.parent(rfl_main_grps[1],rfl_main_grps[2])


        for grp in rfl_main_grps:
            cmds.select(grp)
            autoA = mt.root_grp(autoRoot=True)
            autoB = mt.root_grp()


        #FK IK JOINTS
        cmds.delete(rbl_jnts)

        cmds.select(side_guide)
        ik_joints = mt.duplicate_change_names(input=side_guide, hi=True, search=nc['joint'], replace=nc['ik'])
        cmds.select(side_guide)
        fk_joints = mt.duplicate_change_names(input=side_guide, hi=True, search=nc['joint'], replace=nc['fk'])
        print (ik_joints)#['R_Foot_Ankle_Ik_Jnt', 'R_Foot_Ball_Ik_Jnt', 'R_Foot_Toes_Ik_Jnt']
        print (fk_joints)#['R_Foot_Ankle_Fk_Jnt', 'R_Foot_Ball_Fk_Jnt', 'R_Foot_Toes_Fk_Jnt']


        #fk
        parent_fk = block_parent_fk
        if parent_fk == 'new_locator':
            parent_fk = cmds.spaceLocator(n='{}_ParentFK{}'.format(fk_joints[0], nc['locator']))[0]
        else:
            if parent_fk.startswith(nc['left']) and side_guide.startswith(nc['right']):
                parent_fk = parent_fk.replace(nc['left'], nc['right'])


        #IK
        # create ik handle
        ankle_ikSpline = cmds.ikHandle(sj=ik_joints[0],
                                         ee=ik_joints[1],
                                         sol='ikSCsolver',
                                         n=ik_joints[0].replace(nc['joint'], nc['ik_sc']),
                                         ccv=False,
                                         pcv=False)

        ball_ikSpline = cmds.ikHandle(sj=ik_joints[1],
                                       ee=ik_joints[2],
                                       sol='ikSCsolver',
                                       n= ik_joints[1].replace(nc['joint'], nc['ik_sc']),
                                       ccv=False,
                                       pcv=False)

        cmds.parent(ankle_ikSpline[0], rfl_main_grps[7])
        cmds.parent(ball_ikSpline[0], rfl_main_grps[6])


        #create share controller in case we dont have a switch attr to put it in there
        share_ctrl = mt.curve(input= '',
                              type='circleX',
                              rename=True,
                              custom_name=True,
                              name=side_guide.replace(nc['joint'], '_Share'+nc['ctrl']),
                              size=size)
        share_grp = mt.root_grp()[0]
        mt.match(share_grp, all_joints[6], r=True,t=True)
        cmds.parentConstraint(all_joints[6], share_grp)

        #new toes joint
        cmds.select(cl=True)
        shared_toes_jnt = cmds.joint( n = all_joints[6].replace('_Ball', '_BallToes'))
        cmds.parentConstraint(share_ctrl, shared_toes_jnt, mo=False)

        #parent rfl groups to ik parent
        parent_ik = block_parent_ik
        if parent_ik == 'new_locator':
            parent_ik = cmds.spaceLocator(n = '{}_ParentIK{}'.format(fk_joints[0], nc['locator']))[0]
        else:
            if parent_ik.startswith(nc['left']) and side_guide.startswith(nc['right']):
                parent_ik = parent_ik.replace(nc['left'], nc['right'])

        #cmds.parentConstraint(parent_ik, rfl_main_grps[0], mo=True)
        p = cmds.listRelatives(rfl_main_grps[2], p=True)[0]
        pp = cmds.listRelatives(p, p=True)[0]
        ppp = cmds.listRelatives(pp, p=True)[0]

        #add ik fk ctrl shape
        if ikfk_switch_attr == 'new_attr':
            cmds.select(share_ctrl)
            switch_attr = mt.shape_with_attr(input='', obj_name='{}_Switch'.format(share_ctrl),
                                                   attr_name='Switch_IK_FK')
        else:
            switch_attr = ikfk_switch_attr

        main_joints = cmds.listRelatives(side_guide, c=True, ad=True)
        main_joints.insert(0,side_guide)
        mt.switch_constraints(this=ik_joints[0], that=fk_joints[0], main=main_joints[0], attr=switch_attr)
        mt.switch_constraints(this=ik_joints[1], that=fk_joints[1], main=main_joints[1], attr=switch_attr)
        mt.switch_constraints(this=ik_joints[2], that=fk_joints[2], main=main_joints[2], attr=switch_attr)

        #switch ik fk in the shared ctrl
        #mt.switch_constraints(this=parent_ik, that=parent_fk, main=share_grp, attr=switch_attr)


        #IK RFL Attrs
        if rfl_attr == 'new_locator':
            ik_attrs_shape = cmds.spaceLocator(n = side_guide + '_FootAttrs' + nc['locator'])[0]
        else:
            if rfl_attr.startswith(nc['left']) and side_guide.startswith(nc['right']):
                ik_attrs_shape = rfl_attr.replace(nc['left'], nc['right'])
            else:
                ik_attrs_shape = rfl_attr

        # ['L_Foot_Heel_RFL_Grp' 0 , 'L_Foot_In_RFL_Grp' 1 , 'L_Foot_Out_RFL_Grp' 2 , 'L_Foot_BallFloor_RFL_Grp' 3,
        # 'L_Foot_HeelMid_RFL_Grp' 4 , 'L_Foot_Ankle_RFL_Grp' 5 , 'L_Foot_Toes_RFL_Grp' 6 , 'L_Foot_Ball_RFL_Grp' 7 ]
        rfl_attrs = {'RollToes':'{}.rotateX'.format(cmds.listRelatives(rfl_main_grps[6],p=True)[0]),
                     'PivotToes':'{}.rotateY'.format(cmds.listRelatives(rfl_main_grps[6],p=True)[0]),
                     'PivotBallFloor':'{}.rotateZ'.format(cmds.listRelatives(rfl_main_grps[3],p=True)[0]),
                     'RollBall':'{}.rotateZ'.format(cmds.listRelatives(rfl_main_grps[7],p=True)[0]),
                     'PivotBall':'{}.rotateY'.format(cmds.listRelatives(rfl_main_grps[7],p=True)[0]),
                     'PivotHeelMid':'{}.rotateY'.format(cmds.listRelatives(rfl_main_grps[4],p=True)[0]),
                     'RollHeel':'{}.rotateX'.format(cmds.listRelatives(rfl_main_grps[0],p=True)[0]),
                     'PivotHeel':'{}.rotateY'.format(cmds.listRelatives(rfl_main_grps[0],p=True)[0]),
                     'RollOut':'{}.rotateZ'.format(cmds.listRelatives(rfl_main_grps[2],p=True)[0]),
                     'PivotOut':'{}.rotateY'.format(cmds.listRelatives(rfl_main_grps[2],p=True)[0]),
                     'RollIn':'{}.rotateZ'.format(cmds.listRelatives(rfl_main_grps[1],p=True)[0]),
                     'PivotIn':'{}.rotateY'.format(cmds.listRelatives(rfl_main_grps[1],p=True)[0])
                     }

        mt.line_attr(input = ik_attrs_shape, name = 'RFL', lines = 10)
        for attr in rfl_attrs:
            rfl_temp_attr = mt.new_attr(input= ik_attrs_shape, name = attr, min = -100 , max = 100, default = 0)
            cmds.connectAttr(rfl_temp_attr, rfl_attrs[attr])

        #Foot Roll
        mt.line_attr(input = ik_attrs_shape, name = 'FootRoll', lines = 10)
        break_limit_attr = mt.new_attr(input=ik_attrs_shape, name='BreakRoll', min=-0, max=180, default=45)
        extend_attr = mt.new_attr(input=ik_attrs_shape, name='ExtendRoll', min=-0, max=180, default=90)
        foot_roll_attr = mt.new_attr(input=ik_attrs_shape, name='FootRoll', min=-180, max=180, default=0)

        #Ball
        roll_contidion_node = cmds.shadingNode('condition', asUtility=True, n=side_guide + '_Ball_Limit' + nc['condition'])
        cmds.setAttr(str(roll_contidion_node) + ".operation", 3) #grather equal than
        cmds.connectAttr(break_limit_attr, str(roll_contidion_node) + '.firstTerm')
        cmds.connectAttr(foot_roll_attr, str(roll_contidion_node) + '.secondTerm')
        cmds.connectAttr(foot_roll_attr, str(roll_contidion_node) + '.colorIfTrue.colorIfTrueR')
        cmds.connectAttr(break_limit_attr, str(roll_contidion_node) + '.colorIfFalse.colorIfFalseR')


        #ball negative turn off
        rollneg_contidion_node = cmds.shadingNode('condition', asUtility=True, n=side_guide + '_BallNegative_Limit' + nc['condition'])
        cmds.setAttr(str(rollneg_contidion_node) + ".operation", 2) #grather than
        cmds.setAttr(str(rollneg_contidion_node) + '.secondTerm', 0)
        cmds.setAttr(str(rollneg_contidion_node) + '.outColor.outColorR', 0)

        #reverse ball
        ball_group_attr = '{}.rotateZ'.format(cmds.listRelatives(cmds.listRelatives(rfl_main_grps[7],p=True)[0], p=True)[0])
        mt.connect_md_node(in_x1=str(roll_contidion_node) + '.outColor.outColorR',
                           in_x2=-1.0,
                           out_x=rollneg_contidion_node + '.colorIfTrue.colorIfTrueR'
                           ,mode='mult', name='', force=True)

        cmds.connectAttr(rollneg_contidion_node+'.outColor.outColorR', ball_group_attr)
        cmds.connectAttr(roll_contidion_node+'.outColor.outColorR', rollneg_contidion_node+'.firstTerm')

        #L_Foot_Ball_RFL_Grp_Auto_Grp_Offset_Grp

        #toes
        toes_contidion_node = cmds.shadingNode('condition', asUtility=True, n=side_guide + '_Toes_Limit' + nc['condition'])
        cmds.setAttr(str(toes_contidion_node) + ".operation", 3) #grather equal than
        cmds.connectAttr(break_limit_attr, str(toes_contidion_node) + '.firstTerm')
        cmds.connectAttr(foot_roll_attr, str(toes_contidion_node) + '.secondTerm')

        cmds.setAttr(str(toes_contidion_node) + '.colorIfTrue.colorIfTrueR', 0)

        toes_substract_node = cmds.shadingNode('plusMinusAverage', asUtility=True, n=side_guide + '_Toes_Substract' + nc['plus_minus_average'])
        cmds.setAttr(str(toes_substract_node) + ".operation", 2) #substract
        cmds.setAttr(str(toes_contidion_node) + '.colorIfTrue.colorIfTrueR', 0)

        cmds.connectAttr(toes_substract_node + '.output1D', str(toes_contidion_node) + '.colorIfFalse.colorIfFalseR')
        cmds.connectAttr(break_limit_attr, str(toes_substract_node) + '.input1D[1]')
        cmds.connectAttr(foot_roll_attr, str(toes_substract_node) + '.input1D[0]')

        cmds.connectAttr(str(toes_contidion_node) + '.outColor.outColorR',
         '{}.rotateX'.format(cmds.listRelatives(cmds.listRelatives(rfl_main_grps[6],p=True)[0], p=True)[0]))

        #heel back
        #Heel
        back_heel_contidion_node = cmds.shadingNode('condition', asUtility=True, n=side_guide + '_Toes_Limit' + nc['condition'])
        cmds.setAttr(str(back_heel_contidion_node) + ".operation", 5) #less equal than

        cmds.setAttr(str(back_heel_contidion_node) + '.firstTerm', 0)
        cmds.connectAttr(foot_roll_attr, str(back_heel_contidion_node) + '.secondTerm')
        cmds.setAttr(str(back_heel_contidion_node) + '.colorIfTrue.colorIfTrueR', 0)
        cmds.connectAttr(foot_roll_attr ,str(back_heel_contidion_node) + '.colorIfFalse.colorIfFalseR')

        cmds.connectAttr(str(back_heel_contidion_node) + '.outColor.outColorR',
         '{}.rotateX'.format(cmds.listRelatives(cmds.listRelatives(rfl_main_grps[0],p=True)[0], p=True)[0]))

        #roll reverse
        roll_reverse_contidion_node = cmds.shadingNode('condition', asUtility=True, n=side_guide + '_Toes_Limit' + nc['condition'])
        cmds.setAttr(str(roll_reverse_contidion_node) + ".operation", 3) #grather equal than

        cmds.connectAttr('{}.rotateX'.format(cmds.listRelatives(cmds.listRelatives(rfl_main_grps[6],p=True)[0], p=True)[0]),
                         str(roll_reverse_contidion_node) + '.firstTerm')

        toes_substract_node = cmds.shadingNode('plusMinusAverage', asUtility=True,
                                               n=side_guide + '_Toes_Substract' + nc['plus_minus_average'])
        cmds.setAttr(str(toes_substract_node) + ".operation", 2)  # substract
        cmds.connectAttr(break_limit_attr, str(toes_substract_node) + '.input1D[1]')
        cmds.connectAttr(extend_attr, str(toes_substract_node) + '.input1D[0]')

        cmds.connectAttr(toes_substract_node+'.output1D', str(roll_reverse_contidion_node) + '.secondTerm')

        cmds.connectAttr(toes_substract_node+'.output1D', str(roll_reverse_contidion_node) + '.colorIfTrue.colorIfTrueR')
        cmds.connectAttr('{}.rotateX'.format(cmds.listRelatives(cmds.listRelatives(rfl_main_grps[6],p=True)[0], p=True)[0]),
                        str(roll_reverse_contidion_node) + '.colorIfFalse.colorIfFalseR')


        cmds.connectAttr(roll_reverse_contidion_node + '.outColor.outColorR',
                         '{}.rotateZ'.format(rfl_main_grps[7]))


        #create bind Joints for the skin -------------------------
        ankle_bind_joint = cmds.duplicate(main_joints[0], po=True, n = main_joints[0].replace(nc['joint'], nc['joint_bind']))[0]
        cmds.parentConstraint(main_joints[0], ankle_bind_joint, mo = False)
        try: cmds.parent(ankle_bind_joint, w=True)
        except:pass
        cmds.setAttr('{}.radius'.format(ankle_bind_joint), 1.5)

        ball_bind_joint = cmds.duplicate(shared_toes_jnt, po=True, n = shared_toes_jnt.replace(nc['joint'], nc['joint_bind']))[0]
        cmds.parentConstraint(shared_toes_jnt, ball_bind_joint, mo = False)
        cmds.parent(ball_bind_joint, ankle_bind_joint)
        cmds.setAttr('{}.radius'.format(ball_bind_joint), 1.5)


        #flip right rig  to right side -------------------------

        '''
        #check if the mirror attrs to Only_Right or mirror to True
        if cmds.getAttr('{}.Mirror'.format(config), asString = True) == 'Right_Only':
            miror_ctrl_grp = mt.mirror_group(cmds.listRelatives(auto_grp, p=True)[0], world = True)
            miror_jnt_grp = mt.mirror_group(new_guide, world = True)
            cmds.parentConstraint(block_parent, miror_ctrl_grp , mo = True)
            clean_rig_grp = miror_jnt_grp
            clean_ctrl_grp = miror_ctrl_grp

        elif cmds.getAttr('{}.Mirror'.format(config), asString = True) == 'True':
            if str(side_guide).startswith(nc['right']) :
                miror_ctrl_grp = mt.mirror_group(cmds.listRelatives(auto_grp, p=True)[0], world = True)
                miror_jnt_grp = mt.mirror_group(side_guide, world = True)
                cmds.parentConstraint(block_parent, miror_ctrl_grp , mo = True)
                clean_rig_grp = miror_jnt_grp
                clean_ctrl_grp = miror_ctrl_grp
            else:
                cmds.parentConstraint(block_parent, for_parent , mo = True)
                clean_rig_grp = side_guide
                clean_ctrl_grp = for_parent

        else: #only left side
            cmds.parentConstraint(block_parent, for_parent , mo = True)

        '''
        #blends
        '''
        blends_grp = mt.root_grp(input = '', custom = True, custom_name = 'Blends', autoRoot = False, replace_nc = False)[0]
        blends_grp = blends_grp.replace('_AutoFK','')
        bends = cmds.getAttr('{}.Blends'.format(config).split(':'))
        for blend in bends:
            ''
            #cmds.orientConstraint()
        '''

        #Finish -------------------------------------------
        '''
        #game parents for bind joints
        game_parent = cmds.getAttr('{}.SetGameParent'.format(config))
        if side_guide.startswith(nc['right']):
            game_parent = game_parent.replace(nc['left'],nc['right'])

        if cmds.objExists(game_parent):
            cmds.parent(bind_joint, game_parent)
        else:
            bind_jnt_grp = '{}{}'.format(setup['rig_groups']['bind_joints'], nc['group'])
            if cmds.objExists(bind_jnt_grp):
                cmds.parent(bind_joint, bind_jnt_grp)

        #clean ctrls
        cmds.parent(clean_ctrl_grp, 'Rig_Ctrl_Grp')

        #parent rig
        cmds.parent(clean_rig_grp, '{}{}'.format(setup['rig_groups']['misc'], nc['group']))

        '''  

        #parents at the end

        if main_ik == 'new_locator':
            cmds.parent(cmds.spaceLocator(n = ik_joints[0].replace(nc['joint'],'_Here')), rfl_main_grps[5])
        else:
            if main_ik.startswith(nc['left']) and side_guide.startswith(nc['right']):
                pc_ik = cmds.listRelatives(main_ik.replace(nc['left'], nc['right']),c=True)
                cmds.delete(pc_ik)
                cmds.parent(main_ik.replace(nc['left'], nc['right']), rfl_main_grps[5])
            else:
                pc_ik = cmds.listRelatives(main_ik, c=True)[0]
                cmds.delete(pc_ik)
                cmds.parent(main_ik, rfl_main_grps[5])

        cmds.parentConstraint(parent_ik.replace(nc['ctrl'], nc['joint']), ik_joints[0], mo=True)
        cmds.parentConstraint(parent_ik, ppp, mo =True)
        cmds.parentConstraint(parent_fk, fk_joints[0], mo=True)


    #clean a bit
    clean_rig_grp = cmds.group(em=True, n = '{}{}'.format(block.replace(nc['module'],'_Rig'), nc['group']))


    # build complete ----------------------------------------------------
    print ('Build {} Success'.format(block))


#build_foot_block()
