"""Invoke のタスク定義。"""

import sys

from invoke import task

PROJECT_NAME = "sample-project"


def check_env(c):
    """開発環境がセットアップ済みか確認し、未整備なら `uv sync --dev` を実行する。

    Args:
        c (Context): Invoke のコンテキスト。

    """
    result = c.run("test -d ./.venv", warn=True)
    if result.ok:
        return

    # uv がインストールされているか確認する
    uv_check = c.run("command -v uv", warn=True)
    if uv_check.failed:
        print("Error: 'uv' is not installed. Please install 'uv' first.")
        sys.exit(1)

    print("Running 'uv sync --dev' to set up the development environment.")
    c.run("uv sync --dev")


@task
def docs(c, output="html"):
    """ドキュメントをビルドする。

    Args:
        c (Context): Invoke のコンテキスト。
        output (str): `make -C docs` に渡す Sphinx ビルダー名。

    """
    check_env(c)
    c.run(f"make -C docs {output}")


@task
def test(c):
    """テストスイートを実行する。

    Args:
        c (Context): Invoke のコンテキスト。

    """
    check_env(c)
    c.run("pytest", pty=True)


@task
def format(c, target="."):
    """フォーマッタを実行する。

    Args:
        c (Context): Invoke のコンテキスト。
        target (str): フォーマット対象のファイルまたはディレクトリ。

    """
    check_env(c)
    c.run(f"ruff format {target}", pty=True)


@task
def check(c, target="."):
    """リンタを実行する。

    Args:
        c (Context): Invoke のコンテキスト。
        target (str): リント対象のファイルまたはディレクトリ。

    """
    check_env(c)
    c.run(f"ruff check {target}", pty=True)


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


@task
def update_apidoc(c):
    """API リファレンス (docs の automodule ディレクティブ) を再生成する。

    Args:
        c (Context): Invoke のコンテキスト。

    """
    check_env(c)
    module_name = _derive_module_name(PROJECT_NAME)
    c.run(f"sphinx-apidoc -f -o docs/source/ src/{module_name}", pty=True)


# template-only-start
# テンプレート専用の new-project タスクを invoke に公開する。sys.modules の
# ガードは template_tasks が先に import された場合の循環 import を防ぐ。
if "template_tasks" not in sys.modules:
    from template_tasks import new_project  # noqa: F401
# template-only-end
