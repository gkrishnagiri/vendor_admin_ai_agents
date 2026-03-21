from fastapi import FastAPI
from api.rag import router as rag_router

app = FastAPI(title="Vendor Admin AI Agents")

app.include_router(rag_router, prefix="/rag")


@app.get("/")
def root():
    return {"message": "AI Agent Backend Running"}


@app.get("/health")
def health():
    return {"status": "ok"}