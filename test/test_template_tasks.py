"""template_tasks.py の補助関数のテスト。"""

from datetime import UTC, datetime
from pathlib import Path

import pytest

from tasks import PROJECT_NAME, _derive_module_name
from template_tasks import (
    TEMPLATE_AUTHOR,
    TEMPLATE_AUTHOR_SLUG,
    _rewrite_text,
    _should_strip_template,
    _strip_template_sections,
)


def test_strip_template_sections_removes_block() -> None:
    """start/end マーカーの間の行が取り除かれることを確認する。"""
    text = "keep\n<!-- template-only-start -->\ndrop\n<!-- template-only-end -->\nkeep2\n"
    assert _strip_template_sections(text) == "keep\nkeep2\n"


def test_strip_template_sections_removes_marked_line() -> None:
    """line マーカー付きの行が取り除かれることを確認する。"""
    text = "keep\ndrop <!-- template-only-line -->\nkeep2\n"
    assert _strip_template_sections(text) == "keep\nkeep2\n"


def test_strip_template_sections_removes_hash_comment_block() -> None:
    """# コメント形式のマーカー (tasks.py, CODEOWNERS) でも動作することを確認する。"""
    text = "keep\n# template-only-start\ndrop\n# template-only-end\nkeep2\n"
    assert _strip_template_sections(text) == "keep\nkeep2\n"


def test_strip_template_sections_trims_trailing_blank_lines() -> None:
    """ファイル末尾のブロック除去後に直前の空行が残らないことを確認する。"""
    text = "code\n\n\n# template-only-start\ndrop\n# template-only-end\n"
    assert _strip_template_sections(text) == "code\n"


def test_strip_template_sections_keeps_unmarked_text() -> None:
    """マーカーのないテキストは変更されないことを確認する。"""
    text = "no markers\nat all\n"
    assert _strip_template_sections(text) == text


@pytest.mark.parametrize(
    ("path", "expected"),
    [
        (Path("README.md"), True),
        (Path("docs/source/index.md"), True),
        (Path("tasks.py"), True),
        (Path(".github/CODEOWNERS"), True),
        (Path("pyproject.toml"), False),
        (Path("src/sample_project/sample_add.py"), False),
    ],
)
def test_should_strip_template(path: Path, *, expected: bool) -> None:
    """Markdown と登録済みファイルのみがマーカー除去対象になることを確認する。"""
    assert _should_strip_template(path) is expected


def test_rewrite_text_replaces_copyright_and_author() -> None:
    """conf.py 形式の copyright/author 行が新しい著者と年に置換されることを確認する。"""
    data = f'copyright = "2025, {TEMPLATE_AUTHOR}"\nauthor = "{TEMPLATE_AUTHOR}"\n'
    result = _rewrite_text(data, "demo-app", "New Author", strip_template=False)
    year = datetime.now(tz=UTC).year
    assert f'copyright = "{year}, New Author"' in result
    assert 'author = "New Author"' in result


def test_rewrite_text_replaces_license_copyright() -> None:
    """MIT LICENSE 形式の copyright 行が新しい著者と年に置換されることを確認する。"""
    data = f"Copyright (c) 2025 {TEMPLATE_AUTHOR}\n"
    result = _rewrite_text(data, "demo-app", "New Author", strip_template=False)
    year = datetime.now(tz=UTC).year
    assert result == f"Copyright (c) {year} New Author\n"


def test_rewrite_text_replaces_author_slug() -> None:
    """pyproject.toml 形式の著者エントリが置換されることを確認する。"""
    data = f'authors = [{{ name = "{TEMPLATE_AUTHOR_SLUG}" }}]\n'
    result = _rewrite_text(data, "demo-app", "New Author", strip_template=False)
    assert result == 'authors = [{ name = "New Author" }]\n'


def test_rewrite_text_replaces_project_and_module_name() -> None:
    """プロジェクト名とモジュール名が置換されることを確認する。"""
    module_name = _derive_module_name(PROJECT_NAME)
    data = f"{PROJECT_NAME} uses {module_name}\n"
    result = _rewrite_text(data, "demo-app", "New Author", strip_template=False)
    assert result == "demo-app uses demo_app\n"


def test_rewrite_text_strips_markers_only_when_requested() -> None:
    """strip_template=True のときだけテンプレートマーカーが除去されることを確認する。"""
    data = "keep\ndrop <!-- template-only-line -->\n"
    assert _rewrite_text(data, "demo-app", "New Author", strip_template=True) == "keep\n"
    assert _rewrite_text(data, "demo-app", "New Author", strip_template=False) == data
