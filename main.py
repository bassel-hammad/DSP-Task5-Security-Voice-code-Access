from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem
from PyQt5.QtCore import QTimer
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import sounddevice as sd
import numpy as np
import librosa
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from scipy.io.wavfile import write
from threading import Thread
from Task5Ui import Ui_MainWindow
from class_audio import audio
import sys
from Users_Dictionary import users


class MyMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set up the UI
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Create an instance of the audio class
        self.audio = audio()

        self.Mode=0 #0 for speech recognition, 1 for voice recognition

        #modeComboBox setup
        self.modeComboBox = self.ui.modeComboBox


        # Audio files and labels
        #if bta3t current index
        #
        # #else: bta3tha current index
        # self.audio_files = ["grant_me_access_bassel_1.wav", "grant_me_access_bassel_2.wav", "grant_me_access_bassel_3.wav", "grant_me_access_bassel_4.wav", "grant_me_access_bassel_5.wav","open_middle_door_bassel_1.wav","open_middle_door_bassel_2.wav","open_middle_door_bassel_3.wav","open_middle_door_bassel_4.wav","open_middle_door_bassel_5.wav","unlock_the_gate_bassel_1.wav","unlock_the_gate_bassel_2.wav","unlock_the_gate_bassel_3.wav","unlock_the_gate_bassel_4.wav","unlock_the_gate_bassel_5.wav"]
        # self.labels = ["grant_bassel", "grant_bassel","grant_bassel","grant_bassel","grant_bassel","open_bassel","open_bassel","open_bassel","open_bassel","open_bassel","unlock_bassel","unlock_bassel","unlock_bassel","unlock_bassel","unlock_bassel"]

        # Define a fixed size for the features
        self.fixed_size = (13, 87)  # Adjust the size as needed

        # Create a dataset of features and corresponding labels
        self.X = [self.extract_features(librosa.load(file, sr=None)[0]) for file in self.audio_files]
        self.y = self.labels

        # Split the dataset into training and testing sets
        self.X_train, _,self.y_train, _ = train_test_split(self.X,self.y, test_size=0.1, random_state=42)

        # Create a flat version of the features for training
        self.X_train_flat = np.array([spec.flatten() for spec in self.X_train])

        #sentenceTable setup
        self.sentenceTable = self.ui.sentenceTable
        self.sentenceTable.setColumnCount(3)
        self.sentenceTable.setRowCount(1)
        self.sentenceTable.setHorizontalHeaderLabels(["Open middle door", "Unlock the gate", "Grant me access"])
        self.sentenceTable.setVerticalHeaderLabels([""])
        self.sentenceTable.resizeColumnsToContents()
        self.sentenceTable.resizeRowsToContents()
        
        #IndividualsTable setup
        self.individualsTable = self.ui.individualTable
        self.individualsTable.setColumnCount(3)
        self.individualsTable.setRowCount(8)
        self.individualsTable.setHorizontalHeaderLabels(["Open middle door", "Unlock the gate", "Grant me access"])
        self.individualsTable.setVerticalHeaderLabels(["Bassel", "Omar", "Zeyad", "Mahmoud", "Abdelrahman", "indv 6", "indv 7", "indv 8"])
        self.individualsTable.resizeColumnsToContents()
        self.individualsTable.resizeRowsToContents()

        # Create a Matplotlib figure and canvas
        self.fig = Figure()
        self.canvas = FigureCanvas(self.fig)
        self.spectrogramLayout = self.ui.spectrogramLayout
        self.spectrogramLayout.addWidget(self.canvas)

        # Add a Matplotlib subplot to the figure
        self.spectrogram = self.fig.add_subplot(111)

        #Access Status Label
        self.recordingStatusLabel = self.ui.recordingStatusLabel

        #Connect buttons to functions
        self.ui.recordButton.clicked.connect(self.change_recording_status_label) #record button
         

        #Connect modeComboBox to function
        self.modeComboBox.currentIndexChanged.connect(self.change_mode)


    def change_mode(self):
        self.Mode=self.modeComboBox.currentIndex()

    def change_recording_status_label(self):
        text = self.recordingStatusLabel.text()
        if text == "Start recording":
            self.recordingStatusLabel.setText("Stop recording")
            self.recordingStatusLabel.setStyleSheet("color: rgb(255, 0, 0);")
            QApplication.processEvents()  # Force GUI update
            self.create_audio()
            # Use QTimer to reset the label after 3000 milliseconds (3 seconds)
            QTimer.singleShot(0, self.reset_label)
        else:
            return

    def reset_label(self):
        # Reset the label to its original state
        self.recordingStatusLabel.setText("Start recording")
        self.recordingStatusLabel.setStyleSheet("color: rgb(0, 0, 0);")
        QApplication.processEvents()  # Force GUI update
                    
    def create_audio(self):
        self.audio.record_audio()
        self.plot_spectrogram()
        self.process_audio()

    def plot_spectrogram(self):
        self.fig.clear()
        self.spectrogram = self.fig.add_subplot(111)
        self.spectrogram.specgram(np.array(self.audio.y_coordinates), Fs=self.audio.sample_rate, cmap='viridis', aspect='auto')
        self.spectrogram.set_xlabel('Time (s)')
        self.spectrogram.set_ylabel('Frequency (Hz)')
        self.spectrogram.set_title('Spectrogram')
        self.canvas.draw()

    # Feature extraction (MFCCs)
    def extract_features(self,audioData):
        mfccs = librosa.feature.mfcc(y=audioData, sr=44100, n_mfcc=self.fixed_size[0])

        # Pad or truncate the features to the fixed size
        if mfccs.shape[1] < self.fixed_size[1]:
            mfccs = np.pad(mfccs, ((0, 0), (0, self.fixed_size[1] - mfccs.shape[1])), mode='constant')
        else:
            mfccs = mfccs[:, :self.fixed_size[1]]

        return mfccs
    
    def process_audio(self):
        # Read audio data from file using librosa
        audio_data, _ = librosa.load(self.audio.filename, sr=None)

        # Extract features from the audio data
        features =self.extract_features(audio_data).flatten().reshape(1, -1)

        # Assume X_train_flat and y_train are already defined
        classifier = RandomForestClassifier(n_estimators=100, random_state=42)
        classifier.fit(self.X_train_flat,self.y_train)
        # Get probability estimates for each class
        proba_estimates = classifier.predict_proba(features)
        # Make prediction
        prediction = classifier.predict(features)
        #hena if bta3t current_index=1
        print("Prediction:", prediction)  # Add this line for debugging
        # Print the probability estimates
        print("Probability Estimates:", proba_estimates)

    #mode speech recognition
        # Set a threshold for probability estimates
        threshold = 0.45
        # Check if the maximum probability for any class is below the threshold
        if np.max(proba_estimates) < threshold:
            print("Access Denied: Low Confidence")
            self.ui.accessStatusLabel.setText("Access Denied")
            self.sentenceTable.setItem(0, 0, QTableWidgetItem(f"per={proba_estimates[0][1]*100}%"))
            self.sentenceTable.setItem(0, 1, QTableWidgetItem(f"per={proba_estimates[0][2]*100}%"))
            self.sentenceTable.setItem(0, 2, QTableWidgetItem(f"per={proba_estimates[0][0]*100}%"))
        else:
            # Update the result label
            print(f"Recognition Result: {prediction[0]}")
            self.ui.accessStatusLabel.setText("Access Granted")
            self.sentenceTable.setItem(0, 0, QTableWidgetItem(f"per={proba_estimates[0][1]*100}%"))
            self.sentenceTable.setItem(0, 1, QTableWidgetItem(f"per={proba_estimates[0][2]*100}%"))
            self.sentenceTable.setItem(0, 2, QTableWidgetItem(f"per={proba_estimates[0][0]*100}%"))
        #else bta3t current index

#mode voice recognition        
        # Update the result label
        print(f"Recognition Result: {prediction[0]}")
        self.ui.accessStatusLabel.setText("Access Granted")
        #bassel sentences
        self.individualsTable.setItem(0, 0, QTableWidgetItem(f"per={proba_estimates[0][1]*100}%"))
        self.individualsTable.setItem(0, 1, QTableWidgetItem(f"per={proba_estimates[0][2]*100}%"))
        self.individualsTable.setItem(0, 2, QTableWidgetItem(f"per={proba_estimates[0][0]*100}%"))
        

    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MyMainWindow()
    main_window.show()
    sys.exit(app.exec_())
