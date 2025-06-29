# adds a file to the knowledge base
import ollama

def add_chunk_to_database(chunk, EMBEDDING_MODEL):
    embedding = ollama.embed(model=EMBEDDING_MODEL, input=chunk)['embeddings'][0]
    return (chunk, embedding)


def add_to_kb(filename, EMBEDDING_MODEL):
    dataset = []
    with open(filename, 'r', encoding="utf8") as file:
      dataset = file.readlines()
      print(f'Loaded {len(dataset)} entries')
    
    VECTOR_DB_Local = []

    for i, chunk in enumerate(dataset):
      VECTOR_DB_Local.append(add_chunk_to_database(chunk, EMBEDDING_MODEL))
      print(f'Added chunk {i+1}/{len(dataset)} to the database')
    return VECTOR_DB_Local

