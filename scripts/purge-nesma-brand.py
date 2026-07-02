#!/usr/bin/env python3
"""Remove visible Nesma / نسما branding from HTML site-wide."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

HTTRACK_COMMENT = re.compile(
    r"\s*<!-- Mirrored from nesmapartners\.com/[^>]+-->\s*",
    re.IGNORECASE,
)

REPLACEMENTS: list[tuple[re.Pattern[str], str]] = [
    (re.compile(r"Nesma\s*&amp;\s*Partners(?:’|')?", re.I), "Alruwais"),
    (re.compile(r"Nesma\s*&\s*Partners(?:’|')?", re.I), "Alruwais"),
    (re.compile(r"Nesma\s+and\s+Partners", re.I), "Alruwais"),
    (re.compile(r"NesmaKent", re.I), "Alruwais"),
    (re.compile(r"Nesma\s+High\s+Training\s+Institute(?:s)?", re.I), "Alruwais Training Institute"),
    (re.compile(r"Nesma\s+Partners", re.I), "Alruwais"),
    (re.compile(r"\bNesma\b"), "Alruwais"),
    (re.compile(r"شركة\s+نسما\s*و\s*شرك(?:اهم|ائها|ائه)"), "شركة الرويس"),
    (re.compile(r"نسما\s*و\s*شرك(?:اهم|ائها|ائه)"), "الرويس"),
    (re.compile(r"معهد\s+نسما\s+العالي\s+للتدريب"), "معهد الرويس للتدريب"),
    (re.compile(r"نسما\s+العالي\s+للتدريب"), "الرويس للتدريب"),
    (re.compile(r"نسما"), "الرويس"),
    (re.compile(r"https://nesmapartners\.com/", re.I), "https://alruwais.com.sa/"),
    (re.compile(r"http://nesmapartners\.com/", re.I), "https://alruwais.com.sa/"),
    (re.compile(r"nesmapartners\.com", re.I), "alruwais.com.sa"),
    (re.compile(r"Copyright\s*©?\s*\d{4},?\s*Alruwais\.\s*All Rights Reserved\.", re.I), "Copyright © 2026, Alruwais. All Rights Reserved."),
    (re.compile(r"Copyright\s*2025\s+Alruwais\.\s*All Rights Reserved\.", re.I), "Copyright © 2026, Alruwais. All Rights Reserved."),
]

HOME_LINKS = [
    (re.compile(r'(<a href=")ar/nesma-partners\.html(">\s*الرئيسية)'), r"\1index.html\2"),
    (re.compile(r'(<a href=")en/nesma-partners\.html(">\s*Home)'), r"\1en.html\2"),
    (re.compile(r'(<a href=")\.\./nesma-partners\.html(">\s*Home)'), r"\1../en.html\2"),
    (re.compile(r'(<a href=")\.\./nesma-partners\.html(">\s*الرئيسية)'), r"\1../index.html\2"),
    (re.compile(r'(<a href=")nesma-partners\.html(">\s*Home)'), r"\1../en.html\2"),
    (re.compile(r'(<a href=")nesma-partners\.html(">\s*الرئيسية)'), r"\1../index.html\2"),
    (re.compile(r'(<a href=")\.\./\.\./nesma-partners\.html(">\s*Home)'), r"\1../../en.html\2"),
    (re.compile(r'(<a href=")\.\./\.\./nesma-partners\.html(">\s*الرئيسية)'), r"\1../../index.html\2"),
]


def html_files() -> list[Path]:
    files: list[Path] = []
    for name in ("ar.html", "en.html", "index.html"):
        path = ROOT / name
        if path.is_file():
            files.append(path)
    files.extend(ROOT.rglob("*.html"))
    return sorted(set(p for p in files if "_archived" not in p.parts and "scripts" not in p.parts))


def patch(text: str) -> str:
    text = HTTRACK_COMMENT.sub("\n", text)
    for pattern, repl in REPLACEMENTS:
        text = pattern.sub(repl, text)
    for pattern, repl in HOME_LINKS:
        text = pattern.sub(repl, text)
    return text


def visible_nesma(text: str) -> bool:
    body = re.sub(r"<script[\s\S]*?</script>", "", text, flags=re.I)
    body = re.sub(r"<!--[\s\S]*?-->", "", body)
    body = re.sub(r'href="[^"]*"', "", body)
    return bool(re.search(r"Nesma|نسما|nesmapartners", body, re.I))


def main() -> None:
    changed = 0
    remaining: list[str] = []

    for path in html_files():
        original = path.read_text(encoding="utf-8")
        updated = patch(original)
        if updated != original:
            path.write_text(updated, encoding="utf-8")
            changed += 1
        if visible_nesma(updated):
            remaining.append(str(path.relative_to(ROOT)))

    print("--- nesma brand purge ---")
    print(f"files updated: {changed}")
    print(f"files with remaining visible nesma/نسما (excl href): {len(remaining)}")
    for rel in remaining[:25]:
        print(f"  - {rel}")
    if len(remaining) > 25:
        print(f"  ... and {len(remaining) - 25} more")


if __name__ == "__main__":
    main()
