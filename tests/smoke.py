import hashlib
import json
import re
import shutil
import subprocess
import tempfile
from pathlib import Path
from urllib.parse import urlsplit


ROOT = Path(__file__).resolve().parents[1]
EXAMPLE = ROOT / "exampleSite"


def check(condition, message):
    if not condition:
        raise AssertionError(message)


def write_config(path, flags):
    path.write_text(
        """baseURL = 'http://localhost:1315/docs/'
locale = 'en-us'
title = 'Hugo Content smoke test'
disableKinds = ['taxonomy', 'term']

[module.hugoVersion]
min = '0.167.0'

[module]
[[module.imports]]
path = 'github.com/alchemmist/hugo-content'

[[module.mounts]]
source = 'content'
target = 'content'
[[module.mounts]]
source = 'layouts'
target = 'layouts'
[[module.mounts]]
source = 'assets'
target = 'assets'
[[module.mounts]]
source = 'static'
target = 'static'

[markup.goldmark.renderer]
unsafe = true

[markup.goldmark.extensions.passthrough]
enable = true

[markup.goldmark.extensions.passthrough.delimiters]
block = [['$$', '$$']]
inline = [['$', '$']]

[params.content]
math = %s
mermaid = %s
zoom = %s

[markup.highlight]
style = 'github'
noClasses = false
""" % (str(flags["math"]).lower(), str(flags["mermaid"]).lower(), str(flags["zoom"]).lower())
    )
    if flags.get("custom_mono"):
        with path.open("a") as output:
            output.write('\n[params.content.typography]\nmonoFamily = "CourierCyr"\n')


def write_base_layout(path):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        """<!doctype html>
<html lang="{{ .Site.Language.Lang }}">
  <head>
    <meta charset="UTF-8" />
    {{ partial "content/head.html" . }}
  </head>
  <body>
    {{ block "main" . }}{{ end }}
    {{ partial "content/scripts.html" . }}
  </body>
</html>
"""
    )


def write_single_layout(path):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        """{{ define "main" }}
<main><article><h1>{{ .Title }}</h1>{{ partial "content/body.html" . }}</article></main>
{{ end }}
"""
    )


def write_content(path, rich):
    path.parent.mkdir(parents=True, exist_ok=True)
    if rich:
        body = """# Rich page

## Supported heading

> [!NOTE]
> A supported alert.

```python
print('syntax')
```

```mermaid
flowchart TD
  A --> B
```

Inline math $a^2$ and a block:

$$x^2$$

![Page bundle](fixture.png)

![Global image](/images/global.png)

![Global gif](/images/demo.gif)

![|80](/images/demo.mp4 "Global video")
"""
    else:
        body = """# Minimal page

This page has ordinary Markdown only.
"""
    path.write_text("---\ntitle: Test\n---\n\n" + body)


def build(flags):
    temp = Path(tempfile.mkdtemp(prefix="hugo-content-smoke-"))
    consumer = temp / "consumer"
    shutil.copytree(EXAMPLE, consumer, ignore=shutil.ignore_patterns("resources", "public"))
    write_config(consumer / "hugo.toml", flags)
    write_base_layout(consumer / "layouts/_default/baseof.html")
    write_single_layout(consumer / "layouts/_default/single.html")
    shutil.rmtree(consumer / "content")
    write_content(consumer / "content/rich/index.md", True)
    write_content(consumer / "content/minimal/index.md", False)
    icon_page = consumer / "content/icons/index.md"
    icon_page.parent.mkdir(parents=True)
    icon_page.write_text("---\ntitle: Test \uf2c6\n---\n\n\ueb1b \ueb1b \ueb1c \U000f0001\n")
    shutil.copy(EXAMPLE / "assets/images/distance-between-vectors.png", consumer / "content/rich/fixture.png")
    static_images = consumer / "static/images"
    static_images.mkdir(parents=True, exist_ok=True)
    shutil.copy(EXAMPLE / "assets/images/distance-between-vectors.png", static_images / "global.png")
    shutil.copy(EXAMPLE / "assets/images/typing-demo-1.gif", static_images / "demo.gif")
    shutil.copy(EXAMPLE / "assets/images/noscreenshare-demo.mp4", static_images / "demo.mp4")
    (consumer / "go.mod").write_text(
        "module smoke-consumer\n\ngo 1.23.0\n\nrequire github.com/alchemmist/hugo-content v0.1.0\n\nreplace github.com/alchemmist/hugo-content => " + str(ROOT) + "\n"
    )
    output = temp / "public"
    subprocess.run(["hugo", "--destination", str(output), "--quiet"], cwd=consumer, check=True)
    return temp, consumer, output


def assert_urls_resolve(html, output):
    for value in re.findall(r'(?:src|href|data-(?:zoom|mermaid|math))="([^"]+)"', html):
        parsed = urlsplit(value)
        if parsed.scheme or parsed.netloc or value.startswith("#"):
            continue
        path = parsed.path
        check(path.startswith("/docs/"), "asset URL is missing the /docs/ base URL: " + value)
        relative = path.removeprefix("/docs/").lstrip("/")
        check((output / relative).exists(), "asset URL does not resolve: " + value)



def range_points(value):
    points = set()
    for item in value.split(","):
        bounds = item.strip().removeprefix("U+").split("-")
        start = int(bounds[0].replace("?", "0"), 16)
        end = int(bounds[-1].replace("?", "F"), 16)
        points.update(range(start, end + 1))
    return points


def assert_font_delivery(html, output, custom_mono=False, icons=()):
    stylesheet = re.search(r'<link rel="stylesheet" href="([^"]+)"', html).group(1)
    css = (output / stylesheet.removeprefix("/docs/")).read_text()
    urls = re.findall(r'url\([\"\']?([^\)\"\']+\.woff2)[\"\']?\)', css)
    manifest = json.loads((ROOT / "assets/hugo-content/fonts/nerd-ranges.json").read_text())
    check(len(urls) == 4 + len(manifest), "expected four text faces and all symbol subsets")
    check("SymbolsNerdFont-Regular" not in css, "full symbol font must not be delivered")
    declared = re.findall(r"unicode-range:\s*([^;]+);", css)
    check([range_points(value) for value in declared] == [range_points(entry["unicodeRange"]) for entry in manifest], "subset ranges changed during rendering")
    covered = set()
    sample_bytes = 0
    for entry in manifest:
        points = range_points(entry["unicodeRange"])
        check(not covered.intersection(points), "symbol subsets overlap")
        check(not any(point < 0x23FB for point in points), "symbol face claims ordinary text")
        covered.update(points)
        data = (ROOT / "assets" / entry["path"]).read_bytes()
        check(hashlib.sha256(data).hexdigest() == entry["sha256"], "subset bytes do not match manifest")
        if points.intersection({0xEB1B, 0xF2C6}):
            sample_bytes += len(data)
    check({0xEB1B, 0xF2C6}.issubset(covered), "homepage icons missing")
    check(sample_bytes < 100000, "homepage icon subsets are too large")
    for url in urls:
        check(url.startswith("/docs/"), "font URL lost base path")
        font = output / url.removeprefix("/docs/")
        check(font.is_file(), "font URL does not resolve: " + url)
        digest = hashlib.sha256(font.read_bytes()).hexdigest()
        check("." + digest + ".woff2" in url, "font URL is not content fingerprinted")
    preloads = re.findall(r'<link rel="preload" href="([^"]+)" as="font" type="font/woff2" crossorigin', html)
    symbol_paths = {entry["path"] for entry in manifest if range_points(entry["unicodeRange"]).intersection(icons)}
    expected_symbols = {url for url in urls if any(Path(path).stem + "." in url for path in symbol_paths)}
    check(len(preloads) == (1 if custom_mono else 2) + len(expected_symbols), "unexpected font preloads")
    check(len(preloads) == len(set(preloads)), "duplicate font preload")
    check({url for url in preloads if "/nerd/" in url} == expected_symbols, "preload only symbol subsets used in content or title")
    if custom_mono:
        check(not any("JetBrainsMono" in url for url in preloads), "custom monospace must not preload bundled UI face")
    check(set(preloads).issubset(urls), "preloads and CSS use different font URLs")
    check(not any("SymbolsNerd" in url for url in preloads), "full symbol font must not preload")
    check("unicode-range:" in css, "symbol font is not restricted to supported glyphs")


def main():
    temp, _, output = build({"math": False, "mermaid": False, "zoom": False, "custom_mono": True})
    try:
        assert_font_delivery((output / "minimal/index.html").read_text(), output, custom_mono=True)
    finally:
        shutil.rmtree(temp)

    temp, _, output = build({"math": True, "mermaid": True, "zoom": True})
    try:
        rich = (output / "rich/index.html").read_text()
        minimal = (output / "minimal/index.html").read_text()
        check("Supported heading" in rich, "heading was not rendered")
        check("markdown-alert--note" in rich, "alert was not rendered")
        check('class="language-python"' in rich, "code language class was not rendered")
        check("<pre class=\"mermaid\">" in rich, "Mermaid block was not rendered")
        check("\\(a^2\\)" in rich and "\\[x^2\\]" in rich, "math passthrough was not rendered")
        check("hc-image" in rich and "content-video" in rich, "media render hooks were not applied")
        check("alchemmist.xyz" not in rich and "remark42" not in rich and "umami" not in rich, "blog-specific hardcode leaked into output")
        check("data-mermaid=" in rich and "data-math=" in rich, "enabled runtime flags are missing")
        check("data-mermaid=" not in minimal and "data-math=" not in minimal, "empty runtime flags leaked into minimal page")
        assert_font_delivery(rich, output)
        assert_font_delivery(minimal, output)
        assert_font_delivery((output / "icons/index.html").read_text(), output, icons=(0xEB1B, 0xEB1C, 0xF2C6, 0xF0001))
        assert_urls_resolve(rich, output)
        assert_urls_resolve(minimal, output)
    finally:
        shutil.rmtree(temp)

    temp, _, output = build({"math": False, "mermaid": False, "zoom": False})
    try:
        rich = (output / "rich/index.html").read_text()
        scripts = re.search(r"<script[^>]+data-hc-runtime[^>]*>", rich)
        check(scripts is not None, "runtime script is missing")
        check("data-mermaid=" not in scripts.group(0) and "data-math=" not in scripts.group(0), "disabled runtime flags are present")
        check("data-zoom=" not in scripts.group(0), "disabled zoom flag is present")
    finally:
        shutil.rmtree(temp)


if __name__ == "__main__":
    main()
    print("smoke test passed")
