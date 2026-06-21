#!/usr/bin/env python3
"""Update AR article: best construction companies in Saudi Arabia."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

OLD_TITLE = "جولة قيادية تستعرض التقدم المتسارع في مشروع إكسبو الرياض 2030"
NEW_TITLE = "أفضل شركات المقاولات في المملكة العربية السعودية"
PAGE_TITLE = f"{NEW_TITLE} - الرويس"

ARTICLE = ROOT / "ar" / "article" / "leadership-walkthrough-highlights-rapid-progress-at-expo-2030-riyadh.html"

ARTICLE_BODY = """<p>تعد الرويس من أفضل شركات المقاولات والرائدة في مختلف المجالات المتعلقة بالمقاولات والترميم والصيانة، وصولاً إلى التشغيل وإدارة المرافق.</p><p>تم تأسيس شركة الرويس للمقاولات في عام 2015 برؤية واضحة وأن تكون من ضمن الشركات الرائدة في مجال المقاولات العامة.</p><p>مع تحقيق الرؤية، استطاعت الرويس الحصول على مشاريع عملاقة وضخمة مع جهات حكومية كبيرة مثل أمانة منطقة الرياض، هيئة الزكاة والضريبة والجمارك، وزارة الرياضة وغيرها من الجهات الحكومية، فأصبحت الرويس شريكاً استراتيجياً موثوقاً للجهات الحكومية وأيضاً الخاصة.</p><p>مع حجم العمل وتنوع النشاطات، كان من النقاط المهمة الانتقال إلى مقر جديد يعكس حجم وهوية الرويس للظهور كما يجب كشركة من أفضل شركات المقاولات في الرياض.</p><p>تم الانتقال إلى مقر الشركة الجديد في الرياض، حي النخيل، شارع الثريا، لاستقبال عملائنا وموردينا.</p><p><strong>لماذا تعد الرويس من أفضل شركات المقاولات في الرياض؟</strong></p><p>ليس فقط السمعة والموثوقية من الجهات الحكومية الكبرى، وليس لوجود خبرة طويلة تمتد لأكثر من 15 عاماً في السوق المحلي وتنوع مشاريعنا وأعمالنا... ولكن لأننا نوفر للعميل تجربة استثنائية سواء في مواعيد التسليم والمتابعة والتحقق المستمر.</p><p><strong>الالتزام بالمعايير البيئية والاستدامة:</strong> نحرص على اتباع المعايير البيئية والاستدامة في جميع مشاريعنا، مما يساهم في حماية البيئة وتوفير مجتمعات مستدامة.</p><p><strong>الابتكار واستخدام التكنولوجيا:</strong> نستخدم أحدث التقنيات في جميع أعمالنا، مما يسهم في تحقيق الابتكار وتوفير بيئات معيشية وتجارية حديثة ومريحة.</p><p>بفضل هذه العوامل، نتميز كواحدة من أفضل شركات المقاولات في الرياض ونسعى دائماً لتقديم أفضل الخدمات والمشاريع لعملائنا الكرام.</p><p><strong>كيف يمكن للعملاء أن يحصلوا على استشارات حول مشاريعهم لدى شركة الرويس؟</strong></p><p>يمكن للعملاء الحصول على معلومات أو استشارات حول المشاريع العقارية في الرياض بسهولة عن طريق الخطوات التالية:</p><ul><li>زيارة الموقع الإلكتروني للرويس للحصول على معلومات شاملة حول مشاريعنا والخدمات التي نقدمها وطرق التواصل معنا: <a href="mailto:Info@Alruwais.com.sa">Info@Alruwais.com.sa</a></li><li>الاتصال بنا مباشرة على الرقم الموحد: <a href="tel:920012496">920012496</a> أو <a href="tel:+966571000074">966571000074</a></li><li>زيارتنا في مقرنا الجديد: الرياض — حي النخيل — شارع الثريا — المخطط 2732 البلوك 1 — وحدة رقم 0001</li></ul>"""

META_DESC = (
    "تعد الرويس من أفضل شركات المقاولات في المملكة العربية السعودية، "
    "برؤية راسخة منذ 2015 ومشاريع ضخمة مع جهات حكومية وخاصة."
)

LISTING_FILES = [
    ROOT / "ar" / "news.html",
    ROOT / "ar" / "news2679.html",
    ROOT / "ar" / "nesma-partners.html",
    ROOT / "ar" / "media-room.html",
    ROOT / "ar.html",
    ROOT / "index.html",
]


def update_article() -> None:
    html = ARTICLE.read_text(encoding="utf-8")

    html = html.replace(f"<title>{OLD_TITLE} - الرويس</title>", f"<title>{PAGE_TITLE}</title>")
    html = html.replace(
        f'<meta property="og:title" content="{OLD_TITLE} - الرويس">',
        f'<meta property="og:title" content="{PAGE_TITLE}">',
    )
    html = html.replace(
        f'<meta name="twitter:title" content="{OLD_TITLE} - الرويس">',
        f'<meta name="twitter:title" content="{PAGE_TITLE}">',
    )
    html = html.replace(
        f'"name":"{OLD_TITLE} - الرويس"',
        f'"name":"{PAGE_TITLE}"',
    )

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

    html = html.replace(f"<h2 class=\"_eleY\">{OLD_TITLE}</h2>", f"<h2 class=\"_eleY\">{NEW_TITLE}</h2>")

    html = re.sub(
        r'(<div class="article_txt f f-c _eleWrap">).*?(</div>)',
        rf"\1\n                        {ARTICLE_BODY}\n                    \2",
        html,
        count=1,
        flags=re.DOTALL,
    )

    share_text = "Best+construction+companies+in+Saudi+Arabia"
    html = html.replace(
        "text=Leadership+Walkthrough+Highlights+Rapid+Progress+at+Expo+2030+Riyadh",
        f"text={share_text}",
    )
    html = html.replace(
        "text=Leadership+Walkthrough+Highlights+Rapid+Progress+at+Expo+2030+Riyadh+",
        f"text={share_text}+",
    )

    ARTICLE.write_text(html, encoding="utf-8")


def update_listings() -> None:
    for path in LISTING_FILES:
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        if OLD_TITLE not in text:
            continue
        path.write_text(text.replace(OLD_TITLE, NEW_TITLE), encoding="utf-8")


def main() -> None:
    update_article()
    update_listings()
    print("OK")


if __name__ == "__main__":
    main()
