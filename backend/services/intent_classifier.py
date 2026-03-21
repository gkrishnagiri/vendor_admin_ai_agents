from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def classify_intent(query: str):
    """
    Classify user intent into:
    - RAG (question / info)
    - ACTION (UI operation)
    """

    prompt = f"""
Classify the user query into one of the following categories:

1. RAG → informational question (how, what, why, explain)
2. ACTION → user wants to perform an action (create, update, delete, click, open)

Respond with ONLY one word: RAG or ACTION

---

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