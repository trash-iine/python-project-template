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

    print("Setting up the development environment...")
    c.run("uv sync --dev")


def activate_env(c):
    """Activate the development environment."""
    check_env(c)
    c.run(". ./.venv/bin/activate")


@task
def docs(c):
    """Build the documentation."""
    activate_env(c)
    c.run("make -C docs html", warn=True)
