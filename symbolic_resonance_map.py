# watchgate_vision/symbolic_resonance_map.py
# --------------------------------------------
# Module 10: Symbolic Resonance Map
# Builds and updates a global symbolic field intensity map from repeated overlay analysis results

import numpy as np
from collections import defaultdict

class SymbolicResonanceMap:
    def __init__(self):
        self.map = defaultdict(list)  # key: symbolic_hash, value: [resonance scores]

    def register_observation(self, symbolic_hash: str, resonance_score: float):
        self.map[symbolic_hash].append(resonance_score)

    def get_average_resonance(self, symbolic_hash: str) -> float:
        scores = self.map.get(symbolic_hash, [])
        if not scores:
            return 0.0
        return round(float(np.mean(scores)), 4)

    def get_map_summary(self, top_n=10):
        summary = sorted(
            [(h, self.get_average_resonance(h), len(self.map[h])) for h in self.map],
            key=lambda x: x[1], reverse=True
        )
        return summary[:top_n]

# Example usage:
# srm = SymbolicResonanceMap()
# srm.register_observation("abc123", 0.72)
# srm.register_observation("abc123", 0.81)
# print("Avg:", srm.get_average_resonance("abc123"))
# print("Summary:", srm.get_map_summary())
