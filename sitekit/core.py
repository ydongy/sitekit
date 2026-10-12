"""Shared generator for ydongy's static product websites.

A site repository keeps its copy in i18n/*.json and changelog.json, subclasses `Page` for what is specific
to the product (the home page, and any layout it overrides), and calls `build(site, PageClass)`.
Pages, head tags, header, footer, FAQ, legal pages, changelog, 404, sitemap and lang.js live here.
"""
import html
import json
import re
from dataclasses import dataclass, field
from pathlib import Path

DEFAULT_PAGES = {
    "index": "/", "faq": "/faq", "privacy": "/privacy", "terms": "/terms", "refund": "/refund",
    "changelog": "/changelog",
}


@dataclass
class Site:
    root: Path  # repository root: contains i18n/, changelog.json, public/
    url: str  # https://example.com
    name: str  # product name, shown as the brand
    contact: str  # support address
    theme: tuple  # ((color, "light"), (color, "dark"))
    og_image: tuple | None = None  # (path, width, height) under public/, or None
    pages: dict = field(default_factory=lambda: dict(DEFAULT_PAGES))

    @property
    def public(self):
        return self.root / "public"

    def theme_meta(self):
        return "\n".join(
            f'<meta name="theme-color" content="{c}" media="(prefers-color-scheme: {m})">'
            for c, m in self.theme)


def attr(text):
    """Plain text (possibly already entity-encoded) as a safe attribute value."""
    return html.escape(html.unescape(text), quote=True)


def load(site):
    """Languages (those with an i18n/<code>.json) and their copy."""
    root = site.root
    langs = json.loads((root / "i18n/languages.json").read_text(encoding="utf-8"))
    langs = [l for l in langs if (root / f"i18n/{l['code']}.json").is_file()]
    copy = {
        l["code"]: json.loads((root / f"i18n/{l['code']}.json").read_text(encoding="utf-8"))
        for l in langs
    }
    return langs, copy


class Page:
    """One language's pages. Subclasses implement `home()` and may override the hooks below."""

    def __init__(self, site, lang, langs, copy):
        self.site, self.l, self.langs, self.all = site, lang, langs, copy
        self.t = copy[lang["code"]]
        self.p = lang["path"]

    # --- hooks ---------------------------------------------------------------------------------
    def lang_summary(self):
        """Content of the language menu button."""
        return self.t["name"]

    def tagline(self):
        """Text under the brand in the footer."""
        return self.t["home"]["h1"]

    def contact_link(self):
        return (f"mailto:{self.site.contact}", self.site.contact)

    def og_image_tags(self):
        if not self.site.og_image:
            return '<meta name="twitter:card" content="summary">'
        path, w, h = self.site.og_image
        return (f'<meta property="og:image" content="{self.site.url}{path}">\n'
                f'<meta property="og:image:width" content="{w}">\n'
                f'<meta property="og:image:height" content="{h}">\n'
                '<meta name="twitter:card" content="summary_large_image">')

    def home(self):
        raise NotImplementedError("the product page class implements home()")

    # --- shared pieces ---------------------------------------------------------------------------
    def root(self, s):
        return s.replace("{{root}}", self.p)

    def href(self, lang, page):
        return lang["path"] + self.site.pages[page] if page != "index" else (lang["path"] + "/")

    def head(self, page, title, desc, extra=""):
        alts = "\n".join(
            f'<link rel="alternate" hreflang="{l["html"]}" href="{self.site.url}{self.href(l, page)}">' for l in self.langs)
        alts += f'\n<link rel="alternate" hreflang="x-default" href="{self.site.url}{self.href(self.langs[0], page)}">'
        og = (f'<meta property="og:type" content="website">\n<meta property="og:site_name" content="{self.site.name}">\n'
              f'<meta property="og:title" content="{attr(title)}">\n<meta property="og:description" content="{attr(desc)}">\n'
              f'<meta property="og:url" content="{self.site.url}{self.href(self.l, page)}">\n{self.og_image_tags()}')
        return f'''<!doctype html>
<html lang="{self.l["html"]}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(html.unescape(title), quote=False)}</title>
<meta name="description" content="{attr(desc)}">
{alts}
<link rel="canonical" href="{self.site.url}{self.href(self.l, page)}">
{og}
{self.site.theme_meta()}
<link rel="icon" href="/icon.svg" type="image/svg+xml">
<link rel="stylesheet" href="/style.css">
<script src="/lang.js"></script>{extra}
</head>
<body>
<a class="skip" href="#main">{self.t["nav"]["skip"]}</a>
'''

    def lang_links(self, page):
        out = []
        for l in self.langs:
            cur = ' aria-current="true"' if l is self.l else ""
            out.append(f'<a href="{self.href(l, page)}" hreflang="{l["html"]}" lang="{l["html"]}" data-lang="{l["code"]}"{cur}>{self.all[l["code"]]["name"]}</a>')
        return out

    def header(self, page):
        n, p = self.t["nav"], self.p
        home = "" if page == "index" else f"{p}/"
        faq_cur = ' aria-current="page"' if page == "faq" else ""
        menu = "".join(f"<li>{a}</li>" for a in self.lang_links(page))
        return (f'<header class="site-header"><div class="wrap"><a class="brand" translate="no" href="{p}/"><img src="/icon.svg" alt="">{self.site.name}</a><nav>'
                f'<a href="{home}#download">{n["download"]}</a><a href="{home}#pricing">{n["pricing"]}</a><a href="{p}/faq"{faq_cur}>{n["faq"]}</a>'
                f'<details class="lang-menu"><summary aria-label="{attr(n["language"])}">{self.lang_summary()}</summary><ul>{menu}</ul></details>'
                f'</nav></div></header>')

    def footer(self, page):
        n, p = self.t["nav"], self.p
        home = "" if page == "index" else f"{p}/"
        cols = [
            (n["product"], [(f"{home}#download", n["download"]), (f"{home}#pricing", n["pricing"])]),
            (n["support"], [(f"{p}/faq", n["faq"]), (f"{p}/changelog", n["changelog"])]),
            (n["legal"], [(f"{p}/privacy", n["privacy"]), (f"{p}/terms", n["terms"]), (f"{p}/refund", n["refund"])]),
            (n["contact_h"], [self.contact_link()]),
        ]
        columns = "".join(
            f'<div><h2>{title}</h2>' + "".join(f'<a href="{href}">{label}</a>' for href, label in links) + "</div>"
            for title, links in cols)
        return (f'<footer class="site-footer"><div class="wrap">'
                f'<div class="foot-brand"><a class="brand" translate="no" href="{p}/"><img src="/icon.svg" alt="">{self.site.name}</a><p>{self.tagline()}</p></div>'
                f'<nav class="foot-cols" aria-label="{self.site.name}">{columns}</nav>'
                f'<div class="foot-bottom"><span>{n["copyright"]}</span><span>{n["official"]}</span></div>'
                f'<nav class="langs" aria-label="{attr(n["language"])}">{"".join(self.lang_links(page))}</nav></div></footer>\n</body>\n</html>\n')


    def article(self, page, inner):
        t = self.t
        main = f'''{self.header(page)}
<main id="main" class="wrap narrow page">
<article>
{inner}
</article>
</main>
'''
        return self.head(page, t["meta"][page + "_title"], t["meta"][page + "_desc"]) + main + self.footer(page)

    def faq(self):
        f = self.t["faq"]
        groups = []
        for g in f["groups"]:
            items = "\n".join(f'<details class="qa" id="{i["id"]}"><summary>{i["q"]}</summary><div>{self.root(i["a"])}</div></details>' for i in g["items"])
            groups.append(f'<h2 id="{g["id"]}">{g["h"]}</h2>\n{items}')
        return self.article("faq", f'<h1>{f["h1"]}</h1>\n<p class="lead">{f["lead"]}</p>\n\n' + "\n\n".join(groups))

    @staticmethod
    def note(v):
        """Translation notice under the title of a legal page (English is the reference)."""
        return f'<p class="note">{v["note"]}</p>\n' if v.get("note") else ""

    def changelog(self, releases):
        c, code = self.t["changelog"], self.l["code"]

        def pick(d):
            """The entry's text in this language, or English marked as such."""
            if code in d:
                return d[code], ""
            return d["en"], ' lang="en"'

        def inline(s):
            return re.sub(r"`([^`]+)`", r"<code>\1</code>", html.escape(s, quote=False))

        def heading(kind):
            """The heading of a group of changes in this language: `changelog.groups.<kind>` of the copy."""
            label = c.get("groups", {}).get(kind)
            if not label:
                raise SystemExit(f"i18n/{code}.json: changelog.groups.{kind} is missing")
            return label

        def groups(r):
            """(kind, items, lang attribute) per list of a release. Grouped releases keep the Keep a Changelog
            subsections in order (`groups`: kind plus items per language); a release with a flat `items` list is one
            list without a heading."""
            if r.get("groups"):
                return [(g["kind"], *pick(g["items"])) for g in r["groups"]]
            return [("", *pick(r["items"]))]

        parts = []
        for r in releases:
            title, tl = pick(r["title"]) if r.get("title") else ("", "")
            title_span = f"<span{tl}>{html.escape(title)}</span>" if title else ""
            block = [f'<div class="release" id="v{r["version"]}">',
                     f'<div class="release-head"><h2>{r["version"]}</h2>{title_span}<time datetime="{r["date"]}">{r["date"]}</time></div>']
            if r.get("summary"):
                summary, sl = pick(r["summary"])
                block.append(f"<p{sl}>{inline(summary)}</p>")
            for kind, items, il in groups(r):
                if kind:
                    block.append(f"<h3>{html.escape(heading(kind))}</h3>")
                block.append(f"<ul{il}>" + "".join(f"<li>{inline(i)}</li>" for i in items) + "</ul>")
            block.append("</div>")
            parts.append("\n".join(block))
        body = "\n".join(parts) or f'<p class="lead">{c["empty"]}</p>'
        return self.article("changelog", f'<h1>{c["h1"]}</h1>\n<!-- releases -->\n{body}\n<!-- /releases -->')

    def legal(self, page):
        """Terms, privacy and refund pages: title, last-updated line, optional translation note and lead,
        numbered sections, and the contact line."""
        t, v = self.t, self.t[page]
        lead = f'<p class="lead">{v["lead"]}</p>\n' if v.get("lead") else ""
        updated = f'<p class="lead">{v["updated"]}</p>\n' if v.get("updated") else ""
        secs = "\n\n".join(
            f'<h2>{i}. {s["h"]}</h2>\n{self.root(s["body"])}' for i, s in enumerate(v["sections"], 1))
        return self.article(
            page,
            f'<h1>{v["h1"]}</h1>\n{updated}{self.note(v)}{lead}\n{secs}\n'
            f'<p class="contact">{t["nav"]["contact"]}</p>')

    def privacy(self):
        return self.legal("privacy")

    def terms(self):
        return self.legal("terms")

    def refund(self):
        return self.legal("refund")



def not_found(site, langs, copy):
    links = "<span aria-hidden=\"true\"> / </span>".join(
        f'<a href="{l["path"]}/" lang="{l["html"]}">{copy[l["code"]]["name"]}</a>' for l in langs)
    en = copy[langs[0]["code"]]["nav"]
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Page not found · {site.name}</title>
<meta name="robots" content="noindex">
{site.theme_meta()}
<link rel="icon" href="/icon.svg" type="image/svg+xml">
<link rel="stylesheet" href="/style.css">
</head>
<body>
<a class="skip" href="#main">{en["skip"]}</a>
<header class="site-header"><div class="wrap"><a class="brand" translate="no" href="/"><img src="/icon.svg" alt="">{site.name}</a><nav><a href="/#download">{en["download"]}</a><a href="/#pricing">{en["pricing"]}</a><a href="/faq">{en["faq"]}</a></nav></div></header>
<main id="main" class="wrap narrow page">
<h1>Page not found</h1>
<p class="lead">This page doesn’t exist or has moved.</p>
<p class="lead">{links}</p>
</main>
</body>
</html>
'''



def sitemap(site, langs):
    """Every page in every language, each with its alternates."""
    urls = []
    for page in site.pages:
        for l in langs:
            alts = "".join(f'<xhtml:link rel="alternate" hreflang="{a["html"]}" href="{site.url}{href(site, a, page)}"/>' for a in langs)
            alts += f'<xhtml:link rel="alternate" hreflang="x-default" href="{site.url}{href(site, langs[0], page)}"/>'
            urls.append(f"<url><loc>{site.url}{href(site, l, page)}</loc>{alts}</url>")
    return ('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
            'xmlns:xhtml="http://www.w3.org/1999/xhtml">\n' + "\n".join(urls) + "\n</urlset>\n")


def href(site, lang, page):
    return lang["path"] + site.pages[page] if page != "index" else (lang["path"] + "/")


def lang_js(langs):
    """First visit to an English page from a browser that prefers another supported language goes there."""
    table = sorted(((m, l["path"]) for l in langs if l["path"] for m in l["match"]), key=lambda x: (-len(x[0]), x[0]))  # deterministic
    prefixes = sorted({l["path"] for l in langs if l["path"]}, key=lambda p: (-len(p), p))  # deterministic
    return f'''// Generated by scripts/build.py from i18n/languages.json. Do not edit by hand.
// First visit to an English page from a browser that prefers another supported language goes to that
// language. Choosing a language with the switcher is remembered and wins.
(function () {{
  var KEY = "lang";
  var MATCH = {json.dumps(table)};
  var PREFIXES = {json.dumps(prefixes)};
  var path = location.pathname;
  var current = PREFIXES.filter(function (p) {{ return path === p || path.indexOf(p + "/") === 0; }})[0];
  var saved = null;
  try {{ saved = localStorage.getItem(KEY); }} catch (e) {{}}
  if (!saved && !current) {{
    var first = ((navigator.languages && navigator.languages[0]) || navigator.language || "").toLowerCase();
    for (var i = 0; i < MATCH.length; i++) {{
      var m = MATCH[i][0];
      if (first === m || first.indexOf(m + "-") === 0) {{
        location.replace(MATCH[i][1] + path + location.search + location.hash);
        return;
      }}
    }}
  }}
  document.addEventListener("click", function (e) {{
    var a = e.target.closest && e.target.closest("a[data-lang]");
    if (a) try {{ localStorage.setItem(KEY, a.getAttribute("data-lang")); }} catch (e) {{}}
    var open = document.querySelector(".lang-menu[open]");
    if (open && !open.contains(e.target)) open.removeAttribute("open");
  }});
  document.addEventListener("keydown", function (e) {{
    var open = document.querySelector(".lang-menu[open]");
    if (e.key === "Escape" && open) {{ open.removeAttribute("open"); open.querySelector("summary").focus(); }}
  }});
}})();
'''


def build(site, page_class):
    """Write every language's pages, 404.html, lang.js, sitemap.xml and robots.txt into public/."""
    langs, copy = load(site)
    releases = json.loads((site.root / "changelog.json").read_text(encoding="utf-8"))
    releases.sort(key=lambda r: tuple(int(n) for n in r["version"].split(".")), reverse=True)
    for lang in langs:
        out = site.public / lang["path"].lstrip("/")
        out.mkdir(parents=True, exist_ok=True)
        page = page_class(site, lang, langs, copy)
        for name, text in (
            ("index", page.home()), ("faq", page.faq()), ("privacy", page.privacy()),
            ("terms", page.terms()), ("refund", page.refund()),
            ("changelog", page.changelog(releases)),
        ):
            (out / f"{name}.html").write_text(text, encoding="utf-8")
    (site.public / "404.html").write_text(not_found(site, langs, copy), encoding="utf-8")
    (site.public / "lang.js").write_text(lang_js(langs), encoding="utf-8")
    (site.public / "sitemap.xml").write_text(sitemap(site, langs), encoding="utf-8")
    (site.public / "robots.txt").write_text(
        f"User-agent: *\nAllow: /\nSitemap: {site.url}/sitemap.xml\n", encoding="utf-8")
    print("built:", ", ".join(l["code"] for l in langs))
