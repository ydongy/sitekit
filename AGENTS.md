# AGENTS.md

## What it is

The shared website generator and checks. Sites vendor a copy of `sitekit/` into `scripts/sitekit/` with
`vendor.sh`; nothing here runs from the network. Python standard library only.

## Layout

```
sitekit/    the code that is vendored: core.py, check_i18n.py, check_site.py, preview.py
tests/      unittest smoke tests
vendor.sh   copies sitekit/ into a site repository and records the sitekit commit in VERSION
docs/       design.md (architecture, extension points), adr/ (decisions)
```

Nothing here may name a specific product: examples use `<Name>` and `<domain>`.

## Commands

```bash
python3 -m compileall -q sitekit
python3 -m unittest discover -s tests -v
```

To test a behaviour change, vendor it into a site repository on a branch and run that site's build and checks;
a refactor must leave the site's `public/` byte-identical.

## Conventions

- Python standard library only; no network access at build time.
- Behaviour that differs per product is a hook on `Page` or a field on `Site`, never a product name in code.
- A change that alters generated output for existing sites says so in the pull request.
- `vendor.sh` writes a commit hash to `VERSION`; that is the vendored copy's provenance, not the release version.
- Releases are automated by release-please from Conventional Commits. Do not edit `CHANGELOG.md` entries for
  released versions or bump versions by hand.
- Commit messages and PR titles: `feat|fix|docs|refactor|perf|test|build|ci|chore|revert(scope)!: subject`.
  Branches: `<type>/<issue>-<slug>`.

## Red lines

No credentials or secrets in the repository.
