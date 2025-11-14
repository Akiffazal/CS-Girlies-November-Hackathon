# embeddings.py
import os
import openai
from dotenv import load_dotenv
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
EMBED_MODEL = os.getenv("OPENAI_EMBED_MODEL", "text-embedding-3-small")
openai.api_key = OPENAI_API_KEY

def get_embedding(text: str):
    resp = openai.Embedding.create(model=EMBED_MODEL, input=text)
    return resp['data'][0]['embedding']
