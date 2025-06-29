import os
from dotenv import load_dotenv
load_dotenv()
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL")
LANGUAGE_MODEL = os.getenv("LANGUAGE_MODEL")
print(EMBEDDING_MODEL)
print(LANGUAGE_MODEL)
