"""
THS_DispOCR
Authored by: Julius Librando
In fulfillment of BS Computer Engineering thesis requirement along with
Seungkwan Bang, Harish Chawla, and Aidan Albert Narvaez.
"""

import sys
from pathlib import Path

import cv2
import depthai as dai
from cv2_enumerate_cameras import enumerate_cameras

from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtCore import QCoreApplication, QSysInfo

from app.settings import AppConfigs
from util.IntervalLogger import FileWriter
from util.ScriptHandler import ScriptHandler
from util.Bridge import ListBridge
from util.OpencvRenderer import OpencvImageProvider


if __name__ == "__main__":
    QCoreApplication.setOrganizationName("BrandyLibrando")
    QCoreApplication.setApplicationName("DispOCR")
    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()

    ## SETTINGS AND SCRIPT HANDLER
    settings = AppConfigs
    settings.verifyPaths()
    engine.rootContext().setContextProperty("appSettings", settings)

    scriptHandler = ScriptHandler(settings.getScriptPath(), settings.getScriptPathAlt())
    engine.rootContext().setContextProperty("scriptHandler", scriptHandler)


    ## PY-QML DATA BRIDGES
    # Enumerate webcams (with opencv and cv2_enumerate)
    operating_system = QSysInfo.productType() if QSysInfo.productType() in ["windows", "macos", "unknown", "ios", "android"] else "linux"
    preferred_backend = cv2.CAP_DSHOW if operating_system == "windows" else cv2.CAP_V4L2 if operating_system == "linux" else cv2.CAP_AVFOUNDATION if "macos" else cv2.CAP_ANY
    camera_models = [cam.name for cam in enumerate_cameras(preferred_backend)]
    camera_index = [cam.index for cam in enumerate_cameras(preferred_backend)]

    # Enumerate DepthAI cameras (mainly for OAK)
    dai_models = dai.DeviceBootloader.getAllAvailableDevices()
    dai_names = []
    print("Dai: ", dai_models)

    for idx, device in enumerate(dai.Device.getAllAvailableDevices()):
        print(f"{device.getDeviceId()} {device.state}")
        dai_names.append(f"[D{idx}] ({device.getDeviceId()})")

    print("All: ", camera_models + dai_names)

    # Data bridges
    camera_list = ListBridge(camera_models + dai_names)

    # Camera initialization and image rendering
    if camera_list.size():
        ## HELPERS
        # Camera lists
        engine.rootContext().setContextProperty("cameraList", camera_list)
        engine.rootContext().setContextProperty("cvCamCount", len(camera_models))
        engine.rootContext().setContextProperty("daiCamCount", len(dai_names))

        # Logger class
        logger = FileWriter(settings.getSaveDir())
        engine.rootContext().setContextProperty("fileLogger", logger)

        # Image providers
        cvCameraRenderer = OpencvImageProvider( cv2backend=preferred_backend, daiInit=(not len(camera_models) and len(dai_names)) )
        cvRoiRenderer = cvCameraRenderer.getRoiRenderer()

        engine.rootContext().setContextProperty("cvCameraRenderer", cvCameraRenderer)  # cv base img provider
        engine.addImageProvider("CvCameraFeed", cvCameraRenderer)
        engine.rootContext().setContextProperty("cvRoiRenderer", cvRoiRenderer)  # cv roi img provider
        engine.addImageProvider("CvRoiFeed", cvRoiRenderer)

        ## LOADING OF QML FILE FOR APP
        qml_file = Path(__file__).resolve().parent / "qml/main.qml"
        engine.load(qml_file)

    else:
        print("No cameras detected.\nPlease make sure a camera is properly connected.")
        sys.exit(0)


    ## EXIT CLEANUP
    def cleanup_on_exit():
        print("\n>> Exiting...")

        # Exit camera and OCR threads
        cvCameraRenderer.killThread()
        cvCameraRenderer.destroyOcrThread()

        # Terminate all user script threads
        scriptHandler.end_all_threads()

        # Safely close log files when interrupted (no text correction applied)
        logger.abort()
        while logger.timer.isActive():
            app.processEvents()


    if not engine.rootObjects():
        sys.exit(-1)

    app.aboutToQuit.connect(cleanup_on_exit)
    sys.exit(app.exec())
