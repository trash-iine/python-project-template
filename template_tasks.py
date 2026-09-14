"""新プロジェクトを生成するテンプレート専用の Invoke タスク。

プロジェクトテンプレートのワークフローに固有のもの (``new-project`` タスクと
その補助関数) はすべてここに置く。このモジュールとそのテストは新プロジェクト
生成時のコピー対象から除外されるため、派生プロジェクトにテンプレート専用の
コードが残ることはない。
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
    """git が追跡しているファイルを列挙する。

    Args:
        c (Context): Invoke のコンテキスト。

    Returns:
        list[str]: カレントディレクトリからの相対パスのリスト。

    """
    result = c.run("git ls-files", hide=True)
    return result.stdout.splitlines()


def _copy_project_tree(c, dest: Path) -> None:
    """このリポジトリのファイルツリーを dest にコピーする。

    Args:
        c (Context): Invoke のコンテキスト。
        dest (Path): 新プロジェクトの生成先パス。

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
    """著者名をオプションまたは git config から解決する。

    Args:
        c (Context): Invoke のコンテキスト。
        author (str): コマンドラインで指定された著者名 (空文字可)。

    Returns:
        str: 解決した著者名。

    Raises:
        ValueError: 著者名を解決できない場合。

    """
    if author:
        return author

    result = c.run("git config user.name", warn=True, hide=True)
    if result.ok and result.stdout.strip():
        return result.stdout.strip()

    msg = "Author name is required. Pass --author or set git config user.name."
    raise ValueError(msg)


def _strip_template_sections(text: str) -> str:
    """template-only マーカーで囲まれたブロックと行を取り除く。

    Args:
        text (str): 元のテキスト。

    Returns:
        str: テンプレート専用のブロックと行を取り除いたテキスト。

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
    # ファイル末尾のブロックを取り除くとその直前の空行が残るため、
    # 生成ファイルがフォーマッタに弾かれないように末尾の空行を詰める。
    return stripped.rstrip("\n") + "\n"


def _should_strip_template(path: Path) -> bool:
    """template-only マーカーの除去対象ファイルかどうかを返す。

    Args:
        path (Path): 書き換え対象ファイルのパス。

    Returns:
        bool: テンプレート専用セクションを取り除くべきなら True。

    """
    return path.suffix == ".md" or path.name in STRIP_MARKER_FILES


def _rewrite_text(data: str, new_project: str, author: str, *, strip_template: bool) -> str:
    """ファイル内容にリブランドの置換をすべて適用する。

    Args:
        data (str): 元のファイル内容。
        new_project (str): 新しいプロジェクト名。
        author (str): 新しい著者名。
        strip_template (bool): テンプレート専用セクションを取り除くかどうか。

    Returns:
        str: リブランド後の内容。

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
    """追跡中の全テキストファイルでプロジェクト名・著者・テンプレートマーカーを書き換える。

    Args:
        c (Context): Invoke のコンテキスト。
        repo_root (Path): コピー先プロジェクトのルート。
        new_project (str): 新しいプロジェクト名。
        author (str): 新しい著者名。
        dry_run (bool): True なら変更対象ファイルの表示のみ行う。

    """
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
    """ソースパッケージと API リファレンスページを新しいモジュール名にリネームする。

    Args:
        repo_root (Path): コピー先プロジェクトのルート。
        new_project (str): 新しいプロジェクト名。
        dry_run (bool): True ならリネーム内容の表示のみ行う。

    """
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
    """新プロジェクトで uv.lock を再生成する。

    Args:
        c (Context): Invoke のコンテキスト。
        repo_root (Path): コピー先プロジェクトのルート。
        dry_run (bool): True なら再生成対象の表示のみ行う。

    """
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
    """git リポジトリを初期化し、初回コミットと (指定があれば) リモート登録を行う。

    Args:
        c (Context): Invoke のコンテキスト。
        repo_root (Path): コピー先プロジェクトのルート。
        remote_url (str): origin として登録するリモート URL。空文字なら登録しない。
        dry_run (bool): True なら実行する git 操作の表示のみ行う。

    """
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
    """このリポジトリを dest にコピーし、新プロジェクトとしてリブランドする。

    Args:
        c (Context): Invoke のコンテキスト。
        dest (str): 生成先ディレクトリ。未存在であること。
        project_name (str): 新しいプロジェクト名。省略時は dest のベース名。
        remote_url (str): origin として登録するリモート URL。空文字なら登録しない。
        author (str): 著者名。省略時は `git config user.name` から解決する。
        git (bool): True なら git init と初回コミットを行う。
        dry_run (bool): True なら処理内容の表示のみ行う。

    Raises:
        RuntimeError: dest が既に存在する場合。

    """
    repo_root = Path(__file__).resolve().parent
    dest_path = Path(dest).expanduser().resolve()

    if dest_path.exists():
        msg = f"Destination path already exists: {dest_path}"
        raise RuntimeError(msg)

    project_name = project_name or dest_path.name
    _derive_module_name(project_name)  # 無効な名前はコピー前に弾く
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
