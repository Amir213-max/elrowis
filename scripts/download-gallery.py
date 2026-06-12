#!/usr/bin/env python3
"""Download all gallery-images referenced in HTML."""

import re
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE = "https://nesmapartners.com/"

urls: set[str] = set()
for html in ROOT.rglob("*.html"):
    if "scripts" in html.parts:
        continue
    text = html.read_text(encoding="utf-8", errors="ignore")
    for match in re.findall(r'["\'](/storage/gallery-images/[^"\']+)["\']', text):
        urls.add(match.lstrip("/"))

print(f"Found {len(urls)} gallery images")
ok = fail = 0
for rel in sorted(urls):
    dest = ROOT / rel.replace("/", "\\" if False else "/")
    if dest.exists() and dest.stat().st_size > 0:
        ok += 1
        continue
    dest.parent.mkdir(parents=True, exist_ok=True)
    try:
        urllib.request.urlretrieve(BASE + rel, dest)
        print(f"  downloaded {rel} ({dest.stat().st_size} bytes)")
        ok += 1
    except Exception as exc:
        print(f"  FAILED {rel}: {exc}")
        fail += 1

print(f"Done: {ok} ok, {fail} failed")
