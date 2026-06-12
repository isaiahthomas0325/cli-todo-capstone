from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

from .app import TodoApp
from .models import Todo
from .storage import TodoStorage


DEFAULT_TODO_PATH = Path.home() / ".cli_todo_capstone.json"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Manage a persistent todo list.")
    parser.add_argument(
        "--file",
        default=os.environ.get("TODO_FILE", str(DEFAULT_TODO_PATH)),
        help="Path to the JSON todo file. Defaults to TODO_FILE or ~/.cli_todo_capstone.json.",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    add_parser = subparsers.add_parser("add", help="Add a new todo.")
    add_parser.add_argument("text", help="Todo text.")

    list_parser = subparsers.add_parser("list", help="List todos.")
    list_parser.add_argument(
        "--active",
        action="store_true",
        help="Only show todos that are not completed.",
    )

    complete_parser = subparsers.add_parser("complete", help="Mark a todo complete.")
    complete_parser.add_argument("id", type=int, help="Todo id to complete.")

    delete_parser = subparsers.add_parser("delete", help="Delete a todo.")
    delete_parser.add_argument("id", type=int, help="Todo id to delete.")

    return parser


def format_todo(todo: Todo) -> str:
    marker = "x" if todo.completed else " "
    return f"{todo.id}. [{marker}] {todo.text}"


def run(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    app = TodoApp(TodoStorage(args.file))

    try:
        if args.command == "add":
            todo = app.add(args.text)
            print(f"Added: {format_todo(todo)}")
        elif args.command == "list":
            todos = app.list(include_completed=not args.active)
            if not todos:
                print("No todos found.")
            else:
                for todo in todos:
                    print(format_todo(todo))
        elif args.command == "complete":
            todo = app.complete(args.id)
            print(f"Completed: {format_todo(todo)}")
        elif args.command == "delete":
            todo = app.delete(args.id)
            print(f"Deleted: {format_todo(todo)}")
    except (LookupError, ValueError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    return 0


def main() -> None:
    raise SystemExit(run())


if __name__ == "__main__":
    main()
