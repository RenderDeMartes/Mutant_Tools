"""BVH loader for Maya (Maya has no BVH import). Builds the joint hierarchy and keys it with MFnAnimCurve.
BVH rotation channels are intrinsic in the listed order, so the Maya rotate order is the reversed list."""
import maya.cmds as c, maya.api.OpenMaya as om, maya.api.OpenMayaAnim as oma
def parse(path):
    toks = open(path).read().split()
    i = 0; joints = []; stack = []; chans = []
    def take():
        nonlocal i; t = toks[i]; i += 1; return t
    while True:
        t = take()
        if t in ('ROOT', 'JOINT'):
            name = take(); joints.append({'name': name, 'parent': stack[-1] if stack else None, 'offset': None, 'channels': []}); stack.append(len(joints) - 1)
        elif t == 'End':
            take(); joints.append({'name': joints[stack[-1]]['name'] + '_End', 'parent': stack[-1], 'offset': None, 'channels': [], 'end': True}); stack.append(len(joints) - 1)
        elif t == 'OFFSET':
            joints[stack[-1]]['offset'] = [float(take()) for _ in range(3)]
        elif t == 'CHANNELS':
            n = int(take()); joints[stack[-1]]['channels'] = [take() for _ in range(n)]
            for ch in joints[stack[-1]]['channels']: chans.append((stack[-1], ch))
        elif t == '}':
            stack.pop()
        elif t == 'MOTION':
            break
    take(); frames = int(take()); take(); take(); ft = float(take())
    vals = [float(x) for x in toks[i:i + frames * len(chans)]]
    return joints, chans, frames, ft, vals
def load(path, ns='BVH', scale=1.0, step=4, start=0):
    joints, chans, frames, ft, vals = parse(path)
    if not c.namespace(exists=ns): c.namespace(add=ns)
    made = []
    for j in joints:
        c.select(cl=True)
        n = c.joint(n='%s:%s' % (ns, j['name']))
        if j['parent'] is not None: c.parent(n, made[j['parent']])
        c.setAttr(n + '.t', *[v * scale for v in j['offset']])
        rot = [ch[0].lower() for ch in j['channels'] if ch.endswith('rotation')]
        if len(rot) == 3: c.setAttr(n + '.rotateOrder', ['xyz', 'yzx', 'zxy', 'xzy', 'yxz', 'zyx'].index(''.join(reversed(rot))))
        made.append(c.ls(n, l=True)[0])
    nch = len(chans); idx = list(range(0, frames, step))
    times = om.MTimeArray([om.MTime(start + k, om.MTime.uiUnit()) for k in range(len(idx))])
    for ci, (ji, ch) in enumerate(chans):
        node = made[ji]
        attr = {'Xposition': 'tx', 'Yposition': 'ty', 'Zposition': 'tz', 'Xrotation': 'rx', 'Yrotation': 'ry', 'Zrotation': 'rz'}[ch]
        s = scale if attr.startswith('t') else 1.0
        sel = om.MSelectionList(); sel.add(node + '.' + attr); plug = sel.getPlug(0)
        fn = oma.MFnAnimCurve(); fn.create(plug, oma.MFnAnimCurve.kAnimCurveTA if attr.startswith('r') else oma.MFnAnimCurve.kAnimCurveTL)
        data = [vals[f * nch + ci] * s for f in idx]
        if attr.startswith('r'): data = [om.MAngle(v, om.MAngle.kDegrees).asRadians() for v in data]
        fn.addKeys(times, data)
    c.currentTime(start)
    return made[0], start, start + len(idx) - 1
