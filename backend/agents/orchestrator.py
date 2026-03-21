from services.intent_classifier import classify_intent
from rag.retriever import search


def orchestrate(query: str, trace=None, top_k=3):

    print(f"\n[Orchestrator] Received query: {query}")

    intent = classify_intent(query, trace)

    print(f"[Orchestrator] Detected Intent: {intent}")

    if intent == "RAG":
        return search(query, top_k, trace)

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