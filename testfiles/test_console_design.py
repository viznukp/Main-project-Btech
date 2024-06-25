import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt5.Qsci import QsciScintilla, QsciLexerPython
from PyQt5.QtGui import QFont, QColor


class ConsoleWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Console")
        self.setGeometry(100, 100, 800, 600)

        self.editor = QsciScintilla()
        self.editor.setLexer(QsciLexerPython(self.editor))
        font = QFont()
        font.setFamily('Courier')
        font.setPointSize(10)
        self.editor.setFont(font)
        self.editor.setMarginsFont(self.editor.font())
        self.editor.setMarginWidth(0, 0)
        self.editor.setMarginLineNumbers(1, True)
        self.editor.setUtf8(True)
        self.editor.setWrapMode(QsciScintilla.WrapWord)
        self.editor.setEolMode(QsciScintilla.EolUnix)
        self.editor.setWrapVisualFlags(QsciScintilla.WrapFlagByText)
        self.editor.setIndentationsUseTabs(False)
        self.editor.setAutoIndent(True)
        self.editor.setBraceMatching(QsciScintilla.SloppyBraceMatch)
        self.editor.setCaretLineVisible(True)
        caret_line_color = QColor("lightgrey")
        self.editor.setCaretLineBackgroundColor(caret_line_color)

        layout = QVBoxLayout()
        layout.addWidget(self.editor)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.write_prompt()

    def write_prompt(self):
        self.editor.append('\n>')
        self.editor.setCursorPosition(self.editor.lines(), 0)
        self.editor.ensureCursorVisible()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ConsoleWindow()
    window.show()
    sys.exit(app.exec_())
