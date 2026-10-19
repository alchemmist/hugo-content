# Font provenance

CMU Serif and Typewriter are derived from the Computer Modern Unicode webfonts
in alchemmist/blog at commit 3b7ab95. The typewriter source has U+007E removed
from its character map by that project. Internal family names are changed to
Hugo Content Serif and Hugo Content Typewriter; copyright notices are retained.
See CMU-OFL.txt. CSS family aliases retain the existing typography API.

JetBrains Mono Regular is from the same blog source and is distributed under
JetBrainsMono-OFL.txt. CourierCyr and Open Graph font files are not included.

Symbols Nerd Font Regular is converted without glyph changes from Nerd Fonts
v3.3.0, NerdFontsSymbolsOnly.zip, SymbolsNerdFont-Regular.ttf.
Original TTF SHA-256: d7cda3a97797a3764b80a8df8b54f2bd7229a12cbc75c9c74f31496866c6eee9.
Source: https://github.com/ryanoasis/nerd-fonts/releases/tag/v3.3.0
See Nerd-Fonts-MIT.txt.

Font conversion uses scripts/prepare-fonts.py with fonttools 4.67.0 and brotli
1.2.0. The script accepts the blog's original font directory and the official
Symbols TTF. Consumers use the committed WOFF2 files without conversion tools.

The original full Symbols WOFF2 remains the source asset. Browser delivery uses
256-codepoint Unicode-page subsets in `assets/hugo-content/fonts/nerd/` with
exact supported Unicode ranges in `nerd-ranges.json`. Ordinary text codepoints
are intentionally excluded, matching the original CSS ranges. Font notices
are retained in each subset. Regenerate with `make subset-fonts`; verify exact
reproducibility and complete supported glyph coverage with `make check-font-subsets`.
Both commands use isolated, pinned fonttools and Brotli dependencies through uv;
normal Hugo builds need neither Python font tooling nor uv.
