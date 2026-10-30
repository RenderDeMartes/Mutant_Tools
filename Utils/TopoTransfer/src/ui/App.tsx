import { useEffect, useState } from 'react';
import { loadFiles, loadFromLaunch } from '../state/actions';
import { hasLaunchParams, parseLaunchParams, stripLaunchParams } from '../state/launch';
import { StatusBar } from './panels/StatusBar';
import { Workflow } from './panels/Workflow';
import { TopBar } from './TopBar';
import { HelpDialog } from './Dialogs';
import { Viewport } from './viewport/Viewport';
import { installShortcuts } from './shortcuts';

let launchHandled = false;

/** `?base=…&reference=…&return=…` from a local tool (maya/tt_bridge.py); read once per page load. */
function handleLaunchParams() {
  if (launchHandled) return;
  launchHandled = true;
  const params = parseLaunchParams(window.location.search);
  if (!hasLaunchParams(params)) return;
  // the URLs carry the local bridge's access token: keep them out of the address bar and bookmarks
  window.history.replaceState(window.history.state, '', stripLaunchParams(window.location.href));
  void loadFromLaunch(params);
}

export function App() {
  const [dragging, setDragging] = useState(false);
  useEffect(() => installShortcuts(), []);
  useEffect(handleLaunchParams, []);
  useEffect(() => {
    let depth = 0;
    const hasFiles = (e: DragEvent) => Array.from(e.dataTransfer?.types ?? []).includes('Files');
    const enter = (e: DragEvent) => {
      if (!hasFiles(e)) return;
      e.preventDefault();
      depth++;
      setDragging(true);
    };
    const leave = (e: DragEvent) => {
      if (!hasFiles(e)) return;
      depth = Math.max(0, depth - 1);
      if (depth === 0) setDragging(false);
    };
    const over = (e: DragEvent) => {
      if (hasFiles(e)) e.preventDefault();
    };
    const drop = (e: DragEvent) => {
      if (!hasFiles(e)) return;
      e.preventDefault();
      depth = 0;
      setDragging(false);
      const files = Array.from(e.dataTransfer?.files ?? []);
      if (files.length) void loadFiles(files);
    };
    window.addEventListener('dragenter', enter);
    window.addEventListener('dragleave', leave);
    window.addEventListener('dragover', over);
    window.addEventListener('drop', drop);
    return () => {
      window.removeEventListener('dragenter', enter);
      window.removeEventListener('dragleave', leave);
      window.removeEventListener('dragover', over);
      window.removeEventListener('drop', drop);
    };
  }, []);
  return (
    <div className="app">
      <TopBar />
      <Viewport />
      <Workflow />
      <StatusBar />
      <HelpDialog />
      {dragging && (
        <div className="drop-overlay">
          <div>Drop OBJ / PLY / STL to load</div>
        </div>
      )}
    </div>
  );
}
