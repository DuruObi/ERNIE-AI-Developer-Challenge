# setup
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# convert a PDF to images
python src/pdf_to_images.py data/samples/yourfile.pdf

# run OCR (PaddleOCR)
python src/ocr_infer.py --images "data/uploads/*.png" --out data/uploads/ocr_output.json

# convert OCR to markdown
python src/ocr_to_md.py --in data/uploads/ocr_output.json --out demo/raw.md

# send to ERNIE (set .env or env vars)
python src/ernie_client.py

# view result
open demo/index.html
