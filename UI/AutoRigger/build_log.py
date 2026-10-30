"""Build log split per block and per builder step, with a likely cause for the error.

While building, the AutoRigger prints marker lines into the Mutant log (Mutant_log.txt):

    [Mutant Plan] ["BaseA_Block", ...]                       blocks it is going to build
    [Mutant Section] {"kind": "block", "name": ..., "time": ...}  a block / builder step starts
    [Mutant Result] {"ok": false, "failed": ..., "error": {...}}  how the build ended

show() reads the log and opens BuildLogUI (a Mutant Tools window): one row per section, green when it
built, red and open on the one that stopped the build, yellow when it printed errors but the build went
on, grey when it never ran. Logs written before the markers existed are split on their "Building: X" lines.
"""
from __future__ import absolute_import

import json
import os
import re
import time

from maya import cmds

try:
    from PySide6 import QtCore, QtGui, QtWidgets
except ImportError:  # Maya 2024 and older
    from PySide2 import QtCore, QtGui, QtWidgets

PLAN_TAG = '[Mutant Plan]'
SECTION_TAG = '[Mutant Section]'
RESULT_TAG = '[Mutant Result]'

OK, FAILED, ERRORS, NOT_BUILT = 'ok', 'failed', 'errors', 'not_built'
ICONS = {OK: u'✔', FAILED: u'✖', ERRORS: u'⚠', NOT_BUILT: u'–'}

ERROR_LINE = re.compile(r'^\s*(#\s*)?(Error:|Traceback \(most recent call last\))|^\s*(#\s*)?([\w.]*(Error|Exception)): ')
WARNING_LINE = re.compile(r'^\s*(#\s*)?Warning:')
EXCEPTION_LINE = re.compile(r'^\s*(?:#\s*)?(?:Error:\s*)?(?:[\w]+\.)*(\w*(?:Error|Exception)): (.*)$')
OLD_BLOCK_LINE = re.compile(r'^Building: (\S+)\s*$')
DASH_LINE = re.compile(r'^-{20,}$')

# most common build errors -> what to check. First match wins, {0} = first group of the pattern
HINTS = [
    (r'No module named \'?(exec_\w+)',
     'The block code "{0}" is not installed: the block points to a version this Mutant Tools does not have. '
     'Change the block version in the AutoRigger or update Mutant Tools.'),
    (r'No object matches name: ([\w:|]+\.(?:e|vtx|f|cv)\[[\d:]+\])',
     'The component "{0}" is not on the mesh any more (mesh renamed or topology changed). '
     'Select the edges / vertices again and press Set on that field.'),
    (r'No object matches name: ([\w:|]+\.\w[\w\[\].]*)',
     'The attribute "{0}" does not exist. If it is a block attr, the block config is older than its code: '
     'use Update Block in the AutoRigger. If it comes from a pre / postcode, fix the name there.'),
    (r'No object matches name: ([\w:|]+)|(?:Object|Node) \'([\w:|]+)\' (?:not found|does not exist|is invalid)',
     'A node the block needs is missing: "{0}". Check the Set fields of the block (SetParent, SetJaw...), '
     'that the block making it builds earlier (move it up in Mutant_Build), and that a block version change '
     'did not rename it.'),
    (r'More than one object matches name: ([\w:|]+)',
     'Two nodes are called "{0}". Rename or delete one of them (often a leftover from an older build or an '
     'imported asset), then build again.'),
    (r'The attribute \'([^\']+)\' is locked or connected',
     '"{0}" is locked or already driven, so it can not be set. A postcode, another block or the controller '
     'load is setting a channel that is connected: unlock / disconnect it or remove that line.'),
    (r'(?:already connected|Connection not made)',
     'A block tries to connect an input another block already drives. Look for a duplicated block or a '
     'postcode connecting the same attr.'),
    (r'(?:Unknown object type|Unknown node type|Plug-?in .*(?:not loaded|not found)|Cannot find procedure)\W*(\w*)',
     'A Maya plugin is missing ({0}). Load it in the Plug-in Manager (matrixNodes, ngSkinTools2...) and build again.'),
    (r'(?:influence|skinCluster).*\b(?:not|no|missing)\b|\b(?:not|no|missing)\b.*(?:influence|skinCluster)',
     'Skinning failed: some joints in the Skin block SetJoints do not exist or changed name. Compare the names '
     'and wildcards with the joints the blocks make now (block version changes can rename bind joints).'),
    (r'(?:Nothing (?:is )?selected|Selection list is empty|No objects? (?:found|specified|selected))',
     'A command needed a selection and got none: usually a Set field or a wildcard (Skin SetJoints) that '
     'matched nothing.'),
    (r'Cannot parent|can not be parented|cannot be parented|is already a child',
     'A parent step failed: check the SetParent fields for loops (a block parented under its own ctrls) or a '
     'parent that does not exist yet.'),
    (r'list index out of range',
     'Something came back empty: a guide, ctrl or joint the block looks for by name. Check that the block '
     'guides are all there and the Set fields point to existing nodes.'),
    (r'\'NoneType\' object',
     'A lookup returned nothing: a guide, ctrl or config value the block expected is missing. Check the Set '
     'fields and the guides of the block.'),
    (r'KeyError: \'?([^\'\n]+)',
     'A value looked up by name ("{0}") is not there: often a block attr missing after a version change '
     '(use Update Block) or a renamed node.'),
    (r'(SyntaxError|IndentationError|NameError)',
     'Python {0} in code: if the block has a precode / postcode (or it is a Code block), check that code. '
     'Otherwise it is a bug in the block, send this log.'),
    (r'(?:Cycle on|cycle)',
     'Dependency cycle: two blocks drive each other (often a SetParent pointing to a ctrl that follows this block).'),
]


def log_file():
    return os.path.join(cmds.internalVar(usd=True), 'Mutant_log.txt')


# ----------------------------------------------------------------------------------------------
# markers (printed while the logger writes the script editor history)

def _marker(tag, data):
    print('{} {}'.format(tag, json.dumps(data)))


def plan(blocks):
    _marker(PLAN_TAG, [str(b) for b in blocks])


def section(name, kind='block', label=''):
    """kind: block / tool. label: phase of a block (Pre-Build, Deferred...)."""
    _marker(SECTION_TAG, {'kind': kind, 'name': name, 'label': label, 'time': time.time()})


def result(ok, failed=None, error=None, reverted=False):
    data = {'ok': ok, 'failed': failed, 'reverted': reverted, 'time': time.time()}
    if error is not None:
        # BlockBuildError (Utils/Rigging/block_errors.py): title + message written for the artist
        artist = bool(getattr(error, 'mutant_block_error', False))
        data['error'] = {'type': type(error).__name__,
                         'title': error.title if artist else None,
                         'message': error.message if artist else str(error),
                         'block': error.block if artist else None}
    _marker(RESULT_TAG, data)


# ----------------------------------------------------------------------------------------------
# parse

class Section(object):

    def __init__(self, name, kind='block', label='', start=None):
        self.name = name
        self.kind = kind
        self.label = label
        self.start = start
        self.end = None
        self.lines = []
        self.status = OK

    @property
    def duration(self):
        if self.start and self.end:
            return max(self.end - self.start, 0.0)
        return None

    def error_lines(self):
        return [n for n, line in enumerate(self.lines) if ERROR_LINE.match(line)]

    def exception(self):
        """(type, message) of the last exception line, or None."""
        for line in reversed(self.lines):
            match = EXCEPTION_LINE.match(line)
            if match:
                return match.group(1), match.group(2).strip()
        return None

    def hint(self):
        return hint_for(self.lines)


def _payload(line, tag):
    text = line.strip().lstrip('#').strip()
    if not text.startswith(tag):
        return None
    try:
        return json.loads(text[len(tag):].strip())
    except ValueError:
        return None


def parse(text):
    """(sections, plan, result) from the log text."""
    lines = text.splitlines()
    has_markers = any(SECTION_TAG in line for line in lines)
    sections = [Section('Builder', kind='tool')]
    planned, final = [], None
    for line in lines:
        if PLAN_TAG in line:
            planned = _payload(line, PLAN_TAG) or planned
            continue
        if RESULT_TAG in line:
            final = _payload(line, RESULT_TAG) or final
            continue
        if SECTION_TAG in line:
            data = _payload(line, SECTION_TAG)
            if data:
                sections.append(Section(data.get('name'), data.get('kind', 'block'), data.get('label', ''),
                                        data.get('time')))
                continue
        if not has_markers:
            match = OLD_BLOCK_LINE.match(line)
            if match:
                sections.append(Section(match.group(1)))
                continue
        if DASH_LINE.match(line.strip()):
            continue
        sections[-1].lines.append(line)

    # the Builder intro is only worth a row when it says something
    if not any(line.strip() for line in sections[0].lines) and len(sections) > 1:
        sections.pop(0)

    for current, following in zip(sections, sections[1:]):
        current.end = following.start
    if sections and final:
        sections[-1].end = final.get('time')

    for sec in sections:
        sec.status = ERRORS if sec.error_lines() else OK
    failed = final is not None and not final.get('ok', True)
    if final is None and sections and sections[-1].error_lines():
        failed = True  # older logs: the build stops on the block with the error
    if failed and sections:
        sections[-1].status = FAILED
        built = set(s.name for s in sections if s.kind == 'block')
        for name in planned:
            if name not in built:
                missing = Section(name)
                missing.status = NOT_BUILT
                sections.append(missing)
    return sections, planned, final


def hint_for(lines):
    """Likely cause from the error lines of a section, or None."""
    error_text = '\n'.join(line for line in lines if ERROR_LINE.match(line) or EXCEPTION_LINE.match(line)
                           or 'Error' in line)
    for pattern, text in HINTS:
        match = re.search(pattern, error_text, re.IGNORECASE)
        if match:
            groups = [g for g in match.groups() if g] if match.groups() else []
            return text.format(groups[0] if groups else '')
    return None


# ----------------------------------------------------------------------------------------------
# UI

# Mutant Tools' window colours, as in the TopoTransfer and Web to Rig windows
TONES = {OK: '#7cc48b', FAILED: '#e5847f', ERRORS: '#d9b36c', NOT_BUILT: '#6f7376'}
STYLE = '''
#BuildLog QLabel { color: #bbbbbb; }
#BuildLog QFrame#Header { background: #323436; border: none; border-radius: 8px; }
#BuildLog QLabel#Title { font-size: 16px; font-weight: bold; color: #e8e8e8; }
#BuildLog QLabel#Title[tone="ok"] { color: #7cc48b; }
#BuildLog QLabel#Title[tone="failed"] { color: #e5847f; }
#BuildLog QLabel#Meta { color: #9da1a4; }
#BuildLog QLabel#Count { color: #9da1a4; background: #2b2d2f; border-radius: 9px; padding: 2px 9px; }
#BuildLog QFrame#Card { background: #323436; border: none; border-left: 3px solid #e5847f; border-radius: 8px; }
#BuildLog QLabel#CardTitle { color: #e5847f; font-size: 13px; font-weight: bold; }
#BuildLog QLabel#CardText { color: #c8c8c8; }
#BuildLog QLabel#CauseTag { color: #8a8d90; font-size: 10px; font-weight: bold; }
#BuildLog QFrame#Row { background: #323436; border: none; border-radius: 6px; }
#BuildLog QFrame#Row:hover { background: #393c3e; }
#BuildLog QFrame#Row[status="failed"] { background: #3b3333; }
#BuildLog QLabel#Chevron { color: #8a8d90; min-width: 10px; }
#BuildLog QLabel#Name { color: #e0e0e0; }
#BuildLog QLabel#Name[status="failed"] { color: #e5847f; font-weight: bold; }
#BuildLog QLabel#Name[status="not_built"] { color: #7d8184; }
#BuildLog QLabel#Tag { color: #8a8d90; background: #2b2d2f; border-radius: 4px; padding: 1px 6px; font-size: 10px; }
#BuildLog QLabel#RowMeta { color: #8a8d90; }
#BuildLog QLabel#Hint { color: #c8c8c8; background: #2f3133; border-left: 3px solid #d9b36c; border-radius: 4px; padding: 6px 8px; }
#BuildLog QPlainTextEdit#Log {
    background: #2b2d2f; color: #c8c8c8; border: none; border-radius: 6px; padding: 4px;
    selection-background-color: #4b6eaf; }
#BuildLog QScrollArea { border: none; background: transparent; }
#BuildLog QPushButton#Ghost {
    background: transparent; color: #c8c8c8; border: 1px solid #5c5f61; border-radius: 5px; padding: 4px 10px; }
#BuildLog QPushButton#Ghost:hover { border-color: #7d8184; color: #ffffff; }
#BuildLog QPushButton#Link { background: transparent; border: none; color: #8fb0e6; padding: 0px 4px; }
#BuildLog QPushButton#Link:hover { color: #b5cdf3; }
'''

try:
    from Mutant_Tools.UI import QtMutantWindow
except Exception:  # batch / no Maya main window: show() only prints the log there
    QtMutantWindow = None

_window = None
_raw_window = None


def _named(widget, name, **properties):
    widget.setObjectName(name)
    for key, value in properties.items():
        widget.setProperty(key, value)
    return widget


def show_raw(path=None):
    """The whole log as text in the Mutant Code Reader (the old View Log)."""
    global _raw_window
    from Mutant_Tools.UI.CodeReader import load_codeReader
    path = path or log_file()
    with open(path, encoding='utf-8', errors='replace') as handle:
        text = handle.read()
    try:
        _raw_window.close()
    except Exception:
        pass
    _raw_window = load_codeReader.Code_Reader(mode='view', code='', config_attr='')
    _raw_window.previous_code = text
    _raw_window.modify_ui_based_on_mode()
    _raw_window.ui.code_text.verticalScrollBar().setValue(_raw_window.ui.code_text.verticalScrollBar().maximum())
    _raw_window.set_path_label(code_path=path)
    _raw_window.show()
    return _raw_window


def show(path=None, raw_log=None):
    """Open the Build Log window on the Mutant log (or path). raw_log: callable for the Raw Log button
    (default: show_raw)."""
    global _window
    path = path or log_file()
    raw_log = raw_log or (lambda: show_raw(path))
    text = ''
    if os.path.exists(path):
        with open(path, encoding='utf-8', errors='replace') as handle:
            text = handle.read()
    if cmds.about(batch=True):
        print(text)
        return None
    try:
        _window.close()
        _window.deleteLater()
    except Exception:
        pass
    _window = BuildLogUI(text, path=path, raw_log=raw_log)
    _window.show()
    return _window


class _Highlighter(QtGui.QSyntaxHighlighter):

    def __init__(self, document):
        super(_Highlighter, self).__init__(document)
        self.error_format = QtGui.QTextCharFormat()
        self.error_format.setForeground(QtGui.QColor(TONES[FAILED]))
        self.warning_format = QtGui.QTextCharFormat()
        self.warning_format.setForeground(QtGui.QColor('#8a8d90'))

    def highlightBlock(self, text):
        # traceback lines until the exception line are red too
        previous = self.previousBlockState() == 1
        if ERROR_LINE.match(text) or (previous and text.startswith((' ', '#'))):
            self.setFormat(0, len(text), self.error_format)
            self.setCurrentBlockState(0 if EXCEPTION_LINE.match(text) else 1)
        else:
            # warnings are fine, dimmed so the rest reads first
            if WARNING_LINE.match(text):
                self.setFormat(0, len(text), self.warning_format)
            self.setCurrentBlockState(0)


class _Row(QtWidgets.QFrame):
    clicked = QtCore.Signal()

    def mouseReleaseEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.clicked.emit()
        super(_Row, self).mouseReleaseEvent(event)


class SectionWidget(QtWidgets.QWidget):
    """One block / builder step: a row that toggles its log lines (made the first time it opens)."""

    def __init__(self, sec, parent=None):
        super(SectionWidget, self).__init__(parent)
        self.section = sec
        self.text = None

        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(4)

        self.row = _named(_Row(), 'Row', status=sec.status)
        if sec.status != NOT_BUILT:
            self.row.setCursor(QtCore.Qt.PointingHandCursor)
            self.row.clicked.connect(self.toggle)
        row = QtWidgets.QHBoxLayout(self.row)
        row.setContentsMargins(10, 6, 10, 6)
        row.setSpacing(8)
        self.chevron = _named(QtWidgets.QLabel(u'▸' if sec.status != NOT_BUILT else ''), 'Chevron')
        row.addWidget(self.chevron)
        icon = QtWidgets.QLabel(ICONS[sec.status])
        icon.setStyleSheet('color: {}; font-weight: bold;'.format(TONES[sec.status]))
        icon.setFixedWidth(14)
        row.addWidget(icon)
        row.addWidget(_named(QtWidgets.QLabel(sec.name), 'Name', status=sec.status))
        row.addWidget(_named(QtWidgets.QLabel(sec.label or ('builder' if sec.kind == 'tool' else 'block')), 'Tag'))
        row.addStretch()

        info = []
        if sec.status == NOT_BUILT:
            info.append('not built')
        elif sec.status == ERRORS:
            info.append('errors, build went on')
        if sec.duration is not None:
            info.append('{:.1f} s'.format(sec.duration))
        row.addWidget(_named(QtWidgets.QLabel(u'   ·   '.join(info)), 'RowMeta'))
        if sec.kind == 'block' and cmds.objExists(sec.name):
            select_btn = _named(QtWidgets.QPushButton('Select'), 'Link')
            select_btn.setCursor(QtCore.Qt.PointingHandCursor)
            select_btn.clicked.connect(lambda *_: cmds.objExists(sec.name) and cmds.select(sec.name, replace=True))
            row.addWidget(select_btn)
        layout.addWidget(self.row)

        self.body = QtWidgets.QWidget()
        self.body_layout = QtWidgets.QVBoxLayout(self.body)
        self.body_layout.setContentsMargins(20, 0, 0, 6)
        self.body_layout.setSpacing(6)
        self.body.setVisible(False)
        layout.addWidget(self.body)

    def _build_body(self):
        sec = self.section
        # the failed section has its cause in the card on top
        hint = sec.hint() if sec.status == ERRORS else None
        if hint:
            hint_label = _named(QtWidgets.QLabel('<b>Likely cause:</b> ' + hint), 'Hint')
            hint_label.setWordWrap(True)
            self.body_layout.addWidget(hint_label)
        lines = list(sec.lines)
        while lines and not lines[-1].strip():
            lines.pop()
        while lines and not lines[0].strip():
            lines.pop(0)
        self.text = _named(QtWidgets.QPlainTextEdit(), 'Log')
        self.text.setReadOnly(True)
        self.text.setLineWrapMode(QtWidgets.QPlainTextEdit.NoWrap)
        font = QtGui.QFontDatabase.systemFont(QtGui.QFontDatabase.FixedFont)
        self.text.setFont(font)
        self.highlighter = _Highlighter(self.text.document())
        self.text.setPlainText('\n'.join(lines) or '(nothing printed)')
        visible = min(max(len(lines), 1), 22 if sec.status == FAILED else 14)
        self.text.setFixedHeight(int(QtGui.QFontMetrics(font).lineSpacing() * visible + 20))
        self.body_layout.addWidget(self.text)
        # open on the error
        errors = sec.error_lines()
        if errors:
            self.text.setTextCursor(QtGui.QTextCursor(self.text.document().findBlockByNumber(errors[0])))
            self.text.centerCursor()

    def toggle(self):
        self.set_expanded(not self.body.isVisible())

    def set_expanded(self, expanded):
        if self.section.status == NOT_BUILT:
            return
        if expanded and self.text is None:
            self._build_body()
        self.body.setVisible(expanded)
        self.chevron.setText(u'▾' if expanded else u'▸')


class BuildLogView(QtWidgets.QWidget):
    """Header (build result), error card, one row per section, buttons."""

    def __init__(self, text, path=None, raw_log=None, parent=None):
        super(BuildLogView, self).__init__(parent)
        self.setObjectName('BuildLog')
        self.setStyleSheet(STYLE)
        self.text = text
        self.sections, self.planned, self.final = parse(text)
        failed = [s for s in self.sections if s.status == FAILED]
        failed = failed[0] if failed else None

        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(6, 6, 6, 6)
        layout.setSpacing(8)
        layout.addWidget(self._header(failed))
        if failed:
            layout.addWidget(self._error_card(failed))

        self.scroll = QtWidgets.QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setFrameShape(QtWidgets.QFrame.NoFrame)
        holder = QtWidgets.QWidget()
        rows = QtWidgets.QVBoxLayout(holder)
        rows.setContentsMargins(0, 0, 4, 0)
        rows.setSpacing(4)
        self.rows = []
        for sec in self.sections:
            widget = SectionWidget(sec)
            rows.addWidget(widget)
            self.rows.append(widget)
        rows.addStretch()
        self.scroll.setWidget(holder)
        layout.addWidget(self.scroll, 1)

        buttons = QtWidgets.QHBoxLayout()
        buttons.setSpacing(6)
        for label, callback in [('Expand All', lambda *_: self.expand(True)),
                                ('Collapse All', lambda *_: self.expand(False)),
                                ('Copy Log', lambda *_: QtWidgets.QApplication.clipboard().setText(self.text))]:
            buttons.addWidget(self._ghost(label, callback))
        buttons.addStretch()
        if raw_log:
            raw_btn = self._ghost('Raw Log', lambda *_: raw_log())
            raw_btn.setToolTip(path or '')
            buttons.addWidget(raw_btn)
        layout.addLayout(buttons)

        # only the section that stopped the build opens
        for widget in self.rows:
            if widget.section.status == FAILED:
                widget.set_expanded(True)
                QtCore.QTimer.singleShot(0, lambda w=widget: self.scroll.ensureWidgetVisible(w, 0, 0))

    def _ghost(self, label, callback):
        button = _named(QtWidgets.QPushButton(label), 'Ghost')
        button.setCursor(QtCore.Qt.PointingHandCursor)
        button.clicked.connect(callback)
        return button

    def _header(self, failed):
        blocks = [s for s in self.sections if s.kind == 'block']
        built = [s for s in blocks if s.status in (OK, ERRORS)]
        not_built = [s for s in blocks if s.status == NOT_BUILT]
        times = [s.start for s in self.sections if s.start]
        total_time = self.final['time'] - min(times) if times and self.final and self.final.get('time') else None

        if failed:
            tone, title = FAILED, u'✖  Build failed on {}'.format(failed.name)
            meta = 'The scene was reverted to how it was before the build.' if (self.final or {}).get('reverted') \
                else 'Revert on Fail is off, the scene was left where the build stopped.' if self.final else ''
        elif not blocks and not self.final:
            tone, title, meta = 'empty', 'No build log yet', 'Build the rig to see its log here.'
        else:
            tone, title = OK, u'✔  Build complete'
            with_errors = [s for s in self.sections if s.status == ERRORS]
            meta = '{} block{} printed errors, open them below.'.format(
                len(with_errors), '' if len(with_errors) == 1 else 's') if with_errors else ''

        header = _named(QtWidgets.QFrame(), 'Header')
        col = QtWidgets.QVBoxLayout(header)
        col.setContentsMargins(14, 12, 14, 12)
        col.setSpacing(6)
        col.addWidget(_named(QtWidgets.QLabel(title), 'Title', tone=tone))
        if meta:
            meta_label = _named(QtWidgets.QLabel(meta), 'Meta')
            meta_label.setWordWrap(True)
            col.addWidget(meta_label)
        if blocks:
            chips = ['{} built'.format(len(built))]
            if not_built:
                chips.append('{} not built'.format(len(not_built)))
            if total_time is not None:
                chips.append('{:.1f} s'.format(total_time))
            counts = QtWidgets.QHBoxLayout()
            counts.setSpacing(6)
            for chip in chips:
                counts.addWidget(_named(QtWidgets.QLabel(chip), 'Count'))
            counts.addStretch()
            col.addLayout(counts)
        return header

    def _error_card(self, failed):
        error = (self.final or {}).get('error') or {}
        exception = failed.exception()
        if error.get('title'):
            # BlockBuildError: written for the artist, no guessing
            title, message, hint = error['title'], error.get('message') or '', None
        else:
            if error.get('message'):
                # the exception that stopped the build, the section may print others before it
                title = '{}: {}'.format(error.get('type'), error['message'].strip().splitlines()[0])
            elif exception:
                title = '{}: {}'.format(*exception)
            else:
                title = 'Error in {}'.format(failed.name)
            message = ''
            hint = hint_for(failed.lines + [title])

        card = _named(QtWidgets.QFrame(), 'Card')
        col = QtWidgets.QVBoxLayout(card)
        col.setContentsMargins(14, 10, 14, 12)
        col.setSpacing(6)
        title_label = _named(QtWidgets.QLabel(title), 'CardTitle')
        title_label.setWordWrap(True)
        title_label.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse)
        col.addWidget(title_label)
        if message:
            message_label = _named(QtWidgets.QLabel(message), 'CardText')
            message_label.setWordWrap(True)
            message_label.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse)
            col.addWidget(message_label)
        elif hint:
            col.addWidget(_named(QtWidgets.QLabel('LIKELY CAUSE'), 'CauseTag'))
            hint_label = _named(QtWidgets.QLabel(hint), 'CardText')
            hint_label.setWordWrap(True)
            col.addWidget(hint_label)
        else:
            col.addWidget(_named(QtWidgets.QLabel('No known cause for this one, the open block below shows where it '
                                                  'stopped.'), 'Meta'))
        return card

    def expand(self, expanded):
        for widget in self.rows:
            widget.set_expanded(expanded)


_Base = QtMutantWindow.Qt_Mutant if QtMutantWindow else QtWidgets.QWidget


class BuildLogUI(_Base):
    """The Build Log in a Mutant Tools window."""

    def __init__(self, text, path=None, raw_log=None):
        super(BuildLogUI, self).__init__()
        self.setWindowTitle('Mutant Build Log')
        self.view = BuildLogView(text, path=path, raw_log=raw_log)
        # Qt_Mutant.minimize hides self.ui
        self.ui = self.view
        if QtMutantWindow:
            self.set_title('Build Log')
            self.master_ui.mutant_Layout.addWidget(self.view)
        else:
            QtWidgets.QVBoxLayout(self).addWidget(self.view)
        self.resize(760, 680)
