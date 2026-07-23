"""Template-only Invoke tasks for scaffolding new projects.

Everything specific to the project-template workflow lives here (the
``new-project`` task and its helpers). This module and its tests are
excluded from the copy when a new project is generated, so derived
projects never contain template-only code.
"""

import re
import shutil
from datetime import UTC, datetime
from pathlib import Path

from invoke import task

from tasks import PROJECT_NAME, _derive_module_name

TEMPLATE_AUTHOR = "Trash-iine"
TEMPLATE_AUTHOR_SLUG = "trash-iine"
COPY_EXCLUDES = {"uv.lock", "template_tasks.py", "test/test_template_tasks.py", ".claude/skills/new-project/SKILL.md"}
STRIP_MARKER_FILES = {"tasks.py", "CODEOWNERS"}
TEMPLATE_ONLY_START = "template-only-start"
TEMPLATE_ONLY_END = "template-only-end"
TEMPLATE_ONLY_LINE = "template-only-line"


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
        if file in COPY_EXCLUDES:
            continue
        src_path = src / file
        dest_path = dest / file
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src_path, dest_path)


def _resolve_author(c, author: str) -> str:
    """Resolve the author name from the option or git config.

    Args:
        c: Invoke context.
        author (str): Author name given on the command line (may be empty).

    Returns:
        str: The resolved author name.

    Raises:
        ValueError: If no author name can be resolved.

    """
    if author:
        return author

    result = c.run("git config user.name", warn=True, hide=True)
    if result.ok and result.stdout.strip():
        return result.stdout.strip()

    msg = "Author name is required. Pass --author or set git config user.name."
    raise ValueError(msg)


def _strip_template_sections(text: str) -> str:
    """Remove template-only lines and blocks marked with template-only comments.

    Args:
        text (str): The original text.

    Returns:
        str: The text without template-only lines and blocks.

    """
    lines = []
    in_block = False
    for line in text.splitlines(keepends=True):
        if TEMPLATE_ONLY_START in line:
            in_block = True
            continue
        if TEMPLATE_ONLY_END in line:
            in_block = False
            continue
        if in_block or TEMPLATE_ONLY_LINE in line:
            continue
        lines.append(line)
    stripped = "".join(lines)
    if stripped == text or not stripped.strip():
        return stripped
    # Removing a block at EOF leaves the blank lines that preceded it;
    # trim them so formatters do not flag the generated file.
    return stripped.rstrip("\n") + "\n"


def _should_strip_template(path: Path) -> bool:
    """Return whether template-only markers should be stripped from the file.

    Args:
        path (Path): Path of the file being rewritten.

    Returns:
        bool: True if template-only sections should be removed.

    """
    return path.suffix == ".md" or path.name in STRIP_MARKER_FILES


def _rewrite_text(data: str, new_project: str, author: str, *, strip_template: bool) -> str:
    """Apply all rebranding replacements to a file's content.

    Args:
        data (str): The original file content.
        new_project (str): The new project name.
        author (str): The new author name.
        strip_template (bool): Whether template-only sections are stripped.

    Returns:
        str: The rebranded content.

    """
    module_name = _derive_module_name(PROJECT_NAME)
    new_module = _derive_module_name(new_project)

    updated = _strip_template_sections(data) if strip_template else data
    year = datetime.now(tz=UTC).year
    updated = re.sub(
        rf'copyright = "\d{{4}}, {re.escape(TEMPLATE_AUTHOR)}"',
        f'copyright = "{year}, {author}"',
        updated,
    )
    updated = re.sub(
        rf"Copyright \(c\) \d{{4}} {re.escape(TEMPLATE_AUTHOR)}",
        f"Copyright (c) {year} {author}",
        updated,
    )
    updated = updated.replace(TEMPLATE_AUTHOR, author)
    updated = updated.replace(TEMPLATE_AUTHOR_SLUG, author)
    return updated.replace(PROJECT_NAME, new_project).replace(module_name, new_module)


def _replace_in_repo(
    c,
    repo_root: Path,
    new_project: str,
    author: str,
    *,
    dry_run: bool,
) -> None:
    old_root = Path(__file__).resolve().parent

    files = _list_git_files(c)
    for file in files:
        if file in COPY_EXCLUDES:
            continue
        path = old_root / file if dry_run else repo_root / file
        if path.is_dir():
            continue
        try:
            data = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue

        updated = _rewrite_text(data, new_project, author, strip_template=_should_strip_template(path))

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


def _regenerate_lock(c, repo_root: Path, *, dry_run: bool = False) -> None:
    if dry_run:
        print(f"[dry-run] regenerate lock file: {repo_root / 'uv.lock'}")
        return

    with c.cd(str(repo_root)):
        result = c.run("uv lock", warn=True)
    if result.failed:
        print("Warning: 'uv lock' failed. Run 'uv sync --dev' in the new project to regenerate it.")


def _init_git_repo(
    c,
    repo_root: Path,
    remote_url: str,
    *,
    dry_run: bool = False,
) -> None:
    if dry_run:
        print(f"[dry-run] git init + initial commit: {repo_root}")
        if remote_url:
            print(f"[dry-run] set git remote origin: {remote_url}")
        return

    with c.cd(str(repo_root)):
        c.run("git init")
        c.run("git add -A")
        c.run('git commit -m "🎉 init"')
        if remote_url:
            c.run(f"git remote add origin {remote_url}")


@task
def new_project(
    c,
    dest: str,
    project_name: str = "",
    remote_url: str = "",
    author: str = "",
    *,
    git: bool = True,
    dry_run: bool = False,
) -> None:
    """Copy this repo to dest and rebrand it as a new project.

    If project_name is omitted, the basename of dest is used.
    """
    repo_root = Path(__file__).resolve().parent
    dest_path = Path(dest).expanduser().resolve()

    if dest_path.exists():
        msg = f"Destination path already exists: {dest_path}"
        raise RuntimeError(msg)

    project_name = project_name or dest_path.name
    _derive_module_name(project_name)  # fail fast on invalid names before copying
    author = _resolve_author(c, author)

    if dry_run:
        print(f"[dry-run] would copy: {repo_root} -> {dest_path}")
    else:
        _copy_project_tree(c, dest_path)

    _replace_in_repo(c, dest_path, project_name, author, dry_run=dry_run)
    _rebrand_project(dest_path, project_name, dry_run=dry_run)
    _regenerate_lock(c, dest_path, dry_run=dry_run)
    if git:
        _init_git_repo(c, dest_path, remote_url, dry_run=dry_run)
