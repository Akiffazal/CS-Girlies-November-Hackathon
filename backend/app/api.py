from fastapi import APIRouter, UploadFile, File
from app.utils import load_pdf
from app.vectorstore import save_chunks, search_similar_chunks
from app.config import groq_client, GROQ_MODEL

router = APIRouter()

@router.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    content = await file.read()
    text_chunks = load_pdf(content)
    save_chunks(text_chunks)
    return {"message": "PDF uploaded and processed"}


@router.post("/ask")
async def ask_question(question: str):
    # Search similar text from vectorstore (RAG retrieval)
    context = search_similar_chunks(question, top_k=3)

    # Safety guard: limit context length
    if len(context) > 4000:
        context = context[:4000]


    # LLM call using Groq
    completion = groq_client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {
                "role": "user",
                "content": f"Context:\n{context}\n\nQuestion: {question}\nAnswer:"
            }
        ],
        temperature=0.3,
        max_completion_tokens=512
    )

    answer = completion.choices[0].message.content

    return {"answer": answer}












# from fastapi import APIRouter, UploadFile, File
# from app.utils import load_pdf
# from app.vectorstore import save_chunks, search_similar_chunks
# from app.config import llm

# router = APIRouter()

# @router.post("/upload")
# async def upload_pdf(file: UploadFile = File(...)):
#     content = await file.read()
#     text_chunks = load_pdf(content)
#     save_chunks(text_chunks)
#     return {"message": "PDF uploaded and processed"}

# @router.post("/ask")
# async def ask_question(question: str):
#     context = search_similar_chunks(question)
#     answer = llm.generate(f"Context:\n{context}\n\nQuestion: {question}\nAnswer:")
#     return {"answer": answer}
