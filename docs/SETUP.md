# Installation and setup guide

## Requirements

- Python 3.10 or newer
- pip
- Git (optional, for cloning)
- Docker + Docker Compose (optional)
- Linux, macOS, or Windows are suitable for development

## Option A — Standard virtual environment

```bash
git clone <your-fork-or-repository-url>
cd guardrl
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Windows PowerShell activation:

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open <http://127.0.0.1:8000/docs>. Stop the server with Ctrl+C.

## Option B — Docker

A Dockerfile is included.

```bash
docker build -t guardrl:dev .
docker run --rm -p 8000:8000 -v guardrl-data:/app/data guardrl:dev
```

Open <http://127.0.0.1:8000/docs>. The named volume keeps demo data between container runs.

## Option C — Docker Compose

```bash
docker compose up --build
```

To stop:

```bash
docker compose down
```

The app is exposed on port 8000. Do not expose this development configuration to the public internet.

## Option D — Editable development install

This is useful when adding modules and tests. The project is currently a simple source tree and can be run directly; an editable package configuration can be added as the package matures.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install pytest
pytest -q
uvicorn app.main:app --reload
```

## Option E — Run tests

```bash
pip install pytest
pytest -q
```

Tests are intentionally minimal starter checks, not a complete assurance suite.

## Configuration

Copy `.env.example` to `.env` for local configuration notes. Current code uses conservative hard-coded demo behavior for several settings; do not assume every example environment variable is wired into runtime behavior yet.

## Troubleshooting

### `uvicorn: command not found`
Activate the virtual environment and run `python -m pip install -r requirements.txt`, then `python -m uvicorn app.main:app --reload`.

### Port 8000 is already in use
Run `uvicorn app.main:app --reload --port 8001`, then open port 8001.

### Import errors
Run the command from the repository root (the directory containing `app/`) with the virtual environment active.

### Data looks empty after restart
The current alert dictionary is in memory, while JSONL records are persisted. This prototype does not reload the in-memory alert workflow from disk at startup. A production implementation should use a database and durable alert-state transitions.

### Windows shell activation is blocked
Use an approved Python environment, or run `.venv\Scripts\python.exe -m uvicorn app.main:app --reload` after installing dependencies with that interpreter.

## Safe first run

Use the documentation IP range `198.51.100.0/24` and synthetic events. Review the returned score as a demo signal only; do not use it as a production block decision.
