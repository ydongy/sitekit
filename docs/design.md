<!-- template: library/design.md v1 -->
# sitekit design

## Architecture

`Site` holds the per-product settings (root directory, URL, name, contact, theme colours, optional share
image, page table). `Page` renders one language's pages from `i18n/<code>.json`; shared pieces are methods
(`head`, `header`, `footer`, `faq`, `legal`, `changelog`, `article`). `build(site, PageClass)` loads the
languages that have a copy file, renders every page, and writes the language-independent files.

## Extension points

A site subclasses `Page` and implements `home()`. Hooks it may override: `lang_summary`, `tagline`,
`contact_link`, `og_image_tags`. Anything else that differs is a new hook or a `Site` field, added here.

## Changelog entries

`changelog.json` is a list of releases, newest first: `version`, `date`, optional `title` and `summary`, and the
changes. A release keeps the Keep a Changelog subsections as `groups`, in order: each has a `kind` (`added`,
`changed`, `fixed`, `removed`) and `items` per language. The page shows a heading per group from the copy's
`changelog.groups.<kind>`, which every language must have for each kind it shows. A release with a flat `items`
list instead is one list without headings. A language without its own items shows the English ones, marked
`lang="en"`.

## Compatibility

A site records the sitekit commit it vendored (`scripts/sitekit/VERSION`). A change that alters generated
output is listed in `CHANGELOG.md`; consumers re-vendor and rebuild in their own pull request.
