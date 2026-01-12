"""
__main__.py
Opens the main app for the GUI, and handles
connections between Python backend and the QML components.
"""

import sys, os
from pathlib import Path
import random, time
import numpy as np
import cv2
import depthai as dai
from cv2_enumerate_cameras import enumerate_cameras

from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine
# import PySide6.QtMultimedia

from PySide6.QtGui import QImage
from PySide6.QtCore import Slot, Signal, Property
from PySide6.QtCore import QObject, QTimer, QUrl, QThread, QSysInfo, QStandardPaths
from PySide6.QtQuick import QQuickImageProvider, QQuickView

## Own Utility/Class Imports
from util.Bridge import ListBridge, StringBridge
# from util.NumpyQImageRenderer import NumpyImageProvider
from util.OpencvRenderer import OpencvImageProvider


if __name__ == "__main__":
    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()


    ## PY-QML DATA BRIDGES
    # Enumerate webcams (with opencv and cv2_enumerate)
    operating_system = QSysInfo.productType() if QSysInfo.productType() in ["windows", "macos", "unknown", "ios", "android"] else "linux"
    preferred_backend = cv2.CAP_DSHOW if operating_system == "windows" else cv2.CAP_GSTREAMER if operating_system == "linux" else cv2.CAP_AVFOUNDATION if "macos" else cv2.CAP_ANY
    camera_models = [cam.name for cam in enumerate_cameras(preferred_backend)]
    camera_index = [cam.index for cam in enumerate_cameras(preferred_backend)]

    # Enumerate DepthAI cameras (mainly for OAK)
    dai_models = dai.DeviceBootloader.getAllAvailableDevices()
    dai_names = []
    print(dai_models)

    for idx, info in enumerate(dai_models):
        with dai.Device(dai.Pipeline(), info) as device:
            calib = device.readCalibration()
            eeprom = calib.getEepromData()
            dai_names.append(f"[D{idx}] {eeprom.productName} ({info.deviceId})")

    print(camera_models + dai_names)

    # Data bridges
    initial_directory = QUrl.fromLocalFile(QStandardPaths.writableLocation(QStandardPaths.StandardLocation.HomeLocation))
    log_directory = StringBridge(initial_directory.toString())
    camera_list = ListBridge(camera_models + dai_names)
    dai_configs = ListBridge([16500, 800, 128])  # Defaults for [exposure, ISO, focus]

    engine.rootContext().setContextProperty("logDirectory", log_directory)
    engine.rootContext().setContextProperty("cameraList", camera_list)
    engine.rootContext().setContextProperty("cvCamCount", len(camera_models))
    engine.rootContext().setContextProperty("daiCamCount", len(dai_names))
    engine.rootContext().setContextProperty("daiConfig", dai_configs)


    ## CAMERA AND IMAGE RENDERING
    # engine.rootContext().engine().addImageProvider("numpy", provider)  # to render numpy images to QML
    if camera_models:
        cvCameraRenderer = OpencvImageProvider( cv2backend=preferred_backend, daiSupport=len(dai_names), dai=(not len(camera_models) and len(dai_names)) )
        cvRoiRenderer = cvCameraRenderer.getRoiRenderer()

        engine.rootContext().setContextProperty("cvCameraRenderer", cvCameraRenderer)  # cv base img provider
        engine.addImageProvider("CvCameraFeed", cvCameraRenderer)
        engine.rootContext().setContextProperty("cvRoiRenderer", cvRoiRenderer)  # cv roi img provider
        engine.addImageProvider("CvRoiFeed", cvRoiRenderer)


    ## LOADING OF QML FILE FOR APP
    # qml_file = Path(__file__).resolve().parent / "tester.qml"
    qml_file = Path(__file__).resolve().parent / "main.qml"
    engine.load(qml_file)


    if not engine.rootObjects():
        sys.exit(-1)

    # window = engine.rootObjects()[0]  # Store root window
    # window.closing.connect(myImageProvider.killThread())
    app.aboutToQuit.connect(cvCameraRenderer.killThread)

    sys.exit(app.exec())
