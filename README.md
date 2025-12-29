# Sample Python Project

This is a sample Python project to demonstrate project structure, packaging, and basic functionality. It includes a simple addition function and a command-line interface.

## Features

- Command-line interface to run the main function
- Configured with `pyproject.toml` for easy packaging and dependency management
- Linting with [Ruff](https://github.com/astral-sh/ruff)
- Type checking with [Ty](https://github.com/astral-sh/ty)
- Testing with [Pytest](https://docs.pytest.org/)
- Documentation generation with [Sphinx](https://www.sphinx-doc.org/)
- VSCode settings for a better development experience

## Requirements

- [uv](https://github.com/astral-sh/uv)
- [VSCode](https://code.visualstudio.com/)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/trash-iine/python-project-template.git
   cd python-project-template
   ```
2. Install the required dependencies:
   ```bash
   uv sync --dev
   ```

## Usage

### 1. Running the Command-Line Interface

You can run the command-line interface written in `src/sample_project/__main__.py` using the following command:

```bash
python -m sample_project
```

### 2. Testing

To run the tests, use the following command:

```bash
pytest
```

### File Structure

```
sample-project/
├── .vscode/                  # VSCode settings
│   ├── extensions.json       # Recommended extensions
│   └── settings.json         # VSCode settings
├── docs/                     # Documentation files
│   ├── conf.py               # Sphinx configuration
│   └── index.rst             # Main documentation page
├── src/                      # Source code
│   └── sample_project/       # Sample project package
│       ├── __init__.py       # Package initializer
│       ├── __main__.py       # Command-line interface
│       └── sample_add.py     # Sample addition function
├── tests/                    # Test files
│   ├── __init__.py           # Package initializer
│   └── test_add.py           # Sample test case
├── .gitignore                # Git ignore file
├── .python-version           # Python version specification
├── pyproject.toml            # Project configuration and dependencies
├── tasks.py                  # Task definitions using Invoke
└── README.md                 # Project documentation
```
