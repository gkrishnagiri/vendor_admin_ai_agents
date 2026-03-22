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
            f"{i+1}. {chunk['content'][:100]}"
            for i, chunk in enumerate(context_chunks)
        ])

        print("\n[RAG] Context sent to LLM:")
        print(context_text[:500])

        prompt = f"""
Use the context to answer the question.

Context:
{context_text}

Question:
{query}

Answer:
"""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )

        answer = response.choices[0].message.content

        print(f"\n[RAG] LLM Answer:\n{answer}")

        return answer