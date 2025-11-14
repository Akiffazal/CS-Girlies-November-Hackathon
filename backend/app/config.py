import os
from gpt4all import GPT4All

# Load GPT4All-J model (local)
llm = GPT4All("gpt4all-j")

# Upload directory for PDFs
UPLOAD_DIR = os.path.join(os.path.dirname(__file__), '../uploaded_books')
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Path for FAISS vector store
VECTORSTORE_PATH = os.path.join(os.path.dirname(__file__), '../saved_models/vectorstore.faiss')
os.makedirs(os.path.dirname(VECTORSTORE_PATH), exist_ok=True)
