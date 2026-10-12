# Changelog

Format based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/). Entries say what changes for a
consuming site.

## [Unreleased]

### Added
- Shared page structure, checks, preview server and `vendor.sh`.
- One legal page layout: numbered sections, last-updated line, optional translation note and lead, contact line.
- Deterministic order of browser-language matches in `lang.js`.
- A release entry may omit its title; a legal page may omit its last-updated line.
- The preview server answers HEAD requests like GET.
- A release may keep its changes in `groups` (added, changed, fixed, removed), shown under headings from `changelog.groups.<kind>` of the copy. Releases with a flat `items` list render as before, byte for byte.
