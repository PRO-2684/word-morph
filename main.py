import argparse
from io import StringIO
from pathlib import Path

from fontTools.feaLib.builder import addOpenTypeFeatures
from fontTools.ttLib import TTFont


def glyph_name(ch: str) -> str:
    code = ord(ch)
    if ch.isascii() and (ch.isalpha() or ch.isdigit()):
        return ch
    if code <= 0xFFFF:
        return f"uni{code:04X}"
    return f"u{code:06X}"


def build_feature(word_from: str, word_to: str) -> str:
    if len(word_from) != len(word_to):
        raise ValueError("The two words must have the same length.")
    if not word_from:
        raise ValueError("Words must not be empty.")

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
    lookup_defs: list[tuple[str, str, str]] = []

    for src_ch, dst_ch in zip(word_from, word_to):
        src = glyph_name(src_ch)
        dst = glyph_name(dst_ch)
        key = (src, dst)
        if dst != src and key not in lookup_names:
            name = f"L_{len(lookup_names)}"
            lookup_names[key] = name
            lookup_defs.append((name, src, dst))

    for name, src, dst in lookup_defs:
        lines.extend(
            [
                f"lookup {name} {{",
                f"    sub {src} by {dst};",
                f"}} {name};",
                "",
            ]
        )

    marked_input = " ".join(f"{glyph_name(ch)}'" for ch in word_from)
    contextual_rules = []
    for src_ch, dst_ch in zip(word_from, word_to):
        if dst_ch != src_ch:
            src = glyph_name(src_ch)
            lookup_name = lookup_names[(src, glyph_name(dst_ch))]
            contextual_rules.append(f"{src}' lookup {lookup_name}")
        else:
            contextual_rules.append(f"{glyph_name(src_ch)}'")
    contextual_rule = " ".join(contextual_rules)

    lines.extend(
        [
            "feature calt {",
            "    lookup WORD_SUB {",
            f"        ignore substitute @LETTER {marked_input};",
            f"        ignore substitute {marked_input} @LETTER;",
            "",
            f"        sub {contextual_rule};",
            "    } WORD_SUB;",
            "} calt;",
            "",
        ]
    )

    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("font", help="Input font path")
    parser.add_argument("source", help="Source word, e.g. banana")
    parser.add_argument("target", help="Target word, e.g. orange")
    parser.add_argument(
        "-o",
        "--output",
        help="Output font path; defaults to <input-stem>-mod<suffix>",
    )
    parser.add_argument(
        "--print-feature",
        action="store_true",
        help="Print generated feature text",
    )
    args = parser.parse_args()

    if len(args.source) != len(args.target):
        raise SystemExit("source and target must have the same length")

    font_path = Path(args.font)
    if args.output:
        output_path = Path(args.output)
    else:
        output_path = font_path.with_name(f"{font_path.stem}-mod{font_path.suffix}")

    feature_text = build_feature(args.source, args.target)
    print("Generated OpenType feature text:")
    print(feature_text)

    if args.print_feature:
        print(feature_text)

    font = TTFont(font_path)
    addOpenTypeFeatures(font, StringIO(feature_text))
    font.save(output_path)

    print(f"Saved modified font to {output_path}")


if __name__ == "__main__":
    main()
