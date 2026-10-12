<!-- template: adr.md v1 -->
# 0001 Consumers vendor a copy instead of fetching at build time

- Status: accepted
- Date: 2026-10-03
- Related: None

## Context

Sites are built on a developer's Mac and in CI, and their generated `public/` is committed. A build that
needs the network or a package registry is slower, can break for reasons unrelated to the site, and cannot be
reproduced years later.

## Decision

`vendor.sh` copies `sitekit/` into the site as `scripts/sitekit/` and records the sitekit commit in `VERSION`.
The site builds from its own copy.

## Cost

A fix reaches a site only when someone re-vendors it. Re-vendoring is a normal pull request whose diff shows
exactly what changed.

## Revisit triggers

More than a handful of sites, or a change that must reach all of them at once.
