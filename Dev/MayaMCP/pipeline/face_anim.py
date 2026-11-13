"""Face + finger animation on the Mutant face/hand controls (generic Mutant Tools naming):
expression library, keyed showcase, motion-driven face/fingers for mocap, ARKit (MediaPipe) video -> controls."""
import json, math, numpy as np, maya.cmds as c
def LR(fmt, v): return {fmt % 'L': v, fmt % 'R': v}
def corner(x, y, sides='LR'):
    out = {}
    for S in sides: out['%s_Mouth_Main_Ctrl.tx' % S] = x; out['%s_Mouth_Main_Ctrl.ty' % S] = y
    return out
B = '%s_Brow_Ctrl.ty'; BL = '%s_EyelidsUprBlink_Ctrl.ty'; SN = '%s_Mid_02_Mouth_Up_Ctrl.ty'; LD = '%s_Mid_02_Mouth_Dw_Ctrl.ty'
NO = '%s_Nostril_A_Ctrl.ty'; SQ = '%s_CheekBone_1_Main_Ctrl.ty'; JAW = 'Mouth_Jaw_Ctrl.rx'
BI = '%s_Brow_Driver0_Main_Ctrl.ty'; BO = '%s_Brow_Driver4_Main_Ctrl.ty'; BM = 'Mid_Brow_A_Ctrl.ty'   # inner / outer / middle brow
EXPR = {
    'neutral': {},
    'smile_L': {**corner(1, 1, 'L'), 'L_CheekBone_1_Main_Ctrl.ty': 0.3},
    'smile': {**corner(1, 1), **LR(SQ, 0.3)},
    'happy': {**corner(1, 1), **LR(SQ, 0.6), **LR(B, 0.35), **LR(BI, 0.3), **LR(BL, 0.2)},
    'laugh': {**corner(1, 1), JAW: 15, **LR(SQ, 0.45), **LR(B, 0.3)},
    'kiss': {**corner(-1, 0), **LR(LD, 0.15)},
    'kiss_shift': {**corner(-1, 0.3, 'L'), **corner(-0.6, -0.2, 'R')},
    'frown': {**corner(0.6, -1), **LR(B, -0.4)},
    'sad': {**corner(0.15, -1), **LR(BI, 1), **LR(BO, -0.6), BM: 0.6, **LR(B, 0.2), **LR(BL, 0.3)},
    'angry': {**corner(0.5, -0.4), **LR(B, -1), **LR(BI, -1), BM: -0.8, **LR(SN, 0.35), **LR(NO, 0.4), **LR(SQ, 0.4)},
    'roar': {JAW: 21, **corner(1, 0), **LR(SN, 0.5), **LR(NO, 0.5), **LR(B, -1)},
    'surprise': {**LR(B, 1), **LR(BI, 0.6), **LR(BO, 0.6), BM: 0.6, **LR(BL, -0.8), JAW: 12, **corner(-0.4, 0)},
    'browsUp': {**LR(B, 1), **LR(BI, 0.7), **LR(BO, 0.7), BM: 0.7},
    'disgust': {'L_Mid_02_Mouth_Up_Ctrl.ty': 0.5, 'L_Nostril_A_Ctrl.ty': 0.5, 'L_CheekBone_1_Main_Ctrl.ty': 0.5, **corner(0.3, -0.3, 'L'), 'L_Brow_Ctrl.ty': -0.6},
    'wink_L': {'L_EyelidsUprBlink_Ctrl.ty': 1, **corner(0.8, 0.8, 'L'), 'L_CheekBone_1_Main_Ctrl.ty': 0.5},
    'squint': {**LR(SQ, 0.5), **LR(BL, 0.45), **LR(B, -0.3)},
    'blink': LR(BL, 1),
    'effort': {**corner(-0.2, -0.3), **LR(B, -0.8), **LR(NO, 0.35), **LR(SQ, 0.35)},
    'snarl': {**LR(SN, 0.5), **LR(NO, 0.5), **LR(B, -0.9), **corner(0.6, 0), JAW: 6},
}
def face_plugs():
    s = set()
    for p in EXPR.values(): s |= set(p)
    return sorted(s) + ['L_Eye_Ctrl.tx', 'L_Eye_Ctrl.ty', 'R_Eye_Ctrl.tx', 'R_Eye_Ctrl.ty']
def key_pose(f, pose, plugs=None):
    for p in (plugs or face_plugs()):
        if c.objExists(p.split('.')[0]): c.setKeyframe(p, t=f, v=pose.get(p, 0.0), itt='spline', ott='spline')
def showcase(start, order=None, hold=18, blend=10):
    order = order or ['neutral', 'smile_L', 'happy', 'laugh', 'neutral', 'kiss', 'kiss_shift', 'frown', 'sad', 'neutral', 'angry', 'roar',
                      'surprise', 'disgust', 'wink_L', 'squint', 'blink', 'neutral']
    f = start
    for name in order:
        key_pose(f, EXPR[name]); key_pose(f + hold, EXPR[name]); f += hold + blend
    for t, (x, y) in ((start + 40, (2, 0)), (start + 70, (-2, 1)), (start + 100, (0, 0))):
        for S in 'LR': c.setKeyframe('%s_Eye_Ctrl.tx' % S, t=t, v=x); c.setKeyframe('%s_Eye_Ctrl.ty' % S, t=t, v=y)
    return start, f
def blinks(f0, f1, every=(70, 120), seed=3):
    rng = np.random.RandomState(seed); f = f0 + rng.randint(*every)
    while f < f1 - 6:
        for S in 'LR':
            p = BL % S
            for t, v in ((f - 2, None), (f, 1.0), (f + 3, None)):
                c.setKeyframe(p, t=t, v=(c.getAttr(p, t=t) if v is None else v))
        f += rng.randint(*every)
def motion_face(f0, f1, hands=('hand_l', 'hand_r'), feet=('foot_l', 'foot_r'), mood='effort', peak='snarl', thresh=0.55):
    """AI-driven face for a body clip: intensity from hand/foot speed; mood blends in with intensity, peaks get `peak`"""
    pos = {j: [] for j in hands + feet}
    for f in range(f0, f1 + 1):
        c.currentTime(f)
        for j in pos: pos[j].append(c.xform(j, q=True, ws=True, t=True))
    sp = np.zeros(f1 - f0 + 1)
    for j, p in pos.items():
        p = np.array(p); v = np.r_[0, np.linalg.norm(np.diff(p, axis=0), axis=1)]; sp += v
    k = np.ones(9) / 9; sp = np.convolve(sp, k, mode='same'); it = np.clip(sp / (np.percentile(sp, 95) + 1e-6), 0, 1)
    plugs = face_plugs()
    for i in range(0, len(it), 6):
        f = f0 + i; a = float(it[i]); name = peak if a > thresh else mood
        pose = {p: v * (a if name == mood else min(1, a * 1.2)) for p, v in EXPR[name].items()}
        key_pose(f, pose, plugs)
    blinks(f0, f1)
    return it
def finger_axes(side='L'):
    """curl axis/sign for each finger ctrl: the rotation that brings the finger's last joint toward the wrist"""
    s = side.lower(); out = {}
    for fing in ('Index', 'Middle', 'Ring', 'Pinky', 'Thumb'):
        segs = ['01', '02', '03'] if fing != 'Thumb' else ['01', '02']
        tip = '%s_03_%s' % (fing.lower(), s) if fing != 'Thumb' else 'thumb_03_%s' % s
        if not c.objExists(tip): continue
        for seg in segs:
            ctl = '%s_Hand_%s_%s_Ctrl' % (side, fing, seg)
            if not c.objExists(ctl): continue
            best = None
            for a in 'xyz':
                for sg in (1, -1):
                    p0 = np.array(c.xform(tip, q=True, ws=True, t=True)); c.setAttr('%s.r%s' % (ctl, a), sg * 30)
                    p1 = np.array(c.xform(tip, q=True, ws=True, t=True)); c.setAttr('%s.r%s' % (ctl, a), 0)
                    wr = np.array(c.xform('hand_' + s, q=True, ws=True, t=True))
                    sc = np.linalg.norm(p0 - wr) - np.linalg.norm(p1 - wr)
                    if best is None or sc > best[0]: best = (sc, a, sg)
            out[ctl] = (best[1], best[2])
    return out
def fingers(f0, f1, axes, curl_of_frame, step=3):
    """curl_of_frame(f) -> (curlL, curlR) in 0..1 (0 relaxed hand, 1 fist)"""
    for f in range(f0, f1 + 1, step):
        cl = curl_of_frame(f)
        for ctl, (a, sg) in axes.items():
            S = ctl[0]; amt = cl[0] if S == 'L' else cl[1]
            base = 12 if 'Thumb' not in ctl else 5
            c.setKeyframe('%s.r%s' % (ctl, a), t=f, v=sg * (base + amt * (75 if 'Thumb' not in ctl else 35)))
def video_to_controls(path, start, gain=1.3, smooth=2, head=True):
    """MediaPipe ARKit-style weights (video_face_extract.py json) -> Mutant face controls, keyed from start"""
    d = json.load(open(path)); fr = d['frames']
    names = sorted({k for f in fr if f['bs'] for k in f['bs']}); n = len(fr)
    A = np.full((n, len(names)), np.nan); Y = np.full((n, 3), np.nan)
    for i, f in enumerate(fr):
        if f['bs']: A[i] = [f['bs'][k] for k in names]; Y[i] = [f['yaw'], f['pitch'], f['roll']]
    for M in (A, Y):                                  # fill gaps, then smooth
        for j in range(M.shape[1]):
            col = M[:, j]; ok = ~np.isnan(col)
            if ok.any(): M[:, j] = np.interp(np.arange(n), np.where(ok)[0], col[ok])
        if smooth:
            k = np.exp(-0.5 * (np.arange(-3 * smooth, 3 * smooth + 1) / smooth) ** 2); k /= k.sum()
            for j in range(M.shape[1]): M[:, j] = np.convolve(np.pad(M[:, j], 3 * smooth, mode='edge'), k, mode='valid')
    I = {k: i for i, k in enumerate(names)}
    g = lambda i, k: float(A[i, I[k]]) * gain if k in I else 0.0
    keyed = 0
    for i in range(n):
        f = start + i; v = {}
        for S, side in (('L', 'Left'), ('R', 'Right')):
            wide = g(i, 'mouthStretch' + side) + 0.6 * g(i, 'mouthSmile' + side) + 0.3 * g(i, 'mouthDimple' + side)
            narrow = g(i, 'mouthPucker') + 0.6 * g(i, 'mouthFunnel')
            v['%s_Mouth_Main_Ctrl.tx' % S] = float(np.clip(wide - narrow, -1, 1))
            v['%s_Mouth_Main_Ctrl.ty' % S] = float(np.clip(g(i, 'mouthSmile' + side) - g(i, 'mouthFrown' + side), -1, 1))
            v[SN % S] = 0.5 * min(1, g(i, 'mouthUpperUp' + side)); v[LD % S] = -0.5 * min(1, g(i, 'mouthLowerDown' + side))
            v[NO % S] = 0.5 * min(1, g(i, 'noseSneer' + side)); v[SQ % S] = 0.5 * min(1, g(i, 'cheekSquint' + side))
            v[B % S] = float(np.clip(0.6 * g(i, 'browOuterUp' + side) + 0.6 * g(i, 'browInnerUp') - g(i, 'browDown' + side), -1, 1))
            v[BL % S] = float(np.clip(min(1, g(i, 'eyeBlink' + side) / gain) - 0.6 * g(i, 'eyeWide' + side), -1, 1))
            v['%s_Eye_Ctrl.tx' % S] = 2.5 * ((g(i, 'eyeLookOut' + side) - g(i, 'eyeLookIn' + side)) * (1 if S == 'L' else -1)) / gain
            v['%s_Eye_Ctrl.ty' % S] = 2.5 * (g(i, 'eyeLookUp' + side) - g(i, 'eyeLookDown' + side)) / gain
        v[JAW] = 23.6 * min(1, g(i, 'jawOpen'))
        if head:
            v['Head_Ctrl.ry'] = 0.8 * float(Y[i, 0]); v['Head_Ctrl.rx'] = -0.8 * float(Y[i, 1]); v['Head_Ctrl.rz'] = 0.8 * float(Y[i, 2])
        for p, val in v.items():
            if c.objExists(p.split('.')[0]): c.setKeyframe(p, t=f, v=val); keyed += 1
    return start, start + n - 1, keyed
