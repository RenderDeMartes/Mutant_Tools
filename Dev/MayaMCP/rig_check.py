"""Rig checks: pose it, measure, put it back.

Runs INSIDE Maya. Every check restores the values it changed and reports
whether the rig really came back to rest, so it is safe on a working scene.

    from Mutant_Tools.Dev.MayaMCP import rig_check as rc
    rc.pose_check({'L_Foot_Ik_Ctrl.ty': 15, 'L_Foot_Ik_Ctrl.tz': 10},
                  measure=['L_Knee_Skl', 'L_Ankle_Skl'])
    rc.pole_vector_report('L_Knee_IkPV_Ctrl', watch='L_Knee_Skl')
"""
import maya.cmds as mc

try:
    from . import fit_math as fm
except ImportError:
    import fit_math as fm


def _pos(node):
    return mc.xform(node, q=True, ws=True, t=True)


def _round(p, n=3):
    return [round(v, n) for v in p]


def pose_check(pose, measure, tol=1e-3):
    """Apply a pose, read world positions, restore it.

    pose: {'node.attr': value}; measure: nodes to read (joints, controls).
    Returns {'rest', 'posed', 'moved' (distance per node), 'restored'};
    restored False means some node did not come back within `tol`.
    """
    missing = [n for n in measure if not mc.objExists(n)] + \
              [p for p in pose if not mc.objExists(p)]
    if missing:
        raise ValueError('missing: {}'.format(', '.join(missing)))
    rest = {n: _pos(n) for n in measure}
    saved = {p: mc.getAttr(p) for p in pose}
    try:
        for p, v in pose.items():
            mc.setAttr(p, v)
        posed = {n: _pos(n) for n in measure}
    finally:
        for p, v in saved.items():
            mc.setAttr(p, v)
    back = {n: _pos(n) for n in measure}
    return {'rest': {n: _round(p) for n, p in rest.items()},
            'posed': {n: _round(p) for n, p in posed.items()},
            'moved': {n: round(fm._len(fm._sub(posed[n], rest[n])), 3) for n in measure},
            'restored': all(fm._len(fm._sub(back[n], rest[n])) <= tol for n in measure)}


def _upstream(node, depth=12):
    return set(mc.listHistory(node, levels=depth) or [])


def pole_vector_report(pv_ctrl, watch=None, attr='tz', drags=(-60, -30, 30, 60)):
    """Where a PV control really pulls, and whether dragging it flips the limb.

    Finds the poleVectorConstraints whose target follows `pv_ctrl` (rigs often
    drive a hidden pole locator kept at an offset from the control). With
    `watch` (the knee / elbow joint) the control is dragged along `attr` by
    each of `drags` and the joint position recorded, then restored.
    Returns {'poles': [{'constraint', 'target', 'target_pos', 'offset'}],
    'drags': {value: watch position}, 'restored'}.
    A large offset means the limb aims at a point the animator cannot see.
    """
    if not mc.objExists(pv_ctrl):
        raise ValueError('{} does not exist'.format(pv_ctrl))
    ctrl_pos = _pos(pv_ctrl)
    poles = []
    for pvc in mc.ls(type='poleVectorConstraint'):
        for target in mc.poleVectorConstraint(pvc, q=True, tl=True) or []:
            if target == pv_ctrl or pv_ctrl in _upstream(target):
                tp = _pos(target)
                poles.append({'constraint': pvc, 'target': target, 'target_pos': _round(tp),
                              'offset': round(fm._len(fm._sub(tp, ctrl_pos)), 3)})
    out = {'ctrl_pos': _round(ctrl_pos), 'poles': poles, 'drags': {}, 'restored': True}
    if watch:
        if not mc.objExists(watch):
            raise ValueError('{} does not exist'.format(watch))
        plug = '{}.{}'.format(pv_ctrl, attr)
        start, rest = mc.getAttr(plug), _pos(watch)
        try:
            for d in drags:
                mc.setAttr(plug, start + d)
                out['drags'][d] = _round(_pos(watch))
        finally:
            mc.setAttr(plug, start)
        out['rest'] = _round(rest)
        out['restored'] = fm._len(fm._sub(_pos(watch), rest)) < 1e-3
    return out
