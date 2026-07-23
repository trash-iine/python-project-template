---
name: update-docs
description: Sphinx ドキュメントの更新 (API リファレンス再生成・新規ページ追加・ローカルビルド確認) を定型手順で行う
allowed-tools: Bash(uv run *) Read Write Edit
---

# ドキュメント更新

Sphinx + MyST ドキュメントを規約（CONTRIBUTING.md「ドキュメント規約」）に沿って更新する。

## 手順

### 1. 変更種別の判定

依頼内容から該当する作業をすべて行う:

- **`src/` のモジュール追加・リネーム後** → ステップ 2
- **解説ページの新規追加** → ステップ 3
- **既存ページの編集のみ** → ステップ 4 へ直行

### 2. API リファレンス再生成

```bash
uv run invoke update-apidoc
```

`docs/source/*.rst` が再生成される。リネーム時は古いモジュールの `.rst` が残っていないか確認し、残っていれば削除する。

### 3. 新規ページ追加

- ページは `docs/source/` に Markdown (MyST) で作成する。解説ページの本文は **日本語**
- `docs/source/index.md` の `{toctree}` に必ず追加する（追加漏れは次ステップのビルドで "document isn't included in any toctree" warning として検出される）
- **セットアップ手順・使い方は README.md が唯一の情報源**。`docs/` 配下に重複させない（API リファレンスと記法例のみを置く）

### 4. ローカルビルド確認

```bash
uv run invoke docs
```

- warning が出ないことを確認する（出た場合は解消する）
- 生成物は `docs/build/html/` に出力される（git 管理外）。必要に応じて `docs/build/html/index.html` の内容を確認する

### 5. 報告

変更したページ・再生成したファイルと、ビルド結果（warning の有無）を報告する。`main` へのマージ後は Pages に自動デプロイされることも必要なら添える。
