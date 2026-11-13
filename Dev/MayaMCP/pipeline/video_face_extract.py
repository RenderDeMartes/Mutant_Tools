"""Video -> per-frame ARKit-style face weights + head rotation with MediaPipe Face Landmarker (generic).
usage: python video_face_extract.py <video> <model.task> <out.json> [max_frames]"""
import sys, json, cv2, numpy as np, mediapipe as mp
from mediapipe.tasks import python as mpt
from mediapipe.tasks.python import vision
video, model, out = sys.argv[1], sys.argv[2], sys.argv[3]; maxf = int(sys.argv[4]) if len(sys.argv) > 4 else 10 ** 9
opts = vision.FaceLandmarkerOptions(base_options=mpt.BaseOptions(model_asset_path=model), running_mode=vision.RunningMode.VIDEO,
                                    output_face_blendshapes=True, output_facial_transformation_matrixes=True, num_faces=1,
                                    min_face_detection_confidence=0.3, min_face_presence_confidence=0.3, min_tracking_confidence=0.3)
cap = cv2.VideoCapture(video); fps = cap.get(cv2.CAP_PROP_FPS) or 24
frames = []; i = 0; found = 0
with vision.FaceLandmarker.create_from_options(opts) as lm:
    while i < maxf:
        ok, img = cap.read()
        if not ok: break
        big = cv2.resize(img, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)       # old 320x240 film: upscale helps detection
        res = lm.detect_for_video(mp.Image(image_format=mp.ImageFormat.SRGB, data=cv2.cvtColor(big, cv2.COLOR_BGR2RGB)), int(i * 1000 / fps))
        if res.face_blendshapes:
            bs = {b.category_name: round(float(b.score), 4) for b in res.face_blendshapes[0]}
            M = np.array(res.facial_transformation_matrixes[0])[:3, :3]
            yaw = float(np.degrees(np.arctan2(M[0, 2], M[2, 2]))); pitch = float(np.degrees(np.arcsin(-np.clip(M[1, 2], -1, 1)))); roll = float(np.degrees(np.arctan2(M[1, 0], M[1, 1])))
            frames.append({'f': i, 'bs': bs, 'yaw': round(yaw, 2), 'pitch': round(pitch, 2), 'roll': round(roll, 2)}); found += 1
        else:
            frames.append({'f': i, 'bs': None})
        if i in (60, 300, 600, 900): cv2.imwrite(out.replace('.json', '_frame%04d.png' % i), img)
        i += 1
json.dump({'fps': fps, 'frames': frames}, open(out, 'w'))
print('frames', i, 'with face', found, 'fps', fps)
