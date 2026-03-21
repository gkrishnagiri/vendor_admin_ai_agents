from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_answer(query: str, context_chunks: list):
    """
    Generate final answer using LLM
    """

    context_text = "\n\n".join([
        f"{i+1}. {chunk['content']}"
        for i, chunk in enumerate(context_chunks)
    ])

    prompt = f"""
You are an AI assistant helping with an admin system.

Use the provided context to answer the question.

IMPORTANT RULES:
- You can rephrase and summarize the content.
- You can infer meaning if wording is slightly different (e.g., "amend" = "update").
- Do NOT say "not found" unless the context is completely unrelated.
- Prefer giving a helpful answer based on available context.

---

Context:
{context_text}

---

Question:
{query}

---

Answer clearly and helpfully:
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful admin assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3   # 🔥 slightly increased for better reasoning
    )

    return response.choices[0].message.content