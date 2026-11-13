# MayaMCP pipeline helpers

Generic helpers written while an AI assistant rigged and tested a character with Mutant Tools (Unreal game
template body, Mutant face, Meta Mutant shapes). None of them is character-specific. They are experiments, not
production tools: read them before you use them on a show.

| Module | Runs in | What it does |
| --- | --- | --- |
| `hw_render.py` | mayapy | Headless viewport-style images (Hardware 2.0 batch render): shaded colour, smooth mesh preview, control curves, isolate, wire-on-shaded, x-ray. Pose stills are snapshotted, keyed on spare frames and rendered in one `Render` call per batch; sequences render the scene's own animation. No GUI or commandPort needed. |
| `hw_composite.py` | any Python + Pillow | Composites the RGBA renders over a viewport gradient. |
| `look_transfer.py` | Maya | Copies per-face material assignments, colours and a directional light rig from one version of an asset to older versions (match by mesh name and face count), e.g. to re-shoot early steps in colour. |
| `bvh_loader.py` | Maya | BVH (e.g. CMU mocap) to a keyed joint hierarchy, with the right rotate orders. |
| `world_retarget.py` | Maya | World-space retarget onto the Mutant Unreal game template FK controls (HumanIK-named FBX or CMU BVH): zero-pose calibration, bone-direction alignment, orient constraints with offset, bake, Euler filter. |
| `dynamic_chains.py` | Maya | Joint chains for cloth/skirts: build from a mesh, skin, and a baked Verlet simulation with capsule collision (rest-calibrated so the rest pose doesn't move). |
| `face_anim.py` | Maya | Mutant face expression library, keyed showcase, motion-driven face + finger animation for mocap clips, and ARKit/MediaPipe video weights to Mutant face controls. |
| `mouth_guard.py` | Maya | Keeps tusks, teeth, gums and tongue from cutting through the lips by solving the lip *tweak controls* (and a little of the teeth controls) per pose: finite-difference Jacobian at the neutral face, weighted ridge least squares with a line search, tests in the head's rest frame so it works under mocap. `solve()` for a pose, `bake(frames)` for an animation. No geometry edits: the fix is keys an animator can see. Pass your skin / teeth mesh names and tusk / gum materials. |
| `corrective_inversion.py` | Maya | Mesh ring/neighbour utilities, world points, and exact pre-skin corrective inversion (per-vertex 3x3 from probe evaluations). Set `MESH` / `BS` for your asset. |
| `preview_dump.py` + `soft_render.py` + `render_npz.py` | mayapy / Python | Quick software z-buffer previews of posed meshes when no viewport is available. |
| `make_gif.py` | Python + Pillow | Looping GIF from an image sequence folder. |
| `video_face_extract.py` | Python + MediaPipe | Video to per-frame ARKit blendshape weights and head rotation (MediaPipe Face Landmarker). |

Headless render example:

```python
import hw_render
R = hw_render.Renderer('/tmp/shots')
R.shot('front', eye=(0, 150, 400), aim=(0, 100, 0), w=800, h=1000, isolate=['geo_grp'])
R.seq('walk', range(1, 49, 2), eye=(250, 140, 300), aim=(0, 100, 0), w=480, h=640, isolate=['geo_grp'])
R.flush()
```
