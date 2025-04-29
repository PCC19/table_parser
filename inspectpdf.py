import sys
import fitz  # PyMuPDF

def inspect_pdf_objects(pdf_path):
    doc = fitz.open(pdf_path)
    xref_count = doc.xref_length()
    
    # Create list of all objects (excluding xref 0)
    objects = [(xref, doc.xref_is_stream(xref)) for xref in range(1, xref_count)]
    
    print(f"\nPDF contains {len(objects)} objects:")
    print("XREF | TYPE")
    print("-----|-----")
    for xref, is_stream in objects:
        print(f"{xref:4} | {'Stream' if is_stream else 'Dictionary/Array'}")

    # Interactive inspection
    for xref, is_stream in objects:
        input(f"\nPress Enter to view object {xref} (q to quit)... ")
        try:
            print(60*"=")
            if is_stream:
                content = doc.xref_stream(xref)
                print(f"\nStream Object {xref} (first 500 bytes):")
                print(content[:500], "... [truncated]")
            else:
                content = doc.xref_object(xref)
                print(f"\nObject {xref}:")
                print(content[:500], "... [truncated]")
        except Exception as e:
            print(f"Error reading object {xref}: {str(e)}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python inspect_pdf.py input.pdf")
        sys.exit(1)
    inspect_pdf_objects(sys.argv[1])

