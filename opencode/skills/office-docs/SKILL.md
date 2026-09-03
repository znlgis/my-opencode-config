---
name: office-docs
description: Read and write Microsoft Word (.docx) and Excel (.xlsx) files by converting to/from plain text or Markdown. Use when the task mentions reading a Word/Excel document, extracting text from .docx/.xlsx, creating a .docx/.xlsx, or "读 Word", "读 Excel", "生成 docx", "写 xlsx". Pure-Python via bundled scripts; no MS Office or MCP required.
---

# Office Documents (Word / Excel)

Read and write `.docx` and `.xlsx` files through bundled Python scripts that
convert to/from Markdown and CSV. The model then reads the plain-text output
with the normal `read` tool, or writes a text file that a script converts
back to a binary Office file.

## When to use

- Extract text/content from a `.docx` or `.xlsx` so the model can read it.
- Generate a `.docx` or `.xlsx` from content the model produced.

## Prerequisites

Python 3 with these packages (already installed in this environment):
`python-docx`, `openpyxl`. Scripts live in `scripts/` next to this file.

## Reading

### Word (.docx) -> Markdown

```powershell
python <skill_dir>/scripts/docx2md.py <input.docx> <output.md>
```

Then `read` the `.md`. Omit the output path to print to stdout. Paragraphs,
headings, bullet/numbered lists, and pipe tables are preserved. Numbered
lists are written as Markdown ordered lists, so the renderer re-numbers them
rather than preserving the original values. Inline images are not extracted
(binary media).

### Excel (.xlsx) -> CSV

```powershell
python <skill_dir>/scripts/xlsx2csv.py <input.xlsx> <output_dir>
```

Writes one `<sheetname>.csv` per sheet into `output_dir`. Omit the output
dir to print the first sheet to stdout. Formulas are read as cached values.

### Legacy formats (.doc / .xls)

The scripts only handle the modern OOXML formats. For a legacy `.doc` or
`.xls`, first convert via Word/Excel COM (available on this machine, Office
2007) to `.docx`/`.xlsx`, then run the script above:

```powershell
$w = New-Object -ComObject Word.Application; $w.Visible = $false
$d = $w.Documents.Open('<abs path>.doc'); $d.SaveAs2('<abs path>.docx', 16); $d.Close(); $w.Quit()
```

(Excel: `SaveAs` format 51 = xlsx.) Use absolute paths for COM; a single
quote in a path must be doubled (`''`) to escape.

## Writing

### Markdown -> Word (.docx)

```powershell
python <skill_dir>/scripts/md2docx.py <input.md> <output.docx>
```

Supports ATX headings, paragraphs, `-`/`*` unordered lists, `1.` ordered
lists, and pipe tables. Inline bold/italic/code is not parsed — content is
written as plain runs. This is a lossy plain-text writer for simple
documents, not a styled round-trip.

### CSV -> Excel (.xlsx)

```powershell
python <skill_dir>/scripts/csv2xlsx.py <output.xlsx> <input1.csv> [input2.csv ...]
```

Each CSV becomes a sheet named after its file stem. Numeric-looking cells
are written as numbers, which drops leading zeros (`007` -> `7`) and limits
16+ digit IDs to Excel's 15-digit precision; keep such values as text
(non-numeric) if they must survive unchanged.

## Workflow guidance

1. **Read**: convert to `.md`/`.csv`, then `read` the text file. Never try
   to `read` the binary `.docx`/`.xlsx` directly — opencode rejects binary
   files.
2. **Write**: have the model produce a `.md` or `.csv` file first (via the
   `write` tool), then convert to the Office format with the script.
3. **Fidelity caveat**: these conversions are lossy. Complex styling,
   embedded images, and macros are not preserved. For high-fidelity Office
   round-trips, consider an MCP document server instead.
4. Always use absolute paths for input/output files.
