"""
CameraThreads.py
Contains classes for handling QML threaded camera handling
using OpenCV/DepthAI and QThread.
"""

from collections import deque
import cv2
import numpy as np
import depthai as dai

from PySide6.QtGui import QImage
from PySide6.QtCore import Slot, Signal
from PySide6.QtCore import QThread, QElapsedTimer


class ThreadCvCamera(QThread):
    updateFrame = Signal(QImage, QImage, object)
    updateFps = Signal(float)
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

        self.timer = QElapsedTimer()  # For performance measure
        self.elapsed_queue = deque(maxlen=10)  # To compute moving ave

    def run(self):
        self.openedCamera.emit(self.width, self.height)  # Send width and height to ImageProvider
        self.timer.start()  # Start performance timer

        while self._running:
            if self.roi_changed:
                self.x1, self.y1, self.x2, self.y2 = self.new_roi
                self.roi_changed = False

            if self.cap.isOpened:
                ret, frame = self.cap.read()
                if not ret:
                    break

                try:
                    if self._running and ret:
                        roi_frame = np.ascontiguousarray(frame[self.y1:self.y2, self.x1:self.x2])
                    else:
                        roi_frame = cv2.cvtColor(np.zeros((300, 300), dtype=np.uint8), cv2.COLOR_GRAY2BGR)
                        frame = cv2.cvtColor(np.zeros((300, 300), dtype=np.uint8), cv2.COLOR_GRAY2BGR)
                except:
                    self._running = False
                    break

                img = QImage(frame.data, frame.shape[1], frame.shape[0], QImage.Format_BGR888)
                roi_img = QImage(roi_frame.data, roi_frame.shape[1], roi_frame.shape[0], roi_frame.strides[0], QImage.Format_BGR888)  # try using deep copy later if fail
                self.image = frame
                self.roi_image = roi_frame
                self.updateFrame.emit(img, roi_img, roi_frame)  # signal reload to Image class within QML

                ## Profiling
                if self.timer.elapsed != 0: self.elapsed_queue.append(1000/self.timer.restart())
                ave = 0 if len(self.elapsed_queue) == 0 else sum(self.elapsed_queue)/len(self.elapsed_queue)
                self.updateFps.emit(ave)


    def stop(self):
        self.cap.release()
        self._running = False
        self.requestInterruption()
        self.wait()
        print("> CV thread ended successfully.")

    @Slot()
    def setRoiCoordinates(self, x1, y1, x2, y2):
        self.new_roi = (x1, y1, x2, y2)
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
        self.new_roi = (0, 0, 0, 0)
        self.roi_changed = False

        self.timer = QElapsedTimer()  # For performance measure
        self.elapsed_queue = deque(maxlen=10)  # To compute moving ave

    def run(self):
        self.openedCamera.emit(self.width, self.height)  # Send width and height to ImageProvider
        self.timer.start()  # Start performance timer

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

                ## Profiling
                if self.timer.elapsed != 0: self.elapsed_queue.append(1000/self.timer.restart())
                ave = 0 if len(self.elapsed_queue) == 0 else sum(self.elapsed_queue)/len(self.elapsed_queue)
                self.updateFps.emit(ave)


    def stop(self):
        self.cap.close()
        self._running = False
        self.requestInterruption()
        self.wait()
        print("> DAI thread ended successfully.")

    # @Slot()
    # def setRoiCoordinates(self, x1, y1, x2, y2):
    #     self.new_roi = (x1, y1, x2, y2)
    #     self.roi_changed = True
    #     print("> ROI coordinates set successfully.")

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
