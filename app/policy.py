from collections import defaultdict

class FeedbackPolicy:
    \"\"\"Tiny contextual-bandit-inspired recommendation tuner.

    It learns aggregate outcomes by risk band and action. This is intentionally
    conservative: feedback can change recommendations, never bypass approval.
    \"\"\"
    def __init__(self):
        self.stats = defaultdict(lambda: {"approve": 0, "reject": 0})

    def recommend(self, score: float) -> str:
        if score < 0.35:
            return "monitor"
        if score < 0.70:
            return "investigate"
        band = "high"
        s = self.stats[band]
        # If prior high-risk proposals are often rejected, recommend investigation.
        total = s["approve"] + s["reject"]
        if total >= 5 and s["reject"] / total > 0.5:
            return "investigate"
        return "propose_block"

    def feedback(self, score: float, decision: str):
        band = "high" if score >= .70 else "medium" if score >= .35 else "low"
        self.stats[band][decision] += 1

    def snapshot(self):
        return {k: dict(v) for k, v in self.stats.items()}
