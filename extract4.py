import sys
import pathlib
from pdf2image import convert_from_path
import pytesseract

def extract_text_to_txt(pdf_filename):
    txt_filename = pathlib.Path(pdf_filename).with_suffix('.txt')
    
    # Convert PDF to images (300 DPI for better OCR accuracy)
    images = convert_from_path(pdf_filename, 300)
    
    extracted_text = []
    for i, image in enumerate(images):
        # Optional: Uncomment to process specific region (coordinates in pixels)
        # left = 20 * 3  # Multiply by 3 since 300 DPI vs 100 DPI coordinates
        # top = 50 * 3
        # right = 120 * 3
        # bottom = 150 * 3
        # cropped = image.crop((left, top, right, bottom))
        # text = pytesseract.image_to_string(cropped)
        
        text = pytesseract.image_to_string(image)
        extracted_text.append(text)
    
    # Join pages with form feed character and save
    text = '========\f'.join(extracted_text)
    txt_filename.write_text(text, encoding='utf-8')
    print(f"Extracted text saved to: {txt_filename}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py input.pdf")
        sys.exit(1)
    extract_text_to_txt(sys.argv[1])

