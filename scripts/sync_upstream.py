#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.14"
# dependencies = ["pyyaml>=6.0"]
# ///
"""Mirror the upstream repositories into local/upstream/.

Every source listed in `SOURCES` mirrors three things, each skipped when the upstream repository
does not have it:

- `local/upstream/<directory>`: git checkout, with a read-only `origin` remote.
- `local/upstream/gh-md/<owner>/<repo>`: issues, pull requests, and discussions, via the gh-md extension.
- `local/upstream/<directory>-wiki`: wiki pages, from the repository's separate wiki git repository.

After syncing, regenerate the upstream reference links in `docs/contributing/abbreviations.md`
from the gh-md mirror, so the `[ATAG#12]` shorthand resolves on every page
and its definition title becomes the link tooltip.
A source without a `reference_prefix`, such as wcag3, is mirrored but not registered there.

Safe to re-run: every step updates an existing mirror in place.
Local edits in a code checkout are kept, and reported rather than discarded.
Pass `--only <repo>` to sync a single source.
"""

import argparse
import os
import re
import shutil
import subprocess  # noqa: S404
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent.parent
MIRROR = ROOT / "local/upstream"
GH_MD = MIRROR / "gh-md"

TARGET = ROOT / "docs/contributing/abbreviations.md"
START = "<!-- BEGIN upstream references -->"
END = "<!-- END upstream references -->"
KINDS = ("issues", "pulls", "discussions")


@dataclass(frozen=True)
class Source:
    """An upstream repository, and how to mirror it under local/upstream/."""

    repo: str
    directory: str
    reference_prefix: str | None
    branch: str = "main"

    @property
    def url(self) -> str:
        """HTTPS URL of the repository."""
        return f"https://github.com/{self.repo}.git"

    @property
    def upstream(self) -> str:
        """The remote-tracking ref of the default branch."""
        return f"origin/{self.branch}"

    @property
    def wiki_url(self) -> str:
        """HTTPS URL of the repository's separate wiki repository."""
        return f"https://github.com/{self.repo}.wiki.git"

    @property
    def checkout(self) -> Path:
        """Path of the code checkout."""
        return MIRROR / self.directory

    @property
    def wiki(self) -> Path:
        """Path of the wiki checkout."""
        return MIRROR / f"{self.directory}-wiki"

    @property
    def items(self) -> Path:
        """Path where gh-md mirrors the issues, pull requests, and discussions."""
        return GH_MD / self.repo


SOURCES = (
    Source(repo="w3c-cg/atag", directory="atag", reference_prefix="ATAG"),
    Source(repo="w3c/wcag3", directory="wcag3", reference_prefix=None),
    Source(repo="mgifford/We4Authors", directory="we4authors", reference_prefix=None),
)


def say(message: str) -> None:
    """Report progress on standard output."""
    sys.stdout.write(f"{message}\n")
    sys.stdout.flush()


def run(
    command: str,
    *args: str | Path,
    check: bool = True,
    capture: bool = True,
    env: dict[str, str] | None = None,
) -> subprocess.CompletedProcess[str]:
    """Run a command found on PATH, capturing its output as text unless told to stream it."""
    executable = shutil.which(command)
    if executable is None:
        raise SystemExit(f"{command} is required but was not found on PATH")
    return subprocess.run(  # noqa: S603
        [executable, *map(str, args)],
        check=check,
        capture_output=capture,
        text=True,
        env=env,
    )


def git(directory: Path, *args: str) -> str:
    """Run git in a checkout, using its git directory so nested checkouts never resolve the outer repository."""
    try:
        result = run("git", "-C", directory, "--git-dir=.git", *args)
    except subprocess.CalledProcessError as error:
        raise SystemExit(
            f"git {' '.join(args)} failed in {directory.relative_to(ROOT)}:\n{error.stderr.strip()}"
        ) from error
    return result.stdout.strip()


def capability(repo: str, name: str) -> str:
    """Read a repository capability; an unreachable API returns "" and every source is synced."""
    if shutil.which("gh") is None:
        return ""
    result = run("gh", "api", f"repos/{repo}", "--jq", f".{name}", check=False)
    return result.stdout.strip() if result.returncode == 0 else ""


# ---- Repository checkout -----------------------------------------------------------------


def sync_repository(source: Source, reclone: bool) -> None:
    """Clone or fast-forward the code checkout, keeping local changes."""
    checkout = source.checkout
    if (checkout / ".git").is_dir():
        current = git(checkout, "remote", "get-url", "origin")
        if current != source.url:
            if not reclone:
                raise SystemExit(
                    f"error: {checkout.relative_to(ROOT)} has origin {current}, expected {source.url}.\n"
                    "Run: just sync-upstream --reclone  (replaces it with a clean checkout)"
                )
            shutil.rmtree(checkout)

    if (checkout / ".git").is_dir():
        git(checkout, "fetch", "--prune", "--quiet", "origin")
    else:
        run("git", "clone", "--quiet", source.url, checkout)

    # Fast-forward only: never merge, rebase, or check out over uncommitted work.
    git(checkout, "checkout", "--quiet", source.branch)
    git(checkout, "merge", "--ff-only", "--quiet", source.upstream)

    status = git(checkout, "-c", "status.branch=false", "status", "--short")
    if status:
        say(f"Kept local changes in {checkout.relative_to(ROOT)}:\n{status}")
    else:
        say(
            f"{source.repo}: {source.branch} at "
            f"{git(checkout, 'rev-parse', '--short', source.upstream)}"
        )


# ---- Issues, pull requests, discussions --------------------------------------------------


def sync_items(source: Source, has_issues: str, has_discussions: str) -> bool:
    """Pull issues, pull requests, and discussions with gh-md. Return whether it ran."""
    skipped = f"Skipped {source.repo} issues, pull requests, and discussions"
    if shutil.which("gh") is None:
        say(
            f"{skipped}: install the GitHub CLI (https://cli.github.com), then run: gh auth login"
        )
        return False
    if run("gh", "auth", "status", check=False).returncode != 0:
        say(f"{skipped}: run: gh auth login")
        return False
    extensions = run("gh", "extension", "list", check=False).stdout
    if not any(line.startswith("gh md\t") for line in extensions.splitlines()):
        say(f"{skipped}: run: gh extension install jackchuka/gh-md")
        return False
    if has_issues and has_issues != "true":
        say(f"Skipped {source.repo} issues and pull requests: issues are disabled.")
        return False

    types = ["--issues", "--prs"]
    if has_discussions in ("true", ""):
        types.append("--discussions")
    run(
        "gh",
        "md",
        "pull",
        source.repo,
        *types,
        capture=False,
        env={**os.environ, "GH_MD_ROOT": str(GH_MD)},
    )
    return True


# ---- Wiki --------------------------------------------------------------------------------


def sync_wiki(source: Source, has_wiki: str) -> None:
    """Clone or fast-forward the wiki checkout."""
    wiki = source.wiki
    if has_wiki == "false":
        say(f"Skipped the {source.repo} wiki: the wiki is disabled.")
        return
    if (wiki / ".git").is_dir():
        branch = git(wiki, "rev-parse", "--abbrev-ref", "HEAD")
        git(wiki, "fetch", "--prune", "--quiet", "origin")
        git(wiki, "merge", "--ff-only", "--quiet", f"origin/{branch}")
        say(
            f"{source.repo} wiki: {branch} at {git(wiki, 'rev-parse', '--short', f'origin/{branch}')}"
        )
        return
    # An enabled wiki has no repository until a first page is saved, so check the remote exists.
    probe = run("git", "ls-remote", "--quiet", source.wiki_url, check=False)
    if probe.returncode != 0:
        say(f"Skipped the {source.repo} wiki: no wiki pages exist yet.")
        return
    run("git", "clone", "--quiet", source.wiki_url, wiki)
    branch = git(wiki, "rev-parse", "--abbrev-ref", "HEAD")
    say(f"{source.repo} wiki: {branch} at {git(wiki, 'rev-parse', '--short', 'HEAD')}")


# ---- Upstream reference links ------------------------------------------------------------


def _front_matter(path: Path) -> dict[str, Any]:
    """Read the YAML front matter of a mirrored item."""
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0] != "---" or "---" not in lines[1:]:
        raise SystemExit(f"{path}: expected YAML front matter")
    try:
        data = yaml.safe_load("\n".join(lines[1 : lines.index("---", 1)]))
    except yaml.YAMLError as error:
        raise SystemExit(f"{path}: invalid YAML front matter") from error
    if not isinstance(data, dict):
        raise SystemExit(f"{path}: front matter must be a mapping")
    return data


def _items(source: Source) -> list[tuple[int, str, str]]:
    """Collect the number, URL, and title of every mirrored item."""
    items: list[tuple[int, str, str]] = []
    for kind in KINDS:
        for path in sorted((source.items / kind).glob("*.md")):
            data = _front_matter(path)
            number = data.get("number")
            url = data.get("url")
            title = data.get("title")
            if (
                not isinstance(number, int)
                or not isinstance(url, str)
                or not isinstance(title, str)
            ):
                raise SystemExit(f"{path}: expected number, url, and title")
            items.append((number, url, " ".join(title.split())))
    if not items:
        raise SystemExit(
            f"{source.items}: no mirrored items, run `just sync-upstream` first"
        )
    numbers = [number for number, _, _ in items]
    duplicates = sorted({number for number in numbers if numbers.count(number) > 1})
    if duplicates:
        raise SystemExit(f"{source.items}: duplicate item numbers {duplicates}")
    return sorted(items)


def _tooltip(title: str) -> str:
    """Quote a title so Markdown keeps it as the link tooltip."""
    if '"' not in title:
        return f'"{title}"'
    if "'" not in title:
        return f"'{title}'"
    raise SystemExit(
        f"Title has both quote characters, add its reference by hand: {title}"
    )


def update_references() -> None:
    """Rewrite the reference block, and report how many entries it holds."""
    lines = [START]
    counts: list[str] = []
    for source in SOURCES:
        prefix = source.reference_prefix
        if prefix is None:
            continue
        items = _items(source)
        counts.append(f"{prefix} {len(items)}")
        lines.extend(["", f"<!-- {prefix}: {source.repo} -->"])
        lines.extend(
            f"[{prefix}#{number}]: {url} {_tooltip(title)}"
            for number, url, title in items
        )
    lines.extend(["", END])
    block = "\n".join(lines)

    text = TARGET.read_text(encoding="utf-8")
    pattern = re.compile(rf"{re.escape(START)}.*?{re.escape(END)}", re.DOTALL)
    if not pattern.search(text):
        raise SystemExit(f"{TARGET}: expected {START} and {END} markers")
    TARGET.write_text(pattern.sub(lambda _: block, text), encoding="utf-8")

    say(f"{TARGET.relative_to(ROOT)}: {', '.join(counts)} upstream references.")


# ---- Entry point -------------------------------------------------------------------------


def main() -> None:
    """Sync every upstream source, then regenerate the reference links."""
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--reclone",
        action="store_true",
        help="replace a code checkout whose origin does not point at its upstream repository",
    )
    parser.add_argument(
        "--only",
        metavar="REPO",
        help="sync only the source with this repository, leaving the other mirrors untouched",
    )
    parser.add_argument(
        "--references-only",
        action="store_true",
        help="only regenerate the reference links from the existing mirror, offline",
    )
    options = parser.parse_args()

    if options.references_only:
        update_references()
        return

    sources: tuple[Source, ...] = SOURCES
    if options.only:
        sources = tuple(source for source in SOURCES if source.repo == options.only)
        if not sources:
            known = ", ".join(source.repo for source in SOURCES)
            raise SystemExit(
                f"error: {options.only} is not a source in SOURCES: {known}"
            )

    if shutil.which("git") is None:
        raise SystemExit("git is required: https://git-scm.com/downloads")

    MIRROR.mkdir(parents=True, exist_ok=True)
    pulled = False
    for source in sources:
        say(f"Syncing {source.repo} into local/upstream/")
        has_wiki = capability(source.repo, "has_wiki")
        has_issues = capability(source.repo, "has_issues")
        has_discussions = capability(source.repo, "has_discussions")

        sync_repository(source, options.reclone)
        pulled = sync_items(source, has_issues, has_discussions) or pulled
        sync_wiki(source, has_wiki)

    if pulled:
        update_references()
    else:
        say("Skipped the upstream reference links: no issues were pulled.")


if __name__ == "__main__":
    main()
