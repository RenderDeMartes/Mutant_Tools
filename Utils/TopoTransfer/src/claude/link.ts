/**
 * Claude link: with "Claude" on, the page takes commands from its bridge (sent by Claude Code with
 * maya/tt_claude.py or the Mutant Tools MCP, or by Maya with tt_bridge.claude_call) and answers them:
 *
 *   state       the guides: name, hint, 3D point on each mesh, which ones to place
 *   capture     an orthographic picture of one mesh (front / left / right, optional zoom on a guide)
 *               with the guides drawn on it
 *   set_guides  place guides from pixels of the latest capture of that view (or from 3D points)
 *
 * Nothing leaves the machine: the bridge listens on 127.0.0.1 behind its token.
 */

import * as THREE from 'three';
import { computeBBox } from '../engine/core/mesh';
import { mat4Invert, transformPoint } from '../engine/core/mat3';
import { evalSurfacePoint, Landmark, SurfacePoint } from '../engine/landmarks/landmarks';
import { FACE_PRESET, METAHUMAN_HEAD_VERTICES, presetHint } from '../engine/landmarks/presets';
import { makeHit } from '../engine/spatial/bvh';
import { bvhFor, isMetaHumanBase, mirrorFinished } from '../state/actions';
import { baseEntry, baseRestPositions, get, log, MeshEntry, pushUndo, refEntry, set } from '../state/store';
import { pairColor } from '../ui/theme';

type Mesh = 'reference' | 'base';
type ViewName = 'front' | 'left' | 'right';
type Vec3 = [number, number, number];

const SIZE = 1024;

/** Whether a guide is asked for: with Mirror on, right points of named pairs follow their left point. */
function asked(l: Landmark, all: Landmark[]): boolean {
  return !(get().mirrorGuides && l.label.endsWith(' R') && all.some((x) => x.label === l.label.slice(0, -2) + ' L'));
}

function meshEntry(mesh: Mesh): MeshEntry {
  const e = mesh === 'base' ? baseEntry() : refEntry();
  if (!e) throw new Error(`no ${mesh} mesh loaded`);
  return e;
}

/** World positions of a mesh as shown (the Base aligned onto the Reference). */
function worldPositions(mesh: Mesh): Float64Array {
  return mesh === 'base' ? baseRestPositions()! : meshEntry('reference').loaded.mesh.positions;
}

function guidePoint(mesh: Mesh, l: Landmark): Vec3 | null {
  const sp = mesh === 'base' ? l.base : l.ref;
  return sp ? evalSurfacePoint(worldPositions(mesh), meshEntry(mesh).triangles, sp) : null;
}

const round = (p: Vec3 | null) => (p ? (p.map((v) => +v.toFixed(4)) as Vec3) : null);

function state() {
  const s = get();
  const hints = new Map(FACE_PRESET.map((p) => [p.name, p.hint]));
  return {
    units: s.units,
    mirror: s.mirrorGuides,
    mode: s.guideMode,
    note:
      "Character's left = +X, up = +Y, front = +Z (Base axes, after Align). With mirror on, place only the guides with ask=true " +
      '(left side and centre); their right twins follow. capture gives 1024x1024 pictures; set_guides takes pixels (x right, y down) ' +
      'of the latest capture of that mesh and view.',
    guides: s.landmarks.map((l) => ({
      label: l.label,
      hint: hints.get(l.label) ?? presetHint(l.label) ?? null,
      ask: asked(l, s.landmarks),
      base: round(guidePoint('base', l)),
      reference: round(guidePoint('reference', l)),
    })),
  };
}

// --------------------------------------------------------------- capture

interface Shot {
  cam: THREE.OrthographicCamera;
  forward: THREE.Vector3;
}
const shots = new Map<string, Shot>();

/** Head frame from the aligned Base: its axes and the box of its head (MetaHuman: the head mesh only). */
function headFrame() {
  const b = meshEntry('base');
  const T = get().transform;
  const o = transformPoint([0, 0, 0], T);
  const axis = (v: Vec3) => {
    const p = transformPoint(v, T);
    return new THREE.Vector3(p[0] - o[0], p[1] - o[1], p[2] - o[2]).normalize();
  };
  const world = baseRestPositions()!;
  const box = computeBBox(isMetaHumanBase(b) ? world.subarray(0, METAHUMAN_HEAD_VERTICES * 3) : world);
  return { center: new THREE.Vector3(...box.center), radius: 0.32 * box.diagonal, front: axis([0, 0, 1]), up: axis([0, 1, 0]), left: axis([1, 0, 0]) };
}

function capture(args: { view?: ViewName; mesh?: Mesh; focus?: string; zoom?: number }) {
  const view: ViewName = args.view ?? 'front';
  const mesh: Mesh = args.mesh ?? 'reference';
  const entry = meshEntry(mesh);
  const f = headFrame();
  const center = f.center.clone();
  if (args.focus) {
    const l = get().landmarks.find((x) => x.label === args.focus);
    const p = l && guidePoint(mesh, l);
    if (!p) throw new Error(`no guide ${args.focus} on the ${mesh}`);
    center.set(...p);
  }
  const r = f.radius / Math.max(1, Math.min(args.zoom ?? 1, 20));
  const look = view === 'front' ? f.front : view === 'left' ? f.left : f.left.clone().negate();

  const geom = new THREE.BufferGeometry();
  geom.setAttribute('position', new THREE.BufferAttribute(new Float32Array(worldPositions(mesh)), 3));
  geom.setIndex(new THREE.BufferAttribute(entry.triangles, 1));
  geom.computeVertexNormals();
  const scene = new THREE.Scene();
  scene.background = new THREE.Color('#ffffff');
  scene.add(new THREE.Mesh(geom, new THREE.MeshStandardMaterial({ color: '#b9b4ac', roughness: 0.85, side: THREE.DoubleSide })));
  scene.add(new THREE.HemisphereLight(0xffffff, 0x555555, 1.2));
  const cam = new THREE.OrthographicCamera(-r, r, r, -r, f.radius * 0.01, f.radius * 8);
  cam.position.copy(center).addScaledVector(look, f.radius * 3);
  cam.up.copy(f.up);
  cam.lookAt(center);
  cam.updateMatrixWorld();
  cam.updateProjectionMatrix();
  const light = new THREE.DirectionalLight(0xffffff, 1.6);
  light.position.copy(cam.position);
  scene.add(light);
  const renderer = new THREE.WebGLRenderer({ antialias: true, preserveDrawingBuffer: true });
  renderer.setPixelRatio(1);
  renderer.setSize(SIZE, SIZE, false);
  renderer.render(scene, cam);

  // the guides on top: a dot in the pair's colour and its name
  const canvas = document.createElement('canvas');
  canvas.width = canvas.height = SIZE;
  const ctx = canvas.getContext('2d')!;
  ctx.drawImage(renderer.domElement, 0, 0);
  renderer.dispose();
  geom.dispose();
  ctx.font = '13px sans-serif';
  ctx.lineWidth = 3;
  const forward = new THREE.Vector3().subVectors(center, cam.position).normalize();
  for (const l of get().landmarks) {
    const p = guidePoint(mesh, l);
    if (!p) continue;
    // hidden behind the mesh (the far side of the head): the first hit along the view is elsewhere
    const from: Vec3 = [p[0] - forward.x * f.radius * 4, p[1] - forward.y * f.radius * 4, p[2] - forward.z * f.radius * 4];
    const first = rayHit(mesh, from, [forward.x, forward.y, forward.z]);
    const q = first && evalSurfacePoint(worldPositions(mesh), entry.triangles, first);
    if (!q || Math.hypot(q[0] - p[0], q[1] - p[1], q[2] - p[2]) > 0.01 * f.radius) continue;
    const v = new THREE.Vector3(...p).project(cam);
    const x = ((v.x + 1) / 2) * SIZE, y = ((1 - v.y) / 2) * SIZE;
    if (x < 0 || y < 0 || x > SIZE || y > SIZE) continue;
    ctx.fillStyle = pairColor(l.id);
    ctx.beginPath();
    ctx.arc(x, y, 5, 0, Math.PI * 2);
    ctx.fill();
    ctx.strokeStyle = '#ffffff';
    ctx.strokeText(l.label, x + 8, y + 4);
    ctx.fillStyle = '#222222';
    ctx.fillText(l.label, x + 8, y + 4);
  }
  shots.set(`${mesh}:${view}`, { cam, forward });
  return { png: canvas.toDataURL('image/png').split(',')[1], mesh, view, size: SIZE };
}

// --------------------------------------------------------------- set_guides

interface PointArg {
  label: string;
  mesh?: Mesh;
  view?: ViewName;
  x?: number;
  y?: number;
  position?: Vec3;
}

/** First surface point of `mesh` along a world ray. */
function rayHit(mesh: Mesh, origin: Vec3, dir: Vec3): SurfacePoint | null {
  // the Base is searched in its own coordinates
  const inv = mesh === 'base' ? mat4Invert(get().transform) : null;
  const a = inv ? transformPoint(origin, inv) : origin;
  const b = inv ? transformPoint([origin[0] + dir[0], origin[1] + dir[1], origin[2] + dir[2]], inv) : [origin[0] + dir[0], origin[1] + dir[1], origin[2] + dir[2]];
  const hit = { tri: -1, t: Infinity, u: 0, v: 0, w: 0 };
  return bvhFor(meshEntry(mesh)).raycast(a[0], a[1], a[2], b[0] - a[0], b[1] - a[1], b[2] - a[2], hit) ? { tri: hit.tri, bary: [hit.u, hit.v, hit.w] } : null;
}

/** Surface point of `mesh` under a pixel of its latest capture of `view`, or closest to a 3D point. */
function surfacePoint(mesh: Mesh, p: PointArg): SurfacePoint | null {
  if (p.position) {
    const inv = mesh === 'base' ? mat4Invert(get().transform) : null;
    const q = inv ? transformPoint(p.position, inv) : p.position;
    const hit = makeHit();
    return bvhFor(meshEntry(mesh)).closestPoint(q[0], q[1], q[2], Infinity, hit) ? { tri: hit.tri, bary: [hit.u, hit.v, hit.w] } : null;
  }
  const shot = shots.get(`${mesh}:${p.view ?? 'front'}`);
  if (!shot) throw new Error(`capture the ${mesh} from the ${p.view ?? 'front'} first`);
  const o = new THREE.Vector3((p.x! / SIZE) * 2 - 1, 1 - (p.y! / SIZE) * 2, -1).unproject(shot.cam);
  return rayHit(mesh, [o.x, o.y, o.z], [shot.forward.x, shot.forward.y, shot.forward.z]);
}

function setGuides(args: { points?: PointArg[] }) {
  const points = args.points ?? [];
  const found: { id: number; side: 'base' | 'ref'; sp: SurfacePoint }[] = [];
  const missed: { label: string; reason: string }[] = [];
  let landmarks = get().landmarks;
  let nextId = get().nextLandmarkId;
  for (const p of points) {
    const mesh: Mesh = p.mesh ?? 'reference';
    let l = landmarks.find((x) => x.label === p.label);
    if (!l) {
      l = { id: nextId++, label: p.label, group: 'face', weight: 1, base: null, ref: null };
      landmarks = [...landmarks, l];
    }
    try {
      const sp = surfacePoint(mesh, p);
      if (sp) found.push({ id: l.id, side: mesh === 'base' ? 'base' : 'ref', sp });
      else missed.push({ label: p.label, reason: 'that pixel misses the mesh' });
    } catch (e) {
      missed.push({ label: p.label, reason: (e as Error).message });
    }
  }
  if (found.length) {
    pushUndo('Claude guides');
    for (const f of found) landmarks = landmarks.map((l) => (l.id === f.id ? { ...l, [f.side]: f.sp } : l));
    set({ landmarks, nextLandmarkId: nextId, pendingPick: null, guided: false, tool: 'landmark' });
    if (get().mirrorGuides) for (const f of found) mirrorFinished(f.id, f.side);
    log('info', `Claude placed ${found.length} guide point(s).`);
  }
  return { placed: found.length, missed };
}

// --------------------------------------------------------------- loop

const COMMANDS: Record<string, (args: never) => unknown> = { state, capture, set_guides: setGuides };

/** Ask the bridge for commands while the link is on (long poll), run them and send the answers back. */
export async function runClaudeLink() {
  const url = get().returnUrl;
  if (!url) return;
  const next = new URL('claude/next', url).toString();
  const reply = new URL('claude/reply', url).toString();
  log('info', 'Claude link on: ask Claude Code to place the guides.');
  while (get().claudeLink) {
    let cmd: { id: string; command: string; args: Record<string, unknown> } | null = null;
    try {
      const res = await fetch(next, { cache: 'no-store' });
      if (res.status === 200) cmd = await res.json();
      else if (res.status !== 204) throw new Error(`HTTP ${res.status}`);
    } catch (e) {
      log('warn', `Claude link: the bridge did not answer (${(e as Error).message}). Is the Maya window that opened this page still open?`);
      set({ claudeLink: false });
      break;
    }
    if (!cmd) continue;
    let body: object;
    try {
      const fn = COMMANDS[cmd.command];
      if (!fn) throw new Error(`unknown command ${cmd.command}`);
      body = { id: cmd.id, ok: true, result: fn((cmd.args ?? {}) as never) };
    } catch (e) {
      body = { id: cmd.id, ok: false, message: (e as Error).message };
    }
    await fetch(reply, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body) }).catch(() => undefined);
  }
  log('info', 'Claude link off.');
}
