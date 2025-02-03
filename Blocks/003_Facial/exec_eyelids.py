from __future__ import absolute_import, division
from maya import cmds, OpenMaya
import maya.mel as mel
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

from Mutant_Tools.UI.FaceInstall.faceinstall_utils import postbuilds_faceinstall
reload(postbuilds_faceinstall) 

#---------------------------------------------

TAB_FOLDER = '003_Facial'
PYBLOCK_NAME = 'exec_eyelids'

#Read name conventions as nc[''] and setup as seup['']
PATH = os.path.dirname(__file__)
PATH = Path(PATH)
PATH_PARTS = PATH.parts[:-2]
FOLDER=''
for f in PATH_PARTS:
    FOLDER = os.path.join(FOLDER, f)

# ---------------------------------------------

def create_eyelids_block(name='Eyelids'):

    # Read name conventions as nc[''] and setup as seup['']
    PATH = os.path.dirname(__file__)
    PATH = Path(PATH)
    PATH_PARTS = PATH.parts[:-2]
    FOLDER = ''
    for f in PATH_PARTS:
        FOLDER = os.path.join(FOLDER, f)

    MODULE_FILE = os.path.join(os.path.dirname(__file__), '004_Eyelids.json')
    with open(MODULE_FILE) as module_file:
        module = json.load(module_file)

    nc, curve_data, setup = mt.import_configs()

    # name checks and block creation
    name = mt.ask_name(text=module['Name'])
    if cmds.objExists('{}{}'.format(name, nc['module'])):
        cmds.warning('Name already exists.')
        return ''

    block = mt.create_block(name=name, icon='Eyes', attrs=module['attrs'], build_command=module['build_command'],
                            import_command=module['import'])
    config = block[1]
    block = block[0]

    cmds.select(block)

    print('{} Created Successfully'.format(name))


# create_nose_block()

# -------------------------

def build_eyelids_block():

    nc, curve_data, setup = mt.import_configs()

    mt.check_is_there_is_base()

    block = cmds.ls(sl=True)
    config = cmds.listConnections(block)[1]
    block = block[0]
    #guide = cmds.listRelatives(block, c=True)[0]
    name = block.replace(nc['module'], '')

    # use this locator in case parent is set to new locator
    if cmds.getAttr('{}.SetParent'.format(config)) == 'new_locator':
        block_parent = cmds.spaceLocator(n='{}'.format(str(block).replace(nc['module'], '_Parent' + nc['locator'])))
    else:
        block_parent = cmds.getAttr('{}.SetParent'.format(config))

    ctrl_size = cmds.getAttr('{}.CtrlSize'.format(config))/2

    upper_edge = cmds.getAttr('{}.SetUpperEdge'.format(config), asString=True).split(',')
    lower_edge = cmds.getAttr('{}.SetLowerEdge'.format(config), asString = True).split(',')
    eye_pivot = cmds.getAttr('{}.SetEyePivot'.format(config), asString = True)
    attrs_position = cmds.getAttr('{}.SetAttrsPosition'.format(config), asString = True)

    mirror_attr = cmds.getAttr('{}.Mirror'.format(config), asString=True)

    if cmds.attributeQuery('LimitCtrl', node=config, exists=True):
        limit_ctrls = cmds.getAttr('{}.LimitCtrl'.format(config), asString=True)
    else:
        limit_ctrls=True


    to_build = [name]
    if mirror_attr == 'True':
        to_build = [name, name.replace(nc['left'], nc['right'])]

    for name in to_build:

        #Vis
        to_main_vis = []
        to_tweeks_vis = []
        to_scale_vis = []

        # Connect vis
        if attrs_position == 'new_locator':
            guide_attrs_position = cmds.spaceLocator(n=name + '_Attrs' + nc['locator'])[0]
        else:
            guide_attrs_position = attrs_position

        if guide_attrs_position.startswith(nc['left']) and name.startswith(nc['right']):
            guide_attrs_position = guide_attrs_position.replace(nc['left'], nc['right'])

        # side settings
        if name.startswith(nc['right']):
            color = 'red'
        elif name.startswith(nc['left']):
            color = 'blue'
        else:
            color = 'yellow'

        #Create locator at center of eye with up vector
        eye_pivot_locator = cmds.spaceLocator(n=name+"_EyePivot"+nc['locator'])[0]
        cmds.delete(cmds.parentConstraint(eye_pivot, eye_pivot_locator))
        eye_up_vector_locator = cmds.spaceLocator(n=name+"_UpVector"+nc['locator'])[0]
        cmds.delete(cmds.parentConstraint(eye_pivot_locator, eye_up_vector_locator))
        cmds.move(0,3*ctrl_size,0, r=True)

        def create_eye_system(name, edge, center_pivot, check_curve =True):


            #
            cmds.select(edge)
            #mel.eval('performPolyToCurveSetup OptionBoxWindow|formLayout108|tabLayout5|formLayout110|polyToCurveOptionsFormLayout 1;')
            linear_curve = cmds.polyToCurve(form=0,
                                            degree=1,
                                            #conformToSmoothMeshPreview=1,
                                            n =name+'_Vtx'+nc['curve'],
                                            ch=False)

            linear_curve = linear_curve[0]
            linear_curve_shape = cmds.listRelatives(linear_curve, s=True)[0]
            linear_curve_cvs = cmds.getAttr('{}.spans'.format(linear_curve_shape)) + 1
            #make sure curve is in correct orientation
            if check_curve:
                cmds.select('{}.cv[0]'.format(linear_curve))
                zero_cls = cmds.cluster()[1]
                cmds.select('{}.cv[{}]'.format(linear_curve, linear_curve_cvs))
                one_cls = cmds.cluster()[1]
                if cmds.getAttr('{}.originX'.format(zero_cls)) > cmds.getAttr('{}.originX'.format(one_cls)):
                    cmds.reverseCurve(linear_curve, ch=False, replaceOriginal=True )
                cmds.delete(zero_cls, one_cls)

            cmds.delete(linear_curve, ch=True)

            center_joints = []
            end_joints = []
            end_locators = []
            points_on_curve_infos = []
            tweek_controllers = []
            vtx_joints_grp = cmds.group(em=True, n='{}_VtxJnts{}'.format(name, nc['group']))
            aim_locators_grp = cmds.group(em=True, n='{}_AimLocators{}'.format(name, nc['group']))
            tweek_ctrl_grp = cmds.group(em=True, n='{}_Tweeks{}{}'.format(name, nc['ctrl'], nc['group']))

            for num in range(linear_curve_cvs):
                #Place joint at pivot and on vertex
                cmds.select(cl=True)
                origin_jnt = cmds.joint(n='{}_Origin_{}{}'.format(name, num, nc['joint']))
                center_joints.append(origin_jnt)
                vtx_jnt = cmds.joint(n='{}_{}{}'.format(name, num, nc['joint']))
                end_joints.append(vtx_jnt)
                cmds.select('{}.cv[{}]'.format(linear_curve, num))
                temp_cls = cmds.cluster()
                cmds.delete(cmds.parentConstraint(eye_pivot, origin_jnt))
                cmds.delete(cmds.parentConstraint(temp_cls, vtx_jnt))
                cmds.select(origin_jnt)
                mel.eval('joint -e  -oj xyz -secondaryAxisOrient yup -ch -zso;')
                cmds.delete(temp_cls)
                cmds.parent(origin_jnt, vtx_joints_grp)
                origin_root=mt.root_grp(input=origin_jnt)
                #end locators to work as aim
                end_locator=cmds.spaceLocator(n='{}_{}{}'.format(name, num, nc['locator']))[0]
                end_locators.append(end_locator)
                cmds.delete(cmds.parentConstraint(vtx_jnt, end_locator))
                cmds.parent(end_locator, aim_locators_grp)

                cmds.aimConstraint(end_locator, origin_jnt,
                                   aimVector= (1, 0, 0), upVector =(0, 1, 0),
                                   worldUpType="object", worldUpObject=eye_up_vector_locator)
                cmds.delete(cmds.aimConstraint(end_locator, vtx_jnt,
                                   aimVector= (1, 0, 0), upVector =(0, 1, 0),
                                   worldUpType="object", worldUpObject=eye_up_vector_locator))

                #point on curve info per cv
                poci = cmds.createNode('pointOnCurveInfo', n='{}_{}_POCI'.format(name, num) )
                points_on_curve_infos.append(poci)
                cmds.connectAttr('{}.worldSpace[0]'.format(linear_curve_shape), '{}.inputCurve'.format(poci))
                cmds.connectAttr('{}.position'.format(poci), '{}.translate'.format(end_locator))
                cmds.setAttr('{}.parameter'.format(poci), num)

                # create controllers to control the curve
                ctrl = mt.curve(input=vtx_jnt,
                                type='circleX',
                                rename=True,
                                custom_name=True,
                                name=end_locator.replace(nc['locator'], nc['ctrl']),
                                size=ctrl_size/3)
                tweek_controllers.append(ctrl)
                mt.assign_color(color=color)
                ctrl_root = mt.root_grp()[0]
                mt.match(ctrl_root, vtx_jnt, r = True, t = True)
                #Group so the origin jnt controll te end position of ctrl too as local
                pivot_grp = cmds.group(em=True, n= ctrl_root.replace(nc['group'],'Pivot'+nc['group']))
                pivot_root = mt.root_grp()[0]
                mt.match(pivot_root, origin_jnt, r = True, t = True)
                cmds.parent(ctrl_root, pivot_grp)

                cmds.parent(pivot_root, tweek_ctrl_grp)

                end_root=mt.root_grp(input=vtx_jnt)

                #Connect directy to threat as local
                cmds.connectAttr('{}.rotate'.format(ctrl), '{}.rotate'.format(vtx_jnt))
                cmds.connectAttr('{}.translate'.format(ctrl), '{}.translate'.format(vtx_jnt))
                cmds.connectAttr('{}.scale'.format(ctrl), '{}.scale'.format(vtx_jnt))
                cmds.connectAttr('{}.rotate'.format(origin_jnt), '{}.rotate'.format(pivot_grp))
                cmds.connectAttr('{}.translate'.format(origin_jnt), '{}.translate'.format(pivot_grp))
                cmds.connectAttr('{}.scale'.format(origin_jnt), '{}.scale'.format(pivot_grp))


            main_ctrl_grp = cmds.group(em=True, n='{}{}{}'.format(name, nc['ctrl'], nc['group']))
            cmds.parent(tweek_ctrl_grp, main_ctrl_grp)

            #Create 5 points curve and wire it to the linear one
            five_curve = cmds.duplicate(linear_curve, n=name+'_WireDriver'+nc['curve'])[0]
            mel.eval('rebuildCurve -ch 1 -rpo 1 -rt 0 -end 1 -kr 0'
                     ''
                     ''
                     ' -kcp 0 -kep 1 -kt 0 -s 4 -d 3 -tol 0.01 "{}";'.format(five_curve))
            five_curve_shape = cmds.listRelatives(five_curve, s=True)[0]

            wire = mel.eval('wire -n "{}_Wire" -gw false -en 1.000000 -ce 0.000000 -li 0.000000 -w {} {};'.format(name, five_curve, linear_curve))
            cmds.setAttr('{}.dropoffDistance[0]'.format(wire[0]), 999)
            wire_base=wire[1]+'BaseWire'

            #Create 5 controllers to manipulate main curve
            cv_to_add_ctrl_to = ['{}.cv[0]'.format(five_curve),
                                     '{}.cv[2]'.format(five_curve),
                                     '{}.cv[3]'.format(five_curve),
                                     '{}.cv[4]'.format(five_curve),
                                     '{}.cv[6]'.format(five_curve),
                                     ]
            main_ctrl_names = ['Start',
                               'StartMid',
                               'Mid',
                               'EndMid',
                               'End'
                                ]
            main_ctrls=[]
            five_jnts = []
            main_joint_grp = cmds.group(em=True, n='{}{}{}'.format(name, nc['joint'], nc['group']))

            for num, cv in enumerate(cv_to_add_ctrl_to):
                cmds.select(cv)
                temp_cls = cmds.cluster()
                ctrl = mt.curve(input=temp_cls,
                                type='circleZ',
                                rename=True,
                                custom_name=True,
                                name=name+main_ctrl_names[num]+nc['ctrl'] ,
                                size=ctrl_size/2)
                main_ctrls.append(ctrl)
                mt.hide_attr(input=ctrl, t=False, r=True, s=True, v=False, rotate_order=True)
                mt.assign_color(color=color)
                ctrl_root = mt.root_grp()[0]
                cmds.parent(ctrl_root, main_ctrl_grp)
                mt.match(ctrl_root, temp_cls, r=True, t=True)
                # cmds.delete(cmds.aimConstraint(eye_pivot, ctrl_root,
                #                    aimVector= (0, 0, -1), upVector =(0, 1, 0),
                #                    worldUpType="object", worldUpObject=eye_up_vector_locator))
                cmds.delete(temp_cls)

                cmds.select(cl=True)
                jnt = cmds.joint(n=name+main_ctrl_names[num]+nc['joint'] )
                five_jnts.append(jnt)
                mt.match(jnt, ctrl, r=True, t=True)
                jnt_root = mt.root_grp()[0]
                cmds.parent(jnt_root, main_joint_grp)
                cmds.connectAttr('{}.rotate'.format(ctrl), '{}.rotate'.format(jnt))
                cmds.connectAttr('{}.translate'.format(ctrl), '{}.translate'.format(jnt))

            cmds.skinCluster(five_jnts, five_curve, sm=0, bm=1, tsb=True)
            #sm = 0 - classical linear skinning (default). 1 - dual quaternion (volume preserving), 2 - a weighted blend between the two
            #bm = 1 - Closest distance between a joint, considering the skeleton hierarchy, and a point of the geometry. 2 - Surface heat map diffusion. 3 - Geodesic voxel binding. geomBind

            #Mid ctrls moves with center and corne
            pc = cmds.parentConstraint(main_ctrls[0], main_ctrls[2], cmds.listRelatives(main_ctrls[1],p=True), mo=True)[0]
            cmds.setAttr('{}.interpType'.format(pc), 2)
            pc2 = cmds.parentConstraint(main_ctrls[4], main_ctrls[2], cmds.listRelatives(main_ctrls[3], p=True), mo=True)[0]
            cmds.setAttr('{}.interpType'.format(pc2), 2)

            pcj = cmds.parentConstraint(five_jnts[0], five_jnts[2], cmds.listRelatives(five_jnts[1], p=True), mo=True)[0]
            cmds.setAttr('{}.interpType'.format(pc), 2)
            pc2j = cmds.parentConstraint(five_jnts[4], five_jnts[2], cmds.listRelatives(five_jnts[3], p=True), mo=True)[0]
            cmds.setAttr('{}.interpType'.format(pc2), 2)

            #scale functionality
            scale_group = cmds.group(em=True, n = name+'_Scale'+nc['group'])
            cmds.delete(cmds.parentConstraint(main_ctrls[0], main_ctrls[-1], scale_group))
            cmds.delete(cmds.aimConstraint(main_ctrls[-1], scale_group, mo=False, worldUpType="object", worldUpObject=eye_up_vector_locator))
            cmds.parent(main_joint_grp, vtx_joints_grp, scale_group)

            scale_ctrl = mt.curve(input=scale_group,
                            type='sphere',
                            rename=True,
                            custom_name=True,
                            name=name + '_Scale' + nc['ctrl'],
                            size=ctrl_size / 2)
            mt.assign_color(color='purple')
            scale_root = mt.root_grp()[0]
            cmds.parent(scale_root, main_ctrl_grp)
            cmds.delete(cmds.pointConstraint(main_ctrls[2], scale_root))
            cmds.delete(cmds.orientConstraint(scale_group, scale_root))

            scale_group_root=mt.root_grp(input=scale_group)[0]

            cmds.connectAttr(scale_ctrl+'.scaleX', scale_group+'.scaleX')
            cmds.connectAttr(scale_ctrl+'.scaleY', scale_group+'.scaleY')
            cmds.connectAttr(scale_ctrl+'.scaleZ', scale_group+'.scaleZ')
            cmds.connectAttr(scale_ctrl+'.translateX', scale_group+'.translateX')
            cmds.connectAttr(scale_ctrl+'.translateY', scale_group+'.translateY')
            cmds.connectAttr(scale_ctrl+'.translateZ', scale_group+'.translateZ')
            cmds.connectAttr(scale_ctrl+'.rotateX', scale_group+'.rotateX')
            cmds.connectAttr(scale_ctrl+'.rotateY', scale_group+'.rotateY')
            cmds.connectAttr(scale_ctrl+'.rotateZ', scale_group+'.rotateZ')


            for ctrl in [scale_ctrl]:
                shape = cmds.listRelatives(ctrl, s=True)[0]
                to_scale_vis.append(shape)

            return {'clean_rig': [scale_group_root, aim_locators_grp, linear_curve, five_curve,wire_base],
                    'clean_ctrls': [main_ctrl_grp],
                    'linear_cv':linear_curve,
                    'tweeks': tweek_controllers,
                    'ctrls': main_ctrls,
                    'tweek_joints' : end_joints,
                    'scale_group' : scale_group_root,
                    'for_rotate' : [cmds.listRelatives(main_ctrls[2], p=True)[0], cmds.listRelatives(five_jnts[2], p=True)[0]],
                    'scale_ctrl' : scale_ctrl}

        upper_system = create_eye_system(name = name+'_Up',
                                          edge=upper_edge,
                                          center_pivot=eye_pivot)

        lower_system = create_eye_system(name = name+'_Dw',
                                          edge=lower_edge,
                                          center_pivot=eye_pivot)

        # Attrs location
        for ctrl in upper_system['tweeks']+lower_system['tweeks']:
            shape = cmds.listRelatives(ctrl, s=True)[0]
            to_tweeks_vis.append(shape)
        for ctrl in upper_system['ctrls']+lower_system['ctrls']:
            shape = cmds.listRelatives(ctrl, s=True)[0]
            to_main_vis.append(shape)


        #cmds.setAttr(show_ctrl_attr, 1)
        #cmds.setAttr(show_tweeks_attr, 1)
        #cmds.setAttr(scale_ctrl_attr, 1)

        #Rectangle Controllers for blink
        rectangle, upr_triangle, lwr_triangle = create_eye_blink_slider(name, color, ctrl_size, limit=limit_ctrls)
        rectangle_root = cmds.listRelatives(rectangle, p=True)[0]
        cmds.delete(cmds.pointConstraint(upper_system['tweeks'][-1], rectangle_root))
        cmds.move(ctrl_size*2,0,ctrl_size, rectangle_root, r=True)
        guide_blink_attrs_position = rectangle
        #Smart Blink 0 min video 3
        upr_curve = upper_system['clean_rig'][3]
        lwr_curve = lower_system['clean_rig'][3]

        blink_cv = cmds.duplicate(upr_curve, n=upr_curve.replace('Up_WireDriver', 'Blink'))
        cmds.select(upr_curve, lwr_curve, blink_cv)
        bs = cmds.blendShape(n='{}_Blink{}'.format(name, '_BS'), w=[(0, 1), (1, 1)])[0]

        cmds.select(guide_blink_attrs_position)
        mt.line_attr(input=guide_blink_attrs_position, name='SmartBlink')
        #blink_attr = mt.new_attr(input=guide_blink_attrs_position, name='blink', min=0, max=1, default=0)


        smart_blink_heigth_attr = mt.new_attr(input=guide_blink_attrs_position, name='blinkHeight', min=0, max=1, default=0.35)
        mt.line_attr(guide_blink_attrs_position, name='Mult')
        cmds.connectAttr(smart_blink_heigth_attr, '{}.{}'.format(bs, upr_curve))

        reverse_node = cmds.createNode('reverse', n =name+'_Blink_Reverse')
        cmds.connectAttr(smart_blink_heigth_attr, '{}.input.inputX'.format(reverse_node))
        cmds.connectAttr('{}.output.outputX'.format(reverse_node), '{}.{}'.format(bs, lwr_curve))

        #Target curves 5min video 3
        linear_upr_curve = upper_system['linear_cv']
        linear_lwr_curve = lower_system['linear_cv']
        upr_target_curve = cmds.duplicate(linear_upr_curve, n=upr_curve.replace('WireDriver', 'BlinkTarget'))[0]
        lwr_target_curve = cmds.duplicate(linear_lwr_curve, n=lwr_curve.replace('WireDriver', 'BlinkTarget'))[0]

        cmds.setAttr(smart_blink_heigth_attr, 1)
        up_wire = cmds.wire(upr_target_curve, n="{}_UpWire".format(name) , w=blink_cv)
        cmds.setAttr('{}.dropoffDistance[0]'.format(up_wire[0]), 999)
        cmds.setAttr('{}.scale[0]'.format(up_wire[0]), 0)
        up_wire_base = up_wire[1] + 'BaseWire'

        cmds.setAttr(smart_blink_heigth_attr, 0)
        dw_wire = cmds.wire(lwr_target_curve, n="{}_DwWire".format(name) , w=blink_cv)
        cmds.setAttr('{}.scale[0]'.format(dw_wire[0]), 0)
        cmds.setAttr('{}.dropoffDistance[0]'.format(dw_wire[0]), 999)
        dw_wire_base = dw_wire[1] + 'BaseWire1'

        cmds.select(upr_target_curve, linear_upr_curve)
        up_bs = cmds.blendShape(n='{}_UprBlink{}'.format(name, '_BS'), w=[(0, 1)])[0]

        cmds.select(lwr_target_curve, linear_lwr_curve)
        low_bs = cmds.blendShape(n='{}_LwrBlink{}'.format(name, '_BS'), w=[(0, 1)])[0]


        upr_blink_mult_attr = mt.new_attr(input=guide_blink_attrs_position, name='uprBlinkMult', min=1, max=1.5, default=1)
        lwr_blink_mult_attr = mt.new_attr(input=guide_blink_attrs_position, name='lwrBlinkMult', min=1, max=1.5, default=1)

        mt.line_attr(guide_blink_attrs_position, name='Mode')


        mt.connect_md_node(in_x1=upr_triangle+'.translateY',
                           in_x2=upr_blink_mult_attr,
                           out_x='{}.{}'.format(up_bs, upr_target_curve),
                           mode='mult', name='UprBlink', force=True)

        mt.connect_md_node(in_x1=lwr_triangle+'.translateY',
                           in_x2=lwr_blink_mult_attr,
                           out_x='{}.{}'.format(low_bs, lwr_target_curve),
                           mode='mult', name='LwrBlink', force=True)

        cmds.setAttr(smart_blink_heigth_attr, 0.35)

        #Rotate main Ctrl
        upr_rotate_md = mt.connect_md_node(in_x1=upr_triangle+'.translateX',
                           in_x2 = 100,
                           out_x=upper_system['for_rotate'][1]+'.rotateZ',
                           mode='mult', name='LwrBlink', force=True)
        cmds.connectAttr(upr_rotate_md+'.output.outputX', upper_system['for_rotate'][0]+'.rotateZ')

        lwr_rotate_md = mt.connect_md_node(in_x1=lwr_triangle+'.translateX',
                           in_x2 = 100,
                           out_x=lower_system['for_rotate'][1]+'.rotateZ',
                           mode='mult', name='LwrBlink', force=True)
        cmds.connectAttr(lwr_rotate_md+'.output.outputX', lower_system['for_rotate'][0]+'.rotateZ')

        #Scale Main Box
        scale_ctrl = mt.curve(input=eye_pivot,
                              type='circlePointOut',
                              rename=True,
                              custom_name=True,
                              name=name + '_Scale' + nc['ctrl'],
                              size=ctrl_size * 2)
        mt.assign_color(color='purple')
        mt.match(scale_ctrl, eye_pivot, r=False, t=True)
        scale_ctrl_root = mt.root_grp()[0]
        cmds.parent(upper_system['clean_ctrls'],lower_system['clean_ctrls'], scale_ctrl)
        if guide_attrs_position != scale_ctrl:
            to_scale_vis.append(cmds.listRelatives(scale_ctrl, s=True)[0])

        cmds.delete(cmds.parentConstraint(upper_system['scale_ctrl'], eye_up_vector_locator))
        cmds.move(0, 10, 0, eye_up_vector_locator, r=True)

        scale_group =cmds.group(em=True, name=name + '_Scale' + nc['group'])
        cmds.delete(cmds.pointConstraint(scale_ctrl, scale_group))
        scale_group_root = mt.root_grp()[0]

        cmds.connectAttr(scale_ctrl+'.translate', scale_group+'.translate')
        cmds.connectAttr(scale_ctrl+'.rotate', scale_group+'.rotate')
        cmds.connectAttr(scale_ctrl+'.scale', scale_group+'.scale')

        cmds.select(cl=True)
        scale_jnt = cmds.joint(n=name + '_Scale' + nc['joint'])
        cmds.delete(cmds.pointConstraint(scale_ctrl, scale_jnt))
        scale_jnt_root = mt.root_grp()[0]
        cmds.connectAttr(scale_ctrl + '.scale', scale_jnt + '.scale')
        cmds.connectAttr(scale_ctrl + '.rotate', scale_jnt + '.rotate')
        cmds.connectAttr(scale_ctrl + '.translate', scale_jnt + '.translate')

        #Create Secundary mode:
        #get geo attr,
         #if no geo attr dont create wire
        #duplicate curve
        #create wire if geo face
        #md in between the main system joints
        #clusters on new curve
        # md for move those clsuters
        #create switch attr
        #Connnect an inverse to one md for it to work inverted as the other
        #conncet attrs to both md to have a swtich


        #Clean a bit
        clean_ctrl_grp = cmds.group(em=True, name=name + nc['ctrl'] + nc['group'])
        clean_rig_grp = cmds.group(em=True, name=name + '_Rig' + nc['group'])

        cmds.parent(clean_rig_grp, '{}{}'.format(setup['rig_groups']['misc'], nc['group']))
        cmds.parent(clean_ctrl_grp, setup['base_groups']['control'] + nc['group'])

        cmds.parent(upper_system['clean_rig'],lower_system['clean_rig'],eye_pivot_locator,
                    up_wire_base, dw_wire_base, upr_target_curve, lwr_target_curve,
                    blink_cv, scale_group_root, scale_jnt_root,
                    clean_rig_grp)
        cmds.parent(eye_up_vector_locator, scale_group)
        cmds.parent(scale_ctrl_root, rectangle_root, clean_ctrl_grp)
        cmds.parent(upper_system['scale_group'],lower_system['scale_group'], scale_group)

        #Mirror
        if name.startswith(nc['right']) and mirror_attr == 'True':
            rig_mirror=mt.mirror_group(clean_rig_grp, world = True)
            ctrl_mirror=mt.mirror_group(clean_ctrl_grp, world = True)

            cmds.parent(rig_mirror, '{}{}'.format(setup['rig_groups']['misc'], nc['group']))
            cmds.parent(ctrl_mirror, setup['base_groups']['control'] + nc['group'])


        #create bind joints
        bind_jnt_grp = '{}{}'.format(setup['rig_groups']['bind_joints'], nc['group'])
        for jnt in upper_system['tweek_joints']+lower_system['tweek_joints']+[scale_jnt]:
            cmds.select(cl=True)
            bind_joint = cmds.joint(n=jnt.replace(nc['joint'], nc['joint_bind']))
            cmds.parentConstraint(jnt, bind_joint)
            cmds.scaleConstraint(jnt, bind_joint)
            cmds.setAttr('{}.radius'.format(bind_joint), 1.5)
            cmds.parent(bind_joint, bind_jnt_grp)

        #parent to block_parent
        cmds.parentConstraint(block_parent, clean_ctrl_grp, mo=True)

        # hide ctrls
        if not cmds.attributeQuery('eyeMidCtrls', node=guide_attrs_position, exists=True):
            mt.line_attr(input=guide_attrs_position, name='Eye_Vis')
            show_ctrl_attr = mt.new_enum(input=guide_attrs_position, name='eyeMidCtrls', enums='Hide:Show',
                                         keyable=False)
            show_tweeks_attr = mt.new_enum(input=guide_attrs_position, name='eyeTweekCtrls', enums='Hide:Show',
                                           keyable=False)
            scale_ctrl_attr = mt.new_enum(input=guide_attrs_position, name='eyeScaleCtrls', enums='Hide:Show',
                                          keyable=False)
        else:
            show_ctrl_attr = guide_attrs_position + '.eyeMidCtrls'
            show_tweeks_attr = guide_attrs_position + '.eyeTweekCtrls'
            scale_ctrl_attr = guide_attrs_position + '.eyeScaleCtrls'

        """
        to_main_vis = []
        to_tweeks_vis = []
        to_scale_vis = []
       
        """
        for ctrl in to_main_vis:
            cmds.connectAttr(show_ctrl_attr, '{}.v'.format(ctrl))

        for ctrl in to_tweeks_vis:
            cmds.connectAttr(show_tweeks_attr, '{}.v'.format(ctrl))

        for ctrl in to_scale_vis:
            cmds.connectAttr(scale_ctrl_attr, '{}.v'.format(ctrl))


    if cmds.objExists('BodyEyes'):
        postbuilds_faceinstall.update_eyes(mirror=mirror_attr)


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

    cmds.parent(lwr_blink_triangle_root, upr_blink_triangle_root, blink_rectangle)

    cmds.scale(1,1,1, blink_rectangle_root)

    return [blink_rectangle, upr_blink_triangle, lwr_blink_triangle]

#Video TutorialScripts
#Tutorial: https://vimeo.com/66583205
def getUParam(pnt=[], crv=None):
    point = OpenMaya.MPoint(pnt[0], pnt[1], pnt[2])
    curveFn = OpenMaya.MFnNurbsCurve(getDagPath(crv))
    paramUtill = OpenMaya.MScriptUtil()
    paramPtr = paramUtill.asDoublePtr()
    isOnCurve = curveFn.isPointOnCurve(point)
    if isOnCurve == True:

        curveFn.getParamAtPoint(point, paramPtr, 0.001, OpenMaya.MSpace.kObject)
    else:
        point = curveFn.closestPoint(point, paramPtr, 0.001, OpenMaya.MSpace.kObject)
        curveFn.getParamAtPoint(point, paramPtr, 0.001, OpenMaya.MSpace.kObject)

    param = paramUtill.getDouble(paramPtr)
    return param


def getDagPath(objectName):
    if isinstance(objectName, list) == True:
        oNodeList = []
        for o in objectName:
            selectionList = OpenMaya.MSelectionList()
            selectionList.add(o)
            oNode = OpenMaya.MDagPath()
            selectionList.getDagPath(0, oNode)
            oNodeList.append(oNode)
        return oNodeList
    else:
        selectionList = OpenMaya.MSelectionList()
        selectionList.add(objectName)
        oNode = OpenMaya.MDagPath()
        selectionList.getDagPath(0, oNode)
        return oNode

