#!/usr/bin/env python3
"""Fix design issues, download missing assets, and patch HTML for nesmapartners.com mirror."""

import os
import re
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE_URL = "https://nesmapartners.com/"
GOOGLE_MAPS_DIRECTIONS = (
    "https://www.google.com/maps/search/?api=1&query="
    "Nesma+%26+Partners,+6718+Prince+Majed+bin+AbdulAziz+Street,+Al+Khobar,+Saudi+Arabia"
)
GOOGLE_MAPS_EMBED = (
    "https://www.google.com/maps?q=Building+6718,+Prince+Majed+bin+AbdulAziz+Street,"
    "+Al+Khobar,+Saudi+Arabia&output=embed&z=15"
)

MAP_SECTION_EN = """
                <!-- Map Embed Start -->
                <div class="contact_map_wrap _eleWrap">
                    <h4 class="_eleY">Our Location</h4>
                    <div class="contact_map _eleY">
                        <iframe
                            src="GOOGLE_MAPS_EMBED_PLACEHOLDER"
                            width="100%"
                            height="100%"
                            style="border:0;"
                            allowfullscreen=""
                            loading="lazy"
                            referrerpolicy="no-referrer-when-downgrade"
                            title="Nesma & Partners office location"
                        ></iframe>
                    </div>
                </div>
                <!-- Map Embed End -->
""".replace("GOOGLE_MAPS_EMBED_PLACEHOLDER", GOOGLE_MAPS_EMBED)

MAP_SECTION_AR = MAP_SECTION_EN.replace("Our Location", "موقعنا").replace(
    "Nesma & Partners office location", "موقع مكتب نسما وشركاهم"
)

SITE_FIXES_CSS = '<link href="{prefix}site-fixes.css?v=1" rel="stylesheet">'
SITE_FIXES_JS = '<script defer src="{prefix}site-fixes.js?v=1"></script>'


def normalize_storage_path(url: str) -> str | None:
    url = url.strip()
    if url.startswith("https://nesmapartners.com/"):
        return url.replace("https://nesmapartners.com/", "")
    if url.startswith("http://nesmapartners.com/"):
        return url.replace("http://nesmapartners.com/", "")
    if url.startswith("/storage/"):
        return url.lstrip("/")
    for prefix in ("../../", "../", "./"):
        if url.startswith(prefix + "storage/"):
            return url[len(prefix) :]
    if url.startswith("storage/"):
        return url
    return None


def collect_image_urls() -> set[str]:
    pattern = re.compile(r'data-src=["\']([^"\']+)["\']')
    urls: set[str] = set()
    for html_file in ROOT.rglob("*.html"):
        content = html_file.read_text(encoding="utf-8", errors="ignore")
        for match in pattern.finditer(content):
            path = normalize_storage_path(match.group(1))
            if path and path.startswith("storage/"):
                urls.add(path)
    return urls


def build_download_urls(rel_path: str) -> list[str]:
    """Try multiple URL variants for Laravel media paths."""
    candidates = [
        BASE_URL + rel_path,
        BASE_URL + urllib.parse.quote(rel_path, safe="/"),
        BASE_URL + urllib.parse.quote(urllib.parse.unquote(rel_path), safe="/"),
    ]
    seen: set[str] = set()
    result: list[str] = []
    for url in candidates:
        if url not in seen:
            seen.add(url)
            result.append(url)
    return result


def download_images(urls: set[str], max_retries: int = 2) -> tuple[int, int]:
    downloaded = 0
    failed = 0
    for i, rel_path in enumerate(sorted(urls), 1):
        local_path = ROOT / rel_path.replace("/", os.sep)
        if local_path.exists() and local_path.stat().st_size > 0:
            continue
        local_path.parent.mkdir(parents=True, exist_ok=True)
        ok = False
        for remote_url in build_download_urls(rel_path):
            for attempt in range(max_retries + 1):
                try:
                    req = urllib.request.Request(
                        remote_url,
                        headers={"User-Agent": "Mozilla/5.0 (compatible; SiteFixer/1.0)"},
                    )
                    with urllib.request.urlopen(req, timeout=30) as resp:
                        data = resp.read()
                    if len(data) > 0:
                        local_path.write_bytes(data)
                        downloaded += 1
                        ok = True
                        break
                except Exception:
                    if attempt < max_retries:
                        time.sleep(0.3)
            if ok:
                break
        if not ok:
            failed += 1
        if i % 25 == 0:
            print(f"  Progress: {i}/{len(urls)} (downloaded={downloaded}, failed={failed})", flush=True)
    return downloaded, failed


def localize_remote_data_src(content: str) -> str:
    """Use local storage paths when images were downloaded."""

    def replacer(match: re.Match[str]) -> str:
        quote = match.group(1)
        url = match.group(2)
        path = normalize_storage_path(url)
        if path and (ROOT / path.replace("/", os.sep)).exists():
            return f"data-src={quote}{path}{quote}"
        return match.group(0)

    return re.sub(r'data-src=(["\'])([^"\']+)\1', replacer, content)


def download_extra_assets() -> None:
    extras = [
        ("images/favicon-32x32.png", f"{BASE_URL}images/favicon-32x32.png"),
        ("ae3178bae1c6dab16294.png", f"{BASE_URL}ae3178bae1c6dab16294.png"),
    ]
    for rel, url in extras:
        local_path = ROOT / rel
        if local_path.exists():
            continue
        local_path.parent.mkdir(parents=True, exist_ok=True)
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=20) as resp:
                local_path.write_bytes(resp.read())
            print(f"  Downloaded {rel}")
        except Exception as exc:
            print(f"  Could not download {rel}: {exc}")


def get_prefix(html_path: Path) -> str:
    rel = html_path.relative_to(ROOT)
    depth = len(rel.parts) - 1
    return "../" * depth if depth else ""


def patch_html_file(html_path: Path) -> bool:
    content = html_path.read_text(encoding="utf-8", errors="ignore")
    original = content
    prefix = get_prefix(html_path)
    rel_parts = html_path.relative_to(ROOT).parts

    # Fix broken Get Direction links
    content = content.replace(
        '<a href="#" target="_blank" class="_underline orange_color">Get Direction</a>',
        f'<a href="{GOOGLE_MAPS_DIRECTIONS}" target="_blank" rel="noopener" class="_underline orange_color">Get Direction</a>',
    )
    content = content.replace(
        '<a href="#" target="_blank" class="_underline orange_color">احصل على اتجاهات</a>',
        f'<a href="{GOOGLE_MAPS_DIRECTIONS}" target="_blank" rel="noopener" class="_underline orange_color">احصل على اتجاهات</a>',
    )

    # Fix root homepage footer links only
    if html_path.name in ("en.html", "ar.html"):
        lang = "en" if html_path.name == "en.html" else "ar"
        content = content.replace('href="news.html"', f'href="{lang}/news.html"')
        content = content.replace('href="press-releases.html"', f'href="{lang}/press-releases.html"')

    # Fix script src missing quotes
    content = content.replace(
        '<script src=https://cdn.userway.org/widget.js',
        '<script src="https://cdn.userway.org/widget.js"',
    )

    # Add map embed to contact pages
    if html_path.name == "contact-us.html" and "contact_map_wrap" not in content:
        marker = "<!-- Contact Info End -->"
        if marker in content:
            map_html = MAP_SECTION_AR if "ar" in rel_parts else MAP_SECTION_EN
            content = content.replace(marker, marker + map_html)

    # Inject site-fixes.css after maindc50.css
    css_tag = SITE_FIXES_CSS.format(prefix=prefix)
    if "site-fixes.css" not in content:
        content = re.sub(
            r'(<link href="[^"]*maindc50\.css[^"]*" rel="stylesheet">)',
            r"\1\n    " + css_tag,
            content,
            count=1,
        )

    # Inject site-fixes.js before appdc50.js so image paths are patched first
    js_tag = SITE_FIXES_JS.format(prefix=prefix)
    if "site-fixes.js" not in content:
        content = re.sub(
            r'(<script defer src="[^"]*appdc50\.js[^"]*"></script>)',
            js_tag + "\n    " + r"\1",
            content,
            count=1,
        )

    content = localize_remote_data_src(content)

    if content != original:
        html_path.write_text(content, encoding="utf-8")
        return True
    return False


def fix_root_redirects() -> None:
    for name, target in [("news.html", "ar/news.html"), ("press-releases.html", "ar/press-releases.html")]:
        path = ROOT / name
        path.write_text(
            f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta http-equiv="refresh" content="0; url={target}">
    <title>Redirecting...</title>
    <script>window.location.replace("{target}");</script>
</head>
<body>
    <p>Redirecting to <a href="{target}">{target}</a>...</p>
</body>
</html>
""",
            encoding="utf-8",
        )


def main() -> int:
    args = sys.argv[1:]
    skip_download = "--skip-download" in args

    sys.stdout.reconfigure(line_buffering=True)

    print("=== Fixing root redirects ===")
    fix_root_redirects()

    print("=== Patching HTML files ===")
    patched = 0
    for html_file in ROOT.rglob("*.html"):
        if "scripts" in html_file.parts:
            continue
        if patch_html_file(html_file):
            patched += 1
    print(f"  Patched {patched} HTML files")

    if not skip_download:
        print("=== Collecting image URLs ===")
        urls = collect_image_urls()
        print(f"  Found {len(urls)} unique storage images")

        print("=== Downloading extra assets ===")
        download_extra_assets()

        print("=== Downloading storage images (this may take a while) ===")
        downloaded, failed = download_images(urls)
        print(f"  Done: downloaded={downloaded}, failed={failed}, skipped={len(urls) - downloaded - failed}")
    else:
        print("=== Skipping image download ===")

    print("=== Complete ===")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
