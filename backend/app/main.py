# main.py
import os
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from extraction import extract_text_from_pdf, chunk_text_pages
from embeddings import get_embedding
from vectorstore import create_faiss_index, save_index, load_index, add_embeddings_to_index
from prompts import SYSTEM_PROMPT, ANSWER_PROMPT
from schemas import UploadResponse, AskRequest, AnswerResponse
import numpy as np
import openai
import pickle
from dotenv import load_dotenv
load_dotenv()

app = FastAPI(title="AskYourBook API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

DATA_DIR = os.getenv("DATA_DIR", "./data")
os.makedirs(DATA_DIR, exist_ok=True)
META_PATH = os.path.join(DATA_DIR, "meta.pkl")
INDEX_PATH = os.path.join(DATA_DIR, "faiss.index")

# load or init
index, metadata = load_index()
if index is None:
    # We will set dim after first embedding creation
    index = None
    metadata = []

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY
EMBED_DIM = None  # set after first embedding

@app.post("/upload", response_model=UploadResponse)
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files accepted")
    saved_path = os.path.join(DATA_DIR, file.filename)
    with open(saved_path, "wb") as f:
        f.write(await file.read())
    # Extract and chunk
    pages = extract_text_from_pdf(saved_path)
    chunks = chunk_text_pages(pages, chunk_size=int(os.getenv("CHUNK_SIZE",800)), overlap=int(os.getenv("CHUNK_OVERLAP",150)))
    # Create embeddings for chunks
    embeddings = []
    meta_entries = []
    global index, metadata, EMBED_DIM
    for c in chunks:
        emb = get_embedding(c['text'])
        embeddings.append(emb)
        meta_entries.append({'id': c['id'], 'page': c['page'], 'text': c['text']})
    emb_dim = len(embeddings[0])
    EMBED_DIM = emb_dim
    if index is None:
        index = create_faiss_index(emb_dim)
    # add and persist
    import numpy as np
    arr = np.array(embeddings).astype('float32')
    index.add(arr)
    # append metadata
    metadata.extend(meta_entries)
    save_index(index, metadata)
    return UploadResponse(success=True, message=f"Uploaded and indexed {len(chunks)} chunks from {file.filename}")

@app.post("/ask", response_model=AnswerResponse)
async def ask(req: AskRequest):
    question = req.question
    top_k = req.top_k
    # embed question
    q_emb = get_embedding(question)
    import numpy as np
    vec = np.array(q_emb).astype('float32').reshape(1, -1)
    # retrieve
    D, I = index.search(vec, top_k)
    I = I[0].tolist()
    retrieved = []
    for idx in I:
        if idx < len(metadata):
            retrieved.append(metadata[idx])
    # build context text
    context_snippets = []
    for r in retrieved:
        context_snippets.append(f"[page {r['page']}]: {r['text'][:800]}")  # first 800 chars to limit prompt
    context_text = "\n\n".join(context_snippets)
    # call chat model
    prompt = ANSWER_PROMPT.format(context=context_text, question=question)
    messages = [
        {"role":"system", "content": SYSTEM_PROMPT},
        {"role":"user", "content": prompt}
    ]
    resp = openai.ChatCompletion.create(
        model=os.getenv("OPENAI_CHAT_MODEL", "gpt-4o-mini"),
        messages=messages,
        max_tokens=400,
        temperature=0.0
    )
    answer = resp['choices'][0]['message']['content'].strip()
    # prepare citations: include page numbers from retrieved
    citations = [{'page': r['page'], 'text': r['text'][:400]} for r in retrieved]
    return AnswerResponse(answer=answer, citations=citations)
