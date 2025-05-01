import sys
from pdf2image import convert_from_path
from PIL import Image
import pytesseract
import pathlib
import re
from pathvalidate import sanitize_filename

def get_line(text, word):
    for line in text.splitlines():
        if word.casefold() in line.casefold():
            return line
    return 'na'

def extract_word(text, word):
    line = get_line(text, word)
    last_colon = line.rfind(':')  # Find the last colon
    if last_colon == -1:
        return 'na'  # No colon found
    # Get substring after the colon
    after_colon = line[last_colon+1:]
    # Strip leading spaces
    after_colon = after_colon.lstrip()
    # Find the first space in the remaining string
    first_space = after_colon.find(' ')
    if first_space == -1:
        return after_colon.lower().replace(".","").replace(",","").replace("-","")
    return after_colon[:first_space].lower().replace(".","").replace(",","").replace("-","")

def process_page_pair(page1_img, page2_img, pair_num):
    width, height = page1_img.size
    if height < 4000:
        n = 2
    else:
        n = 5
    block_height = height // n  # 5 horizontal blocks per page
    output = []
    nome = []
    stats = []
    full_text = []

    for block_idx in range(n):
        # Process first page (left blocks only)
        y0 = block_idx * block_height
        y1 = (block_idx + 1) * block_height if block_idx < 4 else height
        left_box = (0, y0, width//2, y1)
        crop = page1_img.crop(left_box)
        text = pytesseract.image_to_string(crop).strip()
        #output.append(f"[Pair {pair_num} Page 1 Block {block_idx+1}]\n{text}")
        danger = extract_word(text, "danger")
        climate = extract_word(text, "climate")
        terrain = extract_word(text, "terrain")
        attribute = extract_word(text, "attribute")
        encounter = extract_word(text, "encounter")
        add = extract_word(text, "additional")
        xp = extract_word(text, "xp")
        nome = '_'.join([danger, climate, terrain, attribute, encounter, add, xp])
        stats = 'STATS: | ' + ' | '.join([danger, climate, terrain, attribute, encounter, add, xp]) + ' |'
        
        # Process second page (both columns)
        # Left column
        left_box = (0, y0, width//2, y1)
        left_crop = page2_img.crop(left_box)
        left_text = pytesseract.image_to_string(left_crop).strip()
        
        # Right column
        right_box = (width//2, y0, width, y1)
        right_crop = page2_img.crop(right_box)
        right_text = pytesseract.image_to_string(right_crop).strip()
        
        # Assemble full text
        tag = f"[Pair {pair_num} Page 2 Block {block_idx+1}]"
        full_text = tag + '\n\n' + stats + '\n\n' + left_text + '\n' + right_text 

        # Save File
        safe_filename = sanitize_filename(nome) + '.enc'  # Remove invalid characters
        with open(safe_filename, 'w', encoding='utf-8') as f:
            f.write(full_text)
        print(f"Extracted text saved to: {safe_filename}")

def extract_paired_pages(pdf_path):
    images = convert_from_path(pdf_path, dpi=300)
    all_text = []
    
    # Process pages in pairs
    for i in range(0, len(images), 2):
        if i+1 >= len(images):
            break  # Skip last page if odd number
        print("Processing page pair: ", i)
        pair_text = process_page_pair(images[i], images[i+1], i//2 + 1)
    print("finished !")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py input.pdf")
        sys.exit(1)
    extract_paired_pages(sys.argv[1])
