from pathlib import Path
import pymupdf4llm


def load_pdf(pdf_path: str) -> list[dict]:
    """Return one dict per non-empty page: {'page': int, 'text': str, 'source': str}."""
    path = Path(pdf_path)
    if not path.is_file():
        raise FileNotFoundError(path)
    markdown = pymupdf4llm.to_markdown(path)
    return markdown
