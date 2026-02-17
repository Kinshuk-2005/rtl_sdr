import sys
import numpy as np
from PyQt5 import QtCore, QtWidgets
import pyqtgraph as pg
from rtlsdr import RtlSdr
import time

# --- Settings ---
TARGET_FREQ = 433.92e6 # Change the frequency as per your need (make sure entered frequency is within rtl-sdr range)
SAMPLE_RATE = 2.048e6
GAIN = 20
WINDOW_SIZE = 10  # Seconds to show on screen

class SDRMonitor(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Initialize SDR
        self.sdr = RtlSdr()
        self.sdr.sample_rate = SAMPLE_RATE
        self.sdr.center_freq = TARGET_FREQ
        self.sdr.gain = GAIN
        
        # UI Setup
        self.win = pg.GraphicsLayoutWidget(title="SDR Power Monitor")
        self.setCentralWidget(self.win)
        self.plot = self.win.addPlot(title=f"Power at {TARGET_FREQ/1e6} MHz")
        self.curve = self.plot.plot(pen='r')
        self.plot.setYRange(-60, 0)
        self.plot.setLabel('left', 'Relative Power', units='dB')
        self.plot.setLabel('bottom', 'Time', units='s')
        
        self.x_data = []
        self.y_data = []
        self.start_time = time.time()
        
        # High-speed timer (50ms interval = 20 updates per second)
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(50)

    def update(self):
        # Read samples and calculate power
        samples = self.sdr.read_samples(1024*16)
        power_db = 10 * np.log10(np.var(samples) + 1e-12) # Add small epsilon to avoid log(0)
        
        curr_time = time.time() - self.start_time
        self.x_data.append(curr_time)
        self.y_data.append(power_db)
        
        # Sliding Window Logic
        if curr_time > WINDOW_SIZE:
            # Set domain to [curr_time - 10, curr_time]
            self.plot.setXRange(curr_time - WINDOW_SIZE, curr_time, padding=0)
            
            # Memory Management: Prune data older than the window
            # Optional: Keeps only double the window size to ensure smooth rendering
            if len(self.x_data) > 1000:
                self.x_data = self.x_data[-500:]
                self.y_data = self.y_data[-500:]

        self.curve.setData(self.x_data, self.y_data)

    def closeEvent(self, event):
        self.sdr.close()
        event.accept()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = SDRMonitor()
    window.show()
    sys.exit(app.exec_())
