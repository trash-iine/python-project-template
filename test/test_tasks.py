"""tasks.py の補助関数のテスト。"""

import datetime
from pathlib import Path

import pytest

from tasks import (
    _derive_module_name,
    _module_exists,
    _next_adr_number,
    _render_adr,
    _stale_apidoc_pages,
    _validate_adr_slug,
)


@pytest.mark.parametrize(
    ("project_name", "expected"),
    [
        ("my-project", "my_project"),
        ("My Project", "my_project"),
        ("myproject", "myproject"),
    ],
)
def test_derive_module_name(project_name: str, expected: str) -> None:
    """プロジェクト名からモジュール名が導出されることを確認する。"""
    assert _derive_module_name(project_name) == expected


@pytest.mark.parametrize("project_name", ["", "1project", "my.project"])
def test_derive_module_name_invalid(project_name: str) -> None:
    """無効なプロジェクト名で ValueError を送出することを確認する。"""
    with pytest.raises(ValueError, match=r"module_name|Invalid module name"):
        _derive_module_name(project_name)


def test_module_exists(tmp_path: Path) -> None:
    """単一モジュールとパッケージの両方を存在判定できることを確認する。"""
    (tmp_path / "pkg").mkdir()
    (tmp_path / "pkg" / "__init__.py").touch()
    (tmp_path / "pkg" / "mod.py").touch()

    assert _module_exists(tmp_path, "pkg")
    assert _module_exists(tmp_path, "pkg.mod")
    assert not _module_exists(tmp_path, "pkg.missing")
    assert not _module_exists(tmp_path, "other")


def test_stale_apidoc_pages(tmp_path: Path) -> None:
    """参照先モジュールがすべて消えた automodule ページだけが stale になることを確認する。"""
    src = tmp_path / "src"
    (src / "pkg").mkdir(parents=True)
    (src / "pkg" / "__init__.py").touch()
    (src / "pkg" / "alive.py").touch()

    source = tmp_path / "docs" / "source"
    source.mkdir(parents=True)
    # 生きているモジュールを 1 つでも参照するページは残す
    (source / "pkg.rst").write_text(
        ".. automodule:: pkg.alive\n\n.. automodule:: pkg.removed\n",
        encoding="utf-8",
    )
    (source / "pkg.removed.rst").write_text(".. automodule:: pkg.removed\n", encoding="utf-8")
    (source / "old_pkg.rst").write_text(".. automodule:: old_pkg\n", encoding="utf-8")
    # automodule を含まないページ (toctree のみ・手書き) は候補外
    (source / "modules.rst").write_text(".. toctree::\n\n   pkg\n", encoding="utf-8")
    (source / "guide.rst").write_text("Guide\n=====\n", encoding="utf-8")

    assert _stale_apidoc_pages(source, src) == [source / "old_pkg.rst", source / "pkg.removed.rst"]


def test_validate_adr_slug() -> None:
    """kebab-case の slug だけを受け付けることを確認する。"""
    assert _validate_adr_slug("my-decision") == "my-decision"
    assert _validate_adr_slug("adr2") == "adr2"


@pytest.mark.parametrize("slug", ["", "My Decision", "my_decision", "-leading", "trailing-"])
def test_validate_adr_slug_invalid(slug: str) -> None:
    """kebab-case でない slug で ValueError を送出することを確認する。"""
    with pytest.raises(ValueError, match="kebab-case"):
        _validate_adr_slug(slug)


def test_next_adr_number(tmp_path: Path) -> None:
    """既存 ADR の最大番号 + 1 が採番され、テンプレートや index は無視されることを確認する。"""
    assert _next_adr_number(tmp_path) == 1

    (tmp_path / "index.md").touch()
    (tmp_path / "_template.md").touch()
    (tmp_path / "0001-first.md").touch()
    (tmp_path / "0003-third.md").touch()
    assert _next_adr_number(tmp_path) == 4


def test_render_adr() -> None:
    """テンプレートのプレースホルダが番号・タイトル・日付で埋まることを確認する。"""
    template = "# $number. $title\n\n- 日付: $date\n"
    rendered = _render_adr(template, 7, "決定のタイトル", datetime.date(2026, 9, 14))
    assert rendered == "# 0007. 決定のタイトル\n\n- 日付: 2026-09-14\n"
