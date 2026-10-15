# GuardRL
### Human-approved security log anomaly detection and IP response

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](#requirements)
[![Status](https://img.shields.io/badge/status-educational%20prototype-orange.svg)](#project-status)

GuardRL is an open-source educational starter for a defensive security workflow: ingest authorized logs, extract event features, score unusual behavior, recommend an action, and require an employee's approval before recording a proposed IP block.

**It does not currently block traffic on a real firewall.** Approved actions go to a local simulated block list. This is deliberate: real enforcement needs authenticated identity, role-based access control, change management, allowlists, expiry, rollback, and deployment-specific adapters.

> **Project status:** prototype / learning project, not production-ready. The included Isolation Forest is initialized from synthetic baseline data. Do not interpret demo scores as calibrated probabilities or claim a detection accuracy from them.

## Contents

- [What it does](#what-it-does)
- [Why human approval](#why-human-approval)
- [Architecture](docs/ARCHITECTURE.md)
- [Installation options](docs/SETUP.md)
- [API usage](docs/API.md)
- [ML and reinforcement-learning concepts](docs/ML_CONCEPTS.md)
- [Metrics, accuracy, and evaluation](docs/EVALUATION.md)
- [Threat model and safety](docs/THREAT_MODEL.md)
- [Comparisons](docs/COMPARISON.md)
- [Benefits and impact](docs/IMPACT.md)
- [Roadmap](docs/ROADMAP.md)
- [Contributing](CONTRIBUTING.md)
- [Code of conduct](CODE_OF_CONDUCT.md)
- [Security reporting](SECURITY.md)
- [Glossary](docs/GLOSSARY.md)

## What it does

1. Accepts a structured log event over a FastAPI endpoint.
2. Extracts features such as HTTP status, failed-login indicator, path length/entropy, bytes sent, and recent event count for a source IP.
3. Produces an anomaly score using an Isolation Forest model.
4. Maps the score to `monitor`, `investigate`, or `propose_block`.
5. For a block proposal, records an employee's decision and reason.
6. Records an approved IP in a **simulated** block list and writes an audit event.
7. Uses approval/rejection feedback to influence future high-risk recommendations through a small contextual-bandit-inspired policy.

The current feedback policy is intentionally simple. It is not a deep RL agent, does not learn a reliable causal model of attacks, and must never bypass human approval.

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate       # Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open <http://127.0.0.1:8000/docs> for interactive API docs.

For more options, including Docker, editable installs, and troubleshooting, see [docs/SETUP.md](docs/SETUP.md).

## Example event

Use synthetic events or logs from systems you are authorized to monitor. The following uses a documentation-only IP address:

```json
{
  "timestamp": "2026-10-15T06:00:00Z",
  "src_ip": "198.51.100.42",
  "username": "demo-user",
  "event_type": "login_failed",
  "status_code": 401,
  "path": "/login",
  "user_agent": "ExampleClient/1.0",
  "bytes_sent": 420
}
```

Send it to `POST /logs`. Inspect the returned alert. If its recommendation is `propose_block`, submit a decision to `POST /alerts/{alert_id}/decision`. See [docs/API.md](docs/API.md) for exact requests.

## Accuracy: what can honestly be claimed?

**No genuine accuracy percentage is established by this repository.** There is no representative, independently labeled test set and no measured precision/recall report. A score from an Isolation Forest is an anomaly score, not the probability an event is malicious. The synthetic baseline exists only so the demo can run.

To report meaningful results, evaluate on a time-separated, representative dataset with reviewed labels. Report precision, recall, false-positive rate, PR-AUC, alert volume, detection delay, and confidence intervals. Document dataset coverage and class imbalance. See [docs/EVALUATION.md](docs/EVALUATION.md).

## License

MIT. See [LICENSE](LICENSE). Dependencies retain their own licenses; review them before redistribution or commercial deployment.

## Disclaimer

This project is for defensive security research, education, and authorized environments. It is provided without warranty. Do not use it to monitor systems without authorization or automatically disrupt production traffic. See [docs/THREAT_MODEL.md](docs/THREAT_MODEL.md).
