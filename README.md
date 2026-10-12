<div align="center">

# sitekit

Shared generator and checks for static, multilingual product websites.

[![CI](https://github.com/ydongy/sitekit/actions/workflows/ci.yml/badge.svg)](https://github.com/ydongy/sitekit/actions/workflows/ci.yml)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Release](https://img.shields.io/github/v/release/ydongy/sitekit)](https://github.com/ydongy/sitekit/releases)

**English** · [简体中文](README.zh-CN.md)

</div>

Python standard library only; the output is plain HTML committed to each site repository.

## Features

- `sitekit/core.py`: `Site` settings, the `Page` base class (head with canonical, hreflang and Open Graph; header; footer; FAQ; legal pages; changelog) and `build()`, which writes every page, `404.html`, `lang.js`, `sitemap.xml` and `robots.txt`.
- `sitekit/check_i18n.py`: checks every language against English (structure, HTML tags, links, placeholders, no dashes); optional `i18n/check-config.json`.
- `sitekit/check_site.py`: every language has every page, links and anchors resolve, nothing violates the Content-Security-Policy.
- `sitekit/preview.py`: local server that behaves like Cloudflare static assets.
- `vendor.sh`: copies `sitekit/` into a site repository as `scripts/sitekit/`.

## Requirements

Python 3.10 or newer (CI runs 3.12) and bash. Nothing to install: sitekit is not published to a package index.
Consumers vendor a copy of it.

## Quick start

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

Preview a built site locally (serves `public/` of the site repository, default port 8765):

```bash
python3 scripts/sitekit/preview.py [port]
```

## Development

```bash
python3 -m compileall -q sitekit
python3 -m unittest discover -s tests -v
```

To test a behaviour change end to end, vendor it into a site repository on a branch and run that site's build
and checks; a refactor must leave the site's `public/` byte-identical.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Commit messages and pull request titles follow
[Conventional Commits](https://www.conventionalcommits.org/); releases are prepared by
[release-please](https://github.com/googleapis/release-please) from them.

## Security

Report vulnerabilities privately via GitHub Security, "Report a vulnerability":
[open an advisory](https://github.com/ydongy/sitekit/security/advisories/new).

## License

[MIT](LICENSE), copyright (c) 2026 ydongy.
