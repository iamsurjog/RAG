import streamlit as st
import os
from rag import Core
from dotenv import load_dotenv

load_dotenv()
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL")
LANGUAGE_MODEL = os.getenv("LANGUAGE_MODEL")

# Dummy backend functions (replace with your logic)
def add_files(files):
    st.info(f"add_file called with: {files}")
    for file in files:
       st.session_state["rag"].add_file(file)

def remove_file(filename):
    st.info(f"remove_file called with: {filename}")
    st.session_state["rag"].remove_file(file)

def rag_answer(question, files):
    # Dummy answer: In real use, call your RAG model here
    sources = ', '.join(files) if files else "No sources"
    response = st.session_state["rag"].generate(question)
    return response, sources

# --- Sidebar: File Management ---
st.sidebar.title("Knowledge Base")
uploaded_files = st.sidebar.file_uploader("Browse files", accept_multiple_files=True)

# Store the previous list of files in session state
if "prev_files" not in st.session_state:
    st.session_state["prev_files"] = []

# Store the core RAG in session state
if "rag" not in st.session_state:
    st.session_state["rag"] = Core(EMBEDDING_MODEL, LANGUAGE_MODEL)

# Convert uploaded_files to a list of filenames
current_files = [file.name for file in uploaded_files] if uploaded_files else []

# Detect added files
added_files = [f for f in current_files if f not in st.session_state["prev_files"]]
if added_files:
    add_files(added_files)

# Detect removed files
removed_files = [f for f in st.session_state["prev_files"] if f not in current_files]
for f in removed_files:
    remove_file(f)

# Update the previous file list
st.session_state["prev_files"] = current_files

# --- Main: Perplexity-like RAG UI ---
st.title("💬 Ask your Knowledge Base")

# Store chat history in session state
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

# Chat input
with st.form("rag_chat", clear_on_submit=True):
    question = st.text_input("Ask a question about your knowledge base...", "")
    submitted = st.form_submit_button("Ask")

if submitted and question:
    # Get answer from RAG system (replace with your logic)
    answer, sources = rag_answer(question, current_files)
    # Save to chat history
    st.session_state["chat_history"].append({
        "question": question,
        "answer": answer,
        "sources": sources
    })

# Display chat history (most recent last)
for chat in st.session_state["chat_history"]:
    with st.chat_message("user"):
        st.markdown(f"**You:** {chat['question']}")
    with st.chat_message("assistant"):
        st.markdown(chat["answer"])
        st.caption("Sources:")
        if current_files:
            st.write(
                " ".join(
                    f"`{file}`" for file in current_files
                )
            )
        else:
            st.write("_No files in knowledge base_")

# Show current files as chips/tags at the top
if current_files:
    st.subheader("Knowledge Base Files")
    st.write(
        " ".join(
            f'<span style="background-color:#e0e0e0; border-radius:8px; padding:4px 8px; margin-right:4px;">{file}</span>'
            for file in current_files
        ),
        unsafe_allow_html=True
    )
else:
    st.info("No files in the knowledge base yet. Upload files from the sidebar.")


