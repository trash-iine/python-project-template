"""Invoke のタスク定義。

単独コマンドの薄いラッパーは置かず、複数ステップを束ねるタスクや
プロジェクト固有の知識 (モジュール名・パス) を必要とするタスクだけを定義する。
"""

import re
import sys
import tempfile
import webbrowser
from pathlib import Path

from invoke import task

PROJECT_NAME = "sample-project"
DOCS_SOURCE = Path("docs/source")
DOCS_HTML_INDEX = Path("docs/build/html/index.html")
SRC_ROOT = Path("src")

# CI (.github/workflows/tests.yml / .gitlab-ci.yml) と同じ順序・内容。変更時は両方を同期させる。
CI_CHECKS = [
    ("ruff check", "ruff check ."),
    ("ruff format", "ruff format --check ."),
    ("ty", "ty check"),
    ("pytest", "pytest"),
]

AUTOMODULE_PATTERN = re.compile(r"^\.\. automodule:: (\S+)", re.MULTILINE)


def _derive_module_name(project_name: str) -> str:
    """プロジェクト名から有効な Python モジュール名を導出する。

    Args:
        project_name (str): プロジェクト名。

    Returns:
        str: 導出したモジュール名。

    Raises:
        ValueError: 導出したモジュール名が無効な場合。

    """
    module_name = project_name.lower().replace("-", "_").replace(" ", "_")

    if not module_name:
        msg = "module_name is required."
        raise ValueError(msg)
    if not module_name.replace("_", "").isalnum() or module_name[0].isdigit():
        msg = f"Invalid module name: {module_name}"
        raise ValueError(msg)

    return module_name


def _module_exists(src_root: Path, dotted: str) -> bool:
    """ドット区切りのモジュール名に対応するファイルまたはパッケージが存在するか返す。

    Args:
        src_root (Path): ソースルート (`src/`)。
        dotted (str): `package.module` 形式のモジュール名。

    Returns:
        bool: `<root>/a/b.py` または `<root>/a/b/__init__.py` が存在すれば True。

    """
    base = src_root.joinpath(*dotted.split("."))
    return base.with_suffix(".py").is_file() or (base / "__init__.py").is_file()


def _stale_apidoc_pages(source_dir: Path, src_root: Path) -> list[Path]:
    """参照先モジュールがすべて消えた sphinx-apidoc 生成ページを列挙する。

    `automodule` ディレクティブを含む `.rst` だけを候補にするため、手書きページや
    `modules.rst` (toctree のみ) は対象外になる。生きているモジュールを 1 つでも
    参照していれば残す。

    Args:
        source_dir (Path): Sphinx のソースディレクトリ (`docs/source/`)。
        src_root (Path): ソースルート (`src/`)。

    Returns:
        list[Path]: 削除してよい `.rst` のパス (ソート済み)。

    """
    stale = []
    for page in sorted(source_dir.glob("*.rst")):
        modules = AUTOMODULE_PATTERN.findall(page.read_text(encoding="utf-8"))
        if modules and not any(_module_exists(src_root, module) for module in modules):
            stale.append(page)
    return stale


@task
def ci(c):
    """CI と同じ 4 チェックを失敗しても最後まで実行し、結果をまとめて表示する。

    Args:
        c (Context): Invoke のコンテキスト。

    """
    failed = []
    for name, command in CI_CHECKS:
        print(f"\n==> {command}")
        if c.run(command, warn=True, pty=True).failed:
            failed.append(name)

    print("\n==> summary")
    for name, _ in CI_CHECKS:
        print(f"  {'FAIL' if name in failed else 'ok  '}  {name}")
    if failed:
        sys.exit(1)


@task
def fix(c):
    """Ruff の自動修正とフォーマットを適用する。

    修正できない違反が残っても `ruff format` まで実行する。残った違反は `invoke ci` で確認する。

    Args:
        c (Context): Invoke のコンテキスト。

    """
    c.run("ruff check --fix .", warn=True, pty=True)
    c.run("ruff format .", pty=True)


@task
def audit(c):
    """依存パッケージの脆弱性を CI と同じ手順で監査する。

    Args:
        c (Context): Invoke のコンテキスト。

    """
    with tempfile.TemporaryDirectory() as tmp:
        requirements = Path(tmp) / "requirements-audit.txt"
        c.run(f"uv export --format requirements-txt --no-hashes --no-emit-project -o {requirements}")
        c.run(f"uvx pip-audit -r {requirements} --disable-pip --no-deps", pty=True)


@task
def docs(c, output="html", *, clean=False, strict=False, open=False):
    """ドキュメントをビルドする。

    Args:
        c (Context): Invoke のコンテキスト。
        output (str): `make -C docs` に渡す Sphinx ビルダー名。
        clean (bool): True ならビルド前に `make -C docs clean` を実行する。
        strict (bool): True なら warning をエラー扱いにする (`-W --keep-going`)。
        open (bool): True ならビルド後に `docs/build/html/index.html` をブラウザで開く。

    """
    if clean:
        c.run("make -C docs clean")
    sphinxopts = ' SPHINXOPTS="-W --keep-going"' if strict else ""
    c.run(f"make -C docs {output}{sphinxopts}", pty=True)
    if open:
        webbrowser.open(DOCS_HTML_INDEX.resolve().as_uri())


@task
def apidoc(c):
    """API リファレンスを再生成し、参照先モジュールが消えたページを削除する。

    Args:
        c (Context): Invoke のコンテキスト。

    """
    module_name = _derive_module_name(PROJECT_NAME)
    c.run(f"sphinx-apidoc -f -o {DOCS_SOURCE}/ {SRC_ROOT / module_name}", pty=True)
    for page in _stale_apidoc_pages(DOCS_SOURCE, SRC_ROOT):
        print(f"Removing stale page: {page}")
        page.unlink()


# template-only-start
# テンプレート専用の new-project タスクを invoke に公開する。sys.modules の
# ガードは template_tasks が先に import された場合の循環 import を防ぐ。
if "template_tasks" not in sys.modules:
    from template_tasks import new_project  # noqa: F401
# template-only-end
