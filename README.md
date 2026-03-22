# Word Morph

## Showcase

1. Clone this repo
2. Open `index.html` in your browser
3. Type `Microsoft` and see `Microslop` below instead

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
