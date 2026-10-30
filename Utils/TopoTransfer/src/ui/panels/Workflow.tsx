/**
 * The whole editing UI as one guided sidebar: 1 Meshes → 2 Align →
 * 3 Guides → 4 Fit → 5 Export. Each step shows only its essential
 * controls; everything else sits behind a "More" disclosure.
 */

import { ReactNode, useMemo, useRef, useState } from 'react';
import * as THREE from 'three';
import { LANDMARK_GROUPS, LandmarkGroup } from '../../engine/landmarks/landmarks';
import { presetHint } from '../../engine/landmarks/presets';
import { maskCoverage } from '../../engine/constraints/mask';
import { DEFAULT_WRAP_PARAMS, QUALITY_PRESETS, qualityOf, Quality } from '../../engine/wrapping/params';
import {
  addMetaHumanGuides,
  autoGuessGuides,
  addPreset,
  alignLandmarks,
  autoAlignAndRefine,
  cancelJob,
  clearLandmarks,
  commitPreview,
  deleteLandmark,
  discardPreview,
  effectiveComponentModes,
  estimateWrapSeconds,
  exportBase,
  isMetaHumanBase,
  loadFiles,
  maskOp,
  meshComponents,
  mirrorLandmarks,
  removeMesh,
  repickLandmark,
  resetDeformation,
  resetParams,
  resetTransform,
  runWrap,
  setComponentMode,
  setParams,
  setTool,
  setTransform,
  skipGuided,
  startGuided,
  swapRoles,
  toggleVisible,
  updateLandmark,
} from '../../state/actions';
import { baseEntry, MeshEntry, refEntry, set, Units, useStore } from '../../state/store';
import { runClaudeLink } from '../../claude/link';
import { Kbd, NumberInput, Segmented, Slider, Toggle } from '../components/controls';
import { pairColor } from '../theme';
import { ExampleItems } from '../TopBar';
import { fmtLen } from '../format';

export function Workflow() {
  const hasBase = useStore((s) => !!baseEntry(s));
  const hasRef = useStore((s) => !!refEntry(s));
  const aligned = useStore((s) => !isIdentity(s.transform) || !!s.committed);
  const wrapped = useStore((s) => !!s.committed);
  const preview = useStore((s) => !!s.preview);
  const both = hasBase && hasRef;
  const placing = useStore((s) => s.tool === 'landmark');
  const guides = useStore((s) => s.landmarks.filter((l) => l.base && l.ref).length);
  const brushing = useStore((s) => s.tool === 'sculpt');
  // after Align, Guides is next until 3 pairs are placed (Fit stays usable at any time)
  const active = !both ? 1 : !aligned ? 2 : placing || (guides < 3 && !wrapped && !preview) ? 3 : !wrapped && !preview ? 4 : 5;
  return (
    <aside className="panel sidebar">
      <Step n={1} title="Meshes" state={both ? 'done' : 'active'}>
        <MeshStep />
      </Step>
      <Step n={2} title="Align" state={!both ? 'todo' : active === 2 ? 'active' : 'done'}>
        <AlignStep />
      </Step>
      <Step n={3} title="Guides" optional state={!both || !aligned ? 'todo' : active === 3 ? 'active' : guides >= 3 ? 'done' : 'optional'}>
        <LandmarkStep />
      </Step>
      <Step n={4} title="Fit" state={!both ? 'todo' : active === 4 || preview ? 'active' : wrapped ? 'done' : 'todo'}>
        <WrapStep />
      </Step>
      <Step n={5} title="Brush" optional state={!wrapped || preview ? 'todo' : brushing ? 'active' : 'optional'}>
        <BrushStep />
      </Step>
      <Step n={6} title="Export" state={!hasBase ? 'todo' : wrapped && !preview && !brushing ? 'active' : 'todo'}>
        <ExportStep />
      </Step>
    </aside>
  );
}

function isIdentity(t: Float64Array) {
  for (let i = 0; i < 16; i++) if (Math.abs(t[i] - (i % 5 === 0 ? 1 : 0)) > 1e-12) return false;
  return true;
}

function Step(props: { n: number; title: string; state: 'todo' | 'active' | 'done' | 'optional'; optional?: boolean; children: ReactNode }) {
  return (
    <section className={`step step-${props.state}`}>
      <header className="step-head">
        <span className="step-num">{props.state === 'done' ? '✓' : props.n}</span>
        <span className="step-title">{props.title}</span>
        {props.optional && <span className="step-opt">optional</span>}
      </header>
      <div className="step-body">{props.children}</div>
    </section>
  );
}

function More(props: { label: string; children: ReactNode; open?: boolean }) {
  const [open, setOpen] = useState(props.open ?? false);
  return (
    <div className={`more ${open ? 'open' : ''}`}>
      <button className="more-toggle" onClick={() => setOpen(!open)}>
        <span className="chev">▸</span> {props.label}
      </button>
      {open && <div className="more-body">{props.children}</div>}
    </div>
  );
}

// ------------------------------------------------------------------ 1. meshes

function MeshStep() {
  const meshes = useStore((s) => s.meshes);
  const job = useStore((s) => s.job);
  const units = useStore((s) => s.units);
  const fileRef = useRef<HTMLInputElement>(null);
  const base = meshes.find((m) => m.role === 'base');
  const ref = meshes.find((m) => m.role === 'reference');
  const others = meshes.filter((m) => !m.role);
  return (
    <>
      <input
        ref={fileRef}
        id="file-input"
        type="file"
        multiple
        accept=".obj,.ply,.stl"
        style={{ display: 'none' }}
        onChange={(e) => {
          const files = Array.from(e.target.files ?? []);
          e.target.value = '';
          if (files.length) void loadFiles(files);
        }}
      />
      {meshes.length === 0 ? (
        <>
          <button className="btn primary wide" disabled={!!job} onClick={() => fileRef.current?.click()}>
            Open meshes…
          </button>
          <p className="muted small">OBJ / PLY for the Base (topology kept), OBJ / PLY / STL for the Reference. Or drop files anywhere, or try an example:</p>
          <div className="menu inline">
            <ExampleItems />
          </div>
        </>
      ) : (
        <>
          <MeshRow label="Base" entry={base} />
          <MeshRow label="Reference" entry={ref} />
          {others.map((m) => (
            <div key={m.id} className="mesh-line other">
              <span className="mesh-line-name" title={m.name}>
                {m.name}
              </span>
              <button className="icon-btn" title="Remove" onClick={() => removeMesh(m.id)}>
                ×
              </button>
            </div>
          ))}
          <div className="row space">
            <span className="row">
              <button className="btn small ghost" disabled={!!job} onClick={() => fileRef.current?.click()}>
                Open…
              </button>
              <button className="btn small ghost" disabled={!base || !ref || !!job} onClick={swapRoles} title="Swap Base and Reference">
                Swap
              </button>
            </span>
            <label className="units" title="Scene units (display only): distances are shown in millimetres">
              Units
              <select value={units} onChange={(e) => set({ units: e.target.value as Units })}>
                <option value="none">—</option>
                <option value="m">m</option>
                <option value="cm">cm</option>
                <option value="mm">mm</option>
              </select>
            </label>
          </div>
          {base && <PartsMore entry={base} />}
        </>
      )}
    </>
  );
}

function MeshRow(props: { label: string; entry?: MeshEntry }) {
  const e = props.entry;
  if (!e) {
    return (
      <div className="mesh-line empty">
        <span className="mesh-role">{props.label}</span>
        <span className="muted small">— open or drop a file</span>
      </div>
    );
  }
  const issues = e.validation.issues.filter((i) => i.severity !== 'info').length;
  return (
    <div className={`mesh-line role-${e.role}`}>
      <span className="mesh-role">{props.label}</span>
      <span className="mesh-line-name" title={`${e.name}\n${e.loaded.attributes.join('\n')}`}>
        {e.name}
      </span>
      <span className="muted small">{e.validation.stats.vertices.toLocaleString()} v</span>
      {issues > 0 && (
        <button className="badge warn" title="Validation findings" onClick={() => set({ drawerOpen: true, bottomTab: 'validation' })}>
          {issues}
        </button>
      )}
      <button className={`icon-btn eye ${e.visible ? 'on' : ''}`} title="Show / hide" onClick={() => toggleVisible(e.id)}>
        {e.visible ? '◉' : '○'}
      </button>
      <button className="icon-btn" title="Remove" onClick={() => removeMesh(e.id)}>
        ×
      </button>
    </div>
  );
}

function PartsMore({ entry }: { entry: MeshEntry }) {
  useStore((s) => s.componentModes);
  const info = meshComponents(entry);
  if (info.sizes.length < 2) return null;
  const modes = effectiveComponentModes() ?? [];
  const counts = { fit: 0, follow: 0, fixed: 0 };
  modes.forEach((m) => counts[m]++);
  const order = info.sizes.map((_, i) => i).sort((a, b) => info.sizes[b] - info.sizes[a]).slice(0, 40);
  return (
    <More label={`Parts: ${counts.fit} fitted · ${counts.follow} following${counts.fixed ? ` · ${counts.fixed} fixed` : ''}`}>
      <p className="muted small">Inner parts (eyes, teeth, tongue) should Follow: they keep their shape and move with the fitted skin.</p>
      <table className="mini-table">
        <tbody>
          {order.map((c) => (
            <tr key={c}>
              <td>
                <i className={`dot mode-${modes[c]}`} /> part {c + 1}
              </td>
              <td className="num-cell">{info.sizes[c].toLocaleString()} v</td>
              <td>
                <select value={modes[c]} onChange={(e) => setComponentMode(c, e.target.value as 'fit' | 'follow' | 'fixed')}>
                  <option value="fit">Fit</option>
                  <option value="follow">Follow</option>
                  <option value="fixed">Fixed</option>
                </select>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </More>
  );
}

// ------------------------------------------------------------------ 2. align

function decompose(t: Float64Array) {
  const m = new THREE.Matrix4().fromArray(t);
  const p = new THREE.Vector3(), q = new THREE.Quaternion(), s = new THREE.Vector3();
  m.decompose(p, q, s);
  const e = new THREE.Euler().setFromQuaternion(q, 'XYZ');
  return { t: [p.x, p.y, p.z], r: [e.x, e.y, e.z].map(THREE.MathUtils.radToDeg), s: (s.x + s.y + s.z) / 3 };
}

function compose(t: number[], rDeg: number[], s: number): Float64Array {
  const [rx, ry, rz] = rDeg.map((v) => THREE.MathUtils.degToRad(v));
  const q = new THREE.Quaternion().setFromEuler(new THREE.Euler(rx, ry, rz, 'XYZ'));
  return Float64Array.from(new THREE.Matrix4().compose(new THREE.Vector3(t[0], t[1], t[2]), q, new THREE.Vector3(s, s, s)).elements);
}

function AlignStep() {
  const transform = useStore((s) => s.transform);
  const locked = useStore((s) => !!s.committed || !!s.preview);
  const job = useStore((s) => s.job);
  const gizmo = useStore((s) => s.display.gizmo);
  const allowScale = useStore((s) => s.allowScale);
  const both = useStore((s) => !!baseEntry(s) && !!refEntry(s));
  const complete = useStore((s) => s.landmarks.filter((l) => l.base && l.ref).length);
  const d = useMemo(() => decompose(transform), [transform]);
  const disabled = !both || locked || !!job;
  const edit = (k: 't' | 'r', i: number, v: number) => {
    const t = [...d.t], r = [...d.r];
    (k === 't' ? t : r)[i] = v;
    setTransform(compose(t, r, d.s), 'Edit transform');
  };
  if (locked) return <p className="muted small">Locked while a deformation exists — reset the deformation to re-align.</p>;
  return (
    <>
      <div className="row">
        <button className="btn primary grow" disabled={disabled} onClick={() => void autoAlignAndRefine()} title="Match bounding boxes, then refine with ICP">
          Auto align
        </button>
        {complete >= 3 && (
          <button className="btn grow" disabled={disabled} onClick={() => alignLandmarks(allowScale)} title="Fit position, rotation and size to your guide pairs">
            From {complete} guides
          </button>
        )}
        <button className="btn ghost" disabled={disabled} onClick={resetTransform} title="Reset placement">
          Reset
        </button>
      </div>
      <Toggle label="Allow uniform scale" checked={allowScale} onChange={(v) => set({ allowScale: v })} hint="On by default: heads of any size are matched. Turn off only when both meshes must keep their real-world size." />
      <More label="Manual">
        <div className="trs">
          <span className="muted small">Move</span>
          {[0, 1, 2].map((i) => (
            <NumberInput key={`t${i}`} value={d.t[i]} onChange={(v) => edit('t', i, v)} disabled={disabled} />
          ))}
          <span className="muted small">Rotate°</span>
          {[0, 1, 2].map((i) => (
            <NumberInput key={`r${i}`} value={d.r[i]} onChange={(v) => edit('r', i, v)} disabled={disabled} format={(v) => v.toFixed(1)} />
          ))}
          <span className="muted small">Scale</span>
          <NumberInput value={d.s} min={1e-6} onChange={(v) => setTransform(compose(d.t, d.r, v), 'Edit scale')} disabled={disabled} format={(v) => v.toPrecision(5)} />
        </div>
        <div className="row">
          <span className="muted small">Gizmo</span>
          <Segmented
            value={gizmo}
            disabled={disabled}
            onChange={(g) => set((s) => ({ display: { ...s.display, gizmo: g } }))}
            options={[
              { value: 'off', label: 'Off' },
              { value: 'translate', label: 'Move', hint: 'T' },
              { value: 'rotate', label: 'Rotate', hint: 'R' },
              { value: 'scale', label: 'Scale', hint: 'S' },
            ]}
          />
        </div>
      </More>
    </>
  );
}

// ------------------------------------------------------------------ 3. landmarks

function LandmarkStep() {
  const landmarks = useStore((s) => s.landmarks);
  const tool = useStore((s) => s.tool);
  const pending = useStore((s) => s.pendingPick);
  const guided = useStore((s) => s.guided);
  const both = useStore((s) => !!baseEntry(s) && !!refEntry(s));
  const complete = landmarks.filter((l) => l.base && l.ref).length;
  const pendingL = pending ? landmarks.find((l) => l.id === pending.landmarkId) : undefined;
  const hasPairs = landmarks.some((l) => / [LR]$/.test(l.label) && (l.base || l.ref));
  const mode = useStore((s) => s.guideMode);
  const mirror = useStore((s) => s.mirrorGuides);
  const claude = useStore((s) => s.claudeLink);
  const dotSize = useStore((s) => s.guideSize);
  const linked = useStore((s) => !!s.returnUrl);
  const metahuman = useStore((s) => isMetaHumanBase(baseEntry(s)));
  const mh = metahuman && mode === 'metahuman';
  const aligned = useStore((s) => !isIdentity(s.transform));
  const side = (s: 'base' | 'ref') => (s === 'base' ? 'Base (left)' : mh ? 'your head (right)' : 'Reference (right)');
  return (
    <>
      {tool !== 'landmark' && (
        <p className="muted small">
          {mh
            ? 'The MetaHuman points are already placed: click each named point on your head.'
            : 'Match the two meshes with a few points: eye corners, mouth corners, nose tip, chin, ears. Each pair gets its own colour.'}
        </p>
      )}
      <div className="row">
        <Segmented
          value={mh ? 'metahuman' : 'free'}
          onChange={(m) => set({ guideMode: m as 'free' | 'metahuman' })}
          options={[
            { value: 'free', label: 'Free', hint: 'Click a point on each mesh' },
            ...(metahuman ? [{ value: 'metahuman', label: 'MetaHuman', hint: 'MetaHuman points pre-placed; click yours' }] : []),
          ]}
        />
      </div>
      <Toggle label="Mirror" checked={mirror} onChange={(v) => set({ mirrorGuides: v })} hint="Place guides on the character's left side only (the right of the screen from the front), as in Mutant Tools; the other side is mirrored." />
      <Toggle
        label="Claude"
        checked={claude}
        disabled={!linked}
        onChange={(v) => {
          set({ claudeLink: v });
          if (v) void runClaudeLink();
        }}
        hint={
          linked
            ? 'Let Claude Code place the guides: with this on, ask Claude Code to place the guides in TopoTransfer.'
            : 'Open the bridge first: open TopoTransfer from Mutant Tools (Misc > TopoTransfer, or Meta Mutant), which opens it for you.'
        }
      />
      <Slider label="Dot size" value={dotSize} min={0.2} max={3} step={0.1} onChange={(v) => set({ guideSize: v })} format={(v) => `${v.toFixed(1)}×`} hint="Size of the guide dots in the view" />
      {claude && <p className="muted small">Claude is linked: ask Claude Code to place the guides. You can still move any dot yourself.</p>}
      <div className="row">
        <button
          className={`btn small ${tool === 'landmark' ? 'active' : 'primary'}`}
          disabled={!both}
          onClick={() => {
            if (!mh) return setTool('landmark');
            addMetaHumanGuides();
            if (aligned) autoGuessGuides(); // a first guess for each point on your head, from the aligned MetaHuman
          }}
          title={mh ? 'Ask for each MetaHuman point on your head' : 'Click a point on the Base, then the same spot on the Reference (L)'}
        >
          Place guides <Kbd>L</Kbd>
        </button>
        {!mh && (
          <button className="btn small" disabled={!both} onClick={() => addPreset('face')} title="32 named face points, asked for one by one">
            Face set
          </button>
        )}
        {!mh && (
          <button className="btn small" disabled={!both} onClick={() => addPreset('body')} title="40 named body points, asked for one by one">
            Body set
          </button>
        )}
        <button className="btn small" disabled={!hasPairs} onClick={mirrorLandmarks} title="Fill missing left/right counterparts across the symmetry plane">
          Mirror L↔R
        </button>
      </div>
      {tool === 'landmark' && (
        <div className="hint-box">
          {pending && pendingL ? (
            <>
              <b>
                <i className="dot" style={{ background: pairColor(pendingL.id) }} /> {pendingL.label} · {side(pending.side)}
              </b>
              <div>{presetHint(pendingL.label) ?? `Click it on the ${side(pending.side)}.`}</div>
            </>
          ) : (
            mh ? (
              <>Check the guessed points on your head (right): drag a wrong dot to its spot. With Mirror on, either side works; the other side follows when you let go. <Kbd>Ctrl</Kbd>+<Kbd>Z</Kbd> undoes.</>
            ) : (
              <>Click a point on the Base (left), then the same spot on the Reference (right). Each pair gets its own colour. Drag a placed dot to move it. <Kbd>Ctrl</Kbd>+<Kbd>Z</Kbd> undoes a point.</>
            )
          )}
          <div className="row end">
            {guided && pending && (
              <button className="btn small ghost" onClick={skipGuided}>
                Skip
              </button>
            )}
            <button className="btn small primary" onClick={() => setTool('navigate')}>
              Done
            </button>
          </div>
        </div>
      )}
      {landmarks.length > 0 && (
        <div className="row space">
          <span className="muted small">
            {complete} of {landmarks.length} complete
          </span>
          {!guided && complete < landmarks.length && both && (
            <button className="btn small ghost" onClick={startGuided}>
              Continue placing
            </button>
          )}
        </div>
      )}
      {landmarks.length > 0 && (
        <More label="List">
          <LandmarkTable />
          <div className="row end">
            <button className="btn small ghost" onClick={clearLandmarks}>
              Clear all
            </button>
          </div>
        </More>
      )}
    </>
  );
}

function LandmarkTable() {
  const landmarks = useStore((s) => s.landmarks);
  const selected = useStore((s) => s.selectedLandmarkId);
  const pending = useStore((s) => s.pendingPick);
  return (
    <table className="lm-table">
      <tbody>
        {landmarks.map((l) => (
          <tr key={l.id} className={l.id === selected ? 'selected' : ''} onClick={() => set({ selectedLandmarkId: l.id })}>
            <td className="lm-name" title={presetHint(l.label) ?? l.label}>
              <i className="dot" style={{ background: pairColor(l.id) }} />
              {l.id} <span className="muted">{l.label !== `L${l.id}` ? l.label : ''}</span>
            </td>
            <td>
              <select value={l.group} onChange={(e) => updateLandmark(l.id, { group: e.target.value as LandmarkGroup })} title="Group">
                {LANDMARK_GROUPS.map((g) => (
                  <option key={g} value={g}>
                    {g}
                  </option>
                ))}
              </select>
            </td>
            <td title="Weight">
              <NumberInput className="tiny" value={l.weight} min={0} max={10} onChange={(v) => updateLandmark(l.id, { weight: v })} format={(v) => v.toFixed(1)} />
            </td>
            <td className="lm-status">
              {(['base', 'ref'] as const).map((side) => (
                <button
                  key={side}
                  className={`pick ${l[side] ? 'ok' : 'missing'} ${pending?.landmarkId === l.id && pending.side === side ? 'pending' : ''}`}
                  title={`${l[side] ? 'Re-pick' : 'Pick'} on ${side === 'base' ? 'Base' : 'Reference'}`}
                  onClick={(e) => {
                    e.stopPropagation();
                    repickLandmark(l.id, side);
                  }}
                >
                  {side === 'base' ? 'B' : 'R'}
                </button>
              ))}
            </td>
            <td>
              <button
                className="icon-btn"
                title="Delete (Del)"
                onClick={(e) => {
                  e.stopPropagation();
                  deleteLandmark(l.id);
                }}
              >
                ×
              </button>
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}

// ------------------------------------------------------------------ 4. wrap

const pct = (v: number) => `${(v * 100).toFixed(1)}%`;

function WrapStep() {
  const p = useStore((s) => s.params);
  const job = useStore((s) => s.job);
  const preview = useStore((s) => s.preview);
  const committed = useStore((s) => s.committed);
  const committedResult = useStore((s) => s.committedResult);
  const both = useStore((s) => !!baseEntry(s) && !!refEntry(s));
  const n = useStore((s) => baseEntry(s)?.validation.stats.vertices ?? 0);
  useStore((s) => s.units);
  const wrapping = job?.kind === 'wrap';
  const quality = qualityOf(p);
  const result = preview?.result ?? (committed ? committedResult : null);
  const d = result?.diagnostics;
  const est = estimateWrapSeconds(n, p);
  return (
    <>
      <Slider
        label="Detail"
        value={1 - p.smoothness}
        min={0}
        max={1}
        step={0.01}
        onChange={(v) => setParams({ smoothness: 1 - v })}
        format={(v) => `${Math.round(v * 100)}`}
        hint="Low: smoother, stiffer result that keeps the Base's own surface. High: follows fine Reference detail."
      />
      <div className="row space">
        <span className="slider-label">Quality</span>
        <Segmented
          value={quality === 'custom' ? ('balanced' as Quality) : quality}
          onChange={(q) => setParams(QUALITY_PRESETS[q])}
          options={[
            { value: 'fast', label: 'Fast', hint: '3 levels × 4 iterations' },
            { value: 'balanced', label: 'Balanced', hint: '4 levels × 6 iterations (default)' },
            { value: 'high', label: 'High', hint: '6 levels × 10 iterations: ~25% less vertex sliding on human bodies, ~2× time' },
          ]}
        />
      </div>
      {quality === 'custom' && <p className="muted small">Custom schedule: {p.levels} levels × {p.iterationsPerLevel} iterations (see More).</p>}

      <div className="wrap-actions">
        {wrapping ? (
          <button className="btn danger wide" onClick={() => void cancelJob()} disabled={!job?.cancellable}>
            {job?.cancellable ? 'Cancel' : 'Cancelling…'} <Kbd>Esc</Kbd>
          </button>
        ) : preview ? (
          <>
            <button className="btn primary grow" onClick={commitPreview} title="Keep this result (Ctrl+Enter)">
              Keep result
            </button>
            <button className="btn grow" onClick={discardPreview}>
              Discard
            </button>
          </>
        ) : (
          <button className="btn primary wide" disabled={!both || !!job} onClick={() => void runWrap()} title="Compute a preview (Ctrl+Enter)">
            {committed ? 'Fit again' : 'Fit'} <Kbd>Ctrl ⏎</Kbd>
          </button>
        )}
      </div>
      {!d && n > 0 && !wrapping && <p className="muted small">About {est < 1 ? '1' : est.toFixed(0)} s for {n.toLocaleString()} vertices (estimate).</p>}

      {d && (
        <div className={`result-card ${d.warnings.length ? 'warn' : ''}`}>
          <div className="result-main">
            <span>
              <b>{fmtLen(d.distanceAfter.mean)}</b> mean
            </span>
            <span>
              <b>{fmtLen(d.distanceAfter.max)}</b> max
            </span>
            <span className={d.quality.flippedTriangles ? 'bad' : ''}>
              <b>{d.quality.flippedTriangles}</b> flips
            </span>
            <span className="muted">{(d.timings.totalMs / 1000).toFixed(1)} s</span>
          </div>
          <div className="muted small">
            {preview ? 'Preview — not kept yet.' : 'Kept.'} Distance to the Reference, measured at {d.distanceAfter.count.toLocaleString()} vertices (was {fmtLen(d.distanceBefore.mean)} mean).
            {d.warnings.length > 0 && ` ${d.warnings.length} warning(s) in the log.`}
          </div>
          <More label="Details">
            <table className="mini-table stats">
              <tbody>
                <tr><td>95th percentile</td><td>{fmtLen(d.distanceBefore.p95)}</td><td>{fmtLen(d.distanceAfter.p95)}</td></tr>
                <tr><td>Fitted region mean</td><td /><td>{fmtLen(d.inlierDistanceAfter.mean)}</td></tr>
                <tr><td>Coverage (ref→base)</td><td>{fmtLen(d.coverageBefore.mean)}</td><td>{fmtLen(d.coverageAfter.mean)}</td></tr>
                <tr><td>Collapsed triangles</td><td /><td>{d.quality.collapsedTriangles}</td></tr>
                <tr><td>Over-stretched edges</td><td /><td>{d.quality.stretchedEdges}</td></tr>
                <tr><td>Edge length ratio</td><td /><td>{d.quality.minEdgeRatio.toFixed(2)}–{d.quality.maxEdgeRatio.toFixed(2)}</td></tr>
                <tr><td>Vertices / faces</td><td /><td>{d.vertexCount.toLocaleString()} unchanged</td></tr>
              </tbody>
            </table>
          </More>
        </div>
      )}
      {(committed || preview) && !wrapping && (
        <div className="row end">
          <button className="btn small ghost" onClick={resetDeformation} title="Back to the aligned, undeformed Base">
            Reset deformation
          </button>
        </div>
      )}
      <RegionsMore />
      <More label="More settings">
        <Slider label="Fitting strength" value={p.fitStrength} min={0} max={2} step={0.05} onChange={(v) => setParams({ fitStrength: v })} hint="Pull of the surface fit relative to stiffness, landmarks and regions." />
        <Slider label="Landmark influence" value={p.landmarkInfluence} min={0} max={5} step={0.1} onChange={(v) => setParams({ landmarkInfluence: v })} />
        <Slider label="Max distance" value={p.maxCorrespondenceDistance} min={0.005} max={0.5} log onChange={(v) => setParams({ maxCorrespondenceDistance: v })} format={pct} hint="Ignore Reference points farther than this (fraction of its size)." />
        <Slider label="Normal alignment" value={p.normalAlignment} min={0} max={0.95} step={0.05} onChange={(v) => setParams({ normalAlignment: v })} hint="0 point-to-point … 1 slide along the surface." />
        <Slider label="Normal threshold°" value={p.normalThresholdDeg} min={10} max={180} step={1} onChange={(v) => setParams({ normalThresholdDeg: v })} format={(v) => v.toFixed(0)} />
        <Slider label="Levels" value={p.levels} min={1} max={8} step={1} onChange={(v) => setParams({ levels: Math.round(v) })} format={(v) => v.toFixed(0)} />
        <Slider label="Iterations / level" value={p.iterationsPerLevel} min={1} max={30} step={1} onChange={(v) => setParams({ iterationsPerLevel: Math.round(v) })} format={(v) => v.toFixed(0)} />
        <Toggle label="Bidirectional correspondences" checked={p.bidirectional} onChange={(v) => setParams({ bidirectional: v })} />
        <Toggle label="Ignore open borders (holes)" checked={p.rejectBoundary} onChange={(v) => setParams({ rejectBoundary: v })} />
        <Toggle label="Two-sided normals" checked={p.twoSidedNormals} onChange={(v) => setParams({ twoSidedNormals: v })} hint="For scans with inconsistent normals." />
        <Toggle label="Seam lock" checked={p.seamLock} onChange={(v) => setParams({ seamLock: v })} hint="Keep coincident unconnected vertices (UV splits) together." />
        <Toggle label="Allow local scaling" checked={p.allowLocalScaling} onChange={(v) => setParams({ allowLocalScaling: v })} />
        <div className="row end">
          <button className="btn small ghost" onClick={resetParams} disabled={JSON.stringify(p) === JSON.stringify(DEFAULT_WRAP_PARAMS)}>
            Restore defaults
          </button>
        </div>
      </More>
    </>
  );
}

function RegionsMore() {
  const p = useStore((s) => s.params);
  const tool = useStore((s) => s.tool);
  const brush = useStore((s) => s.brush);
  const mask = useStore((s) => s.mask);
  useStore((s) => s.maskVersion);
  const job = useStore((s) => s.job);
  const coverage = mask ? maskCoverage(mask) : 0;
  return (
    <More label={mask ? `Regions: ${(coverage * 100).toFixed(1)}% painted` : 'Regions'}>
      <div className="row">
        <button className={`btn small ${tool === 'paint' ? 'active' : ''}`} disabled={!!job} onClick={() => setTool('paint')} title="Left-drag paints, right-drag orbits (P)">
          Paint <Kbd>P</Kbd>
        </button>
        <Segmented
          value={brush.erase ? 'erase' : 'paint'}
          onChange={(v) => set((s) => ({ brush: { ...s.brush, erase: v === 'erase' } }))}
          options={[
            { value: 'paint', label: 'Add' },
            { value: 'erase', label: 'Erase', hint: 'E' },
          ]}
        />
      </div>
      <Segmented
        value={p.maskMode}
        onChange={(v) => setParams({ maskMode: v })}
        options={[
          { value: 'protect', label: 'Protect painted' },
          { value: 'fitOnly', label: 'Fit only painted' },
        ]}
      />
      <Slider label="Brush size" value={brush.radius} min={0.005} max={0.4} log onChange={(v) => set((s) => ({ brush: { ...s.brush, radius: v } }))} format={pct} />
      <Slider label="Strength" value={p.regionInfluence} min={0} max={1} step={0.01} onChange={(v) => setParams({ regionInfluence: v })} hint="How strongly protected vertices stay in place." />
      <div className="btn-grid six">
        {(['smooth', 'grow', 'shrink', 'invert', 'fill', 'clear'] as const).map((op) => (
          <button key={op} className="btn small" disabled={!!job} onClick={() => maskOp(op)}>
            {op[0].toUpperCase() + op.slice(1)}
          </button>
        ))}
      </div>
    </More>
  );
}

// ------------------------------------------------------------------ 5. export

// ------------------------------------------------------------------ 5. brush

const BRUSHES = [
  { value: 'move', label: 'Move', hint: 'Drag the surface under the brush' },
  { value: 'sculpt', label: 'Sculpt', hint: 'Push out for detail; hold Ctrl to push in' },
  { value: 'smooth', label: 'Smooth', hint: 'Project smooth: smooth, then stick back onto the Reference' },
  { value: 'relax', label: 'Relax', hint: 'Project relax: even out the edges along the surface, staying on the Reference' },
] as const;

function BrushStep() {
  const tool = useStore((s) => s.tool);
  const sc = useStore((s) => s.sculpt);
  const ready = useStore((s) => !!s.committed && !s.preview);
  const on = tool === 'sculpt';
  const put = (p: Partial<typeof sc>) => set((s) => ({ sculpt: { ...s.sculpt, ...p } }));
  return (
    <>
      <p className="muted small">{ready ? 'Touch up the fit by hand: left-drag on the result. Right-drag turns the view.' : 'Run Fit and keep the result first.'}</p>
      <div className="row">
        <button className={`btn small ${on ? 'active' : 'primary'}`} disabled={!ready} onClick={() => setTool(on ? 'navigate' : 'sculpt')} title="Brush on the fitted Base (G); [ and ] change its size">
          {on ? 'Done' : 'Brush'} <Kbd>G</Kbd>
        </button>
        <Toggle label="Mirror" checked={sc.mirror} onChange={(v) => put({ mirror: v })} hint="Every stroke also works on the other side of the face." />
      </div>
      {on && (
        <>
          <Segmented value={sc.mode} onChange={(m) => put({ mode: m })} options={BRUSHES.map((b) => ({ ...b }))} />
          <p className="muted small">{BRUSHES.find((b) => b.value === sc.mode)!.hint}.</p>
          <Slider label="Size" value={sc.radius} min={0.005} max={0.2} log onChange={(v) => put({ radius: v })} format={(v) => `${(v * 100).toFixed(1)}%`} />
          {sc.mode !== 'move' && <Slider label="Strength" value={sc.strength} min={0.05} max={1} step={0.05} onChange={(v) => put({ strength: v })} />}
          <p className="muted small">
            <Kbd>Ctrl</Kbd>+<Kbd>Z</Kbd> undoes a stroke.
          </p>
        </>
      )}
    </>
  );
}

// ------------------------------------------------------------------ 6. export

function ExportStep() {
  const space = useStore((s) => s.exportSpace);
  const hasBase = useStore((s) => !!baseEntry(s));
  const committed = useStore((s) => !!s.committed);
  const preview = useStore((s) => !!s.preview);
  const job = useStore((s) => s.job);
  const maya = useStore((s) => !!s.returnUrl);
  const blocked = !hasBase || preview || !!job;
  return (
    <>
      <div className="row">
        <span className="muted small">OBJ</span>
        <select value={space} onChange={(e) => set({ exportSpace: e.target.value as 'reference' | 'original' })} title="Where the exported mesh sits">
          <option value="reference">Reference position</option>
          <option value="original">Original Base position</option>
        </select>
      </div>
      <div className="row">
        {/* the tooltip sits on a wrapper: disabled buttons get no hover in every browser */}
        <span
          className="grow"
          style={{ display: 'flex' }}
          title={
            !maya
              ? 'Maya is not listening. Open the bridge first: open TopoTransfer from Mutant Tools (Misc > TopoTransfer, or Meta Mutant), which opens it for you.'
              : preview
                ? 'Keep or discard the preview first'
                : 'Send the OBJ to Maya (Ctrl+E)'
          }
        >
          <button className="btn primary grow" disabled={blocked || !maya} onClick={() => void exportBase(space, true)}>
            {maya ? 'Send to Maya' : 'Send to Maya (not listening)'}
          </button>
        </span>
        <button className="btn" disabled={blocked} onClick={() => void exportBase(space, false)} title={preview ? 'Keep or discard the preview first' : 'Save the OBJ file'}>
          Download
        </button>
      </div>
      <p className="muted small">
        {committed ? 'Exports the kept fit.' : 'Nothing fitted yet: exports the aligned Base.'} Vertex order, faces and UVs stay the same; the file is checked before it goes out.
      </p>
    </>
  );
}
