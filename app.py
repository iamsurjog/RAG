import streamlit as st
import ollama
import os
from dotenv import load_dotenv
from scripts.add_file import add_to_kb

# Loading the models from the .env file

load_dotenv()
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL")
LANGUAGE_MODEL = os.getenv("LANGUAGE_MODEL")

def cosine_similarity(a, b):
  dot_product = sum([x * y for x, y in zip(a, b)])
  norm_a = sum([x ** 2 for x in a]) ** 0.5
  norm_b = sum([x ** 2 for x in b]) ** 0.5
  return dot_product / (norm_a * norm_b)


def retrieve(query, top_n=3):
  query_embedding = ollama.embed(model=EMBEDDING_MODEL, input=query)['embeddings'][0]
  # temporary list to store (chunk, similarity) pairs
  similarities = []
  for chunk, embedding in st.session_state['VECTOR_DB']:
    similarity = cosine_similarity(query_embedding, embedding)
    similarities.append((chunk, similarity))
  # sort by similarity in descending order, because higher similarity means more relevant chunks
  similarities.sort(key=lambda x: x[1], reverse=True)
  # finally, return the top N most relevant chunks
  return similarities[:top_n]

# --- Sidebar: File List and Add File Button ---
st.sidebar.title("Knowledge Base Files")

# Session state to persist file list, content and vectordb
if 'files' not in st.session_state:
    st.session_state['files'] = {}
if 'selected_file' not in st.session_state:
    st.session_state['selected_file'] = None
if 'VECTOR_DB' not in st.session_state:
    st.session_state['VECTOR_DB'] = []

# Button to add files
uploaded_files = st.sidebar.file_uploader(
    "Add files to knowledge base",
    accept_multiple_files=True,
    key="file_uploader"
)

# Add uploaded files to session state
if uploaded_files:
    for file in uploaded_files:
        st.session_state['VECTOR_DB'].extend(add_to_kb(file.name, EMBEDDING_MODEL))
        st.session_state['files'][file.name] = file.getvalue()

# Display list of files
file_names = list(st.session_state['files'].keys())
if file_names:
    selected = st.sidebar.radio("Files:", file_names, key="file_list")
    st.session_state['selected_file'] = selected
else:
    st.sidebar.write("No files added yet.")

# --- Main Area: File Viewer, Q&A ---
st.title("RAG Knowledge Base")

# Display selected file content
if st.session_state['selected_file']:
    st.subheader(f"Viewing: {st.session_state['selected_file']}")
    file_content = st.session_state['files'][st.session_state['selected_file']]
    try:
        # Try to decode as text
        st.text_area(
            "File Content",
            file_content.decode("utf-8"),
            height=200,
            disabled=True
        )
    except Exception:
        st.write("Cannot display file content (not a text file).")

# Input field for questions
question = st.text_input("Ask a question:")

# Placeholder for answer
if question:
    # Here, you would call your RAG backend to get the answer
    # For now, just echo the question
    retrieved_knowledge = retrieve(question)

    print('Retrieved knowledge:')
    for chunk, similarity in retrieved_knowledge:
        print(f' - (similarity: {similarity:.2f}) {chunk}')
    instruction_prompt = '''You are a helpful chatbot.
    Use only the following pieces of context to answer the question. Don't make up any new information: \n
    ''' + ('\n'.join([f' - {chunk}' for chunk, similarity in retrieved_knowledge]))

    stream = ollama.chat(
      model=LANGUAGE_MODEL,
      messages=[
        {'role': 'system', 'content': instruction_prompt},
        {'role': 'user', 'content': question},
      ],
      stream=True,
    )
    ans = ''
    
    for chunk in stream:
        ans += chunk['message']['content']
    st.markdown("**Answer:**")
    st.write(ans)
else:
    st.markdown("**Answer will appear here.**")
