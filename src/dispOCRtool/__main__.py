"""
THS_DispOCR
Authored by: Julius Librando
In fulfillment of thesis requirement along with
Seungkwan Bang, Harish Chawla, and Aidan Albert Narvaez.
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

from PySide6.QtGui import QImage
from PySide6.QtCore import QCoreApplication, Slot, Signal, Property
from PySide6.QtCore import QObject, QTimer, QUrl, QThread, QSysInfo, QStandardPaths
from PySide6.QtQuick import QQuickImageProvider, QQuickView

## Own Utility/Class Imports
from app.settings import AppSettings
from util.IntervalLogger import FileWriter
from util.Bridge import ListBridge, StringBridge
from util.OpencvRenderer import OpencvImageProvider


if __name__ == "__main__":
    QCoreApplication.setOrganizationName("BrandyLibrando")
    QCoreApplication.setApplicationName("DispOCR")
    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()

    ## SETTINGS
    settings = AppSettings()
    engine.rootContext().setContextProperty("appSettings", settings)


    ## PY-QML DATA BRIDGES
    # Enumerate webcams (with opencv and cv2_enumerate)
    operating_system = QSysInfo.productType() if QSysInfo.productType() in ["windows", "macos", "unknown", "ios", "android"] else "linux"
    preferred_backend = cv2.CAP_DSHOW if operating_system == "windows" else cv2.CAP_V4L2 if operating_system == "linux" else cv2.CAP_AVFOUNDATION if "macos" else cv2.CAP_ANY
    camera_models = [cam.name for cam in enumerate_cameras(preferred_backend)]
    camera_index = [cam.index for cam in enumerate_cameras(preferred_backend)]

    # Enumerate DepthAI cameras (mainly for OAK)
    dai_models = dai.DeviceBootloader.getAllAvailableDevices()
    dai_names = []
    print(dai_models)

    for idx, device in enumerate(dai.Device.getAllAvailableDevices()):
        print(f"{device.getDeviceId()} {device.state}")
        # dai_names.append(f"[D{idx}] ({device.getDeviceId()})")

    print(camera_models + dai_names)

    # Data bridges
    camera_list = ListBridge(camera_models + dai_names)
    dai_configs = ListBridge([16500, 800, 128])  # Defaults for [exposure, ISO, focus]

    engine.rootContext().setContextProperty("cameraList", camera_list)
    engine.rootContext().setContextProperty("cvCamCount", len(camera_models))
    engine.rootContext().setContextProperty("daiCamCount", len(dai_names))
    engine.rootContext().setContextProperty("daiConfig", dai_configs)


    ## HELPERS
    # Logger timer
    logger = FileWriter(settings.getSaveDir())
    engine.rootContext().setContextProperty("fileLogger", logger)

    # Camera initialization and image rendering
    # engine.rootContext().engine().addImageProvider("numpy", provider)  # to render numpy images to QML
    if camera_models:
        cvCameraRenderer = OpencvImageProvider( cv2backend=preferred_backend, daiSupport=len(dai_names), daiInit=(not len(camera_models) and len(dai_names)) )
        cvRoiRenderer = cvCameraRenderer.getRoiRenderer()

        engine.rootContext().setContextProperty("cvCameraRenderer", cvCameraRenderer)  # cv base img provider
        engine.addImageProvider("CvCameraFeed", cvCameraRenderer)
        engine.rootContext().setContextProperty("cvRoiRenderer", cvRoiRenderer)  # cv roi img provider
        engine.addImageProvider("CvRoiFeed", cvRoiRenderer)


    ## LOADING OF QML FILE FOR APP
    qml_file = Path(__file__).resolve().parent / "qml/main.qml"
    engine.load(qml_file)

    if not engine.rootObjects():
        sys.exit(-1)


    ## EXIT CLEANUP
    def cleanup_on_exit():
        print("\n>> Exiting...")

        # Exit camera and OCR threads
        cvCameraRenderer.killThread()
        cvCameraRenderer.destroyOcrThread()

        # Safely close file (no text correction applied)
        logger.abort()
        while logger.timer.isActive():
            app.processEvents()

    # window = engine.rootObjects()[0]  # Store root window
    # window.closing.connect(myImageProvider.killThread())
    # app.aboutToQuit.connect(cvCameraRenderer.killThread)
    # app.aboutToQuit.connect(cvCameraRenderer.destroyOcrThread)
    app.aboutToQuit.connect(cleanup_on_exit)

    sys.exit(app.exec())
