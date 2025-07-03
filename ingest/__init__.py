from ingest import txt
    
def read(fpath):
    ext = fpath.split(".")[-1]
    if ext == "txt":
        txt.read(fpath)
