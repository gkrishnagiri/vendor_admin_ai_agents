from fastapi import APIRouter
from pydantic import BaseModel
from vendor_admin_agents.orchestrator import orchestrate
from agents.tracing import trace

router = APIRouter()


class QueryRequest(BaseModel):
    query: str
    top_k: int = 3


@router.post("/query")
def query_rag(request: QueryRequest):

    return orchestrate(request.query, top_k=request.top_k)