# Approach comparison

These are qualitative trade-offs, not benchmark results. Actual outcomes depend on data quality, implementation, threat model, and operations.

| Approach | Strengths | Weaknesses | Best use |
|---|---|---|---|
| Static rules | Transparent, quick, low compute | Brittle; rules need maintenance; may miss novel patterns | Known indicators and policy violations |
| Rate limits / thresholds | Simple, explainable, efficient | Legitimate traffic spikes can trigger; distributed behavior may evade | Brute-force and volumetric controls |
| Supervised classifier | Can optimize for labeled attack classes | Needs trustworthy labels; vulnerable to dataset shift | Well-labeled, recurring detection tasks |
| Isolation Forest | Can surface unusual points without attack labels | Scores can be noisy; baseline and feature quality matter | Triage and novelty detection |
| Deep sequence model | Can capture temporal patterns | More data/compute and harder explanation | Mature teams with extensive telemetry |
| Human analyst only | Contextual judgment and accountability | Slow, costly, inconsistent under alert fatigue | High-context decisions and escalation |
| GuardRL prototype | Combines anomaly scoring, recommendation, feedback, approval gate | Early prototype; synthetic baseline; no real firewall adapter; no verified metrics | Education, prototyping, and workflow experiments |

## Compared with a fully automatic blocker

GuardRL's approval gate reduces the chance that a single noisy model score directly disrupts a service. It also introduces review latency and depends on reviewer quality and availability. A production system may use different approval tiers based on asset criticality and confidence, but should never silently remove the approval gate.

## Compared with a full RL system

The current policy is a transparent feedback-count heuristic, not deep RL. This is easier to inspect and safer for a starter project. A true RL approach would require a carefully defined state/action/reward model, safe simulation, off-policy evaluation, drift handling, and strict action constraints. It should not be adopted merely because RL sounds more advanced.
