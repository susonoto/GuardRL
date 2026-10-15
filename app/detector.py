import math
from collections import Counter
import numpy as np
from sklearn.ensemble import IsolationForest

def path_entropy(path: str) -> float:
    if not path:
        return 0.0
    counts = Counter(path)
    n = len(path)
    return -sum((v/n) * math.log2(v/n) for v in counts.values())

def event_features(event: dict, ip_counts: Counter | None = None) -> list[float]:
    status = event.get("status_code") or 0
    event_type = str(event.get("event_type", "")).lower()
    failed = 1.0 if ("fail" in event_type or status in (401, 403)) else 0.0
    suspicious_status = 1.0 if status in (401, 403, 429, 500, 503) else 0.0
    ip = str(event.get("src_ip", ""))
    count = (ip_counts or Counter()).get(ip, 0)
    path = str(event.get("path", "/"))
    ua = str(event.get("user_agent", "unknown"))
    return [
        failed,
        suspicious_status,
        min(count, 100),
        min(len(path), 500),
        path_entropy(path),
        min(len(ua), 500),
        min(int(event.get("bytes_sent") or 0), 10_000_000) / 10_000,
        1.0 if path.lower().startswith(("/admin", "/.env", "/wp-admin", "/etc")) else 0.0,
    ]

class AnomalyDetector:
    def __init__(self):
        rng = np.random.default_rng(17)
        # Synthetic baseline only; replace with clean, representative organizational logs.
        baseline = []
        for _ in range(500):
            baseline.append([
                float(rng.random() < .04),
                float(rng.random() < .06),
                float(rng.integers(0, 5)),
                float(rng.integers(5, 80)),
                float(rng.uniform(1.5, 4.5)),
                float(rng.integers(10, 100)),
                float(rng.uniform(0, 20)),
                float(rng.random() < .01),
            ])
        self.model = IsolationForest(n_estimators=150, contamination=0.05, random_state=17)
        self.model.fit(np.asarray(baseline))
        self.low, self.high = -0.25, 0.15

    def score(self, features: list[float]) -> float:
        # IsolationForest decision_function: lower means more anomalous.
        raw = float(self.model.decision_function([features])[0])
        return max(0.0, min(1.0, (self.high - raw) / (self.high - self.low)))
