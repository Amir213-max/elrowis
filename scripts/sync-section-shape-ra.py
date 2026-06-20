#!/usr/bin/env python3
"""Replace diagonal section_shape accent with Ra (ر) logo shape site-wide."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

OLD_SVG = re.compile(
    r'<svg xmlns="http://www\.w3\.org/2000/svg" width="99" height="96" fill="none" viewBox="0 0 99 96">\s*'
    r'<path fill="#003d53" d="M99 38\.677V0L0 57\.323V96l99-57\.323Z"/>\s*'
    r"</svg>",
    re.MULTILINE,
)

NEW_SVG = (
    '<svg xmlns="http://www.w3.org/2000/svg" width="100" height="97" fill="none" '
    'viewBox="0 0 100 97" aria-hidden="true">\n'
    '                            <path fill="#003d53" '
    'd="M8.5 90.5L33.5 90.5L96.5 71.5Q96.5 69.5 96.5 67.5L96.5 10.5Q96.5 8.5 94.5 8.5'
    'L53.5 20L53.5 56L8.5 90.5Z"/>\n'
    "                        </svg>"
)

# Path-only fallback (whitespace variants)
OLD_PATH = 'd="M99 38.677V0L0 57.323V96l99-57.323Z"'
NEW_PATH = (
    'd="M8.5 90.5L33.5 90.5L96.5 71.5Q96.5 69.5 96.5 67.5L96.5 10.5Q96.5 8.5 94.5 8.5'
    'L53.5 20L53.5 56L8.5 90.5Z"'
)


def update_file(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    original = text

    text = OLD_SVG.sub(NEW_SVG, text)
    if OLD_PATH in text:
        text = text.replace(
            'width="99" height="96" fill="none" viewBox="0 0 99 96"',
            'width="100" height="97" fill="none" viewBox="0 0 100 97" aria-hidden="true"',
        )
        text = text.replace(OLD_PATH, NEW_PATH)

    if text != original:
        path.write_text(text, encoding="utf-8")
        return True
    return False


def main() -> None:
    changed = 0
    for path in ROOT.rglob("*.html"):
        if update_file(path):
            changed += 1
    print(f"Updated {changed} files")


if __name__ == "__main__":
    main()
