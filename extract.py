import pdfplumber
import argparse
import os

def extract_text(pdf_path, txt_path):
    with pdfplumber.open(pdf_path) as pdf:
        text = ""
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text
    with open(txt_path, "w", encoding="utf-8") as txt_file:
        txt_file.write(text)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract all text from a PDF and save as TXT.")
    parser.add_argument("pdf_file", help="Path to the PDF file")
    parser.add_argument("--output", "-o", help="Output TXT file path (optional)")
    args = parser.parse_args()

    pdf_file = args.pdf_file
    if args.output:
        txt_file = args.output
    else:
        txt_file = os.path.splitext(pdf_file)[0] + ".txt"

    extract_text(pdf_file, txt_file)
    print(f"Text extracted to {txt_file}")

