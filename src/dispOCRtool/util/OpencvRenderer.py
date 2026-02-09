"""
OpencvRenderer.py
Contains QQuickImageProvider class for
handling Dai/Cv camera threads and OCR thread.
"""

import cv2

from PySide6.QtGui import QImage
from PySide6.QtCore import Slot, Signal
from PySide6.QtCore import QTimer
from PySide6.QtQuick import QQuickImageProvider

from util.CroppedImageRenderer import CroppedImageProvider
from util.CameraThreads import ThreadCvCamera, ThreadDaiCamera
from ocr.ModelPaddleBase import ThreadOcrBase


class OpencvImageProvider(QQuickImageProvider):
    imageChanged = Signal(QImage)
    cameraOpened = Signal(int, int)
    predictionChanged = Signal(str, float)
    fpsCamChanged = Signal(float)
    fpsOcrChanged = Signal(float)

    def __init__(self, index=0, cv2backend=cv2.CAP_ANY, daiInit=False):
        super(OpencvImageProvider, self).__init__(QQuickImageProvider.Image)
        self.roi_renderer = CroppedImageProvider()

        self.api = cv2backend
        self.index = index
        self.cam = None
        self.dai = daiInit

        self.image = None
        self.cropped_image = None
        self.width = 0
        self.height = 0

        self.cam_fps = 0
        self.ocr_fps = 0

        self.ocr_data = ""
        self.ocr_score = 0
        self.ocr = ThreadOcrBase()
        self.ocr.updatePrediction.connect(self.updatePredictedText)
        self.ocr.updateFps.connect(self.getOcrFps)
        self.ocr.start()

        # self.timer = QTimer(self)
        # self.timer.timeout.connect(self.restartOcrThread)
        # self.timer.start(240000)


    def requestImage(self, id, size, requestedSize):
        if self.image:
            img = self.image
        else:
            img = QImage(640, 480, QImage.Format_RGBA8888)
            img.fill("#00BCD4")
        return img


    @Slot(int, str, int)
    def change_camera(self, index, camera_name=None, dai=-1):
        ## Terminate current camera process
        print(index, camera_name, dai)
        if self.dai:  # End OAK cam
            # code for dai end
            print("> Trying to end DAI pipeline.")  # TODO: DELETE LATER
            self.killThread()

        else:  # End webcam
            print("> Trying to end CV camera.")  # TODO: DELETE LATER
            self.killThread()


        ## Start target camera
        # if dai == -1, the index passed to this function is not a DAI camera
        if dai >= 0:  # Start OAK cam
            # code for dai start
            print(f"\n> Trying to start DAI camera {camera_name}.")
            mxid = self.getMxid(camera_name)
            self.dai = True
            self.start(mxid)

        else:  # Start webcam
            print(f"\n> Trying to start CV camera {camera_name}.")
            self.dai = False
            self.index = index
            self.start()

    @Slot()
    def start(self, dai_mxid=None):
        if self.dai:
            print("\n=====================\n> Starting new DAI camera thread...")
            self.cam = ThreadDaiCamera(dai_mxid)
        else:
            print("=====================\n> Starting new CV camera thread...")
            self.cam = ThreadCvCamera(self.index, self.api)

        self.cam.updateFrame.connect(self.updateImage)
        self.cam.updateFps.connect(self.getCamFps)
        self.cam.openedCamera.connect(self.setDimensions)
        self.cam.start()

    ## Public thread functions
    @Slot()
    def killThread(self):  # For camera thread, not OCR
        print("> Finishing current camera thread...")
        if self.cam is not None: self.cam.stop()

    @Slot()
    def destroyOcrThread(self):
        self.ocr.stop()
        self.ocr = None

    @Slot()
    def restartOcrThread(self):
        self.destroyOcrThread()
        self.ocr = ThreadOcrBase()
        self.ocr.updatePrediction.connect(self.updatePredictedText)
        self.ocr.updateFps.connect(self.getOcrFps)
        self.ocr.start()
        print("> OCR thread restarted.")


    ## Image utility functions
    @Slot()
    def updateImage(self, img, roi_img=None, roi_frame=None):
        self.image = img
        self.cropped_image = roi_img

        if self.ocr is not None: self.ocr.change_image(roi_frame)
        self.roi_renderer.setCroppedImage(roi_img)
        self.imageChanged.emit(img)

    @Slot(int, int)
    def setDimensions(self, width, height):
        self.width = width
        self.height = height
        self.cameraOpened.emit(width, height)  # Send camera width and height to QML files
        self.cam.setRoiCoordinates(0, 0, int(width), int(height))  # Set default coordinates

    @Slot(int, int, int, int)
    def setRoi(self, x1, y1, x2, y2):
        self.cam.setRoiCoordinates(x1, y1, x2, y2)

    @Slot(result=int)
    def getWidth(self):
        return self.width

    @Slot(result=int)
    def getHeight(self):
        return self.height


    ## OCR utility functions
    @Slot()
    def updatePredictedText(self, output="", average_confidence=0):
        self.ocr_data = output
        self.ocr_score = average_confidence
        self.predictionChanged.emit(self.ocr_data, self.ocr_score)

    @Slot(result=str)
    def getOcrData(self):
        return self.ocr_data

    @Slot(result=float)
    def getOcrScore(self):
        return self.ocr_score


    ## Others
    def getRoiRenderer(self):
        return self.roi_renderer

    def getMxid(self, text):
        return text.strip().rsplit(" ", 1)

    ## Profiling
    @Slot()
    def getCamFps(self, average_fps):
        self.cam_fps = average_fps
        self.fpsCamChanged.emit(average_fps)

    @Slot()
    def getOcrFps(self, average_fps):
        self.ocr_fps = average_fps
        self.fpsOcrChanged.emit(average_fps)
