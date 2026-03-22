import os
import psycopg2
from dotenv import load_dotenv
from openai import OpenAI
from services.llm_service import generate_answer
from agents.tracing import trace

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def get_embedding(text):

    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return response.data[0].embedding


def search(query, top_k=3):

    conn = psycopg2.connect(os.getenv("DATABASE_URL"))
    cur = conn.cursor()

    query_embedding = get_embedding(query)
    embedding_str = "[" + ",".join(map(str, query_embedding)) + "]"

    cur.execute("""
        SELECT c.content, d.name
        FROM chunks c
        JOIN documents d ON c.document_id = d.id
        ORDER BY c.embedding <-> %s::vector
        LIMIT %s
    """, (embedding_str, top_k))

    results = cur.fetchall()

    cur.close()
    conn.close()

    context_chunks = [
        {"content": r[0], "source": r[1]}
        for r in results
    ]

    answer = generate_answer(query, context_chunks)

    return {
        "query": query,
        "answer": answer,
        "sources": [c["source"] for c in context_chunks]
    }