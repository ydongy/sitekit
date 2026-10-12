<!-- template: adr-index.md v2 -->
# Architecture Decision Records

Each record covers one decision: context, decision, cost. A reversed decision keeps its file: write a new
record and mark the old one "superseded by NNNN".

## Index

| No. | Decision | Status |
|---|---|---|
| [0001](0001-vendored-copy.md) | Consumers vendor a copy instead of fetching at build time | accepted |
| [0002](0002-hooks-not-forks.md) | Per-product differences are hooks, not forks | accepted |

## Record template

See `handbook/templates/common/adr.md` in the ydongy handbook.
