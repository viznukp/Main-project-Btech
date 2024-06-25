import tkinter as tk
import subprocess
import os

class ConsoleApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Terminal Console")
        self.current_directory = "E:/"  # Set initial directory to E:/

        self.create_widgets()

    def create_widgets(self):
        self.console_output = tk.Text(self.root, wrap=tk.WORD, height=20, width=80)
        self.console_output.pack(expand=True, fill=tk.BOTH)

        self.command_entry = tk.Entry(self.root, width=60)
        self.command_entry.pack(side=tk.LEFT, padx=(5, 0), pady=5, expand=True, fill=tk.X)
        self.command_entry.bind("<Return>", self.execute_command)

        self.execute_button = tk.Button(self.root, text="Execute", command=self.execute_command)
        self.execute_button.pack(side=tk.LEFT, padx=(5, 0), pady=5)

    def execute_command(self, event=None):
        command = self.command_entry.get()
        if command:
            # Handle "cd" command
            if command.startswith("cd "):
                directory = command.split(" ", 1)[1]
                self.change_directory(directory)
            else:
                process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, cwd=self.current_directory)
                output, error = process.communicate()
                if output:
                    self.console_output.insert(tk.END, output.decode())
                if error:
                    self.console_output.insert(tk.END, error.decode())
                self.console_output.insert(tk.END, '\n')
                self.console_output.see(tk.END)  # Scroll to the end of the text

            self.command_entry.delete(0, tk.END)  # Clear the entry field

    def change_directory(self, directory):
        # Change directory and update current_directory
        new_directory = os.path.join(self.current_directory, directory)
        if os.path.isdir(new_directory):
            self.current_directory = new_directory
            self.console_output.insert(tk.END, f"\nChanged directory to: {self.current_directory}\n")
        else:
            self.console_output.insert(tk.END, f"\nDirectory '{directory}' not found\n")
        self.console_output.see(tk.END)  # Scroll to the end of the text

def main():
    root = tk.Tk()
    app = ConsoleApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
