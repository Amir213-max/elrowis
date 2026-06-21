#!/usr/bin/env python3
"""Update media-room media kit section to company profile."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MEDIA_ROOM = ROOT / "ar" / "media-room.html"

OLD_LABEL = "حزمة الوسائط"
NEW_LABEL = "الملف التعريفى"
NEW_DESC = (
    "استكشف الملف التعريفي الخاص بشركة الرويس للمقاولات "
    "وتعرف على أحدث مشاريعها وأبرز خدماتها"
)
PDF_HREF = "company-profile.html"
BUTTON_LABEL = "الملف التعريفي"


def update_media_room() -> None:
    html = MEDIA_ROOM.read_text(encoding="utf-8")

    html = html.replace(
        f'<h2 class="_eleY">{OLD_LABEL} </h2>',
        f'<h2 class="_eleY">{NEW_LABEL}</h2>',
    )
    html = html.replace(
        "<p>استكشف حزمة الوسائط الشاملة الخاصة بنا، والتي تحتوي على موارد أساسية ومعلومات حول نسما وشركاهم، مخصصة للصحفيين ومتخصصي الإعلام.</p>",
        f"<p>{NEW_DESC}</p>",
    )
    html = html.replace(
        'href="../storage/files/QlPfTxTh405jLHtxdAugrVK8Z1N1DnGsxDWd4eqi.pdf"',
        f'href="{PDF_HREF}"',
    )
    html = html.replace('aria-label="حزمة الوسائط  2024 "', f'aria-label="{BUTTON_LABEL}"')
    html = html.replace(
        "<strong class=\"uppercase _txt words\">حزمة الوسائط  2024 </strong>",
        f'<strong class="uppercase _txt words">{BUTTON_LABEL}</strong>',
    )
    html = html.replace(OLD_LABEL, NEW_LABEL)

    MEDIA_ROOM.write_text(html, encoding="utf-8")


def sync_nav_label() -> int:
    count = 0
    for path in list(ROOT.glob("ar/**/*.html")) + [ROOT / "ar.html", ROOT / "index.html"]:
        text = path.read_text(encoding="utf-8")
        if OLD_LABEL not in text:
            continue
        path.write_text(text.replace(OLD_LABEL, NEW_LABEL), encoding="utf-8")
        count += 1
    return count


def main() -> None:
    update_media_room()
    n = sync_nav_label()
    print(f"OK — nav updated in {n} files")


if __name__ == "__main__":
    main()
