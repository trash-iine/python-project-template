# sample-project

Python プロジェクトテンプレートです。 <!-- template-only-line -->
CLI、テスト、リント、ドキュメント生成、CI などの基本構成が含まれています。

生成された API ドキュメントは [GitHub Pages](https://trash-iine.github.io/python-project-template/) で公開されています。 <!-- template-only-line -->

## 前提ツール

- [Python](https://www.python.org) 3.13 以上
- [uv](https://github.com/astral-sh/uv): 仮想環境と依存関係の管理
- [Git](https://git-scm.com/)
- [Pandoc](https://pandoc.org/): ドキュメント生成時のみ必要

> [!NOTE]
> インストール方法の例:
> - **Python**: `sudo apt install python3 python3-venv`（Ubuntu/Debian 系）や [公式サイト](https://www.python.org/downloads/) から
> - **uv**: `curl -LsSf https://astral.sh/uv/install.sh | sh` や `pipx install uv` など
> - **Pandoc**: `sudo apt install pandoc`（Ubuntu/Debian 系）や [公式サイト](https://pandoc.org/installing.html) から

<!-- template-only-start -->
## このテンプレートから新規プロジェクトを作る

1. テンプレートをクローンして移動します。

   ```bash
   $ git clone https://github.com/trash-iine/python-project-template.git
   $ cd python-project-template
   ```

2. 新しいプロジェクトを作成します。コピー先ディレクトリの名前がそのままプロジェクト名になり、`sample-project` / `sample_project` と作者名が新しい値に置換された状態でコピーされ、`uv.lock` の再生成と `git init` + 初回コミットまで自動で行われます。

   ```bash
   $ uv run invoke new-project -d ~/new-project-name
   ```

   オプション:

   - `-p, --project-name <name>`: プロジェクト名(省略時はコピー先ディレクトリ名を使用)
   - `--author <name>`: 作者名(省略時は `git config user.name` の値を使用)
   - `--remote-url <url>`: 指定すると `git remote add origin <url>` まで実行
   - `--no-git`: `git init` と初回コミットを行わない
   - `--dry-run`: 実際には作成せず処理内容のみ表示

   ```bash
   $ uv run invoke new-project -d ~/new-project-name --dry-run
   ```

3. 作成したプロジェクトに移動してセットアップします。

   ```bash
   $ cd ~/new-project-name
   $ uv sync --dev
   ```
<!-- template-only-end -->

## セットアップ

依存関係のインストール（`.venv/` の作成）は次の 1 コマンドで完了します。

```bash
$ uv sync --dev
```

Ruff・Pytest・Sphinx・Invoke などの開発ツールがインストールされます。以降のコマンドはすべて `uv run <command>` の形で仮想環境内で実行できます（手動での activate は不要です）。

## Features & Usage

### 1. CLI の実行

`src/sample_project/__main__.py` に実装された CLI を実行します。

```bash
$ uv run sample-project
Hello, World!
```

Or,

```bash
$ uv run python -m sample_project
Hello, World!
```

`src/sample_project/__main__.py` の内容を編集すると実行内容が変更できます。

### 2. ライブラリとして使う

パッケージとして import して利用できます。

```python
>>> from sample_project import sample_add
>>> sample_add(2, 3)
5
```

引数が `int` でない場合は `TypeError` を送出します。

```python
>>> sample_add("2", 3)
Traceback (most recent call last):
    ...
TypeError: Invalid types: a=<class 'str'>, b=<class 'int'>
```

### 3. テスト（Pytest）

`test/` 配下のテストをすべて実行する。

```bash
$ uv run invoke test
==================== test session starts ====================
platform darwin -- Python 3.13.11, pytest-9.0.1, pluggy-1.6.0
rootdir: sample-project
collected 1 item

test/test_add.py .                                     [100%]

===================== 1 passed in 0.00s =====================
```

### 4. フォーマット（Ruff）

リントとフォーマットを行う。

```bash
$ uv run invoke check
All checks passed!
```

```bash
$ uv run invoke format
7 files left unchanged.
```

### 5. ドキュメント生成（Sphinx）

`docs/source/` のマークダウン / rst / ノートブックからドキュメントを生成する。

```bash
$ uv run invoke docs
```

生成された HTML は `docs/build/html/` に出力されます。ブラウザで `docs/build/html/index.html` を開いて確認できます。また、デフォルトブランチへ push すると GitHub では GitHub Actions（`.github/workflows/docs.yml`）が GitHub Pages へ、GitLab では GitLab CI（`.gitlab-ci.yml` の `pages` ジョブ）が GitLab Pages へ自動デプロイします。

## Invoke タスク一覧

開発タスクは `tasks.py` に [Invoke](https://www.pyinvoke.org/) タスクとして定義されています。

| タスク | 実行例 | 説明 |
| --- | --- | --- |
| `test` | `uv run invoke test` | `test/` 配下の Pytest を実行 |
| `check` | `uv run invoke check` | Ruff によるリント |
| `format` | `uv run invoke format` | Ruff によるフォーマット |
| `docs` | `uv run invoke docs` | Sphinx で HTML ドキュメントを生成 |
| `update-apidoc` | `uv run invoke update-apidoc` | `sphinx-apidoc` で API リファレンス（`docs/source/*.rst`）を再生成。モジュールを追加・リネームしたら実行 |
| `new-project` | `uv run invoke new-project -d <dir>` | このテンプレートから新規プロジェクトを作成（`--dry-run` 対応） | <!-- template-only-line -->

CI（GitHub では `.github/workflows/tests.yml`、GitLab では `.gitlab-ci.yml`）では `ruff check` / `ruff format --check` / `ty check` / `pytest` が実行されます。ローカルでも同じチェックを通しておくと安全です。

```bash
$ uv run ruff check .
$ uv run ruff format --check .
$ uv run ty check
$ uv run pytest test
```

## ディレクトリ構成

```
sample-project/
├── src/sample_project/       # サンプルプロジェクト
│   ├── __main__.py           # CLI 実装
│   └── sample_add.py         # 例示用のシンプルなモジュール
├── test/                     # テストコード（`test_*.py`）
├── docs/                     # Sphinx ドキュメント
│   └── source/               # ドキュメントソース（Markdown / rst / ipynb）
├── .github/workflows/        # CI（テスト・リント）と GitHub Pages デプロイ
├── .gitlab-ci.yml            # GitLab CI（GitHub Actions と同等の CI と GitLab Pages デプロイ）
├── tasks.py                  # Invoke タスク定義（lint/format/test/docs/new-project）
├── pyproject.toml            # 依存関係とツール設定
└── README.md                 # 本ドキュメント
```

## VSCode の推奨設定

- `.vscode/extensions.json` のレコメンドに従うと、Python、Ruff、pytest、Sphinx 関連の拡張機能を簡単に導入できます。
- 仮想環境 (`.venv/`) を VSCode が認識しない場合は、コマンドパレットで「Python: Select Interpreter」を選び、`.venv/bin/python` を指定してください。
- フォーマットは Ruff が担当するため、他のフォーマッター拡張は無効化するか適宜設定を見直してください。
