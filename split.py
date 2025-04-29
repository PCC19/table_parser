import sys
import os
from pypdf import PdfReader, PdfWriter

def split_pdf(filename, n):
    # Read the PDF
    reader = PdfReader(filename)
    total_pages = len(reader.pages)
    base_name, ext = os.path.splitext(filename)

    # Calculate pages per file (some files may have one more page if not divisible)
    pages_per_file = total_pages // n
    remainder = total_pages % n

    start = 0
    for i in range(n):
        writer = PdfWriter()
        # Distribute the remainder pages among the first 'remainder' files
        end = start + pages_per_file + (1 if i < remainder else 0)
        for page in range(start, end):
            writer.add_page(reader.pages[page])
        out_filename = f"{base_name}_{i+1}{ext}"
        with open(out_filename, "wb") as out_file:
            writer.write(out_file)
        print(f"Created: {out_filename}")
        start = end

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python split_pdf.py <filename> <n>")
        sys.exit(1)
    filename = sys.argv[1]
    n = int(sys.argv[2])
    split_pdf(filename, n)

