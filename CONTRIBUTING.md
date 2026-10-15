# Contributing to GuardRL

Contributions are welcome. This project is an educational defensive-security prototype; prioritize correctness, explainability, safe defaults, privacy, and documentation.

## Before starting

1. Read `README.md`, `docs/THREAT_MODEL.md`, and `docs/EVALUATION.md`.
2. Search existing issues before opening a new one.
3. For significant changes, open an issue or discussion first.
4. Never submit real credentials, customer logs, private IP inventories, or personal data.

## Development setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install pytest
pytest -q
uvicorn app.main:app --reload
```

## Contribution workflow

1. Fork the repository and create a focused branch.
2. Make the smallest coherent change.
3. Add tests for new behavior and regression cases.
4. Update relevant documentation and examples.
5. Run tests and check formatting/linting if configured.
6. Open a pull request with motivation, design, testing, risks, and any migration notes.

## What makes a good contribution?

- Robust schema validation and timestamp normalization
- Unit and integration tests
- Better dataset evaluation tooling and reproducible reports
- Safer persistence and durable alert lifecycle
- Verified authentication and server-side role checks
- Explainability and analyst feedback quality
- Privacy-preserving redaction and retention controls
- Accessible review dashboard
- Documented SIEM integrations using test fixtures
- Model drift and threshold monitoring

## Safety requirements for pull requests

- The model must not bypass employee approval.
- No real firewall changes should be enabled by default.
- New enforcement integrations need explicit opt-in, least-privilege design, dry-run mode, TTL, allowlists, audit records, and rollback.
- Do not add secrets to source control.
- Avoid claims of accuracy unless supported by reproducible evaluation on a documented held-out dataset.
- Do not submit exploit code or features intended to disrupt third-party systems.

## Pull request checklist

- [ ] Tests added or updated
- [ ] `pytest -q` passes
- [ ] Docs and examples updated
- [ ] No secrets or sensitive logs included
- [ ] Security and privacy impact considered
- [ ] Accuracy/performance claims backed by measurements
- [ ] No silent change to approval or enforcement behavior

## License

By contributing, you agree that your contributions are submitted under the project's MIT license, unless clearly stated otherwise.
