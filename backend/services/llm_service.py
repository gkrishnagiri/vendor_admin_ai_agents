from openai import OpenAI
import os

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

Answer the user query based ONLY on the context below.

If the answer is not found, say:
"I could not find this in the documentation."

---

Context:
{context_text}

---

Question:
{query}

---

Answer:
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful admin assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )

    return response.choices[0].message.content