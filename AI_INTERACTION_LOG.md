# AI Interaction Log

## Interaction 1: Project Setup

- Prompt: "Create a Python project structure for a CLI todo app with separate files for models, storage, application logic, and the CLI interface. Keep it standard-library only at runtime."
- Agent Output: Proposed `src/todo_app/` with `models.py`, `storage.py`, `app.py`, and `cli.py`, plus a `tests/` directory and `README.md`.
- My Review: I checked that the design met the capstone requirement for at least three Python files and that the responsibilities were separated clearly.
- Result: Accepted with one modification: I chose JSON storage because it is simple to inspect and easy to test.

## Interaction 2: SCOPE Prompt for Core Feature

- Prompt: "Specific context: I need a capstone-sized Python CLI todo app for a beginner-friendly agent course. Constraints: use only the standard library at runtime, split code across multiple files, persist todos as JSON, and handle empty text and missing IDs cleanly. Output format: provide code for model, storage, app service, and CLI files. Purpose: demonstrate a complete agent-assisted development lifecycle with readable code and tests. Examples: `add \"write tests\"` should create todo `1. [ ] write tests`; `complete 1` should display `1. [x] write tests`; deleting an unknown ID should return a clear error."
- Agent Output: Created the core `Todo`, `TodoStorage`, `TodoApp`, and argparse CLI implementations.
- My Review: I verified that the prompt included all SCOPE elements: specific context, constraints, output format, purpose, and examples. I reviewed the code for over-complexity and kept the API small.
- Result: Modified slightly by keeping command formatting in `cli.py` instead of mixing it into the core app logic.

## Interaction 3: Testing

- Prompt: "Write pytest tests for normal inputs, edge cases, and error conditions. Cover add/list/complete/delete, empty todo text, missing files, invalid JSON, and CLI error output."
- Agent Output: Added tests across `test_app.py`, `test_storage.py`, and `test_cli.py`.
- My Review: I checked that the tests assert behavior rather than implementation details. I added coverage for active-only filtering because it is user-facing behavior.
- Result: Accepted after expanding the storage tests to reject both invalid JSON and non-list JSON.

## Interaction 4: Bug Fix and Review

- Prompt: "The app should not crash with a traceback when the user deletes or completes a missing todo. Return a clean CLI error and a non-zero status instead."
- Agent Output: Wrapped `LookupError` and `ValueError` in `cli.run()` and returned exit status `1` with a concise error message.
- My Review: I checked that the core app still raises meaningful exceptions for tests and that only the CLI turns them into user-facing text.
- Result: Accepted because the boundary between application behavior and CLI presentation stayed clean.

## Interaction 5: Documentation

- Prompt: "Write a README explaining what the project does, how to run it, basic usage examples, tests, and project structure. Also include a short reflection suitable for a capstone submission."
- Agent Output: Created README sections for features, setup, usage, tests, and capstone notes.
- My Review: I ensured the README commands use `PYTHONPATH=src` or `python3 -m todo_app.cli` from the project root so the app runs without packaging steps.
- Result: Modified to keep the language concise and focused on what a grader needs to verify.

## Reflection

The most effective prompt was the SCOPE prompt in Interaction 2 because it gave the agent the project context, boundaries, expected file-level output, purpose, and concrete command examples. That reduced ambiguity and made the first implementation close to the final shape.

The hardest part of directing the agent was balancing small scope with enough completeness for meaningful testing. Next time I would define the storage format and CLI command examples even earlier so every later prompt can refer back to the same contract.

At the start of the course, I thought agents were mainly code generators. Now I understand they are more useful as iterative collaborators when I provide constraints, review output carefully, run tests, and refine prompts based on what the project needs.
