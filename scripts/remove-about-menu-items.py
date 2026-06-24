#!/usr/bin/env python3
"""Remove last 3 About Us submenu items site-wide."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

ANCHORS = ("corporate-governance", "code-of-conduct", "our-ecosystem")

# Remove one submenu <li> when the anchor appears in the same <a> tag (href hash or data-scroll).
LI_BY_ANCHOR = [
    re.compile(
        rf'\s*<li class="">\s*<a\b[^>]*(?:href="[^"]*{re.escape(anchor)}[^"]*"|data-scroll="{re.escape(anchor)}")[^>]*>.*?</li>',
        re.DOTALL,
    )
    for anchor in ANCHORS
]


def html_files() -> list[Path]:
    files: list[Path] = []
    for pattern in ("ar.html", "en.html", "index.html"):
        p = ROOT / pattern
        if p.is_file():
            files.append(p)
    files.extend((ROOT / "ar").rglob("*.html"))
    files.extend((ROOT / "en").rglob("*.html"))
    return sorted(set(files))


def strip_items(text: str) -> tuple[str, int]:
    total = 0
    for pattern in LI_BY_ANCHOR:
        text, count = pattern.subn("", text)
        total += count
    return text, total


def nav_still_has_anchors(text: str) -> bool:
    menu_start = text.find('class="menu_sub"')
    if menu_start == -1:
        return False
    menu_end = text.find("</ul>", menu_start)
    if menu_end == -1:
        menu_end = menu_start + 4000
    menu = text[menu_start:menu_end]
    return any(a in menu for a in ANCHORS)


def main() -> None:
    total_items = 0
    updated_files = 0
    remaining = 0

    for path in html_files():
        original = path.read_text(encoding="utf-8")
        updated, count = strip_items(original)
        if count:
            path.write_text(updated, encoding="utf-8")
            updated_files += 1
            total_items += count
            print(f"{path.relative_to(ROOT)}: removed {count}")
        if nav_still_has_anchors(updated if count else original):
            remaining += 1

    print("---")
    print(f"files updated: {updated_files}")
    print(f"menu items removed: {total_items}")
    print(f"nav files still referencing anchors: {remaining}")


if __name__ == "__main__":
    main()
