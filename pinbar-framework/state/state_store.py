# state/state_store.py
import json
from pathlib import Path

STATE_FILE = Path(__file__).parent / "state.json"


class StateStore:
    """Remembers which signals have already been alerted, so each
    candle fires at most one alert per strategy."""

    def __init__(self):
        self._data = {}
        if STATE_FILE.exists():
            try:
                self._data = json.loads(STATE_FILE.read_text())
            except (json.JSONDecodeError, OSError):
                self._data = {}

    def already_alerted(self, key: str, timestamp) -> bool:
        entry = self._data.get(key)
        if entry is None:
            return False
        return str(timestamp) == str(entry)

    def mark_alerted(self, key: str, timestamp) -> None:
        self._data[key] = str(timestamp)
        STATE_FILE.write_text(json.dumps(self._data, indent=2))
