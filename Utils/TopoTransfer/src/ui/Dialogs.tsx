import { ReactNode } from 'react';
import { set, useStore } from '../state/store';
import { Kbd } from './components/controls';

function Modal(props: { title: string; onClose: () => void; children: ReactNode; footer?: ReactNode }) {
  return (
    <div className="modal-backdrop" onMouseDown={props.onClose}>
      <div className="modal" onMouseDown={(e) => e.stopPropagation()} role="dialog" aria-label={props.title}>
        <header>
          <span>{props.title}</span>
          <button className="icon-btn" onClick={props.onClose} aria-label="Close">
            ×
          </button>
        </header>
        <div className="modal-body">{props.children}</div>
        {props.footer && <footer>{props.footer}</footer>}
      </div>
    </div>
  );
}

export function HelpDialog() {
  const open = useStore((s) => s.helpOpen);
  if (!open) return null;
  const rows: [string, string][] = [
    ['Ctrl+O', 'Open mesh files'],
    ['F', 'Frame all'],
    ['1 / 2 / 3', 'Shaded / wireframe / shaded + wire'],
    ['B / N', 'Toggle Base / Reference visibility'],
    ['X', 'Toggle Reference transparency'],
    ['O', 'Toggle original (undeformed) overlay'],
    ['H', 'Cycle colour: plain → distance → displacement'],
    ['L', 'Landmark placement tool'],
    ['Drag a dot', 'Guides: move it across the mesh (Mirror applies on release)'],
    ['P', 'Region paint tool (left-drag paint, right-drag orbit)'],
    ['E', 'Toggle paint / erase'],
    ['[ / ]', 'Brush smaller / larger'],
    ['T / R / S', 'Alignment gizmo: move / rotate / uniform scale'],
    ['Del', 'Delete selected landmark'],
    ['Ctrl+Enter', 'Run wrap, or commit the preview'],
    ['Esc', 'Cancel running wrap / leave tool / hide gizmo'],
    ['Ctrl+Z / Ctrl+Shift+Z', 'Undo / redo'],
    ['Ctrl+E', 'Export'],
  ];
  return (
    <Modal title="TopoTransfer — workflow & shortcuts" onClose={() => set({ helpOpen: false })}>
      <ol className="workflow">
        <li>
          <b>Meshes</b>: a Base (OBJ/PLY, the topology to keep) and a Reference (OBJ/PLY/STL, the shape to match). Inner parts such as eyes are set to
          Follow automatically.
        </li>
        <li>
          <b>Align</b>: Auto align (bounding boxes, then ICP, with uniform scale so heads of any size match).
        </li>
        <li>
          <b>Guides</b> (recommended): the meshes side by side; click a point on the Base, then the same spot on the Reference — each pair has its own
          colour. Face or Body set asks for named points; Mirror fills the other side; Ctrl+Z undoes a point. Best way to stop vertices sliding.
        </li>
        <li>
          <b>Fit</b>: set Detail and Quality, run, check the colours and numbers, then Keep or Discard. Regions and all other settings are under More.
        </li>
        <li>
          <b>Export</b> OBJ or PLY — topology is verified by re-importing the file before download.
        </li>
      </ol>
      <table className="shortcuts">
        <tbody>
          {rows.map(([k, v]) => (
            <tr key={k}>
              <td>
                {k.split(' / ').map((p, i) => (
                  <span key={i}>
                    {i > 0 && ' / '}
                    <Kbd>{p}</Kbd>
                  </span>
                ))}
              </td>
              <td>{v}</td>
            </tr>
          ))}
        </tbody>
      </table>
      <p className="muted small">
        Mouse: left-drag orbit, right-drag pan, wheel zoom. Everything runs locally in your browser; no mesh, landmark or project data is uploaded.
      </p>
    </Modal>
  );
}
