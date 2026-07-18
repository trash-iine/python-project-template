"""Test for helper functions in template_tasks.py."""

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
    """Test lines between start/end markers are removed."""
    text = "keep\n<!-- template-only-start -->\ndrop\n<!-- template-only-end -->\nkeep2\n"
    assert _strip_template_sections(text) == "keep\nkeep2\n"


def test_strip_template_sections_removes_marked_line() -> None:
    """Test lines with the line marker are removed."""
    text = "keep\ndrop <!-- template-only-line -->\nkeep2\n"
    assert _strip_template_sections(text) == "keep\nkeep2\n"


def test_strip_template_sections_removes_hash_comment_block() -> None:
    """Test markers in hash-comment style (tasks.py, CODEOWNERS) also work."""
    text = "keep\n# template-only-start\ndrop\n# template-only-end\nkeep2\n"
    assert _strip_template_sections(text) == "keep\nkeep2\n"


def test_strip_template_sections_keeps_unmarked_text() -> None:
    """Test text without markers is unchanged."""
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
    """Test template markers are stripped only in Markdown and registered files."""
    assert _should_strip_template(path) is expected


def test_rewrite_text_replaces_copyright_and_author() -> None:
    """Test conf.py style copyright/author lines get the new author and year."""
    data = f'copyright = "2025, {TEMPLATE_AUTHOR}"\nauthor = "{TEMPLATE_AUTHOR}"\n'
    result = _rewrite_text(data, "demo-app", "New Author", strip_template=False)
    year = datetime.now(tz=UTC).year
    assert f'copyright = "{year}, New Author"' in result
    assert 'author = "New Author"' in result


def test_rewrite_text_replaces_license_copyright() -> None:
    """Test MIT LICENSE style copyright lines get the new author and year."""
    data = f"Copyright (c) 2025 {TEMPLATE_AUTHOR}\n"
    result = _rewrite_text(data, "demo-app", "New Author", strip_template=False)
    year = datetime.now(tz=UTC).year
    assert result == f"Copyright (c) {year} New Author\n"


def test_rewrite_text_replaces_author_slug() -> None:
    """Test pyproject.toml style author entries are replaced."""
    data = f'authors = [{{ name = "{TEMPLATE_AUTHOR_SLUG}" }}]\n'
    result = _rewrite_text(data, "demo-app", "New Author", strip_template=False)
    assert result == 'authors = [{ name = "New Author" }]\n'


def test_rewrite_text_replaces_project_and_module_name() -> None:
    """Test project and module names are replaced."""
    module_name = _derive_module_name(PROJECT_NAME)
    data = f"{PROJECT_NAME} uses {module_name}\n"
    result = _rewrite_text(data, "demo-app", "New Author", strip_template=False)
    assert result == "demo-app uses demo_app\n"


def test_rewrite_text_strips_markers_only_when_requested() -> None:
    """Test template-only markers are stripped only with strip_template=True."""
    data = "keep\ndrop <!-- template-only-line -->\n"
    assert _rewrite_text(data, "demo-app", "New Author", strip_template=True) == "keep\n"
    assert _rewrite_text(data, "demo-app", "New Author", strip_template=False) == data
