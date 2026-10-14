# Changelog

## v0.1.1

Move browser libraries from `vendor` to `lib`: Go module archives exclude
`vendor` directories. Validate the downloaded package in CI so releases contain
all self-hosted runtime assets.

## v0.1.0

Initial extraction of the blog's content rendering into an independent Hugo module.

- Scoped typography, syntax highlighting, headings, alerts, tables, and media.
- Local fonts, Mermaid, MathJax, and image zoom with no browser CDN requests.
- Three integration partials and feature flags for consuming sites.
- Page-bundle and global-asset images, WebP processing, and MP4 controls.
- Standalone example site and integration checks for isolated consumers.

Site navigation, analytics, subscriptions, comments, and poetry layout remain
in the consuming site. CourierCyr is not included in the public distribution.
