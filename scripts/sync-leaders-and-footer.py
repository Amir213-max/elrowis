# -*- coding: utf-8 -*-
"""Update leaders from قادتنا folder and sync Arabic footers to homepage."""
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC_DIR = ROOT / "قادتنا"
OUT_DIR = ROOT / "images" / "about"
ABOUT_HTML = ROOT / "ar" / "about-us.html"
HOME_HTML = ROOT / "ar.html"

LEADERS = [
    (
        "team-1",
        "leader-01.jpg",
        "الصورة 1",
        "نايف العتيبي",
        "رئيس مجلس الإدارة",
    ),
    (
        "team-2",
        "leader-02.jpg",
        "الصورة 2",
        "د. وائل غنام",
        "الرئيس التنفيذي",
    ),
    (
        "team-3",
        "leader-03.jpg",
        "الثالث",
        "م. أحمد حلمي",
        "مدير إدارة المشاريع",
    ),
    (
        "team-4",
        "leader-04.jpg",
        "الرابع",
        "م. جمال حمودة",
        "مدير المكتب الفني",
    ),
    (
        "team-5",
        "leader-abdulmajid.jpg",
        "الصورة 5",
        "عبدالمجيد البدراني",
        "مدير إدارة الموارد البشرية",
    ),
    (
        "team-6",
        "leader-06.jpg",
        "الصورة 6",
        "عبدالله مصطفى",
        "المدير المالي",
    ),
]

SRC_MAP = {
    "leader-01.jpg": "الصورة 1",
    "leader-02.jpg": "الصورة 2",
    "leader-03.jpg": "الثالث",
    "leader-04.jpg": "الرابع",
    "leader-abdulmajid.jpg": "الصورة 5",
    "leader-06.jpg": "الصورة 6",
}


def find_src_file(key: str) -> Path:
  rules = {
    "الصورة 1": lambda n: "الصورة 1" in n and "نايف" in n,
    "الصورة 2": lambda n: "الصورة 2" in n and "وائل" in n,
    "الثالث": lambda n: "الثالث" in n or "حلمي" in n,
    "الرابع": lambda n: "الرابع" in n or "جمال" in n,
    "الصورة 5": lambda n: "عبدالمجيد" in n,
    "الصورة 6": lambda n: "الصورة 6" in n and "مصطفى" in n,
  }
  test = rules.get(key)
  if not test:
    raise KeyError(key)
  for f in SRC_DIR.iterdir():
    if f.is_file() and test(f.name):
      return f
  raise FileNotFoundError(f"No source image for {key}")


def copy_leader_images():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for _, dest, key, _, _ in LEADERS:
        src = find_src_file(key)
        dest_path = OUT_DIR / dest
        shutil.copy2(src, dest_path)
        print("copied", src.name, "->", dest)


def leader_sidebar(team_id: str, img: str, name: str, title: str) -> str:
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


def leader_card(team_id: str, img: str, name: str, title: str) -> str:
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


def update_leaders():
    copy_leader_images()
    content = ABOUT_HTML.read_text(encoding="utf-8")

    sidebars = "\n".join(
        leader_sidebar(tid, img, name, title) for tid, img, _, name, title in LEADERS
    )
    content = re.sub(
        r'<div class="sidebar_set" data-id="team-1">.*?<div class="sidebar_set" data-id="partner-1">',
        sidebars.strip() + '\n\n                <!-- Bar Start -->\n            <div class="sidebar_set" data-id="partner-1">',
        content,
        count=1,
        flags=re.DOTALL,
    )

    cards = "\n".join(
        leader_card(tid, img, name, title) for tid, img, _, name, title in LEADERS
    )
    content = re.sub(
        r'(<div class="tab_panel active _eleWrap" id="panel1">).*?(</div>\s*</div>\s*\n\s*</div>\s*\n\n</section>)',
        r"\1\n" + cards + r"                \2",
        content,
        count=1,
        flags=re.DOTALL,
    )

    ABOUT_HTML.write_text(content, encoding="utf-8")
    print("Updated leaders in", ABOUT_HTML)


def extract_home_footer() -> str:
    html = HOME_HTML.read_text(encoding="utf-8")
    m = re.search(r"(<footer>.*?</footer>)", html, flags=re.DOTALL)
    if not m:
        raise SystemExit("Footer not found in ar.html")
    return m.group(1)


def adjust_footer_links(footer: str, html_path: Path) -> str:
    rel = html_path.relative_to(ROOT).as_posix()
    parts = rel.split("/")

    if rel in ("ar.html", "index.html"):
        return footer

    if parts[0] == "ar" and len(parts) == 2:
        return footer.replace('href="ar/', 'href="')

    if parts[0] == "ar" and parts[1] == "article":
        return footer.replace('href="ar/', 'href="../')

    if parts[0] == "en" and len(parts) == 2:
        return footer.replace('href="ar/', 'href="../ar/')

    if parts[0] == "en" and parts[1] == "article":
        return footer.replace('href="ar/', 'href="../../ar/')

    return footer.replace('href="ar/', 'href="ar/')


def sync_footers():
    home_footer = extract_home_footer()
    targets = [HOME_HTML, ROOT / "index.html"]
    targets.extend(ROOT.glob("ar/**/*.html"))
    updated = 0
    for path in targets:
        if not path.is_file():
            continue
        content = path.read_text(encoding="utf-8")
        if "<footer>" not in content:
            continue
        new_footer = adjust_footer_links(home_footer, path)
        new_content, n = re.subn(
            r"<footer>.*?</footer>",
            new_footer,
            content,
            count=1,
            flags=re.DOTALL,
        )
        if n and new_content != content:
            path.write_text(new_content, encoding="utf-8")
            updated += 1
    print(f"Synced footer on {updated} files")


def main():
    update_leaders()
    sync_footers()


if __name__ == "__main__":
    main()
