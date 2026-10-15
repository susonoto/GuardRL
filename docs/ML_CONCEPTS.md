# ML, reinforcement learning, and formulas

This document introduces the concepts used by GuardRL and explains which are implemented versus planned.

## 1. Log event

A log event is a record of an observed action or state change. Example: a login attempt, HTTP request, privilege change, or process launch. Events should include reliable timestamps, source identity, event type, and context where permitted.

## 2. Feature engineering

Raw strings are not usually fed directly into a classical anomaly model. Feature engineering converts events into numeric variables, for example:

- `failed_login`: 1 when the event suggests a failed login, else 0
- `suspicious_status`: 1 for selected HTTP error/status codes, else 0
- `recent_ip_count`: recent event count for that source
- `path_length`: length of requested path
- `path_entropy`: diversity of characters in the path
- `bytes_sent`: scaled number of response bytes
- `sensitive_path_hint`: 1 for paths matching selected sensitive-path patterns

A feature vector is written as:

**x = [x₁, x₂, …, xₙ]**

Features can encode legitimate activity too. A long path or many requests is not inherently malicious; context and evaluation matter.

## 3. Shannon entropy

For character probabilities pᵢ in a string, Shannon entropy is:

**H(X) = −Σᵢ pᵢ log₂(pᵢ)**

Higher entropy often means characters are more varied. It can help describe encoded or random-looking paths, but it is not a malware detector by itself. In this starter, entropy is computed over path characters.

## 4. Anomaly detection

An anomaly detector identifies events or patterns that differ from a learned baseline. Anomaly does not equal attack. New software deployments, scanners, crawlers, and unusual but valid users can all look anomalous.

### Isolation Forest

Isolation Forest isolates observations using randomly selected features and split points. Unusual points are often isolated in fewer splits than typical points.

The score exposed by scikit-learn's `decision_function` is not a probability. The demo applies a simple linear mapping to create a bounded display score. That mapping is not calibrated and should not be called “probability of attack.”

## 5. Supervised classification versus anomaly detection

- **Supervised classification:** learns from labeled examples such as `benign` and `malicious`. Quality depends on labels and coverage.
- **Unsupervised / semi-supervised anomaly detection:** learns structure in baseline data, often with limited labels. It can surface novel behavior but may create many false positives.
- **Rules:** easy to explain and effective for known patterns, but can be brittle or easy to evade.
- **Hybrid:** combines rules, anomaly scores, threat context, and analyst review.

## 6. Reinforcement learning (RL)

Reinforcement learning studies how an agent chooses actions in an environment to maximize cumulative reward. Standard notation:

- **State s:** current context, e.g. event features, recent behavior, asset criticality.
- **Action a:** an allowed recommendation, e.g. monitor or investigate.
- **Reward r:** feedback after an action, designed to reward useful outcomes and penalize mistakes.
- **Policy π(a|s):** rule/model selecting an action for a state.
- **Return Gₜ:** discounted future rewards, often `Gₜ = Σₖ₌₀∞ γᵏ rₜ₊ₖ₊₁`.
- **Discount γ:** number between 0 and 1 controlling the value of future reward.

A common objective is:

**π* = arg maxπ Eπ[Σₜ γᵗ rₜ₊₁]**

Reward design is critical. If a system is rewarded only for catching attacks, it may block too aggressively. False blocks must carry a substantial cost, and policy updates need offline evaluation and safety constraints.

## 7. Contextual bandit

A contextual bandit observes a context, chooses an action, then receives feedback for that action. Unlike full RL, it generally does not model long state transitions. The starter's policy is only “bandit-inspired”: it tracks approve/reject counts by risk band and changes a recommendation under a simple condition. It is not a statistically rigorous contextual-bandit implementation.

## 8. A safety-aware reward example (conceptual only)

A possible reward for offline simulation could be:

**R = +5·TP − 20·FP − 2·FN − 0.1·C**

Where:
- TP = correctly escalated malicious event
- FP = benign event incorrectly escalated or blocked
- FN = malicious event missed
- C = operational cost, such as analyst minutes

These numbers are illustrative, not validated. The penalty for a false block may need to be much larger for critical services. Do not use this formula directly in production without stakeholder review.

## 9. Human-in-the-loop

Human-in-the-loop means a person reviews or authorizes a consequential decision. It helps add context and accountability, but only when the reviewer has enough evidence, can reject a recommendation, and their identity and reason are audited. Approval can still be mistaken, so add limits, expiry, allowlists, and rollback.

## 10. Conceptual separation

Detection answers “does this look unusual?” Policy answers “what should we recommend?” Approval answers “is this action authorized?” Enforcement answers “what system change is made?” Keep these stages separate so a model error cannot directly trigger a high-impact action.
