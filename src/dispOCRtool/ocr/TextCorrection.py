"""
IntervalLogger.py
Helper class for interval logging.
"""

from pathlib import Path

from PySide6.QtCore import Slot
from PySide6.QtCore import QObject, QThread, QUrl, QElapsedTimer
import language_tool_python


class TextCorrector(QThread):
    def __init__(self, dir, filename, lt_instance=None, parent=None):
        QThread.__init__(self, parent)

        self.out_dir = dir
        self.filename = filename
        self.lt = lt_instance if lt_instance is not None else language_tool_python.LanguageTool("en-US")

        self.timer = QElapsedTimer()  # For performance measure


    def run(self):
        src_path = Path(self.out_dir) / (self.filename + ".txt")
        dst_path = Path(self.out_dir) / (self.filename + "_corrected.txt")

        self.timer.start()
        with open(src_path, "r", encoding="utf-8") as src_file:
            lines = src_file.readlines()

        with open(dst_path, "w", encoding="utf-8") as dst_file:
            for line in lines:
                if line.strip():
                    matches = self.lt.check(line)
                    line = self.lt.utils.correct(line, matches)

                dst_file.write(line)
                print(self.timer.restart())
