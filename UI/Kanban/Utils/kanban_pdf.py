from __future__ import absolute_import
# coding: utf-8
'''
MutantKanban - PDF Export
Generates a styled, print-ready PDF from kanban card data.

Dependencies: Qt PrintSupport (QPrinter) — bundled with Maya.

www.mutanttools.com
author:  Esteban Rodriguez <info@renderdemartes.com>
'''

import os
import datetime

try:
    from PySide6 import QtGui, QtCore, QtWidgets
    _PYSIDE6 = True
except ImportError:
    from PySide2 import QtGui, QtCore, QtWidgets
    _PYSIDE6 = False

from maya import cmds

try:
    import importlib; from importlib import reload
except ImportError:
    import imp; from imp import reload

from Mutant_Tools.UI.Kanban.Utils import kanban_util

# Same palette as the board columns
COL_HEADER_COLORS = [
    '#34495e', '#2c5f4a', '#5c3a2e', '#4a2c5e',
    '#2e4a5e', '#5e4a2c', '#2c2c5e', '#5e2c2c',
    '#2c5e5e', '#4a5e2c',
]

# -------------------------------------------------------
# HTML helpers

def _esc(text):
    """Minimal HTML-escape."""
    return (str(text or '')
            .replace('&', '&amp;')
            .replace('<', '&lt;')
            .replace('>', '&gt;')
            .replace('"', '&quot;'))


def _img_data_uri(encoded):
    """
    Return an inline base64 data URI for the image so QTextDocument never
    needs to load a local file (file:/// URIs are unreliable in QTextDocument).
    Returns '' if the image is missing/invalid.
    """
    if not encoded:
        return ''
    # Normalise: strip b'...' wrapper that older Python repr may add
    clean = str(encoded)
    if clean.startswith("b'") and clean.endswith("'"):
        clean = clean[2:-1]
    pad = len(clean) % 4
    if pad:
        clean += '=' * (4 - pad)
    return 'data:image/jpeg;base64,{}'.format(clean)


# -------------------------------------------------------
# Card HTML

def _card_html(data):
    """Return the HTML table block for one card (dark theme)."""
    title       = _esc(data.get('title', 'Untitled'))
    notes       = _esc(data.get('notes', ''))
    priority    = int(data.get('priority', 1))
    tags_raw    = str(data.get('tags', ''))
    user        = _esc(data.get('user', ''))
    date        = _esc(data.get('date', ''))
    encoded     = data.get('image', '')
    camera      = _esc(data.get('camera', ''))
    time_slider = _esc(str(data.get('time_slider', '')))
    cam_xform   = str(data.get('camera_xform', '') or '')

    p_color = kanban_util.PRIORITY_COLORS.get(priority, '#4a90e2')
    p_label = (kanban_util.PRIORITY_LABELS[priority]
               if 0 <= priority < len(kanban_util.PRIORITY_LABELS) else 'Low')

    # --- image (inline data URI — reliable in QTextDocument) ---
    data_uri = _img_data_uri(encoded)
    img_block = ''
    if data_uri:
        img_block = (
            '<tr><td colspan="2" style="padding:0 12px 8px 14px;">'
            '<img src="{src}" width="260" />'
            '</td></tr>'.format(src=data_uri)
        )

    # --- notes (keep line breaks) ---
    notes_block = ''
    if notes:
        notes_display = notes.replace('&#10;', '<br>').replace('\n', '<br>')
        notes_block = (
            '<tr><td colspan="2" style="padding:0 12px 6px 14px;">'
            '<span style="font-size:11px;color:#b0b8c8;">{}</span>'
            '</td></tr>'.format(notes_display)
        )

    # --- tags ---
    tags_block = ''
    if tags_raw:
        pills = ''
        for t in (t.strip() for t in tags_raw.split(',') if t.strip()):
            pills += (
                '<span style="background:#1a3a5c;color:#7ab4e0;'
                'padding:2px 7px;font-size:9px;margin-right:3px;">'
                '{}</span>'.format(_esc(t))
            )
        if pills:
            tags_block = (
                '<tr><td colspan="2" style="padding:0 12px 6px 14px;">'
                '{}</td></tr>'.format(pills)
            )

    # --- metadata (camera + time slider) ---
    meta_rows = ''
    if camera:
        meta_rows += (
            '<tr>'
            '<td style="width:90px;font-size:9px;color:#667788;'
            'padding:2px 4px 2px 0;">Camera</td>'
            '<td style="font-size:9px;color:#99aabb;padding:2px 0;">{cam}</td>'
            '</tr>'.format(cam=camera)
        )
    if time_slider:
        try:
            frame_label = 'Frame {:.1f}'.format(float(time_slider))
        except ValueError:
            frame_label = time_slider
        meta_rows += (
            '<tr>'
            '<td style="width:90px;font-size:9px;color:#667788;'
            'padding:2px 4px 2px 0;">Time Slider</td>'
            '<td style="font-size:9px;color:#99aabb;padding:2px 0;">{f}</td>'
            '</tr>'.format(f=frame_label)
        )
    if cam_xform:
        meta_rows += (
            '<tr>'
            '<td style="width:90px;font-size:9px;color:#667788;'
            'padding:2px 4px 4px 0;vertical-align:top;">Cam Matrix</td>'
            '<td style="font-size:8px;color:#556677;padding:2px 0;'
            'word-break:break-all;">{xf}</td>'
            '</tr>'.format(xf=_esc(cam_xform))
        )
    meta_block = ''
    if meta_rows:
        meta_block = (
            '<tr><td colspan="2" style="padding:4px 12px 4px 14px;'
            'border-top:1px solid #2e3a4a;">'
            '<table cellspacing="0" cellpadding="0" width="100%">{}</table>'
            '</td></tr>'.format(meta_rows)
        )

    # --- footer (user / date) ---
    footer_block = ''
    if user or date:
        footer_block = (
            '<tr><td colspan="2" style="font-size:9px;color:#556677;'
            'border-top:1px solid #2e3a4a;padding:5px 12px 8px 14px;">'
            '{user} &nbsp;&middot;&nbsp; {date}'
            '</td></tr>'.format(user=user, date=date)
        )

    return '''
<table width="100%" cellspacing="0" cellpadding="0"
 style="background:#252d3a;border:1px solid #2e3a4a;border-left:4px solid {p_color};margin-bottom:8px;">
  <tr>
    <!-- header row (title + badge) -->
    <td style="padding:10px 12px 6px 14px;">
      <table width="100%" cellspacing="0" cellpadding="0">
        <tr>
          <td style="font-size:13px;font-weight:bold;color:#e8edf4;">{title}</td>
          <td align="right" width="56">
            <span style="background:{p_color};color:#ffffff;
                         font-size:9px;font-weight:bold;padding:2px 7px;">
              {p_label}
            </span>
          </td>
        </tr>
      </table>
    </td>
  </tr>
  {img_block}
  {notes_block}
  {tags_block}
  {meta_block}
  {footer_block}
</table>'''.format(
        p_color=p_color, title=title, p_label=p_label,
        img_block=img_block, notes_block=notes_block,
        tags_block=tags_block, meta_block=meta_block,
        footer_block=footer_block,
    )


# -------------------------------------------------------
# Full document HTML

def _build_html(columns_items, scene_name=''):
    """
    Build a complete HTML document.
    columns_items: list of (column_name, [data_dict, ...])
    """
    now = datetime.datetime.now().strftime('%B %d, %Y  %H:%M')
    total = sum(len(cards) for _, cards in columns_items)

    header = '''
<table width="100%" cellspacing="0" cellpadding="0"
 style="background:#1a1a2e;margin-bottom:20px;">
  <tr>
    <td style="padding:22px 28px 18px 28px;">
      <p style="font-size:20px;font-weight:bold;color:#ffffff;margin:0;
                letter-spacing:1px;">MUTANT KANBAN</p>
      <p style="font-size:11px;color:#8899bb;margin:3px 0 0 0;">{scene}</p>
      <table width="100%" cellspacing="0" cellpadding="0"
       style="margin-top:10px;">
        <tr>
          <td style="font-size:10px;color:#667788;">
            Exported: {date}
          </td>
          <td align="right" style="font-size:10px;color:#667788;">
            {cols} column{cs} &nbsp;&middot;&nbsp; {total} card{ts}
          </td>
        </tr>
      </table>
    </td>
  </tr>
</table>
'''.format(
        scene=_esc(scene_name or 'Untitled Scene'),
        date=now,
        cols=len(columns_items),
        cs='' if len(columns_items) == 1 else 's',
        total=total,
        ts='' if total == 1 else 's',
    )

    body = header

    for idx, (col_name, cards) in enumerate(columns_items):
        col_color = COL_HEADER_COLORS[idx % len(COL_HEADER_COLORS)]

        # Column header
        body += '''
<table width="100%" cellspacing="0" cellpadding="0"
 style="background:{col_color};margin-bottom:6px;page-break-before:{pb};">
  <tr>
    <td style="padding:9px 14px;">
      <span style="font-size:12px;font-weight:bold;color:#ffffff;">
        {col}
      </span>
      &nbsp;&nbsp;
      <span style="background:rgba(255,255,255,0.9);color:{col_color};
                   font-size:9px;font-weight:bold;padding:2px 7px;">
        {count}
      </span>
    </td>
  </tr>
</table>
'''.format(
            col_color=col_color,
            col=_esc(col_name),
            count=len(cards),
            pb='always' if idx > 0 else 'auto',
        )

        if cards:
            for card in cards:
                body += _card_html(card)
        else:
            body += (
                '<p style="color:#556677;font-size:10px;'
                'font-style:italic;margin:2px 0 10px 8px;">'
                'No cards in this column.</p>'
            )

        body += '<br>'

    # Page-number note at the very end
    body += (
        '<p style="font-size:9px;color:#445566;text-align:center;'
        'margin-top:20px;border-top:1px solid #2e3a4a;padding-top:8px;">'
        'Generated by Mutant Tools &nbsp;&middot;&nbsp; mutanttools.com'
        '</p>'
    )

    return (
        '<!DOCTYPE html><html><head><meta charset="UTF-8">'
        '<style>html,body{{font-family:Arial,Helvetica,sans-serif;'
        'color:#c8d4e0;background:#1a2130;font-size:12px;margin:0;padding:0;}}'
        'p{{margin:2px 0;}}</style>'
        '</head><body style="background:#1a2130;">{}</body></html>'.format(body)
    )


# -------------------------------------------------------
# Printer / render

def _get_printer():
    """Return a configured QPrinter, or None if unavailable."""
    try:
        from PySide6.QtPrintSupport import QPrinter
        from PySide6.QtGui import QPageSize, QPageLayout
        p = QPrinter(QPrinter.HighResolution)
        p.setOutputFormat(QPrinter.PdfFormat)
        try:
            p.setPageSize(QPageSize(QPageSize.A4))
            p.setPageMargins(QtCore.QMarginsF(0, 0, 0, 0),
                             QPageLayout.Millimeter)
        except Exception:
            pass
        return p
    except ImportError:
        pass

    try:
        from PySide2.QtPrintSupport import QPrinter
        p = QPrinter(QPrinter.HighResolution)
        p.setOutputFormat(QPrinter.PdfFormat)
        try:
            p.setPageSize(QPrinter.A4)
            p.setPageMargins(0, 0, 0, 0, QPrinter.Millimeter)
        except Exception:
            pass
        return p
    except ImportError:
        pass

    return None


def _render(html, path):
    """Render html string to a PDF file. Returns True on success."""
    printer = _get_printer()
    if printer is None:
        cmds.warning(
            'MutantKanban: QPrintSupport not available in this build. '
            'Cannot export PDF.')
        return False

    printer.setOutputFileName(path)
    doc = QtGui.QTextDocument()
    doc.setHtml(html)
    # A4 in points (595 x 842) — avoids calling pageRect() which needs a Unit arg
    doc.setPageSize(QtCore.QSizeF(595, 842))

    try:
        doc.print_(printer)       # PySide2 and PySide6 both expose print_
    except Exception as e:
        cmds.warning('MutantKanban: PDF render error: {}'.format(e))
        return False

    return True


# -------------------------------------------------------
# Column resolver

def _column_for_node(node):
    """Reverse-map a node's Maya parent group back to a column label."""
    parents = cmds.listRelatives(node, parent=True) or []
    if not parents:
        return ''
    parent_name = parents[0]
    for col in kanban_util.get_columns():
        if kanban_util.node_name_for_column(col) == parent_name:
            return col
    return parent_name


# -------------------------------------------------------
# File dialog

def _scene_dir():
    """Return the directory of the current scene, or ~ as fallback."""
    full = cmds.file(q=True, sn=True) or ''
    if full:
        d = os.path.dirname(full)
        if d and os.path.isdir(d):
            return d
    return os.path.expanduser('~')


def _scene_prefix():
    """Return a filesystem-safe scene name prefix like 'myScene_'."""
    raw = cmds.file(q=True, sn=True, shortName=True) or ''
    name = os.path.splitext(raw)[0]  # strip .ma / .mb
    import re as _re
    safe = _re.sub(r'[^A-Za-z0-9_-]', '_', name).strip('_')
    return (safe + '_') if safe else ''


def _ask_save_path(default='kanban_export'):
    path, _ = QtWidgets.QFileDialog.getSaveFileName(
        None,
        'Export Kanban to PDF',
        os.path.join(_scene_dir(), '{}.pdf'.format(default)),
        'PDF Files (*.pdf)',
    )
    return path or ''


# -------------------------------------------------------
# Public API

def export_card_to_pdf(node):
    """Export a single card to its own PDF."""
    data = kanban_util.get_note_data(node)
    if not data:
        cmds.warning('MutantKanban: No data for node: {}'.format(node))
        return

    title_safe = str(data.get('title', 'card')).replace(' ', '_')
    path = _ask_save_path(default='{}kanban_{}'.format(_scene_prefix(), title_safe))
    if not path:
        return

    col = _column_for_node(node)
    scene = cmds.file(q=True, sn=True, shortName=True) or 'Untitled Scene'
    html = _build_html([(col, [data])], scene_name=scene)

    if _render(html, path):
        print('MutantKanban: Exported card to {}'.format(path))


def export_column_to_pdf(column_name):
    """Export all cards in a column to PDF."""
    nodes = kanban_util.get_notes_in_column(column_name)
    cards = [c for c in (kanban_util.get_note_data(n) for n in nodes) if c]

    path = _ask_save_path(
        default='{}kanban_{}'.format(_scene_prefix(), column_name.replace(' ', '_')))
    if not path:
        return

    scene = cmds.file(q=True, sn=True, shortName=True) or 'Untitled Scene'
    html = _build_html([(column_name, cards)], scene_name=scene)

    if _render(html, path):
        print('MutantKanban: Exported column "{}" to {}'.format(
            column_name, path))


def export_all_to_pdf():
    """Export every column and all cards to a single PDF."""
    columns = kanban_util.get_columns()
    items = []
    for col in columns:
        nodes = kanban_util.get_notes_in_column(col)
        cards = [c for c in (kanban_util.get_note_data(n) for n in nodes) if c]
        items.append((col, cards))

    path = _ask_save_path(default='{}kanban_full_export'.format(_scene_prefix()))
    if not path:
        return

    scene = cmds.file(q=True, sn=True, shortName=True) or 'Untitled Scene'
    html = _build_html(items, scene_name=scene)

    if _render(html, path):
        print('MutantKanban: Exported full board to {}'.format(path))
