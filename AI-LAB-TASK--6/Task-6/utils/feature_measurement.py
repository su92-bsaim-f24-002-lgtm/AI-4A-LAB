"""
Facial Feature Measurement from 68-point landmarks.
Provides raw pixel measurements, normalised ratios, and human-readable summaries.
"""
import numpy as np


def _dist(a, b):
    """Euclidean distance between two 2-D points."""
    return float(np.linalg.norm(np.array(a) - np.array(b)))


class FeatureMeasurement:
    """Compute facial measurements from a (68, 2) landmark array."""

    def __init__(self, landmarks: np.ndarray):
        self.lm = landmarks  # shape (68, 2)
        self._measurements = None
        self._normalized = None

    # ------------------------------------------------------------------
    def get_measurements(self) -> dict:
        """Return raw pixel-based measurements."""
        if self._measurements is not None:
            return self._measurements

        lm = self.lm

        # Face dimensions
        face_width = _dist(lm[0], lm[16])
        face_height = _dist(lm[8], lm[27])

        # Eyes
        left_eye_width = _dist(lm[36], lm[39])
        left_eye_height = (_dist(lm[37], lm[41]) + _dist(lm[38], lm[40])) / 2
        right_eye_width = _dist(lm[42], lm[45])
        right_eye_height = (_dist(lm[43], lm[47]) + _dist(lm[44], lm[46])) / 2
        eye_spacing = _dist(lm[39], lm[42])

        # Nose
        nose_length = _dist(lm[27], lm[33])
        nose_width = _dist(lm[31], lm[35])

        # Mouth
        mouth_width = _dist(lm[48], lm[54])
        mouth_height = _dist(lm[51], lm[57])

        # Jaw
        jaw_width = _dist(lm[3], lm[13])
        jaw_length = _dist(lm[8], (lm[3] + lm[13]) / 2)

        self._measurements = {
            "face_width": face_width,
            "face_height": face_height,
            "left_eye_width": left_eye_width,
            "left_eye_height": left_eye_height,
            "right_eye_width": right_eye_width,
            "right_eye_height": right_eye_height,
            "eye_spacing": eye_spacing,
            "nose_length": nose_length,
            "nose_width": nose_width,
            "mouth_width": mouth_width,
            "mouth_height": mouth_height,
            "jaw_width": jaw_width,
            "jaw_length": jaw_length,
        }
        return self._measurements

    # ------------------------------------------------------------------
    def get_normalized_measurements(self) -> dict:
        """Return measurements normalised to face width (0-1 range)."""
        if self._normalized is not None:
            return self._normalized

        m = self.get_measurements()
        fw = m["face_width"] or 1  # avoid division by zero

        self._normalized = {
            "face_ratio": m["face_height"] / fw,
            "left_eye_openness": m["left_eye_height"] / (m["left_eye_width"] or 1),
            "right_eye_openness": m["right_eye_height"] / (m["right_eye_width"] or 1),
            "eye_spacing_ratio": m["eye_spacing"] / fw,
            "nose_length_ratio": m["nose_length"] / fw,
            "nose_width_ratio": m["nose_width"] / fw,
            "mouth_width_ratio": m["mouth_width"] / fw,
            "mouth_height_ratio": m["mouth_height"] / fw,
            "jaw_width_ratio": m["jaw_width"] / fw,
            "jaw_length_ratio": m["jaw_length"] / fw,
        }
        return self._normalized

    # ------------------------------------------------------------------
    def get_summary(self) -> dict:
        """Return a human-readable summary of the feature measurements."""
        n = self.get_normalized_measurements()

        def classify(value, low, high, labels=("narrow", "average", "wide")):
            if value < low:
                return labels[0]
            elif value > high:
                return labels[2]
            return labels[1]

        face_shape = classify(
            n["face_ratio"], 1.1, 1.4, ("round", "oval", "long")
        )
        eye_size = classify(
            (n["left_eye_openness"] + n["right_eye_openness"]) / 2,
            0.25, 0.40,
            ("small", "medium", "large"),
        )
        nose_size = classify(n["nose_width_ratio"], 0.20, 0.30, ("narrow", "average", "wide"))
        mouth_size = classify(n["mouth_width_ratio"], 0.30, 0.45, ("small", "average", "wide"))
        jaw_shape = classify(n["jaw_width_ratio"], 0.65, 0.80, ("narrow", "average", "wide"))

        return {
            "face_shape": face_shape,
            "eye_size": eye_size,
            "nose_size": nose_size,
            "mouth_size": mouth_size,
            "jaw_shape": jaw_shape,
        }
