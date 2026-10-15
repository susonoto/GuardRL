# Security policy

## Scope

GuardRL is a prototype and should not be deployed as a production security control. Security reports are welcome for the repository code, data handling, approval workflow, and documented deployment patterns.

## Reporting a vulnerability

Please report vulnerabilities privately to the repository maintainers using the host platform's private vulnerability reporting feature, if enabled. Include impact, reproduction steps, affected version, and suggested mitigation. Do not publish sensitive data or test against systems you do not own or have authorization to assess.

## Response expectations

Maintainers should acknowledge reports when practical, assess severity, coordinate a fix, and publish a concise advisory after a fix is available. This project has no guaranteed response SLA.

## Safe deployment reminders

- Do not expose the unauthenticated prototype to the internet.
- Do not provide the detector with production firewall credentials.
- Use synthetic data in demos.
- Require verified identity, authorization, audit, expiry, and rollback before enforcement.
