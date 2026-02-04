# Sample Python Project

Python プロジェクトテンプレートです。CLI、テスト、ドキュメント生成などの基本構成が含まれています。

開始方法は [クイックスタート](https://trash-iine.github.io/python-project-template/quickstart.html) を参照してください。

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
