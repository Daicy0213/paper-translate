#!/usr/bin/env python3
"""Extract text from a PDF into a plain-text file with page markers.

Used by the translate-paper skill so that text-only LLM backends - which reject
the non-text PDF content that the built-in `Read` tool sends, producing errors
like `API Error: 400 Model only support text input` - can still translate papers.

Strategy (first available backend wins):
  1. `pdftotext` CLI (poppler)    - best layout/column fidelity
  2. `pdfplumber` Python package  - good fidelity, pure-Python fallback
  3. `pypdf` / `PyPDF2`           - last resort, always installable via pip

Usage:
  python extract_pdf.py <paper.pdf> [--out paper.txt] [--layout]

Notes:
  - By default uses pdftotext's default (column-aware) mode, which reads
    two-column papers in correct reading order. Pass --layout to preserve
    visual layout instead (better for tables, worse for two-column prose).
  - Writes a page marker `--- Page N ---` before each page so the model can
    translate in batches without losing page boundaries.
"""
import argparse
import os
import shutil
import subprocess
import sys

PAGE_MARKER = "--- Page {n} ---"


def extract_with_pdftotext(pdf_path, layout=False):
    if shutil.which("pdftotext") is None:
        return None
    args = ["pdftotext"]
    if layout:
        args.append("-layout")
    args += [pdf_path, "-"]
    try:
        res = subprocess.run(
            args, capture_output=True, text=True,
            encoding="utf-8", errors="replace",
        )
        if res.returncode != 0:
            return None
        pages = res.stdout.split("\f")
        if pages and pages[-1].strip() == "":
            pages.pop()
        return pages
    except Exception:
        return None


def extract_with_pdfplumber(pdf_path):
    try:
        import pdfplumber
    except Exception:
        return None
    pages = []
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                pages.append(page.extract_text() or "")
    except Exception as e:
        print(f"[warn] pdfplumber failed: {e}", file=sys.stderr)
        return None
    return pages


def extract_with_pypdf(pdf_path):
    try:
        import pypdf
    except Exception:
        try:
            import PyPDF2 as pypdf  # type: ignore
        except Exception:
            return None
    pages = []
    try:
        reader = pypdf.PdfReader(pdf_path)
        for page in reader.pages:
            try:
                pages.append(page.extract_text() or "")
            except Exception:
                pages.append("")
    except Exception as e:
        print(f"[warn] pypdf failed: {e}", file=sys.stderr)
        return None
    return pages


def extract(pdf_path, layout=False):
    backends = [
        ("pdftotext", lambda: extract_with_pdftotext(pdf_path, layout)),
        ("pdfplumber", lambda: extract_with_pdfplumber(pdf_path)),
        ("pypdf", lambda: extract_with_pypdf(pdf_path)),
    ]
    for name, fn in backends:
        pages = fn()
        if pages is not None:
            print(f"[info] extracted {len(pages)} page(s) using {name}", file=sys.stderr)
            return pages
    return None


def main():
    ap = argparse.ArgumentParser(description="Extract PDF text with page markers.")
    ap.add_argument("pdf", help="path to the input PDF file")
    ap.add_argument("--out", help="path to output .txt (default: <pdf>.txt)")
    ap.add_argument("--layout", action="store_true",
                    help="preserve visual layout (pdftotext -layout); "
                         "default is column-aware mode, better for two-column papers")
    args = ap.parse_args()

    if not os.path.isfile(args.pdf):
        print(f"[error] file not found: {args.pdf}", file=sys.stderr)
        sys.exit(1)

    out_path = args.out or os.path.splitext(args.pdf)[0] + ".txt"

    pages = extract(args.pdf, args.layout)
    if pages is None:
        print(
            "[error] could not extract text from PDF. Install one of:\n"
            "  - poppler (provides the `pdftotext` command), or\n"
            "  - `pip install pdfplumber`, or\n"
            "  - `pip install pypdf`",
            file=sys.stderr,
        )
        sys.exit(2)

    with open(out_path, "w", encoding="utf-8") as f:
        for i, text in enumerate(pages, start=1):
            f.write(PAGE_MARKER.format(n=i) + "\n")
            f.write((text or "").rstrip() + "\n\n")

    print(f"[done] wrote {len(pages)} page(s) to {out_path}", file=sys.stderr)


if __name__ == "__main__":
    main()
