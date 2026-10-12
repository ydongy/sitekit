# Changelog

Format based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/). Entries say what changes for a
consuming site.

## [0.1.1](https://github.com/ydongy/sitekit/compare/sitekit-v0.1.0...sitekit-v0.1.1) (2026-10-12)


### Documentation

* bilingual README following the open-source layout ([#1](https://github.com/ydongy/sitekit/issues/1)) ([90d533b](https://github.com/ydongy/sitekit/commit/90d533bb29a86d603a0ca0279f9e36547cbb0ca2))

## [Unreleased]

### Added
- Shared page structure, checks, preview server and `vendor.sh`.
- One legal page layout: numbered sections, last-updated line, optional translation note and lead, contact line.
- Deterministic order of browser-language matches in `lang.js`.
- A release entry may omit its title; a legal page may omit its last-updated line.
- The preview server answers HEAD requests like GET.
- A release may keep its changes in `groups` (added, changed, fixed, removed), shown under headings from `changelog.groups.<kind>` of the copy. Releases with a flat `items` list render as before, byte for byte.
