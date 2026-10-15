# API reference

Run `uvicorn app.main:app --reload`, then use <http://127.0.0.1:8000/docs>.

## `GET /`

Returns project name, simulation mode, and approval status.

## `POST /logs`

Submit one event:

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

The response contains `alert_id`, `anomaly_score`, `recommendation`, `status`, and the event. The score is not a probability.

## `GET /alerts`

Returns alerts in the current process memory.

## `GET /alerts/{alert_id}`

Returns one alert.

## `POST /alerts/{alert_id}/decision`

Only alerts with a `propose_block` recommendation accept decisions.

```json
{
  "employee_id": "analyst-001",
  "decision": "approve",
  "reason": "Validated repeated failed logins",
  "ticket_id": "SOC-1024"
}
```

Allowed decisions: `approve`, `reject`. A decision is one-time per alert. In this prototype, `employee_id` is not authenticated; production must derive the identity from a verified session/token.

Approval writes a simulated record to `data/blocks.json`; it does not block network traffic.

## `GET /blocks`

Lists simulated block records.

## `GET /audit`

Returns local audit events.

## `GET /policy`

Shows feedback counts by risk band.

## Example with curl

```bash
curl -X POST http://127.0.0.1:8000/logs \
  -H 'Content-Type: application/json' \
  -d '{"timestamp":"2026-10-15T06:00:00Z","src_ip":"198.51.100.42","username":"demo","event_type":"login_failed","status_code":401,"path":"/login","user_agent":"ExampleClient/1.0","bytes_sent":420}'
```

Use the returned alert ID in the decision endpoint. A particular event may not be classified as `propose_block`; this is expected because the model score is heuristic and synthetic. Test the workflow through the API docs rather than assuming every sample will produce a block proposal.
