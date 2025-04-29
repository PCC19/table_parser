import sys
import os
from PyPDF2 import PdfReader

if len(sys.argv) != 2:
    print("Usage: python extract_pdf_text.py <input.pdf>")
    sys.exit(1)

pdf_path = sys.argv[1]
txt_path = os.path.splitext(pdf_path)[0] + ".txt"

reader = PdfReader(pdf_path)
text = ""

for page in reader.pages:
    page_text = page.extract_text()
    if page_text:
        text += page_text

with open(txt_path, "w", encoding="utf-8") as f:
    f.write(text)

print(f"Extracted text saved to {txt_path}")

