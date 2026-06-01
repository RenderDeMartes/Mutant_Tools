from __future__ import absolute_import
# coding: utf-8
'''
version: 1.0.0
date: 31/05/2026

#----------------
content:
MutantKanban - Main UI
An in-Maya Kanban board. Data lives in the scene under the MutantKanban group.

#----------------
how to:

try:
	import importlib;from importlib import reload
except:
	import imp;from imp import reload

import Mutant_Tools
from Mutant_Tools.UI.Kanban import load_kanban
reload(load_kanban)

try:cKanbanUI.close()
except:pass
cKanbanUI = load_kanban.KanbanUI()
cKanbanUI.show()

#----------------
dependencies:

PySide6 / PySide2
maya.cmds
Mutant_Tools.UI.Kanban.Utils.kanban_util
Mutant_Tools.UI.QtMutantWindow

#----------------
www.mutanttools.com
author:  Esteban Rodriguez <info@renderdemartes.com>

'''

try:
    from shiboken6 import wrapInstance
    from PySide6 import QtGui, QtCore, QtUiTools, QtWidgets
    from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                                   QPushButton, QFrame, QScrollArea, QDialog,
                                   QLineEdit, QPlainTextEdit, QComboBox,
                                   QListWidget, QAbstractItemView, QGroupBox,
                                   QInputDialog, QApplication, QSizePolicy,
                                   QMenu, QAbstractScrollArea)
    from PySide6.QtCore import Signal
except Exception:
    from shiboken2 import wrapInstance
    from PySide2 import QtGui, QtCore, QtUiTools, QtWidgets
    from PySide2.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                                   QPushButton, QFrame, QScrollArea, QDialog,
                                   QLineEdit, QPlainTextEdit, QComboBox,
                                   QListWidget, QAbstractItemView, QGroupBox,
                                   QInputDialog, QApplication, QSizePolicy,
                                   QMenu, QAbstractScrollArea)
    from PySide2.QtCore import Signal

import maya.OpenMayaUI as omui
from functools import partial
import maya.cmds as cmds
import maya.mel as mel

import os
import sys
import json
import math
from pathlib import Path

try:
    import importlib
    from importlib import reload
except Exception:
    import imp
    from imp import reload

import Mutant_Tools.UI
from Mutant_Tools.UI import QtMutantWindow
reload(QtMutantWindow)

import Mutant_Tools
from Mutant_Tools.UI.Kanban.Utils import kanban_util
reload(kanban_util)

# -------------------------------------------------------
# Path constants

Title = 'MutantKanban'
PATH = os.path.dirname(__file__)
_parts = Path(PATH).parts[:-2]
FOLDER = os.path.join(*_parts) if len(_parts) > 1 else _parts[0]

ICONS_PATH = os.path.join(FOLDER, 'Icons')
NOTES_RES = os.path.join(FOLDER, 'UI', 'Notes', 'Resources')
STYLESHEETS_PATH = os.path.join(FOLDER, 'UI', 'Stylesheets')

# MIME type for drag-and-drop between columns
MIME_TYPE = 'application/x-mutant-kanban'

# Column header palette (cycles when more columns than colours)
COL_HEADER_COLORS = [
    '#34495e', '#2c5f4a', '#5c3a2e', '#4a2c5e', '#2e4a5e',
    '#5e4a2c', '#2c2c5e', '#5e2c2c', '#2c5e5e', '#4a5e2c',
]


# -------------------------------------------------------
# Small utilities

def _load_css():
    css_file = os.path.join(STYLESHEETS_PATH, 'FramelessMutant.css')
    if os.path.exists(css_file):
        with open(css_file) as fh:
            return fh.read()
    return ''


def _icon(name, folder=None):
    """
    Return a QIcon, searching in order:
      1. folder (if explicitly supplied)
      2. ICONS_PATH  (root Icons/ folder in the repo)
      3. NOTES_RES   (UI/Notes/Resources fallback)
    """
    search = []
    if folder is not None:
        search.append(folder)
    search.extend([ICONS_PATH, NOTES_RES])
    for d in search:
        path = os.path.join(d, name)
        if os.path.exists(path):
            return QtGui.QIcon(path)
    return QtGui.QIcon()


def _make_icon_btn(icon_name, tooltip='', size=20, folder=None):
    """Create a small flat icon button."""
    btn = QPushButton()
    btn.setFixedSize(size, size)
    btn.setToolTip(tooltip)
    btn.setFlat(True)
    btn.setCursor(QtCore.Qt.PointingHandCursor)
    ico = _icon(icon_name, folder)
    if not ico.isNull():
        btn.setIcon(ico)
        btn.setIconSize(QtCore.QSize(size - 2, size - 2))
    else:
        btn.setText(tooltip[:1])
    return btn


# ========================================================
# IMAGE ANNOTATOR  –  draw on a screenshot before saving
# ========================================================

class DrawingCanvas(QWidget):
    """
    Widget that displays a base QPixmap and lets the user draw on top.
    Supported tools: pencil (freehand), ellipse, arrow.
    """

    def __init__(self, pixmap, parent=None):
        super(DrawingCanvas, self).__init__(parent)
        self._base = pixmap.copy()
        self._annotations = []       # list of finished stroke dicts
        self._current = None         # stroke in progress
        self.tool = 'pencil'         # 'pencil' | 'ellipse' | 'arrow'
        self.pen_color = QtGui.QColor('#ff3333')
        self.pen_width = 3
        self.setMinimumSize(self._base.size())
        self.setMouseTracking(True)
        self.setCursor(QtCore.Qt.CrossCursor)

    # ------------------------------------------------------------------
    def set_tool(self, tool):
        self.tool = tool

    def set_color(self, color):
        self.pen_color = QtGui.QColor(color)

    def set_width(self, width):
        self.pen_width = int(width)

    def undo(self):
        if self._annotations:
            self._annotations.pop()
            self.update()

    def clear_annotations(self):
        self._annotations = []
        self._current = None
        self.update()

    def flat_pixmap(self):
        """Return a QPixmap with all annotations rendered onto the base image."""
        result = self._base.copy()
        painter = QtGui.QPainter(result)
        self._render_strokes(painter, self._annotations)
        painter.end()
        return result

    # ------------------------------------------------------------------
    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        # Scale base image to fill the widget while keeping aspect ratio
        scaled = self._base.scaled(
            self.size(), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
        x_off = (self.width() - scaled.width()) // 2
        y_off = (self.height() - scaled.height()) // 2
        painter.drawPixmap(x_off, y_off, scaled)
        # Compute scale factors so stroke coords map correctly
        sx = scaled.width() / float(self._base.width())
        sy = scaled.height() / float(self._base.height())
        painter.translate(x_off, y_off)
        painter.scale(sx, sy)
        self._render_strokes(painter, self._annotations)
        if self._current:
            self._render_strokes(painter, [self._current])
        painter.end()

    def _render_strokes(self, painter, strokes):
        for s in strokes:
            pen = QtGui.QPen(QtGui.QColor(s['color']),
                             s['width'],
                             QtCore.Qt.SolidLine,
                             QtCore.Qt.RoundCap,
                             QtCore.Qt.RoundJoin)
            painter.setPen(pen)
            painter.setBrush(QtCore.Qt.NoBrush)
            pts = s['points']
            if not pts:
                continue
            if s['type'] == 'pencil':
                if len(pts) == 1:
                    painter.drawPoint(pts[0])
                else:
                    poly = QtGui.QPolygon(pts)
                    painter.drawPolyline(poly)
            elif s['type'] == 'ellipse':
                if len(pts) >= 2:
                    rect = QtCore.QRect(pts[0], pts[-1]).normalized()
                    painter.drawEllipse(rect)
            elif s['type'] == 'arrow':
                if len(pts) >= 2:
                    p1, p2 = pts[0], pts[-1]
                    painter.drawLine(p1, p2)
                    # Arrowhead
                    angle = math.atan2(p1.y() - p2.y(), p1.x() - p2.x())
                    tip_len = max(12, s['width'] * 4)
                    for da in (0.45, -0.45):
                        tip = QtCore.QPoint(
                            int(p2.x() + tip_len * math.cos(angle + da)),
                            int(p2.y() + tip_len * math.sin(angle + da)),
                        )
                        painter.drawLine(p2, tip)

    # ------------------------------------------------------------------
    def _widget_to_image_pt(self, pos):
        """Convert a widget-space QPoint to image-space QPoint."""
        scaled = self._base.scaled(
            self.size(), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
        x_off = (self.width() - scaled.width()) // 2
        y_off = (self.height() - scaled.height()) // 2
        sx = self._base.width() / float(scaled.width())
        sy = self._base.height() / float(scaled.height())
        ix = int((pos.x() - x_off) * sx)
        iy = int((pos.y() - y_off) * sy)
        return QtCore.QPoint(
            max(0, min(ix, self._base.width() - 1)),
            max(0, min(iy, self._base.height() - 1)),
        )

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            pt = self._widget_to_image_pt(event.pos())
            self._current = {
                'type': self.tool,
                'color': self.pen_color.name(),
                'width': self.pen_width,
                'points': [pt],
            }
            self.update()

    def mouseMoveEvent(self, event):
        if self._current and (event.buttons() & QtCore.Qt.LeftButton):
            pt = self._widget_to_image_pt(event.pos())
            if self.tool == 'pencil':
                self._current['points'].append(pt)
            else:
                # For ellipse / arrow only keep first + latest point
                self._current['points'] = [self._current['points'][0], pt]
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton and self._current:
            pt = self._widget_to_image_pt(event.pos())
            if self.tool != 'pencil':
                self._current['points'] = [self._current['points'][0], pt]
            if len(self._current['points']) >= 1:
                self._annotations.append(self._current)
            self._current = None
            self.update()


# --------------------------------------------------------

class ImageAnnotatorDialog(QDialog):
    """
    Full-screen-ish dialog to annotate a screenshot before saving it.
    Returns the annotated QPixmap via .get_result(), or None if cancelled.
    """

    COLORS = [
        ('#ff3333', 'Red'),
        ('#ff9900', 'Orange'),
        ('#ffff00', 'Yellow'),
        ('#33ff33', 'Green'),
        ('#33ccff', 'Cyan'),
        ('#ffffff', 'White'),
        ('#000000', 'Black'),
    ]

    def __init__(self, pixmap, parent=None):
        super(ImageAnnotatorDialog, self).__init__(parent)
        self.setWindowTitle('Annotate Screenshot')
        self.setModal(True)
        self._result_pixmap = None
        self._build_ui(pixmap)
        self.setStyleSheet(_load_css())
        # Size to fit the image comfortably
        w = min(pixmap.width() + 40, 1400)
        h = min(pixmap.height() + 130, 900)
        self.resize(w, h)

    def _build_ui(self, pixmap):
        layout = QVBoxLayout(self)
        layout.setSpacing(6)
        layout.setContentsMargins(8, 8, 8, 8)

        # ---- Toolbar ----
        toolbar = QWidget()
        toolbar.setFixedHeight(44)
        tlay = QHBoxLayout(toolbar)
        tlay.setSpacing(6)
        tlay.setContentsMargins(6, 4, 6, 4)

        # Tool buttons
        def _tool_btn(label, tip, tool_name):
            b = QPushButton(label)
            b.setFixedSize(90, 32)
            b.setCheckable(True)
            b.setToolTip(tip)
            b.setCursor(QtCore.Qt.PointingHandCursor)
            b.clicked.connect(lambda: self._set_tool(tool_name))
            return b

        self._pencil_btn = _tool_btn('✏  Pencil', 'Freehand draw', 'pencil')
        self._ellipse_btn = _tool_btn('⬭  Ellipse', 'Draw an ellipse/circle', 'ellipse')
        self._arrow_btn = _tool_btn('→  Arrow', 'Draw an arrow', 'arrow')
        self._tool_group = [self._pencil_btn, self._ellipse_btn, self._arrow_btn]
        self._pencil_btn.setChecked(True)

        for b in self._tool_group:
            tlay.addWidget(b)

        tlay.addWidget(_vsep())

        # Color swatches
        self._active_color = self.COLORS[0][0]
        self._color_btns = []
        for hex_color, name in self.COLORS:
            cb = QPushButton()
            cb.setFixedSize(26, 26)
            cb.setToolTip(name)
            cb.setCursor(QtCore.Qt.PointingHandCursor)
            cb.setStyleSheet(
                'background: {c}; border: 2px solid #555; border-radius: 4px;'
                .format(c=hex_color))
            cb.clicked.connect(partial(self._set_color, hex_color))
            self._color_btns.append(cb)
            tlay.addWidget(cb)
        self._highlight_color_btn(self.COLORS[0][0])

        tlay.addWidget(_vsep())

        # Pen size
        from PySide6.QtWidgets import QSlider
        try:
            from PySide6.QtWidgets import QSlider
        except Exception:
            from PySide2.QtWidgets import QSlider
        size_lbl = QLabel('Size:')
        self._size_slider = QSlider(QtCore.Qt.Horizontal)
        self._size_slider.setRange(1, 16)
        self._size_slider.setValue(3)
        self._size_slider.setFixedWidth(80)
        self._size_slider.valueChanged.connect(self._set_width)
        tlay.addWidget(size_lbl)
        tlay.addWidget(self._size_slider)

        tlay.addWidget(_vsep())

        undo_btn = QPushButton('↩ Undo')
        undo_btn.setFixedHeight(30)
        undo_btn.clicked.connect(self._undo)
        clear_btn = QPushButton('Clear')
        clear_btn.setFixedHeight(30)
        clear_btn.clicked.connect(self._clear)
        tlay.addWidget(undo_btn)
        tlay.addWidget(clear_btn)
        tlay.addStretch()

        layout.addWidget(toolbar)

        # ---- Canvas ----
        canvas_scroll = QScrollArea()
        canvas_scroll.setWidgetResizable(True)
        canvas_scroll.setFrameShape(QFrame.NoFrame)
        self._canvas = DrawingCanvas(pixmap)
        canvas_scroll.setWidget(self._canvas)
        layout.addWidget(canvas_scroll, 1)

        # ---- Accept / Cancel ----
        btn_row = QHBoxLayout()
        btn_row.addStretch()
        accept_btn = QPushButton('✔  Accept Annotation')
        accept_btn.setMinimumWidth(160)
        accept_btn.setFixedHeight(32)
        accept_btn.setStyleSheet('font-weight: bold; color: #7dff7d;')
        accept_btn.clicked.connect(self._accept)
        cancel_btn = QPushButton('Cancel')
        cancel_btn.setFixedHeight(32)
        cancel_btn.clicked.connect(self.reject)
        btn_row.addWidget(accept_btn)
        btn_row.addWidget(cancel_btn)
        layout.addLayout(btn_row)

    # ------------------------------------------------------------------
    def _vsep(self):
        sep = QFrame()
        sep.setFrameShape(QFrame.VLine)
        sep.setFixedWidth(2)
        return sep

    def _set_tool(self, tool):
        self._canvas.set_tool(tool)
        for b in self._tool_group:
            b.setChecked(False)
        mapping = {'pencil': self._pencil_btn,
                   'ellipse': self._ellipse_btn,
                   'arrow': self._arrow_btn}
        if tool in mapping:
            mapping[tool].setChecked(True)

    def _set_color(self, hex_color):
        self._active_color = hex_color
        self._canvas.set_color(hex_color)
        self._highlight_color_btn(hex_color)

    def _highlight_color_btn(self, hex_color):
        for i, (hc, _) in enumerate(self.COLORS):
            border = '#ffffff' if hc == hex_color else '#555'
            self._color_btns[i].setStyleSheet(
                'background: {c}; border: 2px solid {b}; border-radius: 4px;'
                .format(c=hc, b=border))

    def _set_width(self, val):
        self._canvas.set_width(val)

    def _undo(self):
        self._canvas.undo()

    def _clear(self):
        self._canvas.clear_annotations()

    def _accept(self):
        self._result_pixmap = self._canvas.flat_pixmap()
        self.accept()

    def get_result(self):
        """Returns the annotated QPixmap, or None if cancelled."""
        return self._result_pixmap


def _vsep():
    """Standalone vertical separator for toolbars."""
    sep = QFrame()
    sep.setFrameShape(QFrame.VLine)
    sep.setFrameShadow(QFrame.Sunken)
    sep.setFixedWidth(2)
    return sep


# ========================================================
# CREATE / EDIT CARD DIALOG
# ========================================================

class CardDialog(QDialog):
    """Modal dialog for creating or editing a Kanban card."""

    def __init__(self, parent=None, columns=None, current_column='Backlog',
                 node_data=None):
        super(CardDialog, self).__init__(parent)
        self.columns = columns or ['Backlog']
        self.current_column = current_column
        self.node_data = node_data          # None → create mode
        self._encoded_image = (node_data.get('image', '') or '') if node_data else ''

        is_edit = node_data is not None
        self.setWindowTitle('Edit Card' if is_edit else 'New Card')
        self.setMinimumWidth(500)
        # Non-modal but always on top so the viewport stays interactable
        self.setWindowFlags(
            self.windowFlags()
            | QtCore.Qt.Window
            | QtCore.Qt.WindowStaysOnTopHint
        )
        self._build_ui()
        self.setStyleSheet(_load_css())
        if is_edit:
            self._populate(node_data)

    # ------------------------------------------------------------------
    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(8)
        layout.setContentsMargins(14, 14, 14, 14)

        # Title
        row = QHBoxLayout()
        lbl = QLabel('Title:')
        lbl.setFixedWidth(65)
        self.title_edit = QLineEdit()
        self.title_edit.setPlaceholderText('Task title…')
        row.addWidget(lbl)
        row.addWidget(self.title_edit)
        layout.addLayout(row)

        # Notes
        layout.addWidget(QLabel('Notes:'))
        self.notes_edit = QPlainTextEdit()
        self.notes_edit.setPlaceholderText('Details, links, context…')
        self.notes_edit.setMinimumHeight(80)
        self.notes_edit.setMaximumHeight(160)
        layout.addWidget(self.notes_edit)

        # Screenshot controls
        shot_row = QHBoxLayout()
        self.capture_btn = QPushButton('Capture Viewport')
        self.capture_btn.setIcon(_icon('capture.png'))
        self.capture_btn.clicked.connect(self._capture)
        self.annotate_btn = QPushButton('Annotate')
        self.annotate_btn.setIcon(_icon('draw.png'))
        self.annotate_btn.setToolTip('Draw on the current screenshot')
        self.annotate_btn.clicked.connect(self._annotate_current)
        self.clear_img_btn = QPushButton('Clear Image')
        self.clear_img_btn.setIcon(_icon('clear.png'))
        self.clear_img_btn.clicked.connect(self._clear_image)
        shot_row.addWidget(self.capture_btn)
        shot_row.addWidget(self.annotate_btn)
        shot_row.addWidget(self.clear_img_btn)
        shot_row.addStretch()
        layout.addLayout(shot_row)

        # Thumbnail preview
        self.thumb_lbl = QLabel('No screenshot')
        self.thumb_lbl.setFixedHeight(130)
        self.thumb_lbl.setAlignment(QtCore.Qt.AlignCenter)
        self.thumb_lbl.setStyleSheet(
            'border: 1px solid #444; background: #252525; border-radius: 3px; color: #666;')
        layout.addWidget(self.thumb_lbl)

        # Priority + Column
        meta_row = QHBoxLayout()
        pl = QLabel('Priority:')
        pl.setFixedWidth(55)
        self.priority_combo = QComboBox()
        self.priority_combo.addItems(kanban_util.PRIORITY_LABELS)
        self.priority_combo.setCurrentIndex(1)
        self.priority_combo.currentIndexChanged.connect(self._update_priority_style)

        cl = QLabel('Column:')
        cl.setFixedWidth(50)
        self.column_combo = QComboBox()
        self.column_combo.addItems(self.columns)
        if self.current_column in self.columns:
            self.column_combo.setCurrentIndex(self.columns.index(self.current_column))

        meta_row.addWidget(pl)
        meta_row.addWidget(self.priority_combo)
        meta_row.addSpacing(14)
        meta_row.addWidget(cl)
        meta_row.addWidget(self.column_combo)
        meta_row.addStretch()
        layout.addLayout(meta_row)

        # Tags
        tags_row = QHBoxLayout()
        tl = QLabel('Tags:')
        tl.setFixedWidth(65)
        self.tags_edit = QLineEdit()
        self.tags_edit.setPlaceholderText('comma, separated, tags')
        tags_row.addWidget(tl)
        tags_row.addWidget(self.tags_edit)
        layout.addLayout(tags_row)

        # OK / Cancel
        btn_row = QHBoxLayout()
        btn_row.addStretch()
        self.ok_btn = QPushButton('Save' if self.node_data else 'Create')
        self.ok_btn.setMinimumWidth(80)
        self.ok_btn.clicked.connect(self.accept)
        self.cancel_btn = QPushButton('Cancel')
        self.cancel_btn.clicked.connect(self.reject)
        btn_row.addWidget(self.ok_btn)
        btn_row.addWidget(self.cancel_btn)
        layout.addLayout(btn_row)

        self._update_priority_style()

    def _update_priority_style(self):
        idx = self.priority_combo.currentIndex()
        color = kanban_util.PRIORITY_COLORS.get(idx, '#4a90e2')
        self.priority_combo.setStyleSheet('color: {};'.format(color))

    def _capture(self):
        try:
            img_path = kanban_util.capture_viewport()
        except Exception as e:
            cmds.warning('MutantKanban: Capture failed: {}'.format(e))
            return
        # Auto-open annotator immediately after capture
        annotated = self._run_annotator(img_path)
        if annotated is None:
            # User cancelled annotation — keep the raw screenshot
            self._encoded_image = kanban_util.encode_image(img_path)
            self._show_thumb(img_path)
        else:
            self._apply_annotated_pixmap(annotated)

    def _annotate_current(self):
        """Open the annotator on the existing screenshot (if any)."""
        if not self._encoded_image:
            cmds.warning('MutantKanban: No screenshot to annotate. Capture one first.')
            return
        tmp = kanban_util.decode_image(self._encoded_image, 'annotate_src.jpg')
        if not tmp or not os.path.exists(tmp):
            cmds.warning('MutantKanban: Could not load image for annotation.')
            return
        annotated = self._run_annotator(tmp)
        if annotated is not None:
            self._apply_annotated_pixmap(annotated)

    def _run_annotator(self, img_path):
        """
        Load img_path into the annotator dialog.
        Returns the annotated QPixmap if accepted, else None.
        """
        pix = QtGui.QPixmap(img_path)
        if pix.isNull():
            cmds.warning('MutantKanban: Could not load image: {}'.format(img_path))
            return None
        dlg = ImageAnnotatorDialog(pix, parent=self)
        if dlg.exec_() == QDialog.Accepted:
            return dlg.get_result()
        return None

    def _apply_annotated_pixmap(self, pix):
        """Save an annotated QPixmap to disk, encode it, and show the thumb."""
        import tempfile as _tf
        out_path = os.path.join(kanban_util.temp_folder, 'annotated.jpg')
        pix.save(out_path, 'JPG', 90)
        self._encoded_image = kanban_util.encode_image(out_path)
        self._show_thumb(out_path)

    def _clear_image(self):
        self._encoded_image = ''
        self.thumb_lbl.clear()
        self.thumb_lbl.setText('No screenshot')

    def _show_thumb(self, image_path):
        if image_path and os.path.exists(image_path):
            pix = QtGui.QPixmap(image_path)
            pix = pix.scaledToHeight(128, QtCore.Qt.SmoothTransformation)
            self.thumb_lbl.setPixmap(pix)
            self.thumb_lbl.setText('')

    def _populate(self, d):
        self.title_edit.setText(d.get('title', ''))
        self.notes_edit.setPlainText(d.get('notes', ''))
        self.tags_edit.setText(d.get('tags', ''))
        pri = d.get('priority', 1)
        if isinstance(pri, int) and 0 <= pri <= 3:
            self.priority_combo.setCurrentIndex(pri)
        encoded = d.get('image', '')
        if encoded:
            node_safe = d.get('node', 'edit').replace(':', '_').replace('|', '_')
            tmp = kanban_util.decode_image(encoded, '{}_dlg.jpg'.format(node_safe))
            if tmp:
                self._show_thumb(tmp)

    # ------------------------------------------------------------------
    def get_result(self):
        return {
            'title': self.title_edit.text().strip() or 'Untitled',
            'notes': self.notes_edit.toPlainText(),
            'encoded_image': self._encoded_image,
            'priority': self.priority_combo.currentIndex(),
            'column': self.column_combo.currentText(),
            'tags': self.tags_edit.text().strip(),
        }


# ========================================================
# MANAGE COLUMNS DIALOG
# ========================================================

class ManageColumnsDialog(QDialog):
    """Add, rename, reorder, delete columns and apply presets."""

    def __init__(self, parent=None, columns=None):
        super(ManageColumnsDialog, self).__init__(parent)
        self.setWindowTitle('Manage Columns')
        self.setMinimumSize(380, 420)
        self.setModal(True)
        self._columns = list(columns or [])
        self._build_ui()
        self.setStyleSheet(_load_css())
        self._refresh_list()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(6)
        layout.setContentsMargins(14, 14, 14, 14)

        # Presets
        presets_grp = QGroupBox('Presets')
        presets_layout = QHBoxLayout(presets_grp)
        presets_layout.setSpacing(4)
        for name, cols in kanban_util.DEFAULT_COLUMN_PRESETS.items():
            btn = QPushButton(name)
            btn.setFixedHeight(24)
            btn.clicked.connect(partial(self._apply_preset, cols))
            presets_layout.addWidget(btn)
        layout.addWidget(presets_grp)

        # Column list (drag to reorder)
        cols_grp = QGroupBox('Columns  (drag rows to reorder)')
        cols_layout = QVBoxLayout(cols_grp)
        self.col_list = QListWidget()
        self.col_list.setDragDropMode(QAbstractItemView.InternalMove)
        self.col_list.setDefaultDropAction(QtCore.Qt.MoveAction)
        self.col_list.setAlternatingRowColors(True)
        cols_layout.addWidget(self.col_list)

        # Add / rename / delete row
        action_row = QHBoxLayout()
        self.col_name_edit = QLineEdit()
        self.col_name_edit.setPlaceholderText('Column name…')
        add_btn = QPushButton('Add')
        add_btn.clicked.connect(self._add_column)
        rename_btn = QPushButton('Rename')
        rename_btn.clicked.connect(self._rename_column)
        del_btn = QPushButton('Delete')
        del_btn.clicked.connect(self._delete_column)
        action_row.addWidget(self.col_name_edit)
        action_row.addWidget(add_btn)
        action_row.addWidget(rename_btn)
        action_row.addWidget(del_btn)
        cols_layout.addLayout(action_row)
        layout.addWidget(cols_grp)

        # OK / Cancel
        btn_row = QHBoxLayout()
        btn_row.addStretch()
        ok_btn = QPushButton('Apply')
        ok_btn.setMinimumWidth(80)
        ok_btn.clicked.connect(self.accept)
        cancel_btn = QPushButton('Cancel')
        cancel_btn.clicked.connect(self.reject)
        btn_row.addWidget(ok_btn)
        btn_row.addWidget(cancel_btn)
        layout.addLayout(btn_row)

    def _refresh_list(self):
        self.col_list.clear()
        for col in self._columns:
            self.col_list.addItem(col)

    def _apply_preset(self, cols):
        self._columns = list(cols)
        self._refresh_list()

    def _add_column(self):
        name = self.col_name_edit.text().strip()
        if name and name not in self._columns:
            self._columns.append(name)
            self._refresh_list()
            self.col_name_edit.clear()

    def _rename_column(self):
        item = self.col_list.currentItem()
        if not item:
            return
        new_name = self.col_name_edit.text().strip()
        if new_name and new_name not in self._columns:
            idx = self._columns.index(item.text())
            self._columns[idx] = new_name
            self._refresh_list()
            self.col_name_edit.clear()

    def _delete_column(self):
        item = self.col_list.currentItem()
        if not item:
            return
        col = item.text()
        confirm = cmds.confirmDialog(
            title='Delete Column',
            message='Delete column "{}"?\n'
                    'All cards will move to the first remaining column.'.format(col),
            button=['Delete', 'Cancel'],
            defaultButton='Cancel', cancelButton='Cancel', dismissString='Cancel',
        )
        if confirm == 'Delete':
            self._columns.remove(col)
            self._refresh_list()

    def get_columns(self):
        result = []
        for i in range(self.col_list.count()):
            result.append(self.col_list.item(i).text())
        return result


# ========================================================
# KANBAN CARD WIDGET
# ========================================================

class KanbanCardWidget(QFrame):
    """A single draggable Kanban card."""

    refresh_requested = Signal()
    card_edited = Signal(str)    # node name

    def __init__(self, node_data, column_name, parent=None):
        super(KanbanCardWidget, self).__init__(parent)
        self.node_data = dict(node_data)
        self.node = node_data['node']
        self.column_name = column_name
        self._drag_start = None

        self.setObjectName('KanbanCard')
        self.setFrameShape(QFrame.StyledPanel)
        self.setAcceptDrops(False)
        self.setCursor(QtCore.Qt.OpenHandCursor)

        priority = int(node_data.get('priority', 1))
        pcolor = kanban_util.PRIORITY_COLORS.get(priority, '#4a90e2')
        self.setStyleSheet('''
            QFrame#KanbanCard {{
                background-color: #353535;
                border: 1px solid #484848;
                border-left: 4px solid {pc};
                border-radius: 4px;
                margin: 2px 3px;
            }}
            QFrame#KanbanCard:hover {{
                background-color: #3d3d3d;
                border: 1px solid #666;
                border-left: 4px solid {pc};
            }}
        '''.format(pc=pcolor))

        self._build_ui()

    # ------------------------------------------------------------------
    def _build_ui(self):
        d = self.node_data
        layout = QVBoxLayout(self)
        layout.setSpacing(4)
        layout.setContentsMargins(8, 7, 8, 7)

        # --- Title row ---
        title_row = QHBoxLayout()
        title_row.setSpacing(6)

        title_lbl = QLabel(d.get('title', 'Untitled'))
        title_lbl.setWordWrap(True)
        title_lbl.setStyleSheet(
            'font-weight: bold; font-size: 12px; color: #e8e8e8; background: transparent;')

        priority = int(d.get('priority', 1))
        p_name = kanban_util.PRIORITY_LABELS[priority] if 0 <= priority <= 3 else 'Medium'
        p_color = kanban_util.PRIORITY_COLORS.get(priority, '#4a90e2')
        badge = QLabel(p_name)
        badge.setStyleSheet(
            'color: {c}; font-size: 9px; font-weight: bold;'
            ' border: 1px solid {c}; border-radius: 6px;'
            ' padding: 1px 6px; background: transparent;'.format(c=p_color))
        badge.setFixedHeight(16)

        title_row.addWidget(title_lbl, 1)
        title_row.addWidget(badge)
        layout.addLayout(title_row)

        # --- Thumbnail ---
        encoded = d.get('image', '')
        if encoded:
            node_safe = self.node.replace(':', '_').replace('|', '_')
            thumb_path = kanban_util.decode_image(
                encoded, '{}_thumb.jpg'.format(node_safe))
            if thumb_path and os.path.exists(thumb_path):
                pix = QtGui.QPixmap(thumb_path)
                pix = pix.scaledToWidth(230, QtCore.Qt.SmoothTransformation)
                if pix.height() > 110:
                    pix = pix.scaledToHeight(110, QtCore.Qt.SmoothTransformation)
                thumb_widget = QLabel()
                thumb_widget.setPixmap(pix)
                thumb_widget.setAlignment(QtCore.Qt.AlignCenter)
                thumb_widget.setStyleSheet(
                    'border: 1px solid #444; border-radius: 2px; background: #1e1e1e;')
                layout.addWidget(thumb_widget)

        # --- Notes preview ---
        notes_text = d.get('notes', '')
        if notes_text:
            notes_lbl = QLabel(notes_text)
            notes_lbl.setStyleSheet(
                'color: #aaa; font-size: 11px; background: transparent;')
            notes_lbl.setWordWrap(True)
            layout.addWidget(notes_lbl)

        # --- Tags ---
        tags = d.get('tags', '')
        if tags:
            tags_row = QHBoxLayout()
            tags_row.setSpacing(3)
            for tag in (t.strip() for t in tags.split(',') if t.strip()):
                tag_lbl = QLabel(tag)
                tag_lbl.setStyleSheet(
                    'background: #1a4a7a; color: #aaccee; font-size: 9px;'
                    ' border-radius: 5px; padding: 1px 6px;')
                tags_row.addWidget(tag_lbl)
            tags_row.addStretch()
            layout.addLayout(tags_row)

        # --- Footer ---
        footer = QHBoxLayout()
        footer.setSpacing(2)

        user_date = QLabel('{} · {}'.format(
            d.get('user', '?'), d.get('date', '')))
        user_date.setStyleSheet(
            'color: #666; font-size: 9px; background: transparent;')
        footer.addWidget(user_date, 1)

        # Camera button (only if xform was saved)
        if d.get('camera_xform', ''):
            cam_btn = _make_icon_btn('camera.png', 'Go to Camera')
            cam_btn.clicked.connect(self._go_to_camera)
            footer.addWidget(cam_btn)

        # View image button
        if encoded:
            img_btn = _make_icon_btn('image.png', 'View Screenshot')
            img_btn.clicked.connect(self._view_image)
            footer.addWidget(img_btn)

        edit_btn = _make_icon_btn('edit.png', 'Edit Card')
        edit_btn.clicked.connect(lambda: self.card_edited.emit(self.node))
        footer.addWidget(edit_btn)

        del_btn = _make_icon_btn('delete.png', 'Delete Card')
        del_btn.clicked.connect(self._delete)
        footer.addWidget(del_btn)

        layout.addLayout(footer)

    # ------------------------------------------------------------------
    def _go_to_camera(self):
        kanban_util.go_to_camera(self.node)

    def _view_image(self):
        encoded = self.node_data.get('image', '')
        if not encoded:
            return
        node_safe = self.node.replace(':', '_').replace('|', '_')
        tmp = kanban_util.decode_image(encoded, '{}_view.jpg'.format(node_safe))
        if tmp and os.path.exists(tmp):
            w = cmds.window(t='Screenshot: {}'.format(
                self.node_data.get('title', self.node)))
            cmds.paneLayout()
            cmds.image(image=tmp)
            cmds.showWindow(w)

    def _delete(self):
        confirm = cmds.confirmDialog(
            title='Delete Card',
            message='Delete "{}\"?'.format(self.node_data.get('title', self.node)),
            button=['Delete', 'Cancel'],
            defaultButton='Cancel', cancelButton='Cancel', dismissString='Cancel',
        )
        if confirm == 'Delete':
            kanban_util.delete_note(self.node)
            self.refresh_requested.emit()

    # ------------------------------------------------------------------
    # Drag support

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self._drag_start = event.pos()
        super(KanbanCardWidget, self).mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if not (event.buttons() & QtCore.Qt.LeftButton):
            return
        if self._drag_start is None:
            return
        dist = (event.pos() - self._drag_start).manhattanLength()
        if dist < QApplication.startDragDistance():
            return

        drag = QtGui.QDrag(self)
        mime = QtCore.QMimeData()
        payload = '{}|||{}'.format(self.node, self.column_name)
        mime.setData(MIME_TYPE, QtCore.QByteArray(payload.encode('utf-8')))
        drag.setMimeData(mime)

        # Visual drag representation
        pix = self.grab()
        pix = pix.scaled(240, 90, QtCore.Qt.KeepAspectRatio,
                         QtCore.Qt.SmoothTransformation)
        # Make it slightly transparent
        transparent = QtGui.QPixmap(pix.size())
        transparent.fill(QtCore.Qt.transparent)
        painter = QtGui.QPainter(transparent)
        painter.setOpacity(0.75)
        painter.drawPixmap(0, 0, pix)
        painter.end()
        drag.setPixmap(transparent)
        drag.setHotSpot(QtCore.QPoint(pix.width() // 2, 10))

        self.setCursor(QtCore.Qt.ClosedHandCursor)
        drag.exec_(QtCore.Qt.MoveAction)
        self.setCursor(QtCore.Qt.OpenHandCursor)

    def mouseReleaseEvent(self, event):
        self._drag_start = None
        super(KanbanCardWidget, self).mouseReleaseEvent(event)

    # ------------------------------------------------------------------
    # Context menu — right-click PDF export

    def contextMenuEvent(self, event):
        try:
            import importlib; from importlib import reload
        except ImportError:
            import imp; from imp import reload

        from Mutant_Tools.UI.Kanban.Utils import kanban_pdf
        reload(kanban_pdf)

        menu = QtWidgets.QMenu(self)
        menu.setStyleSheet(
            'QMenu { background:#2b2b2b; color:#e0e0e0; border:1px solid #555; }'
            'QMenu::item:selected { background:#3a6ea5; }'
            'QMenu::separator { height:1px; background:#444; margin:3px 0; }'
        )

        act_card = menu.addAction('Export This Card to PDF')
        act_col  = menu.addAction(
            'Export Column "{}" to PDF'.format(self.column_name))
        menu.addSeparator()
        act_all  = menu.addAction('Export All Cards to PDF')

        action = menu.exec_(event.globalPos())

        if action == act_card:
            kanban_pdf.export_card_to_pdf(self.node)
        elif action == act_col:
            kanban_pdf.export_column_to_pdf(self.column_name)
        elif action == act_all:
            kanban_pdf.export_all_to_pdf()


# ========================================================

class ColumnDropArea(QWidget):
    """Scrollable, droppable container that holds the cards for one column."""

    card_dropped = Signal(str, str, int)   # node, target_column, insert_index

    def __init__(self, column_name, parent=None):
        super(ColumnDropArea, self).__init__(parent)
        self.column_name = column_name
        self.setAcceptDrops(True)

        self._layout = QVBoxLayout(self)
        self._layout.setSpacing(4)
        self._layout.setContentsMargins(4, 4, 4, 4)
        self._layout.addStretch()   # trailing spacer keeps cards packed at top

        self._drop_line = QFrame(self)
        self._drop_line.setFrameShape(QFrame.HLine)
        self._drop_line.setFixedHeight(2)
        self._drop_line.setStyleSheet('background: #4a90e2; border: none;')
        self._drop_line.hide()

    # ------------------------------------------------------------------
    def add_card(self, widget):
        """Append a card before the trailing stretch."""
        self._layout.insertWidget(self._layout.count() - 1, widget)

    def insert_card(self, widget, idx):
        self._layout.insertWidget(idx, widget)

    def clear_cards(self):
        while self._layout.count() > 1:
            item = self._layout.takeAt(0)
            if item and item.widget():
                item.widget().deleteLater()

    def card_count(self):
        return self._layout.count() - 1   # exclude stretch

    # ------------------------------------------------------------------
    # Drop target visuals

    def _insert_index_for_y(self, y):
        """Return the card list index that corresponds to drop position y."""
        for i in range(self._layout.count() - 1):
            item = self._layout.itemAt(i)
            if item and item.widget():
                w = item.widget()
                mid = w.y() + w.height() // 2
                if y < mid:
                    return i
        return self._layout.count() - 1   # append at end

    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat(MIME_TYPE):
            event.acceptProposedAction()
            self.setStyleSheet('background: rgba(74, 111, 165, 0.10);')
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasFormat(MIME_TYPE):
            event.acceptProposedAction()
            idx = self._insert_index_for_y(event.pos().y())
            self._show_drop_line(idx)
        else:
            event.ignore()

    def dragLeaveEvent(self, event):
        self.setStyleSheet('')
        self._drop_line.hide()

    def dropEvent(self, event):
        self.setStyleSheet('')
        self._drop_line.hide()
        if not event.mimeData().hasFormat(MIME_TYPE):
            event.ignore()
            return
        raw = bytes(event.mimeData().data(MIME_TYPE)).decode('utf-8')
        parts = raw.split('|||', 1)
        if len(parts) != 2:
            event.ignore()
            return
        node_name = parts[0]
        idx = self._insert_index_for_y(event.pos().y())
        event.acceptProposedAction()
        self.card_dropped.emit(node_name, self.column_name, idx)

    def _show_drop_line(self, idx):
        """Move the blue drop-indicator line to the correct position."""
        items_with_widgets = [
            self._layout.itemAt(i).widget()
            for i in range(self._layout.count() - 1)
            if self._layout.itemAt(i) and self._layout.itemAt(i).widget()
        ]
        if not items_with_widgets:
            y = 4
        elif idx >= len(items_with_widgets):
            last = items_with_widgets[-1]
            y = last.y() + last.height() + 2
        else:
            y = items_with_widgets[idx].y() - 3

        self._drop_line.setGeometry(4, max(y, 4), self.width() - 8, 2)
        self._drop_line.raise_()
        self._drop_line.show()


# ========================================================
# KANBAN COLUMN WIDGET
# ========================================================

class KanbanColumnWidget(QFrame):
    """Full column panel: coloured header + scrollable card area."""

    add_card_requested = Signal(str)    # column name
    column_renamed = Signal(str, str)   # old name, new name
    column_deleted = Signal(str)        # column name
    refresh_requested = Signal()

    def __init__(self, column_name, color_index=0, parent=None):
        super(KanbanColumnWidget, self).__init__(parent)
        self.column_name = column_name
        self._color = COL_HEADER_COLORS[color_index % len(COL_HEADER_COLORS)]

        self.setObjectName('KanbanColumn')
        self.setMinimumWidth(270)
        self.setMaximumWidth(330)
        self.setFrameShape(QFrame.StyledPanel)
        self.setStyleSheet('''
            QFrame#KanbanColumn {
                background-color: #282828;
                border: 1px solid #3a3a3a;
                border-radius: 6px;
            }
        ''')

        self._build_ui()

    # ------------------------------------------------------------------
    def _build_ui(self):
        main = QVBoxLayout(self)
        main.setSpacing(0)
        main.setContentsMargins(0, 0, 0, 6)

        # Header
        header = QWidget()
        header.setFixedHeight(38)
        header.setStyleSheet(
            'background: {c}; border-top-left-radius: 6px;'
            ' border-top-right-radius: 6px;'.format(c=self._color))
        hlay = QHBoxLayout(header)
        hlay.setContentsMargins(10, 4, 6, 4)

        self.name_lbl = QLabel(self.column_name)
        self.name_lbl.setStyleSheet(
            'color: #fff; font-weight: bold; font-size: 12px; background: transparent;')

        self.count_badge = QLabel('0')
        self.count_badge.setStyleSheet(
            'background: rgba(0,0,0,0.35); color: #fff; font-size: 10px;'
            ' font-weight: bold; border-radius: 8px; padding: 1px 7px;'
            ' min-width: 16px; background: transparent;'
            ' border: 1px solid rgba(255,255,255,0.3);')

        add_btn = QPushButton('+')
        add_btn.setFixedSize(26, 26)
        add_btn.setFlat(True)
        add_btn.setToolTip('Add card to this column')
        add_btn.setCursor(QtCore.Qt.PointingHandCursor)
        add_btn.setStyleSheet(
            'color: #fff; font-size: 18px; font-weight: bold;'
            ' background: rgba(255,255,255,0.15); border-radius: 4px;')
        add_btn.clicked.connect(lambda: self.add_card_requested.emit(self.column_name))

        opts_btn = QPushButton('⋯')
        opts_btn.setFixedSize(26, 26)
        opts_btn.setFlat(True)
        opts_btn.setToolTip('Column options')
        opts_btn.setCursor(QtCore.Qt.PointingHandCursor)
        opts_btn.setStyleSheet(
            'color: #fff; font-size: 14px;'
            ' background: rgba(255,255,255,0.15); border-radius: 4px;')
        opts_btn.clicked.connect(self._show_options)

        hlay.addWidget(self.name_lbl, 1)
        hlay.addWidget(self.count_badge)
        hlay.addWidget(add_btn)
        hlay.addWidget(opts_btn)
        main.addWidget(header)

        # Scroll area
        self._scroll = QScrollArea()
        self._scroll.setWidgetResizable(True)
        self._scroll.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self._scroll.setFrameShape(QFrame.NoFrame)

        self._drop_area = ColumnDropArea(self.column_name)
        self._scroll.setWidget(self._drop_area)
        self._drop_area.card_dropped.connect(self._on_dropped)

        main.addWidget(self._scroll)

    # ------------------------------------------------------------------
    def _show_options(self):
        menu = QMenu(self)
        rename_act = menu.addAction('Rename Column')
        menu.addSeparator()
        delete_act = menu.addAction('Delete Column')
        action = menu.exec_(QtGui.QCursor.pos())
        if action == rename_act:
            self._rename()
        elif action == delete_act:
            self.column_deleted.emit(self.column_name)

    def _rename(self):
        new_name, ok = QInputDialog.getText(
            self, 'Rename Column', 'New name for "{}":'.format(self.column_name))
        if ok and new_name.strip():
            old = self.column_name
            self.column_name = new_name.strip()
            self.name_lbl.setText(new_name.strip())
            self._drop_area.column_name = new_name.strip()
            self.column_renamed.emit(old, new_name.strip())

    def _on_dropped(self, node, target_col, idx):
        """Handle a card being dropped onto this column."""
        kanban_util.move_note_to_column(node, target_col)
        # Reorder: rebuild card_order for all notes now in this column
        notes = kanban_util.get_notes_in_column(target_col)
        if node in notes:
            notes.remove(node)
        notes.insert(idx, node)
        for i, n in enumerate(notes):
            kanban_util.reorder_note(n, i)
        self.refresh_requested.emit()

    # ------------------------------------------------------------------
    def load_cards(self, on_refresh, on_edit):
        """(Re)populate the column with card widgets from scene data."""
        self._drop_area.clear_cards()
        notes = kanban_util.get_notes_in_column(self.column_name)
        for note in notes:
            if not cmds.objExists(note):
                continue
            data = kanban_util.get_note_data(note)
            card = KanbanCardWidget(data, self.column_name,
                                    parent=self._drop_area)
            card.refresh_requested.connect(on_refresh)
            card.card_edited.connect(on_edit)
            self._drop_area.add_card(card)
        self.count_badge.setText(str(len(notes)))

    def get_drop_area(self):
        return self._drop_area


# ========================================================
# KANBAN BOARD WIDGET (the scrollable multi-column board)
# ========================================================

class KanbanBoardWidget(QWidget):
    """Toolbar + horizontal column scroll area."""

    def __init__(self, parent=None):
        super(KanbanBoardWidget, self).__init__(parent)
        self._column_widgets = {}
        self._build_ui()

    # ------------------------------------------------------------------
    def _build_ui(self):
        main = QVBoxLayout(self)
        main.setSpacing(4)
        main.setContentsMargins(6, 6, 6, 6)

        # Toolbar
        toolbar = QWidget()
        toolbar.setFixedHeight(38)
        tlay = QHBoxLayout(toolbar)
        tlay.setContentsMargins(4, 2, 4, 2)
        tlay.setSpacing(6)

        # Mutant logo
        logo_path = os.path.join(ICONS_PATH, 'LogoWhite03.png')
        if os.path.exists(logo_path):
            logo_pix = QtGui.QPixmap(logo_path).scaled(
                22, 22, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
            logo_lbl = QLabel()
            logo_lbl.setPixmap(logo_pix)
            logo_lbl.setFixedSize(22, 22)
            tlay.addWidget(logo_lbl)

        title_lbl = QLabel('MutantKanban')
        title_lbl.setStyleSheet(
            'font-weight: bold; font-size: 13px; color: #c0c0c0;')
        tlay.addWidget(title_lbl)
        tlay.addStretch()

        def _tbtn(text, icon_name=None, tip=''):
            btn = QPushButton(text)
            btn.setFixedHeight(28)
            btn.setToolTip(tip)
            btn.setCursor(QtCore.Qt.PointingHandCursor)
            if icon_name:
                ico = _icon(icon_name)
                if not ico.isNull():
                    btn.setIcon(ico)
                    btn.setIconSize(QtCore.QSize(14, 14))
            return btn

        add_btn = _tbtn('+ Add Card', 'add.png', 'Create a new card')
        add_btn.clicked.connect(self._add_card_global)
        tlay.addWidget(add_btn)

        cols_btn = _tbtn('Columns', tip='Manage board columns')
        cols_btn.clicked.connect(self._manage_columns)
        tlay.addWidget(cols_btn)

        refresh_btn = _tbtn('⟳', tip='Reload from scene')
        refresh_btn.setFixedWidth(30)
        refresh_btn.clicked.connect(self.refresh_board)
        tlay.addWidget(refresh_btn)

        main.addWidget(toolbar)

        # Separator
        sep = QFrame()
        sep.setFrameShape(QFrame.HLine)
        sep.setFrameShadow(QFrame.Sunken)
        main.addWidget(sep)

        # Horizontal column scroll
        self._col_scroll = QScrollArea()
        self._col_scroll.setWidgetResizable(True)
        self._col_scroll.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self._col_scroll.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAsNeeded)
        self._col_scroll.setFrameShape(QFrame.NoFrame)

        self._cols_container = QWidget()
        self._cols_layout = QHBoxLayout(self._cols_container)
        self._cols_layout.setSpacing(10)
        self._cols_layout.setContentsMargins(4, 4, 4, 4)
        self._cols_layout.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)

        self._col_scroll.setWidget(self._cols_container)
        main.addWidget(self._col_scroll)

    # ------------------------------------------------------------------
    def refresh_board(self):
        """Clear all column widgets and rebuild them from scene data."""
        # Remove all column widgets
        while self._cols_layout.count() > 0:
            item = self._cols_layout.takeAt(0)
            if item and item.widget():
                item.widget().deleteLater()
        self._column_widgets = {}

        columns = kanban_util.get_columns()
        for col in columns:
            kanban_util.get_or_create_column_group(col)

        for i, col_name in enumerate(columns):
            col_w = KanbanColumnWidget(col_name, color_index=i)
            col_w.add_card_requested.connect(self._add_card_to_column)
            col_w.column_renamed.connect(self._on_column_renamed)
            col_w.column_deleted.connect(self._on_column_deleted)
            col_w.refresh_requested.connect(self.refresh_board)
            col_w.load_cards(
                on_refresh=self.refresh_board,
                on_edit=self._edit_card,
            )
            self._cols_layout.addWidget(col_w)
            self._column_widgets[col_name] = col_w

        print('MutantKanban: Refreshed — {} columns.'.format(len(columns)))

    # ------------------------------------------------------------------
    def _add_card_global(self):
        cols = kanban_util.get_columns()
        first = cols[0] if cols else 'Backlog'
        self._add_card_to_column(first)

    def _add_card_to_column(self, column_name):
        cols = kanban_util.get_columns()
        dlg = CardDialog(parent=self, columns=cols, current_column=column_name)

        def _on_accepted():
            r = dlg.get_result()
            kanban_util.create_note_node(
                title=r['title'],
                notes=r['notes'],
                encoded_image=r['encoded_image'],
                column_name=r['column'],
                priority=r['priority'],
                tags=r['tags'],
            )
            self.refresh_board()

        dlg.accepted.connect(_on_accepted)
        dlg.show()

    def _edit_card(self, node):
        if not cmds.objExists(node):
            cmds.warning('MutantKanban: Node {} no longer exists.'.format(node))
            return
        data = kanban_util.get_note_data(node)
        cols = kanban_util.get_columns()

        # Determine current column from the node's parent
        current_col = cols[0] if cols else 'Backlog'
        parents = cmds.listRelatives(node, parent=True)
        if parents:
            for col in cols:
                if kanban_util.node_name_for_column(col) == parents[0]:
                    current_col = col
                    break

        dlg = CardDialog(parent=self, columns=cols,
                         current_column=current_col, node_data=data)

        def _on_accepted():
            r = dlg.get_result()
            kanban_util.update_note_data(
                node,
                title=r['title'],
                notes=r['notes'],
                priority=r['priority'],
                tags=r['tags'],
                encoded_image=r['encoded_image'] if r['encoded_image'] else None,
            )
            if r['column'] != current_col:
                kanban_util.move_note_to_column(node, r['column'])
            self.refresh_board()

        dlg.accepted.connect(_on_accepted)
        dlg.show()

    # ------------------------------------------------------------------
    def _manage_columns(self):
        cols = kanban_util.get_columns()
        dlg = ManageColumnsDialog(parent=self, columns=cols)
        if dlg.exec_() == QDialog.Accepted:
            new_cols = dlg.get_columns()
            old_cols = kanban_util.get_columns()
            fallback = new_cols[0] if new_cols else 'Backlog'
            # Move orphan cards out of deleted columns
            for old_col in old_cols:
                if old_col not in new_cols:
                    for note in kanban_util.get_notes_in_column(old_col):
                        kanban_util.move_note_to_column(note, fallback)
            kanban_util.set_columns(new_cols)
            self.refresh_board()

    def _on_column_renamed(self, old_name, new_name):
        cols = kanban_util.get_columns()
        if old_name in cols:
            cols[cols.index(old_name)] = new_name
            kanban_util.set_columns(cols)
            old_node = kanban_util.node_name_for_column(old_name)
            if cmds.objExists(old_node):
                try:
                    new_node = cmds.rename(
                        old_node, kanban_util.node_name_for_column(new_name))
                    if cmds.attributeQuery('column_label', node=new_node, exists=True):
                        try:
                            cmds.setAttr('{}.column_label'.format(new_node),
                                         new_name, type='string')
                        except Exception:
                            pass
                except Exception as e:
                    cmds.warning(
                        'MutantKanban: Could not rename group: {}'.format(e))
        self.refresh_board()

    def _on_column_deleted(self, col_name):
        cols = kanban_util.get_columns()
        if col_name in cols:
            fallback = next((c for c in cols if c != col_name), None)
            if fallback:
                for note in kanban_util.get_notes_in_column(col_name):
                    kanban_util.move_note_to_column(note, fallback)
            cols.remove(col_name)
            kanban_util.set_columns(cols)
        self.refresh_board()


# ========================================================
# MAIN KANBAN WINDOW  (inherits Qt_Mutant)
# ========================================================

class KanbanUI(QtMutantWindow.Qt_Mutant):
    """
    MutantKanban main window.
    Inherits the Mutant frameless chrome and stylesheet from Qt_Mutant.
    """

    def __init__(self):
        super(KanbanUI, self).__init__()

        self.setWindowTitle(Title)
        self.set_title(Title)

        # Build the board and inject into the Mutant content area
        self._board = KanbanBoardWidget(parent=self)
        self.master_ui.mutant_Layout.addWidget(self._board)

        # Honour saved window-mode preference
        if (cmds.optionVar(ex='mutant_standard_window') and
                cmds.optionVar(q='mutant_standard_window')):
            self.apply_window_mode(standard=True)
        else:
            self.make_frameless()

        self.create_menu()
        self._board.refresh_board()

        # Resize to fit actual column count once the layout has settled
        QtCore.QTimer.singleShot(50, self._fit_to_columns)

    def _fit_to_columns(self):
        """
        Set an initial window size that fits the current columns snugly.
        The window remains freely resizable after opening.
        Each column is 300 px wide on average, plus 10 px spacing and chrome.
        Height defaults to 700 px (enough for a comfortable board view).
        """
        col_count = max(1, len(kanban_util.get_columns()))
        col_w = 300          # average column width
        spacing = 10         # between columns
        h_padding = 60       # left + right chrome / scrollbar margin
        toolbar_h = 50       # board toolbar
        chrome_h = 80        # Mutant title bar + menu bar estimate
        board_height = 480

        target_w = col_count * col_w + (col_count - 1) * spacing + h_padding
        target_h = board_height + toolbar_h + chrome_h

        # Use the screen the mouse cursor is currently on
        cursor_pos = QtGui.QCursor.pos()
        screen = QtWidgets.QApplication.screenAt(cursor_pos)
        if screen is None:
            screen = QtWidgets.QApplication.primaryScreen()

        if screen:
            avail = screen.availableGeometry()
            target_w = min(target_w, int(avail.width() * 0.92))
            target_h = min(target_h, int(avail.height() * 0.90))
            self.resize(target_w, target_h)
            # Let the resize propagate so frameGeometry is accurate
            QtWidgets.QApplication.processEvents()
            fg = self.frameGeometry()
            x = avail.x() + (avail.width()  - fg.width())  // 2
            y = avail.y() + (avail.height() - fg.height()) // 2
            self.move(x, y)
        else:
            self.resize(target_w, target_h)
            self.move_to_center_screen()
