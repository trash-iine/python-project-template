"""Test for helper functions in tasks.py."""

from datetime import UTC, datetime

import pytest

from tasks import (
    PROJECT_NAME,
    TEMPLATE_AUTHOR,
    TEMPLATE_AUTHOR_SLUG,
    _derive_module_name,
    _rewrite_text,
    _strip_template_sections,
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
    """Test module names are derived from project names."""
    assert _derive_module_name(project_name) == expected


@pytest.mark.parametrize("project_name", ["", "1project", "my.project"])
def test_derive_module_name_invalid(project_name: str) -> None:
    """Test invalid project names raise ValueError."""
    with pytest.raises(ValueError, match=r"module_name|Invalid module name"):
        _derive_module_name(project_name)


def test_strip_template_sections_removes_block() -> None:
    """Test lines between start/end markers are removed."""
    text = "keep\n<!-- template-only-start -->\ndrop\n<!-- template-only-end -->\nkeep2\n"
    assert _strip_template_sections(text) == "keep\nkeep2\n"


def test_strip_template_sections_removes_marked_line() -> None:
    """Test lines with the line marker are removed."""
    text = "keep\ndrop <!-- template-only-line -->\nkeep2\n"
    assert _strip_template_sections(text) == "keep\nkeep2\n"


def test_strip_template_sections_keeps_unmarked_text() -> None:
    """Test text without markers is unchanged."""
    text = "no markers\nat all\n"
    assert _strip_template_sections(text) == text


def test_rewrite_text_replaces_copyright_and_author() -> None:
    """Test conf.py style copyright/author lines get the new author and year."""
    data = f'copyright = "2025, {TEMPLATE_AUTHOR}"\nauthor = "{TEMPLATE_AUTHOR}"\n'
    result = _rewrite_text(data, "demo-app", "New Author", is_markdown=False)
    year = datetime.now(tz=UTC).year
    assert f'copyright = "{year}, New Author"' in result
    assert 'author = "New Author"' in result


def test_rewrite_text_replaces_author_slug() -> None:
    """Test pyproject.toml style author entries are replaced."""
    data = f'authors = [{{ name = "{TEMPLATE_AUTHOR_SLUG}" }}]\n'
    result = _rewrite_text(data, "demo-app", "New Author", is_markdown=False)
    assert result == 'authors = [{ name = "New Author" }]\n'


def test_rewrite_text_replaces_project_and_module_name() -> None:
    """Test project and module names are replaced."""
    module_name = _derive_module_name(PROJECT_NAME)
    data = f"{PROJECT_NAME} uses {module_name}\n"
    result = _rewrite_text(data, "demo-app", "New Author", is_markdown=False)
    assert result == "demo-app uses demo_app\n"


def test_rewrite_text_strips_markers_only_in_markdown() -> None:
    """Test template-only markers are stripped in Markdown but kept elsewhere."""
    data = "keep\ndrop <!-- template-only-line -->\n"
    assert _rewrite_text(data, "demo-app", "New Author", is_markdown=True) == "keep\n"
    assert _rewrite_text(data, "demo-app", "New Author", is_markdown=False) == data
