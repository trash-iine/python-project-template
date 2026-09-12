"""tasks.py の補助関数のテスト。"""

import pytest

from tasks import _derive_module_name


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
