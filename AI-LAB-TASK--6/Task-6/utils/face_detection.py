"""
Face Detection using OpenCV Haar Cascades and landmark estimation
No dlib dependency required.
"""
import cv2
import numpy as np


class FaceDetector:
    """Detect faces and estimate 68-point landmarks using OpenCV only."""

    def __init__(self):
        # Primary: Haar cascade for frontal face detection
        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        )
        # Eye cascades for landmark refinement
        self.eye_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + "haarcascade_eye.xml"
        )

        if self.face_cascade.empty():
            raise RuntimeError("Failed to load Haar cascade for face detection")

        # Try to load LBF facemark model if available, otherwise we'll estimate
        self._facemark = None
        try:
            facemark = cv2.face.createFacemarkLBF()
            # The model file is optional – works without it via estimation
            facemark.loadModel("lbfmodel.yaml")
            self._facemark = facemark
        except Exception:
            pass  # Will use geometric estimation

    # ------------------------------------------------------------------
    def detect_faces(self, image: np.ndarray):
        """Return list of (x, y, w, h) tuples for detected faces."""
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.equalizeHist(gray)
        faces = self.face_cascade.detectMultiScale(
            gray, scaleFactor=1.1, minNeighbors=5, minSize=(60, 60)
        )
        if len(faces) == 0:
            return []
        return [tuple(map(int, f)) for f in faces]

    # ------------------------------------------------------------------
    def detect_landmarks(self, image: np.ndarray, face_rect):
        """
        Return 68-point landmarks (numpy array of shape (68, 2)).
        Uses geometric estimation based on face rectangle and eye positions.
        """
        x, y, w, h = face_rect
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Attempt LBF model first
        if self._facemark is not None:
            try:
                ok, landmarks_list = self._facemark.fit(
                    gray, np.array([[x, y, w, h]])
                )
                if ok and len(landmarks_list) > 0:
                    return np.array(landmarks_list[0][0], dtype=np.float32)
            except Exception:
                pass

        # Geometric estimation of 68 landmarks
        return self._estimate_landmarks(gray, x, y, w, h)

    # ------------------------------------------------------------------
    @staticmethod
    def _estimate_landmarks(gray, x, y, w, h):
        """
        Produce a 68-point landmark array by geometric proportions.
        These approximate the standard dlib 68-point layout:
          0-16  : jawline
          17-21 : left eyebrow
          22-26 : right eyebrow
          27-30 : nose bridge
          31-35 : lower nose
          36-41 : left eye
          42-47 : right eye
          48-67 : mouth
        """
        cx, cy = x + w / 2, y + h / 2
        pts = np.zeros((68, 2), dtype=np.float32)

        # --- Jawline (0-16) ---
        for i in range(17):
            angle = np.pi * (i / 16)
            jx = cx + (w / 2) * np.cos(np.pi - angle)
            jy = y + h * 0.15 + (h * 0.85) * (np.sin(angle) * 0.5 + 0.5)
            pts[i] = [jx, jy]

        # --- Left eyebrow (17-21) ---
        eb_y = y + h * 0.28
        for i, frac in enumerate([0.22, 0.27, 0.33, 0.38, 0.42]):
            pts[17 + i] = [x + w * frac, eb_y - h * 0.02 * (2 - abs(i - 2))]

        # --- Right eyebrow (22-26) ---
        for i, frac in enumerate([0.58, 0.62, 0.67, 0.73, 0.78]):
            pts[22 + i] = [x + w * frac, eb_y - h * 0.02 * (2 - abs(i - 2))]

        # --- Nose bridge (27-30) ---
        for i in range(4):
            pts[27 + i] = [cx, y + h * (0.33 + 0.08 * i)]

        # --- Lower nose (31-35) ---
        nose_y = y + h * 0.58
        for i, frac in enumerate([0.38, 0.43, 0.50, 0.57, 0.62]):
            pts[31 + i] = [x + w * frac, nose_y + (0 if i in (0, 4) else h * 0.02)]

        # --- Left eye (36-41) ---
        ley, lew, leh = y + h * 0.35, w * 0.12, h * 0.04
        lecx = x + w * 0.32
        pts[36] = [lecx - lew, ley]
        pts[37] = [lecx - lew * 0.5, ley - leh]
        pts[38] = [lecx + lew * 0.5, ley - leh]
        pts[39] = [lecx + lew, ley]
        pts[40] = [lecx + lew * 0.5, ley + leh]
        pts[41] = [lecx - lew * 0.5, ley + leh]

        # --- Right eye (42-47) ---
        recx = x + w * 0.68
        pts[42] = [recx - lew, ley]
        pts[43] = [recx - lew * 0.5, ley - leh]
        pts[44] = [recx + lew * 0.5, ley - leh]
        pts[45] = [recx + lew, ley]
        pts[46] = [recx + lew * 0.5, ley + leh]
        pts[47] = [recx - lew * 0.5, ley + leh]

        # --- Mouth outer (48-59) ---
        mouth_cx, mouth_cy = cx, y + h * 0.72
        mw, mh = w * 0.22, h * 0.07
        for i in range(12):
            angle = 2 * np.pi * i / 12
            pts[48 + i] = [
                mouth_cx + mw * np.cos(np.pi - angle),
                mouth_cy + mh * np.sin(np.pi - angle),
            ]

        # --- Mouth inner (60-67) ---
        mw_inner, mh_inner = mw * 0.6, mh * 0.5
        for i in range(8):
            angle = 2 * np.pi * i / 8
            pts[60 + i] = [
                mouth_cx + mw_inner * np.cos(np.pi - angle),
                mouth_cy + mh_inner * np.sin(np.pi - angle),
            ]

        return pts
