#!/usr/bin/env python3
"""Sync our-business project images only when title matches our-projects."""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUR_BUSINESS = ROOT / "ar" / "our-business.html"
OUR_PROJECTS = ROOT / "ar" / "our-projects.html"

TITLE_ALIASES = {
    "ترmيم وتأhيل mبni 11 وmبni 12 في الهيئة العامة للتطوير الدfاعi": "ترmيم وتأhiel mbani متفرقة في الهيئة العامة للتطوير الدfاعi",
    "عقد منaولة منfذ البطحاء معدات وفniين": "عقد منaولة وتشغيل منfذ البطحاء",
}

PROJECT_BLOCK = re.compile(
    r"(<!-- Project Start -->.*?<!-- Project End -->)",
    re.DOTALL,
)
COVER_RE = re.compile(
    r'(<div class="pro_col_cover">\s*<i class="full_bg load_bg cover" data-src=")([^"]+)("></i>)',
    re.DOTALL,
)
TITLE_RE = re.compile(r"<h4>(.*?)</h4>", re.DOTALL)
PROJECTS_CARD_RE = re.compile(
    r'data-src="(\.\./images/projects/[^"]+)".*?<h5>(.*?)</h5>',
    re.DOTALL,
)


def normalize(text: str) -> str:
    text = re.sub(r"\s+", " ", text.strip())
    for a, b in (("أ", "ا"), ("إ", "ا"), ("آ", "ا"), ("ة", "ه"), ("ى", "ي")):
        text = text.replace(a, b)
    return text


def load_our_projects_images() -> dict[str, str]:
    html = OUR_PROJECTS.read_text(encoding="utf-8")
    return {
        normalize(title): image
        for image, title in PROJECTS_CARD_RE.findall(html)
        if "/images/projects/card" in image
    }


def match_image(title: str, our_projects: dict[str, str]) -> str | None:
    alias = TITLE_ALIASES.get(title)
    if alias and normalize(alias) in our_projects:
        return our_projects[normalize(alias)]
    norm = normalize(title)
    return our_projects.get(norm)


def main() -> None:
    our_projects = load_our_projects_images()
    html = OUR_BUSINESS.read_text(encoding="utf-8")
    matched = 0
    skipped = 0

    def replace_block(block: str) -> str:
        nonlocal matched, skipped
        title_match = TITLE_RE.search(block)
        if not title_match:
            return block
        title = title_match.group(1).strip()
        image = match_image(title, our_projects)
        if not image:
            skipped += 1
            return block
        matched += 1
        new_block, count = COVER_RE.subn(rf"\1{image}?v=2\3", block, count=1)
        return new_block if count else block

    html = PROJECT_BLOCK.sub(lambda m: replace_block(m.group(1)), html)
    OUR_BUSINESS.write_text(html, encoding="utf-8")
    print(f"Updated {matched} matched projects; left {skipped} unchanged")


if __name__ == "__main__":
    main()
