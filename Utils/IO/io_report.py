"""Small end of build report for the rebuild IO (skins / controllers save and load).
Only shows up when something needs a look, every line can be clicked to select the node it names."""
from __future__ import absolute_import

from maya import cmds

from Mutant_Tools.Utils.IO import CtrlUtils

ERROR_COLOR = '#e05c4f'
WARNING_COLOR = '#e0b400'
INFO_COLOR = '#8a8a8a'


class IOReport(object):
    """Collects sections while the build runs: add(title, entries, level) with level error / warning / info."""

    def __init__(self):
        self.sections = []

    def add(self, title, entries, level='error'):
        entries = [str(e) for e in entries or []]
        if entries:
            self.sections.append((title, entries, level))

    def needs_look(self):
        return any(level != 'info' for _, _, level in self.sections)

    def show(self, title='Mutant Build IO Report'):
        for section, entries, level in self.sections:
            print('Mutant IO {} - {} ({})'.format(level.upper(), section, len(entries)))
            for entry in entries:
                print('    {}'.format(entry))
        if not self.needs_look():
            return None
        if cmds.about(batch=True):
            return None
        dialog = IOReportDialog(self.sections, title=title, parent=CtrlUtils._maya_main_window())
        dialog.show()
        return dialog


class IOReportDialog(CtrlUtils.QtWidgets.QDialog):

    def __init__(self, sections, title='Mutant Build IO Report', parent=None):
        super(IOReportDialog, self).__init__(parent)
        QtWidgets = CtrlUtils.QtWidgets
        self.setWindowTitle(title)
        self.resize(620, 460)
        layout = QtWidgets.QVBoxLayout(self)

        counts = {}
        for _, entries, level in sections:
            counts[level] = counts.get(level, 0) + len(entries)
        layout.addWidget(QtWidgets.QLabel('Errors: {}    Warnings: {}    Info: {}'.format(
            counts.get('error', 0), counts.get('warning', 0), counts.get('info', 0))))

        colors = {'error': ERROR_COLOR, 'warning': WARNING_COLOR, 'info': INFO_COLOR}
        for title, entries, level in sorted(sections, key=lambda s: ['error', 'warning', 'info'].index(s[2])):
            section = CtrlUtils._CollapsibleSection('{} ({})'.format(title, len(entries)), colors[level])
            for entry in entries:
                section.add_entry(entry, entry.split(':')[0].split(' ')[0])
            section.set_expanded(level != 'info')
            section.content.itemClicked.connect(self._select)
            layout.addWidget(section)

        layout.addStretch()
        close_btn = QtWidgets.QPushButton('Close')
        close_btn.clicked.connect(self.close)
        layout.addWidget(close_btn)

    def _select(self, item):
        node = item.data(CtrlUtils.QtCore.Qt.UserRole)
        if node and cmds.objExists(node):
            cmds.select(node, replace=True)
