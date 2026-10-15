# Contributing to sitekit

Issues and pull requests may be written in English or Simplified Chinese. Open an issue before starting a large
change. Small fixes can go straight to a pull request.

## Setup

Python 3.10 or newer and bash. No dependencies to install.

```bash
git clone https://github.com/ydongy/sitekit.git
cd sitekit
python3 -m compileall -q sitekit
python3 -m unittest discover -s tests -v
```

Rules for the code: standard library only, no network access at build time, and no product name in code
(use hooks on `Page` or fields on `Site`). A change that alters generated output for existing sites must say so
in the pull request. Record notable design decisions in `docs/adr/`.

## Commits and pull requests

- Commit messages and pull request titles follow [Conventional Commits](https://www.conventionalcommits.org/):
  `feat|fix|docs|refactor|perf|test|build|ci|chore|revert(scope)!: subject`.
- Branch names: `<type>/<issue>-<slug>`, for example `fix/12-sitemap-order`.
- A maintainer squash-merges, so the pull request title becomes the commit message. release-please builds the
  changelog and version from it.
- No sign-off (DCO) is required.
