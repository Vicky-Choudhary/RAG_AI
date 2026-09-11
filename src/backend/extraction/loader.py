from pathlib import Path
import pymupdf4llm


def load_pdf(pdf_path: str) -> list[dict]:
    """Return one dict per non-empty page: {'page': int, 'text': str, 'source': str}."""
    path = Path(pdf_path)
    source = path.name
    if not path.is_file():
        raise FileNotFoundError(path)
    pages = pymupdf4llm.to_markdown(path, page_chunks=True)

    records = []
    for page in pages:
        text = page["text"].strip()
        if not text:
            continue
        records.append({
            "page": page["metadata"]["page_number"],
            "text": text,
            "source": source,
        })
    return records
