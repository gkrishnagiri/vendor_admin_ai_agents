from fastapi import APIRouter
from pydantic import BaseModel
from rag.retriever import search
from services.tracing import start_trace, end_trace

router = APIRouter()


class QueryRequest(BaseModel):
    query: str
    top_k: int = 3


@router.post("/query")
def query_rag(request: QueryRequest):
    trace = start_trace("rag_query")

    try:
        result = search(request.query, request.top_k)
        return result

    finally:
        end_trace(trace)