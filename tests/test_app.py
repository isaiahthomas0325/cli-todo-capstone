from __future__ import annotations

import pytest

from todo_app.app import TodoApp
from todo_app.storage import TodoStorage


def make_app(tmp_path):
    return TodoApp(TodoStorage(tmp_path / "todos.json"))


def test_add_trims_text_and_assigns_incrementing_ids(tmp_path):
    app = make_app(tmp_path)

    first = app.add("  write tests  ")
    second = app.add("update README")

    assert first.id == 1
    assert first.text == "write tests"
    assert second.id == 2
    assert [todo.text for todo in app.list()] == ["write tests", "update README"]


def test_add_rejects_empty_text(tmp_path):
    app = make_app(tmp_path)

    with pytest.raises(ValueError, match="cannot be empty"):
        app.add("   ")


def test_complete_marks_only_requested_todo(tmp_path):
    app = make_app(tmp_path)
    first = app.add("one")
    second = app.add("two")

    completed = app.complete(second.id)

    todos = app.list()
    assert completed.completed is True
    assert todos[0] == first
    assert todos[1].completed is True


def test_complete_unknown_id_raises_lookup_error(tmp_path):
    app = make_app(tmp_path)
    app.add("existing")

    with pytest.raises(LookupError, match="No todo found with id 99"):
        app.complete(99)


def test_delete_removes_requested_todo(tmp_path):
    app = make_app(tmp_path)
    first = app.add("keep")
    second = app.add("remove")

    deleted = app.delete(second.id)

    assert deleted.text == "remove"
    assert app.list() == [first]


def test_list_active_filters_completed_todos(tmp_path):
    app = make_app(tmp_path)
    app.add("done")
    active = app.add("still active")
    app.complete(1)

    assert app.list(include_completed=False) == [active]
