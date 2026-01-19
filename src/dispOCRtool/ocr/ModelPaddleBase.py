"""
ModelPaddleBase.py
Contains class for OCR prediction thread.
Inherits from QThread.
"""

import cv2
import numpy as np
from paddleocr import PaddleOCR

from PySide6.QtCore import Signal
from PySide6.QtCore import QThread


class ThreadOcrBase(QThread):
    updatePrediction = Signal(str)

    def __init__(self, image, scale=0.6, minimum_score=0.5, parent=None):
        QThread.__init__(self, parent)

        self.image = image  # numpy image array
        self.data = None

        self.SCALE = scale
        self.MIN_SCORE = minimum_score

    def run(self):
        ocr = PaddleOCR(
            lang="en", device="cpu",

            text_detection_model_name="PP-OCRv5_mobile_det",
            text_detection_model_dir=None,
            text_recognition_model_name="",
            text_recognition_model_dir=None,
            use_doc_orientation_classify=False,
            use_doc_unwarping=False,
            use_textline_orientation=False,
        )

        if not hasattr(ocr, "predict"):
            print("> ERROR: Your PaddleOCR install doesn't have PaddleOCR.predict(). Are you sure it's PaddleOCR 3.x?")
            return

        ## Prepare frame for prediction
        rgb = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)

        # resize for speed
        h, w = rgb.shape[:2]
        rgb_small = cv2.resize(
            rgb,
            (max(1, int(w * self.SCALE)), max(1, int(h * self.SCALE))),
            interpolation=cv2.INTER_AREA,
        )

        ## Prediction
        results = ocr.predict(rgb_small)
        dets = self.extract_detections(results, self.MIN_SCORE)

        # end
        self.updatePrediction.emit("hi")

    def stop(self):
        self.requestInterruption()
        self.wait()


    def unwrap_payload(self, res0):
        """
        PaddleOCR 3.x results often behave like:
          res0.res -> {'res': {...}}  OR  res0.res -> {...}
        Normalize to the inner dict.
        """
        payload = getattr(res0, "res", res0)
        if isinstance(payload, dict) and "res" in payload and isinstance(payload["res"], dict):
            payload = payload["res"]
        return payload if isinstance(payload, dict) else None

    def extract_detections(self, results, min_score: float):
        """
        Returns list of (poly, text, score) where:
          poly: (N,2) float32
        """
        if not results:
            return []

        payload = self.unwrap_payload(results[0])
        if not payload:
            return []

        dt_polys = payload.get("dt_polys", None)
        rec_texts = payload.get("rec_texts", [])
        rec_scores = payload.get("rec_scores", [])

        if dt_polys is None:
            return []

        dt_polys = np.array(dt_polys)
        if isinstance(rec_scores, np.ndarray):
            rec_scores = rec_scores.tolist()

        dets = []
        if len(rec_texts) == len(dt_polys):
            for poly, txt, sc in zip(dt_polys, rec_texts, rec_scores):
                try:
                    score = float(sc)
                except Exception:
                    score = 0.0
                txt = "" if txt is None else str(txt)
                if txt and score >= min_score:
                    poly = np.array(poly, dtype=np.float32).reshape(-1, 2)
                    dets.append((poly, txt, score))

        return dets



# class ThreadCvCamera(QThread):
#     updateFrame = Signal(QImage, QImage)
#     openedCamera = Signal(int, int)

#     def __init__(self, index, apiPreference=cv2.CAP_ANY, parent=None):
#         QThread.__init__(self, parent)

#         self.cap = cv2.VideoCapture(index, apiPreference)
#         self.width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
#         self.height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

#         self.image = None
#         self.roi_image = None
#         self._running = True

#         self.x1 = 0
#         self.x2 = self.width
#         self.y1 = 0
#         self.y2 = self.height
#         self.new_roi = (0, 0, 0, 0)
#         self.roi_changed = False

#     def run(self):
#         self.openedCamera.emit(self.width, self.height)  # Send width and height to ImageProvider

#         while self._running:
#             if self.roi_changed:
#                 self.x1, self.y1, self.x2, self.y2 = self.new_roi
#                 self.roi_changed = False

#             if self.cap.isOpened:
#                 ret, frame = self.cap.read()
#                 if not ret:
#                     break

#                 try:
#                     if self._running and ret:
#                         roi_frame = np.ascontiguousarray(frame[self.y1:self.y2, self.x1:self.x2])
#                     else:
#                         roi_frame = cv2.cvtColor(np.zeros((300, 300), dtype=np.uint8), cv2.COLOR_GRAY2BGR)
#                         frame = cv2.cvtColor(np.zeros((300, 300), dtype=np.uint8), cv2.COLOR_GRAY2BGR)
#                 except:
#                     self._running = False
#                     break

#                 img = QImage(frame.data, frame.shape[1], frame.shape[0], QImage.Format_BGR888)
#                 roi_img = QImage(roi_frame.data, roi_frame.shape[1], roi_frame.shape[0], roi_frame.strides[0], QImage.Format_BGR888)  # try using deep copy later if fail
#                 self.image = frame
#                 self.roi_image = roi_frame
#                 self.updateFrame.emit(img, roi_img)  # signal reload to Image class within QML

#     def stop(self):
#         self.cap.release()
#         self._running = False
#         self.requestInterruption()
#         self.wait()
#         print("> CV thread ended successfully.")

#     @Slot()
#     def setRoiCoordinates(self, x1, y1, x2, y2):
#         self.new_roi = (x1, y1, x2, y2)
#         self.roi_changed = True
#         print("> ROI coordinates set successfully.")
