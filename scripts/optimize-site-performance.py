#!/usr/bin/env python3
"""Batch performance patches for HTML pages without layout changes."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKIP_DIRS = {"_archived", "draco-master", "livewire", "models", "scripts", "storage", "files"}

USERWAY_RE = re.compile(
    r'\s*<script src="https://cdn\.userway\.org/widget\.js" data-account="JpfuyjTa9e"></script>\s*',
    re.I,
)
VIDEOJS_CSS_RE = re.compile(
    r'\s*<link href="https://vjs\.zencdn\.net/8\.16\.1/video-js\.css" rel="stylesheet" />\s*',
    re.I,
)
VIDEOJS_JS_RE = re.compile(
    r'\s*<script defer src="https://vjs\.zencdn\.net/8\.16\.1/video\.min\.js"></script>\s*',
    re.I,
)
FONT_OLD = "family=Cairo:wght@200..1000&amp;display=swap"
FONT_NEW = "family=Cairo:wght@400;600;700;800&amp;display=swap"
HERO_VIDEO_RE = re.compile(
    r'(<video[^>]*?\s)preload(?:="[^"]*")?([^>]*>\s*<source src="images/alruwais-hero\.mp4)',
    re.I,
)
LOADER_SVG_STYLE_RE = re.compile(
    r'(<div class="site_loader[^"]*" id="loader">\s*<svg[^>]*?) style="visibility: hidden;"',
    re.I,
)


def patch_html(text: str) -> tuple[str, list[str]]:
    changes: list[str] = []

    if USERWAY_RE.search(text):
        text = USERWAY_RE.sub("\n", text)
        changes.append("userway-deferred")

    if VIDEOJS_CSS_RE.search(text):
        text = VIDEOJS_CSS_RE.sub("\n", text)
        changes.append("videojs-css-removed")

    if VIDEOJS_JS_RE.search(text):
        text = VIDEOJS_JS_RE.sub("\n", text)
        changes.append("videojs-js-removed")

    if FONT_OLD in text:
        text = text.replace(FONT_OLD, FONT_NEW)
        changes.append("font-subset")

    new_text, count = HERO_VIDEO_RE.subn(r'\1preload="metadata"\2', text)
    if count:
        text = new_text
        changes.append(f"hero-preload-metadata:{count}")

    if LOADER_SVG_STYLE_RE.search(text):
        text = LOADER_SVG_STYLE_RE.sub(r"\1", text)
        changes.append("loader-svg-visible")

    text = text.replace("site-fixes.js?v=40", "site-fixes.js?v=41")
    text = text.replace("site-fixes.js?v=39", "site-fixes.js?v=41")
    text = text.replace("site-fixes.css?v=60", "site-fixes.css?v=61")
    text = text.replace("site-fixes.css?v=59", "site-fixes.css?v=61")
    text = text.replace("appdc50.js?v=0.825", "appdc50.js?v=0.826")
    text = text.replace("appdc50.js?v=0.824", "appdc50.js?v=0.826")
    if "site-fixes.js?v=41" in text or "site-fixes.css?v=61" in text or "appdc50.js?v=0.826" in text:
        changes.append("asset-versions")

    return text, changes


def iter_html_files() -> list[Path]:
    files: list[Path] = []
    for path in ROOT.rglob("*.html"):
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        files.append(path)
    return sorted(files)


def main() -> None:
    updated = 0
    for path in iter_html_files():
        original = path.read_text(encoding="utf-8")
        patched, changes = patch_html(original)
        if patched != original:
            path.write_text(patched, encoding="utf-8", newline="\n")
            updated += 1
            print(f"{path.relative_to(ROOT)}: {', '.join(changes)}")
    print(f"\nUpdated {updated} HTML files.")


if __name__ == "__main__":
    main()
