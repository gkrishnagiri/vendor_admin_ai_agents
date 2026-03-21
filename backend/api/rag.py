from fastapi import APIRouter
from pydantic import BaseModel
from agents.orchestrator import orchestrate
from services.tracing import start_trace, end_trace

router = APIRouter()


class QueryRequest(BaseModel):
    query: str


@router.post("/query")
def query_rag(request: QueryRequest):
    trace = start_trace("orchestrator")

    try:
        result = orchestrate(request.query)
        return result

    finally:
        end_trace(trace)