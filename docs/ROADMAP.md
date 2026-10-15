# Roadmap and future features

This roadmap is aspirational; it is not a promise that every feature will be implemented.

## Stage 0 — Starter (current)
- FastAPI ingestion endpoint
- Feature extraction and Isolation Forest demo
- Feedback-count recommendation policy
- Employee decision endpoint (identity is not yet authenticated)
- Simulated IP block list and local audit JSONL
- Starter tests and documentation

## Stage 1 — Reliability
- Durable database and alert state recovery
- Structured logging and configuration validation
- Unit/integration test coverage
- Reproducible model artifact loading and versioning
- Better schema normalization and rate limiting

## Stage 2 — Evaluation
- Public or synthetic benchmark fixtures with clear licenses
- Dataset versioning and data quality checks
- Time-based splits, PR curves, calibration research, and threshold selection
- False-positive analysis by source, event type, and asset criticality
- Drift and alert-volume dashboards

## Stage 3 — Analyst experience
- Web dashboard for alert queue and event context
- SSO/OIDC authentication and RBAC
- Approval reasons, case/ticket integration, and reviewer history
- Evidence summaries and explainability
- Accessibility and keyboard-first workflows

## Stage 4 — Integrations
- Syslog and common structured log formats
- SIEM and case-management connectors
- Threat-intelligence enrichment with provenance and expiry
- Firewall adapters behind feature flags and dry-run mode
- Block TTL, allowlists, idempotency, rollback, and health checks

## Stage 5 — Safe learning
- A proper contextual-bandit experiment in a simulator
- Explicit state/action/reward definitions reviewed by security operators
- Counterfactual/off-policy evaluation where valid
- Reward sensitivity analysis and safety constraints
- Human-approved, versioned policy promotion with rollback

## Stage 6 — Production hardening
- Threat modeling and independent security review
- Secrets management and least-privilege deployment
- Tamper-resistant audit storage
- Load tests, resilience tests, disaster recovery
- Privacy review, retention policy, and operational runbooks

## Non-goals

- Autonomous blocking without approval as a default
- Claiming universal or guaranteed detection accuracy
- Replacing a SOC analyst or a full SIEM
- Treating an IP address as conclusive identity
