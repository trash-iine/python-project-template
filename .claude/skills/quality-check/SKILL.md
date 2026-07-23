---
name: quality-check
description: CI と同じ 4 チェック (ruff check / ruff format / ty / pytest) を一括実行し、失敗を修正して green にする
allowed-tools: Bash(uv run *) Read Edit
---

# 品質チェック一括実行

CI と同じ 4 チェックをローカルで実行し、すべて green になるまで修正を繰り返す。

## 手順

### 1. チェック実行

以下を順に実行する（前のチェックが失敗しても最後まで実行し、失敗を全部把握してから修正に入る）:

```bash
uv run ruff check .
uv run ruff format --check .
uv run ty check
uv run pytest
```

### 2. 失敗の修正

すべて成功したら結果を報告して終了。失敗があれば以下の方針で修正し、ステップ 1 に戻る。

- **フォーマット違反**: `uv run ruff format .` で自動修正する
- **リント違反**: まず `uv run ruff check --fix .` の自動修正を試し、残りはコード自体の修正を最優先で検討する
- **ルール抑制は最終手段**: どうしても抑制する場合は CONTRIBUTING.md の抑制ポリシーに従う
  - 行単位: 理由コメント付きの `# noqa: <RULE>`
  - ファイル横断: `pyproject.toml` の `per-file-ignores` に理由コメント付きで追加（既存エントリの書式に合わせる）
- **型エラー**: 型ヒントの追加・修正で対応する（公開関数は型ヒント必須）
- **テスト失敗**: テストを弱めるのではなく、原則コード側を直す。doctest（docstring の `Examples:`）の失敗も `pytest` に含まれる点に注意

### 3. 報告

最終的に 4 チェックの結果と、修正した内容（ファイルと変更点）を簡潔に報告する。
