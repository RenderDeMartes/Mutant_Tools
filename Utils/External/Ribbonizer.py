from __future__ import absolute_import, division
"""
ao_ribbonizer.py
version 2.0
copyright (C) 2018 Orkhan Ashrafov
email: o.ashrafov@gmail.com
given a nurbs surface creates a ribbon.
---------------------------------------------------------------------------------------------------------------------------------------------
install instructions: place this file in the default "scripts" folder. go to maya and run these two lines from a python tab:

import ao_ribbonizer
reload(ao_ribbonizer)
ao_ribbonizer.UI()

import Mutant_Tools
import imp
imp.reload(Mutant_Tools)
from Mutant_Tools.Utils.External import Ribbonizer
Ribbonizer.ribbonize(surf_tr, equal, num_of_Ctrls, num_of_Jnts, prefix, constrain, add_fk, wire)

---------------------------------------------------------------------------------------------------------------------------------------------
EQUAL DIST - if checked, controls are distributed with equal distance from one another. if not,
they are distributed proportionally according to the deformed surface (this was the case in the older version).
no difference in results unless the surface is deformed after creation (i.e: cvs have been moved).
in any case, the final bind joints are always distributed with equal distance. default is checked.
CONSTRAIN - control joints are constrained to the controls. if not checked, joints are controlled by direct connections. default is checked.
WIRE - deform the surface using wire deformer instead of skinCluster. skinCluster is used if there's only 1 control
ADD FK - add fk controls over the ik ones to the rig. skipped if the surface is periodic
"""

import maya.OpenMaya as om
import maya.cmds as cmds
import Mutant_Tools.Utils.Rigging
from Mutant_Tools.Utils.Rigging import main_mutant

mt = main_mutant.Mutant()
nc, curve_data, setup = mt.import_configs()

def get_bbox_center(obj):
    shapes = cmds.listRelatives(obj, s=True)  # get bb of the shape in case there are children
    cvs = []
    for shape in shapes:
        num_of_cvs = cmds.getAttr(shape + ".controlPoints", size=True)
        cvs.append("{}.cv[0:{}]".format(shape, num_of_cvs - 1))

    bbmin = cmds.exactWorldBoundingBox(cvs)[:3]
    bbmax = cmds.exactWorldBoundingBox(cvs)[3:7]

    mid_point = [(b_max + b_min) / 2 for b_min, b_max in zip(bbmin, bbmax)]

    return mid_point


def make_fk_Ctrls(prefix, num_of_Ctrls):
    fk_Ctrls = []
    fk_Ctrl_off_Grps = []

    fk_Ctrls = Ctrl_maker(prefix, Ctrl_type="circle", count=num_of_Ctrls - 1, deg=3, sp=8, name="fk")
    fk_Ctrl_off_Grps = [cmds.group(fk_Ctrl, n=fk_Ctrl + "_offset") for fk_Ctrl in fk_Ctrls]
    [cmds.xform(fk_Ctrl_off_Grp, piv=(0, 0, 0), os=True) for fk_Ctrl_off_Grp in fk_Ctrl_off_Grps]

    for (o, f) in zip(fk_Ctrl_off_Grps[1:], fk_Ctrls[:-1]):
        cmds.parent(o, f)

    return fk_Ctrls, fk_Ctrl_off_Grps


##########################################################################################

def Ctrl_maker(prefix, Ctrl_type, count, deg, sp, name=""):

    ribbonizer_int = 0
    if name != "":
        name = name + "_"

    Ctrls = []
    for x in range(count):

        if Ctrl_type == "cube":
            cmds.select(cl=True)
            c1 = mt.curve(input='',
                            type='cube',
                            rename=True,
                            custom_name=True,
                            name="{}{}{:02d}_Ctrl".format(prefix, name, ribbonizer_int),
                            size=1)
            # c1 = cmds.curve(p=[(-1.0, 1.0, 1.0), (-1.0, 1.0, -1.0), (1.0, 1.0, -1.0),
            #                  (1.0, 1.0, 1.0), (-1.0, 1.0, 1.0), (-1.0, -1.0, 1.0),
            #                  (1.0, -1.0, 1.0), (1.0, -1.0, -1.0), (-1.0, -1.0, -1.0),
            #                  (-1.0, -1.0, 1.0), (-1.0, -1.0, -1.0), (-1.0, 1.0, -1.0),
            #                  (1.0, 1.0, -1.0), (1.0, -1.0, -1.0), (1.0, -1.0, 1.0), (1.0, 1.0, 1.0)],
            #               k=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15], d=1)
            ribbonizer_int = ribbonizer_int + 1
            Ctrls.append(c1)

        elif Ctrl_type == "sphere":
            cmds.select(cl=True)
            c1 = mt.curve(input='',
                            type='sphere',
                            rename=True,
                            custom_name=True,
                            name="{}{}{:02d}_Ctrl".format(prefix, name, ribbonizer_int),
                            size=1)
            # c1 = cmds.circle(d=deg, s=sp, nr=(1, 0, 0), r=1, ch=0)[0]
            # c2 = cmds.circle(d=deg, s=sp, nr=(0, 1, 0), r=1, ch=0)[0]
            # c3 = cmds.circle(d=deg, s=sp, nr=(0, 0, 1), r=1, ch=0)[0]
            #
            # cmds.parent(cmds.listRelatives(c2, s=True), cmds.listRelatives(c3, s=True), c1, r=True, s=True)
            # cmds.delete(c2, c3)
            ribbonizer_int = ribbonizer_int + 1
            Ctrls.append(c1)

        elif Ctrl_type == "circle":
            cmds.select(cl=True)
            c1 = mt.curve(input='',
                            type='circleX',
                            rename=True,
                            custom_name=True,
                            name="{}{}{:02d}_Ctrl".format(prefix, name, ribbonizer_int),
                            size=1)
            # c1 = cmds.circle(d=deg, s=sp, nr=(1, 0, 0), r=1, ch=0)[0]
            ribbonizer_int = ribbonizer_int + 1
            Ctrls.append(c1)

    for x, Ctrl in enumerate(Ctrls):
        #Ctrls[x] = cmds.rename(Ctrl, "{}{}{:02d}_Ctrl".format(prefix, name, x + 1))
        shapes = cmds.listRelatives(Ctrls[x], f=True, s=True)
        for y, shape in enumerate(shapes):
            cmds.rename(shape, "{}Shape{:02d}".format(Ctrls[x], y + 1))

    cmds.select(cl=True)
    return Ctrls


#######################################################################

def lock_hide(objs, attrs):
    for obj in objs:
        for attr in attrs:
            cmds.setAttr(obj + attr, l=True, k=False, cb=False)


#####################################################################

def param_from_length(curve, count, curve_type="open", space="uv", normalized=True):
    if curve_type == "periodic":
        divider = count
    else:
        divider = count - 1

    if divider == 0:
        divider = 1

    dag = om.MDagPath()
    obj = om.MObject()
    crv = om.MSelectionList()
    crv.add(curve)
    crv.getDagPath(0, dag, obj)

    curve_fn = om.MFnNurbsCurve(dag)
    length = curve_fn.length()

    param = [curve_fn.findParamFromLength(i * ((1 / float(divider)) * length)) for i in range(count)]

    if space == "world":
        data = []
        space = om.MSpace.kWorld
        point = om.MPoint()
        for p in param:
            curve_fn.getPointAtParam(p, point, space)
            data.append([point[0], point[1], point[2]])  # world space points
    elif normalized == True:

        def normalizer(value, old_range, new_range):
            return (value - old_range[0]) * (new_range[1] - new_range[0]) / (old_range[1] - old_range[0]) + new_range[0]

        max_v = cmds.getAttr(curve + ".minMaxValue.maxValue")
        min_v = cmds.getAttr(curve + ".minMaxValue.minValue")

        # normalized parameters (before i was just dividing p to max_v. but with weird ranges (ie. 1.4281 to 6.98214) the result is of != as expected. this also could have been fixed by just rebuilding the surface uniformly)
        data = [normalizer(p, [min_v, max_v], [0, 1]) for p in param]
    else:
        data = param

    return data


#####################################################################

def set_color(objects, color):
    color_dict = {"blue": 6, "red": 13, "green": 14, "mid_blue": 15, "yellow": 22, "light_green": 23}

    if isinstance(objects, list):
        for obj in objects:
            if cmds.listRelatives(obj, f=True, s=True) != None:
                shapes = cmds.listRelatives(obj, f=True, s=True)
                for shape in shapes:
                    cmds.setAttr(obj + ".ove", 1)
                    cmds.setAttr(obj + ".ovc", color_dict[color])
            else:
                cmds.setAttr(obj + ".ove", 1)
                cmds.setAttr(obj + ".ovc", color_dict[color])
    else:
        if cmds.listRelatives(objects, f=True, s=True) != None:
            shapes = cmds.listRelatives(objects, f=True, s=True)
            for shape in shapes:
                cmds.setAttr(objects + ".ove", 1)
                cmds.setAttr(objects + ".ovc", color_dict[color])
        else:
            cmds.setAttr(objects + ".ove", 1)
            cmds.setAttr(objects + ".ovc", color_dict[color])


def get_selection():
    # check if nurbsSurface is selected
    sel = cmds.ls(sl=True)

    if not sel:
        cmds.warning("select a nurbs surface to ribbonize")
        return

    shapes = cmds.listRelatives(sel[0], s=True, f=True)

    if shapes and cmds.objectType(shapes[0]) == "nurbsSurface":
        surf_tr = sel[0]
    # after changing attributes on "makeNurbPlane" node it stays selected.
    # so instead of raising an error we just get the connected surface
    elif cmds.objectType(sel[0]) == "makeNurbPlane" or cmds.objectType(sel[0]) == "makeNurbCylinder":
        surf_tr = cmds.listConnections(sel[0] + ".outputSurface", d=True, s=False)[0]
    else:
        cmds.warning("dude, that isn't a nurbs surface")
        return

    return surf_tr


def ribbonize(surf_tr, equal=1, num_of_Ctrls=5, num_of_Jnts=29, prefix="", constrain=1, add_fk=0, wire=0, middle_ctrl_pos='Original'):
    attrs = [".tx", ".ty", ".tz", ".rx", ".ry", ".rz", ".sx", ".sy", ".sz", ".v"]

    if prefix == "":
        cmds.warning("care to name it?")
        return

    else:
        prefix = prefix + "_"

    #####################################################

    surf_tr = cmds.rename(surf_tr, prefix + "ribbon_surface")
    surf = cmds.listRelatives(surf_tr, shapes=True)[0]

    # freeze transformations and delete the surface history
    cmds.makeIdentity(surf_tr, t=True, r=True, s=True, apply=True)
    cmds.delete(surf_tr, ch=True)

    # duplicate surface curves to determine the direction
    u_curve = cmds.duplicateCurve(surf_tr + ".v[.5]", local=True, ch=0)
    v_curve = cmds.duplicateCurve(surf_tr + ".u[.5]", local=True, ch=0)

    # delete the history just in case
    cmds.delete(surf_tr, ch=True)

    u_length = cmds.arclen(u_curve)
    v_length = cmds.arclen(v_curve)

    if u_length < v_length:
        cmds.reverseSurface(surf_tr, d=3, ch=False, rpo=True)
        cmds.reverseSurface(surf_tr, d=0, ch=False, rpo=True)

    parameter = ".parameterU"
    other_param = ".parameterV"

    # correct u_curve after reversing to calculate the length
    u_curve_corr = cmds.duplicateCurve(surf_tr + ".v[.5]", local=True, ch=0)[0]

    #############################################################################

    # selected surface is periodic or open? (cylinder or a plane)
    if cmds.getAttr(surf + ".formU") == 2 or cmds.getAttr(surf + ".formV") == 2:
        curve_type = "periodic"
        divider_for_Ctrls = num_of_Ctrls
    elif cmds.getAttr(surf + ".formU") == 0 or cmds.getAttr(surf + ".formV") == 0:
        curve_type = "open"
        divider_for_Ctrls = num_of_Ctrls - 1

    #############################################################################
    param_Ctrls = param_from_length(u_curve_corr, num_of_Ctrls, curve_type, "uv")
    param_joints = param_from_length(u_curve_corr, num_of_Jnts, curve_type, "uv")

    length = cmds.arclen(u_curve_corr)
    cmds.delete(u_curve, v_curve, u_curve_corr)

    ############################################################################

    # create groups, main control and main control offset
    #final_group = cmds.group(n=prefix + "Ribbon_Grp", em=True)
    Ctrl_joints_Grp = cmds.group(n=prefix + "Ctrl_Joints_Grp", em=True)
    Ctrl_Grp = cmds.group(n=prefix + "Ctrls_Grp", em=True)
    follicles_Grp = cmds.group(n=prefix + "Follicles_Grp", em=True)
    rig_Grp = cmds.group(n=prefix + "Rig_Grp", em=True)
    cmds.select(cl=True)
    main_Ctrl = mt.curve(input='',
                         type='circleX',
                         rename=True,
                         custom_name=True,
                         name=prefix + "Main_Ctrl",
                         size=length / 5)
    main_Ctrl_offset = cmds.group(n=prefix + "Ctrl_Main_Offset_Grp", em=True)
    cmds.parent(main_Ctrl, main_Ctrl_offset)
    cmds.parent(Ctrl_Grp, main_Ctrl)
    #cmds.parent(main_Ctrl_offset, rig_Grp, final_group)
    cmds.parent(surf_tr, Ctrl_joints_Grp, follicles_Grp, rig_Grp)



    ############################################################################

    fols = []
    fols_tr = []
    bind_Jnts = []
    Bind_joints_rad = (length / 60) / (float(num_of_Jnts) / 40)

    #u_value = 1/num_of_Jnts
    #value = 0
    for x in range(num_of_Jnts):
        fol = cmds.createNode("follicle")
        cmds.setAttr(fol + ".visibility", 0)
        temp_fol = cmds.listRelatives(fol, p=True)[0]
        fols_tr.append(cmds.rename(temp_fol, "{}follicle_{:02d}".format(prefix, x + 1)))
        fols.append(cmds.listRelatives(fols_tr[-1], s=True)[0])

        # connect follicle shapes to their transforms
        cmds.connectAttr(fols[-1] + ".outTranslate", fols_tr[-1] + ".translate", f=True)
        cmds.connectAttr(fols[-1] + ".outRotate", fols_tr[-1] + ".rotate", f=True)

        # attach follicle shapes to the surface
        cmds.connectAttr(surf + ".worldMatrix[0]", fols[-1] + ".inputWorldMatrix")
        cmds.connectAttr(surf + ".local", fols[-1] + ".inputSurface")

        cmds.setAttr(fols[-1] + parameter, param_joints[x])
        #cmds.setAttr(fols[-1] + parameter, value)
        cmds.setAttr(fols[-1] + other_param, 0.5)

        cmds.parent(fols_tr[-1], follicles_Grp)

        # create final bind joints on the surface
        bind_Jnts.append(cmds.createNode("joint", n="{}Bind_{:02d}_Bnd".format(prefix, x + 1)))

        cmds.parentConstraint(fols_tr[-1], bind_Jnts[-1], mo=False)
        cmds.scaleConstraint(fols_tr[-1], bind_Jnts[-1], mo=False)

        cmds.setAttr(bind_Jnts[-1] + ".radius", Bind_joints_rad)

        #value = value + u_value

    set_color(bind_Jnts, "mid_blue")

    ############################################################################

    # create temp follicles for control offset groups to align
    temp_fols = []
    temp_fols_tr = []

    for x in range(num_of_Ctrls):
        temp_fols.append(cmds.createNode("follicle"))
        temp_fols_tr.append(cmds.listRelatives(temp_fols[-1], p=True)[0])

        cmds.connectAttr(temp_fols[-1] + ".outTranslate", temp_fols_tr[-1] + ".translate", f=True)
        cmds.connectAttr(temp_fols[-1] + ".outRotate", temp_fols_tr[-1] + ".rotate", f=True)

        cmds.connectAttr(surf + ".worldMatrix[0]", temp_fols[-1] + ".inputWorldMatrix")
        cmds.connectAttr(surf + ".local", temp_fols[-1] + ".inputSurface")

    ####################################################

    if equal == 1:
        for x, temp_fol in enumerate(temp_fols):
            cmds.setAttr(temp_fol + parameter, param_Ctrls[x])
            cmds.setAttr(temp_fol + other_param, 0.5)
    if equal == 0:
        v = 0
        for temp_fol in temp_fols:
            cmds.setAttr(temp_fol + parameter, v)
            cmds.setAttr(temp_fol + other_param, 0.5)
            v = v + (1.0 / divider_for_Ctrls)

    ####################################################

    # move main_Ctrl_offset to the center of the surfaces bbox (in case its pivot is somewhere else)
    if middle_ctrl_pos == 'Start':
        cmds.delete(cmds.parentConstraint(bind_Jnts[0], main_Ctrl_offset))
    elif middle_ctrl_pos == 'End':
        cmds.delete(cmds.parentConstraint(bind_Jnts[-1], main_Ctrl_offset))
    elif middle_ctrl_pos == 'Cloth':
        mid_point = get_bbox_center(surf_tr)
        for attr, mid_pnt_el in zip(attrs[:3], mid_point):
            cmds.setAttr(main_Ctrl_offset + attr, mid_pnt_el)
        cmds.delete(cmds.orientConstraint(bind_Jnts[0], main_Ctrl_offset))
    else:
        mid_point = get_bbox_center(surf_tr)
        for attr, mid_pnt_el in zip(attrs[:3], mid_point):
            cmds.setAttr(main_Ctrl_offset + attr, mid_pnt_el)
        cmds.delete(cmds.orientConstraint(bind_Jnts[0], bind_Jnts[-1], main_Ctrl_offset))

    ############################################################################

    # create controls and control joints
    controls = Ctrl_maker(prefix, Ctrl_type="cube", count=num_of_Ctrls, deg=3, sp=8)

    Ctrl_ofs_Grps = []
    Ctrl_joints = []
    Ctrl_Jnt_ofs_Grps = []
    Ctrl_joints_rad = Bind_joints_rad * 2
    ik_Ctrl_scale = (length / 35) / (float(num_of_Ctrls) / 5)

    for x, Ctrl in enumerate(controls):

        Ctrl_ofs_Grp = cmds.group(Ctrl, n="{}_Offset_Grp".format(Ctrl))
        cmds.delete(cmds.parentConstraint(temp_fols_tr[x], Ctrl_ofs_Grp))
        Ctrl_ofs_Grps.append(Ctrl_ofs_Grp)

        # scale ik controls
        Ctrl_shapes = cmds.listRelatives(Ctrl, s=True)
        for Ctrl_shape in Ctrl_shapes:
            Ctrl_cvs_count = cmds.getAttr(Ctrl_shape + ".controlPoints", size=True)
            cmds.scale(ik_Ctrl_scale, ik_Ctrl_scale, ik_Ctrl_scale, "{}.cv[0:{}]".format(Ctrl_shape, Ctrl_cvs_count - 1),
                     r=True, ocp=True)

        # create the control joints
        Ctrl_joints.append(cmds.createNode("joint", n="{}Ctrl_{:02d}_Jnt".format(prefix, x + 1)))
        # set the radius of controls joints to 2 times that of the surface joints
        cmds.setAttr(Ctrl_joints[x] + ".radius", Ctrl_joints_rad)
        # create offset groups for Ctrl joints
        Ctrl_Jnt_ofs_Grp = cmds.group(Ctrl_joints[-1], n="{}_Offset_Grp".format(Ctrl_joints[-1]))
        cmds.delete(cmds.parentConstraint(temp_fols_tr[x], Ctrl_Jnt_ofs_Grp))
        Ctrl_Jnt_ofs_Grps.append(Ctrl_Jnt_ofs_Grp)

    ###
    set_color(controls, "green")
    set_color(Ctrl_joints, "red")

    cmds.parent(Ctrl_ofs_Grps, Ctrl_Grp)
    cmds.parent(Ctrl_Jnt_ofs_Grps, Ctrl_joints_Grp)

    #lock_hide(Ctrl_ofs_Grps, attrs[:9])
    #lock_hide(Ctrl_Jnt_ofs_Grps, attrs[:9])

    cmds.delete(temp_fols_tr)

    ####################################################

    # determine if constraint or connection method is chosen
    if constrain == 0:
        for (c, j) in zip(controls, Ctrl_joints):
            for attr in attrs[:7]:  # skip scale attributes
                cmds.connectAttr(c + attr, j + attr)

        childs = cmds.listRelatives(Ctrl_joints_Grp, c=True)
        cmds.parent(childs, w=True)
        cmds.delete(cmds.parentConstraint(main_Ctrl, Ctrl_joints_Grp))
        mt.root_grp(input=Ctrl_joints_Grp)
        cmds.parent(childs, Ctrl_joints_Grp)
        cmds.connectAttr('{}.translate'.format(main_Ctrl), '{}.translate'.format(Ctrl_joints_Grp))
        cmds.connectAttr('{}.rotate'.format(main_Ctrl), '{}.rotate'.format(Ctrl_joints_Grp))
        cmds.connectAttr('{}.scale'.format(main_Ctrl), '{}.scale'.format(Ctrl_joints_Grp))

        #cmds.parentConstraint(main_Ctrl, Ctrl_joints_Grp, mo=True)
        #cmds.scaleConstraint(main_Ctrl, Ctrl_joints_Grp)

        # scale the follicles with the main control
        for flt in fols_tr:
            cmds.connectAttr(main_Ctrl + ".sx", flt + ".sx")
            cmds.connectAttr(main_Ctrl + ".sx", flt + ".sy")
            cmds.connectAttr(main_Ctrl + ".sx", flt + ".sz")

    elif constrain == 1:
        for (c, j) in zip(controls, Ctrl_joints):
            cmds.parentConstraint(c, j)
            cmds.scaleConstraint(c, j)

        # scale the follicles with the main control
        for flt in fols_tr:
            cmds.scaleConstraint(main_Ctrl, flt)

    #######################################################################

    if wire == True and num_of_Ctrls > 1:

        temp_crv = cmds.duplicateCurve(surf_tr + ".v[.5]", n=prefix + "wire_crv", local=False, ch=0)[0]

        if num_of_Ctrls == 2:
            degree = 1
        else:
            degree = 3

        wire_crv = cmds.curve(p=param_from_length(temp_crv, num_of_Ctrls + (num_of_Ctrls - 1), "open", "world"), d=degree)

        cmds.delete(temp_crv)

        wire_crv = cmds.rename(wire_crv,
                             prefix + "wire_crv")  # if name at the creation time, the shape doesn't get renamed
        cmds.delete(wire_crv, ch=True)
        wire = cmds.wire(surf_tr, gw=False, en=1.0, ce=0.0, li=0.0, dds=(0, 50), w=wire_crv, n=prefix + "wire")[0]
        cmds.connectAttr(main_Ctrl + ".sx", wire + ".scale[0]")

        cps = param_from_length(wire_crv, num_of_Ctrls, "open", "uv", normalized=False)

        for cp in cps:
            cmds.select("{}.u[{}]".format(wire_crv, cp), r=True)
            cmds.dropoffLocator(1.0, 1.0, wire)

        cmds.select(cl=True)

        for x, Ctrl in enumerate(controls):
            cmds.connectAttr(Ctrl + ".rx", "{}.wireLocatorTwist[{}]".format(wire, x))

        wire_Grp = cmds.group(wire_crv, wire_crv + "BaseWire", n=prefix + "wire_crv_Grp")
        cmds.parent(wire_Grp, rig_Grp)
        lock_hide([wire_Grp], attrs[:9])

        wire_skin_cluster = cmds.skinCluster(Ctrl_joints, wire_crv, dr=2, mi=2, bm=0)[0]

    else:
        # bind the surface to the joints
        nurbs_skin_cluster = cmds.skinCluster(Ctrl_joints, surf_tr, dr=2, mi=num_of_Ctrls - 1, ns=num_of_Ctrls * 5, bm=0,
                                            n=prefix + "skinCluster")[0]
        cmds.skinPercent(nurbs_skin_cluster, surf_tr, pruneWeights=0.2)

    if wire == True and num_of_Ctrls == 1:
        cmds.warning("wire skipped. at least 2 controls needed")

    ##########################################################################################

    cmds.setAttr(surf_tr + ".v", 0)
    cmds.setAttr(rig_Grp + ".v", 0)

    #cmds.connectAttr(main_Ctrl + ".sx", main_Ctrl + ".sy")
    #cmds.connectAttr(main_Ctrl + ".sx", main_Ctrl + ".sz")
    #cmds.aliasAttr("Scale", main_Ctrl + ".sx")
    scale_Attr = mt.new_attr(input=main_Ctrl, name='Scale', min=-9999, max=9999, default=1)
    cmds.connectAttr(scale_Attr, main_Ctrl + ".sx")
    cmds.connectAttr(scale_Attr, main_Ctrl + ".sy")
    cmds.connectAttr(scale_Attr, main_Ctrl + ".sz")

    set_color(main_Ctrl, "yellow")

    #cmds.connectAttr(main_Ctrl_offset + ".sx", main_Ctrl_offset + ".sy")
    #cmds.connectAttr(main_Ctrl_offset + ".sx", main_Ctrl_offset + ".sz")
    #cmds.aliasAttr("Scale", main_Ctrl_offset + ".sx")

    # lock and hide attributes
    #lock_hide([final_group, follicles_Grp, Ctrl_joints_Grp, surf_tr, Ctrl_Grp, rig_Grp], attrs[:9])
    lock_hide([main_Ctrl], attrs[6:])
    lock_hide(controls, attrs[7:])

    # clear selection
    cmds.select(cl=True)  # if selection isn't cleared a control joint gets added to the bind joints set

    # create a set with bind joints
    #bind_Jnts_set = cmds.sets(n=prefix + "bind_Jnts_set")
    #cmds.sets(bind_Jnts, add=bind_Jnts_set)

    cmds.select(cl=True)

    #ik_Ctrls_set = cmds.sets(n=prefix + "ik_Ctrls_set")
    #cmds.sets(controls, add=ik_Ctrls_set)

    cmds.select(cl=True)

    #controls_set = cmds.sets(n=prefix + "controls_set")
    #cmds.sets(main_Ctrl, ik_Ctrls_set, add=controls_set)

    ##########################################################################################

    if add_fk == 1 and cmds.getAttr(surf + ".formU") != 2 and cmds.getAttr(surf + ".formV") != 2:

        fk_Ctrls, fk_Ctrl_off_Grps = make_fk_Ctrls(prefix, num_of_Ctrls)
        cmds.parent(fk_Ctrl_off_Grps[0], Ctrl_Grp)

        # scale fk controls
        fk_Ctrl_scale = ik_Ctrl_scale * 2

        for fk_Ctrl in fk_Ctrls:
            fk_Ctrl_shapes = cmds.listRelatives(fk_Ctrl, s=True)
            for fk_Ctrl_shape in fk_Ctrl_shapes:
                fk_Ctrl_cvs_count = cmds.getAttr(fk_Ctrl_shape + ".controlPoints", size=True)
                cmds.scale(fk_Ctrl_scale, fk_Ctrl_scale, fk_Ctrl_scale,
                         "{}.cv[0:{}]".format(fk_Ctrl_shape, fk_Ctrl_cvs_count - 1), r=True, ocp=True)

        # add fk controls to a set
        cmds.select(cl=True)
        #fk_Ctrls_set = cmds.sets(n=prefix + "fk_Ctrls_set")
        #cmds.sets(fk_Ctrls, add=fk_Ctrls_set)

        ########
        ik_Ctrl_constr_Grps = [cmds.group(Ctrl, n=Ctrl + "_constr_Grp") for Ctrl in controls]
        [cmds.xform(ik_Ctrl_constr_Grp, piv=(0, 0, 0), os=True) for ik_Ctrl_constr_Grp in ik_Ctrl_constr_Grps]

        for ik, fk in zip(controls[:-1], fk_Ctrl_off_Grps):
            cmds.delete(cmds.parentConstraint(ik, fk))

        for fk, ik in zip(fk_Ctrls, ik_Ctrl_constr_Grps[:-1]):
            cmds.parentConstraint(fk, ik)

        # constrain last ik Ctrl
        cmds.parentConstraint(fk_Ctrls[-1], ik_Ctrl_constr_Grps[-1], mo=True)
        #lock_hide(ik_Ctrl_constr_Grps, attrs[:9])

        ########
        set_color(fk_Ctrls, "blue")
        #lock_hide(fk_Ctrl_off_Grps, attrs[:9])

        #cmds.sets(fk_Ctrls_set, add=controls_set)

        cmds.select(cl=True)

    elif add_fk == 1 and (cmds.getAttr(surf + ".formU") == 2 or cmds.getAttr(surf + ".formV") == 2):

        cmds.warning("surface is periodic. fk controls skipped")

    ################ADD MESSAGE ATTRS################

    cmds.addAttr(main_Ctrl, ln="joints", at="message")
    cmds.addAttr(main_Ctrl, ln="follicles", at="message")
    cmds.addAttr(main_Ctrl, ln="surface", at="message")

    if cmds.attributeQuery("i_am_the_surface", node=surf, exists=True) == False:
        cmds.addAttr(surf, ln="i_am_the_surface", at="message")

    cmds.connectAttr(main_Ctrl + ".surface", surf + ".i_am_the_surface")

    for j, f in zip(bind_Jnts, fols):
        cmds.addAttr(j, ln="i_am_a_joint", at="message")
        cmds.addAttr(f, ln="i_am_a_follicle", at="message")
        cmds.connectAttr(main_Ctrl + ".joints", j + ".i_am_a_joint")
        cmds.connectAttr(main_Ctrl + ".follicles", f + ".i_am_a_follicle")

    ##########################################################################################

    # Group bnd joints
    for i in bind_Jnts:
        if cmds.objExists(prefix + 'Bnd_Grp'):
            cmds.parent(i, prefix + 'Bnd_Grp')
        else:
            cmds.group(em=True, n=prefix + 'Bnd_Grp')
            cmds.parent(i, prefix + 'Bnd_Grp')

    #Return stuff after the build
    return [main_Ctrl_offset, rig_Grp, prefix + 'Bnd_Grp']

class UI(object):

    def __init__(self):

        windowName = "ribbonizer_window"
        windowWidth = 400
        windowHeight = 160

        if cmds.window(windowName, ex=True):
            cmds.deleteUI(windowName)
            cmds.windowPref(windowName, remove=True)

        mainWindow = cmds.window(windowName, t="Ribbonizer 3.0 adapted for BARDEL", s=False, mnb=False, mxb=False)
        cmds.window(windowName, e=True, wh=(windowWidth, windowHeight))
        mainFormL = cmds.formLayout()

        prefixText = cmds.text(l="prefix:")
        self.prefixField = cmds.textField("prefix", pht="name me")
        numCtrlsText = cmds.text(l="num_of_Ctrls:")
        self.numCtrlsField = cmds.intField("num_of_Ctrls", min=1, v=5, step=1)
        numJntsText = cmds.text(l="num_of_Jnts:")
        self.numJntsField = cmds.intField("num_of_Jnts", min=1, v=29, step=1)

        self.equalCheckbox = cmds.checkBox("equal", l="equal_dist", v=True)
        self.constrCheckbox = cmds.checkBox("constrain", l="constrain", v=True)
        self.wireCheckbox = cmds.checkBox("wire", l="wire", v=False)
        self.fkCheckbox = cmds.checkBox("add_fk", l="add_fk", v=False)

        self.ribbonizeBtn = cmds.button(l="Ribbonize", c=self.launch)

        cmds.formLayout(mainFormL, e=True,
                      attachForm=[(prefixText, "left", 20), (numCtrlsText, "left", 20), (numJntsText, "left", 20),
                                  (prefixText, "top", 19),
                                  (self.prefixField, "top", 15),
                                  (self.equalCheckbox, "left", 20), (self.wireCheckbox, "left", 20),
                                  (self.constrCheckbox, "left", 110), (self.fkCheckbox, "left", 110),
                                  (self.prefixField, "left", 110), (self.numCtrlsField, "left", 110),
                                  (self.numJntsField, "left", 110),
                                  (self.ribbonizeBtn, "left", 200), (self.ribbonizeBtn, "right", 15),
                                  (self.ribbonizeBtn, "top", 15), (self.ribbonizeBtn, "bottom", 15),
                                  ],

                      attachControl=[(numCtrlsText, "top", 11, prefixText), (numJntsText, "top", 11, numCtrlsText),
                                     (self.numCtrlsField, "top", 5, self.prefixField),
                                     (self.numJntsField, "top", 5, self.numCtrlsField),
                                     (self.equalCheckbox, "top", 20, self.numJntsField),
                                     (self.wireCheckbox, "top", 5, self.equalCheckbox),
                                     (self.constrCheckbox, "top", 20, self.numJntsField),
                                     (self.fkCheckbox, "top", 5, self.constrCheckbox),
                                     (self.prefixField, "right", 15, self.ribbonizeBtn),
                                     (self.numCtrlsField, "right", 15, self.ribbonizeBtn),
                                     (self.numJntsField, "right", 15, self.ribbonizeBtn),

                                     ])
        cmds.showWindow(mainWindow)

    def launch(self, *args):

        sel = get_selection()

        if not sel:
            return

        surf_tr = sel

        equal = cmds.checkBox(self.equalCheckbox, q=True, v=True)
        num_of_Ctrls = cmds.intField(self.numCtrlsField, q=True, v=True)
        num_of_Jnts = cmds.intField(self.numJntsField, q=True, v=True)
        prefix = cmds.textField(self.prefixField, q=True, tx=True)
        constrain = cmds.checkBox(self.constrCheckbox, q=True, v=True)
        add_fk = cmds.checkBox(self.fkCheckbox, q=True, v=True)
        wire = cmds.checkBox(self.wireCheckbox, q=True, v=True)

        ribbonize(surf_tr, equal, num_of_Ctrls, num_of_Jnts, prefix, constrain, add_fk, wire)

'''

ribbonize(surf_tr, equal, num_of_Ctrls, num_of_Jnts, prefix, constrain, add_fk, wire)

'''