"""Task definitions using Invoke."""

import sys

from invoke import task

PROJECT_NAME = "sample-project"


def check_env(c):
    """Check if the development environment is set up.

    Args:
        c (Context): Invoke context.

    """
    result = c.run("test -d ./.venv", warn=True)
    if result.ok:
        return

    # check if uv is installed
    uv_check = c.run("command -v uv", warn=True)
    if uv_check.failed:
        print("Error: 'uv' is not installed. Please install 'uv' first.")
        sys.exit(1)

    print("Running 'uv sync --dev' to set up the development environment.")
    c.run("uv sync --dev")


@task
def docs(c, output="html"):
    """Build the documentation.

    Args:
        c (Context): Invoke context.
        output (str): Sphinx builder name passed to `make -C docs`.

    """
    check_env(c)
    c.run(f"make -C docs {output}")


@task
def test(c):
    """Run the test suite.

    Args:
        c (Context): Invoke context.

    """
    check_env(c)
    c.run("pytest", pty=True)


@task
def format(c, target="."):
    """Run the formatter.

    Args:
        c (Context): Invoke context.
        target (str): File or directory to format.

    """
    check_env(c)
    c.run(f"ruff format {target}", pty=True)


@task
def check(c, target="."):
    """Run the linter.

    Args:
        c (Context): Invoke context.
        target (str): File or directory to lint.

    """
    check_env(c)
    c.run(f"ruff check {target}", pty=True)


def _derive_module_name(project_name: str) -> str:
    """Derive a valid Python module name from a project name.

    Args:
        project_name (str): The new project name.

    Returns:
        str: The derived module name.

    Raises:
        ValueError: If the module name is invalid.

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
    """Update automodule directives in docs.

    Args:
        c (Context): Invoke context.

    """
    check_env(c)
    module_name = _derive_module_name(PROJECT_NAME)
    c.run(f"sphinx-apidoc -f -o docs/source/ src/{module_name}", pty=True)


# template-only-start
# Expose the template-only new-project task to invoke. The sys.modules guard
# avoids a circular-import failure when template_tasks is imported first.
if "template_tasks" not in sys.modules:
    from template_tasks import new_project  # noqa: F401
# template-only-end
