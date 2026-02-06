"""
ScriptHandler.py
Helper class for running Python scripts as subprocesses.
For executing control system scripts.
"""

from pathlib import Path
import subprocess as sp

from PySide6.QtCore import Slot
from PySide6.QtCore import QObject, QUrl


class ScriptHandler(QObject):
    def __init__(self, pass_script_url:QUrl=None, fail_script_url:QUrl=None, parent=None):
        super().__init__(parent)

        if pass_script_url: self.pass_script = QUrl.toLocalFile(pass_script_url)
        else:               self.script = None

        if fail_script_url: self.fail_script = QUrl.toLocalFile(fail_script_url)
        else:               self.fail_script = None


    @Slot()
    def start_pass(self):
        try:
            print("> Executing pass script...")
        except:
            print("> Cannot execute pass script.")


    @Slot()
    def start_fail(self):
        try:
            print("> Executing fail script...")
        except:
            print("> Cannot execute fail script.")


    @Slot(QUrl)
    def update_pass_path(self, path):
        self.pass_script = QUrl.toLocalFile(path)

    @Slot(QUrl)
    def update_fail_path(self, path):
        self.fail_script = QUrl.toLocalFile(path)
