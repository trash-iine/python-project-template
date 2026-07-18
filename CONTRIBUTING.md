# コントリビューションガイド

本書は `sample-project` の開発規則(コーディング規約・ワークフロー)を定めるものです。**セットアップ手順と使い方は [README.md](README.md) が唯一の情報源**であり、本書では繰り返しません。AI エージェント向けの要約は [AGENTS.md](AGENTS.md)(英語)にあります。記述が矛盾した場合は、本書と `pyproject.toml` を正とします。

## 言語ポリシー

- コード・識別子・コメント・docstring・コミットメッセージ: **英語**
- ユーザー向けドキュメント(README、`docs/source/` の解説ページ): **日本語**
- PR / MR の説明文・Issue・レビューコメント: **日本語**
- 本書は日本語で記述し、AGENTS.md は AI 向けのため英語で記述します

## 開発ワークフロー

- `main` への直接コミットは禁止です。必ずブランチを切り、PR(GitHub)/ MR(GitLab)を作成してください。
- ブランチ名は `<type>/<short-kebab-description>`(英語・ケバブケース)とします。`type` はコミットの gitmoji カテゴリに対応します。

  | type | 対応する gitmoji | 用途 |
  | --- | --- | --- |
  | `feature/` | ✨ | 新機能 |
  | `fix/` | 🐛 | バグ修正 |
  | `docs/` | 📝 | ドキュメント |
  | `refactor/` | 🎨 ♻️ | リファクタリング・構造改善 |
  | `test/` | ✅ | テスト |
  | `ci/` | 👷 | CI |
  | `chore/` | 🔧 📦️ | 設定・依存関係 |

  例: `docs/add-contributing-guide`、`fix/handle-none-input`

- マージ条件: CI の 4 チェック(後述)がグリーンであること + レビュー 1 名以上の承認(1 人で開発している場合はセルフマージ可)。
- マージ後はブランチを削除してください。

## コミット規約

- gitmoji プレフィックス + 英語・現在形・72 文字以内で記述します(例: `✨ add sample_add validation`)。
- 使用する絵文字の対応表:

  | 絵文字 | 用途 |
  | --- | --- |
  | ✨ | 新機能 |
  | 🐛 | バグ修正 |
  | 📝 | ドキュメント |
  | ✅ | テスト |
  | 🎨 | コード整形・構造改善 |
  | 🔧 | 設定 |
  | 👷 | CI |
  | 📦️ | 依存関係・パッケージング |
  | 🎉 | 初回コミット |
  | 🚧 | 作業途中 |

- 関連する Issue / PR はコミット本文で参照してください。

## コーディング規約

- **リント設定の唯一の情報源は `pyproject.toml` です**(Ruff `select = ["ALL"]`、`line-length = 120`)。本書では個々のルールを列挙しません。
- 命名: モジュール・関数は `snake_case`、クラスは `PascalCase`。
- 公開関数には型ヒントを必須とします(型チェッカーは `ty`)。
- docstring は Google スタイル(Napoleon)で記述し、公開関数には doctest 形式の `Examples:` セクションを付けます。参照例: `src/sample_project/sample_add.py`
- 例外送出はメッセージを変数に束ねてから送出します(Ruff EM101 / EM102 準拠):

  ```python
  msg = f"Invalid types: a={type(a)}, b={type(b)}"
  raise TypeError(msg)
  ```

- ルール抑制ポリシー: まずコードの修正を検討してください。どうしても抑制する場合は、行単位なら理由コメント付きの `# noqa: <RULE>`、ファイル横断なら `pyproject.toml` の `per-file-ignores` に**理由コメント付き**で追加します(既存エントリの書式に合わせること)。

## テスト規約

- テストは `test/`(単数形)配下に `test_*.py` として配置し、ソースモジュールと対応させます。
- テスト関数名は `test_<unit>_<expectation>` とします(例: `test_sample_add_type_error`)。
- 入力ペアやエラー経路の検証には `pytest.mark.parametrize` を優先して使います。
- テストはハーメティックに保ちます(ネットワークアクセス・外部ファイルシステムへの書き込み禁止)。
- テスト内の `assert` とマジックナンバーは許可済みです(`per-file-ignores` の S101 / PLR2004)。
- docstring の `Examples:`(doctest)は `--doctest-modules` により `pytest` 実行時に自動検証されます。例が古くならないよう、動作する形で維持してください。
- カバレッジは `pytest-cov` で計測され、実行時に表示されます。合格ライン(ゲート)はテンプレートでは未設定です。コードが増えたら `pyproject.toml` のコメントアウトされた `fail_under` を有効化してください。

## ドキュメント規約

- ドキュメントは Sphinx + MyST + nbsphinx で生成します。ローカルビルドは `uv run invoke docs`。
- `src/` のモジュールを追加・リネームしたら `uv run invoke update-apidoc` で API リファレンスを再生成してください。
- 新規ページは `docs/source/` に置き、`docs/source/index.md` の `{toctree}` に必ず追加します。
- セットアップ手順は README.md のみに記載します(`docs/` 配下に重複させない)。
- `main` への push で GitHub Pages / GitLab Pages に自動デプロイされます。

## CI とローカルチェック

- セットアップ後に `uv run pre-commit install` を一度実行してください。コミット時に Ruff の自動修正・フォーマットと基本的な検査(YAML / TOML 構文、行末空白など)が自動実行されます。
  - フックは高速な自動修正系のみです。`ty` や `pytest` は実行時間が長いためフックに含めず、CI で担保します。CI では Ruff を直接実行しているため、pre-commit を CI で重ねて実行することもしません。
- push 前に CI と同じ 4 コマンドをローカルで通してください。

```bash
$ uv run ruff check .
$ uv run ruff format --check .
$ uv run ty check
$ uv run pytest
```

- CI では上記に加えて依存パッケージの脆弱性監査(`pip-audit`)が実行されます(GitHub Actions では週次スケジュールでも実行)。
- ショートカットとして Invoke タスク(`uv run invoke test|check|format|docs|update-apidoc`)も利用できます。

## プルリクエスト / マージリクエスト

- 説明文(日本語)には次を含めてください:
  - 変更概要
  - 実行したコマンドとその結果
  - ドキュメントや CLI 出力の変更時は、スクリーンショットまたはサンプル出力
- 開発規則を変更した場合は、**同一 PR 内で本書と AGENTS.md の両方を更新**してください。

<!-- template-only-start -->
## テンプレートのメンテナンス

- このリポジトリはプロジェクトテンプレート(`trash-iine/python-project-template`)を兼ねています。
- `new-project` タスクとその補助関数はテンプレート専用モジュール `template_tasks.py` にあり、テストは `test/test_template_tasks.py` にあります。両ファイルは `COPY_EXCLUDES` に登録されており、派生プロジェクトにはコピーされません。テンプレート専用のファイルを増やす場合は `COPY_EXCLUDES` に追加してください。
- Markdown を編集する際は `<!-- template-only-start -->` / `<!-- template-only-end -->` / `<!-- template-only-line -->` マーカーを壊さないでください。テンプレート固有の記述を追加する場合はマーカーで囲みます(`new-project` タスクが派生プロジェクトから自動で取り除きます)。
- マーカーは Markdown 以外にも `template_tasks.py` の `STRIP_MARKER_FILES` に登録されたファイル(`tasks.py`、`CODEOWNERS`)で有効です。`#` コメント形式でも機能します。
- テンプレートに関わる変更後は `uv run invoke new-project -d <tmp-dir> --dry-run` で処理内容を確認してください。
<!-- template-only-end -->
