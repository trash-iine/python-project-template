"""Task definitions using Invoke."""

import sys

from invoke import task


def check_env(c):
    """Check if the development environment is set up."""
    result = c.run("test -d ./.venv", warn=True)
    if result.ok:
        return

    # check if uv is installed
    uv_check = c.run("command -v uv", warn=True)
    if uv_check.failed:
        print("Error: 'uv' is not installed. Please install 'uv' first.")
        sys.exit(1)

    print("Run: 'uv sync --dev' to set up the development environment.")
    c.run("uv sync --dev")


def activate_env(c):
    """Activate the development environment."""
    check_env(c)
    c.run(". ./.venv/bin/activate")


@task
def docs(c, output="html"):
    """Build the documentation."""
    activate_env(c)
    c.run(f"make -C docs {output}", warn=True)


@task
def test(c):
    """Run the test suite."""
    activate_env(c)
    c.run("pytest test", pty=True)


@task
def format(c, target="."):
    """Run the formatter."""
    activate_env(c)
    c.run(f"ruff format {target}", pty=True)


@task
def check(c, target="."):
    """Run the linter."""
    activate_env(c)
    c.run(f"ruff check {target}", pty=True)
