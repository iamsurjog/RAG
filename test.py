from rag import Core
import os
from dotenv import load_dotenv

load_dotenv()
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL")
LANGUAGE_MODEL = os.getenv("LANGUAGE_MODEL")

rag = Core(EMBEDDING_MODEL, LANGUAGE_MODEL)
rag.add_files()
