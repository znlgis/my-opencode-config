#!/usr/bin/env python3
"""Slice a large image into overlapping tiles for vision-model ingestion.

Usage:
    python tile.py <input.png> <output_dir> [--grid 2x2] [--overlap 0.10]

DeepSeek vision downscales each image to ~800x800 pixel budget before
tokenizing, so small text in a large image becomes unreadable. Slicing into
an NxN grid of overlapping tiles lets each tile get its own ~800x800 budget,
effectively multiplying readable resolution. --overlap (fraction of tile
size) prevents text straddling a cut line from being truncated. Output files
are named tile-<row>-<col>.<ext>.
"""
import argparse
import os
import re

from PIL import Image


def parse_grid(s):
    m = re.fullmatch(r"(\d+)x(\d+)", s.strip().lower())
    if not m:
        raise argparse.ArgumentTypeError("grid must be ROWSxCOLS, e.g. 2x2")
    rows, cols = int(m.group(1)), int(m.group(2))
    if rows < 1 or cols < 1:
        raise argparse.ArgumentTypeError("grid must be at least 1x1")
    return (rows, cols)


def parse_overlap(s):
    try:
        v = float(s)
    except ValueError:
        raise argparse.ArgumentTypeError(f"invalid overlap: {s!r}")
    if not 0 <= v < 1:
        raise argparse.ArgumentTypeError("overlap must be in [0, 1)")
    return v


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("image")
    ap.add_argument("outdir")
    ap.add_argument("--grid", type=parse_grid, default="2x2", help="rows x cols, e.g. 2x2 or 3x3")
    ap.add_argument("--overlap", type=parse_overlap, default=0.10)
    args = ap.parse_args()

    rows, cols = args.grid

    os.makedirs(args.outdir, exist_ok=True)
    img = Image.open(args.image)
    img = img.convert("RGB")
    w, h = img.size
    ext = os.path.splitext(args.image)[1].lower() or ".png"

    # Tile size with overlap: total span = cols*tile - (cols-1)*overlap*tile
    # Solve for tile so tiles cover the full image.
    tile_w = int(w / (cols - (cols - 1) * args.overlap)) if cols > 1 else w
    tile_h = int(h / (rows - (rows - 1) * args.overlap)) if rows > 1 else h
    step_w = int(tile_w * (1 - args.overlap)) if cols > 1 else w
    step_h = int(tile_h * (1 - args.overlap)) if rows > 1 else h

    for r in range(rows):
        for c in range(cols):
            left = min(c * step_w, w - tile_w)
            top = min(r * step_h, h - tile_h)
            left = max(0, left)
            top = max(0, top)
            box = (left, top, min(left + tile_w, w), min(top + tile_h, h))
            tile = img.crop(box)
            path = os.path.join(args.outdir, f"tile-{r + 1}-{c + 1}{ext}")
            tile.save(path)
            print(f"wrote {path} ({tile.width}x{tile.height})")


if __name__ == "__main__":
    main()
