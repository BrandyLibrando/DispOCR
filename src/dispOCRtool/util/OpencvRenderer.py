"""
OpencvRenderer.py
Contains classes for handling QML threaded camera handling
using OpenCV and QThreads.
"""

import cv2
import numpy as np

from PySide6.QtGui import QImage
from PySide6.QtCore import Slot, Signal
from PySide6.QtCore import QThread
from PySide6.QtQuick import QQuickImageProvider


class ThreadCamera(QThread):
    updateFrame = Signal(QImage)

    def __init__(self, index, apiPreference=cv2.CAP_ANY, parent=None):
        QThread.__init__(self, parent)

        self.cap = cv2.VideoCapture(index, apiPreference)
        self.width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        self.image = None
        self._running = True

    def run(self):
        while self._running:
            if self.cap.isOpened:
                ret, frame = self.cap.read()
                if not ret:
                    break

                try:
                    if self._running and ret: color_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    else: color_frame = cv2.cvtColor(np.zeros((300, 300), dtype=np.uint8), cv2.COLOR_GRAY2BGR)
                except:
                    self._running = False
                    break

                img = QImage(color_frame.data, color_frame.shape[1], color_frame.shape[0], QImage.Format_RGB888)
                self.image = color_frame  # color_frame can be stored for later processing
                self.updateFrame.emit(img)  # signal reload to Image class within QML

    def stop(self):
        self.cap.release()
        self._running = False
        self.requestInterruption()
        self.wait()
        print("Thread ended successfully.")


class OpencvImageProvider(QQuickImageProvider):
    imageChanged = Signal(QImage)

    def __init__(self, index=0, cv2backend=cv2.CAP_ANY):
        super(OpencvImageProvider, self).__init__(QQuickImageProvider.Image)

        self.api = cv2backend
        self.index = index
        self.cam = None
        self.image = None


    def requestImage(self, id, size, requestedSize):
        if self.image:
            img = self.image
        else:
            img = QImage(600, 500, QImage.Format_RGBA8888)
            img.fill("#00BCD4")

        return img

    @Slot(int)
    def change_camera(self, index):
        self.killThread()
        self.index = index

        self.start()

    @Slot()
    def start(self):
        print("")
        print("=====================\nStarting new camera thread...")
        self.cam = ThreadCamera(self.index, self.api)
        self.cam.updateFrame.connect(self.updateImage)
        self.cam.start()

    @Slot()
    def killThread(self):
        print("Finishing current camera thread...")
        self.cam.stop()

    @Slot()
    def updateImage(self, img):
        self.imageChanged.emit(img)
        self.image = img

    @Slot()
    def getWidth(self):
        return self.cam.width

    @Slot()
    def getHeight(self):
        return self.cam.height

