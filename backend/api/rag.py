from fastapi import APIRouter
from pydantic import BaseModel
from agents.orchestrator import orchestrate
from services.tracing import start_trace, end_trace

router = APIRouter()


class QueryRequest(BaseModel):
    query: str
    top_k: int = 3   # ✅ added back


@router.post("/query")
def query_rag(request: QueryRequest):
    trace = start_trace("orchestrator")

    try:
        result = orchestrate(request.query, trace, request.top_k)
        return result

    finally:
        end_trace(trace)