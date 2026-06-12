from __future__ import annotations

import json
from pathlib import Path

from .models import Todo


class TodoStorage:
    """JSON-file persistence for todos."""

    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)

    def load(self) -> list[Todo]:
        if not self.path.exists():
            return []

        try:
            raw_data = json.loads(self.path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            raise ValueError(f"Todo file is not valid JSON: {self.path}") from exc

        if not isinstance(raw_data, list):
            raise ValueError("Todo file must contain a JSON list")

        return [Todo.from_dict(item) for item in raw_data]

    def save(self, todos: list[Todo]) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        payload = [todo.to_dict() for todo in todos]
        self.path.write_text(
            json.dumps(payload, indent=2) + "\n",
            encoding="utf-8",
        )
