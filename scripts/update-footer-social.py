#!/usr/bin/env python3
"""Update site-wide footer and mobile menu social links to Alruwais."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

LINKEDIN = "https://www.linkedin.com/company/alruwais/?viewAsMember=true"
INSTAGRAM = "https://www.instagram.com/alruwais.sa/"
X_PROFILE = "https://x.com/Alruwaisco"
X_ICON_PATH = (
    'm.04 0 6.44 8.63L0 15.649h1.459l5.674-6.144 4.584 6.144h4.964L9.878 6.532 '
    "15.91 0h-1.458L9.226 5.658 5.004 0H.041Zm2.146 1.077h2.28l10.07 13.494h-2.281L2.185 1.077Z"
)

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

LINKEDIN_SOCIAL = re.compile(
    r'(\s*<a href="https://www\.linkedin\.com/company/alruwais/\?viewAsMember=true"[^>]*'
    r'class="rounded_button outline[^"]*"[^>]*>\s*<svg[^>]*>.*?</svg>\s*</a>)',
    re.DOTALL | re.IGNORECASE,
)

REMOVE_X_SOCIAL = re.compile(
    r'\n\s*<a href="https://x\.com/Alruwaisco"[^>]*>.*?</a>',
    re.DOTALL | re.IGNORECASE,
)


def x_social_link(indent: str, label_attr: str) -> str:
    inner = indent + "    "
    return (
        f'{indent}<a href="{X_PROFILE}" target="_blank" rel="noopener noreferrer" '
        f'class="rounded_button outline f a-c j-c magnet" data-dist="1.5" {label_attr}="X">\n'
        f'{inner}<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="none" viewBox="0 0 17 16">\n'
        f'{inner}    <path fill="currentColor" d="{X_ICON_PATH}"/>\n'
        f"{inner}</svg>\n"
        f"{indent}</a>"
    )


def add_x_social_links(text: str) -> tuple[str, int]:
    added = 0

    def linkedin_social_sub(match: re.Match[str]) -> str:
        nonlocal added
        block = match.group(1)
        tail = match.string[match.end() : match.end() + 120]
        if X_PROFILE in tail:
            return block
        first_line = block.split("\n", 1)[0]
        indent_match = re.match(r"^(\s*)", first_line)
        indent = indent_match.group(1) if indent_match else "            "
        label_attr = "arial-label" if "arial-label" in block else "aria-label"
        added += 1
        return block + "\n" + x_social_link(indent, label_attr)

    updated = LINKEDIN_SOCIAL.sub(linkedin_social_sub, text)
    return updated, added


def patch_html(text: str) -> tuple[str, dict[str, int]]:
    counts = {"linkedin": 0, "instagram": 0, "removed": 0, "x_added": 0}

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

    updated = REMOVE_X_SOCIAL.sub("", updated)
    updated, x_added = add_x_social_links(updated)
    counts["x_added"] = x_added

    # Ensure external social links open safely.
    updated = updated.replace(
        f'href="{LINKEDIN}" target="_blank" class=',
        f'href="{LINKEDIN}" target="_blank" rel="noopener noreferrer" class=',
    )
    updated = updated.replace(
        f'href="{INSTAGRAM}" target="_blank" class=',
        f'href="{INSTAGRAM}" target="_blank" rel="noopener noreferrer" class=',
    )
    updated = updated.replace(
        f'href="{X_PROFILE}" target="_blank" class=',
        f'href="{X_PROFILE}" target="_blank" rel="noopener noreferrer" class=',
    )
    updated = re.sub(
        r'<meta\s+name="twitter:site"\s+content="@NesmaPartners"\s*/?>',
        '<meta name="twitter:site" content="@Alruwaisco">',
        updated,
        flags=re.IGNORECASE,
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
    totals = {"files": 0, "linkedin": 0, "instagram": 0, "removed": 0, "x_added": 0}
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
            totals["x_added"] += counts["x_added"]

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
    print(f"x profile links added: {totals['x_added']}")
    print(f"files still mentioning old Nesma social URLs: {remaining}")


if __name__ == "__main__":
    main()
