"""World-space mocap retarget onto the Mutant Tools Unreal game template (FK controls).
Source: HumanIK-named FBX (Maya's Examples/Animation/Motion_Capture). Their zero-rotation pose is a neutral stance
(upright, facing +Z, arms 30 deg down), so calibration = zero the source, rotate each source bone onto our rest bone
direction, constrain every FK control to its source bone with maintain-offset, bake."""
import math, maya.cmds as c, maya.api.OpenMaya as om
MAP = [  # source bone, control, (source child, rig joint, rig child) for the direction match
    ('Hips', 'COG_Ctrl', None),
    ('Spine', 'Spine_Base_FK_Ctrl', ('Spine1', 'spine_01', 'spine_03')),
    ('Spine1', 'Spine_Belly_FK_Ctrl', ('Spine2', 'spine_03', 'spine_04')),
    ('Spine2', None, ('Spine3', 'spine_04', 'spine_05')),
    ('Spine3', 'Spine_Chest_FK_Ctrl', ('Neck', 'spine_05', 'neck_01')),
    ('Neck', 'Neck_Ctrl', ('Head', 'neck_01', 'head')),
    ('Head', 'Head_Ctrl', None)]
for s, S in (('Left', 'L'), ('Right', 'R')):
    l = S.lower()
    MAP += [('%sShoulder' % s, '%s_Clavicle_Ctrl' % S, ('%sArm' % s, 'clavicle_' + l, 'upperarm_' + l)),
            ('%sArm' % s, '%s_Shoulder_Fk_Ctrl' % S, ('%sForeArm' % s, 'upperarm_' + l, 'lowerarm_' + l)),
            ('%sForeArm' % s, '%s_Elbow_Fk_Ctrl' % S, ('%sHand' % s, 'lowerarm_' + l, 'hand_' + l)),
            ('%sHand' % s, '%s_Wrist_Fk_Ctrl' % S, ('%sHandMiddle1' % s, 'hand_' + l, 'middle_01_' + l)),
            ('%sUpLeg' % s, '%s_Hip_Fk_Ctrl' % S, ('%sLeg' % s, 'thigh_' + l, 'calf_' + l)),
            ('%sLeg' % s, '%s_Knee_Fk_Ctrl' % S, ('%sFoot' % s, 'calf_' + l, 'foot_' + l)),
            ('%sFoot' % s, '%s_Ankle_Fk_Ctrl' % S, ('%sToeBase' % s, 'foot_' + l, 'ball_' + l)),
            ('%sToeBase' % s, '%s_Foot_Toes_Ctrl' % S, None)]
CMU = {'Spine': 'LowerBack', 'Spine1': 'Spine', 'Spine2': None, 'Spine3': 'Spine1', 'LeftHandMiddle1': 'LeftFingerBase',
       'RightHandMiddle1': 'RightFingerBase'}
def src_name(hik, names):
    return names.get(hik, hik) if names else hik
SWITCHES = ['L_Hip_Jnt_Switch_Ctrl', 'R_Hip_Jnt_Switch_Ctrl', 'L_Shoulder_Jnt_Switch_Ctrl', 'R_Shoulder_Jnt_Switch_Ctrl']
def wpos(n): return om.MVector(c.xform(n, q=True, ws=True, t=True))
def body_ctrls(): return c.ls('*_Ctrl', type='transform')
def zero_rig():
    for n in body_ctrls():
        for a in ('tx', 'ty', 'tz', 'rx', 'ry', 'rz'):
            try: c.setAttr(n + '.' + a, 0)
            except Exception: pass
def align(j, child, rj, rchild):
    a = (wpos(child) - wpos(j)).normal(); b = (wpos(rchild) - wpos(rj)).normal()
    q = om.MQuaternion(a, b)
    M = om.MMatrix(c.xform(j, q=True, ws=True, m=True))
    p = wpos(j)
    T = om.MTransformationMatrix(); T.setTranslation(-p, om.MSpace.kWorld); Ti = om.MTransformationMatrix(); Ti.setTranslation(p, om.MSpace.kWorld)
    Mn = M * T.asMatrix() * q.asMatrix() * Ti.asMatrix()
    c.xform(j, ws=True, m=list(Mn))
def calibrate_and_bake(hips, ns, f0, f1, start, names=None, extra_hide=()):
    """Retarget a loaded source skeleton (namespace ns, root hips, keys f0..f1) onto the FK controls."""
    N = lambda h: (ns + src_name(h, names)) if src_name(h, names) else None
    for sw in SWITCHES: c.setAttr(sw + '.Switch_IK_FK', 1)
    c.currentTime(f0)
    zero_rig()
    grp = c.group(em=True, n=ns.rstrip(':').replace(':', '_') + '_retarget_space')
    c.parent(hips, grp)
    for j in c.ls(ns + '*', type='joint'):
        for ax in 'xyz':
            try: c.setAttr(j + '.r' + ax, 0)
            except Exception: pass
    src_leg = (wpos(N('LeftUpLeg')) - wpos(N('LeftLeg'))).length() + (wpos(N('LeftLeg')) - wpos(N('LeftFoot'))).length()
    rig_leg = (wpos('thigh_l') - wpos('calf_l')).length() + (wpos('calf_l') - wpos('foot_l')).length()
    sc = rig_leg / src_leg
    c.setAttr(grp + '.s', sc, sc, sc)
    d = wpos('pelvis') - wpos(hips)
    c.setAttr(grp + '.t', d.x, wpos('pelvis').y - wpos(hips).y, d.z)
    for src, ctrl, dd in MAP:
        if dd and N(src) and N(dd[0]) and c.objExists(N(src)) and c.objExists(N(dd[0])):
            align(N(src), N(dd[0]), dd[1], dd[2])
    cons = []
    for src, ctrl, dd in MAP:
        if not ctrl or not N(src) or not c.objExists(N(src)): continue
        cons += c.orientConstraint(N(src), ctrl, mo=True)
    cons += c.pointConstraint(hips, 'COG_Ctrl', mo=True)
    ctrls = [m[1] for m in MAP if m[1]]
    c.bakeResults(ctrls, t=(f0, f1), sm=True, at=['rx', 'ry', 'rz', 'tx', 'ty', 'tz'], disableImplicitControl=True,
                  preserveOutsideKeys=True, sparseAnimCurveBake=False, minimizeRotation=True)
    c.delete(cons)
    curves = c.listConnections(ctrls, s=True, d=False, type='animCurve') or []
    if curves: c.filterCurve(curves, filter='euler')
    c.setAttr(grp + '.v', 0)
    for n in extra_hide:
        if c.objExists(n) and c.attributeQuery('v', node=n, exists=True):
            try: c.setAttr(n + '.v', 0)
            except Exception: pass
    off = start - f0
    if off: c.keyframe(ctrls, e=True, r=True, tc=off, t=(f0, f1))
    return start, start + (f1 - f0), round(sc, 3)
def retarget(fbx, start, tag):
    """HumanIK FBX clip (Maya examples) -> rig"""
    import maya.mel as mel
    before = set(c.ls(assemblies=True))
    mel.eval('FBXImportSetTake -takeIndex 1')      # take 0 = 'No Animation' (an earlier FBXResetImport left it there)
    c.file(fbx, i=True, type='FBX', ignoreVersion=True, ra=True, options='fbx', mergeNamespacesOnClash=False)
    new = [n for n in c.ls(assemblies=True) if n not in before]
    hips = [j for j in c.ls(type='joint') if j.endswith(':Hips')]
    hips = [h for h in hips if any(h.startswith(n.split(':')[0] + ':') for n in new) or h in new][0]
    ns = hips[:-4]
    curves = c.ls(c.listConnections(c.ls(ns + '*', type='joint'), s=True, d=False, type='animCurve') or [])
    f0 = int(min(c.findKeyframe(a, which='first') for a in curves)); f1 = int(max(c.findKeyframe(a, which='last') for a in curves))
    return calibrate_and_bake(hips, ns, f0, f1, start, None, new)
def retarget_bvh(path, start, step=4):
    """CMU BVH (cgspeed conversion) -> rig"""
    try:
        from . import bvh_loader as gr_bvh
    except ImportError:
        import bvh_loader as gr_bvh
    root, f0, f1 = gr_bvh.load(path, ns='CMU', step=step, start=0)
    return calibrate_and_bake(c.ls(root)[0] if c.objExists(root) else root, 'CMU:', f0, f1, start, CMU)
