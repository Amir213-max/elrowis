#!/usr/bin/env python3
"""Archive sustainability pages and remove all site links (reversible).

Restore: copy _archived/sustainability/ar.html -> ar/sustainability.html
         copy _archived/sustainability/en.html -> en/sustainability.html
         then re-run site nav sync or restore from git.
"""

from __future__ import annotations

import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ARCHIVE_DIR = ROOT / "_archived" / "sustainability"

BURGER_SUSTAINABILITY = re.compile(
    r"\s*<li class=\"_ele\">\s*<a href=\"(?:\.\./)*(?:en/|ar/)?sustainability\.html\">"
    r"(?:Sustainability|الاستدامة)</a>\s*</li>",
    re.IGNORECASE,
)

MAIN_NAV_SUSTAINABILITY = re.compile(
    r"\s*<li class=\"f a-c j-c\">\s*"
    r"<a href=\"(?:\.\./)*(?:en/|ar/)?sustainability\.html\"[^>]*>.*?"
    r"</li>",
    re.DOTALL | re.IGNORECASE,
)

FOOTER_SUSTAINABILITY = re.compile(
    r"\s*<div class=\"ft_col f f-c a-s _eleWrap\">\s*"
    r"<strong class=\"_eleY\">(?:Sustainability|الاستدامة)</strong>.*?"
    r"</div>\s*(?=\s*<div class=\"ft_col)",
    re.DOTALL | re.IGNORECASE,
)

# Leftover dropdown items when the outer nav <li> was partially removed.
ORPHAN_SUSTAINABILITY_NAV = re.compile(
    r"\s*<li class=\"\">\s*<a href=\"(?:\.\./)*(?:en/|ar/)?sustainability\.html#[^\"]*\"[\s\S]*?"
    r"</div>\s*</li>\s*(?=<li class=\"f a-c j-c\">\s*<a href=\"(?:\.\./)*(?:en/|ar/)?media-room\.html\")",
    re.IGNORECASE,
)

REDIRECT_AR = """<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="utf-8">
    <meta name="robots" content="noindex, nofollow">
    <meta http-equiv="refresh" content="0; url=../index.html">
    <script>location.replace("../index.html");</script>
    <title>الرويس</title>
</head>
<body><p><a href="../index.html">العودة للرئيسية</a></p></body>
</html>
"""

REDIRECT_EN = """<!DOCTYPE html>
<html lang="en" dir="ltr">
<head>
    <meta charset="utf-8">
    <meta name="robots" content="noindex, nofollow">
    <meta http-equiv="refresh" content="0; url=../en.html">
    <script>location.replace("../en.html");</script>
    <title>Alruwais</title>
</head>
<body><p><a href="../en.html">Back to home</a></p></body>
</html>
"""


def html_files() -> list[Path]:
    files: list[Path] = []
    for name in ("ar.html", "en.html", "index.html"):
        path = ROOT / name
        if path.is_file():
            files.append(path)
    files.extend((ROOT / "ar").rglob("*.html"))
    files.extend((ROOT / "en").rglob("*.html"))
    return sorted(set(files))


def strip_sustainability_links(text: str) -> tuple[str, dict[str, int]]:
    counts = {"burger": 0, "nav": 0, "footer": 0, "orphan": 0}

    def burger_sub(_: re.Match[str]) -> str:
        counts["burger"] += 1
        return ""

    def nav_sub(_: re.Match[str]) -> str:
        counts["nav"] += 1
        return ""

    def footer_sub(_: re.Match[str]) -> str:
        counts["footer"] += 1
        return ""

    text = BURGER_SUSTAINABILITY.sub(burger_sub, text)
    text = MAIN_NAV_SUSTAINABILITY.sub(nav_sub, text)
    text = FOOTER_SUSTAINABILITY.sub(footer_sub, text)

    def orphan_sub(_: re.Match[str]) -> str:
        counts["orphan"] += 1
        return "\n                                            "

    text = ORPHAN_SUSTAINABILITY_NAV.sub(orphan_sub, text)
    return text, counts


def archive_pages() -> None:
    ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
    pairs = [
        (ROOT / "ar" / "sustainability.html", ARCHIVE_DIR / "ar.html"),
        (ROOT / "en" / "sustainability.html", ARCHIVE_DIR / "en.html"),
    ]
    for src, dest in pairs:
        if dest.is_file() and dest.stat().st_size > 5000:
            continue
        if src.is_file() and src.stat().st_size > 5000:
            shutil.copy2(src, dest)
    readme = ARCHIVE_DIR / "README.txt"
    readme.write_text(
        "Archived sustainability pages.\n"
        "Restore: copy ar.html -> ar/sustainability.html, en.html -> en/sustainability.html\n"
        "Then re-add navigation links from git history or a backup.\n",
        encoding="utf-8",
    )


def install_redirect_stubs() -> None:
    (ROOT / "ar" / "sustainability.html").write_text(REDIRECT_AR, encoding="utf-8")
    (ROOT / "en" / "sustainability.html").write_text(REDIRECT_EN, encoding="utf-8")


def main() -> None:
    archive_pages()
    install_redirect_stubs()

    totals = {"files": 0, "burger": 0, "nav": 0, "footer": 0, "orphan": 0}
    remaining = 0

    for path in html_files():
        if path.name == "sustainability.html":
            continue
        original = path.read_text(encoding="utf-8")
        updated, counts = strip_sustainability_links(original)
        if updated != original:
            path.write_text(updated, encoding="utf-8")
            totals["files"] += 1
            totals["burger"] += counts["burger"]
            totals["nav"] += counts["nav"]
            totals["footer"] += counts["footer"]
            totals["orphan"] += counts["orphan"]
        if re.search(r"sustainability\.html", updated if updated != original else original):
            remaining += 1

    print("--- sustainability removal ---")
    print(f"archived to: {ARCHIVE_DIR}")
    print(f"files updated: {totals['files']}")
    print(f"burger links removed: {totals['burger']}")
    print(f"main nav blocks removed: {totals['nav']}")
    print(f"footer columns removed: {totals['footer']}")
    print(f"orphan nav blocks removed: {totals['orphan']}")
    print(f"files still referencing sustainability.html: {remaining}")


if __name__ == "__main__":
    main()
