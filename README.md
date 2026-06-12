# My CLI Todo App

A small persistent command-line todo list built for the Agent Proficiency capstone. It lets users add, list, complete, and delete tasks while storing data in a JSON file.

## Features

- Add todos with automatic numeric IDs
- List all todos or only active todos
- Mark todos complete
- Delete todos by ID
- Store todos in a user-selected JSON file
- Validate empty todo text, missing IDs, and malformed storage files

## Project Structure

```text
src/todo_app/
  app.py       Core todo operations
  cli.py       argparse command-line interface
  models.py    Todo data model and validation
  storage.py   JSON file persistence
tests/         pytest coverage for app, storage, and CLI behavior
```

## Setup

This project uses only the Python standard library at runtime. Pytest is required for tests.

```bash
python3 -m pip install pytest
```

## Usage

Run commands from the project root:

```bash
PYTHONPATH=src python3 -m todo_app.cli --file todos.json add "Finish capstone"
PYTHONPATH=src python3 -m todo_app.cli --file todos.json list
PYTHONPATH=src python3 -m todo_app.cli --file todos.json complete 1
PYTHONPATH=src python3 -m todo_app.cli --file todos.json delete 1
```

If `--file` is omitted, the app uses the `TODO_FILE` environment variable or `~/.cli_todo_capstone.json`.

## Run Tests

```bash
PYTHONPATH=src pytest
```

## Capstone Notes

The app is intentionally modest in scope so the lifecycle is easy to review: plan the structure, implement the core behavior, add tests, fix edge cases, and document the process.
