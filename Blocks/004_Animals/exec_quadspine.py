from __future__ import absolute_import
from __future__ import division
from maya import cmds
import json
import string
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

#---------------------------------------------

TAB_FOLDER = '004_Animals'
PYBLOCK_NAME = 'exec_quadspine'

#---------------------------------------------

def create_quadspine_block(name = 'QuadSpine'):

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

    MODULE_FILE = os.path.join(os.path.dirname(__file__), '05_QuadSpine.json')
    with open(MODULE_FILE) as module_file:
        module = json.load(module_file)

    nc, curve_data, setup = mt.import_configs()

    #---------------------------------------------------
    #---------------------------------------------------
    #---------------------------------------------------

    name = mt.ask_name(text=module['Name'])
    if cmds.objExists('{}{}'.format(name, nc['module'])):
        cmds.warning('Name already exists.')
        return ''
    #amount = mt.ask_name(text=7, ask_for = 'Joints Amount, needs to be Odd (5,7,9...)')
    amount=7
    check_odd = int(amount) / 2
    print(check_odd)
    if check_odd == 0:
        cmds.warning('Needs to be an odd Number')
        return False

    block = mt.create_block(name=name, icon='QuadSpine', attrs=module['attrs'], build_command=module['build_command'],
                            import_command=module['import'])
    config = block[1]
    block = block[0]

    alphabet = string.ascii_uppercase

    past_guide = None
    x_pos = 0
    for num in range(int(amount)):
        cmds.select(cl=True)
        guide = mt.create_joint_guide(name=name+'_'+alphabet[num])
        cmds.move(0,0,x_pos)
        if not past_guide:
            cmds.parent(guide,block)
        else:
            cmds.parent(guide,past_guide)
        past_guide=guide
        x_pos = x_pos+2

    cmds.select(block)

    # mt.orient_joint(input = spineBase_guide)
    # cmds.setAttr("{}.jointOrientX".format(spineInv_guide), 0)
    # cmds.setAttr("{}.jointOrientY".format(spineInv_guide), 0)
    # cmds.setAttr("{}.jointOrientZ".format(spineInv_guide), 0)

    print('{} Created Successfully'.format(name))

#create_quadspine_block()

#-------------------------

def build_quadspine_block():

    nc, curve_data, setup = mt.import_configs()

    mt.check_is_there_is_base()

    block = cmds.ls(sl=True)
    config = cmds.listConnections(block)[1]
    block = block[0]
    guide = cmds.listRelatives(block, c=True)[0]
    name = block.replace(nc['module'],'')


    #cmds.getAttr('{}.AttrName'.format(config))
    #cmds.getAttr('{}.AttrName'.format(config), asString = True)

    #orient the joints
    new_guide = mt.duplicate_and_remove_guides(guide)
    to_build = [new_guide]
    mt.orient_joint(input = new_guide)

    #use this locator in case parent is set to new locator
    if cmds.getAttr('{}.SetParent'.format(config)) == 'new_locator':
        block_parent = cmds.spaceLocator( n = '{}'.format(str(block).replace(nc['module'],'_Parent' + nc['locator'])))
    else:
        block_parent = cmds.getAttr('{}.SetParent'.format(config))

    ctrl_size = cmds.getAttr('{}.CtrlSize'.format(config))

    forward_color = 'green'
    backward_color = 'purple'
    ik_color = 'lightBlue'


    #Build

    #Get spine joints
    alphabet = string.ascii_uppercase
    spine_joints=[]
    num = 0
    while cmds.objExists(name+'_'+alphabet[num]+nc['joint']):
        spine_joints.append(name+'_'+alphabet[num]+nc['joint'])
        num = num+1
    print('Spine Joints:', spine_joints)
    back_distance = cmds.getAttr(spine_joints[-2] + '.translateZ')

    #Create curves
    cv_xforms = []
    k = []
    skip = False
    ik_nums = []
    fk_joints = []
    #Do every other joint
    for num, j in enumerate(spine_joints):
        cmds.makeIdentity(j, a=True, t=True, r=True, s=True) #Orient
        if skip:
            skip=False
            fk_joints.append(j)
            continue
        print(j)
        xform = cmds.xform(j, q=True, ws=True, t=True)
        cv_xforms.append(xform)
        k.append(num)
        ik_nums.append(num)
        skip=True

    print(cv_xforms, k)

    #Fix lats spine orient
    cmds.setAttr("{}.jointOrientX".format(spine_joints[-1]), 0)
    cmds.setAttr("{}.jointOrientY".format(spine_joints[-1]), 0)
    cmds.setAttr("{}.jointOrientZ".format(spine_joints[-1]), 0)


    spine_cv = cmds.curve(d=3, p=cv_xforms, #k=k,
                          n=name + '_Main' + nc['curve'])
    spine_cv = cmds.rebuildCurve(keepRange=0, ch=False, rebuildType=3, kcp=1, kep=1, kt=0, s=k[-1], d=3, tol=0.01)[0]
    spine_cv_shape = cmds.listRelatives(spine_cv, s=True)[0]
    cmds.setAttr('{}.inheritsTransform'.format(spine_cv), 0)

    ik_spline = cmds.ikHandle(sj=spine_joints[0],
                              ee=spine_joints[-1],
                              sol='ikSplineSolver',
                              n=name + nc['ik_sc'],
                              createCurve=False,
                              parentCurve=False,
                              c=spine_cv
                              )
    ik_spline_curve = ik_spline[-1]
    ik_spline = ik_spline[0]

    #Create Ctrls

    # ik ctrls and clusters
    ik_clusters = []
    ik_ctrls = []
    ik_roots = []

    for num in range(len(ik_nums)):
        if num == 0 or num+1 == len(ik_nums):
            ctrl_shape = 'cube'
            size=ctrl_size
        else:
            ctrl_shape = 'sphere'
            size = ctrl_size*0.75
        cmds.select('{}.cv[{}]'.format(spine_cv, num))
        cluster = cmds.cluster(n='{}_{}{}'.format(name, num, nc['cluster']))[1]
        ik_clusters.append(cluster)
        ctrl = mt.curve(input=cluster,
                        type=ctrl_shape,
                        rename=True,
                        custom_name=True,
                        name=cluster.replace(nc['cluster']+'Handle', '_Ik'+nc['ctrl']),
                        size=size)

        mt.assign_color(color=ik_color)
        root_grp = mt.root_grp()[0]
        mt.match(root_grp, cluster, r=True, t=True)
        cmds.parentConstraint(ctrl, cluster, mo=True)
        ik_ctrls.append(ctrl)
        ik_roots.append(root_grp)
        if ctrl_shape == 'sphere':
            mt.hide_attr(ctrl, s=True, r=True, rotate_order=True)
        else:
            mt.hide_attr(ctrl, s=True)


    #Fk Ctrls
    forward_ctrls = []
    for num, joint in enumerate(fk_joints):
        ctrl = mt.curve(input=joint,
                        type='cylinder',
                        rename=True,
                        custom_name=True,
                        name=name+'_'+str(num)+'_Frw'+nc['ctrl'],
                        size=ctrl_size*0.90)
        mt.rotate_shape(input=ctrl, z=90)
        mt.scale_shape(input=ctrl, x=0.5)
        mt.assign_color(color=forward_color)
        root_grp = mt.root_grp()[0]
        mt.hide_attr(ctrl, s=True)

        if len(forward_ctrls) > 0:
            cmds.parent(root_grp, forward_ctrls[-1])
        forward_ctrls.append(ctrl)

        mt.match(root_grp, joint, r=True, t=True)

    backwards_ctrls = []
    for num, joint in enumerate(reversed(fk_joints)):
        ctrl = mt.curve(input=joint,
                        type='cylinder',
                        rename=True,
                        custom_name=True,
                        name=name+'_'+str(num)+'_Bkw'+nc['ctrl'],
                        size=ctrl_size*0.80)
        mt.rotate_shape(input=ctrl, z=90)
        mt.scale_shape(input=ctrl, x=0.5)
        mt.assign_color(color=backward_color)
        root_grp = mt.root_grp()[0]
        mt.hide_attr(ctrl, s=True)
        if len(backwards_ctrls) > 0:
            cmds.parent(root_grp, backwards_ctrls[-1])
        backwards_ctrls.append(ctrl)

        mt.match(root_grp, joint, r=True, t=True)

    cmds.parent(ik_roots[0], backwards_ctrls[-1])
    cmds.parent(ik_roots[-1], forward_ctrls[-1])


    #Fk Constraints IK in Mid
    #Constriants to mid iks
    reversed_backwards_ctrls = list(reversed(backwards_ctrls))
    ik_roots_no_last = ik_roots[1:-1]

    #find pairs
    constraints = []
    constraints_map = {}
    num = 0
    for f, b in zip(forward_ctrls, reversed_backwards_ctrls):
        print('#'*20)
        print('#'*20)
        try: #Will fail on last since no item in list
            pc=cmds.parentConstraint(f, reversed_backwards_ctrls[num+1], ik_roots_no_last[num], mo=True)[0]
            cmds.setAttr('{}.interpType'.format(pc), 2)
            constraints.append(pc)
            constraints_map[pc] = [f, reversed_backwards_ctrls[num+1], ik_roots_no_last[num]]
        except Exception as e:
            print(e)
            pass
        num = num+1

    #create shared locator with: forward strength, backward strength, show forward, show backwars ctrls, show ik ctrls,

    for ctrl in forward_ctrls + backwards_ctrls + ik_ctrls:
        cmds.select(ctrl)
        print(ctrl)
        if cmds.objectType(ctrl) == 'transform':
            share_loc = mt.shape_with_attr(input='', obj_name='{}_Switch'.format(name), attr_name='').split('.')[0]

    print(share_loc)
    mt.line_attr(input=share_loc, name='Visibility')
    show_main_iks_attr = mt.new_enum(input=share_loc, name='IkMain')
    show_mid_iks_attr = mt.new_enum(input=share_loc, name='IkMid')
    show_backwards_attr = mt.new_enum(input=share_loc, name='FkBackwards')
    show_fordward_attr = mt.new_enum(input=share_loc, name='FkForwards')

    cmds.setAttr(show_main_iks_attr, 1)
    cmds.setAttr(show_mid_iks_attr, 1)
    cmds.setAttr(show_backwards_attr, 1)
    cmds.setAttr(show_fordward_attr, 1)

    mt.line_attr(input=share_loc, name='Motion')
    forward_attr = mt.new_attr(input=share_loc, name='FkForward', min=0, max=2, default=1)
    backward_attr = mt.new_attr(input=share_loc, name='FkBackward', min=0, max=2, default=1)

    for ctrl in ik_ctrls[1:-1]:
        cmds.connectAttr(show_mid_iks_attr, '{}.v'.format(cmds.listRelatives(ctrl, s=True)[0]))

    for ctrl in [ik_ctrls[0], ik_ctrls[-1]]:
        cmds.connectAttr(show_main_iks_attr, '{}.v'.format(cmds.listRelatives(ctrl, s=True)[0]))

    for ctrl in forward_ctrls:
        cmds.connectAttr(show_fordward_attr, '{}.v'.format(cmds.listRelatives(ctrl, s=True)[0]))

    for ctrl in backwards_ctrls:
        cmds.connectAttr(show_backwards_attr, '{}.v'.format(cmds.listRelatives(ctrl, s=True)[0]))

    print(constraints)
    for num, pc in enumerate(constraints):
        map = constraints_map[pc]
        #constraints_map[pc] = [f, reversed_backwards_ctrls[num+1], ik_roots_no_last[num]]
        print(pc)
        cmds.connectAttr(forward_attr, '{}.{}W0'.format(pc, map[0]))
        cmds.connectAttr(backward_attr, '{}.{}W1'.format(pc, map[1]))

    #Twist
    #Create twist joints
    #Ik advance twist settings
    cmds.select(cl=True)
    twist_start_joint = cmds.joint(n=name+'_StartTwist'+nc['joint'])

    cmds.select(cl=True)
    twist_end_joint = cmds.joint(n=name+'_EndTwist'+nc['joint'])
    cmds.setAttr('{}.radius'.format(twist_end_joint), 1.2)
    cmds.setAttr('{}.radius'.format(twist_start_joint), 1.2)

    mt.match(this=twist_start_joint, that=spine_joints[0], r=True)
    mt.match(this=twist_end_joint, that=spine_joints[-1], r=True)
    twist_start_joint_root = mt.root_grp(input=twist_start_joint)[0]
    twist_end_joint_root = mt.root_grp(input=twist_end_joint)[0]

    cmds.rotate(0,0,0,twist_start_joint)
    cmds.rotate(0,0,0,twist_end_joint)

    cmds.parentConstraint(ik_ctrls[0], twist_start_joint, mo=True)
    cmds.parentConstraint(ik_ctrls[-1], twist_end_joint, mo=True)
    #cmds.parent(twist_start_joint_root, ik_ctrls[0])
    #cmds.parent(twist_end_joint_root, ik_ctrls[-1])

    cmds.setAttr("{}.dTwistControlEnable".format(ik_spline), 1)
    cmds.setAttr("{}.dWorldUpType".format(ik_spline), 4)

    cmds.connectAttr("{}.worldMatrix[0]".format(twist_start_joint), "{}.dWorldUpMatrix".format(ik_spline), f=True)
    cmds.connectAttr("{}.worldMatrix[0]".format(twist_end_joint), "{}.dWorldUpMatrixEnd".format(ik_spline), f=True)

    cmds.setAttr("{}.dForwardAxis".format(ik_spline), 0)
    cmds.setAttr("{}.dWorldUpAxis".format(ik_spline), 1)
    cmds.setAttr("{}.dWorldUpVectorX".format(ik_spline), 0)
    cmds.setAttr("{}.dWorldUpVectorY".format(ik_spline), -1)
    cmds.setAttr("{}.dWorldUpVectorZ".format(ik_spline), 0)
    cmds.setAttr("{}.dWorldUpVectorEndX".format(ik_spline), 0)
    cmds.setAttr("{}.dWorldUpVectorEndY".format(ik_spline), -1)
    cmds.setAttr("{}.dWorldUpVectorEndZ".format(ik_spline), 0)


    #Stretchy
    #Curve info
    Curveinfonode = cmds.shadingNode('curveInfo', asUtility=True, name=name+'_CurveInfoSpine')
    cmds.connectAttr('{}.worldSpace[0]'.format(spine_cv), str(Curveinfonode) + '.inputCurve', f=True)
    ArcLenght = cmds.arclen(spine_cv)

    #Normalize
    NormalizeDiv = MultiplyDiveNode(name+'NomralizeDivNode', 2)
    print(Curveinfonode, NormalizeDiv)
    cmds.connectAttr(Curveinfonode+'.arcLength', NormalizeDiv+'.input1X.', f=True)
    cmds.connectAttr('Global_Ctrl.scaleX', NormalizeDiv+'.input2X.', f=True)

    #StretchyDiv
    StretchyDiv = MultiplyDiveNode(name+'StretchyDivNode', 2)
    ArcLenghtNode=cmds.shadingNode('floatConstant', asUtility=True, name=name+'ArcLenghtNode')
    cmds.setAttr(ArcLenghtNode+'.inFloat', ArcLenght)
    cmds.connectAttr(NormalizeDiv+'.outputX', StretchyDiv+'.input1X.', f=True)
    cmds.connectAttr(ArcLenghtNode+'.outFloat', StretchyDiv+'.input2X.', f=True)

    #Squash Inv Power
    SquashInvPower = MultiplyDiveNode(name+'SquashInvPower', 3)
    cmds.connectAttr(StretchyDiv+'.outputX', SquashInvPower+'.input1X.', f=True)
    invPower=cmds.shadingNode('floatConstant', asUtility=True, name=name+'05invPower')
    cmds.setAttr(invPower+'.inFloat', 0.5)
    cmds.connectAttr(invPower+'.outFloat', SquashInvPower+'.input2X.', f=True)

    #Squash Div
    SquashDiv = MultiplyDiveNode(name+'SquashDiv', 2)
    cmds.connectAttr(SquashInvPower+'.outputX', SquashDiv+'.input2X.', f=True)
    SquashConstantDiv=cmds.shadingNode('floatConstant', asUtility=True, name=name+'SquashConstantDiv')
    cmds.setAttr(SquashConstantDiv+'.inFloat', 1)
    cmds.connectAttr(SquashConstantDiv+'.outFloat', SquashDiv+'.input1X', f=True)

    cmds.setAttr(StretchyDiv+'.operation', 2)

    #stretch squash attrs
    mt.line_attr(input=share_loc, name='SnS')

    stretch_attr =  mt.new_attr(input=share_loc, name='Stretch', min=0, max=1, default=1)
    squash_attr =  mt.new_attr(input=share_loc, name='Squash', min=0, max=1, default=1)


    #ConnectStretchy to Joints
    for jnt in spine_joints[1:-2]:
        blend_node = cmds.shadingNode('blendColors', asUtility=True, n='{}_Stretch'.format(name, nc['blend']))
        cmds.connectAttr(StretchyDiv+'.outputX', '{}.color1.color1R'.format(blend_node), f=1)
        cmds.setAttr('{}.color2.color2R'.format(blend_node), 1)
        cmds.connectAttr('{}'.format(stretch_attr), '{}.blender'.format(blend_node), f=1)
        cmds.connectAttr('{}.output.outputR'.format(blend_node), jnt+'.scaleX', f=1)

        blend_node = cmds.shadingNode('blendColors', asUtility=True, n='{}_Squash'.format(name, nc['blend']))
        cmds.connectAttr(SquashDiv+'.outputX', '{}.color1.color1R'.format(blend_node), f=1)
        cmds.setAttr('{}.color2.color2R'.format(blend_node), 1)
        cmds.connectAttr('{}'.format(squash_attr), '{}.blender'.format(blend_node), f=1)
        cmds.connectAttr('{}.output.outputR'.format(blend_node), jnt+'.scaleY', f=1)
        cmds.connectAttr('{}.output.outputR'.format(blend_node), jnt+'.scaleZ', f=1)


    #Bind Joints
    # create bind joints
    bind_jnt_grp = '{}{}'.format(setup['rig_groups']['bind_joints'], nc['group'])
    joints = []
    for jnt in spine_joints:
        cmds.select(cl=True)
        bind_joint = cmds.joint(n=jnt.replace(nc['joint'], nc['joint_bind']))
        if joints:
            cmds.parent(bind_joint, joints[-1])
        joints.append(bind_joint)
        cmds.parentConstraint(jnt, bind_joint)
        cmds.scaleConstraint(jnt, bind_joint)
        cmds.setAttr('{}.radius'.format(bind_joint), 1.5)
        cmds.parent(bind_joint, bind_jnt_grp)


    #clean a bit
    clean_ctrl_grp = cmds.group(em=True, name = name + nc['ctrl'] + nc['group'])
    clean_rig_grp = cmds.group(em=True, name = name + '_Rig' + nc['group'])

    cmds.parent(clean_rig_grp, '{}{}'.format(setup['rig_groups']['misc'], nc['group']))
    cmds.parent(clean_ctrl_grp, setup['base_groups']['control'] + nc['group'])

    spine_root_main_chain = mt.root_grp(input=spine_joints[0])[0]
    cmds.parent(spine_root_main_chain, twist_start_joint_root, twist_end_joint_root, ik_spline,spine_cv, ik_clusters,
                clean_rig_grp)
    cmds.parent(ik_roots[1], ik_roots[2], cmds.listRelatives(forward_ctrls[0], p=True)[0], cmds.listRelatives(backwards_ctrls[0], p=True)[0],
                clean_ctrl_grp)

    cmds.parentConstraint(block_parent, clean_ctrl_grp, mo=True)
    cmds.scaleConstraint(block_parent, clean_ctrl_grp, mo=True)
    cmds.parentConstraint(block_parent, spine_root_main_chain, mo=True)
    cmds.scaleConstraint(block_parent, spine_root_main_chain, mo=True)

    print ('Build {} Success'.format(block))



#build_quadspine_block()

def MultiplyDiveNode(Name, mode):
    print(Name, mode)
    node = cmds.shadingNode('multiplyDivide', asUtility=True, name=Name)
    cmds.setAttr(node + '.operation', mode)
    return node