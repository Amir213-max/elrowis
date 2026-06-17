# -*- coding: utf-8 -*-
"""Update Arabic about-us page content for Al-Ruwais."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HTML = ROOT / "ar" / "about-us.html"

LEADERS = [
    (
        "team-1",
        "storage/915/88VRiAZnUlbRDwD3cfR1EzEnSVYBfa-metaQ2hhaXJtYW4tUmFtaWNvbS5qcGc=-.jpg",
        "رئيس مجلس الإدارة",
    ),
    (
        "team-2",
        "storage/917/UGAdML1Cy1XJdiehVQYw50Od2qEg6g-metaQ0VPLW5ld2NvbXAuanBn-.jpg",
        "الرئيس التنفيذي",
    ),
    (
        "team-3",
        "storage/593/vH9c99SCe9DqCzntymmmR9f3CfQSXx-metaSGF5dGhhbS5wbmc=-.png",
        "مدير إدارة المشاريع",
    ),
    (
        "team-4",
        "storage/919/iUh8gfS5Edr2af64b5XPGtX4dBG7X5-metaU2hhd2tpIEdob2xtaWVjb21wLmpwZw==-.jpg",
        "مدير عام الموارد البشرية",
    ),
    (
        "team-5",
        "storage/602/2dbUzTDddIKyRrI0fBEkN2Gmu22y9v-metaTWFyYy5wbmc=-.png",
        "المدير المالي",
    ),
]

SUBSIDIARIES = [
    (
        "partner-1",
        "images/about/subsidiary-rawad.png",
        "رواد الإنشاءات",
        "شركة تابعة لمجموعة الرويس متخصصة في الإنشاءات الحديثة ودعم تنفيذ المشاريع الإنشائية.",
    ),
    (
        "partner-2",
        "images/about/subsidiary-mazen.png",
        "مزن نجد",
        "الذراع التشغيلية لمجموعة الرويس في إدارة المرافق والتشغيل والصيانة.",
    ),
    (
        "partner-3",
        "images/about/subsidiary-asr.png",
        "العصر الصناعي",
        "مصنع صناعي يدعم الشركات والقطاع الحكومي في صناعات الألمنيوم والأخشاب.",
    ),
]

VALUES = [
    (
        "الجودة",
        "نلتزم بتقديم أعمال وخدمات تتوافق مع أعلى معايير الجودة، مع الحرص على الدقة في التنفيذ والتفاصيل التي تضمن رضا العملاء واستدامة النتائج.",
    ),
    (
        "الابتكار",
        "نسعى إلى تبني أحدث التقنيات والحلول الحديثة لتطوير أعمالنا، وتقديم خدمات تلبي متطلبات المستقبل وتواكب تطورات السوق.",
    ),
    (
        "الالتزام",
        "نؤمن بأن الالتزام هو أساس النجاح، لذلك نحرص على الوفاء بوعودنا وتنفيذ مشاريعنا وفق الجداول الزمنية والمعايير المتفق عليها.",
    ),
    (
        "الموثوقية",
        "نؤمن بأن الالتزام هو أساس النجاح، لذلك نحرص على الوفاء بوعودنا وتنفيذ مشاريعنا وفق الجداول الزمنية والمعايير المتفق عليها.",
    ),
    (
        "التأثير",
        "نسعى باستمرار إلى تجاوز التوقعات من خلال الأداء الاحترافي والتحسين المستمر، لنكون الخيار المفضل في جميع المجالات التي نعمل بها.",
    ),
]

TIMELINE = [
    (
        "2015",
        "تأسيس شركة الرويس",
        "تم تأسيس شركة الرويس للمقاولات العامة كمؤسسة ناشئة.",
    ),
    (
        "2019",
        "رواد الإنشائيات الحديثة",
        "تم تأسيس شركة رواد الإنشائيات الحديثة وضمها لمجموعة الرويس.",
    ),
    (
        "2022",
        "مزن نجد",
        "دخول شركة الرويس قطاع إدارة المرافق وتأسيس شركة مزن نجد وأصبحت اليد التشغيلية لمجموعة الرويس.",
    ),
    (
        "2026",
        "مصنع العصر الصناعي",
        "مصنع العصر الصناعي يضاف للمجموعة لدعم الشركات والقطاع الحكومي لصناعات الألمنيوم والأخشاب.",
    ),
]


def leader_sidebar(team_id: str, img: str, title: str) -> str:
    return f"""        <!-- Bar Start -->
        <div class="sidebar_set" data-id="{team_id}">
            <div class="tm_bar f f-c">
                <div class="team_cover _ele">
                    <img class="load_img" data-src="{img}" alt="{title}">
                </div>
                <div class="team_info f f-c _ele">
                    <p><strong>{title}</strong></p>
                </div>
            </div>
        </div>
        <!-- Bar End -->
"""


def leader_card(team_id: str, img: str, title: str, dist: str) -> str:
    return f"""                        <!-- Col Start -->
                            <div class="team_col_set slider_col">
                                <div class="team_col tab_col _x f a-e _eleX" data-id="{team_id}">
                                    <i class="cover load_bg full_bg" data-src="{img}"></i>
                                    <div class="team_info f f-c">
                                        <p><strong>{title}</strong></p>
                                    </div>
                                </div>
                            </div>
                        <!-- Col End -->
"""


def partner_sidebar(partner_id: str, img: str, name: str, desc: str) -> str:
    return f"""            <!-- Bar Start -->
            <div class="sidebar_set" data-id="{partner_id}">
                <div class="partner_bar f f-c">
                    <div class="panel_logo f a-c j-c corners _eleX">
                        <img class="load_img" data-src="{img}" align="Logo" alt="{name}">
                    </div>
                    <div class="team_bio f f-c">
                        <h4>{name}</h4>
                        <span class=" high _ele"><p>{desc}</p></span>
                    </div>
                </div>
            </div>
            <!-- Bar End -->
"""


def partner_logo(partner_id: str, img: str, name: str) -> str:
    return f"""                            <div class="panel_logo_set" data-id="{partner_id}">
                                <div class="panel_logo _x f a-c j-c corners">
                                    <img class="load_img" data-src="{img}" align="Logo" alt="{name}">
                                </div>
                            </div>
"""


def value_block(title: str, body: str) -> str:
    return f"""                        <!-- Q Start -->
                        <div class="faq_block pointer _eleY">
                            <div class="faq_head f a-c s-b">
                                <h4>{title}</h4>
                                <div class="faq_arrow f a-c j-c">
                                    <svg xmlns="http://www.w3.org/2000/svg" width="25" height="24" fill="none" viewBox="0 0 25 24">
                                        <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="m20.5 9-7.293 7.293a1 1 0 0 1-1.414 0L4.5 9"/>
                                    </svg>
                                </div>
                            </div>
                            <div class="faq_body f f-c a-s wide">
                                <p class="gray_color">{body}</p>
                            </div>
                        </div>
                        <!-- Q End -->
"""


def timeline_col(year: str, title: str, body: str) -> str:
    return f"""                                    <!-- Col Start -->
                                    <div class="timeline_col f f-c">
                                        <h1>{year}</h1>
                                        <div class="tl_content f f-c">
                                            <h5><strong>{title}</strong></h5>
                                            <p class="gray_color">{body}</p>
                                        </div>
                                    </div>
                                    <!-- Col End -->
"""


def replace_between(content: str, start_marker: str, end_marker: str, replacement: str) -> str:
    start = content.find(start_marker)
    end = content.find(end_marker, start)
    if start == -1 or end == -1:
        raise SystemExit(f"Markers not found: {start_marker!r} .. {end_marker!r}")
    return content[:start] + replacement + content[end:]


def main():
    content = HTML.read_text(encoding="utf-8")

    # Hero
    content = content.replace(
        '<h1 class="_eleY">معاً,<br />\nنبني التميز</h1>',
        '<h1 class="_eleY">قيم راسخة وإنجازات لا تُنسى</h1>',
    )
    content = content.replace(
        '<p class="_eleY">مجموعة نسما وشركاهم هي المزود الرائد لحلول المشاريع المتكاملة في المملكة العربية السعودية. وبفضل إرثها العريق في قطاع المقاولات، توسعت المجموعة محليًا من خلال خدماتها في المقاولات والخدمات الصناعية، وعالميًا عبر شركتها التابعة المملوكة بالكامل "كنت"، الرائدة في مجالات الهندسة وإدارة المشاريع.</p>',
        '<p class="_eleY">شركة الرويس هي المزود الرائد لحلول المشاريع المتكاملة في المملكة العربية السعودية. بفضل إرثنا العريق في قطاع المقاولات، نقدم خدمات شاملة تمتد من المقاولات العامة والمتخصصة، إلى التشغيل والصيانة وإدارة المرافق الحكومية والخاصة.<br><br>منذ تأسيسنا عام 2015، نمونا لنصبح شريكاً موثوقاً للجهات الحكومية الكبرى، بكوادر بشرية تتجاوز 2,000 متخصص يعملون بدقة عالية ووفق أرقى معايير الجودة والسلامة.</p>\n                <p class="_eleY">نبني اليوم لنصنع المستقبل</p>',
    )

    # Roots / timeline header
    content = content.replace("<h2>قصتنا</h2>", "<h2>جذورنا</h2>")
    content = re.sub(
        r'<h5 class="gray_color">ما بدأ في عام 1981.*?</h5>',
        '<h5 class="gray_color">منذ عام 2015، ونحن نُرسّخ يوماً بعد يوم أن الرويس ليست شركة مقاولات وحسب. في سوق متنامٍ ومتطور، نمونا لنصبح شريكاً استراتيجياً موثوقاً للجهات الحكومية والخاصة — نقدم حلولاً متكاملة تبدأ من التخطيط والتصميم، مروراً بالتنفيذ، وصولاً إلى التشغيل والصيانة وإدارة المرافق.<br><br>ما يميزنا ليس حجم ما بنيناه — بل عمق ما تركناه.</h5>',
        content,
        count=1,
        flags=re.DOTALL,
    )

    timeline_html = "\n".join(timeline_col(y, t, b) for y, t, b in TIMELINE)
    content = replace_between(
        content,
        '<div class="timeline_cols f a-c slider_parent"',
        "</div>\n\n                    </div>\n\n                </div>",
        '<div class="timeline_cols f a-c slider_parent"  data-flickity=\'{ "rightToLeft": true }\' >\n\n'
        + timeline_html
        + "\n                        ",
    )

    # Mission / vision
    content = content.replace(
        '<h5 class="gray_color _eleY">تنفيذ المشاريع بالشراكة مع عملائنا: بأمان، دون أي إصابات تؤدي إلى فقدان وقت العمل. بجودة، دون أي رفض للأعمال. وبسرعة، من خلال الالتزام الدائم بالمواعيد النهائية.</h5>',
        '<h5 class="gray_color _eleY">نؤمن بأن كل مشروع هو فرصة لصناعة أثر دائم. لذلك نسعى إلى تقديم حلول متكاملة تبدأ من الفكرة والتخطيط، وتمتد إلى التنفيذ والتشغيل، وفق أعلى معايير الجودة والسلامة والاستدامة، بما يلبي تطلعات عملائنا ويسهم في دعم مسيرة التنمية الوطنية.</h5>',
    )
    content = content.replace(
        '<h5 class="gray_color _eleY">أن نكون المزود الأول لحلول المشاريع المتكاملة في قطاعات الطاقة، والبنية التحتية، والمباني، محل الثقة في تحويل الرؤى الطموحة إلى واقع داخل المملكة العربية السعودية وخارجها.\n\n</h5>',
        '<h5 class="gray_color _eleY">أن نصنع مستقبلًا عمرانيًا وصناعيًا أكثر تطورًا، وأن نرسخ مكانتنا كأحد الرواد في تنفيذ المشاريع المتكاملة بالمملكة العربية السعودية، عبر الابتكار والجودة والتميز في كل ما نقدمه.</h5>',
    )

    # Values
    values_html = "\n".join(value_block(t, b) for t, b in VALUES)
    content = replace_between(
        content,
        '<div class="faq_blocks f f-c _eleWrap">',
        "</div>\n\n            </div>\n\n        </div>\n\n    </div>\n\n</section>\n<!-- Our Values End -->",
        '<div class="faq_blocks f f-c _eleWrap">\n\n'
        + values_html
        + "\n                ",
    )

    # Team sidebars
    team_sidebars = "\n".join(leader_sidebar(tid, img, title) for tid, img, title in LEADERS)
    content = replace_between(
        content,
        '<div class="sidebar_set" data-id="team-2">',
        '<div class="sidebar_set" data-id="partner-5">',
        team_sidebars + "\n    ",
    )

    # Leaders section - remove tabs, single panel with 5
    leaders_cards = "\n".join(
        leader_card(tid, img, title, str(i)) for i, (tid, img, title) in enumerate(LEADERS, 1)
    )
    leaders_section = f"""        <div class="section_body">
                <div class="tab_panel active _eleWrap" id="panel1">
{leaders_cards}                </div>
        </div>
"""
    content = replace_between(
        content,
        '<div class="section_body">',
        "</section>\n<!-- Management End -->",
        leaders_section,
        # only first occurrence after our-leaders - need more specific
    )

    # The replace_between above might hit wrong section - fix with section id anchor
    start = content.find('<section id="our-leaders">')
    body_start = content.find('<div class="section_body">', start)
    body_end = content.find("</section>\n<!-- Management End -->", start)
    content = (
        content[:body_start]
        + leaders_section.rstrip()
        + "\n\n    </div>\n\n"
        + content[body_end:]
    )

    # Remove tabs nav in leaders head
    content = re.sub(
        r'<div class="tabs_nav_set f f-c a-s">.*?</div>\s*</div>\s*<!-- Arrows Start -->',
        "<!-- Arrows Start -->",
        content,
        count=1,
        flags=re.DOTALL,
    )

    # Partners intro + logos
    content = content.replace(
        '<p class="gray_color">نعمل في بيئة تسودها روش المثابرة والاجتهاد. حيث يسعى جميع أعضاء فريقنا وشركائنا جاهدين لتقديم أفضل الخدمات لعملائنا ضمن المواعيد المحددة.</p>'.replace(
            "روش", "روح"
        ),
        '<p class="gray_color">تحت مظلة شركة الرويس تعمل شركاتنا التابعة يداً بيد — كلٌّ في تخصصها — نحو هدف مشترك وهو تقديم حلول متكاملة بجودة لا تُساوم عليها.</p>',
    )
    content = content.replace(
        '<p class="gray_color">نعمل في بيئة تسودها روح المثابرة والاجتهاد. حيث يسعى جميع أعضاء فريقنا وشركائنا جاهدين لتقديم أفضل الخدمات لعملائنا ضمن المواعيد المحددة.</p>',
        '<p class="gray_color">تحت مظلة شركة الرويس تعمل شركاتنا التابعة يداً بيد — كلٌّ في تخصصها — نحو هدف مشترك وهو تقديم حلول متكاملة بجودة لا تُساوم عليها.</p>',
    )

    partners_logos = "\n".join(
        partner_logo(pid, img, name) for pid, img, name, _ in SUBSIDIARIES
    )
    content = replace_between(
        content,
        '<div class="tab_panel active _eleWrap" id="c-2">',
        "<!--[if ENDBLOCK]><![endif]-->            <!-- Partners Logos End -->",
        '<div class="tab_panel active _eleWrap" id="c-2">\n'
        + partners_logos
        + "                ",
    )

    partner_sidebars = "\n".join(
        partner_sidebar(pid, img, name, desc) for pid, img, name, desc in SUBSIDIARIES
    )
    content = replace_between(
        content,
        '<div class="sidebar_set" data-id="partner-5">',
        "<!--[if ENDBLOCK]><![endif]-->",
        partner_sidebars + "    ",
    )

    HTML.write_text(content, encoding="utf-8")
    print("Updated", HTML)


if __name__ == "__main__":
    main()
