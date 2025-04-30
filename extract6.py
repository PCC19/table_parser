import sys
from pdf2image import convert_from_path
from PIL import Image
import pytesseract
import pathlib

def process_page_pair(page1_img, page2_img, pair_num):
    width, height = page1_img.size
    block_height = height // 5  # 5 horizontal blocks per page
    output = []

    # Process first page (left blocks only)
    for block_idx in range(5):
        y0 = block_idx * block_height
        y1 = (block_idx + 1) * block_height if block_idx < 4 else height
        left_box = (0, y0, width//2, y1)
        crop = page1_img.crop(left_box)
        text = pytesseract.image_to_string(crop).strip()
        output.append(f"[Pair {pair_num} Page 1 Block {block_idx+1}]\n{text}")

    # Process second page (both columns)
    for block_idx in range(5):
        y0 = block_idx * block_height
        y1 = (block_idx + 1) * block_height if block_idx < 4 else height
        
        # Left column
        left_box = (0, y0, width//2, y1)
        left_crop = page2_img.crop(left_box)
        left_text = pytesseract.image_to_string(left_crop).strip()
        
        # Right column
        right_box = (width//2, y0, width, y1)
        right_crop = page2_img.crop(right_box)
        right_text = pytesseract.image_to_string(right_crop).strip()
        
        output.append(f"[Pair {pair_num} Page 2 Block {block_idx+1}]\n{left_text}\n{right_text}")

    return '\n\n'.join(output)

def extract_paired_pages(pdf_path, output_txt='output.txt'):
    images = convert_from_path(pdf_path, dpi=300)
    all_text = []
    
    # Process pages in pairs
    for i in range(0, len(images), 2):
        if i+1 >= len(images):
            break  # Skip last page if odd number
        pair_text = process_page_pair(images[i], images[i+1], i//2 + 1)
        all_text.append(pair_text)
    
    # Join pairs with form feed separator
    final_text = '\n========\f\n'.join(all_text)
    with open(output_txt, 'w', encoding='utf-8') as f:
        f.write(final_text)
    print(f"Extracted text saved to: {output_txt}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py input.pdf")
        sys.exit(1)
    txt_filename = pathlib.Path(sys.argv[1]).with_suffix('.txt')
    extract_paired_pages(sys.argv[1], txt_filename)

