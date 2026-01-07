# watchgate_vision/seed_tracker.py
# ----------------------------------
# Module 5: SEED Tracker
# Tracks symbolic signature recurrence and builds a symbolic memory ledger for WATCHGATE

import os
import json
import hashlib
from typing import Dict, List

class SymbolicSeedTracker:
    def __init__(self, ledger_path="symbolic_ledger.json"):
        self.ledger_path = ledger_path
        self.ledger = self.load_ledger()

    def load_ledger(self) -> Dict:
        if os.path.exists(self.ledger_path):
            with open(self.ledger_path, 'r') as f:
                return json.load(f)
        return {}

    def save_ledger(self):
        with open(self.ledger_path, 'w') as f:
            json.dump(self.ledger, f, indent=2)

    def generate_symbolic_hash(self, entropy: float, fft_peaks: List[float]) -> str:
        combined = f"{round(entropy, 5)}:" + ",".join([str(round(v, 3)) for v in fft_peaks])
        return hashlib.sha256(combined.encode()).hexdigest()

    def register_signature(self, image_path: str, entropy: float, fft_peaks: List[float]) -> str:
        symbolic_hash = self.generate_symbolic_hash(entropy, fft_peaks)
        if symbolic_hash not in self.ledger:
            self.ledger[symbolic_hash] = {
                "instances": [image_path],
                "entropy": round(entropy, 5),
                "fft_peaks": [round(f, 5) for f in fft_peaks],
                "count": 1
            }
        else:
            self.ledger[symbolic_hash]["instances"].append(image_path)
            self.ledger[symbolic_hash]["count"] += 1

        self.save_ledger()
        return symbolic_hash

    def get_known_signatures(self) -> List[str]:
        return list(self.ledger.keys())

    def query_by_hash(self, symbolic_hash: str) -> Dict:
        return self.ledger.get(symbolic_hash, {})

# Example usage:
# tracker = SymbolicSeedTracker()
# hash = tracker.register_signature("b1_25.png", 4.561, [1.2e4, 8.9e3, 7.1e3])
# print("Seed hash:", hash)
