#!/usr/bin/env python3
"""Copy gallery images and update media-room gallery section."""

from __future__ import annotations

import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MEDIA_ROOM = ROOT / "ar" / "media-room.html"
GALLERY_DEST = ROOT / "images" / "media-gallery"
SECTION_OLD = "معرض الوسائط"
SECTION_NEW = "معرض الصور"


def find_source_dir() -> Path:
    for d in ROOT.iterdir():
        if d.is_dir() and "معرض" in d.name and "صور" in d.name:
            return d
    raise FileNotFoundError("Gallery source folder not found")


def copy_gallery_images(source: Path) -> list[str]:
    GALLERY_DEST.mkdir(parents=True, exist_ok=True)
    exts = {".jpg", ".jpeg", ".png", ".webp", ".gif"}
    files = sorted(
        f for f in source.iterdir()
        if f.is_file() and f.suffix.lower() in exts
    )
    if not files:
        raise FileNotFoundError(f"No images in {source}")

    rel_paths: list[str] = []
    for i, src in enumerate(files, start=1):
        ext = src.suffix.lower()
        if ext == ".jpeg":
            ext = ".jpg"
        dest_name = f"gallery-{i:02d}{ext}"
        dest = GALLERY_DEST / dest_name
        shutil.copy2(src, dest)
        rel_paths.append(f"../images/media-gallery/{dest_name}")
    return rel_paths


def build_slides(paths: list[str]) -> str:
    slides = []
    for path in paths:
        slides.append(
            f"""                    <!-- Image Start -->
                    <div class="gallery_slide">
                        <img class="load_img" data-src="{path}" alt="{SECTION_NEW}">
                    </div>
                    <!-- Image End -->"""
        )
    return "\n".join(slides)


def update_media_room(slides_html: str) -> None:
    html = MEDIA_ROOM.read_text(encoding="utf-8")

    html = html.replace(f"<h2>{SECTION_OLD}</h2>", f"<h2>{SECTION_NEW}</h2>")
    html = html.replace(SECTION_OLD, SECTION_NEW)

    html = re.sub(
        r'(<div class="gallery_slider"[^>]*>\s*<!--\[if BLOCK\]><!\[endif\]-->).*?(<!--\[if ENDBLOCK\]><!\[endif\]-->\s*</div>)',
        rf"\1\n{slides_html}\n                \2",
        html,
        count=1,
        flags=re.DOTALL,
    )

    MEDIA_ROOM.write_text(html, encoding="utf-8")


def sync_nav_label() -> int:
    count = 0
    for path in list(ROOT.glob("ar/**/*.html")) + [ROOT / "ar.html", ROOT / "index.html"]:
        text = path.read_text(encoding="utf-8")
        if SECTION_OLD not in text:
            continue
        path.write_text(text.replace(SECTION_OLD, SECTION_NEW), encoding="utf-8")
        count += 1
    return count


def main() -> None:
    source = find_source_dir()
    paths = copy_gallery_images(source)
    slides = build_slides(paths)
    update_media_room(slides)
    n = sync_nav_label()
    print(f"OK — {len(paths)} images, nav updated in {n} files")


if __name__ == "__main__":
    main()
