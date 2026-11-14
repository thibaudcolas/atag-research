"""Regenerate the upstream reference links in the documentation.

Reads the gh-md mirror under `local/upstream/gh-md/` and rewrites the marked block in
`docs/contributing/abbreviations.md`, so the `[#12]` shorthand resolves on every page and
its definition title becomes the link tooltip.
"""

import re
import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent.parent
MIRROR = ROOT / "local/upstream/gh-md/w3c-cg/atag"
TARGET = ROOT / "docs/contributing/abbreviations.md"
START = "<!-- BEGIN upstream references -->"
END = "<!-- END upstream references -->"
KINDS = ("issues", "pulls", "discussions")


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


def _items() -> list[tuple[int, str, str]]:
    """Collect the number, URL, and title of every mirrored item."""
    items: list[tuple[int, str, str]] = []
    for kind in KINDS:
        for path in sorted((MIRROR / kind).glob("*.md")):
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
        raise SystemExit(f"{MIRROR}: no mirrored items, run `just sync-upstream` first")
    numbers = [number for number, _, _ in items]
    duplicates = sorted({number for number in numbers if numbers.count(number) > 1})
    if duplicates:
        raise SystemExit(f"{MIRROR}: duplicate item numbers {duplicates}")
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


def main() -> None:
    """Rewrite the reference block, and report how many entries it holds."""
    entries = [
        f"[#{number}]: {url} {_tooltip(title)}" for number, url, title in _items()
    ]
    block = "\n".join([START, "", *entries, "", END])
    text = TARGET.read_text(encoding="utf-8")
    pattern = re.compile(rf"{re.escape(START)}.*?{re.escape(END)}", re.DOTALL)
    if not pattern.search(text):
        raise SystemExit(f"{TARGET}: expected {START} and {END} markers")
    TARGET.write_text(pattern.sub(lambda _: block, text), encoding="utf-8")
    sys.stdout.write(
        f"{TARGET.relative_to(ROOT)}: {len(entries)} upstream references.\n"
    )


if __name__ == "__main__":
    main()
