import os
import re
import psycopg2
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

conn = psycopg2.connect(os.getenv("DATABASE_URL"))
cur = conn.cursor()


# -----------------------------
# 🔹 SECTION-BASED CHUNKING
# -----------------------------
def split_into_sections(text):
    """
    Split document into logical sections using headings
    """

    # Split on ALL CAPS headings or numbered headings
    sections = re.split(r'\n(?=[A-Z0-9][A-Z0-9\s\.\-→:]+)\n', text)

    cleaned = []
    for sec in sections:
        sec = sec.strip()
        if len(sec) > 50:
            cleaned.append(sec)

    return cleaned


# -----------------------------
# 🔹 OVERLAP CHUNKING
# -----------------------------
def chunk_with_overlap(text, chunk_size=800, overlap=150):
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap

    return chunks


# -----------------------------
# 🔹 FINAL CHUNK PIPELINE
# -----------------------------
def create_chunks(text):
    sections = split_into_sections(text)

    final_chunks = []

    for section in sections:
        if len(section) > 1000:
            # break large sections
            final_chunks.extend(chunk_with_overlap(section))
        else:
            final_chunks.append(section)

    return final_chunks


# -----------------------------
# 🔹 EMBEDDING
# -----------------------------
def get_embedding(text):
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return response.data[0].embedding


# -----------------------------
# 🔹 INGEST DOCUMENT
# -----------------------------
def ingest_document(name, content):

    # 🔥 OPTIONAL: delete existing doc (prevents duplicates)
    cur.execute("DELETE FROM documents WHERE name = %s RETURNING id", (name,))
    existing = cur.fetchone()

    if existing:
        doc_id = existing[0]
        cur.execute("DELETE FROM chunks WHERE document_id = %s", (doc_id,))
        print(f"Deleting existing document chunks: {name}")

    # Insert document
    cur.execute(
        "INSERT INTO documents (name, content) VALUES (%s, %s) RETURNING id",
        (name, content)
    )
    doc_id = cur.fetchone()[0]

    # 🔥 NEW CHUNKING
    chunks = create_chunks(content)

    print(f"Total chunks created: {len(chunks)}")

    for i, chunk in enumerate(chunks):
        embedding = get_embedding(chunk)

        cur.execute(
            "INSERT INTO chunks (document_id, content, embedding) VALUES (%s, %s, %s)",
            (doc_id, chunk, embedding)
        )

    conn.commit()
    print(f"Inserted document: {name}")