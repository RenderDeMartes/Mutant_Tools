"""
Run in Maya Script Editor to compare L vs R Soft IK node networks.
Checks: static attr values, connection structure, and full hierarchy
(parents + children) of key transform nodes — catches scale -1 mirror
groups that flip translate direction on one side.

Returns dict with value_diffs, connection_diffs, missing_nodes, hierarchy_diffs.
"""
from maya import cmds


_NODE_PAIRS = [
    ('L_SoftIK_CtrlDist_MD',         'R_SoftIK_CtrlDist_MD',         'multiplyDivide'),
    ('L_SoftIK_Threshold_PMA',        'R_SoftIK_Threshold_PMA',       'plusMinusAverage'),
    ('L_SoftIK_OverThresh_PMA',       'R_SoftIK_OverThresh_PMA',      'plusMinusAverage'),
    ('L_SoftIK_DivSoftp_MD',          'R_SoftIK_DivSoftp_MD',         'multiplyDivide'),
    ('L_SoftIK_Negate_MD',            'R_SoftIK_Negate_MD',           'multiplyDivide'),
    ('L_SoftIK_Exp_MD',               'R_SoftIK_Exp_MD',              'multiplyDivide'),
    ('L_SoftIK_SoftpExp_MD',          'R_SoftIK_SoftpExp_MD',         'multiplyDivide'),
    ('L_SoftIK_SoftDistCand_PMA',     'R_SoftIK_SoftDistCand_PMA',    'plusMinusAverage'),
    ('L_SoftIK_SoftpGate_COND',       'R_SoftIK_SoftpGate_COND',      'condition'),
    ('L_SoftIK_Main_COND',            'R_SoftIK_Main_COND',           'condition'),
    ('L_SoftIK_Delta_PMA',            'R_SoftIK_Delta_PMA',           'plusMinusAverage'),
    ('L_SoftIK_OneMinusStretch_PMA',  'R_SoftIK_OneMinusStretch_PMA', 'plusMinusAverage'),
    ('L_SoftIK_OneMinusPin_PMA',      'R_SoftIK_OneMinusPin_PMA',     'plusMinusAverage'),
    ('L_SoftIK_StretchWeight_MD',     'R_SoftIK_StretchWeight_MD',    'multiplyDivide'),
    ('L_SoftIK_PinWeight_MD',         'R_SoftIK_PinWeight_MD',        'multiplyDivide'),
    ('L_SoftIK_Sdif_COND',            'R_SoftIK_Sdif_COND',           'condition'),
    ('L_SoftIK_SdifDelta_PMA',        'R_SoftIK_SdifDelta_PMA',       'plusMinusAverage'),
    ('L_SoftIK_StretchAmt_MD',        'R_SoftIK_StretchAmt_MD',       'multiplyDivide'),
    ('L_SoftIK_StretchPinAmt_MD',     'R_SoftIK_StretchPinAmt_MD',    'multiplyDivide'),
    ('knee_plusMinusAverage',          'r_knee_plusMinusAverage',       'plusMinusAverage'),
    ('l_pv_upLeg_joint_distanceShape', 'r_pv_upLeg_joint_distanceShape', 'distanceDimension'),
]

_ATTRS_BY_TYPE = {
    'multiplyDivide':   ['operation', 'input1X', 'input1Y', 'input1Z', 'input2X', 'input2Y', 'input2Z'],
    'plusMinusAverage': ['operation', 'input1D[0]', 'input1D[1]', 'input1D[2]'],
    'condition':        ['operation', 'firstTerm', 'secondTerm',
                         'colorIfTrueR', 'colorIfTrueG', 'colorIfTrueB',
                         'colorIfFalseR', 'colorIfFalseG', 'colorIfFalseB'],
    'distanceDimension': ['distance'],
}

# Key transform nodes whose full parent + child hierarchy we inspect
_TRANSFORM_PAIRS = [
    ('L_Ankle_Ik_Auto_Grp',     'R_Ankle_Ik_Auto_Grp'),
    ('L_Ankle_Ik_Root_Grp',     'R_Ankle_Ik_Root_Grp'),
    ('L_Foot_Ankle_RFL_Grp',    'R_Foot_Ankle_RFL_Grp'),
    ('L_Ankle_Ik_IKrp',         'R_Ankle_Ik_IKrp'),
    ('L_Ankle_Dist_Loc',        'R_Ankle_Dist_Loc'),
    ('L_Pelvis_Dist_Loc',       'R_Pelvis_Dist_Loc'),
    ('L_Knee_Ik_Jnt',           'R_Knee_Ik_Jnt'),
]

_XFORM_ATTRS = ['tx', 'ty', 'tz', 'rx', 'ry', 'rz', 'sx', 'sy', 'sz']

# Tokens replaced with __SIDE__ for structural connection comparison
_L_TOKENS = ['L_SoftIK_', 'L_Ankle', 'L_Hip_Jnt', 'L_KneeMid', 'L_Pelvis',
              'l_pv_upLeg', 'knee_plusMinusAverage']
_R_TOKENS = ['R_SoftIK_', 'R_Ankle', 'R_Hip_Jnt', 'R_KneeMid', 'R_Pelvis',
              'r_pv_upLeg', 'r_knee_plusMinusAverage']


def _normalise_conn(s):
    if s is None:
        return None
    for lt, rt in zip(_L_TOKENS, _R_TOKENS):
        s = s.replace(lt, '__SIDE__').replace(rt, '__SIDE__')
    return s


def _vals_differ(a, b):
    if a is None and b is None:
        return False
    if type(a) != type(b):
        return True
    if isinstance(a, float):
        return abs(a - b) > 1e-6
    return a != b


def _get_ancestors(node, depth=6):
    """Walk up the DAG up to `depth` levels. Returns list of dicts."""
    result = []
    current = node
    for _ in range(depth):
        parents = cmds.listRelatives(current, parent=True, fullPath=False) or []
        if not parents:
            break
        p = parents[0]
        entry = {'node': p}
        if cmds.nodeType(p) == 'transform':
            for a in _XFORM_ATTRS:
                try:
                    entry[a] = cmds.getAttr('{}.{}'.format(p, a))
                except Exception:
                    pass
        result.append(entry)
        current = p
    return result


def _get_children(node, depth=3):
    """Walk down the DAG up to `depth` levels. Returns list of dicts."""
    result = []

    def _recurse(n, d):
        if d == 0:
            return
        kids = cmds.listRelatives(n, children=True, fullPath=False, type='transform') or []
        for k in kids:
            entry = {'node': k, 'parent': n}
            for a in _XFORM_ATTRS:
                try:
                    entry[a] = cmds.getAttr('{}.{}'.format(k, a))
                except Exception:
                    pass
            result.append(entry)
            _recurse(k, d - 1)

    _recurse(node, depth)
    return result


def _node_xform_snapshot(node):
    """Returns {attr: value} for transform + worldMatrix for a node."""
    snap = {}
    if not cmds.objExists(node):
        return snap
    for a in _XFORM_ATTRS:
        try:
            snap[a] = cmds.getAttr('{}.{}'.format(node, a))
        except Exception:
            pass
    try:
        snap['worldMatrix'] = cmds.getAttr('{}.worldMatrix[0]'.format(node))
    except Exception:
        pass
    return snap


def _compare_xform_snapshots(l_snap, r_snap):
    """Compare transform snapshots. For mirrored rigs, sx/sy/sz sign may differ — flag negative scale."""
    diffs = {}
    for attr in _XFORM_ATTRS:
        lv = l_snap.get(attr)
        rv = r_snap.get(attr)
        if lv is None and rv is None:
            continue
        # For scale: compare abs value (mirrored side has -1 vs 1)
        if attr.startswith('s'):
            if lv is not None and rv is not None and abs(abs(lv) - abs(rv)) > 1e-6:
                diffs[attr] = {'L': lv, 'R': rv, 'note': 'abs-magnitude differs'}
            elif lv is not None and rv is not None and (lv < 0 or rv < 0):
                diffs[attr] = {'L': lv, 'R': rv, 'note': 'NEGATIVE SCALE detected'}
        else:
            if _vals_differ(lv, rv):
                diffs[attr] = {'L': lv, 'R': rv}
    return diffs


def _check_hierarchy_pair(l_node, r_node):
    """
    For a pair of transform nodes, compare:
    - Their own xform values
    - All ancestors (parents/grandparents) up 6 levels
    - Direct children (3 levels)
    Returns dict describing any diffs or suspicious scale values.
    """
    result = {'self': {}, 'ancestors': [], 'children': []}

    if not cmds.objExists(l_node) or not cmds.objExists(r_node):
        result['missing'] = True
        return result

    # Self
    l_self = _node_xform_snapshot(l_node)
    r_self = _node_xform_snapshot(r_node)
    self_diffs = _compare_xform_snapshots(l_self, r_self)
    if self_diffs:
        result['self'] = self_diffs

    # Negative scale on self
    for side, snap in (('L', l_self), ('R', r_self)):
        for sa in ('sx', 'sy', 'sz'):
            v = snap.get(sa, 1.0)
            if v is not None and v < 0:
                result.setdefault('negative_scale_self', []).append(
                    '{}.{} = {}'.format(l_node if side == 'L' else r_node, sa, v))

    # Ancestors
    l_anc = _get_ancestors(l_node)
    r_anc = _get_ancestors(r_node)
    for i, (la, ra) in enumerate(zip(l_anc, r_anc)):
        anc_diffs = _compare_xform_snapshots(la, ra)
        # Flag any negative scale in ancestor chain
        for side, anc in (('L', la), ('R', ra)):
            for sa in ('sx', 'sy', 'sz'):
                v = anc.get(sa, 1.0)
                if v is not None and v < 0:
                    result.setdefault('negative_scale_ancestor', []).append(
                        '{} (level {}) .{} = {}'.format(anc['node'], i + 1, sa, v))
        if anc_diffs:
            result['ancestors'].append({
                'level': i + 1,
                'L_node': la['node'],
                'R_node': ra['node'],
                'diffs': anc_diffs,
            })

    # Children
    l_ch = _get_children(l_node)
    r_ch = _get_children(r_node)
    l_ch_map = {c['node']: c for c in l_ch}
    r_ch_map = {c['node']: c for c in r_ch}

    # Match by stripped side prefix
    def _strip_side(n):
        return n.replace('L_', '').replace('R_', '').replace('l_', '').replace('r_', '')

    l_stripped = {_strip_side(k): (k, v) for k, v in l_ch_map.items()}
    r_stripped = {_strip_side(k): (k, v) for k, v in r_ch_map.items()}

    for stripped_key in set(list(l_stripped.keys()) + list(r_stripped.keys())):
        l_pair = l_stripped.get(stripped_key)
        r_pair = r_stripped.get(stripped_key)
        if l_pair and r_pair:
            ch_diffs = _compare_xform_snapshots(l_pair[1], r_pair[1])
            for side, ch in (('L', l_pair[1]), ('R', r_pair[1])):
                for sa in ('sx', 'sy', 'sz'):
                    v = ch.get(sa, 1.0)
                    if v is not None and v < 0:
                        result.setdefault('negative_scale_children', []).append(
                            '{} .{} = {}'.format(ch['node'], sa, v))
            if ch_diffs:
                result['children'].append({
                    'L_node': l_pair[0],
                    'R_node': r_pair[0],
                    'diffs': ch_diffs,
                })

    return result


def compare_softik_sides():
    value_diffs    = {}
    conn_diffs     = {}
    missing        = []
    hierarchy_info = {}

    # ---- node attribute + connection comparison ----
    for l_node, r_node, ntype in _NODE_PAIRS:
        l_ok = cmds.objExists(l_node)
        r_ok = cmds.objExists(r_node)

        if not l_ok or not r_ok:
            missing.append({'L': l_node if not l_ok else 'EXISTS',
                            'R': r_node if not r_ok else 'EXISTS'})
            continue

        attrs = _ATTRS_BY_TYPE.get(ntype, [])
        vd = {}
        cd = {}

        for attr in attrs:
            l_full = '{}.{}'.format(l_node, attr)
            r_full = '{}.{}'.format(r_node, attr)

            try:
                lv = cmds.getAttr(l_full)
                rv = cmds.getAttr(r_full)
                lc = bool(cmds.listConnections(l_full, source=True, destination=False))
                rc = bool(cmds.listConnections(r_full, source=True, destination=False))
                if _vals_differ(lv, rv):
                    vd[attr] = {'L': lv, 'R': rv, 'L_connected': lc, 'R_connected': rc}
            except Exception:
                pass

            try:
                lc_p = cmds.listConnections(l_full, source=True, plugs=True)
                rc_p = cmds.listConnections(r_full, source=True, plugs=True)
                ls = lc_p[0] if lc_p else None
                rs = rc_p[0] if rc_p else None
                if _normalise_conn(ls) != _normalise_conn(rs):
                    cd[attr] = {'L_src': ls, 'R_src': rs}
            except Exception:
                pass

        if vd:
            value_diffs['{} | {} vs {}'.format(ntype, l_node, r_node)] = vd
        if cd:
            conn_diffs['{} | {} vs {}'.format(ntype, l_node, r_node)] = cd

    # ---- hierarchy comparison ----
    for l_node, r_node in _TRANSFORM_PAIRS:
        h = _check_hierarchy_pair(l_node, r_node)
        has_content = (h.get('self') or h.get('ancestors') or h.get('children')
                       or h.get('negative_scale_self') or h.get('negative_scale_ancestor')
                       or h.get('negative_scale_children') or h.get('missing'))
        if has_content:
            hierarchy_info['{} vs {}'.format(l_node, r_node)] = h

    # ---- print report ----
    sep = '=' * 65
    print('\n{}\n  SOFT IK SIDE COMPARISON\n{}'.format(sep, sep))

    if missing:
        print('\n[MISSING NODES]')
        for m in missing:
            print('  L: {}  |  R: {}'.format(m['L'], m['R']))

    print('\n[VALUE DIFFERENCES]')
    if value_diffs:
        for node_key, attrs_d in value_diffs.items():
            print('  {}'.format(node_key))
            for attr, vals in attrs_d.items():
                lc_tag = ' [connected]' if vals['L_connected'] else ''
                rc_tag = ' [connected]' if vals['R_connected'] else ''
                print('    .{}  L={}{} | R={}{}'.format(
                    attr, vals['L'], lc_tag, vals['R'], rc_tag))
    else:
        print('  None')

    print('\n[CONNECTION STRUCTURE DIFFERENCES]')
    if conn_diffs:
        for node_key, attrs_d in conn_diffs.items():
            print('  {}'.format(node_key))
            for attr, conns in attrs_d.items():
                print('    .{}  L <= {}  |  R <= {}'.format(
                    attr, conns['L_src'], conns['R_src']))
    else:
        print('  None')

    print('\n[HIERARCHY / TRANSFORM DIFFERENCES & NEGATIVE SCALE]')
    if hierarchy_info:
        for pair_key, info in hierarchy_info.items():
            print('\n  --- {} ---'.format(pair_key))
            if info.get('missing'):
                print('    One or both nodes missing.')
                continue
            for tag in ('negative_scale_self', 'negative_scale_ancestor', 'negative_scale_children'):
                for entry in info.get(tag, []):
                    print('    *** {} *** {}'.format(tag.upper(), entry))
            if info.get('self'):
                print('    [self xform diffs]')
                for attr, v in info['self'].items():
                    note = '  ({})'.format(v.get('note', '')) if isinstance(v, dict) and 'note' in v else ''
                    print('      .{}  L={} | R={}{}'.format(attr, v.get('L'), v.get('R'), note))
            for anc in info.get('ancestors', []):
                print('    [ancestor level {}]  L:{} | R:{}'.format(
                    anc['level'], anc['L_node'], anc['R_node']))
                for attr, v in anc['diffs'].items():
                    note = '  ({})'.format(v.get('note', '')) if isinstance(v, dict) and 'note' in v else ''
                    print('      .{}  L={} | R={}{}'.format(attr, v.get('L'), v.get('R'), note))
            for ch in info.get('children', []):
                print('    [child]  L:{} | R:{}'.format(ch['L_node'], ch['R_node']))
                for attr, v in ch['diffs'].items():
                    note = '  ({})'.format(v.get('note', '')) if isinstance(v, dict) and 'note' in v else ''
                    print('      .{}  L={} | R={}{}'.format(attr, v.get('L'), v.get('R'), note))
    else:
        print('  None')

    print('\n{}\n'.format(sep))

    return {
        'value_diffs':    value_diffs,
        'conn_diffs':     conn_diffs,
        'missing':        missing,
        'hierarchy_info': hierarchy_info,
    }


result = compare_softik_sides()
