# 0002. Invoke タスクは複合ワークフローに限定する

- 日付: 2026-09-14
- ステータス: 採用

## 背景

`tasks.py` の Invoke タスクは当初 `test` / `check` / `format` / `docs` のような単独コマンドの 1:1 ラッパーだった。`uv run invoke check` と `uv run ruff check .` では文字数がほとんど変わらず、ラッパーを介する価値が薄い。一方で、Claude Code skill(`/quality-check` / `/create-pr` / `/update-docs`)には「CI と同じ 4 チェックを失敗しても最後まで実行して集計する」「apidoc 再生成後に古い `.rst` を確認する」「ビルド後に warning を確認する」といった複数ステップの手順が prose として埋まっており、人間からは再利用できなかった。

## 検討した選択肢

- **Invoke を完全に削除する**: 依存が 1 つ減るが、`new-project` タスクが Invoke の `Context` に依存しているため argparse + subprocess への書き直しが必要で、コストに見合わない
- **1:1 ラッパーを残したまま複合タスクを足す**: README の導線としては分かりやすいが、価値の薄いタスクが残り続け「何を invoke に置くか」の基準が曖昧になる
- **1:1 ラッパーを削り、複合ワークフローだけを Invoke に置く**: 「複数ステップを束ねる」または「プロジェクト固有の知識(モジュール名・パス)が要る」ものだけをタスクにし、skill はそれを呼ぶ

## 決定

3 つ目を採用する。`tasks.py` には `ci`(4 チェックの継続実行と集計)/ `fix`(Ruff 自動修正 + フォーマット)/ `audit`(`pip-audit`)/ `docs`(`--clean` / `--strict` / `--open`)/ `apidoc`(再生成 + 古いページの削除)/ `adr` のような複合タスクのみを置き、単独コマンドは `uv run pytest` のように直接実行する。

CI(`.github/workflows/tests.yml` / `.gitlab-ci.yml`)は `invoke ci` に統一せず、個別ステップのまま残す。CI の UI でどのチェックが落ちたかを一目で分かる状態を優先した。

## 結果

- `tasks.py` の `CI_CHECKS` は CI ワークフローのミラーであり、CI のチェック内容を変えるときは両方を同期させる
- skill は手順を prose で繰り返さず `uv run invoke ci` などのタスクを呼ぶ。人間と AI エージェントが同じ入口を使う
- 単独コマンドの薄いラッパーを `tasks.py` に追加しない(CONTRIBUTING.md の規則)
