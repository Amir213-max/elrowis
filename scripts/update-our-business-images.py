# -*- coding: utf-8 -*-
"""Copy our-business page images from صفحة اعمالنا and update HTML."""
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC_ROOT = ROOT / "صفحة اعمالنا"
HTML = ROOT / "ar" / "our-business.html"
OUT = ROOT / "images" / "business"

SECTORS = [
    {
        "html_id": "building-construction",
        "folder_keys": ("التشييد",),
        "image_keys": (("قطاع", "التشييد"), ("الرئيس",), ("رئيس",)),
        "dest_image": "construction.png",
        "clients_subdir": "construction/clients",
        "cache": "v=2",
    },
    {
        "html_id": "infrastructure",
        "folder_keys": ("البن", "التحت"),
        "image_keys": (("البنية",), ("فطاع",), ("قطاع", "البن"), ("الرئيس",), ("رئيس",)),
        "dest_image": "infrastructure.png",
        "clients_subdir": "infrastructure/clients",
        "cache": "v=1",
    },
]


def find_src_root() -> Path:
    for d in ROOT.iterdir():
        if d.is_dir() and "صفحة" in d.name and "اعمال" in d.name:
            return d
    return SRC_ROOT


def find_sector_dir(src_root: Path, folder_keys: tuple[str, ...]) -> Path | None:
    for d in src_root.iterdir():
        if d.is_dir() and all(k in d.name for k in folder_keys):
            return d
    return None


def find_file(folder: Path, *keywords: str) -> Path | None:
    if not folder.is_dir():
        return None
    for f in folder.iterdir():
        if f.is_file() and all(k in f.name for k in keywords):
            return f
    for f in folder.iterdir():
        if f.is_file() and any(k in f.name for k in keywords):
            return f
    return None


def find_clients_dir(sector_dir: Path) -> Path | None:
    for sub in sector_dir.iterdir():
        if sub.is_dir() and "العملاء" in sub.name:
            return sub
    direct = sector_dir / "العملاء"
    return direct if direct.is_dir() else None


def copy_sector(sector_dir: Path, cfg: dict) -> dict:
    result = {"image": None, "clients": []}
    sector_img = None
    for keys in cfg["image_keys"]:
        sector_img = find_file(sector_dir, *keys)
        if sector_img:
            break
    if sector_img:
        dest = OUT / cfg["dest_image"]
        shutil.copy2(sector_img, dest)
        cache = cfg.get("cache", "")
        suffix = f"?{cache}" if cache else ""
        result["image"] = f"../images/business/{dest.name}{suffix}"

    clients_dir = find_clients_dir(sector_dir)
    if clients_dir:
        clients_out = OUT / cfg["clients_subdir"]
        clients_out.mkdir(parents=True, exist_ok=True)
        files = sorted(
            [f for f in clients_dir.iterdir() if f.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp"}],
            key=lambda p: p.name,
        )
        for i, src in enumerate(files, start=1):
            dest = clients_out / f"client-{i:02d}{src.suffix.lower()}"
            shutil.copy2(src, dest)
            result["clients"].append(f"../images/business/{cfg['clients_subdir']}/{dest.name}")
    return result


def copy_images(src_root: Path) -> dict:
    OUT.mkdir(parents=True, exist_ok=True)
    paths = {}

    header = find_file(src_root, "الهيدر") or find_file(src_root, "هيدر")
    if header:
        dest = OUT / "hero.png"
        shutil.copy2(header, dest)
        paths["hero"] = "../images/business/hero.png"

    paths["sectors"] = {}
    for cfg in SECTORS:
        sector_dir = find_sector_dir(src_root, cfg["folder_keys"])
        if sector_dir:
            paths["sectors"][cfg["html_id"]] = copy_sector(sector_dir, cfg)

    return paths


def client_logo_block(src: str) -> str:
    return f"""                            <div class="panel_logo_set">
                                <div class="panel_logo f a-c j-c corners _eleX">
                                    <img class="load_img" data-src="{src}" align="Logo" alt="">
                                </div>
                            </div>
"""


def update_sector_html(content: str, section_id: str, image: str | None, clients: list) -> str:
    if image:
        content = re.sub(
            rf'(<section id="{re.escape(section_id)}">.*?<i class="full_bg cover load_bg" data-src=")[^"]*(")',
            rf"\1{image}\2",
            content,
            count=1,
            flags=re.DOTALL,
        )
    if clients:
        logos = "\n".join(client_logo_block(p) for p in clients)
        content = re.sub(
            rf'(<section id="{re.escape(section_id)}">.*?<div class="logos_slider slider_parent _eleWrap">\s*).*?(</div>\s*<!-- Partners Logos End -->)',
            rf"\1\n{logos}\n                \2",
            content,
            count=1,
            flags=re.DOTALL,
        )
    return content


def update_html(content: str, paths: dict) -> str:
    if paths.get("hero"):
        content = re.sub(
            r'(<section id="">\s*.*?<i class="full_bg cover load_bg" data-src=")[^"]*(")',
            rf"\1{paths['hero']}\2",
            content,
            count=1,
            flags=re.DOTALL,
        )

    for section_id, data in paths.get("sectors", {}).items():
        content = update_sector_html(content, section_id, data.get("image"), data.get("clients") or [])

    return content


def main():
    src_root = find_src_root()
    if not src_root.is_dir():
        raise SystemExit(f"Source folder not found: {src_root}")

    paths = copy_images(src_root)
    content = HTML.read_text(encoding="utf-8")
    content = update_html(content, paths)
    HTML.write_text(content, encoding="utf-8")

    print("hero:", paths.get("hero"))
    for sid, data in paths.get("sectors", {}).items():
        print(sid, "image:", data.get("image"), "clients:", len(data.get("clients") or []))
    print("Updated", HTML)


if __name__ == "__main__":
    main()
