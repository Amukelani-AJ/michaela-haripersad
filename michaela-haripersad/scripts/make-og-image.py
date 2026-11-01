#!/usr/bin/env python3
# Written by Kone Tshivhinda (Claude Sonnet 5.5) on 2026-10-15 - Renders the 1200x630 link-preview image from scripts/og-image/template.html.
"""Render site/assets/img/og-image.jpg (the picture shown when the site link is shared).

Edit scripts/og-image/template.html, then run from the repository root:
    python3 scripts/make-og-image.py

Needs: pip install playwright pillow   (and: playwright install chromium)
"""
from __future__ import annotations

import io
import pathlib

from PIL import Image
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
TEMPLATE = ROOT / "scripts" / "og-image" / "template.html"
OUTPUT = ROOT / "site" / "assets" / "img" / "og-image.jpg"


def main() -> None:
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1200, "height": 630}, device_scale_factor=1)
        page.goto(TEMPLATE.as_uri())
        page.wait_for_load_state("networkidle")
        page.evaluate("document.fonts.ready")
        page.wait_for_timeout(400)
        png = page.screenshot(clip={"x": 0, "y": 0, "width": 1200, "height": 630})
        browser.close()
    image = Image.open(io.BytesIO(png)).convert("RGB")
    image.save(OUTPUT, "JPEG", quality=88, optimize=True, progressive=True)
    print(f"Wrote {OUTPUT.relative_to(ROOT)} ({OUTPUT.stat().st_size // 1024} KB, {image.size[0]}x{image.size[1]})")


if __name__ == "__main__":
    main()
