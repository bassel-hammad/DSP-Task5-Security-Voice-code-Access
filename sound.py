import sounddevice as sd
from scipy.io.wavfile import write
from threading import Thread
import time

class Sound:
    def __init__(self):
        self.recording = False
        self.filename = "recorded_audio.wav"

    def start_recording(self, duration=10):
        if not self.recording:
            self.recording = True
            self.record_thread = Thread(target=self._record_audio, args=(duration,))
            self.record_thread.start()

    def stop_recording(self):
        if self.recording:
            self.recording = False
            self.record_thread.join()  # Wait for the recording thread to finish

    def _record_audio(self, duration):
        samplerate = 44100

        recording = sd.rec(int(samplerate * duration), samplerate=samplerate, channels=2, dtype='int16')
        sd.wait()

        if self.recording:
            write(self.filename, recording, samplerate)
            print(f"Audio recorded and saved as {self.filename}")


