import os
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.services.rag_service import RAGService

app = FastAPI(title="Clinical RAG API")
rag_service = RAGService()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Clinical RAG API is running.."}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    try:
        content = await file.read()
        return rag_service.upload_document(file.filename, content)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/documents")
def documents():
    return {"documents": rag_service.list_documents()}

class AskRequest(BaseModel):
    document_id: str
    question: str

@app.post("/ask")
def ask(req: AskRequest):
    try:
        return rag_service.ask(req.document_id, req.question)
    except ValueError as e:
        if str(e) == "Document not found":
            raise HTTPException(status_code=404, detail=str(e))
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)