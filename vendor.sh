#!/bin/bash
# Copy sitekit into a site repository as scripts/sitekit/ and record the sitekit commit.
#
#   vendor.sh <site-repo>
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
site="${1:?usage: vendor.sh <site-repo>}"
[[ -d "$site/scripts" ]] || { echo "error: $site/scripts not found" >&2; exit 1; }
dest="$site/scripts/sitekit"
rm -rf "$dest"
mkdir -p "$dest"
cp "$here"/sitekit/*.py "$dest"/
commit="$(git -C "$here" rev-parse HEAD 2> /dev/null || echo unknown)"
dirty=""
[[ -z "$(git -C "$here" status --porcelain 2> /dev/null)" ]] || dirty=" (uncommitted changes)"
printf '%s%s\n' "$commit" "$dirty" > "$dest/VERSION"
echo "vendored sitekit ${commit:0:7}$dirty into $dest"
