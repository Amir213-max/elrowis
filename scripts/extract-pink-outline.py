#!/usr/bin/env python3
"""Derive Ra clip path from user pink reference outline."""

from __future__ import annotations

from collections import deque
from pathlib import Path

from PIL import Image, ImageFilter

SRC = (
    r"C:\Users\LOQ\.cursor\projects\d-nesmapartners-com\assets\c__Users_LOQ_AppData_Roaming_Cursor_User_workspaceStorage_22f67f6b0351547decc5d81fed4c66fc_images_image-56b718a1-3ce8-4d51-bcea-c4dde92d9e6b.png"
)
ROOT = Path(__file__).resolve().parent.parent


def is_pink(r: int, g: int, b: int) -> bool:
    return r > 150 and b > 90 and g < 110 and r > b


def is_gray_bg(r: int, g: int, b: int) -> bool:
    return abs(r - g) < 15 and abs(g - b) < 15 and 175 < r < 220


def flood_outside(blocked: list[list[bool]], w: int, h: int) -> list[list[bool]]:
    outside = [[False] * w for _ in range(h)]
    q: deque[tuple[int, int]] = deque()
    for x in range(w):
        for y in (0, h - 1):
            if not blocked[y][x]:
                outside[y][x] = True
                q.append((x, y))
    for y in range(h):
        for x in (0, w - 1):
            if not blocked[y][x] and not outside[y][x]:
                outside[y][x] = True
                q.append((x, y))
    while q:
        x, y = q.popleft()
        for nx, ny in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
            if 0 <= nx < w and 0 <= ny < h and not blocked[ny][nx] and not outside[ny][nx]:
                outside[ny][nx] = True
                q.append((nx, ny))
    return outside


def simplify_row_profile(
    x0: int, y0: int, tw: int, th: int, inside: list[list[bool]], w: int, h: int
) -> list[tuple[float, float]]:
    def n(x: float, y: float) -> tuple[float, float]:
        return round((x - x0) / tw * 100, 2), round((y - y0) / th * 97, 2)

    # collect boundary points clockwise
    points: list[tuple[float, float]] = []

    # top to bottom: left boundary
    for y in range(y0, y1 + 1):
        row = [x for x in range(x0, x1 + 1) if inside[y][x]]
        if row:
            points.append(n(row[0], y))

    # bottom to top: right boundary
    for y in range(y1, y0 - 1, -1):
        row = [x for x in range(x0, x1 + 1) if inside[y][x]]
        if row:
            points.append(n(row[-1], y))

    return points


def points_to_path(pts: list[tuple[float, float]]) -> str:
    if not pts:
        return ""
    parts = [f"M{pts[0][0]} {pts[0][1]}"]
    for x, y in pts[1:]:
        parts.append(f"L{x} {y}")
    parts.append("Z")
    return "".join(parts)


def scale_to_mask(d: str) -> str:
    import re

    sx = (1150.07 - 769.93) / 100
    sy = (818.68 - 261.32) / 97
    ox, oy = 769.93, 172.72
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
            out.append(f"{ox + x * sx:.2f}")
            out.append(f"{oy + y * sy:.2f}")
            i += 2
        elif cmd == "Q":
            vals = list(map(float, tokens[i : i + 4]))
            for j in range(0, 4, 2):
                out.append(f"{ox + vals[j] * sx:.2f}")
                out.append(f"{oy + vals[j + 1] * sy:.2f}")
            i += 4
    return " ".join(out)


def main() -> None:
    img = Image.open(SRC).convert("RGB")
    w, h = img.size
    px = img.load()

    pink = Image.new("L", (w, h), 0)
    pp = pink.load()
    for y in range(h):
        for x in range(w):
            if is_pink(*px[x, y]):
                pp[x, y] = 255

    pink = pink.filter(ImageFilter.MaxFilter(7)).filter(ImageFilter.MaxFilter(5))
    pp = pink.load()
    blocked = [[pp[x, y] > 0 for x in range(w)] for y in range(h)]

    outside = flood_outside(blocked, w, h)
    inside = [[not blocked[y][x] and not outside[y][x] for x in range(w)] for y in range(h)]

    xs = [x for y in range(h) for x in range(w) if inside[y][x]]
    ys = [y for y in range(h) for x in range(w) if inside[y][x]]
    if not xs:
        raise SystemExit("No interior region found")

    global y0, y1
    x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
    tw, th = x1 - x0, y1 - y0
    print(f"inside bbox: {tw}x{th}")

    def n(x: float, y: float) -> tuple[float, float]:
        return round((x - x0) / tw * 100, 2), round((y - y0) / th * 97, 2)

    # print profile
    for y in range(y0, y1 + 1, max(1, th // 20)):
        row = [x for x in range(x0, x1 + 1) if inside[y][x]]
        if row:
            print(
                f"y={n(0,y)[1]:5.1f} left={n(row[0],y)[0]:5.1f} right={n(row[-1],y)[0]:5.1f}"
            )

    # key points for smooth Ra path
    left_edge = []
    right_edge = []
    for y in range(y0, y1 + 1):
        row = [x for x in range(x0, x1 + 1) if inside[y][x]]
        if row:
            left_edge.append((row[0], y))
            right_edge.append((row[-1], y))

    bl = n(left_edge[-1][0], left_edge[-1][1])
    # find stem x (most common right x in middle-lower)
    mid = (y0 + y1) // 2
    stem_x = max(x for x, y in right_edge if y > mid)
    stem_top_y = min(y for x, y in right_edge if x == stem_x)
    stem_bot_y = max(y for x, y in right_edge if x == stem_x)

    top_y = y0
    tl = n(left_edge[0][0], top_y)
    tr = n(stem_x, top_y)

    # left curve peak
    bulge = max(left_edge[: len(left_edge) // 2], key=lambda t: t[0])
    p_bulge = n(bulge[0], bulge[1])

    # left straight tail bottom
    tail_top_y = max(y for x, y in left_edge if x <= left_edge[-1][0] + 2)
    for y in range(y1, y0, -1):
        row = [x for x in range(x0, x1 + 1) if inside[y][x]]
        if row and row[0] <= left_edge[-1][0] + 3:
            tail_top_y = y
            break

    p_tail = n(left_edge[-1][0], tail_top_y)
    p_stem_top = n(stem_x, stem_top_y)
    p_stem_bot = n(stem_x, stem_bot_y)

    path = (
        f"M{bl[0]} {bl[1]}"
        f"L{p_tail[0]} {p_tail[1]}"
        f"Q{p_bulge[0]} {p_bulge[1]} {tl[0]} {tl[1]}"
        f"L{p_stem_top[0]} {p_stem_top[1]}"
        f"L{p_stem_bot[0]} {p_stem_bot[1]}"
        f"L{bl[0]} {bl[1]}Z"
    )
    print("\npath:", path)
    print("\nmask:", scale_to_path(path))

    (ROOT / "images" / "logo-hole-path.svg").write_text(
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 97" fill="none">\n'
        f'  <path d="{path}" fill="#003d53"/>\n'
        "</svg>\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
