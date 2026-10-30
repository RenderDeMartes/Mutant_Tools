import { addMetaHumanGuides, autoGuessGuides, cancelJob, commitPreview, deleteLandmark, exportBase, isMetaHumanBase, runWrap, setHeatmap, setTool } from '../state/actions';
import { get, redo, set, undo } from '../state/store';
import { requestFrame } from './viewport/SceneController';

function isTyping(e: KeyboardEvent): boolean {
  const t = e.target as HTMLElement | null;
  if (!t) return false;
  const tag = t.tagName;
  return tag === 'INPUT' || tag === 'TEXTAREA' || tag === 'SELECT' || t.isContentEditable;
}

export function installShortcuts(): () => void {
  const onKey = (e: KeyboardEvent) => {
    const s = get();
    const ctrl = e.ctrlKey || e.metaKey;
    if (e.key === 'Escape') {
      if (s.helpOpen) return set({ helpOpen: false });
      if (s.drawerOpen) return set({ drawerOpen: false });
      if (s.job?.kind === 'wrap') return void cancelJob();
      if (s.pendingPick) return set({ pendingPick: null });
      if (s.tool !== 'navigate') return set({ tool: 'navigate' });
      if (s.display.gizmo !== 'off') return set({ display: { ...s.display, gizmo: 'off' } });
      return;
    }
    if (isTyping(e)) return;
    if (ctrl) {
      const k = e.key.toLowerCase();
      if (k === 'z' && !e.shiftKey) {
        e.preventDefault();
        undo();
      } else if ((k === 'z' && e.shiftKey) || k === 'y') {
        e.preventDefault();
        redo();
      } else if (k === 'o') {
        e.preventDefault();
        document.getElementById('file-input')?.click();
      } else if (k === 'e') {
        e.preventDefault();
        if (!s.preview && !s.job && s.meshes.some((m) => m.role === 'base')) void exportBase(s.exportSpace);
      } else if (e.key === 'Enter') {
        e.preventDefault();
        if (s.preview) commitPreview();
        else void runWrap();
      }
      return;
    }
    if (e.altKey) return;
    const d = s.display;
    switch (e.key) {
      case 'f':
      case 'F':
        requestFrame();
        break;
      case '1':
        set({ display: { ...d, mode: 'shaded' } });
        break;
      case '2':
        set({ display: { ...d, mode: 'wire' } });
        break;
      case '3':
        set({ display: { ...d, mode: 'shadedWire' } });
        break;
      case 'b':
        set({ display: { ...d, showBase: !d.showBase } });
        break;
      case 'n':
        set({ display: { ...d, showReference: !d.showReference } });
        break;
      case 'x':
        set({ display: { ...d, refOpacity: d.refOpacity < 0.99 ? 1 : 0.45 } });
        break;
      case 'o':
        set({ display: { ...d, showOriginal: !d.showOriginal } });
        break;
      case 'h': {
        const order = ['none', 'distance', 'displacement'] as const;
        void setHeatmap(order[(order.indexOf(d.heatmap) + 1) % order.length]);
        break;
      }
      case 'l':
        if (s.guideMode === 'metahuman' && isMetaHumanBase() && !s.landmarks.some((l) => l.base && !l.ref) && s.tool !== 'landmark') {
          addMetaHumanGuides();
          if (Array.from(s.transform).some((v, i) => Math.abs(v - (i % 5 === 0 ? 1 : 0)) > 1e-12)) autoGuessGuides();
        }
        else setTool('landmark');
        break;
      case 'p':
        setTool('paint');
        break;
      case 'g':
        if (s.committed && !s.preview) setTool('sculpt');
        break;
      case 'e':
        set({ brush: { ...s.brush, erase: !s.brush.erase } });
        break;
      case '[':
        if (s.tool === 'sculpt') set({ sculpt: { ...s.sculpt, radius: Math.max(0.005, s.sculpt.radius / 1.2) } });
        else set({ brush: { ...s.brush, radius: Math.max(0.005, s.brush.radius / 1.2) } });
        break;
      case ']':
        if (s.tool === 'sculpt') set({ sculpt: { ...s.sculpt, radius: Math.min(0.2, s.sculpt.radius * 1.2) } });
        else set({ brush: { ...s.brush, radius: Math.min(0.4, s.brush.radius * 1.2) } });
        break;
      case 't':
      case 'r':
      case 's': {
        const mode = e.key === 't' ? 'translate' : e.key === 'r' ? 'rotate' : 'scale';
        set({ display: { ...d, gizmo: d.gizmo === mode ? 'off' : mode } });
        break;
      }
      case 'Delete':
      case 'Backspace':
        if (s.selectedLandmarkId !== null) deleteLandmark(s.selectedLandmarkId);
        break;
      case '?':
        set({ helpOpen: true });
        break;
      default:
        return;
    }
    e.preventDefault();
  };
  window.addEventListener('keydown', onKey);
  return () => window.removeEventListener('keydown', onKey);
}
