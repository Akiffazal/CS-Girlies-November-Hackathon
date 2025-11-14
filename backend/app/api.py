from fastapi import APIRouter, UploadFile, File
from app.utils import load_pdf
from app.vectorstore import save_chunks, search_similar_chunks
from app.config import llm

router = APIRouter()

@router.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    content = await file.read()
    text_chunks = load_pdf(content)
    save_chunks(text_chunks)
    return {"message": "PDF uploaded and processed"}

@router.post("/ask")
async def ask_question(question: str):
    context = search_similar_chunks(question)
    answer = llm.generate(f"Context:\n{context}\n\nQuestion: {question}\nAnswer:")
    return {"answer": answer}
