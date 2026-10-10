import fitz #pymupdf

def extract_text(uploaded_file):
    document = fitz.open(stream=uploaded_file.read(),filetype="pdf")
    text=""
    for page in document:
     text += page.get_text()
    return text
