"""sample_add モジュールのテスト。"""

import pytest

from sample_project.sample_add import sample_add


def test_sample_add() -> None:
    """正常な入力で和を返すことを確認する。"""
    assert sample_add(2, 3) == 5
    assert sample_add(-1, 1) == 0
    assert sample_add(0, 0) == 0


@pytest.mark.parametrize(
    ("a", "b"),
    [
        ("1", 2),
        (1.5, 2),
        (None, 2),
        (1, "2"),
        (1, 2.5),
        (1, None),
    ],
)
def test_sample_add_type_error(a: object, b: object) -> None:
    """int 以外の入力で TypeError を送出することを確認する。"""
    with pytest.raises(TypeError):
        sample_add(a, b)  # ty: ignore[invalid-argument-type]  # 型違いの入力を渡すこと自体がテストの目的
