"""
OpencvRenderer.py
Contains classes for handling QML threaded camera handling
using OpenCV and QThreads.
"""

import cv2
import numpy as np
import numpy.typing as nptype

from PySide6.QtGui import QImage
from PySide6.QtCore import Slot, Signal
from PySide6.QtCore import QThread
from PySide6.QtQuick import QQuickImageProvider

from util.CroppedImageRenderer import CroppedImageProvider


class OpencvImageProvider(QQuickImageProvider):
    imageChanged = Signal(QImage)
    cameraOpened = Signal(int, int)

    def __init__(self, index=0, cv2backend=cv2.CAP_ANY):
        super(OpencvImageProvider, self).__init__(QQuickImageProvider.Image)
        self.roi_renderer = CroppedImageProvider()

        self.api = cv2backend
        self.index = index
        self.cam = None

        self.image = None
        self.cropped_image = None
        self.width = 0
        self.height = 0


    def requestImage(self, id, size, requestedSize):
        if self.image:
            img = self.image
        else:
            img = QImage(640, 480, QImage.Format_RGBA8888)
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
        self.cam.openedCamera.connect(self.setDimensions)
        self.cam.start()

    @Slot()
    def killThread(self):
        print("Finishing current camera thread...")
        self.cam.stop()

    @Slot()
    def updateImage(self, img, roi_img=None):
        self.image = img
        self.cropped_image = roi_img
        # frame = np.array(np_img, dtype=np.uint8)
        # self.cropped_image = frame[self.y1:self.y2, self.x1:self.x2]
        self.roi_renderer.setCroppedImage(roi_img)

        self.imageChanged.emit(img)
        # self.imageChanged.emit(img, cropped_qimage)

    def setDimensions(self, width, height):
        self.width = width
        self.height = height
        self.cameraOpened.emit(width, height)
        self.cam.setRoiCoordinates(0, int(width/2), 0, int(height/2))

    @Slot()
    def getWidth(self):
        return self.cam.width

    @Slot()
    def getHeight(self):
        return self.cam.height

    def getRoiRenderer(self):
        return self.roi_renderer



class ThreadCamera(QThread):
    updateFrame = Signal(QImage, QImage)
    openedCamera = Signal(int, int)

    def __init__(self, index, apiPreference=cv2.CAP_ANY, parent=None):
        QThread.__init__(self, parent)

        self.cap = cv2.VideoCapture(index, apiPreference)
        self.width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        self.image = None
        self.roi_image = None
        self._running = True

        self.x1 = 0
        self.x2 = self.width
        self.y1 = 0
        self.y2 = self.height

    def run(self):
        self.openedCamera.emit(self.width, self.height)

        while self._running:
            if self.cap.isOpened:
                ret, frame = self.cap.read()
                if not ret:
                    break

                try:
                    if self._running and ret:
                        roi_frame = frame[self.y1:self.y2, self.x1:self.x2].copy()
                    else:
                        roi_frame = cv2.cvtColor(np.zeros((300, 300), dtype=np.uint8), cv2.COLOR_GRAY2BGR)
                        frame = cv2.cvtColor(np.zeros((300, 300), dtype=np.uint8), cv2.COLOR_GRAY2BGR)
                except:
                    self._running = False
                    break

                img = QImage(frame.data, frame.shape[1], frame.shape[0], QImage.Format_BGR888)
                roi_img = QImage(roi_frame.data, roi_frame.shape[1], roi_frame.shape[0], QImage.Format_BGR888)
                self.image = frame
                self.roi_image = roi_frame
                self.updateFrame.emit(img, roi_img)  # signal reload to Image class within QML

    def stop(self):
        self.cap.release()
        self._running = False
        self.requestInterruption()
        self.wait()
        print("Thread ended successfully.")

    @Slot()
    def setRoiCoordinates(self, x1, x2, y1, y2):
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2

