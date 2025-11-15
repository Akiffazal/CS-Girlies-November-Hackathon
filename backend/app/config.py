# import os
# from gpt4all import GPT4All

# # Load GPT4All-J model (local)
# llm = GPT4All("gpt4all-j")

# # Upload directory for PDFs
# UPLOAD_DIR = os.path.join(os.path.dirname(__file__), '../uploaded_books')
# os.makedirs(UPLOAD_DIR, exist_ok=True)

# # Path for FAISS vector store
# VECTORSTORE_PATH = os.path.join(os.path.dirname(__file__), '../saved_models/vectorstore.faiss')
# os.makedirs(os.path.dirname(VECTORSTORE_PATH), exist_ok=True)




# import os

# # Dummy LLM for testing
# class DummyLLM:
#     def generate(self, prompt):
#         return "This is a dummy answer. GPT4All-J is not loaded."

# llm = DummyLLM()

# UPLOAD_DIR = os.path.join(os.path.dirname(__file__), '../uploaded_books')
# os.makedirs(UPLOAD_DIR, exist_ok=True)

# VECTORSTORE_PATH = os.path.join(os.path.dirname(__file__), '../saved_models/vectorstore.faiss')
# os.makedirs(os.path.dirname(VECTORSTORE_PATH), exist_ok=True)








import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()  # load .env variables

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY is missing in .env")

# Initialize Groq client
groq_client = Groq(api_key=GROQ_API_KEY)

# Model name you want to use
GROQ_MODEL = "openai/gpt-oss-20b"

UPLOAD_DIR = os.path.join(os.path.dirname(__file__), '../uploaded_books')
os.makedirs(UPLOAD_DIR, exist_ok=True)

VECTORSTORE_PATH = os.path.join(os.path.dirname(__file__), '../saved_models/vectorstore.faiss')
