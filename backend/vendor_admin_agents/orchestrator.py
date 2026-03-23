from services.intent_classifier import classify_intent
from rag.retriever import search
from vendor_admin_agents.planner_agent import plan_actions
from vendor_admin_agents.executor import Executor


def orchestrate(query: str, top_k=3):

    print(f"\n[Orchestrator] Query: {query}")

    intent = classify_intent(query)

    print(f"[Orchestrator] Intent: {intent}")

    if intent == "RAG":
        return search(query, top_k)

    elif intent == "ACTION":

        plan = plan_actions(query)

        print("[Orchestrator] Plan:", plan)

        executor = Executor()
        execution_result = executor.execute(plan)

        return {
            "intent": "ACTION",
            "plan": plan,
            "execution": execution_result
        }

    else:
        return {
            "message": "Could not determine intent",
            "intent": intent
        }