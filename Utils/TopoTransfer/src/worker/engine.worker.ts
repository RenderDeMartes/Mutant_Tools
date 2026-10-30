/// <reference lib="webworker" />
/**
 * Geometry engine worker. Runs every expensive operation off the UI thread.
 * Messages: { id, type, payload } → { id, type: 'result' | 'error' | 'progress', ... }.
 */

import { icpAlign } from '../engine/alignment/rigid';
import { exportMesh } from '../engine/export/exporter';
import { validateMesh } from '../engine/geometry/validation';
import { loadMeshFile } from '../engine/io/load';
import { triangulate } from '../engine/core/mesh';
import { TriangleBVH } from '../engine/spatial/bvh';
import { pointToSurfaceDistances } from '../engine/validation/metrics';
import { wrapMesh } from '../engine/wrapping/nricp';
import { BasePrep, prepareBase, prepareReference, RefPrep } from '../engine/wrapping/prepare';
import type { ICPJob, LoadMeshResult, MeasureJob, MeshKey, WrapJob } from '../engine/api';
import type { ExportRequest } from '../engine/export/exporter';
import type { MeshRole } from '../engine/io/load';

declare const self: DedicatedWorkerGlobalScope;

type Req =
  | { id: number; type: 'load'; payload: { name: string; buffer: ArrayBuffer; role: MeshRole } }
  | { id: number; type: 'icp'; payload: ICPJob }
  | { id: number; type: 'wrap'; payload: WrapJob }
  | { id: number; type: 'measure'; payload: MeasureJob }
  | { id: number; type: 'export'; payload: ExportRequest }
  | { id: number; type: 'cancel' };

const keyStr = (k: MeshKey, extra = '') => `${k.id}#${k.version}${extra}`;
let refCache: { key: string; prep: RefPrep } | null = null;
let baseCache: { key: string; prep: BasePrep } | null = null;
let bvhCache: { key: string; bvh: TriangleBVH } | null = null;
let cancelRequested = false;

function getRefPrep(key: MeshKey, positions: Float64Array, triangles: Uint32Array): RefPrep {
  const k = keyStr(key);
  if (refCache?.key !== k) refCache = { key: k, prep: prepareReference(positions, triangles) };
  return refCache.prep;
}

function getBVH(key: MeshKey, positions: Float64Array, triangles: Uint32Array): TriangleBVH {
  const k = keyStr(key);
  if (refCache?.key === k) return refCache.prep.bvh;
  if (bvhCache?.key !== k) bvhCache = { key: k, bvh: TriangleBVH.build(positions, triangles) };
  return bvhCache.bvh;
}

const yieldControl = () => new Promise<void>((resolve) => setTimeout(resolve, 0));

self.onmessage = async (ev: MessageEvent<Req>) => {
  const msg = ev.data;
  if (msg.type === 'cancel') {
    cancelRequested = true;
    return;
  }
  const { id } = msg;
  try {
    switch (msg.type) {
      case 'load': {
        const t0 = performance.now();
        const loaded = loadMeshFile(msg.payload.name, msg.payload.buffer, msg.payload.role);
        const validation = validateMesh(loaded.mesh, msg.payload.role);
        const tri = triangulate(loaded.mesh);
        const result: LoadMeshResult = { loaded, validation, triangles: tri.triangles, triFace: tri.triFace, parseMs: performance.now() - t0 };
        self.postMessage({ id, type: 'result', result });
        break;
      }
      case 'icp': {
        const j = msg.payload;
        const bvh = getBVH(j.refKey, j.refPositions, j.refTriangles);
        const result = icpAlign(j.basePositions, j.initialTransform, bvh, j.options);
        self.postMessage({ id, type: 'result', result });
        break;
      }
      case 'wrap': {
        cancelRequested = false;
        const j = msg.payload;
        const refPrep = getRefPrep(j.refKey, j.refPositions, j.refTriangles);
        const bk = keyStr(j.baseKey, `|seam=${j.params.seamLock}`);
        if (baseCache?.key !== bk) {
          self.postMessage({ id, type: 'progress', progress: { stage: 'setup', level: 0, levels: j.params.levels, iteration: 0, iterationsPerLevel: j.params.iterationsPerLevel, fraction: 0, message: 'Building solver structures (multigrid, BVH)' } });
          await yieldControl();
          baseCache = { key: bk, prep: prepareBase(j.baseRest, j.baseTriangles, j.params.seamLock) };
        }
        const result = await wrapMesh(
          {
            baseRest: j.baseRest,
            baseStart: j.baseStart,
            baseTriangles: j.baseTriangles,
            refPositions: j.refPositions,
            refTriangles: j.refTriangles,
            landmarks: j.landmarks,
            mask: j.mask,
            componentModes: j.componentModes,
            params: j.params,
          },
          {
            basePrep: baseCache.prep,
            refPrep,
            isCancelled: () => cancelRequested,
            yieldControl,
            onProgress: (progress) => self.postMessage({ id, type: 'progress', progress }),
          },
        );
        self.postMessage({ id, type: 'result', result }, [result.positions.buffer]);
        break;
      }
      case 'measure': {
        const j = msg.payload;
        const bvh = getBVH(j.targetKey, j.targetPositions, j.targetTriangles);
        const perPoint = new Float64Array(j.points.length / 3);
        const stats = pointToSurfaceDistances(j.points, bvh, undefined, perPoint);
        self.postMessage({ id, type: 'result', result: { perPoint, stats } }, [perPoint.buffer]);
        break;
      }
      case 'export': {
        const result = exportMesh(msg.payload);
        self.postMessage({ id, type: 'result', result }, [result.data]);
        break;
      }
    }
  } catch (e) {
    self.postMessage({ id, type: 'error', message: e instanceof Error ? e.message : String(e) });
  }
};
