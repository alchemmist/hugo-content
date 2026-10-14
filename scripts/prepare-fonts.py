import argparse
from pathlib import Path

from fontTools.ttLib import TTFont

parser = argparse.ArgumentParser()
parser.add_argument("source", type=Path)
parser.add_argument("nerd_font", type=Path)
args = parser.parse_args()
destination = Path(__file__).resolve().parents[1] / "static/hugo-content/fonts"
destination.mkdir(parents=True, exist_ok=True)
fonts = [
    ("cmu.serif-roman.woff2", "Hugo Content Serif", "Regular"),
    ("cmu.serif-bold.woff2", "Hugo Content Serif", "Bold"),
    ("cmu.typewriter-text-regular.woff2", "Hugo Content Typewriter", "Regular"),
]
for filename, family, style in fonts:
    font = TTFont(args.source / filename)
    names = {1: family, 2: style, 3: f"{family}-{style}", 4: f"{family} {style}", 6: f"{family.replace(' ', '')}-{style}", 16: family, 17: style}
    for record in font["name"].names:
        if record.nameID in names:
            record.string = names[record.nameID].encode(record.getEncoding())
    font.flavor = "woff2"
    font.save(destination / filename)
font = TTFont(args.nerd_font)
font.flavor = "woff2"
font.save(destination / "SymbolsNerdFont-Regular.woff2")
