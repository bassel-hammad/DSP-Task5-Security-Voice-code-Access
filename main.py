from PyQt5.QtWidgets import QApplication, QMainWindow
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import sounddevice as sd
from scipy.io.wavfile import write
from threading import Thread
from Task5Ui import Ui_MainWindow
import sys


class MyMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set up the UI
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

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
        self.spectrrogramLayout = self.ui.spectrogramLayout
        self.spectrrogramLayout.addWidget(self.canvas)

        # Add a Matplotlib subplot to the figure
        self.spectrrogram = self.fig.add_subplot(111)

        #Access Status Label
        self.recordingStatusLabel = self.ui.recordingStatusLabel

        #Connect buttons to functions
        self.ui.recordButton.clicked.connect(self.change_recording_status_label) #record button

    def change_recording_status_label(self):
        text = self.recordingStatusLabel.text()
        if text == "Start recording":
            self.recordingStatusLabel.setText("Stop recording")
            self.recordingStatusLabel.setStyleSheet("color: rgb(255, 0, 0);")
        else:
            self.recordingStatusLabel.setText("Start recording")
            self.recordingStatusLabel.setStyleSheet("color: rgb(0, 0, 0);")
        







if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MyMainWindow()
    main_window.show()
    sys.exit(app.exec_())
