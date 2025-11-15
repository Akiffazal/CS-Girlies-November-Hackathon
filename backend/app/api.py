from fastapi import APIRouter
from pydantic import BaseModel
from app.vectorstore import search_similar_chunks
from app.config import groq_client, GROQ_MODEL

router = APIRouter()

class QuestionRequest(BaseModel):
    question: str

@router.post("/ask")
async def ask_question(req: QuestionRequest):
    question = req.question

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
            {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}\nAnswer:"}
        ],
        temperature=0.3,
        max_completion_tokens=512
    )

    answer = completion.choices[0].message.content

    return {"answer": answer}
