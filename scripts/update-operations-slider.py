# -*- coding: utf-8 -*-
"""Build operations sector slider + client images from صفحة اعمالنا/التشغيل."""
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HTML = ROOT / "ar" / "our-business.html"
OUT_SLIDES = ROOT / "images" / "business" / "operations" / "slides"
OUT_CLIENTS = ROOT / "images" / "business" / "operations" / "clients"

SECTOR_TEXT = (
    "نتميز في إدارة وتشغيل المنشآت الحيوية والمرافق بكفاءة وموثوقية عالية منذ "
    "عام 2015، متبنين حلولاً رقمية وتقنيات ذكية لرفع كفاءة الأداء، تقليل "
    "التكاليف، وضمان استدامة الأصول بما يتوافق مع مستهدفات رؤية 2030."
)


def find_page_root() -> Path:
    for d in ROOT.iterdir():
        if d.is_dir() and "صفحة" in d.name and "اعمال" in d.name:
            return d
    raise SystemExit("صفحة اعمالنا folder not found")


def find_operations_dir(page_root: Path) -> Path:
    for d in page_root.iterdir():
        if d.is_dir() and "التشغيل" in d.name:
            return d
    raise SystemExit("التشغيل folder not found")


def find_subdir(parent: Path, keyword: str) -> Path | None:
    for sub in parent.iterdir():
        if sub.is_dir() and keyword in sub.name:
            return sub
    return None


def title_from_filename(name: str) -> str:
    return Path(name).stem.strip()


def copy_slides(sector_dir: Path) -> list[tuple[str, str]]:
    slides_dir = find_subdir(sector_dir, "القطاع")
    if not slides_dir:
        return []
    OUT_SLIDES.mkdir(parents=True, exist_ok=True)
    items = []
    files = sorted(
        f for f in slides_dir.iterdir()
        if f.is_file() and f.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp"}
    )
    for i, src in enumerate(files, start=1):
        dest = OUT_SLIDES / f"slide-{i:02d}{src.suffix.lower()}"
        shutil.copy2(src, dest)
        title = title_from_filename(src.name)
        rel = f"../images/business/operations/slides/{dest.name}"
        items.append((rel, title))
    return items


def copy_clients(sector_dir: Path) -> list[str]:
    clients_dir = find_subdir(sector_dir, "العملاء")
    if not clients_dir:
        return []
    OUT_CLIENTS.mkdir(parents=True, exist_ok=True)
    paths = []
    files = sorted(
        f for f in clients_dir.iterdir()
        if f.is_file() and f.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp"}
    )
    for i, src in enumerate(files, start=1):
        dest = OUT_CLIENTS / f"client-{i:02d}{src.suffix.lower()}"
        shutil.copy2(src, dest)
        paths.append(f"../images/business/operations/clients/{dest.name}")
    return paths


def slide_col(img: str, title: str, idx: int) -> str:
    return f"""                        <!-- Col Start -->
                            <div class="team_col_set slider_col">
                                <div class="team_col tab_col _x f a-e _eleX" data-id="ops-{idx}">
                                    <i class="cover load_bg full_bg" data-src="{img}"></i>
                                    <div class="team_info f f-c">
                                        <p><strong>{title}</strong></p>
                                    </div>
                                </div>
                            </div>
                        <!-- Col End -->
"""


def client_block(src: str) -> str:
    return f"""                            <div class="panel_logo_set">
                                <div class="panel_logo f a-c j-c corners _eleX">
                                    <img class="load_img" data-src="{src}" align="Logo" alt="">
                                </div>
                            </div>
"""


def build_sector_slider(slides: list[tuple[str, str]]) -> str:
    cols = "".join(slide_col(img, title, i) for i, (img, title) in enumerate(slides, start=1))
    return f"""    <div class="section_wrap tabs_wrap operations_sector_slider white_background f f-c x_padding inner_padding">

        <div class="section_head f a-e s-b">

            <div class="section_shape">
                <svg xmlns="http://www.w3.org/2000/svg" width="99" height="96" fill="none" viewBox="0 0 99 96">
                    <path fill="#003d53" d="M99 38.677V0L0 57.323V96l99-57.323Z"/>
                </svg>
            </div>

            <div class="section_title_set f f-c">
                <div class="section_title f f-c">
                    <h2>قطاع التشغيل</h2>
                </div>
                <p class="gray_color operations_sector_intro">{SECTOR_TEXT}</p>
            </div>

            <div class="arrows_set f">
                <div class="arrow rounded_button orange_bg f a-c j-c magnet _prev" data-dist="1">
                    <svg xmlns="http://www.w3.org/2000/svg" width="13" height="12" fill="none" viewBox="0 0 13 12">
                        <path fill="currentColor" d="M12.598 5.75c0 .383-.301.684-.657.684H2.645L6.28 9.879a.653.653 0 0 1 .028.93c-.247.273-.657.273-.93.027L.566 6.242a.659.659 0 0 1-.191-.492.64.64 0 0 1 .191-.465L5.38.691c.273-.246.684-.246.93.028a.653.653 0 0 1-.028.93L2.645 5.093h9.296c.383 0 .657.3.657.656Z"/>
                    </svg>
                </div>
                <div class="arrow rounded_button orange_bg f a-c j-c magnet _next" data-dist="1">
                    <svg xmlns="http://www.w3.org/2000/svg" width="13" height="12" fill="none" viewBox="0 0 13 12">
                        <path fill="currentColor" d="M.402 5.75c0 .383.301.684.657.684h9.296L6.72 9.879a.653.653 0 0 0-.028.93c.247.273.657.273.93.027l4.813-4.594a.659.659 0 0 0 .191-.492.64.64 0 0 0-.191-.465L7.62.691c-.273-.246-.684-.246-.93.028a.653.653 0 0 0 .028.93l3.636 3.445H1.06c-.383 0-.657.3-.657.656Z"/>
                    </svg>
                </div>
            </div>

        </div>

        <div class="section_body">
            <div class="tab_panel active _eleWrap" id="operations-panel1">
{cols}            </div>
        </div>

    </div>
"""


def main():
    ops_dir = find_operations_dir(find_page_root())
    slides = copy_slides(ops_dir)
    clients = copy_clients(ops_dir)
    if not slides:
        raise SystemExit("No sector slide images found")

    content = HTML.read_text(encoding="utf-8")
    slider_html = build_sector_slider(slides)

    content = re.sub(
        r'<section id="operations">\s*<div class="b_hero dark_green_bg has_overlay f a-c j-c">.*?</div>\s*\n\s*<div class="b_pull_set',
        f'<section id="operations">\n\n{slider_html}\n\n    <div class="b_pull_set',
        content,
        count=1,
        flags=re.DOTALL,
    )

    if clients:
        logos = "\n".join(client_block(p) for p in clients)
        content = re.sub(
            r'(<section id="operations">.*?<div class="logos_slider slider_parent _eleWrap">\s*).*?(</div>\s*<!-- Partners Logos End -->)',
            rf"\1\n{logos}\n                \2",
            content,
            count=1,
            flags=re.DOTALL,
        )

    HTML.write_text(content, encoding="utf-8")
    print("slides:", len(slides), [t for _, t in slides])
    print("clients:", len(clients))
    print("Updated", HTML)


if __name__ == "__main__":
    main()
