/**
 * Imperative three.js scene driven by the app store. React only mounts the
 * canvas; everything else (geometry upload, picking, gizmo, painting) lives
 * here so large meshes are never diffed by React.
 */

import * as THREE from 'three';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js';
import { TransformControls } from 'three/examples/jsm/controls/TransformControls.js';
import { TriangleBVH, RayHit } from '../../engine/spatial/bvh';
import { evalSurfacePoint } from '../../engine/landmarks/landmarks';
import { computeBBox } from '../../engine/core/mesh';
import { AppState, baseCurrentPositions, baseEntry, baseRestPositions, get, MeshEntry, pushUndo, refEntry, set, useStore } from '../../state/store';
import { beginGuideDrag, beginStroke, dragGuide, effectiveComponentModes, endGuideDrag, endStroke, meshComponents, pickLandmarkPoint, strokeAt } from '../../state/actions';
import { sculptBegin, sculptDab, sculptDrag, sculptEnd } from '../../state/sculpt';
import { heatColor, pairColor } from '../theme';

interface MeshObj {
  entry: MeshEntry;
  geom: THREE.BufferGeometry;
  mesh: THREE.Mesh;
  lines: THREE.LineSegments;
  bvh: TriangleBVH | null;
  bvhSource: Float64Array | null;
  positionsSource: Float64Array | null;
}

interface PickHit {
  side: 'base' | 'ref';
  hit: RayHit;
  point: THREE.Vector3;
  positions: Float64Array;
  tris: Uint32Array;
}

const BASE_COLOR = new THREE.Color('#c8c3ba');
const MASK_COLOR = new THREE.Color('#ff7a2f');
const REF_COLOR = new THREE.Color('#3fa7a9');
const GHOST_COLOR = new THREE.Color('#9b7bff');
const FOLLOW_COLOR = new THREE.Color('#7fa6d9');
const FIXED_COLOR = new THREE.Color('#6d7178');

export class SceneController {
  private renderer: THREE.WebGLRenderer;
  private scene = new THREE.Scene();
  private camera: THREE.PerspectiveCamera;
  private controls: OrbitControls;
  private gizmo: TransformControls;
  private pivot = new THREE.Object3D();
  private grid: THREE.GridHelper | null = null;
  private base: MeshObj | null = null;
  private ref: MeshObj | null = null;
  private others = new Map<string, MeshObj>();
  private ghost: THREE.LineSegments | null = null;
  private markers = new THREE.Group();
  private brush: THREE.Mesh;
  private needsRender = true;
  private raf = 0;
  private unsub: () => void;
  private prev: AppState | null = null;
  private resizeObs: ResizeObserver;
  private down: { x: number; y: number; button: number } | null = null;
  private painting = false;
  private lastDab: THREE.Vector3 | null = null;
  /** placed guide dots, for grabbing them; the side of the one being dragged */
  dots: { id: number; side: 'base' | 'ref'; pos: THREE.Vector3 }[] = [];
  private dragging: 'base' | 'ref' | null = null;
  /** Brush stroke in progress; for Move, the view plane the grabbed point slides on */
  private sculpting: { plane: THREE.Plane | null } | null = null;
  private gizmoDragging = false;
  private gizmoStart: { T0: THREE.Matrix4; P0inv: THREE.Matrix4 } | null = null;
  private sphereGeom = new THREE.SphereGeometry(1, 16, 12);
  private labelCache = new Map<string, THREE.Texture>();
  /** Base display transform while placing guides side by side (uniform scale k, offset o). */
  private side: { k: number; o: [number, number, number] } | null = null;

  constructor(private container: HTMLElement) {
    this.renderer = new THREE.WebGLRenderer({ antialias: true, alpha: false, preserveDrawingBuffer: true });
    this.renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    this.renderer.setClearColor('#16181b');
    container.appendChild(this.renderer.domElement);
    this.camera = new THREE.PerspectiveCamera(35, 1, 0.01, 1000);
    this.camera.position.set(2.5, 1.5, 4);
    this.scene.add(this.camera);
    const head = new THREE.DirectionalLight(0xffffff, 1.6);
    head.position.set(0.4, 0.6, 1);
    this.camera.add(head);
    this.scene.add(new THREE.HemisphereLight(0xe6ecff, 0x2a2622, 0.9));
    this.controls = new OrbitControls(this.camera, this.renderer.domElement);
    this.controls.enableDamping = false;
    this.controls.addEventListener('change', () => this.invalidate());
    this.gizmo = new TransformControls(this.camera, this.renderer.domElement);
    this.gizmo.setSize(0.8);
    this.scene.add(this.pivot);
    this.scene.add(this.gizmo.getHelper());
    this.gizmo.addEventListener('dragging-changed', (e) => {
      this.controls.enabled = !(e as unknown as { value: boolean }).value;
    });
    this.gizmo.addEventListener('mouseDown', () => this.onGizmoStart());
    this.gizmo.addEventListener('objectChange', () => this.onGizmoChange());
    this.gizmo.addEventListener('mouseUp', () => {
      this.gizmoDragging = false;
      this.gizmoStart = null;
    });
    this.gizmo.addEventListener('change', () => this.invalidate());
    this.scene.add(this.markers);
    this.brush = new THREE.Mesh(
      new THREE.RingGeometry(0.92, 1, 48),
      new THREE.MeshBasicMaterial({ color: '#ffb36b', side: THREE.DoubleSide, depthTest: false, transparent: true, opacity: 0.9 }),
    );
    this.brush.renderOrder = 10;
    this.brush.visible = false;
    this.scene.add(this.brush);

    const el = this.renderer.domElement;
    if (import.meta.env.DEV) (window as unknown as { __viewport: SceneController }).__viewport = this; // tests only
    // capture: runs before the orbit controls, so grabbing a dot does not also turn the view
    el.addEventListener('pointerdown', this.onPointerDown, { capture: true });
    el.addEventListener('pointermove', this.onPointerMove);
    el.addEventListener('pointerup', this.onPointerUp);
    el.addEventListener('pointerleave', () => {
      this.brush.visible = false;
      this.invalidate();
    });
    el.addEventListener('contextmenu', (e) => e.preventDefault());

    this.resizeObs = new ResizeObserver(() => this.resize());
    this.resizeObs.observe(container);
    this.resize();
    this.unsub = useStore.subscribe((s) => this.sync(s));
    this.sync(get());
    const loop = () => {
      this.raf = requestAnimationFrame(loop);
      if (this.needsRender) {
        this.needsRender = false;
        this.renderer.render(this.scene, this.camera);
      }
    };
    loop();
  }

  dispose() {
    cancelAnimationFrame(this.raf);
    this.unsub();
    this.resizeObs.disconnect();
    this.gizmo.dispose();
    this.controls.dispose();
    this.renderer.dispose();
    this.renderer.domElement.remove();
  }

  invalidate() {
    this.needsRender = true;
  }

  private resize() {
    const w = this.container.clientWidth, h = this.container.clientHeight;
    if (!w || !h) return;
    this.renderer.setSize(w, h);
    this.camera.aspect = w / h;
    this.camera.updateProjectionMatrix();
    this.invalidate();
  }

  // ------------------------------------------------------------ store sync

  private sync(s: AppState) {
    const p = this.prev;
    const b = baseEntry(s), r = refEntry(s);
    const meshesChanged = !p || p.meshes !== s.meshes;
    if (meshesChanged) this.syncMeshes(s);
    const basePos = baseCurrentPositions(s);
    if (this.base && basePos && this.base.positionsSource !== basePos) this.uploadPositions(this.base, basePos);
    if (
      meshesChanged ||
      !p ||
      p.heat !== s.heat ||
      p.mask !== s.mask ||
      p.maskVersion !== s.maskVersion ||
      p.componentModes !== s.componentModes ||
      p.display.showMask !== s.display.showMask
    ) {
      this.updateBaseColors(s);
    }
    if (meshesChanged || !p || p.display !== s.display) this.updateMaterials(s);
    // ghost of the aligned original
    const showGhost = s.display.showOriginal && !!b && (!!s.committed || !!s.preview);
    if (showGhost) {
      const rest = baseRestPositions(s)!;
      if (!this.ghost || (this.ghost.userData.source !== rest) || this.ghost.userData.entry !== b) this.buildGhost(b!, rest);
      this.ghost!.visible = true;
    } else if (this.ghost) this.ghost.visible = false;
    const wasSide = !!this.side;
    if (meshesChanged || !p || p.tool !== s.tool || p.transform !== s.transform || p.committed !== s.committed || p.preview !== s.preview || p.display !== s.display) {
      this.layoutSideBySide(s);
    }
    const sideChanged = wasSide !== !!this.side;
    if (
      sideChanged ||
      meshesChanged ||
      !p ||
      p.landmarks !== s.landmarks ||
      p.selectedLandmarkId !== s.selectedLandmarkId ||
      p.pendingPick !== s.pendingPick ||
      p.hiddenGroups !== s.hiddenGroups ||
      p.showLandmarks !== s.showLandmarks ||
      p.guideSize !== s.guideSize ||
      baseCurrentPositions(p) !== basePos
    ) {
      this.updateMarkers(s);
    }
    if (sideChanged) this.frame(!!this.side);  // guides: face the front of both meshes
    if (!p || p.tool !== s.tool) this.updateTool(s);
    if (sideChanged || meshesChanged || !p || p.display.gizmo !== s.display.gizmo || p.transform !== s.transform || p.committed !== s.committed || p.preview !== s.preview) {
      this.updateGizmo(s);
    }
    if (!p || p.frameRequest !== s.frameRequest) this.frame();
    void r;
    this.prev = s;
    this.invalidate();
  }

  /**
   * Placing guides before any wrap: the Base is shown to the left of the Reference, at the same
   * size, so a point can be clicked on each. Display only (scale k, offset o); picks map back.
   */
  private layoutSideBySide(s: AppState) {
    const b = baseEntry(s), r = refEntry(s);
    const basePos = baseCurrentPositions(s);
    const on = s.tool === 'landmark' && !s.committed && !s.preview && !!b && !!r && !!basePos && s.display.showBase && s.display.showReference;
    if (on) {
      const bb = computeBBox(basePos!), rb = computeBBox(r!.loaded.mesh.positions);
      const k = rb.diagonal / Math.max(bb.diagonal, 1e-12);
      const gap = 0.15 * rb.diagonal;
      const target = [rb.center[0] - (rb.size[0] / 2 + gap + (bb.size[0] * k) / 2), rb.center[1], rb.center[2]];
      this.side = { k, o: [target[0] - k * bb.center[0], target[1] - k * bb.center[1], target[2] - k * bb.center[2]] };
    } else {
      this.side = null;
    }
    for (const obj of [this.base?.mesh, this.base?.lines]) {
      if (!obj) continue;
      obj.position.set(...(this.side ? this.side.o : ([0, 0, 0] as [number, number, number])));
      obj.scale.setScalar(this.side ? this.side.k : 1);
    }
  }

  /** A Base point as displayed (side by side or in place). */
  private shownBase(p: [number, number, number]): [number, number, number] {
    if (!this.side) return p;
    const { k, o } = this.side;
    return [p[0] * k + o[0], p[1] * k + o[1], p[2] * k + o[2]];
  }

  private makeMeshObj(entry: MeshEntry, positions: Float64Array, color: THREE.Color, isBase: boolean): MeshObj {
    const geom = new THREE.BufferGeometry();
    const n = positions.length / 3;
    geom.setAttribute('position', new THREE.BufferAttribute(new Float32Array(positions), 3));
    geom.setAttribute('normal', new THREE.BufferAttribute(new Float32Array(n * 3), 3));
    const colors = new Float32Array(n * 3);
    for (let i = 0; i < n; i++) color.toArray(colors, i * 3);
    geom.setAttribute('color', new THREE.BufferAttribute(colors, 3));
    geom.setIndex(new THREE.BufferAttribute(entry.triangles, 1));
    geom.computeVertexNormals();
    geom.computeBoundingSphere();
    const mat = new THREE.MeshStandardMaterial({
      vertexColors: true,
      side: THREE.DoubleSide,
      roughness: 0.78,
      metalness: 0,
      polygonOffset: true,
      polygonOffsetFactor: 1,
      polygonOffsetUnits: 1,
    });
    const mesh = new THREE.Mesh(geom, mat);
    const lgeom = new THREE.BufferGeometry();
    lgeom.setAttribute('position', geom.getAttribute('position'));
    lgeom.setIndex(new THREE.BufferAttribute(entry.polyEdges, 1));
    const lines = new THREE.LineSegments(lgeom, new THREE.LineBasicMaterial({ color: '#1b1d20', transparent: true, opacity: 0.6 }));
    mesh.renderOrder = isBase ? 1 : 2;
    this.scene.add(mesh);
    this.scene.add(lines);
    return { entry, geom, mesh, lines, bvh: null, bvhSource: null, positionsSource: positions };
  }

  private disposeObj(o: MeshObj) {
    this.scene.remove(o.mesh);
    this.scene.remove(o.lines);
    o.geom.dispose();
    o.lines.geometry.dispose();
    (o.mesh.material as THREE.Material).dispose();
    (o.lines.material as THREE.Material).dispose();
  }

  private syncMeshes(s: AppState) {
    const b = baseEntry(s), r = refEntry(s);
    if (this.base && (!b || this.base.entry.loaded !== b.loaded)) {
      this.disposeObj(this.base);
      this.base = null;
    }
    if (this.ref && (!r || this.ref.entry.loaded !== r.loaded)) {
      this.disposeObj(this.ref);
      this.ref = null;
    }
    if (b && !this.base) this.base = this.makeMeshObj(b, baseCurrentPositions(s)!, BASE_COLOR, true);
    if (r && !this.ref) this.ref = this.makeMeshObj(r, r.loaded.mesh.positions, REF_COLOR, false);
    if (this.base && b) this.base.entry = b;
    if (this.ref && r) this.ref.entry = r;
    // unassigned meshes are shown in grey
    const keep = new Set<string>();
    for (const m of s.meshes) {
      if (m.role) continue;
      keep.add(m.id);
      const o = this.others.get(m.id);
      if (!o) this.others.set(m.id, this.makeMeshObj(m, m.loaded.mesh.positions, new THREE.Color('#6b6f76'), false));
      else o.entry = m;
    }
    for (const [id, o] of this.others) {
      if (!keep.has(id)) {
        this.disposeObj(o);
        this.others.delete(id);
      }
    }
    if (this.ghost && (!b || this.ghost.userData.entry !== b)) {
      this.scene.remove(this.ghost);
      this.ghost.geometry.dispose();
      this.ghost = null;
    }
  }

  private uploadPositions(o: MeshObj, positions: Float64Array) {
    const attr = o.geom.getAttribute('position') as THREE.BufferAttribute;
    (attr.array as Float32Array).set(positions);
    attr.needsUpdate = true;
    o.geom.computeVertexNormals();
    o.geom.computeBoundingSphere();
    o.positionsSource = positions;
  }

  private buildGhost(b: MeshEntry, rest: Float64Array) {
    if (this.ghost) {
      this.scene.remove(this.ghost);
      this.ghost.geometry.dispose();
    }
    const g = new THREE.BufferGeometry();
    g.setAttribute('position', new THREE.BufferAttribute(new Float32Array(rest), 3));
    g.setIndex(new THREE.BufferAttribute(b.polyEdges, 1));
    this.ghost = new THREE.LineSegments(g, new THREE.LineBasicMaterial({ color: GHOST_COLOR, transparent: true, opacity: 0.35, depthWrite: false }));
    this.ghost.userData = { source: rest, entry: b };
    this.ghost.renderOrder = 3;
    this.scene.add(this.ghost);
  }

  private updateBaseColors(s: AppState) {
    if (!this.base) return;
    const attr = this.base.geom.getAttribute('color') as THREE.BufferAttribute;
    const c = attr.array as Float32Array;
    const n = c.length / 3;
    const tmp = new THREE.Color();
    if (s.heat && s.heat.values.length === n) {
      for (let i = 0; i < n; i++) {
        const v = s.heat.values[i];
        heatColor(Number.isFinite(v) ? v / s.heat.max : 0, tmp);
        tmp.toArray(c, i * 3);
      }
    } else {
      const mask = s.display.showMask && s.mask && s.mask.length === n ? s.mask : null;
      const b = baseEntry(s);
      const info = b ? meshComponents(b) : null;
      const modes = info && info.sizes.length > 1 ? effectiveComponentModes() : null;
      for (let i = 0; i < n; i++) {
        tmp.copy(BASE_COLOR);
        if (modes && info) {
          const m = modes[info.labels[i]];
          if (m === 'follow') tmp.copy(FOLLOW_COLOR);
          else if (m === 'fixed') tmp.copy(FIXED_COLOR);
        }
        if (mask && mask[i] > 0) tmp.lerp(MASK_COLOR, Math.min(1, mask[i]) * 0.85);
        tmp.toArray(c, i * 3);
      }
    }
    attr.needsUpdate = true;
  }

  private updateMaterials(s: AppState) {
    const d = s.display;
    const apply = (o: MeshObj | null, visible: boolean, opacity: number, wireColor: string) => {
      if (!o) return;
      const mat = o.mesh.material as THREE.MeshStandardMaterial;
      const lmat = o.lines.material as THREE.LineBasicMaterial;
      const shaded = d.mode !== 'wire';
      const wire = d.mode !== 'shaded';
      o.mesh.visible = visible && shaded;
      o.lines.visible = visible && wire;
      mat.transparent = opacity < 0.999;
      mat.opacity = opacity;
      mat.depthWrite = opacity >= 0.999;
      mat.needsUpdate = true;
      lmat.color.set(d.mode === 'wire' ? wireColor : '#1b1d20');
      lmat.opacity = d.mode === 'wire' ? 0.9 : 0.55 * Math.max(opacity, 0.4);
    };
    apply(this.base, d.showBase && (this.base?.entry.visible ?? false), 1, '#d9d4cb');
    apply(this.ref, d.showReference && (this.ref?.entry.visible ?? false), d.refOpacity, '#55c4c6');
    for (const o of this.others.values()) apply(o, o.entry.visible, 0.5, '#8a8f96');
  }

  private updateMarkers(s: AppState) {
    this.markers.clear();
    const b = baseEntry(s), r = refEntry(s);
    if (!s.showLandmarks || (!b && !r)) return;
    const basePos = baseCurrentPositions(s);
    const diag = Math.max(1e-9, computeBBox(r ? r.loaded.mesh.positions : basePos!).diagonal);
    const rad = diag * 0.0022 * s.guideSize;
    this.dots = [];
    const linePts: number[] = [];
    const lineCols: number[] = [];
    // many guides (a named set): only the point being asked for and the selected one get a label
    const busy = s.landmarks.length > 12;
    for (const l of s.landmarks) {
      if (s.hiddenGroups.includes(l.group)) continue;
      const color = new THREE.Color(pairColor(l.id));
      const selected = l.id === s.selectedLandmarkId;
      const asked = s.pendingPick?.landmarkId === l.id;
      const pts: THREE.Vector3[] = [];
      const addMarker = (p: [number, number, number], side: 'b' | 'r') => {
        const m = new THREE.Mesh(
          this.sphereGeom,
          new THREE.MeshBasicMaterial({ color: selected && !asked ? '#ffffff' : color, depthTest: true }),
        );
        m.position.set(p[0], p[1], p[2]);
        m.scale.setScalar(asked ? rad * 2.2 : selected ? rad * 1.5 : busy ? rad * 0.8 : rad);
        m.renderOrder = 5;
        this.markers.add(m);
        this.dots.push({ id: l.id, side: side === 'b' ? 'base' : 'ref', pos: m.position });
        if (!busy || asked || selected) {
          const sprite = new THREE.Sprite(new THREE.SpriteMaterial({ map: this.label(`${l.id}${side === 'b' ? '' : "'"}`, color), depthTest: false, sizeAttenuation: false }));
          sprite.position.copy(m.position);
          sprite.center.set(-0.15, -0.15);
          sprite.scale.set(0.045, 0.0225, 1);
          sprite.renderOrder = 6;
          this.markers.add(sprite);
        }
        pts.push(m.position.clone());
      };
      if (l.base && b && basePos) addMarker(this.shownBase(evalSurfacePoint(basePos, b.triangles, l.base)), 'b');
      if (l.ref && r) addMarker(evalSurfacePoint(r.loaded.mesh.positions, r.triangles, l.ref), 'r');
      if (pts.length === 2 && (!busy || asked || selected)) {
        linePts.push(pts[0].x, pts[0].y, pts[0].z, pts[1].x, pts[1].y, pts[1].z);
        lineCols.push(color.r, color.g, color.b, color.r, color.g, color.b);
      }
    }
    if (linePts.length) {
      const g = new THREE.BufferGeometry();
      g.setAttribute('position', new THREE.Float32BufferAttribute(linePts, 3));
      g.setAttribute('color', new THREE.Float32BufferAttribute(lineCols, 3));
      const lines = new THREE.LineSegments(g, new THREE.LineBasicMaterial({ vertexColors: true, transparent: true, opacity: 0.7, depthTest: false }));
      lines.renderOrder = 4;
      this.markers.add(lines);
    }
  }

  private label(text: string, color: THREE.Color): THREE.Texture {
    const key = `${text}|${color.getHexString()}`;
    let t = this.labelCache.get(key);
    if (t) return t;
    const c = document.createElement('canvas');
    c.width = 128;
    c.height = 64;
    const ctx = c.getContext('2d')!;
    ctx.font = '600 40px Inter, system-ui, sans-serif';
    ctx.textBaseline = 'middle';
    const w = ctx.measureText(text).width + 20;
    ctx.fillStyle = 'rgba(14,15,17,0.82)';
    ctx.beginPath();
    ctx.roundRect(0, 6, Math.min(128, w), 52, 10);
    ctx.fill();
    ctx.fillStyle = `#${color.getHexString()}`;
    ctx.fillText(text, 10, 33);
    t = new THREE.CanvasTexture(c);
    t.colorSpace = THREE.SRGBColorSpace;
    this.labelCache.set(key, t);
    return t;
  }

  private updateTool(s: AppState) {
    const M = THREE.MOUSE;
    if (s.tool === 'paint' || s.tool === 'sculpt') {
      this.controls.mouseButtons = { LEFT: null, MIDDLE: M.PAN, RIGHT: M.ROTATE };
    } else {
      this.controls.mouseButtons = { LEFT: M.ROTATE, MIDDLE: M.DOLLY, RIGHT: M.PAN };
      this.brush.visible = false;
    }
    this.renderer.domElement.style.cursor = s.tool === 'landmark' ? 'crosshair' : s.tool === 'paint' || s.tool === 'sculpt' ? 'none' : 'default';
  }

  // ------------------------------------------------------------ gizmo

  private updateGizmo(s: AppState) {
    const b = baseEntry(s);
    const locked = !!s.committed || !!s.preview;
    if (!b || s.display.gizmo === 'off' || locked || this.side) {
      this.gizmo.detach();
      return;
    }
    this.gizmo.setMode(s.display.gizmo);
    if (!this.gizmoDragging) {
      const rest = baseRestPositions(s)!;
      const c = computeBBox(rest).center;
      this.pivot.position.set(c[0], c[1], c[2]);
      this.pivot.quaternion.identity();
      this.pivot.scale.set(1, 1, 1);
      this.pivot.updateMatrix();
      this.pivot.updateMatrixWorld();
    }
    if (this.gizmo.object !== this.pivot) this.gizmo.attach(this.pivot);
  }

  private onGizmoStart() {
    this.gizmoDragging = true;
    pushUndo('Gizmo transform');
    this.pivot.updateMatrixWorld();
    this.gizmoStart = {
      T0: new THREE.Matrix4().fromArray(get().transform),
      P0inv: this.pivot.matrixWorld.clone().invert(),
    };
  }

  private onGizmoChange() {
    if (!this.gizmoStart) return;
    if (this.gizmo.mode === 'scale') {
      // uniform scale only (alignment is a similarity transform)
      const sc = this.pivot.scale;
      const dev = [sc.x, sc.y, sc.z].map((v) => Math.abs(v - 1));
      const k = dev.indexOf(Math.max(...dev));
      const v = Math.max(1e-4, [sc.x, sc.y, sc.z][k]);
      sc.set(v, v, v);
    }
    this.pivot.updateMatrixWorld();
    const delta = this.pivot.matrixWorld.clone().multiply(this.gizmoStart.P0inv);
    const T = delta.multiply(this.gizmoStart.T0);
    set({ transform: Float64Array.from(T.elements), heat: null });
  }

  // ------------------------------------------------------------ camera

  frame(front = false) {
    const s = get();
    const boxes: number[] = [];
    const add = (pos: Float64Array | null | undefined) => {
      if (!pos || !pos.length) return;
      const bb = computeBBox(pos);
      boxes.push(...bb.min, ...bb.max);
    };
    const b = baseEntry(s), r = refEntry(s);
    const basePos = b && b.visible ? baseCurrentPositions(s) : null;
    if (basePos && this.side) {
      const bb = computeBBox(basePos);
      boxes.push(...this.shownBase(bb.min as [number, number, number]), ...this.shownBase(bb.max as [number, number, number]));
    } else add(basePos);
    if (r && r.visible) add(r.loaded.mesh.positions);
    for (const m of s.meshes) if (!m.role && m.visible) add(m.loaded.mesh.positions);
    if (!boxes.length) return;
    const bb = computeBBox(boxes);
    const center = new THREE.Vector3(...bb.center);
    const radius = Math.max(1e-6, bb.diagonal / 2);
    const dir = front ? new THREE.Vector3(0, 0, 1) : this.camera.position.clone().sub(this.controls.target).normalize();
    if (!Number.isFinite(dir.x) || dir.lengthSq() === 0) dir.set(0.5, 0.3, 1).normalize();
    const dist = radius / Math.sin(THREE.MathUtils.degToRad(this.camera.fov / 2)) * 1.08;
    this.controls.target.copy(center);
    this.camera.position.copy(center).addScaledVector(dir, dist);
    this.camera.near = Math.max(dist / 1000, radius / 1000);
    this.camera.far = dist * 20 + radius * 10;
    this.camera.updateProjectionMatrix();
    this.controls.update();
    if (this.grid) {
      this.scene.remove(this.grid);
      this.grid.geometry.dispose();
    }
    const size = Math.pow(10, Math.ceil(Math.log10(radius * 4)));
    this.grid = new THREE.GridHelper(size, 20, '#33363b', '#24262a');
    this.grid.position.set(center.x, bb.min[1], center.z);
    (this.grid.material as THREE.Material).depthWrite = false;
    this.grid.renderOrder = -1;
    this.scene.add(this.grid);
    this.invalidate();
  }

  // ------------------------------------------------------------ picking

  private ensureBVH(o: MeshObj, positions: Float64Array): TriangleBVH {
    if (!o.bvh) {
      o.bvh = TriangleBVH.build(positions, o.entry.triangles);
      o.bvhSource = positions;
    } else if (o.bvhSource !== positions) {
      o.bvh.refit(positions);
      o.bvhSource = positions;
    }
    return o.bvh;
  }

  /** Ray-pick visible Base/Reference surfaces. */
  pick(clientX: number, clientY: number, sides: ('base' | 'ref')[]): PickHit | null {
    const s = get();
    const rect = this.renderer.domElement.getBoundingClientRect();
    const ndc = new THREE.Vector2(((clientX - rect.left) / rect.width) * 2 - 1, -((clientY - rect.top) / rect.height) * 2 + 1);
    const ray = new THREE.Raycaster();
    ray.setFromCamera(ndc, this.camera);
    const o = ray.ray.origin, d = ray.ray.direction;
    let best = null as PickHit | null;
    const tryMesh = (side: 'base' | 'ref', obj: MeshObj | null, positions: Float64Array | null, visible: boolean) => {
      if (!obj || !positions || !visible) return;
      const bvh = this.ensureBVH(obj, positions);
      const hit: RayHit = { tri: -1, t: Infinity, u: 0, v: 0, w: 0 };
      // the Base shown side by side: cast in its own space (uniform scale k, offset o), compare in world
      const sb = side === 'base' ? this.side : null;
      const k = sb ? sb.k : 1;
      const ox = sb ? (o.x - sb.o[0]) / k : o.x, oy = sb ? (o.y - sb.o[1]) / k : o.y, oz = sb ? (o.z - sb.o[2]) / k : o.z;
      if (bvh.raycast(ox, oy, oz, d.x, d.y, d.z, hit)) {
        hit.t *= k;
        if (!best || hit.t < best.hit.t) best = { side, hit, point: o.clone().addScaledVector(d, hit.t), positions, tris: obj.entry.triangles };
      }
    };
    const refVisible = s.display.showReference && !!this.ref?.entry.visible;
    if (sides.includes('base')) tryMesh('base', this.base, baseCurrentPositions(s), s.display.showBase && !!this.base?.entry.visible);
    if (sides.includes('ref')) tryMesh('ref', this.ref, this.ref?.entry.loaded.mesh.positions ?? null, refVisible);
    return best;
  }

  /** The guide dot under the mouse (within 10 px of its centre), nearest first. */
  dotAt(clientX: number, clientY: number) {
    const rect = this.renderer.domElement.getBoundingClientRect();
    let best: (typeof this.dots)[number] | null = null;
    let bestD = 10;
    for (const d of this.dots) {
      const v = d.pos.clone().project(this.camera);
      if (v.z > 1) continue;
      const x = rect.left + ((v.x + 1) / 2) * rect.width, y = rect.top + ((1 - v.y) / 2) * rect.height;
      const dist = Math.hypot(x - clientX, y - clientY);
      if (dist < bestD) (best = d), (bestD = dist);
    }
    return best;
  }

  private onPointerDown = (e: PointerEvent) => {
    this.down = { x: e.clientX, y: e.clientY, button: e.button };
    const s = get();
    if (s.tool === 'landmark' && e.button === 0 && !s.job) {
      const dot = this.dotAt(e.clientX, e.clientY);
      if (dot) {
        e.stopImmediatePropagation();
        this.renderer.domElement.setPointerCapture(e.pointerId);
        this.dragging = dot.side;
        beginGuideDrag(dot.id, dot.side);
        return;
      }
    }
    if (s.tool === 'paint' && e.button === 0 && !s.job) {
      const hit = this.pick(e.clientX, e.clientY, ['base']);
      if (hit) {
        this.painting = true;
        this.renderer.domElement.setPointerCapture(e.pointerId);
        beginStroke();
        this.lastDab = null;
        this.dab(hit.point, hit.positions);
      }
    }
    if (s.tool === 'sculpt' && e.button === 0 && !s.job && !s.preview) {
      const hit = this.pick(e.clientX, e.clientY, ['base']);
      if (hit) {
        this.renderer.domElement.setPointerCapture(e.pointerId);
        const view = this.camera.getWorldDirection(new THREE.Vector3());
        this.sculpting = { plane: s.sculpt.mode === 'move' ? new THREE.Plane().setFromNormalAndCoplanarPoint(view, hit.point) : null };
        this.lastDab = hit.point.clone();
        sculptBegin([hit.point.x, hit.point.y, hit.point.z], hit.hit.tri, e.ctrlKey);
      }
    }
  };

  private rayAt(clientX: number, clientY: number): THREE.Ray {
    const rect = this.renderer.domElement.getBoundingClientRect();
    const ndc = new THREE.Vector2(((clientX - rect.left) / rect.width) * 2 - 1, -((clientY - rect.top) / rect.height) * 2 + 1);
    const ray = new THREE.Raycaster();
    ray.setFromCamera(ndc, this.camera);
    return ray.ray;
  }

  private onPointerMove = (e: PointerEvent) => {
    const s = get();
    if (this.dragging) {
      // the dot slides over its own mesh
      const hit = this.pick(e.clientX, e.clientY, [this.dragging]);
      if (hit) dragGuide({ tri: hit.hit.tri, bary: [hit.hit.u, hit.hit.v, hit.hit.w] });
      return;
    }
    if (s.tool !== 'paint' && s.tool !== 'sculpt') return;
    if (this.sculpting?.plane) {
      // Move: the grabbed point follows the mouse on the view plane
      const q = this.rayAt(e.clientX, e.clientY).intersectPlane(this.sculpting.plane, new THREE.Vector3());
      if (q) sculptDrag([q.x, q.y, q.z]);
      this.brush.visible = false;
      this.invalidate();
      return;
    }
    const hit = this.pick(e.clientX, e.clientY, ['base']);
    if (!hit) {
      this.brush.visible = false;
      this.invalidate();
      return;
    }
    const pos = hit.positions;
    const t = hit.hit.tri * 3;
    const a = hit.tris[t] * 3, b = hit.tris[t + 1] * 3, c = hit.tris[t + 2] * 3;
    const n = new THREE.Vector3(pos[b] - pos[a], pos[b + 1] - pos[a + 1], pos[b + 2] - pos[a + 2])
      .cross(new THREE.Vector3(pos[c] - pos[a], pos[c + 1] - pos[a + 1], pos[c + 2] - pos[a + 2]))
      .normalize();
    const diag = computeBBox(pos).diagonal;
    this.brush.position.copy(hit.point);
    this.brush.lookAt(hit.point.clone().add(n));
    const sculpt = s.tool === 'sculpt';
    this.brush.scale.setScalar((sculpt ? s.sculpt.radius : s.brush.radius) * diag);
    (this.brush.material as THREE.MeshBasicMaterial).color.set(sculpt ? '#8fe3a0' : s.brush.erase ? '#7fb8ff' : '#ffb36b');
    this.brush.visible = true;
    if (this.painting) this.dab(hit.point, pos);
    if (this.sculpting && this.lastDab) {
      // dabs spaced along the stroke so fast strokes stay continuous
      const spacing = Math.max(1e-9, s.sculpt.radius * diag * 0.25);
      const steps = Math.min(32, Math.floor(this.lastDab.distanceTo(hit.point) / spacing));
      for (let k = 1; k <= steps; k++) {
        const q = this.lastDab.clone().lerp(hit.point, k / steps);
        sculptDab([q.x, q.y, q.z]);
      }
      if (steps) this.lastDab = hit.point.clone();
    }
    this.invalidate();
  };

  /** Paint at p, filling the gap to the previous dab so fast strokes stay continuous. */
  private dab(p: THREE.Vector3, positions: Float64Array) {
    const spacing = Math.max(1e-9, get().brush.radius * computeBBox(positions).diagonal * 0.3);
    if (this.lastDab) {
      const d = this.lastDab.distanceTo(p);
      const steps = Math.min(64, Math.floor(d / spacing));
      for (let k = 1; k <= steps; k++) {
        const q = this.lastDab.clone().lerp(p, k / (steps + 1));
        strokeAt([q.x, q.y, q.z]);
      }
    }
    strokeAt([p.x, p.y, p.z]);
    this.lastDab = p.clone();
  }

  private onPointerUp = (e: PointerEvent) => {
    const s = get();
    if (this.dragging) {
      this.dragging = null;
      endGuideDrag();
      try {
        this.renderer.domElement.releasePointerCapture(e.pointerId);
      } catch {
        /* already released */
      }
    } else if (this.sculpting) {
      this.sculpting = null;
      this.lastDab = null;
      sculptEnd();
      try {
        this.renderer.domElement.releasePointerCapture(e.pointerId);
      } catch {
        /* already released */
      }
    } else if (this.painting) {
      this.painting = false;
      this.lastDab = null;
      endStroke();
      try {
        this.renderer.domElement.releasePointerCapture(e.pointerId);
      } catch {
        /* already released */
      }
    } else if (s.tool === 'landmark' && this.down && this.down.button === 0 && !s.job) {
      const moved = Math.hypot(e.clientX - this.down.x, e.clientY - this.down.y);
      if (moved < 5) {
        const pending = s.pendingPick;
        const sides: ('base' | 'ref')[] = pending ? [pending.side] : ['base', 'ref'];
        const hit = this.pick(e.clientX, e.clientY, sides);
        if (hit) pickLandmarkPoint(hit.side, { tri: hit.hit.tri, bary: [hit.hit.u, hit.hit.v, hit.hit.w] });
      }
    }
    this.down = null;
  };

  /** Capture the canvas as a PNG data URL (for documentation / bug reports). */
  screenshot(): string {
    this.renderer.render(this.scene, this.camera);
    return this.renderer.domElement.toDataURL('image/png');
  }
}

export function requestFrame() {
  set((s) => ({ frameRequest: s.frameRequest + 1 }));
}
