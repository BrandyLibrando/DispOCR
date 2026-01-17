"""
OpencvRenderer.py
Contains classes for handling QML threaded camera handling
using OpenCV and QThreads.
"""

import cv2
import numpy as np
import depthai as dai

from PySide6.QtGui import QImage
from PySide6.QtCore import Slot, Signal
from PySide6.QtCore import QThread
from PySide6.QtQuick import QQuickImageProvider

from util.CroppedImageRenderer import CroppedImageProvider


class OpencvImageProvider(QQuickImageProvider):
    imageChanged = Signal(QImage)
    cameraOpened = Signal(int, int)

    def __init__(self, index=0, cv2backend=cv2.CAP_ANY, daiSupport=False, dai=False):
        super(OpencvImageProvider, self).__init__(QQuickImageProvider.Image)
        self.roi_renderer = CroppedImageProvider()

        self.api = cv2backend
        self.index = index
        self.cam = None
        self.dai = None

        self.image = None
        self.cropped_image = None
        self.width = 0
        self.height = 0


        # DEPTH AI PIPELINE INITIATION
        if daiSupport:
            self.pipeline = dai.Pipeline()

            self.dai_cam = self.pipeline.create(dai.node.ColorCamera)
            self.dai_cam.setPreviewSize(640, 480)
            self.dai_cam.setInterleaved(False)
            self.dai_cam.setColorOrder(dai.ColorCameraProperties.ColorOrder.BGR)
            self.dai_cam.setFps(30)

            self.dai_xout = self.pipeline.create(dai.node.XLinkOut)
            self.dai_xout.setStreamName("preview")
            self.dai_cam.preview.link(self.dai_xout.input)

            self.dai_control_in = self.pipeline.create(dai.node.XLinkIn)
            self.dai_control_in.setStreamName("control")
            self.dai_control_in.out.link(self.dai_cam.inputControl)


    def requestImage(self, id, size, requestedSize):
        if self.image:
            img = self.image
        else:
            img = QImage(640, 480, QImage.Format_RGBA8888)
            img.fill("#00BCD4")
        return img

    @Slot(int, str, int)
    def change_camera(self, index, camera_name=None, dai=-1):
        # Terminate current camera process
        # End OAK cam
        if self.dai:
            # code for dai end
            print("> Trying to end DAI pipeline.")

        # End webcam
        else:
            print("> Trying to end CV camera.")
            self.killThread()


        # if dai == -1, the index passed to this function is not a DAI camera
        # Start OAK cam
        if dai != -1:
            # code for dai start
            print(f"> Trying to start DAI camera {camera_name}.")

            mxid = self.getMxid(camera_name)
            self.start(mxid)

        # Start webcam
        elif dai >= 0:
            print(f"> Trying to start CV camera {camera_name}.")
            self.index = index
            self.start()

        else:
            print("An error occurred.")

    @Slot()
    def start(self, dai_mxid=None):
        if self.dai:
            print("=====================\n> Starting new DAI camera thread...")
            self.cam = ThreadDaiCamera(self.pipeline, dai_mxid)
        else:
            print("=====================\n> Starting new CV camera thread...")
            self.cam = ThreadCvCamera(self.index, self.api)
        self.cam.updateFrame.connect(self.updateImage)
        self.cam.openedCamera.connect(self.setDimensions)
        self.cam.start()

    @Slot()
    def killThread(self):
        print("> Finishing current CV camera thread...")
        self.cam.stop()

    @Slot()
    def updateImage(self, img, roi_img=None):
        self.image = img
        self.cropped_image = roi_img
        self.roi_renderer.setCroppedImage(roi_img)
        self.imageChanged.emit(img)

    def setDimensions(self, width, height):
        self.width = width
        self.height = height
        self.cameraOpened.emit(width, height)  # Send camera width and height to QML files
        self.cam.setRoiCoordinates(0, int(width), 0, int(height))  # Set default coordinates

    @Slot(int, int, int, int)
    def setRoi(self, x1, y1, x2, y2):
        self.cam.setRoiCoordinates(x1, x2, y1, y2)

    @Slot()
    def getWidth(self):
        return self.cam.width

    @Slot()
    def getHeight(self):
        return self.cam.height

    def getRoiRenderer(self):
        return self.roi_renderer

    def getMxid(self, text):
        return text.strip().rsplit(" ", 1)



class ThreadCvCamera(QThread):
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
        self.new_roi = (0, 0, 0, 0)
        self.roi_changed = False

    def run(self):
        self.openedCamera.emit(self.width, self.height)  # Send width and height to ImageProvider
    
        while self._running:
            if self.roi_changed:
                self.x1, self.x2, self.y1, self.y2 = self.new_roi
                self.roi_changed = False

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
        print("> CV thread ended successfully.")

    @Slot()
    def setRoiCoordinates(self, x1, x2, y1, y2):
        self.new_roi = (x1, x2, y1, y2)
        self.roi_changed = True
        print("> ROI coordinates set successfully.")





class ThreadDaiCamera(QThread):
    updateFrame = Signal(QImage, QImage)
    openedCamera = Signal(int, int)

    def __init__(self, pipeline, mxid, parent=None):
        QThread.__init__(self, parent)

        self.cap = dai.Device(pipeline, mxid)
        self.queue = self.cap.getOutputQueue("preview", maxSize=1, blocking=False)
        self.controls = self.cap.getInputQueue("control")

        frame = self.cap.get().getCvFrame()
        self.height, self.width = frame.shape[:2]

        self.image = None
        self.roi_image = None
        self._running = True

        self.x1 = 0
        self.x2 = self.width
        self.y1 = 0
        self.y2 = self.height

    def run(self):
        self.openedCamera.emit(self.width, self.height)  # Send width and height to ImageProvider

        while self._running:
            inFrame = self.cap.tryGet()
            if inFrame is not None:
                frame = inFrame.getCvFrame()

                try:
                    if self._running and frame:
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
        self.cap.close()
        self._running = False
        self.requestInterruption()
        self.wait()
        print("> DAI thread ended successfully.")

    # @Slot()
    # def send_controls():
    #     ctrl = dai.CameraControl()

    #     if use_manual_exposure:
    #         ctrl.setManualExposure(exposure_us, iso)  # (exposure time, ISO)
    #     else:
    #         ctrl.setAutoExposureEnable()

    #     if use_manual_focus:
    #         ctrl.setManualFocus(focus)
    #     else:
    #         ctrl.setAutoFocusMode(dai.CameraControl.AutoFocusMode.CONTINUOUS_VIDEO)

    #     if use_manual_wb:
    #         ctrl.setManualWhiteBalance(wb_k)
    #     else:
    #         ctrl.setAutoWhiteBalanceMode(dai.CameraControl.AutoWhiteBalanceMode.AUTO)

    #     ctrlQ.send(ctrl)
