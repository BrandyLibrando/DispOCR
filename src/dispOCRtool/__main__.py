import sys
from pathlib import Path
import random, time
import numpy as np
import cv2

from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine
# import PySide6.QtMultimedia

from PySide6.QtGui import QImage
from PySide6.QtCore import Slot, Signal, Property
from PySide6.QtCore import QObject, QTimer, QUrl, QThread, QSysInfo
from PySide6.QtQuick import QQuickImageProvider, QQuickView

## Own Utility/Class Imports
from util.Bridge import StringBridge
# from util.NumpyQImageRenderer import NumpyImageProvider
from util.OpencvRenderer import OpencvImageProvider
        

if __name__ == "__main__":
    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()

    ##############################################
    ## PY-QML DATA BRIDGES
    ##############################################
    operating_system = QSysInfo.productType() if QSysInfo.productType() in ["windows", "macos", "unknown", "ios", "android"] else "linux"
    print(operating_system)
    bridge = StringBridge(operating_system)
    engine.rootContext().setContextProperty("bridge", bridge)


    ##############################################
    ## CAMERA AND IMAGE RENDERING
    ##############################################
    # engine.rootContext().engine().addImageProvider("numpy", provider)  # to render numpy images to QML
    myImageProvider = OpencvImageProvider()

    engine.rootContext().setContextProperty("myImageProvider", myImageProvider)  # to access provider ID in QML
    engine.addImageProvider("MyImageProvider", myImageProvider)  # expose provider to Image classes


    ##############################################
    ## LOADING OF QML FILE FOR APP
    ##############################################
    # qml_file = Path(__file__).resolve().parent / "tester.qml"
    qml_file = Path(__file__).resolve().parent / "main.qml"

    engine.load(qml_file)

    if not engine.rootObjects():
        sys.exit(-1)

    window = engine.rootObjects()[0]  # Store root window
    # window.closing.connect(myImageProvider.killThread())
    app.aboutToQuit.connect(myImageProvider.killThread)

    sys.exit(app.exec())
