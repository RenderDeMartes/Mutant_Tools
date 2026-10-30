import { useEffect, useRef } from 'react';
import { SceneController, requestFrame } from './SceneController';
import { set, useStore } from '../../state/store';
import { Segmented } from '../components/controls';
import { HEAT_GRADIENT_CSS } from '../theme';
import { setHeatmap } from '../../state/actions';
import { fmtLen } from '../format';

let controller: SceneController | null = null;
export const getController = () => controller;

export function Viewport() {
  const ref = useRef<HTMLDivElement>(null);
  useEffect(() => {
    controller = new SceneController(ref.current!);
    // expose for automated checks / debugging in the browser console
    (window as unknown as { __topo?: unknown }).__topo = { controller };
    return () => {
      controller?.dispose();
      controller = null;
    };
  }, []);
  return (
    <div className="viewport">
      <div className="viewport-canvas" ref={ref} />
      <ViewportOverlay />
    </div>
  );
}

function ViewportOverlay() {
  const display = useStore((s) => s.display);
  const tool = useStore((s) => s.tool);
  const sculptMode = useStore((s) => s.sculpt.mode);
  const preview = useStore((s) => !!s.preview);
  const committed = useStore((s) => !!s.committed);
  const heat = useStore((s) => s.heat);
  const hasMeshes = useStore((s) => s.meshes.length > 0);
  const pending = useStore((s) => s.pendingPick);
  const pendingLabel = useStore((s) => (s.pendingPick ? s.landmarks.find((l) => l.id === s.pendingPick!.landmarkId)?.label : undefined));
  const setDisplay = (patch: Partial<typeof display>) => set((s) => ({ display: { ...s.display, ...patch } }));
  return (
    <>
      <div className="vp-toolbar">
        <Segmented
          value={display.mode}
          onChange={(m) => setDisplay({ mode: m })}
          options={[
            { value: 'shaded', label: 'Shaded', hint: '1' },
            { value: 'wire', label: 'Wire', hint: '2' },
            { value: 'shadedWire', label: 'Shaded+Wire', hint: '3' },
          ]}
        />
        <span className="vp-sep" />
        <button className={`vp-toggle ${display.showReference ? 'on' : ''}`} onClick={() => setDisplay({ showReference: !display.showReference })} title="Show Reference (N)">
          Reference
        </button>
        {display.showReference && (
          <input className="vp-opacity" type="range" min={0.05} max={1} step={0.01} value={display.refOpacity} onChange={(e) => setDisplay({ refOpacity: parseFloat(e.target.value) })} title="Reference opacity (X)" />
        )}
        <button className={`vp-toggle ${display.showOriginal ? 'on' : ''}`} onClick={() => setDisplay({ showOriginal: !display.showOriginal })} title="Overlay the undeformed Base (O)">
          Original
        </button>
        <span className="vp-sep" />
        <Segmented
          value={display.heatmap}
          onChange={(m) => void setHeatmap(m)}
          options={[
            { value: 'none', label: 'Plain' },
            { value: 'distance', label: 'Distance', hint: 'Distance to the Reference surface (H)' },
            { value: 'displacement', label: 'Moved', hint: 'How far each vertex moved' },
          ]}
        />
        <button className="btn small ghost" onClick={requestFrame} title="Frame all (F)">
          Frame
        </button>
      </div>
      <div className="vp-badges">
        {preview && <span className="vp-badge preview">PREVIEW — not committed</span>}
        {!preview && committed && <span className="vp-badge committed">Committed result</span>}
        {tool !== 'navigate' && (
          <span className="vp-badge tool">
            {tool === 'landmark' ? (pending ? `Click ${pendingLabel ?? 'landmark'} on the ${pending.side === 'base' ? 'Base' : 'Reference'}` : 'Landmark tool') : tool === 'sculpt' ? `Brush: ${sculptMode}` : 'Paint tool'} · Esc to exit
          </span>
        )}
      </div>
      {heat && (
        <div className="vp-legend">
          <div className="legend-bar" style={{ background: HEAT_GRADIENT_CSS }} />
          <div className="legend-labels">
            <span>0</span>
            <span>{heat.label}</span>
            <span>≥ {fmtLen(heat.max)}</span>
          </div>
        </div>
      )}
      {!hasMeshes && (
        <div className="vp-empty">
          <div>
            <h2>Drop meshes here</h2>
            <p>Base = topology to keep · Reference = shape to match — or pick an example on the right.</p>
          </div>
        </div>
      )}
      <div className="vp-axes muted small">Y up · left orbit · right pan · wheel zoom</div>
    </>
  );
}
