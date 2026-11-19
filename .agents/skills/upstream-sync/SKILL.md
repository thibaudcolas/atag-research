---
name: upstream-sync
description: Refresh the local mirrors of the upstream w3c-cg/atag, w3c/wcag3, and mgifford/We4Authors repositories, issues, pull requests, discussions, and wikis under local/upstream, then bring this workspace's docs and research notes up to date with what changed. Use when research depends on current upstream ATAG, WCAG 3, or We4Authors content, or before quoting minutes, spec text, or discussion outcomes.
license: MIT
metadata:
  version: "1.4.0"
---

# Upstream sync

The authoritative sources are [w3c-cg/atag](https://github.com/w3c-cg/atag) for ATAG, [w3c/wcag3](https://github.com/w3c/wcag3) for WCAG 3, and [mgifford/We4Authors](https://github.com/mgifford/We4Authors) for the We4Authors cluster. This workspace mirrors all three, read-only, under `local/upstream/`:

| Path                                        | Contents                                                                   | Refreshed by                     |
| ------------------------------------------- | -------------------------------------------------------------------------- | -------------------------------- |
| `local/upstream/atag/`                      | ATAG commit history and files, checked out on `main`                       | `git fetch` + fast-forward merge |
| `local/upstream/gh-md/w3c-cg/atag/`         | ATAG issues, pull requests, and discussions as Markdown with frontmatter   | `gh md pull w3c-cg/atag`         |
| `local/upstream/atag-wiki/`                 | ATAG wiki pages                                                            | `git fetch` + fast-forward merge |
| `local/upstream/wcag3/`                     | WCAG 3 commit history and files, checked out on `main`                     | `git fetch` + fast-forward merge |
| `local/upstream/gh-md/w3c/wcag3/`           | WCAG 3 issues, pull requests, and discussions as Markdown with frontmatter | `gh md pull w3c/wcag3`           |
| `local/upstream/wcag3-wiki/`                | WCAG 3 wiki pages                                                          | `git fetch` + fast-forward merge |
| `local/upstream/we4authors/`                | We4Authors Jekyll site source, checked out on `main`                       | `git fetch` + fast-forward merge |
| `local/upstream/gh-md/mgifford/We4Authors/` | We4Authors issues and pull requests, as Markdown with frontmatter          | `gh md pull mgifford/We4Authors` |

The ATAG site is built from `local/upstream/atag/` and the We4Authors site from `local/upstream/we4authors/`, so read the source pages in those checkouts rather than the rendered sites.

`local/` is git-ignored by this repository. Never commit it, and never edit or push the mirrors: they are read-only copies. Use `local/` files as sources for research notes in `docs/` rather than copying upstream text into the site.

`scripts/sync_upstream.py` lists the mirrored repositories in `SOURCES`: add a source there to mirror another repository the same ways. A source whose repository has no wiki, or an enabled wiki with no pages yet, skips that step; We4Authors has neither a wiki with pages nor discussions.

## Refresh

Run from the workspace root:

```sh
just sync-upstream                 # fetch and update every mirror
just sync-upstream --only mgifford/We4Authors  # sync a single source
just sync-upstream --reclone       # replace a code checkout whose origin was changed
```

Requires `git`, the [GitHub CLI](https://cli.github.com) (`gh auth login`), and the [gh-md extension](https://github.com/jackchuka/gh-md) (`gh extension install jackchuka/gh-md`). Each source whose tooling or upstream feature is unavailable is skipped with a message; the rest still sync. Sync is incremental and safe to re-run: it never discards local edits in the code checkout, and it exits non-zero rather than merging divergent history. The [gh-md reference](references/gh-md.md) covers its commands, filters, and file format.

To refresh a single item with extra history, pull it directly:

```sh
GH_MD_ROOT="$PWD/local/upstream/gh-md" gh md pull https://github.com/w3c-cg/atag/issues/123
GH_MD_ROOT="$PWD/local/upstream/gh-md" gh md pull w3c-cg/atag --full --prs
GH_MD_ROOT="$PWD/local/upstream/gh-md" gh md pull w3c/wcag3 --full --prs
```

## Determine what changed

Compare against the previous state rather than re-reading everything:

```sh
# New wiki commits; empty when the wiki did not change.
git -C local/upstream/atag-wiki log --oneline 'origin/master@{1}..origin/master'
git -C local/upstream/wcag3-wiki log --oneline 'origin/master@{1}..origin/master'

# Item states and file paths, and items updated in the last two days.
GH_MD_ROOT="$PWD/local/upstream/gh-md" gh md --list --format=json
GH_MD_ROOT="$PWD/local/upstream/gh-md" gh md --list '--filter=updated > now - duration("48h")'
```

A code checkout has no reflog, so capture the commit before syncing and diff afterwards:

```sh
git -C local/upstream/atag rev-parse origin/main   # run before `just sync-upstream`
just sync-upstream
git -C local/upstream/atag log --oneline <previous-commit>..origin/main
```

The same applies to We4Authors: capture its `origin/main` before syncing, then log the range.

Then check the upstream `minutes/` and `index.html` files against the pages that cite them. Wiki paths are `.md` files at the wiki checkout root.

## Update this workspace

Only touch pages affected by the change. Follow `docs/contributing/README.md` and `docs/contributing/style-guide.md`.

- **Upstream references** in `docs/knowledge-base/atag/`, `docs/knowledge-base/atag-cg/`, and `docs/knowledge-base/atag-wg/`: update facts, links, and summaries that the new upstream content contradicts or supersedes.
- **Workspace research** in `docs/cg-contributions/`, including the WCAG 3 provision reviews: revise notes and recommendations whose evidence moved, especially when a discussion reached a resolution, a new draft branch appears, or a WCAG 3 issue or pull request settles a provision's ATAG relationship.
- **Citations**: link to the live GitHub or W3C URL, not to `local/upstream/`; the mirror is a local aid.
- **Meeting minutes**: append new items rather than rewriting history, and cite the minute's URL.

Do not invent upstream positions: if a discussion is unresolved, say so. Never rewrite pages wholesale: re-reading every page is not a sync.

## Maintain the global reference list

`docs/contributing/abbreviations.md` is appended to every page by `pymdownx.snippets` (`auto_append` in `mkdocs.yml`), so a reference definition there resolves on any page, and the title in the definition becomes the link tooltip:

```text
[ATAG#12]: https://github.com/w3c-cg/atag/discussions/12 "Types of Authoring Tools"
```

Pages cite the item as `[ATAG#12]`. The prefix names the upstream repository, so the ATAG and WCAG 3 mirrors never collide in number space. Within a repository, numbers are unique across issues, pull requests, and discussions, so one label per number covers all three types; the mirror's frontmatter tells you which type an item is.

Only sources with a `reference_prefix` in `scripts/sync_upstream.py` are registered: ATAG is registered as `ATAG#`, and WCAG 3 is mirrored without a prefix, so its items have no shorthand yet. Registering it means setting its `reference_prefix` and updating the pages that would cite it.

The list covers every mirrored item of a registered source, not just the ones pages currently cite, so a new citation rarely needs a manual edit. `just sync-upstream` regenerates it after each sync. To regenerate it offline from the existing mirror:

```sh
just sync-upstream --references-only
```

`scripts/sync_upstream.py` reads the frontmatter of `local/upstream/gh-md/<owner>/<repo>/{issues,pulls,discussions}/*.md`, sorts by number, groups the entries by source under a comment naming that source, and rewrites only the block between `<!-- BEGIN upstream references -->` and `<!-- END upstream references -->`. It quotes each title for the tooltip, switching to single quotes when a title contains double quotes, and stops with an error when a title contains both quote characters (add that entry by hand), when two items share a number, or when the mirror is empty.

- Do not reorder or hand-edit the generated block: change the upstream item, sync, then re-run the script.
- References that are not GitHub items, such as `[UCR]: https://w3c-cg.github.io/atag/docs/ucr/ 'Use Cases and Requirements draft'`, live outside the markers and stay hand-maintained.
- A missing definition does not fail the build: the shorthand renders as literal text. Grep the built page for the label to confirm it resolved.

## Verify

```sh
just lint-prose
just build-docs
```

Unresolved `[ATAG#N]` shorthand renders as literal text rather than failing the build, so grep the page you touched for the label (`grep -o '\[ATAG#[0-9]\+]' site/<page>/index.html`); inline code examples of the syntax match too.

Report each upstream commit, wiki commit, and item counts you synced, and list the workspace pages you changed.
