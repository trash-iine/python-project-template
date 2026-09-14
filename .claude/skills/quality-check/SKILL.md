---
name: quality-check
description: CI と同じ 4 チェック (ruff check / ruff format / ty / pytest) を一括実行し、失敗を修正して green にする
allowed-tools: Bash(uv run *) Read Edit
---

# 品質チェック一括実行

CI と同じ 4 チェックをローカルで実行し、すべて green になるまで修正を繰り返す。

## 手順

### 1. チェック実行

CI と同じ 4 チェック（`ruff check` / `ruff format --check` / `ty check` / `pytest`）を一括実行する。失敗があっても最後まで実行され、末尾の summary に各チェックの成否が並ぶので、失敗を全部把握してから修正に入る:

```bash
uv run invoke ci
```

### 2. 失敗の修正

すべて成功したら結果を報告して終了。失敗があれば以下の方針で修正し、ステップ 1 に戻る。

- **フォーマット違反・リント違反**: まず `uv run invoke fix`（`ruff check --fix` + `ruff format`）で自動修正し、残ったリント違反はコード自体の修正を最優先で検討する
  - D417（`Args:` の引数漏れ）は docstring に `name (type): 説明` 形式で引数説明を追加して直す
- **ルール抑制は最終手段**: どうしても抑制する場合は CONTRIBUTING.md の抑制ポリシーに従う
  - 行単位: 理由コメント付きの `# noqa: <RULE>`
  - ファイル横断: `pyproject.toml` の `per-file-ignores` に理由コメント付きで追加（既存エントリの書式に合わせる）
- **型エラー**: 具体型の修正で対応する。`cast` / `TypeVar` / `Protocol` などの typing 機構や `# ty: ignore` で回避しない（抑制は理由コメント付きの最終手段）
- **テスト失敗**: テストを弱めるのではなく、原則コード側を直す。doctest（docstring の `Examples:`）の失敗も `pytest` に含まれる点に注意

### 3. 報告

最終的に 4 チェックの結果と、修正した内容（ファイルと変更点）を簡潔に報告する。
