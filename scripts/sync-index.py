#!/usr/bin/env python3
"""Copy ar.html to index.html (Arabic default homepage)."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AR = ROOT / "ar.html"
INDEX = ROOT / "index.html"


def main() -> int:
    content = AR.read_text(encoding="utf-8")
    content = content.replace('rel="canonical" href="ar.html"', 'rel="canonical" href="index.html"')
    content = content.replace('hreflang="ar" href="ar.html"', 'hreflang="ar" href="index.html"')
    content = content.replace('hreflang="x-default" href="ar.html"', 'hreflang="x-default" href="index.html"')
    content = content.replace('href="ar.html" aria-label="الرويس"', 'href="index.html" aria-label="الرويس"')
    INDEX.write_text(content, encoding="utf-8")
    print(f"Synced {AR.name} -> {INDEX.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
