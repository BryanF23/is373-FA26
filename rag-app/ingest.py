"""Import approved .txt, .md, and .pdf documents into PostgreSQL + pgvector.

Put files in data/sources/ and add their public source URL to sources.json.
Only ingest documents you are allowed to use for this class project.
"""
import json
import os
import re
from pathlib import Path

import psycopg2
from openai import OpenAI
from pgvector.psycopg2 import register_vector
from pypdf import PdfReader

ROOT = Path(__file__).parent
SOURCE_DIR = ROOT / "data" / "sources"
MANIFEST = ROOT / "data" / "sources.json"
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://raguser:ragpass@localhost:5432/xrlab")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")
EMBEDDING_DIMENSIONS = int(os.getenv("EMBEDDING_DIMENSIONS", "1536"))
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "1200"))


def read_document(path):
    if path.suffix.lower() == ".pdf":
        reader = PdfReader(str(path))
        return "\n".join(page.extract_text() or "" for page in reader.pages)
    return path.read_text(encoding="utf-8")


def split_into_chunks(text, max_chars=CHUNK_SIZE):
    # Start with paragraph-aware chunks. Keep each paragraph intact when possible.
    paragraphs = [re.sub(r"\s+", " ", p).strip() for p in text.splitlines() if p.strip()]
    chunks, current = [], ""
    for paragraph in paragraphs:
        if len(paragraph) > max_chars:
            if current:
                chunks.append(current)
                current = ""
            for start in range(0, len(paragraph), max_chars):
                chunks.append(paragraph[start:start + max_chars])
            continue
        candidate = f"{current}\n{paragraph}".strip() if current else paragraph
        if len(candidate) > max_chars and current:
            chunks.append(current)
            current = paragraph
        else:
            current = candidate
    if current:
        chunks.append(current)
    return chunks


def main():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise SystemExit("Set OPENAI_API_KEY in your local .env file before ingesting.")
    if not MANIFEST.exists():
        raise SystemExit("Missing data/sources.json. Add metadata for each source file.")

    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    client = OpenAI(api_key=api_key)
    connection = psycopg2.connect(DATABASE_URL)
    register_vector(connection)

    try:
        with connection:
            with connection.cursor() as cursor:
                for item in manifest:
                    filename = item["filename"]
                    path = SOURCE_DIR / filename
                    if not path.exists():
                        print(f"Skipping missing file: {filename}")
                        continue
                    if not item.get("approved", False):
                        print(f"Skipping source not marked approved: {filename}")
                        continue

                    title = item["title"]
                    source_url = item.get("source_url", "")
                    text = read_document(path)
                    chunks = split_into_chunks(text)
                    if not chunks:
                        print(f"No extractable text: {filename}")
                        continue

                    cursor.execute(
                        """
                        INSERT INTO documents (title, source_url, filename, publisher, version_label)
                        VALUES (%s, %s, %s, %s, %s)
                        ON CONFLICT (filename) DO UPDATE SET
                            title = EXCLUDED.title,
                            source_url = EXCLUDED.source_url,
                            publisher = EXCLUDED.publisher,
                            version_label = EXCLUDED.version_label,
                            imported_at = NOW()
                        RETURNING id
                        """,
                        (title, source_url, filename, item.get("publisher", ""),
                         item.get("version_label", "")),
                    )
                    document_id = cursor.fetchone()[0]
                    cursor.execute("DELETE FROM chunks WHERE document_id = %s", (document_id,))

                    for index, chunk in enumerate(chunks):
                        response = client.embeddings.create(
                            model=EMBEDDING_MODEL,
                            input=chunk,
                            dimensions=EMBEDDING_DIMENSIONS,
                        )
                        vector = response.data[0].embedding
                        cursor.execute(
                            """
                            INSERT INTO chunks
                                (document_id, chunk_index, section_title, content, embedding, embedding_model)
                            VALUES (%s, %s, %s, %s, %s, %s)
                            """,
                            (document_id, index, title, chunk, vector, EMBEDDING_MODEL),
                        )
                    print(f"Imported {filename}: {len(chunks)} chunks")
    finally:
        connection.close()


if __name__ == "__main__":
    main()
