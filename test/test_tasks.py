"""tasks.py の補助関数のテスト。"""

from pathlib import Path

import pytest

from tasks import _derive_module_name, _module_exists, _stale_apidoc_pages


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
