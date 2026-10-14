import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

revision = sys.argv[1]
with tempfile.TemporaryDirectory(prefix="hugo-content-package-") as directory:
    environment = {**os.environ, "GOMODCACHE": directory, "GOWORK": "off"}
    result = subprocess.check_output(
        ["go", "mod", "download", "-json", f"github.com/alchemmist/hugo-content@{revision}"],
        env=environment,
        text=True,
    )
    module = Path(json.loads(result)["Dir"])
    for relative in [
        "static/hugo-content/lib/mermaid.js",
        "static/hugo-content/lib/zoom.js",
        "static/hugo-content/lib/mathjax/tex-svg.js",
        "static/hugo-content/lib/mathjax/ui/safe.js",
        "static/hugo-content/fonts/cmu.serif-roman.woff2",
        "layouts/partials/content/body.html",
    ]:
        if not (module / relative).is_file():
            raise AssertionError(f"Downloaded module is missing {relative}")
    if not list((module / "static/hugo-content/lib/chunks").glob("*.js")):
        raise AssertionError("Downloaded module is missing Mermaid chunks")
print("downloaded package passed")
