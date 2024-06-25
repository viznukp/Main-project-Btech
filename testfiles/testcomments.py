from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton
from PyQt5.Qsci import QsciScintilla, QsciLexerPython
from PyQt5.QtCore import Qt

class CodeEditor(QsciScintilla):
    def __init__(self):
        super().__init__()
        self.setLexer(QsciLexerPython(self))
        font = self.font()
        font.setFamily('Courier')
        font.setFixedPitch(True)
        font.setPointSize(10)
        self.setFont(font)
        self.setAutoIndent(True)
        self.setMarginLineNumbers(1, True)
        self.setMarginWidth(1, '40')

    def comment_lines(self):
        comment(self, 1, 3)

    def uncomment_lines(self):
        uncomment(self, 1, 3)

    def add_line(self):
        add_new_line(self)

def add_new_line(editor):
    cursor_position = editor.getCursorPosition()
    line_index = cursor_position[0]
    line_position = cursor_position[1]

    # Get the current text
    current_text = editor.text()

    # Split the text into lines
    lines = current_text.split('\n')

    # Insert a new line below the current line
    new_line_index = line_index + 1
    lines.insert(new_line_index, '')

    # Join the lines back together
    new_text = '\n'.join(lines)

    # Set the modified text back to the editor
    editor.setText(new_text)

    # Set the cursor position to the beginning of the new line
    editor.setCursorPosition(new_line_index, 0)




def comment(editor, start_line, end_line, comment_symbol='#'):
    text = editor.text()
    lines = text.split('\n')
    
    # Ensure start_line and end_line are within bounds
    start_line = max(0, min(start_line, len(lines) - 1))
    end_line = max(0, min(end_line, len(lines) - 1))

    # Comment each line within the specified range
    for i in range(start_line-1, end_line):
        if lines[i].strip():  # Only comment non-empty lines
            lines[i] = comment_symbol + lines[i]
    text = '\n'.join(lines)
    editor.setText(text)

def uncomment(editor, start_line, end_line, comment_symbol='#'):
    text = editor.text()
    lines = text.split('\n')
    
    # Ensure start_line and end_line are within bounds
    start_line = max(0, min(start_line, len(lines) - 1))
    end_line = max(0, min(end_line, len(lines) - 1))

    # Uncomment each line within the specified range
    for i in range(start_line-1, end_line):
        if lines[i].strip().startswith(comment_symbol):  # Check if line starts with comment symbol
            lines[i] = lines[i][len(comment_symbol):]  # Remove comment symbol
    text = '\n'.join(lines)
    editor.setText(text)



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.editor = CodeEditor()
        self.editor.setText("Line 1\nLine 2\nLine 3\nLine 4\nLine 5")

        layout = QVBoxLayout()
        layout.addWidget(self.editor)

        button_comment = QPushButton("Comment")
        button_comment.clicked.connect(self.editor.comment_lines)
        layout.addWidget(button_comment)

        button_newline = QPushButton("newline")
        button_newline.clicked.connect(self.editor.add_line)
        layout.addWidget(button_newline)        

        button_uncomment = QPushButton("Uncomment")
        button_uncomment.clicked.connect(self.editor.uncomment_lines)
        layout.addWidget(button_uncomment)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
