import { useState } from 'react';
import { loadExampleKind } from '../state/actions';
import { redo, set, undo, useStore } from '../state/store';

export function ExampleItems(props: { onPick?: () => void }) {
  const pick = (k: 'body' | 'head' | 'synthetic') => {
    props.onPick?.();
    void loadExampleKind(k);
  };
  return (
    <>
      <button className="menu-item" onClick={() => pick('body')}>
        <b>Human body</b>
        <span>Male base cage → female sculpt (CC0)</span>
      </button>
      <button className="menu-item" onClick={() => pick('head')}>
        <b>Human head</b>
        <span>Animation head → sculpt head, eyes Follow (CC0)</span>
      </button>
      <button className="menu-item" onClick={() => pick('synthetic')}>
        <b>Synthetic head</b>
        <span>Quad sphere with eyes → stylised head</span>
      </button>
    </>
  );
}

export function TopBar() {
  const job = useStore((s) => s.job);
  const canUndo = useStore((s) => s.undoStack.length > 0 && !s.job && !s.preview);
  const canRedo = useStore((s) => s.redoStack.length > 0 && !s.job && !s.preview);
  const undoLabel = useStore((s) => s.undoStack[s.undoStack.length - 1]?.label);
  const [menu, setMenu] = useState(false);
  return (
    <header className="topbar">
      <div className="brand">
        <svg width="20" height="20" viewBox="0 0 20 20" aria-hidden>
          <path d="M3 14 L10 3 L17 14 Z" fill="none" stroke="currentColor" strokeWidth="1.6" />
          <path d="M3 14 L10 17 L17 14 M10 3 L10 17" fill="none" stroke="currentColor" strokeWidth="1.2" opacity="0.6" />
        </svg>
        <span>TopoTransfer</span>
      </div>
      <nav className="top-actions">
        <button className="btn ghost" disabled={!!job} onClick={() => document.getElementById('file-input')?.click()} title="Open mesh files (Ctrl+O)">
          Open
        </button>
        <span className="menu-anchor">
          <button className="btn ghost" disabled={!!job} onClick={() => setMenu(!menu)} title="Load an example Base/Reference pair">
            Examples ▾
          </button>
          {menu && (
            <div className="menu" onMouseLeave={() => setMenu(false)}>
              <ExampleItems onPick={() => setMenu(false)} />
            </div>
          )}
        </span>
        <span className="sep" />
        <button className="btn ghost" disabled={!canUndo} onClick={undo} title={undoLabel ? `Undo ${undoLabel} (Ctrl+Z)` : 'Undo (Ctrl+Z)'}>
          Undo
        </button>
        <button className="btn ghost" disabled={!canRedo} onClick={redo} title="Redo (Ctrl+Shift+Z)">
          Redo
        </button>
        <span className="sep" />
        <button className="btn ghost" onClick={() => set({ helpOpen: true })} title="Workflow and shortcuts (?)">
          Help
        </button>
      </nav>
    </header>
  );
}
