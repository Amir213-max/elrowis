# -*- coding: utf-8 -*-
"""Set 6 leaders in order on about-us.html."""
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC_DIR = ROOT / "قادتنا"
OUT_DIR = ROOT / "images" / "about"
ABOUT_HTML = ROOT / "ar" / "about-us.html"

LEADERS = [
    ("team-1", "leader-01.jpg", lambda n: "الصورة 1" in n and "نايف" in n,
     "نايف الرويس", "رئيس مجلس الإدارة"),
    ("team-2", "leader-02.jpg", lambda n: "الصورة 2" in n and "وائل" in n,
     "د. وائل غنام", "الرئيس التنفيذي"),
    ("team-3", "leader-03.jpg", lambda n: "الثالث" in n or "حلمي" in n,
     "م. أحمد حلمي", "مدير إدارة المشاريع"),
    ("team-4", "leader-04.jpg", lambda n: "الرابع" in n or "جمال" in n,
     "م. جمال حمودة", "مدير المكتب الفني"),
    ("team-5", "leader-abdulmajid.jpg", lambda n: "عبدالمجيد" in n,
     "عبدالمجيد البدراني", "مدير إدارة الموارد البشرية"),
    ("team-6", "leader-06.jpg", lambda n: "الصورة 6" in n and "مصطفى" in n,
     "عبدالله مصطفى", "المدير المالي"),
]


def find_src(pred):
    for f in SRC_DIR.iterdir():
        if f.is_file() and pred(f.name):
            return f
    raise FileNotFoundError(pred)


def copy_images():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for _, dest, pred, _, _ in LEADERS:
        src = find_src(pred)
        shutil.copy2(src, OUT_DIR / dest)
        print("copied", src.name, "->", dest)


def sidebar(team_id, img, name, title):
    return f"""        <!-- Bar Start -->
        <div class="sidebar_set" data-id="{team_id}">
            <div class="tm_bar f f-c">
                <div class="team_cover _ele">
                    <img class="load_img" data-src="../images/about/{img}" alt="{name}">
                </div>
                <div class="team_info f f-c _ele">
                    <p><strong>{name}</strong></p>
                    <span class="gray_color high">{title}</span>
                </div>
            </div>
        </div>
        <!-- Bar End -->
"""


def card(team_id, img, name, title):
    return f"""                        <!-- Col Start -->
                            <div class="team_col_set slider_col">
                                <div class="team_col tab_col _x f a-e _eleX" data-id="{team_id}">
                                    <i class="cover load_bg full_bg" data-src="../images/about/{img}"></i>
                                    <div class="team_info f f-c">
                                        <p><strong>{name}</strong></p>
                                        <span class="gray_color high">{title}</span>
                                    </div>
                                </div>
                            </div>
                        <!-- Col End -->
"""


def main():
    copy_images()
    content = ABOUT_HTML.read_text(encoding="utf-8")

    sidebars = "\n".join(
        sidebar(tid, img, name, title) for tid, img, _, name, title in LEADERS
    )
    content = re.sub(
        r'<div class="sidebar_set" data-id="team-1">.*?<div class="sidebar_set" data-id="partner-1">',
        sidebars + '\n                <!-- Bar Start -->\n            <div class="sidebar_set" data-id="partner-1">',
        content,
        count=1,
        flags=re.DOTALL,
    )

    cards = "\n".join(card(tid, img, name, title) for tid, img, _, name, title in LEADERS)
    content = re.sub(
        r'(<div class="tab_panel active _eleWrap" id="panel1">).*?(</div>\s*</div>\s*\n\s*</div>\s*\n\n</section>)',
        r"\1\n" + cards + r"                \2",
        content,
        count=1,
        flags=re.DOTALL,
    )

    ABOUT_HTML.write_text(content, encoding="utf-8")
    print("Updated", ABOUT_HTML)


if __name__ == "__main__":
    main()
