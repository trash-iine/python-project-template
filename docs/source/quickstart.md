# クイックスタート

## Prerequisites

- Python
- uv
- Git
- Pandoc (for documentation generation)

## Start a new project

1. レポジトリをクローンし、テンプレートに移動します。
```sh
$ git clone https://github.com/trash-iine/python-project-template.git
$ cd python-project-template
```
2. 新しいプロジェクトを作成します。
```sh
uv run invoke update-module
```
3. 作成したプロジェクトディレクトリに移動します。
```sh
$ cd ~/new-project-dir
```
4. 仮想環境を作成します。
```sh
$ uv sync --dev
```
