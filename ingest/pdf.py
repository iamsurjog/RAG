from pypdf import PdfReader

def read(file):
    reader = PdfReader(file)
    texts = []
    for page in reader.pages:
        texts.append(page.extract_text())
    return texts
