# gh-md reference

Command reference for the GitHub CLI extension this skill uses to mirror issues, pull requests, and discussions.
See [the skill](../SKILL.md) for when and how to sync.

GitHub CLI extension (`jackchuka/gh-md`). Pulls issues / PRs / discussions into Markdown with YAML frontmatter, incrementally syncs them, and pushes title, body, state, and comment edits back with conflict detection.

```bash
gh extension install jackchuka/gh-md   # once
gh auth login                          # required
brew install fzf                       # only for interactive browse
```

Files live in `~/.gh-md/<owner>/<repo>/{issues,pulls,discussions}/<number>.md`. Override the root with `GH_MD_ROOT` — set it per project when you want the mirror scoped to a workspace. This repo's own upstream, `w3c-cg/atag`, is already mirrored under `local/upstream/gh-md/` by `just sync-upstream`; see [the skill](../SKILL.md) before pulling it again.

## Workflow

1. **Pull** into the local mirror. Incremental: only items updated since the last sync are fetched.
2. **Read / grep / edit** the Markdown files directly, or get paths from `gh md --list --format=json`.
3. **Preview** with `push --dry-run`, then **push**.
4. **Prune** files for closed / merged items when they are no longer useful.

```bash
gh md pull w3c-cg/atag                    # all issues, PRs, discussions (all states)
gh md pull w3c-cg/atag --issues --limit 10
gh md pull https://github.com/w3c-cg/atag/issues/123
gh md repos                               # repositories already pulled
gh md --list --format=json                # repo, number, type, state, title, url, file_path
```

Inside a git repo: `gh md pull` on a PR branch pulls that PR with review comments; on main it pulls the whole repo. Agent-friendly reads: `GH_MD_ROOT="$PWD/<dir>" gh md pull <repo>`, then grep `<dir>`; use an absolute root so `gh md` resolves it outside the workspace root.

## Commands

`gh md [repo] [flags]` — with no subcommand, opens an interactive FZF browser (pre-filtered to the current repo/PR). Flags: `--issues`, `--prs`, `--discussions`, `--new` (browser view of items updated since last pull; returns nothing under `--list`), `--assigned`, `--filter <CEL>`, `--list`, `--format text|json|yaml` (`--format` only with `--list`).

`gh md pull [repo | url | owner/repo/<type>/<number>] [flags]` — `--all` (all managed repos), `--issues`, `--prs`, `--discussions`, `--limit N`, `--open-only`, `--full` (ignore last sync timestamp). Default fetches all states so local state stays accurate; single-item pulls always fetch. A bare name matches managed repos partially, else falls back to `<your-login>/<name>` like `gh repo clone`.

`gh md push [file-path | url] [flags]` — push title/body, open/closed state, new comments, edited comments. `--dry-run` previews; `--force` overrides a remote changed since the last pull. No args → FZF selector for the current repo.

`gh md prune [repo] [flags]` — dry-run by default; `--confirm` deletes. Removes issues/discussions with `state: closed` and PRs `merged`/`closed`, based on local frontmatter only (no network), so `pull` first if state may be stale. `--format text|json|yaml`.

`gh md repos [--format text|json|yaml]` — managed repositories with last sync time.

## CEL filters

Variables: `user`, `now`, `item_type`, `state`, `title`, `body`, `author`, `assigned`, `reviewers`, `labels`, `created`, `updated`, `owner`, `repo`, `number`.

```bash
gh md --filter 'state == "open"' --list
gh md --filter 'labels.exists(l, l == "bug")' --list
gh md --filter 'created > now - duration("168h")' --list   # last 7 days
```

## File format

```markdown
---
id: I_kwDOQUFZWc7Y6-gO
url: https://github.com/owner/repo/issues/123
number: 123
owner: owner
repo: repo
title: Example Issue
state: open
labels: [bug, help wanted]
assignees: [octocat]
created: 2026-01-01T00:00:00Z
updated: 2026-01-24T12:00:00Z
last_pulled: 2026-01-24T12:30:00Z
---

<!-- gh-md:content -->

# Example Issue

Issue body content here.
<!-- /gh-md:content -->

<!-- gh-md:comment
id: IC_def456
author: octocat
created: 2026-01-02T00:00:00Z
-->

### @octocat (2026-01-02)

Comment body.
<!-- /gh-md:comment -->

<!-- gh-md:new-comment -->

<!-- /gh-md:new-comment -->
```

Rules when editing:

- Edit the **body** only between `<!-- gh-md:content -->` and `<!-- /gh-md:content -->`; edit a **comment** only inside its `<!-- gh-md:comment … -->` … `<!-- /gh-md:comment -->` block. Text outside those markers is not pushed.
- New comments go between `<!-- gh-md:new-comment -->` and `<!-- /gh-md:new-comment -->`; the file's `state:` field controls open/closed.
- Titles change in frontmatter `title:` (the `# ` heading inside `content` is part of the body).
- Files for PRs also contain review comments; they are read-only context, not pushable.
- Sync state is tracked in `<root>/<owner>/<repo>/.gh-md-meta.yaml` (`sync: {pulls: <timestamp>}`), which drives incremental pulls. Do not hand-edit it.

## Agent notes

- Pull once, then grep/read the files. Prefer `--list --format=json` for machine-readable paths instead of FZF.
- Always `push --dry-run` before a real push, and never `--force` without checking what changed remotely (`gh md pull` the item first).
- `prune --confirm` deletes files irreversibly; run the dry-run and confirm the repo scope.
- Interactive browse (`gh md`, `gh md push` with no args) needs FZF and a TTY; in non-interactive shells use explicit paths/args.
- The extension name is `md`, so invoke it as `gh md …`, not `gh-md`.
