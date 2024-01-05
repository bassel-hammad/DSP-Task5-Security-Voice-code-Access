from PyQt5.QtWidgets import QApplication, QMainWindow
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write
from threading import Thread
from Task5Ui import Ui_MainWindow
from class_audio import audio
import sys


class MyMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set up the UI
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Create an instance of the audio class
        self.audio = audio()

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
        #self.ui.recordButton.clicked.connect(self.create_audio) #record button 

    def change_recording_status_label(self):
        text = self.recordingStatusLabel.text()
        if text == "Start recording":
            self.recordingStatusLabel.setText("Stop recording")
            self.recordingStatusLabel.setStyleSheet("color: rgb(255, 0, 0);")
            QApplication.processEvents()  # Force GUI update
            self.create_audio()

        else:
            self.recordingStatusLabel.setText("Start recording")
            self.recordingStatusLabel.setStyleSheet("color: rgb(0, 0, 0);")
            QApplication.processEvents()  # Force GUI update
            self.create_audio()
        
    def create_audio(self):
        self.audio.record_audio()
        self.plot_spectrogram()

    def plot_spectrogram(self):
        self.fig.clear()
        self.spectrogram = self.fig.add_subplot(111)
        self.spectrogram.specgram(np.array(self.audio.y_coordinates), Fs=self.audio.sample_rate, cmap='viridis', aspect='auto')
        self.spectrogram.set_xlabel('Time (s)')
        self.spectrogram.set_ylabel('Frequency (Hz)')
        self.spectrogram.set_title('Spectrogram')
        self.canvas.draw()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MyMainWindow()
    main_window.show()
    sys.exit(app.exec_())
