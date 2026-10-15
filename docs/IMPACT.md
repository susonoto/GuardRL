# Benefits, limitations, and potential impact

## Potential benefits

- **Earlier triage:** unusual activity can be ranked for analyst attention.
- **More consistent workflow:** every proposed block can require a reason and decision.
- **Reduced repetitive work:** common log patterns can be surfaced automatically.
- **Auditability:** decision records support post-incident review when protected correctly.
- **Learning opportunity:** combines defensive security, API engineering, anomaly detection, and safe automation.
- **Extensibility:** the architecture can later accept SIEM, identity, case-management, and firewall adapters.

These are potential benefits, not measured results from this prototype.

## Expected operational impact

The value of a detection system depends on more than model scores. It also depends on alert precision, alert volume, integration effort, analyst trust, time to response, and the cost of false positives.

A useful pilot should compare a baseline period with a shadow-mode period and measure:
- number of alerts reviewed per day;
- percentage of alerts analysts confirm;
- time from event to acknowledgement;
- repeated false-positive categories;
- number of proposed blocks rejected;
- user and service disruption avoided;
- operational hours saved, if any.

## Risks and unintended consequences

- False positives may interrupt legitimate users if connected to enforcement.
- Shared IP addresses, carrier NAT, VPNs, and proxies can make IP attribution ambiguous.
- Attackers can adapt behavior to evade features.
- Training data can encode historical bias or blind spots.
- A compromised approval account can authorize harmful changes.
- Logs may contain credentials, personal data, or sensitive URLs.
- A poorly designed reward may incentivize overblocking or underreporting.

## Impact principles

1. Keep the system advisory until evidence supports a controlled rollout.
2. Make decisions explainable enough for analysts to challenge.
3. Minimize and protect log data.
4. Measure errors and report limitations honestly.
5. Keep rollback and expiry available for any future enforcement.
6. Do not treat IP address as definitive identity.
