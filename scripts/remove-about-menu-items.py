import re
from pathlib import Path

root = Path(__file__).resolve().parent.parent
pattern = re.compile(
    r'\s*<li class="">\s*'
    r'<a href="[^"]*#(?:corporate-governance|code-of-conduct|our-ecosystem)"'
    r'[^>]*>\s*'
    r'(?:الحوكمة المؤسسية|مدونة قواعد السلوك|منظومتنا)\s*'
    r'</a>\s*'
    r'</li>',
    re.DOTALL,
)

updated = 0
for f in list(root.glob("ar.html")) + list((root / "ar").rglob("*.html")):
    text = f.read_text(encoding="utf-8")
    new_text, n = pattern.subn("", text)
    if n:
        f.write_text(new_text, encoding="utf-8")
        updated += 1
        print(f"{f.relative_to(root)}: removed {n} items")

print("---")
print("files updated:", updated)

remaining = sum(
    1
    for f in list(root.glob("ar.html")) + list((root / "ar").rglob("*.html"))
    if "الحوكمة المؤسسية" in f.read_text(encoding="utf-8")
)
print("files still containing الحوكمة المؤسسية:", remaining)
