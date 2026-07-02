#!/usr/bin/env python3
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parent.parent
ARCH = ROOT / "_archived" / "nesma-partners"
ARCH.mkdir(parents=True, exist_ok=True)

for lang, dest in (("ar", "../index.html"), ("en", "../en.html")):
    src = ROOT / lang / "nesma-partners.html"
    if src.is_file() and src.stat().st_size > 5000:
        shutil.copy2(src, ARCH / f"{lang}.html")
    html_lang = "en" if lang == "en" else "ar"
    direction = "ltr" if lang == "en" else "rtl"
    stub = f"""<!DOCTYPE html>
<html lang="{html_lang}" dir="{direction}">
<head>
<meta charset="utf-8">
<meta name="robots" content="noindex, nofollow">
<meta http-equiv="refresh" content="0; url={dest}">
<script>location.replace("{dest}");</script>
<title>Alruwais</title>
</head>
<body></body>
</html>
"""
    src.write_text(stub, encoding="utf-8")

print("nesma-partners archived and redirected")
