#!/usr/bin/env python3
"""Remove 'resources' / workplace environment projects from site-wide nav and pages."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Submenu or footer <li> linking to #resources or data-scroll="resources".
LI_BLOCK = re.compile(
    r'\s*<li class="[^"]*">\s*<a\b[^>]*(?:href="[^"]*#resources[^"]*"|data-scroll="resources")[^>]*>.*?</li>',
    re.DOTALL,
)

# Resources section on our-business pages.
RESOURCES_SECTION = re.compile(
    r"\s*<!-- Resources Start -->.*?<!-- Resources End -->",
    re.DOTALL,
)


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
    new_text, count = LI_BLOCK.subn("", text)
    return new_text, count


def strip_section(text: str) -> tuple[str, int]:
    return RESOURCES_SECTION.subn("", text)


def nav_still_has_resources(text: str) -> bool:
    for marker in ('class="menu_sub"', "ft_col"):
        pos = text.find(marker)
        if pos == -1:
            continue
        chunk = text[pos : pos + 8000]
        if "#resources" in chunk or 'data-scroll="resources"' in chunk:
            return True
    return False


def main() -> None:
    li_removed = 0
    files_updated = 0
    sections_removed = 0
    remaining = 0

    for path in html_files():
        original = path.read_text(encoding="utf-8")
        updated, li_count = strip_items(original)
        updated, sec_count = strip_section(updated)
        total = li_count + sec_count
        if total:
            path.write_text(updated, encoding="utf-8")
            files_updated += 1
            li_removed += li_count
            sections_removed += sec_count
            if li_count or sec_count:
                print(f"{path.relative_to(ROOT)}: -{li_count} links, -{sec_count} sections")
        if nav_still_has_resources(updated if total else original):
            remaining += 1

    print("---")
    print(f"files updated: {files_updated}")
    print(f"menu links removed: {li_removed}")
    print(f"page sections removed: {sections_removed}")
    print(f"files still referencing #resources in nav/footer: {remaining}")


if __name__ == "__main__":
    main()
