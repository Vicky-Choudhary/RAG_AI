from pathlib import Path
import pymupdf4llm
from hashlib import sha256
from datetime import datetime, timezone


def load_pdf(pdf_path: str) -> list[dict]:
    """Return one dict per non-empty page: {'page': int, 'text': str, 'source': str}."""
    path = Path(pdf_path)

    if not path.is_file():
        raise FileNotFoundError(path)

    document_id = str(path)
    source_uri = str(path)

    with open(path, "rb") as f:
        file_bytes = f.read()

    content_hash = sha256(file_bytes).hexdigest()
    document_version = 1
    ingested_at = datetime.now(timezone.utc).isoformat()

    
    pages = pymupdf4llm.to_markdown(path, page_chunks=True)

    records = []
    for page in pages:
        text = page["text"].strip()
        if not text:
            continue
        records.append({
            # Page level metadata
            "page": page["metadata"]["page_number"],
            "text": text,

            # Document level metadata
            "document_id": document_id,
            "source_uri": source_uri,
            "document_version": document_version,
            "content_hash": content_hash,
            "ingested_at": ingested_at
        })
    return records
