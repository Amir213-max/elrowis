#!/usr/bin/env python3
"""Update AR careers page: new content, remove related news, rename page."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

PAGE = ROOT / "ar" / "careers.html"
PAGE_NAME = "الوظائف والتدريب المهني"
PAGE_TITLE = f"{PAGE_NAME} - الرويس"
OLD_NAV = "الوظائف والثقافة المؤسسية"

META_DESC = (
    "نوفر في الرويس بيئة عمل متكاملة تعزز الإبداع وتدعم التطور المهني "
    "والتدريب، مع قيم داخلية قائمة على التعاون والسلامة والتميز والتنوع."
)

VALUES = [
    (
        "../storage/value-icons/qQ7BqPY2ts9a2FmcOXdxz03MIO4CNMPk9GKYFgyY.png",
        "التعاون",
        "نبني علاقات قوية قائمة على الثقة والعمل الجماعي لتحقيق النجاح المشترك.",
    ),
    (
        "../storage/value-icons/AmJv6ReuhIGmbDksUJyRoCNrN4bKTZG1BAXJMRyD.png",
        "السلامة",
        "نضع صحة وسلامة موظفينا وشركائنا في مقدمة أولوياتنا، ونعمل وفق أعلى معايير السلامة المهنية.",
    ),
    (
        "../storage/value-icons/Q15dlCaxQg5hVDyDBRBoGjIo68kkvmKrLmCBFaUh.png",
        "التميز",
        "نسعى إلى تحقيق أعلى معايير الجودة والاحترافية في جميع أعمالنا، ونلتزم بتقديم نتائج تتجاوز التوقعات.",
    ),
    (
        "../storage/value-icons/uppjkCKzHSv6yHBrfCk1ws9kOSBU3dBQTR3uouid.png",
        "التنوع",
        "نحتضن التنوع باعتباره مصدرًا للقوة والابتكار، ونوفر بيئة عمل شاملة تتيح للجميع فرصًا متساوية للمساهمة والتطور والنجاح.",
    ),
]


def value_col(icon: str, title: str, text: str) -> str:
    return f"""                <!-- Col Start -->
                <div class="v_col f f-c _eleY">
                    <img src="{icon}" style="width: 60px; height: 60px;" width="60" height="60" />
                    <div class="v_col_content f f-c">
                        <h4>{title}</h4>
                        <p class="gray_color">{text}</p>
                    </div>
                </div>
                <!-- Col End -->"""


def update_careers_page() -> None:
    html = PAGE.read_text(encoding="utf-8")

    html = html.replace("<title>Careers - الرويس</title>", f"<title>{PAGE_TITLE}</title>")
    html = html.replace('"name":"Careers - الرويس"', f'"name":"{PAGE_TITLE}"')
    html = re.sub(
        r'(<meta name="description" content=")[^"]+(")',
        rf"\1{META_DESC}\2",
        html,
        count=1,
    )

    html = html.replace(
        f'<p class="gray_color _eleY">{OLD_NAV}</p>',
        f'<p class="gray_color _eleY">{PAGE_NAME}</p>',
    )

    html = re.sub(
        r'(<h1 class="_eleY">).*?(</h1>)',
        r"\1معًا نرسخ مستقبلًا أفضل\2",
        html,
        count=1,
        flags=re.DOTALL,
    )

    html = re.sub(
        r'(<!--\[if BLOCK\]><!\[endif\]-->\s*)<p class="_eleY">انضم إلينا.*?</p>',
        r"\1<p class=\"_eleY\">نؤمن بأن نجاح مشاريعنا يبدأ من نجاح كوادرنا. لذلك نوفر بيئة عمل متكاملة تعزز الإبداع، وتدعم التطور المهني، وتفتح آفاقًا واسعة للنمو والتميز.</p>",
        html,
        count=1,
        flags=re.DOTALL,
    )

    # Remove hero apply button
    html = re.sub(
        r'\s*<!--\[if BLOCK\]><!\[endif\]-->\s*<a\s+href="https://careers\.nesmapartners\.com/".*?</a>\s*<!--\[if ENDBLOCK\]><!\[endif\]-->\s*</div>\s*</div>\s*</section>\s*<!-- Hero End -->',
        "\n        </div>\n    </div>\n</section>\n<!-- Hero End -->",
        html,
        count=1,
        flags=re.DOTALL,
    )

    values_html = "\n".join(value_col(*v) for v in VALUES)
    html = re.sub(
        r'(<div class="v_wrap f _eleWrap">\s*<!--\[if BLOCK\]><!\[endif\]-->).*?(<!--\[if ENDBLOCK\]><!\[endif\]-->\s*</div>)',
        rf"\1\n{values_html}\n                \2",
        html,
        count=1,
        flags=re.DOTALL,
    )

    html = re.sub(
        r'(<section id="training-career-development">.*?<p class="_eleY">).*?(</p>)',
        r"\1نعمل على تطوير قدرات كوادرنا من خلال برامج تدريبية متخصصة تساهم في صقل المهارات، وتعزيز الخبرات العملية، وإعداد كوادر مؤهلة قادرة على تحقيق التميز والمساهمة في نجاح مشاريعنا.\2",
        html,
        count=1,
        flags=re.DOTALL,
    )

    # Remove training section CTA button
    html = re.sub(
        r'\s*<!--\[if BLOCK\]><!\[endif\]-->\s*<a\s+href="javascript:void\(0\);"\s+data-scroll="internship-request".*?</a>\s*<!--\[if ENDBLOCK\]><!\[endif\]-->\s*</div>\s*</div>\s*</section>\s*<!-- Governance End -->',
        "\n        </div>\n\n    </div>\n\n</section>\n<!-- Governance End -->",
        html,
        count=1,
        flags=re.DOTALL,
    )

    html = html.replace(
        '<h2 class="_eleY">فرص العمل</h2>',
        '<h2 class="_eleY">ابدأ مسيرتك المهنية مع الرويس</h2>',
    )
    html = re.sub(
        r'(<div class="description text-center _eleY">\s*<p>).*?(</p><p></p>\s*</div>)',
        r"\1كن جزءًا من فريق يسعى للتميز ويشارك في تنفيذ مشاريع رائدة في قطاع التشييد والبناء. نوفر بيئة عمل محفزة تدعم التطور المهني، وتشجع الابتكار، وتؤمن بقيمة التنوع وتكافؤ الفرص للجميع.\2",
        html,
        count=1,
        flags=re.DOTALL,
    )

    html = html.replace("<p>معًا نبني التميز​​!</p>", "")

    # Remove related news section
    html = re.sub(
        r'\s*<!-- News Start -->.*?<!-- News End -->\s*',
        "\n        ",
        html,
        count=1,
        flags=re.DOTALL,
    )

    html = html.replace(OLD_NAV, PAGE_NAME)
    html = html.replace("فرص العمل", "ابدأ مسيرتك المهنية")

    PAGE.write_text(html, encoding="utf-8")


def sync_nav_label() -> int:
    count = 0
    for path in list(ROOT.glob("ar/**/*.html")) + [ROOT / "ar.html", ROOT / "index.html"]:
        text = path.read_text(encoding="utf-8")
        if OLD_NAV not in text:
            continue
        path.write_text(text.replace(OLD_NAV, PAGE_NAME), encoding="utf-8")
        count += 1
    return count


def main() -> None:
    update_careers_page()
    n = sync_nav_label()
    print(f"OK — nav updated in {n} files")


if __name__ == "__main__":
    main()
