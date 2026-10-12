# 0002 Per-product differences are hooks, not forks

- Status: accepted
- Date: 2026-10-03
- Related: [0001](0001-vendored-copy.md)

## Context

Two sites started as copies of one generator and drifted: different checks, different head tags, different
legal layouts, each fix made in one place only.

## Decision

Shared structure lives in `Page`. What differs per product is expressed as a `Site` field or an overridable
hook (`lang_summary`, `tagline`, `contact_link`, `og_image_tags`) or lives in the product's own `home()`.
A product that needs something no hook offers adds the hook here.

## Cost

The base class grows a hook for each real difference, and changing a hook's behaviour needs every site
rebuilt and compared.

## Revisit triggers

A hook that only one site uses and that makes `core.py` harder to read.
