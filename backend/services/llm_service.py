from openai import OpenAI
import os
from dotenv import load_dotenv
from agents.tracing import trace

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_answer(query: str, context_chunks: list):

    print(f"\n[RAG] Generating answer for query: {query}")

    with trace("rag_answer_generation"):

        context_text = "\n\n".join([
            f"{i+1}. {chunk['content']}"
            for i, chunk in enumerate(context_chunks)
        ])

        print("\n[RAG] Context sent to LLM:")
        print(context_text)

        prompt = f"""
You are an AI assistant.

Answer the question using ONLY the provided context.

IMPORTANT:
- Extract steps if available
- Do NOT ignore relevant sections
- Provide clear step-by-step instructions

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
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2
        )

        answer = response.choices[0].message.content

        print(f"\n[RAG] LLM Answer:\n{answer}")

        return answer