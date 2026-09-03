#!/usr/bin/env python3
"""Convert a .docx file to Markdown (paragraphs + tables).

Usage:
    python docx2md.py <input.docx> [output.md]

If output.md is omitted, prints to stdout. Tables are rendered as pipe
tables. Inline images are not extracted (binary media).
"""
import sys

from docx import Document
from docx.table import Table
from docx.text.paragraph import Paragraph

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def iter_block_items(parent):
    """Yield paragraphs and tables in document order (python-docx has no
    native iterator over mixed body children)."""
    from docx.oxml.ns import qn

    body = parent.element.body
    for child in body.iterchildren():
        if child.tag == qn("w:p"):
            yield Paragraph(child, parent)
        elif child.tag == qn("w:tbl"):
            yield Table(child, parent)


def para_to_md(p):
    text = p.text.strip()
    if not text:
        return ""
    style = (p.style.name or "").lower()
    if style.startswith("heading") or style.startswith("title"):
        try:
            level = int(style.replace("heading", "").replace("title", "1").strip() or "1")
        except ValueError:
            level = 1
        level = max(1, min(level, 6))
        return f"{'#' * level} {text}"
    if style.startswith("list bullet"):
        return f"- {text}"
    if style.startswith("list number"):
        return f"1. {text}"
    return text


def table_to_md(t):
    rows = []
    for row in t.rows:
        cells = [c.text.strip().replace("\n", " ").replace("|", "\\|") for c in row.cells]
        rows.append(cells)
    if not rows:
        return ""
    widths = max(len(r) for r in rows)
    header = rows[0] + [""] * (widths - len(rows[0]))
    out = ["| " + " | ".join(header) + " |"]
    out.append("| " + " | ".join(["---"] * widths) + " |")
    for r in rows[1:]:
        r = r + [""] * (widths - len(r))
        out.append("| " + " | ".join(r) + " |")
    return "\n".join(out)


def convert(doc):
    parts = []
    for block in iter_block_items(doc):
        if isinstance(block, Paragraph):
            md = para_to_md(block)
            if md:
                parts.append(md)
        elif isinstance(block, Table):
            parts.append(table_to_md(block))
    return "\n\n".join(parts)


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    src = sys.argv[1]
    doc = Document(src)
    md = convert(doc)
    if len(sys.argv) >= 3:
        with open(sys.argv[2], "w", encoding="utf-8") as f:
            f.write(md + "\n")
    else:
        print(md)


if __name__ == "__main__":
    main()
