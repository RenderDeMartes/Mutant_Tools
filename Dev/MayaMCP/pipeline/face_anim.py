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
    # narrow corners stop at 0.6: past that the lip corners sweep in front of the tusks (the rig limits them there)
    'kiss': {**corner(-0.6, 0), **LR(LD, 0.15)},
    'kiss_shift': {**corner(-0.6, 0.3, 'L'), **corner(-0.35, -0.2, 'R')},
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
FINGERS = ('Index', 'Middle', 'Ring', 'Pinky')
def hand_rig(side='L'):
    """measure the hand controls numerically (works whatever their orientation): per finger the curl axis/sign of each
    segment control and the spread axis/sign of the first one, the thumb's curl and opposition, the palm cup"""
    s = side.lower(); wr = lambda: np.array(c.xform('hand_' + s, q=True, ws=True, t=True))
    def tip(f): return '%s_03_%s' % (f.lower(), s)
    def pos(n): return np.array(c.xform(n, q=True, ws=True, t=True))
    def best_axis(ctl, score, axes='xyz'):
        best = None
        for a in axes:
            for sg in (1, -1):
                v = c.getAttr('%s.r%s' % (ctl, a)); c.setAttr('%s.r%s' % (ctl, a), v + sg * 20); sc = score()
                c.setAttr('%s.r%s' % (ctl, a), v)
                if best is None or sc > best[0]: best = (sc, a, sg)
        return best[1], best[2]
    R = dict(curl={}, spread={}, thumb={}, cup=None)
    lat = pos('index_01_' + s) - pos('pinky_01_' + s); lat /= np.linalg.norm(lat)
    for f in FINGERS + ('Thumb',):
        if not c.objExists(tip(f)): continue
        segs = ('01', '02', '03') if f != 'Thumb' else ('01', '02')
        for seg in segs:
            ctl = '%s_Hand_%s_%s_Ctrl' % (side, f, seg)
            if not c.objExists(ctl): continue
            p0 = pos(tip(f)); w = wr()
            R['curl'][ctl] = best_axis(ctl, lambda: np.linalg.norm(p0 - w) - np.linalg.norm(pos(tip(f)) - w))
        ctl = '%s_Hand_%s_01_Ctrl' % (side, f)
        if f != 'Thumb' and c.objExists(ctl):
            ca = R['curl'][ctl][0]; p0 = pos(tip(f)); away = 1.0 if f in ('Index',) else -1.0 if f in ('Ring', 'Pinky') else 0.0
            if away:
                R['spread'][ctl] = best_axis(ctl, lambda: away * ((pos(tip(f)) - p0) @ lat), axes=[a for a in 'xyz' if a != ca])
    th0 = '%s_Hand_Thumb_00_Ctrl' % side
    if c.objExists(th0) and c.objExists('pinky_01_' + s):
        R['thumb'][th0] = best_axis(th0, lambda: -np.linalg.norm(pos(tip('Thumb')) - pos('pinky_01_' + s)))
    cup = '%s_Hand_OutterCup_Ctrl' % side
    if c.objExists(cup):
        R['cup'] = (cup,) + best_axis(cup, lambda: -np.linalg.norm(pos(tip('Pinky')) - pos(tip('Thumb'))))
    return R

def hand_pose(R, curl, spread=0.0, thumb=None, cup=None, lag=None):
    """{plug: value} for one hand: curl 0 relaxed .. 1 fist (cascade: pinky curls most), spread -0.3..1, thumb
    opposition and palm cup default to follow the curl"""
    thumb = curl if thumb is None else thumb; cup = curl if cup is None else cup
    K = {'Index': 0.85, 'Middle': 0.95, 'Ring': 1.0, 'Pinky': 1.08}
    BASE = {'01': 8, '02': 12, '03': 8}; AMP = {'01': 68, '02': 95, '03': 60}
    out = {}
    for ctl, (a, sg) in R['curl'].items():
        f, seg = ctl.split('_')[2], ctl.split('_')[3]
        cf = curl[f] if isinstance(curl, dict) else curl
        if f == 'Thumb': v = (5 + cf * 32) if seg == '01' else (6 + cf * 48)
        else: v = BASE[seg] + min(1.0, cf * K[f]) * AMP[seg] + (4 if f == 'Pinky' else 0)
        out['%s.r%s' % (ctl, a)] = sg * v
    for ctl, (a, sg) in R['spread'].items():
        f = ctl.split('_')[2]; out['%s.r%s' % (ctl, a)] = sg * spread * {'Index': 9, 'Ring': 7, 'Pinky': 15}.get(f, 0)
    for ctl, (a, sg) in R['thumb'].items():
        out['%s.r%s' % (ctl, a)] = sg * 26 * thumb
    if R['cup']:
        ctl, a, sg = R['cup']; out['%s.r%s' % (ctl, a)] = sg * 16 * cup
    return out

def hands(f0, f1, style='relaxed', step=2, smooth=3):
    """AI-driven hand animation for a body clip with no finger data. Per hand and per frame, from the hand's own
    motion: speed (smoothed, normalised by the clip), height above the feet, reach (hand-to-shoulder / arm length).
    style picks how those become curl / spread:
      fighter    guard half-fist, full fist while the hand travels fast and far (punches)
      gorilla    knuckle fists near the ground, claw-spread hands otherwise
      strongman  tense half-fists, a little spread
      jumper     relaxed while running, open spread hands when the arms swing high
      relaxed    gentle curl with the motion
    Fingers lag by a frame or two from index to pinky so the hand reads as alive, not as one switch."""
    sides = [S for S in 'LR' if c.objExists('%s_Hand_Index_01_Ctrl' % S)]
    rigs = {S: hand_rig(S) for S in sides}
    frames = list(range(f0, f1 + 1)); n = len(frames)
    def sm(a, r):
        o = np.empty_like(a)
        for i in range(len(a)): o[i] = a[max(0, i - r):i + r + 1].mean(0)
        return o
    data = {}
    for S in sides:
        s = S.lower(); H, SH, FT = [], [], []
        for f in frames:
            c.currentTime(f)
            H.append(c.xform('hand_' + s, q=True, ws=True, t=True)); SH.append(c.xform('upperarm_' + s, q=True, ws=True, t=True))
            FT.append(min(c.xform('foot_l', q=True, ws=True, t=True)[1], c.xform('foot_r', q=True, ws=True, t=True)[1]))
        H, SH, FT = np.array(H), np.array(SH), np.array(FT)
        sp = np.r_[0, np.linalg.norm(np.diff(H, axis=0), axis=1)]; sp = sm(sp, 2); sp = np.clip(sp / (np.percentile(sp, 90) + 1e-6), 0, 1.5)
        arm = np.percentile(np.linalg.norm(H - SH, axis=1), 95) + 1e-6
        reach = np.clip(np.linalg.norm(H - SH, axis=1) / arm, 0, 1); up = H[:, 1] - SH[:, 1]; height = H[:, 1] - FT
        if style == 'fighter':
            curl = 0.62 + 0.38 * np.clip((sp - 0.45) / 0.45, 0, 1) * np.clip((reach - 0.6) / 0.3, 0, 1) + 0.15 * np.clip(sp, 0, 1)
            spread = np.zeros(n)
        elif style == 'gorilla':
            low = np.clip((45 - height) / 20, 0, 1)
            curl = 0.3 + 0.65 * low; spread = 0.7 * (1 - low)
        elif style == 'strongman':
            curl = 0.5 + 0.2 * np.clip(sp, 0, 1); spread = 0.25 * np.ones(n)
        elif style == 'jumper':
            high = np.clip((up + 5) / 25, 0, 1)
            curl = 0.38 - 0.3 * high; spread = 0.9 * high
        else:
            curl = 0.25 + 0.3 * np.clip(sp, 0, 1); spread = np.zeros(n)
        data[S] = (sm(np.clip(curl, 0, 1), smooth), sm(np.clip(spread, -0.3, 1), smooth))
    keyed = 0; lag = {'Index': 0, 'Middle': 1, 'Ring': 1, 'Pinky': 2, 'Thumb': 0}
    for i in range(0, n, step):
        f = frames[i]
        for S in sides:
            cu, spd = data[S]
            curl = {fg: float(cu[max(0, i - lag[fg])]) for fg in lag}
            for plug, v in hand_pose(rigs[S], curl, float(spd[i]), thumb=curl['Index'], cup=curl['Ring']).items():
                c.setKeyframe(plug, t=f, v=v); keyed += 1
    return dict(style=style, keys=keyed, curl_mean={S: round(float(data[S][0].mean()), 2) for S in sides})

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
