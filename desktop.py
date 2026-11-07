"""Run a standalone PySide6 window containing the GPS map widget."""
import sys

from PySide6.QtWidgets import QApplication, QMainWindow
from gps_widget import GPSWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('GPS Tracker — Desktop')
        self.resize(1000, 650)

        self.gps_tracker = GPSWidget()
        self.setCentralWidget(self.gps_tracker)

        # Example only; replace with live coordinates from your own source.
        # GPSWidget waits for the map to load before showing the marker.
        self.gps_tracker.update_location(8.9475, 125.5406)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
