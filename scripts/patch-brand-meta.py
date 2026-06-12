#!/usr/bin/env python3
"""Patch HTML head: brand titles, favicon, and early brand-head.js loader."""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BRAND_AR = "الرويس"
BRAND_EN = "Alruwais"
FAVICON = "favicon-alruwais-32x32.png?v=1"
BRAND_SCRIPT = '<script src="{base}brand-head.js"></script>'

RE_TITLE_AR = re.compile(
    r"نسما\s*(?:&|و)\s*شرك(?:اهم|ائها|ائه)", re.IGNORECASE
)
RE_TITLE_EN = re.compile(
    r"Nesma\s*(?:&amp;|&)\s*Partners", re.IGNORECASE
)
RE_DEFAULT_OG = re.compile(
    r"Nesma\s*(?:&amp;|&)\s*Partners\s*-\s*Together,\s*We Build Excellence",
    re.IGNORECASE,
)


def depth_prefix(path: Path) -> str:
    rel = path.relative_to(ROOT)
    depth = len(rel.parts) - 1
    return "../" * depth if depth else "./"


def replace_brand_in_text(text: str, is_ar: bool) -> str:
    brand = BRAND_AR if is_ar else BRAND_EN
    tagline = "معاً نبني التميز" if is_ar else "Together, We Build Excellence"
    text = RE_DEFAULT_OG.sub(f"{brand} - {tagline}", text)
    text = RE_TITLE_AR.sub(BRAND_AR, text)
    text = RE_TITLE_EN.sub(BRAND_EN, text)
    return text


def patch_head(html: str, path: Path) -> str:
    is_ar = "/ar/" in str(path).replace("\\", "/") or path.name.startswith("ar")
    lang_attr = 'lang="ar"' in html[:2000] or 'dir="rtl"' in html[:2000]
    is_ar = is_ar or lang_attr

    base = depth_prefix(path)

    # favicon links -> new file with cache buster
    html = re.sub(
        r'<link\s+rel="icon"\s+href="[^"]*favicon[^"]*"\s*/?>',
        f'<link rel="icon" type="image/png" href="{base}images/{FAVICON}">',
        html,
        flags=re.IGNORECASE,
    )

    # title tag
    def _title_sub(m):
        return "<title>" + replace_brand_in_text(m.group(1), is_ar) + "</title>"

    html = re.sub(r"<title>([^<]*)</title>", _title_sub, html, count=1, flags=re.IGNORECASE)

    # og/twitter title metas in head only (first 8000 chars)
    head = html[:8000]
    tail = html[8000:]

    def _meta_sub(m):
        attr, content = m.group(1), m.group(2)
        return f'<meta {attr} content="{replace_brand_in_text(content, is_ar)}">'

    head = re.sub(
        r'<meta\s+(property="og:title"|name="twitter:title")\s+content="([^"]*)"\s*/?>',
        _meta_sub,
        head,
        flags=re.IGNORECASE,
    )

    # ld+json name in head
    def _json_sub(m):
        return replace_brand_in_text(m.group(0), is_ar)

    head = re.sub(
        r'<script\s+type="application/ld\+json">.*?</script>',
        _json_sub,
        head,
        count=1,
        flags=re.DOTALL | re.IGNORECASE,
    )

    html = head + tail

    # inject brand-head.js right after <title>...</title> if missing
    if "brand-head.js" not in html:
        script_tag = BRAND_SCRIPT.format(base=base)
        html = re.sub(
            r"(</title>)",
            r"\1\n    " + script_tag,
            html,
            count=1,
            flags=re.IGNORECASE,
        )

    return html


def main():
    fav_src = ROOT / "images" / "favicon-32x32.png"
    fav_dst = ROOT / "images" / "favicon-alruwais-32x32.png"
    if fav_src.exists():
        fav_dst.write_bytes(fav_src.read_bytes())

    count = 0
    for path in ROOT.rglob("*.html"):
        if "scripts" in path.parts:
            continue
        original = path.read_text(encoding="utf-8")
        updated = patch_head(original, path)
        if updated != original:
            path.write_text(updated, encoding="utf-8")
            count += 1
    print(f"Patched {count} HTML files")


if __name__ == "__main__":
    main()
