<!-- template: AGENTS.md v1 -->
# AGENTS.md

## What it is

The shared website generator and checks. Sites vendor a copy of `sitekit/` into `scripts/sitekit/`; nothing
here runs from the network.

## Sources of truth

Read `handbook/core/` first, then only the guides, stacks and type preset that apply to this project.
Its documented platforms, languages, architecture and distribution remain project decisions.
The handbook link and docs workflow pin one revision; upgrade them together in a migration PR.

`docs/design.md` describes the architecture and the extension points; `docs/adr/` holds the decisions.
`CHANGELOG.md` says what changed for consumers. How we work: the ydongy handbook
(`https://github.com/ydongy/.github/tree/6b48552c969c28a954498123bb502a556f8eed79/handbook`), and `handbook/core/agents.md` for AI collaborators.

## Directory boundaries

```
sitekit/    the code that is vendored: core.py, check_i18n.py, check_site.py, preview.py
vendor.sh   copies sitekit/ into a site repository
docs/       design.md, adr/
```

Nothing here may name a specific product: examples use `<Name>` and `<domain>`.

## Commands

```bash
python3 -c "import ast,sys; [ast.parse(open(f).read()) for f in sys.argv[1:]]" sitekit/*.py
python3 <path to the ydongy/.github repository>/scripts/check-docs.py .
```

To test a change, vendor it into a site repository on a branch and run that site's five commands; a refactor
must leave the site's `public/` byte-identical.

## Project rules

- Python standard library only; no network access at build time.
- Behaviour that differs per product is a hook on `Page` or a field on `Site`, never a product name in code.
- A change that alters generated output for existing sites says so in `CHANGELOG.md`.

## Red lines

No credentials. See `handbook/core/agents.md`.
