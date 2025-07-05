from ingest import txt, pdf
    
def read(fpath):
    # print("helo")
    ext = fpath.split(".")[-1]
    if ext == "txt":
        return txt.read(fpath)
    if ext == "pdf":
        return pdf.read(fpath)
