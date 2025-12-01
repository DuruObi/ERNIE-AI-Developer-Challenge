#!/usr/bin/env python3
# src/ocr_infer.py
import json
from paddleocr import PaddleOCR
import glob
from pathlib import Path
import argparse
from rich import print

def run_ocr(images_glob, out_json):
    ocr = PaddleOCR(use_angle_cls=True, lang='en')  # adjust flags for VL if available
    outputs = []
    imgs = sorted(glob.glob(images_glob))
    print(f"[green]Found {len(imgs)} images[/green]")
    for img in imgs:
        res = ocr.ocr(img, det=True, rec=True, cls=True)
        # format a friendly structure
        page = {"image": img, "blocks": []}
        for block in res:
            # block is usually list-of-lines; adapt depending on returned shape
            # To be robust, collect bbox and aggregated text
            try:
                bbox = block[0]  # detection box
                text = " ".join([line[1][0] for line in block[1:]]) if isinstance(block[1:], list) else ""
            except Exception:
                # Fallback: older paddleocr format: list of (bbox, (text, score))
                if isinstance(block, list) and len(block) >= 2:
                    bbox = block[0]
                    text = block[1][0] if isinstance(block[1], (list, tuple)) else str(block[1])
                else:
                    bbox = None
                    text = str(block)
            page['blocks'].append({"bbox": bbox, "text": text})
        outputs.append(page)
        print(f"[blue]OCRed {img} -> {len(page['blocks'])} blocks[/blue]")
    Path(out_json).parent.mkdir(parents=True, exist_ok=True)
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(outputs, f, indent=2, ensure_ascii=False)
    print(f"[green]Saved OCR JSON to {out_json}[/green]")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--images", default="data/uploads/*.png")
    ap.add_argument("--out", default="data/uploads/ocr_output.json")
    args = ap.parse_args()
    run_ocr(args.images, args.out)
