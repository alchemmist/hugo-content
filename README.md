# Hugo Content

Hugo Content is a reusable content presentation module for technical writing. It provides Markdown render hooks for images, links, headings, alerts, Mermaid diagrams, and responsive media, together with partials for the page head, content body, and scripts.

The module targets Hugo 0.167.0 or newer and Go 1.23 or newer. It ships its prebuilt browser libraries, so a consuming site does not need npm.

## Use the module

Add the module to a Hugo site:

```toml
[module]
[[module.imports]]
path = "github.com/alchemmist/hugo-content"
```

The module exposes three partials. Use them in this order:

```html
<head>
  {{ partial "content/head.html" . }}
</head>
<body>
  {{ partial "content/body.html" . }}
  {{ partial "content/scripts.html" . }}
</body>
```

`content/head.html` loads the module fonts and stylesheet. `content/body.html` renders `.Content` inside a `div.hc-content`. `content/scripts.html` loads the vendored JavaScript and initializes math, Mermaid, and image zoom when the page uses those features.

The module styles are scoped to `.hc-content`. A site can tune the presentation with these custom properties:

```css
.hc-content {
  --hc-font-body: "Computer Modern Roman", serif;
  --hc-font-code: "JetBrains Mono", monospace;
  --hc-font-ui: system-ui, sans-serif;
  --hc-font-size: 18px;
  --hc-line-height: 1.6;
  --hc-color-text: #222;
  --hc-color-link: #0d47a1;
  --hc-code-background: #f5f5f5;
}
```

The defaults preserve the blog's content typography; the example shell adds spacing and navigation. Page shells, navigation, and prose or poetry layouts remain the responsibility of the host site.

The example site uses the module's local JetBrains Mono face. CourierCyr is specific to the author's blog shell and is not redistributed by this module.

## Run the example

The example is a standalone Hugo site that consumes the parent module through a local Go `replace` directive:

```sh
cd exampleSite
hugo server --port 1315
```

For a clean consumer installation, replace the local directive with a released version and run:

```sh
hugo mod init example.com/my-site
hugo mod get github.com/alchemmist/hugo-content@v0.1.0
```


## Markdown configuration

Set these explicitly in the consuming site's Hugo configuration:

```toml
[markup.highlight]
noClasses = false

[markup.goldmark.extensions.passthrough]
enable = true

[markup.goldmark.extensions.passthrough.delimiters]
block = [['$$', '$$']]
inline = [['$', '$']]
```

Enable `markup.goldmark.renderer.unsafe = true` only if your own trusted content
uses raw HTML, as the example does for details and icon samples.

Images can live in page bundles, global assets, or static files. Global raster
assets and bundle images are resized to at most 1600px and emitted as WebP.
GIF and SVG files pass through unchanged. `![alt|400](image.png)` limits display
width in pixels; `![|85](video.mp4)` displays a video at 85% width.

Pages or sites can disable features with `params.content.zoom = false`,
`params.content.math = false`, or `params.content.mermaid = false`.
For images in a host-owned gallery outside `.hc-content`, add `data-content-zoom`
to that gallery's container. Do not also initialize Medium Zoom or MathJax from
the host when using the module's corresponding feature.

## Development

`make example` starts the example at http://localhost:1315/.
`make check` builds the example and exercises an isolated consumer.
`make vendor` runs `npm ci` and rebuilds the committed browser bundles.
Go and Hugo are the only build dependencies for consumers; Node.js is only
needed when changing the module's vendored JavaScript. All browser dependencies,
fonts, and icons are served locally, including MathJax extensions and Mermaid
chunks. Git and Go are required to fetch a released Hugo module.

Local development of another site can use a `replace` directive in that site's
`go.mod`. Remove the local directive and pin a release before deployment.

## License

Module code is MIT. Font licenses, provenance, and bundled JavaScript notices
are included in `licenses/`. The module has no analytics, comments service,
search service, or dependency on the author's blog.
