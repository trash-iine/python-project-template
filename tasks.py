"""Task definitions using Invoke."""

import shutil
import sys
from pathlib import Path

from invoke import task

PROJECT_NAME = "sample-project"


def check_env(c):
    """Check if the development environment is set up."""
    result = c.run("test -d ./.venv", warn=True)
    if result.ok:
        return

    # check if uv is installed
    uv_check = c.run("command -v uv", warn=True)
    if uv_check.failed:
        print("Error: 'uv' is not installed. Please install 'uv' first.")
        sys.exit(1)

    print("Run: 'uv sync --dev' to set up the development environment.")
    c.run("uv sync --dev")


def activate_env(c):
    """Activate the development environment."""
    check_env(c)
    c.run(". ./.venv/bin/activate")


@task
def docs(c, output="html"):
    """Build the documentation."""
    activate_env(c)
    c.run(f"make -C docs {output}", warn=True)


@task
def test(c):
    """Run the test suite."""
    activate_env(c)
    c.run("pytest test", pty=True)


@task
def format(c, target="."):
    """Run the formatter."""
    activate_env(c)
    c.run(f"ruff format {target}", pty=True)


@task
def check(c, target="."):
    """Run the linter."""
    activate_env(c)
    c.run(f"ruff check {target}", pty=True)


def _derive_module_name(project_name: str) -> str:
    """Derive a valid Python module name from a project name.

    Args:
        project_name (str): The new project name.

    Returns:
        str: The derived module name.

    Raises:
        ValueError: If the module name is invalid.

    """
    module_name = project_name.lower().replace("-", "_").replace(" ", "_")

    if not module_name:
        msg = "module_name is required."
        raise ValueError(msg)
    if not module_name.replace("_", "").isalnum() or module_name[0].isdigit():
        msg = f"Invalid module name: {module_name}"
        raise ValueError(msg)

    return module_name


@task
def update_module(c):
    """Update automodule directives in docs."""
    activate_env(c)
    module_name = _derive_module_name(PROJECT_NAME)
    c.run(f"sphinx-apidoc -f -o docs/source/ src/{module_name}", pty=True)


def _list_git_files(c) -> list[str]:
    """List all files tracked by git in the given directory.

    Args:
        c: Invoke context.

    Returns:
        list[str]: A list of file paths relative to cwd.

    """
    result = c.run("git ls-files", hide=True)
    return result.stdout.splitlines()


def _copy_project_tree(c, dest: Path) -> None:
    """Copy the project tree from src to dest.

    Args:
        c: Invoke context.
        dest (Path): Destination path of the new project.

    """
    src = Path(__file__).resolve().parent

    files = _list_git_files(c)
    for file in files:
        src_path = src / file
        dest_path = dest / file
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src_path, dest_path)


def _replace_in_repo(
    c,
    repo_root: Path,
    new_project: str,
    *,
    dry_run: bool,
) -> None:
    module_name = _derive_module_name(PROJECT_NAME)
    new_module = _derive_module_name(new_project)

    old_root = Path(__file__).resolve().parent

    files = _list_git_files(c)
    for file in files:
        path = old_root / file if dry_run else repo_root / file
        if path.is_dir():
            continue
        try:
            data = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue

        updated = data.replace(PROJECT_NAME, new_project).replace(module_name, new_module)
        if path.as_posix().endswith("docs/source/conf.py"):
            updated = updated.replace('author = "Trash-iine"', "")
            updated = updated.replace('copyright = "2025, Trash-iine"', "")

        if updated == data:
            continue

        if dry_run:
            print(f"[dry-run] update: {path}")
        else:
            path.write_text(updated, encoding="utf-8")


def _rebrand_project(repo_root: Path, new_project: str, *, dry_run: bool) -> None:
    module_name = _derive_module_name(PROJECT_NAME)
    new_module = _derive_module_name(new_project)

    src_module = repo_root / "src" / module_name
    dst_module = repo_root / "src" / new_module

    src_doc = repo_root / "docs" / "source" / f"{module_name}.rst"
    dst_doc = repo_root / "docs" / "source" / f"{new_module}.rst"

    if src_module != dst_module:
        if dry_run:
            print(f"[dry-run] rename: {src_module} -> {dst_module}")
        else:
            src_module.rename(dst_module)

    if src_doc != dst_doc:
        if dry_run:
            print(f"[dry-run] rename: {src_doc} -> {dst_doc}")
        else:
            src_doc.rename(dst_doc)


def _set_git_remote(
    c,
    repo_root: Path,
    remote_url: str,
    *,
    dry_run: bool = False,
) -> None:
    if not remote_url:
        return

    if dry_run:
        print(f"[dry-run] set git remote origin: {remote_url}")
        return

    c.run("git init", cwd=str(repo_root))
    c.run(f"git remote add origin {remote_url}", cwd=str(repo_root))


@task
def new_project(
    c,
    dest: str,
    project_name: str,
    remote_url: str = "",
    *,
    dry_run: bool = False,
) -> None:
    """Copy this repo to dest and rebrand it as a new project."""
    repo_root = Path(__file__).resolve().parent
    dest_path = Path(dest).expanduser().resolve()

    if dest_path.exists():
        msg = f"Destination path already exists: {dest_path}"
        raise RuntimeError(msg)

    if dry_run:
        print(f"[dry-run] would copy: {repo_root} -> {dest_path}")
    else:
        _copy_project_tree(c, dest_path)

    _replace_in_repo(c, dest_path, project_name, dry_run=dry_run)

    _rebrand_project(dest_path, project_name, dry_run=dry_run)
    _set_git_remote(c, dest_path, remote_url, dry_run=dry_run)
