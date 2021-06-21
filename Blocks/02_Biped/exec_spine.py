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
PYBLOCK_NAME = 'exec_spine'

#Read name conventions as nc[''] and setup as setup['']
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

MODULE_FILE = (os.path.dirname(__file__) +'/01_Spine.json')
with open(MODULE_FILE) as module_file:
	module = json.load(module_file)

#---------------------------------------------

def create_spine_block(name = 'Spine'):

    #name checks and block creation
    name = mt.ask_name(text = module['Name'])
    if cmds.objExists('{}{}'.format(name,nc['module'])):
        cmds.warning('Name already exists.')
        return ''

    block = mt.create_block(name = name, icon = 'Spine',  attrs = module['attrs'], build_command = module['build_command'], import_command = module['import'])
    config = block[1]
    block = block[0]
    
    cmds.select(cl=True)
    spineBase_guide = mt.create_joint_guide(name = name + '_Base')
    cmds.parent(spineBase_guide, block)
    spineInv_guide = mt.create_joint_guide(name = name + '_Inv')
    cmds.move(0,-1,0)
    spineBelly_guide = mt.create_joint_guide(name = name + '_Belly')
    cmds.move(0,2,0)
    spineChest_guide = mt.create_joint_guide(name = name + '_Chest')
    cmds.move(0,4,0)
    spineEnd_guide = mt.create_joint_guide(name = name + '_End')
    cmds.move(0,6,0)

    cmds.parent(spineBelly_guide,spineBase_guide)
    cmds.parent(spineChest_guide,spineBelly_guide)
    cmds.parent(spineEnd_guide,spineChest_guide)
    cmds.parent(spineInv_guide,spineBase_guide)

    cmds.select(block)
    #mt.orient_joint(input = spineBase_guide)
    #cmds.setAttr("{}.jointOrientX".format(spineInv_guide), 0)
    #cmds.setAttr("{}.jointOrientY".format(spineInv_guide), 0)
    #cmds.setAttr("{}.jointOrientZ".format(spineInv_guide), 0)

    print('{} Created Successfully'.format(name))

#create_spine_block()

#-------------------------

def build_spine_block():

    mt.check_is_there_is_base()

    block = cmds.ls(sl=True)
    config = cmds.listConnections(block)[1]
    block = block[0]
    guide = cmds.listRelatives(block, c=True)[0]
    name = block.replace(nc['module'],'')

    ctrl_size = cmds.getAttr('{}.CtrlSize'.format(config))
    #cmds.getAttr('{}.AttrName'.format(config), asString = True)

    #groups for later cleaning
    clean_rig_grp = ''
    clean_ctrl_grp = ''

    #orient the joints
    mt.orient_joint(input = guide)
    new_guide = mt.duplicate_and_remove_guides(guide)

    cmds.setAttr('{}_End{}.jointOrientX'.format(name, nc['joint']), 0)
    cmds.setAttr('{}_End{}.jointOrientY'.format(name, nc['joint']), 0)
    cmds.setAttr('{}_End{}.jointOrientZ'.format(name, nc['joint']), 0)


    #use this locator in case parent is set to new locator
    if cmds.getAttr('{}.SetParent'.format(config)) == 'new_locator':
        block_parent = cmds.spaceLocator( n = '{}'.format(str(block).replace(nc['module'],'_Parent' + nc['locator'])))
    else:
        block_parent = cmds.getAttr('{}.SetParent'.format(config))

    spine_joints = [ new_guide,
                    '{}_Belly{}'.format(name, nc['joint']),
                    '{}_Chest{}'.format(name, nc['joint']),
                    '{}_End{}'.format(name, nc['joint']),
                    '{}_Inv{}'.format(name, nc['joint']),
                     ]


    #build
    cv_divisions =  3
    #create ik handle
    ikSpline = cmds.ikHandle(sj=new_guide,
                             ee='{}_End{}'.format(name, nc['joint']),
                             sol='ikSplineSolver',
                             n= block.replace(nc['module'],nc['ik_spline']),
                             ccv=True,
                             pcv = False)

    spline_curve =  ikSpline[2]
    spline_curve = cmds.rename(spline_curve, name + nc['curve'])
    spline_curve = cmds.rebuildCurve(spline_curve, ch =  True,  rpo = True, rt = False, end =True, kr = False, kcp = False, kep = True , kt =False, s = cv_divisions, d = 3, tol = 0.01)[0]

    effector_spline = cmds.rename(ikSpline[1],
                                  name + nc['effector'])
    ikSpline = ikSpline[0]

    #move cv to fit the joints
    belly_pos = cmds.xform('{}_Belly{}'.format(name, nc['joint']), q=True, ws=True, t=True)
    cmds.move(belly_pos[0],belly_pos[1],belly_pos[2],'{}.cv[2]'.format(spline_curve))
    chest_pos = cmds.xform('{}_Chest{}'.format(name, nc['joint']), q=True, ws=True, t=True)
    cmds.move(chest_pos[0],chest_pos[1],chest_pos[2],'{}.cv[3]'.format(spline_curve))

    #do ctrl joints to bind to the cv
    print ('Spine Joints:')
    ctrl_joints = []
    for jnt in spine_joints[:-1]:

        cmds.select(cl=True)
        print(jnt)
        ctrl_jnt = cmds.joint(n = jnt.replace(nc['joint'], nc['joint_ctrl']), rad = 1.25)
        cmds.delete(cmds.parentConstraint(jnt, ctrl_jnt, mo=False))    
        ctrl_joints.append(ctrl_jnt)

    cmds.skinCluster(ctrl_joints[:-1], spline_curve, tsb=True)

    #create controllers
    spine_ctrls = []

    cmds.select(cl=True)
    base_ctrl = mt.curve(input = '',
                         type = 'cube', rename = True,
                         custom_name = True,
                         name = str(ctrl_joints[0]).replace(nc['joint_ctrl'],nc['ctrl']),
                         size = ctrl_size)
    mt.assign_color(color = 'yellow')
    base_offset = mt.root_grp()
    mt.match(base_offset,ctrl_joints[0], t=True, r=False)
    cmds.parentConstraint(base_ctrl, ctrl_joints[0], mo=True)
    cmds.parentConstraint(base_ctrl, spine_joints[-1], mo=True)
    spine_ctrls.append(base_ctrl)

    cmds.select(cl=True)
    chest_ctrl = mt.curve(input = '',
                         type = 'cube', rename = True,
                         custom_name = True,
                         name = str(ctrl_joints[2]).replace(nc['joint_ctrl'], nc['ctrl']),
                         size = ctrl_size)
    mt.assign_color(color = 'yellow')
    chest_offset = mt.root_grp()
    mt.match(chest_offset,ctrl_joints[2], t=True, r=False)
    cmds.parentConstraint(chest_ctrl, ctrl_joints[2], mo=True)
    cmds.parentConstraint(chest_ctrl, ctrl_joints[3], mo=True)
    spine_ctrls.append(chest_ctrl)

    cmds.select(cl=True)
    belly_ctrl = mt.curve(input = '',
                         type = 'octagon', rename = True,
                         custom_name = True,
                         name = str(ctrl_joints[1]).replace(nc['joint_ctrl'], nc['ctrl']),
                         size = ctrl_size)
    mt.assign_color(color = 'green')
    belly_offset = mt.root_grp()
    mt.match(belly_offset,ctrl_joints[1], t=True, r=False)
    cmds.parentConstraint(belly_ctrl, ctrl_joints[1], mo=True)
    spine_ctrls.append(belly_ctrl)

    #FK Belly Ctrl
    cmds.select(cl=True)
    belly_fk_ctrl = mt.curve(input = '',
                         type = 'square', rename = True,
                         custom_name = True,
                         name = str(ctrl_joints[1]).replace(nc['joint_ctrl'],'_FK' + nc['ctrl']),
                         size = ctrl_size*1.25)
    mt.assign_color(color = 'lightBlue')
    belly_fk_offset = mt.root_grp()
    mt.match(belly_fk_offset,ctrl_joints[1], t=True, r=False)
    spine_ctrls.append(belly_fk_ctrl)

    #FK Base Ctrl
    cmds.select(cl=True)
    base_fk_ctrl = mt.curve(input = '',
                         type = 'square', rename = True,
                         custom_name = True,
                         name = str(ctrl_joints[0]).replace(nc['joint_ctrl'],'_FK' + nc['ctrl']),
                         size = ctrl_size*1.25)

    mt.assign_color(color = 'lightBlue')
    base_fk_offset = mt.root_grp()
    mt.match(base_fk_ctrl,ctrl_joints[0], t=True, r=False)
    spine_ctrls.append(base_fk_ctrl)

    cmds.parent(belly_fk_offset,base_fk_ctrl)
    cmds.parent(belly_offset,belly_fk_ctrl)
    cmds.parent(chest_offset,belly_fk_ctrl)

    #parent end
    cmds.orientConstraint(chest_ctrl,'{}_End{}'.format(name, nc['joint']), mo=True)


    #Twist Joints
    cmds.select(ctrl_joints[0])
    start_twist_jnt = cmds.joint(n='{}_Base{}'.format(name, nc['joint_twist']), rad=1.35)
    cmds.delete(cmds.parentConstraint('{}_Base{}'.format(name, nc['joint']),start_twist_jnt, mo=False))
    cmds.select(ctrl_joints[3])
    end_twist_jnt = cmds.joint(n='{}_End{}'.format(name, nc['joint_twist']), rad=1.35)
    cmds.delete(cmds.parentConstraint('{}_End{}'.format(name, nc['joint']),end_twist_jnt, mo=False))

    #Enable twist
    cmds.setAttr("{}.dTwistControlEnable".format(ikSpline), 1)
    cmds.setAttr("{}.dWorldUpType".format(ikSpline), 4)
    cmds.connectAttr("{}.worldMatrix[0]".format(start_twist_jnt), "{}.dWorldUpMatrix".format(ikSpline), f=True)
    cmds.connectAttr("{}.worldMatrix[0]".format(end_twist_jnt), "{}.dWorldUpMatrixEnd".format(ikSpline), f=True)

    #Shape attrs
    # add attrs in all controllers
    for ctrl in spine_ctrls:
        cmds.select(ctrl)
        if cmds.objectType(ctrl) == 'transform':
            spine_attrs = mt.shape_with_attr(input='', obj_name='{}_Attrs'.format(name), attr_name='BellyMid')

    cmds.addAttr(spine_attrs, e=1, dv=0.5)
    cmds.setAttr(spine_attrs, 0.5)


    #add AttrsStretchyMult
    mt.line_attr(input= spine_attrs.split('.')[0],name = 'SnS')
    stretchy_attr =mt.new_attr(input= spine_attrs.split('.')[0], name = 'Stretchy', min = 0 , max = 1, default = 1)

    preserve_volume = mt.new_attr(input= stretchy_attr.split('.')[0], name = 'Volume', min = 0 , max = 1, default = 1)
    offset_attr = mt.new_attr(input= stretchy_attr.split('.')[0], name = 'OffsetStretchy', min = -10 , max = 10, default = 0)

    mt.line_attr(input=stretchy_attr.split('.')[0], name='Stretch')
    chest_stretch = mt.new_attr(input=stretchy_attr.split('.')[0], name='ChestStretch', min=0, max=10, default=1)
    belly_stretch = mt.new_attr(input=stretchy_attr.split('.')[0], name='BellyStretch', min=0, max=10, default=1)
    base_stretch = mt.new_attr(input=stretchy_attr.split('.')[0], name='BaseStretch', min=0, max=10, default=1)

    mt.line_attr(input= stretchy_attr.split('.')[0],name = 'Volume')
    chest_volume =mt.new_attr(input= stretchy_attr.split('.')[0], name = 'ChestVolume', min = 0.01 , max = 10, default = 1)
    belly_volume =mt.new_attr(input= stretchy_attr.split('.')[0], name = 'BellyVolume', min = 0.01 , max = 10, default = 1)
    base_volume =mt.new_attr(input= stretchy_attr.split('.')[0], name = 'BaseVolume', min = 0.01 , max = 10, default = 1)

    #Stretchy
    '''
    curve_info_node = cmds.shadingNode("curveInfo", asUtility = True, n = name + "_curveInfo_Node")
    cmds.connectAttr('{}.worldSpace[0]'.format(cmds.listRelatives(spline_curve,shapes=True)[0]),'{}.inputCurve'.format(curve_info_node),f=True)
    original_len = cmds.getAttr('{}.arcLength'.format(curve_info_node))

    condition_node = cmds.shadingNode("condition", asUtility = True, n = name + "_Stretch_Condition_Node")
    cmds.setAttr(condition_node + '.operation', 2 )
    cmds.setAttr(condition_node + '.secondTerm', original_len)
    cmds.connectAttr('{}.arcLength'.format(curve_info_node), condition_node + '.firstTerm')

    mult_offset = mt.connect_md_node(in_x1=original_len, in_x2 = offset_attr, out_x= condition_node + '.secondTerm', mode='mult', name= 'OffsetMult', force=False)

    new_scale_offset = mt.connect_md_node(in_x1='{}.arcLength'.format(curve_info_node), in_x2 = original_len, out_x= condition_node + '.colorIfTrueR', mode='divide', name= 'NewScale', force=False)
    '''

    curve_info_node = cmds.shadingNode("curveInfo", asUtility = True, n = name + "_curveInfo_Node")
    cmds.connectAttr('{}.worldSpace[0]'.format(cmds.listRelatives(spline_curve,shapes=True)[0]),'{}.inputCurve'.format(curve_info_node),f=True)
    arch_lenght_attr = '{}.arcLength'.format(curve_info_node)
    original_len = cmds.getAttr(arch_lenght_attr)

    #normalize
    normalize_loc = cmds.spaceLocator(n = name + '_Normalize' + nc['locator'])[0]
    normalize_node = mt.connect_md_node(in_x1= arch_lenght_attr,
                                   in_x2 = normalize_loc + '.scaleX',
                                   out_x= '',
                                   mode='divide',
                                   name= 'Normalize',
                                   force=False)

    stretchy_divide = mt.connect_md_node(in_x1=  normalize_node + '.output.outputX',
                                   in_x2 = original_len,
                                   out_x= '',
                                   mode='divide',
                                   name= 'StretchyDivide',
                                   force=False)

    squash_inv_node = mt.connect_md_node(in_x1=stretchy_divide + '.output.outputX',
                                         in_x2=0.5,
                                         out_x='',
                                         mode='power',
                                         name='SquashInvPower',
                                         force=False)

    squash_dive_node = mt.connect_md_node(in_x1=1,
                                         in_x2= squash_inv_node + '.output.outputX',
                                         out_x='',
                                         mode='divide',
                                         name='SquashDivide',
                                         force=False)

    attr_toX = stretchy_divide + '.output.outputX'
    attr_toYZ = squash_dive_node + '.output.outputX'
    volume_nodes = []
    #connect to joints
    for jnt in spine_joints[:-2]:
        spine_squash_md = mt.connect_md_node(in_x1=attr_toX,
                                      in_x2= stretchy_attr.split('.')[0] +'.' +jnt.split('_')[1]+'Stretch',
                                      out_x= jnt + '.scaleX',
                                      mode='mult',
                                      name='{}_SquashExtra'.format(jnt),
                                      force=False)

        spine_volume_md = mt.connect_md_node(in_x1=attr_toYZ,
                                      in_x2= stretchy_attr.split('.')[0] +'.' +jnt.split('_')[1]+'Volume',
                                      out_x= jnt + '.scaleY',
                                      mode='mult',
                                      name='{}_SquashExtra'.format(jnt),
                                      force=False)
        volume_nodes.append(spine_volume_md)
        cmds.connectAttr(spine_volume_md + '.output.outputX', jnt + '.scaleZ' )

        #connectExtra

    #turn off on stretch offset and volume
    #stretch
    blendColors = cmds.shadingNode('blendColors', asUtility=True, name = name + '_OffOnStretch'+ nc['blend'])
    cmds.connectAttr('{}.output.outputX'.format(normalize_node), '{}.color1.color1R'.format(blendColors), f=True)
    cmds.connectAttr('{}.output.outputR'.format(blendColors), '{}.input1.input1X'.format(stretchy_divide), f=True)
    cmds.setAttr('{}.color2.color2R'.format(blendColors),original_len)
    cmds.connectAttr(stretchy_attr, '{}.blender'.format(blendColors),f=True)
    #volume
    for node in volume_nodes:
        blendColors_volume = cmds.shadingNode('blendColors', asUtility=True, name=name + '_OffOnVolume' + nc['blend'])
        cmds.connectAttr('{}.output.outputX'.format(node), '{}.color1.color1R'.format(blendColors_volume), f=True)
        jnt_name = cmds.listConnections(node,d=True,  et=True,t='joint',s=False)[0]
        cmds.connectAttr('{}.output.outputR'.format(blendColors_volume), '{}.scaleY'.format(jnt_name), f=True)
        cmds.connectAttr('{}.output.outputR'.format(blendColors_volume), '{}.scaleZ'.format(jnt_name), f=True)
        cmds.setAttr('{}.color2.color2R'.format(blendColors_volume), 1)
        cmds.connectAttr(preserve_volume, '{}.blender'.format(blendColors_volume), f=True)

    #offsetStretch
    double_linear_add = cmds.shadingNode('addDoubleLinear', asUtility=True, name = name + '_OffsetAdd')
    cmds.connectAttr('{}.output.outputX'.format(normalize_node), '{}.input1'.format(double_linear_add), f=True)
    cmds.connectAttr('{}.output'.format(double_linear_add), '{}.color1.color1R'.format(blendColors), f=True)
    cmds.connectAttr(offset_attr, '{}.input2'.format(double_linear_add),f=True)

    #Breath
    chest_volume_nodes = volume_nodes[2]
    #2.5 seg inhale 2.5 exale
    print('Breathing...')

    mt.line_attr(input= stretchy_attr.split('.')[0],name = 'Breath')
    breath_auto =mt.new_attr(input= stretchy_attr.split('.')[0], name = 'BreathAuto', min = 0 , max = 1, default = 0)
    breath_frequency  =mt.new_attr(input= stretchy_attr.split('.')[0], name = 'BreathFrequency', min = 0 , max = 10, default = 2.5)
    breath_amount =mt.new_attr(input= stretchy_attr.split('.')[0], name = 'BreathAmount', min = 0.1 , max = 10, default = 1)
    breath_chest =mt.new_attr(input= stretchy_attr.split('.')[0], name = 'BreathChest', min = 0 , max = 10, default = 1)
    breath_belly=mt.new_attr(input= stretchy_attr.split('.')[0], name = 'BreathBelly', min = 0 , max = 10, default = 0.5)
    chest_rotate=mt.new_attr(input= stretchy_attr.split('.')[0], name = 'ChestRotate', min = 0 , max = 10, default = 2.5)


    #create add Nodes to automate the breathe
    belly_volume_nodes = volume_nodes[1]
    chest_volume_nodes = volume_nodes[1]

    add_x_belly = mt.replace_connection_with_doublelinear(input = '{}_Belly{}'.format(name, nc['joint']),
                                            attr = 'scaleX',
                                            name = 'Belly_Breath_Add_X')

    add_yz_belly = mt.replace_connection_with_doublelinear(input = '{}_Belly{}'.format(name, nc['joint']),
                                            attr = 'scaleY',
                                            name = 'Belly_Breath_Add_YZ')

    cmds.connectAttr('{}.output'.format(add_yz_belly), '{}_Belly{}'.format(name, nc['joint']) + '.scaleZ', f=True)

    add_x_chest = mt.replace_connection_with_doublelinear(input = '{}_Chest{}'.format(name, nc['joint']),
                                            attr = 'scaleX',
                                            name = 'Chest_Breath_Add_X')

    add_yz_chest = mt.replace_connection_with_doublelinear(input = '{}_Chest{}'.format(name, nc['joint']),
                                            attr = 'scaleY',
                                            name = 'Chest_Breath_Add_YZ')
    cmds.connectAttr('{}.output'.format(add_yz_chest), '{}_Chest{}'.format(name, nc['joint']) + '.scaleZ', f=True)

    #chest rotation
    chest_offset = mt.root_grp(input = chest_ctrl, custom = True, custom_name = '{}_Chest_Breath_{}'.format(name, nc['group']))[0]

    #breathing expression
    breath_exp = cmds.expression(n = name + '_breath' + nc['expression'],
                                 s= """//Breath_attrs
                                        $freq = {}/2;
                                        $amount = {} * {};
                                        $breath = sin(time*$freq)*$amount;
                                        //Apply_it_to_the_nodes
                                        {}.input2 = $breath * 0.07 *{};
                                        {}.input2 = $breath * 0.07 *{};
                                        {}.input2 = $breath * 0.07 *{};
                                        {}.input2 = $breath * 0.07 *{};
                                        {}.rotateX = -1 * sin(time*$freq*$amount)*$amount*{}-{}/2;
                                        """.format(breath_frequency,
                                                   breath_amount,
                                                   breath_auto,
                                                   add_x_belly,  breath_belly,
                                                   add_yz_belly, breath_belly,
                                                   add_x_chest,  breath_chest,
                                                   add_yz_chest, breath_chest,
                                                   chest_offset, chest_rotate,chest_rotate
                                                   ).replace(' ', '')
                                 )

    #clean a bit
    clean_rig_grp = cmds.group(em=True, n = '{}{}'.format(block.replace(nc['module'],'_Rig'), nc['group']))

    print ('Build {} Success'.format(block))



#build_spine_block()

"""
Stretchy
COG as option?

"""