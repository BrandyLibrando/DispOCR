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

from app.settings import AppConfigs


class ThreadCvCamera(QThread):
    updateFrame = Signal(object, object)
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

                self.image = frame
                self.roi_image = roi_frame
                self.updateFrame.emit(frame, roi_frame)  # signal reload to Image class within QML

                ## Profiling
                if self.timer.elapsed() != 0: self.elapsed_queue.append(1000/self.timer.restart())
                ave = 0 if len(self.elapsed_queue) == 0 else sum(self.elapsed_queue)/len(self.elapsed_queue)
                self.updateFps.emit(ave)


    def stop(self):
        self.cap.release()
        self._running = False
        self.requestInterruption()
        self.wait()
        print("> CV thread ended successfully.")

    @Slot(int, int, int, int)
    def setRoiCoordinates(self, x1, y1, x2, y2):
        self.new_roi = (x1, y1, x2, y2)
        self.roi_changed = True
        print("> ROI coordinates set successfully.")


class ThreadDaiCamera(QThread):
    updateFrame = Signal(object, object)
    updateFps = Signal(float)
    openedCamera = Signal(int, int)

    def __init__(self, mxid, parent=None):
        QThread.__init__(self, parent)

        self.cfg = AppConfigs
        self.cfg.daiSettingsUpdated.connect(self.send_controls)

        self.width  = 640
        self.height = 480

        self.pipeline = dai.Pipeline()

        self.dai_cam = self.pipeline.create(dai.node.Camera).build()
        self.dai_prev = self.dai_cam.requestOutput(
                (self.width, self.height), 
                type=dai.ImgFrame.Type.BGR888p,
                fps=12
            )

        self.dai_out = self.dai_prev.createOutputQueue()
        self.dai_in  = self.dai_cam.inputControl.createInputQueue()

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
        self.pipeline.start()
        self.openedCamera.emit(self.width, self.height)  # Send width and height to ImageProvider
        self.timer.start()  # Start performance timer

        with self.pipeline:
            while self._running:
                if self.roi_changed:
                    self.x1, self.y1, self.x2, self.y2 = self.new_roi
                    self.roi_changed = False

                try: inFrame = self.dai_out.get() 
                except dai.MessageQueue.QueueException: print("> Cannot proceed getting frame from DAI, queue closed.")
                
                if inFrame is not None:
                    frame = inFrame.getCvFrame()

                try:
                    if self._running and frame is not None:
                        roi_frame = np.ascontiguousarray(frame[self.y1:self.y2, self.x1:self.x2])
                    else:
                        roi_frame = cv2.cvtColor(np.zeros((300, 300), dtype=np.uint8), cv2.COLOR_GRAY2BGR)
                        frame = cv2.cvtColor(np.zeros((300, 300), dtype=np.uint8), cv2.COLOR_GRAY2BGR)
                except:
                    self._running = False
                    break

                self.image = frame
                self.roi_image = roi_frame
                self.updateFrame.emit(frame, roi_frame)  # signal reload to Image class within QML

                ## Profiling
                if self.timer.elapsed() != 0: self.elapsed_queue.append(1000/self.timer.restart())
                ave = 0 if len(self.elapsed_queue) == 0 else sum(self.elapsed_queue)/len(self.elapsed_queue)
                self.updateFps.emit(ave)

                if not self._running:
                    break


    def stop(self):
        self._running = False
        self.pipeline.stop()
        self.wait()
        print("> DAI thread ended successfully.")

    @Slot(int, int, int, int)
    def setRoiCoordinates(self, x1, y1, x2, y2):
        self.new_roi = (x1, y1, x2, y2)
        self.roi_changed = True
        print("> ROI coordinates set successfully.")

    @Slot()
    def send_controls(self):
        use_manual_exposure = self.cfg.getEnableManualExposure()
        use_manual_focus    = self.cfg.getEnableManualFocus()
        use_manual_wb       = self.cfg.getEnableManualWhiteBalance()

        manual_exposure     = self.cfg.getManualExposure()
        manual_iso          = self.cfg.getManualIso()
        manual_focus        = self.cfg.getManualFocus()
        manual_wb           = self.cfg.getManualWhiteBalance()

        ctrl = dai.CameraControl()
        if use_manual_exposure:
            ctrl.setManualExposure(manual_exposure, manual_iso)  # (exposure time, ISO)
        else:
            ctrl.setAutoExposureEnable()

        if use_manual_focus:
            ctrl.setManualFocus(manual_focus)
        else:
            ctrl.setAutoFocusMode(dai.CameraControl.AutoFocusMode.CONTINUOUS_VIDEO)

        if use_manual_wb:
            ctrl.setManualWhiteBalance(manual_wb)
        else:
            ctrl.setAutoWhiteBalanceMode(dai.CameraControl.AutoWhiteBalanceMode.AUTO)

        self.dai_in.send(ctrl)
