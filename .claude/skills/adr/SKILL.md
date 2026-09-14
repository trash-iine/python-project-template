---
name: adr
description: 会話で行った設計判断を ADR (docs/source/adr/) として記録する (invoke adr で生成し、背景・選択肢・決定・結果を埋める)
argument-hint: "[slug]"
allowed-tools: Bash(uv run *) Read Write Edit
---

# ADR 作成

会話の中で行った設計判断を Architecture Decision Record として `docs/source/adr/` に残す。規則そのものは CONTRIBUTING.md に書き、ADR には **理由と検討した選択肢** を書く(CONTRIBUTING.md「設計判断の記録 (ADR)」)。

## 手順

### 1. slug とタイトルを決める

- **slug**: 英語 kebab-case(例: `limit-invoke-tasks-to-composite-workflows`)。`$ARGUMENTS` に渡されていればそれを使う
- **タイトル**: 日本語で、判断内容が一文で分かるもの(例: 「Invoke タスクは複合ワークフローに限定する」)
- 既存の ADR を置き換える判断かどうかを `docs/source/adr/` の一覧で確認する

両方をユーザーに提示して確認してから進む。

### 2. ファイル生成

```bash
uv run invoke adr <slug> --title "<タイトル>"
```

採番とテンプレート展開が自動で行われ、`docs/source/adr/NNNN-<slug>.md` が作られる(一覧ページは glob で拾うので toctree の編集は不要)。

### 3. 本文を埋める

生成されたファイルの各セクションを日本語で埋める:

- **背景**: どんな問題・制約があり、なぜ今この判断が必要になったか
- **検討した選択肢**: 会話で **実際に比較した** 選択肢だけを、利点・欠点つきで列挙する。検討していない選択肢を捏造しない
- **決定**: 何を選んだか、決め手は何か
- **結果**: 生じる影響・トレードオフ・今後守るべき運用

ユーザーと合意済みの判断であれば「ステータス」を `採用` にする。まだ議論中なら `提案中` のままにする。

### 4. 置き換えの処理

既存の ADR を上書きする判断なら、旧 ADR のステータス行を `NNNN により置換`(NNNN は新 ADR の番号)に更新する。旧 ADR の本文は書き換えない。

### 5. ビルド確認と報告

```bash
uv run invoke docs --strict
```

warning がないことを確認し、作成した ADR のパスと要約を報告する。規則が変わる判断なら、CONTRIBUTING.md / AGENTS.md / 該当 skill を同一 PR で更新する必要がある旨も添える。
