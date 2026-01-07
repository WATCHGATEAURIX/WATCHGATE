# watchgate_vision/symbolic_overlay.py
# --------------------------------------
# Symbolic Overlay Engine for WATCHGATE
# Mirrors, aligns, and overlays imagery with pixel shifts to reveal symbolic emergence

import numpy as np
from PIL import Image, ImageOps, ImageChops
import os

class SymbolicOverlayProcessor:
    def __init__(self, shift_range=range(1, 6), output_dir="symbolic_overlays"):
        self.shift_range = shift_range
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def process_image(self, input_path, base_name=None):
        image = Image.open(input_path).convert("L")
        mirrored = ImageOps.mirror(image)
        width, height = image.size

        center_x = width // 2
        alignment_offset = center_x - width // 2  # default 0, can be adjusted
        mirrored = ImageChops.offset(mirrored, alignment_offset, 0)

        overlays = []

        for shift in self.shift_range:
            shifted = ImageChops.offset(mirrored, shift, 0)
            combined = ImageChops.multiply(image, shifted)
            filename = f"{base_name or 'overlay'}_shift_{shift}.png"
            path = os.path.join(self.output_dir, filename)
            combined.save(path)
            overlays.append((shift, path))

        return overlays

# Example usage:
# if __name__ == "__main__":
#     processor = SymbolicOverlayProcessor(shift_range=range(1, 6))
#     overlays = processor.process_image("sample_face.png", base_name="face")
#     print("Generated overlays:", overlays)
