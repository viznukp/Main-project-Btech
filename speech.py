import threading
import queue
import speech_recognition as sr
import audioop
import sys
import os

class SpeechRecognizer:
    def __init__(self):
        self.audio_queue = queue.Queue()
        self.exit_event = threading.Event()
        self.transcription_thread = None

    def is_silent(self, data, threshold):
        rms = audioop.rms(data, 2)
        return rms < threshold

    def transcribe_audio(self):
        r = sr.Recognizer()

        while not self.exit_event.is_set():
            try:
                audio_data = self.audio_queue.get(timeout=0.1)
                text = r.recognize_google(audio_data)
                print("Recognized:", text)
            except queue.Empty:
                continue
            except sr.UnknownValueError:
                print("Could not understand audio")
            except sr.RequestError as e:
                print("Could not request results; {0}".format(e))
        
        # Wait for enter key press before stopping
        input("Press Enter to stop recording...")
        print("Stopped recording")
        self.stop()

    def record_audio(self):
        r = sr.Recognizer()

        with sr.Microphone() as source:
            print("Listening...")
            r.adjust_for_ambient_noise(source)

            while not self.exit_event.is_set():
                audio_data = r.listen(source)
                self.audio_queue.put(audio_data)

    def listen(self):
        if self.transcription_thread is None or not self.transcription_thread.is_alive():
            self.transcription_thread = threading.Thread(target=self.transcribe_audio)
            self.transcription_thread.start()
            # Start thread to monitor the enter key press
            self.enter_key_thread = threading.Thread(target=self.monitor_enter_key)
            self.enter_key_thread.start()

    def stop(self):
        self.exit_event.set()
        if self.transcription_thread and self.transcription_thread.is_alive():
            self.transcription_thread.join()
            self.transcription_thread = None

    def monitor_enter_key(self):
        input("Press Enter to stop recording...")
        print("Stopped recording")
        self.stop()
        os._exit(0)  # Exit the program completely

if __name__ == "__main__":
    recognizer = SpeechRecognizer()
    recognizer.listen()
