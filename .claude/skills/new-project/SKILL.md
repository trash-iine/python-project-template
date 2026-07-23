---
name: new-project
description: このテンプレートから新プロジェクトを生成する (invoke new-project の対話的ガイド)
argument-hint: "[dest-dir]"
allowed-tools: Bash(uv run *) Bash(ls *) Read
---

# new-project 生成ガイド

テンプレート専用タスク `invoke new-project`（実装: `template_tasks.py`）で、このリポジトリを新プロジェクトとして複製・リブランドする。

## 手順

### 1. パラメータ確認

`$ARGUMENTS` に生成先ディレクトリが渡されていればそれを使う。不足している情報はユーザーに確認する:

- **dest**（必須）: 生成先ディレクトリ。既存パスは指定不可
- **プロジェクト名** `-p/--project-name`: 省略時は dest のベース名。モジュール名（小文字 + `_`）に変換できる名前であること
- **著者名** `--author`: 省略時は `git config user.name` から解決
- **リモート URL** `--remote-url`: 省略可。指定すると `origin` に設定される
- **git 初期化** `--no-git`: 省略時は git init + 初回コミット（`🎉 init`）まで行う

### 2. dry-run で確認

まず必ず `--dry-run` で処理内容（コピー・置換・リネーム対象）を表示し、ユーザーに見せる:

```bash
uv run invoke new-project -d <dest> [-p <name>] [--author <author>] [--remote-url <url>] --dry-run
```

### 3. 本実行

内容に問題がなければ `--dry-run` を外して実行する。処理内容: ファイルコピー（テンプレート専用ファイルは除外）→ プロジェクト名・著者のリブランド → `src/` モジュールと docs のリネーム → `uv lock` 再生成 → git 初期化。

### 4. 生成後の案内

生成先での初期セットアップ手順を案内する:

```bash
cd <dest>
uv sync --dev
uv run pre-commit install
```

- `--remote-url` 未指定なら、リモート追加 (`git remote add origin <url>`) と push もあわせて案内する
- `uv lock` が失敗していた場合（実行時に Warning 表示）は生成先で `uv sync --dev` により再生成されることを伝える

### 5. 報告

生成先パス・プロジェクト名・実行したオプションを報告する。
