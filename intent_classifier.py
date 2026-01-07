# watchgate_vision/intent_classifier.py
# --------------------------------------
# Module 4: Intent Classifier
# Determines whether symbolic/fractal activity is spontaneous, planned, or anomalous based on entropy and FFT deltas

class IntentClassifier:
    def __init__(self, entropy_threshold=1.0, fft_threshold=1000.0):
        self.entropy_threshold = entropy_threshold
        self.fft_threshold = fft_threshold

    def classify_intent(self, entropy_delta: float, fft_delta: float) -> str:
        """
        Classifies the symbolic intent of a shift or anomaly
        Returns: 'SPONTANEOUS', 'PLANNED', 'UNCERTAIN'
        """
        if entropy_delta > self.entropy_threshold and fft_delta > self.fft_threshold:
            return "SPONTANEOUS"
        elif entropy_delta < self.entropy_threshold and fft_delta < self.fft_threshold:
            return "PLANNED"
        return "UNCERTAIN"

    def batch_classify(self, ede_results: list) -> list:
        """
        Accepts a list of EDE result dicts and assigns intent labels
        """
        for record in ede_results:
            record['intent'] = self.classify_intent(
                record.get('entropy_delta', 0.0),
                record.get('fft_delta', 0.0)
            )
        return ede_results

# Example usage:
# from ede_detector import EDEDetector
# ede = EDEDetector()
# results = ede.scan_sequence("symbolic_overlays")
# ic = IntentClassifier()
# classified = ic.batch_classify(results)
# for c in classified:
#     print(c)
