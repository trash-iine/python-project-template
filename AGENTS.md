# Repository Guidelines

This repository is a Python project template (`sample-project`, published as `trash-iine/python-project-template`). Besides serving as a small sample package, it provides a `new-project` Invoke task that copies and rebrands the whole repo into a new project directory.

## Project Structure & Module Organization
- `src/sample_project/` holds the package and CLI entrypoint (`__main__.py`); core logic lives in `sample_add.py`.
- `test/` contains pytest suites; add new files as `test_*.py` alongside fixtures.
- `docs/` stores Sphinx sources (`docs/source/`) and make targets; built HTML lands under `docs/build/` (build artifact, not tracked).
- `tasks.py` defines Invoke helpers (docs, test, format, check, update-apidoc, new-project); toolchain and lint rules are in `pyproject.toml`.
- `.github/workflows/` runs CI (`tests.yml`) and deploys docs to GitHub Pages (`docs.yml`).

## Build, Test, and Development Commands
- Install deps: `uv sync --dev` (creates `.venv`; rerun after dependency changes). Run everything through `uv run <command>`.
- Run the app: `uv run python -m sample_project` or the console script `uv run sample-project`.
- Tests: `uv run pytest test` for the full suite; use `-k` to target specific cases.
- Lint/format: `uv run ruff check .` and `uv run ruff format .`.
- Type check: `uv run ty check`.
- Invoke shortcuts: `uv run invoke test|check|format|docs|update-apidoc` (wrappers around pytest, Ruff, and Sphinx).
- Scaffold a new project from this template: `uv run invoke new-project -p <name> -d <dir>` (supports `--dry-run`).
- CI requires all of `ruff check`, `ruff format --check`, `ty check`, and `pytest` to pass — run them locally before pushing.

## Coding Style & Naming Conventions
- Python 3.13; prefer explicit type hints for public functions.
- Ruff enforces style with line length 120; formatting via `ruff format` keeps imports and whitespace consistent.
- Modules and functions use `snake_case`; classes use `PascalCase`; tests follow `test_<unit>_<expectation>` naming.
- Keep docstrings concise with a one-line summary; mention exceptions raised when relevant, and prefer a doctest-style `Examples:` section for public functions.

## Testing Guidelines
- Use Pytest for unit coverage; favor parametrized cases for input pairs and error paths (e.g., TypeError on non-int input).
- Place new tests under `test/` mirroring source modules; keep tests hermetic (no network or external FS writes).
- Run `uv run pytest test` before submitting; add focused runs (`-k`, `--maxfail=1`) during development to speed feedback.

## Documentation
- Docs are built with Sphinx + MyST (Markdown) + nbsphinx (notebooks); build locally with `uv run invoke docs` (HTML lands in `docs/build/html/`).
- The root `README.md` is the single source of truth for setup and usage instructions — do not duplicate setup steps under `docs/`; `docs/source/` holds the API reference and writing-format examples only.
- After adding or renaming modules in `src/`, run `uv run invoke update-apidoc` to regenerate the API reference (`docs/source/*.rst`).
- New doc pages go in `docs/source/` and must be added to the `{toctree}` in `docs/source/index.md`.
- Pushes to `main` deploy the built docs to GitHub Pages automatically.

## Commit & Pull Request Guidelines
- History uses short, present-tense messages with emoji prefixes (e.g., `🎉 init`, `🚧 add invoke`); follow the same concise style (<=72 chars).
- Reference related issues/PRs in the body when applicable.
- Before opening a PR: ensure `ruff check`, `ruff format --check`, `ty check`, and `pytest` pass; include a brief summary of changes and commands executed.
- For doc or CLI output changes, add screenshots or sample command output in the PR description when helpful.
