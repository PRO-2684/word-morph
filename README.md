# Word Morph

## Showcase

> [!NOTE]
> Microsoft is a trademark of Microsoft Corporation. This is a joke font and is not affiliated with Microsoft in any way.

1. Open [the website](https://word-morph.pages.dev) in your browser
2. Type `Microsoft` and see `Microslop` below instead

You can grab and use the prebuilt font file [`Microslop.ttf`](./fonts/Microslop.ttf) without having to install anything.

## Usage

```shell
uv run main.py <input-path> word1 word2 -o <output-path>
```

Note that `word1` and `word2` must be of the same length.

## Example

```shell
$ uv run main.py fonts\MicrosoftYaHei.ttf Microsoft Microslop -o fonts\Microslop.ttf
Saved modified font to fonts\Microslop.ttf
```
