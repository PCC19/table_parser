import sys
import pathlib
import pymupdf

def extract_text_to_txt(pdf_filename):
    # Remove .pdf extension and add .txt
    txt_filename = pathlib.Path(pdf_filename).with_suffix('.txt')
    with pymupdf.open(pdf_filename) as doc:
        # Join text of all pages, separated by form feed
        text = '\f'.join([page.get_text() for page in doc])
        # Write as UTF-8 to support non-ASCII characters
        txt_filename.write_text(text, encoding='utf-8')
    print(f"Extracted text saved to: {txt_filename}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py input.pdf")
        sys.exit(1)
    extract_text_to_txt(sys.argv[1])

