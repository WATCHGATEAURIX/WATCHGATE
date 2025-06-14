# watchgate_vision/temporal_visualizer.py
# ----------------------------------------
# Module 11: Temporal Anomaly Visualizer
# Creates visual timelines or heatmaps showing symbolic resonance and discontinuities across frames

import os
import json
import matplotlib.pyplot as plt

class TemporalVisualizer:
    def __init__(self):
        pass

    def load_log_sequence(self, log_dir: str) -> list:
        logs = []
        for fname in sorted(os.listdir(log_dir)):
            if fname.endswith(".json"):
                path = os.path.join(log_dir, fname)
                with open(path, 'r') as f:
                    logs.append(json.load(f))
        return logs

    def plot_entropy_timeline(self, logs: list, title: str = "Symbolic Entropy Over Time"):
        x = list(range(len(logs)))
        y = [log['entropy'] for log in logs]
        plt.figure(figsize=(10, 4))
        plt.plot(x, y, marker='o', color='orange')
        plt.title(title)
        plt.xlabel("Frame Index")
        plt.ylabel("Entropy")
        plt.grid(True)
        plt.tight_layout()
        plt.show()

    def plot_resonance_timeline(self, logs: list, title="Resonance Score Over Time"):
        x = list(range(len(logs)))
        y = [log.get("cosmic", {}).get("resonance_score", 0.0) for log in logs]
        plt.figure(figsize=(10, 4))
        plt.plot(x, y, marker='o', color='cyan')
        plt.title(title)
        plt.xlabel("Frame Index")
        plt.ylabel("Resonance Score")
        plt.grid(True)
        plt.tight_layout()
        plt.show()

# Example usage:
# viz = TemporalVisualizer()
# logs = viz.load_log_sequence("outpost_logs")
# viz.plot_entropy_timeline(logs)
# viz.plot_resonance_timeline(logs)
