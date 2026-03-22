from pathlib import Path

from fontTools.feaLib.builder import addOpenTypeFeatures
from fontTools.ttLib import TTFont

FONT_PATH = Path("fonts/MicrosoftYaHei.ttf")
FEATURE_PATH = Path("test.fea")
OUTPUT_PATH = Path("fonts/yahei-mod.ttf")


def glyph_name(ch: str) -> str:
    code = ord(ch)
    if 0x20 <= code <= 0x7E and ch.isalnum():
        return ch
    return f"uni{code:04X}"


def build_feature(word_from: str, word_to: str) -> str:
    if len(word_from) != len(word_to):
        raise ValueError("The two words must have the same length.")

    lines: list[str] = [
        "languagesystem DFLT dflt;",
        "languagesystem latn dflt;",
        "",
        "@LETTER = [",
        "    A B C D E F G H I J K L M N O P Q R S T U V W X Y Z",
        "    a b c d e f g h i j k l m n o p q r s t u v w x y z",
        "];",
        "",
    ]

    lookup_names: dict[tuple[str, str], str] = {}
    lookup_order: list[tuple[str, str, str]] = []

    for src, dst in zip(word_from, word_to):
        key = (glyph_name(src), glyph_name(dst))
        if key not in lookup_names:
            lookup_name = f"L_{len(lookup_names)}"
            lookup_names[key] = lookup_name
            lookup_order.append((lookup_name, key[0], key[1]))

    for lookup_name, src, dst in lookup_order:
        lines.extend(
            [
                f"lookup {lookup_name} {{",
                f"    sub {src} by {dst};",
                f"}} {lookup_name};",
                "",
            ]
        )

    marked_from = " ".join(f"{glyph_name(ch)}'" for ch in word_from)
    context_parts = [
        f"{glyph_name(src)}' lookup {lookup_names[(glyph_name(src), glyph_name(dst))]}"
        for src, dst in zip(word_from, word_to)
    ]

    lines.extend(
        [
            "feature calt {",
            "    lookup WORD_SUB {",
            f"        ignore substitute @LETTER {marked_from};",
            f"        ignore substitute {marked_from} @LETTER;",
            "",
            f"        sub {' '.join(context_parts)};",
            "    } WORD_SUB;",
            "} calt;",
            "",
        ]
    )

    return "\n".join(lines)


def main():
    word_from = "banana"
    word_to = "orange"

    feature_text = build_feature(word_from, word_to)
    FEATURE_PATH.write_text(feature_text, encoding="utf-8")
    print(f"Generated {FEATURE_PATH}")

    font = TTFont(FONT_PATH)
    addOpenTypeFeatures(font, str(FEATURE_PATH))
    font.save(OUTPUT_PATH)

    print(f"Saved modified font to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
