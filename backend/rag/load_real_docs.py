import os
from docx import Document
from ingestion import ingest_document

DOCS_PATH = "../docs/uploaded_docs"


def read_docx(file_path):
    doc = Document(file_path)
    return "\n".join([para.text for para in doc.paragraphs])


def read_sql(file_path):
    with open(file_path, "r") as f:
        return f.read()


def load_all_docs():
    for file in os.listdir(DOCS_PATH):
        full_path = os.path.join(DOCS_PATH, file)

        print(f"Processing: {file}")

        if file.endswith(".docx"):
            content = read_docx(full_path)

        elif file.endswith(".sql"):
            content = read_sql(full_path)

        else:
            print(f"Skipping unsupported file: {file}")
            continue

        ingest_document(file, content)


if __name__ == "__main__":
    load_all_docs()