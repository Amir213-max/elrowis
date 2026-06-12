import re, os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
pattern = re.compile(r'data-src=["\']([^"\']+)["\']')
urls = set()
for f in ROOT.rglob("*.html"):
    if "scripts" in f.parts:
        continue
    c = f.read_text(encoding="utf-8", errors="ignore")
    for m in pattern.finditer(c):
        u = m.group(1)
        if u.startswith("https://nesmapartners.com/"):
            u = u.replace("https://nesmapartners.com/", "")
        for p in ("../../", "../", "./"):
            if u.startswith(p + "storage/"):
                u = u[len(p):]
        if u.startswith("storage/"):
            urls.add(u)

missing = [u for u in urls if not (ROOT / u.replace("/", os.sep)).exists()]
print(f"Total: {len(urls)}, existing: {len(urls)-len(missing)}, missing: {len(missing)}")
if missing[:5]:
    print("Sample missing:", missing[:5])
