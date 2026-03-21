import os
import psycopg2
from dotenv import load_dotenv
from openai import OpenAI

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
        SELECT content
        FROM chunks
        ORDER BY embedding <-> %s::vector
        LIMIT %s
    """, (embedding_str, top_k))

    results = cur.fetchall()

    cur.close()
    conn.close()

    return [r[0] for r in results]