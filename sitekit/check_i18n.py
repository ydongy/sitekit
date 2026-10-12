#!/usr/bin/env python3
"""Check every i18n/<code>.json against i18n/en.json before building.

    python3 scripts/check_i18n.py [code ...]

Optional i18n/check-config.json: {"join_lists": ["home.h1", ...]} compares those lists of strings after
joining their parts, for copy that may split a headline differently per language (Chinese).

For each string: same JSON structure, the same HTML tags in the same order, the same link
targets and ids, the same {{root}}, {v} and {os} placeholders, and no em or en dashes.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent  # scripts/sitekit/ -> repository root
TAG = re.compile(r"<(/?)([a-zA-Z][a-zA-Z0-9]*)\b([^>]*)>")
KEEP_ATTRS = re.compile(r'\b(href|id|class|scope)="([^"]*)"')


def shape(s):
    tags = [(c, n.lower(), tuple(KEEP_ATTRS.findall(a))) for c, n, a in TAG.findall(s)]
    marks = sorted(re.findall(r"\{\{root\}\}|\{v\}|\{os\}", s))
    return tags, marks


def walk(en, other, path, errors):
    if isinstance(en, dict):
        if not isinstance(other, dict) or set(en) != set(other):
            errors.append(f"{path}: keys differ: missing {sorted(set(en) - set(other or {}))}, extra {sorted(set(other or {}) - set(en))}")
            return
        for k in en:
            walk(en[k], other[k], f"{path}.{k}", errors)
    elif isinstance(en, list):
        if not isinstance(other, list) or len(en) != len(other):
            errors.append(f"{path}: list length differs ({len(en)} vs {len(other) if isinstance(other, list) else type(other).__name__})")
            return
        for i, (a, b) in enumerate(zip(en, other)):
            walk(a, b, f"{path}[{i}]", errors)
    elif isinstance(en, str):
        if not isinstance(other, str):
            errors.append(f"{path}: not a string")
            return
        if en and not other.strip():
            errors.append(f"{path}: empty")
        if shape(en) != shape(other):
            errors.append(f"{path}: HTML tags, links or placeholders differ from English:\n    en: {en[:160]}\n    xx: {other[:160]}")
        if re.search("[–—]", other):
            errors.append(f"{path}: contains an em or en dash")


def joined(data, dotted_paths):
    """A copy of `data` where each listed list of strings is replaced by one joined string."""
    data = json.loads(json.dumps(data))
    for dotted in dotted_paths:
        *parents, last = dotted.split(".")
        node = data
        for key in parents:
            node = node[key]
        if isinstance(node.get(last), list):
            node[last] = [" ".join(node[last])]
    return data


def main(codes):
    config_file = ROOT / "i18n/check-config.json"
    join = json.loads(config_file.read_text(encoding="utf-8")).get("join_lists", []) if config_file.is_file() else []
    en = json.loads((ROOT / "i18n/en.json").read_text(encoding="utf-8"))
    langs = [l["code"] for l in json.loads((ROOT / "i18n/languages.json").read_text(encoding="utf-8"))]
    codes = codes or [c for c in langs if c != "en" and (ROOT / f"i18n/{c}.json").is_file()]
    failed = False
    for code in codes:
        other = json.loads((ROOT / f"i18n/{code}.json").read_text(encoding="utf-8"))
        errors = []
        walk(joined(en, join), joined(other, join), code, errors)
        print(f"{code}: {'ok' if not errors else str(len(errors)) + ' problem(s)'}")
        for e in errors:
            print("  - " + e)
        failed |= bool(errors)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
