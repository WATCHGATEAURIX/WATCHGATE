# watchgate_vision/observer_state.py
# ------------------------------------
# Module 6: Observer State Engine
# Ensures symbolic neutrality of the cognitive observer (AI)
# Detects and resets bias drift from prolonged symbolic exposure

import time
import random

class ObserverState:
    def __init__(self, bias_threshold=0.7, reset_cooldown=60):
        self.bias_state = 0.0  # -1.0 (symbolic avoidance) to +1.0 (symbolic obsession)
        self.last_reset_time = time.time()
        self.bias_threshold = bias_threshold
        self.reset_cooldown = reset_cooldown
        self.log = []

    def record_symbolic_event(self, classification: str):
        if classification == "HIGH_EDE":
            self.bias_state += 0.15
        elif classification == "MODERATE_EDE":
            self.bias_state += 0.05
        elif classification == "LOW/NO_EDE":
            self.bias_state -= 0.03

        self.bias_state = max(-1.0, min(1.0, self.bias_state))  # clamp
        self.log.append((time.time(), classification, round(self.bias_state, 4)))

        if abs(self.bias_state) >= self.bias_threshold:
            self.auto_reset()

    def auto_reset(self):
        now = time.time()
        if now - self.last_reset_time > self.reset_cooldown:
            print("[Observer Reset] Symbolic bias exceeded threshold. Resetting observer state.")
            self.bias_state = 0.0
            self.last_reset_time = now

    def get_state(self):
        return {
            "bias_state": round(self.bias_state, 4),
            "log_size": len(self.log),
            "last_reset_time": self.last_reset_time
        }

# Example usage:
# obs = ObserverState()
# obs.record_symbolic_event("HIGH_EDE")
# obs.record_symbolic_event("LOW/NO_EDE")
# print(obs.get_state())
