from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from qa import ICHGuidelineQA  # 同じディレクトリのqa.pyから直接import

app = FastAPI(title="ICH Guidelines RAG API")

# リクエストモデル
class QuestionRequest(BaseModel):
    question: str

# レスポンスモデル
class Source(BaseModel):
    title: str
    code: str
    category: str
    source_file: Optional[str]
    preview: str

class RAGResponse(BaseModel):
    answer: str
    sources: List[Source]
    
# QAシステムのグローバルインスタンス
qa_system = ICHGuidelineQA(persist_directory="/vectorstore/ich_db")

@app.post("/rag", response_model=RAGResponse)
async def get_rag_response(request: QuestionRequest):
    try:
        answer = qa_system.answer_question(request.question)
        sources = qa_system.get_relevant_sources(request.question)
        
        return RAGResponse(
            answer=answer,
            sources=sources
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred: {str(e)}"
        )