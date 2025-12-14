# This Python file uses the following encoding: utf-8
import sys
from pathlib import Path

# import PySide6.QtMultimedia
from PySide6.QtGui import QGuiApplication, QImage
from PySide6.QtQml import QQmlApplicationEngine, QmlElement
from PySide6.QtCore import QObject, Slot

## TODO: FOR QML-PY INTEG
# QML_IMPORT_NAME = "io.qt.textproperties"
# QML_IMPORT_MAJOR_VERSION = 1

# @QmlElement
# class Bridge(QObject):
#     @Slot(QImage)
#     def capture(self, preview):
#         # process placeholder
#         print(type(preview))


if __name__ == "__main__":
    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()

    # qml_file = Path(__file__).resolve().parent / "tester.qml"
    qml_file = Path(__file__).resolve().parent / "main.qml"
    engine.load(qml_file)

    if not engine.rootObjects():
        sys.exit(-1)

    sys.exit(app.exec())
