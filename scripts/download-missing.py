#!/usr/bin/env python3
import importlib.util
import sys

spec = importlib.util.spec_from_file_location(
    "fix_site", r"d:\nesmapartners.com\nesmapartners.com\scripts\fix-site.py"
)
fix_site = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fix_site)

urls = fix_site.collect_image_urls()
missing = [
    u
    for u in urls
    if not (fix_site.ROOT / u.replace("/", __import__("os").sep)).exists()
]
print(f"Downloading {len(missing)} missing images...", flush=True)
downloaded, failed = fix_site.download_images(set(missing))
print(f"Done: downloaded={downloaded}, failed={failed}", flush=True)
