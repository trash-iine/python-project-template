# Repository Guidelines

## Project Structure & Module Organization
- `src/sample_project/` holds the package and CLI entrypoint (`__main__.py`); core logic lives in `sample_add.py`.
- `test/` contains pytest suites; add new files as `test_*.py` alongside fixtures.
- `docs/` stores Sphinx sources (`docs/source/`) and make targets; built HTML lands under `docs/build/`.
- `tasks.py` defines Invoke helpers (docs, test, format, check); toolchain and lint rules are in `pyproject.toml`.

## Build, Test, and Development Commands
- Install deps: `uv sync --dev` (creates `.venv`; rerun after dependency changes).
- Run the app: `uv run python -m sample_project` or the console script `uv run sample-project`.
- Tests: `uv run pytest test` for the full suite; use `-k` to target specific cases.
- Lint/format: `uv run ruff check .` and `uv run ruff format .`.
- Invoke shortcuts: `uv run invoke test|check|format|docs` (wrappers around pytest, Ruff, and Sphinx).

## Coding Style & Naming Conventions
- Python 3.13; prefer explicit type hints for public functions.
- Ruff enforces style with line length 120; formatting via `ruff format` keeps imports and whitespace consistent.
- Modules and functions use `snake_case`; classes use `PascalCase`; tests follow `test_<unit>_<expectation>` naming.
- Keep docstrings concise with a one-line summary; mention exceptions raised when relevant.

## Testing Guidelines
- Use Pytest for unit coverage; favor parametrized cases for input pairs and error paths (e.g., TypeError on non-int input).
- Place new tests under `test/` mirroring source modules; keep tests hermetic (no network or external FS writes).
- Run `uv run pytest test` before submitting; add focused runs (`-k`, `--maxfail=1`) during development to speed feedback.

## Commit & Pull Request Guidelines
- History uses short, present-tense messages with emoji prefixes (e.g., `🎉 init`, `🚧 add invoke`); follow the same concise style (<=72 chars).
- Reference related issues/PRs in the body when applicable.
- Before opening a PR: ensure `ruff check` and `pytest` pass; include a brief summary of changes and commands executed.
- For doc or CLI output changes, add screenshots or sample command output in the PR description when helpful.
