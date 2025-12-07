"""Test for sample_add module."""

from sample_project.sample_add import sample_add


def test_sample_add() -> None:
    """Test sample_add function."""
    assert sample_add(2, 3) == 5
    assert sample_add(-1, 1) == 0
    assert sample_add(0, 0) == 0
