---
name: research-workspace
description: Maintain the ATAG research workspace (thibaudcolas/atag-research). Use when adding research notes, knowledge-base pages, or ATAG CG documentation to this MkDocs site.
license: MIT
metadata:
  version: "1.1.0"
---

# Research workspace

Work from the target repository's `AGENTS.md`, `docs/contributing/README.md`, and `docs/contributing/style-guide.md` for its current structure, commands, and writing conventions.

Place reusable knowledge in `docs/knowledge-base/`, evergreen upstream references in `docs/knowledge-base/atag/`, `docs/knowledge-base/atag-cg/`, and `docs/knowledge-base/wcag.md`, and the workspace's own research contributions in `docs/cg-contributions/`. Unpublished source material (meeting minutes, provisions data, downloaded context) lives in `local/`; cite it rather than copying it into the site. Refresh the upstream mirror under `local/upstream/` with `just sync-upstream`, or use the `upstream-sync` skill, before relying on upstream material. Section landing pages use `README.md` so they work on GitHub as well as the docs site.

When adding, moving, or renaming documentation, update both `nav` and the `llmstxt.sections` mapping in `mkdocs.yml`. Use relative Markdown links between documentation pages. Preserve source citations and distinguish findings from assumptions in research notes.

Run `just build-docs` after changes to catch navigation and link errors. The equivalent command is `uv run mkdocs build --strict`. Follow the repository's formatting and link-checking commands before completing the work.
