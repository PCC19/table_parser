import sys
import fitz  # PyMuPDF

def print_stream(stream):
    print("!!!")
    doc = fitz.open()
    page = doc.new_page()
    page.insert_font()  # make page knowing the font Helvetica
    xref = doc.get_new_xref()  # create a new xref
    doc.update_object(xref, "<<>>")  # make it a PDF dictionary

    # replace the fontname by Helvetica
    stream = stream.replace(b"/F*", b"/helv")  # change fontname to Helevetica standard name

    doc.update_stream(xref, stream)  # insert into our new object
    page.set_contents(xref)  # define this to be the page's /Contents

    text = page.get_text(
        clip=fitz.INFINITE_RECT()
    )  # extract the text wherever it has been written
    print(text)

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
        #input(f"\nPress Enter to view object {xref} (q to quit)... ")
        try:
            print(60*"=")
            if is_stream:
                content = doc.xref_stream(xref)
                print(f"\nStream Object {xref} (first 500 bytes):")
                #print(content[:500], "... [truncated]")
                #print(content)
                print_stream(content)
            else:
                content = doc.xref_object(xref)
                print(f"\nObject {xref}:")
                print(content[:500], "... [truncated]")
                #print(content)
        except Exception as e:
            print(f"Error reading object {xref}: {str(e)}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python inspect_pdf.py input.pdf")
        sys.exit(1)
    inspect_pdf_objects(sys.argv[1])

