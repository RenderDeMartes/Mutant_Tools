"""Small end of build report for the rebuild IO (skins / controllers save and load).
Only shows up when something needs a look, every line can be clicked to select the node it names."""
from __future__ import absolute_import

from maya import cmds

try:
    from PySide6 import QtCore, QtWidgets
except ImportError:  # Maya 2024 and older
    from PySide2 import QtCore, QtWidgets

try:
    from Mutant_Tools.UI import QtMutantWindow
except Exception:  # batch / no Maya main window: the report is only printed there
    QtMutantWindow = None

ERROR, WARNING, INFO = 'error', 'warning', 'info'
TONES = {ERROR: '#e5847f', WARNING: '#d9b36c', INFO: '#9da1a4'}
ICONS = {ERROR: u'✖', WARNING: u'⚠', INFO: u'ℹ'}

# same look as the Build Log (UI/AutoRigger/build_log.py)
STYLE = '''
#IOReport QLabel { color: #bbbbbb; }
#IOReport QFrame#Header { background: #323436; border: none; border-radius: 8px; }
#IOReport QLabel#Title { font-size: 16px; font-weight: bold; color: #e8e8e8; }
#IOReport QLabel#Title[tone="error"] { color: #e5847f; }
#IOReport QLabel#Title[tone="warning"] { color: #d9b36c; }
#IOReport QLabel#Meta { color: #9da1a4; }
#IOReport QLabel#Count { color: #9da1a4; background: #2b2d2f; border-radius: 9px; padding: 2px 9px; }
#IOReport QFrame#Row { background: #323436; border: none; border-radius: 6px; }
#IOReport QFrame#Row:hover { background: #393c3e; }
#IOReport QLabel#Chevron { color: #8a8d90; min-width: 10px; }
#IOReport QLabel#Name { color: #e0e0e0; }
#IOReport QLabel#Tag { color: #8a8d90; background: #2b2d2f; border-radius: 4px; padding: 1px 6px; font-size: 10px; }
#IOReport QListWidget#List {
    background: #2b2d2f; color: #c8c8c8; border: none; border-radius: 6px; padding: 4px; outline: 0; }
#IOReport QListWidget#List::item { padding: 3px 4px; border-radius: 4px; }
#IOReport QListWidget#List::item:hover { background: #393c3e; }
#IOReport QListWidget#List::item:selected { background: #4b6eaf; color: #ffffff; }
#IOReport QScrollArea { border: none; background: transparent; }
#IOReport QPushButton#Ghost {
    background: transparent; color: #c8c8c8; border: 1px solid #5c5f61; border-radius: 5px; padding: 4px 10px; }
#IOReport QPushButton#Ghost:hover { border-color: #7d8184; color: #ffffff; }
'''

_window = None


class IOReport(object):
    """Collects sections while the build runs: add(title, entries, level) with level error / warning / info."""

    def __init__(self):
        self.sections = []

    def add(self, title, entries, level=ERROR):
        entries = [str(e) for e in entries or []]
        if entries:
            self.sections.append((title, entries, level))

    def needs_look(self):
        return any(level != INFO for _, _, level in self.sections)

    def show(self, title='Mutant Build IO Report'):
        global _window
        for section, entries, level in self.sections:
            print('Mutant IO {} - {} ({})'.format(level.upper(), section, len(entries)))
            for entry in entries:
                print('    {}'.format(entry))
        if not self.needs_look():
            return None
        if cmds.about(batch=True) or QtMutantWindow is None:
            return None
        try:
            _window.close()
            _window.deleteLater()
        except Exception:
            pass
        _window = IOReportUI(self.sections, title=title)
        _window.show()
        return _window


def _named(widget, name, **properties):
    widget.setObjectName(name)
    for key, value in properties.items():
        widget.setProperty(key, value)
    return widget


def _node(entry):
    """Node an entry names: 'Jaw_Ctrl: not in the scene' -> Jaw_Ctrl."""
    return entry.split(':')[0].split(' ')[0]


class _Row(QtWidgets.QFrame):
    clicked = QtCore.Signal()

    def mouseReleaseEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.clicked.emit()
        super(_Row, self).mouseReleaseEvent(event)


class SectionWidget(QtWidgets.QWidget):
    """One report section: a row that toggles its entries, click an entry to select its node."""

    def __init__(self, title, entries, level, parent=None):
        super(SectionWidget, self).__init__(parent)
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(4)

        self.row = _named(_Row(), 'Row')
        self.row.setCursor(QtCore.Qt.PointingHandCursor)
        self.row.clicked.connect(self.toggle)
        row = QtWidgets.QHBoxLayout(self.row)
        row.setContentsMargins(10, 6, 10, 6)
        row.setSpacing(8)
        self.chevron = _named(QtWidgets.QLabel(u'▸'), 'Chevron')
        row.addWidget(self.chevron)
        icon = QtWidgets.QLabel(ICONS[level])
        icon.setStyleSheet('color: {}; font-weight: bold;'.format(TONES[level]))
        icon.setFixedWidth(14)
        row.addWidget(icon)
        name = _named(QtWidgets.QLabel(title), 'Name')
        name.setWordWrap(True)
        row.addWidget(name, 1)
        row.addWidget(_named(QtWidgets.QLabel(str(len(entries))), 'Tag'))
        layout.addWidget(self.row)

        self.list = _named(QtWidgets.QListWidget(), 'List')
        self.list.setCursor(QtCore.Qt.PointingHandCursor)
        for entry in entries:
            item = QtWidgets.QListWidgetItem(entry)
            item.setData(QtCore.Qt.UserRole, _node(entry))
            item.setToolTip('Click to select {}'.format(_node(entry)))
            self.list.addItem(item)
        self.list.itemClicked.connect(self._select)
        row_height = self.list.sizeHintForRow(0) if entries else 20
        self.list.setFixedHeight(int(row_height * min(len(entries), 10) + 12))
        body = QtWidgets.QWidget()
        body_layout = QtWidgets.QVBoxLayout(body)
        body_layout.setContentsMargins(20, 0, 0, 6)
        body_layout.addWidget(self.list)
        self.body = body
        self.body.setVisible(False)
        layout.addWidget(self.body)

    def toggle(self):
        self.set_expanded(not self.body.isVisible())

    def set_expanded(self, expanded):
        self.body.setVisible(expanded)
        self.chevron.setText(u'▾' if expanded else u'▸')

    def _select(self, item):
        node = item.data(QtCore.Qt.UserRole)
        if node and cmds.objExists(node):
            cmds.select(node, replace=True)


class IOReportView(QtWidgets.QWidget):
    """Header (what needs a look), one row per section (errors open), Copy Report."""

    def __init__(self, sections, parent=None):
        super(IOReportView, self).__init__(parent)
        self.setObjectName('IOReport')
        self.setStyleSheet(STYLE)
        self.sections = sorted(sections, key=lambda s: [ERROR, WARNING, INFO].index(s[2]))

        counts = {}
        for _, entries, level in self.sections:
            counts[level] = counts.get(level, 0) + len(entries)

        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(6, 6, 6, 6)
        layout.setSpacing(8)

        if counts.get(ERROR):
            tone, title = ERROR, u'✖  Some skins or controllers did not load back'
        else:
            tone, title = WARNING, u'⚠  Skins and controllers loaded, a few need a look'
        header = _named(QtWidgets.QFrame(), 'Header')
        col = QtWidgets.QVBoxLayout(header)
        col.setContentsMargins(14, 12, 14, 12)
        col.setSpacing(6)
        col.addWidget(_named(QtWidgets.QLabel(title), 'Title', tone=tone))
        meta = _named(QtWidgets.QLabel('What the rebuild saved before and loaded back after. '
                                       'Click a line to select the node it names.'), 'Meta')
        meta.setWordWrap(True)
        col.addWidget(meta)
        chips = QtWidgets.QHBoxLayout()
        chips.setSpacing(6)
        for level, label in [(ERROR, 'error'), (WARNING, 'warning'), (INFO, 'info')]:
            if counts.get(level):
                chips.addWidget(_named(QtWidgets.QLabel('{} {}{}'.format(
                    counts[level], label, '' if counts[level] == 1 or level == INFO else 's')), 'Count'))
        chips.addStretch()
        col.addLayout(chips)
        layout.addWidget(header)

        scroll = QtWidgets.QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QtWidgets.QFrame.NoFrame)
        holder = QtWidgets.QWidget()
        rows = QtWidgets.QVBoxLayout(holder)
        rows.setContentsMargins(0, 0, 4, 0)
        rows.setSpacing(4)
        for title_text, entries, level in self.sections:
            widget = SectionWidget(title_text, entries, level)
            # errors open, the rest stays closed
            widget.set_expanded(level == ERROR)
            rows.addWidget(widget)
        rows.addStretch()
        scroll.setWidget(holder)
        layout.addWidget(scroll, 1)

        buttons = QtWidgets.QHBoxLayout()
        copy_btn = _named(QtWidgets.QPushButton('Copy Report'), 'Ghost')
        copy_btn.setCursor(QtCore.Qt.PointingHandCursor)
        copy_btn.clicked.connect(lambda *_: QtWidgets.QApplication.clipboard().setText(self.as_text()))
        buttons.addWidget(copy_btn)
        buttons.addStretch()
        layout.addLayout(buttons)

    def as_text(self):
        lines = []
        for title, entries, level in self.sections:
            lines.append('{} - {} ({})'.format(level.upper(), title, len(entries)))
            lines.extend('    {}'.format(entry) for entry in entries)
        return '\n'.join(lines)


_Base = QtMutantWindow.Qt_Mutant if QtMutantWindow else QtWidgets.QWidget


class IOReportUI(_Base):
    """The IO report in a Mutant Tools window."""

    def __init__(self, sections, title='Mutant Build IO Report'):
        super(IOReportUI, self).__init__()
        self.setWindowTitle(title)
        self.view = IOReportView(sections)
        # Qt_Mutant.minimize hides self.ui
        self.ui = self.view
        if QtMutantWindow:
            self.set_title('IO Report')
            self.master_ui.mutant_Layout.addWidget(self.view)
        else:
            QtWidgets.QVBoxLayout(self).addWidget(self.view)
        self.resize(640, 520)
