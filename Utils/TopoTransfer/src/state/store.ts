/**
 * Application state (zustand). Large geometry lives in typed arrays that are
 * replaced (never mutated in place) so subscribers can detect changes by
 * reference.
 */

import { create } from 'zustand';
import type { ValidationReport } from '../engine/geometry/validation';
import type { LoadedMesh } from '../engine/io/load';
import type { Landmark, LandmarkGroup } from '../engine/landmarks/landmarks';
import { mat4Identity, transformPositions } from '../engine/core/mat3';
import { DEFAULT_WRAP_PARAMS, WrapParams } from '../engine/wrapping/params';
import type { WrapProgress, WrapResult } from '../engine/wrapping/nricp';
import type { ComponentMode } from '../engine/constraints/components';

export type MeshRoleUI = 'base' | 'reference' | null;

export interface MeshEntry {
  id: string;
  name: string;
  loaded: LoadedMesh;
  validation: ValidationReport;
  triangles: Uint32Array;
  triFace: Uint32Array;
  /** unique polygon edges (pairs) for quad-aware wireframe */
  polyEdges: Uint32Array;
  visible: boolean;
  role: MeshRoleUI;
  version: number;
}

export type DisplayMode = 'shaded' | 'wire' | 'shadedWire';
export type Tool = 'navigate' | 'landmark' | 'paint' | 'sculpt';
export type HeatmapMode = 'none' | 'distance' | 'displacement';
export type GizmoMode = 'off' | 'translate' | 'rotate' | 'scale';

/** Scene units, used only for display (distances are shown in mm when known). */
export type Units = 'm' | 'cm' | 'mm' | 'none';

export interface LogEntry {
  t: number;
  level: 'info' | 'warn' | 'error';
  text: string;
}

export interface Job {
  kind: 'load' | 'icp' | 'wrap' | 'export' | 'measure';
  label: string;
  progress: number;
  message: string;
  startedAt: number;
  wrapProgress?: WrapProgress;
  cancellable: boolean;
}

export interface Snapshot {
  label: string;
  transform: Float64Array;
  committed: Float64Array | null;
  committedResult: WrapResult | null;
  landmarks: Landmark[];
  mask: Float32Array | null;
}

export interface Heat {
  values: Float32Array;
  max: number;
  label: string;
  mode: HeatmapMode;
}

export interface AppState {
  meshes: MeshEntry[];
  transform: Float64Array;
  committed: Float64Array | null;
  committedResult: WrapResult | null;
  preview: { positions: Float64Array; result: WrapResult } | null;
  landmarks: Landmark[];
  nextLandmarkId: number;
  selectedLandmarkId: number | null;
  pendingPick: { landmarkId: number; side: 'base' | 'ref' } | null;
  /** guided placement: after each pick, advance to the next missing landmark side */
  guided: boolean;
  /** guides: place the character's right side only, the left side is mirrored */
  mirrorGuides: boolean;
  /** guides: free clicking, or MetaHuman (the MetaHuman points are pre-placed) */
  guideMode: 'free' | 'metahuman';
  newLandmarkGroup: LandmarkGroup;
  hiddenGroups: LandmarkGroup[];
  showLandmarks: boolean;
  /** guide dot size, times the default */
  guideSize: number;
  mask: Float32Array | null;
  /** per base component; null = automatic defaults */
  componentModes: ComponentMode[] | null;
  /** bumped on in-place mask edits during a paint stroke */
  maskVersion: number;
  brush: { radius: number; hardness: number; erase: boolean };
  /** the Brush step (src/state/sculpt.ts); radius as a fraction of the Base size */
  sculpt: { mode: 'move' | 'sculpt' | 'smooth' | 'relax'; radius: number; strength: number; mirror: boolean };
  params: WrapParams;
  display: {
    mode: DisplayMode;
    showBase: boolean;
    showReference: boolean;
    showOriginal: boolean;
    refOpacity: number;
    heatmap: HeatmapMode;
    gizmo: GizmoMode;
    showMask: boolean;
  };
  tool: Tool;
  job: Job | null;
  log: LogEntry[];
  heat: Heat | null;
  undoStack: Snapshot[];
  redoStack: Snapshot[];
  bottomTab: 'log' | 'validation' | 'iterations';
  drawerOpen: boolean;
  units: Units;
  exportFormat: 'obj' | 'ply';
  exportSpace: 'reference' | 'original';
  /** loopback URL that Export POSTs the OBJ to (from the `return` launch parameter), instead of downloading */
  returnUrl: string | null;
  /** the page takes commands from Claude Code through the Maya bridge (src/claude/link.ts) */
  claudeLink: boolean;
  /** alignment may scale the Base uniformly */
  allowScale: boolean;
  helpOpen: boolean;
  frameRequest: number;
}

export const useStore = create<AppState>(() => ({
  meshes: [],
  transform: mat4Identity(),
  committed: null,
  committedResult: null,
  preview: null,
  landmarks: [],
  nextLandmarkId: 1,
  selectedLandmarkId: null,
  pendingPick: null,
  guided: false,
  mirrorGuides: true,
  guideMode: 'free',
  newLandmarkGroup: 'face',
  hiddenGroups: [],
  showLandmarks: true,
  guideSize: 1,
  mask: null,
  componentModes: null,
  maskVersion: 0,
  brush: { radius: 0.06, hardness: 0.5, erase: false },
  sculpt: { mode: 'move', radius: 0.03, strength: 0.5, mirror: true },
  params: { ...DEFAULT_WRAP_PARAMS },
  display: {
    mode: 'shaded',
    showBase: true,
    showReference: true,
    showOriginal: false,
    refOpacity: 0.45,
    heatmap: 'none',
    gizmo: 'off',
    showMask: true,
  },
  tool: 'navigate',
  job: null,
  log: [],
  heat: null,
  undoStack: [],
  redoStack: [],
  bottomTab: 'log',
  drawerOpen: false,
  units: 'none',
  exportFormat: 'obj',
  exportSpace: 'reference',
  returnUrl: null,
  claudeLink: false,
  allowScale: true,
  helpOpen: false,
  frameRequest: 0,
}));

export const get = () => useStore.getState();
export const set = (partial: Partial<AppState> | ((s: AppState) => Partial<AppState>)) => useStore.setState(partial);

export function baseEntry(s: AppState = get()): MeshEntry | undefined {
  return s.meshes.find((m) => m.role === 'base');
}

export function refEntry(s: AppState = get()): MeshEntry | undefined {
  return s.meshes.find((m) => m.role === 'reference');
}

let restCache: { mesh: MeshEntry; transform: Float64Array; positions: Float64Array } | null = null;

/** Rigidly placed (aligned) base positions in reference space. */
export function baseRestPositions(s: AppState = get()): Float64Array | null {
  const b = baseEntry(s);
  if (!b) return null;
  if (restCache && restCache.mesh === b && restCache.transform === s.transform) return restCache.positions;
  const positions = transformPositions(b.loaded.mesh.positions, s.transform);
  restCache = { mesh: b, transform: s.transform, positions };
  return positions;
}

/** What the base currently looks like: preview > committed > aligned rest. */
export function baseCurrentPositions(s: AppState = get()): Float64Array | null {
  if (s.preview) return s.preview.positions;
  if (s.committed) return s.committed;
  return baseRestPositions(s);
}

export function log(level: LogEntry['level'], text: string) {
  set((s) => ({ log: [...s.log.slice(-499), { t: Date.now(), level, text }] }));
}

export function snapshot(label: string): Snapshot {
  const s = get();
  return { label, transform: s.transform, committed: s.committed, committedResult: s.committedResult, landmarks: s.landmarks, mask: s.mask };
}

/** Record the current state for undo before a change. */
export function pushUndo(label: string) {
  const snap = snapshot(label);
  set((s) => ({ undoStack: [...s.undoStack.slice(-39), snap], redoStack: [] }));
}

function restore(snap: Snapshot) {
  const s = get();
  // placing guides: undoing a point asks for that point again
  let pendingPick: AppState['pendingPick'] = null;
  if (s.tool === 'landmark' && s.guided) {
    for (const l of snap.landmarks) {
      if (!l.base || !l.ref) {
        pendingPick = { landmarkId: l.id, side: l.base ? 'ref' : 'base' };
        break;
      }
    }
  }
  set({
    transform: snap.transform,
    committed: snap.committed,
    committedResult: snap.committedResult,
    landmarks: snap.landmarks,
    mask: snap.mask,
    maskVersion: s.maskVersion + 1,
    heat: null,
    pendingPick,
  });
}

export function undo() {
  const s = get();
  if (s.job || s.preview) return;
  const snap = s.undoStack[s.undoStack.length - 1];
  if (!snap) return;
  const current = snapshot(snap.label);
  set({ undoStack: s.undoStack.slice(0, -1), redoStack: [...s.redoStack, current] });
  restore(snap);
  log('info', `Undo: ${snap.label}`);
}

export function redo() {
  const s = get();
  if (s.job || s.preview) return;
  const snap = s.redoStack[s.redoStack.length - 1];
  if (!snap) return;
  const current = snapshot(snap.label);
  set({ redoStack: s.redoStack.slice(0, -1), undoStack: [...s.undoStack, current] });
  restore(snap);
  log('info', `Redo: ${snap.label}`);
}
