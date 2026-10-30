/**
 * Stable engine interface. The UI talks only to this interface; it is
 * implemented by a Web Worker client today and could be implemented by an
 * HTTP client to an optional Python backend later without UI changes.
 *
 * All types are plain data (typed arrays + JSON-compatible objects) so they can
 * be structured-cloned across a worker boundary or serialised.
 */

import type { ICPOptions, ICPResult } from './alignment/rigid';
import type { ExportRequest, ExportResult } from './export/exporter';
import type { ValidationReport } from './geometry/validation';
import type { LoadedMesh, MeshRole } from './io/load';
import type { Landmark } from './landmarks/landmarks';
import type { DistanceStats } from './validation/metrics';
import type { WrapParams } from './wrapping/params';
import type { WrapProgress, WrapResult } from './wrapping/nricp';

export interface LoadMeshResult {
  loaded: LoadedMesh;
  validation: ValidationReport;
  triangles: Uint32Array;
  triFace: Uint32Array;
  parseMs: number;
}

/** Identifies cached per-mesh precomputation (BVH, adjacency, multigrid). */
export interface MeshKey {
  id: string;
  /** bump when topology changes (it never does for a loaded mesh, but keeps caches honest) */
  version: number;
}

export interface WrapJob {
  baseKey: MeshKey;
  refKey: MeshKey;
  baseRest: Float64Array;
  baseStart: Float64Array;
  baseTriangles: Uint32Array;
  refPositions: Float64Array;
  refTriangles: Uint32Array;
  landmarks: Landmark[];
  mask: Float32Array | null;
  componentModes: import('./constraints/components').ComponentMode[] | null;
  params: WrapParams;
}

export interface ICPJob {
  refKey: MeshKey;
  /** untransformed base positions */
  basePositions: Float64Array;
  initialTransform: Float64Array;
  refPositions: Float64Array;
  refTriangles: Uint32Array;
  options: ICPOptions;
}

export interface MeasureJob {
  /** distances are measured from these points to the target surface */
  points: Float64Array;
  targetKey: MeshKey;
  targetPositions: Float64Array;
  targetTriangles: Uint32Array;
}

export interface MeasureResult {
  perPoint: Float64Array;
  stats: DistanceStats;
}

export interface GeometryEngine {
  loadMesh(name: string, buffer: ArrayBuffer, role: MeshRole): Promise<LoadMeshResult>;
  icp(job: ICPJob): Promise<ICPResult>;
  wrap(job: WrapJob, onProgress?: (p: WrapProgress) => void): Promise<WrapResult>;
  measure(job: MeasureJob): Promise<MeasureResult>;
  exportMesh(req: ExportRequest): Promise<ExportResult>;
  /** Request cancellation of the running wrap/ICP. Resolves when the engine is idle again. */
  cancel(): Promise<void>;
}
