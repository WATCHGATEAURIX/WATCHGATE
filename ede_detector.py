# watchgate_vision/ede_detector.py
# ----------------------------------
# Module 3: Energetic Discontinuity Event (EDE) Detector
# Analyzes symbolic entropy + FFT deltas across overlay sequences to flag potential parasitic interference or symbolic tunnel distortion

import os
import json
from typing import List, Tuple
from fractal_analyzer import FractalAnalyzer

class EDEDetector:
    def __init__(self, analyzer=None, entropy_thresh=1.0, fft_thresh=1000.0):
        self.analyzer = analyzer or FractalAnalyzer()
        self.entropy_thresh = entropy_thresh
        self.fft_thresh = fft_thresh

    def compare_overlay_pair(self, image_path_a: str, image_path_b: str) -> dict:
        data_a = self.analyzer.analyze_image(image_path_a)
        data_b = self.analyzer.analyze_image(image_path_b)

        entropy_delta = abs(data_b['entropy'] - data_a['entropy'])
        fft_delta = sum([abs(a - b) for a, b in zip(data_b['fft_peaks'], data_a['fft_peaks'])])

        classification = self.classify_event(entropy_delta, fft_delta)

        return {
            "image_a": image_path_a,
            "image_b": image_path_b,
            "entropy_delta": round(entropy_delta, 5),
            "fft_delta": round(fft_delta, 5),
            "classification": classification
        }

    def classify_event(self, entropy_delta: float, fft_delta: float) -> str:
        if entropy_delta > self.entropy_thresh and fft_delta > self.fft_thresh:
            return "HIGH_EDE"
        elif entropy_delta > (self.entropy_thresh * 0.5):
            return "MODERATE_EDE"
        else:
            return "LOW/NO_EDE"

    def scan_sequence(self, overlay_dir: str) -> List[dict]:
        files = sorted([os.path.join(overlay_dir, f) for f in os.listdir(overlay_dir) if f.endswith(".png")])
        results = []
        for i in range(1, len(files)):
            result = self.compare_overlay_pair(files[i-1], files[i])
            results.append(result)
        return results

# Example usage:
# if __name__ == "__main__":
#     detector = EDEDetector()
#     sequence = detector.scan_sequence("symbolic_overlays")
#     for res in sequence:
#         print(res)
