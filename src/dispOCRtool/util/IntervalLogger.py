"""
IntervalLogger.py
Helper class for interval logging.
Uses QTimer.
Also serves as controller for text correct threads.
"""

import os, importlib
from pathlib import Path

from PySide6.QtCore import Slot
from PySide6.QtCore import QObject, QTimer, QUrl, QDateTime

import language_tool_python
from symspellpy import SymSpell
from ocr.TextCorrection import TextCorrector


class FileWriter(QObject):
    def __init__(self, folder_url=None, parent=None):
        super().__init__(parent)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.write_to_file)

        self.data = ""
        self.directory = QUrl.toLocalFile(folder_url)
        self.filename = ""
        self.file = None
        self.aborted = False

        self.lt = language_tool_python.LanguageTool("en-US")
        self.lt_threads = []

        self.sp = SymSpell(max_dictionary_edit_distance=3, prefix_length=7)
        self.dictionary_path = importlib.resources.files("symspellpy") / "frequency_dictionary_en_82_765.txt"
        self.bigram_path = importlib.resources.files("symspellpy") / "frequency_bigramdictionary_en_243_342.txt"

        self.sp.load_dictionary(self.dictionary_path, term_index=0, count_index=1)
        self.sp.load_bigram_dictionary(self.bigram_path, term_index=0, count_index=2)
        


    @Slot(int)
    def start(self, interval_ms):
        if not self.timer.isActive():
            print("\n> Logging started.")
            now = QDateTime.currentDateTime()
            now = now.toString("yyyyMMdd_HHmmss")
            self.filename = f"log_{now}.txt"
            self.file = open(Path(self.directory) / self.filename, "a")

            self.timer.start(interval_ms)

    @Slot(bool)
    def stop(self, enable_correction):
        print("> Stopping log...")
        self.timer.stop()
        self.file.close()
        if enable_correction:
            lt_thread = TextCorrector(
                dir=self.directory,
                filename=self.filename.rsplit('.', 1)[0],
                sp_instance=self.sp,
                lt_instance=self.lt
            )
            self.lt_threads.append(lt_thread)
            lt_thread.finished.connect(lambda: self.lt_threads.remove(lt_thread))
            lt_thread.start()
        print("> Logging stopped successfully.")

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

            self.file.write(f"{nowContents} - {self.data.strip()}\n")
            self.file.flush()

        if self.aborted:
            self.stop(False)

    @Slot()
    def stop_threads(self):
        for thread in self.lt_threads:
            thread.stop()

    @Slot()
    def abort(self):
        self.aborted = True
        self.stop_threads()
        self.lt.close()
