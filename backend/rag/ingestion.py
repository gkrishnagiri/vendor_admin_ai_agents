import os
import psycopg2
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

conn = psycopg2.connect(os.getenv("DATABASE_URL"))
cur = conn.cursor()


def chunk_text(text, chunk_size=500):
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]


def get_embedding(text):
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return response.data[0].embedding


def ingest_document(name, content):
    # Insert document
    cur.execute(
        "INSERT INTO documents (name, content) VALUES (%s, %s) RETURNING id",
        (name, content)
    )
    doc_id = cur.fetchone()[0]

    chunks = chunk_text(content)

    for chunk in chunks:
        embedding = get_embedding(chunk)

        cur.execute(
            "INSERT INTO chunks (document_id, content, embedding) VALUES (%s, %s, %s)",
            (doc_id, chunk, embedding)
        )

    conn.commit()
    print(f"Inserted document: {name}")