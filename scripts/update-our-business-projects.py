#!/usr/bin/env python3
"""Update project titles in our-business.html (names only, keep images)."""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HTML = ROOT / "ar" / "our-business.html"

SECTOR_PROJECTS = {
    "مشاريع قطاع التشييد والبناء": [
        "تطوير مرافق وخدمات الاستاد الرياضي بالمدينة الرياضية بالمجمعة",
        "ترميم مواقع متفرقة برئاسة الحرس الملكي بالمنطقة الوسطى",
        "ترميم مبنى الركاب والجوازات بمنفذ الرقعي",
        "ترميم وتأهيل مبني 11 ومبني 12 في الهيئة العامة للتطوير الدفاعي",
    ],
    "مشاريع قطاع التشغيل": [
        "عقد مناولة منفذ البطحاء معدات وفنيين",
        "عقد مناولة منفذ جسر الملك فهد معدات وفنيين",
        "تشغيل ونظافة دورات المياه لحدائق ومنتزهات متفرقة بمدينة الرياض",
        "عقد مناولة منافذ المنطقة الشرقية معدات وفنيين",
    ],
    "مشاريع قطاع البنية التحتية": [
        "تمديد مواسير لتغذية الخزانات الأرضية بالمياه من مصدر المياه الرئيسي لمبنى إدارة المحروقات بمحطة الأمن العام الثانية بشرق الرياض",
        "مشروع إضافات وتحسينات للأنظمة الكهربائية بمباني وزارة المالية بمخرج 9",
        "مشروع استبدال البنية التحتية لشبكة المياه الرئيسية لإسكان القوات بالمرحلة الثالثة بمدينة الامير نايف الامنية (يشترط تصنيف)",
        "تنفيذ أعمال إنشائية لخطوط مياه تغذية خزان البلدية وخزان الري بمستشفى الأمير محمد بن عبد العزيز بالمدينة المنورة",
    ],
}

PROJECT_BLOCK = re.compile(
    r"(<!-- Project Start -->.*?<!-- Project End -->)",
    re.DOTALL,
)
TITLE_RE = re.compile(r"(<div class=\"pro_title\">\s*<h4>)(.*?)(</h4>)", re.DOTALL)


def update_sector_slider(slider_html: str, titles: list[str]) -> str:
    blocks = PROJECT_BLOCK.findall(slider_html)
    if not blocks:
        return slider_html

    updated_blocks = []
    for i, title in enumerate(titles):
        if i >= len(blocks):
            break
        block = blocks[i]
        block = TITLE_RE.sub(rf"\1{title}\3", block, count=1)
        updated_blocks.append(block)

    prefix = slider_html.split("<!-- Project Start -->", 1)[0]
    suffix_marker = "<!--[if ENDBLOCK]><![endif]-->"
    suffix = slider_html.rsplit(suffix_marker, 1)[-1]

    inner = "\n                                            ".join(updated_blocks)
    return f"{prefix}{inner}\n                    {suffix_marker}{suffix}"


def main() -> None:
    html = HTML.read_text(encoding="utf-8")

    for heading, titles in SECTOR_PROJECTS.items():
        pattern = re.compile(
            rf"(<h2>{re.escape(heading)}</h2>.*?<div class=\"projects_slider slider_parent _eleWrap\">)(.*?)(</div>\s*\n\s*</div>\s*\n\s*<!-- Body End -->)",
            re.DOTALL,
        )
        match = pattern.search(html)
        if not match:
            raise SystemExit(f"Section not found: {heading}")

        new_slider = update_sector_slider(match.group(2), titles)
        html = html[: match.start(2)] + new_slider + html[match.end(2) :]

    HTML.write_text(html, encoding="utf-8")
    print(f"Updated {HTML.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
