import argparse
import hashlib
import io
import json
from pathlib import Path

from fontTools import subset
from fontTools.ttLib import TTFont


ROOT = Path(__file__).resolve().parents[1]
FONTS = ROOT / "assets/hugo-content/fonts"
SOURCE = FONTS / "SymbolsNerdFont-Regular.woff2"
RANGES = [(0x23FB, 0x23FE), (0x2630, 0x2630), (0x2665, 0x2665), (0x26A1, 0x26A1), (0x276C, 0x2771), (0x2B58, 0x2B58), (0xE000, 0xF8FF), (0xF0000, 0xFFFFD), (0x100000, 0x10FFFD)]


def unicode_ranges(points):
    runs = []
    for point in sorted(points):
        if runs and point == runs[-1][1] + 1:
            runs[-1][1] = point
        else:
            runs.append([point, point])
    return ", ".join(f"U+{start:X}" if start == end else f"U+{start:X}-{end:X}" for start, end in runs)


def generate(check):
    with TTFont(SOURCE, recalcTimestamp=False) as source:
        expected = {point for point in source.getBestCmap() if any(start <= point <= end for start, end in RANGES)}
    blocks = {}
    for point in sorted(expected):
        blocks.setdefault(point // 256, []).append(point)
    manifest = []
    covered = set()
    generated = {}
    for block, points in blocks.items():
        font = TTFont(SOURCE, recalcTimestamp=False)
        options = subset.Options()
        options.recalc_timestamp = False
        options.canonical_order = True
        options.name_IDs = [0, 1, 2, 3, 4, 5, 6, 13, 14, 16, 17]
        subsetter = subset.Subsetter(options=options)
        subsetter.populate(unicodes=points)
        subsetter.subset(font)
        stream = io.BytesIO()
        font.save(stream, reorderTables=True)
        data = stream.getvalue()
        with TTFont(io.BytesIO(data)) as result:
            actual = set(result.getBestCmap())
        if actual != set(points) or covered.intersection(actual):
            raise ValueError(f"incorrect glyph coverage in block {block:X}")
        covered.update(actual)
        path = f"nerd/symbols-{block * 256:06x}.woff2"
        generated[FONTS / path] = data
        manifest.append({"path": f"hugo-content/fonts/{path}", "unicodeRange": unicode_ranges(points), "sha256": hashlib.sha256(data).hexdigest()})
        font.close()
    if covered != expected:
        raise ValueError("incomplete symbol coverage")
    generated[FONTS / "nerd-ranges.json"] = (json.dumps(manifest, indent=2) + "\n").encode()
    extras = set((FONTS / "nerd").glob("*.woff2")) - set(generated)
    if check:
        mismatches = [str(path.relative_to(ROOT)) for path, data in generated.items() if not path.exists() or path.read_bytes() != data]
        if mismatches or extras:
            raise ValueError(f"generated assets differ: {mismatches}; extra assets: {sorted(extras)}")
    else:
        (FONTS / "nerd").mkdir(exist_ok=True)
        for path in extras:
            path.unlink()
        for path, data in generated.items():
            path.write_bytes(data)
    print(f"Verified {len(expected)} codepoints in {len(blocks)} deterministic subsets")
    sample = {point // 256 for point in (0xEB1B, 0xF2C6)}
    total = sum(len(generated[FONTS / f"nerd/symbols-{block * 256:06x}.woff2"]) for block in sample)
    print(f"EB1B + F2C6 transfer: {total:,} bytes; original: {SOURCE.stat().st_size:,} bytes")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    generate(parser.parse_args().check)
