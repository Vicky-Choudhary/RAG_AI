from pathlib import Path
from pypdf import PdfReader


def load_pdf(pdf_path: str) -> list[dict]:
    """Return one dict per non-empty page: {'page': int, 'text': str, 'source': str}."""
    path = Path(pdf_path)
    if not path.is_file():
        raise FileNotFoundError(path)

    reader = PdfReader(str(path))
    pages = []
    for i, page in enumerate(reader.pages, start=1):
        text = (page.extract_text() or "").strip()
        if text:
            pages.append({"page": i, "text": text, "source": str(path)})
    return pages
