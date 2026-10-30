/**
 * User-level operations. Every expensive computation goes through the
 * GeometryEngine (Web Worker); cheap, interactive ones (landmark alignment,
 * mask painting) run directly on the engine's pure functions.
 */

import { boundingBoxAlignment } from '../engine/alignment/rigid';
import { computeBBox } from '../engine/core/mesh';
import { buildAdjacency, Adjacency } from '../engine/geometry/topology';
import { alignFromLandmarks, evalSurfacePoint, Landmark, LandmarkGroup, SurfacePoint } from '../engine/landmarks/landmarks';
import { FACE_PRESET, METAHUMAN_FACE_VERTEX, METAHUMAN_HEAD_VERTICES, mirrorName, PRESETS, PresetKind } from '../engine/landmarks/presets';
import { defaultSymmetryPlane, fitSymmetryPlane, mirrorSurfacePoint, Plane } from '../engine/landmarks/mirror';
import { makeHit, TriangleBVH } from '../engine/spatial/bvh';
import { transformPoint } from '../engine/core/mat3';
import { growMask, invertMask, paintSphere, smoothMask } from '../engine/constraints/mask';
import { ComponentInfo, ComponentMode, defaultComponentModes, labelComponents } from '../engine/constraints/components';
import { applyField, exampleHeadBase, HEAD_FIELD, icosphere } from '../engine/synthetic/shapes';
import { writeOBJ } from '../engine/io/obj';
import { isMetaHumanExport } from '../engine/io/load';
import { mat4Identity, transformPositions } from '../engine/core/mat3';
import { DEFAULT_WRAP_PARAMS, WrapParams } from '../engine/wrapping/params';
import type { ExportFormat, ExportSpace } from '../engine/export/exporter';
import { CancelledError, WorkerEngine } from '../worker/client';
import { fmtLen } from '../ui/format';
import { fetchLaunchFile, LaunchParams, postResult } from './launch';
import {
  baseCurrentPositions,
  baseEntry,
  baseRestPositions,
  get,
  HeatmapMode,
  log,
  MeshEntry,
  MeshRoleUI,
  pushUndo,
  refEntry,
  set,
  Tool,
} from './store';

export const engine = new WorkerEngine();

let meshCounter = 1;

// ---------------------------------------------------------------- helpers

function polygonEdges(faceOffsets: Uint32Array, faceIndices: Uint32Array, n: number): Uint32Array {
  const keys: number[] = [];
  for (let f = 0; f + 1 < faceOffsets.length; f++) {
    const s = faceOffsets[f], e = faceOffsets[f + 1];
    for (let k = s; k < e; k++) {
      const a = faceIndices[k], b = faceIndices[k + 1 < e ? k + 1 : s];
      if (a === b) continue;
      keys.push(a < b ? a * n + b : b * n + a);
    }
  }
  const sorted = Float64Array.from(keys).sort();
  const out: number[] = [];
  let last = -1;
  for (const k of sorted) {
    if (k === last) continue;
    last = k;
    out.push(Math.floor(k / n), k % n);
  }
  return Uint32Array.from(out);
}

const adjCache = new WeakMap<object, Adjacency>();
export function baseAdjacency(entry: MeshEntry): Adjacency {
  let a = adjCache.get(entry.loaded);
  if (!a) {
    a = buildAdjacency(entry.triangles, entry.loaded.mesh.positions.length / 3);
    adjCache.set(entry.loaded, a);
  }
  return a;
}

const compCache = new WeakMap<object, ComponentInfo>();
/** Connected components of a mesh (same labelling as the solver uses). */
export function meshComponents(entry: MeshEntry): ComponentInfo {
  let c = compCache.get(entry.loaded);
  if (!c) {
    c = labelComponents(baseAdjacency(entry));
    compCache.set(entry.loaded, c);
  }
  return c;
}

/** Component modes in effect for the current base (explicit or automatic). */
export function effectiveComponentModes(): ComponentMode[] | null {
  const b = baseEntry();
  if (!b) return null;
  const info = meshComponents(b);
  const m = get().componentModes;
  return m && m.length === info.sizes.length ? m : defaultComponentModes(info.sizes);
}

export function setComponentMode(index: number, mode: ComponentMode) {
  const modes = effectiveComponentModes();
  if (!modes) return;
  const next = modes.slice();
  next[index] = mode;
  set({ componentModes: next });
}

function busy(): boolean {
  return get().job !== null;
}

function requireIdle(what: string): boolean {
  if (busy()) {
    log('warn', `${what}: wait for the running operation to finish or cancel it.`);
    return false;
  }
  return true;
}

function fmtMs(ms: number) {
  return ms < 1000 ? `${ms.toFixed(0)} ms` : `${(ms / 1000).toFixed(2)} s`;
}

/** Clear deformation-dependent state when roles or meshes change. */
function resetDependentState(reason: string) {
  const s = get();
  if (s.committed || s.preview || s.landmarks.length || s.mask) log('info', `${reason}: landmarks, regions and deformation were reset.`);
  set({
    committed: null,
    committedResult: null,
    preview: null,
    landmarks: [],
    selectedLandmarkId: null,
    pendingPick: null,
    guided: false,
    mask: null,
    componentModes: null,
    heat: null,
    transform: mat4Identity(),
    undoStack: [],
    redoStack: [],
  });
}

// ---------------------------------------------------------------- loading

export async function loadBuffers(files: { name: string; buffer: ArrayBuffer; role?: MeshRoleUI }[]) {
  for (const f of files) {
    if (!requireIdle('Load')) return;
    const s = get();
    const isStl = f.name.toLowerCase().endsWith('.stl');
    const role: MeshRoleUI = f.role !== undefined ? f.role : !baseEntry(s) && !isStl ? 'base' : !refEntry(s) ? 'reference' : null;
    set({ job: { kind: 'load', label: `Loading ${f.name}`, progress: 0, message: 'Parsing and validating', startedAt: performance.now(), cancellable: false } });
    try {
      const res = await engine.loadMesh(f.name, f.buffer, role === 'base' ? 'base' : 'reference');
      const mesh = res.loaded.mesh;
      const n = mesh.positions.length / 3;
      const entry: MeshEntry = {
        id: `m${meshCounter++}`,
        name: f.name,
        loaded: res.loaded,
        validation: res.validation,
        triangles: res.triangles,
        triFace: res.triFace,
        polyEdges: polygonEdges(mesh.faceOffsets, mesh.faceIndices, n),
        visible: true,
        role,
        version: 1,
      };
      if (role) resetDependentState(`New ${role} mesh`);
      // MetaHuman exports from Meta Mutant are in centimetres
      if (res.loaded.source.kind === 'obj' && res.loaded.source.lines.slice(0, 4).some((l) => l.includes('MetaHuman')) && get().units === 'none') {
        set({ units: 'cm', guideMode: 'metahuman' });
        log('info', `${f.name}: MetaHuman export detected — units set to cm. See Meta Mutant's README.`);
      }
      set((st) => ({ meshes: [...st.meshes.map((m) => (role && m.role === role ? { ...m, role: null } : m)), entry], frameRequest: st.frameRequest + 1 }));
      const st = res.validation.stats;
      log('info', `Loaded ${f.name} as ${role ?? 'unassigned'}: ${st.vertices.toLocaleString()} vertices, ${st.faces.toLocaleString()} faces (${fmtMs(res.parseMs)}).`);
      for (const a of res.loaded.attributes) log('info', `  ${f.name}: ${a}`);
      for (const w of res.loaded.warnings) log('warn', `  ${f.name}: ${w}`);
      for (const issue of res.validation.issues) log(issue.severity === 'error' ? 'error' : issue.severity === 'warning' ? 'warn' : 'info', `  ${f.name}: ${issue.message}`);
      if (role === 'base' && n > 100000) log('warn', `${f.name} has ${n.toLocaleString()} vertices, above the 100k design target for Base meshes. Wrapping will be slow (see docs/PERFORMANCE.md).`);
      if (role !== 'base' && n > 1000000) log('warn', `${f.name} has ${n.toLocaleString()} vertices. Large references mostly cost memory and closest-point time; consider decimating very dense scans.`);
    } catch (e) {
      log('error', `Could not load ${f.name}: ${(e as Error).message}`);
    } finally {
      set({ job: null });
    }
  }
}

export async function loadFiles(files: File[]) {
  const list = await Promise.all(files.map(async (file) => ({ name: file.name, buffer: await file.arrayBuffer() })));
  // Base candidates first: a MetaHuman export is always the Base, STL can only be a Reference
  const rank = (f: { name: string; buffer: ArrayBuffer }) => (isMetaHumanExport(f.buffer) ? 0 : f.name.toLowerCase().endsWith('.stl') ? 2 : 1);
  list.sort((a, b) => rank(a) - rank(b));
  const mh = list.findIndex((f) => isMetaHumanExport(f.buffer));
  if (mh >= 0 && list.length >= 2) {
    // dropping the MetaHuman export together with the custom head: assign both roles explicitly
    await loadBuffers(list.map((f, i) => ({ ...f, role: i === 0 ? ('base' as const) : i === 1 ? ('reference' as const) : null })));
    return;
  }
  await loadBuffers(list);
}

/**
 * Load the meshes named by the launch parameters (`?base=…&reference=…&return=…`,
 * see launch.ts) and remember the return URL for Export.
 */
export async function loadFromLaunch(p: LaunchParams) {
  for (const e of p.errors) log('warn', e);
  if (p.returnUrl) {
    set({ returnUrl: p.returnUrl, exportFormat: 'obj' });
    log('info', `Export will send the OBJ back to ${new URL(p.returnUrl).host} (the tool that opened this page).`);
  }
  const wanted = [
    { url: p.base, role: 'base' as const, fallback: 'base.obj' },
    { url: p.reference, role: 'reference' as const, fallback: 'reference.obj' },
  ].filter((w): w is { url: string; role: 'base' | 'reference'; fallback: string } => !!w.url);
  if (!wanted.length || !requireIdle('Load')) return;
  set({ job: { kind: 'load', label: 'Fetching meshes', progress: 0, message: 'From the tool that opened this page', startedAt: performance.now(), cancellable: false } });
  const files: { name: string; buffer: ArrayBuffer; role: MeshRoleUI }[] = [];
  try {
    for (const w of wanted) {
      try {
        files.push({ ...(await fetchLaunchFile(w.url, w.fallback)), role: w.role });
      } catch (e) {
        log('error', `Could not fetch the ${w.role} mesh from ${new URL(w.url).host}: ${(e as Error).message}. Is the tool that opened this page still running? You can also load the file by hand.`);
      }
    }
  } finally {
    set({ job: null });
  }
  await loadBuffers(files);
}

export type ExampleKind = 'synthetic' | 'body' | 'head';

const HUMAN_EXAMPLES: Record<'body' | 'head', { base: string; ref: string; hint: string }> = {
  body: {
    base: 'body_male_base.obj',
    ref: 'body_female_sculpt_ref.ply',
    hint: 'CC0 human body: male base cage (eyes Follow) → female sculpt (169k vertices). Align with Auto (bounds, scale off) → ICP refine, then Wrap.',
  },
  head: {
    base: 'head_anim_base.obj',
    ref: 'head_sculpt_ref.ply',
    hint: 'CC0 human head: animation topology (sclera/iris Follow) → sculpting head with different topology. Align with Auto → ICP refine, then Wrap.',
  },
};

/** Load one of the bundled examples (human ones are CC0 meshes from Blender Studio, served with the app). */
export async function loadExampleKind(kind: ExampleKind) {
  if (kind === 'synthetic') return loadExample();
  if (!requireIdle('Example')) return;
  const ex = HUMAN_EXAMPLES[kind];
  set({ job: { kind: 'load', label: 'Fetching example', progress: 0, message: 'Downloading bundled CC0 meshes from this app', startedAt: performance.now(), cancellable: false } });
  let files: { name: string; buffer: ArrayBuffer; role: MeshRoleUI }[];
  try {
    const base = import.meta.env.BASE_URL;
    const get1 = async (f: string) => {
      const r = await fetch(`${base}examples/human/${f}`);
      if (!r.ok) throw new Error(`${f}: HTTP ${r.status}`);
      return r.arrayBuffer();
    };
    const [b, r] = await Promise.all([get1(ex.base), get1(ex.ref)]);
    files = [
      { name: ex.base, buffer: b, role: 'base' },
      { name: ex.ref, buffer: r, role: 'reference' },
    ];
  } catch (e) {
    set({ job: null });
    return log('error', `Could not load the example: ${(e as Error).message}`);
  }
  set({ job: null, meshes: [] });
  resetDependentState('Example');
  await loadBuffers(files);
  set({ units: 'm' });
  log('info', ex.hint);
  log('info', 'Example meshes: Blender Studio "Human Base Meshes", CC0.');
}

/**
 * Example scene: a quad sphere base and a differently tessellated stylised
 * head reference, deliberately mis-scaled/offset so alignment is needed.
 * Generated geometry is serialised to OBJ and loaded through the normal path.
 */
export async function loadExample() {
  if (!requireIdle('Example')) return;
  set({ meshes: [] });
  resetDependentState('Example');
  const base = exampleHeadBase(40);
  const ref = applyField(icosphere(6), HEAD_FIELD);
  // reference "scan" in centimetres, rotated slightly and lifted
  const c = Math.cos(0.18), s = Math.sin(0.18);
  const m = mat4Identity();
  m[0] = 12 * c; m[2] = -12 * s; m[5] = 12; m[8] = 12 * s; m[10] = 12 * c;
  m[13] = 160;
  m[12] = 4;
  const refMoved = { ...ref, positions: transformPositions(ref.positions, m) };
  const enc = new TextEncoder();
  await loadBuffers([
    { name: 'example_base_head_with_eyes.obj', buffer: enc.encode(writeOBJ(base, { header: ['TopoTransfer example base: quad sphere head proxy with two eyeball components'] })).buffer as ArrayBuffer, role: 'base' },
    { name: 'example_reference_head.obj', buffer: enc.encode(writeOBJ(refMoved, { header: ['TopoTransfer example reference: stylised head, cm units'] })).buffer as ArrayBuffer, role: 'reference' },
  ]);
  set({ units: 'cm', allowScale: true });
  log('info', 'Example loaded. Next: Align, then Wrap.');
}

export function setRole(id: string, role: MeshRoleUI) {
  if (!requireIdle('Change role')) return;
  const entry = get().meshes.find((m) => m.id === id);
  if (!entry) return;
  if (role === 'base' && entry.loaded.format === 'stl') {
    log('error', 'STL meshes cannot be the Base mesh (no stored connectivity). Use OBJ or PLY.');
    return;
  }
  resetDependentState('Role change');
  set((s) => ({
    meshes: s.meshes.map((m) => (m.id === id ? { ...m, role } : role && m.role === role ? { ...m, role: null } : m)),
  }));
}

export function removeMesh(id: string) {
  if (!requireIdle('Remove')) return;
  const entry = get().meshes.find((m) => m.id === id);
  if (entry?.role) resetDependentState('Mesh removed');
  set((s) => ({ meshes: s.meshes.filter((m) => m.id !== id) }));
}

export function toggleVisible(id: string) {
  set((s) => ({ meshes: s.meshes.map((m) => (m.id === id ? { ...m, visible: !m.visible } : m)) }));
}

// ---------------------------------------------------------------- alignment

function alignmentLocked(): boolean {
  const s = get();
  if (s.committed || s.preview) {
    log('warn', 'Alignment is locked while a deformation exists. Reset the deformation first (alignment and wrapping are separate stages).');
    return true;
  }
  return false;
}

export function setTransform(t: Float64Array, label = 'Transform') {
  if (alignmentLocked()) return;
  pushUndo(label);
  set({ transform: t, heat: null });
}

export function autoAlign(allowScale: boolean) {
  const b = baseEntry(), r = refEntry();
  if (!b || !r) return log('warn', 'Auto alignment needs a Base and a Reference mesh.');
  if (alignmentLocked()) return;
  const t = boundingBoxAlignment(b.loaded.mesh.positions, r.loaded.mesh.positions, allowScale);
  setTransform(t, 'Auto align (bounding box)');
  set((s) => ({ frameRequest: s.frameRequest + 1 }));
  log('info', `Bounding-box alignment applied${allowScale ? ' (with uniform scale)' : ''}.`);
}

export function alignLandmarks(allowScale: boolean) {
  const b = baseEntry(), r = refEntry();
  if (!b || !r) return;
  if (alignmentLocked()) return;
  try {
    const fit = alignFromLandmarks(get().landmarks, b.loaded.mesh.positions, b.triangles, r.loaded.mesh.positions, r.triangles, allowScale);
    setTransform(fit.transform, 'Align from landmarks');
    log('info', `Landmark alignment: RMS residual ${fit.rms.toPrecision(3)} (measured at landmarks), scale ${fit.scale.toFixed(4)}.`);
  } catch (e) {
    log('error', (e as Error).message);
  }
}

export async function runICP(allowScale: boolean) {
  const b = baseEntry(), r = refEntry();
  if (!b || !r) return log('warn', 'ICP needs a Base and a Reference mesh.');
  if (alignmentLocked() || !requireIdle('ICP')) return;
  set({ job: { kind: 'icp', label: 'Rigid ICP', progress: 0, message: 'Iterating closest points', startedAt: performance.now(), cancellable: false } });
  try {
    const res = await engine.icp({
      refKey: { id: r.id, version: r.version },
      basePositions: b.loaded.mesh.positions,
      initialTransform: get().transform,
      refPositions: r.loaded.mesh.positions,
      refTriangles: r.triangles,
      options: { allowScale, maxIterations: 60 },
    });
    if (res.rmsAfter >= res.rmsBefore * (1 - 1e-6)) {
      log('info', `ICP found no placement better than the bounding-box one (RMS ${fmtLen(res.rmsBefore)}); kept it. Normal when the shapes differ a lot — landmarks give a better start.`);
      return;
    }
    setTransform(res.transform, allowScale ? 'ICP (similarity)' : 'ICP (rigid)');
    log(
      'info',
      `ICP ${res.converged ? 'converged' : 'stopped'} after ${res.iterations} iterations: RMS distance ${fmtLen(res.rmsBefore)} → ${fmtLen(res.rmsAfter)} (measured on sampled vertices).`,
    );
  } catch (e) {
    if (!(e instanceof CancelledError)) log('error', `ICP failed: ${(e as Error).message}`);
  } finally {
    set({ job: null });
  }
}

/** One-click alignment: bounding boxes, then ICP refinement (uniform scale on unless turned off). */
export async function autoAlignAndRefine() {
  const allowScale = get().allowScale;
  autoAlign(allowScale);
  if (get().committed || get().preview) return;
  await runICP(allowScale);
}

/** Swap Base and Reference roles (not possible when the Reference is an STL). */
export function swapRoles() {
  const b = baseEntry(), r = refEntry();
  if (!b || !r) return;
  if (r.loaded.format === 'stl') return log('error', 'The Reference is an STL, which cannot be a Base mesh.');
  if (!requireIdle('Swap')) return;
  resetDependentState('Swap');
  set((s) => ({ meshes: s.meshes.map((m) => (m.id === b.id ? { ...m, role: 'reference' as const } : m.id === r.id ? { ...m, role: 'base' as const } : m)) }));
}

export function resetTransform() {
  setTransform(mat4Identity(), 'Reset transform');
}

// ---------------------------------------------------------------- wrapping

export function estimateWrapSeconds(n: number, p: WrapParams): number {
  // linear fit to docs/PERFORMANCE.md (≈ 0.22 ms per vertex for 4×6 iterations); an estimate only
  return (n * 0.22e-3 * (p.levels * p.iterationsPerLevel)) / 24 + 0.3;
}

export async function runWrap() {
  const b = baseEntry(), r = refEntry();
  if (!b || !r) return log('warn', 'Wrapping needs a Base and a Reference mesh.');
  if (!requireIdle('Wrap')) return;
  const s = get();
  if (s.preview) return log('warn', 'Commit or discard the current preview before running again.');
  const rest = baseRestPositions()!;
  const start = s.committed ?? rest;
  const n = rest.length / 3;
  const est = estimateWrapSeconds(n, s.params);
  if (est > 8) log('info', `Estimated wrapping time ≈ ${est.toFixed(0)} s for ${n.toLocaleString()} vertices (estimate from benchmarks; actual time depends on the machine).`);
  set({
    job: { kind: 'wrap', label: 'Wrapping', progress: 0, message: 'Starting', startedAt: performance.now(), cancellable: true },
    heat: null,
  });
  try {
    const res = await engine.wrap(
      {
        baseKey: { id: b.id, version: b.version },
        refKey: { id: r.id, version: r.version },
        baseRest: rest,
        baseStart: start,
        baseTriangles: b.triangles,
        refPositions: r.loaded.mesh.positions,
        refTriangles: r.triangles,
        landmarks: s.landmarks,
        mask: s.mask,
        componentModes: effectiveComponentModes(),
        params: s.params,
      },
      (p) => set((st) => (st.job ? { job: { ...st.job, progress: p.fraction, message: p.message, wrapProgress: p } } : {})),
    );
    if (res.status === 'completed' && res.diagnostics) {
      const d = res.diagnostics;
      set({ preview: { positions: res.positions, result: res }, bottomTab: 'log' });
      log(
        d.warnings.length ? 'warn' : 'info',
        `Wrap preview ready in ${fmtMs(d.timings.totalMs)}: mean distance ${fmtLen(d.distanceBefore.mean)} → ${fmtLen(d.distanceAfter.mean)}, max ${fmtLen(d.distanceAfter.max)} (measured at ${d.distanceAfter.count.toLocaleString()} vertices). Keep or discard it.`,
      );
      for (const w of d.warnings) log('warn', `  ${w}`);
    } else if (res.status === 'cancelled') {
      log('info', res.message);
    } else {
      log('error', `Wrap failed: ${res.message}`);
    }
  } catch (e) {
    if (e instanceof CancelledError) log('info', 'Wrapping cancelled; no changes were applied.');
    else log('error', `Wrap failed: ${(e as Error).message}`);
  } finally {
    set({ job: null });
  }
}

export async function cancelJob() {
  const j = get().job;
  if (!j?.cancellable) return;
  set({ job: { ...j, message: 'Cancelling…', cancellable: false } });
  await engine.cancel();
}

export function commitPreview() {
  const s = get();
  if (!s.preview) return;
  pushUndo('Commit wrap');
  set({ committed: s.preview.positions, committedResult: s.preview.result, preview: null, heat: null });
  log('info', 'Wrap result kept.');
}

export function discardPreview() {
  if (!get().preview) return;
  set({ preview: null, heat: null });
  log('info', 'Wrap preview discarded.');
}

export function resetDeformation() {
  const s = get();
  if (s.preview) discardPreview();
  if (!s.committed) return;
  pushUndo('Reset deformation');
  set({ committed: null, committedResult: null, heat: null });
  log('info', 'Deformation reset to the aligned base mesh.');
}

export function setParams(p: Partial<WrapParams>) {
  set((s) => ({ params: { ...s.params, ...p } }));
}

export function resetParams() {
  set({ params: { ...DEFAULT_WRAP_PARAMS } });
}

// ---------------------------------------------------------------- landmarks

export function setTool(tool: Tool) {
  set((s) => ({ tool: s.tool === tool && tool !== 'navigate' ? 'navigate' : tool, pendingPick: null, guided: false }));
}

/** Next landmark side to place after `fromId` (same landmark's other side first, then following landmarks). */
function nextMissing(landmarks: Landmark[], fromId: number | null, mirror = false): { landmarkId: number; side: 'base' | 'ref' } | null {
  if (!landmarks.length) return null;
  const labels = new Set(landmarks.map((l) => l.label));
  const start = Math.max(0, landmarks.findIndex((l) => l.id === fromId));
  for (let k = 0; k < landmarks.length; k++) {
    const l = landmarks[(start + k) % landmarks.length];
    // mirror on: the right point of a named pair is filled by mirroring its left point, not asked for
    // (guides go on the character's left, as in Mutant Tools)
    if (mirror && l.label.endsWith(' R') && labels.has(l.label.slice(0, -2) + ' L')) continue;
    if (!l.base) return { landmarkId: l.id, side: 'base' };
    if (!l.ref) return { landmarkId: l.id, side: 'ref' };
  }
  return null;
}

function advanceGuided(fromId: number | null) {
  const s = get();
  const next = nextMissing(s.landmarks, fromId, s.mirrorGuides);
  if (!next) {
    set({ pendingPick: null, guided: false, tool: 'navigate' });
    log('info', 'All landmarks are placed.');
    return;
  }
  set({ pendingPick: next, selectedLandmarkId: next.landmarkId, tool: 'landmark' });
}

/** Add a named landmark preset (missing names only) and start guided placement. */
export function addPreset(kind: PresetKind) {
  const s = get();
  const existing = new Set(s.landmarks.map((l) => l.label));
  const add = PRESETS[kind].filter((p) => !existing.has(p.name));
  pushUndo(`Add ${kind} landmark preset`);
  let id = s.nextLandmarkId;
  const created: Landmark[] = add.map((p) => ({ id: id++, label: p.name, group: p.group, weight: 1, base: null, ref: null }));
  set({ landmarks: [...s.landmarks, ...created], nextLandmarkId: id, guided: true });
  log('info', `${created.length} ${kind} landmarks added. Click each highlighted point on the Base, then on the Reference (Skip if a point is not visible; Mirror fills the other side).`);
  advanceGuided(created[0]?.id ?? null);
}

/** Skip the current guided landmark side. */
export function skipGuided() {
  const s = get();
  const p = s.pendingPick;
  if (!p) return;
  const idx = s.landmarks.findIndex((l) => l.id === p.landmarkId);
  // next missing side strictly after this landmark (the skipped one stays empty)
  const rest = [...s.landmarks.slice(idx + 1), ...s.landmarks.slice(0, idx)];
  const n = rest.map((l) => (!l.base ? { landmarkId: l.id, side: 'base' as const } : !l.ref ? { landmarkId: l.id, side: 'ref' as const } : null)).find(Boolean) ?? null;
  if (!n) {
    set({ pendingPick: null, guided: false, tool: 'navigate' });
    return;
  }
  set({ pendingPick: n, selectedLandmarkId: n.landmarkId });
}

export function startGuided() {
  set({ guided: true });
  advanceGuided(get().selectedLandmarkId);
}

const bvhCache = new WeakMap<object, TriangleBVH>();
export function bvhFor(entry: MeshEntry): TriangleBVH {
  let b = bvhCache.get(entry.loaded);
  if (!b) {
    b = TriangleBVH.build(entry.loaded.mesh.positions, entry.triangles);
    bvhCache.set(entry.loaded, b);
  }
  return b;
}

/** Symmetry planes: base in its own coordinates, reference starting from the aligned base plane. */
let planeCache: { b: object; r: object; t: Float64Array; planes: { base: Plane; ref: Plane } } | null = null;

/** Each mesh's symmetry plane, cached per meshes and placement (fitting one walks every vertex). */
export function symmetryPlanes(): { base: Plane; ref: Plane } | null {
  const b = baseEntry(), r = refEntry();
  if (!b || !r) return null;
  if (planeCache && planeCache.b === b.loaded && planeCache.r === r.loaded && planeCache.t === get().transform) return planeCache.planes;
  const planes = fitPlanes(b, r);
  planeCache = { b: b.loaded, r: r.loaded, t: get().transform, planes };
  return planes;
}

function fitPlanes(b: MeshEntry, r: MeshEntry): { base: Plane; ref: Plane } {
  const bp = fitSymmetryPlane(b.loaded.mesh.positions, bvhFor(b), defaultSymmetryPlane(b.loaded.mesh.positions));
  const T = get().transform;
  const p0 = transformPoint(bp.point, T);
  const p1 = transformPoint([bp.point[0] + bp.normal[0], bp.point[1] + bp.normal[1], bp.point[2] + bp.normal[2]], T);
  const nl = Math.hypot(p1[0] - p0[0], p1[1] - p0[1], p1[2] - p0[2]) || 1;
  const init: Plane = { point: p0, normal: [(p1[0] - p0[0]) / nl, (p1[1] - p0[1]) / nl, (p1[2] - p0[2]) / nl] };
  const rp = fitSymmetryPlane(r.loaded.mesh.positions, bvhFor(r), init);
  return { base: bp, ref: rp };
}

/**
 * Fill missing left/right counterparts by mirroring placed points across each
 * mesh's symmetry plane (points are snapped back onto the surface).
 */
export function mirrorLandmarks() {
  const b = baseEntry(), r = refEntry();
  if (!b || !r) return;
  const planes = symmetryPlanes()!;
  const s = get();
  pushUndo('Mirror landmarks');
  const byLabel = new Map(s.landmarks.map((l) => [l.label, l]));
  let next = s.landmarks.map((l) => ({ ...l }));
  let id = s.nextLandmarkId;
  let filled = 0;
  for (const src of s.landmarks) {
    const mn = mirrorName(src.label);
    if (!mn) continue;
    let dst = next.find((l) => l.label === mn);
    if (!dst && !byLabel.has(mn)) {
      dst = { id: id++, label: mn, group: src.group, weight: src.weight, base: null, ref: null };
      next = [...next, dst];
    }
    if (!dst) continue;
    if (src.base && !dst.base) {
      dst.base = mirrorSurfacePoint(b.loaded.mesh.positions, b.triangles, bvhFor(b), src.base, planes.base);
      filled++;
    }
    if (src.ref && !dst.ref) {
      dst.ref = mirrorSurfacePoint(r.loaded.mesh.positions, r.triangles, bvhFor(r), src.ref, planes.ref);
      filled++;
    }
  }
  set({ landmarks: next, nextLandmarkId: id });
  log('info', `Mirrored ${filled} landmark point(s) across the symmetry planes (fitted to each mesh; check them before wrapping).`);
  if (get().guided) advanceGuided(get().pendingPick?.landmarkId ?? null);
}

/** Which side of the character a guide point is on ('C' near the middle), from the mesh's symmetry plane. */
function sideOf(side: 'base' | 'ref', sp: SurfacePoint): 'L' | 'R' | 'C' {
  const planes = symmetryPlanes();
  const entry = side === 'base' ? baseEntry() : refEntry();
  if (!planes || !entry) return 'C';
  const plane = side === 'base' ? planes.base : planes.ref;
  const p = evalSurfacePoint(entry.loaded.mesh.positions, entry.triangles, sp);
  // character's left = +X (front-facing, Y up): orient the normal that way
  const n = plane.normal[0] < 0 ? plane.normal.map((v) => -v) : plane.normal;
  const d = (p[0] - plane.point[0]) * n[0] + (p[1] - plane.point[1]) * n[1] + (p[2] - plane.point[2]) * n[2];
  const tol = 0.02 * computeBBox(entry.loaded.mesh.positions).diagonal;
  return d > tol ? 'L' : d < -tol ? 'R' : 'C';
}

/** Mirror mode: a finished guide gets its twin on the other side of both meshes (centre guides have none).
 *  `changed`: the side just (re)placed, which is mirrored again even if the twin has it already. */
export function mirrorFinished(id: number, changed?: 'base' | 'ref') {
  const s = get();
  const l = s.landmarks.find((x) => x.id === id);
  const b = baseEntry(), r = refEntry();
  const planes = symmetryPlanes();
  if (!l || !l.base || !l.ref || !b || !r || !planes) return;
  let label = l.label;
  let landmarks = s.landmarks;
  if (!mirrorName(label)) {
    const where = sideOf('base', l.base);
    if (where === 'C') return;
    label = `${label} ${where}`;
    landmarks = landmarks.map((x) => (x.id === id ? { ...x, label } : x));
  }
  const twinName = mirrorName(label)!;
  let nextId = s.nextLandmarkId;
  let twin = landmarks.find((x) => x.label === twinName);
  if (!twin) {
    twin = { id: nextId++, label: twinName, group: l.group, weight: l.weight, base: null, ref: null };
    landmarks = [...landmarks, twin];
  }
  const t = twin;
  const filled: Landmark = {
    ...t,
    base: t.base && changed !== 'base' ? t.base : mirrorSurfacePoint(b.loaded.mesh.positions, b.triangles, bvhFor(b), l.base, planes.base),
    ref: t.ref && changed !== 'ref' ? t.ref : mirrorSurfacePoint(r.loaded.mesh.positions, r.triangles, bvhFor(r), l.ref, planes.ref),
  };
  set({ landmarks: landmarks.map((x) => (x.id === t.id ? filled : x)), nextLandmarkId: nextId });
}

/** A placed guide whose point on `side` is right where the user clicked (within 1.5% of the mesh size). */
function nearestGuide(side: 'base' | 'ref', sp: SurfacePoint): Landmark | null {
  const entry = side === 'base' ? baseEntry() : refEntry();
  if (!entry) return null;
  const pos = entry.loaded.mesh.positions;
  const p = evalSurfacePoint(pos, entry.triangles, sp);
  const reach = 0.015 * computeBBox(pos).diagonal;
  let best: Landmark | null = null;
  let bestD = reach;
  for (const l of get().landmarks) {
    const q = l[side];
    if (!q) continue;
    const g = evalSurfacePoint(pos, entry.triangles, q);
    const d = Math.hypot(g[0] - p[0], g[1] - p[1], g[2] - p[2]);
    if (d < bestD) {
      best = l;
      bestD = d;
    }
  }
  return best;
}

/**
 * Auto-guess: every guide placed on the Base but not on the Reference gets a first guess there,
 * the closest point of the Reference to the aligned Base point (run Align first). With Mirror on,
 * right points of named pairs come from mirroring their left point, so both sides stay symmetric.
 */
export function autoGuessGuides() {
  const b = baseEntry(), r = refEntry();
  if (!b || !r) return;
  const s = get();
  const labels = new Set(s.landmarks.map((l) => l.label));
  const todo = s.landmarks.filter((l) => l.base && !l.ref && !(s.mirrorGuides && l.label.endsWith(' R') && labels.has(l.label.slice(0, -2) + ' L')));
  if (!todo.length) return log('info', 'Every guide already has its point on the Reference.');
  pushUndo('Auto-guess guides');
  const bvh = bvhFor(r);
  const hit = makeHit();
  const guessed = new Map<number, SurfacePoint>();
  for (const l of todo) {
    const p = transformPoint(evalSurfacePoint(b.loaded.mesh.positions, b.triangles, l.base!), s.transform);
    hit.distSq = Infinity;
    if (bvh.closestPoint(p[0], p[1], p[2], Infinity, hit)) guessed.set(l.id, { tri: hit.tri, bary: [hit.u, hit.v, hit.w] });
  }
  set({ landmarks: get().landmarks.map((l) => (guessed.has(l.id) ? { ...l, ref: guessed.get(l.id)! } : l)), pendingPick: null, guided: false, tool: 'landmark' });
  if (s.mirrorGuides) for (const id of guessed.keys()) mirrorFinished(id, 'ref');
  log('info', `Guessed ${guessed.size} point(s) on the Reference from the aligned Base. Check them: drag a wrong dot to its spot.`);
}

/** The Base is Meta Mutant's MetaHuman export (its head first, in the shared MetaHuman topology). */
export function isMetaHumanBase(entry: MeshEntry | undefined = baseEntry()): boolean {
  if (!entry || entry.loaded.source.kind !== 'obj') return false;
  const header = entry.loaded.source.lines.slice(0, 4).some((line) => line.includes('MetaHuman'));
  return header && entry.loaded.mesh.positions.length / 3 >= METAHUMAN_HEAD_VERTICES;
}

/** MetaHuman mode: the face guides with their MetaHuman side already placed; only your head is asked for. */
export function addMetaHumanGuides() {
  const b = baseEntry();
  if (!b || !isMetaHumanBase(b)) return log('error', 'MetaHuman mode needs the MetaHuman export from Meta Mutant as the Base.');
  const s = get();
  pushUndo('MetaHuman guides');
  const at = (v: number): SurfacePoint | null => {
    const tris = b.triangles;
    for (let t = 0; t < tris.length; t++) {
      if (tris[t] !== v) continue;
      const bary: [number, number, number] = [0, 0, 0];
      bary[t % 3] = 1;
      return { tri: Math.floor(t / 3), bary };
    }
    return null;
  };
  let nextId = s.nextLandmarkId;
  const landmarks = s.landmarks.map((l) => ({ ...l }));
  for (const p of FACE_PRESET) {
    const v = METAHUMAN_FACE_VERTEX[p.name];
    if (v === undefined) continue;
    const existing = landmarks.find((l) => l.label === p.name);
    if (existing) {
      if (!existing.base) existing.base = at(v);
    } else landmarks.push({ id: nextId++, label: p.name, group: p.group, weight: 1, base: at(v), ref: null });
  }
  set({ landmarks, nextLandmarkId: nextId, guided: true, guideMode: 'metahuman' });
  log('info', 'MetaHuman guides placed on the MetaHuman head. Click each named point on your head' + (get().mirrorGuides ? ' (left side and centre only; the right side is mirrored).' : '.'));
  advanceGuided(landmarks.find((l) => !l.ref)?.id ?? null);
}

/** Called by the viewport when the user clicks a surface in landmark mode. */
export function pickLandmarkPoint(side: 'base' | 'ref', sp: SurfacePoint) {
  const s = get();
  const pending = s.pendingPick;
  if (s.mirrorGuides && sideOf(side, sp) === 'R') {
    const label = pending ? s.landmarks.find((l) => l.id === pending.landmarkId)?.label ?? '' : '';
    if (!label.endsWith(' R')) {
      log('warn', "Mirror is on: place guides on the character's left side (the right of the screen, seen from the front), as in Mutant Tools; the other side is mirrored for you.");
      return;
    }
  }
  pushUndo('Landmark');
  if (pending) {
    if (pending.side !== side) {
      log('warn', `Click the ${pending.side === 'base' ? 'Base' : 'Reference'} mesh to reposition this landmark.`);
      set((st) => ({ undoStack: st.undoStack.slice(0, -1) }));
      return;
    }
    set({ landmarks: s.landmarks.map((l) => (l.id === pending.landmarkId ? { ...l, [side]: sp } : l)), pendingPick: null, selectedLandmarkId: pending.landmarkId });
    if (s.mirrorGuides) mirrorFinished(pending.landmarkId, side);
    if (s.guided) advanceGuided(pending.landmarkId);
    return;
  }
  const near = nearestGuide(side, sp);
  if (near) {
    set((st) => ({ undoStack: st.undoStack.slice(0, -1), pendingPick: { landmarkId: near.id, side }, selectedLandmarkId: near.id }));
    log('info', `${near.label}: click its new spot on the ${side === 'base' ? 'Base' : 'Reference'}.`);
    return;
  }
  const open = [...s.landmarks].reverse().find((l) => l[side] === null);
  if (open) {
    set({ landmarks: s.landmarks.map((l) => (l.id === open.id ? { ...l, [side]: sp } : l)), selectedLandmarkId: open.id });
    if (s.mirrorGuides) mirrorFinished(open.id, side);
    return;
  }
  const id = s.nextLandmarkId;
  const l: Landmark = { id, label: `L${id}`, group: s.newLandmarkGroup, weight: 1, base: side === 'base' ? sp : null, ref: side === 'ref' ? sp : null };
  set({ landmarks: [...s.landmarks, l], nextLandmarkId: id + 1, selectedLandmarkId: id });
}

// ---------------------------------------------------------------- dragging a guide

let drag: { id: number; side: 'base' | 'ref'; moved: boolean } | null = null;

/** Press on a placed dot: it follows the mouse across its mesh until release (one undo step). */
export function beginGuideDrag(id: number, side: 'base' | 'ref') {
  pushUndo('Move guide');
  drag = { id, side, moved: false };
  set({ selectedLandmarkId: id, pendingPick: null });
}

/** The dragged dot is now at `sp` (no mirroring while dragging: it is applied on release). */
export function dragGuide(sp: SurfacePoint) {
  if (!drag) return;
  const { id, side } = drag;
  drag.moved = true;
  set((s) => ({ landmarks: s.landmarks.map((l) => (l.id === id ? { ...l, [side]: sp } : l)) }));
}

/**
 * Release: Mirror updates the other side. A right point of a named pair follows its left twin,
 * so the twin is moved to the mirrored spot and both sides stay symmetric.
 */
export function endGuideDrag() {
  const d = drag;
  drag = null;
  if (!d) return;
  const s = get();
  if (!d.moved) {
    set((st) => ({ undoStack: st.undoStack.slice(0, -1) }));  // a click on a dot only selects it
    return;
  }
  if (!s.mirrorGuides) return;
  const l = s.landmarks.find((x) => x.id === d.id);
  const sp = l?.[d.side];
  if (!l || !sp) return;
  const twin = l.label.endsWith(' R') ? s.landmarks.find((x) => x.label === l.label.slice(0, -2) + ' L') : undefined;
  if (!twin) return mirrorFinished(l.id, d.side);
  const entry = d.side === 'base' ? baseEntry() : refEntry();
  const planes = symmetryPlanes();
  if (!entry || !planes) return;
  const spot = mirrorSurfacePoint(entry.loaded.mesh.positions, entry.triangles, bvhFor(entry), sp, d.side === 'base' ? planes.base : planes.ref);
  set({ landmarks: s.landmarks.map((x) => (x.id === twin.id ? { ...x, [d.side]: spot } : x)) });
  mirrorFinished(twin.id, d.side);
}

export function updateLandmark(id: number, patch: Partial<Landmark>) {
  pushUndo('Edit landmark');
  set((s) => ({ landmarks: s.landmarks.map((l) => (l.id === id ? { ...l, ...patch } : l)) }));
}

export function deleteLandmark(id: number) {
  pushUndo('Delete landmark');
  set((s) => ({
    landmarks: s.landmarks.filter((l) => l.id !== id),
    selectedLandmarkId: s.selectedLandmarkId === id ? null : s.selectedLandmarkId,
    pendingPick: s.pendingPick?.landmarkId === id ? null : s.pendingPick,
  }));
}

export function clearLandmarks() {
  if (!get().landmarks.length) return;
  pushUndo('Clear landmarks');
  set({ landmarks: [], selectedLandmarkId: null, pendingPick: null });
}

export function repickLandmark(id: number, side: 'base' | 'ref') {
  set({ pendingPick: { landmarkId: id, side }, tool: 'landmark', selectedLandmarkId: id });
}

export function toggleGroupVisibility(g: LandmarkGroup) {
  set((s) => ({ hiddenGroups: s.hiddenGroups.includes(g) ? s.hiddenGroups.filter((x) => x !== g) : [...s.hiddenGroups, g] }));
}

// ---------------------------------------------------------------- regions

let strokeActive = false;

export function beginStroke() {
  const b = baseEntry();
  if (!b) return;
  pushUndo('Paint region');
  const s = get();
  const n = b.loaded.mesh.positions.length / 3;
  set({ mask: s.mask ? s.mask.slice() : new Float32Array(n) });
  strokeActive = true;
}

export function strokeAt(center: [number, number, number]) {
  const s = get();
  const b = baseEntry(s);
  const pos = baseCurrentPositions(s);
  if (!strokeActive || !b || !pos || !s.mask) return;
  const diag = computeBBox(pos).diagonal;
  paintSphere(s.mask, pos, center, s.brush.radius * diag, s.brush.erase ? 0 : 1, s.brush.hardness);
  set({ maskVersion: s.maskVersion + 1 });
}

export function endStroke() {
  strokeActive = false;
}

export function maskOp(op: 'invert' | 'grow' | 'shrink' | 'smooth' | 'clear' | 'fill') {
  const s = get();
  const b = baseEntry(s);
  if (!b) return;
  const n = b.loaded.mesh.positions.length / 3;
  pushUndo(`Region: ${op}`);
  if (op === 'clear') return set({ mask: null });
  const m = s.mask ? s.mask.slice() : new Float32Array(n);
  const adj = baseAdjacency(b);
  if (op === 'invert') invertMask(m);
  else if (op === 'grow') growMask(m, adj, true);
  else if (op === 'shrink') growMask(m, adj, false);
  else if (op === 'smooth') smoothMask(m, adj, 2);
  else if (op === 'fill') m.fill(1);
  set({ mask: m });
}

// ---------------------------------------------------------------- analysis & export

export async function setHeatmap(mode: HeatmapMode) {
  set((s) => ({ display: { ...s.display, heatmap: mode } }));
  if (mode === 'none') return set({ heat: null });
  const s = get();
  const b = baseEntry(s), r = refEntry(s);
  const cur = baseCurrentPositions(s);
  if (!b || !cur) return;
  if (mode === 'displacement') {
    const rest = baseRestPositions(s)!;
    const n = rest.length / 3;
    const v = new Float32Array(n);
    let mx = 0;
    for (let i = 0; i < n; i++) {
      v[i] = Math.hypot(cur[i * 3] - rest[i * 3], cur[i * 3 + 1] - rest[i * 3 + 1], cur[i * 3 + 2] - rest[i * 3 + 2]);
      mx = Math.max(mx, v[i]);
    }
    set({ heat: { values: v, max: mx || 1, label: 'Displacement from aligned original', mode } });
    return;
  }
  if (!r) return log('warn', 'Distance heatmap needs a Reference mesh.');
  if (!requireIdle('Heatmap')) return;
  set({ job: { kind: 'measure', label: 'Measuring', progress: 0, message: 'Distance to reference', startedAt: performance.now(), cancellable: false } });
  try {
    const res = await engine.measure({ points: cur, targetKey: { id: r.id, version: r.version }, targetPositions: r.loaded.mesh.positions, targetTriangles: r.triangles });
    set({ heat: { values: Float32Array.from(res.perPoint), max: Math.max(res.stats.p95, 1e-12), label: 'Distance to reference surface', mode } });
    log('info', `Distance to reference (measured at ${res.stats.count.toLocaleString()} vertices): mean ${fmtLen(res.stats.mean)}, 95th pct ${fmtLen(res.stats.p95)}, max ${fmtLen(res.stats.max)}.`);
  } catch (e) {
    log('error', `Measurement failed: ${(e as Error).message}`);
  } finally {
    set({ job: null });
  }
}

function download(data: BlobPart, mime: string, fileName: string) {
  const url = URL.createObjectURL(new Blob([data], { type: mime }));
  const a = document.createElement('a');
  a.href = url;
  a.download = fileName;
  document.body.appendChild(a);
  a.click();
  a.remove();
  setTimeout(() => URL.revokeObjectURL(url), 10000);
}

/** Export the result as OBJ: sent to Maya (the bridge that opened this page) or downloaded. */
export async function exportBase(space: ExportSpace, toMaya = !!get().returnUrl) {
  const format: ExportFormat = 'obj';
  const s = get();
  const b = baseEntry(s);
  if (!b) return log('warn', 'Nothing to export: load a Base mesh.');
  if (s.preview) return log('warn', 'Commit or discard the preview before exporting.');
  if (!requireIdle('Export')) return;
  const positions = s.committed ?? baseRestPositions(s)!;
  set({ job: { kind: 'export', label: 'Exporting', progress: 0, message: 'Writing and validating topology', startedAt: performance.now(), cancellable: false } });
  try {
    const res = await engine.exportMesh({ base: b.loaded, positions, transform: s.transform, format, space });
    let sent = false;
    if (toMaya && s.returnUrl) {
      set({ job: { kind: 'export', label: 'Exporting', progress: 0.9, message: 'Sending to Maya', startedAt: performance.now(), cancellable: false } });
      try {
        const msg = await postResult(s.returnUrl, res.data);
        log('info', `Sent ${res.fileName} to Maya${msg ? `: ${msg}` : '.'}`);
        sent = true;
      } catch (e) {
        log('error', `Could not send ${res.fileName} to Maya (${(e as Error).message}); downloading it instead.`);
      }
    }
    if (!sent) download(res.data, res.mime, res.fileName);
    const c = res.check;
    log(
      'info',
      `Exported ${res.fileName}: topology check passed — vertices ${c.vertexCount[0]} = ${c.vertexCount[1]}, faces ${c.faceCount[0]} = ${c.faceCount[1]}, corners ${c.cornerCount[0]} = ${c.cornerCount[1]}, identical face indices; max position round-off ${c.maxPositionError.toExponential(2)}.`,
    );
    for (const n of res.notes) log('info', `  ${n}`);
    if (!s.committed) log('info', '  No committed deformation: exported the aligned (rigidly placed) base.');
  } catch (e) {
    log('error', `Export failed: ${(e as Error).message}`);
  } finally {
    set({ job: null });
  }
}

