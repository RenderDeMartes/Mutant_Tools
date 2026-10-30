/**
 * GeometryEngine implementation backed by a dedicated Web Worker.
 *
 * Cancellation is cooperative (the solver checks a flag between iterations).
 * If the worker does not acknowledge within a grace period the worker is
 * terminated and recreated, so the UI can always recover. No geometry is ever
 * sent anywhere except this local worker.
 */

import type { GeometryEngine, ICPJob, LoadMeshResult, MeasureJob, MeasureResult, WrapJob } from '../engine/api';
import type { ICPResult } from '../engine/alignment/rigid';
import type { ExportRequest, ExportResult } from '../engine/export/exporter';
import type { MeshRole } from '../engine/io/load';
import type { WrapProgress, WrapResult } from '../engine/wrapping/nricp';

interface Pending {
  resolve: (v: unknown) => void;
  reject: (e: Error) => void;
  onProgress?: (p: WrapProgress) => void;
  kind: string;
}

export class CancelledError extends Error {
  constructor() {
    super('Operation cancelled.');
  }
}

export class WorkerEngine implements GeometryEngine {
  private worker!: Worker;
  private nextId = 1;
  private pending = new Map<number, Pending>();

  constructor() {
    this.spawn();
  }

  private spawn() {
    this.worker = new Worker(new URL('./engine.worker.ts', import.meta.url), { type: 'module' });
    this.worker.onmessage = (ev: MessageEvent) => {
      const msg = ev.data as { id: number; type: string; result?: unknown; message?: string; progress?: WrapProgress };
      const p = this.pending.get(msg.id);
      if (!p) return;
      if (msg.type === 'progress') {
        p.onProgress?.(msg.progress!);
        return;
      }
      this.pending.delete(msg.id);
      if (msg.type === 'result') p.resolve(msg.result);
      else p.reject(new Error(msg.message ?? 'Engine error'));
    };
    this.worker.onerror = (ev) => {
      const err = new Error(`Engine worker crashed: ${ev.message || 'unknown error'}`);
      for (const p of this.pending.values()) p.reject(err);
      this.pending.clear();
      this.worker.terminate();
      this.spawn();
    };
  }

  private call<T>(type: string, payload: unknown, transfer: Transferable[] = [], onProgress?: (p: WrapProgress) => void): Promise<T> {
    const id = this.nextId++;
    return new Promise<T>((resolve, reject) => {
      this.pending.set(id, { resolve: resolve as (v: unknown) => void, reject, onProgress, kind: type });
      this.worker.postMessage({ id, type, payload }, transfer);
    });
  }

  get busy(): boolean {
    return Array.from(this.pending.values()).some((p) => p.kind === 'wrap' || p.kind === 'icp');
  }

  loadMesh(name: string, buffer: ArrayBuffer, role: MeshRole): Promise<LoadMeshResult> {
    return this.call('load', { name, buffer, role }, [buffer]);
  }

  icp(job: ICPJob): Promise<ICPResult> {
    return this.call('icp', job);
  }

  wrap(job: WrapJob, onProgress?: (p: WrapProgress) => void): Promise<WrapResult> {
    return this.call('wrap', job, [], onProgress);
  }

  measure(job: MeasureJob): Promise<MeasureResult> {
    return this.call('measure', job);
  }

  exportMesh(req: ExportRequest): Promise<ExportResult> {
    return this.call('export', req);
  }

  async cancel(): Promise<void> {
    if (!this.busy) return;
    this.worker.postMessage({ type: 'cancel' });
    const deadline = performance.now() + 4000;
    while (this.busy && performance.now() < deadline) {
      await new Promise((r) => setTimeout(r, 50));
    }
    if (this.busy) {
      // hard stop: the solver is inside a long linear solve
      this.worker.terminate();
      for (const p of this.pending.values()) p.reject(new CancelledError());
      this.pending.clear();
      this.spawn();
    }
  }
}
