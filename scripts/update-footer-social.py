#!/usr/bin/env python3
"""Update site-wide footer and mobile menu social links to Alruwais."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

LINKEDIN = "https://www.linkedin.com/company/alruwais/?viewAsMember=true"
INSTAGRAM = "https://www.instagram.com/alruwais.sa/"

LINKEDIN_OLD = re.compile(
    r"https://www\.linkedin\.com/company/(?:NesmaPartners|nesmapartners)/?",
    re.IGNORECASE,
)
INSTAGRAM_OLD = re.compile(
    r"https://www\.instagram\.com/(?:NesmaPartners|nesmapartners)/?",
    re.IGNORECASE,
)

# Old Nesma X / YouTube — remove from nav/footer social blocks only.
REMOVE_SOCIAL = re.compile(
    r"\s*<a\b[^>]*href=\"https://(?:twitter\.com/NesmaPartners|www\.youtube\.com/channel/UCCPaTe4CM2GxpQgAYsdy9IQ)\"[^>]*>.*?</a>",
    re.DOTALL | re.IGNORECASE,
)


def patch_html(text: str) -> tuple[str, dict[str, int]]:
    counts = {"linkedin": 0, "instagram": 0, "removed": 0}

    def linkedin_sub(match: re.Match[str]) -> str:
        counts["linkedin"] += 1
        return LINKEDIN

    def instagram_sub(match: re.Match[str]) -> str:
        counts["instagram"] += 1
        return INSTAGRAM

    updated = LINKEDIN_OLD.sub(linkedin_sub, text)
    updated = INSTAGRAM_OLD.sub(instagram_sub, updated)
    updated, removed = REMOVE_SOCIAL.subn("", updated)
    counts["removed"] = removed

    # Ensure external social links open safely.
    updated = updated.replace(
        f'href="{LINKEDIN}" target="_blank" class=',
        f'href="{LINKEDIN}" target="_blank" rel="noopener noreferrer" class=',
    )
    updated = updated.replace(
        f'href="{INSTAGRAM}" target="_blank" class=',
        f'href="{INSTAGRAM}" target="_blank" rel="noopener noreferrer" class=',
    )

    return updated, counts


def html_files() -> list[Path]:
    files: list[Path] = []
    for name in ("ar.html", "en.html", "index.html"):
        path = ROOT / name
        if path.is_file():
            files.append(path)
    files.extend(ROOT.glob("ar/**/*.html"))
    files.extend(ROOT.glob("en/**/*.html"))
    return sorted(set(files))


def main() -> None:
    totals = {"files": 0, "linkedin": 0, "instagram": 0, "removed": 0}
    remaining = 0

    for path in html_files():
        original = path.read_text(encoding="utf-8")
        updated, counts = patch_html(original)
        if updated != original:
            path.write_text(updated, encoding="utf-8")
            totals["files"] += 1
            totals["linkedin"] += counts["linkedin"]
            totals["instagram"] += counts["instagram"]
            totals["removed"] += counts["removed"]

        if any(
            old in updated
            for old in (
                "NesmaPartners",
                "nesmapartners",
                "twitter.com/NesmaPartners",
                "youtube.com/channel/UCCPaTe4CM2GxpQgAYsdy9IQ",
            )
        ):
            remaining += 1

    print("---")
    print(f"files updated: {totals['files']}")
    print(f"linkedin href updates: {totals['linkedin']}")
    print(f"instagram href updates: {totals['instagram']}")
    print(f"x/youtube links removed: {totals['removed']}")
    print(f"files still mentioning old Nesma social URLs: {remaining}")


if __name__ == "__main__":
    main()
