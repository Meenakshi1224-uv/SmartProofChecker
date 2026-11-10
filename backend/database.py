import json
from pathlib import Path
from datetime import datetime
from typing import Any, Dict, List

BASE_DIR = Path(__file__).resolve().parent
HISTORY_FILE = BASE_DIR / "proof_history.json"


def _read_history() -> List[Dict[str, Any]]:
    if not HISTORY_FILE.exists():
        return []
    try:
        data = json.loads(HISTORY_FILE.read_text(encoding="utf-8"))
        if isinstance(data, list):
            return data
    except (json.JSONDecodeError, OSError):
        pass
    return []


def _write_history(history: List[Dict[str, Any]]) -> None:
    HISTORY_FILE.write_text(json.dumps(history, indent=2), encoding="utf-8")


def add_history_entry(statement: str, method: str, answer: Any = None, steps: List[str] | None = None) -> Dict[str, Any]:
    history = _read_history()
    entry = {
        "statement": str(statement).strip(),
        "method": str(method).strip() or "direct",
        "answer": answer,
        "steps": steps or [],
        "created_at": datetime.utcnow().isoformat(timespec="seconds") + "Z"
    }
    history.insert(0, entry)
    _write_history(history[:50])
    return entry


def get_history(limit: int = 20) -> List[Dict[str, Any]]:
    return _read_history()[:limit]


def clear_history() -> None:
    _write_history([])
