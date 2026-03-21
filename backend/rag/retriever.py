import os
import psycopg2
from dotenv import load_dotenv
from openai import OpenAI
from services.llm_service import generate_answer

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def get_embedding(text):
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return response.data[0].embedding


def search(query, top_k=3, trace=None):
    conn = psycopg2.connect(os.getenv("DATABASE_URL"))
    cur = conn.cursor()

    query_embedding = get_embedding(query)
    embedding_str = "[" + ",".join(map(str, query_embedding)) + "]"

    # 🔥 IMPORTANT: include document name for source
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

    # Prepare context for LLM
    context_chunks = [
        {"content": r[0], "source": r[1]}
        for r in results
    ]

    # 🔥 LLM CALL
    answer = generate_answer(query, context_chunks, trace)
    
    return {
        "query": query,
        "answer": answer,
        "sources": [c["source"] for c in context_chunks]
    }