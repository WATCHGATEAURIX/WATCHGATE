# watchgate_vision/outpost_node.py
# ----------------------------------
# Module 8: AURIX Outpost Node Interface
# Lightweight symbolic scanner node for remote deployment (IoT camera, Pi, drone, etc)

import os
import time
from symbolic_overlay import SymbolicOverlayProcessor
from fractal_analyzer import FractalAnalyzer
from ede_detector import EDEDetector
from intent_classifier import IntentClassifier
from symbolic_ethics import SymbolicEthicsFilter

class OutpostNode:
    def __init__(self, input_dir="node_frames", output_dir="outpost_logs"):
        self.input_dir = input_dir
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

        self.overlay_processor = SymbolicOverlayProcessor()
        self.analyzer = FractalAnalyzer()
        self.ede = EDEDetector(analyzer=self.analyzer)
        self.intent = IntentClassifier()
        self.ethics = SymbolicEthicsFilter()

    def scan(self):
        """
        Scan all images in input_dir, perform overlay + symbolic classification.
        """
        print("[OutpostNode] Scanning directory:", self.input_dir)
        for file in sorted(os.listdir(self.input_dir)):
            if not file.lower().endswith(('.png', '.jpg', '.jpeg')):
                continue

            input_path = os.path.join(self.input_dir, file)
            print(f"[+] Processing {file}...")
            overlays = self.overlay_processor.process_image(input_path, base_name=file[:-4])

            for shift, overlay_path in overlays:
                analysis = self.analyzer.analyze_image(overlay_path)
                classification = self.ede.classify_event(
                    entropy_delta=analysis['entropy'],
                    fft_delta=sum(analysis['fft_peaks'])
                )
                intent = self.intent.classify_intent(
                    entropy_delta=analysis['entropy'],
                    fft_delta=sum(analysis['fft_peaks'])
                )
                ethics_result = self.ethics.assess_risk_profile(
                    entropy_delta=analysis['entropy'],
                    fft_delta=sum(analysis['fft_peaks']),
                    classification=classification,
                    intent=intent,
                    notes=f"from node: {file}"
                )

                log = {
                    "input_frame": file,
                    "overlay_shift": shift,
                    "entropy": analysis['entropy'],
                    "fft": analysis['fft_peaks'],
                    "classification": classification,
                    "intent": intent,
                    "ethics": ethics_result
                }

                log_path = os.path.join(self.output_dir, f"{file[:-4]}_shift{shift}.json")
                with open(log_path, "w") as f:
                    import json
                    json.dump(log, f, indent=2)

                print(f"[-] Saved log to {log_path}")

# Example run:
# if __name__ == "__main__":
#     node = OutpostNode()
#     node.scan()
