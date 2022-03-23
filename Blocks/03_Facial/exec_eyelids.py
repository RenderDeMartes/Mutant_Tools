from maya import cmds, OpenMaya
import maya.mel as mel
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

TAB_FOLDER = '03_Facial'
PYBLOCK_NAME = 'exec_eyelids'

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

MODULE_FILE = os.path.join(os.path.dirname(__file__),'04_Eyelids.json')
with open(MODULE_FILE) as module_file:
    module = json.load(module_file)


# ---------------------------------------------

def create_eyelids_block(name='Nose'):
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

    to_build = [name]
    if mirror_attr == 'True':
        to_build = [name, name.replace(nc['left'], nc['right'])]

    for name in to_build:

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
            linear_curve = cmds.polyToCurve(form = 0,
                                            degree = 1,
                                            conformToSmoothMeshPreview = 1,
                                            n =name+'_Vtx'+nc['curve'],
                                            ch=False)[0]
            linear_curve_shape = cmds.listRelatives(linear_curve, s=True)[0]
            linear_curve_cvs = cmds.getAttr('{}.spans'.format(linear_curve_shape)) + 1

            #make sure curve is in correct orientation
            if check_curve:
                cmds.select('{}.cv[0]'.format(linear_curve))
                zero_cls = cmds.cluster()[1]
                cmds.select('{}.cv[1]'.format(linear_curve))
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
                cmds.connectAttr('{}.rotate'.format(origin_jnt), '{}.rotate'.format(pivot_grp))
                cmds.connectAttr('{}.translate'.format(origin_jnt), '{}.translate'.format(pivot_grp))


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
            #Mid ctrls moves with center and corne
            pc = cmds.parentConstraint(main_ctrls[0], main_ctrls[2], cmds.listRelatives(main_ctrls[1],p=True), mo=True)[0]
            cmds.setAttr('{}.interpType'.format(pc), 2)
            pc2 = cmds.parentConstraint(main_ctrls[4], main_ctrls[2], cmds.listRelatives(main_ctrls[3], p=True), mo=True)[0]
            cmds.setAttr('{}.interpType'.format(pc2), 2)

            pcj = cmds.parentConstraint(five_jnts[0], five_jnts[2], cmds.listRelatives(five_jnts[1], p=True), mo=True)[0]
            cmds.setAttr('{}.interpType'.format(pc), 2)
            pc2j = cmds.parentConstraint(five_jnts[4], five_jnts[2], cmds.listRelatives(five_jnts[3], p=True), mo=True)[0]
            cmds.setAttr('{}.interpType'.format(pc2), 2)

            return {'clean_rig': [vtx_joints_grp, aim_locators_grp, linear_curve, five_curve, main_joint_grp, wire_base],
                    'clean_ctrls': [main_ctrl_grp],
                    'linear_cv':linear_curve,
                    'tweeks': tweek_controllers,
                    'ctrls': main_ctrls,
                    'tweek_joints' : end_joints}

        upper_system = create_eye_system(name = name+'_Up',
                                          edge=upper_edge,
                                          center_pivot=eye_pivot)

        lower_system = create_eye_system(name = name+'_Dw',
                                          edge=lower_edge,
                                          center_pivot=eye_pivot)

        #Attrs location
        if name.startswith(nc['right']):
            attrs_position = attrs_position.replace(nc['left'], nc['right'])

        if attrs_position == 'new_locator':
            guide_attrs_position = cmds.spaceLocator(n=name+'_Attrs'+nc['locator'])[0]

        #hide ctrls
        mt.line_attr(input=guide_attrs_position, name='Eye_Vis')
        show_ctrl_attr = mt.new_enum(input=guide_attrs_position, name='eyeMidCtrls', enums='Hide:Show')
        show_tweeks_attr = mt.new_enum(input=guide_attrs_position, name='eyeTweekCtrls', enums='Hide:Show')

        for ctrl in upper_system['tweeks']+lower_system['tweeks']:
            shape = cmds.listRelatives(ctrl, s=True)[0]
            cmds.connectAttr(show_tweeks_attr, '{}.v'.format(shape))
        for ctrl in upper_system['ctrls']+lower_system['ctrls']:
            shape = cmds.listRelatives(ctrl, s=True)[0]
            cmds.connectAttr(show_ctrl_attr, '{}.v'.format(shape))

        cmds.setAttr(show_ctrl_attr, 0)
        cmds.setAttr(show_tweeks_attr, 0)

        #Smart Blink 0 min video 3
        upr_curve = upper_system['clean_rig'][3]
        lwr_curve = lower_system['clean_rig'][3]

        blink_cv = cmds.duplicate(upr_curve, n=upr_curve.replace('Up_WireDriver', 'Blink'))
        cmds.select(upr_curve, lwr_curve, blink_cv)
        bs = cmds.blendShape(n='{}_Blink{}'.format(name, '_BS'), w=[(0, 1), (1, 1)])[0]

        cmds.select(guide_attrs_position)
        mt.line_attr(input=guide_attrs_position, name='SmartBlink')
        blink_attr = mt.new_attr(input=guide_attrs_position, name='blink', min=0, max=1, default=0)


        smart_blink_heigth_attr = mt.new_attr(input=guide_attrs_position, name='blinkHeight', min=0, max=1, default=0.35)
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


        cmds.select(guide_attrs_position)
        upr_blink_mult_attr = mt.new_attr(input=guide_attrs_position, name='uprBlinkMult', min=1, max=1.5, default=1)
        lwr_blink_mult_attr = mt.new_attr(input=guide_attrs_position, name='lwrBlinkMult', min=1, max=1.5, default=1)


        mt.connect_md_node(in_x1=blink_attr,
                           in_x2=upr_blink_mult_attr,
                           out_x='{}.{}'.format(up_bs, upr_target_curve)
                           ,mode='mult', name='UprBlink', force=True)

        mt.connect_md_node(in_x1=blink_attr,
                           in_x2=lwr_blink_mult_attr,
                           out_x='{}.{}'.format(low_bs, lwr_target_curve)
                           ,mode='mult', name='LwrBlink', force=True)

        cmds.setAttr(smart_blink_heigth_attr, 0.35)

        #Clean a bit
        clean_ctrl_grp = cmds.group(em=True, name=name + nc['ctrl'] + nc['group'])
        clean_rig_grp = cmds.group(em=True, name=name + '_Rig' + nc['group'])

        cmds.parent(clean_rig_grp, '{}{}'.format(setup['rig_groups']['misc'], nc['group']))
        cmds.parent(clean_ctrl_grp, setup['base_groups']['control'] + nc['group'])

        cmds.parent(upper_system['clean_rig'],lower_system['clean_rig'],eye_pivot_locator,
                    eye_up_vector_locator,up_wire_base, dw_wire_base, upr_target_curve, lwr_target_curve,
                    blink_cv,
                    clean_rig_grp)
        cmds.parent(upper_system['clean_ctrls'],lower_system['clean_ctrls'] , clean_ctrl_grp)

        #Mirror
        if name.startswith(nc['right']):
            rig_mirror=mt.mirror_group(clean_rig_grp, world = True)
            ctrl_mirror=mt.mirror_group(clean_ctrl_grp, world = True)

            cmds.parent(rig_mirror, '{}{}'.format(setup['rig_groups']['misc'], nc['group']))
            cmds.parent(ctrl_mirror, setup['base_groups']['control'] + nc['group'])

        #create bind joints
        bind_jnt_grp = '{}{}'.format(setup['rig_groups']['bind_joints'], nc['group'])
        for jnt in upper_system['tweek_joints']+lower_system['tweek_joints']:
            cmds.select(cl=True)
            bind_joint = cmds.joint(n=jnt.replace(nc['joint'], nc['joint_bind']))
            cmds.parentConstraint(jnt, bind_joint)
            cmds.scaleConstraint(jnt, bind_joint)
            cmds.setAttr('{}.radius'.format(bind_joint), 1.5)
            cmds.parent(bind_joint, bind_jnt_grp)

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

#Created during video

















