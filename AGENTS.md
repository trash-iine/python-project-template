# Repository Guidelines

This repository contains the `sample-project` Python package.

`CONTRIBUTING.md` (Japanese) is the canonical contributor guide; this file is its English digest for AI agents. On conflict, `CONTRIBUTING.md` and `pyproject.toml` win.

<!-- template-only-start -->
It is also a Python project template (published as `trash-iine/python-project-template`): the `new-project` Invoke task copies and rebrands the whole repo into a new project directory.
<!-- template-only-end -->

## Project Structure & Module Organization
- `src/sample_project/` holds the package and CLI entrypoint (`__main__.py`); core logic lives in `sample_add.py`; `py.typed` marks the package as typed (PEP 561).
- `test/` contains pytest suites; add new files as `test_*.py` alongside fixtures.
- `docs/` stores Sphinx sources (`docs/source/`) and make targets; built HTML lands under `docs/build/` (build artifact, not tracked).
- `tasks.py` defines Invoke helpers (docs, test, format, check, update-apidoc); toolchain and lint rules are in `pyproject.toml`.
- `template_tasks.py` holds the template-only `new-project` task and helpers (tested in `test/test_template_tasks.py`); both files are excluded from generated projects via `COPY_EXCLUDES`. <!-- template-only-line -->
- `.github/` holds CI (`workflows/tests.yml`), the docs deploy (`workflows/docs.yml`), PR/issue templates, `CODEOWNERS`, and Dependabot config; `.gitlab-ci.yml` mirrors CI and Pages for GitLab.

## Language Policy
- Code, identifiers, comments, docstrings, and commit messages: English.
- User-facing docs (`README.md`, prose pages under `docs/source/`), PR/MR descriptions, and review comments: Japanese.

## Build, Test, and Development Commands
- Install deps: `uv sync --dev` (creates `.venv`; rerun after dependency changes). Run everything through `uv run <command>`.
- Enable git hooks once: `uv run pre-commit install` (fast auto-fixing hooks only — Ruff and file hygiene; ty/pytest stay in CI).
- Run the app: `uv run python -m sample_project` or the console script `uv run sample-project`.
- Tests: `uv run pytest` for the full suite (includes doctests from `src/` and a coverage report); use `-k` to target specific cases.
- Lint/format: `uv run ruff check .` and `uv run ruff format .`.
- Type check: `uv run ty check`.
- Invoke shortcuts: `uv run invoke test|check|format|docs|update-apidoc` (wrappers around pytest, Ruff, and Sphinx).
- Scaffold a new project from this template: `uv run invoke new-project -d <dir>` (the project name defaults to the basename of `<dir>`; supports `-p/--project-name`, `--author`, `--remote-url`, `--no-git`, and `--dry-run`). <!-- template-only-line -->
- CI requires all of `ruff check`, `ruff format --check`, `ty check`, and `pytest` to pass — run them locally before pushing. CI additionally audits dependencies with `pip-audit` (weekly schedule on GitHub Actions).

## Coding Style & Naming Conventions
- Python 3.13; prefer explicit type hints for public functions.
- Ruff enforces style with line length 120; formatting via `ruff format` keeps imports and whitespace consistent.
- Modules and functions use `snake_case`; classes use `PascalCase`; tests follow `test_<unit>_<expectation>` naming.
- Keep docstrings concise with a one-line summary; mention exceptions raised when relevant, and prefer a doctest-style `Examples:` section for public functions.
- `pyproject.toml` is the single source of truth for lint rules (Ruff `select = ["ALL"]`); never bypass rules except via a reasoned `# noqa: <RULE>` or a commented `per-file-ignores` entry.
- Raise exceptions via a message variable (`msg = "..."` then `raise TypeError(msg)`, per EM101/EM102); see `src/sample_project/sample_add.py` for the reference docstring and `Examples:` style.

## Testing Guidelines
- Use Pytest for unit coverage; favor parametrized cases for input pairs and error paths (e.g., TypeError on non-int input).
- Place new tests under `test/` mirroring source modules; keep tests hermetic (no network or external FS writes).
- Docstring `Examples:` sections are executed as doctests (`--doctest-modules`); keep them runnable.
- Coverage is reported by `pytest-cov`; no gate is set in the template — enable the commented `fail_under` in `pyproject.toml` once the codebase grows.
- Run `uv run pytest` before submitting; add focused runs (`-k`, `--maxfail=1`) during development to speed feedback.

## Documentation
- Docs are built with Sphinx + MyST (Markdown) + nbsphinx (notebooks); build locally with `uv run invoke docs` (HTML lands in `docs/build/html/`).
- The root `README.md` is the single source of truth for setup and usage instructions — do not duplicate setup steps under `docs/`; `docs/source/` holds the API reference and writing-format examples only.
- After adding or renaming modules in `src/`, run `uv run invoke update-apidoc` to regenerate the API reference (`docs/source/*.rst`).
- New doc pages go in `docs/source/` and must be added to the `{toctree}` in `docs/source/index.md`.
- Pushes to `main` deploy the built docs to GitHub Pages (or GitLab Pages) automatically.

## Commit & Pull Request Guidelines
- History uses short, present-tense messages with emoji prefixes (e.g., `🎉 init`, `🚧 add invoke`); follow the same concise style (<=72 chars).
- Never commit directly to `main`; branch as `<type>/<short-kebab-description>` where type is one of `feature|fix|docs|refactor|test|ci|chore`, matching the gitmoji of the eventual commits.
- Reference related issues/PRs in the body when applicable.
- When development rules change, update `CONTRIBUTING.md` and this file in the same PR.
- Before opening a PR: ensure `ruff check`, `ruff format --check`, `ty check`, and `pytest` pass; include a brief summary of changes and commands executed.
- For doc or CLI output changes, add screenshots or sample command output in the PR description when helpful.
