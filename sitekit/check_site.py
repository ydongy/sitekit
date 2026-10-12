#!/usr/bin/env python3
"""Sanity checks for public/: every language has every page, internal links and
anchors resolve, and nothing violates the Content-Security-Policy in public/_headers
(no inline style attributes or <style> blocks, no external resources).

Run from the repo root: python3 scripts/sitekit/check_site.py
"""
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent  # scripts/sitekit/ -> repository root
PUB = ROOT / "public"
errors = []


def url_to_file(url):
    path = url.split("#")[0].split("?")[0]
    if path.endswith("/"):
        path += "index"
    for cand in (PUB / path.lstrip("/"), PUB / (path.lstrip("/") + ".html")):
        if cand.is_file():
            return cand
    return None


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids, self.links, self.bad = set(), [], []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if "id" in a:
            self.ids.add(a["id"])
        if "style" in a or tag == "style":
            self.bad.append("inline style")
        if tag == "a" and a.get("href"):
            self.links.append(a["href"])
        for k in ("src", "href"):
            if tag in ("script", "img", "link") and a.get(k, "").startswith(("http://", "https://")) and a.get("rel") != "alternate":
                if not (tag == "link" and a.get("rel") in ("alternate", "canonical")):
                    self.bad.append(f"external {tag} {a[k]}")


pages = {}
for f in sorted(PUB.rglob("*.html")):
    p = Page()
    p.feed(f.read_text(encoding="utf-8"))
    pages[f] = p
    for b in p.bad:
        errors.append(f"{f.relative_to(PUB)}: {b}")

import json
LANG_PATHS = [l["path"].lstrip("/") for l in json.loads((ROOT / "i18n/languages.json").read_text()) if (ROOT / f"i18n/{l['code']}.json").is_file()]
PAGE_NAMES = [name + ".html" for name in ("index", "faq", "privacy", "terms", "refund", "changelog")]
for lang in LANG_PATHS:
    for name in PAGE_NAMES:
        if not (PUB / lang / name).is_file():
            errors.append(f"missing page {lang or '.'}/{name}: run python3 scripts/build.py")

for f, p in pages.items():
    for href in p.links:
        if href.startswith(("http://", "https://", "mailto:")):
            continue
        base = href.split("#")[0]
        frag = href.split("#")[1] if "#" in href else ""
        target = f if base == "" else url_to_file(base)
        if target is None:
            errors.append(f"{f.relative_to(PUB)}: broken link {href}")
        elif target is not None and frag and frag not in pages.get(target, p).ids:
            errors.append(f"{f.relative_to(PUB)}: missing anchor {href}")

if errors:
    print("\n".join(errors))
    sys.exit(1)
print(f"ok: {len(pages)} pages")
