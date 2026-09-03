#!/usr/bin/env python3
"""Convert one or more CSV files into an .xlsx workbook.

Usage:
    python csv2xlsx.py <output.xlsx> <input1.csv> [input2.csv ...]

Each CSV becomes a sheet named after its file stem (sanitized, truncated to
31 chars). Numeric-looking cells are written as numbers; everything else as
text.
"""
import csv
import os
import re
import sys

from openpyxl import Workbook


def sheet_name(stem):
    name = re.sub(r"[\[\]:*?/\\]", "_", stem)[:31]
    return name or "Sheet"


def unique_sheet_name(base, used):
    name = base
    n = 2
    while name in used:
        suffix = f"_{n}"
        name = base[: 31 - len(suffix)] + suffix
        n += 1
    used.add(name)
    return name


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)
    dst = sys.argv[1]
    srcs = sys.argv[2:]
    wb = Workbook()
    first = wb.active
    assert first is not None  # fresh workbook always has one sheet
    used = set()
    for idx, src in enumerate(srcs):
        stem = os.path.splitext(os.path.basename(src))[0]
        ws = first if idx == 0 else wb.create_sheet()
        ws.title = unique_sheet_name(sheet_name(stem), used)
        with open(src, newline="", encoding="utf-8-sig") as f:
            for row in csv.reader(f):
                out = []
                for cell in row:
                    s = cell.strip()
                    if s == "":
                        out.append(None)
                    elif re.fullmatch(r"-?\d+(\.\d+)?", s):
                        out.append(float(s) if "." in s else int(s))
                    else:
                        out.append(s)
                ws.append(out)
    wb.save(dst)
    print(f"wrote {dst}")


if __name__ == "__main__":
    main()
