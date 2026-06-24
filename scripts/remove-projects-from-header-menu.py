# -*- coding: utf-8 -*-
"""Remove 'مشاريعنا' from the 'أعمالنا' dropdown menu in header navigation."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
AR_DIR = ROOT / "ar"

def fix_file(file_path: Path):
    content = file_path.read_text(encoding="utf-8")
    
    # Pattern to match the "مشاريعنا" menu item in the header under "أعمالنا"
    # Match the entire li element containing "مشاريعنا"
    pattern = r'\s+<li class="">\s+<a href="(?:\.\./)?our-projects\.html"[^>]*>\s+مشاريعنا\s+</a>\s+</li>\s+'
    
    new_content = re.sub(pattern, '', content, flags=re.DOTALL)
    
    if new_content != content:
        file_path.write_text(new_content, encoding="utf-8")
        print(f"Fixed: {file_path}")
        return True
    return False

def main():
    fixed_count = 0
    for html_file in AR_DIR.rglob("*.html"):
        if fix_file(html_file):
            fixed_count += 1
    
    print(f"\nTotal files fixed: {fixed_count}")

if __name__ == "__main__":
    main()
