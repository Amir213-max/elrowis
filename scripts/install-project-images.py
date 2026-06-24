#!/usr/bin/env python3
"""Copy project images from مشاريعنا/ and wire them into ar/our-projects.html."""

from __future__ import annotations

import json
import re
import shutil
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCE_ROOT = ROOT / "مشاريعنا"
HTML = ROOT / "ar" / "our-projects.html"
IMAGES_ROOT = ROOT / "images" / "projects"
REPORT = Path(__file__).resolve().parent / "_project_images_report.json"

IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".webp", ".gif"}
PLACEHOLDER = "../images/careers/careers-hero.png"

# Page title -> source folder name when they differ
TITLE_TO_FOLDER: dict[str, str] = {
    "عقد مناولة وتشغيل منفذ الخفجي": "عقد مناوله وتشغيل منفذ الخفجي",
}


def resolve_source_folder(title: str, folders: dict[str, Path]) -> Path | None:
    if title in folders:
        return folders[title]
    alt = TITLE_TO_FOLDER.get(title)
    if alt:
        alt_norm = normalize(alt)
        if alt_norm in folders:
            return folders[alt_norm]
    return None


def normalize(text: str) -> str:
    text = unicodedata.normalize("NFKC", text)
    text = re.sub(r"\s+", " ", text.strip())
    return text


def list_source_folders() -> dict[str, Path]:
    folders: dict[str, Path] = {}
    if not SOURCE_ROOT.is_dir():
        return folders
    for entry in SOURCE_ROOT.iterdir():
        if entry.is_dir():
            folders[normalize(entry.name)] = entry
    return folders


def list_images(folder: Path) -> list[Path]:
    files = [
        p
        for p in folder.iterdir()
        if p.is_file() and p.suffix.lower() in IMAGE_EXTS
    ]
    return sorted(files, key=lambda p: p.name.lower())


def card_titles(html: str) -> dict[str, str]:
    titles: dict[str, str] = {}
    for match in re.finditer(
        r'<div class="pro_card corners pointer f f-c" id="(card\d+)".*?<h5>(.*?)</h5>',
        html,
        flags=re.DOTALL,
    ):
        titles[match.group(1)] = normalize(match.group(2))
    return titles


def copy_project_images(card_id: str, src_folder: Path) -> list[str]:
    dest_dir = IMAGES_ROOT / card_id
    if dest_dir.exists():
        shutil.rmtree(dest_dir)
    dest_dir.mkdir(parents=True, exist_ok=True)

    rel_paths: list[str] = []
    for index, src in enumerate(list_images(src_folder), start=1):
        ext = src.suffix.lower()
        if ext == ".jpeg":
            ext = ".jpg"
        dest = dest_dir / f"{index:02d}{ext}"
        shutil.copy2(src, dest)
        rel_paths.append(f"../images/projects/{card_id}/{dest.name}")
    return rel_paths


def slider_markup(paths: list[str]) -> str:
    lines = [
        f'                    <i class="load_bg cover" data-src="{path}"></i>'
        for path in paths
    ]
    inner = "\n".join(lines)
    return (
        "                <!--[if BLOCK]><![endif]-->"
        f"{inner}\n"
        "                <!--[if ENDBLOCK]><![endif]-->"
    )


def update_popup(html: str, card_id: str, paths: list[str]) -> str:
    pattern = (
        rf'(data-id="{re.escape(card_id)}">.*?'
        r'<div class="project_cover full_bg slider_parent">\s*)'
        r".*?"
        r'(\s*</div>\s*<div class="arrows_set f">)'
    )
    replacement = rf"\1{slider_markup(paths)}\n            \2"
    new_html, count = re.subn(pattern, replacement, html, count=1, flags=re.DOTALL)
    if count != 1:
        raise RuntimeError(f"popup update failed for {card_id}")
    return new_html


def update_card(html: str, card_id: str, cover: str) -> str:
    pattern = (
        rf'(<div class="pro_card corners pointer f f-c" id="{re.escape(card_id)}"[^>]*>\s*'
        r'<div class="pro_cover f a-c j-c">\s*)'
        r".*?"
        r'(\s*<div class="rounded_button orange_bg f a-c j-c">)'
    )
    cover_block = (
        f'<!--[if BLOCK]><![endif]-->                        '
        f'<i class="full_bg load_bg cover" data-src="{cover}"></i>\n'
        f'                    <!--[if ENDBLOCK]><![endif]-->'
    )
    replacement = rf"\1{cover_block}\n                    \2"
    new_html, count = re.subn(pattern, replacement, html, count=1, flags=re.DOTALL)
    if count != 1:
        raise RuntimeError(f"card update failed for {card_id}")
    return new_html


def main() -> None:
    html = HTML.read_text(encoding="utf-8")
    folders = list_source_folders()
    titles = card_titles(html)

    matched: list[dict] = []
    missing_images: list[dict] = []
    unused_folders = set(folders.keys())

    for card_id, title in titles.items():
        src = resolve_source_folder(title, folders)
        if not src:
            missing_images.append({"card_id": card_id, "title": title})
            continue

        unused_folders.discard(normalize(src.name))
        paths = copy_project_images(card_id, src)
        html = update_popup(html, card_id, paths)
        html = update_card(html, card_id, paths[0])
        matched.append(
            {
                "card_id": card_id,
                "title": title,
                "folder": src.name,
                "images": paths,
                "count": len(paths),
            }
        )

    HTML.write_text(html, encoding="utf-8")

    report = {
        "matched_count": len(matched),
        "missing_count": len(missing_images),
        "unused_folder_count": len(unused_folders),
        "matched": matched,
        "missing_images": missing_images,
        "unused_folders": sorted(unused_folders),
    }
    REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"matched={len(matched)} missing={len(missing_images)}")


if __name__ == "__main__":
    main()
