from PyQt5.QtWidgets import *

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt5.QtGui import QFont
from PyQt5.Qsci import QsciScintilla, QsciLexerPython

from PyQt5.QtCore import Qt, QEvent, QTimer

from input_handler import *
from ide_functions import *
# from speech_to_text import *

class CodeEditor(QsciScintilla):
    def __init__(self):
        super().__init__()
        self.setLexer(QsciLexerPython(self))
        font = QFont()
        font.setFamily('Courier')
        font.setFixedPitch(True)
        font.setPointSize(12)
        self.setFont(font)
        self.lexer().setFont(font)
        self.setAutoIndent(True)
        self.setMarginLineNumbers(1, True)
        self.setMarginWidth(1, '40')
        self.language = "python"
        self.current_file_name = ""
        self.current_file_location = ""
        self.initial_text = ""
    
    def check_changes_in_editor_content(self):
        current_text = self.text()
        if current_text != self.initial_text:
            # print("Changes have been made.")
            self.initial_text = current_text
            return True
        else:
            return False
            # print("No changes have been made.")
    # def add_text_at_line(self, line_number, text):
    #     print(line_number)
    #     # Ensure line_number is valid
    #     if line_number < 1:
    #         line_number = 1

    #     # Convert line_number to zero-based index
    #     line_index = line_number - 1
    #     self.insertAt(text, line_index, 0)

    def add_text_cursor(self, text, isClear = False):
        if isClear:
            self.clear()
        self.insert(text)

class MainWindow(QMainWindow):
    def __init__(self, input_handler):
        super().__init__()
        self.input_handler = input_handler
        self.setWindowTitle('AI Assisted Editor')
        self.setGeometry(100, 100, 1500, 800)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Layout for the central widget
        main_layout = QHBoxLayout()
        central_widget.setLayout(main_layout)

         # Add menu bar
        self.menu_bar = QMenuBar()
        self.setMenuBar(self.menu_bar)

        # Add menus to the menu bar
        file_menu = self.menu_bar.addMenu('File')
        edit_menu = self.menu_bar.addMenu('Edit')

        # Left column
        left_column = QWidget()
        left_layout = QVBoxLayout()
        left_column.setLayout(left_layout)


        splitter = QSplitter() #for resizable split
        splitter.setOrientation(Qt.Vertical)

        # Editor window
        self.editor = CodeEditor()
        splitter.addWidget(self.editor)

        # console
        self.console = QsciScintilla()        
        splitter.addWidget(self.console)

        splitter.setSizes([700, 300]) # size ratio
        left_layout.addWidget(splitter)

        # Install event filter for the editor and console
        self.editor.installEventFilter(self)
        self.console.installEventFilter(self)

        # Set indentation width (e.g., set it to 4 spaces)
        self.editor.setIndentationWidth(4)

        # Timer approach: Check for changes every 1 second
        # self.timer = QTimer(self)
        # self.timer.timeout.connect(self.editor.check_changes_in_editor_content)
        # self.timer.start(2000)  # Interval is in milliseconds

        # Add actions to the file menu
        new_action = QAction('New', self)
        file_menu.addAction(new_action)

        open_action = QAction('Open', self)
        file_menu.addAction(open_action)

        save_action = QAction('Save', self)
        save_action.triggered.connect(self.save_editor_content)
        file_menu.addAction(save_action)


        # Right column
        right_column = QWidget()
        right_layout = QVBoxLayout()
        right_column.setLayout(right_layout)

        right_column.setFixedWidth(600)

        # Top row of the right column
        top_row = QWidget()
        top_layout = QVBoxLayout()
        top_row.setLayout(top_layout)
        top_row.setStyleSheet("background-color: lightgrey;")
        top_row.setFixedHeight(500)
        right_layout.addWidget(top_row)

        # Scroll area for chat
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        top_layout.addWidget(self.scroll_area)

        # Chat area
        self.chat_area = QWidget()
        self.chat_area.setFixedWidth(500)
        chat_layout = QVBoxLayout()
        self.chat_area.setLayout(chat_layout)
        self.scroll_area.setWidget(self.chat_area)

        self.add_message("Welcome! Type or ask something to start the conversation.", is_from_user=False)

        # Bottom row of the right column
        bottom_row = QWidget()
        bottom_layout = QVBoxLayout()
        bottom_row.setLayout(bottom_layout)
        right_layout.addWidget(bottom_row)
        
        self.label_input_state = QLabel('Type something:')
        bottom_layout.addWidget(self.label_input_state)

        self.text_input = QTextEdit()
        bottom_layout.addWidget(self.text_input)

        submit_button = QPushButton('Submit')
        submit_button.clicked.connect(self.send_message)
        bottom_layout.addWidget(submit_button)

        self.speak_button = QPushButton('Speak')
        self.speak_button.clicked.connect(self.record_speech)
        bottom_layout.addWidget(self.speak_button)

        self.is_recording = False

        # Add the left and right columns to the main layout
        main_layout.addWidget(left_column)
        main_layout.addWidget(right_column)

    def add_message(self, text, is_from_user=True):
        message_widget = ChatBubble(text, is_from_user)
        self.chat_area.layout().addWidget(message_widget)

        # Scroll to bottom
        scroll_bar = self.scroll_area.verticalScrollBar()
        scroll_bar.setValue(scroll_bar.maximum())

    def send_message(self):
        text = self.text_input.toPlainText().strip()
        if text:
            if self.editor.check_changes_in_editor_content() == True:
                #update content in gpt
                print("\n\n\n\nUpdating content in gpt\n\n\n")
                current_code = self.editor.text()
                current_code = "updated state of code: \"" + current_code + "\""
                response = self.input_handler.ask_gpt(current_code)
                response_str = str(response)
                self.add_message(response_str, is_from_user=False)

            self.add_message(text, is_from_user=True)
            response = self.input_handler.ask_gpt(text)
            # For demonstration purposes, adding a bot response
            # response = evaluate_gpt_response(self.editor,text)
            response_str = str(response)
            self.add_message(response_str, is_from_user=False)
            # self.response_eval(response)
            evaluate_gpt_response(self.editor, self.console, response)
            self.text_input.clear()

    def record_speech(self):
        self.is_recording = not self.is_recording
        
        if self.is_recording:
            self.label_input_state.setText( "Listening..")
            self.speak_button.setText("Stop recording..")
            self.input_handler.recorder.listen()
        else:
            self.label_input_state.setText( "Type your query")
            self.speak_button.setText("Speak")
            
            self.input_handler.recorder.stop()


    # def response_eval(self, dict):
    #     command_type = dict['command']

    #     if(command_type == "code"):
    #         if 'content' in dict:
    #             content = dict['content']
    #             self.editor.add_text_cursor(content)
    #     if(command_type == "select_ln"):
    #         start_line = dict['start_line']
    #         end_line = dict['end_line']
    #         self.editor.setSelection(start_line, end_line)

    def save_editor_content(self):
        save_file(self.editor)
    
    def eventFilter(self, obj, event):
        if obj == self.editor and event.type() == QEvent.KeyPress:
            return self.handleEditorKeyPressEvent(event)
            
        if obj == self.console and event.type() == QEvent.KeyPress:
            return self.handleConsoleKeyPressEvent(event)

        return super().eventFilter(obj, event)
        

    def handleEditorKeyPressEvent(self, event):
        if event.modifiers() == Qt.ControlModifier and event.key() == Qt.Key_S:
            # Handle Ctrl + S to save file
            save_file(self.editor)
            return True  # Event handled

        return False  # Event not handled


    def handleConsoleKeyPressEvent(self, event):
        if event.modifiers() == Qt.ControlModifier and event.key() == Qt.Key_L:
            # Handle Ctrl + L to clear the console
            self.console.clear()
            return True  # Event handled

        if event.key() in (Qt.Key_Return, Qt.Key_Enter):
            # Get the text from the current line
            line_number, _ = self.console.getCursorPosition()
            text = self.console.text(line_number)

            result = process_command(text)

            # Move cursor to the next line
            self.console.SendScintilla(QsciScintilla.SCI_NEWLINE)
            
            self.console.insert(result.stdout)
            self.console.insert(result.stderr)

            # Move cursor to the end of the last line
            self.console.SendScintilla(QsciScintilla.SCI_DOCUMENTEND)

            # Create a new line
            self.console.SendScintilla(QsciScintilla.SCI_NEWLINE)

            # Return True to indicate that the event has been handled
            return True

        return False  # Event not handled


class ChatBubble(QFrame):
    def __init__(self, text, is_from_user):
        super().__init__()
        self.setObjectName("chat-bubble")
        self.init_ui(text, is_from_user)

    def init_ui(self, text, is_from_user):
        layout = QVBoxLayout()
        self.setLayout(layout)

        message_label = QLabel(text)
        message_label.setWordWrap(True)
        layout.addWidget(message_label)

        if is_from_user:
            message_label.setStyleSheet("""
                                    background-color: #DCF8C6;
                                    border-radius: 5px;
                                    border-top-right-radius: 0px;
                                    padding : 5px;
                                    margin-left : 20px
                                    """)
        else:
            message_label.setStyleSheet("""
                                    background-color: #cb7af0;
                                    border-radius: 5px;
                                    border-top-left-radius: 0px;
                                    padding : 5px;
                                    margin-right : 20px
                                    """)


class Editor:
    def init(self, inputHandler):
        self.app = QApplication(sys.argv)
        self.window = MainWindow(inputHandler)
        self.window.show()
        sys.exit(self.app.exec_())    

# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     window = MainWindow()
#     window.show()
#     sys.exit(app.exec_())
