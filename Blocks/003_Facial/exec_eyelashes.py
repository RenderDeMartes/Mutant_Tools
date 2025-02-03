from __future__ import absolute_import, division
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

#---------------------------------------------

TAB_FOLDER = '003_Facial'
PYBLOCK_NAME = 'exec_eyelashes'

#---------------------------------------------

def create_eyelashes_block(name = 'Eyelashes'):

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

    MODULE_FILE = os.path.join(os.path.dirname(__file__), '018_Eyelashes.json')
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

    block = mt.create_block(name = name, icon = 'Eyelashes',  attrs = module['attrs'], build_command = module['build_command'], import_command = module['import'])
    config = block[1]
    block = block[0]
      
    #cmds.getAttr('{}.AttrName'.format(config)) #get attrs from config
    #cmds.getAttr('{}.AttrName'.format(config), asString = True) #for enums
    #joint_one = mt.create_joint_guide(name = name) #guide base with shapes

    cmds.select(block)

    print('{} Created Successfully'.format(name))

#create_eyelashes_block()

#-------------------------

def build_eyelashes_block():

    nc, curve_data, setup = mt.import_configs()

    mt.check_is_there_is_base()

    block = cmds.ls(sl=True)
    config = cmds.listConnections(block)[1]
    block = block[0]
    name = block.replace(nc['module'],'')

    eyes_name = cmds.getAttr('{}.EyeName'.format(config))

    up_vrt_linear_cv = eyes_name + '_Up_Vtx_Crv'
    to_build_up = [up_vrt_linear_cv]
    dw_vrt_linear_cv = eyes_name + '_Dw_Vtx_Crv'
    to_build_dw = [dw_vrt_linear_cv]
    if cmds.objExists(up_vrt_linear_cv.replace(nc['left'], nc['right'])):
        to_build_up.append(up_vrt_linear_cv.replace(nc['left'], nc['right']))

    # Vis Attrs
    attrs_position = cmds.getAttr('{}.SetAttrsPosition'.format(config), asString=True)

    if attrs_position == 'new_locator':
        guide_attrs_position = cmds.spaceLocator(n=name + '_Attrs' + nc['locator'])[0]
    else:
        guide_attrs_position = attrs_position

    if not cmds.attributeQuery('eyelashCtrls', node=guide_attrs_position, exists=True):
        mt.line_attr(input=guide_attrs_position, name='Eyelash_Vis')
        show_ctrl_attr = mt.new_enum(input=guide_attrs_position, name='eyelashCtrls', enums='Hide:Show', keyable=False)
    else:
        show_ctrl_attr = guide_attrs_position+'.eyelashCtrls'

    block_parent = cmds.listConnections('{}_Ctrl_Grp'.format(eyes_name))[0]

    #Build
    for curve in to_build_up:

        # side settings
        if curve.startswith(nc['right']):
            color = 'pink'
        elif curve.startswith(nc['left']):
            color = 'lightBlue'
        else:
            color = 'green'


        if curve.startswith(nc['left']):
            build_name = eyes_name
            block_parent = block_parent

        else:
            build_name=eyes_name.replace(nc['left'], nc['right'])
            block_parent = block_parent.replace(nc['left'], nc['right'])

        dw_curve = curve.replace('_Up_', '_Dw_')
        print(curve, dw_curve)

        new_curve_start_up = cmds.duplicate(curve, n=curve.replace('_Vtx_', '_EyeBrowsStart_'))[0]
        new_curve_end_up = cmds.duplicate(curve, n=curve.replace('_Vtx_', '_EyeBrowsEnd_'))[0]

        new_curve_start_dw = cmds.duplicate(dw_curve, n=dw_curve.replace('_Vtx_', '_EyeBrowsStart_'))[0]
        new_curve_end_dw = cmds.duplicate(dw_curve, n=dw_curve.replace('_Vtx_', '_EyeBrowsEnd_'))[0]

        distance = cmds.arclen(new_curve_start_dw)/2.5
        up_divisions = cmds.getAttr('{}.spans'.format(new_curve_start_up)) + 1
        dw_divisions = cmds.getAttr('{}.spans'.format(new_curve_start_dw)) + 1


        #Mirror if rigth
        if curve.startswith(nc['right']):
            cmds.setAttr('{}.scaleX'.format(new_curve_start_up), -1)
            cmds.setAttr('{}.scaleX'.format(new_curve_end_up), -1)
            cmds.setAttr('{}.scaleX'.format(new_curve_start_dw), -1)
            cmds.setAttr('{}.scaleX'.format(new_curve_end_dw), -1)

        #Create nurb
        pivot = cmds.xform(build_name+'_EyePivot_Loc', rp=True, q=True, ws=True)
        cmds.move(pivot[0], pivot[1], pivot[2], "{}.scalePivot".format(new_curve_end_up), "{}.rotatePivot".format(new_curve_end_up),
                  absolute=True)
        cmds.scale(distance, distance, distance, new_curve_end_up, r=True)

        cmds.move(pivot[0], pivot[1], pivot[2], "{}.scalePivot".format(new_curve_end_dw), "{}.rotatePivot".format(new_curve_end_dw),
                  absolute=True)
        cmds.scale(distance, distance, distance, new_curve_end_dw, r=True)

        nurbs_up = cmds.loft(new_curve_start_up, new_curve_end_up, ch=False, n=build_name+ '_LashUpSurface'+nc['nurb'])[0]
        nurbs_up = cmds.rebuildSurface(nurbs_up, ch=0,rpo=1, rt=0, end=1,kr=0, kcp=0, kc=0, su=0,du=3,sv=up_divisions, dv=3, tol=0.01, fr=0,dir=2)[0]

        nurbs_dw = cmds.loft(new_curve_start_dw, new_curve_end_dw, ch=False, n=build_name+ '_LashDwSurface'+nc['nurb'])[0]
        nurbs_dw = cmds.rebuildSurface(nurbs_dw, ch=0,rpo=1, rt=0, end=1,kr=0, kcp=0, kc=0, su=0,du=3,sv=dw_divisions, dv=3, tol=0.01, fr=0,dir=2)[0]

        #Skin bind joints to nurbs
        bind_joints_up = cmds.ls(build_name+'_Up_*'+nc['joint_bind'])
        bind_joints_dw = cmds.ls(build_name + '_Dw_*' + nc['joint_bind'])

        cmds.skinCluster(nurbs_up, bind_joints_up, tsb=True)
        cmds.skinCluster(nurbs_dw, bind_joints_dw, tsb=True)

        #Wire deformer
        up_wire = build_name+'_Up_ClusterWire'
        dw_wire = build_name + '_Up_ClusterWire'
        mel.eval('deformer -e -g {} {};'.format(nurbs_up, up_wire))
        mel.eval('deformer -e -g {} {};'.format(nurbs_dw, dw_wire))

        #Folicles in surface to skin in case dont want to wrap
        cmds.select(nurbs_up)
        mel.eval("createHair 1 {} 10 0 0 0 0 5 0 1 2 1".format(up_divisions))
        cmds.delete('hairSystem1', 'pfxHair1', 'nucleus1')
        cmds.setAttr(nurbs_up + '.inheritsTransform', 0)

        fol_grp_up = cmds.rename('hairSystem1Follicles', build_name+'EyeLashUp' + nc['follicle'] + nc['group'])
        follicles = []
        for num, fol in enumerate(cmds.listRelatives(fol_grp_up, c=True)):
            gc = cmds.listRelatives(fol, c=True)
            cmds.delete(gc[-1])
            fol = cmds.rename(fol, 'EyeLashUp' + nc['follicle'] + '_' + str(num))
            follicles.append(fol)
            cmds.setAttr(fol + '.parameterV', float(num) / (len(cmds.listRelatives(fol_grp_up, c=True)) - 1))
            cmds.setAttr('{}.parameterU'.format(fol), 0)

        cmds.select(nurbs_dw)
        mel.eval("createHair 1 {} 10 0 0 0 0 5 0 1 2 1".format(dw_divisions))
        cmds.delete('hairSystem1', 'pfxHair1', 'nucleus1')
        cmds.setAttr(nurbs_dw + '.inheritsTransform', 0)

        fol_grp_dw = cmds.rename('hairSystem1Follicles', build_name+'EyeLashDw' + nc['follicle'] + nc['group'])
        for num, fol in enumerate(cmds.listRelatives(fol_grp_dw, c=True)):
            gc = cmds.listRelatives(fol, c=True)
            cmds.delete(gc[-1])
            fol = cmds.rename(fol, 'EyeLashDw' + nc['follicle'] + '_' + str(num))
            follicles.append(fol)
            cmds.setAttr(fol + '.parameterV', float(num) / (len(cmds.listRelatives(fol_grp_dw, c=True)) - 1))
            cmds.setAttr('{}.parameterU'.format(fol), 0)


        fol_joints=[]
        end_joints=[]
        for num, fol in enumerate(follicles):
            cmds.select(cl=True)
            fol_joint = cmds.joint(n='{}{}{}'.format(build_name+'Eyelash', num, nc['joint']))
            fol_joints.append(fol_joint)
            cmds.delete(cmds.parentConstraint(fol, fol_joint))
            cmds.parent(fol_joint, fol)
            cmds.setAttr('{}.radius'.format(fol_joint), 0.25)

        #clean a bit
        clean_ctrl_grp = cmds.group(em=True, name=build_name+'EyeLash'+nc['ctrl']+nc['group'])
        clean_rig_grp = cmds.group(em=True, name=build_name+'EyeLash'+'_Rig'+nc['group'])

        cmds.parent(clean_rig_grp, '{}{}'.format(setup['rig_groups']['misc'], nc['group']))
        cmds.parent(clean_ctrl_grp, setup['base_groups']['control'] + nc['group'])

        #Locals extra systems
        local_geo_up = cmds.duplicate(nurbs_up, n=nurbs_up.replace('_LashUpSurface', '_LashUpLocal'))
        local_geo_dw = cmds.duplicate(nurbs_dw, n=nurbs_dw.replace('_LashDwSurface', '_LashDwLocal'))

        cmds.parent(local_geo_up, local_geo_dw, clean_rig_grp)

        #Create mid ctrls
        #dup curves and convert to 5
        curves = [new_curve_start_up, new_curve_end_up, new_curve_start_dw, new_curve_end_dw]
        five_curves = []
        for curve in curves:
            five_curve = cmds.duplicate(curve, n=curve + '_LocalFive' + nc['curve'])[0]
            cmds.parent(five_curve, w=True)
            mel.eval('rebuildCurve -ch 1 -rpo 1 -rt 0 -end 1 -kr 0'
                     ''
                     ''
                     ' -kcp 0 -kep 1 -kt 0 -s 4 -d 3 -tol 0.01 "{}";'.format(five_curve))
            five_curves.append(five_curve)

        print('5 Curves:', five_curves)
        nurbs_joints = []
        for start, end in zip([five_curves[0], five_curves[2]],[five_curves[1], five_curves[3]]):
            grp = cmds.group(n=start+nc['joint']+nc['group'], em=True)
            ctrl_grp = cmds.group(n=start + nc['ctrl'] + nc['group'], em=True)
            cmds.parent(grp, clean_rig_grp)
            cmds.parent(ctrl_grp, clean_ctrl_grp)
            joints = []
            for cv in [0,2,3,4,6]:
                #create joints in start
                start_pos = cmds.pointPosition('{}.cv[{}]'.format(start, cv))
                end_pos = cmds.pointPosition('{}.cv[{}]'.format(end, cv))
                print(start_pos ,end_pos)

                cmds.select(cl=True)
                jnt = cmds.joint(n=start.replace('_EyeBrowsStart_Crv_LocalFive_Crv', '')+str(cv)+nc['joint'], p=[start_pos[0], start_pos[1], start_pos[2]])
                cmds.setAttr(jnt + '.radius', 0.5)
                root, auto = mt.root_grp(input=jnt, autoRoot=True)
                joints.append(jnt)
                cmds.parent(root, grp)

                #create ctrls in end
                ctrl = mt.curve(input=jnt,
                                type='triangle',
                                rename=True,
                                custom_name=True,
                                name=jnt.replace(nc['joint'], nc['ctrl']),
                                size=distance/3)

                mt.assign_color(color=color)
                root_grp = mt.root_grp()[0]
                mt.match(root_grp, jnt, r=True, t=True)
                cmds.parent(root_grp, ctrl_grp)

                # connect ctrls
                cmds.connectAttr('{}.translate'.format(ctrl), '{}.translate'.format(auto))
                cmds.connectAttr('{}.rotate'.format(ctrl), '{}.rotate'.format(auto))
                cmds.connectAttr('{}.scale'.format(ctrl), '{}.scale'.format(auto))

                #reshape
                cmds.select('{}.cv[*]'.format(ctrl))
                cmds.rotate(90,0,0, r=True)
                if 'Up' in ctrl:
                    cmds.move(0, distance/4, distance/4, r=True)
                else:
                    cmds.move(0, -distance/4, distance/4, r=True)

                #connect attrs
                shapes = cmds.listRelatives(ctrl, s=True)
                for s in shapes:
                    cmds.connectAttr(show_ctrl_attr, s+'.v', f=True)

            nurbs_joints.append(joints)
            cmds.parentConstraint(block_parent, ctrl_grp, mo=True)
            cmds.scaleConstraint(block_parent, ctrl_grp, mo=True)

        cmds.skinCluster(local_geo_up, nurbs_joints[0], tsb=True)
        cmds.skinCluster(local_geo_dw, nurbs_joints[1], tsb=True)

        cmds.delete(five_curves)

        # create bind joints
        bind_jnt_grp = '{}{}'.format(setup['rig_groups']['bind_joints'], nc['group'])
        for jnt in fol_joints:
            cmds.select(cl=True)
            bind_joint = cmds.joint(n=jnt.replace(nc['joint'], nc['joint_bind']))
            cmds.parentConstraint(jnt, bind_joint)
            cmds.scaleConstraint(jnt, bind_joint)
            cmds.setAttr('{}.radius'.format(bind_joint), 0.5)
            cmds.parent(bind_joint, bind_jnt_grp)


        #Finish Clean

        cmds.delete(new_curve_start_dw, new_curve_end_dw)
        cmds.delete(new_curve_start_up, new_curve_end_up)

        cmds.parent(nurbs_up, nurbs_dw, fol_grp_dw, fol_grp_up, clean_rig_grp)




        print ('Build {} Success'.format(block))



#build_eyelashes_block()
