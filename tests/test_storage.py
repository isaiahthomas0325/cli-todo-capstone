from __future__ import annotations

import pytest

from todo_app.models import Todo
from todo_app.storage import TodoStorage


def test_storage_loads_missing_file_as_empty_list(tmp_path):
    storage = TodoStorage(tmp_path / "missing.json")

    assert storage.load() == []


def test_storage_round_trips_todos(tmp_path):
    storage = TodoStorage(tmp_path / "todos.json")
    todos = [Todo(id=1, text="write docs"), Todo(id=2, text="ship", completed=True)]

    storage.save(todos)

    assert storage.load() == todos


def test_storage_rejects_invalid_json(tmp_path):
    path = tmp_path / "todos.json"
    path.write_text("{not json", encoding="utf-8")
    storage = TodoStorage(path)

    with pytest.raises(ValueError, match="not valid JSON"):
        storage.load()


def test_storage_rejects_non_list_json(tmp_path):
    path = tmp_path / "todos.json"
    path.write_text('{"id": 1}', encoding="utf-8")
    storage = TodoStorage(path)

    with pytest.raises(ValueError, match="must contain a JSON list"):
        storage.load()
