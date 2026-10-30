import { useEffect, useRef, useState } from 'react';
import { cancelJob } from '../../state/actions';
import { baseEntry, refEntry, set, useStore } from '../../state/store';

export function StatusBar() {
  const drawer = useStore((s) => s.drawerOpen);
  const tab = useStore((s) => s.bottomTab);
  const last = useStore((s) => s.log[s.log.length - 1]);
  const warnCount = useStore((s) => s.log.filter((l) => l.level !== 'info').length);
  const open = (t: 'log' | 'validation' | 'iterations') => set((s) => ({ drawerOpen: !(s.drawerOpen && s.bottomTab === t), bottomTab: t }));
  return (
    <>
      {drawer && (
        <div className="drawer">
          <div className="tabs">
            <button className={tab === 'log' ? 'active' : ''} onClick={() => set({ bottomTab: 'log' })}>
              Log
            </button>
            <button className={tab === 'validation' ? 'active' : ''} onClick={() => set({ bottomTab: 'validation' })}>
              Mesh checks
            </button>
            <button className={tab === 'iterations' ? 'active' : ''} onClick={() => set({ bottomTab: 'iterations' })}>
              Solver
            </button>
            <button className="icon-btn tabs-right" onClick={() => set({ drawerOpen: false })} title="Close">
              ×
            </button>
          </div>
          <div className="tab-body">{tab === 'log' ? <LogView /> : tab === 'validation' ? <ValidationView /> : <IterationView />}</div>
        </div>
      )}
      <footer className="statusbar">
        <JobStatus />
        <span className={`status-last ${last?.level ?? ''}`} onClick={() => open('log')} title="Open the log">
          {last?.text ?? 'Local processing only — meshes never leave this browser.'}
        </span>
        <button className={`status-btn ${drawer && tab === 'log' ? 'active' : ''}`} onClick={() => open('log')}>
          Log{warnCount > 0 && <span className="badge warn">{warnCount}</span>}
        </button>
        <button className={`status-btn ${drawer && tab === 'validation' ? 'active' : ''}`} onClick={() => open('validation')}>
          Checks
        </button>
        <button className={`status-btn ${drawer && tab === 'iterations' ? 'active' : ''}`} onClick={() => open('iterations')}>
          Solver
        </button>
      </footer>
    </>
  );
}

function JobStatus() {
  const job = useStore((s) => s.job);
  const [, tick] = useState(0);
  useEffect(() => {
    if (!job) return;
    const id = setInterval(() => tick((x) => x + 1), 250);
    return () => clearInterval(id);
  }, [job]);
  if (!job) {
    return (
      <div className="status idle">
        <span className="status-dot" /> Ready
      </div>
    );
  }
  const elapsed = (performance.now() - job.startedAt) / 1000;
  const wp = job.wrapProgress;
  return (
    <div className="status busy">
      <span className="status-dot spin" />
      <span className="status-label">{job.label}</span>
      <div className="progress">
        <div className={`progress-fill ${job.kind !== 'wrap' ? 'indeterminate' : ''}`} style={job.kind === 'wrap' ? { width: `${Math.round(job.progress * 100)}%` } : undefined} />
      </div>
      <span className="status-msg">
        {job.message}
        {wp?.rmsFit !== undefined ? ` · RMS fit ${wp.rmsFit.toPrecision(3)}` : ''}
      </span>
      <span className="muted">{elapsed.toFixed(1)} s</span>
      {job.kind === 'wrap' && (
        <button className="btn small danger" disabled={!job.cancellable} onClick={() => void cancelJob()}>
          {job.cancellable ? 'Cancel' : 'Cancelling…'}
        </button>
      )}
    </div>
  );
}

function LogView() {
  const log = useStore((s) => s.log);
  const ref = useRef<HTMLDivElement>(null);
  useEffect(() => {
    ref.current?.scrollTo(0, ref.current.scrollHeight);
  }, [log.length]);
  if (!log.length) return <div className="muted small pad">Load meshes to begin. Press ? for shortcuts.</div>;
  return (
    <div className="log" ref={ref}>
      {log.map((l, i) => (
        <div key={i} className={`log-line ${l.level}`}>
          <span className="log-time">{new Date(l.t).toLocaleTimeString()}</span>
          <span className="log-level">{l.level === 'info' ? '·' : l.level === 'warn' ? '!' : '✕'}</span>
          <span className="log-text">{l.text}</span>
        </div>
      ))}
    </div>
  );
}

function ValidationView() {
  const base = useStore((s) => baseEntry(s));
  const ref = useStore((s) => refEntry(s));
  const entries = [base, ref].filter(Boolean) as NonNullable<typeof base>[];
  if (!entries.length) return <div className="muted small pad">No Base or Reference mesh assigned.</div>;
  return (
    <div className="validation">
      {entries.map((m) => {
        const st = m.validation.stats;
        return (
          <div key={m.id} className="val-card">
            <div className="val-title">
              <b>{m.role === 'base' ? 'Base' : 'Reference'}</b> {m.name}
            </div>
            <div className="val-stats muted small">
              {st.vertices.toLocaleString()} vertices · {st.faces.toLocaleString()} faces ({Object.entries(st.polygonSizes)
                .map(([k, v]) => `${v.toLocaleString()}×${k}-gon`)
                .join(', ')}) · {st.components} components · {st.closed ? 'closed' : `${st.boundaryEdges} boundary edges`} · bbox {st.bbox.size.map((v) => v.toPrecision(3)).join(' × ')}
            </div>
            {m.validation.issues.length === 0 ? (
              <div className="val-ok small">No problems found.</div>
            ) : (
              <ul className="val-issues">
                {m.validation.issues.map((i, k) => (
                  <li key={k} className={i.severity}>
                    <span className="sev">{i.severity}</span> {i.message}
                    {i.samples && i.samples.length > 0 && <span className="muted small"> e.g. #{i.samples.slice(0, 5).join(', #')}</span>}
                  </li>
                ))}
              </ul>
            )}
          </div>
        );
      })}
    </div>
  );
}

function IterationView() {
  const preview = useStore((s) => s.preview);
  const committed = useStore((s) => s.committedResult);
  const d = (preview?.result ?? committed)?.diagnostics;
  if (!d) return <div className="muted small pad">Run a fit to see per-iteration solver diagnostics.</div>;
  return (
    <div className="iter-wrap">
      <div className="muted small pad">
        Stiffness schedule: {d.schedule.map((l) => l.toExponential(1)).join(' → ')} · multigrid levels {d.amgLevels.join(' / ')} · seam pairs {d.seamPairs} · landmarks used {d.landmarksUsed}
        <br />
        Time by stage (measured):{' '}
        {Object.entries(
          d.iterations.reduce<Record<string, number>>((acc, it) => {
            for (const [k, v] of Object.entries(it.stages)) acc[k] = (acc[k] ?? 0) + v;
            return acc;
          }, {}),
        )
          .sort((a, b) => b[1] - a[1])
          .map(([k, v]) => `${k} ${(v / 1000).toFixed(2)} s`)
          .join(' · ')}
      </div>
      <table className="iter-table">
        <thead>
          <tr>
            <th>Level</th>
            <th>It</th>
            <th>λ</th>
            <th>Accepted</th>
            <th>Reverse</th>
            <th>RMS fit</th>
            <th>CG its</th>
            <th>Residual</th>
            <th>Max step</th>
            <th>Time</th>
          </tr>
        </thead>
        <tbody>
          {d.iterations.map((it, i) => (
            <tr key={i}>
              <td>{it.level + 1}</td>
              <td>{it.iteration + 1}</td>
              <td>{it.lambda.toExponential(1)}</td>
              <td>{(it.acceptedFraction * 100).toFixed(1)}%</td>
              <td>{it.reverseAccepted.toLocaleString()}</td>
              <td>{it.rmsFit.toPrecision(3)}</td>
              <td>{it.cgIterations}</td>
              <td className={it.cgResidual > 1e-3 ? 'bad' : ''}>{it.cgResidual.toExponential(1)}</td>
              <td>{it.maxDisplacement.toPrecision(3)}</td>
              <td>{it.ms.toFixed(0)} ms</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
