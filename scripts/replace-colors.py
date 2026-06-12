#!/usr/bin/env python3
"""Replace orange → navy (#003d53) and green → gray (#d5d7d7) across the site."""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EXTENSIONS = {".html", ".css", ".js", ".svg"}

# (pattern, replacement) — order matters for specific patterns first
REPLACEMENTS = [
    # Orange → Navy
    (re.compile(r"#FF801E", re.I), "#003d53"),
    (re.compile(r"#FB801F", re.I), "#003d53"),
    (re.compile(r"#DD6305", re.I), "#003d53"),
    (re.compile(r"0xDD6305", re.I), "0x003d53"),
    # Green → Gray
    (re.compile(r"#19312F", re.I), "#d5d7d7"),
    (re.compile(r"#21403D", re.I), "#d5d7d7"),
    (re.compile(r"#112624", re.I), "#d5d7d7"),
    (re.compile(r"rgba\(33,\s*64,\s*61,", re.I), "rgba(213, 215, 215,"),
    (re.compile(r"rgba\(17,\s*38,\s*36,", re.I), "rgba(213, 215, 215,"),
    # Green-tinted text gray → navy-tinted (was rgb(33 64 61))
    (re.compile(r"rgb\(33\s+64\s+61\s*/", re.I), "rgb(0 61 83 /"),
]

SKIP_DIRS = {"scripts", "draco-master", "node_modules"}


def should_process(path: Path) -> bool:
    if path.suffix.lower() not in EXTENSIONS:
        return False
    return not any(part in SKIP_DIRS for part in path.parts)


def main() -> None:
    changed = 0
    for file_path in ROOT.rglob("*"):
        if not file_path.is_file() or not should_process(file_path):
            continue
        try:
            content = file_path.read_text(encoding="utf-8")
        except Exception:
            continue
        original = content
        for pattern, repl in REPLACEMENTS:
            content = pattern.sub(repl, content)
        if content != original:
            file_path.write_text(content, encoding="utf-8")
            changed += 1
    print(f"Updated {changed} files")


if __name__ == "__main__":
    main()
