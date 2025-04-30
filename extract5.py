import sys
from pdf2image import convert_from_path
from PIL import Image
import pytesseract
import pathlib

def extract_blocks_from_pdf(pdf_path, output_txt='output.txt'):
    # Convert PDF pages to images
    pages = convert_from_path(pdf_path, dpi=300)
    all_text = []

    for page_num, page_img in enumerate(pages):
        width, height = page_img.size
        block_height = height // 5  # Divide page height into 5 horizontal blocks

        page_text = []

        for block_idx in range(5):
            y0 = block_idx * block_height
            y1 = (block_idx + 1) * block_height if block_idx < 4 else height

            # Split each block into two columns (left and right)
            mid_x = width // 2

            # Left column
            left_box = (0, y0, mid_x, y1)
            left_crop = page_img.crop(left_box)
            left_text = pytesseract.image_to_string(left_crop)
            page_text.append(f"[Page {page_num+1} Block {block_idx+1} Left]\n{left_text.strip()}")

            # Right column
            right_box = (mid_x, y0, width, y1)
            right_crop = page_img.crop(right_box)
            right_text = pytesseract.image_to_string(right_crop)
            page_text.append(f"[Page {page_num+1} Block {block_idx+1} Right]\n{right_text.strip()}")

        all_text.append('\n\n'.join(page_text))
 wa
    # Join all pages with form feed separator
    final_text = '\n========\f\n'.join(all_text)
    txt_filename = pathlib.Path(pdf_path).with_suffix('.txt')
    with open(txt_filename, 'w', encoding='utf-8') as f:
        f.write(final_text)
    print(f"Extracted text saved to: {txt_filename}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py input.pdf")
        sys.exit(1)
    extract_blocks_from_pdf(sys.argv[1])

