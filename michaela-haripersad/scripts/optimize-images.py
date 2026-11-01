#!/usr/bin/env python3
# Written by Kone Tshivhinda (Claude Sonnet 5.5) on 2026-10-15 - Image optimiser for the portfolio photos.
# Written by Kone Tshivhinda (Claude Sonnet 5.5) on 2026-10-15 - P4: reads both photo batches, adds four photos, retires two look-alikes.
"""Turn original photos into web-ready WebP files.

What it does
  * re-encodes every photo as WebP at several widths (responsive srcset),
  * strips ALL embedded metadata (EXIF, GPS, camera data) by re-encoding from pixels,
  * writes site/assets/img/manifest.json with sizes and an average colour per photo
    (used as the image placeholder colour while the photo loads).

Usage
  python3 scripts/optimize-images.py --src <folder with the original photos> --out site/assets/img

Originals are never copied into the repository (see .gitignore: originals/).
To add a photo: add one line to PHOTOS below, run the script, then reference it in site/index.html.

The photos arrived in two batches that both use the file names Media.jpg, Media (1).jpg, ...
so the paths below are relative to --src and the first batch sits in the "Mickys" sub-folder
(on the PC: ...\\My CV\\Micky = second batch, ...\\My CV\\Micky\\Mickys = first batch).
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from PIL import Image, ImageOps

# slug -> (original file path relative to --src, widths to export).
# The largest width should be <= the original width.
PHOTOS: dict[str, tuple[str, list[int]]] = {
    # First batch (sub-folder "Mickys") - the four photos kept after the photo refresh.
    "stage-performance": ("Mickys/Media.jpg", [480, 800, 1200]),
    "studio-portrait-one": ("Mickys/Media (1).jpg", [480, 800, 1200]),
    "office-seated": ("Mickys/Media (3).jpg", [480, 800, 1068]),
    "office-smile-portrait": ("Mickys/Media (5).jpg", [480, 800, 1068]),
    # Second batch (folder root).
    "editorial-suit": ("Media (1).jpg", [480, 800, 1034]),
    "street-golden-hour": ("Media (2).jpg", [480, 800, 1066]),
    "studio-sunglasses": ("Media (5).jpg", [480, 800, 1200]),
    # Small on purpose: the original is only 360 px wide, so it is shown as a thumbnail in Credentials.
    "graduation-portrait": ("Media (3).jpg", [180, 360]),
}
# Retired in the photo refresh (look-alikes of kept photos): "office-smile-wide" and "studio-portrait-two".

# Square crops used for small circular frames: slug -> (source slug, crop box in original pixels, output size)
CROPS: dict[str, tuple[str, tuple[int, int, int, int], int]] = {
    "stage-face": ("stage-performance", (300, 150, 840, 690), 360),
}

QUALITY = 80


def average_colour(img: Image.Image) -> str:
    r, g, b = img.convert("RGB").resize((1, 1), Image.LANCZOS).getpixel((0, 0))
    return f"#{r:02x}{g:02x}{b:02x}"


def save_webp(img: Image.Image, path: Path) -> int:
    # Re-encoding from pixels drops EXIF/GPS/ICC; sRGB is assumed for web delivery.
    img.save(path, "WEBP", quality=QUALITY, method=6)
    return path.stat().st_size


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--src", required=True, type=Path, help="folder holding the original photos")
    ap.add_argument("--out", required=True, type=Path, help="output folder, normally site/assets/img")
    args = ap.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)

    manifest: dict[str, dict] = {}
    originals: dict[str, Image.Image] = {}

    for slug, (name, widths) in PHOTOS.items():
        im = ImageOps.exif_transpose(Image.open(args.src / name)).convert("RGB")
        originals[slug] = im
        w0, h0 = im.size
        files = []
        for w in widths:
            w = min(w, w0)
            h = round(h0 * w / w0)
            out = args.out / f"{slug}-{w}.webp"
            size = save_webp(im.resize((w, h), Image.LANCZOS) if w != w0 else im, out)
            files.append({"file": out.name, "width": w, "height": h, "bytes": size})
        manifest[slug] = {"width": w0, "height": h0, "colour": average_colour(im), "files": files}

    for slug, (source, box, size) in CROPS.items():
        crop = originals[source].crop(box).resize((size, size), Image.LANCZOS)
        out = args.out / f"{slug}-{size}.webp"
        nbytes = save_webp(crop, out)
        manifest[slug] = {"width": size, "height": size, "colour": average_colour(crop),
                          "files": [{"file": out.name, "width": size, "height": size, "bytes": nbytes}]}

    (args.out / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    total = sum(f["bytes"] for m in manifest.values() for f in m["files"])
    print(f"wrote {sum(len(m['files']) for m in manifest.values())} files, {total / 1024:.0f} KB total")
    for slug, m in manifest.items():
        sizes = ", ".join(f"{f['width']}w={f['bytes'] // 1024}KB" for f in m["files"])
        print(f"  {slug:24s} {m['colour']}  {sizes}")


if __name__ == "__main__":
    main()
