---
name: create-pr
description: ブランチ規約チェック → 品質チェック → gitmoji コミット → push → 日本語 PR 作成までを一貫して行う
allowed-tools: Bash(git *) Bash(gh *) Bash(uv run *)
---

# PR 作成フロー

現在の変更をリポジトリ規約（CONTRIBUTING.md）に沿ってコミットし、PR 作成まで行う。

## 手順

### 1. ブランチ確認

`git branch --show-current` と `git status` で現在地を確認する。

- **`main` 上にいる場合**: 直接コミット禁止。変更内容から `<type>/<short-kebab-description>` 形式のブランチ名を提案して切ってから進む
- **ブランチ名が規約に従っていない場合**: リネーム（`git branch -m`）を提案する
- type は `feature|fix|docs|refactor|test|ci|chore` のいずれか（コミットの gitmoji カテゴリと対応させる）

### 2. 品質チェック

CI と同じ 4 コマンドを実行する。失敗があれば `/quality-check` skill の方針で修正してから先へ進む:

```bash
uv run ruff check .
uv run ruff format --check .
uv run ty check
uv run pytest
```

### 3. コミット

- gitmoji プレフィックス + 英語・現在形・72 文字以内（例: `✨ add sample_add validation`）
- 絵文字は CONTRIBUTING.md の対応表に従う: ✨新機能 / 🐛バグ修正 / 📝ドキュメント / ✅テスト / 🎨整形・構造改善 / 🔧設定 / 👷CI / 📦️依存関係
- 独立した変更が混ざっている場合は意味単位でコミットを分ける
- 開発規則を変更した場合、CONTRIBUTING.md と AGENTS.md を同一 PR 内で更新済みか確認する

### 4. push と PR 作成

1. `git push -u origin <branch>` で push する
2. リモートが **GitHub** の場合: `gh pr create` で PR を作成する。本文は **日本語** で、`.github/PULL_REQUEST_TEMPLATE.md` の構成に従う:
   - **変更概要**: 何を・なぜ。関連 Issue があれば参照
   - **実行したコマンドと結果**: ステップ 2 の 4 チェックを、実際に実行して成功したものだけチェック済み `[x]` にする
   - **スクリーンショット / サンプル出力**: ドキュメントや CLI 出力の変更時のみ（なければセクションごと削除）
   - **チェックリスト**: 実際に確認した項目のみ `[x]` にする
3. リモートが **GitLab** の場合: `gh` は使えないため、push 出力に表示される MR 作成 URL を案内し、同じ構成の日本語説明文を貼り付け用に提示する

### 5. 報告

PR / MR の URL と、コミット内容の要約を報告する。
