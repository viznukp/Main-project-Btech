from PyQt5.QtWidgets import QApplication, QFileDialog
from PyQt5.QtGui import QTextCursor
from PyQt5.Qsci import QsciScintilla

import subprocess

def make_dictionary_from_string(text):
    #remove unwanted white space
    pairs = text.replace(" ", "").split(",")

    # Initialize an empty dictionary to store the key-value pairs
    result_dictionary = {}

    # Iterate through the key-value pairs
    for pair in pairs:
        # Split each pair into key and value
        key, value = pair.split(":")

        # Convert value to integer if possible
        if value.isdigit():
            value = int(value)

        # Store key-value pair in the dictionary
        result_dictionary[key] = value

    return result_dictionary


def evaluate_gpt_response(editor, console,  text):
        
        # gpt_response = make_dictionary_from_string(text) # when testing from the command prompt
        gpt_response = text # when using gpt query
        command_type = gpt_response['command']

        if(command_type == "code"):
            if 'content' in gpt_response:
                content = gpt_response['content']
                editor.add_text_cursor(content, True)

        # if(command_type == "select_ln"):
        if(command_type == "select_line"):
            start_line = process_line_number(editor, gpt_response['start_line'])
            end_line = process_line_number(editor, gpt_response['end_line'])
            editor.setSelection(start_line - 1,0, end_line,0)

        if(command_type == "copy"):
            selected_text = editor.selectedText()
            # Copy the selected text to the clipboard
            QApplication.clipboard().setText(selected_text)

        if(command_type == "paste"):
            # Get the text from the clipboard
            clipboard_text = QApplication.clipboard().text()
            # Insert the text from the clipboard at the current cursor position
            editor.paste()
        
        if(command_type == "save"):
            if 'filename' in gpt_response:
                if gpt_response['filename'] != "" and gpt_response['filename'] != "none":
                    filename = gpt_response['filename']
                    editor.current_file_name = filename
            else:
                filename, _ = QFileDialog.getSaveFileName(None, 'Save File')
            if filename:
                with open(filename, 'w') as f:
                    content = editor.text()
                    f.write(content)
                    editor.current_file_name = filename
        
        if(command_type == "cut"):
            editor.cut()

        if(command_type == "goto"):
            if 'line_number' in gpt_response:
                line_number = gpt_response['line_number']
                editor.setCursorPosition(line_number - 1, 0)
            if 'position' in gpt_response:
                if gpt_response['position'] == 'end':
                    # Move the cursor to the end of the current line
                    line_number, _ = editor.getCursorPosition()
                    text = editor.text(line_number).strip() 
                    editor.setCursorPosition(line_number, len(text))

                if gpt_response['position'] == 'start':
                    line_number, _ = editor.getCursorPosition()
                    editor.setCursorPosition(line_number, 0)
            
            editor.setFocus()
            # command:goto, line_number:2, position:end

        if(command_type == "run"):
            result = run_code(editor.current_file_name, editor.language, editor.current_file_location)
            # Move cursor to the end of the last line
            console.SendScintilla(QsciScintilla.SCI_DOCUMENTEND)

            # Create a new line
            console.SendScintilla(QsciScintilla.SCI_NEWLINE)
            console.insert(result.stdout)
            console.insert(result.stderr)

        
        if(command_type == "debug"):
            pass

        if(command_type == "new_line"):
            add_new_line(editor)
        
        if(command_type == "scroll"):
            if 'direction' in gpt_response:
                move_cursor(editor, gpt_response['direction'])
        
        if(command_type == "delete"):
            pass

        if(command_type == "undo"):
            editor.undo()

        if(command_type == "redo"):
            editor.redo()
        


#function to process commands from console
def process_command(command):
    result = subprocess.run(['cmd.exe', '/c', command], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return result

def run_code(filename, language, location = ''):
    if(language == 'python'):
        command = 'python '+ location + filename  #+'.py'
        print(command)
    return subprocess.run(['cmd.exe', '/c', command], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

def save_file(editor, filename= ""):
    file_path, _ = QFileDialog.getSaveFileName(None, "Save File", filename, "Text Files (*.txt);;All Files (*)")
    if file_path:
        # Get the text content from the editor
        text_content = editor.text()
        # Write the content to the selected file
        with open(file_path, 'w') as file:
            file.write(text_content)

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

def move_cursor(editor, direction, lines=10):
    current_line = editor.SendScintilla(editor.SCI_LINEFROMPOSITION, editor.SendScintilla(editor.SCI_GETCURRENTPOS))
    if direction == "up":
        new_line = max(0, current_line - lines)
    elif direction == "down":
        new_line = min(editor.lines() - 1, current_line + lines)
    else:
        return  # Invalid direction

    editor.SendScintilla(editor.SCI_GOTOLINE, new_line)
    editor.setFocus()

def process_line_number(editor, line_number):
    line_base = 1
    line_max = editor.lines()

    if line_number == 'END':
        return line_max
    else:
        line_number = int(line_number)
        if line_number == 0:
            cursor_position = editor.getCursorPosition()
            return cursor_position[0] + 1
        line_number = min(line_max, max(line_base, line_number))
        return line_number

