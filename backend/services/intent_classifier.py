from openai import OpenAI
import os
from dotenv import load_dotenv
from services.tracing import start_span, end_span

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def classify_intent(query: str, trace=None):
    """
    Classify user intent into:
    - RAG
    - ACTION
    """

    span = start_span(trace, "intent_classification")

    try:
        prompt = f"""
Classify the user query into one of the following categories:

1. RAG → informational question
2. ACTION → user wants to perform an action

Respond with ONLY one word: RAG or ACTION

Query:
{query}
"""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an intent classifier."},
                {"role": "user", "content": prompt}
            ],
            temperature=0
        )

        return response.choices[0].message.content.strip()

    finally:
        end_span(span)