<!-- template: library/README.md v1 -->
# sitekit

Shared generator and checks for ydongy's static product websites. Python standard library only;
the output is plain HTML committed to each site repository.

## What is here

| Path | Purpose |
|---|---|
| `sitekit/core.py` | `Site` settings, the `Page` base class (head with canonical, hreflang and Open Graph; header; footer; FAQ; legal pages; changelog), and `build()` which writes every page, `404.html`, `lang.js`, `sitemap.xml` and `robots.txt` |
| `sitekit/check_i18n.py` | Every language against English: structure, HTML tags, links, placeholders, no dashes; optional `i18n/check-config.json` |
| `sitekit/check_site.py` | Every language has every page, links and anchors resolve, nothing violates the Content-Security-Policy |
| `sitekit/preview.py` | Local server that behaves like Cloudflare static assets |
| `vendor.sh` | Copies `sitekit/` into a site repository as `scripts/sitekit/` and records the commit in `VERSION` |

## Using it

```bash
# in the site repository
<path to sitekit>/vendor.sh .
python3 scripts/sitekit/check_i18n.py
python3 scripts/build.py
python3 scripts/sitekit/check_site.py
python3 scripts/check_facts.py
```

A site owns its copy (`i18n/`, `changelog.json`), its styles and assets, and `scripts/build.py`: a `Site(...)`
and a `Page` subclass implementing `home()`. Facts checks stay in the site as `scripts/check_facts.py`.

## Changing it

Change shared behaviour here, record why in `docs/adr/`, add a line to `CHANGELOG.md`, then run `vendor.sh` in
each site in its own pull request. Every site's `public/` must stay reproducible: its CI rebuilds and
requires no diff.

## License

[MIT](LICENSE), copyright (c) 2026 ydongy.
