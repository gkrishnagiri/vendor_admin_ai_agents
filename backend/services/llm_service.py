from openai import OpenAI
import os
from dotenv import load_dotenv
from services.tracing import start_span, end_span

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_answer(query: str, context_chunks: list, trace=None):
    """
    Generate final answer using LLM
    """

    span = start_span(trace, "rag_answer_generation")

    try:
        context_text = "\n\n".join([
            f"{i+1}. {chunk['content']}"
            for i, chunk in enumerate(context_chunks)
        ])

        prompt = f"""
You are an AI assistant helping with an admin system.

Use the provided context to answer the question.

IMPORTANT RULES:
- You can rephrase and summarize the content.
- You can infer meaning if wording is slightly different.
- Do NOT say "not found" unless context is unrelated.

Context:
{context_text}

Question:
{query}

Answer clearly:
"""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful admin assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )

        return response.choices[0].message.content

    finally:
        end_span(span)