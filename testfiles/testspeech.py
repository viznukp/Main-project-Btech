import sys
import queue
import threading
import speech_recognition as sr
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QTextEdit
from PyQt5.QtCore import QObject, pyqtSignal

# Global variables for threading
audio_queue = queue.Queue()
exit_event = threading.Event()

# Function to detect silence
def is_silent(data, threshold):
    rms = audioop.rms(data, 2)  # Calculate root mean square (RMS) of the audio data
    return rms < threshold

# Function to handle transcription
def transcribe_audio(result_display):
    r = sr.Recognizer()

    while not exit_event.is_set():
        try:
            audio_data = audio_queue.get(timeout=0.1)  # Wait for audio data with a timeout
            text = r.recognize_google(audio_data)
            result_display.append(text)  # Append text to the QTextEdit
        except queue.Empty:
            continue
        except sr.UnknownValueError:
            result_display.append("Could not understand audio")
        except sr.RequestError as e:
            result_display.append("Could not request results; {0}".format(e))

# Function to record audio and put it into the queue
def record_audio():
    r = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening...")

        # Adjust ambient noise for better recognition
        r.adjust_for_ambient_noise(source)

        while not exit_event.is_set():
            audio_data = r.listen(source)
            audio_queue.put(audio_data)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.editor = QTextEdit()
        self.result_display = QTextEdit()
        self.record_button = QPushButton('Record Speech')

        self.record_button.clicked.connect(self.toggleRecording)

        layout.addWidget(self.editor)
        layout.addWidget(self.record_button)
        layout.addWidget(self.result_display)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.setWindowTitle('Speech Recognition')
        self.setGeometry(100, 100, 800, 600)

        # Initialize transcription thread
        self.transcription_thread = threading.Thread(target=transcribe_audio, args=(self.result_display,))
        self.transcription_thread.start()

        # Initialize recording thread
        self.recording_thread = threading.Thread(target=record_audio)
        self.recording_thread.start()

    def toggleRecording(self):
        if self.record_button.text() == 'Record Speech':
            self.record_button.setText('Stop Recording')
            exit_event.clear()  # Clear exit event to continue recording
        else:
            self.record_button.setText('Record Speech')
            exit_event.set()  # Set exit event to stop recording

    def closeEvent(self, event):
        # Ensure threads are stopped when closing the window
        exit_event.set()  # Set exit event to stop recording
        self.transcription_thread.join()
        self.recording_thread.join()
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
