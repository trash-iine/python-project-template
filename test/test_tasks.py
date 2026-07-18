"""Test for helper functions in tasks.py."""

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
    """Test module names are derived from project names."""
    assert _derive_module_name(project_name) == expected


@pytest.mark.parametrize("project_name", ["", "1project", "my.project"])
def test_derive_module_name_invalid(project_name: str) -> None:
    """Test invalid project names raise ValueError."""
    with pytest.raises(ValueError, match=r"module_name|Invalid module name"):
        _derive_module_name(project_name)
