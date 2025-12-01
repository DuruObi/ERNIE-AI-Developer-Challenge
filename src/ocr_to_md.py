#!/usr/bin/env python3
# src/ocr_to_md.py
import json
from pathlib import Path
import argparse
from statistics import median

def bbox_height(bbox):
    # bbox is typically [[x1,y1],[x2,y2],[x3,y3],[x4,y4]]
    if not bbox:
        return 0
    ys = [pt[1] for pt in bbox]
    return max(ys) - min(ys)

def guess_heading(text):
    # simple heuristics: short and uppercase-ish
    if len(text) < 60 and sum(1 for c in text if c.isupper()) / max(1, len(text)) > 0.25:
        return True
    if text.strip().endswith(":") or text.strip().lower().startswith("abstract"):
        return True
    return False

def ocr_json_to_md(json_path, out_md_path):
    data = json.load(open(json_path, encoding='utf-8'))
    md_lines = []
    # compute median bbox height to use as baseline for font-size heuristics
    heights = [bbox_height(block['bbox']) for page in data for block in page['blocks'] if block.get('bbox')]
    base = median(heights) if heights else 0

    md_lines.append("# Converted Document\n\n")
    for p_i, page in enumerate(data):
        md_lines.append(f"<!-- Page {p_i+1} -->\n\n")
        for b in page['blocks']:
            txt = (b.get('text') or "").strip()
            if not txt:
                continue
            h = bbox_height(b.get('bbox'))
            # heading heuristic: bbox much larger than median OR guess by content
            if base and h > 1.6 * base:
                md_lines.append(f"## {txt}\n\n")
            elif guess_heading(txt):
                md_lines.append(f"### {txt}\n\n")
            else:
                # preserve paragraphs; add newline
                md_lines.append(txt + "\n\n")
    Path(out_md_path).parent.mkdir(parents=True, exist_ok=True)
    open(out_md_path, "w", encoding="utf-8").write("".join(md_lines))
    print(f"Saved Markdown to {out_md_path}")

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--in", dest="inp", default="data/uploads/ocr_output.json")
    p.add_argument("--out", default="demo/raw.md")
    args = p.parse_args()
    ocr_json_to_md(args.inp, args.out)
