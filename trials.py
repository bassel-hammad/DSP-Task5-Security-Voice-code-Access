import tkinter as tk
from tkinter import ttk
import librosa
import pyaudio
import numpy as np
from threading import Thread
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import sounddevice as sd
from scipy.io.wavfile import write
import matplotlib.pyplot as plt

# Replace this with your actual dataset and labels
audio_files = ["grant.wav","grant1.wav","grant2.wav","grant3.wav", "light_close.wav", "light_close2.wav","light_close1.wav", "light_close3.wav"]
labels = ["grant", "grant","grant","grant", "light_close", "light_close", "light_close", "light_close"]

# Define a fixed size for the features
fixed_size = (13, 87)  # Adjust the size as needed

# Feature extraction (MFCCs)
def extract_features(audio):
    mfccs = librosa.feature.mfcc(y=audio, sr=44100, n_mfcc=fixed_size[0])

    # Pad or truncate the features to the fixed size
    if mfccs.shape[1] < fixed_size[1]:
        mfccs = np.pad(mfccs, ((0, 0), (0, fixed_size[1] - mfccs.shape[1])), mode='constant')
    else:
        mfccs = mfccs[:, :fixed_size[1]]

    return mfccs

# Create a dataset of features and corresponding labels
X = [extract_features(librosa.load(file, sr=None)[0]) for file in audio_files]
y = labels

# Split the dataset into training and testing sets
X_train, _, y_train, _ = train_test_split(X, y, test_size=0.1, random_state=42)

# Create a flat version of the features for training
X_train_flat = np.array([spec.flatten() for spec in X_train])

class SpeechRecognitionUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Speech Recognition UI")

        self.create_ui()

        self.paudio = pyaudio.PyAudio()
        self.audio_stream = None
        self.recording = False

    def create_ui(self):
        self.label = ttk.Label(self.master, text="Live Speech Recognition:")
        self.label.grid(row=0, column=0, padx=10, pady=10)

        self.start_button = ttk.Button(self.master, text="Start Recording", command=self.start_recording)
        self.start_button.grid(row=1, column=0, padx=10, pady=10)

        self.stop_button = ttk.Button(self.master, text="Stop Recording", command=self.stop_recording, state=tk.DISABLED)
        self.stop_button.grid(row=1, column=1, padx=10, pady=10)

        self.result_label = ttk.Label(self.master, text="Recognition Result:")
        self.result_label.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

    def _process_audio(self):
        # Read audio data from file using librosa
        audio_data, _ = librosa.load(self.filename, sr=None)

        # Extract features from the audio data
        features = extract_features(audio_data).flatten().reshape(1, -1)

        # Assume X_train_flat and y_train are already defined
        classifier = RandomForestClassifier(n_estimators=100, random_state=42)
        classifier.fit(X_train_flat, y_train)

        # Make prediction
        prediction = classifier.predict(features)
        print("Prediction:", prediction)  # Add this line for debugging
        # Update the result label
        self.result_label.config(text=f"Recognition Result: {prediction[0]}")

    def __del__(self):
        if self.paudio:
            self.paudio.terminate()

def main():
    root = tk.Tk()
    app = SpeechRecognitionUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
