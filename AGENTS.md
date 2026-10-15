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

## Issues and pull requests

`gh issue create` and `gh pr create --body` skip the issue forms and the pull request template, so write their
structure yourself. Search open issues first; one issue is one problem.

- Issue title: one short sentence that says the problem or the outcome, in English or Simplified Chinese. No type
  prefix such as `[feat]`; the label carries the type.
- Bug, `--label bug`: `## What happened`, `## What you expected`, `## Steps to reproduce`,
  `## Version and environment`.
- Feature or improvement, `--label enhancement`: `## Problem`, `## Proposed solution`,
  `## Alternatives considered` (when there were any), `## Done when`.
- Documentation, `--label documentation`: `## Where`, `## What is missing, unclear or wrong`, `## Suggested change`.
- Labels: `accessibility` marks a barrier for people with disabilities in the generated pages, together with
  `enhancement` or `bug`. The `autorelease: pending` and `autorelease: tagged` labels belong to release-please;
  do not add or remove them.
- Pull request: the title is the Conventional Commits subject (it becomes the squash commit and the changelog
  entry). The body has `## Summary` (what changes and why), `## Related issue` (`Closes #<n>`), `## How tested`
  (the commands run and their results, and what was not run) and `## Checklist`:
  `- [ ] PR title follows Conventional Commits`, `- [ ] Tests pass`,
  `- [ ] Documentation updated where behavior changed`, ticked only when true.

## Red lines

- Credentials never go into code, pull requests, issues, logs or chat. No secrets in the repository.
- Releases, signing and anything sent to an external service need the maintainer's confirmation. Merging the
  release-please pull request publishes a release; do not merge it, create tags or edit the release-please
  manifest without that confirmation.
- No blind `git add -A` of unknown files: stage explicit paths and check the file list.
