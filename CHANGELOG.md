# Changelog

Format based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/). Entries say what changes for a
consuming site.

## [0.1.4](https://github.com/ydongy/sitekit/compare/v0.1.3...v0.1.4) (2026-10-15)


### Documentation

* align the repository with the account standard ([#16](https://github.com/ydongy/sitekit/issues/16)) ([17ab927](https://github.com/ydongy/sitekit/commit/17ab927d4b26efb9cebc704b4e55aabe6d5cd687))

## [0.1.3](https://github.com/ydongy/sitekit/compare/v0.1.2...v0.1.3) (2026-10-12)


### Fixed

* **preview:** use guards that code scanning recognizes ([#13](https://github.com/ydongy/sitekit/issues/13)) ([237ccf2](https://github.com/ydongy/sitekit/commit/237ccf25c297be6844e006f6b48e8ebb0bdb0bbd))

## [0.1.2](https://github.com/ydongy/sitekit/compare/v0.1.1...v0.1.2) (2026-10-12)


### Fixed

* **preview:** use the normalize-and-prefix check and encode the redirect ([#10](https://github.com/ydongy/sitekit/issues/10)) ([a981a25](https://github.com/ydongy/sitekit/commit/a981a25dcb1ed19c1a2fea046ebabfcb58261005))

## [0.1.1](https://github.com/ydongy/sitekit/compare/v0.1.0...v0.1.1) (2026-10-12)


### Fixed

* **preview:** keep request paths inside public/ and sanitize redirects ([#8](https://github.com/ydongy/sitekit/issues/8)) ([17124ca](https://github.com/ydongy/sitekit/commit/17124cab3ad401b710104070bf383fd4df53a473))

## [0.1.0](https://github.com/ydongy/sitekit/releases/tag/v0.1.0) (2026-10-12)

### Added
- Shared page structure, checks, preview server and `vendor.sh`.
- One legal page layout: numbered sections, last-updated line, optional translation note and lead, contact line.
- Deterministic order of browser-language matches in `lang.js`.
- A release entry may omit its title; a legal page may omit its last-updated line.
- The preview server answers HEAD requests like GET.
- A release may keep its changes in `groups` (added, changed, fixed, removed), shown under headings from `changelog.groups.<kind>` of the copy. Releases with a flat `items` list render as before, byte for byte.

### Documentation
- Bilingual README (English and Simplified Chinese) following the open-source layout.
