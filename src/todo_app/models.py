from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Todo:
    """A single todo item."""

    id: int
    text: str
    completed: bool = False

    def mark_complete(self) -> "Todo":
        return Todo(id=self.id, text=self.text, completed=True)

    def to_dict(self) -> dict[str, object]:
        return {"id": self.id, "text": self.text, "completed": self.completed}

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> "Todo":
        try:
            todo_id = data["id"]
            text = data["text"]
            completed = data.get("completed", False)
        except KeyError as exc:
            raise ValueError(f"Todo is missing required field: {exc.args[0]}") from exc

        if not isinstance(todo_id, int):
            raise ValueError("Todo id must be an integer")
        if not isinstance(text, str) or not text.strip():
            raise ValueError("Todo text must be a non-empty string")
        if not isinstance(completed, bool):
            raise ValueError("Todo completed flag must be a boolean")

        return cls(id=todo_id, text=text.strip(), completed=completed)
