# Threat model and safe operation

## Assets to protect

- Availability and integrity of monitored services
- Log confidentiality and integrity
- Reviewer identities and approval decisions
- Model artifacts and training data
- Audit records and any future firewall credentials

## Main threats

| Threat | Example | Mitigation |
|---|---|---|
| Forged approval | Caller submits someone else's employee ID | Verified SSO identity and server-side RBAC |
| Alert manipulation | Attacker floods endpoint with fake events | Authenticate log sources, validate schema, rate-limit, isolate ingestion |
| Data poisoning | Attacker pollutes baseline with malicious-looking normal data | Curated training sets, provenance, review, versioning |
| False-positive outage | Benign shared IP is blocked | Approval gate, asset-aware checks, allowlists, TTL, rollback |
| Audit tampering | Local JSON records are modified | Append-only remote storage, access control, integrity monitoring |
| Sensitive data leakage | Logs expose tokens or personal data | Redaction, minimization, encryption, retention limits |
| Model drift | Normal traffic changes after a release | Drift monitoring, shadow evaluation, rollback to versioned model |
| Privilege escalation | Detector process has firewall administrator rights | Separate enforcement service, least privilege, short-lived credentials |

## Current prototype limitations

- No authentication, SSO, RBAC, or CSRF protection.
- Employee ID is accepted as request data and is not verified.
- JSON files are not tamper-resistant or suitable for concurrent production workloads.
- In-memory alert state does not reload from disk after restart.
- Synthetic model baseline and score mapping are not validated.
- No real firewall integration, expiry, allowlist, or rollback.
- No comprehensive load, security, or adversarial testing.

**Do not expose the API to the public internet or connect it to a production firewall in its current form.**

## Production approval controls

Before real enforcement, require:
- identity provider authentication and role checks;
- MFA or step-up authentication for sensitive actions;
- reviewer reason and ticket reference;
- allowlist / protected asset checks;
- block duration and automatic expiry;
- idempotency and duplicate handling;
- two-person approval where risk warrants it;
- change record and immutable audit trail;
- rollback workflow and tested emergency access;
- monitoring, alerting, and fail-safe behavior.

## Responsible use

Only collect or process logs you are authorized to access. Follow applicable law, contracts, organizational policy, and privacy requirements. Do not use the project to attack, disrupt, or monitor systems without authorization.
