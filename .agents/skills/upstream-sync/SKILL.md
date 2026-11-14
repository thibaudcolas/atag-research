---
name: upstream-sync
description: Refresh the local mirror of the upstream w3c-cg/atag repository, issues, pull requests, discussions, and wiki under local/upstream, then bring this workspace's docs and research notes up to date with what changed. Use when research depends on current upstream ATAG content, or before quoting minutes, spec text, or discussion outcomes.
license: MIT
metadata:
  version: "1.2.0"
---

# Upstream sync

The authoritative source for ATAG material is [w3c-cg/atag](https://github.com/w3c-cg/atag). This workspace mirrors it, read-only, under `local/upstream/`:

| Path                         | Contents                                                            | Refreshed by                     |
| ---------------------------- | ------------------------------------------------------------------- | -------------------------------- |
| `local/upstream/atag/`       | Upstream commit history and files, checked out on `main`            | `git fetch` + fast-forward merge |
| `local/upstream/gh-md/atag/` | Issues, pull requests, and discussions as Markdown with frontmatter | `gh md pull w3c-cg/atag`         |
| `local/upstream/atag-wiki/`  | Wiki pages                                                          | `git fetch` + fast-forward merge |

`local/` is git-ignored by this repository. Never commit it, and never edit or push the mirrors: they are read-only copies. Use `local/` files as sources for research notes in `docs/` rather than copying upstream text into the site.

## Refresh

Run from the workspace root:

```sh
just sync-upstream                 # fetch and update all three mirrors
just sync-upstream --reclone       # replace the code checkout if its origin was changed
```

Requires `git`, the [GitHub CLI](https://cli.github.com) (`gh auth login`), and the [gh-md extension](https://github.com/jackchuka/gh-md) (`gh extension install jackchuka/gh-md`). Each source whose tooling or upstream feature is unavailable is skipped with a message; the rest still sync. Sync is incremental and safe to re-run: it never discards local edits in the code checkout, and it exits non-zero rather than merging divergent history. The [gh-md reference](references/gh-md.md) covers its commands, filters, and file format.

To refresh a single item with extra history, pull it directly:

```sh
GH_MD_ROOT="$PWD/local/upstream/gh-md" gh md pull https://github.com/w3c-cg/atag/issues/123
GH_MD_ROOT="$PWD/local/upstream/gh-md" gh md pull w3c-cg/atag --full --prs
```

## Determine what changed

Compare against the previous state rather than re-reading everything:

```sh
# New wiki commits; empty when the wiki did not change.
git -C local/upstream/atag-wiki log --oneline 'origin/master@{1}..origin/master'

# Item states and file paths, and items updated in the last two days.
GH_MD_ROOT="$PWD/local/upstream/gh-md" gh md --list --format=json
GH_MD_ROOT="$PWD/local/upstream/gh-md" gh md --list '--filter=updated > now - duration("48h")'
```

The code checkout has no reflog, so capture the commit before syncing and diff afterwards:

```sh
git -C local/upstream/atag rev-parse origin/main   # run before `just sync-upstream`
just sync-upstream
git -C local/upstream/atag log --oneline <previous-commit>..origin/main
```

Then check the upstream `minutes/` and `index.html` files against the pages that cite them. Wiki paths are `.md` files at the wiki checkout root.

## Update this workspace

Only touch pages affected by the change. Follow `docs/contributing/README.md` and `docs/contributing/style-guide.md`.

- **Upstream references** in `docs/knowledge-base/atag/`, `docs/knowledge-base/atag-cg/`, and `docs/knowledge-base/atag-wg/`: update facts, links, and summaries that the new upstream content contradicts or supersedes.
- **Workspace research** in `docs/cg-contributions/`: revise notes and recommendations whose evidence moved, especially when a discussion reached a resolution or a new draft branch appears.
- **Citations**: link to the live GitHub or W3C URL, not to `local/upstream/`; the mirror is a local aid.
- **Meeting minutes**: append new items rather than rewriting history, and cite the minute's URL.

Do not invent upstream positions: if a discussion is unresolved, say so. Never rewrite pages wholesale: re-reading every page is not a sync.

## Maintain the global reference list

`docs/contributing/abbreviations.md` is appended to every page by `pymdownx.snippets` (`auto_append` in `mkdocs.yml`), so a reference definition there resolves on any page, and the title in the definition becomes the link tooltip:

```text
[#12]: https://github.com/w3c-cg/atag/discussions/12 "Types of Authoring Tools"
```

Pages cite the item as `[#12]`. Numbers are unique across issues, pull requests, and discussions in a repository, so one label per number covers all three types; the mirror's frontmatter tells you which type an item is.

The list covers every mirrored item, not just the ones pages currently cite, so a new citation rarely needs a manual edit. Regenerate it after each sync:

```sh
uv run python scripts/update_upstream_references.py
```

The script reads the frontmatter of `local/upstream/gh-md/w3c-cg/atag/{issues,pulls,discussions}/*.md`, sorts by number, and rewrites only the block between `<!-- BEGIN upstream references -->` and `<!-- END upstream references -->`. It quotes each title for the tooltip, switching to single quotes when a title contains double quotes, and stops with an error when a title contains both quote characters (add that entry by hand), when two items share a number, or when the mirror is empty.

- Do not reorder or hand-edit the generated block: change the upstream item, sync, then re-run the script.
- References that are not GitHub items, such as `[UCR]: https://w3c-cg.github.io/atag/docs/ucr/ 'Use Cases and Requirements draft'`, live outside the markers and stay hand-maintained.
- A missing definition does not fail the build: the shorthand renders as literal text. Grep the built page for the label to confirm it resolved.

## Verify

```sh
just lint-prose
just build-docs
```

Unresolved `[#N]` shorthand renders as literal text rather than failing the build, so grep the page you touched for the label (`grep -o '\[#[0-9]\+]' site/<page>/index.html`); inline code examples of the syntax match too.

Report the upstream commit, wiki commit, and item counts you synced, and list the workspace pages you changed.
