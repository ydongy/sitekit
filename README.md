# sitekit

[![CI](https://github.com/ydongy/sitekit/actions/workflows/ci.yml/badge.svg)](https://github.com/ydongy/sitekit/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Release](https://img.shields.io/github/v/release/ydongy/sitekit)](https://github.com/ydongy/sitekit/releases)

Shared generator and checks for static, multilingual product websites. Python standard library only; the
output is plain HTML committed to each site repository.

## Features

| Path | Purpose |
|---|---|
| `sitekit/core.py` | `Site` settings, the `Page` base class (head with canonical, hreflang and Open Graph; header; footer; FAQ; legal pages; changelog), and `build()` which writes every page, `404.html`, `lang.js`, `sitemap.xml` and `robots.txt` |
| `sitekit/check_i18n.py` | Every language against English: structure, HTML tags, links, placeholders, no dashes; optional `i18n/check-config.json` |
| `sitekit/check_site.py` | Every language has every page, links and anchors resolve, nothing violates the Content-Security-Policy |
| `sitekit/preview.py` | Local server that behaves like Cloudflare static assets |
| `vendor.sh` | Copies `sitekit/` into a site repository as `scripts/sitekit/` |

## Quick start

Requires Python 3.10 or newer (CI runs 3.12) and bash. There is nothing to install: sitekit is not published to
a package index. Consumers vendor a copy of it.

```bash
# in the site repository
<path to sitekit>/vendor.sh .
python3 scripts/sitekit/check_i18n.py
python3 scripts/build.py
python3 scripts/sitekit/check_site.py
```

`vendor.sh <site-repo>` replaces `<site-repo>/scripts/sitekit/` with the `.py` files from `sitekit/` and writes
`scripts/sitekit/VERSION`. That file holds the sitekit **git commit hash** the copy came from (plus
`(uncommitted changes)` if the working tree was dirty). It records provenance of the vendored copy and is
independent of sitekit's release version (`vX.Y.Z` tags).

## Usage

A site owns its copy of `i18n/` and `changelog.json`, its styles and assets, and `scripts/build.py`: a
`Site(...)` and a `Page` subclass implementing `home()`. Per-product differences are hooks on `Page` or fields
on `Site`. See [docs/design.md](docs/design.md) for the architecture and extension points, and
[docs/adr/](docs/adr/) for the decisions behind it.

## Development

```bash
python3 -m compileall -q sitekit
python3 -m unittest discover -s tests -v
```

To test a behaviour change end to end, vendor it into a site repository on a branch and run that site's build
and checks; a refactor must leave the site's `public/` byte-identical.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Releases are prepared by
[release-please](https://github.com/googleapis/release-please) from Conventional Commits.

## License

[MIT](LICENSE), copyright (c) 2026 ydongy.
