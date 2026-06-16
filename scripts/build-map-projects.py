# -*- coding: utf-8 -*-
"""Build homepage map projects from مشاريع folder."""
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC_DIR = ROOT / "مشاريع"
OUT_DIR = ROOT / "images" / "projects"
AR_HTML = ROOT / "ar.html"

TITLES = [
    "تطوير مرافق وخدمات الاستاد الرياضي بالمدينة الرياضية بالمجمعة",
    "تهيئة بيئة العمل في مواقع وزارة المالية",
    "ترميم مبنى الركاب والجوازات بمنفذ الرقعي",
    "تهيئة مقار إدارة بمقر الهيئة العامة للتطوير الدفاعي",
    "تأهيل وحدة القيادة والتحكم بالمركز الرئيسي لهيئة الهلال الأحمر السعودي",
    "مشروع اضافات وتحسينات للأنظمة الكهربائية بمباني وزارة المالية",
    "تشغيل منفذ سلوي",
    "تشغيل منفذ الخفجي",
    "تشغيل منفذ الرقعي",
    "تشغيل منفذ البطحاء",
]


def region_to_location(region: str) -> str:
    r = region
    if "البطحاء" in r or "الإمارات" in r:
        return "location-1"
    if "الرياض" in r:
        return "location-7"
    if "الشرقية" in r or "حفر الباطن" in r or "قطر" in r or "الكويت" in r:
        return "location-11"
    return "location-11"


def region_label(region: str) -> str:
    if "البطحاء" in region or "الإمارات" in region:
        return "منفذ البطحاء"
    if "الرياض" in region:
        return "الرياض"
    if region:
        return "المنطقة الشرقية"
    return ""


def parse_region(filename: str) -> str:
    name = Path(filename).stem
    if " - " in name:
        return name.split(" - ", 1)[1].strip()
    if "-" in name:
        parts = name.split("-", 1)
        return parts[1].strip() if len(parts) > 1 else ""
    return ""


def order_index(filename: str) -> int:
    name = filename.replace("أ", "ا").replace("إ", "ا").replace("آ", "ا")
    if re.search(r"الاول\b|المشروع الاول", name):
        return 1
    if "التاني" in name or "الثاني" in name:
        return 2
    if "الثالث" in name:
        return 3
    if "الرابع" in name:
        return 4
    if "الخامس" in name:
        return 5
    if "السادس" in name:
        return 6
    if re.search(r"المشروع\s*7\b", name):
        return 7
    if re.search(r"المشروع\s*8\b", name):
        return 8
    if "التاسع" in name:
        return 9
    if re.search(r"ال\s*10\b|المشروع\s*10", name):
        return 10
    m = re.search(r"\b10\b", name)
    if m:
        return 10
    m = re.search(r"\b(\d+)\b", name)
    if m:
        n = int(m.group(1))
        if 1 <= n <= 10:
            return n
    return 999


def card_html(title: str, location: str, image_src: str, region: str) -> str:
    label = region_label(region)
    return f"""                    <!-- Project Start -->
                    <div class="map_project">

                        <div class="map_card f f-c corners white_background _eleY" data-location="{location}">

                            <div class="map_card_head f f-c">

                                <h3>{title}
                                <br></h3>

                                <div class="map_card_info f a-c s-b">
                                    <span></span>
                                    <span>{label}</span>
                                    <span></span>
                                    <span></span>
                                </div>

                            </div>

                            <div class="map_card_cover">
                                <i class="full_bg cover load_bg" data-src="{image_src}"></i>
                            </div>

                            <p class="gray_color">
                                
                            </p>

                        </div>

                    </div>
                    <!-- Project End -->
"""


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    if not SRC_DIR.is_dir():
        raise SystemExit(f"Missing folder: {SRC_DIR}")

    files = sorted(SRC_DIR.glob("*.png"), key=lambda p: order_index(p.name))
    if len(files) != 10:
        raise SystemExit(f"Expected 10 PNG files, found {len(files)}")

    new_cards = []
    for i, src in enumerate(files, start=1):
        region = parse_region(src.name)
        loc = region_to_location(region)
        dest = OUT_DIR / f"project-{i:02d}.png"
        shutil.copy2(src, dest)
        title = TITLES[i - 1]
        new_cards.append(
            card_html(title, loc, f"images/projects/project-{i:02d}.png", region)
        )

    content = AR_HTML.read_text(encoding="utf-8")
    html = "\n".join(new_cards)

    start = content.find('<div class="map_projects f f-c _eleWrap">')
    end = content.find("<!--[if ENDBLOCK]><![endif]-->            </div>", start)
    if start == -1 or end == -1:
        raise SystemExit("Could not find map_projects block")

    inner_start = content.find(">", start) + 1
    new_content = (
        content[:inner_start]
        + "\n\n                <!--[if BLOCK]><![endif]-->"
        + html
        + "                <!--[if ENDBLOCK]><![endif]-->"
        + content[end:]
    )

    AR_HTML.write_text(new_content, encoding="utf-8")
    print(f"Wrote {len(new_cards)} projects (removed last project)")
    for i, src in enumerate(files, 1):
        region = parse_region(src.name)
        print(i, region_to_location(region), src.name[:70])


if __name__ == "__main__":
    main()
