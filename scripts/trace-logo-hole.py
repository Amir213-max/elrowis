#!/usr/bin/env python3
"""Extract precise Ra hollow path from nav-logo-icon.png."""

from __future__ import annotations

from PIL import Image

SRC = r"d:\nesmapartners.com\nesmapartners.com\images\nav-logo-icon.png"
OUT_SVG = r"d:\nesmapartners.com\nesmapartners.com\images\logo-hole-path.svg"


def is_teal(r: int, g: int, b: int, a: int) -> bool:
    if a < 128:
        return False
    return r < 40 and 45 < g < 90 and 60 < b < 110


def main() -> None:
    img = Image.open(SRC).convert("RGBA")
    px = img.load()
    w, h = img.size

    teal = [[is_teal(*px[x, y]) for x in range(w)] for y in range(h)]
    xs = [x for y in range(h) for x in range(w) if teal[y][x]]
    ys = [y for y in range(h) for x in range(w) if teal[y][x]]
    tx0, tx1, ty0, ty1 = min(xs), max(xs), min(ys), max(ys)
    tw, th = tx1 - tx0, ty1 - ty0

    hole = [
        [not teal[y][x] for x in range(w)]
        for y in range(h)
    ]

    def n(x: float, y: float) -> tuple[float, float]:
        return round((x - tx0) / tw * 100, 3), round((y - ty0) / th * 97, 3)

    def left_at(y: int) -> int | None:
        row = [x for x in range(tx0, tx1 + 1) if hole[y][x]]
        return row[0] if row else None

    def right_at(y: int) -> int | None:
        row = [x for x in range(tx0, tx1 + 1) if hole[y][x]]
        return row[-1] if row else None

    y_top = ty0
    y_bot = ty1
    x_bl = left_at(y_bot)
    x_tl = left_at(y_top)

    # right stem x on lower body
    stem_x = max(right_at(y) for y in range(ty0 + th // 3, ty1 + 1) if right_at(y))

    # where flat top ends (right edge drops)
    y_flat = y_top
    for y in range(y_top, ty0 + th // 2):
        if right_at(y) and right_at(y) < stem_x - 5:
            y_flat = y
            break

    # left side before bulge: straight segment from bottom-left upward
    y_left_straight = y_bot
    for y in range(y_bot, y_top, -1):
        lx = left_at(y)
        if lx is not None and lx <= tx0 + tw * 0.02:
            y_left_straight = y
        else:
            break

    # top-right rounded corner area
    y_tr = y_top + int(th * 0.05)
    x_tr = right_at(y_top)

    # bulge control from sampled max left in upper-mid
    best = (0, y_top)
    for y in range(ty0, ty0 + th // 2):
        lx = left_at(y)
        if lx is not None and lx > best[0]:
            best = (lx, y)
    x_bulge, y_bulge = best

    # stem bottom y
    y_stem = max(y for y in range(ty0, ty1 + 1) if right_at(y) == stem_x)

    p_bl = n(x_bl, y_bot)
    p_ls = n(x_bl, y_left_straight)
    p_bulge = n(x_bulge, y_bulge)
    p_tl = n(x_tl, y_top)
    p_tr = n(x_tr, y_top)
    p_trc = n(stem_x, y_tr)
    p_stem = n(stem_x, y_stem)

    path = (
        f"M{p_bl[0]} {p_bl[1]}"
        f"L{p_ls[0]} {p_ls[1]}"
        f"Q{p_bulge[0]} {p_bulge[1]} {p_tl[0]} {p_tl[1]}"
        f"L{p_tr[0]} {p_tr[1]}"
        f"Q{p_tr[0]} {p_tr[1]} {p_trc[0]} {p_trc[1]}"
        f"L{p_stem[0]} {p_stem[1]}"
        f"L{p_bl[0]} {p_bl[1]}Z"
    )

    print("points:")
    print(" bl", p_bl, "ls", p_ls, "bulge", p_bulge, "tl", p_tl, "tr", p_tr, "trc", p_trc, "stem", p_stem)
    print("path:", path)

    svg = (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 97" fill="none">\n'
        f'  <path d="{path}" fill="#003d53"/>\n'
        "</svg>\n"
    )
    with open(OUT_SVG, "w", encoding="utf-8") as f:
        f.write(svg)

    # scale to mission-vision mask (uniform, same placement as before)
    sx = (1150.07 - 769.93) / 100
    sy = (818.68 - 261.32) / 97
    ox, oy = 769.93, 172.72

    def sc(nx: float, ny: float) -> tuple[float, float]:
        return round(ox + nx * sx, 2), round(oy + ny * sy, 2)

    def pt(nx: float, ny: float) -> str:
        x, y = sc(nx, ny)
        return f"{x} {y}"

    mask_path = (
        f"M{pt(*p_bl)}"
        f"L{pt(*p_ls)}"
        f"Q{pt(*p_bulge)} {pt(*p_tl)}"
        f"L{pt(*p_tr)}"
        f"Q{pt(*p_tr)} {pt(*p_trc)}"
        f"L{pt(*p_stem)}"
        f"L{pt(*p_bl)}Z"
    )
    print("\nmask inner:", mask_path)
    print("\nfull evenodd d=")
    print(f"M1920 0H0V1080H1920V0Z{mask_path}")


if __name__ == "__main__":
    main()
