# Accuracy, metrics, and honest evaluation

## No verified accuracy number is available

This repository does not include a representative, labeled benchmark dataset or a completed evaluation report. Therefore, it would be misleading to state that GuardRL is “95% accurate” or provide any genuine accuracy claim.

The starter model's synthetic baseline makes the demo executable. It is not evidence of real-world detection performance. The score is a relative anomaly indicator and is not a calibrated probability that an event is malicious.

## Confusion matrix

For a chosen threshold and labeled test set:

| | Predicted positive | Predicted negative |
|---|---:|---:|
| Actually positive | True positive (TP) | False negative (FN) |
| Actually negative | False positive (FP) | True negative (TN) |

Definitions:

- **Accuracy** = `(TP + TN) / (TP + TN + FP + FN)`
- **Precision** = `TP / (TP + FP)` — of alerts raised, how many were true positives?
- **Recall / TPR** = `TP / (TP + FN)` — of known attacks, how many were detected?
- **Specificity / TNR** = `TN / (TN + FP)`
- **False-positive rate (FPR)** = `FP / (FP + TN)`
- **F1** = `2 × precision × recall / (precision + recall)`
- **Balanced accuracy** = `(TPR + TNR) / 2`

If any denominator is zero, report the metric as undefined rather than silently replacing it with zero.

## Why accuracy alone can mislead

Suppose only 1 in 1,000 events is malicious. A detector that labels every event benign has 99.9% accuracy but detects no attacks. For security operations, precision, recall, FPR, alert volume, and time-to-detect are often more useful.

## Recommended evaluation protocol

1. Collect authorized events and define a clear labeling policy.
2. Remove secrets and minimize personal data.
3. Split data by time, not just randomly, to reduce leakage from repeated sessions and near-duplicate events.
4. Train only on a baseline appropriate to the model's assumptions.
5. Tune thresholds on a validation set; keep the final test set untouched.
6. Compare against simple baselines: fixed rules, rate thresholds, and a majority-class baseline.
7. Report precision, recall, FPR, PR-AUC, ROC-AUC where useful, alerts per day, detection delay, and analyst review time.
8. Evaluate by event type, source system, and environment to find blind spots.
9. Include confidence intervals or repeated time windows where practical.
10. Run in shadow mode before any enforcement.

## Precision-recall formulas

Let precision be P and recall be R:

**F1 = 2PR / (P + R)**

Precision-recall curves are especially useful for imbalanced datasets because they show the trade-off between finding more attacks and flooding analysts with false alerts. PR-AUC must be computed from scores and labels on a held-out dataset.

## Operational metrics

- **Alert rate:** alerts / time period
- **False alerts per day:** false-positive alerts per 24 hours
- **Mean time to detect (MTTD):** average time between attack start and detection
- **Mean time to acknowledge (MTTA):** average time from alert creation to analyst acknowledgement
- **Mean time to respond (MTTR):** define locally; often time to contain or remediate
- **Block reversal rate:** percentage of approved blocks later reverted as mistaken or unnecessary

## Reporting template

```text
Dataset source / permission:
Date range:
Number of events:
Number of labeled malicious events:
Labeling process:
Train / validation / test split:
Baseline:
Model version and features:
Threshold:
Precision:
Recall:
False-positive rate:
PR-AUC:
Alerts per day:
Detection delay:
Known limitations:
Reviewer:
```

Never invent or extrapolate a result from a demo. Publish numbers only with a reproducible method, data provenance, and limitations.
