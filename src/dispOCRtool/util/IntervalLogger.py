"""
IntervalLogger.py
Helper class for interval logging.
"""

from pathlib import Path

from PySide6.QtCore import Slot
from PySide6.QtCore import QObject, QTimer, QUrl, QDateTime

class FileWriter(QObject):
    def __init__(self, folder_url=None, parent=None):
        super().__init__(parent)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.write_to_file)

        self.data = ""
        self.directory = QUrl.toLocalFile(folder_url)
        self.filename = ""

    @Slot(int)
    def start(self, interval_ms):
        if not self.timer.isActive():
            print("> Logging started.")
            now = QDateTime.currentDateTime()
            now = now.toString("yyyyMMdd_HHmmss")
            self.filename = f"log_{now}.txt"

            self.timer.start(interval_ms)

    @Slot()
    def stop(self):
        self.timer.stop()

    @Slot(QUrl)
    def update_dir(self, dir):
        self.directory = QUrl.toLocalFile(dir)

    @Slot(str)
    def update_data(self, data):
        self.data = data

    def write_to_file(self):
        if self.data.strip():
            now = QDateTime.currentDateTime()
            nowContents = now.toString("[yyyy-MM-dd HH:mm:ss.zzz]")

            with open(Path(self.directory) / self.filename, "a") as file:
                file.write(f"{nowContents} - {self.data}\n")
