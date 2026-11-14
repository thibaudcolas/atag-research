# ATAG research

A shared workspace for research on the [Authoring Tool Accessibility Guidelines (ATAG)](https://www.w3.org/TR/ATAG20/), the ATAG Community Group, and working documents. Built for publishing at <https://thibaudcolas.github.io/atag-research/>.

Source material (meeting minutes, provisions data, minutes text conversions) lives in `local/`, which is not part of the published site.

## What's included

| Concern                 | Tool                                                                               |
| ----------------------- | ---------------------------------------------------------------------------------- |
| Documentation site      | [MkDocs](https://www.mkdocs.org/) + Material for MkDocs, built strictly in CI      |
| Task runner             | [just](https://github.com/casey/just) (`justfile`)                                 |
| Python deps             | [uv](https://github.com/astral-sh/uv) (`pyproject.toml`)                           |
| Python lint/format      | [ruff](https://github.com/astral-sh/ruff)                                          |
| Type checking           | [mypy](https://mypy-lang.org/) + [ty](https://docs.astral.sh/ty/)                  |
| Formatting (non-Python) | [prettier](https://prettier.io)                                                    |
| Git hooks               | [prek](https://prek.j178.dev/) (`prek.toml`)                                       |
| Link checking           | [lychee](https://lychee.cli.rs) (`lychee.toml`)                                    |
| CI + deploy             | GitHub Actions: lint, strict docs build, Pages deploy (`.github/workflows/ci.yml`) |

## Site features

Configured in `mkdocs.yml` (each option commented inline):

- Light/dark themes with a custom local color palette (`docs/theme/theme.css`).
- Last-modified dates from git history per page.
- [Tag index](docs/tags.md): page tags and shared folder metadata group related documentation.
- `llms.txt` / `llms-full.txt` generation for LLM consumption.
- [Agent skill publishing](docs/agent-skills.md), with raw skill files and discovery catalogs under `.well-known/`.
- Abbreviation tooltips: `docs/contributing/abbreviations.md` is auto-appended to every page.
- Strict link and nav validation: pages must be in `nav` or opted out; broken anchors fail the build.

## Getting started

Requirements: `uv`, `just`, `prek`, `lychee`, Node.js (`node-version` pins the version).

```sh
just init      # Install dependencies, set up hooks
just docs      # Serve the docs locally on http://localhost:8001
just build-docs  # Strict build (what CI runs)
just lint      # ruff + mypy + ty + prettier checks
just test      # Skill publishing tests
just format    # Auto-format
just check-links  # Link check (requires lychee)
```

## Adding content

1. Put reusable background material in `docs/knowledge-base/`, evergreen upstream references in `docs/knowledge-base/atag/`, `docs/knowledge-base/atag-cg/`, and `docs/knowledge-base/wcag.md`, and the workspace's own CG research in `docs/cg-contributions/`.
2. Add each page to both `nav` and the `llmstxt` `sections` mapping in `mkdocs.yml`.
3. Keep source material in `local/`; reference it from research notes rather than publishing it verbatim.
4. Every skill in `.agents/skills/` is published with the docs, so keep local-only material out of it.

GitHub Pages deploys from GitHub Actions on push to `main`; enable it in the repository settings once.

## License

MIT — see [LICENSE](LICENSE).
