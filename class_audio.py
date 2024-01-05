import tkinter as tk
from tkinter import ttk
import librosa
import pyaudio
import numpy as np
from threading import Thread
import sounddevice as sd
from scipy.io.wavfile import write
import matplotlib.pyplot as plt

class audio:
    def __init__(self):
        self.is_recording = False
        self.filename = "recorded_audio.wav"
        self.sample_rate = 44100
        self.y_coordinates = []
        self.x_coordinates = []

    def record_audio(self, duration=3):
        if not self.is_recording:
            self.is_recording = True
            self.y_coordinates = []  # Reset previous data
            self.x_coordinates = []  # Reset previous data
            # Record audio
            audio_data = sd.rec(int(duration * self.sample_rate), samplerate=self.sample_rate, channels=1, dtype=np.int16)
            sd.wait()
            # Convert audio_data to a flat array and append to y_coordinates
            self.y_coordinates.extend(audio_data.flatten())
            # Create corresponding time values and append to x_coordinates
            self.x_coordinates.extend(np.arange(len(audio_data.flatten())) / self.sample_rate)
        else:
            self.is_recording = False
            self.save_audio()

    def plot_spectrogram(self):
        plt.figure()
        plt.specgram(np.array(self.y_coordinates), Fs=self.sample_rate, cmap='viridis', aspect='auto')
        plt.xlabel('Time (s)')
        plt.ylabel('Frequency (Hz)')
        plt.title('Spectrogram')
        plt.show()

    def save_audio(self):
        write(self.filename, self.sample_rate, np.array(self.y_coordinates))
        print("Audio saved")



