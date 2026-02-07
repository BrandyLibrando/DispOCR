"""
TextCorrection.py
Contains text correct logic using the
language-tool-python library.
"""

from pathlib import Path

# from PySide6.QtCore import QElapsedTimer          # Reimport elapsed timer module if profiling needed
from PySide6.QtCore import QThread
import language_tool_python
from language_tool_python.utils import correct


class TextCorrector(QThread):
    def __init__(self, dir, filename, lt_instance=None, parent=None):
        QThread.__init__(self, parent)

        self.out_dir = dir
        self.filename = filename
        self.lt = lt_instance if lt_instance is not None else language_tool_python.LanguageTool("en-US")

        # self.timer = QElapsedTimer()  # For performance measure
        self.aborted = False


    def run(self):
        src_path = Path(self.out_dir) / (self.filename + ".txt")
        dst_path = Path(self.out_dir) / (self.filename + "_corrected.txt")

        if not src_path.exists():
            print(f"{self.filename}.txt does not exist.")

        else:
            print("> Starting a new text correction thread...")
            # self.timer.start()
            with open(src_path, "r", encoding="utf-8") as src_file:
                lines = src_file.readlines()

            with open(dst_path, "w", encoding="utf-8") as dst_file:
                for line in lines:
                    if self.aborted:
                        dst_file.write("===== Correction of original file aborted. =====")
                        return

                    if line.strip():
                        matches = self.lt.check(line)
                        line = correct(line, matches)

                    dst_file.write(line)
                    # print(self.timer.restart())

        print("> Text correct thread finished successfully.")

    def stop(self):
        self.aborted = True
        self.wait()
        print("> Text correct thread aborted successfully.")
