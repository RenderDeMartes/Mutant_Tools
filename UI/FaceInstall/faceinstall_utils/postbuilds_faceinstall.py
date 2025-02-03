from __future__ import absolute_import, division
from maya import cmds
import maya.mel as mel
import re
try:
    import importlib;from importlib import reload
except:
    import imp;from imp import reload
import Mutant_Tools
import Mutant_Tools.Utils.Rigging
from Mutant_Tools.Utils.Rigging import main_mutant
reload(Mutant_Tools.Utils.Rigging.main_mutant)

mt = main_mutant.Mutant()
nc = mt.import_configs()

lips_name = 'Lips'

#Eye update fix (modified translate with toggle)
# -------------------------

def update_eyes(face_geos=[], mirror='True'):
    '''
    Postbuild that solves Upper, Lower, Left and Right eye setups
    Args:
        face_geos(str list): Extra Facial geo like eyelashes, eyebrows that need the deformer
    '''
    if len(face_geos) == 0: 
        face_geos = cmds.ls(sl=True)
    else:
        face_geos = []

    mt.line_attr(input = 'L_Eyelids_BlinkAttrs_Ctrl', name='Eyelid Sliders')
    if mirror == 'True':
        mt.line_attr(input = 'L_Eyelids_BlinkAttrs_Ctrl', name='Eyelid Sliders')
        mt.line_attr(input = 'R_Eyelids_BlinkAttrs_Ctrl', name='Eyelid Sliders')
    if mirror == 'Right_Only':
        mt.line_attr(input = 'R_Eyelids_BlinkAttrs_Ctrl', name='Eyelid Sliders')
    if mirror == 'False':
        mt.line_attr(input = 'L_Eyelids_BlinkAttrs_Ctrl', name='Eyelid Sliders')

    cmds.select(clear=-True)

    eye_translate_postbuild(section='L_Eyelids_Up',
                            geo='BodyEyes',
                            face_geos=face_geos,
                            attr_control='L_Eyelids_BlinkAttrs_Ctrl', 
                            mirror=mirror)
    eye_translate_postbuild(section='L_Eyelids_Dw',
                            geo='BodyEyes',
                            face_geos=face_geos,
                            attr_control='L_Eyelids_BlinkAttrs_Ctrl', 
                            mirror=mirror)

    organize_inputs(['BodyEyes'])
    organize_inputs(face_geos)
    
    print('Updates to all face curves completed.')

def organize_inputs(geos):
    for modified_geo in geos:
        shape = cmds.listRelatives(cmds.ls(modified_geo)[0], f=True)
        geo_history = cmds.listHistory(modified_geo, ha=True, f=False, il=1)
        geo_connections = cmds.listConnections(shape, type='skinCluster')
        relevant_history = []
        skin_node = None

        for history in geo_history:
            if cmds.nodeType(history) == "skinCluster" or cmds.nodeType(history) == "wire":
                relevant_history.append(history)
                if cmds.nodeType(history) == "skinCluster":
                    skin_node = history
                    try:
                        cmds.reorderDeformers(relevant_history[0], history, modified_geo)
                    except Exception as e:
                        print(e)
        
        try:
            cmds.reorderDeformers(skin_node, relevant_history[0], modified_geo)
            print('Organized inputs for {}.'.format(modified_geo))
        except Exception as e:
            print(e)

    #force last fix on BodyEyes :( )
        if modified_geo == 'BodyEyes':
            print('Hard code fix for last reorder.')
            if geo_connections:
                for skin in geo_connections:
                    try:
                        cmds.reorderDeformers(skin, 'R_Eyelids_Dw_ClusterWire', 'BodyEyes')
                        print('Organized inputs for {}.'.format(modified_geo))
                    except Exception as e:
                        print(e)

def eye_translate_postbuild(section='L_Eyelids_Up', geo='BodyEyes', face_geos=[], attr_control='', mirror='True'):
    '''
    Updated eye system with a toggle to switch between sliding joints and clusters
    Args:
        section(str): Convention for rigging section
        geo(str): Name of face geo
        face_geos(str list): Extra Facial geo like eyelashes, eyebrows
        attr_controls(str): Control to host attr name
        mirror(string): True, False or RIght_Only
    '''
    control_cluster_dict ={'0':'Start_Ctrl',
                            '1':'Start_Ctrl',
                            '2':'StartMid_Ctrl',
                            '3':'Mid_Ctrl',
                            '4':'EndMid_Ctrl',
                            '5':'End_Ctrl',
                            '6':'End_Ctrl'}


    sides = []
    if mirror == 'True':
        sides = ['L_', 'R_']
    if mirror == 'Right_Only':
        sides = ['R_']
    if mirror == 'False':
        sides = ['L_']

    for side in sides:
        #mirror the names
        dup_curve = None
        section_side = section.replace('L_', side) 
        attr_control = attr_control.replace('L_', side) 

        #curve business
        cmds.addAttr(attr_control, sn='{}Slide'.format(section_side.replace(side, '')), dv=True, at='bool', h=False, k=True)
        cmds.setAttr('{ctrl}.{sec}Slide'.format(ctrl=attr_control, sec=section_side.replace(side, '')), False)
        curve = '{}_WireDriver_CrvBaseWire'.format(section_side)

        grp_split = section_side.split('_')
        grp_name = '{}_{}_Rig_Grp'.format(grp_split[0], grp_split[1])
        dup_curve = cmds.duplicate(curve, n = curve.replace('Crv', 'ClusterCrv'))
        cmds.delete(dup_curve[0], ch=True)

        #Get curve CV
        curveCVs = cmds.ls('{0}.cv[:]'.format(dup_curve[0]), fl = True)
        len_curveCVs = len(curveCVs)
        counter = 0
        if curveCVs: 
            while counter<len_curveCVs:
                cv=curveCVs[counter]
                new_name = '{sec}{key}'.format(sec=section_side, key=control_cluster_dict[str(counter)])
                cv_cluster = cmds.cluster(cv, n=new_name.replace('Ctrl', 'cluster'))

                #create nodes
                translate_md = cmds.createNode('multiplyDivide', n='{cv}_md'.format(cv=cv))
                translate_jnt_bc = cmds.createNode('blendColors', n='{cv}_jnt_bc'.format(cv=cv))

                translate_clst_bc = cmds.createNode('blendColors', n='{cv}_clst_bc'.format(cv=cv))
                translate_clst_rev = cmds.createNode('reverse', n='{cv}_clst_rev'.format(cv=cv))

                #connect nodes
                #jnt
                cmds.connectAttr('{at}.{sec}Slide'.format(at=attr_control, sec=section_side.replace(side, '')), '{}.blender'.format(translate_jnt_bc))
                cmds.connectAttr('{name}.translate'.format(name=new_name), '{}.color1'.format(translate_jnt_bc))
                cmds.setAttr('{}.color2R'.format(translate_jnt_bc), 0)
                cmds.setAttr('{}.color2G'.format(translate_jnt_bc), 0)
                cmds.setAttr('{}.color2B'.format(translate_jnt_bc), 0)
                cmds.connectAttr('{}.output'.format(translate_jnt_bc), '{}.translate'.format(new_name.replace('Ctrl','Jnt')), f=True)
                #clstif cmds.nodeType(node) == "skinCluster":
                cmds.connectAttr('{at}.{sec}Slide'.format(at=attr_control, sec=section_side.replace(side, '')), '{}.inputX'.format(translate_clst_rev)) 
                cmds.connectAttr('{}.outputX'.format(translate_clst_rev), '{}.blender'.format(translate_clst_bc)) 
                cmds.connectAttr('{name}.translate'.format(name=new_name), '{}.color1'.format(translate_clst_bc))
                cmds.setAttr('{}.color2R'.format(translate_clst_bc), 0)
                cmds.setAttr('{}.color2G'.format(translate_clst_bc), 0)
                cmds.setAttr('{}.color2B'.format(translate_clst_bc), 0)
                cmds.connectAttr('{}.output'.format(translate_clst_bc), '{}.translate'.format(cv_cluster[1]), f=True)

                #organize
                cmds.parent(cv_cluster, grp_name)

                counter+=1
        else:
            cmds.warning('Found no cvs!')
        
        #connect wisre 
        cmds.select(clear=True)
        dup_curve_deformer = cmds.wire(geo, w=dup_curve[0], n="{sec}_ClusterWire".format(sec=section_side))
        cmds.setAttr('{}.rotation'.format(dup_curve_deformer[0]), 0)
        cmds.setAttr('{}.dropoffDistance[0]'.format(dup_curve_deformer[0]), 999)

        #pass deformer to local geos
        if len(face_geos) > 0:
            for local_geo in face_geos:
                #extra_geo = local_geo.replace('_hi', '_Local')
                if cmds.objExists(local_geo):
                    try:
                        mel.eval('deformer -e -g {} {};'.format(local_geo, "{sec}_ClusterWire".format(sec=section_side)))
                        print('Created {} on {}'.format("{sec}_ClusterWire".format(sec=section_side), local_geo))
                    except:
                        print('Could not pass eyelid deformer to {}.'.format(local_geo))
                else:
                        print('Could not create MoutRollPull blendshape for:{}'.format(local_geo))

        print('Wire modification for {} has been completed.'.format(curve))
    print('Remember to change the input order in the generated wire.')
        

def lip_postbuilds():
    '''
    Collection of Postbuild processes 
    '''
    mt.remove_rivets_ctrls()

    modify_rotation_multiplier()
    mirror_rotation()

    find_corner_controls()
    lip_ctrl_scale_update()

    curve_to_bezier(curve='{}_Up'.format(lips_name))
    curve_to_bezier(curve='{}_Dw'.format(lips_name))

    adjust_corner_percentages()
    
    print('Lip postbuilds have been applied.')
    

def modify_rotation_multiplier():
    lips_locators_main_grp = cmds.ls('{}*_*Roll_**Ctrl_Grp'.format(lips_name))
    for locator in lips_locators_main_grp:
        if 'Main' not in locator:
            plug_rx = cmds.listConnections('{}.rx'.format(locator))[0]
            plug_ry = cmds.listConnections('{}.ry'.format(locator))[0]
            plug_rz = cmds.listConnections('{}.rz'.format(locator))[0]
            
            cmds.setAttr('{}.conversionFactor'.format(plug_ry),0.0056)    
            cmds.setAttr('{}.conversionFactor'.format(plug_rz),0.0056)
            cmds.setAttr('{}.conversionFactor'.format(plug_rx),0.0056)
            if '10' in locator:
                cmds.setAttr('{}.conversionFactor'.format(plug_rx),0.003)

def mirror_rotation():
    lips_Right_locators = cmds.ls('{}*_*Roll_R_*'.format(lips_name))
    for locator in lips_Right_locators:
        plug_ry = cmds.listConnections('{}.ry'.format(locator))[0]
        plug_rz = cmds.listConnections('{}.rz'.format(locator))[0]
        plug_rx = cmds.listConnections('{}.rx'.format(locator))[0]
        cmds.setAttr('{}.conversionFactor'.format(plug_ry), -0.0056)
        cmds.setAttr('{}.conversionFactor'.format(plug_rz),-0.0056)
        cmds.setAttr('{}.conversionFactor'.format(plug_rx),0.0056)

def find_range_value(lip_locs=None):
    '''
    Find minimum and maximun values in the amount of locators
    Args:
        up_lip_locs(locs list): Locators found in a group
    Returns:
        [int,int]: minimun and maximum number of locs
    '''
    result_lip_locs = []
    for inp_str in lip_locs:
        num = re.findall(r'\d+', inp_str)[0]
        result_lip_locs.append(num)
    int_list_top = [eval(i) for i in result_lip_locs] 
    min_value = min(int_list_top)
    max_value = max(int_list_top)
    return [min_value,max_value]

def find_corner_controls():
    #find out corner locs

    up_lip_locs = cmds.listRelatives('{}_Up_FollowLocators_Grp'.format(lips_name))
    dw_lip_locs = cmds.listRelatives('{}_Dw_FollowLocators_Grp'.format(lips_name))

    max_locs = []
    min_locs = []

    values = find_range_value(up_lip_locs)

    for loc_grp in up_lip_locs:
        if '_{}_'.format(str(values[1])) in loc_grp:
            loc_node = cmds.listRelatives(loc_grp, ad = True, type = 'transform')[0]
            max_locs.append(loc_node)
            cmds.parentConstraint('{}_Center_Grp'.format(lips_name), loc_grp, mo = True, sr=["x","y","z"])
        
        if '_{}_'.format(str(values[0])) in loc_grp:
            loc_node = cmds.listRelatives(loc_grp, ad = True, type = 'transform')[0]
            min_locs.append(loc_node) 
            cmds.parentConstraint('{}_Center_Grp'.format(lips_name), loc_grp, mo = True, sr=["x","y","z"])

    values = find_range_value(dw_lip_locs)

    for loc_grp in dw_lip_locs:
        if '_{}_'.format(str(values[1])) in loc_grp:
            loc_node = cmds.listRelatives(loc_grp, ad = True, type = 'transform')[0]
            max_locs.append(loc_node)
        
        if '_{}_'.format(str(values[0])) in loc_grp:
            loc_node = cmds.listRelatives(loc_grp, ad = True, type = 'transform')[0]
            min_locs.append(loc_node)    

    #Create grp to connect ctrls
    max_locs_grps = []
    min_locs_grps = []

    for loc in max_locs:
        off_grp = cmds.group(loc, n = '{}_corner_Ctrl_Grp'.format(loc))
        max_locs_grps.append(off_grp)
        in_poc = cmds.listConnections('{}.translate'.format(loc), plugs = True)[-1]
        cmds.disconnectAttr(in_poc, '{}.translate'.format(loc))
        
    for loc in min_locs:
        off_grp = cmds.group(loc, n = '{}_corner_Ctrl_Grp'.format(loc))
        min_locs_grps.append(off_grp)
        in_poc = cmds.listConnections('{}.translate'.format(loc), plugs = True)[-1]
        cmds.disconnectAttr(in_poc, '{}.translate'.format(loc))

    #Create controleer and place
    L_mid_ctrl = cmds.circle(nr=(0, 0, 1), center = (0,0,0), r = 0.2, n = 'L_{}_Mid_Ctrl'.format(lips_name))
    cmds.group('L_{}_Mid_Ctrl'.format(lips_name), n = 'L_{}_Mid_Ctrl_Offset_Grp'.format(lips_name))
    cmds.parentConstraint('L_{}_Main_Ctrl'.format(lips_name), 'L_{}_Mid_Ctrl_Offset_Grp'.format(lips_name))
    cmds.parent('L_{}_Mid_Ctrl_Offset_Grp'.format(lips_name), '{}_Center_Ctrl'.format(lips_name))

    R_mid_ctrl = cmds.circle(nr=(0, 0, 1), center = (0,0,0), r = 0.2, n = 'R_{}_Mid_Ctrl'.format(lips_name))
    cmds.group('R_{}_Mid_Ctrl'.format(lips_name), n = 'R_{}_Mid_Ctrl_Offset_Grp'.format(lips_name))
    cmds.group('R_{}_Mid_Ctrl_Offset_Grp'.format(lips_name), n = 'R_{}_Mid_Ctrl_Offset_GrpMirror_Grp'.format(lips_name))
    cmds.setAttr('R_{}_Mid_Ctrl_Offset_GrpMirror_Grp.sx'.format(lips_name), -1)
    cmds.setAttr('R_{}_Mid_Ctrl_Offset_GrpMirror_Grp.sy'.format(lips_name), -1)
    cmds.setAttr('R_{}_Mid_Ctrl_Offset_GrpMirror_Grp.sz'.format(lips_name), -1)
    cmds.setAttr('R_{}_Mid_Ctrl_Offset_GrpMirror_Grp.rx'.format(lips_name), 180)
    cmds.delete(cmds.parentConstraint('R_{}_Main_Ctrl'.format(lips_name), 'R_{}_Mid_Ctrl_Offset_GrpMirror_Grp'.format(lips_name)))
    cmds.parentConstraint('R_{}_Main_Ctrl'.format(lips_name), 'R_{}_Mid_Ctrl_Offset_Grp'.format(lips_name))
    cmds.parent('R_{}_Mid_Ctrl_Offset_GrpMirror_Grp'.format(lips_name), '{}_Center_Ctrl'.format(lips_name))

    cmds.select('{}.cv[0:7]'.format(L_mid_ctrl[0]))
    cmds.move(0,0,0.8, wd = False, r=True, oj=True)
    cmds.select('{}.cv[0:7]'.format(R_mid_ctrl[0]))
    cmds.move(0,0,0.8, wd = False, r=True, oj=True)
    cmds.setAttr('{}.lineWidth'.format(L_mid_ctrl[0]), 2)
    cmds.setAttr('{}.lineWidth'.format(R_mid_ctrl[0]), 2)
    mt.assign_color(L_mid_ctrl[0], 'yellow')
    mt.assign_color(R_mid_ctrl[0], 'yellow')

    for grp in max_locs_grps:
        cmds.connectAttr('L_{}_Mid_Ctrl.translate'.format(lips_name), '{}.translate'.format(grp))
        cmds.connectAttr('L_{}_Mid_Ctrl.rotate'.format(lips_name), '{}.rotate'.format(grp))
        cmds.connectAttr('L_{}_Mid_Ctrl.scale'.format(lips_name), '{}.scale'.format(grp))

    for grp in min_locs_grps:
        rev_node = cmds.createNode('multiplyDivide', n = '{}_reverse_md'.format(grp))
        cmds.setAttr('{}.input2X'.format(rev_node), -1)
        cmds.setAttr('{}.input2Y'.format(rev_node), -1)
        cmds.setAttr('{}.input2Z'.format(rev_node), -1)
        cmds.connectAttr('R_{}_Mid_Ctrl.translate'.format(lips_name), '{}.translate'.format(grp))
        cmds.connectAttr('R_{}_Mid_Ctrl.rotate'.format(lips_name), '{}.rotate'.format(grp))
        cmds.connectAttr('R_{}_Mid_Ctrl.scale'.format(lips_name), '{}.scale'.format(grp))
        cmds.connectAttr('R_{}_Mid_Ctrl.translateX'.format(lips_name), '{}.input1X'.format(rev_node))
        cmds.connectAttr('R_{}_Mid_Ctrl.rotateY'.format(lips_name), '{}.input1Y'.format(rev_node))
        cmds.connectAttr('R_{}_Mid_Ctrl.rotateZ'.format(lips_name), '{}.input1Z'.format(rev_node))
        cmds.connectAttr('{}.outputX'.format(rev_node), '{}.translateX'.format(grp), f = True)
        cmds.connectAttr('{}.outputY'.format(rev_node), '{}.rotateY'.format(grp), f = True)
        cmds.connectAttr('{}.outputZ'.format(rev_node), '{}.rotateZ'.format(grp), f = True)     


def lip_ctrl_scale_update():
    #Add scale
    lips_locators = cmds.ls('{}*_*Loc'.format(lips_name))
    for loc in lips_locators:
        first_Parent = cmds.listConnections('{}.rotate'.format(loc) ,s = True,et = True, t = 'parentConstraint')[0]
        for parent_member in first_Parent:
            second_parent = cmds.listConnections('{}.constraintRotateX'.format(first_Parent) ,s = True)[0]
            cmds.scaleConstraint('{}'.format(loc), '{}'.format(second_parent), mo = True)

    lips_locators_grp = cmds.ls('{}*_*Roll_**_Grp'.format(lips_name))
    for loct in lips_locators_grp:
        plug_rx = cmds.listConnections('{}.rx'.format(loct), scn = True)[0]
        plug_ry = cmds.listConnections('{}.ry'.format(loct), scn = True)[0]
        plug_rz = cmds.listConnections('{}.rz'.format(loct), scn = True)[0]
        
        mult_valueX = cmds.getAttr('{}.input2X'.format(plug_rx))
        mult_valueY = cmds.getAttr('{}.input2X'.format(plug_ry))
        mult_valueZ = cmds.getAttr('{}.input2X'.format(plug_rz))
        
        cmds.setAttr('{}.input2Y'.format(plug_rx), mult_valueX*3)
        cmds.setAttr('{}.input2Y'.format(plug_ry), mult_valueY*3)
        cmds.setAttr('{}.input2Y'.format(plug_rz), mult_valueZ*3)
        
        control_plug_x = cmds.listConnections('{}.input1X'.format(plug_rx), scn = True)[0]
        control_plug_y = cmds.listConnections('{}.input1X'.format(plug_ry), scn = True)[0]
        control_plug_z = cmds.listConnections('{}.input1X'.format(plug_rz), scn = True)[0]
        
        minus_one = cmds.createNode('plusMinusAverage', n = '{}_scale_pma_sub'.format(loct))
        cmds.setAttr('{}.operation'.format(minus_one), 2)
        cmds.setAttr('{}.input3D[1].input3Dx'.format(minus_one), 1)
        cmds.setAttr('{}.input3D[1].input3Dy'.format(minus_one), 1)
        cmds.setAttr('{}.input3D[1].input3Dz'.format(minus_one), 1)
        
        cmds.connectAttr('{}.sx'.format(control_plug_x), '{}.input3D[0].input3Dx'.format(minus_one))
        cmds.connectAttr('{}.sy'.format(control_plug_y), '{}.input3D[0].input3Dy'.format(minus_one))
        cmds.connectAttr('{}.sz'.format(control_plug_z), '{}.input3D[0].input3Dz'.format(minus_one))
        
        cmds.connectAttr('{}.output3D.output3Dx'.format(minus_one), '{}.input1Y'.format(plug_rx))
        cmds.connectAttr('{}.output3D.output3Dy'.format(minus_one), '{}.input1Y'.format(plug_ry))
        cmds.connectAttr('{}.output3D.output3Dz'.format(minus_one), '{}.input1Y'.format(plug_rz))
        
        plus_one = cmds.createNode('plusMinusAverage', n = '{}_scale_pma_add'.format(loct))
        cmds.setAttr('{}.input3D[1].input3Dx'.format(plus_one), 1)
        cmds.setAttr('{}.input3D[1].input3Dy'.format(plus_one), 1)
        cmds.setAttr('{}.input3D[1].input3Dz'.format(plus_one), 1)

        cmds.connectAttr('{}.outputY'.format(plug_rx),'{}.input3D[0].input3Dx'.format(plus_one))
        cmds.connectAttr('{}.outputY'.format(plug_ry),'{}.input3D[0].input3Dy'.format(plus_one))
        cmds.connectAttr('{}.outputY'.format(plug_rz),'{}.input3D[0].input3Dz'.format(plus_one))
        
        cmds.connectAttr('{}.output3D.output3Dx'.format(plus_one), '{}.sx'.format(loct))
        cmds.connectAttr('{}.output3D.output3Dy'.format(plus_one), '{}.sy'.format(loct))
        cmds.connectAttr('{}.output3D.output3Dz'.format(plus_one), '{}.sz'.format(loct))
            
        
def curve_to_bezier(curve=''):
    vrt_crv = '{}_Vtx_Crv'.format(curve)
    wireDriver_crv = '{}_WireDriver_Crv'.format(curve)
    #clean existing curves
    curve_history = cmds.listHistory(vrt_crv)
    for node in curve_history:
        if cmds.objExists(node):
            if cmds.nodeType(node) == 'wire':
                try:
                    cmds.delete(node)
                except:
                    continue
    cmds.select(wireDriver_crv)
    mel.eval('doDetachSkin "2" { "1","1" };')
    cmds.select(wireDriver_crv)
    mel.eval('nurbsCurveToBezier;')
    cmds.delete(wireDriver_crv, ch=True)

    curve_nodes = cmds.listRelatives('{}_Jnt_Grp'.format(curve), ad=True)
    curve_skinjnts = []
    for node in curve_nodes:
        if cmds.nodeType(node) == "joint":
            curve_skinjnts.append(node)
    
    cmds.skinCluster(curve_skinjnts, wireDriver_crv, sm=0, bm=1, tsb=True)

    curve_wire = mel.eval('wire -n "{}_Wire" -gw false -en 1.000000 -ce 0.000000 -li 0.000000 -w {} {};'.format(curve, wireDriver_crv, vrt_crv))
        
def adjust_corner_percentages(): 
    dw_lip_locs = cmds.listRelatives('{}_Dw_FollowLocators_Grp'.format(lips_name))
    max_value = find_range_value(dw_lip_locs)[1]

    perc_number = max_value/4
    sum_number = 1/float(perc_number-1)
    count =  max_value-1
    percentage = 1-sum_number

    while  percentage > 0:
        grp = cmds.group('{}_Up_{}_Loc'.format(lips_name, count), n = '{}_Up_{}_Loc_corner_Ctrl_Grp'.format(lips_name, count))
        md_t = cmds.createNode('multiplyDivide', n = '{}_Up_{}_Loc_corner_Ctrl_t_md'.format(lips_name, count))
        cmds.setAttr('{}.input2X'.format(md_t), percentage)
        cmds.setAttr('{}.input2Y'.format(md_t), percentage)
        cmds.setAttr('{}.input2Z'.format(md_t), percentage)
        md_r = cmds.createNode('multiplyDivide', n = '{}_Up_{}_Loc_corner_Ctrl_r_md'.format(lips_name, count))
        cmds.setAttr('{}.input2X'.format(md_r), percentage)
        cmds.setAttr('{}.input2Y'.format(md_r), percentage)
        cmds.setAttr('{}.input2Z'.format(md_r), percentage)
        cmds.connectAttr('L_{}_Mid_Ctrl.translate'.format(lips_name), '{}.input1'.format(md_t))
        cmds.connectAttr('L_{}_Mid_Ctrl.rotate'.format(lips_name), '{}.input1'.format(md_r))
        cmds.connectAttr('{}.output'.format(md_t),'{}.translate'.format(grp))
        cmds.connectAttr('{}.output'.format(md_r),'{}.rotate'.format(grp))


        grp = cmds.group('{}_Dw_{}_Loc'.format(lips_name, count), n = '{}_Dw_{}_Loc_corner_Ctrl_Grp'.format(lips_name, count))
        md_t = cmds.createNode('multiplyDivide', n = '{}_Dw_{}_Loc_corner_Ctrl_t_md'.format(lips_name, count))
        cmds.setAttr('{}.input2X'.format(md_t), percentage)
        cmds.setAttr('{}.input2Y'.format(md_t), percentage)
        cmds.setAttr('{}.input2Z'.format(md_t), percentage)
        md_r = cmds.createNode('multiplyDivide', n = '{}_Dw_{}_Loc_corner_Ctrl_r_md'.format(lips_name, count))
        cmds.setAttr('{}.input2X'.format(md_r), percentage)
        cmds.setAttr('{}.input2Y'.format(md_r), percentage)
        cmds.setAttr('{}.input2Z'.format(md_r), percentage)
        cmds.connectAttr('L_{}_Mid_Ctrl.translate'.format(lips_name), '{}.input1'.format(md_t))
        cmds.connectAttr('L_{}_Mid_Ctrl.rotate'.format(lips_name), '{}.input1'.format(md_r))
        cmds.connectAttr('{}.output'.format(md_t),'{}.translate'.format(grp))
        cmds.connectAttr('{}.output'.format(md_r),'{}.rotate'.format(grp))         
        
        count = count-1
        percentage = percentage-sum_number

    percentage = 1-sum_number
    count = 1
    while  percentage > 0:
        grp = cmds.group('{}_Up_{}_Loc'.format(lips_name, count), n = '{}_Up_{}_Loc_corner_Ctrl_Grp'.format(lips_name, count))
        md_t = cmds.createNode('multiplyDivide', n = '{}_Up_{}_Loc_corner_Ctrl_t_md'.format(lips_name, count))
        cmds.setAttr('{}.input2X'.format(md_t), -percentage)
        cmds.setAttr('{}.input2Y'.format(md_t), percentage)
        cmds.setAttr('{}.input2Z'.format(md_t), percentage)
        md_r = cmds.createNode('multiplyDivide', n = '{}_Up_{}_Loc_corner_Ctrl_r_md'.format(lips_name, count))
        cmds.setAttr('{}.input2X'.format(md_r), percentage)
        cmds.setAttr('{}.input2Y'.format(md_r), -percentage)
        cmds.setAttr('{}.input2Z'.format(md_r), -percentage)
        cmds.connectAttr('R_{}_Mid_Ctrl.translate'.format(lips_name), '{}.input1'.format(md_t))
        cmds.connectAttr('R_{}_Mid_Ctrl.rotate'.format(lips_name), '{}.input1'.format(md_r))
        cmds.connectAttr('{}.output'.format(md_t),'{}.translate'.format(grp))
        cmds.connectAttr('{}.output'.format(md_r),'{}.rotate'.format(grp))

        grp = cmds.group('{}_Dw_{}_Loc'.format(lips_name,count), n = '{}_Dw_{}_Loc_corner_Ctrl_Grp'.format(lips_name, count))
        md_t = cmds.createNode('multiplyDivide', n = '{}_Dw_{}_Loc_corner_Ctrl_t_md'.format(lips_name, count))
        cmds.setAttr('{}.input2X'.format(md_t), -percentage)
        cmds.setAttr('{}.input2Y'.format(md_t), percentage)
        cmds.setAttr('{}.input2Z'.format(md_t), percentage)
        md_r = cmds.createNode('multiplyDivide', n = '{}_Dw_{}_Loc_corner_Ctrl_r_md'.format(lips_name, count))
        cmds.setAttr('{}.input2X'.format(md_r), percentage)
        cmds.setAttr('{}.input2Y'.format(md_r), -percentage)
        cmds.setAttr('{}.input2Z'.format(md_r), -percentage)
        cmds.connectAttr('R_{}_Mid_Ctrl.translate'.format(lips_name), '{}.input1'.format(md_t))
        cmds.connectAttr('R_{}_Mid_Ctrl.rotate'.format(lips_name), '{}.input1'.format(md_r))
        cmds.connectAttr('{}.output'.format(md_t),'{}.translate'.format(grp))
        cmds.connectAttr('{}.output'.format(md_r),'{}.rotate'.format(grp))         
        
        count = count+1
        percentage = percentage-sum_number   
