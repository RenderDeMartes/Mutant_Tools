from __future__ import absolute_import
'''
Tooltips and a right click "Learn more" for the buttons of a designer .ui file.

The help lives next to the .ui file as <ui name>_help.json:
{
    "button_object_name": {
        "tip": "One line, what happens when you click it.",
        "what": "A few sentences: what it does and when to use it.",
        "steps": ["Select ...", "Click it.", "Check ..."],
        "examples": ["...", "..."],
        "details": "Under the hood: nodes / attrs it touches, gotchas.",
        "code": {"file": "UI/Helpers/load_helpers.py", "function": "lock_geo", "connect": "self.lock_geo"}
    }
}

- A tooltip already set in the .ui or by code is kept, the json tip only fills empty ones.
- Buttons that already have their own right click (custom context menu, a menu, actions)
  are skipped, they keep only the tooltip.
- Buttons not in the json are left alone (dynamic buttons, block buttons...).
- Learn more has a Help tab and a Code tab. The Code tab reads the function from the file
  when it opens, so it follows code edits, and can open it in VS Code at that line.

how to:
from Mutant_Tools.UI.CustomWidgets import button_help
button_help.install_later(self.ui, ui_file_path)
'''
import ast
import json
import os
import shutil
import subprocess

try:
    from PySide6 import QtCore, QtGui, QtWidgets
except ImportError:
    from PySide2 import QtCore, QtGui, QtWidgets

FOLDER = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CONTEXT_SIGNAL = QtCore.SIGNAL('customContextMenuRequested(QPoint)')


def help_json_path(ui_file):
    return os.path.splitext(ui_file)[0] + '_help.json'


def read_help(ui_file):
    path = help_json_path(ui_file)
    if not os.path.exists(path):
        return {}
    try:
        with open(path, encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print('Button help: could not read {}: {}'.format(path, e))
        return {}


def has_own_right_click(button):
    if button.contextMenuPolicy() != QtCore.Qt.DefaultContextMenu:
        return True
    if hasattr(button, 'menu') and button.menu():
        return True
    return False


def _button_label(button, name):
    text = button.text().replace('&', '').strip()
    if len(text) > 2:
        return text
    return name.replace('_', ' ').strip().title()


def function_location(code):
    """(absolute path, first line, source) of code['function'] in code['file'], or None."""
    if not code or not code.get('function') or not code.get('file'):
        return None
    path = os.path.join(FOLDER, code['file'])
    if not os.path.exists(path):
        return None
    with open(path, encoding='utf-8', errors='ignore') as f:
        source = f.read()
    for node in ast.walk(ast.parse(source)):
        if isinstance(node, ast.FunctionDef) and node.name == code['function']:
            lines = source.splitlines()[node.lineno - 1:node.end_lineno]
            return os.path.normpath(path), node.lineno, '\n'.join(lines)
    return None


def _vscode_executable():
    found = shutil.which('code')
    if found:
        return found
    local = os.environ.get('LOCALAPPDATA', '')
    for candidate in [os.path.join(local, 'Programs', 'Microsoft VS Code', 'bin', 'code.cmd'),
                      os.path.join(os.environ.get('ProgramFiles', ''), 'Microsoft VS Code', 'bin', 'code.cmd'),
                      '/usr/local/bin/code', '/usr/bin/code']:
        if candidate and os.path.exists(candidate):
            return candidate
    return None


def open_in_vscode(path, line=1):
    """Open path at line in VS Code: the code command when found, else the vscode:// link."""
    executable = _vscode_executable()
    if executable:
        subprocess.Popen([executable, '-g', '{}:{}'.format(path, line)], shell=executable.endswith('.cmd'))
        return True
    url = QtCore.QUrl('vscode://file/{}:{}'.format(path.replace('\\', '/'), line))
    return QtGui.QDesktopServices.openUrl(url)


# -------------------------------------------------------------------

DIALOG_QSS = '''
QDialog#LearnMore { background: #2b2b2b; }
QWidget#LearnMoreBody, QWidget#CodePage { background: #2b2b2b; }
QFrame#Header { background: #353535; border-bottom: 1px solid #1f1f1f; }
QLabel#IconTile { background: #444444; border-radius: 8px; }
QLabel#Title { color: #f0f0f0; }
QLabel#Tip { color: #b8b8b8; }
QTabWidget#Tabs::pane { border: none; background: #2b2b2b; }
QTabWidget#Tabs > QTabBar::tab { background: #353535; color: #b8b8b8; padding: 6px 18px; border: none;
    border-bottom: 2px solid #353535; min-width: 60px; }
QTabWidget#Tabs > QTabBar::tab:selected { color: #f0f0f0; border-bottom: 2px solid #8fb4d0; }
QTabWidget#Tabs > QTabBar::tab:hover { color: #f0f0f0; }
QFrame#Card { background: #333333; border: 1px solid #3d3d3d; border-radius: 6px; }
QLabel#CardTitle { color: #8fb4d0; }
QLabel#Body { color: #dcdcdc; }
QLabel#Number { background: #4a6a85; color: #ffffff; border-radius: 10px; }
QLabel#Bullet { color: #8fb4d0; }
QLabel#Path { font-family: Consolas, "Courier New", monospace; color: #c9c9c9; background: #252525;
    border: 1px solid #3d3d3d; border-radius: 4px; padding: 4px 6px; }
QLabel#Muted { font-family: Consolas, "Courier New", monospace; color: #9a9a9a; }
QPushButton#Action { background: #3d3d3d; border: 1px solid #555555; border-radius: 4px; padding: 4px 12px; color: #e0e0e0; }
QPushButton#Action:hover { border-color: #8fb4d0; }
QPushButton#Primary, QPushButton#Close { background: #4a6a85; border: none; border-radius: 4px; padding: 5px 16px; color: #ffffff; }
QPushButton#Primary:hover, QPushButton#Close:hover { background: #5a7d9a; }
QScrollArea { background: transparent; border: none; }
'''
BODY_WIDTH = 520
CODE_HEIGHT = 440


def _scaled_font(font, scale, bold=False):
    # Maya fonts are often pixel sized (pointSizeF() == -1)
    if font.pointSizeF() > 0:
        font.setPointSizeF(font.pointSizeF() * scale)
    elif font.pixelSize() > 0:
        font.setPixelSize(int(round(font.pixelSize() * scale)))
    font.setBold(bold)
    return font


def _label(text, name, wrap=True, selectable=True):
    label = QtWidgets.QLabel(text)
    label.setObjectName(name)
    label.setWordWrap(wrap)
    if selectable:
        label.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse)
    return label


def _button(text, name, callback):
    button = QtWidgets.QPushButton(text)
    button.setObjectName(name)
    button.setCursor(QtCore.Qt.PointingHandCursor)
    button.clicked.connect(callback)
    return button


def _card(title):
    card = QtWidgets.QFrame()
    card.setObjectName('Card')
    layout = QtWidgets.QVBoxLayout(card)
    layout.setContentsMargins(12, 10, 12, 12)
    layout.setSpacing(8)
    head = _label(title.upper(), 'CardTitle', wrap=False, selectable=False)
    head.setFont(_scaled_font(head.font(), 0.85, bold=True))
    layout.addWidget(head)
    return card, layout


def _row(marker, text):
    row = QtWidgets.QHBoxLayout()
    row.setSpacing(8)
    row.addWidget(marker, 0, QtCore.Qt.AlignTop)
    row.addWidget(_label(text, 'Body'), 1)
    return row


def _number(n):
    badge = _label(str(n), 'Number', wrap=False, selectable=False)
    badge.setFixedSize(20, 20)
    badge.setAlignment(QtCore.Qt.AlignCenter)
    badge.setFont(_scaled_font(badge.font(), 0.85, bold=True))
    return badge


class LearnMoreDialog(QtWidgets.QDialog):
    """Help tab (what it does, how to use it, examples, under the hood) and Code tab (the handler source)."""

    def __init__(self, button, name, entry, parent=None):
        super(LearnMoreDialog, self).__init__(parent or button.window())
        self.setObjectName('LearnMore')
        self.setStyleSheet(DIALOG_QSS)
        title_text = _button_label(button, name)
        self.setWindowTitle('Learn more: {}'.format(title_text))
        self.code = entry.get('code') or {}
        self.location = function_location(self.code)

        outer = QtWidgets.QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)
        outer.addWidget(self._header(button, title_text, entry.get('tip', '')))

        self.tabs = QtWidgets.QTabWidget()
        self.tabs.setObjectName('Tabs')
        self.tabs.setDocumentMode(True)
        self.tabs.addTab(self._help_page(entry), 'Help')
        if self.location:
            self.tabs.addTab(self._code_page(), 'Code')
        outer.addWidget(self.tabs)

        footer = QtWidgets.QHBoxLayout()
        footer.setContentsMargins(16, 8, 16, 12)
        footer.addStretch(1)
        footer.addWidget(_button('Close', 'Close', self.reject))
        outer.addLayout(footer)
        outer.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)

    def _header(self, button, title_text, tip_text):
        header = QtWidgets.QFrame()
        header.setObjectName('Header')
        layout = QtWidgets.QHBoxLayout(header)
        layout.setContentsMargins(16, 14, 16, 14)
        layout.setSpacing(12)
        if not button.icon().isNull():
            tile = QtWidgets.QLabel()
            tile.setObjectName('IconTile')
            tile.setFixedSize(44, 44)
            tile.setAlignment(QtCore.Qt.AlignCenter)
            tile.setPixmap(button.icon().pixmap(28, 28))
            layout.addWidget(tile, 0, QtCore.Qt.AlignTop)
        texts = QtWidgets.QVBoxLayout()
        texts.setSpacing(2)
        title = _label(title_text, 'Title', wrap=True)
        title.setFont(_scaled_font(title.font(), 1.6, bold=True))
        texts.addWidget(title)
        if tip_text:
            texts.addWidget(_label(tip_text, 'Tip'))
        layout.addLayout(texts, 1)
        return header

    def _help_page(self, entry):
        body = QtWidgets.QWidget()
        body.setObjectName('LearnMoreBody')
        body.setFixedWidth(BODY_WIDTH)
        layout = QtWidgets.QVBoxLayout(body)
        layout.setContentsMargins(16, 14, 16, 14)
        layout.setSpacing(10)

        if entry.get('what'):
            card, card_layout = _card('What it does')
            card_layout.addWidget(_label(entry['what'], 'Body'))
            layout.addWidget(card)
        if entry.get('steps'):
            card, card_layout = _card('How to use it')
            for n, step in enumerate(entry['steps'], 1):
                card_layout.addLayout(_row(_number(n), step))
            layout.addWidget(card)
        if entry.get('examples'):
            card, card_layout = _card('Examples')
            for example in entry['examples']:
                card_layout.addLayout(_row(_label(u'›', 'Bullet', wrap=False, selectable=False), example))
            layout.addWidget(card)
        if entry.get('details') or self.code:
            card, card_layout = _card('Under the hood')
            if entry.get('details'):
                card_layout.addWidget(_label(entry['details'], 'Body'))
            if self.code:
                where = self.code.get('file', '')
                if self.location:
                    where += u'  ›  {}()  line {}'.format(self.code['function'], self.location[1])
                card_layout.addWidget(_label(where, 'Path'))
                if self.code.get('connect') and self.code.get('connect') != 'self.{}'.format(self.code.get('function')):
                    card_layout.addWidget(_label(u'clicked › {}'.format(self.code['connect']), 'Muted'))
            layout.addWidget(card)

        scroll = QtWidgets.QScrollArea()
        scroll.setWidget(body)
        scroll.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        scroll.setFixedWidth(BODY_WIDTH)
        self.help_scroll = scroll
        self.help_body = body
        self._fitted = False
        return scroll

    def showEvent(self, event):
        super(LearnMoreDialog, self).showEvent(event)
        if not self._fitted:
            self._fitted = True
            self.fit_help_page()

    def fit_help_page(self):
        """Size the Help page once the dialog stylesheet is applied (fonts / padding change the wrapped heights).
        Taller than 65% of the screen: it scrolls."""
        body, scroll = self.help_body, self.help_scroll
        for widget in [body] + body.findChildren(QtWidgets.QWidget):
            widget.ensurePolished()
        layout = body.layout()
        layout.invalidate()
        body_height = layout.totalHeightForWidth(BODY_WIDTH)
        max_height = int(QtGui.QGuiApplication.primaryScreen().availableGeometry().height() * 0.65)
        needs_scroll = body_height > max_height
        scrollbar = scroll.verticalScrollBar().sizeHint().width() if needs_scroll else 0
        if needs_scroll:
            # the scrollbar takes width: measure again at the narrower width
            body.setFixedWidth(BODY_WIDTH - scrollbar)
            body_height = layout.totalHeightForWidth(BODY_WIDTH - scrollbar)
        body.setFixedHeight(body_height)
        scroll.setFixedHeight(min(body_height, max_height))
        code_page = self.tabs.widget(1)
        if code_page is not None:
            # keep both tabs the same height so switching tabs does not resize the window
            scroll.setFixedHeight(max(scroll.height(), min(code_page.sizeHint().height(), max_height)))
        self.adjustSize()

    def _code_page(self):
        path, line, source = self.location
        page = QtWidgets.QWidget()
        page.setObjectName('CodePage')
        layout = QtWidgets.QVBoxLayout(page)
        layout.setContentsMargins(16, 12, 16, 12)
        layout.setSpacing(8)

        layout.addWidget(_label(u'{}  ›  {}()  line {}'.format(self.code['file'], self.code['function'], line), 'Path'))
        buttons = QtWidgets.QHBoxLayout()
        buttons.addWidget(_button('Open in VS Code', 'Primary', lambda: self.open_vscode(path, line)))
        buttons.addWidget(_button('Copy path', 'Action',
                                  lambda: QtWidgets.QApplication.clipboard().setText('{}:{}'.format(path, line))))
        buttons.addWidget(_button('Copy code', 'Action', lambda: QtWidgets.QApplication.clipboard().setText(source)))
        buttons.addStretch(1)
        layout.addLayout(buttons)

        try:
            from Mutant_Tools.UI.CustomWidgets import codeEditorWidget
            editor = codeEditorWidget.IDECodeEditor(page)
        except Exception:
            editor = QtWidgets.QPlainTextEdit(page)
            editor.setFont(QtGui.QFontDatabase.systemFont(QtGui.QFontDatabase.FixedFont))
        editor.setPlainText(source)
        editor.setReadOnly(True)
        editor.setLineWrapMode(QtWidgets.QPlainTextEdit.NoWrap)
        editor.setFixedHeight(CODE_HEIGHT)
        layout.addWidget(editor)
        page.setFixedWidth(BODY_WIDTH)
        return page

    def open_vscode(self, path, line):
        if not open_in_vscode(path, line):
            QtWidgets.QMessageBox.warning(self, 'Open in VS Code',
                                          'VS Code was not found. Install it or add "code" to the PATH.\n{}:{}'.format(path, line))


def show_learn_more(button, name, entry):
    dialog = LearnMoreDialog(button, name, entry)
    dialog.setAttribute(QtCore.Qt.WA_DeleteOnClose)
    dialog.show()
    return dialog


def _context_menu(button, name, entry, pos):
    # the tool connected its own right click after the install: let that one win
    if button.receivers(CONTEXT_SIGNAL) > 1:
        return
    menu = QtWidgets.QMenu(button)
    menu.addAction('Learn more', lambda: show_learn_more(button, name, entry))
    menu.exec_(button.mapToGlobal(pos)) if hasattr(menu, 'exec_') else menu.exec(button.mapToGlobal(pos))


def install(root, ui_file):
    """Tooltips + Learn more on the buttons of root (the widget loaded from ui_file)."""
    data = read_help(ui_file)
    if not data or root is None:
        return 0
    count = 0
    for button in root.findChildren(QtWidgets.QAbstractButton):
        name = button.objectName()
        entry = data.get(name)
        if not entry:
            continue
        own_right_click = has_own_right_click(button)
        if not button.toolTip() and entry.get('tip'):
            button.setToolTip(entry['tip'])
        if own_right_click:
            continue
        button.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        button.customContextMenuRequested.connect(
            lambda pos, b=button, n=name, e=entry: _context_menu(b, n, e, pos))
        count += 1
    return count


def install_later(root, ui_file):
    """Install once the tool finished its own setup (its right clicks are connected by then)."""
    QtCore.QTimer.singleShot(0, lambda: _safe_install(root, ui_file))


def _safe_install(root, ui_file):
    try:
        install(root, ui_file)
    except RuntimeError:
        # widget deleted before the event loop came back
        pass
    except Exception as e:
        print('Button help: {}'.format(e))
