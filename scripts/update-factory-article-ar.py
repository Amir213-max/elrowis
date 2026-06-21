#!/usr/bin/env python3
"""Update AR article: Al Asr Industrial Factory joins Alruwais."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

OLD_TITLES = [
    "تكريم الرويس لدورها في دعم المبادرات الإنسانية والمجتمعية",
    "تكريم نسما وشركاهم لدورها في دعم المبادرات الإنسانية والمجتمعية",
]

NEW_TITLE = (
    "مصنع العصر الصناعي ينضم إلى شركة الرويس: "
    "حلول متكاملة لواجهات الزجاج والألومنيوم والأعمال الخشبية في السعودية"
)
PAGE_TITLE = f"{NEW_TITLE} - الرويس"

ARTICLE = (
    ROOT
    / "ar"
    / "article"
    / "recognized-for-supporting-humanitarian-and-community-impact-initiatives.html"
)

ARTICLE_BODY = """<p>تُعلن شركة الرويس عن انضمام مصنع العصر الصناعي إلى مجموعة شركاتها، في خطوة استراتيجية تُعزز قدراتها في تصنيع وتركيب الواجهات الزجاجية، منتجات الألومنيوم، والأعمال الخشبية لمشاريع التشطيبات والبناء في المملكة العربية السعودية.</p><p><strong>عن مصنع العصر الصناعي:</strong></p><p>تأسّس مصنع العصر الصناعي عام 2026 ليكون منشأةً صناعية متخصصة في تصنيع الحلول المعمارية والتصميمية عالية الجودة. يعمل المصنع على ثلاثة محاور إنتاجية رئيسية تخدم القطاع الحكومي والخاص على حدٍّ سواء.</p><p><strong>واجهات زجاجية:</strong></p><p>تصنيع وتركيب واجهات كرتن وول، واجهات هيكلية، وزجاج سيكوريت مقسى للمباني التجارية والحكومية.</p><p><strong>أعمال خشبية وأثاث:</strong></p><p>ديكور خشبي، أثاث مخصص، تكيسات خشبية، وتشطيبات داخلية للمكاتب والمشاريع التجارية.</p><p><strong>منتجات ألومنيوم:</strong></p><p>قطاعات ألومنيوم، واجهات كلادينج، ديكورات وأنظمة ألومنيوم بعزل حراري للمشاريع السكنية والتجارية.</p><p><strong>مصنع متكامل من التصنيع إلى التركيب:</strong></p><p>يمتلك مصنع العصر الصناعي خطوط إنتاج متطورة تغطي جميع مراحل التصنيع: من قص وتشكيل قطاعات الألومنيوم، إلى تصنيع الواجهات الزجاجية بمواصفات الكود السعودي، وصولاً إلى تنفيذ الأعمال الخشبية والتشطيبات الداخلية. هذا التكامل الرأسي يُمكّن شركة الرويس من تقديم حلول «من التصنيع إلى التركيب» لعملائها في مشاريع المقاولات وإدارة المرافق — بجودة أعلى وتكلفة توريد أقل وسرعة في تسليم المشاريع.</p><p><strong>خدمة مشاريع القطاع الحكومي والخاص:</strong></p><p>يخدم المصنع طيفاً واسعاً من المشاريع في المملكة العربية السعودية، تشمل:</p><ul><li>مباني إدارية وتجارية</li><li>وزارات ومدارس ومستشفيات</li><li>فلل ومجمعات سكنية</li><li>مطاعم وكافيات ومحلات</li><li>فنادق ومنتجعات</li><li>مشاريع إدارة المرافق</li></ul><p><strong>ما الذي يعنيه هذا الانضمام لعملاء شركة الرويس؟</strong></p><p>بانضمام مصنع العصر الصناعي، تصبح شركة الرويس قادرة على تنفيذ أعمال الواجهات الزجاجية والكلادينج والتشطيبات الخشبية ضمن منظومتها التشغيلية المتكاملة — دون الحاجة إلى مقاولي الباطن الخارجيين. هذا يعني لعملاء الشركة: جودة موحّدة، إشراف مباشر على التنفيذ، والتزام أقوى بمواعيد التسليم في مشاريع المقاولات والتشطيبات الكبرى بالمملكة العربية السعودية.</p>"""

META_DESC = (
    "تُعلن شركة الرويس عن انضمام مصنع العصر الصناعي إلى مجموعتها، "
    "لتعزيز حلول الواجهات الزجاجية والألومنيوم والأعمال الخشبية في السعودية."
)

OLD_ARIA = "Recognized for Supporting Humanitarian and Community Impact Initiatives"

LISTING_FILES = [
    ROOT / "ar" / "news.html",
    ROOT / "ar" / "news2679.html",
    ROOT / "ar" / "media-room.html",
]


def update_article() -> None:
    html = ARTICLE.read_text(encoding="utf-8")

    for old in OLD_TITLES:
        html = html.replace(f"<title>{old} - الرويس</title>", f"<title>{PAGE_TITLE}</title>")
        html = html.replace(
            f'<meta property="og:title" content="{old} - الرويس">',
            f'<meta property="og:title" content="{PAGE_TITLE}">',
        )
        html = html.replace(
            f'<meta name="twitter:title" content="{old} - الرويس">',
            f'<meta name="twitter:title" content="{PAGE_TITLE}">',
        )
        html = html.replace(f'"name":"{old} - الرويس"', f'"name":"{PAGE_TITLE}"')
        html = html.replace(f'<h2 class="_eleY">{old}</h2>', f'<h2 class="_eleY">{NEW_TITLE}</h2>')

    html = re.sub(
        r'(<meta name="description" content=")[^"]+(")',
        rf"\1{META_DESC}\2",
        html,
        count=1,
    )
    html = re.sub(
        r'(<meta property="og:description" content=")[^"]+(")',
        rf"\1{META_DESC}\2",
        html,
        count=1,
    )
    html = re.sub(
        r'(<meta name="twitter:description" content=")[^"]+(")',
        rf"\1{META_DESC}\2",
        html,
        count=1,
    )

    html = re.sub(
        r'(<div class="article_txt f f-c _eleWrap">).*?(</div>)',
        rf"\1\n                        {ARTICLE_BODY}\n                    \2",
        html,
        count=1,
        flags=re.DOTALL,
    )

    share_text = "Al+Asr+Industrial+Factory+joins+Alruwais"
    html = html.replace(
        "text=Recognized+for+Supporting+Humanitarian+and+Community+Impact+Initiatives",
        f"text={share_text}",
    )
    html = html.replace(
        "text=Recognized+for+Supporting+Humanitarian+and+Community+Impact+Initiatives+",
        f"text={share_text}+",
    )

    ARTICLE.write_text(html, encoding="utf-8")


def update_listings() -> None:
    for path in LISTING_FILES:
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        changed = False
        for old in OLD_TITLES:
            if old in text:
                text = text.replace(old, NEW_TITLE)
                changed = True
        if OLD_ARIA in text:
            text = text.replace(OLD_ARIA, NEW_TITLE)
            changed = True
        if changed:
            path.write_text(text, encoding="utf-8")


def main() -> None:
    update_article()
    update_listings()
    print("OK")


if __name__ == "__main__":
    main()
