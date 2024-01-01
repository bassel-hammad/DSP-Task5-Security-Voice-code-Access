import numpy as np
import matplotlib.pyplot as plt
import scipy.io.wavfile as wav
from scipy.signal import spectrogram
from sklearn.metrics import mean_squared_error
from scipy.io.wavfile import write
import sounddevice as sd
import speech_recognition as sr
import functions as f

class SecuritySystem:
    def __init__(self):
        self.passcode_sentences = ["Open middle door", "Unlock the gate", "Grant me access"]
        self.users = ["User1", "User2", "User3", "User4", "User5", "User6", "User7", "User8"]
        self.access_mode = None
        self.selected_users = []

    def set_access_mode(self, mode):
        self.access_mode = mode

    def set_selected_users(self, users):
        self.selected_users = users

    def record_voice(self, duration=5, fs=44100, filename='recorded_voice.wav'):
        print("Recording...")
        voice_data = sd.rec(int(duration * fs), samplerate=fs, channels=2, dtype=np.int16)
        sd.wait()
        write(filename, voice_data, fs)
        print("Recording saved as", filename)

    def create_spectrogram(self, filename, fs=44100):
        _, data = wav.read(filename)
        f, t, Sxx = spectrogram(data, fs)
        plt.pcolormesh(t, f, 10 * np.log10(Sxx))
        plt.ylabel('Frequency [Hz]')
        plt.xlabel('Time [sec]')
        plt.show()

    def recognize_passcode(self, audio_filename):
        recognizer = sr.Recognizer()
        with sr.AudioFile(audio_filename) as source:
            audio_data = recognizer.record(source)
            try:
                recognized_text = recognizer.recognize_google(audio_data)
                print("Recognized text:", recognized_text)
                return recognized_text
            except sr.UnknownValueError:
                print("Could not understand audio")
                return None

    def match_passcode(self, recognized_text):
        for sentence in self.passcode_sentences:
            mse = mean_squared_error(np.array([ord(c) for c in sentence]), np.array([ord(c) for c in recognized_text]))
            print(f"MSE with '{sentence}': {mse}")
        return mse

    def match_user(self, audio_filename):
        # Implement user matching logic using fingerprint or other techniques
        pass

    def grant_access(self, mse_passcode, mse_user):
        if self.access_mode == 1 and mse_passcode < 100:
            print("Access granted based on passcode.")
            return True
        elif self.access_mode == 2 and any(mse_user < 100 for mse_user in mse_user):
            print("Access granted based on user fingerprint.")
            return True
        else:
            print("Access denied.")
            return False

# Example usage
security_system = SecuritySystem()

# Set access mode (1 for Security voice code, 2 for Security voice fingerprint)
security_system.set_access_mode(1)

# Set selected users (applicable only in Security voice fingerprint mode)
security_system.set_selected_users(["User1", "User2"])

# Record voice and save as 'recorded_voice.wav'
security_system.record_voice()

# Create spectrogram from the recorded voice
security_system.create_spectrogram('recorded_voice.wav')

# Recognize passcode from the recorded voice
recognized_text = security_system.recognize_passcode('recorded_voice.wav')

# Match passcode and user
mse_passcode = security_system.match_passcode(recognized_text)
mse_user = security_system.match_user('recorded_voice.wav')

# Grant access based on matching results
access_granted = security_system.grant_access(mse_passcode, mse_user)
