from services.intent_classifier import classify_intent
from rag.retriever import search


def orchestrate(query: str, trace=None):
    """
    Main brain of the system
    """

    intent = classify_intent(query, trace)

    print(f"[Orchestrator] Intent: {intent}")

    if intent == "RAG":
        return search(query, trace)

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