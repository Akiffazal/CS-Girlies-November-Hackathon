import fitz  # PyMuPDF

def load_pdf(content):
    doc = fitz.open(stream=content, filetype="pdf")
    full_text = ""

    for page in doc:
        full_text += page.get_text()

    doc.close()
    
    # simple splitting
    chunks = full_text.split("\n\n")
    return [c.strip() for c in chunks if len(c.strip()) > 20]
