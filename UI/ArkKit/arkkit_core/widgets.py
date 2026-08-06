"""Custom Qt widgets used by the ArkKit UI."""

from PySide6 import QtWidgets, QtCore, QtGui

from . import config


# -------- Collapsible Groups --------

class CollapsibleGroup(QtWidgets.QWidget):
    """A titled section that collapses/expands its content."""

    def __init__(self, title, expanded=True):
        super().__init__()

        self._title = title

        self.toggle_btn = QtWidgets.QToolButton()
        arrow = "▾" if expanded else "▸"
        self.toggle_btn.setText("{}  {}".format(arrow, title))
        self.toggle_btn.setCheckable(True)
        self.toggle_btn.setChecked(expanded)
        self.toggle_btn.setStyleSheet("color: white; font-weight: bold;")

        self.content = QtWidgets.QWidget()
        self.content_layout = QtWidgets.QVBoxLayout(self.content)
        self.content_layout.setContentsMargins(10, 2, 10, 2)
        self.content_layout.setSpacing(3)
        self.content.setVisible(expanded)

        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.toggle_btn)
        layout.addWidget(self.content)

        self.toggle_btn.toggled.connect(self.toggle)

    def toggle(self, state):
        self.content.setVisible(state)
        arrow = "▾" if state else "▸"
        self.toggle_btn.setText("{}  {}".format(arrow, self._title))


# -------- Expression Row --------

class ExpressionRow(QtWidgets.QWidget):
    """One ARKit expression: name + blend slider + record button.

    Paints a rounded dark background with a left accent strip that is bright
    when the expression has recorded data and dim when it is still empty.
    """

    clicked = QtCore.Signal(object)          # (self) — for multi-select
    valueChanged = QtCore.Signal(str, float)  # (name, 0..1)
    recordToggled = QtCore.Signal(str)        # (name) — user pressed record
    dragStarted = QtCore.Signal()
    dragEnded = QtCore.Signal()

    def __init__(self, name):
        super().__init__()

        self.name = name
        self.selected = False
        self.has_data = False
        self.recording = False

        self.accent = QtGui.QColor(config.color_for_expression(name))

        self.setMinimumHeight(30)

        layout = QtWidgets.QHBoxLayout(self)
        layout.setContentsMargins(14, 3, 6, 3)
        layout.setSpacing(6)

        self.label = QtWidgets.QLabel(name)
        self.label.setMinimumWidth(150)
        self.label.setStyleSheet("color: white;")

        self.slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.slider.setRange(0, config.SLIDER_RESOLUTION)

        self.record_btn = QtWidgets.QPushButton("REC")
        self.record_btn.setFixedWidth(46)
        self.record_btn.setToolTip(
            "Record this expression.\n"
            "Turns red while active; move the rig controls, then press again to\n"
            "store the pose as a delta from the captured defaults."
        )

        layout.addWidget(self.label)
        layout.addWidget(self.slider, 1)
        layout.addWidget(self.record_btn)

        self.slider.valueChanged.connect(self._emit_value)
        self.slider.sliderPressed.connect(self.dragStarted.emit)
        self.slider.sliderReleased.connect(self.dragEnded.emit)
        self.record_btn.clicked.connect(lambda: self.recordToggled.emit(self.name))

        self._refresh_record_style()

    # -------- events --------

    def mousePressEvent(self, event):
        # Clicks that reach the row background (or the label, which ignores
        # them) count as a selection click.
        self.clicked.emit(self)
        super().mousePressEvent(event)

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        rect = self.rect()

        # base background
        painter.setBrush(QtGui.QColor(40, 40, 40))
        painter.setPen(QtCore.Qt.NoPen)
        painter.drawRoundedRect(rect, 4, 4)

        # left accent strip — bright if recorded, dim if empty
        color = QtGui.QColor(self.accent)
        color.setAlpha(230 if self.has_data else 45)
        strip = QtCore.QRect(rect.x(), rect.y(), 8, rect.height())
        painter.setBrush(color)
        painter.drawRoundedRect(strip, 3, 3)

        # selection border
        if self.selected:
            pen = QtGui.QPen(QtGui.QColor("white"))
            pen.setWidth(2)
            painter.setPen(pen)
            painter.setBrush(QtCore.Qt.NoBrush)
            painter.drawRoundedRect(rect.adjusted(1, 1, -1, -1), 4, 4)

    # -------- state --------

    def _emit_value(self):
        self.valueChanged.emit(self.name, self.get_value())

    def set_value(self, v):
        self.slider.blockSignals(True)
        self.slider.setValue(int(round(v * config.SLIDER_RESOLUTION)))
        self.slider.blockSignals(False)

    def get_value(self):
        return self.slider.value() / float(config.SLIDER_RESOLUTION)

    def reset(self):
        self.set_value(0)

    def set_selected(self, state):
        self.selected = state
        self.update()

    def set_has_data(self, state):
        self.has_data = bool(state)
        self.update()

    def set_recording(self, state):
        self.recording = bool(state)
        self._refresh_record_style()
        self.update()

    def set_locked(self, locked):
        """Disable the slider + record button (used while another row records)."""
        self.slider.setEnabled(not locked)
        self.record_btn.setEnabled(not locked)

    def _refresh_record_style(self):
        if self.recording:
            self.record_btn.setText("STOP")
            self.record_btn.setStyleSheet(
                "background-color: #C0392B; color: white; font-weight: bold;"
            )
        else:
            self.record_btn.setText("REC")
            self.record_btn.setStyleSheet("")
