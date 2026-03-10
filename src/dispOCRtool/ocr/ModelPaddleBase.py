"""
ModelPaddleBase.py
Contains class for OCR prediction thread.
Inherits from QThread.
"""

from collections import deque
import cv2
import numpy as np
from paddleocr import PaddleOCR

from PySide6.QtCore import Slot, Signal
from PySide6.QtCore import QThread, QElapsedTimer


class ThreadOcrBase(QThread):
    updatePrediction = Signal(str, float)
    updateFps = Signal(float)

    def __init__(self, image=None, scale=0.6, minimum_score=0.65, parent=None):
        QThread.__init__(self, parent)

        self._running = False
        self._setup = False
        self.image = image  # numpy image array
        self.text = None
        self.score = 0

        self.SCALE = scale
        self.MIN_SCORE = minimum_score

        self.timer = QElapsedTimer()  # For performance measure
        self.elapsed_queue = deque(maxlen=10)  # To compute moving ave


    def run(self):
        ocr = PaddleOCR(
            ## GENERAL OPTIONS
            use_doc_orientation_classify=False,
            use_doc_unwarping=False,
            use_textline_orientation=False,
            show_log=False,
            
            ## PADDLEV3 OPTIONS (Tested on 3.3.2)
            # device="cpu",
            # text_detection_model_name="PP-OCRv4_mobile_det",
            # text_detection_model_dir=None,
            # text_recognition_model_name="en_PP-OCRv4_mobile_rec",
            # text_recognition_model_dir=None,

            ## PADDLEV2 OPTIONS (Tested on 2.9.1)
            lang="en",
            det_model_name="en_PP-OCRv4_mobile_det",
            rec_model_name="en_PP-OCRv4_mobile_rec",
            # rec_algorithm="SVTR_LCNet",
            drop_score=self.MIN_SCORE,

        )

        print("> PaddleOCR successfully initialized.")
        self._running = True
        while self._running:
            if self.image is not None:
                self.timer.start()  # Start performance timer

                ## Prepare frame for prediction
                self._setup = True  # Prevent modifying self.image during color mode conversion
                rgb = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
                self._setup = False

                # Resize for speed
                h, w = rgb.shape[:2]
                if h < 150 or w < 150:
                    rgb_small = rgb
                else:
                    rgb_small = cv2.resize(
                        rgb,
                        (max(1, int(w * self.SCALE)), max(1, int(h * self.SCALE))),
                        interpolation=cv2.INTER_AREA,
                    )

                ## Prediction
                if hasattr(ocr, "predict"):
                    final_str, ave_score = self.paddle_v3_predict(ocr, rgb_small)
                else:
                    final_str, ave_score = self.paddle_v2_predict(ocr, rgb_small)

                ## Emit results to main
                self.updatePrediction.emit(final_str, ave_score)

                ## Profiling
                if self.timer.elapsed() != 0: 
                    if "arm" in platform.machine().lower() or "aarch" in platform.machine().lower():
                        # Throttle to max 10 fps if ARM arch
                        time_el = self.timer.restart()
                        if time_el < 100:
                            time.sleep((100-time_el)/1000)
                            time_el = 100
                        self.elapsed_queue.append(1000/time_el)
                        self.timer.restart()
                    else:
                        self.elapsed_queue.append(1000/self.timer.restart())
                    
                ave = 0 if len(self.elapsed_queue) == 0 else sum(self.elapsed_queue)/len(self.elapsed_queue)
                self.updateFps.emit(ave)


    def stop(self):
        self._running = False
        self.requestInterruption()
        self.wait()
        print("> OCR thread ended successfully.")

    @Slot(object)
    def change_image(self, frame):
        if not self._setup:
            self.image = frame.copy()


    def paddle_v2_predict(self, ocr, image):
        results = ocr.ocr(image, cls=False)

        # Parse result
        final_str = ""
        ave_score = 0
        count = 0
        if isinstance(results, list) and len(results) > 0 and results[0] is not None:
            for r in results[0]:
                try:
                    txt = str(r[1][0])
                    conf = float(r[1][1])
                    final_str += " " + txt
                    ave_score += conf
                    count += 1
                except Exception:
                    pass
            ave_score = ave_score / count

        return final_str, ave_score
    

    def paddle_v3_predict(self, ocr, image):
        results = ocr.predict(image)
        dets = self.extract_detections(results, self.MIN_SCORE)

        final_str = ""
        ave_score = 0
        for txt, score in dets:
            final_str += txt + " "
            ave_score += score

        if len(dets):
            ave_score = ave_score / len(dets)

        return final_str, ave_score


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
            for txt, sc in zip(rec_texts, rec_scores):
                try:
                    score = float(sc)
                except Exception:
                    score = 0.0
                txt = "" if txt is None else str(txt)
                if txt and score >= min_score:
                    dets.append((txt, score))

        return dets
