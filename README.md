# Sample Python Project

シンプルな CLI 付きの Python プロジェクトテンプレート。

## Requirements

- Python>=3.13
- [uv](https://github.com/astral-sh/uv)（依存関係/仮想環境管理）
- 開発支援ツール (`uv sync --dev` で自動導入)
   - [Ruff](https://docs.astral.sh/ruff/) （コード品質チェック）
   - [ty](https://docs.astral.sh/ty/) （型チェック）
   - [Pytest](https://docs.pytest.org/) （テストフレームワーク）
   - [Sphinx](https://www.sphinx-doc.org/) （ドキュメント生成）
   - [Invoke](https://www.pyinvoke.org/) （タスクランナー）

## Installation

1. リポジトリを取得する
   ```bash
   git clone https://github.com/trash-iine/python-project-template.git
   ```
2. プロジェクトディレクトリに移動する
   ```bash
   cd python-project-template
   ```
3. 依存関係をインストールする
   ```bash
   uv sync --dev
   ```
   `.venv/` が生成され、開発用ツールも導入される

## Features & Usage

### 1. CLI の実行

`src/sample_project/__main__.py` に実装された CLI を実行する。

```bash
$ uv run sample-project
Hello, World!
```

Or,

```bash
$ uv run python -m sample_project
Hello, World!
```

### 2. テスト（Pytest）

`test/` 配下のテストをすべて実行する。

```bash
$ uv run invoke test
==================== test session starts ====================
platform darwin -- Python 3.13.11, pytest-9.0.1, pluggy-1.6.0
rootdir: sample-project
configfile: pyproject.toml
collected 1 item

test/test_add.py .                                     [100%]

===================== 1 passed in 0.00s =====================
```

### 3. フォーマット（Ruff）

リントとフォーマットを行う。

```bash
$ uv run invoke check
All checks passed!
```

```bash
$ uv run invoke format
7 files left unchanged.
```


### 4. ドキュメント生成（Sphinx）

`docs/source/` のマークダウン / rst ファイルからドキュメントを生成する。

```bash
$ uv run invoke docs html
```

## ディレクトリ構成

```
sample-project/
├── src/sample_project/       # サンプルプロジェクト
│   ├── __main__.py           # CLI 実装
│   └── sample_add.py         # 例示用のシンプルなモジュール
├── test/                     # テストコード（`test_*.py`）
├── docs/                     # Sphinx ソースとビルドターゲット
├── tasks.py                  # Invoke タスク定義（lint/format/test/docs）
├── pyproject.toml            # 依存関係とツール設定
└── README.md                 # 本ドキュメント
```

## VSCode の推奨設定

- `.vscode/extensions.json` のレコメンドに従うと、Python、Ruff、pytest、Sphinx 関連の拡張機能を簡単に導入できます。
- 仮想環境 (`.venv/`) を VSCode が認識しない場合は、コマンドパレットで「Python: Select Interpreter」を選び、`.venv/bin/python` を指定してください。
- フォーマットは Ruff が担当するため、他のフォーマッター拡張は無効化するか適宜設定を見直してください。
