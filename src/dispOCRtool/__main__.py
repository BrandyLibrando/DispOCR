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
from PySide6.QtCore import QObject, QTimer, QUrl, QThread, QPermission, QCameraPermission
from PySide6.QtQuick import QQuickImageProvider, QQuickView

## Own Utility/Class Imports
from .util.Bridge import StringBridge
from .util.NumpyQImageRenderer import NumpyImageProvider




class ThreadCamera(QThread):
    updateFrame = Signal(QImage)

    def __init__(self, parent=None):
        QThread.__init__(self, parent)

    def run(self):
        self.cap = cv2.VideoCapture(0)
        while self.cap.isOpened():
            ret, frame = self.cap.read()
            if not ret:
                img = QImage("./images/network.png")
                self.updateFrame.emit(img)
            color_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = QImage(color_frame.data, color_frame.shape[1], color_frame.shape[0], QImage.Format_RGB888)
            self.updateFrame.emit(img)


class ImageProvider(QQuickImageProvider):
    imageChanged = Signal(QImage)

    def __init__(self):
        super(ImageProvider, self).__init__(QQuickImageProvider.Image)

        self.cam = ThreadCamera()
        self.cam.updateFrame.connect(self.update_image)
        self.image = None

    def requestImage(self, id, size, requestedSize):
        if self.image:
            img = self.image
        else:
            img = QImage(600, 500, QImage.Format_RGBA8888)
            img.fill("#4CAF50")

        return img


    @Slot()
    def update_image(self, img):
        self.imageChanged.emit(img)
        self.image = img

    @Slot()
    def start(self):
        print("Starting...")
        self.cam.start()

    @Slot()
    def killThread(self):
        print("Finishing...")
        try:
            self.cam.cap.release()
        except:
            pass


if __name__ == "__main__":
    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()



    ##############################################
    ## PY-QML INTEG
    ##############################################
    bridge = StringBridge()

    ## Expose Python object to QML
    # engine.rootContext().engine().addImageProvider("numpy", provider)
    myImageProvider = ImageProvider()

    engine.rootContext().setContextProperty("bridge", bridge)
    engine.rootContext().setContextProperty("myImageProvider", myImageProvider)

    engine.addImageProvider("MyImageProvider", myImageProvider)


    ##############################################
    ## LOADING OF QML FILE FOR APP
    ##############################################
    # qml_file = Path(__file__).resolve().parent / "tester.qml"
    qml_file = Path(__file__).resolve().parent / "main.qml"

    engine.load(qml_file)

    if not engine.rootObjects():
        sys.exit(-1)

    sys.exit(app.exec())
