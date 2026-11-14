---
search:
  boost: 1.5
---

# Contribution guidelines

Thank you for considering to help this project.

## Project architecture

See [Project architecture](architecture.md) for how the workspace and its tooling are organized.

## Development

### Installation

> Requirements: [`uv`](https://github.com/astral-sh/uv), [Node.js and pnpm](https://nodejs.org/en/download) (use the version in `.node-version`), [just](https://github.com/casey/just), [prek](https://prek.j178.dev/), [lychee](https://lychee.cli.rs/)

Clone the repository, configure the git hooks, then initialize with `just init`.

```sh
git clone git@github.com:thibaudcolas/atag-research.git
cd atag-research/
# Install everything.
just init
```

Initialization installs Python and pnpm dependencies and downloads the pinned Vale binary for prose checks. This first run requires network access; the checked-in Vale rules need no separate style download.

#### Upstream sources

Research depends on the current state of the upstream [w3c-cg/atag](https://github.com/w3c-cg/atag) repository, its issues, pull requests, discussions, and wiki. `just sync-upstream` mirrors them read-only into the git-ignored `local/upstream/` directory, which research notes read from:

| Path                         | Contents                                         |
| ---------------------------- | ------------------------------------------------ |
| `local/upstream/atag/`       | Code and minutes, checked out on upstream `main` |
| `local/upstream/gh-md/atag/` | Issues, pull requests, and discussions           |
| `local/upstream/atag-wiki/`  | Wiki pages                                       |

Install the tools the sync uses beyond `git`, which is already required:

```sh
brew install gh           # GitHub CLI
gh auth login
gh extension install jackchuka/gh-md
```

Run `just sync-upstream` after installing, and whenever you need current upstream content; it is incremental and safe to re-run. Sources whose upstream feature or tooling is unavailable are skipped with a message. Commit and push nothing from `local/upstream/`. Refresh it before citing upstream material in a research note.

### Commands

- `just help`: See what commands are available.
- `just init`: Install dependencies and initialize for development.
- `just lint`: Lint the project.
- `just lint-prose`: Check prose terminology and common American English spellings with Vale.
- `just format *paths="."`: Format project files.
- `just check-links`: Check local links without network access.
- `just check-external-links`: Check HTTP(S) sources separately.
- `just build-docs`: Build the documentation.
- `just test`: Test agent skill publishing and documentation rendering.
- `just docs`: Build the documentation and serve it locally.
- `just sync-upstream`: Sync the upstream repository, issues, pull requests, discussions, and wiki into `local/upstream/`. See [Upstream sources](#upstream-sources).

## Coding style & conventions

We follow [PEP 8](https://peps.python.org/pep-0008/) for Python code style, enforced automatically by `ruff`:

- **Python**: formatted with `ruff format`, linted with `ruff check`. Configuration in `pyproject.toml`.
- **Other files**: formatted with `prettier` (see `prettier.config.js`).
- **Indentation**: 4 spaces, no tabs.
- **Type annotations**: required on all production code, checked by `mypy` with strict settings and by `ty` (experimental).
- **Naming**: `snake_case` for functions, methods, and variables; `PascalCase` for classes; `UPPER_CASE` for constants. Test modules follow `test_*.py`, test functions `test_*`, test classes `Test*`.
- **Imports**: organized automatically by `ruff` (isort rules in `pyproject.toml`).
- **Error handling**: use specific exception types; avoid bare `except:` clauses (BLE rules).
- **Comments**: avoid hard-wrapping lines, except at full stops, or other punctuation like commas if must be.

## Documentation

Good documentation helps users and contributors understand the project without reading source code. We aim for docs that are accurate, discoverable, and maintainable.

For prose style, tone, terminology, headings, and linking conventions, follow the [documentation style guide](style-guide.md).

### Prose documentation

- User-facing docs live in `docs/`; the README is the entry point.
- Keep language concise and in **Sentence case** (no Title Case).
- Follow the [documentation style guide](style-guide.md) for tone, terminology, headings, and linking conventions.
- Run `just format` before committing so prettier formats Markdown files consistently.

### MkDocs configuration

The documentation site is built with [MkDocs](https://www.mkdocs.org/) from the Markdown files in `docs/`, configured in `mkdocs.yml`. When you add, rename, or move pages, keep the configuration in sync with the file structure:

- **Landing pages**: each section folder uses a `README.md` as its landing page, so it also renders when browsing the folder on GitHub.
- **Navigation**: the `nav` key should list all pages of the site.
- **llms.txt**: the `llmstxt` plugin's `sections` key lists the pages included in the generated `llms-full.txt`. Add new section landing pages there as well.

`mkdocs.yml` documents each option with an inline comment. The Markdown-facing syntax for features such as code annotations, tabbed blocks, or page tags is documented in the [documentation style guide](style-guide.md); the build-time behavior of each plugin is described in [Project architecture](architecture.md#documentation-build).

Every docs page must be listed in `nav`, or explicitly opted out:

- Working drafts are published like any other page, with a draft-status callout at the top (see the [style guide](style-guide.md#callouts-and-blockquotes)).
- Files that aren't pages (snippet sources like `contributing/abbreviations.md`) are listed in `exclude_docs`.
- Pages intentionally published outside `nav` must match the top-level `not_in_nav` setting in `mkdocs.yml`, which accepts file patterns relative to `docs/`:

```yaml
not_in_nav: |
  /cg-contributions/supporting-notes.md
```

This only suppresses navigation warnings; the page remains published and searchable. Use the [search controls](style-guide.md#search-controls) to adjust search separately.

Run `just build-docs` to check your changes – it builds with `--strict`, so missing nav entries, unresolved links, and broken anchors fail the build.

## Pull request workflow

1. Create a branch from `main` with a descriptive name.
2. Make your changes, following the coding style and testing guidelines above.
3. Run `just lint`, `just check-links`, `just build-docs`, and `just test` locally. Run `just check-external-links` when adding or updating sources.
4. Open a pull request with a clear description of what the change does and why. Include relevant test evidence (commands and their output) and links to related issues.
5. CI runs linting (ruff, mypy, ty, prettier, Vale), local link checking, tests, and a strict documentation build. External links run in a separate workflow; investigate failures as broken or unverified sources. That workflow also runs weekly and does not gate deployment.
6. Squash merge when approved. Keep the commit message concise, in the imperative mood, and using Sentence case (no Title Case).

## Support guidelines

### Static typing

All project code should pass static type checking by [mypy](https://mypy.readthedocs.io/en/latest/index.html), with as strict of a configuration as possible, and tentatively also pass type checks with the [ty](https://docs.astral.sh/ty/) checker.
