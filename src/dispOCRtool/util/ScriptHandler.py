"""
ScriptHandler.py
Helper class for running Python scripts as subprocesses.
For executing control system scripts.
"""

from PySide6.QtCore import Slot
from PySide6.QtCore import QObject, QUrl

from util.ScriptThread import ScriptThread


class ScriptHandler(QObject):
    def __init__(self, pass_script_url:QUrl=None, fail_script_url:QUrl=None, parent=None):
        super().__init__(parent)

        self.pass_script = QUrl.toLocalFile(pass_script_url) if pass_script_url else None
        self.fail_script = QUrl.toLocalFile(fail_script_url) if fail_script_url else None

        self.__threads = []


    def execute(self, file, is_pass):
        thread = ScriptThread(file, is_pass)
        self.__threads.append(thread)
        thread.finished.connect(lambda: self.__threads.remove(thread))
        thread.start()


    @Slot()
    def start_pass(self):
        self.execute(self.pass_script, True)

    @Slot()
    def start_fail(self):
        self.execute(self.fail_script, False)

    @Slot()
    def end_all_threads(self, file):
        for th in self.__threads:
            th.stop()
            th.wait()


    @Slot(QUrl)
    def update_pass_path(self, path):
        self.pass_script = QUrl.toLocalFile(path)

    @Slot(QUrl)
    def update_fail_path(self, path):
        self.fail_script = QUrl.toLocalFile(path)
