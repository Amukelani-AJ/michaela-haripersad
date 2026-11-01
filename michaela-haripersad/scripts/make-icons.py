#!/usr/bin/env python3
# Written by Kone Tshivhinda (Claude Sonnet 5.5) on 2026-10-15 - Builds the MH monogram favicon set from the site's own Playfair Display font.
"""Generate site/favicon.svg, site/favicon-32.png and site/apple-touch-icon.png.

The "MH" letters are converted to vector paths (so the SVG does not depend on an installed font)
and drawn on the same warm gradient used by the logo in the page header.

Needs (only when you want to regenerate the icons - the site itself has no build step):
    pip install fonttools brotli playwright   (and: playwright install chromium)

Run from the repository root:
    python3 scripts/make-icons.py
"""
from __future__ import annotations

import pathlib
import sys

from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
FONT = SITE / "assets" / "fonts" / "playfair-display-latin-700-normal.woff2"

INK = "#14172e"
GRADIENT = (("0", "#ff4d8d"), ("0.52", "#ff7b54"), ("1", "#ffc247"))


def monogram_path(text: str, box: float, width_ratio: float) -> str:
    """Return one SVG path 'd' string for `text`, centred in a square of side `box`."""
    font = TTFont(FONT)
    glyphs = font.getGlyphSet()
    cmap = font.getBestCmap()
    names = [cmap[ord(ch)] for ch in text]
    advances = [font["hmtx"][name][0] for name in names]

    # Ink bounds of the whole run, in font units, so the letters can be optically centred.
    x_cursor, left, right, top, bottom = 0, None, None, None, None
    for name, adv in zip(names, advances):
        pen = BoundsPen(glyphs)
        glyphs[name].draw(pen)
        x0, y0, x1, y1 = pen.bounds
        left = x0 + x_cursor if left is None else min(left, x0 + x_cursor)
        right = x1 + x_cursor if right is None else max(right, x1 + x_cursor)
        top = y1 if top is None else max(top, y1)
        bottom = y0 if bottom is None else min(bottom, y0)
        x_cursor += adv

    scale = (box * width_ratio) / (right - left)
    tx = (box - (right - left) * scale) / 2 - left * scale
    ty = (box + (top - bottom) * scale) / 2 + bottom * scale  # SVG y grows downwards

    commands = []
    x_cursor = 0
    for name, adv in zip(names, advances):
        svg_pen = SVGPathPen(glyphs, ntos=lambda v: f"{v:.2f}".rstrip("0").rstrip("."))
        transform = TransformPen(svg_pen, (scale, 0, 0, -scale, tx + x_cursor * scale, ty))
        glyphs[name].draw(transform)
        commands.append(svg_pen.getCommands())
        x_cursor += adv
    return " ".join(commands)


def icon_svg(rounded: bool, width_ratio: float) -> str:
    stops = "".join(f'<stop offset="{o}" stop-color="{c}"/>' for o, c in GRADIENT)
    radius = ' rx="15"' if rounded else ""
    d = monogram_path("MH", 64, width_ratio)
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="64" height="64" role="img" aria-label="MH monogram">'
        f'<defs><linearGradient id="g" x1="0.08" y1="0" x2="0.92" y2="1">{stops}</linearGradient></defs>'
        f'<rect width="64" height="64"{radius} fill="url(#g)"/>'
        f'<path fill="{INK}" d="{d}"/>'
        "</svg>\n"
    )


def render_png(svg: str, size: int, destination: pathlib.Path, transparent: bool) -> None:
    from playwright.sync_api import sync_playwright

    html = f"<!doctype html><meta charset=utf-8><style>html,body{{margin:0;background:transparent}}svg{{display:block;width:{size}px;height:{size}px}}</style>{svg}"
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": size, "height": size}, device_scale_factor=1)
        page.set_content(html)
        page.screenshot(path=str(destination), omit_background=transparent, clip={"x": 0, "y": 0, "width": size, "height": size})
        browser.close()


def main() -> int:
    if not FONT.exists():
        print(f"Font not found: {FONT}", file=sys.stderr)
        return 1
    rounded = icon_svg(rounded=True, width_ratio=0.60)
    (SITE / "favicon.svg").write_text(rounded, encoding="utf-8")
    render_png(rounded, 32, SITE / "favicon-32.png", transparent=True)
    # iOS applies its own rounded mask, so the touch icon is a full-bleed square.
    render_png(icon_svg(rounded=False, width_ratio=0.56), 180, SITE / "apple-touch-icon.png", transparent=False)
    print("Wrote favicon.svg, favicon-32.png, apple-touch-icon.png")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
