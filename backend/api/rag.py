from fastapi import APIRouter
from pydantic import BaseModel
from rag.retriever import search

router = APIRouter()


class QueryRequest(BaseModel):
    query: str
    top_k: int = 3


@router.post("/query")
def query_rag(request: QueryRequest):
    results = search(request.query, request.top_k)

    return {
        "query": request.query,
        "results": results
    }