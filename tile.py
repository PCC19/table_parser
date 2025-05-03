#!/usr/bin/env python3

import sys
from PIL import Image

def tile_image(image_path, w, h, output_path="tiled_output.png"):
    # Open the original image
    original = Image.open(image_path)
    orig_w, orig_h = original.size

    # Create new blank image with tiled size
    tiled_image = Image.new('RGB', (orig_w * w, orig_h * h))

    # Paste original image in a grid
    for i in range(w):
        for j in range(h):
            tiled_image.paste(original, (i * orig_w, j * orig_h))

    # Save output
    tiled_image.save(output_path)
    print(f"Tiled image saved as {output_path}")

def main():
    if len(sys.argv) != 4:
        print("Usage: python tile_image.py <image_path> <w> <h>")
        sys.exit(1)

    image_path = sys.argv[1]
    try:
        w = int(sys.argv[2])
        h = int(sys.argv[3])
    except ValueError:
        print("Error: w and h must be integers.")
        sys.exit(1)

    if w <= 0 or h <= 0:
        print("Error: w and h must be positive integers.")
        sys.exit(1)

    tile_image(image_path, w, h)

if __name__ == "__main__":
    main()

