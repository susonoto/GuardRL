import json
from pathlib import Path
from threading import Lock

DATA = Path("data")
DATA.mkdir(exist_ok=True)
_lock = Lock()

def append_jsonl(name: str, item: dict):
    with _lock, (DATA / name).open("a", encoding="utf-8") as f:
        f.write(json.dumps(item, default=str) + "\\n")

def read_jsonl(name: str) -> list[dict]:
    path = DATA / name
    if not path.exists():
        return []
    with _lock, path.open(encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]

def read_json(name: str, default):
    path = DATA / name
    if not path.exists():
        return default
    with _lock, path.open(encoding="utf-8") as f:
        return json.load(f)

def write_json(name: str, value):
    with _lock, (DATA / name).open("w", encoding="utf-8") as f:
        json.dump(value, f, indent=2, default=str)
