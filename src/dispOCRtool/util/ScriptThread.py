"""
ScriptThread.py
Thread worker for running scripts.
Inherits from QThread.
"""

import os
import subprocess as sp

from PySide6.QtCore import QThread, Signal


class ScriptThread(QThread):
    finished = Signal()

    def __init__(self, file, passing:bool, parent=None):
        QThread.__init__(self, parent)
        self.file = file
        self.is_pass = passing
        self.prompt = "pass" if passing else "fail"


    def run(self):
        if not os.path.isfile(self.file):
            print(f"> File for {self.prompt} script not found. \n  Have you selected an exsting Python script file?")
            self.finished_signal.emit()
            return

        try:
            print(f"Condition {self.prompt}ed. Executing {self.prompt} script...")
            self.process = sp.Popen(["python", self.file])
        except:
            print(f"Cannot execute {self.prompt} script properly.")
        finally:
            self.process.wait()
            self.finished.emit()
            return


    def stop(self):
        self.process.terminate()
        self.wait()
        print("> Script aborted successfully.")
