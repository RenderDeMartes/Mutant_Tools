from __future__ import absolute_import, division

try:
    from PySide6 import QtGui, QtCore, QtWidgets
except:
    from PySide2 import QtGui, QtCore, QtWidgets

import re


class PythonSyntaxHighlighter(QtGui.QSyntaxHighlighter):

    def __init__(self, document):
        super(PythonSyntaxHighlighter, self).__init__(document)

        self.formats = {}
        self.formats['keyword'] = QtGui.QTextCharFormat()
        self.formats['keyword'].setForeground(QtGui.QColor(86, 156, 214))
        self.formats['keyword'].setFontWeight(QtGui.QFont.Bold)

        self.formats['builtin'] = QtGui.QTextCharFormat()
        self.formats['builtin'].setForeground(QtGui.QColor(78, 201, 176))

        self.formats['number'] = QtGui.QTextCharFormat()
        self.formats['number'].setForeground(QtGui.QColor(181, 206, 168))

        self.formats['string'] = QtGui.QTextCharFormat()
        self.formats['string'].setForeground(QtGui.QColor(206, 145, 120))

        self.formats['comment'] = QtGui.QTextCharFormat()
        self.formats['comment'].setForeground(QtGui.QColor(106, 153, 85))

        self.formats['decorator'] = QtGui.QTextCharFormat()
        self.formats['decorator'].setForeground(QtGui.QColor(220, 220, 170))

        self.formats['function'] = QtGui.QTextCharFormat()
        self.formats['function'].setForeground(QtGui.QColor(220, 220, 170))

        self.formats['class'] = QtGui.QTextCharFormat()
        self.formats['class'].setForeground(QtGui.QColor(78, 201, 176))
        self.formats['class'].setFontWeight(QtGui.QFont.Bold)

        self.formats['attribute'] = QtGui.QTextCharFormat()
        self.formats['attribute'].setForeground(QtGui.QColor(156, 220, 254))

        self.formats['constant'] = QtGui.QTextCharFormat()
        self.formats['constant'].setForeground(QtGui.QColor(197, 134, 192))

        keywords = [
            'False', 'None', 'True', 'and', 'as', 'assert', 'async', 'await',
            'break', 'class', 'continue', 'def', 'del', 'elif', 'else', 'except',
            'finally', 'for', 'from', 'global', 'if', 'import', 'in', 'is',
            'lambda', 'nonlocal', 'not', 'or', 'pass', 'raise', 'return', 'try',
            'while', 'with', 'yield'
        ]

        builtins = [
            'abs', 'all', 'any', 'bin', 'bool', 'dict', 'enumerate', 'filter',
            'float', 'format', 'int', 'len', 'list', 'map', 'max', 'min', 'open',
            'print', 'range', 'reversed', 'set', 'sorted', 'str', 'sum', 'tuple',
            'type', 'zip'
        ]

        self.rules = []
        for keyword in keywords:
            self.rules.append((re.compile(r'\b{}\b'.format(re.escape(keyword))), self.formats['keyword'], 0))
        for builtin in builtins:
            self.rules.append((re.compile(r'\b{}\b'.format(re.escape(builtin))), self.formats['builtin'], 0))

        self.rules.append((re.compile(r'\bdef\s+([A-Za-z_][A-Za-z0-9_]*)'), self.formats['function'], 1))
        self.rules.append((re.compile(r'\bclass\s+([A-Za-z_][A-Za-z0-9_]*)'), self.formats['class'], 1))
        self.rules.append((re.compile(r'\bself\.([A-Za-z_][A-Za-z0-9_]*)'), self.formats['attribute'], 1))
        self.rules.append((re.compile(r'\b([A-Za-z_][A-Za-z0-9_]*)\s*(?=\()'), self.formats['function'], 1))
        self.rules.append((re.compile(r'\b[A-Z_][A-Z0-9_]{2,}\b'), self.formats['constant'], 0))
        self.rules.append((re.compile(r'@[A-Za-z_][A-Za-z0-9_]*'), self.formats['decorator'], 0))
        self.rules.append((re.compile(r'\b[0-9]+(?:\.[0-9]+)?\b'), self.formats['number'], 0))

        # Keep strings/comments at the end so they override other token styles.
        self.rules.append((re.compile(r'"[^"\\]*(?:\\.[^"\\]*)*"'), self.formats['string'], 0))
        self.rules.append((re.compile(r"'[^'\\]*(?:\\.[^'\\]*)*'"), self.formats['string'], 0))
        self.rules.append((re.compile(r'#.*$'), self.formats['comment'], 0))

        self.multi_line_single = (re.compile(r"'''"), re.compile(r"'''"), 1, self.formats['string'])
        self.multi_line_double = (re.compile(r'"""'), re.compile(r'"""'), 2, self.formats['string'])

    def highlightBlock(self, text):
        for pattern, text_format, capture_group in self.rules:
            for match in pattern.finditer(text):
                if capture_group > 0:
                    try:
                        start = match.start(capture_group)
                        end = match.end(capture_group)
                    except IndexError:
                        start = match.start()
                        end = match.end()
                else:
                    start = match.start()
                    end = match.end()

                if end > start:
                    self.setFormat(start, end - start, text_format)

        self.setCurrentBlockState(0)
        if self._match_multiline(text, *self.multi_line_single):
            return
        self._match_multiline(text, *self.multi_line_double)

    def _match_multiline(self, text, start_pattern, end_pattern, state, text_format):
        if self.previousBlockState() == state:
            start = 0
            start_len = 0
        else:
            start_match = start_pattern.search(text)
            if not start_match:
                return False
            start = start_match.start()
            start_len = start_match.end() - start_match.start()

        while start >= 0:
            end_match = end_pattern.search(text, start + start_len)
            if end_match:
                end = end_match.end()
                self.setCurrentBlockState(0)
            else:
                end = len(text)
                self.setCurrentBlockState(state)

            self.setFormat(start, max(0, end - start), text_format)

            if not end_match:
                break

            next_start_match = start_pattern.search(text, end)
            if next_start_match:
                start = next_start_match.start()
                start_len = next_start_match.end() - next_start_match.start()
            else:
                start = -1

        return self.currentBlockState() == state


class SearchReplacePanel(QtWidgets.QFrame):
    def __init__(self, editor):
        super(SearchReplacePanel, self).__init__(editor)
        self.editor = editor
        
        self.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.setStyleSheet(
            'SearchReplacePanel {'
            '  background-color: #2D2D2D;'
            '  border: 1px solid #3F3F3F;'
            '  border-radius: 4px;'
            '}'
            'QLineEdit {'
            '  background-color: #3C3C3C;'
            '  color: #CCCCCC;'
            '  border: 1px solid #555555;'
            '  border-radius: 2px;'
            '  padding: 2px 4px;'
            '}'
            'QPushButton {'
            '  background-color: #3A3A3A;'
            '  color: #DDDDDD;'
            '  border: 1px solid #555555;'
            '  border-radius: 2px;'
            '  padding: 2px 6px;'
            '  font-size: 11px;'
            '}'
            'QPushButton:hover {'
            '  background-color: #4A4A4A;'
            '}'
            'QLabel {'
            '  color: #FF5555;'
            '  font-size: 10px;'
            '}'
        )
        
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(6, 6, 6, 6)
        layout.setSpacing(4)
        
        # Row 1: Search field + Find button + Close button
        row1 = QtWidgets.QHBoxLayout()
        self.search_input = QtWidgets.QLineEdit()
        self.search_input.setPlaceholderText('Search...')
        self.search_input.setMinimumWidth(120)
        row1.addWidget(self.search_input)
        
        self.find_btn = QtWidgets.QPushButton('Find')
        self.find_btn.clicked.connect(self.find_next)
        row1.addWidget(self.find_btn)
        
        self.close_btn = QtWidgets.QPushButton('X')
        self.close_btn.setFixedSize(18, 18)
        self.close_btn.setStyleSheet('border: none; background: transparent; color: #888888; font-weight: bold;')
        self.close_btn.clicked.connect(self.hide_panel)
        row1.addWidget(self.close_btn)
        layout.addLayout(row1)
        
        # Row 2: Replace field + Replace button + Replace All button
        row2 = QtWidgets.QHBoxLayout()
        self.replace_input = QtWidgets.QLineEdit()
        self.replace_input.setPlaceholderText('Replace with...')
        self.replace_input.setMinimumWidth(120)
        row2.addWidget(self.replace_input)
        
        self.replace_btn = QtWidgets.QPushButton('Replace')
        self.replace_btn.clicked.connect(self.replace_current)
        row2.addWidget(self.replace_btn)
        
        self.replace_all_btn = QtWidgets.QPushButton('All')
        self.replace_all_btn.clicked.connect(self.replace_all)
        row2.addWidget(self.replace_all_btn)
        layout.addLayout(row2)
        
        # Status Label
        self.status_label = QtWidgets.QLabel('')
        layout.addWidget(self.status_label)
        
        # Adjust panel size to contents
        self.adjustSize()
        self.hide()
        
        # Set shortcut context
        self.search_input.returnPressed.connect(self.find_next)
        self.replace_input.returnPressed.connect(self.replace_current)

    def show_panel(self):
        self.adjustSize()
        editor_width = self.editor.width()
        panel_width = self.width()
        scrollbar_w = self.editor.verticalScrollBar().width() if self.editor.verticalScrollBar().isVisible() else 0
        x = max(10, editor_width - panel_width - scrollbar_w - 10)
        y = 5
        self.move(x, y)
        self.show()
        self.raise_()
        self.search_input.setFocus()
        self.search_input.selectAll()

    def hide_panel(self):
        self.hide()
        self.editor.setFocus()

    def find_next(self):
        search_text = self.search_input.text()
        if not search_text:
            return
        
        cursor = self.editor.textCursor()
        document = self.editor.document()
        
        found_cursor = document.find(search_text, cursor)
        if found_cursor.isNull():
            found_cursor = document.find(search_text, 0)
            
        if not found_cursor.isNull():
            self.editor.setTextCursor(found_cursor)
            self.editor.ensureCursorVisible()
            self.status_label.setText('')
        else:
            self.status_label.setText('Text not found!')

    def replace_current(self):
        search_text = self.search_input.text()
        replace_text = self.replace_input.text()
        if not search_text:
            return
            
        cursor = self.editor.textCursor()
        if cursor.selectedText() == search_text:
            cursor.insertText(replace_text)
            self.find_next()
        else:
            self.find_next()

    def replace_all(self):
        search_text = self.search_input.text()
        replace_text = self.replace_input.text()
        if not search_text:
            return
            
        document = self.editor.document()
        cursor = self.editor.textCursor()
        cursor.beginEditBlock()
        
        found_cursor = document.find(search_text, 0)
        count = 0
        while not found_cursor.isNull():
            found_cursor.insertText(replace_text)
            found_cursor = document.find(search_text, found_cursor)
            count += 1
            
        cursor.endEditBlock()
        self.editor.refresh_editor()
        self.status_label.setText('Replaced {} occurrences.'.format(count))


class LineNumberArea(QtWidgets.QWidget):

    def __init__(self, editor):
        super(LineNumberArea, self).__init__(editor)
        self.editor = editor

    def sizeHint(self):
        return QtCore.QSize(self.editor.line_number_area_width(), 0)

    def paintEvent(self, event):
        self.editor.line_number_area_paint_event(event)


class IDECodeEditor(QtWidgets.QPlainTextEdit):

    def __init__(self, parent=None, max_height_limit=600):
        super(IDECodeEditor, self).__init__(parent)
        self.max_height_limit = max_height_limit

        self.line_number_area = LineNumberArea(self)
        self.block_count_changed_connection = self.blockCountChanged.connect(self.update_line_number_area_width)
        self.update_request_connection = self.updateRequest.connect(self.update_line_number_area)
        self.cursor_position_connection = self.cursorPositionChanged.connect(self.highlight_current_line)

        self.setLineWrapMode(QtWidgets.QPlainTextEdit.NoWrap)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.setTabStopDistance(self.fontMetrics().horizontalAdvance(' ') * 4)

        font = QtGui.QFont('Consolas')
        if not QtGui.QFontInfo(font).exactMatch():
            font = QtGui.QFont('Courier New')
        font.setPointSize(10)
        self.setFont(font)

        self.setStyleSheet(
            'QPlainTextEdit {'
            'background-color: #1E1E1E;'
            'color: #D4D4D4;'
            'selection-background-color: #264F78;'
            'border: 1px solid #2D2D2D;'
            'padding: 4px;'
            '}'
            'QScrollBar:horizontal { height: 12px; }'
            'QScrollBar:vertical { width: 12px; }'
        )

        self.highlighter = PythonSyntaxHighlighter(self.document())

        self.update_line_number_area_width(0)
        self.highlight_current_line()

        self.is_manually_resized = False
        self.textChanged.connect(self.on_text_changed)
        self.search_replace_panel = SearchReplacePanel(self)

    def on_text_changed(self):
        if not getattr(self, 'is_manually_resized', False):
            self.adjust_height_to_fit()

    def show_search_replace(self):
        if not getattr(self, 'search_replace_panel', None):
            self.search_replace_panel = SearchReplacePanel(self)
        self.search_replace_panel.show_panel()

    def keyPressEvent(self, event):
        # Intercept Ctrl+F when editor has focus
        if event.key() == QtCore.Qt.Key_F and event.modifiers() == QtCore.Qt.ControlModifier:
            self.show_search_replace()
            event.accept()
            return
            
        # Let Escape close the panel if visible
        if event.key() == QtCore.Qt.Key_Escape:
            if getattr(self, 'search_replace_panel', None) and self.search_replace_panel.isVisible():
                self.search_replace_panel.hide_panel()
                event.accept()
                return
                
        super(IDECodeEditor, self).keyPressEvent(event)

    def adjust_height_to_fit(self):
        line_count = max(1, self.blockCount())
        line_height = self.fontMetrics().lineSpacing()
        doc_margin = self.document().documentMargin()
        
        # Calculate needed height (adding 2 extra lines worth of spacing to prevent vertical scrollbar)
        needed_height = int((line_count + 2) * line_height + doc_margin * 2 + 10)
        
        # If the horizontal scrollbar is visible, add its height
        if self.horizontalScrollBar().isVisible():
            needed_height += self.horizontalScrollBar().height()
            
        needed_height = max(80, needed_height)
        if getattr(self, 'max_height_limit', None) is not None:
            needed_height = min(needed_height, self.max_height_limit)
        
        self.setFixedHeight(needed_height)
        self.line_number_area.update()
        self.updateGeometry()
        
        parent = self.parentWidget()
        if parent:
            parent.update()
            if parent.layout():
                parent.layout().activate()

    def insertFromMimeData(self, source):
        # On paste, reset manual resize so it auto-fits to the new pasted content size
        self.is_manually_resized = False
        super(IDECodeEditor, self).insertFromMimeData(source)
        self.refresh_editor()

    def refresh_editor(self):
        self.adjust_height_to_fit()
        if getattr(self, 'highlighter', None):
            self.highlighter.rehighlight()
        self.update_line_number_area_width(0)
        self.line_number_area.update()
        self.viewport().update()

    def line_number_area_width(self):
        digits = len(str(max(1, self.blockCount())))
        return 10 + self.fontMetrics().horizontalAdvance('9') * digits

    def update_line_number_area_width(self, _):
        self.setViewportMargins(self.line_number_area_width(), 0, 0, 0)

    def update_line_number_area(self, rect, dy):
        if dy:
            self.line_number_area.scroll(0, dy)
        else:
            self.line_number_area.update(0, rect.y(), self.line_number_area.width(), rect.height())

        if rect.contains(self.viewport().rect()):
            self.update_line_number_area_width(0)

    def resizeEvent(self, event):
        super(IDECodeEditor, self).resizeEvent(event)
        content_rect = self.contentsRect()
        self.line_number_area.setGeometry(
            QtCore.QRect(content_rect.left(), content_rect.top(), self.line_number_area_width(), content_rect.height())
        )
        if getattr(self, 'search_replace_panel', None) and self.search_replace_panel.isVisible():
            self.search_replace_panel.show_panel()

    def line_number_area_paint_event(self, event):
        painter = QtGui.QPainter(self.line_number_area)
        painter.fillRect(event.rect(), QtGui.QColor(35, 35, 35))

        block = self.firstVisibleBlock()
        block_number = block.blockNumber()
        top = int(self.blockBoundingGeometry(block).translated(self.contentOffset()).top())
        bottom = top + int(self.blockBoundingRect(block).height())

        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                number = str(block_number + 1)
                painter.setPen(QtGui.QColor(120, 120, 120))
                painter.drawText(
                    0,
                    top,
                    self.line_number_area.width() - 4,
                    self.fontMetrics().height(),
                    QtCore.Qt.AlignRight,
                    number
                )

            block = block.next()
            top = bottom
            bottom = top + int(self.blockBoundingRect(block).height())
            block_number += 1

    def highlight_current_line(self):
        extra_selections = []
        if not self.isReadOnly():
            selection = QtWidgets.QTextEdit.ExtraSelection()
            selection.format.setBackground(QtGui.QColor(255, 255, 255, 15))
            selection.format.setProperty(QtGui.QTextFormat.FullWidthSelection, True)
            selection.cursor = self.textCursor()
            selection.cursor.clearSelection()
            extra_selections.append(selection)
        self.setExtraSelections(extra_selections)

    def set_language(self, language='python'):
        if getattr(self, 'highlighter', None):
            try:
                self.highlighter.setDocument(None)
            except Exception:
                pass

        if str(language).lower() == 'python':
            self.highlighter = PythonSyntaxHighlighter(self.document())
        else:
            self.highlighter = None
