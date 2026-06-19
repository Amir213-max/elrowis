# -*- coding: utf-8 -*-
"""Update Arabic our-business page with new Alruwais content."""
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HTML = ROOT / "ar" / "our-business.html"
SRC_DIR = ROOT / "اعمالنا"
OUT_DIR = ROOT / "images" / "business"
OUT_DIR.mkdir(parents=True, exist_ok=True)

IMAGE_MAP = {
    "construction": "تشييد",
    "operations": "التشغيل",
    "infrastructure": "البنية التحتية",
}

FALLBACK_IMAGES = {
    "construction": ROOT / "images" / "business" / "construction.png",
    "operations": ROOT / "images" / "business" / "facilities-operations.png",
    "infrastructure": ROOT / "images" / "business" / "work-environment.png",
}

HERO = {
    "title": "نحوّل الرؤى إلى إنجازات راسخة",
    "intro": (
        "نمتلك الخبرة والقدرات التي تمكننا من تنفيذ مشاريع نوعية في مختلف القطاعات، "
        "مع الالتزام بأعلى معايير الجودة والسلامة والاستدامة، بما يضمن تحقيق أفضل "
        "النتائج لعملائنا والمجتمعات التي نخدمها"
    ),
}

OVERVIEW = (
    "منذ تأسيسنا ونحن نعمل لترسيخ قيمنا ونواصل تنفيذ مشاريع استراتيجية تسهم فى "
    "دعم التنمية وبناء مستقبل اكثر استدامة فى مختلف القطاعات."
)

SECTORS = {
    "building-construction": {
        "old_id": "energy",
        "title": "قطاع التشييد والبناء",
        "text": (
            "نصنع واقعاً هندسياً ملموساً يدمج بين القيمة الراسخة والأصالة العريقة. "
            "نسخر خبراتنا الممتدة منذ 2015 في تنفيذ مشاريع إنشائية كبرى وحلول بنائية "
            "مبتكرة تتسم بالقوة، والمتانة، والفخامة المعمارية."
        ),
        "clients": "عملاء قطاع التشييد والبناء",
        "projects": "مشاريع قطاع التشييد والبناء",
        "image_key": "construction",
    },
    "operations": {
        "old_id": "infrastructure",
        "title": "قطاع التشغيل",
        "text": (
            "نتميز في إدارة وتشغيل المنشآت الحيوية والمرافق بكفاءة وموثوقية عالية منذ "
            "عام 2015، متبنين حلولاً رقمية وتقنيات ذكية لرفع كفاءة الأداء، تقليل "
            "التكاليف، وضمان استدامة الأصول بما يتوافق مع مستهدفات رؤية 2030."
        ),
        "clients": "عملاء قطاع التشغيل",
        "projects": "مشاريع قطاع التشغيل",
        "image_key": "operations",
    },
    "infrastructure": {
        "old_id": "buildings",
        "title": "قطاع البنية التحتية",
        "text": (
            "نتميز في وضع الأسس الراسخة للمدن والمجتمعات الحديثة منذ عام 2015، من "
            "خلال تنفيذ شبكات مياه، وطرق، وأنظمة تصريف متكاملة تتماشى مع رؤية 2030 "
            "لتوفير بيئة عمرانية متطورة وأكثر استدامة."
        ),
        "clients": "عملاء قطاع البنية التحتية",
        "projects": "مشاريع قطاع البنية التحتية",
        "image_key": "infrastructure",
    },
}


def find_image(keyword: str) -> Path | None:
    if not SRC_DIR.is_dir():
        return None
    for f in SRC_DIR.iterdir():
        if f.is_file() and keyword in f.name and f.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp"}:
            return f
    return None


def copy_sector_images():
    copied = {}
    files = {
        "construction": ("construction.png", "تشييد"),
        "operations": ("facilities-operations.png", "التشغيل"),
        "infrastructure": ("infrastructure.png", "البنية التحتية"),
    }
    for key, (dest_name, kw) in files.items():
        dest = OUT_DIR / dest_name
        src = find_image(kw)
        if src:
            shutil.copy2(src, dest)
        elif not dest.exists() and FALLBACK_IMAGES.get(key) and FALLBACK_IMAGES[key].exists():
            dest = FALLBACK_IMAGES[key]
        elif dest.exists():
            pass
        else:
            continue
        copied[key] = f"../images/business/{dest.name}"
    return copied


def replace_section_id(content: str, old_id: str, new_id: str) -> str:
    return content.replace(f'<section id="{old_id}">', f'<section id="{new_id}">', 1)


def update_sector_block(content: str, old_id: str, sector: dict, image_path: str | None) -> str:
    pattern = rf'(<section id="{re.escape(old_id if old_id != sector.get("new_id") else old_id)}">.*?)(</section>)'
    # After id rename, use new id
    new_id = sector["new_id"] if "new_id" in sector else old_id
    m = re.search(rf'<section id="{re.escape(new_id)}">.*?</section>', content, flags=re.DOTALL)
    if not m:
        # try before rename
        pass

    replacements = [
        (r"<h1 class=\"_eleY\">[^<]*</h1>", f'<h1 class="_eleY">{sector["title"]}</h1>'),
        (
            r'(<section id="' + re.escape(new_id) + r'">.*?<p class="_eleY">)[^<]*(</p>)',
            rf"\1{sector['text']}\2",
        ),
        (r"<h2>عملاء[^<]*</h2>", f'<h2>{sector["clients"]}</h2>'),
        (r"<h2>مشاريع[^<]*</h2>", f'<h2>{sector["projects"]}</h2>'),
    ]
    # Scope replacements to section only
    sec_pat = rf'(<section id="{re.escape(new_id)}">.*?</section>)'
    sec_m = re.search(sec_pat, content, flags=re.DOTALL)
    if not sec_m:
        return content
    block = sec_m.group(1)
    block = re.sub(r"<h1 class=\"_eleY\">[^<]*</h1>", f'<h1 class="_eleY">{sector["title"]}</h1>', block, count=1)
    block = re.sub(
        r'(<div class="hero_content f f-c a-c _eleWrap">\s*<h1 class="_eleY">[^<]*</h1>\s*<p class="_eleY">)[^<]*(</p>)',
        rf"\1{sector['text']}\2",
        block,
        count=1,
        flags=re.DOTALL,
    )
    block = re.sub(r"<h2>عملاء[^<]*</h2>", f'<h2>{sector["clients"]}</h2>', block)
    block = re.sub(r"<h2>مشاريع[^<]*</h2>", f'<h2>{sector["projects"]}</h2>', block)
    if image_path:
        block = re.sub(
            r'(<section id="' + re.escape(new_id) + r'">.*?<i class="full_bg cover load_bg" data-src=")[^"]*(")',
            rf"\1{image_path}\2",
            block,
            count=1,
            flags=re.DOTALL,
        )
    return content[: sec_m.start()] + block + content[sec_m.end() :]


def update_nav(content: str) -> str:
    nav_items = [
        ("overview", "نظرة عامة", False),
        ("building-construction", "التشييد والبناء", True),
        ("operations", "التشغيل", True),
        ("infrastructure", "البنية التحتية", True),
    ]
    # Remove old sector nav entries and resources from page subnav
    content = re.sub(
        r'<li class="has_indent">\s*<a href="javascript:void\(0\);"\s*class="scrollTo"\s*data-scroll="energy"[^>]*>.*?</li>\s*',
        "",
        content,
        flags=re.DOTALL,
    )
    content = re.sub(
        r'<li class="has_indent">\s*<a href="javascript:void\(0\);"\s*class="scrollTo"\s*data-scroll="building-construction"[^>]*>.*?</li>\s*',
        "",
        content,
        flags=re.DOTALL,
    )
    content = re.sub(
        r'<li class="">\s*<a href="javascript:void\(0\);"\s*class="scrollTo"\s*data-scroll="resources"[^>]*>.*?</li>\s*',
        "",
        content,
        flags=re.DOTALL,
    )
    # Insert new nav after overview
    new_links = ""
    for scroll_id, label, indent in nav_items[1:]:
        cls = "has_indent" if indent else ""
        new_links += f'''                                                                                                                                <li class="{cls}">
                                                <a href="javascript:void(0);"
                                                    class="scrollTo"                                                     data-scroll="{scroll_id}" >
                                                    {label}
                                                </a>
                                            </li>
'''
    content = content.replace(
        '''                                                    نظرة عامة
                                                </a>
                                            </li>
''',
        '''                                                    نظرة عامة
                                                </a>
                                            </li>
''' + new_links,
        1,
    )
    return content


def main():
    images = copy_sector_images()
    content = HTML.read_text(encoding="utf-8")

    # Hero (first page hero only)
    content = content.replace(
        "<h1 class=\"_eleY\">مستوى عالٍ من التميز التقنية والجمالي</h1>",
        f'<h1 class="_eleY">{HERO["title"]}</h1>',
        1,
    )
    content = content.replace(
        "<p class=\"_eleY\">نلتزم بتشكيل مستقبل أفضل للمجتمعات التي نخدمها من خلال تقديم حلول مبتكرة ومستدامة للأجيال القادمة.</p>",
        f'<p class="_eleY">{HERO["intro"]}</p>',
        1,
    )

    content = content.replace(
        "<p>على مدى أكثر من 44 عاماً من الابتكار، برزنا كرواد في هذا المجال، مدفوعين بالاستحواذات الاستراتيجية والشراكات الفعالة. تمتد أعمالنا عبر ثلاث قطاعات ديناميكية.</p>",
        f"<p>{OVERVIEW}</p>",
        1,
    )

    # Rename section ids
    content = replace_section_id(content, "energy", "building-construction")
    content = replace_section_id(content, "infrastructure", "operations")
    content = replace_section_id(content, "buildings", "infrastructure")

    # Update each sector
    mapping = [
        ("building-construction", SECTORS["building-construction"], images.get("construction")),
        ("operations", SECTORS["operations"], images.get("operations")),
        ("infrastructure", SECTORS["infrastructure"], images.get("infrastructure")),
    ]
    for sec_id, data, img in mapping:
        data = {**data, "new_id": sec_id}
        content = update_sector_block(content, sec_id, data, img)

    content = update_nav(content)

    # Hide resources section
    if 'id="resources"' in content:
        content = content.replace('<section id="resources">', '<section id="resources" hidden style="display:none !important">', 1)

    HTML.write_text(content, encoding="utf-8")
    print("Updated", HTML)


if __name__ == "__main__":
    main()
