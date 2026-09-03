#!/usr/bin/env python3
"""Render PDF pages to PNG images for vision-model ingestion.

Usage:
    python pdf2png.py <input.pdf> <output_dir> [--pages 1-3,5] [--zoom 2.0]

DeepSeek vision does not accept PDF input, so pages must be rasterized first.
--zoom scales render resolution (1.0 = ~72dpi; 2.0 = ~144dpi). Default renders
all pages. --pages accepts comma/range syntax like "1-3,5". Output files are
named page-<n>.png (1-based). Rendered pages larger than ~2000px on the long
edge should be tiled with tile.py before sending to the model.
"""
import argparse
import os
import re

import pymupdf


def parse_pages_spec(s):
    for part in s.split(","):
        part = part.strip()
        if not re.fullmatch(r"\d+(-\d+)?", part):
            raise argparse.ArgumentTypeError(f"invalid page spec: {part!r}")
    return s


def positive_float(s):
    try:
        v = float(s)
    except ValueError:
        raise argparse.ArgumentTypeError(f"invalid number: {s!r}")
    if v <= 0:
        raise argparse.ArgumentTypeError("zoom must be greater than 0")
    return v


def parse_pages(spec, total):
    if not spec:
        return list(range(total))
    pages = set()
    for part in spec.split(","):
        part = part.strip()
        if "-" in part:
            a, b = part.split("-", 1)
            pages.update(range(int(a) - 1, int(b)))
        else:
            pages.add(int(part) - 1)
    return sorted(p for p in pages if 0 <= p < total)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pdf")
    ap.add_argument("outdir")
    ap.add_argument("--pages", type=parse_pages_spec, default=None, help="e.g. 1-3,5")
    ap.add_argument("--zoom", type=positive_float, default=2.0)
    args = ap.parse_args()

    os.makedirs(args.outdir, exist_ok=True)
    doc = pymupdf.open(args.pdf)
    total = doc.page_count
    for pno in parse_pages(args.pages, total):
        page = doc[pno]
        pix = page.get_pixmap(matrix=pymupdf.Matrix(args.zoom, args.zoom))
        path = os.path.join(args.outdir, f"page-{pno + 1}.png")
        pix.save(path)
        print(f"wrote {path} ({pix.width}x{pix.height})")


if __name__ == "__main__":
    main()
