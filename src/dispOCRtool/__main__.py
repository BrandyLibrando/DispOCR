import sys
from pathlib import Path
import random, time
import numpy as np
import cv2
from cv2_enumerate_cameras import enumerate_cameras

from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine
# import PySide6.QtMultimedia

from PySide6.QtGui import QImage
from PySide6.QtCore import Slot, Signal, Property
from PySide6.QtCore import QObject, QTimer, QUrl, QThread, QSysInfo
from PySide6.QtQuick import QQuickImageProvider, QQuickView

## Own Utility/Class Imports
from util.Bridge import ListBridge, StringBridge
# from util.NumpyQImageRenderer import NumpyImageProvider
from util.OpencvRenderer import OpencvImageProvider


if __name__ == "__main__":
    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()

    ##############################################
    ## PY-QML DATA BRIDGES
    ##############################################
    operating_system = QSysInfo.productType() if QSysInfo.productType() in ["windows", "macos", "unknown", "ios", "android"] else "linux"
    preferred_backend = cv2.CAP_DSHOW if operating_system == "windows" else cv2.CAP_GSTREAMER if operating_system == "linux" else cv2.CAP_AVFOUNDATION if "macos" else cv2.CAP_ANY
    camera_models = [cam.name for cam in enumerate_cameras(preferred_backend)]
    camera_index = [cam.index for cam in enumerate_cameras(preferred_backend)]

    bridge = StringBridge(operating_system)
    camera_list = ListBridge(camera_models)

    engine.rootContext().setContextProperty("bridge", bridge)
    engine.rootContext().setContextProperty("cameraList", camera_list)


    ##############################################
    ## CAMERA AND IMAGE RENDERING
    ##############################################
    # engine.rootContext().engine().addImageProvider("numpy", provider)  # to render numpy images to QML
    if (camera_models):
        cvCameraRenderer = OpencvImageProvider(cv2backend=preferred_backend)

        engine.rootContext().setContextProperty("cvCameraRenderer", cvCameraRenderer)  # to access provider ID in QML
        engine.addImageProvider("CvCameraFeed", cvCameraRenderer)  # expose provider to Image classes


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

    app.aboutToQuit.connect(cvCameraRenderer.killThread)

    sys.exit(app.exec())
