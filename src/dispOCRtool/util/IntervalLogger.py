"""
IntervalLogger.py
Helper class for interval logging.
"""

from pathlib import Path

from PySide6.QtCore import Slot
from PySide6.QtCore import QObject, QTimer, QUrl, QDateTime
import language_tool_python

from ocr.TextCorrection import TextCorrector


class FileWriter(QObject):
    def __init__(self, folder_url=None, parent=None):
        super().__init__(parent)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.write_to_file)

        self.data = ""
        self.directory = QUrl.toLocalFile(folder_url)
        self.filename = ""

        self.lt = language_tool_python.LanguageTool("en-US")
        self.lt_threads = []


    @Slot(int)
    def start(self, interval_ms):
        if not self.timer.isActive():
            print("> Logging started.")
            now = QDateTime.currentDateTime()
            now = now.toString("yyyyMMdd_HHmmss")
            self.filename = f"log_{now}.txt"

            self.timer.start(interval_ms)

    @Slot(bool)
    def stop(self, enable_correction):
        self.timer.stop()
        if enable_correction:
            lt_thread = TextCorrector(
                dir=self.directory,
                filename=self.filename.rsplit('.', 1)[0],
                lt_instance=self.lt
            )
            self.lt_threads.append(lt_thread)
            lt_thread.finished.connect(lambda: self.lt_threads.remove(lt_thread))
            lt_thread.start()

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
