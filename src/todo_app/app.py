from __future__ import annotations

from .models import Todo
from .storage import TodoStorage


class TodoApp:
    """Core todo actions independent from command-line formatting."""

    def __init__(self, storage: TodoStorage) -> None:
        self.storage = storage

    def add(self, text: str) -> Todo:
        clean_text = text.strip()
        if not clean_text:
            raise ValueError("Todo text cannot be empty")

        todos = self.storage.load()
        next_id = max((todo.id for todo in todos), default=0) + 1
        todo = Todo(id=next_id, text=clean_text)
        self.storage.save([*todos, todo])
        return todo

    def list(self, include_completed: bool = True) -> list[Todo]:
        todos = self.storage.load()
        if include_completed:
            return todos
        return [todo for todo in todos if not todo.completed]

    def complete(self, todo_id: int) -> Todo:
        todos = self.storage.load()
        updated: list[Todo] = []
        completed_todo: Todo | None = None

        for todo in todos:
            if todo.id == todo_id:
                completed_todo = todo.mark_complete()
                updated.append(completed_todo)
            else:
                updated.append(todo)

        if completed_todo is None:
            raise LookupError(f"No todo found with id {todo_id}")

        self.storage.save(updated)
        return completed_todo

    def delete(self, todo_id: int) -> Todo:
        todos = self.storage.load()
        remaining = [todo for todo in todos if todo.id != todo_id]

        if len(remaining) == len(todos):
            raise LookupError(f"No todo found with id {todo_id}")

        deleted = next(todo for todo in todos if todo.id == todo_id)
        self.storage.save(remaining)
        return deleted
