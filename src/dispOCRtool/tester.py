import argparse
import sys
import time

import cv2
import numpy as np
from paddleocr import PaddleOCR


def unwrap_payload(res0):
    """
    PaddleOCR 3.x results often behave like:
      res0.res -> {'res': {...}}  OR  res0.res -> {...}
    Normalize to the inner dict.
    """
    payload = getattr(res0, "res", res0)
    if isinstance(payload, dict) and "res" in payload and isinstance(payload["res"], dict):
        payload = payload["res"]
    return payload if isinstance(payload, dict) else None


def extract_detections(results, min_score: float):
    """
    Returns list of (poly, text, score) where:
      poly: (N,2) float32
    """
    if not results:
        return []

    payload = unwrap_payload(results[0])
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


def draw(frame_bgr, dets):
    for poly, txt, score in dets:
        pts = np.array(poly, dtype=np.int32).reshape((-1, 1, 2))
        cv2.polylines(frame_bgr, [pts], True, (0, 255, 0), 2)

        x, y = int(pts[0, 0, 0]), int(pts[0, 0, 1])
        label = f"{txt} ({score:.2f})"
        cv2.putText(
            frame_bgr,
            label,
            (x, max(0, y - 6)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 255, 0),
            2,
            cv2.LINE_AA,
        )


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cam", type=int, default=0)
    ap.add_argument("--width", type=int, default=1280)
    ap.add_argument("--height", type=int, default=720)

    ap.add_argument("--lang", type=str, default="en")
    ap.add_argument("--device", type=str, default="cpu")  # e.g., cpu, gpu:0

    # Official model names (used if you DON'T pass --det-dir/--rec-dir)
    ap.add_argument("--det-model", type=str, default="PP-OCRv5_mobile_det")
    ap.add_argument("--rec-model", type=str, default="en_PP-OCRv5_mobile_rec")

    # NEW: local exported inference dirs (contain inference.yml)
    ap.add_argument("--det-dir", type=str, default=None,
                    help="Path to exported DET inference dir (contains inference.yml)")
    ap.add_argument("--rec-dir", type=str, default=None,
                    help="Path to exported REC inference dir (contains inference.yml)")

    ap.add_argument("--ocr-every", type=int, default=8, help="run OCR every N frames")
    ap.add_argument("--scale", type=float, default=0.6, help="resize factor before OCR (smaller=faster)")
    ap.add_argument("--min-score", type=float, default=0.5)
    args = ap.parse_args()

    # --- Init OCR (PaddleOCR 3.x) ---
    # If *-dir is provided, use your local exported model dir.
    # Otherwise fall back to the official model name.
    ocr = PaddleOCR(
    lang=args.lang,
    device=args.device,

    text_detection_model_name=args.det_model,
    text_detection_model_dir=args.det_dir,

    text_recognition_model_name=args.rec_model,   # <-- always set the name
    text_recognition_model_dir=args.rec_dir,      # <-- optional local dir

    use_doc_orientation_classify=False,
    use_doc_unwarping=False,
    use_textline_orientation=False,
)


    if not hasattr(ocr, "predict"):
        print("ERROR: Your PaddleOCR install doesn't have PaddleOCR.predict(). Are you sure it's PaddleOCR 3.x?")
        sys.exit(1)

    # --- Camera ---
    cap = cv2.VideoCapture(args.cam)
    if not cap.isOpened():
        raise RuntimeError(f"Could not open camera index {args.cam}. Try --cam 1 or --cam 2")

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, args.width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, args.height)

    frame_i = 0
    last_dets = []
    t_prev = time.perf_counter()

    print("Press 'q' to quit.")
    print(
        "Using "
        + (f"det_dir={args.det_dir} " if args.det_dir else f"det_model={args.det_model} ")
        + (f"rec_dir={args.rec_dir} " if args.rec_dir else f"rec_model={args.rec_model} ")
        + f"lang={args.lang} device={args.device}"
    )

    while True:
        ok, frame_bgr = cap.read()
        if not ok:
            break

        frame_i += 1

        if frame_i % max(1, args.ocr_every) == 0:
            rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)

            # resize for speed
            if abs(args.scale - 1.0) > 1e-6:
                h, w = rgb.shape[:2]
                rgb_small = cv2.resize(
                    rgb,
                    (max(1, int(w * args.scale)), max(1, int(h * args.scale))),
                    interpolation=cv2.INTER_AREA,
                )
            else:
                rgb_small = rgb

            results = ocr.predict(rgb_small)
            dets = extract_detections(results, args.min_score)

            # map polys back to full frame if scaled
            if abs(args.scale - 1.0) > 1e-6 and dets:
                inv = 1.0 / args.scale
                last_dets = [(poly * inv, txt, sc) for (poly, txt, sc) in dets]
            else:
                last_dets = dets

        draw(frame_bgr, last_dets)

        # FPS
        t_now = time.perf_counter()
        fps = 1.0 / max(1e-6, (t_now - t_prev))
        t_prev = t_now
        cv2.putText(
            frame_bgr,
            f"FPS: {fps:.1f} | dets: {len(last_dets)} | OCR every: {args.ocr_every}",
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255, 255, 255),
            2,
            cv2.LINE_AA,
        )

        cv2.imshow("PaddleOCR 3.x Webcam", frame_bgr)
        if (cv2.waitKey(1) & 0xFF) == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
