# watchgate_vision/narrative_reconstructor.py
# --------------------------------------------
# Module 13: Narrative Symbol Reconstructor
# Breaks down and reassembles symbolic components across data formats (text/image/video)

import re
from collections import defaultdict

class NarrativeSymbolReconstructor:
    def __init__(self):
        self.archetypes = [
            "hero", "villain", "sacrifice", "loss", "betrayal", "awakening",
            "war", "purification", "threshold", "ascension", "deception"
        ]
        self.symbols = defaultdict(int)  # symbolic keyword frequencies

    def extract_symbols_from_text(self, narrative: str) -> dict:
        tokens = re.findall(r"\b\w+\b", narrative.lower())
        matches = {arch: 0 for arch in self.archetypes}
        for word in tokens:
            for arch in self.archetypes:
                if arch in word:
                    matches[arch] += 1
        self.symbols.update(matches)
        return matches

    def summarize_symbolic_footprint(self) -> dict:
        return dict(sorted(self.symbols.items(), key=lambda x: x[1], reverse=True))

    def reconstruct_lineage(self, symbol: str) -> str:
        lineage_map = {
            "hero": "origin -> challenge -> transformation",
            "loss": "bond -> rupture -> meaning",
            "ascension": "awakening -> sacrifice -> rise",
            "deception": "masking -> manipulation -> collapse"
        }
        return lineage_map.get(symbol, "unknown -> tension -> repetition")

# Example usage:
# recon = NarrativeSymbolReconstructor()
# result = recon.extract_symbols_from_text("A hero suffers great loss during war, leading to ascension.")
# print(result)
# print(recon.reconstruct_lineage("ascension"))
