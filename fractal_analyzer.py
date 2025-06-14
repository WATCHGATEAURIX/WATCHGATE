# watchgate_vision/fractal_analyzer.py
# --------------------------------------
# Module 2: Fractal Analyzer
# Calculates Shannon entropy and FFT spectrum features to quantify symbolic emergence

import numpy as np
from PIL import Image
from skimage.measure import shannon_entropy
from scipy.fftpack import fft2, fftshift
import os
import json

class FractalAnalyzer:
    def __init__(self):
        pass

    def calculate_entropy(self, image: Image.Image) -> float:
        array = np.array(image)
        return shannon_entropy(array)

    def calculate_fft_signature(self, image: Image.Image, top_n=5) -> list:
        array = np.array(image)
        f_transform = fftshift(fft2(array))
        magnitude = np.abs(f_transform)
        flattened = magnitude.flatten()
        indices = np.argsort(flattened)[-top_n:]
        return [flattened[i] for i in indices]

    def analyze_image(self, image_path: str, output_json: str = None) -> dict:
        image = Image.open(image_path).convert("L")
        entropy = self.calculate_entropy(image)
        fft_peaks = self.calculate_fft_signature(image)
        result = {
            "path": image_path,
            "entropy": round(entropy, 5),
            "fft_peaks": [round(f, 5) for f in fft_peaks]
        }

        if output_json:
            with open(output_json, "w") as f:
                json.dump(result, f, indent=2)

        return result

# Example usage:
# if __name__ == "__main__":
#     analyzer = FractalAnalyzer()
#     stats = analyzer.analyze_image("symbolic_overlays/face_shift_3.png")
#     print(stats)
