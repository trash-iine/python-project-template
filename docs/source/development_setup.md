# 開始ガイド

このページでは、このサンプルプロジェクトを開発用の土台として使い始めるための手順をまとめます。

## 1. 新規プロジェクトの開始方法

### 事前準備

- Python
- [uv](https://github.com/astral-sh/uv): Python の仮想環境と依存関係管理ツール
- [Pandoc](https://pandoc.org/): ドキュメント生成ツール

```{admonition} Note
Python, uv, pandoc のインストールは例えば以下の方法があります。

- **Python**: `sudo apt install python3 python3-venv`（Ubuntu/Debian 系）や [公式サイト](https://www.python.org/downloads/) から
- **uv**: `curl -LsSf https://astral.sh/uv/install.sh | sh` や `pipx install uv` (pipx 別途インストール必要) など
- **Pandoc**: `sudo apt install pandoc`（Ubuntu/Debian 系）や [公式サイト](https://pandoc.org/installing.html) から
```

### 開発環境セットアップ手順

リポジトリをクローンし、プロジェクトディレクトリに移動します。

```bash
$ git clone https://github.com/trash-iine/python-project-template.git
$ cd python-project-template
```

自分のプロジェクトを新規作成します。

```bash
$ uv run invoke new-project -p new-project-name -d ~/new-project-dir
```

新しく作成されたプロジェクトディレクトリに移動します。

```bash
$ cd ~/new-project-dir
```

`uv` を使って仮想環境と依存関係をセットアップします。

```bash
$ uv sync --dev
```

`.venv/` が作成され、Ruff・Pytest・Sphinx・Invoke などの開発ツールがインストールされます。

## 2. 仮想環境の有効化

- コマンドライン: `uv run <command>` で仮想環境内のコマンドを実行できます。
- VSCode: コマンドパレットから「Python: Select Interpreter」で `.venv/bin/python` を選択します。

## 3. 動作確認

CLI を実行して環境が正しく構成されているか確認します。

```bash
$ uv run python -m sample_project
Hello, World!
```

## 4. テスト

`test/` 配下のテストをすべて実行して、動作確認を行います。

```bash
$ uv run invoke test
```

## 5. ドキュメントビルド

```bash
$ uv run invoke docs
```

生成された HTML は `docs/build/` 配下に出力されます。ブラウザで開いて内容を確認できます。

```{admonition} Note
PDF 出力もサポートしています。`uv run invoke docs pdf` を実行すると `docs/build/pdf` 配下に PDF が生成されます。
```

## 6. コード編集のヒント (VSCode)

- `.vscode/extensions.json` のレコメンドに従うと必要な拡張機能をまとめて導入できます。
- Ruff をフォーマッターとして使うため、他フォーマッター拡張の自動整形は無効化するか競合しないよう設定してください。

## 8. 次に行うこと

- `src/sample_project/`（リネーム後のパス）にあなたのコードを追加します。
- 新しいモジュールや関数を作成したら、`test/` に対応する `test_*.py` を追加してください。
- 新しいモジュールや関数を作成したら、 `uv run update-apidoc` を実行して API ドキュメントを更新します。
- 仕様や手順を文書化する場合は、`docs/source/` に Markdown かノートブックを追加し、`index.md` の `{toctree}` に追記します。
