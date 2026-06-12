#!/usr/bin/env python3
"""Replace all old Nesma branding in social meta, OG image, and UI labels."""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OG_IMAGE = "images/og-alruwais.png"
DESC_EN = (
    "Alruwais is committed to shaping a better future through innovative, "
    "sustainable progress for the communities we serve."
)
DESC_AR = (
    "الرويس ملتزمة ببناء مستقبل أفضل من خلال التقدم المبتكر والمستدام "
    "للمجتمعات التي نخدمها."
)
TAGLINE_EN = "Together, We Build Excellence"
TAGLINE_AR = "معاً نبني التميز"


def depth_prefix(path: Path) -> str:
    rel = path.relative_to(ROOT)
    depth = len(rel.parts) - 1
    return "../" * depth if depth else "./"


def is_arabic_page(html: str, path: Path) -> bool:
    if "/ar/" in str(path).replace("\\", "/") or path.name.startswith("ar"):
        return True
    head = html[:2500]
    return 'lang="ar"' in head or 'dir="rtl"' in head


def patch_file(path: Path) -> str:
    html = path.read_text(encoding="utf-8")
    base = depth_prefix(path)
    is_ar = is_arabic_page(html, path)
    brand = "الرويس" if is_ar else "Alruwais"
    tagline = TAGLINE_AR if is_ar else TAGLINE_EN
    desc = DESC_AR if is_ar else DESC_EN
    og_url = f"{base}{OG_IMAGE}"

    # OG / Twitter image
    html = re.sub(
        r'<meta\s+property="og:image"\s+content="[^"]*"\s*/?>',
        f'<meta property="og:image" content="{og_url}">',
        html,
        flags=re.IGNORECASE,
    )
    if 'name="twitter:image"' not in html:
        html = re.sub(
            r'(<meta\s+property="og:image"\s+content="[^"]*"\s*/?>)',
            r'\1\n    <meta name="twitter:image" content="' + og_url + '">',
            html,
            count=1,
            flags=re.IGNORECASE,
        )
    else:
        html = re.sub(
            r'<meta\s+name="twitter:image"\s+content="[^"]*"\s*/?>',
            f'<meta name="twitter:image" content="{og_url}">',
            html,
            flags=re.IGNORECASE,
        )

    # Descriptions (head section)
    head_limit = html.find("</head>")
    if head_limit == -1:
        head_limit = len(html)
    head = html[:head_limit]
    tail = html[head_limit:]

    head = re.sub(
        r'(<meta\s+name="description"\s+content=")[^"]*(")',
        rf"\1{desc}\2",
        head,
        flags=re.IGNORECASE,
    )
    head = re.sub(
        r'(<meta\s+property="og:description"\s+content=")[^"]*(")',
        rf"\1{desc}\2",
        head,
        flags=re.IGNORECASE,
    )
    head = re.sub(
        r'(<meta\s+name="twitter:description"\s+content=")[^"]*(")',
        rf"\1{desc}\2",
        head,
        flags=re.IGNORECASE,
    )

    # Fix duplicate / broken titles in head
    def fix_title_content(content: str, page_title: str | None) -> str:
        content = re.sub(
            r"Nesma\s*(?:&amp;|&)\s*Partners",
            brand,
            content,
            flags=re.IGNORECASE,
        )
        content = re.sub(
            r"نسما\s*(?:&|و)\s*شرك(?:اهم|ائها|ائه)",
            brand,
            content,
            flags=re.IGNORECASE,
        )
        if content.strip() in {f"{brand} - {brand}", brand, f"Alruwais - Alruwais"}:
            if page_title and page_title != brand:
                return f"{page_title} - {brand}"
            return f"{brand} - {tagline}"
        if re.fullmatch(rf"{re.escape(brand)}\s*-\s*{re.escape(tagline)}", content.strip()):
            return content
        return content

    title_match = re.search(r"<title>([^<]*)</title>", head, re.IGNORECASE)
    page_title = title_match.group(1).strip() if title_match else None
    if page_title:
        page_title = re.sub(
            r"\s*-\s*(?:نسما\s*(?:&|و)\s*شرك(?:اهم|ائها|ائه)|Nesma\s*(?:&amp;|&)\s*Partners|Alruwais|الرويس)\s*$",
            "",
            page_title,
            flags=re.IGNORECASE,
        ).strip()
        if page_title in {brand, "Alruwais", "الرويس", ""}:
            new_title = f"{brand} - {tagline}"
        else:
            new_title = f"{page_title} - {brand}"
        head = re.sub(
            r"<title>[^<]*</title>",
            f"<title>{new_title}</title>",
            head,
            count=1,
            flags=re.IGNORECASE,
        )

    def meta_title_sub(m):
        attr, content = m.group(1), m.group(2)
        return f'<meta {attr} content="{fix_title_content(content, page_title)}">'

    head = re.sub(
        r'<meta\s+(property="og:title"|name="twitter:title")\s+content="([^"]*)"\s*/?>',
        meta_title_sub,
        head,
        flags=re.IGNORECASE,
    )

    html = head + tail

    # Normalize JSON-LD in full file
    def json_sub(m):
        block = m.group(0)
        block = re.sub(r"Nesma\s*(?:&amp;|&)\s*Partners", brand if not is_ar else "Alruwais", block, flags=re.I)
        block = re.sub(r"نسما\s*(?:&|و)\s*شرك(?:اهم|ائها|ائه)", brand, block, flags=re.I)
        block = re.sub(
            r'"description"\s*:\s*"[^"]*"',
            f'"description": "{desc}"',
            block,
            count=1,
        )
        block = re.sub(
            r'"name"\s*:\s*"Alruwais - Alruwais"',
            f'"name": "{brand} - {tagline}"',
            block,
        )
        if is_ar:
            block = re.sub(
                r'"name"\s*:\s*"Alruwais - الرويس"',
                f'"name": "{brand} - {tagline}"',
                block,
            )
        return block

    html = re.sub(
        r'<script\s+type="application/ld\+json">.*?</script>',
        json_sub,
        html,
        flags=re.DOTALL | re.IGNORECASE,
    )

    # Remove duplicate meta block inserted after brand-head.js (keep first canonical set)
    html = re.sub(
        r'(<script\s+src="[^"]*brand-head\.js"></script>\s*)'
        r'<meta\s+name="description"[^>]*>\s*'
        r'<meta\s+property="og:title"[^>]*>\s*'
        r'<meta\s+property="og:description"[^>]*>\s*'
        r'(?:<meta\s+name="twitter:title"[^>]*>\s*)?'
        r'<meta\s+name="twitter:description"[^>]*>\s*',
        r'\1',
        html,
        count=1,
        flags=re.IGNORECASE,
    )

    # Fix mixed-language homepage og titles on AR pages
    if is_ar:
        html = re.sub(
            r'<meta\s+property="og:title"\s+content="Alruwais - الرويس"\s*/?>',
            f'<meta property="og:title" content="{brand} - {tagline}">',
            html,
            flags=re.IGNORECASE,
        )
        html = re.sub(
            r'<meta\s+name="twitter:title"\s+content="Alruwais - الرويس"\s*/?>',
            f'<meta name="twitter:title" content="{brand} - {tagline}">',
            html,
            flags=re.IGNORECASE,
        )

    # UI / accessibility labels
    html = re.sub(
        r'aria-label="Nesma\s*&\s*Partners"',
        f'aria-label="{brand}"',
        html,
        flags=re.IGNORECASE,
    )
    html = re.sub(
        r"Copyright\s+2025\s+Nesma\s*&amp;\s*Partners\.\s*All Rights Reserved\.",
        "Copyright 2025 Alruwais. All Rights Reserved.",
        html,
        flags=re.IGNORECASE,
    )
    html = re.sub(
        r"حقوق النشر\s+2025\s+نسما\s*و\s*شركاهم\.\s*جميع الحقوق محفوظة\.",
        "حقوق النشر 2025 الرويس. جميع الحقوق محفوظة.",
        html,
    )
    html = re.sub(
        r'<meta\s+name="theme-color"\s+content="#FFFFFF"\s*/?>',
        '<meta name="theme-color" content="#003d53">',
        html,
        flags=re.IGNORECASE,
    )

    return html


def main():
    changed = 0
    for path in ROOT.rglob("*.html"):
        if "scripts" in path.parts:
            continue
        original = path.read_text(encoding="utf-8")
        updated = patch_file(path)
        if updated != original:
            path.write_text(updated, encoding="utf-8")
            changed += 1
    print(f"Updated {changed} HTML files")


if __name__ == "__main__":
    main()
