#!/usr/bin/env python3
# src/pdf_to_images.py
from pdf2image import convert_from_path
from pathlib import Path
import argparse

def pdf_to_images(pdf_path: Path, out_dir: Path, dpi=300):
    out_dir.mkdir(parents=True, exist_ok=True)
    pages = convert_from_path(str(pdf_path), dpi=dpi)
    saved = []
    for i, p in enumerate(pages):
        out_path = out_dir / f"page_{i:03d}.png"
        p.save(out_path, "PNG")
        saved.append(out_path)
        print(f"Saved {out_path}")
    return saved

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("pdf", help="PDF file path (data/samples/your.pdf)")
    p.add_argument("--out", default="data/uploads", help="output image folder")
    p.add_argument("--dpi", type=int, default=300)
    args = p.parse_args()
    pdf_to_images(Path(args.pdf), Path(args.out), dpi=args.dpi)
