#!/bin/sh
# Mirror the upstream w3c-cg/atag repository into local/upstream/.
#
# Three sources, each skipped when it does not apply to the upstream repository:
# - local/upstream/atag: git checkout, with a read-only "origin" remote pointing at w3c-cg/atag.
# - local/upstream/gh-md/atag: issues, pull requests, and discussions, via the gh-md extension.
# - local/upstream/atag-wiki: wiki pages, from the repository's separate wiki git repository.
#
# Safe to re-run: every step updates an existing mirror in place. Local edits in the code
# checkout are kept, and the script reports them rather than discarding them.
#
# Usage: scripts/sync_upstream.sh [--reclone]
#   --reclone  Replace the code checkout when its origin does not point at w3c-cg/atag.
set -eu

UPSTREAM="w3c-cg/atag"
ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
MIRROR="$ROOT/local/upstream"
REPO="$MIRROR/atag"
GH_MD="$MIRROR/gh-md"
WIKI="$MIRROR/atag-wiki"
MIRROR_URL="https://github.com/$UPSTREAM.git"
WIKI_URL="https://github.com/$UPSTREAM.wiki.git"
RECLONE=false

for argument in "$@"; do
    case $argument in
        --reclone) RECLONE=true ;;
        *)
            echo "Unknown option: $argument. Use --reclone to replace the code checkout." >&2
            exit 2
            ;;
    esac
done

if ! command -v git >/dev/null 2>&1; then
    echo "git is required: https://git-scm.com/downloads" >&2
    exit 1
fi

# Use the git directory directly so nested checkouts never resolve the outer repository.
git_at() {
    git -C "$REPO" --git-dir=.git "$@"
}

# Keep gh-md files out of the outer repository's git status.
add_exclude() {
    exclude=$REPO/.git/info/exclude
    grep -qxF '/gh-md/' "$exclude" && return 0
    printf '\n# Written by `just sync-upstream`.\n/gh-md/\n' >>"$exclude"
}

# Repository capabilities; an unreachable API falls back to syncing every source type.
capability() {
    gh api "repos/$UPSTREAM" --jq ".$1" 2>/dev/null || true
}

has_wiki=$(capability has_wiki)
has_issues=$(capability has_issues)
has_discussions=$(capability has_discussions)

mkdir -p "$MIRROR"
echo "Syncing $UPSTREAM into local/upstream/"

# ---- Repository checkout --------------------------------------------------------------
if [ -d "$REPO/.git" ]; then
    current=$(git_at remote get-url origin)
    if [ "$current" != "$MIRROR_URL" ]; then
        if [ "$RECLONE" = false ]; then
            echo "error: local/upstream/atag has origin $current, expected $MIRROR_URL." >&2
            echo "Run: just sync-upstream --reclone  (replaces it with a clean checkout)" >&2
            exit 1
        fi
        rm -rf "$REPO"
    fi
fi

if [ -d "$REPO/.git" ]; then
    git_at fetch --prune --quiet origin
else
    git clone --quiet "$MIRROR_URL" "$REPO"
fi

# Fast-forward only: never merge, rebase, or check out over uncommitted work.
git_at merge --ff-only --quiet origin/main
add_exclude

if [ -n "$(git_at status --porcelain)" ]; then
    echo "Kept local changes in local/upstream/atag:"
    git -c status.branch=false -C "$REPO" status --short
else
    echo "Repository: main at $(git_at rev-parse --short origin/main)"
fi

# ---- Issues, pull requests, discussions -----------------------------------------------
if ! command -v gh >/dev/null 2>&1; then
    echo "Skipped issues, pull requests, and discussions: install the GitHub CLI (https://cli.github.com), then run: gh auth login"
elif ! gh auth status >/dev/null 2>&1; then
    echo "Skipped issues, pull requests, and discussions: run: gh auth login"
elif ! gh extension list | grep -q '^gh md	'; then
    echo "Skipped issues, pull requests, and discussions: run: gh extension install jackchuka/gh-md"
elif [ "$has_issues" != true ]; then
    echo "Skipped issues and pull requests: $UPSTREAM has issues disabled."
elif [ "$has_discussions" = true ]; then
    GH_MD_ROOT="$GH_MD" gh md pull "$UPSTREAM" --issues --prs --discussions
else
    GH_MD_ROOT="$GH_MD" gh md pull "$UPSTREAM" --issues --prs
fi

# ---- Wiki ----------------------------------------------------------------------------
if [ "$has_wiki" = "false" ]; then
    echo "Skipped the wiki: $UPSTREAM has no wiki enabled."
elif [ -d "$WIKI/.git" ]; then
    branch=$(git -C "$WIKI" rev-parse --abbrev-ref HEAD)
    git -C "$WIKI" fetch --prune --quiet origin
    git -C "$WIKI" merge --ff-only --quiet "origin/$branch"
    echo "Wiki: $branch at $(git -C "$WIKI" rev-parse --short "origin/$branch")"
else
    git clone --quiet "$WIKI_URL" "$WIKI"
    branch=$(git -C "$WIKI" rev-parse --abbrev-ref HEAD)
    echo "Wiki: $branch at $(git -C "$WIKI" rev-parse --short HEAD)"
fi
