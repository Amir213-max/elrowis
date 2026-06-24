#!/usr/bin/env python3
"""Replace our-projects page content with Alruwais project portfolio."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HTML = ROOT / "ar" / "our-projects.html"
PLACEHOLDER_IMG = "../images/careers/careers-hero.png"

MARKERS = [
    (-5, 4),
    (-8, -3),
    (1, -1),
    (-6, 3),
    (2, -4),
    (-2, 7),
    (-10, -5),
    (3, -4),
    (1, 2),
    (-9, -2),
    (0, 0),
    (2, -5),
    (-6, 2),
    (1, -2),
    (-4, 1),
]

RAW_PROJECTS = [
    {
        "title": "تطوير مرافق وخدمات الاستاد الرياضي بالمدينة الرياضية بالمجمعة",
        "type": "إنشاءات",
        "city": "الرياض",
        "client": "وزارة الرياضة",
        "content": (
            "تطوير مرافق وخدمات الاستاد الرياضي بالمدينة الرياضية بالمجمعة. "
            "يهدف المشروع إلى الارتقاء بكفاءة الاستاد الرياضي من خلال تنفيذ أعمال التطوير "
            "والتأهيل الشاملة للمرافق والبنية التحتية والخدمات التشغيلية، بما يشمل تحسين "
            "المرافق الرياضية والخدمية، وتحديث الأنظمة الكهربائية والميكانيكية والتقنية، "
            "ورفع مستوى السلامة والجودة، وتوفير بيئة تشغيلية متطورة تضمن استدامة الأصول "
            "وتعزز تجربة الرياضيين والجماهير والزوار، بما يتوافق مع أفضل الممارسات الهندسية "
            "والمعايير المعتمدة للمنشآت الرياضية الحديثة."
        ),
    },
    {
        "title": "ترميم مبنى الركاب والجوازات بمنفذ الرقعي",
        "type": "إنشاءات",
        "city": "حفر الباطن",
        "client": "هيئة الزكاة والضريبة والجمارك",
        "content": (
            "ترميم مبنى الركاب والجوازات بمنفذ الرقعي. "
            "يشمل المشروع أعمال ترميم وتأهيل مبنى الركاب والجوازات بمنفذ الرقعي، "
            "بهدف رفع كفاءة المرافق وتحسين بيئة العمل والخدمات المقدمة للمسافرين، "
            "بما يواكب المتطلبات التشغيلية ويعزز جودة تجربة العبور عبر المنفذ."
        ),
    },
    {
        "title": "ترميم وتأهيل مباني متفرقة في الهيئة العامة للتطوير الدفاعي",
        "type": "إنشاءات",
        "city": "الرياض",
        "client": "الهيئة العامة للتطوير الدفاعي",
        "content": (
            "يهدف المشروع إلى تأهيل وتطوير عدد من المباني التابعة للهيئة العامة للتطوير الدفاعي، "
            "عبر تنفيذ أعمال الترميم والتحديث ورفع كفاءة المرافق، بما يضمن استدامة الأداء "
            "التشغيلي وتحقيق أعلى مستويات الجودة والجاهزية."
        ),
    },
    {
        "title": "توريد وتركيب متطلبات تهيئة بيئة العمل في مواقع وزارة المالية",
        "type": "تهيئة بيئة العمل",
        "city": "الرياض",
        "client": "وزارة المالية",
        "content": (
            "يهدف المشروع إلى تجهيز وتهيئة بيئة العمل في مواقع وزارة المالية من خلال توريد "
            "وتركيب المرافق والتجهيزات اللازمة، بما يسهم في تحسين بيئة العمل ورفع كفاءة "
            "المرافق التشغيلية بما يتوافق مع متطلبات الجهات الحكومية الحديثة."
        ),
    },
    {
        "title": "ترميم مواقع متفرقة برئاسة الحرس الملكي بالمنطقة الوسطى",
        "type": "إنشاءات",
        "city": "الرياض",
        "client": "الحرس الملكي",
        "content": (
            "يشمل المشروع تنفيذ أعمال الترميم والتأهيل لعدد من المواقع التابعة لرئاسة الحرس الملكي "
            "بالمنطقة الوسطى، بهدف رفع كفاءة المرافق وتحسين جاهزيتها التشغيلية، "
            "بما يحقق أعلى مستويات الجودة والسلامة والاستدامة."
        ),
    },
    {
        "title": "أعمال تأسيس وتشطيب بمشروع عمارة أرم (90 شقة)",
        "type": "إنشاءات",
        "city": "الرياض",
        "client": "أرم العقارية",
        "content": (
            "تمتد أعمال المشروع لتشمل تنفيذ أعمال التأسيس والتشطيب لعمارة أرم المكونة من 90 شقة سكنية، "
            "مع التركيز على جودة التنفيذ ودقة التفاصيل، بما يسهم في تقديم مشروع سكني متكامل "
            "يلبي احتياجات السكان ويعكس أعلى مستويات الإتقان والتميز."
        ),
    },
    {
        "title": "مشروع تأهيل وتطوير مبنى مستشفى الأطفال القديم بمدينة الملك سعود الطبية",
        "type": "إنشاءات",
        "city": "الرياض",
        "client": "وزارة الصحة",
        "content": (
            "يهدف المشروع إلى إعادة تأهيل وتطوير مبنى مستشفى الأطفال القديم وفق أحدث المعايير "
            "الفنية والهندسية، بما يسهم في تحسين بيئة الرعاية الصحية ورفع كفاءة المرافق الطبية "
            "والخدمية لدعم جودة الخدمات المقدمة للمستفيدين."
        ),
    },
    {
        "title": "تأهيل وحدة القيادة والتحكم بالمركز الرئيسي لهيئة الهلال الأحمر السعودي",
        "type": "تهيئة بيئة العمل",
        "city": "الرياض",
        "client": "الهلال الأحمر السعودي",
        "content": (
            "يشمل المشروع أعمال تأهيل وتطوير وحدة القيادة والتحكم بالمركز الرئيسي لهيئة الهلال الأحمر السعودي، "
            "بهدف تهيئة بيئة عمل متكاملة تدعم كفاءة العمليات التشغيلية وتعزز سرعة الاستجابة "
            "واتخاذ القرار وفق أعلى المعايير الفنية والتشغيلية."
        ),
    },
    {
        "title": "تشغيل ونظافة دورات مياه لحدائق ومنتزهات متفرقة بمدينة الرياض",
        "type": "تشغيل",
        "city": "الرياض",
        "client": "إمارة منطقة الرياض",
        "content": (
            "يهدف المشروع إلى تشغيل وصيانة ونظافة دورات المياه في المواقع الترفيهية والحدائق العامة "
            "بمدينة الرياض، من خلال تطبيق أفضل الممارسات التشغيلية ومعايير الجودة، "
            "بما يسهم في تحسين مستوى الخدمات المقدمة لمرتادي المرافق العامة."
        ),
    },
    {
        "title": "عقد مناولة وتشغيل منفذ الرقعي",
        "type": "تشغيل",
        "city": "حفر الباطن",
        "client": "هيئة الزكاة والضريبة والجمارك",
        "content": (
            "يهدف المشروع إلى إدارة وتشغيل أعمال المناولة بمنفذ الرقعي بكفاءة عالية، "
            "من خلال تطبيق أفضل الممارسات التشغيلية وتنظيم الخدمات اللوجستية، "
            "بما يسهم في تعزيز سرعة الإنجاز وتحسين جودة الخدمات المقدمة بالمنافذ الحدودية."
        ),
    },
    {
        "title": "عقد مناولة وتشغيل منفذ سلوى",
        "type": "تشغيل",
        "city": "العديد",
        "client": "هيئة الزكاة والضريبة والجمارك",
        "content": (
            "يشمل المشروع تنفيذ أعمال المناولة والتشغيل بمنفذ سلوى، بما يضمن إدارة العمليات "
            "التشغيلية بكفاءة عالية وتنظيم حركة الشحنات والمركبات، بما يسهم في تسهيل إجراءات "
            "العبور ورفع مستوى جودة الخدمات المقدمة للمستفيدين."
        ),
    },
    {
        "title": "عقد مناولة وتشغيل منفذ عرعر",
        "type": "تشغيل",
        "city": "عرعر",
        "client": "هيئة الزكاة والضريبة والجمارك",
        "content": (
            "تمتد أعمال المشروع لتشمل مناولة وتشغيل منفذ عرعر من خلال إدارة العمليات التشغيلية "
            "والخدمات المساندة، بما يعزز كفاءة العمل ويرفع مستوى الجاهزية التشغيلية، "
            "ويسهم في تقديم خدمات متكاملة وفق أعلى معايير الجودة والسلامة."
        ),
    },
    {
        "title": "عقد مناولة منفذ جسر الملك فهد",
        "type": "تشغيل",
        "city": "الخبر",
        "client": "هيئة الزكاة والضريبة والجمارك",
        "content": (
            "يشمل المشروع تنفيذ أعمال المناولة بمنفذ جسر الملك فهد، بما يضمن كفاءة التعامل "
            "مع حركة البضائع والشحنات وتنظيم العمليات التشغيلية، بما يسهم في تعزيز انسيابية "
            "الحركة ورفع مستوى الخدمات اللوجستية المقدمة."
        ),
    },
    {
        "title": "عقد مناولة وتشغيل منفذ البطحاء",
        "type": "تشغيل",
        "city": "العديد",
        "client": "هيئة الزكاة والضريبة والجمارك",
        "content": (
            "تمتد أعمال المشروع لتشمل مناولة وتشغيل منفذ البطحاء من خلال إدارة العمليات "
            "التشغيلية والخدمات المساندة بكفاءة واحترافية، بما يدعم استمرارية الأعمال "
            "ويعزز جودة الخدمات اللوجستية وفق أعلى معايير الجودة والسلامة."
        ),
    },
    {
        "title": "عقد مناولة وتشغيل منفذ الخفجي",
        "type": "تشغيل",
        "city": "الخفجي",
        "client": "هيئة الزكاة والضريبة والجمارك",
        "content": (
            "مشروع يهدف إلى تعزيز كفاءة التشغيل ورفع مستوى الجاهزية التشغيلية للمنفذ "
            "من خلال تنفيذ أعمال الصيانة والتطوير الشاملة للمرافق والبنية التحتية، "
            "وفق أفضل الممارسات الهندسية ومعايير الجودة والسلامة، بما يدعم استمرارية "
            "الخدمات وتحقيق أعلى مستويات الأداء."
        ),
    },
]

# Interleave operation/port projects among construction projects.
ORDER = [1, 10, 2, 11, 3, 12, 4, 13, 5, 14, 6, 15, 7, 8, 9]
PROJECTS = [RAW_PROJECTS[i - 1] for i in ORDER]

CLOSE_BTN = """        <div class="rounded_button orange_bg f a-c j-c close pointer magnet" data-dist="1">
            <svg xmlns="http://www.w3.org/2000/svg" width="25" height="24" fill="none" viewBox="0 0 25 24">
                <path stroke="#fff" stroke-linecap="round" stroke-width="2" d="m5.969 4.994 14 14m0-14-14 14"/>
            </svg>
        </div>"""

ARROWS = """            <div class="arrows_set f">
                <div class="arrow rounded_button orange_bg f a-c j-c magnet _prev" data-dist="1">
                    <svg xmlns="http://www.w3.org/2000/svg" width="13" height="12" fill="none" viewBox="0 0 13 12">
                        <path fill="currentColor" d="M12.598 5.75c0 .383-.301.684-.657.684H2.645L6.28 9.879a.653.653 0 0 1 .028.93c-.247.273-.657.273-.93.027L.566 6.242a.659.659 0 0 1-.191-.492.64.64 0 0 1 .191-.465L5.38.691c.273-.246.684-.246.93.028a.653.653 0 0 1-.028.93L2.645 5.093h9.296c.383 0 .657.3.657.656Z"/>
                    </svg>
                </div>
                <div class="arrow rounded_button orange_bg f a-c j-c magnet _next" data-dist="1">
                    <svg xmlns="http://www.w3.org/2000/svg" width="13" height="12" fill="none" viewBox="0 0 13 12">
                        <path fill="currentColor" d="M.402 5.75c0 .383.301.684.657.684h9.296L6.72 9.879a.653.653 0 0 0-.028.93c.247.273.657.273.93.027l4.813-4.594a.659.659 0 0 0 .191-.492.64.64 0 0 1 .191-.465L7.62.691c-.273-.246-.684-.246-.93.028a.653.653 0 0 0 .028.93l3.636 3.445H1.06c-.383 0-.657.3-.657.656Z"/>
                    </svg>
                </div>
            </div>"""

CARD_ICON = """                    <div class="rounded_button orange_bg f a-c j-c">
                        <svg xmlns="http://www.w3.org/2000/svg" width="25" height="24" fill="none" viewBox="0 0 25 24">
                            <path fill="#fff" fill-rule="evenodd" d="M13.969 2.994h8v8h-1.5V5.555l-5.5 5.5-1.06-1.06 5.5-5.5h-5.44v-1.5Zm-1.94 11-5.5 5.5h5.44v1.5h-8v-8h1.5v5.44l5.5-5.5 1.06 1.06Z" clip-rule="evenodd"/>
                        </svg>
                    </div>"""


def popup_html(card_id: str, project: dict) -> str:
    return f"""    <!-- Project Start -->
    <div class="popup_card f corners white_background has_slider" data-id="{card_id}">

{CLOSE_BTN}

        <div class="project_cover_set f a-e j-e corners">
            <div class="project_cover full_bg slider_parent">
                <!--[if BLOCK]><![endif]-->                    <i class="load_bg cover" data-src="{PLACEHOLDER_IMG}"></i>
                <!--[if ENDBLOCK]><![endif]-->            </div>
{ARROWS}
        </div>

        <div class="pro_side f f-c">

            <div class="pro_title">
                <h3>{project["title"]}</h3>
            </div>
            <div class="pro_card_info f f-c">
                <ul class="f f-w">
                    <li class="f">
                        <strong>النوع:</strong>
                        <span class="gray_color">{project["type"]}</span>
                    </li>
                    <li class="f">
                        <strong>المدينة:</strong>
                        <span class="gray_color">{project["city"]}</span>
                    </li>
                    <li class="f">
                        <strong>العميل:</strong>
                        <span class="gray_color">{project["client"]}</span>
                    </li>
                </ul>
            </div>

            <div class="pro_details f f-c" style="max-height: 400px; overflow-y: auto">
                <p>{project["content"]}</p>
            </div>

        </div>

    </div>
    <!-- Project End -->"""


def card_html(card_id: str, project: dict, marker: tuple[int, int]) -> str:
    x, z = marker
    return f"""            <!-- Card Start -->
            <div class="pro_card corners pointer f f-c" id="{card_id}" data-marker-x="{x}" data-marker-z="{z}">
                <div class="pro_cover f a-c j-c">
                                        <!--[if BLOCK]><![endif]-->                        <i class="full_bg load_bg cover" data-src="{PLACEHOLDER_IMG}"></i>
                    <!--[if ENDBLOCK]><![endif]-->{CARD_ICON}
                </div>
                <div class="map_card_info f a-c s-b">
                    <span>{project["type"]}</span>
                    <span>{project["client"]}</span>
                    <span>{project["city"]}</span>
                </div>
                <div class="pro_title">
                    <h5>{project["title"]}</h5>
                </div>
            </div>
            <!-- Card End -->"""


def build_popups() -> str:
    blocks = []
    for idx, project in enumerate(PROJECTS, start=1):
        blocks.append(popup_html(f"card{idx}", project))
    return "    <!--[if BLOCK]><![endif]-->    " + "\n        ".join(blocks) + "\n    <!--[if ENDBLOCK]><![endif]-->"


def build_cards() -> str:
    blocks = []
    for idx, project in enumerate(PROJECTS, start=1):
        blocks.append(card_html(f"card{idx}", project, MARKERS[(idx - 1) % len(MARKERS)]))
    return "            <!--[if BLOCK]><![endif]-->            " + "\n                        ".join(blocks) + "\n            <!--[if ENDBLOCK]><![endif]-->"


def main() -> None:
    html = HTML.read_text(encoding="utf-8")

    html = re.sub(
        r"(<!-- Popup Start -->\s*<div class=\"popup_wrap[^>]*>\s*).*?(<!--\[if ENDBLOCK\]><!\[endif\]-->\s*</div>\s*<!-- Popup End -->)",
        rf"\1{build_popups()}\n</div>\n<!-- Popup End -->",
        html,
        count=1,
        flags=re.DOTALL,
    )

    html = re.sub(
        r"(<div class=\"pro_cards f f-c\">\s*).*?(<!--\[if ENDBLOCK\]><!\[endif\]-->\s*</div>\s*\n\s*</div>\s*\n\s*</section>\s*<!-- Map End -->)",
        rf"\1{build_cards()}\n        </div>\n\n    </div>\n\n</section>\n<!-- Map End -->",
        html,
        count=1,
        flags=re.DOTALL,
    )

    HTML.write_text(html, encoding="utf-8")
    print(f"OK — {len(PROJECTS)} projects")


if __name__ == "__main__":
    main()
