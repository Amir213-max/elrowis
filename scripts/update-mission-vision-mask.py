#!/usr/bin/env python3
"""Mission-vision mask — clean Ra shape, no corner bulges."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ABOUT = ROOT / "ar" / "about-us.html"
HOLE_SVG = ROOT / "images" / "logo-hole-path.svg"

# Clean polygon — Q control points stay on edges (no outward bulges)
RA_PATH = (
    "M8.5 90.5"
    "L33.5 90.5"
    "L96.5 71.5"
    "Q96.5 69.5 96.5 67.5"
    "L96.5 10.5"
    "Q96.5 8.5 94.5 8.5"
    "L53.5 20"
    "L53.5 56"
    "L8.5 90.5"
    "Z"
)

MASK_CENTER_X = 960.0
MASK_WIDTH = (1150.07 - 769.93) * 1.08
OX = MASK_CENTER_X - MASK_WIDTH / 2
SX = MASK_WIDTH / 100
SY = (818.68 - 261.32) / 97
OY = 172.72


def scale_path(d: str) -> str:
    tokens = re.findall(r"[MLQZ]|[-+]?(?:\d*\.\d+|\d+)", d)
    out: list[str] = []
    i = 0
    cmd = "M"
    while i < len(tokens):
        t = tokens[i]
        if t in "MLQZ":
            cmd = t
            out.append(t)
            i += 1
            continue
        if cmd in "ML":
            x, y = float(tokens[i]), float(tokens[i + 1])
            out.append(f"{OX + x * SX:.2f}")
            out.append(f"{OY + y * SY:.2f}")
            i += 2
        elif cmd == "Q":
            vals = list(map(float, tokens[i : i + 4]))
            for j in range(0, 4, 2):
                out.append(f"{OX + vals[j] * SX:.2f}")
                out.append(f"{OY + vals[j + 1] * SY:.2f}")
            i += 4
    return " ".join(out)


def main() -> None:
    inner = scale_path(RA_PATH)
    mask_d = f"M1920 0H0V1080H1920V0Z {inner}"

    HOLE_SVG.write_text(
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 97" fill="none">\n'
        f'  <path d="{RA_PATH}" fill="#003d53"/>\n'
        "</svg>\n",
        encoding="utf-8",
    )

    html = ABOUT.read_text(encoding="utf-8")
    pattern = re.compile(
        r'(<path fill-rule="evenodd" clip-rule="evenodd" d=")M1920 0H0V1080H1920V0Z[^"]+(" fill="#d5d7d7"/>)'
    )
    if not pattern.search(html):
        raise SystemExit("Mask path not found")
    ABOUT.write_text(pattern.sub(rf"\1{mask_d}\2", html, count=1), encoding="utf-8")
    print("OK")


if __name__ == "__main__":
    main()
