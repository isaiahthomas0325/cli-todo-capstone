from __future__ import annotations

from todo_app.cli import run


def test_cli_add_and_list_use_requested_file(tmp_path, capsys):
    todo_file = tmp_path / "todos.json"

    assert run(["--file", str(todo_file), "add", "buy milk"]) == 0
    assert run(["--file", str(todo_file), "list"]) == 0

    output = capsys.readouterr().out
    assert "Added: 1. [ ] buy milk" in output
    assert "1. [ ] buy milk" in output


def test_cli_returns_error_for_missing_todo(tmp_path, capsys):
    todo_file = tmp_path / "todos.json"

    exit_code = run(["--file", str(todo_file), "delete", "42"])

    captured = capsys.readouterr()
    assert exit_code == 1
    assert "No todo found with id 42" in captured.err
