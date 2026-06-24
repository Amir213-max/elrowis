# -*- coding: utf-8 -*-
"""Fix header navigation menu across all Arabic pages to match homepage order."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
AR_DIR = ROOT / "ar"

def fix_file(file_path: Path):
    content = file_path.read_text(encoding="utf-8")
    
    # Check if this is an article file (in ar/article/ subdirectory)
    is_article = 'article' in str(file_path)
    
    # Pattern to match the old menu items in header navigation
    # We need to replace the entire block of menu items after "نظرة عامة"
    
    # Find the menu_sub div with أعمالنا
    pattern = r'(نظرة عامة\s*</a>\s*</li>\s*).*?(<li class="">\s*<a href="(?:\.\./)?our-projects\.html")'
    
    # The new menu items - use relative path for article files
    if is_article:
        new_menu = r'''\1                                                                                                                                <li class="has_indent">
                                                <a href="../our-business.html#building-construction"
                                                                                                      >
                                                    التشييد والبناء
                                                </a>
                                            </li>
                                                                                                                                <li class="has_indent">
                                                <a href="../our-business.html#operations"
                                                                                                      >
                                                    إدارة المرافق
                                                </a>
                                            </li>
                                                                                                                                <li class="has_indent">
                                                <a href="../our-business.html#resources"
                                                                                                      >
                                                    مشاريع تهيئة بيئة العمل
                                                </a>
                                            </li>
                                                                                                                                <li class="has_indent">
                                                <a href="../our-business.html#infrastructure"
                                                                                                      >
                                                    بنية تحتية
                                                </a>
                                            </li>
                                            \2'''
    else:
        new_menu = r'''\1                                                                                                                                <li class="has_indent">
                                                <a href="our-business.html#building-construction"
                                                                                                      >
                                                    التشييد والبناء
                                                </a>
                                            </li>
                                                                                                                                <li class="has_indent">
                                                <a href="our-business.html#operations"
                                                                                                      >
                                                    إدارة المرافق
                                                </a>
                                            </li>
                                                                                                                                <li class="has_indent">
                                                <a href="our-business.html#resources"
                                                                                                      >
                                                    مشاريع تهيئة بيئة العمل
                                                </a>
                                            </li>
                                                                                                                                <li class="has_indent">
                                                <a href="our-business.html#infrastructure"
                                                                                                      >
                                                    بنية تحتية
                                                </a>
                                            </li>
                                            \2'''
    
    new_content = re.sub(pattern, new_menu, content, flags=re.DOTALL)
    
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
