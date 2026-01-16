# 開始ガイド

本章ではこのサンプルプロジェクトを開発用の土台として使い始めるための手順をまとめます。

## 1. 環境準備

- 前提: Python 3.13 と [uv](https://github.com/astral-sh/uv) がインストールされていること。
- 依存関係とツールを導入します。

```bash
uv sync --dev
```

> `.venv/` が作成され、Ruff・Pytest・Sphinx・Invoke などの開発ツールも入ります。

## 2. 仮想環境の有効化

コマンドラインで使う場合は `source .venv/bin/activate`。VSCode ではコマンドパレットから「Python: Select Interpreter」で `.venv/bin/python` を選択します。

## 3. 動作確認

CLI を実行して環境が正しく構成されているか確認します。

```bash
uv run python -m sample_project
```

## 4. 品質チェックとテスト

- フォーマット: `uv run ruff format .`
- Lint: `uv run ruff check .`
- テスト: `uv run pytest test`

> 変更を加えたら、フォーマット → Lint → テストの順で確認すると安全です。

## 5. ドキュメントビルド

```bash
uv run invoke docs
```

生成された HTML は `docs/build/` 配下に出力されます。ブラウザで開いて内容を確認できます。

## 6. コード編集のヒント (VSCode)

- `.vscode/extensions.json` のレコメンドに従うと必要な拡張機能をまとめて導入できます。
- Ruff をフォーマッターとして使うため、他フォーマッター拡張の自動整形は無効化するか競合しないよう設定してください。

## 7. 自分用プロジェクトへの書き換え

- メタデータ更新: `pyproject.toml` の `[project]` セクションで `name` と `authors` を自分のプロジェクト名・名前に変更します。例: `authors = [{ name = "Your Name" }]`。
- CLI 名変更: `project.scripts` のエントリ（`sample-project`）も新しいパッケージ名に合わせて変更し、`src/sample_project/` ディレクトリ名もリネームします。
- README/ドキュメント: プロジェクトの目的や使用例を README と `docs/source/` のページに反映します。
- ライセンス: 必要に応じてライセンスファイルを追加・更新します。

## 8. 次に行うこと

- `src/sample_project/`（リネーム後のパス）に必要なロジックを追加します。
- 新しいモジュールや関数を作成したら、`test/` に対応する `test_*.py` を追加してください。
- 新しいモジュールや関数を作成したら、 `uv run sphinx-apidoc -o docs/source/sample_project_api src/sample_project` を実行して API ドキュメントを更新します。
- 仕様や手順を文書化する場合は、`docs/source/` に Markdown かノートブックを追加し、`index.md` の `{toctree}` に追記します。
