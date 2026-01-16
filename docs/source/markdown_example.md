# Markdown Example (MyST)

この章では Sphinx で使える Markdown/MyST の一般的なパターンを紹介します。

## 基本記法

- 見出し: `#` / `##` / `###` で階層を作ります。
- 強調: `**bold**`、`*italic*`。
- 箇条書き: `- item` でリスト、`1.` で番号付きリスト。
- リンク: `[Sphinx](https://www.sphinx-doc.org/)`。
- 画像: `![alt](path/to/image.png)`（パスは `docs/source/` 基準）。

## コードとブロック

行内コードはバッククォートで囲みます（例: `sample_project`）。複数行はフェンスを使います。

```python
from sample_project.sample_add import sample_add

print(sample_add(2, 3))
```

## 引用と注意書き

> 引用は `>` で始めます。文章の抜粋やメモに便利です。

```{note}
MyST のディレクティブで注記を入れられます。
```

## 表

| 項目   | 説明           |
| ------ | -------------- |
| A      | サンプルの A   |
| B      | サンプルの B   |

## ToC への追加

新しいページを追加したら、`docs/source/index.md` の `{toctree}` にファイル名を追記すると、ナビゲーションに表示されます。
