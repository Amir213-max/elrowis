# -*- coding: utf-8 -*-
"""Fix menu order across all Arabic pages to match homepage order."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
AR_DIR = ROOT / "ar"

# Fix: change href="our-business.html#infrastructure" to href="our-business.html#operations" when the text is "إدارة المرافق"
def fix_file(file_path: Path):
    content = file_path.read_text(encoding="utf-8")
    
    # Pattern to match: href="our-business.html#infrastructure" or href="../our-business.html#infrastructure" followed by "إدارة المرافق"
    # We need to change the href to #operations
    pattern = r'(href=["\'](?:\.\./)?our-business\.html#)infrastructure(["\'].*?>\s*)إدارة المرافق'
    replacement = r'\1operations\2إدارة المرافق'
    
    new_content = re.sub(pattern, replacement, content)
    
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
