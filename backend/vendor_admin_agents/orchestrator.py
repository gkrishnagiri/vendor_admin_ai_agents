from services.intent_classifier import classify_intent
from rag.retriever import search
from agents.tracing import trace


def orchestrate(query: str, top_k=3):

    print(f"\n[Orchestrator] Received query: {query}")

    intent = classify_intent(query)

    print(f"[Orchestrator] Detected Intent: {intent}")

    if intent == "RAG":
        return search(query, top_k)

    elif intent == "ACTION":
        return {
            "message": "UI actions not implemented yet",
            "intent": intent
        }

    else:
        return {
            "message": "Could not determine intent",
            "intent": intent
        }