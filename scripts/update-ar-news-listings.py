#!/usr/bin/env python3
"""Keep only the 3 edited AR news cards and sync the netzero article listing title."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

OLD_NETZERO_TITLE = (
    "نت زيرو ونسما وشركاهم يحققان إنجاز العام الأول من مبادرة زراعة 40 ألف شجرة"
)
NEW_NETZERO_TITLE = (
    "كيف تختار شركة مقاولات موثوقة في السعودية؟ 7 معايير لا تتنازل عنها"
)
OLD_NETZERO_ARIA_EN = (
    "NetZero and Nesma &amp; Partners Mark First-Year Milestone of 40,000 Trees Initiative"
)

N_CARD_RE = re.compile(
    r"(\s*(?:<!--\[if BLOCK\][^\n]*-->\s*)?"
    r"<!-- Card Start -->[\s\S]*?class=\"card_set n_card[\s\S]*?<!-- Card End -->)",
    re.MULTILINE,
)

WARP_F_FW_RE = re.compile(
    r'(<div class="cards_warp f f-w _eleWrap">)([\s\S]*?)(<!--\[if ENDBLOCK\]><!\[endif\]-->\s*</div>)',
    re.MULTILINE,
)

SLIDER_WARP_RE = re.compile(
    r'(<div class="cards_warp slider_parent">)([\s\S]*?)(<!--\[if ENDBLOCK\]><!\[endif\]-->\s*</div>)',
    re.MULTILINE,
)


def update_netzero_titles(html: str) -> str:
    html = html.replace(OLD_NETZERO_TITLE, NEW_NETZERO_TITLE)
    html = html.replace(OLD_NETZERO_ARIA_EN, NEW_NETZERO_TITLE)
    return html


def trim_warp_inner(inner: str, limit: int = 3) -> str:
    cards = N_CARD_RE.findall(inner)
    if not cards or len(cards) <= limit:
        return inner

    header_match = re.match(r"(\s*<!--\[if BLOCK\][^\n]*-->\s*)", inner)
    header = header_match.group(1) if header_match else ""

    footer_match = re.search(r"(\s*<!--\[if ENDBLOCK\][^\n]*-->)", inner)
    footer = footer_match.group(1) if footer_match else ""

    return header + "".join(cards[:limit]) + footer


def trim_cards_warps(html: str, limit: int = 3) -> str:
    def repl(match: re.Match[str]) -> str:
        return match.group(1) + trim_warp_inner(match.group(2), limit) + match.group(3)

    return WARP_F_FW_RE.sub(repl, html)


def build_home_cards(prefix: str) -> str:
    article = f"{prefix}article"
    return f"""                <!--[if BLOCK]><![endif]-->                    <!-- Card Start -->
                    <a href="{article}/leadership-walkthrough-highlights-rapid-progress-at-expo-2030-riyadh.html" class="card_set n_card f f-c s-b corners" aria-label="أفضل شركات المقاولات في المملكة العربية السعودية">
                        <div class="n_content f f-c">
                            <h5>
                                <strong>أفضل شركات المقاولات في المملكة العربية السعودية</strong>
                            </h5>
                            <span class="n_subtitle gray_color"></span>
                        </div>
                        <div class="n_cover f a-e corners">
                            <!--[if BLOCK]><![endif]-->                                <i class="load_bg cover full_bg" data-src="storage/1000/vfUk2lWkPbSmv5qYbiapgnPwiETcRT-metaSU1HXzUzNjEuSlBH-.jpg"></i>
                            <!--[if ENDBLOCK]><![endif]-->                            <div class="n_cover_info f a-c s-b">
                                <strong class="label small">الثلاثاء, 19 مايو 2026</strong>
                            </div>
                        </div>
                    </a>
                    <!-- Card End -->
                                    <!-- Card Start -->
                    <a href="{article}/recognized-for-supporting-humanitarian-and-community-impact-initiatives.html" class="card_set n_card f f-c s-b corners" aria-label="مصنع العصر الصناعي ينضم إلى شركة الرويس: حلول متكاملة لواجهات الزجاج والألومنيوم والأعمال الخشبية في السعودية">
                        <div class="n_content f f-c">
                            <h5>
                                <strong>مصنع العصر الصناعي ينضم إلى شركة الرويس: حلول متكاملة لواجهات الزجاج والألومنيوم والأعمال الخشبية في السعودية</strong>
                            </h5>
                            <span class="n_subtitle gray_color"></span>
                        </div>
                        <div class="n_cover f a-e corners">
                            <!--[if BLOCK]><![endif]-->                                <i class="load_bg cover full_bg" data-src="storage/1011/T8BZskAR8ZKdrIgiEHIMGx8vqatFeY-metaV2hhdHNBcHAgSW1hZ2UgMjAyNi0wNS0xNCBhdCA1LjAzLjAwIFBNLmpwZWc%3d-.jpg"></i>
                            <!--[if ENDBLOCK]><![endif]-->                            <div class="n_cover_info f a-c s-b">
                                <strong class="label small">الأربعاء, 13 مايو 2026</strong>
                            </div>
                        </div>
                    </a>
                    <!-- Card End -->
                                    <!-- Card Start -->
                    <a href="{article}/netzero-and-nesma-partners-mark-first-year-milestone-of-40000-trees-initiative.html" class="card_set n_card f f-c s-b corners" aria-label="{NEW_NETZERO_TITLE}">
                        <div class="n_content f f-c">
                            <h5>
                                <strong>{NEW_NETZERO_TITLE}</strong>
                            </h5>
                            <span class="n_subtitle gray_color"></span>
                        </div>
                        <div class="n_cover f a-e corners">
                            <!--[if BLOCK]><![endif]-->                                <i class="load_bg cover full_bg" data-src="storage/1009/CwZR2RABRhaJZsyPLMK4F3c5gKYqOD-metaRFNDMDU5MTFfZnVsbHJlcy5qcGc%3d-.jpg"></i>
                            <!--[if ENDBLOCK]><![endif]-->                            <div class="n_cover_info f a-c s-b">
                                <strong class="label small">الخميس, 7 مايو 2026</strong>
                            </div>
                        </div>
                    </a>
                    <!-- Card End -->
                """


def build_nesma_cards() -> str:
    return build_home_cards("").replace(
        'data-src="storage/1011/',
        'data-src="../storage/1011/',
    )


def replace_slider_cards(html: str, cards_html: str) -> str:
    return SLIDER_WARP_RE.sub(
        r"\1\n" + cards_html + r"\n                \3",
        html,
        count=1,
    )


def cleanup_orphan_slider_tail(html: str) -> str:
    """Remove leftover card markup after a broken slider replace."""
    return re.sub(
        r"(<!--\[if ENDBLOCK\]><!\[endif\]-->\s*</div>\s*)"
        r"(?:\s*<div class=\"n_cover[\s\S]*?<!-- Card End -->[\s\S]*?"
        r"<!--\[if ENDBLOCK\]><!\[endif\]-->\s*</div>)",
        r"\1",
        html,
        count=1,
    )


def main() -> None:
    trim_paths = [
        ROOT / "ar" / "media-room.html",
        ROOT / "ar" / "news.html",
        ROOT / "ar" / "news2679.html",
    ]

    for path in trim_paths:
        html = update_netzero_titles(path.read_text(encoding="utf-8"))
        html = trim_cards_warps(html)
        path.write_text(html, encoding="utf-8")
        print(f"Trimmed: {path.relative_to(ROOT)}")

    for path in (ROOT / "ar.html", ROOT / "index.html"):
        html = path.read_text(encoding="utf-8")
        html = cleanup_orphan_slider_tail(html)
        html = replace_slider_cards(html, build_home_cards("ar/"))
        path.write_text(html, encoding="utf-8")
        print(f"Replaced slider: {path.relative_to(ROOT)}")

    nesma = ROOT / "ar" / "nesma-partners.html"
    html = cleanup_orphan_slider_tail(nesma.read_text(encoding="utf-8"))
    html = replace_slider_cards(html, build_nesma_cards())
    nesma.write_text(html, encoding="utf-8")
    print(f"Replaced slider: {nesma.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
