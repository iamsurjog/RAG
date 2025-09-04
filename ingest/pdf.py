from pypdf import PdfReader

def read(file):
    reader = PdfReader(file)
    texts = []
    for page in reader.pages:
        texts.extend(page.extract_text().split("\n"))
    return texts
